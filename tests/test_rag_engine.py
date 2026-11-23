#!/usr/bin/env python3
"""
tests/test_rag_engine.py — Unit Tests for Industrial Standards Hybrid RAG Engine
Tests corpus integrity, BM25 + Dense vector retrieval, RRF fusion, and prompt augmentation.
"""

import pytest
from plc_platform.rag import (
    IndustrialStandardsCorpus,
    HybridStandardsRetriever,
    StandardsPromptAugmenter
)


def test_standards_corpus_integrity():
    docs = IndustrialStandardsCorpus.get_all_documents()
    assert len(docs) >= 12
    standards = {d.standard_name for d in docs}
    assert "ISA-88" in standards
    assert "PACKML" in standards
    assert "ISA-18.2" in standards
    assert "IEC-61131-3" in standards
    assert "SIEMENS" in standards
    assert "ROCKWELL" in standards
    assert "BECKHOFF" in standards


def test_packml_retrieval():
    retriever = HybridStandardsRetriever()
    results = retriever.retrieve("What are the PackML machine states for execute and holding?", top_k=2)
    assert len(results) > 0
    top = results[0]
    assert top.standard_name == "PACKML"
    assert "EXECUTE" in top.content
    assert "HOLDING" in top.content
    assert top.score > 0


def test_alarm_deadband_retrieval():
    retriever = HybridStandardsRetriever()
    results = retriever.retrieve("How to compute alarm deadband hysteresis and flood suppression in ISA-18.2?", top_k=1)
    assert len(results) == 1
    top = results[0]
    assert top.standard_name == "ISA-18.2"
    assert "Deadband" in top.content
    assert "Flood" in top.content


def test_vendor_and_sector_filtering():
    retriever = HybridStandardsRetriever()
    # Test Rockwell filtering
    rockwell_res = retriever.retrieve("Add-On Instruction routine", top_k=2, vendor="ROCKWELL")
    assert len(rockwell_res) > 0
    assert all(r.vendor in ("ROCKWELL", "ALL") for r in rockwell_res)

    # Test Automotive sector filtering
    auto_res = retriever.retrieve("Robotic welding laser battery", top_k=2, sector="AUTOMOTIVE")
    assert len(auto_res) > 0
    assert any(r.sector == "AUTOMOTIVE" for r in auto_res)


def test_abbreviation_expansion():
    retriever = HybridStandardsRetriever()
    # "cip" should expand to "clean in place sanitization caustic wash"
    results = retriever.retrieve("CIP cycle", top_k=1)
    assert len(results) == 1
    assert "SECTOR-FB-001" in results[0].doc_id or "food-beverage" in results[0].tags


def test_prompt_augmenter():
    augmenter = StandardsPromptAugmenter()
    base = "Generate IEC 61131-3 Function Block for Rotary Bottle Filler."
    augmented = augmenter.augment_prompt(
        base_prompt=base,
        query="Food beverage aseptic rotary bottling sanitization",
        top_k=2,
        sector="FOOD_BEVERAGE"
    )
    assert base in augmented
    assert "<!-- INDUSTRIAL STANDARDS & OEM SPECIFICATION CONTEXT (RAG INJECTED) -->" in augmented
    assert "Standard Reference [1]" in augmented
    assert "Aseptic" in augmented
