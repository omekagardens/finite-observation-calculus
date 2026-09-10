# 04 — Question-relative minimal summaries

There is no universal "sufficient statistic." The coarsest adequate summary of a history is defined **only relative to a declared family of future questions**.

## 1. Predictive equivalence

Fix a family of source-history maps $\mathcal J_h$ (one per history $h$) and a declared family of future instruments $\{\mathcal F^u_y\}$. For each history define two linear functionals on input operators:

$$d_h(\rho) = \operatorname{Tr}\mathcal J_h(\rho), \qquad
n_h^{u,y}(\rho) = \operatorname{Tr}\mathcal F^u_y\big(\mathcal J_h(\rho)\big).$$

The probability of future outcome $y$ under setting $u$, *conditioned* on history $h$, is

$$\frac{n_h^{u,y}(\rho)}{d_h(\rho)} .$$

Two histories $h \sim k$ are **predictively equivalent** when these ratios agree for every declared $(u,y)$ and every input state $\rho$ where both denominators are positive.

The equivalence classes form the **coarsest summary valid for this future family**: a summary label $T(h)$ is valid exactly when equal labels imply $h \sim k$.

## 2. The question-relativity

The same histories partition differently for different future families.

- A summary sufficient for one set of future questions need not be sufficient for another.
- Richer future families can **split** classes; they never merge previously distinct ones.
- The guarantee concerns **conditional future probabilities only** — it does *not* preserve the history weights $d_h$, arbitrary feedback, or all information about an unknown input.

## 3. Worked example: measure $Z$, then $X$

The four branch maps are

$$\mathcal J_{z,s}(\rho) = Q_s P_z \rho P_z Q_s = \frac{\rho_{zz}}{2}\,Q_s .$$

For every history $(z,s)$, the normalized conditional state is $Q_s$ — the eigenstate of $X$ with sign $s$ — **independent of $z$**. Therefore:

- for *all* future measurements on the qubit, the history's prediction depends only on $s$,
- the four histories collapse to **two** prediction classes: $\{s=+1\}$ and $\{s=-1\}$.

So "keep only the last $X$ outcome" is the coarsest summary sufficient for any future measurement on the qubit.

**But** this summary does not preserve the history weights. At $\rho = \operatorname{diag}(3/4, 1/4)$, the two histories mapping to the class $s=+1$ have weights $3/8$ (from $z=0$) and $1/8$ (from $z=1$). A question that asks "what was the discarded $Z$ outcome?" — i.e., a question about the full record probability — is **not** answered by the summary.

## 4. The practical consequence

You cannot ask "what is the minimal representation of this state?" without first answering "**for what downstream prediction?**"

- **KV-cache / hidden-state compression.** The right summary of a transformer's hidden state depends on which next-token (or next-layer) questions you must preserve. A summary optimal for one head is not optimal for another.
- **Distillation.** A student model need only preserve the classes induced by the *declared* target tasks — but that is an explicit, question-relative choice, not a universal property of the teacher's activations.
- **Forgetting a mark can change a predicted mean.** Deleting an interior piece of the record because it "looks irrelevant" is only safe relative to a specific future family; against a different one it changes predictions.

---

**Next:** [05 — Forgetting vs. recombination](05-forgetting.md).
