# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_fsm.py
Implements Phase 4: Deterministic 14-Stage Operational Production Finite State Machine (FSM)
for Commercial Continuous Overpressure Industrial Retort Sterilization (States 0..13).
"""

def generate_fsm():
    return '''(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
 * Regulatory Standard: US FDA 21 CFR Part 113 Continuous Rotary Thermal Processing
 * Operational States:
 *   Stage 00: STATE_IDLE
 *   Stage 01: STATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK
 *   Stage 02: STATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE
 *   Stage 03: STATE_COME_UP_HEATING_RAMP_TO_121C
 *   Stage 04: STATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK
 *   Stage 05: STATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM
 *   Stage 06: STATE_TARGET_F0_REACHED_HEATING_CUTOFF
 *   Stage 07: STATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION
 *   Stage 08: STATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE
 *   Stage 09: STATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C
 *   Stage 10: STATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN
 *   Stage 11: STATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH
 *   Stage 12: STATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN
 *   Stage 13: STATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * STATE TRANSITION STROBE & TIMERS MANAGEMENT
 * --------------------------------------------------------------------------------------------------------------------- *)
IF iFSM_CurrentState <> iFSM_PreviousState THEN
    bFSM_FirstScanInState := TRUE;
    rFSM_StateTimer_s     := 0.0;
    iFSM_PreviousState    := iFSM_CurrentState;
ELSE
    bFSM_FirstScanInState := FALSE;
    rFSM_StateTimer_s     := rFSM_StateTimer_s + rTs_s;
END_IF;

(* Cumulative Run / Cycle Timer Management *)
IF (iFSM_CurrentState >= 1) AND (iFSM_CurrentState <= 12) THEN
    rFSM_TotalCycleTimer_s := rFSM_TotalCycleTimer_s + rTs_s;
ELSIF iFSM_CurrentState = 0 THEN
    rFSM_TotalCycleTimer_s := 0.0;
END_IF;

iCurrentState := iFSM_CurrentState;

(* ---------------------------------------------------------------------------------------------------------------------
 * GLOBAL CRITICAL SAFETY TRIP INTERLOCK OVERRIDE
 * Immediate vectoring to State 13 on any catastrophic hardware or pressure fault
 * --------------------------------------------------------------------------------------------------------------------- *)
IF NOT bDI_EmergencyStop_PB OR bTripLatched_PressHH OR bTripLatched_TempHH OR bTripLatched_DeltaPHH THEN
    IF iFSM_CurrentState <> cSTATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP THEN
        iFSM_CurrentState := cSTATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 14-STAGE DETERMINISTIC FINITE STATE MACHINE LOGIC
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_CurrentState OF

    (* -------------------------------------------------------------------------
     * STATE 00: STATE_IDLE
     * Standby state awaiting operator cycle initiation and pre-flight validation.
     * ------------------------------------------------------------------------- *)
    cSTATE_IDLE:
        bCmd_DoorSealInflate            := FALSE;
        bCmd_DrainValveOpen             := FALSE;
        bCmd_SafetyReliefPilotOpen      := FALSE;
        rCmd_DischargeConveyorSpeed_pct := 0.0;
        bEmergencyAbortActive           := FALSE;
        bCycleComplete_Sterile          := FALSE;
        bTargetF0Reached                := FALSE;
        bProcessDeviationActive         := FALSE;
        rFSM_SterilizationHoldTimer_s   := 0.0;
        rDeviationCompTimer_s           := 0.0;

        (* Check operator start command and baseline safety prerequisites *)
        IF bCmd_StartContinuousCycle AND bDI_EmergencyStop_PB AND NOT bDI_SafetyReliefPoppetOpen_ZS THEN
            IF bDI_SafetyDoorClosed_ZS1 THEN
                iFSM_CurrentState := cSTATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK;
            END_IF;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 01: STATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK
     * Infeed continuous container stream into rotary helix pockets, engage hydraulic
     * lock ring, and inflate pneumatic silicone elastomer door gasket.
     * ------------------------------------------------------------------------- *)
    cSTATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;

        (* Rotary drum inches forward slowly to accept infeed container collation *)
        IF rFSM_StateTimer_s < 10.0 THEN
            rCmd_RotaryDrumSpeed_RPM := 2.50; (* Infeed pocket indexing *)
        ELSE
            rCmd_RotaryDrumSpeed_RPM := 0.0;
        END_IF;

        (* Verify mechanical door lock and pneumatic seal pressure >= 5.0 bar *)
        IF bDI_SafetyDoorClosed_ZS1 AND bDI_SafetyDoorLocked_ZS2 AND (rDoorSealPress_bar >= 5.00) THEN
            IF rFSM_StateTimer_s >= 15.0 THEN
                iFSM_CurrentState := cSTATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE;
            END_IF;
        END_IF;

        (* Abort to Idle on operator stop *)
        IF bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_IDLE;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 02: STATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE
     * Full exhaust vent opening to evacuate atmospheric air using culinary steam sweep.
     * Guaranteed compliance with US FDA 21 CFR Part 113 venting schedule.
     * ------------------------------------------------------------------------- *)
    cSTATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;

        (* Maintain continuous rotation at slow purge speed to circulate headspace *)
        rCmd_RotaryDrumSpeed_RPM := 5.0;

        (* Vent criteria: Voted temperature achieves atmospheric boiling >= 100.5 deg C
         * and minimum purge time of 120 seconds has elapsed to clear non-condensables *)
        IF (rVoted_Temp_degC >= 100.50) AND (rFSM_StateTimer_s >= 120.0) THEN
            iFSM_CurrentState := cSTATE_COME_UP_HEATING_RAMP_TO_121C;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 03: STATE_COME_UP_HEATING_RAMP_TO_121C
     * Thermal Come-Up Heating Ramp. Modulating steam injection throttles thermal rise
     * while compressed air injects counter-overpressure to prevent pouch delamination.
     * ------------------------------------------------------------------------- *)
    cSTATE_COME_UP_HEATING_RAMP_TO_121C:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;

        (* Drum accelerates to nominal process agitation speed *)
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* Transition to Equilibrium Lock when within 0.50 deg C of target cook temperature *)
        IF rVoted_Temp_degC >= (rSet_SterilizationTemp_degC - 0.50) THEN
            iFSM_CurrentState := cSTATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 04: STATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK
     * Stabilization dwell ensuring temperature uniformity across all RTD sensors
     * and establishing exact overpressure equilibrium before logging sterilization time.
     * ------------------------------------------------------------------------- *)
    cSTATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* Criteria: 30-second dwell with chamber pressure and temperature tightly locked *)
        IF (rFSM_StateTimer_s >= 30.0) AND (rVoted_Temp_degC >= (rSet_SterilizationTemp_degC - 0.30)) THEN
            IF (rVoted_Press_bar >= (rSet_RetortOverpressure_bar - 0.08)) THEN
                iFSM_CurrentState := cSTATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM;
            END_IF;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 05: STATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM
     * High-precision sterilization hold. Real-time Bigelow F0 lethality accumulation.
     * Automated US FDA 21 CFR Part 113 process deviation monitoring and dwell compensation.
     * ------------------------------------------------------------------------- *)
    cSTATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        rFSM_SterilizationHoldTimer_s := rFSM_SterilizationHoldTimer_s + rTs_s;

        (* Process Deviation Detection: Temp drops more than 0.50 deg C below scheduled cook *)
        IF rVoted_Temp_degC < (rSet_SterilizationTemp_degC - 0.50) THEN
            bProcessDeviationActive := TRUE;
            rDeviationCompTimer_s   := rDeviationCompTimer_s + rTs_s;
        END_IF;

        (* Sterilization Complete Criteria: F0 target attained AND minimum residence dwell fulfilled *)
        IF bTargetF0Reached AND (rFSM_SterilizationHoldTimer_s >= (rCalculatedDwellTime_min * 60.0)) THEN
            iFSM_CurrentState := cSTATE_TARGET_F0_REACHED_HEATING_CUTOFF;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 06: STATE_TARGET_F0_REACHED_HEATING_CUTOFF
     * Target thermal death time achieved. Culinary steam supply instantaneously shut off.
     * Overpressure actively boosted to prevent vacuum collapse as steam begins condensing.
     * ------------------------------------------------------------------------- *)
    cSTATE_TARGET_F0_REACHED_HEATING_CUTOFF:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* 10-second pressure lock transition prior to introducing quench water *)
        IF rFSM_StateTimer_s >= 10.0 THEN
            iFSM_CurrentState := cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 07: STATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION
     * Pre-tempered water spray injection. Overpressure clamped at design rating to
     * prevent internal container vapor flashing and pouch seal rupture.
     * ------------------------------------------------------------------------- *)
    cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* Once chamber temperature drops below 95.0 deg C, transition to Full Immersion Cascade *)
        IF (rVoted_Temp_degC <= 95.00) AND (rFSM_StateTimer_s >= 20.0) THEN
            iFSM_CurrentState := cSTATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 08: STATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE
     * High-volume tempered cooling water cascade spray. Continuous rotary drum agitation
     * ensures rapid convective boundary heat transfer out of product containers.
     * ------------------------------------------------------------------------- *)
    cSTATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* Transition to Final Cold Chilldown when chamber temperature drops below 65.0 deg C *)
        IF (rVoted_Temp_degC <= 65.00) AND (rFSM_StateTimer_s >= 60.0) THEN
            iFSM_CurrentState := cSTATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 09: STATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C
     * Deep cooling with plant chilled sterile water to bring container core cold-spot
     * below 40.0 deg C to permanently arrest thermophilic spore germination.
     * ------------------------------------------------------------------------- *)
    cSTATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := FALSE;
        rCmd_RotaryDrumSpeed_RPM := rSet_NominalDrumSpeed_RPM;

        (* Criteria: Container Core Temperature drops below target discharge cooling setpoint *)
        IF (rX_State[2] <= rSet_TargetCoolingTemp_degC) AND (rFSM_StateTimer_s >= 45.0) THEN
            iFSM_CurrentState := cSTATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 10: STATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN
     * Opening vessel bottom rapid drain and modulating exhaust vent to smoothly
     * depressurize chamber without sudden container expansion or panelling.
     * ------------------------------------------------------------------------- *)
    cSTATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN:
        bCmd_DoorSealInflate := TRUE;
        bCmd_DrainValveOpen  := TRUE; (* Rapid drain valve open *)
        rCmd_RotaryDrumSpeed_RPM := 5.0;

        (* Criteria: Chamber pressure approaches atmospheric (< 1.06 bar) and sump is dry (< 20 mm) *)
        IF (rVoted_Press_bar <= 1.060) AND (rVoted_Level_mm <= 25.0) AND (rFSM_StateTimer_s >= 30.0) THEN
            iFSM_CurrentState := cSTATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 11: STATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH
     * Full atmospheric venting, vacuum break, deflate inflatable door gasket,
     * and disengage hydraulic door safety locking ring.
     * ------------------------------------------------------------------------- *)
    cSTATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH:
        bCmd_DoorSealInflate := FALSE; (* Deflate door gasket *)
        bCmd_DrainValveOpen  := TRUE;
        rCmd_RotaryDrumSpeed_RPM := 0.0;

        (* Verify complete depressurization and door gasket deflation *)
        IF (rVoted_Press_bar <= 1.025) AND (rDoorSealPress_bar <= 0.50) AND (rFSM_StateTimer_s >= 15.0) THEN
            iFSM_CurrentState := cSTATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 12: STATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN
     * Rotor helical drum rotates forward in discharge mode, transporting sterilized,
     * cooled pouches/cans out onto high-speed discharge packaging line conveyors.
     * ------------------------------------------------------------------------- *)
    cSTATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN:
        bCmd_DoorSealInflate            := FALSE;
        bCmd_DrainValveOpen             := TRUE;
        rCmd_RotaryDrumSpeed_RPM        := 10.0; (* Continuous discharge rotation *)
        rCmd_DischargeConveyorSpeed_pct := 85.0; (* Outfeed packaging conveyor running *)
        bCycleComplete_Sterile          := TRUE;

        (* Transition back to Idle once discharge dwell finishes or operator stops *)
        IF (rFSM_StateTimer_s >= 60.0) OR bCmd_StopCycle THEN
            iFSM_CurrentState := cSTATE_IDLE;
        END_IF;

    (* -------------------------------------------------------------------------
     * STATE 13: STATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP
     * Hard failsafe state: Steam isolation, emergency depressurization pilot,
     * emergency cooling deluge, and automated batch quarantine flagging.
     * ------------------------------------------------------------------------- *)
    cSTATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP:
        bEmergencyAbortActive           := TRUE;
        rCmd_SteamModValve_pct          := 0.0;  (* Hard steam shutoff *)
        bCmd_DoorSealInflate            := TRUE; (* Retain door seal locked *)
        rCmd_DischargeConveyorSpeed_pct := 0.0;
        rCmd_RotaryDrumSpeed_RPM        := 0.0;

        (* Active Pressure Safety Dump *)
        IF rVoted_Press_bar >= cTrip_Press_HH_bar THEN
            bCmd_SafetyReliefPilotOpen := TRUE;
            rCmd_ExhaustVentValve_pct  := 100.0;
            rCmd_AirOverpressValve_pct := 0.0;
        ELSE
            bCmd_SafetyReliefPilotOpen := FALSE;
            (* Modulate vent to safely maintain 1.50 bar cushion if containers are still hot *)
            IF rVoted_Press_bar > 1.500 THEN
                rCmd_ExhaustVentValve_pct := 25.0;
            ELSE
                rCmd_ExhaustVentValve_pct := 0.0;
            END_IF;
        END_IF;

        (* Keep cooling cascade active to suppress thermal runaways *)
        rCmd_CoolingWaterCascadeValve_pct := 100.0;
        bCmd_DrainValveOpen := TRUE;

        (* Operator Reset Logic *)
        IF bCmd_EmergencyTripReset AND bDI_EmergencyStop_PB AND (rVoted_Press_bar <= 1.050) AND (rVoted_Temp_degC <= 45.0) THEN
            bTripLatched_PressHH        := FALSE;
            bTripLatched_TempHH         := FALSE;
            bTripLatched_DeltaPHH       := FALSE;
            bTripLatched_DeltaPLL       := FALSE;
            bEmergencyAbortActive       := FALSE;
            iFSM_CurrentState           := cSTATE_IDLE;
        END_IF;

ELSE
    iFSM_CurrentState := cSTATE_IDLE;
END_CASE;'''
