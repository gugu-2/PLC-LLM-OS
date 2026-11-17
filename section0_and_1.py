# section0_and_1.py
# Implements Phase 0 (Init) and Phase 1 (2oo3 TMR voting + 4-Tie-Bar Balancing)

def get_section0():
    return """
(* ========================================================================================= *)
(* 0.0 FIRST-SCAN MATRIX PARAMETERIZATION & OBSERVER / MPC WEIGHT INITIALIZATION             *)
(* ========================================================================================= *)
IF NOT bMatricesInitialized THEN
    (* ------------------------------------------------------------------------------------- *)
    (* Discrete State Transition Matrix A (6x6) - Sample Time Ts = 1.0 ms                    *)
    (* States:                                                                               *)
    (*   x1: Plunger injection velocity [m/s]                                                *)
    (*   x2: Hydraulic shot cylinder head pressure [bar]                                     *)
    (*   x3: Mold cavity vacuum pressure [mbar]                                              *)
    (*   x4: Total 4-tie-bar clamping force [kN]                                             *)
    (*   x5: Mold cavity face surface temperature [deg C]                                    *)
    (*   x6: Cast part shell solidification thickness [mm]                                   *)
    (* ------------------------------------------------------------------------------------- *)
    A_mat[1,1] := 0.9450;  A_mat[1,2] := 0.0035;  A_mat[1,3] := -0.0008; A_mat[1,4] := 0.0000;  A_mat[1,5] := 0.0000;  A_mat[1,6] := -0.0120;
    A_mat[2,1] := -0.1850; A_mat[2,2] := 0.9250;  A_mat[2,3] := 0.0000;  A_mat[2,4] := 0.0012;  A_mat[2,5] := 0.0000;  A_mat[2,6] := 0.0350;
    A_mat[3,1] := 0.0000;  A_mat[3,2] := 0.0000;  A_mat[3,3] := 0.8950;  A_mat[3,4] := -0.0005; A_mat[3,5] := 0.0045;  A_mat[3,6] := 0.0000;
    A_mat[4,1] := 0.0000;  A_mat[4,2] := 0.0240;  A_mat[4,3] := 0.0000;  A_mat[4,4] := 0.9980;  A_mat[4,5] := 0.0850;  A_mat[4,6] := 0.0000;
    A_mat[5,1] := 0.0150;  A_mat[5,2] := 0.0000;  A_mat[5,3] := 0.0000;  A_mat[5,4] := 0.0000;  A_mat[5,5] := 0.9650;  A_mat[5,6] := -0.0450;
    A_mat[6,1] := 0.0025;  A_mat[6,2] := 0.0008;  A_mat[6,3] := 0.0000;  A_mat[6,4] := 0.0000;  A_mat[6,5] := -0.0035; A_mat[6,6] := 0.9850;

    (* ------------------------------------------------------------------------------------- *)
    (* Input Control Coupling Matrix B (6x5)                                                 *)
    (* Inputs:                                                                               *)
    (*   u1: High-response servo proportional pilot valve [%]                                *)
    (*   u2: Hydraulic accumulator fast-discharge poppet valve [%]                           *)
    (*   u3: Intensifier booster multiplier pilot valve [%]                                  *)
    (*   u4: High-vacuum line extraction throttle valve [%]                                  *)
    (*   u5: Die thermal tempering oil circulating pump speed [%]                            *)
    (* ------------------------------------------------------------------------------------- *)
    B_mat[1,1] := 0.1250;  B_mat[1,2] := 0.2850;  B_mat[1,3] := 0.0150;  B_mat[1,4] := 0.0000;  B_mat[1,5] := 0.0000;
    B_mat[2,1] := 0.0850;  B_mat[2,2] := 0.4500;  B_mat[2,3] := 1.8500;  B_mat[2,4] := 0.0000;  B_mat[2,5] := 0.0000;
    B_mat[3,1] := 0.0000;  B_mat[3,2] := 0.0000;  B_mat[3,3] := 0.0000;  B_mat[3,4] := -0.6500; B_mat[3,5] := 0.0000;
    B_mat[4,1] := 0.0000;  B_mat[4,2] := 0.0180;  B_mat[4,3] := 0.1450;  B_mat[4,4] := 0.0000;  B_mat[4,5] := 0.0250;
    B_mat[5,1] := 0.0000;  B_mat[5,2] := 0.0000;  B_mat[5,3] := 0.0000;  B_mat[5,4] := 0.0000;  B_mat[5,5] := -0.1550;
    B_mat[6,1] := 0.0000;  B_mat[6,2] := 0.0000;  B_mat[6,3] := 0.0025;  B_mat[6,4] := 0.0000;  B_mat[6,5] := 0.0085;

    (* ------------------------------------------------------------------------------------- *)
    (* Measurement Observation Matrix C (6x6) - Identity State Direct Observability          *)
    (* ------------------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 6 DO
        FOR iIdx2 := 1 TO 6 DO
            IF iIdx1 = iIdx2 THEN
                C_mat[iIdx1, iIdx2] := 1.0;
            ELSE
                C_mat[iIdx1, iIdx2] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Direct Feedthrough Matrix D (6x5) - Strictly Zero Algebraic Feedthrough               *)
    (* ------------------------------------------------------------------------------------- *)
    FOR iIdx1 := 1 TO 6 DO
        FOR iIdx2 := 1 TO 5 DO
            D_mat[iIdx1, iIdx2] := 0.0;
        END_FOR;
    END_FOR;

    (* ------------------------------------------------------------------------------------- *)
    (* Kalman / Luenberger Observer Innovation Gain Matrix L (6x6)                           *)
    (* ------------------------------------------------------------------------------------- *)
    L_obs[1,1] := 0.3850; L_obs[1,2] := 0.0012; L_obs[1,3] := 0.0000; L_obs[1,4] := 0.0000; L_obs[1,5] := 0.0000; L_obs[1,6] := 0.0000;
    L_obs[2,1] := 0.0045; L_obs[2,2] := 0.4250; L_obs[2,3] := 0.0000; L_obs[2,4] := 0.0008; L_obs[2,5] := 0.0000; L_obs[2,6] := 0.0015;
    L_obs[3,1] := 0.0000; L_obs[3,2] := 0.0000; L_obs[3,3] := 0.3500; L_obs[3,4] := 0.0000; L_obs[3,5] := 0.0005; L_obs[3,6] := 0.0000;
    L_obs[4,1] := 0.0000; L_obs[4,2] := 0.0015; L_obs[4,3] := 0.0000; L_obs[4,4] := 0.2850; L_obs[4,5] := 0.0025; L_obs[4,6] := 0.0000;
    L_obs[5,1] := 0.0000; L_obs[5,2] := 0.0000; L_obs[5,3] := 0.0000; L_obs[5,4] := 0.0000; L_obs[5,5] := 0.3150; L_obs[5,6] := 0.0008;
    L_obs[6,1] := 0.0000; L_obs[6,2] := 0.0002; L_obs[6,3] := 0.0000; L_obs[6,4] := 0.0000; L_obs[6,5] := 0.0010; L_obs[6,6] := 0.2950;

    (* ------------------------------------------------------------------------------------- *)
    (* Model Predictive Control (MPC) Cost Weight Matrices (Q, R, S, P)                      *)
    (* ------------------------------------------------------------------------------------- *)
    Q_diag[1] := 45.00; (* State 1 Penalty: Plunger injection velocity tracking precision *)
    Q_diag[2] := 18.50; (* State 2 Penalty: Hydraulic shot cylinder head pressure dynamics *)
    Q_diag[3] := 25.00; (* State 3 Penalty: Mold cavity vacuum level (high penalty for sub-vacuum) *)
    Q_diag[4] := 12.00; (* State 4 Penalty: Total 4-tie-bar clamping force balance *)
    Q_diag[5] := 4.50;  (* State 5 Penalty: Mold cavity face surface temperature *)
    Q_diag[6] := 8.00;  (* State 6 Penalty: Solidification shell growth tracking *)

    R_diag[1] := 1.25;  (* Actuator 1 Penalty: Pilot servo valve control effort *)
    R_diag[2] := 0.85;  (* Actuator 2 Penalty: Accumulator poppet valve aggressive firing *)
    R_diag[3] := 2.40;  (* Actuator 3 Penalty: Intensifier booster multiplier pilot effort *)
    R_diag[4] := 0.65;  (* Actuator 4 Penalty: Vacuum throttle valve actuation effort *)
    R_diag[5] := 0.40;  (* Actuator 5 Penalty: Tempering oil pump speed variation *)

    S_diag[1] := 3.50;  (* Slew Damping 1: Pilot valve dU/dt rate limiting *)
    S_diag[2] := 4.80;  (* Slew Damping 2: Poppet valve dU/dt rate limiting *)
    S_diag[3] := 6.50;  (* Slew Damping 3: Intensifier booster dU/dt damping *)
    S_diag[4] := 1.80;  (* Slew Damping 4: Vacuum valve dU/dt damping *)
    S_diag[5] := 1.20;  (* Slew Damping 5: Tempering pump dU/dt damping *)

    P_diag[1] := 85.00; (* Terminal Penalty: Velocity stabilization at end of horizon *)
    P_diag[2] := 45.00; (* Terminal Penalty: Intensification pressure squeeze terminal *)
    P_diag[3] := 50.00; (* Terminal Penalty: Vacuum state terminal boundary *)
    P_diag[4] := 25.00; (* Terminal Penalty: Tie-bar force terminal integrity *)
    P_diag[5] := 10.00; (* Terminal Penalty: Mold temperature steady-state *)
    P_diag[6] := 18.00; (* Terminal Penalty: Solidification complete boundary *)

    (* Initialize State Estimators to Ambient Baseline *)
    x_hat[1] := 0.0;
    x_hat[2] := 15.0;
    x_hat[3] := 1013.0;
    x_hat[4] := 0.0;
    x_hat[5] := 220.0;
    x_hat[6] := 0.0;

    FOR iIdx1 := 1 TO 6 DO
        x_state[iIdx1] := x_hat[iIdx1];
        x_err[iIdx1]   := 0.0;
    END_FOR;

    FOR iIdx1 := 1 TO 5 DO
        u_mpc[iIdx1]    := 0.0;
        u_prev[iIdx1]   := 0.0;
        u_target[iIdx1] := 0.0;
        u_delta[iIdx1]  := 0.0;
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;
"""

def get_section1():
    return """
(* ========================================================================================= *)
(* 1.0 TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING SUITE & PERSISTENCE TIMERS             *)
(* ========================================================================================= *)
(* Executes deterministic median selection with cross-channel deviation checking across     *)
(* all four critical mega-casting instrument triplets. Gracefully degrades from 2oo3 to     *)
(* 1oo2, and finally to 1oo1 fail-safe before latching an automatic emergency shutdown.     *)

dwStatusWord2 := 16#0000_0000;

(* ----------------------------------------------------------------------------------------- *)
(* 1.1 Plunger Injection Velocity 2oo3 Voting Bank (rPlungerVel_A, B, C)                     *)
(* ----------------------------------------------------------------------------------------- *)
bVel_A_Healthy := (rPlungerVel_A_ms >= -0.50) AND (rPlungerVel_A_ms <= 12.50);
bVel_B_Healthy := (rPlungerVel_B_ms >= -0.50) AND (rPlungerVel_B_ms <= 12.50);
bVel_C_Healthy := (rPlungerVel_C_ms >= -0.50) AND (rPlungerVel_C_ms <= 12.50);

rDev_Vel_AB := ABS(rPlungerVel_A_ms - rPlungerVel_B_ms);
rDev_Vel_BC := ABS(rPlungerVel_B_ms - rPlungerVel_C_ms);
rDev_Vel_CA := ABS(rPlungerVel_C_ms - rPlungerVel_A_ms);

IF bVel_A_Healthy AND bVel_B_Healthy AND bVel_C_Healthy THEN
    bVel_Degraded_1oo2 := FALSE;
    bVel_Failed_Trip   := FALSE;
    (* Standard 2oo3 Median Sorting *)
    IF ((rPlungerVel_A_ms >= rPlungerVel_B_ms) AND (rPlungerVel_A_ms <= rPlungerVel_C_ms)) OR
       ((rPlungerVel_A_ms >= rPlungerVel_C_ms) AND (rPlungerVel_A_ms <= rPlungerVel_B_ms)) THEN
        rPlungerVel_Voted_ms := rPlungerVel_A_ms;
    ELSIF ((rPlungerVel_B_ms >= rPlungerVel_A_ms) AND (rPlungerVel_B_ms <= rPlungerVel_C_ms)) OR
          ((rPlungerVel_B_ms >= rPlungerVel_C_ms) AND (rPlungerVel_B_ms <= rPlungerVel_A_ms)) THEN
        rPlungerVel_Voted_ms := rPlungerVel_B_ms;
    ELSE
        rPlungerVel_Voted_ms := rPlungerVel_C_ms;
    END_IF;

    (* Cross-Channel Discrepancy Check (Tolerance = 0.45 m/s, Persistence = 20.0 ms) *)
    IF (rDev_Vel_AB > 0.45) OR (rDev_Vel_BC > 0.45) OR (rDev_CA > 0.45) THEN
        rTon_Vel_Discrep_s := rTon_Vel_Discrep_s + rCycleTime_sec;
        IF rTon_Vel_Discrep_s >= 0.020 THEN
            dwStatusWord2 := dwStatusWord2 OR 16#0000_0001; (* Velocity triplet discrepancy warning *)
        END_IF;
    ELSE
        rTon_Vel_Discrep_s := 0.0;
    END_IF;

ELSIF bVel_A_Healthy AND bVel_B_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := (rPlungerVel_A_ms + rPlungerVel_B_ms) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0002; (* Velocity degraded 1oo2 (Chan C fail) *)
ELSIF bVel_B_Healthy AND bVel_C_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := (rPlungerVel_B_ms + rPlungerVel_C_ms) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0004; (* Velocity degraded 1oo2 (Chan A fail) *)
ELSIF bVel_C_Healthy AND bVel_A_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := (rPlungerVel_C_ms + rPlungerVel_A_ms) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0008; (* Velocity degraded 1oo2 (Chan B fail) *)
ELSIF bVel_A_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := rPlungerVel_A_ms;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0010; (* Velocity degraded 1oo1 (Chan A only) *)
ELSIF bVel_B_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := rPlungerVel_B_ms;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0020; (* Velocity degraded 1oo1 (Chan B only) *)
ELSIF bVel_C_Healthy THEN
    bVel_Degraded_1oo2   := TRUE;
    rPlungerVel_Voted_ms := rPlungerVel_C_ms;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0040; (* Velocity degraded 1oo1 (Chan C only) *)
ELSE
    bVel_Failed_Trip     := TRUE;
    rPlungerVel_Voted_ms := 0.0;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0080; (* Velocity complete sensor bank failure *)
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 1.2 Hydraulic Shot Head Pressure 2oo3 Voting Bank (rShotPress_A, B, C)                    *)
(* ----------------------------------------------------------------------------------------- *)
bPress_A_Healthy := (rShotPress_A_bar >= 0.0) AND (rShotPress_A_bar <= 1650.0);
bPress_B_Healthy := (rShotPress_B_bar >= 0.0) AND (rShotPress_B_bar <= 1650.0);
bPress_C_Healthy := (rShotPress_C_bar >= 0.0) AND (rShotPress_C_bar <= 1650.0);

rDev_Press_AB := ABS(rShotPress_A_bar - rShotPress_B_bar);
rDev_Press_BC := ABS(rShotPress_B_bar - rShotPress_C_bar);
rDev_Press_CA := ABS(rShotPress_C_bar - rShotPress_A_bar);

IF bPress_A_Healthy AND bPress_B_Healthy AND bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := FALSE;
    bPress_Failed_Trip   := FALSE;
    IF ((rShotPress_A_bar >= rShotPress_B_bar) AND (rShotPress_A_bar <= rShotPress_C_bar)) OR
       ((rShotPress_A_bar >= rShotPress_C_bar) AND (rShotPress_A_bar <= rShotPress_B_bar)) THEN
        rShotPress_Voted_bar := rShotPress_A_bar;
    ELSIF ((rShotPress_B_bar >= rShotPress_A_bar) AND (rShotPress_B_bar <= rShotPress_C_bar)) OR
          ((rShotPress_B_bar >= rShotPress_C_bar) AND (rShotPress_B_bar <= rShotPress_A_bar)) THEN
        rShotPress_Voted_bar := rShotPress_B_bar;
    ELSE
        rShotPress_Voted_bar := rShotPress_C_bar;
    END_IF;

    IF (rDev_Press_AB > 35.0) OR (rDev_Press_BC > 35.0) OR (rDev_Press_CA > 35.0) THEN
        rTon_Press_Discrep_s := rTon_Press_Discrep_s + rCycleTime_sec;
        IF rTon_Press_Discrep_s >= 0.020 THEN
            dwStatusWord2 := dwStatusWord2 OR 16#0000_0100; (* Pressure triplet discrepancy warning *)
        END_IF;
    ELSE
        rTon_Press_Discrep_s := 0.0;
    END_IF;

ELSIF bPress_A_Healthy AND bPress_B_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := (rShotPress_A_bar + rShotPress_B_bar) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0200;
ELSIF bPress_B_Healthy AND bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := (rShotPress_B_bar + rShotPress_C_bar) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0400;
ELSIF bPress_C_Healthy AND bPress_A_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := (rShotPress_C_bar + rShotPress_A_bar) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_0800;
ELSIF bPress_A_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := rShotPress_A_bar;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_1000;
ELSIF bPress_B_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := rShotPress_B_bar;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_2000;
ELSIF bPress_C_Healthy THEN
    bPress_Degraded_1oo2 := TRUE;
    rShotPress_Voted_bar := rShotPress_C_bar;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_4000;
ELSE
    bPress_Failed_Trip   := TRUE;
    rShotPress_Voted_bar := 0.0;
    dwStatusWord2        := dwStatusWord2 OR 16#0000_8000;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 1.3 Mold Cavity Vacuum Level 2oo3 Voting Bank (rCavityVac_A, B, C)                        *)
(* ----------------------------------------------------------------------------------------- *)
bVac_A_Healthy := (rCavityVac_A_mbar >= 0.5) AND (rCavityVac_A_mbar <= 1050.0);
bVac_B_Healthy := (rCavityVac_B_mbar >= 0.5) AND (rCavityVac_B_mbar <= 1050.0);
bVac_C_Healthy := (rCavityVac_C_mbar >= 0.5) AND (rCavityVac_C_mbar <= 1050.0);

rDev_Vac_AB := ABS(rCavityVac_A_mbar - rCavityVac_B_mbar);
rDev_Vac_BC := ABS(rCavityVac_B_mbar - rCavityVac_C_mbar);
rDev_Vac_CA := ABS(rCavityVac_C_mbar - rCavityVac_A_mbar);

IF bVac_A_Healthy AND bVac_B_Healthy AND bVac_C_Healthy THEN
    bVac_Degraded_1oo2 := FALSE;
    bVac_Failed_Trip   := FALSE;
    IF ((rCavityVac_A_mbar >= rCavityVac_B_mbar) AND (rCavityVac_A_mbar <= rCavityVac_C_mbar)) OR
       ((rCavityVac_A_mbar >= rCavityVac_C_mbar) AND (rCavityVac_A_mbar <= rCavityVac_B_mbar)) THEN
        rCavityVac_Voted_mbar := rCavityVac_A_mbar;
    ELSIF ((rCavityVac_B_mbar >= rCavityVac_A_mbar) AND (rCavityVac_B_mbar <= rCavityVac_C_mbar)) OR
          ((rCavityVac_B_mbar >= rCavityVac_C_mbar) AND (rCavityVac_B_mbar <= rCavityVac_A_mbar)) THEN
        rCavityVac_Voted_mbar := rCavityVac_B_mbar;
    ELSE
        rCavityVac_Voted_mbar := rCavityVac_C_mbar;
    END_IF;

    IF (rDev_Vac_AB > 8.0) OR (rDev_Vac_BC > 8.0) OR (rDev_Vac_CA > 8.0) THEN
        rTon_Vac_Discrep_s := rTon_Vac_Discrep_s + rCycleTime_sec;
        IF rTon_Vac_Discrep_s >= 0.020 THEN
            dwStatusWord2 := dwStatusWord2 OR 16#0001_0000; (* Vacuum discrepancy warning *)
        END_IF;
    ELSE
        rTon_Vac_Discrep_s := 0.0;
    END_IF;

ELSIF bVac_A_Healthy AND bVac_B_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := (rCavityVac_A_mbar + rCavityVac_B_mbar) * 0.5;
    dwStatusWord2         := dwStatusWord2 OR 16#0002_0000;
ELSIF bVac_B_Healthy AND bVac_C_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := (rCavityVac_B_mbar + rCavityVac_C_mbar) * 0.5;
    dwStatusWord2         := dwStatusWord2 OR 16#0004_0000;
ELSIF bVac_C_Healthy AND bVac_A_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := (rCavityVac_C_mbar + rCavityVac_A_mbar) * 0.5;
    dwStatusWord2         := dwStatusWord2 OR 16#0008_0000;
ELSIF bVac_A_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := rCavityVac_A_mbar;
    dwStatusWord2         := dwStatusWord2 OR 16#0010_0000;
ELSIF bVac_B_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := rCavityVac_B_mbar;
    dwStatusWord2         := dwStatusWord2 OR 16#0020_0000;
ELSIF bVac_C_Healthy THEN
    bVac_Degraded_1oo2    := TRUE;
    rCavityVac_Voted_mbar := rCavityVac_C_mbar;
    dwStatusWord2         := dwStatusWord2 OR 16#0040_0000;
ELSE
    bVac_Failed_Trip      := TRUE;
    rCavityVac_Voted_mbar := 1013.25;
    dwStatusWord2         := dwStatusWord2 OR 16#0080_0000;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 1.4 Gross 4-Tie-Bar Clamping Force 2oo3 Voting Bank (rClampForce_A, B, C)                 *)
(* ----------------------------------------------------------------------------------------- *)
bClamp_A_Healthy := (rClampForce_A_kN >= 0.0) AND (rClampForce_A_kN <= 110000.0);
bClamp_B_Healthy := (rClampForce_B_kN >= 0.0) AND (rClampForce_B_kN <= 110000.0);
bClamp_C_Healthy := (rClampForce_C_kN >= 0.0) AND (rClampForce_C_kN <= 110000.0);

rDev_Clamp_AB := ABS(rClampForce_A_kN - rClampForce_B_kN);
rDev_Clamp_BC := ABS(rClampForce_B_kN - rClampForce_C_kN);
rDev_Clamp_CA := ABS(rClampForce_C_kN - rClampForce_A_kN);

IF bClamp_A_Healthy AND bClamp_B_Healthy AND bClamp_C_Healthy THEN
    bClamp_Degraded_1oo2 := FALSE;
    bClamp_Failed_Trip   := FALSE;
    IF ((rClampForce_A_kN >= rClampForce_B_kN) AND (rClampForce_A_kN <= rClampForce_C_kN)) OR
       ((rClampForce_A_kN >= rClampForce_C_kN) AND (rClampForce_A_kN <= rClampForce_B_kN)) THEN
        rClampForce_Voted_kN := rClampForce_A_kN;
    ELSIF ((rClampForce_B_kN >= rClampForce_A_kN) AND (rClampForce_B_kN <= rClampForce_C_kN)) OR
          ((rClampForce_B_kN >= rClampForce_C_kN) AND (rClampForce_B_kN <= rClampForce_A_kN)) THEN
        rClampForce_Voted_kN := rClampForce_B_kN;
    ELSE
        rClampForce_Voted_kN := rClampForce_C_kN;
    END_IF;

    IF (rDev_Clamp_AB > 1200.0) OR (rDev_Clamp_BC > 1200.0) OR (rDev_Clamp_CA > 1200.0) THEN
        rTon_Clamp_Discrep_s := rTon_Clamp_Discrep_s + rCycleTime_sec;
        IF rTon_Clamp_Discrep_s >= 0.020 THEN
            dwStatusWord2 := dwStatusWord2 OR 16#0100_0000; (* Clamp load cell discrepancy warning *)
        END_IF;
    ELSE
        rTon_Clamp_Discrep_s := 0.0;
    END_IF;

ELSIF bClamp_A_Healthy AND bClamp_B_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := (rClampForce_A_kN + rClampForce_B_kN) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0200_0000;
ELSIF bClamp_B_Healthy AND bClamp_C_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := (rClampForce_B_kN + rClampForce_C_kN) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0400_0000;
ELSIF bClamp_C_Healthy AND bClamp_A_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := (rClampForce_C_kN + rClampForce_A_kN) * 0.5;
    dwStatusWord2        := dwStatusWord2 OR 16#0800_0000;
ELSIF bClamp_A_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := rClampForce_A_kN;
    dwStatusWord2        := dwStatusWord2 OR 16#1000_0000;
ELSIF bClamp_B_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := rClampForce_B_kN;
    dwStatusWord2        := dwStatusWord2 OR 16#2000_0000;
ELSIF bClamp_C_Healthy THEN
    bClamp_Degraded_1oo2 := TRUE;
    rClampForce_Voted_kN := rClampForce_C_kN;
    dwStatusWord2        := dwStatusWord2 OR 16#4000_0000;
ELSE
    bClamp_Failed_Trip   := TRUE;
    rClampForce_Voted_kN := 0.0;
    dwStatusWord2        := dwStatusWord2 OR 16#8000_0000;
END_IF;

(* ----------------------------------------------------------------------------------------- *)
(* 1.5 Individual 4-Tie-Bar Load Balancing, Eccentricity & Bending Moments                   *)
(* ----------------------------------------------------------------------------------------- *)
(* Tie-Bar Geometry:                                                                         *)
(*   TB1: Top-Left       TB2: Top-Right                                                      *)
(*   TB3: Bottom-Left    TB4: Bottom-Right                                                   *)
(* Evaluates dynamic load distribution across all four 750 mm diameter tie-bars.             *)

rTieBar_Mean_kN := (rTieBarForce_TB1_kN + rTieBarForce_TB2_kN + rTieBarForce_TB3_kN + rTieBarForce_TB4_kN) * 0.25;

rTieBar_Dev_TB1 := rTieBarForce_TB1_kN - rTieBar_Mean_kN;
rTieBar_Dev_TB2 := rTieBarForce_TB2_kN - rTieBar_Mean_kN;
rTieBar_Dev_TB3 := rTieBarForce_TB3_kN - rTieBar_Mean_kN;
rTieBar_Dev_TB4 := rTieBarForce_TB4_kN - rTieBar_Mean_kN;

(* Dynamic Platen Tilting & Torsional Warping Forces [kN] *)
rEccentricity_Horiz_kN := ABS((rTieBarForce_TB1_kN + rTieBarForce_TB3_kN) - (rTieBarForce_TB2_kN + rTieBarForce_TB4_kN));
rEccentricity_Vert_kN  := ABS((rTieBarForce_TB1_kN + rTieBarForce_TB2_kN) - (rTieBarForce_TB3_kN + rTieBarForce_TB4_kN));
rEccentricity_Diag_kN  := ABS((rTieBarForce_TB1_kN + rTieBarForce_TB4_kN) - (rTieBarForce_TB2_kN + rTieBarForce_TB3_kN));

(* Peak Dynamic Eccentricity Evaluation *)
rTieBarMaxEccentricity_kN := rEccentricity_Horiz_kN;
IF rEccentricity_Vert_kN > rTieBarMaxEccentricity_kN THEN
    rTieBarMaxEccentricity_kN := rEccentricity_Vert_kN;
END_IF;
IF rEccentricity_Diag_kN > rTieBarMaxEccentricity_kN THEN
    rTieBarMaxEccentricity_kN := rEccentricity_Diag_kN;
END_IF;

(* Active Hydraulic Balancing Nut Servo Trimming (Closed-Loop PI Compensation) *)
IF (iState >= c_STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN) AND 
   (iState <= c_STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD) AND 
   NOT bSystemTripped THEN

    (* TB1 Trimming *)
    rTieBar_Integral_TB1 := rTieBar_Integral_TB1 + (-1.0 * rTieBar_Dev_TB1 * 0.00025 * rCycleTime_sec);
    IF rTieBar_Integral_TB1 > 8.0 THEN rTieBar_Integral_TB1 := 8.0; END_IF;
    IF rTieBar_Integral_TB1 < -8.0 THEN rTieBar_Integral_TB1 := -8.0; END_IF;
    rTieBar1_HydNut_pct := 50.0 + (-0.0085 * rTieBar_Dev_TB1) + rTieBar_Integral_TB1;

    (* TB2 Trimming *)
    rTieBar_Integral_TB2 := rTieBar_Integral_TB2 + (-1.0 * rTieBar_Dev_TB2 * 0.00025 * rCycleTime_sec);
    IF rTieBar_Integral_TB2 > 8.0 THEN rTieBar_Integral_TB2 := 8.0; END_IF;
    IF rTieBar_Integral_TB2 < -8.0 THEN rTieBar_Integral_TB2 := -8.0; END_IF;
    rTieBar2_HydNut_pct := 50.0 + (-0.0085 * rTieBar_Dev_TB2) + rTieBar_Integral_TB2;

    (* TB3 Trimming *)
    rTieBar_Integral_TB3 := rTieBar_Integral_TB3 + (-1.0 * rTieBar_Dev_TB3 * 0.00025 * rCycleTime_sec);
    IF rTieBar_Integral_TB3 > 8.0 THEN rTieBar_Integral_TB3 := 8.0; END_IF;
    IF rTieBar_Integral_TB3 < -8.0 THEN rTieBar_Integral_TB3 := -8.0; END_IF;
    rTieBar3_HydNut_pct := 50.0 + (-0.0085 * rTieBar_Dev_TB3) + rTieBar_Integral_TB3;

    (* TB4 Trimming *)
    rTieBar_Integral_TB4 := rTieBar_Integral_TB4 + (-1.0 * rTieBar_Dev_TB4 * 0.00025 * rCycleTime_sec);
    IF rTieBar_Integral_TB4 > 8.0 THEN rTieBar_Integral_TB4 := 8.0; END_IF;
    IF rTieBar_Integral_TB4 < -8.0 THEN rTieBar_Integral_TB4 := -8.0; END_IF;
    rTieBar4_HydNut_pct := 50.0 + (-0.0085 * rTieBar_Dev_TB4) + rTieBar_Integral_TB4;

    (* Bound Actuator Commands [0..100%] *)
    IF rTieBar1_HydNut_pct < 0.0 THEN rTieBar1_HydNut_pct := 0.0; END_IF;
    IF rTieBar1_HydNut_pct > 100.0 THEN rTieBar1_HydNut_pct := 100.0; END_IF;
    IF rTieBar2_HydNut_pct < 0.0 THEN rTieBar2_HydNut_pct := 0.0; END_IF;
    IF rTieBar2_HydNut_pct > 100.0 THEN rTieBar2_HydNut_pct := 100.0; END_IF;
    IF rTieBar3_HydNut_pct < 0.0 THEN rTieBar3_HydNut_pct := 0.0; END_IF;
    IF rTieBar3_HydNut_pct > 100.0 THEN rTieBar3_HydNut_pct := 100.0; END_IF;
    IF rTieBar4_HydNut_pct < 0.0 THEN rTieBar4_HydNut_pct := 0.0; END_IF;
    IF rTieBar4_HydNut_pct > 100.0 THEN rTieBar4_HydNut_pct := 100.0; END_IF;
ELSE
    rTieBar1_HydNut_pct := 0.0;
    rTieBar2_HydNut_pct := 0.0;
    rTieBar3_HydNut_pct := 0.0;
    rTieBar4_HydNut_pct := 0.0;
    rTieBar_Integral_TB1 := 0.0;
    rTieBar_Integral_TB2 := 0.0;
    rTieBar_Integral_TB3 := 0.0;
    rTieBar_Integral_TB4 := 0.0;
END_IF;
"""

if __name__ == "__main__":
    print("Section 0 len:", len(get_section0()))
    print("Section 1 len:", len(get_section1()))
