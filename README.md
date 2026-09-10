# finite-observation-calculus

A small, **exact** (all-rational, dependency-free) calculus of *records, observations, and inference* — built to make one idea precise and reusable:

> When two different underlying structures produce the same observations, there are **two distinct reasons** for it. One is fixable by measuring more or better. The other survives **even the complete observable law** — no amount of additional measurement can resolve it.

This repository extracts that mathematics and states it in plain, computation-focused language, with a runnable Python reference implementation. It is intended for people working on **language models, sequence models, inference systems, calibration, and model interpretability**.

It deliberately does **not** carry any philosophical, physical, or ontological commitments. Those live elsewhere (see [Background and further reading](#background-and-further-reading)).

---

## The one-sentence summary

An observation is a *lossy trace* of an underlying state or structure. The gap between the two is not always closed by collecting more data. This repository gives you exact, checkable examples of when it is and when it is not.

---

## Core results (each with runnable code)

1. **Behavioral vs. mechanistic equivalence** (`docs/02-equivalence.md`)
   Two processes can have *identical* input–output behavior yet *different* internal computation. Discarding intermediate records can certify an equality that is false once records are retained. This is the mathematical reason *behavioral* evaluation cannot substitute for *mechanistic* understanding.

2. **The two-kinds-of-ambiguity taxonomy** (`docs/03-ambiguity-taxonomy.md`)
   - *Channel-limited ambiguity*: two hypotheses agree on one measurement but differ on a richer one. Fixed by asking a better question.
   - *Point-law-surviving ambiguity*: two hypotheses agree on the **complete** observable law. Not fixed by *any* common observation channel — the distinguishing information is not in the observable at all.

3. **Question-relative minimal summaries** (`docs/04-minimal-summaries.md`)
   There is no universal "sufficient statistic." The coarsest adequate summary of a history is defined **only relative to a declared family of future questions**. Change the question, and the right summary changes.

4. **Forgetting is not recombination** (`docs/05-forgetting.md`)
   Coarsening an outcome (summing *probability maps*) is fundamentally different from coherently recombining *amplitudes*. The two must never be conflated when compressing or pruning a representation.

5. **Marginal vs. conditional confidence** (`docs/06-confidence.md`)
   A procedure can have correct *unconditional* coverage while being *conditionally* wrong with probability one on a positive-probability event. "Calibrated on average" does not imply "trustworthy per instance."

6. **Separation budgets under distortion** (`docs/07-separation-and-distortion.md`)
   Distinguishing two hypotheses has a precise, exact sample-complexity certificate, and systematic distortion erodes the separation margin at a specific rate. Under enough shift, two hypotheses become literally indistinguishable.

---

## The general result behind them

The six results above are instances of one theorem (`docs/08-ambiguity-dichotomy.md`). Fix a declared observation class; then every pair of worlds is exactly one of **separated**, **channel-limited**, or **law-surviving**, and the law-surviving case is the *annihilator* of the completed effect algebra — physically, the invisible sector of a superselection rule; in parametric families, the gauge orbit of the law map.

`docs/09-decidability.md` develops the consequences:

- **Integrability** — *symmetry is group-relative*: every fiber is locally a pseudogroup orbit, so "is this ambiguity a symmetry?" must name a group. For a declared linear group the check is the computable symmetry algebra `𝔞(L)`, giving a continuous / discrete / accidental trichotomy.
- **Distortion** — the collapse is sharp at `2e = d`, with a matching non-asymptotic rate `n* = Θ((d−2e)⁻²log(1/δ))`.
- **One-sided decidability** — with the model in hand the trichotomy is a finite rank computation costing no experiments; from data alone the resolvable labels are certifiable but the law-surviving label is *not*. **Channel-limited ambiguity is a statement about the data; law-surviving ambiguity is a statement about the model.**

`docs/10-locality-and-access.md` reads the dichotomy as a theory of **access**: it splits the classical local/global binary into *scope* (channel-limited) and *observability* (law-surviving), shows the annihilator is exactly the nonlocal content (one-body access on two qubits leaves a 9-dimensional invisible sector = the two-body correlations), and identifies holonomy as the local-to-global obstruction.

`docs/11-certification-dichotomy.md` states the certification theorem formally: at any margin `t` the whole trichotomy is certifiable from data at cost `Θ(t⁻²log(1/δ))`, while the exact case is the non-certifiable singular limit `t→0` (certification radius `≍ (log(1/δ)/n)^{1/2}`).

These documents (`08`–`11`) are an expository **synthesis** — they assemble known mathematics (identifiability, gauge and Lie-foliation theory, Le Cam testing) into the dichotomy with exact witnesses. They are not new theorems; the contribution is the unified framing. The computable core is implemented in `src/foc/ambiguity.py`; open directions are tracked in [`NEXT_STEPS.md`](NEXT_STEPS.md).

---

## Quick start

No dependencies — Python 3.9+ standard library only.

```bash
# run the demonstrations
python3 demo.py

# run the test suite (stdlib unittest)
python3 -m unittest discover -s tests -v
```

Install as a package (optional):

```bash
pip install -e .
```

---

## Repository map

```
finite-observation-calculus/
├── README.md
├── LICENSE                     # MIT
├── pyproject.toml
├── demo.py                     # runnable walkthrough of every result
├── NEXT_STEPS.md               # open tracks (nonlinear symmetry, protocol, ...)
├── docs/
│   ├── 01-record-model.md
│   ├── 02-equivalence.md
│   ├── 03-ambiguity-taxonomy.md
│   ├── 04-minimal-summaries.md
│   ├── 05-forgetting.md
│   ├── 06-confidence.md
│   ├── 07-separation-and-distortion.md
│   ├── 08-ambiguity-dichotomy.md        # the general dichotomy (synthesis)
│   ├── 09-decidability.md               # integrability, distortion, one-sided decidability
│   ├── 10-locality-and-access.md        # locality vs global access; the access trichotomy
│   └── 11-certification-dichotomy.md    # the certification theorem (margin form)
├── src/foc/                    # the reference implementation
│   ├── linalg.py               # exact rational matrix helpers
│   ├── instruments.py          # observation maps, states, channels
│   ├── schedule.py             # records, schedules, the Z/X counterexample
│   ├── summaries.py            # predictive equivalence, minimal summaries
│   ├── geometry.py             # the two-kinds-of-ambiguity example
│   ├── forgetting.py           # coarse-graining (sum of maps) vs coherent recombination
│   ├── confidence.py           # binomial intervals, budgets, distortion
│   └── ambiguity.py            # the general dichotomy: annihilator, symmetry, collapse
└── tests/                      # stdlib unittest suite
```

---

## Why "exact"?

Every number in this repository is a rational number (`fractions.Fraction`), never a float. The claims — "these two hypotheses have the identical complete observable law," "these two targets differ by exactly 3/80" — are *exact*, not approximate. That is what makes them genuine counterexamples rather than numerical curiosities: a single exact witness refutes a universal claim ("measurement always suffices").

---

## What this is not

- Not a claim that measurement *never* suffices. It is a collection of exact counterexamples that refute the *universal* claim that measurement *always* suffices, plus a taxonomy of *why* it fails when it does.
- Not a new learning algorithm. It is a set of precise, transferable *diagnostics* and *limits* for algorithms you already have.
- **Not new mathematics.** The theory notes (`docs/08`, `docs/09`) are an exact *synthesis* of known results — identifiability, gauge/Lie-foliation theory, Le Cam testing. The contribution is the unified framing, the exact witnesses, and the decidability reading, not new theorems.
- Not tied to any interpretation of probability, quantum mechanics, or computation. The classical case (probability vectors, stochastic maps) is a fully contained special case of the same notation.

---

## Background and further reading

This calculus is drawn from a larger finite record/quantum/order mathematics program. For the full treatment (including the quantum-operations framing, order geometry, and the exact-rational verification machinery), see:

- https://github.com/omekagardens/det_8_framework

The present repository is intentionally self-contained: every definition needed here is stated here, and the source repository is referenced only for depth.

---

## Wider applications (brief)

The same ideas appear, under different names, across several fields:

- **Statistics** — partial identification of structural parameters under bounds; the distinction between "ambiguous" and "model-infeasible" data.
- **Conformal prediction** — the gap between marginal validity and conditional validity.
- **Causal inference** — observationally equivalent causal structures.
- **Discrete geometry** — recovering structure from order + volume, and the geometry/density factorization ambiguity that blocks it.

The initial focus of this repository is the AI/inference reading; the wider notes are kept brief.

---

## License

MIT. See [LICENSE](LICENSE).
