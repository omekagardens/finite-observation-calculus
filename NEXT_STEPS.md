# NEXT_STEPS — open tracks

A living list of what is done and what is open. Companion to `README.md` and `docs/`.

## Done

- `docs/01`–`07`: the six core results, each with module + test + demo.
- `docs/08`: the ambiguity dichotomy (annihilator reading).
- `docs/09`: integrability / distortion / decidability.
- `docs/10`: locality and access.
- `docs/11`: the certification dichotomy (margin form; certification radius).
- `src/foc/ambiguity.py`: `annihilator_dim`, `classify`, `probe_audit`,
  `linear_symmetry_dim`, `l_inf_separation`, `l_inf_erosion_rate`,
  `llm_probe_audit`.

## Open tracks

### T1 — Nonlinear symmetry  *(open; interesting)*
`docs/09` §2 decides the **linear** case via `𝔞(L) ⊂ gl(n)`. Extend to
**nonlinear / algebraic** symmetries: a criterion for when an ambiguity is an
orbit of a declared nonlinear group, not just `GL(n)`. Caveat already recorded:
every rank-one fiber is *locally* a nonlinear tangent-flow orbit, so the intrinsic
question is ill-posed and any criterion must be **relative to a declared group /
 Lie pseudogroup**. Related machinery: Lie foliations (Molino), the holonomy group
(`docs/09` §2 Remark, `docs/10` §3).

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
