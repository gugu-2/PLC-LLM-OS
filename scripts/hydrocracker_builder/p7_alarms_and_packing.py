# -*- coding: utf-8 -*-
"""
Part 7: Phase 7 (ISA-18.2 Multi-Tiered Alarm Hierarchy & Discrepancy Diagnostics) and
Phase 8 (Actuator Slew Filtering & Bit-Packed Status Words Serialization)
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_alarms_and_packing_block():
    return """(* ==========================================================================================
 * PHASE 7: ISA-18.2 MULTI-TIERED ALARM HIERARCHY & RUNAWAY TRIP LOGIC
 * ========================================================================================== *)

(* --- 7.1 CATALYST BED TEMPERATURE HOTSPOT ALARMS WITH DEBOUNCE & HYSTERESIS --- *)
(* HH Trip: Catalyst Hotspot Overheat Trip (435.0 deg C) *)
IF rObserved_PeakCatalystTemp_degC >= rBedTemp_HH_Trip THEN
    tAlarmTimer_BedTempHH := tAlarmTimer_BedTempHH + rDeltaTime_s;
    IF tAlarmTimer_BedTempHH >= 1.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000001; (* Bit 0: Catalyst Hotspot Overheat Trip *)
    END_IF;
ELSIF rObserved_PeakCatalystTemp_degC < (rBedTemp_HH_Trip - rBedTemp_Deadband) THEN
    tAlarmTimer_BedTempHH := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFFE;
END_IF;

(* Rate of Change Runaway Trip: dT/dt >= 15.0 deg C/min *)
IF (rObserved_Bed1_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
   (rObserved_Bed2_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
   (rObserved_Bed3_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) OR
   (rObserved_Bed4_dTdt_degCmin >= rBedTemp_Runaway_Rate_Trip) THEN
    tAlarmTimer_RunawayTrigger := tAlarmTimer_RunawayTrigger + rDeltaTime_s;
    IF tAlarmTimer_RunawayTrigger >= 0.5 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000002; (* Bit 1: Bed dT/dt Thermal Runaway Trip *)
    END_IF;
ELSE
    tAlarmTimer_RunawayTrigger := 0.0;
END_IF;

(* H Alarm: High Catalyst Temperature Warning (425.0 deg C) *)
IF rObserved_PeakCatalystTemp_degC >= rBedTemp_H_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000001; (* Bit 0: High Temperature Warning *)
ELSIF rObserved_PeakCatalystTemp_degC < (rBedTemp_H_Trip - rBedTemp_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFFE;
END_IF;

(* L Alarm: Low Catalyst Bed Temperature (360.0 deg C) *)
IF (rObserved_PeakCatalystTemp_degC <= rBedTemp_L_Trip) AND bUnitInRunState THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000002; (* Bit 1: Low Bed Temp / Low Conversion *)
ELSIF rObserved_PeakCatalystTemp_degC > (rBedTemp_L_Trip + rBedTemp_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFFD;
END_IF;

(* LL Trip: Reaction Extinction Loss of Heat (320.0 deg C) *)
IF (rObserved_PeakCatalystTemp_degC <= rBedTemp_LL_Trip) AND bUnitInRunState THEN
    tAlarmTimer_BedTempLL := tAlarmTimer_BedTempLL + rDeltaTime_s;
    IF tAlarmTimer_BedTempLL >= 3.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000004; (* Bit 2: Reaction Extinction Trip *)
    END_IF;
ELSIF rObserved_PeakCatalystTemp_degC > (rBedTemp_LL_Trip + rBedTemp_Deadband) THEN
    tAlarmTimer_BedTempLL := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFFB;
END_IF;

(* --- 7.2 REACTOR INLET PRESSURE ALARMS --- *)
(* HH Trip: Reactor Overpressure Safety Depressurization Slam (198.0 bar) *)
IF rTMR7_VotedVal >= rReactorPress_HH_Trip THEN
    tAlarmTimer_PressHH := tAlarmTimer_PressHH + rDeltaTime_s;
    IF tAlarmTimer_PressHH >= 0.5 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000008; (* Bit 3: Reactor Overpressure Slam Trip *)
    END_IF;
ELSIF rTMR7_VotedVal < (rReactorPress_HH_Trip - rReactorPress_Deadband) THEN
    tAlarmTimer_PressHH := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFF7;
END_IF;

(* H Alarm: High Operating Pressure Warning (190.0 bar) *)
IF rTMR7_VotedVal >= rReactorPress_H_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000004; (* Bit 2: High Operating Pressure Warning *)
ELSIF rTMR7_VotedVal < (rReactorPress_H_Trip - rReactorPress_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFFB;
END_IF;

(* L Alarm: Low Operating Pressure Warning (160.0 bar) *)
IF (rTMR7_VotedVal <= rReactorPress_L_Trip) AND bUnitInRunState THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000008; (* Bit 3: Low Pressure Warning *)
ELSIF rTMR7_VotedVal > (rReactorPress_L_Trip + rReactorPress_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFF7;
END_IF;

(* LL Trip: Severe Containment Depressurization (130.0 bar) *)
IF (rTMR7_VotedVal <= rReactorPress_LL_Trip) AND bUnitInRunState THEN
    tAlarmTimer_PressLL := tAlarmTimer_PressLL + rDeltaTime_s;
    IF tAlarmTimer_PressLL >= 2.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000010; (* Bit 4: Loss of Containment Trip *)
    END_IF;
ELSIF rTMR7_VotedVal > (rReactorPress_LL_Trip + rReactorPress_Deadband) THEN
    tAlarmTimer_PressLL := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFEF;
END_IF;

(* --- 7.3 REACTOR TOTAL DIFFERENTIAL PRESSURE (FOULING / CRUSHING) ALARMS --- *)
(* HH Trip: Bed Crushing & Severe Maldistribution (12.0 bar) *)
IF rTMR6_VotedVal >= rReactorDP_HH_Trip THEN
    tAlarmTimer_DPHH := tAlarmTimer_DPHH + rDeltaTime_s;
    IF tAlarmTimer_DPHH >= 2.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000020; (* Bit 5: Catalyst Bed Crushing Trip *)
    END_IF;
ELSIF rTMR6_VotedVal < (rReactorDP_HH_Trip - rReactorDP_Deadband) THEN
    tAlarmTimer_DPHH := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFDF;
END_IF;

(* H Alarm: High Reactor Differential Pressure (8.5 bar) *)
IF rTMR6_VotedVal >= rReactorDP_H_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000010; (* Bit 4: High Differential Pressure Warning *)
ELSIF rTMR6_VotedVal < (rReactorDP_H_Trip - rReactorDP_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFEF;
END_IF;

(* --- 7.4 HIGH-PRESSURE SEPARATOR LEVEL ALARMS --- *)
(* HH Trip: Separator Overfill / Gas Carryover Prevention (85.0%) *)
IF rTMR5_VotedVal >= rHPSepLevel_HH_Trip THEN
    tAlarmTimer_SepLvlHH := tAlarmTimer_SepLvlHH + rDeltaTime_s;
    IF tAlarmTimer_SepLvlHH >= 1.5 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000040; (* Bit 6: HP Separator High-High Level Trip *)
    END_IF;
ELSIF rTMR5_VotedVal < (rHPSepLevel_HH_Trip - rHPSepLevel_Deadband) THEN
    tAlarmTimer_SepLvlHH := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFFBF;
END_IF;

(* H Alarm: High Level Warning (72.0%) *)
IF rTMR5_VotedVal >= rHPSepLevel_H_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000020; (* Bit 5: HP Separator High Level Warning *)
ELSIF rTMR5_VotedVal < (rHPSepLevel_H_Trip - rHPSepLevel_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFDF;
END_IF;

(* L Alarm: Low Level Warning (30.0%) *)
IF rTMR5_VotedVal <= rHPSepLevel_L_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000040; (* Bit 6: HP Separator Low Level Warning *)
ELSIF rTMR5_VotedVal > (rHPSepLevel_L_Trip + rHPSepLevel_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFFBF;
END_IF;

(* LL Trip: Gas Blowby into Low-Pressure Plant Prevention (15.0%) *)
IF rTMR5_VotedVal <= rHPSepLevel_LL_Trip THEN
    tAlarmTimer_SepLvlLL := tAlarmTimer_SepLvlLL + rDeltaTime_s;
    IF tAlarmTimer_SepLvlLL >= 1.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000080; (* Bit 7: Gas Blowby Low-Low Level Trip *)
    END_IF;
ELSIF rTMR5_VotedVal > (rHPSepLevel_LL_Trip + rHPSepLevel_Deadband) THEN
    tAlarmTimer_SepLvlLL := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFF7F;
END_IF;

(* --- 7.5 AMINE ABSORBER SOUR GAS OVERHEAD H2S ALARMS --- *)
(* HH Trip: Severe Recycle Compressor Corrosion & Catalyst Poisoning (150.0 ppm) *)
IF rTMR8_VotedVal >= rAmineH2S_HH_Trip THEN
    tAlarmTimer_AmineH2SHH := tAlarmTimer_AmineH2SHH + rDeltaTime_s;
    IF tAlarmTimer_AmineH2SHH >= 3.0 THEN
        dwAlarmWord1_Critical := dwAlarmWord1_Critical OR 16#00000100; (* Bit 8: Recycle Gas Severe H2S Trip *)
    END_IF;
ELSIF rTMR8_VotedVal < (rAmineH2S_HH_Trip - rAmineH2S_Deadband) THEN
    tAlarmTimer_AmineH2SHH := 0.0;
    dwAlarmWord1_Critical := dwAlarmWord1_Critical AND 16#FFFFFEFF;
END_IF;

(* H Alarm: High H2S Warning (50.0 ppm) *)
IF rTMR8_VotedVal >= rAmineH2S_H_Trip THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process OR 16#00000080; (* Bit 7: High H2S Recycle Warning *)
ELSIF rTMR8_VotedVal < (rAmineH2S_H_Trip - rAmineH2S_Deadband) THEN
    dwAlarmWord2_Process := dwAlarmWord2_Process AND 16#FFFFFF7F;
END_IF;

(* --- 7.6 2oo3 TMR SENSOR VOTING CHANNEL DISCREPANCY BIT-PACKING --- *)
dwAlarmWord3_TMR := 16#00000000;
IF bTMR1_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000001; END_IF;
IF bTMR1_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000002; END_IF;
IF bTMR1_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000004; END_IF;

IF bTMR2_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000008; END_IF;
IF bTMR2_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000010; END_IF;
IF bTMR2_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000020; END_IF;

IF bTMR3_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000040; END_IF;
IF bTMR3_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000080; END_IF;
IF bTMR3_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000100; END_IF;

IF bTMR4_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000200; END_IF;
IF bTMR4_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000400; END_IF;
IF bTMR4_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00000800; END_IF;

IF bTMR5_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00001000; END_IF;
IF bTMR5_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00002000; END_IF;
IF bTMR5_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00004000; END_IF;

IF bTMR6_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00008000; END_IF;
IF bTMR6_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00010000; END_IF;
IF bTMR6_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00020000; END_IF;

IF bTMR7_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00040000; END_IF;
IF bTMR7_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00080000; END_IF;
IF bTMR7_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00100000; END_IF;

IF bTMR8_FaultA THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00200000; END_IF;
IF bTMR8_FaultB THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00400000; END_IF;
IF bTMR8_FaultC THEN dwAlarmWord3_TMR := dwAlarmWord3_TMR OR 16#00800000; END_IF;

(* Global Alarm Aggregation Flags *)
bAlarm_AnyCritical := (dwAlarmWord1_Critical <> 16#00000000);
bAlarm_AnyWarning  := (dwAlarmWord2_Process <> 16#00000000);

(* Operator Acknowledgment Command *)
IF bAckAlarms THEN
    dwAlarmWord2_Process := 16#00000000;
END_IF;


(* ==========================================================================================
 * PHASE 8: ACTUATOR OUTPUT SLEW FILTERING & BIT-PACKED STATUS WORDS SERIALIZATION
 * ========================================================================================== *)

(* --- 8.1 ACTUATOR FIRST-ORDER LOW PASS FILTERING & CLAMPING --- *)
rQuench1_Filtered := rQuench1_Filtered + (0.25 * (rValve_QuenchBed1_pct - rQuench1_Filtered));
IF rQuench1_Filtered < 0.0 THEN rQuench1_Filtered := 0.0; ELSIF rQuench1_Filtered > 100.0 THEN rQuench1_Filtered := 100.0; END_IF;
rValve_QuenchBed1_pct := rQuench1_Filtered;

rQuench2_Filtered := rQuench2_Filtered + (0.25 * (rValve_QuenchBed2_pct - rQuench2_Filtered));
IF rQuench2_Filtered < 0.0 THEN rQuench2_Filtered := 0.0; ELSIF rQuench2_Filtered > 100.0 THEN rQuench2_Filtered := 100.0; END_IF;
rValve_QuenchBed2_pct := rQuench2_Filtered;

rQuench3_Filtered := rQuench3_Filtered + (0.25 * (rValve_QuenchBed3_pct - rQuench3_Filtered));
IF rQuench3_Filtered < 0.0 THEN rQuench3_Filtered := 0.0; ELSIF rQuench3_Filtered > 100.0 THEN rQuench3_Filtered := 100.0; END_IF;
rValve_QuenchBed3_pct := rQuench3_Filtered;

rFurnace_Filtered := rFurnace_Filtered + (0.10 * (rValve_ChargeFurnaceFuel_pct - rFurnace_Filtered));
IF rFurnace_Filtered < 0.0 THEN rFurnace_Filtered := 0.0; ELSIF rFurnace_Filtered > 100.0 THEN rFurnace_Filtered := 100.0; END_IF;
rValve_ChargeFurnaceFuel_pct := rFurnace_Filtered;

rLetdownA_Filtered := rLetdownA_Filtered + (0.30 * (rValve_HPSep_LetdownA_pct - rLetdownA_Filtered));
IF rLetdownA_Filtered < 0.0 THEN rLetdownA_Filtered := 0.0; ELSIF rLetdownA_Filtered > 100.0 THEN rLetdownA_Filtered := 100.0; END_IF;
rValve_HPSep_LetdownA_pct := rLetdownA_Filtered;

rLetdownB_Filtered := rLetdownB_Filtered + (0.30 * (rValve_HPSep_LetdownB_pct - rLetdownB_Filtered));
IF rLetdownB_Filtered < 0.0 THEN rLetdownB_Filtered := 0.0; ELSIF rLetdownB_Filtered > 100.0 THEN rLetdownB_Filtered := 100.0; END_IF;
rValve_HPSep_LetdownB_pct := rLetdownB_Filtered;

rAminePump_Filtered := rAminePump_Filtered + (0.20 * (rPump_LeanAmine_Speed_pct - rAminePump_Filtered));
IF rAminePump_Filtered < 0.0 THEN rAminePump_Filtered := 0.0; ELSIF rAminePump_Filtered > 100.0 THEN rAminePump_Filtered := 100.0; END_IF;
rPump_LeanAmine_Speed_pct := rAminePump_Filtered;

rReflux_Filtered := rReflux_Filtered + (0.20 * (rValve_DynamicReflux_pct - rReflux_Filtered));
IF rReflux_Filtered < 0.0 THEN rReflux_Filtered := 0.0; ELSIF rReflux_Filtered > 100.0 THEN rReflux_Filtered := 100.0; END_IF;
rValve_DynamicReflux_pct := rReflux_Filtered;

rReboiler_Filtered := rReboiler_Filtered + (0.15 * (rValve_FractionatorReboiler_pct - rReboiler_Filtered));
IF rReboiler_Filtered < 0.0 THEN rReboiler_Filtered := 0.0; ELSIF rReboiler_Filtered > 100.0 THEN rReboiler_Filtered := 100.0; END_IF;
rValve_FractionatorReboiler_pct := rReboiler_Filtered;

(* --- 8.2 BIT-PACKED SYSTEM STATUS WORDS SERIALIZATION --- *)
dwSystemStatusWord := 16#00000000;
IF bEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000001; END_IF;
IF bAutoMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000002; END_IF;
IF bUnitInRunState THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000004; END_IF;
IF bReadyForHydrocarbonFeed THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000008; END_IF;
IF bAlarm_RunawayTripActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000010; END_IF;
IF bAlarm_AnyCritical THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000020; END_IF;
IF bAlarm_AnyWarning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000040; END_IF;
IF bFlareHeaderReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#00000080; END_IF;

(* Encode Active State in bits 8..15 *)
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iState), 8);
(* Encode Sulfiding Stage in bits 16..23 *)
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iSulfidingStage), 16);

(* --- 8.3 2oo3 TMR COMPOSITE HEALTH BITMASK (dwTMRStatusWord) --- *)
dwTMRStatusWord := 16#00000000;
dwTMRStatusWord := dwTMRStatusWord OR (INT_TO_DWORD(iTMR1_HealthGrade) AND 16#00000007);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR2_HealthGrade) AND 16#00000007), 3);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR3_HealthGrade) AND 16#00000007), 6);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR4_HealthGrade) AND 16#00000007), 9);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR5_HealthGrade) AND 16#00000007), 12);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR6_HealthGrade) AND 16#00000007), 15);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR7_HealthGrade) AND 16#00000007), 18);
dwTMRStatusWord := dwTMRStatusWord OR SHL((INT_TO_DWORD(iTMR8_HealthGrade) AND 16#00000007), 21);

(* --- 8.4 ACTUATOR & SOLENOID DISCRETE ECHO BITMASK (dwActuatorStatusWord) --- *)
dwActuatorStatusWord := 16#00000000;
IF bValve_EmergencyBlowdownA_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000001; END_IF;
IF bValve_EmergencyBlowdownB_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000002; END_IF;
IF bValve_ReactorFeed_EmergencyShut THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000004; END_IF;
IF bValve_QuenchFastDump_Open THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000008; END_IF;
IF bValve_MakeupH2_EmergencyShut THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000010; END_IF;
IF bIgniter_ChargeFurnace_Kill THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#00000020; END_IF;

(* Output active state code for external SCADA / DCS *)
iCurrentState := iState;

END_FUNCTION_BLOCK
"""
