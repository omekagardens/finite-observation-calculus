"""B4/B5 + projections: flat vs nested regimes, routing ambiguity, distribution (``docs/25``).

Exact integer bit accounting built on ``docs/19``'s precision rule. The honest
finding the benchmark produces: **modularity beats a monolith when margins are
heterogeneous, but *nesting* does not reduce bits — it adds routing cost.** The
payoff of nested regimes is distribution and incremental growth, not precision.
"""

from fractions import Fraction


def ceil_log2(x):
    """Smallest integer ``b`` with ``2**b >= x`` (exact; ``x > 0``)."""
    x = Fraction(x)
    if x <= 0:
        raise ValueError("ceil_log2 needs a positive value")
    b = 0
    while Fraction(2) ** b < x:
        b += 1
    return b


def precision_bits(margin, L=1):
    """Weight precision for a decision margin: ``max(0, ceil(log2(2L/margin)))``."""
    return max(0, ceil_log2(Fraction(2 * L, 1) / margin))


def bits_vs_steps(steps, L=1, D=1):
    """Projection (``docs/19``): ``bits = ceil(log2(2L/D)) + ceil(log2 steps)``."""
    return precision_bits(D, L) + max(0, ceil_log2(Fraction(steps)))


def routing_bits_flat(split_margins, L=1):
    """One n-way router must resolve the hardest split: ``ceil(log2(2L/min margin))``."""
    return precision_bits(min(split_margins), L)


def routing_bits_nested(split_margins, L=1):
    """A tree of binary routers: one precision term per split (sum >= flat)."""
    return sum(precision_bits(m, L) for m in split_margins)


def leaf_bits(task_margins, params_per_leaf, L=1):
    """Total leaf precision: each leaf pays only its own margin."""
    return sum(p * precision_bits(m, L) for p, m in zip(params_per_leaf, task_margins))


def monolithic_bits(n_params, finest_margin, L=1):
    """One model, every parameter at the finest precision."""
    return n_params * precision_bits(finest_margin, L)


def routing_ambiguity(margins, t):
    """Fraction of inputs whose routing margin is below ``t`` (ambiguous, ``docs/21`` §2)."""
    return Fraction(sum(1 for m in margins if m < t), len(margins))


def parallel_speedup(node_work):
    """Ideal wall-clock speedup when independent nodes run in parallel: ``sum / max``."""
    return Fraction(sum(node_work), max(node_work))


def benchmark_regimes():
    """B4/B5 over a hierarchical margin profile (three easy splits, one hard)."""
    splits = [Fraction(1, 2), Fraction(1, 2), Fraction(1, 2), Fraction(1, 10)]
    params = [6, 6, 6, 6]
    return {
        "flat_router_bits": routing_bits_flat(splits),
        "nested_router_bits": routing_bits_nested(splits),
        "monolithic_bits": monolithic_bits(sum(params), min(splits)),
        "modular_bits": leaf_bits(splits, params),
        "ambiguity_at_1_4": routing_ambiguity(splits, Fraction(1, 4)),
        "parallel_speedup": parallel_speedup(params),
        "bits_at_1024_steps": bits_vs_steps(1024),
    }
