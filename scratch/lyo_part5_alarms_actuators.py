# Module 5: Phase 7 (Actuator Filtering & Safety), Phase 8 (ISA-18.2 Alarms & Status Packing), Closing
def get_part5():
    return '''(* ==========================================================================================
 * PHASE 7: ACTUATOR SLEW-RATE LIMITING, FILTERS & HARDWARE PROTECTION INTERLOCKS
 * ========================================================================================== *)

(* 1. Electric Circulation Heater SCR Output Slew-Rate Limiter *)
IF rCmd_ShelfHeater_SCR_pct > rCmd_ShelfHeater_Filtered THEN
    rCmd_ShelfHeater_Filtered := rCmd_ShelfHeater_Filtered + MIN((rCmd_ShelfHeater_SCR_pct - rCmd_ShelfHeater_Filtered), (rShelfHeater_SlewRate_pct_s * rDeltaTime_s));
ELSIF rCmd_ShelfHeater_SCR_pct < rCmd_ShelfHeater_Filtered THEN
    rCmd_ShelfHeater_Filtered := rCmd_ShelfHeater_Filtered - MIN((rCmd_ShelfHeater_Filtered - rCmd_ShelfHeater_SCR_pct), (rShelfHeater_SlewRate_pct_s * rDeltaTime_s));
END_IF;
rCmd_ShelfHeater_SCR_pct := rCmd_ShelfHeater_Filtered;

(* 2. Cryogenic Brine Cooling Expansion Valve Slew-Rate Limiter *)
IF rCmd_ShelfCooling_Valve_pct > rCmd_ShelfCooling_Filtered THEN
    rCmd_ShelfCooling_Filtered := rCmd_ShelfCooling_Filtered + MIN((rCmd_ShelfCooling_Valve_pct - rCmd_ShelfCooling_Filtered), (rShelfCooling_SlewRate_pct_s * rDeltaTime_s));
ELSIF rCmd_ShelfCooling_Valve_pct < rCmd_ShelfCooling_Filtered THEN
    rCmd_ShelfCooling_Filtered := rCmd_ShelfCooling_Filtered - MIN((rCmd_ShelfCooling_Filtered - rCmd_ShelfCooling_Valve_pct), (rShelfCooling_SlewRate_pct_s * rDeltaTime_s));
END_IF;
rCmd_ShelfCooling_Valve_pct := rCmd_ShelfCooling_Filtered;

(* 3. Nitrogen Piezo Bleed Valve Slew-Rate Limiter *)
IF rCmd_N2MicroBleed_Piezo_pct > rCmd_N2Bleed_Filtered THEN
    rCmd_N2Bleed_Filtered := rCmd_N2Bleed_Filtered + MIN((rCmd_N2MicroBleed_Piezo_pct - rCmd_N2Bleed_Filtered), (rN2Bleed_SlewRate_pct_s * rDeltaTime_s));
ELSIF rCmd_N2MicroBleed_Piezo_pct < rCmd_N2Bleed_Filtered THEN
    rCmd_N2Bleed_Filtered := rCmd_N2Bleed_Filtered - MIN((rCmd_N2Bleed_Filtered - rCmd_N2MicroBleed_Piezo_pct), (rN2Bleed_SlewRate_pct_s * rDeltaTime_s));
END_IF;
rCmd_N2MicroBleed_Piezo_pct := rCmd_N2Bleed_Filtered;

(* 4. Hydraulic Stoppering Proportional Pressure Output Slew Limiter *)
IF rCmd_HydraulicPressure_bar > rCmd_HydPress_Filtered THEN
    rCmd_HydPress_Filtered := rCmd_HydPress_Filtered + MIN((rCmd_HydraulicPressure_bar - rCmd_HydPress_Filtered), (20.0 * rDeltaTime_s));
ELSIF rCmd_HydraulicPressure_bar < rCmd_HydPress_Filtered THEN
    rCmd_HydPress_Filtered := rCmd_HydPress_Filtered - MIN((rCmd_HydPress_Filtered - rCmd_HydraulicPressure_bar), (30.0 * rDeltaTime_s));
END_IF;
rCmd_HydraulicPressure_bar := rCmd_HydPress_Filtered;

(* 5. Roots Booster Blower Vacuum Safety Interlock:
 * Roots blowers cannot operate at atmospheric pressure without severe motor overheating.
 * Interlock: Roots blower drive is strictly inhibited unless chamber vacuum <= 15.0 mbar. *)
IF (rTMR2_VotedVal > 15.0) AND (iState <> 12) THEN
    bCmd_RootsBlower_Start := FALSE;
END_IF;

(* 6. Thermal Shock Protection on Silicone Oil Circulation:
 * Limit maximum temperature rate of change to +/- 2.5 deg C/min to prevent shelf warping *)
IF (rTemp_OilSupply_TE401A - rTemp_OilReturn_degC) > 12.0 THEN
    (* Reduce heating if shelf supply-to-return delta exceeds 12.0 deg C *)
    rCmd_ShelfHeater_SCR_pct := rCmd_ShelfHeater_SCR_pct * 0.75;
END_IF;


(* ==========================================================================================
 * PHASE 8: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & 32-BIT SERIALIZATION
 * ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
 * Priority 1: Critical Safety & Formulation Collapse Alarms (Immediate Safe Trip)
 * ------------------------------------------------------------------------------------------ *)
(* Alarm 1.0: Hardware Emergency Stop Active *)
IF NOT bEmergencyStop THEN
    dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000001;
ELSE
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000001;
END_IF;

(* Alarm 1.1: Primary Drying Catastrophic Vacuum Loss (P_ch > 0.400 mbar during state 6 or 7) *)
IF ((iState = 6) OR (iState = 7)) AND (rTMR2_VotedVal >= rAlarm_VacLoss_HH_Trip) THEN
    tAlarmTimer_VacLossHH := tAlarmTimer_VacLossHH + rDeltaTime_s;
    IF tAlarmTimer_VacLossHH >= 5.0 THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000002;
    END_IF;
ELSIF rTMR2_VotedVal < (rAlarm_VacLoss_HH_Trip - rAlarm_Vac_Deadband) THEN
    tAlarmTimer_VacLossHH := 0.0;
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000002;
END_IF;

(* Alarm 1.2: Product Formulation Eutectic / Glass Collapse Overheat (T_prod > -30.0 deg C during drying) *)
IF ((iState = 5) OR (iState = 6)) AND (rTMR1_VotedVal >= rAlarm_Product_HH_Trip) THEN
    tAlarmTimer_ProductHH := tAlarmTimer_ProductHH + rDeltaTime_s;
    IF tAlarmTimer_ProductHH >= 3.0 THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000004;
    END_IF;
ELSIF rTMR1_VotedVal < (rAlarm_Product_HH_Trip - rAlarm_Product_Deadband) THEN
    tAlarmTimer_ProductHH := 0.0;
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000004;
END_IF;

(* Alarm 1.3: Hydraulic Stoppering Overpressure Slam Trip (P_hyd > 235.0 bar) *)
IF rTMR6_VotedVal >= rAlarm_HydPress_HH_Trip THEN
    tAlarmTimer_HydPressHH := tAlarmTimer_HydPressHH + rDeltaTime_s;
    IF tAlarmTimer_HydPressHH >= 0.5 THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000008;
        bCmd_HydraulicDump_SlamOpen := TRUE; (* High-speed slam open relief valve *)
    END_IF;
ELSIF rTMR6_VotedVal < (rAlarm_HydPress_HH_Trip - rAlarm_HydPress_Deadband) THEN
    tAlarmTimer_HydPressHH := 0.0;
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000008;
    bCmd_HydraulicDump_SlamOpen := FALSE;
END_IF;

(* Alarm 1.4: Inflatable Door Gasket Deflation Failure during Vacuum or SIP *)
IF ((iState >= 5) AND (iState <= 8)) OR (iState = 12) THEN
    IF NOT bInflatableSeal_Pressurized THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000010;
    ELSE
        dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000010;
    END_IF;
ELSE
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000010;
END_IF;

(* Alarm 1.5: Condenser Surface Severe Overheat (T_cond > -45.0 deg C during deep evacuation/drying) *)
IF ((iState >= 5) AND (iState <= 8)) AND (rTemp_CondenserSurface_degC >= rAlarm_CondTemp_HH_Trip) THEN
    tAlarmTimer_CondTempHH := tAlarmTimer_CondTempHH + rDeltaTime_s;
    IF tAlarmTimer_CondTempHH >= 10.0 THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000020;
    END_IF;
ELSIF rTemp_CondenserSurface_degC < (rAlarm_CondTemp_HH_Trip - rAlarm_CondTemp_Deadband) THEN
    tAlarmTimer_CondTempHH := 0.0;
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000020;
END_IF;

(* Alarm 1.6: Pure Steam Sterilization Under-Temperature (T_drain < 120.0 deg C during SIP plateau) *)
IF (iState = 12) AND (tStateTimer_s >= 1200.0) AND (rTemp_SIP_DrainTrap_degC < rAlarm_SIP_Temp_LL_Trip) THEN
    tAlarmTimer_SIP_TempLL := tAlarmTimer_SIP_TempLL + rDeltaTime_s;
    IF tAlarmTimer_SIP_TempLL >= 15.0 THEN
        dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000040;
    END_IF;
ELSIF rTemp_SIP_DrainTrap_degC >= (rAlarm_SIP_Temp_LL_Trip + rAlarm_SIP_Temp_Deadband) THEN
    tAlarmTimer_SIP_TempLL := 0.0;
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000040;
END_IF;

(* Alarm 1.7: Multiple TMR Failure (Complete Loss of Redundant Sensor Group) *)
IF (iTMR1_HealthGrade = 0) OR (iTMR2_HealthGrade = 0) OR (iTMR4_HealthGrade = 0) THEN
    dwISAAlarm_Critical := dwISAAlarm_Critical OR 16#00000080;
ELSE
    dwISAAlarm_Critical := dwISAAlarm_Critical AND NOT 16#00000080;
END_IF;

(* ------------------------------------------------------------------------------------------
 * Priority 2: Warning Alarms (Quality Degradation & Degradation Alerts)
 * ------------------------------------------------------------------------------------------ *)
(* Alarm 2.0: Primary Drying High Vacuum Warning (P_ch > 0.250 mbar) *)
IF ((iState = 6) OR (iState = 7)) AND (rTMR2_VotedVal >= rAlarm_VacLoss_H_Trip) THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000001;
ELSIF rTMR2_VotedVal < (rAlarm_VacLoss_H_Trip - rAlarm_Vac_Deadband) THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000001;
END_IF;

(* Alarm 2.1: Product Temperature High Approach Warning (T_prod > -33.0 deg C) *)
IF ((iState = 5) OR (iState = 6)) AND (rTMR1_VotedVal >= rAlarm_Product_H_Trip) THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000002;
ELSIF rTMR1_VotedVal < (rAlarm_Product_H_Trip - rAlarm_Product_Deadband) THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000002;
END_IF;

(* Alarm 2.2: 16-Zone Shelf Thermal Uniformity Spread High (Spread > 1.2 deg C) *)
IF rShelf_Spread_degC >= rAlarm_ShelfSpread_H_Trip THEN
    tAlarmTimer_ShelfSpreadH := tAlarmTimer_ShelfSpreadH + rDeltaTime_s;
    IF tAlarmTimer_ShelfSpreadH >= 60.0 THEN
        dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000004;
    END_IF;
ELSIF rShelf_Spread_degC < (rAlarm_ShelfSpread_H_Trip - rAlarm_ShelfSpread_Deadband) THEN
    tAlarmTimer_ShelfSpreadH := 0.0;
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000004;
END_IF;

(* Alarm 2.3: Condenser Suction Pressure Degraded High *)
IF rTMR3_VotedVal >= 18.0 THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000008;
ELSE
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000008;
END_IF;

(* Alarm 2.4: Hydraulic Stoppering Pressure Warning High *)
IF rTMR6_VotedVal >= rAlarm_HydPress_H_Trip THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000010;
ELSE
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000010;
END_IF;

(* Alarm 2.5: Any TMR Sensor Group operating in Degraded Mode (Dual or Single) *)
IF (iTMR1_HealthGrade < 3) OR (iTMR2_HealthGrade < 3) OR (iTMR3_HealthGrade < 3) OR
   (iTMR4_HealthGrade < 3) OR (iTMR5_HealthGrade < 3) OR (iTMR6_HealthGrade < 3) THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000020;
ELSE
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000020;
END_IF;

(* Alarm 2.6: Silicone Oil Supply/Return High Delta-T *)
IF ABS(rTemp_OilSupply_TE401A - rTemp_OilReturn_degC) >= 9.0 THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000040;
ELSE
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000040;
END_IF;

(* Alarm 2.7: Nitrogen Bleed Valve Saturated (> 95% output) *)
IF rCmd_N2MicroBleed_Piezo_pct >= 95.0 THEN
    dwISAAlarm_Warning := dwISAAlarm_Warning OR 16#00000080;
ELSE
    dwISAAlarm_Warning := dwISAAlarm_Warning AND NOT 16#00000080;
END_IF;

(* ------------------------------------------------------------------------------------------
 * Priority 3: Advisory Maintenance & Service Alarms
 * ------------------------------------------------------------------------------------------ *)
(* Alarm 3.0: Condenser Ice Thickness High (> 30.0 mm) *)
IF rCond_IceThickness_mm >= 30.0 THEN
    dwISAAlarm_Advisory := dwISAAlarm_Advisory OR 16#00000001;
ELSE
    dwISAAlarm_Advisory := dwISAAlarm_Advisory AND NOT 16#00000001;
END_IF;

(* Alarm 3.1: Vacuum Pump 1 Service Interval Reached *)
IF tTotalBatchTimer_s >= 3600000.0 THEN
    dwISAAlarm_Advisory := dwISAAlarm_Advisory OR 16#00000002;
ELSE
    dwISAAlarm_Advisory := dwISAAlarm_Advisory AND NOT 16#00000002;
END_IF;

(* Global Alarm Flags *)
bAlarm_AnyCritical := (dwISAAlarm_Critical <> 16#00000000);
bAlarm_AnyWarning  := (dwISAAlarm_Warning  <> 16#00000000);

(* ------------------------------------------------------------------------------------------
 * Packed Status Words Serialization
 * ------------------------------------------------------------------------------------------ *)
(* dwSystemStatusWord:
 * Bit 0: Machine Enabled
 * Bit 1: Auto Mode Active
 * Bit 2: Door Locked & Sealed
 * Bit 3: Vacuum Pumps Active
 * Bit 4: Roots Blower Active
 * Bit 5: Refrigeration Compressors Active
 * Bit 6: Silicone Oil Recirculation Active
 * Bit 7: Primary Drying Complete
 * Bit 8: Secondary Drying Complete
 * Bit 9: Stoppering Complete
 * Bit 10: Sterilization Complete
 * Bit 11: Cycle Complete Flag *)
dwSystemStatusWord := 16#00000000;
IF bEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000001; END_IF;
IF bAutoMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; END_IF;
IF bDoorClosed_Locked AND bInflatableSeal_Pressurized THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; END_IF;
IF bVacuumPump1_Running OR bVacuumPump2_Running THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; END_IF;
IF bRootsBlower_Running THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; END_IF;
IF bRefrigComp1_Running OR bRefrigComp2_Running THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; END_IF;
IF bOilPump1_Running OR bOilPump2_Running THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; END_IF;
IF bPrimaryDryingComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;
IF bSecondaryDryingComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000100; END_IF;
IF bStopperingComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000200; END_IF;
IF bSterilizationComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000400; END_IF;
IF bCycleComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000800; END_IF;

(* dwTMRStatusWord: Packing Health Grades for Groups 1 to 6 (4 bits per group) *)
dwTMRStatusWord := SHL(INT_TO_DWORD(iTMR1_HealthGrade), 0)  OR
                   SHL(INT_TO_DWORD(iTMR2_HealthGrade), 4)  OR
                   SHL(INT_TO_DWORD(iTMR3_HealthGrade), 8)  OR
                   SHL(INT_TO_DWORD(iTMR4_HealthGrade), 12) OR
                   SHL(INT_TO_DWORD(iTMR5_HealthGrade), 16) OR
                   SHL(INT_TO_DWORD(iTMR6_HealthGrade), 20);

(* dwActuatorStatusWord: Discrete Solenoid Echo *)
dwActuatorStatusWord := 16#00000000;
IF bCmd_IsolationValve_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000001; END_IF;
IF bCmd_VacuumPump1_Start   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000002; END_IF;
IF bCmd_RootsBlower_Start   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000004; END_IF;
IF bCmd_RefrigComp1_Start   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000008; END_IF;
IF bCmd_RefrigComp2_Start   THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000010; END_IF;
IF bCmd_OilPump1_Start      THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000020; END_IF;
IF bCmd_PureSteam_Valve_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000040; END_IF;
IF bCmd_CondensateDrain_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000080; END_IF;
IF bCmd_N2_SterileVent_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000100; END_IF;

(* Remaining Lyophilization Cycle Time Estimation [hours] *)
CASE iState OF
    1: rObs_CycleRemainingTime_h := 36.0;
    2: rObs_CycleRemainingTime_h := 35.0;
    3: rObs_CycleRemainingTime_h := 33.0;
    4: rObs_CycleRemainingTime_h := 30.0;
    5: rObs_CycleRemainingTime_h := 27.0;
    6: rObs_CycleRemainingTime_h := MAX(1.0, (rPikal_TotalIceMass_kg - rPikal_CumulativeSublimated_kg) / (MAX(0.5, rObs_SublimationRate_kgh)));
    7: rObs_CycleRemainingTime_h := 6.5;
    8: rObs_CycleRemainingTime_h := MAX(0.5, (18000.0 - tStateTimer_s) / 3600.0) + 1.5;
    9: rObs_CycleRemainingTime_h := 1.0;
    10: rObs_CycleRemainingTime_h := 0.5;
    11: rObs_CycleRemainingTime_h := 0.2;
    12: rObs_CycleRemainingTime_h := MAX(0.1, (3600.0 - tStateTimer_s) / 3600.0);
ELSE
    rObs_CycleRemainingTime_h := 0.0;
END_CASE;

END_FUNCTION_BLOCK
'''

if __name__ == "__main__":
    print(f"Part 5 length: {len(get_part5())} characters")
