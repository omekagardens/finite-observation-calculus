"""Certified truncation: the calculus's error budget bounds exact bit growth (``docs/19``).

Exact training grows denominators without bound (``docs/18``). The calculus
supplies the precision it is worth keeping: an observation distortion ``e``
erodes a separation at **rate two** (``docs/09`` §3) and anything below the
**margin** is in the annihilator, hence not certifiable (``docs/08`` §4,
``docs/11``). So rounding every weight to a grid of quantum ``1/n``:

- bounds the denominators at ``log2(n)`` bits (independent of the step count);
- changes any **separation** by at most ``2 e`` (the triangle inequality, the
  rate-two bound), where ``e`` is the induced output distortion;
- therefore preserves any verdict "separated by ``>= t``" whenever ``2 e < D - t``.

Truncation is a *certified fixed-point* scheme: not exact, but the error is
bounded and known.
"""

from fractions import Fraction

from . import transformer as tr


def truncate(ws, n):
    """Round every weight to the nearest multiple of ``1/n`` (exact, ties to even)."""
    return [Fraction(round(x * n), n) for x in ws]


def denominator_bits(ws):
    """Max denominator bit length across the weights."""
    return max(w.denominator.bit_length() for w in ws)


def separation(ws, X_a, X_b):
    """The observable separation between two inputs: ``|f(X_a) - f(X_b)|``."""
    return abs(tr.predict(ws, X_a) - tr.predict(ws, X_b))


def output_distortion(ws, ws_q, inputs):
    """Max output change from truncating ``ws`` to ``ws_q`` (the distortion ``e``)."""
    return max(abs(tr.predict(ws_q, X) - tr.predict(ws, X)) for X in inputs)


def certified_truncation(steps=2, eta=Fraction(1, 50), grids=(16, 32, 64, 96, 128, 192, 256)):
    """Train exactly, then truncate to coarser and coarser grids (``docs/19``).

    The verdict is "the two inputs are separated by ``>= t``" for ``t = D/2``;
    for each grid the function reports the induced distortion ``e``, the eroded
    separation, whether the rate-two bound ``erosion <= 2e`` holds, and whether
    the verdict survives. A grid coarse enough to zero out the attention scores
    degenerates the model (reported as ``degenerate``).
    """
    ws = tr.train_exact(tr.TOY_DATA, steps=steps, eta=eta)[-1][0]
    X_a, X_b = tr.TOY_DATA[0][0], tr.TOY_DATA[2][0]
    inputs = [X for X, _ in tr.TOY_DATA]
    D = separation(ws, X_a, X_b)
    margin = D / 2
    rows = []
    for n in grids:
        wq = truncate(ws, n)
        try:
            e = output_distortion(ws, wq, inputs)
            Dq = separation(wq, X_a, X_b)
        except ZeroDivisionError:
            rows.append({"grid": n, "bits": denominator_bits(wq), "e": None,
                         "separation": Fraction(0), "erosion": D,
                         "rate_two_ok": None, "verdict_ok": False, "degenerate": True})
            continue
        erosion = D - Dq
        rows.append({
            "grid": n,
            "bits": denominator_bits(wq),
            "e": e,
            "separation": Dq,
            "erosion": erosion,
            "rate_two_ok": erosion <= 2 * e,
            "verdict_ok": Dq >= margin,
            "degenerate": False,
        })
    return {"exact_bits": denominator_bits(ws), "separation": D, "margin": margin, "rows": rows}
