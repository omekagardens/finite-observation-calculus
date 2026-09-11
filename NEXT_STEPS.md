# NEXT_STEPS — open tracks

A living list of what is done and what is open. Companion to `README.md` and `docs/`.

## Done

- `docs/01`–`07`: the six core results, each with module + test + demo.
- `docs/08`: the ambiguity dichotomy (annihilator reading).
- `docs/09`: integrability / distortion / decidability.
- `docs/10`: locality and access.
- `docs/11`: the certification dichotomy (margin form; certification radius).
- `docs/12`: nonlinear symmetry (declared generators; the rank-one theorem).
- `docs/13`: the empirical probe-audit protocol (margin + sample budget).
- `docs/14`: the certificate toolkit (exact, machine-checkable verdicts).
- `docs/15`: cross-domain witness zoo (causal / conformal / partial-ID).
- `docs/16`: a controlled model run of the probe audit (scored vs ground truth).
- `docs/17`: exact rational training + a trained-model audit.
- `docs/18`: a genuine transformer trained without floats (exact dual-number gradients).
- `docs/19`: certified precision — the correction rate bounds exact bit growth.
- `docs/20`: regime composition — transformers as certified nodes; routing as a record.
- `docs/21`: a certified router + the routing theorems (type gap, immateriality, boundary).
- `docs/22`: internal certification — self-consistency (fixed point) + closed, monotone growth.
- `docs/23`: the corrective loop — localize an external failure into a bounded correction.
- `docs/24`: bootstrap — turn a local LLM's regimes/examples into certified nodes (runnable).
- `docs/25`: benchmarks + projections (B1–B6) — math ladder, long sessions, regimes, distribution.
- `docs/26`: the real math oracle — `qwen2.5-coder:3b` seeds cleanly; reasoning models time out.
- `docs/27`: richer node classes — cubic / quartic / rational lifts; `min_lift` = symmetry degree.
- `docs/28`: distribution at scale — node sharding across processes (5.79x, bit-identical, JSON).
- `docs/29`: the hierarchical router — build/route; nesting adds routing cost (6 vs 9 bits).
- `docs/30`: replacement robustness — minimax retention, the replacement envelope, the sharp menu
  bound, aggregate≠per-instance, opposite tilts cancel. (from `qr-05-bridge`, `qr-05aa`–`ae`)
- `docs/31`: certified enclosures — `L≤G≤U` bracketing, refinement that tightens the gap but not
  the error, the three-way error split, the kernel discrepancy. (from `qr-05ag`/`ah`/`ai`)
- `docs/32`: summaries are not compositional — pair additivity vs chain closure, the covariance
  identity, conditionals with row sum `1/4`. (from `qr-05aj`/`ak`)
- `src/foc/replacement.py`: `excess`, `minimax_certificate`, `envelope_profile`,
  `retention_optimizer`, `retention_kkt`, `menu_gap`, `group_polynomials`,
  `forward_tilt`, `tilt_cancellation`, `replacement_report`.
- `src/foc/enclosure.py`: `bounds`, `certify`, `refine`, `error_decomposition`,
  `kernel_discrepancy`, `membership`, `enclosure_report`.
- `src/foc/composition.py`: `pair_int_1d`, `triple_int_1d`, `pair_measure`,
  `triple_measure`, `pair_product`, `covariance_identity_1d`, `coarsening_weights`,
  `unit_rectangle_report`, `composition_report`.
- `src/foc/ambiguity.py`: `annihilator_dim`, `classify`, `probe_audit`,
  `linear_symmetry_dim`, `polynomial_symmetry_dim`, `rank1_symmetry_field`,
  `feature_separation`, `certify_audit`, `l_inf_separation`,
  `l_inf_erosion_rate`, `llm_probe_audit`.
- `src/foc/certificate.py`: `build_certificate`, `verify_certificate`, `to_wire`,
  `from_wire`, `verify_wire`.

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

### T2 — Empirical protocol  *(docs/13; controlled `docs/16`; rational-trained `docs/17`; real trained model open)*
`docs/13` specifies the protocol; `docs/16` runs it on a controlled exact model;
`docs/17` trains a model in pure rationals and audits the learned representation.
Open: a run on a *real trained* model (probe directions and separations estimated
from held-out data), which needs a float/GPU stack and a data path outside this
zero-dependency package (design B).

### T3 — Certificate toolkit  *(done: `docs/14`, `src/foc/certificate.py`)*
Exact certificates per verdict plus an independent verifier and a JSON wire form
(QR-01 style). Residual: a batch `verify` that checks a *set* of certificates and
reports the nesting consistently across many features.

### T4 — Cross-domain witness zoo  *(done: `docs/15`, `src/foc/crossdomain.py`)*
Three exact witnesses (causal observational equivalence; conformal marginal vs
conditional; partial identification). Residual: more domains / larger examples
(causal bounds, IV, differential privacy), if wanted.

### T5 — Formalization (Lean)
The finite-dimensional core is exact rational, hence Lean-friendly; machine-check
the theorems to make the "exact" claim a "certified" one.

### T6 — `qr-05-bridge` beyond the record calculus  *(deliberately not folded)*
The remaining `qr-05a*` studies (roughly `qr-05al` onward: middle moments, field
measurements, measurement stability, source portability, metric reconstruction,
Laplacian / Lorentzian-operator convergence, Bell correspondence, physical
protocol design) are geometry / physics **protocol** work. They sit in the
ontology layer this project deliberately strips (`AGENTS.md`), so they are folded
only if and when the calculus gains a genuine classical/quantum *record*
statement from them.

## Recently closed

- **Certification complexity** — `docs/09` §4's sketch is now the theorem of
  `docs/11` (margin form; the exact case is the non-certifiable singular limit).
- **Exact collapse constant** — the threshold and the erosion rate are closed-form
  (`docs/09` §3; `ambiguity.l_inf_separation`, `l_inf_erosion_rate`).
