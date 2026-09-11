# 32 — Summaries are not compositional

`docs/04` says the coarsest adequate summary is question-relative; `docs/05` says
forgetting (a sum of maps) is not recombination (a sum of amplitudes). This note
gives the sharpest version of that obstruction for **causal / order** summaries:
an exactly additive *pair* summary does **not** close under composition to a
*chain* summary, and the exact size of the gap is a covariance.

The shape is taken from the upstream QR-05AJ/AK validation studies; the exact
statements are restated here in this project's notation.

## 1. Setup

Use the flat metric `ds^2 = du\,dv`, so the measure is `d\mu = du\,dv/2`, and the
strict product order

$$x \prec y \iff u_x < u_y \ \text{and}\ v_x < v_y .$$

For rectangular clips `A, B, C` write

$$h_A = \mu(A), \quad
J_{AB} = \iint \mathbf 1(x \prec y)\, d\mu(x)\,d\mu(y), \quad
T_{ABC} = \iiint \mathbf 1(x \prec y \prec z)\, d\mu(x)\,d\mu(y)\,d\mu(z).$$

Both factorize over the two coordinates — `J` as one quarter of the two directed
1-D integrals, `T` as one eighth of the two directed 1-D triple integrals — which
is what makes them exactly computable.

## 2. The pair-product surrogate

A pair-only summary, asked to predict the chain, multiplies the two adjacent
pairs and divides by the middle volume:

$$P_{ABC} = \frac{J_{AB}\, J_{BC}}{h_B} \qquad (h_B > 0).$$

The prediction error is *exactly* a covariance:

$$\boxed{\,T - P = h_B \cdot \operatorname{Cov}_B(L_A, R_C)\,}$$

where, for a uniform point `Y` in `B`, `L_A(Y)` is the volume of the
predecessors of `Y` in `A` and `R_C(Y)` the volume of its successors in `C`. So
the pair summary is **not** blindly wrong — it is wrong by exactly the *middle's
own dependence* on the two ends, and that is zero only when the two ends are
uncorrelated in the middle.

## 3. The unit-clip numbers

For `A = B = C = [0,1]^2` (so `h = 1/2`):

| quantity | value |
|---|---:|
| pair measure `J_{AA}` | `1/16` |
| triple measure `T_{AAA}` | `1/288` |
| pair fraction `J_{AA}/h^2` | `1/4` |
| triple fraction `T_{AAA}/h^3` | `1/36` |
| pair product `P_{AAA} = J^2/h` | `1/128` |
| product error `P - T` | `5/1152` |
| middle covariance `(T-P)/h_B` | `-5/576` |

The pair fraction and the triple fraction are **not** related by squaring:
`(1/4)^2 = 1/16 \ne 1/36`. Squaring the pair fraction re-draws the middle point;
the true chain shares it. That single discrepancy (`1/288` versus `1/128`) is
the whole content: **pair additivity is not chain composition.**

## 4. Conditionals are not transition probabilities

The natural conditional is `C_{AB} = J_{AB}/(h_A h_B)`. For `A = B = [0,1]^2`
this is `1/4` — so its **row sum is `1/4`, not `1`**. It is not a stochastic
transition matrix, and row-normalizing it to `1` would silently change the
statistic.

Coarsening a pair measure across a partition uses the *geometric* child weights

$$w_{ab} = \frac{h_a h_b}{h_A h_B}, \qquad
C_{AB} = \sum_{ab} w_{ab}\, C_{ab},$$

and only those reproduce `C_{AB}`. Annotation-derived substitutes (any weighting
by supplied marks `w_a` rather than true child volumes `h_a`) generally fail once
the marks are stale.

## 5. The demonstration

`foc.composition.composition_report`:

- unit clip: `T = 1/288`, `P = 1/128`, pair fraction `1/4` (row sum `\ne 1`),
  triple fraction `1/36` (squaring mismatch), middle covariance `-5/576`;
- covariance identity on `A=[0,1]`, `B=[1/4,3/4]`, `C=[0,1]`:
  `T = 11/96`, `P = 1/8`, `\operatorname{Cov} = -1/48`, and `T - P = h_B\operatorname{Cov}`
  holds exactly (and on the other test clips as well);
- geometric coarsening: weights `[[1/6,1/3],[1/6,1/3]]` (sum `1`) give `11/24`,
  whereas the unweighted average gives `7/16`.

## 6. Status

Implemented as `foc.composition` (`pair_int_1d`, `triple_int_1d`, `clip_volume`,
`pair_measure`, `triple_measure`, `pair_product`, `middle_covariance`,
`conditional`, `covariance_identity_1d`, `coarsening_weights`,
`aggregate_conditional`, `unit_rectangle_report`, `composition_report`) and run in
demo section 28.

**Provenance.** Upstream-derived (QR-05AJ/AK): the pair-product construction, the
covariance identity and the unit-clip numbers come from the upstream studies. The
exact 1-D integral machinery and the coarsening fixture are this project's.

**Back to** [README](../README.md).
