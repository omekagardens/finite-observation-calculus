"""Internal certification: self-consistency and closed composition (``docs/22``).

A model that reinforces on its own outputs is not *externally* grounded, but it is
**internally** certifiable: over declared interfaces the certification is closed
and local (`docs/20` composition, `docs/21` §5 replacement). Self-reinforcement is
stable iff the model is a **fixed point of its own replacement criterion**;
otherwise a **colliding-inputs witness** is the local instability certificate.

Internal certificates are *conditional* — they certify structure, not truth.
"""

from fractions import Fraction

from . import linalg as la
from . import forgetting as fg
from . import instruments as ins
from . import ambiguity as amb
from . import router as rt
from . import modelrun as mr

_Z = la.mat([[1, 0], [0, -1]])


def self_consistent(experts, downstream, states):
    """Is the model a fixed point of its own replacement criterion? (``docs/22``)

    True iff hard routing is a valid replacement for soft for the model's own
    downstream and its own outputs — so reinforcing on its hard decisions does
    not move it.
    """
    return rt.replacement_holds(experts, downstream, states)


def instability_witness(experts, rho_a, rho_b):
    """The colliding inputs where self-reinforcement forgets coherence (``docs/22``)."""
    return rt.collision_witness(experts, rho_a, rho_b)


def compose_annihilator_dim(probe_sets, basis):
    """The composed invisible sector = annihilator of the **union** of probe sets (``docs/20`` §5).

    Adding nodes grows the union, so it can only *shrink* the annihilator: internal
    growth is monotone — more regimes can only reduce law-surviving ambiguity.
    """
    union = [E for probes in probe_sets for E in probes]
    return amb.annihilator_dim(union, basis)


def _two_qubit_traceless():
    def op(a, b):
        return la.kron(a, b)
    full = [op(a, b) for a in (mr.I2, mr.X, mr.Y, mr.Z) for b in (mr.I2, mr.X, mr.Y, mr.Z)]
    return [M for M in full if la.trace(M) == 0]


def _pairs():
    return [la.kron(a, b) for a in (mr.X, mr.Y, mr.Z) for b in (mr.X, mr.Y, mr.Z)]


def internal_report():
    """Assemble the internal-certification results (``docs/22``)."""
    classical = la.mat([[Fraction(3, 4), Fraction(0)], [Fraction(0), Fraction(1, 4)]])
    coherent = [ins.rho_plus(), ins.rho_minus(), ins.rho_mixed()]
    basis = _two_qubit_traceless()
    return {
        "stable": self_consistent([fg.P0, fg.P1], [_Z], [classical]),
        "unstable": self_consistent([fg.D0, fg.D1], [_Z], coherent),
        "witness": instability_witness([fg.D0, fg.D1], ins.rho_plus(), ins.rho_minus()),
        "annihilator_local_node": compose_annihilator_dim([mr.LOCAL], basis),
        "annihilator_pairs_node": compose_annihilator_dim([_pairs()], basis),
        "annihilator_composed": compose_annihilator_dim([mr.LOCAL, _pairs()], basis),
    }
