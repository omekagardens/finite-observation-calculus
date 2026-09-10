"""Observation maps, states, and channels (all real, all exact).

A projective instrument is a dict mapping an outcome label to a projector
(its single Kraus operator). The outcome map is ``rho -> M rho M^T``.
"""

from fractions import Fraction

from . import linalg as la

# --- standard qubit objects (real, Z basis) --------------------------------

P0 = la.mat([[1, 0], [0, 0]])              # |0><0|
P1 = la.mat([[0, 0], [0, 1]])              # |1><1|

_h = Fraction(1, 2)
QP = [[_h, _h], [_h, _h]]                  # (I + X)/2 : |+><+|
QM = [[_h, -_h], [-_h, _h]]                # (I - X)/2 : |-><-|


def rho_0():
    return la.mat(P0)


def rho_1():
    return la.mat(P1)


def rho_plus():
    return la.mat(QP)


def rho_minus():
    return la.mat(QM)


def rho_mixed():
    """Maximally mixed state I/2."""
    return [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]]


def projective(projectors):
    """Build an instrument from a dict {outcome: projector}."""
    return {outcome: la.mat(P) for outcome, P in projectors.items()}


def z_instrument():
    return projective({"0": P0, "1": P1})


def x_instrument():
    return projective({"+": QP, "-": QM})


def apply_outcome(instrument, outcome, rho):
    """Unnormalized post-measurement state M rho M^T for the given outcome."""
    M = instrument[outcome]
    return la.mat_mul(la.mat_mul(M, rho), la.transpose(M))


def outcome_probability(instrument, outcome, rho) -> Fraction:
    return la.trace(apply_outcome(instrument, outcome, rho))


def channel(instrument, rho):
    """Discard the record: sum the outcome maps (a trace-preserving channel)."""
    acc = la.zero(len(rho))
    for outcome in instrument:
        acc = la.mat_add(acc, apply_outcome(instrument, outcome, rho))
    return acc


def normalize(m):
    t = la.trace(m)
    if t == 0:
        raise ValueError("cannot normalize a zero-trace state")
    return la.scale(Fraction(1, 1) / t, m)
