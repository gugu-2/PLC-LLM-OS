# Phase 1 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase1_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE WITH DISCREPANCY TIMERS
Channels:
  1. Feed Line Sanitary Diaphragm Pressure Transmitters (PT_Feed_101A/B/C) [bar], Tol = 0.15 [bar]
  2. Retentate Line Sanitary Diaphragm Pressure Transmitters (PT_Ret_201A/B/C) [bar], Tol = 0.15 [bar]
  3. Permeate Line Sanitary Diaphragm Pressure Transmitters (PT_Perm_301A/B/C) [bar], Tol = 0.10 [bar]
  4. Inline Flow-Cell UV-Vis 280 nm Photometers (AT_UV_401A/B/C) [g/L], Tol = 2.50 [g/L]
  5. Feed Line Sanitary Coriolis Mass Flowmeters (FT_Feed_501A/B/C) [L/h], Tol = 18.0 [L/h]
Persistence Discrepancy Threshold = 0.100 [s] (100 ms = 10 consecutive cycles at Ts = 10.0 ms)
Bumpless Degradation: 3-Healthy (Median) -> 2-Healthy (Dual-Average) -> 1-Healthy -> 0-Healthy (Fail-Safe)
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
 * Channel Group 1: Feed Line Sanitary Diaphragm Pressure Transmitters (PT_Feed_101A/B/C) [bar]
 * ------------------------------------------------------------------------------------------------- *)
rPT_Feed_Diff_AB := ABS(rPT_Feed_101A_bar - rPT_Feed_101B_bar);
rPT_Feed_Diff_BC := ABS(rPT_Feed_101B_bar - rPT_Feed_101C_bar);
rPT_Feed_Diff_AC := ABS(rPT_Feed_101A_bar - rPT_Feed_101C_bar);

IF rPT_Feed_Diff_AB > 0.15 THEN
    rPT_Feed_Timer_AB := rPT_Feed_Timer_AB + rCycleTime_s;
ELSE
    rPT_Feed_Timer_AB := MAX(0.0, rPT_Feed_Timer_AB - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Feed_Diff_BC > 0.15 THEN
    rPT_Feed_Timer_BC := rPT_Feed_Timer_BC + rCycleTime_s;
ELSE
    rPT_Feed_Timer_BC := MAX(0.0, rPT_Feed_Timer_BC - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Feed_Diff_AC > 0.15 THEN
    rPT_Feed_Timer_AC := rPT_Feed_Timer_AC + rCycleTime_s;
ELSE
    rPT_Feed_Timer_AC := MAX(0.0, rPT_Feed_Timer_AC - (rCycleTime_s * 0.5));
END_IF;

(* Identify Defective Channel via Pairwise Correlation Persistence *)
IF (rPT_Feed_Timer_AB >= 0.100) AND (rPT_Feed_Timer_AC >= 0.100) THEN
    bPT_Feed_Degraded_A := TRUE;
END_IF;
IF (rPT_Feed_Timer_AB >= 0.100) AND (rPT_Feed_Timer_BC >= 0.100) THEN
    bPT_Feed_Degraded_B := TRUE;
END_IF;
IF (rPT_Feed_Timer_AC >= 0.100) AND (rPT_Feed_Timer_BC >= 0.100) THEN
    bPT_Feed_Degraded_C := TRUE;
END_IF;

IF bResetFault THEN
    bPT_Feed_Degraded_A := FALSE;
    bPT_Feed_Degraded_B := FALSE;
    bPT_Feed_Degraded_C := FALSE;
    rPT_Feed_Timer_AB := 0.0;
    rPT_Feed_Timer_BC := 0.0;
    rPT_Feed_Timer_AC := 0.0;
END_IF;

(* 2oo3 Bumpless Voting Logic *)
IF (NOT bPT_Feed_Degraded_A) AND (NOT bPT_Feed_Degraded_B) AND (NOT bPT_Feed_Degraded_C) THEN
    nPT_Feed_HealthStatus := 0; (* Triple Modular Healthy *)
    IF (rPT_Feed_101A_bar >= rPT_Feed_101B_bar AND rPT_Feed_101A_bar <= rPT_Feed_101C_bar) OR 
       (rPT_Feed_101A_bar <= rPT_Feed_101B_bar AND rPT_Feed_101A_bar >= rPT_Feed_101C_bar) THEN
        rVoted_PT_Feed_bar := rPT_Feed_101A_bar;
    ELSIF (rPT_Feed_101B_bar >= rPT_Feed_101A_bar AND rPT_Feed_101B_bar <= rPT_Feed_101C_bar) OR 
          (rPT_Feed_101B_bar <= rPT_Feed_101A_bar AND rPT_Feed_101B_bar >= rPT_Feed_101C_bar) THEN
        rVoted_PT_Feed_bar := rPT_Feed_101B_bar;
    ELSE
        rVoted_PT_Feed_bar := rPT_Feed_101C_bar;
    END_IF;
ELSIF bPT_Feed_Degraded_A AND (NOT bPT_Feed_Degraded_B) AND (NOT bPT_Feed_Degraded_C) THEN
    nPT_Feed_HealthStatus := 1; (* Channel A Degraded -> Dual Average of B & C *)
    rVoted_PT_Feed_bar := (rPT_Feed_101B_bar + rPT_Feed_101C_bar) * 0.5;
ELSIF (NOT bPT_Feed_Degraded_A) AND bPT_Feed_Degraded_B AND (NOT bPT_Feed_Degraded_C) THEN
    nPT_Feed_HealthStatus := 2; (* Channel B Degraded -> Dual Average of A & C *)
    rVoted_PT_Feed_bar := (rPT_Feed_101A_bar + rPT_Feed_101C_bar) * 0.5;
ELSIF (NOT bPT_Feed_Degraded_A) AND (NOT bPT_Feed_Degraded_B) AND bPT_Feed_Degraded_C THEN
    nPT_Feed_HealthStatus := 3; (* Channel C Degraded -> Dual Average of A & B *)
    rVoted_PT_Feed_bar := (rPT_Feed_101A_bar + rPT_Feed_101B_bar) * 0.5;
ELSIF bPT_Feed_Degraded_A AND bPT_Feed_Degraded_B AND (NOT bPT_Feed_Degraded_C) THEN
    nPT_Feed_HealthStatus := 4; (* Channels A & B Degraded -> Single Healthy Channel C *)
    rVoted_PT_Feed_bar := rPT_Feed_101C_bar;
ELSIF bPT_Feed_Degraded_A AND (NOT bPT_Feed_Degraded_B) AND bPT_Feed_Degraded_C THEN
    nPT_Feed_HealthStatus := 4; (* Channels A & C Degraded -> Single Healthy Channel B *)
    rVoted_PT_Feed_bar := rPT_Feed_101B_bar;
ELSIF (NOT bPT_Feed_Degraded_A) AND bPT_Feed_Degraded_B AND bPT_Feed_Degraded_C THEN
    nPT_Feed_HealthStatus := 4; (* Channels B & C Degraded -> Single Healthy Channel A *)
    rVoted_PT_Feed_bar := rPT_Feed_101A_bar;
ELSE
    nPT_Feed_HealthStatus := 5; (* All Channels Degraded -> Fail-Safe Hold & System Trip *)
    bSystemTrip_Interlock := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
 * Channel Group 2: Retentate Line Sanitary Diaphragm Pressure Transmitters (PT_Ret_201A/B/C) [bar]
 * ------------------------------------------------------------------------------------------------- *)
rPT_Ret_Diff_AB := ABS(rPT_Ret_201A_bar - rPT_Ret_201B_bar);
rPT_Ret_Diff_BC := ABS(rPT_Ret_201B_bar - rPT_Ret_201C_bar);
rPT_Ret_Diff_AC := ABS(rPT_Ret_201A_bar - rPT_Ret_201C_bar);

IF rPT_Ret_Diff_AB > 0.15 THEN
    rPT_Ret_Timer_AB := rPT_Ret_Timer_AB + rCycleTime_s;
ELSE
    rPT_Ret_Timer_AB := MAX(0.0, rPT_Ret_Timer_AB - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Ret_Diff_BC > 0.15 THEN
    rPT_Ret_Timer_BC := rPT_Ret_Timer_BC + rCycleTime_s;
ELSE
    rPT_Ret_Timer_BC := MAX(0.0, rPT_Ret_Timer_BC - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Ret_Diff_AC > 0.15 THEN
    rPT_Ret_Timer_AC := rPT_Ret_Timer_AC + rCycleTime_s;
ELSE
    rPT_Ret_Timer_AC := MAX(0.0, rPT_Ret_Timer_AC - (rCycleTime_s * 0.5));
END_IF;

IF (rPT_Ret_Timer_AB >= 0.100) AND (rPT_Ret_Timer_AC >= 0.100) THEN
    bPT_Ret_Degraded_A := TRUE;
END_IF;
IF (rPT_Ret_Timer_AB >= 0.100) AND (rPT_Ret_Timer_BC >= 0.100) THEN
    bPT_Ret_Degraded_B := TRUE;
END_IF;
IF (rPT_Ret_Timer_AC >= 0.100) AND (rPT_Ret_Timer_BC >= 0.100) THEN
    bPT_Ret_Degraded_C := TRUE;
END_IF;

IF bResetFault THEN
    bPT_Ret_Degraded_A := FALSE;
    bPT_Ret_Degraded_B := FALSE;
    bPT_Ret_Degraded_C := FALSE;
    rPT_Ret_Timer_AB := 0.0;
    rPT_Ret_Timer_BC := 0.0;
    rPT_Ret_Timer_AC := 0.0;
END_IF;

IF (NOT bPT_Ret_Degraded_A) AND (NOT bPT_Ret_Degraded_B) AND (NOT bPT_Ret_Degraded_C) THEN
    nPT_Ret_HealthStatus := 0;
    IF (rPT_Ret_201A_bar >= rPT_Ret_201B_bar AND rPT_Ret_201A_bar <= rPT_Ret_201C_bar) OR 
       (rPT_Ret_201A_bar <= rPT_Ret_201B_bar AND rPT_Ret_201A_bar >= rPT_Ret_201C_bar) THEN
        rVoted_PT_Ret_bar := rPT_Ret_201A_bar;
    ELSIF (rPT_Ret_201B_bar >= rPT_Ret_201A_bar AND rPT_Ret_201B_bar <= rPT_Ret_201C_bar) OR 
          (rPT_Ret_201B_bar <= rPT_Ret_201A_bar AND rPT_Ret_201B_bar >= rPT_Ret_201C_bar) THEN
        rVoted_PT_Ret_bar := rPT_Ret_201B_bar;
    ELSE
        rVoted_PT_Ret_bar := rPT_Ret_201C_bar;
    END_IF;
ELSIF bPT_Ret_Degraded_A AND (NOT bPT_Ret_Degraded_B) AND (NOT bPT_Ret_Degraded_C) THEN
    nPT_Ret_HealthStatus := 1;
    rVoted_PT_Ret_bar := (rPT_Ret_201B_bar + rPT_Ret_201C_bar) * 0.5;
ELSIF (NOT bPT_Ret_Degraded_A) AND bPT_Ret_Degraded_B AND (NOT bPT_Ret_Degraded_C) THEN
    nPT_Ret_HealthStatus := 2;
    rVoted_PT_Ret_bar := (rPT_Ret_201A_bar + rPT_Ret_201C_bar) * 0.5;
ELSIF (NOT bPT_Ret_Degraded_A) AND (NOT bPT_Ret_Degraded_B) AND bPT_Ret_Degraded_C THEN
    nPT_Ret_HealthStatus := 3;
    rVoted_PT_Ret_bar := (rPT_Ret_201A_bar + rPT_Ret_201B_bar) * 0.5;
ELSIF bPT_Ret_Degraded_A AND bPT_Ret_Degraded_B AND (NOT bPT_Ret_Degraded_C) THEN
    nPT_Ret_HealthStatus := 4;
    rVoted_PT_Ret_bar := rPT_Ret_201C_bar;
ELSIF bPT_Ret_Degraded_A AND (NOT bPT_Ret_Degraded_B) AND bPT_Ret_Degraded_C THEN
    nPT_Ret_HealthStatus := 4;
    rVoted_PT_Ret_bar := rPT_Ret_201B_bar;
ELSIF (NOT bPT_Ret_Degraded_A) AND bPT_Ret_Degraded_B AND bPT_Ret_Degraded_C THEN
    nPT_Ret_HealthStatus := 4;
    rVoted_PT_Ret_bar := rPT_Ret_201A_bar;
ELSE
    nPT_Ret_HealthStatus := 5;
    bSystemTrip_Interlock := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
 * Channel Group 3: Permeate Line Sanitary Diaphragm Pressure Transmitters (PT_Perm_301A/B/C) [bar]
 * ------------------------------------------------------------------------------------------------- *)
rPT_Perm_Diff_AB := ABS(rPT_Perm_301A_bar - rPT_Perm_301B_bar);
rPT_Perm_Diff_BC := ABS(rPT_Perm_301B_bar - rPT_Perm_301C_bar);
rPT_Perm_Diff_AC := ABS(rPT_Perm_301A_bar - rPT_Perm_301C_bar);

IF rPT_Perm_Diff_AB > 0.10 THEN
    rPT_Perm_Timer_AB := rPT_Perm_Timer_AB + rCycleTime_s;
ELSE
    rPT_Perm_Timer_AB := MAX(0.0, rPT_Perm_Timer_AB - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Perm_Diff_BC > 0.10 THEN
    rPT_Perm_Timer_BC := rPT_Perm_Timer_BC + rCycleTime_s;
ELSE
    rPT_Perm_Timer_BC := MAX(0.0, rPT_Perm_Timer_BC - (rCycleTime_s * 0.5));
END_IF;

IF rPT_Perm_Diff_AC > 0.10 THEN
    rPT_Perm_Timer_AC := rPT_Perm_Timer_AC + rCycleTime_s;
ELSE
    rPT_Perm_Timer_AC := MAX(0.0, rPT_Perm_Timer_AC - (rCycleTime_s * 0.5));
END_IF;

IF (rPT_Perm_Timer_AB >= 0.100) AND (rPT_Perm_Timer_AC >= 0.100) THEN
    bPT_Perm_Degraded_A := TRUE;
END_IF;
IF (rPT_Perm_Timer_AB >= 0.100) AND (rPT_Perm_Timer_BC >= 0.100) THEN
    bPT_Perm_Degraded_B := TRUE;
END_IF;
IF (rPT_Perm_Timer_AC >= 0.100) AND (rPT_Perm_Timer_BC >= 0.100) THEN
    bPT_Perm_Degraded_C := TRUE;
END_IF;

IF bResetFault THEN
    bPT_Perm_Degraded_A := FALSE;
    bPT_Perm_Degraded_B := FALSE;
    bPT_Perm_Degraded_C := FALSE;
    rPT_Perm_Timer_AB := 0.0;
    rPT_Perm_Timer_BC := 0.0;
    rPT_Perm_Timer_AC := 0.0;
END_IF;

IF (NOT bPT_Perm_Degraded_A) AND (NOT bPT_Perm_Degraded_B) AND (NOT bPT_Perm_Degraded_C) THEN
    nPT_Perm_HealthStatus := 0;
    IF (rPT_Perm_301A_bar >= rPT_Perm_301B_bar AND rPT_Perm_301A_bar <= rPT_Perm_301C_bar) OR 
       (rPT_Perm_301A_bar <= rPT_Perm_301B_bar AND rPT_Perm_301A_bar >= rPT_Perm_301C_bar) THEN
        rVoted_PT_Perm_bar := rPT_Perm_301A_bar;
    ELSIF (rPT_Perm_301B_bar >= rPT_Perm_301A_bar AND rPT_Perm_301B_bar <= rPT_Perm_301C_bar) OR 
          (rPT_Perm_301B_bar <= rPT_Perm_301A_bar AND rPT_Perm_301B_bar >= rPT_Perm_301C_bar) THEN
        rVoted_PT_Perm_bar := rPT_Perm_301B_bar;
    ELSE
        rVoted_PT_Perm_bar := rPT_Perm_301C_bar;
    END_IF;
ELSIF bPT_Perm_Degraded_A AND (NOT bPT_Perm_Degraded_B) AND (NOT bPT_Perm_Degraded_C) THEN
    nPT_Perm_HealthStatus := 1;
    rVoted_PT_Perm_bar := (rPT_Perm_301B_bar + rPT_Perm_301C_bar) * 0.5;
ELSIF (NOT bPT_Perm_Degraded_A) AND bPT_Perm_Degraded_B AND (NOT bPT_Perm_Degraded_C) THEN
    nPT_Perm_HealthStatus := 2;
    rVoted_PT_Perm_bar := (rPT_Perm_301A_bar + rPT_Perm_301C_bar) * 0.5;
ELSIF (NOT bPT_Perm_Degraded_A) AND (NOT bPT_Perm_Degraded_B) AND bPT_Perm_Degraded_C THEN
    nPT_Perm_HealthStatus := 3;
    rVoted_PT_Perm_bar := (rPT_Perm_301A_bar + rPT_Perm_301B_bar) * 0.5;
ELSIF bPT_Perm_Degraded_A AND bPT_Perm_Degraded_B AND (NOT bPT_Perm_Degraded_C) THEN
    nPT_Perm_HealthStatus := 4;
    rVoted_PT_Perm_bar := rPT_Perm_301C_bar;
ELSIF bPT_Perm_Degraded_A AND (NOT bPT_Perm_Degraded_B) AND bPT_Perm_Degraded_C THEN
    nPT_Perm_HealthStatus := 4;
    rVoted_PT_Perm_bar := rPT_Perm_301B_bar;
ELSIF (NOT bPT_Perm_Degraded_A) AND bPT_Perm_Degraded_B AND bPT_Perm_Degraded_C THEN
    nPT_Perm_HealthStatus := 4;
    rVoted_PT_Perm_bar := rPT_Perm_301A_bar;
ELSE
    nPT_Perm_HealthStatus := 5;
    bSystemTrip_Interlock := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
 * Channel Group 4: Inline Flow-Cell UV-Vis 280 nm Photometers (AT_UV_401A/B/C) [g/L]
 * ------------------------------------------------------------------------------------------------- *)
rAT_UV_Diff_AB := ABS(rAT_UV_401A_gL - rAT_UV_401B_gL);
rAT_UV_Diff_BC := ABS(rAT_UV_401B_gL - rAT_UV_401C_gL);
rAT_UV_Diff_AC := ABS(rAT_UV_401A_gL - rAT_UV_401C_gL);

IF rAT_UV_Diff_AB > 2.50 THEN
    rAT_UV_Timer_AB := rAT_UV_Timer_AB + rCycleTime_s;
ELSE
    rAT_UV_Timer_AB := MAX(0.0, rAT_UV_Timer_AB - (rCycleTime_s * 0.5));
END_IF;

IF rAT_UV_Diff_BC > 2.50 THEN
    rAT_UV_Timer_BC := rAT_UV_Timer_BC + rCycleTime_s;
ELSE
    rAT_UV_Timer_BC := MAX(0.0, rAT_UV_Timer_BC - (rCycleTime_s * 0.5));
END_IF;

IF rAT_UV_Diff_AC > 2.50 THEN
    rAT_UV_Timer_AC := rAT_UV_Timer_AC + rCycleTime_s;
ELSE
    rAT_UV_Timer_AC := MAX(0.0, rAT_UV_Timer_AC - (rCycleTime_s * 0.5));
END_IF;

IF (rAT_UV_Timer_AB >= 0.100) AND (rAT_UV_Timer_AC >= 0.100) THEN
    bAT_UV_Degraded_A := TRUE;
END_IF;
IF (rAT_UV_Timer_AB >= 0.100) AND (rAT_UV_Timer_BC >= 0.100) THEN
    bAT_UV_Degraded_B := TRUE;
END_IF;
IF (rAT_UV_Timer_AC >= 0.100) AND (rAT_UV_Timer_BC >= 0.100) THEN
    bAT_UV_Degraded_C := TRUE;
END_IF;

IF bResetFault THEN
    bAT_UV_Degraded_A := FALSE;
    bAT_UV_Degraded_B := FALSE;
    bAT_UV_Degraded_C := FALSE;
    rAT_UV_Timer_AB := 0.0;
    rAT_UV_Timer_BC := 0.0;
    rAT_UV_Timer_AC := 0.0;
END_IF;

IF (NOT bAT_UV_Degraded_A) AND (NOT bAT_UV_Degraded_B) AND (NOT bAT_UV_Degraded_C) THEN
    nAT_UV_HealthStatus := 0;
    IF (rAT_UV_401A_gL >= rAT_UV_401B_gL AND rAT_UV_401A_gL <= rAT_UV_401C_gL) OR 
       (rAT_UV_401A_gL <= rAT_UV_401B_gL AND rAT_UV_401A_gL >= rAT_UV_401C_gL) THEN
        rVoted_AT_UV_gL := rAT_UV_401A_gL;
    ELSIF (rAT_UV_401B_gL >= rAT_UV_401A_gL AND rAT_UV_401B_gL <= rAT_UV_401C_gL) OR 
          (rAT_UV_401B_gL <= rAT_UV_401A_gL AND rAT_UV_401B_gL >= rAT_UV_401C_gL) THEN
        rVoted_AT_UV_gL := rAT_UV_401B_gL;
    ELSE
        rVoted_AT_UV_gL := rAT_UV_401C_gL;
    END_IF;
ELSIF bAT_UV_Degraded_A AND (NOT bAT_UV_Degraded_B) AND (NOT bAT_UV_Degraded_C) THEN
    nAT_UV_HealthStatus := 1;
    rVoted_AT_UV_gL := (rAT_UV_401B_gL + rAT_UV_401C_gL) * 0.5;
ELSIF (NOT bAT_UV_Degraded_A) AND bAT_UV_Degraded_B AND (NOT bAT_UV_Degraded_C) THEN
    nAT_UV_HealthStatus := 2;
    rVoted_AT_UV_gL := (rAT_UV_401A_gL + rAT_UV_401C_gL) * 0.5;
ELSIF (NOT bAT_UV_Degraded_A) AND (NOT bAT_UV_Degraded_B) AND bAT_UV_Degraded_C THEN
    nAT_UV_HealthStatus := 3;
    rVoted_AT_UV_gL := (rAT_UV_401A_gL + rAT_UV_401B_gL) * 0.5;
ELSIF bAT_UV_Degraded_A AND bAT_UV_Degraded_B AND (NOT bAT_UV_Degraded_C) THEN
    nAT_UV_HealthStatus := 4;
    rVoted_AT_UV_gL := rAT_UV_401C_gL;
ELSIF bAT_UV_Degraded_A AND (NOT bAT_UV_Degraded_B) AND bAT_UV_Degraded_C THEN
    nAT_UV_HealthStatus := 4;
    rVoted_AT_UV_gL := rAT_UV_401B_gL;
ELSIF (NOT bAT_UV_Degraded_A) AND bAT_UV_Degraded_B AND bAT_UV_Degraded_C THEN
    nAT_UV_HealthStatus := 4;
    rVoted_AT_UV_gL := rAT_UV_401A_gL;
ELSE
    nAT_UV_HealthStatus := 5;
    bSystemTrip_Interlock := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
 * Channel Group 5: Feed Line Sanitary Coriolis Mass Flowmeters (FT_Feed_501A/B/C) [L/h]
 * ------------------------------------------------------------------------------------------------- *)
rFT_Feed_Diff_AB := ABS(rFT_Feed_501A_Lh - rFT_Feed_501B_Lh);
rFT_Feed_Diff_BC := ABS(rFT_Feed_501B_Lh - rFT_Feed_501C_Lh);
rFT_Feed_Diff_AC := ABS(rFT_Feed_501A_Lh - rFT_Feed_501C_Lh);

IF rFT_Feed_Diff_AB > 18.0 THEN
    rFT_Feed_Timer_AB := rFT_Feed_Timer_AB + rCycleTime_s;
ELSE
    rFT_Feed_Timer_AB := MAX(0.0, rFT_Feed_Timer_AB - (rCycleTime_s * 0.5));
END_IF;

IF rFT_Feed_Diff_BC > 18.0 THEN
    rFT_Feed_Timer_BC := rFT_Feed_Timer_BC + rCycleTime_s;
ELSE
    rFT_Feed_Timer_BC := MAX(0.0, rFT_Feed_Timer_BC - (rCycleTime_s * 0.5));
END_IF;

IF rFT_Feed_Diff_AC > 18.0 THEN
    rFT_Feed_Timer_AC := rFT_Feed_Timer_AC + rCycleTime_s;
ELSE
    rFT_Feed_Timer_AC := MAX(0.0, rFT_Feed_Timer_AC - (rCycleTime_s * 0.5));
END_IF;

IF (rFT_Feed_Timer_AB >= 0.100) AND (rFT_Feed_Timer_AC >= 0.100) THEN
    bFT_Feed_Degraded_A := TRUE;
END_IF;
IF (rFT_Feed_Timer_AB >= 0.100) AND (rFT_Feed_Timer_BC >= 0.100) THEN
    bFT_Feed_Degraded_B := TRUE;
END_IF;
IF (rFT_Feed_Timer_AC >= 0.100) AND (rFT_Feed_Timer_BC >= 0.100) THEN
    bFT_Feed_Degraded_C := TRUE;
END_IF;

IF bResetFault THEN
    bFT_Feed_Degraded_A := FALSE;
    bFT_Feed_Degraded_B := FALSE;
    bFT_Feed_Degraded_C := FALSE;
    rFT_Feed_Timer_AB := 0.0;
    rFT_Feed_Timer_BC := 0.0;
    rFT_Feed_Timer_AC := 0.0;
END_IF;

IF (NOT bFT_Feed_Degraded_A) AND (NOT bFT_Feed_Degraded_B) AND (NOT bFT_Feed_Degraded_C) THEN
    nFT_Feed_HealthStatus := 0;
    IF (rFT_Feed_501A_Lh >= rFT_Feed_501B_Lh AND rFT_Feed_501A_Lh <= rFT_Feed_501C_Lh) OR 
       (rFT_Feed_501A_Lh <= rFT_Feed_501B_Lh AND rFT_Feed_501A_Lh >= rFT_Feed_501C_Lh) THEN
        rVoted_FT_Feed_Lh := rFT_Feed_501A_Lh;
    ELSIF (rFT_Feed_501B_Lh >= rFT_Feed_501A_Lh AND rFT_Feed_501B_Lh <= rFT_Feed_501C_Lh) OR 
          (rFT_Feed_501B_Lh <= rFT_Feed_501A_Lh AND rFT_Feed_501B_Lh >= rFT_Feed_501C_Lh) THEN
        rVoted_FT_Feed_Lh := rFT_Feed_501B_Lh;
    ELSE
        rVoted_FT_Feed_Lh := rFT_Feed_501C_Lh;
    END_IF;
ELSIF bFT_Feed_Degraded_A AND (NOT bFT_Feed_Degraded_B) AND (NOT bFT_Feed_Degraded_C) THEN
    nFT_Feed_HealthStatus := 1;
    rVoted_FT_Feed_Lh := (rFT_Feed_501B_Lh + rFT_Feed_501C_Lh) * 0.5;
ELSIF (NOT bFT_Feed_Degraded_A) AND bFT_Feed_Degraded_B AND (NOT bFT_Feed_Degraded_C) THEN
    nFT_Feed_HealthStatus := 2;
    rVoted_FT_Feed_Lh := (rFT_Feed_501A_Lh + rFT_Feed_501C_Lh) * 0.5;
ELSIF (NOT bFT_Feed_Degraded_A) AND (NOT bFT_Feed_Degraded_B) AND bFT_Feed_Degraded_C THEN
    nFT_Feed_HealthStatus := 3;
    rVoted_FT_Feed_Lh := (rFT_Feed_501A_Lh + rFT_Feed_501B_Lh) * 0.5;
ELSIF bFT_Feed_Degraded_A AND bFT_Feed_Degraded_B AND (NOT bFT_Feed_Degraded_C) THEN
    nFT_Feed_HealthStatus := 4;
    rVoted_FT_Feed_Lh := rFT_Feed_501C_Lh;
ELSIF bFT_Feed_Degraded_A AND (NOT bFT_Feed_Degraded_B) AND bFT_Feed_Degraded_C THEN
    nFT_Feed_HealthStatus := 4;
    rVoted_FT_Feed_Lh := rFT_Feed_501B_Lh;
ELSIF (NOT bFT_Feed_Degraded_A) AND bFT_Feed_Degraded_B AND bFT_Feed_Degraded_C THEN
    nFT_Feed_HealthStatus := 4;
    rVoted_FT_Feed_Lh := rFT_Feed_501A_Lh;
ELSE
    nFT_Feed_HealthStatus := 5;
    bSystemTrip_Interlock := TRUE;
END_IF;""")

    return "\n".join(lines)

print("Phase 1 builder ready")
