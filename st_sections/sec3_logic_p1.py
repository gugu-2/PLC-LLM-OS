# Section 3: Logic Part 1 - Cycle Init, 2oo3 TMR Voting Engine, and Real-Time Hydrogen Thermodynamics
def get_sec3_logic_p1():
    return """(* === 1. SYSTEM INITIALIZATION, CLOCK MONITORING & WATCHDOGS === *)
diScanCounter := diScanCounter + 1;

(* Clamp discrete delta time between 1 ms and 50 ms to preserve numerical stability *)
IF rCycleTime_s >= 0.001 AND rCycleTime_s <= 0.050 THEN
    rDt := rCycleTime_s;
ELSE
    rDt := 0.005; (* Default to 5 ms deterministic task rate *)
END_IF;

(* Clear cycle diagnostic warning words before evaluation *)
dwWarningWord1 := 16#00000000;
dwWarningWord2 := 16#00000000;
bDegradedSensorMode := FALSE;

(* === 2. TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING ENGINE === *)
(* Populate Raw Arrays *)
arrSuctPress_Raw[1]  := rSuctionPress_CH1_bar;
arrSuctPress_Raw[2]  := rSuctionPress_CH2_bar;
arrSuctPress_Raw[3]  := rSuctionPress_CH3_bar;

arrDischPress_Raw[1] := rDischargePress_CH1_bar;
arrDischPress_Raw[2] := rDischargePress_CH2_bar;
arrDischPress_Raw[3] := rDischargePress_CH3_bar;

arrFlowDP_Raw[1]     := rSuctionFlowDP_CH1_mbar;
arrFlowDP_Raw[2]     := rSuctionFlowDP_CH2_mbar;
arrFlowDP_Raw[3]     := rSuctionFlowDP_CH3_mbar;

arrSuctTemp_Raw[1]   := rSuctionTemp_CH1_K;
arrSuctTemp_Raw[2]   := rSuctionTemp_CH2_K;
arrSuctTemp_Raw[3]   := rSuctionTemp_CH3_K;

arrDischTemp_Raw[1]  := rDischargeTemp_CH1_K;
arrDischTemp_Raw[2]  := rDischargeTemp_CH2_K;
arrDischTemp_Raw[3]  := rDischargeTemp_CH3_K;

arrSpeed_Raw[1]      := rShaftSpeed_CH1_rpm;
arrSpeed_Raw[2]      := rShaftSpeed_CH2_rpm;
arrSpeed_Raw[3]      := rShaftSpeed_CH3_rpm;

(* 2.1 SUCTION PRESSURE 2oo3 VOTING & DIAGNOSTICS *)
FOR iState := 1 TO 3 DO
    (* Range check: 0.0 to 140.0 bar *)
    IF arrSuctPress_Raw[iState] < 0.5 OR arrSuctPress_Raw[iState] > 140.0 THEN
        arrSuctPress_Health[iState] := FALSE;
    ELSE
        arrSuctPress_Health[iState] := TRUE;
    END_IF;
END_FOR;

IF arrSuctPress_Health[1] AND arrSuctPress_Health[2] AND arrSuctPress_Health[3] THEN
    (* Cross-channel deviation checks (1.5 bar threshold) *)
    IF ABS(arrSuctPress_Raw[1] - arrSuctPress_Raw[2]) > 1.5 OR
       ABS(arrSuctPress_Raw[2] - arrSuctPress_Raw[3]) > 1.5 OR
       ABS(arrSuctPress_Raw[3] - arrSuctPress_Raw[1]) > 1.5 THEN
        dwWarningWord2 := dwWarningWord2 OR 16#00000001; (* Bit 0: Suction Pressure Discrepancy *)
    END_IF;
    (* Mid-Value Median Filter *)
    IF (arrSuctPress_Raw[1] >= arrSuctPress_Raw[2] AND arrSuctPress_Raw[1] <= arrSuctPress_Raw[3]) OR
       (arrSuctPress_Raw[1] >= arrSuctPress_Raw[3] AND arrSuctPress_Raw[1] <= arrSuctPress_Raw[2]) THEN
        rSuctPress_Voted_bar := arrSuctPress_Raw[1];
    ELSIF (arrSuctPress_Raw[2] >= arrSuctPress_Raw[1] AND arrSuctPress_Raw[2] <= arrSuctPress_Raw[3]) OR
          (arrSuctPress_Raw[2] >= arrSuctPress_Raw[3] AND arrSuctPress_Raw[2] <= arrSuctPress_Raw[1]) THEN
        rSuctPress_Voted_bar := arrSuctPress_Raw[2];
    ELSE
        rSuctPress_Voted_bar := arrSuctPress_Raw[3];
    END_IF;
ELSIF arrSuctPress_Health[1] AND arrSuctPress_Health[2] THEN
    rSuctPress_Voted_bar := (arrSuctPress_Raw[1] + arrSuctPress_Raw[2]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020; (* Bit 5: Degraded 1oo2 Mode *)
ELSIF arrSuctPress_Health[2] AND arrSuctPress_Health[3] THEN
    rSuctPress_Voted_bar := (arrSuctPress_Raw[2] + arrSuctPress_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrSuctPress_Health[1] AND arrSuctPress_Health[3] THEN
    rSuctPress_Voted_bar := (arrSuctPress_Raw[1] + arrSuctPress_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrSuctPress_Health[1] THEN
    rSuctPress_Voted_bar := arrSuctPress_Raw[1];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040; (* Bit 6: Degraded 1oo1 Mode *)
ELSIF arrSuctPress_Health[2] THEN
    rSuctPress_Voted_bar := arrSuctPress_Raw[2];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSIF arrSuctPress_Health[3] THEN
    rSuctPress_Voted_bar := arrSuctPress_Raw[3];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSE
    rSuctPress_Voted_bar := c_rDesignSuctionPressure_bar;
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000002; (* Bit 1: Triple Suction Transmitter Failure *)
END_IF;

(* 2.2 DISCHARGE PRESSURE 2oo3 VOTING & DIAGNOSTICS *)
FOR iState := 1 TO 3 DO
    IF arrDischPress_Raw[iState] < 0.5 OR arrDischPress_Raw[iState] > 160.0 THEN
        arrDischPress_Health[iState] := FALSE;
    ELSE
        arrDischPress_Health[iState] := TRUE;
    END_IF;
END_FOR;

IF arrDischPress_Health[1] AND arrDischPress_Health[2] AND arrDischPress_Health[3] THEN
    IF ABS(arrDischPress_Raw[1] - arrDischPress_Raw[2]) > 2.0 OR
       ABS(arrDischPress_Raw[2] - arrDischPress_Raw[3]) > 2.0 OR
       ABS(arrDischPress_Raw[3] - arrDischPress_Raw[1]) > 2.0 THEN
        dwWarningWord2 := dwWarningWord2 OR 16#00000002; (* Bit 1: Discharge Pressure Discrepancy *)
    END_IF;
    IF (arrDischPress_Raw[1] >= arrDischPress_Raw[2] AND arrDischPress_Raw[1] <= arrDischPress_Raw[3]) OR
       (arrDischPress_Raw[1] >= arrDischPress_Raw[3] AND arrDischPress_Raw[1] <= arrDischPress_Raw[2]) THEN
        rDischPress_Voted_bar := arrDischPress_Raw[1];
    ELSIF (arrDischPress_Raw[2] >= arrDischPress_Raw[1] AND arrDischPress_Raw[2] <= arrDischPress_Raw[3]) OR
          (arrDischPress_Raw[2] >= arrDischPress_Raw[3] AND arrDischPress_Raw[2] <= arrDischPress_Raw[1]) THEN
        rDischPress_Voted_bar := arrDischPress_Raw[2];
    ELSE
        rDischPress_Voted_bar := arrDischPress_Raw[3];
    END_IF;
ELSIF arrDischPress_Health[1] AND arrDischPress_Health[2] THEN
    rDischPress_Voted_bar := (arrDischPress_Raw[1] + arrDischPress_Raw[2]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrDischPress_Health[2] AND arrDischPress_Health[3] THEN
    rDischPress_Voted_bar := (arrDischPress_Raw[2] + arrDischPress_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrDischPress_Health[1] AND arrDischPress_Health[3] THEN
    rDischPress_Voted_bar := (arrDischPress_Raw[1] + arrDischPress_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrDischPress_Health[1] THEN
    rDischPress_Voted_bar := arrDischPress_Raw[1];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSIF arrDischPress_Health[2] THEN
    rDischPress_Voted_bar := arrDischPress_Raw[2];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSIF arrDischPress_Health[3] THEN
    rDischPress_Voted_bar := arrDischPress_Raw[3];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSE
    rDischPress_Voted_bar := c_rDesignDischargePressure_bar;
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000004; (* Bit 2: Triple Discharge Transmitter Failure *)
END_IF;

(* 2.3 SUCTION FLOW ORIFICE DIFFERENTIAL PRESSURE 2oo3 VOTING *)
FOR iState := 1 TO 3 DO
    IF arrFlowDP_Raw[iState] < -5.0 OR arrFlowDP_Raw[iState] > 600.0 THEN
        arrFlowDP_Health[iState] := FALSE;
    ELSE
        arrFlowDP_Health[iState] := TRUE;
    END_IF;
END_FOR;

IF arrFlowDP_Health[1] AND arrFlowDP_Health[2] AND arrFlowDP_Health[3] THEN
    IF ABS(arrFlowDP_Raw[1] - arrFlowDP_Raw[2]) > 15.0 OR
       ABS(arrFlowDP_Raw[2] - arrFlowDP_Raw[3]) > 15.0 OR
       ABS(arrFlowDP_Raw[3] - arrFlowDP_Raw[1]) > 15.0 THEN
        dwWarningWord2 := dwWarningWord2 OR 16#00000004; (* Bit 2: Flow DP Discrepancy *)
    END_IF;
    IF (arrFlowDP_Raw[1] >= arrFlowDP_Raw[2] AND arrFlowDP_Raw[1] <= arrFlowDP_Raw[3]) OR
       (arrFlowDP_Raw[1] >= arrFlowDP_Raw[3] AND arrFlowDP_Raw[1] <= arrFlowDP_Raw[2]) THEN
        rFlowDP_Voted_mbar := arrFlowDP_Raw[1];
    ELSIF (arrFlowDP_Raw[2] >= arrFlowDP_Raw[1] AND arrFlowDP_Raw[2] <= arrFlowDP_Raw[3]) OR
          (arrFlowDP_Raw[2] >= arrFlowDP_Raw[3] AND arrFlowDP_Raw[2] <= arrFlowDP_Raw[1]) THEN
        rFlowDP_Voted_mbar := arrFlowDP_Raw[2];
    ELSE
        rFlowDP_Voted_mbar := arrFlowDP_Raw[3];
    END_IF;
ELSIF arrFlowDP_Health[1] AND arrFlowDP_Health[2] THEN
    rFlowDP_Voted_mbar := (arrFlowDP_Raw[1] + arrFlowDP_Raw[2]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrFlowDP_Health[2] AND arrFlowDP_Health[3] THEN
    rFlowDP_Voted_mbar := (arrFlowDP_Raw[2] + arrFlowDP_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrFlowDP_Health[1] AND arrFlowDP_Health[3] THEN
    rFlowDP_Voted_mbar := (arrFlowDP_Raw[1] + arrFlowDP_Raw[3]) * 0.5;
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000020;
ELSIF arrFlowDP_Health[1] THEN
    rFlowDP_Voted_mbar := arrFlowDP_Raw[1];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSIF arrFlowDP_Health[2] THEN
    rFlowDP_Voted_mbar := arrFlowDP_Raw[2];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSIF arrFlowDP_Health[3] THEN
    rFlowDP_Voted_mbar := arrFlowDP_Raw[3];
    bDegradedSensorMode := TRUE;
    dwWarningWord2 := dwWarningWord2 OR 16#00000040;
ELSE
    rFlowDP_Voted_mbar := 0.0;
    dwAlarmWord1 := dwAlarmWord1 OR 16#00000008; (* Bit 3: Triple Flow DP Transmitter Failure *)
END_IF;

(* 2.4 TEMPERATURE & SHAFT SPEED 2oo3 VOTING *)
(* Suction Temperature Median Selection *)
IF (arrSuctTemp_Raw[1] >= arrSuctTemp_Raw[2] AND arrSuctTemp_Raw[1] <= arrSuctTemp_Raw[3]) OR
   (arrSuctTemp_Raw[1] >= arrSuctTemp_Raw[3] AND arrSuctTemp_Raw[1] <= arrSuctTemp_Raw[2]) THEN
    rSuctTemp_Voted_K := arrSuctTemp_Raw[1];
ELSIF (arrSuctTemp_Raw[2] >= arrSuctTemp_Raw[1] AND arrSuctTemp_Raw[2] <= arrSuctTemp_Raw[3]) OR
      (arrSuctTemp_Raw[2] >= arrSuctTemp_Raw[3] AND arrSuctTemp_Raw[2] <= arrSuctTemp_Raw[1]) THEN
    rSuctTemp_Voted_K := arrSuctTemp_Raw[2];
ELSE
    rSuctTemp_Voted_K := arrSuctTemp_Raw[3];
END_IF;
rSuctTemp_Voted_K := MAX(220.0, MIN(380.0, rSuctTemp_Voted_K));

(* Discharge Temperature Median Selection *)
IF (arrDischTemp_Raw[1] >= arrDischTemp_Raw[2] AND arrDischTemp_Raw[1] <= arrDischTemp_Raw[3]) OR
   (arrDischTemp_Raw[1] >= arrDischTemp_Raw[3] AND arrDischTemp_Raw[1] <= arrDischTemp_Raw[2]) THEN
    rDischTemp_Voted_K := arrDischTemp_Raw[1];
ELSIF (arrDischTemp_Raw[2] >= arrDischTemp_Raw[1] AND arrDischTemp_Raw[2] <= arrDischTemp_Raw[3]) OR
      (arrDischTemp_Raw[2] >= arrDischTemp_Raw[3] AND arrDischTemp_Raw[2] <= arrDischTemp_Raw[1]) THEN
    rDischTemp_Voted_K := arrDischTemp_Raw[2];
ELSE
    rDischTemp_Voted_K := arrDischTemp_Raw[3];
END_IF;
rDischTemp_Voted_K := MAX(220.0, MIN(450.0, rDischTemp_Voted_K));

(* Shaft Speed Median Selection *)
IF (arrSpeed_Raw[1] >= arrSpeed_Raw[2] AND arrSpeed_Raw[1] <= arrSpeed_Raw[3]) OR
   (arrSpeed_Raw[1] >= arrSpeed_Raw[3] AND arrSpeed_Raw[1] <= arrSpeed_Raw[2]) THEN
    rShaftSpeed_Voted_rpm := arrSpeed_Raw[1];
ELSIF (arrSpeed_Raw[2] >= arrSpeed_Raw[1] AND arrSpeed_Raw[2] <= arrSpeed_Raw[3]) OR
      (arrSpeed_Raw[2] >= arrSpeed_Raw[3] AND arrSpeed_Raw[2] <= arrSpeed_Raw[1]) THEN
    rShaftSpeed_Voted_rpm := arrSpeed_Raw[2];
ELSE
    rShaftSpeed_Voted_rpm := arrSpeed_Raw[3];
END_IF;
rShaftSpeed_Voted_rpm := MAX(0.0, MIN(25000.0, rShaftSpeed_Voted_rpm));

(* === 3. HIGH-PRESSURE HYDROGEN REAL-TIME THERMODYNAMICS & EQUATION OF STATE === *)
(* 3.1 Gas Composition & Molecular Weight Supervision *)
IF rGasMolecularWeight_gmol >= 1.80 AND rGasMolecularWeight_gmol <= 5.00 THEN
    rGasConstant_Rspec := c_rUniversalGasConstant / (rGasMolecularWeight_gmol * 0.001);
ELSE
    rGasConstant_Rspec := c_rUniversalGasConstant / (c_rNominalMolecularWeight_H2 * 0.001);
END_IF;

IF rGasSpecificHeatRatio >= 1.30 AND rGasSpecificHeatRatio <= 1.50 THEN
    rGamma := rGasSpecificHeatRatio;
ELSE
    rGamma := 1.405; (* Standard diatomic hydrogen specific heat ratio *)
END_IF;

(* 3.2 High-Pressure Compressibility Factor Z(P, T) via Virial EOS for Hydrogen *)
(* Z = 1 + [ b0 + b1*(300/T) ] * P_bar *)
rZ_Suct  := 1.0 + (0.00055 + 0.00015 * (300.0 / rSuctTemp_Voted_K)) * rSuctPress_Voted_bar;
rZ_Disch := 1.0 + (0.00055 + 0.00015 * (300.0 / rDischTemp_Voted_K)) * rDischPress_Voted_bar;
rZ_Avg   := (rZ_Suct + rZ_Disch) * 0.5;

(* 3.3 Suction Gas Density & Sonic Velocity *)
(* rho = (P * 10^5) / (Z * R_spec * T) [kg/m3] *)
rGasDensitySuction_kgm3 := (rSuctPress_Voted_bar * 100000.0) / (rZ_Suct * rGasConstant_Rspec * rSuctTemp_Voted_K);
rGasDensitySuction_kgm3 := MAX(0.5, MIN(25.0, rGasDensitySuction_kgm3));

(* Speed of sound: a = sqrt(gamma * Z * R_spec * T) [m/s] *)
rSpeedOfSound_ms := SQRT(rGamma * rZ_Avg * rGasConstant_Rspec * rSuctTemp_Voted_K);
rSpeedOfSound_ms := MAX(1000.0, MIN(1600.0, rSpeedOfSound_ms));

(* 3.4 Compression Ratio & Polytropic Head *)
IF rSuctPress_Voted_bar > 1.0 THEN
    rCompressionRatio := rDischPress_Voted_bar / rSuctPress_Voted_bar;
ELSE
    rCompressionRatio := 1.0;
END_IF;

(* Polytropic Exponent n and factor m = (n-1)/n, assuming stage polytropic efficiency approx 0.825 *)
rPolytropicFactor_m := (rGamma - 1.0) / (rGamma * 0.825);
rPolytropicExponent_n := 1.0 / (1.0 - rPolytropicFactor_m);

(* Polytropic Head: H_p = [ Z_avg * R_spec * T_suct / m ] * [ (Rc)^m - 1.0 ] [kJ/kg] *)
IF rCompressionRatio > 1.001 THEN
    rPolytropicHead_kJkg := (rZ_Avg * rGasConstant_Rspec * rSuctTemp_Voted_K / rPolytropicFactor_m) *
                            (EXPT(rCompressionRatio, rPolytropicFactor_m) - 1.0) * 0.001;
ELSE
    rPolytropicHead_kJkg := 0.0;
END_IF;
rPolytropicHead_kJkg := MAX(0.0, MIN(350.0, rPolytropicHead_kJkg));

(* 3.5 Mass Flow Rate & Reduced Flow Coordinates *)
(* Flow from differential pressure orifice: m_dot = C_d * eps * (pi/4)*d^2 * sqrt(2 * rho * DeltaP) *)
IF rFlowDP_Voted_mbar > 0.0 THEN
    rMassFlow_kgs := 0.0482 * SQRT(2.0 * rGasDensitySuction_kgm3 * (rFlowDP_Voted_mbar * 100.0));
ELSE
    rMassFlow_kgs := 0.0;
END_IF;
rActualVolumetricFlow_m3s := rMassFlow_kgs / rGasDensitySuction_kgm3;

(* Reduced Flow Squared: q_red^2 = (m_dot^2 * Z_suct * T_suct / MW) / P_suct^2 *)
IF rSuctPress_Voted_bar > 1.0 THEN
    rReducedFlow_Squared := (rMassFlow_kgs * rMassFlow_kgs * rZ_Suct * rSuctTemp_Voted_K /
                            (c_rNominalMolecularWeight_H2 * 0.001)) /
                            (rSuctPress_Voted_bar * rSuctPress_Voted_bar * 100.0);
ELSE
    rReducedFlow_Squared := 0.0;
END_IF;
"""
