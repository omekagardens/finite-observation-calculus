#!/usr/bin/env python3
"""Bootstrap certified regime nodes from a local LLM (``docs/24``).

Offline (deterministic mock):
    python3 scripts/bootstrap_llm.py

Against a local LLM:
    ollama serve                                   # once, in another shell
    python3 scripts/bootstrap_llm.py --endpoint http://localhost:11434 --model llama3.2:3b
    python3 scripts/bootstrap_llm.py --backend openai --endpoint http://localhost:1234 --model microsoft/phi-4

The LLM supplies declared regimes and labeled examples; the calculus trains and
certifies each node exactly (all numbers are ``Fraction``).
"""

import argparse
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src"))

from foc import bootstrap as bs  # noqa: E402


def main():
    ap = argparse.ArgumentParser(description="Bootstrap certified regime nodes from a local LLM.")
    ap.add_argument("--endpoint", default=None,
                    help="local LLM base URL; omit for the offline mock")
    ap.add_argument("--backend", default="ollama", choices=["ollama", "openai"])
    ap.add_argument("--model", default="llama3.2:3b")
    ap.add_argument("--task", default="predict a rational target from two rational inputs")
    ap.add_argument("--regimes", type=int, default=2)
    ap.add_argument("--examples", type=int, default=6)
    args = ap.parse_args()

    if args.endpoint is None:
        llm, where = bs.MockLLM(), "MockLLM (offline, deterministic)"
    else:
        llm, where = bs.LocalLLM(args.endpoint, args.model, args.backend), \
            f"{args.backend} {args.endpoint} ({args.model})"

    print(f"task   : {args.task}")
    print(f"oracle : {where}")
    try:
        report = bs.bootstrap(args.task, llm, args.regimes, args.examples)
    except Exception as exc:  # noqa: BLE001 - the oracle is untrusted
        print(f"bootstrap failed: {type(exc).__name__}: {exc}")
        return 1

    print(f"regimes: {report['regimes']}")
    print(f"{'node':14} {'c0 (x1)':>10} {'c1 (x2)':>10} {'c2 (x1x2)':>11} {'loss':>8}  product?")
    for n in report["nodes"]:
        c = n["coefficients"]
        print(f"{n['regime']:14} {str(c[0]):>10} {str(c[1]):>10} {str(c[2]):>11} "
              f"{str(n['loss']):>8}  {n['uses_product']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
