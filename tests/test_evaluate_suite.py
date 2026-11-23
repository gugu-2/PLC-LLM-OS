#!/usr/bin/env python3
"""
tests/test_evaluate_suite.py — Comprehensive Audit Verification for Evaluation Suite
Reference: DOC-06 §Part 1 to §Part 6
"""

import json
import pytest
from pathlib import Path

from evaluate.hallucination_detector import detect_hallucinations, compute_hr
from evaluate.run_benchmark import evaluate_outputs, THRESHOLDS
from evaluate.ab_test import run_ab_comparison

BENCHMARK_PATH = Path(__file__).resolve().parent.parent / "evaluate" / "benchmark_31_items.json"

# ============================================================================
# 1. HALLUCINATION DETECTION PATTERN TESTS
# ============================================================================

def test_hallucination_h1_temperature():
    # Compliant
    code_ok = "FUNCTION_BLOCK FB_T\nVAR r_OvenTemp : REAL := 250.0; END_VAR\nEND_FUNCTION_BLOCK"
    assert len(detect_hallucinations(code_ok)) == 0

    # Over 1800 C
    code_high = "FUNCTION_BLOCK FB_T\nVAR r_OvenTemp : REAL := 2500.0; END_VAR\nEND_FUNCTION_BLOCK"
    h_high = detect_hallucinations(code_high)
    assert any(h["type"] == "H1_temperature_range" and h["severity"] == "critical" for h in h_high)

    # Sub-absolute zero <-273.15 C
    code_subzero = "FUNCTION_BLOCK FB_T\nVAR r_ZoneTemp : REAL := -300.0; END_VAR\nEND_FUNCTION_BLOCK"
    h_subzero = detect_hallucinations(code_subzero)
    assert any(h["type"] == "H1_temperature_range" and h["severity"] == "critical" for h in h_subzero)


def test_hallucination_h2_pressure():
    # Compliant
    code_ok = "FUNCTION_BLOCK FB_P\nVAR r_HydroPress : REAL := 350.0; END_VAR\nEND_FUNCTION_BLOCK"
    assert len(detect_hallucinations(code_ok)) == 0

    # Over 1500 bar
    code_high = "FUNCTION_BLOCK FB_P\nVAR r_CylinderPress : REAL := 2500.0; END_VAR\nEND_FUNCTION_BLOCK"
    h_high = detect_hallucinations(code_high)
    assert any(h["type"] == "H2_pressure_range" and h["severity"] == "high" for h in h_high)

    # Negative pressure below -1.0 bar
    code_neg = "FUNCTION_BLOCK FB_P\nVAR r_Pressure : REAL := -5.0; END_VAR\nEND_FUNCTION_BLOCK"
    h_neg = detect_hallucinations(code_neg)
    assert any(h["type"] == "H2_pressure_range" and h["severity"] == "high" for h in h_neg)


def test_hallucination_h3_scan_time():
    # Compliant
    code_ok = "FUNCTION_BLOCK FB_S\nVAR SCAN_TIME : REAL := 0.01; END_VAR\nEND_FUNCTION_BLOCK"
    assert len(detect_hallucinations(code_ok)) == 0

    # Under 0.1ms (0.0001s)
    code_fast = "FUNCTION_BLOCK FB_S\nVAR CYCLE_TIME : REAL := 0.00005; END_VAR\nEND_FUNCTION_BLOCK"
    h_fast = detect_hallucinations(code_fast)
    assert any(h["type"] == "H3_scan_cycle" and h["severity"] == "medium" for h in h_fast)

    # Over 2.0s
    code_slow = "FUNCTION_BLOCK FB_S\nVAR SCAN_TIME : REAL := 5.0; END_VAR\nEND_FUNCTION_BLOCK"
    h_slow = detect_hallucinations(code_slow)
    assert any(h["type"] == "H3_scan_cycle" and h["severity"] == "medium" for h in h_slow)


def test_hallucination_h4_non_square_a_matrix():
    # Square 4x4 (0..3, 0..3)
    code_sq = "FUNCTION_BLOCK FB_M\nVAR A_Matrix : ARRAY[0..3, 0..3] OF LREAL; END_VAR\nEND_FUNCTION_BLOCK"
    assert len(detect_hallucinations(code_sq)) == 0

    # Square 1-based 4x4 (1..4, 1..4)
    code_sq1 = "FUNCTION_BLOCK FB_M\nVAR A_Matrix : ARRAY[1..4, 1..4] OF LREAL; END_VAR\nEND_FUNCTION_BLOCK"
    assert len(detect_hallucinations(code_sq1)) == 0

    # Non-square 4x6 (0..3, 0..5)
    code_nonsq = "FUNCTION_BLOCK FB_M\nVAR A_Matrix : ARRAY[0..3, 0..5] OF LREAL; END_VAR\nEND_FUNCTION_BLOCK"
    h_nonsq = detect_hallucinations(code_nonsq)
    assert any(h["type"] == "H4_non_square_A_matrix" and h["severity"] == "critical" for h in h_nonsq)


def test_hallucination_h5_isa18_alarm_hierarchy():
    # Compliant HH > H > L > LL
    code_ok = """
    FUNCTION_BLOCK FB_A
    VAR
        r_Alarm_HH : REAL := 300.0;
        r_Alarm_H  : REAL := 280.0;
        r_Alarm_L  : REAL := 50.0;
        r_Alarm_LL : REAL := 20.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    assert len(detect_hallucinations(code_ok)) == 0

    # Inverted HH <= H
    code_inv_hh = """
    FUNCTION_BLOCK FB_A
    VAR
        r_Alarm_HH : REAL := 220.0;
        r_Alarm_H  : REAL := 250.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    h_hh = detect_hallucinations(code_inv_hh)
    assert any(h["type"] == "H5_alarm_tier_ordering" and h["severity"] == "critical" for h in h_hh)

    # Inverted LL >= L
    code_inv_ll = """
    FUNCTION_BLOCK FB_A
    VAR
        r_Alarm_L  : REAL := 20.0;
        r_Alarm_LL : REAL := 25.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    h_ll = detect_hallucinations(code_inv_ll)
    assert any(h["type"] == "H5_alarm_tier_ordering" and h["severity"] == "critical" for h in h_ll)


def test_hallucination_comments_stripping():
    # Flawed numbers in comments should NOT trigger hallucinations
    code_commented = """
    FUNCTION_BLOCK FB_C
    VAR
        // r_OvenTemp := 9999.0;
        (* r_HydroPress := 5000.0; *)
        (* A_Matrix : ARRAY[0..2, 0..9] OF REAL; *)
        r_OvenTemp : REAL := 200.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    assert len(detect_hallucinations(code_commented)) == 0


def test_compute_hr():
    clean_sample = "FUNCTION_BLOCK FB_OK\nVAR A : ARRAY[0..2, 0..2] OF REAL; END_VAR\nEND_FUNCTION_BLOCK"
    bad_sample = "FUNCTION_BLOCK FB_NG\nVAR A : ARRAY[0..2, 0..5] OF REAL; END_VAR\nEND_FUNCTION_BLOCK"
    assert compute_hr([]) == 0.0
    assert compute_hr([clean_sample, clean_sample]) == 0.0
    assert compute_hr([clean_sample, bad_sample]) == 0.5
    assert compute_hr([bad_sample, bad_sample]) == 1.0


# ============================================================================
# 2. BENCHMARK 31 ITEMS SECTOR COVERAGE TESTS
# ============================================================================

def test_benchmark_31_items_coverage():
    assert BENCHMARK_PATH.exists(), f"Benchmark file missing at {BENCHMARK_PATH}"
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    assert len(items) == 31, f"Expected 31 benchmark items, got {len(items)}"

    sector_counts = {}
    for it in items:
        sec = it["sector"]
        sector_counts[sec] = sector_counts.get(sec, 0) + 1
        assert "benchmark_id" in it
        assert "subsector" in it
        assert "fb_name_target" in it
        assert "prompt" in it
        assert "expected_elements" in it
        exp = it["expected_elements"]
        assert all(k in exp for k in ["has_tmr", "has_mpc", "has_fsm", "has_isa18"])

    # 6 manufacturing sectors
    expected_sectors = {
        "automotive": 5,
        "electronics": 5,
        "heavy_machinery": 5,
        "plastics": 5,
        "foodbev": 5,
        "steelmaking": 6
    }
    assert sector_counts == expected_sectors, f"Sector distribution mismatch: {sector_counts}"


# ============================================================================
# 3. BENCHMARK EVALUATION HARNESS TESTS
# ============================================================================

def make_synthetic_st(item, has_error=False, has_halluc=False):
    fb_name = item["fb_name_target"]
    sector = item["sector"]
    subsector = item["subsector"]
    temp_val = 2500.0 if has_halluc else 250.0
    a_cols = 5 if has_halluc else 3
    code = f"""FUNCTION_BLOCK {fb_name}
(* Sector: {sector} - Subsector: {subsector} *)
(* Industrial process: {item['prompt'][:100]} *)
(* Engineering physical units: [deg C] [bar] [kN] [s] [mm] *)
VAR_INPUT
    b_Enable : BOOL := TRUE;
    r_SetPoint : REAL := 100.0;
    r_Sensor_A : REAL := 100.0;
    r_Sensor_B : REAL := 100.0;
    r_Sensor_C : REAL := 100.0;
END_VAR
VAR_OUTPUT
    b_Active : BOOL := FALSE;
    r_ControlOut : REAL := 0.0;
    b_TMR_Fault : BOOL := FALSE;
END_VAR
VAR
    A_Matrix : ARRAY[0..3, 0..{a_cols}] OF LREAL;
    B_Matrix : ARRAY[0..3, 0..1] OF LREAL;
    C_Matrix : ARRAY[0..0, 0..3] OF LREAL;
    N_HORIZON : INT := 15;
    r_OvenTemp : REAL := {temp_val};
    r_Alarm_HH : REAL := 300.0;
    r_Alarm_H : REAL := 280.0;
    r_Alarm_L : REAL := 50.0;
    r_Alarm_LL : REAL := 20.0;
    r_HydroPress : REAL := 150.0;
    SCAN_TIME : REAL := 0.01;
    n_State : INT := 0;
    r_VotedVal : REAL := 0.0;
    t_DiscrepancyTimer : TON;
    b_DiscrepancyDetected : BOOL := FALSE;
    i : INT := 0;
END_VAR

// 2oo3 Triple Modular Redundancy (TMR) Voter Logic
IF (ABS(r_Sensor_A - r_Sensor_B) < 1.0) THEN
    r_VotedVal := (r_Sensor_A + r_Sensor_B) * 0.5;
ELSIF (ABS(r_Sensor_A - r_Sensor_C) < 1.0) THEN
    r_VotedVal := (r_Sensor_A + r_Sensor_C) * 0.5;
ELSE
    r_VotedVal := (r_Sensor_B + r_Sensor_C) * 0.5;
END_IF;

// Discrepancy Timer Verification
b_DiscrepancyDetected := (ABS(r_Sensor_A - r_Sensor_B) >= 1.0);
t_DiscrepancyTimer(IN := b_DiscrepancyDetected, PT := T#500ms);
IF t_DiscrepancyTimer.Q THEN
    b_TMR_Fault := TRUE;
END_IF;

// MPC Loop
FOR i := 0 TO N_HORIZON DO
    r_ControlOut := r_ControlOut + 0.1;
END_FOR;

// 4-State FSM
CASE n_State OF
    0: // INIT
        b_Active := FALSE;
        IF b_Enable THEN
            n_State := 1;
        END_IF;
    1: // RUN
        b_Active := TRUE;
        r_ControlOut := r_VotedVal;
        IF NOT b_Enable THEN
            n_State := 2;
        END_IF;
    2: // COOLDOWN
        b_Active := FALSE;
        n_State := 3;
    3: // STOPPED
        b_Active := FALSE;
        n_State := 0;
END_CASE;
"""
    if has_error:
        code += "\nIF b_Enable THEN // Parity error\n"
    code += "(* Pad token density [deg C] [bar] [kN] [s] [mm] *)\n" * 50
    code += "END_FUNCTION_BLOCK\n"
    return code


def test_evaluate_outputs_pipeline():
    with open(BENCHMARK_PATH, "r", encoding="utf-8") as f:
        items = json.load(f)

    # 1. Clean outputs
    clean_outputs = [make_synthetic_st(it) for it in items]
    res_clean = evaluate_outputs(items, clean_outputs)

    assert res_clean["total_evaluated"] == 31
    assert res_clean["metrics"]["IEC_PR"]["score"] == 1.0
    assert res_clean["metrics"]["DCA"]["score"] == 1.0
    assert res_clean["metrics"]["HR"]["score"] == 0.0
    assert res_clean["metrics"]["SEMANTIC_PASS_RATE"]["score"] == 1.0
    assert res_clean["all_automated_gates_passed"] is True

    # 2. Defective outputs (with syntax and hallucination errors)
    defective_outputs = [make_synthetic_st(it, has_error=(i < 3), has_halluc=(i in [5, 6])) for i, it in enumerate(items)]
    res_defective = evaluate_outputs(items, defective_outputs)

    assert res_defective["metrics"]["HR"]["score"] > THRESHOLDS["HR"]
    assert res_defective["metrics"]["HR"]["pass"] is False
    assert res_defective["all_automated_gates_passed"] is False


# ============================================================================
# 4. A/B TEST COMPARISON TESTS
# ============================================================================

def test_ab_test_comparison_scenarios():
    m_base = {
        "IEC_PR": {"score": 0.95},
        "DCA": {"score": 0.88},
        "HR": {"score": 0.05},
        "SEMANTIC_PASS_RATE": {"score": 0.80}
    }
    m_superior = {
        "IEC_PR": {"score": 0.99},
        "DCA": {"score": 0.96},
        "HR": {"score": 0.01},
        "SEMANTIC_PASS_RATE": {"score": 0.92}
    }
    m_subpar_iec = {
        "IEC_PR": {"score": 0.96},  # < 0.98 gate
        "DCA": {"score": 0.96},
        "HR": {"score": 0.01},
        "SEMANTIC_PASS_RATE": {"score": 0.92}
    }

    # Case 1: Superior candidate -> DEPLOY_MODEL_B
    r1 = run_ab_comparison(m_base, m_superior)
    assert r1["recommendation"] == "DEPLOY_MODEL_B"
    assert r1["model_b_wins"] == 4
    assert r1["metrics_comparison"]["HR"]["winner"] == "Model_B"

    # Case 2: Subpar IEC parity -> KEEP_MODEL_A
    r2 = run_ab_comparison(m_base, m_subpar_iec)
    assert r2["recommendation"] == "KEEP_MODEL_A"

    # Case 3: Baseline superior -> KEEP_MODEL_A
    r3 = run_ab_comparison(m_superior, m_base)
    assert r3["recommendation"] == "KEEP_MODEL_A"
    assert r3["model_b_wins"] == 0

    # Case 4: Complete tie -> KEEP_MODEL_A
    r4 = run_ab_comparison(m_base, m_base)
    assert r4["recommendation"] == "KEEP_MODEL_A"
