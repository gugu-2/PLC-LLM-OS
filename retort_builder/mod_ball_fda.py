# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_ball_fda.py
Implements Phase 4: C.O. Ball Process Deviation & Thermal Lethality Assurance Engine
in strict compliance with FDA 21 CFR Part 113 for Low-Acid Canned Foods (LACF).
"""

def generate_ball_fda():
    return '''(* =====================================================================================================================
 * PHASE 4: C.O. BALL PROCESS DEVIATION & THERMAL LETHALITY ASSURANCE ENGINE
 * Regulatory Compliance: US FDA 21 CFR Part 113 (Thermal Processing of Low-Acid Canned Foods)
 * Algorithmic Features:
 *   1. Automated Thermal Process Deviation Detection (Tv < Scheduled Cook Temp - 0.50 deg C)
 *   2. C.O. Ball Mathematical Process Time Formulation:
 *        B = fh * [ LOG10(jch * Ih) - LOG10(g) ]
 *   3. Dynamic Lethality Deficit Quadrature: Supplemental Hold Time Calculation
 *   4. Legal Batch Sterility Certification & FDA 21 CFR 113 Compliance Bit-Packing
 * ===================================================================================================================== *)

(* -------------------------------------------------------------------------
 * SUB-SECTION 4.1: BALL PROCESS PARAMETERS EVALUATION
 * ------------------------------------------------------------------------- *)
(* Ih: Initial Temperature Difference Between Scheduled Retort Steam and Initial Food Core *)
rBall_Ih := rSet_TargetCookTemp_degC - 20.0;
IF rBall_Ih < 1.0 THEN
    rBall_Ih := 1.0; (* Prevent non-positive singularity in logarithmic evaluation *)
END_IF;

(* g: Temperature Difference Between Retort Steam and Product Cold-Spot Core *)
rBall_g := rSet_TargetCookTemp_degC - rVotedCanCoreTemp_degC;
IF rBall_g < 0.05 THEN
    rBall_g := 0.05; (* Container cold-spot has achieved asymptotic thermal equilibrium *)
END_IF;

(* Evaluate C.O. Ball Scheduled Cook Time B [minutes] *)
(* Formula: B = fh * ( LOG10(jch * Ih) - LOG10(g) ) *)
rTempCalc1 := rSet_Ball_jch * rBall_Ih;
IF rTempCalc1 > 0.0 THEN
    rTempCalc2 := LN(rTempCalc1) / 2.302585092994046; (* LOG10(jch * Ih) *)
ELSE
    rTempCalc2 := 1.0;
END_IF;

rTempCalc3 := LN(rBall_g) / 2.302585092994046; (* LOG10(g) *)
rBall_ScheduledCookDuration_s := rSet_Ball_fh_min * (rTempCalc2 - rTempCalc3) * 60.0;

(* Clamp scheduled cook duration to operator recipe floor *)
IF rBall_ScheduledCookDuration_s < rSet_ScheduledCookTime_s THEN
    rBall_ScheduledCookDuration_s := rSet_ScheduledCookTime_s;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 4.2: FDA 21 CFR PART 113 PROCESS DEVIATION DETECTION
 * A process deviation occurs if during the Sterilization Hold Stage (State 5),
 * the voted vessel temperature drops more than 0.50 deg C below recipe setpoint.
 * ------------------------------------------------------------------------- *)
IF (iFSM_CurrentState = 5) THEN
    IF rVotedVesselTemp_degC < (rSet_TargetCookTemp_degC - 0.50) THEN
        bBall_DeviationLatching := TRUE;
        bBall_CatchupActive     := TRUE;
        rBall_DevCookRampDown_s := rBall_DevCookRampDown_s + rTs_s;
        dwFDAComplianceWord     := dwFDAComplianceWord OR 16#0000_0004; (* Process Deviation Recorded *)
        dwWarningWord           := dwWarningWord OR 16#0000_0010;       (* Sub-lethal Cook Temp Deviation *)
    END_IF;
END_IF;

(* -------------------------------------------------------------------------
 * SUB-SECTION 4.3: DYNAMIC LETHALITY DEFICIT & SUPPLEMENTAL TIME CALCULATION
 * If a deviation occurs, calculate the exact additional cooking time required
 * at current temperature to guarantee batch achieves target F0 lethality.
 * Supplemental Time = (Target F0 - Current F0) / Instantaneous Lethality Rate
 * ------------------------------------------------------------------------- *)
IF bBall_CatchupActive THEN
    IF rIntegratedF0 < rSet_TargetF0_min THEN
        rTempCalc1 := rSet_TargetF0_min - rIntegratedF0; (* F0 Deficit [min] *)
        IF rInstantLethality > 0.010 THEN
            (* Supplemental cook seconds needed at current kill rate *)
            rBall_SuppleTimeNeeded_s := (rTempCalc1 / rInstantLethality) * 60.0;
        ELSE
            (* Ineffective temperature: assume baseline rate at scheduled temp *)
            rTempCalc2 := EXP(((rSet_TargetCookTemp_degC - rRefSterilTemp_degC) / rSet_Ball_z_degC) * 2.302585);
            rBall_SuppleTimeNeeded_s := (rTempCalc1 / rTempCalc2) * 60.0;
        END_IF;
    ELSE
        rBall_SuppleTimeNeeded_s := 0.0;
        bBall_CatchupActive     := FALSE; (* Deficit satisfied *)
    END_IF;
ELSE
    rBall_SuppleTimeNeeded_s := 0.0;
END_IF;

rBallCatchupTimeRemaining_s := rBall_SuppleTimeNeeded_s;

(* -------------------------------------------------------------------------
 * SUB-SECTION 4.4: BATCH STERILITY CERTIFICATION STATUS
 * ------------------------------------------------------------------------- *)
IF rIntegratedF0 >= rSet_TargetF0_min THEN
    bProcessQualified_FDA := TRUE;
    dwFDAComplianceWord   := dwFDAComplianceWord OR 16#0000_0001; (* FDA Part 113 Sterility Satisfied *)
ELSE
    bProcessQualified_FDA := FALSE;
END_IF;

IF bBall_CatchupActive THEN
    bBallDeviationCatchupActive := TRUE;
    dwFDAComplianceWord         := dwFDAComplianceWord OR 16#0000_0002; (* Catch-up Mode Active *)
ELSE
    bBallDeviationCatchupActive := FALSE;
END_IF;

(* Process Cook Timers Tracking *)
IF (iFSM_CurrentState = 5) THEN
    rBall_CookAccumulated_s := rBall_CookAccumulated_s + rTs_s;
    IF rBall_ScheduledCookDuration_s > rBall_CookAccumulated_s THEN
        rRemainingCookTime_s := rBall_ScheduledCookDuration_s - rBall_CookAccumulated_s;
    ELSE
        rRemainingCookTime_s := 0.0;
    END_IF;
ELSIF (iFSM_CurrentState = 6) THEN
    (* Deviation hold mode: time remaining is the dynamic supplemental time *)
    rRemainingCookTime_s := rBallCatchupTimeRemaining_s;
ELSE
    rRemainingCookTime_s := 0.0;
END_IF;
'''

if __name__ == "__main__":
    b = generate_ball_fda();
    print("Ball FDA length:", len(b))
    print(b[:300])
