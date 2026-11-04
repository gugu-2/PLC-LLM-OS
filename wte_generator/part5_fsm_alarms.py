# part5_fsm_alarms.py

def get_part5_fsm_alarms():
    return """(* =====================================================================================================================
 * PHASE 5: HYDRAULIC STOKER JAM DETECTION & FAST REVERSE CLEARANCE SUBROUTINE
 * ===================================================================================================================== *)

(* Zone 1 Stoker Hydraulic Jam Supervision *)
IF rGrateHydraulicPressure_Zone1_bar > c_rGrateHydraulicJamPressure_bar THEN
    IF NOT bGrateInReverse_Zone1 THEN
        bGrateInReverse_Zone1 := TRUE;
        rGrateReverseTimer_Zone1_s := 0.0;
        iGrateJamRetryCount_Zone1 := iGrateJamRetryCount_Zone1 + 1;
        bGrateHydraulicJamReverse := TRUE;
    END_IF;
END_IF;

IF bGrateInReverse_Zone1 THEN
    rGrateReverseTimer_Zone1_s := rGrateReverseTimer_Zone1_s + c_rTs;
    rGrateSpeedCmd_Zone1_strokes_h := -25.0; (* Fast reverse motion *)
    IF rGrateReverseTimer_Zone1_s >= c_rGrateReverseStrokeTime_s THEN
        bGrateInReverse_Zone1 := FALSE;
        rGrateReverseTimer_Zone1_s := 0.0;
        IF iGrateJamRetryCount_Zone1 >= 3 THEN
            bTripLatch_GrateJam_Zone1 := TRUE;
            dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0100; (* Bit 8: Zone 1 Jam Persistent Trip *)
        END_IF;
    END_IF;
END_IF;

(* Zone 2 Stoker Hydraulic Jam Supervision *)
IF rGrateHydraulicPressure_Zone2_bar > c_rGrateHydraulicJamPressure_bar THEN
    IF NOT bGrateInReverse_Zone2 THEN
        bGrateInReverse_Zone2 := TRUE;
        rGrateReverseTimer_Zone2_s := 0.0;
        iGrateJamRetryCount_Zone2 := iGrateJamRetryCount_Zone2 + 1;
        bGrateHydraulicJamReverse := TRUE;
    END_IF;
END_IF;

IF bGrateInReverse_Zone2 THEN
    rGrateReverseTimer_Zone2_s := rGrateReverseTimer_Zone2_s + c_rTs;
    rGrateSpeedCmd_Zone2_strokes_h := -25.0;
    IF rGrateReverseTimer_Zone2_s >= c_rGrateReverseStrokeTime_s THEN
        bGrateInReverse_Zone2 := FALSE;
        rGrateReverseTimer_Zone2_s := 0.0;
        IF iGrateJamRetryCount_Zone2 >= 3 THEN
            bTripLatch_GrateJam_Zone2 := TRUE;
            dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0200; (* Bit 9: Zone 2 Jam Persistent Trip *)
        END_IF;
    END_IF;
END_IF;

(* Zone 3 Stoker Hydraulic Jam Supervision *)
IF rGrateHydraulicPressure_Zone3_bar > c_rGrateHydraulicJamPressure_bar THEN
    IF NOT bGrateInReverse_Zone3 THEN
        bGrateInReverse_Zone3 := TRUE;
        rGrateReverseTimer_Zone3_s := 0.0;
        iGrateJamRetryCount_Zone3 := iGrateJamRetryCount_Zone3 + 1;
        bGrateHydraulicJamReverse := TRUE;
    END_IF;
END_IF;

IF bGrateInReverse_Zone3 THEN
    rGrateReverseTimer_Zone3_s := rGrateReverseTimer_Zone3_s + c_rTs;
    rGrateSpeedCmd_Zone3_strokes_h := -25.0;
    IF rGrateReverseTimer_Zone3_s >= c_rGrateReverseStrokeTime_s THEN
        bGrateInReverse_Zone3 := FALSE;
        rGrateReverseTimer_Zone3_s := 0.0;
        IF iGrateJamRetryCount_Zone3 >= 3 THEN
            bTripLatch_GrateJam_Zone3 := TRUE;
            dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0400; (* Bit 10: Zone 3 Jam Persistent Trip *)
        END_IF;
    END_IF;
END_IF;

(* Zone 4 Stoker Hydraulic Jam Supervision *)
IF rGrateHydraulicPressure_Zone4_bar > c_rGrateHydraulicJamPressure_bar THEN
    IF NOT bGrateInReverse_Zone4 THEN
        bGrateInReverse_Zone4 := TRUE;
        rGrateReverseTimer_Zone4_s := 0.0;
        iGrateJamRetryCount_Zone4 := iGrateJamRetryCount_Zone4 + 1;
        bGrateHydraulicJamReverse := TRUE;
    END_IF;
END_IF;

IF bGrateInReverse_Zone4 THEN
    rGrateReverseTimer_Zone4_s := rGrateReverseTimer_Zone4_s + c_rTs;
    rGrateSpeedCmd_Zone4_strokes_h := -20.0;
    IF rGrateReverseTimer_Zone4_s >= c_rGrateReverseStrokeTime_s THEN
        bGrateInReverse_Zone4 := FALSE;
        rGrateReverseTimer_Zone4_s := 0.0;
        IF iGrateJamRetryCount_Zone4 >= 3 THEN
            bTripLatch_GrateJam_Zone4 := TRUE;
            dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0800; (* Bit 11: Zone 4 Jam Persistent Trip *)
        END_IF;
    END_IF;
END_IF;

IF NOT bGrateInReverse_Zone1 AND NOT bGrateInReverse_Zone2 AND NOT bGrateInReverse_Zone3 AND NOT bGrateInReverse_Zone4 THEN
    bGrateHydraulicJamReverse := FALSE;
END_IF;

(* =====================================================================================================================
 * PHASE 6: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
 * ===================================================================================================================== *)

(* State Transition Memory & Dwell Timer Accumulation *)
IF iFSM_State = iFSM_PrevState THEN
    rStateTimer_s := rStateTimer_s + c_rTs;
    bStateEntry := FALSE;
ELSE
    rStateTimer_s := 0.0;
    bStateEntry := TRUE;
    iFSM_PrevState := iFSM_State;
END_IF;

CASE iFSM_State OF

    (* -----------------------------------------------------------------------------------------------------------------
     * State 1: SYSTEM_OFFLINE_COLD_INSPECTION
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        wFSM_CurrentState := 16#0001;
        bSystemReady := FALSE;
        rGrateSpeedCmd_Zone1_strokes_h := 0.0;
        rGrateSpeedCmd_Zone2_strokes_h := 0.0;
        rGrateSpeedCmd_Zone3_strokes_h := 0.0;
        rGrateSpeedCmd_Zone4_strokes_h := 0.0;
        rPrimaryAirDamperCmd_pct := 0.0;
        rSecondaryAirDamperCmd_pct := 0.0;
        rPrimaryAirFanRPMCmd_rpm := 0.0;
        rSecondaryAirFanRPMCmd_rpm := 0.0;
        rIDF_FanSpeedCmd_rpm := 0.0;
        rUreaDosingPumpSpeedCmd_pct := 0.0;
        rLimeSlurryFeedPumpCmd_pct := 0.0;
        rActivatedCarbonFeederCmd_kgh := 0.0;
        rAuxiliaryBurnerFiringRate_pct := 0.0;

        IF bEnable AND bStartAutoIncineration AND bIDFanRunningPermissive THEN
            iFSM_State := 2; (* Transition to REFRACTORY_PREHEAT_AUX_BURNER *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 2: REFRACTORY_PREHEAT_AUX_BURNER
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        wFSM_CurrentState := 16#0002;
        bSystemReady := FALSE;
        rIDF_FanSpeedCmd_rpm := 650.0; (* Maintain -2.5 mbar furnace draft *)
        rPrimaryAirDamperCmd_pct := 15.0;
        rPrimaryAirFanRPMCmd_rpm := 350.0;
        rSecondaryAirDamperCmd_pct := 0.0;
        rAuxiliaryBurnerFiringRate_pct := LIMIT(20.0, 20.0 + rStateTimer_s * 0.05, 100.0);

        (* Hold until combustion refractory reaches >= 850 °C per statutory requirement *)
        IF (rCombustionChamberTempVoted_degC >= 850.0) AND (rPostCombustion2SecTempVoted_degC >= 850.0) THEN
            iFSM_State := 3; (* Transition to WASTE_FEED_CHUTE_PRIME *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 3: WASTE_FEED_CHUTE_PRIME
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        wFSM_CurrentState := 16#0003;
        rIDF_FanSpeedCmd_rpm := 750.0;
        rAuxiliaryBurnerFiringRate_pct := 80.0;
        rGrateSpeedCmd_Zone1_strokes_h := 15.0; (* Feed ram prime *)
        rPrimaryAirDamperCmd_pct := 25.0;
        rPrimaryAirFanRPMCmd_rpm := 500.0;

        IF rStateTimer_s >= 180.0 THEN (* Chute loaded and waste bed front established *)
            iFSM_State := 4; (* Transition to GRATE_IGNITION_BED_ESTABLISH *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 4: GRATE_IGNITION_BED_ESTABLISH
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        wFSM_CurrentState := 16#0004;
        rGrateSpeedCmd_Zone1_strokes_h := 22.0;
        rGrateSpeedCmd_Zone2_strokes_h := 18.0;
        rGrateSpeedCmd_Zone3_strokes_h := 0.0;
        rGrateSpeedCmd_Zone4_strokes_h := 0.0;
        rPrimaryAirDamperCmd_pct := 45.0;
        rPrimaryAirFanRPMCmd_rpm := 750.0;
        rAuxiliaryBurnerFiringRate_pct := 60.0;

        IF (rCombustionChamberTempVoted_degC >= 920.0) AND (rStateTimer_s >= 240.0) THEN
            iFSM_State := 5; (* Transition to SECONDARY_AIR_O2_STABILIZATION *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 5: SECONDARY_AIR_O2_STABILIZATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        wFSM_CurrentState := 16#0005;
        rGrateSpeedCmd_Zone1_strokes_h := 30.0;
        rGrateSpeedCmd_Zone2_strokes_h := 25.0;
        rGrateSpeedCmd_Zone3_strokes_h := 20.0;
        rGrateSpeedCmd_Zone4_strokes_h := 12.0;
        rPrimaryAirDamperCmd_pct := 60.0;
        rPrimaryAirFanRPMCmd_rpm := 950.0;
        rSecondaryAirDamperCmd_pct := 40.0;
        rSecondaryAirFanRPMCmd_rpm := 1150.0;
        rAuxiliaryBurnerFiringRate_pct := 25.0;

        IF (AIT_STACK_O2_404A >= 5.5) AND (rPostCombustion2SecTempVoted_degC >= 950.0) THEN
            iFSM_State := 6; (* Transition to FULL_LOAD_AUTONOMOUS_INCINERATION *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 6: FULL_LOAD_AUTONOMOUS_INCINERATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        wFSM_CurrentState := 16#0006;
        bSystemReady := TRUE;
        rAuxiliaryBurnerFiringRate_pct := 0.0; (* Self-sustaining mass-burn *)

        (* Base Stoker Speeds Modulated by MPC au_control *)
        IF NOT bGrateInReverse_Zone1 THEN rGrateSpeedCmd_Zone1_strokes_h := LIMIT(15.0, 38.5 + au_control[1], 55.0); END_IF;
        IF NOT bGrateInReverse_Zone2 THEN rGrateSpeedCmd_Zone2_strokes_h := LIMIT(12.0, 32.0 + au_control[2], 48.0); END_IF;
        IF NOT bGrateInReverse_Zone3 THEN rGrateSpeedCmd_Zone3_strokes_h := LIMIT(10.0, 28.0 + au_control[2], 42.0); END_IF;
        IF NOT bGrateInReverse_Zone4 THEN rGrateSpeedCmd_Zone4_strokes_h := LIMIT(8.0, 18.0 + au_control[3], 30.0); END_IF;

        (* Combustion Air Staged Modulation *)
        rPrimaryAirDamperCmd_pct := LIMIT(30.0, 70.0 + (au_control[4] / 100.0), 95.0);
        rPrimaryAirFanRPMCmd_rpm := LIMIT(600.0, 1150.0 + (au_control[4] * 0.05), 1450.0);
        rSecondaryAirDamperCmd_pct := LIMIT(25.0, 55.0 + (au_control[5] / 80.0), 90.0);
        rSecondaryAirFanRPMCmd_rpm := LIMIT(700.0, 1280.0 + (au_control[5] * 0.06), 1480.0);

        (* Active DeNOx and Scrubbing Coordination *)
        IF rStackNOxVoted_mgNm3 > 60.0 THEN
            iFSM_State := 7; (* Transition to DENOX_AMMONIA_OPTIMIZATION *)
        ELSIF (rStackSO2Voted_mgNm3 > 30.0) OR (rFlueGasHClVoted_mgNm3 > 8.0) THEN
            iFSM_State := 8; (* Transition to ACID_GAS_SCRUBBER_TRIM *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 7: DENOX_AMMONIA_OPTIMIZATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        wFSM_CurrentState := 16#0007;
        bSystemReady := TRUE;
        (* SNCR Multi-Level Aqueous Urea Injection Pacing *)
        rUreaDosingPumpSpeedCmd_pct := LIMIT(10.0, 55.0 + au_control[6] * 0.8, 95.0);

        IF (rStackNOxVoted_mgNm3 <= 62.0) AND (rStackNH3SlipVoted_mgNm3 <= 2.0) THEN
            iFSM_State := 6; (* Return to FULL_LOAD_AUTONOMOUS_INCINERATION *)
        ELSIF (rStackSO2Voted_mgNm3 > 35.0) THEN
            iFSM_State := 8; (* Branch to ACID_GAS_SCRUBBER_TRIM *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 8: ACID_GAS_SCRUBBER_TRIM
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        wFSM_CurrentState := 16#0008;
        bSystemReady := TRUE;
        rLimeSlurryAtomizerSpeedCmd_rpm := 12500.0; (* High atomization velocity *)
        rLimeSlurryFeedPumpCmd_pct := LIMIT(15.0, 62.0 + au_control[7] * 0.6, 98.0);
        rActivatedCarbonFeederCmd_kgh := LIMIT(10.0, 32.5 + au_control[8], 65.0);

        IF (rStackSO2Voted_mgNm3 <= 26.0) AND (rFlueGasHClVoted_mgNm3 <= 6.8) THEN
            iFSM_State := 6; (* Return to FULL_LOAD_AUTONOMOUS_INCINERATION *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 9: SLAG_DISCHARGE_EXTRACTOR_SYNC
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        wFSM_CurrentState := 16#0009;
        (* Synchronize Zone 4 char discharge with submerged ash extractor *)
        IF NOT bSlagExtractorRunning THEN
            rGrateSpeedCmd_Zone4_strokes_h := 0.0; (* Pause ash dumping to prevent hopper choking *)
        ELSE
            rGrateSpeedCmd_Zone4_strokes_h := 18.0;
            iFSM_State := 6;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 10: CONTROLLED_BURN_OUT_SHUTDOWN
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        wFSM_CurrentState := 16#000A;
        bSystemReady := FALSE;
        rGrateSpeedCmd_Zone1_strokes_h := 0.0; (* Stop feeding new MSW *)
        rGrateSpeedCmd_Zone2_strokes_h := 15.0;
        rGrateSpeedCmd_Zone3_strokes_h := 20.0;
        rGrateSpeedCmd_Zone4_strokes_h := 25.0; (* Clear existing char bed *)
        rControlledShutdownTimer_s := rControlledShutdownTimer_s + c_rTs;

        IF rControlledShutdownTimer_s >= 7200.0 THEN (* 2 hours burnout completed *)
            iFSM_State := 1; (* Return to OFFLINE *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 11: EMERGENCY_FEED_CUT_SMOKE_STOP
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        wFSM_CurrentState := 16#000B;
        bSystemReady := FALSE;
        rGrateSpeedCmd_Zone1_strokes_h := 0.0;
        rGrateSpeedCmd_Zone2_strokes_h := 0.0;
        rGrateSpeedCmd_Zone3_strokes_h := 0.0;
        rGrateSpeedCmd_Zone4_strokes_h := 0.0;
        rPrimaryAirDamperCmd_pct := 10.0;
        rSecondaryAirDamperCmd_pct := 0.0;
        rPrimaryAirFanRPMCmd_rpm := 250.0;
        rSecondaryAirFanRPMCmd_rpm := 0.0;
        rUreaDosingPumpSpeedCmd_pct := 0.0;
        rLimeSlurryFeedPumpCmd_pct := 25.0; (* Maintain acid scrub *)
        rActivatedCarbonFeederCmd_kgh := 0.0;
        rAuxiliaryBurnerFiringRate_pct := 0.0;
        rIDF_FanSpeedCmd_rpm := 600.0; (* Maintain negative pressure to evacuate toxic gases *)

        IF bResetFault AND bEnable THEN
            iFSM_State := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * State 12: SAFETY_INTERRUPT_ID_FAN_RUNAWAY
     * ----------------------------------------------------------------------------------------------------------------- *)
    12:
        wFSM_CurrentState := 16#000C;
        bSystemReady := FALSE;
        rGrateSpeedCmd_Zone1_strokes_h := 0.0;
        rGrateSpeedCmd_Zone2_strokes_h := 0.0;
        rGrateSpeedCmd_Zone3_strokes_h := 0.0;
        rGrateSpeedCmd_Zone4_strokes_h := 0.0;
        rPrimaryAirFanRPMCmd_rpm := 0.0;
        rSecondaryAirFanRPMCmd_rpm := 0.0;
        rIDF_FanSpeedCmd_rpm := 0.0;
        rPrimaryAirDamperCmd_pct := 0.0;
        rSecondaryAirDamperCmd_pct := 0.0;
        rUreaDosingPumpSpeedCmd_pct := 0.0;
        rLimeSlurryFeedPumpCmd_pct := 0.0;
        rActivatedCarbonFeederCmd_kgh := 0.0;
        rAuxiliaryBurnerFiringRate_pct := 0.0;

        IF bResetFault AND bIDFanRunningPermissive THEN
            iFSM_State := 1;
        END_IF;

END_CASE;

(* =====================================================================================================================
 * PHASE 7: ISA-18.2 MULTI-TIERED PROCESS ALARM LADDER & FAST LEGAL BREACH TRIP (< 1.0 s)
 * ===================================================================================================================== *)

(* Compute Rate-of-Change (ROC) *)
rROC_CombTemp_degCs := (rCombustionChamberTempVoted_degC - rPrevROC_CombTemp) / c_rTs;
rROC_PostCombTemp_degCs := (rPostCombustion2SecTempVoted_degC - rPrevROC_PostCombTemp) / c_rTs;
rROC_StackNOx_mgNm3s := (rStackNOxVoted_mgNm3 - rPrevROC_StackNOx) / c_rTs;
rROC_Draft_mbars := (PT_FURNACE_DRAFT_103A - rPrevROC_Draft) / c_rTs;

rPrevROC_CombTemp := rCombustionChamberTempVoted_degC;
rPrevROC_PostCombTemp := rPostCombustion2SecTempVoted_degC;
rPrevROC_StackNOx := rStackNOxVoted_mgNm3;
rPrevROC_Draft := PT_FURNACE_DRAFT_103A;

(* 7.1 Statutory Temperature Alarms (EU Directive 2010/75/EU Floor 850.0 °C) *)
IF rPostCombustion2SecTempVoted_degC < c_rTrip_PostCombTemp_LO_LO THEN
    IF rBreachAccumulator_Temp_s >= 1.0 THEN
        bTripLatch_PostComb_LO_LO := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0001; (* Bit 0: Statutory 850 °C Temperature Breach Trip *)
    END_IF;
ELSIF rPostCombustion2SecTempVoted_degC < c_rWarn_PostCombTemp_LO THEN
    bWarnLatch_PostComb_LO := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0001; (* Bit 0: Post-Comb Low Warning *)
ELSE
    bWarnLatch_PostComb_LO := FALSE;
END_IF;

IF rPostCombustion2SecTempVoted_degC > c_rTrip_PostCombTemp_HI_HI THEN
    bTripLatch_PostComb_HI_HI := TRUE;
    dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0002; (* Bit 1: Refractory Slagging Redline Trip *)
ELSIF rPostCombustion2SecTempVoted_degC > c_rWarn_PostCombTemp_HI THEN
    bWarnLatch_PostComb_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0002; (* Bit 1: Post-Comb High Warning *)
ELSE
    bWarnLatch_PostComb_HI := FALSE;
END_IF;

(* 7.2 Legal Emission Exceedance Alarms with Fast < 1.0 s Latching Trip *)
(* Clean Stack NOx Limit: 80.0 mg/Nm3 *)
IF rStackNOxVoted_mgNm3 > c_rTrip_StackNOx_HI_HI THEN
    rBreachAccumulator_NOx_s := rBreachAccumulator_NOx_s + c_rTs;
    IF rBreachAccumulator_NOx_s >= 0.50 THEN
        bTripLatch_StackNOx_HI_HI := TRUE;
        bLegalEmissionBreachTrip := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0004; (* Bit 2: NOx Legal Breach Trip *)
    END_IF;
ELSIF rStackNOxVoted_mgNm3 > c_rWarn_StackNOx_HI THEN
    bWarnLatch_StackNOx_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0004; (* Bit 2: NOx High Warning *)
    rBreachAccumulator_NOx_s := 0.0;
ELSE
    bWarnLatch_StackNOx_HI := FALSE;
    rBreachAccumulator_NOx_s := 0.0;
END_IF;

(* Stack NH3 Slip Limit: 3.0 mg/Nm3 *)
IF rStackNH3SlipVoted_mgNm3 > c_rTrip_StackNH3_HI_HI THEN
    rBreachAccumulator_NH3_s := rBreachAccumulator_NH3_s + c_rTs;
    IF rBreachAccumulator_NH3_s >= 0.50 THEN
        bTripLatch_StackNH3_HI_HI := TRUE;
        bLegalEmissionBreachTrip := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0008; (* Bit 3: Ammonia Slip Legal Breach Trip *)
    END_IF;
ELSIF rStackNH3SlipVoted_mgNm3 > c_rWarn_StackNH3_HI THEN
    bWarnLatch_StackNH3_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0008; (* Bit 3: NH3 Slip High Warning *)
    rBreachAccumulator_NH3_s := 0.0;
ELSE
    bWarnLatch_StackNH3_HI := FALSE;
    rBreachAccumulator_NH3_s := 0.0;
END_IF;

(* Stack SO2 Limit: 50.0 mg/Nm3 *)
IF rStackSO2Voted_mgNm3 > c_rTrip_StackSO2_HI_HI THEN
    rBreachAccumulator_SO2_s := rBreachAccumulator_SO2_s + c_rTs;
    IF rBreachAccumulator_SO2_s >= 0.50 THEN
        bTripLatch_StackSO2_HI_HI := TRUE;
        bLegalEmissionBreachTrip := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0010; (* Bit 4: SO2 Legal Breach Trip *)
    END_IF;
ELSIF rStackSO2Voted_mgNm3 > c_rWarn_StackSO2_HI THEN
    bWarnLatch_StackSO2_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0010; (* Bit 4: SO2 High Warning *)
    rBreachAccumulator_SO2_s := 0.0;
ELSE
    bWarnLatch_StackSO2_HI := FALSE;
    rBreachAccumulator_SO2_s := 0.0;
END_IF;

(* Stack HCl Limit: 10.0 mg/Nm3 *)
IF rFlueGasHClVoted_mgNm3 > c_rTrip_StackHCl_HI_HI THEN
    rBreachAccumulator_HCl_s := rBreachAccumulator_HCl_s + c_rTs;
    IF rBreachAccumulator_HCl_s >= 0.50 THEN
        bTripLatch_StackHCl_HI_HI := TRUE;
        bLegalEmissionBreachTrip := TRUE;
        dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0020; (* Bit 5: HCl Legal Breach Trip *)
    END_IF;
ELSIF rFlueGasHClVoted_mgNm3 > c_rWarn_StackHCl_HI THEN
    bWarnLatch_StackHCl_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0020; (* Bit 5: HCl High Warning *)
    rBreachAccumulator_HCl_s := 0.0;
ELSE
    bWarnLatch_StackHCl_HI := FALSE;
    rBreachAccumulator_HCl_s := 0.0;
END_IF;

(* 7.3 Furnace Draft Implosion & Positive Pressure Protection *)
IF PT_FURNACE_DRAFT_103A > c_rTrip_FurnaceDraft_HI_HI THEN
    bTripLatch_Draft_HI_HI := TRUE;
    dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0040; (* Bit 6: Furnace Positive Pressure Blowout Trip *)
ELSIF PT_FURNACE_DRAFT_103A > c_rWarn_FurnaceDraft_HI THEN
    bWarnLatch_Draft_HI := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0040;
ELSE
    bWarnLatch_Draft_HI := FALSE;
END_IF;

IF PT_FURNACE_DRAFT_103A < c_rTrip_FurnaceDraft_LO_LO THEN
    bTripLatch_Draft_LO_LO := TRUE;
    dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0080; (* Bit 7: Furnace Severe Implosion Negative Pressure Trip *)
ELSIF PT_FURNACE_DRAFT_103A < c_rWarn_FurnaceDraft_LO THEN
    bWarnLatch_Draft_LO := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0080;
ELSE
    bWarnLatch_Draft_LO := FALSE;
END_IF;

(* 7.4 Boiler Superheater Tube Corrosion Thinning Warning *)
IF rSuperheaterThicknessVoted_mm < c_rTrip_SuperheaterWall_LO_LO THEN
    bTripLatch_Superheater_LO_LO := TRUE;
    dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_1000; (* Bit 12: Tube Rupture Imminent Trip *)
ELSIF rSuperheaterThicknessVoted_mm < c_rWarn_SuperheaterWall_LO THEN
    bWarnLatch_Superheater_LO := TRUE;
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_1000; (* Bit 12: Superheater Thinning Early Advisory *)
ELSE
    bWarnLatch_Superheater_LO := FALSE;
END_IF;

(* Automatic Safety Interruption: If Legal Emission Breach Latched -> Force Emergency State 11 *)
IF bLegalEmissionBreachTrip OR bTripLatch_PostComb_LO_LO OR bTripLatch_Draft_HI_HI OR bTripLatch_Draft_LO_LO THEN
    iFSM_State := 11; (* Transition to EMERGENCY_FEED_CUT_SMOKE_STOP *)
END_IF;

(* =====================================================================================================================
 * PHASE 8: DIAGNOSTIC STATUS WORD BIT-PACKING & ACTUATOR COMMAND NORMALIZATION
 * ===================================================================================================================== *)

(* Pack Global System Status Word *)
dwSystemStatusWord := 16#0000_0000;
IF bEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bEU_Directive_2010_75_Compliant THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bLegalEmissionBreachTrip THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bGrateHydraulicJamReverse THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bAuxiliaryBurnerActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bStateSpaceInitialized THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
dwSystemStatusWord := dwSystemStatusWord OR (SHL(INT_TO_DWORD(iFSM_State), 8));

(* Pack Actuator Status Word *)
dwActuatorStatusWord := 16#0000_0000;
IF rGrateSpeedCmd_Zone1_strokes_h > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0001; END_IF;
IF rGrateSpeedCmd_Zone2_strokes_h > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0002; END_IF;
IF rGrateSpeedCmd_Zone3_strokes_h > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0004; END_IF;
IF rGrateSpeedCmd_Zone4_strokes_h > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0008; END_IF;
IF rPrimaryAirFanRPMCmd_rpm > 100.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0010; END_IF;
IF rSecondaryAirFanRPMCmd_rpm > 100.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0020; END_IF;
IF rIDF_FanSpeedCmd_rpm > 100.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0040; END_IF;
IF rUreaDosingPumpSpeedCmd_pct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0080; END_IF;
IF rLimeSlurryFeedPumpCmd_pct > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0100; END_IF;
IF rActivatedCarbonFeederCmd_kgh > 1.0 THEN dwActuatorStatusWord := dwActuatorStatusWord OR 16#0000_0200; END_IF;

(* Final Hard Safety Clamping on Physical Actuators *)
rGrateSpeedCmd_Zone1_strokes_h := LIMIT(-25.0, rGrateSpeedCmd_Zone1_strokes_h, 60.0);
rGrateSpeedCmd_Zone2_strokes_h := LIMIT(-25.0, rGrateSpeedCmd_Zone2_strokes_h, 50.0);
rGrateSpeedCmd_Zone3_strokes_h := LIMIT(-25.0, rGrateSpeedCmd_Zone3_strokes_h, 45.0);
rGrateSpeedCmd_Zone4_strokes_h := LIMIT(-20.0, rGrateSpeedCmd_Zone4_strokes_h, 35.0);

rPrimaryAirDamperCmd_pct := LIMIT(0.0, rPrimaryAirDamperCmd_pct, 100.0);
rSecondaryAirDamperCmd_pct := LIMIT(0.0, rSecondaryAirDamperCmd_pct, 100.0);
rPrimaryAirFanRPMCmd_rpm := LIMIT(0.0, rPrimaryAirFanRPMCmd_rpm, 1500.0);
rSecondaryAirFanRPMCmd_rpm := LIMIT(0.0, rSecondaryAirFanRPMCmd_rpm, 1500.0);
rIDF_FanSpeedCmd_rpm := LIMIT(0.0, rIDF_FanSpeedCmd_rpm, 1200.0);

rUreaDosingPumpSpeedCmd_pct := LIMIT(0.0, rUreaDosingPumpSpeedCmd_pct, 100.0);
rLimeSlurryAtomizerSpeedCmd_rpm := LIMIT(0.0, rLimeSlurryAtomizerSpeedCmd_rpm, 15000.0);
rLimeSlurryFeedPumpCmd_pct := LIMIT(0.0, rLimeSlurryFeedPumpCmd_pct, 100.0);
rActivatedCarbonFeederCmd_kgh := LIMIT(0.0, rActivatedCarbonFeederCmd_kgh, 80.0);
rAuxiliaryBurnerFiringRate_pct := LIMIT(0.0, rAuxiliaryBurnerFiringRate_pct, 100.0);

END_FUNCTION_BLOCK
"""
