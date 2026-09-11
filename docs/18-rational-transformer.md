# 18 — A genuine transformer, trained without floats

This note **corrects** the claim in `docs/17` §5 that a trained transformer needs
floating point. It does not.

## 1. Why the claim was wrong

The only primitives a transformer needs that are irrational for rational inputs
are three, and each has an exact rational substitute:

| primitive | why irrational | rational substitute |
|---|---|---|
| `softmax` (`exp`) | transcendental | **linear** or **squared-normalized** attention $a_i^2/\sum_j a_j^2$; or a truncated Taylor $\exp$ |
| `LayerNorm` (`sqrt`) | square root | sum / $L^1$ normalization |
| `GELU` / `SiLU` (`exp`, `erf`) | transcendental | **ReLU** (exact for rationals), or a polynomial activation |

So a *genuine* transformer — attention + residual + MLP — is exactly
representable, and exactly trainable.

## 2. The block

One head, over `Fraction`:

$$Q = XW_Q,\ K = XW_K,\ V = XW_V,\quad S = QK^\top,\quad
A_{ij} = \frac{S_{ij}^2}{\sum_k S_{ik}^2},\quad O = AV;$$
$$X_1 = X + O,\quad H = \mathrm{ReLU}(X_1 W_1),\quad X_2 = X_1 + H W_2,\quad
\hat y = X_2^{(\text{last})}\cdot w.$$

Every operation is rational; the "softmax" is replaced by squared normalization.

## 3. Exact automatic differentiation

Forward-mode AD via **dual numbers over $\mathbb Q$** (a value plus a derivative),
so every gradient is an exact `Fraction`. Exact gradient descent follows.

## 4. The run

`foc.transformer.train_exact(TOY_DATA, steps=2, eta=1/50)`:

```
step 0: loss = 115.721    max denominator bits = 6
step 1: loss =   5.1398   max denominator bits = 187
step 2: loss =   0.822898 max denominator bits = 5839
```

The loss falls and **every weight is a `Fraction`** — no float is used anywhere.

## 5. The real cost: arithmetic growth

Exact denominators roughly triple in bits per step ($6 \to 187 \to 5839$). Full-model
exact training is therefore practical for only a few steps; beyond that the
big-integer arithmetic dominates. Mitigations that stay exact:

- train the **readout** in closed form (least squares, `docs/17`) on a frozen block;
- **fixed-denominator / integer-scaled** arithmetic (exact so long as denominators
  are tracked explicitly);
- simply take few steps.

Truncating denominators would bound the cost but would *break* exactness — that is
floating point by another name.

## 6. The corrected statement

> Floating point is a **practical representation** for training a transformer, not
> a **logical necessity**. A genuine transformer trains exactly in rationals; the
> binding constraint is arithmetic growth, not representability.

## 7. Status

Implemented as `foc.transformer` (`Dual`, `loss`, `grad`, `exact_step`,
`train_exact`) and run in demo section 16; tested in `tests/test_transformer.py`.

**Back to** [README](../README.md).
