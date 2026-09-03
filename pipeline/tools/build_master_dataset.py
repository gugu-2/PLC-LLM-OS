"""
build_master_dataset.py
=======================
Phase 1.3 — Build the Master Training Dataset

Merges TIER_1/TIER_2 (filtered) datasets into a single
clean, shuffled, train/validation split ready for fine-tuning.

Output:
  data/master/train.jsonl
  data/master/validation.jsonl
  data/master/dataset_card.md
"""

import json
import re
import hashlib
import random
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("MasterDatasetBuilder")

BASE_DIR   = Path(__file__).resolve().parent.parent.parent
DATA_DIR   = BASE_DIR / "data"
MASTER_DIR = DATA_DIR / "master"

# Seed for reproducible shuffling and splitting
RANDOM_SEED = 42

# Validation split fraction
VAL_FRACTION = 0.10

# === Approved source datasets (TIER_1 only for first build) ===
# Format: (filename, description)
APPROVED_SOURCES = [
    ("synthetic_generation_v3_enterprise_CLEAN.jsonl",
     "Swarm-generated ultra-complex IEC 61131-3 controllers (cleaned)"),
    ("evol_instruct_dataset.jsonl",
     "Evolved instruction dataset baseline (1648 records)"),
    ("final_verified_dataset.jsonl",
     "Large curated legacy dataset of verified ST logic (5919 records)"),
    ("verified_github_code.jsonl",
     "Verified GitHub PLC code samples"),
    ("verified_oscat.jsonl",
     "Verified OSCAT library code samples"),
]

# Dynamically add all new isolated swarm files (Strategy A)
SWARM_RAW_DIR = DATA_DIR / "swarm_raw"
if SWARM_RAW_DIR.exists():
    for f in SWARM_RAW_DIR.glob("*.json"):
        APPROVED_SOURCES.append((f"swarm_raw/{f.name}", "Isolated cloud swarm raw payload"))

# Dynamically add locally generated files (from local GPU pipeline)
LOCAL_RAW_DIR = DATA_DIR / "local_raw"
if LOCAL_RAW_DIR.exists():
    for f in LOCAL_RAW_DIR.glob("*.json"):
        APPROVED_SOURCES.append((f"local_raw/{f.name}", "Locally generated (Ollama/Qwen2.5-Coder)"))


# Quality gate params
MIN_ASSISTANT_LENGTH = 1500  # chars
REFUSAL_PHRASES = [
    "cannot provide", "cannot fulfill", "must decline",
    "safety guidelines", "i cannot", "not able to provide actionable"
]

FB_PATTERN    = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
LOGIC_PATTERN = re.compile(r'\bEND_IF\b|\bEND_CASE\b', re.IGNORECASE)


def load_and_filter(filepath: Path, source_name: str) -> list:
    """Load a JSONL file and return only quality-passing records."""
    if not filepath.exists():
        logger.warning(f"  File not found, skipping: {filepath.name}")
        return []

    records = []
    skipped = 0

    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        # If it's a single JSON object (from swarm_raw), parse the whole file
        if filepath.suffix == '.json':
            try:
                raw_objs = [json.load(f)]
            except json.JSONDecodeError:
                raw_objs = []
                skipped += 1
        else:
            raw_objs = []
            for line in f:
                stripped = line.strip()
                if not stripped:
                    continue
                try:
                    raw_objs.append(json.loads(stripped))
                except json.JSONDecodeError:
                    skipped += 1
                    
        for obj in raw_objs:
            messages = obj.get("messages", [])
            if len(messages) < 2:
                skipped += 1
                continue

            assistant_content = messages[1].get("content", "")
            content_lower = assistant_content.lower()

            # Skip refusals
            if any(p in content_lower for p in REFUSAL_PHRASES):
                skipped += 1
                continue

            # Skip too-short records
            if len(assistant_content) < MIN_ASSISTANT_LENGTH:
                skipped += 1
                continue

            # Skip records missing core IEC structure
            if not FB_PATTERN.search(assistant_content) and not LOGIC_PATTERN.search(assistant_content):
                skipped += 1
                continue

            # Normalize prompt instructions (GAP-001/ARCH-003)
            user_content = messages[0].get("content", "")
            if "OUTPUT ONLY THE RAW CODE" in user_content or "DO NOT OUTPUT MARKDOWN" in user_content:
                user_content = user_content.replace("OUTPUT ONLY THE RAW CODE", "")
                user_content = user_content.replace("DO NOT OUTPUT MARKDOWN", "Output the code enclosed in a ```iec-st markdown code fence.")
                messages[0]["content"] = user_content
            
            # Normalize response format (BUG-007 double fence fix)
            # Strip existing backtick fences first, then re-wrap
            clean_code = re.sub(r'^```[a-zA-Z\-]*\s*', '', assistant_content, flags=re.MULTILINE)
            clean_code = re.sub(r'^```\s*$', '', clean_code, flags=re.MULTILINE)
            clean_code = clean_code.strip()
            
            assistant_content = f"```iec-st\n{clean_code}\n```"
            messages[1]["content"] = assistant_content

            # Inject System Prompt (ARCH-002)
            if len(messages) > 0 and messages[0].get("role") != "system":
                system_msg = {
                    "role": "system",
                    "content": "You are Lumina AI, an expert industrial automation and IEC 61131-3 controls engineer. Generate mathematically verifiable, deterministic Structured Text (ST), Siemens SCL, or Rockwell L5X code. Ensure all arrays are bounded, all memory addresses are typed, and safety invariants are strictly preserved."
                }
                messages.insert(0, system_msg)
                obj["messages"] = messages

            # Add source metadata
            obj["_source"] = source_name
            records.append(obj)

    logger.info(f"  {filepath.name}: loaded {len(records)}, skipped {skipped}")
    return records


def deduplicate(records: list) -> list:
    """Remove exact duplicates based on first 400 chars of assistant content."""
    seen = set()
    unique = []
    dupes = 0
    for rec in records:
        content = rec["messages"][1]["content"]
        h = hashlib.sha256(content[:400].encode()).hexdigest()
        if h in seen:
            dupes += 1
            continue
        seen.add(h)
        unique.append(rec)
    logger.info(f"  Deduplication: {dupes} duplicates removed, {len(unique)} unique records")
    return unique


def strip_metadata(records: list) -> list:
    """Remove internal _source field before writing (not needed by trainer)."""
    cleaned = []
    for rec in records:
        out = {k: v for k, v in rec.items() if not k.startswith("_")}
        cleaned.append(out)
    return cleaned


def write_jsonl(records: list, filepath: Path):
    """Write records to a JSONL file, one object per line."""
    filepath.parent.mkdir(parents=True, exist_ok=True)
    with open(filepath, "w", encoding="utf-8") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def write_dataset_card(train: list, val: list, source_stats: dict, filepath: Path):
    """Write a markdown dataset card for the master dataset."""
    total = len(train) + len(val)
    train_lengths = [len(r["messages"][1]["content"]) for r in train]
    val_lengths   = [len(r["messages"][1]["content"]) for r in val]
    all_lengths   = train_lengths + val_lengths

    lines = [
        "# Master Training Dataset Card",
        f"*Built: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "## Overview",
        f"- **Total records:** {total:,}",
        f"- **Train split:** {len(train):,} ({100 * len(train) // total}%)",
        f"- **Validation split:** {len(val):,} ({100 * len(val) // total}%)",
        f"- **Random seed:** {RANDOM_SEED}",
        f"- **Validation fraction:** {VAL_FRACTION * 100:.0f}%",
        "",
        "## Content Quality",
        f"- **Avg assistant length:** {sum(all_lengths) // len(all_lengths):,} chars",
        f"- **Min assistant length:** {min(all_lengths):,} chars",
        f"- **Max assistant length:** {max(all_lengths):,} chars",
        f"- **Min threshold applied:** {MIN_ASSISTANT_LENGTH:,} chars",
        "",
        "## Source Breakdown",
        "",
        "| Source File | Records Contributed |",
        "|-------------|---------------------|",
    ]
    for src, count in source_stats.items():
        lines.append(f"| `{src}` | {count:,} |")

    lines += [
        "",
        "## Format",
        "All records follow the ChatML format:",
        "```json",
        '{',
        '  "messages": [',
        '    {"role": "system", "content": "You are Lumina AI..."},',
        '    {"role": "user", "content": "<engineering task prompt>"},',
        '    {"role": "assistant", "content": "```iec-st\\n<IEC 61131-3 code>\\n```"}',
        '  ]',
        '}',
        "```",
        "",
        "## Quality Guarantees",
        "- ✅ Zero JSON parse errors",
        "- ✅ Zero LLM refusals",
        "- ✅ All records >= 1500 chars in assistant content",
        "- ✅ All records have IEC 61131-3 FUNCTION_BLOCK or logic keywords",
        "- ✅ Deduplicated (sha256 hash of first 400 chars)",
        "- ✅ Randomly shuffled with fixed seed for reproducibility",
    ]

    filepath.write_text("\n".join(lines), encoding="utf-8")


def main():
    logger.info("=== Master Dataset Builder ===")

    all_records = []
    source_stats = {}

    # === Load all approved sources ===
    for filename, description in APPROVED_SOURCES:
        filepath = DATA_DIR / filename
        logger.info(f"Loading: {filename}")
        records = load_and_filter(filepath, filename)
        source_stats[filename] = len(records)
        all_records.extend(records)

    logger.info(f"\nTotal records before dedup: {len(all_records)}")

    # === Deduplicate ===
    all_records = deduplicate(all_records)
    logger.info(f"Total records after dedup: {len(all_records)}")

    if len(all_records) == 0:
        logger.error("No valid records found! Check source files.")
        return

    # === Shuffle ===
    random.seed(RANDOM_SEED)
    random.shuffle(all_records)

    # === Train / Validation Split ===
    val_size   = max(1, int(len(all_records) * VAL_FRACTION))
    train_size = len(all_records) - val_size

    val_records   = all_records[:val_size]
    train_records = all_records[val_size:]

    logger.info(f"\nSplit: {len(train_records)} train / {len(val_records)} validation")

    # === Write output ===
    train_path = MASTER_DIR / "train.jsonl"
    val_path   = MASTER_DIR / "validation.jsonl"
    card_path  = MASTER_DIR / "dataset_card.md"

    write_jsonl(train_records, train_path)
    write_jsonl(val_records, val_path)
    write_dataset_card(
        train_records,
        val_records,
        source_stats,
        card_path
    )

    logger.info("")
    logger.info("=" * 55)
    logger.info("  MASTER DATASET BUILD COMPLETE")
    logger.info("=" * 55)
    logger.info(f"  Train:      {train_path} ({len(train_records):,} records)")
    logger.info(f"  Validation: {val_path} ({len(val_records):,} records)")
    logger.info(f"  Card:       {card_path}")
    logger.info("=" * 55)


if __name__ == "__main__":
    main()
