# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_fsm.py
Implements Phase 4: Deterministic 14-Stage Production Finite State Machine (FSM)
for 500 kA Hall-Heroult Aluminum Reduction Potline Cell.
States 0..13:
  0: STATE_IDLE
  1: STATE_COLD_POT_COKE_PREHEAT_CURRENT_RAMP
  2: STATE_LIQUID_ELECTROLYTE_BATH_TRANSFER
  3: STATE_POT_STARTUP_AND_INITIAL_ACD_SET
  4: STATE_NOMINAL_ELECTROLYSIS_CLOSED_LOOP_MPC
  5: STATE_REGULAR_POINT_FEEDER_PULSE_CYCLE
  6: STATE_ANODE_BEAM_INCREMENTAL_TRACKING_MOVE
  7: STATE_EARLY_ANODE_EFFECT_PREDICTION_WARNING
  8: STATE_ANODE_EFFECT_SUPPRESSION_GAS_DISPERSAL
  9: STATE_AUTOMATED_CARBON_ANODE_BLOCK_CHANGE
  10: STATE_VACUUM_CRUCIBLE_LIQUID_ALUMINUM_TAP
  11: STATE_BATH_CHEMISTRY_ALF3_CORRECTION_CYCLE
  12: STATE_CONTROLLED_POT_DE-ENERGIZATION_BYPASS
  13: STATE_EMERGENCY_POT_TAP_LEAK_OR_ACD_COLLAPSE_TRIP
"""

def generate_fsm():
    return '''(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
 * Controls complete electrochemical lifecycle, Anode Effect suppression, and metal tapping/anode change routines.
 * ===================================================================================================================== *)

(* State dwell elapsed time accounting *)
IF nFSM_CurrentState <> nFSM_PreviousState THEN
    rFSM_StateTimer_s := 0.0;
    nFSM_PreviousState := nFSM_CurrentState;
ELSE
    rFSM_StateTimer_s := rFSM_StateTimer_s + rLocalDeltaT_s;
END_IF;

(* Global Hardwired Safety Emergency Interlock Check *)
IF bDI_EmergencyStop_PB OR bDI_AnodeHoistMotorOverload OR
   (rPot_EstAnodeCathodeDist_mm <= c_ACD_Trip_LL AND nFSM_CurrentState >= 3) THEN
    nFSM_CurrentState := 13; (* Immediate transition to EMERGENCY TRIP *)
END_IF;

CASE nFSM_CurrentState OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 0: STATE_IDLE
     * Pot de-energized, waiting for operator start command and safety interlock verification.
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        (* De-energize all field actuator outputs *)
        rCmd_AnodeBeamHoistPulse_mm := 0.0;
        bCmd_AnodeBeamHoistUp := FALSE;
        bCmd_AnodeBeamHoistDown := FALSE;
        rCmd_PointFeederPulseRate_ppm := 0.0;
        bCmd_PointFeederFire1 := FALSE;
        bCmd_PointFeederFire2 := FALSE;
        bCmd_PointFeederFire3 := FALSE;
        bCmd_PointFeederFire4 := FALSE;
        bCmd_CrustBreakerPunch1 := FALSE;
        bCmd_CrustBreakerPunch2 := FALSE;
        bCmd_CrustBreakerPunch3 := FALSE;
        bCmd_CrustBreakerPunch4 := FALSE;
        rCmd_AlF3AdditionDose_pct := 0.0;
        rCmd_ExhaustDamperPosition_pct := 15.0; (* Minimum draft ventilation *)
        bCmd_PotlineBypassShuntWedgeFire := FALSE;
        bCmd_AnodeEffectHornStrobe := FALSE;

        bPot_FeedingModeNominal := FALSE;
        bPot_FeedingModeUnderfeed := FALSE;
        bPot_FeedingModeOverfeed := FALSE;
        bPot_BeamRockingActive := FALSE;
        bPot_EmergencyTripped := FALSE;

        (* Transition to Cold Pot Coke Preheat upon valid start command and clear interlocks *)
        IF bCmd_StartElectrolysis AND NOT bDI_EmergencyStop_PB AND NOT bDI_PotBypassSwitchClosed THEN
            nFSM_CurrentState := 1;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 1: STATE_COLD_POT_COKE_PREHEAT_CURRENT_RAMP
     * Thermal soak of refractory lining and carbon cathode block via resistor coke bed.
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        rCmd_AnodeBeamHoistPulse_mm := 0.0;
        bCmd_AnodeBeamHoistUp := FALSE;
        bCmd_AnodeBeamHoistDown := FALSE;
        rCmd_PointFeederPulseRate_ppm := 0.0;
        rCmd_ExhaustDamperPosition_pct := 30.0;

        (* Calculate synthetic preheat target current ramp: 0 to 500 kA over 48 hours *)
        rPreheatRampCurrent_kA := (rFSM_StateTimer_s / 172800.0) * 500.0;
        IF rPreheatRampCurrent_kA > 500.0 THEN
            rPreheatRampCurrent_kA := 500.0;
        END_IF;

        (* Check thermal soak completion: Cathode shell temperature >= 850 deg C or dwell timeout *)
        IF (rCathodeShellTemp_degC >= 850.0 OR rFSM_StateTimer_s >= 172800.0) AND (rPot_VotedLineCurrent_kA >= 450.0) THEN
            nFSM_CurrentState := 2; (* Advance to Molten Bath Transfer *)
        END_IF;

        IF bCmd_StopCycle THEN
            nFSM_CurrentState := 12;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 2: STATE_LIQUID_ELECTROLYTE_BATH_TRANSFER
     * Charging molten cryolite bath from donor cells via siphon ladle into cathode cavity.
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        rCmd_ExhaustDamperPosition_pct := 40.0;
        rElectrolyteFillVolume_pct := (rFSM_StateTimer_s / 3600.0) * 100.0;
        IF rElectrolyteFillVolume_pct > 100.0 THEN
            rElectrolyteFillVolume_pct := 100.0;
        END_IF;

        (* Transition once liquid bath volume reaches nominal and temperature exceeds 940 deg C *)
        IF (rElectrolyteFillVolume_pct >= 100.0 OR rFSM_StateTimer_s >= 3600.0) AND (rPot_VotedBathTemp_degC >= 940.0) THEN
            nFSM_CurrentState := 3; (* Advance to Startup & Initial ACD Set *)
        END_IF;

        IF bCmd_StopCycle THEN
            nFSM_CurrentState := 12;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 3: STATE_POT_STARTUP_AND_INITIAL_ACD_SET
     * Anode beam lowered into liquid electrolyte, striking electrolysis arc, establishing 42 mm ACD.
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        rCmd_ExhaustDamperPosition_pct := 50.0;
        rStartupACDTimer_s := rStartupACDTimer_s + rLocalDeltaT_s;

        (* Lower beam smoothly toward nominal target resistance *)
        IF rPot_FilteredResistance_uOhm > 5.80 THEN
            rCmd_AnodeBeamHoistPulse_mm := -0.50; (* Lower beam by 0.5 mm steps *)
            bCmd_AnodeBeamHoistDown := TRUE;
            bCmd_AnodeBeamHoistUp := FALSE;
        ELSIF rPot_FilteredResistance_uOhm < 4.20 THEN
            rCmd_AnodeBeamHoistPulse_mm := 0.50;  (* Raise beam by 0.5 mm steps *)
            bCmd_AnodeBeamHoistUp := TRUE;
            bCmd_AnodeBeamHoistDown := FALSE;
        ELSE
            rCmd_AnodeBeamHoistPulse_mm := 0.0;
            bCmd_AnodeBeamHoistUp := FALSE;
            bCmd_AnodeBeamHoistDown := FALSE;
        END_IF;

        (* Transition to Nominal Closed-Loop MPC once resistance and current stabilize *)
        IF (rPot_FilteredResistance_uOhm >= 4.40 AND rPot_FilteredResistance_uOhm <= 5.60) AND
           (rPot_VotedLineCurrent_kA >= 480.0) AND (rStartupACDTimer_s >= 600.0) THEN
            nFSM_CurrentState := 4; (* Nominal Production Operation *)
        END_IF;

        IF bCmd_StopCycle THEN
            nFSM_CurrentState := 12;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 4: STATE_NOMINAL_ELECTROLYSIS_CLOSED_LOOP_MPC
     * Core steady-state production mode: 6x6 state space and 10-iteration unrolled MPC actively modulating cell.
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        bPot_FeedingModeNominal := TRUE;
        bPot_FeedingModeUnderfeed := FALSE;
        bPot_FeedingModeOverfeed := FALSE;
        bPot_BeamRockingActive := FALSE;
        bCmd_AnodeEffectHornStrobe := FALSE;

        (* Route MPC optimizer outputs to physical command setpoints *)
        rCmd_AnodeBeamHoistPulse_mm := arrU_Applied[1];
        rCmd_PointFeederPulseRate_ppm := arrU_Applied[2];
        rCmd_AlF3AdditionDose_pct := arrU_Applied[3];
        rCmd_ExhaustDamperPosition_pct := arrU_Applied[4];

        (* Trigger Beam Move execution state if optimizer commands displacement beyond deadband *)
        IF ABS(rCmd_AnodeBeamHoistPulse_mm) >= rBeamDeadband_mm THEN
            nFSM_CurrentState := 6; (* Execute Anode Beam Hoist Move *)
        END_IF;

        (* Feeder Inter-Pulse Cycle Timer Accounting *)
        rFeederCycleTimer_s := rFeederCycleTimer_s + rLocalDeltaT_s;
        IF rCmd_PointFeederPulseRate_ppm > 0.50 THEN
            rTargetPulsePeriod_s := 60.0 / rCmd_PointFeederPulseRate_ppm;
        ELSE
            rTargetPulsePeriod_s := 120.0;
        END_IF;

        IF rFeederCycleTimer_s >= rTargetPulsePeriod_s THEN
            rFeederCycleTimer_s := 0.0;
            nFSM_CurrentState := 5; (* Execute Point Feeder Pulse Cycle *)
        END_IF;

        (* Evaluate Early Anode Effect Slope / Curvature Warning *)
        IF bPot_EarlyAnodeEffectWarning THEN
            nFSM_CurrentState := 7; (* Early AE Warning Mitigation *)
        END_IF;

        (* Evaluate Full Flash Anode Effect Critical Event *)
        IF bPot_InAnodeEffect OR (rPot_VotedCellVoltage_V >= c_Volt_AnodeEffect_Threshold) THEN
            nFSM_CurrentState := 8; (* Full Anode Effect Suppression *)
        END_IF;

        (* Operator and Maintenance Service Requests *)
        IF bCmd_AnodeChangeRequest AND NOT bDI_AnodeChangerCraneInPotArea THEN
            nFSM_CurrentState := 9; (* Carbon Anode Block Replacement *)
        ELSIF bCmd_MetalTapRequest AND bDI_TappingSuctionWandEngaged THEN
            nFSM_CurrentState := 10; (* Liquid Metal Tap *)
        ELSIF rAlF3CycleTimer_s >= 86400.0 OR (rExcessAlF3_pct < 9.50) THEN
            nFSM_CurrentState := 11; (* Bath Chemistry AlF3 Correction *)
        ELSIF bCmd_StopCycle THEN
            nFSM_CurrentState := 12; (* Controlled De-energization *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 5: STATE_REGULAR_POINT_FEEDER_PULSE_CYCLE
     * Sequences crust breaker pneumatic chisel stroke followed by volumetric alumina metering plunger discharge.
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        rFeederShotDurationTimer_s := rFeederShotDurationTimer_s + rLocalDeltaT_s;

        (* Sub-phase A: High-Force Crust Breaker Chisel Punch (0.0 to 2.0 s) *)
        IF rFeederShotDurationTimer_s < 2.00 THEN
            bCrustBreakerActive := TRUE;
            bFeederShotActive := FALSE;
            CASE nActiveFeederHead OF
                1: bCmd_CrustBreakerPunch1 := TRUE;
                2: bCmd_CrustBreakerPunch2 := TRUE;
                3: bCmd_CrustBreakerPunch3 := TRUE;
                4: bCmd_CrustBreakerPunch4 := TRUE;
            END_CASE;
        (* Sub-phase B: Volumetric Alumina Plunger Injection (2.0 to 3.8 s) *)
        ELSIF rFeederShotDurationTimer_s < 3.80 THEN
            bCrustBreakerActive := FALSE;
            bFeederShotActive := TRUE;
            bCmd_CrustBreakerPunch1 := FALSE;
            bCmd_CrustBreakerPunch2 := FALSE;
            bCmd_CrustBreakerPunch3 := FALSE;
            bCmd_CrustBreakerPunch4 := FALSE;
            CASE nActiveFeederHead OF
                1: bCmd_PointFeederFire1 := TRUE;
                2: bCmd_PointFeederFire2 := TRUE;
                3: bCmd_PointFeederFire3 := TRUE;
                4: bCmd_PointFeederFire4 := TRUE;
            END_CASE;
        (* Sub-phase C: Retraction and Complete *)
        ELSE
            bCmd_PointFeederFire1 := FALSE;
            bCmd_PointFeederFire2 := FALSE;
            bCmd_PointFeederFire3 := FALSE;
            bCmd_PointFeederFire4 := FALSE;
            bFeederShotActive := FALSE;
            rFeederShotDurationTimer_s := 0.0;

            (* Advance round-robin active feeder index *)
            nActiveFeederHead := nActiveFeederHead + 1;
            IF nActiveFeederHead > 4 THEN
                nActiveFeederHead := 1;
            END_IF;

            (* Return to Nominal Closed Loop *)
            nFSM_CurrentState := 4;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 6: STATE_ANODE_BEAM_INCREMENTAL_TRACKING_MOVE
     * Drives electromechanical hoist jack screws to physically displace the 50-ton carbon anode assembly.
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        rHoistDutyCycleTimer_s := rHoistDutyCycleTimer_s + rLocalDeltaT_s;

        IF rCmd_AnodeBeamHoistPulse_mm > 0.0 THEN
            (* Commanded upward move *)
            IF NOT bDI_AnodeHoistUpperLimit_LS THEN
                bCmd_AnodeBeamHoistUp := TRUE;
                bCmd_AnodeBeamHoistDown := FALSE;
            ELSE
                bCmd_AnodeBeamHoistUp := FALSE;
            END_IF;
        ELSIF rCmd_AnodeBeamHoistPulse_mm < 0.0 THEN
            (* Commanded downward move *)
            IF NOT bDI_AnodeHoistLowerLimit_LS AND (rPot_EstAnodeCathodeDist_mm > c_ACD_Trip_L) THEN
                bCmd_AnodeBeamHoistDown := TRUE;
                bCmd_AnodeBeamHoistUp := FALSE;
            ELSE
                bCmd_AnodeBeamHoistDown := FALSE;
            END_IF;
        ELSE
            bCmd_AnodeBeamHoistUp := FALSE;
            bCmd_AnodeBeamHoistDown := FALSE;
        END_IF;

        (* Pulse completion: typical mechanical step takes 1.2 seconds *)
        IF rFSM_StateTimer_s >= 1.200 OR ABS(rPot_VotedBeamPos_mm - arrX_Trajectory[0, 4]) < 0.15 THEN
            bCmd_AnodeBeamHoistUp := FALSE;
            bCmd_AnodeBeamHoistDown := FALSE;
            rCmd_AnodeBeamHoistPulse_mm := 0.0;
            nFSM_CurrentState := 4; (* Return to nominal closed loop *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 7: STATE_EARLY_ANODE_EFFECT_PREDICTION_WARNING
     * Preemptive intervention: Rapid overfeed pulsing and preparatory down-stroke before full AE flash.
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        bPot_FeedingModeNominal := FALSE;
        bPot_FeedingModeUnderfeed := FALSE;
        bPot_FeedingModeOverfeed := TRUE;
        bCmd_AnodeEffectHornStrobe := TRUE;

        (* Maximize alumina feed rate: 45 pulses/min across all 4 feeders *)
        rCmd_PointFeederPulseRate_ppm := 45.0;
        rCmd_ExhaustDamperPosition_pct := 75.0;

        (* Preemptive micro-lowering: nudge beam down by 1.2 mm to thin stagnant bubble blanket *)
        IF rFSM_StateTimer_s < 2.00 THEN
            rCmd_AnodeBeamHoistPulse_mm := -1.20;
            bCmd_AnodeBeamHoistDown := TRUE;
            bCmd_AnodeBeamHoistUp := FALSE;
        ELSE
            bCmd_AnodeBeamHoistDown := FALSE;
            rCmd_AnodeBeamHoistPulse_mm := 0.0;
        END_IF;

        (* Fire all feeders rapidly in staggered pairs *)
        IF rFSM_StateTimer_s >= 0.50 AND rFSM_StateTimer_s < 2.20 THEN
            bCmd_PointFeederFire1 := TRUE;
            bCmd_PointFeederFire3 := TRUE;
        ELSIF rFSM_StateTimer_s >= 2.20 AND rFSM_StateTimer_s < 3.90 THEN
            bCmd_PointFeederFire1 := FALSE;
            bCmd_PointFeederFire3 := FALSE;
            bCmd_PointFeederFire2 := TRUE;
            bCmd_PointFeederFire4 := TRUE;
        ELSE
            bCmd_PointFeederFire2 := FALSE;
            bCmd_PointFeederFire4 := FALSE;
        END_IF;

        (* If slope abates and alumina recovers, return to nominal state *)
        IF (rPot_ResistanceSlope_uOhm_min < (c_ResSlope_EarlyAE_Warn * 0.35)) AND (arrX_hat[2] >= 2.25) AND (rFSM_StateTimer_s >= 8.0) THEN
            bCmd_AnodeEffectHornStrobe := FALSE;
            bPot_EarlyAnodeEffectWarning := FALSE;
            nFSM_CurrentState := 4;
        END_IF;

        (* If voltage spikes past AE threshold, escalate immediately to full AE suppression *)
        IF rPot_VotedCellVoltage_V >= c_Volt_AnodeEffect_Threshold THEN
            nFSM_CurrentState := 8;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 8: STATE_ANODE_EFFECT_SUPPRESSION_GAS_DISPERSAL
     * Critical full-flash suppression: Anode Beam Rocking, 100% draft exhaust, continuous crust breaker punching.
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        bPot_InAnodeEffect := TRUE;
        bPot_BeamRockingActive := TRUE;
        bCmd_AnodeEffectHornStrobe := TRUE;
        rCmd_ExhaustDamperPosition_pct := 100.0; (* Full hood draft to capture CF4/C2F6 fluorocarbons *)
        rCmd_PointFeederPulseRate_ppm := 60.0;   (* Max alumina feeding *)

        (* Execute Dynamic Anode Beam Rocking Routine *)
        rBeamRockingTimer_s := rBeamRockingTimer_s + rLocalDeltaT_s;
        CASE nBeamRockingStage OF
            0: (* Initialize Rocking Base Elevation *)
                rPreRockingSavedPos_mm := rPot_VotedBeamPos_mm;
                nBeamRockingStage := 1;
                rBeamRockingTimer_s := 0.0;

            1: (* Sub-step 1: High-Speed Down-Stroke (-4.8 mm) to squeeze and displace gas film *)
                bCmd_AnodeBeamHoistDown := TRUE;
                bCmd_AnodeBeamHoistUp := FALSE;
                rCmd_AnodeBeamHoistPulse_mm := -rRockingStrokeDepth_mm;
                IF rBeamRockingTimer_s >= 3.20 OR (rPot_EstAnodeCathodeDist_mm <= 30.0) THEN
                    bCmd_AnodeBeamHoistDown := FALSE;
                    nBeamRockingStage := 2;
                    rBeamRockingTimer_s := 0.0;
                END_IF;

            2: (* Sub-step 2: Bottom Dwell with continuous breaker chisel punching *)
                bCmd_AnodeBeamHoistDown := FALSE;
                bCmd_AnodeBeamHoistUp := FALSE;
                bCmd_CrustBreakerPunch1 := TRUE;
                bCmd_CrustBreakerPunch2 := TRUE;
                bCmd_CrustBreakerPunch3 := TRUE;
                bCmd_CrustBreakerPunch4 := TRUE;
                bCmd_PointFeederFire1 := TRUE;
                bCmd_PointFeederFire2 := TRUE;
                bCmd_PointFeederFire3 := TRUE;
                bCmd_PointFeederFire4 := TRUE;
                IF rBeamRockingTimer_s >= 4.00 THEN
                    nBeamRockingStage := 3;
                    rBeamRockingTimer_s := 0.0;
                END_IF;

            3: (* Sub-step 3: Rapid Retract Upward back to nominal elevation *)
                bCmd_CrustBreakerPunch1 := FALSE;
                bCmd_CrustBreakerPunch2 := FALSE;
                bCmd_CrustBreakerPunch3 := FALSE;
                bCmd_CrustBreakerPunch4 := FALSE;
                bCmd_PointFeederFire1 := FALSE;
                bCmd_PointFeederFire2 := FALSE;
                bCmd_PointFeederFire3 := FALSE;
                bCmd_PointFeederFire4 := FALSE;
                bCmd_AnodeBeamHoistUp := TRUE;
                bCmd_AnodeBeamHoistDown := FALSE;
                rCmd_AnodeBeamHoistPulse_mm := rRockingStrokeDepth_mm;
                IF rBeamRockingTimer_s >= 3.20 OR (rPot_VotedBeamPos_mm >= rPreRockingSavedPos_mm) THEN
                    bCmd_AnodeBeamHoistUp := FALSE;
                    nBeamRockingStage := 0; (* Reset rocking stage *)
                    rBeamRockingTimer_s := 0.0;
                END_IF;
        END_CASE;

        (* Extinction Verification: Cell voltage collapses below 4.60 V for 4.0 seconds *)
        IF rPot_VotedCellVoltage_V <= 4.60 THEN
            rAnodeEffectDurationTimer_s := rAnodeEffectDurationTimer_s + rLocalDeltaT_s;
            IF rAnodeEffectDurationTimer_s >= 4.00 THEN
                bPot_InAnodeEffect := FALSE;
                bPot_BeamRockingActive := FALSE;
                bCmd_AnodeEffectHornStrobe := FALSE;
                nBeamRockingStage := 0;
                rAnodeEffectDurationTimer_s := 0.0;
                nFSM_CurrentState := 4; (* Return to nominal closed loop *)
            END_IF;
        ELSE
            rAnodeEffectDurationTimer_s := 0.0;
        END_IF;

        (* Severe Timeout: If Anode Effect persists beyond 240 s, trigger emergency trip *)
        IF rFSM_StateTimer_s >= 240.0 THEN
            nFSM_CurrentState := 13;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------------
     * STATE 9: STATE_AUTOMATED_CARBON_ANODE_BLOCK_CHANGE
     * Crane removes spent carbon anode butt and inserts new cold anode block.
     * --------------------------------------------------------------------------------------------------------------------- *)
    9:
        rAnodeChangeElapsedTime_s := rAnodeChangeElapsedTime_s + rLocalDeltaT_s;
        rCmd_AnodeBeamHoistPulse_mm := 0.0;
        bCmd_AnodeBeamHoistUp := FALSE;
        bCmd_AnodeBeamHoistDown := FALSE;
        rCmd_PointFeederPulseRate_ppm := 15.0; (* Low baseline feed during anode change *)
        rCmd_ExhaustDamperPosition_pct := 85.0; (* High draft to capture air ingress *)

        (* Complete cycle once crane departs pot operating zone and operator releases request *)
        IF (NOT bCmd_AnodeChangeRequest AND NOT bDI_AnodeChangerCraneInPotArea) OR (rAnodeChangeElapsedTime_s >= 1800.0) THEN
            rAnodeChangeElapsedTime_s := 0.0;
            nFSM_CurrentState := 4;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------------
     * STATE 10: STATE_VACUUM_CRUCIBLE_LIQUID_ALUMINUM_TAP
     * Vacuum siphon extracts 2.0 tons molten Al metal pad; beam descends concurrently to preserve ACD.
     * --------------------------------------------------------------------------------------------------------------------- *)
    10:
        rMetalTapElapsedTime_s := rMetalTapElapsedTime_s + rLocalDeltaT_s;
        rCmd_ExhaustDamperPosition_pct := 60.0;

        (* Coordinated Beam Downward Tracking to match metal pad level drop: dACD/dt = 0 *)
        IF rPot_EstAnodeCathodeDist_mm > 43.50 THEN
            rCmd_AnodeBeamHoistPulse_mm := -0.35;
            bCmd_AnodeBeamHoistDown := TRUE;
            bCmd_AnodeBeamHoistUp := FALSE;
        ELSE
            bCmd_AnodeBeamHoistDown := FALSE;
            rCmd_AnodeBeamHoistPulse_mm := 0.0;
        END_IF;

        (* Complete tap once suction wand disengages and operator clears tap request *)
        IF (NOT bCmd_MetalTapRequest AND NOT bDI_TappingSuctionWandEngaged) OR (rMetalTapElapsedTime_s >= 1200.0) THEN
            rMetalTapElapsedTime_s := 0.0;
            bCmd_AnodeBeamHoistDown := FALSE;
            nFSM_CurrentState := 4;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------------
     * STATE 11: STATE_BATH_CHEMISTRY_ALF3_CORRECTION_CYCLE
     * Dosing aluminum fluoride (AlF3) powder to restore cryolite ratio (CR = NaF / AlF3 = 2.22).
     * --------------------------------------------------------------------------------------------------------------------- *)
    11:
        rAlF3AdditionElapsedTime_s := rAlF3AdditionElapsedTime_s + rLocalDeltaT_s;
        rCmd_AlF3AdditionDose_pct := 65.0; (* Pulse AlF3 vibratory hopper *)
        rCmd_ExhaustDamperPosition_pct := 55.0;

        IF rAlF3AdditionElapsedTime_s >= 300.0 THEN
            rCmd_AlF3AdditionDose_pct := 0.0;
            rAlF3AdditionElapsedTime_s := 0.0;
            rAlF3CycleTimer_s := 0.0;
            nFSM_CurrentState := 4;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------------
     * STATE 12: STATE_CONTROLLED_POT_DE-ENERGIZATION_BYPASS
     * Shunting 500 kA line current through mechanical wedge bypass switches for scheduled pot overhaul.
     * --------------------------------------------------------------------------------------------------------------------- *)
    12:
        rBypassElapsedTime_s := rBypassElapsedTime_s + rLocalDeltaT_s;
        rCmd_AnodeBeamHoistPulse_mm := 0.0;
        bCmd_AnodeBeamHoistUp := FALSE;
        bCmd_AnodeBeamHoistDown := FALSE;
        rCmd_PointFeederPulseRate_ppm := 0.0;
        rCmd_AlF3AdditionDose_pct := 0.0;
        rCmd_ExhaustDamperPosition_pct := 20.0;

        (* Engage heavy potline bypass shunt wedge *)
        bCmd_PotlineBypassShuntWedgeFire := TRUE;

        IF bDI_PotBypassSwitchClosed THEN
            nFSM_CurrentState := 0; (* Pot is fully shunted, return to Idle *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------------
     * STATE 13: STATE_EMERGENCY_POT_TAP_LEAK_OR_ACD_COLLAPSE_TRIP
     * Catastrophic safety shutdown: immediate bypass shunt fire, hoist freeze, and alarm latching.
     * --------------------------------------------------------------------------------------------------------------------- *)
    13:
        bPot_EmergencyTripped := TRUE;
        bCmd_PotlineBypassShuntWedgeFire := TRUE; (* Shunt current immediately to prevent catastrophic burn-out *)
        bCmd_AnodeEffectHornStrobe := TRUE;
        rCmd_AnodeBeamHoistPulse_mm := 0.0;
        bCmd_AnodeBeamHoistUp := FALSE;
        bCmd_AnodeBeamHoistDown := FALSE;
        rCmd_PointFeederPulseRate_ppm := 0.0;
        bCmd_PointFeederFire1 := FALSE;
        bCmd_PointFeederFire2 := FALSE;
        bCmd_PointFeederFire3 := FALSE;
        bCmd_PointFeederFire4 := FALSE;
        bCmd_CrustBreakerPunch1 := FALSE;
        bCmd_CrustBreakerPunch2 := FALSE;
        bCmd_CrustBreakerPunch3 := FALSE;
        bCmd_CrustBreakerPunch4 := FALSE;
        rCmd_AlF3AdditionDose_pct := 0.0;
        rCmd_ExhaustDamperPosition_pct := 100.0;

        rTripLockoutTimer_s := rTripLockoutTimer_s + rLocalDeltaT_s;

        (* Exit trip only upon operator reset command with all interlocks healthy and minimum 30 s dwell *)
        IF bCmd_ResetTrip AND NOT bDI_EmergencyStop_PB AND NOT bDI_AnodeHoistMotorOverload AND
           (rPot_EstAnodeCathodeDist_mm > c_ACD_Trip_LL) AND (rTripLockoutTimer_s >= 30.0) THEN
            bPot_EmergencyTripped := FALSE;
            bCmd_AnodeEffectHornStrobe := FALSE;
            rTripLockoutTimer_s := 0.0;
            nFSM_CurrentState := 0; (* Return to Idle for controlled restart *)
        END_IF;

ELSE
    nFSM_CurrentState := 0;
END_CASE;

(* Route Active State to Block Output *)
nFSM_CurrentState := nFSM_CurrentState;
'''
