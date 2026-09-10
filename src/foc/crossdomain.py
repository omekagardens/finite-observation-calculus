"""Exact witnesses of the dichotomy in three neighbouring fields (``docs/15``).

Each is a small, exact instance of the same phenomenon — observational
equivalence with a real distinction hidden in a channel a *declared* access class
does not reach:

- **causal observational equivalence** — chain vs fork: same observational law,
  different interventional ``P(Z | do(X))``;
- **conformal marginal vs conditional** — a set with valid marginal coverage and a
  stratum it never covers;
- **partial identification** — a structural mean identified only to an interval;
  the outside is *infeasible*, not merely ambiguous.
"""

from fractions import Fraction


def causal_observational_equivalence():
    """The chain ``X -> Y -> Z`` and the fork ``X <- Y -> Z`` (``docs/15``).

    Both realize ``X = Y = Z`` from an exogenous ``U ~ Bern(1/2)``, so they induce
    the *same* observational joint. They differ under intervention on ``X``: in
    the chain ``X`` causes ``Y`` and ``Z`` (``P(Z=1 | do(X=1)) = 1``); in the fork
    ``X`` is a child, so intervening leaves ``Y, Z ~ Bern(1/2)``
    (``P(Z=1 | do(X=1)) = 1/2``). The causal direction is invisible to
    observational data — *channel-limited* if interventions are admissible,
    *law-surviving* if only observations are.
    """
    obs = {(0, 0, 0): Fraction(1, 2), (1, 1, 1): Fraction(1, 2)}
    chain_do = Fraction(1)      # X -> Y -> Z: do(X=1) forces Y=1, Z=1
    fork_do = Fraction(1, 2)    # X <- Y -> Z: do(X=1) leaves Y,Z ~ Bern(1/2)
    return {
        "observational": obs,
        "chain_P_Z_given_do_X1": chain_do,
        "fork_P_Z_given_do_X1": fork_do,
        "same_observational_law": True,
        "interventions_differ": chain_do != fork_do,
    }


def conformal_marginal_vs_conditional():
    """A conformal-style set with valid marginal coverage, zero on a stratum.

    The population is two strata; the set covers stratum 0 always and stratum 1
    never, and stratum 1 has mass ``1/20`` — so marginal coverage is ``19/20``
    while conditional coverage in stratum 1 is ``0`` (``docs/15``; cf. `docs/06`).
    """
    p_stratum1 = Fraction(1, 20)
    return {
        "stratum_mass": (1 - p_stratum1, p_stratum1),
        "stratum_coverage": (Fraction(1), Fraction(0)),
        "marginal_coverage": 1 - p_stratum1,
        "marginal_ok": (1 - p_stratum1) >= Fraction(19, 20),
        "conditional_coverage_stratum1": Fraction(0),
    }


def partial_identification():
    """Missing-data (Manski) bounds: the mean is identified only to an interval.

    A fraction ``f`` of ``Y`` is observed with mean ``m``; the rest is missing, so
    ``E[Y]`` lies in ``[f m, f m + (1 - f)]``. Values inside are *ambiguous* (some
    completion realizes them); values outside are *infeasible* (``docs/15``).
    """
    f = Fraction(3, 4)
    m = Fraction(1, 2)
    lo = f * m
    hi = f * m + (1 - f)
    inside = (lo + hi) / 2
    outside = hi + 1
    return {
        "identified_set": (lo, hi),
        "inside_is_ambiguous": lo <= inside <= hi,
        "outside_is_infeasible": not (lo <= outside <= hi),
    }
