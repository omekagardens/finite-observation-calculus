"""Distributing regime nodes across processes with JSON certificates (``docs/28``).

Each node is independently certifiable (``docs/22`` §2), so nodes shard cleanly
across processes / CPUs / machines, and exact arithmetic makes the results
bit-identical. Certificates are JSON (``docs/14`` style) -- the transport between
processes. ``benchmark_distributed`` shards a batch of node jobs and reports
serial vs parallel wall-clock (and honest overhead on tiny nodes).
"""

import json
import time
from concurrent.futures import ProcessPoolExecutor

from . import mathbench as mb


def node_certificate(task):
    """A node's exact result as a JSON-serializable certificate."""
    losses = {lift: str(mb.fit(task, lift)["loss"]) for lift in mb.LIFT_ORDER}
    return {
        "task": task,
        "min_lift": mb.min_lift(task) or "none",
        "verdict": mb.verdict(task),
        "losses": losses,
    }


def _job(task):
    return node_certificate(task)


def run_serial(tasks):
    return [_job(t) for t in tasks]


def run_parallel(tasks, workers=None):
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(_job, tasks))


def benchmark_distributed(reps=8):
    """Shard ``reps * len(TASKS)`` node jobs; serial vs parallel wall-clock + agreement."""
    tasks = [t for _ in range(reps) for t in mb.TASKS]
    t0 = time.perf_counter()
    serial = run_serial(tasks)
    t_serial = time.perf_counter() - t0
    parallel = None
    t_parallel = None
    agree = None
    try:
        t0 = time.perf_counter()
        parallel = run_parallel(tasks)
        t_parallel = time.perf_counter() - t0
        agree = serial == parallel
    except Exception:  # noqa: BLE001 - process pools are environment-dependent
        pass
    return {
        "n_jobs": len(tasks),
        "serial_s": t_serial,
        "parallel_s": t_parallel,
        "speedup": (t_serial / t_parallel) if t_parallel else None,
        "agree": agree,
        "certificate_sample": json.dumps(serial[0]) if serial else None,
    }
