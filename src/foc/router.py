"""A certified router, and routing theorems against the calculus (``docs/21``).

`docs/20` certifies the *nodes* and shows the routing *type* matters; this note
supplies the missing object — the **router** — and the routing theorems.

The router is a **declared policy** (`docs/01` §2): it reads a declared record
(a score) and picks a regime. Two things are certified:

- **the routing** — an input is routed *unambiguously* iff its distance to the
  boundary exceeds the margin, so the router has its own bit budget (`docs/19`);
- **the routing *type*** — hard routing (sum of maps) versus soft routing
  (recombination) differ by the cross term ``sum_{x != y} M_x rho M_y^T``, which
  vanishes iff the input carries no coherence between the experts' ranges
  (`docs/05`).
"""

from fractions import Fraction

from . import linalg as la
from . import forgetting as fg
from . import instruments as ins
from . import truncate as tc


# --- the router: a declared policy on a declared record ----------------------

def score(w, x):
    """The router's declared record: the linear score ``w . x``."""
    return sum(w[i] * x[i] for i in range(len(w)))


def route(w, x):
    """Route to ``"A"`` if the score is positive, else ``"B"``."""
    return "A" if score(w, x) > 0 else "B"


def routing_margin(w, x):
    """Distance of input ``x`` from the routing boundary: ``|w . x|``."""
    return abs(score(w, x))


def certified_route(w, x, margin):
    """The certified regime, or ``None`` if the routing is ambiguous at ``margin``."""
    return route(w, x) if routing_margin(w, x) >= margin else None


def router_precision(w, inputs, margin, choices=(4, 8, 16, 32, 64, 128, 256)):
    """Coarsest grid whose *certified* routings match the exact router's (`docs/19`).

    The router is a small model; its weights truncate like any other, and the
    margin sets the coarsest grid that keeps every certified routing.
    """
    exact = [certified_route(w, x, margin) for x in inputs]
    for n in choices:
        wq = tc.truncate(w, n)
        if [certified_route(wq, x, margin) for x in inputs] == exact:
            return {"grid": n, "bits": tc.denominator_bits(wq)}
    return None


# --- routing theorems --------------------------------------------------------

def routing_type_gap(experts, rho):
    """Hard routing (sum of maps) versus soft routing (recombination) on ``rho`` (``docs/05``).

    The gap is the cross term ``sum_{x != y} M_x rho M_y^T``; it vanishes exactly
    when ``rho`` carries no coherence between the experts' ranges.
    """
    hard = fg.incoherent_sum(experts, rho)
    soft = fg.coherent_recombination(experts, rho)
    return {"hard": hard, "soft": soft, "differ": hard != soft}


def hard_routing(experts, rho):
    """Hard routing: sum of maps (the router's choice is a discarded record)."""
    return fg.incoherent_sum(experts, rho)


def soft_routing(experts, rho):
    """Soft routing: recombination (amplitudes summed before squaring)."""
    return fg.coherent_recombination(experts, rho)


def replacement_holds(experts, downstream, states):
    """Is hard routing a **valid replacement** for soft for the declared downstream? (``docs/05`` §3)

    ``downstream`` is a family of effects; the replacement holds iff every
    downstream effect is blind to the gap ``soft - hard`` on every state, i.e.
    ``Tr(E (soft - hard)(rho)) = 0`` for all ``E``, ``rho``.
    """
    for rho in states:
        gap = la.mat_sub(soft_routing(experts, rho), hard_routing(experts, rho))
        if any(la.trace(la.mat_mul(E, gap)) != 0 for E in downstream):
            return False
    return True


def collision_witness(experts, rho_a, rho_b):
    """A **colliding-inputs** certificate: two inputs hard routing collides that soft separates.

    By ``docs/05`` §4 this is an actual impossibility proof — no operation on the
    hard (coarse) output can reproduce both required outputs — not merely the
    failure of one candidate replacement.
    """
    hard_a, hard_b = hard_routing(experts, rho_a), hard_routing(experts, rho_b)
    soft_a, soft_b = soft_routing(experts, rho_a), soft_routing(experts, rho_b)
    return {
        "hard_collides": hard_a == hard_b,
        "soft_separates": soft_a != soft_b,
        "no_replacement": hard_a == hard_b and soft_a != soft_b,
    }


_Z = la.mat([[1, 0], [0, -1]])


def replacement_report():
    """The replacement criterion on the ``docs/05`` experts (``docs/21`` §4).

    A downstream that only *counts* (reads ``I``) is blind to the gap and admits
    the hard replacement; a downstream that reads ``Z`` is not — with the
    colliding-inputs witness ``(|+>, |->)``.
    """
    experts = [fg.D0, fg.D1]
    states = [ins.rho_plus(), ins.rho_minus(), ins.rho_mixed()]
    return {
        "counts_valid": replacement_holds(experts, [la.identity(2)], states),
        "reads_Z_valid": replacement_holds(experts, [_Z], states),
        "witness": collision_witness(experts, ins.rho_plus(), ins.rho_minus()),
    }


def router_report(margin=Fraction(1, 2)):
    """Assemble the certified-routing and routing-type results (``docs/21``)."""
    w = [Fraction(3, 5), Fraction(-4, 5)]
    inputs = [
        (Fraction(3), Fraction(1)),
        (Fraction(1), Fraction(3)),
        (Fraction(1, 2), Fraction(1, 2)),
    ]
    orthogonal = [fg.P0, fg.P1]
    classical = la.mat([[Fraction(3, 4), Fraction(0)], [Fraction(0), Fraction(1, 4)]])
    coherent = ins.rho_plus()
    return {
        "routes": [
            {"x": x, "route": route(w, x), "margin": routing_margin(w, x),
             "certified": certified_route(w, x, margin)}
            for x in inputs
        ],
        "router_precision": router_precision(w, inputs, margin),
        "type_orthogonal_classical": routing_type_gap(orthogonal, classical)["differ"],
        "type_orthogonal_coherent": routing_type_gap(orthogonal, coherent)["differ"],
        "type_overlapping_classical": routing_type_gap([fg.D0, fg.D1], classical)["differ"],
    }
