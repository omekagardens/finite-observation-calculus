# 02 — Behavioral vs. mechanistic equivalence

Two computations can be indistinguishable from the outside yet different on the inside. This note makes that exact.

## 1. Two notions of equality

Fix two observation events and compare them after "forgetting" the record versus after retaining it.

- **Record-discarded equality.** After executing the events, trace out the record and compare only the residual state.
- **Recorded equality.** Compare the complete classical–quantum object $\Xi = \sum_R \tau_R \otimes |R\rangle\langle R|$, including the record.

The central point: **the first is strictly weaker than the second**, and the gap is exactly where "behavioral" equivalence stops being "mechanistic" equivalence.

## 2. The commuting-map criterion

For incomparable events $e,f$ with fixed outcomes $x,y$, define the outcome maps $\mathcal I^s_{e,x}$ and $\mathcal I^t_{f,y}$. A *sufficient* condition for every schedule to agree — after canonical record-slot identification — is

$$\mathcal I^t_{f,y} \circ \mathcal I^s_{e,x} = \mathcal I^s_{e,x} \circ \mathcal I^t_{f,y}
\quad\text{for every } x, y .$$

This is the familiar commuting-map argument, applied to *recorded* maps. Every pair of linear extensions of a finite partial order is connected by adjacent swaps of incomparable events, so pairwise commutativity propagates to all schedules.

## 3. The Z/X counterexample

The cleanest witness that discarding records hides a real difference. Let $Z$ and $X$ be the two projective measurements on a single qubit, with record always displayed as $(Z\text{ outcome},\, X\text{ outcome})$.

Start in state $|0\rangle$. The two schedules give:

| Record | $Z$ then $X$ | $X$ then $Z$ |
|---|---:|---:|
| $(0, +)$ | $1/2$ | $1/4$ |
| $(0, -)$ | $1/2$ | $1/4$ |
| $(1, +)$ | $0$ | $1/4$ |
| $(1, -)$ | $0$ | $1/4$ |

The recorded instruments plainly differ. But **discard the record**: both $Z$-then-$X$ and $X$-then-$Z$ send *every* qubit state to the maximally mixed state $I/2$. Their record-discarded channels commute — so a "behavioral" check that ignores intermediate records would certify an equality that is **false** for the retained evidence.

## 4. Even complete joint probabilities can miss the difference

A stronger control. Start from $I/2$. Both schedules then assign probability $1/4$ to *all four* joint records — the complete joint probability distributions agree. Yet the residual state in each branch differs:

- $Z$ then $X$: each branch ends in an $X$-eigenstate,
- $X$ then $Z$: each branch ends in a $Z$-eigenstate.

So identical joint *probabilities* still hide an operator-level (mechanistic) disagreement. Comparing outputs — even the full output distribution — is not the same as comparing internal states.

## 5. Why this matters for inference systems

- **Behavioral evals cannot certify mechanistic claims.** Two models can match on every held-out input–output pair and still differ internally. If the goal is interpretability, alignment auditing, or transfer, you must retain and compare intermediate states, not just final outputs.
- **"Output-equivalent" is not "internally equivalent."** A distilled model that reproduces a teacher's logits does not, by that fact alone, reproduce the teacher's computation. The Z/X example is the minimal proof.
- **The record is the thing being lost.** The information that separates the two schedules lives in the *intermediate* record. Drop it, and the difference vanishes. This is the core theme of the whole repository.

---

**Next:** [03 — The two-kinds-of-ambiguity taxonomy](03-ambiguity-taxonomy.md).
