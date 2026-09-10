# NEXT_STEPS — open tracks

A living list of what is done and what is open. Companion to `README.md` and `docs/`.

## Done

- `docs/01`–`07`: the six core results, each with module + test + demo.
- `docs/08`: the ambiguity dichotomy (annihilator reading).
- `docs/09`: integrability / distortion / decidability.
- `docs/10`: locality and access.
- `docs/11`: the certification dichotomy (margin form; certification radius).
- `docs/12`: nonlinear symmetry (declared generators; the rank-one theorem).
- `src/foc/ambiguity.py`: `annihilator_dim`, `classify`, `probe_audit`,
  `linear_symmetry_dim`, `polynomial_symmetry_dim`, `rank1_symmetry_field`,
  `l_inf_separation`, `l_inf_erosion_rate`, `llm_probe_audit`.

## Open tracks

### T1 — Nonlinear symmetry  *(documented in `docs/12`; residual items open)*
`docs/12` settles the main question: the intrinsic symmetry algebra is
infinite-dimensional (the degree-`≤d` polynomial symmetry space grows as
`d(d+1)/2`), so the question is relative to a declared generator space; and every
**rank-one** fiber is a 1-parameter group orbit, `X=(L_y,−L_x)`. Residual open
items:
- an explicit exact **non-Lie-foliation** witness (a rank-`≥2` parametric
  foliation with nonvanishing Godbillon–Vey class) to instantiate the
  codimension-`≥2` case;
- a criterion for the **minimal symmetry degree**;
- decidability of the foliation case from finitely many derivatives.

### T2 — Empirical protocol
Instantiate the certifier (`docs/11`) on a real probe family and an empirical
measurement model: the rank/annihilator audit on activations, plus margin-vs-radius
finite-sample certification. The current `llm_probe_audit()` is the toy stand-in.

### T3 — Certificate toolkit
Machine-checkable exact certificates per verdict (separated / channel-limited /
law-surviving) plus a verifier; ties to the upstream QR-01 wire schema.

### T4 — Cross-domain exact-witness zoo
One small exact module + doc + test each: causal observational equivalence;
conformal marginal-vs-conditional; partial identification.

### T5 — Formalization (Lean)
The finite-dimensional core is exact rational, hence Lean-friendly; machine-check
the theorems to make the "exact" claim a "certified" one.

## Recently closed

- **Certification complexity** — `docs/09` §4's sketch is now the theorem of
  `docs/11` (margin form; the exact case is the non-certifiable singular limit).
- **Exact collapse constant** — the threshold and the erosion rate are closed-form
  (`docs/09` §3; `ambiguity.l_inf_separation`, `l_inf_erosion_rate`).
