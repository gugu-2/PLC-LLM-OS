# Generator part 7: State-Space Propagation and MPC Optimization
def get_ss_mpc_logic():
    return """(* ============================================================================================= *)
(* SECTION 3: 8x8 DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER INNOVATION                  *)
(* ============================================================================================= *)

(* 3.1 Map Actual Process Telemetry into Output Vector y[0..7] *)
aOutput_y[0] := rVoted_TotalMillWeight_tons - 1320.5;
aOutput_y[1] := rEstimated_SlurryHoldUp_m3 - 245.0;
aOutput_y[2] := rEstimated_ToeAngle_deg - 135.0;
aOutput_y[3] := rCalculated_LinerImpactIndex - 25.0;
aOutput_y[4] := rVoted_SumpLevel_Pct - 58.5;
aOutput_y[5] := (rVoted_SlurryDensity_SG - 1.540) * 100.0;
aOutput_y[6] := rVoted_ManifoldPress_kPa - 92.5;
aOutput_y[7] := rVoted_RingMotorPower_MW - 23.45;

(* 3.2 Map Manipulated Variable Deviations into Vector u[0..5] *)
aControl_u[0] := rSAG_FreshFeedRateCmd_tph - 2850.0;
aControl_u[1] := rMillInletWaterFlowCmd_m3h - 850.0;
aControl_u[2] := rRingMotorSpeedCmd_RPM - 9.15;
aControl_u[3] := rCyclonePumpSpeedCmd_RPM - 520.0;
aControl_u[4] := rCycloneSumpWaterValveCmd_Pct - 38.0;
aControl_u[5] := INT_TO_REAL(iActiveCyclonesTargetCount) - 9.0;

(* 3.3 Map Process Disturbance Deviations into Vector d[0..2] *)
aDisturb_d[0] := (rAustin_SpecificBreakage_S0 - 0.485) * 10.0;
aDisturb_d[1] := WT_PEBBLE_RECYCLE_CONVEYOR_102A - 280.0;
aDisturb_d[2] := (AT_CYCLONE_OVERFLOW_P80_506 - 150.0) * 0.10;

(* 3.4 Discrete State Prediction: x_pred = A * x_hat + B * u + E * d *)
FOR iIdx := 0 TO 7 DO
    rTmpSum := 0.0;
    (* State transition contribution *)
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + (aMatrix_A[iIdx, jIdx] * aState_x_hat[jIdx]);
    END_FOR;
    (* Control input contribution *)
    FOR jIdx := 0 TO 5 DO
        rTmpSum := rTmpSum + (aMatrix_B[iIdx, jIdx] * aControl_u[jIdx]);
    END_FOR;
    (* Disturbance contribution *)
    FOR jIdx := 0 TO 2 DO
        rTmpSum := rTmpSum + (aMatrix_E[iIdx, jIdx] * aDisturb_d[jIdx]);
    END_FOR;
    aState_x_pred[iIdx] := rTmpSum;
END_FOR;

(* 3.5 Kalman Observer Correction: x_hat = x_pred + K_obs * (y - C * x_pred) *)
FOR iIdx := 0 TO 7 DO
    (* Output prediction y_hat = C * x_pred *)
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + (aMatrix_C[iIdx, jIdx] * aState_x_pred[jIdx]);
    END_FOR;
    aOutput_y_error[iIdx] := aOutput_y[iIdx] - rTmpSum;
END_FOR;

FOR iIdx := 0 TO 7 DO
    rTmpSum := 0.0;
    FOR jIdx := 0 TO 7 DO
        rTmpSum := rTmpSum + (aMatrix_K_obs[iIdx, jIdx] * aOutput_y_error[jIdx]);
    END_FOR;
    aState_x_hat[iIdx] := aState_x_pred[iIdx] + rTmpSum;
    aState_x[iIdx] := aState_x_hat[iIdx];
END_FOR;

(* ============================================================================================= *)
(* SECTION 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QUADRATIC OPTIMIZATION            *)
(* ============================================================================================= *)
IF bMPC_Permissive AND (iMachineState = 50) THEN
    bMPC_ControllerActive := TRUE;

    (* Initialize control changes du from previous cycle *)
    FOR jIdx := 0 TO 5 DO
        aControl_du[jIdx] := aControl_u[jIdx] - aControl_u_prev[jIdx];
    END_FOR;

    (* Active-Set Projected Gradient Descent Optimization Loop *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        (* Compute gradient vector g = 2 * B^T * Q * (x_hat - x_sp) + 2 * R * u + 2 * S * du *)
        FOR jIdx := 0 TO 5 DO
            rTmpSum := 0.0;
            FOR iIdx := 0 TO 7 DO
                rTmpSum := rTmpSum + (aMatrix_B[iIdx, jIdx] * aWeight_Q[iIdx] * (aState_x_hat[iIdx] - aOutput_y_sp[iIdx]));
            END_FOR;
            rTmpSum := (2.0 * rTmpSum) + (2.0 * aWeight_R[jIdx] * aControl_u[jIdx]) + (2.0 * aWeight_S[jIdx] * aControl_du[jIdx]);

            (* Dynamic Shell Liner Impact Mitigation Penalty Injection *)
            (* If acoustic direct impact index > 45%, heavily bias speed reduction and feed boost *)
            IF (jIdx = 2) AND (rCalculated_LinerImpactIndex > 45.0) THEN
                (* Squeeze ring motor speed down aggressively *)
                rTmpSum := rTmpSum + (18.5 * (rCalculated_LinerImpactIndex - 45.0));
            END_IF;
            IF (jIdx = 0) AND (rCalculated_LinerImpactIndex > 45.0) THEN
                (* Bias feed conveyor up to create cushioning toe bed *)
                rTmpSum := rTmpSum - (12.0 * (rCalculated_LinerImpactIndex - 45.0));
            END_IF;

            aGrad_g[jIdx] := rTmpSum;
        END_FOR;

        (* Projected Step along negative gradient *)
        FOR jIdx := 0 TO 5 DO
            aStep_du[jIdx] := aControl_du[jIdx] - (rAlphaStep * aGrad_g[jIdx]);

            (* Enforce Slew Rate Dynamic Constraints *)
            IF aStep_du[jIdx] > aLimit_du_Max[jIdx] THEN
                aStep_du[jIdx] := aLimit_du_Max[jIdx];
            ELSIF aStep_du[jIdx] < aLimit_du_Min[jIdx] THEN
                aStep_du[jIdx] := aLimit_du_Min[jIdx];
            END_IF;

            (* Update control action candidate *)
            aControl_u[jIdx] := aControl_u_prev[jIdx] + aStep_du[jIdx];

            (* Enforce Physical Actuator Saturation Constraints *)
            IF (aControl_u_base[jIdx] + aControl_u[jIdx]) > aLimit_u_Max[jIdx] THEN
                aControl_u[jIdx] := aLimit_u_Max[jIdx] - aControl_u_base[jIdx];
            ELSIF (aControl_u_base[jIdx] + aControl_u[jIdx]) < aLimit_u_Min[jIdx] THEN
                aControl_u[jIdx] := aLimit_u_Min[jIdx] - aControl_u_base[jIdx];
            END_IF;

            aControl_du[jIdx] := aStep_du[jIdx];
        END_FOR;
    END_FOR;

    (* Apply Optimized MPC Actuator Demands *)
    rSAG_FreshFeedRateCmd_tph     := aControl_u_base[0] + aControl_u[0];
    rMillInletWaterFlowCmd_m3h    := aControl_u_base[1] + aControl_u[1];
    rRingMotorSpeedCmd_RPM        := aControl_u_base[2] + aControl_u[2];
    rCyclonePumpSpeedCmd_RPM      := aControl_u_base[3] + aControl_u[3];
    rCycloneSumpWaterValveCmd_Pct := aControl_u_base[4] + aControl_u[4];
    iActiveCyclonesTargetCount    := REAL_TO_INT(aControl_u_base[5] + aControl_u[5]);

    (* Save control memory *)
    FOR jIdx := 0 TO 5 DO
        aControl_u_prev[jIdx] := aControl_u[jIdx];
    END_FOR;
ELSE
    bMPC_ControllerActive := FALSE;
END_IF;
"""

print("SS and MPC module loaded.")
