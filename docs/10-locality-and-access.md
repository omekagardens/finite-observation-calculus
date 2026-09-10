# 10 — Locality and access

The dichotomy of `docs/08` is usually read as a statement about *ambiguity*. Read
as a statement about **access**, it does something sharper: it refuses the binary
"local versus global." This note makes that reading precise, and separates the
part that is exactly computable from the part that is a geometric analogy.

## 1. Access is two axes, not one

Let $E$ be a declared family of **accesses** (local probes) and $E^\*$ its
**closure** under composition and record-retention (global access). The three
cases of `08` are then:

| case | reading |
|---|---|
| separated | reachable by local access already |
| channel-limited | a **scope** failure — reachable by `E*` (a better/global probe) |
| law-surviving | **not** a scope failure — unreachable by `E*` |

So the classical local/global axis is the *channel-limited* axis. Law-surviving
is **orthogonal** to it. The usual binary

$$\{\text{local},\ \text{global}\}$$

is replaced by a **$2\times 2$**: $\{\text{local},\text{global}\} \times
\{\text{observable},\text{unobservable}\}$, and the cell that has no name in the
usual framing — *globally accessible but unobservable* — is exactly
law-surviving ambiguity.

**"Global" is relational.** $E^\*$ is the closure of the *declared* admissible
operations, so global access is not a privileged vantage point; it is whatever
that closure reaches. Law-surviving is *defined* as lying outside the closure.
Like question-relative summaries (`04`) and group-relative symmetry (`09` §2),
globality is relative to a declared frame.

## 2. The exact core: the annihilator is the nonlocal content

Recall (`08` §4) that the invisible sector of an accessible effect span $M_E$ is
the annihilator $A_E = M_E^{\perp} \cap S$, with
$\dim A_E = \dim S - \dim M_E$. Make $M_E$ a **local** algebra and $A_E$ becomes
large — and its content is precisely the *nonlocal* structure of the world.

**Exact instance (two qubits; Hermitian observables, $\dim = 16$, traceless
$\dim = 15$).** Take one-body (**local**) access,
$M_{\mathrm{loc}} = \operatorname{span}\{X\!\otimes\! I, Y\!\otimes\! I,
Z\!\otimes\! I, I\!\otimes\! X, I\!\otimes\! Y, I\!\otimes\! Z\}$, $\dim = 6$.
Then

$$\dim A_{\mathrm{loc}} = 15 - 6 = 9,$$

and the annihilator is *exactly* the **two-body correlation space**
$\{X,Y,Z\}\otimes\{X,Y,Z\}$ — the entanglement/signalling content. Admitting
*pair* (joint) access makes the family tomographically complete
($\dim(M_{\mathrm{loc}} \cup \{\text{pairs}\}) = 15$, $A = 0$). So:

- the two-body correlations are **channel-limited**: local access misses them,
  joint access resolves them;
- if a **superselection rule forbids joint access**, the same correlations become
  **law-surviving** — invisible at every admissible scope.

This is the operability of the slogan: *what a local observer cannot see is,
by construction, the global (nonlocal) structure.* It is the
identifiable-content version of the algebraic-QFT picture, where
spacelike-separated algebras lie in each other's commutants and a superselection
charge lives in the commutant, so **local observables are structurally blind to a
global charge.**

*One-qubit instance (`08`, `03`):* accessible $\{Z\}$ leaves $A = \operatorname{span}\{X\}$
(the coherence), channel-limited once $X$ is admitted.

## 3. The geometric face: local homogeneity is free, global is holonomy

The sharpest locality/global phenomenon is structural, and it is why §2 of `09`
had to be corrected.

**Local symmetry is automatic (exact).** By the rank theorem, for any
$L:\Theta\to\mathbb R^m$ of constant rank near $\theta_0$ there are adapted
coordinates in which $L$ is a coordinate projection; the fiber is an affine
subspace and the local translations *in those coordinates* preserve $L$ and act
transitively on it. So **every** fiber is a local orbit of a local group; local
homogeneity carries no information.

**Global symmetry is not (the obstruction is monodromy).** The local actions need
not patch into a single global orbit. The failure is measured by the **holonomy**
of the foliation — the pseudogroup of local transverse identifications obtained
by going around loops in the leaves. Discrete example: the projection of the
**Möbius band** onto its circle has fiber an interval (locally a translation
orbit, exactly as in a trivial product), yet the bundle is nontrivial — its
monodromy is the flip $x\mapsto 1-x$. Local data (a trivial neighborhood) cannot
distinguish a cylinder from a Möbius band; the global invariant is the monodromy.

Stated as a principle: **local structure never determines global structure, and
the deficiency is measured by holonomy.** The same object appears as the Berry /
geometric phase (holonomy of a connection), the Wilson loop (gauge theory), and
Gauss–Bonnet (local curvature integrating to global topology). In machine
learning it is the fact that a manifold's local charts do not determine its
global topology.

The **operational**, exactly-checkable content of this section is the
$\mathfrak a(L)$ trichotomy of `09` §2 (continuous / discrete / accidental) —
computed by a rank calculation from the law map's derivatives.

## 4. Epistemology: differences are local, identities are global

The one-sided decidability theorem (`09` §4) is a locality statement about
*knowledge*:

- a **difference** ($\tilde d > 0$) is a local fact — a single witness, finitely
  many experiments, certifies it;
- an **identity** ($\tilde d = 0$) is a global fact — **no finite amount of local
  data confirms it**; only the structural certificate does.

And `09` §3 sharpens the fragility: distortion erodes local access at **rate
two**, so local distinctions fold into the global-only class under enough shift.
*Local access is fragile; structural access is not.*

## 5. What is refined, and what is challenged

**Refined, not overturned.** Locality is not wrong; the *binary* is. The genuine
addition is the third category — inaccessible even globally — and the observation
that "global" is itself a closure, hence relative.

**Challenged — three assumptions:**

1. **"Global access is sufficient."** It is not. $E^\*$ has a boundary; there is
   a real outside (law-surviving), and no amount of scope closes it.
2. **"A negative local probe means absence"** (the ML / interpretability one). A
   failed local probe is ambiguous in exactly two ways: channel-limited (get a
   better or joint probe) and law-surviving (nothing works). Current evaluation
   and probing implicitly collapse the two; the calculus says a negative result
   carries *two* meanings.
3. **"The global state is the objective description."** Records are local, and
   the global description can be ambiguous in a way no local record fixes —
   which is precisely law-surviving ambiguity (relational / Wigner's-friend
   territory).

## 6. The relativity chain

The repository's three relativity moves — question-relative sufficiency (`04`),
group-relative symmetry (`09` §2), access-class-relative globality (`10` here) —
are one pattern: **there is no absolute summary, no absolute symmetry, and no
absolute global.** "Local versus global access" is the visible face of that
relativity, and the calculus's substantive thesis is stronger than
$\text{local} < \text{global}$:

> There is a realm that is neither local nor global — it is *unavailable* — and
> distinguishing it from the merely-not-yet-global is the difference between
> designing a better experiment and chasing information that does not exist.

**Back to** [README](../README.md).
