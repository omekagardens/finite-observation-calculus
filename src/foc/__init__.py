"""finite-observation-calculus: an exact, dependency-free calculus of records,
observations, and inference.

All numbers are ``fractions.Fraction``; nothing here uses floating point.
"""

from . import (
    linalg, instruments, schedule, summaries, geometry, forgetting, confidence,
    ambiguity, certificate, crossdomain, modelrun, train, transformer, truncate,
    regime, router, internal, corrective, bootstrap,
    mathbench, nested, longsession, hierarchical, distributed,
    replacement, enclosure, composition,
)

__all__ = [
    "linalg", "instruments", "schedule", "summaries", "geometry", "forgetting",
    "confidence", "ambiguity", "certificate", "crossdomain", "modelrun", "train",
    "transformer", "truncate", "regime", "router", "internal", "corrective",
    "bootstrap", "mathbench", "nested", "longsession", "hierarchical", "distributed",
    "replacement", "enclosure", "composition",
]

__version__ = "0.1.0"
