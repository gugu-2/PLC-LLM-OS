(* =====================================================================================================================
 * PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION & NON-LINEAR RHEOLOGY ENGINE
 * System Dimensions: n = 16 States, m = 14 Actuator Inputs, p = 16 Measured Outputs (Ts = 20 ms)
 * ===================================================================================================================== *)

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 2.1: DETERMINISTIC MATRIX INITIALIZATION (EXPLICIT FIRST-PRINCIPLES THERMO-MECHANICAL COEFFICIENTS)
 * --------------------------------------------------------------------------------------------------------------------- *)
IF NOT bMatricesInitialized THEN
    (* Clear all matrix memory structures to strictly defined zero states *)
    FOR idx_i := 1 TO 16 DO
        FOR idx_j := 1 TO 16 DO
            A_mat[idx_i, idx_j] := 0.0;
            C_mat[idx_i, idx_j] := 0.0;
            L_obs[idx_i, idx_j] := 0.0;
        END_FOR;
        FOR idx_j := 1 TO 14 DO
            B_mat[idx_i, idx_j] := 0.0;
        END_FOR;
    END_FOR;

    (* --- Matrix A: 12-Zone Barrel Thermal Conduction, Ambient Radiation & Convective Transport --- *)
    (* Zone 01: Feed Throat (Water-Cooled Isolation Section) *)
    A_mat[1, 1] := 0.9820;  A_mat[1, 2] := 0.0035;
    B_mat[1, 1] := 0.0380;

    (* Zone 02: Solids Conveying & Pre-Heating Section *)
    A_mat[2, 1] := 0.0032;  A_mat[2, 2] := 0.9880;  A_mat[2, 3] := 0.0038;
    B_mat[2, 2] := 0.0520;

    (* Zone 03: Primary Kneading & Polymer Melting Section (High Shear Dissipation) *)
    A_mat[3, 2] := 0.0035;  A_mat[3, 3] := 0.9850;  A_mat[3, 4] := 0.0042;
    A_mat[3, 15] := 0.000042; (* Direct Conductive Coupling from Screw Shaft Mechanical Torque *)
    B_mat[3, 3] := 0.0580;
    B_mat[3, 13] := 0.00185;  (* Viscous Shear Heating Injection via Screw Speed *)

    (* Zone 04: Melt Homogenization Section *)
    A_mat[4, 3] := 0.0040;  A_mat[4, 4] := 0.9860;  A_mat[4, 5] := 0.0036;
    A_mat[4, 15] := 0.000035;
    B_mat[4, 4] := 0.0560;
    B_mat[4, 13] := 0.00145;

    (* Zone 05: Side-Feeder Introduction Section (Glass Fiber Cold Infeed) *)
    A_mat[5, 4] := 0.0034;  A_mat[5, 5] := 0.9810;  A_mat[5, 6] := 0.0038;
    B_mat[5, 5] := 0.0510;

    (* Zone 06: Filler Dispersive & Distributive Mixing Section *)
    A_mat[6, 5] := 0.0036;  A_mat[6, 6] := 0.9840;  A_mat[6, 7] := 0.0040;
    A_mat[6, 15] := 0.000048;
    B_mat[6, 6] := 0.0570;
    B_mat[6, 13] := 0.00195;

    (* Zone 07: Thermal Conditioning Section *)
    A_mat[7, 6] := 0.0038;  A_mat[7, 7] := 0.9875;  A_mat[7, 8] := 0.0035;
    B_mat[7, 7] := 0.0540;

    (* Zone 08: Atmospheric Venting Section *)
    A_mat[8, 7] := 0.0035;  A_mat[8, 8] := 0.9865;  A_mat[8, 9] := 0.0037;
    B_mat[8, 8] := 0.0530;

    (* Zone 09: Vacuum Degassing Chamber Section *)
    A_mat[9, 8] := 0.0036;  A_mat[9, 9] := 0.9855;  A_mat[9, 10] := 0.0038;
    B_mat[9, 9] := 0.0520;

    (* Zone 10: Melt Pressurization & Pumping Section *)
    A_mat[10, 9] := 0.0037;  A_mat[10, 10] := 0.9870;  A_mat[10, 11] := 0.0042;
    A_mat[10, 15] := 0.000028;
    B_mat[10, 10] := 0.0550;
    B_mat[10, 13] := 0.00115;

    (* Zone 11: Screen Changer Filter Entrance *)
    A_mat[11, 10] := 0.0040;  A_mat[11, 11] := 0.9880;  A_mat[11, 12] := 0.0045;
    B_mat[11, 11] := 0.0560;

    (* Zone 12: Gear Pump Adapter Flange Transition *)
    A_mat[12, 11] := 0.0042;  A_mat[12, 12] := 0.9890;
    B_mat[12, 12] := 0.0580;

    (* --- State 13: Bulk Polymer Melt Temperature at Extruder Discharge [°C] --- *)
    A_mat[13, 10] := 0.0185;  A_mat[13, 11] := 0.0320;  A_mat[13, 12] := 0.0550;
    A_mat[13, 13] := 0.8850;  A_mat[13, 15] := 0.000085;
    B_mat[13, 13] := 0.00385; (* Viscous Dissipation Temperature Rise w.r.t Screw Speed *)

    (* --- State 14: Die Head Melt Pressure PT-101 [bar] --- *)
    A_mat[14, 13] := -0.0450; (* Thermal Fluid Viscosity Drop Reduces Die Hydraulic Resistance *)
    A_mat[14, 14] := 0.9420;   (* Die Cavity Fluid Compressibility Capacitance Decay *)
    B_mat[14, 14] := 0.3850;   (* Gear Pump Delivery Volume Flow Boosts Die Pressure *)

    (* --- State 15: Extruder Screw Drive Shaft Torque TT-301 [Nm] --- *)
    A_mat[15, 13] := -14.50;  (* Melt Temperature Rise Reduces Bulk Polymer Apparent Viscosity *)
    A_mat[15, 15] := 0.8750;  (* Mechanical Drive Train Rotational Inertia Damping *)
    B_mat[15, 13] := 9.250;   (* Dynamic Shear Drag Resistance with Screw Speed Acceleration *)

    (* --- State 16: Melt Gear Pump Suction Flange Pressure PT-102 [bar] --- *)
    A_mat[16, 13] := -0.0280;
    A_mat[16, 16] := 0.9620;  (* Suction Buffer Cavity Pressure Storage Decay *)
    B_mat[16, 13] := 0.0885;  (* Screw Extruder Throughput Positive Pressure Feed *)
    B_mat[16, 14] := -0.4450; (* Gear Pump Positive Displacement Volumetric Suction Drawdown *)

    (* --- Matrix C: Direct Unity Sensor Mapping (16x16 Identity) --- *)
    FOR idx_i := 1 TO 16 DO
        C_mat[idx_i, idx_i] := 1.0;
    END_FOR;

    (* --- Matrix L: Luenberger Observer Kalman Innovation Gain Matrix (16x16) --- *)
    L_obs[1, 1]   := 0.165;  L_obs[2, 2]   := 0.175;  L_obs[3, 3]   := 0.195;
    L_obs[4, 4]   := 0.185;  L_obs[5, 5]   := 0.170;  L_obs[6, 6]   := 0.190;
    L_obs[7, 7]   := 0.180;  L_obs[8, 8]   := 0.175;  L_obs[9, 9]   := 0.185;
    L_obs[10, 10] := 0.205;  L_obs[11, 11] := 0.210;  L_obs[12, 12] := 0.220;
    L_obs[13, 13] := 0.245;  L_obs[14, 14] := 0.285;  L_obs[15, 15] := 0.260;
    L_obs[16, 16] := 0.310;

    (* Initialize State Vector to Physical Plant Baseline Equilibrium *)
    FOR idx_i := 1 TO 12 DO
        x_state[idx_i] := 25.0; (* Ambient Room Temperature Cold Barrel [°C] *)
    END_FOR;
    x_state[13] := 25.0;  (* Melt Temp [°C] *)
    x_state[14] := 0.0;   (* Die Pres [bar] *)
    x_state[15] := 0.0;   (* Torque [Nm] *)
    x_state[16] := 0.0;   (* Suction Pres [bar] *)

    bMatricesInitialized := TRUE;
END_IF;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 2.2: VECTORIZE PHYSICAL MEASUREMENTS & CURRENT ACTUATOR COMMANDS
 * --------------------------------------------------------------------------------------------------------------------- *)
y_meas[1]  := rZoneTemp_Act_Z01_In;
y_meas[2]  := rZoneTemp_Act_Z02_In;
y_meas[3]  := rZoneTemp_Act_Z03_In;
y_meas[4]  := rZoneTemp_Act_Z04_In;
y_meas[5]  := rZoneTemp_Act_Z05_In;
y_meas[6]  := rZoneTemp_Act_Z06_In;
y_meas[7]  := rZoneTemp_Act_Z07_In;
y_meas[8]  := rZoneTemp_Act_Z08_In;
y_meas[9]  := rZoneTemp_Act_Z09_In;
y_meas[10] := rZoneTemp_Act_Z10_In;
y_meas[11] := rZoneTemp_Act_Z11_In;
y_meas[12] := rZoneTemp_Act_Z12_In;
y_meas[13] := rVoted_MeltTemp_Out;
y_meas[14] := rVoted_DieMeltPres_Out;
y_meas[15] := rVoted_ScrewTorque_Out;
y_meas[16] := rGearPump_SuctPres_In;

u_input[1]  := rZoneHeat_Cmd_Z01_Out;
u_input[2]  := rZoneHeat_Cmd_Z02_Out;
u_input[3]  := rZoneHeat_Cmd_Z03_Out;
u_input[4]  := rZoneHeat_Cmd_Z04_Out;
u_input[5]  := rZoneHeat_Cmd_Z05_Out;
u_input[6]  := rZoneHeat_Cmd_Z06_Out;
u_input[7]  := rZoneHeat_Cmd_Z07_Out;
u_input[8]  := rZoneHeat_Cmd_Z08_Out;
u_input[9]  := rZoneHeat_Cmd_Z09_Out;
u_input[10] := rZoneHeat_Cmd_Z10_Out;
u_input[11] := rZoneHeat_Cmd_Z11_Out;
u_input[12] := rZoneHeat_Cmd_Z12_Out;
u_input[13] := rScrewSpeed_Cmd_Out;
u_input[14] := rGearPumpSpeed_Cmd_Out;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 2.3: DISCRETE STATE-SPACE PREDICTION & LUENBERGER OBSERVER INNOVATION UPDATE
 * Equations:
 *   x_pred[k+1|k] = A * x_state[k] + B * u[k]
 *   e[k]          = y_meas[k] - C * x_pred[k+1|k]
 *   x_state[k+1]  = x_pred[k+1|k] + L * e[k]
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Compute Forward State Prediction Vector x_pred *)
FOR idx_i := 1 TO 16 DO
    rCalc_Sum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rCalc_Sum := rCalc_Sum + (A_mat[idx_i, idx_j] * x_state[idx_j]);
    END_FOR;
    FOR idx_j := 1 TO 14 DO
        rCalc_Sum := rCalc_Sum + (B_mat[idx_i, idx_j] * u_input[idx_j]);
    END_FOR;
    x_pred[idx_i] := rCalc_Sum;
END_FOR;

(* Compute Predicted Measurement Vector y_est and Innovation Error e_obs *)
FOR idx_i := 1 TO 16 DO
    rCalc_Sum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rCalc_Sum := rCalc_Sum + (C_mat[idx_i, idx_j] * x_pred[idx_j]);
    END_FOR;
    y_est[idx_i] := rCalc_Sum;
    e_obs[idx_i] := y_meas[idx_i] - y_est[idx_i];
END_FOR;

(* Apply Observer Correction Matrix L to Compute Updated State Vector x_state *)
FOR idx_i := 1 TO 16 DO
    rCalc_Sum := 0.0;
    FOR idx_j := 1 TO 16 DO
        rCalc_Sum := rCalc_Sum + (L_obs[idx_i, idx_j] * e_obs[idx_j]);
    END_FOR;
    x_state[idx_i] := x_pred[idx_i] + rCalc_Sum;
END_FOR;

(* ---------------------------------------------------------------------------------------------------------------------
 * STEP 2.4: HIGH-FIDELITY NON-LINEAR POLYMER RHEOLOGY & SPECIFIC MECHANICAL ENERGY (SME)
 * --------------------------------------------------------------------------------------------------------------------- *)
(* Sum Total Instantaneous Gravimetric Throughput Rate [kg/h] *)
rOnline_TotalThroughput := rFeeder_ActFlow_01_In + rFeeder_ActFlow_02_In +
                           rFeeder_ActFlow_03_In + rFeeder_ActFlow_04_In +
                           rFeeder_ActFlow_05_In;
rTotalThroughput_Out := rOnline_TotalThroughput;

(* Apparent Screw Channel Shear Rate gamma_dot [1/s]: gamma_dot = (pi * D * N) / (60 * H) *)
IF (rScrewSpeed_Act_In > 0.5) AND (SCREW_FLIGHT_DEPTH > 0.001) THEN
    rOnline_ShearRate := (PI_CONST * SCREW_DIAMETER * rScrewSpeed_Act_In) / (60.0 * SCREW_FLIGHT_DEPTH);
ELSE
    rOnline_ShearRate := 0.1;
END_IF;

(* Online Cross-WLF Apparent Melt Viscosity Estimation [Pa*s] *)
(* Temperature Shift: T_kelvin = x_state[13] + 273.15 *)
rCalc_TempA := x_state[13] + 273.15;
IF rCalc_TempA < 420.0 THEN
    rCalc_TempA := 420.0;
END_IF;

(* WLF Shift Factor ln(a_T) = -A1 * (T - D2) / (A2 + (T - D2)) *)
rCalc_TempB := rCalc_TempA - POLYMER_WLF_D2;
IF (POLYMER_WLF_A2 + rCalc_TempB) > 1.0 THEN
    rCalc_TempC := (-POLYMER_WLF_A1 * rCalc_TempB) / (POLYMER_WLF_A2 + rCalc_TempB);
    (* Clamp exponential argument to prevent numerical floating point overflow *)
    IF rCalc_TempC > 15.0 THEN
        rCalc_TempC := 15.0;
    ELSIF rCalc_TempC < -25.0 THEN
        rCalc_TempC := -25.0;
    END_IF;
    rCalc_TempD := EXP(rCalc_TempC);
ELSE
    rCalc_TempD := 1.0E-04;
END_IF;

(* Zero-Shear Viscosity: eta_0 = D1 * a_T *)
rCalc_TempA := POLYMER_WLF_D1 * rCalc_TempD * 1.0E-06; (* Scaled down to prevent IEEE-754 overflow *)

(* Cross Model Shear Thinning: eta = eta_0 / (1.0 + ( (eta_0 * gamma_dot) / Tau* )^(1 - n) ) *)
IF (rOnline_ShearRate > 0.5) AND (POLYMER_TAU_STAR > 100.0) THEN
    rCalc_TempB := (rCalc_TempA * rOnline_ShearRate) / POLYMER_TAU_STAR;
    IF rCalc_TempB > 0.001 THEN
        (* Approximating Power Law (1 - n) with n = 0.365 -> exponent = 0.635 *)
        rCalc_TempC := 1.0 + EXP(0.635 * LN(rCalc_TempB));
        rOnline_ApparentViscosity := rCalc_TempA / rCalc_TempC;
    ELSE
        rOnline_ApparentViscosity := rCalc_TempA;
    END_IF;
ELSE
    rOnline_ApparentViscosity := rCalc_TempA;
END_IF;

(* Bound Estimated Viscosity to Physical Compounding Window [20.0 to 3500.0 Pa*s] *)
IF rOnline_ApparentViscosity < 20.0 THEN
    rOnline_ApparentViscosity := 20.0;
ELSIF rOnline_ApparentViscosity > 3500.0 THEN
    rOnline_ApparentViscosity := 3500.0;
END_IF;
rApparentViscosity_Out := rOnline_ApparentViscosity;

(* Specific Mechanical Energy (SME) Input [kWh/kg]:
 * SME = (2 * pi * N * Torque) / (60 * 1000 * TotalThroughput) *)
IF (rOnline_TotalThroughput > 20.0) AND (rScrewSpeed_Act_In > 5.0) THEN
    rOnline_SME := (2.0 * PI_CONST * rScrewSpeed_Act_In * rVoted_ScrewTorque_Out) /
                   (60.0 * 1000.0 * rOnline_TotalThroughput);
ELSE
    rOnline_SME := 0.0;
END_IF;
rSpecificMechEnergy_Out := rOnline_SME;

(* Total Instantaneous Mechanical Viscous Dissipation Heat Generation Power [kW] *)
rOnline_ShearHeatingPowerKW := (2.0 * PI_CONST * rScrewSpeed_Act_In * rVoted_ScrewTorque_Out) / (60.0 * 1000.0);
rShearHeatPower_Out := rOnline_ShearHeatingPowerKW;

(* Screw Channel Degree of Fill Estimation [%] *)
IF rScrewSpeed_Act_In > 1.0 THEN
    (* Channel Volumetric Drag Capacity: Q_drag = 0.5 * pi^2 * D^2 * H * sin(theta)*cos(theta) * N *)
    rCalc_TempA := 0.5 * (PI_CONST * PI_CONST) * (SCREW_DIAMETER * SCREW_DIAMETER) *
                   SCREW_FLIGHT_DEPTH * 0.285 * (rScrewSpeed_Act_In / 60.0) * POLYMER_MELT_DENSITY * 3600.0;
    IF rCalc_TempA > 10.0 THEN
        rDegreeOfFill_Out := (rOnline_TotalThroughput / rCalc_TempA) * 100.0;
        IF rDegreeOfFill_Out > 100.0 THEN
            rDegreeOfFill_Out := 100.0;
        ELSIF rDegreeOfFill_Out < 0.0 THEN
            rDegreeOfFill_Out := 0.0;
        END_IF;
    ELSE
        rDegreeOfFill_Out := 0.0;
    END_IF;
ELSE
    rDegreeOfFill_Out := 0.0;
END_IF;
