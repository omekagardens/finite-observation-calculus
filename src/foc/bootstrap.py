"""Bootstrapping certified regime nodes from a local LLM (``docs/24``).

The calculus needs *declared* regimes and *declared* data. A local LLM can supply
both: ask it for regimes, ask it for per-regime labeled examples, then **train and
certify each node exactly**. The LLM is an external oracle — declared, not
certified (`docs/22` §7); everything downstream of its text is exact rational
arithmetic.

Standard library only: ``MockLLM`` runs offline and deterministically, and
``LocalLLM`` talks to a local endpoint (Ollama or OpenAI-compatible) over HTTP.
"""

import json
import urllib.request
from fractions import Fraction

from . import train


def _frac(v):
    """Parse a JSON scalar into an exact ``Fraction`` (never a binary float)."""
    if isinstance(v, bool):
        raise ValueError("bool is not a rational")
    if isinstance(v, int):
        return Fraction(v)
    if isinstance(v, str):
        return Fraction(v.strip())
    if isinstance(v, float):
        return Fraction(str(v))
    raise ValueError(f"cannot parse rational: {v!r}")


def parse_json(text):
    """Extract the first JSON object/array from LLM text (tolerates prose/fences)."""
    start = min((i for i in (text.find("{"), text.find("[")) if i >= 0), default=-1)
    if start < 0:
        raise ValueError("no JSON found in LLM output")
    depth, open_ch = 0, None
    for i in range(start, len(text)):
        c = text[i]
        if c in "{[":
            depth += 1
            open_ch = c
        elif c in "}]":
            depth -= 1
            if depth == 0:
                return json.loads(text[start:i + 1])
    raise ValueError("unbalanced JSON in LLM output")


def regimes_prompt(task, r):
    return (f'You are a task analyst. Propose exactly {r} regimes for the task: "{task}". '
            f'Reply with ONLY a JSON object, no prose: '
            f'{{"regimes":[{{"name":"...","description":"..."}}]}}')


def examples_prompt(task, regime, k):
    return (f'Task: "{task}". Regime: "{regime["name"]}" ({regime.get("description", "")}). '
            f'Give exactly {k} labeled examples. Each input is a pair of small integers '
            f'[x1, x2]; each label y is an integer computed by the regime rule. '
            f'Reply with ONLY a JSON object, no prose: '
            f'{{"examples":[{{"x":[x1,x2],"y":y}}]}}')


# --- oracles ----------------------------------------------------------------

class MockLLM:
    """A deterministic offline oracle with exact rational examples."""

    _REGIMES = [
        {"name": "linear", "description": "target is linear in x1"},
        {"name": "interaction", "description": "target is the product x1*x2"},
    ]
    _POINTS = [(1, 0), (1, 1), (2, 1), (0, 1), (2, 2), (3, 1)]

    def regimes(self, task, r):
        return self._REGIMES[:r]

    def examples(self, task, regime, k):
        pts = self._POINTS[:k]
        name = regime["name"]
        if name == "linear":
            return [{"x": [a, b], "y": a} for a, b in pts]
        if name == "interaction":
            return [{"x": [a, b], "y": a * b} for a, b in pts]
        raise ValueError(f"unknown regime {name!r}")


class LocalLLM:
    """A local LLM endpoint (Ollama or OpenAI-compatible), standard library HTTP."""

    def __init__(self, endpoint="http://localhost:11434", model="llama3.2:3b",
                 backend="ollama", timeout=120):
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.backend = backend
        self.timeout = timeout

    def complete(self, prompt):
        if self.backend == "ollama":
            url = self.endpoint + "/api/generate"
            payload = {"model": self.model, "prompt": prompt, "stream": False,
                       "options": {"temperature": 0}}
            data = self._post(url, payload)
            return data.get("response", "")
        url = self.endpoint + "/v1/chat/completions"
        payload = {"model": self.model, "temperature": 0,
                   "messages": [{"role": "user", "content": prompt}]}
        data = self._post(url, payload)
        return data["choices"][0]["message"]["content"]

    def _post(self, url, payload):
        req = urllib.request.Request(
            url, data=json.dumps(payload).encode("utf-8"),
            headers={"Content-Type": "application/json"})
        with urllib.request.urlopen(req, timeout=self.timeout) as resp:
            return json.loads(resp.read().decode("utf-8"))

    def regimes(self, task, r):
        parsed = parse_json(self.complete(regimes_prompt(task, r)))
        return list(parsed["regimes"])[:r]

    def examples(self, task, regime, k):
        parsed = parse_json(self.complete(examples_prompt(task, regime, k)))
        return list(parsed["examples"])[:k]


# --- the bootstrap ----------------------------------------------------------

def train_node(examples):
    """Fit ``y = c0 x1 + c1 x2 + c2 x1 x2`` exactly by closed-form least squares."""
    A = [[_frac(e["x"][0]), _frac(e["x"][1]),
          _frac(e["x"][0]) * _frac(e["x"][1])] for e in examples]
    b = [_frac(e["y"]) for e in examples]
    coeffs = train.least_squares(A, b)
    resid = [sum(A[i][j] * coeffs[j] for j in range(3)) - b[i] for i in range(len(A))]
    loss = Fraction(1, 2) * sum(v * v for v in resid)
    return {"coefficients": coeffs, "loss": loss, "n_examples": len(examples)}


def bootstrap(task, llm, r=2, k=6):
    """Bootstrap certified regime nodes from an LLM oracle (``docs/24``)."""
    regimes = llm.regimes(task, r)
    nodes = []
    for regime in regimes:
        examples = llm.examples(task, regime, k)
        node = train_node(examples)
        node["regime"] = regime["name"]
        node["uses_product"] = node["coefficients"][2] != 0
        nodes.append(node)
    return {"task": task, "regimes": [g["name"] for g in regimes], "nodes": nodes}
