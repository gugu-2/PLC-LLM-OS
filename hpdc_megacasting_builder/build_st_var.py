# hpdc_megacasting_builder/build_st_var.py

def get_var_declarations():
    return """VAR
    (* =================================================================================================================
     * SECTION 1: CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL MATRICES & VECTORS (Ts = 1.0 ms)
     * Continuous-to-discrete conversion via matrix exponential at 1 kHz:
     * x[k+1] = A * x[k] + B * u[k] + Ew * w[k]
     * y[k]   = C * x[k] + D * u[k]
     * x1: Plunger Stroke Position Deviation [mm]
     * x2: Plunger Axial Velocity Deviation [m/s]
     * x3: Shot Cylinder Head Chamber Hydraulic Pressure [bar]
     * x4: Shot Cylinder Rod Chamber Hydraulic Pressure [bar]
     * x5: In-Cavity Molten Alloy Dynamic Infiltration Pressure [bar]
     * x6: Cavity Evacuation Absolute Gas Pressure [mbar]
     * x7: Average Die Surface Steel Bulk Temperature Deviation [deg C]
     * x8: Intensifier Hydraulic Accumulator Intermediate Pressure [bar]
     * u1: Main Shot Servo Valve Spool Position Command [%] (-100% to +100%)
     * u2: High-Speed Accumulator Discharge Cartridge Valve [%] (0 to 100%)
     * u3: Intensifier High-Pressure Actuation Spool [%] (0 to 100%)
     * u4: Cavity Vacuum Assist Proportional Throttle Valve [%] (0 to 100%)
     * u5: Main Clamping Force Hydraulic Line Pressure [bar] (0 to 350 bar)
     * u6: Die Thermal Channel Total Cooling Flow Rate [%] (0 to 100%)
     * ================================================================================================================= *)
    rMatrix_A                    : ARRAY[1..8, 1..8] OF REAL;  (* System Dynamics Discrete State Transition Matrix A *)
    rMatrix_B                    : ARRAY[1..8, 1..6] OF REAL;  (* Actuator Input Coupling Matrix B *)
    rMatrix_Ew                   : ARRAY[1..8, 1..3] OF REAL;  (* Exogenous Disturbance Coupling Matrix Ew *)
    rMatrix_C                    : ARRAY[1..6, 1..8] OF REAL;  (* Sensor Output Observation Matrix C *)
    rMatrix_D                    : ARRAY[1..6, 1..6] OF REAL;  (* Direct Feedthrough Transmission Matrix D *)
    rMatrix_K_Kalman             : ARRAY[1..8, 1..6] OF REAL;  (* Steady-State Optimal Kalman Observer Gain Matrix K *)

    rVec_x_State                 : ARRAY[1..8] OF REAL;        (* Current Estimated State Vector x[k] *)
    rVec_x_Next                  : ARRAY[1..8] OF REAL;        (* Propagated State Vector Prediction x[k+1] *)
    rVec_x_Corrected             : ARRAY[1..8] OF REAL;        (* Innovation Corrected State Vector x_hat[k|k] *)
    rVec_u_Control               : ARRAY[1..6] OF REAL;        (* Control Input Vector u[k] *)
    rVec_u_Previous              : ARRAY[1..6] OF REAL;        (* Previous Cycle Control Vector u[k-1] *)
    rVec_y_Estimated             : ARRAY[1..6] OF REAL;        (* Model Estimated Output Vector y_hat[k] *)
    rVec_y_Measured              : ARRAY[1..6] OF REAL;        (* Filtered Sensor Output Vector y[k] *)
    rVec_y_Residual              : ARRAY[1..6] OF REAL;        (* Innovation Residual Vector e_y = y - y_hat *)
    rVec_w_Disturbance           : ARRAY[1..3] OF REAL;        (* Estimated Exogenous Disturbances (viscosity, leak, flow) *)

    (* --- State-Space Initialization and Matrix Check Flags --- *)
    bStateSpace_Initialized      : BOOL := FALSE;              (* One-Shot Matrix Cold-Start Initialization Latch *)
    iRow_Idx                     : INT;                        (* Matrix Math Outer Row Loop Index *)
    iCol_Idx                     : INT;                        (* Matrix Math Inner Column Loop Index *)
    iInner_Idx                   : INT;                        (* Matrix Multiplication Accumulator Index *)
    rMatMul_Sum                  : REAL;                       (* Real Accumulator for Dot Product Computations *)

    (* =================================================================================================================
     * SECTION 2: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT (PGD)
     * Quadratic Cost Function: J = sum((y - r)^T * Q * (y - r) + u^T * R * u + du^T * S * du)
     * Horizon: Np = 5 prediction steps, Nc = 3 control steps. Unrolled 6-iteration PGD solver.
     * ================================================================================================================= *)
    rMPC_Weight_Q                : ARRAY[1..6] OF REAL;        (* Output Error Tracking Penalty Weights Q *)
    rMPC_Weight_R                : ARRAY[1..6] OF REAL;        (* Control Effort Magnitude Penalty Weights R *)
    rMPC_Weight_S                : ARRAY[1..6] OF REAL;        (* Control Rate-of-Change (Slew) Penalty Weights S *)

    rVec_r_Reference             : ARRAY[1..6] OF REAL;        (* Real-Time Dynamic Setpoint Trajectory r[k] *)
    rVec_u_Optimized             : ARRAY[1..6] OF REAL;        (* PGD Optimal Solution Candidate Vector *)
    rVec_u_Gradient              : ARRAY[1..6] OF REAL;        (* Analytically Computed Cost Function Gradient dJ/du *)
    rVec_u_MinLimit              : ARRAY[1..6] OF REAL;        (* Lower Actuator Saturation Hard Boundaries *)
    rVec_u_MaxLimit              : ARRAY[1..6] OF REAL;        (* Upper Actuator Saturation Hard Boundaries *)
    rVec_du_MaxRate              : ARRAY[1..6] OF REAL;        (* Maximum Allowable Slew Rate Limit Per Millisecond *)

    rMPC_StepSize_Alpha          : REAL := 0.045;              (* PGD Line Search Gradient Descent Step Size *)
    rMPC_Cost_Total              : REAL;                       (* Evaluated Total Quadratic Objective Function Cost *)
    rMPC_Cost_Tracking           : REAL;                       (* Error Tracking Cost Contribution *)
    rMPC_Cost_Effort             : REAL;                       (* Actuator Energy Cost Contribution *)
    rMPC_Cost_Slew               : REAL;                       (* Rate-of-Change Jerk Cost Contribution *)
    iMPC_Iteration               : INT;                        (* Unrolled PGD Optimization Loop Counter *)
    iMPC_Actuator                : INT;                        (* Actuator Variable Index for Gradient Step *)

    (* =================================================================================================================
     * SECTION 3: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT MANAGEMENT DATA STRUCTURES
     * Redundant acquisition, median voting, discrepancy timers, and bumpless single/dual degradation
     * ================================================================================================================= *)
    (* Channel 1: PT-101 Injection Cylinder Head Pressure *)
    rTMR_PT101_Voted             : REAL;                       (* Voted Output Pressure [bar] *)
    rTMR_PT101_DevAB             : REAL;                       (* Absolute Deviation Channel A to B [bar] *)
    rTMR_PT101_DevBC             : REAL;                       (* Absolute Deviation Channel B to C [bar] *)
    rTMR_PT101_DevCA             : REAL;                       (* Absolute Deviation Channel C to A [bar] *)
    rTMR_PT101_TimerA            : REAL := 0.0;                (* Channel A Discrepancy Millisecond Accumulator [ms] *)
    rTMR_PT101_TimerB            : REAL := 0.0;                (* Channel B Discrepancy Millisecond Accumulator [ms] *)
    rTMR_PT101_TimerC            : REAL := 0.0;                (* Channel C Discrepancy Millisecond Accumulator [ms] *)
    bTMR_PT101_HealthyA          : BOOL := TRUE;               (* Transducer 101A Operational Health Status *)
    bTMR_PT101_HealthyB          : BOOL := TRUE;               (* Transducer 101B Operational Health Status *)
    bTMR_PT101_HealthyC          : BOOL := TRUE;               (* Transducer 101C Operational Health Status *)
    iTMR_PT101_DegradeMode       : INT := 3;                   (* 3 = 2oo3 Active, 2 = 1oo2 Degraded, 1 = Single, 0 = Fail *)

    (* Channel 2: PT-201 Injection Cylinder Rod Pressure *)
    rTMR_PT201_Voted             : REAL;                       (* Voted Output Rod Pressure [bar] *)
    rTMR_PT201_DevAB             : REAL;
    rTMR_PT201_DevBC             : REAL;
    rTMR_PT201_DevCA             : REAL;
    rTMR_PT201_TimerA            : REAL := 0.0;
    rTMR_PT201_TimerB            : REAL := 0.0;
    rTMR_PT201_TimerC            : REAL := 0.0;
    bTMR_PT201_HealthyA          : BOOL := TRUE;
    bTMR_PT201_HealthyB          : BOOL := TRUE;
    bTMR_PT201_HealthyC          : BOOL := TRUE;
    iTMR_PT201_DegradeMode       : INT := 3;

    (* Channel 3: ENC-301 Plunger Absolute Optical Position *)
    rTMR_ENC301_Voted            : REAL;                       (* Voted Optical Linear Position [mm] *)
    rTMR_ENC301_DevAB            : REAL;
    rTMR_ENC301_DevBC            : REAL;
    rTMR_ENC301_DevCA            : REAL;
    rTMR_ENC301_TimerA           : REAL := 0.0;
    rTMR_ENC301_TimerB           : REAL := 0.0;
    rTMR_ENC301_TimerC           : REAL := 0.0;
    bTMR_ENC301_HealthyA         : BOOL := TRUE;
    bTMR_ENC301_HealthyB         : BOOL := TRUE;
    bTMR_ENC301_HealthyC         : BOOL := TRUE;
    iTMR_ENC301_DegradeMode      : INT := 3;

    (* Channel 4: VPT-401 Die Cavity Absolute Vacuum *)
    rTMR_VPT401_Voted            : REAL;                       (* Voted Cavity Absolute Vacuum Pressure [mbar] *)
    rTMR_VPT401_DevAB            : REAL;
    rTMR_VPT401_DevBC            : REAL;
    rTMR_VPT401_DevCA            : REAL;
    rTMR_VPT401_TimerA           : REAL := 0.0;
    rTMR_VPT401_TimerB           : REAL := 0.0;
    rTMR_VPT401_TimerC           : REAL := 0.0;
    bTMR_VPT401_HealthyA         : BOOL := TRUE;
    bTMR_VPT401_HealthyB         : BOOL := TRUE;
    bTMR_VPT401_HealthyC         : BOOL := TRUE;
    iTMR_VPT401_DegradeMode      : INT := 3;

    (* Channel 5: PT-501 High-Pressure Accumulator *)
    rTMR_PT501_Voted             : REAL;                       (* Voted Accumulator Pressure [bar] *)
    rTMR_PT501_DevAB             : REAL;
    rTMR_PT501_DevBC             : REAL;
    rTMR_PT501_DevCA             : REAL;
    rTMR_PT501_TimerA            : REAL := 0.0;
    rTMR_PT501_TimerB            : REAL := 0.0;
    rTMR_PT501_TimerC            : REAL := 0.0;
    bTMR_PT501_HealthyA          : BOOL := TRUE;
    bTMR_PT501_HealthyB          : BOOL := TRUE;
    bTMR_PT501_HealthyC          : BOOL := TRUE;
    iTMR_PT501_DegradeMode       : INT := 3;

    (* Channel 6: LC-601 Main Clamping Force Load Cells *)
    rTMR_LC601_Voted             : REAL;                       (* Voted Total Locking Tonnage [kN] *)
    rTMR_LC601_DevAB             : REAL;
    rTMR_LC601_DevBC             : REAL;
    rTMR_LC601_DevCA             : REAL;
    rTMR_LC601_TimerA            : REAL := 0.0;
    rTMR_LC601_TimerB            : REAL := 0.0;
    rTMR_LC601_TimerC            : REAL := 0.0;
    bTMR_LC601_HealthyA          : BOOL := TRUE;
    bTMR_LC601_HealthyB          : BOOL := TRUE;
    bTMR_LC601_HealthyC          : BOOL := TRUE;
    iTMR_LC601_DegradeMode       : INT := 3;

    (* Channel 7: TT-701 Shot Sleeve Melt Temperature *)
    rTMR_TT701_Voted             : REAL;                       (* Voted Pouring Temperature [deg C] *)
    rTMR_TT701_DevAB             : REAL;
    rTMR_TT701_DevBC             : REAL;
    rTMR_TT701_DevCA             : REAL;
    rTMR_TT701_TimerA            : REAL := 0.0;
    rTMR_TT701_TimerB            : REAL := 0.0;
    rTMR_TT701_TimerC            : REAL := 0.0;
    bTMR_TT701_HealthyA          : BOOL := TRUE;
    bTMR_TT701_HealthyB          : BOOL := TRUE;
    bTMR_TT701_HealthyC          : BOOL := TRUE;
    iTMR_TT701_DegradeMode       : INT := 3;

    (* Calibrated Discrepancy Tolerances and Trip Times *)
    rTMR_Tol_Pres_PT101          : REAL := 12.0;               (* Head Pressure Deviation Limit [bar] *)
    rTMR_Tol_Pres_PT201          : REAL := 12.0;               (* Rod Pressure Deviation Limit [bar] *)
    rTMR_Tol_Pos_ENC301          : REAL := 1.8;                (* Linear Encoder Deviation Limit [mm] *)
    rTMR_Tol_Vac_VPT401          : REAL := 25.0;               (* Vacuum Transducer Deviation Limit [mbar] *)
    rTMR_Tol_Accum_PT501         : REAL := 15.0;               (* Accumulator Deviation Limit [bar] *)
    rTMR_Tol_Clamp_LC601         : REAL := 1200.0;             (* Clamping Load Cell Deviation Limit [kN] *)
    rTMR_Tol_Temp_TT701          : REAL := 22.0;               (* Shot Sleeve Temp Deviation Limit [deg C] *)
    rTMR_Discrepancy_Limit_ms    : REAL := 50.0;               (* Max Discrepancy Duration Before Channel Trip [ms] *)

    (* =================================================================================================================
     * SECTION 4: KINEMATICS, HYDROSTATICS & FLUID DYNAMICS CALCULATION VARIABLES
     * Plunger velocity derivation, digital filtering, metal pressure transformation, gating hydraulics
     * ================================================================================================================= *)
    rPlungerPos_Prev             : REAL := 0.0;                (* Plunger Position at Previous Scan [mm] *)
    rPlungerPos_Prev2            : REAL := 0.0;                (* Plunger Position 2 Scans Ago [mm] *)
    rRawVelocity                 : REAL := 0.0;                (* Backward Difference Raw Plunger Velocity [m/s] *)
    rFiltVelocity                : REAL := 0.0;                (* Butterworth 2nd Order Filtered Velocity [m/s] *)
    rFiltVel_z1                  : REAL := 0.0;                (* Filter State Delay z^-1 [m/s] *)
    rFiltVel_z2                  : REAL := 0.0;                (* Filter State Delay z^-2 [m/s] *)
    rRawAcceleration             : REAL := 0.0;                (* Plunger Axial Acceleration [m/s^2] *)
    rPeakVelocityRecorded        : REAL := 0.0;                (* Latched Maximum Phase 2 Injection Velocity [m/s] *)

    (* Hydraulic Cylinder Geometric Constants *)
    rCylHead_Diameter_m          : REAL := 0.320;              (* Shot Cylinder Bore Diameter (320 mm) [m] *)
    rCylRod_Diameter_m           : REAL := 0.180;              (* Shot Cylinder Rod Diameter (180 mm) [m] *)
    rPlunger_Diameter_m          : REAL := 0.160;              (* Plunger Tip Diameter (160 mm) [m] *)
    rCylHead_Area_m2             : REAL;                       (* Computed Piston Head Area [m2] *)
    rCylRod_Area_m2              : REAL;                       (* Computed Piston Rod Area [m2] *)
    rPlunger_Area_m2             : REAL;                       (* Computed Plunger Tip Area [m2] *)
    rIntensifier_Multiplier      : REAL := 3.25;               (* Intensifier Hydraulic Amplification Ratio *)

    (* Hydrostatic Forces and Specific Metal Pressures *)
    rForce_Head_kN               : REAL;                       (* Forward Hydraulic Thrust Force [kN] *)
    rForce_Rod_kN                : REAL;                       (* Opposing Rod Chamber Hydraulic Force [kN] *)
    rForce_Net_kN                : REAL;                       (* Net Mechanical Injection Force [kN] *)
    rSpecificMetalPres_bar       : REAL;                       (* Effective Metal Pressure on Solidifying Alloy [bar] *)
    rPeakIntensPresRecorded      : REAL := 0.0;                (* Latched Peak Specific Metal Pressure [bar] *)
    rIntensRiseTimer_ms          : REAL := 0.0;                (* Intensification Dynamic Rise Time Counter [ms] *)
    bIntensRiseTimer_Active      : BOOL := FALSE;              (* Flag Indicating Rise Time Measurement in Progress *)
    rIntensRiseTimeAchieved_ms   : REAL := 0.0;                (* Latched Pressure Rise Duration [ms] *)

    (* Fluid Dynamics: Gating & Wave Crest Suppression (Phase 1) *)
    rIngate_Area_m2              : REAL := 0.00145;            (* Ingate Cross-Sectional Throttle Area (1450 mm2) [m2] *)
    rIngate_Velocity_ms          : REAL;                       (* Ingate Molten Aluminum Flow Velocity [m/s] *)
    rSleeve_Fill_Ratio           : REAL := 0.42;               (* Shot Sleeve Volumetric Fill Fraction (42%) *)
    rCritical_Wave_Velocity_ms   : REAL;                       (* Critical Plunger Speed to Prevent Wave Breaking [m/s] *)
    rCavity_Volume_m3            : REAL := 0.0185;             (* Total Cavity + Overflow Casting Volume (18.5 L) [m3] *)
    rTheoretical_FillTime_ms     : REAL;                       (* Computed Cavity Fill Duration at Phase 2 Speed [ms] *)

    (* Tie-Bar Structural Balance & Dynamic Parallelism *)
    rTieBar_AvgStrain            : REAL;                       (* Mean Column Strain Extensometer Reading [um] *)
    rTieBar_MaxEccentricity      : REAL;                       (* Maximum Dynamic Platen Tilt Angular Deflection [um] *)
    bTieBar_TonnageImbalance     : BOOL := FALSE;              (* Platen Angular Skew Fault Interlock *)

    (* Biscuit Measurement & Geometry *)
    rBiscuit_Thickness_mm        : REAL := 0.0;                (* Computed Solidified Biscuit Length [mm] *)
    rMachine_Full_Stroke_mm      : REAL := 1250.0;             (* Total Mechanical Shot Stroke Limit [mm] *)

    (* =================================================================================================================
     * SECTION 5: MULTI-ZONE THERMAL DIE BALANCING SUBSYSTEM (12 INDEPENDENT CHANNELS)
     * High-pressure oil/pressurized water thermo-regulators with anti-windup PID and PWM solenoid control
     * ================================================================================================================= *)
    rDieTemp_Current             : ARRAY[1..12] OF REAL;       (* Acquired Zone Steel Temperatures [deg C] *)
    rDieTemp_Setpoint            : ARRAY[1..12] OF REAL;       (* Recipe Target Equilibrium Temperatures [deg C] *)
    rDieTemp_Error               : ARRAY[1..12] OF REAL;       (* Current Temperature Error [deg C] *)
    rDieTemp_Integral            : ARRAY[1..12] OF REAL;       (* Anti-Windup Integral Error Accumulator *)
    rDieTemp_Derivative          : ARRAY[1..12] OF REAL;       (* Rate of Temperature Rise/Fall [deg C/s] *)
    rDieTemp_Prev                : ARRAY[1..12] OF REAL;       (* Previous Cycle Zone Temperature [deg C] *)
    rDieCooling_DutyCycle        : ARRAY[1..12] OF REAL;       (* Calculated Solenoid Duty Cycle (0 to 100%) *)
    rDieHeatExtracted_kW         : ARRAY[1..12] OF REAL;       (* Computed Thermal Energy Extraction Rate [kW] *)

    (* Thermal PID Gains per Channel *)
    rPID_Kp                      : ARRAY[1..12] OF REAL;       (* Proportional Thermal Gain *)
    rPID_Ki                      : ARRAY[1..12] OF REAL;       (* Integral Thermal Reset Gain *)
    rPID_Kd                      : ARRAY[1..12] OF REAL;       (* Derivative Rate Action Gain *)
    iPWM_CycleCounter_ms         : INT := 0;                   (* 1000 ms Base Pulse-Width Modulation Counter *)
    iZone_Loop                   : INT;                        (* Multi-Zone Loop Processing Index *)

    (* =================================================================================================================
     * SECTION 6: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
     * Sequential execution of 4,000-ton gigacasting machine cycle
     * ================================================================================================================= *)
    iFSM_CurrentState            : INT := 0;                   (* Current Operational Machine State *)
    iFSM_NextState               : INT := 0;                   (* Evaluated Next Sequential Machine State *)
    iFSM_PreviousState           : INT := 0;                   (* Prior Operational State for Tracking *)
    rFSM_StateTimer_s            : REAL := 0.0;                (* High-Resolution State Duration Stopwatch [s] *)
    bFSM_StateFirstScan          : BOOL := TRUE;               (* One-Shot State Entry Trigger Flag *)

    (* State Numeric Identifiers *)
    (*  0: STATE_00_IDLE_SAFETY_INTERLOCK
     *  1: STATE_01_DIE_LOCKUP_TONNAGE_BUILD
     *  2: STATE_02_LADLE_ROBOTIC_POUR
     *  3: STATE_03_BISCUIT_SLOW_SHOT_PHASE1
     *  4: STATE_04_VACUUM_EVACUATION_PUMP
     *  5: STATE_05_HIGH_SPEED_INJECTION_PHASE2
     *  6: STATE_06_INTENSIFICATION_HOLD_PHASE3
     *  7: STATE_07_SOLIDIFICATION_COOLING
     *  8: STATE_08_VACUUM_VENT_EQUALIZATION
     *  9: STATE_09_CORE_SLIDE_RETRACT
     * 10: STATE_10_DIE_DECLAMP_AND_OPEN
     * 11: STATE_11_HYDRAULIC_EJECTOR_KNOCKOUT
     * 12: STATE_12_ROBOT_EXTRACT_PERMISSIVE
     * 13: STATE_13_DIE_SPRAY_LUBRICATION_AIR_PURGE
     * 14: STATE_14_EMERGENCY_DUMP_FAILSAFE *)

    rTotalCycleTimer_s           : REAL := 0.0;                (* Total Elapsed Production Cycle Timer [s] *)
    bCycleRunning                : BOOL := FALSE;              (* Casting Cycle in Active Progress *)
    rSprayTimer_s                : REAL := 0.0;                (* Lubrication Spray Cycle Elapsed Time [s] *)
    rEvacuationTimer_s           : REAL := 0.0;                (* Vacuum Evacuation Dwell Timer [s] *)
    rSolidifyTimer_s             : REAL := 0.0;                (* Solidification Dwell Timer [s] *)
    rEjectTimer_s                : REAL := 0.0;                (* Hydraulic Ejector Pin Motion Timer [s] *)

    (* =================================================================================================================
     * SECTION 7: STATISTICAL PROCESS CONTROL (SPC) & QUALITY VERIFICATION ARRAYS
     * Rolling circular buffers (N = 30 shots) for Cp, Cpk, Mean, and Standard Deviation monitoring
     * ================================================================================================================= *)
    arrSPC_Biscuit_History       : ARRAY[1..30] OF REAL;       (* Historical Solidified Biscuit Thicknesses [mm] *)
    arrSPC_PeakVel_History       : ARRAY[1..30] OF REAL;       (* Historical Peak Shot Velocities [m/s] *)
    arrSPC_RiseTime_History      : ARRAY[1..30] OF REAL;       (* Historical Intensification Rise Times [ms] *)
    arrSPC_PeakPres_History      : ARRAY[1..30] OF REAL;       (* Historical Intensification Peak Pressures [bar] *)

    iSPC_ShotCount               : INT := 0;                   (* Total Lifetime Produced Castings Counter *)
    iSPC_BufferIndex             : INT := 1;                   (* Circular History Buffer Pointer (1 to 30) *)
    iSPC_Loop                    : INT;                        (* Statistical Computation Loop Iterator *)

    rSPC_Biscuit_Mean            : REAL := 25.0;               (* Sample Mean Biscuit Thickness [mm] *)
    rSPC_Biscuit_Variance        : REAL := 0.0;                (* Sample Variance of Biscuit Thickness *)
    rSPC_Biscuit_StdDev          : REAL := 0.5;                (* Standard Deviation (Sigma) of Biscuit [mm] *)
    rSPC_Biscuit_Cp              : REAL := 1.5;                (* Process Capability Index Cp *)
    rSPC_Biscuit_Cpk             : REAL := 1.4;                (* Lower Process Capability Index Cpk *)

    rSPC_PeakVel_Mean            : REAL := 7.5;                (* Mean Fast Shot Velocity [m/s] *)
    rSPC_PeakVel_StdDev          : REAL := 0.15;               (* Velocity Standard Deviation [m/s] *)

    rSPC_RiseTime_Mean           : REAL := 12.0;               (* Mean Intensification Rise Time [ms] *)
    rSPC_RiseTime_StdDev         : REAL := 1.2;                (* Rise Time Standard Deviation [ms] *)

    (* Customer Engineering Specifications *)
    rSpec_Biscuit_USL            : REAL := 32.0;               (* Upper Specification Limit for Biscuit [mm] *)
    rSpec_Biscuit_LSL            : REAL := 18.0;               (* Lower Specification Limit for Biscuit [mm] *)
    rSpec_RiseTime_Max           : REAL := 18.0;               (* Maximum Allowable Pressure Rise Time [ms] *)
    rSpec_PeakPres_Min           : REAL := 720.0;              (* Minimum Permissible Squeeze Pressure [bar] *)
    rSpec_Vacuum_Max             : REAL := 60.0;               (* Maximum Permissible Cavity Pressure [mbar] *)

    (* =================================================================================================================
     * SECTION 8: ISA-18.2 MULTI-TIER ALARM ENGINE & BIT-PACKED TELEMETRY VARIABLES
     * Trip limits, deadbands, first-out latching, priority classification
     * ================================================================================================================= *)
    (* Alarm Trip Limits *)
    rLim_PT101_HH                : REAL := 320.0;              (* Shot Head Pressure High-High Trip [bar] *)
    rLim_PT101_H                 : REAL := 290.0;              (* Shot Head Pressure High Warning [bar] *)
    rLim_PT101_L                 : REAL := 20.0;               (* Shot Head Pressure Low Warning [bar] *)
    rLim_PT101_LL                : REAL := 5.0;                (* Shot Head Pressure Low-Low Trip [bar] *)

    rLim_PT501_Accum_L           : REAL := 220.0;              (* Accumulator Charge Pressure Low Warning [bar] *)
    rLim_PT501_Accum_LL          : REAL := 180.0;              (* Accumulator Charge Pressure Low-Low Abort [bar] *)

    rLim_Vel_HH                  : REAL := 11.5;               (* Plunger Velocity High-High Flashing Trip [m/s] *)
    rLim_Vel_LL                  : REAL := 0.05;               (* Plunger Stiction Stall Trip [m/s] *)

    rLim_DieTemp_HH              : REAL := 360.0;              (* Die Steel Overheat Hot Spot Alarm [deg C] *)
    rLim_DieTemp_LL              : REAL := 140.0;              (* Die Steel Cold Shut Warning [deg C] *)

    rAlarm_Deadband_Pres         : REAL := 3.0;                (* Hydraulic Pressure Clearance Deadband [bar] *)
    rAlarm_Deadband_Temp         : REAL := 4.0;                (* Temperature Clearance Deadband [deg C] *)

    (* Alarm Discrete Flags *)
    bAlarm_HeadPres_HH           : BOOL := FALSE;
    bAlarm_HeadPres_H            : BOOL := FALSE;
    bAlarm_HeadPres_L            : BOOL := FALSE;
    bAlarm_HeadPres_LL           : BOOL := FALSE;
    bAlarm_AccumPres_LowTrip     : BOOL := FALSE;
    bAlarm_Velocity_Overshoot    : BOOL := FALSE;
    bAlarm_Intens_TooSlow        : BOOL := FALSE;
    bAlarm_Vacuum_NotAchieved    : BOOL := FALSE;
    bAlarm_Biscuit_OutRange      : BOOL := FALSE;
    bAlarm_TieBar_Eccentricity   : BOOL := FALSE;
    bAlarm_EmergencyStop_Active  : BOOL := FALSE;
    bAlarm_SafetyGate_Open       : BOOL := FALSE;
    bAlarm_TMR_MajorDegrade      : BOOL := FALSE;
    bAlarm_Die_HotSpot           : BOOL := FALSE;

    (* Telemetry 32-Bit Bit-Packing Registers *)
    dwReg_FSM                    : DWORD := 16#00000000;
    dwReg_Motion                 : DWORD := 16#00000000;
    dwReg_CritTrip               : DWORD := 16#00000000;
    dwReg_Warning                : DWORD := 16#00000000;
    dwReg_TMRHealth              : DWORD := 16#00000000;
    dwReg_Quality                : DWORD := 16#00000000;

END_VAR
"""
