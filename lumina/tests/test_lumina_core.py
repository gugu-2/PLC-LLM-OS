"""
Lumina Core Engine & Verification Gauntlet Unit Tests
=====================================================
Tests:
  - Protocol Abstraction Layer (PAL) multi-protocol drivers & ISA-95 mapping
  - Layer 1 Static Analysis & Heuristic Linter
  - Layer 2 Z3 SMT Bounded Model Checker (Valid Proof vs. Counterexample Generation)
  - Layer 3 Digital Twin HIL Sandbox
"""

import pytest
import sys
import os

# Add backend directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from lumina_pal import PALManager, NormalizedTag, ProtocolType, DataType, SiemensS7Driver
from lumina_verify import VerificationGauntlet, Layer1StaticLinter, Layer2SMTModelChecker, Layer3DigitalTwinSandbox
from lumina_ai import LuminaAIEngine


@pytest.mark.asyncio
async def test_pal_initialization_and_tag_mapping():
    pal = PALManager()
    await pal.initialize_default_plant_topology()
    
    assert len(pal.drivers) >= 3
    assert "Line3.Servo.DecelRamp_ms" in pal.tags
    assert pal.tags["Line3.Servo.DecelRamp_ms"].value == 500
    
    # Test writing normalized tag
    success = await pal.write_normalized_tag("Line3.Servo.DecelRamp_ms", 380)
    assert success is True
    assert pal.tags["Line3.Servo.DecelRamp_ms"].value == 380


def test_layer1_static_linter_unbounded_while():
    linter = Layer1StaticLinter()
    
    bad_code = """
    PROGRAM UnsafeLoop
    VAR nCounter : INT := 0; END_VAR
    WHILE nCounter < 100 DO
        nCounter := nCounter + 1;
    END_WHILE;
    END_PROGRAM
    """
    passed, violations = linter.check(bad_code)
    assert passed is False
    assert any("WHILE" in v for v in violations)

    good_code = """
    PROGRAM SafeLoop
    VAR i : INT; END_VAR
    FOR i := 0 TO 50 DO
        // Bounded deterministic iteration
    END_FOR;
    END_PROGRAM
    """
    passed, violations = linter.check(good_code)
    assert passed is True
    assert len(violations) == 0


def test_layer2_z3_smt_bounded_model_checker_proven_safe():
    smt = Layer2SMTModelChecker()
    variables = {
        "Clamp_Closed": "BOOL",
        "Table_Indexing": "BOOL",
        "DecelRamp_ms": "INT"
    }
    transition_rules = [
        {"target": "Clamp_Closed", "type": "ASSIGN_BOOL", "condition": "bBottlePresent"},
        {"target": "Table_Indexing", "type": "ASSIGN_BOOL", "condition": {"op": "NOT", "arg": "bBottlePresent"}},
        {"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 200, "max": 800, "condition": 380}
    ]
    safety_invariants = [
        "MUTUAL_EXCLUSION_CLAMP_INDEX",
        "DECEL_RAMP_SAFE_BOUNDS"
    ]

    proved, counterexample, msg = smt.verify_safety_invariants(
        variables, transition_rules, safety_invariants, bound_steps=10
    )
    assert proved is True
    assert counterexample is None
    assert "PROVEN_SAFE" in msg


def test_layer2_z3_smt_bounded_model_checker_detects_counterexample():
    smt = Layer2SMTModelChecker()
    variables = {
        "Clamp_Closed": "BOOL",
        "Table_Indexing": "BOOL"
    }
    # Deliberately flawed logic: sets BOTH clamp and table index to TRUE simultaneously
    flawed_rules = [
        {"target": "Clamp_Closed", "type": "ASSIGN_BOOL", "condition": {"op": "OR", "args": ["bBottlePresent", "bBottlePresent"]}},
        {"target": "Table_Indexing", "type": "ASSIGN_BOOL", "condition": {"op": "OR", "args": ["bBottlePresent", "bBottlePresent"]}}
    ]
    safety_invariants = ["MUTUAL_EXCLUSION_CLAMP_INDEX"]

    proved, counterexample, msg = smt.verify_safety_invariants(
        variables, flawed_rules, safety_invariants, bound_steps=5
    )
    assert proved is False
    assert counterexample is not None
    assert "SAFETY_VIOLATION" in msg


def test_layer3_digital_twin_kinematic_simulation():
    twin = Layer3DigitalTwinSandbox()
    
    # Test safe deceleration profile
    passed, metrics, msg = twin.simulate("VAR DecelRamp := 380;", {"DecelRamp_ms": 500})
    assert passed is True
    assert metrics["collisions_detected"] == 0
    assert metrics["vibration_peak_g"] < 2.0
    assert metrics["projected_throughput_ppm"] >= 58.0

    # Test dangerous aggressive ramp (<150ms) causing motor stall
    passed, metrics, msg = twin.simulate("VAR DecelRamp := 100;", {"DecelRamp_ms": 500})
    assert passed is False
    assert metrics["collisions"] > 0
    assert "KINEMATIC_COLLISION" in msg


def test_full_3layer_verification_gauntlet():
    gauntlet = VerificationGauntlet()
    ai = LuminaAIEngine()
    
    proposal = ai.generate_optimization_for_anomaly("BEARING_VIBRATION_LINE3", {})
    
    res = gauntlet.verify(
        st_code=proposal.generated_code,
        variables=proposal.variables,
        transition_rules=proposal.transition_rules,
        safety_invariants=proposal.safety_invariants
    )
    assert res.passed is True
    assert res.smt_proved is True
    assert res.simulation_metrics["cycles_executed"] == 1000
