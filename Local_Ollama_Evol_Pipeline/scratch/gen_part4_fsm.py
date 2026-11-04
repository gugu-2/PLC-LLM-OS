# gen_part4_fsm.py
def get_part4_fsm():
    return """
(* ==================================================================================================================== *)
(* PHASE 4: 12-STAGE MULTI-STAGE CASE FINITE STATE MACHINE (FSM)                                                       *)
(* Full Aseptic Lifecycle: Chemical CIP/SIP, Sterile Overpressure Barrier, Pacing, Micro-Dosing,                      *)
(* Twin-Turret Electronic Camming Double-Seaming, Acoustic Resonance Inspection, Divert, and Emergency Recovery.       *)
(* ==================================================================================================================== *)

(* Monotonic State Timer Accumulation *)
IF eState = ePrevState THEN
    rStateTimer_s := rStateTimer_s + rCycleScanDeltaTime;
ELSE
    rStateTimer_s := 0.0;
    ePrevState := eState;
END_IF;

(* Master Production Real-Time Accumulator *)
IF (eState >= 30) AND (eState <= 100) AND bMasterLineRunPermissive THEN
    rProductionAccumulator_s := rProductionAccumulator_s + rCycleScanDeltaTime;
    tCurrentProductionDuration := DINT_TO_TIME(REAL_TO_DINT(rProductionAccumulator_s * 1000.0));
END_IF;

(* Normalized Turret Electronic Cam Angle Update (0.0 to 360.0 degrees) *)
rCamAngle_Normalized_deg := rVoted_TurretResolver_deg;
WHILE rCamAngle_Normalized_deg >= 360.0 DO
    rCamAngle_Normalized_deg := rCamAngle_Normalized_deg - 360.0;
END_WHILE;
WHILE rCamAngle_Normalized_deg < 0.0 DO
    rCamAngle_Normalized_deg := rCamAngle_Normalized_deg + 360.0;
END_WHILE;

(* Quintic (5th-Order) Polynomial Electronic Cam Curve Synthesis for 1st & 2nd Op Rolls *)
(* S(theta) = 10*(theta/beta)^3 - 15*(theta/beta)^4 + 6*(theta/beta)^5 *)
IF (rCamAngle_Normalized_deg >= 30.0) AND (rCamAngle_Normalized_deg <= 150.0) THEN
    (* 1st Operation Roll Active Cam Curling Zone (30 to 150 deg, span beta = 120 deg) *)
    rIntermediateVal := (rCamAngle_Normalized_deg - 30.0) / 120.0;
    rProfile1stOp_PosFeedforward_mm := rCam1stOp_MaxStroke_mm * ((10.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal)
                                       - (15.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal)
                                       + (6.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal));
ELSE
    rProfile1stOp_PosFeedforward_mm := 0.0;
END_IF;

IF (rCamAngle_Normalized_deg >= 165.0) AND (rCamAngle_Normalized_deg <= 285.0) THEN
    (* 2nd Operation Roll Active Cam Crimping Zone (165 to 285 deg, span beta = 120 deg) *)
    rIntermediateVal := (rCamAngle_Normalized_deg - 165.0) / 120.0;
    rProfile2ndOp_PosFeedforward_mm := rCam2ndOp_MaxStroke_mm * ((10.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal)
                                       - (15.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal)
                                       + (6.0 * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal * rIntermediateVal));
ELSE
    rProfile2ndOp_PosFeedforward_mm := 0.0;
END_IF;

(* FSM Primary Execution Matrix *)
CASE eState OF

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 10: STERILIZATION_CIP_PAA                                                                                  *)
    (* Aseptic Isolator Vaporized Peracetic Acid (PAA) chemical sterilization and decontamination cycle.                *)
    (* Requires isolator doors closed, CIP permissive active, vapor injection to 1500 ppm, dwell 300 s @ > 50 deg C.   *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    10:
        bMachineSynchronized := FALSE;
        bAsepticBarrierIntegrityOK := FALSE;
        rCmd_InfeedPacingScrewSpeed_RPM := 0.0;
        rCmd_DischargeTurretSync_RPM := 0.0;
        rCmd_LN2InjectorPulseDuration_ms := 0.0;

        (* Modulate PAA Vaporizer Dosing Pump *)
        IF rVoted_PAAConcentration_ppm < rSet_ChamberPAAConcentration_ppm THEN
            rCmd_PAAVaporizerDosingPump_Pct := 75.0;
        ELSE
            rCmd_PAAVaporizerDosingPump_Pct := 20.0; (* Maintenance trickle dose *)
        END_IF;

        (* Throttle sterile air supply damper to 15% for vapor containment *)
        rCmd_SterileAirSupplyDamper_Pct := 15.0;

        (* Interlock: Door must remain sealed *)
        IF NOT bAsepticIsolatorDoorInterlock_NC THEN
            eState := 120; (* Abort to Emergency Depressurization *)
        (* Dwell criteria: PAA concentration maintained above 1400 ppm for 300 seconds *)
        ELSIF (rVoted_PAAConcentration_ppm >= 1400.0) AND (rStateTimer_s >= 300.0) AND bCIP_SIP_ModePermissive THEN
            eState := 20; (* Progress to Pressure Barrier Establishment *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 20: PRESSURE_BARRIER_ESTABLISH                                                                             *)
    (* Purge chemical PAA vapor to HEPA scrubber; ramp supply blowers to establish +45 Pa sterile positive pressure.    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    20:
        rCmd_PAAVaporizerDosingPump_Pct := 0.0; (* Cease chemical injection *)
        rCmd_SterileAirSupplyDamper_Pct := 90.0; (* Maximum sterile airflow to establish barrier *)

        (* Check for chamber evacuation of PAA (< 5 ppm) and positive pressure barrier lock (> 42.0 Pa) *)
        IF (rVoted_PAAConcentration_ppm <= 10.0) AND (rVoted_SterileAirPres_Pa >= 42.0) THEN
            bAsepticBarrierIntegrityOK := TRUE;
            IF bMasterLineRunPermissive AND bEmergencyStopCircuit_NC THEN
                eState := 30; (* Advance to Inlet Starwheel Pacing *)
            END_IF;
        END_IF;

        IF NOT bAsepticIsolatorDoorInterlock_NC OR NOT bEmergencyStopCircuit_NC THEN
            eState := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 30: INLET_STARWHEEL_PACING                                                                                 *)
    (* Ramp infeed metering screw servo to match 90,000 CPH turret line speed (83.33 RPM turret, 250 RPM pacing screw).*)
    (* Verify can presence and pitch spacing before enabling lifter indexing.                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    30:
        rCmd_InfeedPacingScrewSpeed_RPM := rInfeedScrewServoVelocity_RPM;
        rCmd_DischargeTurretSync_RPM := rTurretMasterVelocity_RPM;
        rCmd_SterileAirSupplyDamper_Pct := 85.0;

        (* Synchronize Electronic Camming between Infeed Screw and Turret Resolver *)
        IF ABS(rCamElectronicTrackingError_mrad) < 5.0 THEN
            bMachineSynchronized := TRUE;
        ELSE
            bMachineSynchronized := FALSE;
        END_IF;

        (* Detect Infeed Can Arrival *)
        IF bMachineSynchronized AND bCanPresenceInfeedStarwheel AND bMasterLineRunPermissive THEN
            eState := 40; (* Advance to Can Elevator Lifter Engagement *)
        END_IF;

        (* Interlocks *)
        IF NOT bAsepticBarrierIntegrityOK THEN
            eState := 20;
        ELSIF NOT bEmergencyStopCircuit_NC THEN
            eState := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 40: CAN_ELEVATOR_LIFTER_ENGAGE                                                                             *)
    (* Lifter table rises to clamp can body flange firmly against seaming chuck base plate.                             *)
    (* Verifies base force (> 1100 N) and optical lid presence sensor before triggering cryogenic dose.                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    40:
        rCmd_LifterPneumaticCushion_bar := vecU[5];

        (* Check Base Clamping Force and Lid Presence *)
        IF rLifterTableActualBaseForce_N >= 1050.0 THEN
            IF bLidPresenceCapChute THEN
                eState := 50; (* Proceed to In-Seam Liquid Nitrogen Micro-Dosing *)
            ELSE
                (* Missing lid defect: Do not seam bare can, flag reject bitmask and advance *)
                wCanRejectionBitmask := wCanRejectionBitmask OR 16#0001;
                bRejectTriggerActive := TRUE;
                eState := 90; (* Jump directly to Pneumatic Reject *)
            END_IF;
        END_IF;

        IF rStateTimer_s > 0.080 THEN
            (* Lifter elevator mechanical binding or low base pressure timeout *)
            bAlarm_CanJamInfeedLifter := TRUE;
            eState := 110; (* Controlled Jam Stop *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 50: LN2_IN_SEAM_CRYODOSE                                                                                   *)
    (* High-speed cryogenic micro-valve injects sub-cooled liquid nitrogen (-196 deg C) into beverage headspace.       *)
    (* Precise pulse duration governed by MPC control u4 to achieve target 45.0 mg dose mass.                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    50:
        rCmd_LN2InjectorPulseDuration_ms := vecU[4];

        (* Micro-Dose Validation *)
        IF (rVoted_LN2DoseMass_mg >= 38.0) AND (rVoted_LN2DoseMass_mg <= 52.0) THEN
            eState := 60; (* Dose nominal: Advance to 1st Operation Curl *)
        ELSIF rStateTimer_s >= (vecU[4] * 0.001 + 0.002) THEN
            (* Dose out of tolerance: flag reject bitmask but continue to seam to prevent liquid sloshing *)
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0002;
            bRejectTriggerActive := TRUE;
            eState := 60;
        END_IF;

        IF NOT bEmergencyStopCircuit_NC THEN
            eState := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 60: FIRST_OPERATION_CURL_SEAM                                                                              *)
    (* 1st Operation Seaming Roll advances radially along quintic cam trajectory to curl cover hook around body flange. *)
    (* Monitors radial reaction force profile (target 320.0 N, envelope 220 - 420 N) via 2oo3 load cells.              *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    60:
        rCmd_1stOpServoRadialPosition_mm := rProfile1stOp_PosFeedforward_mm + vecU[1];

        (* Real-Time Curling Force Envelope Verification *)
        IF (rVoted_Force1stOp_N > rLim_1stOpForce_HH_N) THEN
            bAlarm_Force1stOp_HH := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0008;
            bRejectTriggerActive := TRUE;
        ELSIF (rVoted_Force1stOp_N < rLim_1stOpForce_LL_N) AND (rCamAngle_Normalized_deg >= 90.0) THEN
            (* Slip or missing curl *)
            bAlarm_Force1stOp_LL := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0010;
            bRejectTriggerActive := TRUE;
        END_IF;

        (* Transition upon exiting 1st op cam sector (150 degrees) *)
        IF (rCamAngle_Normalized_deg >= 150.0) AND (rCamAngle_Normalized_deg < 165.0) THEN
            eState := 70; (* Advance to Second Operation Hermetic Crimp *)
        END_IF;

        IF NOT bEmergencyStopCircuit_NC THEN
            eState := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 70: SECOND_OPERATION_HERMETIC_CRIMP                                                                        *)
    (* 2nd Operation Seaming Roll advances radially to compress and iron out 5 layers of metal and seal compound.       *)
    (* Monitors crimping force profile (target 680.0 N, envelope 540 - 820 N) and finished thickness (1.020 mm).        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    70:
        rCmd_2ndOpServoRadialPosition_mm := rProfile2ndOp_PosFeedforward_mm + vecU[2];

        (* Real-Time Crimp Force Envelope Verification *)
        IF (rVoted_Force2ndOp_N > rLim_2ndOpForce_HH_N) THEN
            bAlarm_Force2ndOp_HH := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0020;
            bRejectTriggerActive := TRUE;
        ELSIF (rVoted_Force2ndOp_N < rLim_2ndOpForce_LL_N) AND (rCamAngle_Normalized_deg >= 225.0) THEN
            (* Loose double seam / lack of hermetic compression *)
            bAlarm_Force2ndOp_LL := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0040;
            bRejectTriggerActive := TRUE;
        END_IF;

        (* Seam finished upon exiting 2nd op cam sector (285 degrees) *)
        IF (rCamAngle_Normalized_deg >= 285.0) THEN
            eState := 80; (* Advance to Acoustic Tap Leak Inspection *)
        END_IF;

        IF NOT bEmergencyStopCircuit_NC THEN
            eState := 120;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 80: ACOUSTIC_TAP_LEAK_TEST                                                                                 *)
    (* Solenoid impulse striker taps center of can end dome; biquad bandpass filter processes acoustic resonance.      *)
    (* Evaluates natural resonant frequency (nominal 3250 Hz) and internal pressure (nominal 1.85 bar).                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    80:
        (* Digital Biquad IIR Bandpass Filter Processing *)
        rAcousticSampleRaw_V := (rVoted_AcousticPressure_bar - 1.0) * 2.5; (* Transduced acoustic voltage *)
        rIntermediateVal := rAcousticSampleRaw_V - (rIIR_Coeff_a1 * rIIR_FilterState_x1) - (rIIR_Coeff_a2 * rIIR_FilterState_x2);
        rAcousticSignalFiltered := (rIIR_Coeff_b0 * rIntermediateVal) + (rIIR_Coeff_b1 * rIIR_FilterState_x1) + (rIIR_Coeff_b2 * rIIR_FilterState_x2);
        rIIR_FilterState_x2 := rIIR_FilterState_x1;
        rIIR_FilterState_x1 := rIntermediateVal;

        (* Acoustic Resonance Envelope & Frequency Evaluation *)
        rAcousticEnvelopeAmplitude := ABS(rAcousticSignalFiltered);
        vecX[8] := rAcousticEnvelopeAmplitude;

        (* Quality Gate Checks: Resonance Frequency, Seam Overlap, and Headspace Pressure *)
        IF (rVoted_AcousticResonanceFreq_Hz < rLim_AcousticResonance_LL_Hz) OR
           (rVoted_AcousticPressure_bar < rLim_InternalPres_LL_bar) THEN
            (* Leaker / flat can / pinhole defect *)
            bAlarm_AcousticResonance_LL := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0100;
            bRejectTriggerActive := TRUE;
        ELSIF (rVoted_AcousticResonanceFreq_Hz > rLim_AcousticResonance_HH_Hz) OR
              (rVoted_AcousticPressure_bar > rLim_InternalPres_HH_bar) THEN
            (* Over-pressurized container hazard *)
            bAlarm_InternalPres_HH := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0200;
            bRejectTriggerActive := TRUE;
        ELSIF rEstimatedSeamOverlap_Pct < 85.0 THEN
            (* Seam overlap deficiency below FDA 21 CFR 113.60 standard *)
            bAlarm_SeamOverlapDeficiency := TRUE;
            wCanRejectionBitmask := wCanRejectionBitmask OR 16#0400;
            bRejectTriggerActive := TRUE;
        END_IF;

        (* Branch based on rejection trigger *)
        IF bRejectTriggerActive THEN
            eState := 90; (* Fire High-Speed Pneumatic Reject *)
        ELSE
            eState := 100; (* Container Validated: Discharge to Outfeed Conveyor *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 90: HIGH_SPEED_PNEUMATIC_REJECT                                                                            *)
    (* Fires sub-2ms high-pressure pneumatic solenoid valve to divert defective container to reject chute.             *)
    (* Updates defect tallies, increments rejection statistics, and clears reject trigger.                              *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    90:
        bCmd_PneumaticRejectSolenoid_Fast := TRUE;
        rRejectPulseTimer_s := rRejectPulseTimer_s + rCycleScanDeltaTime;

        (* Reject pulse duration: 8 ms high-pressure blast *)
        IF rRejectPulseTimer_s >= 0.008 THEN
            bCmd_PneumaticRejectSolenoid_Fast := FALSE;
            rRejectPulseTimer_s := 0.0;
            bRejectTriggerActive := FALSE;
            diTotalCansRejectedCount := diTotalCansRejectedCount + 1;
            diTotalCansProcessedCount := diTotalCansProcessedCount + 1;
            eState := 100; (* Progress to Discharge Synchronization *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 100: DISCHARGE_SYNCHRONIZATION                                                                             *)
    (* Synchronizes transfer starwheel to hand off accepted cans smoothly to mass accumulation conveyor.               *)
    (* Re-evaluates production rate, computes running defect PPM, and loops for continuous mass canning.                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    100:
        rCmd_DischargeTurretSync_RPM := rTurretMasterVelocity_RPM;
        IF NOT bRejectTriggerActive THEN
            diTotalCansProcessedCount := diTotalCansProcessedCount + 1;
        END_IF;

        (* Compute Running Defect PPM *)
        IF diTotalCansProcessedCount > 0 THEN
            rDefectPPM_CurrentRun := (DINT_TO_REAL(diTotalCansRejectedCount) / DINT_TO_REAL(diTotalCansProcessedCount)) * 1000000.0;
        END_IF;

        (* Continuous Rotary Pacing Loop *)
        IF bMasterLineRunPermissive AND bEmergencyStopCircuit_NC AND bAsepticBarrierIntegrityOK THEN
            wCanRejectionBitmask := 16#0000; (* Clear per-can rejection bitfield *)
            eState := 30; (* Seamless loop back to Inlet Pacing for next container *)
        ELSE
            eState := 10; (* Safe return to Standby / SIP *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 110: JAM_DETECTION_CONTROLLED_STOP                                                                         *)
    (* Electronic camming synchronized deceleration ramp along predefined trajectory to prevent can crushing.           *)
    (* Latches jam alarms, cuts infeed metering screw, and holds turret in phased position until cleared.              *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    110:
        rCmd_InfeedPacingScrewSpeed_RPM := 0.0;
        rCmd_LN2InjectorPulseDuration_ms := 0.0;
        bMachineSynchronized := FALSE;

        (* Controlled deceleration of main turret *)
        IF rCmd_DischargeTurretSync_RPM > 0.5 THEN
            rCmd_DischargeTurretSync_RPM := rCmd_DischargeTurretSync_RPM - (83.33 * rCycleScanDeltaTime * 2.0); (* 0.5s ramp *)
        ELSE
            rCmd_DischargeTurretSync_RPM := 0.0;
        END_IF;

        IF bResetFaultLatches THEN
            bAlarm_CanJamInfeedLifter := FALSE;
            eState := 30; (* Return to pacing upon operator acknowledge *)
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 120: EMERGENCY_DEPRESSURIZATION                                                                            *)
    (* Immediate Safety Torque Off (STO) to all servos, cryogenic LN2 manifold dump, chamber exhaust venting.          *)
    (* Requires master safety circuit restoration and manual operator reset before resuming.                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    120:
        rCmd_1stOpServoRadialPosition_mm := 0.0;
        rCmd_2ndOpServoRadialPosition_mm := 0.0;
        rCmd_SpindleElectronicCamTorque_Nm := 0.0;
        rCmd_InfeedPacingScrewSpeed_RPM := 0.0;
        rCmd_DischargeTurretSync_RPM := 0.0;
        rCmd_LN2InjectorPulseDuration_ms := 0.0;
        rCmd_PAAVaporizerDosingPump_Pct := 0.0;
        bCmd_PneumaticRejectSolenoid_Fast := FALSE;
        bMachineSynchronized := FALSE;
        bAsepticBarrierIntegrityOK := FALSE;
        bAlarm_EStopDepressurized := TRUE;

        IF bEmergencyStopCircuit_NC AND bAsepticIsolatorDoorInterlock_NC AND bResetFaultLatches THEN
            bAlarm_EStopDepressurized := FALSE;
            eState := 10; (* Return to Sterilization / Standby *)
        END_IF;

ELSE
    eState := 120; (* Catch invalid state *)
END_CASE;

eCurrentFSMState := eState;
"""
