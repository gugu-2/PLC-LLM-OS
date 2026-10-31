# part6_dump_alarms.py
dump_alarms_text = """(* ==========================================================================================================
   PHASE 5: HIGH-SPEED DECOMPOSITION DETECTION & SIL-3 EMERGENCY DUMP EXECUTION (< 45 MS)
   ========================================================================================================== *)
(* 5.1: Explosive Runaway Decomposition Detection Logic *)
IF (rCalculated_dPdt_Max_bar_s >= c_Lim_dPdt_HH_bar_s) OR
   (rVoted_Temp_Peak1_degC >= 325.0) OR
   (rVoted_Temp_Peak2_degC >= 328.0) OR
   (rVoted_Temp_Peak3_degC >= 325.0) OR
   (rVoted_Temp_Peak4_degC >= 320.0) OR
   (rVoted_Press_Inlet_bar >= 3250.0) OR
   (NOT bEmergencyStop) THEN

    (* Immediate Emergency State Jump *)
    iState := 120;
    bAlarm_dPdt_Decomp_HH := TRUE;
    bCmd_DumpValve_Z1_Fire := TRUE;
    bCmd_DumpValve_Z2_Fire := TRUE;
    bCmd_DumpValve_Z3_Fire := TRUE;
    bCmd_DumpValve_Z4_Fire := TRUE;
    bCmd_HyperTrip_FastStop := TRUE;
    bCmd_HPS_IsolateValve_Close := TRUE;
    bCmd_FlareCatchTank_Deluge := TRUE;
    bCmd_N2_QuenchBarrier_Open := TRUE;
    bSIL3_DumpTriggered := TRUE;
END_IF;

(* 5.2: Multi-Variable Decomposition Risk Score (0.0 to 1.0) *)
rDecompositionRiskIndex := (rCalculated_dPdt_Max_bar_s / 1500.0) * 0.45
                         + ((rVoted_Temp_Peak2_degC - 200.0) / 130.0) * 0.35
                         + ((rVoted_Press_Inlet_bar - 2500.0) / 750.0) * 0.20;
IF rDecompositionRiskIndex < 0.0 THEN rDecompositionRiskIndex := 0.0; END_IF;
IF rDecompositionRiskIndex > 1.0 THEN rDecompositionRiskIndex := 1.0; END_IF;

(* 5.3: High-Pressure Let-Down Valve Cavitation & Acoustic Shock Index *)
IF rVoted_Press_Outlet_bar > rPress_HPS_Separator_bar THEN
    rLetdownCavitationIndex := (rVoted_Press_Outlet_bar - rPress_HPS_Separator_bar) / (rVoted_Press_Outlet_bar + 1.0)
                             * (1.0 - (rPos_HPLDV_Actual_pct / 100.0));
ELSE
    rLetdownCavitationIndex := 0.0;
END_IF;

(* ==========================================================================================================
   PHASE 6: ISA-18.2 ALARMS, METRICS & BIT-PACKED TELEMETRY DWORDS
   ========================================================================================================== *)
(* 6.1: ISA-18.2 Pressure Alarms with 1.5% Deadband Hysteresis *)
IF rVoted_Press_Inlet_bar >= c_Lim_Press_HH_bar THEN
    bAlarm_Press_HH := TRUE;
ELSIF rVoted_Press_Inlet_bar <= (c_Lim_Press_HH_bar - c_Hyst_Press_bar) THEN
    bAlarm_Press_HH := FALSE;
END_IF;

IF rVoted_Press_Inlet_bar >= c_Lim_Press_H_bar THEN
    bAlarm_Press_H := TRUE;
ELSIF rVoted_Press_Inlet_bar <= (c_Lim_Press_H_bar - c_Hyst_Press_bar) THEN
    bAlarm_Press_H := FALSE;
END_IF;

IF rVoted_Press_Inlet_bar <= c_Lim_Press_LL_bar AND (iState >= 30) THEN
    bAlarm_Press_LL := TRUE;
ELSIF rVoted_Press_Inlet_bar >= (c_Lim_Press_LL_bar + c_Hyst_Press_bar) THEN
    bAlarm_Press_LL := FALSE;
END_IF;

IF rVoted_Press_Inlet_bar <= c_Lim_Press_L_bar AND (iState >= 30) THEN
    bAlarm_Press_L := TRUE;
ELSIF rVoted_Press_Inlet_bar >= (c_Lim_Press_L_bar + c_Hyst_Press_bar) THEN
    bAlarm_Press_L := FALSE;
END_IF;

(* 6.2: ISA-18.2 Reaction Peak Temperature Alarms *)
IF (rVoted_Temp_Peak1_degC >= c_Lim_Temp_HH_degC) OR (rVoted_Temp_Peak2_degC >= c_Lim_Temp_HH_degC) OR
   (rVoted_Temp_Peak3_degC >= c_Lim_Temp_HH_degC) OR (rVoted_Temp_Peak4_degC >= c_Lim_Temp_HH_degC) THEN
    bAlarm_Temp_HH := TRUE;
ELSIF (rVoted_Temp_Peak1_degC <= (c_Lim_Temp_HH_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak2_degC <= (c_Lim_Temp_HH_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak3_degC <= (c_Lim_Temp_HH_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak4_degC <= (c_Lim_Temp_HH_degC - c_Hyst_Temp_degC)) THEN
    bAlarm_Temp_HH := FALSE;
END_IF;

IF (rVoted_Temp_Peak1_degC >= c_Lim_Temp_H_degC) OR (rVoted_Temp_Peak2_degC >= c_Lim_Temp_H_degC) OR
   (rVoted_Temp_Peak3_degC >= c_Lim_Temp_H_degC) OR (rVoted_Temp_Peak4_degC >= c_Lim_Temp_H_degC) THEN
    bAlarm_Temp_H := TRUE;
ELSIF (rVoted_Temp_Peak1_degC <= (c_Lim_Temp_H_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak2_degC <= (c_Lim_Temp_H_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak3_degC <= (c_Lim_Temp_H_degC - c_Hyst_Temp_degC)) AND
      (rVoted_Temp_Peak4_degC <= (c_Lim_Temp_H_degC - c_Hyst_Temp_degC)) THEN
    bAlarm_Temp_H := FALSE;
END_IF;

(* 6.3: Mechanical & Machinery Alarms *)
IF rVib_HyperCrosshead_RMS_mm_s >= c_Lim_Vib_HH_mm_s THEN
    bAlarm_Vib_Hyper_HH := TRUE;
ELSIF rVib_HyperCrosshead_RMS_mm_s <= (c_Lim_Vib_HH_mm_s - c_Hyst_Vib_mm_s) THEN
    bAlarm_Vib_Hyper_HH := FALSE;
END_IF;

IF rVib_HyperCrosshead_RMS_mm_s >= c_Lim_Vib_H_mm_s THEN
    bAlarm_Vib_Hyper_H := TRUE;
ELSIF rVib_HyperCrosshead_RMS_mm_s <= (c_Lim_Vib_H_mm_s - c_Hyst_Vib_mm_s) THEN
    bAlarm_Vib_Hyper_H := FALSE;
END_IF;

IF rFlow_HyperPackingLeak_kg_h >= c_Lim_PackingLeak_HH_kg_h THEN
    bAlarm_PackingLeak_HH := TRUE;
ELSIF rFlow_HyperPackingLeak_kg_h <= (c_Lim_PackingLeak_HH_kg_h - c_Hyst_Leak_kg_h) THEN
    bAlarm_PackingLeak_HH := FALSE;
END_IF;

IF rFlow_HyperPackingLeak_kg_h >= c_Lim_PackingLeak_H_kg_h THEN
    bAlarm_PackingLeak_H := TRUE;
ELSIF rFlow_HyperPackingLeak_kg_h <= (c_Lim_PackingLeak_H_kg_h - c_Hyst_Leak_kg_h) THEN
    bAlarm_PackingLeak_H := FALSE;
END_IF;

IF rPress_HydrDumpAccum_bar < 160.0 THEN
    bAlarm_DumpAccum_Low := TRUE;
ELSIF rPress_HydrDumpAccum_bar >= 175.0 THEN
    bAlarm_DumpAccum_Low := FALSE;
END_IF;

IF rLetdownCavitationIndex > 0.85 THEN
    bAlarm_HPLDV_Cavitation := TRUE;
ELSIF rLetdownCavitationIndex < 0.70 THEN
    bAlarm_HPLDV_Cavitation := FALSE;
END_IF;

(* Operator Alarm Acknowledgment Clearing *)
IF bResetAlarms THEN
    IF NOT (rCalculated_dPdt_Max_bar_s >= c_Lim_dPdt_HH_bar_s) THEN bAlarm_dPdt_Decomp_HH := FALSE; END_IF;
END_IF;

(* 6.4: System Health Summary *)
bSystemHealthy := (NOT bAlarm_Press_HH) AND
                  (NOT bAlarm_Temp_HH) AND
                  (NOT bAlarm_dPdt_Decomp_HH) AND
                  (NOT bAlarm_Vib_Hyper_HH) AND
                  (NOT bAlarm_PackingLeak_HH) AND
                  (NOT bSIL3_DumpTriggered) AND
                  bEmergencyStop;

(* 6.5: 32-Bit Telemetry Bit-Packing *)
(* dwStatusWord_01: Operational States and Readiness *)
dwStatusWord_01 := 16#00000000;
IF bMasterEnable THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000001; END_IF;
IF bEmergencyStop THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000002; END_IF;
IF bEVA_ModeSelect THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000004; END_IF;
IF bAutoTuningEnable THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000008; END_IF;
IF bSystemHealthy THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000010; END_IF;
IF bSIL3_DumpTriggered THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000020; END_IF;
IF bDegraded_TMR_Active THEN dwStatusWord_01 := dwStatusWord_01 OR 16#00000040; END_IF;
dwStatusWord_01 := dwStatusWord_01 OR SHL(INT_TO_DWORD(iFSM_State), 8);
dwStatusWord_01 := dwStatusWord_01 OR SHL(INT_TO_DWORD(iFSM_SubState), 16);

(* dwStatusWord_02: Valve, Pump & Compressor Actuator Commands Feedback *)
dwStatusWord_02 := 16#00000000;
IF rCmd_HyperSpeed_rpm > 100.0 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000001; END_IF;
IF rCmd_PeroxidePump_Z1_Stroke_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000002; END_IF;
IF rCmd_PeroxidePump_Z2_Stroke_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000004; END_IF;
IF rCmd_PeroxidePump_Z3_Stroke_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000008; END_IF;
IF rCmd_PeroxidePump_Z4_Stroke_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000010; END_IF;
IF rCmd_CTA_DosingPump_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000020; END_IF;
IF rCmd_VAM_InjectionPump_pct > 0.5 THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000040; END_IF;
IF bCmd_DumpValve_Z1_Fire THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000080; END_IF;
IF bCmd_DumpValve_Z2_Fire THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000100; END_IF;
IF bCmd_DumpValve_Z3_Fire THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000200; END_IF;
IF bCmd_DumpValve_Z4_Fire THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000400; END_IF;
IF bCmd_HyperTrip_FastStop THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00000800; END_IF;
IF bCmd_HPS_IsolateValve_Close THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00001000; END_IF;
IF bCmd_FlareCatchTank_Deluge THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00002000; END_IF;
IF bCmd_N2_QuenchBarrier_Open THEN dwStatusWord_02 := dwStatusWord_02 OR 16#00004000; END_IF;

(* dwAlarmWord_01: ISA-18.2 Critical Emergency & High-High Trips *)
dwAlarmWord_01 := 16#00000000;
IF bAlarm_dPdt_Decomp_HH THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000001; END_IF;
IF bAlarm_Press_HH THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000002; END_IF;
IF bAlarm_Temp_HH THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000004; END_IF;
IF bAlarm_Vib_Hyper_HH THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000008; END_IF;
IF bAlarm_PackingLeak_HH THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000010; END_IF;
IF bAlarm_DumpAccum_Low THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000020; END_IF;
IF NOT bEmergencyStop THEN dwAlarmWord_01 := dwAlarmWord_01 OR 16#00000040; END_IF;

(* dwAlarmWord_02: ISA-18.2 High and Low Process Warnings *)
dwAlarmWord_02 := 16#00000000;
IF bAlarm_Press_H THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000001; END_IF;
IF bAlarm_Press_L THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000002; END_IF;
IF bAlarm_Press_LL THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000004; END_IF;
IF bAlarm_Temp_H THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000008; END_IF;
IF bAlarm_Temp_L THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000010; END_IF;
IF bAlarm_Temp_LL THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000020; END_IF;
IF bAlarm_Vib_Hyper_H THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000040; END_IF;
IF bAlarm_PackingLeak_H THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000080; END_IF;
IF bAlarm_HPLDV_Cavitation THEN dwAlarmWord_02 := dwAlarmWord_02 OR 16#00000100; END_IF;

(* dwAlarmWord_03: Machinery & Hydraulic Interlocks *)
dwAlarmWord_03 := 16#00000000;
IF rPress_FlareHeader_bar > 3.0 THEN dwAlarmWord_03 := dwAlarmWord_03 OR 16#00000001; END_IF;
IF rTemp_HyperBearing_degC > 85.0 THEN dwAlarmWord_03 := dwAlarmWord_03 OR 16#00000002; END_IF;
IF rPress_HPS_Separator_bar > 320.0 THEN dwAlarmWord_03 := dwAlarmWord_03 OR 16#00000004; END_IF;
IF rPress_HPS_Separator_bar < 180.0 THEN dwAlarmWord_03 := dwAlarmWord_03 OR 16#00000008; END_IF;

(* dwDiagnosticWord_01: 2oo3 TMR Sensor Health Bitfield *)
dwDiagnosticWord_01 := 16#00000000;
IF NOT bInlet_ChA_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000001; END_IF;
IF NOT bInlet_ChB_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000002; END_IF;
IF NOT bInlet_ChC_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000004; END_IF;
IF NOT bZ1_ChA_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000008; END_IF;
IF NOT bZ1_ChB_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000010; END_IF;
IF NOT bZ1_ChC_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000020; END_IF;
IF NOT bT1_ChA_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000040; END_IF;
IF NOT bT1_ChB_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000080; END_IF;
IF NOT bT1_ChC_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000100; END_IF;
IF NOT bHyper_ChA_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000200; END_IF;
IF NOT bHyper_ChB_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000400; END_IF;
IF NOT bHyper_ChC_Healthy THEN dwDiagnosticWord_01 := dwDiagnosticWord_01 OR 16#00000800; END_IF;

(* dwDiagnosticWord_02: Solvers, Estimators and Slew Limits *)
dwDiagnosticWord_02 := 16#00000000;
IF ABS(rCalculated_dPdt_Inlet) > 200.0 THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000001; END_IF;
IF rDecompositionRiskIndex > 0.50 THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000002; END_IF;
IF rLetdownCavitationIndex > 0.60 THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000004; END_IF;
IF bAutoTuningEnable THEN dwDiagnosticWord_02 := dwDiagnosticWord_02 OR 16#00000008; END_IF;

END_FUNCTION_BLOCK
"""

