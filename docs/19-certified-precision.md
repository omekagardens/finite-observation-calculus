# 19 — Certified precision: the correction rate pays for the bit growth

`docs/18` left exact training with an unbounded cost — denominators growing ~×3
in bits per step. This note shows the calculus's **own** error structure bounds
that growth: the precision worth keeping is set by the observable margin, and the
**rate-two** erosion is the exchange rate between discarded bits and lost
separation.

## 1. The ledger

- **Cost:** exact descent tracks precision no verdict needs.
- **Supply:** an observation distortion $e$ erodes a separation at **rate two**
  (`docs/09` §3, $D \mapsto \max(D-2e,0)$); anything below the **margin** is in
  the annihilator (`docs/08` §4) and is not certifiable (`docs/11`).

## 2. The identification

> The annihilator / margin is exactly the set of bits you may discard without
> changing any certifiable verdict; rate two is the price of the bits you keep
> discarding.

Round every weight to a grid of quantum $1/n$. Then:

- denominators are **bounded** by $\log_2 n$ bits — independent of the step count;
- any separation changes by at most $2e$ (the triangle inequality — the rate-two
  bound), where $e$ is the induced output distortion;
- so the verdict "separated by $\ge t$" survives whenever $2e < D - t$.

The one-sided decidability theorem is the **license**: below the margin there is
no certifiable fact, so discarding bits is free.

## 3. The demonstration

Train the rational transformer two exact steps (`docs/18`), then truncate
(`foc.truncate.certified_truncation`). Verdict: the two probe inputs are separated
by at least $t = D/2$.

| exact | grid | denom bits | separation | erosion | rate-two | verdict |
|---|---:|---:|---:|---:|---:|---|
| 5839 bits | 16 | **5** | 0.4792 | $2.2\times10^{-2}$ | ✓ | ✓ |
| | 32 | 6 | 0.5319 | $-3.1\times10^{-2}$ | ✓ | ✓ |
| | 64 | 7 | 0.4966 | $4.4\times10^{-3}$ | ✓ | ✓ |
| | 256 | 9 | 0.4991 | $1.9\times10^{-3}$ | ✓ | ✓ |

The exact weights need **5839 bits**; truncating to a grid of **16** needs **5
bits** — a ~1000× reduction — and the separation verdict (true value $\approx
0.501$, margin $0.251$) is preserved. On every grid the erosion obeys the
rate-two bound. (Very coarse grids zero out the attention scores and degenerate
the model; that is the collapse, reported rather than silent.)

## 4. The bound

For a step budget $k$ and model Lipschitz factor $L$ (weight $\to$ law), keeping
the accumulated distortion below the margin needs quantum $q < D/(2Lk)$:

$$\text{bits} \;=\; \log_2\!\frac{2L}{D} + \log_2 k .$$

Exact growth ($3^k$) becomes **logarithmic** ($O(\log k)$). That is the match: a
*constant* correction rate (`2L`) bounds the bit growth.

## 5. Caveats

- **$L$ matters.** A large weight$\to$law Lipschitz factor buys few bits; the bound
  is only as good as $L$.
- **Truncation perturbs the optimization**, not just the verdict; rate two bounds
  the *observation* error, while accumulation depends on the dynamics' stability.
- **It is no longer exact** — it is a *certified fixed-point* scheme. But
  "certified" is this project's currency, and it is more than float training gives:
  the precision is set by the observable margin, and the error is bounded.

## 6. Status

Implemented as `foc.truncate` (`truncate`, `denominator_bits`, `separation`,
`output_distortion`, `certified_truncation`) and run in demo section 17.

**Back to** [README](../README.md).
