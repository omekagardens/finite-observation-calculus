"""Exact, machine-checkable certificates for the ambiguity classification.

``docs/14``. Each verdict carries a certificate a verifier can re-check *without
re-running the analysis*:

- **separated** — a witness effect in the accessible span with ``Tr(delta E) != 0``;
- **channel-limited** — ``delta`` invisible to the accessible span, plus a witness
  in the completed span;
- **law-surviving** — ``delta`` invisible to the completed span.

Certificates are JSON-serializable (rationals as strings), matching the upstream
QR-01 wire style.
"""

from fractions import Fraction

from . import linalg as la
from . import ambiguity as amb


def _find_witness(delta, family):
    for E in family:
        if la.trace(la.mat_mul(delta, E)) != 0:
            return E
    return None


def build_certificate(delta, accessible, completed):
    """Classify ``delta`` and attach a witness; return the exact certificate."""
    label = amb.classify(delta, accessible, completed)
    witness = None
    if label == "separated":
        witness = _find_witness(delta, accessible)
    elif label == "channel-limited":
        witness = _find_witness(delta, completed)
    return {
        "label": label,
        "delta": delta,
        "accessible": list(accessible),
        "completed": list(completed),
        "witness": witness,
    }


def _is_witness(w, delta, family):
    return (
        w is not None
        and any(w == E for E in family)
        and la.trace(la.mat_mul(delta, w)) != 0
    )


def verify_certificate(cert):
    """Re-check a certificate exactly; returns ``True`` iff it is valid."""
    delta = cert["delta"]
    accessible = cert["accessible"]
    completed = cert["completed"]
    witness = cert.get("witness")
    in_a = amb.in_annihilator(delta, accessible)
    in_c = amb.in_annihilator(delta, completed)
    if in_c and not in_a:  # nesting: A_E must contain A_{E*}
        return False
    label = cert["label"]
    if label == "separated":
        return (not in_a) and _is_witness(witness, delta, accessible)
    if label == "channel-limited":
        return in_a and (not in_c) and _is_witness(witness, delta, completed)
    if label == "law-surviving":
        return in_c and witness is None
    return False


def to_wire(cert):
    """JSON-serializable wire form (rationals as strings)."""
    def m(mat):
        return [[str(x) for x in row] for row in mat]

    return {
        "label": cert["label"],
        "delta": m(cert["delta"]),
        "accessible": [m(E) for E in cert["accessible"]],
        "completed": [m(E) for E in cert["completed"]],
        "witness": m(cert["witness"]) if cert["witness"] is not None else None,
    }


def from_wire(wire):
    """Parse a wire-form certificate back to exact matrices."""
    def m(mat):
        return [[Fraction(x) for x in row] for row in mat]

    return {
        "label": wire["label"],
        "delta": m(wire["delta"]),
        "accessible": [m(E) for E in wire["accessible"]],
        "completed": [m(E) for E in wire["completed"]],
        "witness": m(wire["witness"]) if wire["witness"] is not None else None,
    }


def verify_wire(wire):
    """Verify a wire-form certificate."""
    return verify_certificate(from_wire(wire))
