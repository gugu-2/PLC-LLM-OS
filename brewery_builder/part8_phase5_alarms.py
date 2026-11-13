# brewery_builder/part8_phase5_alarms.py

def get_part8():
    return """(* ============================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM MATRIX & BIT-PACKED TELEMETRY                       *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.1: ISA-18.2 PROCESS ALARM DEBOUNCING & HYSTERESIS TRIP EVALUATION                       *)
(* ---------------------------------------------------------------------------------------------- *)

(* 1. Lauter Tun Grain Bed Differential Pressure Alarms *)
IF fVotedGrainBedDP >= fLauterDP_TripHH THEN
    tTimerDP_HH := tTimerDP_HH + fCycleDeltaTimeSec;
    IF tTimerDP_HH >= 0.300 THEN
        bAlarmDP_HH_Active := TRUE;
        bUnackDP_HH := TRUE;
    END_IF;
ELSIF fVotedGrainBedDP <= (fLauterDP_TripHH - fLauterDP_Deadband) THEN
    tTimerDP_HH := 0.0;
    bAlarmDP_HH_Active := FALSE;
END_IF;

IF fVotedGrainBedDP >= fLauterDP_TripH THEN
    tTimerDP_H := tTimerDP_H + fCycleDeltaTimeSec;
    IF tTimerDP_H >= 0.500 THEN
        bAlarmDP_H_Active := TRUE;
    END_IF;
ELSIF fVotedGrainBedDP <= (fLauterDP_TripH - fLauterDP_Deadband) THEN
    tTimerDP_H := 0.0;
    bAlarmDP_H_Active := FALSE;
END_IF;

(* 2. Vorlauf Wort Clarity & Optical Turbidity Alarms *)
IF fVotedWortTurbidity >= fTurbidity_TripHH THEN
    tTimerTurb_HH := tTimerTurb_HH + fCycleDeltaTimeSec;
    IF tTimerTurb_HH >= 0.400 THEN
        bAlarmTurb_HH_Active := TRUE;
        bUnackTurb_HH := TRUE;
    END_IF;
ELSIF fVotedWortTurbidity <= (fTurbidity_TripHH - fTurbidity_Deadband) THEN
    tTimerTurb_HH := 0.0;
    bAlarmTurb_HH_Active := FALSE;
END_IF;

IF fVotedWortTurbidity >= fTurbidity_TripH THEN
    tTimerTurb_H := tTimerTurb_H + fCycleDeltaTimeSec;
    IF tTimerTurb_H >= 0.600 THEN
        bAlarmTurb_H_Active := TRUE;
    END_IF;
ELSIF fVotedWortTurbidity <= (fTurbidity_TripH - fTurbidity_Deadband) THEN
    tTimerTurb_H := 0.0;
    bAlarmTurb_H_Active := FALSE;
END_IF;

(* 3. Wort Kettle Boiling Temperature RTD Alarms *)
IF fVotedKettleTemp >= fKettleTemp_TripHH THEN
    tTimerTemp_HH := tTimerTemp_HH + fCycleDeltaTimeSec;
    IF tTimerTemp_HH >= 0.300 THEN
        bAlarmTemp_HH_Active := TRUE;
        bUnackTemp_HH := TRUE;
    END_IF;
ELSIF fVotedKettleTemp <= (fKettleTemp_TripHH - fKettleTemp_Deadband) THEN
    tTimerTemp_HH := 0.0;
    bAlarmTemp_HH_Active := FALSE;
END_IF;

IF fVotedKettleTemp >= fKettleTemp_TripH THEN
    tTimerTemp_H := tTimerTemp_H + fCycleDeltaTimeSec;
    IF tTimerTemp_H >= 0.500 THEN
        bAlarmTemp_H_Active := TRUE;
    END_IF;
ELSIF fVotedKettleTemp <= (fKettleTemp_TripH - fKettleTemp_Deadband) THEN
    tTimerTemp_H := 0.0;
    bAlarmTemp_H_Active := FALSE;
END_IF;

(* Low Temperature Boiling Simmer Failure (Active only during Vigorous Boil State 11) *)
IF (eState = 11) AND (fVotedKettleTemp <= fKettleTemp_TripLL) THEN
    tTimerTemp_LL := tTimerTemp_LL + fCycleDeltaTimeSec;
    IF tTimerTemp_LL >= 1.000 THEN
        bAlarmTemp_LL_Active := TRUE;
    END_IF;
ELSIF (fVotedKettleTemp >= (fKettleTemp_TripLL + fKettleTemp_Deadband)) OR (eState <> 11) THEN
    tTimerTemp_LL := 0.0;
    bAlarmTemp_LL_Active := FALSE;
END_IF;

(* 4. Calandria Saturated Steam Header Pressure Alarms *)
IF fVotedCalandriaSteamP >= fSteamP_TripHH THEN
    tTimerSteamP_HH := tTimerSteamP_HH + fCycleDeltaTimeSec;
    IF tTimerSteamP_HH >= 0.250 THEN
        bAlarmSteamP_HH_Active := TRUE;
        bUnackSteamP_HH := TRUE;
    END_IF;
ELSIF fVotedCalandriaSteamP <= (fSteamP_TripHH - fSteamP_Deadband) THEN
    tTimerSteamP_HH := 0.0;
    bAlarmSteamP_HH_Active := FALSE;
END_IF;

IF fVotedCalandriaSteamP >= fSteamP_TripH THEN
    tTimerSteamP_H := tTimerSteamP_H + fCycleDeltaTimeSec;
    IF tTimerSteamP_H >= 0.400 THEN
        bAlarmSteamP_H_Active := TRUE;
    END_IF;
ELSIF fVotedCalandriaSteamP <= (fSteamP_TripH - fSteamP_Deadband) THEN
    tTimerSteamP_H := 0.0;
    bAlarmSteamP_H_Active := FALSE;
END_IF;

(* 5. Wort Kettle Radar Hydrostatic Level Alarms *)
IF fVotedKettleLevel >= fKettleLevel_TripHH THEN
    tTimerLevel_HH := tTimerLevel_HH + fCycleDeltaTimeSec;
    IF tTimerLevel_HH >= 0.350 THEN
        bAlarmLevel_HH_Active := TRUE;
        bUnackLevel_HH := TRUE;
    END_IF;
ELSIF fVotedKettleLevel <= (fKettleLevel_TripHH - fKettleLevel_Deadband) THEN
    tTimerLevel_HH := 0.0;
    bAlarmLevel_HH_Active := FALSE;
END_IF;

(* 6. Wort Rake Mechanical Drive Dynamic Load Torque Alarms *)
IF fRakeMotorTorque >= fRakeTorque_TripHH THEN
    tTimerTorque_HH := tTimerTorque_HH + fCycleDeltaTimeSec;
    IF tTimerTorque_HH >= 0.200 THEN
        bAlarmTorque_HH_Active := TRUE;
        bUnackTorque_HH := TRUE;
    END_IF;
ELSIF fRakeMotorTorque <= (fRakeTorque_TripHH - fRakeTorque_Deadband) THEN
    tTimerTorque_HH := 0.0;
    bAlarmTorque_HH_Active := FALSE;
END_IF;

IF fRakeMotorTorque >= fRakeTorque_TripH THEN
    tTimerTorque_H := tTimerTorque_H + fCycleDeltaTimeSec;
    IF tTimerTorque_H >= 0.400 THEN
        bAlarmTorque_H_Active := TRUE;
    END_IF;
ELSIF fRakeMotorTorque <= (fRakeTorque_TripH - fRakeTorque_Deadband) THEN
    tTimerTorque_H := 0.0;
    bAlarmTorque_H_Active := FALSE;
END_IF;

(* 7. Emergency Stop Circuit Tripped Alarm *)
bAlarmEmergencyStopActive := NOT bEmergencyStop;

(* Common Priority 1 Critical High-High Trip Master Latch *)
bAlarmHighHigh := bAlarmDP_HH_Active OR bAlarmTemp_HH_Active OR bAlarmSteamP_HH_Active OR
                  bAlarmLevel_HH_Active OR bAlarmTorque_HH_Active OR bAlarmEmergencyStopActive;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.2: ROOT-CAUSE FIRST-OUT LATENT MEMORY LATCH                                             *)
(* ---------------------------------------------------------------------------------------------- *)
IF NOT bFirstOutLatched THEN
    IF bAlarmEmergencyStopActive THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000001; (* Code 1: Emergency Stop Pushbutton Tripped *)
    ELSIF bAlarmDP_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000002; (* Code 2: Grain Bed Extreme Differential Pressure *)
    ELSIF bAlarmLevel_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000004; (* Code 4: Kettle Overfill Hydrostatic Level HH *)
    ELSIF bAlarmTemp_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000008; (* Code 8: Calandria Boiling Overtemperature HH *)
    ELSIF bAlarmSteamP_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000010; (* Code 16: Calandria High Pressure Steam HH *)
    ELSIF bAlarmTorque_HH_Active THEN
        bFirstOutLatched := TRUE;
        dwFirstOutCode := 16#00000020; (* Code 32: Wort Rake Mechanical Drive Jam HH *)
    END_IF;
END_IF;

(* Reset Logic for Latched Alarms & First-Out Memory *)
IF bReset THEN
    bUnackDP_HH := FALSE;
    bUnackTurb_HH := FALSE;
    bUnackTemp_HH := FALSE;
    bUnackSteamP_HH := FALSE;
    bUnackLevel_HH := FALSE;
    bUnackTorque_HH := FALSE;
    bFirstOutLatched := FALSE;
    dwFirstOutCode := 16#00000000;
    bError := FALSE;

    (* Clear TMR Latched Sensor Faults on Explicit Reset *)
    bCh1_S1_FaultLatched := FALSE; bCh1_S2_FaultLatched := FALSE; bCh1_S3_FaultLatched := FALSE;
    bCh2_S1_FaultLatched := FALSE; bCh2_S2_FaultLatched := FALSE; bCh2_S3_FaultLatched := FALSE;
    bCh3_S1_FaultLatched := FALSE; bCh3_S2_FaultLatched := FALSE; bCh3_S3_FaultLatched := FALSE;
    bCh4_S1_FaultLatched := FALSE; bCh4_S2_FaultLatched := FALSE; bCh4_S3_FaultLatched := FALSE;
    bCh5_S1_FaultLatched := FALSE; bCh5_S2_FaultLatched := FALSE; bCh5_S3_FaultLatched := FALSE;
    bCh6_S1_FaultLatched := FALSE; bCh6_S2_FaultLatched := FALSE; bCh6_S3_FaultLatched := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.3: SAFETY INTERLOCK ENFORCEMENT & ACTUATOR TRIPPING                                     *)
(* ---------------------------------------------------------------------------------------------- *)
IF bAlarmHighHigh OR NOT bEmergencyStop THEN
    bRunoffPumpRun := FALSE;
    bRecircPumpRun := FALSE;
    bCalandriaCircPumpRun := FALSE;
    bSpentGrainDischargeDoorOpen := FALSE;
    bHopDoserValve1 := FALSE;
    bHopDoserValve2 := FALSE;
    bCIPSupplyValveOpen := FALSE;
    bVaporCondenserPumpRun := FALSE;

    fRunoffValveCommand := 0.0;
    fRecircValveCommand := 0.0;
    fCalandriaSteamValveCommand := 0.0;
    fSpargeValveCommand := 0.0;
    fWhirlpoolPumpCommand := 0.0;
    fRakeSpeedCommand := 0.0;
    (* Maintain Rake Elevation Safe Park Clearance *)
    fRakeHeightCommand := 350.0;

    bActive := FALSE;
    bError := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 5.4: 32-BIT BIT-PACKED STATUS & ALARM TELEMETRY WORD ENCODING                             *)
(* ---------------------------------------------------------------------------------------------- *)

(* Status Word 1: Operational States, Sub-Steps & Master Permissives *)
(* Bits 0-3: Current FSM State (0 to 13) *)
dwStatusWord1 := INT_TO_DWORD(eState AND 16#0F);
(* Bits 4-7: Current Sub-Step (0 to 15) *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(iSubStep AND 16#0F), 4);
(* Bit 8: Master Block Ready *)
IF bReady THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
(* Bit 9: Master Block Active *)
IF bActive THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
(* Bit 10: Automatic Control Mode *)
IF bAutoMode THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
(* Bit 11: Emergency Stop Ok *)
IF bEmergencyStop THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
(* Bit 12: General Error Latched *)
IF bError THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
(* Bit 13: High-High Common Alarm Active *)
IF bAlarmHighHigh THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
(* Bit 14: Deep Cut In Progress *)
IF eState = 7 THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
(* Bit 15: Vigorous Boil In Progress *)
IF eState = 11 THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
(* Bit 16: Whirlpool Rest In Progress *)
IF eState = 12 THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF;
(* Bit 17: CIP Loop Active *)
IF eState = 13 THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF;

(* Status Word 2: Actuator Runtime Status & 2oo3 TMR Degradation Masks *)
dwStatusWord2 := 16#00000000;
IF bRunoffPumpRun THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bRecircPumpRun THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bCalandriaCircPumpRun THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF bSpentGrainDischargeDoorOpen THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;
IF bHopDoserValve1 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bHopDoserValve2 THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bCIPSupplyValveOpen THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF bVaporCondenserPumpRun THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;

(* TMR Sensor Health Degradation Bits *)
IF bAlarmTMR_DP_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bAlarmTMR_Turb_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bAlarmTMR_Temp_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF bAlarmTMR_Level_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;
IF bAlarmTMR_SteamP_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bAlarmTMR_Flow_Degraded THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bBedChokeDetected THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF bCalandriaFoulingAlarm THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;

(* Alarm Word 1: ISA-18.2 Priority 1 Critical Trips (High-High & Low-Low) *)
dwAlarmWord1 := 16#00000000;
IF bAlarmDP_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bAlarmTurb_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bAlarmTemp_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bAlarmTemp_LL_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bAlarmSteamP_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bAlarmLevel_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF bAlarmTorque_HH_Active THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF bAlarmEmergencyStopActive THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF (iCh1_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;
IF (iCh2_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF;
IF (iCh3_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF;
IF (iCh4_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF;
IF (iCh5_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF;
IF (iCh6_HealthySensors = 0) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF;

(* Alarm Word 2: ISA-18.2 Priority 2 Warning Process Deviations (High & Low) *)
dwAlarmWord2 := 16#00000000;
IF bAlarmDP_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bAlarmTurb_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bAlarmTemp_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bAlarmSteamP_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bAlarmTorque_H_Active THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF bBedChokeDetected THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bCalandriaFoulingAlarm THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bDegradedTMRMode THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;

(* First-Out Telemetry Output Word *)
dwFirstOutWord := dwFirstOutCode;

END_FUNCTION_BLOCK
"""
