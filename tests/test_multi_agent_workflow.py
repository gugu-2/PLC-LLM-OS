#!/usr/bin/env python3
"""
tests/test_multi_agent_workflow.py — Test Suite for 5-Agent Engineering Assembly Line
Verifies:
1. Requirements discovery & clarification generation.
2. Architectural synthesis with state-space and TMR.
3. Multi-dialect code generation.
4. Independent static audit (non-self-certifying).
5. Z3 SMT formal proof and closed-loop delivery.
"""

import pytest
import sys
import os
from pathlib import Path

# Add root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

from plc_platform.agents.orchestrator import IndustrialEngineeringOrchestrator


def test_orchestrator_complete_workflow():
    orchestrator = IndustrialEngineeringOrchestrator()
    prompt = (
        "Generate a Siemens S7-1500 SCL function block for an automated motorcycle tubular frame "
        "robotic MIG welding cell with 2oo3 TMR temperature monitoring and state space control."
    )

    result = orchestrator.execute_workflow(prompt, allow_defaults=True)

    assert result.status == "CERTIFIED_SAFE"
    assert result.brief.target_vendor == "SIEMENS"
    assert result.brief.sector == "automotive"
    assert result.architecture is not None
    assert result.code_package is not None
    assert result.audit_report is not None
    assert result.audit_report.passed is True
    assert result.formal_proof is not None
    assert result.formal_proof.smt_proved_safe is True
    assert len(result.traceability_log) >= 5


def test_orchestrator_clarification_mode():
    orchestrator = IndustrialEngineeringOrchestrator()
    vague_prompt = "Make a controller."

    result = orchestrator.execute_workflow(vague_prompt, allow_defaults=False)

    assert result.status == "NEEDS_CLARIFICATION"
    assert len(result.clarification_questions) >= 1
    assert any("Target PLC Platform" in q for q in result.clarification_questions)


if __name__ == "__main__":
    test_orchestrator_complete_workflow()
    test_orchestrator_clarification_mode()
    print("ALL MULTI-AGENT WORKFLOW TESTS PASSED!")
