# parts_body3.py

PHASE3_MPC_BLOCK = """
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION & ACTIVE CHATTER SUPPRESSION (PGD SOLVER)                *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.1: Reference Setpoint Vector & Nominal Equilibrium Trajectory Update                               *)
(* ---------------------------------------------------------------------------------------------------- *)
FOR idx_i := 1 TO 10 DO
    x_ref[idx_i] := 0.0; (* Desired state trajectory: zero error, zero modal vibration, nominal preload *)
END_FOR;

u_ref[1] := 0.0;                       (* Zero active damper X nominal force *)
u_ref[2] := 0.0;                       (* Zero active damper Y nominal force *)
u_ref[3] := 0.0;                       (* Zero active piezo Z nominal force *)
u_ref[4] := rThermalGrowth_Z_um;       (* Dynamic feedforward offset reference *)
u_ref[5] := 100.0;                     (* Nominal 100% feedrate override *)
u_ref[6] := 45.0 + (0.55 * (rVotedStatorTemp_degC - 25.0)); (* Base chiller valve demand *)
IF u_ref[6] > 100.0 THEN
    u_ref[6] := 100.0;
ELSIF u_ref[6] < 10.0 THEN
    u_ref[6] := 10.0;
END_IF;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.2: Unrolled 5-Step Receding Prediction Horizon Simulation                                          *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Shift receding control horizon from previous step *)
FOR idx_k := 1 TO 4 DO
    FOR idx_j := 1 TO 6 DO
        u_mpc_traj[idx_k, idx_j] := u_mpc_traj[idx_k + 1, idx_j];
    END_FOR;
END_FOR;
FOR idx_j := 1 TO 6 DO
    u_mpc_traj[5, idx_j] := u_ref[idx_j];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.3: Projected Gradient Descent (PGD) Unrolled Optimization (3 Iterations)                          *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Iteration 1 of PGD *)
FOR idx_j := 1 TO 6 DO
    (* Compute Analytical Quadratic Cost Gradient Term *)
    grad_u[idx_j] := (2.0 * r_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_ref[idx_j])) +
                     (2.0 * s_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_prev[idx_j]));
    
    (* State Backpropagation Coupling via B^T * Q * (x - x_ref) *)
    rTempSum := 0.0;
    FOR idx_i := 1 TO 10 DO
        rTempSum := rTempSum + (b_mat[idx_i, idx_j] * q_diag[idx_i] * (x_state[idx_i] - x_ref[idx_i]));
    END_FOR;
    grad_u[idx_j] := grad_u[idx_j] + (2.0 * rTempSum);
    
    (* Gradient Descent Step *)
    u_tentative[idx_j] := u_mpc_traj[1, idx_j] - (rMpcStepSize * grad_u[idx_j]);
    
    (* Physical Box Saturation Projection *)
    IF u_tentative[idx_j] > u_box_max[idx_j] THEN
        u_tentative[idx_j] := u_box_max[idx_j];
    ELSIF u_tentative[idx_j] < u_box_min[idx_j] THEN
        u_tentative[idx_j] := u_box_min[idx_j];
    END_IF;
    
    (* Dynamic Actuator Slew Rate Limiter *)
    IF (u_tentative[idx_j] - u_prev[idx_j]) > du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] + du_slew_max[idx_j];
    ELSIF (u_tentative[idx_j] - u_prev[idx_j]) < -du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] - du_slew_max[idx_j];
    END_IF;
    
    u_mpc_traj[1, idx_j] := u_tentative[idx_j];
END_FOR;

(* Iteration 2 of PGD *)
FOR idx_j := 1 TO 6 DO
    grad_u[idx_j] := (2.0 * r_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_ref[idx_j])) +
                     (2.0 * s_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_prev[idx_j]));
    
    rTempSum := 0.0;
    FOR idx_i := 1 TO 10 DO
        rTempSum := rTempSum + (b_mat[idx_i, idx_j] * q_diag[idx_i] * (x_state[idx_i] - x_ref[idx_i]));
    END_FOR;
    grad_u[idx_j] := grad_u[idx_j] + (2.0 * rTempSum);
    
    u_tentative[idx_j] := u_mpc_traj[1, idx_j] - (rMpcStepSize * grad_u[idx_j]);
    
    IF u_tentative[idx_j] > u_box_max[idx_j] THEN
        u_tentative[idx_j] := u_box_max[idx_j];
    ELSIF u_tentative[idx_j] < u_box_min[idx_j] THEN
        u_tentative[idx_j] := u_box_min[idx_j];
    END_IF;
    
    IF (u_tentative[idx_j] - u_prev[idx_j]) > du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] + du_slew_max[idx_j];
    ELSIF (u_tentative[idx_j] - u_prev[idx_j]) < -du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] - du_slew_max[idx_j];
    END_IF;
    
    u_mpc_traj[1, idx_j] := u_tentative[idx_j];
END_FOR;

(* Iteration 3 of PGD (Final Unrolled Step) *)
FOR idx_j := 1 TO 6 DO
    grad_u[idx_j] := (2.0 * r_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_ref[idx_j])) +
                     (2.0 * s_diag[idx_j] * (u_mpc_traj[1, idx_j] - u_prev[idx_j]));
    
    rTempSum := 0.0;
    FOR idx_i := 1 TO 10 DO
        rTempSum := rTempSum + (b_mat[idx_i, idx_j] * q_diag[idx_i] * (x_state[idx_i] - x_ref[idx_i]));
    END_FOR;
    grad_u[idx_j] := grad_u[idx_j] + (2.0 * rTempSum);
    
    u_tentative[idx_j] := u_mpc_traj[1, idx_j] - (rMpcStepSize * grad_u[idx_j]);
    
    IF u_tentative[idx_j] > u_box_max[idx_j] THEN
        u_tentative[idx_j] := u_box_max[idx_j];
    ELSIF u_tentative[idx_j] < u_box_min[idx_j] THEN
        u_tentative[idx_j] := u_box_min[idx_j];
    END_IF;
    
    IF (u_tentative[idx_j] - u_prev[idx_j]) > du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] + du_slew_max[idx_j];
    ELSIF (u_tentative[idx_j] - u_prev[idx_j]) < -du_slew_max[idx_j] THEN
        u_tentative[idx_j] := u_prev[idx_j] - du_slew_max[idx_j];
    END_IF;
    
    u_mpc_traj[1, idx_j] := u_tentative[idx_j];
    u_ctrl[idx_j] := u_mpc_traj[1, idx_j];
    u_prev[idx_j] := u_ctrl[idx_j];
END_FOR;

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.4: Active Inertial Mass Damping (AIMD) & Proof-Mass Control Law                                     *)
(* ---------------------------------------------------------------------------------------------------- *)
IF bActiveDampingEnable THEN
    (* Anti-phase proof-mass voice coil counter-forces *)
    rActiveDampForceCmd_X_N := u_ctrl[1] - (35.0 * x_state[4]); (* Modal velocity derivative feedback *)
    rActiveDampForceCmd_Y_N := u_ctrl[2] - (38.0 * x_state[5]);
    rActiveDampForceCmd_Z_N := u_ctrl[3] - (45.0 * x_state[6]);
    
    (* Dynamic Clamping to Actuator Limits *)
    IF rActiveDampForceCmd_X_N > 450.0 THEN
        rActiveDampForceCmd_X_N := 450.0;
    ELSIF rActiveDampForceCmd_X_N < -450.0 THEN
        rActiveDampForceCmd_X_N := -450.0;
    END_IF;
    
    IF rActiveDampForceCmd_Y_N > 450.0 THEN
        rActiveDampForceCmd_Y_N := 450.0;
    ELSIF rActiveDampForceCmd_Y_N < -450.0 THEN
        rActiveDampForceCmd_Y_N := -450.0;
    END_IF;
    
    IF rActiveDampForceCmd_Z_N > 800.0 THEN
        rActiveDampForceCmd_Z_N := 800.0;
    ELSIF rActiveDampForceCmd_Z_N < -800.0 THEN
        rActiveDampForceCmd_Z_N := -800.0;
    END_IF;
ELSE
    rActiveDampForceCmd_X_N := 0.0;
    rActiveDampForceCmd_Y_N := 0.0;
    rActiveDampForceCmd_Z_N := 0.0;
END_IF;

rChillerValveDemand_pct := u_ctrl[6];

(* ---------------------------------------------------------------------------------------------------- *)
(* 3.5: Spindle Speed Variation (SSV) Regenerative Chatter Suppression & Feedrate Throttling            *)
(* ---------------------------------------------------------------------------------------------------- *)
(* Compute Triaxial Spindle Nose Vibration Vector Magnitude *)
rTempSum := SQRT((rVotedSpindleAccel_X_ms2 * rVotedSpindleAccel_X_ms2) +
                 (rVotedSpindleAccel_Y_ms2 * rVotedSpindleAccel_Y_ms2) +
                 (rVotedSpindleAccel_Z_ms2 * rVotedSpindleAccel_Z_ms2));

(* Peak Spectral Acceleration Low-Pass Filter *)
rChatterPeakSpectrum_ms2 := rChatterPeakSpectrum_ms2 + 0.080 * (rTempSum - rChatterPeakSpectrum_ms2);
rPeakChatterAmplitude_ms2 := rChatterPeakSpectrum_ms2;

(* Dominant Chatter Resonant Frequency Estimation *)
IF rVotedSpindleSpeed_rpm > 100.0 AND nToolFluteCount > 0 THEN
    rDominantChatterFreq_Hz := ((REAL_TO_INT(nToolFluteCount) * rVotedSpindleSpeed_rpm) / 60.0) * 1.185 + 28.5;
ELSE
    rDominantChatterFreq_Hz := 0.0;
END_IF;

(* Evaluate Chatter Threshold and Modulate Spindle Speed Continuously *)
IF rPeakChatterAmplitude_ms2 >= VIB_CHATTER_H_WARN_MS2 THEN
    bChatterActiveCondition := TRUE;
    
    (* Integrate Sinusoidal Phase Angle *)
    rSSV_ModulationPhase_rad := rSSV_ModulationPhase_rad +
                                (2.0 * 3.14159265 * rSSV_ModulationFreq_Hz * T_CYCLE_SEC);
    IF rSSV_ModulationPhase_rad > 6.2831853 THEN
        rSSV_ModulationPhase_rad := rSSV_ModulationPhase_rad - 6.2831853;
    END_IF;
    
    (* Sinusoidally Modulated Spindle Speed Command *)
    rModulatedSpindleSpeed_rpm := rCmdSpindleSpeed_rpm *
                                  (1.0 + rSSV_AmplitudeFactor * SIN(rSSV_ModulationPhase_rad));
    
    (* Dynamically Throttle Feedrate Override to Starve Chatter Energy *)
    rAdaptiveFeedOverride_pct := 100.0 - ((rPeakChatterAmplitude_ms2 - VIB_CHATTER_H_WARN_MS2) * 8.50);
    IF rAdaptiveFeedOverride_pct < 35.0 THEN
        rAdaptiveFeedOverride_pct := 35.0;
    ELSIF rAdaptiveFeedOverride_pct > 100.0 THEN
        rAdaptiveFeedOverride_pct := 100.0;
    END_IF;
ELSE
    bChatterActiveCondition := FALSE;
    rModulatedSpindleSpeed_rpm := rCmdSpindleSpeed_rpm;
    rAdaptiveFeedOverride_pct := u_ctrl[5];
END_IF;
"""
