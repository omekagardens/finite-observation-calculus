"""The corrective loop: localizing an external failure (``docs/23``).

Internal certificates are the fast, closed, conditional layer; the external
verdict is the scarce grounding layer. This module turns an external failure into
a **localized, bounded, refinement-safe** correction:

- ``localize`` — the nodes whose probes *can see* the failing feature (the
  annihilator filter): a node blind to the feature cannot be responsible
  (`docs/08` §4, `docs/22` §2);
- ``blame_edge`` — the edges whose gap the failing downstream *reads*
  (`docs/21` §5);
- ``accept_correction`` — re-certify: accept iff the correction refines
  (monotone, `docs/22` §5) and the external verdict holds.

Localization is only as good as the declared interfaces, and the external verdict
is still required — internal certificates are conditional (`docs/22` §7).
"""

from fractions import Fraction

from . import linalg as la
from . import ambiguity as amb
from . import forgetting as fg
from . import instruments as ins
from . import modelrun as mr
from . import router as rt
from . import internal as ic

_Z = la.mat([[1, 0], [0, -1]])


def localize(failing_feature, nodes):
    """Nodes whose probes can see the failing feature: not in their annihilator (``docs/23``)."""
    return [name for name, probes in nodes if not amb.in_annihilator(failing_feature, probes)]


def blame_edge(failing_downstream, edges, states):
    """Edges whose gap the failing downstream reads: hard is not a valid replacement there (``docs/21`` §5)."""
    return [name for name, experts in edges
            if not rt.replacement_holds(experts, failing_downstream, states)]


def accept_correction(before_probes, after_probes, verdict, basis):
    """Re-certify a correction: accept iff it refines (monotone) and the external verdict holds (``docs/23``)."""
    ann_before = ic.compose_annihilator_dim([before_probes], basis)
    ann_after = ic.compose_annihilator_dim([after_probes], basis)
    refined = ann_after <= ann_before
    return {
        "annihilator_before": ann_before,
        "annihilator_after": ann_after,
        "refinement_safe": refined,
        "verdict_holds": verdict,
        "accepted": refined and verdict,
    }


def corrective_report():
    """Assemble the corrective-loop results (``docs/23``)."""
    def op(a, b):
        return la.kron(a, b)

    pairs = [op(a, b) for a in (mr.X, mr.Y, mr.Z) for b in (mr.X, mr.Y, mr.Z)]
    nodes = [("local", mr.LOCAL), ("pairs", pairs)]
    edges = [("overlapping", [fg.D0, fg.D1]), ("orthogonal", [fg.P0, fg.P1])]
    states = [ins.rho_plus(), ins.rho_minus(), ins.rho_mixed()]
    basis = ic._two_qubit_traceless()
    return {
        "localize_2body": localize(op(mr.Z, mr.Z), nodes),
        "localize_1body": localize(op(mr.Z, mr.I2), nodes),
        "blame_Z": blame_edge([_Z], edges, states),
        "blame_I": blame_edge([mr.I2], edges, states),
        "correction": accept_correction(mr.LOCAL, mr.LOCAL + [op(mr.Z, mr.Z)], True, basis),
    }
