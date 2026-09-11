# 22 — Internal certification: self-consistency and closed growth

A model that reinforces on its own outputs is not **externally** grounded — but it
is **internally** certifiable. This note makes the internal notion precise: it is
closed over declared interfaces, and self-reinforcement has a local fixed-point
theorem with a local instability certificate.

## 1. Two notions of certification

- **External**: relative to the *world*. A self-generated record is ungrounded
  here (`docs/01` §2 — declared records only). This is what a feedback loop cannot
  supply.
- **Internal**: relative to **declared interfaces**. A node reading another node's
  output is certified *given* that interface. This is closed and local.

The mistake is to apply the external rule to an internal composition. Node-to-node
edges are declared, so the internal certificate survives self-reinforcement.

## 2. Internal certification is closed

It is built from pieces already proved:

- **Composition** (`docs/20` §5): node verdicts compose, and the global annihilator
  is the **intersection** of node annihilators.
- **Replacement** (`docs/21` §5): "is hard routing a valid replacement for soft for
  the declared downstream?" is a purely **local** question with a local certificate.

So an edge `A → B` is certified locally, and the whole is certified by composing
the edges — no external data required.

## 3. Self-consistency: the fixed-point theorem

Self-reinforcement feeds a model's own **hard-routed** outputs back as inputs. So:

> **Self-consistency.** The model is stable under self-reinforcement **iff it is a
> fixed point of its own replacement criterion** — hard routing is a valid
> replacement for soft **for the model's own downstream and its own outputs**.

If it is a fixed point, reinforcing on hard decisions does not move the soft
behavior: self-reinforcement is *stable*, and the certificate
`self_consistent(experts, downstream, states)` is local and internal.

## 4. The instability certificate

If it is **not** a fixed point, the failure is not a vague drift: it is a
**colliding-inputs witness** (`docs/05` §4, `docs/21` §5) — the exact inputs where
the model, reinforcing on its own hard decisions, *forgets coherence*. Instability
is a **local replacement failure**, not global ungroundedness.

## 5. Closed growth is monotone

Because the composed invisible sector is the annihilator of the **union** of probe
sets (`docs/20` §5), adding nodes grows the union and can only **shrink** the
annihilator: *more regimes can only reduce law-surviving ambiguity.* Growth never
blinds you to something a node could already see.

## 6. The demonstration

`foc.internal.internal_report`:

| check | result |
|---|---|
| stable node (orthogonal experts, classical) | `self_consistent` = **True** |
| unstable node (overlapping experts, coherent) | `self_consistent` = **False** |
| instability witness $(\lvert+\rangle, \lvert-\rangle)$ | `no_replacement` = **True** |
| invisible sector: local node / pairs node / composed | **9 / 6 / 0** |

The last row is closure in action: the two nodes compose to a **fully visible**
whole (`0`), each alone blind to part of it.

## 7. What internal certification is — and is not

- **Is**: structural soundness — correct composition, non-degenerate routing,
  precision floors, a fixed-point/instability certificate.
- **Is not**: external validity. Internal certificates are **conditional** (given
  the interfaces); a model can be internally perfect and externally wrong.

## 8. Status

Implemented as `foc.internal` (`self_consistent`, `instability_witness`,
`compose_annihilator_dim`, `internal_report`) and run in demo section 20.

**Back to** [README](../README.md).
