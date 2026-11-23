#!/usr/bin/env python3
"""
scripts/check_sector_balance.py — Industrial Sector Quota & Balance Auditor
Reference: DOC-02, DOC-03

Audits sector distribution of the indexed corpus against target manufacturing proportions:
- Automotive & EV Powertrain: 25%
- Heavy Machinery & Tooling: 20%
- Electronics & PCBA: 15%
- Semiconductor Packaging: 15%
- Plastics & Polymer Processing: 10%
- Food & Beverage Packaging: 10%
- Metallurgy & Strip Steelmaking: 5%

Outputs deficit / surplus metrics and recommended generation counts for next swarm wave.
"""

import os
import sys
import json
import argparse
from pathlib import Path
from typing import Dict, List

TARGET_QUOTAS = {
    "automotive": 0.25,
    "heavy_machinery": 0.20,
    "electronics": 0.15,
    "semiconductor": 0.15,
    "plastics": 0.10,
    "foodbev": 0.10,
    "steelmaking": 0.05
}

def analyze_sector_balance(catalog_path: Path, next_wave_size: int = 100) -> Dict:
    if not catalog_path.exists():
        print(f"Error: Catalog {catalog_path} not found. Run scripts/build_corpus_index.py first.")
        sys.exit(1)

    records = []
    with open(catalog_path, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                records.append(json.loads(line))

    # Filter to approved domain passes
    approved = [r for r in records if r.get("validation", {}).get("domain_verdict") == "PASS"]
    total_approved = len(approved)

    sector_counts = {}
    for r in approved:
        sec = r.get("sector", "unclassified")
        sector_counts[sec] = sector_counts.get(sec, 0) + 1

    balance_report = []
    recommended_wave_targets = {}

    for sec, target_ratio in TARGET_QUOTAS.items():
        actual_cnt = sector_counts.get(sec, 0)
        actual_ratio = actual_cnt / max(1, total_approved)
        delta_ratio = actual_ratio - target_ratio
        
        # Calculate target count in a balanced ideal corpus of size total_approved
        ideal_count = int(round(total_approved * target_ratio))
        deficit = ideal_count - actual_cnt
        
        # Calculate next wave allocation (weighting heavily toward deficits)
        weight = max(0.01, target_ratio + max(0.0, -delta_ratio * 1.5))
        recommended_wave_targets[sec] = weight

        if deficit > 0:
            status = "DEFICIT"
        elif deficit < 0:
            status = "SURPLUS"
        else:
            status = "BALANCED"

        balance_report.append({
            "sector": sec,
            "actual_count": actual_cnt,
            "actual_percentage": round(actual_ratio * 100, 2),
            "target_percentage": round(target_ratio * 100, 2),
            "deficit_count": deficit,
            "status": status
        })

    # Normalize next wave targets to sum exactly to next_wave_size using largest remainder method
    weight_sum = sum(recommended_wave_targets.values())
    raw_allocations = {
        sec: max(1.0, (w / weight_sum) * next_wave_size)
        for sec, w in recommended_wave_targets.items()
    }
    wave_allocations = {sec: int(val) for sec, val in raw_allocations.items()}
    remainder = next_wave_size - sum(wave_allocations.values())
    
    fractions = sorted(
        raw_allocations.keys(),
        key=lambda s: raw_allocations[s] - wave_allocations[s],
        reverse=True
    )
    for i in range(remainder):
        wave_allocations[fractions[i % len(fractions)]] += 1

    return {
        "total_corpus_records": len(records),
        "approved_manufacturing_records": total_approved,
        "sector_audit": balance_report,
        "recommended_next_wave_allocations": wave_allocations
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Sector Balance Auditor")
    parser.add_argument("--catalog", default="catalog/corpus_index.jsonl", help="Path to index JSONL")
    parser.add_argument("--wave-size", type=int, default=50, help="Target count for next planned generation wave")
    parser.add_argument("--report", default="reports/sector_balance_audit.json", help="Path for JSON report")
    parser.add_argument("--warn-if-imbalanced", type=str, default=None, help="Warn if any sector imbalance exceeds percentage threshold (e.g. 10%)")
    args = parser.parse_args()

    res = analyze_sector_balance(Path(args.catalog), next_wave_size=args.wave_size)

    print("\n--- INDUSTRIAL SECTOR BALANCE AUDIT ---")
    print(f"Total Approved Manufacturing Datasets: {res['approved_manufacturing_records']}")
    print("\nSector Distribution vs Target:")
    for row in res["sector_audit"]:
        print(f"  {row['sector'].ljust(18)} : {row['actual_count']} ({row['actual_percentage']}%) | Target: {row['target_percentage']}% | Deficit: {row['deficit_count']} [{row['status']}]")

    print(f"\nRecommended Next Wave Allocation (Batch Size = {args.wave_size}):")
    for sec, cnt in res["recommended_next_wave_allocations"].items():
        print(f"  {sec.ljust(18)} : {cnt} datasets")

    if args.warn_if_imbalanced:
        threshold = float(args.warn_if_imbalanced.rstrip("%"))
        imbalanced = [
            row for row in res["sector_audit"]
            if abs(row["actual_percentage"] - row["target_percentage"]) > threshold
        ]
        if imbalanced:
            print(f"\n[WARNING] {len(imbalanced)} sector(s) exceed imbalance threshold of {threshold}%:")
            for row in imbalanced:
                delta = row["actual_percentage"] - row["target_percentage"]
                print(f"  - {row['sector']}: delta = {delta:+.2f}%")

    if args.report:
        rep_p = Path(args.report)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as rf:
            json.dump(res, rf, indent=2)
        print(f"\nSaved balance report to {rep_p}")
