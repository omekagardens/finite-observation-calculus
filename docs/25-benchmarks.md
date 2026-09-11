# 25 — Benchmarks, projections, and next steps

A reproducible, exact benchmark suite for the certified regime architecture
(`scripts/benchmarks.py`). Every figure is a `Fraction`; the report is
deterministic and distributable.

## 1. The setup

- **Exact + reproducible.** No floats anywhere, so two runs — or two *machines* —
  agree bit-for-bit. That is what makes the benchmarks comparable.
- **Distributable.** Each node is independently certifiable (`docs/22` §2), the
  composition is a map-reduce over the probe union (`docs/20` §5), and
  certificates ship as JSON (`docs/14`). Nodes can run in separate processes /
  CPUs / machines; `scripts/benchmarks.py --distributed` runs the per-node fits
  across processes and checks the results agree.

## 2. B1/B2 — the math-task ladder

| task | loss linear | loss quadratic | verdict | ground truth |
|---|---:|---:|---|---|
| `add` (`a+b`) | 0 | 0 | **separated** | separated ✓ |
| `mul` (`a·b`) | 50 | 0 | **channel-limited** | channel-limited ✓ |
| `square` (`(a+b)²`) | 270 | 0 | **channel-limited** | channel-limited ✓ |
| `modp` (`(a·b) mod 5`) | 28 | 305/14 | **law-surviving** | law-surviving ✓ |

The ladder *is* the dichotomy: a linear lift suffices → separated; a quadratic
lift is needed → channel-limited; no declared lift fits → law-surviving. Sample
efficiency (fewest examples to exact fit): `add` 6/11, `mul` 6/11, `square`
—/11, `modp` —/—.

## 3. B3 — longer training (certified truncation)

Truncating to a grid each step bounds the precision; the loss falls to a
**quantization floor**:

```
grid=64, steps=8:  loss 115.7 -> 0.405   max bits 7 (bounded)   projected 4
```

**Projection:** bits `= ceil(log2(2L/D)) + ceil(log2 steps)` — `11` bits at
`1024` steps. Exact training has no such bound (`docs/18`); truncation is what
makes long sessions finite, at the cost of a loss floor set by the grid.

## 4. B4/B5 — regimes, nesting, and distribution

```
routing bits  flat 5  vs  nested 11     <- nesting ADDS routing cost
total bits    monolithic 120  vs  modular 66   <- modularity wins when margins differ
ambiguity at t=1/4: 1/4    parallel speedup (4 nodes): 4x
```

**The honest correction to the earlier intuition:** nesting does **not** reduce the
bit budget — every hard split must be resolved wherever it lives, and a tree adds
routers (`Σ >= max`). The bit saving comes from **modularity** (each leaf pays its
own margin: 66 vs 120). What nesting *does* buy is **distribution** and
**incremental growth**: independent subtrees, and adding a leaf re-certifies one
path. (A real distributed run agrees exactly but is slower on tiny nodes — process
overhead dominates; the `4x` is the ideal projection.)

## 5. B6 — corrective localization

```
2-body feature -> blame ['pairs']   1-body -> ['local']
edge blame (reads Z): ['overlapping']   correction accepted (invisible 9 -> 8)
```

## 6. Projections (order-of-magnitude, with caveats)

- **Bits vs steps:** `log2(L/D) + log2 k` — logarithmic, not `3^k`.
- **Bits vs regimes:** routing `log2(R·L/D)`; total = routing + `Σ` leaf precision.
- **Modularity:** saves `Σ p·bits(m_r)` vs `P·bits(min m_r)`; wins iff margins are
  heterogeneous.
- **Inference floor:** `bits × active_params` for a declared margin — the
  right-sizing claim.

**Caveats:** projections depend on `L` (the weight→law Lipschitz factor), the
margin profile, and the task's identifiability; all benchmarks are on **toy exact
models**, so they project the **certified composition layer**, not LM quality. A
full LM still trains with floats.

## 7. What the numbers actually say

1. **The dichotomy is real and measurable** on exact tasks (B1/B2).
2. **Long training is feasible only certified** — bounded bits, log-in-steps (B3).
3. **Modularity, not nesting, is the bit lever** (B4) — a correction to the
   starting intuition, produced by building it.
4. **Distribution is the nesting payoff** — independent nodes, map-reduce,
   bit-identical across machines.
5. **Corrections localize** (B6) — the bound that makes continual growth cheap.

## 8. Next steps

- **Real math oracle**: run the bootstrap (`docs/24`) against a math-capable local
  model (`qwen2.5-coder:3b`, `deepseek-r1:8b`) to seed regimes from real math.
- **Richer node classes**: the ladder uses a quadratic lift; add higher-degree and
  rational-function lifts, and re-run B1/B2.
- **Distribution for real**: shard nodes across processes with the JSON
  certificates (`docs/14`) as the transport, and measure wall-clock at scale.
- **Hierarchical router**: build the tree and confirm B4's prediction (nesting
  adds bits) on a real margin profile.

## 9. Status

Implemented as `foc.mathbench` (B1/B2), `foc.longsession` (B3), `foc.nested`
(B4/B5 + projections), and `scripts/benchmarks.py`; summary in demo section 23.

**Back to** [README](../README.md).
