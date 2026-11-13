# ammonia_refrigeration_builder/build_st_phases_7_to_10.py

def get_phases_7_to_10():
    return """(* ==================================================================================================================== *)
(* PHASE 5: MULTI-ZONE REVERSE HOT-GAS DEFROST COORDINATION & INTERLOCK ENGINE                                          *)
(* ==================================================================================================================== *)

(* Prevent simultaneous defrost of multiple zones to maintain rack suction balance & avoid flash boil carryover *)
IF iDefrostZoneActive = 0 THEN
    IF bZone1_DefrostRequest THEN
        iDefrostZoneActive := 1;
    ELSIF bZone2_DefrostRequest THEN
        iDefrostZoneActive := 2;
    ELSIF bZone3_DefrostRequest THEN
        iDefrostZoneActive := 3;
    ELSIF bZone4_DefrostRequest THEN
        iDefrostZoneActive := 4;
    END_IF;
END_IF;

(* Track Zone Defrost Elapsed Timers *)
IF iDefrostZoneActive = 1 THEN
    rDefrostTimer_Zone1 := rDefrostTimer_Zone1 + rCycleTime_dt_sec;
ELSE
    rDefrostTimer_Zone1 := 0.0;
END_IF;

IF iDefrostZoneActive = 2 THEN
    rDefrostTimer_Zone2 := rDefrostTimer_Zone2 + rCycleTime_dt_sec;
ELSE
    rDefrostTimer_Zone2 := 0.0;
END_IF;

IF iDefrostZoneActive = 3 THEN
    rDefrostTimer_Zone3 := rDefrostTimer_Zone3 + rCycleTime_dt_sec;
ELSE
    rDefrostTimer_Zone3 := 0.0;
END_IF;

IF iDefrostZoneActive = 4 THEN
    rDefrostTimer_Zone4 := rDefrostTimer_Zone4 + rCycleTime_dt_sec;
ELSE
    rDefrostTimer_Zone4 := 0.0;
END_IF;

(* ==================================================================================================================== *)
(* PHASE 6: ISA-18.2 MULTI-TIERED ALARM ENGINE WITH DEADBAND HYSTERESIS & FIRST-OUT CAPTURE                             *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.1: SUCTION HEADER PRESSURE MULTI-TIER ALARMS (PT-101)                                                              *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* High-High Trip (4.80 bar) *)
IF rVoted_SuctionPressure_bar >= rAlarmTrip_Suction_HH_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000080;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000080;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_SuctionPressure_bar <= (rAlarmTrip_Suction_HH_bar - rAlarmDeadband_Suction_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000080;
    END_IF;
END_IF;

(* Low-Low Vacuum Trip (0.85 bar) *)
IF rVoted_SuctionPressure_bar <= rAlarmTrip_Suction_LL_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000040;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000040;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_SuctionPressure_bar >= (rAlarmTrip_Suction_LL_bar + rAlarmDeadband_Suction_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000040;
    END_IF;
END_IF;

(* High Warning (3.80 bar) *)
IF rVoted_SuctionPressure_bar >= rAlarmTrip_Suction_H_bar THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000001;
ELSIF rVoted_SuctionPressure_bar <= (rAlarmTrip_Suction_H_bar - rAlarmDeadband_Suction_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000001;
END_IF;

(* Low Warning (1.25 bar) *)
IF rVoted_SuctionPressure_bar <= rAlarmTrip_Suction_L_bar THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000002;
ELSIF rVoted_SuctionPressure_bar >= (rAlarmTrip_Suction_L_bar + rAlarmDeadband_Suction_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000002;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.2: CONDENSER DISCHARGE PRESSURE MULTI-TIER ALARMS (PT-601)                                                         *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* High-High Overpressure Trip (16.50 bar) *)
IF rVoted_CondenserPressure_bar >= rAlarmTrip_DischPress_HH_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000100;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000100;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_CondenserPressure_bar <= (rAlarmTrip_DischPress_HH_bar - rAlarmDeadband_DischPress_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000100;
    END_IF;
END_IF;

(* Low-Low Pressure Trip (6.80 bar) *)
IF rVoted_CondenserPressure_bar <= rAlarmTrip_DischPress_LL_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000200;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000200;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_CondenserPressure_bar >= (rAlarmTrip_DischPress_LL_bar + rAlarmDeadband_DischPress_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000200;
    END_IF;
END_IF;

(* High Warning (14.50 bar) *)
IF rVoted_CondenserPressure_bar >= rAlarmTrip_DischPress_H_bar THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000004;
ELSIF rVoted_CondenserPressure_bar <= (rAlarmTrip_DischPress_H_bar - rAlarmDeadband_DischPress_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000004;
END_IF;

(* Low Warning (8.20 bar) *)
IF rVoted_CondenserPressure_bar <= rAlarmTrip_DischPress_L_bar THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000008;
ELSIF rVoted_CondenserPressure_bar >= (rAlarmTrip_DischPress_L_bar + rAlarmDeadband_DischPress_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000008;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.3: COMPRESSOR DISCHARGE TEMPERATURE MULTI-TIER ALARMS (TT-201)                                                     *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* High-High Trip (115.0 deg C) *)
IF rVoted_DischargeTemp_degC >= rAlarmTrip_DischTemp_HH_degC THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000400;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000400;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_DischargeTemp_degC <= (rAlarmTrip_DischTemp_HH_degC - rAlarmDeadband_DischTemp_degC) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000400;
    END_IF;
END_IF;

(* High Warning (102.0 deg C) *)
IF rVoted_DischargeTemp_degC >= rAlarmTrip_DischTemp_H_degC THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000010;
ELSIF rVoted_DischargeTemp_degC <= (rAlarmTrip_DischTemp_H_degC - rAlarmDeadband_DischTemp_degC) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000010;
END_IF;

(* Low Warning (45.0 deg C) *)
IF rVoted_DischargeTemp_degC <= rAlarmTrip_DischTemp_L_degC THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000020;
ELSIF rVoted_DischargeTemp_degC >= (rAlarmTrip_DischTemp_L_degC + rAlarmDeadband_DischTemp_degC) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000020;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.4: LUBRICATING OIL DIFFERENTIAL PRESSURE MULTI-TIER ALARMS (PDT-301)                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Low-Low Trip (1.50 bar) *)
IF (iFSM_State >= FSM_STATE_LEAD_COMP_SOFT_START) AND (rVoted_OilDiffPressure_bar <= rAlarmTrip_OilDP_LL_bar) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000800;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00000800;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_OilDiffPressure_bar >= (rAlarmTrip_OilDP_LL_bar + rAlarmDeadband_OilDP_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00000800;
    END_IF;
END_IF;

(* Low Warning (2.00 bar) *)
IF (iFSM_State >= FSM_STATE_LEAD_COMP_SOFT_START) AND (rVoted_OilDiffPressure_bar <= rAlarmTrip_OilDP_L_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000040;
ELSIF rVoted_OilDiffPressure_bar >= (rAlarmTrip_OilDP_L_bar + rAlarmDeadband_OilDP_bar) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000040;
END_IF;

(* High Differential Filter Plugged Trip (5.20 bar) *)
IF rVoted_OilDiffPressure_bar >= rAlarmTrip_OilDP_HH_bar THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00001000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00001000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_OilDiffPressure_bar <= (rAlarmTrip_OilDP_HH_bar - rAlarmDeadband_OilDP_bar) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00001000;
    END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.5: OIL SUMP TEMPERATURE MULTI-TIER ALARMS (TT-302)                                                                 *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* High-High Trip (72.0 deg C) *)
IF TT_OIL_SEPARATOR_SUMP >= rAlarmTrip_OilTemp_HH_degC THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00002000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00002000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF TT_OIL_SEPARATOR_SUMP <= (rAlarmTrip_OilTemp_HH_degC - rAlarmDeadband_OilTemp_degC) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00002000;
    END_IF;
END_IF;

(* High Warning (62.0 deg C) *)
IF TT_OIL_SEPARATOR_SUMP >= rAlarmTrip_OilTemp_H_degC THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000080;
ELSIF TT_OIL_SEPARATOR_SUMP <= (rAlarmTrip_OilTemp_H_degC - rAlarmDeadband_OilTemp_degC) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000080;
END_IF;

(* Low Warning (32.0 deg C) *)
IF TT_OIL_SEPARATOR_SUMP <= rAlarmTrip_OilTemp_L_degC THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000100;
ELSIF TT_OIL_SEPARATOR_SUMP >= (rAlarmTrip_OilTemp_L_degC + rAlarmDeadband_OilTemp_degC) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000100;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.6: AMMONIA AMBIENT GAS MULTI-TIER ALARMS (AT-401)                                                                  *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Critical Scrubber Trip (300.0 ppm) *)
IF rVoted_AmbientNH3_ppm >= rAlarmTrip_NH3_Critical_ppm THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00004000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00004000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF rVoted_AmbientNH3_ppm <= (rAlarmTrip_NH3_Critical_ppm - rAlarmDeadband_NH3_ppm) THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00004000;
    END_IF;
END_IF;

(* Warning (50.0 ppm) *)
IF rVoted_AmbientNH3_ppm >= rAlarmTrip_NH3_Warning_ppm THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000200;
ELSIF rVoted_AmbientNH3_ppm <= (rAlarmTrip_NH3_Warning_ppm - rAlarmDeadband_NH3_ppm) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000200;
END_IF;

(* Alert (25.0 ppm) *)
IF rVoted_AmbientNH3_ppm >= rAlarmTrip_NH3_Alert_ppm THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000400;
ELSIF rVoted_AmbientNH3_ppm <= (rAlarmTrip_NH3_Alert_ppm - rAlarmDeadband_NH3_ppm) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000400;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 6.7: VESSEL LIQUID LEVEL & COALESCER FILTER ALARMS                                                                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
(* Suction Accumulator High-High Level Slugging Trip (80.0%) *)
IF LT_SUCTION_ACCUMULATOR_LEVEL >= 80.0 THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00008000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00008000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF LT_SUCTION_ACCUMULATOR_LEVEL <= 70.0 THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00008000;
    END_IF;
END_IF;

(* Suction Accumulator High Warning (65.0%) *)
IF LT_SUCTION_ACCUMULATOR_LEVEL >= 65.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000800;
ELSIF LT_SUCTION_ACCUMULATOR_LEVEL <= 55.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00000800;
END_IF;

(* Oil Separator Low Level Trip (20.0%) *)
IF LT_OIL_SEPARATOR_LEVEL <= 20.0 THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00010000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00010000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF LT_OIL_SEPARATOR_LEVEL >= 30.0 THEN
    IF bAcknowledgeFaultReset THEN
        dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00010000;
    END_IF;
END_IF;

(* Oil Separator Low Level Warning (35.0%) *)
IF LT_OIL_SEPARATOR_LEVEL <= 35.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00001000;
ELSIF LT_OIL_SEPARATOR_LEVEL >= 45.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00001000;
END_IF;

(* Coalescer Filter High DP Warning (0.80 bar) *)
IF PDT_OIL_COALESCER_FILTER >= 0.80 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00002000;
ELSIF PDT_OIL_COALESCER_FILTER <= 0.60 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning AND NOT 16#00002000;
END_IF;

(* E-Stop Trip Assertion *)
IF NOT bEmergencyStopCircuit_NC THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00020000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00020000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF bAcknowledgeFaultReset THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00020000;
END_IF;

(* Fire Alarm Assertion *)
IF NOT bMachineryRoomFireAlarm_NC THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00040000;
    IF NOT bFirstOutLatched THEN
        dwFirstOut_Alarm := 16#00040000;
        bFirstOutLatched := TRUE;
    END_IF;
ELSIF bAcknowledgeFaultReset THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#00040000;
END_IF;

(* Clear First-Out Register on Operator Fault Reset *)
IF bAcknowledgeFaultReset AND (dwAlarmWord_Critical = 16#00000000) THEN
    bFirstOutLatched := FALSE;
    dwFirstOut_Alarm := 16#00000000;
END_IF;

(* ==================================================================================================================== *)
(* PHASE 7: 32-BIT BIT-PACKED STATUS, INTERLOCK & TELEMETRY WORD ENCODING                                               *)
(* ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 7.1: GENERAL STATUS WORD (dwStatusWord_General)                                                                      *)
(* -------------------------------------------------------------------------------------------------------------------- *)
dwStatusWord_General := 16#00000000;
IF bMasterSystemEnable THEN dwStatusWord_General := dwStatusWord_General OR 16#00000001; END_IF;
IF bAutomaticModeSelect THEN dwStatusWord_General := dwStatusWord_General OR 16#00000002; END_IF;
IF bComp1_RunningFeedback THEN dwStatusWord_General := dwStatusWord_General OR 16#00000004; END_IF;
IF bComp2_RunningFeedback THEN dwStatusWord_General := dwStatusWord_General OR 16#00000008; END_IF;
IF bComp3_RunningFeedback THEN dwStatusWord_General := dwStatusWord_General OR 16#00000010; END_IF;
IF bPreLubeOilPump_Command THEN dwStatusWord_General := dwStatusWord_General OR 16#00000020; END_IF;
IF (rEconomizer_EEV_Opening_Pct > 5.0) THEN dwStatusWord_General := dwStatusWord_General OR 16#00000040; END_IF;
IF bCondenser_SprayPump1_Command THEN dwStatusWord_General := dwStatusWord_General OR 16#00000080; END_IF;
IF bCondenser_SprayPump2_Command THEN dwStatusWord_General := dwStatusWord_General OR 16#00000100; END_IF;
IF (iDefrostZoneActive > 0) THEN dwStatusWord_General := dwStatusWord_General OR 16#00000200; END_IF;
IF (iDefrostZoneActive = 1) THEN dwStatusWord_General := dwStatusWord_General OR 16#00000400; END_IF;
IF (iDefrostZoneActive = 2) THEN dwStatusWord_General := dwStatusWord_General OR 16#00000800; END_IF;
IF (iDefrostZoneActive = 3) THEN dwStatusWord_General := dwStatusWord_General OR 16#00001000; END_IF;
IF (iDefrostZoneActive = 4) THEN dwStatusWord_General := dwStatusWord_General OR 16#00002000; END_IF;
IF bEmergencyVentilationFan1 OR bEmergencyVentilationFan2 THEN dwStatusWord_General := dwStatusWord_General OR 16#00004000; END_IF;
IF (dwAlarmWord_Warning <> 16#00000000) THEN dwStatusWord_General := dwStatusWord_General OR 16#00008000; END_IF;
IF (dwAlarmWord_Critical <> 16#00000000) THEN dwStatusWord_General := dwStatusWord_General OR 16#00010000; END_IF;
IF (rOilSumpHeater_DutyCycle_Pct > 0.0) THEN dwStatusWord_General := dwStatusWord_General OR 16#00020000; END_IF;

(* Encode current FSM state in upper nibbles (Bits 24..27) *)
dwStatusWord_General := dwStatusWord_General OR SHL(INT_TO_DWORD(iFSM_State), 24);

(* -------------------------------------------------------------------------------------------------------------------- *)
(* 7.2: HARDWARE INTERLOCK STATUS WORD (dwInterlockWord)                                                                *)
(* -------------------------------------------------------------------------------------------------------------------- *)
dwInterlockWord := 16#00000000;
IF bMasterSystemEnable THEN dwInterlockWord := dwInterlockWord OR 16#00000001; END_IF;
IF bEmergencyStopCircuit_NC THEN dwInterlockWord := dwInterlockWord OR 16#00000002; END_IF;
IF bMachineryRoomFireAlarm_NC THEN dwInterlockWord := dwInterlockWord OR 16#00000004; END_IF;
IF bAutomaticModeSelect THEN dwInterlockWord := dwInterlockWord OR 16#00000008; END_IF;
IF bEconomizerSubcoolingPermissive THEN dwInterlockWord := dwInterlockWord OR 16#00000010; END_IF;
IF bCondenserWaterSumpHeaterPermissive THEN dwInterlockWord := dwInterlockWord OR 16#00000020; END_IF;
IF bComp1_RunningFeedback THEN dwInterlockWord := dwInterlockWord OR 16#00000040; END_IF;
IF bComp2_RunningFeedback THEN dwInterlockWord := dwInterlockWord OR 16#00000080; END_IF;
IF bComp3_RunningFeedback THEN dwInterlockWord := dwInterlockWord OR 16#00000100; END_IF;
IF bEmergencyLiquidLineKingValveShut THEN dwInterlockWord := dwInterlockWord OR 16#00000200; END_IF;
IF (rComp1_AntiRecycleTimer_sec <= 0.0) THEN dwInterlockWord := dwInterlockWord OR 16#00000400; END_IF;
IF (rComp2_AntiRecycleTimer_sec <= 0.0) THEN dwInterlockWord := dwInterlockWord OR 16#00000800; END_IF;
IF (rComp3_AntiRecycleTimer_sec <= 0.0) THEN dwInterlockWord := dwInterlockWord OR 16#00001000; END_IF;

(* ==================================================================================================================== *)
(* PHASE 8: ACTUATOR COMMAND CLAMPING, OIL COOLER REGULATION & FAIL-SAFE SHUTDOWN                                       *)
(* ==================================================================================================================== *)

(* Modulate Oil Cooler 3-Way Thermostatic Mixing Valve to maintain 48.0 deg C target *)
rOilCooler3WayValve_Command_Pct := vecU[6];
IF TT_OIL_SEPARATOR_SUMP >= 58.0 THEN
    rOilCooler3WayValve_Command_Pct := 100.0; (* Full flow through cooler *)
ELSIF TT_OIL_SEPARATOR_SUMP <= 40.0 THEN
    rOilCooler3WayValve_Command_Pct := 0.0;   (* Full bypass around cooler *)
END_IF;

(* Enforce Fail-Safe Output De-assertion if Critical Alarm or Emergency Stop Active *)
IF (dwAlarmWord_Critical <> 16#00000000) OR (iFSM_State = FSM_STATE_EMERGENCY_VENT_SCRUB) THEN
    rComp1_VFD_SpeedCommand_Hz := 0.0;
    rComp1_SlideValve_Command_Pct := 0.0;
    rComp2_SlideValve_Command_Pct := 0.0;
    rComp3_SlideValve_Command_Pct := 0.0;
    bComp1_StartCommand := FALSE;
    bComp2_StartCommand := FALSE;
    bComp3_StartCommand := FALSE;
    rEconomizer_EEV_Opening_Pct := 0.0;
    rOilSumpHeater_DutyCycle_Pct := 0.0;
    bEmergencyLiquidLineKingValveShut := TRUE;
    bEmergencyVentilationFan1 := TRUE;
    bEmergencyVentilationFan2 := TRUE;
    bEmergencyScrubberCircPump := TRUE;
    bAudibleVisualHornStrobeAlarm := TRUE;
END_IF;

END_FUNCTION_BLOCK
"""
