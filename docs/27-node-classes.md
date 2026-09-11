# 27 — Richer node classes

`docs/25` fit the math ladder with two lifts (linear, quadratic). This note adds
higher-degree and rational lifts and re-runs **B1/B2**.

## 1. The lifts

| lift | features | degree |
|---|---:|---|
| `linear` | 3 | 1 |
| `quadratic` | 6 | 2 |
| `cubic` | 10 | 3 |
| `quartic` | 15 | 4 |
| `rational` | 8 | poly + `1/(b+4)`, `a/(b+4)` |

The rational lift keeps only **two** rational features: `b/(b+4) = 1 − 4/(b+4)`
and `ab/(b+4) = a − 4a/(b+4)` are linear combinations of the other columns, so
including them makes the normal equations **singular** — a real degeneracy the
build exposed. The grid is 7 points/variable so a degree-≤4 polynomial cannot
interpolate the rational features (otherwise they, too, are dependent).

## 2. B1/B2 re-run

`foc.mathbench.min_lift` reports the *coarsest* lift that fits exactly:

| task | target | min lift | verdict |
|---|---|---|---|
| `add` | `a+b` | linear | separated |
| `mul` | `a·b` | quadratic | channel-limited |
| `square` | `(a+b)²` | quadratic | channel-limited |
| `cube` | `a³` | **cubic** | channel-limited |
| `quart` | `a²b²` | **quartic** | channel-limited |
| `div` | `a/(b+4)` | **rational** | channel-limited |
| `divprod` | `ab/(b+4)` | **rational** | channel-limited |
| `modp` | `(a·b) mod 5` | **none** | law-surviving |

Every `min_lift` matches ground truth. `min_lift` is the **symmetry degree** of
`docs/12` made operational: it says *how far* a task is from linear, not merely
that it is not linear.

## 3. What it shows

- The dichotomy survives richer families: linear → separated, any higher lift →
  channel-limited, no lift → law-surviving.
- **Overfitting floor**: `modp` is law-surviving only because the declared family
  is smaller than the grid (25 values); a family with ≥ grid-many independent
  features would interpolate it. Law-surviving is *relative to the declared
  family*, exactly as the calculus insists.

## 4. Status

Implemented in `foc.mathbench` (five lifts, eight tasks, `min_lift`) and reported
in demo section 24.

**Back to** [README](../README.md).
