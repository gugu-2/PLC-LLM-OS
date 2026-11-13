# cbw_tunnel_washer_builder/part7_alarms_diagnostics.py
# ISA-18.2 Process Alarms, Bit-Packed Registers & Diagnostic Management

def get_part7_alarms_diagnostics():
    return """(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS & 32-BIT BIT-PACKED STATUS WORDS                          *)
(* ==================================================================================================== *)

(* -------------------------------------------------------------------------------------------------- *)
(* ISA-18.2 PROCESS ALARM EVALUATION WITH DEADBAND HYSTERESIS                                         *)
(* -------------------------------------------------------------------------------------------------- *)
(* TT-101 Main Wash Temperature High-High Trip (92.0 C, Deadband 1.5 C) *)
IF rVotedMainWashTemp_degC >= rTrip_TT101_HH THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000001; (* Bit 0 *)
    bSequenceFault := TRUE;
ELSIF rVotedMainWashTemp_degC <= (rTrip_TT101_HH - rDeadband_TT101) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFFE;
    END_IF;
END_IF;

(* TT-101 Main Wash Temperature High Warning (88.0 C, Deadband 1.5 C) *)
IF rVotedMainWashTemp_degC >= rTrip_TT101_H THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000002; (* Bit 1 *)
ELSIF rVotedMainWashTemp_degC <= (rTrip_TT101_H - rDeadband_TT101) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFFD;
    END_IF;
END_IF;

(* TT-101 Main Wash Temperature Low Warning (80.0 C in Stage 5, Deadband 1.5 C) *)
IF (nFsmState = 5) AND (rVotedMainWashTemp_degC <= rTrip_TT101_L) THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000004; (* Bit 2 *)
ELSIF rVotedMainWashTemp_degC >= (rTrip_TT101_L + rDeadband_TT101) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFFB;
    END_IF;
END_IF;

(* TT-101 Main Wash Temperature Low-Low Disinfection Trip (72.0 C, Deadband 1.5 C) *)
IF (nFsmState = 5) AND (tStateTimer >= T#15000MS) AND (rVotedMainWashTemp_degC <= rTrip_TT101_LL) THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000008; (* Bit 3 *)
    bSequenceFault := TRUE;
ELSIF rVotedMainWashTemp_degC >= (rTrip_TT101_LL + rDeadband_TT101) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFF7;
    END_IF;
END_IF;

(* AT-201 Rinse Conductivity High-High Detergent Carryover Trip (0.65 mS/cm) *)
IF rVotedRinseConductivity_mS >= rTrip_AT201_HH THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000010; (* Bit 4 *)
    bSequenceFault := TRUE;
ELSIF rVotedRinseConductivity_mS <= (rTrip_AT201_HH - rDeadband_AT201) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFEF;
    END_IF;
END_IF;

(* AT-201 Rinse Conductivity High Warning (0.45 mS/cm) *)
IF rVotedRinseConductivity_mS >= rTrip_AT201_H THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000020; (* Bit 5 *)
ELSIF rVotedRinseConductivity_mS <= (rTrip_AT201_H - rDeadband_AT201) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFDF;
    END_IF;
END_IF;

(* PT-301 Hydraulic Press High-High Overpressure Trip (53.0 bar) *)
IF rVotedPressPressure_bar >= rTrip_PT301_HH THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000040; (* Bit 6 *)
    bSequenceFault := TRUE;
ELSIF rVotedPressPressure_bar <= (rTrip_PT301_HH - rDeadband_PT301) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFFBF;
    END_IF;
END_IF;

(* PT-301 Hydraulic Press Low Pressure Compaction Failure in Phase D (< 32.0 bar) *)
IF (nFsmState = 11) AND (nDewaterSequenceStep = 3) AND (tPressRampTimer >= T#10000MS) AND (rVotedPressPressure_bar <= rTrip_PT301_LL) THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000080; (* Bit 7 *)
    bSequenceFault := TRUE;
ELSIF rVotedPressPressure_bar >= (rTrip_PT301_LL + rDeadband_PT301) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFF7F;
    END_IF;
END_IF;

(* FT-401 Cold Freshwater Supply Feed Failure Low-Low (< 1.2 m3/h when intake commanded) *)
IF (rFreshwaterMakeupValveCmd_pct >= 50.0) AND (tStateTimer >= T#5000MS) AND (rVotedFreshwaterFlow_m3h <= rTrip_FT401_LL) THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000100; (* Bit 8 *)
    bSequenceFault := TRUE;
ELSIF rVotedFreshwaterFlow_m3h >= (rTrip_FT401_LL + rDeadband_FT401) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFEFF;
    END_IF;
END_IF;

(* ST-501 Drum Drive Mechanical Jam Overload Torque High-High Trip (4500 N*m) *)
IF rVotedDrumTorque_Nm >= rTrip_ST501_HH THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000200; (* Bit 9 *)
    bSequenceFault := TRUE;
ELSIF rVotedDrumTorque_Nm <= (rTrip_ST501_HH - rDeadband_ST501) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFDFF;
    END_IF;
END_IF;

(* PDT-902 Rotary Drum Lint Screen Blinding High-High Trip (1.40 bar) *)
IF rPDT_902_LintFilterDiffPress_bar >= rTrip_PDT902_HH THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000400; (* Bit 10 *)
    bSequenceFault := TRUE;
ELSIF rPDT_902_LintFilterDiffPress_bar <= (rTrip_PDT902_HH - rDeadband_PDT902) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFFBFF;
    END_IF;
END_IF;

(* PDT-902 Rotary Drum Lint Screen Backwash Warning (1.10 bar) *)
IF rPDT_902_LintFilterDiffPress_bar >= rTrip_PDT902_H THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00000800; (* Bit 11 *)
ELSIF rPDT_902_LintFilterDiffPress_bar <= (rTrip_PDT902_H - rDeadband_PDT902) THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFF7FF;
    END_IF;
END_IF;

(* Live Steam Supply Header Pressure Low (< 3.5 bar) *)
IF rPT_801_SteamHeaderPress_bar < 3.5 THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00001000; (* Bit 12 *)
ELSIF rPT_801_SteamHeaderPress_bar >= 4.0 THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFEFFF;
    END_IF;
END_IF;

(* HPU Hydraulic Sump Oil Temperature High (> 65.0 C) *)
IF rTT_302_HydraulicOilTemp_degC > 65.0 THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00002000; (* Bit 13 *)
ELSIF rTT_302_HydraulicOilTemp_degC <= 60.0 THEN
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFDFFF;
    END_IF;
END_IF;

(* Chemical Suction Tanks Low Level Discrete Float Warning *)
IF bChemicalSuctionTanksLow_DI503 THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00004000; (* Bit 14 *)
ELSE
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFFBFFF;
    END_IF;
END_IF;

(* Linen Cake Residual Moisture Out-of-Tolerance Warning (> 54.0%) *)
IF (nFsmState = 12) AND (rEstimatedCakeMoisture_pct > 54.0) THEN
    dwAlarmWordProcess := dwAlarmWordProcess OR 16#00008000; (* Bit 15 *)
ELSE
    IF bAckAlarm THEN
        dwAlarmWordProcess := dwAlarmWordProcess AND 16#FFFF7FFF;
    END_IF;
END_IF;


(* -------------------------------------------------------------------------------------------------- *)
(* 2oo3 SENSOR DIAGNOSTIC ALARM REGISTER PACKING (dwAlarmWordSensors)                                 *)
(* -------------------------------------------------------------------------------------------------- *)
dwAlarmWordSensors := 16#00000000;
IF NOT bTT_101A_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000001; END_IF;
IF NOT bTT_101B_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000002; END_IF;
IF NOT bTT_101C_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000004; END_IF;
IF bTT_101_DiscrepancyFault_AB THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000008; END_IF;
IF bTT_101_DiscrepancyFault_BC THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000010; END_IF;
IF bTT_101_DiscrepancyFault_CA THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000020; END_IF;

IF NOT bAT_201A_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000040; END_IF;
IF NOT bAT_201B_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000080; END_IF;
IF NOT bAT_201C_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000100; END_IF;
IF bAT_201_DiscrepancyFault_AB THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000200; END_IF;
IF bAT_201_DiscrepancyFault_BC THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000400; END_IF;
IF bAT_201_DiscrepancyFault_CA THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00000800; END_IF;

IF NOT bPT_301A_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00001000; END_IF;
IF NOT bPT_301B_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00002000; END_IF;
IF NOT bPT_301C_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00004000; END_IF;
IF bPT_301_DiscrepancyFault_AB THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00008000; END_IF;
IF bPT_301_DiscrepancyFault_BC THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00010000; END_IF;
IF bPT_301_DiscrepancyFault_CA THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00020000; END_IF;

IF NOT bFT_401A_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00040000; END_IF;
IF NOT bFT_401B_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00080000; END_IF;
IF NOT bFT_401C_Valid THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00100000; END_IF;
IF bFT_401_DiscrepancyFault_AB THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00200000; END_IF;
IF bFT_401_DiscrepancyFault_BC THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00400000; END_IF;
IF bFT_401_DiscrepancyFault_CA THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#00800000; END_IF;

IF bST_501_DiscrepancyFault THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#01000000; END_IF;
IF bLT_601_DiscrepancyFault THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#02000000; END_IF;
IF bTT_701_DiscrepancyFault THEN dwAlarmWordSensors := dwAlarmWordSensors OR 16#04000000; END_IF;


(* -------------------------------------------------------------------------------------------------- *)
(* 32-BIT SYSTEM STATUS REGISTER PACKING (dwSystemStatusWord)                                         *)
(* -------------------------------------------------------------------------------------------------- *)
dwSystemStatusWord := 16#00000000;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000001; END_IF;              (* Bit 0 *)
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; END_IF;            (* Bit 1 *)
IF bDrumTransferCycleActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; END_IF;  (* Bit 2 *)
IF bDewateringPressActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; END_IF;    (* Bit 3 *)
IF (rMainWashSteamValveCmd_pct > 1.0) OR (rBleachSteamValveCmd_pct > 1.0) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000010;                                        (* Bit 4 *)
END_IF;
IF (rAlkaliDosingPumpCmd_ml > 1.0) OR (rDetergentDosingPumpCmd_ml > 1.0) OR (rBleachDosingPumpCmd_ml > 1.0) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000020;                                        (* Bit 5 *)
END_IF;
IF rCounterFlowRecircPumpCmd_pct > 5.0 THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#00000040;                                        (* Bit 6 *)
END_IF;
IF bLintFilterBackwashValveCmd THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;(* Bit 7 *)
IF rThermalEnergyReclaimed_kW > 10.0 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; END_IF; (* Bit 8 *)
IF bDegradedSensorMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000200; END_IF;      (* Bit 9 *)
IF bSequenceFault THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000400; END_IF;           (* Bit 10 *)
IF bDrumHomePosition_LS101 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000800; END_IF;  (* Bit 11 *)
IF bPressRamTopDeadCenter_LS301 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00001000; END_IF; (* Bit 12 *)
IF bShuttleConveyorInPosition_LS601 THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00002000; END_IF; (* Bit 13 *)
IF bEmergencyStop THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00004000; END_IF;           (* Bit 14: E-Stop Healthy *)
IF (dwAlarmWordProcess <> 16#00000000) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00008000; END_IF; (* Bit 15: Alarm Active *)

(* Pack Active FSM Stage into Upper Word Bits 16..23 *)
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(nFsmState), 16);

(* Fast Execution Scan Increment *)
nScanCounter := nScanCounter + 1;

END_FUNCTION_BLOCK
"""
