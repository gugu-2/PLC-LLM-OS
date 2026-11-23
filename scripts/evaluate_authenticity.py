#!/usr/bin/env python3
"""
scripts/evaluate_authenticity.py — PLC Code Authenticity & Effectiveness Evaluator
Reference: MODEL_EVALUATION_AND_BENCHMARKS.md, PLC_DOMAIN_INTELLIGENCE.md

This script calculates the authentic production-readiness percentage of PLC code datasets.
Evaluates across 5 industrial dimensions:
1. IEC-PR (IEC 61131-3 Syntax & Parity Pass Rate)
2. DCA (Deterministic Control & State Machine Accuracy)
3. HR (Foreign Hallucination Rate — Lower is Better)
4. VDCS (Vendor Dialect Conformance: Siemens SCL, Rockwell L5X, Beckhoff TwinCAT)
5. ESCS (Engineering Safety Certification Score via Z3 SMT Formal Proof)

Emits a composite "Authenticity Score (%)" and detailed defect report.
"""

import sys
import os
import re
import json
import argparse
from pathlib import Path
from typing import Dict, List, Any, Optional

# Ensure project root is on PYTHONPATH
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from plc_platform.agents.static_auditor import StaticAnalysisAuditor
from plc_platform.agents.smt_verifier import SMTVerificationTester
from plc_platform.dialects.siemens_scl import SiemensSCLEngine
from plc_platform.dialects.rockwell_l5x import RockwellL5XEngine
from plc_platform.dialects.twincat_pou import TwinCATPOUEngine


class AuthenticityEvaluator:
    """Calculates production authenticity and effectiveness percentage of PLC datasets."""

    def __init__(self):
        self.auditor = StaticAnalysisAuditor()
        self.verifier = SMTVerificationTester()
        
        # Foreign tokens indicating model hallucination from general web data
        self.foreign_tokens = [
            r"\bSystem\.out\b", r"\bconsole\.log\b", r"\bprintf\b", r"\bmalloc\b",
            r"\bfree\b", r"\bimport\s+java\b", r"\b#include\b", r"\bdef\s+\w+\(.*\):",
            r"\bclass\s+\w+:", r"\breturn\s+new\b", r"\bstd::\b", r"\bnullptr\b"
        ]

    def evaluate_code(
        self,
        code_text: str,
        vendor: str = "GENERIC_IEC",
        system_name: str = "Industrial Process"
    ) -> Dict[str, Any]:
        """
        Evaluates a single PLC program and calculates the 5 core industrial metrics.
        """
        # -------------------------------------------------------------
        # Metric 1: IEC-PR (IEC 61131-3 Syntax Parity Pass Rate)
        # -------------------------------------------------------------
        audit_rep = self.auditor.audit_code_text(code_text, min_chars=50)
        parity_defects = [d for d in audit_rep.defects if d.stage == "PARITY"]
        var_defects = [d for d in audit_rep.defects if d.error_type == "UNDECLARED_VARIABLE"]
        
        # If parity passes and variable declarations are valid
        iec_pr = 1.0
        if not audit_rep.iec_parity_passed or parity_defects:
            iec_pr -= 0.35 * len(parity_defects)
        if var_defects:
            iec_pr -= 0.15 * min(3, len(var_defects))
        iec_pr = round(max(0.0, min(1.0, iec_pr)), 4)

        # -------------------------------------------------------------
        # Metric 2: DCA (Deterministic Control Accuracy)
        # -------------------------------------------------------------
        # Checks: State machine presence, discrete state matrix propagation, non-blocking timers
        has_fsm = bool(re.search(r"\bCASE\b[^;]+\bOF\b", code_text) and "END_CASE" in code_text)
        has_state_propagation = bool(re.search(r"r_State_X\[\d+\]\s*:=", code_text) or re.search(r"\bState_X\b", code_text))
        has_blocking_while = bool(re.search(r"\bWHILE\b[^;]*\bDO\b", code_text) and "ton" not in code_text.lower())
        has_packml = bool(re.search(r"EXECUTE|HOLDING|STOPPED|STARTING|ABORTING", code_text, re.IGNORECASE))

        dca_score = 0.20  # Base
        if has_fsm:
            dca_score += 0.35
        if has_state_propagation:
            dca_score += 0.25
        if has_packml:
            dca_score += 0.10
        if not has_blocking_while:
            dca_score += 0.10
        dca = round(max(0.0, min(1.0, dca_score)), 4)

        # -------------------------------------------------------------
        # Metric 3: HR (Foreign Hallucination Rate - Lower is Better)
        # -------------------------------------------------------------
        lines = code_text.splitlines()
        hallucination_lines = 0
        for line in lines:
            if any(re.search(tok, line) for tok in self.foreign_tokens):
                hallucination_lines += 1
        hr = round(hallucination_lines / max(1, len(lines)), 4)

        # -------------------------------------------------------------
        # Metric 4: VDCS (Vendor Dialect Conformance Score)
        # -------------------------------------------------------------
        v_upper = vendor.upper()
        vdcs = 0.50
        if "SIEMENS" in v_upper:
            has_opt = "S7_Optimized_Access" in code_text
            has_scoped_hash = "#" in code_text
            has_region = "REGION" in code_text
            vdcs += (0.20 if has_opt else 0.0) + (0.15 if has_scoped_hash else 0.0) + (0.15 if has_region else 0.0)
        elif "ROCKWELL" in v_upper:
            has_aoi = "AddOnInstruction" in code_text or "AOI_" in code_text or "EnableIn" in code_text
            has_l5x = "RSLogix5000Content" in code_text or "RLLContent" in code_text or "XIC(" in code_text
            vdcs += (0.25 if has_aoi else 0.0) + (0.25 if has_l5x else 0.0)
        elif "BECKHOFF" in v_upper:
            has_attr = "{attribute" in code_text
            has_tc = "TcPlcObject" in code_text or "TcPOU" in code_text or "fb_Axis" in code_text or "MC_" in code_text
            vdcs += (0.25 if has_attr else 0.0) + (0.25 if has_tc else 0.0)
        else:
            # Generic IEC 61131-3
            has_fb = "FUNCTION_BLOCK" in code_text and "END_FUNCTION_BLOCK" in code_text
            has_vars = "VAR_INPUT" in code_text and "VAR_OUTPUT" in code_text
            vdcs = 0.60 + (0.20 if has_fb else 0.0) + (0.20 if has_vars else 0.0)
        vdcs = round(max(0.0, min(1.0, vdcs)), 4)

        # -------------------------------------------------------------
        # Metric 5: ESCS (Engineering Safety Certification Score)
        # -------------------------------------------------------------
        has_estop = bool(re.search(r"NOT\s+b_EStop_OK", code_text, re.IGNORECASE))
        has_tmr = bool(re.search(r"2oo3|Voted|Median|ChA_Raw|ChB_Raw", code_text, re.IGNORECASE))
        has_discrepancy_timer = bool(re.search(r"ton_Discrepancy|T#\d+ms", code_text, re.IGNORECASE))
        
        # Formal SMT verification
        smt_report = self.verifier.verify_code_text(code_text)
        smt_ok = smt_report.smt_proved_safe

        escs_score = 0.0
        if has_estop:
            escs_score += 0.35
        if has_tmr or has_discrepancy_timer:
            escs_score += 0.25
        if smt_ok:
            escs_score += 0.40
        else:
            escs_score += 0.10
        escs = round(max(0.0, min(1.0, escs_score)), 4)

        # -------------------------------------------------------------
        # Final Composite Authenticity Percentage (%)
        # Weights:
        # 25% IEC Syntax Parity + 25% Control Accuracy + 15% (1 - HR) + 15% Vendor Dialect + 20% Safety
        # -------------------------------------------------------------
        composite = (0.25 * iec_pr) + (0.25 * dca) + (0.15 * max(0.0, 1.0 - hr)) + (0.15 * vdcs) + (0.20 * escs)
        authenticity_percentage = round(composite * 100.0, 2)

        return {
            "system_name": system_name,
            "vendor": vendor,
            "char_count": len(code_text),
            "line_count": len(lines),
            "metrics": {
                "iec_pr": iec_pr,
                "dca": dca,
                "hr": hr,
                "vdcs": vdcs,
                "escs": escs,
            },
            "authenticity_percentage": authenticity_percentage,
            "audit_passed": audit_rep.passed,
            "smt_proved_safe": smt_ok,
            "defects_found": [d.message for d in audit_rep.defects]
        }

    def evaluate_dataset_file(self, json_path: Path) -> Dict[str, Any]:
        """Loads a dataset JSON or JSONL file and evaluates its authenticity."""
        with open(json_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        code_text = ""
        # Check standard Lumina / Schema v2.0 / OpenAI messages fields
        if "messages" in data:
            for turn in reversed(data["messages"]):
                if turn.get("role") == "assistant":
                    content = turn.get("content", "")
                    m = re.search(r"```(?:iec-st|st|scl)?\s*(FUNCTION_BLOCK.*?END_FUNCTION_BLOCK)\s*```", content, re.DOTALL)
                    if m:
                        code_text = m.group(1)
                    else:
                        code_text = content
                    break
        elif "conversations" in data:
            for turn in reversed(data["conversations"]):
                if turn.get("role") == "assistant":
                    content = turn.get("content", "")
                    m = re.search(r"```(?:iec-st|st|scl)?\s*(FUNCTION_BLOCK.*?END_FUNCTION_BLOCK)\s*```", content, re.DOTALL)
                    if m:
                        code_text = m.group(1)
                    else:
                        code_text = content
                    break
        elif "st_code" in data:
            code_text = data["st_code"]
        elif "output_target" in data:
            code_text = data["output_target"]

        vendor = data.get("vendor", data.get("controller_target", "GENERIC_IEC"))
        system_name = data.get("system_name", data.get("subsystem", json_path.stem))

        return self.evaluate_code(code_text, vendor=vendor, system_name=system_name)


def main():
    parser = argparse.ArgumentParser(description="Evaluate PLC Code Authenticity & Effectiveness Percentage")
    parser.add_argument("--file", type=str, help="Path to a single JSON dataset file")
    parser.add_argument("--dir", type=str, help="Path to a directory containing JSON datasets")
    parser.add_argument("--sample-limit", type=int, default=10, help="Max files to evaluate in directory")
    args = parser.parse_args()

    evaluator = AuthenticityEvaluator()

    if args.file:
        p = Path(args.file)
        if not p.exists():
            print(f"Error: File not found: {p}")
            sys.exit(1)
        res = evaluator.evaluate_dataset_file(p)
        print(json.dumps(res, indent=2))
        return

    target_dir = Path(args.dir) if args.dir else Path("data/swarm_raw")
    if not target_dir.exists():
        print(f"Directory {target_dir} does not exist. Running self-test on built-in code...")
        sample_code = """
FUNCTION_BLOCK FB_Battery_DispenseModule
VAR_INPUT
    b_SystemEnable : BOOL; // System permissive [ms]
    b_EStop_OK : BOOL; // Dual safety circuit [ms]
    r_Sensor_ChA_Raw : REAL; // Sensor A [bar]
    r_Sensor_ChB_Raw : REAL; // Sensor B [bar]
    r_ClampForce : REAL; // Actuator clamp [kN]
END_VAR
VAR_OUTPUT
    b_Running : BOOL;
    b_FaultActive : BOOL;
END_VAR
VAR
    i_State : DINT;
    r_State_X : ARRAY[0..3] OF REAL;
END_VAR
IF NOT b_EStop_OK OR NOT b_SystemEnable THEN
    b_Running := FALSE;
    b_FaultActive := TRUE;
    RETURN;
END_IF;
CASE i_State OF
0: // IDLE
    IF b_SystemEnable THEN i_State := 10; END_IF;
10: // EXECUTE
    b_Running := TRUE;
    r_State_X[0] := 0.95 * r_State_X[0] + 0.05 * r_Sensor_ChA_Raw;
END_CASE;
END_FUNCTION_BLOCK
"""
        res = evaluator.evaluate_code(sample_code, vendor="SIEMENS", system_name="Battery Dispense Self-Test")
        print("\n============================================================")
        print("          PLC CODE AUTHENTICITY EVALUATION REPORT           ")
        print("============================================================")
        print(f"System:                  {res['system_name']}")
        print(f"Target Vendor:           {res['vendor']}")
        print(f"Total Character Count:   {res['char_count']} chars")
        print("------------------------------------------------------------")
        print(f"IEC-PR (Syntax Parity):  {res['metrics']['iec_pr']*100:.1f}%")
        print(f"DCA (Control Accuracy):  {res['metrics']['dca']*100:.1f}%")
        print(f"HR (Hallucination Rate): {res['metrics']['hr']*100:.2f}%")
        print(f"VDCS (Vendor Dialect):   {res['metrics']['vdcs']*100:.1f}%")
        print(f"ESCS (Safety Proof):     {res['metrics']['escs']*100:.1f}%")
        print("============================================================")
        print(f"OVERALL AUTHENTICITY SCORE: {res['authenticity_percentage']}%")
        print(f"SMT Safety Proved:       {res['smt_proved_safe']}")
        print("============================================================\n")
        return

    json_files = list(target_dir.glob("*.json"))[:args.sample_limit]
    if not json_files:
        print(f"No JSON files found in {target_dir}")
        return

    print(f"\nEvaluating {len(json_files)} datasets from {target_dir}...")
    scores = []
    for f in json_files:
        try:
            r = evaluator.evaluate_dataset_file(f)
            scores.append(r["authenticity_percentage"])
            print(f"[{r['authenticity_percentage']:5.1f}%] {r['system_name']} ({r['vendor']}) - {r['char_count']} chars")
        except Exception as e:
            print(f"[ERROR] {f.name}: {e}")

    if scores:
        mean_auth = sum(scores) / len(scores)
        print("\n============================================================")
        print(f"EVALUATED {len(scores)} DATASETS")
        print(f"AVERAGE AUTHENTICITY PERCENTAGE: {mean_auth:.2f}%")
        print(f"MIN AUTHENTICITY:                {min(scores):.2f}%")
        print(f"MAX AUTHENTICITY:                {max(scores):.2f}%")
        print("============================================================\n")


if __name__ == "__main__":
    main()
