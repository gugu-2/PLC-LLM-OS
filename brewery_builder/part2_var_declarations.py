# brewery_builder/part2_var_declarations.py

def get_part2():
    return """VAR
    (* ============================================================================================== *)
    (* INTERNAL CYBER-PHYSICAL STATE CONSTANTS & BREWHOUSE GEOMETRIC PARAMETERS                        *)
    (* ============================================================================================== *)
    fPI                                 : REAL := 3.14159265359; (* Mathematical Ratio Constant Pi *)
    fLauterTunDiameter                  : REAL := 6.5;      (* Lauter Tun Internal Diameter [m] *)
    fLauterTunArea                      : REAL := 33.183;   (* Lauter Tun Slotted False Bottom Area [m2] *)
    fGrainBedNominalHeight              : REAL := 0.380;    (* Nominal Spent Grain Cake Thickness [m] *)
    fWortSpecificHeatCp                 : REAL := 3.98;     (* Hot Sweet Wort Specific Heat Capacity [kJ/(kg*K)] *)
    fWortDensityNominal                 : REAL := 1048.0;   (* Nominal Sweet Wort Specific Mass Density [kg/m3] *)
    fCalandriaSurfaceArea               : REAL := 85.0;     (* Calandria Shell-and-Tube Heat Transfer Area [m2] *)
    fCleanCalandriaHeatTransferU        : REAL := 2150.0;   (* Nominal Clean Calandria Overall U-Value [W/(m2*K)] *)
    fSteamLatentHeatHfg                 : REAL := 2133.0;   (* Saturated Steam Latent Heat of Condensation [kJ/kg] *)
    fWaterLatentHeatVap                 : REAL := 2260.0;   (* Water Vaporization Enthalpy at 100 deg C [kJ/kg] *)
    fArrheniusActivationEnergySMM       : REAL := 125600.0; (* SMM Thermal Cleavage Activation Energy Ea [J/mol] *)
    fArrheniusPreExponentialA           : REAL := 8.45E13;  (* SMM Cleavage Kinetic Frequency Factor A [1/s] *)
    fUniversalGasConstantR              : REAL := 8.314462; (* Universal Molar Gas Constant R [J/(mol*K)] *)

    (* Execution Clock, Scan Cycle Timers & Initialization Flags *)
    bInitialized                        : BOOL := FALSE;    (* Cold Start Initialization Permissive Flag *)
    bWarmRestart                        : BOOL := FALSE;    (* Warm Start Transition Latch *)
    fCycleDeltaTimeSec                  : REAL := 0.100;    (* Execution Cycle Delta Time Ts [s] *)
    udiCycleCounter                     : UDINT := 0;       (* Execution Loop Cycle Counter *)
    fMasterBatchTimeSeconds             : REAL := 0.0;      (* Cumulative Brewhouse Cycle Clock [s] *)

    (* ============================================================================================== *)
    (* PHASE 2: FIRST-PRINCIPLES 6-STATE DISCRETE STATE-SPACE MODEL & LUENBERGER OBSERVER MATRICES    *)
    (* ============================================================================================== *)
    (* States x[k]:
         x[1] = Lauter Bed Differential Pressure Delta_P [mbar]
         x[2] = Vorlauf Wort Turbidity / Suspended Solids [EBC]
         x[3] = Lauter Runoff Volumetric Flow Rate Q_runoff [hL/h]
         x[4] = Wort Kettle Calandria Boiling Temperature T_boil [deg C]
         x[5] = Wort Kettle Continuous Evaporation Rate E_rate [%/h]
         x[6] = Volatile Dimethyl Sulfide (DMS) Residual Concentration [ppb]
       Controls u[k]:
         u[1] = Wort Rake Vertical Cutting Elevation Setpoint [mm]
         u[2] = Wort Rake Rotational Speed Setpoint [RPM]
         u[3] = Lauter Runoff Control Valve Position [%]
         u[4] = Calandria Steam Supply Pressure Setpoint [bar]
         u[5] = Vorlauf Recirculation Diverter Valve Position [%] *)
    matA                                : ARRAY[1..6, 1..6] OF REAL; (* Discrete System Dynamics Matrix A (6x6) *)
    matB                                : ARRAY[1..6, 1..5] OF REAL; (* Discrete Control Input Matrix B (6x5) *)
    matC                                : ARRAY[1..6, 1..6] OF REAL; (* Discrete Measurement Output Matrix C (6x6) *)
    matD                                : ARRAY[1..6, 1..5] OF REAL; (* Discrete Direct Feedthrough Matrix D (6x5) *)
    matL                                : ARRAY[1..6, 1..6] OF REAL; (* Luenberger Observer Innovation Gain L (6x6) *)

    vecX_hat                            : ARRAY[1..6] OF REAL; (* Cyber-Physical Observer Estimated States x_hat[k] *)
    vecX_hat_prev                       : ARRAY[1..6] OF REAL; (* Previous Step Estimated States x_hat[k-1] *)
    vecX_hat_next                       : ARRAY[1..6] OF REAL; (* Propagated Next Step Estimated States x_hat[k+1] *)
    vecY_meas                           : ARRAY[1..6] OF REAL; (* Synthesized Voted Process Measurements y_meas[k] *)
    vecY_est                            : ARRAY[1..6] OF REAL; (* Observer Estimated Process Measurements y_est[k] *)
    vecY_innov                          : ARRAY[1..6] OF REAL; (* Observer Innovation Residuals y_meas - y_est *)
    vecU_active                         : ARRAY[1..5] OF REAL; (* Active Control Input Vector Applied to Plant *)
    vecU_active_prev                    : ARRAY[1..5] OF REAL; (* Previous Execution Cycle Control Input Vector *)

    (* ============================================================================================== *)
    (* PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD)    *)
    (* ============================================================================================== *)
    (* Horizons & Optimization Iteration Parameters *)
    iMPC_HorizonN                       : INT := 5;         (* Prediction Horizon Length N = 5 Steps *)
    iMPC_MaxIter                        : INT := 10;        (* Unrolled Projected Gradient Descent Iterations *)
    fMPC_StepSizeAlpha                  : REAL := 0.0085;   (* Gradient Descent Step Length Factor alpha *)

    (* Cost Function Quadratic Weighting Matrices *)
    diagQ_StateCost                     : ARRAY[1..6] OF REAL; (* State Tracking Error Weighting Matrix Q *)
    diagR_ControlCost                   : ARRAY[1..5] OF REAL; (* Actuator Effort Penalty Matrix R *)
    diagR_SlewCost                      : ARRAY[1..5] OF REAL; (* Actuator Rate-of-Change Slew Penalty Matrix R_slew *)
    diagP_TerminalCost                  : ARRAY[1..6] OF REAL; (* Terminal Horizon State Penalty Matrix P *)

    (* Trajectory Rollout Arrays (Steps 0 to 5 for States, 0 to 4 for Controls) *)
    arrX_Trajectory                     : ARRAY[0..5, 1..6] OF REAL; (* Predicted State Trajectory across Horizon *)
    arrU_Trajectory                     : ARRAY[0..4, 1..5] OF REAL; (* Control Actuation Profile across Horizon *)
    arrU_Trajectory_Best                : ARRAY[0..4, 1..5] OF REAL; (* Optimal Bounded Control Trajectory *)
    arrLambda_Costate                   : ARRAY[0..5, 1..6] OF REAL; (* Adjoint Costate Backpropagation Vectors *)
    arrGrad_J                           : ARRAY[0..4, 1..5] OF REAL; (* Cost Function Gradient Vectors dJ/du *)

    (* MPC Setpoint Targets & Actuator Physical Bounds *)
    vecX_Setpoint                       : ARRAY[1..6] OF REAL; (* Target State Tracking Reference Vector *)
    vecU_Target                         : ARRAY[1..5] OF REAL; (* Nominal Steady-State Actuator Target *)
    vecU_MinBox                         : ARRAY[1..5] OF REAL; (* Hard Lower Bound Physical Actuator Saturation *)
    vecU_MaxBox                         : ARRAY[1..5] OF REAL; (* Hard Upper Bound Physical Actuator Saturation *)
    vecU_SlewLimit                      : ARRAY[1..5] OF REAL; (* Maximum Allowable Slew Rate per Scan Cycle [units/scan] *)

    (* Internal MPC Temporary Loop Variables *)
    fCost_J_Current                     : REAL := 0.0;      (* Evaluated Total Quadratic MPC Cost *)
    fCost_J_Best                        : REAL := 1.0E9;    (* Minimum Discovered Cost along Iterations *)
    fTempStateError                     : REAL := 0.0;      (* Scalar Error Temp for Matrix Quadratic Forms *)
    fTempControlError                   : REAL := 0.0;      (* Scalar Actuator Error Temp *)
    fTempDeltaControl                   : REAL := 0.0;      (* Scalar Slew Rate Error Temp *)
    fCandidateU                         : REAL := 0.0;      (* Intermediate Projected Candidate Actuator Value *)

    (* ============================================================================================== *)
    (* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING STRUCTURES                         *)
    (* ============================================================================================== *)
    (* Channel 1: Lauter Tun Grain Bed Differential Pressure Transmitters [mbar] *)
    fCh1_S1_Val                         : REAL := 0.0;
    fCh1_S2_Val                         : REAL := 0.0;
    fCh1_S3_Val                         : REAL := 0.0;
    bCh1_S1_Valid                       : BOOL := TRUE;
    bCh1_S2_Valid                       : BOOL := TRUE;
    bCh1_S3_Valid                       : BOOL := TRUE;
    bCh1_Disc_12                        : BOOL := FALSE;
    bCh1_Disc_23                        : BOOL := FALSE;
    bCh1_Disc_13                        : BOOL := FALSE;
    fCh1_DiscTimer_12                   : REAL := 0.0;
    fCh1_DiscTimer_23                   : REAL := 0.0;
    fCh1_DiscTimer_13                   : REAL := 0.0;
    bCh1_S1_FaultLatched                : BOOL := FALSE;
    bCh1_S2_FaultLatched                : BOOL := FALSE;
    bCh1_S3_FaultLatched                : BOOL := FALSE;
    iCh1_HealthySensors                 : INT := 3;
    fCh1_VotedVal                       : REAL := 0.0;
    fCh1_LastGoodVal                    : REAL := 0.0;
    fCh1_TolDelta                       : REAL := 4.5;      (* Discrepancy Tolerance Delta [mbar] *)
    fCh1_TripTimerThresh                : REAL := 0.450;    (* Discrepancy Latching Filter Time [s] *)

    (* Channel 2: Vorlauf Optical Wort Turbidity Transmitters [EBC] *)
    fCh2_S1_Val                         : REAL := 0.0;
    fCh2_S2_Val                         : REAL := 0.0;
    fCh2_S3_Val                         : REAL := 0.0;
    bCh2_S1_Valid                       : BOOL := TRUE;
    bCh2_S2_Valid                       : BOOL := TRUE;
    bCh2_S3_Valid                       : BOOL := TRUE;
    bCh2_Disc_12                        : BOOL := FALSE;
    bCh2_Disc_23                        : BOOL := FALSE;
    bCh2_Disc_13                        : BOOL := FALSE;
    fCh2_DiscTimer_12                   : REAL := 0.0;
    fCh2_DiscTimer_23                   : REAL := 0.0;
    fCh2_DiscTimer_13                   : REAL := 0.0;
    bCh2_S1_FaultLatched                : BOOL := FALSE;
    bCh2_S2_FaultLatched                : BOOL := FALSE;
    bCh2_S3_FaultLatched                : BOOL := FALSE;
    iCh2_HealthySensors                 : INT := 3;
    fCh2_VotedVal                       : REAL := 0.0;
    fCh2_LastGoodVal                    : REAL := 0.0;
    fCh2_TolDelta                       : REAL := 6.0;      (* Discrepancy Tolerance Delta [EBC] *)
    fCh2_TripTimerThresh                : REAL := 0.500;    (* Discrepancy Latching Filter Time [s] *)

    (* Channel 3: Wort Kettle Boiling Temperature RTD Transmitters [deg C] *)
    fCh3_S1_Val                         : REAL := 20.0;
    fCh3_S2_Val                         : REAL := 20.0;
    fCh3_S3_Val                         : REAL := 20.0;
    bCh3_S1_Valid                       : BOOL := TRUE;
    bCh3_S2_Valid                       : BOOL := TRUE;
    bCh3_S3_Valid                       : BOOL := TRUE;
    bCh3_Disc_12                        : BOOL := FALSE;
    bCh3_Disc_23                        : BOOL := FALSE;
    bCh3_Disc_13                        : BOOL := FALSE;
    fCh3_DiscTimer_12                   : REAL := 0.0;
    fCh3_DiscTimer_23                   : REAL := 0.0;
    fCh3_DiscTimer_13                   : REAL := 0.0;
    bCh3_S1_FaultLatched                : BOOL := FALSE;
    bCh3_S2_FaultLatched                : BOOL := FALSE;
    bCh3_S3_FaultLatched                : BOOL := FALSE;
    iCh3_HealthySensors                 : INT := 3;
    fCh3_VotedVal                       : REAL := 20.0;
    fCh3_LastGoodVal                    : REAL := 20.0;
    fCh3_TolDelta                       : REAL := 2.5;      (* Discrepancy Tolerance Delta [deg C] *)
    fCh3_TripTimerThresh                : REAL := 0.400;    (* Discrepancy Latching Filter Time [s] *)

    (* Channel 4: Wort Kettle Radar Hydrostatic Level Transmitters [%] *)
    fCh4_S1_Val                         : REAL := 0.0;
    fCh4_S2_Val                         : REAL := 0.0;
    fCh4_S3_Val                         : REAL := 0.0;
    bCh4_S1_Valid                       : BOOL := TRUE;
    bCh4_S2_Valid                       : BOOL := TRUE;
    bCh4_S3_Valid                       : BOOL := TRUE;
    bCh4_Disc_12                        : BOOL := FALSE;
    bCh4_Disc_23                        : BOOL := FALSE;
    bCh4_Disc_13                        : BOOL := FALSE;
    fCh4_DiscTimer_12                   : REAL := 0.0;
    fCh4_DiscTimer_23                   : REAL := 0.0;
    fCh4_DiscTimer_13                   : REAL := 0.0;
    bCh4_S1_FaultLatched                : BOOL := FALSE;
    bCh4_S2_FaultLatched                : BOOL := FALSE;
    bCh4_S3_FaultLatched                : BOOL := FALSE;
    iCh4_HealthySensors                 : INT := 3;
    fCh4_VotedVal                       : REAL := 0.0;
    fCh4_LastGoodVal                    : REAL := 0.0;
    fCh4_TolDelta                       : REAL := 3.0;      (* Discrepancy Tolerance Delta [%] *)
    fCh4_TripTimerThresh                : REAL := 0.450;    (* Discrepancy Latching Filter Time [s] *)

    (* Channel 5: Calandria Steam Header Pressure Transmitters [bar] *)
    fCh5_S1_Val                         : REAL := 0.0;
    fCh5_S2_Val                         : REAL := 0.0;
    fCh5_S3_Val                         : REAL := 0.0;
    bCh5_S1_Valid                       : BOOL := TRUE;
    bCh5_S2_Valid                       : BOOL := TRUE;
    bCh5_S3_Valid                       : BOOL := TRUE;
    bCh5_Disc_12                        : BOOL := FALSE;
    bCh5_Disc_23                        : BOOL := FALSE;
    bCh5_Disc_13                        : BOOL := FALSE;
    fCh5_DiscTimer_12                   : REAL := 0.0;
    fCh5_DiscTimer_23                   : REAL := 0.0;
    fCh5_DiscTimer_13                   : REAL := 0.0;
    bCh5_S1_FaultLatched                : BOOL := FALSE;
    bCh5_S2_FaultLatched                : BOOL := FALSE;
    bCh5_S3_FaultLatched                : BOOL := FALSE;
    iCh5_HealthySensors                 : INT := 3;
    fCh5_VotedVal                       : REAL := 0.0;
    fCh5_LastGoodVal                    : REAL := 0.0;
    fCh5_TolDelta                       : REAL := 0.35;     (* Discrepancy Tolerance Delta [bar] *)
    fCh5_TripTimerThresh                : REAL := 0.300;    (* Discrepancy Latching Filter Time [s] *)

    (* Channel 6: Lauter Runoff Magnetic Flowmeter Transmitters [hL/h] *)
    fCh6_S1_Val                         : REAL := 0.0;
    fCh6_S2_Val                         : REAL := 0.0;
    fCh6_S3_Val                         : REAL := 0.0;
    bCh6_S1_Valid                       : BOOL := TRUE;
    bCh6_S2_Valid                       : BOOL := TRUE;
    bCh6_S3_Valid                       : BOOL := TRUE;
    bCh6_Disc_12                        : BOOL := FALSE;
    bCh6_Disc_23                        : BOOL := FALSE;
    bCh6_Disc_13                        : BOOL := FALSE;
    fCh6_DiscTimer_12                   : REAL := 0.0;
    fCh6_DiscTimer_23                   : REAL := 0.0;
    fCh6_DiscTimer_13                   : REAL := 0.0;
    bCh6_S1_FaultLatched                : BOOL := FALSE;
    bCh6_S2_FaultLatched                : BOOL := FALSE;
    bCh6_S3_FaultLatched                : BOOL := FALSE;
    iCh6_HealthySensors                 : INT := 3;
    fCh6_VotedVal                       : REAL := 0.0;
    fCh6_LastGoodVal                    : REAL := 0.0;
    fCh6_TolDelta                       : REAL := 12.0;     (* Discrepancy Tolerance Delta [hL/h] *)
    fCh6_TripTimerThresh                : REAL := 0.400;    (* Discrepancy Latching Filter Time [s] *)

    (* ============================================================================================== *)
    (* PHASE 4: DETERMINISTIC 14-STAGE BREWHOUSE FINITE STATE MACHINE (FSM) VARIABLES                 *)
    (* ============================================================================================== *)
    (* Enumerated State Constants:
         0: STATE_IDLE
         1: STATE_PREFILL_FOUNDATION_WATER
         2: STATE_MASH_TRANSFER_INFLOW
         3: STATE_REST_GRAIN_BED_SETTLING
         4: STATE_VORLAUF_RECIRCULATION
         5: STATE_FIRST_WORT_RUNOFF_OPTIMIZATION
         6: STATE_SPARGING_HOT_WATER_DISTRIBUTION
         7: STATE_RAKE_DEEP_CUTTING_SEQUENCE
         8: STATE_SWEET_WATER_RUNOFF_CUTOFF
         9: STATE_SPENT_GRAIN_EVACUATION
        10: STATE_KETTLE_HEATING_CALANDRIA
        11: STATE_VIGOROUS_BOIL_EVAPORATION
        12: STATE_WHIRLPOOL_TANGENTIAL_INLET_REST
        13: STATE_CIP_CAUSTIC_SANITIZATION *)
    eState                              : INT := 0;         (* Active Operational State *)
    ePrevState                          : INT := 0;         (* Previous Operational State *)
    tStateTimer                         : REAL := 0.0;      (* Active State Continuous Run Timer [s] *)
    tSubStateTimer                      : REAL := 0.0;      (* Internal Substate Progression Timer [s] *)
    iSubStep                            : INT := 0;         (* Sequence Progression Step Index *)

    (* FSM Specific Process Accumulators & Interlocks *)
    fFoundationWaterAccumVolume         : REAL := 0.0;      (* Prefill Underlet Water Volume [hL] *)
    fMashTransferAccumVolume            : REAL := 0.0;      (* Mash Inflow Accumulated Volume [hL] *)
    fRunoffAccumVolume                  : REAL := 0.0;      (* Total Runoff Volume Transferred to Kettle [hL] *)
    fSpargeWaterAccumVolume             : REAL := 0.0;      (* Cumulative Hot Sparge Liquor Applied [hL] *)
    fBoilTimerSeconds                   : REAL := 0.0;      (* Cumulative Vigorous Boiling Clock [s] *)
    fWhirlpoolRestTimerSeconds          : REAL := 0.0;      (* Quiescent Trub Cone Settling Timer [s] *)
    fCIPStepTimerSeconds                : REAL := 0.0;      (* Automated Cleaning Loop Step Timer [s] *)
    bDeepCutRequired                    : BOOL := FALSE;    (* Bed Differential Pressure Deep Cut Trigger *)
    iDeepCutCycleCount                  : INT := 0;         (* Total Deep Cut Maneuvers Completed in Batch *)
    bHopAddition1Done                   : BOOL := FALSE;    (* Bittering Hop Charge Discharged Latch *)
    bHopAddition2Done                   : BOOL := FALSE;    (* Aroma Hop Charge Discharged Latch *)
    bSpentGrainDoorOpenPermissive       : BOOL := FALSE;    (* Safe Hydraulic Interlock for Spent Grain Hatch *)

    (* ============================================================================================== *)
    (* PHASE 5: ISA-18.2 MULTI-TIER PROCESS ALARM ENGINE & BIT-PACKED STATUS WORDS                   *)
    (* ============================================================================================== *)
    (* Alarm Trip Setpoints *)
    fLauterDP_TripHH                    : REAL := 55.0;     (* Differential Pressure Critical High-High [mbar] *)
    fLauterDP_TripH                     : REAL := 42.0;     (* Differential Pressure Warning High [mbar] *)
    fLauterDP_Deadband                  : REAL := 3.0;      (* Differential Pressure Trip Deadband [mbar] *)

    fTurbidity_TripHH                   : REAL := 120.0;    (* Runoff Turbidity Critical High-High [EBC] *)
    fTurbidity_TripH                    : REAL := 50.0;     (* Runoff Turbidity Warning High [EBC] *)
    fTurbidity_Deadband                 : REAL := 4.0;      (* Runoff Turbidity Deadband [EBC] *)

    fKettleTemp_TripHH                  : REAL := 105.0;    (* Kettle Boiling Temp Critical High-High [deg C] *)
    fKettleTemp_TripH                   : REAL := 103.0;    (* Kettle Boiling Temp Warning High [deg C] *)
    fKettleTemp_TripL                   : REAL := 96.0;     (* Kettle Boiling Temp Warning Low [deg C] *)
    fKettleTemp_TripLL                  : REAL := 85.0;     (* Kettle Boiling Temp Critical Low-Low [deg C] *)
    fKettleTemp_Deadband                : REAL := 1.2;      (* Kettle Temperature Deadband [deg C] *)

    fSteamP_TripHH                      : REAL := 4.6;      (* Calandria Steam Supply Critical High-High [bar] *)
    fSteamP_TripH                       : REAL := 4.0;      (* Calandria Steam Supply Warning High [bar] *)
    fSteamP_TripL                       : REAL := 1.2;      (* Calandria Steam Supply Warning Low [bar] *)
    fSteamP_TripLL                      : REAL := 0.6;      (* Calandria Steam Supply Critical Low-Low [bar] *)
    fSteamP_Deadband                    : REAL := 0.20;     (* Calandria Steam Pressure Deadband [bar] *)

    fKettleLevel_TripHH                 : REAL := 95.0;     (* Wort Kettle Level Critical High-High [%] *)
    fKettleLevel_TripH                  : REAL := 90.0;     (* Wort Kettle Level Warning High [%] *)
    fKettleLevel_TripLL                 : REAL := 4.0;      (* Wort Kettle Level Critical Low-Low [%] *)
    fKettleLevel_Deadband               : REAL := 2.0;      (* Wort Kettle Level Deadband [%] *)

    fRakeTorque_TripHH                  : REAL := 1850.0;   (* Wort Rake Cutting Motor Critical High-High Torque [Nm] *)
    fRakeTorque_TripH                   : REAL := 1500.0;   (* Wort Rake Cutting Motor Warning High Torque [Nm] *)
    fRakeTorque_Deadband                : REAL := 80.0;     (* Wort Rake Cutting Torque Deadband [Nm] *)

    (* Alarm Debounce Timers *)
    tTimerDP_HH                         : REAL := 0.0;
    tTimerDP_H                          : REAL := 0.0;
    tTimerTurb_HH                       : REAL := 0.0;
    tTimerTurb_H                        : REAL := 0.0;
    tTimerTemp_HH                       : REAL := 0.0;
    tTimerTemp_H                        : REAL := 0.0;
    tTimerTemp_LL                       : REAL := 0.0;
    tTimerSteamP_HH                     : REAL := 0.0;
    tTimerSteamP_H                      : REAL := 0.0;
    tTimerLevel_HH                      : REAL := 0.0;
    tTimerTorque_HH                     : REAL := 0.0;
    tTimerTorque_H                      : REAL := 0.0;

    (* Active Alarm Condition Flags *)
    bAlarmDP_HH_Active                  : BOOL := FALSE;
    bAlarmDP_H_Active                   : BOOL := FALSE;
    bAlarmTurb_HH_Active                : BOOL := FALSE;
    bAlarmTurb_H_Active                 : BOOL := FALSE;
    bAlarmTemp_HH_Active                : BOOL := FALSE;
    bAlarmTemp_H_Active                 : BOOL := FALSE;
    bAlarmTemp_LL_Active                : BOOL := FALSE;
    bAlarmSteamP_HH_Active              : BOOL := FALSE;
    bAlarmSteamP_H_Active               : BOOL := FALSE;
    bAlarmLevel_HH_Active               : BOOL := FALSE;
    bAlarmTorque_HH_Active              : BOOL := FALSE;
    bAlarmTorque_H_Active               : BOOL := FALSE;
    bAlarmTMR_DP_Degraded               : BOOL := FALSE;
    bAlarmTMR_Turb_Degraded             : BOOL := FALSE;
    bAlarmTMR_Temp_Degraded             : BOOL := FALSE;
    bAlarmTMR_Level_Degraded            : BOOL := FALSE;
    bAlarmTMR_SteamP_Degraded           : BOOL := FALSE;
    bAlarmTMR_Flow_Degraded             : BOOL := FALSE;
    bAlarmEmergencyStopActive           : BOOL := FALSE;

    (* Unacknowledged Alarm Latches (ISA-18.2 Sequence A) *)
    bUnackDP_HH                         : BOOL := FALSE;
    bUnackTurb_HH                       : BOOL := FALSE;
    bUnackTemp_HH                       : BOOL := FALSE;
    bUnackSteamP_HH                     : BOOL := FALSE;
    bUnackLevel_HH                      : BOOL := FALSE;
    bUnackTorque_HH                     : BOOL := FALSE;

    (* Latched First-Out Trip Memory *)
    bFirstOutLatched                    : BOOL := FALSE;
    dwFirstOutCode                      : DWORD := 16#00000000;

    (* General Cyber-Physical Process Estimators & Filters *)
    fWortDynamicViscosity               : REAL := 0.00165;  (* Sweet Wort Dynamic Viscosity mu [Pa*s] *)
    fPermeabilityDarcyRaw               : REAL := 1.2E-10;  (* Computed Darcy Permeability K [m2] *)
    fPermeabilityFiltered               : REAL := 1.2E-10;  (* Low-Pass Filtered Permeability [m2] *)
    fDiffPressureRateOfChange           : REAL := 0.0;      (* Time Derivative of Grain Bed DP d(DP)/dt [mbar/s] *)
    fPrevVotedDP                        : REAL := 0.0;      (* Previous Scan Voted Differential Pressure [mbar] *)
    fCalandriaCleanDutyWatts            : REAL := 0.0;      (* Clean Calandria Theoretical Thermal Duty [W] *)
    fCalandriaActualDutyWatts           : REAL := 0.0;      (* Actual Calandria Observed Thermal Duty [W] *)
    fCalandriaFoulingFactor             : REAL := 1.0;      (* Ratio of Actual to Clean U-Value [-] *)
    fSMM_Concentration                  : REAL := 450.0;    (* Malt S-Methylmethionine Precursor Pool [ppb] *)
    fDMS_StrippingRateCoeff             : REAL := 0.0;      (* Volatilization Kinetic Coefficient [1/s] *)
    fSMM_CleavageRateCoeff              : REAL := 0.0;      (* Thermal Decomposition Kinetic Coefficient [1/s] *)

    (* Temporary Optimization, Matrix Arithmetic & Iteration Counters *)
    idxRow                              : INT := 1;
    idxCol                              : INT := 1;
    idxInput                            : INT := 1;
    idxHorizon                          : INT := 0;
    idxIter                             : INT := 1;
    fTempSum                            : REAL := 0.0;
    fTempScalar                         : REAL := 0.0;
    fMedianArray                        : ARRAY[1..3] OF REAL;
    fTempSort                           : REAL := 0.0;
END_VAR
"""
