# Phase 3: Discrete 8x8 State-Space & Receding-Horizon MPC for FB_Mining_SAG_BallMill_GrindingCircuit

def get_phase3():
    return """(* === PHASE 3: DISCRETE 8x8 STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC === *)

(* 3.1 Map Reconstructed Plant Telemetry into Discrete State Vector x[1..8] *)
aState_x[1] := rEstimatedChargeWeight_tons;
aState_x[2] := rEstimatedSlurryVolume_m3;
aState_x[3] := rEstimatedToeAngle_deg;
aState_x[4] := rVoted_MotorPower_MW;
aState_x[5] := rVoted_SumpLevel_pct;
aState_x[6] := rVoted_ProductDensity_SG;
aState_x[7] := rCirculatingLoadRatio_pct;
aState_x[8] := rEstimatedP80_microns;

(* Map Actuator Outputs into Control Vector u[1..8] *)
aControl_u[1] := (WT_FEEDER_1_ORE_TONS_HR_114 + WT_FEEDER_2_ORE_TONS_HR_115);
aControl_u[2] := rSagFeedWaterFlowSp_m3h;
aControl_u[3] := rSagMotorSpeedRef_rpm;
aControl_u[4] := rPebbleCrusherFeedSp_tph;
aControl_u[5] := rCyclonePumpSpeedRef_pct;
aControl_u[6] := rSumpDilutionValveCmd_pct;
aControl_u[7] := INT_TO_REAL(iActiveCycloneValvesCount);
aControl_u[8] := rBallMill1FeedSp_tph;

(* Calculate Actuator Slew Rate Vector Delta_u[1..8] *)
FOR iLoopCol := 1 TO 8 DO
    aDelta_u[iLoopCol] := aControl_u[iLoopCol] - aControl_u_prev[iLoopCol];
    aControl_u_prev[iLoopCol] := aControl_u[iLoopCol];
END_FOR;

(* 3.2 Discrete State-Space Propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR iLoopRow := 1 TO 8 DO
    rScratchSum := 0.0;
    (* State transition matrix multiplication A * x *)
    FOR iLoopCol := 1 TO 8 DO
        rScratchSum := rScratchSum + (aMatrix_A[iLoopRow, iLoopCol] * (aState_x[iLoopCol] - aState_x_ref[iLoopCol]));
    END_FOR;

    (* Actuator input gain matrix multiplication B * u *)
    FOR iLoopCol := 1 TO 8 DO
        rScratchSum := rScratchSum + (aMatrix_B[iLoopRow, iLoopCol] * aDelta_u[iLoopCol]);
    END_FOR;

    aState_x_next[iLoopRow] := aState_x_ref[iLoopRow] + rScratchSum;
END_FOR;

(* Output Measurement Mapping: y[k] = C * x[k] + D * u[k] *)
FOR iLoopRow := 1 TO 8 DO
    rScratchSum := 0.0;
    FOR iLoopCol := 1 TO 8 DO
        rScratchSum := rScratchSum + (aMatrix_C[iLoopRow, iLoopCol] * aState_x[iLoopCol]) +
                                     (aMatrix_D[iLoopRow, iLoopCol] * aControl_u[iLoopCol]);
    END_FOR;
    aOutput_y[iLoopRow] := rScratchSum;
END_FOR;

(* 3.3 Receding-Horizon Model Predictive Control (MPC) Solver *)
(* Initialize MPC candidate controls over control horizon Nu = 3 *)
FOR iMpcStep := 1 TO c_iMpcControlHorizon_Nu DO
    FOR iLoopCol := 1 TO 8 DO
        aMpc_U_cand[iMpcStep, iLoopCol] := aControl_u[iLoopCol];
    END_FOR;
END_FOR;

(* Projected Gradient Descent Iteration Loop *)
iMpcIterationsCount := 0;
bMpcSolutionFeasible := TRUE;
rScratchCost := 0.0;

FOR iMpcIter := 1 TO c_iMpcMaxIterations DO
    iMpcIterationsCount := iMpcIterationsCount + 1;

    (* Forward state prediction rollout over prediction horizon Np = 5 *)
    FOR iLoopCol := 1 TO 8 DO
        aMpc_X_pred[1, iLoopCol] := aState_x[iLoopCol];
    END_FOR;

    FOR iMpcStep := 1 TO (c_iMpcPredictionHorizon_Np - 1) DO
        FOR iLoopRow := 1 TO 8 DO
            rScratchSum := 0.0;
            FOR iLoopCol := 1 TO 8 DO
                rScratchSum := rScratchSum + (aMatrix_A[iLoopRow, iLoopCol] * (aMpc_X_pred[iMpcStep, iLoopCol] - aState_x_ref[iLoopCol]));
            END_FOR;

            (* Apply candidate control if within control horizon Nu, else hold last control *)
            IF iMpcStep <= c_iMpcControlHorizon_Nu THEN
                FOR iLoopCol := 1 TO 8 DO
                    rScratchSum := rScratchSum + (aMatrix_B[iLoopRow, iLoopCol] * (aMpc_U_cand[iMpcStep, iLoopCol] - aControl_u_prev[iLoopCol]));
                END_FOR;
            ELSE
                FOR iLoopCol := 1 TO 8 DO
                    rScratchSum := rScratchSum + (aMatrix_B[iLoopRow, iLoopCol] * (aMpc_U_cand[c_iMpcControlHorizon_Nu, iLoopCol] - aControl_u_prev[iLoopCol]));
                END_FOR;
            END_IF;

            aMpc_X_pred[iMpcStep + 1, iLoopRow] := aState_x_ref[iLoopRow] + rScratchSum;
        END_FOR;
    END_FOR;

    (* Compute Quadratic Objective Cost J: Stage Costs + Slew Costs + Terminal Costs *)
    rScratchCost := 0.0;

    (* Stage Costs: sum_{k=1..Np} (x_k - x_ref)^T * Q * (x_k - x_ref) *)
    FOR iMpcStep := 1 TO c_iMpcPredictionHorizon_Np DO
        FOR iLoopCol := 1 TO 8 DO
            rScratchTerm := aMpc_X_pred[iMpcStep, iLoopCol] - aState_x_ref[iLoopCol];
            rScratchCost := rScratchCost + (rScratchTerm * rScratchTerm * aWeights_Q[iLoopCol]);

            (* Direct Shell Liner Impact Nonlinear Penalty *)
            IF iLoopCol = 3 AND aMpc_X_pred[iMpcStep, 3] < 38.0 THEN
                (* Severe penalty for toe angle receding below 38 degrees (bare liner impact) *)
                rScratchCost := rScratchCost + (EXPT((38.0 - aMpc_X_pred[iMpcStep, 3]), 2.0) * 85.0);
            END_IF;
        END_FOR;
    END_FOR;

    (* Actuator Slew Rate Penalty: sum_{k=1..Nu} Delta_u_k^T * R * Delta_u_k *)
    FOR iMpcStep := 1 TO c_iMpcControlHorizon_Nu DO
        FOR iLoopCol := 1 TO 8 DO
            IF iMpcStep = 1 THEN
                rScratchTerm := aMpc_U_cand[1, iLoopCol] - aControl_u_prev[iLoopCol];
            ELSE
                rScratchTerm := aMpc_U_cand[iMpcStep, iLoopCol] - aMpc_U_cand[iMpcStep - 1, iLoopCol];
            END_IF;
            rScratchCost := rScratchCost + (rScratchTerm * rScratchTerm * aWeights_R[iLoopCol]);
        END_FOR;
    END_FOR;

    (* Terminal State Penalty: (x_Np - x_ref)^T * P * (x_Np - x_ref) *)
    FOR iLoopCol := 1 TO 8 DO
        rScratchTerm := aMpc_X_pred[c_iMpcPredictionHorizon_Np, iLoopCol] - aState_x_ref[iLoopCol];
        rScratchCost := rScratchCost + (rScratchTerm * rScratchTerm * aWeights_P[iLoopCol]);
    END_FOR;

    (* Compute Numerical Gradient with respect to first control step u_cand[1] *)
    FOR iLoopCol := 1 TO 8 DO
        rScratchGrad := 2.0 * aWeights_R[iLoopCol] * (aMpc_U_cand[1, iLoopCol] - aControl_u_prev[iLoopCol]);
        FOR iLoopRow := 1 TO 8 DO
            rScratchGrad := rScratchGrad +
                            (2.0 * aWeights_Q[iLoopRow] * (aMpc_X_pred[2, iLoopRow] - aState_x_ref[iLoopRow]) * aMatrix_B[iLoopRow, iLoopCol]);
        END_FOR;
        aMpc_Grad_u[iLoopCol] := rScratchGrad;

        (* Projected Gradient Descent Step with Adaptive Damping (alpha = 0.005) *)
        aMpc_U_cand[1, iLoopCol] := aMpc_U_cand[1, iLoopCol] - (0.005 * aMpc_Grad_u[iLoopCol]);

        (* Slew Rate Clamping *)
        IF (aMpc_U_cand[1, iLoopCol] - aControl_u_prev[iLoopCol]) > aMaxSlewRate_u[iLoopCol] THEN
            aMpc_U_cand[1, iLoopCol] := aControl_u_prev[iLoopCol] + aMaxSlewRate_u[iLoopCol];
        ELSIF (aMpc_U_cand[1, iLoopCol] - aControl_u_prev[iLoopCol]) < -aMaxSlewRate_u[iLoopCol] THEN
            aMpc_U_cand[1, iLoopCol] := aControl_u_prev[iLoopCol] - aMaxSlewRate_u[iLoopCol];
        END_IF;

        (* Physical Lower and Upper Actuator Bounding *)
        IF aMpc_U_cand[1, iLoopCol] < aMin_u[iLoopCol] THEN
            aMpc_U_cand[1, iLoopCol] := aMin_u[iLoopCol];
            bMpcSolutionFeasible := FALSE;
        ELSIF aMpc_U_cand[1, iLoopCol] > aMax_u[iLoopCol] THEN
            aMpc_U_cand[1, iLoopCol] := aMax_u[iLoopCol];
            bMpcSolutionFeasible := FALSE;
        END_IF;
    END_FOR;
END_FOR;

rMpcOptimizationCost := rScratchCost;
"""
