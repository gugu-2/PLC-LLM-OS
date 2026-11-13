# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_var_decl.py
Declares VAR ... END_VAR for FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance.
"""

def generate_var_decl():
    return '''VAR
    (* ==================== SYSTEM INITIALIZATION & DIAGNOSTICS ==================== *)
    bInitialized                    : BOOL := FALSE; (* First-Scan Initialization Routine Complete Flag *)
    nScanCounter                    : UDINT := 0;    (* Execution Task Scan Cycle Iteration Counter *)
    rLocalDeltaT_s                  : REAL := 0.100; (* Internal Clamped Scan Execution Time Step [s] *)

    (* ==================== ELECTROCHEMICAL PHYSICAL CONSTANTS ==================== *)
    c_Faraday_C_mol                 : REAL := 96485.332; (* Faraday Electrochemical Constant [C/mol] *)
    c_MolarMass_Al2O3_g_mol         : REAL := 101.9613;  (* Molar Mass of High-Purity Smelter Alumina [g/mol] *)
    c_MolarMass_Al_g_mol            : REAL := 26.98154;  (* Atomic Weight of Elemental Aluminum [g/mol] *)
    c_Valence_Electrons_Al2O3       : REAL := 6.0;       (* Electrons Exchanged per Mol of Al2O3 Decomposed [-] *)
    c_Nominal_EMF_V                 : REAL := 1.650;     (* Pseudo-Counter Electromotive Force Back-EMF [V] *)
    c_Nominal_BathMass_kg           : REAL := 8250.0;    (* Total Active Molten Cryolite Electrolyte Mass [kg] *)
    c_Nominal_MetalPadMass_kg       : REAL := 14500.0;   (* Total Liquid Aluminum Cathode Reservoir Mass [kg] *)
    c_Nominal_AnodeArea_m2          : REAL := 34.80;     (* Cumulative Active Carbon Anode Bottom Surface [m^2] *)
    c_BathResistivity_Ohm_cm        : REAL := 0.448;     (* Specific Electrical Resistivity of Molten Bath [Ohm*cm] *)
    c_ACD_Sensitivity_uOhm_mm       : REAL := 0.1287;    (* ACD-to-Resistance Sensitivity Gain [micro-Ohm/mm] *)
    c_Nominal_CryoliteRatio         : REAL := 2.22;      (* Target Molar Cryolite Ratio NaF/AlF3 [-] *)
    c_Nominal_EnthalpyDecomp_J_g    : REAL := 31500.0;   (* Specific Endothermic Decomposition Heat [J/g Al] *)

    (* ==================== DISCRETE STATE-SPACE MATRICES (6x6 SYSTEM) ==================== *)
    (* States x = [x1: dR_pot (uOhm), x2: C_Al2O3 (wt%), x3: T_bath (degC), x4: dACD (mm), x5: BubbleCov (%), x6: MetalPad (cm)] *)
    (* Inputs u = [u1: HoistCmd (mm), u2: FeederRate (ppm), u3: AlF3Hopper (%), u4: ExhaustDamper (%), u5: RodTrim (mm)] *)
    arrA                            : ARRAY[1..6, 1..6] OF REAL; (* Discrete State Transition Matrix A (6x6) *)
    arrB                            : ARRAY[1..6, 1..5] OF REAL; (* Discrete Actuator Input Gain Matrix B (6x5) *)
    arrC                            : ARRAY[1..6, 1..6] OF REAL; (* Discrete Process Output Observer Matrix C (6x6) *)
    arrD                            : ARRAY[1..6, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix D (6x5) *)
    arrL                            : ARRAY[1..6, 1..6] OF REAL; (* Discrete Luenberger Innovation Observer Gain L (6x6) *)

    arrX_hat                        : ARRAY[1..6] OF REAL; (* Current Observer Estimated State Deviation Vector *)
    arrX_hat_prev                   : ARRAY[1..6] OF REAL; (* Prior Execution Step State Vector *)
    arrY_meas                       : ARRAY[1..6] OF REAL; (* Real-Time Sensor Measurement Vector *)
    arrY_est                        : ARRAY[1..6] OF REAL; (* Synthetic Estimated Measurement Vector *)
    arrInnovation                   : ARRAY[1..6] OF REAL; (* Observer Innovation Error Vector (Y_meas - Y_est) *)
    arrU_Applied                    : ARRAY[1..5] OF REAL; (* Actuator Commands Applied to Physical Field Devices *)
    arrU_Previous                   : ARRAY[1..5] OF REAL; (* Actuator Commands Retained from Previous Execution *)

    (* ==================== RECEDING HORIZON MPC OPTIMIZER ARRAYS ==================== *)
    arrQ                            : ARRAY[1..6, 1..6] OF REAL; (* State Deviation Tracking Cost Matrix (6x6) *)
    arrR                            : ARRAY[1..5, 1..5] OF REAL; (* Actuator Effort Energy Penalty Matrix (5x5) *)
    arrS                            : ARRAY[1..5, 1..5] OF REAL; (* Actuator Slew Rate Damping Cost Matrix (5x5) *)
    arrP                            : ARRAY[1..6, 1..6] OF REAL; (* Terminal State Cost Algebraic Riccati Matrix (6x6) *)

    arrX_Trajectory                 : ARRAY[0..5, 1..6] OF REAL; (* Predicted Future State Horizon (Steps 0..5, 6 States) *)
    arrU_Trajectory                 : ARRAY[0..4, 1..5] OF REAL; (* Control Input Sequence Horizon (Steps 0..4, 5 Inputs) *)
    arrLambda                       : ARRAY[0..5, 1..6] OF REAL; (* Adjoint Backward Costate Vectors (Steps 0..5, 6 Costates) *)
    arrGrad_U                       : ARRAY[0..4, 1..5] OF REAL; (* Projected Gradient Horizon for Actuator Updates *)

    arrU_Min                        : ARRAY[1..5] OF REAL; (* Absolute Hardware Actuator Lower Bounds *)
    arrU_Max                        : ARRAY[1..5] OF REAL; (* Absolute Hardware Actuator Upper Bounds *)
    arrDeltaU_Max                   : ARRAY[1..5] OF REAL; (* Slew Rate Limiter Maximum Delta per Cycle *)
    rPGD_StepSize                   : REAL := 0.0450;      (* Projected Gradient Descent Learning Rate Alpha *)

    (* ==================== 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR SUITES ==================== *)
    (* Channel 1: Pot Cell Voltage [V] *)
    rDev_Volt_12                    : REAL; (* Absolute Deviation Between Channel 1 and 2 [V] *)
    rDev_Volt_23                    : REAL; (* Absolute Deviation Between Channel 2 and 3 [V] *)
    rDev_Volt_31                    : REAL; (* Absolute Deviation Between Channel 3 and 1 [V] *)
    bDiscr_Volt_12                  : BOOL; (* Instantaneous Discrepancy Flag 1 vs 2 *)
    bDiscr_Volt_23                  : BOOL; (* Instantaneous Discrepancy Flag 2 vs 3 *)
    bDiscr_Volt_31                  : BOOL; (* Instantaneous Discrepancy Flag 3 vs 1 *)
    rTimer_Volt_12_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 1-2 [ms] *)
    rTimer_Volt_23_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 2-3 [ms] *)
    rTimer_Volt_31_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 3-1 [ms] *)
    bHealth_Volt_CH1                : BOOL := TRUE; (* Hardware Channel 1 Integrity Healthy *)
    bHealth_Volt_CH2                : BOOL := TRUE; (* Hardware Channel 2 Integrity Healthy *)
    bHealth_Volt_CH3                : BOOL := TRUE; (* Hardware Channel 3 Integrity Healthy *)
    nDegradedMode_Volt              : INT := 0; (* Degradation State: 0=3 healthy, 1=2 healthy, 2=1 healthy, 3=Fault *)

    (* Channel 2: Potline DC Total Current [kA] *)
    rDev_Curr_12                    : REAL; (* Absolute Deviation Between Channel 1 and 2 [kA] *)
    rDev_Curr_23                    : REAL; (* Absolute Deviation Between Channel 2 and 3 [kA] *)
    rDev_Curr_31                    : REAL; (* Absolute Deviation Between Channel 3 and 1 [kA] *)
    bDiscr_Curr_12                  : BOOL; (* Instantaneous Discrepancy Flag 1 vs 2 *)
    bDiscr_Curr_23                  : BOOL; (* Instantaneous Discrepancy Flag 2 vs 3 *)
    bDiscr_Curr_31                  : BOOL; (* Instantaneous Discrepancy Flag 3 vs 1 *)
    rTimer_Curr_12_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 1-2 [ms] *)
    rTimer_Curr_23_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 2-3 [ms] *)
    rTimer_Curr_31_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 3-1 [ms] *)
    bHealth_Curr_CH1                : BOOL := TRUE; (* Hardware Channel 1 Integrity Healthy *)
    bHealth_Curr_CH2                : BOOL := TRUE; (* Hardware Channel 2 Integrity Healthy *)
    bHealth_Curr_CH3                : BOOL := TRUE; (* Hardware Channel 3 Integrity Healthy *)
    nDegradedMode_Curr              : INT := 0; (* Degradation State: 0=3 healthy, 1=2 healthy, 2=1 healthy, 3=Fault *)

    (* Channel 3: Molten Bath Electrolyte Temperature [deg C] *)
    rDev_Temp_12                    : REAL; (* Absolute Deviation Between Channel 1 and 2 [deg C] *)
    rDev_Temp_23                    : REAL; (* Absolute Deviation Between Channel 2 and 3 [deg C] *)
    rDev_Temp_31                    : REAL; (* Absolute Deviation Between Channel 3 and 1 [deg C] *)
    bDiscr_Temp_12                  : BOOL; (* Instantaneous Discrepancy Flag 1 vs 2 *)
    bDiscr_Temp_23                  : BOOL; (* Instantaneous Discrepancy Flag 2 vs 3 *)
    bDiscr_Temp_31                  : BOOL; (* Instantaneous Discrepancy Flag 3 vs 1 *)
    rTimer_Temp_12_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 1-2 [ms] *)
    rTimer_Temp_23_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 2-3 [ms] *)
    rTimer_Temp_31_ms               : REAL := 0.0; (* Persistence Timer: Discrepancy 3-1 [ms] *)
    bHealth_Temp_CH1                : BOOL := TRUE; (* Hardware Channel 1 Integrity Healthy *)
    bHealth_Temp_CH2                : BOOL := TRUE; (* Hardware Channel 2 Integrity Healthy *)
    bHealth_Temp_CH3                : BOOL := TRUE; (* Hardware Channel 3 Integrity Healthy *)
    nDegradedMode_Temp              : INT := 0; (* Degradation State: 0=3 healthy, 1=2 healthy, 2=1 healthy, 3=Fault *)

    (* Channel 4: Anode Beam Elevation Position [mm] *)
    rDev_Pos_12                     : REAL; (* Absolute Deviation Between Channel 1 and 2 [mm] *)
    rDev_Pos_23                     : REAL; (* Absolute Deviation Between Channel 2 and 3 [mm] *)
    rDev_Pos_31                     : REAL; (* Absolute Deviation Between Channel 3 and 1 [mm] *)
    bDiscr_Pos_12                   : BOOL; (* Instantaneous Discrepancy Flag 1 vs 2 *)
    bDiscr_Pos_23                   : BOOL; (* Instantaneous Discrepancy Flag 2 vs 3 *)
    bDiscr_Pos_31                   : BOOL; (* Instantaneous Discrepancy Flag 3 vs 1 *)
    rTimer_Pos_12_ms                : REAL := 0.0; (* Persistence Timer: Discrepancy 1-2 [ms] *)
    rTimer_Pos_23_ms                : REAL := 0.0; (* Persistence Timer: Discrepancy 2-3 [ms] *)
    rTimer_Pos_31_ms                : REAL := 0.0; (* Persistence Timer: Discrepancy 3-1 [ms] *)
    bHealth_Pos_CH1                 : BOOL := TRUE; (* Hardware Channel 1 Integrity Healthy *)
    bHealth_Pos_CH2                 : BOOL := TRUE; (* Hardware Channel 2 Integrity Healthy *)
    bHealth_Pos_CH3                 : BOOL := TRUE; (* Hardware Channel 3 Integrity Healthy *)
    nDegradedMode_Pos               : INT := 0; (* Degradation State: 0=3 healthy, 1=2 healthy, 2=1 healthy, 3=Fault *)

    (* ==================== ROLLING RESISTANCE, NOISE, AND AE DERIVATIVE OBSERVER ==================== *)
    arrResRingBuffer                : ARRAY[0..31] OF REAL; (* Circular Buffer for Instantaneous Pseudo-Resistance [uOhm] *)
    nRingBufferIdx                  : INT := 0; (* Ring Buffer Head Pointer *)
    bRingBufferFilled               : BOOL := FALSE; (* Ring Buffer Has Completed First Full Rotation *)
    rResSum                         : REAL := 0.0; (* Rolling Sum for Mean Resistance Calculation *)
    rResMean                        : REAL := 5.0; (* Rolling Mean Resistance [uOhm] *)
    rResVarianceSum                 : REAL := 0.0; (* Rolling Sum of Squared Deviations *)
    rResVariance                    : REAL := 0.0; (* Bubble Noise Variance in 0.5 - 2.0 Hz Band [uOhm^2] *)

    rRes_k0                         : REAL := 5.0; (* Resistance Sample at Time k [uOhm] *)
    rRes_k1                         : REAL := 5.0; (* Resistance Sample at Time k-1 [uOhm] *)
    rRes_k2                         : REAL := 5.0; (* Resistance Sample at Time k-2 [uOhm] *)
    rRes_k3                         : REAL := 5.0; (* Resistance Sample at Time k-3 [uOhm] *)
    rRes_k4                         : REAL := 5.0; (* Resistance Sample at Time k-4 [uOhm] *)

    rSlope_k0                       : REAL := 0.0; (* Resistance 1st Derivative dR/dt [uOhm/min] *)
    rSlope_k1                       : REAL := 0.0; (* Resistance 1st Derivative at k-1 [uOhm/min] *)
    rCurvature_k0                   : REAL := 0.0; (* Resistance 2nd Derivative d2R/dt2 [uOhm/s^2] *)

    (* ==================== ELECTROCHEMICAL PROCESS BALANCES ==================== *)
    rInstantCurrentEfficiency       : REAL := 0.945; (* Calculated Current Efficiency (0.85 - 0.96) [-] *)
    rAluminaConsumptionRate_kgs     : REAL := 0.0832; (* Faradaic Alumina Consumption Mass Flow [kg/s] *)
    rAluminaFeedRate_kgs            : REAL := 0.0832; (* Effective Point Feeder Inflow Rate [kg/s] *)
    rNetAluminaMassRate_kgs         : REAL := 0.0; (* Net Alumina Accumulation Rate [kg/s] *)
    rEstimatedLiquidus_degC         : REAL := 941.5; (* Cryolite Bath Liquidus Equilibrium Freezing Temp [deg C] *)
    rCalculatedSuperheat_degC       : REAL := 13.5;  (* Superheat Delta = BathTemp - LiquidusTemp [deg C] *)
    rExcessAlF3_pct                 : REAL := 11.2;  (* Excess AlF3 Relative to Cryolite Stoichiometry [%] *)
    rBathFluorideRatio              : REAL := 1.13;  (* Weight Ratio NaF / AlF3 [-] *)

    (* ==================== POINT FEEDER & CRUST BREAKER SEQUENCER ==================== *)
    rFeederCycleTimer_s             : REAL := 0.0;   (* Feeder Master Cycle Inter-Pulse Period Timer [s] *)
    rFeederShotDurationTimer_s      : REAL := 0.0;   (* Pneumatic Shot Solenoid Valve Energize Timer [s] *)
    rCrustBreakerPunchTimer_s       : REAL := 0.0;   (* Pneumatic Chisel Punch Cylinder Stroke Timer [s] *)
    nActiveFeederHead               : INT := 1;      (* Round-Robin Rotational Index for Feeders 1..4 *)
    bFeederShotActive               : BOOL := FALSE; (* Feeder Volumetric Chamber Discharge In Progress *)
    bCrustBreakerActive             : BOOL := FALSE; (* Mechanical Breaker Chisel Punch In Progress *)
    rUnderfeedDuration_s            : REAL := 0.0;   (* Cumulative Dwell in Diagnostic Underfeed Mode [s] *)
    rOverfeedDuration_s             : REAL := 0.0;   (* Cumulative Dwell in Alumina Replenishment Overfeed [s] *)
    rNominalPulsePeriod_s           : REAL := 45.0;  (* Inter-Shot Delay Time for Nominal Feed Mode [s] *)
    rUnderfeedPulsePeriod_s         : REAL := 85.0;  (* Inter-Shot Delay Time for Diagnostic Underfeed [s] *)
    rOverfeedPulsePeriod_s          : REAL := 18.0;  (* Inter-Shot Delay Time for Replenishment Overfeed [s] *)
    rTargetPulsePeriod_s            : REAL := 45.0;  (* Active Dynamic Firing Period Setpoint [s] *)

    (* ==================== ANODE BEAM HOIST SERVO & ROCKING MECHANISM ==================== *)
    rBeamMoveAccumulator_mm         : REAL := 0.0;   (* Total Beam Distance Traveled in Current 24h Window [mm] *)
    rBeamDeadband_mm                : REAL := 0.12;  (* Minimum Move Threshold to Prevent Jack Screw Wear [mm] *)
    rBeamRockingTimer_s             : REAL := 0.0;   (* High-Speed Bubble Dispersion Rocking Timer [s] *)
    nBeamRockingStage               : INT := 0;      (* Rocking Step: 0=Off, 1=DownStroke, 2=Dwell, 3=UpStroke *)
    rPreRockingSavedPos_mm          : REAL := 0.0;   (* Base Beam Elevation Latched Prior to Rocking Move [mm] *)
    rRockingStrokeDepth_mm          : REAL := 4.80;  (* Dynamic Immersion Stroke Depth for Gas Layer Pinch [mm] *)
    rHoistDutyCycleTimer_s          : REAL := 0.0;   (* Motor Duty Cycle Thermal Protection Timer [s] *)

    (* ==================== 14-STAGE DETERMINISTIC PRODUCTION FSM ==================== *)
    nFSM_PreviousState              : INT := 0;      (* Latched Previous FSM Execution State *)
    rFSM_StateTimer_s               : REAL := 0.0;   (* Monotonic Elapsed Dwell Timer in Current State [s] *)
    rPreheatRampCurrent_kA          : REAL := 0.0;   (* Synthetic Ramp Target for Cold Pot Coke Preheating [kA] *)
    rElectrolyteFillVolume_pct      : REAL := 0.0;   (* Liquid Bath Transfer Ladle Filling Progress [%] *)
    rStartupACDTimer_s              : REAL := 0.0;   (* Post-Startup Polarization Normalization Dwell [s] *)
    rAnodeChangeElapsedTime_s       : REAL := 0.0;   (* Time Spent in Manual Carbon Anode Replacement [s] *)
    rMetalTapElapsedTime_s          : REAL := 0.0;   (* Time Spent in Vacuum Crucible Metal Siphon Tap [s] *)
    rAlF3AdditionElapsedTime_s      : REAL := 0.0;   (* Time Spent in Bath Chemistry Fluoride Dosing [s] *)
    rBypassElapsedTime_s            : REAL := 0.0;   (* Time Spent in Shunted Potline Circuit Bypass [s] *)
    rTripLockoutTimer_s             : REAL := 0.0;   (* Post-Trip Cooldown and Venting Lockout Timer [s] *)

    (* ==================== ISA-18.2 ALARM TRIP POINTS & HYSTERESIS ==================== *)
    c_Volt_Trip_HH                  : REAL := 4.80;  (* Cell Voltage High-High Critical Limit [V] *)
    c_Volt_Trip_H                   : REAL := 4.45;  (* Cell Voltage High Pre-Alarm Limit [V] *)
    c_Volt_Trip_L                   : REAL := 3.85;  (* Cell Voltage Low Under-Potential Limit [V] *)
    c_Volt_Trip_LL                  : REAL := 3.60;  (* Cell Voltage Low-Low Short-Circuit Collapse Limit [V] *)
    c_Volt_Hysteresis               : REAL := 0.040; (* Voltage Alarm Reset Deadband Hysteresis [V] *)
    c_Volt_AnodeEffect_Threshold    : REAL := 7.50;  (* Full Flash Anode Effect Critical Threshold [V] *)

    c_Res_Trip_HH                   : REAL := 6.80;  (* Pot Resistance High-High Limit [micro-Ohm] *)
    c_Res_Trip_H                    : REAL := 5.80;  (* Pot Resistance High Target Deviation Limit [micro-Ohm] *)
    c_Res_Trip_L                    : REAL := 4.40;  (* Pot Resistance Low Target Deviation Limit [micro-Ohm] *)
    c_Res_Trip_LL                   : REAL := 3.80;  (* Pot Resistance Low-Low Short Risk Limit [micro-Ohm] *)
    c_Res_Hysteresis                : REAL := 0.075; (* Resistance Reset Deadband Hysteresis [micro-Ohm] *)
    c_ResSlope_EarlyAE_Warn         : REAL := 0.018; (* Early AE Predictive Slope Threshold [uOhm/min] *)
    c_ResCurv_EarlyAE_Warn          : REAL := 0.0035;(* Early AE Acceleration Curvature Threshold [uOhm/s^2] *)

    c_Temp_Trip_HH                  : REAL := 980.0; (* Bath Temperature High-High Boiling/Fluoride Loss [deg C] *)
    c_Temp_Trip_H                   : REAL := 968.0; (* Bath Temperature High Thermal Expansion Warning [deg C] *)
    c_Temp_Trip_L                   : REAL := 942.0; (* Bath Temperature Low Sludge Formation Risk [deg C] *)
    c_Temp_Trip_LL                  : REAL := 930.0; (* Bath Temperature Low-Low Freeze Freeze-Up Danger [deg C] *)
    c_Temp_Hysteresis               : REAL := 2.50;  (* Temperature Reset Deadband Hysteresis [deg C] *)

    c_Alumina_Trip_HH               : REAL := 4.60;  (* Alumina Concentration High-High Muck Sludge Limit [wt%] *)
    c_Alumina_Trip_H                : REAL := 3.80;  (* Alumina Concentration High Overfeed Warning [wt%] *)
    c_Alumina_Trip_L                : REAL := 1.85;  (* Alumina Concentration Low Polarization Inception [wt%] *)
    c_Alumina_Trip_LL               : REAL := 1.45;  (* Alumina Concentration Low-Low Anode Effect Flash [wt%] *)
    c_Alumina_Hysteresis            : REAL := 0.12;  (* Alumina Reset Deadband Hysteresis [wt%] *)

    c_ACD_Trip_HH                   : REAL := 58.0;  (* ACD High-High Severe Ohmic Overheating [mm] *)
    c_ACD_Trip_H                    : REAL := 50.0;  (* ACD High Resistance Imbalance Warning [mm] *)
    c_ACD_Trip_L                    : REAL := 34.0;  (* ACD Low Metal Wave Contact Risk [mm] *)
    c_ACD_Trip_LL                   : REAL := 28.0;  (* ACD Low-Low Imminent Cathode Short Trip [mm] *)
    c_ACD_Hysteresis                : REAL := 1.20;  (* ACD Reset Deadband Hysteresis [mm] *)

    (* Raw Alarm Evaluation Flags *)
    bAlm_Volt_HH_Raw                : BOOL := FALSE;
    bAlm_Volt_H_Raw                 : BOOL := FALSE;
    bAlm_Volt_L_Raw                 : BOOL := FALSE;
    bAlm_Volt_LL_Raw                : BOOL := FALSE;
    bAlm_Res_HH_Raw                 : BOOL := FALSE;
    bAlm_Res_H_Raw                  : BOOL := FALSE;
    bAlm_Res_L_Raw                  : BOOL := FALSE;
    bAlm_Res_LL_Raw                 : BOOL := FALSE;
    bAlm_Temp_HH_Raw                : BOOL := FALSE;
    bAlm_Temp_H_Raw                 : BOOL := FALSE;
    bAlm_Temp_L_Raw                 : BOOL := FALSE;
    bAlm_Temp_LL_Raw                : BOOL := FALSE;
    bAlm_Alumina_HH_Raw             : BOOL := FALSE;
    bAlm_Alumina_H_Raw              : BOOL := FALSE;
    bAlm_Alumina_L_Raw              : BOOL := FALSE;
    bAlm_Alumina_LL_Raw             : BOOL := FALSE;
    bAlm_ACD_HH_Raw                 : BOOL := FALSE;
    bAlm_ACD_H_Raw                  : BOOL := FALSE;
    bAlm_ACD_L_Raw                  : BOOL := FALSE;
    bAlm_ACD_LL_Raw                 : BOOL := FALSE;

    (* Latched Process Alarms *)
    bAlm_Volt_HH_Latched            : BOOL := FALSE;
    bAlm_Volt_H_Latched             : BOOL := FALSE;
    bAlm_Volt_L_Latched             : BOOL := FALSE;
    bAlm_Volt_LL_Latched            : BOOL := FALSE;
    bAlm_Res_HH_Latched             : BOOL := FALSE;
    bAlm_Res_H_Latched              : BOOL := FALSE;
    bAlm_Res_L_Latched              : BOOL := FALSE;
    bAlm_Res_LL_Latched             : BOOL := FALSE;
    bAlm_Temp_HH_Latched            : BOOL := FALSE;
    bAlm_Temp_H_Latched             : BOOL := FALSE;
    bAlm_Temp_L_Latched             : BOOL := FALSE;
    bAlm_Temp_LL_Latched            : BOOL := FALSE;
    bAlm_Alumina_HH_Latched         : BOOL := FALSE;
    bAlm_Alumina_H_Latched          : BOOL := FALSE;
    bAlm_Alumina_L_Latched          : BOOL := FALSE;
    bAlm_Alumina_LL_Latched         : BOOL := FALSE;
    bAlm_ACD_HH_Latched             : BOOL := FALSE;
    bAlm_ACD_H_Latched              : BOOL := FALSE;
    bAlm_ACD_L_Latched              : BOOL := FALSE;
    bAlm_ACD_LL_Latched             : BOOL := FALSE;

    (* Safety & System Fault Flags *)
    bAlm_AnodeEffectActive          : BOOL := FALSE;
    bAlm_AnodeEffectPredicted       : BOOL := FALSE;
    bAlm_HoistMotorOverloadTrip     : BOOL := FALSE;
    bAlm_HoistTravelLimitTrip       : BOOL := FALSE;
    bAlm_PotlineBypassEngaged       : BOOL := FALSE;
    bAlm_EmergencyStopLatched       : BOOL := FALSE;
    bAlm_PointFeederJamAny          : BOOL := FALSE;
    bAlm_TMR_Discrepancy_Volt       : BOOL := FALSE;
    bAlm_TMR_Discrepancy_Curr       : BOOL := FALSE;
    bAlm_TMR_Discrepancy_Temp       : BOOL := FALSE;
    bAlm_TMR_Discrepancy_Pos        : BOOL := FALSE;

    (* Loop and Scratch Variables *)
    i                               : INT := 1;
    j                               : INT := 1;
    k                               : INT := 1;
    nIter                           : INT := 1;
    nStep                           : INT := 0;
    rScratch1                       : REAL := 0.0;
    rScratch2                       : REAL := 0.0;
    rScratch3                       : REAL := 0.0;
    rScratch4                       : REAL := 0.0;
END_VAR'''
