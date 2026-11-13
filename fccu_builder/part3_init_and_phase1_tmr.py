# fccu_builder/part3_init_and_phase1_tmr.py

def get_part3_init_and_phase1_tmr():
    lines = []
    lines.append("""(*
========================================================================================================================
  PHASE 0: FIRST-SCAN DETERMINISTIC MATRIX INITIALIZATION & CYBER-PHYSICAL CALIBRATION
========================================================================================================================
*)
IF NOT bFirstScanInitDone THEN
    (* 1. Plant Transition Matrix A (8x8) Discrete State Evolution (Ts = 25 ms) *)
    (* x1: Riser Outlet Temperature [deg C] *)
    A_Matrix[1, 1] := 0.988500; A_Matrix[1, 2] := -0.003400; A_Matrix[1, 3] := 0.006200; A_Matrix[1, 4] := 0.002800;
    A_Matrix[1, 5] := 0.001100; A_Matrix[1, 6] := 0.004500; A_Matrix[1, 7] := 0.000000; A_Matrix[1, 8] := -0.000002;

    (* x2: Riser Top Differential Pressure [kPa] *)
    A_Matrix[2, 1] := 0.002200; A_Matrix[2, 2] := 0.975000; A_Matrix[2, 3] := 0.000800; A_Matrix[2, 4] := 0.000400;
    A_Matrix[2, 5] := -0.003500; A_Matrix[2, 6] := 0.007800; A_Matrix[2, 7] := 0.000000; A_Matrix[2, 8] := 0.000000;

    (* x3: Regenerator 1st Stage Dense Bed Temperature [deg C] *)
    A_Matrix[3, 1] := 0.001500; A_Matrix[3, 2] := 0.000600; A_Matrix[3, 3] := 0.991200; A_Matrix[3, 4] := 0.004800;
    A_Matrix[3, 5] := 0.005200; A_Matrix[3, 6] := -0.003100; A_Matrix[3, 7] := 0.012500; A_Matrix[3, 8] := 0.000015;

    (* x4: Regenerator 2nd Stage Dense Bed Temperature [deg C] *)
    A_Matrix[4, 1] := 0.000800; A_Matrix[4, 2] := 0.000300; A_Matrix[4, 3] := 0.006500; A_Matrix[4, 4] := 0.989500;
    A_Matrix[4, 5] := 0.002100; A_Matrix[4, 6] := -0.004200; A_Matrix[4, 7] := 0.018200; A_Matrix[4, 8] := 0.000022;

    (* x5: Spent Catalyst Slide Valve Differential Pressure (dP_SCSV) [kPa] *)
    A_Matrix[5, 1] := 0.000500; A_Matrix[5, 2] := -0.004800; A_Matrix[5, 3] := -0.002500; A_Matrix[5, 4] := -0.001800;
    A_Matrix[5, 5] := 0.982000; A_Matrix[5, 6] := 0.006500; A_Matrix[5, 7] := -0.001200; A_Matrix[5, 8] := 0.000000;

    (* x6: Regenerated Catalyst Slide Valve Differential Pressure (dP_RCSV) [kPa] *)
    A_Matrix[6, 1] := -0.002800; A_Matrix[6, 2] := -0.006200; A_Matrix[6, 3] := 0.003800; A_Matrix[6, 4] := 0.004200;
    A_Matrix[6, 5] := 0.005800; A_Matrix[6, 6] := 0.981500; A_Matrix[6, 7] := 0.001500; A_Matrix[6, 8] := 0.000000;

    (* x7: Regenerator Flue Gas Excess Oxygen Content [% O2] *)
    A_Matrix[7, 1] := 0.000000; A_Matrix[7, 2] := 0.000000; A_Matrix[7, 3] := -0.002400; A_Matrix[7, 4] := -0.003100;
    A_Matrix[7, 5] := -0.001500; A_Matrix[7, 6] := 0.000800; A_Matrix[7, 7] := 0.965000; A_Matrix[7, 8] := -0.000045;

    (* x8: Combustion Flue Gas Carbon Monoxide Concentration [ppmv] *)
    A_Matrix[8, 1] := 0.000000; A_Matrix[8, 2] := 0.000000; A_Matrix[8, 3] := -0.045000; A_Matrix[8, 4] := -0.052000;
    A_Matrix[8, 5] := 0.082000; A_Matrix[8, 6] := -0.024000; A_Matrix[8, 7] := -1.850000; A_Matrix[8, 8] := 0.942000;

    (* 2. Input Coupling Transmission Matrix B (8x6) *)
    (* u1: RCSV [%], u2: SCSV [%], u3: Air Blower [%], u4: Torch Oil [%], u5: Lift Steam [%], u6: Flue Gas Slide Valve [%] *)
    B_Matrix[1, 1] := 0.038500; B_Matrix[1, 2] := -0.004200; B_Matrix[1, 3] := 0.001500; B_Matrix[1, 4] := 0.000800; B_Matrix[1, 5] := -0.012500; B_Matrix[1, 6] := 0.000600;
    B_Matrix[2, 1] := 0.024500; B_Matrix[2, 2] := 0.001800; B_Matrix[2, 3] := 0.000400; B_Matrix[2, 4] := 0.000200; B_Matrix[2, 5] := -0.038000; B_Matrix[2, 6] := -0.004500;
    B_Matrix[3, 1] := -0.015000; B_Matrix[3, 2] := 0.042000; B_Matrix[3, 3] := 0.035000; B_Matrix[3, 4] := 0.058000; B_Matrix[3, 5] := 0.000000; B_Matrix[3, 6] := 0.002200;
    B_Matrix[4, 1] := -0.018500; B_Matrix[4, 2] := 0.031000; B_Matrix[4, 3] := 0.048000; B_Matrix[4, 4] := 0.042000; B_Matrix[4, 5] := 0.000000; B_Matrix[4, 6] := 0.003500;
    B_Matrix[5, 1] := 0.008500; B_Matrix[5, 2] := -0.065000; B_Matrix[5, 3] := -0.012000; B_Matrix[5, 4] := -0.005000; B_Matrix[5, 5] := 0.004200; B_Matrix[5, 6] := 0.045000;
    B_Matrix[6, 1] := -0.072000; B_Matrix[6, 2] := 0.011000; B_Matrix[6, 3] := 0.018000; B_Matrix[6, 4] := 0.008000; B_Matrix[6, 5] := -0.008500; B_Matrix[6, 6] := -0.052000;
    B_Matrix[7, 1] := -0.000800; B_Matrix[7, 2] := -0.004500; B_Matrix[7, 3] := 0.024000; B_Matrix[7, 4] := -0.032000; B_Matrix[7, 5] := 0.000000; B_Matrix[7, 6] := 0.001100;
    B_Matrix[8, 1] := 0.022000; B_Matrix[8, 2] := 0.185000; B_Matrix[8, 3] := -0.420000; B_Matrix[8, 4] := 0.125000; B_Matrix[8, 5] := 0.000000; B_Matrix[8, 6] := -0.015000;

    (* 3. Output Observation Matrix C (6x8) *)
    (* y1: Riser Temp, y2: Riser DP, y3: Regen Bed Temp, y4: SCSV DP, y5: RCSV DP, y6: Flue Gas O2 *)
    C_Matrix[1, 1] := 1.000000; C_Matrix[1, 2] := 0.000000; C_Matrix[1, 3] := 0.000000; C_Matrix[1, 4] := 0.000000; C_Matrix[1, 5] := 0.000000; C_Matrix[1, 6] := 0.000000; C_Matrix[1, 7] := 0.000000; C_Matrix[1, 8] := 0.000000;
    C_Matrix[2, 1] := 0.000000; C_Matrix[2, 2] := 1.000000; C_Matrix[2, 3] := 0.000000; C_Matrix[2, 4] := 0.000000; C_Matrix[2, 5] := 0.000000; C_Matrix[2, 6] := 0.000000; C_Matrix[2, 7] := 0.000000; C_Matrix[2, 8] := 0.000000;
    C_Matrix[3, 1] := 0.000000; C_Matrix[3, 2] := 0.000000; C_Matrix[3, 3] := 1.000000; C_Matrix[3, 4] := 0.000000; C_Matrix[3, 5] := 0.000000; C_Matrix[3, 6] := 0.000000; C_Matrix[3, 7] := 0.000000; C_Matrix[3, 8] := 0.000000;
    C_Matrix[4, 1] := 0.000000; C_Matrix[4, 2] := 0.000000; C_Matrix[4, 3] := 0.000000; C_Matrix[4, 4] := 0.000000; C_Matrix[4, 5] := 1.000000; C_Matrix[4, 6] := 0.000000; C_Matrix[4, 7] := 0.000000; C_Matrix[4, 8] := 0.000000;
    C_Matrix[5, 1] := 0.000000; C_Matrix[5, 2] := 0.000000; C_Matrix[3, 3] := 0.000000; C_Matrix[5, 4] := 0.000000; C_Matrix[5, 5] := 0.000000; C_Matrix[5, 6] := 1.000000; C_Matrix[5, 7] := 0.000000; C_Matrix[5, 8] := 0.000000;
    C_Matrix[6, 1] := 0.000000; C_Matrix[6, 2] := 0.000000; C_Matrix[6, 3] := 0.000000; C_Matrix[6, 4] := 0.000000; C_Matrix[6, 5] := 0.000000; C_Matrix[6, 6] := 0.000000; C_Matrix[6, 7] := 1.000000; C_Matrix[6, 8] := 0.000000;

    (* 4. Direct High-Frequency Feedthrough Matrix D (6x6) *)
    FOR iIdx := 1 TO 6 DO
        FOR jIdx := 1 TO 6 DO
            IF iIdx = jIdx THEN
                D_Matrix[iIdx, jIdx] := 0.000500;
            ELSE
                D_Matrix[iIdx, jIdx] := 0.000000;
            END_IF;
        END_FOR;
    END_FOR;

    (* 5. Steady-State Luenberger Observer Innovation Matrix L (8x6) *)
    L_Matrix[1, 1] := 0.125000; L_Matrix[1, 2] := 0.004200; L_Matrix[1, 3] := 0.001800; L_Matrix[1, 4] := 0.000500; L_Matrix[1, 5] := 0.001200; L_Matrix[1, 6] := 0.000000;
    L_Matrix[2, 1] := 0.003500; L_Matrix[2, 2] := 0.145000; L_Matrix[2, 3] := 0.000400; L_Matrix[2, 4] := -0.002200; L_Matrix[2, 5] := 0.004500; L_Matrix[2, 6] := 0.000000;
    L_Matrix[3, 1] := 0.001800; L_Matrix[3, 2] := 0.000600; L_Matrix[3, 3] := 0.118000; L_Matrix[3, 4] := 0.003200; L_Matrix[3, 5] := -0.001500; L_Matrix[3, 6] := 0.008500;
    L_Matrix[4, 1] := 0.001200; L_Matrix[4, 2] := 0.000300; L_Matrix[4, 3] := 0.045000; L_Matrix[4, 4] := 0.001800; L_Matrix[4, 5] := -0.002800; L_Matrix[4, 6] := 0.012500;
    L_Matrix[5, 1] := 0.000600; L_Matrix[5, 2] := -0.003800; L_Matrix[5, 3] := 0.001500; L_Matrix[5, 4] := 0.138000; L_Matrix[5, 5] := 0.008500; L_Matrix[5, 6] := -0.000800;
    L_Matrix[6, 1] := -0.001500; L_Matrix[6, 2] := 0.004200; L_Matrix[6, 3] := -0.002200; L_Matrix[6, 4] := 0.007800; L_Matrix[6, 5] := 0.142000; L_Matrix[6, 6] := 0.001100;
    L_Matrix[7, 1] := 0.000000; L_Matrix[7, 2] := 0.000000; L_Matrix[7, 3] := -0.001800; L_Matrix[7, 4] := -0.000500; L_Matrix[7, 5] := 0.000800; L_Matrix[7, 6] := 0.165000;
    L_Matrix[8, 1] := 0.000000; L_Matrix[8, 2] := 0.000000; L_Matrix[8, 3] := -0.025000; L_Matrix[8, 4] := 0.012000; L_Matrix[8, 5] := -0.008000; L_Matrix[8, 6] := -0.850000;

    (* 6. MPC Quadratic Cost Matrix Diagonal Weights *)
    Q_diag[1] := 18.0; (* Riser Outlet Temperature Tracking Weight *)
    Q_diag[2] := 6.5;  (* Riser Top Differential Pressure Tracking Weight *)
    Q_diag[3] := 14.0; (* Regenerator 1st Bed Temp Tracking Weight *)
    Q_diag[4] := 8.0;  (* Regenerator 2nd Bed Temp Tracking Weight *)
    Q_diag[5] := 35.0; (* Spent Catalyst Slide Valve DP Seal Weight *)
    Q_diag[6] := 38.0; (* Regenerated Catalyst Slide Valve DP Seal Weight *)
    Q_diag[7] := 25.0; (* Flue Gas Excess Oxygen Tracking Weight *)
    Q_diag[8] := 0.05; (* Flue Gas CO Concentration Minimization Weight *)

    R_diag[1] := 8.5;  (* RCSV Actuator Slew Rate Penalty Weight *)
    R_diag[2] := 8.5;  (* SCSV Actuator Slew Rate Penalty Weight *)
    R_diag[3] := 4.2;  (* Air Blower Vane Slew Rate Penalty Weight *)
    R_diag[4] := 2.5;  (* Torch Oil Fuel Slew Rate Penalty Weight *)
    R_diag[5] := 5.0;  (* Lift Steam Slew Rate Penalty Weight *)
    R_diag[6] := 6.0;  (* Flue Gas Slide Valve Slew Rate Penalty Weight *)

    P_diag[1] := 32.0; P_diag[2] := 12.0; P_diag[3] := 28.0; P_diag[4] := 16.0;
    P_diag[5] := 75.0; P_diag[6] := 80.0; P_diag[7] := 48.0; P_diag[8] := 0.10;

    (* Actuator Hard Mechanical Boundaries & Slew Rates per Scan (Ts = 25 ms) *)
    u_min[1] := 0.0; u_max[1] := 100.0; du_max[1] := rSlewRate_RCSV_pct_s * rTs_sec;
    u_min[2] := 0.0; u_max[2] := 100.0; du_max[2] := rSlewRate_SCSV_pct_s * rTs_sec;
    u_min[3] := 0.0; u_max[3] := 100.0; du_max[3] := rSlewRate_AirBlower_pct_s * rTs_sec;
    u_min[4] := 0.0; u_max[4] := 100.0; du_max[4] := rSlewRate_TorchOil_pct_s * rTs_sec;
    u_min[5] := 0.0; u_max[5] := 100.0; du_max[5] := rSlewRate_LiftSteam_pct_s * rTs_sec;
    u_min[6] := 0.0; u_max[6] := 100.0; du_max[6] := rSlewRate_FlueGasValve_pct_s * rTs_sec;

    (* Initial Setpoint Vector Vector Defaults *)
    x_sp[1] := 528.0; (* Baseline Target Riser Outlet Temp [deg C] *)
    x_sp[2] := 48.0;  (* Baseline Target Riser Top DP [kPa] *)
    x_sp[3] := 715.0; (* Baseline Target Regen Stage 1 Bed Temp [deg C] *)
    x_sp[4] := 728.0; (* Baseline Target Regen Stage 2 Bed Temp [deg C] *)
    x_sp[5] := 52.0;  (* Baseline Target Spent Valve DP [kPa] *)
    x_sp[6] := 55.0;  (* Baseline Target Regen Valve DP [kPa] *)
    x_sp[7] := 1.65;  (* Baseline Target Flue Gas Excess Oxygen [% O2] *)
    x_sp[8] := 85.0;  (* Baseline Target Flue Gas CO [ppmv] *)

    (* Initialize State Estimates to Default Baseline *)
    FOR iIdx := 1 TO 8 DO
        x_hat[iIdx] := x_sp[iIdx];
        x_pred[iIdx] := x_sp[iIdx];
    END_FOR;

    FOR mIdx := 1 TO 6 DO
        u_cmd[mIdx] := 0.0;
        u_prev[mIdx] := 0.0;
        u_opt[mIdx] := 0.0;
    END_FOR;

    bFirstScanInitDone := TRUE;
END_IF;

(* Update Target Setpoints from Operator VAR_INPUT if Valid *)
IF rTargetRiserTemp_degC >= 480.0 AND rTargetRiserTemp_degC <= 560.0 THEN
    x_sp[1] := rTargetRiserTemp_degC;
END_IF;
IF rTargetSlideValveDP_kPa >= 35.0 AND rTargetSlideValveDP_kPa <= 70.0 THEN
    x_sp[5] := rTargetSlideValveDP_kPa;
    x_sp[6] := rTargetSlideValveDP_kPa;
END_IF;
IF rTargetRegenTemp_degC >= 640.0 AND rTargetRegenTemp_degC <= 760.0 THEN
    x_sp[3] := rTargetRegenTemp_degC;
    x_sp[4] := rTargetRegenTemp_degC + 10.0;
END_IF;
IF rTargetFlueGasO2_pct >= 0.5 AND rTargetFlueGasO2_pct <= 4.0 THEN
    x_sp[7] := rTargetFlueGasO2_pct;
END_IF;

(*
========================================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS
========================================================================================================================
*)
(* ---------------------------------------------------------------------------------------------------------------------
   1.1 Riser Outlet Temperature Transmitters (TT_RISER_101A / TT_RISER_101B / TT_RISER_101C) [deg C]
   --------------------------------------------------------------------------------------------------------------------- *)
(* Sanity Range Check on Raw Channels *)
bChannelFault_TT101A := (rTT_RISER_101A_degC < rTT_RISER_Min_degC) OR (rTT_RISER_101A_degC > rTT_RISER_Max_degC);
bChannelFault_TT101B := (rTT_RISER_101B_degC < rTT_RISER_Min_degC) OR (rTT_RISER_101B_degC > rTT_RISER_Max_degC);
bChannelFault_TT101C := (rTT_RISER_101C_degC < rTT_RISER_Min_degC) OR (rTT_RISER_101C_degC > rTT_RISER_Max_degC);

(* Pairwise Discordance Checks *)
bDiscrep_TT101_AB := ABS(rTT_RISER_101A_degC - rTT_RISER_101B_degC) > rDiscrepancyTol_TT101_degC;
bDiscrep_TT101_BC := ABS(rTT_RISER_101B_degC - rTT_RISER_101C_degC) > rDiscrepancyTol_TT101_degC;
bDiscrep_TT101_AC := ABS(rTT_RISER_101A_degC - rTT_RISER_101C_degC) > rDiscrepancyTol_TT101_degC;

(* Discordance Accumulation Timers (Threshold: 300 ms = 0.300 s) *)
IF bDiscrep_TT101_AB THEN
    rTimer_TT101_AB_sec := rTimer_TT101_AB_sec + rTs_sec;
ELSE
    rTimer_TT101_AB_sec := 0.0;
END_IF;

IF bDiscrep_TT101_BC THEN
    rTimer_TT101_BC_sec := rTimer_TT101_BC_sec + rTs_sec;
ELSE
    rTimer_TT101_BC_sec := 0.0;
END_IF;

IF bDiscrep_TT101_AC THEN
    rTimer_TT101_AC_sec := rTimer_TT101_AC_sec + rTs_sec;
ELSE
    rTimer_TT101_AC_sec := 0.0;
END_IF;

(* Automatic Fault Isolation on Persistent Discordance *)
IF (rTimer_TT101_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT101_AC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT101A := TRUE;
END_IF;
IF (rTimer_TT101_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT101_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT101B := TRUE;
END_IF;
IF (rTimer_TT101_AC_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT101_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT101C := TRUE;
END_IF;

(* 2oo3 Bumpless Voting Logic Execution *)
IF NOT bChannelFault_TT101A AND NOT bChannelFault_TT101B AND NOT bChannelFault_TT101C THEN
    (* All 3 Channels Healthy: Exact Median Selection *)
    IF (rTT_RISER_101A_degC >= rTT_RISER_101B_degC AND rTT_RISER_101A_degC <= rTT_RISER_101C_degC) OR 
       (rTT_RISER_101A_degC <= rTT_RISER_101B_degC AND rTT_RISER_101A_degC >= rTT_RISER_101C_degC) THEN
        rVoted_RiserTemp_degC := rTT_RISER_101A_degC;
    ELSIF (rTT_RISER_101B_degC >= rTT_RISER_101A_degC AND rTT_RISER_101B_degC <= rTT_RISER_101C_degC) OR 
          (rTT_RISER_101B_degC <= rTT_RISER_101A_degC AND rTT_RISER_101B_degC >= rTT_RISER_101C_degC) THEN
        rVoted_RiserTemp_degC := rTT_RISER_101B_degC;
    ELSE
        rVoted_RiserTemp_degC := rTT_RISER_101C_degC;
    END_IF;
ELSIF NOT bChannelFault_TT101A AND NOT bChannelFault_TT101B THEN
    rVoted_RiserTemp_degC := 0.5 * (rTT_RISER_101A_degC + rTT_RISER_101B_degC);
ELSIF NOT bChannelFault_TT101A AND NOT bChannelFault_TT101C THEN
    rVoted_RiserTemp_degC := 0.5 * (rTT_RISER_101A_degC + rTT_RISER_101C_degC);
ELSIF NOT bChannelFault_TT101B AND NOT bChannelFault_TT101C THEN
    rVoted_RiserTemp_degC := 0.5 * (rTT_RISER_101B_degC + rTT_RISER_101C_degC);
ELSIF NOT bChannelFault_TT101A THEN
    rVoted_RiserTemp_degC := rTT_RISER_101A_degC;
ELSIF NOT bChannelFault_TT101B THEN
    rVoted_RiserTemp_degC := rTT_RISER_101B_degC;
ELSIF NOT bChannelFault_TT101C THEN
    rVoted_RiserTemp_degC := rTT_RISER_101C_degC;
ELSE
    (* All Channels Tripped: Hold Last Valid Posterior Observer Value *)
    rVoted_RiserTemp_degC := x_hat[1];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   1.2 Regenerator Stage 1 Dense Bed Temperature Transmitters (TT_REGEN_201A / B / C) [deg C]
   --------------------------------------------------------------------------------------------------------------------- *)
bChannelFault_TT201A := (rTT_REGEN_201A_degC < rTT_REGEN_Min_degC) OR (rTT_REGEN_201A_degC > rTT_REGEN_Max_degC);
bChannelFault_TT201B := (rTT_REGEN_201B_degC < rTT_REGEN_Min_degC) OR (rTT_REGEN_201B_degC > rTT_REGEN_Max_degC);
bChannelFault_TT201C := (rTT_REGEN_201C_degC < rTT_REGEN_Min_degC) OR (rTT_REGEN_201C_degC > rTT_REGEN_Max_degC);

bDiscrep_TT201_AB := ABS(rTT_REGEN_201A_degC - rTT_REGEN_201B_degC) > rDiscrepancyTol_TT201_degC;
bDiscrep_TT201_BC := ABS(rTT_REGEN_201B_degC - rTT_REGEN_201C_degC) > rDiscrepancyTol_TT201_degC;
bDiscrep_TT201_AC := ABS(rTT_REGEN_201A_degC - rTT_REGEN_201C_degC) > rDiscrepancyTol_TT201_degC;

IF bDiscrep_TT201_AB THEN
    rTimer_TT201_AB_sec := rTimer_TT201_AB_sec + rTs_sec;
ELSE
    rTimer_TT201_AB_sec := 0.0;
END_IF;

IF bDiscrep_TT201_BC THEN
    rTimer_TT201_BC_sec := rTimer_TT201_BC_sec + rTs_sec;
ELSE
    rTimer_TT201_BC_sec := 0.0;
END_IF;

IF bDiscrep_TT201_AC THEN
    rTimer_TT201_AC_sec := rTimer_TT201_AC_sec + rTs_sec;
ELSE
    rTimer_TT201_AC_sec := 0.0;
END_IF;

IF (rTimer_TT201_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT201_AC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT201A := TRUE;
END_IF;
IF (rTimer_TT201_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT201_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT201B := TRUE;
END_IF;
IF (rTimer_TT201_AC_sec >= rDiscrepancyTripTime_sec) AND (rTimer_TT201_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_TT201C := TRUE;
END_IF;

IF NOT bChannelFault_TT201A AND NOT bChannelFault_TT201B AND NOT bChannelFault_TT201C THEN
    IF (rTT_REGEN_201A_degC >= rTT_REGEN_201B_degC AND rTT_REGEN_201A_degC <= rTT_REGEN_201C_degC) OR 
       (rTT_REGEN_201A_degC <= rTT_REGEN_201B_degC AND rTT_REGEN_201A_degC >= rTT_REGEN_201C_degC) THEN
        rVoted_RegenBedTemp_degC := rTT_REGEN_201A_degC;
    ELSIF (rTT_REGEN_201B_degC >= rTT_REGEN_201A_degC AND rTT_REGEN_201B_degC <= rTT_REGEN_201C_degC) OR 
          (rTT_REGEN_201B_degC <= rTT_REGEN_201A_degC AND rTT_REGEN_201B_degC >= rTT_REGEN_201C_degC) THEN
        rVoted_RegenBedTemp_degC := rTT_REGEN_201B_degC;
    ELSE
        rVoted_RegenBedTemp_degC := rTT_REGEN_201C_degC;
    END_IF;
ELSIF NOT bChannelFault_TT201A AND NOT bChannelFault_TT201B THEN
    rVoted_RegenBedTemp_degC := 0.5 * (rTT_REGEN_201A_degC + rTT_REGEN_201B_degC);
ELSIF NOT bChannelFault_TT201A AND NOT bChannelFault_TT201C THEN
    rVoted_RegenBedTemp_degC := 0.5 * (rTT_REGEN_201A_degC + rTT_REGEN_201C_degC);
ELSIF NOT bChannelFault_TT201B AND NOT bChannelFault_TT201C THEN
    rVoted_RegenBedTemp_degC := 0.5 * (rTT_REGEN_201B_degC + rTT_REGEN_201C_degC);
ELSIF NOT bChannelFault_TT201A THEN
    rVoted_RegenBedTemp_degC := rTT_REGEN_201A_degC;
ELSIF NOT bChannelFault_TT201B THEN
    rVoted_RegenBedTemp_degC := rTT_REGEN_201B_degC;
ELSIF NOT bChannelFault_TT201C THEN
    rVoted_RegenBedTemp_degC := rTT_REGEN_201C_degC;
ELSE
    rVoted_RegenBedTemp_degC := x_hat[3];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   1.3 Spent Catalyst Slide Valve Differential Pressure Transmitters (PDT_SCSV_301A / B / C) [kPa]
   --------------------------------------------------------------------------------------------------------------------- *)
bChannelFault_PDT301A := (rPDT_SCSV_301A_kPa < rPDT_SCSV_Min_kPa) OR (rPDT_SCSV_301A_kPa > rPDT_SCSV_Max_kPa);
bChannelFault_PDT301B := (rPDT_SCSV_301B_kPa < rPDT_SCSV_Min_kPa) OR (rPDT_SCSV_301B_kPa > rPDT_SCSV_Max_kPa);
bChannelFault_PDT301C := (rPDT_SCSV_301C_kPa < rPDT_SCSV_Min_kPa) OR (rPDT_SCSV_301C_kPa > rPDT_SCSV_Max_kPa);

bDiscrep_PDT301_AB := ABS(rPDT_SCSV_301A_kPa - rPDT_SCSV_301B_kPa) > rDiscrepancyTol_PDT301_kPa;
bDiscrep_PDT301_BC := ABS(rPDT_SCSV_301B_kPa - rPDT_SCSV_301C_kPa) > rDiscrepancyTol_PDT301_kPa;
bDiscrep_PDT301_AC := ABS(rPDT_SCSV_301A_kPa - rPDT_SCSV_301C_kPa) > rDiscrepancyTol_PDT301_kPa;

IF bDiscrep_PDT301_AB THEN
    rTimer_PDT301_AB_sec := rTimer_PDT301_AB_sec + rTs_sec;
ELSE
    rTimer_PDT301_AB_sec := 0.0;
END_IF;

IF bDiscrep_PDT301_BC THEN
    rTimer_PDT301_BC_sec := rTimer_PDT301_BC_sec + rTs_sec;
ELSE
    rTimer_PDT301_BC_sec := 0.0;
END_IF;

IF bDiscrep_PDT301_AC THEN
    rTimer_PDT301_AC_sec := rTimer_PDT301_AC_sec + rTs_sec;
ELSE
    rTimer_PDT301_AC_sec := 0.0;
END_IF;

IF (rTimer_PDT301_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT301_AC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT301A := TRUE;
END_IF;
IF (rTimer_PDT301_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT301_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT301B := TRUE;
END_IF;
IF (rTimer_PDT301_AC_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT301_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT301C := TRUE;
END_IF;

IF NOT bChannelFault_PDT301A AND NOT bChannelFault_PDT301B AND NOT bChannelFault_PDT301C THEN
    IF (rPDT_SCSV_301A_kPa >= rPDT_SCSV_301B_kPa AND rPDT_SCSV_301A_kPa <= rPDT_SCSV_301C_kPa) OR 
       (rPDT_SCSV_301A_kPa <= rPDT_SCSV_301B_kPa AND rPDT_SCSV_301A_kPa >= rPDT_SCSV_301C_kPa) THEN
        rVoted_SCSV_dP_kPa := rPDT_SCSV_301A_kPa;
    ELSIF (rPDT_SCSV_301B_kPa >= rPDT_SCSV_301A_kPa AND rPDT_SCSV_301B_kPa <= rPDT_SCSV_301C_kPa) OR 
          (rPDT_SCSV_301B_kPa <= rPDT_SCSV_301A_kPa AND rPDT_SCSV_301B_kPa >= rPDT_SCSV_301C_kPa) THEN
        rVoted_SCSV_dP_kPa := rPDT_SCSV_301B_kPa;
    ELSE
        rVoted_SCSV_dP_kPa := rPDT_SCSV_301C_kPa;
    END_IF;
ELSIF NOT bChannelFault_PDT301A AND NOT bChannelFault_PDT301B THEN
    rVoted_SCSV_dP_kPa := 0.5 * (rPDT_SCSV_301A_kPa + rPDT_SCSV_301B_kPa);
ELSIF NOT bChannelFault_PDT301A AND NOT bChannelFault_PDT301C THEN
    rVoted_SCSV_dP_kPa := 0.5 * (rPDT_SCSV_301A_kPa + rPDT_SCSV_301C_kPa);
ELSIF NOT bChannelFault_PDT301B AND NOT bChannelFault_PDT301C THEN
    rVoted_SCSV_dP_kPa := 0.5 * (rPDT_SCSV_301B_kPa + rPDT_SCSV_301C_kPa);
ELSIF NOT bChannelFault_PDT301A THEN
    rVoted_SCSV_dP_kPa := rPDT_SCSV_301A_kPa;
ELSIF NOT bChannelFault_PDT301B THEN
    rVoted_SCSV_dP_kPa := rPDT_SCSV_301B_kPa;
ELSIF NOT bChannelFault_PDT301C THEN
    rVoted_SCSV_dP_kPa := rPDT_SCSV_301C_kPa;
ELSE
    rVoted_SCSV_dP_kPa := x_hat[5];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   1.4 Regenerated Catalyst Slide Valve Differential Pressure Transmitters (PDT_RCSV_401A / B / C) [kPa]
   --------------------------------------------------------------------------------------------------------------------- *)
bChannelFault_PDT401A := (rPDT_RCSV_401A_kPa < rPDT_RCSV_Min_kPa) OR (rPDT_RCSV_401A_kPa > rPDT_RCSV_Max_kPa);
bChannelFault_PDT401B := (rPDT_RCSV_401B_kPa < rPDT_RCSV_Min_kPa) OR (rPDT_RCSV_401B_kPa > rPDT_RCSV_Max_kPa);
bChannelFault_PDT401C := (rPDT_RCSV_401C_kPa < rPDT_RCSV_Min_kPa) OR (rPDT_RCSV_401C_kPa > rPDT_RCSV_Max_kPa);

bDiscrep_PDT401_AB := ABS(rPDT_RCSV_401A_kPa - rPDT_RCSV_401B_kPa) > rDiscrepancyTol_PDT401_kPa;
bDiscrep_PDT401_BC := ABS(rPDT_RCSV_401B_kPa - rPDT_RCSV_401C_kPa) > rDiscrepancyTol_PDT401_kPa;
bDiscrep_PDT401_AC := ABS(rPDT_RCSV_401A_kPa - rPDT_RCSV_401C_kPa) > rDiscrepancyTol_PDT401_kPa;

IF bDiscrep_PDT401_AB THEN
    rTimer_PDT401_AB_sec := rTimer_PDT401_AB_sec + rTs_sec;
ELSE
    rTimer_PDT401_AB_sec := 0.0;
END_IF;

IF bDiscrep_PDT401_BC THEN
    rTimer_PDT401_BC_sec := rTimer_PDT401_BC_sec + rTs_sec;
ELSE
    rTimer_PDT401_BC_sec := 0.0;
END_IF;

IF bDiscrep_PDT401_AC THEN
    rTimer_PDT401_AC_sec := rTimer_PDT401_AC_sec + rTs_sec;
ELSE
    rTimer_PDT401_AC_sec := 0.0;
END_IF;

IF (rTimer_PDT401_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT401_AC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT401A := TRUE;
END_IF;
IF (rTimer_PDT401_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT401_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT401B := TRUE;
END_IF;
IF (rTimer_PDT401_AC_sec >= rDiscrepancyTripTime_sec) AND (rTimer_PDT401_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_PDT401C := TRUE;
END_IF;

IF NOT bChannelFault_PDT401A AND NOT bChannelFault_PDT401B AND NOT bChannelFault_PDT401C THEN
    IF (rPDT_RCSV_401A_kPa >= rPDT_RCSV_401B_kPa AND rPDT_RCSV_401A_kPa <= rPDT_RCSV_401C_kPa) OR 
       (rPDT_RCSV_401A_kPa <= rPDT_RCSV_401B_kPa AND rPDT_RCSV_401A_kPa >= rPDT_RCSV_401C_kPa) THEN
        rVoted_RCSV_dP_kPa := rPDT_RCSV_401A_kPa;
    ELSIF (rPDT_RCSV_401B_kPa >= rPDT_RCSV_401A_kPa AND rPDT_RCSV_401B_kPa <= rPDT_RCSV_401C_kPa) OR 
          (rPDT_RCSV_401B_kPa <= rPDT_RCSV_401A_kPa AND rPDT_RCSV_401B_kPa >= rPDT_RCSV_401C_kPa) THEN
        rVoted_RCSV_dP_kPa := rPDT_RCSV_401B_kPa;
    ELSE
        rVoted_RCSV_dP_kPa := rPDT_RCSV_401C_kPa;
    END_IF;
ELSIF NOT bChannelFault_PDT401A AND NOT bChannelFault_PDT401B THEN
    rVoted_RCSV_dP_kPa := 0.5 * (rPDT_RCSV_401A_kPa + rPDT_RCSV_401B_kPa);
ELSIF NOT bChannelFault_PDT401A AND NOT bChannelFault_PDT401C THEN
    rVoted_RCSV_dP_kPa := 0.5 * (rPDT_RCSV_401A_kPa + rPDT_RCSV_401C_kPa);
ELSIF NOT bChannelFault_PDT401B AND NOT bChannelFault_PDT401C THEN
    rVoted_RCSV_dP_kPa := 0.5 * (rPDT_RCSV_401B_kPa + rPDT_RCSV_401C_kPa);
ELSIF NOT bChannelFault_PDT401A THEN
    rVoted_RCSV_dP_kPa := rPDT_RCSV_401A_kPa;
ELSIF NOT bChannelFault_PDT401B THEN
    rVoted_RCSV_dP_kPa := rPDT_RCSV_401B_kPa;
ELSIF NOT bChannelFault_PDT401C THEN
    rVoted_RCSV_dP_kPa := rPDT_RCSV_401C_kPa;
ELSE
    rVoted_RCSV_dP_kPa := x_hat[6];
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
   1.5 Flue Gas Zirconia Oxygen Analyzers (AT_O2_501A / B / C) [% O2]
   --------------------------------------------------------------------------------------------------------------------- *)
bChannelFault_AT501A := (rAT_O2_501A_pct < rAT_O2_Min_pct) OR (rAT_O2_501A_pct > rAT_O2_Max_pct);
bChannelFault_AT501B := (rAT_O2_501B_pct < rAT_O2_Min_pct) OR (rAT_O2_501B_pct > rAT_O2_Max_pct);
bChannelFault_AT501C := (rAT_O2_501C_pct < rAT_O2_Min_pct) OR (rAT_O2_501C_pct > rAT_O2_Max_pct);

bDiscrep_AT501_AB := ABS(rAT_O2_501A_pct - rAT_O2_501B_pct) > rDiscrepancyTol_AT501_pct;
bDiscrep_AT501_BC := ABS(rAT_O2_501B_pct - rAT_O2_501C_pct) > rDiscrepancyTol_AT501_pct;
bDiscrep_AT501_AC := ABS(rAT_O2_501A_pct - rAT_O2_501C_pct) > rDiscrepancyTol_AT501_pct;

IF bDiscrep_AT501_AB THEN
    rTimer_AT501_AB_sec := rTimer_AT501_AB_sec + rTs_sec;
ELSE
    rTimer_AT501_AB_sec := 0.0;
END_IF;

IF bDiscrep_AT501_BC THEN
    rTimer_AT501_BC_sec := rTimer_AT501_BC_sec + rTs_sec;
ELSE
    rTimer_AT501_BC_sec := 0.0;
END_IF;

IF bDiscrep_AT501_AC THEN
    rTimer_AT501_AC_sec := rTimer_AT501_AC_sec + rTs_sec;
ELSE
    rTimer_AT501_AC_sec := 0.0;
END_IF;

IF (rTimer_AT501_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_AT501_AC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_AT501A := TRUE;
END_IF;
IF (rTimer_AT501_AB_sec >= rDiscrepancyTripTime_sec) AND (rTimer_AT501_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_AT501B := TRUE;
END_IF;
IF (rTimer_AT501_AC_sec >= rDiscrepancyTripTime_sec) AND (rTimer_AT501_BC_sec >= rDiscrepancyTripTime_sec) THEN
    bChannelFault_AT501C := TRUE;
END_IF;

IF NOT bChannelFault_AT501A AND NOT bChannelFault_AT501B AND NOT bChannelFault_AT501C THEN
    IF (rAT_O2_501A_pct >= rAT_O2_501B_pct AND rAT_O2_501A_pct <= rAT_O2_501C_pct) OR 
       (rAT_O2_501A_pct <= rAT_O2_501B_pct AND rAT_O2_501A_pct >= rAT_O2_501C_pct) THEN
        rVoted_FlueGasO2_pct := rAT_O2_501A_pct;
    ELSIF (rAT_O2_501B_pct >= rAT_O2_501A_pct AND rAT_O2_501B_pct <= rAT_O2_501C_pct) OR 
          (rAT_O2_501B_pct <= rAT_O2_501A_pct AND rAT_O2_501B_pct >= rAT_O2_501C_pct) THEN
        rVoted_FlueGasO2_pct := rAT_O2_501B_pct;
    ELSE
        rVoted_FlueGasO2_pct := rAT_O2_501C_pct;
    END_IF;
ELSIF NOT bChannelFault_AT501A AND NOT bChannelFault_AT501B THEN
    rVoted_FlueGasO2_pct := 0.5 * (rAT_O2_501A_pct + rAT_O2_501B_pct);
ELSIF NOT bChannelFault_AT501A AND NOT bChannelFault_AT501C THEN
    rVoted_FlueGasO2_pct := 0.5 * (rAT_O2_501A_pct + rAT_O2_501C_pct);
ELSIF NOT bChannelFault_AT501B AND NOT bChannelFault_AT501C THEN
    rVoted_FlueGasO2_pct := 0.5 * (rAT_O2_501B_pct + rAT_O2_501C_pct);
ELSIF NOT bChannelFault_AT501A THEN
    rVoted_FlueGasO2_pct := rAT_O2_501A_pct;
ELSIF NOT bChannelFault_AT501B THEN
    rVoted_FlueGasO2_pct := rAT_O2_501B_pct;
ELSIF NOT bChannelFault_AT501C THEN
    rVoted_FlueGasO2_pct := rAT_O2_501C_pct;
ELSE
    rVoted_FlueGasO2_pct := x_hat[7];
END_IF;

(* Evaluate Slide Valve Differential Pressure Minimum Operating Margin *)
IF rVoted_SCSV_dP_kPa < rVoted_RCSV_dP_kPa THEN
    rSlideValveMinMargin_kPa := rVoted_SCSV_dP_kPa - 35.0;
ELSE
    rSlideValveMinMargin_kPa := rVoted_RCSV_dP_kPa - 35.0;
END_IF;
""")
    return "\n".join(lines)
