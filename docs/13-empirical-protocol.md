# 13 — An empirical probe-audit protocol

`docs/10` §5 gives a decision procedure for negative probing results and `docs/11`
gives its certifiability. This note turns them into an operational protocol and
instantiates it exactly on the two-site model.

## 1. The protocol

Given a representation (a model's internal state) and a feature of interest:

1. **Declare the probe families**, coarse to fine:
   $E_0 \subset E_1 \subset \cdots$, each a set of readout directions (effects).
   This declaration is the modeling choice that makes "symmetry" / "observability"
   well-posed (`docs/09` §2, `docs/12`).
2. **Define the feature** as a difference $\Delta$ of two representation states.
3. **Estimate the separation**

$$d_F(\Delta) \;=\; \max_{E \in F} \lvert \operatorname{Tr}(\Delta E) \rvert$$

   under each family, from `n` samples.
4. **Apply the margin certifier.** Pick a margin $t > 0$ and a confidence
   $\delta$; the margin-$t$ verdict is *certified* iff
   $n \cdot t^2 \ge K(\delta)$ — the rational certificate of `docs/07`
   ($K(1/20) = 10$).
5. **Report** the verdict per feature and the samples needed.

## 2. The certifier

With $E_0$ the declared family and $E_{\text{last}}$ the finest:

| verdict | condition |
|---|---|
| **separated** | $d_{E_0} \ge t$ |
| **channel-limited** | $d_{E_0} < t \le d_{E_{\text{last}}}$ |
| **law-surviving (to $t$)** | $d_{E_{\text{last}}} < t$ |

Certified iff $n \cdot t^2 \ge K(\delta)$; samples needed
$= \lceil K(\delta) / t^2 \rceil$. The separation is estimated (a *difference*,
certifiable); the *exact* identity is not (`docs/11`): the protocol can report
"law-surviving **to $t$**", never law-surviving outright.

## 3. Synthetic instantiation

Two-site representation; probe families `local` (one site at a time) and `joint`
(plus cross-site); features `site-A logit` $(Z \otimes I)$ and
`cross-site correlation` $(Z \otimes Z)$; measurement models `open` (joint
admissible) and `local-only` (a superselection rule). Separations are exact:
`site-A logit` has $d_{\text{local}} = 4$; `cross-site correlation` has
$d_{\text{local}} = 0$, $d_{\text{joint}} = 4$.

At margin $t = 2$, $n = 100$, $K = 10$ (certified, $\lceil 10/4 \rceil = 3$
samples needed):

| feature | model | $d_{\text{decl}} / d_{\text{full}}$ | verdict |
|---|---|---|---|
| site-A logit | open | 4 / 4 | separated |
| cross-site correlation | open | 0 / 4 | channel-limited |
| site-A logit | local-only | 4 / 4 | separated |
| cross-site correlation | local-only | 0 / 0 | law-surviving |

At margin $t = 5 > 4$ **every** feature falls below the margin: the verdict is
"law-surviving to 5" throughout. A coarse enough margin resolves nothing — the
certification-radius effect of `docs/11` §4, seen from the practitioner's side.

## 4. Applying to a real model

Replace the toy effects by the actual probe readouts (linear, MLP, attention, or
cross-layer directions), estimate $d_F(\Delta)$ from held-out data, and apply the
same certifier. Two honest boundaries:

- the separation is *estimated*; a negative result is "law-surviving to the
  margin", never exact (`docs/11` §2c);
- the **declaration** of the families is what makes the verdict meaningful — a
  feature invisible to `E_0` is channel-limited *relative to* the declared
  completion, not absolutely.

## 5. Status

The protocol is Le Cam/Chernoff testing (`docs/11`) plus the annihilator rank test
(`docs/09` §4a); the instantiation is exact (`Fraction`). The contribution is the
operational packaging — the margin, the sample budget, and the disciplined
report — implemented as `ambiguity.certify_audit` and run in demo section 11.

**Back to** [README](../README.md).
