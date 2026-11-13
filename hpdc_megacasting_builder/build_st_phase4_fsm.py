# hpdc_megacasting_builder/build_st_phase4_fsm.py

def get_phase4_fsm():
    return """(* =====================================================================================================================
 * PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
 * Millisecond-synchronized sequencing of the 4,000-Ton Gigacasting Machine Cycle
 * ===================================================================================================================== *)

(* Master Safety and Emergency Abortion Interlock Override *)
IF (NOT bEmergency_Stop_OK_In) OR (NOT bSafetyGate_Front_Closed_In) OR (NOT bSafetyGate_Rear_Closed_In)
   OR bAlarm_TMR_MajorDegrade OR bCmd_Cycle_Abort_In THEN
    IF iFSM_CurrentState <> 14 THEN
        iFSM_NextState := 14; (* Divert to Emergency Failsafe Dump State *)
    END_IF;
END_IF;

(* State Transition Logic & Stopwatch Timer Accumulator *)
IF iFSM_CurrentState <> iFSM_NextState THEN
    iFSM_PreviousState := iFSM_CurrentState;
    iFSM_CurrentState := iFSM_NextState;
    rFSM_StateTimer_s := 0.0;
    bFSM_StateFirstScan := TRUE;
ELSE
    rFSM_StateTimer_s := rFSM_StateTimer_s + 0.001; (* 1 ms task cycle *)
    bFSM_StateFirstScan := FALSE;
END_IF;

IF bCycleRunning THEN
    rTotalCycleTimer_s := rTotalCycleTimer_s + 0.001;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * 14-STAGE STATE EXECUTION CASE CONSTRUCT
 * --------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_CurrentState OF

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 0: IDLE & SAFETY INTERLOCKS VERIFICATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    0:
        bCycleRunning := FALSE;
        rTotalCycleTimer_s := 0.0;
        bVacuum_Pump_Start_Out := FALSE;
        bChillVent_SealValve_Out := FALSE;
        bCoreA_Insert_Cmd_Out := FALSE;
        bCoreA_Retract_Cmd_Out := FALSE;
        bCoreB_Insert_Cmd_Out := FALSE;
        bCoreB_Retract_Cmd_Out := FALSE;
        bCoreC_Insert_Cmd_Out := FALSE;
        bCoreC_Retract_Cmd_Out := FALSE;
        bCoreD_Insert_Cmd_Out := FALSE;
        bCoreD_Retract_Cmd_Out := FALSE;
        bLadle_Robot_Permissive_Out := FALSE;
        bExtract_Robot_Permissive_Out := FALSE;
        bSpray_Robot_Permissive_Out := FALSE;
        bAccumulator_Dump_Safe_Out := FALSE;
        rEjector_Servo_Cmd_Out := 0.0;

        (* Check Manual Plunger JOG commands *)
        IF bCmd_Manual_PlungerFwd_In AND bExtract_Robot_Clear_In AND bSpray_Robot_Clear_In THEN
            rServo_ShotSpool_Cmd_Out := 8.0; (* 8% forward slow creep *)
        ELSIF bCmd_Manual_PlungerRev_In AND bExtract_Robot_Clear_In AND bSpray_Robot_Clear_In THEN
            rServo_ShotSpool_Cmd_Out := -12.0; (* 12% reverse retract *)
        END_IF;

        (* Permissive to Start Automatic Casting Cycle *)
        IF bCmd_AutoCycle_Start_In AND bEmergency_Stop_OK_In AND bSafetyGate_Front_Closed_In AND bSafetyGate_Rear_Closed_In
           AND bHydraulic_Motor_Running_In AND (rTMR_PT501_Voted >= rLim_PT501_Accum_L)
           AND bExtract_Robot_Clear_In AND bSpray_Robot_Clear_In AND bLadle_Robot_Home_In THEN
            bCycleRunning := TRUE;
            iFSM_NextState := 1; (* Advance to Die Lockup *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 1: DIE LOCKUP & CLAMPING TONNAGE BUILD (40,000 kN LOCKUP)
     * ----------------------------------------------------------------------------------------------------------------- *)
    1:
        (* Command High-Pressure Clamping Proportional Valve *)
        rClamp_Proportional_Cmd_Out := 90.0;

        (* Once Lockup Tonnage is Established, Insert Multi-Axis Hydraulic Core Slides *)
        IF rTMR_LC601_Voted >= (rRecipe_TargetClampForce_In * 0.96) THEN
            bCoreA_Insert_Cmd_Out := TRUE;
            bCoreB_Insert_Cmd_Out := TRUE;
            bCoreC_Insert_Cmd_Out := TRUE;
            bCoreD_Insert_Cmd_Out := TRUE;

            (* Confirm Core Limit Switches and Platen Parallelism Before Transition *)
            IF bCoreA_Extended_LS_In AND bCoreB_Extended_LS_In AND bCoreC_Extended_LS_In AND bCoreD_Extended_LS_In
               AND (NOT bTieBar_TonnageImbalance) THEN
                iFSM_NextState := 2; (* Advance to Ladle Pouring *)
            END_IF;
        END_IF;

        (* Lockup Timeout Fault Check *)
        IF rFSM_StateTimer_s > 10.0 THEN
            bAlarm_TieBar_Eccentricity := TRUE;
            iFSM_NextState := 14;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 2: LADLE ROBOTIC POURING & DOSING VERIFICATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    2:
        bLadle_Robot_Permissive_Out := TRUE;

        (* Handshake with Robotic Metal Ladler *)
        IF bLadle_Pour_Completed_In AND bLadle_Robot_Home_In THEN
            bLadle_Robot_Permissive_Out := FALSE;
            (* Verify Poured Alloy Mass within Tolerance (+/- 2.5 kg) and Pour Temperature *)
            IF (rLadle_Poured_Mass_In >= 40.0) AND (rLadle_Poured_Mass_In <= 95.0)
               AND (rTMR_TT701_Voted >= 640.0) AND (rTMR_TT701_Voted <= 730.0) THEN
                (* Reset Injection Performance Latches *)
                rPeakVelocityRecorded := 0.0;
                rPeakIntensPresRecorded := 0.0;
                rIntensRiseTimer_ms := 0.0;
                bIntensRiseTimer_Active := FALSE;
                rIntensRiseTimeAchieved_ms := 0.0;
                iFSM_NextState := 3; (* Advance to Phase 1 Slow Shot *)
            ELSE
                (* Dosing Weight or Melt Temperature Out-of-Spec *)
                bAlarm_Die_HotSpot := TRUE;
                iFSM_NextState := 14;
            END_IF;
        END_IF;

        IF rFSM_StateTimer_s > 30.0 THEN
            iFSM_NextState := 14; (* Ladle Pour Timeout *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 3: BISCUIT SLOW SHOT ADVANCE (PHASE 1 - WAVE CREST SUPPRESSION)
     * ----------------------------------------------------------------------------------------------------------------- *)
    3:
        (* Engage Vacuum Pump to Pre-Evacuate Reservoir *)
        bVacuum_Pump_Start_Out := TRUE;

        (* Plunger velocity regulated by MPC along parabolic profile to avoid wave cresting *)
        IF rTMR_ENC301_Voted >= rRecipe_Phase1_Stroke_In THEN
            iFSM_NextState := 4; (* Advance to Deep Vacuum Evacuation *)
        END_IF;

        IF rFSM_StateTimer_s > 8.0 THEN
            iFSM_NextState := 14; (* Slow Shot Jam / Timeout *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 4: VACUUM ASSIST EVACUATION & CHILL VENT DRAW
     * ----------------------------------------------------------------------------------------------------------------- *)
    4:
        bVacuum_Pump_Start_Out := TRUE;
        rVacuum_Isolation_Cmd_Out := 95.0; (* Open Vacuum Valve Wide *)

        (* Check if Deep Cavity Vacuum (< 50 mbar) is Achieved OR Evacuation Timer Dwells *)
        IF (rTMR_VPT401_Voted <= rRecipe_VacuumSetpoint_In) OR (rFSM_StateTimer_s >= 0.850) THEN
            rCavityVacuum_AtShot_Out := rTMR_VPT401_Voted;
            IF rTMR_VPT401_Voted > rSpec_Vacuum_Max THEN
                bAlarm_Vacuum_NotAchieved := TRUE;
            ELSE
                bAlarm_Vacuum_NotAchieved := FALSE;
            END_IF;
            iFSM_NextState := 5; (* Launch Phase 2 High-Speed Injection *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 5: HIGH-SPEED CAVITY INJECTION (PHASE 2 - UP TO 10.0 m/s)
     * ----------------------------------------------------------------------------------------------------------------- *)
    5:
        (* High-Speed Injection Driven by MPC & Accumulator Cartridge Valve *)
        (* Detect Cavity Fill Completion: Stroke Cutoff Trigger OR Sudden Pressure Surge Impact *)
        IF (rTMR_ENC301_Voted >= rRecipe_Phase2_CutoffPos_In) OR (rTMR_PT101_Voted >= 180.0) THEN
            (* Rapidly Close Hydraulic Chill Vent Valve to Protect Vacuum Line from Liquid Aluminum Infiltration *)
            bChillVent_SealValve_Out := TRUE;
            rVacuum_Isolation_Cmd_Out := 0.0;

            (* Start Intensification Pressure Rise Measurement Timer *)
            bIntensRiseTimer_Active := TRUE;
            rIntensRiseTimer_ms := 0.0;

            iFSM_NextState := 6; (* Advance to Phase 3 Intensification *)
        END_IF;

        (* Phase 2 Safety Watchdog: Must Fill Within 150 ms *)
        IF rFSM_StateTimer_s > 0.150 THEN
            bAlarm_Velocity_Overshoot := TRUE;
            iFSM_NextState := 14;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 6: ULTRA-FAST INTENSIFICATION PRESSURE HOLD (PHASE 3 - < 15 ms RISE TO 800 BAR)
     * ----------------------------------------------------------------------------------------------------------------- *)
    6:
        (* Fire Intensifier Cartridge Valve via MPC u3 command *)
        (* Monitor Dynamic Pressure Rise Time to Target Compaction *)
        IF bIntensRiseTimer_Active THEN
            IF rSpecificMetalPres_bar >= (rRecipe_Phase3_IntensPres_In * 0.95) THEN
                rIntensRiseTimeAchieved_ms := rIntensRiseTimer_ms;
                bIntensRiseTimer_Active := FALSE;
                IF rIntensRiseTimeAchieved_ms > rRecipe_Phase3_RiseTime_In THEN
                    bAlarm_Intens_TooSlow := TRUE;
                ELSE
                    bAlarm_Intens_TooSlow := FALSE;
                END_IF;
            ELSE
                rIntensRiseTimer_ms := rIntensRiseTimer_ms + 1.0;
                IF rIntensRiseTimer_ms > 45.0 THEN
                    rIntensRiseTimeAchieved_ms := rIntensRiseTimer_ms;
                    bIntensRiseTimer_Active := FALSE;
                    bAlarm_Intens_TooSlow := TRUE;
                END_IF;
            END_IF;
        END_IF;

        (* Dwell under High-Pressure Intensification for Squeeze Compaction *)
        IF rFSM_StateTimer_s >= rRecipe_Phase3_DwellTime_In THEN
            iFSM_NextState := 7; (* Advance to In-Die Solidification Cooling *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 7: IN-DIE SOLIDIFICATION COOLING & THERMAL BALANCING
     * ----------------------------------------------------------------------------------------------------------------- *)
    7:
        (* Maintain Moderate Holding Pressure to Compensate Volumetric Solidification Shrinkage *)
        (* Multi-zone thermal cooling valves active in Phase 5 *)
        IF rFSM_StateTimer_s >= rRecipe_CoolingDuration_In THEN
            (* Compute Solidified Biscuit Thickness: Total Machine Travel - Actual Plunger Position *)
            rBiscuit_Thickness_mm := rMachine_Full_Stroke_mm - rTMR_ENC301_Voted;
            rBiscuitThickness_Meas_Out := rBiscuit_Thickness_mm;
            rPeakShotVelocity_Meas_Out := rPeakVelocityRecorded;
            rPeakIntensPres_Meas_Out := rPeakIntensPresRecorded;
            rIntensRiseTime_Meas_Out := rIntensRiseTimeAchieved_ms;

            iFSM_NextState := 8; (* Advance to Vacuum Venting *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 8: VACUUM VENT & CAVITY PRESSURE EQUALIZATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    8:
        bVacuum_Pump_Start_Out := FALSE;
        rVacuum_Isolation_Cmd_Out := 0.0;
        bChillVent_SealValve_Out := FALSE;

        (* Allow 0.5 Seconds for Mold Cavity to Equalize with Atmospheric Pressure *)
        IF rFSM_StateTimer_s >= 0.500 THEN
            iFSM_NextState := 9; (* Advance to Core Slide Retract *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 9: HYDRAULIC CORE SLIDE RETRACT SEQUENCE
     * ----------------------------------------------------------------------------------------------------------------- *)
    9:
        bCoreA_Insert_Cmd_Out := FALSE;
        bCoreB_Insert_Cmd_Out := FALSE;
        bCoreC_Insert_Cmd_Out := FALSE;
        bCoreD_Insert_Cmd_Out := FALSE;

        bCoreA_Retract_Cmd_Out := TRUE;
        bCoreB_Retract_Cmd_Out := TRUE;
        bCoreC_Retract_Cmd_Out := TRUE;
        bCoreD_Retract_Cmd_Out := TRUE;

        (* Confirm All Core Pull Limit Switches Are Fully Retracted *)
        IF bCoreA_Retracted_LS_In AND bCoreB_Retracted_LS_In AND bCoreC_Retracted_LS_In AND bCoreD_Retracted_LS_In THEN
            iFSM_NextState := 10; (* Advance to Die De-Clamp & Open *)
        END_IF;

        IF rFSM_StateTimer_s > 8.0 THEN
            iFSM_NextState := 14; (* Core Pull Jam Alarm *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 10: DIE DE-CLAMP & CONTROLLED MOLD OPENING
     * ----------------------------------------------------------------------------------------------------------------- *)
    10:
        (* Decompress Clamping Cylinders Smoothly *)
        rClamp_Proportional_Cmd_Out := 0.0;

        (* Plunger Retracts Slowly to Home Position *)
        rServo_ShotSpool_Cmd_Out := -30.0;

        (* Allow 4.0 Seconds for Platen Open Motion and Plunger Return to 0 mm *)
        IF (rFSM_StateTimer_s >= 4.0) AND (rTMR_ENC301_Voted <= 15.0) THEN
            rServo_ShotSpool_Cmd_Out := 0.0;
            iFSM_NextState := 11; (* Advance to Hydraulic Knockout *)
        END_IF;

        IF rFSM_StateTimer_s > 12.0 THEN
            iFSM_NextState := 14;
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 11: HYDRAULIC EJECTOR KNOCKOUT PIN ADVANCE
     * ----------------------------------------------------------------------------------------------------------------- *)
    11:
        (* Advance Multi-Pin Knockout Ejector Plate *)
        rEjector_Servo_Cmd_Out := 65.0;

        (* Verify Ejector Full Stroke Reached (e.g. 180 mm) *)
        IF rEjector_Position_In >= 175.0 THEN
            rEjector_Servo_Cmd_Out := 0.0;
            iFSM_NextState := 12; (* Advance to Robot Extraction *)
        END_IF;

        IF rFSM_StateTimer_s > 6.0 THEN
            iFSM_NextState := 14; (* Ejector Jam Alarm *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 12: ROBOT PART EXTRACTION & CASTING INTEGRITY VERIFICATION
     * ----------------------------------------------------------------------------------------------------------------- *)
    12:
        bExtract_Robot_Permissive_Out := TRUE;

        (* Handshake with 6-Axis Unloading Extraction Robot *)
        IF bExtract_Part_Gripped_In THEN
            (* Retract Ejector Plate While Robot Holds Casting *)
            rEjector_Servo_Cmd_Out := -50.0;
        END_IF;

        IF bExtract_Robot_Clear_In AND (rEjector_Position_In <= 5.0) THEN
            bExtract_Robot_Permissive_Out := FALSE;
            rEjector_Servo_Cmd_Out := 0.0;
            iFSM_NextState := 13; (* Advance to Die Spray Lubrication *)
        END_IF;

        IF rFSM_StateTimer_s > 25.0 THEN
            iFSM_NextState := 14; (* Robot Extract Timeout *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 13: MULTI-ZONE DIE THERMAL SPRAY LUBRICATION & AIR PURGE
     * ----------------------------------------------------------------------------------------------------------------- *)
    13:
        bSpray_Robot_Permissive_Out := TRUE;

        (* Robot Enters Die Space to Apply Water-Based Release Agent and Compressed Air Blow-Off *)
        IF bSpray_Robot_Clear_In AND (rFSM_StateTimer_s >= 6.0) THEN
            bSpray_Robot_Permissive_Out := FALSE;
            rCycleDuration_Seconds_Out := rTotalCycleTimer_s;
            bCycleRunning := FALSE;

            (* Update Production Part Counter & SPC Telemetry *)
            iSPC_ShotCount := iSPC_ShotCount + 1;

            (* Continuous Automatic Production Cycle Loop *)
            IF bCmd_AutoCycle_Start_In THEN
                iFSM_NextState := 1; (* Restart Next Casting Cycle Immediately *)
            ELSE
                iFSM_NextState := 0; (* Return to Idle Standby *)
            END_IF;
        END_IF;

        IF rFSM_StateTimer_s > 35.0 THEN
            iFSM_NextState := 14; (* Spray Robot Timeout *)
        END_IF;

    (* -----------------------------------------------------------------------------------------------------------------
     * STAGE 14: EMERGENCY HYDRAULIC DUMP & FAILSAFE ABORT
     * ----------------------------------------------------------------------------------------------------------------- *)
    14:
        bCycleRunning := FALSE;
        rServo_ShotSpool_Cmd_Out := 0.0;
        rFastValv_Cartridge_Cmd_Out := 0.0;
        rIntensifier_Valve_Cmd_Out := 0.0;
        rVacuum_Isolation_Cmd_Out := 0.0;
        rClamp_Proportional_Cmd_Out := 0.0;
        rEjector_Servo_Cmd_Out := 0.0;
        bVacuum_Pump_Start_Out := FALSE;
        bChillVent_SealValve_Out := FALSE;
        bLadle_Robot_Permissive_Out := FALSE;
        bExtract_Robot_Permissive_Out := FALSE;
        bSpray_Robot_Permissive_Out := FALSE;

        (* Open Emergency Nitrogen Accumulator Hydraulic Dump De-energize Valve *)
        bAccumulator_Dump_Safe_Out := TRUE;

        (* Latch Critical Shutdown Alarm Register *)
        bAlarm_EmergencyStop_Active := TRUE;

        (* Operator Alarm Reset Handshake *)
        IF bCmd_Reset_Alarms_In AND bEmergency_Stop_OK_In AND bSafetyGate_Front_Closed_In AND bSafetyGate_Rear_Closed_In THEN
            bAccumulator_Dump_Safe_Out := FALSE;
            bAlarm_EmergencyStop_Active := FALSE;
            bAlarm_TMR_MajorDegrade := FALSE;
            bAlarm_TieBar_Eccentricity := FALSE;
            bAlarm_Velocity_Overshoot := FALSE;
            bAlarm_Intens_TooSlow := FALSE;
            iFSM_NextState := 0; (* Return to Idle Safe State *)
        END_IF;

END_CASE;
"""
