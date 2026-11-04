# scripts/feedmill_builder/part2_var.py
# -*- coding: utf-8 -*-

def get_var_block():
    return """VAR
    (* ====================================================================================================
       1. DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (8-STATE, 6-INPUT, 3-DISTURBANCE, Ts = 50 ms)
       ==================================================================================================== *)
    bModelInitialized               : BOOL := FALSE;    (* Cold-Start Model Embedding Flag *)
    
    (* System State-Space Matrix A (8x8) *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL;
    (* Input Actuator Coupling Matrix B (8x6) *)
    B_mat                           : ARRAY[1..8, 1..6] OF REAL;
    (* Disturbance Coupling Matrix E (8x3) *)
    E_mat                           : ARRAY[1..8, 1..3] OF REAL;
    (* Output Measurement Matrix C (8x8) *)
    C_mat                           : ARRAY[1..8, 1..8] OF REAL;
    (* Feedthrough Matrix D (8x6) *)
    D_mat                           : ARRAY[1..8, 1..6] OF REAL;

    (* Real-Time State Vectors *)
    x_state                         : ARRAY[1..8] OF REAL;  (* Current Plant State x(k) *)
    x_next                          : ARRAY[1..8] OF REAL;  (* One-Step Ahead Predicted State x(k+1) *)
    x_prev                          : ARRAY[1..8] OF REAL;  (* Previous Step State Vector x(k-1) *)
    x_target                        : ARRAY[1..8] OF REAL;  (* Active Target Setpoint Vector x_sp *)
    x_error                         : ARRAY[1..8] OF REAL;  (* State Tracking Error e_x = x_state - x_target *)

    (* Manipulated Control Actuator Vectors *)
    u_ctrl                          : ARRAY[1..6] OF REAL;  (* Current Computed Control Actuators u(k) *)
    u_prev                          : ARRAY[1..6] OF REAL;  (* Previous Execution Control Actuators u(k-1) *)
    u_delta                         : ARRAY[1..6] OF REAL;  (* Rate-of-Change Increment Delta_u = u - u_prev *)
    u_min                           : ARRAY[1..6] OF REAL;  (* Absolute Actuator Lower Clamping Bounds *)
    u_max                           : ARRAY[1..6] OF REAL;  (* Absolute Actuator Upper Clamping Bounds *)
    du_max                          : ARRAY[1..6] OF REAL;  (* Maximum Allowable Slew Rate per Execution Scan *)

    (* Disturbance Vector *)
    d_dist                          : ARRAY[1..3] OF REAL;  (* External Process Disturbances [Tin, Win, Phdr] *)

    (* ====================================================================================================
       2. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & BUFFERS (Np = 3 HORIZON)
       ==================================================================================================== *)
    (* MPC Quadratic Penalty Weights *)
    Q_diag                          : ARRAY[1..8] OF REAL;  (* Diagonal State Tracking Penalty Weights *)
    R_diag                          : ARRAY[1..6] OF REAL;  (* Diagonal Actuator Slew Rate Penalties *)
    P_diag                          : ARRAY[1..8] OF REAL;  (* Diagonal Terminal Horizon Penalty Weights *)

    (* Receding-Horizon Predicted Trajectories over Np = 3 Steps *)
    x_pred                          : ARRAY[1..3, 1..8] OF REAL; (* Trajectory Predictions for Steps 1, 2, 3 *)
    J_cost                          : REAL;                 (* Evaluated Total Quadratic Horizon Cost J *)
    u_gradient                      : ARRAY[1..6] OF REAL;  (* Analytical Gradient of Cost wrt Control u *)
    rMpcStepGamma                   : REAL := 0.0125;       (* Adaptive Gradient Projection Step Size *)

    (* ====================================================================================================
       3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING STRUCTURES & DISCREPANCY TIMERS
       ==================================================================================================== *)
    (* Triplet 1: Conditioner Discharge Mash Temperature (TE101A, TE101B, TE101C) [deg C] *)
    rTmr_CondTemp_Val               : REAL;
    bTmr_CondTemp_Discrep_AB        : BOOL;
    bTmr_CondTemp_Discrep_BC        : BOOL;
    bTmr_CondTemp_Discrep_CA        : BOOL;
    tTmr_CondTemp_Timer_AB          : REAL := 0.0;
    tTmr_CondTemp_Timer_BC          : REAL := 0.0;
    tTmr_CondTemp_Timer_CA          : REAL := 0.0;
    bTmr_CondTemp_Fault_A           : BOOL := FALSE;
    bTmr_CondTemp_Fault_B           : BOOL := FALSE;
    bTmr_CondTemp_Fault_C           : BOOL := FALSE;
    bTmr_CondTemp_Degraded_1oo2     : BOOL := FALSE;
    bTmr_CondTemp_Trip_0oo3         : BOOL := FALSE;

    (* Triplet 2: Pellet Press 400 kW Motor Phase Current (JT201A, JT201B, JT201C) [A] *)
    rTmr_PressCurr_Val              : REAL;
    bTmr_PressCurr_Discrep_AB       : BOOL;
    bTmr_PressCurr_Discrep_BC       : BOOL;
    bTmr_PressCurr_Discrep_CA       : BOOL;
    tTmr_PressCurr_Timer_AB         : REAL := 0.0;
    tTmr_PressCurr_Timer_BC         : REAL := 0.0;
    tTmr_PressCurr_Timer_CA         : REAL := 0.0;
    bTmr_PressCurr_Fault_A          : BOOL := FALSE;
    bTmr_PressCurr_Fault_B          : BOOL := FALSE;
    bTmr_PressCurr_Fault_C          : BOOL := FALSE;
    bTmr_PressCurr_Degraded_1oo2    : BOOL := FALSE;
    bTmr_PressCurr_Trip_0oo3        : BOOL := FALSE;

    (* Triplet 3: Roller Gap Dynamic Hydraulic Pressure (PT202A, PT202B, PT202C) [bar] *)
    rTmr_HydGapPress_Val            : REAL;
    bTmr_HydGapPress_Discrep_AB     : BOOL;
    bTmr_HydGapPress_Discrep_BC     : BOOL;
    bTmr_HydGapPress_Discrep_CA     : BOOL;
    tTmr_HydGapPress_Timer_AB       : REAL := 0.0;
    tTmr_HydGapPress_Timer_BC       : REAL := 0.0;
    tTmr_HydGapPress_Timer_CA       : REAL := 0.0;
    bTmr_HydGapPress_Fault_A        : BOOL := FALSE;
    bTmr_HydGapPress_Fault_B        : BOOL := FALSE;
    bTmr_HydGapPress_Fault_C        : BOOL := FALSE;
    bTmr_HydGapPress_Degraded_1oo2  : BOOL := FALSE;
    bTmr_HydGapPress_Trip_0oo3      : BOOL := FALSE;

    (* Triplet 4: Counterflow Cooler Microwave Bed Level (LT301A, LT301B, LT301C) [mm] *)
    rTmr_CoolerLevel_Val            : REAL;
    bTmr_CoolerLevel_Discrep_AB     : BOOL;
    bTmr_CoolerLevel_Discrep_BC     : BOOL;
    bTmr_CoolerLevel_Discrep_CA     : BOOL;
    tTmr_CoolerLevel_Timer_AB       : REAL := 0.0;
    tTmr_CoolerLevel_Timer_BC       : REAL := 0.0;
    tTmr_CoolerLevel_Timer_CA       : REAL := 0.0;
    bTmr_CoolerLevel_Fault_A        : BOOL := FALSE;
    bTmr_CoolerLevel_Fault_B        : BOOL := FALSE;
    bTmr_CoolerLevel_Fault_C        : BOOL := FALSE;
    bTmr_CoolerLevel_Degraded_1oo2  : BOOL := FALSE;
    bTmr_CoolerLevel_Trip_0oo3      : BOOL := FALSE;

    (* General 2oo3 Discrepancy Limits & Integration Time Constants *)
    rDiscrepLimit_CondTemp_degC     : REAL := 4.5;      (* Discrepancy Margin for Mash Temp [deg C] *)
    rDiscrepLimit_PressCurr_A       : REAL := 35.0;     (* Discrepancy Margin for Motor Current [A] *)
    rDiscrepLimit_HydGapPress_bar   : REAL := 18.0;     (* Discrepancy Margin for Hydraulic Gap [bar] *)
    rDiscrepLimit_CoolerLevel_mm    : REAL := 85.0;     (* Discrepancy Margin for Cooler Bed Level [mm] *)
    tDiscrepTimeout_s               : REAL := 2.50;     (* Discrepancy Persistent Debounce Time [s] *)

    (* ====================================================================================================
       4. REAL-TIME CYBER-PHYSICAL PROPERTY ESTIMATORS & KINETIC OBSERVERS
       ==================================================================================================== *)
    (* Starch Gelatinization Kinetic Variables *)
    rGelat_k0                       : REAL := 1.25E7;   (* Kinetic Frequency Pre-exponential Factor [s^-1] *)
    rGelat_Ea                       : REAL := 68500.0;  (* Activation Energy [J/mol] *)
    rGelat_Rgas                     : REAL := 8.314;    (* Universal Gas Constant [J/(mol*K)] *)
    rGelat_Wcrit                    : REAL := 11.8;     (* Threshold Critical Moisture Level [%] *)
    rGelat_Wref                     : REAL := 5.0;      (* Reference Moisture Spread [%] *)
    rGelat_BetaW                    : REAL := 1.45;     (* Non-linear Moisture Plasticization Exponent *)
    rGelat_GammaShear               : REAL := 0.0028;   (* Paddle Shaft Shear Rate Sensitizer [rpm^-1] *)
    rGelat_nOrder                   : REAL := 1.20;     (* Order of Starch Gelatinization Reaction *)
    rGelat_Rate_dAlpha_dt           : REAL := 0.0;      (* Real-Time Gelatinization Rate [s^-1] *)
    rGelat_State_Alpha              : REAL := 0.08;     (* Integrated Starch Gelatinization Index [0..1] *)

    (* Culinary Steam Mass & Thermal Enthalpy Balance *)
    rSteam_mDot_Max_kg_s            : REAL := 0.55;     (* Max Saturated Steam Injection Flow Rate [kg/s] *)
    rSteam_mDot_Actual_kg_s         : REAL := 0.0;      (* Calculated Actual Steam Injected [kg/s] *)
    rSteam_hfg_kJ_kg                : REAL := 2148.1;   (* Steam Latent Heat at 2.5 bar(g) [kJ/kg] *)
    rSteam_hg_kJ_kg                 : REAL := 2732.4;   (* Total Saturated Steam Enthalpy [kJ/kg] *)
    rMash_HeatCap_cp                : REAL := 1.88;     (* Poultry/Swine Mash Specific Heat [kJ/(kg*K)] *)
    rWater_HeatCap_cp               : REAL := 4.184;    (* Liquid Water Specific Heat [kJ/(kg*K)] *)
    rMash_FlowRate_kg_s             : REAL := 0.0;      (* Gravimetric Mash Feed Mass Flow [kg/s] *)
    rMash_MoistUptake_pct           : REAL := 0.0;      (* Calculated Net Moisture Condensation Uptake [%] *)

    (* Ring-Die Pellet Press Mechanical, Tribological & Electrical Balance *)
    rPress_FullLoadCurrent_A        : REAL := 715.0;    (* 400 kW Motor Rated Full-Load Amperage [A] *)
    rPress_ActivePower_kW           : REAL := 0.0;      (* Calculated Active Electric Power [kW] *)
    rPress_MechanicalTorque_Nm      : REAL := 0.0;      (* Effective Shaft Drive Torque [Nm] *)
    rPress_SpecificEnergy_kWh_t     : REAL := 0.0;      (* SEC Energy Consumption Index [kWh/t] *)
    rPress_DieDiameter_mm           : REAL := 900.0;    (* Ring Die Internal Track Working Diameter [mm] *)
    rPress_RollerDiameter_mm        : REAL := 420.0;    (* Twin Roller External Rolling Diameter [mm] *)
    rPress_DieLinearSpeed_m_s       : REAL := 0.0;      (* Die Ring Tangential Surface Velocity [m/s] *)
    rPress_RollerLinearSpeed_m_s    : REAL := 0.0;      (* Roller Tangential Surface Velocity [m/s] *)
    rPress_RollerSlip_Ratio         : REAL := 0.0;      (* Dynamic Traction Slip Factor [0.0..1.0] *)
    rPress_DieThermalExp_mm         : REAL := 0.0;      (* Die Ring Radial Thermal Expansion [mm] *)
    rPress_EffectiveGap_mm          : REAL := 0.65;     (* Net Corrected Roller-Die Extrusion Gap [mm] *)
    rPress_ShearStress_MPa          : REAL := 0.0;      (* Estimated Main Shaft Shear Pin Stress [MPa] *)

    (* Counterflow Cooler Psychrometrics & Chung-Pfost Moisture Equilibrium *)
    rCooler_BedArea_m2              : REAL := 6.25;     (* Cooler Active Bed Cross-Sectional Area [m2] *)
    rCooler_PelletBulkDensity       : REAL := 650.0;    (* Extruded Pellets Bulk Density [kg/m3] *)
    rCooler_AirDensity              : REAL := 1.205;    (* Intake Ambient Air Density [kg/m3] *)
    rCooler_AirSpecificHeat         : REAL := 1.005;    (* Dry Air Specific Heat [kJ/(kg*K)] *)
    rCooler_EMC_ChungPfost_C1       : REAL := 0.165;    (* Chung-Pfost Empirical Constant C1 *)
    rCooler_EMC_ChungPfost_C2       : REAL := 35.80;    (* Chung-Pfost Empirical Constant C2 *)
    rCooler_EMC_ChungPfost_C3       : REAL := 452.0;    (* Chung-Pfost Empirical Constant C3 *)
    rCooler_EMC_EquilibriumMoist    : REAL := 12.15;    (* Equilibrium Moisture Content at Intake RH/T [%] *)
    rCooler_BedHoldupMass_kg        : REAL := 0.0;      (* Calculated Pellet Bed Mass [kg] *)
    rCooler_ResidenceTime_min       : REAL := 0.0;      (* Pellets Active Cooling Residence Time [min] *)

    (* Vacuum Coater Batch Cycle Process Variables *)
    rCoater_EvacTarget_bar          : REAL := -0.85;    (* Target Evacuation Gauge Vacuum Pressure [bar] *)
    rCoater_EvacRate_bar_s          : REAL := 0.0;      (* Real-Time Chamber Drawdown Depressurization Rate [bar/s] *)
    rCoater_FatMassDosed_kg         : REAL := 0.0;      (* Accumulated Fat Dose Injected into Batch [kg] *)
    rCoater_EnzymeMassDosed_g       : REAL := 0.0;      (* Micro-Metered Liquid Enzyme Dose [g] *)
    rCoater_CapillaryPenetration    : REAL := 0.0;      (* Estimated Depth of Micro-Pore Fat Core Infusion [0..1] *)

    (* ====================================================================================================
       5. 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES
       ==================================================================================================== *)
    nFsm_CurrentState               : INT := 0;         (* Active Operational State Index (0 to 11) *)
    nFsm_PreviousState              : INT := 0;         (* Previous Scan Operational State Index *)
    bFsm_StateFirstScan             : BOOL := TRUE;     (* One-Shot State Transition Pulse Flag *)
    rFsm_StateTimeElapsed_s         : REAL := 0.0;      (* Continuous Running Timer in Current State [s] *)
    bFsm_StateTimeoutAlarm          : BOOL := FALSE;    (* State Maximum Permitted Duration Exceeded *)
    bFsm_InterlockTripped           : BOOL := FALSE;    (* Safety or Hardware Interlock Immediate Trip *)
    nFsm_ShearPinTripLatch          : BOOL := FALSE;    (* Mechanical Shear Pin Latching Trip Flag *)
    nFsm_DieChokeFaultLatch         : BOOL := FALSE;    (* Pellet Mill Jam / Die Choke Overload Latch *)

    (* FSM Sequence Time Constants *)
    tFsm_SteamPurgeTime_s           : REAL := 35.0;     (* Saturated Steam Condensate Purge Time [s] *)
    tFsm_PreheatTime_s              : REAL := 60.0;     (* Conditioner Empty Cylinder Warm-up Time [s] *)
    tFsm_MillStarDelta_s            : REAL := 12.0;     (* 400 kW Motor Star-Delta / Soft-Start Ramp [s] *)
    tFsm_FeederInitialRamp_s        : REAL := 45.0;     (* Feeder Gentle Ramp from 0 to 15% Flow [s] *)
    tFsm_CondEquilibration_s        : REAL := 90.0;     (* Mash Hydrothermal Equilibrating Duration [s] *)
    tFsm_FlushShutdown_s            : REAL := 75.0;     (* Dry Purge Meal Die Clean-Out Duration [s] *)

    (* ====================================================================================================
       6. ISA-18.2 MULTI-TIERED ALARM ENGINE & TRIP THRESHOLDS
       ==================================================================================================== *)
    (* Alarm Trip Limits: Conditioner Mash Temperature [deg C] *)
    rAlarmTrip_CondTemp_HH          : REAL := 98.0;     (* High-High Trip: Protein Denaturation / Scorch *)
    rAlarmTrip_CondTemp_H           : REAL := 94.0;     (* High Warning: Approaching Thermal Max *)
    rAlarmTrip_CondTemp_L           : REAL := 82.0;     (* Low Warning: Inadequate Gelatinization *)
    rAlarmTrip_CondTemp_LL          : REAL := 65.0;     (* Low-Low Trip: Severe Under-Temperature Choke Risk *)
    rAlarmDeadband_CondTemp         : REAL := 1.5;      (* Thermal Deadband Hysteresis [deg C] *)

    (* Alarm Trip Limits: Conditioned Mash Moisture [%] *)
    rAlarmTrip_MashMoist_HH         : REAL := 18.5;     (* High-High Trip: Imminent Die Choke & Roller Slip *)
    rAlarmTrip_MashMoist_H          : REAL := 17.2;     (* High Warning: High Water Content *)
    rAlarmTrip_MashMoist_L          : REAL := 14.5;     (* Low Warning: Brittle Pellet / High SEC *)
    rAlarmTrip_MashMoist_LL         : REAL := 12.5;     (* Low-Low Trip: High Die Wear / Mechanical Jam *)
    rAlarmDeadband_MashMoist        : REAL := 0.4;      (* Moisture Deadband Hysteresis [%] *)

    (* Alarm Trip Limits: Pellet Press 400 kW Motor Current [A] *)
    rAlarmTrip_PressCurr_HH_Inst    : REAL := 760.0;    (* Instantaneous Die Overload Shear Pin Trip [A] *)
    rAlarmTrip_PressCurr_HH_Timed   : REAL := 720.0;    (* Timed (3.0s) High-High Motor Overload Trip [A] *)
    rAlarmTrip_PressCurr_H          : REAL := 660.0;    (* High Warning: Near Full-Load Current [A] *)
    rAlarmTrip_PressCurr_L          : REAL := 240.0;    (* Low Warning: Drive Belt Slippage / Feed Loss [A] *)
    tAlarmPressCurr_Timer_HH        : REAL := 0.0;      (* Timed Overcurrent Accumulator [s] *)

    (* Alarm Trip Limits: Dynamic Hydraulic Roller Gap Pressure [bar] *)
    rAlarmTrip_HydPress_HH          : REAL := 220.0;    (* High-High Trip: Hydraulic Ram Hydrostatic Surge [bar] *)
    rAlarmTrip_HydPress_H           : REAL := 185.0;    (* High Warning: Heavy Extrusion Resistance [bar] *)
    rAlarmTrip_HydPress_L           : REAL := 45.0;     (* Low Warning: Loss of Mash Extrusion Cushion [bar] *)
    rAlarmTrip_HydPress_LL          : REAL := 25.0;     (* Low-Low Trip: Hydraulic Accumulator Failure [bar] *)

    (* Alarm Trip Limits: Ring Die Face Optical Temperature [deg C] *)
    rAlarmTrip_DieTemp_HH           : REAL := 125.0;    (* High-High Trip: Metal Friction / Galling Risk [deg C] *)
    rAlarmTrip_DieTemp_H            : REAL := 112.0;    (* High Warning: High Extrusion Friction [deg C] *)

    (* Alarm Trip Limits: Roller Dynamic Slip Factor [0..1] *)
    rAlarmTrip_RollerSlip_HH        : REAL := 0.35;     (* High-High Trip: Roller Stall / Impending Choke *)
    rAlarmTrip_RollerSlip_H         : REAL := 0.18;     (* High Warning: Traction Breakdown Warning *)

    (* Alarm Trip Limits: Counterflow Cooler Bed Level [mm] *)
    rAlarmTrip_CoolerBed_HH         : REAL := 1420.0;   (* High-High Trip: Cooler Intake Chute Overflow [mm] *)
    rAlarmTrip_CoolerBed_H          : REAL := 1250.0;   (* High Warning: High Bed Level [mm] *)
    rAlarmTrip_CoolerBed_L          : REAL := 500.0;    (* Low Warning: Under-Retention / Warm Pellets [mm] *)
    rAlarmTrip_CoolerBed_LL         : REAL := 250.0;    (* Low-Low Trip: Complete Bed Depletion [mm] *)

    (* Diagnostic Iteration Indices & General Loop Variables *)
    i                               : INT := 1;
    j                               : INT := 1;
    m                               : INT := 1;
    k_step                          : INT := 1;
    rTempAccum                      : REAL := 0.0;
    rSumPredCost                    : REAL := 0.0;
END_VAR
"""
