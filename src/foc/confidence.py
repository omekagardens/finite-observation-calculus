"""Finite-record confidence: binomial intervals, separation budgets, distortion."""

from fractions import Fraction
from math import comb

from . import linalg as la


# --- exact binomial tools ---------------------------------------------------

def binomial_pmf(k, n, p):
    p = la.frac(p)
    return Fraction(comb(n, k)) * (p ** k) * ((1 - p) ** (n - k))


def binomial_cdf(k, n, p):
    return sum(binomial_pmf(i, n, p) for i in range(k + 1))


def binomial_sf(k, n, p):
    """P(X >= k), the upper tail."""
    return 1 - (binomial_cdf(k - 1, n, p) if k > 0 else 0)


# --- Clopper-Pearson interval (simultaneous coverage) -----------------------

def _bisect_low(k, n, a2, K=20):
    """Lower endpoint: the p where the increasing tail P(X >= k | p) crosses a2.

    Returns a value rounded *downward* (outward), preserving coverage.
    """
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(K):
        mid = (lo + hi) / 2
        if binomial_sf(k, n, mid) >= a2:
            hi = mid  # root at or below mid
        else:
            lo = mid  # root above mid
    return lo


def _bisect_high(k, n, a2, K=20):
    """Upper endpoint: the p where the decreasing tail P(X <= k | p) crosses a2.

    Returns a value rounded *upward* (outward), preserving coverage.
    """
    lo, hi = Fraction(0), Fraction(1)
    for _ in range(K):
        mid = (lo + hi) / 2
        if binomial_cdf(k, n, mid) >= a2:
            lo = mid  # root at or above mid (cdf decreasing)
        else:
            hi = mid  # root below mid
    return hi


def clopper_pearson(k, n, alpha, K=20):
    """Exact Clopper-Pearson interval ``[low, high]`` with outward rounding.

    Satisfies ``P(low <= p <= high | p) >= 1 - alpha`` for every ``p`` in
    ``[0, 1]`` (simultaneous coverage over the continuous domain).
    """
    alpha = la.frac(alpha)
    a2 = alpha / 2
    low = Fraction(0) if k == 0 else _bisect_low(k, n, a2, K)
    high = Fraction(1) if k == n else _bisect_high(k, n, a2, K)
    return low, high


# --- marginal vs. conditional coverage --------------------------------------

def marginal_vs_conditional():
    """An exact demonstration that unconditional coverage does not imply
    conditional coverage.

    ``n=4, p=1/4``. On outcome ``X=3`` the procedure reports the singleton
    ``{3/4}``; otherwise it abstains. Unconditional coverage is ``61/64 >= 19/20``,
    yet conditional on the singleton being reported the guess is always wrong.
    """
    n = 4
    p = Fraction(1, 4)
    guess = Fraction(3, 4)
    prob_singleton = binomial_pmf(3, n, p)          # 3/64
    return {
        "n": n,
        "p": p,
        "singleton_guess": guess,
        "prob_singleton": prob_singleton,
        "unconditional_coverage": 1 - prob_singleton,   # 61/64
        "unconditional_coverage_ok": (1 - prob_singleton) >= Fraction(19, 20),
        "conditional_error_given_singleton": Fraction(1),
    }


# --- separation budget and acquisition distortion ---------------------------

def distortion_margin(D, e):
    """Distorted separation ``D_e = max(D - 2e, 0)``."""
    D = la.frac(D)
    e = la.frac(e)
    v = D - 2 * e
    return v if v > 0 else Fraction(0)


def budget_slack(D, e, m=256):
    """``slack = D - 2e - 2/m``."""
    return la.frac(D) - 2 * la.frac(e) - Fraction(2, la.frac(m))


def budget_score(n, slack):
    """``score = n * slack^2``."""
    return la.frac(n) * slack ** 2


def sufficient(D, e, n=65536, m=256, threshold=10):
    """The fixed-budget certificate: ``slack > 0`` and ``score >= threshold``."""
    slack = budget_slack(D, e, m)
    return slack > 0 and budget_score(n, slack) >= threshold


def bv_table():
    """The eight class/error rows of the distortion census.

    Each row ``(name, D, e_fraction)`` has ``e = D * e_fraction`` with
    ``e_fraction`` in ``{0, 1/4, 1/2}``.
    """
    rows = [
        ("uniform/zero", Fraction(3, 64), Fraction(0)),
        ("uniform/quarter", Fraction(3, 64), Fraction(1, 4)),
        ("uniform/contact", Fraction(3, 64), Fraction(1, 2)),
        ("half/zero", Fraction(1, 48), Fraction(0)),
        ("half/quarter", Fraction(1, 48), Fraction(1, 4)),
        ("half/contact", Fraction(1, 48), Fraction(1, 2)),
        ("one/zero", Fraction(0), Fraction(0)),
        ("two/zero", Fraction(0), Fraction(0)),
    ]
    out = []
    for name, D, f in rows:
        e = D * f
        slack = budget_slack(D, e)
        out.append({
            "name": name,
            "D": D,
            "e": e,
            "D_e": distortion_margin(D, e),
            "slack": slack,
            "score": budget_score(65536, slack),
            "sufficient": slack > 0 and budget_score(65536, slack) >= 10,
        })
    return out
