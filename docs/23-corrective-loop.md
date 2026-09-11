# 23 — The corrective loop: localizing an external failure

Internal certificates (`docs/22`) are the fast, closed, conditional layer; the
external verdict is the scarce grounding layer. This note shows the calculus turns
an external failure into a **localized, bounded, refinement-safe** correction —
rather than a global retrain.

## 1. The split: speed vs validity

- **Internal**: cheap, closed, local, *conditional* — structural soundness in
  rank arithmetic (`docs/22` §7).
- **External**: the scarce signal that only the world supplies — and the layer a
  self-reinforcing model cannot generate.

The loop: run the internal layer continuously, the external layer rarely, and let
each external verdict **propagate internally** as a correction.

## 2. Localization — which node

A node **cannot** be responsible for a failing feature it is **blind to** — the
feature lies in its annihilator (`docs/08` §4). So responsibility is confined to
the nodes whose probes *can see* the feature:

$$\text{blame}(\Delta) = \{\, \text{node} \;:\; \Delta \notin A_{\text{node}} \,\}.$$

That is a hard, checkable filter.

## 3. Localization — which edge

An edge failure implicates exactly the edges whose **gap** the failing downstream
**reads** (`docs/21` §5): the edge is blamed iff `Tr(E (S − H)) ≠ 0` for some
downstream effect `E` and state. A blind downstream implicates nothing.

## 4. Re-certification, and safety in one direction

After a correction the model must be re-certified. By monotonicity (`docs/22` §5):

- **refinement** corrections (adding probes) *shrink* the global annihilator —
  **always safe**;
- **coarsening** corrections can *increase* it — risky.

So a correction is **accepted** iff it is refinement-safe (annihilator does not
grow) **and** the external verdict holds. Because each node's certificate is
independent given declared interfaces, the rest of the model is provably
unaffected — the blast radius is exactly the localization.

## 5. The demonstration

`foc.corrective.corrective_report`:

| check | result |
|---|---|
| failing 2-body feature $Z\!\otimes\! Z$ | blamed on **pairs** |
| failing 1-body feature $Z\!\otimes\! I$ | blamed on **local** |
| failing downstream reads $Z$ | edge blame **overlapping** |
| failing downstream reads $I$ | edge blame **(none)** |
| correction: invisible sector | $9 \to 8$, refinement-safe, accepted |

The first two rows show the annihilator filter working: a one-body node is blind
to a two-body feature, and vice versa. The last row shows a safe correction —
refining a node's probes shrinks the invisible sector.

## 6. Limits

- The external verdict is still **required**; internal certificates never supply it.
- Localization is only as good as the **declared interfaces** — an error from an
  undeclared interaction localizes to the wrong node.
- Re-certification is cheap but **required** after every correction: that is the
  loop's cost.

## 7. Status

Implemented as `foc.corrective` (`localize`, `blame_edge`, `accept_correction`,
`corrective_report`) and run in demo section 21.

**Back to** [README](../README.md).
