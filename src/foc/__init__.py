"""finite-observation-calculus: an exact, dependency-free calculus of records,
observations, and inference.

All numbers are ``fractions.Fraction``; nothing here uses floating point.
"""

from . import linalg, instruments, schedule, summaries, geometry, forgetting, confidence, ambiguity

__all__ = ["linalg", "instruments", "schedule", "summaries", "geometry", "forgetting", "confidence", "ambiguity"]

__version__ = "0.1.0"
