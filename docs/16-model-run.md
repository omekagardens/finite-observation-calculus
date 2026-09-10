# 16 — A controlled model run of the probe-audit protocol

`docs/13` gives the protocol. This note runs it end-to-end, exactly, on a **model
with a known feature encoding**, so the verdicts can be scored against ground
truth.

## 1. Why a controlled model

A run on a model of *unknown* encoding can only report, not *validate*. The
protocol's payload is a negative-result claim, so validating it needs a model whose
encoding we control: three features — one **linear**, one **joint-only**, one
**absent**.

## 2. The model

A **pairwise-correlation head**: an input triple $(a, b, c)$ prepares a two-site
state

$$\rho(a,b,c) = \tfrac14\big[\, I \otimes I \;+\; a\,Z \otimes I \;+\; c\,Z \otimes Z \,\big],$$

with $b$ ignored. All entries are exact rationals, and $\rho$ is a valid state for
$|a| + |c| \le 1$. Ground truth:

- $a$ is encoded in site A's marginal → a one-body (**linear**) feature;
- $c$ is encoded only in the A–B correlation → a two-body (**joint**) feature;
- $b$ is not encoded.

## 3. The run

Probe families: `local` (one-body) and `joint` (one-body + two-body).

| feature | separation local / joint | verdict | ground truth |
|---|---|---|---|
| marginal $a$ | $1 / 1$ | separated | separated ✓ |
| correlation $c$ | $0 / 1$ | channel-limited | channel-limited ✓ |
| null $b$ | $0 / 0$ | law-surviving | law-surviving ✓ |

All three verdicts match ground truth. Note the middle row: $a$ and $c$ are the
same *kind* of number, but the audit separates them by *which probe family sees
them* — that is the whole point of the protocol.

## 4. The margin effect

At margin $t = \tfrac12$ the verdicts are as above; at $t = 2$ — above every
separation (all $\le 1$) — **all** features fall to "law-surviving to 2". This is
the certification-radius effect (`docs/11` §4) on a concrete model.

## 5. What it establishes, and its limits

- **Establishes:** the protocol classifies a model's features correctly, against
  ground truth, with a runnable decision procedure.
- **Limits:** the model is *controlled* (constructed, not trained) and small; the
  exact rational setting keeps every repository invariant. A run on a **trained**
  model cannot be scored this way — it can only *report*, and it needs a
  float/GPU stack outside this package (design B).

## 6. Status

Exact, reproducible, zero-dependency; validates the protocol on known ground truth.
Implemented as `foc.modelrun` (`correlation_head`, `model_run`) and run in demo
section 14.

**Back to** [README](../README.md).
