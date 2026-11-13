# ldpe_reactor_builder/st_phase2_observers.py

def get_phase2_observers():
    return """(* ============================================================================================== *)
(* PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION (6X6 SYSTEM)                   *)
(* DISCRETE MATRICES A, B, C, D AND OBSERVER GAIN L_OBS                                          *)
(* CALORIMETRIC HEAT BALANCE, AXIAL EXOTHERM PEAK TRACKING, WALL GEL FOULING & MFI PREDICTION    *)
(* ============================================================================================== *)

(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.1: INITIALIZATION OF DISCRETE STATE-SPACE MATRICES A, B, C, D & OBSERVER L_OBS        *)
(* Sample Period Ts = 0.005 s, Linearized at P = 3,050 bar, T_peak = 302 C, Feed = 115 t/h        *)
(* ---------------------------------------------------------------------------------------------- *)
IF NOT bMatricesInitialized THEN
    (* System Matrix A (6x6): Discrete Transition Dynamics *)
    (* Row 1: T_peak dynamics (thermal inertia, convection along tube) *)
    matA[1, 1] := 0.9882;  matA[1, 2] := 0.0035;  matA[1, 3] := 0.0012;  matA[1, 4] := 0.0000;  matA[1, 5] := 0.4250;  matA[1, 6] := 0.0000;
    (* Row 2: Z_peak spatial location (axial velocity tracking ~ 12 m/s) *)
    matA[2, 1] := 0.0450;  matA[2, 2] := 0.9915;  matA[2, 3] := 0.0085;  matA[2, 4] := -0.0042; matA[2, 5] := -0.1250; matA[2, 6] := 0.0000;
    (* Row 3: P_inlet pressure dynamics (supercritical acoustic capacitance & hyper-compressor flow) *)
    matA[3, 1] := 0.0120;  matA[3, 2] := 0.0000;  matA[3, 3] := 0.9765;  matA[3, 4] := 0.0185;  matA[3, 5] := 0.0050;  matA[3, 6] := 0.0000;
    (* Row 4: P_outlet pressure dynamics (letdown throttle valve pressure drop) *)
    matA[4, 1] := 0.0080;  matA[4, 2] := 0.0000;  matA[4, 3] := 0.0220;  matA[4, 4] := 0.9680;  matA[4, 5] := 0.0085;  matA[4, 6] := 0.0000;
    (* Row 5: X_conv monomer conversion rate (free-radical initiation & propagation rate) *)
    matA[5, 1] := 0.0215;  matA[5, 2] := 0.0012;  matA[5, 3] := 0.0045;  matA[5, 4] := 0.0000;  matA[5, 5] := 0.9820;  matA[5, 6] := 0.0000;
    (* Row 6: MFI melt flow index (chain transfer, beta-scission, and molecular weight distribution) *)
    matA[6, 1] := 0.0055;  matA[6, 2] := 0.0000;  matA[6, 3] := -0.0028; matA[6, 4] := 0.0000;  matA[6, 5] := -0.0180; matA[6, 6] := 0.9940;

    (* Input Coupling Matrix B (6x4) *)
    (* Inputs: [1: Q_comp_trim, 2: S_perox_trim, 3: u_HPLDV_trim, 4: u_jkt_trim] *)
    matB[1, 1] := -0.0450; matB[1, 2] := 0.8500;  matB[1, 3] := 0.0120;  matB[1, 4] := -0.6200;
    matB[2, 1] := 0.6500;  matB[2, 2] := -1.2500; matB[2, 3] := 0.0450;  matB[2, 4] := 0.4800;
    matB[3, 1] := 1.8500;  matB[3, 2] := 0.0350;  matB[3, 3] := -2.4500; matB[3, 4] := 0.0150;
    matB[4, 1] := 0.4500;  matB[4, 2] := 0.0280;  matB[4, 3] := -3.8500; matB[4, 4] := 0.0220;
    matB[5, 1] := -0.0320; matB[5, 2] := 0.2850;  matB[5, 3] := 0.0050;  matB[5, 4] := -0.0850;
    matB[6, 1] := -0.0150; matB[6, 2] := -0.0650; matB[6, 3] := 0.0025;  matB[6, 4] := 0.0280;

    (* Measurement Coupling Matrix C (6x6) *)
    matC[1, 1] := 1.0; matC[1, 2] := 0.0; matC[1, 3] := 0.0; matC[1, 4] := 0.0; matC[1, 5] := 0.0; matC[1, 6] := 0.0;
    matC[2, 1] := 0.0; matC[2, 2] := 1.0; matC[2, 3] := 0.0; matC[2, 4] := 0.0; matC[2, 5] := 0.0; matC[2, 6] := 0.0;
    matC[3, 1] := 0.0; matC[3, 2] := 0.0; matC[3, 3] := 1.0; matC[3, 4] := 0.0; matC[3, 5] := 0.0; matC[3, 6] := 0.0;
    matC[4, 1] := 0.0; matC[4, 2] := 0.0; matC[4, 3] := 0.0; matC[4, 4] := 1.0; matC[4, 5] := 0.0; matC[4, 6] := 0.0;
    matC[5, 1] := 0.0; matC[5, 2] := 0.0; matC[5, 3] := 0.0; matC[5, 4] := 0.0; matC[5, 5] := 1.0; matC[5, 6] := 0.0;
    matC[6, 1] := 0.0; matC[6, 2] := 0.0; matC[6, 3] := 0.0; matC[6, 4] := 0.0; matC[6, 5] := 0.0; matC[6, 6] := 1.0;

    (* Direct Transmission Matrix D (6x4) *)
    FOR idx_i := 1 TO 6 DO
        FOR idx_j := 1 TO 4 DO
            matD[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* Observer Innovation Feedback Gain Matrix L_obs (6x6) *)
    matL_Obs[1, 1] := 0.1850; matL_Obs[1, 2] := 0.0025; matL_Obs[1, 3] := 0.0005; matL_Obs[1, 4] := 0.0000; matL_Obs[1, 5] := 0.0450; matL_Obs[1, 6] := 0.0000;
    matL_Obs[2, 1] := 0.0120; matL_Obs[2, 2] := 0.2250; matL_Obs[2, 3] := 0.0015; matL_Obs[2, 4] := 0.0000; matL_Obs[2, 5] := 0.0180; matL_Obs[2, 6] := 0.0000;
    matL_Obs[3, 1] := 0.0008; matL_Obs[3, 2] := 0.0000; matL_Obs[3, 3] := 0.3150; matL_Obs[3, 4] := 0.0240; matL_Obs[3, 5] := 0.0020; matL_Obs[3, 6] := 0.0000;
    matL_Obs[4, 1] := 0.0005; matL_Obs[4, 2] := 0.0000; matL_Obs[4, 3] := 0.0280; matL_Obs[4, 4] := 0.2950; matL_Obs[4, 5] := 0.0015; matL_Obs[4, 6] := 0.0000;
    matL_Obs[5, 1] := 0.0150; matL_Obs[5, 2] := 0.0010; matL_Obs[5, 3] := 0.0012; matL_Obs[5, 4] := 0.0005; matL_Obs[5, 5] := 0.1650; matL_Obs[5, 6] := 0.0000;
    matL_Obs[6, 1] := 0.0025; matL_Obs[6, 2] := 0.0000; matL_Obs[6, 3] := -0.0010;matL_Obs[6, 4] := 0.0000; matL_Obs[6, 5] := -0.0120;matL_Obs[6, 6] := 0.1450;

    (* Initialize State Vector Estimates with Nominal Recipe Conditions *)
    vecX_Est[iState_Tpeak] := rRecipe_PeakTemp_Target_degC;
    vecX_Est[iState_Zpeak] := rRecipe_PeakLocation_Target_m;
    vecX_Est[iState_Pinlet] := rRecipe_TargetReactorPressure_bar;
    vecX_Est[iState_Poutlet] := rRecipe_TargetReactorPressure_bar - 180.0;
    vecX_Est[iState_Xconv] := rRecipe_TargetConversion_pct;
    vecX_Est[iState_MFI] := rRecipe_TargetMFI_g10min;

    (* Initialize Control Bounds & Slew Limits *)
    vecU_Min[iInput_HyperCompTrim] := -15.0;  vecU_Max[iInput_HyperCompTrim] := 15.0;  vecDeltaU_Max[iInput_HyperCompTrim] := 0.50;
    vecU_Min[iInput_PeroxMasterTrim] := -25.0;vecU_Max[iInput_PeroxMasterTrim] := 25.0;vecDeltaU_Max[iInput_PeroxMasterTrim] := 1.25;
    vecU_Min[iInput_HPLDVBaseTrim] := -20.0;  vecU_Max[iInput_HPLDVBaseTrim] := 20.0;  vecDeltaU_Max[iInput_HPLDVBaseTrim] := 2.50;
    vecU_Min[iInput_JacketWaterTrim] := -30.0;vecU_Max[iInput_JacketWaterTrim] := 30.0;vecDeltaU_Max[iInput_JacketWaterTrim] := 1.50;

    bMatricesInitialized := TRUE;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.2: SENSOR RECONSTRUCTION & MULTI-ZONE EXOTHERM PEAK LOCALIZATION                        *)
(* ---------------------------------------------------------------------------------------------- *)
(* Peak Exotherm Temperature & Axial Location Z_peak Search Across Zones Along 1,500 m Tube *)
(* Zone 1 (300-600 m), Zone 2 (600-900 m), Zone 3 (900-1200 m), Zone 4 (1200-1500 m) *)
rTempCalc1 := rTemp_Zone1_Reaction_degC;
rTempCalc2 := 450.0; (* Zone 1 Midpoint [m] *)

IF rTemp_Zone2_Reaction_degC > rTempCalc1 THEN
    rTempCalc1 := rTemp_Zone2_Reaction_degC;
    rTempCalc2 := 750.0; (* Zone 2 Midpoint [m] *)
END_IF;

IF rTemp_Zone3_Reaction_degC > rTempCalc1 THEN
    rTempCalc1 := rTemp_Zone3_Reaction_degC;
    rTempCalc2 := 1050.0; (* Zone 3 Midpoint [m] *)
END_IF;

IF rTemp_Zone4_Reaction_degC > rTempCalc1 THEN
    rTempCalc1 := rTemp_Zone4_Reaction_degC;
    rTempCalc2 := 1350.0; (* Zone 4 Midpoint [m] *)
END_IF;

(* Parabolic 3-Point Interpolation for Exact Axial Peak Location Z_peak [m] *)
IF (rTempCalc2 >= 700.0) AND (rTempCalc2 <= 800.0) THEN
    (* Peak in Zone 2: Interpolate with Zone 1 and Zone 3 *)
    rTempCalc3 := (rTemp_Zone1_Reaction_degC - 2.0 * rTemp_Zone2_Reaction_degC + rTemp_Zone3_Reaction_degC);
    IF ABS(rTempCalc3) > 0.05 THEN
        rTempCalc4 := 750.0 - (300.0 * (rTemp_Zone3_Reaction_degC - rTemp_Zone1_Reaction_degC)) / (2.0 * rTempCalc3);
        IF rTempCalc4 >= 300.0 AND rTempCalc4 <= 1450.0 THEN
            rTempCalc2 := rTempCalc4;
        END_IF;
    END_IF;
ELSIF (rTempCalc2 >= 1000.0) AND (rTempCalc2 <= 1100.0) THEN
    (* Peak in Zone 3: Interpolate with Zone 2 and Zone 4 *)
    rTempCalc3 := (rTemp_Zone2_Reaction_degC - 2.0 * rTemp_Zone3_Reaction_degC + rTemp_Zone4_Reaction_degC);
    IF ABS(rTempCalc3) > 0.05 THEN
        rTempCalc4 := 1050.0 - (300.0 * (rTemp_Zone4_Reaction_degC - rTemp_Zone2_Reaction_degC)) / (2.0 * rTempCalc3);
        IF rTempCalc4 >= 300.0 AND rTempCalc4 <= 1450.0 THEN
            rTempCalc2 := rTempCalc4;
        END_IF;
    END_IF;
END_IF;

(* Reconstruct Observation Vector y_meas from Voted Telemetry *)
vecY_Meas[1] := rVoted_PeakTemperature_degC;
vecY_Meas[2] := rTempCalc2; (* Calculated Spatial Peak Location Z_peak [m] *)
vecY_Meas[3] := rVoted_ReactorPressure_bar;
vecY_Meas[4] := rVoted_ReactorPressure_bar - (120.0 + (rRecipe_EthyleneFeedRate_tph / 115.0) * 60.0); (* Outlet Pressure *)

(* Single-Pass Conversion X_conv [%] derived from Calorimetric Heat Balance *)
(* Delta H_rxn = 3,550 kJ/kg; Adiabatic heat capacity = 2.65 kJ/kg K *)
rTempCalc1 := (rVoted_PeakTemperature_degC - rTemp_InletZone_degC);
IF rTempCalc1 < 0.0 THEN
    rTempCalc1 := 0.0;
END_IF;
(* Approx 1% conversion per 13.4 deg C temperature rise plus heat extracted to cooling jacket *)
rTempCalc2 := (rTempCalc1 / 13.4) + ((rJacketWater_ReturnTemp_degC - rJacketWater_SupplyTemp_degC) * 0.32);
IF rTempCalc2 < 0.0 THEN
    rTempCalc2 := 0.0;
ELSIF rTempCalc2 > 42.0 THEN
    rTempCalc2 := 42.0;
END_IF;
vecY_Meas[5] := rTempCalc2;

(* Melt Flow Index MFI [g/10min] derived from CTA, Temperature and Pressure Correlation *)
(* Log10(MFI) ~ k1*CTA + k2*T_peak - k3*P_inlet *)
rTempCalc3 := 0.0018 * rRecipe_CTA_Concentration_ppm + 0.012 * (rVoted_PeakTemperature_degC - 300.0) - 0.0015 * (rVoted_ReactorPressure_bar - 3000.0);
(* Linear approximation around operating point MFI = 2.10 *)
rTempCalc4 := 2.10 * (1.0 + rTempCalc3);
IF rTempCalc4 < 0.10 THEN
    rTempCalc4 := 0.10;
ELSIF rTempCalc4 > 50.0 THEN
    rTempCalc4 := 50.0;
END_IF;
vecY_Meas[6] := rTempCalc4;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.3: ONE-STEP AHEAD STATE PREDICTION: x_pred = A * x_est + B * u_prev                     *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idx_i := 1 TO 6 DO
    vecX_Pred[idx_i] := 0.0;
    (* State Transition Product A * x_est *)
    FOR idx_j := 1 TO 6 DO
        vecX_Pred[idx_i] := vecX_Pred[idx_i] + (matA[idx_i, idx_j] * vecX_Est[idx_j]);
    END_FOR;
    (* Control Coupling Product B * u_prev *)
    FOR idx_m := 1 TO 4 DO
        vecX_Pred[idx_i] := vecX_Pred[idx_i] + (matB[idx_i, idx_m] * vecU_Prev[idx_m]);
    END_FOR;
END_FOR;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.4: OUTPUT ESTIMATION & INNOVATION RESIDUAL: y_err = y_meas - (C * x_pred + D * u_prev)  *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idx_i := 1 TO 6 DO
    vecY_Pred[idx_i] := 0.0;
    FOR idx_j := 1 TO 6 DO
        vecY_Pred[idx_i] := vecY_Pred[idx_i] + (matC[idx_i, idx_j] * vecX_Pred[idx_j]);
    END_FOR;
    FOR idx_m := 1 TO 4 DO
        vecY_Pred[idx_i] := vecY_Pred[idx_i] + (matD[idx_i, idx_m] * vecU_Prev[idx_m]);
    END_FOR;
    vecY_Err[idx_i] := vecY_Meas[idx_i] - vecY_Pred[idx_i];
END_FOR;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.5: OBSERVER STATE CORRECTION UPDATE: x_est = x_pred + L_obs * y_err                    *)
(* ---------------------------------------------------------------------------------------------- *)
FOR idx_i := 1 TO 6 DO
    rTempCalc1 := 0.0;
    FOR idx_j := 1 TO 6 DO
        rTempCalc1 := rTempCalc1 + (matL_Obs[idx_i, idx_j] * vecY_Err[idx_j]);
    END_FOR;
    vecX_Est[idx_i] := vecX_Pred[idx_i] + rTempCalc1;
END_FOR;

(* State Physical Bounds Clamping *)
IF vecX_Est[iState_Tpeak] < 20.0 THEN
    vecX_Est[iState_Tpeak] := 20.0;
ELSIF vecX_Est[iState_Tpeak] > 380.0 THEN
    vecX_Est[iState_Tpeak] := 380.0;
END_IF;

IF vecX_Est[iState_Zpeak] < 100.0 THEN
    vecX_Est[iState_Zpeak] := 100.0;
ELSIF vecX_Est[iState_Zpeak] > 1500.0 THEN
    vecX_Est[iState_Zpeak] := 1500.0;
END_IF;

IF vecX_Est[iState_Pinlet] < 0.0 THEN
    vecX_Est[iState_Pinlet] := 0.0;
ELSIF vecX_Est[iState_Pinlet] > 3800.0 THEN
    vecX_Est[iState_Pinlet] := 3800.0;
END_IF;

IF vecX_Est[iState_Poutlet] < 0.0 THEN
    vecX_Est[iState_Poutlet] := 0.0;
ELSIF vecX_Est[iState_Poutlet] > 3600.0 THEN
    vecX_Est[iState_Poutlet] := 3600.0;
END_IF;

IF vecX_Est[iState_Xconv] < 0.0 THEN
    vecX_Est[iState_Xconv] := 0.0;
ELSIF vecX_Est[iState_Xconv] > 50.0 THEN
    vecX_Est[iState_Xconv] := 50.0;
END_IF;

IF vecX_Est[iState_MFI] < 0.05 THEN
    vecX_Est[iState_MFI] := 0.05;
ELSIF vecX_Est[iState_MFI] > 100.0 THEN
    vecX_Est[iState_MFI] := 100.0;
END_IF;


(* ---------------------------------------------------------------------------------------------- *)
(* STEP 2.6: INNER TUBE WALL GEL FOULING & THERMAL RESISTANCE R_foul MODELING                     *)
(* Stagnant high-viscosity LDPE gel boundary layer thickens during steady laminar shear           *)
(* and is violently scoured during high-pressure cyclic letdown valve (HPLDV) decompression wave  *)
(* ---------------------------------------------------------------------------------------------- *)
(* Continuous gel deposition rate proportional to conversion and inversely proportional to temp *)
rGelDepositionRate_um_s := rDepositionRate_um_per_s * (vecX_Est[iState_Xconv] / 30.0);

(* Wall Shear Stress tau_w during normal operation: tau_w = (d/4) * (dP/L) *)
rTempCalc1 := ABS(vecX_Est[iState_Pinlet] - vecX_Est[iState_Poutlet]) * 100000.0; (* Delta P in Pa *)
rTempCalc2 := (rTube_InnerDiameter_m / (4.0 * rTube_Length_Total_m)) * rTempCalc1; (* Normal Shear [Pa] *)

(* Scouring Gel Removal Model during Pulsation Shock Wave *)
IF bPulsePhaseActive THEN
    (* Cyclic letdown generates negative expansion acoustic shock wave *)
    (* Scouring shear stress jumps by factor of 3 to 5 *)
    rTempCalc3 := rTempCalc2 * 4.2;
    IF rTempCalc3 > rScourShearStress_Critical_Pa THEN
        rGelRemovalRate_um_s := 18.5 * ((rTempCalc3 - rScourShearStress_Critical_Pa) / rScourShearStress_Critical_Pa);
    ELSE
        rGelRemovalRate_um_s := 0.0;
    END_IF;
ELSE
    rGelRemovalRate_um_s := 0.0;
END_IF;

(* Discrete Integration of Polymer Gel Thickness: dW/dt = dep - scour *)
rCurrent_WallGelThickness_um := rCurrent_WallGelThickness_um + (rGelDepositionRate_um_s - rGelRemovalRate_um_s) * tScanCycleTime_s;
IF rCurrent_WallGelThickness_um < 5.0 THEN
    rCurrent_WallGelThickness_um := 5.0; (* Baseline clean boundary layer *)
ELSIF rCurrent_WallGelThickness_um > 650.0 THEN
    rCurrent_WallGelThickness_um := 650.0; (* Severe fouling limit *)
END_IF;

(* Boundary Layer Thermal Resistance R_foul = Thickness / Thermal Conductivity *)
(* k_polymer = 0.22 W/m K. R_foul in m2 K/kW *)
rCurrent_FoulingResistance_m2K_kW := (rCurrent_WallGelThickness_um * 0.001) / rPolymer_ThermalConductivity_W_mK;

(* Assign Cyber-Physical Outputs *)
rEst_PeakExothermLocation_m   := vecX_Est[iState_Zpeak];
rEst_EthyleneConversion_pct   := vecX_Est[iState_Xconv];
rEst_PolyethyleneMFI_g10min   := vecX_Est[iState_MFI];
rEst_FoulingResistance_m2K_kW := rCurrent_FoulingResistance_m2K_kW;
rEst_WallGelThickness_um      := rCurrent_WallGelThickness_um;
"""
