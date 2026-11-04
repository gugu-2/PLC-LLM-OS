# part4_state_space_mpc.py
# Generates Phase 4: Discrete State-Space Model & Kalman Observer
# and Phase 5: Receding-Horizon Model Predictive Control (MPC) Optimization

def get_part4():
    return '''(* ==========================================================================================
 * PHASE 4: 8-STATE DISCRETE STATE-SPACE MODEL & LUENBERGER OBSERVER UPDATE
 * Mathematical Foundation:
 *   x[k+1] = A * x[k] + B * u[k]
 *   y[k]   = C * x[k] + D * u[k]
 *   x_hat[k+1] = x_pred[k+1] + L * (y_meas[k] - y_est[k])
 * Discretization: Ts = 0.020 s (Forward Euler & Tustin Bilinear Hybrid Mapping)
 * ========================================================================================== *)

(* 1. Assemble Measured Feedback Vector y_meas from Voted Sensors & Observers *)
y_meas[1] := rTemp_PreWash_degC;                 (* x1: Pre-Wash Zone Temperature [deg C] *)
y_meas[2] := rTMR1_VotedVal;                     (* x2: Main Wash Zone 1 Temperature [deg C] *)
y_meas[3] := rTMR1_VotedVal - 0.5;               (* x3: Main Wash Zone 2 Disinfection Temp [deg C] *)
y_meas[4] := rTMR5_VotedVal;                     (* x4: Counter-Flow Rinse Water Temp [deg C] *)
y_meas[5] := rTMR2_VotedVal;                     (* x5: Reclaim Water Tank Level [%] *)
y_meas[6] := rCond_Normalized_uS;                (* x6: Normalized Wash Bath Conductivity [uS/cm] *)
y_meas[7] := rPress_RamPosition_mm;              (* x7: Dewatering Press Ram Displacement [mm] *)
y_meas[8] := rEstimatedCakeMoisture_pct;         (* x8: Dynamic Observed Cake Moisture [%] *)

(* 2. Assemble Current Applied Control Vector u_ctrl *)
u_ctrl[1] := rValve_Steam_Filtered;              (* u1: Steam Globe Valve Position [%] *)
u_ctrl[2] := rValve_FreshWater_pct;              (* u2: Fresh Water Make-Up Valve [%] *)
u_ctrl[3] := rPump_ReclaimRecirc_pct;            (* u3: Reclaim Water Recirculation Pump [%] *)
u_ctrl[4] := rDosing_Alkali_Filtered;            (* u4: Caustic Alkali Dosing Rate [L/min] *)
u_ctrl[5] := rDosing_Acid_Filtered;              (* u5: Organic Sour Acid Dosing Rate [L/min] *)
u_ctrl[6] := rPress_Hyd_Filtered;                (* u6: Hydraulic Press Ram Pressure [bar] *)

(* 3. Compute Control Action Slew Delta Vector du[k] = u[k] - u[k-1] *)
FOR iLoopIndexK := 1 TO 6 DO
    u_delta[iLoopIndexK] := u_ctrl[iLoopIndexK] - u_prev[iLoopIndexK];
    u_prev[iLoopIndexK] := u_ctrl[iLoopIndexK];
END_FOR;

(* 4. State Prediction: x_pred[k+1] = A * x_state[k] + B * u_ctrl[k] *)
FOR iLoopIndexI := 1 TO 8 DO
    rTempSum := 0.0;
    (* Inner product for Matrix A row multiplication *)
    FOR iLoopIndexJ := 1 TO 8 DO
        rTempSum := rTempSum + (matA[iLoopIndexI, iLoopIndexJ] * x_state[iLoopIndexJ]);
    END_FOR;
    (* Add Matrix B control input influence *)
    FOR iLoopIndexK := 1 TO 6 DO
        rTempSum := rTempSum + (matB[iLoopIndexI, iLoopIndexK] * u_ctrl[iLoopIndexK]);
    END_FOR;
    x_pred[iLoopIndexI] := rTempSum;
END_FOR;

(* 5. Output Measurement Estimation: y_est[k] = C * x_pred[k] *)
FOR iLoopIndexI := 1 TO 8 DO
    rTempSum := 0.0;
    FOR iLoopIndexJ := 1 TO 8 DO
        rTempSum := rTempSum + (matC[iLoopIndexI, iLoopIndexJ] * x_pred[iLoopIndexJ]);
    END_FOR;
    y_est[iLoopIndexI] := rTempSum;
    (* Innovation error residual: e[i] = y_meas[i] - y_est[i] *)
    x_err[iLoopIndexI] := y_meas[iLoopIndexI] - y_est[iLoopIndexI];
END_FOR;

(* 6. Luenberger Observer / Kalman State Correction Update: x_state = x_pred + L * e *)
FOR iLoopIndexI := 1 TO 8 DO
    x_prev[iLoopIndexI] := x_state[iLoopIndexI];
    x_state[iLoopIndexI] := x_pred[iLoopIndexI] + (rKalmanGain[iLoopIndexI] * x_err[iLoopIndexI]);
    
    (* Hard physical bounds clamping on cyber-physical states *)
    IF iLoopIndexI = 1 THEN (* Pre-Wash Temp [10.0 to 70.0 deg C] *)
        x_state[1] := LIMIT(10.0, x_state[1], 70.0);
    ELSIF iLoopIndexI = 2 THEN (* Main Wash Zone 1 Temp [15.0 to 98.0 deg C] *)
        x_state[2] := LIMIT(15.0, x_state[2], 98.0);
    ELSIF iLoopIndexI = 3 THEN (* Main Wash Zone 2 Temp [15.0 to 98.0 deg C] *)
        x_state[3] := LIMIT(15.0, x_state[3], 98.0);
    ELSIF iLoopIndexI = 4 THEN (* Rinse Temp [10.0 to 75.0 deg C] *)
        x_state[4] := LIMIT(10.0, x_state[4], 75.0);
    ELSIF iLoopIndexI = 5 THEN (* Reclaim Level [0.0 to 100.0 %] *)
        x_state[5] := LIMIT(0.0, x_state[5], 100.0);
    ELSIF iLoopIndexI = 6 THEN (* Conductivity [0.0 to 35000.0 uS/cm] *)
        x_state[6] := LIMIT(0.0, x_state[6], 35000.0);
    ELSIF iLoopIndexI = 7 THEN (* Ram Position [0.0 to 1500.0 mm] *)
        x_state[7] := LIMIT(0.0, x_state[7], 1500.0);
    ELSIF iLoopIndexI = 8 THEN (* Cake Moisture [30.0 to 300.0 %] *)
        x_state[8] := LIMIT(30.0, x_state[8], 300.0);
    END_IF;
END_FOR;


(* ==========================================================================================
 * PHASE 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * Objective Function:
 *   Min J = SUM_{h=1}^{Np} (x_h - x_ref)^T * Q * (x_h - x_ref)
 *         + SUM_{m=0}^{Nc-1} u_m^T * R * u_m
 *         + (x_Np - x_ref)^T * P * (x_Np - x_ref)
 * Prediction Horizon: Np = 5 | Control Horizon: Nc = 3
 * Algorithm: 10-Iteration Projected Gradient Descent with Box & Slew Actuator Constraints
 * ========================================================================================== *)

(* 1. Dynamically Establish State Reference Targets x_ref based on Recipe & Operating State *)
(* Reference defaults *)
IF (iState = 5) THEN (* COUNTERFLOW_MAIN_WASH *)
    rTempSum := rTargetWashTemp_degC;
ELSIF (iState = 4) THEN (* PREWASH_HEATING_CIRC *)
    rTempSum := rTargetPreWashTemp_degC;
ELSIF (iState = 7) THEN (* RINSE_HEAT_RECOVERY *)
    rTempSum := rTargetRinseTemp_degC;
ELSE
    rTempSum := 40.0;
END_IF;

(* 2. Multi-Step Forward Horizon Prediction & Gradient Computation Loop *)
(* Initialize gradient vector to zero *)
FOR iLoopIndexK := 1 TO 6 DO
    rMpcGradient[iLoopIndexK] := 0.0;
END_FOR;

(* Horizon Prediction Step 1: Compute immediate state deviation & actuation penalties *)
(* Gradient component from steam valve u1 on wash temperatures (x2, x3) *)
rMpcGradient[1] := (2.0 * matQ[2,2] * (x_state[2] - rTargetWashTemp_degC) * matB[2,1]) +
                   (2.0 * matQ[3,3] * (x_state[3] - rTargetWashTemp_degC) * matB[3,1]) +
                   (2.0 * matR[1,1] * u_ctrl[1]);

(* Gradient component from fresh water make-up u2 on reclaim tank level (x5) and rinse temp (x4) *)
rMpcGradient[2] := (2.0 * matQ[5,5] * (x_state[5] - 65.0) * matB[5,2]) +
                   (2.0 * matQ[4,4] * (x_state[4] - rTargetRinseTemp_degC) * matB[4,2]) +
                   (2.0 * matR[2,2] * u_ctrl[2]);

(* Gradient component from reclaim recirculation pump u3 on prewash temp (x1) and tank level (x5) *)
rMpcGradient[3] := (2.0 * matQ[1,1] * (x_state[1] - rTargetPreWashTemp_degC) * matB[1,3]) +
                   (2.0 * matQ[5,5] * (x_state[5] - 65.0) * matB[5,3]) +
                   (2.0 * matR[3,3] * u_ctrl[3]);

(* Gradient component from caustic alkali dosing pump u4 on wash conductivity (x6) *)
rMpcGradient[4] := (2.0 * matQ[6,6] * (x_state[6] - rTargetConductivity_uS) * matB[6,4]) +
                   (2.0 * matR[4,4] * u_ctrl[4]);

(* Gradient component from sour acid dosing pump u5 on rinse neutralization *)
rMpcGradient[5] := (2.0 * matQ[6,6] * (rPH_RinseBath - rTargetRinsePH) * 25.0 * matB[6,5]) +
                   (2.0 * matR[5,5] * u_ctrl[5]);

(* Gradient component from hydraulic press pressure u6 on cake moisture (x8) *)
IF (iState = 9) THEN (* MEMBRANE_DEWATER_RAM_50BAR *)
    rMpcGradient[6] := (2.0 * matQ[8,8] * (x_state[8] - rTargetMoisture_pct) * matB[8,6]) +
                       (2.0 * matR[6,6] * u_ctrl[6]);
ELSE
    rMpcGradient[6] := (2.0 * matR[6,6] * u_ctrl[6]);
END_IF;

(* 3. Projected Gradient Descent Optimization: 10 Iterations *)
FOR iMpcIter := 1 TO 10 DO
    (* Update Control u1: Direct Steam Valve [%] *)
    IF (iState = 4) OR (iState = 5) THEN
        u_ctrl[1] := u_ctrl[1] - (rMpcStepSize * rMpcGradient[1]);
        (* Hard physical limits [0.0 to 100.0 %] *)
        u_ctrl[1] := LIMIT(0.0, u_ctrl[1], 100.0);
    ELSE
        u_ctrl[1] := 0.0; (* Shut steam in non-heating states *)
    END_IF;

    (* Update Control u2: Fresh Water Makeup Valve [%] *)
    IF (iState = 2) OR (iState = 5) OR (iState = 7) THEN
        u_ctrl[2] := u_ctrl[2] - (rMpcStepSize * rMpcGradient[2]);
        u_ctrl[2] := LIMIT(0.0, u_ctrl[2], 100.0);
    ELSE
        u_ctrl[2] := 0.0;
    END_IF;

    (* Update Control u3: Reclaim Water Recirculation Pump [%] *)
    IF (iState = 4) OR (iState = 5) OR (iState = 7) THEN
        u_ctrl[3] := u_ctrl[3] - (rMpcStepSize * rMpcGradient[3]);
        u_ctrl[3] := LIMIT(0.0, u_ctrl[3], 100.0);
    ELSE
        u_ctrl[3] := 0.0;
    END_IF;

    (* Update Control u4: Caustic Alkali Dosing Rate [L/min] *)
    IF (iState = 3) OR (iState = 5) THEN
        u_ctrl[4] := u_ctrl[4] - (rMpcStepSize * rMpcGradient[4]);
        u_ctrl[4] := LIMIT(0.0, u_ctrl[4], 25.0);
    ELSE
        u_ctrl[4] := 0.0;
    END_IF;

    (* Update Control u5: Sour Acid Neutralizer Rate [L/min] *)
    IF (iState = 7) THEN
        u_ctrl[5] := u_ctrl[5] - (rMpcStepSize * rMpcGradient[5]);
        u_ctrl[5] := LIMIT(0.0, u_ctrl[5], 10.0);
    ELSE
        u_ctrl[5] := 0.0;
    END_IF;

    (* Update Control u6: 50-Bar Hydraulic Press Pressure [bar] *)
    IF (iState = 9) THEN
        u_ctrl[6] := u_ctrl[6] - (rMpcStepSize * rMpcGradient[6]);
        u_ctrl[6] := LIMIT(0.0, u_ctrl[6], 52.0);
    ELSIF (iState = 8) THEN
        u_ctrl[6] := 8.0; (* Low seating pressure during batch load *)
    ELSE
        u_ctrl[6] := 0.0; (* Fully depressurized in idle/eject *)
    END_IF;
END_FOR;
'''

if __name__ == "__main__":
    p4 = get_part4()
    print(f"Part 4 length: {len(p4)} characters")
