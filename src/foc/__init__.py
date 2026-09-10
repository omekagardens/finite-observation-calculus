"""finite-observation-calculus: an exact, dependency-free calculus of records,
observations, and inference.

All numbers are ``fractions.Fraction``; nothing here uses floating point.
"""

from . import (
    linalg, instruments, schedule, summaries, geometry, forgetting, confidence,
    ambiguity, certificate, crossdomain, modelrun,
)

__all__ = [
    "linalg", "instruments", "schedule", "summaries", "geometry", "forgetting",
    "confidence", "ambiguity", "certificate", "crossdomain", "modelrun",
]

__version__ = "0.1.0"
