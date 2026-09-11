"""A hierarchical (nested) router: build the tree and confirm B4's prediction (``docs/29``).

`docs/25` predicted that nesting *adds* routing cost. This module builds a real
balanced tree over 1-D regime positions, routes inputs through it, and measures
flat vs nested routing bits on the actual split margins -- a confirmation on a
concrete profile rather than an assumed one.
"""

from fractions import Fraction

from . import nested as nd


def build_tree(positions):
    """Balanced binary tree over sorted 1-D regime positions; internal nodes carry the split margin."""
    pos = sorted(Fraction(p) for p in positions)
    def build(lo, hi):
        if hi - lo == 1:
            return {"leaf": pos[lo]}
        mid = (lo + hi) // 2
        return {
            "margin": pos[mid] - pos[mid - 1],
            "boundary": (pos[mid - 1] + pos[mid]) / 2,
            "left": build(lo, mid),
            "right": build(mid, hi),
        }
    return build(0, len(pos))


def internal_margins(tree):
    """Every internal (routing) margin, in the tree."""
    if "leaf" in tree:
        return []
    return ([tree["margin"]]
            + internal_margins(tree["left"]) + internal_margins(tree["right"]))


def leaves(tree):
    if "leaf" in tree:
        return [tree["leaf"]]
    return leaves(tree["left"]) + leaves(tree["right"])


def route(tree, x):
    """Route ``x`` to a leaf by walking the tree (``log R`` comparisons)."""
    node = tree
    while "leaf" not in node:
        node = node["left"] if Fraction(x) < node["boundary"] else node["right"]
    return node["leaf"]


def flat_margin(positions):
    """A single n-way router must resolve the closest adjacent pair."""
    pos = sorted(Fraction(p) for p in positions)
    return min(pos[i + 1] - pos[i] for i in range(len(pos) - 1))


def benchmark_hierarchy(positions=None, L=1):
    """Build a tree and compare flat vs nested routing bits on the real margins."""
    if positions is None:
        positions = [Fraction(0), Fraction(1, 2), Fraction(11, 20), Fraction(2)]
    tree = build_tree(positions)
    margins = internal_margins(tree)
    flat = nd.precision_bits(flat_margin(positions), L)
    nested = sum(nd.precision_bits(m, L) for m in margins)
    return {
        "positions": positions,
        "internal_margins": margins,
        "flat_router_bits": flat,
        "nested_router_bits": nested,
        "nesting_costs_more": nested >= flat,
        "routes": {str(x): str(route(tree, x)) for x in positions},
    }
