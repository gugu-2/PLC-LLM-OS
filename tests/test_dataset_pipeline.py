#!/usr/bin/env python3
"""
tests/test_dataset_pipeline.py — Unit Tests for 10-Archetype Dataset Pipeline & Splitting
Tests Schema v2.0 generation across DS-01..DS-10, MinHash dedup, and project-based zero-contamination splitting.
"""

import pytest
import tempfile
import os
import json
from pathlib import Path
from plc_platform.datasets import (
    DatasetArchetype,
    DatasetRecordV2,
    DatasetArchetypeGenerator,
    ProjectBasedSplitter,
    DatasetEngineeringPipeline
)


def test_generate_all_10_archetypes():
    for arch in DatasetArchetype:
        rec = DatasetArchetypeGenerator.generate_sample(
            archetype=arch,
            project_id=f"PROJ-TEST-{arch.value}",
            sector="AUTOMOTIVE",
            vendor="SIEMENS",
            language="STRUCTURED_TEXT"
        )
        assert rec.archetype_id == arch.value
        assert rec.dataset_id.startswith(arch.value.replace("-", ""))
        assert len(rec.instruction) > 5
        assert len(rec.output_target) > 10
        assert rec.verification_status == "VERIFIED_STATIC_SMT"

        # Test serialization round-trip
        json_str = rec.to_json()
        assert arch.value in json_str
        d = json.loads(json_str)
        reloaded = DatasetRecordV2.from_dict(d)
        assert reloaded.dataset_id == rec.dataset_id


def test_project_based_splitting_zero_contamination():
    # Create 20 records distributed across 5 independent projects
    records = []
    projects = [f"FACILITY_{i}" for i in range(1, 6)]
    for i, proj in enumerate(projects):
        for arch in [DatasetArchetype.DS_01_CONVERSATIONS, DatasetArchetype.DS_03_VERIFIED_CODE, DatasetArchetype.DS_08_SAFETY_VALIDATION]:
            records.append(DatasetArchetypeGenerator.generate_sample(
                archetype=arch,
                project_id=proj,
                sector="AUTOMOTIVE"
            ))

    splitter = ProjectBasedSplitter(train_ratio=0.6, val_ratio=0.2, test_ratio=0.2, seed=42)
    result = splitter.split(records)

    assert result.contamination_verified_zero is True
    # Verify mathematical disjointness
    assert len(result.train_projects & result.val_projects) == 0
    assert len(result.train_projects & result.test_projects) == 0
    assert len(result.val_projects & result.test_projects) == 0
    assert len(result.train_records) > 0
    assert len(result.val_records) > 0
    assert len(result.test_records) > 0


def test_pipeline_deduplication():
    pipeline = DatasetEngineeringPipeline(dedup_threshold=0.85)

    base_rec = DatasetArchetypeGenerator.generate_sample(
        DatasetArchetype.DS_03_VERIFIED_CODE, project_id="PROJ_A"
    )
    dup_rec = DatasetRecordV2.from_dict(base_rec.to_dict())
    dup_rec.dataset_id = "DS03-DUPLICATE"

    records = [base_rec, dup_rec]
    deduped, dropped = pipeline.deduplicate(records)

    assert dropped == 1
    assert len(deduped) == 1
    assert deduped[0].dataset_id == base_rec.dataset_id


def test_pipeline_export_jsonl():
    with tempfile.TemporaryDirectory() as tmpdir:
        records = []
        for i in range(10):
            records.append(DatasetArchetypeGenerator.generate_sample(
                DatasetArchetype.DS_03_VERIFIED_CODE,
                project_id=f"PROJ_PLANT_{i}"
            ))

        pipeline = DatasetEngineeringPipeline()
        split_res = pipeline.process_and_split(records, output_dir=tmpdir)

        train_file = Path(tmpdir) / "train.jsonl"
        val_file = Path(tmpdir) / "val.jsonl"
        test_file = Path(tmpdir) / "test.jsonl"

        assert train_file.exists()
        assert val_file.exists()
        assert test_file.exists()

        # Verify JSONL lines can be parsed
        with open(train_file, "r", encoding="utf-8") as f:
            lines = f.readlines()
            assert len(lines) == len(split_res.train_records)
            first_obj = json.loads(lines[0])
            assert "dataset_id" in first_obj
            assert "output_target" in first_obj
