# ammonia_refrigeration_builder/build_st_phases_4_to_6.py

def get_phases_4_to_6():
    return """(* ==================================================================================================================== *)
(* PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                               *)
(* ==================================================================================================================== *)

(* Update Operational Timers *)
rFSM_StateStepTimer_sec := rFSM_StateStepTimer_sec + rCycleTime_dt_sec;
IF rComp1_AntiRecycleTimer_sec > 0.0 THEN
    rComp1_AntiRecycleTimer_sec := MAX(0.0, rComp1_AntiRecycleTimer_sec - rCycleTime_dt_sec);
END_IF;
IF rComp2_AntiRecycleTimer_sec > 0.0 THEN
    rComp2_AntiRecycleTimer_sec := MAX(0.0, rComp2_AntiRecycleTimer_sec - rCycleTime_dt_sec);
END_IF;
IF rComp3_AntiRecycleTimer_sec > 0.0 THEN
    rComp3_AntiRecycleTimer_sec := MAX(0.0, rComp3_AntiRecycleTimer_sec - rCycleTime_dt_sec);
END_IF;

(* Cumulative Run Hour Accumulators *)
IF bComp1_RunningFeedback THEN
    rComp1_CumulativeRunHours := rComp1_CumulativeRunHours + (rCycleTime_dt_sec / 3600.0);
END_IF;
IF bComp2_RunningFeedback THEN
    rComp2_CumulativeRunHours := rComp2_CumulativeRunHours + (rCycleTime_dt_sec / 3600.0);
END_IF;
IF bComp3_RunningFeedback THEN
    rComp3_CumulativeRunHours := rComp3_CumulativeRunHours + (rCycleTime_dt_sec / 3600.0);
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* EMERGENCY OVERRIDE INTERLOCK CHECK: IMMEDIATE FAULT TRANSITION TO EMERGENCY VENTILATION & SCRUBBER                   *)
(* -------------------------------------------------------------------------------------------------------------------- *)
IF (NOT bEmergencyStopCircuit_NC) OR 
   (NOT bMachineryRoomFireAlarm_NC) OR 
   (rVoted_AmbientNH3_ppm >= rAlarmTrip_NH3_Critical_ppm) OR
   (dwAlarmWord_Critical <> 16#00000000) THEN
    iFSM_State := FSM_STATE_EMERGENCY_VENT_SCRUB;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------- *)
(* FINITE STATE MACHINE STATE EVALUATION & STEP EXECUTION                                                               *)
(* -------------------------------------------------------------------------------------------------------------------- *)
CASE iFSM_State OF

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 0: INITIALIZATION & COLD-BOOT SYSTEM HEALTH CHECKS                                                         *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_INITIALIZE_SYS:
        (* Ensure all compressor contactors are de-energized *)
        bComp1_StartCommand := FALSE;
        bComp2_StartCommand := FALSE;
        bComp3_StartCommand := FALSE;
        rComp1_SlideValve_Command_Pct := 0.0;
        rComp2_SlideValve_Command_Pct := 0.0;
        rComp3_SlideValve_Command_Pct := 0.0;
        rComp1_VFD_SpeedCommand_Hz := 0.0;
        bPreLubeOilPump_Command := FALSE;
        rEconomizer_EEV_Opening_Pct := 0.0;

        (* Verify liquid ammonia levels and lube oil inventory *)
        IF (LT_OIL_SEPARATOR_LEVEL >= 35.0) AND 
           (LT_SUCTION_ACCUMULATOR_LEVEL <= 65.0) AND
           bMasterSystemEnable AND 
           bEmergencyStopCircuit_NC AND 
           bMachineryRoomFireAlarm_NC THEN

            (* Turn on oil sump immersion heater if oil temperature is below minimum pre-lube threshold *)
            IF TT_OIL_SEPARATOR_SUMP < rAlarmTrip_OilTemp_LL_degC THEN
                rOilSumpHeater_DutyCycle_Pct := 100.0;
            ELSE
                rOilSumpHeater_DutyCycle_Pct := 0.0;
                (* Advance to Pre-Lube Circulation once oil is warm enough *)
                IF rFSM_StateStepTimer_sec >= 5.0 THEN
                    iFSM_State := FSM_STATE_PRE_LUBE_CIRCULATION;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 1: PRE-LUBE CIRCULATION & OIL DIFFERENTIAL PRESSURE PRIMING                                                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_PRE_LUBE_CIRCULATION:
        bPreLubeOilPump_Command := TRUE;

        (* Modulate oil sump immersion heater to achieve 40 deg C starting temperature *)
        IF TT_OIL_SEPARATOR_SUMP < 40.0 THEN
            rOilSumpHeater_DutyCycle_Pct := 80.0;
        ELSE
            rOilSumpHeater_DutyCycle_Pct := 0.0;
        END_IF;

        (* Verify positive oil differential pressure building across twin-screw bearings *)
        IF (rVoted_OilDiffPressure_bar >= 2.20) AND 
           (TT_OIL_SEPARATOR_SUMP >= 30.0) AND 
           (rFSM_StateStepTimer_sec >= 15.0) THEN
            iFSM_State := FSM_STATE_STANDBY_READY;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

        (* Timeout Fault: Pre-lube pump failed to establish differential pressure *)
        IF rFSM_StateStepTimer_sec >= 60.0 AND rVoted_OilDiffPressure_bar < 2.0 THEN
            dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000020;
            iFSM_State := FSM_STATE_INITIALIZE_SYS;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 2: STANDBY READY (MONITORING SUCTION PRESSURE & PULL-DOWN DEMAND)                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_STANDBY_READY:
        bPreLubeOilPump_Command := FALSE;
        rComp1_VFD_SpeedCommand_Hz := 0.0;
        rComp1_SlideValve_Command_Pct := 0.0;

        (* Maintain oil temperature in standby readiness *)
        IF TT_OIL_SEPARATOR_SUMP < 42.0 THEN
            rOilSumpHeater_DutyCycle_Pct := 50.0;
        ELSE
            rOilSumpHeater_DutyCycle_Pct := 0.0;
        END_IF;

        (* Evaluate Refrigeration Demand: Suction pressure exceeds setpoint + start deadband *)
        IF bMasterSystemEnable AND bAutomaticModeSelect THEN
            IF (rVoted_SuctionPressure_bar >= (rSet_SuctionPressure_Target_bar + 0.20)) AND 
               (rComp1_AntiRecycleTimer_sec <= 0.0) THEN
                iFSM_State := FSM_STATE_LEAD_COMP_SOFT_START;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 3: LEAD COMPRESSOR SOFT-START & VFD RAMP-UP (15% UNLOADED INITIALIZATION)                                  *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_LEAD_COMP_SOFT_START:
        (* Ensure auxiliary lube pump is active during initial rotor breakaway acceleration *)
        bPreLubeOilPump_Command := TRUE;
        bComp1_StartCommand := TRUE;
        rComp1_SlideValve_Command_Pct := 15.0; (* Unloaded Start Stroke *)
        rComp1_Vi_Command := 2.6;              (* Low Vi setting to minimize starting torque *)

        (* Ramp VFD from 0 to minimum operating frequency 30.0 Hz *)
        IF rFSM_StateStepTimer_sec < 8.0 THEN
            rComp1_VFD_SpeedCommand_Hz := (rFSM_StateStepTimer_sec / 8.0) * 30.0;
        ELSE
            rComp1_VFD_SpeedCommand_Hz := 30.0;
        END_IF;

        (* Confirm compressor is running and oil pressure transferred to internal injection *)
        IF (rFSM_StateStepTimer_sec >= 12.0) AND bComp1_RunningFeedback THEN
            IF rVoted_OilDiffPressure_bar >= 2.50 THEN
                bPreLubeOilPump_Command := FALSE; (* Disengage auxiliary pre-lube pump *)
                iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 4: BASE LOAD REGULATION (LEAD COMPRESSOR VFD & SLIDE MODULATION VIA MPC)                                   *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_BASE_LOAD_REGULATION:
        bPreLubeOilPump_Command := FALSE;
        rOilSumpHeater_DutyCycle_Pct := 0.0;

        (* Actuator Commands driven directly by Phase 3 MPC Optimizations *)
        rComp1_SlideValve_Command_Pct := vecU[1];
        rComp1_VFD_SpeedCommand_Hz    := vecU[2];
        rComp1_Vi_Command             := rOptimumVi_Ratio;

        (* Staging Up Evaluation: Lead compressor fully loaded for sustained duration *)
        IF (rVoted_SuctionPressure_bar > (rSet_SuctionPressure_Target_bar + 0.30)) AND 
           (rComp1_SlideValve_Feedback >= 90.0) AND 
           (rComp1_VFD_ActualSpeed_Hz >= 58.0) THEN
            rStageUpDelayTimer_sec := rStageUpDelayTimer_sec + rCycleTime_dt_sec;
            IF (rStageUpDelayTimer_sec >= 120.0) AND (rComp2_AntiRecycleTimer_sec <= 0.0) THEN
                iFSM_State := FSM_STATE_LAG_STAGE_UP_SEQUENCE;
                rFSM_StateStepTimer_sec := 0.0;
                rStageUpDelayTimer_sec := 0.0;
            END_IF;
        ELSE
            rStageUpDelayTimer_sec := MAX(0.0, rStageUpDelayTimer_sec - rCycleTime_dt_sec);
        END_IF;

        (* Economizer Integration Evaluation *)
        IF bEconomizerSubcoolingPermissive AND (rCompPressureRatio >= 3.80) THEN
            iFSM_State := FSM_STATE_ECONOMIZER_SUBCOOL_ACTIVE;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

        (* Floating Head Condenser Modulation *)
        iFSM_State := FSM_STATE_FLOATING_CONDENSING_CTRL;

        (* Low Load Standby Transition *)
        IF (rVoted_SuctionPressure_bar < (rSet_SuctionPressure_Target_bar - 0.30)) AND 
           (rComp1_SlideValve_Feedback <= 20.0) AND 
           (rComp1_VFD_ActualSpeed_Hz <= 32.0) THEN
            rStageDownDelayTimer_sec := rStageDownDelayTimer_sec + rCycleTime_dt_sec;
            IF rStageDownDelayTimer_sec >= 180.0 THEN
                iFSM_State := FSM_STATE_CONTROLLED_DECEL_STANDBY;
                rFSM_StateStepTimer_sec := 0.0;
                rStageDownDelayTimer_sec := 0.0;
            END_IF;
        ELSE
            rStageDownDelayTimer_sec := MAX(0.0, rStageDownDelayTimer_sec - rCycleTime_dt_sec);
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 5: LAG COMPRESSOR STAGE-UP SEQUENCE (COMPRESSOR 2 INITIALIZATION)                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_LAG_STAGE_UP_SEQUENCE:
        (* Run pre-lube pump to prime Compressor 2 bearings *)
        bPreLubeOilPump_Command := TRUE;
        rComp2_SlideValve_Command_Pct := 0.0; (* Unloaded Start *)
        rComp2_Vi_Command := 2.8;

        IF rFSM_StateStepTimer_sec >= 8.0 THEN
            bComp2_StartCommand := TRUE;
            IF bComp2_RunningFeedback AND (rFSM_StateStepTimer_sec >= 15.0) THEN
                bPreLubeOilPump_Command := FALSE;
                iFSM_State := FSM_STATE_MULTI_COMP_COORDINATION;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 6: MULTI-COMPRESSOR COORDINATION & LOAD SHARING VIA MPC                                                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_MULTI_COMP_COORDINATION:
        bComp1_StartCommand := TRUE;
        bComp2_StartCommand := TRUE;

        (* Lead Comp 1 trims load via VFD, Lag Comp 2 takes base load via Slide Valve *)
        rComp1_SlideValve_Command_Pct := vecU[1];
        rComp1_VFD_SpeedCommand_Hz    := vecU[2];
        rComp2_SlideValve_Command_Pct := vecU[3];
        rComp1_Vi_Command             := rOptimumVi_Ratio;
        rComp2_Vi_Command             := rOptimumVi_Ratio;

        (* Stage-Down Condition: Both compressors lightly loaded *)
        IF (rVoted_SuctionPressure_bar <= (rSet_SuctionPressure_Target_bar - 0.20)) AND 
           (rComp1_VFD_ActualSpeed_Hz <= 35.0) AND 
           (rComp2_SlideValve_Feedback <= 30.0) THEN
            rStageDownDelayTimer_sec := rStageDownDelayTimer_sec + rCycleTime_dt_sec;
            IF rStageDownDelayTimer_sec >= 120.0 THEN
                iFSM_State := FSM_STATE_LAG_STAGE_DOWN_SEQUENCE;
                rFSM_StateStepTimer_sec := 0.0;
                rStageDownDelayTimer_sec := 0.0;
            END_IF;
        ELSE
            rStageDownDelayTimer_sec := MAX(0.0, rStageDownDelayTimer_sec - rCycleTime_dt_sec);
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 7: ECONOMIZER SUBCOOLING ACTIVE (FLASH VESSEL & EEV MODULATION)                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_ECONOMIZER_SUBCOOL_ACTIVE:
        (* Stepper EEV modulated via MPC Output vecU[4] *)
        rEconomizer_EEV_Opening_Pct := vecU[4];

        (* Verify economizer port pressure is safe: must be between suction and discharge *)
        IF (rVoted_EconomizerPressure_bar <= (rVoted_SuctionPressure_bar + 0.80)) OR
           (rVoted_EconomizerPressure_bar >= (rVoted_CondenserPressure_bar - 1.50)) THEN
            (* Pressure inversion risk: close EEV *)
            rEconomizer_EEV_Opening_Pct := 0.0;
        END_IF;

        (* Check Defrost Requests *)
        IF bZone1_DefrostRequest OR bZone2_DefrostRequest OR bZone3_DefrostRequest OR bZone4_DefrostRequest THEN
            iFSM_State := FSM_STATE_DEFROST_PUMP_DOWN;
            rFSM_StateStepTimer_sec := 0.0;
        ELSE
            iFSM_State := FSM_STATE_FLOATING_CONDENSING_CTRL;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 8: FLOATING CONDENSING PRESSURE CONTROL (TRACKING WET-BULB + APPROACH)                                     *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_FLOATING_CONDENSING_CTRL:
        (* Fan Bank Speed driven by MPC Output vecU[5] *)
        rCondenser_FanBank_Speed_Pct := vecU[5];

        (* Evaporative Sump Spray Pump Staging Logic *)
        IF rCondenser_FanBank_Speed_Pct >= 60.0 THEN
            bCondenser_SprayPump1_Command := TRUE;
        ELSIF rCondenser_FanBank_Speed_Pct <= 40.0 THEN
            bCondenser_SprayPump1_Command := FALSE;
        END_IF;

        IF rCondenser_FanBank_Speed_Pct >= 85.0 THEN
            bCondenser_SprayPump2_Command := TRUE;
        ELSIF rCondenser_FanBank_Speed_Pct <= 70.0 THEN
            bCondenser_SprayPump2_Command := FALSE;
        END_IF;

        (* Condenser Sump Freeze Protection *)
        IF TT_CONDENSER_SUMP_WATER <= 4.0 THEN
            rCondenser_FanBank_Speed_Pct := 15.0; (* Minimum speed *)
            bCondenser_SprayPump1_Command := FALSE;
            bCondenser_SprayPump2_Command := FALSE;
        END_IF;

        (* Check Defrost Scheduling *)
        IF bZone1_DefrostRequest OR bZone2_DefrostRequest OR bZone3_DefrostRequest OR bZone4_DefrostRequest THEN
            iFSM_State := FSM_STATE_DEFROST_PUMP_DOWN;
            rFSM_StateStepTimer_sec := 0.0;
        ELSIF bComp2_RunningFeedback THEN
            iFSM_State := FSM_STATE_MULTI_COMP_COORDINATION;
        ELSE
            iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 9: EVAPORATOR DEFROST PUMP-DOWN (COIL EVACUATION PRIOR TO HOT GAS)                                         *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_DEFROST_PUMP_DOWN:
        (* Identify which zone requested defrost and close liquid feed *)
        IF bZone1_DefrostRequest THEN
            iDefrostZoneActive := 1;
            bZone1_LiquidSupplyValve := FALSE; (* Shut liquid supply *)
            bZone1_SuctionStopValve := TRUE;   (* Keep suction valve open to evacuate *)
            IF (PT_ZONE1_COIL_PRESSURE <= 1.20) OR (rFSM_StateStepTimer_sec >= 240.0) THEN
                bZone1_SuctionStopValve := FALSE; (* Close suction stop valve before hot gas *)
                iFSM_State := FSM_STATE_DEFROST_HOT_GAS_FEED;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        ELSIF bZone2_DefrostRequest THEN
            iDefrostZoneActive := 2;
            bZone2_LiquidSupplyValve := FALSE;
            bZone2_SuctionStopValve := TRUE;
            IF (PT_ZONE2_COIL_PRESSURE <= 1.20) OR (rFSM_StateStepTimer_sec >= 240.0) THEN
                bZone2_SuctionStopValve := FALSE;
                iFSM_State := FSM_STATE_DEFROST_HOT_GAS_FEED;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        ELSIF bZone3_DefrostRequest THEN
            iDefrostZoneActive := 3;
            bZone3_LiquidSupplyValve := FALSE;
            bZone3_SuctionStopValve := TRUE;
            IF (PT_ZONE3_COIL_PRESSURE <= 1.20) OR (rFSM_StateStepTimer_sec >= 240.0) THEN
                bZone3_SuctionStopValve := FALSE;
                iFSM_State := FSM_STATE_DEFROST_HOT_GAS_FEED;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        ELSIF bZone4_DefrostRequest THEN
            iDefrostZoneActive := 4;
            bZone4_LiquidSupplyValve := FALSE;
            bZone4_SuctionStopValve := TRUE;
            IF (PT_ZONE4_COIL_PRESSURE <= 1.20) OR (rFSM_StateStepTimer_sec >= 240.0) THEN
                bZone4_SuctionStopValve := FALSE;
                iFSM_State := FSM_STATE_DEFROST_HOT_GAS_FEED;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        ELSE
            iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 10: DEFROST HOT GAS INJECTION & CONDENSATE RETURN (FROST MELTING)                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_DEFROST_HOT_GAS_FEED:
        CASE iDefrostZoneActive OF
            1:
                bZone1_HotGasSupplyValve := TRUE;
                IF (PT_ZONE1_COIL_PRESSURE >= rSet_DefrostSupplyPressure_bar) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostMaxDuration_sec) THEN
                    bZone1_HotGasSupplyValve := FALSE;
                    iFSM_State := FSM_STATE_DEFROST_BLEED_REPRESS;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            2:
                bZone2_HotGasSupplyValve := TRUE;
                IF (PT_ZONE2_COIL_PRESSURE >= rSet_DefrostSupplyPressure_bar) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostMaxDuration_sec) THEN
                    bZone2_HotGasSupplyValve := FALSE;
                    iFSM_State := FSM_STATE_DEFROST_BLEED_REPRESS;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            3:
                bZone3_HotGasSupplyValve := TRUE;
                IF (PT_ZONE3_COIL_PRESSURE >= rSet_DefrostSupplyPressure_bar) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostMaxDuration_sec) THEN
                    bZone3_HotGasSupplyValve := FALSE;
                    iFSM_State := FSM_STATE_DEFROST_BLEED_REPRESS;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            4:
                bZone4_HotGasSupplyValve := TRUE;
                IF (PT_ZONE4_COIL_PRESSURE >= rSet_DefrostSupplyPressure_bar) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostMaxDuration_sec) THEN
                    bZone4_HotGasSupplyValve := FALSE;
                    iFSM_State := FSM_STATE_DEFROST_BLEED_REPRESS;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
        END_CASE;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 11: DEFROST SOFT EQUALIZATION BLEED-DOWN & COIL RE-PRESSURIZATION                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_DEFROST_BLEED_REPRESS:
        CASE iDefrostZoneActive OF
            1:
                bZone1_SoftBleedValve := TRUE;
                (* Bleed down high pressure before opening main suction stop valve to prevent water hammer *)
                IF (PT_ZONE1_COIL_PRESSURE <= (rVoted_SuctionPressure_bar + 0.40)) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostSoftRepressTime_sec) THEN
                    bZone1_SoftBleedValve := FALSE;
                    bZone1_SuctionStopValve := TRUE;
                    bZone1_LiquidSupplyValve := TRUE;
                    iDefrostZoneActive := 0;
                    iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            2:
                bZone2_SoftBleedValve := TRUE;
                IF (PT_ZONE2_COIL_PRESSURE <= (rVoted_SuctionPressure_bar + 0.40)) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostSoftRepressTime_sec) THEN
                    bZone2_SoftBleedValve := FALSE;
                    bZone2_SuctionStopValve := TRUE;
                    bZone2_LiquidSupplyValve := TRUE;
                    iDefrostZoneActive := 0;
                    iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            3:
                bZone3_SoftBleedValve := TRUE;
                IF (PT_ZONE3_COIL_PRESSURE <= (rVoted_SuctionPressure_bar + 0.40)) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostSoftRepressTime_sec) THEN
                    bZone3_SoftBleedValve := FALSE;
                    bZone3_SuctionStopValve := TRUE;
                    bZone3_LiquidSupplyValve := TRUE;
                    iDefrostZoneActive := 0;
                    iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
            4:
                bZone4_SoftBleedValve := TRUE;
                IF (PT_ZONE4_COIL_PRESSURE <= (rVoted_SuctionPressure_bar + 0.40)) OR 
                   (rFSM_StateStepTimer_sec >= rSet_DefrostSoftRepressTime_sec) THEN
                    bZone4_SoftBleedValve := FALSE;
                    bZone4_SuctionStopValve := TRUE;
                    bZone4_LiquidSupplyValve := TRUE;
                    iDefrostZoneActive := 0;
                    iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
                    rFSM_StateStepTimer_sec := 0.0;
                END_IF;
        END_CASE;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 12: LAG COMPRESSOR STAGE-DOWN SEQUENCE (CONTROLLED UNLOAD & STOP)                                          *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_LAG_STAGE_DOWN_SEQUENCE:
        (* Unload Compressor 2 slide valve to 0% *)
        rComp2_SlideValve_Command_Pct := 0.0;

        (* Transfer load to Lead Compressor 1 *)
        rComp1_VFD_SpeedCommand_Hz := MIN(60.0, rComp1_VFD_ActualSpeed_Hz + 10.0);

        IF (rComp2_SlideValve_Feedback <= 5.0) OR (rFSM_StateStepTimer_sec >= 20.0) THEN
            bComp2_StartCommand := FALSE;
            rComp2_AntiRecycleTimer_sec := 900.0; (* 15 Minute Anti-Recycle Protection *)
            iFSM_State := FSM_STATE_BASE_LOAD_REGULATION;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 13: CONTROLLED SYSTEM DECELERATION & STANDBY GLIDE-DOWN                                                    *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_CONTROLLED_DECEL_STANDBY:
        (* Glide down compressor speeds to unloaded minimum *)
        rComp1_SlideValve_Command_Pct := 15.0;
        rComp1_VFD_SpeedCommand_Hz := 30.0;
        rEconomizer_EEV_Opening_Pct := 0.0;

        IF rFSM_StateStepTimer_sec >= 15.0 THEN
            bComp1_StartCommand := FALSE;
            bPreLubeOilPump_Command := TRUE; (* Run post-lube cycle for bearing thermal dissipate *)
            rComp1_AntiRecycleTimer_sec := 900.0;

            IF rFSM_StateStepTimer_sec >= 75.0 THEN
                bPreLubeOilPump_Command := FALSE;
                iFSM_State := FSM_STATE_STANDBY_READY;
                rFSM_StateStepTimer_sec := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 14: EMERGENCY TOXIC AMMONIA VENTILATION & ACID SCRUBBER MITIGATION                                         *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    FSM_STATE_EMERGENCY_VENT_SCRUB:
        (* Immediate Emergency Trip of All Rotating Machinery *)
        bComp1_StartCommand := FALSE;
        bComp2_StartCommand := FALSE;
        bComp3_StartCommand := FALSE;
        rComp1_SlideValve_Command_Pct := 0.0;
        rComp2_SlideValve_Command_Pct := 0.0;
        rComp3_SlideValve_Command_Pct := 0.0;
        rComp1_VFD_SpeedCommand_Hz := 0.0;
        bPreLubeOilPump_Command := FALSE;
        rEconomizer_EEV_Opening_Pct := 0.0;
        rOilSumpHeater_DutyCycle_Pct := 0.0;

        (* Shut High-Pressure Liquid Supply and All Evaporator Feeds *)
        bEmergencyLiquidLineKingValveShut := TRUE;
        bZone1_LiquidSupplyValve := FALSE;
        bZone2_LiquidSupplyValve := FALSE;
        bZone3_LiquidSupplyValve := FALSE;
        bZone4_LiquidSupplyValve := FALSE;
        bZone1_HotGasSupplyValve := FALSE;
        bZone2_HotGasSupplyValve := FALSE;
        bZone3_HotGasSupplyValve := FALSE;
        bZone4_HotGasSupplyValve := FALSE;

        (* Engage Life Safety Mitigation Systems *)
        bEmergencyVentilationFan1 := TRUE;
        bEmergencyVentilationFan2 := TRUE;
        bEmergencyScrubberCircPump := TRUE;
        bAudibleVisualHornStrobeAlarm := TRUE;

        (* Latch Critical Safety Alarm in ISA-18.2 First-Out Register *)
        IF NOT bFirstOutLatched THEN
            dwFirstOut_Alarm := 16#00000080; (* NH3 Toxic Gas Emergency Scrubber Trip *)
            bFirstOutLatched := TRUE;
        END_IF;

        (* Recovery Permissive: Requires ambient ammonia to drop below 20 ppm and manual engineer reset *)
        IF (rVoted_AmbientNH3_ppm <= 20.0) AND 
           bEmergencyStopCircuit_NC AND 
           bMachineryRoomFireAlarm_NC AND 
           bAcknowledgeFaultReset THEN
            bEmergencyVentilationFan1 := FALSE;
            bEmergencyVentilationFan2 := FALSE;
            bEmergencyScrubberCircPump := FALSE;
            bEmergencyLiquidLineKingValveShut := FALSE;
            bAudibleVisualHornStrobeAlarm := FALSE;
            iFSM_State := FSM_STATE_INITIALIZE_SYS;
            rFSM_StateStepTimer_sec := 0.0;
        END_IF;

    ELSE
        (* Failsafe default fall-through *)
        iFSM_State := FSM_STATE_INITIALIZE_SYS;
        rFSM_StateStepTimer_sec := 0.0;
END_CASE;

(* Update Output Current State *)
iFSM_CurrentState := iFSM_State;
"""
