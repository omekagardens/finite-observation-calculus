# 26 — The real math oracle

`docs/24` bootstrapped from a general 3B model. This note runs it against
**math-capable** local models, which is what the bootstrap actually needs.

## 1. The run

```
python3 scripts/bootstrap_llm.py --endpoint http://localhost:11434 \
    --model qwen2.5-coder:3b --task "multiply two integers a and b"
```

| oracle | result |
|---|---|
| `qwen2.5-coder:3b` | regimes `['Basic Arithmetic', 'Bitwise Multiplication']`; **both nodes recover `y = a·b` exactly (loss 0)** |
| `deepseek-r1:8b` | **timed out** (reasoning model: long think-blocks, slow) |

## 2. What it shows

- **Oracle choice is load-bearing.** `qwen2.5-coder:3b` emitted consistent
  examples and the calculus recovered the exact rule `y = x1·x2` with **zero loss**;
  the earlier `llama3.2:3b` run left a nonzero loss (its examples were
  inconsistent with the model class). A math/code model is the right oracle.
- **Reasoning models are a poor oracle** for this protocol: `deepseek-r1:8b`
  emits long reasoning blocks that both slow the call past the timeout and break
  clean JSON. For seeding, prefer a small *instruct/code* model.

## 3. Why this matters

The bootstrap is the boundary where an untrusted text oracle becomes an exact,
certified structure (`docs/22` §7). A clean oracle makes that boundary sharp: the
0 loss is a *certificate* that the oracle's examples lie exactly in the declared
family — a check the bootstrap performs for free.

## 4. Status

Run recorded here; the mechanism is `foc.bootstrap` (`docs/24`). No new code —
the point is the oracle selection.

**Back to** [README](../README.md).
