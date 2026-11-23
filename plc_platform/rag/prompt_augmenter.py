#!/usr/bin/env python3
"""
plc_platform/rag/prompt_augmenter.py — Engineering Context Injector for LLM Prompts
Reference: PLC_DOMAIN_INTELLIGENCE.md, AGENTIC_ENGINEERING_WORKFLOW.md

Takes retrieved standards chunks and formats them into high-signal engineering context
blocks for LLM system/user prompts.
"""

from typing import List, Optional
from .retriever import RetrievedStandardChunk, HybridStandardsRetriever


class StandardsPromptAugmenter:
    """Injects industrial standards knowledge into LLM engineering prompts."""

    def __init__(self, retriever: Optional[HybridStandardsRetriever] = None):
        self.retriever = retriever or HybridStandardsRetriever()

    def augment_prompt(
        self,
        base_prompt: str,
        query: str,
        top_k: int = 3,
        vendor: Optional[str] = None,
        sector: Optional[str] = None,
        standard: Optional[str] = None
    ) -> str:
        """
        Retrieves top relevant standards and appends a structured engineering context block.
        """
        chunks = self.retriever.retrieve(
            query=query,
            top_k=top_k,
            vendor=vendor,
            sector=sector,
            standard=standard
        )

        if not chunks:
            return base_prompt

        context_lines = [
            base_prompt,
            "",
            "<!-- INDUSTRIAL STANDARDS & OEM SPECIFICATION CONTEXT (RAG INJECTED) -->",
            "> [!NOTE] Industrial standards and OEM guidelines retrieved for this engineering task:"
        ]

        for i, c in enumerate(chunks, 1):
            context_lines.extend([
                f"### Standard Reference [{i}]: {c.title} ({c.standard_name})",
                f"- **Vendor / Sector Scope**: Vendor: {c.vendor} | Sector: {c.sector} | Category: {c.category}",
                f"- **RRF Relevance Score**: {c.score}",
                "```text",
                c.content,
                "```",
                ""
            ])

        context_lines.append("<!-- END INDUSTRIAL STANDARDS CONTEXT -->")
        return "\n".join(context_lines)
