# mining_flotation_builder/section_var_declarations.py
"""
Section: Internal Variable Declarations (VAR)
Function Block: FB_Mining_Flotation_RougherScavenger_FrothDepth_ReagentDosing
"""

def get_var_declarations():
    return """VAR
    (* ========================================================================= *)
    (* SYSTEM INITIALIZATION, CYCLIC EXECUTION & TIME BASE                       *)
    (* ========================================================================= *)
    bInitDone                       : BOOL := FALSE;        (* Initialization complete latch *)
    rCycleTimeSec                   : REAL := 0.020;        (* Discrete scan cycle interval [s] (20 ms) *)
    nCycleCounter                   : UDINT := 0;           (* Cyclic execution loop counter *)
    rActiveTimeSec                  : REAL := 0.0;          (* Total active operational running time [s] *)

    (* ========================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING INTERNAL STRUCTURES          *)
    (* ========================================================================= *)
    (* Channel A/B/C Raw Latch and Sanity Bounds *)
    rPulpLevel_ChA_Clamped          : REAL;                 (* Clamped valid input [mm] *)
    rPulpLevel_ChB_Clamped          : REAL;                 (* Clamped valid input [mm] *)
    rPulpLevel_ChC_Clamped          : REAL;                 (* Clamped valid input [mm] *)
    rFrothHeight_ChA_Clamped        : REAL;                 (* Clamped valid input [mm] *)
    rFrothHeight_ChB_Clamped        : REAL;                 (* Clamped valid input [mm] *)
    rFrothHeight_ChC_Clamped        : REAL;                 (* Clamped valid input [mm] *)
    rPulpPH_ChA_Clamped             : REAL;                 (* Clamped valid input [pH] *)
    rPulpPH_ChB_Clamped             : REAL;                 (* Clamped valid input [pH] *)
    rPulpPH_ChC_Clamped             : REAL;                 (* Clamped valid input [pH] *)
    rSlurryDensity_ChA_Clamped      : REAL;                 (* Clamped valid input [kg/m3] *)
    rSlurryDensity_ChB_Clamped      : REAL;                 (* Clamped valid input [kg/m3] *)
    rSlurryDensity_ChC_Clamped      : REAL;                 (* Clamped valid input [kg/m3] *)

    (* TMR Discrepancy Thresholds & Tolerances *)
    rPulpLevel_DevLimit             : REAL := 85.0;         (* Max permissible channel delta [mm] *)
    rFrothHeight_DevLimit           : REAL := 35.0;         (* Max permissible channel delta [mm] *)
    rPH_DevLimit                    : REAL := 0.45;         (* Max permissible channel delta [pH] *)
    rDensity_DevLimit               : REAL := 65.0;         (* Max permissible channel delta [kg/m3] *)

    (* TMR Persistence Discrepancy Timers (250 ms fault qualification) *)
    tPulpLevel_Timer_AB             : REAL := 0.0;          (* Discrepancy timer pair AB [s] *)
    tPulpLevel_Timer_BC             : REAL := 0.0;          (* Discrepancy timer pair BC [s] *)
    tPulpLevel_Timer_CA             : REAL := 0.0;          (* Discrepancy timer pair CA [s] *)

    tFrothHeight_Timer_AB           : REAL := 0.0;          (* Discrepancy timer pair AB [s] *)
    tFrothHeight_Timer_BC           : REAL := 0.0;          (* Discrepancy timer pair BC [s] *)
    tFrothHeight_Timer_CA           : REAL := 0.0;          (* Discrepancy timer pair CA [s] *)

    tPH_Timer_AB                    : REAL := 0.0;          (* Discrepancy timer pair AB [s] *)
    tPH_Timer_BC                    : REAL := 0.0;          (* Discrepancy timer pair BC [s] *)
    tPH_Timer_CA                    : REAL := 0.0;          (* Discrepancy timer pair CA [s] *)

    tDensity_Timer_AB               : REAL := 0.0;          (* Discrepancy timer pair AB [s] *)
    tDensity_Timer_BC               : REAL := 0.0;          (* Discrepancy timer pair BC [s] *)
    tDensity_Timer_CA               : REAL := 0.0;          (* Discrepancy timer pair CA [s] *)

    rDiscrepancyTripTime            : REAL := 0.250;        (* Persistence threshold: 250 milliseconds *)

    (* TMR Channel Fault Disqualification Flags *)
    bFail_PulpLevel_A               : BOOL := FALSE;
    bFail_PulpLevel_B               : BOOL := FALSE;
    bFail_PulpLevel_C               : BOOL := FALSE;

    bFail_FrothHeight_A             : BOOL := FALSE;
    bFail_FrothHeight_B             : BOOL := FALSE;
    bFail_FrothHeight_C             : BOOL := FALSE;

    bFail_PH_A                      : BOOL := FALSE;
    bFail_PH_B                      : BOOL := FALSE;
    bFail_PH_C                      : BOOL := FALSE;

    bFail_Density_A                 : BOOL := FALSE;
    bFail_Density_B                 : BOOL := FALSE;
    bFail_Density_C                 : BOOL := FALSE;

    (* Previous Good Voted Holds for Bumpless Degradation *)
    rPulpLevel_LastValid            : REAL := 3200.0;       (* Hold last valid level [mm] *)
    rFrothHeight_LastValid          : REAL := 180.0;        (* Hold last valid froth [mm] *)
    rPH_LastValid                   : REAL := 10.50;        (* Hold last valid pH [pH] *)
    rDensity_LastValid              : REAL := 1450.0;       (* Hold last valid density [kg/m3] *)

    (* ========================================================================= *)
    (* FIRST-PRINCIPLES FLOTATION HYDRODYNAMICS & CHEMICAL KINETICS VARIABLES   *)
    (* ========================================================================= *)
    rCellNetVolume_M3               : REAL := 160.0;        (* Active slurry volumetric capacity of rougher tank [m3] *)
    rCellCrossSectionArea_M2        : REAL := 38.5;         (* Planar top surface cross sectional area [m2] *)
    rRotorDiameter_M                : REAL := 1.25;         (* Agitation rotor impeller diameter [m] *)
    rMeanBubbleDiameter_M           : REAL;                 (* Sauter mean bubble diameter in meters [m] *)
    rSuperficialGasVelocity_M_S     : REAL;                 (* Superficial gas velocity in SI units [m/s] *)
    rSlurryVolumetricFlow_M3_S      : REAL;                 (* Volumetric feed flow in cubic meters per second [m3/s] *)
    rSlurryDensity_SI               : REAL;                 (* Pulp density in kg/m3 *)
    rSlurryApparentViscosity_PaS    : REAL := 0.0035;       (* Apparent non-Newtonian Bingham plastic viscosity [Pa*s] *)
    rMineralParticleDiameter_M      : REAL := 0.000075;     (* P80 primary grind particle size d80 = 75 microns [m] *)
    rMineralParticleDensity_KgM3    : REAL := 4200.0;       (* Chalcopyrite (CuFeS2) mineral crystal density [kg/m3] *)
    rWaterDensity_KgM3              : REAL := 1000.0;       (* Process water reference density [kg/m3] *)

    (* Dimensionless Hydrodynamic Numbers *)
    rSlurryReynoldsNumber           : REAL;                 (* Agitator impeller Reynolds number Re *)
    rBubbleReynoldsNumber           : REAL;                 (* Dispersed gas bubble slip Reynolds number Re_b *)
    rFroudeNumber                   : REAL;                 (* Rotor centrifugal Froude number Fr *)

    (* Probabilistic Micro-Scale Flotation Sub-Processes *)
    rProbabilityCollision_Pc        : REAL;                 (* Particle-bubble collision probability (Sutherland / Weber) *)
    rProbabilityAttachment_Pa       : REAL;                 (* Particle-bubble attachment probability (Dobby-Finch contact angle) *)
    rProbabilityDetachment_Ed       : REAL;                 (* Froth zone detachment drop-back probability *)
    rFrothDropBackFactor_Rf         : REAL;                 (* Froth recovery factor Rf = 1.0 - Ed *)
    rFrothResidenceTime_Sec         : REAL;                 (* Residence time of mineralized bubbles in froth layer [s] *)
    rBubbleSurfaceAreaFlux_Sb       : REAL;                 (* Bubble surface area flux Sb = 6 * Jg / d32 [1/s] *)
    rFlotationRateConstant_k        : REAL;                 (* Dynamic rate constant k [1/s] *)
    rFlotationRateConstant_k_Min    : REAL;                 (* Rate constant per minute [1/min] *)
    rMaxTheoreticalRecovery_Rmax    : REAL := 0.965;        (* Maximum recoverable fast-floating copper fraction *)
    rHydrodynamicResTime_Sec        : REAL;                 (* Hydrodynamic residence time Tres [s] *)
    rHydrodynamicResTime_Min        : REAL;                 (* Hydrodynamic residence time Tres [min] *)
    rModelCalculatedRecovery        : REAL;                 (* First-principles theoretical recovery R = Rmax*(1-exp(-k*t)) *)

    (* Decoupled Pulp-Froth Hydraulic Geometry *)
    rTotalPulpFrothHeight           : REAL;                 (* Measured total cell head [mm] *)
    rOverflowWeirCrestElevation     : REAL := 4200.0;       (* Mechanical overflow lip elevation above cell floor [mm] *)
    rDartValve1_CvMax               : REAL := 850.0;        (* Dart valve 1 maximum flow capacity coefficient Cv *)
    rDartValve2_CvMax               : REAL := 850.0;        (* Dart valve 2 maximum flow capacity coefficient Cv *)
    rDartValve1_FlowM3H             : REAL;                 (* Instantaneous volumetric discharge flow valve 1 [m3/h] *)
    rDartValve2_FlowM3H             : REAL;                 (* Instantaneous volumetric discharge flow valve 2 [m3/h] *)
    rTotalTailingsDischargeFlow     : REAL;                 (* Total cell underflow slurry evacuation [m3/h] *)
    rNetHydraulicMassBalanceDelta   : REAL;                 (* Slurry inflow vs outflow imbalance [m3/h] *)

    (* Machine Vision Spectral Grade Correlation *)
    rFrothColor_Hue                 : REAL;                 (* Calculated HSV Hue angle [deg] *)
    rFrothColor_Saturation          : REAL;                 (* Calculated HSV Saturation [0..1] *)
    rFrothColor_Value               : REAL;                 (* Calculated HSV Brightness Value [0..1] *)
    rSpectralCopperIndex            : REAL;                 (* Spectral band ratio (Red - Blue) / (Red + Blue + 0.001) *)
    rVisionEstimatedGrade_Cu        : REAL;                 (* Optical inferred copper concentrate grade [% Cu] *)

    (* Reagent Dosing Cascade Multipliers *)
    rPAX_TonnageRatio_Dynamic       : REAL;                 (* Dynamic PAX dose [g/t dry ore] *)
    rMIBC_TonnageRatio_Dynamic      : REAL;                 (* Dynamic MIBC frother dose [g/t dry ore] *)
    rPAX_MassFlowTarget_KgH         : REAL;                 (* PAX pure mass delivery target [kg/h] *)
    rMIBC_MassFlowTarget_KgH        : REAL;                 (* MIBC pure mass delivery target [kg/h] *)
    rLimeVolumetricDose_LPH         : REAL;                 (* Milk of lime slurry volumetric dose [L/h] *)
    rLimeTitrationGain              : REAL := 125.0;        (* Non-linear acid-base titration slope gain *)

    (* ========================================================================= *)
    (* DISCRETE STATE-SPACE OBSERVER MATRICES (6x6 SYSTEM)                       *)
    (* ========================================================================= *)
    (* States x: [x1: Pulp Level (mm), x2: Froth Depth (mm), x3: pH,            *)
    (*            x4: Cu Recovery (%), x5: Cu Grade (%), x6: Air Holdup (%)]     *)
    (* Actuators u: [u1: Dart Valve 1 (%), u2: Air Damper (%),                  *)
    (*               u3: PAX Pump (%), u4: MIBC Pump (%), u5: Lime Valve (%)]    *)
    A_Matrix                        : ARRAY[1..6, 1..6] OF REAL; (* Discrete state transition matrix A (6x6) *)
    B_Matrix                        : ARRAY[1..6, 1..5] OF REAL; (* Discrete control input matrix B (6x5) *)
    C_Matrix                        : ARRAY[1..6, 1..6] OF REAL; (* Discrete output measurement matrix C (6x6) *)
    D_Matrix                        : ARRAY[1..6, 1..5] OF REAL; (* Direct feedthrough matrix D (6x5) *)
    L_Gain                          : ARRAY[1..6, 1..6] OF REAL; (* Steady-state Luenberger observer innovation gain L (6x6) *)

    (* Observer Vector Registers *)
    x_hat                           : ARRAY[1..6] OF REAL; (* Observer estimated state vector at step k *)
    x_hat_next                      : ARRAY[1..6] OF REAL; (* State propagation vector at step k+1 *)
    x_corr                          : ARRAY[1..6] OF REAL; (* Innovation corrected state vector at step k *)
    x_ref                           : ARRAY[1..6] OF REAL; (* Reference target state vector *)
    x_err                           : ARRAY[1..6] OF REAL; (* State tracking error vector (x_hat - x_ref) *)
    y_meas                          : ARRAY[1..6] OF REAL; (* TMR voted actual measurement vector *)
    y_est                           : ARRAY[1..6] OF REAL; (* Estimated measurement output vector C*x_hat + D*u *)
    y_innov                         : ARRAY[1..6] OF REAL; (* Innovation residual vector (y_meas - y_est) *)
    u_act                           : ARRAY[1..5] OF REAL; (* Actuator command vector applied at step k *)
    u_prev                          : ARRAY[1..5] OF REAL; (* Actuator command vector from previous scan k-1 *)
    delta_u                         : ARRAY[1..5] OF REAL; (* Actuator slew vector (u_act - u_prev) *)

    (* ========================================================================= *)
    (* RECEDING-HORIZON MPC OPTIMIZATION MATRICES & PGD ITERATION VARIABLES     *)
    (* ========================================================================= *)
    Q_Weight                        : ARRAY[1..6, 1..6] OF REAL; (* State tracking error penalty matrix Q (6x6) *)
    R_Weight                        : ARRAY[1..5, 1..5] OF REAL; (* Actuator effort penalty matrix R (5x5) *)
    S_Weight                        : ARRAY[1..5, 1..5] OF REAL; (* Actuator slew rate damping penalty matrix S (5x5) *)
    P_Weight                        : ARRAY[1..6, 1..6] OF REAL; (* Terminal state penalty matrix P (6x6) *)

    (* Actuator Hard Saturation & Slew Constraints *)
    u_min                           : ARRAY[1..5] OF REAL; (* Lower bounds on actuators [%] *)
    u_max                           : ARRAY[1..5] OF REAL; (* Upper bounds on actuators [%] *)
    du_min                          : ARRAY[1..5] OF REAL; (* Maximum negative slew per cycle [%/scan] *)
    du_max                          : ARRAY[1..5] OF REAL; (* Maximum positive slew per cycle [%/scan] *)

    (* PGD Optimization Unrolled Variables *)
    rPGD_StepSize                   : REAL := 0.0125;       (* Gradient descent step size alpha *)
    rParetoTradeOffSlope            : REAL := 1.85;         (* Recovery vs Grade Pareto trade-off curve slope *)
    rParetoGradePenaltyThreshold    : REAL := 22.0;         (* Critical concentrate Cu grade floor [%] *)
    rDynamicGradePenaltyWeight      : REAL;                 (* Exponential penalty multiplier if grade drops *)

    (* Optimization Vector Scratchpads *)
    u_opt                           : ARRAY[1..5] OF REAL; (* Candidate optimized control input *)
    u_cand                          : ARRAY[1..5] OF REAL; (* Intermediate candidate input *)
    grad_J                          : ARRAY[1..5] OF REAL; (* Cost function gradient with respect to control u *)
    lambda_costate                  : ARRAY[1..6] OF REAL; (* Adjoint costate vector backwards propagated *)
    x_rollout                       : ARRAY[1..6] OF REAL; (* Forward simulated state rollout *)

    (* ========================================================================= *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) VARIABLES              *)
    (* ========================================================================= *)
    eState                          : INT := 0;             (* Active FSM stage index (0 to 13) *)
    ePrevState                      : INT := -1;            (* Previous FSM stage index *)
    rStateTimerSec                  : REAL := 0.0;          (* Elapsed duration in active state [s] *)
    bStateFirstScan                 : BOOL := TRUE;         (* First scan trigger upon state transition *)
    nSubStageCounter                : INT := 0;             (* Internal sub-step sequencing index *)

    (* Specific FSM Operational Target Buffers & Ramp Rates *)
    rWaterFillTargetLevel           : REAL := 2800.0;       (* Baseline water fill depth [mm] *)
    rAgitatorRampTargetSpeed        : REAL := 185.0;        (* Agitator operational rotor speed [rpm] *)
    rAgitatorIdleSpeed              : REAL := 60.0;         (* Agitator idling keep-alive speed [rpm] *)
    rAirDamperSoftBlowPosition      : REAL := 25.0;         (* Soft-blow aeration sparging damper position [%] *)
    rAirDamperNominalPosition       : REAL := 65.0;         (* Nominal aeration sparging damper position [%] *)
    rDrainDartValvePosition         : REAL := 95.0;         (* Slurry tank drain dump dart valve position [%] *)
    rAcidFlushPinchValveCmd         : REAL := 45.0;         (* Descaling acid loop pinch valve command [%] *)

    (* ========================================================================= *)
    (* ISA-18.2 MULTI-TIER ALARM ENGINE TRIP POINTS, TIMERS & LATCHES           *)
    (* ========================================================================= *)
    (* Trip Point Thresholds *)
    rPulpLevel_HH                   : REAL := 4200.0;       (* Pulp Level High-High Trip [mm] *)
    rPulpLevel_H                    : REAL := 3950.0;       (* Pulp Level High Warning [mm] *)
    rPulpLevel_L                    : REAL := 2300.0;       (* Pulp Level Low Warning [mm] *)
    rPulpLevel_LL                   : REAL := 2050.0;       (* Pulp Level Low-Low Trip [mm] *)
    rPulpLevel_Hyst                 : REAL := 30.0;         (* Hysteresis clearance deadband [mm] *)

    rFrothDepth_HH                  : REAL := 550.0;        (* Froth Depth High-High Overflow Risk [mm] *)
    rFrothDepth_H                   : REAL := 450.0;        (* Froth Depth High Thick Bed [mm] *)
    rFrothDepth_L                   : REAL := 90.0;         (* Froth Depth Low Thin Bed [mm] *)
    rFrothDepth_LL                  : REAL := 45.0;         (* Froth Depth Low-Low Loss of Lip Seal [mm] *)
    rFrothDepth_Hyst                : REAL := 12.0;         (* Hysteresis deadband [mm] *)

    rSlurryPH_HH                    : REAL := 12.2;         (* Slurry pH High-High Caustic Limit [pH] *)
    rSlurryPH_H                     : REAL := 11.4;         (* Slurry pH High Warning [pH] *)
    rSlurryPH_L                     : REAL := 9.8;          (* Slurry pH Low Pyrite Activation Warning [pH] *)
    rSlurryPH_LL                    : REAL := 8.8;          (* Slurry pH Low-Low Extreme Acid Slurry [pH] *)
    rSlurryPH_Hyst                  : REAL := 0.15;         (* Hysteresis deadband [pH] *)

    rSlurryDensity_HH               : REAL := 2150.0;       (* Slurry Specific Gravity High-High Sanding Trip [kg/m3] *)
    rSlurryDensity_H                : REAL := 1950.0;       (* Slurry Specific Gravity High Warning [kg/m3] *)
    rSlurryDensity_L                : REAL := 1250.0;       (* Slurry Specific Gravity Low Dilution Warning [kg/m3] *)
    rSlurryDensity_LL               : REAL := 1120.0;       (* Slurry Specific Gravity Low-Low Empty Cell [kg/m3] *)
    rSlurryDensity_Hyst             : REAL := 25.0;         (* Hysteresis deadband [kg/m3] *)

    rAgitatorTorque_HH              : REAL := 42.0;         (* Rotor shaft torque High-High Sanding Overload [kN*m] *)
    rAgitatorTorque_H               : REAL := 35.0;         (* Rotor shaft torque High Warning [kN*m] *)
    rAgitatorTorque_Hyst            : REAL := 1.5;          (* Hysteresis deadband [kN*m] *)

    rAgitatorPower_HH               : REAL := 560.0;        (* Agitator motor power High-High Electrical Trip [kW] *)
    rAgitatorPower_H                : REAL := 510.0;        (* Agitator motor power High Warning [kW] *)
    rAgitatorPower_Hyst             : REAL := 15.0;         (* Hysteresis deadband [kW] *)

    rAirHeaderPressure_HH           : REAL := 3.20;         (* Sparging air pressure High-High Blower Surge [bar] *)
    rAirHeaderPressure_H            : REAL := 2.85;         (* Sparging air pressure High Warning [bar] *)
    rAirHeaderPressure_L            : REAL := 1.25;         (* Sparging air pressure Low Loss of Aeration [bar] *)
    rAirHeaderPressure_LL           : REAL := 0.85;         (* Sparging air pressure Low-Low Air Blower Trip [bar] *)
    rAirHeaderPressure_Hyst         : REAL := 0.08;         (* Hysteresis deadband [bar] *)

    rConcentrateGrade_L             : REAL := 15.0;         (* Concentrate copper grade Low Economic Loss [% Cu] *)
    rConcentrateGrade_LL            : REAL := 10.5;         (* Concentrate copper grade Low-Low Barren Froth [% Cu] *)
    rConcentrateGrade_Hyst          : REAL := 0.60;         (* Hysteresis deadband [% Cu] *)

    rCopperRecovery_L               : REAL := 76.0;         (* Rougher copper recovery Low Tailings Losses [%] *)
    rCopperRecovery_LL              : REAL := 66.0;         (* Rougher copper recovery Low-Low Catastrophic Losses [%] *)
    rCopperRecovery_Hyst            : REAL := 1.20;         (* Hysteresis deadband [%] *)

    rDartValveStiction_H            : REAL := 12.0;         (* Dart valve cmd vs feedback deviation warning [%] *)
    rDartValveStiction_HH           : REAL := 24.0;         (* Dart valve cmd vs feedback deviation critical jam [%] *)
    rDartValveStiction_Hyst         : REAL := 2.0;          (* Hysteresis deadband [%] *)

    (* Alarm Delay Qualification Timers [s] *)
    tTimer_Level_HH                 : REAL := 0.0;
    tTimer_Level_H                  : REAL := 0.0;
    tTimer_Level_L                  : REAL := 0.0;
    tTimer_Level_LL                 : REAL := 0.0;

    tTimer_Froth_HH                 : REAL := 0.0;
    tTimer_Froth_H                  : REAL := 0.0;
    tTimer_Froth_L                  : REAL := 0.0;
    tTimer_Froth_LL                 : REAL := 0.0;

    tTimer_PH_HH                    : REAL := 0.0;
    tTimer_PH_H                     : REAL := 0.0;
    tTimer_PH_L                     : REAL := 0.0;
    tTimer_PH_LL                    : REAL := 0.0;

    tTimer_Density_HH               : REAL := 0.0;
    tTimer_Density_H                : REAL := 0.0;
    tTimer_Density_L                : REAL := 0.0;
    tTimer_Density_LL               : REAL := 0.0;

    tTimer_Torque_HH                : REAL := 0.0;
    tTimer_Torque_H                 : REAL := 0.0;

    tTimer_Power_HH                 : REAL := 0.0;
    tTimer_Power_H                  : REAL := 0.0;

    tTimer_AirPress_HH              : REAL := 0.0;
    tTimer_AirPress_H               : REAL := 0.0;
    tTimer_AirPress_L               : REAL := 0.0;
    tTimer_AirPress_LL              : REAL := 0.0;

    tTimer_Grade_L                  : REAL := 0.0;
    tTimer_Grade_LL                 : REAL := 0.0;

    tTimer_Recovery_L               : REAL := 0.0;
    tTimer_Recovery_LL              : REAL := 0.0;

    tTimer_DartStiction             : REAL := 0.0;

    (* Latched Alarm Boolean Status Registers *)
    bAlarm_Level_HH                 : BOOL := FALSE;
    bAlarm_Level_H                  : BOOL := FALSE;
    bAlarm_Level_L                  : BOOL := FALSE;
    bAlarm_Level_LL                 : BOOL := FALSE;

    bAlarm_Froth_HH                 : BOOL := FALSE;
    bAlarm_Froth_H                  : BOOL := FALSE;
    bAlarm_Froth_L                  : BOOL := FALSE;
    bAlarm_Froth_LL                 : BOOL := FALSE;

    bAlarm_PH_HH                    : BOOL := FALSE;
    bAlarm_PH_H                     : BOOL := FALSE;
    bAlarm_PH_L                     : BOOL := FALSE;
    bAlarm_PH_LL                    : BOOL := FALSE;

    bAlarm_Density_HH               : BOOL := FALSE;
    bAlarm_Density_H                : BOOL := FALSE;
    bAlarm_Density_L                : BOOL := FALSE;
    bAlarm_Density_LL               : BOOL := FALSE;

    bAlarm_Torque_HH                : BOOL := FALSE;
    bAlarm_Torque_H                 : BOOL := FALSE;

    bAlarm_Power_HH                 : BOOL := FALSE;
    bAlarm_Power_H                  : BOOL := FALSE;

    bAlarm_AirPress_HH              : BOOL := FALSE;
    bAlarm_AirPress_H               : BOOL := FALSE;
    bAlarm_AirPress_L               : BOOL := FALSE;
    bAlarm_AirPress_LL              : BOOL := FALSE;

    bAlarm_Grade_L                  : BOOL := FALSE;
    bAlarm_Grade_LL                 : BOOL := FALSE;

    bAlarm_Recovery_L               : BOOL := FALSE;
    bAlarm_Recovery_LL              : BOOL := FALSE;

    bAlarm_DartStiction_Jam         : BOOL := FALSE;
    bAlarm_PAX_Starvation           : BOOL := FALSE;
    bAlarm_MIBC_Starvation          : BOOL := FALSE;
    bAlarm_LimeSupplyLoss           : BOOL := FALSE;

    (* First-Out Alarm Capturing Latch *)
    bFirstOutLatched                : BOOL := FALSE;
    nFirstOutFaultCode              : UDINT := 0;

    (* Math & Array Iteration Scratch Index Registers *)
    nIdxRow                         : INT;
    nIdxCol                         : INT;
    nIdxIter                        : INT;
    nIdxAct                         : INT;
    rTempSum                        : REAL;
    rTempDelta                      : REAL;
    rTempClamp                      : REAL;
END_VAR
"""
