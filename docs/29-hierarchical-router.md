# 29 — The hierarchical router

`docs/25` predicted that **nesting adds routing cost** (B4). This note builds the
tree and confirms it on a concrete margin profile.

## 1. The tree

`foc.hierarchical.build_tree` turns sorted 1-D regime positions into a balanced
binary tree; each internal node records the **split margin** (`pos[mid] −
pos[mid−1]`) and a boundary. `route` walks the tree (`log R` comparisons).

For positions `[0, 1/2, 11/20, 2]`:

| | |
|---|---|
| internal margins | `[1/20, 1/2, 29/20]` |
| flat router bits | **6** (one 4-way router resolves the closest pair `1/20`) |
| nested router bits | **9** (sum over the three binary splits) |
| nesting costs more | **yes** |

## 2. The confirmation

$$\text{nested} = \sum_i \lceil\log_2(2/m_i)\rceil \;\ge\; \max_i \lceil\log_2(2/m_i)\rceil
= \lceil\log_2(2/\min_i m_i)\rceil = \text{flat}.$$

The hard split must be resolved *wherever it lives*, and the tree pays for the
easy splits it also makes. So **nesting is not a bit lever** — `docs/25`'s
prediction, now measured on a real profile (6 vs 9).

## 3. What nesting *is* for

- **Distribution** (`docs/28`): subtrees certify independently.
- **Incremental growth**: adding a leaf re-certifies one path, not the model.
- **Per-branch models**: a subtree may use a different family (`docs/27`).

Routing itself is `O(log R)` in comparisons — a compute property, not a bit one.

## 4. Status

Implemented as `foc.hierarchical` (`build_tree`, `internal_margins`, `route`,
`flat_margin`, `benchmark_hierarchy`) and reported in demo section 25.

**Back to** [README](../README.md).
