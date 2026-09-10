"""The two-kinds-of-ambiguity example (geometry vs. sampling density).

Two hypotheses over a supplied geometry can share the *single-mark* law
(channel-limited ambiguity) or the *complete* point law (factorization
obstruction). This module makes both exact.
"""

from fractions import Fraction

from . import linalg as la


def mass(eta, delta, z, scale=1):
    """Integrated mass ``M_z(delta) = (s/2)[z + (eta+delta)z^2/4 + eta*delta*z^3/9]``."""
    eta = la.frac(eta)
    delta = la.frac(delta)
    z = la.frac(z)
    s = la.frac(scale)
    return (s / 2) * (z + (eta + delta) * z ** 2 / 4 + eta * delta * z ** 3 / 9)


def q_mark(eta, delta, scale=1):
    """Normalized mark probabilities ``(q1, q2)`` for rectangles of area 1/4 and 3/8."""
    M_Q = mass(eta, delta, 1, scale)
    q1 = mass(eta, delta, Fraction(1, 4), scale) / M_Q
    q2 = mass(eta, delta, Fraction(3, 8), scale) / M_Q
    return q1, q2


def target(eta):
    """Geometric target ``tau = (16 + eta) / (16 (4 + eta))``."""
    eta = la.frac(eta)
    return (16 + eta) / (16 * (4 + eta))


def point_poly(eta, delta):
    """Coefficients of the full point-law polynomial ``1 + (eta+delta)uv + eta*delta u^2v^2``."""
    eta = la.frac(eta)
    delta = la.frac(delta)
    return {"const": Fraction(1), "uv": eta + delta, "u2v2": eta * delta}


def delta_for_q(eta, q):
    """Invert ``q(eta, delta) = (a + b delta)/(c + d delta)`` for ``delta``."""
    eta = la.frac(eta)
    q = la.frac(q)
    a = 144 + 9 * eta
    b = 9 + eta
    c = 576 + 144 * eta
    d = 144 + 64 * eta
    den = d * q - b
    if den == 0:
        raise ZeroDivisionError("inverse pole: no unique delta")
    return (a - c * q) / den


def type1_obstruction():
    """Kind 1 (factorization obstruction): identical *complete* point law,
    different targets. Not fixable by any common observation channel."""
    flat = (0, 1)
    conf = (1, 0)
    q1_flat, q2_flat = q_mark(*flat)
    q1_conf, q2_conf = q_mark(*conf)
    return {
        "flat_point_poly": point_poly(*flat),
        "conf_point_poly": point_poly(*conf),
        "same_point_law": point_poly(*flat) == point_poly(*conf),
        "q1": q1_flat,
        "q2": q2_flat,
        "same_q1": q1_flat == q1_conf,
        "same_q2": q2_flat == q2_conf,
        "targets": (target(0), target(1)),
        "target_gap": abs(target(1) - target(0)),
    }


def type2_obstruction():
    """Kind 2 (channel-limited): same single-mark law, different point law.
    A richer channel (the second mark q2) splits it."""
    d_flat = delta_for_q(0, Fraction(1, 5))
    d_conf = delta_for_q(1, Fraction(1, 5))
    q1_flat, q2_flat = q_mark(0, d_flat)
    q1_conf, q2_conf = q_mark(1, d_conf)
    return {
        "delta_flat": d_flat,
        "delta_conf": d_conf,
        "q1_equal": q1_flat == q1_conf,
        "q1": q1_flat,
        "poly_flat": point_poly(0, d_flat),
        "poly_conf": point_poly(1, d_conf),
        "point_law_differs": point_poly(0, d_flat) != point_poly(1, d_conf),
        "q2_flat": q2_flat,
        "q2_conf": q2_conf,
        "q2_gap": abs(q2_flat - q2_conf),
        "q2_splits": q2_flat != q2_conf,
    }
