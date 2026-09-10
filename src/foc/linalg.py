"""Exact rational matrix helpers.

Matrices are lists of lists of ``fractions.Fraction``. All entries are real for
the examples in this repository, so the adjoint coincides with the transpose.
"""

from fractions import Fraction


def frac(x) -> Fraction:
    """Coerce an int/str/Fraction to a Fraction (passes Fractions through)."""
    return x if isinstance(x, Fraction) else Fraction(x)


def mat(rows):
    """Build a matrix from nested lists of int/str/Fraction."""
    return [[frac(x) for x in row] for row in rows]


def nrow(A) -> int:
    return len(A)


def ncol(A) -> int:
    return len(A[0]) if A else 0


def mat_add(A, B):
    return [[A[i][j] + B[i][j] for j in range(ncol(A))] for i in range(nrow(A))]


def mat_sub(A, B):
    return [[A[i][j] - B[i][j] for j in range(ncol(A))] for i in range(nrow(A))]


def scale(c, A):
    c = frac(c)
    return [[c * A[i][j] for j in range(ncol(A))] for i in range(nrow(A))]


def mat_mul(A, B):
    assert ncol(A) == nrow(B), "shape mismatch"
    return [
        [sum(A[i][k] * B[k][j] for k in range(ncol(A))) for j in range(ncol(B))]
        for i in range(nrow(A))
    ]


def transpose(A):
    return [[A[j][i] for j in range(nrow(A))] for i in range(ncol(A))]


def trace(A) -> Fraction:
    return sum(A[i][i] for i in range(nrow(A)))


def identity(n):
    return [[Fraction(1 if i == j else 0) for j in range(n)] for i in range(n)]


def zero(n):
    return [[Fraction(0) for _ in range(n)] for _ in range(n)]


def kron(A, B):
    """Kronecker product (for tensor-product / separate-subsystem models)."""
    ra, ca = nrow(A), ncol(A)
    rb, cb = nrow(B), ncol(B)
    out = [[Fraction(0) for _ in range(ca * cb)] for _ in range(ra * rb)]
    for i in range(ra):
        for j in range(ca):
            for k in range(rb):
                for l in range(cb):
                    out[i * rb + k][j * cb + l] = A[i][j] * B[k][l]
    return out
