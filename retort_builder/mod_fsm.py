# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_fsm.py
Implements Phase 5: Deterministic 14-Stage Operational Production Finite State Machine (FSM)
for Low-Acid Canned Foods (LACF) Rotary Overpressure Retort Autoclave.
"""

def generate_fsm():
    return '''(* =====================================================================================================================
 * PHASE 5: DETERMINISTIC 14-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Control Topology: High-Integrity Deterministic State Sequence for FDA 21 CFR Part 113 Autoclaves
 * Sequence Structure:
 *   Stage 00: STATE_IDLE_STANDBY
 *   Stage 01: STATE_VESSEL_LOCK_SEAL_INFLATION
 *   Stage 02: STATE_AIR_VENT_PURGE
 *   Stage 03: STATE_STEAM_COME_UP_RAMP
 *   Stage 04: STATE_TEMPERATURE_CUT_IN
 *   Stage 05: STATE_OVERPRESSURE_STERILIZATION_HOLD
 *   Stage 06: STATE_BALL_PROCESS_DEVIATION_CATCHUP
 *   Stage 07: STATE_PRE_COOLING_PRESSURE_EQUALIZATION
 *   Stage 08: STATE_WATER_SPRAY_CASCADE_COOLING
 *   Stage 09: STATE_RECIRCULATION_EVAPORATIVE_COOLING
 *   Stage 10: STATE_OVERPRESSURE_WATER_DRAIN
 *   Stage 11: STATE_ATMOSPHERIC_VACUUM_BREAK
 *   Stage 12: STATE_LID_SEAL_DEFLATION_UNLATCH
 *   Stage 13: STATE_CIP_SIP_SANITATION
 *   Stage 14: STATE_EMERGENCY_SAFETY_RELIEF_ABORT
 * ===================================================================================================================== *)

(* State Transition Strobe & Timer Updates *)
IF iFSM_CurrentState <> iFSM_PreviousState THEN
    bFSM_FirstScanInState := TRUE;
    rFSM_StateTimer_s     := 0.0;
    iFSM_PreviousState    := iFSM_CurrentState;
ELSE
    bFSM_FirstScanInState := FALSE;
    rFSM_StateTimer_s     := rFSM_StateTimer_s + rTs_s;
END_IF;

IF (iFSM_CurrentState > 0) AND (iFSM_CurrentState < 12) THEN
    rFSM_TotalCycleTimer_s := rFSM_TotalCycleTimer_s + rTs_s;
ELSE
    IF iFSM_CurrentState = 0 THEN
        rFSM_TotalCycleTimer_s := 0.0;
    END_IF;
END_IF;

rStageElapsedTime_s := rFSM_StateTimer_s;
rCycleElapsedTime_s := rFSM_TotalCycleTimer_s;
iState              := iFSM_CurrentState;

(* Master Safety Interrupt: Emergency Stop or Catastrophic Pressure/Temp Trip *)
IF bTripLatched_EStop OR bTripLatched_PressHH OR bTripLatched_TempHH OR (NOT bDI_EmergencyStop_PB100) THEN
    iFSM_CurrentState := 14; (* Direct branch to emergency abort *)
END_IF;

CASE iFSM_CurrentState OF
    (* =========================================================================
     * STAGE 00: IDLE / STANDBY
     * Vessel unpressurized, door open/unlatched, waiting for operator load command
     * ========================================================================= *)
    0:
        sStateName := 'STATE_00_IDLE_STANDBY';
        bCycleComplete := FALSE;

        (* Reset actuators to safe baseline *)
        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 0.0;
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        bDO_MainSteamIsolationValve := FALSE;
        bDO_AirOverpressSupplyValve := FALSE;
        bDO_CoolingWaterPumpRun     := FALSE;
        bDO_RecirculationPumpRun    := FALSE;
        bDO_SumpDrainValveOpen      := FALSE;
        bDO_VacuumBreakValveOpen    := TRUE;  (* Keep open to ensure zero gauge pressure *)
        bDO_DoorSealInflateSol      := FALSE;
        bDO_DoorSealDeflateSol      := TRUE;  (* Gasket deflated for door movement *)
        bDO_HydraulicPinLockActuate := FALSE;
        bDO_EmergencyQuenchValve    := FALSE;
        bDO_RotaryBrakeRelease      := FALSE; (* Mechanical brake engaged *)

        (* Transition triggers *)
        IF bCmd_StartCycle AND bDI_DoorClosedLimit_ZS101 THEN
            rIntegratedF0 := 0.0;
            bBall_DeviationLatching := FALSE;
            bBall_CatchupActive     := FALSE;
            rBall_CookAccumulated_s := 0.0;
            rBall_DevCookRampDown_s := 0.0;
            iFSM_CurrentState       := 1; (* Advance to Door Lock & Seal Inflation *)
        ELSIF bCmd_StartCIP AND bDI_DoorClosedLimit_ZS101 THEN
            iFSM_CurrentState := 13; (* Branch to Clean-In-Place / SIP *)
        END_IF;

    (* =========================================================================
     * STAGE 01: VESSEL DOOR LOCK & SEAL INFLATION
     * Engage hydraulic locking ring, inflate elastomer gasket, verify 5.5 bar seal
     * ========================================================================= *)
    1:
        sStateName := 'STATE_01_VESSEL_LOCK_SEAL_INFLATION';

        (* Engage hydraulic lock pins and inflate door seal *)
        bDO_HydraulicPinLockActuate := TRUE;
        bDO_DoorSealDeflateSol      := FALSE;
        bDO_DoorSealInflateSol      := TRUE;
        bDO_VacuumBreakValveOpen    := FALSE;

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 0.0;
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        (* Interlock qualification check *)
        IF (rFSM_StateTimer_s >= cTime_SealInflate_s) THEN
            IF bDI_DoorLockedLimit_ZS102 AND bDI_DoorSealPressureOK_PS103 AND (rPT_601_DoorSealPress_bar >= 5.0) THEN
                iFSM_CurrentState := 2; (* Advance to Vent Purge *)
            ELSE
                bTripLatched_DoorSealLoss := TRUE;
                iFSM_CurrentState := 14; (* Abort: Door Seal Failure *)
            END_IF;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 11; (* Controlled Abort to Vacuum Break *)
        END_IF;

    (* =========================================================================
     * STAGE 02: AIR VENT PURGE
     * Displace non-condensable atmospheric air pockets with low-pressure culinary steam sweep
     * ========================================================================= *)
    2:
        sStateName := 'STATE_02_AIR_VENT_PURGE';

        (* Open main steam isolation, throttle steam to displace cold air pockets *)
        bDO_MainSteamIsolationValve := TRUE;
        bDO_AirOverpressSupplyValve := FALSE;
        bDO_SumpDrainValveOpen      := TRUE; (* Bleed cold condensate trap *)
        bDO_RotaryBrakeRelease      := TRUE; (* Free drum *)

        (* Modulate steam to establish 100.5 deg C atmospheric sweep *)
        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 100.0; (* 100% open top vents to expel air *)
        rAO_RotaryDriveSpeed_RPM    := 4.0;   (* Slow rotation to agitate air pockets *)

        (* Purge duration qualification: steam sweep time + vent temp >= 100.0 deg C *)
        IF (rFSM_StateTimer_s >= rSet_VentPurgeDuration_s) AND (rVotedVesselTemp_degC >= 100.0) THEN
            bDO_SumpDrainValveOpen := FALSE; (* Close purge drains *)
            iFSM_CurrentState      := 3;     (* Advance to Steam Come-Up Ramp *)
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 10;
        END_IF;

    (* =========================================================================
     * STAGE 03: STEAM COME-UP RAMP
     * Ramp vessel temperature at rate-limited trajectory (e.g. 2.5 deg C/min)
     * Apply air overpressure to maintain positive counter-pressure cushion
     * ========================================================================= *)
    3:
        sStateName := 'STATE_03_STEAM_COME_UP_RAMP';

        bDO_MainSteamIsolationValve := TRUE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        (* Full MPC multivariable modulation *)
        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM * 0.60; (* Intermediate rotation *)

        (* Transition to Temperature Cut-In when vessel reaches within 0.5 deg C of cook setpoint *)
        IF rVotedVesselTemp_degC >= (rSet_TargetCookTemp_degC - 0.50) THEN
            iFSM_CurrentState := 4;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 7; (* Pre-Cool Equalization *)
        END_IF;

    (* =========================================================================
     * STAGE 04: TEMPERATURE CUT-IN
     * FDA 21 CFR 113 Legal Qualification Point:
     * Verify all 3 TMR temperature channels >= Scheduled Cook Temp and stable
     * ========================================================================= *)
    4:
        sStateName := 'STATE_04_TEMPERATURE_CUT_IN';

        bDO_MainSteamIsolationValve := TRUE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM;

        (* Dwell 10 seconds to verify steady-state thermal stability *)
        IF (rFSM_StateTimer_s >= 10.0) AND (rVotedVesselTemp_degC >= rSet_TargetCookTemp_degC) THEN
            IF (rVotedVesselPress_bar >= (rAntoine_Pv_sat_bar + 0.150)) THEN
                iFSM_CurrentState := 5; (* Advance to Sterilization Hold *)
            END_IF;
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 7;
        END_IF;

    (* =========================================================================
     * STAGE 05: OVERPRESSURE STERILIZATION HOLD
     * Isothermal (+/- 0.2 deg C) and isobaric hold, continuous rotary agitation,
     * tracking scheduled cook time and cumulative Ball F0 lethality integral
     * ========================================================================= *)
    5:
        sStateName := 'STATE_05_OVERPRESSURE_STERILIZATION_HOLD';

        bDO_MainSteamIsolationValve := TRUE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM;

        (* Check for thermal process deviation *)
        IF bBall_CatchupActive THEN
            iFSM_CurrentState := 6; (* Branch to Ball Process Deviation Catch-up *)
        ELSIF (rBall_CookAccumulated_s >= rBall_ScheduledCookDuration_s) AND (rIntegratedF0 >= rSet_TargetF0_min) THEN
            (* Dual criteria met: Scheduled cook time satisfied AND legal F0 lethality reached *)
            iFSM_CurrentState := 7; (* Advance to Pre-Cooling Pressure Equalization *)
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 7;
        END_IF;

    (* =========================================================================
     * STAGE 06: BALL PROCESS DEVIATION CATCH-UP
     * Automated compensation mode: freeze cook countdown, compute lethality deficit,
     * dynamically extend sterilization hold until cumulative F0 >= Target F0
     * ========================================================================= *)
    6:
        sStateName := 'STATE_06_BALL_PROCESS_DEVIATION_CATCHUP';

        bDO_MainSteamIsolationValve := TRUE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        (* MPC aggressive recovery to return to scheduled cook setpoint *)
        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM;

        (* Return to normal hold if temperature recovered and supplemental time satisfied *)
        IF (rIntegratedF0 >= rSet_TargetF0_min) THEN
            bBall_CatchupActive := FALSE;
            iFSM_CurrentState   := 7; (* Deficit made up; proceed to Pre-Cooling *)
        ELSIF (rVotedVesselTemp_degC >= rSet_TargetCookTemp_degC) AND (rBall_SuppleTimeNeeded_s <= 0.0) THEN
            bBall_CatchupActive := FALSE;
            iFSM_CurrentState   := 5; (* Return to standard hold *)
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 7;
        END_IF;

    (* =========================================================================
     * STAGE 07: PRE-COOLING PRESSURE EQUALIZATION
     * Critical Deflection Protection: Pre-charge compressed air overpressure
     * (+0.35..+0.45 bar above steam saturation) prior to cold water injection
     * to eliminate pouch burst/crush transient during steam condensation collapse
     * ========================================================================= *)
    7:
        sStateName := 'STATE_07_PRE_COOLING_AIR_EQUALIZATION';

        bDO_MainSteamIsolationValve := FALSE; (* Shut off main steam *)
        bDO_AirOverpressSupplyValve := TRUE;  (* High-capacity compressed air feed *)
        bDO_RotaryBrakeRelease      := TRUE;

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 80.0; (* Force air injection *)
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 0.0;
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM * 0.80;

        (* Verify air cushion established and hold for dwell duration *)
        IF (rFSM_StateTimer_s >= cTime_PreCoolEquil_s) AND (rVotedVesselPress_bar >= (rAntoine_Pv_sat_bar + 0.350)) THEN
            iFSM_CurrentState := 8; (* Advance to Cold Water Cascade Cooling *)
        END_IF;

    (* =========================================================================
     * STAGE 08: WATER SPRAY CASCADE COOLING
     * Introduce cold water top and side atomized sprays while dynamically modulating
     * compressed air overpressure to maintain zero net wall stress (DeltaP ~ 0.0)
     * ========================================================================= *)
    8:
        sStateName := 'STATE_08_WATER_SPRAY_CASCADE_COOLING';

        bDO_MainSteamIsolationValve := FALSE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_CoolingWaterPumpRun     := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        (* Multivariable decoupled cooling action *)
        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := rMPC_OptimizedU[3];
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM;

        (* Advance to recirculation cooling when core temp drops below 70 deg C *)
        IF (rVotedCanCoreTemp_degC <= 70.0) OR (rFSM_StateTimer_s >= 600.0) THEN
            iFSM_CurrentState := 9;
        END_IF;

    (* =========================================================================
     * STAGE 09: RECIRCULATION EVAPORATIVE COOLING
     * Recirculate sump cooling water through external plate heat exchanger,
     * cooling container product cold spot below 40.0 deg C (halt thermophilic germination)
     * ========================================================================= *)
    9:
        sStateName := 'STATE_09_RECIRCULATION_EVAP_COOLING';

        bDO_MainSteamIsolationValve := FALSE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_CoolingWaterPumpRun     := TRUE;
        bDO_RecirculationPumpRun    := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := rMPC_OptimizedU[3];
        rAO_VentModulatingValve_pct := rMPC_OptimizedU[4];
        rAO_RotaryDriveSpeed_RPM    := rSet_RotaryCookRPM * 0.50;

        (* Cool until product core drops below recipe target (typically 38..40 deg C) *)
        IF (rVotedCanCoreTemp_degC <= rSet_TargetCoolingTemp_degC) THEN
            dwFDAComplianceWord := dwFDAComplianceWord OR 16#0000_0020; (* Core Below 40C Target *)
            iFSM_CurrentState   := 10; (* Advance to Overpressure Water Drain *)
        END_IF;

    (* =========================================================================
     * STAGE 10: OVERPRESSURE WATER DRAIN
     * Evacuate cooling water sump while maintaining 0.40 bar air cushion
     * to prevent hydrostatic shock and tinplate can end buckling
     * ========================================================================= *)
    10:
        sStateName := 'STATE_10_OVERPRESSURE_WATER_DRAIN';

        bDO_MainSteamIsolationValve := FALSE;
        bDO_AirOverpressSupplyValve := TRUE;
        bDO_CoolingWaterPumpRun     := FALSE;
        bDO_RecirculationPumpRun    := FALSE;
        bDO_SumpDrainValveOpen      := TRUE;  (* Open bottom drain *)
        bDO_RotaryBrakeRelease      := FALSE; (* Stop basket rotation *)

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := rMPC_OptimizedU[2];
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 10.0;
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        (* Drain completion qualification: sump level < 25 mm AND timeout satisfied *)
        IF (rFSM_StateTimer_s >= cTime_OverpressDrain_s) OR (rVotedSumpLevel_mm <= 25.0) THEN
            bDO_SumpDrainValveOpen := FALSE;
            iFSM_CurrentState      := 11; (* Advance to Vacuum Break *)
        END_IF;

    (* =========================================================================
     * STAGE 11: ATMOSPHERIC VACUUM BREAK
     * Controlled depressurization: slowly vent remaining compressed air to atmosphere,
     * verifying vessel absolute pressure returns to 1.013 bar (0.00 bar gauge)
     * ========================================================================= *)
    11:
        sStateName := 'STATE_11_ATMOSPHERIC_VACUUM_BREAK';

        bDO_MainSteamIsolationValve := FALSE;
        bDO_AirOverpressSupplyValve := FALSE;
        bDO_CoolingWaterPumpRun     := FALSE;
        bDO_RecirculationPumpRun    := FALSE;
        bDO_SumpDrainValveOpen      := TRUE;
        bDO_VacuumBreakValveOpen    := TRUE; (* Open siphon breaker *)
        bDO_RotaryBrakeRelease      := FALSE;

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 100.0; (* Full vent open *)
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        (* Vessel fully depressurized to atmosphere (Pv <= 1.050 bar) *)
        IF (rFSM_StateTimer_s >= cTime_VacuumBreak_s) AND (rVotedVesselPress_bar <= 1.050) THEN
            iFSM_CurrentState := 12; (* Advance to Door Seal Deflate *)
        END_IF;

    (* =========================================================================
     * STAGE 12: LID SEAL DEFLATION & DOOR UNLATCH
     * Deflate pneumatic gasket under vacuum, retract hydraulic locking pins,
     * confirm zero pressure interlock, declare cycle complete
     * ========================================================================= *)
    12:
        sStateName := 'STATE_12_SEAL_DEFLATE_DOOR_UNLATCH';

        bDO_DoorSealInflateSol      := FALSE;
        bDO_DoorSealDeflateSol      := TRUE;  (* Deflate seal *)
        bDO_HydraulicPinLockActuate := FALSE; (* Retract hydraulic lock *)
        bDO_VacuumBreakValveOpen    := TRUE;

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 0.0;
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        IF (rFSM_StateTimer_s >= cTime_SealDeflate_s) AND (rPT_601_DoorSealPress_bar <= 0.50) THEN
            bCycleComplete    := TRUE;
            dwStatusWord      := dwStatusWord OR 16#0000_8000; (* Batch Complete *)
            iFSM_CurrentState := 0; (* Return to Idle Standby *)
        END_IF;

    (* =========================================================================
     * STAGE 13: CIP / SIP SANITATION
     * Clean-In-Place / Steam-In-Place sequence: hot caustic wash circulation (85 deg C),
     * sterile rinse, followed by pure culinary steam sanitization (125 deg C, F0 >= 15 min)
     * ========================================================================= *)
    13:
        sStateName := 'STATE_13_CIP_SIP_SANITATION';

        bDO_MainSteamIsolationValve := TRUE;
        bDO_CoolingWaterPumpRun     := FALSE;
        bDO_RecirculationPumpRun    := TRUE;
        bDO_RotaryBrakeRelease      := TRUE;

        rAO_SteamControlValve_pct   := rMPC_OptimizedU[1];
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 0.0;
        rAO_VentModulatingValve_pct := 15.0;
        rAO_RotaryDriveSpeed_RPM    := 6.0;

        IF (rFSM_StateTimer_s >= 1800.0) AND (rIntegratedF0 >= 15.0) THEN
            iFSM_CurrentState := 10; (* Transition to Drain & Cool *)
        END_IF;

        IF bCmd_StopCycle THEN
            iFSM_CurrentState := 10;
        END_IF;

    (* =========================================================================
     * STAGE 14: EMERGENCY SAFETY RELIEF ABORT
     * Catastrophic Overpressure / Over-Temperature / E-Stop Trips:
     * Fast-close steam, open full vent, trigger emergency cold deluge quench,
     * lock vessel door, alarm sounders
     * ========================================================================= *)
    14:
        sStateName := 'STATE_14_EMERGENCY_SAFETY_ABORT';
        bEmergencyStopActive := TRUE;

        (* Immediate failsafe actuator trip *)
        bDO_MainSteamIsolationValve := FALSE; (* Hard shutoff steam *)
        bDO_AirOverpressSupplyValve := FALSE;
        bDO_EmergencyQuenchValve    := TRUE;  (* Emergency water deluge *)
        bDO_CoolingWaterPumpRun     := TRUE;
        bDO_RecirculationPumpRun    := FALSE;
        bDO_SumpDrainValveOpen      := TRUE;  (* Drain vessel *)
        bDO_VacuumBreakValveOpen    := FALSE;
        bDO_HydraulicPinLockActuate := TRUE;  (* Keep door locked for safety! *)
        bDO_DoorSealInflateSol      := TRUE;
        bDO_DoorSealDeflateSol      := FALSE;
        bDO_RotaryBrakeRelease      := FALSE; (* Hard mechanical brake *)

        rAO_SteamControlValve_pct   := 0.0;
        rAO_AirOverpressValve_pct   := 0.0;
        rAO_CoolingWaterValve_pct   := 100.0; (* 100% cold quench *)
        rAO_VentModulatingValve_pct := 100.0; (* 100% emergency vent *)
        rAO_RotaryDriveSpeed_RPM    := 0.0;

        (* Acknowledge and Reset Trip Operator Sequence *)
        IF bCmd_ResetTrip AND bDI_EmergencyStop_PB100 THEN
            IF (rVotedVesselPress_bar <= 1.050) AND (rVotedVesselTemp_degC <= 60.0) THEN
                bTripLatched_EStop       := FALSE;
                bTripLatched_PressHH     := FALSE;
                bTripLatched_TempHH      := FALSE;
                bTripLatched_TMR_Failure := FALSE;
                bEmergencyStopActive     := FALSE;
                bDO_EmergencyQuenchValve := FALSE;
                iFSM_CurrentState        := 0; (* Return to Idle Standby *)
            END_IF;
        END_IF;
END_CASE;
'''

if __name__ == "__main__":
    f = generate_fsm()
    print("FSM length:", len(f))
    print(f[:300])
