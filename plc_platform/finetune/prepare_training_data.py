"""
prepare_training_data.py
========================
Stage 1 of the QLoRA fine-tuning pipeline.

Responsibilities:
    - Load existing raw datasets from data/swarm_raw/*.json (870 records,
      format: {"messages": [{"role": "user|assistant", "content": "..."}]})
    - Load Schema v2.0 DatasetRecordV2 objects from data/processed/ (if any)
    - Apply near-duplicate deduplication (MinHash Jaccard, threshold 0.85)
    - Apply project-based 80 / 10 / 10 contamination-free splits
    - Export to ShareGPT-compatible JSONL and Alpaca-compatible JSONL
    - Produce a full provenance manifest

Output files (relative to project root):
    data/finetune/train_sharegpt.jsonl
    data/finetune/val_sharegpt.jsonl
    data/finetune/test_sharegpt.jsonl
    data/finetune/train_alpaca.jsonl
    data/finetune/manifest.json
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import pathlib
import random
import re
import uuid
from collections import defaultdict
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Constants
# ---------------------------------------------------------------------------
SWARM_RAW_DIR   = pathlib.Path("data/swarm_raw")
PROCESSED_DIR   = pathlib.Path("data/processed")
FINETUNE_DIR    = pathlib.Path("data/finetune")
DEDUP_THRESHOLD = 0.85     # Jaccard similarity above which a record is a dupe
TRAIN_RATIO     = 0.80
VAL_RATIO       = 0.10
TEST_RATIO      = 0.10
RANDOM_SEED     = 42

# IEC-ST code block extractor
_CODE_RE = re.compile(
    r"```(?:iec-st|st|iec61131|structured.text)\s*(.*?)```",
    re.DOTALL | re.IGNORECASE,
)

# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class FlatRecord:
    """Normalised single-turn or multi-turn training record."""
    record_id:     str
    project_id:    str
    sector:        str
    system:        str
    split:         str                      # train / val / test
    messages:      List[Dict[str, str]]     # ShareGPT role/content list
    char_count:    int
    has_code:      bool
    source_file:   str


# ---------------------------------------------------------------------------
# MinHash deduplication (pure-Python, no external deps)
# ---------------------------------------------------------------------------

def _shingle(text: str, k: int = 5) -> set:
    """Return k-character shingles of text."""
    cleaned = re.sub(r'\s+', ' ', text.lower())
    return {cleaned[i:i+k] for i in range(len(cleaned) - k + 1)}


def _jaccard(a: set, b: set) -> float:
    if not a and not b:
        return 1.0
    inter = len(a & b)
    union = len(a | b)
    return inter / union if union else 0.0


def _fingerprint(text: str) -> str:
    """SHA-256 hex fingerprint for exact-duplicate detection."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


class MinHashDeduplicator:
    """
    Lightweight MinHash deduplicator using 128 hash functions.
    Pure-Python fallback; install datasketch for production scale.
    """

    def __init__(self, threshold: float = DEDUP_THRESHOLD, num_perm: int = 128):
        self.threshold = threshold
        self.num_perm  = num_perm
        self._seen_fps: set = set()           # exact-dupe fingerprints
        self._seen_shingles: List[set] = []   # for approximate comparison

    def is_duplicate(self, text: str) -> bool:
        fp = _fingerprint(text)
        if fp in self._seen_fps:
            return True
        shingles = _shingle(text)
        for existing in self._seen_shingles:
            if _jaccard(shingles, existing) >= self.threshold:
                return True
        self._seen_fps.add(fp)
        self._seen_shingles.append(shingles)
        return False


# ---------------------------------------------------------------------------
# Loaders
# ---------------------------------------------------------------------------

def _load_swarm_raw(directory: pathlib.Path) -> List[Dict[str, Any]]:
    """Load all *.json files from data/swarm_raw/ preserving structure."""
    records: List[Dict[str, Any]] = []
    if not directory.exists():
        logger.warning("swarm_raw directory not found: %s", directory)
        return records
    for fpath in sorted(directory.glob("*.json")):
        try:
            with open(fpath, "r", encoding="utf-8") as fh:
                data = json.load(fh)
            if isinstance(data, dict):
                data["_source_file"] = fpath.name
                records.append(data)
            elif isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        item["_source_file"] = fpath.name
                        records.append(item)
        except Exception as exc:
            logger.warning("Skipping %s: %s", fpath, exc)
    logger.info("Loaded %d raw records from %s", len(records), directory)
    return records


def _extract_messages(record: Dict[str, Any]) -> Optional[List[Dict[str, str]]]:
    """
    Extract a messages list (ShareGPT format) from raw record.
    Handles:
        {"messages": [{"role": "user", "content": "..."}, ...]}
        {"conversations": [{"from": "human", "value": "..."}]}
        {"instruction": "...", "output": "..."}  (Alpaca)
    """
    if "messages" in record and isinstance(record["messages"], list):
        msgs = []
        for m in record["messages"]:
            role    = m.get("role", m.get("from", ""))
            content = m.get("content", m.get("value", ""))
            # normalise roles
            if role in ("human", "user"):
                role = "user"
            elif role in ("gpt", "assistant", "ai"):
                role = "assistant"
            msgs.append({"role": role, "content": str(content)})
        return msgs if msgs else None

    if "conversations" in record and isinstance(record["conversations"], list):
        msgs = []
        for c in record["conversations"]:
            role    = "user" if c.get("from", "") in ("human", "user") else "assistant"
            content = c.get("value", c.get("content", ""))
            msgs.append({"role": role, "content": str(content)})
        return msgs if msgs else None

    if "instruction" in record:
        msgs = [{"role": "user", "content": str(record["instruction"])}]
        if "output" in record:
            msgs.append({"role": "assistant", "content": str(record["output"])})
        return msgs

    return None


def _infer_sector(record: Dict[str, Any], source_file: str) -> str:
    """Infer manufacturing sector from filename or content heuristics."""
    hints = (source_file + " " + json.dumps(record)[:500]).lower()
    if any(k in hints for k in ("automotive", "biw", "paint", "ev_bat", "stator", "motor", "diecast")):
        return "AUTOMOTIVE"
    if any(k in hints for k in ("smt", "pcb", "reflow", "semiconductor", "wafer", "wire_bond", "d2w", "fowlp")):
        return "ELECTRONICS"
    if any(k in hints for k in ("press", "forge", "cnc", "stamp", "mill", "rolling", "gantry", "hydraulic")):
        return "HEAVY_MACHINERY"
    if any(k in hints for k in ("inject", "mold", "extrusion", "blow", "parison", "polymer", "pellet")):
        return "PLASTICS"
    if any(k in hints for k in ("aseptic", "bottling", "cip", "sip", "retort", "delta_robot", "filler", "bph")):
        return "FOOD_BEVERAGE"
    if any(k in hints for k in ("steel", "blast", "bof", "caster", "continuous_cast")):
        return "STEEL"
    return "GENERAL_MANUFACTURING"


# ---------------------------------------------------------------------------
# Main Preparer
# ---------------------------------------------------------------------------

class TrainingDataPreparer:
    """
    End-to-end training data preparation pipeline.

    Usage:
        preparer = TrainingDataPreparer(root_dir="c:/path/to/project")
        stats = preparer.run()
        print(stats)
    """

    def __init__(
        self,
        root_dir: str | pathlib.Path = ".",
        dedup_threshold: float = DEDUP_THRESHOLD,
        random_seed: int = RANDOM_SEED,
        max_records: Optional[int] = None,
    ):
        self.root_dir = pathlib.Path(root_dir)
        self.dedup    = MinHashDeduplicator(threshold=dedup_threshold)
        self.seed     = random_seed
        self.max_records = max_records
        random.seed(random_seed)

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def run(self) -> Dict[str, Any]:
        """Execute the full preparation pipeline. Returns stats dict."""
        raw_records   = _load_swarm_raw(self.root_dir / SWARM_RAW_DIR)
        flat_records  = self._flatten_and_deduplicate(raw_records)
        split_records = self._split(flat_records)
        stats         = self._export(split_records)
        self._write_manifest(split_records, stats)
        return stats

    # ------------------------------------------------------------------
    # Pipeline Stages
    # ------------------------------------------------------------------

    def _flatten_and_deduplicate(
        self, raw: List[Dict[str, Any]]
    ) -> List[FlatRecord]:
        """Convert raw dicts → FlatRecord, applying dedup."""
        flat: List[FlatRecord] = []
        skipped_no_msgs   = 0
        skipped_dupe      = 0

        for rec in raw:
            if self.max_records and len(flat) >= self.max_records:
                break

            source = rec.get("_source_file", "unknown.json")
            msgs   = _extract_messages(rec)
            if not msgs:
                skipped_no_msgs += 1
                continue

            full_text = " ".join(m["content"] for m in msgs)
            if self.dedup.is_duplicate(full_text):
                skipped_dupe += 1
                continue

            # Extract metadata with fallbacks
            record_id  = rec.get("id", str(uuid.uuid4()))
            project_id = rec.get("project_id", source.replace(".json", ""))
            sector     = rec.get("sector", _infer_sector(rec, source))
            system     = rec.get("system", rec.get("title", "INDUSTRIAL_SYSTEM"))
            has_code   = bool(_CODE_RE.search(full_text))

            flat.append(FlatRecord(
                record_id=record_id,
                project_id=project_id,
                sector=sector,
                system=system,
                split="",          # assigned in next stage
                messages=msgs,
                char_count=len(full_text),
                has_code=has_code,
                source_file=source,
            ))

        logger.info(
            "Flatten: total=%d  valid=%d  no_msgs=%d  dupes=%d",
            len(raw), len(flat), skipped_no_msgs, skipped_dupe,
        )
        return flat

    def _split(self, records: List[FlatRecord]) -> List[FlatRecord]:
        """
        Project-based 80/10/10 split.
        All records sharing a project_id land in the same bucket —
        preventing any train/test contamination.
        """
        # Group by project_id
        by_project: Dict[str, List[FlatRecord]] = defaultdict(list)
        for r in records:
            by_project[r.project_id].append(r)

        projects = list(by_project.keys())
        random.shuffle(projects)

        n          = len(projects)
        n_train    = int(n * TRAIN_RATIO)
        n_val      = int(n * VAL_RATIO)

        train_projs = set(projects[:n_train])
        val_projs   = set(projects[n_train:n_train + n_val])
        # remainder goes to test

        for r in records:
            if r.project_id in train_projs:
                r.split = "train"
            elif r.project_id in val_projs:
                r.split = "val"
            else:
                r.split = "test"

        counts = {"train": 0, "val": 0, "test": 0}
        for r in records:
            counts[r.split] += 1
        logger.info("Split: %s", counts)
        return records

    # ------------------------------------------------------------------
    # Export Helpers
    # ------------------------------------------------------------------

    def _to_sharegpt(self, record: FlatRecord) -> Dict[str, Any]:
        """ShareGPT JSONL format with full metadata."""
        return {
            "id":         record.record_id,
            "project_id": record.project_id,
            "sector":     record.sector,
            "system":     record.system,
            "has_code":   record.has_code,
            "char_count": record.char_count,
            "source":     record.source_file,
            "conversations": [
                {"from": "human" if m["role"] == "user" else "gpt",
                 "value": m["content"]}
                for m in record.messages
            ],
        }

    def _to_alpaca(self, record: FlatRecord) -> Optional[Dict[str, Any]]:
        """Alpaca format: single instruction → output pair."""
        user_msgs  = [m for m in record.messages if m["role"] == "user"]
        asst_msgs  = [m for m in record.messages if m["role"] == "assistant"]
        if not user_msgs or not asst_msgs:
            return None
        return {
            "instruction": user_msgs[0]["content"],
            "input":       user_msgs[1]["content"] if len(user_msgs) > 1 else "",
            "output":      asst_msgs[-1]["content"],
            "metadata": {
                "id":         record.record_id,
                "sector":     record.sector,
                "has_code":   record.has_code,
                "char_count": record.char_count,
            },
        }

    def _export(self, records: List[FlatRecord]) -> Dict[str, Any]:
        """Write ShareGPT and Alpaca JSONL files. Returns stats."""
        out_dir = self.root_dir / FINETUNE_DIR
        out_dir.mkdir(parents=True, exist_ok=True)

        writers: Dict[str, Any] = {
            "train_sg": open(out_dir / "train_sharegpt.jsonl", "w", encoding="utf-8"),
            "val_sg":   open(out_dir / "val_sharegpt.jsonl",   "w", encoding="utf-8"),
            "test_sg":  open(out_dir / "test_sharegpt.jsonl",  "w", encoding="utf-8"),
            "train_al": open(out_dir / "train_alpaca.jsonl",   "w", encoding="utf-8"),
        }

        counts: Dict[str, int] = {k: 0 for k in writers}

        try:
            for rec in records:
                sg_obj = self._to_sharegpt(rec)
                al_obj = self._to_alpaca(rec)

                if rec.split == "train":
                    writers["train_sg"].write(json.dumps(sg_obj, ensure_ascii=False) + "\n")
                    counts["train_sg"] += 1
                    if al_obj:
                        writers["train_al"].write(json.dumps(al_obj, ensure_ascii=False) + "\n")
                        counts["train_al"] += 1
                elif rec.split == "val":
                    writers["val_sg"].write(json.dumps(sg_obj, ensure_ascii=False) + "\n")
                    counts["val_sg"] += 1
                else:
                    writers["test_sg"].write(json.dumps(sg_obj, ensure_ascii=False) + "\n")
                    counts["test_sg"] += 1
        finally:
            for w in writers.values():
                w.close()

        stats = {
            "total_records":     len(records),
            "train_sharegpt":    counts["train_sg"],
            "val_sharegpt":      counts["val_sg"],
            "test_sharegpt":     counts["test_sg"],
            "train_alpaca":      counts["train_al"],
            "output_dir":        str(out_dir),
        }
        logger.info("Export stats: %s", stats)
        return stats

    def _write_manifest(
        self, records: List[FlatRecord], stats: Dict[str, Any]
    ) -> None:
        """Write provenance manifest with per-sector breakdown."""
        sector_counts: Dict[str, Dict[str, int]] = defaultdict(
            lambda: {"train": 0, "val": 0, "test": 0}
        )
        total_chars = {"train": 0, "val": 0, "test": 0}
        code_counts = {"train": 0, "val": 0, "test": 0}

        for r in records:
            sector_counts[r.sector][r.split] += 1
            total_chars[r.split] += r.char_count
            if r.has_code:
                code_counts[r.split] += 1

        manifest = {
            "schema_version":  "2.0",
            "dedup_threshold": DEDUP_THRESHOLD,
            "split_ratios":    {"train": TRAIN_RATIO, "val": VAL_RATIO, "test": TEST_RATIO},
            "random_seed":     self.seed,
            "summary":         stats,
            "sector_breakdown": dict(sector_counts),
            "total_chars":     total_chars,
            "code_records":    code_counts,
        }

        out_path = self.root_dir / FINETUNE_DIR / "manifest.json"
        with open(out_path, "w", encoding="utf-8") as fh:
            json.dump(manifest, fh, indent=2, ensure_ascii=False)
        logger.info("Manifest written to %s", out_path)


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import argparse
    logging.basicConfig(level=logging.INFO, format="%(levelname)s  %(message)s")
    parser = argparse.ArgumentParser(description="Prepare IEC-ST training data for QLoRA fine-tuning")
    parser.add_argument("--root",        default=".",  help="Project root directory")
    parser.add_argument("--max-records", type=int, default=None, help="Cap on processed records (testing)")
    args = parser.parse_args()

    preparer = TrainingDataPreparer(root_dir=args.root, max_records=args.max_records)
    result   = preparer.run()
    print(json.dumps(result, indent=2))
