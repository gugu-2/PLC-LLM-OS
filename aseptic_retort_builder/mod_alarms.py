# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_alarms.py
Implements Phase 5: ISA-18.2 Multi-Tier Process Alarms, Deadband Hysteresis,
32-Bit Bit-Packed Words (Status, Warning, Fault, Quality/Sterility), and Actuator Interlock Enforcement.
"""

def generate_alarms():
    return '''(* =====================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARMS, DEADBANDS & 32-BIT PACKED TELEMETRY
 * Alarm Hierarchy:
 *   Severity Level 1 (Emergency Trips): Automatic failsafe shutdown, steam isolation, depressurization pilot.
 *   Severity Level 2 (Abnormal Warnings): Process alarms alerting operators to approaching limit boundaries.
 *   Quality Assurance (FDA 21 CFR Part 113): Automated commercial sterility auditing and batch certification.
 * 32-Bit Bit-Packed Telemetry Registers:
 *   - dwStatusWord           : Subsystem mechanical and sequence state bits
 *   - dwWarningWord          : ISA-18.2 Advisory warnings and TMR sensor degradation
 *   - dwFaultWord            : ISA-18.2 Critical safety trips and hardware interlock faults
 *   - dwQualitySterilityWord : US FDA 21 CFR Part 113 compliance and sterility certification
 * ===================================================================================================================== *)

(* Initialize dynamic warning bits while preserving hardware interlock status *)
dwWarningWord := dwWarningWord AND 16#0000_000F;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.1: RETORT TEMPERATURE ALARMS (ISA-18.2 HH, H, L, LL)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Temperature Trip (HH: 138.0 deg C) *)
IF rVoted_Temp_degC >= cTrip_Temp_HH_degC THEN
    rAlarmTimer_TempHH := rAlarmTimer_TempHH + rTs_s;
    IF rAlarmTimer_TempHH >= 0.50 THEN
        bTripLatched_TempHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0001; (* Bit 0: Temp HH Trip *)
    END_IF;
ELSE
    rAlarmTimer_TempHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVoted_Temp_degC < (cTrip_Temp_HH_degC - cHyst_Temp_degC)) THEN
        bTripLatched_TempHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0001;
    END_IF;
END_IF;

(* High Temperature Advisory Warning (H: 135.0 deg C) *)
IF rVoted_Temp_degC >= cWarn_Temp_H_degC THEN
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Bit 0: Temp H Warning *)
ELSIF rVoted_Temp_degC < (cWarn_Temp_H_degC - cHyst_Temp_degC) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0001;
END_IF;

(* Low Temperature Warnings and Underprocessing Trips during Cooking States (States 4, 5, 6) *)
IF (iFSM_CurrentState >= 4) AND (iFSM_CurrentState <= 6) THEN
    (* Low Temperature Warning (L: 120.0 deg C) *)
    IF rVoted_Temp_degC <= cWarn_Temp_L_degC THEN
        dwWarningWord := dwWarningWord OR 16#0000_0002; (* Bit 1: Temp L Warning *)
    ELSIF rVoted_Temp_degC > (cWarn_Temp_L_degC + cHyst_Temp_degC) THEN
        dwWarningWord := dwWarningWord AND NOT 16#0000_0002;
    END_IF;

    (* Low-Low Temperature Trip (LL: 116.0 deg C) *)
    IF rVoted_Temp_degC <= cTrip_Temp_LL_degC THEN
        rAlarmTimer_TempLL := rAlarmTimer_TempLL + rTs_s;
        IF rAlarmTimer_TempLL >= 3.00 THEN
            bTripLatched_TempLL := TRUE;
            dwFaultWord := dwFaultWord OR 16#0000_0002; (* Bit 1: Temp LL Underprocessing Trip *)
        END_IF;
    ELSE
        rAlarmTimer_TempLL := 0.0;
        IF bCmd_AcknowledgeAlarm AND (rVoted_Temp_degC > (cTrip_Temp_LL_degC + cHyst_Temp_degC)) THEN
            bTripLatched_TempLL := FALSE;
            dwFaultWord := dwFaultWord AND NOT 16#0000_0002;
        END_IF;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.2: RETORT TOTAL CHAMBER PRESSURE ALARMS (ISA-18.2 HH, H, L, LL)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Pressure Structural Safety Trip (HH: 4.10 bar) *)
IF rVoted_Press_bar >= cTrip_Press_HH_bar THEN
    rAlarmTimer_PressHH := rAlarmTimer_PressHH + rTs_s;
    IF rAlarmTimer_PressHH >= 0.20 THEN
        bTripLatched_PressHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0004; (* Bit 2: Press HH Structural Trip *)
    END_IF;
ELSE
    rAlarmTimer_PressHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVoted_Press_bar < (cTrip_Press_HH_bar - cHyst_Press_bar)) THEN
        bTripLatched_PressHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0004;
    END_IF;
END_IF;

(* High Pressure Advisory Warning (H: 3.85 bar) *)
IF rVoted_Press_bar >= cWarn_Press_H_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Bit 2: Press H Warning *)
ELSIF rVoted_Press_bar < (cWarn_Press_H_bar - cHyst_Press_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0004;
END_IF;

(* Low Pressure Warnings and Overpressure Collapse Trips during Heated States (States 3, 4, 5, 6, 7) *)
IF (iFSM_CurrentState >= 3) AND (iFSM_CurrentState <= 7) THEN
    IF rVoted_Press_bar <= cWarn_Press_L_bar THEN
        dwWarningWord := dwWarningWord OR 16#0000_0008; (* Bit 3: Press L Warning *)
    ELSIF rVoted_Press_bar > (cWarn_Press_L_bar + cHyst_Press_bar) THEN
        dwWarningWord := dwWarningWord AND NOT 16#0000_0008;
    END_IF;

    IF rVoted_Press_bar <= cTrip_Press_LL_bar THEN
        rAlarmTimer_PressLL := rAlarmTimer_PressLL + rTs_s;
        IF rAlarmTimer_PressLL >= 2.00 THEN
            bTripLatched_PressLL := TRUE;
            dwFaultWord := dwFaultWord OR 16#0000_0008; (* Bit 3: Press LL Overpressure Loss Trip *)
        END_IF;
    ELSE
        rAlarmTimer_PressLL := 0.0;
        IF bCmd_AcknowledgeAlarm AND (rVoted_Press_bar > (cTrip_Press_LL_bar + cHyst_Press_bar)) THEN
            bTripLatched_PressLL := FALSE;
            dwFaultWord := dwFaultWord AND NOT 16#0000_0008;
        END_IF;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.3: CONTAINER WALL DIFFERENTIAL STRESS ALARMS (BURST VS BUCKLE)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* High-High Differential Stress Trip: Pouch Burst Hazard (DeltaP >= +0.150 bar) *)
IF rContainerDeltaP_bar >= cTrip_DeltaP_HH_bar THEN
    rAlarmTimer_DeltaPHH := rAlarmTimer_DeltaPHH + rTs_s;
    IF rAlarmTimer_DeltaPHH >= 0.30 THEN
        bTripLatched_DeltaPHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0010; (* Bit 4: DeltaP HH Pouch Burst Trip *)
    END_IF;
ELSE
    rAlarmTimer_DeltaPHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rContainerDeltaP_bar < (cTrip_DeltaP_HH_bar - cHyst_DeltaP_bar)) THEN
        bTripLatched_DeltaPHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0010;
    END_IF;
END_IF;

(* High Differential Stress Warning (DeltaP >= +0.110 bar) *)
IF rContainerDeltaP_bar >= cWarn_DeltaP_H_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Bit 4: DeltaP H Warning *)
ELSIF rContainerDeltaP_bar < (cWarn_DeltaP_H_bar - cHyst_DeltaP_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0010;
END_IF;

(* Low Differential Stress Warning: External Overpressure High (DeltaP <= -0.110 bar) *)
IF rContainerDeltaP_bar <= cWarn_DeltaP_L_bar THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Bit 5: DeltaP L Warning *)
ELSIF rContainerDeltaP_bar > (cWarn_DeltaP_L_bar + cHyst_DeltaP_bar) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0020;
END_IF;

(* Low-Low Differential Stress Trip: Can Buckling / Panelling Hazard (DeltaP <= -0.150 bar) *)
IF rContainerDeltaP_bar <= cTrip_DeltaP_LL_bar THEN
    rAlarmTimer_DeltaPLL := rAlarmTimer_DeltaPLL + rTs_s;
    IF rAlarmTimer_DeltaPLL >= 0.50 THEN
        bTripLatched_DeltaPLL := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0020; (* Bit 5: DeltaP LL Can Buckling Trip *)
    END_IF;
ELSE
    rAlarmTimer_DeltaPLL := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rContainerDeltaP_bar > (cTrip_DeltaP_LL_bar + cHyst_DeltaP_bar)) THEN
        bTripLatched_DeltaPLL := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0020;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.4: CONDENSATE SUMP LEVEL & TMR DEGRADATION ALARMS
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Sump Flooding / Condensate Backup High-High Trip (HH: 350.0 mm) *)
IF rVoted_Level_mm >= cTrip_Level_HH_mm THEN
    rAlarmTimer_LevelHH := rAlarmTimer_LevelHH + rTs_s;
    IF rAlarmTimer_LevelHH >= 2.00 THEN
        bTripLatched_LevelHH := TRUE;
        dwFaultWord := dwFaultWord OR 16#0000_0040; (* Bit 6: Sump Level HH Trip *)
    END_IF;
ELSE
    rAlarmTimer_LevelHH := 0.0;
    IF bCmd_AcknowledgeAlarm AND (rVoted_Level_mm < (cTrip_Level_HH_mm - cHyst_Level_mm)) THEN
        bTripLatched_LevelHH := FALSE;
        dwFaultWord := dwFaultWord AND NOT 16#0000_0040;
    END_IF;
END_IF;

(* Sump High Level Warning (H: 220.0 mm) *)
IF rVoted_Level_mm >= cWarn_Level_H_mm THEN
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Bit 6: Sump Level H Warning *)
ELSIF rVoted_Level_mm < (cWarn_Level_H_mm - cHyst_Level_mm) THEN
    dwWarningWord := dwWarningWord AND NOT 16#0000_0040;
END_IF;

(* TMR Degradation Status Mapping *)
IF (iTMR_TempMode = 2) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Bit 7: Temp TMR Degraded to 1oo2 *)
ELSIF (iTMR_TempMode <= 1) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800; (* Bit 11: Single Sensor Degraded Mode *)
END_IF;

IF (iTMR_PressMode = 2) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0100; (* Bit 8: Press TMR Degraded to 1oo2 *)
ELSIF (iTMR_PressMode <= 1) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800;
END_IF;

IF (iTMR_LevelMode = 2) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Bit 9: Level TMR Degraded to 1oo2 *)
ELSIF (iTMR_LevelMode <= 1) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800;
END_IF;

IF (iTMR_PouchMode = 2) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Bit 10: Pouch TMR Degraded to 1oo2 *)
ELSIF (iTMR_PouchMode <= 1) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0800;
END_IF;

IF (iTMR_TempMode = 0) OR (iTMR_PressMode = 0) THEN
    dwFaultWord := dwFaultWord OR 16#0000_0080; (* Bit 7: Critical TMR Sensor Failsafe Trip *)
END_IF;

(* Hardware Interlocks in Fault Word *)
IF NOT bDI_SafetyDoorClosed_ZS1 AND (iFSM_CurrentState >= 2) AND (iFSM_CurrentState <= 10) THEN
    dwFaultWord := dwFaultWord OR 16#0000_0100; (* Bit 8: Door Opened in Heated Cycle *)
END_IF;

IF NOT bDI_EmergencyStop_PB THEN
    dwFaultWord := dwFaultWord OR 16#0000_0200; (* Bit 9: Emergency Stop Depressed *)
END_IF;

IF bDI_SafetyReliefPoppetOpen_ZS THEN
    dwFaultWord := dwFaultWord OR 16#0000_0800; (* Bit 11: ASME Relief Valve Poppet Lifted *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.5: 32-BIT BIT-PACKED STATUS WORD (dwStatusWord)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwStatusWord := 16#0000_0000;

(* Pack Active FSM Operational State (Bits 0..3) *)
dwStatusWord := dwStatusWord OR (INT_TO_DWORD(iFSM_CurrentState) AND 16#0000_000F);

(* Mechanical & Actuator Discretes Status *)
IF bDI_SafetyDoorClosed_ZS1 AND bDI_SafetyDoorLocked_ZS2 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0010; (* Bit 4: Safety Door Locked *)
END_IF;

IF bCmd_DoorSealInflate AND (rDoorSealPress_bar >= 5.0) THEN
    dwStatusWord := dwStatusWord OR 16#0000_0020; (* Bit 5: Door Seal Inflated & Pressurized *)
END_IF;

IF rCmd_SteamModValve_pct > 1.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0040; (* Bit 6: Steam Modulating Valve Open *)
END_IF;

IF rCmd_AirOverpressValve_pct > 1.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0080; (* Bit 7: Compressed Air Overpressure Open *)
END_IF;

IF rCmd_ExhaustVentValve_pct > 1.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0100; (* Bit 8: Top Exhaust Vent Open *)
END_IF;

IF rCmd_CoolingWaterCascadeValve_pct > 1.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0200; (* Bit 9: Cascade Cooling Water Spray Open *)
END_IF;

IF rRotaryDrumSpeed_RPM > 0.50 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0400; (* Bit 10: Rotary Helix Agitation Drum Running *)
END_IF;

IF rCmd_DischargeConveyorSpeed_pct > 5.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_0800; (* Bit 11: Discharge Outfeed Conveyor Running *)
END_IF;

IF bCmd_DrainValveOpen THEN
    dwStatusWord := dwStatusWord OR 16#0000_1000; (* Bit 12: Bottom Rapid Drain Valve Open *)
END_IF;

IF NOT bDI_SafetyReliefPoppetOpen_ZS THEN
    dwStatusWord := dwStatusWord OR 16#0000_2000; (* Bit 13: ASME Safety Valve Sealed Normal *)
END_IF;

IF rEstimatedThroughput_cpm >= 1000.0 THEN
    dwStatusWord := dwStatusWord OR 16#0000_4000; (* Bit 14: High-Speed Production Rate Active *)
END_IF;

IF bCycleComplete_Sterile THEN
    dwStatusWord := dwStatusWord OR 16#0000_8000; (* Bit 15: Sterilization Cycle Validated Complete *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.6: US FDA 21 CFR PART 113 QUALITY & STERILITY WORD (dwQualitySterilityWord)
 * --------------------------------------------------------------------------------------------------------------------- *)
dwQualitySterilityWord := 16#0000_0000;

IF bTargetF0Reached THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0001; (* Bit 0: Minimum Inactivation F0 Achieved *)
END_IF;

IF bProcessDeviationActive THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0002; (* Bit 1: Process Thermal Deviation Logged *)
END_IF;

IF (rVoted_Temp_degC >= (rSet_SterilizationTemp_degC - 0.50)) AND (iFSM_CurrentState >= 4) THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0004; (* Bit 2: Temperature Cut-In Confirmed *)
END_IF;

IF (rInstantaneousLethalityRate_L > 0.010) THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0008; (* Bit 3: Active Sterilization Lethality Accrual *)
END_IF;

IF (ABS(rContainerDeltaP_bar) <= rSet_MaxCanDeltaP_bar) THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0010; (* Bit 4: Hermetic Container Structural Integrity OK *)
END_IF;

IF (rX_State[2] <= rSet_TargetCoolingTemp_degC) AND (iFSM_CurrentState >= 9) THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0020; (* Bit 5: Deep Chilldown Complete (< 40 deg C) *)
END_IF;

IF bEmergencyAbortActive THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0040; (* Bit 6: Batch Quarantined - Underprocessed *)
END_IF;

IF bCycleComplete_Sterile AND NOT bEmergencyAbortActive AND (rIntegratedF0_min >= rSet_TargetF0_min) THEN
    dwQualitySterilityWord := dwQualitySterilityWord OR 16#0000_0080; (* Bit 7: Batch Electronically Signed & Released *)
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * SUB-SECTION 5.7: FINAL ACTUATOR CLAMPING & SAFETY INTERLOCK ENFORCEMENT
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Strict Hardware Interlock Clamping *)
IF NOT bDI_SafetyDoorClosed_ZS1 OR NOT bDI_SafetyDoorLocked_ZS2 THEN
    rCmd_SteamModValve_pct := 0.0;
    rCmd_AirOverpressValve_pct := 0.0;
END_IF;

IF NOT bDI_EmergencyStop_PB THEN
    rCmd_SteamModValve_pct := 0.0;
    rCmd_AirOverpressValve_pct := 0.0;
    rCmd_RotaryDrumSpeed_RPM := 0.0;
    rCmd_DischargeConveyorSpeed_pct := 0.0;
END_IF;

(* Boundary Clamping of Modulating Actuator Outputs *)
IF rCmd_SteamModValve_pct < 0.0 THEN
    rCmd_SteamModValve_pct := 0.0;
ELSIF rCmd_SteamModValve_pct > 100.0 THEN
    rCmd_SteamModValve_pct := 100.0;
END_IF;

IF rCmd_AirOverpressValve_pct < 0.0 THEN
    rCmd_AirOverpressValve_pct := 0.0;
ELSIF rCmd_AirOverpressValve_pct > 100.0 THEN
    rCmd_AirOverpressValve_pct := 100.0;
END_IF;

IF rCmd_ExhaustVentValve_pct < 0.0 THEN
    rCmd_ExhaustVentValve_pct := 0.0;
ELSIF rCmd_ExhaustVentValve_pct > 100.0 THEN
    rCmd_ExhaustVentValve_pct := 100.0;
END_IF;

IF rCmd_CoolingWaterCascadeValve_pct < 0.0 THEN
    rCmd_CoolingWaterCascadeValve_pct := 0.0;
ELSIF rCmd_CoolingWaterCascadeValve_pct > 100.0 THEN
    rCmd_CoolingWaterCascadeValve_pct := 100.0;
END_IF;

IF rCmd_RotaryDrumSpeed_RPM < 0.0 THEN
    rCmd_RotaryDrumSpeed_RPM := 0.0;
ELSIF rCmd_RotaryDrumSpeed_RPM > 25.0 THEN
    rCmd_RotaryDrumSpeed_RPM := 25.0;
END_IF;

END_FUNCTION_BLOCK'''
