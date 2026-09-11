"""Exact rational training and a trained-model audit (``docs/17``).

Training is exact whenever the model, loss, data, initialization and step size are
all rational: closed-form least squares is a rational linear solve, and gradient
descent on a polynomial loss stays in ``Fraction``. This module trains a small
quadratic model on a controlled rational task and then runs the probe audit
(``docs/13``) on the *learned* representation, scored against what training
actually learned.

The model: ``y_hat(x) = a x_1 + c x_1 x_2`` (a linear and a product term). Its
state is

    rho(x) = (1/4) [ I(x)I + (a x_1) Z(x)I + (c x_1 x_2) Z(x)Z ].

On a task that needs only the linear term, training drives ``c -> 0`` and the
correlation feature is *not learned*; on a task that needs the product it is. The
audit recovers exactly that.
"""

from fractions import Fraction

from . import linalg as la
from . import ambiguity as amb
from . import modelrun as mr

# training data: (x1, x2, x3); the design matrix is (x1, x1 x2)
DATA = [(1, 0, 0), (1, 1, 0), (2, 1, 0), (0, 1, 0)]


def _target(task, x):
    if task == "linear":
        return Fraction(x[0])
    if task == "quadratic":
        return Fraction(x[0]) + Fraction(x[0] * x[1])
    raise ValueError(f"unknown task {task!r}")


def _design():
    return [[Fraction(x[0]), Fraction(x[0] * x[1])] for x in DATA]


def _solve(M, b):
    """Exact Gaussian elimination for the square system ``M x = b``."""
    n = len(M)
    A = [list(M[i]) + [b[i]] for i in range(n)]
    for col in range(n):
        piv = next((r for r in range(col, n) if A[r][col] != 0), None)
        if piv is None:
            raise ValueError("singular system")
        A[col], A[piv] = A[piv], A[col]
        pv = A[col][col]
        A[col] = [x / pv for x in A[col]]
        for r in range(n):
            if r != col and A[r][col] != 0:
                f = A[r][col]
                A[r] = [A[r][j] - f * A[col][j] for j in range(n + 1)]
    return tuple(A[i][n] for i in range(n))


def least_squares(A, b):
    """Exact closed-form least squares: solve ``(A^T A) x = A^T b`` over ``Q``."""
    m, n = len(A), len(A[0])
    AtA = [[sum(A[k][i] * A[k][j] for k in range(m)) for j in range(n)] for i in range(n)]
    Atb = [sum(A[k][i] * b[k] for k in range(m)) for i in range(n)]
    return _solve(AtA, Atb)


def gradient_step(A, b, theta, eta):
    """One exact gradient step on ``(1/2)||A theta - b||^2`` with step ``eta``."""
    m, n = len(A), len(A[0])
    r = [sum(A[k][j] * theta[j] for j in range(n)) - b[k] for k in range(m)]
    g = [sum(A[k][i] * r[k] for k in range(m)) for i in range(n)]
    return tuple(theta[i] - eta * g[i] for i in range(n))


def _loss(A, b, theta):
    m, n = len(A), len(A[0])
    r = [sum(A[k][j] * theta[j] for j in range(n)) - b[k] for k in range(m)]
    return Fraction(1, 2) * sum(v * v for v in r)


def train_toy(task="quadratic", steps=2, eta=Fraction(1, 20)):
    """Train ``(a, c)`` by closed-form least squares and ``steps`` exact GD steps."""
    A = _design()
    b = [_target(task, x) for x in DATA]
    ls = least_squares(A, b)
    theta = (Fraction(0), Fraction(0))
    gd = []
    for _ in range(steps):
        theta = gradient_step(A, b, theta, eta)
        gd.append(theta)
    return {
        "task": task,
        "ls": ls,
        "gd": gd,
        "loss_ls": _loss(A, b, ls),
        "loss_gd": [_loss(A, b, t) for t in gd],
    }


def _op(a, b):
    return la.kron(a, b)


def trained_audit(task="quadratic", steps=2, eta=Fraction(1, 20)):
    """Audit the *learned* representation of the trained model (``docs/17``).

    State-space features at probe input ``x = (1, 1, 0)``: the marginal part
    ``(a/4) Z(x)I``, the correlation part ``(c/4) Z(x)Z``, and the distractor
    ``x_3`` (which the model never uses). Verdicts come from ``ambiguity.classify``.
    """
    tr = train_toy(task, steps, eta)
    a, c = tr["ls"]
    delta_marg = la.scale(a / 4, _op(mr.Z, mr.I2))
    delta_corr = la.scale(c / 4, _op(mr.Z, mr.Z))
    delta_dist = la.zero(4)
    cases = [
        ("marginal a", delta_marg, "separated"),
        ("correlation c", delta_corr,
         "channel-limited" if c != 0 else "law-surviving"),
        ("distractor x_3", delta_dist, "law-surviving"),
    ]
    rows = []
    for name, delta, expected in cases:
        verdict = amb.classify(delta, mr.LOCAL, mr.JOINT)
        rows.append({
            "feature": name,
            "sep_local": amb.feature_separation(delta, mr.LOCAL),
            "sep_joint": amb.feature_separation(delta, mr.JOINT),
            "verdict": verdict,
            "expected": expected,
            "correct": verdict == expected,
        })
    return {"trained": tr, "rows": rows}
