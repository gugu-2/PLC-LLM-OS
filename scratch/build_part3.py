# Part 3: Phases 4, 5, 6
import os

code_part3 = '''
(* ==================================================================================================== *)
(* === PHASE 4: 8x8 DISCRETE STATE-SPACE PREDICTION & KALMAN OBSERVER                               === *)
(* ==================================================================================================== *)

(* 4.1 State-Space System Matrix Initialization at Ts = 2 ms *)
IF NOT bStateSpaceInitialized THEN
    (* Zero all 8x8 matrix elements *)
    FOR iLoopIndex_i := 1 TO 8 DO
        FOR iLoopIndex_j := 1 TO 8 DO
            aMatrixA[iLoopIndex_i, iLoopIndex_j] := 0.0;
            aMatrixB[iLoopIndex_i, iLoopIndex_j] := 0.0;
            aMatrixC[iLoopIndex_i, iLoopIndex_j] := 0.0;
            aMatrixD[iLoopIndex_i, iLoopIndex_j] := 0.0;
            aMatrixL[iLoopIndex_i, iLoopIndex_j] := 0.0;
        END_FOR;
        aStateVector_x[iLoopIndex_i]      := 0.0;
        aStateVector_x_pred[iLoopIndex_i] := 0.0;
        aInputVector_u[iLoopIndex_i]      := 0.0;
        aOutputVector_y[iLoopIndex_i]     := 0.0;
        aStateSetpoint_r[iLoopIndex_i]    := 0.0;
        aStateError_e[iLoopIndex_i]       := 0.0;
    END_FOR;

    (* Matrix A: System Dynamics (Coupled Thermal, Rheological, Chemical, Kinetic, and Hydraulic States) *)
    (* x1: True Melt Temp [deg C] *)
    aMatrixA[1, 1] :=  0.9982; (* Thermal mass relaxation pole *)
    aMatrixA[1, 7] :=  0.0015; (* SME heat dissipation coupling *)
    (* x2: Radical Grafting Conversion [%] *)
    aMatrixA[2, 1] :=  0.0008; (* Arrhenius temp acceleration *)
    aMatrixA[2, 2] :=  0.9960; (* Monomer conversion relaxation *)
    (* x3: Zero-Shear Viscosity Eta0 [Pa.s] *)
    aMatrixA[3, 1] := -0.0450; (* Thermal thinning *)
    aMatrixA[3, 2] :=  0.0220; (* Polar MAH functional branch thickening *)
    aMatrixA[3, 3] :=  0.9975; (* Viscosity viscoelastic relaxation pole *)
    (* x4: Barrel Channel Fill Degree [0..1] *)
    aMatrixA[4, 4] :=  0.9940; (* Inventory mass balance pole *)
    (* x5: Gear Pump Suction Pressure [bar] *)
    aMatrixA[5, 3] :=  0.0150; (* Viscosity head pressure generation *)
    aMatrixA[5, 4] :=  1.2500; (* Channel degree of fill pressurization *)
    aMatrixA[5, 5] :=  0.9880; (* Suction cavity pressure relaxation pole *)
    (* x6: Slit-Die Head Discharge Pressure [bar] *)
    aMatrixA[6, 3] :=  0.0350; (* Melt viscosity directly scales die backpressure *)
    aMatrixA[6, 6] :=  0.9850; (* Die viscoelastic relaxation pole *)
    (* x7: Specific Mechanical Energy [kWh/ton] *)
    aMatrixA[7, 3] :=  0.0012; (* Higher melt viscosity increases shear torque *)
    aMatrixA[7, 7] :=  0.9920; (* Motor shaft electromechanical pole *)
    (* x8: MFI Deviation [g/10min] *)
    aMatrixA[8, 3] := -0.0018; (* Viscosity inverse power coupling *)
    aMatrixA[8, 8] :=  0.9965; (* MFI persistence pole *)

    (* Matrix B: Control Actuator Coupling Matrix *)
    (* u1: Screw Speed [rpm] *)
    aMatrixB[1, 1] :=  0.0024; (* Screw speed viscous shear heating *)
    aMatrixB[4, 1] := -0.00015;(* Higher screw speed clears flight channels faster *)
    aMatrixB[5, 1] :=  0.0450; (* Screw speed pumps melt into gear pump suction *)
    aMatrixB[7, 1] :=  0.0850; (* Screw speed drives up SME *)
    (* u2: Main Feeder [kg/h] *)
    aMatrixB[4, 2] :=  0.00008;(* Base resin delivery increases fill degree *)
    aMatrixB[5, 2] :=  0.0120; (* Main throughput feeds gear pump suction *)
    aMatrixB[7, 2] := -0.0240; (* Higher throughput slightly reduces SME per ton *)
    (* u3: Side Feeder Monomer [kg/h] *)
    aMatrixB[2, 3] :=  0.0350; (* Monomer addition increases grafting yield *)
    (* u4: Peroxide Pump Stroke [%] *)
    aMatrixB[2, 4] :=  0.0120; (* Peroxide initiator triggers radical grafting *)
    aMatrixB[3, 4] := -0.0550; (* Peroxide beta-scission degrades polymer chains *)
    aMatrixB[8, 4] :=  0.0045; (* Beta-scission directly raises MFI *)
    (* u5: Melt Gear Pump Speed [rpm] *)
    aMatrixB[5, 5] := -0.3800; (* Gear pump speed draws down suction cavity *)
    aMatrixB[6, 5] :=  0.4200; (* Gear pump speed directly drives die head pressure *)
    (* u6: Barrel Reactive Zone Heating Duty [%] *)
    aMatrixB[1, 6] :=  0.0045; (* Induction heater power input *)
    (* u7: Barrel Reactive Zone CO2 Cooling Duty [%] *)
    aMatrixB[1, 7] := -0.0085; (* Supercritical CO2 direct cooling enthalpy extraction *)
    (* u8: Slit-Die Heating Duty [%] *)
    aMatrixB[6, 8] := -0.0250; (* Die wall heating lowers wall viscosity and die pressure *)

    (* Matrix C: Output Measurement Mapping Matrix (Identity / Transducer Scales) *)
    aMatrixC[1, 1] := 1.0; (* y1 = True Melt Temp *)
    aMatrixC[2, 2] := 1.0; (* y2 = Grafting Conversion *)
    aMatrixC[3, 3] := 1.0; (* y3 = Observed Viscosity *)
    aMatrixC[4, 4] := 1.0; (* y4 = Degree of Fill *)
    aMatrixC[5, 5] := 1.0; (* y5 = Gear Pump Suction Pressure *)
    aMatrixC[6, 6] := 1.0; (* y6 = Slit-Die Head Pressure *)
    aMatrixC[7, 7] := 1.0; (* y7 = Calculated SME *)
    aMatrixC[8, 8] := 1.0; (* y8 = Melt Flow Index *)

    (* Matrix L: Kalman / Luenberger Observer Gain Matrix (Diagonal Innovation Weights) *)
    aMatrixL[1, 1] := 0.0850;
    aMatrixL[2, 2] := 0.0450;
    aMatrixL[3, 3] := 0.1200;
    aMatrixL[4, 4] := 0.0650;
    aMatrixL[5, 5] := 0.2500;
    aMatrixL[6, 6] := 0.3200;
    aMatrixL[7, 7] := 0.0950;
    aMatrixL[8, 8] := 0.1800;

    (* MPC Cost Weight Matrices *)
    aWeightQ[1] :=  65.0;  (* Melt temp penalty *)
    aWeightQ[2] :=  45.0;  (* Grafting conversion penalty *)
    aWeightQ[3] :=  55.0;  (* Viscosity penalty *)
    aWeightQ[4] :=  30.0;  (* Degree of fill penalty *)
    aWeightQ[5] :=  85.0;  (* Gear pump suction pressure stability penalty *)
    aWeightQ[6] := 250.0;  (* Die head pressure penalty (CRITICAL: +/- 0.5 bar stability) *)
    aWeightQ[7] :=  40.0;  (* SME optimization penalty *)
    aWeightQ[8] := 180.0;  (* MFI precision penalty (CRITICAL: +/- 1.5% target) *)

    aWeightR[1] :=  0.15;  (* Screw speed effort *)
    aWeightR[2] :=  0.10;  (* Main feeder effort *)
    aWeightR[3] :=  0.25;  (* Side feeder effort *)
    aWeightR[4] :=  0.85;  (* Peroxide pump dosing effort *)
    aWeightR[5] :=  0.20;  (* Gear pump speed effort *)
    aWeightR[6] :=  0.05;  (* Induction heating effort *)
    aWeightR[7] :=  0.08;  (* CO2 cooling effort *)
    aWeightR[8] :=  0.05;  (* Die heating effort *)

    aWeightS[1] :=  1.50;  (* Screw speed slew rate penalty *)
    aWeightS[2] :=  1.00;  (* Main feeder slew penalty *)
    aWeightS[3] :=  2.50;  (* Side feeder slew penalty *)
    aWeightS[4] :=  5.00;  (* Peroxide stroke slew penalty *)
    aWeightS[5] :=  2.00;  (* Gear pump speed slew penalty *)
    aWeightS[6] :=  0.50;  (* Heater duty slew penalty *)
    aWeightS[7] :=  0.80;  (* Cooler duty slew penalty *)
    aWeightS[8] :=  0.50;  (* Die heater slew penalty *)

    FOR iLoopIndex_i := 1 TO 8 DO
        aWeightP[iLoopIndex_i] := aWeightQ[iLoopIndex_i] * 3.5; (* Terminal cost heuristic *)
    END_FOR;

    (* Actuator Hard Saturation Constraints *)
    aInputMin[1] := 0.0;     aInputMax[1] := 1200.0; aDeltaInputMax[1] := 15.0;  (* Screw Speed [rpm] *)
    aInputMin[2] := 0.0;     aInputMax[2] := 2800.0; aDeltaInputMax[2] := 35.0;  (* Main Feeder [kg/h] *)
    aInputMin[3] := 0.0;     aInputMax[3] :=  250.0; aDeltaInputMax[3] :=  5.0;  (* Side Feeder [kg/h] *)
    aInputMin[4] := 0.0;     aInputMax[4] :=  100.0; aDeltaInputMax[4] :=  2.0;  (* Peroxide Stroke [%] *)
    aInputMin[5] := 0.0;     aInputMax[5] :=   95.0; aDeltaInputMax[5] :=  1.5;  (* Gear Pump Speed [rpm] *)
    aInputMin[6] := 0.0;     aInputMax[6] :=  100.0; aDeltaInputMax[6] :=  5.0;  (* Zone Heat [%] *)
    aInputMin[7] := 0.0;     aInputMax[7] :=  100.0; aDeltaInputMax[7] :=  5.0;  (* Zone Cool [%] *)
    aInputMin[8] := 0.0;     aInputMax[8] :=  100.0; aDeltaInputMax[8] :=  4.0;  (* Die Heat [%] *)

    bStateSpaceInitialized := TRUE;
END_IF;

(* 4.2 Measurement Vector Assembly & Observer Innovation *)
aMeasurementVector_z[1] := rTrueMeltTemp_Voted_degC;
aMeasurementVector_z[2] := rGraftingConversion_pct;
aMeasurementVector_z[3] := rObservedViscosity_Pas;
aMeasurementVector_z[4] := rDegreeOfFill_pct * 0.01;
aMeasurementVector_z[5] := rGearPumpSuction_Voted_bar;
aMeasurementVector_z[6] := rDiePressure_Voted_bar;
aMeasurementVector_z[7] := rCalculatedSME_kWh_ton;
aMeasurementVector_z[8] := rEstimatedMFI_g10min;

(* Desired Reference Setpoint Vector *)
aStateSetpoint_r[1] := aBarrelTempSetpoints_degC[6];
aStateSetpoint_r[2] := 85.0; (* 85% target grafting conversion *)
aStateSetpoint_r[3] := rCrossModelViscosity_Pas;
aStateSetpoint_r[4] := 0.55; (* 55% optimal fill fraction *)
aStateSetpoint_r[5] := rTargetGearPumpInletPressure_bar;
aStateSetpoint_r[6] := rTargetDiePressure_bar;
aStateSetpoint_r[7] := 0.185; (* 0.185 kWh/kg = 185 kWh/t optimal SME *)
aStateSetpoint_r[8] := rTargetMFI_g10min;

(* Output Estimation: y = C * x_pred *)
FOR iLoopIndex_i := 1 TO 8 DO
    aOutputVector_y[iLoopIndex_i] := 0.0;
    FOR iLoopIndex_j := 1 TO 8 DO
        aOutputVector_y[iLoopIndex_i] := aOutputVector_y[iLoopIndex_i] + (aMatrixC[iLoopIndex_i, iLoopIndex_j] * aStateVector_x_pred[iLoopIndex_j]);
    END_FOR;
    (* Innovation error: e_y = z - y *)
    aObserverInnovation_y_err[iLoopIndex_i] := aMeasurementVector_z[iLoopIndex_i] - aOutputVector_y[iLoopIndex_i];
END_FOR;

(* State Update with Observer Gain: x_corr = x_pred + L * e_y *)
FOR iLoopIndex_i := 1 TO 8 DO
    rTempCalc_A := 0.0;
    FOR iLoopIndex_j := 1 TO 8 DO
        rTempCalc_A := rTempCalc_A + (aMatrixL[iLoopIndex_i, iLoopIndex_j] * aObserverInnovation_y_err[iLoopIndex_j]);
    END_FOR;
    aStateVector_x[iLoopIndex_i] := aStateVector_x_pred[iLoopIndex_i] + rTempCalc_A;
    aStateError_e[iLoopIndex_i] := aStateSetpoint_r[iLoopIndex_i] - aStateVector_x[iLoopIndex_i];
END_FOR;

(* Prior State Propagation for Next Sample: x_pred[k+1] = A * x_corr[k] + B * u[k] *)
FOR iLoopIndex_i := 1 TO 8 DO
    rTempCalc_A := 0.0;
    rTempCalc_B := 0.0;
    FOR iLoopIndex_j := 1 TO 8 DO
        rTempCalc_A := rTempCalc_A + (aMatrixA[iLoopIndex_i, iLoopIndex_j] * aStateVector_x[iLoopIndex_j]);
        rTempCalc_B := rTempCalc_B + (aMatrixB[iLoopIndex_i, iLoopIndex_j] * aInputVector_u[iLoopIndex_j]);
    END_FOR;
    aStateVector_x_pred[iLoopIndex_i] := rTempCalc_A + rTempCalc_B;
END_FOR;

(* ==================================================================================================== *)
(* === PHASE 5: RECEDING-HORIZON MPC OPTIMIZATION & DECOUPLED ACTUATION                              === *)
(* ==================================================================================================== *)

(* 5.1 Quadratic Cost Gradient Projection Solver *)
rMPC_ObjectiveCost_J := 0.0;
FOR iLoopIndex_i := 1 TO 8 DO
    (* State penalty: e^T * Q * e *)
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (aStateError_e[iLoopIndex_i] * aWeightQ[iLoopIndex_i] * aStateError_e[iLoopIndex_i]);
    (* Actuator penalty: u^T * R * u *)
    rMPC_ObjectiveCost_J := rMPC_ObjectiveCost_J + (aInputVector_u[iLoopIndex_i] * aWeightR[iLoopIndex_i] * aInputVector_u[iLoopIndex_i]);
END_FOR;

(* Active-Set Quadratic Descent Iterations (3 Iterations per 2 ms scan) *)
FOR iMPCIterationCounter := 1 TO 3 DO
    FOR iLoopIndex_i := 1 TO 8 DO
        (* Compute negative gradient: grad_i = sum_k (B_ki * Q_k * e_k) - R_i * u_i *)
        rTempCalc_A := 0.0;
        FOR iLoopIndex_j := 1 TO 8 DO
            rTempCalc_A := rTempCalc_A + (aMatrixB[iLoopIndex_j, iLoopIndex_i] * aWeightQ[iLoopIndex_j] * aStateError_e[iLoopIndex_j]);
        END_FOR;
        rTempCalc_A := rTempCalc_A - (aWeightR[iLoopIndex_i] * aInputVector_u[iLoopIndex_i]);

        (* Slew-rate incremental step *)
        aOptimalDeltaU[iLoopIndex_i] := 0.05 * rTempCalc_A;

        (* Enforce slew rate constraint *)
        IF aOptimalDeltaU[iLoopIndex_i] > aDeltaInputMax[iLoopIndex_i] THEN
            aOptimalDeltaU[iLoopIndex_i] := aDeltaInputMax[iLoopIndex_i];
        ELSIF aOptimalDeltaU[iLoopIndex_i] < (-1.0 * aDeltaInputMax[iLoopIndex_i]) THEN
            aOptimalDeltaU[iLoopIndex_i] := -1.0 * aDeltaInputMax[iLoopIndex_i];
        END_IF;

        (* Trial update *)
        aInputVector_u[iLoopIndex_i] := aInputVector_u[iLoopIndex_i] + aOptimalDeltaU[iLoopIndex_i];

        (* Enforce hard box actuator limits *)
        IF aInputVector_u[iLoopIndex_i] > aInputMax[iLoopIndex_i] THEN
            aInputVector_u[iLoopIndex_i] := aInputMax[iLoopIndex_i];
        ELSIF aInputVector_u[iLoopIndex_i] < aInputMin[iLoopIndex_i] THEN
            aInputVector_u[iLoopIndex_i] := aInputMin[iLoopIndex_i];
        END_IF;
    END_FOR;
END_FOR;

(* ==================================================================================================== *)
(* === PHASE 6: MULTI-PORT GRAVIMETRIC FEEDER SYNCHRONIZATION & GEAR PUMP ANTI-SURGE                 === *)
(* ==================================================================================================== *)

(* 6.1 Multi-Port Loss-in-Weight Feeder Synchronization *)
IF bEnable AND (iFSM_State >= 5) THEN
    (* Base resin gravimetric delivery setpoint *)
    rFeederMainCmd_kgh := rThroughputSetPoint_kgh * (rBaseResinRatio_pct * 0.01);
    IF rFeederMainCmd_kgh > 2600.0 THEN rFeederMainCmd_kgh := 2600.0; END_IF;

    (* Side stuffer functional monomer delivery setpoint *)
    IF iFSM_State >= 6 THEN
        rFeederSideCmd_kgh := rThroughputSetPoint_kgh * (rSideMonomerRatio_pct * 0.01);
        IF rFeederSideCmd_kgh > 200.0 THEN rFeederSideCmd_kgh := 200.0; END_IF;

        (* Peroxide micro-dosing pump: concentration in ppm *)
        rPeroxidePumpCmd_pct := (rThroughputSetPoint_kgh * (rPeroxideConcentration_ppm * 0.000001) / 25.0) * 100.0;
        IF rPeroxidePumpCmd_pct < 0.0 THEN rPeroxidePumpCmd_pct := 0.0; END_IF;
        IF rPeroxidePumpCmd_pct > 100.0 THEN rPeroxidePumpCmd_pct := 100.0; END_IF;
    ELSE
        rFeederSideCmd_kgh := 0.0;
        rPeroxidePumpCmd_pct := 0.0;
    END_IF;
ELSE
    rFeederMainCmd_kgh := 0.0;
    rFeederSideCmd_kgh := 0.0;
    rPeroxidePumpCmd_pct := 0.0;
END_IF;

(* 6.2 Melt Gear Pump Pressure Decoupling & Active Anti-Surge Stabilization *)
(* Die Entrance Head Pressure Rate-of-Change [bar/s] *)
rDiePressureROC_bars := (rDiePressure_Voted_bar - rPrevDiePressure_bar) / c_Ts_s;
rPrevDiePressure_bar := rDiePressure_Voted_bar;

(* Volumetric Efficiency eta_vol of positive displacement gear pump *)
rTempCalc_A := rDiePressure_Voted_bar - rGearPumpSuction_Voted_bar;
IF rTempCalc_A < 0.0 THEN rTempCalc_A := 0.0; END_IF;
IF rObservedViscosity_Pas > 10.0 THEN
    rVolumetricEfficiency_eta := 1.0 - (c_rGearPumpSlipFactor * (rTempCalc_A * 100000.0) / rObservedViscosity_Pas);
ELSE
    rVolumetricEfficiency_eta := 0.95;
END_IF;
IF rVolumetricEfficiency_eta < 0.65 THEN rVolumetricEfficiency_eta := 0.65; END_IF;
IF rVolumetricEfficiency_eta > 0.99 THEN rVolumetricEfficiency_eta := 0.99; END_IF;

(* Feedforward Gear Pump Speed: N_gp = Q / (V_disp * eta_vol * 60) *)
IF (rVolumetricThroughput_m3s > 0.000001) AND (c_rGearPumpDisplacement_m3 > 0.00001) THEN
    rGearPumpFeedforwardSpeed_rpm := (rVolumetricThroughput_m3s) /
                                     (c_rGearPumpDisplacement_m3 * rVolumetricEfficiency_eta * 60.0);
ELSE
    rGearPumpFeedforwardSpeed_rpm := 0.0;
END_IF;

(* Closed-Loop Feedback PID Trim on Die Discharge Pressure (Target: 250.0 bar +/- 0.5 bar) *)
rGearPumpPressureError_bar := rTargetDiePressure_bar - rDiePressure_Voted_bar;

(* Small deadband of 0.15 bar to prevent high-frequency servo chattering *)
IF ABS(rGearPumpPressureError_bar) > 0.15 THEN
    rGearPumpIntegral_bar_s := rGearPumpIntegral_bar_s + (rGearPumpPressureError_bar * c_Ts_s);
    (* Anti-windup clamping *)
    IF rGearPumpIntegral_bar_s > 15.0 THEN rGearPumpIntegral_bar_s := 15.0; END_IF;
    IF rGearPumpIntegral_bar_s < -15.0 THEN rGearPumpIntegral_bar_s := -15.0; END_IF;
END_IF;

(* Active Anti-Surge Damping Lead-Lag Filter: rapidly counteracts pressure surges *)
IF ABS(rDiePressureROC_bars) > 8.0 THEN
    rAntiSurgeDampingTrim_rpm := -0.045 * rDiePressureROC_bars;
    IF rAntiSurgeDampingTrim_rpm > 6.0 THEN rAntiSurgeDampingTrim_rpm := 6.0; END_IF;
    IF rAntiSurgeDampingTrim_rpm < -6.0 THEN rAntiSurgeDampingTrim_rpm := -6.0; END_IF;
ELSE
    rAntiSurgeDampingTrim_rpm := 0.0;
END_IF;

(* Net Gear Pump Command *)
IF bEnable AND (iFSM_State >= 5) AND NOT bDieFreezeInterlockActive THEN
    rGearPumpSpeedCmd_rpm := rGearPumpFeedforwardSpeed_rpm +
                             (0.28 * rGearPumpPressureError_bar) +
                             (0.04 * rGearPumpIntegral_bar_s) +
                             rAntiSurgeDampingTrim_rpm;
    IF rGearPumpSpeedCmd_rpm < 1.0 THEN rGearPumpSpeedCmd_rpm := 1.0; END_IF;
    IF rGearPumpSpeedCmd_rpm > 95.0 THEN rGearPumpSpeedCmd_rpm := 95.0; END_IF;
ELSE
    rGearPumpSpeedCmd_rpm := 0.0;
    rGearPumpIntegral_bar_s := 0.0;
END_IF;

(* 6.3 Twin-Screw Drive Speed Regulation & Gear Pump Suction Head Balancing *)
rGearPumpSuctionError_bar := rTargetGearPumpInletPressure_bar - rGearPumpSuction_Voted_bar;
IF ABS(rGearPumpSuctionError_bar) > 0.5 THEN
    rGearPumpSuctionIntegral_bar_s := rGearPumpSuctionIntegral_bar_s + (rGearPumpSuctionError_bar * c_Ts_s);
    IF rGearPumpSuctionIntegral_bar_s > 40.0 THEN rGearPumpSuctionIntegral_bar_s := 40.0; END_IF;
    IF rGearPumpSuctionIntegral_bar_s < -40.0 THEN rGearPumpSuctionIntegral_bar_s := -40.0; END_IF;
END_IF;

IF bEnable AND (iFSM_State >= 4) AND NOT bColdStartInterlockActive THEN
    IF iFSM_State = 4 THEN
        (* Low-speed jog start *)
        rScrewSpeedCmd_rpm := 50.0;
    ELSE
        (* Normal compounding speed trimmed to maintain 35.0 bar suction pressure *)
        rScrewSpeedCmd_rpm := rScrewSpeedNominal_rpm +
                              (1.85 * rGearPumpSuctionError_bar) +
                              (0.12 * rGearPumpSuctionIntegral_bar_s);
        IF rScrewSpeedCmd_rpm < 40.0 THEN rScrewSpeedCmd_rpm := 40.0; END_IF;
        IF rScrewSpeedCmd_rpm > 1150.0 THEN rScrewSpeedCmd_rpm := 1150.0; END_IF;
    END_IF;
ELSE
    rScrewSpeedCmd_rpm := 0.0;
    rGearPumpSuctionIntegral_bar_s := 0.0;
END_IF;
'''

with open('scratch/code_part3.st', 'w', encoding='utf-8') as f:
    f.write(code_part3)
print("Part 3 written, len =", len(code_part3))
