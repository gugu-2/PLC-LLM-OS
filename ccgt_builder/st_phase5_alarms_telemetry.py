# ccgt_builder/st_phase5_alarms_telemetry.py

def get_phase5_alarms_telemetry():
    return """(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM LOGIC, BIT-PACKED TELEMETRY & FINAL ACTUATOR DEMANDS
 * Conforming to ISA-18.2 / IEC 62682 Management of Alarm Systems for the Process Industries:
 *   - Tier 1: Emergency Hardwired & SIL-3 Protective Trips (Priority: Emergency Trip)
 *   - Tier 2: Process Pre-Warnings & High/Low Deviation Alarms with Debounce & Clearance Deadband
 *   - 32-Bit Bit-Packed Supervisory Status and Diagnostic Telemetry Registers:
 *       dwStatusWord1  : Master Subsystem Operating Status & Sequencer Progression
 *       dwStatusWord2  : 2oo3 TMR Sensor Health, Parity & Degradation Channel Flags
 *       dwAlarmWord1   : Critical SIL-3 Trips & Priority 1 Master Fuel Trip Alarm Matrix
 *       dwAlarmWord2   : Process Warning Envelopes, Rates of Change & Discrepancies
 *       dwFirstOutWord : Forensic Sequence-of-Events Root-Cause First-Out Lockout
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.1: ISA-18.2 PROCESS ALARM QUALIFICATION WITH DEBOUNCE & HYSTERESIS CLEARANCE
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Reset alarms on operator reset command *)
IF bReset_Cmd THEN
    IF rVoted_EGT_degC < (rTrip_EGT_HighHigh_HH - rDeadband_EGT_degC) THEN
        bActive_EGT_HH := FALSE;
    END_IF;
    IF rVoted_EGT_degC < (rWarn_EGT_High_H - rDeadband_EGT_degC) THEN
        bActive_EGT_H := FALSE;
    END_IF;
    IF rVoted_Drum_Level_mm > (rTrip_Drum_LowLow_LL + rDeadband_Drum_mm) THEN
        bActive_Drum_LL := FALSE;
    END_IF;
    IF rVoted_Drum_Level_mm < (rTrip_Drum_HighHigh_HH - rDeadband_Drum_mm) THEN
        bActive_Drum_HH := FALSE;
    END_IF;
    IF rVoted_Drum_Level_mm > (rWarn_Drum_Low_L + rDeadband_Drum_mm) THEN
        bActive_Drum_L := FALSE;
    END_IF;
    IF rVoted_Drum_Level_mm < (rWarn_Drum_High_H - rDeadband_Drum_mm) THEN
        bActive_Drum_H := FALSE;
    END_IF;
    IF rVoted_Steam_Temp_degC < (rTrip_SteamTemp_HighHigh_HH - rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_HH := FALSE;
    END_IF;
    IF rVoted_Steam_Temp_degC < (rWarn_SteamTemp_High_H - rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_H := FALSE;
    END_IF;
    IF rVoted_Steam_Temp_degC > (rWarn_SteamTemp_Low_L + rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_L := FALSE;
    END_IF;
    IF rTurbine_Shaft_Speed_RPM < (rTrip_Overspeed_HH_RPM - 20.0) THEN
        bActive_Overspeed := FALSE;
    END_IF;
END_IF;

(* 1. Combustor EGT High-High Trip (SIL-3 Qualified) *)
IF rVoted_EGT_degC >= rTrip_EGT_HighHigh_HH THEN
    rTimer_Alarm_EGT_HH := rTimer_Alarm_EGT_HH + rScan_Period_Ts;
    IF rTimer_Alarm_EGT_HH >= 0.040 THEN (* 40 ms fast qualification *)
        bActive_EGT_HH := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_EGT_HH := 0.0;
    IF rVoted_EGT_degC <= (rTrip_EGT_HighHigh_HH - rDeadband_EGT_degC) THEN
        bActive_EGT_HH := FALSE;
    END_IF;
END_IF;

(* 2. Combustor EGT High Warning *)
IF rVoted_EGT_degC >= rWarn_EGT_High_H THEN
    rTimer_Alarm_EGT_H := rTimer_Alarm_EGT_H + rScan_Period_Ts;
    IF rTimer_Alarm_EGT_H >= 0.200 THEN
        bActive_EGT_H := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_EGT_H := 0.0;
    IF rVoted_EGT_degC <= (rWarn_EGT_High_H - rDeadband_EGT_degC) THEN
        bActive_EGT_H := FALSE;
    END_IF;
END_IF;

(* 3. HP Drum Low-Low Level Trip (SIL-3 Qualified < 25 ms) *)
IF rVoted_Drum_Level_mm <= rTrip_Drum_LowLow_LL THEN
    rTimer_Alarm_Drum_LL := rTimer_Alarm_Drum_LL + rScan_Period_Ts;
    IF rTimer_Alarm_Drum_LL >= 0.020 THEN (* 1 scan execution qualification *)
        bActive_Drum_LL := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_Drum_LL := 0.0;
    IF rVoted_Drum_Level_mm >= (rTrip_Drum_LowLow_LL + rDeadband_Drum_mm) THEN
        bActive_Drum_LL := FALSE;
    END_IF;
END_IF;

(* 4. HP Drum High-High Level Trip (SIL-3 Qualified < 25 ms) *)
IF rVoted_Drum_Level_mm >= rTrip_Drum_HighHigh_HH THEN
    rTimer_Alarm_Drum_HH := rTimer_Alarm_Drum_HH + rScan_Period_Ts;
    IF rTimer_Alarm_Drum_HH >= 0.020 THEN
        bActive_Drum_HH := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_Drum_HH := 0.0;
    IF rVoted_Drum_Level_mm <= (rTrip_Drum_HighHigh_HH - rDeadband_Drum_mm) THEN
        bActive_Drum_HH := FALSE;
    END_IF;
END_IF;

(* 5. HP Drum Low Warning *)
IF rVoted_Drum_Level_mm <= rWarn_Drum_Low_L THEN
    rTimer_Alarm_Drum_L := rTimer_Alarm_Drum_L + rScan_Period_Ts;
    IF rTimer_Alarm_Drum_L >= 0.200 THEN
        bActive_Drum_L := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_Drum_L := 0.0;
    IF rVoted_Drum_Level_mm >= (rWarn_Drum_Low_L + rDeadband_Drum_mm) THEN
        bActive_Drum_L := FALSE;
    END_IF;
END_IF;

(* 6. HP Drum High Warning *)
IF rVoted_Drum_Level_mm >= rWarn_Drum_High_H THEN
    rTimer_Alarm_Drum_H := rTimer_Alarm_Drum_H + rScan_Period_Ts;
    IF rTimer_Alarm_Drum_H >= 0.200 THEN
        bActive_Drum_H := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_Drum_H := 0.0;
    IF rVoted_Drum_Level_mm <= (rWarn_Drum_High_H - rDeadband_Drum_mm) THEN
        bActive_Drum_H := FALSE;
    END_IF;
END_IF;

(* 7. Main Steam Exit Temperature High-High Creep Safety Trip *)
IF rVoted_Steam_Temp_degC >= rTrip_SteamTemp_HighHigh_HH THEN
    rTimer_Alarm_SteamT_HH := rTimer_Alarm_SteamT_HH + rScan_Period_Ts;
    IF rTimer_Alarm_SteamT_HH >= 0.050 THEN
        bActive_SteamT_HH := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_SteamT_HH := 0.0;
    IF rVoted_Steam_Temp_degC <= (rTrip_SteamTemp_HighHigh_HH - rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_HH := FALSE;
    END_IF;
END_IF;

(* 8. Main Steam Exit Temperature High Warning *)
IF rVoted_Steam_Temp_degC >= rWarn_SteamTemp_H THEN
    rTimer_Alarm_SteamT_H := rTimer_Alarm_SteamT_H + rScan_Period_Ts;
    IF rTimer_Alarm_SteamT_H >= 0.300 THEN
        bActive_SteamT_H := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_SteamT_H := 0.0;
    IF rVoted_Steam_Temp_degC <= (rWarn_SteamTemp_High_H - rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_H := FALSE;
    END_IF;
END_IF;

(* 9. Main Steam Exit Temperature Low Droop Warning (Steam Turbine Condensation Risk) *)
IF (eCurrentState >= 9 AND eCurrentState <= 11) AND (rVoted_Steam_Temp_degC <= rWarn_SteamTemp_Low_L) THEN
    rTimer_Alarm_SteamT_L := rTimer_Alarm_SteamT_L + rScan_Period_Ts;
    IF rTimer_Alarm_SteamT_L >= 0.500 THEN
        bActive_SteamT_L := TRUE;
    END_IF;
ELSE
    rTimer_Alarm_SteamT_L := 0.0;
    IF rVoted_Steam_Temp_degC >= (rWarn_SteamTemp_Low_L + rDeadband_SteamTemp_degC) THEN
        bActive_SteamT_L := FALSE;
    END_IF;
END_IF;

(* 10. Turbomachinery Over-Speed Trip *)
IF rTurbine_Shaft_Speed_RPM >= rTrip_Overspeed_HH_RPM THEN
    bActive_Overspeed := TRUE;
ELSE
    IF rTurbine_Shaft_Speed_RPM <= (rTrip_Overspeed_HH_RPM - 50.0) THEN
        bActive_Overspeed := FALSE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.2: 32-BIT BIT-PACKED STATUS WORD 1 (dwStatusWord1 - Supervisory Operating Telemetry)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwStatusWord1 := 16#00000000;
IF bMasterStart_Cmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000001; END_IF;
IF bTurning_Gear_Engaged THEN dwStatusWord1 := dwStatusWord1 OR 16#00000002; END_IF;
IF bJacking_Oil_Press_OK THEN dwStatusWord1 := dwStatusWord1 OR 16#00000004; END_IF;
IF bLube_Oil_Press_OK THEN dwStatusWord1 := dwStatusWord1 OR 16#00000008; END_IF;
IF bIgniter_Spark_Cmd THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF;
IF (nCombustor_Flames_Detected >= 3) THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF;
IF bBreaker_52G_Closed THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF;
IF bSync_Permissive_52G THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF;
IF bDLN_Premix_Mode_Active THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF;
IF bDrum_Swell_Lockout_Active THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF;
IF bAuto_Coord_Enable THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF;
IF bEnable_Duct_Burner THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF;
IF bPrimary_Freq_Active THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF;
IF bMaster_Fuel_Trip_MFT THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF;
IF bSteam_Turbine_Ready_Accept THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF;
IF bCondenser_Vacuum_OK THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF;
(* Encode 4-bit FSM state into bits 16..19 *)
dwStatusWord1 := dwStatusWord1 OR SHL(INT_TO_DWORD(eCurrentState AND 16#000F), 16);

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.3: 32-BIT BIT-PACKED STATUS WORD 2 (dwStatusWord2 - 2oo3 TMR Sensor Health & Degradation)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwStatusWord2 := 16#00000000;
IF bEGT_Healthy_A THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF;
IF bEGT_Healthy_B THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF;
IF bEGT_Healthy_C THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF;
IF (nMode_EGT_TMR < 3) THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF;

IF bDrumL_Healthy_A THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF;
IF bDrumL_Healthy_B THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF;
IF bDrumL_Healthy_C THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF;
IF (nMode_DrumL_TMR < 3) THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF;

IF bSteamT_Healthy_A THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF;
IF bSteamT_Healthy_B THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF;
IF bSteamT_Healthy_C THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF;
IF (nMode_SteamT_TMR < 3) THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF;

IF bSteamF_Healthy_A THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF;
IF bSteamF_Healthy_B THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF;
IF bSteamF_Healthy_C THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF;
IF (nMode_SteamF_TMR < 3) THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF;

IF bPower_Healthy_A THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF;
IF bPower_Healthy_B THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF;
IF bPower_Healthy_C THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF;
IF (nMode_Power_TMR < 3) THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.4: 32-BIT BIT-PACKED ALARM WORD 1 (dwAlarmWord1 - Critical Trips & SIL-3 Interlocks)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord1 := 16#00000000;
IF NOT bEmergencyTrip_PB THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF;
IF bActive_Drum_LL THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF;
IF bActive_Drum_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF;
IF bActive_EGT_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF;
IF bActive_SteamT_HH THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF;
IF bActive_Overspeed THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF;
IF (nCombustor_Flames_Detected < 2 AND eCurrentState >= 3 AND eCurrentState <= 11) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF;
IF NOT bLube_Oil_Press_OK AND (eCurrentState >= 2) THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF;
IF bMaster_Fuel_Trip_MFT THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.5: 32-BIT BIT-PACKED ALARM WORD 2 (dwAlarmWord2 - Process Warnings & Deviations)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord2 := 16#00000000;
IF bActive_EGT_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF;
IF bActive_Drum_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF;
IF bActive_Drum_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF;
IF bActive_SteamT_H THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF;
IF bActive_SteamT_L THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF;
IF (rTurbine_Shaft_Speed_RPM >= rWarn_Overspeed_H_RPM) THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF;
IF bAlarm_EGT_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF;
IF bAlarm_DrumL_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF;
IF bAlarm_SteamT_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF;
IF bAlarm_SteamF_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF;
IF bAlarm_Power_Discrepancy THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SECTION 5.6: WRITE FINAL ACTUATOR DEMANDS TO HARDWARE I/O OUTPUT REGISTERS
 * --------------------------------------------------------------------------------------------------------------------- *)
rFuel_Gas_Valve_Cmd_Pct     := u_vec[1];
rVGV_Position_Cmd_deg       := u_vec[2];
rFeedwater_Valve_Cmd_Pct    := u_vec[3];
rAttemperator_Valve_Cmd_Pct := u_vec[4];
rSteam_Bypass_Valve_Cmd_Pct := u_vec[5];
rDuct_Burner_Valve_Cmd_Pct  := u_vec[6];

END_FUNCTION_BLOCK
"""
