#!/usr/bin/env python3
"""
tests/test_evaluation_harness.py — Unit Tests for 5-Way Comparative Benchmark Suite
Tests 31-benchmark catalog, 5 core metrics calculation, and comparative scorecard table.
"""

import pytest
from plc_platform.evaluate import (
    BenchmarkSuite,
    MetricsCalculator,
    ComparativeBenchmarkRunner,
    ComparativeScorecard
)


def test_benchmark_suite_completeness():
    benches = BenchmarkSuite.get_all_benchmarks()
    assert len(benches) == 31
    sectors = {b.sector for b in benches}
    assert "AUTOMOTIVE" in sectors
    assert "ELECTRONICS" in sectors
    assert "HEAVY_MACHINERY" in sectors
    assert "PLASTICS" in sectors
    assert "FOOD_BEVERAGE" in sectors


def test_metrics_calculator_syntax_and_hallucination():
    calc = MetricsCalculator()

    # Code with syntax error (missing END_IF) and foreign Java hallucination
    bad_code = """
FUNCTION_BLOCK FB_BadTest
VAR_INPUT
    b_Start : BOOL;
END_VAR
IF b_Start THEN
    System.out.println("Actuator Started");
END_FUNCTION_BLOCK
"""
    res = calc.evaluate_candidate(
        bench_id="BENCH-TEST",
        config_name="BASE",
        code_text=bad_code,
        target_vendor="SIEMENS",
        expected_states=["STATE_INIT"],
        safety_invariants=[]
    )

    assert res.iec_pr < 1.0  # Failed parity
    assert res.hr > 0.0     # Caught System.out hallucination
    assert res.smt_verified is False


def test_metrics_calculator_certified_safe_code():
    calc = MetricsCalculator()

    safe_code = """
FUNCTION_BLOCK FB_SafeTest
VAR_INPUT
    b_SystemEnable : BOOL; // Permissive [ms]
    b_EStop_OK : BOOL; // Safety circuit [ms]
    r_Sensor_ChA_Raw : REAL; // Sensor A [bar]
    r_Sensor_ChB_Raw : REAL; // Sensor B [bar]
    r_ClampForce : REAL; // Actuator clamp [kN]
END_VAR
VAR_OUTPUT
    b_Running : BOOL;
    b_FaultActive : BOOL;
END_VAR
VAR
    r_State_X : ARRAY[0..3] OF REAL;
END_VAR
IF NOT b_EStop_OK OR NOT b_SystemEnable THEN
    b_Running := FALSE;
    b_FaultActive := TRUE;
    RETURN;
END_IF;
b_Running := TRUE;
r_State_X[0] := 0.95 * r_State_X[0] + 0.05 * r_Sensor_ChA_Raw;
END_FUNCTION_BLOCK
"""
    res = calc.evaluate_candidate(
        bench_id="BENCH-SAFE",
        config_name="FINETUNED_RAG_GAUNTLET",
        code_text=safe_code,
        target_vendor="GENERIC_IEC",
        expected_states=[],
        safety_invariants=["NOT b_EStop_OK => b_Running = FALSE"]
    )

    assert res.iec_pr == 1.0
    assert res.hr == 0.0
    assert res.smt_verified is True
    assert res.composite_score > 0.85


def test_comparative_runner_slice():
    runner = ComparativeBenchmarkRunner()
    # Run on a 2-benchmark slice across all 5 tiers
    sample_benches = BenchmarkSuite.get_all_benchmarks()[:2]
    scorecard = runner.run_benchmark_suite(benchmarks=sample_benches)

    assert len(scorecard.summaries) == 5
    assert "BASE" in scorecard.summaries
    assert "BASE_RAG" in scorecard.summaries
    assert "FINETUNED" in scorecard.summaries
    assert "FINETUNED_RAG" in scorecard.summaries
    assert "FINETUNED_RAG_GAUNTLET" in scorecard.summaries

    # Monotonic progression: Gauntlet outperforms Base significantly
    base_comp = scorecard.summaries["BASE"].mean_composite
    gauntlet_comp = scorecard.summaries["FINETUNED_RAG_GAUNTLET"].mean_composite
    assert gauntlet_comp > base_comp

    md_table = scorecard.to_markdown_table()
    assert "| Evaluation Tier |" in md_table
    assert "FINETUNED_RAG_GAUNTLET" in md_table
