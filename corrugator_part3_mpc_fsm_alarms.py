# -*- coding: utf-8 -*-
"""
Part 3 of FB_Packaging_Corrugator_SingleFacer_FlyingShear
Contains: Phase 3 (State Space Model & Observer), Phase 4 (Receding-Horizon MPC),
          Phase 5 (12-Stage Production FSM), Phase 6 (ISA-18.2 Alarms & Diagnostic Words),
          and END_FUNCTION_BLOCK.
"""

def get_part3():
    return '''
(* =====================================================================================================================
 * PHASE 3: DISCRETE STATE-SPACE MODEL PROPAGATION & LUENBERGER OBSERVER
 * =====================================================================================================================
 * 8-State Discrete Cyber-Physical Dynamics:
 *   x[1]: Upper corrugating roll surface temperature T_corrug [deg C]
 *   x[2]: Starch adhesive dynamic liquid film thickness h_glue [um]
 *   x[3]: Bridge web accumulator buffer length L_bridge [m]
 *   x[4]: Double-backer Zone 1 steam chest plate temp T_sb1 [deg C]
 *   x[5]: Double-backer Zone 2 steam chest plate temp T_sb2 [deg C]
 *   x[6]: Combined board residual moisture content M_board [%]
 *   x[7]: Dry-end web entry tension F_tension [N]
 *   x[8]: Flying cutoff shear synchronization phase error Delta_theta [mrad]
 *
 * 4-Actuator Inputs:
 *   u[1]: Single-facer steam modulating valve position [0.0 to 100.0 %]
 *   u[2]: Starch glue applicator gap servo position trim [-50.0 to +50.0 um]
 *   u[3]: Double-backer steam chest control valve position [0.0 to 100.0 %]
 *   u[4]: Flying shear knife servo velocity trim command [-15.0 to +15.0 m/min]
 *
 * Model Equations:
 *   x[k+1] = A * x[k] + B * u[k]
 *   y[k]   = C * x[k] + D * u[k]
 *   x_hat[k] = x_pred[k] + L * (y_meas[k] - y_est[k])
 *)

(* 1. MATRIX COEFFICIENT INITIALIZATION *)
(* Matrix A (8x8): Discrete-time state transition at Ts = 10 ms *)
rMat_A[1, 1] := 0.9982; rMat_A[1, 2] := 0.0000; rMat_A[1, 3] := 0.0000; rMat_A[1, 4] := 0.0000; rMat_A[1, 5] := 0.0000; rMat_A[1, 6] := -0.0012; rMat_A[1, 7] := 0.0000; rMat_A[1, 8] := 0.0000;
rMat_A[2, 1] := -0.0015; rMat_A[2, 2] := 0.9850; rMat_A[2, 3] := 0.0000; rMat_A[2, 4] := 0.0000; rMat_A[2, 5] := 0.0000; rMat_A[2, 6] := 0.0000; rMat_A[2, 7] := 0.0000; rMat_A[2, 8] := 0.0000;
rMat_A[3, 1] := 0.0000; rMat_A[3, 2] := 0.0000; rMat_A[3, 3] := 1.0000; rMat_A[3, 4] := 0.0000; rMat_A[3, 5] := 0.0000; rMat_A[3, 6] := 0.0000; rMat_A[3, 7] := -0.0005; rMat_A[3, 8] := 0.0000;
rMat_A[4, 1] := 0.0000; rMat_A[4, 2] := 0.0000; rMat_A[4, 3] := 0.0000; rMat_A[4, 4] := 0.9940; rMat_A[4, 5] := 0.0015; rMat_A[4, 6] := -0.0025; rMat_A[4, 7] := 0.0000; rMat_A[4, 8] := 0.0000;
rMat_A[5, 1] := 0.0000; rMat_A[5, 2] := 0.0000; rMat_A[5, 3] := 0.0000; rMat_A[5, 4] := 0.0020; rMat_A[5, 5] := 0.9935; rMat_A[5, 6] := -0.0030; rMat_A[5, 7] := 0.0000; rMat_A[5, 8] := 0.0000;
rMat_A[6, 1] := -0.0008; rMat_A[6, 2] := 0.0045; rMat_A[6, 3] := 0.0000; rMat_A[6, 4] := -0.0022; rMat_A[6, 5] := -0.0035; rMat_A[6, 6] := 0.9910; rMat_A[6, 7] := 0.0000; rMat_A[6, 8] := 0.0000;
rMat_A[7, 1] := 0.0000; rMat_A[7, 2] := 0.0000; rMat_A[7, 3] := 0.0085; rMat_A[7, 4] := 0.0000; rMat_A[7, 5] := 0.0000; rMat_A[7, 6] := 0.0120; rMat_A[7, 7] := 0.9780; rMat_A[7, 8] := 0.0000;
rMat_A[8, 1] := 0.0000; rMat_A[8, 2] := 0.0000; rMat_A[8, 3] := 0.0000; rMat_A[8, 4] := 0.0000; rMat_A[8, 5] := 0.0000; rMat_A[8, 6] := 0.0000; rMat_A[8, 7] := 0.0002; rMat_A[8, 8] := 0.9920;

(* Matrix B (8x4): Actuation input coupling *)
rMat_B[1, 1] := 0.0450; rMat_B[1, 2] := 0.0000; rMat_B[1, 3] := 0.0000; rMat_B[1, 4] := 0.0000;
rMat_B[2, 1] := 0.0000; rMat_B[2, 2] := 0.3850; rMat_B[2, 3] := 0.0000; rMat_B[2, 4] := 0.0000;
rMat_B[3, 1] := 0.0000; rMat_B[3, 2] := 0.0000; rMat_B[3, 3] := 0.0000; rMat_B[3, 4] := 0.0000;
rMat_B[4, 1] := 0.0000; rMat_B[4, 2] := 0.0000; rMat_B[4, 3] := 0.0650; rMat_B[4, 4] := 0.0000;
rMat_B[5, 1] := 0.0000; rMat_B[5, 2] := 0.0000; rMat_B[5, 3] := 0.0820; rMat_B[5, 4] := 0.0000;
rMat_B[6, 1] := -0.0015; rMat_B[6, 2] := 0.0080; rMat_B[6, 3] := -0.0042; rMat_B[6, 4] := 0.0000;
rMat_B[7, 1] := 0.0000; rMat_B[7, 2] := 0.0000; rMat_B[7, 3] := 0.0000; rMat_B[7, 4] := -0.0250;
rMat_B[8, 1] := 0.0000; rMat_B[8, 2] := 0.0000; rMat_B[8, 3] := 0.0000; rMat_B[8, 4] := 0.0520;

(* Matrix C (8x8): Output measurement mapping *)
FOR nIdx_i := 1 TO 8 DO
    FOR nIdx_j := 1 TO 8 DO
        IF nIdx_i = nIdx_j THEN
            rMat_C[nIdx_i, nIdx_j] := 1.0;
        ELSE
            rMat_C[nIdx_i, nIdx_j] := 0.0;
        END_IF;
    END_FOR;
END_FOR;

(* Matrix D (8x4): Direct transmission *)
FOR nIdx_i := 1 TO 8 DO
    FOR nIdx_j := 1 TO 4 DO
        rMat_D[nIdx_i, nIdx_j] := 0.0;
    END_FOR;
END_FOR;

(* Luenberger Observer Innovation Matrix L (8x8) *)
FOR nIdx_i := 1 TO 8 DO
    FOR nIdx_j := 1 TO 8 DO
        IF nIdx_i = nIdx_j THEN
            rMat_L[nIdx_i, nIdx_j] := 0.125;
        ELSE
            rMat_L[nIdx_i, nIdx_j] := 0.0;
        END_IF;
    END_FOR;
END_FOR;

(* 2. SENSOR MEASUREMENT VECTOR PACKING *)
rVec_Y_Meas[1] := rAct_UpperRollTempVoted_degC;
rVec_Y_Meas[2] := rGlueFilmThickness_um;
rVec_Y_Meas[3] := rBridgeAccumulatorLength_Act;
rVec_Y_Meas[4] := rPlateTemp_Zone1_Act;
rVec_Y_Meas[5] := rPlateTemp_Zone2_Act;
rVec_Y_Meas[6] := 0.5 * (rBoardMoistureTopLiner_Pct + rBoardMoistureBottomLiner_Pct);
rVec_Y_Meas[7] := rAct_WebTensionEntryDB_N;
rVec_Y_Meas[8] := rKnifeCutoffPhaseError_deg * (3.14159265 / 180.0) * 1000.0; (* mrad *)

(* 3. STATE ESTIMATION & PREDICTION EQUATIONS *)
(* Estimate output: y_est = C * x + D * u *)
FOR nIdx_i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR nIdx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMat_C[nIdx_i, nIdx_j] * rVec_X[nIdx_j]);
    END_FOR;
    FOR nIdx_j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (rMat_D[nIdx_i, nIdx_j] * rVec_U[nIdx_j]);
    END_FOR;
    rVec_Y_Est[nIdx_i] := rTemp_Sum;
END_FOR;

(* Innovation correction: x_hat = x + L * (y_meas - y_est) *)
FOR nIdx_i := 1 TO 8 DO
    rTemp_Diff := rVec_Y_Meas[nIdx_i] - rVec_Y_Est[nIdx_i];
    rTemp_Sum := 0.0;
    FOR nIdx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMat_L[nIdx_i, nIdx_j] * rTemp_Diff);
    END_FOR;
    rVec_X[nIdx_i] := rVec_X[nIdx_i] + rTemp_Sum;
END_FOR;

(* Time update prediction: x_pred = A * x + B * u *)
FOR nIdx_i := 1 TO 8 DO
    rTemp_Sum := 0.0;
    FOR nIdx_j := 1 TO 8 DO
        rTemp_Sum := rTemp_Sum + (rMat_A[nIdx_i, nIdx_j] * rVec_X[nIdx_j]);
    END_FOR;
    FOR nIdx_j := 1 TO 4 DO
        rTemp_Sum := rTemp_Sum + (rMat_B[nIdx_i, nIdx_j] * rVec_U[nIdx_j]);
    END_FOR;
    rVec_X_Pred[nIdx_i] := rTemp_Sum;
    rVec_X[nIdx_i] := rVec_X_Pred[nIdx_i];
END_FOR;


(* =====================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * =====================================================================================================================
 * Quadratic Cost Formulation:
 *   J = (x - x_ref)^T * Q * (x - x_ref) + Delta_u^T * R * Delta_u + (x_pred - x_ref)^T * P * (x_pred - x_ref)
 * Penalizes sheet cutoff length error (Q[8,8]), moisture deviation (Q[6,6]), roll temperature drift (Q[1,1]),
 * glue film error (Q[2,2]), steam modulating valve throttling rate (R[1,1], R[3,3]), and glue gap servo travel (R[2,2]).
 * Solved via iterative Projected Gradient Descent under operational box constraints.
 *)

(* 1. REFERENCE TRAJECTORY VECTOR INITIALIZATION *)
rVec_X_Ref[1] := 172.0; (* Optimal roll temperature setpoint [deg C] *)
rVec_X_Ref[2] := 18.0;  (* Optimal liquid starch film thickness [um] *)
rVec_X_Ref[3] := 25.0;  (* Nominal bridge buffer length [m] *)
rVec_X_Ref[4] := rT_SteamChestZone1_Setpt;
rVec_X_Ref[5] := rT_SteamChestZone2_Setpt;
rVec_X_Ref[6] := 7.0;   (* Target board moisture [%] *)
rVec_X_Ref[7] := 450.0; (* Web tension reference [N] *)
rVec_X_Ref[8] := 0.0;   (* Zero cutoff phase error [mrad] *)

(* Actuator Reference Points *)
rVec_U_Ref[1] := 55.0; (* Steam valve nominal 55 % *)
rVec_U_Ref[2] := 0.0;  (* Starch gap trim 0 um *)
rVec_U_Ref[3] := 62.0; (* Double backer steam valve nominal 62 % *)
rVec_U_Ref[4] := 0.0;  (* Knife servo speed trim 0 m/min *)

(* 2. PENALTY WEIGHTING MATRICES Q, R, P *)
FOR nIdx_i := 1 TO 8 DO
    FOR nIdx_j := 1 TO 8 DO
        rMat_Q[nIdx_i, nIdx_j] := 0.0;
        rMat_P[nIdx_i, nIdx_j] := 0.0;
    END_FOR;
END_FOR;

(* Diagonal state error weights Q *)
rMat_Q[1, 1] := 12.0;  (* Roll temperature penalty *)
rMat_Q[2, 2] := 25.0;  (* Glue film thickness penalty *)
rMat_Q[3, 3] := 5.0;   (* Bridge buffer length penalty *)
rMat_Q[4, 4] := 8.0;   (* Steam chest Zone 1 penalty *)
rMat_Q[5, 5] := 10.0;  (* Steam chest Zone 2 penalty *)
rMat_Q[6, 6] := 45.0;  (* Board moisture penalty (critical for warp prevention) *)
rMat_Q[7, 7] := 4.0;   (* Web tension penalty *)
rMat_Q[8, 8] := 150.0; (* Sheet cutoff length error penalty (highest precision priority) *)

(* Diagonal terminal state weights P *)
FOR nIdx_i := 1 TO 8 DO
    rMat_P[nIdx_i, nIdx_i] := 1.5 * rMat_Q[nIdx_i, nIdx_i];
END_FOR;

(* Diagonal actuator control effort penalty weights R *)
FOR nIdx_i := 1 TO 4 DO
    FOR nIdx_j := 1 TO 4 DO
        rMat_R[nIdx_i, nIdx_j] := 0.0;
    END_FOR;
END_FOR;
rMat_R[1, 1] := 2.5;   (* Single-facer steam valve movement penalty *)
rMat_R[2, 2] := 15.0;  (* Glue applicator servo gap movement penalty *)
rMat_R[3, 3] := 3.0;   (* Double-backer steam valve movement penalty *)
rMat_R[4, 4] := 8.5;   (* Knife servo speed trim adjustment penalty *)

(* Actuator Box Constraints *)
rU_Min[1] := 5.0;   rU_Max[1] := 95.0;  rDelta_U_Max[1] := 5.0;  (* Valve % *)
rU_Min[2] := -40.0; rU_Max[2] := 40.0;  rDelta_U_Max[2] := 2.5;  (* Gap trim um *)
rU_Min[3] := 10.0;  rU_Max[3] := 95.0;  rDelta_U_Max[3] := 6.0;  (* Valve % *)
rU_Min[4] := -15.0; rU_Max[4] := 15.0;  rDelta_U_Max[4] := 3.0;  (* Speed trim m/min *)

(* 3. PROJECTED GRADIENT DESCENT OPTIMIZATION SOLVER *)
IF bMpcEnable_Cmd AND (eCorrugatorState = cSTATE_07_CONTINUOUS_HIGH_SPEED) THEN
    (* Initialize optimal controls with current actuation *)
    FOR nIdx_i := 1 TO 4 DO
        rVec_U_Opt[nIdx_i] := rVec_U[nIdx_i];
    END_FOR;

    FOR nIdx_iter := 1 TO nMpcMaxIter DO
        (* Compute cost function gradient with respect to actuator increment:
         * Grad = 2 * (B^T * Q * (x - x_ref) + R * (u - u_ref))
         *)
        FOR nIdx_i := 1 TO 4 DO
            rTemp_Sum := 0.0;
            FOR nIdx_j := 1 TO 8 DO
                rTemp_Diff := rVec_X[nIdx_j] - rVec_X_Ref[nIdx_j];
                rTemp_Sum := rTemp_Sum + (rMat_B[nIdx_j, nIdx_i] * rMat_Q[nIdx_j, nIdx_j] * rTemp_Diff);
            END_FOR;
            rTemp_Term := rMat_R[nIdx_i, nIdx_i] * (rVec_U_Opt[nIdx_i] - rVec_U_Ref[nIdx_i]);
            rGrad_J[nIdx_i] := 2.0 * (rTemp_Sum + rTemp_Term);
        END_FOR;

        (* Projected gradient step with saturation *)
        FOR nIdx_i := 1 TO 4 DO
            rVec_Delta_U[nIdx_i] := -rMpcStepSize_Alpha * rGrad_J[nIdx_i];
            (* Slew rate clamp *)
            rVec_Delta_U[nIdx_i] := MAX(-rDelta_U_Max[nIdx_i], MIN(rDelta_U_Max[nIdx_i], rVec_Delta_U[nIdx_i]));
            (* Apply step *)
            rVec_U_Opt[nIdx_i] := rVec_U_Opt[nIdx_i] + rVec_Delta_U[nIdx_i];
            (* Box constraint projection *)
            rVec_U_Opt[nIdx_i] := MAX(rU_Min[nIdx_i], MIN(rU_Max[nIdx_i], rVec_U_Opt[nIdx_i]));
        END_FOR;
    END_FOR;

    (* Apply calculated optimal control actions to internal vector *)
    FOR nIdx_i := 1 TO 4 DO
        rVec_U[nIdx_i] := rVec_U_Opt[nIdx_i];
    END_FOR;

    (* Pack MPC Diagnostic Word *)
    dwDiagnosticWord_MPC := DWORD#16#00000001; (* Solver converged *)
    IF rVec_U_Opt[1] >= rU_Max[1] OR rVec_U_Opt[1] <= rU_Min[1] THEN
        dwDiagnosticWord_MPC := dwDiagnosticWord_MPC OR DWORD#16#00000002; (* Actuator 1 at limit *)
    END_IF;
    IF rVec_U_Opt[2] >= rU_Max[2] OR rVec_U_Opt[2] <= rU_Min[2] THEN
        dwDiagnosticWord_MPC := dwDiagnosticWord_MPC OR DWORD#16#00000004; (* Actuator 2 at limit *)
    END_IF;
    IF rVec_U_Opt[3] >= rU_Max[3] OR rVec_U_Opt[3] <= rU_Min[3] THEN
        dwDiagnosticWord_MPC := dwDiagnosticWord_MPC OR DWORD#16#00000008; (* Actuator 3 at limit *)
    END_IF;
    IF rVec_U_Opt[4] >= rU_Max[4] OR rVec_U_Opt[4] <= rU_Min[4] THEN
        dwDiagnosticWord_MPC := dwDiagnosticWord_MPC OR DWORD#16#00000010; (* Actuator 4 at limit *)
    END_IF;
ELSE
    (* Fallback feedforward controls *)
    rVec_U[1] := 50.0;
    rVec_U[2] := 0.0;
    rVec_U[3] := 55.0;
    rVec_U[4] := 0.0;
    dwDiagnosticWord_MPC := DWORD#16#00000000;
END_IF;


(* =====================================================================================================================
 * PHASE 5: 12-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * =====================================================================================================================
 * Stage 1:  cSTATE_01_ROLL_PREHEAT             - Thermal Crowning Soak & Slow Spin (170 deg C)
 * Stage 2:  cSTATE_02_GLUE_LINE_PRIME          - Starch Circulation Loop Conditioning & Viscosity Stabilization
 * Stage 3:  cSTATE_03_PAPER_WEB_THREADING      - Vacuum Threading Tables & Nip Insertion
 * Stage 4:  cSTATE_04_SLOW_INCHING             - First Flute Formation & Glue Transfer (25 m/min, 15 bar nip)
 * Stage 5:  cSTATE_05_SPEED_ACCELERATION_RAMP  - Acceleration to 150 m/min, Nip Clamp to 25 bar
 * Stage 6:  cSTATE_06_BRIDGE_ACCUMULATION      - Bridge Festoon Charging & Double-Backer Pre-Heat
 * Stage 7:  cSTATE_07_CONTINUOUS_HIGH_SPEED    - Continuous 400 m/min Corrugating with Closed-Loop MPC
 * Stage 8:  cSTATE_08_FLYING_SPLICE_CHANGEOVER - High-Speed Flying Splice, Slitter/Scorer Tool Index Swap
 * Stage 9:  cSTATE_09_GLUE_DAM_FLUSH           - Automated Adhesive Tray Water Rinse & Dam Scraper
 * Stage 10: cSTATE_10_ROLL_RETRACTION          - Hydraulic Nip De-Clamping & Mechanical Retraction
 * Stage 11: cSTATE_11_CONTROLLED_COOLDOWN      - Controlled Roll Thermal Cool-Down & Bow Prevention
 * Stage 12: cSTATE_12_EMERGENCY_WRAPUP_STOP    - Optical Paper Wrap-Up Jam Fast Safety Trip (< 100 ms)
 *)

(* Master Safety Priority Interlock *)
IF bEmergencyStop_Trip OR bAlm_WebWrapUpJam_HH THEN
    eCorrugatorState := cSTATE_12_EMERGENCY_WRAPUP_STOP;
END_IF;

(* Track state transition entry pulse *)
IF eCorrugatorState <> eCorrugatorPrevState THEN
    bStateEntry := TRUE;
    rStateTimer_Sec := 0.0;
    eCorrugatorPrevState := eCorrugatorState;
ELSE
    bStateEntry := FALSE;
    rStateTimer_Sec := rStateTimer_Sec + rT_CycleTime_Sec;
END_IF;

CASE eCorrugatorState OF

    cSTATE_01_ROLL_PREHEAT:
        (* Entry actions *)
        IF bStateEntry THEN
            bCmd_SteamHeaderIsolationValve_Open := TRUE;
            bCmd_RollRetractHydraulicCyl_Retract := FALSE;
            bCmd_EmergencyBrakeEngage := FALSE;
        END_IF;

        (* Slow rotation to prevent roll sag / thermal deflection *)
        rCmd_SingleFacerDrive_Speed := 8.0; (* 8 m/min slow spin *)
        rCmd_BridgeConveyorDrive_Speed := 0.0;
        rCmd_DoubleBackerDrive_Speed := 0.0;
        rCmd_FlyingShearKnife_ServoVelocity := 0.0;
        rCmd_NipHydraulicPropValve_Pct := 10.0; (* Minimal nip touch *)
        rCmd_SteamChestZone1_Valve_Pct := 40.0;
        rCmd_SteamChestZone2_Valve_Pct := 40.0;
        rCmd_SteamChestZone3_Valve_Pct := 30.0;

        (* Transition to Glue Line Prime once rolls reach 165 deg C and soak for 60 s *)
        IF (rAct_UpperRollTempVoted_degC >= 165.0) AND (rAct_LowerRollTempVoted_degC >= 165.0) AND
           (rStateTimer_Sec >= 60.0) AND bSystemEnable_Cmd THEN
            eCorrugatorState := cSTATE_02_GLUE_LINE_PRIME;
        END_IF;

    cSTATE_02_GLUE_LINE_PRIME:
        IF bStateEntry THEN
            bCmd_GlueDamWashSolenoid_Open := FALSE;
        END_IF;

        rCmd_SingleFacerDrive_Speed := 8.0;
        rCmd_StarchApplicatorGap_ServoPos := 0.200; (* Calibrated prime gap *)
        rCmd_NipHydraulicPropValve_Pct := 15.0;

        (* Verify starch viscosity is within spec (35 to 55 s) and glue pump recirculating for 30 s *)
        IF (rVisc_StarchSteinHall_Sec >= 35.0) AND (rVisc_StarchSteinHall_Sec <= 55.0) AND
           (rStateTimer_Sec >= 30.0) THEN
            eCorrugatorState := cSTATE_03_PAPER_WEB_THREADING;
        END_IF;

    cSTATE_03_PAPER_WEB_THREADING:
        rCmd_SingleFacerDrive_Speed := 12.0; (* Threading creep speed *)
        rCmd_BridgeConveyorDrive_Speed := 12.0;
        rCmd_DoubleBackerDrive_Speed := 12.0;
        rCmd_NipHydraulicPropValve_Pct := 20.0;
        rCmd_BridgeFestoonSuctionBrake_Pct := 15.0;

        (* Operator verifies paper insertion and web tension latches above 100 N *)
        IF (rAct_WebTensionEntryDB_N >= 100.0) AND (rStateTimer_Sec >= 20.0) THEN
            eCorrugatorState := cSTATE_04_SLOW_INCHING;
        END_IF;

    cSTATE_04_SLOW_INCHING:
        rCmd_SingleFacerDrive_Speed := 25.0; (* 25 m/min inching *)
        rCmd_BridgeConveyorDrive_Speed := 25.0;
        rCmd_DoubleBackerDrive_Speed := 25.0;
        rCmd_NipHydraulicPropValve_Pct := 60.0; (* 15 bar nip clamping *)
        rCmd_StarchApplicatorGap_ServoPos := rGap_StarchApplicatorNominal_Setpt;

        (* Transition to Acceleration Ramp when web is stable for 15 s *)
        IF (rCalc_StarchFilmCoatWeight_gsm >= 10.0) AND (rStateTimer_Sec >= 15.0) AND bAutoSpeedTrack_Enable THEN
            eCorrugatorState := cSTATE_05_SPEED_ACCELERATION_RAMP;
        END_IF;

    cSTATE_05_SPEED_ACCELERATION_RAMP:
        (* Accelerate line up to 150 m/min at controlled 1.5 m/s2 *)
        rCmd_SingleFacerDrive_Speed := MIN(150.0, 25.0 + (1.5 * rStateTimer_Sec * 60.0));
        rCmd_BridgeConveyorDrive_Speed := rCmd_SingleFacerDrive_Speed;
        rCmd_DoubleBackerDrive_Speed := rCmd_SingleFacerDrive_Speed;
        rCmd_NipHydraulicPropValve_Pct := 100.0; (* Full 25 bar nip pressure *)

        IF (rAct_LineSpeedMaster_m_min >= 140.0) THEN
            eCorrugatorState := cSTATE_06_BRIDGE_ACCUMULATION;
        END_IF;

    cSTATE_06_BRIDGE_ACCUMULATION:
        (* Over-speed single facer slightly (+15 m/min) to charge bridge accumulator *)
        rCmd_SingleFacerDrive_Speed := 165.0;
        rCmd_BridgeConveyorDrive_Speed := 160.0;
        rCmd_DoubleBackerDrive_Speed := 150.0;

        (* Once bridge web length reaches 22 m and catenary sag is within 800 - 1200 mm, transition to high speed *)
        IF (rBridgeAccumulatorLength_Act >= 22.0) AND
           (rAct_BridgeSagVoted_mm >= 800.0) AND (rAct_BridgeSagVoted_mm <= 1200.0) THEN
            eCorrugatorState := cSTATE_07_CONTINUOUS_HIGH_SPEED;
        END_IF;

    cSTATE_07_CONTINUOUS_HIGH_SPEED:
        (* High-Speed Production up to 400 m/min with Full Multivariable MPC *)
        IF bAutoSpeedTrack_Enable THEN
            rCmd_DoubleBackerDrive_Speed := rV_TargetLineSpeed_Setpt;
            rCmd_SingleFacerDrive_Speed  := rV_TargetLineSpeed_Setpt + (0.5 * (25.0 - rBridgeAccumulatorLength_Act));
            rCmd_BridgeConveyorDrive_Speed := 0.5 * (rCmd_SingleFacerDrive_Speed + rCmd_DoubleBackerDrive_Speed);
        END_IF;

        (* Modulating steam valves governed by MPC actuator outputs *)
        rCmd_SteamChestZone1_Valve_Pct := rVec_U[3] * 0.95;
        rCmd_SteamChestZone2_Valve_Pct := rVec_U[3] * 1.05;
        rCmd_SteamChestZone3_Valve_Pct := rVec_U[3] * 0.90;

        (* Transitions: Order Change Flying Splice, Retraction, or Faults *)
        IF bOrderChangeFlyingSplice_Cmd THEN
            eCorrugatorState := cSTATE_08_FLYING_SPLICE_CHANGEOVER;
        ELSIF bRollRetraction_Cmd THEN
            eCorrugatorState := cSTATE_10_ROLL_RETRACTION;
        ELSIF bGlueFlushPurge_Cmd THEN
            eCorrugatorState := cSTATE_09_GLUE_DAM_FLUSH;
        END_IF;

    cSTATE_08_FLYING_SPLICE_CHANGEOVER:
        IF bStateEntry THEN
            bCmd_FlyingSpliceNipEngage := TRUE;
            bCmd_SlitterScorerIndexShift := TRUE;
            bSlitterIndexBusy := TRUE;
            rSlitterIndexTimer_Sec := 0.0;
        END_IF;

        (* Temporarily depress double-backer speed to 300 m/min during splice contact *)
        rCmd_DoubleBackerDrive_Speed := 300.0;
        rCmd_SingleFacerDrive_Speed := 300.0;

        rSlitterIndexTimer_Sec := rSlitterIndexTimer_Sec + rT_CycleTime_Sec;
        IF rSlitterIndexTimer_Sec >= 2.5 THEN
            bCmd_FlyingSpliceNipEngage := FALSE;
            bCmd_SlitterScorerIndexShift := FALSE;
            bSlitterIndexBusy := FALSE;
            eCorrugatorState := cSTATE_07_CONTINUOUS_HIGH_SPEED;
        END_IF;

    cSTATE_09_GLUE_DAM_FLUSH:
        IF bStateEntry THEN
            bCmd_GlueDamWashSolenoid_Open := TRUE;
        END_IF;

        rCmd_SingleFacerDrive_Speed := 15.0;
        rCmd_StarchApplicatorGap_ServoPos := 0.350; (* Fully open gap *)
        rCmd_NipHydraulicPropValve_Pct := 10.0;

        IF rStateTimer_Sec >= 45.0 THEN
            bCmd_GlueDamWashSolenoid_Open := FALSE;
            eCorrugatorState := cSTATE_10_ROLL_RETRACTION;
        END_IF;

    cSTATE_10_ROLL_RETRACTION:
        IF bStateEntry THEN
            bCmd_RollRetractHydraulicCyl_Retract := TRUE;
        END_IF;

        rCmd_SingleFacerDrive_Speed := 10.0;
        rCmd_DoubleBackerDrive_Speed := 10.0;
        rCmd_NipHydraulicPropValve_Pct := 0.0; (* Zero nip pressure *)

        IF rStateTimer_Sec >= 20.0 THEN
            eCorrugatorState := cSTATE_11_CONTROLLED_COOLDOWN;
        END_IF;

    cSTATE_11_CONTROLLED_COOLDOWN:
        (* Slow rotation to cool rolls below 60 deg C without bow *)
        rCmd_SingleFacerDrive_Speed := 5.0;
        rCmd_DoubleBackerDrive_Speed := 0.0;
        rCmd_FlyingShearKnife_ServoVelocity := 0.0;
        bCmd_SteamHeaderIsolationValve_Open := FALSE;

        IF (rAct_UpperRollTempVoted_degC <= 65.0) AND (rAct_LowerRollTempVoted_degC <= 65.0) THEN
            rCmd_SingleFacerDrive_Speed := 0.0;
        END_IF;

    cSTATE_12_EMERGENCY_WRAPUP_STOP:
        (* Sub-100 ms fast stop *)
        bCmd_EmergencyBrakeEngage := TRUE;
        bCmd_RollRetractHydraulicCyl_Retract := TRUE;
        bCmd_SteamHeaderIsolationValve_Open := FALSE;
        rCmd_SingleFacerDrive_Speed := 0.0;
        rCmd_BridgeConveyorDrive_Speed := 0.0;
        rCmd_DoubleBackerDrive_Speed := 0.0;
        rCmd_FlyingShearKnife_ServoVelocity := 0.0;
        rCmd_NipHydraulicPropValve_Pct := 0.0;

        IF bFaultReset_Cmd AND NOT bEmergencyStop_Trip AND NOT bAlm_WebWrapUpJam_HH THEN
            bCmd_EmergencyBrakeEngage := FALSE;
            eCorrugatorState := cSTATE_01_ROLL_PREHEAT;
        END_IF;

END_CASE;


(* =====================================================================================================================
 * PHASE 6: ISA-18.2 PROCESS ALARM ENGINE & STATUS WORD PACKING
 * =====================================================================================================================
 * Tiered Alarm Detection with Deadband Hysteresis:
 * - Upper Corrugating Roll Temperature (HH / H / L / LL)
 * - Steam Header Supply Pressure (HH / H / L / LL)
 * - Bridge Web Catenary Sag (HH / H / L / LL)
 * - Double-Backer Entry Web Tension (HH / H / L / LL)
 * - Flying Cutoff Shear Length Error (HH / H)
 * - Web Wrap-Up Jam Fast Detector (HH)
 * - Priority Escalation: Unacknowledged Warning H escalates to HH after 45 s.
 *)

(* 1. UPPER ROLL TEMPERATURE ALARM EVALUATION *)
IF rAct_UpperRollTempVoted_degC >= cALM_TEMP_ROLL_HH THEN
    bAlm_TempRoll_HH := TRUE;
ELSIF rAct_UpperRollTempVoted_degC <= (cALM_TEMP_ROLL_HH - cALM_TEMP_DEADBAND) THEN
    bAlm_TempRoll_HH := FALSE;
END_IF;

IF rAct_UpperRollTempVoted_degC >= cALM_TEMP_ROLL_H THEN
    bAlm_TempRoll_H := TRUE;
    rTimer_AlmEscalate_TempH := rTimer_AlmEscalate_TempH + rT_CycleTime_Sec;
    IF rTimer_AlmEscalate_TempH >= cTIME_ALARM_ESCALATION_SEC THEN
        bAlm_TempRoll_HH := TRUE; (* Escalated to Critical *)
    END_IF;
ELSIF rAct_UpperRollTempVoted_degC <= (cALM_TEMP_ROLL_H - cALM_TEMP_DEADBAND) THEN
    bAlm_TempRoll_H := FALSE;
    rTimer_AlmEscalate_TempH := 0.0;
END_IF;

IF rAct_UpperRollTempVoted_degC <= cALM_TEMP_ROLL_LL THEN
    bAlm_TempRoll_LL := TRUE;
ELSIF rAct_UpperRollTempVoted_degC >= (cALM_TEMP_ROLL_LL + cALM_TEMP_DEADBAND) THEN
    bAlm_TempRoll_LL := FALSE;
END_IF;

IF rAct_UpperRollTempVoted_degC <= cALM_TEMP_ROLL_L THEN
    bAlm_TempRoll_L := TRUE;
ELSIF rAct_UpperRollTempVoted_degC >= (cALM_TEMP_ROLL_L + cALM_TEMP_DEADBAND) THEN
    bAlm_TempRoll_L := FALSE;
END_IF;

(* 2. STEAM SUPPLY PRESSURE ALARM EVALUATION *)
IF rVec_Y_Meas[1] >= cALM_PRESS_STEAM_HH THEN
    bAlm_PressSteam_HH := TRUE;
ELSIF rVec_Y_Meas[1] <= (cALM_PRESS_STEAM_HH - cALM_PRESS_DEADBAND) THEN
    bAlm_PressSteam_HH := FALSE;
END_IF;

IF rVec_Y_Meas[1] >= cALM_PRESS_STEAM_H THEN
    bAlm_PressSteam_H := TRUE;
    rTimer_AlmEscalate_PressH := rTimer_AlmEscalate_PressH + rT_CycleTime_Sec;
    IF rTimer_AlmEscalate_PressH >= cTIME_ALARM_ESCALATION_SEC THEN
        bAlm_PressSteam_HH := TRUE;
    END_IF;
ELSIF rVec_Y_Meas[1] <= (cALM_PRESS_STEAM_H - cALM_PRESS_DEADBAND) THEN
    bAlm_PressSteam_H := FALSE;
    rTimer_AlmEscalate_PressH := 0.0;
END_IF;

IF rVec_Y_Meas[1] <= cALM_PRESS_STEAM_LL THEN
    bAlm_PressSteam_LL := TRUE;
ELSIF rVec_Y_Meas[1] >= (cALM_PRESS_STEAM_LL + cALM_PRESS_DEADBAND) THEN
    bAlm_PressSteam_LL := FALSE;
END_IF;

IF rVec_Y_Meas[1] <= cALM_PRESS_STEAM_L THEN
    bAlm_PressSteam_L := TRUE;
ELSIF rVec_Y_Meas[1] >= (cALM_PRESS_STEAM_L + cALM_PRESS_DEADBAND) THEN
    bAlm_PressSteam_L := FALSE;
END_IF;

(* 3. BRIDGE CATENARY SAG ALARM EVALUATION *)
IF rAct_BridgeSagVoted_mm >= cALM_SAG_BRIDGE_HH THEN
    bAlm_SagBridge_HH := TRUE;
ELSIF rAct_BridgeSagVoted_mm <= (cALM_SAG_BRIDGE_HH - cALM_SAG_DEADBAND) THEN
    bAlm_SagBridge_HH := FALSE;
END_IF;

IF rAct_BridgeSagVoted_mm >= cALM_SAG_BRIDGE_H THEN
    bAlm_SagBridge_H := TRUE;
    rTimer_AlmEscalate_SagH := rTimer_AlmEscalate_SagH + rT_CycleTime_Sec;
    IF rTimer_AlmEscalate_SagH >= cTIME_ALARM_ESCALATION_SEC THEN
        bAlm_SagBridge_HH := TRUE;
    END_IF;
ELSIF rAct_BridgeSagVoted_mm <= (cALM_SAG_BRIDGE_H - cALM_SAG_DEADBAND) THEN
    bAlm_SagBridge_H := FALSE;
    rTimer_AlmEscalate_SagH := 0.0;
END_IF;

IF rAct_BridgeSagVoted_mm <= cALM_SAG_BRIDGE_LL THEN
    bAlm_SagBridge_LL := TRUE;
ELSIF rAct_BridgeSagVoted_mm >= (cALM_SAG_BRIDGE_LL + cALM_SAG_DEADBAND) THEN
    bAlm_SagBridge_LL := FALSE;
END_IF;

IF rAct_BridgeSagVoted_mm <= cALM_SAG_BRIDGE_L THEN
    bAlm_SagBridge_L := TRUE;
ELSIF rAct_BridgeSagVoted_mm >= (cALM_SAG_BRIDGE_L + cALM_SAG_DEADBAND) THEN
    bAlm_SagBridge_L := FALSE;
END_IF;

(* 4. WEB TENSION ALARM EVALUATION *)
IF rAct_WebTensionEntryDB_N >= cALM_TENSION_DB_HH THEN
    bAlm_TensionDB_HH := TRUE;
ELSIF rAct_WebTensionEntryDB_N <= (cALM_TENSION_DB_HH - cALM_TENSION_DEADBAND) THEN
    bAlm_TensionDB_HH := FALSE;
END_IF;

IF rAct_WebTensionEntryDB_N >= cALM_TENSION_DB_H THEN
    bAlm_TensionDB_H := TRUE;
    rTimer_AlmEscalate_TensionH := rTimer_AlmEscalate_TensionH + rT_CycleTime_Sec;
    IF rTimer_AlmEscalate_TensionH >= cTIME_ALARM_ESCALATION_SEC THEN
        bAlm_TensionDB_HH := TRUE;
    END_IF;
ELSIF rAct_WebTensionEntryDB_N <= (cALM_TENSION_DB_H - cALM_TENSION_DEADBAND) THEN
    bAlm_TensionDB_H := FALSE;
    rTimer_AlmEscalate_TensionH := 0.0;
END_IF;

IF rAct_WebTensionEntryDB_N <= cALM_TENSION_DB_LL THEN
    bAlm_TensionDB_LL := TRUE;
ELSIF rAct_WebTensionEntryDB_N >= (cALM_TENSION_DB_LL + cALM_TENSION_DEADBAND) THEN
    bAlm_TensionDB_LL := FALSE;
END_IF;

IF rAct_WebTensionEntryDB_N <= cALM_TENSION_DB_L THEN
    bAlm_TensionDB_L := TRUE;
ELSIF rAct_WebTensionEntryDB_N >= (cALM_TENSION_DB_L + cALM_TENSION_DEADBAND) THEN
    bAlm_TensionDB_L := FALSE;
END_IF;

(* 5. SHEET CUTOFF ERROR & WEB WRAP-UP ALARM EVALUATION *)
IF ABS(rErr_SheetLengthCutoff_mm) >= cALM_CUT_ERR_HH THEN
    bAlm_CutErr_HH := TRUE;
ELSIF ABS(rErr_SheetLengthCutoff_mm) <= (cALM_CUT_ERR_HH - 0.5) THEN
    bAlm_CutErr_HH := FALSE;
END_IF;

IF ABS(rErr_SheetLengthCutoff_mm) >= cALM_CUT_ERR_H THEN
    bAlm_CutErr_H := TRUE;
ELSIF ABS(rErr_SheetLengthCutoff_mm) <= (cALM_CUT_ERR_H - 0.1) THEN
    bAlm_CutErr_H := FALSE;
END_IF;

(* Web wrap-up jam fast detector: Sudden speed drop while drive energized *)
IF (rCmd_SingleFacerDrive_Speed > 50.0) AND (rAct_LineSpeedMaster_m_min < 10.0) AND
   (eCorrugatorState = cSTATE_07_CONTINUOUS_HIGH_SPEED) THEN
    bAlm_WebWrapUpJam_HH := TRUE;
    bCmd_WebWrapUpDetectorTripped := TRUE;
ELSE
    bCmd_WebWrapUpDetectorTripped := FALSE;
END_IF;

(* Reset alarms upon operator command *)
IF bFaultReset_Cmd THEN
    bAlm_WebWrapUpJam_HH := FALSE;
    rTimer_AlmEscalate_TempH := 0.0;
    rTimer_AlmEscalate_PressH := 0.0;
    rTimer_AlmEscalate_SagH := 0.0;
    rTimer_AlmEscalate_TensionH := 0.0;
END_IF;

(* 6. STATUS WORD PACKING *)
(* dwStatusWord_State *)
dwStatusWord_State := INT_TO_DWORD(eCorrugatorState);
IF bMpcEnable_Cmd THEN dwStatusWord_State := dwStatusWord_State OR DWORD#16#00010000; END_IF;
IF bAutoSpeedTrack_Enable THEN dwStatusWord_State := dwStatusWord_State OR DWORD#16#00020000; END_IF;
IF bKnifeInSyncCutZone THEN dwStatusWord_State := dwStatusWord_State OR DWORD#16#00040000; END_IF;
IF bSlitterIndexBusy THEN dwStatusWord_State := dwStatusWord_State OR DWORD#16#00080000; END_IF;

(* dwStatusWord_Alarms_Critical *)
dwStatusWord_Alarms_Critical := DWORD#16#00000000;
IF bAlm_TempRoll_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000001; END_IF;
IF bAlm_TempRoll_LL THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000002; END_IF;
IF bAlm_PressSteam_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000004; END_IF;
IF bAlm_PressSteam_LL THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000008; END_IF;
IF bAlm_SagBridge_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000010; END_IF;
IF bAlm_SagBridge_LL THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000020; END_IF;
IF bAlm_TensionDB_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000040; END_IF;
IF bAlm_TensionDB_LL THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000080; END_IF;
IF bAlm_CutErr_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000100; END_IF;
IF bAlm_WebWrapUpJam_HH THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000200; END_IF;
IF bEmergencyStop_Trip THEN dwStatusWord_Alarms_Critical := dwStatusWord_Alarms_Critical OR DWORD#16#00000400; END_IF;

(* dwStatusWord_Alarms_Warning *)
dwStatusWord_Alarms_Warning := DWORD#16#00000000;
IF bAlm_TempRoll_H THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000001; END_IF;
IF bAlm_TempRoll_L THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000002; END_IF;
IF bAlm_PressSteam_H THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000004; END_IF;
IF bAlm_PressSteam_L THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000008; END_IF;
IF bAlm_SagBridge_H THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000010; END_IF;
IF bAlm_SagBridge_L THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000020; END_IF;
IF bAlm_TensionDB_H THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000040; END_IF;
IF bAlm_TensionDB_L THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000080; END_IF;
IF bAlm_CutErr_H THEN dwStatusWord_Alarms_Warning := dwStatusWord_Alarms_Warning OR DWORD#16#00000100; END_IF;

END_FUNCTION_BLOCK
'''

if __name__ == '__main__':
    p3 = get_part3()
    print("Part 3 length:", len(p3))
