# -*- coding: utf-8 -*-
"""
Generator module: internal variables (VAR block)
"""

def get_var_internal():
    return """VAR
    (* =========================================================================================== *)
    (* 1.0 DISCRETE STATE-SPACE MATRICES & OBSERVER VECTORS (8x8 Dynamics @ Ts = 10 ms)            *)
    (* =========================================================================================== *)
    bMatricesInitialized                : BOOL := FALSE;    (* First-Cycle State Matrix Setup Gate *)
    arrA                                : ARRAY[1..8, 1..8] OF REAL; (* State Transition Dynamics A *)
    arrB                                : ARRAY[1..8, 1..6] OF REAL; (* Actuator Input Coupling B *)
    arrC                                : ARRAY[1..8, 1..8] OF REAL; (* State Observation Matrix C *)
    arrD                                : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedthrough Matrix D *)
    arrX_State                          : ARRAY[1..8] OF REAL; (* Current State Vector x[k] *)
    arrX_Next                           : ARRAY[1..8] OF REAL; (* Predicted State Vector x[k+1] *)
    arrX_Ref                            : ARRAY[1..8] OF REAL; (* Setpoint Target State Vector r[k] *)
    arrX_Err                            : ARRAY[1..8] OF REAL; (* Multivariable State Tracking Error e[k] *)
    arrY_Obs                            : ARRAY[1..8] OF REAL; (* Sensor State Observation Output y[k] *)

    (* Matrix Arithmetic Iteration Indices *)
    nIdx_i                              : INT := 1;         (* Outer Row Loop Index *)
    nIdx_j                              : INT := 1;         (* Inner Column Loop Index *)
    nIdx_m                              : INT := 1;         (* Control Actuator Dimension Index *)
    nIdx_p                              : INT := 1;         (* Observed Output Dimension Index *)
    rAccumulator                        : REAL := 0.0;      (* Scalar Summing Register *)

    (* =========================================================================================== *)
    (* 2.0 RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) MATRICES & COEFFICIENTS                 *)
    (* =========================================================================================== *)
    arrQ_Weight                         : ARRAY[1..8] OF REAL; (* Diagonal State Tracking Cost Penalty *)
    arrR_Weight                         : ARRAY[1..6] OF REAL; (* Actuator Effort Quadratic Penalty *)
    arrS_Weight                         : ARRAY[1..6] OF REAL; (* Actuator Slew Rate Quadratic Penalty *)
    arrP_Weight                         : ARRAY[1..8] OF REAL; (* Terminal Horizon State Cost Penalty *)
    arrU_Cmd                            : ARRAY[1..6] OF REAL; (* Actuator Commands u[k] *)
    arrU_Prev                           : ARRAY[1..6] OF REAL; (* Previous Step Commands u[k-1] *)
    arrU_Min                            : ARRAY[1..6] OF REAL; (* Actuator Lower Saturation Bounds *)
    arrU_Max                            : ARRAY[1..6] OF REAL; (* Actuator Upper Saturation Bounds *)
    arrDeltaU_Max                       : ARRAY[1..6] OF REAL; (* Maximum Allowable Slew Rate / Cycle *)
    arrMPC_X_Pred                       : ARRAY[1..5, 1..8] OF REAL; (* Predicted State Trajectory (5 Horizons) *)
    arrMPC_U_Seq                        : ARRAY[1..5, 1..6] OF REAL; (* Planned Actuator Sequence *)
    arrMPC_Grad                         : ARRAY[1..6] OF REAL; (* Projected Cost Function Gradient *)
    arrMPC_StepSize                     : ARRAY[1..6] OF REAL; (* Gradient Descent Learning Rates *)
    rMPC_CostTotal                      : REAL := 0.0;      (* Total Evaluated Quadratic Cost J *)
    rMPC_CostState                      : REAL := 0.0;      (* State Deviation Quadratic Cost *)
    rMPC_CostInput                      : REAL := 0.0;      (* Actuator Energy Quadratic Cost *)
    rMPC_CostSlew                       : REAL := 0.0;      (* Actuator Slew Rate Penalty Cost *)
    rMPC_CostTerminal                   : REAL := 0.0;      (* Terminal State Horizon Cost *)
    nHorz_k                             : INT := 1;         (* Receding Horizon Step Index (1..5) *)
    nHorz_j                             : INT := 1;         (* Horizon Sub-Loop Index *)
    rStateError                         : REAL := 0.0;      (* Scalar Intermediate State Error *)
    rInputDiff                          : REAL := 0.0;      (* Scalar Intermediate Input Delta *)

    (* =========================================================================================== *)
    (* 3.0 BIOPROCESS KINETICS, RESPIROMETRY & HYDRODYNAMIC CONSTANTS                              *)
    (* =========================================================================================== *)
    rVesselWorkingVolume_L              : REAL := 20000.0;  (* Nominal Mammalian Broth Liquid Volume [L] *)
    rVesselTotalVolume_L                : REAL := 25000.0;  (* Vessel Total Geometric Internal Volume [L] *)
    rMuMax_per_h                        : REAL := 0.038;    (* Max CHO Specific Growth Rate [1/h] *)
    rKs_glc_g_per_L                     : REAL := 0.35;     (* Monod Affinity Constant for Glucose [g/L] *)
    rKi_lac_g_per_L                     : REAL := 4.50;     (* Non-Competitive Lactate Inhibition Constant [g/L] *)
    rKs_gln_mmol_per_L                  : REAL := 0.25;     (* Monod Affinity Constant for Glutamine [mmol/L] *)
    rKi_amm_mmol_per_L                  : REAL := 6.00;     (* Non-Competitive Ammonium Inhibition Constant [mmol/L] *)
    rK_death_per_h                      : REAL := 0.0045;   (* Baseline Cellular Mortality Constant [1/h] *)
    rY_x_glc_g_per_g                    : REAL := 0.28;     (* True Biomass Yield on Substrate Glucose [g/g] *)
    rY_lac_glc_g_per_g                  : REAL := 1.15;     (* Metabolic Lactate Production Yield on Glucose [g/g] *)
    rqO2_max_pmol_per_cell_h            : REAL := 0.22;     (* Maximum Single-Cell Oxygen Uptake [pmol/(cell*h)] *)
    rKO2_pct                            : REAL := 2.50;     (* Michaelis-Menten Oxygen Saturation Constant [%] *)
    rBrothDensity_kg_per_L              : REAL := 1.025;    (* Culture Broth Specific Gravity [kg/L] *)
    rBrothSpecificHeat_kJ_kgK           : REAL := 4.184;    (* Liquid Broth Specific Heat Capacity [kJ/(kg*K)] *)
    rJacketUA_kW_per_K                  : REAL := 18.5;     (* Heat Transfer Surface Overall Conductance [kW/K] *)
    rMembraneArea_m2                    : REAL := 46.0;     (* Hollow-Fiber PES Membrane Surface Area [m2] *)
    rMembraneCleanResistance_per_m      : REAL := 1.45E12;  (* Intrinsic Clean Membrane Hydraulic Resistance [1/m] *)
    rPermeateViscosity_Pa_s             : REAL := 0.00089;  (* Clarified Culture Filtrate Dynamic Viscosity [Pa*s] *)
    rMolarVolumeGas_L_per_mol           : REAL := 22.414;   (* Standard Gas Molar Volume [L/mol] *)
    rInletO2Fraction_Air                : REAL := 0.2095;   (* Ambient Atmospheric Compressed Air O2 Fraction *)
    rInletCO2Fraction_Air               : REAL := 0.0004;   (* Ambient Atmospheric Compressed Air CO2 Fraction *)
    rInletN2Fraction_Air                : REAL := 0.7901;   (* Ambient Atmospheric Compressed Air N2 Fraction *)
    rDilutionRate_per_h                 : REAL := 0.040;    (* Active Perfusion Dilution Rate D = F_perm / V_L [1/h] *)
    rCellBleedRatio                     : REAL := 0.040;    (* Fraction of Perfusion Rate Diverted to Bleed *)

    (* =========================================================================================== *)
    (* 4.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & HEALTH STRUCTURES             *)
    (* =========================================================================================== *)
    (* Group 1: Optical Dissolved Oxygen (dO2 A, B, C) *)
    arrDO_Sensors                       : ARRAY[1..3] OF REAL; (* dO2 raw sensor readings *)
    arrDO_Diff                          : ARRAY[1..3] OF REAL; (* Pairwise absolute discrepancies *)
    arrDO_DiscrepTimer_s                : ARRAY[1..3] OF REAL; (* Persistence discrepancy timers *)
    arrDO_Healthy                       : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor operational status *)
    rDO_Tolerance_pct                   : REAL := 5.0;      (* dO2 2oo3 allowable difference [%] *)
    rDO_DiscrepLimit_s                  : REAL := 1.000;    (* Discrepancy timeout threshold [s] *)
    bDO_Degraded                        : BOOL := FALSE;    (* Voting degraded to 1oo2 mode *)
    bDO_CriticalFault                   : BOOL := FALSE;    (* All dO2 channels disqualified *)

    (* Group 2: Pressurized Gel Glass pH (pH A, B, C) *)
    arrPH_Sensors                       : ARRAY[1..3] OF REAL; (* pH raw sensor readings *)
    arrPH_Diff                          : ARRAY[1..3] OF REAL; (* Pairwise absolute discrepancies *)
    arrPH_DiscrepTimer_s                : ARRAY[1..3] OF REAL; (* Persistence discrepancy timers *)
    arrPH_Healthy                       : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor operational status *)
    rPH_Tolerance                       : REAL := 0.08;     (* pH 2oo3 allowable difference [pH] *)
    rPH_DiscrepLimit_s                  : REAL := 1.500;    (* Discrepancy timeout threshold [s] *)
    bPH_Degraded                        : BOOL := FALSE;    (* Voting degraded to 1oo2 mode *)
    bPH_CriticalFault                   : BOOL := FALSE;    (* All pH channels disqualified *)

    (* Group 3: Core Broth Pt100 RTD Temperature (Temp A, B, C) *)
    arrTemp_Sensors                     : ARRAY[1..3] OF REAL; (* Temp raw sensor readings *)
    arrTemp_Diff                        : ARRAY[1..3] OF REAL; (* Pairwise absolute discrepancies *)
    arrTemp_DiscrepTimer_s              : ARRAY[1..3] OF REAL; (* Persistence discrepancy timers *)
    arrTemp_Healthy                     : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor operational status *)
    rTemp_Tolerance_degC                : REAL := 0.25;     (* Temp 2oo3 allowable difference [deg C] *)
    rTemp_DiscrepLimit_s                : REAL := 0.800;    (* Discrepancy timeout threshold [s] *)
    bTemp_Degraded                      : BOOL := FALSE;    (* Voting degraded to 1oo2 mode *)
    bTemp_CriticalFault                 : BOOL := FALSE;    (* All Temp channels disqualified *)

    (* Group 4: ATF Membrane Retentate Pressure (RetPress A, B, C) *)
    arrRetP_Sensors                     : ARRAY[1..3] OF REAL; (* Retentate pressure raw sensor readings *)
    arrRetP_Diff                        : ARRAY[1..3] OF REAL; (* Pairwise absolute discrepancies *)
    arrRetP_DiscrepTimer_s              : ARRAY[1..3] OF REAL; (* Persistence discrepancy timers *)
    arrRetP_Healthy                     : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor operational status *)
    rRetP_Tolerance_bar                 : REAL := 0.050;    (* Retentate allowable difference [bar] *)
    rRetP_DiscrepLimit_s                : REAL := 0.600;    (* Discrepancy timeout threshold [s] *)
    bRetP_Degraded                      : BOOL := FALSE;    (* Voting degraded to 1oo2 mode *)
    bRetP_CriticalFault                 : BOOL := FALSE;    (* All Retentate channels disqualified *)

    (* Group 5: ATF Membrane Permeate Pressure (PermPress A, B, C) *)
    arrPermP_Sensors                    : ARRAY[1..3] OF REAL; (* Permeate pressure raw sensor readings *)
    arrPermP_Diff                       : ARRAY[1..3] OF REAL; (* Pairwise absolute discrepancies *)
    arrPermP_DiscrepTimer_s             : ARRAY[1..3] OF REAL; (* Persistence discrepancy timers *)
    arrPermP_Healthy                    : ARRAY[1..3] OF BOOL := [TRUE, TRUE, TRUE]; (* Sensor operational status *)
    rPermP_Tolerance_bar                : REAL := 0.040;    (* Permeate allowable difference [bar] *)
    rPermP_DiscrepLimit_s               : REAL := 0.600;    (* Discrepancy timeout threshold [s] *)
    bPermP_Degraded                     : BOOL := FALSE;    (* Voting degraded to 1oo2 mode *)
    bPermP_CriticalFault                : BOOL := FALSE;    (* All Permeate channels disqualified *)

    (* Rate-of-Change (RoC) Memory Registers *)
    rDO_Prev_pct                        : REAL := 50.0;     (* Previous cycle dO2 for RoC calculation *)
    rDO_RoC_pct_per_min                 : REAL := 0.0;      (* dO2 Rate of Change [%/min] *)
    rPH_Prev                            : REAL := 7.05;     (* Previous cycle pH for RoC calculation *)
    rPH_RoC_per_min                     : REAL := 0.0;      (* pH Rate of Change [pH/min] *)
    rTemp_Prev_degC                     : REAL := 37.0;     (* Previous cycle Temp for RoC calculation *)
    rTemp_RoC_degC_per_min              : REAL := 0.0;      (* Temp Rate of Change [deg C/min] *)
    rTMP_Prev_bar                       : REAL := 0.180;    (* Previous cycle TMP for RoC calculation *)
    rTMP_RoC_bar_per_min                : REAL := 0.0;      (* TMP Rate of Change [bar/min] *)

    (* =========================================================================================== *)
    (* 5.0 ISA-18.2 MULTI-TIERED ALARM SETPOINTS, DEADBANDS & LATCH FLAGS                          *)
    (* =========================================================================================== *)
    (* Broth Temperature Setpoints [deg C] *)
    rSP_Temp_HH                         : REAL := 38.50;    (* Temperature Trip High-High (Enzyme denaturation) *)
    rSP_Temp_H                          : REAL := 37.30;    (* Temperature Warning High *)
    rSP_Temp_L                          : REAL := 36.70;    (* Temperature Warning Low *)
    rSP_Temp_LL                         : REAL := 35.50;    (* Temperature Trip Low-Low (Metabolic arrest) *)
    rDeadband_Temp                      : REAL := 0.08;     (* Temperature Alarm Deadband Hysteresis [deg C] *)

    (* Dissolved Oxygen Setpoints [% air sat] *)
    rSP_DO_HH                           : REAL := 75.00;    (* dO2 Trip High-High (Oxidative shear stress) *)
    rSP_DO_H                            : REAL := 65.00;    (* dO2 Warning High *)
    rSP_DO_L                            : REAL := 35.00;    (* dO2 Warning Low *)
    rSP_DO_LL                           : REAL := 20.00;    (* dO2 Trip Low-Low (Cellular anoxia risk) *)
    rDeadband_DO                        : REAL := 2.00;     (* dO2 Alarm Deadband Hysteresis [%] *)

    (* Liquid Broth Core pH Setpoints [pH] *)
    rSP_PH_HH                           : REAL := 7.350;    (* pH Trip High-High (Severe alkalosis) *)
    rSP_PH_H                            : REAL := 7.220;    (* pH Warning High *)
    rSP_PH_L                            : REAL := 6.880;    (* pH Warning Low *)
    rSP_PH_LL                           : REAL := 6.750;    (* pH Trip Low-Low (Acidosis / Lactate spike) *)
    rDeadband_PH                        : REAL := 0.030;    (* pH Alarm Deadband Hysteresis [pH] *)

    (* Transmembrane Pressure TMP Setpoints [bar] *)
    rSP_TMP_HH                          : REAL := 0.400;    (* TMP Trip High-High (Severe membrane fouling / rupture risk) *)
    rSP_TMP_H                           : REAL := 0.320;    (* TMP Warning High (Trigger automatic backpulse) *)
    rSP_TMP_L                           : REAL := 0.050;    (* TMP Warning Low (Permeate line leak / siphon) *)
    rSP_TMP_LL                          : REAL := 0.010;    (* TMP Trip Low-Low (Diaphragm pump decoupling) *)
    rDeadband_TMP                       : REAL := 0.015;    (* TMP Alarm Deadband Hysteresis [bar] *)

    (* Viable Cell Density Setpoints [10^6 cells/mL] *)
    rSP_VCD_HH                          : REAL := 120.00;   (* VCD High-High (Oxygen mass transfer limit exceeded) *)
    rSP_VCD_H                           : REAL := 105.00;   (* VCD High Warning (Increase cell bleed rate) *)
    rSP_VCD_L                           : REAL := 60.00;    (* VCD Low Warning (Inadequate perfusion biomass) *)
    rSP_VCD_LL                          : REAL := 40.00;    (* VCD Low-Low Trip (Severe culture wash-out) *)
    rDeadband_VCD                       : REAL := 2.50;     (* VCD Alarm Deadband Hysteresis [10^6 cells/mL] *)

    (* Raman Glucose Substrate Setpoints [g/L] *)
    rSP_Glc_HH                          : REAL := 8.00;     (* Glucose High-High (Osmolality elevation) *)
    rSP_Glc_H                           : REAL := 6.00;     (* Glucose High Warning *)
    rSP_Glc_L                           : REAL := 2.00;     (* Glucose Low Warning (Starvation onset) *)
    rSP_Glc_LL                          : REAL := 1.00;     (* Glucose Low-Low Trip (Apoptosis trigger) *)
    rDeadband_Glc                       : REAL := 0.25;     (* Glucose Alarm Deadband Hysteresis [g/L] *)

    (* Raman Lactate Byproduct Setpoints [g/L] *)
    rSP_Lac_HH                          : REAL := 3.50;     (* Lactate High-High Trip (Cytotoxic accumulation) *)
    rSP_Lac_H                           : REAL := 2.50;     (* Lactate High Warning *)
    rDeadband_Lac                       : REAL := 0.15;     (* Lactate Alarm Deadband Hysteresis [g/L] *)

    (* Headspace Foam Conductivity Setpoints [%] *)
    rSP_Foam_HH                         : REAL := 40.0;     (* Foam High-High Trip (Filter fouling danger) *)
    rSP_Foam_H                          : REAL := 20.0;     (* Foam High Warning (Trigger antifoam micro-dosing) *)
    rDeadband_Foam                      : REAL := 3.0;      (* Foam Deadband Hysteresis [%] *)

    (* ISA-18.2 Latch Flags *)
    bAlarm_Temp_HH                      : BOOL := FALSE;
    bAlarm_Temp_H                       : BOOL := FALSE;
    bAlarm_Temp_L                       : BOOL := FALSE;
    bAlarm_Temp_LL                      : BOOL := FALSE;
    bAlarm_DO_HH                        : BOOL := FALSE;
    bAlarm_DO_H                         : BOOL := FALSE;
    bAlarm_DO_L                         : BOOL := FALSE;
    bAlarm_DO_LL                        : BOOL := FALSE;
    bAlarm_PH_HH                        : BOOL := FALSE;
    bAlarm_PH_H                         : BOOL := FALSE;
    bAlarm_PH_L                         : BOOL := FALSE;
    bAlarm_PH_LL                        : BOOL := FALSE;
    bAlarm_TMP_HH                       : BOOL := FALSE;
    bAlarm_TMP_H                        : BOOL := FALSE;
    bAlarm_TMP_L                        : BOOL := FALSE;
    bAlarm_TMP_LL                       : BOOL := FALSE;
    bAlarm_VCD_HH                       : BOOL := FALSE;
    bAlarm_VCD_H                        : BOOL := FALSE;
    bAlarm_VCD_L                        : BOOL := FALSE;
    bAlarm_VCD_LL                       : BOOL := FALSE;
    bAlarm_Glc_HH                       : BOOL := FALSE;
    bAlarm_Glc_H                        : BOOL := FALSE;
    bAlarm_Glc_L                        : BOOL := FALSE;
    bAlarm_Glc_LL                       : BOOL := FALSE;
    bAlarm_Lac_HH                       : BOOL := FALSE;
    bAlarm_Lac_H                        : BOOL := FALSE;
    bAlarm_Foam_HH                      : BOOL := FALSE;
    bAlarm_Foam_H                       : BOOL := FALSE;
    bAlarm_DO_RoC                       : BOOL := FALSE;
    bAlarm_PH_RoC                       : BOOL := FALSE;
    bAlarm_TMP_RoC                      : BOOL := FALSE;

    (* =========================================================================================== *)
    (* 6.0 DETERMINISTIC 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES                 *)
    (* =========================================================================================== *)
    nFSM_State                          : INT := 0;         (* Active FSM State (0 to 11) *)
    nFSM_SubState                       : INT := 0;         (* Active Sub-State Sequence Step *)
    rFSM_StateTimer_s                   : REAL := 0.0;      (* Elapsed Dwell Time in Current State [s] *)
    rFSM_SubTimer_s                     : REAL := 0.0;      (* Elapsed Sub-Phase Timer [s] *)
    bStateHoldActive                    : BOOL := FALSE;    (* Interlock Holding State Transition *)
    bTransitionPermitted                : BOOL := FALSE;    (* Automatic Forward Step Permissive *)

    (* Process Stage Integrators & Accumulators *)
    rSIP_Lethality_F0_accum             : REAL := 0.0;      (* Steam-in-Place Thermal Lethality F0 [min] *)
    rSIP_TargetLethality_F0             : REAL := 30.0;     (* Target Sterile Lethality (F0 = 30.0 min @ 121.1 C) *)
    rMediaFillIntegrated_L              : REAL := 0.0;      (* Cumulative Volume of Sterile Media Loaded [L] *)
    rBatchGrowthHours                   : REAL := 0.0;      (* Batch Seed Phase Integrated Runtime [h] *)
    rExponentialGrowthHours             : REAL := 0.0;      (* Exponential Growth Phase Integrated Runtime [h] *)
    rChemostatSteadyHours               : REAL := 0.0;      (* Continuous Perfusion Integrated Runtime [h] *)
    rDeactivationTimer_s                : REAL := 0.0;      (* Post-Harvest Thermal Inactivation Timer [s] *)

    (* =========================================================================================== *)
    (* 7.0 ATF DIAPHRAGM PNEUMATIC OSCILLATION & ANTIFOULING BACKPULSE REGISTERS                   *)
    (* =========================================================================================== *)
    rATF_PressureStrokeDuration_s       : REAL := 8.50;     (* Pneumatic Forward Pressure Stroke Time [s] *)
    rATF_VacuumStrokeDuration_s         : REAL := 8.50;     (* Pneumatic Reverse Vacuum Exhaust Time [s] *)
    rATF_CycleTimer_s                   : REAL := 0.0;      (* Diaphragm Oscillation Period Elapsed Timer [s] *)
    nATF_StrokePhase                    : INT := 0;         (* Diaphragm Phase: 0 = Vacuum/Aspirate, 1 = Pressure/Expel *)
    bATF_BackpulseActive                : BOOL := FALSE;    (* Reverse Permeate Backpulse Active Gate *)
    rATF_BackpulseTimer_s               : REAL := 0.0;      (* Backpulse Duration Elapsed Timer [s] *)
    rATF_BackpulseDuration_s            : REAL := 3.20;     (* Commanded Reverse Backpulse Duration [s] *)
    nCumulativeBackpulseCount           : DINT := 0;        (* Total Lifetime Backpulse Invocations *)
    rATF_PressurePWM                    : REAL := 75.0;     (* Calibrated Pressure Solenoid PWM Command [%] *)
    rATF_VacuumPWM                      : REAL := 80.0;     (* Calibrated Vacuum Solenoid PWM Command [%] *)

    (* =========================================================================================== *)
    (* 8.0 4-GAS MASS FLOW CONTROLLER CASCADE & pH DECOUPLED DOSING BUFFERS                        *)
    (* =========================================================================================== *)
    rGas_BaseAirFlow_SLPM               : REAL := 350.0;    (* Baseline Compressed Air Aeration Flow [SLPM] *)
    rGas_O2_EnrichmentFlow_SLPM         : REAL := 0.0;      (* Dynamic Pure O2 Enrichment Flow [SLPM] *)
    rGas_N2_StrippingFlow_SLPM          : REAL := 0.0;      (* Dynamic Pure N2 dO2 Stripping Flow [SLPM] *)
    rGas_CO2_AcidTrimFlow_SLPM          : REAL := 0.0;      (* Dynamic Pure CO2 Acidic Shift Sparge Flow [SLPM] *)
    rBase_DosingRate_mLph               : REAL := 0.0;      (* Calculated NaHCO3 Peristaltic Feed Rate [mL/h] *)
    rPH_DeadbandCenter                  : REAL := 7.050;    (* Target Core Broth Acidity Setpoint [pH] *)
    rPH_ControlDeadband                 : REAL := 0.020;    (* Inactive Deadband Width Preventing Gas/Base Titration [pH] *)
    rBase_Kp                            : REAL := 250.0;    (* Base Dosing Proportional Injection Gain *)
    rCO2_Kp                             : REAL := 45.0;     (* CO2 Sparge Proportional Injection Gain *)

    (* =========================================================================================== *)
    (* 9.0 PRECISION THERMAL JACKET SPLIT-RANGE DUAL-VALVE CONTROLLER BUFFERS                      *)
    (* =========================================================================================== *)
    rJacket_ThermalOutput               : REAL := 0.0;      (* Internal PID Thermal Effort (-100% Cooling to +100% Heating) *)
    rJacket_SteamValveCmd               : REAL := 0.0;      (* Modulating High-Pressure Steam Control Valve [%] *)
    rJacket_ChilledWaterCmd             : REAL := 0.0;      (* Modulating Secondary Glycol/Chilled Water Valve [%] *)
    rJacket_Error                       : REAL := 0.0;      (* Temperature Tracking Error e_T = SP - BrothTemp [deg C] *)
    rJacket_ErrorIntegral               : REAL := 0.0;      (* Anti-Windup Temperature Error Integral [deg C*s] *)
    rJacket_Kp                          : REAL := 85.0;     (* Proportional Controller Gain [% / deg C] *)
    rJacket_Ki                          : REAL := 0.12;     (* Integral Controller Gain [% / (deg C * s)] *)
    rJacket_Kd                          : REAL := 15.0;     (* Derivative Controller Gain [% * s / deg C] *)

    (* =========================================================================================== *)
    (* 10.0 ANTIFOAM MICRO-DOSING CONTROLLER BUFFERS                                               *)
    (* =========================================================================================== *)
    bAntifoamPumpingActive              : BOOL := FALSE;    (* Antifoam Peristaltic Run Indicator *)
    rAntifoamPulseTimer_s               : REAL := 0.0;      (* Dosing Pulse Duty Cycle Timer [s] *)
    rAntifoamCycleDuration_s            : REAL := 10.0;     (* Repeating Dosing Period [s] *)
    rAntifoamOnTime_s                   : REAL := 1.5;      (* Active Injection Pulse Width [s] *)
    rAntifoamTotalDelivered_kg          : REAL := 0.0;      (* Cumulative Consumed Antifoam Emulsion [kg] *)
END_VAR
"""

print("get_var_internal ready.")
