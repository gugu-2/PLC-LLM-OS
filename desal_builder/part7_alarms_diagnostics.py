# desal_builder/part7_alarms_diagnostics.py
# Phase 5: ISA-18.2 Multi-Tier Process Alarms, Bit-Packed Diagnostics & Block Closure

def get_part7_alarms_diagnostics():
    return """
(* ====================================================================================================
   PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM LOGIC & 32-BIT BIT-PACKED STATUS WORDS
   Manages Emergency Hard Trips, High/Low Process Warnings, Deadband Hysteresis,
   and First-Out Diagnostics for SCADA/DCS Historian Integration.
   ==================================================================================================== *)

(* ----------------------------------------------------------------------------------------------------
   STEP 5.1: CRITICAL EMERGENCY SAFETY TRIPS (TIER 1 - IMMEDIATE SHUTDOWN)
   ---------------------------------------------------------------------------------------------------- *)
(* Trip 1: High-High Membrane Feed Pressure PT-201 (Overpressure Rupture Protection) *)
IF rVoted_PT201_HpFeedPress_bar >= rSp_PT201_Trip_HH_bar THEN
    rTimer_Trip_PT201_HH_sec := rTimer_Trip_PT201_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_PT201_HH_sec >= 0.050 THEN (* 50 ms Fast Trip *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000020;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000020; (* First-Out Latch *)
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_PT201_HH_sec := 0.0;
END_IF;

(* Trip 2: Low-Low Feed Intake Pressure PT-101 (Centrifugal Pump Cavitation Prevention) *)
IF (nFsmState >= 4) AND (rVoted_PT101_IntakePress_bar <= rSp_PT101_Trip_LL_bar) THEN
    rTimer_Trip_PT101_LL_sec := rTimer_Trip_PT101_LL_sec + rCycleTime_sec;
    IF rTimer_Trip_PT101_LL_sec >= 0.500 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000040;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000040;
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_PT101_LL_sec := 0.0;
END_IF;

(* Trip 3: Feed Chlorine Redox Breakthrough AT-102 (Polyamide Active Skin Halogenation Protection) *)
IF (nFsmState >= 3) AND (rVoted_AT102_FeedOrp_mV >= rSp_AT102_Trip_HH_mV) THEN
    rTimer_Trip_AT102_HH_sec := rTimer_Trip_AT102_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_AT102_HH_sec >= 1.000 THEN (* 1.0 s Persistent Breakthrough *)
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000080;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000080;
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_AT102_HH_sec := 0.0;
END_IF;

(* Trip 4: ERD Differential Overpressure (Ceramic Rotor Stalling / Clearance Seizure) *)
IF (nFsmState >= 5) AND ((rVoted_PT201_HpFeedPress_bar - rVoted_PT501_PxDischPress_bar) >= rSp_DP_Erd_Trip_HH_bar) THEN
    rTimer_Trip_DPErd_HH_sec := rTimer_Trip_DPErd_HH_sec + rCycleTime_sec;
    IF rTimer_Trip_DPErd_HH_sec >= 1.500 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000100;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000100;
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_DPErd_HH_sec := 0.0;
END_IF;

(* Trip 5: HPP Motor Bearing Temperature High-High *)
IF (rHppBearingTempDe_degC >= rSp_HppBearingTemp_Trip_HH_degC) 
   OR (rHppBearingTempNde_degC >= rSp_HppBearingTemp_Trip_HH_degC) THEN
    rTimer_Trip_BearingTemp_sec := rTimer_Trip_BearingTemp_sec + rCycleTime_sec;
    IF rTimer_Trip_BearingTemp_sec >= 2.000 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000200;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000200;
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_BearingTemp_sec := 0.0;
END_IF;

(* Trip 6: HPP Mechanical Vibration Velocity High-High *)
IF rHppVibrationRms_mms >= rSp_HppVibration_Trip_HH_mms THEN
    rTimer_Trip_Vibration_sec := rTimer_Trip_Vibration_sec + rCycleTime_sec;
    IF rTimer_Trip_Vibration_sec >= 1.000 THEN
        dwAlarmWord1 := dwAlarmWord1 OR 16#00000400;
        IF dwTripWord = 16#00000000 THEN
            dwTripWord := 16#00000400;
        END_IF;
    END_IF;
ELSE
    rTimer_Trip_Vibration_sec := 0.0;
END_IF;

(* Trip 7: Hardware Emergency Depressurization Pushbutton *)
IF bEmergencyDepressurize THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000800;
    IF dwTripWord = 16#00000000 THEN
        dwTripWord := 16#00000800;
    END_IF;
END_IF;

(* Global Critical Trip Summary Flag *)
bCriticalTripActive := (dwAlarmWord1 <> 16#00000000);

(* ----------------------------------------------------------------------------------------------------
   STEP 5.2: PROCESS WARNING ALARMS (TIER 2 - CLEARED WITH DEADBAND HYSTERESIS)
   ---------------------------------------------------------------------------------------------------- *)
(* Warning 1: High HP Feed Pressure *)
IF rVoted_PT201_HpFeedPress_bar >= rSp_PT201_Alarm_H_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000001;
ELSIF rVoted_PT201_HpFeedPress_bar <= (rSp_PT201_Alarm_H_bar - rAlarmHysteresis_bar) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000001;
END_IF;

(* Warning 2: Low Feed Intake Pressure *)
IF rVoted_PT101_IntakePress_bar <= rSp_PT101_Alarm_L_bar THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000002;
ELSIF rVoted_PT101_IntakePress_bar >= (rSp_PT101_Alarm_L_bar + rAlarmHysteresis_bar) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000002;
END_IF;

(* Warning 3: Feed ORP Elevated *)
IF rVoted_AT102_FeedOrp_mV >= rSp_AT102_Alarm_H_mV THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000004;
ELSIF rVoted_AT102_FeedOrp_mV <= (rSp_AT102_Alarm_H_mV - rAlarmHysteresis_mV) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000004;
END_IF;

(* Warning 4: Permeate Conductivity High *)
IF rVoted_AT301_PermConduct_uS >= rSp_AT301_Alarm_H_uS THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000008;
ELSIF rVoted_AT301_PermConduct_uS <= (rSp_AT301_Alarm_H_uS - rAlarmHysteresis_uS) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000008;
END_IF;

(* Warning 5: Permeate Conductivity Off-Spec Diverted *)
IF bPermeateOffSpecDiverted THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000010;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000010;
END_IF;

(* Warning 6: Cartridge Filter Differential Pressure High (Filter Clogging) *)
IF rCartridgeFilterDp_bar >= 0.95 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000020;
ELSIF rCartridgeFilterDp_bar <= 0.70 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000020;
END_IF;

(* Warning 7: Seawater Feed Temperature High (> 35 C increases scaling risk) *)
IF rRawSeawaterTemp_degC >= 35.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000040;
ELSIF rRawSeawaterTemp_degC <= 33.5 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000040;
END_IF;

(* Warning 8: Seawater Feed Silt Density Index SDI-15 High (> 4.0 fouling risk) *)
IF rRawSeawaterSdi15 >= 4.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000080;
ELSIF rRawSeawaterSdi15 <= 3.2 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000080;
END_IF;

(* Warning 9: Scaling Index High (S&DSI > 0.35) *)
IF rObservedScalingIndex_Lsi >= 0.35 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000100;
ELSIF rObservedScalingIndex_Lsi <= 0.20 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000100;
END_IF;

(* Warning 10: Chemical Day Tank Levels Low *)
IF rSbsDayTankLevel_pct <= 20.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000200;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000200;
END_IF;

IF rAntiscalantDayTankLevel_pct <= 20.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00000400;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00000400;
END_IF;

(* Warning 11: 2oo3 TMR Sensor Discordance & Degradation Flags *)
IF bDegraded_PT101 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00001000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00001000;
END_IF;

IF bDegraded_PT201 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00002000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00002000;
END_IF;

IF bDegraded_AT301 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00004000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00004000;
END_IF;

IF bDegraded_FT401 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00008000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00008000;
END_IF;

IF bDegraded_AT102 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00010000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00010000;
END_IF;

IF bDegraded_PT501 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00020000;
ELSE
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00020000;
END_IF;

(* Warning 12: High Specific Energy Consumption Warning (> 3.4 kWh/m3) *)
IF rObservedSpecificEnergy_kWh_m3 >= 3.40 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00040000;
ELSIF rObservedSpecificEnergy_kWh_m3 <= 3.10 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00040000;
END_IF;

(* Warning 13: ERD Efficiency Sub-optimal (< 91.0%) *)
IF rObservedErdEnergyRecovery_pct <= 91.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00080000;
ELSIF rObservedErdEnergyRecovery_pct >= 94.0 THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00080000;
END_IF;

(* Warning 14: Membrane Specific Permeability Loss > 15% (Clean-In-Place Recommended) *)
IF x_state[8] <= (rCleanMembranePermeability_Kw0 * 0.85) THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#00100000;
ELSIF x_state[8] >= (rCleanMembranePermeability_Kw0 * 0.92) THEN
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#00100000;
END_IF;

(* Global Warning Alarm Summary Flag *)
bWarningAlarmActive := (dwAlarmWord2 <> 16#00000000);

(* Fault Reset Handler: Clears Latched Emergency Trips upon Operator Pushbutton *)
IF bResetFault AND NOT bEmergencyDepressurize THEN
    IF (rVoted_PT201_HpFeedPress_bar < rSp_PT201_Alarm_H_bar) 
       AND (rVoted_AT102_FeedOrp_mV < rSp_AT102_Alarm_H_mV) THEN
        dwAlarmWord1 := 16#00000000;
        bCriticalTripActive := FALSE;
    END_IF;
END_IF;

(* ----------------------------------------------------------------------------------------------------
   STEP 5.3: BIT-PACKED OPERATIONAL STATUS WORD ASSEMBLY
   ---------------------------------------------------------------------------------------------------- *)
dwStatusWord := 16#00000000;
IF bInitialized THEN
    dwStatusWord := dwStatusWord OR 16#00000001; (* Bit 0: System Initialized *)
END_IF;
IF bEnable THEN
    dwStatusWord := dwStatusWord OR 16#00000002; (* Bit 1: Auto Remote Permissive *)
END_IF;
IF bSystemRunning THEN
    dwStatusWord := dwStatusWord OR 16#00000004; (* Bit 2: Production Running *)
END_IF;
IF bSequenceComplete THEN
    dwStatusWord := dwStatusWord OR 16#00000008; (* Bit 3: Steady State Reached *)
END_IF;
IF NOT bPermeateOffSpecDiverted AND bSystemRunning THEN
    dwStatusWord := dwStatusWord OR 16#00000010; (* Bit 4: Permeate Quality On-Spec *)
END_IF;
IF bPermeateOffSpecDiverted THEN
    dwStatusWord := dwStatusWord OR 16#00000020; (* Bit 5: Permeate Off-Spec Diverted *)
END_IF;
IF bCipCycleActive THEN
    dwStatusWord := dwStatusWord OR 16#00000040; (* Bit 6: CIP Chemical Cleaning Active *)
END_IF;
IF nFsmState = 10 THEN
    dwStatusWord := dwStatusWord OR 16#00000080; (* Bit 7: Scheduled LP Flush Active *)
END_IF;

(* Bits 8..15: Active Deterministic FSM State Code *)
dwStatusWord := dwStatusWord OR SHL(INT_TO_DWORD(nFsmState), 8);

(* Bit 16: MPC Active Optimization Engaged *)
IF (nFsmState = 7) OR (nFsmState = 8) OR (nFsmState = 9) THEN
    dwStatusWord := dwStatusWord OR 16#00010000;
END_IF;

(* Bit 17: TMR Instrument Degradation *)
IF bDegraded_PT101 OR bDegraded_PT201 OR bDegraded_AT301 
   OR bDegraded_FT401 OR bDegraded_AT102 OR bDegraded_PT501 THEN
    dwStatusWord := dwStatusWord OR 16#00020000;
END_IF;

(* Bit 18: Critical Safety Hard Trip Active *)
IF bCriticalTripActive THEN
    dwStatusWord := dwStatusWord OR 16#00040000;
END_IF;

(* Bit 19: Process Warning Alarm Active *)
IF bWarningAlarmActive THEN
    dwStatusWord := dwStatusWord OR 16#00080000;
END_IF;

(* ----------------------------------------------------------------------------------------------------
   STEP 5.4: EXECUTION SCAN COUNTER & ACTUATOR COMMAND STATE STORE
   ---------------------------------------------------------------------------------------------------- *)
nScanCounter := nScanCounter + 1;
u_prev[1] := rHppVfdSpeedReference_Hz;
u_prev[2] := rPxBpVfdSpeedReference_Hz;
u_prev[3] := rBrineThrottleValveCmd_pct;
u_prev[4] := rAntiscalantDosingStroke_pct;
u_prev[5] := rSbsDosingPumpStroke_pct;
u_prev[6] := rPermeateDivertValveCmd_pct;

END_FUNCTION_BLOCK
"""
