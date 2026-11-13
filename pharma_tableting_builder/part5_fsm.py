# pharma_tableting_builder/part5_fsm.py

def get_part5():
    return """(* === PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE === *)

rStateTimer_s := rStateTimer_s + T_CYCLE_SEC;

(* Global Safety Interlock: Immediate Drop to Safe State on E-Stop or Critical Trip *)
IF (NOT bEmergencyStop) OR bTripLatched_EmergencyStop OR bTripLatched_MainForce_HH THEN
    nOperationalState := 14; (* Emergency Overpressure / E-Stop Abort *)
END_IF;

CASE nOperationalState OF

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 0: SYSTEM OFFLINE & IDLE STANDBY                                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    0:
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bBatchDrainingActive := FALSE;
        bBatchDrainComplete := FALSE;
        bWarmupComplete := FALSE;
        bDryBlendEquilibrated := FALSE;
        bNucleationEstablished := FALSE;
        bMoistureStabilized := FALSE;
        bFeederShoeFilled := FALSE;
        bTurretSpeedSynchronized := FALSE;
        bContinuousTabletingSteady := FALSE;
        
        (* Inhibit All Actuators in Idle *)
        rFeederMotorSpeedCommand_Hz := 0.0;
        rBinderPumpFlowCommand_gpmin := 0.0;
        rGranulatorScrewSpeedCommand_rpm := 0.0;
        rFluidBedHeaterDuty_pct := 0.0;
        rFluidBedAirFlowVelocity_pct := 0.0;
        rTurretDriveSpeedCommand_rpm := 0.0;
        rFeederShoePaddleSpeedCommand_rpm := 0.0;
        bHighSpeedRejectGateSolenoidCmd := FALSE;

        IF bSystemEnable AND bEmergencyStop AND bProductionRunCmd THEN
            nOperationalState := 1; (* Advance to Recipe Handshake *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 1: RECIPE PARAMETER VALIDATION & SCADA HANDSHAKE                                    *)
    (* ----------------------------------------------------------------------------------------- *)
    1:
        bSystemReady := FALSE;
        bProductionActive := FALSE;

        (* Range Verification of Validated Processing Parameters *)
        IF (rRecipeTargetFeederFlow_kgh >= 5.0) AND (rRecipeTargetFeederFlow_kgh <= 50.0) AND
           (rRecipeTargetLiquidSolidRatio_pct >= 6.0) AND (rRecipeTargetLiquidSolidRatio_pct <= 16.0) AND
           (rRecipeTargetMoistureLOD_pct >= 1.0) AND (rRecipeTargetMoistureLOD_pct <= 3.0) AND
           (rRecipeTargetFluidBedTemp_degC >= 40.0) AND (rRecipeTargetFluidBedTemp_degC <= 70.0) AND
           (rRecipeTargetTurretSpeed_rpm >= 20.0) AND (rRecipeTargetTurretSpeed_rpm <= 105.0) AND
           (rRecipeTargetMainCompForce_kN >= 15.0) AND (rRecipeTargetMainCompForce_kN <= 50.0) THEN
            
            IF rStateTimer_s >= 0.500 THEN
                nOperationalState := 2; (* Advance to Instrumentation TMR Pre-Check *)
                rStateTimer_s := 0.0;
            END_IF;
        ELSE
            (* Invalidate Recipe Handshake *)
            bSystemReady := FALSE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 2: PROCESS INSTRUMENTATION & 2oo3 TMR PRE-CHECK                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    2:
        bSystemReady := FALSE;

        (* Verify that all critical primary sensor channels have at least 2 valid probes *)
        IF (nFeeder_VotingMode >= 2) AND
           (nMoist_VotingMode >= 2) AND
           (nPreComp_VotingMode >= 2) AND
           (nMainComp_VotingMode >= 2) AND
           (nTurret_VotingMode >= 2) AND
           (nFBDiff_VotingMode >= 2) THEN
            
            IF rStateTimer_s >= 1.500 THEN
                nOperationalState := 3; (* Advance to Fluid Bed Warmup *)
                rStateTimer_s := 0.0;
            END_IF;
        ELSE
            (* Sensor redundancy degraded beyond allowable startup permissive *)
            bSystemReady := FALSE;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 3: CONTINUOUS FLUID BED DRYER AIRFLOW & THERMAL WARMUP                              *)
    (* ----------------------------------------------------------------------------------------- *)
    3:
        bSystemReady := FALSE;
        
        (* Ramp fluidization air velocity and supply air heating thyristor *)
        rFluidBedAirFlowVelocity_pct := 55.0;
        rFluidBedHeaterDuty_pct := 65.0;

        (* Check for temperature equilibration within +- 2.0 deg C of recipe setpoint *)
        IF (ABS(rFluidBedInletAirTemp_degC - rRecipeTargetFluidBedTemp_degC) <= 2.0) AND
           (rVotedFluidBedDiffPress_mbar >= 6.0) THEN
            bWarmupComplete := TRUE;
            IF rStateTimer_s >= 5.000 THEN
                nOperationalState := 4; (* Advance to Twin-Screw Dry Feed Pre-Blend *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 4: TWIN-SCREW GRANULATOR DRY RUN PRE-BLEND                                          *)
    (* ----------------------------------------------------------------------------------------- *)
    4:
        bSystemReady := FALSE;

        (* Start granulator screw drive at recipe speed *)
        rGranulatorScrewSpeedCommand_rpm := rRecipeTargetScrewSpeed_rpm;
        
        (* Engage loss-in-weight dry powder feeder at target rate *)
        rFeederMotorSpeedCommand_Hz := u_ref[1];

        (* Verify screw drive torque is within normal empty/dry powder limits (< 30 Nm) *)
        IF (rGranulatorScrewTorque_Nm < 30.0) AND 
           (rVotedFeederFlow_kgh >= (rRecipeTargetFeederFlow_kgh * 0.85)) THEN
            bDryBlendEquilibrated := TRUE;
            IF rStateTimer_s >= 8.000 THEN
                nOperationalState := 5; (* Advance to Liquid Binder Cut-In *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 5: LIQUID BINDER CUT-IN & GRANULE NUCLEATION                                        *)
    (* ----------------------------------------------------------------------------------------- *)
    5:
        bSystemReady := FALSE;

        (* Activate peristaltic micro-pump dosing cascade *)
        rBinderPumpFlowCommand_gpmin := u_ref[2];

        (* Verify L/S ratio within target range and granulator torque rise indicates wet massing *)
        IF (ABS(rObservedLiquidSolidRatio_pct - rRecipeTargetLiquidSolidRatio_pct) <= 1.0) AND
           (rGranulatorScrewTorque_Nm >= 15.0) AND (rGranulatorScrewTorque_Nm <= 45.0) THEN
            bNucleationEstablished := TRUE;
            IF rStateTimer_s >= 10.000 THEN
                nOperationalState := 6; (* Advance to Continuous Granule Transport & Drying *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 6: CONTINUOUS GRANULE TRANSPORT & DRYING                                            *)
    (* ----------------------------------------------------------------------------------------- *)
    6:
        bSystemReady := FALSE;

        (* Granule mass enters fluid bed dryer cells; adjust air velocity to fluidized regime *)
        rFluidBedAirFlowVelocity_pct := 65.0;
        
        (* Monitor bed pressure drop reflecting bed holdup *)
        IF (rVotedFluidBedDiffPress_mbar >= 10.0) AND (rVotedFluidBedDiffPress_mbar <= 22.0) THEN
            IF rStateTimer_s >= 15.000 THEN
                nOperationalState := 7; (* Advance to Microwave LOD Moisture Equilibration *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 7: MICROWAVE RESONANCE LOD MOISTURE EQUILIBRATION                                   *)
    (* ----------------------------------------------------------------------------------------- *)
    7:
        bSystemReady := FALSE;

        (* Closed-loop moisture tracking: must remain within release tolerance for 10 s *)
        IF ABS(rVotedMoistureLOD_pct - rRecipeTargetMoistureLOD_pct) <= 0.25 THEN
            bMoistureStabilized := TRUE;
            IF rStateTimer_s >= 10.000 THEN
                nOperationalState := 8; (* Advance to Rotary Press Feeder Shoe Fill *)
                rStateTimer_s := 0.0;
            END_IF;
        ELSE
            rStateTimer_s := 0.0; (* Reset dwell timer if moisture drifts out of release window *)
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 8: ROTARY TABLET PRESS FEEDER SHOE FILL & DIE CHARGING                              *)
    (* ----------------------------------------------------------------------------------------- *)
    8:
        bSystemReady := FALSE;

        (* Start force feeder dual paddle wheels to fluidize granule bed over die table *)
        rFeederShoePaddleSpeedCommand_rpm := rRecipeTargetTurretSpeed_rpm * 0.75;

        (* Lower punch dosing cam servo positioned to recipe target *)
        rLowerPunchDosingCamCommand_mm := u_ref[8];

        IF rStateTimer_s >= 6.000 THEN
            bFeederShoeFilled := TRUE;
            nOperationalState := 9; (* Advance to Turret Acceleration *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 9: ROTARY TURRET SPEED SYNCHRONIZATION & ACCELERATION                               *)
    (* ----------------------------------------------------------------------------------------- *)
    9:
        bSystemReady := FALSE;

        (* Accelerate turret drive servo toward recipe setpoint *)
        rTurretDriveSpeedCommand_rpm := rRecipeTargetTurretSpeed_rpm;
        rFeederShoePaddleSpeedCommand_rpm := rRecipeTargetTurretSpeed_rpm * 0.85;

        (* Check speed tracking error *)
        IF ABS(rVotedTurretSpeed_rpm - rRecipeTargetTurretSpeed_rpm) <= 0.80 THEN
            bTurretSpeedSynchronized := TRUE;
            IF rStateTimer_s >= 4.000 THEN
                nOperationalState := 10; (* Advance to Continuous Commercial Tableting *)
                rStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 10: ACTIVE CONTINUOUS DUAL-COMPRESSION TABLETING (250,000 TABLETS/HOUR)            *)
    (* ----------------------------------------------------------------------------------------- *)
    10:
        bSystemReady := TRUE;
        bProductionActive := TRUE;
        bContinuousTabletingSteady := TRUE;

        (* Full Closed-Loop MPC Regulation Active for Both Wet Granulation and Tableting *)
        rFeederMotorSpeedCommand_Hz := u_ctrl[1];
        rBinderPumpFlowCommand_gpmin := u_ctrl[2];
        rGranulatorScrewSpeedCommand_rpm := u_ctrl[3];
        rFluidBedHeaterDuty_pct := u_ctrl[4];
        rFluidBedAirFlowVelocity_pct := u_ctrl[5];
        rTurretDriveSpeedCommand_rpm := u_ctrl[6];
        rFeederShoePaddleSpeedCommand_rpm := u_ctrl[7];
        rLowerPunchDosingCamCommand_mm := u_ctrl[8];

        (* Check for Batch Drain Request *)
        IF bBatchDrainModeCmd THEN
            nOperationalState := 13; (* Transition to Batch Drain Runout *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 11: SINGLE-TABLET DYNAMIC REJECT MONITORING                                         *)
    (* ----------------------------------------------------------------------------------------- *)
    11:
        (* Sub-state transition handler: returns directly to state 10 after station flagging *)
        nOperationalState := 10;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 12: AUTOMATED PUNCH LUBRICATION INJECTION CYCLE                                     *)
    (* ----------------------------------------------------------------------------------------- *)
    12:
        (* Automated micro-spray pulse of magnesium stearate on punch barrels *)
        IF rTabletEjectionForce_N > 220.0 THEN
            rPunchLubricationDosingFlow_mgps := 15.0;
        ELSE
            rPunchLubricationDosingFlow_mgps := 8.0;
        END_IF;
        
        IF rStateTimer_s >= 2.000 THEN
            nOperationalState := 10; (* Return to Active Tableting *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 13: CONTROLLED PRODUCTION BATCH DRAIN & RUNOUT                                      *)
    (* ----------------------------------------------------------------------------------------- *)
    13:
        bProductionActive := FALSE;
        bBatchDrainingActive := TRUE;

        (* Step 1: Immediately cut liquid binder dosing *)
        rBinderPumpFlowCommand_gpmin := 0.0;

        (* Step 2: Inhibit dry powder feeder *)
        rFeederMotorSpeedCommand_Hz := 0.0;

        (* Step 3: Run granulator screws and fluid bed to clear lingering product *)
        rGranulatorScrewSpeedCommand_rpm := 300.0;
        rFluidBedAirFlowVelocity_pct := 50.0;

        (* Step 4: After 20 seconds, runout tablet press at reduced speed *)
        IF rStateTimer_s >= 20.000 THEN
            rTurretDriveSpeedCommand_rpm := 25.0;
            rFeederShoePaddleSpeedCommand_rpm := 20.0;
        END_IF;

        (* Step 5: After 45 seconds, complete shutdown *)
        IF rStateTimer_s >= 45.000 THEN
            rGranulatorScrewSpeedCommand_rpm := 0.0;
            rFluidBedHeaterDuty_pct := 0.0;
            rFluidBedAirFlowVelocity_pct := 0.0;
            rTurretDriveSpeedCommand_rpm := 0.0;
            rFeederShoePaddleSpeedCommand_rpm := 0.0;
            bBatchDrainComplete := TRUE;
            bBatchDrainingActive := FALSE;
            nOperationalState := 0; (* Return to Idle Standby *)
            rStateTimer_s := 0.0;
        END_IF;

    (* ----------------------------------------------------------------------------------------- *)
    (* STAGE 14: EMERGENCY OVERPRESSURE / DIE JAM IMMEDIATE ABORT                                *)
    (* ----------------------------------------------------------------------------------------- *)
    14:
        bSystemReady := FALSE;
        bProductionActive := FALSE;
        bEmergencyTripped := TRUE;

        (* Instantaneous Actuator Retraction (< 2 ms) *)
        rTurretDriveSpeedCommand_rpm := 0.0;
        rFeederShoePaddleSpeedCommand_rpm := 0.0;
        rGranulatorScrewSpeedCommand_rpm := 0.0;
        rBinderPumpFlowCommand_gpmin := 0.0;
        rFeederMotorSpeedCommand_Hz := 0.0;
        rFluidBedHeaterDuty_pct := 0.0;
        rFluidBedAirFlowVelocity_pct := 0.0;

        (* Retract lower punch dosing cam to relieve tooling strain *)
        rLowerPunchDosingCamCommand_mm := 0.50;

        (* Latch emergency stop trip *)
        bTripLatched_EmergencyStop := TRUE;

        (* Operator Reset Permissive *)
        IF bAlarmReset AND bEmergencyStop AND (NOT bTripLatched_MainForce_HH) THEN
            bTripLatched_EmergencyStop := FALSE;
            bEmergencyTripped := FALSE;
            nOperationalState := 0; (* Return to Standby *)
            rStateTimer_s := 0.0;
        END_IF;

    ELSE
        nOperationalState := 0;
END_CASE;
"""
