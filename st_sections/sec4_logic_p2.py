# Section 4: Logic Part 2 - Surge Lines, 5x5 State Space, MPC, Acoustic Damping, and Seal Vacuum
def get_sec4_logic_p2():
    return """(* === 4. DYNAMIC ANTI-SURGE LIMIT LINES & SURGE MARGIN METRICS === *)
(* 4.1 Parabolic Surge Limit Line (SLL) in Head vs Reduced Flow Squared *)
(* FlowSquared_SLL = (PolytropicHead - K0) / K2 *)
IF rPolytropicHead_kJkg >= c_rSLL_K0 THEN
    rFlowSquared_SLL := 0.50;
ELSE
    rFlowSquared_SLL := (rPolytropicHead_kJkg - c_rSLL_K0) / c_rSLL_K2;
END_IF;
rFlowSquared_SLL := MAX(0.50, MIN(120.0, rFlowSquared_SLL));

(* 4.2 Dynamic Biases to Safety Margin *)
(* Molecular Weight Bias: If gas is heavier than pure H2 due to contaminant ingress, shift SLL outward *)
IF rGasMolecularWeight_gmol > c_rNominalMolecularWeight_H2 THEN
    rMolecularWeightShiftBias_pct := (rGasMolecularWeight_gmol - c_rNominalMolecularWeight_H2) * 8.5;
ELSE
    rMolecularWeightShiftBias_pct := 0.0;
END_IF;

(* Acceleration Bias: When machine accelerates rapidly, add transient safety margin *)
IF (rShaftSpeed_Voted_rpm - rPrevShaftSpeed_rpm) > 5.0 THEN
    rAccelerationBias_pct := ((rShaftSpeed_Voted_rpm - rPrevShaftSpeed_rpm) / rDt) * 0.004;
ELSE
    rAccelerationBias_pct := 0.0;
END_IF;
rAccelerationBias_pct := MIN(6.0, rAccelerationBias_pct);

(* Acoustic Pulsation Bias: High standing waves in discharge line reduce aerodynamic boundary layer stability *)
IF rAcousticPulsationRMS_mbar > 1200.0 THEN
    rAcousticPulsationBias_pct := (rAcousticPulsationRMS_mbar - 1200.0) * 0.0025;
ELSE
    rAcousticPulsationBias_pct := 0.0;
END_IF;
rAcousticPulsationBias_pct := MIN(5.0, rAcousticPulsationBias_pct);

(* Total Dynamic Surge Control Margin *)
rDynamicSafetyMargin_pct := c_rBaseSurgeMargin_pct + rMolecularWeightShiftBias_pct +
                            rAccelerationBias_pct + rAcousticPulsationBias_pct;
rDynamicSafetyMargin_pct := MAX(10.0, MIN(28.0, rDynamicSafetyMargin_pct));

(* 4.3 Control Boundaries Coordinates *)
(* Surge Control Line (SCL) *)
rFlowSquared_SCL := rFlowSquared_SLL * (1.0 + rDynamicSafetyMargin_pct * 0.01) * (1.0 + rDynamicSafetyMargin_pct * 0.01);

(* Surge Backup Line (SBL) *)
rFlowSquared_SBL := rFlowSquared_SLL * (1.0 + c_rBackupSurgeMargin_pct * 0.01) * (1.0 + c_rBackupSurgeMargin_pct * 0.01);

(* Solenoid Trip Kick Line (SKL) *)
rFlowSquared_SKL := rFlowSquared_SLL * (1.0 + c_rSolenoidTripMargin_pct * 0.01) * (1.0 + c_rSolenoidTripMargin_pct * 0.01);

(* 4.4 Normalized Surge Margin & Rate of Approach *)
IF rFlowSquared_SLL > 0.01 THEN
    rSurgeMargin_pct := ((rReducedFlow_Squared - rFlowSquared_SLL) / rFlowSquared_SLL) * 100.0;
ELSE
    rSurgeMargin_pct := 50.0;
END_IF;

IF rFlowSquared_SCL > 0.01 THEN
    rDistanceToSCL_pct := ((rReducedFlow_Squared - rFlowSquared_SCL) / rFlowSquared_SCL) * 100.0;
ELSE
    rDistanceToSCL_pct := 25.0;
END_IF;

(* Numerical derivative of surge margin dSigma/dt [%/s] *)
rRateOfApproachToSurge_pct_s := (rSurgeMargin_pct - rPrevSurgeMargin_pct) / rDt;

(* Open-Loop Derivative Surge Kick Logic *)
IF bFastValveKickEnable AND (rRateOfApproachToSurge_pct_s < -15.0) AND (rDistanceToSCL_pct < 8.0) THEN
    bFastValveKickActive := TRUE;
    (* Calculate instantaneous valve kick magnitude proportional to approach velocity *)
    rRateOfApproachBias_pct := ABS(rRateOfApproachToSurge_pct_s + 15.0) * 1.25;
    rRateOfApproachBias_pct := MIN(50.0, rRateOfApproachBias_pct);
    IF rRateOfApproachBias_pct > rValveKickBias_pct THEN
        rValveKickBias_pct := rRateOfApproachBias_pct;
    END_IF;
    dwWarningWord1 := dwWarningWord1 OR 16#00000008; (* Bit 3: Fast Valve Kick Active *)
ELSE
    bFastValveKickActive := FALSE;
    (* Smooth exponential decay of open-loop kick bias *)
    rValveKickBias_pct := rValveKickBias_pct * rValveKickDecay;
    IF rValveKickBias_pct < 0.20 THEN
        rValveKickBias_pct := 0.0;
    END_IF;
END_IF;

(* === 5. DISCRETE 5x5 STATE-SPACE DYNAMIC MODEL SIMULATION === *)
(* State Vector:
   x[1]: Delta_Flow (kg/s)
   x[2]: Delta_P_disch (bar)
   x[3]: Delta_P_suct (bar)
   x[4]: Delta_Speed (rpm)
   x[5]: Delta_P_acoustic (mbar)
*)
(* Populate Discretized Dynamic Matrix A_d (5x5) *)
arrMatA[1,1] := 0.8850; arrMatA[1,2] := -0.0450; arrMatA[1,3] := 0.0650; arrMatA[1,4] := 0.0012; arrMatA[1,5] := -0.0008;
arrMatA[2,1] := 0.0350; arrMatA[2,2] := 0.9420;  arrMatA[2,3] := 0.0150; arrMatA[2,4] := 0.0022; arrMatA[2,5] := 0.0011;
arrMatA[3,1] := -0.0280;arrMatA[3,2] := 0.0080;  arrMatA[3,3] := 0.9510; arrMatA[3,4] := -0.0004;arrMatA[3,5] := 0.0002;
arrMatA[4,1] := -0.0150;arrMatA[4,2] := -0.0080; arrMatA[4,3] := 0.0050; arrMatA[4,4] := 0.9850; arrMatA[4,5] := 0.0000;
arrMatA[5,1] := 0.0520; arrMatA[5,2] := 0.0780;  arrMatA[5,3] := -0.0210;arrMatA[5,4] := 0.0014; arrMatA[5,5] := 0.7200;

(* Populate Input Coupling Matrix B_d (5x3)
   u[1]: Delta_ASV_Position_pct
   u[2]: Delta_Speed_Ref_rpm
   u[3]: Delta_Vac_Valve_pct
*)
arrMatB[1,1] := 0.3200; arrMatB[1,2] := -0.0002; arrMatB[1,3] := 0.0000;
arrMatB[2,1] := -0.2800;arrMatB[2,2] := 0.0042;  arrMatB[2,3] := 0.0000;
arrMatB[3,1] := 0.1900; arrMatB[3,2] := -0.0008; arrMatB[3,3] := 0.0000;
arrMatB[4,1] := 0.0250; arrMatB[4,2] := 0.0850;  arrMatB[4,3] := 0.0000;
arrMatB[5,1] := -0.1500;arrMatB[5,2] := 0.0005;  arrMatB[5,3] := 0.0000;

(* Populate Output Observation Matrix C_d (4x5)
   y[1]: Surge Margin Deviation (%)
   y[2]: Compression Ratio Deviation (-)
   y[3]: Seal Differential Pressure Deviation (bar)
   y[4]: Acoustic Dynamic Pressure RMS (mbar)
*)
arrMatC[1,1] := 1.450; arrMatC[1,2] := -0.320; arrMatC[1,3] := 0.280; arrMatC[1,4] := 0.015; arrMatC[1,5] := -0.050;
arrMatC[2,1] := -0.012;arrMatC[2,2] := 0.020;  arrMatC[2,3] := -0.020;arrMatC[2,4] := 0.0001;arrMatC[2,5] := 0.0000;
arrMatC[3,1] := 0.000; arrMatC[3,2] := 0.000;  arrMatC[3,3] := -0.010;arrMatC[3,4] := 0.0000;arrMatC[3,5] := 0.0000;
arrMatC[4,1] := 0.000; arrMatC[4,2] := 0.000;  arrMatC[4,3] := 0.000; arrMatC[4,4] := 0.0000;arrMatC[4,5] := 1.0000;

(* Populate Feedthrough Matrix D_d (4x3) *)
arrMatD[1,1] := 0.420; arrMatD[1,2] := 0.000; arrMatD[1,3] := 0.000;
arrMatD[2,1] := -0.005;arrMatD[2,2] := 0.0001;arrMatD[2,3] := 0.000;
arrMatD[3,1] := 0.000; arrMatD[3,2] := 0.000; arrMatD[3,3] := 0.000;
arrMatD[4,1] := -0.120;arrMatD[4,2] := 0.000; arrMatD[4,3] := 0.000;

(* Plant Observation Feedback into State Vector *)
arrStateX[1] := rMassFlow_kgs - 3.25;
arrStateX[2] := rDischPress_Voted_bar - 100.0;
arrStateX[3] := rSuctPress_Voted_bar - 50.0;
arrStateX[4] := rShaftSpeed_Voted_rpm - 18500.0;
arrStateX[5] := rAcousticDynamicPress_CH2_bar * 1000.0;

(* Input Vector *)
arrInputU[1] := rAntiSurgeValveActual_pct - 20.0;
arrInputU[2] := rSpeedRefActual_rpm - 18500.0;
arrInputU[3] := rVacValveActual_pct - 35.0;

(* Compute x[k+1] = A_d * x[k] + B_d * u[k] *)
FOR iState := 1 TO 5 DO
    arrNextStateX[iState] := arrMatA[iState,1] * arrStateX[1] +
                             arrMatA[iState,2] * arrStateX[2] +
                             arrMatA[iState,3] * arrStateX[3] +
                             arrMatA[iState,4] * arrStateX[4] +
                             arrMatA[iState,5] * arrStateX[5] +
                             arrMatB[iState,1] * arrInputU[1] +
                             arrMatB[iState,2] * arrInputU[2] +
                             arrMatB[iState,3] * arrInputU[3];
END_FOR;

(* Compute y[k] = C_d * x[k] + D_d * u[k] *)
FOR iState := 1 TO 4 DO
    arrOutputY[iState] := arrMatC[iState,1] * arrStateX[1] +
                          arrMatC[iState,2] * arrStateX[2] +
                          arrMatC[iState,3] * arrStateX[3] +
                          arrMatC[iState,4] * arrStateX[4] +
                          arrMatC[iState,5] * arrStateX[5] +
                          arrMatD[iState,1] * arrInputU[1] +
                          arrMatD[iState,2] * arrInputU[2] +
                          arrMatD[iState,3] * arrInputU[3];
END_FOR;

(* === 6. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST OPTIMIZATION === *)
IF bMPCControlEnable AND NOT bCompressorTrip THEN
    (* Evaluate Gradient: g = H * Delta_u + F * x0 *)
    (* Target: maintain surge margin at setpoint (arrOutputSP[1] = 15%), minimize acoustic energy *)
    arrGradientG[1] := arrWeightQ[1] * (arrOutputY[1] - arrOutputSP[1]) * arrMatD[1,1] +
                       arrWeightQ[4] * (arrOutputY[4] - arrOutputSP[4]) * arrMatD[4,1] +
                       arrWeightR[1] * arrDeltaU_Opt[1];

    arrGradientG[2] := arrWeightQ[2] * (arrOutputY[2] - arrOutputSP[2]) * arrMatD[2,2] +
                       arrWeightR[2] * arrDeltaU_Opt[2];

    arrGradientG[3] := arrWeightQ[3] * (arrOutputY[3] - arrOutputSP[3]) * 0.10 +
                       arrWeightR[3] * arrDeltaU_Opt[3];

    (* Numerical conditioning check *)
    IF ABS(arrGradientG[1]) > 5000.0 OR ABS(arrGradientG[2]) > 5000.0 THEN
        bMpcIllConditioned := TRUE;
        dwWarningWord2 := dwWarningWord2 OR 16#00000080; (* Bit 7: MPC Ill-conditioned *)
    ELSE
        bMpcIllConditioned := FALSE;
    END_IF;

    IF NOT bMpcIllConditioned THEN
        (* Projected gradient descent move *)
        arrDeltaU_Opt[1] := -rMpcStepAlpha * arrGradientG[1];
        arrDeltaU_Opt[2] := -rMpcStepAlpha * arrGradientG[2];
        arrDeltaU_Opt[3] := -rMpcStepAlpha * arrGradientG[3];

        (* Clamp optimal control rate to asymmetric actuator limits *)
        arrDeltaU_Opt[1] := MAX(-c_rASV_MaxCloseRate_pct_s * rDt,
                            MIN(c_rASV_MaxOpenRate_pct_s * rDt, arrDeltaU_Opt[1]));

        (* If distance to SCL is negative (inside control margin), prioritize fast opening *)
        IF rDistanceToSCL_pct < 0.0 THEN
            arrDeltaU_Opt[1] := arrDeltaU_Opt[1] + ABS(rDistanceToSCL_pct) * 0.45;
        END_IF;

        bMPCActive := TRUE;
    ELSE
        bMPCActive := FALSE;
    END_IF;
ELSE
    bMPCActive := FALSE;
    arrDeltaU_Opt[1] := 0.0;
    arrDeltaU_Opt[2] := 0.0;
    arrDeltaU_Opt[3] := 0.0;
END_IF;

(* 6.1 Decoupled PID Anti-Surge Fallback (Active if MPC is inactive or ill-conditioned) *)
IF NOT bMPCActive AND NOT bCompressorTrip THEN
    (* Error defined as distance to Surge Control Line: e = SCL - Operating_Point *)
    rASV_PID_Derivative := ((rFlowSquared_SCL - rReducedFlow_Squared) - rASV_PID_PrevError) / rDt;
    rASV_PID_PrevError  := (rFlowSquared_SCL - rReducedFlow_Squared);

    IF rDistanceToSCL_pct < 0.0 THEN
        (* Operating point is inside SCL: aggressive opening proportional action *)
        rASV_PID_Integral := rASV_PID_Integral + 2.5 * ABS(rDistanceToSCL_pct) * rDt;
        rASV_PID_Output := 15.0 + 3.2 * ABS(rDistanceToSCL_pct) + rASV_PID_Integral + 0.15 * rASV_PID_Derivative;
    ELSE
        (* Safe operating region: slowly ramp integral closed *)
        rASV_PID_Integral := rASV_PID_Integral - 0.45 * rDt;
        rASV_PID_Output := rASV_PID_Integral;
    END_IF;
    rASV_PID_Integral := MAX(0.0, MIN(100.0, rASV_PID_Integral));
    rASV_PID_Output   := MAX(0.0, MIN(100.0, rASV_PID_Output));
END_IF;

(* === 7. PIPELINE ACOUSTIC WAVE STANDING WAVE PULSATION ACTIVE DAMPING === *)
(* 7.1 Dynamic Pressure Input from Piezo Transducer [bar -> mbar] *)
rAcousticInput_mbar := rAcousticDynamicPress_CH2_bar * 1000.0;

(* 7.2 2nd-Order Butterworth Digital Bandpass Filter (120 - 350 Hz) *)
(* Difference equation: Y0 = b0*X0 + b1*X1 + b2*X2 - a1*Y1 - a2*Y2 *)
rAcousticFilt_X0 := rAcousticInput_mbar;
rAcousticFilt_Y0 := c_rIIR_b0 * rAcousticFilt_X0 +
                    c_rIIR_b1 * rAcousticFilt_X1 +
                    c_rIIR_b2 * rAcousticFilt_X2 -
                    c_rIIR_a1 * rAcousticFilt_Y1 -
                    c_rIIR_a2 * rAcousticFilt_Y2;

(* Update delay registers *)
rAcousticFilt_X2 := rAcousticFilt_X1;
rAcousticFilt_X1 := rAcousticFilt_X0;
rAcousticFilt_Y2 := rAcousticFilt_Y1;
rAcousticFilt_Y1 := rAcousticFilt_Y0;

(* 7.3 Rolling Window RMS Calculation (100 samples) *)
rAcousticSumSquares := rAcousticSumSquares -
                       (arrAcousticHistory[iAcousticHistIndex] * arrAcousticHistory[iAcousticHistIndex]);
arrAcousticHistory[iAcousticHistIndex] := rAcousticFilt_Y0;
rAcousticSumSquares := rAcousticSumSquares + (rAcousticFilt_Y0 * rAcousticFilt_Y0);
iAcousticHistIndex := iAcousticHistIndex + 1;
IF iAcousticHistIndex > 100 THEN
    iAcousticHistIndex := 1;
END_IF;
IF rAcousticSumSquares > 0.0 THEN
    rAcousticPulsationRMS_mbar := SQRT(rAcousticSumSquares * 0.01);
ELSE
    rAcousticPulsationRMS_mbar := 0.0;
END_IF;

(* 7.4 Phase-Lead Dynamic Anti-Pulsation Modulation *)
IF bAcousticDampingEnable AND (rAcousticPulsationRMS_mbar > 450.0) AND NOT bCompressorTrip THEN
    (* Phase lead transfer function: G_lead = K * (Y0 + tau * dY/dt) *)
    rAcousticPhaseLeadOutput := -c_rAcousticPhaseLeadGain *
                                (rAcousticFilt_Y0 + 0.0022 * ((rAcousticFilt_Y0 - rAcousticFilt_Y1) / rDt));

    (* Micro-dither command clamped between -c_rAcousticDitherMaxClamp_pct and +c_rAcousticDitherMaxClamp_pct *)
    rAcousticDitherModulation := MAX(-c_rAcousticDitherMaxClamp_pct,
                                 MIN(c_rAcousticDitherMaxClamp_pct, rAcousticPhaseLeadOutput));
    bAcousticDampingEngaged := TRUE;
ELSE
    rAcousticDitherModulation := 0.0;
    bAcousticDampingEngaged := FALSE;
END_IF;

(* === 8. DRY GAS SEAL LEAKAGE VACUUM EXTRACTION SUBSYSTEM === *)
(* 8.1 Primary Seal Gas Differential Pressure Supervision *)
rPrimarySealDP_bar := rSealGasSupplyPress_bar - rSuctPress_Voted_bar;

IF rPrimarySealDP_bar < c_rCriticalLowSealDP_bar THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000200; (* Bit 9: Primary Seal Gas DP Low-Low *)
ELSIF rPrimarySealDP_bar < c_rMinPrimarySealDP_bar THEN
    dwWarningWord1 := dwWarningWord1 OR 16#00000400; (* Bit 10: Seal DP Low Warning *)
END_IF;

(* 8.2 Primary Vent Cavity Pressure Regulation (-80.0 mbar gauge setpoint) *)
rVac_PID_Error := rPrimaryVentPress_mbar - c_rVacSetpoint_mbar;

(* Anti-windup PID formulation for vacuum extraction modulating valve *)
rVac_PID_Derivative := (rVac_PID_Error - rVac_PID_PrevError) / rDt;
rVac_PID_PrevError  := rVac_PID_Error;

rVac_PID_Integral := rVac_PID_Integral + (0.015 * rVac_PID_Error * rDt);
rVac_PID_Integral := MAX(0.0, MIN(100.0, rVac_PID_Integral));

rVacExtractionValveRaw_pct := 35.0 + (0.28 * rVac_PID_Error) + rVac_PID_Integral + (0.05 * rVac_PID_Derivative);
rVacExtractionValveRaw_pct := MAX(0.0, MIN(100.0, rVacExtractionValveRaw_pct));

IF rPrimaryVentPress_mbar >= -120.0 AND rPrimaryVentPress_mbar <= 200.0 THEN
    bSealVacuumHealthy := TRUE;
ELSE
    bSealVacuumHealthy := FALSE;
END_IF;

(* 8.3 Secondary Buffer Nitrogen Gas & LEL Protection *)
IF rBufferN2SupplyPress_bar < 1.50 THEN
    dwAlarmWord3 := dwAlarmWord3 OR 16#00000001; (* Bit 0: N2 Buffer Supply Low-Low *)
END_IF;

IF rSealVentH2Concentration_LEL >= c_rTripH2Concentration_LEL THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00001000; (* Bit 12: Vent Duct H2 LEL High-High Trip *)
ELSIF rSealVentH2Concentration_LEL >= 25.0 THEN
    dwWarningWord2 := dwWarningWord2 OR 16#00000800; (* Bit 11: Vent Duct H2 LEL High Warning *)
END_IF;

IF rPrimarySealLeakage_Nm3h >= c_rTripPrimaryLeakage_Nm3h THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000800; (* Bit 11: Primary Seal Leakage High-High Trip *)
ELSIF rPrimarySealLeakage_Nm3h >= c_rMaxPrimaryLeakage_Nm3h THEN
    dwWarningWord2 := dwWarningWord2 OR 16#00000400; (* Bit 10: Primary Seal Leakage High Warning *)
END_IF;
"""
