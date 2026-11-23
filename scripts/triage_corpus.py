#!/usr/bin/env python3
"""
scripts/triage_corpus.py — Non-Destructive Multi-Stage Corpus Triage Orchestrator
Reference: DOC-01, DOC-02, DOC-05

Executes the full 4-stage validation and governance pipeline:
Stage 1: Domain Verification (Sanctioned Manufacturing Sectors vs Forbidden Domains)
Stage 2: Structural Syntax Parity (Balanced IF, CASE, FOR, Comments, Physical Units)
Stage 3: Cyber-Physical Semantics (VAR completeness, State-Space nxn, FSM, MPC unroll, 2oo3 TMR)
Stage 4: Size Gating (Classifies Stubs <100k, Standard 100k-350k, Extended 350k-700k, Ultra-Dense >700k)

IMPORTANT: STRICTLY NON-DESTRUCTIVE!
Original datasets in data/swarm_raw/ are NEVER deleted or modified.
Verified datasets are non-destructively copied to data/verified/{sector}/ for training convenience.
"""

import os
import sys
import json
import shutil
import argparse
from pathlib import Path
from datetime import datetime, timezone
from typing import Dict, List

# Add root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import validate_domain
import validate_iec
import validate_semantic
import size_gate

def run_triage(
    input_dir: Path,
    verified_base_dir: Path,
    report_path: Path,
    copy_verified: bool = True,
    max_files: int = None
) -> Dict:
    files = list(input_dir.glob("*.json"))
    if max_files:
        files = files[:max_files]

    print(f"\n=======================================================")
    print(f"  LUMINA NON-DESTRUCTIVE CORPUS TRIAGE PIPELINE")
    print(f"  Source Directory: {input_dir}")
    print(f"  Total Datasets to Audit: {len(files)}")
    print(f"  Policy: Zero deletions — original datasets preserved")
    print(f"=======================================================\n")

    triage_results = {
        "verified_pass": [],
        "quarantined_semantic_warn": [],
        "quarantined_stub_size": [],
        "rejected_off_target_domain": [],
        "rejected_syntax_fail": []
    }

    sector_counts = {}

    for idx, fp in enumerate(files):
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
            content = next((m.get("content", "") for m in data.get("messages", []) if m.get("role") == "assistant"), "")
        except Exception as e:
            triage_results["rejected_syntax_fail"].append({
                "file": fp.name,
                "reason": f"Corrupt JSON: {e}"
            })
            continue

        char_count = len(content)
        fb_name = validate_domain.extract_fb_name(content)

        # Stage 1: Domain
        dom = validate_domain.classify_dataset(fb_name, content)
        if dom["verdict"] == "REJECT":
            triage_results["rejected_off_target_domain"].append({
                "file": fp.name,
                "fb_name": fb_name,
                "forbidden_domain": dom["forbidden_domain"],
                "hits": dom["forbidden_hits"]
            })
            continue

        # Stage 2: Syntax
        iec = validate_iec.check_parity(content, min_chars=3500)
        if iec["verdict"] == "FAIL":
            triage_results["rejected_syntax_fail"].append({
                "file": fp.name,
                "fb_name": fb_name,
                "errors": iec["errors"]
            })
            continue

        # Stage 4 check early: Size Gate (Stub)
        if char_count < size_gate.STUB_THRESHOLD:
            triage_results["quarantined_stub_size"].append({
                "file": fp.name,
                "fb_name": fb_name,
                "char_count": char_count,
                "sector": dom["matched_sector"]
            })
            continue

        # Stage 3: Semantics
        sem = validate_semantic.validate_semantic_st(content, str(fp))
        if sem.verdict == "FAIL":
            triage_results["quarantined_semantic_warn"].append({
                "file": fp.name,
                "fb_name": fb_name,
                "errors": sem.errors,
                "sector": dom["matched_sector"]
            })
            continue

        # PASSED ALL GATES!
        sector = dom["matched_sector"] or "other_manufacturing"
        sector_counts[sector] = sector_counts.get(sector, 0) + 1

        entry = {
            "file": fp.name,
            "fb_name": fb_name,
            "sector": sector,
            "char_count": char_count,
            "semantic_verdict": sem.verdict,
            "has_tmr": sem.metrics.get("has_tmr", False),
            "mpc_n": sem.metrics.get("mpc_declared_n")
        }
        triage_results["verified_pass"].append(entry)

        # Non-destructive copy to verified structure
        if copy_verified:
            dest_dir = verified_base_dir / sector
            dest_dir.mkdir(parents=True, exist_ok=True)
            dest_fp = dest_dir / fp.name
            if not dest_fp.exists():
                shutil.copy2(str(fp), str(dest_fp))

        if (idx + 1) % 100 == 0 or (idx + 1) == len(files):
            print(f"  Processed {idx + 1}/{len(files)}: Verified={len(triage_results['verified_pass'])}...")

    summary = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "total_scanned": len(files),
        "verified_pass_count": len(triage_results["verified_pass"]),
        "quarantined_semantic_count": len(triage_results["quarantined_semantic_warn"]),
        "quarantined_stub_count": len(triage_results["quarantined_stub_size"]),
        "rejected_off_target_domain_count": len(triage_results["rejected_off_target_domain"]),
        "rejected_syntax_fail_count": len(triage_results["rejected_syntax_fail"]),
        "verified_pass_pct": round(len(triage_results["verified_pass"]) / max(1, len(files)) * 100, 2),
        "verified_sector_distribution": sector_counts
    }

    report_path.parent.mkdir(parents=True, exist_ok=True)
    with open(report_path, "w", encoding="utf-8") as rf:
        json.dump({"summary": summary, "results": triage_results}, rf, indent=2)

    print("\n=======================================================")
    print("  TRIAGE PIPELINE AUDIT SUMMARY")
    print("=======================================================")
    print(f"Total Scanned: {summary['total_scanned']}")
    print(f"VERIFIED (Clean Manufacturing Training Core): {summary['verified_pass_count']} ({summary['verified_pass_pct']}%)")
    print(f"QUARANTINED (Semantic Warnings / Repairable): {summary['quarantined_semantic_count']}")
    print(f"QUARANTINED (Micro/Stub Datasets < 100k chars): {summary['quarantined_stub_count']}")
    print(f"REJECTED (Off-Target Domains: Marine/Pharma/Defense): {summary['rejected_off_target_domain_count']}")
    print(f"REJECTED (Syntax Parity Failures): {summary['rejected_syntax_fail_count']}")
    print(f"\nVerified Sector Distribution:")
    for s, c in sector_counts.items():
        print(f"  {s.ljust(20)}: {c} datasets")
    print(f"\nMaster report saved to {report_path}")

    return summary

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Non-Destructive Triage Orchestrator")
    parser.add_argument("--input-dir", default="data/swarm_raw", help="Path to input datasets")
    parser.add_argument("--verified-dir", default="data/verified", help="Destination directory for verified copies")
    parser.add_argument("--report", default="reports/triage_master_report.json", help="Path for JSON audit report")
    parser.add_argument("--no-copy", action="store_true", help="Audit mode without copying files")
    parser.add_argument("--max-files", type=int, default=None, help="Limit number of files for quick testing")
    args = parser.parse_args()

    run_triage(
        Path(args.input_dir),
        Path(args.verified_dir),
        Path(args.report),
        copy_verified=not args.no_copy,
        max_files=args.max_files
    )
