"""A genuine transformer trained exactly, without floats (``docs/18``).

This corrects the earlier claim that a trained transformer needs floating point.
It does not: the only irrational primitives are softmax/``exp``, LayerNorm/``sqrt``,
and GELU/SiLU/``erf``; each has an exact rational substitute (linear or
**squared-normalized** attention, sum normalization, **ReLU**). What follows is a
one-head transformer block -- squared-normalized attention, a ReLU MLP, and a
residual stream -- with exact forward-mode automatic differentiation over
``Fraction`` (dual numbers), trained by exact gradient descent.

The honest cost is *arithmetic growth*: exact denominators roughly triple in bits
per step, so full-model exact training is practical only for a few steps (see
``docs/18``). Floats are a practical representation, not a logical necessity.
"""

import sys
from fractions import Fraction

if hasattr(sys, "set_int_max_str_digits"):
    sys.set_int_max_str_digits(1_000_000)


# --- forward-mode AD: dual numbers over Q -----------------------------------

class Dual:
    """A value with a derivative, over ``Fraction`` (exact forward-mode AD)."""

    __slots__ = ("v", "d")

    def __init__(self, v, d=0):
        self.v = v if isinstance(v, Fraction) else Fraction(v)
        self.d = d if isinstance(d, Fraction) else Fraction(d)

    def __add__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.v + o.v, self.d + o.d)

    __radd__ = __add__

    def __sub__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.v - o.v, self.d - o.d)

    def __rsub__(self, o):
        return Dual(o) - self

    def __mul__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.v * o.v, self.v * o.d + self.d * o.v)

    __rmul__ = __mul__

    def __truediv__(self, o):
        o = o if isinstance(o, Dual) else Dual(o)
        return Dual(self.v / o.v, (self.d * o.v - self.v * o.d) / (o.v * o.v))

    def __neg__(self):
        return Dual(-self.v, -self.d)

    def __pow__(self, k):
        r = Dual(1)
        for _ in range(k):
            r = r * self
        return r


def _relu(x):
    """ReLU: exact for rationals; subgradient 0 at the kink."""
    return Dual(x.v, x.d) if x.v > 0 else Dual(0, 0)


def _T(A):
    return [list(r) for r in zip(*A)]


def _mm(A, B):
    return [
        [sum((A[i][k] * B[k][j] for k in range(len(B))), Dual(0)) for j in range(len(B[0]))]
        for i in range(len(A))
    ]


def _mat(v):
    return [v[0:2], v[2:4]]


# --- the transformer block ---------------------------------------------------

def _params_to_dual(ws, seed=None):
    return [Dual(w, 1 if seed == i else 0) for i, w in enumerate(ws)]


def _forward_dual(ws, X):
    WQ, WK, WV, W1, W2 = (_mat(ws[0:4]), _mat(ws[4:8]), _mat(ws[8:12]),
                          _mat(ws[12:16]), _mat(ws[16:20]))
    w = ws[20:22]
    Q, K, V = _mm(X, WQ), _mm(X, WK), _mm(X, WV)
    S = _mm(Q, _T(K))
    Sq = [[s * s for s in row] for row in S]                    # squared-normalized attention
    den = [sum(row, Dual(0)) for row in Sq]
    A = [[Sq[i][j] / den[i] for j in range(len(Sq[i]))] for i in range(len(Sq))]
    O = _mm(A, V)
    X1 = [[X[i][j] + O[i][j] for j in range(len(X[0]))] for i in range(len(X))]   # residual
    H = [[_relu(x) for x in row] for row in _mm(X1, W1)]                          # ReLU MLP
    HW2 = _mm(H, W2)
    X2 = [[X1[i][j] + HW2[i][j] for j in range(len(X1[0]))] for i in range(len(X1))]
    h = X2[-1]
    return sum((h[j] * w[j] for j in range(len(w))), Dual(0))


def _loss_dual(ws, data):
    return sum((( _forward_dual(ws, X) - y) ** 2 for X, y in data), Dual(0)) / 2


def loss(ws, data):
    """Exact loss value (``Fraction``) at ``ws``."""
    return _loss_dual(_params_to_dual(ws), data).v


def grad(ws, data, k):
    """Exact partial derivative of the loss w.r.t. parameter ``k`` (``Fraction``)."""
    return _loss_dual(_params_to_dual(ws, seed=k), data).d


def exact_step(ws, data, eta):
    """One exact gradient-descent step; every weight stays a ``Fraction``."""
    return [ws[k] - eta * grad(ws, data, k) for k in range(len(ws))]


def train_exact(data, steps=2, eta=Fraction(1, 50), init=None):
    """Exact gradient descent; returns ``[(weights, loss), ...]`` for steps 0..steps."""
    ws = list(init) if init is not None else [Fraction(2 * k + 1, 40) for k in range(22)]
    history = [(list(ws), loss(ws, data))]
    for _ in range(steps):
        ws = exact_step(ws, data, eta)
        history.append((list(ws), loss(ws, data)))
    return history


# --- a tiny task -------------------------------------------------------------

TOY_DATA = [
    ([[Fraction(1), Fraction(0)], [Fraction(0), Fraction(1)]], Fraction(1)),
    ([[Fraction(1), Fraction(1)], [Fraction(0), Fraction(1)]], Fraction(2)),
    ([[Fraction(0), Fraction(1)], [Fraction(1), Fraction(0)]], Fraction(0)),
    ([[Fraction(2), Fraction(0)], [Fraction(0), Fraction(1)]], Fraction(2)),
]
