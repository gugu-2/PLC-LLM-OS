# phase_generators_pt2.py
# Phase 3: State-Space Propagation & Luenberger Observer
# Phase 4: Receding-Horizon MPC Optimization with 6 Unrolled Iterations of PGD

def generate_phase3():
    return """
(* ==================================================================================================== *)
(* PHASE 3: CYBER-PHYSICAL DISCRETE STATE-SPACE PROPAGATION & LUENBERGER OBSERVER                       *)
(* Mathematical Formulation at Ts = 1.0 ms:                                                            *)
(*   x_pred[k+1] = A * x_state[k] + B * u_ctrl[k]                                                      *)
(*   y_est[k]    = C * x_pred[k+1] + D * u_ctrl[k]                                                      *)
(*   e_innov[k]  = y_meas[k] - y_est[k]                                                                *)
(*   x_hat[k+1]  = x_pred[k+1] + L * e_innov[k]                                                        *)
(*   x_state[k+1]= x_hat[k+1]                                                                           *)
(* ==================================================================================================== *)

(* Pack Control Actuator Vector u_ctrl *)
u_ctrl[1] := rCmd_InjectionServoCurrent_pct;
u_ctrl[2] := rCmd_HoldingPressure_bar;
u_ctrl[3] := rCmd_ScrewRotationSpeed_rpm;
u_ctrl[4] := rCmd_BackpressureValve_bar;
u_ctrl[5] := rCmd_MoldCoolingValve_pct;
u_ctrl[6] := rCmd_ClampingToggleServo_pct;

(* Pack Filtered Sensor Measurement Vector y_meas *)
y_meas[1] := rCalculatedScrewVelocity_mms;
y_meas[2] := rVoted_PT101_bar;
y_meas[3] := rVoted_PT201_bar;
y_meas[4] := rPT_Cavity_204_EndFill;
y_meas[5] := rVoted_WT401_kN;
y_meas[6] := rVoted_TT501_degC;

(* Forward State Propagation: x_pred = A * x_state + B * u_ctrl *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matA[i, j] * x_state[j]);
    END_FOR;
    FOR j := 1 TO 6 DO
        rTempSum := rTempSum + (matB[i, j] * u_ctrl[j]);
    END_FOR;
    x_pred[i] := rTempSum;
END_FOR;

(* Physical Safety Clamping of Predicted State Trajectory *)
x_pred[1] := LIMIT(-50.0,  x_pred[1], 350.0);   (* Screw Velocity [mm/s] *)
x_pred[2] := LIMIT(0.0,    x_pred[2], 2400.0);  (* Nozzle Pressure [bar] *)
x_pred[3] := LIMIT(0.0,    x_pred[3], 1500.0);  (* Cavity 1 Pressure [bar] *)
x_pred[4] := LIMIT(0.0,    x_pred[4], 1200.0);  (* Cavity 4 Pressure [bar] *)
x_pred[5] := LIMIT(0.0,    x_pred[5], 28000.0); (* Clamping Tonnage [kN] *)
x_pred[6] := LIMIT(60.0,   x_pred[6], 180.0);   (* Mold Cavity Temperature [deg C] *)
x_pred[7] := LIMIT(0.0,    x_pred[7], 1500.0);  (* Gate Frozen Skin Thickness [um] *)
x_pred[8] := LIMIT(0.0,    x_pred[8], 300.0);   (* Screw Backpressure [bar] *)

(* Estimated Physical Outputs: y_est = C * x_pred + D * u_ctrl *)
FOR i := 1 TO 6 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + (matC[i, j] * x_pred[j]);
    END_FOR;
    FOR j := 1 TO 6 DO
        rTempSum := rTempSum + (matD[i, j] * u_ctrl[j]);
    END_FOR;
    y_est[i] := rTempSum;
    e_innov[i] := y_meas[i] - y_est[i];
END_FOR;

(* Luenberger State Innovation Correction: x_hat = x_pred + L * e_innov *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 6 DO
        rTempSum := rTempSum + (matL[i, j] * e_innov[j]);
    END_FOR;
    x_hat[i] := x_pred[i] + rTempSum;
    x_state[i] := x_hat[i];
END_FOR;

(* Update Real-Time Monitored Telemetry Outputs *)
rEst_ScrewVelocity_mms        := x_state[1];
rEst_NozzlePressure_bar       := x_state[2];
rEst_Cavity1Pressure_bar      := x_state[3];
rEst_Cavity4Pressure_bar      := x_state[4];
rEst_ClampingTonnage_kN       := x_state[5];
rEst_GateSkinThickness_um     := x_state[7];
rEst_MeltShearRate_s1         := rCalculatedShearRate_s1;
rEst_MeltApparentViscosity_Pas:= rCalculatedViscosity_Pas;
rEst_MoldDeflection_um        := rMoldSeparation_um;
rEst_TieBarAsymmetry_kN       := rMaxTieBarDelta_kN;
rEst_CavityPressureDeriv_bars := rFiltered_dPCav_dt;
rMon_ScrewLinearPos_mm        := rVoted_ST301_mm;
"""

def generate_phase4():
    return """
(* ==================================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) VIA 6 UNROLLED PGD ITERATIONS               *)
(* Solves real-time quadratic cost functional over prediction horizon Np = 5 steps:                    *)
(*   min_{u} J = sum_{k=1}^5 (x_k - x_ref)' * Q * (x_k - x_ref) +                                      *)
(*               sum_{k=0}^4 (u_k - u_ref)' * R * (u_k - u_ref) + du_k' * S * du_k +                   *)
(*               (x_5 - x_ref)' * P * (x_5 - x_ref)                                                     *)
(* Subject to actuator box constraints [u_min, u_max] and maximum slew limits [-du_max, +du_max].     *)
(* Optimization Algorithm: 6 Unrolled Iterations of Projected Gradient Descent (PGD).                   *)
(* ==================================================================================================== *)

(* Dynamic State Reference Trajectory Allocation based on Machine Operating Regime *)
IF nFsmState = 4 THEN (* Fast Volumetric Injection Fill *)
    x_ref[1] := rSet_InjectionSpeed_Stage2;          (* Target Injection Velocity Profile [mm/s] *)
    x_ref[2] := 1650.0;                             (* Maximum Dynamic Nozzle Fill Head [bar] *)
    x_ref[3] := 450.0;                              (* Target Cavity 1 Filling Pressure [bar] *)
    x_ref[4] := 280.0;                              (* Target Cavity 4 Filling Pressure [bar] *)
    x_ref[5] := rSet_ClampTonnage_Target;           (* Full Clamp Force Tonnage [kN] *)
    x_ref[6] := 120.0;                              (* Conformal Mold Surface Temperature [deg C] *)
    x_ref[7] := 0.0;                                (* Suppress Gate Skin Formation During Fast Fill *)
    x_ref[8] := 0.0;                                (* Backpressure Decoupled *)
ELSIF nFsmState = 5 THEN (* V/P Transfer Point Deceleration *)
    x_ref[1] := 15.0;                               (* Deceleration Velocity Approaching Switch [mm/s] *)
    x_ref[2] := rSet_HoldPressure_Stage1;           (* Target Pack Pressure [bar] *)
    x_ref[3] := rSet_HoldPressure_Stage1 * 0.85;    (* Cavity 1 Pressure Transfer Target [bar] *)
    x_ref[4] := rSet_HoldPressure_Stage1 * 0.70;    (* Cavity 4 Pressure Transfer Target [bar] *)
    x_ref[5] := rSet_ClampTonnage_Target;           (* Clamp Tonnage [kN] *)
    x_ref[6] := 120.0;                              (* Mold Temperature [deg C] *)
    x_ref[7] := 50.0;                               (* Initial Skin Layer Growth [um] *)
    x_ref[8] := 0.0;
ELSIF nFsmState = 6 THEN (* Multi-Stage Packing & Holding Pressure *)
    x_ref[1] := 0.0;                                (* Stationary Cushion Target [mm/s] *)
    CASE nHoldingProfileSubStage OF
        1: x_ref[2] := rSet_HoldPressure_Stage1;
        2: x_ref[2] := rSet_HoldPressure_Stage2;
        3: x_ref[2] := rSet_HoldPressure_Stage3;
        4: x_ref[2] := rSet_HoldPressure_Stage4;
        5: x_ref[2] := rSet_HoldPressure_Stage5;
    ELSE
        x_ref[2] := rSet_HoldPressure_Stage2;
    END_CASE;
    x_ref[3] := x_ref[2] * 0.88;                    (* Direct Cavity 1 Quartz Pressure Target [bar] *)
    x_ref[4] := x_ref[2] * 0.75;                    (* End-of-Fill Cavity 4 Pressure Target [bar] *)
    x_ref[5] := rSet_ClampTonnage_Target;           (* Full Clamp Force Tonnage [kN] *)
    x_ref[6] := 120.0;                              (* Tooling Temperature [deg C] *)
    x_ref[7] := rGateHalfThickness_um;              (* Complete Gate Solidification Target [um] *)
    x_ref[8] := 0.0;
ELSIF nFsmState = 8 THEN (* Plasticizing Extruder Recovery & Backpressure *)
    x_ref[1] := -18.0;                              (* Linear Screw Recovery Velocity [mm/s] *)
    x_ref[2] := rSet_PlasticizingBackpress;         (* Barrel Head Pressure [bar] *)
    x_ref[3] := 0.0;
    x_ref[4] := 0.0;
    x_ref[5] := rSet_ClampTonnage_Target;
    x_ref[6] := 120.0;
    x_ref[7] := rGateHalfThickness_um;
    x_ref[8] := rSet_PlasticizingBackpress;         (* Regulated Backpressure [bar] *)
ELSE (* Idle / Standby Baseline References *)
    x_ref[1] := 0.0;
    x_ref[2] := 0.0;
    x_ref[3] := 0.0;
    x_ref[4] := 0.0;
    x_ref[5] := 0.0;
    x_ref[6] := 120.0;
    x_ref[7] := 0.0;
    x_ref[8] := 0.0;
END_IF;

(* Initialize Control Horizon Plan u_horizon with Previous Solution *)
FOR k_idx := 1 TO 5 DO
    FOR j := 1 TO 6 DO
        u_horizon[k_idx, j] := u_prev[j];
    END_FOR;
END_FOR;

(* ==================================================================================================== *)
(* UNROLLED 6-ITERATION PROJECTED GRADIENT DESCENT (PGD) OPTIMIZATION LOOP                              *)
(* ==================================================================================================== *)
FOR iter_idx := 1 TO 6 DO
    (* Step 1: Forward State Rollout Over Prediction Horizon Np = 5 *)
    FOR k_idx := 1 TO 5 DO
        FOR i := 1 TO 8 DO
            rTempSum := 0.0;
            IF k_idx = 1 THEN
                FOR j := 1 TO 8 DO
                    rTempSum := rTempSum + (matA[i, j] * x_state[j]);
                END_FOR;
            ELSE
                FOR j := 1 TO 8 DO
                    rTempSum := rTempSum + (matA[i, j] * x_rollout[k_idx - 1, j]);
                END_FOR;
            END_IF;
            FOR j := 1 TO 6 DO
                rTempSum := rTempSum + (matB[i, j] * u_horizon[k_idx, j]);
            END_FOR;
            x_rollout[k_idx, i] := rTempSum;
        END_FOR;
    END_FOR;

    (* Step 2: Cumulative Quadratic Objective Function J Evaluation *)
    rCost_J := 0.0;
    FOR k_idx := 1 TO 5 DO
        FOR i := 1 TO 8 DO
            IF k_idx < 5 THEN
                rCost_J := rCost_J + (matQ[i, i] * EXPT(x_rollout[k_idx, i] - x_ref[i], 2.0));
            ELSE
                rCost_J := rCost_J + (matP[i, i] * EXPT(x_rollout[k_idx, i] - x_ref[i], 2.0));
            END_IF;
        END_FOR;
        FOR j := 1 TO 6 DO
            rCost_J := rCost_J + (matR[j, j] * EXPT(u_horizon[k_idx, j] - u_prev[j], 2.0));
            rCost_J := rCost_J + (matS[j, j] * EXPT(u_horizon[k_idx, j] - u_prev[j], 2.0));
        END_FOR;
    END_FOR;

    (* Step 3: Compute Projected Analytical Gradient grad_J = dJ/du at Stage 1 *)
    FOR j := 1 TO 6 DO
        rTempSum := 0.0;
        (* State tracking penalty adjoint sensitivity backpropagation *)
        FOR k_idx := 1 TO 5 DO
            FOR i := 1 TO 8 DO
                IF k_idx < 5 THEN
                    rTempSum := rTempSum + (2.0 * matQ[i, i] * (x_rollout[k_idx, i] - x_ref[i]) * matB[i, j]);
                ELSE
                    rTempSum := rTempSum + (2.0 * matP[i, i] * (x_rollout[k_idx, i] - x_ref[i]) * matB[i, j]);
                END_IF;
            END_FOR;
        END_FOR;
        (* Actuator effort and slew rate penalties *)
        rTempSum := rTempSum + (2.0 * matR[j, j] * (u_horizon[1, j] - u_prev[j])) +
                               (2.0 * matS[j, j] * (u_horizon[1, j] - u_prev[j]));
        grad_J[j] := rTempSum;
    END_FOR;

    (* Step 4: Gradient Descent Step with Analytical Box Saturation & Slew Projection *)
    FOR j := 1 TO 6 DO
        (* Gradient Descent Update *)
        u_mpc_opt[j] := u_horizon[1, j] - (rAlpha_pgd * grad_J[j]);

        (* Hard Box Constraint Saturation Projection *)
        u_mpc_opt[j] := LIMIT(u_min[j], u_mpc_opt[j], u_max[j]);

        (* Slew Rate Maximum Acceleration Projection *)
        rDelta_u := LIMIT(-du_max[j], u_mpc_opt[j] - u_prev[j], du_max[j]);
        u_horizon[1, j] := u_prev[j] + rDelta_u;
    END_FOR;
END_FOR;
"""
