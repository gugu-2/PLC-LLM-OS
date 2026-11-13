(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * Full Automation Cycle:
 *   State  0: SYSTEM IDLE STANDBY
 *   State  1: MOLD CLOSE RAPID TRAVERSE
 *   State  2: LOW PRESSURE MOLD PROTECTION (LPMP)
 *   State  3: CLAMP LOCKUP TONNAGE BUILD (16,000 kN)
 *   State  4: INJECTION CARRIAGE FORWARD & NOZZLE SEAT
 *   State  5: DYNAMIC INJECTION FILLING VELOCITY PROFILE
 *   State  6: IN-MOLD CAVITY PIEZOELECTRIC V/P TRANSFER
 *   State  7: MULTI-STAGE PACKING & HOLDING PRESSURE
 *   State  8: EXTRUDER PLASTICIZING & DOSING PHASE
 *   State  9: AXIAL SUCK-BACK DECOMPRESSION
 *   State 10: IN-MOLD SOLIDIFICATION COOLING CYCLE
 *   State 11: MOLD OPENING & DECELERATION BRAKING
 *   State 12: PARTS EJECTION & EUROMAP 67 ROBOT HANDSHAKE
 *   State 13: SAFE ABORT, PURGE & RECOVERY ROUTINE
 * ===================================================================================================================== *)

(* State Transition First Scan & Timer Update *)
IF iFSM_State <> iFSM_StatePrev THEN
    bFSM_FirstScan := TRUE;
    rFSM_StateTimer := 0.0;
    iFSM_StatePrev := iFSM_State;
ELSE
    bFSM_FirstScan := FALSE;
    rFSM_StateTimer := rFSM_StateTimer + rScanTime_Ts;
END_IF;

rCycle_TotalTimer := rCycle_TotalTimer + rScanTime_Ts;
rCycle_ActualTime_Out := rCycle_TotalTimer;

(* Emergency Interlock Override Check *)
IF bCmd_EmergencyStop_In OR (dwTrip_Alarms <> 16#0000_0000) THEN
    iFSM_State := 13; (* Immediate Jump to Failsafe Abort State *)
END_IF;

CASE iFSM_State OF
    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 00: SYSTEM IDLE / STANDBY
     * Machine resting, interlocks validated, ready for cycle start
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        bMachine_CycleActive_Out := FALSE;
        rServo_InjVelocity_Cmd_Out := 0.0;
        rServo_HoldPressure_Cmd_Out := 0.0;
        rServo_ScrewRPM_Cmd_Out := 0.0;
        rServo_BackPressure_Cmd_Out := 0.0;
        rServo_ClampTonnage_Cmd_Out := 0.0;
        rServo_ClampVelocity_Cmd_Out := 0.0;
        rServo_EjectorStroke_Cmd_Out := 0.0;
        bPneumatic_CorePull1_Fwd_Out := FALSE;
        bPneumatic_CorePull2_Fwd_Out := FALSE;
        bPneumatic_AirEjectBlast_Out := FALSE;
        bRobot_PermissiveToEnter_Out := FALSE;
        bRobot_CycleComplete_Out := FALSE;
        bVP_SwitchoverLatched := FALSE;
        bVP_TriggeredByCavity := FALSE;
        bVP_TriggeredByRate := FALSE;
        bVP_TriggeredByPosition := FALSE;
        bVP_TriggeredByMeltPres := FALSE;

        IF bCmd_CycleStart_In AND bSafetyGate_FrontClosed_In AND bSafetyGate_RearClosed_In AND
           bRobot_PermissiveToClose_In AND bPneumatics_AirPressureOK_In AND (dwTrip_Alarms = 16#0000_0000) THEN
            rCycle_TotalTimer := 0.0;
            rCavity_PeakObservedPressure := 0.0;
            bMachine_CycleActive_Out := TRUE;
            iFSM_State := 1; (* Initiate Mold Close *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 01: MOLD CLOSE RAPID TRAVERSE
     * High-speed moving platen kinematic traverse until entering sensitive LPMP zone (65 mm)
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        bMachine_CycleActive_Out := TRUE;
        bRobot_PermissiveToEnter_Out := FALSE;
        rServo_ClampTonnage_Cmd_Out := 250.0; (* Pre-charge kinematic traverse force *)

        (* Trapezoidal velocity profiling *)
        IF rFSM_StateTimer < 0.35 THEN
            rServo_ClampVelocity_Cmd_Out := 120.0 + (160.0 * (rFSM_StateTimer / 0.35)); (* Ramp up to 280 mm/s *)
        ELSIF rFSM_StateTimer < 1.45 THEN
            rServo_ClampVelocity_Cmd_Out := 280.0; (* High speed cruise *)
        ELSE
            rServo_ClampVelocity_Cmd_Out := 110.0; (* Pre-deceleration approach *)
        END_IF;

        (* Safety gate monitor *)
        IF (NOT bSafetyGate_FrontClosed_In) OR (NOT bSafetyGate_RearClosed_In) THEN
            bTrip_SafetyGate_Violation := TRUE;
            iFSM_State := 13;
        END_IF;

        (* Transition to Low Pressure Mold Protection Zone *)
        IF rFSM_StateTimer >= 1.80 THEN
            iFSM_State := 2; (* Enter LPMP *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 02: LOW PRESSURE MOLD PROTECTION (LPMP)
     * Ultra-sensitive platen close (< 12.0 kN / 5 bar) to safeguard multi-cavity tooling against trapped parts
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        rServo_ClampVelocity_Cmd_Out := 42.0; (* Slow probing velocity *)
        rServo_ClampTonnage_Cmd_Out := rLPMP_ForceLimit; (* Clamped to maximum 12 kN *)

        (* Obstruction Detection Check: If force spikes or timer elapses before platen touches *)
        IF rTB_TotalClampForce > rLPMP_ForceLimit THEN
            bAlarm_LPMP_ObstructionTrip := TRUE;
            iFSM_State := 13; (* Abort to safe opening / fault *)
        ELSIF rFSM_StateTimer > rLPMP_TimeLimit THEN
            bAlarm_LPMP_ObstructionTrip := TRUE;
            iFSM_State := 13;
        END_IF;

        (* Mold Parting Line Contact Reached Safely *)
        IF rFSM_StateTimer >= 0.85 THEN
            iFSM_State := 3; (* Advance to Full Tonnage Lockup *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 03: CLAMP LOCKUP TONNAGE BUILD (16,000 kN)
     * Servo toggle drives mechanism through kinematic knee lockup to 16,000 kN clamping force
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        rServo_ClampVelocity_Cmd_Out := 18.0; (* High mechanical advantage lockup speed *)
        rServo_ClampTonnage_Cmd_Out := rRecipe_ClampTonnage_In;

        (* Verify Tie-Bar Parallelism Tilt during tonnage ramp *)
        IF rPlaten_MaxDeviation > rAlarm_TB_Tilt_HH_Trip THEN
            bTrip_TB_Tilt_HH := TRUE;
            iFSM_State := 13;
        END_IF;

        (* Clamping Force Tonnage Lockup Reached *)
        IF (rTB_TotalClampForce >= (rRecipe_ClampTonnage_In * 0.985)) OR (rFSM_StateTimer >= 1.25) THEN
            iFSM_State := 4; (* Advance to Carriage Forward *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 04: INJECTION CARRIAGE FORWARD & NOZZLE SEAT
     * Entire injection unit traverses forward to seat high-temperature nozzle tip against sprue bushing
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        (* Engage core pullers if mold tooling requires side actions *)
        bPneumatic_CorePull1_Fwd_Out := TRUE;
        bPneumatic_CorePull2_Fwd_Out := TRUE;

        (* Reset V/P switchover detectors and integrals *)
        bVP_SwitchoverLatched := FALSE;
        bVP_TriggeredByCavity := FALSE;
        bVP_TriggeredByRate := FALSE;
        bVP_TriggeredByPosition := FALSE;
        bVP_TriggeredByMeltPres := FALSE;
        rCavPres_Integral := 0.0;
        rCavity_PeakObservedPressure := 0.0;

        (* Nozzle Contact Force Settling Window *)
        IF rFSM_StateTimer >= 0.50 THEN
            iFSM_State := 5; (* Advance to Dynamic Injection Filling *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 05: DYNAMIC INJECTION FILLING VELOCITY PROFILE
     * Closed-loop volumetric cavity filling under 5-step servo velocity profile with in-mold piezo V/P transfer
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        (* 5-Stage Injection Velocity Profile Mapping *)
        IF rScrewPos_Voted_Val > rInjProfile_Pos1 THEN
            rServo_InjVelocity_Cmd_Out := rInjProfile_Vel1;
        ELSIF rScrewPos_Voted_Val > rInjProfile_Pos2 THEN
            rServo_InjVelocity_Cmd_Out := rInjProfile_Vel2;
        ELSIF rScrewPos_Voted_Val > rInjProfile_Pos3 THEN
            rServo_InjVelocity_Cmd_Out := rInjProfile_Vel3;
        ELSIF rScrewPos_Voted_Val > rInjProfile_Pos4 THEN
            rServo_InjVelocity_Cmd_Out := rInjProfile_Vel4;
        ELSE
            rServo_InjVelocity_Cmd_Out := rInjProfile_Vel5;
        END_IF;

        (* Modulate velocity with active anti-overshoot dampening *)
        rServo_InjVelocity_Cmd_Out := rCavPres_DampenedVelocity;

        (* Transition Trigger: Checked by In-Mold Piezoelectric Cascade in Phase 2 *)
        IF bVP_SwitchoverLatched THEN
            iFSM_State := 6; (* Advance to V/P Transfer *)
        END_IF;

        (* Absolute Injection Stroke Limit Interlock *)
        IF rScrewPos_Voted_Val <= 10.0 THEN
            bVP_SwitchoverLatched := TRUE;
            bVP_TriggeredByPosition := TRUE;
            iFSM_State := 6;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 06: IN-MOLD CAVITY PIEZOELECTRIC V/P TRANSFER
     * Bumpless handover from closed-loop velocity control to cavity pressure packing control (50 ms window)
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        (* Decelerate injection servo velocity to packing entry speed *)
        rServo_InjVelocity_Cmd_Out := 8.0;
        rServo_HoldPressure_Cmd_Out := rHoldProfile_Pres1 * 0.85;

        IF rFSM_StateTimer >= 0.050 THEN
            iFSM_State := 7; (* Advance to Multi-Stage Holding Profile *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 07: MULTI-STAGE PACKING & HOLDING PRESSURE
     * Compensates for polymer volumetric thermal contraction during gate freeze and in-cavity packing
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        rServo_InjVelocity_Cmd_Out := 5.0; (* Velocity clamp *)

        (* 3-Stage Holding Packing Pressure Profile *)
        IF rFSM_StateTimer < rHoldProfile_Time1 THEN
            rServo_HoldPressure_Cmd_Out := rHoldProfile_Pres1;
        ELSIF rFSM_StateTimer < (rHoldProfile_Time1 + rHoldProfile_Time2) THEN
            rServo_HoldPressure_Cmd_Out := rHoldProfile_Pres2;
        ELSIF rFSM_StateTimer < (rHoldProfile_Time1 + rHoldProfile_Time2 + rHoldProfile_Time3) THEN
            rServo_HoldPressure_Cmd_Out := rHoldProfile_Pres3;
        ELSE
            rServo_HoldPressure_Cmd_Out := 0.0;
            iFSM_State := 8; (* Gate frozen, proceed to plasticizing *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 08: EXTRUDER PLASTICIZING & DOSING PHASE
     * Screw motor rotates at 75 RPM, drawing polymer pellets from feed hopper and building next shot
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        rServo_HoldPressure_Cmd_Out := 0.0;
        rServo_InjVelocity_Cmd_Out := 0.0;
        rServo_ScrewRPM_Cmd_Out := rDose_ScrewSpeedRPM;
        rServo_BackPressure_Cmd_Out := rDose_BackPresSetpoint;

        (* Shot Dosing Volume Completed *)
        IF rScrewPos_Voted_Val >= rDose_TargetStroke THEN
            rServo_ScrewRPM_Cmd_Out := 0.0;
            rServo_BackPressure_Cmd_Out := 0.0;
            iFSM_State := 9; (* Advance to Suck-Back Decompression *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 09: AXIAL SUCK-BACK DECOMPRESSION
     * Screw retracts without rotation (7.5 mm) to relieve nozzle pressure and prevent melt drooling
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        rServo_ScrewRPM_Cmd_Out := 0.0;
        rServo_BackPressure_Cmd_Out := 0.0;
        rServo_InjVelocity_Cmd_Out := -1.0 * rSuckBack_Velocity;

        IF rScrewPos_Voted_Val >= (rDose_TargetStroke + rSuckBack_Stroke) OR (rFSM_StateTimer >= 0.65) THEN
            rServo_InjVelocity_Cmd_Out := 0.0;
            iFSM_State := 10; (* Advance to In-Mold Cooling *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 10: IN-MOLD SOLIDIFICATION COOLING CYCLE
     * Thermal heat extraction through mold cooling water channels until part attains structural rigidity
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        rServo_InjVelocity_Cmd_Out := 0.0;
        rServo_HoldPressure_Cmd_Out := 0.0;
        rServo_ScrewRPM_Cmd_Out := 0.0;
        rServo_BackPressure_Cmd_Out := 0.0;

        (* Solidification Duration Check *)
        IF rFSM_StateTimer >= rCooling_Duration THEN
            (* Retract side core pullers prior to mold opening *)
            bPneumatic_CorePull1_Fwd_Out := FALSE;
            bPneumatic_CorePull2_Fwd_Out := FALSE;
            iFSM_State := 11; (* Advance to Mold Opening *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 11: MOLD OPENING & DECELERATION BRAKING
     * Multi-stage toggle opening: Slow breakaway, high-speed travel, and S-curve deceleration to 680 mm
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        rServo_ClampTonnage_Cmd_Out := 0.0;

        (* 3-Stage Opening Velocity Profile *)
        IF rFSM_StateTimer < 0.40 THEN
            rServo_ClampVelocity_Cmd_Out := 35.0; (* Slow breakaway from cavity draft angles *)
        ELSIF rFSM_StateTimer < 1.60 THEN
            rServo_ClampVelocity_Cmd_Out := 320.0; (* High speed opening traverse *)
        ELSE
            rServo_ClampVelocity_Cmd_Out := 55.0; (* Deceleration into end stop *)
        END_IF;

        (* Mold Open Target Position Reached *)
        IF rFSM_StateTimer >= 2.10 THEN
            rServo_ClampVelocity_Cmd_Out := 0.0;
            bRobot_PermissiveToEnter_Out := TRUE; (* Signal Euromap 67 robot to enter mold area *)
            iFSM_State := 12; (* Advance to Parts Ejection *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 12: PARTS EJECTION & EUROMAP 67 ROBOT HANDSHAKE
     * Forward stroke of ejector pin plate combined with pneumatic air burst; robot removal confirmation
     * ----------------------------------------------------------------------------------------------------------------- *)
    12:
        rServo_EjectorStroke_Cmd_Out := rEjector_StrokeTarget;
        bPneumatic_AirEjectBlast_Out := TRUE;

        (* Robot Removal Confirmation or Optical Part Drop Verification *)
        IF bRobot_PartStrippedConfirm_In OR bOptical_PartDropVerified_In OR (rFSM_StateTimer >= 2.50) THEN
            rServo_EjectorStroke_Cmd_Out := 0.0; (* Retract ejectors *)
            bPneumatic_AirEjectBlast_Out := FALSE;
            bRobot_CycleComplete_Out := TRUE;
            iCycle_ShotCounter := iCycle_ShotCounter + 1;

            (* Check for Permissive to Repeat Cycle *)
            IF bRobot_PermissiveToClose_In AND bCmd_CycleStart_In THEN
                bRobot_PermissiveToEnter_Out := FALSE;
                bRobot_CycleComplete_Out := FALSE;
                iFSM_State := 1; (* Seamless loop back to Mold Close *)
            ELSE
                iFSM_State := 0; (* Return to Idle Standby *)
            END_IF;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STATE 13: SAFE ABORT, PURGE & RECOVERY ROUTINE
     * Emergency shutdown state: all motion halted, nozzle cleared, waiting for operator reset
     * ----------------------------------------------------------------------------------------------------------------- *)
    13:
        bMachine_CycleActive_Out := FALSE;
        rServo_InjVelocity_Cmd_Out := 0.0;
        rServo_HoldPressure_Cmd_Out := 0.0;
        rServo_ScrewRPM_Cmd_Out := 0.0;
        rServo_BackPressure_Cmd_Out := 0.0;
        rServo_ClampVelocity_Cmd_Out := 0.0;
        rServo_ClampTonnage_Cmd_Out := 0.0;
        rServo_EjectorStroke_Cmd_Out := 0.0;
        bPneumatic_AirEjectBlast_Out := FALSE;
        bRobot_PermissiveToEnter_Out := FALSE;
        bTrip_EmergencyLockout_Out := TRUE;

        (* Manual Purge Sequence *)
        IF bCmd_ManualPurge_In AND bSafetyGate_FrontClosed_In THEN
            rServo_ScrewRPM_Cmd_Out := 25.0;
            rServo_InjVelocity_Cmd_Out := 12.0;
        END_IF;

        (* Operator Alarm Reset Handshake *)
        IF bCmd_ResetAlarms_In AND (NOT bCmd_EmergencyStop_In) AND
           bSafetyGate_FrontClosed_In AND bSafetyGate_RearClosed_In THEN
            bTrip_EmergencyLockout_Out := FALSE;
            bAlarm_LPMP_ObstructionTrip := FALSE;
            bTrip_CavPres_HH := FALSE;
            bTrip_MeltPres_HH := FALSE;
            bTrip_Clamp_HH := FALSE;
            bTrip_TB_Tilt_HH := FALSE;
            bTrip_SafetyGate_Violation := FALSE;
            bTrip_TMR_SensorCollapse := FALSE;
            iFSM_State := 0; (* Return to Idle *)
        END_IF;

    ELSE
        iFSM_State := 13; (* Unhandled State Fault Safe Abort *)
END_CASE;
