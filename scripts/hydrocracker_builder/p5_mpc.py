# -*- coding: utf-8 -*-
"""
Part 5: Phase 5 (Receding-Horizon Model Predictive Control Quadratic Optimization)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_mpc_block():
    return """(* ==========================================================================================
 * PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QUADRATIC OPTIMIZATION
 * ========================================================================================== *)

(* Calculate Slew Delta Vector: du[k] = u[k] - u[k-1] *)
FOR iIdxK := 1 TO 6 DO
    u_delta[iIdxK] := u_ctrl[iIdxK] - u_prev[iIdxK];
END_FOR;

(* --- 5.1 MULTIVARIABLE QUADRATIC COST OPTIMIZATION (10 GRADIENT DESCENT ITERATIONS) --- *)
(* Objective: Minimize J(u) = e^T Q e + du^T R du + e_term^T P e_term *)
(* Subject to: 0.0 <= u[k] <= 100.0% and slew constraints |du[k]| <= du_max *)

FOR iMpcIter := 1 TO 10 DO
    (* 1. Compute Analytical Unconstrained Gradient Vector dJ/du (6x1) *)
    (* Gradient component 1: Cold Quench Injection 1 (Bed 1-2 Interbed Split) *)
    rMpcGradient[1] := (matR[1,1] * (u_ctrl[1] - u_prev[1])) +
                       (matB[1,1] * (matQ[1,1] * (x_state[1] - 395.0) + matP[1,1] * (x_pred[1] - 395.0))) +
                       (matB[2,1] * (matQ[2,2] * (x_state[2] - 405.0) + matP[2,2] * (x_pred[2] - 405.0))) +
                       (matB[5,1] * (matQ[5,5] * (x_state[5] - 12000.0) + matP[5,5] * (x_pred[5] - 12000.0))) +
                       (matB[6,1] * (matQ[6,6] * (x_state[6] - 4.50) + matP[6,6] * (x_pred[6] - 4.50)));

    (* Gradient component 2: Cold Quench Injection 2 (Bed 2-3 Interbed Split) *)
    rMpcGradient[2] := (matR[2,2] * (u_ctrl[2] - u_prev[2])) +
                       (matB[2,2] * (matQ[2,2] * (x_state[2] - 405.0) + matP[2,2] * (x_pred[2] - 405.0))) +
                       (matB[3,2] * (matQ[3,3] * (x_state[3] - 415.0) + matP[3,3] * (x_pred[3] - 415.0))) +
                       (matB[5,2] * (matQ[5,5] * (x_state[5] - 12000.0) + matP[5,5] * (x_pred[5] - 12000.0))) +
                       (matB[6,2] * (matQ[6,6] * (x_state[6] - 4.50) + matP[6,6] * (x_pred[6] - 4.50)));

    (* Gradient component 3: Cold Quench Injection 3 (Bed 3-4 Interbed Split) *)
    rMpcGradient[3] := (matR[3,3] * (u_ctrl[3] - u_prev[3])) +
                       (matB[3,3] * (matQ[3,3] * (x_state[3] - 415.0) + matP[3,3] * (x_pred[3] - 415.0))) +
                       (matB[4,3] * (matQ[4,4] * (x_state[4] - 420.0) + matP[4,4] * (x_pred[4] - 420.0))) +
                       (matB[5,3] * (matQ[5,5] * (x_state[5] - 12000.0) + matP[5,5] * (x_pred[5] - 12000.0))) +
                       (matB[6,3] * (matQ[6,6] * (x_state[6] - 4.50) + matP[6,6] * (x_pred[6] - 4.50)));

    (* Gradient component 4: Combined Feed Charge Heater Fuel Gas Duty *)
    rMpcGradient[4] := (matR[4,4] * (u_ctrl[4] - u_prev[4])) +
                       (matB[1,4] * (matQ[1,1] * (x_state[1] - 395.0) + matP[1,1] * (x_pred[1] - 395.0))) +
                       (matB[2,4] * (matQ[2,2] * (x_state[2] - 405.0) + matP[2,2] * (x_pred[2] - 405.0))) +
                       (matB[3,4] * (matQ[3,3] * (x_state[3] - 415.0) + matP[3,3] * (x_pred[3] - 415.0))) +
                       (matB[4,4] * (matQ[4,4] * (x_state[4] - 420.0) + matP[4,4] * (x_pred[4] - 420.0))) +
                       (matB[8,4] * (matQ[8,8] * (x_state[8] - 15.0) + matP[8,8] * (x_pred[8] - 15.0)));

    (* Gradient component 5: Cold HP Separator Liquid Level Letdown Valve *)
    rMpcGradient[5] := (matR[5,5] * (u_ctrl[5] - u_prev[5])) +
                       (matB[7,5] * (matQ[7,7] * (x_state[7] - 55.0) + matP[7,7] * (x_pred[7] - 55.0)));

    (* Gradient component 6: Lean MDEA Scrubber Circulation Flow *)
    rMpcGradient[6] := (matR[6,6] * (u_ctrl[6] - u_prev[6])) +
                       (matB[8,6] * (matQ[8,8] * (x_state[8] - 15.0) + matP[8,8] * (x_pred[8] - 15.0)));

    (* 2. Projected Gradient Descent Step with Adaptive Step Size *)
    FOR iIdxK := 1 TO 6 DO
        u_ctrl[iIdxK] := u_ctrl[iIdxK] - (rMpcStepSize * rMpcGradient[iIdxK]);

        (* Actuator Box Limits Clamping [0.0% .. 100.0%] *)
        IF u_ctrl[iIdxK] < 0.0 THEN
            u_ctrl[iIdxK] := 0.0;
        ELSIF u_ctrl[iIdxK] > 100.0 THEN
            u_ctrl[iIdxK] := 100.0;
        END_IF;
    END_FOR;
END_FOR;

(* --- 5.2 RATE-OF-CHANGE SLEW LIMITING ON MPC OUTPUT COMMANDS --- *)
(* Slew limits per second: Quench valves = 20%/s, Furnace = 5%/s, Letdown = 25%/s, Amine pump = 10%/s *)
(* Delta time scaled limits *)
rMathMax := 20.0 * rDeltaTime_s;
IF (u_ctrl[1] - u_prev[1]) > rMathMax THEN
    u_ctrl[1] := u_prev[1] + rMathMax;
ELSIF (u_ctrl[1] - u_prev[1]) < -rMathMax THEN
    u_ctrl[1] := u_prev[1] - rMathMax;
END_IF;

IF (u_ctrl[2] - u_prev[2]) > rMathMax THEN
    u_ctrl[2] := u_prev[2] + rMathMax;
ELSIF (u_ctrl[2] - u_prev[2]) < -rMathMax THEN
    u_ctrl[2] := u_prev[2] - rMathMax;
END_IF;

IF (u_ctrl[3] - u_prev[3]) > rMathMax THEN
    u_ctrl[3] := u_prev[3] + rMathMax;
ELSIF (u_ctrl[3] - u_prev[3]) < -rMathMax THEN
    u_ctrl[3] := u_prev[3] - rMathMax;
END_IF;

rMathMax := 5.0 * rDeltaTime_s;
IF (u_ctrl[4] - u_prev[4]) > rMathMax THEN
    u_ctrl[4] := u_prev[4] + rMathMax;
ELSIF (u_ctrl[4] - u_prev[4]) < -rMathMax THEN
    u_ctrl[4] := u_prev[4] - rMathMax;
END_IF;

rMathMax := 25.0 * rDeltaTime_s;
IF (u_ctrl[5] - u_prev[5]) > rMathMax THEN
    u_ctrl[5] := u_prev[5] + rMathMax;
ELSIF (u_ctrl[5] - u_prev[5]) < -rMathMax THEN
    u_ctrl[5] := u_prev[5] - rMathMax;
END_IF;

rMathMax := 10.0 * rDeltaTime_s;
IF (u_ctrl[6] - u_prev[6]) > rMathMax THEN
    u_ctrl[6] := u_prev[6] + rMathMax;
ELSIF (u_ctrl[6] - u_prev[6]) < -rMathMax THEN
    u_ctrl[6] := u_prev[6] - rMathMax;
END_IF;

(* Save current control vector into u_prev for next scan *)
FOR iIdxK := 1 TO 6 DO
    u_prev[iIdxK] := u_ctrl[iIdxK];
END_FOR;
"""
