# 24 — Bootstrapping certified nodes from a local LLM

`docs/20`–`23` assume *declared* regimes and data. This note fills that gap: a
local LLM supplies both, and the calculus trains and certifies each node exactly.

## 1. The gap

The calculus needs declared regimes, declared interfaces, and declared data. A
local LLM can *propose* all three cheaply — as a **declared** structure, not a
certified one (`docs/22` §7). Everything downstream of the LLM's text is exact
rational arithmetic.

## 2. The recipe

1. **Regimes** — ask the LLM to partition the task into named regimes.
2. **Examples** — ask it for `k` labeled examples per regime (JSON, exact
   rationals).
3. **Train** — fit a node per regime **exactly** by closed-form least squares
   (`docs/17`): `y = c0 x1 + c1 x2 + c2 x1x2`.
4. **Certify** — the node's coefficients are exact; its loss is exact; the
   regime's structure (linear vs product) is read off the coefficients.
5. **Declare** — the regimes and interfaces are now declared, so the router
   (`docs/21`) and the corrective loop (`docs/23`) can take over.

The LLM is an **external oracle** — declared, not certified. The bootstrap is the
boundary where an untrusted text source becomes an exact, certified structure.

## 3. The prototype

Standard library only:
- `MockLLM` — offline, deterministic (used by the demo and tests);
- `LocalLLM` — an HTTP client for a local endpoint (Ollama `/api/generate`, or
  OpenAI-compatible `/v1/chat/completions`).

```
python3 scripts/bootstrap_llm.py                                   # offline mock
python3 scripts/bootstrap_llm.py --endpoint http://localhost:11434 --model llama3.2:3b
python3 scripts/bootstrap_llm.py --backend openai --endpoint http://localhost:1234 --model microsoft/phi-4
```

## 4. The real run (local `llama3.2:3b`)

```
regimes: ['Regime A', 'Regime B']
node        c0 (x1)   c1 (x2)   c2 (x1x2)    loss   product?
Regime A       7/10  -247/1120     -9/224  57/280   True
Regime B        2/5    -37/560     -3/112  37/70    True
```

The whole chain ran: an untrusted 3B model proposed the regimes and the examples;
the calculus parsed them, solved the normal equations exactly, and reported
**exact** coefficients and loss. The nonzero loss is itself the point — the
oracle's examples do not lie in the model class, and the bootstrap *measures that
inconsistency exactly* rather than hiding it in a float.

## 5. What it shows, and its limits

- **Shows**: a usable, dependency-free path from a local LLM to a **certified**
  regime structure — the seeding step the open/continual architecture needed.
- **Limits**: the oracle's *content* is not certified (`docs/22` §7); parsing can
  fail on a weak model (the script reports it rather than guessing); the node
  class is small (a linear + product model). Richer node classes are drop-in —
  the bootstrap's job is only to produce declared data.

## 6. Status

Implemented as `foc.bootstrap` (`parse_json`, `MockLLM`, `LocalLLM`,
`train_node`, `bootstrap`) and `scripts/bootstrap_llm.py`; exercised offline in
demo section 22 and against a real local Ollama model.

**Back to** [README](../README.md).
