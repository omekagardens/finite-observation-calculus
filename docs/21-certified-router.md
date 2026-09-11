# 21 — A certified router, and routing theorems

`docs/20` certifies the *nodes* of a regime model and shows the routing *type*
matters — but never certifies the **router**. This note supplies it, and states
the routing theorems the calculus yields.

## 1. The router is a declared policy

A router maps an input to a regime by reading a **declared record** (a score).
It is subject to the discipline of `docs/01` §2: it may read only declared
inputs — a router reading an *undeclared* record is uncertifiable. Write the
router as a linear score

$$s(x) = w \cdot x, \qquad \text{route ``A''} \iff s(x) > 0,$$

with **routing margin** $|s(x)|$ = distance to the boundary.

## 2. Certified routing, and the router's bit budget

An input routes **unambiguously** iff $|s(x)| \ge t$ (the margin); below $t$ the
routing is *ambiguous* — a declared property, not a failure.

The router is a small model, so it truncates like any other: the score distortion
from a grid of quantum $1/n$ is bounded, and **rate two** (`docs/09`, `docs/19`)
says a distortion $\delta$ needs a margin $2\delta$. So the router has its own
bit budget $\approx \log_2(2L/t)$, **added to** the node budgets.

## 3. Routing theorem 1 — the routing-type gap

The router's *type* is how it combines experts: **hard** (route to one; the choice
is a *record*) or **soft** (superpose). By `docs/05`:

$$\text{soft} - \text{hard} \;=\; \sum_{x \ne y} M_x\,(\cdot)\,M_y^\top ,$$

a **sum of maps** versus a **recombination** — different transformations.

## 4. Routing theorem 2 — when the type is immaterial

The gap vanishes iff $M_x\,\rho\,M_y^\top = 0$ for all $x \ne y$: **the router
type is immaterial exactly when the input carries no coherence between the
experts' ranges.** Consequently:

- **orthogonal experts + classical (diagonal) input** → the type does not matter;
- **orthogonal experts + coherent input** → it does (a colliding-inputs witness);
- **overlapping experts** (e.g. the non-projective `docs/05` experts) → it does,
  even for classical inputs.

So a meta-model must **declare its routing type**, and hard routing is a valid
replacement for soft **only** in the classical / orthogonal case — otherwise
`docs/05`'s obstruction applies.

## 5. Routing theorem 3 — the replacement criterion

Theorem 2 says when the type is immaterial *globally*. The sharper,
decision-relevant question is **source-relative** (`docs/05` §3): is hard routing
a valid **replacement** for soft *for a declared downstream*?

> **Replacement criterion.** Hard routing is a valid replacement for soft for a
> downstream family $\{E\}$ iff every downstream effect is **blind to the gap**
> $S - H$: $\operatorname{Tr}\big(E\,(S(\rho) - H(\rho))\big) = 0$ for all $E$,
> $\rho$.

- a downstream that only **counts** (reads $I$) is blind — the replacement is valid;
- a downstream that reads $Z$ is **not** — the replacement fails.

Failure is certified by a **colliding-inputs witness** (`docs/05` §4): two inputs
hard routing *merges* that soft routing *separates* — $|+\rangle$ and $|-\rangle$,
which $H$ both send to $I/2$ while $S$ sends to distinct states. That is an
*impossibility proof* (no operation on the hard output reproduces both required
outputs), not the failure of one candidate.

## 6. Routing theorem 4 — the boundary is ambiguous

An input with margin $< t$ is ambiguous, and the ambiguity is exactly the
taxonomy of `docs/08`:

- **channel-limited** — a richer declared score separates the regimes at that
  input: build a finer router;
- **law-surviving** — no score separates them: the regimes genuinely overlap on
  the declared record, and the routing is *declared*, never certified.

## 7. Composition

Total precision $=\;$ router bits $+\sum_r$ node bits, and the meta-verdict is the
nodes' verdicts composed with the router's. This closes `docs/20`.

## 8. The demonstration

`foc.router.router_report`:

| input | score $s$ | margin | certified route ($t=1/2$) |
|---|---:|---:|---|
| $(3,1)$ | $1$ | $1$ | **A** |
| $(1,3)$ | $-9/5$ | $9/5$ | **B** |
| $(1/2,1/2)$ | $-1/10$ | $1/10$ | **ambiguous** |

Router precision at $t=1/2$: coarsest grid $4$, **3 bits**. Routing type:
orthogonal/classical → immaterial; orthogonal/coherent → material; overlapping/
classical → material.

Replacement criterion (`foc.router.replacement_report`): counting downstream →
valid; $Z$-reading downstream → invalid, with the colliding-inputs witness.

## 9. Status

Implemented as `foc.router` (`score`, `route`, `routing_margin`,
`certified_route`, `router_precision`, `routing_type_gap`, `hard_routing`,
`soft_routing`, `replacement_holds`, `collision_witness`, `replacement_report`,
`router_report`) and run in demo section 19.

**Back to** [README](../README.md).
