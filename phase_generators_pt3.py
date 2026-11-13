# phase_generators_pt3.py
# Phase 5: Dynamic V/P Transfer Point Decoupling Logic
# Phase 6: Deterministic 14-Stage Production Finite State Machine (FSM)

def generate_phase5():
    return """
(* ==================================================================================================== *)
(* PHASE 5: DYNAMIC V/P (VELOCITY-TO-PRESSURE) TRANSFER POINT DECOUPLING LOGIC                           *)
(* Multi-Criteria Decoupling Matrix:                                                                    *)
(*   Criterion A: Linear Screw Stroke Threshold s_screw <= s_VP (sub-0.10 mm precision window)         *)
(*   Criterion B: Direct Cavity 1 Piezoelectric Pressure Trigger P_cav1 >= P_VP_threshold               *)
(*   Criterion C: Real-Time Cavity 1 Pressure Derivative Peak d(P_cav1)/dt >= dP_threshold (< 0.5 ms)   *)
(*   Criterion D: Injection Nozzle Peak Overpressure Hydraulic Spike Limit P_nozzle >= 1,950 bar        *)
(*   Criterion E: Volumetric Injection Fill Maximum Time Watchdog Limit t_fill >= t_max_fill           *)
(* Bumpless Transfer Dynamics:                                                                          *)
(*   - Freezes instantaneous screw stroke, peak pressure, and elapsed filling duration into memory.     *)
(*   - Decouples injection servo current loop from closed-loop linear velocity control to closed-loop   *)
(*     pressure regulation, preventing hydraulic shockwaves and optical stress birefringence.          *)
(* ==================================================================================================== *)

IF (nFsmState = 4 OR nFsmState = 5) AND NOT bVP_TransferTriggered THEN
    (* Criterion A: Optical Linear Scale Position Threshold *)
    bVP_Cond_Position := (rVoted_ST301_mm <= rSet_VP_PositionThreshold);

    (* Criterion B: Direct Quartz Piezoelectric Cavity Pressure *)
    bVP_Cond_CavityPressure := (rVoted_PT201_bar >= rSet_VP_CavityPressureThreshold) AND (rSet_VP_CavityPressureThreshold > 50.0);

    (* Criterion C: Real-Time Numerical Filtered Cavity Pressure Derivative Peak *)
    bVP_Cond_PressureDeriv := (rFiltered_dPCav_dt >= rSet_VP_PressureDerivThreshold) AND (rSet_VP_PressureDerivThreshold > 100.0);

    (* Criterion D: Injection Nozzle Head Overpressure Hydraulic Spike *)
    bVP_Cond_NozzleSpike := (rVoted_PT101_bar >= 1950.0);

    (* Criterion E: Volumetric Fill Watchdog Duration Timeout *)
    bVP_Cond_Timeout := (rFillStageStopwatch_sec >= rSet_MaxFillTimeLimit) AND (rSet_MaxFillTimeLimit > 0.50);

    (* Master V/P Switchover Evaluation *)
    IF bVP_Cond_Position OR bVP_Cond_CavityPressure OR bVP_Cond_PressureDeriv OR bVP_Cond_NozzleSpike OR bVP_Cond_Timeout THEN
        bVP_TransferTriggered := TRUE;

        (* Latch Switchover State Metrics *)
        rSwitchoverScrewPos_mm     := rVoted_ST301_mm;
        rSwitchoverPeakPress_bar   := rVoted_PT101_bar;
        rSwitchoverFillTime_sec    := rFillStageStopwatch_sec;
        rSwitchoverCavityPress_bar := rVoted_PT201_bar;

        (* Check for Fill Watchdog Timeout Warning *)
        IF bVP_Cond_Timeout AND NOT (bVP_Cond_Position OR bVP_Cond_CavityPressure) THEN
            bAlarmLatched_FillTimeout := TRUE;
        END_IF;

        (* Advance FSM State Machine Directly to V/P Deceleration Stage *)
        IF nFsmState = 4 THEN
            nFsmNextState := 5;
        END_IF;
    END_IF;
END_IF;
"""

def generate_phase6():
    return """
(* ==================================================================================================== *)
(* PHASE 6: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)                                 *)
(* Industrial Machine Sequence Architecture:                                                            *)
(*   State 0:  MACHINE_IDLE_AND_SAFETY_GATE_LOCK                                                        *)
(*   State 1:  MOLD_HIGH_SPEED_CLOSE_AND_LOW_PRESSURE_PROTECT                                           *)
(*   State 2:  TOGGLE_LOCKUP_AND_TONNAGE_BUILD (25,000 kN)                                              *)
(*   State 3:  INJECTION_CARRIAGE_FORWARD_AND_TOUCH                                                     *)
(*   State 4:  SERVO_INJECTION_PHASE1_FAST_FILL (to 95% volume)                                         *)
(*   State 5:  VP_TRANSFER_SWITCH_AND_DECELERATION                                                      *)
(*   State 6:  MULTI_STAGE_PACKING_AND_HOLDING_PRESSURE                                                 *)
(*   State 7:  GATE_FREEZE_OFF_ENDPOINT_DETECTION                                                       *)
(*   State 8:  SCREW_PLASTICIZING_ROTATION_AND_BACKPRESSURE                                             *)
(*   State 9:  MELT_DECOMPRESSION_SUCKBACK_SEQUENCE                                                     *)
(*   State 10: INJECTION_UNIT_RETRACT_CARRIAGE                                                          *)
(*   State 11: MOLD_OPEN_SOFT_DECELERATION_AND_INDEX                                                    *)
(*   State 12: MULTI_PIN_SERVO_EJECTION_AND_PART_DROP_CHECK                                             *)
(*   State 13: EMERGENCY_OVERPRESSURE_DIE_FLASH_TRIP                                                    *)
(* ==================================================================================================== *)

(* Stopwatch & Timers Accumulation *)
rStateElapsedTime_sec := rStateElapsedTime_sec + rCycleTime_sec;
IF nFsmState >= 1 AND nFsmState <= 12 THEN
    rTotalCycleTimer_sec := rTotalCycleTimer_sec + rCycleTime_sec;
END_IF;

(* Continuous Fast Emergency Interlock Supervision *)
IF NOT bEmergencyStop OR NOT bSafetyGateClosed OR NOT bRearSafetyGateClosed THEN
    nFsmNextState := 13; (* Emergency Trip *)
    IF nFirstOutAlarmCode = 0 THEN
        nFirstOutAlarmCode := 101; (* E-Stop / Safety Gate Open *)
    END_IF;
ELSIF rMoldSeparation_um >= rSp_PartingSeparation_HH_um THEN
    nFsmNextState := 13; (* Mold Flash Parting Line Separation Trip *)
    bAlarmLatched_FlashTrip := TRUE;
    IF nFirstOutAlarmCode = 0 THEN
        nFirstOutAlarmCode := 102; (* Mold Flash Deflection HH *)
    END_IF;
ELSIF rMaxTieBarDelta_kN >= rSp_TieBarImbalance_HH_kN THEN
    nFsmNextState := 13; (* Tie-Bar Asymmetry Imbalance Trip *)
    bAlarmLatched_TieBarTrip := TRUE;
    IF nFirstOutAlarmCode = 0 THEN
        nFirstOutAlarmCode := 103; (* Tie-Bar Strain Asymmetry HH *)
    END_IF;
ELSIF rVoted_PT101_bar >= rSp_NozzlePress_HH_bar THEN
    nFsmNextState := 13; (* Nozzle Melt Overpressure Trip *)
    bAlarmLatched_NozzlePressHH := TRUE;
    IF nFirstOutAlarmCode = 0 THEN
        nFirstOutAlarmCode := 104; (* Nozzle Pressure HH *)
    END_IF;
ELSIF rVoted_PT201_bar >= rSp_CavityPress_HH_bar THEN
    nFsmNextState := 13; (* Cavity Quartz Overpressure Trip *)
    bAlarmLatched_CavityPressHH := TRUE;
    IF nFirstOutAlarmCode = 0 THEN
        nFirstOutAlarmCode := 105; (* Cavity Pressure HH *)
    END_IF;
END_IF;

(* State First Scan Transition Detector *)
IF nFsmState <> nFsmNextState THEN
    nFsmState := nFsmNextState;
    rStateElapsedTime_sec := 0.0;
    bStateFirstScan := TRUE;
ELSE
    bStateFirstScan := FALSE;
END_IF;

nState_Current := nFsmState;

CASE nFsmState OF
    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 0: MACHINE IDLE & SAFETY GATE LOCK                                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    0:
        sFsmStateName := 'MACHINE_IDLE_AND_SAFETY_GATE_LOCK';
        rCmd_InjectionServoCurrent_pct := 0.0;
        rCmd_HoldingPressure_bar       := 0.0;
        rCmd_ScrewRotationSpeed_rpm    := 0.0;
        rCmd_BackpressureValve_bar     := 0.0;
        rCmd_MoldCoolingValve_pct      := 35.0;
        rCmd_ClampingToggleServo_pct   := 0.0;
        rCmd_EjectorServoSpeed_pct     := 0.0;
        rCmd_CarriageServoSpeed_pct    := 0.0;
        bCmd_HotRunnerValveGatesOpen   := FALSE;
        bCmd_PurgeGuardLock            := FALSE;
        bCycleCompletePulse            := FALSE;
        bGateFreezeOffAchieved         := FALSE;
        bVP_TransferTriggered          := FALSE;

        IF bAutoCycleStart AND bSafetyGateClosed AND bRearSafetyGateClosed AND bEmergencyStop AND
           bHydraulicPumpsReady AND bElectricServosReady THEN
            rTotalCycleTimer_sec := 0.0;
            nFsmNextState := 1;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 1: MOLD HIGH-SPEED CLOSE & LOW-PRESSURE MOLD PROTECT                                       *)
    (* ------------------------------------------------------------------------------------------------ *)
    1:
        sFsmStateName := 'MOLD_HIGH_SPEED_CLOSE_AND_LOW_PRESSURE_PROTECT';
        bCmd_PurgeGuardLock := TRUE;
        bCmd_HotRunnerValveGatesOpen := FALSE;
        
        (* Multi-Stage Mold Close Kinematics: High-speed traverse -> Mold Protect Zone *)
        IF rST_MoldPlatenPos > 65.0 THEN
            (* Fast Platen Traverse *)
            rCmd_ClampingToggleServo_pct := 75.0;
        ELSE
            (* Low-Pressure Mold Protect Zone (Last 65 mm): Reduced torque and velocity *)
            rCmd_ClampingToggleServo_pct := 18.0;

            (* Obstruction Protection: If platen stalls or time exceeds 2.5 s before touch *)
            IF rStateElapsedTime_sec > 2.50 THEN
                bAlarmLatched_MoldProtectTrip := TRUE;
                nFsmNextState := 13;
                IF nFirstOutAlarmCode = 0 THEN
                    nFirstOutAlarmCode := 106; (* Mold Protect Obstruction *)
                END_IF;
            END_IF;
        END_IF;

        (* Platen Face Touchdown Detected (Platen Pos <= 2.0 mm) *)
        IF rST_MoldPlatenPos <= 2.0 THEN
            nFsmNextState := 2;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 2: TOGGLE LOCKUP & HIGH TONNAGE BUILD (25,000 kN)                                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    2:
        sFsmStateName := 'TOGGLE_LOCKUP_AND_TONNAGE_BUILD';
        (* Servo Toggle Actuator Over-Center Camming & Lockup *)
        rCmd_ClampingToggleServo_pct := 95.0;

        (* Verify Tonnage Build and Tie-Bar Parallelism *)
        IF rVoted_WT401_kN >= (rSet_ClampTonnage_Target * 0.985) AND (rStateElapsedTime_sec >= 0.150) THEN
            IF rMaxTieBarDelta_kN <= rSp_TieBarImbalance_H_kN THEN
                nFsmNextState := 3;
            ELSE
                bAlarmWarn_TieBarImbalanceH := TRUE;
                (* Allow cycle if below critical HH trip limit *)
                IF rMaxTieBarDelta_kN < rSp_TieBarImbalance_HH_kN THEN
                    nFsmNextState := 3;
                ELSE
                    nFsmNextState := 13;
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 3: INJECTION CARRIAGE FORWARD & SPRUE TOUCH                                                *)
    (* ------------------------------------------------------------------------------------------------ *)
    3:
        sFsmStateName := 'INJECTION_CARRIAGE_FORWARD_AND_TOUCH';
        rCmd_CarriageServoSpeed_pct := 35.0; (* Forward Carriage Advance *)

        (* Nozzle-to-Sprue Seating Verification via Contact Load Cell *)
        IF rWT_NozzleContactForce >= 140.0 OR rST_CarriagePos <= 1.0 THEN
            rCmd_CarriageServoSpeed_pct := 5.0; (* Maintain Positive Seating Force *)
            bCmd_HotRunnerValveGatesOpen := TRUE; (* Open 4 Valve Gates *)
            
            IF rStateElapsedTime_sec >= 0.100 THEN
                nFsmNextState := 4;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 4: SERVO INJECTION PHASE 1 FAST VOLUMETRIC FILL (to 95% volume)                            *)
    (* ------------------------------------------------------------------------------------------------ *)
    4:
        sFsmStateName := 'SERVO_INJECTION_PHASE1_FAST_FILL';
        rFillStageStopwatch_sec := rFillStageStopwatch_sec + rCycleTime_sec;
        bCmd_HotRunnerValveGatesOpen := TRUE;

        (* Multi-Segment Closed-Loop Injection Velocity Profiling *)
        IF rVoted_ST301_mm > (rSet_PlasticizingStroke * 0.85) THEN
            (* Sub-Stage 1: Soft Start Through Submarine Gate (avoids optical jetting) *)
            rCmd_InjectionServoCurrent_pct := (rSet_InjectionSpeed_Stage1 / 350.0) * 100.0;
        ELSIF rVoted_ST301_mm > (rSet_VP_PositionThreshold + 15.0) THEN
            (* Sub-Stage 2: High-Speed Primary Cavity Volumetric Fill *)
            rCmd_InjectionServoCurrent_pct := (rSet_InjectionSpeed_Stage2 / 350.0) * 100.0;
        ELSIF rVoted_ST301_mm > (rSet_VP_PositionThreshold + 3.0) THEN
            (* Sub-Stage 3: Moderate Speed Fill *)
            rCmd_InjectionServoCurrent_pct := (rSet_InjectionSpeed_Stage3 / 350.0) * 100.0;
        ELSE
            (* Sub-Stage 4: Deceleration Approaching V/P Switch Window *)
            rCmd_InjectionServoCurrent_pct := (rSet_InjectionSpeed_Stage4 / 350.0) * 100.0;
        END_IF;

        (* Dynamic Cavity Pressure Peak Recording *)
        IF rVoted_PT201_bar > rPeakCavityPressHold_bar THEN
            rPeakCavityPressHold_bar := rVoted_PT201_bar;
        END_IF;

        (* V/P Transfer Evaluation handled continuously in Phase 5 *)
        IF bVP_TransferTriggered THEN
            nFsmNextState := 5;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 5: V/P TRANSFER SWITCHOVER & DYNAMIC DECELERATION                                          *)
    (* ------------------------------------------------------------------------------------------------ *)
    5:
        sFsmStateName := 'VP_TRANSFER_SWITCH_AND_DECELERATION';
        (* Ultra-Fast Bumpless Decoupling Phase (< 5 ms execution window) *)
        rCmd_InjectionServoCurrent_pct := 15.0;
        rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage1;

        (* Verify Pressure Profile & Immediate Handoff to Multi-Stage Pack *)
        IF rStateElapsedTime_sec >= 0.005 THEN
            nHoldingProfileSubStage := 1;
            rSubStageTimer_sec := 0.0;
            nFsmNextState := 6;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 6: MULTI-STAGE PACKING & DYNAMIC CAVITY PRESSURE HOLDING                                   *)
    (* ------------------------------------------------------------------------------------------------ *)
    6:
        sFsmStateName := 'MULTI_STAGE_PACKING_AND_HOLDING_PRESSURE';
        rPackStageStopwatch_sec := rPackStageStopwatch_sec + rCycleTime_sec;
        rSubStageTimer_sec := rSubStageTimer_sec + rCycleTime_sec;

        (* Continuous Minimum Screw Cushion Monitoring *)
        IF rVoted_ST301_mm < rMinCushionHold_mm THEN
            rMinCushionHold_mm := rVoted_ST301_mm;
        END_IF;

        (* 5-Stage Precision Optical Lens Holding Profile *)
        CASE nHoldingProfileSubStage OF
            1: (* Stage 1: High Initial Pack (1,100 bar) to compress melt wavefront *)
                rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage1;
                IF rSubStageTimer_sec >= rSet_HoldTime_Stage1 THEN
                    nHoldingProfileSubStage := 2;
                    rSubStageTimer_sec := 0.0;
                END_IF;

            2: (* Stage 2: Main Holding Pack (950 bar) for optical core density uniformity *)
                rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage2;
                IF rSubStageTimer_sec >= rSet_HoldTime_Stage2 THEN
                    nHoldingProfileSubStage := 3;
                    rSubStageTimer_sec := 0.0;
                END_IF;

            3: (* Stage 3: Density Compensation Pack (800 bar) counteracting thermal shrinkage *)
                rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage3;
                IF rSubStageTimer_sec >= rSet_HoldTime_Stage3 THEN
                    nHoldingProfileSubStage := 4;
                    rSubStageTimer_sec := 0.0;
                END_IF;

            4: (* Stage 4: Gate Freeze Pack (600 bar) preventing cavity backflow *)
                rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage4;
                IF rSubStageTimer_sec >= rSet_HoldTime_Stage4 THEN
                    nHoldingProfileSubStage := 5;
                    rSubStageTimer_sec := 0.0;
                END_IF;

            5: (* Stage 5: Residual Relaxation Pack (350 bar) reducing molded-in birefringence *)
                rCmd_HoldingPressure_bar := rSet_HoldPressure_Stage5;
                IF rSubStageTimer_sec >= rSet_HoldTime_Stage5 THEN
                    nFsmNextState := 7;
                END_IF;
        END_CASE;

        (* Gate Solidification Early Exit Check *)
        IF (x_state[7] >= (rGateHalfThickness_um * 0.98)) AND (rPackStageStopwatch_sec >= 4.0) THEN
            nFsmNextState := 7;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 7: GATE FREEZE-OFF ENDPOINT DETECTION & MASS ISOLATION                                     *)
    (* ------------------------------------------------------------------------------------------------ *)
    7:
        sFsmStateName := 'GATE_FREEZE_OFF_ENDPOINT_DETECTION';
        rCmd_HoldingPressure_bar := 0.0;
        bCmd_HotRunnerValveGatesOpen := FALSE; (* Close Valve Gates *)
        bGateFreezeOffAchieved := TRUE;

        (* Confirm Complete Mass Isolation & Launch Recovery *)
        IF rStateElapsedTime_sec >= 0.050 THEN
            rCoolingStopwatch_sec := 0.0;
            nFsmNextState := 8;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 8: SCREW PLASTICIZING ROTATION & PROPORTIONAL BACKPRESSURE                                 *)
    (* ------------------------------------------------------------------------------------------------ *)
    8:
        sFsmStateName := 'SCREW_PLASTICIZING_ROTATION_AND_BACKPRESSURE';
        rCoolingStopwatch_sec := rCoolingStopwatch_sec + rCycleTime_sec;

        (* Plasticizing Rotation Motor & Closed-Loop Backpressure Valve *)
        rCmd_ScrewRotationSpeed_rpm := rSet_PlasticizingRPM;
        rCmd_BackpressureValve_bar  := rSet_PlasticizingBackpress;

        (* Metering Shot Size Stroke Reached (ST_ScrewPos >= Target Stroke) *)
        IF rVoted_ST301_mm >= rSet_PlasticizingStroke THEN
            rCmd_ScrewRotationSpeed_rpm := 0.0;
            rCmd_BackpressureValve_bar  := 0.0;
            nFsmNextState := 9;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 9: MELT DECOMPRESSION SUCKBACK SEQUENCE                                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    9:
        sFsmStateName := 'MELT_DECOMPRESSION_SUCKBACK_SEQUENCE';
        rCoolingStopwatch_sec := rCoolingStopwatch_sec + rCycleTime_sec;

        (* Screw Linear Pullback without Rotation to Relieve Nozzle Pressure *)
        rCmd_InjectionServoCurrent_pct := -15.0;

        (* Target Suckback Stroke Reached (ST_ScrewPos >= PlasticizingStroke + DecompressionStroke) *)
        IF rVoted_ST301_mm >= (rSet_PlasticizingStroke + rSet_DecompressionStroke) THEN
            rCmd_InjectionServoCurrent_pct := 0.0;

            (* Wait for Remaining In-Mold Cooling Time to Expire *)
            IF rCoolingStopwatch_sec >= rSet_CoolingTime THEN
                nFsmNextState := 10;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 10: INJECTION UNIT RETRACT CARRIAGE                                                        *)
    (* ------------------------------------------------------------------------------------------------ *)
    10:
        sFsmStateName := 'INJECTION_UNIT_RETRACT_CARRIAGE';
        rCmd_CarriageServoSpeed_pct := -25.0; (* Retract Carriage *)

        (* Break Sprue Contact (Retract 50 mm) *)
        IF rST_CarriagePos >= 50.0 OR rStateElapsedTime_sec >= 0.800 THEN
            rCmd_CarriageServoSpeed_pct := 0.0;
            nFsmNextState := 11;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 11: MOLD OPEN SOFT DECELERATION & INDEX                                                    *)
    (* ------------------------------------------------------------------------------------------------ *)
    11:
        sFsmStateName := 'MOLD_OPEN_SOFT_DECELERATION_AND_INDEX';
        
        (* Multi-Segment Mold Open Kinematics: High-force break -> High speed -> Soft cushioning *)
        IF rST_MoldPlatenPos < 25.0 THEN
            (* High-Force Mold Breakaway Stage *)
            rCmd_ClampingToggleServo_pct := 40.0;
        ELSIF rST_MoldPlatenPos < (rSet_MoldOpenStroke - 80.0) THEN
            (* High-Speed Traverse Stroke *)
            rCmd_ClampingToggleServo_pct := 85.0;
        ELSE
            (* Soft Cushioning Deceleration to Open Stop Position *)
            rCmd_ClampingToggleServo_pct := 15.0;
        END_IF;

        (* Daylight Open Stroke Reached *)
        IF rST_MoldPlatenPos >= rSet_MoldOpenStroke THEN
            rCmd_ClampingToggleServo_pct := 0.0;
            nEjectorPulseCounter := 0;
            bEjectorStrokeForwardActive := TRUE;
            nFsmNextState := 12;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 12: MULTI-PIN SERVO EJECTION & PART DROP VERIFICATION                                      *)
    (* ------------------------------------------------------------------------------------------------ *)
    12:
        sFsmStateName := 'MULTI_PIN_SERVO_EJECTION_AND_PART_DROP_CHECK';

        (* Multi-Pulse Ejector Shaking Demolding Cycle *)
        IF bEjectorStrokeForwardActive THEN
            rCmd_EjectorServoSpeed_pct := 45.0; (* Advance Ejector Pins *)
            IF rST_EjectorPos >= rSet_EjectorStroke THEN
                bEjectorStrokeForwardActive := FALSE;
                nEjectorPulseCounter := nEjectorPulseCounter + 1;
            END_IF;
        ELSE
            rCmd_EjectorServoSpeed_pct := -45.0; (* Retract Ejector Pins *)
            IF rST_EjectorPos <= 1.0 THEN
                IF nEjectorPulseCounter < rSet_EjectorPulses THEN
                    bEjectorStrokeForwardActive := TRUE;
                END_IF;
            END_IF;
        END_IF;

        (* Verify Part Demolding via Optical Curtain or Robot Extraction Handshake *)
        IF (rST_EjectorPos <= 1.0) AND (nEjectorPulseCounter >= rSet_EjectorPulses) THEN
            IF bPartDropVerified OR bRobotTakeoutHandshake THEN
                rCmd_EjectorServoSpeed_pct := 0.0;
                bCycleCompletePulse := TRUE;

                (* Latch Cycle Production Monitored Parameters *)
                rMon_FillTime_sec           := rSwitchoverFillTime_sec;
                rMon_CycleTime_sec          := rTotalCycleTimer_sec;
                rMon_CushionPosition_mm     := rMinCushionHold_mm;
                rMon_PeakCavityPressure_bar := rPeakCavityPressHold_bar;

                (* Continuous Production Loop Check *)
                IF bAutoCycleStart AND NOT bAutoCycleStop THEN
                    nFsmNextState := 1; (* Start Next Mold Close Cycle *)
                ELSE
                    nFsmNextState := 0; (* Return to Idle Standby *)
                END_IF;
            END_IF;
        END_IF;

    (* ------------------------------------------------------------------------------------------------ *)
    (* STATE 13: EMERGENCY OVERPRESSURE & DIE FLASH SAFETY TRIP                                         *)
    (* ------------------------------------------------------------------------------------------------ *)
    13:
        sFsmStateName := 'EMERGENCY_OVERPRESSURE_DIE_FLASH_TRIP';
        (* Immediate Emergency De-energization of Injection Servos *)
        rCmd_InjectionServoCurrent_pct := 0.0;
        rCmd_HoldingPressure_bar       := 0.0;
        rCmd_ScrewRotationSpeed_rpm    := 0.0;
        rCmd_BackpressureValve_bar     := 0.0;
        rCmd_EjectorServoSpeed_pct     := 0.0;
        rCmd_CarriageServoSpeed_pct    := 0.0;
        bCmd_HotRunnerValveGatesOpen   := FALSE;
        
        (* Maintain Mold Clamping Tonnage to prevent molten resin explosive discharge *)
        rCmd_ClampingToggleServo_pct   := 15.0;
        rCmd_MoldCoolingValve_pct      := 100.0; (* Max Cooling to solidify escaping flash *)

        (* Manual Reset Pushbutton Evaluation *)
        IF bManualResetAlarms AND bSafetyGateClosed AND bRearSafetyGateClosed AND bEmergencyStop THEN
            bAlarmLatched_FlashTrip       := FALSE;
            bAlarmLatched_TieBarTrip      := FALSE;
            bAlarmLatched_NozzlePressHH   := FALSE;
            bAlarmLatched_CavityPressHH   := FALSE;
            bAlarmLatched_ClampTonnageHH  := FALSE;
            bAlarmLatched_ClampTonnageLL  := FALSE;
            bAlarmLatched_CushionLL       := FALSE;
            bAlarmLatched_FillTimeout     := FALSE;
            bAlarmLatched_MoldProtectTrip := FALSE;
            nFirstOutAlarmCode            := 0;
            nFsmNextState                 := 0;
        END_IF;

ELSE
    nFsmNextState := 13;
END_CASE;
"""
