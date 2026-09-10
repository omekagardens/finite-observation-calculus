"""Records, schedules, and the Z/X counterexample."""

from fractions import Fraction

from . import linalg as la
from . import instruments as ins


def joint_record(events, rho):
    """Execute a list of instruments left-to-right, appending outcomes to a record.

    Returns ``(probs, states)``:
      - ``probs``: dict ``{record_tuple: Fraction}`` (unnormalized branch trace),
      - ``states``: dict ``{record_tuple: matrix | None}`` (normalized residual
        state, or ``None`` for a zero-probability branch).
    """
    branches = {(): la.mat(rho)}
    for ev in events:
        new = {}
        for rec, state in branches.items():
            for outcome in ev:
                M = ev[outcome]
                out = la.mat_mul(la.mat_mul(M, state), la.transpose(M))
                new[rec + (outcome,)] = out
        branches = new
    probs = {rec: la.trace(m) for rec, m in branches.items()}
    states = {
        rec: (ins.normalize(m) if la.trace(m) > 0 else None)
        for rec, m in branches.items()
    }
    return probs, states


def zx_counterexample(rho=None):
    """The two schedules Z-then-X and X-then-Z, with retained records.

    Records are canonicalized to ``(z_outcome, x_outcome)`` — by event identity,
    not execution order — so the two schedules are directly comparable.
    """
    if rho is None:
        rho = ins.rho_0()
    z = ins.z_instrument()
    x = ins.x_instrument()
    p_zx, _ = joint_record([z, x], rho)       # keys already (z, x)
    p_xz_raw, _ = joint_record([x, z], rho)   # keys are (x, z)
    p_xz = {(z_out, x_out): p for (x_out, z_out), p in p_xz_raw.items()}
    return p_zx, p_xz


def record_discarded_equal(z, x, rho):
    """True iff Z-then-X and X-then-Z send ``rho`` to the same record-discarded
    state (the behavioral / output-only comparison)."""
    zx = ins.channel(x, ins.channel(z, rho))
    xz = ins.channel(z, ins.channel(x, rho))
    return zx == xz


def recorded_equal(z, x, rho):
    """True iff the two schedules produce identical joint record laws AND
    identical per-record residual states (the strongest recorded comparison)."""
    p_zx, s_zx = joint_record([z, x], rho)
    p_xz_raw, s_xz_raw = joint_record([x, z], rho)
    p_xz = {(z_out, x_out): p for (x_out, z_out), p in p_xz_raw.items()}
    s_xz = {(z_out, x_out): m for (x_out, z_out), m in s_xz_raw.items()}
    if set(p_zx) != set(p_xz) or any(p_zx[r] != p_xz[r] for r in p_zx):
        return False
    for r in p_zx:
        if (s_zx[r] is None) != (s_xz[r] is None):
            return False
        if s_zx[r] is not None and s_zx[r] != s_xz[r]:
            return False
    return True
