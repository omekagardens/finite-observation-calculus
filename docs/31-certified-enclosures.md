# 31 — Certified enclosures, and where the observation error lives

`docs/19` bounds the bits worth keeping; `docs/14` ships a verdict as a portable
certificate. This note adds the **geometric** case: when an observation is *which
cells of a supplied partition fall inside a query*, the loss splits into exactly
three **signed** parts, each certified by an exact finite enclosure.

The result is a finite enclosure, **not** a continuum limit: the gate is given a
flat geometry and never reconstructs a metric. The shape is taken from the
upstream QR-05AG–AI series; the statements are restated in this project's
notation.

## 1. Two access layers

The mathematics separates cleanly into what is *supplied* and what is *observed*:

- the **geometry layer** sees the domain, the cell bounds, the representatives,
  the supplied marks and the probes — it may compute areas and bounds;
- the **observation layer** sees only the retained induced order, fixed marker
  IDs, the selection law and the retained cells' marks.

The enclosure below is a *geometry-layer* statement. It must not be described as
a conclusion derivable from an order-only record.

## 2. Bracketing

For a probe `Q` and each cell `i` with geometric area `g_i`, classify the cell as

- **inner** — the whole cell lies in `Q` (up to zero-area boundaries);
- **outer** — the clipped intersection with `Q` has strictly positive area;
- **representative** — its representative lies strictly inside `Q`.

Define `L = \sum_{\text{inner}} g_i`, `U = \sum_{\text{outer}} g_i`,
`G = \sum_{\text{rep}} g_i`, the supplied target `T = \sum_{\text{rep}} w_i`, the
true query volume `V`, and the **gap** `= U - L`. Then, exactly,

$$L \le G \le U, \qquad L \le V \le U, \qquad
|G - V| \le \text{gap},$$

and the *signed* certificate `G - U \le G - V \le G - L`. Note what is **not**
claimed: `G` and `V` are **not ordered** — the representative sum may sit on
either side of the true volume. A boundary-only touch is not "outer"; the bounds
use geometric areas, never the supplied marks.

## 3. Refinement tightens the gap — not the error

A nested refinement (each new cell has one declared parent; child areas and
child marks sum to the parent's) satisfies

$$L_{\text{fine}} \ge L_{\text{coarse}}, \qquad
U_{\text{fine}} \le U_{\text{coarse}}, \qquad
\text{gap}_{\text{fine}} \le \text{gap}_{\text{coarse}} .$$

The three are monotone. But the **signed and absolute representative quadrature
errors need not improve** — a finer partition can move `G` further from `V`. This
is an exact finite statement, not asymptotic convergence, and the module carries
an explicit constructive counterexample rather than leaving it as a caveat.

## 4. The three-way error identity

For a single retained record, the signed errors of an estimator `mean` and the
three named targets satisfy, exactly,

$$\underbrace{\text{mean} - V}_{\text{total}}
= \underbrace{(\text{mean} - T)}_{\text{sampling bias}}
+ \underbrace{(T - G)}_{\text{annotation}}
+ \underbrace{(G - V)}_{\text{quadrature}} .$$

Each term is kept signed and never relabelled "noise". The **annotation** error is
zero precisely when the supplied marks equal the geometric areas; the
**quadrature** error is what the enclosure of §2 brackets; the **sampling** bias is
not bounded by the geometric enclosure at all — it is a property of the
*retained record*, not of the geometry.

## 5. The kernel discrepancy

The same decomposition appears for the bilinear (pair) measure. With `P_g` the
geometric pair sum, `K` the clipped-order sum, `Jcross` and `Jdiag` the cross-cell
and within-cell integrals (`J = Jcross + Jdiag`),

$$P_g - J = \underbrace{(P_g - K)}_{\text{boundary}}
+ \underbrace{(K - Jcross)}_{\text{cross-order}}
- \underbrace{Jdiag}_{\text{omission}} .$$

The one-cell `[L, U]` enclosure of §2 is **not** reused as a bilinear error bound;
the three kernel terms carry that job.

## 6. The demonstration

`foc.enclosure.enclosure_report` — a `3 \times 2` grid of `[0,1]^2` (cell area
`1/12`), with cell `(0,1)` split at `v = 3/4`:

| probe | `L` | `G` | `U` | `V` | `gap` | exact? |
|---|---:|---:|---:|---:|---:|---|
| aligned `[0,2/3]\times[0,1/2]` | `1/6` | `1/6` | `1/6` | `1/6` | `0` | yes |
| unaligned `[0,4/5]^2` (coarse) | `1/6` | `1/3` | `1/2` | `8/25` | `1/3` | no |
| unaligned (refined) | `5/24` | `7/24` | `1/2` | `8/25` | `7/24` | no |

The aligned probe is exact (`L = G = U = V`) for a whole cell. The unaligned
probe brackets with `G > V` coarse and `G < V` fine — the pair is unordered. The
refinement raises `L` by `1/24`, leaves `U` fixed, and shrinks the gap by `1/24`,
yet the quadrature error goes `1/75 \mapsto -17/600`: its **absolute** value
grows. The three-way split for the coarse probe is
`17/150 = 1/10 + 0 + 1/75` (sampling + annotation + quadrature), and the kernel
decomposition is `0 = 1/20 + 1/20 - 1/10`.

## 7. Status

Implemented as `foc.enclosure` (`bounds`, `certify`, `refine`,
`quadrature_error`, `error_decomposition`, `kernel_discrepancy`, `membership`,
`enclosure_report`) and run in demo section 27.

**Provenance.** Upstream-derived (QR-05AG/AH/AI): the bracketing, refinement and
error-decomposition statements are extractions restated in this project's
notation. The particular `3\times2` fixture and the non-monotone counterexample
are this project's exact constructions.

**Back to** [README](../README.md).
