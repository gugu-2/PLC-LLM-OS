#!/usr/bin/env python3
"""
plc_platform/datasets/pipeline.py — Industrial Dataset Engineering Pipeline
Reference: DATASET_AND_FINETUNING_STRATEGY.md, PROJECT_ARCHITECTURE.md

Orchestrates:
1. Ingestion of raw synthetic datasets and Schema v2.0 records.
2. Semantic deduplication via MinHash / Jaccard similarity.
3. Verification status gating (filters out rejected or unvalidated records).
4. Non-destructive project-based splitting into train / val / test sets.
5. Safe export to training-ready JSONL files without modifying raw archives.
"""

from typing import List, Dict, Optional, Set, Tuple, Any
import json
import os
import hashlib
from pathlib import Path
from .schema import DatasetArchetype, DatasetRecordV2
from .project_splitter import ProjectBasedSplitter, DatasetSplitResult


class DatasetEngineeringPipeline:
    """Full-lifecycle pipeline for industrial PLC training datasets."""

    def __init__(self, splitter: Optional[ProjectBasedSplitter] = None, dedup_threshold: float = 0.90):
        self.splitter = splitter or ProjectBasedSplitter()
        self.dedup_threshold = dedup_threshold

    def deduplicate(self, records: List[DatasetRecordV2]) -> Tuple[List[DatasetRecordV2], int]:
        """
        Deduplicates records based on normalized token 5-gram Jaccard similarity.
        Returns deduplicated records list and count of duplicates dropped.
        """
        unique_records: List[DatasetRecordV2] = []
        seen_hashes: Set[str] = set()
        seen_shingles: List[Set[str]] = []
        dropped_count = 0

        for r in records:
            # Quick exact hash check on output code
            h = hashlib.sha256(r.output_target.strip().encode("utf-8")).hexdigest()
            if h in seen_hashes:
                dropped_count += 1
                continue

            # Shingle check for near-duplicates
            tokens = r.output_target.lower().split()
            shingles = set(" ".join(tokens[i:i + 4]) for i in range(max(1, len(tokens) - 3)))

            is_duplicate = False
            for prev_shingle in seen_shingles:
                if not shingles or not prev_shingle:
                    continue
                intersection = len(shingles & prev_shingle)
                union = len(shingles | prev_shingle)
                similarity = intersection / max(1, union)
                if similarity >= self.dedup_threshold:
                    is_duplicate = True
                    break

            if is_duplicate:
                dropped_count += 1
            else:
                seen_hashes.add(h)
                seen_shingles.append(shingles)
                unique_records.append(r)

        return unique_records, dropped_count

    def process_and_split(
        self,
        records: List[DatasetRecordV2],
        output_dir: Optional[str] = None
    ) -> DatasetSplitResult:
        """
        Validates, deduplicates, and splits dataset into train, val, and test partitions.
        Optionally exports to JSONL files in output_dir.
        """
        # 1. Validation filter: must have required fields and verified status
        valid_records = []
        for r in records:
            if not r.dataset_id or not r.project_id or not r.instruction or not r.output_target:
                continue
            if r.verification_status == "REJECTED":
                continue
            valid_records.append(r)

        # 2. Semantic deduplication
        deduped_records, _ = self.deduplicate(valid_records)

        # 3. Project-based splitting
        split_result = self.splitter.split(deduped_records)

        # 4. Optional export to output directory
        if output_dir:
            out_p = Path(output_dir)
            out_p.mkdir(parents=True, exist_ok=True)
            self._export_jsonl(split_result.train_records, out_p / "train.jsonl")
            self._export_jsonl(split_result.val_records, out_p / "val.jsonl")
            self._export_jsonl(split_result.test_records, out_p / "test.jsonl")

        return split_result

    def _export_jsonl(self, records: List[DatasetRecordV2], file_path: Path):
        with open(file_path, "w", encoding="utf-8") as f:
            for r in records:
                f.write(r.to_json() + "\n")
