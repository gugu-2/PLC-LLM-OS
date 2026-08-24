"""
repair_dataset.py
=================
Phase 1.1 — Emergency Dataset Rescue

Repairs synthetic_generation_v3_enterprise.jsonl by:
  A) Splitting concatenated JSON objects (the "Extra data" corruption)
  B) Filtering LLM refusals
  C) Normalizing code format (all records use ```iec-st fence)
  D) Quality gate (FUNCTION_BLOCK, length, dedup)

Output: data/synthetic_generation_v3_enterprise_CLEAN.jsonl
"""

import json
import re
import hashlib
import logging
from pathlib import Path

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("DatasetRepair")

# --- Paths ---
BASE_DIR = Path(__file__).resolve().parent.parent.parent
INPUT_FILE  = BASE_DIR / "data" / "synthetic_generation_v3_enterprise.jsonl"
OUTPUT_FILE = BASE_DIR / "data" / "synthetic_generation_v3_enterprise_CLEAN.jsonl"
LOG_FILE    = BASE_DIR / "data" / "repair_log.txt"

# --- Refusal Detection ---
REFUSAL_PHRASES = [
    "cannot provide", "cannot fulfill", "must decline",
    "safety guidelines", "i cannot generate", "i cannot provide",
    "not able to provide actionable", "theoretical perspective",
    "as an ai language model", "i'm not able to", "i am not able to",
    "violates safety", "prohibited use", "actionable engineering implementations"
]

# --- Code Format Detection ---
CODE_FENCE_PATTERN = re.compile(
    r'```(?:iec-st|iec61131|iec 61131|st|pascal|structured.text)?\s*\n(.*?)```',
    re.DOTALL | re.IGNORECASE
)
FUNCTION_BLOCK_PATTERN = re.compile(
    r'\bFUNCTION_BLOCK\b', re.IGNORECASE
)


def extract_all_json_objects(raw_text: str) -> list:
    """
    Step A — Corruption Splitter.

    Uses json.JSONDecoder().raw_decode() in a sliding window to extract
    ALL valid JSON objects from a string, even if multiple objects are
    concatenated without separators on the same line.

    e.g. '{"a":1}{"b":2}' → [{"a":1}, {"b":2}]
    """
    decoder = json.JSONDecoder()
    objects = []
    idx = 0
    text = raw_text.strip()

    while idx < len(text):
        # Skip whitespace between objects
        while idx < len(text) and text[idx] in ' \t\r\n':
            idx += 1
        if idx >= len(text):
            break
        if text[idx] != '{':
            # Not a JSON object start — skip to next '{'
            next_brace = text.find('{', idx)
            if next_brace == -1:
                break
            idx = next_brace
            continue
        try:
            obj, end_idx = decoder.raw_decode(text, idx)
            objects.append(obj)
            idx = end_idx
        except json.JSONDecodeError:
            # Skip this character and try from next position
            idx += 1

    return objects


def is_refusal(content: str) -> bool:
    """Step B — Check if assistant content is an LLM refusal."""
    content_lower = content.lower()
    return any(phrase in content_lower for phrase in REFUSAL_PHRASES)


def normalize_format(record: dict) -> dict:
    """
    Step C — Format Normalizer.

    Ensures the assistant content always uses ```iec-st fence.
    For old records with raw code (no fence), wraps the code.
    """
    messages = record.get("messages", [])
    if len(messages) < 2:
        return record

    assistant_content = messages[1]["content"]

    # Check if already has a code fence
    if CODE_FENCE_PATTERN.search(assistant_content):
        return record  # already normalized

    # Check if it looks like raw IEC 61131-3 code
    if FUNCTION_BLOCK_PATTERN.search(assistant_content):
        # Wrap raw code in a proper fence
        normalized_content = f"```iec-st\n{assistant_content.strip()}\n```"
        messages[1] = {"role": "assistant", "content": normalized_content}
        record["messages"] = messages

    return record


def passes_quality_gate(record: dict, seen_hashes: set) -> tuple:
    """
    Step D — Quality Gate.
    Returns (True, "") if the record passes, or (False, reason) if it fails.
    """
    messages = record.get("messages", [])

    # Must have exactly 2 messages: user + assistant
    if len(messages) < 2:
        return False, "Less than 2 messages"

    user_content      = messages[0].get("content", "")
    assistant_content = messages[1].get("content", "")

    # Minimum length
    if len(assistant_content) < 2000:
        return False, f"Assistant content too short: {len(assistant_content)} chars"

    # Must have FUNCTION_BLOCK (98% of good records do)
    if not FUNCTION_BLOCK_PATTERN.search(assistant_content):
        return False, "Missing FUNCTION_BLOCK keyword"

    # Must have END_IF or END_CASE (any logic)
    if "END_IF" not in assistant_content and "END_CASE" not in assistant_content:
        return False, "Missing END_IF / END_CASE (no logic structure found)"

    # Duplicate detection (hash of first 500 chars of assistant content)
    content_hash = hashlib.sha256(assistant_content[:500].encode()).hexdigest()
    if content_hash in seen_hashes:
        return False, "Duplicate record"
    seen_hashes.add(content_hash)

    return True, ""


def main():
    logger.info(f"=== Dataset Repair Tool ===")
    logger.info(f"Input:  {INPUT_FILE}")
    logger.info(f"Output: {OUTPUT_FILE}")

    if not INPUT_FILE.exists():
        logger.error(f"Input file not found: {INPUT_FILE}")
        return

    # Read raw file content
    raw_content = INPUT_FILE.read_text(encoding="utf-8")
    raw_lines   = raw_content.splitlines()
    logger.info(f"Raw lines in file: {len(raw_lines)}")

    # Statistics
    stats = {
        "total_lines":      len(raw_lines),
        "empty_lines":      0,
        "objects_extracted": 0,
        "refusals_removed":  0,
        "format_normalized": 0,
        "quality_failed":    0,
        "duplicates":        0,
        "saved":             0,
    }

    all_extracted_objects = []
    log_lines = []

    # === Step A: Corruption Splitter ===
    logger.info("Step A: Splitting concatenated JSON objects...")
    for line_num, line in enumerate(raw_lines, start=1):
        stripped = line.strip()
        if not stripped:
            stats["empty_lines"] += 1
            continue

        objects = extract_all_json_objects(stripped)

        if len(objects) == 0:
            log_lines.append(f"[LINE {line_num}] PARSE_FAILED: Could not extract any JSON objects")
        elif len(objects) == 1:
            all_extracted_objects.append((line_num, objects[0], "clean"))
        elif len(objects) > 1:
            log_lines.append(f"[LINE {line_num}] SPLIT: Found {len(objects)} concatenated objects — rescued")
            for obj in objects:
                all_extracted_objects.append((line_num, obj, "rescued"))

    stats["objects_extracted"] = len(all_extracted_objects)
    logger.info(f"  Extracted {stats['objects_extracted']} total objects (from {len(raw_lines)} lines)")

    # === Steps B, C, D: Filter + Normalize + Quality Gate ===
    logger.info("Steps B-D: Filtering refusals, normalizing format, quality gate...")
    seen_hashes = set()
    good_records = []

    for line_num, obj, source in all_extracted_objects:
        messages = obj.get("messages", [])
        if len(messages) < 2:
            log_lines.append(f"[LINE {line_num}] SKIP: Not a valid messages record")
            stats["quality_failed"] += 1
            continue

        assistant_content = messages[1].get("content", "")

        # Step B: Refusal filter
        if is_refusal(assistant_content):
            log_lines.append(f"[LINE {line_num}] REFUSAL_REMOVED: {assistant_content[:80]}")
            stats["refusals_removed"] += 1
            continue

        # Step C: Format normalization
        before_content = assistant_content
        obj = normalize_format(obj)
        after_content  = obj["messages"][1]["content"]
        if before_content != after_content:
            log_lines.append(f"[LINE {line_num}] FORMAT_NORMALIZED: Wrapped raw code in ```iec-st fence")
            stats["format_normalized"] += 1

        # Step D: Quality gate
        passed, reason = passes_quality_gate(obj, seen_hashes)
        if not passed:
            if "Duplicate" in reason:
                stats["duplicates"] += 1
            else:
                stats["quality_failed"] += 1
            log_lines.append(f"[LINE {line_num}] QUALITY_FAILED ({source}): {reason}")
            continue

        good_records.append(obj)

    stats["saved"] = len(good_records)

    # === Step E: Write Output ===
    logger.info(f"Writing {stats['saved']} clean records to {OUTPUT_FILE}...")
    OUTPUT_FILE.parent.mkdir(parents=True, exist_ok=True)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for record in good_records:
            json_str = json.dumps(record, ensure_ascii=False)
            f.write(json_str + "\n")

    # Write repair log
    LOG_FILE.write_text("\n".join(log_lines), encoding="utf-8")

    # === Final Report ===
    logger.info("")
    logger.info("=" * 55)
    logger.info("  REPAIR COMPLETE — FINAL STATISTICS")
    logger.info("=" * 55)
    logger.info(f"  Raw lines in input:         {stats['total_lines']}")
    logger.info(f"  Empty lines skipped:        {stats['empty_lines']}")
    logger.info(f"  JSON objects extracted:     {stats['objects_extracted']}")
    logger.info(f"  Refusals removed:           {stats['refusals_removed']}")
    logger.info(f"  Format normalized:          {stats['format_normalized']}")
    logger.info(f"  Quality gate failures:      {stats['quality_failed']}")
    logger.info(f"  Duplicate records removed:  {stats['duplicates']}")
    logger.info(f"  ✅ Clean records saved:     {stats['saved']}")
    logger.info(f"  Output: {OUTPUT_FILE}")
    logger.info(f"  Log:    {LOG_FILE}")
    logger.info("=" * 55)


if __name__ == "__main__":
    main()
