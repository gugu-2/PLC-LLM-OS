"""
plc_platform/evaluate — 5-Way Comparative Evaluation Harness & Industrial Benchmarks.

Implements:
- 31 Held-out industrial benchmark suites across 6 commercial manufacturing sectors.
- Evaluator for 5 core metrics: IEC-PR, DCA, HR, VDCS, ESCS.
- Comparative runner across Base, Base+RAG, FT, FT+RAG, and FT+RAG+Gauntlet.
"""

from .benchmarks import BenchmarkSuite, BenchmarkItem
from .metrics import MetricsCalculator, BenchmarkEvaluationResult
from .runner import ComparativeBenchmarkRunner, ComparativeScorecard

__all__ = [
    "BenchmarkSuite",
    "BenchmarkItem",
    "MetricsCalculator",
    "BenchmarkEvaluationResult",
    "ComparativeBenchmarkRunner",
    "ComparativeScorecard",
]
