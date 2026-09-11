"""B3: longer training via certified truncation — bits vs steps (``docs/25``, ``docs/19``).

Exact training grows denominators ~x3 per step (``docs/18``). Truncating to a
grid each step keeps the precision bounded (``docs/19``). This measures the loss
and the denominator bits over a session, next to the ``log``-in-steps projection.
"""

from fractions import Fraction

from . import transformer as tr
from . import truncate as tc
from . import nested as nd


def truncated_training(steps, grid=64, eta=Fraction(1, 50)):
    """Gradient descent with certified truncation each step; returns ``[(step, loss, bits)]``."""
    ws = [Fraction(2 * k + 1, 40) for k in range(22)]
    rows = [(0, tr.loss(ws, tr.TOY_DATA), tc.denominator_bits(ws))]
    for s in range(1, steps + 1):
        ws = tc.truncate(tr.exact_step(ws, tr.TOY_DATA, eta), grid)
        rows.append((s, tr.loss(ws, tr.TOY_DATA), tc.denominator_bits(ws)))
    return rows


def benchmark_long_session(steps=8, grid=64):
    """B3 report: truncated session plus the ``log``-in-steps projection."""
    rows = truncated_training(steps, grid)
    return {
        "grid": grid,
        "rows": rows,
        "max_bits": max(b for _, _, b in rows),
        "projected_bits": nd.bits_vs_steps(steps),
        "loss_first": rows[0][1],
        "loss_last": rows[-1][1],
    }
