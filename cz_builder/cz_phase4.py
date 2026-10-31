# cz_builder/cz_phase4.py

def get_phase4():
    return """(* === PHASE 4: MULTI-STAGE CASE FINITE STATE MACHINE === *)
(* 12 deterministic operational stages managing vacuum pump-down, argon purge, polysilicon  *)
(* melting, dash necking, crown expansion, steady body pull, tail-off, and ingot unload.   *)

CASE iState OF

    0: (* STAGE 0: FURNACE VACUUM PUMP-DOWN & GRAPHITE OUTGASSING *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;
        bDislocationFreeStructure := FALSE;

        (* Safe parked actuator setpoints *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 0.0;
        rTargetLowerPowerInternal := 0.0;
        rTargetBottomPowerInternal := 0.0;
        rTargetSeedRotInternal := 0.0;
        rTargetCrucibleRotInternal := 0.0;
        rTargetArgonFlowInternal := 0.0;
        rTargetThrottleInternal := 100.0; (* 100% wide-open vacuum throttle valve *)

        (* Reset state machine timers *)
        tPumpDownTimer(IN := bVacuumPumpSkidReady, PT := T#300S);
        tArgonPurgeTimer(IN := FALSE);
        tPolyMeltingTimer(IN := FALSE);
        tMeltStabilizeTimer(IN := FALSE);
        tDashNeckingTimer(IN := FALSE);
        tCrownGrowthTimer(IN := FALSE);
        tBodyStabilizeTimer(IN := FALSE);
        tTailOffTimer(IN := FALSE);
        tIngotLiftTimer(IN := FALSE);
        tCoolDownTimer(IN := FALSE);
        tFaultHoldTimer(IN := FALSE);

        (* Advance to Argon Purge when vacuum is established *)
        IF bMasterEnable AND NOT bSystemTripped AND (rVotedChamberPress_mbar < 0.05) AND tPumpDownTimer.Q THEN
            tPumpDownTimer(IN := FALSE);
            iState := 1; (* Advance to Argon Purge Flush *)
        END_IF;

    1: (* STAGE 1: ARGON GAS PURGE FLUSH & PRESSURE REGULATION (20.0 mbar) *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        (* Establish 100 slpm Argon flow and throttle valve regulation *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 0.0;
        rTargetLowerPowerInternal := 0.0;
        rTargetBottomPowerInternal := 0.0;
        rTargetSeedRotInternal := 0.0;
        rTargetCrucibleRotInternal := 0.0;
        rTargetArgonFlowInternal := 100.0;
        rTargetThrottleInternal := 45.0;

        tArgonPurgeTimer(IN := (rVotedChamberPress_mbar > 15.0) AND (rVotedChamberPress_mbar < 25.0), PT := T#180S);
        IF tArgonPurgeTimer.Q AND (ABS(rVotedChamberPress_mbar - 20.0) < 2.0) AND (rActualArgonInletFlow_slpm > 85.0) THEN
            tArgonPurgeTimer(IN := FALSE);
            iState := 2; (* Advance to Polysilicon Melting & Doping *)
        END_IF;

    2: (* STAGE 2: POLYSILICON MELTING & DOPANT ALLOYING (1,480 DEG C) *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        (* Multi-zone heater ramp up: Upper 120 kW, Lower 95 kW, Bottom 55 kW *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 120.0;
        rTargetLowerPowerInternal := 95.0;
        rTargetBottomPowerInternal := 55.0;
        rTargetSeedRotInternal := 0.0;
        rTargetCrucibleRotInternal := 2.5; (* Slow spin to prevent thermal stress on quartz *)
        rTargetArgonFlowInternal := 100.0;
        rTargetThrottleInternal := 45.0;

        tPolyMeltingTimer(IN := (rVotedCrucibleTemp_DegC > 1450.0), PT := T#600S);
        IF tPolyMeltingTimer.Q AND (rVotedCrucibleTemp_DegC >= 1510.0) AND (rVotedMeltTemp_DegC >= 1435.0) THEN
            tPolyMeltingTimer(IN := FALSE);
            iState := 3; (* Advance to Melt Stabilization *)
        END_IF;

    3: (* STAGE 3: MELT STABILIZATION, CONVECTION DAMPING & ZERO TARE (1,420 DEG C) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := FALSE;

        (* Lower heater powers to soak setpoints *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 100.0;
        rTargetLowerPowerInternal := 80.0;
        rTargetBottomPowerInternal := 45.0;
        rTargetSeedRotInternal := 8.0;
        rTargetCrucibleRotInternal := 5.0; (* Suppress Marangoni thermocapillary vortices *)
        rTargetArgonFlowInternal := 95.0;
        rTargetThrottleInternal := 45.0;

        (* Zero tare length integrators *)
        rNeckLength_mm := 0.0;
        rCrownLength_mm := 0.0;
        rBodyLength_mm := 0.0;
        rTailLength_mm := 0.0;

        tMeltStabilizeTimer(IN := (ABS(rVotedMeltTemp_DegC - 1420.0) < 3.0), PT := T#120S);
        IF tMeltStabilizeTimer.Q AND (ABS(rVotedMeltLevel_mm) < 0.5) THEN
            tMeltStabilizeTimer(IN := FALSE);
            iState := 4; (* Advance to Seed Dip & Dash Necking *)
        END_IF;

    4: (* STAGE 4: SEED CRYSTAL DIP & DASH NECKING (4.5 - 5.5 mm/min, 3.5 mm DIA) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := FALSE;

        (* High pull velocity to force dislocation line propagation to free surface *)
        rTargetPullSpeedInternal := 5.20;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 102.0;
        rTargetLowerPowerInternal := 80.0;
        rTargetBottomPowerInternal := 44.0;
        rTargetSeedRotInternal := 18.0;
        rTargetCrucibleRotInternal := -5.0;
        rTargetArgonFlowInternal := 90.0;
        rTargetThrottleInternal := 45.0;

        (* Integrate pulled neck length *)
        rNeckLength_mm := rNeckLength_mm + ((rActualPullSpeed_mmpm / 60.0) * rCycleTime_sec);

        (* Confirm dislocation elimination if neck > 220 mm and diameter 3.0 to 4.0 mm *)
        IF (rNeckLength_mm >= 220.0) AND (rVotedMeniscusDiam_mm >= 2.8) AND (rVotedMeniscusDiam_mm <= 4.2) THEN
            bDislocationFreeStructure := TRUE;
        END_IF;

        IF (rNeckLength_mm >= 250.0) AND bDislocationFreeStructure THEN
            iState := 5; (* Advance to Crown Expansion Shoulder Growth *)
        END_IF;

    5: (* STAGE 5: CROWN EXPANSION SHOULDER CONE GROWTH (0.7 mm/min, CONE TO 300 mm) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := FALSE;

        (* Decelerate pull speed and cool melt slightly to expand growth angle *)
        rTargetPullSpeedInternal := 0.72;
        rTargetCrucibleLiftInternal := 0.05;
        rTargetUpperPowerInternal := 97.0;
        rTargetLowerPowerInternal := 77.0;
        rTargetBottomPowerInternal := 42.0;
        rTargetSeedRotInternal := 16.0;
        rTargetCrucibleRotInternal := -6.0;
        rTargetArgonFlowInternal := 95.0;
        rTargetThrottleInternal := 45.0;

        (* Integrate crown cone length *)
        rCrownLength_mm := rCrownLength_mm + ((rActualPullSpeed_mmpm / 60.0) * rCycleTime_sec);

        (* Transition to body when diameter reaches shoulder limit *)
        IF rVotedMeniscusDiam_mm >= 298.5 THEN
            iState := 6; (* Advance to Body Diameter Stabilization *)
        END_IF;

    6: (* STAGE 6: BODY SHOULDER ROLL-OFF & DIAMETER STABILIZATION (300.0 mm LOCK) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := TRUE;

        (* Roll shoulder over: increase pull speed to steady-state nominal *)
        rTargetPullSpeedInternal := 1.10;
        rTargetCrucibleLiftInternal := rMeltLevelDropVelocity_mmpm + (0.15 * rCrucibleLiftError_mm);
        rTargetUpperPowerInternal := 98.5;
        rTargetLowerPowerInternal := 78.5;
        rTargetBottomPowerInternal := 43.0;
        rTargetSeedRotInternal := 15.0;
        rTargetCrucibleRotInternal := -6.5;
        rTargetArgonFlowInternal := 100.0;
        rTargetThrottleInternal := 45.0;

        tBodyStabilizeTimer(IN := (ABS(rVotedMeniscusDiam_mm - 300.0) < 0.6), PT := T#60S);
        IF tBodyStabilizeTimer.Q AND (ABS(rVotedMeniscusDiam_mm - 300.0) < 0.3) THEN
            tBodyStabilizeTimer(IN := FALSE);
            iState := 7; (* Advance to Steady-State Body Pull *)
        END_IF;

    7: (* STAGE 7: STEADY-STATE CYLINDRICAL BODY GROWTH (1,800 mm, 300 kg INGOT) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := TRUE;

        (* Active Receding-Horizon MPC closed-loop regulation *)
        rTargetPullSpeedInternal := aControl_u[1];
        rTargetCrucibleLiftInternal := aControl_u[2];
        rTargetUpperPowerInternal := aControl_u[3];
        rTargetLowerPowerInternal := aControl_u[4];
        rTargetBottomPowerInternal := aControl_u[5];
        rTargetSeedRotInternal := aControl_u[6];
        rTargetCrucibleRotInternal := aControl_u[7];
        rTargetArgonFlowInternal := aControl_u[8];
        rTargetThrottleInternal := 45.0;

        (* Integrate cylindrical body length *)
        rBodyLength_mm := rBodyLength_mm + ((rActualPullSpeed_mmpm / 60.0) * rCycleTime_sec);
        rCrystalLength_mm := rNeckLength_mm + rCrownLength_mm + rBodyLength_mm;

        (* Terminate body growth when target length is achieved or melt is depleted *)
        IF (rBodyLength_mm >= rTargetIngotLength_mm) OR (rRemainingMeltMass_kg <= 25.0) THEN
            iState := 8; (* Advance to Tail-Off Cone Reduction *)
        END_IF;

    8: (* STAGE 8: TAIL-OFF END CONE TAPERING (2.8 mm/min, TAPERING TO 0 mm) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        bDiameterLockEngaged := FALSE;

        (* Accelerate pull speed and warm interface to taper crystal down to a point *)
        rTargetPullSpeedInternal := 2.80;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 108.0;
        rTargetLowerPowerInternal := 86.0;
        rTargetBottomPowerInternal := 48.0;
        rTargetSeedRotInternal := 14.0;
        rTargetCrucibleRotInternal := -5.0;
        rTargetArgonFlowInternal := 105.0;
        rTargetThrottleInternal := 45.0;

        (* Integrate tail length *)
        rTailLength_mm := rTailLength_mm + ((rActualPullSpeed_mmpm / 60.0) * rCycleTime_sec);

        tTailOffTimer(IN := (rVotedMeniscusDiam_mm <= 10.0), PT := T#90S);
        IF (rVotedMeniscusDiam_mm <= 8.0) AND tTailOffTimer.Q THEN
            tTailOffTimer(IN := FALSE);
            iState := 9; (* Advance to Ingot Separation & Lift *)
        END_IF;

    9: (* STAGE 9: INGOT SEPARATION & HIGH-SPEED LIFT TO COOLING CHAMBER *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        (* Detach crystal from melt surface and hoist into upper cooling station *)
        rTargetPullSpeedInternal := 45.0; (* 45 mm/min rapid lift *)
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 75.0;
        rTargetLowerPowerInternal := 60.0;
        rTargetBottomPowerInternal := 30.0;
        rTargetSeedRotInternal := 5.0;
        rTargetCrucibleRotInternal := 2.0;
        rTargetArgonFlowInternal := 120.0;
        rTargetThrottleInternal := 45.0;

        tIngotLiftTimer(IN := TRUE, PT := T#120S);
        IF tIngotLiftTimer.Q THEN
            tIngotLiftTimer(IN := FALSE);
            iState := 10; (* Advance to Controlled Furnace Cooldown *)
        END_IF;

    10: (* STAGE 10: FURNACE & COOLING CHAMBER CONTROLLED COOL-DOWN *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        (* Ramp down hot zone power to protect graphite and quartz components *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 0.0;
        rTargetLowerPowerInternal := 0.0;
        rTargetBottomPowerInternal := 0.0;
        rTargetSeedRotInternal := 2.0;
        rTargetCrucibleRotInternal := 2.0;
        rTargetArgonFlowInternal := 140.0;
        rTargetThrottleInternal := 50.0;

        tCoolDownTimer(IN := (rVotedCrucibleTemp_DegC < 550.0) AND (rChamberShellTemp_DegC < 38.0), PT := T#300S);
        IF tCoolDownTimer.Q THEN
            tCoolDownTimer(IN := FALSE);
            iState := 11; (* Advance to Maintenance Turnaround *)
        END_IF;

    11: (* STAGE 11: MAINTENANCE TURNAROUND & INGOT UNLOAD *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 0.0;
        rTargetLowerPowerInternal := 0.0;
        rTargetBottomPowerInternal := 0.0;
        rTargetSeedRotInternal := 0.0;
        rTargetCrucibleRotInternal := 0.0;
        rTargetArgonFlowInternal := 0.0;
        rTargetThrottleInternal := 100.0;

        (* Await operator reset and recipe start *)
        IF bResetFaults AND bMasterEnable THEN
            iState := 0; (* Cycle back to state 0 for next ingot run *)
        END_IF;

    99: (* STAGE 99: EMERGENCY FAILSFE HOLD & QUENCH PURGE *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bDiameterLockEngaged := FALSE;

        (* Immediate emergency power dump and protective inert gas flood *)
        rTargetPullSpeedInternal := 0.0;
        rTargetCrucibleLiftInternal := 0.0;
        rTargetUpperPowerInternal := 0.0;
        rTargetLowerPowerInternal := 0.0;
        rTargetBottomPowerInternal := 0.0;
        rTargetSeedRotInternal := 0.0;
        rTargetCrucibleRotInternal := 0.0;
        rTargetArgonFlowInternal := 150.0; (* Full flood *)
        rTargetThrottleInternal := 40.0;

        (* Fault recovery requires unlatching all safety alarms *)
        IF bResetFaults AND NOT bSystemTripped THEN
            iState := 0; (* Return to parked state *)
        END_IF;

END_CASE;

iOperatingStage := iState;
"""
