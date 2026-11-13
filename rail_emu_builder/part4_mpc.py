# rail_emu_builder/part4_mpc.py

def get_part4():
    return '''(* ============================================================================================== *)
(* PHASE 3: FIRST-PRINCIPLES CYBER-PHYSICAL 8-STATE DISCRETE STATE-SPACE MODEL ESTIMATION         *)
(* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
(* y[k]   = C * x[k] + D * u[k], with Luenberger Innovation Observer Correction                    *)
(* ============================================================================================== *)

(* 1. Populate Measured Output Vector y_meas (8x1) *)
y_meas[1] := rTrainSpeed_ms;
y_meas[2] := rAxle1_LinearVelocity_ms;
y_meas[3] := rAxle2_LinearVelocity_ms;
y_meas[4] := rVotedPantoForce_N;
y_meas[5] := rVotedDCLinkVoltage_V;
y_meas[6] := rTractionTorqueCommand_kNm;
y_meas[7] := rVotedBrakeCylPressure_bar;
y_meas[8] := rObservedAdhesionCoeff;

(* 2. Populate External Disturbance Vector d_dist (4x1) *)
(* d[1]: Track Topography Elevation Force [kN] = M * g * sin(theta) *)
d_dist[1] := (TRAIN_MASS_TARE_KG * 0.00981 * rTrackGradient_permille) / 1000.0;
(* d[2]: Headwind Relative Air Velocity [m/s] *)
d_dist[2] := rRelativeHeadwindSpeed_ms;
(* d[3]: Catenary Voltage Fluctuation from 25.0 kV Nominal [kV] *)
d_dist[3] := rCatenaryLineVoltage_kV - 25.0;
(* d[4]: Railhead Surface Contamination Friction Derating (1.0=Dry, 0.2=Leaves/Ice) *)
IF (rAmbientAirTemp_degC < 2.0) OR bTrackSandingManualCmd THEN
    d_dist[4] := 0.45;
ELSE
    d_dist[4] := 1.00;
END_IF;

(* 3. Compute Discrete State-Space Propagation x[k+1] = A*x[k] + B*u[k] + E*d[k] *)
FOR i := 1 TO 8 DO
    rScratchAccum := 0.0;
    (* State transition A * x *)
    FOR j := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (a_mat[i, j] * x_state[j]);
    END_FOR;
    (* Control input coupling B * u *)
    FOR j := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (b_mat[i, j] * u_ctrl[j]);
    END_FOR;
    (* Disturbance coupling E * d *)
    FOR j := 1 TO 4 DO
        rScratchAccum := rScratchAccum + (e_mat[i, j] * d_dist[j]);
    END_FOR;
    x_next[i] := rScratchAccum;
END_FOR;

(* 4. Compute Output Innovation Residual and Update Observer State *)
FOR i := 1 TO 8 DO
    rScratchDiff := y_meas[i] - x_state[i]; (* y_meas - C*x *)
    x_state[i] := x_next[i] + (l_observer_gain[i] * rScratchDiff);
END_FOR;

(* Physical Clamping of Observer State Estimates *)
x_state[1] := MAX(0.0, MIN(110.0, x_state[1]));       (* Train Speed: 0 to 110 m/s (~396 km/h) *)
x_state[2] := MAX(0.0, MIN(120.0, x_state[2]));       (* Axle 1 Speed: 0 to 120 m/s *)
x_state[3] := MAX(0.0, MIN(120.0, x_state[3]));       (* Axle 2 Speed: 0 to 120 m/s *)
x_state[4] := MAX(0.0, MIN(300.0, x_state[4]));       (* Pantograph Force: 0 to 300 N *)
x_state[5] := MAX(1500.0, MIN(4200.0, x_state[5]));   (* DC Link Voltage: 1500 to 4200 V *)
x_state[6] := MAX(-15.0, MIN(15.0, x_state[6]));      (* Traction Torque: -15 to +15 kNm *)
x_state[7] := MAX(0.0, MIN(4.5, x_state[7]));         (* Brake Pressure: 0 to 4.5 bar *)
x_state[8] := MAX(0.02, MIN(0.42, x_state[8]));       (* Adhesion: 0.02 to 0.42 *)

(* ============================================================================================== *)
(* PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT       *)
(* Multi-Objective Quadratic Cost Functional Optimization with Actuator Box & Slew Saturation     *)
(* ============================================================================================== *)

(* 1. Define Dynamic Reference Setpoint Trajectory x_ref (8x1) *)
IF bTractionEnableCmd AND (rDriverTractionNotch_pct > 1.0) THEN
    x_ref[1] := rATOSpeedSetpoint_kmh / 3.6;
    x_ref[2] := x_ref[1];
    x_ref[3] := x_ref[1];
    x_ref[4] := rPantoTargetForce_N;
    x_ref[5] := 3000.0;
    x_ref[6] := (rDriverTractionNotch_pct / 100.0) * MOTOR_PEAK_TORQUE_KNM * 2.0;
    x_ref[7] := 0.0;
    x_ref[8] := rTheoreticalAdhesionLimit;
ELSIF bBrakingEnableCmd OR (rDriverBrakeNotch_pct > 1.0) THEN
    x_ref[1] := 0.0;
    x_ref[2] := 0.0;
    x_ref[3] := 0.0;
    x_ref[4] := rPantoTargetForce_N;
    x_ref[5] := 3000.0;
    x_ref[6] := -(rDriverBrakeNotch_pct / 100.0) * MOTOR_PEAK_TORQUE_KNM * 2.0;
    x_ref[7] := (rDriverBrakeNotch_pct / 100.0) * 3.80;
    x_ref[8] := rTheoreticalAdhesionLimit;
ELSE
    x_ref[1] := rTrainSpeed_ms;
    x_ref[2] := rTrainSpeed_ms;
    x_ref[3] := rTrainSpeed_ms;
    x_ref[4] := rPantoTargetForce_N;
    x_ref[5] := 3000.0;
    x_ref[6] := 0.0;
    x_ref[7] := 0.0;
    x_ref[8] := rTheoreticalAdhesionLimit;
END_IF;

(* 2. Define Nominal Actuator Baseline u_ref (8x1) *)
u_ref[1] := 180.0;  (* Nominal Isd* magnetizing current [A] *)
IF bTractionEnableCmd THEN
    u_ref[2] := (rDriverTractionNotch_pct / 100.0) * 450.0;
    u_ref[5] := 0.0;
    u_ref[6] := 0.0;
ELSIF bBrakingEnableCmd THEN
    u_ref[2] := -(rDriverBrakeNotch_pct / 100.0) * 450.0;
    u_ref[5] := (rDriverBrakeNotch_pct / 100.0) * 10.0;
    u_ref[6] := (rDriverBrakeNotch_pct / 100.0) * 75.0;
ELSE
    u_ref[2] := 0.0;
    u_ref[5] := 0.0;
    u_ref[6] := 0.0;
END_IF;
u_ref[3] := 85.0;   (* 4QC Modulation nominal depth [%] *)
u_ref[4] := 45.0;   (* Pantograph valve nominal [%] *)
u_ref[7] := 0.0;    (* WSSP dump nominal inactive *)
u_ref[8] := 0.0;    (* WSSP apply nominal inactive *)

(* 3. Multi-Horizon Quadratic Cost J Evaluation *)
rTotalCostFunctional := 0.0;
FOR k := 1 TO HORIZON_NP DO
    FOR i := 1 TO 8 DO
        (* State tracking quadratic penalty *)
        rScratchDiff := x_state[i] - x_ref[i];
        rTotalCostFunctional := rTotalCostFunctional + (q_diag[i] * rScratchDiff * rScratchDiff);
        (* Actuator effort quadratic penalty *)
        rScratchDiff := u_mpc_traj[k, i] - u_ref[i];
        rTotalCostFunctional := rTotalCostFunctional + (r_diag[i] * rScratchDiff * rScratchDiff);
        (* Actuator slew rate quadratic penalty *)
        IF k = 1 THEN
            rScratchDiff := u_mpc_traj[k, i] - u_prev[i];
        ELSE
            rScratchDiff := u_mpc_traj[k, i] - u_mpc_traj[k - 1, i];
        END_IF;
        rTotalCostFunctional := rTotalCostFunctional + (s_diag[i] * rScratchDiff * rScratchDiff);
    END_FOR;
END_FOR;

(* Terminal State Penalty x_N' * P * x_N *)
FOR i := 1 TO 8 DO
    rScratchDiff := x_state[i] - x_ref[i];
    rTotalCostFunctional := rTotalCostFunctional + (p_diag[i] * rScratchDiff * rScratchDiff);
END_FOR;

(* 4. Analytical Gradient Computation dJ / du_1 (8x1) *)
FOR i := 1 TO 8 DO
    (* Direct Actuator Effort and Slew Rate Derivatives *)
    grad_u[i] := (2.0 * r_diag[i] * (u_ctrl[i] - u_ref[i])) + (2.0 * s_diag[i] * (u_ctrl[i] - u_prev[i]));
    (* Back-propagated State Tracking Error through B Matrix: sum_j( 2 * B_ji * Q_j * (x_j - x_ref_j) ) *)
    rScratchAccum := 0.0;
    FOR j := 1 TO 8 DO
        rScratchAccum := rScratchAccum + (2.0 * b_mat[j, i] * q_diag[j] * (x_state[j] - x_ref[j]));
    END_FOR;
    grad_u[i] := grad_u[i] + rScratchAccum;
END_FOR;

(* 5. Projected Gradient Descent Step with Actuator Box Saturation & Slew Limiting *)
FOR i := 1 TO 8 DO
    (* Gradient Descent Step *)
    u_tentative[i] := u_ctrl[i] - (rMpcAlphaStep * grad_u[i]);
    
    (* Dynamic Actuator Slew Rate Saturation *)
    rScratchDiff := u_tentative[i] - u_prev[i];
    IF rScratchDiff > du_slew_max[i] THEN
        u_tentative[i] := u_prev[i] + du_slew_max[i];
    ELSIF rScratchDiff < -du_slew_max[i] THEN
        u_tentative[i] := u_prev[i] - du_slew_max[i];
    END_IF;
    
    (* Physical Box Constraint Saturation *)
    u_ctrl[i] := MAX(u_box_min[i], MIN(u_box_max[i], u_tentative[i]));
    u_prev[i] := u_ctrl[i];
    u_mpc_traj[1, i] := u_ctrl[i];
END_FOR;
'''
