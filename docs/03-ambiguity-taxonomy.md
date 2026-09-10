# 03 — The two-kinds-of-ambiguity taxonomy

This is the centerpiece. There are **two fundamentally different reasons** two hypotheses can be observationally indistinguishable, and conflating them is the single most common error in "can we recover the structure from the data?" arguments.

## 1. The setup

A supplied geometry with metric

$$ds^2 = s\,(1 + \eta u v)\,du\,dv ,$$

volume density $s(1+\eta uv)/2$, and sampling density $1 + \delta uv$. The **geometric target** is

$$\tau = \frac{16 + \eta}{16\,(4 + \eta)} ,$$

so $\tau = 1/4$ for the "flat" case ($\eta = 0$) and $\tau = 17/80$ for the "conformal" case ($\eta = 1$). The nuisance is the sampling coefficient $\delta$.

For a rectangle anchored at the origin with area $z$, the integrated mass is

$$M_z(\delta) = \frac{s}{2}\left[ z + \frac{(\eta + \delta) z^2}{4} + \frac{\eta\,\delta\, z^3}{9} \right] .$$

The normalized single-mark probability is $q_1 = M_{I_1}/M_Q$ where $Q=(0,1)^2$ has area $1$ and $I_1=(0,1/2)^2$ has area $1/4$. A **second mark** $I_2 = (0,3/4)\times(0,1/2)$ of area $3/8$ gives $q_2 = M_{I_2}/M_Q$.

The full **point law** is proportional to

$$1 + (\eta + \delta)\,uv + \eta\,\delta\,u^2 v^2 .$$

Two worlds have the *identical* point law precisely when both $(\eta+\delta)$ and $\eta\,\delta$ agree.

## 2. Kind 1 — the factorization obstruction

Consider **flat** $\eta=0,\delta=1$ versus **conformal** $\eta=1,\delta=0$:

- both give $\eta + \delta = 1$ and $\eta\,\delta = 0$,
- so both have the **identical** point law $(4/5)(1 + uv)$,
- both give the same mark probability $q_1 = 17/80$,
- **yet their targets differ**: $1/4$ versus $17/80$, a gap of exactly $3/80$.

This pair is a *witness*: two genuinely different underlying structures that generate the **identical complete observable law**. An observer with unlimited i.i.d. samples from the full point law cannot separate them, **even in principle**. The information that distinguishes them lives in the *factorization* (geometry $\eta$ versus sampling density $\delta$), which is not present in the observable at all.

> **More records of the same law cannot separate this pair.** This is an exact information obstruction, not a sampling limitation.

## 3. Kind 2 — a limited channel

Now consider the membership probability $q_1 = 1/5$. Solving for $\delta$ under each geometry gives

- flat: $\delta = 16/11$,
- conformal: $\delta = 45/158$.

These two worlds share the *single-mark* probability $q_1 = 1/5$ — a membership-only collision. But their **point laws differ**: the flat world has no $u^2v^2$ term, while the conformal world has coefficient $45/158$.

The difference is *present in the point law* but invisible to the single-mark channel. A richer channel — the second mark, which sees the $u^2v^2$ coefficient — **splits** the collision.

> This is a *channel-limited* ambiguity: fixed by asking a better question, not by collecting more data from the same question.

## 4. The taxonomy, stated generally

| | Kind 1: factorization obstruction | Kind 2: channel-limited |
|---|---|---|
| Same single-channel law? | yes | yes |
| Same **complete** observable law? | **yes** | no |
| Fixable by more data? | **no** | no |
| Fixable by a richer channel? | **no** | **yes** |
| Where the information lives | nowhere observable | in the discarded higher-order terms |

## 5. The practical consequence

When an experiment, probe, or interpretability method fails to find a hypothesized structure, ask **which kind** of failure it is:

1. **Channel-limited.** A richer observable exists that would reveal the difference. The right move is to design it.
2. **Factorization obstruction.** No observable over the accessible record can reveal the difference, because the two worlds are observationally identical *in full*. The right move is to recognize that the question is not empirically decidable from this record — no amount of data or cleverness closes the gap.

Conflating the two is the failure mode: treating a factorization obstruction as if it were a measurement problem leads to unbounded effort chasing information that is not there to be found.

---

**Next:** [04 — Question-relative minimal summaries](04-minimal-summaries.md).
