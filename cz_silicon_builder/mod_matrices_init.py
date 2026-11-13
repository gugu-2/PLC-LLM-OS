# cz_silicon_builder/mod_matrices_init.py
# -*- coding: utf-8 -*-

def generate_matrices_init():
    return """(* ==========================================================================================
   INITIALIZATION & FIRST SCAN MATRIX CONFIGURATION (6x6 DISCRETE STATE-SPACE & MPC WEIGHTS)
   ========================================================================================== *)
IF bFirstScan THEN
    (* Compute effective discrete scan time in seconds *)
    IF tCycleTime > T#0MS THEN
        rCycleTimeSec := TIME_TO_REAL(tCycleTime) / 1000.0;
    ELSE
        rCycleTimeSec := 0.10;
    END_IF;

    (* --------------------------------------------------------------------------------------
       A_mat: Discrete State Transition Matrix (6x6)
       Dynamics sampled at Ts = 100 ms representing thermal diffusion, crystallization kinetics,
       and cusp magnetic viscous damping.
       -------------------------------------------------------------------------------------- *)
    A_mat[1,1] := 0.9880; A_mat[1,2] := -0.0450; A_mat[1,3] := 0.0180; A_mat[1,4] := -0.0060; A_mat[1,5] := -0.0035; A_mat[1,6] := -0.1420;
    A_mat[2,1] := 0.0025; A_mat[2,2] := 0.9720; A_mat[2,3] := -0.0280; A_mat[2,4] := 0.0650; A_mat[2,5] := 0.0120; A_mat[2,6] := 0.0380;
    A_mat[3,1] := 0.0010; A_mat[3,2] := -0.0150; A_mat[3,3] := 0.9650; A_mat[3,4] := -0.0220; A_mat[3,5] := -0.0080; A_mat[3,6] := 0.0820;
    A_mat[4,1] := 0.0000; A_mat[4,2] := 0.0085; A_mat[4,3] := -0.0040; A_mat[4,4] := 0.9910; A_mat[4,5] := 0.0160; A_mat[4,6] := -0.0050;
    A_mat[5,1] := 0.0000; A_mat[5,2] := 0.0220; A_mat[5,3] := 0.0000; A_mat[5,4] := 0.0450; A_mat[5,5] := 0.8850; A_mat[5,6] := 0.0000;
    A_mat[6,1] := 0.0000; A_mat[6,2] := 0.0000; A_mat[6,3] := 0.0000; A_mat[6,4] := 0.0000; A_mat[6,5] := 0.0000; A_mat[6,6] := 0.9200;

    (* --------------------------------------------------------------------------------------
       B_mat: Discrete Input Coupling Matrix (6x5)
       Inputs: u1: Pull Speed [mm/min], u2: Main Heater [kW], u3: Crucible Lift [mm/min],
               u4: Cusp Current [A], u5: Seed Rotation [RPM]
       -------------------------------------------------------------------------------------- *)
    B_mat[1,1] := -0.1650; B_mat[1,2] := -0.0145; B_mat[1,3] := 0.0035; B_mat[1,4] := 0.0008; B_mat[1,5] := -0.0012;
    B_mat[2,1] := 0.0420; B_mat[2,2] := 0.0850; B_mat[2,3] := 0.0060; B_mat[2,4] := -0.0180; B_mat[2,5] := 0.0110;
    B_mat[3,1] := 0.0950; B_mat[3,2] := -0.0380; B_mat[3,3] := -0.0025; B_mat[3,4] := 0.0045; B_mat[3,5] := -0.0085;
    B_mat[4,1] := -0.0080; B_mat[4,2] := 0.1250; B_mat[4,3] := 0.0140; B_mat[4,4] := -0.0065; B_mat[4,5] := 0.0150;
    B_mat[5,1] := 0.0000; B_mat[5,2] := 0.0350; B_mat[5,3] := 0.0000; B_mat[5,4] := -0.0780; B_mat[5,5] := 0.0250;
    B_mat[6,1] := 0.8500; B_mat[6,2] := 0.0000; B_mat[6,3] := 0.0000; B_mat[6,4] := 0.0000; B_mat[6,5] := 0.0000;

    (* --------------------------------------------------------------------------------------
       C_mat: Discrete Output Observation Matrix (6x6)
       Maps internal physical states to sensor observables.
       -------------------------------------------------------------------------------------- *)
    C_mat[1,1] := 0.0000; C_mat[1,2] := 1.0000; C_mat[1,3] := 0.0000; C_mat[1,4] := 0.0000; C_mat[1,5] := 0.0000; C_mat[1,6] := 0.0000;
    C_mat[2,1] := 1.0000; C_mat[2,2] := 0.0000; C_mat[2,3] := 0.0000; C_mat[2,4] := 0.0000; C_mat[2,5] := 0.0000; C_mat[2,6] := 0.0000;
    C_mat[3,1] := 0.9850; C_mat[3,2] := -0.0020; C_mat[3,3] := 0.0000; C_mat[3,4] := 0.0000; C_mat[3,5] := 0.0000; C_mat[3,6] := 0.0120;
    C_mat[4,1] := 0.0000; C_mat[4,2] := 0.0000; C_mat[4,3] := 0.0000; C_mat[4,4] := 1.0000; C_mat[4,5] := 0.0000; C_mat[4,6] := 0.0000;
    C_mat[5,1] := 0.0000; C_mat[5,2] := 0.0000; C_mat[5,3] := 0.0000; C_mat[5,4] := 0.0000; C_mat[5,5] := 1.0000; C_mat[5,6] := 0.0000;
    C_mat[6,1] := 0.0000; C_mat[6,2] := 0.0000; C_mat[6,3] := 0.0000; C_mat[6,4] := 0.0000; C_mat[6,5] := 0.0000; C_mat[6,6] := 1.0000;

    (* --------------------------------------------------------------------------------------
       D_mat: Direct Feedthrough Matrix (6x5)
       -------------------------------------------------------------------------------------- *)
    D_mat[1,1] := 0.0; D_mat[1,2] := 0.0; D_mat[1,3] := 0.0; D_mat[1,4] := 0.0; D_mat[1,5] := 0.0;
    D_mat[2,1] := 0.0; D_mat[2,2] := 0.0; D_mat[2,3] := 0.0; D_mat[2,4] := 0.0; D_mat[2,5] := 0.0;
    D_mat[3,1] := 0.0; D_mat[3,2] := 0.0; D_mat[3,3] := 0.0; D_mat[3,4] := 0.0; D_mat[3,5] := 0.0;
    D_mat[4,1] := 0.0; D_mat[4,2] := 0.0; D_mat[4,3] := 0.0; D_mat[4,4] := 0.0; D_mat[4,5] := 0.0;
    D_mat[5,1] := 0.0; D_mat[5,2] := 0.0; D_mat[5,3] := 0.0; D_mat[5,4] := 0.0; D_mat[5,5] := 0.0;
    D_mat[6,1] := 0.0; D_mat[6,2] := 0.0; D_mat[6,3] := 0.0; D_mat[6,4] := 0.0; D_mat[6,5] := 0.0;

    (* --------------------------------------------------------------------------------------
       L_mat: Luenberger Observer / Kalman Gain Innovation Matrix (6x6)
       Designed to place observer poles strictly inside the unit circle (|lambda| < 0.65).
       -------------------------------------------------------------------------------------- *)
    L_mat[1,1] := 0.0240; L_mat[1,2] := 0.2850; L_mat[1,3] := 0.1450; L_mat[1,4] := -0.0020; L_mat[1,5] := -0.0010; L_mat[1,6] := -0.0520;
    L_mat[2,1] := 0.3200; L_mat[2,2] := 0.0180; L_mat[2,3] := 0.0050; L_mat[2,4] := 0.0420; L_mat[2,5] := 0.0150; L_mat[2,6] := 0.0120;
    L_mat[3,1] := -0.0150; L_mat[3,2] := 0.0350; L_mat[3,3] := 0.0180; L_mat[3,4] := -0.0120; L_mat[3,5] := -0.0050; L_mat[3,6] := 0.0450;
    L_mat[4,1] := 0.0280; L_mat[4,2] := -0.0040; L_mat[4,3] := 0.0000; L_mat[4,4] := 0.2650; L_mat[4,5] := 0.0180; L_mat[4,6] := -0.0020;
    L_mat[5,1] := 0.0120; L_mat[5,2] := 0.0000; L_mat[5,3] := 0.0000; L_mat[5,4] := 0.0150; L_mat[5,5] := 0.3800; L_mat[5,6] := 0.0000;
    L_mat[6,1] := 0.0000; L_mat[6,2] := -0.0220; L_mat[6,3] := 0.0110; L_mat[6,4] := 0.0000; L_mat[6,5] := 0.0000; L_mat[6,6] := 0.4200;

    (* --------------------------------------------------------------------------------------
       Q_mat: Quadratic State Tracking Penalty Matrix (6x6)
       Heavily penalizes diameter deviation (x1) and meniscus temperature deviation (x2).
       -------------------------------------------------------------------------------------- *)
    Q_mat[1,1] := 140.0; Q_mat[1,2] := 0.0;   Q_mat[1,3] := 0.0;   Q_mat[1,4] := 0.0;   Q_mat[1,5] := 0.0;   Q_mat[1,6] := 0.0;
    Q_mat[2,1] := 0.0;   Q_mat[2,2] := 45.0;  Q_mat[2,3] := 0.0;   Q_mat[2,4] := 0.0;   Q_mat[2,5] := 0.0;   Q_mat[2,6] := 0.0;
    Q_mat[3,1] := 0.0;   Q_mat[3,2] := 0.0;   Q_mat[3,3] := 65.0;  Q_mat[3,4] := 0.0;   Q_mat[3,5] := 0.0;   Q_mat[3,6] := 0.0;
    Q_mat[4,1] := 0.0;   Q_mat[4,2] := 0.0;   Q_mat[4,3] := 0.0;   Q_mat[4,4] := 18.0;  Q_mat[4,5] := 0.0;   Q_mat[4,6] := 0.0;
    Q_mat[5,1] := 0.0;   Q_mat[5,2] := 0.0;   Q_mat[5,3] := 0.0;   Q_mat[5,4] := 0.0;   Q_mat[5,5] := 25.0;  Q_mat[5,6] := 0.0;
    Q_mat[6,1] := 0.0;   Q_mat[6,2] := 0.0;   Q_mat[6,3] := 0.0;   Q_mat[6,4] := 0.0;   Q_mat[6,5] := 0.0;   Q_mat[6,6] := 35.0;

    (* --------------------------------------------------------------------------------------
       R_mat: Quadratic Actuator Effort Penalty Matrix (5x5)
       Balances pull servo speed variations and graphite heater power consumption.
       -------------------------------------------------------------------------------------- *)
    R_mat[1,1] := 15.0;  R_mat[1,2] := 0.0;   R_mat[1,3] := 0.0;   R_mat[1,4] := 0.0;   R_mat[1,5] := 0.0;
    R_mat[2,1] := 0.0;   R_mat[2,2] := 8.5;   R_mat[2,3] := 0.0;   R_mat[2,4] := 0.0;   R_mat[2,5] := 0.0;
    R_mat[3,1] := 0.0;   R_mat[3,2] := 0.0;   R_mat[3,3] := 12.0;  R_mat[3,4] := 0.0;   R_mat[3,5] := 0.0;
    R_mat[4,1] := 0.0;   R_mat[4,2] := 0.0;   R_mat[4,3] := 0.0;   R_mat[4,4] := 4.2;   R_mat[4,5] := 0.0;
    R_mat[5,1] := 0.0;   R_mat[5,2] := 0.0;   R_mat[5,3] := 0.0;   R_mat[5,4] := 0.0;   R_mat[5,5] := 6.5;

    (* --------------------------------------------------------------------------------------
       S_mat: Quadratic Actuator Slew Rate Damping Penalty Matrix (5x5)
       Prevents aggressive actuator jerks that trigger crystallographic slip dislocations.
       -------------------------------------------------------------------------------------- *)
    S_mat[1,1] := 80.0;  S_mat[1,2] := 0.0;   S_mat[1,3] := 0.0;   S_mat[1,4] := 0.0;   S_mat[1,5] := 0.0;
    S_mat[2,1] := 0.0;   S_mat[2,2] := 35.0;  S_mat[2,3] := 0.0;   S_mat[2,4] := 0.0;   S_mat[2,5] := 0.0;
    S_mat[3,1] := 0.0;   S_mat[3,2] := 0.0;   S_mat[3,3] := 40.0;  S_mat[3,4] := 0.0;   S_mat[3,5] := 0.0;
    S_mat[4,1] := 0.0;   S_mat[4,2] := 0.0;   S_mat[4,3] := 0.0;   S_mat[4,4] := 15.0;  S_mat[4,5] := 0.0;
    S_mat[5,1] := 0.0;   S_mat[5,2] := 0.0;   S_mat[5,3] := 0.0;   S_mat[5,4] := 0.0;   S_mat[5,5] := 20.0;

    (* --------------------------------------------------------------------------------------
       P_mat: Terminal State Quadratic Cost Matrix (6x6)
       Derived from discrete algebraic Riccati equation (DARE) solution.
       -------------------------------------------------------------------------------------- *)
    P_mat[1,1] := 220.0; P_mat[1,2] := 0.0;   P_mat[1,3] := 0.0;   P_mat[1,4] := 0.0;   P_mat[1,5] := 0.0;   P_mat[1,6] := 0.0;
    P_mat[2,1] := 0.0;   P_mat[2,2] := 80.0;  P_mat[2,3] := 0.0;   P_mat[2,4] := 0.0;   P_mat[2,5] := 0.0;   P_mat[2,6] := 0.0;
    P_mat[3,1] := 0.0;   P_mat[3,2] := 0.0;   P_mat[3,3] := 95.0;  P_mat[3,4] := 0.0;   P_mat[3,5] := 0.0;   P_mat[3,6] := 0.0;
    P_mat[4,1] := 0.0;   P_mat[4,2] := 0.0;   P_mat[4,3] := 0.0;   P_mat[4,4] := 32.0;  P_mat[4,5] := 0.0;   P_mat[4,6] := 0.0;
    P_mat[5,1] := 0.0;   P_mat[5,2] := 0.0;   P_mat[5,3] := 0.0;   P_mat[5,4] := 0.0;   P_mat[5,5] := 45.0;  P_mat[5,6] := 0.0;
    P_mat[6,1] := 0.0;   P_mat[6,2] := 0.0;   P_mat[6,3] := 0.0;   P_mat[6,4] := 0.0;   P_mat[6,5] := 0.0;   P_mat[6,6] := 55.0;

    (* --------------------------------------------------------------------------------------
       Physical Actuator Box Bounds & Maximum Allowable Slew Limits
       -------------------------------------------------------------------------------------- *)
    u_min[1] := 0.0;    u_max[1] := 14.0;   du_max[1] := 0.15;  (* Pull Speed [mm/min] *)
    u_min[2] := 25.0;   u_max[2] := 175.0;  du_max[2] := 1.80;  (* Main Graphite Heater [kW] *)
    u_min[3] := 0.0;    u_max[3] := 6.50;   du_max[3] := 0.12;  (* Crucible Lift Speed [mm/min] *)
    u_min[4] := 0.0;    u_max[4] := 550.0;  du_max[4] := 12.0;  (* Cusp Coil DC Current [A] *)
    u_min[5] := 0.0;    u_max[5] := 24.0;   du_max[5] := 0.80;  (* Seed Shaft Rotation [RPM] *)

    (* Initialize State Reference Setpoint Trajectory *)
    x_ref[1] := rTargetIngotDiameter; (* 300.0 mm *)
    x_ref[2] := 1414.0; (* Solidification Tri-Junction Isotherm [deg C] *)
    x_ref[3] := 3.45;   (* Interface Axial Temperature Gradient [K/mm] *)
    x_ref[4] := 1426.0; (* Bulk Liquid Crucible Melt [deg C] *)
    x_ref[5] := 0.40;   (* Damped Convective Turbulence Target [mm/s] *)
    x_ref[6] := 0.0;    (* Zero Pull Speed Deviation [mm/min] *)

    (* Initialize Observer State Estimates to Safe Physical Resting Datum *)
    x_hat[1] := 0.0;
    x_hat[2] := 25.0;
    x_hat[3] := 0.0;
    x_hat[4] := 25.0;
    x_hat[5] := 0.0;
    x_hat[6] := 0.0;

    (* Initialize Actuator Vectors *)
    FOR iLoopIndex := 1 TO 5 DO
        u_cmd[iLoopIndex] := 0.0;
        u_prev[iLoopIndex] := 0.0;
        u_rate[iLoopIndex] := 0.0;
    END_FOR;

    (* Initial charge mass *)
    IF rInitialSiliconChargeMass > 50.0 THEN
        rSiliconMeltMassRemaining_kg := rInitialSiliconChargeMass;
    ELSE
        rSiliconMeltMassRemaining_kg := 350.0;
    END_IF;

    bFirstScan := FALSE;
END_IF;"""
