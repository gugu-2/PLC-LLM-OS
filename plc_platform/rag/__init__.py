"""
plc_platform/rag — Industrial Standards Knowledge Base & Hybrid Retrieval Engine.

Implements:
- Authoritative knowledge corpus for ISA-88, PackML, ISA-18.2, IEC 61131-3, and Vendor Diagnostics.
- Hybrid BM25 + Dense Semantic Retriever with Reciprocal Rank Fusion (RRF).
- Domain and Vendor metadata filtering.
- Prompt Augmentation for LLM Engineering Context Injection.
"""

from .standards_kb import IndustrialStandardsCorpus, StandardDocument
from .retriever import HybridStandardsRetriever, RetrievedStandardChunk
from .prompt_augmenter import StandardsPromptAugmenter

__all__ = [
    "IndustrialStandardsCorpus",
    "StandardDocument",
    "HybridStandardsRetriever",
    "RetrievedStandardChunk",
    "StandardsPromptAugmenter",
]
