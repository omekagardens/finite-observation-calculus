# 08 — The ambiguity dichotomy (general form)

This note states the general result that `docs/03`, `04`, `05`, `06`, and `07` are
instances of. It is a *framework theorem*: the clauses below are each provable, and
the content is their assembly into one calculus of *what is observable*.

## 0. The result in one line

> Fix a declared observation class. Every two worlds are either **already
> separated**, **channel-limited** (separated by a richer admissible observation),
> or **law-surviving** (identical complete observable law). Law-surviving
> ambiguity is exactly the *gauge orbit* of the law map; it is the only
> unresolvable kind; and sufficient distortion converts channel-limited pairs
> into law-surviving ones.

## 1. Worlds, experiments, and the law map

- Let $\Theta$ be a set of **worlds** (full descriptions of the underlying
  structure), and $\mathcal X$ a set of **experiments** (preparation + instrument
  + record-retaining protocol).
- Experiment $e$ has outcomes $\Omega_e$, and world $\theta$ induces a law
  $P_\theta^e \in \Delta(\Omega_e)$.
- For a class $E \subseteq \mathcal X$ define the **observable law map**

$$L_E : \Theta \to \prod_{e \in E} \Delta(\Omega_e), \qquad
L_E(\theta) = \big(P_\theta^e\big)_{e \in E}.$$

$L_E(\theta)$ is the *complete observable law* of $\theta$ within $E$; it is the
only thing that is observable. Write $\theta_1 \approx_E \theta_2$ iff
$L_E(\theta_1) = L_E(\theta_2)$.

**Hypothesis (point separation).** $E^\*$ is *complete*: $L_{E^\*}$ separates
worlds that any admissible observation can separate (§4 makes this precise as
injectivity modulo gauge).

## 2. Records refine: the equivalence hierarchy

Enriching the experiment class refines indistinguishability:
$E \subseteq E' \Rightarrow {\approx_{E'}} \subseteq {\approx_E}$.

Retaining the **record** (every intermediate outcome and residual state, not just
the final output) is exactly such an enrichment. Hence the chain

$$\underbrace{\approx_{\text{output}}}_{\text{behavioral}}
\;\supseteq\;
\underbrace{\approx_{\text{record}}}_{\text{mechanistic}}$$

is *strict*. Witnesses (`schedule.py`): the Z/X schedules share the
record-discarded channel yet differ as recorded instruments; and from $I/2$ they
even share the complete joint *distribution* while differing in residual
operators. Discarding a record certifies an equality that the retained record
refutes.

## 3. The dichotomy theorem

Fix a declared class $E$ and its completion $E^\* \supseteq E$. For any
$\theta_1, \theta_2$, exactly one case holds:

1. **Separated** — $L_E(\theta_1) \neq L_E(\theta_2)$: some experiment in $E$
   already tells them apart.
2. **Channel-limited** — $L_E(\theta_1) = L_E(\theta_2)$ but
   $L_{E^\*}(\theta_1) \neq L_{E^\*}(\theta_2)$: a *richer admissible
   observation* separates them. Fixed by asking a better question.
3. **Law-surviving** — $L_{E^\*}(\theta_1) = L_{E^\*}(\theta_2)$: no admissible
   observation separates them. The distinction is not in the observable at all.

*Proof.* Immediate from the definitions (the three cases are the exhaustive
possibilities for the pair of booleans
$\big[L_E(\theta_1)\!=\!L_E(\theta_2)\big]$, $\big[L_{E^\*}(\theta_1)\!=\!L_{E^\*}(\theta_2)\big]$).
The substance is that cases 2 and 3 have the structural readings of §4–§6. $\square$

## 4. Law-surviving ambiguity *is* gauge symmetry

Let a group $G$ act on $\Theta$. The law map is **$G$-invariant** when
$L_{E^\*}(g\cdot\theta) = L_{E^\*}(\theta)$ for all $g \in G$.

**Proposition.** If $L_{E^\*}$ is $G$-invariant then the orbit $G\cdot\theta$ lies
inside the fiber $L_{E^\*}^{-1}(L_{E^\*}(\theta))$. If moreover $L_{E^\*}$ is
injective on the quotient $\Theta/G$ (a *gauge fixing*), the inclusion is an
equality:

$$\theta_2 \approx_{E^\*} \theta_1 \iff \theta_2 \in G\cdot\theta_1.$$

*Proof.* Invariance gives orbit $\subseteq$ fiber. Injectivity on $\Theta/G$ gives
fiber $\subseteq$ orbit. $\square$

So **law-surviving ambiguity is precisely the gauge redundancy of the
observable law.** This sharpens the taxonomy into two sub-kinds by the fiber's
local dimension:

- **Discrete (symmetry) ambiguity** — $\ker DL_{E^\*}(\theta) = 0$ yet $L$ is
  globally non-injective: an isolated orbit, e.g. a finite group action.
- **Continuous (degenerate) ambiguity** — $\ker DL_{E^\*}(\theta) \neq 0$: a
  positive-dimensional family of worlds sharing the law.

**Local identifiability.** For open $\Theta \subseteq \mathbb R^n$ and smooth
$L$, the *infinitesimal* law-surviving directions at $\theta$ are
$\ker DL_{E^\*}(\theta)$, and the identifiable functionals are exactly those
$f$ whose gradient is orthogonal to it (equivalently, $\nabla f \in
\operatorname{row} DL_{E^\*}(\theta)$). The number of identifiable directions is
$\operatorname{rank} DL_{E^\*}(\theta)$.

*Instance.* The geometry family $\theta=(\eta,\delta)$ has
$L(\eta,\delta) = (\eta+\delta,\ \eta\delta)$ (the elementary symmetric
functions). $L$ is invariant under the $\mathbb Z/2$ swap $\eta
\leftrightarrow \delta$, and injective on unordered pairs, so the fiber is
the orbit — a **discrete** ambiguity. The Jacobian has rank $2$ at the flat
point $(0,1)$, confirming the absence of a continuous degeneracy: no amount of
data separates the swap, and no local perturbation can either.

## 5. Sufficiency is question-relative; nothing proper is universal

A summary $T : \Theta \to S$ is **$E$-sufficient** iff equal summaries imply
equal law: $T(\theta_1) = T(\theta_2) \Rightarrow \theta_1 \approx_E \theta_2$.

**Proposition.**
1. The coarsest $E$-sufficient summary is $L_E$ itself, up to bijection
   (a sufficient $T$ must factor as $T = \varphi \circ L_E$ with $\varphi$
   injective on the image).
2. The map $E \mapsto$ (coarsest $E$-sufficient summary) is strictly
   order-reversing: the finer the experiment class, the finer the summary.
3. Consequently **no proper (lossy) summary is sufficient for every $E$**. The
   complete law $L_{E^\*}$ is the unique $E$-universal sufficient summary, and it
   is not a compression.

*Proof.* (1) $T$ sufficient $\Rightarrow$ $T$ constant on $\approx_E$-classes
$\Rightarrow$ $T$ factors through the class map $= L_E$ up to bijection. Minimality
excludes any proper coarsening. (2),(3) If $E \subset E'$ there are
$\theta_1,\theta_2$ with $L_E$ equal but $L_{E'}$ unequal; any summary that merges
them is $E'$-insufficient. $\square$

*Instance.* `summaries.py`: "keep only the last X outcome" is the coarsest summary
sufficient for any future qubit measurement, yet it discards the Z-history
weights ($3/8$ vs $1/8$) that a question about the full record requires.

## 6. Quantitative: the separation budget, and distortion at rate two

Let $d(\theta_1,\theta_2)$ be the separation of the restricted laws under $E$
(e.g. total variation). Define the **budget** $B(\theta_1,\theta_2;E,\varepsilon)$
= the number of independent experiments needed to distinguish them with error
$\le \varepsilon$.

**Proposition.**
1. $B = \infty \iff L_E(\theta_1) = L_E(\theta_2)$. Law-surviving is exactly
   *infinite budget*; channel-limited pairs have finite budget.
2. For a channel-limited pair, $B \asymp \dfrac{\log(1/\varepsilon)}{d^2}$
   (Chernoff–Stein / Le Cam).
3. Under per-experiment distortion $\lVert P_\theta - \tilde P_\theta\rVert_\infty
   \le e$, the effective separation obeys
   $d \mapsto \max(d - 2e,\,0)$ (the triangle inequality), so the **effective
   budget** blows up and the pair becomes indistinguishable once $2e \ge d$.

So the dichotomy is not merely binary: it has a **robustness margin**, and
sufficient distortion *converts a channel-limited ambiguity into a law-surviving
one*.

*Instance.* `confidence.py`: the census row `uniform/contact` has ideal
$D = 3/64 > 0$ but distorted $D_e = \max(D - 2e,0) = 0$ at $e = D/2$ — a
resolvable pair driven to collision by distortion. The three failure reasons in
`docs/07` are the three ways $B$ can fail to certify: genuine collision
($d=0$), budget failure ($B$ finite but too large), grid failure ($d$ below
resolution).

## 7. The earlier results are instances

| Result | Reading in the dichotomy |
|---|---|
| `03` two-kinds taxonomy | The dichotomy itself; §4 is the gauge reading of kind 1 |
| `04` minimal summaries | §5: $L_E$ is the coarsest $E$-sufficient summary; question-relativity |
| `05` forgetting vs recombination | §2: retaining the record strictly refines $\approx$ |
| `06` marginal vs conditional | §5 in a stratum: the report event is not $E$-sufficient |
| `07` separation budgets | §6: finite vs infinite budget; distortion at rate two |
| Z/X and $I/2$ counterexamples | Strictness witnesses for §2 |

## 8. Applications: language models and inference systems

1. **A decision procedure for negative results (probing / interpretability).**
   When a probe fails to recover a feature, §3 says there are two distinct
   explanations. Compute, over a declared probe family $E$, whether the feature
   is separated by $E$; if not, test whether it is separated by the completion
   $E^\*$ (richer probes, retained activations). **Channel-limited ⇒ design a
   better probe; law-surviving ⇒ stop — the information is not in the record.**
   This prevents unbounded effort chasing an absent distinction.
2. **Behavioral evals cannot certify internal equivalence (§2).** Output-only
   agreement is $E$-agreement for a class that discards records; the generic case
   is channel-limited difference in the retained computation. Mechanistic
   claims require retaining and comparing intermediate records (activations,
   checkpoints), not outputs.
3. **Compression, distillation, KV-cache (§5).** There is no universal summary;
   you must *declare the downstream question family* first. The coarsest safe
   compression is $L_E$ for that family, and it is task-specific.
4. **Calibration and conformal prediction (§5).** Marginal validity is
   $E$-sufficiency over all inputs; conditional validity requires the summary to
   be sufficient *within each stratum*. The gap is exactly the insufficiency of
   the report event.
5. **Distribution shift and robustness (§6).** At rate two, shift erodes the
   margin and can render two models *literally* indistinguishable. A
   separability-margin diagnostic predicts when this collapse occurs.
6. **Provenance and identifiability (§4).** Training procedures related by a
   symmetry of the observable law are mutually unrecoverable from outputs;
   recovering them requires the retained record (RNG state, data order,
   checkpoints) — a gauge-fixing choice, not a measurement.

## 9. Status and novelty

Every clause is individually known mathematics: the equivalence/record hierarchy
is operational quantum mechanics; "$L$ equal $\iff$ indistinguishable" is
identifiability (Koopmans–Reiersøl); "law-surviving $=$ gauge orbit" is the
standard reading of gauge redundancy; the minimal sufficient statistic is the
Fisher–Neyman factorisation; the budget is Le Cam/Chernoff; and
"distortion closes the gap" is the triangle inequality. **The contribution is the
assembly** — one exact calculus that spans quantum, classical, and statistical
inference, with the two sharp readings this note adds: **law-surviving ambiguity
= gauge orbit**, split into discrete vs continuous, and **sufficient distortion
converts resolvable pairs into irreducible ones**. As with the rest of the
repository, the value is a precise synthesis with exact witnesses, not a new
theorem.

## 10. Where a genuinely new theorem could live

- A structural criterion for when $L_{E^\*}$ factors through a gauge group
  (an analogue of a commutant for arbitrary observable algebras).
- A tight, non-asymptotic rate for the distortion-induced collapse (§6.3), with a
  matching lower bound.
- A completeness theorem: the three cases are the *only* ones for a declared
  family, with an effective procedure to decide between them from finitely many
  experiments.

**Back to** [README](../README.md).
