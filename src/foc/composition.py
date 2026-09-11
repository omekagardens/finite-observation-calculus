"""Summaries are not compositional (``docs/32``).

``docs/04`` says the coarsest adequate summary is question-relative; ``docs/05``
says forgetting is not recombination. This module gives the sharpest version of
that obstruction for **causal / order** summaries: an exactly additive *pair*
summary does **not** close under composition to a *chain* summary.

With the flat metric ``ds^2 = du dv`` (measure ``dmu = du dv / 2``) and the strict
product order ``x < y`` iff ``u_x < u_y`` and ``v_x < v_y``:

- the pair measure ``J_AB`` and the triple measure ``T_ABC`` are exact integrals;
- the pair-product surrogate ``P_ABC = J_AB J_BC / h_B`` is what a pair-only
  summary would predict for the chain;
- the exact error is a covariance,
  ``T - P = h_B * Cov_B(L_A, R_C)``, so pair additivity does **not** imply
  higher-chain composition closure (``docs/32`` §3);
- the pair conditionals are not transition probabilities: ``C_AA = J_AA/h_A^2``
  has row sum ``1/4``, not ``1``;
- coarse-graining pair measures uses the *geometric* weights
  ``h_a h_b / (h_A h_B)``, and only those reproduce ``C_AB`` (``docs/32`` §4).
"""

from fractions import Fraction


# --- exact 1-D causal integrals ---------------------------------------------

def _clamp(x, lo, hi):
    if x < lo:
        return lo
    if x > hi:
        return hi
    return x


def _predecessor(y, a, b):
    """``|A ∩ (-inf, y]|`` for ``A = [a, b]``."""
    return _clamp(y - a, Fraction(0), b - a)


def _successor(y, e, f):
    """``|C ∩ (y, inf)|`` for ``C = [e, f]``."""
    return _clamp(f - y, Fraction(0), f - e)


def _breakpoints(lo, hi, *points):
    pts = {lo, hi}
    for p in points:
        if lo < p < hi:
            pts.add(p)
    return sorted(pts)


def pair_int_1d(a, b, c, d):
    """``int_{x in A} int_{y in B} 1(x < y)`` for ``A = [a,b]``, ``B = [c,d]``."""
    a, b, c, d = (Fraction(x) for x in (a, b, c, d))
    if b <= a or d <= c:
        return Fraction(0)
    total = Fraction(0)
    pts = _breakpoints(c, d, a, b)
    for lo, hi in zip(pts, pts[1:]):
        total += (hi - lo) * (_predecessor(lo, a, b) + _predecessor(hi, a, b)) / 2
    return total


def triple_int_1d(a, b, c, d, e, f):
    """``int_A int_B int_C 1(x < y < z)`` for ``A=[a,b]``, ``B=[c,d]``, ``C=[e,f]``."""
    a, b, c, d, e, f = (Fraction(x) for x in (a, b, c, d, e, f))
    if b <= a or d <= c or f <= e:
        return Fraction(0)
    total = Fraction(0)
    pts = _breakpoints(c, d, a, b, e, f)
    for lo, hi in zip(pts, pts[1:]):
        gl, gh = _successor(lo, e, f), _successor(hi, e, f)
        hl, hh = _predecessor(lo, a, b), _predecessor(hi, a, b)
        dg, dh = gh - gl, hh - hl
        # integral over s in [0,1] of (g_l + dg s)(h_l + dh s) ds
        val = gl * hl + (gl * dh + hl * dg) / 2 + dg * dh / 3
        total += (hi - lo) * val
    return total


# --- 2-D clip measures under du dv / 2 ---------------------------------------

def clip_volume(ul, uh, vl, vh):
    """Area of the rectangle ``[ul,uh] x [vl,vh]`` under ``dmu = du dv / 2``."""
    return (Fraction(uh) - Fraction(ul)) * (Fraction(vh) - Fraction(vl)) / 2


def pair_measure(clip_x, clip_y):
    """The 2-D causal pair measure ``J_XY``; factorizes as ``I_u I_v / 4``."""
    ux = pair_int_1d(clip_x[0], clip_x[1], clip_y[0], clip_y[1])
    vx = pair_int_1d(clip_x[2], clip_x[3], clip_y[2], clip_y[3])
    return ux * vx / 4


def triple_measure(clip_x, clip_y, clip_z):
    """The 2-D causal triple measure ``T_XYZ``; factorizes as ``K_u K_v / 8``."""
    ux = triple_int_1d(clip_x[0], clip_x[1], clip_y[0], clip_y[1], clip_z[0], clip_z[1])
    vx = triple_int_1d(clip_x[2], clip_x[3], clip_y[2], clip_y[3], clip_z[2], clip_z[3])
    return ux * vx / 8


# --- the pair-product surrogate and its error --------------------------------

def pair_product(J_ab, J_bc, h_b):
    """``P_ABC = J_AB J_BC / h_B`` — what a pair-only summary predicts for a chain."""
    if h_b == 0:
        return None
    return J_ab * J_bc / h_b


def middle_covariance(T, P, h_b):
    """``(T - P)/h_B`` — the exact dependence the pair product drops."""
    if h_b == 0:
        return None
    return (T - P) / h_b


def conditional(J, h_a, h_b):
    """``C_AB = J_AB / (h_A h_B)`` (``None`` when the volume product vanishes)."""
    if h_a * h_b == 0:
        return None
    return J / (h_a * h_b)


def covariance_identity_1d(a, b, c, d, e, f):
    """Verify ``T - P = h_B * Cov_B(L_A, R_C)`` for 1-D clips (``docs/32`` §3)."""
    a, b, c, d, e, f = (Fraction(x) for x in (a, b, c, d, e, f))
    h_b = d - c
    if h_b == 0:
        return None
    T = triple_int_1d(a, b, c, d, e, f)
    J_ab = pair_int_1d(a, b, c, d)
    J_bc = pair_int_1d(c, d, e, f)
    P = J_ab * J_bc / h_b
    covariance = T / h_b - (J_ab / h_b) * (J_bc / h_b)
    return {"T": T, "J_ab": J_ab, "J_bc": J_bc, "P": P, "h_b": h_b,
            "covariance": covariance, "identity": T - P == h_b * covariance}


# --- geometric coarsening of pair measures -----------------------------------

def coarsening_weights(h_a_children, h_b_children, h_a, h_b):
    """The child block weights ``h_a h_b / (h_A h_B)`` (``docs/32`` §4)."""
    if h_a * h_b == 0:
        return None
    return [[ha * hb / (h_a * h_b) for hb in h_b_children] for ha in h_a_children]


def aggregate_conditional(weights, child_conditionals):
    """``C_AB = sum_ab w_ab C_ab`` — geometric-weight aggregation."""
    return sum(weights[i][j] * child_conditionals[i][j]
               for i in range(len(weights)) for j in range(len(weights[0])))


# --- the demonstration -------------------------------------------------------

def unit_rectangle_report():
    """The exact unit-clip numbers: ``T = 1/288`` versus ``P = 1/128`` (``docs/32`` §3)."""
    clip = (Fraction(0), Fraction(1), Fraction(0), Fraction(1))
    h = clip_volume(*clip)
    J = pair_measure(clip, clip)
    T = triple_measure(clip, clip, clip)
    P = pair_product(J, J, h)
    row_sum = conditional(J, h, h)
    return {
        "volume": h,
        "pair": J,
        "triple": T,
        "pair_product": P,
        "pair_fraction": row_sum,
        "triple_fraction": T / h ** 3,
        "row_sum_is_one": row_sum == 1,
        "squared_pair_fraction": row_sum ** 2,
        "product_error": P - T,
        "noncompositional": T != P,
        "squaring_mismatch": row_sum ** 2 != T / h ** 3,
        "middle_covariance": middle_covariance(T, P, h),
    }


def composition_report():
    """Assemble the non-compositionality results (``docs/32`` §5)."""
    weights = coarsening_weights([Fraction(1, 4), Fraction(1, 4)],
                                 [Fraction(1, 4), Fraction(1, 2)],
                                 Fraction(1, 2), Fraction(3, 4))
    child_conditionals = [[Fraction(1, 4), Fraction(3, 4)],
                          [Fraction(1, 2), Fraction(1, 4)]]
    weighted = aggregate_conditional(weights, child_conditionals)
    unweighted = sum(sum(row) for row in child_conditionals) / 4
    return {
        "unit": unit_rectangle_report(),
        "covariance": covariance_identity_1d(0, 1, Fraction(1, 4), Fraction(3, 4), 0, 1),
        "weights": weights,
        "weight_sum": sum(sum(row) for row in weights),
        "aggregation": {
            "weighted": weighted,
            "unweighted": unweighted,
            "differ": weighted != unweighted,
            "geometric_ok": weighted == Fraction(11, 24),
        },
    }
