# Phase 5 Builder for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys

def get_phase5_code():
    lines = []
    lines.append("""(*
====================================================================================================
PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX, PARTICLE TRIPS & 32-BIT STATUS WORDS
Standards Compliance:
  - ANSI/ISA-18.2-2016 Management of Alarm Systems for the Process Industries
  - 4-Tier Hierarchical Classification: High-High (HH), High (H), Low (L), Low-Low (LL)
  - Configurable Deadband Clearance Hysteresis Preventing Alarm Chattering
  - Sub-10ms Fast Hydrodynamic Overpressure Cutoff Trip Interlock
  - First-Out Diagnostic Root-Cause Fault Registration Latch
  - 32-Bit Bit-Packed Telemetry Diagnostic Words (dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2)
====================================================================================================
*)

(* -------------------------------------------------------------------------------------------------
 * 1. ISA-18.2 Multi-Tier Process Alarm Evaluator
 * ------------------------------------------------------------------------------------------------- *)
(* Alarm Group 1: Transmembrane Pressure TMP [bar] *)
IF arrX_State[1] >= rLimit_TMP_HH_bar THEN
    bAlarm_TMP_HH := TRUE;
    bSystemTrip_Interlock := TRUE;          (* Instantaneous Fast Cutoff Interlock *)
ELSIF arrX_State[1] <= (rLimit_TMP_HH_bar - rDeadband_TMP_bar) THEN
    IF bAckAlarm THEN
        bAlarm_TMP_HH := FALSE;
    END_IF;
END_IF;

IF arrX_State[1] >= rLimit_TMP_H_bar THEN
    bAlarm_TMP_H := TRUE;
ELSIF arrX_State[1] <= (rLimit_TMP_H_bar - rDeadband_TMP_bar) THEN
    IF bAckAlarm THEN
        bAlarm_TMP_H := FALSE;
    END_IF;
END_IF;

IF (arrX_State[1] <= rLimit_TMP_L_bar) AND (nState >= 4) AND (nState <= 6) THEN
    bAlarm_TMP_L := TRUE;
ELSIF arrX_State[1] >= (rLimit_TMP_L_bar + rDeadband_TMP_bar) THEN
    IF bAckAlarm THEN
        bAlarm_TMP_L := FALSE;
    END_IF;
END_IF;

IF (arrX_State[1] <= rLimit_TMP_LL_bar) AND (nState >= 4) AND (nState <= 6) THEN
    bAlarm_TMP_LL := TRUE;
ELSIF arrX_State[1] >= (rLimit_TMP_LL_bar + rDeadband_TMP_bar) THEN
    IF bAckAlarm THEN
        bAlarm_TMP_LL := FALSE;
    END_IF;
END_IF;

(* Alarm Group 2: Permeate Volumetric Flux J_flux [LMH] *)
IF arrX_State[2] >= rLimit_Flux_HH_LMH THEN
    bAlarm_Flux_HH := TRUE;
ELSIF arrX_State[2] <= (rLimit_Flux_HH_LMH - rDeadband_Flux_LMH) THEN
    IF bAckAlarm THEN
        bAlarm_Flux_HH := FALSE;
    END_IF;
END_IF;

IF arrX_State[2] >= rLimit_Flux_H_LMH THEN
    bAlarm_Flux_H := TRUE;
ELSIF arrX_State[2] <= (rLimit_Flux_H_LMH - rDeadband_Flux_LMH) THEN
    IF bAckAlarm THEN
        bAlarm_Flux_H := FALSE;
    END_IF;
END_IF;

IF (arrX_State[2] <= rLimit_Flux_L_LMH) AND (nState >= 4) AND (nState <= 6) THEN
    bAlarm_Flux_L := TRUE;
ELSIF arrX_State[2] >= (rLimit_Flux_L_LMH + rDeadband_Flux_LMH) THEN
    IF bAckAlarm THEN
        bAlarm_Flux_L := FALSE;
    END_IF;
END_IF;

IF (arrX_State[2] <= rLimit_Flux_LL_LMH) AND (nState >= 4) AND (nState <= 6) THEN
    bAlarm_Flux_LL := TRUE;
ELSIF arrX_State[2] >= (rLimit_Flux_LL_LMH + rDeadband_Flux_LMH) THEN
    IF bAckAlarm THEN
        bAlarm_Flux_LL := FALSE;
    END_IF;
END_IF;

(* Alarm Group 3: Retentate Recirculation Temperature T_ret [deg C] *)
IF arrX_State[7] >= rLimit_Temp_HH_degC THEN
    bAlarm_Temp_HH := TRUE;
    bSystemTrip_Interlock := TRUE;          (* Protein Denaturation Protection Trip *)
ELSIF arrX_State[7] <= (rLimit_Temp_HH_degC - rDeadband_Temp_degC) THEN
    IF bAckAlarm THEN
        bAlarm_Temp_HH := FALSE;
    END_IF;
END_IF;

IF arrX_State[7] >= rLimit_Temp_H_degC THEN
    bAlarm_Temp_H := TRUE;
ELSIF arrX_State[7] <= (rLimit_Temp_H_degC - rDeadband_Temp_degC) THEN
    IF bAckAlarm THEN
        bAlarm_Temp_H := FALSE;
    END_IF;
END_IF;

IF arrX_State[7] <= rLimit_Temp_L_degC THEN
    bAlarm_Temp_L := TRUE;
ELSIF arrX_State[7] >= (rLimit_Temp_L_degC + rDeadband_Temp_degC) THEN
    IF bAckAlarm THEN
        bAlarm_Temp_L := FALSE;
    END_IF;
END_IF;

IF arrX_State[7] <= rLimit_Temp_LL_degC THEN
    bAlarm_Temp_LL := TRUE;
    bSystemTrip_Interlock := TRUE;          (* Freezing Prevention Trip *)
ELSIF arrX_State[7] >= (rLimit_Temp_LL_degC + rDeadband_Temp_degC) THEN
    IF bAckAlarm THEN
        bAlarm_Temp_LL := FALSE;
    END_IF;
END_IF;

(* Alarm Group 4: Retentate Channel Wall Shear Rate gamma_w [s-1] *)
IF arrX_State[5] >= rLimit_Shear_HH_s1 THEN
    bAlarm_Shear_HH := TRUE;
    bSystemTrip_Interlock := TRUE;          (* Shear-Induced Aggregation Interlock Trip *)
ELSIF arrX_State[5] <= (rLimit_Shear_HH_s1 - rDeadband_Shear_s1) THEN
    IF bAckAlarm THEN
        bAlarm_Shear_HH := FALSE;
    END_IF;
END_IF;

IF arrX_State[5] >= rLimit_Shear_H_s1 THEN
    bAlarm_Shear_H := TRUE;
ELSIF arrX_State[5] <= (rLimit_Shear_H_s1 - rDeadband_Shear_s1) THEN
    IF bAckAlarm THEN
        bAlarm_Shear_H := FALSE;
    END_IF;
END_IF;

IF (arrX_State[5] <= rLimit_Shear_L_s1) AND (nState >= 3) AND (nState <= 6) THEN
    bAlarm_Shear_L := TRUE;
ELSIF arrX_State[5] >= (rLimit_Shear_L_s1 + rDeadband_Shear_s1) THEN
    IF bAckAlarm THEN
        bAlarm_Shear_L := FALSE;
    END_IF;
END_IF;

IF (arrX_State[5] <= rLimit_Shear_LL_s1) AND (nState >= 3) AND (nState <= 6) THEN
    bAlarm_Shear_LL := TRUE;
ELSIF arrX_State[5] >= (rLimit_Shear_LL_s1 + rDeadband_Shear_s1) THEN
    IF bAckAlarm THEN
        bAlarm_Shear_LL := FALSE;
    END_IF;
END_IF;

(* Alarm Group 5: Diafiltration Sump Mass Balance Scale Weight Deviation delta_M_sump [g] *)
IF arrX_State[8] >= rLimit_SumpDev_HH_g THEN
    bAlarm_SumpDev_HH := TRUE;
ELSIF arrX_State[8] <= (rLimit_SumpDev_HH_g - rDeadband_SumpDev_g) THEN
    IF bAckAlarm THEN
        bAlarm_SumpDev_HH := FALSE;
    END_IF;
END_IF;

IF arrX_State[8] >= rLimit_SumpDev_H_g THEN
    bAlarm_SumpDev_H := TRUE;
ELSIF arrX_State[8] <= (rLimit_SumpDev_H_g - rDeadband_SumpDev_g) THEN
    IF bAckAlarm THEN
        bAlarm_SumpDev_H := FALSE;
    END_IF;
END_IF;

IF arrX_State[8] <= rLimit_SumpDev_L_g THEN
    bAlarm_SumpDev_L := TRUE;
ELSIF arrX_State[8] >= (rLimit_SumpDev_L_g + rDeadband_SumpDev_g) THEN
    IF bAckAlarm THEN
        bAlarm_SumpDev_L := FALSE;
    END_IF;
END_IF;

IF arrX_State[8] <= rLimit_SumpDev_LL_g THEN
    bAlarm_SumpDev_LL := TRUE;
ELSIF arrX_State[8] >= (rLimit_SumpDev_LL_g + rDeadband_SumpDev_g) THEN
    IF bAckAlarm THEN
        bAlarm_SumpDev_LL := FALSE;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
 * 2. 32-Bit Bit-Packed System Status Words Telemetry Encoding
 * ------------------------------------------------------------------------------------------------- *)
(* Reset Status Word 1 *)
dwStatusWord1 := 16#00000000;

(* Bits 0..13: One-Hot State Machine Encoding *)
IF nState >= 0 AND nState <= 13 THEN
    dwStatusWord1 := dwStatusWord1 OR SHL(16#00000001, nState);
END_IF;

(* Functional Bit Flags *)
IF bAutoCycleStart THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;      (* Bit 14 *)
IF bSequencePaused THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;      (* Bit 15 *)
IF bCycleComplete THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;       (* Bit 16 *)
IF bFeedPump_Run_Enable THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17 *)
IF bBufferPump_Run_Enable THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18 *)
IF bPermeateIsolation_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19 *)
IF bWFI_SupplyValve_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF; (* Bit 20 *)
IF bCIP_SupplyValve_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF; (* Bit 21 *)
IF bAirBlowdown_Valve_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF; (* Bit 22 *)
IF bProductDrain_Valve_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF; (* Bit 23 *)
IF bSystemTrip_Interlock THEN dwStatusWord1 := dwStatusWord1 OR 16#01000000; END_IF; (* Bit 24 *)
IF bEmergencyStop THEN dwStatusWord1 := dwStatusWord1 OR 16#02000000; END_IF;       (* Bit 25 *)
IF bManualMode THEN dwStatusWord1 := dwStatusWord1 OR 16#04000000; END_IF;          (* Bit 26 *)
IF bFirstScanDone THEN dwStatusWord1 := dwStatusWord1 OR 16#08000000; END_IF;       (* Bit 27 *)
IF bFirstOut_Latched THEN dwStatusWord1 := dwStatusWord1 OR 16#10000000; END_IF;    (* Bit 28 *)

(* -------------------------------------------------------------------------------------------------
 * Status Word 2: TMR Voting Channel Health, Hardware Interlocks & Analytical Registers
 * ------------------------------------------------------------------------------------------------- *)
dwStatusWord2 := 16#00000000;

(* Packed Sensor Health Modes (3 Bits per Group) *)
dwStatusWord2 := dwStatusWord2 OR (INT_TO_DWORD(nPT_Feed_HealthStatus) AND 16#00000007);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nPT_Ret_HealthStatus) AND 16#00000007, 3);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nPT_Perm_HealthStatus) AND 16#00000007, 6);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nAT_UV_HealthStatus) AND 16#00000007, 9);
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nFT_Feed_HealthStatus) AND 16#00000007, 12);

(* TMR Degradation Summary Flag (Bit 15) *)
IF (nPT_Feed_HealthStatus > 0) OR (nPT_Ret_HealthStatus > 0) OR (nPT_Perm_HealthStatus > 0) OR 
   (nAT_UV_HealthStatus > 0) OR (nFT_Feed_HealthStatus > 0) THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00008000;
END_IF;

IF bLevel_High_RecircTank THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF; (* Bit 16 *)
IF bLevel_Low_RecircTank THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;  (* Bit 17 *)
IF NOT bRuptureDisc_Burst_Sensor THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF; (* Bit 18: Disc OK *)

(* Pack SubState Index in Bits 24..31 *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nSubState) AND 16#000000FF, 24);

(* -------------------------------------------------------------------------------------------------
 * 3. 32-Bit Bit-Packed Process Alarm Words Telemetry Encoding
 * ------------------------------------------------------------------------------------------------- *)
(* Alarm Word 1: Critical High & High-High Process Alarms *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_TMP_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;          (* Bit 0 *)
IF bAlarm_TMP_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;           (* Bit 1 *)
IF bAlarm_Flux_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;         (* Bit 2 *)
IF bAlarm_Flux_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;          (* Bit 3 *)
IF bAlarm_Temp_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;         (* Bit 4 *)
IF bAlarm_Temp_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;          (* Bit 5 *)
IF bAlarm_Shear_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;        (* Bit 6 *)
IF bAlarm_Shear_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;         (* Bit 7 *)
IF bAlarm_SumpDev_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;      (* Bit 8 *)
IF bAlarm_SumpDev_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;       (* Bit 9 *)
IF bRuptureDisc_Burst_Sensor THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF; (* Bit 10 *)
IF bSystemTrip_Interlock THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;  (* Bit 11 *)

(* Alarm Word 2: Low & Low-Low Alarms, TMR Catastrophic Fails & Recovery Failures *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_TMP_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;           (* Bit 0 *)
IF bAlarm_TMP_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;          (* Bit 1 *)
IF bAlarm_Flux_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;          (* Bit 2 *)
IF bAlarm_Flux_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;         (* Bit 3 *)
IF bAlarm_Temp_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;          (* Bit 4 *)
IF bAlarm_Temp_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;         (* Bit 5 *)
IF bAlarm_Shear_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;         (* Bit 6 *)
IF bAlarm_Shear_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;        (* Bit 7 *)
IF bAlarm_SumpDev_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;       (* Bit 8 *)
IF bAlarm_SumpDev_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;      (* Bit 9 *)
IF nPT_Feed_HealthStatus = 5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10 *)
IF nPT_Ret_HealthStatus = 5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;  (* Bit 11 *)
IF nPT_Perm_HealthStatus = 5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12 *)
IF nAT_UV_HealthStatus = 5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;   (* Bit 13 *)
IF nFT_Feed_HealthStatus = 5 THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF; (* Bit 14 *)
IF (nState = 11) AND (rCalc_NWPFluxRecovery_pct < 90.0) THEN 
    dwAlarmWord2 := dwAlarmWord2 OR 16#00008000;                                     (* Bit 15 *)
END_IF;

(* First-Out Root Cause Diagnostic DWORD Registration *)
dwFirstOutWord := INT_TO_DWORD(nFirstOut_Code);

(* Update Active State Telemetry Outputs *)
rStateTime_s := rStateTimer_s;
nSubState := nSubState;""")

    return "\n".join(lines)

print("Phase 5 builder ready")
