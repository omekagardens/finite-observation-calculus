"""Predictive equivalence and question-relative minimal summaries."""

from fractions import Fraction

from . import linalg as la
from . import instruments as ins


def zthenx_branches(rho):
    """Return, for each Z-then-X history ``(z, s)``, the pair
    ``(weight, normalized_residual_state)``.

    The branch map is ``Q_s P_z rho P_z Q_s``, whose normalization is ``Q_s``
    independent of ``z``.
    """
    z = ins.z_instrument()
    x = ins.x_instrument()
    branches = {}
    for z_out in z:
        for x_out in x:
            Pz = z[z_out]
            Qs = x[x_out]
            m = la.mat_mul(
                la.mat_mul(Qs, la.mat_mul(la.mat_mul(Pz, rho), Pz)), Qs
            )
            t = la.trace(m)
            branches[(z_out, x_out)] = (t, ins.normalize(m) if t > 0 else None)
    return branches


def zthenx_classes(rho):
    """The coarsest partition of Z-then-X histories by residual state.

    Returns a list of ``(residual_state, [history tuples])`` groups.
    Zero-probability histories (residual ``None``) each form their own group.
    """
    branches = zthenx_branches(rho)
    groups = []
    for hist, (_t, st) in branches.items():
        if st is None:
            groups.append((None, [hist]))
            continue
        placed = False
        for g_state, g_hists in groups:
            if g_state is not None and g_state == st:
                g_hists.append(hist)
                placed = True
                break
        if not placed:
            groups.append((st, [hist]))
    return groups


def summary_loses_weights(rho=None):
    """Show that the "keep only the last X outcome" summary does not preserve
    history weights.

    At ``rho = diag(3/4, 1/4)`` the histories ``(0,+)`` and ``(1,+)`` share the
    same residual state ``Q_+`` but have different weights ``3/8`` and ``1/8``.
    Returns ``(w(0,+), w(1,+))``.
    """
    if rho is None:
        rho = [[Fraction(3, 4), Fraction(0)], [Fraction(0), Fraction(1, 4)]]
    branches = zthenx_branches(la.mat(rho))
    return branches[("0", "+")][0], branches[("1", "+")][0]
