# 09 — Decidability, distortion, and the integrability of ambiguity

`docs/08` states the ambiguity dichotomy and its sharp clause (§4, the annihilator
$A_E = M_E^{\perp} \cap S$). This note develops the three results that clause
exposes — **when a continuous ambiguity is a symmetry** (§2), **how fast
distortion collapses a resolvable pair** (§3), and **what it costs to certify
which case holds** (§4). Their combination is a single statement (§5):

> **The classification of observational ambiguity is structurally decidable but
> statistically one-sided.**

The whole note is exact: every number is a `Fraction`.

## 1. Setup (recap of `08`)

- Worlds $\theta \in \Theta$; admissible experiments $E$ with completion $E^\*$;
  law map $L_E : \Theta \to \prod_{e\in E}\Delta(\Omega_e)$.
- Accessible effects span the real space $M_E$; $A_E := M_E^{\perp}\cap S$ is the
  annihilator inside the admissible state-difference space $S$; and
  $\theta_1 \approx_E \theta_2 \iff \rho_1-\rho_2 \in A_E$.
- The dichotomy is the nesting $A_{E^\*} \subseteq A_E$ (separated / channel-limited
  / law-surviving).

Throughout, $B_e(P) := \{R : \lVert R-P\rVert_{\mathrm{TV}} \le e\}$ is the
distortion ball.

## 2. Integrability: symmetry is group-relative, and computable

**The trap.** "The ambiguity is a group orbit" is *not* an intrinsic property.
Every constant-rank fiber is locally homogeneous: the rank theorem gives adapted
coordinates in which $L$ is a coordinate projection, the fiber is an affine
subspace, and the local translations in the adapted coordinates preserve $L$ and
act transitively on the fiber. So every fiber is a local orbit of *some*
(generally nonlinear) group, and any honest claim that a given unidentifiability
is a *symmetry* must name the group.

**The right question.** Fix a **declared** group $G$ acting on the world space
$\Theta$. Since $L$ is $G$-invariant exactly when $G$ preserves each fiber, the
fiber $F$ through $\theta$ is a single $G$-orbit iff $G$ acts transitively on
$F$:

> The ambiguity is a **symmetry** of $G$ iff $G$ acts transitively on the fiber;
> otherwise it is an **accidental** degeneracy relative to $G$.

**The computable case (linear $G = GL(n)$).** For the *declared* group the linear
group, transitivity is decided by the finite-dimensional **infinitesimal linear
symmetry algebra**

$$\mathfrak a(L) \;=\; \{\, A \in \mathfrak{gl}(n) \;:\; DL(\theta)\,A\,\theta = 0
\ \text{ for all } \theta \in \Theta \,\},$$

computed by a null-space (rank) calculation. The orbit of $\exp\mathfrak a(L)$
through $\theta$ has tangent space $\{A\theta : A \in \mathfrak a(L)\}$, so
*locally*

$$F \text{ is a single } GL(n)\text{-orbit through } \theta \iff
\dim\operatorname{span}\{A\theta : A \in \mathfrak a(L)\} = \dim F.$$

**Three kinds of law-surviving ambiguity** (exact instances, verified):

| $L$ | $\dim \mathfrak a(L)$ | fibers | reading |
|---|---:|---|---|
| $x^2+y^2$ | 1 | circles | **continuous** $GL(2)$ symmetry (rotation) |
| $xy$ | 1 | hyperbolas | **continuous** $GL(2)$ symmetry (scaling) |
| $(\eta+\delta,\ \eta\delta)$ | 0 | $\mathbb Z/2$ orbits | **discrete** symmetry (the swap) |
| $x^3+y^3$ | 0 | cubic curves | no **linear** symmetry |

Only the first two earn the word "symmetry" *within* $GL(n)$.

> **Not "no symmetry" — no *linear* symmetry.** $\mathfrak a(L)=0$ is a statement
> about $GL(n)$ only, and a non-linear continuous symmetry may still exist. For
> example $L(x,y)=y-x^3$ has $\mathfrak a(L)=0$, yet
> $(x,y)\mapsto(x+t,\;y+3x^2t+3xt^2+t^3)$ preserves $L$ — a genuine one-parameter
> symmetry that is *quadratic*, hence outside $GL(2)$. Indeed, by the trap above,
> *every* rank-one fiber is locally an orbit of a (generally non-linear) tangent
> flow. So "no linear symmetry" is only ever accidental **relative to the declared
> group**.

**Remark (finite-dimensional transverse structure).** A stronger, *transverse*
condition is that the kernel distribution be a **Lie foliation** (Molino): it
admits a frame with **constant** structure functions
$[X_i,X_j] = \sum_l c^l_{ij} X_l$, with the structure tensor — and in codimension
one the Godbillon–Vey class — as obstruction. This is *not* the same as leaf
homogeneity (which is automatic for every fiber); it asks that the *transverse*
geometry be a finite-dimensional Lie group. It is the natural home of a genuine
finite-dimensional gauge structure.

**Status.** The $\mathfrak a(L)$ computation is standard Lie theory. The *new*
content is the reading: **symmetry is group-relative** — the intrinsic question
is ill-posed, because every fiber is already a local pseudogroup orbit — and the
continuous / discrete / accidental trichotomy that follows.

## 3. Distortion: the collapse is sharp at $2e = d$, with a matching rate

Fix laws $P,Q$ on a finite outcome set, $d := \lVert P-Q\rVert_{\mathrm{TV}}$, and
per-law TV distortion $e$. Consider the composite hypotheses
$B_e(P)$ vs $B_e(Q)$ under equal priors.

**Proposition 3.1 (minimax separation).** The minimax total variation between the
two balls is

$$\tilde d(e) \;=\; \min_{P' \in B_e(P),\, Q' \in B_e(Q)} \lVert P'-Q'\rVert_{\mathrm{TV}}
\;=\; \max(d - 2e,\, 0).$$

*Proof.* Lower: $\lVert P'-Q'\rVert \ge d - \lVert P-P'\rVert - \lVert Q'-Q\rVert \ge d-2e$
by the triangle inequality, and $\ge 0$ trivially. Upper (tightness): for
$e \le d/2$ take the segment points $P' = P + \tfrac{e}{d}(Q-P)$,
$Q' = Q + \tfrac{e}{d}(P-Q)$; then $\lVert P'-P\rVert = \lVert Q'-Q\rVert = e$ and
$\lVert P'-Q'\rVert = (1 - 2e/d)\,d = d-2e$. For $e \ge d/2$ the midpoint
$\tfrac12(P+Q)$ lies in both balls, so the minimax distance is $0$. $\square$

**Theorem 3.2 (collapse rate).** Let $n^*(d,e,\delta)$ be the least $n$ admitting a
test of min-max error $\le \delta$. Then

1. **(Collapse)** $n^* = \infty \iff 2e \ge d$ (equivalently, $B_e(P) \cap B_e(Q) \neq \varnothing$).
2. **(Upper)** for $2e < d$: $n^* = O\!\big((d-2e)^{-2}\log(1/\delta)\big)$.
3. **(Lower)** for $2e < d$: $n^* = \Omega\!\big((d-2e)^{-2}\log(1/\delta)\big)$.

Hence $n^*(d,e,\delta) = \Theta\!\big((d-2e)^{-2}\log(1/\delta)\big)$, and the
threshold $2e = d$ is exact.

*Proof.*
1. If the balls intersect at $R$, the adversary sets $P'=Q'=R$: both hypotheses
   induce $R^{\otimes n}$; no test beats $1/2$. If disjoint, Prop. 3.1 gives
   $\tilde d > 0$.
2. Disjoint convex sets admit a separating functional $v$ with
   $v\cdot(P'-Q') \ge \tilde d' > 0$ for all $P'\in B_e(P), Q'\in B_e(Q)$, with
   $\tilde d' \ge c\,\tilde d$. Estimate $\hat m_n = \tfrac1n\sum_i v(X_i)$;
   Hoeffding gives $|\hat m_n - v\cdot P'| \le t$ with probability
   $1-2e^{-2nt^2}$. Threshold at the midpoint of the two intervals; with
   $t = c\tilde d/4$ the error is $\le 2e^{-n c^2 \tilde d^2/8}$, i.e.
   $n = O(\tilde d^{-2}\log(1/\delta))$.
3. Le Cam's two-point method at the extremal pair $P',Q'$ of Prop. 3.1 plus
   Bretagnolle–Huber: any test has error
   $\ge \tfrac12\big(1 - \lVert P'^{\otimes n} - Q'^{\otimes n}\rVert_{\mathrm{TV}}\big)$,
   and $\lVert P'^{\otimes n} - Q'^{\otimes n}\rVert_{\mathrm{TV}}
   \le \sqrt{1-(1-H^2)^n}$ with $H^2$ the squared Hellinger affinity. Since
   $H^2(P',Q') \asymp \tilde d^2$ for small $\tilde d$, error $\le \delta$
   forces $n \ge \log\frac{1}{4\delta(1-\delta)}\big/\log\frac{1}{1-H^2}
   = \Omega(\tilde d^{-2}\log(1/\delta))$. $\square$

**Exact instance.** Distinguishing $\mathrm{Bin}(\tfrac12)$ from
$\mathrm{Bin}(\tfrac14)$ has $d = \tfrac14$; the exact optimal (Bayes) error first
drops to $\le \tfrac1{20}$ at $n^* = 39$ — against the heuristic
$\log(1/\delta)/d^2 = 48$, same order with constant $\approx 0.81$. Distortion at
$e = \tfrac18 = d/2$ collapses it ($\tilde d = 0$); at $e = \tfrac1{16}$ the
effective separation is $\tilde d = \tfrac18$.

**Per-outcome ($\ell^\infty$) variant (exact).** If instead
$\lVert R-P\rVert_\infty \le e$, write $\Delta := P - Q$ and

$$A_+ = \!\!\sum_{\Delta_i > 0}\!\! \min(2e, \Delta_i), \qquad
A_- = \!\!\sum_{\Delta_i < 0}\!\! \min(2e, -\Delta_i).$$

Then the minimax separation is $\tilde d_\infty(e) = d - \min(A_+, A_-)$, and the
balls collide iff $2e \ge \lVert P-Q\rVert_\infty$.

*Proof.* For any admissible pair, $z := \Delta - (P'-Q')$ satisfies
$\sum_i z_i = 0$ (both laws are normalized) and $|z_i| \le 2e$, so
$\lVert P'-Q'\rVert_1 \ge \lVert\Delta\rVert_1 - \sum_i|z_i|$; the balance
constraint $\sum_i z_i = 0$ caps $\sum_i|z_i|$ at $2\min(A_+,A_-)$. Moving each
component toward the other by $\min(2e, |\Delta_i|)$ on the smaller side attains
it. $\square$

Consequently the **erosion rate is $2\min(k_+,k_-)$**, where $k_\pm$ counts the
positive / negative components of $\Delta$ (for $2e$ below the smallest
$|\Delta_i|$). So the headline "rate two" of `docs/07` holds exactly for a
**one-sided** separation ($\min(k_+,k_-)=1$) — every binary law and any monotone
shift — while a *spread* separation erodes faster; the TV-ball model (Prop. 3.1)
has rate two unconditionally.

## 4. Certification: the one-sided decidability theorem

The classification problem: given a pair of worlds, decide
*separated* / *channel-limited* / *law-surviving*.

**(a) Structural decidability.** Given the accessible and completed effect spans
$M_E, M_{E^\*}$ and the difference $\Delta := \rho_1-\rho_2$ as input, the
classification is a **finite rank computation**:

$$\text{separated} \iff \Delta \notin A_E, \qquad
\text{channel-limited} \iff \Delta \in A_E \setminus A_{E^\*}, \qquad
\text{law-surviving} \iff \Delta \in A_{E^\*}.$$

Cost $O(n^3)$ exact arithmetic; **no experiments**. So with the model in hand the
trichotomy is *decidable*.

**(b) Statistical certifiability.** Suppose only samples are available.

**Theorem 4.1 (one-sided decidability).**
1. "Separated" and "channel-limited" are **certifiable**: with
   $n = \Theta(\tilde d^{-2}\log(1/\delta))$ samples (Theorem 3.2) a test outputs
   the correct resolvable label with probability $\ge 1-\delta$.
2. "Law-surviving" is **not finitely certifiable**: for every finite $n$ and every
   $\delta < \tfrac12$ there is a channel-limited pair whose $n$-sample min-max
   error exceeds $\delta$. No test separates the label "law-surviving" from
   "channel-limited with an arbitrarily small completion-component."
3. Consequently law-surviving is decidable **only structurally** — a certificate
   must name the algebra $M_{E^\*}$ (equivalently the annihilator $A_{E^\*}$).

*Proof of (2).* Let the channel-limited difference be $\Delta_\varepsilon$ with
completion-component $\varepsilon > 0$, so that $\Delta_\varepsilon \to \Delta_0$
(a law-surviving difference) as $\varepsilon \to 0$. For fixed $n$ the induced
laws satisfy $\lVert P_\varepsilon^{\otimes n} - P_0^{\otimes n}\rVert_{\mathrm{TV}}
\to 0$ (continuity, bounded by Bretagnolle–Huber), and
$P_0^{\otimes n} = Q_0^{\otimes n}$ exactly. Hence any test's min-max error on the
pair $\{P_0, P_\varepsilon\}$ is
$\ge \tfrac12(1 - \lVert P_\varepsilon^{\otimes n} - P_0^{\otimes n}\rVert_{\mathrm{TV}})
\to \tfrac12$ as $\varepsilon \to 0$. So no fixed-$n$ test certifies the
law-surviving label against all nearby channel-limited alternatives. $\square$

The asymmetry is structural: **channel-limited ambiguity is a statement about the
data; law-surviving ambiguity is a statement about the model.** This is the
rigorous form of "absence of evidence is not evidence of absence."

**(c) Rank certification from noisy data.** If the effect span itself must be
learned, certifying its dimension (hence $A_{E^\*}$) is a rank-estimation problem:
exact rank recovery needs a spectral gap $g$ and
$n = \Theta(g^{-2}\log\dim)$ samples per effect coordinate — again finite for the
resolvable structure, vacuous for the exact-zero claim.

## 5. The unifying statement

2, 3, and 4 assemble into:

> **One-sided decidability of observational ambiguity.** With the model (effect
> algebra) given, the trichotomy is decidable by an $O(n^3)$ rank computation and
> costs no experiments. From data alone it is decidable in *one direction*: the
> resolvable labels (separated, channel-limited) are certifiable at
> $\Theta(\tilde d^{-2}\log(1/\delta))$ samples, while the unresolvable label
> (law-surviving) is certifiable only by structure. The boundary between the two
> directions is the collapse threshold $2e = d$ of Theorem 3.2.

## 6. Status: what is imported, what is new

| Clause | Imported from | New here |
|---|---|---|
| §2 integrability | linear symmetry algebras; Lie foliations (Molino) as the transverse refinement | the reading *symmetry is group-relative* + the continuous / discrete / accidental trichotomy |
| §3 collapse rate | Le Cam two-point, Bretagnolle–Huber, Hoeffding/Chernoff | the sharp threshold $2e=d$ in the identifiability setting; the $\ell^\infty$ refinement |
| §4 one-sided decidability | sharp-null non-testability (folklore) | the **trichotomy packaging**: data vs structure, with the rank test as the structural oracle |

No clause is a theorem new to mathematics. The claimable contribution is the
**assembly and the decidability framing** — a rigorous statement of *when
ambiguity is refutable by data and when it is not.*

## 7. Where a genuinely new theorem could still live

- **Nonlinear symmetry** (§2): extend $\mathfrak a(L)$ (linear symmetries) to
  *algebraic / Lie-group* symmetries of the law map — a criterion for when an
  ambiguity is a symmetry of a declared nonlinear group.
- **Intrinsic symmetry, if any** (§2): the intrinsic question is ill-posed
  because every fiber is a local pseudogroup orbit; is there a canonical minimal
  group (analogue of a holonomy group) whose transitivity *is* intrinsic?
- **Exact collapse constant** (§3): now **settled** for the separation — the
  collision threshold ($2e \ge \lVert P-Q\rVert_\infty$, resp. $2e \ge d$ for TV)
  and the erosion rate ($2\min(k_+,k_-)$, resp. $2$) are closed-form and
  implemented (`ambiguity.l_inf_separation`, `l_inf_erosion_rate`). What remains
  open is the exact **error-exponent constant** $c^\*$ in
  $n^\* = (c^\* + o(1))\log(1/\delta)/\tilde d^2$ — the minimax Chernoff
  information of the two balls, transcendental and with no closed form in general.
- **Certification complexity** (§4): prove a lower bound showing that *no*
  structure-free test certifies law-surviving — turning the folklore into a
  theorem with a formal model of "certifying test."

**Back to** [README](../README.md).
