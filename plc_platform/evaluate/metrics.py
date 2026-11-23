#!/usr/bin/env python3
"""
plc_platform/evaluate/metrics.py — 5 Core Evaluation Metrics for Industrial PLC Intelligence
Reference: MODEL_EVALUATION_AND_BENCHMARKS.md, PLC_DOMAIN_INTELLIGENCE.md

Calculates:
1. IEC-PR: IEC 61131-3 Syntax Pass Rate (Target >= 98.0%)
2. DCA: Deterministic Control Accuracy (Target >= 95.0%)
3. HR: Hallucination Rate (Target < 2.0%)
4. VDCS: Vendor Dialect Conformance Score (Target >= 95.0%)
5. ESCS: Engineering Safety Certification Score (Target >= 92.0%)
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional, Any
import re
from ..agents.static_auditor import StaticAnalysisAuditor
from ..agents.smt_verifier import SMTVerifier


@dataclass
class BenchmarkEvaluationResult:
    bench_id: str
    config_name: str
    iec_pr: float        # 0.0 to 1.0
    dca: float           # 0.0 to 1.0
    hr: float            # 0.0 to 1.0 (Lower is better)
    vdcs: float          # 0.0 to 1.0
    escs: float          # 0.0 to 1.0
    composite_score: float
    audit_defects: List[str] = field(default_factory=list)
    smt_verified: bool = False


class MetricsCalculator:
    """Evaluates PLC code packages across the 5 core industrial benchmark metrics."""

    def __init__(self):
        self.auditor = StaticAnalysisAuditor()
        self.verifier = SMTVerifier()

        # Foreign hallucination indicators
        self.foreign_tokens = [
            r"\bSystem\.out\b", r"\bconsole\.log\b", r"\bprintf\b", r"\bmalloc\b",
            r"\bfree\b", r"\bimport\s+java\b", r"\b#include\b", r"\bdef\s+\w+\(.*\):",
            r"\bclass\s+\w+:", r"\breturn\s+new\b", r"\bstd::\b"
        ]

    def evaluate_candidate(
        self,
        bench_id: str,
        config_name: str,
        code_text: str,
        target_vendor: str,
        expected_states: List[str],
        safety_invariants: List[str]
    ) -> BenchmarkEvaluationResult:
        """Computes all 5 metrics for a generated PLC code block."""

        # 1. IEC-PR: Syntax Pass Rate via StaticAnalysisAuditor
        report = self.auditor.audit_code(code_text)
        iec_pr = 1.0 if report.iec_parity_passed else max(0.0, 1.0 - (len([d for d in report.defects if d.stage == "PARITY"]) * 0.25))

        # 2. DCA: Deterministic Control Accuracy
        # Check FSM states, matrix propagation, and absence of blocking loops
        fsm_hits = sum(1 for state in expected_states if state in code_text)
        fsm_ratio = fsm_hits / max(1, len(expected_states))
        
        has_state_propagation = bool(re.search(r"r_State_X\[\d+\]\s*:=", code_text) or re.search(r"\bState_X\b", code_text))
        has_blocking_while = bool(re.search(r"\bWHILE\b[^;]*\bDO\b", code_text) and "ton" not in code_text.lower())
        
        dca_score = (fsm_ratio * 0.5) + (0.3 if has_state_propagation else 0.15) + (0.2 if not has_blocking_while else 0.0)
        dca = round(min(1.0, max(0.0, dca_score)), 3)

        # 3. HR: Hallucination Rate
        hallucination_count = 0
        lines = code_text.splitlines()
        for line in lines:
            if any(re.search(tok, line) for tok in self.foreign_tokens):
                hallucination_count += 1
        hr = round(hallucination_count / max(1, len(lines)), 4)

        # 4. VDCS: Vendor Dialect Conformance Score
        vdcs = 0.5
        v_upper = target_vendor.upper()
        if "SIEMENS" in v_upper:
            has_opt = "S7_Optimized_Access" in code_text
            has_scoped_hash = "#" in code_text
            has_region = "REGION" in code_text
            vdcs = 0.5 + (0.2 if has_opt else 0.0) + (0.15 if has_scoped_hash else 0.0) + (0.15 if has_region else 0.0)
        elif "ROCKWELL" in v_upper:
            has_aoi = "AddOnInstruction" in code_text or "AOI_" in code_text or "EnableIn" in code_text
            has_l5x = "RSLogix5000Content" in code_text or "RLLContent" in code_text or "XIC(" in code_text
            vdcs = 0.5 + (0.25 if has_aoi else 0.0) + (0.25 if has_l5x else 0.0)
        elif "BECKHOFF" in v_upper:
            has_attr = "{attribute" in code_text
            has_tc = "TcPlcObject" in code_text or "TcPOU" in code_text or "fb_Axis" in code_text or "MC_" in code_text
            vdcs = 0.5 + (0.25 if has_attr else 0.0) + (0.25 if has_tc else 0.0)
        else:
            # Generic IEC
            has_fb = "FUNCTION_BLOCK" in code_text and "END_FUNCTION_BLOCK" in code_text
            has_var = "VAR_INPUT" in code_text and "VAR_OUTPUT" in code_text
            vdcs = 0.6 + (0.2 if has_fb else 0.0) + (0.2 if has_var else 0.0)
        vdcs = round(min(1.0, max(0.0, vdcs)), 3)

        # 5. ESCS: Engineering Safety Certification Score
        # Check E-Stop cutoff, 2oo3 voting, and run SMT verifier
        has_estop = bool(re.search(r"NOT\s+b_EStop_OK", code_text, re.IGNORECASE))
        has_tmr = bool(re.search(r"2oo3|Voted|Median|ChA_Raw", code_text, re.IGNORECASE))
        
        smt_report = self.verifier.verify_code_text(code_text)
        smt_ok = smt_report.smt_proved_safe

        escs_score = (0.35 if has_estop else 0.0) + (0.25 if has_tmr else 0.0) + (0.40 if smt_ok else 0.15)
        escs = round(min(1.0, max(0.0, escs_score)), 3)

        # Composite Score = 0.25*IEC_PR + 0.25*DCA + 0.15*(1-HR) + 0.15*VDCS + 0.20*ESCS
        composite = (0.25 * iec_pr) + (0.25 * dca) + (0.15 * max(0.0, 1.0 - hr)) + (0.15 * vdcs) + (0.20 * escs)
        composite = round(composite, 4)

        return BenchmarkEvaluationResult(
            bench_id=bench_id,
            config_name=config_name,
            iec_pr=iec_pr,
            dca=dca,
            hr=hr,
            vdcs=vdcs,
            escs=escs,
            composite_score=composite,
            audit_defects=report.defect_descriptions,
            smt_verified=smt_ok
        )
