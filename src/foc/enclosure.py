"""Exact finite enclosures and their error decomposition (``docs/31``).

An observation is a lossy trace (``docs/01``). When the trace is a *geometric*
one — which cells of a supplied partition fall inside a query — the loss splits
into exactly three signed parts, and each part has an exact certificate.

The results:

- **bracketing** (``docs/31`` §2): with ``L = sum(inner areas)``,
  ``U = sum(outer areas)`` and ``G = sum(representative areas)``,
  ``L <= G <= U`` and ``L <= V <= U`` for the true query volume ``V`` — so
  ``|G - V| <= gap = U - L``.  ``G`` and ``V`` are *not* ordered.
- **refinement monotonicity** (``docs/31`` §3): a nested refinement raises ``L``,
  lowers ``U`` and shrinks the ``gap`` — but the *representative* quadrature error
  need not shrink, and the module carries the exact counterexample.
- **three-way error identity** (``docs/31`` §4):
  ``mean - V = (mean - T) + (T - G) + (G - V)`` — sampling bias + annotation +
  quadrature, each signed and retained.
- **kernel discrepancy** (``docs/31`` §5):
  ``P_g - J = (P_g - K) + (K - Jcross) - Jdiag`` — boundary + cross-order +
  omission errors of the discrete bilinear measure.
"""

from fractions import Fraction


# --- 1. bracketing -----------------------------------------------------------

def bounds(areas, inner, outer, representative):
    """The three sums and the gap from boolean membership masks.

    ``inner[i]`` is true when cell ``i`` lies inside the probe (up to zero-area
    boundaries); ``outer[i]`` when its clipped intersection has positive area;
    ``representative[i]`` when its representative lies strictly inside the probe.
    """
    def sel(mask):
        return sum(areas[i] for i in range(len(areas)) if mask[i])
    lower, upper, rep = sel(inner), sel(outer), sel(representative)
    return {"lower": lower, "upper": upper, "representative": rep, "gap": upper - lower}


def certify(b, volume):
    """The enclosure certificate (``docs/31`` §2); deliberate that ``G`` and ``V`` may cross."""
    lower, upper, rep, gap = b["lower"], b["upper"], b["representative"], b["gap"]
    return {
        "lower_le_rep_le_upper": lower <= rep <= upper,
        "lower_le_volume_le_upper": lower <= volume <= upper,
        "signed_certificate": rep - upper <= rep - volume <= rep - lower,
        "abs_error_within_gap": abs(rep - volume) <= gap,
    }


# --- 2. refinement ----------------------------------------------------------

def refine(coarse, fine):
    """Refinement gains/drops. All three are provably nonnegative (``docs/31`` §3)."""
    return {
        "lower_gain": fine["lower"] - coarse["lower"],
        "upper_drop": coarse["upper"] - fine["upper"],
        "gap_drop": coarse["gap"] - fine["gap"],
    }


def quadrature_error(b, volume):
    """The signed representative quadrature error ``G - V``."""
    return b["representative"] - volume


# --- 3. the three-way error decomposition ------------------------------------

def error_decomposition(mean, supplied, geometric, volume):
    """``mean - V = (mean - T) + (T - G) + (G - V)`` (``docs/31`` §4).

    ``T`` = supplied marks, ``G`` = geometric target, ``V`` = true volume. The
    three signed terms are sampling bias, annotation error and quadrature error.
    """
    sampling = mean - supplied
    annotation = supplied - geometric
    quadrature = geometric - volume
    return {
        "sampling": sampling,
        "annotation": annotation,
        "quadrature": quadrature,
        "total": mean - volume,
        "identity": sampling + annotation + quadrature == mean - volume,
    }


# --- 4. kernel discrepancy ---------------------------------------------------

def kernel_discrepancy(geometric_target, clipped_order_sum, cross_cell_integral,
                       within_cell_integral, continuum_pair):
    """``P_g - J = (P_g - K) + (K - Jcross) - Jdiag`` (``docs/31`` §5).

    ``P_g`` geometric pair sum, ``K`` clipped-order sum, ``Jcross`` cross-cell
    integral, ``Jdiag`` within-cell integral, ``J = Jcross + Jdiag``.
    """
    boundary = geometric_target - clipped_order_sum
    cross_order = clipped_order_sum - cross_cell_integral
    omission = -within_cell_integral
    total = geometric_target - continuum_pair
    return {
        "boundary": boundary,
        "cross_order": cross_order,
        "omission": omission,
        "total": total,
        "identity": boundary + cross_order + omission == total,
        "split_ok": cross_cell_integral + within_cell_integral == continuum_pair,
    }


# --- the demonstration -------------------------------------------------------

def _cell(i, j):
    return {"u": (Fraction(i, 3), Fraction(i + 1, 3)),
            "v": (Fraction(j, 2), Fraction(j + 1, 2))}


def _area(cell):
    return (cell["u"][1] - cell["u"][0]) * (cell["v"][1] - cell["v"][0]) / 2


def _mid(cell):
    return ((cell["u"][0] + cell["u"][1]) / 2, (cell["v"][0] + cell["v"][1]) / 2)


def membership(cell, probe):
    """Which enclosure class the cell is in, relative to ``probe`` (``docs/31`` §2)."""
    (ul, uh), (vl, vh) = cell["u"], cell["v"]
    (pl, ph), (ql, qh) = probe["u"], probe["v"]
    inter_u = max(Fraction(0), min(uh, ph) - max(ul, pl))
    inter_v = max(Fraction(0), min(vh, qh) - max(vl, ql))
    ru, rv = _mid(cell)
    return {
        "inner": ul >= pl and uh <= ph and vl >= ql and vh <= qh,
        "outer": inter_u * inter_v > 0,
        "representative": pl < ru < ph and ql < rv < qh,
    }


def _probe_view(cells, areas, probe):
    mem = [membership(c, probe) for c in cells]
    b = bounds(areas, [m["inner"] for m in mem], [m["outer"] for m in mem],
               [m["representative"] for m in mem])
    volume = (probe["u"][1] - probe["u"][0]) * (probe["v"][1] - probe["v"][0]) / 2
    return {"bounds": b, "volume": volume, "checks": certify(b, volume)}


def enclosure_report():
    """Assemble the enclosure results on a 3x2 grid of ``[0,1]^2`` (``docs/31`` §6).

    Split cell ``(0,1)`` at ``v = 3/4``: the aligned probe is exact, the
    unaligned probe brackets with a *signed* error, and the refinement shows the
    gap shrink while the absolute representative error grows.
    """
    cells = [_cell(i, j) for i in range(3) for j in range(2)]
    areas = [_area(c) for c in cells]
    aligned = {"u": (Fraction(0), Fraction(2, 3)), "v": (Fraction(0), Fraction(1, 2))}
    unaligned = {"u": (Fraction(0), Fraction(4, 5)), "v": (Fraction(0), Fraction(4, 5))}

    coarse = {"aligned": _probe_view(cells, areas, aligned),
              "unaligned": _probe_view(cells, areas, unaligned)}

    split = _cell(0, 1)
    children = [
        {"u": split["u"], "v": (Fraction(1, 2), Fraction(3, 4))},
        {"u": split["u"], "v": (Fraction(3, 4), Fraction(1))},
    ]
    fine_cells = [cells[0], children[0], children[1]] + cells[2:]
    fine_areas = [_area(c) for c in fine_cells]
    fine = {"unaligned": _probe_view(fine_cells, fine_areas, unaligned)}

    coarse_b = coarse["unaligned"]["bounds"]
    fine_b = fine["unaligned"]["bounds"]
    volume = coarse["unaligned"]["volume"]
    marks = coarse_b["representative"]  # T: supplied marks equal the geometric target
    return {
        "cell_area": areas[0],
        "aligned": coarse["aligned"],
        "unaligned_coarse": coarse["unaligned"],
        "unaligned_fine": fine["unaligned"],
        "refinement": refine(coarse_b, fine_b),
        "quadrature_coarse": quadrature_error(coarse_b, volume),
        "quadrature_fine": quadrature_error(fine_b, volume),
        "abs_error_grew": abs(quadrature_error(fine_b, volume)) > abs(quadrature_error(coarse_b, volume)),
        "decomposition": error_decomposition(marks + Fraction(1, 10), marks,
                                             coarse_b["representative"], volume),
        "kernel": kernel_discrepancy(
            geometric_target=Fraction(1, 4),
            clipped_order_sum=Fraction(1, 5),
            cross_cell_integral=Fraction(3, 20),
            within_cell_integral=Fraction(1, 10),
            continuum_pair=Fraction(1, 4),
        ),
    }
