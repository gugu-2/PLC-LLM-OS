# mega_casting_builder/build_phase5_fsm.py

def get_phase5_fsm():
    return """(* =====================================================================================================================
 * PHASE 5: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
 * Full industrial casting sequence for 6,000-Ton Giga-Casting cell:
 *   0: STATE_IDLE
 *   1: STATE_MOLD_DIE_PREHEAT_OIL_BALANCE
 *   2: STATE_LADLE_POUR_MOLTEN_ALUMINUM_SHOT_SLEEVE
 *   3: STATE_TOGGLE_CLAMP_LOCKUP_60000KN
 *   4: STATE_VACUUM_EVACUATION_DRAWDOWN_25MBAR
 *   5: STATE_PHASE1_SLOW_SHOT_WAVE_FREE_ACCEL
 *   6: STATE_PHASE2_FAST_SHOT_GATE_INJECTION_RUN
 *   7: STATE_PHASE3_INSTANT_INTENSIFICATION_SPIKE
 *   8: STATE_PHASE4_BISCUIT_HOLD_AND_SOLIDIFICATION
 *   9: STATE_VACUUM_VENT_AND_CORE_PULL_RETRACT
 *   10: STATE_DIE_CLAMP_OPEN_AND_DECEL_CUSHION
 *   11: STATE_SERVO_EJECTOR_CASTING_DEMOLD
 *   12: STATE_ROBOTIC_EXTRACTOR_AND_DIE_SPRAY_COAT
 *   13: STATE_EMERGENCY_METAL_FLASH_OR_PRESSURE_TRIP
 * ===================================================================================================================== *)

(* Detect FSM State Transition & Handle State Timer *)
IF iFSM_State <> iFSM_PrevState THEN
    bFSM_FirstScan := TRUE;
    rFSM_StateTimer_s := 0.0;
    iFSM_PrevState := iFSM_State;
ELSE
    bFSM_FirstScan := FALSE;
    rFSM_StateTimer_s := rFSM_StateTimer_s + rScanDeltaT;
END_IF;

iFSM_CurrentState := iFSM_State;
bCycleComplete_Pulse := FALSE;

(* Global Safety Interlock Check: Any trip forces immediate emergency state *)
IF (NOT bEmergencyStop) OR (bGeneralFault) OR (bAlarm_HeadPress_HH) OR (bAlarm_CavityPress_HH) OR (bAlarm_Clamp_LL AND (iFSM_State >= 5 AND iFSM_State <= 8)) THEN
    IF iFSM_State <> 13 THEN
        iFSM_State := 13; (* Force STATE_EMERGENCY_METAL_FLASH_OR_PRESSURE_TRIP *)
        bFSM_FirstScan := TRUE;
    END_IF;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * MAIN DETERMINISTIC FINITE STATE MACHINE DISPATCHER
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_State OF

    (* =================================================================================================================
     * STATE 0: STATE_IDLE
     * Cell waiting in safe quiescent standby for automatic casting cycle start permissive
     * ================================================================================================================= *)
    0:
        IF bFSM_FirstScan THEN
            bCycleActive                 := FALSE;
            bVacuumValve_Open_Cmd        := FALSE;
            bVacuumPurge_N2_Cmd          := FALSE;
            bCorePull_Advance_Cmd        := FALSE;
            bCorePull_Retract_Cmd        := FALSE;
            bClampLockup_Cmd             := FALSE;
            bClampOpen_Cmd               := FALSE;
            bServoEjector_Fire_Cmd       := FALSE;
            bRobotExtractor_Start_Cmd    := FALSE;
            bRobotSpray_Start_Cmd        := FALSE;
            bIntensification_Triggered   := FALSE;
            bIntensification_Complete    := FALSE;
            rShotCycle_Timer_Sec         := 0.0;
        END_IF;

        (* Check System Readiness Interlocks *)
        IF bEnable AND bEmergencyStop AND bSafetyGate_Closed AND bRobot_Extractor_Home AND bRobot_Spray_Home AND
           bEjector_Retracted_Permissive AND bAccumulator_Charged_Permissive AND NOT bGeneralFault THEN

            IF bAutoCycleStart THEN
                bCycleActive := TRUE;
                iFSM_State := 1; (* Advance to STATE_MOLD_DIE_PREHEAT_OIL_BALANCE *)
            END_IF;
        END_IF;

    (* =================================================================================================================
     * STATE 1: STATE_MOLD_DIE_PREHEAT_OIL_BALANCE
     * Circulate thermal regulation oil until fixed and moving die halves reach thermal equilibrium
     * ================================================================================================================= *)
    1:
        IF bFSM_FirstScan THEN
            bPreheat_Balanced := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Check Die Surface Equilibrium: Must be within 15 deg C and >= 195 deg C *)
        IF (rFixedDie_Temp_Actual >= (rRecipe_DieTemp_Target_degC - 25.0)) AND
           (rMovingDie_Temp_Actual >= (rRecipe_DieTemp_Target_degC - 30.0)) AND
           (ABS(rFixedDie_Temp_Actual - rMovingDie_Temp_Actual) <= 15.0) THEN
            bPreheat_Balanced := TRUE;
        ELSE
            bPreheat_Balanced := FALSE;
        END_IF;

        (* Permissive to proceed with ladle pour once die steel is warm *)
        IF bPreheat_Balanced OR (rFSM_StateTimer_s > 5.0) THEN
            iFSM_State := 2; (* Advance to STATE_LADLE_POUR_MOLTEN_ALUMINUM_SHOT_SLEEVE *)
        END_IF;

        (* Watchdog Timeout *)
        IF rFSM_StateTimer_s > rFSM_StateTimeout_s THEN
            bGeneralWarning := TRUE;
        END_IF;

    (* =================================================================================================================
     * STATE 2: STATE_LADLE_POUR_MOLTEN_ALUMINUM_SHOT_SLEEVE
     * 6-Axis robotic ladle pours 75 kg of molten AlSi10MnMg alloy at 680 deg C into cold chamber sleeve
     * ================================================================================================================= *)
    2:
        IF bFSM_FirstScan THEN
            bLadle_Pour_Ready := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Wait for Robotic Ladle Sequence Complete Permissive *)
        IF bLadle_Pour_Completed AND (rLadle_Dosed_Weight_kg >= 70.0) AND (rLadle_Dosed_Weight_kg <= 82.0) THEN
            (* Validate Molten Alloy Pour Temperature: nominal 680 C +/- 25 C *)
            IF (rLadle_Melt_Temp_Actual >= 650.0) AND (rLadle_Melt_Temp_Actual <= 715.0) THEN
                bLadle_Pour_Ready := TRUE;
                iFSM_State := 3; (* Advance to STATE_TOGGLE_CLAMP_LOCKUP_60000KN *)
            END_IF;
        END_IF;

        (* Pour Timeout Trip: Molten metal will chill if sitting in sleeve > 18 seconds *)
        IF rFSM_StateTimer_s > 18.0 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 3: STATE_TOGGLE_CLAMP_LOCKUP_60000KN
     * Hydraulic toggle cylinders close moving platen, engage low-pressure mold protection, lockup to 60,000 kN
     * ================================================================================================================= *)
    3:
        IF bFSM_FirstScan THEN
            bClampLockup_Cmd := TRUE;
            bClamp_Locked_Permissive := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Advance Side Core Slides simultaneously during lockup *)
        bCorePull_Advance_Cmd := TRUE;

        (* Evaluate Clamping Force Lockup: Must reach >= 95% of recipe tonnage (57,000 kN) *)
        IF (rTotalClampingForce_kN >= (rRecipe_ClampTonnage_kN * 0.95)) AND
           (rPlatenTilt_Parallelism_um <= rTrip_PlatenTilt_H) AND
           bCorePins_Advanced_Permissive THEN

            bClamp_Locked_Permissive := TRUE;
            iFSM_State := 4; (* Advance to STATE_VACUUM_EVACUATION_DRAWDOWN_25MBAR *)
        END_IF;

        (* Lockup Timeout Trip *)
        IF rFSM_StateTimer_s > 12.0 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 4: STATE_VACUUM_EVACUATION_DRAWDOWN_25MBAR
     * Open dual parting-plane chill block vacuum valves, drawdown sleeve and cavity to < 25 mbar
     * ================================================================================================================= *)
    4:
        IF bFSM_FirstScan THEN
            bVacuumValve_Open_Cmd := TRUE;
            bVacuum_Evacuated_Permissive := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Vacuum Drawdown Evaluation *)
        IF (rVacPressure_Voted <= rRecipe_Vacuum_Threshold_mbar) THEN
            (* Check Acoustic Leak Rate: Parting seal must be tight (< 25 mbar/s leak rate) *)
            IF rVac_LeakRate_Actual_mbar_s < 25.0 THEN
                bVacuum_Evacuated_Permissive := TRUE;
                iFSM_State := 5; (* Advance to STATE_PHASE1_SLOW_SHOT_WAVE_FREE_ACCEL *)
            END_IF;
        END_IF;

        (* Evacuation Timeout: If cannot reach deep vacuum in 2.5 seconds, abort to prevent shot freeze *)
        IF rFSM_StateTimer_s > 2.50 THEN
            bAlarm_Vac_LL := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 5: STATE_PHASE1_SLOW_SHOT_WAVE_FREE_ACCEL
     * Plunger moves at critical wave speed (0.25..0.65 m/s) with parabolic wave suppression to cover pour hole
     * ================================================================================================================= *)
    5:
        IF bFSM_FirstScan THEN
            bPhase1_Complete := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Transition to Phase 2 Fast Shot once plunger crosses recipe switchpoint position *)
        IF rPlungerPos_Voted >= rRecipe_Phase1_SwitchPos THEN
            bPhase1_Complete := TRUE;
            iFSM_State := 6; (* Advance to STATE_PHASE2_FAST_SHOT_GATE_INJECTION_RUN *)
        END_IF;

        (* Phase 1 Stiction / Jam Timeout *)
        IF rFSM_StateTimer_s > 4.50 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 6: STATE_PHASE2_FAST_SHOT_GATE_INJECTION_RUN
     * Ultra-fast cavity fill up to 9.5 m/s (critical fill time 30 - 45 ms) under real-time closed loop
     * ================================================================================================================= *)
    6:
        IF bFSM_FirstScan THEN
            bPhase2_Complete := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Detect Infill Completion / Transition to Phase 3 Intensification *)
        (* Trigger Conditions:
         * 1) In-Cavity Dynamic Piezo Pressure jumps above 150 bar (metal front hits end of cavity)
         * 2) Acoustic Fill Shock Wave Gradient dP_cavity/dt exceeds 35 bar/ms (hydrodynamic water hammer)
         * 3) Plunger position reaches mechanical infill cushion switchpoint *)
        IF (rCavityPress_Voted >= 150.0) OR
           (rAcousticFillShock_bar_ms >= 35.0) OR
           (rPlungerPos_Voted >= (rTotalStrokeLength_mm - (rRecipe_Biscuit_Nominal_mm + 25.0))) THEN

            bPhase2_Complete := TRUE;
            bIntensification_Triggered := TRUE;
            rIntensification_Timer_ms := 0.0;
            rIntensification_StartPress_bar := rHeadPress_Voted;
            iFSM_State := 7; (* Advance to STATE_PHASE3_INSTANT_INTENSIFICATION_SPIKE *)
        END_IF;

        (* Fast Shot Runaway Timeout *)
        IF rFSM_StateTimer_s > 0.850 THEN
            bAlarm_PlungerVel_HH := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 7: STATE_PHASE3_INSTANT_INTENSIFICATION_SPIKE
     * Accumulator booster cartridge valve fires to build 1,200 bar specific pressure within 15 ms
     * ================================================================================================================= *)
    7:
        IF bFSM_FirstScan THEN
            bPhase3_Complete := FALSE;
            rIntensification_Timer_ms := 0.0;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;
        rIntensification_Timer_ms := rIntensification_Timer_ms + (rScanDeltaT * 1000.0);

        (* Intensification Pressure Rise Verification *)
        IF (rHeadPress_Voted >= (rRecipe_Intensification_Press * 0.95)) OR (rIntensification_Timer_ms >= 35.0) THEN
            rIntensification_RiseTime_Actual_ms := rIntensification_Timer_ms;
            bIntensification_Complete := TRUE;
            bPhase3_Complete := TRUE;

            (* Check ISA-18.2 Rise Time Performance Limit (<= 15.0 ms ideal, > 22.0 ms triggers warning) *)
            IF rIntensification_RiseTime_Actual_ms > rTrip_IntensificationDelay_HH THEN
                bAlarm_IntensificationDelay_HH := TRUE;
            END_IF;

            iFSM_State := 8; (* Advance to STATE_PHASE4_BISCUIT_HOLD_AND_SOLIDIFICATION *)
        END_IF;

    (* =================================================================================================================
     * STATE 8: STATE_PHASE4_BISCUIT_HOLD_AND_SOLIDIFICATION
     * Crystallization holding pressure (950 bar) maintained during in-die solid cooling dwell (14.5 s)
     * ================================================================================================================= *)
    8:
        IF bFSM_FirstScan THEN
            bPhase4_Complete := FALSE;
            (* Record Final Plunger Rest Coordinate for Biscuit Thickness Calculation *)
            rPlunger_FinalCushionPos_mm := rPlungerPos_Voted;
            rBiscuitThickness_Actual_mm := rTotalStrokeLength_mm - rPlunger_FinalCushionPos_mm;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Maintain Holding Pressure until Solidification Dwell Complete *)
        IF rFSM_StateTimer_s >= rRecipe_Hold_Solidification_Time_s THEN
            bPhase4_Complete := TRUE;
            iFSM_State := 9; (* Advance to STATE_VACUUM_VENT_AND_CORE_PULL_RETRACT *)
        END_IF;

    (* =================================================================================================================
     * STATE 9: STATE_VACUUM_VENT_AND_CORE_PULL_RETRACT
     * Close vacuum valves, purge channels with nitrogen, retract hydraulic side core slides
     * ================================================================================================================= *)
    9:
        IF bFSM_FirstScan THEN
            bVacuumValve_Open_Cmd := FALSE;
            bVacuumPurge_N2_Cmd   := TRUE;
            bCorePull_Retract_Cmd := TRUE;
            bVacuum_Vented_Permissive := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Wait for Core Pins Retracted and Cavity Vented to Atmospheric Pressure *)
        IF bCorePins_Retracted_Permissive AND (rVacPressure_Voted >= 900.0) AND (rFSM_StateTimer_s >= 0.80) THEN
            bVacuumPurge_N2_Cmd := FALSE;
            bVacuum_Vented_Permissive := TRUE;
            iFSM_State := 10; (* Advance to STATE_DIE_CLAMP_OPEN_AND_DECEL_CUSHION *)
        END_IF;

        (* Retract Timeout *)
        IF rFSM_StateTimer_s > 6.0 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 10: STATE_DIE_CLAMP_OPEN_AND_DECEL_CUSHION
     * Decompress toggle hydraulic cylinder, slow crack-open stroke, fast traverse open, deceleration cushion
     * ================================================================================================================= *)
    10:
        IF bFSM_FirstScan THEN
            bClampLockup_Cmd := FALSE;
            bClampOpen_Cmd   := TRUE;
            bClamp_Open_Permissive := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Wait for Moving Platen to Reach Full Open Stroke Distance (e.g. 2,800 mm stroke) *)
        IF (rTotalClampingForce_kN <= 250.0) AND (rFSM_StateTimer_s >= 3.80) THEN
            bClamp_Open_Permissive := TRUE;
            iFSM_State := 11; (* Advance to STATE_SERVO_EJECTOR_CASTING_DEMOLD *)
        END_IF;

        (* Clamp Open Timeout *)
        IF rFSM_StateTimer_s > 10.0 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 11: STATE_SERVO_EJECTOR_CASTING_DEMOLD
     * Multi-stage servo ejector plate advances 180 mm to demold 75 kg rear underbody casting
     * ================================================================================================================= *)
    11:
        IF bFSM_FirstScan THEN
            bServoEjector_Fire_Cmd := TRUE;
            bDemold_Ejection_Permissive := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Ejector Forward Dwell and Part Release Confirmation *)
        IF rFSM_StateTimer_s >= 1.50 THEN
            bDemold_Ejection_Permissive := TRUE;
            iFSM_State := 12; (* Advance to STATE_ROBOTIC_EXTRACTOR_AND_DIE_SPRAY_COAT *)
        END_IF;

    (* =================================================================================================================
     * STATE 12: STATE_ROBOTIC_EXTRACTOR_AND_DIE_SPRAY_COAT
     * 6-Axis heavy part unloader robot grips casting, spray tooling coats die faces with release agent
     * ================================================================================================================= *)
    12:
        IF bFSM_FirstScan THEN
            bRobotExtractor_Start_Cmd := TRUE;
            bRobotSpray_Start_Cmd     := TRUE;
            bPart_Extracted_Permissive := FALSE;
            bDie_Sprayed_Permissive    := FALSE;
        END_IF;

        rShotCycle_Timer_Sec := rShotCycle_Timer_Sec + rScanDeltaT;

        (* Wait for Robot Extractor and Spray Manifold to Complete and Return Home *)
        IF bRobot_Extractor_Home AND bRobot_Spray_Home AND (rFSM_StateTimer_s >= 4.50) THEN
            bPart_Extracted_Permissive := TRUE;
            bDie_Sprayed_Permissive    := TRUE;
            bServoEjector_Fire_Cmd     := FALSE; (* Retract ejector pins *)

            (* End-of-Cycle Handshake *)
            rCycleTime_Elapsed_s := rShotCycle_Timer_Sec;
            bCycleComplete_Pulse := TRUE;
            iFSM_State := 0; (* Return to STATE_IDLE *)
        END_IF;

        (* Extraction Timeout *)
        IF rFSM_StateTimer_s > 25.0 THEN
            bGeneralFault := TRUE;
            iFSM_State := 13;
        END_IF;

    (* =================================================================================================================
     * STATE 13: STATE_EMERGENCY_METAL_FLASH_OR_PRESSURE_TRIP
     * Emergency abort state: immediate injection valve dump, vacuum isolation, alarm latching
     * ================================================================================================================= *)
    13:
        IF bFSM_FirstScan THEN
            (* Isolate all fluid power actuation *)
            bVacuumValve_Open_Cmd     := FALSE;
            bVacuumPurge_N2_Cmd       := FALSE;
            bCorePull_Advance_Cmd     := FALSE;
            bCorePull_Retract_Cmd     := FALSE;
            bServoEjector_Fire_Cmd    := FALSE;
            bRobotExtractor_Start_Cmd := FALSE;
            bRobotSpray_Start_Cmd     := FALSE;
            bGeneralFault             := TRUE;
        END_IF;

        (* Operator Alarm Reset Handshake *)
        IF bResetAlarms AND bEmergencyStop AND bSafetyGate_Closed THEN
            bGeneralFault := FALSE;
            bAlarm_HeadPress_HH := FALSE;
            bAlarm_CavityPress_HH := FALSE;
            bAlarm_PlungerVel_HH := FALSE;
            bAlarm_Vac_LL := FALSE;
            bAlarm_Clamp_LL := FALSE;
            bFirstOut_Latched := FALSE;
            dwFirstOut_Code := 16#00000000;
            iFSM_State := 0; (* Return to STATE_IDLE *)
        END_IF;

END_CASE;
"""
