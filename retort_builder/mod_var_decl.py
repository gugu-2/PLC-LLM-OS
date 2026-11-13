# -*- coding: utf-8 -*-
"""
Module: retort_builder/mod_var_decl.py
Declares the comprehensive VAR block for FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo.
"""

def generate_var_decl():
    return '''VAR
    (* ==================== SYSTEM EXECUTION CONSTANTS ==================== *)
    rTs_s                           : REAL := 0.100; (* Control Scan Cycle Time Interval [s] (100 ms) *)
    rPI                             : REAL := 3.141592653589793; (* Mathematical Constant Pi [-] *)
    rGasConstant_R                  : REAL := 8.314462; (* Universal Molar Gas Constant [J/(mol*K)] *)
    rMolarMassWater                 : REAL := 0.018015; (* Molecular Weight of Water Vapor [kg/mol] *)
    rMolarMassAir                   : REAL := 0.028964; (* Molecular Weight of Atmospheric Dry Air [kg/mol] *)
    rKelvinOffset                   : REAL := 273.15; (* Celsius to Absolute Kelvin Temperature Datum [K] *)
    rRefSterilTemp_degC             : REAL := 121.11; (* C. botulinum Standard Reference Temperature T0 [deg C] *)

    (* ==================== PHYSICAL VESSEL & PRODUCT PARAMETERS ==================== *)
    rVesselVolume_m3                : REAL := 5.850; (* Retort Vessel Total Free Internal Volume [m3] *)
    rVesselInternalArea_m2          : REAL := 18.42; (* Vessel Shell Wetted Heat Transfer Surface Area [m2] *)
    rVesselMetalMass_kg             : REAL := 4250.0; (* 316L Stainless Steel Shell and Door Mass [kg] *)
    rSpecificHeatSteel_JkgK         : REAL := 500.0; (* Stainless Steel Specific Heat Capacity [J/(kg*K)] *)
    rBasketProductMass_kg           : REAL := 1850.0; (* Total Batch Mass of Canned Food Products [kg] *)
    rSpecificHeatFood_JkgK          : REAL := 3850.0; (* High-Moisture Aqueous Food Specific Heat [J/(kg*K)] *)
    rCanNominalVolume_m3            : REAL := 0.000450; (* Standard 450 mL (300x407) Can Volume [m3] *)
    rCanHeadspaceFrac               : REAL := 0.075; (* Nominal Headspace Fraction (7.5% Can Volume) [-] *)
    rCanRadius_m                    : REAL := 0.0381; (* Container Outer Cylindrical Radius (3 inches / 2) [m] *)
    rCanHalfHeight_m                : REAL := 0.0570; (* Container Half-Height (4.5 inches / 2) [m] *)
    rThermalDiffusivity_alpha       : REAL := 0.000000148; (* Product Thermal Diffusivity (alpha) [m2/s] *)
    rConvectiveHTC_W_m2K            : REAL := 1250.0; (* Vessel Steam-to-Can Overall Surface HTC [W/(m2*K)] *)

    (* ==================== DISCRETE STATE-SPACE MODEL MATRICES (8x8) ==================== *)
    (* State Vector x:
     * x[1]: Vessel Temperature Tv [deg C]
     * x[2]: Vessel Total Absolute Pressure Pv [bar]
     * x[3]: Product Cold-Spot Core Temperature Tcore [deg C]
     * x[4]: Container Internal Pressure Pcan [bar]
     * x[5]: Container Differential Pressure DeltaP = Pcan - Pv [bar]
     * x[6]: Instantaneous Microbial Lethality Rate L(Tcore) [-]
     * x[7]: Cumulative Lethality Integral F0 [min]
     * x[8]: Sump Liquid Water Level Hsump [mm]
     *)
    rA                              : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    rB                              : ARRAY[1..8, 1..5] OF REAL; (* Discrete Control Input Coupling Matrix B (8x5) *)
    rC                              : ARRAY[1..6, 1..8] OF REAL; (* Discrete Measurement Matrix C (6x8) *)
    rD                              : ARRAY[1..6, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix D (6x5) *)

    rX_State                        : ARRAY[1..8] OF REAL; (* Current State Vector x[k] *)
    rX_StatePrev                    : ARRAY[1..8] OF REAL; (* Prior Cycle State Vector x[k-1] *)
    rX_StateNext                    : ARRAY[1..8] OF REAL; (* Predicted Next State Vector x[k+1] *)
    rU_Control                      : ARRAY[1..5] OF REAL; (* Active Control Actuator Vector u[k] *)
    rU_ControlPrev                  : ARRAY[1..5] OF REAL; (* Prior Cycle Control Vector u[k-1] *)
    rY_Estimated                    : ARRAY[1..6] OF REAL; (* Estimated Measurable Output Vector y[k] *)
    rX_Reference                    : ARRAY[1..8] OF REAL; (* Target Reference State Vector x_ref *)

    (* ==================== MODEL PREDICTIVE CONTROL (MPC) & PGD OPTIMIZER ==================== *)
    rQ_Weights                      : ARRAY[1..8] OF REAL; (* State Tracking Error Quadratic Cost Penalties *)
    rR_Weights                      : ARRAY[1..5] OF REAL; (* Actuator Effort Quadratic Cost Penalties *)
    rS_Weights                      : ARRAY[1..5] OF REAL; (* Actuator Slew Rate Quadratic Cost Penalties *)
    rP_TerminalWeights              : ARRAY[1..8] OF REAL; (* Terminal Horizon State Cost Penalties *)

    rMPC_PredStates                 : ARRAY[1..5, 1..8] OF REAL; (* Predicted States Across Horizon Steps N=1..5 *)
    rMPC_CandInputs                 : ARRAY[1..5, 1..5] OF REAL; (* Candidate Actuator Inputs Over Horizon N=1..5 *)
    rMPC_Gradients                  : ARRAY[1..5, 1..5] OF REAL; (* Unrolled Cost Gradient dJ/du at Each Horizon Step *)
    rMPC_OptimizedU                 : ARRAY[1..5] OF REAL; (* Final Optimal Actuator Set for Step k *)

    rMPC_StepSize_alpha             : REAL := 0.0035; (* PGD Fixed Descent Step Size Parameter [-] *)
    rU_SlewLimit_pct_per_s          : ARRAY[1..5] OF REAL; (* Actuator Rate of Change Clamp Limits [%/s] *)
    rU_LowerBound_pct               : ARRAY[1..5] OF REAL; (* Actuator Lower Saturation Limit [0.0..100.0] *)
    rU_UpperBound_pct               : ARRAY[1..5] OF REAL; (* Actuator Upper Saturation Limit [0.0..100.0] *)

    (* Decoupling Feedforward Gains *)
    rDecouple_SteamToAirRatio       : REAL := 0.320; (* Air Trim Feedforward Compensation During Steam Injection *)
    rDecouple_CoolToAirRate         : REAL := 0.785; (* High-Speed Air Inrush Pre-charge Gain During Water Spray *)

    (* ==================== 2oo3 TMR VOTING DATA STRUCTURES ==================== *)
    (* Channel A, B, C Raw Registers *)
    rTMR_TT101_Raw                  : ARRAY[1..3] OF REAL; (* Vessel Temperature Triplicate Array [deg C] *)
    rTMR_PT201_Raw                  : ARRAY[1..3] OF REAL; (* Vessel Pressure Triplicate Array [bar] *)
    rTMR_TT301_Raw                  : ARRAY[1..3] OF REAL; (* Can Core Temperature Triplicate Array [deg C] *)
    rTMR_LT401_Raw                  : ARRAY[1..3] OF REAL; (* Sump Level Triplicate Array [mm] *)

    (* Sorted TMR Registers *)
    rTMR_TT101_Sorted               : ARRAY[1..3] OF REAL; (* Sorted Vessel Temperature Readings [deg C] *)
    rTMR_PT201_Sorted               : ARRAY[1..3] OF REAL; (* Sorted Vessel Pressure Readings [bar] *)
    rTMR_TT301_Sorted               : ARRAY[1..3] OF REAL; (* Sorted Can Core Temperature Readings [deg C] *)
    rTMR_LT401_Sorted               : ARRAY[1..3] OF REAL; (* Sorted Sump Level Readings [mm] *)

    (* Discrepancy Timers and Tolerance Thresholds *)
    rTMR_TT101_DiscrepTimer         : ARRAY[1..3] OF REAL; (* Temperature Channel Divergence Timers [s] *)
    rTMR_PT201_DiscrepTimer         : ARRAY[1..3] OF REAL; (* Pressure Channel Divergence Timers [s] *)
    rTMR_TT301_DiscrepTimer         : ARRAY[1..3] OF REAL; (* Core Temp Channel Divergence Timers [s] *)
    rTMR_LT401_DiscrepTimer         : ARRAY[1..3] OF REAL; (* Sump Level Channel Divergence Timers [s] *)

    cTMR_TT101_MaxDev_degC          : REAL := 1.20; (* Allowable Temperature Discrepancy Tolerance [deg C] *)
    cTMR_PT201_MaxDev_bar           : REAL := 0.12; (* Allowable Pressure Discrepancy Tolerance [bar] *)
    cTMR_TT301_MaxDev_degC          : REAL := 1.80; (* Allowable Core Temperature Discrepancy Tolerance [deg C] *)
    cTMR_LT401_MaxDev_mm            : REAL := 35.0; (* Allowable Sump Level Discrepancy Tolerance [mm] *)
    cTMR_DiscrepTimeout_s           : REAL := 2.50; (* Duration of Persistence Before Channel Trip [s] *)

    (* Fault Flags and Degraded Modes (3 = 2oo3 Normal, 2 = 1oo2 Degraded, 1 = 1oo1 Failsafe, 0 = Tripped) *)
    bTMR_TT101_ChFault              : ARRAY[1..3] OF BOOL; (* Temperature Channel Individual Fault Flags *)
    bTMR_PT201_ChFault              : ARRAY[1..3] OF BOOL; (* Pressure Channel Individual Fault Flags *)
    bTMR_TT301_ChFault              : ARRAY[1..3] OF BOOL; (* Core Temp Channel Individual Fault Flags *)
    bTMR_LT401_ChFault              : ARRAY[1..3] OF BOOL; (* Sump Level Channel Individual Fault Flags *)

    iTMR_TT101_Mode                 : INT := 3; (* Temperature Voting Subsystem Active Mode (3, 2, 1, 0) *)
    iTMR_PT201_Mode                 : INT := 3; (* Pressure Voting Subsystem Active Mode (3, 2, 1, 0) *)
    iTMR_TT301_Mode                 : INT := 3; (* Core Temp Voting Subsystem Active Mode (3, 2, 1, 0) *)
    iTMR_LT401_Mode                 : INT := 3; (* Sump Level Voting Subsystem Active Mode (3, 2, 1, 0) *)

    (* Reconciled Voted Values *)
    rTMR_TT101_Voted                : REAL; (* Reconciled Vessel Temperature [deg C] *)
    rTMR_PT201_Voted                : REAL; (* Reconciled Vessel Pressure [bar] *)
    rTMR_TT301_Voted                : REAL; (* Reconciled Can Core Temperature [deg C] *)
    rTMR_LT401_Voted                : REAL; (* Reconciled Sump Level [mm] *)

    (* ==================== THERMODYNAMICS & ANTOINE SATURATION ==================== *)
    rAntoine_Pv_sat_bar             : REAL; (* Saturated Water Vapor Pressure at Current Tv [bar] *)
    rAntoine_Pcan_sat_bar           : REAL; (* Saturated Water Vapor Pressure at Product Tcore [bar] *)
    rDalton_Pair_bar                : REAL; (* Retort Vessel Compressed Air Partial Overpressure [bar] *)
    rDalton_Pcan_air_bar            : REAL; (* Container Headspace Thermal Expansion Air Partial Pressure [bar] *)
    rTotalEstimatedPcan_bar         : REAL; (* Total Absolute Internal Container Pressure [bar] *)
    rStressDeltaP_bar               : REAL; (* Differential Pouch Wall Pressure: Pcan - Pvessel [bar] *)
    rSteamCondensate_kg_per_s       : REAL; (* Instantaneous Condensation Mass Rate on Shell/Cans [kg/s] *)
    rSprayCoolingEnthalpy_kW        : REAL; (* Heat Extraction Rate by Water Spray Atomization [kW] *)

    (* ==================== BALL FORMULA & FDA 21 CFR 113 ENGINE ==================== *)
    rInstantLethality               : REAL; (* Microbial Kill Rate L = 10^((Tcore - 121.11)/z) [-] *)
    rPrevLethality                  : REAL; (* Prior Scan Microbial Kill Rate L[k-1] [-] *)
    rIntegratedF0                   : REAL := 0.0; (* Accumulated Sterility Lethality Integral F0 [min] *)
    rSimpsonBuffer                  : ARRAY[1..4] OF REAL; (* Simpson 3/8 Integration Sliding History Buffer *)
    iSimpsonStep                    : INT := 1; (* Rolling Counter for Multi-Step Numerical Quadrature *)

    rBall_Ih                        : REAL; (* Ball Thermal Difference: Cook Temp minus Initial Temp [deg C] *)
    rBall_g                         : REAL; (* Difference Between Retort Temp and Can Cold Spot Temp [deg C] *)
    rBall_ScheduledCookDuration_s   : REAL := 1800.0; (* Scheduled Hold Duration from Thermal Schedule [s] *)
    rBall_CookAccumulated_s         : REAL := 0.0; (* Elapsed Time Under Qualified Sterilization Temp [s] *)
    rBall_DevCookRampDown_s         : REAL := 0.0; (* Total Duration Vessel Spent Below Cut-in During Hold [s] *)
    rBall_SuppleTimeNeeded_s        : REAL := 0.0; (* Added Compensation Dwell Calculated via Lethality Deficit [s] *)
    bBall_DeviationLatching         : BOOL := FALSE; (* Process Deviation Fault Trigger Flag *)
    bBall_CatchupActive             : BOOL := FALSE; (* Automatic Lethality Extension Mode Engaged *)

    (* ==================== FINITE STATE MACHINE (14 STAGES) ==================== *)
    (* State Enumeration:
     * 00: STATE_IDLE_STANDBY
     * 01: STATE_DOOR_LOCK_SEAL_INFLATION
     * 02: STATE_AIR_VENT_PURGE
     * 03: STATE_STEAM_COME_UP_RAMP
     * 04: STATE_TEMPERATURE_CUT_IN
     * 05: STATE_STERILIZATION_HOLD_F0
     * 06: STATE_BALL_PROCESS_DEVIATION
     * 07: STATE_PRE_COOLING_AIR_EQUALIZATION
     * 08: STATE_WATER_SPRAY_CASCADE_COOLING
     * 09: STATE_RECIRCULATION_EVAP_COOLING
     * 10: STATE_OVERPRESSURE_WATER_DRAIN
     * 11: STATE_ATMOSPHERIC_VACUUM_BREAK
     * 12: STATE_SEAL_DEFLATE_DOOR_UNLATCH
     * 13: STATE_CIP_SIP_SANITATION
     * 14: STATE_EMERGENCY_SAFETY_ABORT
     *)
    iFSM_CurrentState               : INT := 0; (* Active Stage Index *)
    iFSM_PreviousState              : INT := -1; (* Prior Scan Stage Index *)
    bFSM_FirstScanInState           : BOOL := TRUE; (* One-Shot Transition Strobe for Current Stage *)
    rFSM_StateTimer_s               : REAL := 0.0; (* Elapsed Execution Time in Active State [s] *)
    rFSM_TotalCycleTimer_s          : REAL := 0.0; (* Grand Cycle Runtime Accumulator [s] *)

    (* State Stage Preset Constants *)
    cTime_SealInflate_s             : REAL := 15.0; (* Door Gasket Pressure Stabilization Timeout [s] *)
    cTime_AirPurge_s                : REAL := 90.0; (* Vent Steam Sweeping Displace Air Phase [s] *)
    cTime_PreCoolEquil_s            : REAL := 30.0; (* Deflection Balancing Air Pre-charge Dwell [s] *)
    cTime_OverpressDrain_s          : REAL := 75.0; (* Water Evacuation with Counter-Pressure [s] *)
    cTime_VacuumBreak_s             : REAL := 25.0; (* Slow Depressurization to Atmospheric Datum [s] *)
    cTime_SealDeflate_s             : REAL := 12.0; (* Elastomer Seal Vacuum Deflate Retract [s] *)

    (* ==================== ISA-18.2 ALARMS & TRIP THRESHOLDS ==================== *)
    (* Trip Limits *)
    cTrip_Temp_HH_degC              : REAL := 138.0; (* Extreme High Vessel Temperature Safety Shutoff [deg C] *)
    cTrip_Temp_LL_degC              : REAL := 115.0; (* Unrecoverable Low Vessel Temperature During Cook [deg C] *)
    cTrip_Press_HH_bar              : REAL := 4.20;  (* Vessel Shell Structural Overpressure Trip [bar] *)
    cTrip_Press_LL_bar              : REAL := 0.05;  (* Vessel Vacuum Collapse Safety Trip [bar] *)
    cTrip_DeltaP_Burst_bar          : REAL := 0.38;  (* Critical Pouch Bursting Limit [bar] *)
    cTrip_DeltaP_Buckle_bar         : REAL := -0.42; (* Critical Pouch Panelling/Crushing Limit [bar] *)
    cTrip_Sump_HH_mm                : REAL := 480.0; (* Sump Flooding Can Submergence Hazard [mm] *)

    (* Warning Limits *)
    cWarn_Temp_H_degC               : REAL := 135.0; (* High Temperature Advisory [deg C] *)
    cWarn_Temp_L_degC               : REAL := 120.0; (* Low Cook Temperature Advisory [deg C] *)
    cWarn_Press_H_bar               : REAL := 3.80;  (* High Vessel Pressure Advisory [bar] *)
    cWarn_Press_L_bar               : REAL := 1.80;  (* Low Pressure Cook Advisory [bar] *)
    cWarn_DeltaP_H_bar              : REAL := 0.28;  (* Pouch Distension Warning [bar] *)
    cWarn_DeltaP_L_bar              : REAL := -0.30; (* Pouch Concavity Warning [bar] *)
    cWarn_Sump_H_mm                 : REAL := 350.0; (* High Sump Water Level Advisory [mm] *)
    cWarn_Sump_L_mm                 : REAL := 60.0;  (* Low Sump Water Recirculation Cavitation Warning [mm] *)

    cHyst_Temp_degC                 : REAL := 0.50;  (* Alarm Return Deadband for Temperature [deg C] *)
    cHyst_Press_bar                 : REAL := 0.05;  (* Alarm Return Deadband for Pressure [bar] *)
    cHyst_DeltaP_bar                : REAL := 0.02;  (* Alarm Return Deadband for Differential Pressure [bar] *)
    cHyst_Sump_mm                   : REAL := 10.0;  (* Alarm Return Deadband for Sump Level [mm] *)

    (* Alarm Debounce Timers *)
    rAlarmTimer_TempHH              : REAL := 0.0; (* Vessel Temp HH Timer [s] *)
    rAlarmTimer_TempH               : REAL := 0.0; (* Vessel Temp H Timer [s] *)
    rAlarmTimer_TempL               : REAL := 0.0; (* Vessel Temp L Timer [s] *)
    rAlarmTimer_TempLL              : REAL := 0.0; (* Vessel Temp LL Timer [s] *)
    rAlarmTimer_PressHH             : REAL := 0.0; (* Vessel Press HH Timer [s] *)
    rAlarmTimer_PressH              : REAL := 0.0; (* Vessel Press H Timer [s] *)
    rAlarmTimer_PressL              : REAL := 0.0; (* Vessel Press L Timer [s] *)
    rAlarmTimer_PressLL             : REAL := 0.0; (* Vessel Press LL Timer [s] *)
    rAlarmTimer_DeltaP_Burst        : REAL := 0.0; (* Pouch Burst Timer [s] *)
    rAlarmTimer_DeltaP_Buckle       : REAL := 0.0; (* Pouch Buckle Timer [s] *)
    rAlarmTimer_SumpHH              : REAL := 0.0; (* Sump Level HH Timer [s] *)
    rAlarmTimer_SealPressLow        : REAL := 0.0; (* Inflatable Seal Low Pressure Timer [s] *)
    rAlarmTimer_AgitatorStall       : REAL := 0.0; (* Agitation Basket Slip/Stall Timer [s] *)

    (* Alarm Latches *)
    bTripLatched_TempHH             : BOOL := FALSE; (* Latched High-High Temperature Trip *)
    bTripLatched_TempLL             : BOOL := FALSE; (* Latched Low-Low Temperature Trip *)
    bTripLatched_PressHH            : BOOL := FALSE; (* Latched High-High Pressure Trip *)
    bTripLatched_PressLL            : BOOL := FALSE; (* Latched Low-Low Vacuum Trip *)
    bTripLatched_PouchBurst         : BOOL := FALSE; (* Latched Pouch Burst Hazard Trip *)
    bTripLatched_PouchBuckle        : BOOL := FALSE; (* Latched Pouch Crush Hazard Trip *)
    bTripLatched_TMR_Failure        : BOOL := FALSE; (* Latched Complete Sensor TMR Loss Trip *)
    bTripLatched_DoorSealLoss       : BOOL := FALSE; (* Latched Door Gasket Pressure Drop Trip *)
    bTripLatched_EStop              : BOOL := FALSE; (* Latched Emergency Stop Active *)

    (* ==================== SCRATCH ARRAYS & WORKING REGISTERS ==================== *)
    iIdx1                           : INT := 1; (* Primary Iteration Loop Counter *)
    iIdx2                           : INT := 1; (* Secondary Iteration Loop Counter *)
    iIdx3                           : INT := 1; (* Tertiary Iteration Loop Counter *)
    iIdx4                           : INT := 1; (* Quaternary Iteration Loop Counter *)
    rTempCalc1                      : REAL := 0.0; (* General High-Precision Floating-Point Scratchpad 1 *)
    rTempCalc2                      : REAL := 0.0; (* General High-Precision Floating-Point Scratchpad 2 *)
    rTempCalc3                      : REAL := 0.0; (* General High-Precision Floating-Point Scratchpad 3 *)
    rTempCalc4                      : REAL := 0.0; (* General High-Precision Floating-Point Scratchpad 4 *)
    rTempSum                        : REAL := 0.0; (* Running Accumulator Scratchpad *)
    bInitMatricesComplete           : BOOL := FALSE; (* Cold-Start Matrix Initialization One-Shot Flag *)
    iCycleCounter                   : UDINT := 0; (* Running Scan Execution Counter *)
END_VAR
'''

if __name__ == "__main__":
    v = generate_var_decl()
    print("VAR block length:", len(v))
    print(v[:300])
