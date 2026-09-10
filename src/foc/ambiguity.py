"""The ambiguity dichotomy: annihilator classification, linear symmetry, collapse.

``docs/08`` §4, ``docs/09`` §2-§3, ``docs/10``. Everything is exact (``Fraction``).
The three computable pieces are:

- the **annihilator** ``A_E = M_E^{\\perp}`` of an accessible effect span, which
  decides separated / channel-limited / law-surviving (``classify``);
- the **linear symmetry algebra** ``a(L)``, which decides whether a continuous
  ambiguity is a symmetry or an accidental degeneracy (``linear_symmetry_dim``);
- the **collapse threshold** ``2e = d`` of distortion (``collapses``).
"""

import itertools
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


def symmetry_examples():
    """The continuous / discrete / accidental trichotomy of ``docs/09`` §2.

    Returns ``(name, dim_a_L, kind)`` for four law maps, with ``a(L)`` computed
    from a finite generic grid of sample points. ``dim a(L) = 0`` means no
    continuous linear symmetry: the ambiguity is either discrete (a finite
    orbit) or accidental (a generic coincidence).
    """
    pts = [(Fraction(a), Fraction(b)) for a in (-2, -1, 1, 2) for b in (-2, -1, 1, 2)]
    pts_nn = [(Fraction(a), Fraction(b)) for a in (0, 1, 2, 3) for b in (0, 1, 2, 3)]
    cases = [
        ("x^2+y^2", lambda t: [[2 * t[0], 2 * t[1]]], pts, "continuous (rotation)"),
        ("x*y", lambda t: [[t[1], t[0]]], pts, "continuous (scaling)"),
        ("x^3+y^3", lambda t: [[3 * t[0] ** 2, 3 * t[1] ** 2]], pts, "no linear symmetry"),
        ("(eta+delta, eta*delta)",
         lambda t: [[Fraction(1), Fraction(1)], [t[1], t[0]]], pts_nn, "discrete (Z/2)"),
    ]
    return [
        (name, linear_symmetry_dim(jac, grid, 2), kind)
        for name, jac, grid, kind in cases
    ]


def polynomial_symmetry_dim(jacobian, d, grid, n=2):
    """Dimension of the degree-``<= d`` **polynomial** symmetry space (``docs/12``).

    Fields are ``X_i(theta) = sum_{|alpha|<=d} c_{i,alpha} theta^alpha``; the
    condition ``DL(theta) X(theta) = 0`` on the sample ``grid`` is a linear
    system whose kernel is the symmetry space. For a rank-one law map this space is
    the degree-``<= d`` section space of ``ker DL``, of dimension ``d(d+1)/2`` --
    it grows without bound, so the *intrinsic* symmetry algebra is
    infinite-dimensional. The ``grid`` must be large enough to pin the polynomial
    identity ``DL X = 0`` (at least ``deg(DL) + d + 1`` points per variable).
    """
    exps = [a for a in itertools.product(range(d + 1), repeat=n) if sum(a) <= d]
    n_unk = len(exps) * n
    rows = []
    for th in grid:
        J = jacobian(th)
        for k in range(len(J)):
            row = [Fraction(0)] * n_unk
            for mi, a in enumerate(exps):
                val = Fraction(1)
                for i in range(n):
                    val *= th[i] ** a[i]
                for i in range(n):
                    row[mi * n + i] += J[k][i] * val
            rows.append(row)
    return n_unk - _rank(rows)


def rank1_symmetry_field(jacobian):
    """The tangent field ``X = (L_y, -L_x)`` of a rank-one law map ``R^2 -> R``.

    It satisfies ``DL . X = L_x L_y - L_y L_x = 0`` identically, so by the
    rank-one theorem (``docs/12``) *every* rank-one fiber is a 1-parameter group
    orbit -- its flow. ``rank1_symmetry_field(jac)(theta)`` returns the value
    ``X(theta)``.
    """
    def field(th):
        J = jacobian(th)[0]  # DL = (L_x, L_y)
        return (J[1], -J[0])
    return field


def symmetry_growth():
    """Degree-filtered polynomial symmetry dimension for ``L = x^2 + y^2``.

    Returns ``[(d, dim)]``; the values are the triangular numbers ``d(d+1)/2``,
    the dimension of the degree-``<= d`` sections of ``ker DL`` -- evidence that
    the intrinsic symmetry algebra is infinite-dimensional (``docs/12``).
    """
    grid = [(Fraction(i), Fraction(j)) for i in range(7) for j in range(7)]
    jac = lambda t: [[2 * t[0], 2 * t[1]]]
    return [(d, polynomial_symmetry_dim(jac, d, grid)) for d in (1, 2, 3, 4)]


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


def llm_probe_audit():
    """An LLM-style probe audit on a two-site toy representation (``docs/10`` §5).

    The representation is a two-site residual pair. Probe families, coarse to
    fine: ``"local"`` reads one site at a time; ``"joint"`` adds cross-site
    readouts. A measurement ``model`` says whether joint probes are admissible.

    For each **feature** (a difference between two representation states) the
    audit returns a verdict and the action it licenses:

    - ``separated`` — a declared probe reads it now;
    - ``channel-limited`` — a *richer* declared probe reads it: build one;
    - ``law-surviving`` — no declared probe reads it: stop, it is not in the
      record.

    This is the ``docs/10`` §5 decision procedure: a failed probe is ambiguous
    between "get a better probe" and "not there", and the audit says which.
    """
    def op(a, b):
        return la.kron(a, b)

    local = [op(X, I2), op(Z, I2), op(I2, X), op(I2, Z)]
    joint = local + [op(a, b) for a in (X, Z) for b in (X, Z)]
    families = {"open": [local, joint], "local-only": [local]}
    features = [("site-A logit", op(Z, I2)), ("cross-site correlation", op(Z, Z))]

    rows = []
    for model, fams in families.items():
        for name, delta in features:
            idx = probe_audit(delta, fams)
            if idx == 0:
                verdict, action = "separated", "read it with the current probe"
            elif idx is not None:
                verdict, action = "channel-limited", "build a richer probe"
            else:
                verdict, action = "law-surviving", "stop: not in the record"
            rows.append({
                "feature": name,
                "model": model,
                "verdict": verdict,
                "action": action,
            })
    return rows
