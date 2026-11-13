# Header and VAR blocks for FB_PulpPaper_Fourdrinier_Headbox_SliceLip_BasisWeight

def generate_iec_code():
    parts = []

    # Opening declaration
    parts.append("FUNCTION_BLOCK FB_PulpPaper_Fourdrinier_Headbox_SliceLip_BasisWeight\n")

    # Header comments
    header_comment = """(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: PULP, PAPER & CONTINUOUS WEB PROCESSING
SYSTEM: 1,800 [m/min] HIGH-SPEED FOURDRINIER PAPER MACHINE HYDRAULIC HEADBOX
ACTUATION: 64 CROSS-DIRECTION THERMAL MICRO-EXPANSION SLICE LIP SPINDLES & JET-TO-WIRE SYNC
SUBSYSTEMS:
  - HYDRAULIC HEADBOX WITH PRESSURIZED COMPRESSED AIR CUSHION / ATTENUATION DAMPER
  - TOTAL HEAD EQUATION: H_total = P_air / (rho_stock * g) + h_liquid [mm H2O]
  - TORRICELLI-BERNOULLI SLICE JET EXIT VELOCITY: v_jet = C_discharge * SQRT(2 * g * H_total) [m/min]
  - JET-TO-WIRE SPEED RATIO CONTROL: J_W = v_jet / v_wire OPTIMIZED AT 1.025 [-]
  - 64 CROSS-DIRECTION (CD) THERMAL MICRO-EXPANSION SLICE LIP SPINDLE ACTUATORS
  - TOEPLITZ / GAUSSIAN SPATIAL CROSS-COUPLING ATTENUATION MATRIX: Delta_w = G * Delta_u_slice
  - MECHANICAL SLICE LIP BENDING MOMENT & CURVATURE CONSTRAINTS (PREVENT BEAM PLASTIC BUCKLING)
  - 6-STATE FIRST-PRINCIPLES DISCRETE CYBER-PHYSICAL STATE-SPACE OBSERVER (Ts = 0.010 [s])
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH 10 UNROLLED PROJECTED GRADIENT DESCENT (PGD)
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ACROSS 4 PROCESS CHANNELS (PERSISTENCE 150 [ms])
  - DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM STATES 0 TO 13)
  - ISA-18.2 MULTI-TIER PROCESS ALARMS (HH, H, L, LL) WITH DEADBAND HYSTERESIS & 32-BIT TELEMETRY
====================================================================================================
*)
"""
    parts.append(header_comment)

    # VAR_INPUT
    var_input = """VAR_INPUT
    (* Master Execution Controls & Machine Permissives *)
    bEnable                         : BOOL;         (* Master Function Block Execution Enable Command [-] *)
    bAutoCycleStart                 : BOOL;         (* Automatic Sequence Start Permissive [-] *)
    bMachineStop                    : BOOL;         (* Controlled Paper Machine Ramp-Down Stop Command [-] *)
    bEmergencyStop                  : BOOL;         (* Safety Cat-4 Hardwired Emergency Master Trip [-] *)
    bFaultReset                     : BOOL;         (* Latched Diagnostic Fault & Alarm Pushbutton Reset [-] *)
    bAlarmAck                       : BOOL;         (* ISA-18.2 Alarm Silence & Acknowledge Command [-] *)
    bMpcEnable                      : BOOL;         (* Receding-Horizon Model Predictive Controller Master Enable [-] *)
    bCdControlEnable                : BOOL;         (* 64-Zone Cross-Direction Basis Weight Profiler Enable [-] *)
    bGradeChangeCmd                 : BOOL;         (* Online High-Speed Grade Change Transition Initiation [-] *)
    bSheetBreakDetected             : BOOL;         (* Optical Wire Sheet Break Fast Detector Interlock [-] *)
    bCleanInPlaceCmd                : BOOL;         (* Post-Run Acid/Caustic Chemical CIP Washdown Trigger [-] *)
    bFanPumpReady                   : BOOL;         (* Primary White Water Fan Pump VFD Skid Running & Permissive [-] *)
    bAirCompressorReady             : BOOL;         (* Compressed Air Cushion Header Supply Pressurized & Ready [-] *)
    bWireDriveRunning               : BOOL;         (* Fourdrinier Wire Section Multi-Drive Section Running [-] *)
    bWhiteWaterFlushPermissive      : BOOL;         (* Deaerated White Water Header Supply Valve Permissive [-] *)

    (* Channel Group 1: Triplicated Total Head Piezoresistive Pressure Transmitters (2oo3 TMR) *)
    rHeadPress_1A_kPa               : REAL;         (* Total Head Hydraulic Pressure Transmitter Ch 1A [kPa] *)
    rHeadPress_1B_kPa               : REAL;         (* Total Head Hydraulic Pressure Transmitter Ch 1B [kPa] *)
    rHeadPress_1C_kPa               : REAL;         (* Total Head Hydraulic Pressure Transmitter Ch 1C [kPa] *)

    (* Channel Group 2: Triplicated Stock Pond Microwave/Radar Level Sensors (2oo3 TMR) *)
    rPondLevel_2A_mm                : REAL;         (* Stock Pond Free Surface Radar Level Transmitter Ch 2A [mm] *)
    rPondLevel_2B_mm                : REAL;         (* Stock Pond Free Surface Radar Level Transmitter Ch 2B [mm] *)
    rPondLevel_2C_mm                : REAL;         (* Stock Pond Free Surface Radar Level Transmitter Ch 2C [mm] *)

    (* Channel Group 3: Triplicated Dilution Profiling Header Electromagnetic Flowmeters (2oo3 TMR) *)
    rDilutionFlow_3A_m3h            : REAL;         (* Dilution Profiling White Water Header Flowmeter Ch 3A [m3/h] *)
    rDilutionFlow_3B_m3h            : REAL;         (* Dilution Profiling White Water Header Flowmeter Ch 3B [m3/h] *)
    rDilutionFlow_3C_m3h            : REAL;         (* Dilution Profiling White Water Header Flowmeter Ch 3C [m3/h] *)

    (* Channel Group 4: Triplicated Forming Wire Optical Encoder Speed Sensors (2oo3 TMR) *)
    rWireSpeed_4A_mpmin             : REAL;         (* Forming Wire Section Optical Speed Encoder Ch 4A [m/min] *)
    rWireSpeed_4B_mpmin             : REAL;         (* Forming Wire Section Optical Speed Encoder Ch 4B [m/min] *)
    rWireSpeed_4C_mpmin             : REAL;         (* Forming Wire Section Optical Speed Encoder Ch 4C [m/min] *)

    (* Pulp Stock Physics, Slurry Thermodynamics & Physical Properties *)
    rStockConsistency_Inlet_pct     : REAL;         (* Approach Flow Fiber Slurry Mass Consistency [%] *)
    rStockDensity_kgm3              : REAL;         (* Stock Slurry Bulk Density in Headbox Pond [kg/m3] *)
    rStockTemperature_degC          : REAL;         (* Fiber Stock Slurry Flow Temperature [deg C] *)
    rStockFreeness_CSF_ml           : REAL;         (* Canadian Standard Freeness Drainage Metric [ml] *)
    rAirPadPressure_Direct_kPa      : REAL;         (* Direct Air Cushion Pressure Vessel Sensor [kPa] *)

    (* Actuator Physical Position & Velocity Feedbacks *)
    rFanPump_SpeedFb_pct            : REAL;         (* Primary Fan Pump Motor Variable Frequency Drive Speed Fb [%] *)
    rAirChargeValve_PosFb_pct       : REAL;         (* Compressed Air Cushion Proportional Inflow Valve Pos Fb [%] *)
    rAirBleedValve_PosFb_pct        : REAL;         (* Compressed Air Cushion Proportional Bleed Vent Valve Pos Fb [%] *)
    rSliceLipMean_PosFb_mm          : REAL;         (* Overall Slice Lip Mechanical Spindle Mean Gap Pos Fb [mm] *)
    rDilutionHeaderValve_PosFb_pct  : REAL;         (* Dilution Profiling Main Header Control Valve Pos Fb [%] *)
    rStockOverflow_PosFb_pct        : REAL;         (* Stock Pond Recirculation Overflow Return Valve Pos Fb [%] *)

    (* Machine Production Setpoints & Dynamic Target References *)
    rTarget_JetToWireRatio          : REAL;         (* Target Jet-to-Wire Speed Ratio Reference (Nominal 1.025) [-] *)
    rTarget_BasisWeight_gpm2        : REAL;         (* Target Bone-Dry Finished Paper Web Basis Weight [g/m2] *)
    rTarget_PondLevel_mm            : REAL;         (* Target Stock Pond Liquid Free Surface Level Reference [mm] *)
    rTarget_TotalHead_mmH2O         : REAL;         (* Target Total Hydraulic Head Pressure Reference [mm H2O] *)
    rTarget_WireSpeed_mpmin         : REAL;         (* Target Forming Wire Machine Speed Reference [m/min] *)
    rTarget_Consistency_gpL         : REAL;         (* Target Fiber Consistency in Headbox Chamber [g/L] *)

    (* 64-Zone Cross-Direction (CD) Quality Control System (QCS) Scanner Profile Inputs *)
    arrScanner_BasisWeight_gpm2     : ARRAY[1..64] OF REAL; (* 64 CD Transverse Basis Weight Scanner Profile [g/m2] *)
    bScannerDataValid               : BOOL;         (* QCS Scanner Cross-Direction Profile Array Valid Signal [-] *)
    rScannerScanTime_s              : REAL;         (* QCS Scanner Full Cross-Machine Single Traverse Period [s] *)
    arrThermalHeater_TempFb_degC    : ARRAY[1..64] OF REAL; (* 64 Thermal Expansion Spindle Core Temperature Fb [deg C] *)
END_VAR
"""
    parts.append(var_input)

    # VAR_OUTPUT
    var_output = """VAR_OUTPUT
    (* Modulating Process Control Actuator Commands *)
    rFanPump_SpeedCmd_pct           : REAL;         (* Primary White Water Fan Pump VFD Speed Setpoint Command [%] *)
    rAirChargeValve_Cmd_pct         : REAL;         (* Compressed Air Cushion Charge Proportional Valve Command [%] *)
    rAirBleedValve_Cmd_pct          : REAL;         (* Compressed Air Cushion Bleed Vent Proportional Valve Command [%] *)
    rSliceLipMean_Cmd_mm            : REAL;         (* Main Slice Lip Mean Mechanical Opening Gap Command [mm] *)
    rDilutionHeaderValve_Cmd_pct    : REAL;         (* Dilution Profiling Total Header Control Valve Command [%] *)
    rStockOverflowValve_Cmd_pct     : REAL;         (* Stock Pond Recirculation Overflow Bypass Valve Command [%] *)
    rWhiteWaterFlushValve_Cmd_pct   : REAL;         (* Deaerator White Water System Flush Isolation Valve Command [%] *)

    (* Fast Discrete Auxiliary Solenoid & Protective Safety Commands *)
    bEmergencySlurryDivertValve     : BOOL;         (* Emergency Slurry Divert Gate to Wire Pit Couch Solenoid [-] *)
    bSliceLipProtectiveRetract      : BOOL;         (* Protective Slice Lip Actuator Fast Retract Solenoid [-] *)
    bFanPumpFastTrip                : BOOL;         (* Hardwired Digital Fan Pump Emergency Stop Interlock Trip [-] *)
    bAirPadFastDepressurize         : BOOL;         (* Fast Emergency Air Pad Depressurization Vent Solenoid [-] *)
    bWhiteWaterBypassValve          : BOOL;         (* White Water Startup Recirculation Bypass Diverter [-] *)

    (* 64 Cross-Direction (CD) Thermal Micro-Expansion Slice Lip Actuator Commands *)
    arrThermalHeater_PowerCmd_pct   : ARRAY[1..64] OF REAL; (* 64 Micro-Expansion Spindle Electrical Heating Power [%] *)
    arrSliceSpindle_EstGap_um       : ARRAY[1..64] OF REAL; (* 64 CD Slice Lip Local Micro-Gap Absolute Height [um] *)

    (* First-Principles Cyber-Physical Observer Estimated States *)
    rEst_TotalHead_mmH2O            : REAL;         (* Observer Estimated Total Hydraulic Head Pressure [mm H2O] *)
    rEst_PondLevel_mm               : REAL;         (* Observer Estimated Stock Pond Slurry Level [mm] *)
    rEst_JetWireDiff_mpmin          : REAL;         (* Observer Estimated Jet-to-Wire Speed Differential [m/min] *)
    rEst_MeanBasisWeight_gpm2       : REAL;         (* Observer Estimated Web Mean Basis Weight [g/m2] *)
    rEst_FiberConsistency_gpL       : REAL;         (* Observer Estimated Fiber Slurry Consistency [g/L] *)
    rEst_AirPadPressure_kPa         : REAL;         (* Observer Estimated Compressed Air Cushion Pad Pressure [kPa] *)

    (* Headbox Hydrodynamics & Machine Process Diagnostics *)
    rCalc_TotalHead_mmH2O           : REAL;         (* First-Principles Calculated Total Hydraulic Head [mm H2O] *)
    rCalc_JetVelocity_mpmin         : REAL;         (* Torricelli Slice Jet Exit Velocity [m/min] *)
    rCalc_JetToWireRatio            : REAL;         (* Actual Operating Jet-to-Wire Velocity Ratio [-] *)
    rCalc_MeanBasisWeight_gpm2      : REAL;         (* Mean Cross-Machine Web Basis Weight Calculation [g/m2] *)
    rCalc_Sigma_BasisWeight_gpm2    : REAL;         (* Cross-Machine Basis Weight Profile Standard Deviation [g/m2] *)
    rCalc_TwoSigma_Pct              : REAL;         (* 2-Sigma CD Basis Weight Variation Percentage [%] *)
    rCalc_MaxSliceCurvature_um      : REAL;         (* Peak Mechanical Slice Lip Beam Curvature Second Difference [um] *)
    rCalc_MaxAdjacentDelta_um       : REAL;         (* Maximum Adjacent Spindle Mechanical Differential [um] *)
    rMpc_QuadraticCostValue         : REAL;         (* Receding-Horizon MPC Quadratic Optimization Cost Metric [-] *)
    iActiveFsmState                 : INT;          (* Active Production Finite State Machine Operational Stage [0..13] *)

    (* 32-Bit Bit-Packed Telemetry & Diagnostic Status Words *)
    dwStatusWord1                   : DWORD;        (* Machine Operational State, Permissives & Subsystem Health Bits [-] *)
    dwStatusWord2                   : DWORD;        (* 2oo3 TMR Voting Health, CD Spindle Status & Observer Convergence [-] *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Critical Process Trips & Safety Interlocks (HH/LL) [-] *)
    dwAlarmWord2                    : DWORD;        (* ISA-18.2 Warning Deviations, Timers & Discrepancies (H/L) [-] *)
    dwFirstOutWord                  : DWORD;        (* First-Out Latching Root Cause Process Fault Identifier [-] *)
END_VAR
"""
    parts.append(var_output)

    # VAR
    var_internal = """VAR
    (* Execution Control, Scan Timing & Initialization Flags *)
    bFirstScanDone                  : BOOL := FALSE;    (* First Scan One-Shot Initialization Execution Flag [-] *)
    tScanCycleTime_s                : REAL := 0.010;    (* Discrete Task Execution Sample Period [s] *)
    iCycleCounter                   : DINT := 0;        (* Continuous Execution Scan Cycle Monotonic Counter [-] *)

    (* Physical & Hydraulic Constants *)
    rGravity_mps2                   : REAL := 9.80665;  (* Standard Acceleration of Gravity [m/s2] *)
    rDischargeCoeff                 : REAL := 0.982;    (* Slice Lip Fluid Discharge Contraction Coefficient [-] *)
    rSliceThermalAlpha              : REAL := 1.65E-5;  (* Micro-Expansion Spindle Thermal Expansion Alpha [1/K] *)
    rSpindleLength_mm               : REAL := 250.0;    (* Thermal Expansion Active Cartridge Spindle Length [mm] *)
    rSpindleThermalTau_s            : REAL := 45.0;     (* Thermal Expansion Spindle First-Order Thermal Time Constant [s] *)
    rSpindleHeaterGain_K_pct        : REAL := 0.85;     (* Steady-State Spindle Temperature Rise Per Percent Power [K/%] *)
    rAmbientTemp_degC               : REAL := 32.0;     (* Headbox Surroundings Ambient Air Dry-Bulb Temperature [deg C] *)

    (* 6x6 Discrete State-Space Cyber-Physical Matrices (Ts = 0.010 [s]) *)
    matA                            : ARRAY[0..5, 0..5] OF REAL; (* State Dynamic Transition Matrix A (6x6) [-] *)
    matB                            : ARRAY[0..5, 0..4] OF REAL; (* Actuator Control Mapping Matrix B (6x5) [-] *)
    matC                            : ARRAY[0..5, 0..5] OF REAL; (* Sensory Observation Output Matrix C (6x6) [-] *)
    matD                            : ARRAY[0..5, 0..4] OF REAL; (* Direct Feedthrough Matrix D (6x5) [-] *)
    matL                            : ARRAY[0..5, 0..5] OF REAL; (* Luenberger Observer Innovation Gain Matrix L (6x6) [-] *)

    (* State Vectors & Estimation Workspace Arrays *)
    vecX                            : ARRAY[0..5] OF REAL; (* Cyber-Physical Plant True Physical State Vector [-] *)
    vecX_hat                        : ARRAY[0..5] OF REAL; (* Luenberger Observer Filtered State Estimate Vector [-] *)
    vecX_pred                       : ARRAY[0..5] OF REAL; (* Observer One-Step-Ahead State Prediction Vector [-] *)
    vecY_meas                       : ARRAY[0..5] OF REAL; (* Voted Sensory Measurement Vector [-] *)
    vecY_hat                        : ARRAY[0..5] OF REAL; (* Observer Estimated Sensory Measurement Vector [-] *)
    vecInnov                        : ARRAY[0..5] OF REAL; (* Estimation Innovation Residual Vector (y - y_hat) [-] *)
    vecU                            : ARRAY[0..4] OF REAL; (* Current Optimal Actuator Output Command Vector [-] *)
    vecU_prev                       : ARRAY[0..4] OF REAL; (* Previous Execution Cycle Actuator Output Vector [-] *)
    vecU_rate                       : ARRAY[0..4] OF REAL; (* Instantaneous Actuator Slew Rate Vector [%/s] *)
    vecX_target                     : ARRAY[0..5] OF REAL; (* Target Dynamic State Trajectory Setpoint Vector [-] *)
    vecU_target                     : ARRAY[0..4] OF REAL; (* Nominal Steady-State Actuator Setpoint Vector [-] *)

    (* Model Predictive Control (MPC) Cost Weighting & Sizing Arrays *)
    vecQ_weight                     : ARRAY[0..5] OF REAL; (* State Tracking Error Quadratic Diagonal Penalty Q [-] *)
    vecR_weight                     : ARRAY[0..4] OF REAL; (* Actuator Effort Quadratic Diagonal Penalty R [-] *)
    vecS_rate_weight                : ARRAY[0..4] OF REAL; (* Actuator Slew Rate-of-Change Diagonal Penalty S [-] *)
    vecP_terminal                   : ARRAY[0..5] OF REAL; (* Terminal Horizon State Penalty Diagonal Matrix P [-] *)
    vecU_min                        : ARRAY[0..4] OF REAL; (* Actuator Physical Absolute Lower Saturation Limits [%] *)
    vecU_max                        : ARRAY[0..4] OF REAL; (* Actuator Physical Absolute Upper Saturation Limits [%] *)
    vecU_slewMax                    : ARRAY[0..4] OF REAL; (* Actuator Maximum Slew Rate Per Scan Execution Limit [%] *)

    (* Receding-Horizon Prediction Workspace (Horizon N=10, 10 Unrolled PGD Iterations) *)
    trajX_mpc                       : ARRAY[0..10, 0..5] OF REAL; (* MPC Forward State Trajectory Over Horizon N=10 [-] *)
    trajU_mpc                       : ARRAY[0..9, 0..4] OF REAL;  (* MPC Control Actuator Trajectory Over Horizon N=10 [-] *)
    trajCostate                     : ARRAY[0..10, 0..5] OF REAL; (* Backward Adjoint Costate Vector Over Horizon N=10 [-] *)
    trajGrad_J                      : ARRAY[0..9, 0..4] OF REAL;  (* Analytical Cost Functional Gradient w.r.t U [-] *)
    trajU_cand                      : ARRAY[0..9, 0..4] OF REAL;  (* Candidate Actuator Update Trajectory [-] *)
    rPgd_StepSize                   : REAL := 0.024;    (* Projected Gradient Descent Learning Step Size Gamma [-] *)
    rMpc_AccumulatedCost            : REAL := 0.0;      (* Unrolled MPC Quadratic Objective Cost Function Value [-] *)

    (* 64 Cross-Direction (CD) Basis Weight Profiler Internal Workspace *)
    arrTargetBasisWeight_CD         : ARRAY[1..64] OF REAL; (* 64 CD Zone Target Setpoint Basis Weight Profile [g/m2] *)
    arrErrorBasisWeight_CD          : ARRAY[1..64] OF REAL; (* Raw Cross-Direction Basis Weight Spatial Error [g/m2] *)
    arrFilteredError_CD             : ARRAY[1..64] OF REAL; (* Spatially Smoothed 3-Point Filtered Error Profile [g/m2] *)
    arrIntegralError_CD             : ARRAY[1..64] OF REAL; (* Spatial Actuator Integral Deviation Accumulator [g*s/m2] *)
    arrSliceSpindleCmd_um           : ARRAY[1..64] OF REAL; (* Commanded Spindle Mechanical Thermal Micro-Displacement [um] *)
    arrSliceSpindlePrev_um          : ARRAY[1..64] OF REAL; (* Previous Execution Cycle Spindle Displacement [um] *)
    arrAdjacentDelta_um             : ARRAY[1..64] OF REAL; (* Adjacent Actuator Differential Displacement Profile [um] *)
    arrCurvature_um                 : ARRAY[1..64] OF REAL; (* Slice Lip Beam Mechanical Curvature Profile [um] *)
    arrThermalExpansion_um          : ARRAY[1..64] OF REAL; (* Actual Thermal Rod Expansion Model Calculation [um] *)
    arrThermalModelTemp_degC        : ARRAY[1..64] OF REAL; (* Spindle Core Dynamic Temperature Estimate [deg C] *)
    matG_Toeplitz                   : ARRAY[1..64, 1..64] OF REAL; (* Spatial Cross-Coupling Attenuation Kernel Matrix [-] *)
    rMaxAllowedAdjacentDelta_um     : REAL := 25.0;     (* Permissible Adjacent Actuator Relative Step Limit [um] *)
    rMaxAllowedCurvature_um         : REAL := 18.0;     (* Permissible Slice Lip Beam Second Difference Limit [um] *)
    rCdProfileGain_Kp               : REAL := 1.45;     (* Proportional Controller Gain for Basis Weight Profile [-] *)
    rCdProfileGain_Ki               : REAL := 0.085;    (* Integral Controller Gain for Basis Weight Profile [1/s] *)

    (* 2oo3 Triple Modular Redundancy (TMR) Sensor Channels *)
    (* Channel Group 1: Total Head Pressure *)
    rHeadPress_Voted_kPa            : REAL := 158.5;    (* 2oo3 Voted Total Hydraulic Head Pressure [kPa] *)
    bHeadPress_HealthA              : BOOL := TRUE;     (* Pressure Transmitter Ch 1A Healthy Flag [-] *)
    bHeadPress_HealthB              : BOOL := TRUE;     (* Pressure Transmitter Ch 1B Healthy Flag [-] *)
    bHeadPress_HealthC              : BOOL := TRUE;     (* Pressure Transmitter Ch 1C Healthy Flag [-] *)
    rHeadPress_Disc_AB_ms           : REAL := 0.0;      (* Channel 1A vs 1B Discrepancy Timer Accumulator [ms] *)
    rHeadPress_Disc_BC_ms           : REAL := 0.0;      (* Channel 1B vs 1C Discrepancy Timer Accumulator [ms] *)
    rHeadPress_Disc_CA_ms           : REAL := 0.0;      (* Channel 1C vs 1A Discrepancy Timer Accumulator [ms] *)
    bHeadPress_Degraded             : BOOL := FALSE;    (* Total Head Operating on Degraded 2oo2 Voting [-] *)
    bHeadPress_SingleFallback       : BOOL := FALSE;    (* Total Head Operating on Single Channel 1oo1 [-] *)
    bHeadPress_Trip                 : BOOL := FALSE;    (* Total Head Transmitter Complete Failure Trip Flag [-] *)

    (* Channel Group 2: Stock Pond Level *)
    rPondLevel_Voted_mm             : REAL := 320.0;    (* 2oo3 Voted Stock Pond Free Surface Level [mm] *)
    bPondLevel_HealthA              : BOOL := TRUE;     (* Level Transmitter Ch 2A Healthy Flag [-] *)
    bPondLevel_HealthB              : BOOL := TRUE;     (* Level Transmitter Ch 2B Healthy Flag [-] *)
    bPondLevel_HealthC              : BOOL := TRUE;     (* Level Transmitter Ch 2C Healthy Flag [-] *)
    rPondLevel_Disc_AB_ms           : REAL := 0.0;      (* Channel 2A vs 2B Discrepancy Timer Accumulator [ms] *)
    rPondLevel_Disc_BC_ms           : REAL := 0.0;      (* Channel 2B vs 2C Discrepancy Timer Accumulator [ms] *)
    rPondLevel_Disc_CA_ms           : REAL := 0.0;      (* Channel 2C vs 2A Discrepancy Timer Accumulator [ms] *)
    bPondLevel_Degraded             : BOOL := FALSE;    (* Pond Level Operating on Degraded 2oo2 Voting [-] *)
    bPondLevel_SingleFallback       : BOOL := FALSE;    (* Pond Level Operating on Single Channel 1oo1 [-] *)
    bPondLevel_Trip                 : BOOL := FALSE;    (* Pond Level Transmitter Complete Failure Trip Flag [-] *)

    (* Channel Group 3: Dilution Profiling Header Flow *)
    rDilutionFlow_Voted_m3h         : REAL := 145.0;    (* 2oo3 Voted Dilution Header Flow Rate [m3/h] *)
    bDilutionFlow_HealthA           : BOOL := TRUE;     (* Flowmeter Ch 3A Healthy Flag [-] *)
    bDilutionFlow_HealthB           : BOOL := TRUE;     (* Flowmeter Ch 3B Healthy Flag [-] *)
    bDilutionFlow_HealthC           : BOOL := TRUE;     (* Flowmeter Ch 3C Healthy Flag [-] *)
    rDilutionFlow_Disc_AB_ms        : REAL := 0.0;      (* Channel 3A vs 3B Discrepancy Timer Accumulator [ms] *)
    rDilutionFlow_Disc_BC_ms        : REAL := 0.0;      (* Channel 3B vs 3C Discrepancy Timer Accumulator [ms] *)
    rDilutionFlow_Disc_CA_ms        : REAL := 0.0;      (* Channel 3C vs 3A Discrepancy Timer Accumulator [ms] *)
    bDilutionFlow_Degraded          : BOOL := FALSE;    (* Dilution Flow Operating on Degraded 2oo2 Voting [-] *)
    bDilutionFlow_SingleFallback    : BOOL := FALSE;    (* Dilution Flow Operating on Single Channel 1oo1 [-] *)
    bDilutionFlow_Trip              : BOOL := FALSE;    (* Dilution Flowmeter Complete Failure Trip Flag [-] *)

    (* Channel Group 4: Forming Wire Section Speed *)
    rWireSpeed_Voted_mpmin          : REAL := 1800.0;   (* 2oo3 Voted Forming Wire Speed [m/min] *)
    bWireSpeed_HealthA              : BOOL := TRUE;     (* Wire Encoder Ch 4A Healthy Flag [-] *)
    bWireSpeed_HealthB              : BOOL := TRUE;     (* Wire Encoder Ch 4B Healthy Flag [-] *)
    bWireSpeed_HealthC              : BOOL := TRUE;     (* Wire Encoder Ch 4C Healthy Flag [-] *)
    rWireSpeed_Disc_AB_ms           : REAL := 0.0;      (* Channel 4A vs 4B Discrepancy Timer Accumulator [ms] *)
    rWireSpeed_Disc_BC_ms           : REAL := 0.0;      (* Channel 4B vs 4C Discrepancy Timer Accumulator [ms] *)
    rWireSpeed_Disc_CA_ms           : REAL := 0.0;      (* Channel 4C vs 4A Discrepancy Timer Accumulator [ms] *)
    bWireSpeed_Degraded             : BOOL := FALSE;    (* Wire Speed Operating on Degraded 2oo2 Voting [-] *)
    bWireSpeed_SingleFallback       : BOOL := FALSE;    (* Wire Speed Operating on Single Channel 1oo1 [-] *)
    bWireSpeed_Trip                 : BOOL := FALSE;    (* Wire Speed Encoder Complete Failure Trip Flag [-] *)

    (* Deterministic 14-Stage Production Finite State Machine Engine *)
    eState                          : INT := 0;         (* Active Operational State Index [0..13] [-] *)
    ePrevState                      : INT := 0;         (* Previous Scan Operational State Index [0..13] [-] *)
    rStateTimer_s                   : REAL := 0.0;      (* Dwell Time Elapsed in Active State [s] *)
    rSubStateTimer_s                : REAL := 0.0;      (* Internal Sub-State Dwell Timer [s] *)
    iFsmStepIndex                   : INT := 0;         (* Sequential Step Index Within Active Stage [-] *)
    bFsmTransitionTrigger           : BOOL := FALSE;    (* State Discrete Transition Condition Validated [-] *)

    (* State Machine Specific Operation Timers *)
    rFlushTimer_s                   : REAL := 0.0;      (* White Water Flush & Warmup Timer [s] *)
    rAirSealTimer_s                 : REAL := 0.0;      (* Compressed Air Cushion Pressurization & Seal Timer [s] *)
    rFanPumpRampTimer_s             : REAL := 0.0;      (* Primary Fan Pump Soft Acceleration Timer [s] *)
    rLevelLockTimer_s               : REAL := 0.0;      (* Stock Pond Level Closed Loop Lock-In Timer [s] *)
    rHeadStabilizeTimer_s           : REAL := 0.0;      (* Total Head Hydraulic Stabilization Timer [s] *)
    rJetSyncTimer_s                 : REAL := 0.0;      (* Jet-to-Wire Speed Ratio Synchronization Timer [s] *)
    rSliceThermalBaselineTimer_s    : REAL := 0.0;      (* 64 Thermal Spindle Warmup & Baseline Timer [s] *)
    rGradeChangeTimer_s             : REAL := 0.0;      (* Online Grade Transition Trajectory Ramp Timer [s] *)
    rSheetBreakDivertTimer_s        : REAL := 0.0;      (* Sheet Break Slurry Emergency Dump Gate Timer [s] *)
    rWireRampdownTimer_s            : REAL := 0.0;      (* Controlled Wire Rampdown Deceleration Timer [s] *)
    rCipCleanTimer_s                : REAL := 0.0;      (* Post-Run Chemical CIP Washdown Execution Timer [s] *)
    rEmergencyTripTimer_s           : REAL := 0.0;      (* Emergency Pump Cavitation & Stock Runout Trip Dwell [s] *)

    (* ISA-18.2 Multi-Tier Process Alarm Limits, Deadbands & Latch Flags *)
    (* Total Head Pressure Alarms [kPa] *)
    rHead_HH_Limit_kPa              : REAL := 220.0;    (* Total Head High-High Rupture Burst Danger Trip [kPa] *)
    rHead_H_Limit_kPa               : REAL := 195.0;    (* Total Head High Process Deviation Warning [kPa] *)
    rHead_L_Limit_kPa               : REAL := 120.0;    (* Total Head Low Process Deviation Warning [kPa] *)
    rHead_LL_Limit_kPa              : REAL := 95.0;     (* Total Head Low-Low Collapse Loss of Jet Trip [kPa] *)
    rHead_Deadband_kPa              : REAL := 2.5;      (* Total Head Alarm Clearance Hysteresis Deadband [kPa] *)

    (* Stock Pond Liquid Level Alarms [mm] *)
    rPond_HH_Limit_mm               : REAL := 480.0;    (* Stock Pond High-High Air Cushion Flooding Trip [mm] *)
    rPond_H_Limit_mm                : REAL := 410.0;    (* Stock Pond High Level Deviation Warning [mm] *)
    rPond_L_Limit_mm                : REAL := 230.0;    (* Stock Pond Low Level Deviation Warning [mm] *)
    rPond_LL_Limit_mm               : REAL := 160.0;    (* Stock Pond Low-Low Air Ingress / Vortexing Trip [mm] *)
    rPond_Deadband_mm               : REAL := 5.0;      (* Stock Pond Level Alarm Clearance Deadband [mm] *)

    (* Compressed Air Cushion Pressure Alarms [kPa] *)
    rAirPad_HH_Limit_kPa            : REAL := 180.0;    (* Air Pad High-High Vessel Overpressure Relief Trip [kPa] *)
    rAirPad_H_Limit_kPa             : REAL := 155.0;    (* Air Pad High Pressure Advisory Warning [kPa] *)
    rAirPad_L_Limit_kPa             : REAL := 60.0;     (* Air Pad Low Pressure Advisory Warning [kPa] *)
    rAirPad_LL_Limit_kPa            : REAL := 35.0;     (* Air Pad Low-Low Complete Pressure Loss Trip [kPa] *)
    rAirPad_Deadband_kPa            : REAL := 2.0;      (* Air Pad Pressure Alarm Clearance Deadband [kPa] *)

    (* Jet-to-Wire Speed Ratio Alarms [-] *)
    rJetWire_HH_Limit               : REAL := 1.120;    (* Jet-to-Wire Speed Ratio High-High Fiber Wave Trip [-] *)
    rJetWire_H_Limit                : REAL := 1.065;    (* Jet-to-Wire Speed Ratio High Formation Deviation [-] *)
    rJetWire_L_Limit                : REAL := 0.985;    (* Jet-to-Wire Speed Ratio Low Dragging Web Deviation [-] *)
    rJetWire_LL_Limit               : REAL := 0.940;    (* Jet-to-Wire Speed Ratio Low-Low Severe Web Tear Trip [-] *)
    rJetWire_Deadband               : REAL := 0.005;    (* Jet-to-Wire Ratio Alarm Clearance Deadband [-] *)

    (* Finished Web Mean Basis Weight Alarms [g/m2] *)
    rWeight_HH_Limit_gpm2           : REAL := 115.0;    (* Basis Weight High-High Overload Reject Trip [g/m2] *)
    rWeight_H_Limit_gpm2            : REAL := 88.0;     (* Basis Weight High Process Variation Warning [g/m2] *)
    rWeight_L_Limit_gpm2            : REAL := 72.0;     (* Basis Weight Low Process Variation Warning [g/m2] *)
    rWeight_LL_Limit_gpm2           : REAL := 55.0;     (* Basis Weight Low-Low Under-Weight Reject Trip [g/m2] *)
    rWeight_Deadband_gpm2           : REAL := 1.0;      (* Basis Weight Alarm Clearance Deadband [g/m2] *)

    (* Active Alarm Condition Latch Bits *)
    bHead_HH_Active                 : BOOL := FALSE;
    bHead_H_Active                  : BOOL := FALSE;
    bHead_L_Active                  : BOOL := FALSE;
    bHead_LL_Active                 : BOOL := FALSE;
    bPond_HH_Active                 : BOOL := FALSE;
    bPond_H_Active                  : BOOL := FALSE;
    bPond_L_Active                  : BOOL := FALSE;
    bPond_LL_Active                 : BOOL := FALSE;
    bAirPad_HH_Active               : BOOL := FALSE;
    bAirPad_H_Active                : BOOL := FALSE;
    bAirPad_L_Active                : BOOL := FALSE;
    bAirPad_LL_Active               : BOOL := FALSE;
    bJetWire_HH_Active              : BOOL := FALSE;
    bJetWire_H_Active               : BOOL := FALSE;
    bJetWire_L_Active               : BOOL := FALSE;
    bJetWire_LL_Active              : BOOL := FALSE;
    bWeight_HH_Active               : BOOL := FALSE;
    bWeight_H_Active                : BOOL := FALSE;
    bWeight_L_Active                : BOOL := FALSE;
    bWeight_LL_Active               : BOOL := FALSE;
    bSigma_H_Active                 : BOOL := FALSE;
    bSigma_HH_Active                : BOOL := FALSE;
    bCurvature_HH_Active            : BOOL := FALSE;
    bAdjacentDelta_HH_Active        : BOOL := FALSE;

    (* First-Out Latching Internal Logic *)
    bFirstOutLatched                : BOOL := FALSE;    (* First-Out Root Cause Frozen Latched Flag [-] *)
    dwFirstOutCapturedCode          : DWORD := 16#00000000; (* Captured Initial Fault Root Cause Code [-] *)

    (* Scratch Loop Counters & Temporary Math Computation Reals *)
    iIdx                            : INT := 0;         (* Primary State Vector Loop Counter [-] *)
    jIdx                            : INT := 0;         (* Matrix Column Loop Counter [-] *)
    mIdx                            : INT := 0;         (* Actuator Dimension Loop Counter [-] *)
    kStep                           : INT := 0;         (* MPC Horizon Time Step Counter [-] *)
    iIter                           : INT := 0;         (* PGD Optimization Unrolled Iteration Counter [-] *)
    iAct                            : INT := 0;         (* Cross-Direction Actuator Index (1..64) [-] *)
    jAct                            : INT := 0;         (* Cross-Direction Toeplitz Column Index (1..64) [-] *)
    rTempSum                        : REAL := 0.0;      (* Dot Product Matrix Multiply Accumulator [-] *)
    rTempDiff                       : REAL := 0.0;      (* Scalar Difference Intermediate Real [-] *)
    rTempCandidate                  : REAL := 0.0;      (* Actuator Gradient Candidate Value [-] *)
    rTempProfileMean                : REAL := 0.0;      (* CD Profile Summation Accumulator for Mean [g/m2] *)
    rTempProfileVariance            : REAL := 0.0;      (* CD Profile Sum of Squared Deviations [g2/m4] *)
    rTempDeltaLeft                  : REAL := 0.0;      (* Slice Lip Actuator Left Differential [um] *)
    rTempDeltaRight                 : REAL := 0.0;      (* Slice Lip Actuator Right Differential [um] *)
    rTempAirHydroHead_mmH2O         : REAL := 0.0;      (* Hydrostatic Head from Air Cushion [mm H2O] *)
    rTempDelta                      : REAL := 0.0;      (* Temporary Delta Real Variable [-] *)
END_VAR
"""
    parts.append(var_internal)

    return parts
