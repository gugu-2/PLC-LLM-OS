# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_var_decl.py
Declares internal variables (VAR ... END_VAR) for FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization.
"""

def generate_var_decl():
    return '''VAR
    (* ==================== SYSTEM EXECUTION & TIME CONSTANTS ==================== *)
    rTs_s                           : REAL := 0.100;    (* Discrete PLC Control Loop Execution Interval [s] *)
    bInitMatricesComplete           : BOOL := FALSE;    (* Cold-Start Matrix One-Shot Initialization Done Flag [-] *)
    rKelvinOffset                   : REAL := 273.150;  (* Thermodynamic Absolute Temperature Offset [deg C -> K] *)

    (* ==================== DISCRETE STATE-SPACE MATRICES (6x6 SYSTEM) ==================== *)
    (* States x = [T_retort, T_core, P_retort, P_internal, F0_accum, C0_accum] *)
    (* Inputs u = [u_steam, u_air, u_vent, u_cooling, u_drum_speed] *)
    rA                              : ARRAY[1..6, 1..6] OF REAL; (* State Transition Dynamics Matrix A (6x6) [-] *)
    rB                              : ARRAY[1..6, 1..5] OF REAL; (* Control Input Coupling Matrix B (6x5) [-] *)
    rC                              : ARRAY[1..6, 1..6] OF REAL; (* State-to-Output Observation Matrix C (6x6) [-] *)
    rD                              : ARRAY[1..6, 1..5] OF REAL; (* Direct Feedthrough Transmission Matrix D (6x5) [-] *)

    rX_State                        : ARRAY[1..6] OF REAL; (* Cyber-Physical Internal State Vector x[k] *)
    rX_StateNext                    : ARRAY[1..6] OF REAL; (* Forward Propagated State Vector x[k+1] *)
    rX_Reference                    : ARRAY[1..6] OF REAL; (* Receding Horizon State Reference Target Vector x_ref *)
    rY_Output                       : ARRAY[1..6] OF REAL; (* System Physical Output Estimation Vector y[k] *)
    rU_Control                      : ARRAY[1..5] OF REAL; (* Current Optimal Control Actuator Vector u[k] *)
    rU_ControlPrev                  : ARRAY[1..5] OF REAL; (* Previous Execution Cycle Actuator Vector u[k-1] *)

    (* ==================== MODEL PREDICTIVE CONTROL (MPC) MATRICES & ARRAYS ==================== *)
    rQ_Weights                      : ARRAY[1..6] OF REAL; (* State Tracking Error Quadratic Penalty Diagonal Q [-] *)
    rR_Weights                      : ARRAY[1..5] OF REAL; (* Actuator Effort Quadratic Penalty Diagonal R [-] *)
    rS_Weights                      : ARRAY[1..5] OF REAL; (* Actuator Rate of Change (Slew) Penalty Diagonal S [-] *)
    rP_TerminalWeights              : ARRAY[1..6] OF REAL; (* Terminal Horizon State Error Penalty Diagonal P [-] *)

    rMPC_Umin                       : ARRAY[1..5] OF REAL; (* Actuator Lower Saturation Hard Boundaries [%, RPM] *)
    rMPC_Umax                       : ARRAY[1..5] OF REAL; (* Actuator Upper Saturation Hard Boundaries [%, RPM] *)
    rMPC_DeltaUmax                  : ARRAY[1..5] OF REAL; (* Actuator Maximum Slew Velocity Limits [units/s] *)
    rMPC_AlphaStep                  : REAL := 0.0125;   (* Projected Gradient Descent Optimization Step Size alpha [-] *)

    rMPC_PredStates                 : ARRAY[1..5, 1..6] OF REAL; (* Predicted Horizon States x[k+h] (N=5, states=6) *)
    rMPC_CandInputs                 : ARRAY[1..5, 1..5] OF REAL; (* Optimized Candidate Actuators u[k+h] (N=5, acts=5) *)
    rMPC_Gradients                  : ARRAY[1..5, 1..5] OF REAL; (* Unrolled Cost Function Jacobians dJ/du[k+h, m] *)

    (* ==================== 2oo3 TMR SENSOR VOTING SUB-SYSTEM ==================== *)
    (* Channel 1: Retort Chamber RTD Temperature Sensors (deg C) *)
    rTMR_TempRaw                    : ARRAY[1..3] OF REAL; (* Raw RTD Temperature Feedback Array [deg C] *)
    rTMR_TempSorted                 : ARRAY[1..3] OF REAL; (* Median Ranked Temperature Elements [deg C] *)
    bTMR_TempChFault                : ARRAY[1..3] OF BOOL; (* RTD Sensor Individual Hardware Fault Flags [-] *)
    rTMR_TempDiscrepTimer           : ARRAY[1..3] OF REAL; (* RTD Deviation Debounce Accumulator Timers [s] *)
    rVoted_Temp_degC                : REAL;             (* Triple Modular Redundancy Voted Retort Chamber Temp [deg C] *)
    iTMR_TempMode                   : INT := 3;         (* Degradation Mode: 3=2oo3, 2=1oo2, 1=1oo1, 0=Failsafe [-] *)

    (* Channel 2: Retort Shell Piezoresistive Pressure Sensors (bar) *)
    rTMR_PressRaw                   : ARRAY[1..3] OF REAL; (* Raw Pressure Sensor Array [bar] *)
    rTMR_PressSorted                : ARRAY[1..3] OF REAL; (* Median Ranked Pressure Elements [bar] *)
    bTMR_PressChFault               : ARRAY[1..3] OF BOOL; (* Pressure Sensor Individual Fault Flags [-] *)
    rTMR_PressDiscrepTimer          : ARRAY[1..3] OF REAL; (* Pressure Deviation Debounce Accumulator Timers [s] *)
    rVoted_Press_bar                : REAL;             (* Triple Modular Redundancy Voted Chamber Pressure [bar] *)
    iTMR_PressMode                  : INT := 3;         (* Degradation Mode: 3=2oo3, 2=1oo2, 1=1oo1, 0=Failsafe [-] *)

    (* Channel 3: Sump Condensate Level DP Sensors (mm) *)
    rTMR_LevelRaw                   : ARRAY[1..3] OF REAL; (* Raw Sump Condensate Level Transducer Array [mm] *)
    rTMR_LevelSorted                : ARRAY[1..3] OF REAL; (* Median Ranked Level Elements [mm] *)
    bTMR_LevelChFault               : ARRAY[1..3] OF BOOL; (* Level Sensor Hardware Fault Flags [-] *)
    rTMR_LevelDiscrepTimer          : ARRAY[1..3] OF REAL; (* Level Discrepancy Debounce Timers [s] *)
    rVoted_Level_mm                 : REAL;             (* Triple Modular Redundancy Voted Sump Water Level [mm] *)
    iTMR_LevelMode                  : INT := 3;         (* Degradation Mode: 3=2oo3, 2=1oo2, 1=1oo1, 0=Failsafe [-] *)

    (* Channel 4: Wireless Pouch/Can Internal Pressure Telemetry Transponders (bar) *)
    rTMR_PouchRaw                   : ARRAY[1..3] OF REAL; (* Raw Telemetry Capsule Pressure Feedback [bar] *)
    rTMR_PouchSorted                : ARRAY[1..3] OF REAL; (* Median Ranked Telemetry Pressure Elements [bar] *)
    bTMR_PouchChFault               : ARRAY[1..3] OF BOOL; (* Telemetry Transponder Fault / Signal Loss Flags [-] *)
    rTMR_PouchDiscrepTimer          : ARRAY[1..3] OF REAL; (* Telemetry Deviation Debounce Timers [s] *)
    rVoted_PouchPress_bar           : REAL;             (* Voted In-Can / In-Pouch Internal Pressure [bar] *)
    iTMR_PouchMode                  : INT := 3;         (* Degradation Mode: 3=2oo3, 2=1oo2, 1=1oo1, 0=Failsafe [-] *)

    (* TMR Discrepancy & Voting Threshold Constants *)
    cTMR_TempMaxDev_degC            : REAL := 1.500;    (* Maximum Allowable Discrepancy Between RTD Sensors [deg C] *)
    cTMR_PressMaxDev_bar            : REAL := 0.150;    (* Maximum Allowable Discrepancy Between Shell PTs [bar] *)
    cTMR_LevelMaxDev_mm             : REAL := 35.000;   (* Maximum Allowable Discrepancy Between Level Transmitters [mm] *)
    cTMR_PouchMaxDev_bar            : REAL := 0.200;    (* Maximum Allowable Discrepancy Between Telemetry Tags [bar] *)
    cTMR_DiscrepTimeout_s           : REAL := 2.500;    (* Debounce Persistence Duration to Trip Channel Fault [s] *)

    (* ==================== CYBER-PHYSICAL THERMODYNAMICS & INACTIVATION KINETICS ==================== *)
    rAntoine_Pv_sat_bar             : REAL;             (* Retort Pure Saturated Water Vapor Pressure [bar] *)
    rDalton_Pair_bar                : REAL;             (* Retort Chamber Partial Air Overpressure Component [bar] *)
    rAntoine_Pcan_sat_bar           : REAL;             (* Container Cold-Spot Product Aqueous Vapor Pressure [bar] *)
    rDalton_Pcan_air_bar            : REAL;             (* Container Headspace Trapped Air Thermal Expansion Pressure [bar] *)
    rTotalEstimatedPcan_bar         : REAL;             (* Net Calculated Container Internal Pressure [bar] *)
    rContainerDeltaP_bar            : REAL;             (* Wall Net Stress Differential DeltaP = Pcan - Pretort [bar] *)

    (* Clostridium botulinum Bigelow Lethality Kinetics Constants *)
    cBigelow_Tref_degC              : REAL := 121.110;  (* Standard Reference Thermal Inactivation Temperature [deg C] *)
    cBigelow_z_degC                 : REAL := 10.000;   (* Thermal Inactivation Sensitivity z-Value for Clostridium [deg C] *)
    rInstantaneousLethalityRate_L   : REAL;             (* Instantaneous Inactivation Rate L = 10^((Tcore - 121.11)/z) [min/min] *)
    rIntegratedF0_min               : REAL := 0.000;    (* Integrated Microbial Lethality F0 Value [min] *)

    (* Nutrient & Quality Degradation Cook Value C0 Kinetics Constants *)
    cCook_Tref_degC                 : REAL := 100.000;  (* Standard Quality Degradation Reference Temperature [deg C] *)
    cCook_z_degC                    : REAL := 33.100;   (* Thermal Degradation Sensitivity z-Value for Thiamine/Texture [deg C] *)
    rInstantaneousCookRate_C        : REAL;             (* Instantaneous Cook Value Rate L_c = 10^((Tcore - 100)/33.1) [min/min] *)
    rIntegratedC0_min               : REAL := 0.000;    (* Integrated Cook Degradation C0 Value [min] *)

    (* Continuous Rotary Drum Kinematics & Agitation Mechanics *)
    cDrumLength_m                   : REAL := 12.500;   (* Active Axial Sterilization Length of Continuous Rotary Drum [m] *)
    cHelixPitch_m                   : REAL := 0.085;    (* Rotor Spiral Helix Axial Advance Pitch Per Revolution [m/rev] *)
    cSlotsPerRevolution             : REAL := 48.000;   (* Internal Drum Peripheral Pouch / Can Carrier Pocket Capacity [-] *)
    rCalculatedDwellTime_min        : REAL;             (* Calculated Container Residence Dwell Exposure Duration [min] *)
    rEstimatedThroughput_cpm        : REAL;             (* Real-Time Finished Container Rate Throughput [cans/min] *)

    (* Cooling Water Heat Exchange Cascade Variables *)
    rCoolingThermalPower_kW         : REAL;             (* Recirculated Cooling Water Thermal Power Extraction Rate [kW] *)
    cWaterSpecificHeat_kJkgK        : REAL := 4.184;    (* Isobaric Specific Heat Capacity of Sterile Cooling Water [kJ/kg.K] *)

    (* ==================== DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) ==================== *)
    iFSM_CurrentState               : INT := 0;         (* Active Operational Sequence State Index (0..13) [-] *)
    iFSM_PreviousState              : INT := -1;        (* State Memory for One-Shot Transition Edge Strobe [-] *)
    bFSM_FirstScanInState           : BOOL := TRUE;     (* Strobe Bit Set True on First Scan of Entering State [-] *)
    rFSM_StateTimer_s               : REAL := 0.0;      (* Elapsed Dwell Timer in Current Operational Stage [s] *)
    rFSM_TotalCycleTimer_s          : REAL := 0.0;      (* Cumulative Batch / Production Run Total Operating Clock [s] *)
    rFSM_SterilizationHoldTimer_s   : REAL := 0.0;      (* Elapsed Exposure Timer at Scheduled Cook Temperature [s] *)
    bTargetF0Reached                : BOOL := FALSE;    (* Flag Latched True When Cumulative F0 Exceeds Target [-] *)
    bProcessDeviationActive         : BOOL := FALSE;    (* FDA 21 CFR Part 113 Temperature Process Deviation Latched [-] *)
    rDeviationCompTimer_s           : REAL := 0.0;      (* Additional Dynamic Inactivation Compensating Dwell Time [s] *)

    (* FSM State Index Constants *)
    cSTATE_IDLE                                             : INT := 0;
    cSTATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK     : INT := 1;
    cSTATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE             : INT := 2;
    cSTATE_COME_UP_HEATING_RAMP_TO_121C                    : INT := 3;
    cSTATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK         : INT := 4;
    cSTATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM       : INT := 5;
    cSTATE_TARGET_F0_REACHED_HEATING_CUTOFF                : INT := 6;
    cSTATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION    : INT := 7;
    cSTATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE         : INT := 8;
    cSTATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C               : INT := 9;
    cSTATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN           : INT := 10;
    cSTATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH                : INT := 11;
    cSTATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN        : INT := 12;
    cSTATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP  : INT := 13;

    (* ==================== ISA-18.2 ALARMS, DEADBANDS & STATUS WORDS ==================== *)
    (* Trip & Warning Limit Constants *)
    cTrip_Temp_HH_degC              : REAL := 138.000;  (* Retort Over-Temperature Safety Trip Limit [deg C] *)
    cWarn_Temp_H_degC               : REAL := 135.000;  (* Retort High Temperature Advisory Warning Limit [deg C] *)
    cWarn_Temp_L_degC               : REAL := 120.000;  (* Retort Low Temperature Thermal Warning During Cook [deg C] *)
    cTrip_Temp_LL_degC              : REAL := 116.000;  (* Retort Underprocessing Safety Trip Limit During Cook [deg C] *)
    cHyst_Temp_degC                 : REAL := 1.000;    (* Retort Temperature Alarm Clearance Deadband [deg C] *)

    cTrip_Press_HH_bar              : REAL := 4.100;    (* Retort Vessel Structural Overpressure Safety Trip [bar] *)
    cWarn_Press_H_bar               : REAL := 3.850;    (* Retort High Pressure Advisory Warning Limit [bar] *)
    cWarn_Press_L_bar               : REAL := 1.850;    (* Retort Low Pressure Advisory Warning Limit [bar] *)
    cTrip_Press_LL_bar              : REAL := 1.350;    (* Retort Severe Loss of Overpressure Trip Limit [bar] *)
    cHyst_Press_bar                 : REAL := 0.080;    (* Retort Pressure Alarm Clearance Deadband [bar] *)

    cTrip_DeltaP_HH_bar             : REAL := 0.150;    (* Container Rupture / Peaking Positive Critical Trip [bar] *)
    cWarn_DeltaP_H_bar              : REAL := 0.110;    (* Container Headspace Stress High Warning Threshold [bar] *)
    cWarn_DeltaP_L_bar              : REAL := -0.110;   (* Container External Crushing Low Warning Threshold [bar] *)
    cTrip_DeltaP_LL_bar             : REAL := -0.150;   (* Container Structural Buckling / Panelling Negative Trip [bar] *)
    cHyst_DeltaP_bar                : REAL := 0.020;    (* Differential Stress Alarm Clearance Deadband [bar] *)

    cTrip_Level_HH_mm               : REAL := 350.000;  (* Vessel Bottom Sump Flooding / Condensate Backup Trip [mm] *)
    cWarn_Level_H_mm                : REAL := 220.000;  (* Sump High Condensate Level Advisory Warning [mm] *)
    cHyst_Level_mm                  : REAL := 15.000;   (* Sump Condensate Level Alarm Clearance Deadband [mm] *)

    (* Latched Safety Alarm Bits & Persistence Timers *)
    bTripLatched_TempHH             : BOOL := FALSE;
    bTripLatched_TempLL             : BOOL := FALSE;
    bTripLatched_PressHH            : BOOL := FALSE;
    bTripLatched_PressLL            : BOOL := FALSE;
    bTripLatched_DeltaPHH           : BOOL := FALSE;
    bTripLatched_DeltaPLL           : BOOL := FALSE;
    bTripLatched_LevelHH            : BOOL := FALSE;
    bTripLatched_Underprocessed     : BOOL := FALSE;

    rAlarmTimer_TempHH              : REAL := 0.0;
    rAlarmTimer_TempLL              : REAL := 0.0;
    rAlarmTimer_PressHH             : REAL := 0.0;
    rAlarmTimer_PressLL             : REAL := 0.0;
    rAlarmTimer_DeltaPHH            : REAL := 0.0;
    rAlarmTimer_DeltaPLL            : REAL := 0.0;
    rAlarmTimer_LevelHH             : REAL := 0.0;

    (* ==================== MATHEMATICAL COMPUTATION WORKSPACE VARIABLES ==================== *)
    iIdx1                           : INT := 0;         (* Inner Vector Index Counter 1 [-] *)
    iIdx2                           : INT := 0;         (* Inner Matrix Row Counter 2 [-] *)
    iIdx3                           : INT := 0;         (* Inner Matrix Column Counter 3 [-] *)
    iIdx4                           : INT := 0;         (* Horizon / Gradient Iteration Loop Counter 4 [-] *)
    iIdx5                           : INT := 0;         (* General Scratch Counter 5 [-] *)

    rTempCalc1                      : REAL := 0.0;      (* High-Precision Floating-Point Scratch Register 1 *)
    rTempCalc2                      : REAL := 0.0;      (* High-Precision Floating-Point Scratch Register 2 *)
    rTempCalc3                      : REAL := 0.0;      (* High-Precision Floating-Point Scratch Register 3 *)
    rTempCalc4                      : REAL := 0.0;      (* High-Precision Floating-Point Scratch Register 4 *)
    rTempSum                        : REAL := 0.0;      (* Matrix Dot Product & Convolution Accumulator *)
END_VAR'''
