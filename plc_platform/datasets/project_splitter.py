#!/usr/bin/env python3
"""
plc_platform/datasets/project_splitter.py — Non-Destructive Project-Based Splitter
Reference: DATASET_AND_FINETUNING_STRATEGY.md, PROJECT_ARCHITECTURE.md

Guarantees 0% train/test data contamination by splitting dataset records strictly
on independent project IDs (facilities/manufacturing cells) rather than random record splitting.
"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Any
import random
from collections import defaultdict
from .schema import DatasetRecordV2


@dataclass
class DatasetSplitResult:
    train_records: List[DatasetRecordV2]
    val_records: List[DatasetRecordV2]
    test_records: List[DatasetRecordV2]
    train_projects: Set[str]
    val_projects: Set[str]
    test_projects: Set[str]
    archetype_distribution: Dict[str, Dict[str, int]]
    sector_distribution: Dict[str, Dict[str, int]]
    contamination_verified_zero: bool


class ProjectBasedSplitter:
    """Splits datasets cleanly by project_id to avoid data leakage and contamination."""

    def __init__(self, train_ratio: float = 0.80, val_ratio: float = 0.10, test_ratio: float = 0.10, seed: int = 42):
        assert abs((train_ratio + val_ratio + test_ratio) - 1.0) < 1e-6, "Split ratios must sum to 1.0"
        self.train_ratio = train_ratio
        self.val_ratio = val_ratio
        self.test_ratio = test_ratio
        self.seed = seed

    def split(self, records: List[DatasetRecordV2]) -> DatasetSplitResult:
        """
        Executes non-destructive, project-based train/val/test split.
        """
        if not records:
            return DatasetSplitResult(
                train_records=[],
                val_records=[],
                test_records=[],
                train_projects=set(),
                val_projects=set(),
                test_projects=set(),
                archetype_distribution={},
                sector_distribution={},
                contamination_verified_zero=True
            )

        # 1. Group records by project_id
        project_map: Dict[str, List[DatasetRecordV2]] = defaultdict(list)
        for r in records:
            project_map[r.project_id].append(r)

        unique_projects = sorted(list(project_map.keys()))
        rng = random.Random(self.seed)
        rng.shuffle(unique_projects)

        n_projects = len(unique_projects)
        if n_projects == 1:
            # Single project cannot be partitioned cleanly without cross-leakage; place all in train
            train_projs = set(unique_projects)
            val_projs: Set[str] = set()
            test_projs: Set[str] = set()
        elif n_projects == 2:
            train_projs = {unique_projects[0]}
            val_projs = {unique_projects[1]}
            test_projs = set()
        else:
            n_train = max(1, int(round(n_projects * self.train_ratio)))
            n_val = max(1, int(round(n_projects * self.val_ratio)))
            # Remaining goes to test
            train_projs = set(unique_projects[:n_train])
            val_projs = set(unique_projects[n_train:n_train + n_val])
            test_projs = set(unique_projects[n_train + n_val:])
            if not test_projs and len(val_projs) > 1:
                # Borrow one from val if test is empty
                borrowed = list(val_projs)[-1]
                val_projs.remove(borrowed)
                test_projs.add(borrowed)

        # 2. Collect records for each split
        train_records = [r for p in train_projs for r in project_map[p]]
        val_records = [r for p in val_projs for r in project_map[p]]
        test_records = [r for p in test_projs for r in project_map[p]]

        # 3. Verify zero project overlap
        zero_overlap = (
            len(train_projs & val_projs) == 0 and
            len(train_projs & test_projs) == 0 and
            len(val_projs & test_projs) == 0
        )

        # 4. Compute distributions
        archetype_dist = {
            "train": self._count_field(train_records, "archetype_id"),
            "val": self._count_field(val_records, "archetype_id"),
            "test": self._count_field(test_records, "archetype_id")
        }
        sector_dist = {
            "train": self._count_field(train_records, "sector"),
            "val": self._count_field(val_records, "sector"),
            "test": self._count_field(test_records, "sector")
        }

        return DatasetSplitResult(
            train_records=train_records,
            val_records=val_records,
            test_records=test_records,
            train_projects=train_projs,
            val_projects=val_projs,
            test_projects=test_projs,
            archetype_distribution=archetype_dist,
            sector_distribution=sector_dist,
            contamination_verified_zero=zero_overlap
        )

    def _count_field(self, records: List[DatasetRecordV2], field_name: str) -> Dict[str, int]:
        counts: Dict[str, int] = defaultdict(int)
        for r in records:
            val = getattr(r, field_name, "UNKNOWN")
            counts[val] += 1
        return dict(counts)
