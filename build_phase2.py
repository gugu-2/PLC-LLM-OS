# -*- coding: utf-8 -*-
"""
Generator module for Phase 2: Mechanical Kinematics, Eccentric Tonnage & Cyber-Physical Observer
"""

def generate_phase_2():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 2: MECHANICAL KINEMATICS, ECCENTRIC TONNAGE & CYBER-PHYSICAL STATE OBSERVER             *)
(* Non-linear Slider-Crank Kinematics, 4-Corner Overturning Moments & 8x8 Luenberger Observer     *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.1: Non-Linear Mechanical Press Slider-Crank Kinematics                                 *)
(* ---------------------------------------------------------------------------------------------- *)
theta_crank_rad := TMR_CRANK_VOTED_RESULT * 0.0174532925199433; (* [deg] to [rad] *)
sin_theta  := SIN(theta_crank_rad);
cos_theta  := COS(theta_crank_rad);
sin_2theta := SIN(2.000000 * theta_crank_rad);

(* Instantaneous Angular Velocity omega = 2 * pi * SPM / 60 [rad/s] *)
omega_crank_rad_s := (SETPOINT_PRESS_SPEED_SPM * 6.283185307179586) / 60.000000;

(* Analytical Closed-Form Slider-Crank Slide Position z(theta) [mm] from TDC *)
kinematic_stroke_z := CONST_CRANK_RADIUS_RC * (1.000000 - cos_theta)
    + CONST_CONROD_LENGTH_LR * (1.000000 - SQRT(1.000000 - (CONST_LINK_RATIO_LAMBDA * CONST_LINK_RATIO_LAMBDA * sin_theta * sin_theta)));

(* Analytical Instantaneous Slide Linear Velocity v_z(theta) [mm/s] *)
kinematic_velocity_vz := omega_crank_rad_s * CONST_CRANK_RADIUS_RC * (sin_theta
    + ((CONST_LINK_RATIO_LAMBDA * sin_2theta) / (2.000000 * SQRT(1.000000 - (CONST_LINK_RATIO_LAMBDA * CONST_LINK_RATIO_LAMBDA * sin_theta * sin_theta)))));

(* Analytical Slide Linear Acceleration a_z(theta) [mm/s2] *)
kinematic_accel_az := omega_crank_rad_s * omega_crank_rad_s * CONST_CRANK_RADIUS_RC * (cos_theta
    + (CONST_LINK_RATIO_LAMBDA * COS(2.000000 * theta_crank_rad)));

(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.2: 4-Corner Strain Gauge Tonnage Summation & Eccentric Moments                         *)
(* ---------------------------------------------------------------------------------------------- *)
sum_tonnage_front := TMR_LOAD_FL_VOTED + TMR_LOAD_FR_VOTED;
sum_tonnage_rear  := TMR_LOAD_RL_VOTED + TMR_LOAD_RR_VOTED;
sum_tonnage_left  := TMR_LOAD_FL_VOTED + TMR_LOAD_RL_VOTED;
sum_tonnage_right := TMR_LOAD_FR_VOTED + TMR_LOAD_RR_VOTED;

OUT_ESTIMATED_TOTAL_TONNAGE := sum_tonnage_front + sum_tonnage_rear;
OUT_ESTIMATED_TONNAGE_FL    := TMR_LOAD_FL_VOTED;
OUT_ESTIMATED_TONNAGE_FR    := TMR_LOAD_FR_VOTED;
OUT_ESTIMATED_TONNAGE_RL    := TMR_LOAD_RL_VOTED;
OUT_ESTIMATED_TONNAGE_RR    := TMR_LOAD_RR_VOTED;

(* Structural Bed/Crown Elastic Tie-Rod Deflection delta = F / K [um] *)
IF CONST_FRAME_STIFFNESS_K > 100.0 THEN
    OUT_FRAME_ELASTIC_DEFLECTION := (OUT_ESTIMATED_TOTAL_TONNAGE / CONST_FRAME_STIFFNESS_K) * 1000.000;
ELSE
    OUT_FRAME_ELASTIC_DEFLECTION := 0.000;
END_IF;

(* Off-Center Eccentric Tonnage Centers of Force (ex, ey) & Overturning Moments (Mx, My) *)
IF OUT_ESTIMATED_TOTAL_TONNAGE > 150.000 THEN
    eccentric_offset_x_mm := ((sum_tonnage_right - sum_tonnage_left) / OUT_ESTIMATED_TOTAL_TONNAGE) * (CONST_BED_WIDTH_X * 0.500000);
    eccentric_offset_y_mm := ((sum_tonnage_front - sum_tonnage_rear) / OUT_ESTIMATED_TOTAL_TONNAGE) * (CONST_BED_DEPTH_Y * 0.500000);
    overturning_moment_mx := (sum_tonnage_front - sum_tonnage_rear) * ((CONST_BED_DEPTH_Y * 0.500000) * 0.001000);
    overturning_moment_my := (sum_tonnage_right - sum_tonnage_left) * ((CONST_BED_WIDTH_X * 0.500000) * 0.001000);
ELSE
    eccentric_offset_x_mm := 0.000;
    eccentric_offset_y_mm := 0.000;
    overturning_moment_mx := 0.000;
    overturning_moment_my := 0.000;
END_IF;

OUT_ESTIMATED_ECCENTRIC_MOMENT_X := overturning_moment_mx;
OUT_ESTIMATED_ECCENTRIC_MOMENT_Y := overturning_moment_my;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.3: Slide Parallelism Tilt Calculation & 4-Corner Hydraulic Leveling Trim PID           *)
(* ---------------------------------------------------------------------------------------------- *)
OUT_VOTED_SLIDE_POSITION := (TMR_SLIDE_FL_VOTED + TMR_SLIDE_FR_VOTED + TMR_SLIDE_RL_VOTED + TMR_SLIDE_RR_VOTED) * 0.250000;

(* Pitch Tilt: Front vs Rear Deviation [mm] *)
parallelism_tilt_pitch := ((TMR_SLIDE_FL_VOTED + TMR_SLIDE_FR_VOTED) * 0.500000) - ((TMR_SLIDE_RL_VOTED + TMR_SLIDE_RR_VOTED) * 0.500000);
(* Roll Tilt: Left vs Right Deviation [mm] *)
parallelism_tilt_roll  := ((TMR_SLIDE_FL_VOTED + TMR_SLIDE_RL_VOTED) * 0.500000) - ((TMR_SLIDE_FR_VOTED + TMR_SLIDE_RR_VOTED) * 0.500000);

OUT_SLIDE_PARALLELISM_TILT_X := parallelism_tilt_pitch;
OUT_SLIDE_PARALLELISM_TILT_Y := parallelism_tilt_roll;

(* Real-Time Active Leveling Hydraulic PID Computation *)
IF ENABLE_PARALLELISM_ACTIVE_COMP AND (OUT_ESTIMATED_TOTAL_TONNAGE > 300.000) THEN
    (* Pitch Axis Controller: Target Tilt = 0.000 mm *)
    pid_pitch_error := 0.000000 - parallelism_tilt_pitch;
    pid_pitch_integral := pid_pitch_integral + (pid_pitch_error * 0.002000);
    (* Anti-Windup Integral Clamping *)
    IF pid_pitch_integral > 0.050 THEN
        pid_pitch_integral := 0.050;
    ELSIF pid_pitch_integral < -0.050 THEN
        pid_pitch_integral := -0.050;
    END_IF;
    pid_pitch_deriv := (pid_pitch_error - pid_pitch_error_prev) / 0.002000;
    pid_pitch_error_prev := pid_pitch_error;

    pid_pitch_out := (pid_pitch_error * 450.000) + (pid_pitch_integral * 120.000) + (pid_pitch_deriv * 4.500)
        + (overturning_moment_mx * 0.035000); (* Feedforward Moment Compensation *)

    (* Roll Axis Controller: Target Tilt = 0.000 mm *)
    pid_roll_error := 0.000000 - parallelism_tilt_roll;
    pid_roll_integral := pid_roll_integral + (pid_roll_error * 0.002000);
    IF pid_roll_integral > 0.050 THEN
        pid_roll_integral := 0.050;
    ELSIF pid_roll_integral < -0.050 THEN
        pid_roll_integral := -0.050;
    END_IF;
    pid_roll_deriv := (pid_roll_error - pid_roll_error_prev) / 0.002000;
    pid_roll_error_prev := pid_roll_error;

    pid_roll_out := (pid_roll_error * 450.000) + (pid_roll_integral * 120.000) + (pid_roll_deriv * 4.500)
        + (overturning_moment_my * 0.035000);

    (* Distribute Leveling Effort to 4 Corner Trim Cylinders [%] *)
    OUT_TILT_VALVE_CMD_FL := 50.000 + (pid_pitch_out * 0.500) + (pid_roll_out * 0.500);
    OUT_TILT_VALVE_CMD_FR := 50.000 + (pid_pitch_out * 0.500) - (pid_roll_out * 0.500);
    OUT_TILT_VALVE_CMD_RL := 50.000 - (pid_pitch_out * 0.500) + (pid_roll_out * 0.500);
    OUT_TILT_VALVE_CMD_RR := 50.000 - (pid_pitch_out * 0.500) - (pid_roll_out * 0.500);
ELSE
    pid_pitch_integral := 0.000;
    pid_roll_integral  := 0.000;
    OUT_TILT_VALVE_CMD_FL := 50.000;
    OUT_TILT_VALVE_CMD_FR := 50.000;
    OUT_TILT_VALVE_CMD_RL := 50.000;
    OUT_TILT_VALVE_CMD_RR := 50.000;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.4: 8-Point Dynamic Cushion Force & Pressure Aggregation                                *)
(* ---------------------------------------------------------------------------------------------- *)
OUT_MEAN_CUSHION_PRESSURE := (TMR_PRESS_P1_VOTED + TMR_PRESS_P2_VOTED + TMR_PRESS_P3_VOTED + TMR_PRESS_P4_VOTED
    + TMR_PRESS_P5_VOTED + TMR_PRESS_P6_VOTED + TMR_PRESS_P7_VOTED + TMR_PRESS_P8_VOTED) * 0.125000;

(* Hydraulic Cushion Force = (Pressure [bar] * 100 kPa/bar * Area [m2]) [kN] per cylinder *)
OUT_TOTAL_CUSHION_FORCE := (
    (TMR_PRESS_P1_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P2_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P3_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P4_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P5_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P6_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P7_VOTED - PT_HYD_RETURN) +
    (TMR_PRESS_P8_VOTED - PT_HYD_RETURN)
) * (CONST_CUSH_BORE_AREA_M2 * 100.000);

IF OUT_TOTAL_CUSHION_FORCE < 0.000 THEN
    OUT_TOTAL_CUSHION_FORCE := 0.000;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 2.5: Cyber-Physical 8x8 Luenberger State Observer Propagation                            *)
(* ---------------------------------------------------------------------------------------------- *)
(* Formulate Current Measurement Vector y_meas *)
y_meas_vec[1] := TMR_CRANK_VOTED_RESULT;
y_meas_vec[2] := OUT_VOTED_SLIDE_POSITION;
y_meas_vec[3] := kinematic_velocity_vz;
y_meas_vec[4] := parallelism_tilt_pitch;
y_meas_vec[5] := parallelism_tilt_roll;
y_meas_vec[6] := OUT_MEAN_CUSHION_PRESSURE;
y_meas_vec[7] := OUT_TOTAL_CUSHION_FORCE;
y_meas_vec[8] := OUT_FRAME_ELASTIC_DEFLECTION;

(* 1. Explicit A*x + B*u State Prediction (64 Matrix Terms + 40 Input Terms) *)
x_state_pred[1] := (A_MAT[1,1]*x_state_hat[1] + A_MAT[1,2]*x_state_hat[2] + A_MAT[1,3]*x_state_hat[3] + A_MAT[1,4]*x_state_hat[4] + A_MAT[1,5]*x_state_hat[5] + A_MAT[1,6]*x_state_hat[6] + A_MAT[1,7]*x_state_hat[7] + A_MAT[1,8]*x_state_hat[8])
    + (B_MAT[1,1]*u_control_cmd[1] + B_MAT[1,2]*u_control_cmd[2] + B_MAT[1,3]*u_control_cmd[3] + B_MAT[1,4]*u_control_cmd[4] + B_MAT[1,5]*u_control_cmd[5]);

x_state_pred[2] := (A_MAT[2,1]*x_state_hat[1] + A_MAT[2,2]*x_state_hat[2] + A_MAT[2,3]*x_state_hat[3] + A_MAT[2,4]*x_state_hat[4] + A_MAT[2,5]*x_state_hat[5] + A_MAT[2,6]*x_state_hat[6] + A_MAT[2,7]*x_state_hat[7] + A_MAT[2,8]*x_state_hat[8])
    + (B_MAT[2,1]*u_control_cmd[1] + B_MAT[2,2]*u_control_cmd[2] + B_MAT[2,3]*u_control_cmd[3] + B_MAT[2,4]*u_control_cmd[4] + B_MAT[2,5]*u_control_cmd[5]);

x_state_pred[3] := (A_MAT[3,1]*x_state_hat[1] + A_MAT[3,2]*x_state_hat[2] + A_MAT[3,3]*x_state_hat[3] + A_MAT[3,4]*x_state_hat[4] + A_MAT[3,5]*x_state_hat[5] + A_MAT[3,6]*x_state_hat[6] + A_MAT[3,7]*x_state_hat[7] + A_MAT[3,8]*x_state_hat[8])
    + (B_MAT[3,1]*u_control_cmd[1] + B_MAT[3,2]*u_control_cmd[2] + B_MAT[3,3]*u_control_cmd[3] + B_MAT[3,4]*u_control_cmd[4] + B_MAT[3,5]*u_control_cmd[5]);

x_state_pred[4] := (A_MAT[4,1]*x_state_hat[1] + A_MAT[4,2]*x_state_hat[2] + A_MAT[4,3]*x_state_hat[3] + A_MAT[4,4]*x_state_hat[4] + A_MAT[4,5]*x_state_hat[5] + A_MAT[4,6]*x_state_hat[6] + A_MAT[4,7]*x_state_hat[7] + A_MAT[4,8]*x_state_hat[8])
    + (B_MAT[4,1]*u_control_cmd[1] + B_MAT[4,2]*u_control_cmd[2] + B_MAT[4,3]*u_control_cmd[3] + B_MAT[4,4]*u_control_cmd[4] + B_MAT[4,5]*u_control_cmd[5]);

x_state_pred[5] := (A_MAT[5,1]*x_state_hat[1] + A_MAT[5,2]*x_state_hat[2] + A_MAT[5,3]*x_state_hat[3] + A_MAT[5,4]*x_state_hat[4] + A_MAT[5,5]*x_state_hat[5] + A_MAT[5,6]*x_state_hat[6] + A_MAT[5,7]*x_state_hat[7] + A_MAT[5,8]*x_state_hat[8])
    + (B_MAT[5,1]*u_control_cmd[1] + B_MAT[5,2]*u_control_cmd[2] + B_MAT[5,3]*u_control_cmd[3] + B_MAT[5,4]*u_control_cmd[4] + B_MAT[5,5]*u_control_cmd[5]);

x_state_pred[6] := (A_MAT[6,1]*x_state_hat[1] + A_MAT[6,2]*x_state_hat[2] + A_MAT[6,3]*x_state_hat[3] + A_MAT[6,4]*x_state_hat[4] + A_MAT[6,5]*x_state_hat[5] + A_MAT[6,6]*x_state_hat[6] + A_MAT[6,7]*x_state_hat[7] + A_MAT[6,8]*x_state_hat[8])
    + (B_MAT[6,1]*u_control_cmd[1] + B_MAT[6,2]*u_control_cmd[2] + B_MAT[6,3]*u_control_cmd[3] + B_MAT[6,4]*u_control_cmd[4] + B_MAT[6,5]*u_control_cmd[5]);

x_state_pred[7] := (A_MAT[7,1]*x_state_hat[1] + A_MAT[7,2]*x_state_hat[2] + A_MAT[7,3]*x_state_hat[3] + A_MAT[7,4]*x_state_hat[4] + A_MAT[7,5]*x_state_hat[5] + A_MAT[7,6]*x_state_hat[6] + A_MAT[7,7]*x_state_hat[7] + A_MAT[7,8]*x_state_hat[8])
    + (B_MAT[7,1]*u_control_cmd[1] + B_MAT[7,2]*u_control_cmd[2] + B_MAT[7,3]*u_control_cmd[3] + B_MAT[7,4]*u_control_cmd[4] + B_MAT[7,5]*u_control_cmd[5]);

x_state_pred[8] := (A_MAT[8,1]*x_state_hat[1] + A_MAT[8,2]*x_state_hat[2] + A_MAT[8,3]*x_state_hat[3] + A_MAT[8,4]*x_state_hat[4] + A_MAT[8,5]*x_state_hat[5] + A_MAT[8,6]*x_state_hat[6] + A_MAT[8,7]*x_state_hat[7] + A_MAT[8,8]*x_state_hat[8])
    + (B_MAT[8,1]*u_control_cmd[1] + B_MAT[8,2]*u_control_cmd[2] + B_MAT[8,3]*u_control_cmd[3] + B_MAT[8,4]*u_control_cmd[4] + B_MAT[8,5]*u_control_cmd[5]);

(* 2. Explicit C*x_pred + D*u Output Prediction (64 Matrix Terms + 40 Input Terms) *)
y_pred_vec[1] := (C_MAT[1,1]*x_state_pred[1] + C_MAT[1,2]*x_state_pred[2] + C_MAT[1,3]*x_state_pred[3] + C_MAT[1,4]*x_state_pred[4] + C_MAT[1,5]*x_state_pred[5] + C_MAT[1,6]*x_state_pred[6] + C_MAT[1,7]*x_state_pred[7] + C_MAT[1,8]*x_state_pred[8])
    + (D_MAT[1,1]*u_control_cmd[1] + D_MAT[1,2]*u_control_cmd[2] + D_MAT[1,3]*u_control_cmd[3] + D_MAT[1,4]*u_control_cmd[4] + D_MAT[1,5]*u_control_cmd[5]);

y_pred_vec[2] := (C_MAT[2,1]*x_state_pred[1] + C_MAT[2,2]*x_state_pred[2] + C_MAT[2,3]*x_state_pred[3] + C_MAT[2,4]*x_state_pred[4] + C_MAT[2,5]*x_state_pred[5] + C_MAT[2,6]*x_state_pred[6] + C_MAT[2,7]*x_state_pred[7] + C_MAT[2,8]*x_state_pred[8])
    + (D_MAT[2,1]*u_control_cmd[1] + D_MAT[2,2]*u_control_cmd[2] + D_MAT[2,3]*u_control_cmd[3] + D_MAT[2,4]*u_control_cmd[4] + D_MAT[2,5]*u_control_cmd[5]);

y_pred_vec[3] := (C_MAT[3,1]*x_state_pred[1] + C_MAT[3,2]*x_state_pred[2] + C_MAT[3,3]*x_state_pred[3] + C_MAT[3,4]*x_state_pred[4] + C_MAT[3,5]*x_state_pred[5] + C_MAT[3,6]*x_state_pred[6] + C_MAT[3,7]*x_state_pred[7] + C_MAT[3,8]*x_state_pred[8])
    + (D_MAT[3,1]*u_control_cmd[1] + D_MAT[3,2]*u_control_cmd[2] + D_MAT[3,3]*u_control_cmd[3] + D_MAT[3,4]*u_control_cmd[4] + D_MAT[3,5]*u_control_cmd[5]);

y_pred_vec[4] := (C_MAT[4,1]*x_state_pred[1] + C_MAT[4,2]*x_state_pred[2] + C_MAT[4,3]*x_state_pred[3] + C_MAT[4,4]*x_state_pred[4] + C_MAT[4,5]*x_state_pred[5] + C_MAT[4,6]*x_state_pred[6] + C_MAT[4,7]*x_state_pred[7] + C_MAT[4,8]*x_state_pred[8])
    + (D_MAT[4,1]*u_control_cmd[1] + D_MAT[4,2]*u_control_cmd[2] + D_MAT[4,3]*u_control_cmd[3] + D_MAT[4,4]*u_control_cmd[4] + D_MAT[4,5]*u_control_cmd[5]);

y_pred_vec[5] := (C_MAT[5,1]*x_state_pred[1] + C_MAT[5,2]*x_state_pred[2] + C_MAT[5,3]*x_state_pred[3] + C_MAT[5,4]*x_state_pred[4] + C_MAT[5,5]*x_state_pred[5] + C_MAT[5,6]*x_state_pred[6] + C_MAT[5,7]*x_state_pred[7] + C_MAT[5,8]*x_state_pred[8])
    + (D_MAT[5,1]*u_control_cmd[1] + D_MAT[5,2]*u_control_cmd[2] + D_MAT[5,3]*u_control_cmd[3] + D_MAT[5,4]*u_control_cmd[4] + D_MAT[5,5]*u_control_cmd[5]);

y_pred_vec[6] := (C_MAT[6,1]*x_state_pred[1] + C_MAT[6,2]*x_state_pred[2] + C_MAT[6,3]*x_state_pred[3] + C_MAT[6,4]*x_state_pred[4] + C_MAT[6,5]*x_state_pred[5] + C_MAT[6,6]*x_state_pred[6] + C_MAT[6,7]*x_state_pred[7] + C_MAT[6,8]*x_state_pred[8])
    + (D_MAT[6,1]*u_control_cmd[1] + D_MAT[6,2]*u_control_cmd[2] + D_MAT[6,3]*u_control_cmd[3] + D_MAT[6,4]*u_control_cmd[4] + D_MAT[6,5]*u_control_cmd[5]);

y_pred_vec[7] := (C_MAT[7,1]*x_state_pred[1] + C_MAT[7,2]*x_state_pred[2] + C_MAT[7,3]*x_state_pred[3] + C_MAT[7,4]*x_state_pred[4] + C_MAT[7,5]*x_state_pred[5] + C_MAT[7,6]*x_state_pred[6] + C_MAT[7,7]*x_state_pred[7] + C_MAT[7,8]*x_state_pred[8])
    + (D_MAT[7,1]*u_control_cmd[1] + D_MAT[7,2]*u_control_cmd[2] + D_MAT[7,3]*u_control_cmd[3] + D_MAT[7,4]*u_control_cmd[4] + D_MAT[7,5]*u_control_cmd[5]);

y_pred_vec[8] := (C_MAT[8,1]*x_state_pred[1] + C_MAT[8,2]*x_state_pred[2] + C_MAT[8,3]*x_state_pred[3] + C_MAT[8,4]*x_state_pred[4] + C_MAT[8,5]*x_state_pred[5] + C_MAT[8,6]*x_state_pred[6] + C_MAT[8,7]*x_state_pred[7] + C_MAT[8,8]*x_state_pred[8])
    + (D_MAT[8,1]*u_control_cmd[1] + D_MAT[8,2]*u_control_cmd[2] + D_MAT[8,3]*u_control_cmd[3] + D_MAT[8,4]*u_control_cmd[4] + D_MAT[8,5]*u_control_cmd[5]);

(* 3. Innovation Calculation e = y_meas - y_pred *)
FOR i_loop := 1 TO 8 DO
    innov_vec[i_loop] := y_meas_vec[i_loop] - y_pred_vec[i_loop];
END_FOR;

(* 4. State Update x_hat = x_pred + L * innov (64 Observer Correction Terms) *)
x_state_hat[1] := x_state_pred[1] + (L_OBS[1,1]*innov_vec[1] + L_OBS[1,2]*innov_vec[2] + L_OBS[1,3]*innov_vec[3] + L_OBS[1,4]*innov_vec[4] + L_OBS[1,5]*innov_vec[5] + L_OBS[1,6]*innov_vec[6] + L_OBS[1,7]*innov_vec[7] + L_OBS[1,8]*innov_vec[8]);
x_state_hat[2] := x_state_pred[2] + (L_OBS[2,1]*innov_vec[1] + L_OBS[2,2]*innov_vec[2] + L_OBS[2,3]*innov_vec[3] + L_OBS[2,4]*innov_vec[4] + L_OBS[2,5]*innov_vec[5] + L_OBS[2,6]*innov_vec[6] + L_OBS[2,7]*innov_vec[7] + L_OBS[2,8]*innov_vec[8]);
x_state_hat[3] := x_state_pred[3] + (L_OBS[3,1]*innov_vec[1] + L_OBS[3,2]*innov_vec[2] + L_OBS[3,3]*innov_vec[3] + L_OBS[3,4]*innov_vec[4] + L_OBS[3,5]*innov_vec[5] + L_OBS[3,6]*innov_vec[6] + L_OBS[3,7]*innov_vec[7] + L_OBS[3,8]*innov_vec[8]);
x_state_hat[4] := x_state_pred[4] + (L_OBS[4,1]*innov_vec[1] + L_OBS[4,2]*innov_vec[2] + L_OBS[4,3]*innov_vec[3] + L_OBS[4,4]*innov_vec[4] + L_OBS[4,5]*innov_vec[5] + L_OBS[4,6]*innov_vec[6] + L_OBS[4,7]*innov_vec[7] + L_OBS[4,8]*innov_vec[8]);
x_state_hat[5] := x_state_pred[5] + (L_OBS[5,1]*innov_vec[1] + L_OBS[5,2]*innov_vec[2] + L_OBS[5,3]*innov_vec[3] + L_OBS[5,4]*innov_vec[4] + L_OBS[5,5]*innov_vec[5] + L_OBS[5,6]*innov_vec[6] + L_OBS[5,7]*innov_vec[7] + L_OBS[5,8]*innov_vec[8]);
x_state_hat[6] := x_state_pred[6] + (L_OBS[6,1]*innov_vec[1] + L_OBS[6,2]*innov_vec[2] + L_OBS[6,3]*innov_vec[3] + L_OBS[6,4]*innov_vec[4] + L_OBS[6,5]*innov_vec[5] + L_OBS[6,6]*innov_vec[6] + L_OBS[6,7]*innov_vec[7] + L_OBS[6,8]*innov_vec[8]);
x_state_hat[7] := x_state_pred[7] + (L_OBS[7,1]*innov_vec[1] + L_OBS[7,2]*innov_vec[2] + L_OBS[7,3]*innov_vec[3] + L_OBS[7,4]*innov_vec[4] + L_OBS[7,5]*innov_vec[5] + L_OBS[7,6]*innov_vec[6] + L_OBS[7,7]*innov_vec[7] + L_OBS[7,8]*innov_vec[8]);
x_state_hat[8] := x_state_pred[8] + (L_OBS[8,1]*innov_vec[1] + L_OBS[8,2]*innov_vec[2] + L_OBS[8,3]*innov_vec[3] + L_OBS[8,4]*innov_vec[4] + L_OBS[8,5]*innov_vec[5] + L_OBS[8,6]*innov_vec[6] + L_OBS[8,7]*innov_vec[7] + L_OBS[8,8]*innov_vec[8]);

(* Map Filtered State Observer Outputs *)
OUT_VOTED_CRANK_ANGLE      := x_state_hat[1];
OUT_ESTIMATED_RAM_VELOCITY := x_state_hat[3];
""")
    return "".join(lines)

print("Phase 2 module loaded.")
