"""Regime composition: transformers as certified nodes, and routing as a record (``docs/20``).

The calculus is regime-relative (question-relative sufficiency, ``docs/04``;
access-relative observability, ``docs/08``/``10``), so each expert node is
certified *for its regime* by the same theorem. Two consequences are made exact
here:

- **per-regime precision** — a regime with a coarse margin tolerates a coarse
  truncation grid (``docs/19``), so the aggregate bit budget is the *sum* over
  regimes, not the max: routing/regimes refine bit usage when margins differ;
- **routing is a record** — the router's choice is a record (``docs/01``), and
  hard routing (sum of maps) versus soft routing (recombination) are *different*
  maps (``docs/05``): the certified global law depends on the routing type.
"""

from fractions import Fraction

from . import transformer as tr
from . import truncate as tc
from . import forgetting as fg
from . import instruments as ins

GRID_CHOICES = (4, 8, 16, 32, 64, 128, 256, 512)


def _regime_inputs():
    return tr.TOY_DATA[0][0], tr.TOY_DATA[2][0], [X for X, _ in tr.TOY_DATA]


def coarsest_safe_grid(ws, margin, choices=GRID_CHOICES):
    """Coarsest truncation grid whose **certified** separation ``D - 2e`` still meets ``margin``.

    Uses the rate-two certificate ``D - 2e >= margin`` (``docs/09``, ``docs/19``),
    which is monotone in the margin; coarse grids whose distortion breaks it (or
    that degenerate the model) are rejected.
    """
    X_a, X_b, inputs = _regime_inputs()
    D = tc.separation(ws, X_a, X_b)
    for n in choices:
        wq = tc.truncate(ws, n)
        try:
            e = tc.output_distortion(ws, wq, inputs)
        except ZeroDivisionError:
            continue
        if (D - 2 * e) >= margin:
            return n
    return None


def regime_precision(margins, steps=2, eta=Fraction(1, 50)):
    """Per-regime bit budgets (``docs/20``).

    For each declared margin, the coarsest safe grid and its denominator bits.
    ``modular_bits`` is the sum over regimes (separate nodes); ``monolithic_bits``
    is the finest regime applied everywhere. The two agree iff the margins are
    homogeneous.
    """
    ws = tr.train_exact(tr.TOY_DATA, steps=steps, eta=eta)[-1][0]
    rows = []
    for t in margins:
        n = coarsest_safe_grid(ws, t)
        bits = tc.denominator_bits(tc.truncate(ws, n)) if n is not None else None
        rows.append({"margin": t, "grid": n, "bits": bits})
    have = [r["bits"] for r in rows if r["bits"] is not None]
    modular = sum(have) if have else None
    monolithic = len(have) * max(have) if have else None
    return {
        "per_regime": rows,
        "modular_bits": modular,
        "monolithic_bits": monolithic,
        "saving": (monolithic - modular) if have else None,
    }


def routing_laws():
    """Hard routing (sum of maps) vs soft routing (recombination) on the same experts (``docs/05``).

    The router's choice is a record; discarding it (hard) is a sum of *maps*,
    keeping the amplitudes (soft) is a *recombination*. They differ.
    """
    rho = ins.rho_plus()
    hard = fg.incoherent_sum([fg.D0, fg.D1], rho)
    soft = fg.coherent_recombination([fg.D0, fg.D1], rho)
    return {"hard": hard, "soft": soft, "differ": hard != soft}
