# st_phase4_5_6_7.py
# Contains Phase 4 (20-Stack Splitting), Phase 5 (12-Stage FSM), Phase 6 (TSA Pacing), Phase 7 (ISA-18.2 Alarms), and END_FUNCTION_BLOCK

def get_phase4_5_6_7():
    return """
(* ===================================================================================================================
 * PHASE 4: 20-STACK DYNAMIC POWER SPLITTING & FAST RENEWABLE TRACKING
 * =================================================================================================================== *)
(* 4.1 Renewable Target Trajectory Slew-Rate Limiter *)
IF bAutoRenewableTrackingEnable THEN
    (* Determine net setpoint from grid target, wind, solar, and grid frequency droop *)
    rDeltaPowerDemand := rGridTargetTotalPower_MW;
    IF bGridFrequencySupportEnable THEN
        rDeltaPowerDemand := rDeltaPowerDemand - rGridFrequencyDroopGain_MW_per_Hz * (rGridFrequency_Hz - 50.00);
    END_IF;

    (* Bound demand to total 100.0 MW facility capacity *)
    IF rDeltaPowerDemand < 0.0 THEN
        rDeltaPowerDemand := 0.0;
    ELSIF rDeltaPowerDemand > 100.0 THEN
        rDeltaPowerDemand := 100.0;
    END_IF;

    (* Fast Trajectory Ramp Governor (< 5.0 s for 0 to 100% full swing = 20 MW/s) *)
    IF rDeltaPowerDemand > rFilteredTargetPower_MW THEN
        rFilteredTargetPower_MW := rFilteredTargetPower_MW + rGridPowerRampRate_MW_per_s * c_rTs;
        IF rFilteredTargetPower_MW > rDeltaPowerDemand THEN
            rFilteredTargetPower_MW := rDeltaPowerDemand;
        END_IF;
    ELSIF rDeltaPowerDemand < rFilteredTargetPower_MW THEN
        rFilteredTargetPower_MW := rFilteredTargetPower_MW - rGridPowerRampRate_MW_per_s * c_rTs;
        IF rFilteredTargetPower_MW < rDeltaPowerDemand THEN
            rFilteredTargetPower_MW := rDeltaPowerDemand;
        END_IF;
    END_IF;
ELSE
    rFilteredTargetPower_MW := 10.0; (* Base fallback load *)
END_IF;

(* 4.2 Dynamic Health & Degradation Weighted Dispatch Engine *)
rActiveStacksCount := 0.0;
rTotalDispatchWeight := 0.0;

FOR iIdx := 1 TO 20 DO
    IF NOT aStackInhibited[iIdx] THEN
        rActiveStacksCount := rActiveStacksCount + 1.0;
        
        (* Weight inversely proportional to aging degradation factor, with thermal balance trim *)
        IF aStackDegradationFactor[iIdx] < 0.80 THEN
            aStackDegradationFactor[iIdx] := 1.00;
        END_IF;
        
        (* Thermal penalty factor: derate stacks that are drifting above 72.0 deg C *)
        aStackDispatchWeight[iIdx] := (1.0 / aStackDegradationFactor[iIdx]) *
            (1.0 - 0.03 * ABS(aStackTemp_Actual[iIdx] - 70.0));
        IF aStackDispatchWeight[iIdx] < 0.20 THEN
            aStackDispatchWeight[iIdx] := 0.20;
        END_IF;
        
        rTotalDispatchWeight := rTotalDispatchWeight + aStackDispatchWeight[iIdx];
    ELSE
        aStackDispatchWeight[iIdx] := 0.0;
    END_IF;
END_FOR;

(* 4.3 Turndown Preservation & Stack Power Allocation *)
(* Prevent active stacks from dipping below 5% (0.25 MW) where H2-in-O2 crossover spikes *)
IF rTotalDispatchWeight > 0.01 AND iFSM_State = 60 THEN
    FOR iIdx := 1 TO 20 DO
        IF NOT aStackInhibited[iIdx] THEN
            rAllocatedStackPower := (rFilteredTargetPower_MW + au_control[1]) *
                (aStackDispatchWeight[iIdx] / rTotalDispatchWeight);
            
            (* Low-Load Turndown Protection *)
            IF rAllocatedStackPower < rMinStackTurndownPower_MW THEN
                rAllocatedStackPower := rMinStackTurndownPower_MW;
            ELSIF rAllocatedStackPower > 5.00 THEN
                rAllocatedStackPower := 5.00;
            END_IF;
            
            aStackPowerCmd_MW[iIdx] := rAllocatedStackPower;
            
            (* Calculate Current Setpoint from Stack Actual Terminal Voltage *)
            IF aStackVoltage_Actual[iIdx] > 500.0 THEN
                aStackCurrentCmd_A[iIdx] := (rAllocatedStackPower * 1000000.0) / aStackVoltage_Actual[iIdx];
            ELSE
                aStackCurrentCmd_A[iIdx] := (rAllocatedStackPower * 1000000.0) / 1000.0;
            END_IF;
            
            (* Individual Thermal Heat Exchanger Valve Regulation (70.0 deg C target) *)
            aStackCoolingValveCmd_pct[iIdx] := 50.0 + 4.5 * (aStackTemp_Actual[iIdx] - 70.0);
            IF aStackCoolingValveCmd_pct[iIdx] < 0.0 THEN
                aStackCoolingValveCmd_pct[iIdx] := 0.0;
            ELSIF aStackCoolingValveCmd_pct[iIdx] > 100.0 THEN
                aStackCoolingValveCmd_pct[iIdx] := 100.0;
            END_IF;
        ELSE
            aStackPowerCmd_MW[iIdx] := 0.0;
            aStackCurrentCmd_A[iIdx] := 0.0;
            aStackCoolingValveCmd_pct[iIdx] := 0.0;
        END_IF;
    END_FOR;
ELSIF iFSM_State = 50 THEN
    (* 5% Turndown Start State: All uninhibited stacks run at exactly 0.25 MW (250 A) *)
    FOR iIdx := 1 TO 20 DO
        IF NOT aStackInhibited[iIdx] THEN
            aStackPowerCmd_MW[iIdx] := 0.250;
            aStackCurrentCmd_A[iIdx] := 250.0;
            aStackCoolingValveCmd_pct[iIdx] := 35.0;
        ELSE
            aStackPowerCmd_MW[iIdx] := 0.0;
            aStackCurrentCmd_A[iIdx] := 0.0;
            aStackCoolingValveCmd_pct[iIdx] := 0.0;
        END_IF;
    END_FOR;
ELSE
    (* System Offline or Stopping: Clamp currents to 0.0 *)
    FOR iIdx := 1 TO 20 DO
        aStackPowerCmd_MW[iIdx] := 0.0;
        aStackCurrentCmd_A[iIdx] := 0.0;
        aStackCoolingValveCmd_pct[iIdx] := 10.0;
    END_FOR;
END_IF;

(* Compute Aggregate Facility Power Actually Dispatched *)
rFacilityTotalPower_MW := 0.0;
FOR iIdx := 1 TO 20 DO
    rFacilityTotalPower_MW := rFacilityTotalPower_MW + aStackPowerCmd_MW[iIdx];
END_FOR;

(* ===================================================================================================================
 * PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * =================================================================================================================== *)
rStateTimer_s := rStateTimer_s + c_rTs;

CASE iFSM_State OF
    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 10: SYSTEM_OFFLINE_N2_PURGED
     * Facility idle, all 20 stacks de-energized, N2 blanket maintained at 1.5 bar, DI water drained or stagnant.
     * --------------------------------------------------------------------------------------------------------------- *)
    10:
        bSystemReady := bEnableMaster AND bEmergencyStop_NC AND NOT bSystemTripped AND bN2_PurgeHeaderAvailable;
        bSystemRunning := FALSE;
        bPowerTrackingActive := FALSE;
        bCrossoverDerateActive := FALSE;
        bFastPurgeActive := FALSE;

        (* Actuator Safe Idle Positioning *)
        rValveCmd_CathodeBackpress_pct := 10.0;
        rValveCmd_AnodeBackpress_pct := 10.0;
        rPumpCmd_DI_WaterCirculation_pct := 0.0;
        rValveCmd_DI_WaterMakeUp_pct := 0.0;
        rPumpCmd_MainCoolingLoop_pct := 0.0;
        bValveCmd_H2_ProductOffSpecVent := TRUE;
        bValveCmd_N2_PurgeSupplyMain := FALSE;

        (* Transition to Water Fill upon Supervisory Enable *)
        IF bEnableMaster AND bEmergencyStop_NC AND NOT bSystemTripped THEN
            iNextFSM_State := 20;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 20: DI_WATER_FILL_CIRCULATION
     * Priming anode circulation loops with high-purity DI water (< 0.055 uS/cm), de-aerating headers.
     * --------------------------------------------------------------------------------------------------------------- *)
    20:
        bSystemRunning := TRUE;
        rFillCirculationTimer_s := rFillCirculationTimer_s + c_rTs;
        rPumpCmd_DI_WaterCirculation_pct := 45.0;
        rValveCmd_DI_WaterMakeUp_pct := 60.0;
        rPumpCmd_MainCoolingLoop_pct := 30.0;
        rValveCmd_CathodeBackpress_pct := 25.0;
        rValveCmd_AnodeBackpress_pct := 25.0;

        (* Verify DI water quality conductivity < 0.08 uS/cm and circulation established for 30 seconds *)
        IF rFillCirculationTimer_s >= 30.0 AND rVoted_DI_WaterConductivity_uScm < 0.080 AND rVoted_DI_WaterFeedFlow_m3h > 5.0 THEN
            rFillCirculationTimer_s := 0.0;
            iNextFSM_State := 30;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 30: MEMBRANE_HYDRATION_SOAK
     * Warm water circulation at 50.0 deg C to fully re-hydrate Nafion polymer membrane matrices (lambda -> 14).
     * --------------------------------------------------------------------------------------------------------------- *)
    30:
        rHydrationSoakTimer_s := rHydrationSoakTimer_s + c_rTs;
        rPumpCmd_DI_WaterCirculation_pct := 65.0;
        rPumpCmd_MainCoolingLoop_pct := 40.0;
        rValveCmd_CoolingTowerBypass_pct := 80.0; (* Bypass cooling tower to warm stack headers *)

        (* Soak dwell for 45.0 seconds and temperature reaching 48.0 deg C *)
        IF rHydrationSoakTimer_s >= 45.0 AND rVoted_CoolingOutletTemp_degC >= 48.0 THEN
            rHydrationSoakTimer_s := 0.0;
            iNextFSM_State := 40;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 40: CATHODE_ANODE_PRE_PRESSURIZE
     * Equalizing anode and cathode headers up to 5.0 bar using inert buffer gas, verifying zero differential leak.
     * --------------------------------------------------------------------------------------------------------------- *)
    40:
        rPressurizeRampTimer_s := rPressurizeRampTimer_s + c_rTs;
        rValveCmd_CathodeBackpress_pct := 75.0;
        rValveCmd_AnodeBackpress_pct := 75.0;
        rPumpCmd_DI_WaterCirculation_pct := 60.0;

        (* Check differential pressure stability within +-0.03 bar and both vessels > 4.5 bar *)
        IF rPressurizeRampTimer_s >= 25.0 AND ABS(rVoted_MembraneDiffPressure_bar) <= 0.035 AND
           rVoted_AnodePressure_bar >= 4.5 AND rVoted_CathodePressure_bar >= 4.5 THEN
            rPressurizeRampTimer_s := 0.0;
            iNextFSM_State := 50;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 50: STACK_MINIMUM_LOAD_START_5PCT
     * Engaging 20 thyristor rectifiers at 5% turndown (250 A / 0.25 MW per stack), initiating gas evolution.
     * --------------------------------------------------------------------------------------------------------------- *)
    50:
        rMinLoadStartTimer_s := rMinLoadStartTimer_s + c_rTs;
        bPowerTrackingActive := FALSE;
        rPumpCmd_DI_WaterCirculation_pct := 70.0;
        rPumpCmd_MainCoolingLoop_pct := 60.0;
        bValveCmd_H2_ProductOffSpecVent := TRUE; (* Off-spec purge during ignition *)

        (* Pressurize vessels up to nominal 30.0 bar under electrochemical gas generation *)
        IF rVoted_AnodePressure_bar < 29.5 THEN
            rValveCmd_AnodeBackpress_pct := 80.0;
        ELSE
            rValveCmd_AnodeBackpress_pct := 50.0;
        END_IF;

        IF rVoted_CathodePressure_bar < 29.5 THEN
            rValveCmd_CathodeBackpress_pct := 80.0;
        ELSE
            rValveCmd_CathodeBackpress_pct := 50.0;
        END_IF;

        (* Check pressure reached 29.0 bar, H2-in-O2 < 0.8%, and ignition timer expired (40 s) *)
        IF rMinLoadStartTimer_s >= 40.0 AND rVoted_AnodePressure_bar >= 29.0 AND
           rVoted_CathodePressure_bar >= 29.0 AND rVoted_H2_in_O2_Crossover_pct < 0.80 THEN
            rMinLoadStartTimer_s := 0.0;
            bValveCmd_H2_ProductOffSpecVent := FALSE; (* Route product to TSA dryer *)
            iNextFSM_State := 60;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 60: RENEWABLE_POWER_FOLLOWING_MPC
     * Autonomous closed-loop production, dynamic power splitting across 20 stacks tracking wind/solar fluctuations.
     * --------------------------------------------------------------------------------------------------------------- *)
    60:
        bPowerTrackingActive := TRUE;
        bSystemRunning := TRUE;

        (* Supervise Gas Crossover Proximity to Safety Margin (1.50 % vol) *)
        IF rVoted_H2_in_O2_Crossover_pct >= c_rH2Cross_Alarm_HI THEN
            iNextFSM_State := 90; (* Divert immediately to CROSSOVER_SAFETY_DERATE_HOLD *)
        END_IF;

        (* Check if supervisory stop requested *)
        IF NOT bEnableMaster THEN
            iNextFSM_State := 100; (* Controlled de-energization *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 70: DEOXO_PURIFICATION_PULSE
     * Catalytic palladium deoxo reactor temperature and moisture pacing, pulsing off-spec product gas.
     * --------------------------------------------------------------------------------------------------------------- *)
    70:
        bValveCmd_H2_ProductOffSpecVent := TRUE;
        IF rVoted_O2_in_H2_Crossover_pct < 0.010 AND rVoted_ProductH2_Dewpoint_degC < -70.0 THEN
            bValveCmd_H2_ProductOffSpecVent := FALSE;
            iNextFSM_State := 60;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 80: TSA_BED_DESORPTION_REGEN
     * Pacing dual-bed swing cycle execution.
     * --------------------------------------------------------------------------------------------------------------- *)
    80:
        IF bTSA_RegenAutoSequenceEnable THEN
            iNextFSM_State := 60;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 90: CROSSOVER_SAFETY_DERATE_HOLD
     * Gas permeation safety hold: Clamping power reduction, boosting cathode backpressure, holding until purge clears.
     * --------------------------------------------------------------------------------------------------------------- *)
    90:
        bCrossoverDerateActive := TRUE;
        bPowerTrackingActive := FALSE;
        rCrossoverDerateTimer_s := rCrossoverDerateTimer_s + c_rTs;

        (* Boost anode loop DI water circulation to sweep gas bubbles from MEA channels *)
        rPumpCmd_DI_WaterCirculation_pct := 95.0;

        (* Modulate backpressure valves to eliminate negative differential pressure *)
        IF rVoted_MembraneDiffPressure_bar < 0.010 THEN
            rValveCmd_CathodeBackpress_pct := rValveCmd_CathodeBackpress_pct + 1.5;
        END_IF;

        (* Recover to normal operation once H2 in O2 drops below 1.10% (hysteresis clear) *)
        IF rVoted_H2_in_O2_Crossover_pct <= (c_rH2Cross_Alarm_HI - c_rH2Cross_Deadband) AND rCrossoverDerateTimer_s >= 20.0 THEN
            bCrossoverDerateActive := FALSE;
            rCrossoverDerateTimer_s := 0.0;
            iNextFSM_State := 60;
        END_IF;

        (* If crossover continues rising above 1.90%, fast trip to emergency vent *)
        IF rVoted_H2_in_O2_Crossover_pct >= c_rH2Cross_Trip_HI_HI THEN
            iNextFSM_State := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 100: CONTROLLED_DE_ENERGIZATION
     * Orderly ramp-down of all 20 rectifiers at 10.0 MW/s to zero load, maintaining differential pressure balance.
     * --------------------------------------------------------------------------------------------------------------- *)
    100:
        bPowerTrackingActive := FALSE;
        rDeenergizationRampTimer_s := rDeenergizationRampTimer_s + c_rTs;

        (* Ramp power setpoint to zero *)
        IF rFilteredTargetPower_MW > 0.50 THEN
            rFilteredTargetPower_MW := rFilteredTargetPower_MW - 10.0 * c_rTs;
        ELSE
            rFilteredTargetPower_MW := 0.0;
        END_IF;

        IF rFilteredTargetPower_MW <= 0.05 OR rDeenergizationRampTimer_s >= 15.0 THEN
            rDeenergizationRampTimer_s := 0.0;
            iNextFSM_State := 110;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 110: N2_FLUSH_STANDBY_PARK
     * Depressurizing to 2.0 bar, flushing headers with dry N2 until H2 < 0.2% and O2 < 0.5%.
     * --------------------------------------------------------------------------------------------------------------- *)
    110:
        rN2FlushStandbyTimer_s := rN2FlushStandbyTimer_s + c_rTs;
        bValveCmd_H2_ProductOffSpecVent := TRUE;
        bValveCmd_N2_PurgeSupplyMain := TRUE;
        rValveCmd_CathodeBackpress_pct := 15.0;
        rValveCmd_AnodeBackpress_pct := 15.0;
        rPumpCmd_DI_WaterCirculation_pct := 20.0;

        (* Maintain flush for 60.0 seconds *)
        IF rN2FlushStandbyTimer_s >= 60.0 AND rVoted_CathodePressure_bar <= 2.5 AND rVoted_AnodePressure_bar <= 2.5 THEN
            rN2FlushStandbyTimer_s := 0.0;
            bValveCmd_N2_PurgeSupplyMain := FALSE;
            iNextFSM_State := 10; (* Park in SYSTEM_OFFLINE_N2_PURGED *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STATE 120: EMERGENCY_ESTOP_VENT
     * Instantaneous SIL-3 DC breaker fast trip (< 10 ms), opening fast dump depressurization valves, N2 auto-blast.
     * --------------------------------------------------------------------------------------------------------------- *)
    120:
        bSystemTripped := TRUE;
        bSystemRunning := FALSE;
        bPowerTrackingActive := FALSE;
        bFastPurgeActive := TRUE;
        rEStopVentTimer_s := rEStopVentTimer_s + c_rTs;

        (* Trip All 20 DC Breakers Immediately *)
        FOR iIdx := 1 TO 20 DO
            aStackBreakerTripCmd[iIdx] := TRUE;
            aStackPowerCmd_MW[iIdx] := 0.0;
            aStackCurrentCmd_A[iIdx] := 0.0;
        END_FOR;

        (* Fire Nitrogen Auto-Blast Purge Valve *)
        bValveCmd_N2_PurgeSupplyMain := TRUE;
        bValveCmd_H2_ProductOffSpecVent := TRUE;

        (* Fast Depressurization *)
        rValveCmd_CathodeBackpress_pct := 0.0;
        rValveCmd_AnodeBackpress_pct := 0.0;
        rPumpCmd_DI_WaterCirculation_pct := 0.0;
        rPumpCmd_MainCoolingLoop_pct := 0.0;

        (* Latch Trip until Reset Command Received in De-Pressurized State *)
        IF bFaultReset AND bEmergencyStop_NC AND rVoted_CathodePressure_bar <= 1.5 AND rVoted_AnodePressure_bar <= 1.5 THEN
            bSystemTripped := FALSE;
            bFastPurgeActive := FALSE;
            bValveCmd_N2_PurgeSupplyMain := FALSE;
            FOR iIdx := 1 TO 20 DO
                aStackBreakerTripCmd[iIdx] := FALSE;
            END_FOR;
            iNextFSM_State := 10;
        END_IF;
END_CASE;

(* Update State Indices *)
iPrevFSM_State := iFSM_State;
IF iNextFSM_State <> iFSM_State THEN
    iFSM_State := iNextFSM_State;
    rStateTimer_s := 0.0;
END_IF;
nActiveFSM_State := iFSM_State;

(* ===================================================================================================================
 * PHASE 6: TSA DUAL-BED DEOXO / DRYER SWING REGENERATION PACING
 * =================================================================================================================== *)
IF bTSA_RegenAutoSequenceEnable AND bSystemRunning THEN
    rTSA_CycleTimer_s := rTSA_CycleTimer_s + c_rTs;

    CASE iTSA_Step OF
        1: (* Bed 1 Adsorbing at 30 bar / Bed 2 Thermal Desorption & Purge *)
            bValveCmd_TSA_Bed1_Adsorption := TRUE;
            bValveCmd_TSA_Bed1_Desorption := FALSE;
            bValveCmd_TSA_Bed1_Depress := FALSE;

            IF rTSA_CycleTimer_s < c_rTSA_DesorptionHeatingTime_s THEN
                (* Heating Phase: Bed 2 heated to 180.0 deg C *)
                bValveCmd_TSA_Bed2_Adsorption := FALSE;
                bValveCmd_TSA_Bed2_Desorption := TRUE;
                bValveCmd_TSA_Bed2_Depress := FALSE;
                rHeaterCmd_TSA_RegenHeater_pct := 90.0;
            ELSIF rTSA_CycleTimer_s < (c_rTSA_DesorptionHeatingTime_s + c_rTSA_CoolingPurgeTime_s) THEN
                (* Cooling Phase: Bed 2 cooled with dry slip stream *)
                rHeaterCmd_TSA_RegenHeater_pct := 0.0;
                bValveCmd_TSA_Bed2_Desorption := TRUE;
            ELSE
                (* Re-pressurize Bed 2 to 30.0 bar *)
                bValveCmd_TSA_Bed2_Desorption := FALSE;
                bValveCmd_TSA_Bed2_Depress := FALSE;
            END_IF;

            IF rTSA_CycleTimer_s >= c_rTSA_HalfCycleDuration_s THEN
                rTSA_CycleTimer_s := 0.0;
                iTSA_Step := 2; (* Switch to Bed 2 Adsorption *)
            END_IF;

        2: (* Bed 2 Adsorbing at 30 bar / Bed 1 Thermal Desorption & Purge *)
            bValveCmd_TSA_Bed2_Adsorption := TRUE;
            bValveCmd_TSA_Bed2_Desorption := FALSE;
            bValveCmd_TSA_Bed2_Depress := FALSE;

            IF rTSA_CycleTimer_s < c_rTSA_DesorptionHeatingTime_s THEN
                bValveCmd_TSA_Bed1_Adsorption := FALSE;
                bValveCmd_TSA_Bed1_Desorption := TRUE;
                bValveCmd_TSA_Bed1_Depress := FALSE;
                rHeaterCmd_TSA_RegenHeater_pct := 90.0;
            ELSIF rTSA_CycleTimer_s < (c_rTSA_DesorptionHeatingTime_s + c_rTSA_CoolingPurgeTime_s) THEN
                rHeaterCmd_TSA_RegenHeater_pct := 0.0;
                bValveCmd_TSA_Bed1_Desorption := TRUE;
            ELSE
                bValveCmd_TSA_Bed1_Desorption := FALSE;
                bValveCmd_TSA_Bed1_Depress := FALSE;
            END_IF;

            IF rTSA_CycleTimer_s >= c_rTSA_HalfCycleDuration_s THEN
                rTSA_CycleTimer_s := 0.0;
                iTSA_Step := 1; (* Cycle back to Bed 1 Adsorption *)
            END_IF;
    END_CASE;
ELSE
    rHeaterCmd_TSA_RegenHeater_pct := 0.0;
END_IF;

(* ===================================================================================================================
 * PHASE 7: ISA-18.2 ALARMS & DIAGNOSTIC WORD BIT PACKING
 * =================================================================================================================== *)
(* 7.1 Rate-of-Change (ROC) Calculations *)
rROC_H2Cross := ABS(rVoted_H2_in_O2_Crossover_pct - rPrev_H2Cross) / c_rTs;
rROC_DP := ABS(rVoted_MembraneDiffPressure_bar - rPrev_DP) / c_rTs;
rROC_StackTemp := ABS(rVoted_CoolingOutletTemp_degC - rPrev_StackTemp) / c_rTs;

rPrev_H2Cross := rVoted_H2_in_O2_Crossover_pct;
rPrev_DP := rVoted_MembraneDiffPressure_bar;
rPrev_StackTemp := rVoted_CoolingOutletTemp_degC;

(* 7.2 H2-in-O2 Permeation Alarms *)
IF rVoted_H2_in_O2_Crossover_pct >= c_rH2Cross_Trip_HI_HI THEN
    bAlarm_H2Cross_HI_HI := TRUE;
ELSIF rVoted_H2_in_O2_Crossover_pct <= (c_rH2Cross_Trip_HI_HI - c_rH2Cross_Deadband) THEN
    bAlarm_H2Cross_HI_HI := FALSE;
END_IF;

IF rVoted_H2_in_O2_Crossover_pct >= c_rH2Cross_Alarm_HI THEN
    bAlarm_H2Cross_HI := TRUE;
ELSIF rVoted_H2_in_O2_Crossover_pct <= (c_rH2Cross_Alarm_HI - c_rH2Cross_Deadband) THEN
    bAlarm_H2Cross_HI := FALSE;
END_IF;

IF rROC_H2Cross >= c_rH2Cross_Max_ROC THEN
    bAlarm_H2Cross_ROC := TRUE;
ELSE
    bAlarm_H2Cross_ROC := FALSE;
END_IF;

(* 7.3 Membrane Differential Pressure Alarms *)
IF rVoted_MembraneDiffPressure_bar >= c_rDP_Trip_HI_HI THEN
    bAlarm_DP_HI_HI := TRUE;
ELSIF rVoted_MembraneDiffPressure_bar <= (c_rDP_Trip_HI_HI - c_rDP_Deadband) THEN
    bAlarm_DP_HI_HI := FALSE;
END_IF;

IF rVoted_MembraneDiffPressure_bar >= c_rDP_Alarm_HI THEN
    bAlarm_DP_HI := TRUE;
ELSIF rVoted_MembraneDiffPressure_bar <= (c_rDP_Alarm_HI - c_rDP_Deadband) THEN
    bAlarm_DP_HI := FALSE;
END_IF;

IF rVoted_MembraneDiffPressure_bar <= c_rDP_Alarm_LO THEN
    bAlarm_DP_LO := TRUE;
ELSIF rVoted_MembraneDiffPressure_bar >= (c_rDP_Alarm_LO + c_rDP_Deadband) THEN
    bAlarm_DP_LO := FALSE;
END_IF;

IF rVoted_MembraneDiffPressure_bar <= c_rDP_Trip_LO_LO THEN
    bAlarm_DP_LO_LO := TRUE;
ELSIF rVoted_MembraneDiffPressure_bar >= (c_rDP_Trip_LO_LO + c_rDP_Deadband) THEN
    bAlarm_DP_LO_LO := FALSE;
END_IF;

(* 7.4 Stack Core Operating Temperature Alarms *)
IF rVoted_CoolingOutletTemp_degC >= c_rStackTemp_Trip_HI_HI THEN
    bAlarm_StackTemp_HI_HI := TRUE;
ELSIF rVoted_CoolingOutletTemp_degC <= (c_rStackTemp_Trip_HI_HI - c_rStackTemp_Deadband) THEN
    bAlarm_StackTemp_HI_HI := FALSE;
END_IF;

IF rVoted_CoolingOutletTemp_degC >= c_rStackTemp_Alarm_HI THEN
    bAlarm_StackTemp_HI := TRUE;
ELSIF rVoted_CoolingOutletTemp_degC <= (c_rStackTemp_Alarm_HI - c_rStackTemp_Deadband) THEN
    bAlarm_StackTemp_HI := FALSE;
END_IF;

IF rVoted_CoolingOutletTemp_degC <= c_rStackTemp_Alarm_LO THEN
    bAlarm_StackTemp_LO := TRUE;
ELSIF rVoted_CoolingOutletTemp_degC >= (c_rStackTemp_Alarm_LO + c_rStackTemp_Deadband) THEN
    bAlarm_StackTemp_LO := FALSE;
END_IF;

IF rVoted_CoolingOutletTemp_degC <= c_rStackTemp_Trip_LO_LO THEN
    bAlarm_StackTemp_LO_LO := TRUE;
ELSIF rVoted_CoolingOutletTemp_degC >= (c_rStackTemp_Trip_LO_LO + c_rStackTemp_Deadband) THEN
    bAlarm_StackTemp_LO_LO := FALSE;
END_IF;

(* 7.5 DI Water Electrical Conductivity Alarms *)
IF rVoted_DI_WaterConductivity_uScm >= c_rConductivity_Trip_HI_HI THEN
    bAlarm_Conductivity_HI_HI := TRUE;
ELSIF rVoted_DI_WaterConductivity_uScm <= (c_rConductivity_Trip_HI_HI - c_rConductivity_Deadband) THEN
    bAlarm_Conductivity_HI_HI := FALSE;
END_IF;

IF rVoted_DI_WaterConductivity_uScm >= c_rConductivity_Alarm_HI THEN
    bAlarm_Conductivity_HI := TRUE;
ELSIF rVoted_DI_WaterConductivity_uScm <= (c_rConductivity_Alarm_HI - c_rConductivity_Deadband) THEN
    bAlarm_Conductivity_HI := FALSE;
END_IF;

(* 7.6 Final Product Dewpoint Alarm *)
IF rVoted_ProductH2_Dewpoint_degC >= -70.0 THEN
    bAlarm_Dewpoint_HI := TRUE;
ELSE
    bAlarm_Dewpoint_HI := FALSE;
END_IF;

(* 7.7 Bit-Packing Diagnostic Words *)
(* dwSystemStatusWord *)
dwSystemStatusWord := 16#0000_0000;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bPowerTrackingActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bCrossoverDerateActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bFastPurgeActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bTSA_RegenAutoSequenceEnable THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iFSM_State), 8);

(* dwProcessAlarmWord *)
dwProcessAlarmWord := 16#0000_0000;
IF bAlarm_H2Cross_HI THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0001; END_IF;
IF bAlarm_H2Cross_ROC THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0002; END_IF;
IF bAlarm_DP_HI THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0004; END_IF;
IF bAlarm_DP_LO THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0008; END_IF;
IF bAlarm_StackTemp_HI THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0010; END_IF;
IF bAlarm_StackTemp_LO THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0020; END_IF;
IF bAlarm_Conductivity_HI THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0040; END_IF;
IF bAlarm_Dewpoint_HI THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0080; END_IF;
IF bAlarm_TMR_Degraded THEN dwProcessAlarmWord := dwProcessAlarmWord OR 16#0000_0100; END_IF;

(* dwCriticalSafetyTripWord *)
dwCriticalSafetyTripWord := 16#0000_0000;
IF NOT bEmergencyStop_NC THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0001; END_IF;
IF bAlarm_H2Cross_HI_HI THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0002; END_IF;
IF bAlarm_DP_HI_HI THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0004; END_IF;
IF bAlarm_DP_LO_LO THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0008; END_IF;
IF bAlarm_StackTemp_HI_HI THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0010; END_IF;
IF bAlarm_StackTemp_LO_LO THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0020; END_IF;
IF bAlarm_Conductivity_HI_HI THEN dwCriticalSafetyTripWord := dwCriticalSafetyTripWord OR 16#0000_0040; END_IF;

(* 7.8 Master Emergency Fast Trip Handler *)
IF dwCriticalSafetyTripWord <> 16#0000_0000 THEN
    bSystemTripped := TRUE;
    iNextFSM_State := 120; (* Transition directly to EMERGENCY_ESTOP_VENT *)
END_IF;

END_FUNCTION_BLOCK
```"""
