#!/usr/bin/env python3
"""
tests/audit_supplementary_pipelines.py — Automated Auditor for Supplementary Dataset Pipelines
Audits:
- scripts/generate_type1_dialogue.py
- scripts/generate_type2_debug.py
- scripts/generate_type3_incremental.py
- scripts/generate_type4_concept_code.py

Verification Criteria:
1. Script execution and output generation
2. Valid JSON structure and RFC 8259 syntax
3. Schema v2.0 conformity (id, schema_version=2.0, dataset_type, metadata, messages)
4. IEC 61131-3 syntax and parity validation (validate_iec)
"""

import os
import sys
import json
import subprocess
from pathlib import Path

# Add project root to path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import validate_iec

PIPELINE_SPECS = {
    "type1_dialogue": {
        "name": "Type 1: Technical Dialogue Q&A",
        "script": "scripts/generate_type1_dialogue.py",
        "out_dir": "data/supplementary/type_1_dialogue",
        "expected_type": "type_1_dialogue_qa",
        "required_metadata": ["topic", "sector", "system"],
    },
    "type2_debug": {
        "name": "Type 2: 3-Turn Fault Diagnosis & Debug Chain",
        "script": "scripts/generate_type2_debug.py",
        "out_dir": "data/supplementary/type_2_debug",
        "expected_type": "type_2_debug_chain",
        "required_metadata": ["fault_type", "sector", "system"],
    },
    "type3_incremental": {
        "name": "Type 3: Incremental Modification",
        "script": "scripts/generate_type3_incremental.py",
        "out_dir": "data/supplementary/type_3_incremental",
        "expected_type": "type_3_incremental_modification",
        "required_metadata": ["task_name", "sector", "system"],
    },
    "type4_concept_code": {
        "name": "Type 4: Concept-to-Code Translation",
        "script": "scripts/generate_type4_concept_code.py",
        "out_dir": "data/supplementary/type_4_concept_code",
        "expected_type": "type_4_concept_to_code",
        "required_metadata": ["concept", "sector", "system"],
    },
}

def run_pipeline_audit():
    audit_report = {
        "pipeline_results": {},
        "total_datasets_tested": 0,
        "total_passed": 0,
        "total_failed": 0,
        "all_passed": True,
    }

    print("========================================================================")
    print("      LUMINA SUPPLEMENTARY DATASET PIPELINE VERIFICATION AUDIT          ")
    print("========================================================================\n")

    for key, spec in PIPELINE_SPECS.items():
        print(f"[*] Auditing {spec['name']} ({spec['script']})...")
        pipeline_res = {
            "name": spec["name"],
            "script": spec["script"],
            "execution_ok": False,
            "json_valid": True,
            "schema_v2_valid": True,
            "iec_valid": True,
            "generated_files": [],
            "errors": [],
        }

        out_path = root_dir / spec["out_dir"]
        out_path.mkdir(parents=True, exist_ok=True)

        # 1. Run the script with --count 2
        cmd = [sys.executable, str(root_dir / spec["script"]), "--count", "2", "--out-dir", str(out_path)]
        proc = subprocess.run(cmd, capture_output=True, text=True)
        if proc.returncode != 0:
            pipeline_res["execution_ok"] = False
            pipeline_res["errors"].append(f"Script execution failed with exit code {proc.returncode}: {proc.stderr}")
            audit_report["all_passed"] = False
            audit_report["pipeline_results"][key] = pipeline_res
            print(f"    [FAIL] Execution failed: {proc.stderr.strip()[:100]}")
            continue
        else:
            pipeline_res["execution_ok"] = True
            print(f"    [PASS] Execution succeeded (exit code 0)")

        # 2. Check generated JSON files
        files = list(out_path.glob("*.json"))
        if not files:
            pipeline_res["errors"].append(f"No JSON files found in {out_path}")
            pipeline_res["schema_v2_valid"] = False
            audit_report["all_passed"] = False
            audit_report["pipeline_results"][key] = pipeline_res
            print(f"    [FAIL] No output files generated.")
            continue

        for f in files:
            audit_report["total_datasets_tested"] += 1
            file_record = {"file": f.name, "char_count": f.stat().st_size, "errors": []}

            # A. JSON Validity
            try:
                with open(f, "r", encoding="utf-8") as jf:
                    data = json.load(jf)
            except Exception as e:
                file_record["errors"].append(f"Corrupt JSON: {e}")
                pipeline_res["json_valid"] = False
                audit_report["all_passed"] = False
                continue

            # B. Schema v2.0 Compliance
            if not data.get("id"):
                file_record["errors"].append("Missing required field 'id'")
                pipeline_res["schema_v2_valid"] = False

            if data.get("schema_version") != "2.0":
                file_record["errors"].append(f"schema_version mismatch: expected '2.0', got '{data.get('schema_version')}'")
                pipeline_res["schema_v2_valid"] = False

            if data.get("dataset_type") != spec["expected_type"]:
                file_record["errors"].append(f"dataset_type mismatch: expected '{spec['expected_type']}', got '{data.get('dataset_type')}'")
                pipeline_res["schema_v2_valid"] = False

            for meta_field in spec["required_metadata"]:
                if not data.get(meta_field):
                    file_record["errors"].append(f"Missing required metadata field: '{meta_field}'")
                    pipeline_res["schema_v2_valid"] = False

            msgs = data.get("messages", [])
            if not isinstance(msgs, list) or len(msgs) < 2:
                file_record["errors"].append(f"Invalid messages list: expected at least 2 messages, got {len(msgs) if isinstance(msgs, list) else 'non-list'}")
                pipeline_res["schema_v2_valid"] = False
            else:
                for idx, m in enumerate(msgs):
                    if not isinstance(m, dict) or "role" not in m or "content" not in m:
                        file_record["errors"].append(f"Message index {idx} missing 'role' or 'content'")
                        pipeline_res["schema_v2_valid"] = False
                    elif m["role"] not in ["user", "assistant"]:
                        file_record["errors"].append(f"Message index {idx} has unrecognized role '{m['role']}'")
                        pipeline_res["schema_v2_valid"] = False
                    elif not m["content"].strip():
                        file_record["errors"].append(f"Message index {idx} has empty content")
                        pipeline_res["schema_v2_valid"] = False

            # C. IEC Validation
            iec_errs = validate_iec.validate_json_file(f)
            if iec_errs:
                file_record["errors"].extend(iec_errs)
                pipeline_res["iec_valid"] = False
                audit_report["all_passed"] = False

            if file_record["errors"]:
                audit_report["total_failed"] += 1
                pipeline_res["errors"].extend([f"[{f.name}] {e}" for e in file_record["errors"]])
                print(f"    - {f.name}: [FAIL] {'; '.join(file_record['errors'])}")
            else:
                audit_report["total_passed"] += 1
                print(f"    - {f.name}: [PASS] Schema v2.0 & IEC Valid")

            pipeline_res["generated_files"].append(file_record)

        audit_report["pipeline_results"][key] = pipeline_res
        print()

    print("========================================================================")
    print(f"AUDIT SUMMARY: Tested {audit_report['total_datasets_tested']} datasets across 4 pipelines.")
    print(f"PASSED: {audit_report['total_passed']} | FAILED: {audit_report['total_failed']}")
    print(f"OVERALL CERTIFICATION STATUS: {'VERIFIED & APPROVED' if audit_report['all_passed'] else 'REJECTED'}")
    print("========================================================================")
    return audit_report

if __name__ == "__main__":
    report = run_pipeline_audit()
    sys.exit(0 if report["all_passed"] else 1)
