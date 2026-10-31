# part4_mpc.py
mpc_text = """(* ==========================================================================================================
   PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZATION
   ========================================================================================================== *)
(* 3.1: Reference Trajectory Real-Time Synchronization *)
IF rSet_ReactorPressure_bar >= 2000.0 AND rSet_ReactorPressure_bar <= 3250.0 THEN
    xState_Ref[5] := rSet_ReactorPressure_bar;
    xState_Ref[6] := rSet_ReactorPressure_bar - 55.0;  (* Frictional differential drop to Mid *)
    xState_Ref[7] := rSet_ReactorPressure_bar - 125.0; (* Differential drop to Let-Down Valve *)
END_IF;

IF rSet_PeakTemp_Z1_degC >= 160.0 AND rSet_PeakTemp_Z1_degC <= 315.0 THEN
    xState_Ref[1] := rSet_PeakTemp_Z1_degC;
END_IF;
IF rSet_PeakTemp_Z2_degC >= 160.0 AND rSet_PeakTemp_Z2_degC <= 315.0 THEN
    xState_Ref[2] := rSet_PeakTemp_Z2_degC;
END_IF;
IF rSet_PeakTemp_Z3_degC >= 160.0 AND rSet_PeakTemp_Z3_degC <= 315.0 THEN
    xState_Ref[3] := rSet_PeakTemp_Z3_degC;
END_IF;
IF rSet_PeakTemp_Z4_degC >= 160.0 AND rSet_PeakTemp_Z4_degC <= 315.0 THEN
    xState_Ref[4] := rSet_PeakTemp_Z4_degC;
END_IF;

(* 3.2: Error Vector Evaluation *)
FOR idx_i := 1 TO 16 DO
    xState_Err[idx_i] := xState_Pred[idx_i] - xState_Ref[idx_i];
END_FOR;

(* Adaptive Tuning: Scale Q-weights if peak temp approaches runaway boundary *)
IF bAutoTuningEnable THEN
    IF xState_Pred[1] > 300.0 THEN
        qWeight_Q[1] := 350.0;
    ELSE
        qWeight_Q[1] := 180.0;
    END_IF;
    IF xState_Pred[2] > 305.0 THEN
        qWeight_Q[2] := 450.0;
    ELSE
        qWeight_Q[2] := 220.0;
    END_IF;
    IF xState_Pred[5] > 3050.0 THEN
        qWeight_Q[5] := 600.0;
    ELSE
        qWeight_Q[5] := 350.0;
    END_IF;
END_IF;

(* 3.3: Initialize Optimal Control Vector with Current Manipulated Variables *)
FOR idx_j := 1 TO 8 DO
    uControl_Opt[idx_j] := uControl_Curr[idx_j];
END_FOR;

(* 3.4: Constrained Projected Gradient Quadratic Programming Solver *)
FOR iMPC_Iter := 1 TO 3 DO
    (* Compute Analytic Gradient: grad_J = B^T * Q * e + R * (u - u_prev) *)
    FOR idx_j := 1 TO 8 DO
        rAccum := 0.0;
        FOR idx_i := 1 TO 16 DO
            rAccum := rAccum + (bInput_B[idx_i, idx_j] * qWeight_Q[idx_i] * xState_Err[idx_i]);
        END_FOR;
        uControl_Delta[idx_j] := uControl_Opt[idx_j] - uControl_Prev[idx_j];
        mpcGrad[idx_j] := rAccum + (rWeight_R[idx_j] * uControl_Delta[idx_j]);

        (* Approximate Diagonal Hessian Element: H_jj = sum(B_ij^2 * Q_i) + R_j + epsilon *)
        rTempCalc := 0.0;
        FOR idx_i := 1 TO 16 DO
            rTempCalc := rTempCalc + (bInput_B[idx_i, idx_j] * bInput_B[idx_i, idx_j] * qWeight_Q[idx_i]);
        END_FOR;
        mpcHessDiag[idx_j] := rTempCalc + rWeight_R[idx_j] + 0.085;
    END_FOR;

    (* Apply Gradient Descent Step with Actuator Hard and Rate Constraints *)
    FOR idx_j := 1 TO 8 DO
        IF mpcHessDiag[idx_j] > 0.001 THEN
            rTempCalc := uControl_Opt[idx_j] - ((mpcGrad[idx_j] / mpcHessDiag[idx_j]) * rMPC_StepSize);
        ELSE
            rTempCalc := uControl_Opt[idx_j];
        END_IF;

        (* Box Constraint Projection: [uMin, uMax] *)
        IF rTempCalc < uMin_Limits[idx_j] THEN
            rTempCalc := uMin_Limits[idx_j];
        ELSIF rTempCalc > uMax_Limits[idx_j] THEN
            rTempCalc := uMax_Limits[idx_j];
        END_IF;

        (* Slew Rate Clamping: [-deltaU_max, +deltaU_max] *)
        IF (rTempCalc - uControl_Prev[idx_j]) > deltaU_Limits[idx_j] THEN
            rTempCalc := uControl_Prev[idx_j] + deltaU_Limits[idx_j];
        ELSIF (rTempCalc - uControl_Prev[idx_j]) < -deltaU_Limits[idx_j] THEN
            rTempCalc := uControl_Prev[idx_j] - deltaU_Limits[idx_j];
        END_IF;

        uControl_Opt[idx_j] := rTempCalc;
    END_FOR;
END_FOR;

(* Store previous actuator vector for rate penalty evaluation on next scan *)
FOR idx_j := 1 TO 8 DO
    uControl_Prev[idx_j] := uControl_Curr[idx_j];
END_FOR;
"""

