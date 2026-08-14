"""
Lumina ICS Cybersecurity & Hardware Deployment Proxy Tests
==========================================================
Tests:
  - Safety PLC air-gapping (rejection of SIL 2/3 memory writes)
  - Cognitive AI meta-monitor burst detection
  - Semantic target drift detection
  - Golden Master cryptographic rollback
"""

import pytest
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "backend"))

from lumina_security import HardwareDeploymentProxy


def test_safety_plc_air_gap_policy_rejection():
    proxy = HardwareDeploymentProxy()

    # Attempt to write to a Safety Tag
    passed, reason = proxy.inspect_and_filter(
        target_machine="Line3_RotaryCapper",
        target_tag="SAFETY_GUARD_INTERLOCK_SIL3",
        code_payload="// Malicious attempt to bypass safety door"
    )
    assert passed is False
    assert "POLICY_VIOLATION" in reason
    assert "SIL 2/3" in reason


def test_cognitive_meta_monitor_burst_attack_circuit_breaker():
    proxy = HardwareDeploymentProxy()

    # Fire 12 rapid deployment requests in a loop
    results = []
    for i in range(12):
        passed, reason = proxy.inspect_and_filter(
            target_machine="Line3_Infeed",
            target_tag="Line3.Servo.DecelRamp_ms",
            code_payload=f"VAR nRamp : INT := {380 + i};"
        )
        results.append(passed)

    # First 9 should pass, but 10th+ must trigger the circuit breaker!
    assert any(r is True for r in results[:9])
    assert results[-1] is False
    assert "CIRCUIT_BREAKER_TRIPPED" in proxy.audit_log[-1].reason


def test_semantic_target_drift_detection():
    proxy = HardwareDeploymentProxy()

    # Line 3 packaging AI trying to write to Central Refrigeration Chiller PLC
    passed, reason = proxy.inspect_and_filter(
        target_machine="Line3_Infeed",
        target_tag="Utilities.AmmoniaChiller.CompressorSetpoint",
        code_payload="VAR Setpoint : REAL := -12.0;"
    )
    assert passed is False
    assert "SEMANTIC_DRIFT_DETECTED" in reason


def test_golden_master_cryptographic_rollback():
    proxy = HardwareDeploymentProxy()

    res = proxy.execute_golden_rollback("Line3_Infeed")
    assert res["success"] is True
    assert "signature" in res
    assert res["restored_state"]["Line3.Servo.DecelRamp_ms"] == 500
    assert "Successfully rolled back" in res["message"]
