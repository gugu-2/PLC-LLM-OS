# Section 6: Phase 5 ISA-18.2 Alarms & Diagnostic Bit-Packing

def get_sec6():
    return """
(* =====================================================================================================================
 * PHASE 5: ISA-18.2 ALARMS, RATE-OF-CHANGE & DIAGNOSTIC WORD BIT-PACKING
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * 5.1 First-Derivative Rate-of-Change (ROC) Calculations
 * --------------------------------------------------------------------------------------------------------------------- *)
rROC_MeltPress_bar_per_s     := (rVoted_ExtruderMeltPress_bar - rPrevMeltPress_bar) / c_rTs;
rROC_CatenarySag_mm_per_s    := (rVoted_CatenarySag_mm - rPrevCatenarySag_mm) / c_rTs;
rROC_TubeN2Press_bar_per_s   := (rVoted_TubeN2Press_bar - rPrevTubeN2Press_bar) / c_rTs;
rROC_HaulOffTension_kN_per_s := (rVoted_HaulOffTension_kN - rPrevHaulOffTension_kN) / c_rTs;

rPrevMeltPress_bar     := rVoted_ExtruderMeltPress_bar;
rPrevCatenarySag_mm    := rVoted_CatenarySag_mm;
rPrevTubeN2Press_bar   := rVoted_TubeN2Press_bar;
rPrevHaulOffTension_kN := rVoted_HaulOffTension_kN;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5.2 Multi-Tiered Alarm Evaluation with Deadband Hysteresis
 * --------------------------------------------------------------------------------------------------------------------- *)

(* 1. Melt Pressure Alarms *)
IF rVoted_ExtruderMeltPress_bar >= c_rTrip_MeltPress_HH_bar THEN
    bAlarm_MeltPress_HH := TRUE;
ELSIF rVoted_ExtruderMeltPress_bar < (c_rTrip_MeltPress_HH_bar - c_rDeadband_MeltPress_bar) THEN
    bAlarm_MeltPress_HH := FALSE;
END_IF;

IF rVoted_ExtruderMeltPress_bar >= c_rAlarm_MeltPress_H_bar THEN
    bAlarm_MeltPress_H := TRUE;
ELSIF rVoted_ExtruderMeltPress_bar < (c_rAlarm_MeltPress_H_bar - c_rDeadband_MeltPress_bar) THEN
    bAlarm_MeltPress_H := FALSE;
END_IF;

IF rVoted_ExtruderMeltPress_bar <= c_rAlarm_MeltPress_L_bar THEN
    bAlarm_MeltPress_L := TRUE;
ELSIF rVoted_ExtruderMeltPress_bar > (c_rAlarm_MeltPress_L_bar + c_rDeadband_MeltPress_bar) THEN
    bAlarm_MeltPress_L := FALSE;
END_IF;

IF rVoted_ExtruderMeltPress_bar <= c_rTrip_MeltPress_LL_bar THEN
    bAlarm_MeltPress_LL := TRUE;
ELSIF rVoted_ExtruderMeltPress_bar > (c_rTrip_MeltPress_LL_bar + c_rDeadband_MeltPress_bar) THEN
    bAlarm_MeltPress_LL := FALSE;
END_IF;

bAlarm_MeltPress_ROC := ABS(rROC_MeltPress_bar_per_s) >= 25.0;

(* 2. Catenary Sag Tube Wall Contact Alarms *)
IF rVoted_CatenarySag_mm >= c_rTrip_CatenarySag_HH_mm THEN
    bAlarm_CatenarySag_HH := TRUE;
ELSIF rVoted_CatenarySag_mm < (c_rTrip_CatenarySag_HH_mm - c_rDeadband_CatenarySag_mm) THEN
    bAlarm_CatenarySag_HH := FALSE;
END_IF;

IF rVoted_CatenarySag_mm >= c_rAlarm_CatenarySag_H_mm THEN
    bAlarm_CatenarySag_H := TRUE;
ELSIF rVoted_CatenarySag_mm < (c_rAlarm_CatenarySag_H_mm - c_rDeadband_CatenarySag_mm) THEN
    bAlarm_CatenarySag_H := FALSE;
END_IF;

IF rVoted_CatenarySag_mm <= c_rAlarm_CatenarySag_L_mm THEN
    bAlarm_CatenarySag_L := TRUE;
ELSIF rVoted_CatenarySag_mm > (c_rAlarm_CatenarySag_L_mm + c_rDeadband_CatenarySag_mm) THEN
    bAlarm_CatenarySag_L := FALSE;
END_IF;

IF rVoted_CatenarySag_mm <= c_rTrip_CatenarySag_LL_mm THEN
    bAlarm_CatenarySag_LL := TRUE;
ELSIF rVoted_CatenarySag_mm > (c_rTrip_CatenarySag_LL_mm + c_rDeadband_CatenarySag_mm) THEN
    bAlarm_CatenarySag_LL := FALSE;
END_IF;

bAlarm_CatenarySag_ROC := ABS(rROC_CatenarySag_mm_per_s) >= 1.50;

(* 3. Tube Nitrogen Overpressure Alarms *)
IF rVoted_TubeN2Press_bar >= c_rTrip_TubeN2Press_HH_bar THEN
    bAlarm_TubeN2Press_HH := TRUE;
ELSIF rVoted_TubeN2Press_bar < (c_rTrip_TubeN2Press_HH_bar - c_rDeadband_TubeN2Press_bar) THEN
    bAlarm_TubeN2Press_HH := FALSE;
END_IF;

IF rVoted_TubeN2Press_bar >= c_rAlarm_TubeN2Press_H_bar THEN
    bAlarm_TubeN2Press_H := TRUE;
ELSIF rVoted_TubeN2Press_bar < (c_rAlarm_TubeN2Press_H_bar - c_rDeadband_TubeN2Press_bar) THEN
    bAlarm_TubeN2Press_H := FALSE;
END_IF;

IF rVoted_TubeN2Press_bar <= c_rAlarm_TubeN2Press_L_bar THEN
    bAlarm_TubeN2Press_L := TRUE;
ELSIF rVoted_TubeN2Press_bar > (c_rAlarm_TubeN2Press_L_bar + c_rDeadband_TubeN2Press_bar) THEN
    bAlarm_TubeN2Press_L := FALSE;
END_IF;

IF rVoted_TubeN2Press_bar <= c_rTrip_TubeN2Press_LL_bar THEN
    bAlarm_TubeN2Press_LL := TRUE;
ELSIF rVoted_TubeN2Press_bar > (c_rTrip_TubeN2Press_LL_bar + c_rDeadband_TubeN2Press_bar) THEN
    bAlarm_TubeN2Press_LL := FALSE;
END_IF;

bAlarm_TubeN2Press_ROC := ABS(rROC_TubeN2Press_bar_per_s) >= 0.50;

(* 4. Zone 1 Radiant Temperature Alarms *)
IF rVoted_Zone1Temp_degC >= c_rTrip_Zone1Temp_HH_degC THEN
    bAlarm_Zone1Temp_HH := TRUE;
ELSIF rVoted_Zone1Temp_degC < (c_rTrip_Zone1Temp_HH_degC - c_rDeadband_Zone1Temp_degC) THEN
    bAlarm_Zone1Temp_HH := FALSE;
END_IF;

IF rVoted_Zone1Temp_degC >= c_rAlarm_Zone1Temp_H_degC THEN
    bAlarm_Zone1Temp_H := TRUE;
ELSIF rVoted_Zone1Temp_degC < (c_rAlarm_Zone1Temp_H_degC - c_rDeadband_Zone1Temp_degC) THEN
    bAlarm_Zone1Temp_H := FALSE;
END_IF;

IF rVoted_Zone1Temp_degC <= c_rAlarm_Zone1Temp_L_degC THEN
    bAlarm_Zone1Temp_L := TRUE;
ELSIF rVoted_Zone1Temp_degC > (c_rAlarm_Zone1Temp_L_degC + c_rDeadband_Zone1Temp_degC) THEN
    bAlarm_Zone1Temp_L := FALSE;
END_IF;

IF rVoted_Zone1Temp_degC <= c_rTrip_Zone1Temp_LL_degC THEN
    bAlarm_Zone1Temp_LL := TRUE;
ELSIF rVoted_Zone1Temp_degC > (c_rTrip_Zone1Temp_LL_degC + c_rDeadband_Zone1Temp_degC) THEN
    bAlarm_Zone1Temp_LL := FALSE;
END_IF;

(* 5. Quench Water Level Alarms *)
IF rVoted_QuenchWaterLvl_mm >= c_rTrip_QuenchWaterLvl_HH_mm THEN
    bAlarm_QuenchWaterLvl_HH := TRUE;
ELSIF rVoted_QuenchWaterLvl_mm < (c_rTrip_QuenchWaterLvl_HH_mm - c_rDeadband_QuenchWaterLvl_mm) THEN
    bAlarm_QuenchWaterLvl_HH := FALSE;
END_IF;

IF rVoted_QuenchWaterLvl_mm >= c_rAlarm_QuenchWaterLvl_H_mm THEN
    bAlarm_QuenchWaterLvl_H := TRUE;
ELSIF rVoted_QuenchWaterLvl_mm < (c_rAlarm_QuenchWaterLvl_H_mm - c_rDeadband_QuenchWaterLvl_mm) THEN
    bAlarm_QuenchWaterLvl_H := FALSE;
END_IF;

IF rVoted_QuenchWaterLvl_mm <= c_rAlarm_QuenchWaterLvl_L_mm THEN
    bAlarm_QuenchWaterLvl_L := TRUE;
ELSIF rVoted_QuenchWaterLvl_mm > (c_rAlarm_QuenchWaterLvl_L_mm + c_rDeadband_QuenchWaterLvl_mm) THEN
    bAlarm_QuenchWaterLvl_L := FALSE;
END_IF;

IF rVoted_QuenchWaterLvl_mm <= c_rTrip_QuenchWaterLvl_LL_mm THEN
    bAlarm_QuenchWaterLvl_LL := TRUE;
ELSIF rVoted_QuenchWaterLvl_mm > (c_rTrip_QuenchWaterLvl_LL_mm + c_rDeadband_QuenchWaterLvl_mm) THEN
    bAlarm_QuenchWaterLvl_LL := FALSE;
END_IF;

(* 6. Haul-Off Line Tension Alarms *)
IF rVoted_HaulOffTension_kN >= c_rTrip_HaulOffTension_HH_kN THEN
    bAlarm_HaulOffTension_HH := TRUE;
ELSIF rVoted_HaulOffTension_kN < (c_rTrip_HaulOffTension_HH_kN - c_rDeadband_HaulOffTension_kN) THEN
    bAlarm_HaulOffTension_HH := FALSE;
END_IF;

IF rVoted_HaulOffTension_kN >= c_rAlarm_HaulOffTension_H_kN THEN
    bAlarm_HaulOffTension_H := TRUE;
ELSIF rVoted_HaulOffTension_kN < (c_rAlarm_HaulOffTension_H_kN - c_rDeadband_HaulOffTension_kN) THEN
    bAlarm_HaulOffTension_H := FALSE;
END_IF;

IF rVoted_HaulOffTension_kN <= c_rAlarm_HaulOffTension_L_kN THEN
    bAlarm_HaulOffTension_L := TRUE;
ELSIF rVoted_HaulOffTension_kN > (c_rAlarm_HaulOffTension_L_kN + c_rDeadband_HaulOffTension_kN) THEN
    bAlarm_HaulOffTension_L := FALSE;
END_IF;

IF rVoted_HaulOffTension_kN <= c_rTrip_HaulOffTension_LL_kN THEN
    bAlarm_HaulOffTension_LL := TRUE;
ELSIF rVoted_HaulOffTension_kN > (c_rTrip_HaulOffTension_LL_kN + c_rDeadband_HaulOffTension_kN) THEN
    bAlarm_HaulOffTension_LL := FALSE;
END_IF;

(* 7. Cable Wall Eccentricity Alarms *)
IF rCalculated_WallEccentricity_pct >= c_rTrip_Eccentricity_HH_pct THEN
    bAlarm_Eccentricity_HH := TRUE;
ELSE
    bAlarm_Eccentricity_HH := FALSE;
END_IF;

IF rCalculated_WallEccentricity_pct >= c_rAlarm_Eccentricity_H_pct THEN
    bAlarm_Eccentricity_H := TRUE;
ELSE
    bAlarm_Eccentricity_H := FALSE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 5.3 Bit-Packing into ISA-18.2 Diagnostic & Status Words
 * --------------------------------------------------------------------------------------------------------------------- *)

(* dwStatusWord_CVLine: Bit-Packed Operational State *)
dwStatusWord_CVLine := 16#0000_0000;
IF bSystemReady             THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0001; END_IF;
IF bSystemRunning           THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0002; END_IF;
IF bEmergencyTripped        THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0004; END_IF;
IF bCatenarySagCenteringOk  THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0008; END_IF;
IF bTubeContactHazardActive THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0010; END_IF;
IF bCrossLinkingTargetAchieved THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0020; END_IF;
IF bEccentricityAlarmActive THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0040; END_IF;
IF bHydrostaticSealBalanced THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0080; END_IF;
IF bSpoolTransferPermissive THEN dwStatusWord_CVLine := dwStatusWord_CVLine OR 16#0000_0100; END_IF;
dwStatusWord_CVLine := dwStatusWord_CVLine OR SHL(INT_TO_DWORD(nActiveFSM_State), 16);

(* dwStatusWord_Extruders: Actuator Flags *)
dwStatusWord_Extruders := 16#0000_0000;
IF rCmd_Extruder2_XLPE_RPM > 0.1 THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0001; END_IF;
IF rCmd_Extruder1_CondScreen_RPM > 0.1 THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0002; END_IF;
IF rCmd_Extruder3_InsScreen_RPM > 0.1 THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0004; END_IF;
IF rCmd_HaulOffCapstan_Speed_mpm > 0.1 THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0008; END_IF;
IF bCmd_CaterpillarPneumaticBrakeClamp THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0010; END_IF;
IF bCmd_EmergencyN2FastVent            THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0020; END_IF;
IF bCmd_TelescopicSealIsolate          THEN dwStatusWord_Extruders := dwStatusWord_Extruders OR 16#0000_0040; END_IF;

(* dwAlarmWord_Trip: Priority 1 Safety Trips *)
dwAlarmWord_Trip := 16#0000_0000;
IF bAlarm_MeltPress_HH      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0001; END_IF;
IF bAlarm_MeltPress_LL      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0002; END_IF;
IF bAlarm_CatenarySag_HH    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0004; END_IF;
IF bAlarm_CatenarySag_LL    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0008; END_IF;
IF bAlarm_TubeN2Press_HH    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0010; END_IF;
IF bAlarm_TubeN2Press_LL    THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0020; END_IF;
IF bAlarm_Zone1Temp_HH      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0040; END_IF;
IF bAlarm_Zone1Temp_LL      THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0080; END_IF;
IF bAlarm_QuenchWaterLvl_HH THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0100; END_IF;
IF bAlarm_QuenchWaterLvl_LL THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0200; END_IF;
IF bAlarm_HaulOffTension_HH THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0400; END_IF;
IF bAlarm_HaulOffTension_LL THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0800; END_IF;
IF bAlarm_Eccentricity_HH   THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_1000; END_IF;
IF bAlarm_TMR_MajorDivergence THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_2000; END_IF;

(* dwAlarmWord_Warning: Priority 2 Process Deviations *)
dwAlarmWord_Warning := 16#0000_0000;
IF bAlarm_MeltPress_H       THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0001; END_IF;
IF bAlarm_MeltPress_L       THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0002; END_IF;
IF bAlarm_MeltPress_ROC     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0004; END_IF;
IF bAlarm_CatenarySag_H     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0008; END_IF;
IF bAlarm_CatenarySag_L     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0010; END_IF;
IF bAlarm_CatenarySag_ROC   THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0020; END_IF;
IF bAlarm_TubeN2Press_H     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0040; END_IF;
IF bAlarm_TubeN2Press_L     THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0080; END_IF;
IF bAlarm_TubeN2Press_ROC   THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0100; END_IF;
IF bAlarm_Zone1Temp_H       THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0200; END_IF;
IF bAlarm_Zone1Temp_L       THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0400; END_IF;
IF bAlarm_QuenchWaterLvl_H  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0800; END_IF;
IF bAlarm_QuenchWaterLvl_L  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_1000; END_IF;
IF bAlarm_HaulOffTension_H  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_2000; END_IF;
IF bAlarm_HaulOffTension_L  THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_4000; END_IF;
IF bAlarm_Eccentricity_H    THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_8000; END_IF;

END_FUNCTION_BLOCK
"""

if __name__ == "__main__":
    s6 = get_sec6()
    print("Section 6 Length:", len(s6))
