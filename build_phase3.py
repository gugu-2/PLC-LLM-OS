# -*- coding: utf-8 -*-
"""
Generator module for Phase 3: Receding-Horizon MPC Optimization with Projected Gradient Descent
"""

def generate_phase_3():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)              *)
(* Horizons: Np = 10, Nc = 4. Quadratic Cost Functional with Physical Box & Slew Limiters        *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* Step 3.1: Dynamic Cushion Target Force Interpolation from 10-Point Profile                     *)
(* ---------------------------------------------------------------------------------------------- *)
IF OUT_VOTED_SLIDE_POSITION <= cush_depth_breakpoints[1] THEN
    cush_target_current_kn := cush_target_force_table[1];
ELSIF OUT_VOTED_SLIDE_POSITION >= cush_depth_breakpoints[10] THEN
    cush_target_current_kn := cush_target_force_table[10];
ELSE
    cush_target_current_kn := cush_target_force_table[1];
    FOR i_loop := 1 TO 9 DO
        IF (OUT_VOTED_SLIDE_POSITION >= cush_depth_breakpoints[i_loop]) AND (OUT_VOTED_SLIDE_POSITION < cush_depth_breakpoints[i_loop + 1]) THEN
            diff_temp := cush_depth_breakpoints[i_loop + 1] - cush_depth_breakpoints[i_loop];
            IF diff_temp > 0.001 THEN
                val_temp := (OUT_VOTED_SLIDE_POSITION - cush_depth_breakpoints[i_loop]) / diff_temp;
                cush_target_current_kn := cush_target_force_table[i_loop]
                    + (val_temp * (cush_target_force_table[i_loop + 1] - cush_target_force_table[i_loop]));
            END_IF;
        END_IF;
    END_FOR;
END_IF;

(* Convert Target Cushion Force [kN] to Mean Chamber Pressure Setpoint [bar] *)
(* P = (F_total / (8 * Area_m2 * 100)) + P_return *)
cush_target_press_bar := (cush_target_current_kn / (8.000000 * CONST_CUSH_BORE_AREA_M2 * 100.000)) + PT_HYD_RETURN;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 3.2: Reference Trajectory Generation Over Prediction Horizon Np = 10                     *)
(* ---------------------------------------------------------------------------------------------- *)
FOR step_idx := 1 TO 10 DO
    val_temp := TMR_CRANK_VOTED_RESULT + (INT_TO_REAL(step_idx) * 0.002000 * (SETPOINT_PRESS_SPEED_SPM * 6.000000));
    IF val_temp >= 360.000 THEN
        val_temp := val_temp - 360.000;
    END_IF;

    x_ref_trajectory[step_idx, 1] := val_temp; (* Target Crank Angle [deg] *)
    x_ref_trajectory[step_idx, 2] := kinematic_stroke_z + (INT_TO_REAL(step_idx) * 0.002000 * kinematic_velocity_vz);
    x_ref_trajectory[step_idx, 3] := kinematic_velocity_vz;
    x_ref_trajectory[step_idx, 4] := 0.000000; (* Zero Pitch Tilt Target [mm] *)
    x_ref_trajectory[step_idx, 5] := 0.000000; (* Zero Roll Tilt Target [mm] *)
    x_ref_trajectory[step_idx, 6] := cush_target_press_bar;
    x_ref_trajectory[step_idx, 7] := cush_target_current_kn;
    x_ref_trajectory[step_idx, 8] := (SETPOINT_NOMINAL_TONNAGE / CONST_FRAME_STIFFNESS_K) * 1000.000;
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 3.3: Projected Gradient Descent (PGD) Multi-Objective Optimization Loop                   *)
(* ---------------------------------------------------------------------------------------------- *)
FOR pgd_iter := 1 TO 12 DO
    (* Calculate Analytical Gradient grad_J_u across Control Horizon Nc = 4 *)
    FOR step_idx := 1 TO 4 DO
        FOR j_loop := 1 TO 5 DO
            (* Actuator Energy Penalty Term: 2 * R * u *)
            grad_J_u[step_idx, j_loop] := 2.000000 * R_WEIGHT_DIAG[j_loop] * u_opt_horizon[step_idx, j_loop];

            (* Actuator Slew Rate Penalty Term: 2 * S * (u - u_prev) *)
            IF step_idx = 1 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (2.000000 * S_WEIGHT_DIAG[j_loop] * (u_opt_horizon[step_idx, j_loop] - u_control_prev[j_loop]));
            ELSE
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (2.000000 * S_WEIGHT_DIAG[j_loop] * (u_opt_horizon[step_idx, j_loop] - u_opt_horizon[step_idx - 1, j_loop]));
            END_IF;

            (* State Error Sensitivity Back-Propagation Approximations *)
            IF j_loop = 1 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (Q_WEIGHT_DIAG[3] * (x_state_hat[3] - x_ref_trajectory[step_idx, 3]) * B_MAT[3, 1] * 0.150000);
            ELSIF j_loop = 2 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (Q_WEIGHT_DIAG[6] * (x_state_hat[6] - x_ref_trajectory[step_idx, 6]) * B_MAT[6, 2] * 0.180000);
            ELSIF j_loop = 3 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (Q_WEIGHT_DIAG[4] * (x_state_hat[4] - x_ref_trajectory[step_idx, 4]) * B_MAT[4, 3] * 0.250000);
            ELSIF j_loop = 4 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (Q_WEIGHT_DIAG[5] * (x_state_hat[5] - x_ref_trajectory[step_idx, 5]) * B_MAT[5, 4] * 0.250000);
            ELSIF j_loop = 5 THEN
                grad_J_u[step_idx, j_loop] := grad_J_u[step_idx, j_loop]
                    + (Q_WEIGHT_DIAG[6] * (x_state_hat[6] - x_ref_trajectory[step_idx, 6]) * B_MAT[6, 5] * 0.200000);
            END_IF;

            (* Projected Gradient Update Step with Step Size alpha = 0.00350 *)
            val_temp := u_opt_horizon[step_idx, j_loop] - (0.003500 * grad_J_u[step_idx, j_loop]);

            (* Box Saturation Clamping [u_box_min, u_box_max] *)
            IF val_temp > u_box_max[j_loop] THEN
                val_temp := u_box_max[j_loop];
            ELSIF val_temp < u_box_min[j_loop] THEN
                val_temp := u_box_min[j_loop];
            END_IF;

            (* Dynamic Slew Rate Clamping *)
            IF step_idx = 1 THEN
                diff_temp := val_temp - u_control_prev[j_loop];
                IF diff_temp > u_slew_max[j_loop] THEN
                    val_temp := u_control_prev[j_loop] + u_slew_max[j_loop];
                ELSIF diff_temp < -u_slew_max[j_loop] THEN
                    val_temp := u_control_prev[j_loop] - u_slew_max[j_loop];
                END_IF;
            ELSE
                diff_temp := val_temp - u_opt_horizon[step_idx - 1, j_loop];
                IF diff_temp > u_slew_max[j_loop] THEN
                    val_temp := u_opt_horizon[step_idx - 1, j_loop] + u_slew_max[j_loop];
                ELSIF diff_temp < -u_slew_max[j_loop] THEN
                    val_temp := u_opt_horizon[step_idx - 1, j_loop] - u_slew_max[j_loop];
                END_IF;
            END_IF;

            u_opt_horizon[step_idx, j_loop] := val_temp;
        END_FOR;
    END_FOR;
END_FOR;

(* ---------------------------------------------------------------------------------------------- *)
(* Step 3.4: Actuator Allocation & Individual Valve Dispatching                                   *)
(* ---------------------------------------------------------------------------------------------- *)
FOR j_loop := 1 TO 5 DO
    u_control_cmd[j_loop] := u_opt_horizon[1, j_loop];
    u_control_prev[j_loop] := u_control_cmd[j_loop];
END_FOR;

(* Allocate Primary Servo Ram Drive Commands *)
OUT_SERVO_RAM_SPEED_REF    := kinematic_velocity_vz;
OUT_SERVO_RAM_TORQUE_LIMIT := 50.000 + (u_control_cmd[1] * 0.500);

(* Dispatch Proportional Cushion Valve Commands to 8 Individual Cylinders (P1 to P8) [%] *)
OUT_CUSH_VALVE_CMD_P1 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P1_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P2 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P2_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P3 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P3_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P4 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P4_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P5 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P5_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P6 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P6_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P7 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P7_VOTED) * 0.450);
OUT_CUSH_VALVE_CMD_P8 := u_control_cmd[2] + ((cush_target_press_bar - TMR_PRESS_P8_VOTED) * 0.450);

(* Clamp 8 Cushion Valve Commands between 0% and 100% *)
IF OUT_CUSH_VALVE_CMD_P1 > 100.0 THEN OUT_CUSH_VALVE_CMD_P1 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P1 < 0.0 THEN OUT_CUSH_VALVE_CMD_P1 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P2 > 100.0 THEN OUT_CUSH_VALVE_CMD_P2 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P2 < 0.0 THEN OUT_CUSH_VALVE_CMD_P2 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P3 > 100.0 THEN OUT_CUSH_VALVE_CMD_P3 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P3 < 0.0 THEN OUT_CUSH_VALVE_CMD_P3 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P4 > 100.0 THEN OUT_CUSH_VALVE_CMD_P4 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P4 < 0.0 THEN OUT_CUSH_VALVE_CMD_P4 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P5 > 100.0 THEN OUT_CUSH_VALVE_CMD_P5 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P5 < 0.0 THEN OUT_CUSH_VALVE_CMD_P5 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P6 > 100.0 THEN OUT_CUSH_VALVE_CMD_P6 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P6 < 0.0 THEN OUT_CUSH_VALVE_CMD_P6 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P7 > 100.0 THEN OUT_CUSH_VALVE_CMD_P7 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P7 < 0.0 THEN OUT_CUSH_VALVE_CMD_P7 := 0.0; END_IF;
IF OUT_CUSH_VALVE_CMD_P8 > 100.0 THEN OUT_CUSH_VALVE_CMD_P8 := 100.0; ELSIF OUT_CUSH_VALVE_CMD_P8 < 0.0 THEN OUT_CUSH_VALVE_CMD_P8 := 0.0; END_IF;
""")
    return "".join(lines)

print("Phase 3 module loaded.")
