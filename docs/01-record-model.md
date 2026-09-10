# 01 — The record model

This note fixes the minimal formal vocabulary used throughout. Everything is finite and exact.

## 1. States

A **state** $\rho$ is a positive semidefinite, unit-trace operator on a finite-dimensional real or complex inner-product space, or a probability vector over a finite set.

- **Classical special case.** $\rho$ is a probability vector $p = (p_1,\dots,p_d)$, $p_i \ge 0$, $\sum_i p_i = 1$. An observation map is a stochastic matrix (a conditional distribution).
- **General case.** $\rho$ is a density operator (positive semidefinite, $\operatorname{Tr}\rho = 1$). An observation map is a collection of Kraus operators. The classical case is the restriction to diagonal operators, so nothing below is lost by working in the general notation.

We write $\rho \succeq 0$ for positive semidefinite, and $\operatorname{Tr}$ for the trace (sum of diagonal entries).

## 2. Events, records, and settings

A **model** consists of:

- a finite set $V$ of **events**,
- a strict partial order $\prec$ on $V$ ("precedes"; a partial order that is irreflexive and transitive),
- an initial state $\rho$.

Each event $e$ carries:

- a finite **setting** set $S_e$ (the *choice* the event can make), and
- a finite **outcome** set $\Omega_e$.

Executing an event appends a **record** entry — the pair $(s, x)$ of the selected setting and the observed outcome — to a fresh, uniquely identified record slot $r_e$. Each slot has exactly one writer.

An event may **read** a declared set $A_e \subseteq \{r_f : f \prec e\}$ of prior record slots, and it chooses its setting through a deterministic policy

$$s_e = g_e\big(R_{A_e}\big),$$

where $R_{A_e}$ is the portion of the record visible to $e$.

> **Discipline.** A policy may read only *declared causal-past* records. It may not read the future, an incomparable event, execution position, a hidden state, or an undeclared record. This is the formal version of "an agent can only condition on what it has actually observed."

## 3. Observation maps

For event $e$, setting $s$, and outcome $x$, an **instrument** supplies Kraus operators $M^s_{e,x,a}$ (the index $a$ labels alternatives not separately recorded) with

$$\sum_{x,a} (M^s_{e,x,a})^\dagger M^s_{e,x,a} = I .$$

The outcome-$x$ map acts as

$$\mathcal I^s_{e,x}(\rho) = \sum_a M^s_{e,x,a}\,\rho\,(M^s_{e,x,a})^\dagger ,$$

so the outcome probability and the post-measurement state are

$$p(x \mid \rho, e, s) = \operatorname{Tr}\mathcal I^s_{e,x}(\rho), \qquad
\rho_x = \frac{\mathcal I^s_{e,x}(\rho)}{p(x \mid \rho, e, s)} \quad\text{if } p > 0 .$$

- Each outcome map is **trace-nonincreasing** (probabilities never exceed one).
- The sum over all outcomes is a **trace-preserving channel** (total probability is conserved).
- The **classical special case** is a projective measurement in the diagonal basis: $\mathcal I_x(\rho) = P_x \rho P_x$ with $\sum_x P_x = I$.

## 4. Records are first-class objects

A **record** $R$ is the partial map assigning each written slot $r_e$ its pair $(s_e, x_e)$. The record is kept *separate* from the state $\rho$: a record alone does **not** determine a state, and a state alone does not determine a record.

The full object after executing a schedule is a **classical–quantum state**

$$\Xi = \sum_R \tau_R \otimes |R\rangle\langle R|,$$

a block-diagonal object in which the classical record and the residual state are correlated. This is the formal reason the record must be retained rather than traced out: the two are entangled by the observation.

## 5. Schedules

A **schedule** is a linear extension $\sigma = (e_1,\dots,e_n)$ of $\prec$: a total order in which every predecessor of an event appears before it.

Executing a schedule from $\rho$ produces a probability over complete **histories**

$$p_\sigma(h \mid \rho) = \operatorname{Tr}\mathcal J_h^\sigma(\rho), \qquad
\mathcal J_h^\sigma = \mathcal I^{s_n}_{e_n,x_n} \circ \cdots \circ \mathcal I^{s_1}_{e_1,x_1},$$

where the settings in a history must obey their policies, and composition acts right-to-left.

---

**Next:** [02 — Behavioral vs. mechanistic equivalence](02-equivalence.md).
