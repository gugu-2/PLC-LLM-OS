"""
plc_platform/datasets — 10-Archetype Dataset Pipeline & Project-Based Splitting.

Implements:
- Schema v2.0 for all 10 industrial dataset archetypes (DS-01 to DS-10).
- Generators and synthesizers for industrial training data.
- Project-based non-destructive train/val/test splitting to prevent benchmark contamination.
- Validation, filtering, and export pipeline for LLM fine-tuning.
"""

from .schema import DatasetArchetype, DatasetRecordV2
from .generators import DatasetArchetypeGenerator
from .project_splitter import ProjectBasedSplitter, DatasetSplitResult
from .pipeline import DatasetEngineeringPipeline

__all__ = [
    "DatasetArchetype",
    "DatasetRecordV2",
    "DatasetArchetypeGenerator",
    "ProjectBasedSplitter",
    "DatasetSplitResult",
    "DatasetEngineeringPipeline",
]
