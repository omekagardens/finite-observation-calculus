"""Coarse-graining (summing probability maps) is not recombination (summing amplitudes).

``docs/05-forgetting.md``. Forgetting which of several fine outcomes occurred
merges their outcome maps by *addition*: ``C_z = sum_{x: f(x)=z} I_x`` — a sum
of probabilities, which destroys coherence between the merged branches. Summing
the *amplitudes* before squaring is a different transformation and must never be
conflated with it.

The coarse map is not invertible, yet feedback that still reads the fine record
can undo it. Exactly that gap is certified below: two inputs the coarse channel
sends to the same state whose fine feedback sends to different states, so no
coarse-only replacement instrument ``G`` can satisfy ``sum_x F_x o I_x = G o C``.
"""

from fractions import Fraction

from . import linalg as la
from . import instruments as ins

# The Z-basis (projective) instrument: the sum of branches is dephasing, the sum
# of amplitudes is the identity.
P0 = ins.P0
P1 = ins.P1

# A *non-projective* two-outcome qubit instrument with rational Kraus operators:
# D0^T D0 + D1^T D1 = I, but neither D0^T D0 nor D1^T D1 is a projector.
D0 = la.mat([[Fraction(4, 5), 0], [0, Fraction(3, 5)]])
D1 = la.mat([[Fraction(3, 5), 0], [0, Fraction(-4, 5)]])


def coherent_recombination(kraus, rho):
    """Sum amplitudes *before* the square: ``(sum_g C_g) rho (sum_g C_g)^T``."""
    acc = kraus[0]
    for c in kraus[1:]:
        acc = la.mat_add(acc, c)
    return la.mat_mul(la.mat_mul(acc, rho), la.transpose(acc))


def incoherent_sum(kraus, rho):
    """Sum branches *after* the square: ``sum_g C_g rho C_g^T`` (classical forgetting)."""
    acc = la.zero(len(rho))
    for c in kraus:
        acc = la.mat_add(acc, la.mat_mul(la.mat_mul(c, rho), la.transpose(c)))
    return acc


def is_instrument(kraus, dim):
    """True iff ``sum_g C_g^T C_g = I`` (a trace-preserving instrument)."""
    acc = la.zero(dim)
    for c in kraus:
        acc = la.mat_add(acc, la.mat_mul(la.transpose(c), c))
    return acc == la.identity(dim)


def z_example():
    """Minimal contrast on the Z instrument and a coherent state ``|+>``.

    Summing branches is dephasing (``|+><+| -> I/2``); summing amplitudes is the
    identity (``(P0 + P1) rho (P0 + P1) = rho``). They disagree on any coherent rho.
    """
    rho = ins.rho_plus()
    forgotten = incoherent_sum([P0, P1], rho)
    recombined = coherent_recombination([P0, P1], rho)
    mixed = [[Fraction(1, 2), Fraction(0)], [Fraction(0), Fraction(1, 2)]]
    return {
        "rho": rho,
        "forgotten": forgotten,
        "recombined": recombined,
        "differ": forgotten != recombined,
        "forgotten_is_dephased": forgotten == mixed,
        "recombined_is_identity": recombined == rho,
    }


def impossibility_witness():
    """The ``docs/05-forgetting.md`` §4 witness: two inputs the coarse channel
    merges but the fine feedback separates.

    Merging ``D0`` and ``D1`` into one coarse class gives
    ``C = D0 (.) D0^T + D1 (.) D1^T``, which here is Z-dephasing. The inputs
    ``|+><+|`` and ``|-><-|`` both map to ``I/2`` under ``C``. Feedback that flips
    the sign of the second fine branch -- ``F0 = id``, ``F1 = conjugation by Z`` --
    sends them to different states, so no ``G`` with ``G o C = sum_x F_x o I_x``
    exists: a coarse-only replacement is impossible.
    """
    rho_plus = ins.rho_plus()
    rho_minus = ins.rho_minus()
    Z = la.mat([[1, 0], [0, -1]])
    feedback = [la.identity(2), Z]

    def coarse(rho):
        return incoherent_sum([D0, D1], rho)

    def fine_feedback(rho):
        acc = la.zero(2)
        for M, U in zip([D0, D1], feedback):
            branch = la.mat_mul(la.mat_mul(M, rho), la.transpose(M))
            acc = la.mat_add(acc, la.mat_mul(la.mat_mul(U, branch), la.transpose(U)))
        return acc

    c_plus, c_minus = coarse(rho_plus), coarse(rho_minus)
    f_plus, f_minus = fine_feedback(rho_plus), fine_feedback(rho_minus)
    return {
        "rho_plus": rho_plus,
        "rho_minus": rho_minus,
        "coarse_state": c_plus,
        "coarse_plus": c_plus,
        "coarse_minus": c_minus,
        "coarse_merges": c_plus == c_minus,
        "fine_plus": f_plus,
        "fine_minus": f_minus,
        "fine_separates": f_plus != f_minus,
        "no_replacement": c_plus == c_minus and f_plus != f_minus,
    }
