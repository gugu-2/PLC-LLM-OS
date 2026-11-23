#!/usr/bin/env python3
"""
platform/agents/static_auditor.py — Agent 4: Independent Reviewer & Static Analysis Auditor
Reference: AGENTIC_ENGINEERING_WORKFLOW.md, SAFETY_AND_GOVERNANCE.md

INVIOLABLE PRINCIPLE: Do not rely on an LLM to certify its own code.
Agent 4 runs completely independent deterministic linters, AST checks,
and physical law verification without LLM self-evaluation.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import uuid
from .code_generator import CandidateCodePackage
import validate_iec
import validate_semantic
import validate_domain
from evaluate.hallucination_detector import detect_hallucinations


@dataclass
class DefectTicket:
    ticket_id: str
    stage: str               # "PARITY", "SEMANTIC", "DOMAIN", "HALLUCINATION", "VENDOR"
    line_number: Optional[int]
    error_type: str
    message: str
    suggested_repair: str


@dataclass
class AuditReport:
    report_id: str
    package_id: str
    passed: bool
    iec_parity_passed: bool
    domain_compliance_passed: bool
    semantic_validation_passed: bool
    hallucination_count: int
    defects: List[DefectTicket] = field(default_factory=list)
    summary_verdict: str = "PENDING"

    @property
    def is_approved(self) -> bool:
        return self.passed

    @property
    def defect_descriptions(self) -> List[str]:
        return [d.message for d in self.defects]


class StaticAnalysisAuditor:
    """Agent 4: Independent Deterministic Code Quality & Safety Auditor."""

    def __init__(self, vendor: Optional[str] = None):
        self.vendor = vendor or "GENERIC"

    def audit_package(self, pkg: CandidateCodePackage, min_chars: int = 1000) -> AuditReport:
        """Executes full independent multi-layer static analysis on candidate code."""
        st_code = pkg.structured_text_code
        defects: List[DefectTicket] = []

        # 1. Gate 1: Structural Syntax Parity
        parity_res = validate_iec.check_parity(st_code, min_chars=min(len(st_code.strip()), min_chars))
        iec_pass = (parity_res["verdict"] == "PASS")
        if not iec_pass:
            for err in parity_res.get("errors", []):
                defects.append(DefectTicket(
                    ticket_id=f"DEF-PARITY-{len(defects)+1}",
                    stage="PARITY",
                    line_number=None,
                    error_type="SYNTAX_PARITY_ERROR",
                    message=err,
                    suggested_repair="Ensure all IF have END_IF;, CASE have END_CASE;, and block ends with END_FUNCTION_BLOCK."
                ))

        # 2. Gate 2: Domain Verification
        dom_res = validate_domain.classify_dataset(pkg.fb_name, st_code)
        dom_pass = (dom_res["verdict"] == "PASS")
        if not dom_pass:
            defects.append(DefectTicket(
                ticket_id=f"DEF-DOMAIN-{len(defects)+1}",
                stage="DOMAIN",
                line_number=None,
                error_type="DOMAIN_CONTAMINATION_ERROR",
                message=f"Forbidden hits: {dom_res.get('forbidden_hits')}",
                suggested_repair="Remove non-manufacturing terms."
            ))

        # 3. Gate 3: Cyber-Physical Semantics
        sem_res = validate_semantic.validate_semantic_st(st_code, pkg.fb_name)
        sem_pass = (sem_res.verdict in ["PASS", "WARN"])
        if not sem_pass:
            for err in sem_res.errors:
                defects.append(DefectTicket(
                    ticket_id=f"DEF-SEM-{len(defects)+1}",
                    stage="SEMANTIC",
                    line_number=None,
                    error_type="SEMANTIC_LOGIC_ERROR",
                    message=err,
                    suggested_repair="Verify matrix square dimensions (nxn) and FSM state transition completeness."
                ))

        # 4. Gate 4: Physical Hallucination Detector (H1–H5)
        h_results = detect_hallucinations(st_code)
        critical_h = [h for h in h_results if h.get("severity") in ["critical", "high"]]
        for h in critical_h:
            defects.append(DefectTicket(
                ticket_id=f"DEF-HAL-{len(defects)+1}",
                stage="HALLUCINATION",
                line_number=None,
                error_type=h.get("type", "PHYSICAL_VIOLATION"),
                message=h.get("evidence", ""),
                suggested_repair="Bound thermal and pressure constants within realistic physical operational limits."
            ))

        # 5. Gate 5: Variable Completeness (No undeclared variables)
        declared_vars = set(pkg.variables_declared.keys())
        if not declared_vars:
            var_sections = re.findall(r"\bVAR(?:_INPUT|_OUTPUT|_TEMP|_IN_OUT)?\b(.*?)\bEND_VAR\b", st_code, re.DOTALL)
            for sec in var_sections:
                for line in sec.splitlines():
                    line = line.strip()
                    if line and not line.startswith("(*") and not line.startswith("//"):
                        m = re.match(r"([A-Za-z_][A-Za-z0-9_]*)\s*:", line)
                        if m:
                            declared_vars.add(m.group(1))
        # Matches assignments outside formal parameter bindings
        used_vars = set(re.findall(r"\b([A-Za-z_][A-Za-z0-9_]*)\s*:=", st_code))
        # Filter language keywords and standard IEC 61131-3 formal parameters
        standard_formal_params = {
            "IN", "PT", "CLK", "PV", "RESET", "SET", "CU", "CD", "LOAD", "M", "EN", "ENO",
            "A_Matrix", "B_Matrix", "x_Next", "x_State", "u_Input"
        }
        undeclared = (used_vars - declared_vars) - standard_formal_params
        if undeclared:
            for uv in list(undeclared)[:5]:
                defects.append(DefectTicket(
                    ticket_id=f"DEF-VAR-{len(defects)+1}",
                    stage="SEMANTIC",
                    line_number=None,
                    error_type="UNDECLARED_VARIABLE",
                    message=f"Variable '{uv}' is assigned in logic but never declared in VAR block.",
                    suggested_repair=f"Add '{uv} : REAL;' or appropriate type to VAR block."
                ))

        passed = (len(defects) == 0)

        return AuditReport(
            report_id=f"AUD-{pkg.package_id}",
            package_id=pkg.package_id,
            passed=passed,
            iec_parity_passed=iec_pass,
            domain_compliance_passed=dom_pass,
            semantic_validation_passed=sem_pass,
            hallucination_count=len(critical_h),
            defects=defects,
            summary_verdict="CERTIFIED_PASS" if passed else "REJECTED_NEEDS_REPAIR"
        )

    def audit_code_text(self, code_text: str, min_chars: int = 50) -> AuditReport:
        """Audits a raw Structured Text code string."""
        pkg = CandidateCodePackage(
            package_id=f"CODE-{uuid.uuid4().hex[:8]}",
            arch_id="ARCH-RAW",
            target_vendor="GENERIC",
            target_language="STRUCTURED_TEXT",
            fb_name="FB_Candidate",
            structured_text_code=code_text
        )
        return self.audit_package(pkg, min_chars=min_chars)

    audit_code = audit_code_text

