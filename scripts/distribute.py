#!/usr/bin/env python3
"""Distribute regime nodes across processes with JSON certificates (``docs/28``).

    python3 scripts/distribute.py            # default batch
    python3 scripts/distribute.py --reps 32  # bigger batch -> visible speedup

Run as a file (not piped): the process pool re-imports ``__main__`` under spawn.
Each node is independently certifiable, so the batch shards across processes; the
results are bit-identical (exact arithmetic) and certificates are JSON.
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from foc import distributed as ds  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Distribute regime nodes across processes.")
    ap.add_argument("--reps", type=int, default=8, help="repeats of the task set")
    args = ap.parse_args()
    rep = ds.benchmark_distributed(reps=args.reps)
    print(f"jobs       : {rep['n_jobs']}")
    print(f"serial     : {rep['serial_s'] * 1e3:.1f} ms")
    if rep["parallel_s"] is None:
        print("parallel   : unavailable in this environment (nodes still independent)")
    else:
        print(f"parallel   : {rep['parallel_s'] * 1e3:.1f} ms   speedup {rep['speedup']:.2f}x")
    print(f"agreement  : {rep['agree']}  (bit-identical across processes)")
    print(f"certificate: {rep['certificate_sample']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
