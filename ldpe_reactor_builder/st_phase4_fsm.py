# ldpe_reactor_builder/st_phase4_fsm.py

def get_phase4_fsm():
    return """(* ============================================================================================== *)
(* PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)                          *)
(* STATES 0 TO 13 WITH SAFETY INTERLOCKS, STEP TIMERS, TRANSITION GUARDS & HPLDV PULSATION RUN     *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* GLOBAL SAFETY OVERRIDE: SUB-5 MS EXPLOSIVE DECOMPOSITION OR MANUAL EMERGENCY TRIP             *)
(* Immediately forces state transition to STATE 13 regardless of active operating phase          *)
(* ---------------------------------------------------------------------------------------------- *)
IF (bDecompDetected OR bEmergencyTrip OR bDecomp_TripQualified) AND (iState <> STATE_EMERGENCY_DECOMP_SNORT) THEN
    iPreviousState := iState;
    iState := STATE_EMERGENCY_DECOMP_SNORT;
    tStateTimer_s := 0.0;
    bStateFirstScan := TRUE;
END_IF;

(* Track State Elapsed Time *)
tStateTimer_s := tStateTimer_s + tScanCycleTime_s;

CASE iState OF

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 0: STATE_IDLE - COLD STANDBY & SAFETY PERMISSIVE AUDIT                               *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_IDLE:
        iActiveStateNumber := 0;
        rStateProgress_pct := 0.0;
        bPulsePhaseActive := FALSE;
        bHPLDV_InPulseExecution := FALSE;

        (* Safe Standby Actuator Outputs *)
        rCmd_HyperComp_SpeedTrim_pct        := 0.0;
        rCmd_PeroxidePump1_Stroke_pct       := 0.0;
        rCmd_PeroxidePump2_Stroke_pct       := 0.0;
        rCmd_PeroxidePump3_Stroke_pct       := 0.0;
        rCmd_PeroxidePump4_Stroke_pct       := 0.0;
        rCmd_HPLDV_Position_pct             := 0.0; (* Letdown closed or minimal crack *)
        rCmd_JacketWater_TemperingValve_pct := 0.0;
        rCmd_JacketWater_BoosterPump_pct    := 25.0;(* Minimum circulation to prevent stagnation *)
        rCmd_CTA_DosingPump_pct             := 0.0;
        bCmd_SnortValve_EmergencyDump       := FALSE;
        bCmd_HyperComp_EmergencyTrip        := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed   := TRUE;(* Blocked in idle *)
        bCmd_JacketWater_ColdDelugeTrip     := FALSE;
        bCmd_HPLDV_PulseActive              := FALSE;

        (* State Transition Permissives *)
        IF bEnable AND bStartProduction AND (rTMR_Health_Overall_pct >= 75.0) AND (NOT bLatched_Press_HH) THEN
            iPreviousState := STATE_IDLE;
            iState := STATE_JACKET_WATER_PREHEAT;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 1: STATE_JACKET_WATER_PREHEAT_CIRCULATION_WARMUP                                     *)
    (* Circulates 180 C pressurized hot water through jackets to preheat 1,500 m tube             *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_JACKET_WATER_PREHEAT:
        iActiveStateNumber := 1;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        (* Modulate Tempering Valve to Ramp Water Temperature to 180 C *)
        rCmd_JacketWater_TemperingValve_pct := 85.0;
        rCmd_JacketWater_BoosterPump_pct    := 90.0;
        rCmd_HPLDV_Position_pct             := 5.0; (* Low purge position *)

        (* Calculate Warmup Progress Metric *)
        IF rJacketWater_SupplyTemp_degC < 180.0 THEN
            rStateProgress_pct := (rJacketWater_SupplyTemp_degC / 180.0) * 100.0;
        ELSE
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Jacket Water Reaches 175 C and Soak Time >= 120 s *)
        IF (rJacketWater_SupplyTemp_degC >= 175.0) AND (tStateTimer_s >= 120.0) THEN
            iPreviousState := STATE_JACKET_WATER_PREHEAT;
            iState := STATE_ETHYLENE_GAS_PRESS_1000;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 2: STATE_ETHYLENE_GAS_PRESSURIZATION_RAMP_1000BAR                                   *)
    (* Primary compressor pressurizes 1,500 m tube with fresh/recycle ethylene to 1,000 bar       *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_ETHYLENE_GAS_PRESS_1000:
        iActiveStateNumber := 2;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        (* Maintain Jacket Tempering at 180 C to prevent monomer phase condensation *)
        rCmd_JacketWater_TemperingValve_pct := 65.0;
        rCmd_JacketWater_BoosterPump_pct    := 80.0;
        rCmd_HPLDV_Position_pct             := 8.0; (* Pressure holding crack *)

        (* Progress Metric: 0 to 1,000 bar ramp *)
        rStateProgress_pct := (rVoted_ReactorPressure_bar / 1000.0) * 100.0;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Inlet Pressure reaches 980 bar with zero excessive dP/dt *)
        IF (rVoted_ReactorPressure_bar >= 980.0) AND (ABS(rEst_RateOfPressureRise_bar_s) < 50.0) AND (tStateTimer_s >= 60.0) THEN
            iPreviousState := STATE_ETHYLENE_GAS_PRESS_1000;
            iState := STATE_HYPER_COMPRESSOR_SPINUP;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 3: STATE_HYPER_COMPRESSOR_SPINUP_TO_3000BAR                                         *)
    (* Plungers load up, ramping pressure from 1,000 bar to 3,000 bar supercritical state         *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_HYPER_COMPRESSOR_SPINUP:
        iActiveStateNumber := 3;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        (* Ramp Hyper-Compressor Throughput Trim & Modulate Letdown Valve *)
        rCmd_HyperComp_SpeedTrim_pct        := 5.0;
        rCmd_HPLDV_Position_pct             := 18.0;
        rCmd_JacketWater_TemperingValve_pct := 55.0;
        rCmd_JacketWater_BoosterPump_pct    := 85.0;

        (* Progress: 1,000 to 3,000 bar *)
        IF rVoted_ReactorPressure_bar > 1000.0 THEN
            rStateProgress_pct := ((rVoted_ReactorPressure_bar - 1000.0) / 2000.0) * 100.0;
        ELSE
            rStateProgress_pct := 0.0;
        END_IF;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Reactor Pressure >= 2,950 bar and Hyper-Compressor Seal Oil Healthy *)
        IF (rVoted_ReactorPressure_bar >= 2950.0) AND (rHyperComp_SealOilDiffPress_bar >= 100.0) AND (tStateTimer_s >= 90.0) THEN
            iPreviousState := STATE_HYPER_COMPRESSOR_SPINUP;
            iState := STATE_INITIATOR_PRIME_AIR_EXPUL;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 4: STATE_INITIATOR_COCKTAIL_PRIME_AND_AIR_EXPULSION                                  *)
    (* Diaphragm micro-metering pumps de-aerated, lines primed with organic peroxide / solvent   *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_INITIATOR_PRIME_AIR_EXPUL:
        iActiveStateNumber := 4;
        bPulsePhaseActive := FALSE;

        (* Maintain Steady Supercritical Flow at 3,000 bar *)
        rCmd_HyperComp_SpeedTrim_pct        := 0.0;
        rCmd_HPLDV_Position_pct             := 25.0;
        rCmd_JacketWater_TemperingValve_pct := 50.0;
        rCmd_JacketWater_BoosterPump_pct    := 75.0;

        (* Prime Dosing Pumps at Low Stroke (Recirculation Mode) *)
        rCmd_PeroxidePump1_Stroke_pct := 10.0;
        rCmd_PeroxidePump2_Stroke_pct := 10.0;
        rCmd_PeroxidePump3_Stroke_pct := 10.0;
        rCmd_PeroxidePump4_Stroke_pct := 10.0;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE; (* Ready for injection *)

        rStateProgress_pct := (tStateTimer_s / 30.0) * 100.0;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Prime Timer Complete (30 s) & Peroxide Coriolis Meters Flowing *)
        IF (tStateTimer_s >= 30.0) AND (rVoted_PeroxideFlow_kgh >= 5.0) THEN
            iPreviousState := STATE_INITIATOR_PRIME_AIR_EXPUL;
            iState := STATE_FIRST_ZONE_PEROXIDE_IGNIT;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 5: STATE_FIRST_ZONE_PEROXIDE_INJECTION_IGNITION                                      *)
    (* Inject low-temperature peroxide cocktail into Zone 1, igniting exothermic polymerization   *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_FIRST_ZONE_PEROXIDE_IGNIT:
        iActiveStateNumber := 5;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE;

        (* Step Up Zone 1 Peroxide Flow to Light-Off Reaction *)
        rCmd_PeroxidePump1_Stroke_pct := 35.0;
        rCmd_PeroxidePump2_Stroke_pct := 5.0;
        rCmd_PeroxidePump3_Stroke_pct := 0.0;
        rCmd_PeroxidePump4_Stroke_pct := 0.0;
        rCmd_HPLDV_Position_pct       := 26.5;

        (* Track Reaction Light-Off: Zone 1 Temperature Rising Above 220 C *)
        IF rTemp_Zone1_Reaction_degC > 180.0 THEN
            rStateProgress_pct := ((rTemp_Zone1_Reaction_degC - 180.0) / 80.0) * 100.0;
        ELSE
            rStateProgress_pct := 0.0;
        END_IF;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Exotherm Established (Zone 1 Temp >= 245 C and dT/dt > 0.5 K/s) *)
        IF (rTemp_Zone1_Reaction_degC >= 245.0) AND (rVoted_PeakTemperature_degC >= 250.0) THEN
            iPreviousState := STATE_FIRST_ZONE_PEROXIDE_IGNIT;
            iState := STATE_NOMINAL_EXOTHERMIC_RUN;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 6: STATE_NOMINAL_EXOTHERMIC_POLYMERIZATION_RUN                                       *)
    (* Full multi-zone steady production running under closed-loop MPC and state-space observer    *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_NOMINAL_EXOTHERMIC_RUN:
        iActiveStateNumber := 6;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE;
        rStateProgress_pct := 100.0;

        (* Normal Closed-Loop Regulation via MPC Phase 3 Outputs *)
        (* Check if Cyclic Pulsation De-Fouling Should Start *)
        IF tStateTimer_s >= 45.0 THEN
            iPreviousState := STATE_NOMINAL_EXOTHERMIC_RUN;
            iState := STATE_CYCLIC_LETDOWN_PULSE_RUN;
            tStateTimer_s := 0.0;
            tHPLDV_PulseCycleTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

        (* Over-Temperature Protection Guard *)
        IF rVoted_PeakTemperature_degC >= rAlarm_Temp_H_degC THEN
            iPreviousState := STATE_NOMINAL_EXOTHERMIC_RUN;
            iState := STATE_PEAK_TEMP_LIMITING_TRIM;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

        (* Turndown Request *)
        IF bControlledTurndown THEN
            iPreviousState := STATE_NOMINAL_EXOTHERMIC_RUN;
            iState := STATE_CONTROLLED_TURNDOWN_FLUSH;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 7: STATE_CYCLIC_LETDOWN_PULSE_WALL_DE-FOULING_RUN                                    *)
    (* Executes periodic 250-bar letdown pulses every 20 seconds to scour stagnant gel layer      *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_CYCLIC_LETDOWN_PULSE_RUN:
        iActiveStateNumber := 7;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE;
        rStateProgress_pct := 100.0;

        (* Cyclic Pulsation Sequence Timer *)
        tHPLDV_PulseCycleTimer_s := tHPLDV_PulseCycleTimer_s + tScanCycleTime_s;

        IF (NOT bHPLDV_InPulseExecution) AND (tHPLDV_PulseCycleTimer_s >= rRecipe_HPLDV_PulseInterval_s) THEN
            (* Trigger Pulse Phase *)
            bHPLDV_InPulseExecution := TRUE;
            bPulsePhaseActive := TRUE;
            bCmd_HPLDV_PulseActive := TRUE;
            tHPLDV_PulsePhaseTimer_s := 0.0;
            rMeasured_PrePulsePress_bar := rVoted_ReactorPressure_bar;
            rMeasured_MinPulsePress_bar := rVoted_ReactorPressure_bar;
            tHPLDV_PulseCycleTimer_s := 0.0;
        END_IF;

        IF bHPLDV_InPulseExecution THEN
            tHPLDV_PulsePhaseTimer_s := tHPLDV_PulsePhaseTimer_s + tScanCycleTime_s;

            (* Step Open Letdown Valve to Pulse Stroke (42%) to create acoustic negative wave *)
            rCmd_HPLDV_Position_pct := rHPLDV_PulseStepStroke_pct;

            (* Track Minimum Pressure Reached *)
            IF rVoted_ReactorPressure_bar < rMeasured_MinPulsePress_bar THEN
                rMeasured_MinPulsePress_bar := rVoted_ReactorPressure_bar;
            END_IF;

            (* Calculate Measured Pulse Amplitude *)
            rEst_HPLDV_PulseAmplitude_bar := rMeasured_PrePulsePress_bar - rMeasured_MinPulsePress_bar;

            (* Pulse Duration Check (Nominal 0.85 s) *)
            IF tHPLDV_PulsePhaseTimer_s >= rRecipe_HPLDV_PulseDuration_s THEN
                (* End Pulse and Return to MPC Baseline *)
                bHPLDV_InPulseExecution := FALSE;
                bPulsePhaseActive := FALSE;
                bCmd_HPLDV_PulseActive := FALSE;
                tHPLDV_PulsePhaseTimer_s := 0.0;
                iTotalPulseCyclesCompleted := iTotalPulseCyclesCompleted + 1;
            END_IF;
        ELSE
            bPulsePhaseActive := FALSE;
            bCmd_HPLDV_PulseActive := FALSE;
        END_IF;

        (* Transitions *)
        IF rVoted_PeakTemperature_degC >= rAlarm_Temp_H_degC THEN
            iPreviousState := STATE_CYCLIC_LETDOWN_PULSE_RUN;
            iState := STATE_PEAK_TEMP_LIMITING_TRIM;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSIF bControlledTurndown THEN
            iPreviousState := STATE_CYCLIC_LETDOWN_PULSE_RUN;
            iState := STATE_CONTROLLED_TURNDOWN_FLUSH;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 8: STATE_DYNAMIC_GRADE_MFI_DENSITY_TRANSITION                                        *)
    (* Smoothly transitions reaction setpoints (CTA ppm, Peak T, Operating P) to new recipe      *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_DYNAMIC_GRADE_TRANSITION:
        iActiveStateNumber := 8;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE;

        (* Grade Transition Progress: MFI convergence *)
        rTempCalc1 := ABS(vecX_Est[iState_MFI] - rRecipe_TargetMFI_g10min);
        IF rTempCalc1 < 0.15 THEN
            rStateProgress_pct := 100.0;
            (* Return to Nominal Cyclic Pulse Run *)
            iPreviousState := STATE_DYNAMIC_GRADE_TRANSITION;
            iState := STATE_CYCLIC_LETDOWN_PULSE_RUN;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        ELSE
            rStateProgress_pct := (1.0 - (rTempCalc1 / 2.0)) * 100.0;
            IF rStateProgress_pct < 0.0 THEN
                rStateProgress_pct := 0.0;
            END_IF;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 9: STATE_PEAK_TEMPERATURE_LIMITING_AUTO_TRIM                                         *)
    (* Protective auto-throttle: cuts peroxide flow to hottest zone & maximizes jacket cooling    *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_PEAK_TEMP_LIMITING_TRIM:
        iActiveStateNumber := 9;
        bCmd_Peroxide_EmergencyBlockBleed := FALSE;

        (* Throttle Peroxide Pumps by 35% *)
        rCmd_PeroxidePump1_Stroke_pct := rCmd_PeroxidePump1_Stroke_pct * 0.65;
        rCmd_PeroxidePump2_Stroke_pct := rCmd_PeroxidePump2_Stroke_pct * 0.65;
        rCmd_PeroxidePump3_Stroke_pct := rCmd_PeroxidePump3_Stroke_pct * 0.65;
        rCmd_PeroxidePump4_Stroke_pct := rCmd_PeroxidePump4_Stroke_pct * 0.65;

        (* Maximize Pressurized Jacket Cooling *)
        rCmd_JacketWater_TemperingValve_pct := 10.0; (* Cold blend injection *)
        rCmd_JacketWater_BoosterPump_pct    := 100.0;

        rStateProgress_pct := 50.0;

        (* Transition Guard: Peak Temperature Restored Below Warning Deadband *)
        IF rVoted_PeakTemperature_degC <= (rAlarm_Temp_H_degC - rAlarm_Temp_Deadband_degC) THEN
            iPreviousState := STATE_PEAK_TEMP_LIMITING_TRIM;
            iState := STATE_CYCLIC_LETDOWN_PULSE_RUN;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 10: STATE_CONTROLLED_PRODUCTION_TURNDOWN_AND_FLUSH                                   *)
    (* Extinguishes reaction by shutting peroxide feeds, flushes solvent, and cuts hyper speed    *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_CONTROLLED_TURNDOWN_FLUSH:
        iActiveStateNumber := 10;
        bPulsePhaseActive := FALSE;
        bHPLDV_InPulseExecution := FALSE;

        (* Shut off Peroxides and Block Lines *)
        rCmd_PeroxidePump1_Stroke_pct := 0.0;
        rCmd_PeroxidePump2_Stroke_pct := 0.0;
        rCmd_PeroxidePump3_Stroke_pct := 0.0;
        rCmd_PeroxidePump4_Stroke_pct := 0.0;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        (* Ramp down Hyper-Compressor Throughput *)
        rCmd_HyperComp_SpeedTrim_pct        := -10.0;
        rCmd_HPLDV_Position_pct             := 35.0;
        rCmd_JacketWater_TemperingValve_pct := 70.0; (* Maintain warm tube for flush *)

        rStateProgress_pct := (tStateTimer_s / 120.0) * 100.0;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Transition Guard: Reaction Extinguished (T_peak < 210 C) and Flush Completed *)
        IF (rVoted_PeakTemperature_degC < 210.0) AND (tStateTimer_s >= 120.0) THEN
            iPreviousState := STATE_CONTROLLED_TURNDOWN_FLUSH;
            iState := STATE_ETHYLENE_RECYCLE_DEPRESS;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 11: STATE_ETHYLENE_MONOMER_RECYCLE_AND_DEPRESSURIZE                                  *)
    (* Recycles monomer back to primary compressors, depressurizing tube from 3,000 to 250 bar   *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_ETHYLENE_RECYCLE_DEPRESS:
        iActiveStateNumber := 11;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        (* Controlled Depressurization via HPLDV *)
        rCmd_HyperComp_SpeedTrim_pct := -15.0;
        rCmd_HPLDV_Position_pct      := 55.0;

        rStateProgress_pct := ((3000.0 - rVoted_ReactorPressure_bar) / 2750.0) * 100.0;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        ELSIF rStateProgress_pct < 0.0 THEN
            rStateProgress_pct := 0.0;
        END_IF;

        (* Transition Guard: Pressure Drops Below 300 bar *)
        IF (rVoted_ReactorPressure_bar <= 300.0) AND (tStateTimer_s >= 90.0) THEN
            iPreviousState := STATE_ETHYLENE_RECYCLE_DEPRESS;
            iState := STATE_REACTOR_POST_WASH_NITRO;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 12: STATE_REACTOR_TUBE_POST_WASH_AND_NITROGEN_SEAL                                   *)
    (* Purges remaining hydrocarbons with inert nitrogen and establishes safe blanket seal        *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_REACTOR_POST_WASH_NITRO:
        iActiveStateNumber := 12;
        bPulsePhaseActive := FALSE;
        bCmd_Peroxide_EmergencyBlockBleed := TRUE;

        rCmd_HyperComp_SpeedTrim_pct        := 0.0;
        rCmd_HPLDV_Position_pct             := 10.0;
        rCmd_JacketWater_TemperingValve_pct := 0.0;
        rCmd_JacketWater_BoosterPump_pct    := 25.0;

        rStateProgress_pct := (tStateTimer_s / 60.0) * 100.0;
        IF rStateProgress_pct > 100.0 THEN
            rStateProgress_pct := 100.0;
        END_IF;

        (* Return to Cold Idle on Reset or Operator Command *)
        IF (tStateTimer_s >= 60.0) AND (NOT bStartProduction) THEN
            iPreviousState := STATE_REACTOR_POST_WASH_NITRO;
            iState := STATE_IDLE;
            tStateTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;


    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 13: STATE_EMERGENCY_DECOMPOSITION_FAST_SNORT_DUMP_TRIP                               *)
    (* Sub-5 ms Explosive Decomposition Fast Venting Response: Fires hydraulic snort dump valves  *)
    (* into quench silo, trips secondary compressor, isolates peroxide feed, floods cold deluge   *)
    (* ------------------------------------------------------------------------------------------ *)
    STATE_EMERGENCY_DECOMP_SNORT:
        iActiveStateNumber := 13;
        rStateProgress_pct := 100.0;
        bPulsePhaseActive := FALSE;
        bHPLDV_InPulseExecution := FALSE;

        (* Fast Explosive Actuation Signals *)
        bCmd_SnortValve_EmergencyDump     := TRUE; (* Fire Fast Hydraulic Snort Dump Pilot Solenoids *)
        bCmd_HyperComp_EmergencyTrip      := TRUE; (* Hardwired Trip Secondary Plunger Motor *)
        bCmd_Peroxide_EmergencyBlockBleed := TRUE; (* Isolate & Depressurize Initiator Metering Lines *)
        bCmd_JacketWater_ColdDelugeTrip   := TRUE; (* Maximum Cold Water Deluge into Jackets *)
        bCmd_HPLDV_PulseActive            := FALSE;

        (* Open High-Pressure Letdown Valve to Maximum 100% to Assist Venting *)
        rCmd_HPLDV_Position_pct := 100.0;

        (* Zero All Dosing Pumps *)
        rCmd_PeroxidePump1_Stroke_pct := 0.0;
        rCmd_PeroxidePump2_Stroke_pct := 0.0;
        rCmd_PeroxidePump3_Stroke_pct := 0.0;
        rCmd_PeroxidePump4_Stroke_pct := 0.0;
        rCmd_CTA_DosingPump_pct       := 0.0;

        (* Snort Dump Duration Accumulator *)
        tSnortDumpActiveTimer_s := tSnortDumpActiveTimer_s + tScanCycleTime_s;

        (* Snort Valves Remain Latched Open for at least 180 seconds and until pressure < 50 bar *)
        IF (tSnortDumpActiveTimer_s >= 180.0) AND (rVoted_ReactorPressure_bar <= 50.0) AND bResetAlarms THEN
            bCmd_SnortValve_EmergencyDump := FALSE;
            bCmd_JacketWater_ColdDelugeTrip := FALSE;
            bDecomp_TripQualified := FALSE;
            bDecompDetected := FALSE;
            iPreviousState := STATE_EMERGENCY_DECOMP_SNORT;
            iState := STATE_IDLE;
            tStateTimer_s := 0.0;
            tSnortDumpActiveTimer_s := 0.0;
            bStateFirstScan := TRUE;
        END_IF;

END_CASE;
"""
