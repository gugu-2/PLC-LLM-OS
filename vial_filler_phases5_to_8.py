# -*- coding: utf-8 -*-
"""
vial_filler_phases5_to_8.py
Contains Phases 5 to 8 for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh:
- Phase 5: 100% In-Line Tare & Gross Dynamic Checkweighing & Adaptive Trim & SPC Cpk
- Phase 6: Continuous N2 Headspace Inerting & Rotary Vacuum Stoppering Wheel
- Phase 7: Rotary 16-Head Aluminum Crimp Capper Container Closure Integrity (CCI)
- Phase 8: High-Speed Pocket Reject Shift Register & Air-Puff Diverter
"""

def get_phases5_to_8_code():
    return """(* ========================================================================================= *)
(* SECTION 5: PHASE 5 - 100% TARE & GROSS DYNAMIC CHECKWEIGHING & ADAPTIVE SPC TRIM           *)
(* ========================================================================================= *)
(* High-speed electromagnetic force restoration (EMFR) checkweighing at 600 VPM (100 ms).   *)
(* Sub-milligram net mass calculation with per-needle closed loop adaptive integral feedback *)
(* and rolling 120-sample Statistical Process Control (SPC) evaluating Cp and Cpk.          *)

(* Trigger checkweigh evaluation when turret passes the indexing measurement window *)
(* Measurement dwell zone: rTurretIndexAngle_deg between 12.0 and 18.0 degrees *)
IF (rTurretIndexAngle_deg >= 12.0) AND (rTurretIndexAngle_deg <= 18.0) THEN
    (* 1. Tare Checkweigh Station (Station Pocket 4) *)
    IF arPocketVialPresent[4] THEN
        arPocketTareWeight_mg[4] := rTareVoted_mg;
        (* Verify empty glass vial tare within allowable tare tolerance *)
        IF (rTareVoted_mg < (15000.0 - rTareWeightTolerance_mg)) OR
           (rTareVoted_mg > (15000.0 + rTareWeightTolerance_mg)) THEN
            arPocketRejectFlag[4] := TRUE;
            arPocketRejectReason[4] := arPocketRejectReason[4] OR 16#0000_0001; (* Bit 0: Tare out of tolerance *)
        END_IF;
    END_IF;

    (* 2. Gross Checkweigh Station (Station Pocket 24) *)
    IF arPocketVialPresent[24] AND NOT arPocketRejectFlag[24] THEN
        arPocketGrossWeight_mg[24] := rGrossVoted_mg;
        (* Calculate Net Filled Liquid Mass: Net = Gross - Tare *)
        arNeedleNetWeight_mg[arPocketDispenseChannel[24]] := rGrossVoted_mg - arPocketTareWeight_mg[24];
        
        (* Verify Net Filled Mass against specification tolerance limits *)
        IF (arNeedleNetWeight_mg[arPocketDispenseChannel[24]] < rLowerSpecLimit_mg) OR
           (arNeedleNetWeight_mg[arPocketDispenseChannel[24]] > rUpperSpecLimit_mg) THEN
            arPocketRejectFlag[24] := TRUE;
            arPocketRejectReason[24] := arPocketRejectReason[24] OR 16#0000_0002; (* Bit 1: Gross net out of spec *)
            iConsecutiveWeightRejects := iConsecutiveWeightRejects + 1;
            arNeedleRejectCount[arPocketDispenseChannel[24]] := arNeedleRejectCount[arPocketDispenseChannel[24]] + 1;
        ELSE
            iConsecutiveWeightRejects := 0;
            arNeedleDispenseCount[arPocketDispenseChannel[24]] := arNeedleDispenseCount[arPocketDispenseChannel[24]] + 1;
        END_IF;

        (* Closed-Loop Adaptive Integral Trim Feedback per Individual Needle *)
        idx_k := arPocketDispenseChannel[24];
        IF (idx_k >= 1) AND (idx_k <= 12) THEN
            rScratchAccum := arNeedleNetWeight_mg[idx_k] - rTargetNetWeight_mg;
            (* Accumulate integral bias *)
            arChannelIntegralError[idx_k] := arChannelIntegralError[idx_k] + (rScratchAccum * 0.05);
            (* Anti-windup clamping on integral bias *)
            IF arChannelIntegralError[idx_k] > 25.0 THEN
                arChannelIntegralError[idx_k] := 25.0;
            ELSIF arChannelIntegralError[idx_k] < -25.0 THEN
                arChannelIntegralError[idx_k] := -25.0;
            END_IF;

            (* Micro-liter trim adjustment based on fluid density *)
            arPumpOffsetTrim_ul[idx_k] := arPumpOffsetTrim_ul[idx_k] -
                ((arChannelGain[idx_k] * rScratchAccum) / rLiquidDensity_g_cm3) -
                (0.01 * arChannelIntegralError[idx_k]);

            (* Saturation limit on micro-liter trim (+/- 150 ul) *)
            IF arPumpOffsetTrim_ul[idx_k] > 150.0 THEN
                arPumpOffsetTrim_ul[idx_k] := 150.0;
            ELSIF arPumpOffsetTrim_ul[idx_k] < -150.0 THEN
                arPumpOffsetTrim_ul[idx_k] := -150.0;
            END_IF;
        END_IF;

        (* Insert Net Weight into Rolling 120-Sample FIFO Circular Buffer *)
        arWeightBuffer_mg[iBufferHead] := arNeedleNetWeight_mg[arPocketDispenseChannel[24]];
        iBufferHead := iBufferHead + 1;
        IF iBufferHead > 120 THEN
            iBufferHead := 1;
        END_IF;
        IF iBufferCount < 120 THEN
            iBufferCount := iBufferCount + 1;
        END_IF;
    END_IF;
END_IF;

(* Statistical Process Control (SPC) Dynamic Moving Evaluation *)
IF iBufferCount >= 10 THEN
    rSumGrossWeight_mg := 0.0;
    FOR idx_i := 1 TO iBufferCount DO
        rSumGrossWeight_mg := rSumGrossWeight_mg + arWeightBuffer_mg[idx_i];
    END_FOR;
    rMeanGrossWeight_mg := rSumGrossWeight_mg / INT_TO_REAL(iBufferCount);
    rMeanDosingVolume_ml := rMeanGrossWeight_mg / (rLiquidDensity_g_cm3 * 1000.0);

    rSumSqGrossWeight_mg := 0.0;
    FOR idx_i := 1 TO iBufferCount DO
        rScratchAccum := arWeightBuffer_mg[idx_i] - rMeanGrossWeight_mg;
        rSumSqGrossWeight_mg := rSumSqGrossWeight_mg + (rScratchAccum * rScratchAccum);
    END_FOR;
    (* Sample Standard Deviation: s = SQRT(sum_sq / (N - 1)) *)
    IF iBufferCount > 1 THEN
        rStdDevGrossWeight_mg := SQRT(rSumSqGrossWeight_mg / INT_TO_REAL(iBufferCount - 1));
    ELSE
        rStdDevGrossWeight_mg := 0.001;
    END_IF;

    (* Process Capability Index Cpk Calculation *)
    IF rStdDevGrossWeight_mg > 0.001 THEN
        rScratchAccum := (rUpperSpecLimit_mg - rMeanGrossWeight_mg) / (3.0 * rStdDevGrossWeight_mg);
        rProcessCapability_Cpk := (rMeanGrossWeight_mg - rLowerSpecLimit_mg) / (3.0 * rStdDevGrossWeight_mg);
        IF rScratchAccum < rProcessCapability_Cpk THEN
            rProcessCapability_Cpk := rScratchAccum;
        END_IF;
    ELSE
        rProcessCapability_Cpk := 2.50; (* Ideal capability *)
    END_IF;
ELSE
    rMeanGrossWeight_mg := rTargetNetWeight_mg;
    rStdDevGrossWeight_mg := 1.0;
    rProcessCapability_Cpk := 1.67;
END_IF;

(* ========================================================================================= *)
(* SECTION 6: PHASE 6 - CONTINUOUS N2 HEADSPACE INERTING & ROTARY VACUUM STOPPERING WHEEL    *)
(* ========================================================================================= *)
(* Displaces atmospheric oxygen from vial neck headspace with high-purity nitrogen before    *)
(* inserting sterile elastomeric stoppers under laminar flow to guarantee residual O2 < 0.8% *)

(* Nitrogen Gas Purge Flow Controller *)
rN2PurgeFlowCmd_lnpm := rN2PurgeFlow_Set_lnpm;
IF (iFsmState = 5) THEN
    (* Verify actual N2 supply line pressure *)
    IF rN2SupplyPressure_bar < 3.8 THEN
        (* Elevate purge valve duty cycle to compensate for low supply pressure *)
        rN2PurgeValveCmd_pct := 85.0;
    END_IF;
ELSE
    rN2PurgeFlowCmd_lnpm := 2.5; (* Standby trickle flow *)
END_IF;

(* Continuous 24-Pocket Rotary Vacuum Stoppering Wheel Monitoring *)
(* Rotary vacuum wheel rotates synchronously with monoblock main turret *)
FOR idx_i := 1 TO 24 DO
    arStopperWheelPocketVacuum_bar[idx_i] := rStopperVacuumSense_bar;
    (* Verify vacuum threshold: P < -0.45 bar indicates presence of seated elastomeric stopper *)
    IF arStopperWheelPocketVacuum_bar[idx_i] <= -0.45 THEN
        arStopperWheelPocketPresent[idx_i] := TRUE;
    ELSE
        arStopperWheelPocketPresent[idx_i] := FALSE;
    END_IF;
END_FOR;

(* Insertion Station: Starwheel Pocket 30 receives stopper from wheel pocket *)
IF arPocketVialPresent[30] AND NOT arPocketRejectFlag[30] THEN
    (* Check whether corresponding stoppering pocket had a verified stopper *)
    IF NOT arStopperWheelPocketPresent[1] THEN
        (* Missing stopper detected *)
        arPocketRejectFlag[30] := TRUE;
        arPocketRejectReason[30] := arPocketRejectReason[30] OR 16#0000_0004; (* Bit 2: Missing stopper *)
        iConsecutiveStopperRejects := iConsecutiveStopperRejects + 1;
    ELSE
        iConsecutiveStopperRejects := 0;
    END_IF;

    (* Verify Non-Destructive Headspace Oxygen via TDLAS Laser Sensor *)
    IF rHeadspaceO2_Sensor_pct > rHeadspaceO2_Max_Pct THEN
        arPocketRejectFlag[30] := TRUE;
        arPocketRejectReason[30] := arPocketRejectReason[30] OR 16#0000_0008; (* Bit 3: High residual O2 *)
    END_IF;
END_IF;

(* ========================================================================================= *)
(* SECTION 7: PHASE 7 - ROTARY 16-HEAD CRIMP CAPPER CONTAINER CLOSURE INTEGRITY (CCI)        *)
(* ========================================================================================= *)
(* 16-spindle rotary capping turret crimps aluminum flip-off seals over elastomeric stopper.  *)
(* Dynamic piezoelectric force sensor & spring deflection measure Container Closure Integrity*)

(* Capping Station: Starwheel Pocket 38 *)
IF arPocketVialPresent[38] AND NOT arPocketRejectFlag[38] THEN
    (* Dynamic Crimp Sealing Force Verification *)
    arCrimpSpindleSealForce_N[1] := rCrimpForceSensor_N;
    arCrimpSpindleDeflection_mm[1] := rCrimpDeflection_mm;

    (* Evaluate force envelope: Nominal 145 N +/- 15 N *)
    IF (rCrimpForceSensor_N < (rCrimpForce_Nominal_N - rCrimpForce_Tol_N)) OR
       (rCrimpForceSensor_N > (rCrimpForce_Nominal_N + rCrimpForce_Tol_N)) THEN
        arPocketRejectFlag[38] := TRUE;
        arPocketRejectReason[38] := arPocketRejectReason[38] OR 16#0000_0010; (* Bit 4: Crimp force out of spec *)
        iConsecutiveCrimpRejects := iConsecutiveCrimpRejects + 1;
    ELSE
        (* Evaluate spring deflection: Nominal 2.1 mm +/- 0.4 mm *)
        IF (rCrimpDeflection_mm < 1.70) OR (rCrimpDeflection_mm > 2.50) THEN
            arPocketRejectFlag[38] := TRUE;
            arPocketRejectReason[38] := arPocketRejectReason[38] OR 16#0000_0020; (* Bit 5: Deflection out of spec *)
            iConsecutiveCrimpRejects := iConsecutiveCrimpRejects + 1;
        ELSE
            iConsecutiveCrimpRejects := 0;
        END_IF;
    END_IF;
END_IF;

(* Dynamic Crimp Servo Position and Torque Command Modulation *)
rCrimpServoPosCmd_mm := 18.5 - (0.015 * (rCrimpForceSensor_N - rCrimpForce_Nominal_N));
IF rCrimpServoPosCmd_mm < 15.0 THEN rCrimpServoPosCmd_mm := 15.0; END_IF;
IF rCrimpServoPosCmd_mm > 22.0 THEN rCrimpServoPosCmd_mm := 22.0; END_IF;

(* ========================================================================================= *)
(* SECTION 8: PHASE 8 - HIGH-SPEED POCKET REJECT SHIFT REGISTER & AIR-PUFF DIVERTER          *)
(* ========================================================================================= *)
(* Tracks every vial position across all 48 pockets. Directs defective containers to reject  *)
(* collection bin via synchronized servo gate and high-pressure pneumatic air blast.        *)

(* Starwheel Pitch Advance Trigger: when index angle wraps through 0 degrees *)
IF (rTurretIndexAngle_deg < 1.5) AND (iFsmState = 5) THEN
    (* Advance 48-pocket shift register backwards from pocket 48 down to pocket 2 *)
    FOR idx_i := 48 TO 2 BY -1 DO
        arPocketVialPresent[idx_i]     := arPocketVialPresent[idx_i - 1];
        arPocketTareWeight_mg[idx_i]   := arPocketTareWeight_mg[idx_i - 1];
        arPocketGrossWeight_mg[idx_i]  := arPocketGrossWeight_mg[idx_i - 1];
        arPocketDispenseChannel[idx_i] := arPocketDispenseChannel[idx_i - 1];
        arPocketRejectFlag[idx_i]      := arPocketRejectFlag[idx_i - 1];
        arPocketRejectReason[idx_i]    := arPocketRejectReason[idx_i - 1];
    END_FOR;

    (* Load new vial into pocket 1 from infeed screw / starwheel *)
    IF bVialInfeedDetect AND bDepyrogenationTunnelReady THEN
        arPocketVialPresent[1]     := TRUE;
        arPocketTareWeight_mg[1]   := 0.0;
        arPocketGrossWeight_mg[1]  := 0.0;
        arPocketDispenseChannel[1] := (DINT_TO_INT(diTotalVialsProcessed) MOD 12) + 1;
        arPocketRejectFlag[1]      := FALSE;
        arPocketRejectReason[1]    := 16#0000_0000;
        diTotalVialsProcessed      := diTotalVialsProcessed + 1;
    ELSE
        arPocketVialPresent[1]     := FALSE;
        arPocketTareWeight_mg[1]   := 0.0;
        arPocketGrossWeight_mg[1]  := 0.0;
        arPocketDispenseChannel[1] := 1;
        arPocketRejectFlag[1]      := FALSE;
        arPocketRejectReason[1]    := 16#0000_0000;
    END_IF;
END_IF;

(* Reject Diverter Station at Pocket 44 *)
IF arPocketVialPresent[44] THEN
    IF arPocketRejectFlag[44] THEN
        (* Fire high-speed pneumatic reject gate and air-puff nozzle *)
        bRejectGateCmd := TRUE;
        bRejectAirPuffCmd := TRUE;
        bRejectActive := TRUE;
        diTotalVialsRejected := diTotalVialsRejected + 1;

        (* Categorize reject accountability counters *)
        IF (arPocketRejectReason[44] AND 16#0000_0003) <> 0 THEN
            diDosingRejectsCount := diDosingRejectsCount + 1;
        ELSIF (arPocketRejectReason[44] AND 16#0000_0004) <> 0 THEN
            diStopperRejectsCount := diStopperRejectsCount + 1;
        ELSIF (arPocketRejectReason[44] AND 16#0000_0030) <> 0 THEN
            diCrimpRejectsCount := diCrimpRejectsCount + 1;
        END_IF;
    ELSE
        (* Conforming vial safely transferred to packaging conveyor *)
        bRejectGateCmd := FALSE;
        bRejectAirPuffCmd := FALSE;
        bRejectActive := FALSE;
        diTotalVialsAccepted := diTotalVialsAccepted + 1;
    END_IF;
ELSE
    bRejectGateCmd := FALSE;
    bRejectAirPuffCmd := FALSE;
    bRejectActive := FALSE;
END_IF;
"""
