"""Benchmarks B1/B2: a math-task ladder on exact-checkable tasks (``docs/25``, ``docs/27``).

Each task has a known exact target, so "learned" means ``loss == 0`` exactly. The
ladder instantiates the dichotomy and its refinement: a task a *linear* lift fits
is **separated**, one that needs a richer (higher-degree / rational) lift is
**channel-limited**, and one outside *every* declared lift is **law-surviving**.

``min_lift`` reports the coarsest lift that fits, so the ladder exposes the
*symmetry degree* of each task, not just the three-way verdict.
"""

from fractions import Fraction

from . import train

GRID = [(Fraction(a), Fraction(b)) for a in range(-3, 4) for b in range(-3, 4)]


def _linear(x):
    return [Fraction(1), x[0], x[1]]


def _quadratic(x):
    return [Fraction(1), x[0], x[1], x[0] * x[0], x[0] * x[1], x[1] * x[1]]


def _cubic(x):
    a, b = x
    return _quadratic(x) + [a ** 3, a * a * b, a * b * b, b ** 3]


def _quartic(x):
    a, b = x
    return _cubic(x) + [a ** 4, a ** 3 * b, a * a * b * b, a * b ** 3, b ** 4]


def _rational(x):
    # b/(b+4) = 1 - 4/(b+4) and ab/(b+4) = a - 4a/(b+4), so only two rational
    # features are independent of the polynomial block -- include exactly those.
    a, b = x
    d = b + 4
    return _quadratic(x) + [Fraction(1) / d, a / d]


LIFTS = {
    "linear": _linear,
    "quadratic": _quadratic,
    "cubic": _cubic,
    "quartic": _quartic,
    "rational": _rational,
}
LIFT_ORDER = ["linear", "quadratic", "cubic", "quartic", "rational"]


def _add(a, b):
    return a + b


def _mul(a, b):
    return a * b


def _square(a, b):
    return (a + b) * (a + b)


def _cube(a, b):
    return a * a * a


def _quart(a, b):
    return a * a * b * b


def _div(a, b):
    return a / (b + 4)


def _divprod(a, b):
    return (a * b) / (b + 4)


def _modp(a, b):
    return (a * b) % 5


# task -> (target, ground-truth minimal lift)
TASKS = {
    "add": (_add, "linear"),
    "mul": (_mul, "quadratic"),
    "square": (_square, "quadratic"),
    "cube": (_cube, "cubic"),
    "quart": (_quart, "quartic"),
    "div": (_div, "rational"),
    "divprod": (_divprod, "rational"),
    "modp": (_modp, "none"),
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


def min_lift(task, data=GRID):
    """The coarsest lift that fits exactly, or ``None`` (law-surviving)."""
    for name in LIFT_ORDER:
        if fit(task, name, data)["loss"] == 0:
            return name
    return None


def verdict(task, data=GRID):
    """Three-way verdict: linear -> separated, richer -> channel-limited, none -> law-surviving."""
    m = min_lift(task, data)
    if m is None:
        return "law-surviving"
    return "separated" if m == "linear" else "channel-limited"


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
    """B1 (exact fit, minimal lift, verdict) and B2 (sample efficiency) over the ladder."""
    rows = []
    for task in TASKS:
        ml = min_lift(task)
        rows.append({
            "task": task,
            "min_lift": ml or "none",
            "expected_lift": TASKS[task][1],
            "verdict": verdict(task),
            "samples_linear": sample_efficiency(task, "linear"),
            "samples_min": sample_efficiency(task, ml) if ml else None,
        })
    return rows
