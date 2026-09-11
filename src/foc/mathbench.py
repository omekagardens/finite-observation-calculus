"""Benchmarks B1/B2: a math-task ladder on exact-checkable tasks (``docs/25``).

Each task has a known exact target, so "learned" means ``loss == 0`` exactly. The
ladder instantiates the dichotomy: a task a linear lift fits is *separated*, one
that needs a quadratic lift is *channel-limited*, and one outside the declared
feature family is *law-surviving*.
"""

from fractions import Fraction

from . import train

GRID = [(Fraction(a), Fraction(b)) for a in range(-2, 3) for b in range(-2, 3)]


def _linear(x):
    return [Fraction(1), x[0], x[1]]


def _quadratic(x):
    return [Fraction(1), x[0], x[1], x[0] * x[0], x[0] * x[1], x[1] * x[1]]


LIFTS = {"linear": _linear, "quadratic": _quadratic}


def _add(a, b):
    return a + b


def _mul(a, b):
    return a * b


def _square(a, b):
    return (a + b) * (a + b)


def _modp(a, b):
    return (a * b) % 5


# task -> (target, ground-truth verdict)
TASKS = {
    "add": (_add, "separated"),
    "mul": (_mul, "channel-limited"),
    "square": (_square, "channel-limited"),
    "modp": (_modp, "law-surviving"),
}


def _fit(A, b, coeffs):
    resid = [sum(A[i][j] * coeffs[j] for j in range(len(coeffs))) - b[i] for i in range(len(A))]
    return Fraction(1, 2) * sum(v * v for v in resid)


def fit(task, lift, data=GRID):
    """Exact closed-form fit of ``task`` under feature ``lift``; returns coefficients and loss."""
    target, _ = TASKS[task]
    phi = LIFTS[lift]
    A = [phi(x) for x in data]
    b = [target(*x) for x in data]
    coeffs = train.least_squares(A, b)
    return {"coefficients": coeffs, "loss": _fit(A, b, coeffs)}


def verdict(task, data=GRID):
    """The coarsest lift that fits exactly (loss 0), else ``law-surviving``."""
    if fit(task, "linear", data)["loss"] == 0:
        return "separated"
    if fit(task, "quadratic", data)["loss"] == 0:
        return "channel-limited"
    return "law-surviving"


def sample_efficiency(task, lift, data=GRID):
    """Fewest leading examples for an exact fit (``loss == 0``), or ``None``."""
    target, _ = TASKS[task]
    phi = LIFTS[lift]
    for n in range(1, len(data) + 1):
        sub = data[:n]
        A = [phi(x) for x in sub]
        b = [target(*x) for x in sub]
        try:
            coeffs = train.least_squares(A, b)
        except ValueError:  # singular (too few / degenerate examples)
            continue
        if _fit(A, b, coeffs) == 0:
            return n
    return None


def benchmark_tasks():
    """B1 (exact fit + verdict) and B2 (sample efficiency) over the ladder."""
    rows = []
    for task in TASKS:
        rows.append({
            "task": task,
            "loss_linear": fit(task, "linear")["loss"],
            "loss_quadratic": fit(task, "quadratic")["loss"],
            "verdict": verdict(task),
            "expected": TASKS[task][1],
            "samples_linear": sample_efficiency(task, "linear"),
            "samples_quadratic": sample_efficiency(task, "quadratic"),
        })
    return rows
