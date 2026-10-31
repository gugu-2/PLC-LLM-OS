# module_phases_6_7.py
# Contains Phase 6 (12-Stage Operational FSM), Phase 7 (ISA-18.2 Alarms) and Footer

def get_phase6_fsm():
    return """(* ================================================================================================== *)
(* === PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) ===                                  *)
(* ================================================================================================== *)
tStateTimer(IN := TRUE, PT := T#86400S);

CASE iActiveFSMState OF
    1: (* STATE_01_BAG_LEAK_TEST: Pre-use single-use bag sterile pressure decay integrity test *)
        rCmd_MFC_Air_Macro_sLpm := 2.50; (* Pressurize single-use bag with sterile clean air *)
        rCmd_AgitatorSpeed_rpm := 0.0;
        rCmd_PerfusionFeedPump_Lph := 0.0;
        rCmd_PermeateHarvestPump_Lph := 0.0;
        rCmd_CellBleedPump_Lph := 0.0;
        rCmd_BasePeristalticPump_mLph := 0.0;
        rCmd_TCU_HeatingPower_kW := 0.0;
        rCmd_TCU_CoolingValve_Pct := 0.0;

        IF rVesselInternalPress_mbar >= 28.0 THEN
            rCmd_MFC_Air_Macro_sLpm := 0.0; (* Isolate inlet air valve *)
            IF rBagLeakStartPress_mbar = 0.0 THEN
                rBagLeakStartPress_mbar := rVesselInternalPress_mbar;
            END_IF;
            tLeakHoldTimer(IN := TRUE, PT := T#600S); (* 10-Minute pressure hold *)
            rBagLeakDecay_mbar := rBagLeakStartPress_mbar - rVesselInternalPress_mbar;

            IF rBagLeakDecay_mbar > 1.50 THEN
                (* Excessive pressure loss: Single-use bag sterile barrier failure *)
                dwAlarmWord_2 := dwAlarmWord_2 OR 16#00010000; (* Bit 16: Bag Leak Test Fail *)
                bCriticalAlarmSummary := TRUE;
            END_IF;

            IF tLeakHoldTimer.Q AND (rBagLeakDecay_mbar <= 1.50) THEN
                tLeakHoldTimer(IN := FALSE);
                rBagLeakStartPress_mbar := 0.0;
                iActiveFSMState := 2; (* Advance to Media Pre-Fill & Heat Conditioning *)
            END_IF;
        END_IF;

    2: (* STATE_02_MEDIA_PREFILL_CONDITION: Charge 350L basal media, heat to 37C, start gentle agitation *)
        rCmd_MFC_Air_Macro_sLpm := 0.50; (* Headspace blanket sweep *)
        IF arrX_State[11] < 350.0 THEN
            rCmd_PerfusionFeedPump_Lph := 48.0; (* Pump in basal growth media *)
        ELSE
            rCmd_PerfusionFeedPump_Lph := 0.0;
        END_IF;

        IF arrX_State[11] >= 200.0 THEN
            rCmd_AgitatorSpeed_rpm := 45.0; (* Gentle mixing to prevent thermal stratification *)
        END_IF;

        (* Warm jacket to reach setpoint temperature *)
        rErr_Temp := rSet_Temperature_degC - arrX_State[10];
        IF rErr_Temp > 0.10 THEN
            rCmd_TCU_HeatingPower_kW := 3.50;
            rCmd_TCU_CoolingValve_Pct := 0.0;
        ELSIF rErr_Temp < -0.10 THEN
            rCmd_TCU_HeatingPower_kW := 0.0;
            rCmd_TCU_CoolingValve_Pct := 25.0;
        ELSE
            rCmd_TCU_HeatingPower_kW := 0.85; (* Steady thermal holding *)
            rCmd_TCU_CoolingValve_Pct := 0.0;
        END_IF;

        IF (arrX_State[11] >= 350.0) AND (ABS(arrX_State[10] - rSet_Temperature_degC) <= 0.20) THEN
            iActiveFSMState := 3; (* Advance to Probe Calibration & Inoculation *)
        END_IF;

    3: (* STATE_03_PROBE_CALIBRATION_INOCULATION: Air sparge DO span calibration and seed train transfer *)
        rCmd_AgitatorSpeed_rpm := 120.0;
        rCmd_MFC_Air_Micro_sLpm := 8.00; (* Sparge air to saturate liquid at 100% DO span *)
        rCmd_MFC_Air_Macro_sLpm := 1.00;
        tInoculationTimer(IN := TRUE, PT := T#1200S); (* Allow DO saturation and operator transfer *)

        IF tInoculationTimer.Q OR bCmd_AdvanceFSM_Phase THEN
            tInoculationTimer(IN := FALSE);
            bInoculationComplete := TRUE;
            iActiveFSMState := 4; (* Advance to Batch Exponential Growth Phase *)
        END_IF;

    4: (* STATE_04_BATCH_EXPONENTIAL_GROWTH: Cell exponential proliferation without cell retention *)
        rCmd_AgitatorSpeed_rpm := rSet_AgitatorBaseSpeed_rpm;
        rCmd_PerfusionFeedPump_Lph := 0.0;
        rCmd_PermeateHarvestPump_Lph := 0.0;
        rCmd_CellBleedPump_Lph := 0.0;

        (* Execute DO split-range gas cascade *)
        rErr_DO := rSet_DO_Pct - arrX_State[8];
        IF rErr_DO > 2.0 THEN
            rCmd_MFC_O2_Micro_sLpm  := arrU_Optimal[1];
            rCmd_MFC_Air_Micro_sLpm := arrU_Optimal[2];
            rCmd_MFC_N2_Macro_sLpm  := 0.0;
        ELSIF rErr_DO < -5.0 THEN
            rCmd_MFC_O2_Micro_sLpm  := 0.0;
            rCmd_MFC_Air_Micro_sLpm := 0.0;
            rCmd_MFC_N2_Macro_sLpm  := 1.50; (* Nitrogen deoxygenation *)
        ELSE
            rCmd_MFC_O2_Micro_sLpm  := arrU_Optimal[1] * 0.50;
            rCmd_MFC_Air_Micro_sLpm := arrU_Optimal[2];
            rCmd_MFC_N2_Macro_sLpm  := 0.0;
        END_IF;

        (* Execute Dual pH regulation: CO2 acidifying vs NaHCO3 base addition *)
        rErr_pH := arrX_State[9] - rSet_PH;
        IF rErr_pH > 0.04 THEN
            rCmd_MFC_CO2_Macro_sLpm := arrU_Optimal[3]; (* CO2 acidifying pulse *)
            rCmd_BasePeristalticPump_mLph := 0.0;
        ELSIF rErr_pH < -0.04 THEN
            rCmd_MFC_CO2_Macro_sLpm := 0.0;
            rCmd_BasePeristalticPump_mLph := arrU_Optimal[4]; (* Base pumping *)
        ELSE
            rCmd_MFC_CO2_Macro_sLpm := 0.0;
            rCmd_BasePeristalticPump_mLph := 0.0;
        END_IF;

        (* Thermal regulation *)
        rCmd_TCU_HeatingPower_kW  := arrU_Optimal[8] * 0.60 + 0.40;
        rCmd_TCU_CoolingValve_Pct := 0.0;

        (* Transition criteria: Biomass reached 6.0 x 10^6 cells/mL or Glucose depleted *)
        IF (arrX_State[1] >= 6.00) OR (arrX_State[3] <= 3.00) OR bCmd_AdvanceFSM_Phase THEN
            iActiveFSMState := 5; (* Advance to Perfusion Feed Ramp-Up *)
        END_IF;

    5: (* STATE_05_PERFUSION_FEED_RAMP_UP: Prime TFF hollow fiber module, establish crossflow & ramp *)
        rRetentateCircFlow_Lph := 320.0; (* Retentate recirculation crossflow engaged *)
        rPerfusionRamp_VVD := (arrX_State[1] * rSet_CSPR_Target_pL_cell_d * 1.0E-6);
        IF rPerfusionRamp_VVD < 0.20 THEN rPerfusionRamp_VVD := 0.20; END_IF;
        IF rPerfusionRamp_VVD > 1.00 THEN rPerfusionRamp_VVD := 1.00; END_IF;

        rCmd_PermeateHarvestPump_Lph := (rPerfusionRamp_VVD * arrX_State[11]) / 24.0;
        rCmd_PerfusionFeedPump_Lph := rCmd_PermeateHarvestPump_Lph + ((rSet_WorkingVolume_L - arrX_State[11]) * 0.50);
        rCmd_CellBleedPump_Lph := 0.0;
        rCmd_AgitatorSpeed_rpm := rSet_AgitatorBaseSpeed_rpm + 20.0;

        (* MPC gas and thermal regulation active *)
        rCmd_MFC_O2_Micro_sLpm  := arrU_Optimal[1];
        rCmd_MFC_Air_Micro_sLpm := arrU_Optimal[2];
        rCmd_MFC_CO2_Macro_sLpm := arrU_Optimal[3];
        rCmd_BasePeristalticPump_mLph := arrU_Optimal[4];
        rCmd_TCU_HeatingPower_kW := arrU_Optimal[8] * 0.50 + 0.50;

        IF (rPerfusionRamp_VVD >= 0.95) AND (arrX_State[1] >= 20.0) THEN
            iActiveFSMState := 6; (* Advance to Steady-State Continuous Perfusion Chemostat *)
        END_IF;

    6: (* STATE_06_CONTINUOUS_PERFUSION_STEADY: Full high-density continuous perfusion chemostat *)
        rRetentateCircFlow_Lph := 320.0;
        rPerfusionRamp_VVD := (arrX_State[1] * rSet_CSPR_Target_pL_cell_d * 1.0E-6);
        IF rPerfusionRamp_VVD < 1.00 THEN rPerfusionRamp_VVD := 1.00; END_IF;
        IF rPerfusionRamp_VVD > rSet_MaxPerfusionRate_VVD THEN rPerfusionRamp_VVD := rSet_MaxPerfusionRate_VVD; END_IF;

        rCmd_PermeateHarvestPump_Lph := (rPerfusionRamp_VVD * arrX_State[11]) / 24.0;
        rCmd_PerfusionFeedPump_Lph := rCmd_PermeateHarvestPump_Lph + rCmd_CellBleedPump_Lph + ((rSet_WorkingVolume_L - arrX_State[11]) * 0.85);
        rCmd_AgitatorSpeed_rpm := rSet_AgitatorBaseSpeed_rpm + 30.0;

        (* Optimal MPC command outputs *)
        rCmd_MFC_O2_Micro_sLpm  := arrU_Optimal[1];
        rCmd_MFC_Air_Micro_sLpm := arrU_Optimal[2];
        rCmd_MFC_CO2_Macro_sLpm := arrU_Optimal[3];
        rCmd_BasePeristalticPump_mLph := arrU_Optimal[4];
        rCmd_TCU_HeatingPower_kW := arrU_Optimal[8] * 0.50 + 0.50;

        (* Automated backflush cycle trigger *)
        tBackflushCycleTimer(IN := TRUE, PT := REAL_TO_TIME(rSet_BackflushInterval_s * 1000.0));
        IF tBackflushCycleTimer.Q OR (rCalc_TMP_mbar >= rSet_TMP_AlarmThreshold_mbar) OR bCmd_ForceBackflushNow THEN
            tBackflushCycleTimer(IN := FALSE);
            iActiveFSMState := 7; (* Branch to Filter Backflush Cycle *)
        ELSIF arrX_State[1] >= rSet_VCD_Target_1e6 THEN
            iActiveFSMState := 8; (* Branch to High-Density Cell Bleed Adjustment *)
        END_IF;

    7: (* STATE_07_FILTER_BACKFLUSH_PERMEATE_CYCLE: High-speed reverse permeate pulse cleaning *)
        rCmd_PermeateHarvestPump_Lph := 0.0; (* Pause forward permeate harvest *)
        bCmd_TFF_BackflushValve := TRUE;    (* Energize reverse backflush valve *)
        bBackflushActive := TRUE;
        tBackflushPulseTimer(IN := TRUE, PT := REAL_TO_TIME(rSet_BackflushDuration_s * 1000.0));

        IF tBackflushPulseTimer.Q THEN
            tBackflushPulseTimer(IN := FALSE);
            bCmd_TFF_BackflushValve := FALSE;
            bBackflushActive := FALSE;
            iActiveFSMState := 6; (* Return to Continuous Perfusion Steady-State *)
        END_IF;

    8: (* STATE_08_HIGH_DENSITY_CELL_BLEED_CONTROL: Continuous biomass chemostat holding at setpoint *)
        rRetentateCircFlow_Lph := 320.0;
        rPerfusionRamp_VVD := (rSet_VCD_Target_1e6 * rSet_CSPR_Target_pL_cell_d * 1.0E-6);
        rCmd_PermeateHarvestPump_Lph := (rPerfusionRamp_VVD * arrX_State[11]) / 24.0;

        (* Modulate cell bleed pump based on excess viable cell density and growth rate *)
        rChemostatBleedSetpoint_Lph := (rMu_Net * arrX_State[11]) * (((arrX_State[1] - rSet_VCD_Target_1e6) / rSet_VCD_Target_1e6) * 1.50 + 1.0);
        IF rChemostatBleedSetpoint_Lph < 0.10 THEN rChemostatBleedSetpoint_Lph := 0.10; END_IF;
        IF rChemostatBleedSetpoint_Lph > 14.0 THEN rChemostatBleedSetpoint_Lph := 14.0; END_IF;
        rCmd_CellBleedPump_Lph := rChemostatBleedSetpoint_Lph;

        rCmd_PerfusionFeedPump_Lph := rCmd_PermeateHarvestPump_Lph + rCmd_CellBleedPump_Lph + ((rSet_WorkingVolume_L - arrX_State[11]) * 0.90);
        rCmd_AgitatorSpeed_rpm := rSet_AgitatorBaseSpeed_rpm + 40.0;

        (* Track cumulative harvest *)
        rCumulativeHarvest_kg := rCumulativeHarvest_kg + (rCmd_PermeateHarvestPump_Lph * tTaskCycleTime_s / 3600.0);
        IF rCumulativeHarvest_kg >= 200.0 THEN
            iActiveFSMState := 9; (* Divert to new harvest tote *)
        END_IF;

        IF bCmd_AbortRun THEN
            iActiveFSMState := 10; (* Advance to End-of-Run Terminate *)
        END_IF;

    9: (* STATE_09_PRODUCT_HARVEST_COLLECTION: Dual-manifold harvest tote switching sequence *)
        bCmd_HarvestDivertValve := TRUE; (* Switch valve to tote B *)
        rCumulativeHarvest_kg := 0.0;    (* Reset tote weight counter *)
        iActiveFSMState := 8;            (* Return to High-Density Bleed Chemostat *)

    10: (* STATE_10_HARVEST_END_OF_RUN_TERMINATE: Halt media feed, chill broth to 15C, drain vessel *)
        rCmd_PerfusionFeedPump_Lph := 0.0; (* Stop fresh nutrient media *)
        rCmd_AgitatorSpeed_rpm := 35.0;     (* Low speed to prevent foaming *)
        rCmd_TCU_HeatingPower_kW := 0.0;
        rCmd_TCU_CoolingValve_Pct := 100.0; (* Quench metabolism by cooling to 15C *)
        rCmd_PermeateHarvestPump_Lph := 35.0; (* Drain remaining clarified broth *)
        rCmd_CellBleedPump_Lph := 15.0;       (* Drain remaining biomass heel *)

        IF arrX_State[11] <= 15.0 THEN
            rCmd_PermeateHarvestPump_Lph := 0.0;
            rCmd_CellBleedPump_Lph := 0.0;
            iActiveFSMState := 11; (* Advance to In-line CIP Waste Neutralization *)
        END_IF;

    11: (* STATE_11_INLINE_CIP_WASTE_NEUTRALIZATION: Caustic decontamination of retention lines *)
        bCmd_WasteNeutralizeValve := TRUE; (* Open 0.5M NaOH flush line *)
        rCmd_AgitatorSpeed_rpm := 0.0;
        rCmd_MFC_Air_Macro_sLpm := 0.0;
        tNeutralizationTimer(IN := TRUE, PT := T#1800S); (* 30-Minute chemical contact *)

        IF tNeutralizationTimer.Q OR bCmd_AdvanceFSM_Phase THEN
            tNeutralizationTimer(IN := FALSE);
            bCmd_WasteNeutralizeValve := FALSE;
            iActiveFSMState := 12; (* Advance to System Standby Safe *)
        END_IF;

    12: (* STATE_12_SYSTEM_STANDBY_SAFE: Safe parked state, all actuators de-energized *)
        rCmd_MFC_O2_Micro_sLpm        := 0.0;
        rCmd_MFC_Air_Micro_sLpm       := 0.0;
        rCmd_MFC_Air_Macro_sLpm       := 0.0;
        rCmd_MFC_CO2_Macro_sLpm       := 0.0;
        rCmd_MFC_N2_Macro_sLpm        := 0.0;
        rCmd_AgitatorSpeed_rpm        := 0.0;
        rCmd_TCU_HeatingPower_kW      := 0.0;
        rCmd_TCU_CoolingValve_Pct     := 0.0;
        rCmd_PerfusionFeedPump_Lph    := 0.0;
        rCmd_PermeateHarvestPump_Lph  := 0.0;
        rCmd_CellBleedPump_Lph        := 0.0;
        rCmd_BasePeristalticPump_mLph := 0.0;
        bCmd_AntifoamDosePulse        := FALSE;
        bCmd_TFF_BackflushValve       := FALSE;
        bCmd_HarvestDivertValve       := FALSE;
        bCmd_WasteNeutralizeValve     := FALSE;
END_CASE;
"""

def get_phase7_alarms():
    return """(* ================================================================================================== *)
(* === PHASE 7: ISA-18.2 MULTI-TIERED ALARMS & BIT-PACKED TELEMETRY ===                              *)
(* ================================================================================================== *)
(* 7.1 Automated Antifoam Dosing Logic *)
IF bFoamDetectHeadspace AND NOT tAntifoamLockoutTimer.IN THEN
    bCmd_AntifoamDosePulse := TRUE;
    bAntifoamActive := TRUE;
    tAntifoamShotTimer(IN := TRUE, PT := T#3S); (* 3-Second antifoam shot *)
END_IF;

IF tAntifoamShotTimer.Q THEN
    tAntifoamShotTimer(IN := FALSE);
    bCmd_AntifoamDosePulse := FALSE;
    bAntifoamActive := FALSE;
    tAntifoamLockoutTimer(IN := TRUE, PT := T#180S); (* 3-Minute lockout interlock *)
END_IF;

IF tAntifoamLockoutTimer.Q THEN
    tAntifoamLockoutTimer(IN := FALSE);
END_IF;

tAlarmDebounce_FoamPersistent(IN := bFoamDetectHeadspace, PT := T#60S);
IF tAlarmDebounce_FoamPersistent.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00100000; (* Bit 20: Persistent Foam Alarm *)
END_IF;

(* 7.2 Dissolved Oxygen ISA-18.2 Alarms *)
tAlarmDebounce_DO_LL(IN := (rVoted_DO_Pct < c_rDO_LL_Limit), PT := T#3S);
IF tAlarmDebounce_DO_LL.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000001; (* Bit 0: DO Low-Low Critical *)
ELSIF rVoted_DO_Pct > (c_rDO_LL_Limit + c_rDO_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000001;
END_IF;

IF rVoted_DO_Pct < c_rDO_L_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000002; (* Bit 1: DO Low Warning *)
ELSIF rVoted_DO_Pct > (c_rDO_L_Limit + c_rDO_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000002;
END_IF;

IF rVoted_DO_Pct > c_rDO_H_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000004; (* Bit 2: DO High Warning *)
ELSIF rVoted_DO_Pct < (c_rDO_H_Limit - c_rDO_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000004;
END_IF;

tAlarmDebounce_DO_HH(IN := (rVoted_DO_Pct > c_rDO_HH_Limit), PT := T#3S);
IF tAlarmDebounce_DO_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000008; (* Bit 3: DO High-High Critical *)
ELSIF rVoted_DO_Pct < (c_rDO_HH_Limit - c_rDO_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000008;
END_IF;

(* 7.3 Broth pH ISA-18.2 Alarms *)
tAlarmDebounce_PH_LL(IN := (rVoted_PH < c_rPH_LL_Limit), PT := T#5S);
IF tAlarmDebounce_PH_LL.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000010; (* Bit 4: pH Low-Low Critical *)
ELSIF rVoted_PH > (c_rPH_LL_Limit + c_rPH_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000010;
END_IF;

IF rVoted_PH < c_rPH_L_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000020; (* Bit 5: pH Low Warning *)
ELSIF rVoted_PH > (c_rPH_L_Limit + c_rPH_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000020;
END_IF;

IF rVoted_PH > c_rPH_H_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000040; (* Bit 6: pH High Warning *)
ELSIF rVoted_PH < (c_rPH_H_Limit - c_rPH_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000040;
END_IF;

tAlarmDebounce_PH_HH(IN := (rVoted_PH > c_rPH_HH_Limit), PT := T#5S);
IF tAlarmDebounce_PH_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000080; (* Bit 7: pH High-High Critical *)
ELSIF rVoted_PH < (c_rPH_HH_Limit - c_rPH_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000080;
END_IF;

(* 7.4 Broth Temperature ISA-18.2 Alarms *)
tAlarmDebounce_Temp_LL(IN := (rBrothTemp_degC < c_rTemp_LL_Limit), PT := T#5S);
IF tAlarmDebounce_Temp_LL.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000100; (* Bit 8: Temp Low-Low Critical *)
ELSIF rBrothTemp_degC > (c_rTemp_LL_Limit + c_rTemp_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000100;
END_IF;

tAlarmDebounce_Temp_HH(IN := (rBrothTemp_degC > c_rTemp_HH_Limit), PT := T#5S);
IF tAlarmDebounce_Temp_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00000800; (* Bit 11: Temp High-High Critical *)
ELSIF rBrothTemp_degC < (c_rTemp_HH_Limit - c_rTemp_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00000800;
END_IF;

(* 7.5 Single-Use Bag Internal Pressure Alarms *)
IF rVesselInternalPress_mbar > c_rPress_Bag_H_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00001000; (* Bit 12: Bag Pressure Warning *)
ELSIF rVesselInternalPress_mbar < (c_rPress_Bag_H_Limit - c_rPress_Bag_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00001000;
END_IF;

tAlarmDebounce_Press_HH(IN := (rVesselInternalPress_mbar > c_rPress_Bag_HH_Limit), PT := T#1S);
IF tAlarmDebounce_Press_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00002000; (* Bit 13: Bag Pressure HH Burst Risk *)
    bCriticalAlarmSummary := TRUE;
ELSIF rVesselInternalPress_mbar < (c_rPress_Bag_HH_Limit - c_rPress_Bag_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00002000;
END_IF;

(* 7.6 TFF Transmembrane Pressure Alarms *)
IF rCalc_TMP_mbar > c_rTMP_H_Limit THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00004000; (* Bit 14: TMP High Fouling Warning *)
ELSIF rCalc_TMP_mbar < (c_rTMP_H_Limit - c_rTMP_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00004000;
END_IF;

tAlarmDebounce_TMP_HH(IN := (rCalc_TMP_mbar > c_rTMP_HH_Limit), PT := T#3S);
IF tAlarmDebounce_TMP_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00008000; (* Bit 15: TMP High-High Irreversible Fouling *)
ELSIF rCalc_TMP_mbar < (c_rTMP_HH_Limit - c_rTMP_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00008000;
END_IF;

(* 7.7 Skid Weight Alarms *)
tAlarmDebounce_Weight_HH(IN := (rVoted_Weight_kg > c_rWeight_HH_Limit), PT := T#2S);
IF tAlarmDebounce_Weight_HH.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00080000; (* Bit 19: Skid Weight HH Spill Risk *)
    bCriticalAlarmSummary := TRUE;
ELSIF rVoted_Weight_kg < (c_rWeight_HH_Limit - c_rWeight_Deadband) THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00080000;
END_IF;

(* 7.8 Agitator Coupling & Speed Deviation *)
tAlarmDebounce_AgitatorDecouple(IN := (ABS(rAgitatorSpeedFeedback_rpm - rCmd_AgitatorSpeed_rpm) > 25.0) AND (rCmd_AgitatorSpeed_rpm > 10.0), PT := T#4S);
IF tAlarmDebounce_AgitatorDecouple.Q THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00200000; (* Bit 21: Agitator Decoupling Fault *)
END_IF;

(* 7.9 Metabolic Respiratory Quotient Excursion *)
IF (rCalc_RQ < 0.65) OR (rCalc_RQ > 1.35) THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00400000; (* Bit 22: Metabolic RQ Abnormal *)
ELSE
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00400000;
END_IF;

(* 7.10 CSPR Nutrient Starvation Warning *)
rCalc_CSPR_pL_cell_d := (rCmd_PermeateHarvestPump_Lph * 24.0 * 1.0E6) / (arrX_State[1] * arrX_State[11]);
IF (rCalc_CSPR_pL_cell_d < 15.0) AND (iActiveFSMState >= 6) AND (iActiveFSMState <= 8) THEN
    dwAlarmWord_1 := dwAlarmWord_1 OR 16#00800000; (* Bit 23: CSPR Starvation Warning *)
ELSE
    dwAlarmWord_1 := dwAlarmWord_1 AND NOT 16#00800000;
END_IF;

(* 7.11 Alarm Acknowledgement *)
IF bCmd_AcknowledgeAlarms THEN
    dwAlarmWord_1 := dwAlarmWord_1 AND 16#80000000; (* Preserve E-Stop trip bit *)
    dwAlarmWord_2 := 16#00000000;
    bCriticalAlarmSummary := FALSE;
END_IF;

(* 7.12 Status Word 1 Packing: Operational Modes & Actuator States *)
dwStatusWord_1 := INT_TO_DWORD(iActiveFSMState) AND 16#0000000F;
IF bEnableSystem THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000010; END_IF;
IF bSterileBarrierOk THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000020; END_IF;
IF rCmd_AgitatorSpeed_rpm > 10.0 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000040; END_IF;
IF rCmd_TCU_HeatingPower_kW > 0.10 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000080; END_IF;
IF rCmd_TCU_CoolingValve_Pct > 5.0 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000100; END_IF;
IF rCmd_MFC_O2_Micro_sLpm > 0.05 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000200; END_IF;
IF rCmd_MFC_Air_Micro_sLpm > 0.05 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000400; END_IF;
IF rCmd_MFC_CO2_Macro_sLpm > 0.05 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00000800; END_IF;
IF rCmd_PerfusionFeedPump_Lph > 0.10 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00001000; END_IF;
IF rCmd_PermeateHarvestPump_Lph > 0.10 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00002000; END_IF;
IF rCmd_CellBleedPump_Lph > 0.05 THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00004000; END_IF;
IF bBackflushActive THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00008000; END_IF;
IF bAntifoamActive THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00010000; END_IF;
IF bCmd_HarvestDivertValve THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00020000; END_IF;
IF bCmd_WasteNeutralizeValve THEN dwStatusWord_1 := dwStatusWord_1 OR 16#00040000; END_IF;

(* 7.13 Status Word 2 Packing: Metabolic Quality Metrics *)
dwStatusWord_2 := 16#00000000;
IF arrX_State[1] >= rSet_VCD_Target_1e6 THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000001; END_IF;
IF (rCalc_CSPR_pL_cell_d >= 25.0) AND (rCalc_CSPR_pL_cell_d <= 35.0) THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000002; END_IF;
IF (rCalc_RQ >= 0.85) AND (rCalc_RQ <= 1.10) THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000004; END_IF;
IF rCalc_MembraneResistance_1e11 <= 3.00 THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000008; END_IF;
IF rCalc_ShearRate_s_inv < 2000.0 THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000010; END_IF;
IF (rCalc_PowerPerVolume_W_m3 >= 20.0) AND (rCalc_PowerPerVolume_W_m3 <= 60.0) THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000020; END_IF;
IF rCalc_kLa_h_inv >= 15.0 THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000040; END_IF;
IF rCalc_KolmogorovScale_um >= 80.0 THEN dwStatusWord_2 := dwStatusWord_2 OR 16#00000080; END_IF;

(* System Health Summary Flag *)
bSystemHealthy := (dwAlarmWord_1 = 16#00000000) AND (dwAlarmWord_2 = 16#00000000) AND bEmergencyStopOk AND bSterileBarrierOk;

END_FUNCTION_BLOCK
"""
