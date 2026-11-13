# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_alarms.py
Implements Phase 5: ISA-18.2 Multi-Tier Alarms (HH, H, L, LL with Hysteresis Deadbands),
Latching/Acknowledgment Engine, Bit-Packed Telemetry DWORDs, and END_FUNCTION_BLOCK.
"""

def generate_alarms():
    return '''(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS & BIT-PACKED TELEMETRY DWORDS
 * Multi-tier alarm trips (HH, H, L, LL) with deadband hysteresis, first-out capture, and bit-packed telemetry words.
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 1. CELL VOLTAGE MULTI-TIER ALARMS (HH, H, L, LL)
 * Nominal: 4.15 V, Deadband Hysteresis: 0.040 V
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Alarm: 4.80 V *)
IF rPot_VotedCellVoltage_V >= c_Volt_Trip_HH THEN
    bAlm_Volt_HH_Raw := TRUE;
ELSIF rPot_VotedCellVoltage_V <= (c_Volt_Trip_HH - c_Volt_Hysteresis) THEN
    bAlm_Volt_HH_Raw := FALSE;
END_IF;

(* High Alarm: 4.45 V *)
IF rPot_VotedCellVoltage_V >= c_Volt_Trip_H THEN
    bAlm_Volt_H_Raw := TRUE;
ELSIF rPot_VotedCellVoltage_V <= (c_Volt_Trip_H - c_Volt_Hysteresis) THEN
    bAlm_Volt_H_Raw := FALSE;
END_IF;

(* Low Alarm: 3.85 V *)
IF rPot_VotedCellVoltage_V <= c_Volt_Trip_L THEN
    bAlm_Volt_L_Raw := TRUE;
ELSIF rPot_VotedCellVoltage_V >= (c_Volt_Trip_L + c_Volt_Hysteresis) THEN
    bAlm_Volt_L_Raw := FALSE;
END_IF;

(* Low-Low Alarm: 3.60 V (Imminent Short Circuit) *)
IF rPot_VotedCellVoltage_V <= c_Volt_Trip_LL THEN
    bAlm_Volt_LL_Raw := TRUE;
ELSIF rPot_VotedCellVoltage_V >= (c_Volt_Trip_LL + c_Volt_Hysteresis) THEN
    bAlm_Volt_LL_Raw := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 2. POT PSEUDO-RESISTANCE MULTI-TIER ALARMS (HH, H, L, LL)
 * Nominal: 5.00 uOhm, Deadband Hysteresis: 0.075 uOhm
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Alarm: 6.80 uOhm *)
IF rPot_FilteredResistance_uOhm >= c_Res_Trip_HH THEN
    bAlm_Res_HH_Raw := TRUE;
ELSIF rPot_FilteredResistance_uOhm <= (c_Res_Trip_HH - c_Res_Hysteresis) THEN
    bAlm_Res_HH_Raw := FALSE;
END_IF;

(* High Alarm: 5.80 uOhm *)
IF rPot_FilteredResistance_uOhm >= c_Res_Trip_H THEN
    bAlm_Res_H_Raw := TRUE;
ELSIF rPot_FilteredResistance_uOhm <= (c_Res_Trip_H - c_Res_Hysteresis) THEN
    bAlm_Res_H_Raw := FALSE;
END_IF;

(* Low Alarm: 4.40 uOhm *)
IF rPot_FilteredResistance_uOhm <= c_Res_Trip_L THEN
    bAlm_Res_L_Raw := TRUE;
ELSIF rPot_FilteredResistance_uOhm >= (c_Res_Trip_L + c_Res_Hysteresis) THEN
    bAlm_Res_L_Raw := FALSE;
END_IF;

(* Low-Low Alarm: 3.80 uOhm *)
IF rPot_FilteredResistance_uOhm <= c_Res_Trip_LL THEN
    bAlm_Res_LL_Raw := TRUE;
ELSIF rPot_FilteredResistance_uOhm >= (c_Res_Trip_LL + c_Res_Hysteresis) THEN
    bAlm_Res_LL_Raw := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 3. BATH ELECTROLYTE TEMPERATURE MULTI-TIER ALARMS (HH, H, L, LL)
 * Nominal: 955.0 deg C, Deadband Hysteresis: 2.50 deg C
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Alarm: 980.0 deg C (Boiling / Fluoride Loss) *)
IF rPot_VotedBathTemp_degC >= c_Temp_Trip_HH THEN
    bAlm_Temp_HH_Raw := TRUE;
ELSIF rPot_VotedBathTemp_degC <= (c_Temp_Trip_HH - c_Temp_Hysteresis) THEN
    bAlm_Temp_HH_Raw := FALSE;
END_IF;

(* High Alarm: 968.0 deg C *)
IF rPot_VotedBathTemp_degC >= c_Temp_Trip_H THEN
    bAlm_Temp_H_Raw := TRUE;
ELSIF rPot_VotedBathTemp_degC <= (c_Temp_Trip_H - c_Temp_Hysteresis) THEN
    bAlm_Temp_H_Raw := FALSE;
END_IF;

(* Low Alarm: 942.0 deg C (Sludge Formation Risk) *)
IF rPot_VotedBathTemp_degC <= c_Temp_Trip_L THEN
    bAlm_Temp_L_Raw := TRUE;
ELSIF rPot_VotedBathTemp_degC >= (c_Temp_Trip_L + c_Temp_Hysteresis) THEN
    bAlm_Temp_L_Raw := FALSE;
END_IF;

(* Low-Low Alarm: 930.0 deg C (Severe Freeze-Up Danger) *)
IF rPot_VotedBathTemp_degC <= c_Temp_Trip_LL THEN
    bAlm_Temp_LL_Raw := TRUE;
ELSIF rPot_VotedBathTemp_degC >= (c_Temp_Trip_LL + c_Temp_Hysteresis) THEN
    bAlm_Temp_LL_Raw := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 4. DISSOLVED ALUMINA CONCENTRATION MULTI-TIER ALARMS (HH, H, L, LL)
 * Nominal: 2.45 wt%, Deadband Hysteresis: 0.12 wt%
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Alarm: 4.60 wt% (Undissolved Muck Sludge) *)
IF arrX_hat[2] >= c_Alumina_Trip_HH THEN
    bAlm_Alumina_HH_Raw := TRUE;
ELSIF arrX_hat[2] <= (c_Alumina_Trip_HH - c_Alumina_Hysteresis) THEN
    bAlm_Alumina_HH_Raw := FALSE;
END_IF;

(* High Alarm: 3.80 wt% *)
IF arrX_hat[2] >= c_Alumina_Trip_H THEN
    bAlm_Alumina_H_Raw := TRUE;
ELSIF arrX_hat[2] <= (c_Alumina_Trip_H - c_Alumina_Hysteresis) THEN
    bAlm_Alumina_H_Raw := FALSE;
END_IF;

(* Low Alarm: 1.85 wt% (Polarization Inception) *)
IF arrX_hat[2] <= c_Alumina_Trip_L THEN
    bAlm_Alumina_L_Raw := TRUE;
ELSIF arrX_hat[2] >= (c_Alumina_Trip_L + c_Alumina_Hysteresis) THEN
    bAlm_Alumina_L_Raw := FALSE;
END_IF;

(* Low-Low Alarm: 1.45 wt% (Full Anode Effect Flash Imminent) *)
IF arrX_hat[2] <= c_Alumina_Trip_LL THEN
    bAlm_Alumina_LL_Raw := TRUE;
ELSIF arrX_hat[2] >= (c_Alumina_Trip_LL + c_Alumina_Hysteresis) THEN
    bAlm_Alumina_LL_Raw := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5. ANODE-CATHODE DISTANCE (ACD) MULTI-TIER ALARMS (HH, H, L, LL)
 * Nominal: 42.0 mm, Deadband Hysteresis: 1.20 mm
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Alarm: 58.0 mm (Excessive Ohmic Voltage / Heat) *)
IF rPot_EstAnodeCathodeDist_mm >= c_ACD_Trip_HH THEN
    bAlm_ACD_HH_Raw := TRUE;
ELSIF rPot_EstAnodeCathodeDist_mm <= (c_ACD_Trip_HH - c_ACD_Hysteresis) THEN
    bAlm_ACD_HH_Raw := FALSE;
END_IF;

(* High Alarm: 50.0 mm *)
IF rPot_EstAnodeCathodeDist_mm >= c_ACD_Trip_H THEN
    bAlm_ACD_H_Raw := TRUE;
ELSIF rPot_EstAnodeCathodeDist_mm <= (c_ACD_Trip_H - c_ACD_Hysteresis) THEN
    bAlm_ACD_H_Raw := FALSE;
END_IF;

(* Low Alarm: 34.0 mm (Metal Wave Contact Risk) *)
IF rPot_EstAnodeCathodeDist_mm <= c_ACD_Trip_L THEN
    bAlm_ACD_L_Raw := TRUE;
ELSIF rPot_EstAnodeCathodeDist_mm >= (c_ACD_Trip_L + c_ACD_Hysteresis) THEN
    bAlm_ACD_L_Raw := FALSE;
END_IF;

(* Low-Low Alarm: 28.0 mm (Imminent Cathode Short Circuit) *)
IF rPot_EstAnodeCathodeDist_mm <= c_ACD_Trip_LL THEN
    bAlm_ACD_LL_Raw := TRUE;
ELSIF rPot_EstAnodeCathodeDist_mm >= (c_ACD_Trip_LL + c_ACD_Hysteresis) THEN
    bAlm_ACD_LL_Raw := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 6. HARDWARE & SAFETY FAULT ALARM STATUS EVALUATION
 * --------------------------------------------------------------------------------------------------------------------- *)
bAlm_AnodeEffectActive := bPot_InAnodeEffect;
bAlm_AnodeEffectPredicted := bPot_EarlyAnodeEffectWarning;
bAlm_HoistMotorOverloadTrip := bDI_AnodeHoistMotorOverload;
bAlm_HoistTravelLimitTrip := bDI_AnodeHoistUpperLimit_LS OR bDI_AnodeHoistLowerLimit_LS;
bAlm_PotlineBypassEngaged := bDI_PotBypassSwitchClosed;
bAlm_EmergencyStopLatched := bDI_EmergencyStop_PB;
bAlm_PointFeederJamAny := bDI_PointFeederCrustBreaker1_Jam OR bDI_PointFeederCrustBreaker2_Jam OR
                           bDI_PointFeederCrustBreaker3_Jam OR bDI_PointFeederCrustBreaker4_Jam;

bAlm_TMR_Discrepancy_Volt := (nDegradedMode_Volt > 0);
bAlm_TMR_Discrepancy_Curr := (nDegradedMode_Curr > 0);
bAlm_TMR_Discrepancy_Temp := (nDegradedMode_Temp > 0);
bAlm_TMR_Discrepancy_Pos  := (nDegradedMode_Pos > 0);

(* ---------------------------------------------------------------------------------------------------------------------
 * 7. ISA-18.2 ALARM LATCHING AND ACKNOWLEDGMENT MANAGEMENT
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High and High Alarms Latching *)
IF bAlm_Volt_HH_Raw THEN bAlm_Volt_HH_Latched := TRUE; END_IF;
IF bAlm_Volt_H_Raw THEN bAlm_Volt_H_Latched := TRUE; END_IF;
IF bAlm_Res_HH_Raw THEN bAlm_Res_HH_Latched := TRUE; END_IF;
IF bAlm_Res_H_Raw THEN bAlm_Res_H_Latched := TRUE; END_IF;
IF bAlm_Temp_HH_Raw THEN bAlm_Temp_HH_Latched := TRUE; END_IF;
IF bAlm_Temp_H_Raw THEN bAlm_Temp_H_Latched := TRUE; END_IF;
IF bAlm_Alumina_HH_Raw THEN bAlm_Alumina_HH_Latched := TRUE; END_IF;
IF bAlm_Alumina_H_Raw THEN bAlm_Alumina_H_Latched := TRUE; END_IF;
IF bAlm_ACD_HH_Raw THEN bAlm_ACD_HH_Latched := TRUE; END_IF;
IF bAlm_ACD_H_Raw THEN bAlm_ACD_H_Latched := TRUE; END_IF;

(* Low-Low and Low Alarms Latching *)
IF bAlm_Volt_LL_Raw THEN bAlm_Volt_LL_Latched := TRUE; END_IF;
IF bAlm_Volt_L_Raw THEN bAlm_Volt_L_Latched := TRUE; END_IF;
IF bAlm_Res_LL_Raw THEN bAlm_Res_LL_Latched := TRUE; END_IF;
IF bAlm_Res_L_Raw THEN bAlm_Res_L_Latched := TRUE; END_IF;
IF bAlm_Temp_LL_Raw THEN bAlm_Temp_LL_Latched := TRUE; END_IF;
IF bAlm_Temp_L_Raw THEN bAlm_Temp_L_Latched := TRUE; END_IF;
IF bAlm_Alumina_LL_Raw THEN bAlm_Alumina_LL_Latched := TRUE; END_IF;
IF bAlm_Alumina_L_Raw THEN bAlm_Alumina_L_Latched := TRUE; END_IF;
IF bAlm_ACD_LL_Raw THEN bAlm_ACD_LL_Latched := TRUE; END_IF;
IF bAlm_ACD_L_Raw THEN bAlm_ACD_L_Latched := TRUE; END_IF;

(* Reset latched alarms when raw condition has cleared and operator issues Reset Trip *)
IF bCmd_ResetTrip THEN
    IF NOT bAlm_Volt_HH_Raw THEN bAlm_Volt_HH_Latched := FALSE; END_IF;
    IF NOT bAlm_Volt_H_Raw THEN bAlm_Volt_H_Latched := FALSE; END_IF;
    IF NOT bAlm_Res_HH_Raw THEN bAlm_Res_HH_Latched := FALSE; END_IF;
    IF NOT bAlm_Res_H_Raw THEN bAlm_Res_H_Latched := FALSE; END_IF;
    IF NOT bAlm_Temp_HH_Raw THEN bAlm_Temp_HH_Latched := FALSE; END_IF;
    IF NOT bAlm_Temp_H_Raw THEN bAlm_Temp_H_Latched := FALSE; END_IF;
    IF NOT bAlm_Alumina_HH_Raw THEN bAlm_Alumina_HH_Latched := FALSE; END_IF;
    IF NOT bAlm_Alumina_H_Raw THEN bAlm_Alumina_H_Latched := FALSE; END_IF;
    IF NOT bAlm_ACD_HH_Raw THEN bAlm_ACD_HH_Latched := FALSE; END_IF;
    IF NOT bAlm_ACD_H_Raw THEN bAlm_ACD_H_Latched := FALSE; END_IF;

    IF NOT bAlm_Volt_LL_Raw THEN bAlm_Volt_LL_Latched := FALSE; END_IF;
    IF NOT bAlm_Volt_L_Raw THEN bAlm_Volt_L_Latched := FALSE; END_IF;
    IF NOT bAlm_Res_LL_Raw THEN bAlm_Res_LL_Latched := FALSE; END_IF;
    IF NOT bAlm_Res_L_Raw THEN bAlm_Res_L_Latched := FALSE; END_IF;
    IF NOT bAlm_Temp_LL_Raw THEN bAlm_Temp_LL_Latched := FALSE; END_IF;
    IF NOT bAlm_Temp_L_Raw THEN bAlm_Temp_L_Latched := FALSE; END_IF;
    IF NOT bAlm_Alumina_LL_Raw THEN bAlm_Alumina_LL_Latched := FALSE; END_IF;
    IF NOT bAlm_Alumina_L_Raw THEN bAlm_Alumina_L_Latched := FALSE; END_IF;
    IF NOT bAlm_ACD_LL_Raw THEN bAlm_ACD_LL_Latched := FALSE; END_IF;
    IF NOT bAlm_ACD_L_Raw THEN bAlm_ACD_L_Latched := FALSE; END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 8. DETERMINISTIC FIRST-OUT TRIP CAPTURE
 * Captures root cause initiation flag on the very first scan cycle of an emergency trip event.
 * --------------------------------------------------------------------------------------------------------------------- *)
IF bPot_EmergencyTripped AND (dwFirstOutWord = 16#00000000) THEN
    IF bDI_EmergencyStop_PB THEN
        dwFirstOutWord := 16#00000001; (* Bit 0: Hardwired E-Stop Pushbutton *)
    ELSIF bDI_AnodeHoistMotorOverload THEN
        dwFirstOutWord := 16#00000002; (* Bit 1: Anode Hoist Motor Overload Contactor *)
    ELSIF rPot_EstAnodeCathodeDist_mm <= c_ACD_Trip_LL THEN
        dwFirstOutWord := 16#00000004; (* Bit 2: ACD Low-Low Collapse Short Circuit *)
    ELSIF rPot_VotedCellVoltage_V >= c_Volt_AnodeEffect_Threshold AND rFSM_StateTimer_s >= 240.0 THEN
        dwFirstOutWord := 16#00000008; (* Bit 3: Anode Effect Extinction Timeout *)
    ELSIF rPot_VotedCellVoltage_V >= c_Volt_Trip_HH THEN
        dwFirstOutWord := 16#00000010; (* Bit 4: Cell Voltage High-High Trip *)
    ELSIF rPot_VotedBathTemp_degC >= c_Temp_Trip_HH THEN
        dwFirstOutWord := 16#00000020; (* Bit 5: Bath Temperature High-High Trip *)
    ELSIF bDI_PointFeederCrustBreaker1_Jam OR bDI_PointFeederCrustBreaker2_Jam THEN
        dwFirstOutWord := 16#00000040; (* Bit 6: Mechanical Crust Breaker Chisel Jam *)
    ELSE
        dwFirstOutWord := 16#00000080; (* Bit 7: Supervisory SCADA Remote Trip *)
    END_IF;
END_IF;

IF bCmd_ResetTrip AND NOT bPot_EmergencyTripped THEN
    dwFirstOutWord := 16#00000000;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 9. BIT-PACKED 32-BIT TELEMETRY DWORDS
 * Bit-packs internal states, sensor diagnostics, and alarms for high-speed industrial SCADA / Historian polling.
 * --------------------------------------------------------------------------------------------------------------------- *)
(* dwStatusWord1: Primary Subsystem Status *)
dwStatusWord1 := 16#00000000;
dwStatusWord1 := dwStatusWord1 OR INT_TO_DWORD(nFSM_CurrentState AND 16#0F);
IF bPot_FeedingModeNominal         THEN dwStatusWord1 := dwStatusWord1 OR 16#00000010; END_IF; (* Bit 4 *)
IF bPot_FeedingModeUnderfeed       THEN dwStatusWord1 := dwStatusWord1 OR 16#00000020; END_IF; (* Bit 5 *)
IF bPot_FeedingModeOverfeed        THEN dwStatusWord1 := dwStatusWord1 OR 16#00000040; END_IF; (* Bit 6 *)
IF bPot_BeamRockingActive          THEN dwStatusWord1 := dwStatusWord1 OR 16#00000080; END_IF; (* Bit 7 *)
IF bHealth_Volt_CH1                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000100; END_IF; (* Bit 8 *)
IF bHealth_Volt_CH2                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000200; END_IF; (* Bit 9 *)
IF bHealth_Volt_CH3                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000400; END_IF; (* Bit 10 *)
IF bHealth_Curr_CH1                THEN dwStatusWord1 := dwStatusWord1 OR 16#00000800; END_IF; (* Bit 11 *)
IF bHealth_Curr_CH2                THEN dwStatusWord1 := dwStatusWord1 OR 16#00001000; END_IF; (* Bit 12 *)
IF bHealth_Curr_CH3                THEN dwStatusWord1 := dwStatusWord1 OR 16#00002000; END_IF; (* Bit 13 *)
IF bHealth_Temp_CH1                THEN dwStatusWord1 := dwStatusWord1 OR 16#00004000; END_IF; (* Bit 14 *)
IF bHealth_Temp_CH2                THEN dwStatusWord1 := dwStatusWord1 OR 16#00008000; END_IF; (* Bit 15 *)
IF bHealth_Temp_CH3                THEN dwStatusWord1 := dwStatusWord1 OR 16#00010000; END_IF; (* Bit 16 *)
IF bHealth_Pos_CH1                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00020000; END_IF; (* Bit 17 *)
IF bHealth_Pos_CH2                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00040000; END_IF; (* Bit 18 *)
IF bHealth_Pos_CH3                 THEN dwStatusWord1 := dwStatusWord1 OR 16#00080000; END_IF; (* Bit 19 *)
IF bCmd_AnodeBeamHoistUp           THEN dwStatusWord1 := dwStatusWord1 OR 16#00100000; END_IF; (* Bit 20 *)
IF bCmd_AnodeBeamHoistDown         THEN dwStatusWord1 := dwStatusWord1 OR 16#00200000; END_IF; (* Bit 21 *)
IF bCmd_PointFeederFire1           THEN dwStatusWord1 := dwStatusWord1 OR 16#00400000; END_IF; (* Bit 22 *)
IF bCmd_PointFeederFire2           THEN dwStatusWord1 := dwStatusWord1 OR 16#00800000; END_IF; (* Bit 23 *)
IF bCmd_PointFeederFire3           THEN dwStatusWord1 := dwStatusWord1 OR 16#01000000; END_IF; (* Bit 24 *)
IF bCmd_PointFeederFire4           THEN dwStatusWord1 := dwStatusWord1 OR 16#02000000; END_IF; (* Bit 25 *)
IF bCmd_CrustBreakerPunch1         THEN dwStatusWord1 := dwStatusWord1 OR 16#04000000; END_IF; (* Bit 26 *)
IF bCmd_CrustBreakerPunch2         THEN dwStatusWord1 := dwStatusWord1 OR 16#08000000; END_IF; (* Bit 27 *)
IF bCmd_CrustBreakerPunch3         THEN dwStatusWord1 := dwStatusWord1 OR 16#10000000; END_IF; (* Bit 28 *)
IF bCmd_CrustBreakerPunch4         THEN dwStatusWord1 := dwStatusWord1 OR 16#20000000; END_IF; (* Bit 29 *)
IF bInitialized                    THEN dwStatusWord1 := dwStatusWord1 OR 16#40000000; END_IF; (* Bit 30 *)
IF bPot_EmergencyTripped           THEN dwStatusWord1 := dwStatusWord1 OR 16#80000000; END_IF; (* Bit 31 *)

(* dwStatusWord2: Secondary Subsystem Modes & Interlocks *)
dwStatusWord2 := 16#00000000;
IF bCmd_AutoModeEnable             THEN dwStatusWord2 := dwStatusWord2 OR 16#00000001; END_IF; (* Bit 0 *)
IF bCmd_ManualOverride             THEN dwStatusWord2 := dwStatusWord2 OR 16#00000002; END_IF; (* Bit 1 *)
IF bDI_AnodeHoistUpperLimit_LS     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000004; END_IF; (* Bit 2 *)
IF bDI_AnodeHoistLowerLimit_LS     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000008; END_IF; (* Bit 3 *)
IF bDI_AnodeHoistMotorOverload     THEN dwStatusWord2 := dwStatusWord2 OR 16#00000010; END_IF; (* Bit 4 *)
IF bDI_PotBypassSwitchClosed       THEN dwStatusWord2 := dwStatusWord2 OR 16#00000020; END_IF; (* Bit 5 *)
IF bDI_TappingSuctionWandEngaged   THEN dwStatusWord2 := dwStatusWord2 OR 16#00000040; END_IF; (* Bit 6 *)
IF bDI_AnodeChangerCraneInPotArea  THEN dwStatusWord2 := dwStatusWord2 OR 16#00000080; END_IF; (* Bit 7 *)
IF bPot_InAnodeEffect              THEN dwStatusWord2 := dwStatusWord2 OR 16#00000100; END_IF; (* Bit 8 *)
IF bPot_EarlyAnodeEffectWarning    THEN dwStatusWord2 := dwStatusWord2 OR 16#00000200; END_IF; (* Bit 9 *)
IF bDiscr_Volt_12                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00000400; END_IF; (* Bit 10 *)
IF bDiscr_Volt_23                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00000800; END_IF; (* Bit 11 *)
IF bDiscr_Volt_31                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00001000; END_IF; (* Bit 12 *)
IF bDiscr_Curr_12                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00002000; END_IF; (* Bit 13 *)
IF bDiscr_Curr_23                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00004000; END_IF; (* Bit 14 *)
IF bDiscr_Curr_31                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00008000; END_IF; (* Bit 15 *)
IF bDiscr_Temp_12                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00010000; END_IF; (* Bit 16 *)
IF bDiscr_Temp_23                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00020000; END_IF; (* Bit 17 *)
IF bDiscr_Temp_31                  THEN dwStatusWord2 := dwStatusWord2 OR 16#00040000; END_IF; (* Bit 18 *)
IF bDiscr_Pos_12                   THEN dwStatusWord2 := dwStatusWord2 OR 16#00080000; END_IF; (* Bit 19 *)
IF bDiscr_Pos_23                   THEN dwStatusWord2 := dwStatusWord2 OR 16#00100000; END_IF; (* Bit 20 *)
IF bDiscr_Pos_31                   THEN dwStatusWord2 := dwStatusWord2 OR 16#00200000; END_IF; (* Bit 21 *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nDegradedMode_Volt AND 16#03), 22);         (* Bits 22..23 *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nDegradedMode_Curr AND 16#03), 24);         (* Bits 24..25 *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nDegradedMode_Temp AND 16#03), 26);         (* Bits 26..27 *)
dwStatusWord2 := dwStatusWord2 OR SHL(INT_TO_DWORD(nDegradedMode_Pos  AND 16#03), 28);         (* Bits 28..29 *)
IF bCmd_PotlineBypassShuntWedgeFire THEN dwStatusWord2 := dwStatusWord2 OR 16#40000000; END_IF; (* Bit 30 *)
IF bCmd_AnodeEffectHornStrobe      THEN dwStatusWord2 := dwStatusWord2 OR 16#80000000; END_IF; (* Bit 31 *)

(* dwAlarmWord1: High-High and High Process Severity Latched Alarms *)
dwAlarmWord1 := 16#00000000;
IF bAlm_Volt_HH_Latched            THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000001; END_IF; (* Bit 0 *)
IF bAlm_Volt_H_Latched             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; END_IF; (* Bit 1 *)
IF bAlm_Res_HH_Latched             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; END_IF; (* Bit 2 *)
IF bAlm_Res_H_Latched              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; END_IF; (* Bit 3 *)
IF bAlm_Temp_HH_Latched            THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000010; END_IF; (* Bit 4 *)
IF bAlm_Temp_H_Latched             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000020; END_IF; (* Bit 5 *)
IF bAlm_Alumina_HH_Latched         THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000040; END_IF; (* Bit 6 *)
IF bAlm_Alumina_H_Latched          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000080; END_IF; (* Bit 7 *)
IF bAlm_ACD_HH_Latched             THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000100; END_IF; (* Bit 8 *)
IF bAlm_ACD_H_Latched              THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; END_IF; (* Bit 9 *)
IF bAlm_AnodeEffectActive          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000400; END_IF; (* Bit 10 *)
IF bAlm_AnodeEffectPredicted       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; END_IF; (* Bit 11 *)
IF bAlm_HoistMotorOverloadTrip     THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; END_IF; (* Bit 12 *)
IF bAlm_HoistTravelLimitTrip       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00002000; END_IF; (* Bit 13 *)
IF bAlm_PotlineBypassEngaged       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00004000; END_IF; (* Bit 14 *)
IF bAlm_EmergencyStopLatched       THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00008000; END_IF; (* Bit 15 *)
IF bAlm_PointFeederJamAny          THEN dwAlarmWord1 := dwAlarmWord1 OR 16#00010000; END_IF; (* Bit 16 *)

(* dwAlarmWord2: Low-Low, Low, and Sensor TMR Discrepancy Latched Alarms *)
dwAlarmWord2 := 16#00000000;
IF bAlm_Volt_LL_Latched            THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000001; END_IF; (* Bit 0 *)
IF bAlm_Volt_L_Latched             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000002; END_IF; (* Bit 1 *)
IF bAlm_Res_LL_Latched             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000004; END_IF; (* Bit 2 *)
IF bAlm_Res_L_Latched              THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000008; END_IF; (* Bit 3 *)
IF bAlm_Temp_LL_Latched            THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000010; END_IF; (* Bit 4 *)
IF bAlm_Temp_L_Latched             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000020; END_IF; (* Bit 5 *)
IF bAlm_Alumina_LL_Latched         THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000040; END_IF; (* Bit 6 *)
IF bAlm_Alumina_L_Latched          THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000080; END_IF; (* Bit 7 *)
IF bAlm_ACD_LL_Latched             THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000100; END_IF; (* Bit 8 *)
IF bAlm_ACD_L_Latched              THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000200; END_IF; (* Bit 9 *)
IF bAlm_TMR_Discrepancy_Volt       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000400; END_IF; (* Bit 10 *)
IF bAlm_TMR_Discrepancy_Curr       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00000800; END_IF; (* Bit 11 *)
IF bAlm_TMR_Discrepancy_Temp       THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00001000; END_IF; (* Bit 12 *)
IF bAlm_TMR_Discrepancy_Pos        THEN dwAlarmWord2 := dwAlarmWord2 OR 16#00002000; END_IF; (* Bit 13 *)

END_FUNCTION_BLOCK
'''
