# -*- coding: utf-8 -*-
"""
Generator module for Phase 0 to Phase 6 of FB_Mechanical_HeavyPress_ServoDieCushion_TonnageSync
"""

def generate_phase_0():
    lines = []
    lines.append("""(* ============================================================================================== *)
(* PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT FIRST-SCAN INITIALIZATION                       *)
(* ============================================================================================== *)
IF NOT bFirstScanDone THEN
    (* ------------------------------------------------------------------------------------------ *)
    (* Discrete State Transition Matrix A (8x8) at Ts = 2 ms (Sampling Frequency 500 Hz)        *)
    (* States: [theta_deg, z_pos_mm, v_ram_mms, tilt_x_mm, tilt_y_mm, p_cush_bar, f_bh_kn, def_um]*)
    (* ------------------------------------------------------------------------------------------ *)
    A_MAT[1,1] := 1.000000; A_MAT[1,2] := 0.000000; A_MAT[1,3] := 0.000000; A_MAT[1,4] := 0.000000;
    A_MAT[1,5] := 0.000000; A_MAT[1,6] := 0.000000; A_MAT[1,7] := 0.000000; A_MAT[1,8] := 0.000000;

    A_MAT[2,1] := 0.000000; A_MAT[2,2] := 1.000000; A_MAT[2,3] := 0.002000; A_MAT[2,4] := 0.000000;
    A_MAT[2,5] := 0.000000; A_MAT[2,6] := 0.000000; A_MAT[2,7] := 0.000000; A_MAT[2,8] := 0.000000;

    A_MAT[3,1] := 0.000000; A_MAT[3,2] := 0.000000; A_MAT[3,3] := 0.982500; A_MAT[3,4] := 0.000000;
    A_MAT[3,5] := 0.000000; A_MAT[3,6] := -0.000450; A_MAT[3,7] := -0.000120; A_MAT[3,8] := 0.000000;

    A_MAT[4,1] := 0.000000; A_MAT[4,2] := 0.000000; A_MAT[4,3] := 0.000000; A_MAT[4,4] := 0.965000;
    A_MAT[4,5] := 0.000000; A_MAT[4,6] := 0.000000; A_MAT[4,7] := 0.000000; A_MAT[4,8] := 0.000015;

    A_MAT[5,1] := 0.000000; A_MAT[5,2] := 0.000000; A_MAT[5,3] := 0.000000; A_MAT[5,4] := 0.000000;
    A_MAT[5,5] := 0.965000; A_MAT[5,6] := 0.000000; A_MAT[5,7] := 0.000000; A_MAT[5,8] := 0.000015;

    A_MAT[6,1] := 0.000000; A_MAT[6,2] := 0.000000; A_MAT[6,3] := 0.045000; A_MAT[6,4] := 0.000000;
    A_MAT[6,5] := 0.000000; A_MAT[6,6] := 0.978000; A_MAT[6,7] := 0.000000; A_MAT[6,8] := 0.000000;

    A_MAT[7,1] := 0.000000; A_MAT[7,2] := 0.000000; A_MAT[7,3] := 1.414000; A_MAT[7,4] := 0.000000;
    A_MAT[7,5] := 0.000000; A_MAT[7,6] := 31.41600; A_MAT[7,7] := 0.975000; A_MAT[7,8] := 0.000000;

    A_MAT[8,1] := 0.000000; A_MAT[8,2] := 0.000000; A_MAT[8,3] := 0.000000; A_MAT[8,4] := 0.000000;
    A_MAT[8,5] := 0.000000; A_MAT[8,6] := 0.000000; A_MAT[8,7] := 0.057140; A_MAT[8,8] := 0.950000;

    (* ------------------------------------------------------------------------------------------ *)
    (* Discrete Control Input Coupling Matrix B (8x5) at Ts = 2 ms                                *)
    (* Inputs: [t_ram_pct, q_cush_pct, m_bal_x_kNm, m_bal_y_kNm, x_decomp_pct]                   *)
    (* ------------------------------------------------------------------------------------------ *)
    B_MAT[1,1] := 0.001250; B_MAT[1,2] := 0.000000; B_MAT[1,3] := 0.000000; B_MAT[1,4] := 0.000000; B_MAT[1,5] := 0.000000;
    B_MAT[2,1] := 0.000450; B_MAT[2,2] := 0.000000; B_MAT[2,3] := 0.000000; B_MAT[2,4] := 0.000000; B_MAT[2,5] := 0.000000;
    B_MAT[3,1] := 0.225000; B_MAT[3,2] := -0.01500; B_MAT[3,3] := 0.000000; B_MAT[3,4] := 0.000000; B_MAT[3,5] := 0.000000;
    B_MAT[4,1] := 0.000000; B_MAT[4,2] := 0.000000; B_MAT[4,3] := 0.000850; B_MAT[4,4] := 0.000000; B_MAT[4,5] := 0.000000;
    B_MAT[5,1] := 0.000000; B_MAT[5,2] := 0.000000; B_MAT[5,3] := 0.000000; B_MAT[5,4] := 0.000850; B_MAT[5,5] := 0.000000;
    B_MAT[6,1] := 0.000000; B_MAT[6,2] := 0.350000; B_MAT[6,3] := 0.000000; B_MAT[6,4] := 0.000000; B_MAT[6,5] := -0.42000;
    B_MAT[7,1] := 0.000000; B_MAT[7,2] := 11.00000; B_MAT[7,3] := 0.000000; B_MAT[7,4] := 0.000000; B_MAT[7,5] := -13.1950;
    B_MAT[8,1] := 0.000000; B_MAT[8,2] := 0.000000; B_MAT[8,3] := 0.000000; B_MAT[8,4] := 0.000000; B_MAT[8,5] := 0.000000;

    (* ------------------------------------------------------------------------------------------ *)
    (* Discrete Measurement Mapping Matrix C (8x8)                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    C_MAT[1,1] := 1.0; C_MAT[1,2] := 0.0; C_MAT[1,3] := 0.0; C_MAT[1,4] := 0.0; C_MAT[1,5] := 0.0; C_MAT[1,6] := 0.0; C_MAT[1,7] := 0.0; C_MAT[1,8] := 0.0;
    C_MAT[2,1] := 0.0; C_MAT[2,2] := 1.0; C_MAT[2,3] := 0.0; C_MAT[2,4] := 0.0; C_MAT[2,5] := 0.0; C_MAT[2,6] := 0.0; C_MAT[2,7] := 0.0; C_MAT[2,8] := 0.0;
    C_MAT[3,1] := 0.0; C_MAT[3,2] := 0.0; C_MAT[3,3] := 1.0; C_MAT[3,4] := 0.0; C_MAT[3,5] := 0.0; C_MAT[3,6] := 0.0; C_MAT[3,7] := 0.0; C_MAT[3,8] := 0.0;
    C_MAT[4,1] := 0.0; C_MAT[4,2] := 0.0; C_MAT[4,3] := 0.0; C_MAT[4,4] := 1.0; C_MAT[4,5] := 0.0; C_MAT[4,6] := 0.0; C_MAT[4,7] := 0.0; C_MAT[4,8] := 0.0;
    C_MAT[5,1] := 0.0; C_MAT[5,2] := 0.0; C_MAT[5,3] := 0.0; C_MAT[5,4] := 0.0; C_MAT[5,5] := 1.0; C_MAT[5,6] := 0.0; C_MAT[5,7] := 0.0; C_MAT[5,8] := 0.0;
    C_MAT[6,1] := 0.0; C_MAT[6,2] := 0.0; C_MAT[6,3] := 0.0; C_MAT[6,4] := 0.0; C_MAT[6,5] := 0.0; C_MAT[6,6] := 1.0; C_MAT[6,7] := 0.0; C_MAT[6,8] := 0.0;
    C_MAT[7,1] := 0.0; C_MAT[7,2] := 0.0; C_MAT[7,3] := 0.0; C_MAT[7,4] := 0.0; C_MAT[7,5] := 0.0; C_MAT[7,6] := 0.0; C_MAT[7,7] := 1.0; C_MAT[7,8] := 0.0;
    C_MAT[8,1] := 0.0; C_MAT[8,2] := 0.0; C_MAT[8,3] := 0.0; C_MAT[8,4] := 0.0; C_MAT[8,5] := 0.0; C_MAT[8,6] := 0.0; C_MAT[8,7] := 0.0; C_MAT[8,8] := 1.0;

    (* ------------------------------------------------------------------------------------------ *)
    (* Discrete Direct Feedthrough Matrix D (8x5)                                                *)
    (* ------------------------------------------------------------------------------------------ *)
    FOR i_loop := 1 TO 8 DO
        FOR j_loop := 1 TO 5 DO
            D_MAT[i_loop, j_loop] := 0.000000;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------ *)
    (* Cyber-Physical Observer Gain Matrix L (8x8)                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    L_OBS[1,1] := 0.125000; L_OBS[1,2] := 0.000000; L_OBS[1,3] := 0.000000; L_OBS[1,4] := 0.000000; L_OBS[1,5] := 0.000000; L_OBS[1,6] := 0.000000; L_OBS[1,7] := 0.000000; L_OBS[1,8] := 0.000000;
    L_OBS[2,1] := 0.000000; L_OBS[2,2] := 0.145000; L_OBS[2,3] := 0.000000; L_OBS[2,4] := 0.000000; L_OBS[2,5] := 0.000000; L_OBS[2,6] := 0.000000; L_OBS[2,7] := 0.000000; L_OBS[2,8] := 0.000000;
    L_OBS[3,1] := 0.000000; L_OBS[3,2] := 0.000000; L_OBS[3,3] := 0.185000; L_OBS[3,4] := 0.000000; L_OBS[3,5] := 0.000000; L_OBS[3,6] := 0.000000; L_OBS[3,7] := 0.000000; L_OBS[3,8] := 0.000000;
    L_OBS[4,1] := 0.000000; L_OBS[4,2] := 0.000000; L_OBS[4,3] := 0.000000; L_OBS[4,4] := 0.220000; L_OBS[4,5] := 0.000000; L_OBS[4,6] := 0.000000; L_OBS[4,7] := 0.000000; L_OBS[4,8] := 0.000000;
    L_OBS[5,1] := 0.000000; L_OBS[5,2] := 0.000000; L_OBS[5,3] := 0.000000; L_OBS[5,4] := 0.000000; L_OBS[5,5] := 0.220000; L_OBS[5,6] := 0.000000; L_OBS[5,7] := 0.000000; L_OBS[5,8] := 0.000000;
    L_OBS[6,1] := 0.000000; L_OBS[6,2] := 0.000000; L_OBS[6,3] := 0.000000; L_OBS[6,4] := 0.000000; L_OBS[6,5] := 0.000000; L_OBS[6,6] := 0.165000; L_OBS[6,7] := 0.000000; L_OBS[6,8] := 0.000000;
    L_OBS[7,1] := 0.000000; L_OBS[7,2] := 0.000000; L_OBS[7,3] := 0.000000; L_OBS[7,4] := 0.000000; L_OBS[7,5] := 0.000000; L_OBS[7,6] := 0.000000; L_OBS[7,7] := 0.175000; L_OBS[7,8] := 0.000000;
    L_OBS[8,1] := 0.000000; L_OBS[8,2] := 0.000000; L_OBS[8,3] := 0.000000; L_OBS[8,4] := 0.000000; L_OBS[8,5] := 0.000000; L_OBS[8,6] := 0.000000; L_OBS[8,7] := 0.000000; L_OBS[8,8] := 0.110000;

    (* ------------------------------------------------------------------------------------------ *)
    (* MPC Quadratic Penalty Weights (Q, R, S, P)                                                *)
    (* ------------------------------------------------------------------------------------------ *)
    Q_WEIGHT_DIAG[1] := 1.500;  (* Crank Angle Tracking Weight *)
    Q_WEIGHT_DIAG[2] := 10.00;  (* Slide Stroke Depth Weight *)
    Q_WEIGHT_DIAG[3] := 2.500;  (* Slide Velocity Tracking Weight *)
    Q_WEIGHT_DIAG[4] := 150.0;  (* Pitch Tilt Parallelism Weight *)
    Q_WEIGHT_DIAG[5] := 150.0;  (* Roll Tilt Parallelism Weight *)
    Q_WEIGHT_DIAG[6] := 12.00;  (* Cushion Hydraulic Pressure Weight *)
    Q_WEIGHT_DIAG[7] := 0.050;  (* Blank Holder Total Force Weight *)
    Q_WEIGHT_DIAG[8] := 0.850;  (* Structural Frame Deflection Weight *)

    R_WEIGHT_DIAG[1] := 0.025;  (* Servo Drive Torque Effort Weight *)
    R_WEIGHT_DIAG[2] := 0.050;  (* Cushion Servo Valve Effort Weight *)
    R_WEIGHT_DIAG[3] := 0.200;  (* Pitch Leveling Actuator Effort Weight *)
    R_WEIGHT_DIAG[4] := 0.200;  (* Roll Leveling Actuator Effort Weight *)
    R_WEIGHT_DIAG[5] := 0.080;  (* Fast Decompression Pilot Effort Weight *)

    S_WEIGHT_DIAG[1] := 0.150;  (* Drive Torque Slew Rate Penalty *)
    S_WEIGHT_DIAG[2] := 0.250;  (* Cushion Valve Slew Rate Penalty *)
    S_WEIGHT_DIAG[3] := 0.500;  (* Pitch Leveling Slew Rate Penalty *)
    S_WEIGHT_DIAG[4] := 0.500;  (* Roll Leveling Slew Rate Penalty *)
    S_WEIGHT_DIAG[5] := 0.300;  (* Decompression Slew Rate Penalty *)

    P_WEIGHT_DIAG[1] := 3.000;
    P_WEIGHT_DIAG[2] := 25.00;
    P_WEIGHT_DIAG[3] := 5.000;
    P_WEIGHT_DIAG[4] := 300.0;
    P_WEIGHT_DIAG[5] := 300.0;
    P_WEIGHT_DIAG[6] := 25.00;
    P_WEIGHT_DIAG[7] := 0.100;
    P_WEIGHT_DIAG[8] := 1.700;

    (* Actuator Box Limits & Slew Limits *)
    u_box_min[1] := -100.0; u_box_max[1] := 100.0; u_slew_max[1] := 8.500;  (* Main Ram Torque [%] *)
    u_box_min[2] := 0.0;    u_box_max[2] := 100.0; u_slew_max[2] := 12.000; (* Cushion Valve Flow [%] *)
    u_box_min[3] := -500.0; u_box_max[3] := 500.0; u_slew_max[3] := 45.000; (* Pitch Moment Actuator [kNm] *)
    u_box_min[4] := -500.0; u_box_max[4] := 500.0; u_slew_max[4] := 45.000; (* Roll Moment Actuator [kNm] *)
    u_box_min[5] := 0.0;    u_box_max[5] := 100.0; u_slew_max[5] := 25.000; (* Decompression Valve [%] *)

    (* ------------------------------------------------------------------------------------------ *)
    (* 10-Point Dynamic Cushion Force vs. Forming Stroke Depth Lookup Table                       *)
    (* ------------------------------------------------------------------------------------------ *)
    cush_depth_breakpoints[1]  := 0.000;   cush_target_force_table[1]  := 2500.00; (* Initial Impact Grip [kN] *)
    cush_depth_breakpoints[2]  := 25.000;  cush_target_force_table[2]  := 3800.00; (* Flange Draw Ingress [kN] *)
    cush_depth_breakpoints[3]  := 50.000;  cush_target_force_table[3]  := 5200.00; (* Deep Draw Wall Transition [kN] *)
    cush_depth_breakpoints[4]  := 75.000;  cush_target_force_table[4]  := 6000.00; (* Maximum Blank Holder Clamping [kN] *)
    cush_depth_breakpoints[5]  := 100.000; cush_target_force_table[5]  := 6000.00; (* Steady Plastic Flow Stage [kN] *)
    cush_depth_breakpoints[6]  := 130.000; cush_target_force_table[6]  := 5800.00; (* Tapered Relief Drawing [kN] *)
    cush_depth_breakpoints[7]  := 160.000; cush_target_force_table[7]  := 5400.00; (* Bottom Wall Drawing [kN] *)
    cush_depth_breakpoints[8]  := 190.000; cush_target_force_table[8]  := 4800.00; (* Pre-Coining Transition [kN] *)
    cush_depth_breakpoints[9]  := 215.000; cush_target_force_table[9]  := 4200.00; (* Final Sizing Stage [kN] *)
    cush_depth_breakpoints[10] := 235.000; cush_target_force_table[10] := 3500.00; (* BDC Coining Clamp [kN] *)

    (* Reset State Estimation Vectors *)
    FOR i_loop := 1 TO 8 DO
        x_state_hat[i_loop]  := 0.000000;
        x_state_pred[i_loop] := 0.000000;
        y_meas_vec[i_loop]   := 0.000000;
        y_pred_vec[i_loop]   := 0.000000;
        innov_vec[i_loop]    := 0.000000;
    END_FOR;
    x_state_hat[6] := 15.000; (* Standby cushion pre-charge pressure [bar] *)

    FOR j_loop := 1 TO 5 DO
        u_control_cmd[j_loop]  := 0.000000;
        u_control_prev[j_loop] := 0.000000;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;
""")
    return "".join(lines)

print("Phase 0 module loaded.")
