# 06 — Marginal vs. conditional confidence

"Calibrated on average" does not imply "trustworthy per instance." This note makes the gap exact and gives a constructive fix.

## 1. Simultaneous coverage over a continuous domain

For $n$ Bernoulli trials with true success probability $p$ and observed count $k$, the **Clopper–Pearson** interval $[p_{\text{low}}, p_{\text{high}}]$ is defined by inclusive binomial tails:

$$p_{\text{low}} = \sup\Big\{p : \Pr(X \ge k \mid p) \le \alpha/2\Big\}, \qquad
p_{\text{high}} = \inf\Big\{p : \Pr(X \le k \mid p) \le \alpha/2\Big\} .$$

Its key property is *simultaneous*: for **every** $p \in [0,1]$,

$$\Pr\big(p_{\text{low}} \le p \le p_{\text{high}} \mid p\big) \ge 1 - \alpha .$$

The word "simultaneous" matters — the guarantee holds uniformly over the whole continuous probability domain, not at a single fixed $p$.

## 2. The gap: unconditional coverage $\not\Rightarrow$ conditional coverage

A procedure can satisfy the unconditional (marginal) guarantee while being wrong *conditionally* with probability one on a positive-probability event.

**Exact construction.** Take $n = 4$, true $p = 1/4$. Define a procedure that:

- on outcome $X = 3$, reports the *singleton* guess $\{3/4\}$,
- on every other outcome, abstains (reports "no confident answer").

Now:

- $\Pr(X = 3 \mid p=1/4) = \binom{4}{3}(1/4)^3(3/4) = 12/256 = 3/64 \approx 0.047 < 0.05$.
- **Unconditional coverage** $= 1 - 3/64 = 61/64 \approx 0.953 \ge 0.95$. ✓
- **Conditional on the singleton being reported** (i.e., on $X=3$), the guess $3/4 \ne 1/4$ is wrong with probability **one**. ✗

So a $\ge 95\%$ *unconditional*-coverage procedure can be *conditionally* useless — every confident report it ever makes is wrong. This is not an edge case in a corner; it is a positive-probability event.

## 3. What this means in practice

- **Marginal calibration is a floor, not a guarantee.** A language model that is well-calibrated *across all inputs* can still be badly calibrated within a specific sub-population, prompt template, or topic. The singleton construction shows the failure can be total *within* a stratum.
- **Abstention is the escape hatch.** The construction only attains unconditional coverage by *refusing to answer* on the events where it would be wrong. "I don't know" on a stratum is how a procedure stays honest without being conditionally right.
- **The fix is conditioning, not more averaging.** To get per-instance trustworthiness you must condition on the right covariates and verify coverage *within* them — not just improve the global average.

## 4. The honest statement

- Unconditional coverage: necessary, cheap, and checkable.
- Conditional coverage: what users actually experience, and strictly stronger.
- The two agree only when the report event carries no information about correctness — which, in the singleton example, it plainly does.

---

**Next:** [07 — Separation budgets under distortion](07-separation-and-distortion.md).
