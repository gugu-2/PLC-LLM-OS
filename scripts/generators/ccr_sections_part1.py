# -*- coding: utf-8 -*-
"""
Part 1 of CCR Platforming Function Block: Header, VAR_INPUT, VAR_OUTPUT, VAR declarations.
"""

def get_header():
    return """FUNCTION_BLOCK FB_Chemical_CCR_NaphthaReformer_MultiBedInterheater
(*
    ======================================================================================================
    LUMINA CYBER-PHYSICAL SYSTEMS SWARM - V7 MAX-PERSONA ENGINEERING STANDARD
    PETROLEUM REFINING & PETROCHEMICAL CATALYSIS DIVISION
    ------------------------------------------------------------------------------------------------------
    SYSTEM: 45,000 BPD CONTINUOUS CATALYTIC REFORMING (CCR) PLATFORMING UNIT
    ARCHITECTURE: QUAD MULTI-BED RADIAL-FLOW REACTORS (Rx-101..104) WITH DIRECT-FIRED INTERHEATERS (F-101..104),
                  CONTINUOUS CATALYST GRAVITY CIRCULATION & OXYCHLORINATION REGENERATION LOOP,
                  15 MW HIGH-PRESSURE HYDROGEN RECYCLE COMPRESSOR, AND REFORMATE OCTANE / C5+ YIELD MPC
    DESIGNATION: FB_Chemical_CCR_NaphthaReformer_MultiBedInterheater
    EXECUTION CYCLE: 1000 ms DETERMINISTIC DISCRETE UPDATE (1.0 s)
    STANDARDS: IEC 61131-3 3RD ED, ISA-18.2 ALARM MANAGEMENT, API 560 FIRED HEATERS,
               API 670 ROTATING MACHINERY PROTECTION, NFPA 85 BOILER/COMBUSTION HAZARDS
    ======================================================================================================
    PROCESS SUMMARY:
    Continuous Catalytic Reforming converts low-octane heavy straight-run naphtha (feed rate ~298.0 m3/h,
    density ~755.0 kg/m3, N+2A index 45-65 vol%) into high-octane aromatic-rich motor fuel blendstock
    (Target: 102.0 RON) while simultaneously generating high-purity hydrogen byproduct (80-92 mol% H2).
    
    The reaction mechanism occurs across four radial-flow catalyst beds with intermediate reheating:
      Bed 1 (Rx-101): Rapid endothermic dehydrogenation of cyclohexanes/alkylcyclohexanes to aromatics
                      (Delta H_rxn ~ +220 kJ/mol). Large temperature drop (Delta T ~ 45 - 60 deg C).
      Interheater 1 (F-102): Radiant furnace reheats Bed 1 effluent back to target inlet temperature (495 - 530 deg C).
      Bed 2 (Rx-102): Continuing naphthene dehydrogenation & alkylcyclopentane dehydroisomerization.
                      (Delta T ~ 25 - 40 deg C).
      Interheater 2 (F-103): Reheats Bed 2 effluent back to target inlet temperature.
      Bed 3 (Rx-103): Paraffin dehydrocyclization (alkanes -> aromatics + H2, Delta H_rxn ~ +255 kJ/mol)
                      and initial paraffin hydrocracking (Delta H_rxn ~ -55 kJ/mol). (Delta T ~ 12 - 25 deg C).
      Interheater 3 (F-104): Final interheater reheating Bed 3 effluent.
      Bed 4 (Rx-104): Final dehydrocyclization, slow isomerization, and octane-cracking equilibrium.
                      (Delta T ~ 5 - 15 deg C).
    
    Weighted Average Bed Temperature (WABT) is calculated with catalyst inventory weighting:
      w_cat = [0.10, 0.15, 0.30, 0.45] representing 10%, 15%, 30%, 45% catalyst mass in Beds 1, 2, 3, 4.
    
    SAFETY & CONTROL LAYERS:
      - 2oo3 Triple Modular Redundancy (TMR) voting across 11 critical process sensor trios.
      - Discrete State-Space dynamic plant observer (8 states, 4 inputs, 2 disturbances).
      - Model Predictive Control (MPC) quadratic cost optimization with TMT metallurgical creep penalty.
      - 16-Pass Furnace Low Charge Flow Interlock (API 560 30-second low flow double-block trip).
      - Centrifugal compressor anti-surge dynamic decoupling with polytropic head observer.
      - Moving-bed catalyst lift-pot pneumatic cycling and regenerator oxychlorination coke burn rate observer.
      - 16-channel ISA-18.2 multi-tiered alarm engine with first-out trip recording and diagnostic word packing.
    ======================================================================================================
*)
"""

def get_var_input():
    return """VAR_INPUT
    (* ================================================================================================== *)
    (* 1. MASTER UNIT CONTROLS & COMMAND INTERFACE                                                        *)
    (* ================================================================================================== *)
    bEnable                             : BOOL := FALSE;    (* Master Execution Enable [TRUE: Active, FALSE: Standby/Deactivated] *)
    bReset                              : BOOL := FALSE;    (* Master Fault, Interlock and Alarm Latch Reset [Rising Edge Triggered] *)
    bEmergencyStop                      : BOOL := FALSE;    (* Emergency Shutdown Pushbutton (ESD Trip) [FALSE: Normal, TRUE: TRIP] *)
    bFeedCutInPermissive                : BOOL := FALSE;    (* Upstream Hydrotreater Naphtha Charge Ready Permissive [TRUE: Charge OK] *)
    bRegenPermissive                    : BOOL := FALSE;    (* Catalyst Regeneration Section Circulation Ready Permissive [TRUE: OK] *)
    iOperatingModeCmd                   : INT := 0;         (* Operating Mode Request:
                                                                 0: STANDBY_CIRCULATION, 1: DRYING_PURGE, 2: FURNACE_RAMP,
                                                                 3: FEED_CUT_IN, 4: OCTANE_SEEKING_MPC, 5: MAX_YIELD_OPTIMAL,
                                                                 6: CONTROLLED_PARK_IDLE, 7: COOLDOWN_N2_SWEEP *)
    rTargetRON                          : REAL := 102.0;    (* Target Research Octane Number Setpoint [98.0 .. 104.0 RON] *)
    rTargetWABT_Manual_degC             : REAL := 515.0;    (* Operator Manual WABT Setpoint Override [490.0 .. 535.0 deg C] *)
    bManualWABT_Select                  : BOOL := FALSE;    (* Manual WABT Setpoint Selection Flag [FALSE: MPC RON, TRUE: Manual] *)

    (* ================================================================================================== *)
    (* 2. NAPHTHA FEED CHARACTERISTICS & PHYSICAL PROPERTIES                                              *)
    (* ================================================================================================== *)
    rFeedFlow_m3h                       : REAL := 298.0;    (* Heavy Naphtha Charge Volumetric Flow [0.0 .. 350.0 m3/h, 45,000 BPD = 298.0] *)
    rFeedDensity_kgm3                   : REAL := 755.0;    (* Naphtha Feed Density at 15 deg C [720.0 .. 790.0 kg/m3] *)
    rFeed_N2A_VolPct                    : REAL := 54.0;     (* Feed Naphthenes + 2*Aromatics Precursor Index [35.0 .. 75.0 vol %] *)
    rFeedSulphur_ppm                    : REAL := 0.20;     (* Feed Total Sulphur Contaminant Level [0.0 .. 5.0 ppm wt, Limit < 0.5 ppm] *)
    rFeedMoisture_ppm                   : REAL := 6.5;      (* Feed Dissolved Water Content [0.0 .. 50.0 ppm wt, Limit < 10.0 ppm] *)
    rFeedNitrogen_ppm                   : REAL := 0.15;     (* Feed Basic Nitrogen Catalyst Poison [0.0 .. 2.0 ppm wt, Limit < 0.5 ppm] *)

    (* ================================================================================================== *)
    (* 3. 2oo3 TMR REACTOR BED TEMPERATURE SENSORS (BEDS 1..4 INLET & OUTLET CHANNELS)                   *)
    (* ================================================================================================== *)
    rT_Bed1_In_Ch1                      : REAL := 515.0;    (* Reactor 1 Inlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed1_In_Ch2                      : REAL := 515.2;    (* Reactor 1 Inlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed1_In_Ch3                      : REAL := 514.8;    (* Reactor 1 Inlet Temperature Sensor Channel 3 [deg C] *)
    rT_Bed1_Out_Ch1                     : REAL := 462.0;    (* Reactor 1 Outlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed1_Out_Ch2                     : REAL := 461.7;    (* Reactor 1 Outlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed1_Out_Ch3                     : REAL := 462.3;    (* Reactor 1 Outlet Temperature Sensor Channel 3 [deg C] *)

    rT_Bed2_In_Ch1                      : REAL := 518.0;    (* Reactor 2 Inlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed2_In_Ch2                      : REAL := 518.3;    (* Reactor 2 Inlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed2_In_Ch3                      : REAL := 517.8;    (* Reactor 2 Inlet Temperature Sensor Channel 3 [deg C] *)
    rT_Bed2_Out_Ch1                     : REAL := 486.0;    (* Reactor 2 Outlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed2_Out_Ch2                     : REAL := 485.8;    (* Reactor 2 Outlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed2_Out_Ch3                     : REAL := 486.4;    (* Reactor 2 Outlet Temperature Sensor Channel 3 [deg C] *)

    rT_Bed3_In_Ch1                      : REAL := 522.0;    (* Reactor 3 Inlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed3_In_Ch2                      : REAL := 522.2;    (* Reactor 3 Inlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed3_In_Ch3                      : REAL := 521.7;    (* Reactor 3 Inlet Temperature Sensor Channel 3 [deg C] *)
    rT_Bed3_Out_Ch1                     : REAL := 504.0;    (* Reactor 3 Outlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed3_Out_Ch2                     : REAL := 503.6;    (* Reactor 3 Outlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed3_Out_Ch3                     : REAL := 504.2;    (* Reactor 3 Outlet Temperature Sensor Channel 3 [deg C] *)

    rT_Bed4_In_Ch1                      : REAL := 525.0;    (* Reactor 4 Inlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed4_In_Ch2                      : REAL := 525.1;    (* Reactor 4 Inlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed4_In_Ch3                      : REAL := 524.8;    (* Reactor 4 Inlet Temperature Sensor Channel 3 [deg C] *)
    rT_Bed4_Out_Ch1                     : REAL := 517.0;    (* Reactor 4 Outlet Temperature Sensor Channel 1 [deg C] *)
    rT_Bed4_Out_Ch2                     : REAL := 516.8;    (* Reactor 4 Outlet Temperature Sensor Channel 2 [deg C] *)
    rT_Bed4_Out_Ch3                     : REAL := 517.3;    (* Reactor 4 Outlet Temperature Sensor Channel 3 [deg C] *)

    (* ================================================================================================== *)
    (* 4. FURNACE TUBE METAL TEMPERATURES (TMT) MAXIMUM SKIN SENSORS                                      *)
    (* ================================================================================================== *)
    rF101_MaxTMT                        : REAL := 580.0;    (* F-101 Charge Heater Maximum Radiant Tube Metal Temp [deg C] *)
    rF102_MaxTMT                        : REAL := 582.0;    (* F-102 Interheater 1 Maximum Radiant Tube Metal Temp [deg C] *)
    rF103_MaxTMT                        : REAL := 586.0;    (* F-103 Interheater 2 Maximum Radiant Tube Metal Temp [deg C] *)
    rF104_MaxTMT                        : REAL := 588.0;    (* F-104 Interheater 3 Maximum Radiant Tube Metal Temp [deg C] *)

    (* ================================================================================================== *)
    (* 5. FURNACE PASS FLOW SENSORS (4 PASSES PER FURNACE, API 560 INTERLOCK MONITORING)                  *)
    (* ================================================================================================== *)
    rF101_PassFlow_1                    : REAL := 74.5;     (* F-101 Charge Heater Pass 1 Hydrocarbon Flow [m3/h] *)
    rF101_PassFlow_2                    : REAL := 75.0;     (* F-101 Charge Heater Pass 2 Hydrocarbon Flow [m3/h] *)
    rF101_PassFlow_3                    : REAL := 74.2;     (* F-101 Charge Heater Pass 3 Hydrocarbon Flow [m3/h] *)
    rF101_PassFlow_4                    : REAL := 74.3;     (* F-101 Charge Heater Pass 4 Hydrocarbon Flow [m3/h] *)

    rF102_PassFlow_1                    : REAL := 74.8;     (* F-102 Interheater 1 Pass 1 Hydrocarbon Flow [m3/h] *)
    rF102_PassFlow_2                    : REAL := 74.1;     (* F-102 Interheater 1 Pass 2 Hydrocarbon Flow [m3/h] *)
    rF102_PassFlow_3                    : REAL := 74.9;     (* F-102 Interheater 1 Pass 3 Hydrocarbon Flow [m3/h] *)
    rF102_PassFlow_4                    : REAL := 74.2;     (* F-102 Interheater 1 Pass 4 Hydrocarbon Flow [m3/h] *)

    rF103_PassFlow_1                    : REAL := 75.1;     (* F-103 Interheater 2 Pass 1 Hydrocarbon Flow [m3/h] *)
    rF103_PassFlow_2                    : REAL := 74.6;     (* F-103 Interheater 2 Pass 2 Hydrocarbon Flow [m3/h] *)
    rF103_PassFlow_3                    : REAL := 74.0;     (* F-103 Interheater 2 Pass 3 Hydrocarbon Flow [m3/h] *)
    rF103_PassFlow_4                    : REAL := 74.3;     (* F-103 Interheater 2 Pass 4 Hydrocarbon Flow [m3/h] *)

    rF104_PassFlow_1                    : REAL := 74.4;     (* F-104 Interheater 3 Pass 1 Hydrocarbon Flow [m3/h] *)
    rF104_PassFlow_2                    : REAL := 74.8;     (* F-104 Interheater 3 Pass 2 Hydrocarbon Flow [m3/h] *)
    rF104_PassFlow_3                    : REAL := 74.5;     (* F-104 Interheater 3 Pass 3 Hydrocarbon Flow [m3/h] *)
    rF104_PassFlow_4                    : REAL := 74.3;     (* F-104 Interheater 3 Pass 4 Hydrocarbon Flow [m3/h] *)

    (* ================================================================================================== *)
    (* 6. 2oo3 TMR FURNACE FUEL GAS MANIFOLD SENSORS                                                      *)
    (* ================================================================================================== *)
    rP_FuelGas_Ch1                      : REAL := 2.45;     (* Fuel Gas Manifold Pressure Channel 1 [bar gauge] *)
    rP_FuelGas_Ch2                      : REAL := 2.46;     (* Fuel Gas Manifold Pressure Channel 2 [bar gauge] *)
    rP_FuelGas_Ch3                      : REAL := 2.44;     (* Fuel Gas Manifold Pressure Channel 3 [bar gauge] *)
    rF_FuelGas_Ch1                      : REAL := 6200.0;   (* Total Fuel Gas Header Flow Channel 1 [Nm3/h] *)
    rF_FuelGas_Ch2                      : REAL := 6195.0;   (* Total Fuel Gas Header Flow Channel 2 [Nm3/h] *)
    rF_FuelGas_Ch3                      : REAL := 6210.0;   (* Total Fuel Gas Header Flow Channel 3 [Nm3/h] *)

    (* ================================================================================================== *)
    (* 7. SEPARATOR & RECYCLE HYDROGEN COMPRESSOR SENSORS                                                  *)
    (* ================================================================================================== *)
    rSeparator_P_bar                    : REAL := 5.20;     (* High Pressure Separator Operating Pressure [bar gauge] *)
    rSeparator_T_degC                   : REAL := 38.0;     (* High Pressure Separator Operating Temp [deg C] *)
    rSuctionDrum_Level_Ch1              : REAL := 32.5;     (* Recycle Gas Suction Knock-out Drum Level Ch 1 [%] (2oo3) *)
    rSuctionDrum_Level_Ch2              : REAL := 32.8;     (* Recycle Gas Suction Knock-out Drum Level Ch 2 [%] (2oo3) *)
    rSuctionDrum_Level_Ch3              : REAL := 32.2;     (* Recycle Gas Suction Knock-out Drum Level Ch 3 [%] (2oo3) *)
    rRecycleCompressor_SuctionP_bar     : REAL := 4.80;     (* Recycle Compressor Suction Pressure [bar gauge] *)
    rRecycleCompressor_DischargeP_bar   : REAL := 12.50;    (* Recycle Compressor Discharge Pressure [bar gauge] *)
    rRecycleCompressor_Flow_Nm3h        : REAL := 95000.0;  (* Recycle Hydrogen Volumetric Flow [Nm3/h] *)
    rRecycleCompressor_Speed_RPM        : REAL := 8750.0;   (* Recycle Centrifugal Compressor Shaft Speed [RPM] *)
    rRecycleGas_H2Purity_molPct         : REAL := 85.5;     (* Online Gas Chromatograph Recycle H2 Purity [mol %] *)

    (* ================================================================================================== *)
    (* 8. REACTOR DIFFERENTIAL PRESSURES & HYDRAULIC DROP SENSORS                                         *)
    (* ================================================================================================== *)
    rDP_Reactor1                        : REAL := 450.0;    (* Reactor 1 Bed & Center-Pipe Scallop DP [mbar] *)
    rDP_Reactor2                        : REAL := 520.0;    (* Reactor 2 Bed & Center-Pipe Scallop DP [mbar] *)
    rDP_Reactor3                        : REAL := 680.0;    (* Reactor 3 Bed & Center-Pipe Scallop DP [mbar] *)
    rDP_Reactor4                        : REAL := 820.0;    (* Reactor 4 Bed & Center-Pipe Scallop DP [mbar] *)

    (* ================================================================================================== *)
    (* 9. CONTINUOUS CATALYST REGENERATION (CCR) LOOP SENSORS                                             *)
    (* ================================================================================================== *)
    rCatalyst_LiftPot_DP_mbar           : REAL := 180.0;    (* Reactor Bottom Catalyst Lift Pot Differential Pressure [mbar] *)
    bCatalyst_LiftPot_HighLevel         : BOOL := FALSE;    (* Catalyst Lift Pot Gamma-Ray High Level Detector Switch *)
    bCatalyst_SurgeHopper_LowLevel      : BOOL := FALSE;    (* Regenerator Top Surge Hopper Gamma Low Level Detector Switch *)
    rRegen_BurnZonePeakT_degC           : REAL := 498.0;    (* Catalyst Regenerator Primary Burn Zone Peak Temperature [deg C] *)
    rRegen_FlueGas_O2_molPct            : REAL := 0.85;     (* Regenerator Flue Gas Residual Oxygen Concentration [mol %] *)
    rRegen_ChlorideContent_wtPct        : REAL := 0.95;     (* Regenerated Catalyst Active Surface Chloride Content [wt %] *)
    rCatalyst_CirculationRate_kgh       : REAL := 750.0;    (* Catalyst Gravity Circulation Rate [kg/h] *)
END_VAR
"""

def get_var_output():
    return """VAR_OUTPUT
    (* ================================================================================================== *)
    (* 1. FURNACE FUEL GAS ACTUATOR DEMANDS (0.0 .. 100.0 %)                                              *)
    (* ================================================================================================== *)
    rDemand_F101_FuelGas_Pct            : REAL := 0.0;      (* F-101 Charge Heater Fuel Gas Control Valve Demand [%] *)
    rDemand_F102_FuelGas_Pct            : REAL := 0.0;      (* F-102 Interheater 1 Fuel Gas Control Valve Demand [%] *)
    rDemand_F103_FuelGas_Pct            : REAL := 0.0;      (* F-103 Interheater 2 Fuel Gas Control Valve Demand [%] *)
    rDemand_F104_FuelGas_Pct            : REAL := 0.0;      (* F-104 Interheater 3 Fuel Gas Control Valve Demand [%] *)

    (* ================================================================================================== *)
    (* 2. RECYCLE GAS COMPRESSOR & ANTI-SURGE ACTUATOR DEMANDS                                            *)
    (* ================================================================================================== *)
    rDemand_RecycleCompressor_Speed_RPM : REAL := 0.0;      (* Recycle Gas Centrifugal Compressor Speed Demand [RPM] *)
    rDemand_RecycleAntiSurge_Pct        : REAL := 0.0;      (* Anti-Surge Recycle Valve Demand [0.0: Closed, 100.0: Open %] *)

    (* ================================================================================================== *)
    (* 3. CATALYST CIRCULATION & OXYCHLORINATION DOSING COMMANDS                                          *)
    (* ================================================================================================== *)
    rDemand_ChlorideDosing_kgh          : REAL := 0.0;      (* Oxychlorination Perchloroethylene Injection Rate [kg/h] *)
    bCmd_Catalyst_LiftGas_Valve         : BOOL := FALSE;    (* Catalyst Pneumatic Lift Gas Supply Solenoid Valve *)
    bCmd_Catalyst_Equalize_Valve        : BOOL := FALSE;    (* Catalyst Lock Hopper Pressure Equalizing Solenoid Valve *)
    bCmd_Catalyst_Vent_Valve            : BOOL := FALSE;    (* Catalyst Lock Hopper Depressuring Vent Solenoid Valve *)

    (* ================================================================================================== *)
    (* 4. SAFETY & EMERGENCY INTERLOCK ACTUATION COMMANDS                                                 *)
    (* ================================================================================================== *)
    bCmd_FuelGas_EmergencyShutoff_ESD   : BOOL := FALSE;    (* Fuel Gas Double-Block and Bleed Slam-Shut ESD Valve Command *)
    bCmd_ReformerEmergencyDepressure_BDV: BOOL := FALSE;    (* Reactor Loop High-Pressure Emergency Flare Blowdown Valve *)
    bCmd_NaphthaChargeCutoff            : BOOL := FALSE;    (* Naphtha Feed Charge Emergency Isolation Valve Cutoff *)

    (* ================================================================================================== *)
    (* 5. PROCESS PERFORMANCE METRICS & MODEL PREDICTIONS                                                 *)
    (* ================================================================================================== *)
    rCalculated_WABT_degC               : REAL := 0.0;      (* Calculated Weighted Average Bed Temperature (WABT) [deg C] *)
    rPredicted_RON                      : REAL := 0.0;      (* Model-Predicted Reformate Research Octane Number *)
    rPredicted_C5Plus_Yield_wtPct       : REAL := 0.0;      (* Model-Predicted C5+ Liquid Product Mass Yield [wt %] *)
    rH2_HC_MoleRatio                    : REAL := 0.0;      (* Calculated Combined Feed Hydrogen / Hydrocarbon Mole Ratio [mol/mol] *)
    rCompressor_SurgeMargin_Pct         : REAL := 0.0;      (* Recycle Compressor Distance-to-Surge Deviation Margin [%] *)
    rCatalyst_CokeBurnRate_kgh          : REAL := 0.0;      (* Catalyst Regenerator Calculated Coke Combustion Rate [kg/h] *)
    rBed1_DeltaT_degC                   : REAL := 0.0;      (* Reactor Bed 1 Endothermic Temperature Drop [deg C] *)
    rBed2_DeltaT_degC                   : REAL := 0.0;      (* Reactor Bed 2 Endothermic Temperature Drop [deg C] *)
    rBed3_DeltaT_degC                   : REAL := 0.0;      (* Reactor Bed 3 Endothermic Temperature Drop [deg C] *)
    rBed4_DeltaT_degC                   : REAL := 0.0;      (* Reactor Bed 4 Temperature Drop / Thermal Equilibrium [deg C] *)
    rTotalReactionsDuty_MW              : REAL := 0.0;      (* Total Reactor Train Endothermic Duty Absorbance [MW] *)

    (* ================================================================================================== *)
    (* 6. UNIT STATE, DIAGNOSTICS & ISA-18.2 ALARM WORDS                                                  *)
    (* ================================================================================================== *)
    iActiveState                        : INT := 0;         (* Active Finite State Machine State Code [0 .. 10] *)
    dwAlarms_Priority1_Trips            : DWORD := 16#00000000; (* ISA-18.2 Priority 1 Emergency Trip Alarm Bitmask *)
    dwAlarms_Priority2_High             : DWORD := 16#00000000; (* ISA-18.2 Priority 2 Process Deviation Alarm Bitmask *)
    dwAlarms_Priority3_Warn             : DWORD := 16#00000000; (* ISA-18.2 Priority 3 Advisory / Maintenance Warning Bitmask *)
    dwSystemDiagnostics                 : DWORD := 16#00000000; (* Hardware, Voting & Subsystem Diagnostic Flags Bitmask *)
    bUnitTripped                        : BOOL := FALSE;    (* Master Reformer Emergency Shutdown Trip Latched Flag *)
    bUnitPermissiveReady                : BOOL := FALSE;    (* All Reformer Start-up and Cut-in Permissives Satisfied *)
    iMPC_SolverStatus                   : INT := 0;         (* MPC Optimization Solver Status (0: Optimal, 1: Constrained, -1: Error) *)
    rMPC_CurrentCost                    : REAL := 0.0;      (* MPC Quadratic Cost Objective Value J at Current Cycle *)
END_VAR
"""

def get_var():
    return """VAR
    (* ================================================================================================== *)
    (* 1. DISCRETE STATE-SPACE MATRICES & VECTORS (x[k+1] = A*x[k] + B*u[k] + E*d[k])                     *)
    (*    States x (8): [Delta_T1, Delta_T2, Delta_T3, Delta_T4, xi_Naph, xi_Paraff, Delta_RH2, Delta_TMT]*)
    (*    Inputs u (4): [Delta_F101_Fuel, Delta_F102_Fuel, Delta_F103_Fuel, Delta_F104_Fuel]             *)
    (*    Disturbances d (2): [Delta_FeedFlow, Delta_FeedN2A]                                             *)
    (*    Outputs y (4): [WABT, RON, Yield_C5Plus, TMT_Peak]                                             *)
    (* ================================================================================================== *)
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix (8x8) *)
    aB                                  : ARRAY[1..8, 1..4] OF REAL; (* Discrete Input Coupling Matrix (8x4) *)
    aC                                  : ARRAY[1..4, 1..8] OF REAL; (* Discrete Measurement Matrix (4x8) *)
    aD_matrix                           : ARRAY[1..4, 1..4] OF REAL; (* Direct Feedthrough Transmission Matrix (4x4) *)
    aE_dist                             : ARRAY[1..8, 1..2] OF REAL; (* Disturbance Coupling Matrix (8x2) *)
    aL_Kalman                           : ARRAY[1..8, 1..4] OF REAL; (* Kalman Observer Innovation Gain Matrix (8x4) *)
    aX                                  : ARRAY[1..8] OF REAL;       (* Estimated Discrete State Vector at k *)
    aX_pred                             : ARRAY[1..8] OF REAL;       (* A-Priori Predicted State Vector at k+1 *)
    aY_pred                             : ARRAY[1..4] OF REAL;       (* Model-Predicted Process Output Vector *)
    aInnov                              : ARRAY[1..4] OF REAL;       (* Innovation Residual Vector (y_meas - y_pred) *)
    aU                                  : ARRAY[1..4] OF REAL;       (* Control Input Vector (Fuel Gas Trims [Nm3/h]) *)
    aU_prev                             : ARRAY[1..4] OF REAL;       (* Control Input Vector at Previous Cycle (k-1) *)
    aDeltaU                             : ARRAY[1..4] OF REAL;       (* Control Slew Rate Vector (u[k] - u[k-1]) *)
    aDist                               : ARRAY[1..2] OF REAL;       (* Process Disturbance Vector [Delta_F, Delta_N2A] *)

    (* ================================================================================================== *)
    (* 2. MODEL PREDICTIVE CONTROL (MPC) QUADRATIC COST WEIGHTS & OPTIMIZATION ARRAYS                     *)
    (*    Cost Functional: J = sum(x - r)'*Q*(x - r) + u'*R*u + Delta_u'*S*Delta_u + (x - r)'*P*(x - r)   *)
    (* ================================================================================================== *)
    aQ                                  : ARRAY[1..8] OF REAL;       (* Diagonal State Error Deviation Penalty Vector *)
    aR                                  : ARRAY[1..4] OF REAL;       (* Diagonal Actuator Effort Penalty Vector *)
    aS                                  : ARRAY[1..4] OF REAL;       (* Diagonal Actuator Slew Rate Penalty Vector *)
    aP_term                             : ARRAY[1..8] OF REAL;       (* Diagonal Terminal State Error Penalty Vector *)
    aRef                                : ARRAY[1..8] OF REAL;       (* Target State Reference Trajectory Vector *)
    aGrad                               : ARRAY[1..4] OF REAL;       (* Gradient of Quadratic Cost Objective wrt u *)
    aHessianDiag                        : ARRAY[1..4] OF REAL;       (* Analytical Diagonal Approximation of Hessian *)
    aStep                               : ARRAY[1..4] OF REAL;       (* Projected Gradient Newton Step Vector *)
    aU_cand                             : ARRAY[1..4] OF REAL;       (* Candidate Control Input Vector During Iteration *)
    rMPC_Alpha                          : REAL := 0.285;             (* Gradient Descent Relaxation Damping Parameter *)
    rMaxSlewRate_PctPerSec              : REAL := 1.50;              (* Maximum Allowable Fuel Gas Slew Rate [%/s] *)
    rMinFuelDemand_Pct                  : REAL := 8.0;               (* Minimum Burner Flame Stability Limit [%] *)
    rMaxFuelDemand_Pct                  : REAL := 95.0;              (* Maximum Radiant Furnace Thermal Capacity [%] *)

    (* Base Operating Point Offsets for Deviation Models *)
    rWABT_Base_degC                     : REAL := 515.0;             (* Base Nominal WABT Equilibrium [deg C] *)
    rRON_Base                           : REAL := 102.0;             (* Base Nominal Reformate Octane Equilibrium *)
    rYield_Base_wtPct                   : REAL := 87.2;              (* Base Nominal C5+ Liquid Yield [wt %] *)
    rTMT_Base_degC                      : REAL := 585.0;             (* Base Nominal Tube Metal Temperature [deg C] *)
    rFeedFlow_Base_m3h                  : REAL := 298.0;             (* Base Nominal Naphtha Charge Flow [m3/h] *)
    rFeedN2A_Base_volPct                : REAL := 54.0;              (* Base Nominal Naphtha N+2A Precursor [vol %] *)

    (* ================================================================================================== *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING INTERNAL STRUCTURES                                 *)
    (* ================================================================================================== *)
    (* Bed 1 Inlet Temperature Voting *)
    rVoted_Bed1_In_degC                 : REAL := 515.0;
    bBed1_In_Ch1_Fault                  : BOOL := FALSE;
    bBed1_In_Ch2_Fault                  : BOOL := FALSE;
    bBed1_In_Ch3_Fault                  : BOOL := FALSE;
    tBed1_In_DiscTimer_12               : REAL := 0.0;
    tBed1_In_DiscTimer_23               : REAL := 0.0;
    tBed1_In_DiscTimer_31               : REAL := 0.0;

    (* Bed 1 Outlet Temperature Voting *)
    rVoted_Bed1_Out_degC                : REAL := 462.0;
    bBed1_Out_Ch1_Fault                 : BOOL := FALSE;
    bBed1_Out_Ch2_Fault                 : BOOL := FALSE;
    bBed1_Out_Ch3_Fault                 : BOOL := FALSE;
    tBed1_Out_DiscTimer_12              : REAL := 0.0;
    tBed1_Out_DiscTimer_23              : REAL := 0.0;
    tBed1_Out_DiscTimer_31              : REAL := 0.0;

    (* Bed 2 Inlet Temperature Voting *)
    rVoted_Bed2_In_degC                 : REAL := 518.0;
    bBed2_In_Ch1_Fault                  : BOOL := FALSE;
    bBed2_In_Ch2_Fault                  : BOOL := FALSE;
    bBed2_In_Ch3_Fault                  : BOOL := FALSE;
    tBed2_In_DiscTimer_12               : REAL := 0.0;
    tBed2_In_DiscTimer_23               : REAL := 0.0;
    tBed2_In_DiscTimer_31               : REAL := 0.0;

    (* Bed 2 Outlet Temperature Voting *)
    rVoted_Bed2_Out_degC                : REAL := 486.0;
    bBed2_Out_Ch1_Fault                 : BOOL := FALSE;
    bBed2_Out_Ch2_Fault                 : BOOL := FALSE;
    bBed2_Out_Ch3_Fault                 : BOOL := FALSE;
    tBed2_Out_DiscTimer_12              : REAL := 0.0;
    tBed2_Out_DiscTimer_23              : REAL := 0.0;
    tBed2_Out_DiscTimer_31              : REAL := 0.0;

    (* Bed 3 Inlet Temperature Voting *)
    rVoted_Bed3_In_degC                 : REAL := 522.0;
    bBed3_In_Ch1_Fault                  : BOOL := FALSE;
    bBed3_In_Ch2_Fault                  : BOOL := FALSE;
    bBed3_In_Ch3_Fault                  : BOOL := FALSE;
    tBed3_In_DiscTimer_12               : REAL := 0.0;
    tBed3_In_DiscTimer_23               : REAL := 0.0;
    tBed3_In_DiscTimer_31               : REAL := 0.0;

    (* Bed 3 Outlet Temperature Voting *)
    rVoted_Bed3_Out_degC                : REAL := 504.0;
    bBed3_Out_Ch1_Fault                 : BOOL := FALSE;
    bBed3_Out_Ch2_Fault                 : BOOL := FALSE;
    bBed3_Out_Ch3_Fault                 : BOOL := FALSE;
    tBed3_Out_DiscTimer_12              : REAL := 0.0;
    tBed3_Out_DiscTimer_23              : REAL := 0.0;
    tBed3_Out_DiscTimer_31              : REAL := 0.0;

    (* Bed 4 Inlet Temperature Voting *)
    rVoted_Bed4_In_degC                 : REAL := 525.0;
    bBed4_In_Ch1_Fault                  : BOOL := FALSE;
    bBed4_In_Ch2_Fault                  : BOOL := FALSE;
    bBed4_In_Ch3_Fault                  : BOOL := FALSE;
    tBed4_In_DiscTimer_12               : REAL := 0.0;
    tBed4_In_DiscTimer_23               : REAL := 0.0;
    tBed4_In_DiscTimer_31               : REAL := 0.0;

    (* Bed 4 Outlet Temperature Voting *)
    rVoted_Bed4_Out_degC                : REAL := 517.0;
    bBed4_Out_Ch1_Fault                 : BOOL := FALSE;
    bBed4_Out_Ch2_Fault                 : BOOL := FALSE;
    bBed4_Out_Ch3_Fault                 : BOOL := FALSE;
    tBed4_Out_DiscTimer_12              : REAL := 0.0;
    tBed4_Out_DiscTimer_23              : REAL := 0.0;
    tBed4_Out_DiscTimer_31              : REAL := 0.0;

    (* Fuel Gas Pressure Voting *)
    rVoted_FuelGas_P_bar                : REAL := 2.45;
    bFuelGas_P_Ch1_Fault                : BOOL := FALSE;
    bFuelGas_P_Ch2_Fault                : BOOL := FALSE;
    bFuelGas_P_Ch3_Fault                : BOOL := FALSE;
    tFuelGas_P_DiscTimer_12             : REAL := 0.0;
    tFuelGas_P_DiscTimer_23             : REAL := 0.0;
    tFuelGas_P_DiscTimer_31             : REAL := 0.0;

    (* Fuel Gas Flow Voting *)
    rVoted_FuelGas_Flow_Nm3h            : REAL := 6200.0;
    bFuelGas_F_Ch1_Fault                : BOOL := FALSE;
    bFuelGas_F_Ch2_Fault                : BOOL := FALSE;
    bFuelGas_F_Ch3_Fault                : BOOL := FALSE;
    tFuelGas_F_DiscTimer_12             : REAL := 0.0;
    tFuelGas_F_DiscTimer_23             : REAL := 0.0;
    tFuelGas_F_DiscTimer_31             : REAL := 0.0;

    (* Suction Drum Liquid Level Voting *)
    rVoted_SuctionDrum_Level_Pct        : REAL := 32.5;
    bSuctionDrum_L_Ch1_Fault            : BOOL := FALSE;
    bSuctionDrum_L_Ch2_Fault            : BOOL := FALSE;
    bSuctionDrum_L_Ch3_Fault            : BOOL := FALSE;
    tSuctionDrum_L_DiscTimer_12         : REAL := 0.0;
    tSuctionDrum_L_DiscTimer_23         : REAL := 0.0;
    tSuctionDrum_L_DiscTimer_31         : REAL := 0.0;

    (* TMR Tuning Constants *)
    rTMR_TempDiscrepancyLimit_degC      : REAL := 6.0;               (* Max Allowable Discrepancy Between TCs [deg C] *)
    rTMR_PressDiscrepancyLimit_bar      : REAL := 0.35;              (* Max Allowable Discrepancy for Pressure [bar] *)
    rTMR_FlowDiscrepancyLimit_Nm3h      : REAL := 450.0;             (* Max Allowable Discrepancy for Flow [Nm3/h] *)
    rTMR_LevelDiscrepancyLimit_Pct      : REAL := 5.0;               (* Max Allowable Discrepancy for Drum Level [%] *)
    rTMR_DiscrepancyTripTime_s          : REAL := 4.0;               (* Discrepancy Persistent Fault Delay [s] *)

    (* ================================================================================================== *)
    (* 4. THERMODYNAMIC CONSTANTS, REACTION KINETICS & FLUID PROPERTIES                                   *)
    (* ================================================================================================== *)
    rR_GasConstant                      : REAL := 8.314462;          (* Universal Ideal Gas Constant [J / (mol * K)] *)
    rMw_Naphtha_kgkmol                  : REAL := 115.2;             (* Average Naphtha Feed Molecular Weight [kg/kmol] *)
    rMw_Hydrogen_kgkmol                 : REAL := 2.01588;           (* Molecular Weight of Hydrogen H2 [kg/kmol] *)
    rCp_NaphthaVapor_kJkgK              : REAL := 2.450;             (* Naphtha Vapor Mean Specific Heat [kJ / (kg * K)] *)
    rCp_RecycleGas_kJkgK                : REAL := 13.850;            (* Recycle Gas (85 mol% H2) Specific Heat [kJ/(kg*K)] *)
    rDeltaH_NaphDehydrog_kJmol          : REAL := 220.0;             (* Naphthene Dehydrogenation Endotherm [kJ/mol] *)
    rDeltaH_ParaffDehydrocycl_kJmol     : REAL := 255.0;             (* Paraffin Dehydrocyclization Endotherm [kJ/mol] *)
    rDeltaH_Hydrocracking_kJmol         : REAL := -55.0;             (* Paraffin Hydrocracking Exotherm [kJ/mol] *)
    rEa_Naph_Jmol                       : REAL := 125000.0;          (* Dehydrogenation Activation Energy [J/mol] *)
    rEa_Paraff_Jmol                     : REAL := 172000.0;          (* Dehydrocyclization Activation Energy [J/mol] *)
    rEa_Crack_Jmol                      : REAL := 215000.0;          (* Hydrocracking Activation Energy [J/mol] *)
    rk0_Naph                            : REAL := 4.80E7;            (* Dehydrogenation Frequency Factor [1/s] *)
    rk0_Paraff                          : REAL := 1.15E9;            (* Dehydrocyclization Frequency Factor [1/s] *)
    rk0_Crack                           : REAL := 8.50E10;           (* Hydrocracking Frequency Factor [1/s] *)
    rTotalCatalystVolume_m3             : REAL := 185.0;             (* Total Platinum-Tin Catalyst Inventory [m3] *)

    (* Catalyst Distribution Weighting Fractions across Beds 1..4 *)
    rw1_Bed                             : REAL := 0.10;              (* Bed 1 Catalyst Mass Weighting Fraction *)
    rw2_Bed                             : REAL := 0.15;              (* Bed 2 Catalyst Mass Weighting Fraction *)
    rw3_Bed                             : REAL := 0.30;              (* Bed 3 Catalyst Mass Weighting Fraction *)
    rw4_Bed                             : REAL := 0.45;              (* Bed 4 Catalyst Mass Weighting Fraction *)

    (* ================================================================================================== *)
    (* 5. CENTRIFUGAL COMPRESSOR ANTI-SURGE CONTROLLER INTERNAL VARIABLES                                 *)
    (* ================================================================================================== *)
    rAntiSurge_Kp                       : REAL := 3.20;              (* Anti-Surge Proportional Controller Gain *)
    rAntiSurge_Ki                       : REAL := 0.75;              (* Anti-Surge Integral Reset Time Constant [1/s] *)
    rAntiSurge_Kd                       : REAL := 0.40;              (* Anti-Surge Derivative Rate Gain [s] *)
    rAntiSurge_IntegralAccum            : REAL := 0.0;               (* Anti-Surge Controller Integral Accumulator *)
    rAntiSurge_PrevError                : REAL := 0.0;               (* Anti-Surge Controller Previous Cycle Error *)
    rAntiSurge_TargetMargin_Pct         : REAL := 15.0;              (* Safety Surge Control Line Setpoint Margin [%] *)
    rCompressor_PolytropicHead_m        : REAL := 0.0;               (* Real-time Polytropic Compression Head [m] *)
    rCompressor_VolFlow_m3h             : REAL := 0.0;               (* Suction Volumetric Gas Flow Rate [m3/h] *)

    (* ================================================================================================== *)
    (* 6. MOVING-BED CATALYST CIRCULATION LIFT-POT FSM VARIABLES                                          *)
    (* ================================================================================================== *)
    iLiftPotState                       : INT := 0;                  (* Lift Pot FSM State:
                                                                          0: IDLE_STANDBY, 1: GRAVITY_FILL, 2: SEAL_VALVES,
                                                                          3: PRESSURIZE_GAS, 4: LIFT_IMPULSE, 5: BLOWDOWN_VENT,
                                                                          6: CYCLE_COMPLETE *)
    tLiftPotTimer_s                     : REAL := 0.0;               (* Lift Pot Sequence Internal Elapsed Timer [s] *)
    iLiftCycleCount                     : DINT := 0;                 (* Total Number of Catalyst Lift Pulses Executed *)
    bLiftPotTransferFault               : BOOL := FALSE;             (* Lift Pot Differential Pressure / Plug Fault *)

    (* ================================================================================================== *)
    (* 7. REGENERATOR OXYCHLORINATION DOSING CONTROLLER VARIABLES                                         *)
    (* ================================================================================================== *)
    rChloride_Kp                        : REAL := 0.85;              (* Chloride Concentration Controller Proportional Gain *)
    rChloride_Ki                        : REAL := 0.05;              (* Chloride Concentration Controller Integral Gain [1/s] *)
    rChloride_IntegralAccum             : REAL := 0.0;               (* Chloride Controller Integral Accumulator *)
    rChloride_Target_wtPct              : REAL := 0.95;              (* Target Catalyst Surface Chloride Concentration [wt %] *)
    rBurnZone_MaxAllowableT_degC        : REAL := 540.0;             (* Maximum Sintering Threshold Burn Temperature [deg C] *)

    (* ================================================================================================== *)
    (* 8. FURNACE PASS FLOW LOW PROTECTION ACCUMULATOR TIMERS (API 560 COMPLIANCE)                        *)
    (* ================================================================================================== *)
    tF101_PassLowTimer_s                : REAL := 0.0;               (* F-101 Low Flow Persistent Countdown Timer [s] *)
    tF102_PassLowTimer_s                : REAL := 0.0;               (* F-102 Low Flow Persistent Countdown Timer [s] *)
    tF103_PassLowTimer_s                : REAL := 0.0;               (* F-103 Low Flow Persistent Countdown Timer [s] *)
    tF104_PassLowTimer_s                : REAL := 0.0;               (* F-104 Low Flow Persistent Countdown Timer [s] *)
    rPassFlow_LowWarningThreshold_m3h   : REAL := 18.0;              (* Pass Flow Low Warning Limit [m3/h] *)
    rPassFlow_LowTripThreshold_m3h      : REAL := 15.0;              (* Pass Flow Low Trip Threshold [m3/h] *)
    rPassFlow_LowInstantTrip_m3h        : REAL := 8.0;               (* Pass Flow Instantaneous No-Delay Trip [m3/h] *)

    (* ================================================================================================== *)
    (* 9. ISA-18.2 ALARM ENGINE REGISTERS & FIRST-OUT CAPTURE                                             *)
    (* ================================================================================================== *)
    (* Trip Alarm Latches & Delay Timers *)
    bAlmActive_TMT_HH                   : BOOL := FALSE;
    bAlmActive_PassFlow_LL              : BOOL := FALSE;
    bAlmActive_SuctionDrum_HH           : BOOL := FALSE;
    bAlmActive_FuelGasP_LL              : BOOL := FALSE;
    bAlmActive_ReactorDP_HH             : BOOL := FALSE;
    bAlmActive_RegenTemp_HH             : BOOL := FALSE;
    bAlmActive_ESD_PB                   : BOOL := FALSE;

    (* Priority 2 Deviation Alarm Latches *)
    bAlmActive_H2Purity_LL              : BOOL := FALSE;
    bAlmActive_H2HC_Ratio_L             : BOOL := FALSE;
    bAlmActive_SurgeMargin_L            : BOOL := FALSE;
    bAlmActive_TMT_H                    : BOOL := FALSE;
    bAlmActive_FuelGasP_L               : BOOL := FALSE;

    (* Priority 3 Maintenance Warning Latches *)
    bAlmActive_Chloride_L               : BOOL := FALSE;
    bAlmActive_LiftDP_H                 : BOOL := FALSE;
    bAlmActive_FeedMoisture_H           : BOOL := FALSE;
    bAlmActive_FeedSulphur_H            : BOOL := FALSE;

    (* Alarm Delay Verification Timers *)
    tAlmDelay_TMT_HH                    : REAL := 0.0;
    tAlmDelay_PassFlow_LL               : REAL := 0.0;
    tAlmDelay_SuctionDrum_HH            : REAL := 0.0;
    tAlmDelay_FuelGasP_LL               : REAL := 0.0;
    tAlmDelay_ReactorDP_HH              : REAL := 0.0;
    tAlmDelay_RegenTemp_HH              : REAL := 0.0;
    tAlmDelay_H2Purity_LL               : REAL := 0.0;
    tAlmDelay_SurgeMargin_L             : REAL := 0.0;

    iFirstOutAlarmCode                  : INT := 0;                  (* First-Out Tripping Cause Code (1..7) *)

    (* ================================================================================================== *)
    (* 10. MULTI-STAGE REFORMER FINITE STATE MACHINE (FSM) VARIABLES                                      *)
    (* ================================================================================================== *)
    iState                              : INT := 0;                  (* Current Unit Operating State Code *)
    tStateTimer_s                       : REAL := 0.0;               (* Elapsed Dwell Time in Current State [s] *)
    tHeatupRampTimer_s                  : REAL := 0.0;               (* Furnace Warm-Up Controlled Ramp Timer [s] *)
    tQuenchSweepTimer_s                 : REAL := 0.0;               (* Emergency Feed Trip H2 Sweep Timer [s] *)
    rActiveTargetWABT_degC              : REAL := 515.0;             (* Dynamic Working WABT Target for MPC [deg C] *)

    (* Loop Counters & Scratch Variables *)
    i                                   : INT := 0;
    j                                   : INT := 0;
    k                                   : INT := 0;
    m                                   : INT := 0;
    p                                   : INT := 0;
    iter                                : INT := 0;
    rTempCalc                           : REAL := 0.0;
    rTempDiff                           : REAL := 0.0;
    bInitialized                        : BOOL := FALSE;
END_VAR
"""
