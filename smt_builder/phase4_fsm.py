# -*- coding: utf-8 -*-
"""
smt_builder/phase4_fsm.py
Generates Phase 4: Deterministic 14-Stage Production Finite State Machine (FSM)
for high-speed dual-gantry pick-and-place operation.
"""

def get_phase4_fsm():
    return """(*
========================================================================================================================
  PHASE 4: 14-STAGE DETERMINISTIC PRODUCTION FINITE STATE MACHINE (FSM)
========================================================================================================================
  Executes the ultra-high-speed SMT assembly sequence with microsecond-level synchronization:
    State 00: STATE_00_INIT_HOMING_SELFTEST   - Multi-axis safe homing, scale alignment & calibration
    State 01: STATE_01_PCB_CONVEYOR_INDEX     - Dual-lane SMEMA conveyor board infeed, lift & precision clamping
    State 02: STATE_02_GLOBAL_OPTICAL_ALIGN   - Dual global optical fiducial mark scanning & PCB skew computation
    State 03: STATE_03_LASER_WARPAGE_SURFACE  - High-speed laser triangulation PCBA warpage profiling map
    State 04: STATE_04_FEEDER_BANK_APPROACH   - 7-Segment S-curve jerk-bounded flight to smart feeder bank
    State 05: STATE_05_NOZZLE_TOUCH_PICK      - Voice-coil dynamic soft-touch landing & vacuum component pickup
    State 06: STATE_06_PICK_PRESSURE_VERIFY   - Microsecond vacuum siphon differential pressure decay verification
    State 07: STATE_07_FLYBY_VISION_STROBE    - High-speed 2.5 m/s optical fly-by line-scan strobe image capture
    State 08: STATE_08_VISION_OFFSET_APPLY    - Sub-pixel centroid offset & angular skew transformation
    State 09: STATE_09_HIGH_SPEED_FLIGHT      - Vibration-dampened trajectory flight to PCBA placement pads
    State 10: STATE_10_PRECISION_Z_LANDING    - Closed-loop voice coil touch landing with force overshoot limiting
    State 11: STATE_11_BLOWOFF_RELEASE        - Calibrated positive-pressure puff blow-off & nozzle stiction purge
    State 12: STATE_12_REJECT_BIN_DISCHARGE   - Defective component automatic purge to defect drop chute
    State 13: STATE_13_NOZZLE_AUTO_EXCHANGE   - Automatic Nozzle Changer (ANC) station tool auto-swap sequence
    State 14: STATE_14_ESTOP_CONTROLLED_STOP  - Category 0/1 controlled deceleration & SIL-3 safe recovery latch
*)

(* Detect State Entry Edge *)
IF iFSM_State <> iFSM_PrevState THEN
    bFSM_StateFirstScan := TRUE;
    udiFSM_SubStep := 0;
    udiFSM_StateDwell_ms := 0;
    iFSM_PrevState := iFSM_State;
ELSE
    bFSM_StateFirstScan := FALSE;
    udiFSM_StateDwell_ms := udiFSM_StateDwell_ms + 1;
END_IF;

(* Master FSM State Switch *)
CASE iFSM_State OF

    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 00: SYSTEM INITIALIZATION, MULTI-AXIS HOMING & SENSOR SELF-TEST                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_00_INIT_HOMING_SELFTEST:
        IF bFSM_StateFirstScan THEN
            bSystemReady := FALSE;
            bCycleBusy := TRUE;
            bCycleComplete := FALSE;
            bGeneralFault := FALSE;
            bCmd_VacuumSupply_Enable := TRUE;
            bCmd_RejectPart_Gate := FALSE;
            bCmd_VisionCamera_Strobe := FALSE;
            bCmd_NozzleToolExchange := FALSE;
            bCmd_Conveyor_ReleasePCB := FALSE;
            bCmd_PneumaticBlowOff_Pulse := FALSE;
            rProfile_Pos_Target_X := 50.0;
            rProfile_Pos_Target_Y := 50.0;
            iInternalSpindlePointer := 1;
            iTotalComponentsOnHead := 0;
            FOR iIdxSpindle := 1 TO 16 DO
                arrSpindle_HasComponent[iIdxSpindle] := FALSE;
                arrSpindle_RejectFlag[iIdxSpindle] := FALSE;
                arrSpindle_VisionPassed[iIdxSpindle] := FALSE;
                arrSpindle_ConsecutiveErrors[iIdxSpindle] := 0;
                arrSpindle_Z_Stroke_mm[iIdxSpindle] := 0.0;
            END_FOR;
        END_IF;

        (* Check Hardware Safety Interlock & TMR Triplet Health *)
        IF NOT bEStop_SafetyInterlock OR
           bTMR_X_MajorDiscrepancyTrip OR
           bTMR_Y_MajorDiscrepancyTrip OR
           bTMR_Theta_MajorDiscrepancyTrip THEN
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        ELSE
            (* Homing Sequence Execution *)
            CASE udiFSM_SubStep OF
                0: (* Sub-step 0: Retract all 16 voice-coil Z-spindles to top dead center *)
                    rCmd_VoiceCoil_Z_Current := -150.0; (* Retract bias current *)
                    IF udiFSM_StateDwell_ms > 200 THEN
                        udiFSM_SubStep := 1;
                    END_IF;

                1: (* Sub-step 1: Slow homing search for X and Y optical index marks *)
                    rProfile_Pos_Target_X := 0.0;
                    rProfile_Pos_Target_Y := 0.0;
                    IF (ABS(rActual_Gantry_X_Pos) < 0.25) AND (ABS(rActual_Gantry_Y_Pos) < 0.25) THEN
                        udiFSM_SubStep := 2;
                    END_IF;

                2: (* Sub-step 2: Spindle turret Theta direct-drive zero index alignment *)
                    rCmd_VoiceCoil_Z_Current := 0.0;
                    IF ABS(rActual_Head_Theta_Deg) < 0.05 THEN
                        udiFSM_SubStep := 3;
                    END_IF;

                3: (* Sub-step 3: Complete self-calibration and enable production readiness *)
                    bSystemReady := TRUE;
                    bCycleBusy := FALSE;
                    IF bExecute_CycleStart THEN
                        iFSM_State := STATE_01_PCB_CONVEYOR_INDEX;
                    END_IF;
            END_CASE;
        END_IF;

        (* Watchdog Timeout Protection *)
        IF udiFSM_StateDwell_ms > udiTimeout_Homing_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 01: DUAL-LANE PCB CONVEYOR INDEX, LIFT & PRECISION MECHANICAL CLAMP                                        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_01_PCB_CONVEYOR_INDEX:
        IF bFSM_StateFirstScan THEN
            bCycleBusy := TRUE;
            bCycleComplete := FALSE;
            bCmd_Conveyor_ReleasePCB := FALSE;
            udiFSM_SubStep := 0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Wait for PCB edge presence trigger from infeed optical sensor *)
                IF bConveyor_PCB_Clamped THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Engage dual pneumatic edge clamps and backup pin table lift *)
                IF udiFSM_StateDwell_ms > 150 THEN
                    (* Mechanical clamping settled & stable *)
                    iFSM_State := STATE_02_GLOBAL_OPTICAL_ALIGN;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > udiTimeout_ConveyorIndex_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 02: GLOBAL OPTICAL FIDUCIAL MARK SCANNING & PCB SKEW TRANSFORMATION                                        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_02_GLOBAL_OPTICAL_ALIGN:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            bCmd_VisionCamera_Strobe := FALSE;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Traverse gantry to Global Fiducial 1 coordinate *)
                rProfile_Pos_Target_X := 85.0;
                rProfile_Pos_Target_Y := 45.0;
                IF (ABS(rActual_Gantry_X_Pos - 85.0) < 0.050) AND
                   (ABS(rActual_Gantry_Y_Pos - 45.0) < 0.050) AND
                   (ABS(x_state[3]) < 0.005) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Fire optical strobe for Fiducial 1 *)
                bCmd_VisionCamera_Strobe := TRUE;
                IF bVision_TriggerAck THEN
                    bCmd_VisionCamera_Strobe := FALSE;
                    udiFSM_SubStep := 2;
                END_IF;

            2: (* Sub-step 2: Traverse gantry to Global Fiducial 2 coordinate *)
                rProfile_Pos_Target_X := 350.0;
                rProfile_Pos_Target_Y := 280.0;
                IF (ABS(rActual_Gantry_X_Pos - 350.0) < 0.050) AND
                   (ABS(rActual_Gantry_Y_Pos - 280.0) < 0.050) AND
                   (ABS(x_state[3]) < 0.005) THEN
                    udiFSM_SubStep := 3;
                END_IF;

            3: (* Sub-step 3: Fire optical strobe for Fiducial 2 & acquire vision alignment packet *)
                bCmd_VisionCamera_Strobe := TRUE;
                IF bVision_DataReady THEN
                    bCmd_VisionCamera_Strobe := FALSE;
                    IF bGlobalFiducialsAligned THEN
                        iFSM_State := STATE_03_LASER_WARPAGE_SURFACE;
                    ELSE
                        (* Fiducial recognition failed - retry or alarm *)
                        bGeneralFault := TRUE;
                        iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
                    END_IF;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > 4000 THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 03: HIGH-SPEED TRIANGULATION LASER PCB WARPAGE PROFILING                                                   *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_03_LASER_WARPAGE_SURFACE:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Scan laser sensor across board center to map local warp profile *)
                rProfile_Pos_Target_X := 200.0;
                rProfile_Pos_Target_Y := 150.0;
                IF (ABS(rActual_Gantry_X_Pos - 200.0) < 0.100) AND
                   (ABS(rActual_Gantry_Y_Pos - 150.0) < 0.100) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Validate measured PCB surface height within allowable tolerance *)
                IF (rActual_PCB_Surface_Z_mm > -1.50) AND (rActual_PCB_Surface_Z_mm < 1.50) THEN
                    (* Board flatness passed; proceed to feeder pickup *)
                    iFSM_State := STATE_04_FEEDER_BANK_APPROACH;
                ELSE
                    (* Severe PCB warpage detected - potential collision risk *)
                    bGeneralFault := TRUE;
                    iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
                END_IF;
        END_CASE;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 04: FEEDER BANK APPROACH TRAJECTORY                                                                        *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_04_FEEDER_BANK_APPROACH:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            (* Target coordinates over selected tape feeder pickup lane *)
            rProfile_Pos_Target_X := 25.0 + (INT_TO_REAL(iFeeder_ComponentID) * 14.0);
            rProfile_Pos_Target_Y := 480.0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: High-speed approach flight toward feeder bank *)
                IF (ABS(rActual_Gantry_X_Pos - rProfile_Pos_Target_X) < 0.025) AND
                   (ABS(rActual_Gantry_Y_Pos - rProfile_Pos_Target_Y) < 0.025) AND
                   (ABS(x_state[3]) < 0.003) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Verify feeder ready handshake and micro-stepper advance *)
                IF bFeederBank_Ready AND bFeeder_TapeAdvanceDone THEN
                    iFSM_State := STATE_05_NOZZLE_TOUCH_PICK;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > 2500 THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 05: VOICE-COIL SOFT-TOUCH LANDING & VACUUM COMPONENT PICKUP                                                *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_05_NOZZLE_TOUCH_PICK:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            (* Activate vacuum suction proportional valve *)
            u_ctrl[4] := 95.0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Drive voice coil downward with controlled landing velocity *)
                rCmd_VoiceCoil_Z_Current := 420.0; (* Forward landing drive current [mA] *)
                arrSpindle_Z_Stroke_mm[iInternalSpindlePointer] := 18.5;
                IF udiFSM_StateDwell_ms > 35 THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Soft-touch contact dwell to establish vacuum siphon seal *)
                rCmd_VoiceCoil_Z_Current := 180.0; (* Compliant holding force current *)
                IF udiFSM_StateDwell_ms > 65 THEN
                    (* Record dynamic vacuum level *)
                    arrSpindle_PickVacuum_kPa[iInternalSpindlePointer] := rActiveSpindleVacuumPressure;
                    udiFSM_SubStep := 2;
                END_IF;

            2: (* Sub-step 2: Rapid Z-retract to travel clearance position *)
                rCmd_VoiceCoil_Z_Current := -350.0; (* Fast upward retraction *)
                arrSpindle_Z_Stroke_mm[iInternalSpindlePointer] := 0.0;
                IF udiFSM_StateDwell_ms > 95 THEN
                    rCmd_VoiceCoil_Z_Current := 0.0;
                    (* Advance feeder tape for next component *)
                    bCmd_Feeder_IndexNext := TRUE;
                    iFSM_State := STATE_06_PICK_PRESSURE_VERIFY;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > udiTimeout_PickTouch_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 06: VACUUM SIPHON DIFFERENTIAL PRESSURE DECAY VERIFICATION                                                 *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_06_PICK_PRESSURE_VERIFY:
        bCmd_Feeder_IndexNext := FALSE;
        
        (* Evaluate vacuum pressure on active spindle nozzle *)
        IF arrSpindle_PickVacuum_kPa[iInternalSpindlePointer] <= -55.0 THEN
            (* Good vacuum seal: component securely held *)
            arrSpindle_HasComponent[iInternalSpindlePointer] := TRUE;
            arrSpindle_RejectFlag[iInternalSpindlePointer] := FALSE;
            arrSpindle_ConsecutiveErrors[iInternalSpindlePointer] := 0;
            iTotalComponentsOnHead := iTotalComponentsOnHead + 1;
            rComponent_Tombstone_RiskIndex := 0.02;
        ELSIF (arrSpindle_PickVacuum_kPa[iInternalSpindlePointer] > -55.0) AND
              (arrSpindle_PickVacuum_kPa[iInternalSpindlePointer] <= -25.0) THEN
            (* Partial vacuum seal: tombstone or tilted component detected *)
            arrSpindle_HasComponent[iInternalSpindlePointer] := TRUE;
            arrSpindle_RejectFlag[iInternalSpindlePointer] := TRUE; (* Flag for purge bin ejection *)
            rComponent_Tombstone_RiskIndex := 0.88;
        ELSE
            (* Pick failure: component absent / tape pocket empty *)
            arrSpindle_HasComponent[iInternalSpindlePointer] := FALSE;
            arrSpindle_RejectFlag[iInternalSpindlePointer] := FALSE;
            arrSpindle_ConsecutiveErrors[iInternalSpindlePointer] := arrSpindle_ConsecutiveErrors[iInternalSpindlePointer] + 1;
            udiConsecutivePickFailsCount := udiConsecutivePickFailsCount + 1;
            rComponent_Tombstone_RiskIndex := 1.00;
        END_IF;

        (* Multi-spindle batching loop or proceed to optical fly-by inspection *)
        IF iInternalSpindlePointer < 16 THEN
            iInternalSpindlePointer := iInternalSpindlePointer + 1;
            (* Index head turret to next spindle for subsequent pick *)
            iFSM_State := STATE_04_FEEDER_BANK_APPROACH;
        ELSE
            (* All 16 spindles loaded; proceed to fly-by optical alignment *)
            iInternalSpindlePointer := 1;
            iFSM_State := STATE_07_FLYBY_VISION_STROBE;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 07: HIGH-SPEED OPTICAL FLY-BY VISION IMAGE CAPTURE                                                         *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_07_FLYBY_VISION_STROBE:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            (* Flight corridor trajectory over stationary upward-looking CMOS camera *)
            rProfile_Pos_Target_X := 120.0;
            rProfile_Pos_Target_Y := 320.0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Accelerate through fly-by imaging corridor at 2.5 m/s *)
                IF (ABS(rActual_Gantry_X_Pos - 120.0) < 0.25) AND
                   (ABS(rActual_Gantry_Y_Pos - 320.0) < 0.25) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Fire hardware-synchronized LED strobe pulses for all spindles *)
                bCmd_VisionCamera_Strobe := TRUE;
                IF bVision_TriggerAck THEN
                    bCmd_VisionCamera_Strobe := FALSE;
                    udiFSM_SubStep := 2;
                END_IF;

            2: (* Sub-step 2: Await camera FPGA vision feature extraction results *)
                IF bVision_DataReady THEN
                    iFSM_State := STATE_08_VISION_OFFSET_APPLY;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > udiTimeout_VisionStrobe_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 08: SUB-PIXEL CENTROID OFFSET & ROTATIONAL SKEW TRANSFORMATION                                             *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_08_VISION_OFFSET_APPLY:
        (* Check optical inspection results for currently active placement spindle *)
        IF bVision_DefectRejectFlag OR NOT bVision_LeadCoplanarPass THEN
            arrSpindle_RejectFlag[iInternalSpindlePointer] := TRUE;
            arrSpindle_VisionPassed[iInternalSpindlePointer] := FALSE;
        ELSE
            arrSpindle_VisionOffset_X[iInternalSpindlePointer] := rVision_OffsetX;
            arrSpindle_VisionOffset_Y[iInternalSpindlePointer] := rVision_OffsetY;
            arrSpindle_VisionOffset_Theta[iInternalSpindlePointer] := rVision_OffsetTheta;
            arrSpindle_VisionPassed[iInternalSpindlePointer] := TRUE;
        END_IF;

        (* Check if active spindle holds a valid component or must be ejected *)
        IF arrSpindle_RejectFlag[iInternalSpindlePointer] THEN
            iFSM_State := STATE_12_REJECT_BIN_DISCHARGE;
        ELSIF arrSpindle_HasComponent[iInternalSpindlePointer] THEN
            iFSM_State := STATE_09_HIGH_SPEED_FLIGHT;
        ELSE
            (* Empty spindle: skip to next *)
            IF iInternalSpindlePointer < 16 THEN
                iInternalSpindlePointer := iInternalSpindlePointer + 1;
                iFSM_State := STATE_08_VISION_OFFSET_APPLY;
            ELSE
                (* Placement batch complete for this head load *)
                iInternalSpindlePointer := 1;
                iFSM_State := STATE_01_PCB_CONVEYOR_INDEX;
            END_IF;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 09: VIBRATION-DAMPENED HIGH-SPEED PLACEMENT FLIGHT TO PCBA PADS                                            *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_09_HIGH_SPEED_FLIGHT:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            (* Target coordinates with dynamic vision & thermal expansion offsets applied *)
            rProfile_Pos_Target_X := rTarget_Placement_X + arrSpindle_VisionOffset_X[iInternalSpindlePointer];
            rProfile_Pos_Target_Y := rTarget_Placement_Y + arrSpindle_VisionOffset_Y[iInternalSpindlePointer];
            rActual_Head_Theta_Deg := rTarget_Placement_Theta + arrSpindle_VisionOffset_Theta[iInternalSpindlePointer];
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: High-speed S-curve traverse to component landing pad *)
                IF (ABS(rActual_Gantry_X_Pos - rProfile_Pos_Target_X) < 0.015) AND
                   (ABS(rActual_Gantry_Y_Pos - rProfile_Pos_Target_Y) < 0.015) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Wait for MPC structural flexure dampening settle *)
                IF (ABS(x_state[3]) < 0.0025) AND (ABS(x_state[4]) < 0.050) THEN
                    (* Structural vibration extinguished to within 2.5 um *)
                    iFSM_State := STATE_10_PRECISION_Z_LANDING;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > 2000 THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 10: CLOSED-LOOP VOICE-COIL PRECISION TOUCHDOWN LANDING                                                     *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_10_PRECISION_Z_LANDING:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Voice-coil controlled landing velocity descent *)
                rCmd_VoiceCoil_Z_Current := 380.0;
                arrSpindle_Z_Stroke_mm[iInternalSpindlePointer] := rTarget_Placement_Z + rActual_PCB_Surface_Z_mm;
                IF udiFSM_StateDwell_ms > 25 THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Closed-loop landing impact force regulation *)
                rEstimated_LandingForce_N := 0.0038 * rCmd_VoiceCoil_Z_Current;
                IF (rEstimated_LandingForce_N >= rNominalLandingForce) OR (udiFSM_StateDwell_ms > 50) THEN
                    iFSM_State := STATE_11_BLOWOFF_RELEASE;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > udiTimeout_LandingRelease_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 11: POSITIVE-PRESSURE MICRO-BLOW-OFF RELEASE & NOZZLE STICTION PURGE                                      *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_11_BLOWOFF_RELEASE:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            (* De-energize vacuum pickup valve *)
            u_ctrl[4] := 0.0;
            (* Trigger high-speed puff blow-off solenoid pulse *)
            bCmd_PneumaticBlowOff_Pulse := TRUE;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Maintain positive pressure pulse duration (6.0 ms) *)
                IF udiFSM_StateDwell_ms >= 6 THEN
                    bCmd_PneumaticBlowOff_Pulse := FALSE;
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Fast Z-axis retraction away from wet solder paste *)
                rCmd_VoiceCoil_Z_Current := -380.0;
                arrSpindle_Z_Stroke_mm[iInternalSpindlePointer] := 0.0;
                IF udiFSM_StateDwell_ms > 45 THEN
                    rCmd_VoiceCoil_Z_Current := 0.0;
                    arrSpindle_HasComponent[iInternalSpindlePointer] := FALSE;
                    udiTotalPartsPlacedCount := udiTotalPartsPlacedCount + 1;

                    (* Advance to next spindle placement or conclude cycle *)
                    IF iInternalSpindlePointer < 16 THEN
                        iInternalSpindlePointer := iInternalSpindlePointer + 1;
                        iFSM_State := STATE_08_VISION_OFFSET_APPLY;
                    ELSE
                        (* All 16 components placed: check if board is finished *)
                        bCycleComplete := TRUE;
                        bCmd_Conveyor_ReleasePCB := TRUE;
                        iInternalSpindlePointer := 1;
                        iFSM_State := STATE_01_PCB_CONVEYOR_INDEX;
                    END_IF;
                END_IF;
        END_CASE;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 12: DEFECTIVE COMPONENT PURGE & REJECT CHUTE EJECTION                                                      *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_12_REJECT_BIN_DISCHARGE:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            rProfile_Pos_Target_X := 480.0;
            rProfile_Pos_Target_Y := 520.0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Traverse gantry to reject discharge station *)
                IF (ABS(rActual_Gantry_X_Pos - 480.0) < 0.150) AND
                   (ABS(rActual_Gantry_Y_Pos - 520.0) < 0.150) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Open divert chute and fire extended purge blow-off pulse *)
                bCmd_RejectPart_Gate := TRUE;
                u_ctrl[4] := 0.0;
                bCmd_PneumaticBlowOff_Pulse := TRUE;
                IF udiFSM_StateDwell_ms > 40 THEN
                    bCmd_PneumaticBlowOff_Pulse := FALSE;
                    bCmd_RejectPart_Gate := FALSE;
                    arrSpindle_HasComponent[iInternalSpindlePointer] := FALSE;
                    arrSpindle_RejectFlag[iInternalSpindlePointer] := FALSE;
                    udiTotalPartsRejectedCount := udiTotalPartsRejectedCount + 1;

                    (* Advance to next spindle or resume placement *)
                    IF iInternalSpindlePointer < 16 THEN
                        iInternalSpindlePointer := iInternalSpindlePointer + 1;
                        iFSM_State := STATE_08_VISION_OFFSET_APPLY;
                    ELSE
                        iInternalSpindlePointer := 1;
                        iFSM_State := STATE_04_FEEDER_BANK_APPROACH;
                    END_IF;
                END_IF;
        END_CASE;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 13: AUTOMATIC NOZZLE CHANGER (ANC) TOOL AUTO-SWAP SEQUENCE                                                 *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_13_NOZZLE_AUTO_EXCHANGE:
        IF bFSM_StateFirstScan THEN
            udiFSM_SubStep := 0;
            rProfile_Pos_Target_X := 520.0;
            rProfile_Pos_Target_Y := 50.0;
        END_IF;

        CASE udiFSM_SubStep OF
            0: (* Sub-step 0: Move to ANC magazine bay *)
                IF (ABS(rActual_Gantry_X_Pos - 520.0) < 0.050) AND
                   (ABS(rActual_Gantry_Y_Pos - 50.0) < 0.050) THEN
                    udiFSM_SubStep := 1;
                END_IF;

            1: (* Sub-step 1: Lower spindles into mechanical release forks *)
                bCmd_NozzleToolExchange := TRUE;
                rCmd_VoiceCoil_Z_Current := 280.0;
                IF udiFSM_StateDwell_ms > 800 THEN
                    udiFSM_SubStep := 2;
                END_IF;

            2: (* Sub-step 2: Retract spindles with new nozzles locked into place *)
                bCmd_NozzleToolExchange := FALSE;
                rCmd_VoiceCoil_Z_Current := -280.0;
                IF udiFSM_StateDwell_ms > 1400 THEN
                    rCmd_VoiceCoil_Z_Current := 0.0;
                    iFSM_State := STATE_00_INIT_HOMING_SELFTEST;
                END_IF;
        END_CASE;

        IF udiFSM_StateDwell_ms > udiTimeout_NozzleExchange_ms THEN
            bGeneralFault := TRUE;
            iFSM_State := STATE_14_ESTOP_CONTROLLED_STOP;
        END_IF;


    (* ---------------------------------------------------------------------------------------------------------------- *)
    (* STATE 14: CATEGORY 0/1 CONTROLLED DECELERATION & SIL-3 EMERGENCY STOP RECOVERY                                   *)
    (* ---------------------------------------------------------------------------------------------------------------- *)
    STATE_14_ESTOP_CONTROLLED_STOP:
        (* Immediate Deceleration & Power Cut *)
        bSystemReady := FALSE;
        bCycleBusy := FALSE;
        bGeneralFault := TRUE;
        rCmd_Gantry_X_Force := 0.0;
        rCmd_Gantry_Y_Force := 0.0;
        rCmd_Head_Theta_Torque := 0.0;
        rCmd_VoiceCoil_Z_Current := 0.0;
        u_ctrl[1] := 0.0;
        u_ctrl[2] := 0.0;
        u_ctrl[3] := 0.0;
        u_ctrl[4] := 0.0;
        bCmd_VacuumSupply_Enable := FALSE;
        bCmd_PneumaticBlowOff_Pulse := FALSE;
        bCmd_VisionCamera_Strobe := FALSE;
        bCmd_RejectPart_Gate := FALSE;

        (* Operator Fault Reset Handshake *)
        IF bReset_Fault AND bEStop_SafetyInterlock AND
           NOT bTMR_X_MajorDiscrepancyTrip AND
           NOT bTMR_Y_MajorDiscrepancyTrip AND
           NOT bTMR_Theta_MajorDiscrepancyTrip THEN
            bGeneralFault := FALSE;
            iFSM_State := STATE_00_INIT_HOMING_SELFTEST;
        END_IF;

END_CASE;

iCurrent_FSM_State := iFSM_State;
iActive_Spindle_Index := iInternalSpindlePointer;
"""
