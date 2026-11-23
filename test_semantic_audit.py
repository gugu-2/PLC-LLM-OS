"""
test_semantic_audit.py — Comprehensive Unit & Integration Test Suite for validate_semantic.py
Audits all 5 cyber-physical semantic checks with clean and deliberately broken test cases.
"""

import sys
import json
from validate_semantic import (
    SemanticReport,
    clean_st_code,
    check_var_declarations,
    check_matrix_dimensions,
    check_fsm_completeness,
    check_mpc_horizon,
    check_tmr_completeness,
    validate_semantic_st,
)

def run_test(name, func):
    print(f"\n==================================================")
    print(f"RUNNING TEST: {name}")
    print(f"==================================================")
    try:
        passed, details = func()
        status = "PASSED" if passed else "FAILED"
        print(f"RESULT: [{status}] - {details}")
        return passed, details
    except Exception as e:
        print(f"RESULT: [EXCEPTION] - {e}")
        import traceback
        traceback.print_exc()
        return False, str(e)

# ==============================================================================
# CHECK 1: Variable Declaration Completeness & Duplicate Detection
# ==============================================================================

def test_check1_clean():
    code = """
    FUNCTION_BLOCK FB_Clean_Vars
    VAR_INPUT
        i_Execute : BOOL;
        i_Reset : BOOL;
        i_SetPoint : LREAL;
    END_VAR
    VAR_OUTPUT
        q_Busy : BOOL;
        q_Done : BOOL;
        q_Error : BOOL;
        q_ErrorID : UDINT;
    END_VAR
    VAR
        nState : INT;
        rTimer_Discrepancy : TON;
        lrFeedback : LREAL;
        lrMeasuredVal : LREAL;
        lrTargetVal : LREAL;
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test1_clean", "FB_Clean_Vars")
    check_var_declarations(code, rep)
    
    ok = (rep.verdict == "PASS" and 
          len(rep.errors) == 0 and 
          len(rep.warnings) == 0 and 
          rep.metrics.get("declared_var_count", 0) >= 10)
    return ok, f"Declared: {rep.metrics.get('declared_var_count')}, Errors: {rep.errors}, Warnings: {rep.warnings}"

def test_check1_broken_few_vars():
    code = """
    FUNCTION_BLOCK FB_Few_Vars
    VAR_INPUT
        i_Execute : BOOL;
    END_VAR
    VAR_OUTPUT
        q_Done : BOOL;
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test1_few", "FB_Few_Vars")
    check_var_declarations(code, rep)
    
    ok = (rep.verdict == "FAIL" and 
          any("abnormally few variables declared" in e for e in rep.errors))
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}"

def test_check1_broken_duplicate_vars():
    code = """
    FUNCTION_BLOCK FB_Dup_Vars
    VAR_INPUT
        i_Execute : BOOL;
        i_Reset : BOOL;
        i_SetPoint : LREAL;
        i_FeedRate : LREAL;
    END_VAR
    VAR_OUTPUT
        q_Busy : BOOL;
        q_Done : BOOL;
        q_Error : BOOL;
        q_ErrorID : UDINT;
    END_VAR
    VAR
        nState : INT;
        i_Execute : BOOL; (* DUPLICATE *)
        rTimer : TON;
        lrFeedback : LREAL;
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test1_dup", "FB_Dup_Vars")
    check_var_declarations(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          any("Duplicate variable declarations" in w for w in rep.warnings))
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

# ==============================================================================
# CHECK 2: State-Space Matrix Dimension Consistency
# ==============================================================================

def test_check2_clean():
    code = """
    FUNCTION_BLOCK FB_Clean_Matrix
    VAR
        A_Matrix : ARRAY[0..3, 0..3] OF LREAL; (* 4x4 State Matrix *)
        B_Matrix : ARRAY[0..3, 0..1] OF LREAL; (* 4x2 Input Matrix *)
        C_Matrix : ARRAY[0..1, 0..3] OF LREAL; (* 2x4 Output Matrix *)
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test2_clean", "FB_Clean_Matrix")
    check_matrix_dimensions(code, rep)
    
    ok = (rep.verdict == "PASS" and 
          len(rep.errors) == 0 and 
          "A_MATRIX" in rep.metrics.get("matrix_declarations", {}) and
          rep.metrics["matrix_declarations"]["A_MATRIX"] == (4, 4) and
          rep.metrics["matrix_declarations"]["B_MATRIX"] == (4, 2))
    return ok, f"Verdict: {rep.verdict}, Matrices: {rep.metrics.get('matrix_declarations')}, Errors: {rep.errors}"

def test_check2_broken_non_square_a():
    code = """
    FUNCTION_BLOCK FB_NonSquare_A
    VAR
        A_Matrix : ARRAY[0..2, 0..3] OF LREAL; (* 3x4 State Matrix -> INVALID! *)
        B_Matrix : ARRAY[0..2, 0..1] OF LREAL; (* 3x2 Input Matrix *)
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test2_non_square", "FB_NonSquare_A")
    check_matrix_dimensions(code, rep)
    
    ok = (rep.verdict == "FAIL" and 
          any("is non-square: 3x4 (must be nxn)" in e for e in rep.errors))
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}"

def test_check2_broken_dimension_mismatch():
    code = """
    FUNCTION_BLOCK FB_Dim_Mismatch
    VAR
        A_Matrix : ARRAY[0..3, 0..3] OF LREAL; (* 4x4 State Matrix *)
        B_Matrix : ARRAY[0..2, 0..1] OF LREAL; (* 3x2 Input Matrix -> Mismatch: 3 != 4! *)
    END_VAR
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test2_mismatch", "FB_Dim_Mismatch")
    check_matrix_dimensions(code, rep)
    
    ok = (rep.verdict == "FAIL" and 
          any("Dimension mismatch between state matrix" in e for e in rep.errors))
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}"

# ==============================================================================
# CHECK 3: FSM State Completeness & Deadlock Transition Detection
# ==============================================================================

def test_check3_clean():
    code = """
    FUNCTION_BLOCK FB_Clean_FSM
    VAR
        nState : INT;
        bStart : BOOL;
        bDone : BOOL;
        bFault : BOOL;
    END_VAR
    CASE nState OF
        0: (* INIT *)
            IF bStart THEN
                nState := 10;
            END_IF;
        10: (* RUNNING *)
            IF bDone THEN
                nState := 20;
            ELSIF bFault THEN
                nState := 999;
            END_IF;
        20: (* COMPLETING *)
            nState := 0;
        STATE_ERROR: (* SINK EXEMPT *)
            bFault := TRUE;
    END_CASE;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test3_clean", "FB_Clean_FSM")
    check_fsm_completeness(code, rep)
    
    ok = (rep.verdict == "PASS" and 
          len(rep.errors) == 0 and 
          len(rep.warnings) == 0 and 
          rep.metrics.get("fsm_nState_states", 0) == 4)
    return ok, f"Verdict: {rep.verdict}, States: {rep.metrics.get('fsm_nState_states')}, Warnings: {rep.warnings}"

def test_check3_broken_missing_fsm():
    code = """
    FUNCTION_BLOCK FB_No_FSM
    VAR
        x : INT;
    END_VAR
    x := x + 1;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test3_no_fsm", "FB_No_FSM")
    check_fsm_completeness(code, rep)
    
    ok = (rep.verdict == "FAIL" and 
          any("No CASE State OF state-machine construct found" in e for e in rep.errors))
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}"

def test_check3_broken_too_few_states():
    code = """
    FUNCTION_BLOCK FB_Few_States
    VAR
        nState : INT;
    END_VAR
    CASE nState OF
        0:
            nState := 1;
        1:
            nState := 0;
    END_CASE;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test3_few_states", "FB_Few_States")
    check_fsm_completeness(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          any("has only 2 states" in w for w in rep.warnings))
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

def test_check3_broken_deadlock_state():
    code = """
    FUNCTION_BLOCK FB_Deadlock_FSM
    VAR
        nState : INT;
        bStart : BOOL;
    END_VAR
    CASE nState OF
        0: (* INIT *)
            IF bStart THEN
                nState := 10;
            END_IF;
        10: (* PROCESSING - DEADLOCK! No transition statement *)
            bStart := FALSE;
        20: (* COMPLETING *)
            nState := 0;
        STATE_FAULT: (* SINK EXEMPT *)
            bStart := FALSE;
    END_CASE;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test3_deadlock", "FB_Deadlock_FSM")
    check_fsm_completeness(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          rep.warnings == ["FSM state(s) without detected outgoing transition: ['10']"])
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

# ==============================================================================
# CHECK 4: MPC Prediction Horizon Unroll Verification
# ==============================================================================

def test_check4_clean():
    code = """
    FUNCTION_BLOCK FB_Clean_MPC
    VAR
        i : INT;
        PRED_HORIZON : INT := 15;
    END_VAR
    (* ModelPredictive Control Formulation *)
    FOR i := 0 TO PRED_HORIZON DO
        (* Unrolled MPC state extrapolation *)
    END_FOR;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test4_clean", "FB_Clean_MPC")
    check_mpc_horizon(code, rep)
    
    ok = (rep.verdict == "PASS" and 
          len(rep.errors) == 0 and 
          len(rep.warnings) == 0 and 
          rep.metrics.get("mpc_declared_n") == 15 and 
          rep.metrics.get("mpc_horizon_loops", 0) >= 1)
    return ok, f"Verdict: {rep.verdict}, N: {rep.metrics.get('mpc_declared_n')}, Loops: {rep.metrics.get('mpc_horizon_loops')}, Warnings: {rep.warnings}"

def test_check4_broken_missing_mpc():
    code = """
    FUNCTION_BLOCK FB_Simple_Actuator
    VAR
        lrPosition : LREAL;
    END_VAR
    lrPosition := 1.0;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test4_no_mpc", "FB_Simple_Actuator")
    check_mpc_horizon(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          any("No Model Predictive Control (MPC) references detected" in w for w in rep.warnings))
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

def test_check4_broken_short_horizon():
    code = """
    FUNCTION_BLOCK FB_Short_Horizon
    VAR
        i : INT;
        N_HORIZON : INT := 4;
    END_VAR
    (* MPC Optimization *)
    FOR i := 0 TO N_HORIZON DO
        (* short loop *)
    END_FOR;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test4_short_horizon", "FB_Short_Horizon")
    check_mpc_horizon(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          any("MPC Prediction Horizon is N=4 (recommended N >= 10" in w for w in rep.warnings))
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

# ==============================================================================
# CHECK 5: 2oo3 Triple Modular Redundancy (TMR) Voter & Discrepancy Timer
# ==============================================================================

def test_check5_clean():
    code = """
    FUNCTION_BLOCK FB_Clean_TMR
    VAR
        bTMR_Voter_Output : BOOL;
        Timer_Discrepancy : TON;
    END_VAR
    (* 2oo3 Triple Modular Redundant Voting Logic *)
    bTMR_Voter_Output := (ChA AND ChB) OR (ChB AND ChC) OR (ChA AND ChC);
    (* Discrepancy detection *)
    Timer_Discrepancy(IN := (ChA <> ChB) OR (ChB <> ChC), PT := T#50MS);
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test5_clean", "FB_Clean_TMR")
    check_tmr_completeness(code, rep)
    
    ok = (rep.verdict == "PASS" and 
          rep.metrics.get("has_tmr") == True and 
          rep.metrics.get("has_tmr_discrepancy") == True and 
          len(rep.errors) == 0 and 
          len(rep.warnings) == 0)
    return ok, f"Verdict: {rep.verdict}, TMR: {rep.metrics.get('has_tmr')}, Discrepancy: {rep.metrics.get('has_tmr_discrepancy')}"

def test_check5_broken_missing_tmr():
    code = """
    FUNCTION_BLOCK FB_Single_Channel_Sensor
    VAR
        sensorVal : REAL;
    END_VAR
    sensorVal := 12.5;
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test5_no_tmr", "FB_Single_Channel_Sensor")
    check_tmr_completeness(code, rep)
    
    ok = (rep.verdict == "FAIL" and 
          any("Missing 2oo3 Triple Modular Redundancy (TMR) voting logic" in e for e in rep.errors))
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}"

def test_check5_broken_missing_discrepancy():
    code = """
    FUNCTION_BLOCK FB_Triple_Voter_Standalone
    VAR
        bTMR_Voter_Out : BOOL;
    END_VAR
    (* 2oo3 Voting Logic *)
    bTMR_Voter_Out := (ChA AND ChB) OR (ChB AND ChC) OR (ChA AND ChC);
    END_FUNCTION_BLOCK
    """
    rep = SemanticReport("test5_no_discrepancy", "FB_Triple_Voter_Standalone")
    check_tmr_completeness(code, rep)
    
    ok = (rep.verdict == "WARN" and 
          any("no discrepancy / deviation timer detected" in w for w in rep.warnings))
    return ok, f"Verdict: {rep.verdict}, Warnings: {rep.warnings}"

# ==============================================================================
# INTEGRATION TESTS: Full Function Blocks
# ==============================================================================

def test_full_golden_function_block():
    code = """
    FUNCTION_BLOCK FB_Golden_Industrial_Controller
    VAR_INPUT
        i_bExecute : BOOL;
        i_bReset : BOOL;
        i_lrChA_Pressure : LREAL;
        i_lrChB_Pressure : LREAL;
        i_lrChC_Pressure : LREAL;
    END_VAR
    VAR_OUTPUT
        q_bActive : BOOL;
        q_bFault : BOOL;
        q_lrVotedPressure : LREAL;
        q_lrControlEffort : LREAL;
        q_nStateCode : INT;
    END_VAR
    VAR
        nState : INT;
        PRED_HORIZON : INT := 12;
        i : INT;
        A_Matrix : ARRAY[0..3, 0..3] OF LREAL;
        B_Matrix : ARRAY[0..3, 0..1] OF LREAL;
        C_Matrix : ARRAY[0..1, 0..3] OF LREAL;
        fbTimer_Discrepancy : TON;
        lrDiscrepancyLimit : LREAL := 2.5;
        bTMR_VoterFault : BOOL;
        b2oo3_VoterActive : BOOL;
    END_VAR

    (* 2oo3 Triple Modular Redundancy (TMR) Voting Algorithm *)
    IF (i_lrChA_Pressure >= i_lrChB_Pressure AND i_lrChA_Pressure <= i_lrChC_Pressure) OR
       (i_lrChA_Pressure >= i_lrChC_Pressure AND i_lrChA_Pressure <= i_lrChB_Pressure) THEN
        q_lrVotedPressure := i_lrChA_Pressure;
    ELSIF (i_lrChB_Pressure >= i_lrChA_Pressure AND i_lrChB_Pressure <= i_lrChC_Pressure) OR
          (i_lrChB_Pressure >= i_lrChC_Pressure AND i_lrChB_Pressure <= i_lrChA_Pressure) THEN
        q_lrVotedPressure := i_lrChB_Pressure;
    ELSE
        q_lrVotedPressure := i_lrChC_Pressure;
    END_IF;

    (* Discrepancy Timer Verification *)
    fbTimer_Discrepancy(
        IN := (ABS(i_lrChA_Pressure - i_lrChB_Pressure) > lrDiscrepancyLimit) OR
              (ABS(i_lrChB_Pressure - i_lrChC_Pressure) > lrDiscrepancyLimit),
        PT := T#100MS
    );
    bTMR_VoterFault := fbTimer_Discrepancy.Q;

    (* Model Predictive Control (MPC) Horizon Unroll *)
    FOR i := 0 TO PRED_HORIZON DO
        (* Predict state propagation x[k+1] = A x[k] + B u[k] *)
        q_lrControlEffort := q_lrControlEffort + 0.1;
    END_FOR;

    (* Finite State Machine Logic *)
    CASE nState OF
        0: (* STATE_INIT *)
            IF i_bExecute THEN
                nState := 10;
            END_IF;
        10: (* STATE_RUNNING *)
            IF bTMR_VoterFault THEN
                nState := 999;
            ELSIF NOT i_bExecute THEN
                nState := 20;
            END_IF;
        20: (* STATE_SHUTDOWN *)
            nState := 0;
        999: (* STATE_FAULT_SINK *)
            IF i_bReset THEN
                nState := 0;
            END_IF;
    END_CASE;
    END_FUNCTION_BLOCK
    """
    rep = validate_semantic_st(code, "golden_fb.st")
    ok = (rep.verdict == "PASS" and len(rep.errors) == 0 and len(rep.warnings) == 0)
    return ok, f"Verdict: {rep.verdict}, Errors: {rep.errors}, Warnings: {rep.warnings}, Metrics: {json.dumps(rep.metrics)}"

def test_full_catastrophic_failure_block():
    code = """
    FUNCTION_BLOCK FB_Catastrophic_Failure
    VAR
        a : INT;
        b : INT;
        A_Matrix : ARRAY[0..2, 0..4] OF LREAL; (* Non-square: 3x5 *)
        B_Matrix : ARRAY[0..1, 0..1] OF LREAL; (* Dimension mismatch: 2 rows != 3 rows *)
    END_VAR
    (* No State Machine *)
    (* Standalone assignment *)
    a := a + 1;
    END_FUNCTION_BLOCK
    """
    rep = validate_semantic_st(code, "catastrophic.st")
    has_few_vars = any("abnormally few variables" in e for e in rep.errors)
    has_non_square = any("is non-square" in e for e in rep.errors)
    has_dim_mismatch = any("Dimension mismatch" in e for e in rep.errors)
    has_no_fsm = any("No CASE State OF" in e for e in rep.errors)
    has_no_tmr = any("Missing 2oo3 Triple Modular Redundancy" in e for e in rep.errors)
    
    ok = (rep.verdict == "FAIL" and 
          has_few_vars and 
          has_non_square and 
          has_dim_mismatch and 
          has_no_fsm and 
          has_no_tmr)
    return ok, f"Verdict: {rep.verdict}, Errors Count: {len(rep.errors)} (Expected >= 5), Errors: {rep.errors}"

def main():
    suite = [
        ("Check 1 [Clean]: Variable Declarations >= 10, No Duplicates", test_check1_clean),
        ("Check 1 [Broken]: Abnormally Few Variables (< 10)", test_check1_broken_few_vars),
        ("Check 1 [Broken]: Duplicate Variable Declarations", test_check1_broken_duplicate_vars),
        ("Check 2 [Clean]: Consistent State-Space Matrices (Square A 4x4, B 4x2)", test_check2_clean),
        ("Check 2 [Broken]: Non-Square State Matrix A (3x4)", test_check2_broken_non_square_a),
        ("Check 2 [Broken]: Matrix Dimension Row Mismatch (A 4x4 vs B 3x2)", test_check2_broken_dimension_mismatch),
        ("Check 3 [Clean]: FSM State Completeness & Deadlock-Free Transitions", test_check3_clean),
        ("Check 3 [Broken]: Missing CASE State Construct", test_check3_broken_missing_fsm),
        ("Check 3 [Broken]: FSM Too Few States (< 3)", test_check3_broken_too_few_states),
        ("Check 3 [Broken]: FSM State Deadlock (Missing Outgoing Transition)", test_check3_broken_deadlock_state),
        ("Check 4 [Clean]: MPC Horizon Unroll N >= 10 and Iteration Loop", test_check4_clean),
        ("Check 4 [Broken]: Missing MPC References", test_check4_broken_missing_mpc),
        ("Check 4 [Broken]: MPC Prediction Horizon Short (N < 10)", test_check4_broken_short_horizon),
        ("Check 5 [Clean]: 2oo3 TMR Voter & Discrepancy Timer", test_check5_clean),
        ("Check 5 [Broken]: Missing 2oo3 TMR Voting Logic", test_check5_broken_missing_tmr),
        ("Check 5 [Broken]: TMR Present but Missing Discrepancy Timer", test_check5_broken_missing_discrepancy),
        ("Integration [Clean]: Golden Industrial Controller FB (All 5 Checks Satisfied)", test_full_golden_function_block),
        ("Integration [Broken]: Catastrophic Failure FB (All 5 Checks Violated Simultaneously)", test_full_catastrophic_failure_block),
    ]

    results = []
    for name, fn in suite:
        passed, details = run_test(name, fn)
        results.append((name, passed, details))

    total = len(results)
    passed_count = sum(1 for _, p, _ in results if p)
    failed_count = total - passed_count

    print("\n" + "=" * 60)
    print("AUDIT EXECUTION SUMMARY REPORT")
    print("=" * 60)
    print(f"Total Test Cases: {total}")
    print(f"Passed:           {passed_count}")
    print(f"Failed:           {failed_count}")
    print(f"Pass Rate:        {(passed_count/total)*100:.1f}%\n")

    for name, p, det in results:
        status_str = "PASS" if p else "FAIL"
        print(f"[{status_str}] {name}")

    if failed_count > 0:
        sys.exit(1)
    else:
        print("\nALL SEMANTIC AUDIT TEST CASES VERIFIED SUCCESSFULLY.")
        sys.exit(0)

if __name__ == "__main__":
    main()
