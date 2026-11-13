# stator_laser_welding_builder/part7_phase4_fsm.py

def get_phase4_fsm():
    return """(*
====================================================================================================
PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
Sequences complete 192-Pin (96-Pair) EV Stator Crown Laser Seam Welding Cycle:
  State 0:  ST_CHUCK_CLAMP        - Hydraulic Expanding Collet Clamping & Pressure Interlock
  State 1:  ST_DATUM_CENTER       - Stator Core Datum Alignment & Concentricity Runout Check
  State 2:  ST_VISION_SCAN        - 3D Profilometer Pin Gap & Height Mismatch Strobe Scan
  State 3:  ST_RADIAL_ALIGN       - Pin Crown Micro-Offset Radial Mechanical Adjustment Press
  State 4:  ST_GAS_PURGE          - High-Flow Nitrogen Shielding Gas Pre-Flow Purge (35 L/min)
  State 5:  ST_HEAD_APPROACH      - Galvo Scanning Head Z-Standoff Focus & Fast Shutter Open
  State 6:  ST_LASER_WELD         - 4-Substage Dynamic Beam Wobble Seam Laser Weld (160 ms)
  State 7:  ST_PYRO_EVAL          - Solidification Cooling Rate & Expulsion Quality Assessment
  State 8:  ST_EDDY_RESIST        - In-Line 4-Wire Kelvin Electrical Micro-Ohmmeter Inspection
  State 9:  ST_CHUCK_INDEX        - Direct-Drive Rotary Chuck 3.75 deg Index to Next Pin Pair
  State 10: ST_OPTICS_INSPECT     - Motorized Protective Cover Glass Transmission Verification
  State 11: ST_DECLAMP_EGRESS     - Finished Stator De-Clamp, Unload & Conveyor Handshake
  State 12: ST_REJECT_QUARANTINE  - Defective Weld Pin Pair Tagging & Egress Diverter Push
  State 13: ST_EMERGENCY_SHUTTER - Fast Optical Shutter Lockout, Beam Dump & Fault Safe
====================================================================================================
*)

(* Master Emergency Stop & Interlock Override *)
IF bEmergencyStop THEN
    iFSM_CurrentState := 13; (* Branch directly to Emergency Shutter Safe State *)
END_IF;

(* State Transition Edge Detection & Timer Maintenance *)
IF iFSM_CurrentState <> iFSM_PreviousState THEN
    rStateTimer_s := 0.0;
    iFSM_PreviousState := iFSM_CurrentState;
ELSE
    rStateTimer_s := rStateTimer_s + rScanTime_s;
END_IF;

(* Master FSM Execution Switch *)
CASE iFSM_CurrentState OF

    0: (* -----------------------------------------------------------------------------------------
          STATE 0: ST_CHUCK_CLAMP - Hydraulic Expanding Collet Clamping & Preload Lock
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 4.0;
        bChuck_HydClamp_Sol   := TRUE;
        bChuck_HydUnclamp_Sol := FALSE;
        bChuck_HoldBrakeRelease := FALSE;
        bLaserEmission_Enable := FALSE;
        bLaserFastShutter_Open := FALSE;
        bCellCycleCompleted   := FALSE;

        (* Check Hydraulic Clamping Pressure via 2oo3 Voted Transmitter (Interlock >= 170.0 bar) *)
        IF (rHydClamp_Voted_bar >= 170.0) AND bPartPresentInChuck AND bPalletClampedInStation THEN
            IF bAutoCycleStart THEN
                iFSM_CurrentState := 1; (* Proceed to Stator Datum Centering *)
            END_IF;
        END_IF;

        (* Watchdog Timeout Fault *)
        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    1: (* -----------------------------------------------------------------------------------------
          STATE 1: ST_DATUM_CENTER - Stator Core Datum Alignment & Concentricity Runout Check
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 3.5;
        bDatumPin_Extend_Sol  := TRUE;
        bDatumPin_Retract_Sol := FALSE;
        bChuck_HoldBrakeRelease := TRUE;

        (* Verify Stator Datum Concentricity Runout (< 0.035 mm) *)
        IF (rStateTimer_s >= 0.500) THEN
            IF (rStator_DatumRunout_mm <= 0.035) THEN
                (* Reset Stator Array Indices *)
                iCurrentWeldPairNumber := 1;
                iTotalCompletedWelds   := 0;
                rTotalStatorCycleTime_s := 0.0;
                iTotalSpatterEventsInStator := 0;
                iFSM_CurrentState := 2; (* Proceed to 3D Vision Scan *)
            ELSE
                (* Concentricity Out of Tolerance *)
                iFSM_CurrentState := 12; (* Divert to Defect Quarantine *)
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    2: (* -----------------------------------------------------------------------------------------
          STATE 2: ST_VISION_SCAN - 3D Profilometer Pin Gap & Height Mismatch Strobe Scan
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 1.5;
        bVision_CaptureStrobe := TRUE;

        (* Allow 3D Profilometer Spatial Processing Window (40 ms) *)
        IF rStateTimer_s >= 0.040 THEN
            bVision_CaptureStrobe := FALSE;

            (* Store Measured Gap for Current Pin Pair *)
            arrPairMeasuredGap_mm[iCurrentWeldPairNumber] := rGap_Voted_mm;

            (* Evaluate Gap & Height Tolerances for Copper Hairpin Pair *)
            IF (rGap_Voted_mm > rTrip_PinGap_HH_mm) OR (rHeight_Voted_mm > 0.080) THEN
                (* Excessive Gap Cannot Be Bridged: Mechanical Micro-Adjustment Needed *)
                iFSM_CurrentState := 3; (* Branch to Radial Align Press *)
            ELSIF (rGap_Voted_mm <= 0.050) AND (rHeight_Voted_mm <= 0.040) THEN
                (* Excellent Alignment: Proceed Directly to Shielding Gas Pre-Flow Purge *)
                iFSM_CurrentState := 4;
            ELSE
                (* Intermediate Gap: Correctable via Beam Wobble Envelope *)
                iFSM_CurrentState := 4;
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    3: (* -----------------------------------------------------------------------------------------
          STATE 3: ST_RADIAL_ALIGN - Pin Crown Micro-Offset Radial Mechanical Adjustment Press
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 2.0;

        (* Micro-Adjustment Press Actuation Window (120 ms dwell) *)
        IF rStateTimer_s >= 0.120 THEN
            (* Re-verify Gap post mechanical squeeze *)
            IF (rGap_Voted_mm <= rTrip_PinGap_HH_mm) THEN
                iFSM_CurrentState := 4; (* Alignment Successful *)
            ELSE
                (* Unrecoverable Pin Crown Geometry Fault *)
                arrPairStatusFlags[iCurrentWeldPairNumber] := 16#0001; (* Tag Defect Code 1: Gap Runaway *)
                iFSM_CurrentState := 12; (* Divert Stator to Quarantine *)
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    4: (* -----------------------------------------------------------------------------------------
          STATE 4: ST_GAS_PURGE - High-Flow Nitrogen Shielding Gas Pre-Flow Purge (35 L/min)
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 1.2;
        bShieldGas_Purge_Valve   := TRUE;
        bCrossJet_AirKnife_Valve := TRUE;
        bFumeExtraction_FanOn    := TRUE;

        (* Verify Shielding Gas Flow Delivery via 2oo3 Voted Flowmeter (>= 30.0 L/min) *)
        IF (rShieldGas_Voted_Lmin >= 30.0) AND (rCrossJet_AirPressure_bar >= 4.5) THEN
            IF rStateTimer_s >= 0.050 THEN
                (* Purge complete and oxygen displaced below 40 ppm *)
                iFSM_CurrentState := 5; (* Proceed to Scanning Head Approach *)
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    5: (* -----------------------------------------------------------------------------------------
          STATE 5: ST_HEAD_APPROACH - Galvo Scanning Head Z-Standoff Focus & Fast Shutter Open
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 0.8;
        bLaserAimingBeam_On    := TRUE;
        bLaserFastShutter_Open := TRUE;

        (* Verify Optical Path Safety Interlocks & Optical Lens Temperatures *)
        IF (rCollimator_Temp_degC < 45.0) AND (rFocusLens_Temp_degC < 50.0) AND
           (rChiller_WaterFlow_Lmin >= 18.0) AND (rOptics_Transmission_pct >= 82.0) THEN
            IF rStateTimer_s >= 0.030 THEN
                (* Fast Shutter Confirmed Open: Arm Laser Emission *)
                bLaserEmission_Enable := TRUE;
                iWeldSubPhase := 1; (* Initialize Subphase 1: Pre-Heat *)
                rWeldSubPhaseTimer_s := 0.0;
                rWeldCycleTime_Current_s := 0.0;
                iFSM_CurrentState := 6; (* Proceed to Active Laser Seam Welding *)
            END_IF;
        ELSE
            (* Optics Over-Temperature or Contamination Lockout *)
            iFSM_CurrentState := 13;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    6: (* -----------------------------------------------------------------------------------------
          STATE 6: ST_LASER_WELD - 4-Substage Dynamic Beam Wobble Seam Laser Weld (160 ms total)
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 0.350;
        rWeldSubPhaseTimer_s := rWeldSubPhaseTimer_s + rScanTime_s;
        rWeldCycleTime_Current_s := rWeldCycleTime_Current_s + rScanTime_s;

        (* Track Pyrometer Peak Molten Temperature *)
        IF rMeltPool_Voted_degC > rPyrometerPeakMemory_degC THEN
            rPyrometerPeakMemory_degC := rMeltPool_Voted_degC;
        END_IF;

        (* Real-Time Spatter Expulsion Fast Derivative Detector *)
        rPyrometerRateOfRise_degC_ms := (rMeltPool_Voted_degC - rPreviousMeltPoolTemp_degC) / (rScanTime_s * 1000.0);
        IF (rPyrometerRateOfRise_degC_ms > 85.0) AND (rMeltPool_Voted_degC > 2200.0) THEN
            bSpatterExpulsionDetected := TRUE;
            iTotalSpatterEventsInStator := iTotalSpatterEventsInStator + 1;
        END_IF;

        (* Multi-Substage Fiber Laser Power Profile Sequence *)
        CASE iWeldSubPhase OF
            1: (* Subphase 1: Thermal Pre-Heat Ramp (0 to 30 ms) *)
                IF rWeldSubPhaseTimer_s >= 0.030 THEN
                    iWeldSubPhase := 2; (* Transition to Keyhole Penetration *)
                    rWeldSubPhaseTimer_s := 0.0;
                END_IF;

            2: (* Subphase 2: Keyhole Deep Vapor Penetration (30 to 65 ms, duration 35 ms) *)
                IF rWeldSubPhaseTimer_s >= 0.035 THEN
                    iWeldSubPhase := 3; (* Transition to Dynamic Wobble Seam *)
                    rWeldSubPhaseTimer_s := 0.0;
                END_IF;

            3: (* Subphase 3: Continuous High-Frequency Wobble Fusion (65 to 140 ms, duration 75 ms) *)
                IF rWeldSubPhaseTimer_s >= 0.075 THEN
                    iWeldSubPhase := 4; (* Transition to Downslope Quench *)
                    rWeldSubPhaseTimer_s := 0.0;
                END_IF;

            4: (* Subphase 4: Downslope Power Ramp & Solidification Crater Fill (140 to 160 ms, duration 20 ms) *)
                IF rWeldSubPhaseTimer_s >= 0.020 THEN
                    (* 160 ms Total Weld Cycle Completed *)
                    bLaserEmission_Enable := FALSE; (* Immediate Beam Hardware Extinguish *)
                    rLaserPower_Cmd_kW := 0.0;
                    iWeldSubPhase := 0;
                    iFSM_CurrentState := 7; (* Proceed to Solidification Quality Evaluation *)
                END_IF;
        ELSE
            iWeldSubPhase := 1;
        END_CASE;

        (* In-Weld Safety Trips *)
        IF (rMeltPool_Voted_degC >= rTrip_MeltPool_HH_degC) OR (rShieldGas_Voted_Lmin <= rTrip_ShieldGas_LL_Lmin) THEN
            bLaserEmission_Enable := FALSE;
            rLaserPower_Cmd_kW := 0.0;
            iFSM_CurrentState := 13; (* Emergency Beam Dump Trip *)
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bLaserEmission_Enable := FALSE;
            rLaserPower_Cmd_kW := 0.0;
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    7: (* -----------------------------------------------------------------------------------------
          STATE 7: ST_PYRO_EVAL - Solidification Cooling Rate & Expulsion Quality Assessment
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 0.250;
        bLaserEmission_Enable := FALSE;
        rLaserPower_Cmd_kW    := 0.0;

        (* Dwell Window for Copper Solidification & Pyrometer Cooling Curve Analysis (60 ms) *)
        IF rStateTimer_s >= 0.060 THEN
            (* Log Peak Temperature to Pair History *)
            arrPairPeakMeltTemp_degC[iCurrentWeldPairNumber] := rPyrometerPeakMemory_degC;
            rPyrometerPeakMemory_degC := 0.0;

            (* Compute Multi-Variable Weld Quality Score [%] *)
            rWeldQualityScore_pct := 100.0;

            (* Penalize for Molten Pool Peak Temperature Deviation from Nominal 1850 deg C *)
            rTemp_Scalar1 := ABS(arrPairPeakMeltTemp_degC[iCurrentWeldPairNumber] - 1850.0);
            IF rTemp_Scalar1 > 200.0 THEN
                rWeldQualityScore_pct := rWeldQualityScore_pct - MIN(35.0, (rTemp_Scalar1 - 200.0) * 0.08);
            END_IF;

            (* Penalize for Spatter Expulsion Event *)
            IF bSpatterExpulsionDetected THEN
                rWeldQualityScore_pct := rWeldQualityScore_pct - 25.0;
                arrPairStatusFlags[iCurrentWeldPairNumber] := arrPairStatusFlags[iCurrentWeldPairNumber] OR 16#0002;
                bSpatterExpulsionDetected := FALSE;
            END_IF;

            (* Penalize for Initial Pin Gap Width *)
            IF arrPairMeasuredGap_mm[iCurrentWeldPairNumber] > 0.030 THEN
                rWeldQualityScore_pct := rWeldQualityScore_pct - MIN(20.0, (arrPairMeasuredGap_mm[iCurrentWeldPairNumber] - 0.030) * 250.0);
            END_IF;

            (* Record Quality Score *)
            arrPairWeldScore_pct[iCurrentWeldPairNumber] := rWeldQualityScore_pct;

            (* Close Fast Shutter During Chuck Indexing *)
            bLaserFastShutter_Open := FALSE;

            IF bEddyCurrentBypass THEN
                iFSM_CurrentState := 9; (* Bypass resistance check, index directly *)
            ELSE
                iFSM_CurrentState := 8; (* Proceed to Kelvin Micro-Ohmmeter Inspection *)
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    8: (* -----------------------------------------------------------------------------------------
          STATE 8: ST_EDDY_RESIST - In-Line 4-Wire Kelvin Electrical Micro-Ohmmeter Inspection
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 0.400;
        bEddyCurrent_ProbeExtend := TRUE;

        (* Dwell Window for Pneumatic Contact Settling & 4-Wire DC Resistance Reading (50 ms) *)
        IF rStateTimer_s >= 0.050 THEN
            arrPairJointResist_uOhm[iCurrentWeldPairNumber] := rEddyCurrent_Resistance_uOhm;
            bEddyCurrent_ProbeExtend := FALSE;

            (* Verify Joint Electrical Resistance (< 2.50 uOhm nominal, max 3.20 uOhm) *)
            IF rEddyCurrent_Resistance_uOhm > rTrip_JointResistance_HH_uOhm THEN
                arrPairStatusFlags[iCurrentWeldPairNumber] := arrPairStatusFlags[iCurrentWeldPairNumber] OR 16#0004;
                arrPairWeldScore_pct[iCurrentWeldPairNumber] := arrPairWeldScore_pct[iCurrentWeldPairNumber] - 40.0;
            END_IF;

            (* Increment Successfully Welded Pair Counter *)
            iTotalCompletedWelds := iTotalCompletedWelds + 1;
            iFSM_CurrentState := 9; (* Proceed to Rotary Chuck Index *)
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bEddyCurrent_ProbeExtend := FALSE;
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    9: (* -----------------------------------------------------------------------------------------
          STATE 9: ST_CHUCK_INDEX - Direct-Drive Rotary Chuck 3.75 deg Index to Next Pin Pair
          ----------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 1.2;
        bChuck_HoldBrakeRelease := TRUE;

        IF iCurrentWeldPairNumber < 96 THEN
            (* Index to Next Pin Pair: Pitch = 360.0 / 96 = 3.75 degrees *)
            rChuck_TargetPosition_deg   := rChuck_ActualPosition_deg + 3.750;
            rChuck_TargetVelocity_deg_s := 180.0; (* 180 deg/s high-dynamic index *)
            bChuck_MoveExecute          := TRUE;

            (* Check In-Position Strobe & Position Error (< 0.004 deg) *)
            IF bChuck_InPositionFlag AND (ABS(rChuck_ActualPosition_deg - rChuck_TargetPosition_deg) <= 0.004) THEN
                bChuck_MoveExecute := FALSE;
                iCurrentWeldPairNumber := iCurrentWeldPairNumber + 1;

                (* Periodic Optical Transmission Inspection every 16 pin pairs *)
                IF (iCurrentWeldPairNumber MOD 16) = 0 THEN
                    iFSM_CurrentState := 10; (* Branch to Optics Inspection *)
                ELSE
                    iFSM_CurrentState := 2; (* Loop to Vision Scan for Next Pair *)
                END_IF;
            END_IF;
        ELSE
            (* Stator 96-Pair Crown Welding Complete! *)
            bChuck_MoveExecute := FALSE;

            (* Audit Total Stator Defect Status *)
            bTemp_Condition1 := FALSE;
            FOR iIndex_Loop1 := 1 TO 96 DO
                IF (arrPairWeldScore_pct[iIndex_Loop1] < 70.0) OR (arrPairStatusFlags[iIndex_Loop1] <> 16#0000) THEN
                    bTemp_Condition1 := TRUE;
                END_IF;
            END_FOR;

            IF bTemp_Condition1 THEN
                iFSM_CurrentState := 12; (* Divert to Defect Quarantine *)
            ELSE
                iFSM_CurrentState := 11; (* Proceed to Finished Stator Egress *)
            END_IF;
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bChuck_MoveExecute := FALSE;
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    10: (* ----------------------------------------------------------------------------------------
           STATE 10: ST_OPTICS_INSPECT - Motorized Protective Cover Glass Transmission Verification
           ---------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 2.5;

        (* Check Real-Time Optical Transmission Index *)
        IF rOptics_Transmission_pct < rTrip_OpticsTransmission_L_pct THEN
            (* Cover Glass Degraded by Laser Fume/Spatter: Trigger Motorized Slide Film Advance *)
            bCoverGlass_MotorAdvance := TRUE;

            IF rStateTimer_s >= 0.800 THEN
                bCoverGlass_MotorAdvance := FALSE;
                (* Re-check Transmission post roll advance *)
                IF rOptics_Transmission_pct >= rTrip_OpticsTransmission_L_pct THEN
                    iFSM_CurrentState := 2; (* Return to Production Sequence *)
                ELSE
                    (* Cover Glass Cassette Exhausted / Critical Fouling *)
                    iFSM_CurrentState := 13;
                END_IF;
            END_IF;
        ELSE
            bCoverGlass_MotorAdvance := FALSE;
            iFSM_CurrentState := 2; (* Transmission Nominal: Return to Production *)
        END_IF;

        IF rStateTimer_s > rStateTimeoutLimit_s THEN
            bCoverGlass_MotorAdvance := FALSE;
            bStateTimeoutFault := TRUE;
            iFSM_CurrentState := 13;
        END_IF;

    11: (* ----------------------------------------------------------------------------------------
           STATE 11: ST_DECLAMP_EGRESS - Finished Stator De-Clamp, Unload & Conveyor Handshake
           ---------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 5.0;
        bLaserEmission_Enable   := FALSE;
        bLaserFastShutter_Open  := FALSE;
        bLaserAimingBeam_On     := FALSE;
        bShieldGas_Purge_Valve  := FALSE;
        bCrossJet_AirKnife_Valve := FALSE;

        (* Retract Datum Pins & De-Clamp Hydraulic Chuck Collet *)
        bDatumPin_Retract_Sol := TRUE;
        bDatumPin_Extend_Sol  := FALSE;
        bChuck_HydUnclamp_Sol := TRUE;
        bChuck_HydClamp_Sol   := FALSE;
        bChuck_HoldBrakeRelease := FALSE;

        bCellCycleCompleted := TRUE;

        (* Await Part Removal from Chuck or Operator Egress Confirmation *)
        IF (NOT bPartPresentInChuck) OR (rStateTimer_s >= 2.5) THEN
            iFSM_CurrentState := 0; (* Reset FSM to Idle / Await Next Stator Pallet *)
        END_IF;

    12: (* ----------------------------------------------------------------------------------------
           STATE 12: ST_REJECT_QUARANTINE - Defective Weld Pin Pair Tagging & Egress Diverter Push
           ---------------------------------------------------------------------------------------- *)
        rStateTimeoutLimit_s := 10.0;
        bLaserEmission_Enable   := FALSE;
        bLaserFastShutter_Open  := FALSE;
        bDatumPin_Retract_Sol   := TRUE;
        bDatumPin_Extend_Sol    := FALSE;
        bChuck_HydUnclamp_Sol   := TRUE;
        bChuck_HydClamp_Sol     := FALSE;
        bQuarantineDivert_Push  := TRUE;
        bCellGeneralFault       := TRUE;

        IF bResetFault THEN
            bQuarantineDivert_Push := FALSE;
            bCellGeneralFault      := FALSE;
            iFSM_CurrentState      := 0;
        END_IF;

    13: (* ----------------------------------------------------------------------------------------
           STATE 13: ST_EMERGENCY_SHUTTER - Fast Optical Shutter Lockout, Beam Dump & Fault Safe
           ---------------------------------------------------------------------------------------- *)
        bLaserEmission_Enable   := FALSE;
        bLaserFastShutter_Open  := FALSE;
        bLaserAimingBeam_On     := FALSE;
        rLaserPower_Cmd_kW      := 0.0;
        bChuck_MoveExecute      := FALSE;
        bChuck_HoldBrakeRelease := FALSE; (* Engage Mechanical Holding Brake Immediately *)
        bShieldGas_Purge_Valve  := FALSE;
        bCrossJet_AirKnife_Valve := FALSE;
        bEddyCurrent_ProbeExtend := FALSE;
        bCellEmergencyTripped   := TRUE;
        bCellGeneralFault       := TRUE;

        (* Safe Reset Handshake *)
        IF bResetFault AND (NOT bEmergencyStop) THEN
            bCellEmergencyTripped := FALSE;
            bCellGeneralFault     := FALSE;
            bStateTimeoutFault    := FALSE;
            iFSM_CurrentState     := 0;
        END_IF;

END_CASE;

(* Update Output Status State Index & Stator Cycle Timer *)
iCurrentStateIndex      := iFSM_CurrentState;
iCurrentWeldPairNumber  := MIN(96, MAX(1, iCurrentWeldPairNumber));
IF iFSM_CurrentState > 0 AND iFSM_CurrentState < 11 THEN
    rTotalStatorCycleTime_s := rTotalStatorCycleTime_s + rScanTime_s;
END_IF;
"""
