# parts_body1.py

INIT_BLOCK = """
(* ==================================================================================================== *)
(* FIRST-SCAN CYBER-PHYSICAL STATE-SPACE & MPC MATRIX INITIALIZATION                                    *)
(* ==================================================================================================== *)
IF NOT bInitDone THEN
    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete State Transition Matrix A (10x10) for Machine Tool Dynamics at Ts = 1 ms                *)
    (* States: x1=e_x [um], x2=e_y [um], x3=e_z [um], x4=v_x [mm/s], x5=v_y [mm/s], x6=v_z [mm/s],     *)
    (*         x7=Delta_Lz [um], x8=Delta_Fpre [N], x9=F_cut [N], x10=p_aimd [mm]                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR idx_i := 1 TO 10 DO
        FOR idx_j := 1 TO 10 DO
            a_mat[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Row 1: X-Axis TCP Position Error Dynamics *)
    a_mat[1, 1] := 0.9850;   (* Servo position loop natural decay *)
    a_mat[1, 4] := 0.0010;   (* Structural vibration coupling from modal velocity x4 *)
    a_mat[1, 9] := -0.00015; (* Structural compliance deflection under cutting force x9 *)
    a_mat[1, 10]:= 0.00008;  (* Proof-mass inertial reaction coupling *)

    (* Row 2: Y-Axis TCP Position Error Dynamics *)
    a_mat[2, 2] := 0.9850;   (* Servo position loop natural decay *)
    a_mat[2, 5] := 0.0010;   (* Structural vibration coupling from modal velocity x5 *)
    a_mat[2, 9] := -0.00018; (* Structural compliance deflection under cutting force x9 *)
    a_mat[2, 10]:= 0.00008;  (* Proof-mass inertial reaction coupling *)

    (* Row 3: Z-Axis TCP Position Error Dynamics *)
    a_mat[3, 3] := 0.9880;   (* Servo position loop natural decay *)
    a_mat[3, 6] := 0.0010;   (* Vertical structural vibration coupling x6 *)
    a_mat[3, 7] := 1.0000;   (* Direct additive coupling of rotor thermal expansion x7 *)
    a_mat[3, 9] := -0.00009; (* Axial compliance deflection under cutting force x9 *)

    (* Row 4: Structural Modal Vibration Velocity X-Axis (28.5 Hz First Gantry Mode) *)
    a_mat[4, 1] := -0.4200;  (* Restoring stiffness from position displacement *)
    a_mat[4, 4] := 0.9780;   (* Modal damping ratio decay (zeta = 0.035) *)
    a_mat[4, 9] := 0.0125;   (* Dynamic cutting force regenerative excitation *)
    a_mat[4, 10]:= -0.0085;  (* Inertial damper momentum transfer *)

    (* Row 5: Structural Modal Vibration Velocity Y-Axis (42.0 Hz Ram Bending Mode) *)
    a_mat[5, 2] := -0.5800;  (* Restoring stiffness from position displacement *)
    a_mat[5, 5] := 0.9720;   (* Modal damping ratio decay (zeta = 0.042) *)
    a_mat[5, 9] := 0.0140;   (* Dynamic cutting force regenerative excitation *)
    a_mat[5, 10]:= -0.0092;  (* Inertial damper momentum transfer *)

    (* Row 6: Structural Modal Vibration Velocity Z-Axis (65.0 Hz Axial Column Mode) *)
    a_mat[6, 3] := -0.8500;  (* Axial column stiffness restoration *)
    a_mat[6, 6] := 0.9650;   (* High axial modal damping *)
    a_mat[6, 9] := 0.0085;   (* Dynamic thrust cutting force excitation *)

    (* Row 7: Spindle Rotor Axial Thermal Growth Delta_Lz [um] (Dominant tau = 850 s) *)
    a_mat[7, 7] := 0.999988; (* Continuous thermal dissipation decay exp(-Ts/tau) *)
    a_mat[7, 8] := 0.000015; (* Preload thermo-elastic cross-coupling *)

    (* Row 8: Front Bearing Dynamic Preload Variation [N] (Dominant tau = 120 s) *)
    a_mat[8, 8] := 0.999915; (* Preload differential temperature relaxation *)
    a_mat[8, 7] := 0.00025;  (* Shaft elongation induced axial contact stress *)

    (* Row 9: Reconstructed Dynamic Cutting Force Vector [N] *)
    a_mat[9, 4] := 1.2500;   (* Regenerative chip thickness inner surface modulation *)
    a_mat[9, 5] := 1.4500;   (* Regenerative chip thickness outer surface modulation *)
    a_mat[9, 9] := 0.9200;   (* Dynamic cutting force autoregressive persistence *)

    (* Row 10: Active Inertial Damper Proof-Mass Position [mm] *)
    a_mat[10, 4] := 0.0012;  (* Mechanical motion integration *)
    a_mat[10, 10]:= 0.9910;  (* Damper centering spring-damper restoration *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Discrete Input Coupling Matrix B (10x6)                                                          *)
    (* Inputs: u1=F_damp_x [N], u2=F_damp_y [N], u3=F_piezo_z [N], u4=Delta_z_comp [um],               *)
    (*         u5=Feed_Override [%], u6=Chiller_Flow [%]                                                *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR idx_i := 1 TO 10 DO
        FOR idx_j := 1 TO 6 DO
            b_mat[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    b_mat[1, 1] := -0.000045; (* X-axis position response to damper force *)
    b_mat[2, 2] := -0.000048; (* Y-axis position response to damper force *)
    b_mat[3, 3] := -0.000025; (* Z-axis position response to piezo force *)
    b_mat[3, 4] := -1.000000; (* Direct feedforward thermal offset cancellation *)
    
    b_mat[4, 1] := -0.001420; (* X structural velocity damping from voice-coil actuator *)
    b_mat[5, 2] := -0.001550; (* Y structural velocity damping from voice-coil actuator *)
    b_mat[6, 3] := -0.000850; (* Z structural velocity damping from high-force piezo *)
    
    b_mat[7, 6] := -0.000082; (* Chiller flow rate reduction of rotor thermal elongation *)
    b_mat[8, 6] := -0.000145; (* Chiller flow rate reduction of bearing preload stress *)
    
    b_mat[9, 5] := 2.500000;  (* Cutting force dependence on feedrate override percentage *)
    b_mat[10, 1]:= 0.000650;  (* Proof-mass displacement response to voice-coil drive *)
    b_mat[10, 2]:= 0.000650;  (* Proof-mass displacement response to voice-coil drive *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* State Output Matrix C (10x10) and Direct Feedthrough Matrix D (10x6)                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    FOR idx_i := 1 TO 10 DO
        FOR idx_j := 1 TO 10 DO
            IF idx_i = idx_j THEN
                c_mat[idx_i, idx_j] := 1.0;
            ELSE
                c_mat[idx_i, idx_j] := 0.0;
            END_IF;
        END_FOR;
        FOR idx_j := 1 TO 6 DO
            d_mat[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------------------ *)
    (* Luenberger Observer Gains K_obs (10)                                                             *)
    (* ------------------------------------------------------------------------------------------------ *)
    k_obs[1] := 0.220; (* Position X innovation gain *)
    k_obs[2] := 0.220; (* Position Y innovation gain *)
    k_obs[3] := 0.250; (* Position Z innovation gain *)
    k_obs[4] := 0.180; (* Velocity X modal innovation gain *)
    k_obs[5] := 0.180; (* Velocity Y modal innovation gain *)
    k_obs[6] := 0.190; (* Velocity Z modal innovation gain *)
    k_obs[7] := 0.085; (* Rotor thermal growth innovation gain *)
    k_obs[8] := 0.065; (* Bearing preload innovation gain *)
    k_obs[9] := 0.320; (* Cutting force observer innovation gain *)
    k_obs[10]:= 0.150; (* Proof-mass displacement innovation gain *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* MPC Quadratic Cost Weighting Matrices (Q, R, S, P)                                               *)
    (* ------------------------------------------------------------------------------------------------ *)
    q_diag[1] := 150.0;  (* Penality on X position error [um] *)
    q_diag[2] := 150.0;  (* Penality on Y position error [um] *)
    q_diag[3] := 250.0;  (* Penality on Z position error [um] *)
    q_diag[4] := 80.0;   (* Penality on X structural vibration velocity *)
    q_diag[5] := 85.0;   (* Penality on Y structural vibration velocity *)
    q_diag[6] := 95.0;   (* Penality on Z structural vibration velocity *)
    q_diag[7] := 180.0;  (* Penality on uncompensated thermal growth *)
    q_diag[8] := 45.0;   (* Penality on excessive bearing preload deviation *)
    q_diag[9] := 25.0;   (* Penality on cutting force fluctuation *)
    q_diag[10]:= 12.0;   (* Penality on proof-mass excursion *)

    r_diag[1] := 0.045;  (* Penality on X active damper voice-coil force *)
    r_diag[2] := 0.045;  (* Penality on Y active damper voice-coil force *)
    r_diag[3] := 0.065;  (* Penality on Z active piezo stack force *)
    r_diag[4] := 0.020;  (* Penality on thermal compensation offset authority *)
    r_diag[5] := 0.120;  (* Penality on cutting feedrate override throttling *)
    r_diag[6] := 0.015;  (* Penality on chiller valve modulation *)

    s_diag[1] := 0.085;  (* Slew rate penalty on X voice-coil actuator *)
    s_diag[2] := 0.085;  (* Slew rate penalty on Y voice-coil actuator *)
    s_diag[3] := 0.110;  (* Slew rate penalty on Z piezo actuator *)
    s_diag[4] := 0.050;  (* Slew rate penalty on thermal offset rate of change *)
    s_diag[5] := 0.250;  (* Slew rate penalty on feedrate override jump *)
    s_diag[6] := 0.035;  (* Slew rate penalty on chiller flow valve hunting *)

    p_diag[1] := 320.0;  (* Terminal penalty X position *)
    p_diag[2] := 320.0;  (* Terminal penalty Y position *)
    p_diag[3] := 480.0;  (* Terminal penalty Z position *)
    p_diag[4] := 160.0;  (* Terminal penalty X vibration *)
    p_diag[5] := 170.0;  (* Terminal penalty Y vibration *)
    p_diag[6] := 190.0;  (* Terminal penalty Z vibration *)
    p_diag[7] := 350.0;  (* Terminal penalty thermal expansion *)
    p_diag[8] := 90.0;   (* Terminal penalty bearing preload *)
    p_diag[9] := 50.0;   (* Terminal penalty cutting force *)
    p_diag[10]:= 25.0;   (* Terminal penalty proof-mass excursion *)

    (* ------------------------------------------------------------------------------------------------ *)
    (* Actuator Box Saturation Constraints & Maximum Slew Limits                                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    u_box_min[1] := -450.0;  u_box_max[1] := 450.0;   du_slew_max[1] := 85.0;   (* X Damper: +/-450 N *)
    u_box_min[2] := -450.0;  u_box_max[2] := 450.0;   du_slew_max[2] := 85.0;   (* Y Damper: +/-450 N *)
    u_box_min[3] := -800.0;  u_box_max[3] := 800.0;   du_slew_max[3] := 140.0;  (* Z Piezo: +/-800 N *)
    u_box_min[4] := -150.0;  u_box_max[4] := 150.0;   du_slew_max[4] := 1.50;   (* Thermal Comp: +/-150 um *)
    u_box_min[5] := 20.0;    u_box_max[5] := 120.0;   du_slew_max[5] := 2.50;   (* Feed Override: 20-120% *)
    u_box_min[6] := 0.0;     u_box_max[6] := 100.0;   du_slew_max[6] := 5.00;   (* Chiller Valve: 0-100% *)

    (* Initialize state and actuator histories *)
    FOR idx_i := 1 TO 10 DO
        x_state[idx_i] := 0.0;
        x_next[idx_i] := 0.0;
        x_ref[idx_i] := 0.0;
    END_FOR;
    FOR idx_j := 1 TO 6 DO
        u_ctrl[idx_j] := 0.0;
        u_ref[idx_j] := 0.0;
        u_prev[idx_j] := 0.0;
        FOR idx_k := 1 TO 5 DO
            u_mpc_traj[idx_k, idx_j] := 0.0;
        END_FOR;
    END_FOR;
    u_ref[5] := 100.0; (* Nominal feedrate override 100% *)
    u_ref[6] := 50.0;  (* Nominal chiller valve 50% *)

    bInitDone := TRUE;
END_IF;
"""

PHASE1_TMR_BLOCK = """
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT ISOLATION WITH DISCREPANCY TIMERS       *)
(* ==================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.1: Gantry X-Axis Optical Linear Scale Triplet (Master / Slave Reference)                           *)
(* ---------------------------------------------------------------------------------------------------- *)
rX_Delta_AB := ABS(rLinearScale_X_ChA_mm - rLinearScale_X_ChB_mm);
rX_Delta_BC := ABS(rLinearScale_X_ChB_mm - rLinearScale_X_ChC_mm);
rX_Delta_CA := ABS(rLinearScale_X_ChC_mm - rLinearScale_X_ChA_mm);

IF (rX_Delta_AB > rX_DiscLimit_mm) OR (rX_Delta_BC > rX_DiscLimit_mm) OR (rX_Delta_CA > rX_DiscLimit_mm) THEN
    rX_DiscTimer_s := rX_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rX_DiscTimer_s > 0.0 THEN
        rX_DiscTimer_s := rX_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rX_DiscTimer_s < 0.0 THEN
            rX_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rX_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rX_Delta_AB > rX_DiscLimit_mm) AND (rX_Delta_CA > rX_DiscLimit_mm) THEN
        bX_ChA_Valid := FALSE;
    ELSIF (rX_Delta_AB > rX_DiscLimit_mm) AND (rX_Delta_BC > rX_DiscLimit_mm) THEN
        bX_ChB_Valid := FALSE;
    ELSIF (rX_Delta_BC > rX_DiscLimit_mm) AND (rX_Delta_CA > rX_DiscLimit_mm) THEN
        bX_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bX_ChA_Valid := TRUE;
    bX_ChB_Valid := TRUE;
    bX_ChC_Valid := TRUE;
    rX_DiscTimer_s := 0.0;
END_IF;

IF bX_ChA_Valid AND bX_ChB_Valid AND bX_ChC_Valid THEN
    nX_VotingMode := 3;
    IF (rLinearScale_X_ChA_mm >= rLinearScale_X_ChB_mm AND rLinearScale_X_ChA_mm <= rLinearScale_X_ChC_mm) OR
       (rLinearScale_X_ChA_mm <= rLinearScale_X_ChB_mm AND rLinearScale_X_ChA_mm >= rLinearScale_X_ChC_mm) THEN
        rVotedPos_X_mm := rLinearScale_X_ChA_mm;
    ELSIF (rLinearScale_X_ChB_mm >= rLinearScale_X_ChA_mm AND rLinearScale_X_ChB_mm <= rLinearScale_X_ChC_mm) OR
          (rLinearScale_X_ChB_mm <= rLinearScale_X_ChA_mm AND rLinearScale_X_ChB_mm >= rLinearScale_X_ChC_mm) THEN
        rVotedPos_X_mm := rLinearScale_X_ChB_mm;
    ELSE
        rVotedPos_X_mm := rLinearScale_X_ChC_mm;
    END_IF;
ELSIF bX_ChA_Valid AND bX_ChB_Valid THEN
    nX_VotingMode := 2;
    rVotedPos_X_mm := 0.5 * (rLinearScale_X_ChA_mm + rLinearScale_X_ChB_mm);
ELSIF bX_ChB_Valid AND bX_ChC_Valid THEN
    nX_VotingMode := 2;
    rVotedPos_X_mm := 0.5 * (rLinearScale_X_ChB_mm + rLinearScale_X_ChC_mm);
ELSIF bX_ChA_Valid AND bX_ChC_Valid THEN
    nX_VotingMode := 2;
    rVotedPos_X_mm := 0.5 * (rLinearScale_X_ChA_mm + rLinearScale_X_ChC_mm);
ELSIF bX_ChA_Valid THEN
    nX_VotingMode := 1;
    rVotedPos_X_mm := rLinearScale_X_ChA_mm;
ELSIF bX_ChB_Valid THEN
    nX_VotingMode := 1;
    rVotedPos_X_mm := rLinearScale_X_ChB_mm;
ELSIF bX_ChC_Valid THEN
    nX_VotingMode := 1;
    rVotedPos_X_mm := rLinearScale_X_ChC_mm;
ELSE
    nX_VotingMode := 0;
    rVotedPos_X_mm := rX_Filt_mm;
END_IF;

rX_Filt_mm := rX_Filt_mm + TMR_FILTER_ALPHA * (rVotedPos_X_mm - rX_Filt_mm);
rVotedPos_X_mm := rX_Filt_mm;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.2: Crossbeam Y-Axis Optical Linear Scale Triplet                                                   *)
(* ---------------------------------------------------------------------------------------------------- *)
rY_Delta_AB := ABS(rLinearScale_Y_ChA_mm - rLinearScale_Y_ChB_mm);
rY_Delta_BC := ABS(rLinearScale_Y_ChB_mm - rLinearScale_Y_ChC_mm);
rY_Delta_CA := ABS(rLinearScale_Y_ChC_mm - rLinearScale_Y_ChA_mm);

IF (rY_Delta_AB > rY_DiscLimit_mm) OR (rY_Delta_BC > rY_DiscLimit_mm) OR (rY_Delta_CA > rY_DiscLimit_mm) THEN
    rY_DiscTimer_s := rY_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rY_DiscTimer_s > 0.0 THEN
        rY_DiscTimer_s := rY_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rY_DiscTimer_s < 0.0 THEN
            rY_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rY_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rY_Delta_AB > rY_DiscLimit_mm) AND (rY_Delta_CA > rY_DiscLimit_mm) THEN
        bY_ChA_Valid := FALSE;
    ELSIF (rY_Delta_AB > rY_DiscLimit_mm) AND (rY_Delta_BC > rY_DiscLimit_mm) THEN
        bY_ChB_Valid := FALSE;
    ELSIF (rY_Delta_BC > rY_DiscLimit_mm) AND (rY_Delta_CA > rY_DiscLimit_mm) THEN
        bY_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bY_ChA_Valid := TRUE;
    bY_ChB_Valid := TRUE;
    bY_ChC_Valid := TRUE;
    rY_DiscTimer_s := 0.0;
END_IF;

IF bY_ChA_Valid AND bY_ChB_Valid AND bY_ChC_Valid THEN
    nY_VotingMode := 3;
    IF (rLinearScale_Y_ChA_mm >= rLinearScale_Y_ChB_mm AND rLinearScale_Y_ChA_mm <= rLinearScale_Y_ChC_mm) OR
       (rLinearScale_Y_ChA_mm <= rLinearScale_Y_ChB_mm AND rLinearScale_Y_ChA_mm >= rLinearScale_Y_ChC_mm) THEN
        rVotedPos_Y_mm := rLinearScale_Y_ChA_mm;
    ELSIF (rLinearScale_Y_ChB_mm >= rLinearScale_Y_ChA_mm AND rLinearScale_Y_ChB_mm <= rLinearScale_Y_ChC_mm) OR
          (rLinearScale_Y_ChB_mm <= rLinearScale_Y_ChA_mm AND rLinearScale_Y_ChB_mm >= rLinearScale_Y_ChC_mm) THEN
        rVotedPos_Y_mm := rLinearScale_Y_ChB_mm;
    ELSE
        rVotedPos_Y_mm := rLinearScale_Y_ChC_mm;
    END_IF;
ELSIF bY_ChA_Valid AND bY_ChB_Valid THEN
    nY_VotingMode := 2;
    rVotedPos_Y_mm := 0.5 * (rLinearScale_Y_ChA_mm + rLinearScale_Y_ChB_mm);
ELSIF bY_ChB_Valid AND bY_ChC_Valid THEN
    nY_VotingMode := 2;
    rVotedPos_Y_mm := 0.5 * (rLinearScale_Y_ChB_mm + rLinearScale_Y_ChC_mm);
ELSIF bY_ChA_Valid AND bY_ChC_Valid THEN
    nY_VotingMode := 2;
    rVotedPos_Y_mm := 0.5 * (rLinearScale_Y_ChA_mm + rLinearScale_Y_ChC_mm);
ELSIF bY_ChA_Valid THEN
    nY_VotingMode := 1;
    rVotedPos_Y_mm := rLinearScale_Y_ChA_mm;
ELSIF bY_ChB_Valid THEN
    nY_VotingMode := 1;
    rVotedPos_Y_mm := rLinearScale_Y_ChB_mm;
ELSIF bY_ChC_Valid THEN
    nY_VotingMode := 1;
    rVotedPos_Y_mm := rLinearScale_Y_ChC_mm;
ELSE
    nY_VotingMode := 0;
    rVotedPos_Y_mm := rY_Filt_mm;
END_IF;

rY_Filt_mm := rY_Filt_mm + TMR_FILTER_ALPHA * (rVotedPos_Y_mm - rY_Filt_mm);
rVotedPos_Y_mm := rY_Filt_mm;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.3: Ram Z-Axis Optical Linear Scale Triplet                                                         *)
(* ---------------------------------------------------------------------------------------------------- *)
rZ_Delta_AB := ABS(rLinearScale_Z_ChA_mm - rLinearScale_Z_ChB_mm);
rZ_Delta_BC := ABS(rLinearScale_Z_ChB_mm - rLinearScale_Z_ChC_mm);
rZ_Delta_CA := ABS(rLinearScale_Z_ChC_mm - rLinearScale_Z_ChA_mm);

IF (rZ_Delta_AB > rZ_DiscLimit_mm) OR (rZ_Delta_BC > rZ_DiscLimit_mm) OR (rZ_Delta_CA > rZ_DiscLimit_mm) THEN
    rZ_DiscTimer_s := rZ_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rZ_DiscTimer_s > 0.0 THEN
        rZ_DiscTimer_s := rZ_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rZ_DiscTimer_s < 0.0 THEN
            rZ_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rZ_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rZ_Delta_AB > rZ_DiscLimit_mm) AND (rZ_Delta_CA > rZ_DiscLimit_mm) THEN
        bZ_ChA_Valid := FALSE;
    ELSIF (rZ_Delta_AB > rZ_DiscLimit_mm) AND (rZ_Delta_BC > rZ_DiscLimit_mm) THEN
        bZ_ChB_Valid := FALSE;
    ELSIF (rZ_Delta_BC > rZ_DiscLimit_mm) AND (rZ_Delta_CA > rZ_DiscLimit_mm) THEN
        bZ_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bZ_ChA_Valid := TRUE;
    bZ_ChB_Valid := TRUE;
    bZ_ChC_Valid := TRUE;
    rZ_DiscTimer_s := 0.0;
END_IF;

IF bZ_ChA_Valid AND bZ_ChB_Valid AND bZ_ChC_Valid THEN
    nZ_VotingMode := 3;
    IF (rLinearScale_Z_ChA_mm >= rLinearScale_Z_ChB_mm AND rLinearScale_Z_ChA_mm <= rLinearScale_Z_ChC_mm) OR
       (rLinearScale_Z_ChA_mm <= rLinearScale_Z_ChB_mm AND rLinearScale_Z_ChA_mm >= rLinearScale_Z_ChC_mm) THEN
        rVotedPos_Z_mm := rLinearScale_Z_ChA_mm;
    ELSIF (rLinearScale_Z_ChB_mm >= rLinearScale_Z_ChA_mm AND rLinearScale_Z_ChB_mm <= rLinearScale_Z_ChC_mm) OR
          (rLinearScale_Z_ChB_mm <= rLinearScale_Z_ChA_mm AND rLinearScale_Z_ChB_mm >= rLinearScale_Z_ChC_mm) THEN
        rVotedPos_Z_mm := rLinearScale_Z_ChB_mm;
    ELSE
        rVotedPos_Z_mm := rLinearScale_Z_ChC_mm;
    END_IF;
ELSIF bZ_ChA_Valid AND bZ_ChB_Valid THEN
    nZ_VotingMode := 2;
    rVotedPos_Z_mm := 0.5 * (rLinearScale_Z_ChA_mm + rLinearScale_Z_ChB_mm);
ELSIF bZ_ChB_Valid AND bZ_ChC_Valid THEN
    nZ_VotingMode := 2;
    rVotedPos_Z_mm := 0.5 * (rLinearScale_Z_ChB_mm + rLinearScale_Z_ChC_mm);
ELSIF bZ_ChA_Valid AND bZ_ChC_Valid THEN
    nZ_VotingMode := 2;
    rVotedPos_Z_mm := 0.5 * (rLinearScale_Z_ChA_mm + rLinearScale_Z_ChC_mm);
ELSIF bZ_ChA_Valid THEN
    nZ_VotingMode := 1;
    rVotedPos_Z_mm := rLinearScale_Z_ChA_mm;
ELSIF bZ_ChB_Valid THEN
    nZ_VotingMode := 1;
    rVotedPos_Z_mm := rLinearScale_Z_ChB_mm;
ELSIF bZ_ChC_Valid THEN
    nZ_VotingMode := 1;
    rVotedPos_Z_mm := rLinearScale_Z_ChC_mm;
ELSE
    nZ_VotingMode := 0;
    rVotedPos_Z_mm := rZ_Filt_mm;
END_IF;

rZ_Filt_mm := rZ_Filt_mm + TMR_FILTER_ALPHA * (rVotedPos_Z_mm - rZ_Filt_mm);
rVotedPos_Z_mm := rZ_Filt_mm;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.4: Spindle Rotary Speed Magnetic Ring Encoder Triplet                                              *)
(* ---------------------------------------------------------------------------------------------------- *)
rSpd_Delta_AB := ABS(rSpindleRotSpeed_ChA_rpm - rSpindleRotSpeed_ChB_rpm);
rSpd_Delta_BC := ABS(rSpindleRotSpeed_ChB_rpm - rSpindleRotSpeed_ChC_rpm);
rSpd_Delta_CA := ABS(rSpindleRotSpeed_ChC_rpm - rSpindleRotSpeed_ChA_rpm);

IF (rSpd_Delta_AB > rSpd_DiscLimit_rpm) OR (rSpd_Delta_BC > rSpd_DiscLimit_rpm) OR (rSpd_Delta_CA > rSpd_DiscLimit_rpm) THEN
    rSpd_DiscTimer_s := rSpd_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rSpd_DiscTimer_s > 0.0 THEN
        rSpd_DiscTimer_s := rSpd_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rSpd_DiscTimer_s < 0.0 THEN
            rSpd_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rSpd_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rSpd_Delta_AB > rSpd_DiscLimit_rpm) AND (rSpd_Delta_CA > rSpd_DiscLimit_rpm) THEN
        bSpd_ChA_Valid := FALSE;
    ELSIF (rSpd_Delta_AB > rSpd_DiscLimit_rpm) AND (rSpd_Delta_BC > rSpd_DiscLimit_rpm) THEN
        bSpd_ChB_Valid := FALSE;
    ELSIF (rSpd_Delta_BC > rSpd_DiscLimit_rpm) AND (rSpd_Delta_CA > rSpd_DiscLimit_rpm) THEN
        bSpd_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bSpd_ChA_Valid := TRUE;
    bSpd_ChB_Valid := TRUE;
    bSpd_ChC_Valid := TRUE;
    rSpd_DiscTimer_s := 0.0;
END_IF;

IF bSpd_ChA_Valid AND bSpd_ChB_Valid AND bSpd_ChC_Valid THEN
    nSpd_VotingMode := 3;
    IF (rSpindleRotSpeed_ChA_rpm >= rSpindleRotSpeed_ChB_rpm AND rSpindleRotSpeed_ChA_rpm <= rSpindleRotSpeed_ChC_rpm) OR
       (rSpindleRotSpeed_ChA_rpm <= rSpindleRotSpeed_ChB_rpm AND rSpindleRotSpeed_ChA_rpm >= rSpindleRotSpeed_ChC_rpm) THEN
        rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChA_rpm;
    ELSIF (rSpindleRotSpeed_ChB_rpm >= rSpindleRotSpeed_ChA_rpm AND rSpindleRotSpeed_ChB_rpm <= rSpindleRotSpeed_ChC_rpm) OR
          (rSpindleRotSpeed_ChB_rpm <= rSpindleRotSpeed_ChA_rpm AND rSpindleRotSpeed_ChB_rpm >= rSpindleRotSpeed_ChC_rpm) THEN
        rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChB_rpm;
    ELSE
        rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChC_rpm;
    END_IF;
ELSIF bSpd_ChA_Valid AND bSpd_ChB_Valid THEN
    nSpd_VotingMode := 2;
    rVotedSpindleSpeed_rpm := 0.5 * (rSpindleRotSpeed_ChA_rpm + rSpindleRotSpeed_ChB_rpm);
ELSIF bSpd_ChB_Valid AND bSpd_ChC_Valid THEN
    nSpd_VotingMode := 2;
    rVotedSpindleSpeed_rpm := 0.5 * (rSpindleRotSpeed_ChB_rpm + rSpindleRotSpeed_ChC_rpm);
ELSIF bSpd_ChA_Valid AND bSpd_ChC_Valid THEN
    nSpd_VotingMode := 2;
    rVotedSpindleSpeed_rpm := 0.5 * (rSpindleRotSpeed_ChA_rpm + rSpindleRotSpeed_ChC_rpm);
ELSIF bSpd_ChA_Valid THEN
    nSpd_VotingMode := 1;
    rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChA_rpm;
ELSIF bSpd_ChB_Valid THEN
    nSpd_VotingMode := 1;
    rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChB_rpm;
ELSIF bSpd_ChC_Valid THEN
    nSpd_VotingMode := 1;
    rVotedSpindleSpeed_rpm := rSpindleRotSpeed_ChC_rpm;
ELSE
    nSpd_VotingMode := 0;
    rVotedSpindleSpeed_rpm := rSpd_Filt_rpm;
END_IF;

rSpd_Filt_rpm := rSpd_Filt_rpm + TMR_FILTER_ALPHA * (rVotedSpindleSpeed_rpm - rSpd_Filt_rpm);
rVotedSpindleSpeed_rpm := rSpd_Filt_rpm;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.5: Spindle Rotor Angular Orientation Triplet                                                      *)
(* ---------------------------------------------------------------------------------------------------- *)
rAng_Delta_AB := ABS(rSpindleRotAngle_ChA_deg - rSpindleRotAngle_ChB_deg);
rAng_Delta_BC := ABS(rSpindleRotAngle_ChB_deg - rSpindleRotAngle_ChC_deg);
rAng_Delta_CA := ABS(rSpindleRotAngle_ChC_deg - rSpindleRotAngle_ChA_deg);

IF (rAng_Delta_AB > rAng_DiscLimit_deg) OR (rAng_Delta_BC > rAng_DiscLimit_deg) OR (rAng_Delta_CA > rAng_DiscLimit_deg) THEN
    rAng_DiscTimer_s := rAng_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rAng_DiscTimer_s > 0.0 THEN
        rAng_DiscTimer_s := rAng_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rAng_DiscTimer_s < 0.0 THEN
            rAng_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rAng_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rAng_Delta_AB > rAng_DiscLimit_deg) AND (rAng_Delta_CA > rAng_DiscLimit_deg) THEN
        bAng_ChA_Valid := FALSE;
    ELSIF (rAng_Delta_AB > rAng_DiscLimit_deg) AND (rAng_Delta_BC > rAng_DiscLimit_deg) THEN
        bAng_ChB_Valid := FALSE;
    ELSIF (rAng_Delta_BC > rAng_DiscLimit_deg) AND (rAng_Delta_CA > rAng_DiscLimit_deg) THEN
        bAng_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bAng_ChA_Valid := TRUE;
    bAng_ChB_Valid := TRUE;
    bAng_ChC_Valid := TRUE;
    rAng_DiscTimer_s := 0.0;
END_IF;

IF bAng_ChA_Valid AND bAng_ChB_Valid AND bAng_ChC_Valid THEN
    nAng_VotingMode := 3;
    IF (rSpindleRotAngle_ChA_deg >= rSpindleRotAngle_ChB_deg AND rSpindleRotAngle_ChA_deg <= rSpindleRotAngle_ChC_deg) OR
       (rSpindleRotAngle_ChA_deg <= rSpindleRotAngle_ChB_deg AND rSpindleRotAngle_ChA_deg >= rSpindleRotAngle_ChC_deg) THEN
        rVotedSpindleAngle_deg := rSpindleRotAngle_ChA_deg;
    ELSIF (rSpindleRotAngle_ChB_deg >= rSpindleRotAngle_ChA_deg AND rSpindleRotAngle_ChB_deg <= rSpindleRotAngle_ChC_deg) OR
          (rSpindleRotAngle_ChB_deg <= rSpindleRotAngle_ChA_deg AND rSpindleRotAngle_ChB_deg >= rSpindleRotAngle_ChC_deg) THEN
        rVotedSpindleAngle_deg := rSpindleRotAngle_ChB_deg;
    ELSE
        rVotedSpindleAngle_deg := rSpindleRotAngle_ChC_deg;
    END_IF;
ELSIF bAng_ChA_Valid AND bAng_ChB_Valid THEN
    nAng_VotingMode := 2;
    rVotedSpindleAngle_deg := 0.5 * (rSpindleRotAngle_ChA_deg + rSpindleRotAngle_ChB_deg);
ELSIF bAng_ChB_Valid AND bAng_ChC_Valid THEN
    nAng_VotingMode := 2;
    rVotedSpindleAngle_deg := 0.5 * (rSpindleRotAngle_ChB_deg + rSpindleRotAngle_ChC_deg);
ELSIF bAng_ChA_Valid AND bAng_ChC_Valid THEN
    nAng_VotingMode := 2;
    rVotedSpindleAngle_deg := 0.5 * (rSpindleRotAngle_ChA_deg + rSpindleRotAngle_ChC_deg);
ELSIF bAng_ChA_Valid THEN
    nAng_VotingMode := 1;
    rVotedSpindleAngle_deg := rSpindleRotAngle_ChA_deg;
ELSIF bAng_ChB_Valid THEN
    nAng_VotingMode := 1;
    rVotedSpindleAngle_deg := rSpindleRotAngle_ChB_deg;
ELSIF bAng_ChC_Valid THEN
    nAng_VotingMode := 1;
    rVotedSpindleAngle_deg := rSpindleRotAngle_ChC_deg;
ELSE
    nAng_VotingMode := 0;
    rVotedSpindleAngle_deg := rAng_Filt_deg;
END_IF;

rAng_Filt_deg := rAng_Filt_deg + TMR_FILTER_ALPHA * (rVotedSpindleAngle_deg - rAng_Filt_deg);
rVotedSpindleAngle_deg := rAng_Filt_deg;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.6: Front Bearing Pack RTD Pt100 Temperature Triplet                                               *)
(* ---------------------------------------------------------------------------------------------------- *)
rTF_Delta_AB := ABS(rFrontBearingTemp_ChA_degC - rFrontBearingTemp_ChB_degC);
rTF_Delta_BC := ABS(rFrontBearingTemp_ChB_degC - rFrontBearingTemp_ChC_degC);
rTF_Delta_CA := ABS(rFrontBearingTemp_ChC_degC - rFrontBearingTemp_ChA_degC);

IF (rTF_Delta_AB > rTF_DiscLimit_degC) OR (rTF_Delta_BC > rTF_DiscLimit_degC) OR (rTF_Delta_CA > rTF_DiscLimit_degC) THEN
    rTF_DiscTimer_s := rTF_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rTF_DiscTimer_s > 0.0 THEN
        rTF_DiscTimer_s := rTF_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rTF_DiscTimer_s < 0.0 THEN
            rTF_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rTF_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rTF_Delta_AB > rTF_DiscLimit_degC) AND (rTF_Delta_CA > rTF_DiscLimit_degC) THEN
        bTF_ChA_Valid := FALSE;
    ELSIF (rTF_Delta_AB > rTF_DiscLimit_degC) AND (rTF_Delta_BC > rTF_DiscLimit_degC) THEN
        bTF_ChB_Valid := FALSE;
    ELSIF (rTF_Delta_BC > rTF_DiscLimit_degC) AND (rTF_Delta_CA > rTF_DiscLimit_degC) THEN
        bTF_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bTF_ChA_Valid := TRUE;
    bTF_ChB_Valid := TRUE;
    bTF_ChC_Valid := TRUE;
    rTF_DiscTimer_s := 0.0;
END_IF;

IF bTF_ChA_Valid AND bTF_ChB_Valid AND bTF_ChC_Valid THEN
    nTF_VotingMode := 3;
    IF (rFrontBearingTemp_ChA_degC >= rFrontBearingTemp_ChB_degC AND rFrontBearingTemp_ChA_degC <= rFrontBearingTemp_ChC_degC) OR
       (rFrontBearingTemp_ChA_degC <= rFrontBearingTemp_ChB_degC AND rFrontBearingTemp_ChA_degC >= rFrontBearingTemp_ChC_degC) THEN
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChA_degC;
    ELSIF (rFrontBearingTemp_ChB_degC >= rFrontBearingTemp_ChA_degC AND rFrontBearingTemp_ChB_degC <= rFrontBearingTemp_ChC_degC) OR
          (rFrontBearingTemp_ChB_degC <= rFrontBearingTemp_ChA_degC AND rFrontBearingTemp_ChB_degC >= rFrontBearingTemp_ChC_degC) THEN
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChB_degC;
    ELSE
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChC_degC;
    END_IF;
ELSIF bTF_ChA_Valid AND bTF_ChB_Valid THEN
    nTF_VotingMode := 2;
    rVotedFrontBearingTemp_degC := 0.5 * (rFrontBearingTemp_ChA_degC + rFrontBearingTemp_ChB_degC);
ELSIF bTF_ChB_Valid AND bTF_ChC_Valid THEN
    nTF_VotingMode := 2;
    rVotedFrontBearingTemp_degC := 0.5 * (rFrontBearingTemp_ChB_degC + rFrontBearingTemp_ChC_degC);
ELSIF bTF_ChA_Valid AND bTF_ChC_Valid THEN
    nTF_VotingMode := 2;
    rVotedFrontBearingTemp_degC := 0.5 * (rFrontBearingTemp_ChA_degC + rFrontBearingTemp_ChC_degC);
ELSIF bTF_ChA_Valid THEN
    nTF_VotingMode := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChA_degC;
ELSIF bTF_ChB_Valid THEN
    nTF_VotingMode := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChB_degC;
ELSIF bTF_ChC_Valid THEN
    nTF_VotingMode := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChC_degC;
ELSE
    nTF_VotingMode := 0;
    rVotedFrontBearingTemp_degC := rTF_Filt_degC;
END_IF;

rTF_Filt_degC := rTF_Filt_degC + TMR_FILTER_ALPHA * (rVotedFrontBearingTemp_degC - rTF_Filt_degC);
rVotedFrontBearingTemp_degC := rTF_Filt_degC;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.7: Rear Floating Bearing RTD Pt100 Temperature Triplet                                            *)
(* ---------------------------------------------------------------------------------------------------- *)
rTR_Delta_AB := ABS(rRearBearingTemp_ChA_degC - rRearBearingTemp_ChB_degC);
rTR_Delta_BC := ABS(rRearBearingTemp_ChB_degC - rRearBearingTemp_ChC_degC);
rTR_Delta_CA := ABS(rRearBearingTemp_ChC_degC - rRearBearingTemp_ChA_degC);

IF (rTR_Delta_AB > rTR_DiscLimit_degC) OR (rTR_Delta_BC > rTR_DiscLimit_degC) OR (rTR_Delta_CA > rTR_DiscLimit_degC) THEN
    rTR_DiscTimer_s := rTR_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rTR_DiscTimer_s > 0.0 THEN
        rTR_DiscTimer_s := rTR_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rTR_DiscTimer_s < 0.0 THEN
            rTR_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rTR_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rTR_Delta_AB > rTR_DiscLimit_degC) AND (rTR_Delta_CA > rTR_DiscLimit_degC) THEN
        bTR_ChA_Valid := FALSE;
    ELSIF (rTR_Delta_AB > rTR_DiscLimit_degC) AND (rTR_Delta_BC > rTR_DiscLimit_degC) THEN
        bTR_ChB_Valid := FALSE;
    ELSIF (rTR_Delta_BC > rTR_DiscLimit_degC) AND (rTR_Delta_CA > rTR_DiscLimit_degC) THEN
        bTR_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bTR_ChA_Valid := TRUE;
    bTR_ChB_Valid := TRUE;
    bTR_ChC_Valid := TRUE;
    rTR_DiscTimer_s := 0.0;
END_IF;

IF bTR_ChA_Valid AND bTR_ChB_Valid AND bTR_ChC_Valid THEN
    nTR_VotingMode := 3;
    IF (rRearBearingTemp_ChA_degC >= rRearBearingTemp_ChB_degC AND rRearBearingTemp_ChA_degC <= rRearBearingTemp_ChC_degC) OR
       (rRearBearingTemp_ChA_degC <= rRearBearingTemp_ChB_degC AND rRearBearingTemp_ChA_degC >= rRearBearingTemp_ChC_degC) THEN
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChA_degC;
    ELSIF (rRearBearingTemp_ChB_degC >= rRearBearingTemp_ChA_degC AND rRearBearingTemp_ChB_degC <= rRearBearingTemp_ChC_degC) OR
          (rRearBearingTemp_ChB_degC <= rRearBearingTemp_ChA_degC AND rRearBearingTemp_ChB_degC >= rRearBearingTemp_ChC_degC) THEN
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChB_degC;
    ELSE
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChC_degC;
    END_IF;
ELSIF bTR_ChA_Valid AND bTR_ChB_Valid THEN
    nTR_VotingMode := 2;
    rVotedRearBearingTemp_degC := 0.5 * (rRearBearingTemp_ChA_degC + rRearBearingTemp_ChB_degC);
ELSIF bTR_ChB_Valid AND bTR_ChC_Valid THEN
    nTR_VotingMode := 2;
    rVotedRearBearingTemp_degC := 0.5 * (rRearBearingTemp_ChB_degC + rRearBearingTemp_ChC_degC);
ELSIF bTR_ChA_Valid AND bTR_ChC_Valid THEN
    nTR_VotingMode := 2;
    rVotedRearBearingTemp_degC := 0.5 * (rRearBearingTemp_ChA_degC + rRearBearingTemp_ChC_degC);
ELSIF bTR_ChA_Valid THEN
    nTR_VotingMode := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChA_degC;
ELSIF bTR_ChB_Valid THEN
    nTR_VotingMode := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChB_degC;
ELSIF bTR_ChC_Valid THEN
    nTR_VotingMode := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChC_degC;
ELSE
    nTR_VotingMode := 0;
    rVotedRearBearingTemp_degC := rTR_Filt_degC;
END_IF;

rTR_Filt_degC := rTR_Filt_degC + TMR_FILTER_ALPHA * (rVotedRearBearingTemp_degC - rTR_Filt_degC);
rVotedRearBearingTemp_degC := rTR_Filt_degC;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.8: Spindle Stator Winding RTD Pt100 Temperature Triplet                                           *)
(* ---------------------------------------------------------------------------------------------------- *)
rTS_Delta_AB := ABS(rSpindleStatorTemp_ChA_degC - rSpindleStatorTemp_ChB_degC);
rTS_Delta_BC := ABS(rSpindleStatorTemp_ChB_degC - rSpindleStatorTemp_ChC_degC);
rTS_Delta_CA := ABS(rSpindleStatorTemp_ChC_degC - rSpindleStatorTemp_ChA_degC);

IF (rTS_Delta_AB > rTS_DiscLimit_degC) OR (rTS_Delta_BC > rTS_DiscLimit_degC) OR (rTS_Delta_CA > rTS_DiscLimit_degC) THEN
    rTS_DiscTimer_s := rTS_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rTS_DiscTimer_s > 0.0 THEN
        rTS_DiscTimer_s := rTS_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rTS_DiscTimer_s < 0.0 THEN
            rTS_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rTS_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rTS_Delta_AB > rTS_DiscLimit_degC) AND (rTS_Delta_CA > rTS_DiscLimit_degC) THEN
        bTS_ChA_Valid := FALSE;
    ELSIF (rTS_Delta_AB > rTS_DiscLimit_degC) AND (rTS_Delta_BC > rTS_DiscLimit_degC) THEN
        bTS_ChB_Valid := FALSE;
    ELSIF (rTS_Delta_BC > rTS_DiscLimit_degC) AND (rTS_Delta_CA > rTS_DiscLimit_degC) THEN
        bTS_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bTS_ChA_Valid := TRUE;
    bTS_ChB_Valid := TRUE;
    bTS_ChC_Valid := TRUE;
    rTS_DiscTimer_s := 0.0;
END_IF;

IF bTS_ChA_Valid AND bTS_ChB_Valid AND bTS_ChC_Valid THEN
    nTS_VotingMode := 3;
    IF (rSpindleStatorTemp_ChA_degC >= rSpindleStatorTemp_ChB_degC AND rSpindleStatorTemp_ChA_degC <= rSpindleStatorTemp_ChC_degC) OR
       (rSpindleStatorTemp_ChA_degC <= rSpindleStatorTemp_ChB_degC AND rSpindleStatorTemp_ChA_degC >= rSpindleStatorTemp_ChC_degC) THEN
        rVotedStatorTemp_degC := rSpindleStatorTemp_ChA_degC;
    ELSIF (rSpindleStatorTemp_ChB_degC >= rSpindleStatorTemp_ChA_degC AND rSpindleStatorTemp_ChB_degC <= rSpindleStatorTemp_ChC_degC) OR
          (rSpindleStatorTemp_ChB_degC <= rSpindleStatorTemp_ChA_degC AND rSpindleStatorTemp_ChB_degC >= rSpindleStatorTemp_ChC_degC) THEN
        rVotedStatorTemp_degC := rSpindleStatorTemp_ChB_degC;
    ELSE
        rVotedStatorTemp_degC := rSpindleStatorTemp_ChC_degC;
    END_IF;
ELSIF bTS_ChA_Valid AND bTS_ChB_Valid THEN
    nTS_VotingMode := 2;
    rVotedStatorTemp_degC := 0.5 * (rSpindleStatorTemp_ChA_degC + rSpindleStatorTemp_ChB_degC);
ELSIF bTS_ChB_Valid AND bTS_ChC_Valid THEN
    nTS_VotingMode := 2;
    rVotedStatorTemp_degC := 0.5 * (rSpindleStatorTemp_ChB_degC + rSpindleStatorTemp_ChC_degC);
ELSIF bTS_ChA_Valid AND bTS_ChC_Valid THEN
    nTS_VotingMode := 2;
    rVotedStatorTemp_degC := 0.5 * (rSpindleStatorTemp_ChA_degC + rSpindleStatorTemp_ChC_degC);
ELSIF bTS_ChA_Valid THEN
    nTS_VotingMode := 1;
    rVotedStatorTemp_degC := rSpindleStatorTemp_ChA_degC;
ELSIF bTS_ChB_Valid THEN
    nTS_VotingMode := 1;
    rVotedStatorTemp_degC := rSpindleStatorTemp_ChB_degC;
ELSIF bTS_ChC_Valid THEN
    nTS_VotingMode := 1;
    rVotedStatorTemp_degC := rSpindleStatorTemp_ChC_degC;
ELSE
    nTS_VotingMode := 0;
    rVotedStatorTemp_degC := rTS_Filt_degC;
END_IF;

rTS_Filt_degC := rTS_Filt_degC + TMR_FILTER_ALPHA * (rVotedStatorTemp_degC - rTS_Filt_degC);
rVotedStatorTemp_degC := rTS_Filt_degC;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.9: Spindle Nose Piezo Accelerometer X-Axis Triplet                                                 *)
(* ---------------------------------------------------------------------------------------------------- *)
rAX_Delta_AB := ABS(rSpindleAccel_X_ChA_ms2 - rSpindleAccel_X_ChB_ms2);
rAX_Delta_BC := ABS(rSpindleAccel_X_ChB_ms2 - rSpindleAccel_X_ChC_ms2);
rAX_Delta_CA := ABS(rSpindleAccel_X_ChC_ms2 - rSpindleAccel_X_ChA_ms2);

IF (rAX_Delta_AB > rAX_DiscLimit_ms2) OR (rAX_Delta_BC > rAX_DiscLimit_ms2) OR (rAX_Delta_CA > rAX_DiscLimit_ms2) THEN
    rAX_DiscTimer_s := rAX_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rAX_DiscTimer_s > 0.0 THEN
        rAX_DiscTimer_s := rAX_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rAX_DiscTimer_s < 0.0 THEN
            rAX_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rAX_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rAX_Delta_AB > rAX_DiscLimit_ms2) AND (rAX_Delta_CA > rAX_DiscLimit_ms2) THEN
        bAX_ChA_Valid := FALSE;
    ELSIF (rAX_Delta_AB > rAX_DiscLimit_ms2) AND (rAX_Delta_BC > rAX_DiscLimit_ms2) THEN
        bAX_ChB_Valid := FALSE;
    ELSIF (rAX_Delta_BC > rAX_DiscLimit_ms2) AND (rAX_Delta_CA > rAX_DiscLimit_ms2) THEN
        bAX_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bAX_ChA_Valid := TRUE;
    bAX_ChB_Valid := TRUE;
    bAX_ChC_Valid := TRUE;
    rAX_DiscTimer_s := 0.0;
END_IF;

IF bAX_ChA_Valid AND bAX_ChB_Valid AND bAX_ChC_Valid THEN
    nAX_VotingMode := 3;
    IF (rSpindleAccel_X_ChA_ms2 >= rSpindleAccel_X_ChB_ms2 AND rSpindleAccel_X_ChA_ms2 <= rSpindleAccel_X_ChC_ms2) OR
       (rSpindleAccel_X_ChA_ms2 <= rSpindleAccel_X_ChB_ms2 AND rSpindleAccel_X_ChA_ms2 >= rSpindleAccel_X_ChC_ms2) THEN
        rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChA_ms2;
    ELSIF (rSpindleAccel_X_ChB_ms2 >= rSpindleAccel_X_ChA_ms2 AND rSpindleAccel_X_ChB_ms2 <= rSpindleAccel_X_ChC_ms2) OR
          (rSpindleAccel_X_ChB_ms2 <= rSpindleAccel_X_ChA_ms2 AND rSpindleAccel_X_ChB_ms2 >= rSpindleAccel_X_ChC_ms2) THEN
        rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChB_ms2;
    ELSE
        rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChC_ms2;
    END_IF;
ELSIF bAX_ChA_Valid AND bAX_ChB_Valid THEN
    nAX_VotingMode := 2;
    rVotedSpindleAccel_X_ms2 := 0.5 * (rSpindleAccel_X_ChA_ms2 + rSpindleAccel_X_ChB_ms2);
ELSIF bAX_ChB_Valid AND bAX_ChC_Valid THEN
    nAX_VotingMode := 2;
    rVotedSpindleAccel_X_ms2 := 0.5 * (rSpindleAccel_X_ChB_ms2 + rSpindleAccel_X_ChC_ms2);
ELSIF bAX_ChA_Valid AND bAX_ChC_Valid THEN
    nAX_VotingMode := 2;
    rVotedSpindleAccel_X_ms2 := 0.5 * (rSpindleAccel_X_ChA_ms2 + rSpindleAccel_X_ChC_ms2);
ELSIF bAX_ChA_Valid THEN
    nAX_VotingMode := 1;
    rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChA_ms2;
ELSIF bAX_ChB_Valid THEN
    nAX_VotingMode := 1;
    rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChB_ms2;
ELSIF bAX_ChC_Valid THEN
    nAX_VotingMode := 1;
    rVotedSpindleAccel_X_ms2 := rSpindleAccel_X_ChC_ms2;
ELSE
    nAX_VotingMode := 0;
    rVotedSpindleAccel_X_ms2 := rAX_Filt_ms2;
END_IF;

rAX_Filt_ms2 := rAX_Filt_ms2 + TMR_FILTER_ALPHA * (rVotedSpindleAccel_X_ms2 - rAX_Filt_ms2);
rVotedSpindleAccel_X_ms2 := rAX_Filt_ms2;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.10: Spindle Nose Piezo Accelerometer Y-Axis Triplet                                                *)
(* ---------------------------------------------------------------------------------------------------- *)
rAY_Delta_AB := ABS(rSpindleAccel_Y_ChA_ms2 - rSpindleAccel_Y_ChB_ms2);
rAY_Delta_BC := ABS(rSpindleAccel_Y_ChB_ms2 - rSpindleAccel_Y_ChC_ms2);
rAY_Delta_CA := ABS(rSpindleAccel_Y_ChC_ms2 - rSpindleAccel_Y_ChA_ms2);

IF (rAY_Delta_AB > rAY_DiscLimit_ms2) OR (rAY_Delta_BC > rAY_DiscLimit_ms2) OR (rAY_Delta_CA > rAY_DiscLimit_ms2) THEN
    rAY_DiscTimer_s := rAY_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rAY_DiscTimer_s > 0.0 THEN
        rAY_DiscTimer_s := rAY_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rAY_DiscTimer_s < 0.0 THEN
            rAY_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rAY_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rAY_Delta_AB > rAY_DiscLimit_ms2) AND (rAY_Delta_CA > rAY_DiscLimit_ms2) THEN
        bAY_ChA_Valid := FALSE;
    ELSIF (rAY_Delta_AB > rAY_DiscLimit_ms2) AND (rAY_Delta_BC > rAY_DiscLimit_ms2) THEN
        bAY_ChB_Valid := FALSE;
    ELSIF (rAY_Delta_BC > rAY_DiscLimit_ms2) AND (rAY_Delta_CA > rAY_DiscLimit_ms2) THEN
        bAY_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bAY_ChA_Valid := TRUE;
    bAY_ChB_Valid := TRUE;
    bAY_ChC_Valid := TRUE;
    rAY_DiscTimer_s := 0.0;
END_IF;

IF bAY_ChA_Valid AND bAY_ChB_Valid AND bAY_ChC_Valid THEN
    nAY_VotingMode := 3;
    IF (rSpindleAccel_Y_ChA_ms2 >= rSpindleAccel_Y_ChB_ms2 AND rSpindleAccel_Y_ChA_ms2 <= rSpindleAccel_Y_ChC_ms2) OR
       (rSpindleAccel_Y_ChA_ms2 <= rSpindleAccel_Y_ChB_ms2 AND rSpindleAccel_Y_ChA_ms2 >= rSpindleAccel_Y_ChC_ms2) THEN
        rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChA_ms2;
    ELSIF (rSpindleAccel_Y_ChB_ms2 >= rSpindleAccel_Y_ChA_ms2 AND rSpindleAccel_Y_ChB_ms2 <= rSpindleAccel_Y_ChC_ms2) OR
          (rSpindleAccel_Y_ChB_ms2 <= rSpindleAccel_Y_ChA_ms2 AND rSpindleAccel_Y_ChB_ms2 >= rSpindleAccel_Y_ChC_ms2) THEN
        rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChB_ms2;
    ELSE
        rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChC_ms2;
    END_IF;
ELSIF bAY_ChA_Valid AND bAY_ChB_Valid THEN
    nAY_VotingMode := 2;
    rVotedSpindleAccel_Y_ms2 := 0.5 * (rSpindleAccel_Y_ChA_ms2 + rSpindleAccel_Y_ChB_ms2);
ELSIF bAY_ChB_Valid AND bAY_ChC_Valid THEN
    nAY_VotingMode := 2;
    rVotedSpindleAccel_Y_ms2 := 0.5 * (rSpindleAccel_Y_ChB_ms2 + rSpindleAccel_Y_ChC_ms2);
ELSIF bAY_ChA_Valid AND bAY_ChC_Valid THEN
    nAY_VotingMode := 2;
    rVotedSpindleAccel_Y_ms2 := 0.5 * (rSpindleAccel_Y_ChA_ms2 + rSpindleAccel_Y_ChC_ms2);
ELSIF bAY_ChA_Valid THEN
    nAY_VotingMode := 1;
    rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChA_ms2;
ELSIF bAY_ChB_Valid THEN
    nAY_VotingMode := 1;
    rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChB_ms2;
ELSIF bAY_ChC_Valid THEN
    nAY_VotingMode := 1;
    rVotedSpindleAccel_Y_ms2 := rSpindleAccel_Y_ChC_ms2;
ELSE
    nAY_VotingMode := 0;
    rVotedSpindleAccel_Y_ms2 := rAY_Filt_ms2;
END_IF;

rAY_Filt_ms2 := rAY_Filt_ms2 + TMR_FILTER_ALPHA * (rVotedSpindleAccel_Y_ms2 - rAY_Filt_ms2);
rVotedSpindleAccel_Y_ms2 := rAY_Filt_ms2;

(* ---------------------------------------------------------------------------------------------------- *)
(* 1.11: Spindle Nose Piezo Accelerometer Z-Axis Triplet                                                *)
(* ---------------------------------------------------------------------------------------------------- *)
rAZ_Delta_AB := ABS(rSpindleAccel_Z_ChA_ms2 - rSpindleAccel_Z_ChB_ms2);
rAZ_Delta_BC := ABS(rSpindleAccel_Z_ChB_ms2 - rSpindleAccel_Z_ChC_ms2);
rAZ_Delta_CA := ABS(rSpindleAccel_Z_ChC_ms2 - rSpindleAccel_Z_ChA_ms2);

IF (rAZ_Delta_AB > rAZ_DiscLimit_ms2) OR (rAZ_Delta_BC > rAZ_DiscLimit_ms2) OR (rAZ_Delta_CA > rAZ_DiscLimit_ms2) THEN
    rAZ_DiscTimer_s := rAZ_DiscTimer_s + T_CYCLE_SEC;
ELSE
    IF rAZ_DiscTimer_s > 0.0 THEN
        rAZ_DiscTimer_s := rAZ_DiscTimer_s - (0.5 * T_CYCLE_SEC);
        IF rAZ_DiscTimer_s < 0.0 THEN
            rAZ_DiscTimer_s := 0.0;
        END_IF;
    END_IF;
END_IF;

IF rAZ_DiscTimer_s >= T_DISCREPANCY_FAULT_SEC THEN
    IF (rAZ_Delta_AB > rAZ_DiscLimit_ms2) AND (rAZ_Delta_CA > rAZ_DiscLimit_ms2) THEN
        bAZ_ChA_Valid := FALSE;
    ELSIF (rAZ_Delta_AB > rAZ_DiscLimit_ms2) AND (rAZ_Delta_BC > rAZ_DiscLimit_ms2) THEN
        bAZ_ChB_Valid := FALSE;
    ELSIF (rAZ_Delta_BC > rAZ_DiscLimit_ms2) AND (rAZ_Delta_CA > rAZ_DiscLimit_ms2) THEN
        bAZ_ChC_Valid := FALSE;
    END_IF;
END_IF;

IF bAlarmReset THEN
    bAZ_ChA_Valid := TRUE;
    bAZ_ChB_Valid := TRUE;
    bAZ_ChC_Valid := TRUE;
    rAZ_DiscTimer_s := 0.0;
END_IF;

IF bAZ_ChA_Valid AND bAZ_ChB_Valid AND bAZ_ChC_Valid THEN
    nAZ_VotingMode := 3;
    IF (rSpindleAccel_Z_ChA_ms2 >= rSpindleAccel_Z_ChB_ms2 AND rSpindleAccel_Z_ChA_ms2 <= rSpindleAccel_Z_ChC_ms2) OR
       (rSpindleAccel_Z_ChA_ms2 <= rSpindleAccel_Z_ChB_ms2 AND rSpindleAccel_Z_ChA_ms2 >= rSpindleAccel_Z_ChC_ms2) THEN
        rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChA_ms2;
    ELSIF (rSpindleAccel_Z_ChB_ms2 >= rSpindleAccel_Z_ChA_ms2 AND rSpindleAccel_Z_ChB_ms2 <= rSpindleAccel_Z_ChC_ms2) OR
          (rSpindleAccel_Z_ChB_ms2 <= rSpindleAccel_Z_ChA_ms2 AND rSpindleAccel_Z_ChB_ms2 >= rSpindleAccel_Z_ChC_ms2) THEN
        rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChB_ms2;
    ELSE
        rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChC_ms2;
    END_IF;
ELSIF bAZ_ChA_Valid AND bAZ_ChB_Valid THEN
    nAZ_VotingMode := 2;
    rVotedSpindleAccel_Z_ms2 := 0.5 * (rSpindleAccel_Z_ChA_ms2 + rSpindleAccel_Z_ChB_ms2);
ELSIF bAZ_ChB_Valid AND bAZ_ChC_Valid THEN
    nAZ_VotingMode := 2;
    rVotedSpindleAccel_Z_ms2 := 0.5 * (rSpindleAccel_Z_ChB_ms2 + rSpindleAccel_Z_ChC_ms2);
ELSIF bAZ_ChA_Valid AND bAZ_ChC_Valid THEN
    nAZ_VotingMode := 2;
    rVotedSpindleAccel_Z_ms2 := 0.5 * (rSpindleAccel_Z_ChA_ms2 + rSpindleAccel_Z_ChC_ms2);
ELSIF bAZ_ChA_Valid THEN
    nAZ_VotingMode := 1;
    rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChA_ms2;
ELSIF bAZ_ChB_Valid THEN
    nAZ_VotingMode := 1;
    rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChB_ms2;
ELSIF bAZ_ChC_Valid THEN
    nAZ_VotingMode := 1;
    rVotedSpindleAccel_Z_ms2 := rSpindleAccel_Z_ChC_ms2;
ELSE
    nAZ_VotingMode := 0;
    rVotedSpindleAccel_Z_ms2 := rAZ_Filt_ms2;
END_IF;

rAZ_Filt_ms2 := rAZ_Filt_ms2 + TMR_FILTER_ALPHA * (rVotedSpindleAccel_Z_ms2 - rAZ_Filt_ms2);
rVotedSpindleAccel_Z_ms2 := rAZ_Filt_ms2;
"""
