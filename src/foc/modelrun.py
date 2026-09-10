"""An exact model run of the probe-audit protocol (``docs/16``).

A *controlled* model (known feature encoding) audited end-to-end, exactly. The
model is a **pairwise-correlation head**: an input triple ``(a, b, c)`` prepares
a two-site state

    rho(a, b, c) = (1/4) [ I(x)I + a Z(x)I + c Z(x)Z ],

where ``b`` is not used. Ground truth:

- ``a`` is encoded in site A's marginal        -> a **linear** (one-body) feature;
- ``c`` is encoded only in the A-B correlation -> a **joint** (two-body) feature;
- ``b`` is not encoded at all.

The audit should return separated / channel-limited / law-surviving, and
``model_run`` scores the verdicts against that ground truth (``docs/13``, ``16``).
"""

from fractions import Fraction

from . import linalg as la
from . import ambiguity as amb

I2 = la.identity(2)
X = la.mat([[0, 1], [1, 0]])
Y = la.mat([[0, -1], [1, 0]])
Z = la.mat([[1, 0], [0, -1]])


def _op(a, b):
    return la.kron(a, b)


# probe families: one-body (local) and one-body + two-body (joint)
LOCAL = [_op(P, I2) for P in (X, Y, Z)] + [_op(I2, P) for P in (X, Y, Z)]
JOINT = LOCAL + [_op(P, Q) for P in (X, Y, Z) for Q in (X, Y, Z)]


def correlation_head(a, b, c):
    """The model: ``(a, b, c) -> rho = (1/4)[I + a Z(x)I + c Z(x)Z]``, exact. ``b`` is ignored."""
    a = Fraction(a)
    c = Fraction(c)
    rho = la.scale(Fraction(1, 4), la.identity(4))
    rho = la.mat_add(rho, la.scale(a / 4, _op(Z, I2)))
    rho = la.mat_add(rho, la.scale(c / 4, _op(Z, Z)))
    return rho


def _feature(x1, x2):
    return la.mat_sub(correlation_head(*x1), correlation_head(*x2))


def model_run(margin=None):
    """Run the probe audit on the correlation-head model, scored against ground truth.

    Features: the marginal ``a`` (ground truth *separated*), the correlation ``c``
    (*channel-limited*), and the null input ``b`` (*law-surviving*). With a
    ``margin`` the verdict is the ``docs/13`` margin verdict instead of the exact one.
    """
    cases = [
        ("marginal a", _feature((1, 0, 0), (0, 0, 0)), "separated"),
        ("correlation c", _feature((0, 0, 1), (0, 0, 0)), "channel-limited"),
        ("null b", _feature((0, 1, 0), (0, 0, 0)), "law-surviving"),
    ]
    rows = []
    for name, delta, truth in cases:
        s_local = amb.feature_separation(delta, LOCAL)
        s_joint = amb.feature_separation(delta, JOINT)
        if margin is None:
            verdict = amb.classify(delta, LOCAL, JOINT)
        elif s_local >= margin:
            verdict = "separated"
        elif s_joint >= margin:
            verdict = "channel-limited"
        else:
            verdict = "law-surviving"
        rows.append({
            "feature": name,
            "sep_local": s_local,
            "sep_joint": s_joint,
            "verdict": verdict,
            "ground_truth": truth,
            "correct": verdict == truth,
        })
    return rows
