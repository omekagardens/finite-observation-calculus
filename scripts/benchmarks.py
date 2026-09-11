#!/usr/bin/env python3
"""Reproducible benchmarks for the certified regime architecture (``docs/25``).

    python3 scripts/benchmarks.py               # B1-B6, serial
    python3 scripts/benchmarks.py --distributed # also run the per-node fits across processes

All figures are exact (``Fraction``); the report is deterministic.
"""

import argparse
import os
import sys
import time

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from foc import mathbench, nested, longsession, corrective  # noqa: E402


def b12_math_ladder():
    print("B1/B2  math-task ladder (exact fit + sample efficiency)")
    print(f"  {'task':8} {'loss_lin':>10} {'loss_quad':>10} {'verdict':16} {'expected':16} lin/quad samples")
    for r in mathbench.benchmark_tasks():
        ok = "ok" if r["verdict"] == r["expected"] else "MISMATCH"
        print(f"  {r['task']:8} {str(r['loss_linear']):>10} {str(r['loss_quadratic']):>10} "
              f"{r['verdict']:16} {r['expected']:16} {r['samples_linear']}/{r['samples_quadratic']}  {ok}")


def b3_long_session(steps=8, grid=64):
    rep = longsession.benchmark_long_session(steps=steps, grid=grid)
    print(f"B3  long session (certified truncation, grid={grid}, steps={steps})")
    print(f"  loss {float(rep['loss_first']):.4g} -> {float(rep['loss_last']):.4g}"
          f"   max bits {rep['max_bits']} (bounded)   projected {rep['projected_bits']}")


def b45_regimes():
    rep = nested.benchmark_regimes()
    print("B4/B5  regimes: flat vs nested, modular vs monolithic, distribution")
    print(f"  routing bits  flat {rep['flat_router_bits']}  vs  nested {rep['nested_router_bits']}"
          f"   (nesting adds routing cost)")
    print(f"  total bits    monolithic {rep['monolithic_bits']}  vs  modular {rep['modular_bits']}"
          f"   (modularity wins when margins differ)")
    print(f"  routing ambiguity at t=1/4: {rep['ambiguity_at_1_4']}"
          f"   parallel speedup (4 nodes): {rep['parallel_speedup']}x"
          f"   bits at 1024 steps: {rep['bits_at_1024_steps']}")


def b6_corrective():
    rep = corrective.corrective_report()
    print("B6  corrective localization")
    print(f"  2-body feature -> blame {rep['localize_2body']};  1-body -> {rep['localize_1body']}")
    print(f"  edge blame (reads Z): {rep['blame_Z']}   correction accepted: {rep['correction']['accepted']}"
          f"  (invisible {rep['correction']['annihilator_before']} -> {rep['correction']['annihilator_after']})")


def distributed_demo(tasks=("add", "mul", "square", "modp")):
    """Run the per-task fits across processes -- the map-reduce the architecture allows."""
    print("DISTRIBUTED  per-node fits across processes (map-reduce over independent nodes)")
    t0 = time.perf_counter()
    serial = [mathbench.verdict(t) for t in tasks]
    t_serial = time.perf_counter() - t0
    try:
        from concurrent.futures import ProcessPoolExecutor
        t0 = time.perf_counter()
        with ProcessPoolExecutor() as ex:
            par = list(ex.map(mathbench.verdict, tasks))
        t_par = time.perf_counter() - t0
        print(f"  serial {t_serial * 1e3:.1f} ms -> parallel {t_par * 1e3:.1f} ms"
              f"   (results agree: {serial == par})")
    except Exception as exc:  # noqa: BLE001 - process pools are environment-dependent
        print(f"  process pool unavailable ({type(exc).__name__}); nodes are still independent "
              f"(results: {serial})")


def main():
    ap = argparse.ArgumentParser(description="Benchmark the certified regime architecture.")
    ap.add_argument("--distributed", action="store_true", help="also run per-node fits across processes")
    args = ap.parse_args()
    b12_math_ladder()
    print()
    b3_long_session()
    print()
    b45_regimes()
    print()
    b6_corrective()
    if args.distributed:
        print()
        distributed_demo()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
