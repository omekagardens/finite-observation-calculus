# 08 — The ambiguity dichotomy (general form)

This note states the general result that `docs/03`, `04`, `05`, `06`, and `07` are
instances of. It is a *framework theorem*: the clauses below are each provable, and
the content is their assembly into one calculus of *what is observable*.

## 0. The result in one line

> Fix a declared observation class. Every two worlds are either **already
> separated**, **channel-limited** (separated by a richer admissible observation),
> or **law-surviving** (identical complete observable law). Law-surviving
> ambiguity is exactly the *annihilator* of the completed effect algebra —
> physically, the invisible sector of a superselection rule; in parametric
> families, the gauge orbit of the law map. It is the only unresolvable kind, and
> sufficient distortion converts channel-limited pairs into law-surviving ones.

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

## 4. Law-surviving ambiguity is the annihilator — superselection and gauge

The fiber characterization of §2–3 has a concrete, computable form. Let $S$ be
the real vector space of admissible *state differences* (e.g. traceless Hermitian
operators, or the real symmetric subspace), and let $M_E \subseteq S^*$ be the
span of the accessible effects viewed as linear functionals
$\rho \mapsto \operatorname{Tr}(\rho E)$. Write $A_E := M_E^{\perp} \cap S$ for
the **annihilator** of the accessible effects inside the state space.

**Proposition (identification duality).**
$$\theta_1 \approx_E \theta_2 \iff \rho_1 - \rho_2 \in A_E,
\qquad \dim A_E = \dim S - \dim M_E.$$

The dichotomy is therefore a nesting $A_{E^\*} \subseteq A_E$:

| case | condition |
|---|---|
| separated | $\rho_1-\rho_2 \notin A_E$ |
| channel-limited | $\rho_1-\rho_2 \in A_E \setminus A_{E^\*}$ |
| law-surviving | $\rho_1-\rho_2 \in A_{E^\*}$ |

*Proof.* $\theta_1 \approx_E \theta_2 \iff \operatorname{Tr}((\rho_1-\rho_2)E)=0$
for every accessible effect $E \iff \rho_1-\rho_2 \perp M_E$; the dimension is
rank–nullity. $\square$

> **Where the state space matters.** The annihilator must be taken *inside* the
> admissible state space. With real symmetric qubit states, $\{Z,X\}$ spans the
> traceless space ($\dim M_E=2$, $A_E=0$); on the *complex* Hermitian space its
> annihilator is spanned by the antisymmetric $Y$ — but $Y$ is a difference of no
> two real density matrices, so it costs nothing. Getting this wrong flips the
> verdict.

**Physical reading (superselection).** When $E^\*$ is closed under composition
and adjoint — an *algebra of observables* — the annihilator $A_{E^\*}$ is the
**invisible sector**: the coherences no admissible observable sees. For an
algebra carrying a superselection rule, $A_{E^\*}$ is exactly the forbidden
inter-sector coherence. **Law-surviving ambiguity is superselection structure.**

**Exact instances** (real symmetric qubit states, $\dim S=2$ traceless):

| accessible effects | $\dim M_E$ | $\dim A_E$ | reading |
|---|---:|---:|---|
| $\{Z\}$ | 1 | 1 (span $X$) | the $X$-coherence; **channel-limited** once $X$ is allowed (`03`, kind 2) |
| $\{Z,X\}$ | 2 | 0 | fully identifiable |
| $\{Z\}$ closed (no $X$ allowed) | 1 | 1 | superselection: $|+\rangle,|-\rangle$ **law-surviving** |

**Nonlinear / parametric realization (gauge).** When worlds are parameters
$\theta$ and the law is a smooth $L$, the annihilator is replaced by the *kernel
of the linearized law map*: the infinitesimal ambiguity at $\theta_0$ is
$\ker DL(\theta_0)$, and the identifiable functionals are those orthogonal to it;
globally the ambiguity is the fiber $L^{-1}(L(\theta_0))$. For the geometry family
$L(\eta,\delta)=(\eta+\delta,\eta\delta)$ the fiber is *exactly* the $\mathbb Z/2$
orbit $\{(\eta,\delta),(\delta,\eta)\}$ (verified), while $DL$ has full rank — a
**discrete** ambiguity, an isolated gauge orbit rather than a continuous family.
So **annihilator** (linear/algebraic) and **gauge orbit** (nonlinear/parametric)
are the same clause in two settings.

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
| `03` two-kinds taxonomy | The dichotomy itself; §4 is the annihilator reading of kind 1 (superselection) |
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

## 10. The three results this exposes

The sharp clause of §4 is developed in
**[09 — Decidability, distortion, and the integrability of ambiguity](09-decidability.md)**:

- **Integrability** (§2 there): a continuous ambiguity is a genuine *symmetry*
  exactly when its fibers are homogeneous — a Lie foliation with constant
  structure functions; otherwise it is a foliation, not a group orbit.
- **Distortion** (§3): the collapse threshold $2e=d$ is exact, with
  $n^\* = \Theta((d-2e)^{-2}\log(1/\delta))$ and matching bounds.
- **Certification** (§4): the trichotomy is decidable by a rank computation given
  the model, but from data it is **one-sidedly** decidable — the resolvable labels
  are certifiable, the law-surviving label is not.

What remains genuinely open (`09` §7): an algebraic criterion for homogeneous
ambiguity; the exact collapse constant; a lower bound making the certification
asymmetry a theorem under a formal model of certifying test.

**Next:** [09 — Decidability, distortion, and the integrability of ambiguity](09-decidability.md).
