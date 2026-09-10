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

## 2. Integrability: ambiguity is a symmetry only when it is homogeneous

Let $L : \Theta \to \mathbb R^m$ be smooth of constant rank $r$ on an open
$U \subseteq \mathbb R^n$. Its fibers are the leaves of the involutive
distribution $D := \ker DL$ (involutive because it is the tangent bundle of the
level sets; equivalently, Frobenius holds automatically).

**Theorem 2.1 (integrability criterion).**
1. Each leaf is *locally homogeneous* — an orbit of a local Lie-group action —
   iff $D$ is a **Lie foliation**: there is a local frame $X_1,\dots,X_k$ of $D$
   with $[X_i,X_j] = \sum_l c^l_{ij}\,X_l$ for **constants** $c^l_{ij}$.
2. The leaves are *globally* orbits of a Lie group iff (1) holds with trivial
   monodromy and each $X_i$ complete.
3. If $D$ is not a Lie foliation, the ambiguity is a genuine foliation with
   non-homogeneous leaves: a continuous ambiguity that is **not** a symmetry.

*Proof sketch.* A group orbit is homogeneous, and the fundamental vector fields
of a connected Lie group are complete, span the tangent space at each point, and
close under bracket with structure *constants*. Conversely, a frame closed with
constant structure generates a finite-dimensional Lie algebra $\mathfrak g$;
Palais' theorem integrates it to a local Lie-group action, and completeness +
trivial monodromy globalize it. If the structure functions are not constant, the
generated (pseudo-)group is infinite-dimensional — the leaf is a leaf, not an
orbit. $\square$

**Corollary 2.2.**
- $\operatorname{rank} D = 1$: always locally homogeneous — a single vector
  field's flow acts transitively on each integral curve.
- **Linear** $L(\theta) = A\theta$: the fiber is the affine space
  $\theta_0 + \ker A$, a translation orbit (abelian group). So the
  group-versus-foliation question is *inherently nonlinear*.
- The geometry family of `08`/`03`, $L(\eta,\delta)=(\eta+\delta,\eta\delta)$,
  has $D=0$: a **discrete** ambiguity (the $\mathbb Z/2$ swap) — a finite orbit.

**Obstruction.** The failure of (1) is measured by a cohomological invariant of
the foliation (the structure tensor; in codimension one, the **Godbillon–Vey
class**).

**Status.** The mathematics is classical — this is the theory of **Lie
foliations** (Molino) and the structure-functions invariant. The *new* content is
the reading: **gauge symmetry = the homogeneous case**, so "is this an
unidentifiability by symmetry?" becomes the checkable question "are the structure
functions constant?" A continuous ambiguity need not be a symmetry.

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

**Per-outcome ($\ell^\infty$) variant.** If instead
$\lVert R-P\rVert_\infty \le e$, the same segment argument gives
$\tilde d = \max\!\big(d - 2e\,(d/\lVert P-Q\rVert_\infty),\,0\big) \ge \max(d-2e,0)$.
So the repository's bound $D_e = \max(D-2e,0)$ is always *valid* and is exact
whenever $d = \lVert P-Q\rVert_\infty$ (in particular for binary outcomes).

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
| §2 integrability | Lie foliations (Molino), structure functions, Godbillon–Vey | the identification *gauge symmetry = homogeneous case* |
| §3 collapse rate | Le Cam two-point, Bretagnolle–Huber, Hoeffding/Chernoff | the sharp threshold $2e=d$ in the identifiability setting; the $\ell^\infty$ refinement |
| §4 one-sided decidability | sharp-null non-testability (folklore) | the **trichotomy packaging**: data vs structure, with the rank test as the structural oracle |

No clause is a theorem new to mathematics. The claimable contribution is the
**assembly and the decidability framing** — a rigorous statement of *when
ambiguity is refutable by data and when it is not.*

## 7. Where a genuinely new theorem could still live

- **Integrability from structure** (§2): derive the constancy of the structure
  functions from the *observable algebra* rather than importing it from foliation
  theory — a purely algebraic criterion for homogeneous ambiguity.
- **Exact collapse constant** (§3): replace $\Theta$ by the exact minimax constant
  for the $\ell^\infty$-ball model.
- **Certification complexity** (§4): prove a lower bound showing that *no*
  structure-free test certifies law-surviving — turning the folklore into a
  theorem with a formal model of "certifying test."

**Back to** [README](../README.md).
