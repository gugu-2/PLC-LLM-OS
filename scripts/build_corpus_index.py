#!/usr/bin/env python3
"""
scripts/build_corpus_index.py — Schema v2.0 Corpus Indexer
Reference: DOC-02, DOC-05

Scans dataset JSON files non-destructively, extracts structured metadata,
and generates machine-readable catalog index files:
- catalog/corpus_index.jsonl
- reports/corpus_inventory.json
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List, Optional

# Add root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import validate_domain
import validate_semantic
import validate_iec
import size_gate

def analyze_dataset_entry(filepath: Path) -> Optional[Dict]:
    """Extract Schema v2.0 metadata from a dataset file."""
    try:
        with open(filepath, "r", encoding="utf-8", errors="replace") as f:
            data = json.load(f)
    except Exception as e:
        return {
            "id": filepath.stem,
            "file": filepath.name,
            "error": f"Failed to parse JSON: {e}",
            "is_valid": False
        }

    user_msg = ""
    assistant_content = ""
    for msg in data.get("messages", []):
        if msg.get("role") == "user":
            user_msg = msg.get("content", "")
        elif msg.get("role") == "assistant":
            assistant_content = msg.get("content", "")

    char_count = len(assistant_content)
    token_est = int(char_count / 3.1)
    
    # Extract FB Name
    fb_name = validate_domain.extract_fb_name(assistant_content)
    
    # Extract Sector & Domain
    domain_res = validate_domain.classify_dataset(fb_name, assistant_content)
    sector = domain_res["matched_sector"] or "unclassified"
    
    # Syntax check
    iec_res = validate_iec.check_parity(assistant_content, min_chars=3500)
    
    # Semantic check
    sem_res = validate_semantic.validate_semantic_st(assistant_content, str(filepath))

    # Complexity tier
    if char_count < 100_000:
        complexity_tier = 1
    elif char_count < 350_000:
        complexity_tier = 2
    else:
        complexity_tier = 3

    subsector = "general"
    if domain_res.get("sanctioned_hits"):
        raw_sub = domain_res["sanctioned_hits"][0].split("::")[-1]
        subsector = re.sub(r'([a-z])([A-Z])', r'\1_\2', raw_sub).lower()

    return {
        "id": filepath.stem,
        "schema_version": "2.0",
        "file": filepath.name,
        "function_block": fb_name,
        "sector": sector,
        "subsector": subsector,
        "complexity_tier": complexity_tier,
        "char_count": char_count,
        "token_estimate": token_est,
        "size_category": size_gate.categorize_size(char_count),
        "validation": {
            "syntax_parity": iec_res["verdict"] == "PASS",
            "domain_verdict": domain_res["verdict"],
            "semantic_verdict": sem_res.verdict,
            "forbidden_hits": domain_res["forbidden_hits"]
        },
        "content_flags": {
            "has_tmr": sem_res.metrics.get("has_tmr", False),
            "has_tmr_discrepancy": sem_res.metrics.get("has_tmr_discrepancy", False),
            "has_mpc": bool(sem_res.metrics.get("mpc_declared_n")),
            "mpc_horizon": sem_res.metrics.get("mpc_declared_n"),
            "has_fsm": "CASE" in assistant_content,
            "has_isa18_alarms": bool(re.search(r'\b(?:ISA.18\.2|HH_Alarm|LL_Alarm)\b', assistant_content, re.IGNORECASE)),
            "declared_vars": sem_res.metrics.get("declared_var_count", 0)
        },
        "indexed_at": datetime.now(timezone.utc).isoformat()
    }

def build_index(input_dir: Path, output_jsonl: Path, report_json: Path, max_files: Optional[int] = None):
    files = sorted(list(input_dir.glob("*.json")))
    if max_files:
        files = files[:max_files]
        
    print(f"Indexing {len(files)} datasets from {input_dir}...")
    output_jsonl.parent.mkdir(parents=True, exist_ok=True)
    report_json.parent.mkdir(parents=True, exist_ok=True)

    records = []
    with open(output_jsonl, "w", encoding="utf-8") as out_f:
        for idx, fp in enumerate(files):
            rec = analyze_dataset_entry(fp)
            if rec:
                records.append(rec)
                out_f.write(json.dumps(rec) + "\n")
            if (idx + 1) % 100 == 0 or (idx + 1) == len(files):
                print(f"  Processed {idx + 1}/{len(files)}...")

    # Aggregations
    sector_dist = {}
    size_dist = {}
    syntax_pass = sum(1 for r in records if r.get("validation", {}).get("syntax_parity"))
    domain_pass = sum(1 for r in records if r.get("validation", {}).get("domain_verdict") == "PASS")
    semantic_pass = sum(1 for r in records if r.get("validation", {}).get("semantic_verdict") == "PASS")
    semantic_warn = sum(1 for r in records if r.get("validation", {}).get("semantic_verdict") == "WARN")
    semantic_fail = sum(1 for r in records if r.get("validation", {}).get("semantic_verdict") == "FAIL")

    for r in records:
        sec = r.get("sector", "unknown")
        sector_dist[sec] = sector_dist.get(sec, 0) + 1
        sz = r.get("size_category", "unknown")
        size_dist[sz] = size_dist.get(sz, 0) + 1

    summary = {
        "indexed_count": len(records),
        "source_directory": str(input_dir),
        "catalog_file": str(output_jsonl),
        "syntax_pass_count": syntax_pass,
        "domain_pass_count": domain_pass,
        "semantic_pass_count": semantic_pass,
        "semantic_warn_count": semantic_warn,
        "semantic_fail_count": semantic_fail,
        "sector_distribution": sector_dist,
        "size_distribution": size_dist
    }

    with open(report_json, "w", encoding="utf-8") as rep_f:
        json.dump(summary, rep_f, indent=2)

    print(f"\nIndex completed:")
    print(f"  Catalog: {output_jsonl} ({len(records)} entries)")
    print(f"  Summary: {report_json}")
    print(f"  Domain PASS: {domain_pass}/{len(records)} | Syntax PASS: {syntax_pass}/{len(records)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Schema v2.0 Corpus Indexer")
    parser.add_argument("--input-dir", default="data/swarm_raw", help="Path to raw datasets")
    parser.add_argument("--output", default="catalog/corpus_index.jsonl", help="Output JSONL index")
    parser.add_argument("--report", default="reports/corpus_inventory.json", help="Summary report path")
    parser.add_argument("--max-files", type=int, default=None, help="Limit number of files for quick testing")
    args = parser.parse_args()

    build_index(Path(args.input_dir), Path(args.output), Path(args.report), max_files=args.max_files)
