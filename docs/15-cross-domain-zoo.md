# 15 — Cross-domain witness zoo

The dichotomy (`docs/08`) is stated abstractly. This note collects three small
*exact* witnesses of the same phenomenon in neighbouring fields. Each is an
instance of *observational equivalence, with a real distinction hidden in a
channel the declared access class does not reach*.

## W1 — Causal observational equivalence

Chain $X \to Y \to Z$ and fork $X \leftarrow Y \to Z$. Both realize
$X = Y = Z$ from an exogenous $U \sim \mathrm{Bern}(1/2)$, so they induce the
**same** observational joint
$\{(0,0,0): \tfrac12,\ (1,1,1): \tfrac12\}$ — indeed all three DAGs on the
skeleton $X\!-\!Y\!-\!Z$ with no collider are Markov equivalent. But

$$P(Z=1 \mid do(X=1)) = 1 \text{ (chain)}, \qquad = \tfrac12 \text{ (fork)}.$$

So the causal direction is invisible to observational data. In the dichotomy it is
**channel-limited** if interventions are admissible and **law-surviving** if only
observations are.

## W2 — Conformal marginal vs conditional

A conformal-style prediction set covers stratum 0 always and stratum 1 never;
stratum 1 has mass $\tfrac1{20}$. Marginal coverage is $\tfrac{19}{20} \ge 0.95$,
while conditional coverage in stratum 1 is $0$. In the dichotomy the *report
event* ("which stratum") is a record that is not $E$-sufficient: the marginal
guarantee is sufficiency over the pooled input, the conditional guarantee is
sufficiency *within the stratum* (`docs/06`).

## W3 — Partial identification

A fraction $\tfrac34$ of $Y$ is observed with mean $\tfrac12$; the rest is
missing, so Manski bounds give $E[Y] \in [\tfrac38, \tfrac58]$. Values inside the
interval are **ambiguous** (some completion realizes them); values outside are
**infeasible**. The identified set is the ambiguity; the "ambiguous vs infeasible"
cut is the analogue of channel-limited vs law-surviving (a completion exists vs no
model exists).

## What they share

Each is "same observable, different structure," and each distinction is reachable
only through a channel *outside* the declared access class — an intervention, a
stratum label, a missing-data completion. The dichotomy supplies the vocabulary:
**resolvable by a richer channel** vs **not**.

## Status

Exact restatements of standard distinctions (Markov equivalence; marginal vs
conditional validity; Manski bounds) — pedagogical witnesses, not new results.
Implemented as `foc.crossdomain`.

**Back to** [README](../README.md).
