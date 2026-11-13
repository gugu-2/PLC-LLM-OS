# steel_dri_builder/part8_phase5_alarms.py
"""
Part 8: Phase 5 - ISA-18.2 Multi-Tier Process Alarms, SIL-3 Interlocks & 32-Bit Telemetry
"""

def get_phase5_alarms():
    return """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, ANTI-STICTION DITHER & 32-BIT BIT-PACKED TELEMETRY      *)
(* ==================================================================================================== *)

(* 5.1 SIL-3 Fast Oxygen Ingress Deflagration Trip Detection (<20 ms Latency) *)
(* Evaluate highest trace O2 readings across redundant zirconia analyzers *)
IF rAT_O2_Inlet_601A >= rAT_O2_Inlet_601B THEN
    rO2_Inlet_Rate := (rAT_O2_Inlet_601A - rO2_Prev_Inlet) / rTs_Seconds;
    rO2_Prev_Inlet := rAT_O2_Inlet_601A;
ELSE
    rO2_Inlet_Rate := (rAT_O2_Inlet_601B - rO2_Prev_Inlet) / rTs_Seconds;
    rO2_Prev_Inlet := rAT_O2_Inlet_601B;
END_IF;

IF (rAT_O2_Inlet_601A >= rO2_Max_Safety_Trip) OR (rAT_O2_Inlet_601B >= rO2_Max_Safety_Trip) OR
   (rAT_O2_TopGas_602A >= 0.15) OR (rAT_O2_TopGas_602B >= 0.15) OR (rO2_Inlet_Rate >= rO2_Max_RateOfRise) THEN
    bO2_Ingress_InterlockTripped := TRUE;
    bOxygenIngressTrip := TRUE;
END_IF;

IF bReset AND (rAT_O2_Inlet_601A < 0.05) AND (rAT_O2_Inlet_601B < 0.05) AND
   (rAT_O2_TopGas_602A < 0.06) AND (rAT_O2_TopGas_602B < 0.06) THEN
    bO2_Ingress_InterlockTripped := FALSE;
    bOxygenIngressTrip := FALSE;
END_IF;


(* 5.2 ISA-18.2 Multi-Tier Alarm Matrix with Deadband Clearance Hysteresis *)

(* Parameter 1: Bustle Pipe Temperature [deg C] *)
IF rPV_BustleTemp_Voted >= rLimit_Bustle_HH THEN
    bAlarm_Bustle_HH := TRUE;
ELSIF rPV_BustleTemp_Voted <= (rLimit_Bustle_HH - rHyst_Bustle) THEN
    bAlarm_Bustle_HH := FALSE;
END_IF;

IF rPV_BustleTemp_Voted >= rLimit_Bustle_H THEN
    bAlarm_Bustle_H := TRUE;
ELSIF rPV_BustleTemp_Voted <= (rLimit_Bustle_H - rHyst_Bustle) THEN
    bAlarm_Bustle_H := FALSE;
END_IF;

IF rPV_BustleTemp_Voted <= rLimit_Bustle_L THEN
    bAlarm_Bustle_L := TRUE;
ELSIF rPV_BustleTemp_Voted >= (rLimit_Bustle_L + rHyst_Bustle) THEN
    bAlarm_Bustle_L := FALSE;
END_IF;

IF rPV_BustleTemp_Voted <= rLimit_Bustle_LL THEN
    bAlarm_Bustle_LL := TRUE;
ELSIF rPV_BustleTemp_Voted >= (rLimit_Bustle_LL + rHyst_Bustle) THEN
    bAlarm_Bustle_LL := FALSE;
END_IF;

(* Parameter 2: Shaft Differential Pressure [kPa] *)
IF rPV_ShaftDP_Voted >= rLimit_ShaftDP_HH THEN
    bAlarm_ShaftDP_HH := TRUE;
ELSIF rPV_ShaftDP_Voted <= (rLimit_ShaftDP_HH - rHyst_ShaftDP) THEN
    bAlarm_ShaftDP_HH := FALSE;
END_IF;

IF rPV_ShaftDP_Voted >= rLimit_ShaftDP_H THEN
    bAlarm_ShaftDP_H := TRUE;
ELSIF rPV_ShaftDP_Voted <= (rLimit_ShaftDP_H - rHyst_ShaftDP) THEN
    bAlarm_ShaftDP_H := FALSE;
END_IF;

IF rPV_ShaftDP_Voted <= rLimit_ShaftDP_L THEN
    bAlarm_ShaftDP_L := TRUE;
ELSIF rPV_ShaftDP_Voted >= (rLimit_ShaftDP_L + rHyst_ShaftDP) THEN
    bAlarm_ShaftDP_L := FALSE;
END_IF;

IF rPV_ShaftDP_Voted <= rLimit_ShaftDP_LL THEN
    bAlarm_ShaftDP_LL := TRUE;
ELSIF rPV_ShaftDP_Voted >= (rLimit_ShaftDP_LL + rHyst_ShaftDP) THEN
    bAlarm_ShaftDP_LL := FALSE;
END_IF;

(* Parameter 3: Top Gas H2/CO Ratio [ratio] *)
IF rPV_TopGasH2CO_Voted >= rLimit_GasH2CO_HH THEN
    bAlarm_GasH2CO_HH := TRUE;
ELSIF rPV_TopGasH2CO_Voted <= (rLimit_GasH2CO_HH - rHyst_GasH2CO) THEN
    bAlarm_GasH2CO_HH := FALSE;
END_IF;

IF rPV_TopGasH2CO_Voted >= rLimit_GasH2CO_H THEN
    bAlarm_GasH2CO_H := TRUE;
ELSIF rPV_TopGasH2CO_Voted <= (rLimit_GasH2CO_H - rHyst_GasH2CO) THEN
    bAlarm_GasH2CO_H := FALSE;
END_IF;

IF rPV_TopGasH2CO_Voted <= rLimit_GasH2CO_L THEN
    bAlarm_GasH2CO_L := TRUE;
ELSIF rPV_TopGasH2CO_Voted >= (rLimit_GasH2CO_L + rHyst_GasH2CO) THEN
    bAlarm_GasH2CO_L := FALSE;
END_IF;

IF rPV_TopGasH2CO_Voted <= rLimit_GasH2CO_LL THEN
    bAlarm_GasH2CO_LL := TRUE;
ELSIF rPV_TopGasH2CO_Voted >= (rLimit_GasH2CO_LL + rHyst_GasH2CO) THEN
    bAlarm_GasH2CO_LL := FALSE;
END_IF;

(* Parameter 4: Discharged DRI Bound Carbon [wt% C] *)
IF x_Hat[6] >= rLimit_Carbon_HH THEN
    bAlarm_Carbon_HH := TRUE;
ELSIF x_Hat[6] <= (rLimit_Carbon_HH - rHyst_Carbon) THEN
    bAlarm_Carbon_HH := FALSE;
END_IF;

IF x_Hat[6] >= rLimit_Carbon_H THEN
    bAlarm_Carbon_H := TRUE;
ELSIF x_Hat[6] <= (rLimit_Carbon_H - rHyst_Carbon) THEN
    bAlarm_Carbon_H := FALSE;
END_IF;

IF x_Hat[6] <= rLimit_Carbon_L THEN
    bAlarm_Carbon_L := TRUE;
ELSIF x_Hat[6] >= (rLimit_Carbon_L + rHyst_Carbon) THEN
    bAlarm_Carbon_L := FALSE;
END_IF;

IF x_Hat[6] <= rLimit_Carbon_LL THEN
    bAlarm_Carbon_LL := TRUE;
ELSIF x_Hat[6] >= (rLimit_Carbon_LL + rHyst_Carbon) THEN
    bAlarm_Carbon_LL := FALSE;
END_IF;


(* 5.3 Bit-Packed 32-Bit Telemetry Status Words *)

(* dwStatusWord1: System Operating Mode, Interlocks and Critical Flags *)
dwStatusWord1 := 16#00000000;
IF bInitialized THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bEnable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bAutoMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bMPC_OptimalActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bFurnaceReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF bPellet_Feed_Permissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bDischarge_Feeder_Permissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bHeater_Ignition_Permissive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bRoof_Snort_Dump_Open THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bNitrogen_Purge_Valve_Cmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bCluster_Breaker_Vibrator_Cmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bClusterStickingWarning THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bTMR_DegradedAlarm THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bTMR_CriticalFailureAlarm THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bEmergencyStop THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bHeartbeatBit THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;

(* Actuator High Saturation Bits (16..21) *)
IF u_Act[1] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;
IF u_Act[2] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;
IF u_Act[3] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF;
IF u_Act[4] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF;
IF u_Act[5] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF;
IF u_Act[6] >= 99.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF;

(* Actuator Low Saturation Bits (22..27) *)
IF u_Act[1] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF;
IF u_Act[2] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF;
IF u_Act[3] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#01000000; END_IF;
IF u_Act[4] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#02000000; END_IF;
IF u_Act[5] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#04000000; END_IF;
IF u_Act[6] <= 0.5 THEN dwStatusWord1 := dwStatusWord1 OR 16#08000000; END_IF;


(* dwStatusWord2: Active FSM State, Sub-Phase & Sensor Channel Health *)
dwStatusWord2 := INT_TO_DWORD(iState) AND 16#0000000F;
dwStatusWord2 := dwStatusWord2 OR (SHL(INT_TO_DWORD(iFSM_SubPhase), 4) AND 16#000000F0);

(* TMR Individual Channel Degraded Flags (Bits 8..13) *)
IF bTMR_Bustle_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bTMR_ShaftDP_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bTMR_GasH2CO_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bTMR_GasCO2_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bTMR_Burden_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bTMR_DRITemp_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;

(* TMR Individual Channel Critical Flags (Bits 14..19) *)
IF bTMR_Bustle_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bTMR_ShaftDP_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;
IF bTMR_GasH2CO_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bTMR_GasCO2_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bTMR_Burden_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF bTMR_DRITemp_Critical THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

(* Product Metallization Quality Tier (Bits 20..21) *)
IF x_Hat[2] >= 94.5 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00300000; (* Tier 3: Premium EAF DRI >= 94.5% *)
ELSIF x_Hat[2] >= 90.0 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00200000; (* Tier 2: Standard DRI 90.0 - 94.5% *)
ELSIF x_Hat[2] >= 75.0 THEN
    dwStatusWord2 := dwStatusWord2 OR 16#00100000; (* Tier 1: Sub-Grade Ramp DRI *)
ELSE
    dwStatusWord2 := dwStatusWord2 OR 16#00000000; (* Tier 0: Unreduced Mineral *)
END_IF;


(* dwAlarmWord1: High and High-High Alarms (ISA-18.2 Warning & Trip Vectors) *)
dwAlarmWord1 := 16#00000000;
IF bAlarm_Bustle_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarm_Bustle_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarm_ShaftDP_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarm_ShaftDP_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarm_GasH2CO_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarm_GasH2CO_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarm_Carbon_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarm_Carbon_H THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bOxygenIngressTrip THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF (rPV_DRITemp_Voted > 750.0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF (rPT_CoolingGas_701 > 220.0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF (rPV_BurdenLevel_Voted > 22.0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;


(* dwAlarmWord2: Low and Low-Low Alarms & Sensor Fault Flags *)
dwAlarmWord2 := 16#00000000;
IF bAlarm_Bustle_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarm_Bustle_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarm_ShaftDP_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarm_ShaftDP_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarm_GasH2CO_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bAlarm_GasH2CO_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bAlarm_Carbon_LL THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_Carbon_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF (rPV_BurdenLevel_Voted < 12.0) THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF (rPT_CoolingGas_701 < 100.0) THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bTMR_Bustle_DiscAB OR bTMR_Bustle_DiscBC OR bTMR_Bustle_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;
IF bTMR_ShaftDP_DiscAB OR bTMR_ShaftDP_DiscBC OR bTMR_ShaftDP_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF;
IF bTMR_GasH2CO_DiscAB OR bTMR_GasH2CO_DiscBC OR bTMR_GasH2CO_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF;
IF bTMR_GasCO2_DiscAB OR bTMR_GasCO2_DiscBC OR bTMR_GasCO2_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF;
IF bTMR_Burden_DiscAB OR bTMR_Burden_DiscBC OR bTMR_Burden_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00004000; END_IF;
IF bTMR_DRITemp_DiscAB OR bTMR_DRITemp_DiscBC OR bTMR_DRITemp_DiscAC THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00008000; END_IF;

END_FUNCTION_BLOCK
"""
