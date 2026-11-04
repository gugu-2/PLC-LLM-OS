# -*- coding: utf-8 -*-
"""
Builder module for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
Part 6: Phase 5 - ISA-18.2 Process Alarms & Diagnostic Bitmask Packing
"""

def get_phase5_alarms():
    code = """(* ============================================================================================================== *)
(* PHASE 5: ISA-18.2 PROCESS ALARMS & DIAGNOSTIC WORD BIT PACKING                                                 *)
(* ============================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------- *)
(* 5.1: MULTI-TIERED ALARM EVALUATION WITH DEADBAND HYSTERESIS                                                    *)
(* -------------------------------------------------------------------------------------------------------------- *)

(* Drum Bed Temperature Alarms *)
IF rVoted_DrumBedTemp_degC >= c_rTrip_DrumBedTemp_HI_HI THEN
    bAlarm_DrumBedTemp_HI_HI := TRUE;
ELSIF rVoted_DrumBedTemp_degC <= (c_rTrip_DrumBedTemp_HI_HI - c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_DrumBedTemp_HI_HI := FALSE;
END_IF;

IF rVoted_DrumBedTemp_degC >= c_rAlarm_DrumBedTemp_HI THEN
    bAlarm_DrumBedTemp_HI := TRUE;
ELSIF rVoted_DrumBedTemp_degC <= (c_rAlarm_DrumBedTemp_HI - c_rDeadband_Temperature) THEN
    bAlarm_DrumBedTemp_HI := FALSE;
END_IF;

IF rVoted_DrumBedTemp_degC <= c_rAlarm_DrumBedTemp_LO THEN
    bAlarm_DrumBedTemp_LO := TRUE;
ELSIF rVoted_DrumBedTemp_degC >= (c_rAlarm_DrumBedTemp_LO + c_rDeadband_Temperature) THEN
    bAlarm_DrumBedTemp_LO := FALSE;
END_IF;

IF rVoted_DrumBedTemp_degC <= c_rTrip_DrumBedTemp_LO_LO THEN
    bAlarm_DrumBedTemp_LO_LO := TRUE;
ELSIF rVoted_DrumBedTemp_degC >= (c_rTrip_DrumBedTemp_LO_LO + c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_DrumBedTemp_LO_LO := FALSE;
END_IF;

(* Slurry Header Pressure Alarms *)
IF rVoted_SlurryFeedPress_bar >= c_rTrip_SlurryPress_HI_HI THEN
    bAlarm_SlurryPress_HI_HI := TRUE;
ELSIF rVoted_SlurryFeedPress_bar <= (c_rTrip_SlurryPress_HI_HI - c_rDeadband_Pressure) AND bFaultReset THEN
    bAlarm_SlurryPress_HI_HI := FALSE;
END_IF;

IF rVoted_SlurryFeedPress_bar >= c_rAlarm_SlurryPress_HI THEN
    bAlarm_SlurryPress_HI := TRUE;
ELSIF rVoted_SlurryFeedPress_bar <= (c_rAlarm_SlurryPress_HI - c_rDeadband_Pressure) THEN
    bAlarm_SlurryPress_HI := FALSE;
END_IF;

IF rVoted_SlurryFeedPress_bar <= c_rAlarm_SlurryPress_LO THEN
    bAlarm_SlurryPress_LO := TRUE;
ELSIF rVoted_SlurryFeedPress_bar >= (c_rAlarm_SlurryPress_LO + c_rDeadband_Pressure) THEN
    bAlarm_SlurryPress_LO := FALSE;
END_IF;

IF rVoted_SlurryFeedPress_bar <= c_rTrip_SlurryPress_LO_LO THEN
    bAlarm_SlurryPress_LO_LO := TRUE;
ELSIF rVoted_SlurryFeedPress_bar >= (c_rTrip_SlurryPress_LO_LO + c_rDeadband_Pressure) AND bFaultReset THEN
    bAlarm_SlurryPress_LO_LO := FALSE;
END_IF;

(* Slurry Header Temperature Alarms *)
IF rVoted_SlurryFeedTemp_degC >= c_rTrip_SlurryTemp_HI_HI THEN
    bAlarm_SlurryTemp_HI_HI := TRUE;
ELSIF rVoted_SlurryFeedTemp_degC <= (c_rTrip_SlurryTemp_HI_HI - c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_SlurryTemp_HI_HI := FALSE;
END_IF;

IF rVoted_SlurryFeedTemp_degC >= c_rAlarm_SlurryTemp_HI THEN
    bAlarm_SlurryTemp_HI := TRUE;
ELSIF rVoted_SlurryFeedTemp_degC <= (c_rAlarm_SlurryTemp_HI - c_rDeadband_Temperature) THEN
    bAlarm_SlurryTemp_HI := FALSE;
END_IF;

IF rVoted_SlurryFeedTemp_degC <= c_rAlarm_SlurryTemp_LO THEN
    bAlarm_SlurryTemp_LO := TRUE;
ELSIF rVoted_SlurryFeedTemp_degC >= (c_rAlarm_SlurryTemp_LO + c_rDeadband_Temperature) THEN
    bAlarm_SlurryTemp_LO := FALSE;
END_IF;

IF rVoted_SlurryFeedTemp_degC <= c_rTrip_SlurryTemp_LO_LO THEN
    bAlarm_SlurryTemp_LO_LO := TRUE;
ELSIF rVoted_SlurryFeedTemp_degC >= (c_rTrip_SlurryTemp_LO_LO + c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_SlurryTemp_LO_LO := FALSE;
END_IF;

(* Drum Shell Hotspot Alarms *)
IF rVoted_DrumShellHotspot_degC >= c_rTrip_ShellHotspot_HI_HI THEN
    bAlarm_ShellHotspot_HI_HI := TRUE;
ELSIF rVoted_DrumShellHotspot_degC <= (c_rTrip_ShellHotspot_HI_HI - c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_ShellHotspot_HI_HI := FALSE;
END_IF;

IF rVoted_DrumShellHotspot_degC >= c_rAlarm_ShellHotspot_HI THEN
    bAlarm_ShellHotspot_HI := TRUE;
ELSIF rVoted_DrumShellHotspot_degC <= (c_rAlarm_ShellHotspot_HI - c_rDeadband_Temperature) THEN
    bAlarm_ShellHotspot_HI := FALSE;
END_IF;

(* Dryer Inlet Flue Gas Alarms *)
IF rVoted_DryerInletTemp_degC >= c_rTrip_DryerInletTemp_HI_HI THEN
    bAlarm_DryerInletTemp_HI_HI := TRUE;
ELSIF rVoted_DryerInletTemp_degC <= (c_rTrip_DryerInletTemp_HI_HI - c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_DryerInletTemp_HI_HI := FALSE;
END_IF;

IF rVoted_DryerInletTemp_degC >= c_rAlarm_DryerInletTemp_HI THEN
    bAlarm_DryerInletTemp_HI := TRUE;
ELSIF rVoted_DryerInletTemp_degC <= (c_rAlarm_DryerInletTemp_HI - c_rDeadband_Temperature) THEN
    bAlarm_DryerInletTemp_HI := FALSE;
END_IF;

(* Cooler Exit Granule Temperature Alarms *)
IF rVoted_CoolerZone4Temp_degC >= c_rTrip_CoolerExitTemp_HI_HI THEN
    bAlarm_CoolerExitTemp_HI_HI := TRUE;
ELSIF rVoted_CoolerZone4Temp_degC <= (c_rTrip_CoolerExitTemp_HI_HI - c_rDeadband_Temperature) AND bFaultReset THEN
    bAlarm_CoolerExitTemp_HI_HI := FALSE;
END_IF;

IF rVoted_CoolerZone4Temp_degC >= c_rAlarm_CoolerExitTemp_HI THEN
    bAlarm_CoolerExitTemp_HI := TRUE;
ELSIF rVoted_CoolerZone4Temp_degC <= (c_rAlarm_CoolerExitTemp_HI - c_rDeadband_Temperature) THEN
    bAlarm_CoolerExitTemp_HI := FALSE;
END_IF;

(* Venturi Scrubber Delta P Alarms *)
IF rVoted_VenturiDeltaP_mbar >= c_rTrip_ScrubberDeltaP_HI_HI THEN
    bAlarm_ScrubberDeltaP_HI_HI := TRUE;
ELSIF rVoted_VenturiDeltaP_mbar <= (c_rTrip_ScrubberDeltaP_HI_HI - c_rDeadband_DeltaP) AND bFaultReset THEN
    bAlarm_ScrubberDeltaP_HI_HI := FALSE;
END_IF;

IF rVoted_VenturiDeltaP_mbar >= c_rAlarm_ScrubberDeltaP_HI THEN
    bAlarm_ScrubberDeltaP_HI := TRUE;
ELSIF rVoted_VenturiDeltaP_mbar <= (c_rAlarm_ScrubberDeltaP_HI - c_rDeadband_DeltaP) THEN
    bAlarm_ScrubberDeltaP_HI := FALSE;
END_IF;

IF rVoted_VenturiDeltaP_mbar <= c_rAlarm_ScrubberDeltaP_LO THEN
    bAlarm_ScrubberDeltaP_LO := TRUE;
ELSIF rVoted_VenturiDeltaP_mbar >= (c_rAlarm_ScrubberDeltaP_LO + c_rDeadband_DeltaP) THEN
    bAlarm_ScrubberDeltaP_LO := FALSE;
END_IF;

IF rVoted_VenturiDeltaP_mbar <= c_rTrip_ScrubberDeltaP_LO_LO THEN
    bAlarm_ScrubberDeltaP_LO_LO := TRUE;
ELSIF rVoted_VenturiDeltaP_mbar >= (c_rTrip_ScrubberDeltaP_LO_LO + c_rDeadband_DeltaP) AND bFaultReset THEN
    bAlarm_ScrubberDeltaP_LO_LO := FALSE;
END_IF;

(* Scrubber Liquor pH Alarms *)
IF rVoted_Scrubber_pH <= c_rTrip_Scrubber_pH_LO_LO THEN
    bAlarm_Scrubber_pH_LO_LO := TRUE;
ELSIF rVoted_Scrubber_pH >= (c_rTrip_Scrubber_pH_LO_LO + c_rDeadband_pH) AND bFaultReset THEN
    bAlarm_Scrubber_pH_LO_LO := FALSE;
END_IF;

IF rVoted_Scrubber_pH <= c_rAlarm_Scrubber_pH_LO THEN
    bAlarm_Scrubber_pH_LO := TRUE;
ELSIF rVoted_Scrubber_pH >= (c_rAlarm_Scrubber_pH_LO + c_rDeadband_pH) THEN
    bAlarm_Scrubber_pH_LO := FALSE;
END_IF;

IF rVoted_Scrubber_pH >= c_rAlarm_Scrubber_pH_HI THEN
    bAlarm_Scrubber_pH_HI := TRUE;
ELSIF rVoted_Scrubber_pH <= (c_rAlarm_Scrubber_pH_HI - c_rDeadband_pH) THEN
    bAlarm_Scrubber_pH_HI := FALSE;
END_IF;

IF rVoted_Scrubber_pH >= c_rTrip_Scrubber_pH_HI_HI THEN
    bAlarm_Scrubber_pH_HI_HI := TRUE;
ELSIF rVoted_Scrubber_pH <= (c_rTrip_Scrubber_pH_HI_HI - c_rDeadband_pH) AND bFaultReset THEN
    bAlarm_Scrubber_pH_HI_HI := FALSE;
END_IF;

(* Stack Emission Alarms *)
IF rVoted_StackDust_mgNm3 >= c_rTrip_StackDust_HI_HI THEN
    bAlarm_StackDust_HI_HI := TRUE;
ELSIF rVoted_StackDust_mgNm3 <= (c_rTrip_StackDust_HI_HI - c_rDeadband_StackDust) AND bFaultReset THEN
    bAlarm_StackDust_HI_HI := FALSE;
END_IF;

IF rVoted_StackDust_mgNm3 >= c_rAlarm_StackDust_HI THEN
    bAlarm_StackDust_HI := TRUE;
ELSIF rVoted_StackDust_mgNm3 <= (c_rAlarm_StackDust_HI - c_rDeadband_StackDust) THEN
    bAlarm_StackDust_HI := FALSE;
END_IF;

IF rVoted_StackAmmoniaSlip_ppmv >= c_rTrip_AmmoniaSlip_HI_HI THEN
    bAlarm_AmmoniaSlip_HI_HI := TRUE;
ELSIF rVoted_StackAmmoniaSlip_ppmv <= (c_rTrip_AmmoniaSlip_HI_HI - 1.00) AND bFaultReset THEN
    bAlarm_AmmoniaSlip_HI_HI := FALSE;
END_IF;

IF rVoted_StackAmmoniaSlip_ppmv >= c_rAlarm_AmmoniaSlip_HI THEN
    bAlarm_AmmoniaSlip_HI := TRUE;
ELSIF rVoted_StackAmmoniaSlip_ppmv <= (c_rAlarm_AmmoniaSlip_HI - 1.00) THEN
    bAlarm_AmmoniaSlip_HI := FALSE;
END_IF;

(* Thermal Rate of Rise Trip *)
IF rBedTempDerivFiltered_degCps >= c_rMaxAllowableRateOfRise_degCps THEN
    bAlarm_ThermalRateOfRise_Trip := TRUE;
ELSIF rBedTempDerivFiltered_degCps < 0.200 AND bFaultReset THEN
    bAlarm_ThermalRateOfRise_Trip := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------- *)
(* 5.2: ISA-18.2 TELEMETRY BITMASK WORD COMPILATION                                                               *)
(* -------------------------------------------------------------------------------------------------------------- *)

(* Word 1: Priority 1 Critical Plant Safety Trips *)
wAlarmWord_Critical_ISA18 := 16#00000000;
IF bAlarm_DrumBedTemp_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000001; END_IF;
IF bAlarm_DrumBedTemp_LO_LO       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000002; END_IF;
IF bAlarm_SlurryPress_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000004; END_IF;
IF bAlarm_SlurryPress_LO_LO       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000008; END_IF;
IF bAlarm_SlurryTemp_HI_HI        THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000010; END_IF;
IF bAlarm_SlurryTemp_LO_LO        THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000020; END_IF;
IF bAlarm_ShellHotspot_HI_HI      THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000040; END_IF;
IF bAlarm_DryerInletTemp_HI_HI    THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000080; END_IF;
IF bAlarm_BurnerFlameLoss_Trip     THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000100; END_IF;
IF bAlarm_CoolerExitTemp_HI_HI    THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000200; END_IF;
IF bAlarm_ScrubberDeltaP_HI_HI    THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000400; END_IF;
IF bAlarm_ScrubberDeltaP_LO_LO    THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00000800; END_IF;
IF bAlarm_Scrubber_pH_LO_LO       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00001000; END_IF;
IF bAlarm_Scrubber_pH_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00002000; END_IF;
IF bAlarm_StackDust_HI_HI         THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00004000; END_IF;
IF bAlarm_AmmoniaSlip_HI_HI       THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00008000; END_IF;
IF bAlarm_ThermalRateOfRise_Trip  THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00010000; END_IF;
IF bRunawayDecompositionTripped   THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00020000; END_IF;
IF bEmergencyDelugeActive         THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#00040000; END_IF;
IF NOT bSafetyCircuitHealthy_NC   THEN wAlarmWord_Critical_ISA18 := wAlarmWord_Critical_ISA18 OR 16#80000000; END_IF;

(* Word 2: Priority 2 Process Deviations & Warnings *)
wAlarmWord_Warning_ISA18 := 16#00000000;
IF bAlarm_DrumBedTemp_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000001; END_IF;
IF bAlarm_DrumBedTemp_LO          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000002; END_IF;
IF bAlarm_SlurryPress_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000004; END_IF;
IF bAlarm_SlurryPress_LO          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000008; END_IF;
IF bAlarm_SlurryTemp_HI           THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000010; END_IF;
IF bAlarm_SlurryTemp_LO           THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000020; END_IF;
IF bAlarm_ShellHotspot_HI         THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000040; END_IF;
IF bAlarm_DryerInletTemp_HI       THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000080; END_IF;
IF bAlarm_CoolerExitTemp_HI       THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000100; END_IF;
IF bAlarm_ScrubberDeltaP_HI       THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000200; END_IF;
IF bAlarm_ScrubberDeltaP_LO       THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000400; END_IF;
IF bAlarm_Scrubber_pH_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00000800; END_IF;
IF bAlarm_Scrubber_pH_LO          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00001000; END_IF;
IF bAlarm_StackDust_HI            THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00002000; END_IF;
IF bAlarm_AmmoniaSlip_HI          THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00004000; END_IF;
IF bAlarm_TMR_MajorDegraded_Warn  THEN wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00008000; END_IF;
IF rCalc_CalculatedRecycleRatio < 2.0 OR rCalc_CalculatedRecycleRatio > 4.5 THEN
    wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00010000;
END_IF;
IF rCalc_EstimatedCrushStrength_N < rSet_MinCrushStrength_N THEN
    wAlarmWord_Warning_ISA18 := wAlarmWord_Warning_ISA18 OR 16#00020000;
END_IF;

(* Word 3: 2oo3 TMR Triplet Health & Discrepancy Bitmask *)
wDiagnosticMask_TMR_Health := 16#00000000;
IF bIso_BedTemp_ChA OR bIso_BedTemp_ChB OR bIso_BedTemp_ChC               THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000001; END_IF;
IF bIso_SlurryPress_ChA OR bIso_SlurryPress_ChB OR bIso_SlurryPress_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000002; END_IF;
IF bIso_SlurryTemp_ChA OR bIso_SlurryTemp_ChB OR bIso_SlurryTemp_ChC       THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000004; END_IF;
IF bIso_ShellHotspot_ChA OR bIso_ShellHotspot_ChB OR bIso_ShellHotspot_ChC THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000008; END_IF;
IF bIso_DryerInletTemp_ChA OR bIso_DryerInletTemp_ChB OR bIso_DryerInletTemp_ChC THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000010; END_IF;
IF bIso_BurnerGasFlow_ChA OR bIso_BurnerGasFlow_ChB OR bIso_BurnerGasFlow_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000020; END_IF;
IF bIso_BurnerAirFlow_ChA OR bIso_BurnerAirFlow_ChB OR bIso_BurnerAirFlow_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000040; END_IF;
IF bIso_BurnerFlame_ChA OR bIso_BurnerFlame_ChB OR bIso_BurnerFlame_ChC       THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000080; END_IF;
IF bIso_CoolerTemp_ChA OR bIso_CoolerTemp_ChB OR bIso_CoolerTemp_ChC       THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000100; END_IF;
IF bIso_CoolerPlenum_ChA OR bIso_CoolerPlenum_ChB OR bIso_CoolerPlenum_ChC THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000200; END_IF;
IF bIso_RecycleFlow_ChA OR bIso_RecycleFlow_ChB OR bIso_RecycleFlow_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000400; END_IF;
IF bIso_ProductFlow_ChA OR bIso_ProductFlow_ChB OR bIso_ProductFlow_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00000800; END_IF;
IF bIso_VenturiDeltaP_ChA OR bIso_VenturiDeltaP_ChB OR bIso_VenturiDeltaP_ChC THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00001000; END_IF;
IF bIso_Scrubber_pH_ChA OR bIso_Scrubber_pH_ChB OR bIso_Scrubber_pH_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00002000; END_IF;
IF bIso_StackDust_ChA OR bIso_StackDust_ChB OR bIso_StackDust_ChC       THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00004000; END_IF;
IF bIso_AmmoniaSlip_ChA OR bIso_AmmoniaSlip_ChB OR bIso_AmmoniaSlip_ChC   THEN wDiagnosticMask_TMR_Health := wDiagnosticMask_TMR_Health OR 16#00008000; END_IF;

(* Word 4: Complex Operational Readiness Word *)
wPlantSubsystemStatus := 16#00000000;
IF bMasterAutoEnable              THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000001; END_IF;
IF bSafetyCircuitHealthy_NC       THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000002; END_IF;
IF bNitrogenPurgePermissive       THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000004; END_IF;
IF bBoilerSteamHeaderReady        THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000008; END_IF;
IF bNaturalGasHeaderReady         THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000010; END_IF;
IF bDelugeWaterSupplyReady        THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000020; END_IF;
IF bEmergencyPowerAvailable       THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000040; END_IF;
IF bPlantInProduction             THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000080; END_IF;
IF rVoted_BurnerFlameIntensity_pct >= 80.0 THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000100; END_IF;
IF rVoted_VenturiDeltaP_mbar >= 40.0       THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000200; END_IF;
IF rCalc_EstimatedCrushStrength_N >= rSet_MinCrushStrength_N THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000400; END_IF;
IF rCalc_EstimatedGranuleMoisture_pct <= rSet_DryerOutletMoistureMax_pct * 3.5 THEN wPlantSubsystemStatus := wPlantSubsystemStatus OR 16#00000800; END_IF;

END_FUNCTION_BLOCK
"""
    return code
