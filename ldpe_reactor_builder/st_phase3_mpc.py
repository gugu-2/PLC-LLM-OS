# ldpe_reactor_builder/st_phase3_mpc.py

def get_phase3_mpc():
    return """(* ============================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH UNROLLED PGD OPTIMIZATION        *)
(* 10 EXPLICIT UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)                            *)
(* CONTROL HORIZON Nc = 4, PREDICTION HORIZON Np = 10, CONTROL INPUTS Nu = 4, STATES Nx = 6       *)
(* BALANCING:                                                                                     *)
(*   u1: HYPER-COMPRESSOR THROUGHPUT TRIM [%]                                                     *)
(*   u2: ORGANIC PEROXIDE INJECTION PUMP MASTER STROKE TRIM [%]                                   *)
(*   u3: HIGH-PRESSURE LETDOWN VALVE (HPLDV) BASELINE POSITION TRIM [%]                           *)
(*   u4: PRESSURIZED JACKET WATER CIRCULATION COOLING THROTTLE VALVES [%]                         *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.1: MPC WEIGHT MATRICES INITIALIZATION (Q, R, P_term, S_slew)                            *)
(* ---------------------------------------------------------------------------------------------- *)
(* State Tracking Cost Matrix Q (6x6 Diagonal) *)
matQ[1, 1] := 14.5; matQ[1, 2] := 0.0;   matQ[1, 3] := 0.0;  matQ[1, 4] := 0.0;  matQ[1, 5] := 0.0;  matQ[1, 6] := 0.0;
matQ[2, 1] := 0.0;  matQ[2, 2] := 0.095; matQ[2, 3] := 0.0;  matQ[2, 4] := 0.0;  matQ[2, 5] := 0.0;  matQ[2, 6] := 0.0;
matQ[3, 1] := 0.0;  matQ[3, 2] := 0.0;   matQ[3, 3] := 4.85; matQ[3, 4] := 0.0;  matQ[3, 5] := 0.0;  matQ[3, 6] := 0.0;
matQ[4, 1] := 0.0;  matQ[4, 2] := 0.0;   matQ[4, 3] := 0.0;  matQ[4, 4] := 1.25; matQ[4, 5] := 0.0;  matQ[4, 6] := 0.0;
matQ[5, 1] := 0.0;  matQ[5, 2] := 0.0;   matQ[5, 3] := 0.0;  matQ[5, 4] := 0.0;  matQ[5, 5] := 22.0; matQ[5, 6] := 0.0;
matQ[6, 1] := 0.0;  matQ[6, 2] := 0.0;   matQ[6, 3] := 0.0;  matQ[6, 4] := 0.0;  matQ[6, 5] := 0.0;  matQ[6, 6] := 28.5;

(* Actuator Penalty Matrix R (4x4 Diagonal) *)
matR[1, 1] := 2.25; matR[1, 2] := 0.0;  matR[1, 3] := 0.0;  matR[1, 4] := 0.0;
matR[2, 1] := 0.0;  matR[2, 2] := 2.85; matR[2, 3] := 0.0;  matR[2, 4] := 0.0;
matR[3, 1] := 0.0;  matR[3, 2] := 0.0;  matR[3, 3] := 1.75; matR[3, 4] := 0.0;
matR[4, 1] := 0.0;  matR[4, 2] := 0.0;  matR[4, 3] := 0.0;  matR[4, 4] := 1.15;

(* Terminal State Penalty Matrix P_term = 1.65 * Q *)
FOR idx_i := 1 TO 6 DO
    FOR idx_j := 1 TO 6 DO
        matP_Term[idx_i, idx_j] := matQ[idx_i, idx_j] * 1.65;
    END_FOR;
END_FOR;

(* Actuator Slew Rate Penalty Matrix S_slew (4x4 Diagonal) *)
matS_Slew[1, 1] := 9.50; matS_Slew[1, 2] := 0.0;  matS_Slew[1, 3] := 0.0;  matS_Slew[1, 4] := 0.0;
matS_Slew[2, 1] := 0.0;  matS_Slew[2, 2] := 6.20; matS_Slew[2, 3] := 0.0;  matS_Slew[2, 4] := 0.0;
matS_Slew[3, 1] := 0.0;  matS_Slew[3, 2] := 0.0;  matS_Slew[3, 3] := 4.50; matS_Slew[3, 4] := 0.0;
matS_Slew[4, 1] := 0.0;  matS_Slew[4, 2] := 0.0;  matS_Slew[4, 3] := 0.0;  matS_Slew[4, 4] := 2.80;

(* Set Target Reference Vector x_ref *)
vecX_Ref[iState_Tpeak]   := rRecipe_PeakTemp_Target_degC;
vecX_Ref[iState_Zpeak]   := rRecipe_PeakLocation_Target_m;
vecX_Ref[iState_Pinlet]  := rRecipe_TargetReactorPressure_bar;
vecX_Ref[iState_Poutlet] := rRecipe_TargetReactorPressure_bar - 180.0;
vecX_Ref[iState_Xconv]   := rRecipe_TargetConversion_pct;
vecX_Ref[iState_MFI]     := rRecipe_TargetMFI_g10min;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.2: WARM-START TRAJECTORY INITIALIZATION                                                 *)
(* Shift previous optimal plan forward by 1 time step and append last control                     *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idx_k := 1 TO 9 DO
    FOR idx_m := 1 TO 4 DO
        arrU_HorizonPlan[idx_k, idx_m] := arrU_HorizonPlan[idx_k + 1, idx_m];
    END_FOR;
END_FOR;
FOR idx_m := 1 TO 4 DO
    arrU_HorizonPlan[10, idx_m] := arrU_HorizonPlan[9, idx_m];
END_FOR;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.3: 10 UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)                           *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idx_k := 1 TO 10 DO

    (* --- SUB-STEP A: FORWARD PREDICTION OVER 10-STEP PREDICTION HORIZON --- *)
    (* Step 1 starts from current filtered state vecX_Est *)
    FOR idx_i := 1 TO 6 DO
        arrX_HorizonPred[1, idx_i] := 0.0;
        FOR idx_j := 1 TO 6 DO
            arrX_HorizonPred[1, idx_i] := arrX_HorizonPred[1, idx_i] + (matA[idx_i, idx_j] * vecX_Est[idx_j]);
        END_FOR;
        FOR idx_m := 1 TO 4 DO
            arrX_HorizonPred[1, idx_i] := arrX_HorizonPred[1, idx_i] + (matB[idx_i, idx_m] * arrU_HorizonPlan[1, idx_m]);
        END_FOR;
    END_FOR;

    (* Steps 2 to 10 propagate forward: x(n) = A * x(n-1) + B * u(n) *)
    FOR idx_i := 2 TO 10 DO
        FOR idx_j := 1 TO 6 DO
            arrX_HorizonPred[idx_i, idx_j] := 0.0;
            FOR idx_m := 1 TO 6 DO
                arrX_HorizonPred[idx_i, idx_j] := arrX_HorizonPred[idx_i, idx_j] + (matA[idx_j, idx_m] * arrX_HorizonPred[idx_i - 1, idx_m]);
            END_FOR;
            FOR idx_m := 1 TO 4 DO
                arrX_HorizonPred[idx_i, idx_j] := arrX_HorizonPred[idx_i, idx_j] + (matB[idx_j, idx_m] * arrU_HorizonPlan[idx_i, idx_m]);
            END_FOR;
        END_FOR;
    END_FOR;


    (* --- SUB-STEP B: BACKWARD ADJOINT COSTATE PROPAGATION FOR EXACT GRADIENT EVALUATION --- *)
    (* Terminal Costate at step 10: lambda(10) = P_term * (x(10) - x_ref) *)
    (* We reuse arrX_HorizonPred temporary registers to compute costate vectors *)
    (* Compute Analytical Gradients Grad_U(n) = R * u(n) + S * (u(n) - u(n-1)) + B^T * lambda(n+1) *)

    (* Gradient Evaluation for Step 10 *)
    FOR idx_m := 1 TO 4 DO
        rTempCalc1 := matR[idx_m, idx_m] * arrU_HorizonPlan[10, idx_m]; (* Actuator penalty *)
        rTempCalc2 := matS_Slew[idx_m, idx_m] * (arrU_HorizonPlan[10, idx_m] - arrU_HorizonPlan[9, idx_m]); (* Slew penalty *)
        rTempCalc3 := 0.0;
        FOR idx_j := 1 TO 6 DO
            (* Terminal state error weighted by P_term *)
            rTempCalc4 := matP_Term[idx_j, idx_j] * (arrX_HorizonPred[10, idx_j] - vecX_Ref[idx_j]);
            rTempCalc3 := rTempCalc3 + (matB[idx_j, idx_m] * rTempCalc4);
        END_FOR;
        arrGrad_U[10, idx_m] := rTempCalc1 + rTempCalc2 + rTempCalc3;
    END_FOR;

    (* Gradient Evaluation for Steps 9 Down to 2 *)
    FOR idx_i := 9 TO 2 BY -1 DO
        FOR idx_m := 1 TO 4 DO
            rTempCalc1 := matR[idx_m, idx_m] * arrU_HorizonPlan[idx_i, idx_m];
            rTempCalc2 := matS_Slew[idx_m, idx_m] * (arrU_HorizonPlan[idx_i, idx_m] - arrU_HorizonPlan[idx_i - 1, idx_m]);
            rTempCalc3 := 0.0;
            FOR idx_j := 1 TO 6 DO
                rTempCalc4 := matQ[idx_j, idx_j] * (arrX_HorizonPred[idx_i, idx_j] - vecX_Ref[idx_j]);
                rTempCalc3 := rTempCalc3 + (matB[idx_j, idx_m] * rTempCalc4);
            END_FOR;
            arrGrad_U[idx_i, idx_m] := rTempCalc1 + rTempCalc2 + rTempCalc3;
        END_FOR;
    END_FOR;

    (* Gradient Evaluation for Step 1 (Coupled to Previous Executed Control vecU_Prev) *)
    FOR idx_m := 1 TO 4 DO
        rTempCalc1 := matR[idx_m, idx_m] * arrU_HorizonPlan[1, idx_m];
        rTempCalc2 := matS_Slew[idx_m, idx_m] * (arrU_HorizonPlan[1, idx_m] - vecU_Prev[idx_m]);
        rTempCalc3 := 0.0;
        FOR idx_j := 1 TO 6 DO
            rTempCalc4 := matQ[idx_j, idx_j] * (arrX_HorizonPred[1, idx_j] - vecX_Ref[idx_j]);
            rTempCalc3 := rTempCalc3 + (matB[idx_j, idx_m] * rTempCalc4);
        END_FOR;
        arrGrad_U[1, idx_m] := rTempCalc1 + rTempCalc2 + rTempCalc3;
    END_FOR;


    (* --- SUB-STEP C: GRADIENT DESCENT STEP & PROJECTION ONTO FEASIBLE ACTUATION CONSTRAINTS --- *)
    FOR idx_i := 1 TO 10 DO
        FOR idx_m := 1 TO 4 DO
            (* Gradient Descent Update *)
            rTempCalc1 := arrU_HorizonPlan[idx_i, idx_m] - (rPGD_StepSizeAlpha * arrGrad_U[idx_i, idx_m]);

            (* Slew Rate Constraint Projection: |u(n) - u(n-1)| <= DeltaU_Max *)
            IF idx_i = 1 THEN
                rTempCalc2 := vecU_Prev[idx_m];
            ELSE
                rTempCalc2 := arrU_HorizonPlan[idx_i - 1, idx_m];
            END_IF;

            IF (rTempCalc1 - rTempCalc2) > vecDeltaU_Max[idx_m] THEN
                rTempCalc1 := rTempCalc2 + vecDeltaU_Max[idx_m];
            ELSIF (rTempCalc1 - rTempCalc2) < -vecDeltaU_Max[idx_m] THEN
                rTempCalc1 := rTempCalc2 - vecDeltaU_Max[idx_m];
            END_IF;

            (* Absolute Bound Projection: u_min <= u(n) <= u_max *)
            IF rTempCalc1 < vecU_Min[idx_m] THEN
                rTempCalc1 := vecU_Min[idx_m];
            ELSIF rTempCalc1 > vecU_Max[idx_m] THEN
                rTempCalc1 := vecU_Max[idx_m];
            END_IF;

            arrU_HorizonPlan[idx_i, idx_m] := rTempCalc1;
        END_FOR;
    END_FOR;

END_FOR; (* End of 10 PGD Iterations *)


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.4: RECEDING HORIZON ACTION ASSIGNMENT & MULTI-ZONE PEROXIDE METERING SPLIT              *)
(* Extract First Step Control Vector u_cmd = arrU_HorizonPlan[1]                                  *)
(* ---------------------------------------------------------------------------------------------- *)
vecU_Cmd[iInput_HyperCompTrim]   := arrU_HorizonPlan[1, iInput_HyperCompTrim];
vecU_Cmd[iInput_PeroxMasterTrim] := arrU_HorizonPlan[1, iInput_PeroxMasterTrim];
vecU_Cmd[iInput_HPLDVBaseTrim]   := arrU_HorizonPlan[1, iInput_HPLDVBaseTrim];
vecU_Cmd[iInput_JacketWaterTrim] := arrU_HorizonPlan[1, iInput_JacketWaterTrim];

(* Store for Next Scan Slew Reference *)
vecU_Prev[1] := vecU_Cmd[1];
vecU_Prev[2] := vecU_Cmd[2];
vecU_Prev[3] := vecU_Cmd[3];
vecU_Prev[4] := vecU_Cmd[4];

(* Assign Master MPC Actuator Output Trims *)
rCmd_HyperComp_SpeedTrim_pct        := vecU_Cmd[iInput_HyperCompTrim];
rCmd_HPLDV_Position_pct             := rHPLDV_PulseBaselineStroke_pct + vecU_Cmd[iInput_HPLDVBaseTrim];
rCmd_JacketWater_TemperingValve_pct := 50.0 + vecU_Cmd[iInput_JacketWaterTrim];
rCmd_JacketWater_BoosterPump_pct    := 75.0 - (vecU_Cmd[iInput_JacketWaterTrim] * 0.50);

(* Chain Transfer Agent (CTA) Modulating Pump Command *)
rTempCalc1 := 50.0 + (rRecipe_CTA_Concentration_ppm - 450.0) * 0.08 - (vecX_Est[iState_MFI] - rRecipe_TargetMFI_g10min) * 12.0;
IF rTempCalc1 < 10.0 THEN
    rTempCalc1 := 10.0;
ELSIF rTempCalc1 > 95.0 THEN
    rTempCalc1 := 95.0;
END_IF;
rCmd_CTA_DosingPump_pct := rTempCalc1;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 3.5: DYNAMIC MULTI-ZONE PEROXIDE INITIATOR SPLIT OPTIMIZATION                             *)
(* Distributes Master Peroxide Flow Trim to 4 High-Pressure Metering Diaphragm Pumps              *)
(* Based on Axial Reaction Peak Z_peak Location and Differential Zone Temperatures                 *)
(* ---------------------------------------------------------------------------------------------- *)
(* Master Peroxide Baseline Flow Rate: 100% nominal = 50.0 kg/h *)
rTempCalc1 := 50.0 * (1.0 + vecU_Cmd[iInput_PeroxMasterTrim] * 0.01);

(* Spatial Peak Shift Compensation: If peak moves forward (Z_peak > Target), boost Zone 1 & 2 *)
rTempCalc2 := (vecX_Est[iState_Zpeak] - rRecipe_PeakLocation_Target_m) * 0.0005;

(* Zone 1 Pump Command (Preheat / Ignition Section: 300 to 600 m) *)
rTempCalc3 := (rPeroxide_Zone1_Ratio + rTempCalc2) * rTempCalc1;
rCmd_PeroxidePump1_Stroke_pct := (rTempCalc3 / 15.0) * 100.0;
IF rCmd_PeroxidePump1_Stroke_pct < 0.0 THEN
    rCmd_PeroxidePump1_Stroke_pct := 0.0;
ELSIF rCmd_PeroxidePump1_Stroke_pct > 100.0 THEN
    rCmd_PeroxidePump1_Stroke_pct := 100.0;
END_IF;

(* Zone 2 Pump Command (Main Exotherm Section: 600 to 900 m) *)
rTempCalc3 := (rPeroxide_Zone2_Ratio + (rTempCalc2 * 0.5)) * rTempCalc1;
rCmd_PeroxidePump2_Stroke_pct := (rTempCalc3 / 25.0) * 100.0;
IF rCmd_PeroxidePump2_Stroke_pct < 0.0 THEN
    rCmd_PeroxidePump2_Stroke_pct := 0.0;
ELSIF rCmd_PeroxidePump2_Stroke_pct > 100.0 THEN
    rCmd_PeroxidePump2_Stroke_pct := 100.0;
END_IF;

(* Zone 3 Pump Command (Second Reaction Peak Section: 900 to 1,200 m) *)
rTempCalc3 := (rPeroxide_Zone3_Ratio - (rTempCalc2 * 0.75)) * rTempCalc1;
rCmd_PeroxidePump3_Stroke_pct := (rTempCalc3 / 18.0) * 100.0;
IF rCmd_PeroxidePump3_Stroke_pct < 0.0 THEN
    rCmd_PeroxidePump3_Stroke_pct := 0.0;
ELSIF rCmd_PeroxidePump3_Stroke_pct > 100.0 THEN
    rCmd_PeroxidePump3_Stroke_pct := 100.0;
END_IF;

(* Zone 4 Pump Command (Tail Polishing Section: 1,200 to 1,500 m) *)
rTempCalc3 := (rPeroxide_Zone4_Ratio - (rTempCalc2 * 0.75)) * rTempCalc1;
rCmd_PeroxidePump4_Stroke_pct := (rTempCalc3 / 12.0) * 100.0;
IF rCmd_PeroxidePump4_Stroke_pct < 0.0 THEN
    rCmd_PeroxidePump4_Stroke_pct := 0.0;
ELSIF rCmd_PeroxidePump4_Stroke_pct > 100.0 THEN
    rCmd_PeroxidePump4_Stroke_pct := 100.0;
END_IF;
"""
