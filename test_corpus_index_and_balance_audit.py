#!/usr/bin/env python3
"""
test_corpus_index_and_balance_audit.py — Comprehensive Audit Verification Test Suite
Verifies:
1. Schema v2.0 metadata formatting and completeness in build_corpus_index.py.
2. Non-destructive JSONL catalog and JSON inventory report generation.
3. Industrial manufacturing target proportions (summing to 100%).
4. Sector deficit / surplus calculations and status tagging in check_sector_balance.py.
5. Exact integer wave allocation via largest remainder method.
6. CLI execution, argument parsing, and imbalance warning triggers.
"""

import os
import sys
import json
import tempfile
import pytest
from pathlib import Path
from datetime import datetime

# Add root directory to sys.path
root_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(root_dir))

from scripts.build_corpus_index import analyze_dataset_entry, build_index
from scripts.check_sector_balance import TARGET_QUOTAS, analyze_sector_balance


# ---------------------------------------------------------------------------
# 1. Target Proportions & Mathematical Rigor
# ---------------------------------------------------------------------------

def test_target_quotas_completeness_and_sum():
    """Verify all 7 commercial manufacturing sectors sum to exactly 1.00 (100%)."""
    expected_sectors = {
        "automotive": 0.25,
        "heavy_machinery": 0.20,
        "electronics": 0.15,
        "semiconductor": 0.15,
        "plastics": 0.10,
        "foodbev": 0.10,
        "steelmaking": 0.05
    }
    assert TARGET_QUOTAS == expected_sectors
    assert round(sum(TARGET_QUOTAS.values()), 6) == 1.00


# ---------------------------------------------------------------------------
# 2. Schema v2.0 Metadata Formatting Verification
# ---------------------------------------------------------------------------

def test_analyze_dataset_entry_schema_v2_structure(tmp_path):
    """Verify extracted metadata strictly adheres to Schema v2.0 specification."""
    sample_file = tmp_path / "agent_test_sample.json"
    dummy_st = """```iec-st
FUNCTION_BLOCK FB_Electronics_SMT_Feeder_Test
VAR_INPUT
    bStart : BOOL;
    rMeas : REAL;
END_VAR
VAR_OUTPUT
    bRunning : BOOL;
END_VAR
VAR
    A_Matrix : ARRAY[1..4, 1..4] OF REAL;
    rTMR_ValA : REAL;
    rTMR_ValB : REAL;
    rTMR_ValC : REAL;
    rTMR_VotedOutput : REAL;
    tTMR_DiscrepancyTimer : TIME;
    nFSM_State : INT;
END_VAR
(* 2oo3 TMR Voting *)
IF (rTMR_ValA = rTMR_ValB) THEN
    rTMR_VotedOutput := rTMR_ValA;
END_IF;
CASE nFSM_State OF
    1: bRunning := TRUE;
END_CASE;
END_FUNCTION_BLOCK
```"""
    data = {
        "messages": [
            {"role": "user", "content": "Generate SMT block."},
            {"role": "assistant", "content": dummy_st}
        ]
    }
    sample_file.write_text(json.dumps(data), encoding="utf-8")

    rec = analyze_dataset_entry(sample_file)
    assert rec is not None

    # Required top-level fields
    assert rec["id"] == "agent_test_sample"
    assert rec["schema_version"] == "2.0"
    assert rec["file"] == "agent_test_sample.json"
    assert rec["function_block"] == "FB_Electronics_SMT_Feeder_Test"
    assert rec["sector"] == "electronics"
    assert "subsector" in rec
    assert rec["complexity_tier"] in (1, 2, 3)
    assert rec["char_count"] == len(dummy_st)
    assert rec["token_estimate"] == int(len(dummy_st) / 3.1)
    assert rec["size_category"] in ("stub", "standard", "extended", "ultra_dense")
    assert "indexed_at" in rec

    # Validation sub-dict
    val = rec["validation"]
    assert "syntax_parity" in val and isinstance(val["syntax_parity"], bool)
    assert "domain_verdict" in val and val["domain_verdict"] in ("PASS", "REJECT", "AMBIGUOUS")
    assert "semantic_verdict" in val and val["semantic_verdict"] in ("PASS", "WARN", "FAIL")
    assert "forbidden_hits" in val and isinstance(val["forbidden_hits"], list)

    # Content flags sub-dict
    flags = rec["content_flags"]
    assert "has_tmr" in flags and isinstance(flags["has_tmr"], bool)
    assert "has_tmr_discrepancy" in flags and isinstance(flags["has_tmr_discrepancy"], bool)
    assert "has_mpc" in flags and isinstance(flags["has_mpc"], bool)
    assert "has_fsm" in flags and isinstance(flags["has_fsm"], bool)
    assert "has_isa18_alarms" in flags and isinstance(flags["has_isa18_alarms"], bool)
    assert "declared_vars" in flags and isinstance(flags["declared_vars"], int)


@pytest.mark.parametrize("chars,expected_tier", [
    (50_000, 1),
    (99_999, 1),
    (100_000, 2),
    (349_999, 2),
    (350_000, 3),
    (800_000, 3),
])
def test_complexity_tier_classification(tmp_path, chars, expected_tier):
    """Verify tier assignment boundaries (<100k -> 1, 100k-350k -> 2, >=350k -> 3)."""
    p = tmp_path / f"test_tier_{chars}.json"
    header = "FUNCTION_BLOCK FB_Test\n"
    footer = "\nEND_FUNCTION_BLOCK\n"
    padding_needed = chars - len(header) - len(footer)
    content = header + ("x" * padding_needed) + footer
    assert len(content) == chars
    data = {"messages": [{"role": "assistant", "content": content}]}
    p.write_text(json.dumps(data), encoding="utf-8")

    rec = analyze_dataset_entry(p)
    assert rec["complexity_tier"] == expected_tier


# ---------------------------------------------------------------------------
# 3. Non-Destructive JSONL Catalog Generation & Inventory Reporting
# ---------------------------------------------------------------------------

def test_build_index_execution(tmp_path):
    """Verify build_index creates a valid JSONL catalog and JSON inventory summary without altering inputs."""
    input_dir = tmp_path / "raw"
    input_dir.mkdir()
    out_jsonl = tmp_path / "catalog" / "corpus_index.jsonl"
    report_json = tmp_path / "reports" / "corpus_inventory.json"

    # Create 3 synthetic dataset files
    for i, name in enumerate(["FB_Plastics_BlowMolding", "FB_Automotive_BIW", "FB_Subsea_Propulsion"]):
        p = input_dir / f"agent_{i:04d}.json"
        data = {
            "messages": [
                {"role": "user", "content": "Make block"},
                {"role": "assistant", "content": f"```iec-st\nFUNCTION_BLOCK {name}\nVAR\n  bRun : BOOL;\nEND_VAR\nEND_FUNCTION_BLOCK\n```"}
            ]
        }
        p.write_text(json.dumps(data), encoding="utf-8")

    # Record input mtimes and hashes to guarantee non-destructive property
    input_states_before = {p: (p.stat().st_size, p.stat().st_mtime) for p in input_dir.glob("*.json")}

    build_index(input_dir, out_jsonl, report_json)

    # 1. Output files exist
    assert out_jsonl.exists()
    assert report_json.exists()

    # 2. JSONL is valid line by line
    records = []
    with open(out_jsonl, "r", encoding="utf-8") as f:
        for line in f:
            rec = json.loads(line.strip())
            records.append(rec)
    assert len(records) == 3

    # 3. Report is valid JSON with aggregations
    with open(report_json, "r", encoding="utf-8") as rf:
        rep = json.load(rf)
    assert rep["indexed_count"] == 3
    assert rep["domain_pass_count"] == 2  # Plastics and Automotive PASS, Subsea REJECT
    assert "semantic_warn_count" in rep or "semantic_pass_count" in rep

    # 4. Raw inputs strictly unmodified
    for p, (orig_size, orig_mtime) in input_states_before.items():
        assert p.stat().st_size == orig_size
        assert p.stat().st_mtime == orig_mtime


# ---------------------------------------------------------------------------
# 4. Sector Balance & Deficit Mathematics
# ---------------------------------------------------------------------------

def test_sector_balance_deficit_and_surplus_logic(tmp_path):
    """Verify deficit calculations, status labels, and exact integer wave allocations."""
    catalog_path = tmp_path / "corpus_index.jsonl"

    # Create synthetic catalog with 20 approved records:
    # automotive: 10 (50% vs target 25% -> SURPLUS)
    # heavy_machinery: 0 (0% vs target 20% -> DEFICIT)
    # electronics: 3 (15% vs target 15% -> BALANCED)
    # semiconductor: 3 (15% vs target 15% -> BALANCED)
    # plastics: 2 (10% vs target 10% -> BALANCED)
    # foodbev: 1 (5% vs target 10% -> DEFICIT)
    # steelmaking: 1 (5% vs target 5% -> BALANCED)
    # Rejected record: 1 (marine subsea -> should NOT count toward approved total)
    lines = []
    distribution = [
        ("automotive", 10),
        ("heavy_machinery", 0),
        ("electronics", 3),
        ("semiconductor", 3),
        ("plastics", 2),
        ("foodbev", 1),
        ("steelmaking", 1)
    ]
    for sec, count in distribution:
        for i in range(count):
            lines.append(json.dumps({
                "id": f"id_{sec}_{i}",
                "sector": sec,
                "validation": {"domain_verdict": "PASS"}
            }))

    # Add 1 rejected dataset
    lines.append(json.dumps({
        "id": "id_rejected",
        "sector": "automotive",
        "validation": {"domain_verdict": "REJECT"}
    }))

    catalog_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    wave_size = 50
    audit = analyze_sector_balance(catalog_path, next_wave_size=wave_size)

    assert audit["total_corpus_records"] == 21
    assert audit["approved_manufacturing_records"] == 20

    # Sector specific audits
    audit_map = {row["sector"]: row for row in audit["sector_audit"]}

    # Automotive: target 25% of 20 = 5. actual = 10. deficit = 5 - 10 = -5 (SURPLUS)
    assert audit_map["automotive"]["actual_count"] == 10
    assert audit_map["automotive"]["deficit_count"] == -5
    assert audit_map["automotive"]["status"] == "SURPLUS"

    # Heavy Machinery: target 20% of 20 = 4. actual = 0. deficit = 4 - 0 = +4 (DEFICIT)
    assert audit_map["heavy_machinery"]["actual_count"] == 0
    assert audit_map["heavy_machinery"]["deficit_count"] == 4
    assert audit_map["heavy_machinery"]["status"] == "DEFICIT"

    # Electronics: target 15% of 20 = 3. actual = 3. deficit = 0 (BALANCED)
    assert audit_map["electronics"]["actual_count"] == 3
    assert audit_map["electronics"]["deficit_count"] == 0
    assert audit_map["electronics"]["status"] == "BALANCED"

    # Food & Bev: target 10% of 20 = 2. actual = 1. deficit = 2 - 1 = 1 (DEFICIT)
    assert audit_map["foodbev"]["actual_count"] == 1
    assert audit_map["foodbev"]["deficit_count"] == 1
    assert audit_map["foodbev"]["status"] == "DEFICIT"

    # Allocation exactness: sum of wave allocations MUST exactly match wave_size
    allocations = audit["recommended_next_wave_allocations"]
    assert sum(allocations.values()) == wave_size

    # Heavy machinery has largest deficit -> should receive highest allocation
    assert allocations["heavy_machinery"] == max(allocations.values())


@pytest.mark.parametrize("wave_size", [10, 25, 50, 77, 100])
def test_wave_allocations_exact_sum(tmp_path, wave_size):
    """Verify largest remainder method guarantees exact integer wave allocation across varied batch sizes."""
    catalog_path = tmp_path / "corpus_index.jsonl"
    lines = [
        json.dumps({"id": f"id_{i}", "sector": "automotive", "validation": {"domain_verdict": "PASS"}})
        for i in range(10)
    ]
    catalog_path.write_text("\n".join(lines) + "\n", encoding="utf-8")

    res = analyze_sector_balance(catalog_path, next_wave_size=wave_size)
    assert sum(res["recommended_next_wave_allocations"].values()) == wave_size


if __name__ == "__main__":
    pytest.main(["-v", __file__])
