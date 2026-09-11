# 30 — Replacement robustness: a minimax theory of coarse replacement

`docs/05` §3 and `docs/21` §5 decide *whether* a coarse replacement is valid for a
declared downstream — a binary, source-relative criterion ("is the downstream
blind to the gap?"). This note makes the same question **quantitative**: over a
*declared* uncertainty set, how bad can a replacement be, and exactly when is the
worst case attained? Everything is exact.

The shape is taken from the upstream QR-05AA–AE validation series (declared
bounds, fixed blends, subtract-coarse-before-maximising); the exact statements
below are restated here in this project's notation.

## 1. The setup

Fix an **actual noise level** `t` in a declared finite set, an **assumed model**
`s`, and a **retained-detailed weight** `a`, giving the fixed blend

$$h_a = (1-a)\,g + a\,f_s$$

of the coarse forecast `g` and the detailed forecast `f_s`. The risk `R(t,s,a)` is
Brier risk; `G(t)` is the coarse-only risk under the *same* actual law; the
**signed excess** is

$$E(t,s,a) = R(t,s,a) - G(t).$$

The coarse rule is `a = 0`, so `E(t,s,0) = 0` identically.

## 2. Minimax retention

The declared uncertainty bound `u` picks the set `S_u = {t \le u}`. The
worst-case excess and its minimax value are

$$M(s,u,a) = \max_{t \in S_u} E(t,s,a), \qquad V(s,u) = \min_a M(s,u,a).$$

Two rules of evaluation define the object (getting them wrong changes the
answer): **subtract coarse risk before the maximum** (never
`max R − max G`), and **retain negative values** (never clip at zero). Three
consequences hold by construction:

- **`V(s,u) \le 0`** — the coarse rule `a = 0` is always available and gives `0`;
- **monotonicity** — nested bounds make every `M` and `V` nondecreasing in `u`;
- **everything is retained** — *all* maximizers and *all* minimizing weights, not a
  tie representative.

Optimality is relative to the declared menu of weights and the declared bounds.

## 3. The replacement envelope

Replace the finite menu by a *whole-fiber* replacement class: for each fiber `N`
an arbitrary law `\mu_N` on its alphabet, with clean excess `c` and per-fiber
coefficients `B_N(z)`. The envelope is

$$E(t,\mu) = (1-t)\,c + t \sum_N \sum_z \mu_N(z)\, B_N(z),
\qquad U_t = (1-t)\,c + t\,S, \quad S = \sum_N \max_z B_N(z).$$

> **Attainment criterion.** A maximum over the closed simplex is attained by a
> *strictly positive* law **iff zero is a worst world** (then every law attains
> `c`) **or every fiber is flat** (then every law attains `S`).

The two halves are the only ways a boundary attainment can avoid being a
boundary artifact: either the `t = 0` term carries the maximum, or the
per-fiber maximizers can all be given full support at once.

## 4. Continuous retention, and what the menu costs

The whole-fiber excess reduces, per rule, to a convex quadratic in the retained
weight (`docs/30` §1's affine structure):

$$Q(a) = A\,a^2 - 2B\,a, \qquad A = (1-t)D_0 + t\,S_1 \ge 0,
\qquad B = (1-t)C_0 \ge 0 .$$

On `[0,1]` the minimizer is the projection `a^* = \operatorname{clip}(B/A, 0, 1)`
(unique for `A > 0`; the whole interval only when `A = B = 0`). The certificate is
the exact **KKT identity**

$$Q(a) - Q(a^*) = A\,(a-a^*)^2 + g^* (a-a^*), \qquad g^* = 2A a^* - 2B,$$

and the cost of restricting to a finite menu `\mathcal M` is bounded **sharply**:

$$0 \le \min_{\mathcal M} Q - \min_{[0,1]} Q \le \frac{A}{16}
\qquad (\text{i.e. } 16\cdot\text{gap} \le A).$$

The `1/16` is the squared `1/4` grid spacing of the three-point menu
`\{0, \tfrac12, 1\}`.

## 5. Aggregate is not per-instance

Per history `H` the same excess is a quadratic `Q_H(a) = A_H a^2 - 2B_H a`. The
aggregate polynomial splits into **three signed groups** by the sign of `Q_H` on
each stratum:

$$P(a) = \sum_{\text{positive}} w_H Q_H(a), \quad
N(a) = \sum_{\text{negative}} w_H Q_H(a), \quad
Z(a) = \sum_{\text{zero}} w_H Q_H(a),$$

with the **coefficientwise identity** `P + N + Z = \sum_H w_H Q_H` everywhere.
Keeping the `Z` group matters: on a stratum where the aggregate vanishes, `Z` can
carry nonzero coefficients. Consequently a **witness that maximizes the aggregate
need not bound any single history**, and an **aggregate zero can hide
equal-and-opposite per-history risks** — the replacement analogue of
`docs/06`'s marginal-vs-conditional gap.

## 6. Opposite stress tilts cancel

Two declared stress tilts on a fiber of `m` labels (rank `r = 0..m-1`) are

$$\mu_{\text{fwd}}(z_r) = \frac{2(r+1)}{m(m+1)}, \qquad
\mu_{\text{rev}}(z_r) = \frac{2(m-r)}{m(m+1)} .$$

Both are positive and normalized, their pointwise mean is the uniform law
`1/m`, and therefore the two tilted worst cases **cancel exactly** against the
nominal one:

$$\frac{M_{\text{fwd}} + M_{\text{rev}}}{2} = M_0 .$$

## 7. The demonstration

`foc.replacement.replacement_report` (four noise levels, three weights, two
assumed models):

| quantity | value |
|---|---|
| minimax `V`, model 0 | `−1/4, 0, 0, 0` (nondecreasing, `≤ 0`) |
| minimax `V`, model 1 | `−1/4, −1/4, −1/4, −1/4` |
| envelope `S` / max (sharp fibers) | `5/4` — **not** full-support attained |
| envelope max (flat fibers) | `5/6` — full-support attained |
| envelope max (clean worst) | `2` — zero is worst, attained |
| continuous optimum `a*` (A=1/2, B=3/10) | `3/5`, with menu gap `1/200 ≤ A/16` |
| aggregate zero at `a = 1/2` | hides `+1/8` and `−1/8` |
| tilt identity (`m = 4`) | `(3/20 + (−3/20))/2 = 0` |

## 8. Status

Implemented as `foc.replacement` (`excess`, `excess_table`, `affine_in_t`,
`worst_excess`, `minimax_certificate`, `minimax_values`, `envelope`,
`full_replacement_max`, `all_fibers_flat`, `full_support_maximum_attained`,
`envelope_profile`, `retention_excess`, `retention_optimizer`,
`retention_minimum`, `retention_kkt`, `menu_gap`, `menu_gap_sharp`,
`history_excess`, `aggregate_coefficients`, `group_polynomials`,
`aggregate_zero_hides_risk`, `forward_tilt`, `reverse_tilt`, `tilt_mean`,
`tilts_are_opposite`, `tilt_cancellation`, `replacement_report`) and run in demo
section 26.

**Provenance.** Upstream-derived (QR-05AA–AE): the minimax, envelope and
full-support statements are extractions restated in this project's notation; the
`1/16` menu bound, the signed-group reading of `docs/06`, and the exact
implementation are this project's.

**Back to** [README](../README.md).
