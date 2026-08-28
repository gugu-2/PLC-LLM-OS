"""
audit_all_datasets.py
=====================
Phase 1.2 — Audit All Data Files

Scans every JSONL file in the data/ directory and produces a
quality report + DATA_CATALOG.md

Quality Tiers:
  TIER_1: >90% records pass all checks → safe for fine-tuning
  TIER_2: 50-90% pass → needs filtering first
  TIER_3: <50% pass  → raw/unverified, archive only
"""

import json
import re
import hashlib
import logging
from pathlib import Path
from datetime import datetime

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("DatasetAudit")

BASE_DIR  = Path(__file__).resolve().parent.parent.parent
DATA_DIR  = BASE_DIR / "data"
CATALOG   = DATA_DIR / "DATA_CATALOG.md"

REFUSAL_PHRASES = [
    "cannot provide", "cannot fulfill", "must decline",
    "safety guidelines", "i cannot", "not able to provide"
]

FB_PATTERN  = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
VAR_PATTERN = re.compile(r'\bVAR_INPUT\b|\bVAR_OUTPUT\b', re.IGNORECASE)
LOGIC_PATTERN = re.compile(r'\bEND_IF\b|\bEND_CASE\b', re.IGNORECASE)


def audit_file(filepath: Path) -> dict:
    """Run a full quality audit on a single JSONL file."""
    result = {
        "file": filepath.name,
        "size_mb": round(filepath.stat().st_size / 1_048_576, 2),
        "total_lines": 0,
        "parse_errors": 0,
        "empty_lines": 0,
        "refusals": 0,
        "has_function_block": 0,
        "has_var_io": 0,
        "has_logic": 0,
        "avg_length": 0,
        "min_length": float("inf"),
        "max_length": 0,
        "good_records": 0,
        "tier": "UNKNOWN",
        "content_hashes": set(),
        "duplicates": 0,
    }

    lengths = []

    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            for line in f:
                result["total_lines"] += 1
                stripped = line.strip()
                if not stripped:
                    result["empty_lines"] += 1
                    continue

                try:
                    obj = json.loads(stripped)
                except json.JSONDecodeError:
                    result["parse_errors"] += 1
                    continue

                messages = obj.get("messages", [])
                if len(messages) < 2:
                    result["parse_errors"] += 1
                    continue

                # Checks
                assistant_content = messages[1].get("content", "")
                content_lower = assistant_content.lower()
                if any(p in content_lower for p in REFUSAL_PHRASES):
                    result["refusals"] += 1
                    continue

                # Add to length stats ONLY if it's not a refusal
                assistant_content = messages[1].get("content", "")
                
                # Dedup
                h = hashlib.sha256(assistant_content[:300].encode()).hexdigest()
                if h in result["content_hashes"]:
                    result["duplicates"] += 1
                result["content_hashes"].add(h)
                
                content_len = len(assistant_content)
                lengths.append(content_len)

                has_fb = bool(FB_PATTERN.search(assistant_content))
                has_var = bool(VAR_PATTERN.search(assistant_content))
                has_logic = bool(LOGIC_PATTERN.search(assistant_content))

                if has_fb: result["has_function_block"] += 1
                if has_var: result["has_var_io"] += 1
                if has_logic: result["has_logic"] += 1

                # A record is only "good" for fine-tuning if it actually contains IEC 61131-3 code
                # And is above 1500 chars (relaxing to match new thresholds)
                if has_fb and has_var and content_len >= 1500:
                    result["good_records"] += 1
                
                result["min_length"] = min(result["min_length"], content_len)
                result["max_length"] = max(result["max_length"], content_len)

    except Exception as e:
        logger.error(f"Failed to read {filepath.name}: {e}")
        result["tier"] = "ERROR"
        return result

    # Compute derived stats
    valid = result["good_records"]
    parseable = valid + result["refusals"] + (result["total_lines"] - result["empty_lines"] - result["parse_errors"] - result["good_records"] - result["refusals"]) # total parsed records
    
    # Actually, pass rate should be valid / (total_lines - empty_lines - parse_errors)
    total_parsed = result["total_lines"] - result["empty_lines"] - result["parse_errors"]
    
    if total_parsed > 0:
        pass_rate = valid / total_parsed
    else:
        pass_rate = 0.0

    result["pass_rate"] = round(pass_rate * 100, 1)
    result["avg_length"] = int(sum(lengths) / len(lengths)) if lengths else 0
    if result["min_length"] == float("inf"):
        result["min_length"] = 0

    # Tier assignment
    if pass_rate >= 0.90:
        result["tier"] = "TIER_1 ✅ Safe for fine-tuning"
    elif pass_rate >= 0.50:
        result["tier"] = "TIER_2 ⚠️ Needs filtering"
    else:
        result["tier"] = "TIER_3 ❌ Archive only"

    del result["content_hashes"]  # not serializable, not needed in report
    return result


def main():
    logger.info("=== Dataset Audit Tool ===")
    logger.info(f"Scanning: {DATA_DIR}")

    jsonl_files = sorted(DATA_DIR.glob("*.jsonl"))
    logger.info(f"Found {len(jsonl_files)} JSONL files to audit")

    all_results = []
    for fp in jsonl_files:
        logger.info(f"  Auditing: {fp.name} ({fp.stat().st_size // 1024} KB)...")
        r = audit_file(fp)
        all_results.append(r)
        logger.info(f"    → {r['good_records']} good / {r['total_lines']} total | Pass: {r['pass_rate']}% | {r['tier']}")

    # === Write DATA_CATALOG.md ===
    lines = [
        "# Data Catalog",
        f"*Generated: {datetime.now().strftime('%Y-%m-%d %H:%M')}*",
        "",
        "---",
        "",
        "## Summary Table",
        "",
        "| File | Size | Total Lines | Good Records | Parse Errors | Refusals | Dups | Pass Rate | Tier |",
        "|------|------|-------------|--------------|--------------|----------|------|-----------|------|",
    ]
    for r in all_results:
        lines.append(
            f"| `{r['file']}` | {r['size_mb']} MB | {r['total_lines']} | "
            f"{r['good_records']} | {r['parse_errors']} | {r['refusals']} | "
            f"{r['duplicates']} | {r['pass_rate']}% | {r['tier']} |"
        )

    lines += [
        "",
        "---",
        "",
        "## Detailed Breakdown",
        "",
    ]

    for r in all_results:
        lines += [
            f"### `{r['file']}`",
            f"- **Size:** {r['size_mb']} MB",
            f"- **Total lines:** {r['total_lines']} ({r['empty_lines']} empty)",
            f"- **JSON parse errors:** {r['parse_errors']}",
            f"- **Refusals filtered:** {r['refusals']}",
            f"- **Duplicate records:** {r['duplicates']}",
            f"- **✅ Good records:** {r['good_records']} ({r['pass_rate']}%)",
            f"- **FUNCTION_BLOCK present:** {r['has_function_block']}",
            f"- **VAR_INPUT/OUTPUT present:** {r['has_var_io']}",
            f"- **END_IF/END_CASE present:** {r['has_logic']}",
            f"- **Avg assistant length:** {r['avg_length']:,} chars",
            f"- **Min / Max length:** {r['min_length']:,} / {r['max_length']:,} chars",
            f"- **Quality Tier:** **{r['tier']}**",
            "",
        ]

    lines += [
        "---",
        "",
        "## Fine-Tuning Usage Guide",
        "",
        "| Tier | Meaning | Action |",
        "|------|---------|--------|",
        "| TIER_1 ✅ | >90% records are valid IEC 61131-3 | Include directly in training |",
        "| TIER_2 ⚠️ | 50-90% valid | Run through `repair_dataset.py` first |",
        "| TIER_3 ❌ | <50% valid | Move to `raw_archive/` — do NOT train on this |",
    ]

    CATALOG.write_text("\n".join(lines), encoding="utf-8")
    logger.info(f"\n✅ DATA_CATALOG.md written to: {CATALOG}")
    logger.info("Audit complete.")


if __name__ == "__main__":
    main()
