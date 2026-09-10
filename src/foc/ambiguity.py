"""The ambiguity dichotomy: annihilator classification, linear symmetry, collapse.

``docs/08`` §4, ``docs/09`` §2-§3, ``docs/10``. Everything is exact (``Fraction``).
The three computable pieces are:

- the **annihilator** ``A_E = M_E^{\\perp}`` of an accessible effect span, which
  decides separated / channel-limited / law-surviving (``classify``);
- the **linear symmetry algebra** ``a(L)``, which decides whether a continuous
  ambiguity is a symmetry or an accidental degeneracy (``linear_symmetry_dim``);
- the **collapse threshold** ``2e = d`` of distortion (``collapses``).
"""

from fractions import Fraction

from . import linalg as la

# single-qubit Paulis (Y is the antisymmetric generator, used only for algebras)
I2 = la.identity(2)
X = la.mat([[0, 1], [1, 0]])
Y = la.mat([[0, -1], [1, 0]])
Z = la.mat([[1, 0], [0, -1]])

# traceless real symmetric qubit state-difference space: span{X, Z}
QUBIT_STATE_BASIS = [X, Z]


def _rank(rows):
    """Exact rank over Q of a list of row vectors."""
    if not rows:
        return 0
    M = [list(r) for r in rows]
    R, C = len(M), len(M[0])
    r = 0
    for c in range(C):
        piv = next((i for i in range(r, R) if M[i][c] != 0), None)
        if piv is None:
            continue
        M[r], M[piv] = M[piv], M[r]
        pv = M[r][c]
        M[r] = [x / pv for x in M[r]]
        for i in range(R):
            if i != r and M[i][c] != 0:
                f = M[i][c]
                M[i] = [M[i][j] - f * M[r][j] for j in range(C)]
        r += 1
    return r


def effect_rank(effects, basis):
    """Rank of the effect functionals ``rho -> Tr(rho E)`` restricted to ``span(basis)``."""
    rows = [[la.trace(la.mat_mul(B, E)) for B in basis] for E in effects]
    return _rank(rows)


def annihilator_dim(effects, basis):
    """Dimension of the annihilator ``A_E`` inside ``span(basis)`` (``docs/08`` §4).

    ``dim A_E = dim span(basis) - dim M_E``; this is the size of the invisible
    sector for the accessible effects.
    """
    return len(basis) - effect_rank(effects, basis)


def in_annihilator(delta, effects):
    """True iff ``delta`` is invisible to every effect: ``Tr(delta E) = 0`` for all E."""
    return all(la.trace(la.mat_mul(delta, E)) == 0 for E in effects)


def classify(delta, accessible, completed):
    """Classify the difference ``delta`` (``docs/08`` §4, ``docs/09`` §4).

    ``accessible`` and ``completed`` are spanning sets of effects (the second
    contains the first). Returns ``"separated"``, ``"channel-limited"``, or
    ``"law-surviving"``.
    """
    if not in_annihilator(delta, accessible):
        return "separated"
    if not in_annihilator(delta, completed):
        return "channel-limited"
    return "law-surviving"


def probe_audit(delta, families):
    """Decision procedure for a negative probing result (``docs/10`` §5).

    ``families`` is a chain of probe families, coarse to fine. Returns the index
    of the first family that separates ``delta`` — the ambiguity is
    *channel-limited* and the fix is a richer probe — or ``None`` if even the
    finest family leaves it invisible, i.e. *law-surviving*: stop, the structure
    is not in the record.
    """
    for i, family in enumerate(families):
        if not in_annihilator(delta, family):
            return i
    return None


def linear_symmetry_dim(jacobian, points, n):
    """Dimension of ``a(L) = { A in gl(n) : J(theta) A theta = 0 for all sampled theta }``.

    ``jacobian(theta)`` returns the ``m x n`` Jacobian of the law map at ``theta``
    (``docs/09`` §2). The result is the number of independent infinitesimal
    *linear* symmetries of ``L``.
    """
    rows = []
    for th in points:
        J = jacobian(th)
        for i in range(len(J)):
            row = [Fraction(0)] * (n * n)
            for j in range(n):
                for k in range(n):
                    row[j * n + k] += J[i][j] * th[k]
            rows.append(row)
    return n * n - _rank(rows)


def distortion_separation(d, e):
    """Minimax separation under distortion: ``max(d - 2e, 0)`` (``docs/09`` Prop 3.1)."""
    d = la.frac(d)
    e = la.frac(e)
    v = d - 2 * e
    return v if v > 0 else Fraction(0)


def collapses(d, e):
    """True iff distortion ``e`` collapses the separation ``d``: ``2e >= d`` (``docs/09`` §3)."""
    return 2 * la.frac(e) >= la.frac(d)


def l_inf_separation(P, Q, e):
    """Minimax TV separation under per-outcome (``l_inf``) distortion ``e`` (``docs/09`` §3).

    With ``A+ = sum_{P_i>Q_i} min(2e, P_i-Q_i)`` and symmetrically ``A-``, the
    exact separation is ``d - min(A+, A-)`` where ``d = (1/2)||P-Q||_1``. This
    equals ``distortion_separation(d, e)`` for binary laws and is smaller in
    general (a spread separation erodes faster).
    """
    P = [la.frac(x) for x in P]
    Q = [la.frac(x) for x in Q]
    e = la.frac(e)
    d = Fraction(1, 2) * sum(abs(P[i] - Q[i]) for i in range(len(P)))
    a_pos = sum(min(2 * e, P[i] - Q[i]) for i in range(len(P)) if P[i] > Q[i])
    a_neg = sum(min(2 * e, Q[i] - P[i]) for i in range(len(P)) if Q[i] > P[i])
    return d - min(a_pos, a_neg)


def l_inf_erosion_rate(P, Q):
    """Small-``e`` erosion coefficient ``2*min(k+, k-)`` for the ``l_inf`` model.

    The headline "rate two" of `docs/07` holds exactly when the separation is
    *one-sided* (``min(k+, k-) = 1``): all binary laws, and any monotone shift.
    """
    kp = sum(1 for i in range(len(P)) if P[i] > Q[i])
    kn = sum(1 for i in range(len(P)) if Q[i] > P[i])
    return 2 * min(kp, kn)


def qubit_coherence():
    """Accessible ``{Z}`` vs completed ``{Z, X}`` on a qubit.

    The coherence ``X`` is *channel-limited* (X resolves it) but *law-surviving*
    if only diagonal, Z-type effects are admissible (a superselection rule).
    """
    P0 = la.mat([[1, 0], [0, 0]])
    P1 = la.mat([[0, 0], [0, 1]])
    h = Fraction(1, 2)
    Qp = la.mat([[h, h], [h, h]])
    Qm = la.mat([[h, -h], [-h, h]])
    return {
        "accessible": [P0, P1],
        "completed": [P0, P1, Qp, Qm],
        "dim_accessible": annihilator_dim([P0, P1], QUBIT_STATE_BASIS),
        "dim_completed": annihilator_dim([P0, P1, Qp, Qm], QUBIT_STATE_BASIS),
        "class_open": classify(X, [P0, P1], [P0, P1, Qp, Qm]),
        "class_closed": classify(X, [P0, P1], [P0, P1]),
    }


def two_qubit_locality():
    """Local (one-body) access on two qubits leaves a 9-dimensional invisible sector,
    exactly the two-body correlation space; joint access removes it (``docs/10`` §2)."""
    def op(a, b):
        return la.kron(a, b)

    one_body = [op(P, I2) for P in (X, Y, Z)] + [op(I2, P) for P in (X, Y, Z)]
    pairs = [op(P, Q) for P in (X, Y, Z) for Q in (X, Y, Z)]
    full = [op(a, b) for a in (I2, X, Y, Z) for b in (I2, X, Y, Z)]
    traceless = [M for M in full if la.trace(M) == 0]  # 15 basis
    return {
        "dim_local": annihilator_dim(one_body, traceless),
        "dim_joint": annihilator_dim(one_body + pairs, traceless),
    }
