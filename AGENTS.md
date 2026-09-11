# AGENTS.md — finite-observation-calculus

## What this project is

An **exact** (all-rational, zero-dependency) calculus of *records, observations, and inference*. It makes precise one idea:

> When two different underlying structures produce the same observations, there are **two distinct reasons**. One is fixable by measuring more or better; the other survives even the complete observable law.

It is a self-contained extraction and AI/inference re-statement of the record/observation mathematics in the **`omekagardens/det_8_framework`** program (`ret` and `qr-05-bridge` branches). The canonical upstream formal definition is `docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` there (quantum instruments, record slots, the Z/X counterexample, schedule-independence via commuting maps); the predictive-summary and coarse-graining material traces to the upstream QR-02/QR-03 validation studies, and the replacement-robustness, enclosure and non-compositionality material (`docs/30`–`32`) traces to the `qr-05a*` series on the `qr-05-bridge` branch.

The local project deliberately strips away the upstream `det_8_framework`'s ontology/κ-physics layer and keeps only the **finite, exact, classical-or-quantum record/observation calculus**, restated in computation-focused language.

## Commands

```bash
python3 demo.py                              # runnable walkthrough of every result
python3 -m unittest discover -s tests -v     # stdlib unittest suite (120 tests)
pip install -e .                             # optional: install as a package
```

Python 3.9+ standard library only. **No dependencies.** The test suite is `unittest`; `pytest` is listed as an optional test dependency but the canonical command is `unittest discover`.

## Invariants (do not break these)

1. **Every number is a `fractions.Fraction`, never a float.** The whole point of the project is *exact* witnesses, not approximate numerics. Do not introduce `float`, `math` (except `math.comb` for binomial coefficients), or any floating-point comparison. Rational arithmetic only.
2. **No dependencies.** Standard library only. Do not add `numpy`, `sympy`, etc.
3. **A record is a first-class object, kept separate from the state.** Do not conflate the classical record with the quantum/probability state. This separation is the mathematical content (`docs/01-record-model.md` §4).
4. **Every core result in the README has a runnable `demo.py` section and a test.** A new "result" is not complete without both.
5. **Docstrings describe the mathematical claim, not the code mechanics.** Follow the existing style: a module docstring states the result, each function states its exact claim (often with the closed-form formula).

## Repository layout

```
docs/01-record-model.md            minimal vocabulary: states, events, records, instruments, schedules
docs/02-equivalence.md             behavioral (record-discarded) vs mechanistic (recorded) equivalence
docs/03-ambiguity-taxonomy.md      the centerpiece: two kinds of observational ambiguity
docs/04-minimal-summaries.md       question-relative predictive equivalence / minimal summaries
docs/05-forgetting.md              coarse-graining (sum of maps) vs recombination (sum of amplitudes)
docs/06-confidence.md              marginal vs conditional coverage
docs/07-separation-and-distortion.md  exact separation budgets under distortion
docs/08-ambiguity-dichotomy.md     the general dichotomy (all of 03–07 as instances)
docs/09-decidability.md            integrability / distortion rate / one-sided decidability
docs/10-locality-and-access.md     locality vs global access; the access trichotomy
docs/11-certification-dichotomy.md the certification theorem (margin form; radius)
docs/12-nonlinear-symmetry.md      declared generators; the rank-one symmetry theorem
docs/13-empirical-protocol.md      the probe-audit protocol (margin + sample budget)
docs/14-certificate-toolkit.md     exact, machine-checkable verdict certificates
docs/15-cross-domain-zoo.md        exact witnesses (causal / conformal / partial-ID)
docs/16-model-run.md               a controlled model run of the probe audit
docs/17-trained-model.md           exact rational training + a trained-model audit
docs/18-rational-transformer.md    a genuine transformer trained without floats
docs/19-certified-precision.md     the correction rate bounds exact bit growth
docs/20-regime-composition.md      transformers as certified nodes; routing as a record
docs/21-certified-router.md        a certified router + the routing theorems
docs/22-internal-certification.md  self-consistency + closed growth (internal certificates)
docs/23-corrective-loop.md         localizing an external failure into a bounded correction
docs/24-bootstrap.md               bootstrapping certified nodes from a local LLM
docs/25-benchmarks.md              benchmarks, projections, and next steps (B1-B6)
docs/26-math-oracle.md             the real math oracle (local model selection)
docs/27-node-classes.md            richer lifts (cubic / quartic / rational)
docs/28-distribution.md            distributing nodes across processes (JSON certs)
docs/29-hierarchical-router.md     the nested router (nesting adds cost)
docs/30-replacement-robustness.md  minimax retention, the replacement envelope, stress tilts
docs/31-certified-enclosures.md    L<=G<=U bracketing + the three-way error split
docs/32-summaries-not-compositional.md  pair additivity is not chain closure
src/foc/linalg.py                  exact rational matrix helpers (lists of lists of Fraction)
src/foc/instruments.py             states, projectors, outcome maps, channels
src/foc/schedule.py                records, schedules, the Z/X counterexample
src/foc/summaries.py               predictive equivalence, minimal summaries
src/foc/geometry.py                the two-kinds-of-ambiguity example (geometry vs sampling density)
src/foc/forgetting.py              coarse-graining (sum of maps) vs coherent recombination
src/foc/confidence.py              Clopper-Pearson, marginal/conditional, separation budgets
src/foc/ambiguity.py               the general dichotomy: annihilator, symmetry, collapse, protocol
src/foc/certificate.py             exact, machine-checkable verdict certificates
src/foc/crossdomain.py             cross-domain exact witnesses
src/foc/modelrun.py                a controlled model run of the probe audit (exact)
src/foc/train.py                   exact rational training + a trained-model audit
src/foc/transformer.py             a genuine transformer trained without floats
src/foc/truncate.py                certified precision: bit growth bounded by the margin
src/foc/regime.py                  transformers as certified nodes; per-regime precision
src/foc/router.py                  a certified router + the routing theorems
src/foc/internal.py                internal certification: self-consistency + closed growth
src/foc/corrective.py              the corrective loop: localizing an external failure
src/foc/bootstrap.py               bootstrap certified nodes from a local LLM
src/foc/mathbench.py               B1/B2: math-task ladder
src/foc/nested.py                  B4/B5: flat vs nested regimes, projections
src/foc/longsession.py             B3: longer training via certified truncation
src/foc/hierarchical.py            the nested router (build, route, flat vs nested bits)
src/foc/distributed.py             distribute regime nodes across processes (JSON certs)
src/foc/replacement.py             minimax retention, the replacement envelope, stress tilts
src/foc/enclosure.py               L<=G<=U bracketing + the three-way error decomposition
src/foc/composition.py             pair additivity vs chain closure (the covariance identity)
tests/                             stdlib unittest suite, one file per module
```

## Provenance map (what came from where)

This matters because the project's README cites the upstream `det_8_framework` as its source of depth. The mapping is:

| Local artifact | Upstream source (`det_8_framework`/`ret`) | Status |
|---|---|---|
| `docs/01-record-model.md`, `instruments.py` | `docs/QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §4 (instrument `I^s_{e,x} = Σ M ρ M†`, record-slot discipline) | **Direct extraction** — notation matches |
| `docs/02-equivalence.md`, `schedule.py` Z/X counterexample | `QUANTUM_RECORD_STRUCTURE_RESEARCH.md` §5.4 (exact same numbers) | **Direct extraction** — verified |
| `docs/04-minimal-summaries.md`, `summaries.py` | `docs/validation/qr-03-predictive-histories` (predictive equivalence `n_h/d_h`, "keep last X" fixture) | **Extraction** — concept matches |
| `docs/05-forgetting.md`, `forgetting.py` | QR-02 (coarse-graining: "do not sum amplitudes when forgetting an outcome") | **Extraction** — concept matches; the non-projective witness instrument is local |
| `docs/03-ambiguity-taxonomy.md`, `geometry.py` | Order-geometry/density theme from the upstream program; **the exact η/δ factorization obstruction example is this project's own construction** | **Local synthesis** — do not attribute the specific formula to upstream |
| `docs/06-confidence.md`, `confidence.py` (marginal/conditional) | Upstream RET doctrine (marginal vs conditional predictive support); the n=4 singleton construction is local | **Local synthesis** |
| `docs/07-separation-and-distortion.md`, `confidence.py` (budgets) | Upstream "separation" theme (QR-06 / RET); the specific `slack = D − 2e − 2/m` certificate is local | **Local synthesis** |
| `docs/08-ambiguity-dichotomy.md`, `docs/09-decidability.md`, `docs/10-locality-and-access.md`, `docs/11-certification-dichotomy.md` | This project's own assembly of the dichotomy from identifiability, gauge / Lie-foliation theory, and Le Cam testing; no direct upstream counterpart | **Local synthesis** — the general theorem and its consequences, marked as synthesis in the docs themselves |
| `docs/30-replacement-robustness.md`, `replacement.py` | QR-05 bridge branch, `docs/validation/qr-05aa`–`qr-05ae` (declared uncertainty bounds, fixed blends, subtract-coarse-before-max; the whole-fiber replacement envelope and the two stress tilts) | **Extraction** — the minimax/envelope/full-support/tilt statements are upstream-derived; the `1/16` menu bound and the signed-group reading are local |
| `docs/31-certified-enclosures.md`, `enclosure.py` | QR-05 bridge branch, `docs/validation/qr-05ag`/`qr-05ah`/`qr-05ai` (supplied local-volume marks; boundary refinement; weighted kernels) | **Extraction** — bracketing, refinement monotonicity and the error identities are upstream-derived; the fixture and non-monotone counterexample are local |
| `docs/32-summaries-not-compositional.md`, `composition.py` | QR-05 bridge branch, `docs/validation/qr-05aj`/`qr-05ak` (pair coarsening; the shared middle) | **Extraction** — the pair product, covariance identity and unit-clip numbers are upstream-derived; the 1-D integral machinery and coarsening fixture are local |

**Rule:** when extending or documenting the code, preserve this distinction. The record-model, equivalence/Z/X, summaries, and forgetting results are upstream-derived — keep them notationally aligned with `det_8_framework`. The ambiguity taxonomy, confidence, and separation-budget results are this project's own exact-ification of upstream *themes* — mark them as such rather than claiming upstream has the exact construction.

## Style

- Follow existing module structure: one conceptual result per module, thin functions with `Fraction`-typed math, docstrings that state the exact claim.
- Tests assert **exact** `Fraction` equality, never approximate `assertAlmostEqual` for the core claims (a `assertLessEqual` sanity check on an interval endpoint is the one exception, in `test_confidence.py`).
- Matrix representation is a list of lists of `Fraction`. The adjoint is the transpose (all examples are real).
- Do not add comments narrating what the code does; the docstrings already carry the mathematical claim.
