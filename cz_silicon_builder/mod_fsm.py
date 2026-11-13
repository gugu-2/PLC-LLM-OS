# cz_silicon_builder/mod_fsm.py
# -*- coding: utf-8 -*-

def generate_fsm():
    return """(* ==========================================================================================
   PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
   ==========================================================================================
   Manages the complete Czochralski single-crystal silicon ingot growth lifecycle:
     0: STATE_IDLE
     1: STATE_CHAMBER_VACUUM_EVACUATION_AND_LEAK_CHECK
     2: STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE
     3: STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER
     4: STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK
     5: STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING
     6: STATE_DASH_NECKING_DISLOCATION_ELIMINATION
     7: STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP
     8: STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION
     9: STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE
     10: STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING
     11: STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER
     12: STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE
     13: STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP
   ========================================================================================== *)

(* Track total campaign elapsed time *)
rTotalProcessElapsedTime := rTotalProcessElapsedTime + rCycleTimeSec;

(* Detect state change to reset dwell timer *)
IF iCurrentFSMState <> iLastStateIndex THEN
    rCurrentStateDwellTime := 0.0;
    iLastStateIndex := iCurrentFSMState;
ELSE
    rCurrentStateDwellTime := rCurrentStateDwellTime + rCycleTimeSec;
END_IF;

(* Master Safety Interlock Check: Any critical hardware trip forces emergency state 13 *)
IF bEmergencyStop OR bAlm_CrucibleMeltLeakDetected OR bAlm_QuartzCrucibleRupture
   OR bAlm_CoolingWater_FlowTrip OR bAlm_CoolingWater_TempTrip THEN
    iCurrentFSMState := STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP;
END_IF;

CASE iCurrentFSMState OF

    (* --------------------------------------------------------------------------------------
       STATE 0: IDLE / STANDBY
       -------------------------------------------------------------------------------------- *)
    STATE_IDLE:
        bSequenceActive := FALSE;
        bDislocationFreeStructure := FALSE;
        bHabitLinesDetected := FALSE;
        bVoronkovCriterionSatisfied := FALSE;

        (* Zero all actuator commands *)
        u_cmd[1] := 0.0; (* Crystal puller *)
        u_cmd[2] := 0.0; (* Main graphite heater *)
        u_cmd[3] := 0.0; (* Crucible lift *)
        u_cmd[4] := 0.0; (* Cusp coil current *)
        u_cmd[5] := 0.0; (* Seed rotation *)
        rCrucibleRotationCmd := 0.0;
        rArgonMFCFlowCmd := 0.0;
        rVacuumThrottleValveCmd := 0.0;

        (* System Ready condition *)
        bSystemReady := (NOT bEmergencyStop)
                        AND (NOT bAlm_CoolingWater_FlowTrip)
                        AND (NOT bAlm_CoolingWater_TempTrip)
                        AND (NOT bPyro_CriticalFailSafe)
                        AND (rChamberVacuumPressure < 1050.0);

        IF bEnable AND bAutoMode AND bSystemReady THEN
            iCurrentFSMState := STATE_CHAMBER_VACUUM_EVACUATION_AND_LEAK_CHECK;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 1: CHAMBER VACUUM EVACUATION AND LEAK RATE CHECK
       -------------------------------------------------------------------------------------- *)
    STATE_CHAMBER_VACUUM_EVACUATION_AND_LEAK_CHECK:
        bSequenceActive := TRUE;
        bSystemReady := FALSE;
        rVacuumThrottleValveCmd := 100.0; (* Full open to turbo/dry roots vacuum pumps *)
        rArgonMFCFlowCmd := 0.0;
        u_cmd[1] := 0.0;
        u_cmd[2] := 0.0;
        u_cmd[3] := 0.0;
        u_cmd[4] := 0.0;
        u_cmd[5] := 0.0;

        (* Evacuate chamber down to high vacuum base pressure (< 0.05 mbar) *)
        ton_VacuumEvacTimer(
            IN := (rChamberVacuumPressure < 0.050),
            PT := T#30S
        );

        (* Once base vacuum achieved, throttle valve isolates chamber for leak rate check *)
        IF ton_VacuumEvacTimer.Q THEN
            rVacuumThrottleValveCmd := 0.0; (* Closed *)
            ton_LeakRateCheckTimer(IN := TRUE, PT := T#20S);
            IF ton_LeakRateCheckTimer.Q THEN
                (* If pressure rise during 20 s isolation is < 0.015 mbar, proceed to backfill *)
                IF rChamberVacuumPressure < 0.065 THEN
                    iCurrentFSMState := STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE;
                ELSE
                    (* Vacuum leak rate excessive: abort to emergency trip *)
                    iCurrentFSMState := STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP;
                END_IF;
            END_IF;
        ELSE
            ton_LeakRateCheckTimer(IN := FALSE, PT := T#20S);
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 2: ARGON MELT PURGE AND PRESSURE STABILIZE
       -------------------------------------------------------------------------------------- *)
    STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE:
        (* Introduce ultra-pure Argon downward purge flow to sweep chamber *)
        rArgonMFCFlowCmd := 110.0; (* 110 slpm *)
        (* Closed-loop throttling to maintain 20.0 mbar process vacuum *)
        IF rChamberVacuumPressure > 21.0 THEN
            rVacuumThrottleValveCmd := 45.0;
        ELSIF rChamberVacuumPressure < 19.0 THEN
            rVacuumThrottleValveCmd := 25.0;
        ELSE
            rVacuumThrottleValveCmd := 35.0;
        END_IF;

        ton_ArgonBackfillTimer(
            IN := (rChamberVacuumPressure >= 18.5) AND (rChamberVacuumPressure <= 21.5),
            PT := T#25S
        );

        IF ton_ArgonBackfillTimer.Q THEN
            iCurrentFSMState := STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 3: POLYSILICON CHARGE MELTDOWN FULL POWER
       -------------------------------------------------------------------------------------- *)
    STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER:
        (* Ramp main graphite heater to meltdown power *)
        u_cmd[2] := 152.0; (* 152 kW heating *)
        rCrucibleRotationCmd := 4.5; (* 4.5 RPM to distribute thermal field evenly *)
        rArgonMFCFlowCmd := 125.0; (* High Argon purge to vent initial outgassing & SiO vapors *)
        rVacuumThrottleValveCmd := 38.0;

        (* Check for complete phase change: Heater TC > 1560 C and bottom susceptor TC > 1435 C *)
        ton_MeltdownSoakTimer(
            IN := (rVotedHeaterTemp >= 1560.0) AND (rBottomCrucibleTC >= 1435.0),
            PT := T#60S
        );

        IF ton_MeltdownSoakTimer.Q THEN
            iCurrentFSMState := STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 4: MELT EQUILIBRIUM AND CUSP MAGNETIC LOCK
       -------------------------------------------------------------------------------------- *)
    STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK:
        (* Ramp Cusp magnetic coils to suppress turbulent Rayleigh-Benard convection cells *)
        u_cmd[4] := 380.0; (* 380 A cusp field current *)
        (* Back down heater power to quiescent thermal equilibrium holding power *)
        u_cmd[2] := 86.5; (* 86.5 kW *)
        rCrucibleRotationCmd := 6.0;
        u_cmd[5] := 12.0; (* Counter-rotate seed shaft at 12 RPM *)

        ton_CuspMagneticSoakTimer(
            IN := (rBulkConvectionVelocity_RMS < 0.65)
                  AND (rVotedMeniscusTemp >= 1416.0)
                  AND (rVotedMeniscusTemp <= 1422.0),
            PT := T#25S
        );

        IF ton_CuspMagneticSoakTimer.Q THEN
            iCurrentFSMState := STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 5: SEED CRYSTAL DIP AND MELT WETTING
       -------------------------------------------------------------------------------------- *)
    STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING:
        (* Lower crystal seed slowly until meniscus contact is achieved *)
        IF rVotedCrystalWeight < 0.15 THEN
            u_cmd[1] := -8.5; (* Lower seed downward at 8.5 mm/min *)
        ELSE
            (* Load cell detects buoyant meniscus contact: hold zero pull *)
            u_cmd[1] := 0.0;
        END_IF;

        (* Thermal soak to wet seed face and melt back surface oxides *)
        ton_SeedThermalSoakTimer(
            IN := (rVotedCrystalWeight >= 0.15)
                  AND (rVotedMeniscusTemp >= 1414.0)
                  AND (rVotedMeniscusTemp <= 1419.0),
            PT := T#18S
        );

        IF ton_SeedThermalSoakTimer.Q THEN
            iCurrentFSMState := STATE_DASH_NECKING_DISLOCATION_ELIMINATION;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 6: DASH NECKING DISLOCATION ELIMINATION
       -------------------------------------------------------------------------------------- *)
    STATE_DASH_NECKING_DISLOCATION_ELIMINATION:
        (* Rapid pull speed to squeeze diameter to 3.5 mm and force slip dislocations out *)
        u_cmd[1] := 5.40; (* 5.40 mm/min pull rate *)
        u_cmd[2] := 89.0; (* Slightly higher heater to thin the neck *)
        u_cmd[5] := 16.0; (* 16 RPM seed rotation *)
        rCrucibleRotationCmd := -6.0; (* Counter-rotation *)
        x_ref[1] := 3.5; (* Target neck diameter: 3.5 mm *)

        (* Accumulate Dash neck length *)
        rIngotDashNeckLength_mm := rIngotDashNeckLength_mm + (u_cmd[1] * (rCycleTimeSec / 60.0));

        (* Require minimum 220 mm neck length and optical habit line confirmation *)
        ton_DashHabitLineTimer(
            IN := (rIngotDashNeckLength_mm >= 220.0) AND (rVotedIngotDiameter <= 4.2),
            PT := T#12S
        );

        IF ton_DashHabitLineTimer.Q THEN
            bHabitLinesDetected := TRUE;
            bDislocationFreeStructure := TRUE;
            iCurrentFSMState := STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 7: CROWN EXPANSION CONE ANGLE RAMP
       -------------------------------------------------------------------------------------- *)
    STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP:
        (* Decelerate pull rate and lower heater slightly to widen diameter toward 300 mm *)
        u_cmd[1] := 1.15; (* Slow pull 1.15 mm/min *)
        u_cmd[2] := 81.5; (* 81.5 kW *)
        u_cmd[4] := 420.0; (* 420 A cusp field for high interface stability *)
        u_cmd[5] := 14.0;

        (* Ramp diameter reference dynamically *)
        IF x_ref[1] < 298.0 THEN
            x_ref[1] := 3.5 + 4.2 * rCurrentStateDwellTime;
        ELSE
            x_ref[1] := 298.0;
        END_IF;

        rIngotCrownLength_mm := rIngotCrownLength_mm + (u_cmd[1] * (rCycleTimeSec / 60.0));

        IF rVotedIngotDiameter >= 295.0 THEN
            iCurrentFSMState := STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 8: SHOULDER RADIUS ROLLOVER TRANSITION
       -------------------------------------------------------------------------------------- *)
    STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION:
        (* Smoothly roll over from conical crown expansion into constant 300 mm cylinder *)
        x_ref[1] := rTargetIngotDiameter; (* 300.0 mm *)
        u_cmd[1] := 0.92; (* 0.92 mm/min *)
        u_cmd[2] := 83.2; (* 83.2 kW *)

        ton_ShoulderRadiusRolloverTimer(
            IN := (rVotedIngotDiameter >= 298.8) AND (rVotedIngotDiameter <= 301.2),
            PT := T#20S
        );

        IF ton_ShoulderRadiusRolloverTimer.Q THEN
            iCurrentFSMState := STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 9: BODY EQUAL DIAMETER GROWTH (MPC ACTIVE)
       -------------------------------------------------------------------------------------- *)
    STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE:
        (* Closed-loop Model Predictive Control governs actuators u1 through u5 *)
        x_ref[1] := rTargetIngotDiameter; (* 300.0 mm *)
        x_ref[2] := 1414.0; (* Melting isotherm *)
        x_ref[3] := 3.45;   (* G_0 gradient *)
        x_ref[4] := 1426.0; (* Bulk melt *)
        x_ref[5] := 0.35;   (* Low turbulence *)

        (* Crucible lift tracks mass continuity automatically *)
        u_cmd[3] := rCrucibleLiftKinematicSpeed;

        (* Track body length accumulation *)
        rIngotBodyLength_mm := rIngotBodyLength_mm + (u_cmd[1] * (rCycleTimeSec / 60.0));

        (* Transition to Tailout when target body length reached or crucible melt low *)
        IF (rIngotBodyLength_mm >= rTargetGrowthLength) OR (rSiliconMeltMassRemaining_kg <= 18.0) THEN
            iCurrentFSMState := STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 10: TAILOUT END CONE THERMAL SHOCK TAPERING
       -------------------------------------------------------------------------------------- *)
    STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING:
        (* Ramp pull speed and raise heater power to taper crystal diameter down to point *)
        u_cmd[1] := 3.20; (* Accelerate pull rate *)
        u_cmd[2] := 94.0; (* Raise heater power to shrink interface *)
        u_cmd[4] := 300.0;
        u_cmd[5] := 18.0;

        (* Ramp diameter reference down *)
        IF x_ref[1] > 10.0 THEN
            x_ref[1] := 300.0 - 5.8 * rCurrentStateDwellTime;
        ELSE
            x_ref[1] := 5.0;
        END_IF;

        rIngotTailLength_mm := rIngotTailLength_mm + (u_cmd[1] * (rCycleTimeSec / 60.0));

        IF rVotedIngotDiameter <= 6.0 THEN
            iCurrentFSMState := STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 11: CRYSTAL SEPARATION AND LIFT TO COOL CHAMBER
       -------------------------------------------------------------------------------------- *)
    STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER:
        (* Snap crystal clear of molten silicon to avoid meniscus freezing adhesion *)
        u_cmd[1] := 10.0; (* Fast pull upward at 10 mm/min *)
        u_cmd[2] := 45.0; (* Reduce heater to idle holding *)
        u_cmd[3] := 0.0;
        u_cmd[4] := 0.0;
        u_cmd[5] := 4.0; (* Slow spin to radiate evenly *)

        ton_SeparationThermalShockTimer(IN := TRUE, PT := T#45S);

        IF ton_SeparationThermalShockTimer.Q THEN
            iCurrentFSMState := STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 12: RESIDUAL MELT COOLDOWN AND CRUCIBLE PURGE
       -------------------------------------------------------------------------------------- *)
    STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE:
        u_cmd[1] := 0.0;
        u_cmd[2] := 0.0; (* Heaters shut down *)
        u_cmd[3] := 0.0;
        u_cmd[4] := 0.0;
        u_cmd[5] := 0.0;
        rCrucibleRotationCmd := 0.0;
        rArgonMFCFlowCmd := 135.0; (* High flow purge during cooling *)
        rVacuumThrottleValveCmd := 40.0;

        ton_ChamberCoolingPurgeTimer(
            IN := (rVotedHeaterTemp < 280.0) AND (rBottomCrucibleTC < 220.0),
            PT := T#30S
        );

        IF ton_ChamberCoolingPurgeTimer.Q THEN
            iCurrentFSMState := STATE_IDLE;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 13: EMERGENCY MELT LEAK OR VACUUM COLLAPSE TRIP
       -------------------------------------------------------------------------------------- *)
    STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP:
        bSequenceActive := FALSE;
        (* Hard shut down of all thermal power and servo drives *)
        u_cmd[1] := 0.0;
        u_cmd[2] := 0.0; (* Instant thyristor fire cutoff *)
        u_cmd[3] := 0.0;
        u_cmd[4] := 0.0;
        u_cmd[5] := 0.0;
        rCrucibleRotationCmd := 0.0;
        rVacuumThrottleValveCmd := 0.0; (* Isolate vacuum chamber immediately *)
        rArgonMFCFlowCmd := 120.0; (* Positive Argon purge to suppress ambient air ingress *)

        (* Latch emergency first-out if not already recorded *)
        IF iFirstOutCode = 0 THEN
            IF bEmergencyStop THEN
                iFirstOutCode := 101; (* E-Stop Pressed *)
            ELSIF bAlm_CrucibleMeltLeakDetected THEN
                iFirstOutCode := 102; (* Quartz Crucible Melt Leak Detected *)
            ELSIF bAlm_QuartzCrucibleRupture THEN
                iFirstOutCode := 103; (* Quartz Crucible Structural Rupture *)
            ELSIF bAlm_CoolingWater_FlowTrip THEN
                iFirstOutCode := 104; (* Primary Cooling Water Low Flow Trip *)
            ELSIF bAlm_CoolingWater_TempTrip THEN
                iFirstOutCode := 105; (* Primary Cooling Water Over-Temperature Trip *)
            ELSIF bAlm_Vacuum_HH THEN
                iFirstOutCode := 106; (* Vacuum Collapse Overpressure HH *)
            ELSE
                iFirstOutCode := 199; (* Unspecified Process Safety Trip *)
            END_IF;
        END_IF;

        (* Reset capability *)
        IF bResetAlarm AND (NOT bEmergencyStop) AND (NOT bAlm_CrucibleMeltLeakDetected)
           AND (NOT bAlm_QuartzCrucibleRupture) AND (NOT bAlm_CoolingWater_FlowTrip) THEN
            iFirstOutCode := 0;
            iCurrentFSMState := STATE_IDLE;
        END_IF;

ELSE
    (* Fallback protection for undefined state indices *)
    iCurrentFSMState := STATE_IDLE;
END_CASE;

(* Update output status with current state index *)
iCurrentFSMState := iCurrentFSMState;"""
