"""Quantitative replacement robustness (``docs/30``).

``docs/05`` and ``docs/21`` decide *whether* a coarse replacement is valid for a
declared downstream — a binary, source-relative criterion. This module quantifies
*how bad* a replacement can be over a **declared uncertainty set**, and exactly
when the worst case is attained. Everything is exact ``Fraction`` arithmetic.

Four results:

- **minimax retention** (``docs/30`` §2): subtract the coarse risk *before* the
  worst-case maximum; the minimax excess ``V(s,u) = min_a max_{t<=u} (R-G)`` is
  nondecreasing in the bound ``u`` and always ``<= 0`` (coarse is available).
- **the replacement envelope** (``docs/30`` §3): over a product-of-simplices
  replacement class the per-world worst case is ``U_t = (1-t)c + tS``; a
  *strictly positive* law attains it iff zero is a worst world or every fiber's
  coefficients are constant over its complete alphabet.
- **continuous retention** (``docs/30`` §4): ``Q(a) = A a^2 - 2 B a`` on ``[0,1]``
  has optimizer ``clip(B/A, 0, 1)``; the exact KKT identity and the sharp
  finite-menu gap bound ``16 * gap <= A``.
- **aggregate is not per-instance** (``docs/30`` §5): the signed groups ``P+N+Z``
  reproduce the aggregate *coefficientwise*, so an aggregate zero can hide
  equal-and-opposite per-history excesses and a worst case for the aggregate need
  not bound any single history.
- **opposite tilts cancel** (``docs/30`` §6): the forward/reverse stress tilts
  average to the uniform law, hence ``(M_forward + M_reverse)/2 = M0``.
"""

from fractions import Fraction


# --- 1. minimax retention over a declared uncertainty set --------------------

def excess(risk, coarse):
    """The signed excess ``E = R - G``: subtract coarse *before* any maximum."""
    return risk - coarse


def excess_table(problem):
    """Replace every risk by its excess ``R - G`` (same shape: worlds x assumed x rules)."""
    out = []
    for world in problem["worlds"]:
        g = world["coarse"]
        out.append([[r - g for r in row] for row in world["risks"]])
    return out


def affine_in_t(problem):
    """Check ``E(t) = (1-t) E(0) + t E(1)`` for every assumed model and rule.

    A fixed replacement rule with an affine-in-``t`` actual law gives an affine
    excess in the actual noise level. The minimax algorithm does not need it, but
    the endpoint-membership control does.
    """
    E = excess_table(problem)
    lo, hi = E[0], E[-1]
    for idx, world in enumerate(problem["worlds"]):
        t = problem["levels"][idx]
        for s in range(len(lo)):
            for a in range(len(lo[s])):
                if E[idx][s][a] != (1 - t) * lo[s][a] + t * hi[s][a]:
                    return False
    return True


def worst_excess(problem, assumed, bound_index, rule_index):
    """``M(s,u,a) = max_{t <= u} E(t,s,a)`` — the worst case over the bound."""
    E = excess_table(problem)
    return max(E[t][assumed][rule_index] for t in range(bound_index + 1))


def minimax_certificate(problem):
    """The complete minimax retention certificate (``docs/30`` §2).

    For every assumed model ``s`` and every declared bound ``u``: each rule's
    worst-case excess, the minimax value ``V = min_a M``, *all* minimizers, and
    the nested-monotonicity check against the previous bound.
    """
    weights = problem["weights"]
    n_models = len(problem["worlds"][0]["risks"])
    certs = []
    for s in range(n_models):
        previous = None
        for u in range(len(problem["levels"])):
            candidates = []
            for a in range(len(weights)):
                we = [excess_table(problem)[t][s][a] for t in range(u + 1)]
                worst = max(we)
                candidates.append({
                    "weight": weights[a],
                    "world_excesses": we,
                    "worst": worst,
                    "worst_indices": [t for t in range(u + 1) if we[t] == worst],
                })
            value = min(c["worst"] for c in candidates)
            minimizers = [i for i, c in enumerate(candidates) if c["worst"] == value]
            certs.append({
                "assumed": s,
                "bound": u,
                "candidates": candidates,
                "minimax": value,
                "minimizer_indices": minimizers,
                "minimizer_weights": [weights[i] for i in minimizers],
                "coarse_available": any(w == 0 for w in weights),
                "nondecreasing": previous is None or value >= previous,
            })
            previous = value
    return certs


def minimax_values(problem):
    """The minimax value ``V(s,u)`` for every ``(assumed, bound)`` pair."""
    return [[c["minimax"] for c in minimax_certificate(problem) if c["assumed"] == s]
            for s in range(len(problem["worlds"][0]["risks"]))]


# --- 2. the replacement envelope ---------------------------------------------

def envelope(clean_excess, full_excess, t):
    """``U_t = (1-t) c + t S`` — the per-world replacement envelope."""
    return (1 - t) * clean_excess + t * full_excess


def full_replacement_max(fibers):
    """``S = sum_N max_z B_N(z)`` — the full-retention upper excess.

    ``fibers`` is a list of fibers, each a list of its alphabet's coefficients.
    """
    return sum(max(B) for B in fibers)


def all_fibers_flat(fibers):
    """True iff every fiber's coefficients are constant over its alphabet."""
    return all(all(b == B[0] for b in B) for B in fibers)


def full_support_maximum_attained(clean_excess, fibers, envelope_maximum, worst_indices):
    """``docs/30`` §3: is the envelope maximum attained by a *strictly positive* law?

    Exactly when zero is a worst world (then every law, including full support,
    attains ``c``) or every fiber is flat (then every law attains ``S``).
    """
    zero_is_worst = 0 in worst_indices
    return zero_is_worst or all_fibers_flat(fibers)


def envelope_profile(clean_excess, fibers, levels):
    """Compute the envelope, its maximum, and the full-support attainment test."""
    S = full_replacement_max(fibers)
    values = [envelope(clean_excess, S, t) for t in levels]
    maximum = max(values)
    worst_indices = [i for i, v in enumerate(values) if v == maximum]
    attained = full_support_maximum_attained(clean_excess, fibers, maximum, worst_indices)
    return {
        "full_excess": S,
        "envelopes": values,
        "maximum": maximum,
        "worst_indices": worst_indices,
        "zero_is_worst": 0 in worst_indices,
        "all_fibers_flat": all_fibers_flat(fibers),
        "full_support_maximum_attained": attained,
        "every_full_support_mechanism_strict": maximum < 0 or (maximum == 0 and not attained),
    }


# --- 3. continuous retention and its discretization cost ---------------------

def retention_excess(A, B, a):
    """A single convex quadratic excess ``Q(a) = A a^2 - 2 B a`` (``docs/30`` §4)."""
    return A * a * a - 2 * B * a


def retention_optimizer(A, B):
    """Minimizer of ``Q`` on ``[0,1]``: a point, or the whole interval when flat."""
    if A == 0:
        if B > 0:
            return {"kind": "point", "weight": Fraction(1)}
        if B < 0:
            return {"kind": "point", "weight": Fraction(0)}
        return {"kind": "interval", "lower": Fraction(0), "upper": Fraction(1)}
    a = B / A
    if a < 0:
        a = Fraction(0)
    if a > 1:
        a = Fraction(1)
    return {"kind": "point", "weight": a}


def retention_minimum(A, B):
    """The continuous minimum ``min_{a in [0,1]} Q(a)``."""
    opt = retention_optimizer(A, B)
    if opt["kind"] == "interval":
        return Fraction(0)
    return retention_excess(A, B, opt["weight"])


def retention_kkt(A, B, a, astar):
    """The exact KKT identity ``Q(a) - Q(a*) = A (a-a*)^2 + g* (a-a*)``, ``g* = 2A a* - 2B``."""
    gstar = 2 * A * astar - 2 * B
    return (retention_excess(A, B, a) - retention_excess(A, B, astar)
            == A * (a - astar) ** 2 + gstar * (a - astar))


def menu_gap(A, B, menu):
    """``min_menu Q - min Q`` — the cost of restricting the weight to a finite menu."""
    return min(retention_excess(A, B, a) for a in menu) - retention_minimum(A, B)


def menu_gap_sharp(A, B, menu):
    """``16 * menu_gap <= A`` — the sharp ``1/16`` discretization bound (``docs/30`` §4)."""
    return 16 * menu_gap(A, B, menu) <= A


# --- 4. aggregate is not per-instance ----------------------------------------

def history_excess(A, B, a):
    """A history's conditional excess polynomial ``A a^2 - 2 B a`` (``docs/30`` §5)."""
    return A * a * a - 2 * B * a


def aggregate_coefficients(histories):
    """``(sum_H w_H A_H, sum_H w_H B_H)`` — the aggregate excess polynomial."""
    return (sum(w * A for w, A, _ in histories),
            sum(w * B for w, _, B in histories))


def group_polynomials(histories, a):
    """Signed sign-partition ``P + N + Z`` of the weighted per-history excesses.

    ``histories`` is ``[(w, A, B), ...]``. The three group values sum to the
    aggregate *value* at ``a`` (and, coefficientwise, to the aggregate polynomial).
    """
    positive = negative = zero = Fraction(0)
    pos_idx, neg_idx, zero_idx = [], [], []
    for i, (w, A, B) in enumerate(histories):
        q = history_excess(A, B, a)
        if q > 0:
            positive += w * q
            pos_idx.append(i)
        elif q < 0:
            negative += w * q
            neg_idx.append(i)
        else:
            zero += w * q
            zero_idx.append(i)
    return {
        "positive": positive,
        "negative": negative,
        "zero": zero,
        "aggregate": positive + negative + zero,
        "positive_indices": pos_idx,
        "negative_indices": neg_idx,
        "zero_indices": zero_idx,
    }


def aggregate_zero_hides_risk(histories, a):
    """Report whether an aggregate zero at ``a`` hides nonzero per-history risks."""
    groups = group_polynomials(histories, a)
    return {
        "aggregate": groups["aggregate"],
        "is_zero": groups["aggregate"] == 0,
        "hides": groups["aggregate"] == 0
        and (groups["positive"] != 0 or groups["negative"] != 0),
        "positive": groups["positive"],
        "negative": groups["negative"],
    }


# --- 5. opposite stress tilts cancel -----------------------------------------

def forward_tilt(m):
    """``mu_forward(z_r|N) = 2(r+1) / (m(m+1))`` for ``r = 0..m-1``."""
    return [Fraction(2 * (r + 1), m * (m + 1)) for r in range(m)]


def reverse_tilt(m):
    """``mu_reverse(z_r|N) = 2(m-r) / (m(m+1))`` for ``r = 0..m-1``."""
    return [Fraction(2 * (m - r), m * (m + 1)) for r in range(m)]


def tilt_mean(m):
    """The two tilts average pointwise to the uniform law ``1/m``."""
    f, r = forward_tilt(m), reverse_tilt(m)
    return [(f[i] + r[i]) / 2 for i in range(m)]


def tilts_are_opposite(m):
    """True iff both tilts are positive, normalized, and average to uniform."""
    f, r = forward_tilt(m), reverse_tilt(m)
    return (
        all(x > 0 for x in f) and all(x > 0 for x in r)
        and sum(f) == 1 and sum(r) == 1
        and tilt_mean(m) == [Fraction(1, m)] * m
    )


def tilt_cancellation(M_forward, M_reverse, M0):
    """``(M_forward + M_reverse)/2 = M0`` — the opposite tilts cancel exactly."""
    return (M_forward + M_reverse) / 2 == M0


# --- the demonstration -------------------------------------------------------

_LEVELS = [Fraction(0), Fraction(1, 2), Fraction(3, 4), Fraction(1)]
_WEIGHTS = [Fraction(0), Fraction(1, 2), Fraction(1)]


def _demo_problem():
    """A small exact AA-style risk table: two assumed models, four noise levels.

    Model ``s=0`` has an affine excess increasing in ``t`` (a rule that helps at
    clean and hurts under shift); model ``s=1`` has a constant negative excess
    for the non-coarse rules (a strict, robust benefit).
    """
    g = Fraction(1, 2)
    return {
        "levels": _LEVELS,
        "weights": _WEIGHTS,
        "worlds": [
            {"coarse": g, "risks": [[g, Fraction(3, 8), Fraction(1, 4)],
                                    [g, Fraction(3, 8), Fraction(1, 4)]]},
            {"coarse": g, "risks": [[g, g, g],
                                    [g, Fraction(3, 8), Fraction(1, 4)]]},
            {"coarse": g, "risks": [[g, Fraction(9, 16), Fraction(5, 8)],
                                    [g, Fraction(3, 8), Fraction(1, 4)]]},
            {"coarse": g, "risks": [[g, Fraction(5, 8), Fraction(3, 4)],
                                    [g, Fraction(3, 8), Fraction(1, 4)]]},
        ],
    }


def replacement_report():
    """Assemble the replacement-robustness results (``docs/30`` §7)."""
    problem = _demo_problem()
    certs = minimax_certificate(problem)
    fibers_sharp = [[Fraction(1, 2), Fraction(1, 2), Fraction(0)],
                    [Fraction(1, 4), Fraction(3, 4)]]
    fibers_flat = [[Fraction(1, 3), Fraction(1, 3)], [Fraction(1, 2), Fraction(1, 2)]]
    fibers_clean = [[Fraction(1), Fraction(1, 2), Fraction(0)]]
    A, B, menu = Fraction(1, 2), Fraction(3, 10), _WEIGHTS
    astar = retention_optimizer(A, B)["weight"]
    histories = [(Fraction(1, 2), Fraction(1), Fraction(1, 2)),
                 (Fraction(1, 2), Fraction(1), Fraction(0))]
    return {
        "affine": affine_in_t(problem),
        "minimax": certs,
        "values": minimax_values(problem),
        "envelope_sharp": envelope_profile(Fraction(1, 10), fibers_sharp, _LEVELS),
        "envelope_flat": envelope_profile(Fraction(1, 10), fibers_flat, _LEVELS),
        "envelope_clean_worst": envelope_profile(Fraction(2), fibers_clean, _LEVELS),
        "retention": {
            "A": A, "B": B, "optimizer": astar,
            "minimum": retention_minimum(A, B),
            "kkt_at_half": retention_kkt(A, B, Fraction(1, 2), astar),
            "menu_gap": menu_gap(A, B, menu),
            "menu_gap_sharp": menu_gap_sharp(A, B, menu),
        },
        "aggregate_zero": aggregate_zero_hides_risk(histories, Fraction(1, 2)),
        "aggregate_coefficients": aggregate_coefficients(histories),
        "tilts": {
            "m": 4,
            "forward": forward_tilt(4),
            "reverse": reverse_tilt(4),
            "opposite": tilts_are_opposite(4),
            "cancellation": tilt_cancellation(Fraction(3, 20), Fraction(-3, 20), Fraction(0)),
        },
    }
