# 20 — Regime composition: transformers as certified nodes

Treat several transformers as **nodes** of a larger *regime* model — each node
handling a declared regime, a router selecting among them. Two things follow from
the calculus, both exact:

1. **Per-regime precision refines the bit budget.** A regime with a coarse margin
   tolerates a coarse truncation grid (`docs/19`), so the aggregate is the *sum*
   over regimes, not the max.
2. **Routing is a record**, and **hard routing (sum of maps) vs soft routing
   (recombination) are different maps** (`docs/05`): the certified global law
   depends on the routing type.

## 1. Regimes are declared contexts

The calculus never certifies absolutely: sufficiency is question-relative
(`docs/04`) and observability is access-relative (`docs/08`, `docs/10`). A
**regime** is exactly such a declaration — a sub-population, task, or region with
its own **margin** $t_r$ and probe family. So each node is certified *for its
regime* by the **same theorem**: nothing new is needed.

## 2. Per-node certification, and the bit budget

Per node, `docs/19` gives a bit budget set by the regime margin. Because the safe
grid is the coarsest whose *certified* separation `D − 2e` still meets the margin
(rate two, `docs/09`):

$$\text{modular bits} \;=\; \sum_r b_r \;\; \text{vs} \;\;
\text{monolithic bits} \;=\; R \cdot \max_r b_r .$$

They are equal iff the margins are homogeneous. With **separate nodes** the
savings are real; a monolithic model must carry the *finest* precision
everywhere.

## 3. The demonstration

`foc.regime.regime_precision` runs the exact transformer (`docs/18`) and finds the
coarsest certified grid per declared margin:

| regime margin $t_r$ | coarsest grid | bits |
|---:|---:|---:|
| 0.25 | 16 | 5 |
| 0.30 | 16 | 5 |
| 0.40 | 16 | 5 |
| 0.48 | 256 | 9 |

Modular (sum) = **24** bits; monolithic (finest everywhere) = **36** bits — a
~33% saving, from regimes with different margins. Homogeneous margins would give
no saving.

## 4. Routing is a record (the sharp part)

The router's choice — *which node fires* — is a **record** (`docs/01`). Discarding
it (**hard** routing) is a **sum of maps** (classical forgetting); keeping the
amplitudes (**soft** routing) is a **recombination** (`docs/05`). `foc.regime.
routing_laws` shows they differ on the *same* experts:

$$\text{hard} = \begin{pmatrix} 1/2 & 0 \\ 0 & 1/2 \end{pmatrix}
\quad\neq\quad
\text{soft} = \begin{pmatrix} 49/50 & -7/50 \\ -7/50 & 1/50 \end{pmatrix}.$$

So a meta-model's certification **must declare its routing type**: hard and soft
give *different global laws* even when the experts agree. This is `docs/05`'s
obstruction, restated for architecture.

## 5. How the certification composes

- The meta-model's accessible effects are the **union** of the nodes' probe
  families (plus the router's); the **global annihilator** is their
  **intersection** — the sector where *every* node is blind, i.e. the certified
  invisible content (`docs/08` §4).
- The **global margin** is a declared function (min / tuple / sum) of the node
  margins; the global bit budget follows.
- Each node is a **local observer**; the meta-model is **global** access — a
  locality structure (`docs/10`), with routers as the new probes.

## 6. Caveats

- **Parameter cost.** Modularity multiplies parameters; the honest comparison is
  `bits × params`, and the saving is real only when the margin spread outweighs
  the extra parameters.
- **Declare the routing type** (hard vs soft) and the **margin composition**;
  `docs/11` says a regime's margin is *certified*, never exact.
- **Declared records only.** A router reading an *undeclared* record violates the
  discipline of `docs/01` §2 and voids the certification.

## 7. Status

Implemented as `foc.regime` (`coarsest_safe_grid`, `regime_precision`,
`routing_laws`) and run in demo section 18.

**Back to** [README](../README.md).
