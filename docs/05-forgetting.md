# 05 — Forgetting is not recombination

When a representation is compressed, two operations look superficially alike but are mathematically different. Confusing them produces silently wrong models.

## 1. Coarse-graining = summing probability maps

If a fine outcome $x$ is reported only as a coarse value $z = f(x)$, the coarse instrument is a **sum of maps**, not a sum of amplitudes:

$$\mathcal C_z = \sum_{x : f(x) = z} \mathcal I_x .$$

This is **classical forgetting**: each fine branch contributes its probability, and the branches are added as *channels*. Nothing is recombined coherently.

## 2. Coherent recombination = summing amplitudes

By contrast, when the model genuinely superposes alternatives, the amplitudes (Kraus operators) are summed **before** the square-modulus, and the result is a single state:

$$\rho_{\text{coherent}} = \Big(\sum_\gamma C_\gamma\Big)\rho\Big(\sum_\delta C_\delta\Big)^\dagger
\quad \ne \quad
\rho_{\text{discarded}} = \sum_\gamma C_\gamma \rho C_\gamma^\dagger .$$

The two are different transformations. Discarding a classical record does **not** restore cross terms; summing amplitudes is *not* the same as summing branches.

## 3. The replacement condition

Suppose later feedback uses the fine $x$ through an instrument $\{\mathcal F_{x,y}\}$. Replacing it by feedback that depends only on the coarse $z$ requires a physical instrument $\{\mathcal G_{z,y}\}$ satisfying, for every $z,y$ and all inputs,

$$\sum_{x : f(x)=z} \mathcal F_{x,y} \circ \mathcal I_x
= \mathcal G_{z,y} \circ \mathcal C_z .$$

This is a **source-relative replacement condition**. It is not automatic, and its failure has a clean certificate.

## 4. The impossibility witness

To prove no physical replacement exists, exhibit two inputs that the coarse channel sends to the **same** state but that the fine feedback sends to **different** states:

- identical coarse input,
- different required output.

No single operation on the coarse input can reproduce both required outputs. This "two colliding inputs" argument is the information-theoretic signature of non-invertibility, and it is an *actual* impossibility proof — not merely the failure of one candidate replacement.

## 5. Why this matters for compression

- **Quantization and pruning are forgetting, not recombination.** Merging two latent states of a network is a sum of probability mass (or a weighted merge of channels). It must *never* be treated as a coherent superposition. The correct correctness criterion is the replacement condition above.
- **"Can this smaller model reproduce the larger one?"** is answered by the impossibility witness: find two inputs the compressed state collapses together that the full model distinguishes. If they exist, the compression is lossy *for that downstream behavior*.
- **A failed candidate is not a proof of impossibility.** Only the colliding-inputs construction is. Distinguishing "I haven't found a good compression" from "no compression exists" is exactly the difference between the two.

---

**Next:** [06 — Marginal vs. conditional confidence](06-confidence.md).
