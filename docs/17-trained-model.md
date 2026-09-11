# 17 — A trained model in pure rationals

`docs/16` ran the protocol on a *constructed* model. This note **trains** one —
exact rational training, closed-form plus gradient descent — then audits the
learned representation, scored against what training actually learned.

## 1. Why it is possible without torch or floats

Training is exact whenever the **model, loss, data, initialization, and step size**
are all rational. Rational functions have rational derivatives, and closed-form
optima are rational linear solves. So a trained model needs only `fractions.Fraction`
and the exact `linalg` helpers — no dependency, no floating point.

## 2. The model and the task

$$\hat y(x) = a\,x_1 + c\,x_1 x_2, \qquad
\rho(x) = \tfrac14\big[\, I\!\otimes\! I + (a\,x_1)\,Z\!\otimes\! I
+ (c\,x_1 x_2)\,Z\!\otimes\! Z \,\big].$$

Data: four rational points. Two tasks:

- **linear:** $y = x_1$;
- **quadratic:** $y = x_1 + x_1 x_2$.

## 3. Training, exactly

**Closed-form least squares.** $(a,c)$ solves $(\Phi^\top\Phi)(a,c) = \Phi^\top y$
by exact Gaussian elimination. Both tasks fit *exactly*:

| task | $(a,c)$ | residual |
|---|---|---|
| linear | $(1,\ 0)$ | $0$ |
| quadratic | $(1,\ 1)$ | $0$ |

**Exact gradient descent.** Two steps from $(0,0)$ with $\eta = \tfrac1{20}$ keep
every iterate rational and strictly decrease $\tfrac12\lVert\Phi\theta - y\rVert^2$:

```
quadratic:  (0,0) -> (11/20, 1/2) -> (81/100, 59/80) -> ...
  loss:        943/400   >   169581/320000   >   15324301/128000000
```

## 4. The trained-model audit

At probe input $x = (1,1,0)$, the learned state decomposes into a marginal part
$(a/4) Z\!\otimes\! I$ and a correlation part $(c/4) Z\!\otimes\! Z$; the model
never uses $x_3$. The audit (`ambiguity.classify`) gives:

| feature | linear task | quadratic task |
|---|---|---|
| marginal $a$ | separated | separated |
| correlation $c$ | **law-surviving** ($c=0$) | **channel-limited** |
| distractor $x_3$ | law-surviving | law-surviving |

Every verdict matches what training learned. The headline row is the correlation:
when the task does **not** need the product, training drives $c \to 0$ and the
audit correctly reports **law-surviving** — the feature was never learned.

## 5. What it establishes, and its limits

- **Establishes:** the probe audit works on a *trained* model in exact rationals;
  training determines which components are present, and the audit recovers exactly
  that — with a closed-form anchor and an illustrative exact GD path.
- **Limits:** a toy model and task; rational architecture (no `exp`/softmax); the
  anchor is closed-form LS, with GD illustrative. It is not a trained transformer;
  a genuine one needs floats and design B.

## 6. Status

Exact, reproducible, zero-dependency. Implemented as `foc.train`
(`least_squares`, `gradient_step`, `train_toy`, `trained_audit`) and run in demo
section 15.

**Back to** [README](../README.md).
