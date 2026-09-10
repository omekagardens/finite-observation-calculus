# 11 — The certification dichotomy

`docs/09` §4 sketched the one-sided decidability of the classification. This note
makes it a theorem. The key object is a **margin** $t$: at any fixed margin the
whole trichotomy is certifiable from data at cost $\Theta(t^{-2}\log(1/\delta))$;
the *exact* (unmargined) classification is the singular limit $t \to 0$, and only
there is it non-certifiable.

> **Differences are certifiable; exact identities are not.**

## 1. Setup

- Worlds $\theta \in \Theta$; a finite **admissible** experiment class $E^\*$; a
  **declared** sub-class $E \subseteq E^\*$.
- A **pair** $\omega = (\theta_1, \theta_2)$; for $e \in E^\*$ it induces laws
  $P^e_1, P^e_2 \in \Delta(\Omega_e)$.
- **Separation** under $F \subseteq E^\*$:
  $d_F(\omega) = \max_{e \in F} \lVert P^e_1 - P^e_2\rVert_{\mathrm{TV}}$.
- **Labels:** *separated* $(d_E > 0)$, *channel-limited* $(d_E = 0$ and
  $d_{E^\*} > 0)$, *law-surviving* $(d_{E^\*} = 0)$. These three exhaust the
  possibilities.

By `docs/08` §4, $d_F = 0 \iff \rho_1 - \rho_2 \in A_F$, so the labels are exactly
the annihilator nesting $A_{E^\*} \subseteq A_E$ (`docs/09` §4a).

## 2. The theorem

**Theorem 2.1 (certification dichotomy).** Fix a margin $t > 0$.

**(a) Certifiable to margin $t$.** There is a certifier using
$n = O(t^{-2}\log(1/\delta))$ samples per experiment whose verdict is correct
*to precision $t$* with error $\le \delta$:

$$d_E \ge t \Rightarrow \text{“separated”}, \qquad
d_E < t \le d_{E^\*} \Rightarrow \text{“channel-limited (to } t\text{)”}, \qquad
d_{E^\*} < t \Rightarrow \text{“law-surviving (to } t\text{)”}.$$

**(b) Tight.** $n = \Omega(t^{-2}\log(1/\delta))$ is necessary.

**(c) Singular limit.** The *exact* classification ($t = 0$) is **not**
certifiable: for every $n$ and every $\delta < \tfrac12$ there are $\omega$ with
$d_{E^\*} = 0$ and $\omega_\varepsilon$ with $d_E = 0 < d_{E^\*} \le \varepsilon$
whose $n$-sample laws differ by $o(1)$ as $\varepsilon \to 0$. No certifier has
uniform error $< \tfrac12$.

*Proof.* **(a)** Empirical estimates of each TV distance concentrate (Hoeffding /
Chernoff); thresholding at $t/2$ with a union bound over the finitely many
experiments $E^\*$ gives the verdict at $n = O(t^{-2}\log(1/\delta))$. **(b)** Two
laws at TV distance $t$ need $\Omega(t^{-2}\log(1/\delta))$ samples to distinguish
— Le Cam's two-point method with Bretagnolle–Huber (`docs/09` Thm 3.2); take the
extremal pair at separation $t$. **(c)** At $\varepsilon = 0$ the pair has
$P^e_1 = P^e_2$ on all of $E^\*$; the laws are continuous in $\varepsilon$, so for
fixed $n$, $P^{e,\otimes n}_\varepsilon \to P^{e,\otimes n}_0$, and Le Cam gives
min-max error $\ge \tfrac12(1 - o(1))$. $\square$

This *corrects* the sketch in `docs/09` §4: "channel-limited is certifiable" holds
only **to a margin** — deciding it as opposed to *separated* requires the
$E$-agreement $d_E < t$, which is itself a margin claim, certifiable at the same
$\Theta(t^{-2})$ cost but never exactly at $t=0$.

## 3. Mechanism: existentials certify, universals do not

A **difference** is an existential over experiments — $\exists e$ with
$d^e \ge t$ — certified by a single witness experiment $e$. An **identity** is a
universal — $\forall e$, $d^e = 0$ — and no finite sample set confirms a universal
at a continuum of precision. The margin $t$ turns the two-sided question into a
finite one; the exact classification is the limit in which the demanded witness
can no longer be produced.

## 4. The certification radius

At $n$ samples the smallest margin that can be certified at error $\delta$ is

$$r(\delta) \asymp \big(\log(1/\delta)\,/\,n\big)^{1/2}.$$

So the certifiable content is a **ball of radius $r(\delta)$** around the truth in
separation space: the classification is pinned down only to that radius, which
shrinks like $n^{-1/2}$ and never reaches $0$. Law-surviving is the point in the
interior of the ball that is never pinned. This is the precise sense in which
"no finite amount of data certifies law-surviving."

## 5. Structural decidability closes the gap

If the effect algebras $(M_E, M_{E^\*})$ are *given* and the difference $\Delta$ is
supplied, the exact label is a finite rank computation costing **no samples**
(`docs/09` §4a). So the exact dichotomy is decidable **structurally**, never
statistically — the precise form of "channel-limited is a statement about the
data; law-surviving is a statement about the model."

## 6. Status

| Clause | Imported from | New here |
|---|---|---|
| §2(a,b) certifiable to margin | Le Cam two-point, Bretagnolle–Huber, Hoeffding/Chernoff | the *margin* formulation over the (E, E*) split |
| §2(c) singular limit | sharp-null non-testability (folklore) | the clean statement as the $t \to 0$ limit |
| §4 certification radius | — | the $\Theta(n^{-1/2})$ radius as the quantitative one-sidedness |
| §5 structural | `docs/09` §4a (rank test) | — |

The contribution is the **margin formulation**: the trichotomy is certifiable at
every positive margin at cost $\Theta(t^{-2})$ and non-certifiable only at zero
margin, with a certification radius $r(\delta) \asymp (\log(1/\delta)/n)^{1/2}$.

## 7. Parallel and open tracks

- **Nonlinear symmetry** (`docs/09` §7): extend $\mathfrak a(L)$ beyond $GL(n)$ —
  a criterion for nonlinear / algebraic symmetries. Kept **open**; untouched here.
- **Empirical protocol** (next): instantiate the certifier on a real probe family
  and an empirical measurement model.

**Back to** [README](../README.md).
