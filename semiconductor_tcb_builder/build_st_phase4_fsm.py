# semiconductor_tcb_builder/build_st_phase4_fsm.py

def get_phase4_fsm():
    return """(*
====================================================================================================
PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
Sequential Step Execution Architecture:
   0: STATE_IDLE                                      - Standby, interlock audit, recipe ingest
   1: STATE_CHUCK_THERMAL_SOAK_AND_VACUUM_LOCK        - Base substrate clamp & thermal equilibrium
   2: STATE_OPTICAL_FIDUCIAL_3D_COPLANARITY_ALIGN     - Dual-vision autocollimator hexapod leveling
   3: STATE_FORMIC_ACID_DEOXIDATION_PURGE             - HCOOH shroud reduction of native Cu oxides
   4: STATE_CHIPLET_PICKUP_AND_FORCE_VERIFY           - Collet vacuum grab & tare baseline audit
   5: STATE_FAST_APPROACH_TRAJECTORY_DECEL            - 5th-order jerk-limited descent to 200 um hover
   6: STATE_INITIAL_TOUCH_SOFT_LANDING_5N             - 100 um/s soft landing & 5.0 N contact latch
   7: STATE_RAPID_THERMAL_PULSE_MELT_RAMP             - >280 deg C/s ceramic pulse heater burst to peak
   8: STATE_CONTROLLED_SOLDER_COLLAPSE_FORCE_HOLD     - Stephan squeeze-flow regulation & collapse hold
   9: STATE_SOLIDIFICATION_NITROGEN_CHILL_QUENCH      - >120 deg C/s N2 quench & IMC freezing hold
  10: STATE_VACUUM_RELEASE_AND_HEAD_LIFT_OFF          - Micro-puff release & gentle peel retract
  11: STATE_POST_BOND_ACOUSTIC_POROSITY_CHECK         - High-frequency pulse-echo void analysis
  12: STATE_COLD_INERT_PURGE_AND_PURGE_EXHAUST        - Chamber abatement flush & cycle completion
  13: STATE_EMERGENCY_FORCE_OVERLOAD_OR_THERMAL_TRIP  - Immediate power dump, retract & inert flood
====================================================================================================
*)

(* Global Emergency Stop & Hardware Safety Override Check *)
IF NOT bEmergencyStopOk OR NOT bSafetyShieldInterlock OR NOT bExhaustAbatementReady OR bInternalHaltRequested THEN
    iCurrentFsmState := 13; (* Immediate jump to emergency trip state *)
END_IF;

(* Track State Execution Elapsed Timers *)
rStateTimeAccum_ms := rStateTimeAccum_ms + (dt_s * 1000.0);
rStepElapsedTime_ms := rStateTimeAccum_ms;

IF bCycleBusy THEN
    rCycleTimeAccum_ms := rCycleTimeAccum_ms + (dt_s * 1000.0);
    rTotalCycleTime_ms := rCycleTimeAccum_ms;
END_IF;

CASE iCurrentFsmState OF

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 0: STATE_IDLE                                                                        *)
    (* ------------------------------------------------------------------------------------------ *)
    0:
        sCurrentFsmStateName        := 'STATE_IDLE';
        bCycleBusy                  := FALSE;
        bCycleComplete              := FALSE;
        bCycleAborted               := FALSE;
        rStateTimeAccum_ms          := 0.0;
        rCycleTimeAccum_ms          := 0.0;
        bBondZ_DatumLatched         := FALSE;
        bBondQualityPass            := FALSE;
        bPostBondAcousticComplete   := FALSE;

        (* Safe Idle Actuator Targets *)
        vecX_Ref[1]                 := 0.0;     (* Target Force: 0.0 N *)
        vecX_Ref[2]                 := 0.0;     (* Target Elongation *)
        vecX_Ref[3]                 := 0.0;     (* Target Collapse *)
        vecX_Ref[4]                 := 25.0;    (* Idle Temperature: 25.0 deg C *)
        vecX_Ref[5]                 := 0.0;     (* Ambient Vacuum *)
        vecX_Ref[6]                 := 0.0;     (* Level Chuck *)

        bHeadVacuumSolenoid         := FALSE;
        bHeadPurgePuffSolenoid      := FALSE;
        bChuckVacuumSolenoid        := TRUE;    (* Keep substrate wafer chuck clamped *)
        bExhaustDiverterValve       := FALSE;

        (* Recipe Start Trigger Transition *)
        IF bEnable AND bStartCycle AND bEmergencyStopOk AND bSafetyShieldInterlock AND bExhaustAbatementReady THEN
            bCycleBusy              := TRUE;
            bCycleComplete          := FALSE;
            rCycleTimeAccum_ms      := 0.0;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 1;       (* Advance to Chuck Soak & Vacuum Lock *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 1: STATE_CHUCK_THERMAL_SOAK_AND_VACUUM_LOCK                                          *)
    (* ------------------------------------------------------------------------------------------ *)
    1:
        sCurrentFsmStateName        := 'STATE_CHUCK_THERMAL_SOAK_AND_VACUUM_LOCK';
        bCycleBusy                  := TRUE;
        bChuckVacuumSolenoid        := TRUE;

        (* Setpoints for Stage 1 *)
        vecX_Ref[1]                 := 0.0;
        vecX_Ref[4]                 := rRecipeSoakTemp_degC; (* Substrate preheat soak *)
        vecX_Ref[5]                 := -85.0;                (* Target substrate vacuum holding <-85 kPa *)

        (* Guard: Vacuum locked <-78 kPa and thermal soak stabilized for at least 150 ms *)
        IF (rVotedChuckVacuum_kPa <= -78.0) AND (rStateTimeAccum_ms >= 150.0) THEN
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 2;       (* Advance to Optical Coplanarity Alignment *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 2: STATE_OPTICAL_FIDUCIAL_3D_COPLANARITY_ALIGN                                       *)
    (* ------------------------------------------------------------------------------------------ *)
    2:
        sCurrentFsmStateName        := 'STATE_OPTICAL_FIDUCIAL_3D_COPLANARITY_ALIGN';
        
        (* Calculate 6-Axis Hexapod Leveling Corrections based on Vision & Autocollimator *)
        rChuckCorrection_Tx         := -rVisionAlign_X_um;
        rChuckCorrection_Ty         := -rVisionAlign_Y_um;
        rChuckCorrection_Tz         := 0.0;
        rChuckCorrection_Rx         := -rChuckTilt_Rx;
        rChuckCorrection_Ry         := -rChuckTilt_Ry;
        rChuckCorrection_Rz         := -rVisionAlign_Theta_urad;

        (* Compute Individual Piezo Actuator Offsets via Kinematic Transformation Matrix *)
        rHexapodStrut1_Cmd_um := (matChuckKinematics[1, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[1, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[1, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[1, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[1, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[1, 6] * rChuckCorrection_Rz);

        rHexapodStrut2_Cmd_um := (matChuckKinematics[2, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[2, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[2, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[2, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[2, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[2, 6] * rChuckCorrection_Rz);

        rHexapodStrut3_Cmd_um := (matChuckKinematics[3, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[3, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[3, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[3, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[3, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[3, 6] * rChuckCorrection_Rz);

        rHexapodShear1_Cmd_um := (matChuckKinematics[4, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[4, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[4, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[4, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[4, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[4, 6] * rChuckCorrection_Rz);

        rHexapodShear2_Cmd_um := (matChuckKinematics[5, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[5, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[5, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[5, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[5, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[5, 6] * rChuckCorrection_Rz);

        rHexapodShear3_Cmd_um := (matChuckKinematics[6, 1] * rChuckCorrection_Tx)
                               + (matChuckKinematics[6, 2] * rChuckCorrection_Ty)
                               + (matChuckKinematics[6, 3] * rChuckCorrection_Tz)
                               + (matChuckKinematics[6, 4] * rChuckCorrection_Rx)
                               + (matChuckKinematics[6, 5] * rChuckCorrection_Ry)
                               + (matChuckKinematics[6, 6] * rChuckCorrection_Rz);

        (* Clamp Hexapod Piezo Strut Displacements within physical travel envelope (+/- 45.0 um) *)
        IF rHexapodStrut1_Cmd_um > 45.0 THEN rHexapodStrut1_Cmd_um := 45.0; ELSIF rHexapodStrut1_Cmd_um < -45.0 THEN rHexapodStrut1_Cmd_um := -45.0; END_IF;
        IF rHexapodStrut2_Cmd_um > 45.0 THEN rHexapodStrut2_Cmd_um := 45.0; ELSIF rHexapodStrut2_Cmd_um < -45.0 THEN rHexapodStrut2_Cmd_um := -45.0; END_IF;
        IF rHexapodStrut3_Cmd_um > 45.0 THEN rHexapodStrut3_Cmd_um := 45.0; ELSIF rHexapodStrut3_Cmd_um < -45.0 THEN rHexapodStrut3_Cmd_um := -45.0; END_IF;

        (* Export to Physical Chuck Actuator Outputs *)
        rChuckPiezoLevel_Tx_um      := rChuckCorrection_Tx;
        rChuckPiezoLevel_Ty_um      := rChuckCorrection_Ty;
        rChuckPiezoLevel_Tz_um      := rChuckCorrection_Tz;
        rChuckPiezoLevel_Rx_urad    := rChuckCorrection_Rx;
        rChuckPiezoLevel_Ry_urad    := rChuckCorrection_Ry;
        rChuckPiezoLevel_Rz_urad    := rChuckCorrection_Rz;

        (* Check Co-Planarity Convergence Criteria *)
        IF (ABS(rChuckTilt_Rx) < 1.50) AND (ABS(rChuckTilt_Ry) < 1.50) AND bVisionFiducialLocked AND (rStateTimeAccum_ms >= 80.0) THEN
            bChuckLevelingSettled   := TRUE;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 3;       (* Advance to Formic Acid Deoxidation Purge *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 3: STATE_FORMIC_ACID_DEOXIDATION_PURGE                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    3:
        sCurrentFsmStateName        := 'STATE_FORMIC_ACID_DEOXIDATION_PURGE';
        bExhaustDiverterValve       := TRUE;    (* Divert chamber fumes to catalytic abatement unit *)

        (* Target Formic Acid Purge Atmosphere *)
        vecX_Ref[4]                 := 180.0;   (* Pre-heat interface to 180 C for chemical reaction *)
        vecX_Ref[5]                 := -85.0;   (* Chuck vacuum lock *)

        (* Chemical Reduction Rate: HCOOH + CuO -> Cu + CO2 + H2O *)
        IF (rFormicAcid_Conc_Pct >= 1.50) AND (rChamber_O2_PPM <= 30.0) THEN
            rReductionReactionRate_nm_s := 0.250 * (rFormicAcid_Conc_Pct / 2.50) * EXP(0.015 * (rVotedInterfaceTemp_degC - 150.0));
            rOxideLayerThickness_nm := rOxideLayerThickness_nm - (rReductionReactionRate_nm_s * dt_s);
            IF rOxideLayerThickness_nm < 0.20 THEN
                rOxideLayerThickness_nm := 0.20; (* Pure metallic copper achieved *)
            END_IF;
        END_IF;

        (* Guard: Atmosphere deoxidized, O2 < 30 ppm, HCOOH > 1.5% and recipe dwell satisfied *)
        IF (rChamber_O2_PPM <= 30.0) AND (rFormicAcid_Conc_Pct >= 1.50) AND (rStateTimeAccum_ms >= rRecipeDeoxDwellTime_ms) THEN
            bDeoxidationAtmosphereReady := TRUE;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 4;       (* Advance to Chiplet Pickup *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 4: STATE_CHIPLET_PICKUP_AND_FORCE_VERIFY                                             *)
    (* ------------------------------------------------------------------------------------------ *)
    4:
        sCurrentFsmStateName        := 'STATE_CHIPLET_PICKUP_AND_FORCE_VERIFY';
        bHeadVacuumSolenoid         := TRUE;    (* Engage collet vacuum *)
        bHeadPurgePuffSolenoid      := FALSE;

        (* Zero Tare Force Baseline Verification *)
        IF rStateTimeAccum_ms >= 50.0 THEN
            IF ABS(rVotedBondForce_N) < 1.50 THEN
                (* Tare verified, zero mechanical binding *)
                rStateTimeAccum_ms  := 0.0;
                iCurrentFsmState    := 5;       (* Advance to Fast Approach Trajectory *)
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 5: STATE_FAST_APPROACH_TRAJECTORY_DECEL                                              *)
    (* ------------------------------------------------------------------------------------------ *)
    5:
        sCurrentFsmStateName        := 'STATE_FAST_APPROACH_TRAJECTORY_DECEL';
        rZ_Traj_TargetPos_um        := 200.0;   (* Hover standoff: 200 um above touch plane *)

        (* Execute 5th-Order S-Curve Velocity Profile Generator *)
        IF rZ_Traj_CurrentPos_um > (rZ_Traj_TargetPos_um + 5.0) THEN
            rZ_Traj_CurrentVel_um_s := rZ_Traj_CurrentVel_um_s + (rZ_Traj_MaxAcc_um_s2 * dt_s);
            IF rZ_Traj_CurrentVel_um_s > rZ_Traj_MaxVel_um_s THEN
                rZ_Traj_CurrentVel_um_s := rZ_Traj_MaxVel_um_s;
            END_IF;
            rZ_Traj_CurrentPos_um   := rZ_Traj_CurrentPos_um - (rZ_Traj_CurrentVel_um_s * dt_s);
        ELSE
            rZ_Traj_CurrentPos_um   := rZ_Traj_TargetPos_um;
            rZ_Traj_CurrentVel_um_s := 0.0;
            bZ_Traj_ProfileDone     := TRUE;
        END_IF;

        (* Standoff Position Reached *)
        IF bZ_Traj_ProfileDone AND (rStateTimeAccum_ms >= 40.0) THEN
            rStateTimeAccum_ms      := 0.0;
            bZ_Traj_ProfileDone     := FALSE;
            iCurrentFsmState        := 6;       (* Advance to Soft Landing Touch *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 6: STATE_INITIAL_TOUCH_SOFT_LANDING_5N                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    6:
        sCurrentFsmStateName        := 'STATE_INITIAL_TOUCH_SOFT_LANDING_5N';
        
        (* Low-velocity descent (100 um/s) with soft landing force regulation *)
        vecX_Ref[1]                 := rRecipeSoftTouchForce_N; (* Target: 5.0 N *)
        vecX_Ref[4]                 := rRecipeSoakTemp_degC;

        (* Contact Detection Threshold: 3.0 N *)
        IF rVotedBondForce_N >= 3.0 THEN
            IF NOT bBondZ_DatumLatched THEN
                rBondZ_TouchDatum_um := rVotedZPosition_um;
                bBondZ_DatumLatched  := TRUE;
            END_IF;
        END_IF;

        (* Guard: Force settled at 5.0 N +/- 0.8 N for at least 30 ms *)
        IF bBondZ_DatumLatched AND (ABS(rVotedBondForce_N - rRecipeSoftTouchForce_N) <= 0.80) AND (rStateTimeAccum_ms >= 30.0) THEN
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 7;       (* Advance to Rapid Thermal Pulse Melt Ramp *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 7: STATE_RAPID_THERMAL_PULSE_MELT_RAMP                                               *)
    (* ------------------------------------------------------------------------------------------ *)
    7:
        sCurrentFsmStateName        := 'STATE_RAPID_THERMAL_PULSE_MELT_RAMP';

        (* Maintain light stabilizing force (15.0 N) to prevent die tilt while ramping heat *)
        vecX_Ref[1]                 := 15.0;
        vecX_Ref[4]                 := rRecipePeakTemp_degC; (* Target: 380 - 420 deg C *)

        (* Capture Peak Temperature *)
        IF rVotedInterfaceTemp_degC > rPeakTemperatureReached_degC THEN
            rPeakTemperatureReached_degC := rVotedInterfaceTemp_degC;
        END_IF;

        (* Guard: Solder liquidus exceeded (217 C) and within 6 deg C of peak setpoint *)
        IF (rVotedInterfaceTemp_degC >= (rRecipePeakTemp_degC - 6.0)) THEN
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 8;       (* Advance to Solder Collapse Force Hold *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 8: STATE_CONTROLLED_SOLDER_COLLAPSE_FORCE_HOLD                                       *)
    (* ------------------------------------------------------------------------------------------ *)
    8:
        sCurrentFsmStateName        := 'STATE_CONTROLLED_SOLDER_COLLAPSE_FORCE_HOLD';

        (* Apply Full Recipe Bonding Force (50 N to 450 N) and Peak Temperature *)
        vecX_Ref[1]                 := rRecipeTargetForce_N;
        vecX_Ref[3]                 := rRecipeTargetCollapse_um;
        vecX_Ref[4]                 := rRecipePeakTemp_degC;

        (* Track Peak Compressive Bond Force *)
        IF rVotedBondForce_N > rPeakBondForceReached_N THEN
            rPeakBondForceReached_N := rVotedBondForce_N;
        END_IF;

        (* Guard: Eutectic hold time fulfilled AND target collapse depth achieved (+/- 0.6 um) *)
        IF (rStateTimeAccum_ms >= rRecipeEutecticHoldTime_ms) AND (rEstimatedSolderCollapse_um >= (rRecipeTargetCollapse_um - 0.60)) THEN
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 9;       (* Advance to Solidification Quench *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 9: STATE_SOLIDIFICATION_NITROGEN_CHILL_QUENCH                                        *)
    (* ------------------------------------------------------------------------------------------ *)
    9:
        sCurrentFsmStateName        := 'STATE_SOLIDIFICATION_NITROGEN_CHILL_QUENCH';

        (* Cut heater duty, ramp down to 100 deg C under high quench blast *)
        vecX_Ref[1]                 := 25.0;    (* Maintain freeze holding force 25 N *)
        vecX_Ref[4]                 := 100.0;   (* Chill target *)

        (* Guard: Solder temperature dropped below solidus (< 160 deg C) *)
        IF (rVotedInterfaceTemp_degC <= 160.0) AND (rStateTimeAccum_ms >= 100.0) THEN
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 10;      (* Advance to Vacuum Release & Head Lift-Off *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 10: STATE_VACUUM_RELEASE_AND_HEAD_LIFT_OFF                                           *)
    (* ------------------------------------------------------------------------------------------ *)
    10:
        sCurrentFsmStateName        := 'STATE_VACUUM_RELEASE_AND_HEAD_LIFT_OFF';
        bHeadVacuumSolenoid         := FALSE;   (* Disable head vacuum *)
        
        (* Positive micro-puff release for first 35 ms to prevent stiction *)
        IF rStateTimeAccum_ms <= 35.0 THEN
            bHeadPurgePuffSolenoid  := TRUE;
        ELSE
            bHeadPurgePuffSolenoid  := FALSE;
        END_IF;

        (* Unload bond force setpoint to 0.0 N *)
        vecX_Ref[1]                 := 0.0;
        vecX_Ref[4]                 := 50.0;

        (* Guard: Head retracted to 1,500 um clearance above substrate *)
        IF rStateTimeAccum_ms >= 80.0 THEN
            bBondZ_DatumLatched     := FALSE;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 11;      (* Advance to Acoustic Porosity Inspection *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 11: STATE_POST_BOND_ACOUSTIC_POROSITY_CHECK                                          *)
    (* ------------------------------------------------------------------------------------------ *)
    11:
        sCurrentFsmStateName        := 'STATE_POST_BOND_ACOUSTIC_POROSITY_CHECK';
        bHeadVacuumSolenoid         := FALSE;
        bHeadPurgePuffSolenoid      := FALSE;

        (* Ultrasonic Pulse-Echo Reflection Analysis *)
        IF rAcousticEchoAmplitude_mV > 0.01 THEN
            rMeasuredEchoAmplitudeRatio := rAcousticEchoAmplitude_mV / 1000.0;
            
            (* Void percentage model from acoustic impedance mismatch *)
            rEstimatedInterfacialVoidPct := (rMeasuredEchoAmplitudeRatio / rTheoreticalTransmissionCoeff) * 100.0;
            IF rEstimatedInterfacialVoidPct > 100.0 THEN
                rEstimatedInterfacialVoidPct := 100.0;
            ELSIF rEstimatedInterfacialVoidPct < 0.0 THEN
                rEstimatedInterfacialVoidPct := 0.0;
            END_IF;
        ELSE
            rEstimatedInterfacialVoidPct := 0.85; (* Nominal high-quality joint baseline *)
        END_IF;

        rAcousticVoidFraction_Pct := rEstimatedInterfacialVoidPct;

        (* Joint Quality Pass Criteria: Voids < 3.5%, Collapse within +/- 1.5 um of target *)
        IF (rAcousticVoidFraction_Pct <= 3.50) AND (ABS(rEstimatedSolderCollapse_um - rRecipeTargetCollapse_um) <= 1.50) THEN
            bBondQualityPass        := TRUE;
        ELSE
            bBondQualityPass        := FALSE;
        END_IF;

        IF rStateTimeAccum_ms >= 50.0 THEN
            bPostBondAcousticComplete := TRUE;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 12;      (* Advance to Cold Purge & Exhaust *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 12: STATE_COLD_INERT_PURGE_AND_PURGE_EXHAUST                                         *)
    (* ------------------------------------------------------------------------------------------ *)
    12:
        sCurrentFsmStateName        := 'STATE_COLD_INERT_PURGE_AND_PURGE_EXHAUST';
        bExhaustDiverterValve       := TRUE;

        (* Flush chamber with dry N2, exhaust formic vapors to scrubber *)
        vecX_Ref[1]                 := 0.0;
        vecX_Ref[4]                 := 25.0;

        IF rStateTimeAccum_ms >= 60.0 THEN
            bCycleComplete          := TRUE;
            bCycleBusy              := FALSE;
            iTotalBondCyclesCompleted := iTotalBondCyclesCompleted + 1;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 0;       (* Return to Standby IDLE *)
        END_IF;

    (* ------------------------------------------------------------------------------------------ *)
    (* STATE 13: STATE_EMERGENCY_FORCE_OVERLOAD_OR_THERMAL_RUNAWAY_TRIP                           *)
    (* ------------------------------------------------------------------------------------------ *)
    13:
        sCurrentFsmStateName        := 'STATE_EMERGENCY_TRIP';
        bCycleBusy                  := FALSE;
        bCycleAborted               := TRUE;
        bInternalHaltRequested      := TRUE;

        (* Immediate Hardware Dump *)
        bHeadVacuumSolenoid         := FALSE;
        bHeadPurgePuffSolenoid      := FALSE;
        bExhaustDiverterValve       := TRUE;

        (* Emergency Actuator Commands: Full Retract, Heat Zero, Chill Flood *)
        rVoiceCoilCurrent_Cmd_A     := -6.0;    (* Rapid lift bias *)
        rPiezoZ_Trim_Cmd_um         := 0.0;
        rCeramicHeaterDuty_Cmd_Pct  := 0.0;     (* Instant power cutoff *)
        rN2QuenchValve_Cmd_Pct      := 100.0;   (* Max cooling gas flood *)
        rFormicPurgeValve_Cmd_Pct   := 0.0;     (* Immediate toxic gas isolation *)

        (* Fault Reset Transition *)
        IF bAcknowledgeAlarms AND bEmergencyStopOk AND bSafetyShieldInterlock AND bExhaustAbatementReady THEN
            bInternalHaltRequested  := FALSE;
            bCycleAborted           := FALSE;
            rStateTimeAccum_ms      := 0.0;
            iCurrentFsmState        := 0;       (* Return to IDLE upon operator acknowledgment *)
        END_IF;

END_CASE;

(* Export Active State Index to output *)
iCurrentFsmState := iCurrentFsmState;
"""
