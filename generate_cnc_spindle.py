import json
import os
import sys

def generate_iec_st():
    parts = []

    # =========================================================================
    # 0. HEADER COMMENT
    # =========================================================================
    parts.append("""FUNCTION_BLOCK FB_CNC_5Axis_SpindleThermalExpansion_ActiveVibrationDamping
(*
 ====================================================================================================
  PROJECT:       5-AXIS HIGH-SPEED MACHINING CENTER (HSM) GANTRY AUTOMATION & CYBER-PHYSICAL CONTROL
  SUBSYSTEM:     MOTORIZED SPINDLE ACTIVE THERMAL EXPANSION COMPENSATION & PIEZO CHATTER SUPPRESSION
  DISCIPLINE:    HIGH-PRECISION MACHINE TOOL MECHATRONICS / ADVANCED ADAPTIVE CYBER-PHYSICAL CONTROL
  IEC STANDARD:  IEC 61131-3 3RD EDITION (DETERMINISTIC EMBEDDED REAL-TIME CNC PLC EXECUTION)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  MACHINE CLASS: 5-AXIS GANTRY MACHINING CENTER (X, Y, Z, A-TILTING TRUNNION, C-ROTARY TABLE)
  SPINDLE SPEC:  30,000 RPM | 45.0 kW CONTINUOUS (60.0 kW S6-40%) | HSK-A63 HOLLOW TAPER CLAMPING
  BEARING SPEC:  CERAMIC HYBRID ANGULAR CONTACT (Si3N4 BALLS, CRONIDUR 30 RINGS) + ROLLER FLOATING REAR
  ACTUATION:     HIGH-FREQUENCY PIEZOELECTRIC STACK COUNTER-FORCE ACTUATORS (> 2,500 Hz BANDWIDTH)
  THERMAL SPEC:  10-NODE FINITE-DIFFERENCE SPINDLE SHAFT THERMAL INTEGRAL (Z-AXIS SUB-MICRON OFFSET)
  CYCLE TICK:    Ts = 0.001000 s (1.000 MILLISECOND SYNCHRONOUS DETERMINISTIC PLC / SERVO SCAN)
 ====================================================================================================
  CYBER-PHYSICAL SYSTEM ARCHITECTURAL OVERVIEW:
  ----------------------------------------------------------------------------------------------------
  This high-performance IEC 61131-3 Function Block executes deterministic sub-millisecond control,
  finite-difference thermal growth integration, and active piezoelectric regenerative chatter damping
  for an ultra-precision 5-axis high-speed CNC gantry machining center.
  
  The cyber-physical architecture integrates five coupled engineering domains:
  1. Spindle Active Thermal Growth & Radial Drift Compensation:
     - 10-node finite difference axial thermal discretization along the rotating spindle cartridge:
       z_growth = integral [ alpha_shaft(T(z)) * (T(z) - T_ref) ] dz
     - 8 RTD / Fiber Bragg Grating (FBG) optical temperature sensors measuring ceramic hybrid bearing
       races, motor stator core, winding end-turns, cooling jacket inlet/outlet, and spindle nose.
     - Real-time numerical integration via Simpson/trapezoidal quadrature injecting sub-micron (+/- 1.0 um)
       compensation offsets into the CNC Z-axis servo position loop, eliminating workpiece depth errors.
     - 2D radial thermal drift estimation compensating spindle centerline shifts along X and Y axes.
  2. Piezoelectric Active Regenerative Chatter Vibration Damping:
     - 4 pre-stressed multilayer PZT stack actuators configured in orthogonal push-pull pairs (X+, X-, Y+, Y-)
       delivering dynamic counter-forces up to +/- 1,500 N with sub-millisecond latency.
     - Tri-axial high-bandwidth piezoelectric accelerometers mounted directly adjacent to the front bearing.
     - Real-time regenerative cutting force observer evaluating delayed surface undulations:
       F_cut(t) = K_t * b * [ h_0 - z(t) + z(t - tau) ]
     - Direct Velocity Feedback (DVFB) active damping augmenting the natural damping ratio of the dominant
       structural tool-spindle bending modes from zeta = 0.015 up to zeta = 0.125.
  3. Spindle Speed Variation (SSV) Autonomous Modulation:
     - Dynamic stability lobe diagram (SLD) real-time boundary proximity evaluation.
     - Continuous sinusoidal / triangular modulation of nominal spindle speed:
       N(t) = N_0 + Delta_N * sin(2 * pi * f_m * t)
     - Disrupts the regenerative wave phase relationship between subsequent tooth passes, quenching chatter.
  4. 16x16 Discrete Multivariable State-Space Model & Receding-Horizon MPC:
     - 16 system states capturing structural compliance, regenerative delay, thermal nodes, and actuator dynamics.
     - 8 control inputs regulating piezo voltages, servo offsets, speed trim, feedrate override, and cooling.
     - Online quadratic cost optimization with explicit box constraints and actuator rate limits.
  5. Closed-Loop Oil-Air Micro-Lubrication & Chilled Glycol Thermal Management:
     - High-precision micro-dosing pump dispensing 0.03 cm3 synthetic oil shots into high-velocity compressed air.
     - Optical streak sensor confirming droplet passage and elastohydrodynamic (EHD) oil film integrity.
     - Predictive feedforward cooling jacket valve modulation balancing spindle motor electrical and friction heat.
  6. Triple Modular Redundancy (2oo3 TMR) Voting & Fault Degradation:
     - Triplicate tri-axial accelerometers (X, Y, Z), bearing temperature probes, and spindle tachometers.
     - Median selection with discrepancy persistence timers, failing over to 1oo2 or safe shutdown.
  7. 12-Stage Operational Finite State Machine (FSM):
     - Complete operational lifecycle from cold pre-lube purge, warm-up ramping, laser tool length metrology,
       chatter monitoring, thermal compensation, SSV actuation, to tool retract and emergency E-stop.
  8. ISA-18.2 Multi-Tiered Alarm Matrix:
     - Multi-tier thresholds (HH, H, L, LL) with deadband hysteresis, priority escalation, and bit-packed telemetry.
 ====================================================================================================
*)
""")

    # =========================================================================
    # 1. VAR_INPUT
    # =========================================================================
    parts.append("""
VAR_INPUT
    (* ===================================================================================== *)
    (* 1.0 SYSTEM MASTER DIGITAL PERMISSIVES & OPERATOR COMMANDS                             *)
    (* ===================================================================================== *)
    bEnableSystem                   : BOOL := FALSE;    (* Master Machine Control Automation Enable Permissive [BOOL] *)
    bEmergencyStop                  : BOOL := TRUE;     (* Hardwired Fail-Safe SIL-3 Emergency Stop Relay (Active High = Healthy) [BOOL] *)
    bResetAlarms                    : BOOL := FALSE;    (* Operator Master Alarm Trip Acknowledgement and Reset Command [BOOL] *)
    bAutoCyclePermissive            : BOOL := FALSE;    (* CNC Executive Controller Automatic Machining Cycle Permissive [BOOL] *)
    bChillerUnitReady               : BOOL := TRUE;     (* Recirculating Closed-Loop Glycol Chiller Ready Status [BOOL] *)
    bLubricationUnitReady           : BOOL := TRUE;     (* Oil-Air Micro-Lubrication System Supply Pressure Ready Status [BOOL] *)
    bPiezoAmplifierReady            : BOOL := TRUE;     (* High-Voltage Piezoelectric Power Amplifier Operational Ready [BOOL] *)
    bToolClampedHSK                 : BOOL := TRUE;     (* HSK-A63 Motorized Drawbar Tool Clamped Proximity Sensor [BOOL] *)
    bLaserMetrologyReady            : BOOL := TRUE;     (* Non-Contact Optical Laser Tool Setter Calibrated and Ready [BOOL] *)
    bCoolantThroughSpindleActive    : BOOL := FALSE;    (* High-Pressure Through-Spindle Coolant (CTS) Flow Status [BOOL] *)
    bInCutSignalFromCNC             : BOOL := FALSE;    (* CNC Interpolator Flag: Cutting Tool Actively Engaged in Workpiece [BOOL] *)
    bManualOverrideEnable           : BOOL := FALSE;    (* Maintenance Technician Manual Actuator Override Permissive [BOOL] *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) SPINDLE HOUSING ACCELEROMETERS [m/s2]            *)
    (* Tri-axial high-bandwidth piezoelectric accelerometers mounted at front bearing flange  *)
    (* ===================================================================================== *)
    rVibrationAccel_X_A             : REAL := 0.0;      (* Spindle Front Nose Radial X-Axis Acceleration Channel A [m/s2] *)
    rVibrationAccel_X_B             : REAL := 0.0;      (* Spindle Front Nose Radial X-Axis Acceleration Channel B [m/s2] *)
    rVibrationAccel_X_C             : REAL := 0.0;      (* Spindle Front Nose Radial X-Axis Acceleration Channel C [m/s2] *)
    rVibrationAccel_Y_A             : REAL := 0.0;      (* Spindle Front Nose Radial Y-Axis Acceleration Channel A [m/s2] *)
    rVibrationAccel_Y_B             : REAL := 0.0;      (* Spindle Front Nose Radial Y-Axis Acceleration Channel B [m/s2] *)
    rVibrationAccel_Y_C             : REAL := 0.0;      (* Spindle Front Nose Radial Y-Axis Acceleration Channel C [m/s2] *)
    rVibrationAccel_Z_A             : REAL := 0.0;      (* Spindle Front Nose Axial Z-Axis Acceleration Channel A [m/s2] *)
    rVibrationAccel_Z_B             : REAL := 0.0;      (* Spindle Front Nose Axial Z-Axis Acceleration Channel B [m/s2] *)
    rVibrationAccel_Z_C             : REAL := 0.0;      (* Spindle Front Nose Axial Z-Axis Acceleration Channel C [m/s2] *)

    (* ===================================================================================== *)
    (* 3.0 SPINDLE CARTRIDGE & MOTOR THERMAL SENSOR NETWORK [deg C]                          *)
    (* 8 RTD / Fiber Bragg Grating (FBG) optical temperature stations along spindle assembly *)
    (* ===================================================================================== *)
    rTempFrontBearing_degC          : REAL := 22.5;     (* Front Ceramic Hybrid Bearing Outer Ring Temperature [deg C] *)
    rTempRearBearing_degC           : REAL := 22.0;     (* Rear Floating Roller Bearing Outer Ring Temperature [deg C] *)
    rTempStatorCore_degC            : REAL := 24.0;     (* Built-in Synchronous Motor Stator Iron Lamination Core [deg C] *)
    rTempStatorWinding_degC         : REAL := 26.5;     (* Built-in Synchronous Motor Stator Copper End-Turn Winding [deg C] *)
    rTempChillerInlet_degC          : REAL := 20.0;     (* Recirculating Cooling Jacket Chilled Glycol Supply Inlet [deg C] *)
    rTempChillerOutlet_degC         : REAL := 21.2;     (* Recirculating Cooling Jacket Chilled Glycol Return Outlet [deg C] *)
    rTempSpindleNose_degC           : REAL := 22.8;     (* Toolholder Taper / Spindle Nose Non-Contact Pyrometer [deg C] *)
    rTempAmbientGantry_degC         : REAL := 21.0;     (* Machine Tool Gantry Column Reference Ambient Temperature [deg C] *)

    (* ===================================================================================== *)
    (* 4.0 TRIPLE MODULAR REDUNDANCY (2oo3) FRONT BEARING DEDICATED RTDs [deg C]             *)
    (* ===================================================================================== *)
    rTempBearing_A_degC             : REAL := 22.5;     (* Front Bearing Set Temperature RTD Channel A [deg C] *)
    rTempBearing_B_degC             : REAL := 22.5;     (* Front Bearing Set Temperature RTD Channel B [deg C] *)
    rTempBearing_C_degC             : REAL := 22.5;     (* Front Bearing Set Temperature RTD Channel C [deg C] *)

    (* ===================================================================================== *)
    (* 5.0 TRIPLE MODULAR REDUNDANCY (2oo3) SPINDLE TACHOMETER RING ENCODERS [RPM]           *)
    (* High-resolution magnetic/optical spindle ring encoders measuring rotational velocity  *)
    (* ===================================================================================== *)
    rSpindleSpeed_EncA_RPM          : REAL := 0.0;      (* Spindle Shaft Absolute Optical Ring Encoder Channel A [RPM] *)
    rSpindleSpeed_EncB_RPM          : REAL := 0.0;      (* Spindle Shaft Absolute Optical Ring Encoder Channel B [RPM] *)
    rSpindleSpeed_EncC_RPM          : REAL := 0.0;      (* Spindle Shaft Absolute Optical Ring Encoder Channel C [RPM] *)

    (* ===================================================================================== *)
    (* 6.0 CNC TRAJECTORY, CUTTING KINEMATICS & PROCESS METERING                             *)
    (* Real-time trajectory demands and feedback signals from CNC interpolator & sensors     *)
    (* ===================================================================================== *)
    rCommandSpindleSpeed_RPM        : REAL := 18000.0;  (* Programmed Nominal Spindle Rotational Speed Setpoint [RPM] *)
    rCommandFeedrate_mmpm           : REAL := 4500.0;   (* Programmed CNC Axis Cutting Feedrate Velocity [mm/min] *)
    rProgrammedCutDepth_mm          : REAL := 2.500;    (* Programmed Axial Cutting Depth of Cut a_p [mm] *)
    rProgrammedRadialWidth_mm       : REAL := 6.000;    (* Programmed Radial Width of Cut a_e [mm] *)
    iToolFluteCount                 : INT := 4;         (* Active Solid Carbide / Inserted End Mill Flute Count [-] *)
    rToolDiameter_mm                : REAL := 16.000;   (* Active Cutting Tool Outer Diameter [mm] *)
    rToolGageLength_mm              : REAL := 125.000;  (* Tool Assembly Gage Length from Spindle Gage Line [mm] *)
    rSpindleMotorTorque_Nm          : REAL := 14.20;    (* Spindle Synchronous Drive Active Electromagnetic Torque [Nm] *)
    rSpindleMotorCurrent_A          : REAL := 28.50;    (* Spindle Synchronous Drive Stator RMS Phase Current [A] *)
    rLubricationPressure_bar        : REAL := 3.10;     (* Oil-Air Micro-Lubrication Mixing Manifold Pressure [bar] *)
    rChillerFlowRate_lpm            : REAL := 12.40;    (* Recirculating Glycol Coolant Volumetric Flow Rate [l/min] *)
    bStreakSensorOilPulse           : BOOL := FALSE;    (* Optical Capillary Streak Sensor Detecting Oil Droplet Passage [BOOL] *)
    rAcousticEmission_dB            : REAL := 42.5;     (* High-Frequency Acoustic Emission Sensor Amplitude [dB] *)
    rLaserMeasuredToolRunout_um     : REAL := 1.20;     (* Laser Tool Setter Dynamic Radial Runout Measurement [um] *)
    rLaserMeasuredToolLength_mm     : REAL := 125.002;  (* Laser Tool Setter Dynamic Tool Gage Length at Speed [mm] *)
END_VAR
""")

    # =========================================================================
    # 2. VAR_OUTPUT
    # =========================================================================
    parts.append("""
VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1.0 REAL-TIME CNC SERVO COMPENSATION OFFSETS & ACTUATOR DEMANDS                       *)
    (* ===================================================================================== *)
    rZAxisThermalCompOffset_um      : REAL := 0.0;      (* Real-Time CNC Z-Axis Servo Thermal Growth Offset Injection [um] *)
    rXAxisRadialDriftOffset_um      : REAL := 0.0;      (* Real-Time CNC X-Axis Servo Centerline Radial Drift Offset [um] *)
    rYAxisRadialDriftOffset_um      : REAL := 0.0;      (* Real-Time CNC Y-Axis Servo Centerline Radial Drift Offset [um] *)
    rPiezoVoltage_X_V               : REAL := 65.0;     (* Piezo Stack X-Axis Dynamic Drive Voltage Demand (-20 to +150V) [V] *)
    rPiezoVoltage_Y_V               : REAL := 65.0;     (* Piezo Stack Y-Axis Dynamic Drive Voltage Demand (-20 to +150V) [V] *)
    rSSV_SpeedTrim_RPM              : REAL := 0.0;      (* Spindle Speed Variation (SSV) Dynamic Speed Modulation Trim [RPM] *)
    rFeedrateOverride_pct           : REAL := 100.0;    (* Dynamic CNC Feedrate Override Multiplier Demand (10 to 120%) [%] *)
    rChillerValveDemand_pct         : REAL := 45.0;     (* Proportional Chilled Glycol Control Valve Flow Demand [%] *)
    bLubricationInjectPulse         : BOOL := FALSE;    (* Micro-Shot Oil Dosing Pump Metering Solenoid Firing Pulse [BOOL] *)
    bSpindleDriveSTO_Trip           : BOOL := FALSE;    (* Safe Torque Off (STO) Hardwired Drive Safety Trip Request [BOOL] *)
    bPiezoClampActive               : BOOL := FALSE;    (* Piezoelectric Stack Actuator Safety Discharge Clamp Active [BOOL] *)
    bToolWearRetractReq             : BOOL := FALSE;    (* Autonomous CNC Cycle Hold and Safe Tool Retract Request [BOOL] *)

    (* ===================================================================================== *)
    (* 2.0 SYNTHESIZED 2oo3 VOTED PROCESS MEASUREMENTS                                       *)
    (* ===================================================================================== *)
    rVotedVibration_X_m_s2          : REAL := 0.0;      (* 2oo3 Median Voted Spindle X-Axis Vibration Acceleration [m/s2] *)
    rVotedVibration_Y_m_s2          : REAL := 0.0;      (* 2oo3 Median Voted Spindle Y-Axis Vibration Acceleration [m/s2] *)
    rVotedVibration_Z_m_s2          : REAL := 0.0;      (* 2oo3 Median Voted Spindle Z-Axis Vibration Acceleration [m/s2] *)
    rVotedBearingTemp_degC          : REAL := 22.5;     (* 2oo3 Median Voted Front Ceramic Hybrid Bearing Temperature [deg C] *)
    rVotedSpindleSpeed_RPM          : REAL := 0.0;      (* 2oo3 Median Voted Spindle Rotational Shaft Speed [RPM] *)

    (* ===================================================================================== *)
    (* 3.0 CYBER-PHYSICAL ESTIMATIONS, SPECTRAL METRICS & TELEMETRY                          *)
    (* ===================================================================================== *)
    rCalculatedThermalGrowth_um     : REAL := 0.0;      (* Cumulative Finite-Difference Spindle Axial Thermal Growth [um] *)
    rCalculatedRadialDrift_um       : REAL := 0.0;      (* Resultant Centerline Radial Thermal Drift Magnitude [um] *)
    rChatterSeverityIndex           : REAL := 0.0;      (* Normalized Chatter Severity Index (0.0=Stable, 1.0=Chatter) [-] *)
    rDominantChatterFreq_Hz         : REAL := 0.0;      (* Detected Dominant Spectral Vibration Chatter Peak Frequency [Hz] *)
    rEstimatedCuttingForce_N        : REAL := 0.0;      (* Dynamic Observer Estimated Tangential Cutting Force [N] *)
    rBearingLubricationFilm_pct     : REAL := 98.5;     (* Estimated Elastohydrodynamic (EHD) Specific Film Thickness Lambda [%] *)
    rCoolingHeatExtraction_kW       : REAL := 1.85;     (* Instantaneous Thermal Heat Extracted by Cooling Jacket [kW] *)
    rToolWearIndex_pct              : REAL := 4.2;      (* Cumulative In-Situ Acoustic / Dynamic Tool Edge Wear Index [%] *)
    iActiveFSMStage                 : INT := 10;        (* Current Supervisory Operational FSM Stage Register (10 to 120) [-] *)

    (* ===================================================================================== *)
    (* 4.0 ISA-18.2 COMPLIANT TELEMETRY, WARNING & ALARM STATUS BITMASKS                     *)
    (* ===================================================================================== *)
    dwSystemStatusWord              : DWORD := 16#0000_0000; (* 32-Bit Spindle Operational State & Telemetry Bitmask *)
    dwAlarmWord1                    : DWORD := 16#0000_0000; (* 32-Bit Primary Safety Interlock & Machine Protection Trips *)
    dwAlarmWord2                    : DWORD := 16#0000_0000; (* 32-Bit Dynamic Chatter, Vibration & Thermal Overheat Trips *)
    dwAlarmWord3                    : DWORD := 16#0000_0000; (* 32-Bit Auxiliary Subsystem Trips (Lube, Chiller, Piezo, Tool) *)
    dwWarningWord                   : DWORD := 16#0000_0000; (* 32-Bit Advisory Process Warnings & Boundary Slew Limits *)
    dwDegradationWord               : DWORD := 16#0000_0000; (* 32-Bit 2oo3 Sensor Discrepancy & Channel Degradation Word *)
END_VAR
""")

    # =========================================================================
    # 3. VAR
    # =========================================================================
    parts.append("""
VAR
    (* ===================================================================================== *)
    (* 1.0 FINITE STATE MACHINE (FSM) CONTROL REGISTERS & PROCESS TIMERS                     *)
    (* 12-Stage Operational State Machine from Cold Standby to Precision Machining & E-Stop  *)
    (* ===================================================================================== *)
    iState                          : INT := 10;        (* Primary Supervisory State Register *)
    iSubState                       : INT := 0;         (* Internal Sub-State Execution Phase *)
    iPrevState                      : INT := 10;        (* State History for Edge Detection *)
    iStateCycleCount                : DINT := 0;        (* Dwell Cycle Counter inside Current Stage *)
    rStateElapsedSec                : REAL := 0.0;      (* Continuous Elapsed Time in Active Stage [s] *)

    tStateTimer                     : TON;              (* Primary FSM Stage Dwell Timer *)
    tLubeCycleTimer                 : TON;              (* Oil-Air Micro-Lubrication Shot Interval Timer *)
    tLubePulseDurationTimer         : TON;              (* Micro-Dosing Solenoid Injection Pulse Duration Timer *)
    tStreakDetectionTimeoutTimer    : TON;              (* Optical Capillary Streak Arrival Window Timer *)
    tChillerPacingTimer             : TON;              (* Recirculating Coolant Thermal Pacing Scheduler *)
    tWarmUpRampTimer                : TON;              (* Cold Spindle Stepped Speed Ramp Stage Timer *)
    tLaserMetrologyDwellTimer       : TON;              (* Optical Tool Setter Settling and Reading Timer *)
    tChatterDebounceTimer           : TON;              (* Regenerative Chatter Threshold Persistence Debounce *)
    tSSV_CycleTimer                 : TON;              (* Spindle Speed Variation Sinusoidal Modulation Period Timer *)
    tCoolDownRampTimer              : TON;              (* Post-Operation Spindle Thermal Decay Idle Timer *)
    tSensorTripDebounceTimer        : TON;              (* 2oo3 Triplicate Discrepancy Fault Debounce Timer *)
    tPiezoDischargeTimer            : TON;              (* Piezoelectric Power Amplifier Safe Bleed-Down Timer *)

    (* ===================================================================================== *)
    (* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) VOTING REGISTERS & SPREAD TRACKING               *)
    (* Graceful degradation: 2oo3 healthy -> 1oo2 degraded -> Fail-Safe STO Trip             *)
    (* ===================================================================================== *)
    (* Accelerometer X-Axis Group [m/s2] *)
    rDev_AccX_AB                    : REAL := 0.0;
    rDev_AccX_BC                    : REAL := 0.0;
    rDev_AccX_CA                    : REAL := 0.0;
    bAccX_A_Healthy                 : BOOL := TRUE;
    bAccX_B_Healthy                 : BOOL := TRUE;
    bAccX_C_Healthy                 : BOOL := TRUE;
    bAccX_Degraded_1oo2             : BOOL := FALSE;
    bAccX_Trip                      : BOOL := FALSE;
    rTimer_AccX_Discrep             : REAL := 0.0;

    (* Accelerometer Y-Axis Group [m/s2] *)
    rDev_AccY_AB                    : REAL := 0.0;
    rDev_AccY_BC                    : REAL := 0.0;
    rDev_AccY_CA                    : REAL := 0.0;
    bAccY_A_Healthy                 : BOOL := TRUE;
    bAccY_B_Healthy                 : BOOL := TRUE;
    bAccY_C_Healthy                 : BOOL := TRUE;
    bAccY_Degraded_1oo2             : BOOL := FALSE;
    bAccY_Trip                      : BOOL := FALSE;
    rTimer_AccY_Discrep             : REAL := 0.0;

    (* Accelerometer Z-Axis Group [m/s2] *)
    rDev_AccZ_AB                    : REAL := 0.0;
    rDev_AccZ_BC                    : REAL := 0.0;
    rDev_AccZ_CA                    : REAL := 0.0;
    bAccZ_A_Healthy                 : BOOL := TRUE;
    bAccZ_B_Healthy                 : BOOL := TRUE;
    bAccZ_C_Healthy                 : BOOL := TRUE;
    bAccZ_Degraded_1oo2             : BOOL := FALSE;
    bAccZ_Trip                      : BOOL := FALSE;
    rTimer_AccZ_Discrep             : REAL := 0.0;

    (* Front Bearing Temperature RTD Group [deg C] *)
    rDev_TempB_AB                   : REAL := 0.0;
    rDev_TempB_BC                   : REAL := 0.0;
    rDev_TempB_CA                   : REAL := 0.0;
    bTempB_A_Healthy                : BOOL := TRUE;
    bTempB_B_Healthy                : BOOL := TRUE;
    bTempB_C_Healthy                : BOOL := TRUE;
    bTempB_Degraded_1oo2            : BOOL := FALSE;
    bTempB_Trip                     : BOOL := FALSE;
    rTimer_TempB_Discrep            : REAL := 0.0;

    (* Spindle Speed Optical Ring Encoder Group [RPM] *)
    rDev_Speed_AB                   : REAL := 0.0;
    rDev_Speed_BC                   : REAL := 0.0;
    rDev_Speed_CA                   : REAL := 0.0;
    bSpeed_A_Healthy                : BOOL := TRUE;
    bSpeed_B_Healthy                : BOOL := TRUE;
    bSpeed_C_Healthy                : BOOL := TRUE;
    bSpeed_Degraded_1oo2            : BOOL := FALSE;
    bSpeed_Trip                     : BOOL := FALSE;
    rTimer_Speed_Discrep            : REAL := 0.0;

    (* Discrepancy Tolerance Limits & Persist Durations *)
    c_rMaxDiscrepancyTime_s         : REAL := 0.250;    (* Discrepancy Persistence Trip Limit [s] *)
    c_rAccelDiscrepancyTol_m_s2     : REAL := 12.5;     (* Acceleration Inter-Channel Tolerance [m/s2] *)
    c_rTempDiscrepancyTol_degC      : REAL := 3.5;      (* Temperature Inter-Channel Tolerance [deg C] *)
    c_rSpeedDiscrepancyTol_RPM      : REAL := 250.0;    (* Speed Inter-Channel Tolerance [RPM] *)

    (* ===================================================================================== *)
    (* 3.0 MECHATRONIC CONSTANTS & CUTTING DYNAMICS PARAMETERS                               *)
    (* ===================================================================================== *)
    c_ShaftLength_m                 : REAL := 0.720;    (* Total Spindle Rotating Shaft Core Length [m] *)
    c_ShaftDiameter_m               : REAL := 0.085;    (* Spindle Front Bearing Journal Outer Diameter [m] *)
    c_ShaftMass_kg                  : REAL := 28.5;     (* Rotating Shaft, Rotor and Toolholder Assembly Mass [kg] *)
    c_RadialStiffness_N_um          : REAL := 145.0;    (* Ceramic Hybrid Front Bearing Set Dynamic Radial Stiffness [N/um] *)
    c_AxialStiffness_N_um           : REAL := 180.0;    (* Bearing Preload Mechanism Axial Restoring Stiffness [N/um] *)
    c_StructuralDamping_Ns_m        : REAL := 650.0;    (* Spindle Bearing Viscous Damping Coefficient [N*s/m] *)
    c_SteelAlpha_1_K                : REAL := 0.0000117;(* High-Alloy Tool Steel Thermal Expansion Coefficient alpha [1/K] *)
    c_AlphaTempCoeff                : REAL := 0.00050;  (* Second-Order Thermal Expansion Temperature Drift Factor [1/K^2] *)
    c_SteelThermalConduct_W_mK      : REAL := 45.0;     (* Spindle Shaft Material Thermal Conductivity [W/(m*K)] *)
    c_SpecificHeatSteel_J_kgK       : REAL := 480.0;    (* Spindle Shaft Material Specific Heat Capacity [J/(kg*K)] *)
    c_ScanTime_Ts_s                 : REAL := 0.001000; (* Synchronous Deterministic Scan Execution Interval [s] *)
    c_Pi                            : REAL := 3.14159265359;
    c_RadToDeg                      : REAL := 57.2957795131;
    c_DegToRad                      : REAL := 0.01745329251;

    (* Cutting Force Mechanics (Altintas Milling Mechanics) *)
    c_CutCoeff_Kt_N_mm2             : REAL := 1250.0;   (* Tangential Specific Cutting Pressure Coefficient [N/mm2] *)
    c_CutCoeff_Kr_N_mm2             : REAL := 480.0;    (* Radial Specific Cutting Pressure Coefficient [N/mm2] *)
    c_CutCoeff_Ka_N_mm2             : REAL := 290.0;    (* Axial Specific Cutting Pressure Coefficient [N/mm2] *)

    (* Piezoelectric Stack Actuator Mechatronics *)
    c_PiezoD33_pm_V                 : REAL := 650.0;    (* Piezoelectric Charge Constant d33 [pm/V] *)
    c_PiezoMaxStroke_um             : REAL := 25.0;     (* Maximum Mechanical Stroke Deflection (+/- 25 um) [um] *)
    c_PiezoMaxForce_N               : REAL := 3500.0;   (* Maximum Actuator Compressive Blocking Force [N] *)
    c_PiezoCapacitance_uF           : REAL := 3.20;     (* Multilayer Piezo Stack Total Electrical Capacitance [uF] *)
    c_PiezoVoltageMin_V             : REAL := -20.0;    (* Actuator Minimum Reverse Polarization Margin [V] *)
    c_PiezoVoltageMax_V             : REAL := 150.0;    (* Actuator Maximum Forward Continuous Voltage Limit [V] *)
    c_PiezoBandwidth_Hz             : REAL := 2800.0;   (* Dynamic Small-Signal Mechanical Response Bandwidth [Hz] *)

    (* Chilled Glycol Loop Mechatronics *)
    c_GlycolSpecificHeat_J_kgK      : REAL := 3750.0;   (* 40% Ethylene Glycol Coolant Specific Heat [J/(kg*K)] *)
    c_GlycolDensity_kg_m3           : REAL := 1055.0;   (* 40% Ethylene Glycol Coolant Mass Density [kg/m3] *)
    c_NominalChillerSetpoint_degC   : REAL := 20.00;    (* Spindle Cartridge Target Thermal Equilibrium Datum [deg C] *)

    (* ===================================================================================== *)
    (* 4.0 10-NODE FINITE-DIFFERENCE SPINDLE AXIAL & RADIAL THERMAL MODEL ARRAYS             *)
    (* Axial Node Stations: z1=Nose, z2=Bearing1, z3=Bearing2, z4=Housing, z5=StatorFront,   *)
    (*                     z6=StatorMid, z7=StatorRear, z8=RearBearing, z9=Cooling, z10=Tail *)
    (* ===================================================================================== *)
    c_NodeZ_mm                      : ARRAY[1..10] OF REAL := [0.0, 65.0, 130.0, 210.0, 290.0, 380.0, 470.0, 560.0, 640.0, 720.0];
    c_SegmentDZ_mm                  : ARRAY[1..9] OF REAL := [65.0, 65.0, 80.0, 80.0, 90.0, 90.0, 90.0, 80.0, 80.0];
    rNodeTemp_degC                  : ARRAY[1..10] OF REAL;
    rNodeDeltaT_degC                : ARRAY[1..10] OF REAL;
    rNodeAlpha_1_K                  : ARRAY[1..10] OF REAL;
    rSegmentElongation_um           : ARRAY[1..9] OF REAL;
    rRawThermalGrowth_um            : REAL := 0.0;
    rFilteredThermalGrowth_um       : REAL := 0.0;
    rPrevFilteredGrowth_um          : REAL := 0.0;
    rThermalGrowthRate_um_s         : REAL := 0.0;
    c_rMaxThermalCompSlewRate_um_s  : REAL := 6.0;      (* Maximum Allowable Servo Compensation Slew Rate [um/s] *)

    (* Radial Thermal Drift & Centerline Tilt Mechanics *)
    rCenterlineTiltX_urad           : REAL := 0.0;      (* Angular Tilt Drift in Gantry X-Z Plane [urad] *)
    rCenterlineTiltY_urad           : REAL := 0.0;      (* Angular Tilt Drift in Gantry Y-Z Plane [urad] *)
    rRadialDriftX_Raw_um            : REAL := 0.0;      (* Unfiltered Spindle Nose Radial Drift X [um] *)
    rRadialDriftY_Raw_um            : REAL := 0.0;      (* Unfiltered Spindle Nose Radial Drift Y [um] *)
    rRadialDriftX_Filt_um           : REAL := 0.0;      (* Filtered Spindle Nose Radial Drift X [um] *)
    rRadialDriftY_Filt_um           : REAL := 0.0;      (* Filtered Spindle Nose Radial Drift Y [um] *)

    (* ===================================================================================== *)
    (* 5.0 REGENERATIVE CHATTER DYNAMICS, DELAY BUFFER & SPECTRAL ESTIMATORS                 *)
    (* Delay Buffer for Surface Wave Modulation: tau = 60 / (N * Z_t)                        *)
    (* ===================================================================================== *)
    rDelayLine_Z                    : ARRAY[1..128] OF REAL; (* Circular Delay Buffer for Tool Surface Wave [um] *)
    iDelayIndex                     : INT := 1;              (* Active Circular Delay Write Pointer *)
    iDelayLength                    : INT := 20;             (* Active Tooth Passing Period Sample Count tau / Ts *)
    rToothPassingPeriod_s           : REAL := 0.001667;      (* Tooth Passing Time Period tau = 60 / (N * Z_t) [s] *)
    rToothPassingFreq_Hz            : REAL := 600.0;         (* Tooth Passing Excitation Frequency f_t = N * Z_t / 60 [Hz] *)
    rSpindleRotFreq_Hz              : REAL := 150.0;         (* Spindle Rotational Fundamental Frequency f_s = N / 60 [Hz] *)
    rDynamicChipThickness_um        : REAL := 18.5;          (* Instantaneous Dynamic Chip Thickness h(t) [um] *)
    rNominalChipThickness_um        : REAL := 25.0;          (* Nominal Kinematic Chip Thickness h_0 [um] *)
    rDelayedSurfaceZ_um             : REAL := 0.0;           (* Delayed Previous Tooth Surface Profile z(t - tau) [um] *)
    rCurrentSurfaceZ_um             : REAL := 0.0;           (* Current Instantaneous Tool Displacement z(t) [um] *)

    (* 2nd-Order IIR Digital Bandpass Filters for 4 Critical Frequency Bands *)
    (* Band 1: Spindle Rotational 1X Harmonic (e.g. 300-500 Hz) *)
    rIIR_B1_x1                      : REAL := 0.0; rIIR_B1_x2 : REAL := 0.0;
    rIIR_B1_y1                      : REAL := 0.0; rIIR_B1_y2 : REAL := 0.0;
    rIIR_B1_Output                  : REAL := 0.0;
    rRMS_Band1_1X                   : REAL := 0.0;

    (* Band 2: Tooth Passing Frequency (e.g. 1000-2000 Hz) *)
    rIIR_B2_x1                      : REAL := 0.0; rIIR_B2_x2 : REAL := 0.0;
    rIIR_B2_y1                      : REAL := 0.0; rIIR_B2_y2 : REAL := 0.0;
    rIIR_B2_Output                  : REAL := 0.0;
    rRMS_Band2_ToothPass            : REAL := 0.0;

    (* Band 3: Spindle Cartridge Primary Cantilever Bending Mode (1,250 Hz) *)
    rIIR_B3_x1                      : REAL := 0.0; rIIR_B3_x2 : REAL := 0.0;
    rIIR_B3_y1                      : REAL := 0.0; rIIR_B3_y2 : REAL := 0.0;
    rIIR_B3_Output                  : REAL := 0.0;
    rRMS_Band3_Mode1                : REAL := 0.0;

    (* Band 4: Toolholder/End Mill Second Flexural Bending Mode (2,450 Hz) *)
    rIIR_B4_x1                      : REAL := 0.0; rIIR_B4_x2 : REAL := 0.0;
    rIIR_B4_y1                      : REAL := 0.0; rIIR_B4_y2 : REAL := 0.0;
    rIIR_B4_Output                  : REAL := 0.0;
    rRMS_Band4_Mode2                : REAL := 0.0;

    (* Normalized Chatter Severity Index Evaluator *)
    rTotalRMS_Vibration             : REAL := 0.0;
    rChatterRatio                   : REAL := 0.0;
    rChatterThreshold_Warning       : REAL := 0.35;
    rChatterThreshold_Severe        : REAL := 0.70;
    bChatterActiveFlag              : BOOL := FALSE;
    bChatterSevereFlag              : BOOL := FALSE;

    (* ===================================================================================== *)
    (* 6.0 16x16 MULTIVARIABLE DISCRETE STATE-SPACE CYBER-PHYSICAL MODEL                     *)
    (* States x (16x1):                                                                      *)
    (*   x[1]:  Spindle axial compliance displacement z [um]                                 *)
    (*   x[2]:  Spindle axial compliance velocity z_dot [um/s]                               *)
    (*   x[3]:  Spindle radial X compliance displacement x [um]                              *)
    (*   x[4]:  Spindle radial X compliance velocity x_dot [um/s]                            *)
    (*   x[5]:  Spindle radial Y compliance displacement y [um]                              *)
    (*   x[6]:  Spindle radial Y compliance velocity y_dot [um/s]                            *)
    (*   x[7]:  Piezo stack X actuator dynamic strain/charge state [N]                      *)
    (*   x[8]:  Piezo stack Y actuator dynamic strain/charge state [N]                      *)
    (*   x[9]:  Front ceramic hybrid bearing thermal deviation Delta_T_b1 [deg C]           *)
    (*   x[10]: Rear floating roller bearing thermal deviation Delta_T_b2 [deg C]            *)
    (*   x[11]: Synchronous motor stator core thermal deviation Delta_T_stator [deg C]       *)
    (*   x[12]: Spindle rotating shaft cumulative thermal elongation z_th [um]               *)
    (*   x[13]: Regenerative delayed chip thickness wave state z(t - tau) [um]               *)
    (*   x[14]: Instantaneous tangential dynamic cutting force state F_cut [N]               *)
    (*   x[15]: Spindle rotational shaft speed perturbation Delta_Omega [rad/s]              *)
    (*   x[16]: Cooling jacket thermal extraction rate Q_cool [W]                            *)
    (* Controls u (8x1):                                                                     *)
    (*   u[1]:  Piezo X command voltage V_px [V] (-20 to +150V)                              *)
    (*   u[2]:  Piezo Y command voltage V_py [V] (-20 to +150V)                              *)
    (*   u[3]:  Z-axis CNC servo thermal growth compensation offset injection Z_comp [um]    *)
    (*   u[4]:  Spindle Speed Variation (SSV) speed trim command Delta_N_ssv [RPM]           *)
    (*   u[5]:  CNC cutting feedrate override pacing multiplier F_ovr [%]                    *)
    (*   u[6]:  Chiller proportional valve flow demand V_cool [%]                            *)
    (*   u[7]:  Oil-air micro-lubrication dosing pump pulse request P_lube [step]            *)
    (*   u[8]:  Active damping counter-force gain tuning parameter K_damp [N/(um/s)]         *)
    (* ===================================================================================== *)
    A_mat                           : ARRAY[1..16, 1..16] OF REAL;
    B_mat                           : ARRAY[1..16, 1..8] OF REAL;
    C_mat                           : ARRAY[1..16, 1..16] OF REAL;
    D_mat                           : ARRAY[1..16, 1..8] OF REAL;

    x_state                         : ARRAY[1..16] OF REAL;
    x_pred                          : ARRAY[1..16] OF REAL;
    x_ref                           : ARRAY[1..16] OF REAL;
    x_err                           : ARRAY[1..16] OF REAL;

    u_mpc                           : ARRAY[1..8] OF REAL;
    u_delta                         : ARRAY[1..8] OF REAL;
    u_prev                          : ARRAY[1..8] OF REAL;

    Q_diag                          : ARRAY[1..16] OF REAL;
    R_diag                          : ARRAY[1..8] OF REAL;
    P_diag                          : ARRAY[1..16] OF REAL;

    grad_J                          : ARRAY[1..8] OF REAL;
    H_diag                          : ARRAY[1..8] OF REAL;

    bMatricesInitialized            : BOOL := FALSE;
    iRow                            : INT := 1;
    iCol                            : INT := 1;
    iIter                           : INT := 1;
    rMpcStepSize                    : REAL := 0.0125;
    rQuadraticCostValue             : REAL := 0.0;

    (* ===================================================================================== *)
    (* 7.0 ACTIVE PIEZOELECTRIC COUNTER-DAMPING & SPINDLE SPEED VARIATION (SSV) SYNTHESIS    *)
    (* ===================================================================================== *)
    (* Direct Velocity Feedback (DVFB) Control Gains *)
    rPiezoGain_Velocity_Ns_m        : REAL := 1850.0;   (* Active Counter-Damping Gain [N*s/m] *)
    rPiezoGain_Position_N_m         : REAL := 45000.0;  (* Active Stiffness Augmentation Gain [N/m] *)
    rPiezoHysteresisState_X         : REAL := 0.0;      (* Piezo Hysteresis Bouc-Wen State Variable X *)
    rPiezoHysteresisState_Y         : REAL := 0.0;      (* Piezo Hysteresis Bouc-Wen State Variable Y *)
    rPiezoDemandedForce_X_N         : REAL := 0.0;      (* Target Counter-Force X Demand [N] *)
    rPiezoDemandedForce_Y_N         : REAL := 0.0;      (* Target Counter-Force Y Demand [N] *)

    (* Spindle Speed Variation (SSV) Waveform Generator *)
    rSSV_Phase_rad                  : REAL := 0.0;      (* Continuous Modulation Phase Accumulator [rad] *)
    rSSV_Frequency_Hz               : REAL := 2.50;     (* SSV Sinusoidal Modulation Frequency f_m [Hz] *)
    rSSV_AmplitudeRatio_RVA         : REAL := 0.12;     (* SSV Relative Speed Amplitude RVA = Delta_N / N_0 [-] *)
    rSSV_CalculatedTrim_RPM         : REAL := 0.0;      (* Real-Time Computed Speed Trim Value [RPM] *)

    (* ===================================================================================== *)
    (* 8.0 CLOSED-LOOP OIL-AIR MICRO-LUBRICATION & PREDICTIVE CHILLER PACING                 *)
    (* ===================================================================================== *)
    rLubeShotInterval_s             : REAL := 120.0;    (* Nominal Micro-Shot Injection Interval (120 s) [s] *)
    rLubePulseDuration_s            : REAL := 0.350;    (* Dosing Solenoid Injection Pulse Width (350 ms) [s] *)
    rStreakTimeoutWindow_s          : REAL := 12.0;     (* Maximum Time Allowed for Optical Streak Detection [s] *)
    iLubeTotalShots                 : DINT := 0;        (* Lifetime Cumulative Injection Shot Counter *)
    rLubeCumulativeVolume_cm3       : REAL := 0.0;      (* Cumulative Lubricant Consumed (0.03 cm3/shot) [cm3] *)
    bStreakArrivalLatched           : BOOL := FALSE;    (* Optical Streak Sensor Arrival Detection Latch *)
    bStreakMissingWarning           : BOOL := FALSE;    (* Lubrication Capillary Starvation Advisory *)

    (* Predictive Heat Balance & Chiller Pacing PID *)
    rEstimatedSpindleLosses_W       : REAL := 0.0;      (* Friction and Electromagnetic Spindle Heat Dissipation [W] *)
    rChillerHeatExtraction_W        : REAL := 0.0;      (* Real-Time Thermal Power Removed by Glycol Jacket [W] *)
    rChillerError_degC              : REAL := 0.0;      (* Temperature Error Relative to 20.0 deg C Datum [deg C] *)
    rChillerIntegralAccum_degC_s    : REAL := 0.0;      (* Chiller PID Integral Error Accumulator [deg C*s] *)
    rChillerPID_Output_pct          : REAL := 45.0;     (* Chiller Valve Demand Computed by Controller [%] *)

    (* ===================================================================================== *)
    (* 9.0 ISA-18.2 MULTI-TIERED ALARM THRESHOLDS, DEADANDS & BIT FLAGS                     *)
    (* Multi-tier hierarchy: High-High (HH), High (H), Low (L), Low-Low (LL)                 *)
    (* ===================================================================================== *)
    (* Spindle Bearing Radial Vibration [m/s2] *)
    c_rVib_HH_m_s2                  : REAL := 65.0;     (* Critical Bearing Vibration Trip (HH) [m/s2] *)
    c_rVib_H_m_s2                   : REAL := 35.0;     (* Elevated Bearing Vibration Warning (H) [m/s2] *)
    c_rVib_Deadband_m_s2            : REAL := 3.0;      (* Vibration Alarm Reset Hysteresis Deadband [m/s2] *)

    (* Front Ceramic Bearing Temperature [deg C] *)
    c_rBearingTemp_HH_degC          : REAL := 75.0;     (* Front Bearing Overheat Safety Trip (HH) [deg C] *)
    c_rBearingTemp_H_degC           : REAL := 62.0;     (* Front Bearing Elevated Temperature Warning (H) [deg C] *)
    c_rBearingTemp_Deadband_degC    : REAL := 2.5;      (* Bearing Thermal Hysteresis Deadband [deg C] *)

    (* Motor Stator Copper Winding Temperature [deg C] *)
    c_rStatorTemp_HH_degC           : REAL := 125.0;    (* Motor Stator Over-Temperature Safety Trip (HH) [deg C] *)
    c_rStatorTemp_H_degC            : REAL := 105.0;    (* Motor Stator Thermal Overload Warning (H) [deg C] *)
    c_rStatorTemp_Deadband_degC     : REAL := 3.0;      (* Stator Thermal Hysteresis Deadband [deg C] *)

    (* Oil-Air Lubrication Manifold Air Pressure [bar] *)
    c_rLubePress_HH_bar             : REAL := 4.80;     (* Lubrication High-High Pressure Blockage Trip [bar] *)
    c_rLubePress_H_bar              : REAL := 4.10;     (* Lubrication Elevated Pressure Warning [bar] *)
    c_rLubePress_L_bar              : REAL := 2.40;     (* Lubrication Low Pressure Advisory [bar] *)
    c_rLubePress_LL_bar             : REAL := 1.80;     (* Lubrication Pressure Loss Machine Protection Trip [bar] *)
    c_rLubePress_Deadband_bar       : REAL := 0.20;     (* Lubrication Pressure Deadband [bar] *)

    (* Chilled Glycol Coolant Flow Rate [l/min] *)
    c_rChillerFlow_L_lpm            : REAL := 8.50;     (* Chiller Inadequate Coolant Flow Warning [l/min] *)
    c_rChillerFlow_LL_lpm           : REAL := 5.00;     (* Chiller Loss of Coolant Flow Safety Trip [l/min] *)
    c_rChillerFlow_Deadband_lpm     : REAL := 0.60;     (* Coolant Flow Deadband [l/min] *)

    (* High-Frequency Acoustic Emission Tool Breakage Detection [dB] *)
    c_rAE_ToolBreakage_HH_dB        : REAL := 82.0;     (* Acoustic Emission Fracture Spike Trip [dB] *)
    c_rAE_ToolWear_H_dB             : REAL := 68.0;     (* Elevated Acoustic Emission Flank Wear Warning [dB] *)
    c_rAE_Deadband_dB               : REAL := 3.0;      (* Acoustic Emission Deadband [dB] *)

    (* Spindle Nose Dynamic Runout [um] *)
    c_rRunout_HH_um                 : REAL := 6.50;     (* Excessive Spindle Nose Runout Trip [um] *)
    c_rRunout_H_um                  : REAL := 3.80;     (* Elevated Spindle Tooling Runout Warning [um] *)
    c_rRunout_Deadband_um           : REAL := 0.50;     (* Runout Hysteresis Deadband [um] *)

    (* Internal Latched Alarm Flags *)
    bAlarm_Vibration_HH             : BOOL := FALSE;
    bAlarm_Vibration_H              : BOOL := FALSE;
    bAlarm_BearingTemp_HH           : BOOL := FALSE;
    bAlarm_BearingTemp_H            : BOOL := FALSE;
    bAlarm_StatorTemp_HH            : BOOL := FALSE;
    bAlarm_StatorTemp_H             : BOOL := FALSE;
    bAlarm_LubePress_LL             : BOOL := FALSE;
    bAlarm_LubePress_L              : BOOL := FALSE;
    bAlarm_LubePress_H              : BOOL := FALSE;
    bAlarm_LubePress_HH             : BOOL := FALSE;
    bAlarm_ChillerFlow_LL           : BOOL := FALSE;
    bAlarm_ChillerFlow_L            : BOOL := FALSE;
    bAlarm_AE_ToolBreak_HH          : BOOL := FALSE;
    bAlarm_AE_ToolWear_H            : BOOL := FALSE;
    bAlarm_Runout_HH                : BOOL := FALSE;
    bAlarm_Runout_H                 : BOOL := FALSE;
    bAlarm_ChatterSevere_HH         : BOOL := FALSE;
    bAlarm_PiezoAmpFault_HH         : BOOL := FALSE;
    bAlarm_SensorDegraded_H         : BOOL := FALSE;
    bAlarm_SensorFailureTrip_HH     : BOOL := FALSE;

    (* Temporary Loop Registers & Math Accumulators *)
    iLoopIdx                        : INT := 0;
    rTempCalc1                      : REAL := 0.0;
    rTempCalc2                      : REAL := 0.0;
    rTempCalc3                      : REAL := 0.0;
    rTempCalc4                      : REAL := 0.0;
END_VAR
""")

    # =========================================================================
    # 4. PHASE 1: SIL-3 MASTER SAFETY INTERLOCKS & SAFE TORQUE OFF (STO)
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 1: SIL-3 MASTER SAFETY INTERLOCKS & SAFE TORQUE OFF (STO) EVALUATION                  === *)
(* ================================================================================================= *)
(* Evaluates hardwired emergency stop, master system enable, front bearing over-temperature,         *)
(* extreme vibration chatter, lubrication loss, and piezoelectric amplifier health.                  *)
(* Any critical condition trips Safe Torque Off (STO), clamps piezo actuators, and forces E-Stop.   *)

dwAlarmWord1 := 16#0000_0000;
dwAlarmWord2 := 16#0000_0000;
dwAlarmWord3 := 16#0000_0000;

(* Master Interlock 1.1: Active-High Hardwired SIL-3 Emergency Stop Relay Check *)
IF NOT bEmergencyStop THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: Emergency Stop Circuit Tripped *)
END_IF;

(* Master Interlock 1.2: Machine Master Enable Permissive Lost *)
IF NOT bEnableSystem THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: Machine Automation Master Enable Dropped *)
END_IF;

(* Master Interlock 1.3: HSK-A63 Tool Clamping Drawbar Unclamped During Spindle Rotation *)
IF (NOT bToolClampedHSK) AND (rVotedSpindleSpeed_RPM > 50.0) THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: Tool Unclamped While Spindle Rotating Trip *)
END_IF;

(* Master Interlock 1.4: Spindle Bearing Temperature High-High Safety Trip (> 75.0 deg C) *)
IF rVotedBearingTemp_degC > c_rBearingTemp_HH_degC THEN
    bAlarm_BearingTemp_HH := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Ceramic Hybrid Bearing Temperature HH Trip *)
ELSIF rVotedBearingTemp_degC < (c_rBearingTemp_HH_degC - c_rBearingTemp_Deadband_degC) THEN
    IF bResetAlarms THEN
        bAlarm_BearingTemp_HH := FALSE;
    END_IF;
END_IF;

(* Master Interlock 1.5: Built-in Synchronous Motor Stator Copper Winding High-High Trip (> 125.0 deg C) *)
IF rTempStatorWinding_degC > c_rStatorTemp_HH_degC THEN
    bAlarm_StatorTemp_HH := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Bit 4: Motor Stator Winding Overheat HH Trip *)
ELSIF rTempStatorWinding_degC < (c_rStatorTemp_HH_degC - c_rStatorTemp_Deadband_degC) THEN
    IF bResetAlarms THEN
        bAlarm_StatorTemp_HH := FALSE;
    END_IF;
END_IF;

(* Master Interlock 1.6: Spindle Bearing Housing Vibration High-High Trip (> 65.0 m/s2) *)
IF (rVotedVibration_X_m_s2 > c_rVib_HH_m_s2) OR 
   (rVotedVibration_Y_m_s2 > c_rVib_HH_m_s2) OR 
   (rVotedVibration_Z_m_s2 > c_rVib_HH_m_s2) THEN
    bAlarm_Vibration_HH := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; (* Bit 5: Bearing Housing Destructive Vibration HH Trip *)
ELSIF (rVotedVibration_X_m_s2 < (c_rVib_HH_m_s2 - c_rVib_Deadband_m_s2)) AND
      (rVotedVibration_Y_m_s2 < (c_rVib_HH_m_s2 - c_rVib_Deadband_m_s2)) AND
      (rVotedVibration_Z_m_s2 < (c_rVib_HH_m_s2 - c_rVib_Deadband_m_s2)) THEN
    IF bResetAlarms THEN
        bAlarm_Vibration_HH := FALSE;
    END_IF;
END_IF;

(* Master Interlock 1.7: Oil-Air Micro-Lubrication Low-Low Pressure Loss Trip (< 1.8 bar) *)
IF rLubricationPressure_bar < c_rLubePress_LL_bar THEN
    bAlarm_LubePress_LL := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* Bit 6: Oil-Air Lubrication Pressure Loss LL Trip *)
ELSIF rLubricationPressure_bar > (c_rLubePress_LL_bar + c_rLubePress_Deadband_bar) THEN
    IF bResetAlarms THEN
        bAlarm_LubePress_LL := FALSE;
    END_IF;
END_IF;

(* Master Interlock 1.8: Piezoelectric High-Voltage Power Amplifier Fault *)
IF NOT bPiezoAmplifierReady THEN
    bAlarm_PiezoAmpFault_HH := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* Bit 7: Piezo Amplifier Hardware Trip *)
ELSIF bResetAlarms THEN
    bAlarm_PiezoAmpFault_HH := FALSE;
END_IF;

(* Master Safety Action: Trigger Safe Torque Off (STO) & Clamp Piezo Stack *)
IF (dwAlarmWord1 <> 16#0000_0000) THEN
    bSpindleDriveSTO_Trip := TRUE;
    bPiezoClampActive := TRUE;
    rPiezoVoltage_X_V := 0.0;
    rPiezoVoltage_Y_V := 0.0;
    rFeedrateOverride_pct := 0.0;
    iState := 120; (* Force Transition to EMERGENCY E-STOP STAGE *)
ELSE
    bSpindleDriveSTO_Trip := FALSE;
    bPiezoClampActive := FALSE;
END_IF;
""")

    # =========================================================================
    # 5. PHASE 2: 2oo3 TMR SENSOR VOTING & DISCREPANCY TIMERS
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS          === *)
(* ================================================================================================= *)
(* Executes deterministic median voting across tri-axial accelerometers (X, Y, Z), front bearing     *)
(* temperature RTDs, and spindle optical speed encoders. Monitors inter-channel spread, tracks       *)
(* persistence discrepancy timers, and degrades gracefully from 2oo3 to 1oo2, or latches a trip.    *)

dwDegradationWord := 16#0000_0000;

(* --- GROUP 2.1: SPINDLE FRONT HOUSING X-AXIS ACCELEROMETERS [m/s2] --- *)
rDev_AccX_AB := ABS(rVibrationAccel_X_A - rVibrationAccel_X_B);
rDev_AccX_BC := ABS(rVibrationAccel_X_B - rVibrationAccel_X_C);
rDev_AccX_CA := ABS(rVibrationAccel_X_C - rVibrationAccel_X_A);

bAccX_A_Healthy := (rVibrationAccel_X_A >= -250.0) AND (rVibrationAccel_X_A <= 250.0);
bAccX_B_Healthy := (rVibrationAccel_X_B >= -250.0) AND (rVibrationAccel_X_B <= 250.0);
bAccX_C_Healthy := (rVibrationAccel_X_C >= -250.0) AND (rVibrationAccel_X_C <= 250.0);

IF bAccX_A_Healthy AND bAccX_B_Healthy AND bAccX_C_Healthy THEN
    bAccX_Degraded_1oo2 := FALSE;
    bAccX_Trip := FALSE;
    (* Deterministic Median Selection *)
    IF ((rVibrationAccel_X_A >= rVibrationAccel_X_B) AND (rVibrationAccel_X_A <= rVibrationAccel_X_C)) OR
       ((rVibrationAccel_X_A >= rVibrationAccel_X_C) AND (rVibrationAccel_X_A <= rVibrationAccel_X_B)) THEN
        rVotedVibration_X_m_s2 := rVibrationAccel_X_A;
    ELSIF ((rVibrationAccel_X_B >= rVibrationAccel_X_A) AND (rVibrationAccel_X_B <= rVibrationAccel_X_C)) OR
          ((rVibrationAccel_X_B >= rVibrationAccel_X_C) AND (rVibrationAccel_X_B <= rVibrationAccel_X_A)) THEN
        rVotedVibration_X_m_s2 := rVibrationAccel_X_B;
    ELSE
        rVotedVibration_X_m_s2 := rVibrationAccel_X_C;
    END_IF;
    (* Discrepancy Persistence Monitor *)
    IF (rDev_AccX_AB > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccX_BC > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccX_CA > c_rAccelDiscrepancyTol_m_s2) THEN
        rTimer_AccX_Discrep := rTimer_AccX_Discrep + c_ScanTime_Ts_s;
        IF rTimer_AccX_Discrep > c_rMaxDiscrepancyTime_s THEN
            dwDegradationWord := dwDegradationWord OR 16#0000_0001; (* Accel X Triplet Discrepancy Flag *)
        END_IF;
    ELSE
        rTimer_AccX_Discrep := 0.0;
    END_IF;
ELSIF bAccX_A_Healthy AND bAccX_B_Healthy THEN
    bAccX_Degraded_1oo2 := TRUE;
    rVotedVibration_X_m_s2 := (rVibrationAccel_X_A + rVibrationAccel_X_B) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0002; (* Accel X Degraded to 1oo2 (Channel C Failed) *)
ELSIF bAccX_B_Healthy AND bAccX_C_Healthy THEN
    bAccX_Degraded_1oo2 := TRUE;
    rVotedVibration_X_m_s2 := (rVibrationAccel_X_B + rVibrationAccel_X_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0004; (* Accel X Degraded to 1oo2 (Channel A Failed) *)
ELSIF bAccX_A_Healthy AND bAccX_C_Healthy THEN
    bAccX_Degraded_1oo2 := TRUE;
    rVotedVibration_X_m_s2 := (rVibrationAccel_X_A + rVibrationAccel_X_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0008; (* Accel X Degraded to 1oo2 (Channel B Failed) *)
ELSE
    bAccX_Trip := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0000_0010; (* Accel X Multi-Channel Failure Trip *)
END_IF;

(* --- GROUP 2.2: SPINDLE FRONT HOUSING Y-AXIS ACCELEROMETERS [m/s2] --- *)
rDev_AccY_AB := ABS(rVibrationAccel_Y_A - rVibrationAccel_Y_B);
rDev_AccY_BC := ABS(rVibrationAccel_Y_B - rVibrationAccel_Y_C);
rDev_AccY_CA := ABS(rVibrationAccel_Y_C - rVibrationAccel_Y_A);

bAccY_A_Healthy := (rVibrationAccel_Y_A >= -250.0) AND (rVibrationAccel_Y_A <= 250.0);
bAccY_B_Healthy := (rVibrationAccel_Y_B >= -250.0) AND (rVibrationAccel_Y_B <= 250.0);
bAccY_C_Healthy := (rVibrationAccel_Y_C >= -250.0) AND (rVibrationAccel_Y_C <= 250.0);

IF bAccY_A_Healthy AND bAccY_B_Healthy AND bAccY_C_Healthy THEN
    bAccY_Degraded_1oo2 := FALSE;
    bAccY_Trip := FALSE;
    IF ((rVibrationAccel_Y_A >= rVibrationAccel_Y_B) AND (rVibrationAccel_Y_A <= rVibrationAccel_Y_C)) OR
       ((rVibrationAccel_Y_A >= rVibrationAccel_Y_C) AND (rVibrationAccel_Y_A <= rVibrationAccel_Y_B)) THEN
        rVotedVibration_Y_m_s2 := rVibrationAccel_Y_A;
    ELSIF ((rVibrationAccel_Y_B >= rVibrationAccel_Y_A) AND (rVibrationAccel_Y_B <= rVibrationAccel_Y_C)) OR
          ((rVibrationAccel_Y_B >= rVibrationAccel_Y_C) AND (rVibrationAccel_Y_B <= rVibrationAccel_Y_A)) THEN
        rVotedVibration_Y_m_s2 := rVibrationAccel_Y_B;
    ELSE
        rVotedVibration_Y_m_s2 := rVibrationAccel_Y_C;
    END_IF;
    IF (rDev_AccY_AB > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccY_BC > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccY_CA > c_rAccelDiscrepancyTol_m_s2) THEN
        rTimer_AccY_Discrep := rTimer_AccY_Discrep + c_ScanTime_Ts_s;
        IF rTimer_AccY_Discrep > c_rMaxDiscrepancyTime_s THEN
            dwDegradationWord := dwDegradationWord OR 16#0000_0020; (* Accel Y Triplet Discrepancy Flag *)
        END_IF;
    ELSE
        rTimer_AccY_Discrep := 0.0;
    END_IF;
ELSIF bAccY_A_Healthy AND bAccY_B_Healthy THEN
    bAccY_Degraded_1oo2 := TRUE;
    rVotedVibration_Y_m_s2 := (rVibrationAccel_Y_A + rVibrationAccel_Y_B) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0040;
ELSIF bAccY_B_Healthy AND bAccY_C_Healthy THEN
    bAccY_Degraded_1oo2 := TRUE;
    rVotedVibration_Y_m_s2 := (rVibrationAccel_Y_B + rVibrationAccel_Y_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0080;
ELSIF bAccY_A_Healthy AND bAccY_C_Healthy THEN
    bAccY_Degraded_1oo2 := TRUE;
    rVotedVibration_Y_m_s2 := (rVibrationAccel_Y_A + rVibrationAccel_Y_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0100;
ELSE
    bAccY_Trip := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0000_0200;
END_IF;

(* --- GROUP 2.3: SPINDLE FRONT HOUSING Z-AXIS ACCELEROMETERS [m/s2] --- *)
rDev_AccZ_AB := ABS(rVibrationAccel_Z_A - rVibrationAccel_Z_B);
rDev_AccZ_BC := ABS(rVibrationAccel_Z_B - rVibrationAccel_Z_C);
rDev_AccZ_CA := ABS(rVibrationAccel_Z_C - rVibrationAccel_Z_A);

bAccZ_A_Healthy := (rVibrationAccel_Z_A >= -250.0) AND (rVibrationAccel_Z_A <= 250.0);
bAccZ_B_Healthy := (rVibrationAccel_Z_B >= -250.0) AND (rVibrationAccel_Z_B <= 250.0);
bAccZ_C_Healthy := (rVibrationAccel_Z_C >= -250.0) AND (rVibrationAccel_Z_C <= 250.0);

IF bAccZ_A_Healthy AND bAccZ_B_Healthy AND bAccZ_C_Healthy THEN
    bAccZ_Degraded_1oo2 := FALSE;
    bAccZ_Trip := FALSE;
    IF ((rVibrationAccel_Z_A >= rVibrationAccel_Z_B) AND (rVibrationAccel_Z_A <= rVibrationAccel_Z_C)) OR
       ((rVibrationAccel_Z_A >= rVibrationAccel_Z_C) AND (rVibrationAccel_Z_A <= rVibrationAccel_Z_B)) THEN
        rVotedVibration_Z_m_s2 := rVibrationAccel_Z_A;
    ELSIF ((rVibrationAccel_Z_B >= rVibrationAccel_Z_A) AND (rVibrationAccel_Z_B <= rVibrationAccel_Z_C)) OR
          ((rVibrationAccel_Z_B >= rVibrationAccel_Z_C) AND (rVibrationAccel_Z_B <= rVibrationAccel_Z_A)) THEN
        rVotedVibration_Z_m_s2 := rVibrationAccel_Z_B;
    ELSE
        rVotedVibration_Z_m_s2 := rVibrationAccel_Z_C;
    END_IF;
    IF (rDev_AccZ_AB > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccZ_BC > c_rAccelDiscrepancyTol_m_s2) OR 
       (rDev_AccZ_CA > c_rAccelDiscrepancyTol_m_s2) THEN
        rTimer_AccZ_Discrep := rTimer_AccZ_Discrep + c_ScanTime_Ts_s;
        IF rTimer_AccZ_Discrep > c_rMaxDiscrepancyTime_s THEN
            dwDegradationWord := dwDegradationWord OR 16#0000_0400; (* Accel Z Triplet Discrepancy Flag *)
        END_IF;
    ELSE
        rTimer_AccZ_Discrep := 0.0;
    END_IF;
ELSIF bAccZ_A_Healthy AND bAccZ_B_Healthy THEN
    bAccZ_Degraded_1oo2 := TRUE;
    rVotedVibration_Z_m_s2 := (rVibrationAccel_Z_A + rVibrationAccel_Z_B) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_0800;
ELSIF bAccZ_B_Healthy AND bAccZ_C_Healthy THEN
    bAccZ_Degraded_1oo2 := TRUE;
    rVotedVibration_Z_m_s2 := (rVibrationAccel_Z_B + rVibrationAccel_Z_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_1000;
ELSIF bAccZ_A_Healthy AND bAccZ_C_Healthy THEN
    bAccZ_Degraded_1oo2 := TRUE;
    rVotedVibration_Z_m_s2 := (rVibrationAccel_Z_A + rVibrationAccel_Z_C) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0000_2000;
ELSE
    bAccZ_Trip := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0000_4000;
END_IF;

(* --- GROUP 2.4: FRONT BEARING DEDICATED RTDs [deg C] --- *)
rDev_TempB_AB := ABS(rTempBearing_A_degC - rTempBearing_B_degC);
rDev_TempB_BC := ABS(rTempBearing_B_degC - rTempBearing_C_degC);
rDev_TempB_CA := ABS(rTempBearing_C_degC - rTempBearing_A_degC);

bTempB_A_Healthy := (rTempBearing_A_degC >= 0.0) AND (rTempBearing_A_degC <= 120.0);
bTempB_B_Healthy := (rTempBearing_B_degC >= 0.0) AND (rTempBearing_B_degC <= 120.0);
bTempB_C_Healthy := (rTempBearing_C_degC >= 0.0) AND (rTempBearing_C_degC <= 120.0);

IF bTempB_A_Healthy AND bTempB_B_Healthy AND bTempB_C_Healthy THEN
    bTempB_Degraded_1oo2 := FALSE;
    bTempB_Trip := FALSE;
    IF ((rTempBearing_A_degC >= rTempBearing_B_degC) AND (rTempBearing_A_degC <= rTempBearing_C_degC)) OR
       ((rTempBearing_A_degC >= rTempBearing_C_degC) AND (rTempBearing_A_degC <= rTempBearing_B_degC)) THEN
        rVotedBearingTemp_degC := rTempBearing_A_degC;
    ELSIF ((rTempBearing_B_degC >= rTempBearing_A_degC) AND (rTempBearing_B_degC <= rTempBearing_C_degC)) OR
          ((rTempBearing_B_degC >= rTempBearing_C_degC) AND (rTempBearing_B_degC <= rTempBearing_A_degC)) THEN
        rVotedBearingTemp_degC := rTempBearing_B_degC;
    ELSE
        rVotedBearingTemp_degC := rTempBearing_C_degC;
    END_IF;
    IF (rDev_TempB_AB > c_rTempDiscrepancyTol_degC) OR 
       (rDev_TempB_BC > c_rTempDiscrepancyTol_degC) OR 
       (rDev_TempB_CA > c_rTempDiscrepancyTol_degC) THEN
        rTimer_TempB_Discrep := rTimer_TempB_Discrep + c_ScanTime_Ts_s;
        IF rTimer_TempB_Discrep > c_rMaxDiscrepancyTime_s THEN
            dwDegradationWord := dwDegradationWord OR 16#0000_8000; (* Bearing RTD Discrepancy Flag *)
        END_IF;
    ELSE
        rTimer_TempB_Discrep := 0.0;
    END_IF;
ELSIF bTempB_A_Healthy AND bTempB_B_Healthy THEN
    bTempB_Degraded_1oo2 := TRUE;
    rVotedBearingTemp_degC := (rTempBearing_A_degC + rTempBearing_B_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0001_0000;
ELSIF bTempB_B_Healthy AND bTempB_C_Healthy THEN
    bTempB_Degraded_1oo2 := TRUE;
    rVotedBearingTemp_degC := (rTempBearing_B_degC + rTempBearing_C_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0002_0000;
ELSIF bTempB_A_Healthy AND bTempB_C_Healthy THEN
    bTempB_Degraded_1oo2 := TRUE;
    rVotedBearingTemp_degC := (rTempBearing_A_degC + rTempBearing_C_degC) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0004_0000;
ELSE
    bTempB_Trip := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0008_0000;
END_IF;

(* --- GROUP 2.5: SPINDLE TACHOMETER OPTICAL RING ENCODERS [RPM] --- *)
rDev_Speed_AB := ABS(rSpindleSpeed_EncA_RPM - rSpindleSpeed_EncB_RPM);
rDev_Speed_BC := ABS(rSpindleSpeed_EncB_RPM - rSpindleSpeed_EncC_RPM);
rDev_Speed_CA := ABS(rSpindleSpeed_EncC_RPM - rSpindleSpeed_EncA_RPM);

bSpeed_A_Healthy := (rSpindleSpeed_EncA_RPM >= -500.0) AND (rSpindleSpeed_EncA_RPM <= 35000.0);
bSpeed_B_Healthy := (rSpindleSpeed_EncB_RPM >= -500.0) AND (rSpindleSpeed_EncB_RPM <= 35000.0);
bSpeed_C_Healthy := (rSpindleSpeed_EncC_RPM >= -500.0) AND (rSpindleSpeed_EncC_RPM <= 35000.0);

IF bSpeed_A_Healthy AND bSpeed_B_Healthy AND bSpeed_C_Healthy THEN
    bSpeed_Degraded_1oo2 := FALSE;
    bSpeed_Trip := FALSE;
    IF ((rSpindleSpeed_EncA_RPM >= rSpindleSpeed_EncB_RPM) AND (rSpindleSpeed_EncA_RPM <= rSpindleSpeed_EncC_RPM)) OR
       ((rSpindleSpeed_EncA_RPM >= rSpindleSpeed_EncC_RPM) AND (rSpindleSpeed_EncA_RPM <= rSpindleSpeed_EncB_RPM)) THEN
        rVotedSpindleSpeed_RPM := rSpindleSpeed_EncA_RPM;
    ELSIF ((rSpindleSpeed_EncB_RPM >= rSpindleSpeed_EncA_RPM) AND (rSpindleSpeed_EncB_RPM <= rSpindleSpeed_EncC_RPM)) OR
          ((rSpindleSpeed_EncB_RPM >= rSpindleSpeed_EncC_RPM) AND (rSpindleSpeed_EncB_RPM <= rSpindleSpeed_EncA_RPM)) THEN
        rVotedSpindleSpeed_RPM := rSpindleSpeed_EncB_RPM;
    ELSE
        rVotedSpindleSpeed_RPM := rSpindleSpeed_EncC_RPM;
    END_IF;
    IF (rDev_Speed_AB > c_rSpeedDiscrepancyTol_RPM) OR 
       (rDev_Speed_BC > c_rSpeedDiscrepancyTol_RPM) OR 
       (rDev_Speed_CA > c_rSpeedDiscrepancyTol_RPM) THEN
        rTimer_Speed_Discrep := rTimer_Speed_Discrep + c_ScanTime_Ts_s;
        IF rTimer_Speed_Discrep > c_rMaxDiscrepancyTime_s THEN
            dwDegradationWord := dwDegradationWord OR 16#0010_0000; (* Spindle Tach Discrepancy Flag *)
        END_IF;
    ELSE
        rTimer_Speed_Discrep := 0.0;
    END_IF;
ELSIF bSpeed_A_Healthy AND bSpeed_B_Healthy THEN
    bSpeed_Degraded_1oo2 := TRUE;
    rVotedSpindleSpeed_RPM := (rSpindleSpeed_EncA_RPM + rSpindleSpeed_EncB_RPM) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0020_0000;
ELSIF bSpeed_B_Healthy AND bSpeed_C_Healthy THEN
    bSpeed_Degraded_1oo2 := TRUE;
    rVotedSpindleSpeed_RPM := (rSpindleSpeed_EncB_RPM + rSpindleSpeed_EncC_RPM) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0040_0000;
ELSIF bSpeed_A_Healthy AND bSpeed_C_Healthy THEN
    bSpeed_Degraded_1oo2 := TRUE;
    rVotedSpindleSpeed_RPM := (rSpindleSpeed_EncA_RPM + rSpindleSpeed_EncC_RPM) * 0.5;
    dwDegradationWord := dwDegradationWord OR 16#0080_0000;
ELSE
    bSpeed_Trip := TRUE;
    dwDegradationWord := dwDegradationWord OR 16#0100_0000;
END_IF;
""")

    # =========================================================================
    # 6. PHASE 3: 10-NODE FINITE-DIFFERENCE SPINDLE THERMAL EXPANSION
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 3: 10-NODE FINITE-DIFFERENCE SPINDLE AXIAL & RADIAL THERMAL GROWTH INTEGRATION        === *)
(* ================================================================================================= *)
(* Computes the real-time thermal expansion integral along the 10 discretized axial shaft stations.   *)
(* Accounts for temperature-dependent expansion coefficient alpha(T) and evaluates radial drift      *)
(* vector (dx, dy). Limits rate-of-change slew rate before injecting offsets into CNC servo loop.     *)

(* Map Measured RTD & FBG Temperatures to 10 Finite-Difference Axial Nodes *)
rNodeTemp_degC[1]  := rTempSpindleNose_degC;                                            (* Node 1: Spindle Nose / HSK Taper *)
rNodeTemp_degC[2]  := rVotedBearingTemp_degC;                                          (* Node 2: Front Bearing Outer Set 1 *)
rNodeTemp_degC[3]  := (rVotedBearingTemp_degC * 0.70) + (rTempFrontBearing_degC * 0.30);(* Node 3: Front Bearing Set 2 / Labyrinth *)
rNodeTemp_degC[4]  := (rVotedBearingTemp_degC * 0.50) + (rTempStatorCore_degC * 0.50);  (* Node 4: Spindle Housing Forward Sleeve *)
rNodeTemp_degC[5]  := rTempStatorWinding_degC;                                         (* Node 5: Motor Stator Front End-Turn *)
rNodeTemp_degC[6]  := rTempStatorCore_degC;                                            (* Node 6: Stator Core Center Lamination *)
rNodeTemp_degC[7]  := (rTempStatorWinding_degC * 0.60) + (rTempRearBearing_degC * 0.40);(* Node 7: Stator Rear End-Turn *)
rNodeTemp_degC[8]  := rTempRearBearing_degC;                                           (* Node 8: Rear Floating Roller Bearing *)
rNodeTemp_degC[9]  := rTempChillerOutlet_degC;                                         (* Node 9: Cooling Jacket Return Manifold *)
rNodeTemp_degC[10] := (rTempChillerInlet_degC * 0.50) + (rTempAmbientGantry_degC * 0.50); (* Node 10: Rear Spindle Encoder Housing *)

(* Calculate Local Temperature Deviations Delta_T and Second-Order Alpha Coefficients *)
FOR iLoopIdx := 1 TO 10 DO
    rNodeDeltaT_degC[iLoopIdx] := rNodeTemp_degC[iLoopIdx] - c_NominalChillerSetpoint_degC;
    rNodeAlpha_1_K[iLoopIdx] := c_SteelAlpha_1_K * (1.0 + (c_AlphaTempCoeff * rNodeDeltaT_degC[iLoopIdx]));
END_FOR;

(* Numerical Trapezoidal Quadrature Along 9 Discretized Shaft Segments: *)
(* dL_segment_i = (dz_i / 2) * [ alpha_i * Delta_T_i + alpha_{i+1} * Delta_T_{i+1} ] *)
rRawThermalGrowth_um := 0.0;
FOR iLoopIdx := 1 TO 9 DO
    rSegmentElongation_um[iLoopIdx] := (c_SegmentDZ_mm[iLoopIdx] * 0.5) * 
        ((rNodeAlpha_1_K[iLoopIdx] * rNodeDeltaT_degC[iLoopIdx]) + 
         (rNodeAlpha_1_K[iLoopIdx + 1] * rNodeDeltaT_degC[iLoopIdx + 1])) * 1000.0;
    rRawThermalGrowth_um := rRawThermalGrowth_um + rSegmentElongation_um[iLoopIdx];
END_FOR;

(* First-Order Low-Pass Filter on Calculated Axial Growth (tau_f = 0.25 s) *)
rFilteredThermalGrowth_um := (rFilteredThermalGrowth_um * 0.996) + (rRawThermalGrowth_um * 0.004);
rCalculatedThermalGrowth_um := rFilteredThermalGrowth_um;

(* Slew-Rate Limiter on Z-Axis Servo Offset Injection (+/- 6.0 um/s) *)
rThermalGrowthRate_um_s := (rFilteredThermalGrowth_um - rPrevCompOffset_um) / c_ScanTime_Ts_s;
IF rThermalGrowthRate_um_s > c_rMaxThermalCompSlewRate_um_s THEN
    rZAxisThermalCompOffset_um := rPrevCompOffset_um + (c_rMaxThermalCompSlewRate_um_s * c_ScanTime_Ts_s);
ELSIF rThermalGrowthRate_um_s < (-1.0 * c_rMaxThermalCompSlewRate_um_s) THEN
    rZAxisThermalCompOffset_um := rPrevCompOffset_um - (c_rMaxThermalCompSlewRate_um_s * c_ScanTime_Ts_s);
ELSE
    rZAxisThermalCompOffset_um := rFilteredThermalGrowth_um;
END_IF;
rPrevCompOffset_um := rZAxisThermalCompOffset_um;

(* 2D Radial Thermal Drift & Centerline Tilt Mechanics *)
(* Asymmetric thermal gradients between front bearing and stator generate spindle nose radial drift *)
rCenterlineTiltX_urad := ((rNodeTemp_degC[2] - rNodeTemp_degC[8]) * 1.85) + 
                         ((rTempChillerOutlet_degC - rTempChillerInlet_degC) * 0.65);
rCenterlineTiltY_urad := ((rNodeTemp_degC[5] - rTempAmbientGantry_degC) * 1.45) - 
                         ((rNodeTemp_degC[6] - c_NominalChillerSetpoint_degC) * 0.95);

rRadialDriftX_Raw_um := (rCenterlineTiltX_urad * (c_ShaftLength_m * 1000.0)) * 0.000001;
rRadialDriftY_Raw_um := (rCenterlineTiltY_urad * (c_ShaftLength_m * 1000.0)) * 0.000001;

rRadialDriftX_Filt_um := (rRadialDriftX_Filt_um * 0.998) + (rRadialDriftX_Raw_um * 0.002);
rRadialDriftY_Filt_um := (rRadialDriftY_Filt_um * 0.998) + (rRadialDriftY_Raw_um * 0.002);

rXAxisRadialDriftOffset_um := rRadialDriftX_Filt_um;
rYAxisRadialDriftOffset_um := rRadialDriftY_Filt_um;
rCalculatedRadialDrift_um := SQRT((rRadialDriftX_Filt_um * rRadialDriftX_Filt_um) + 
                                  (rRadialDriftY_Filt_um * rRadialDriftY_Filt_um));
""")

    # =========================================================================
    # 7. PHASE 4: REGENERATIVE CHATTER VIBRATION SPECTRAL ESTIMATION & SLD
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 4: REAL-TIME REGENERATIVE CHATTER VIBRATION SPECTRAL ESTIMATION & SLD                 === *)
(* ================================================================================================= *)
(* Discretizes circular delay buffer for tooth passing modulation wave: tau = 60 / (N * Z_t).        *)
(* Evaluates dynamic cutting force F_cut(t) = K_t * b * [ h_0 - z(t) + z(t - tau) ].                *)
(* Executes 4 parallel 2nd-order IIR bandpass filters on vibration signal to detect chatter peaks.   *)

(* Tooth Passing Period & Delay Buffer Pointer Scheduling *)
IF rVotedSpindleSpeed_RPM > 100.0 THEN
    rToothPassingFreq_Hz := (rVotedSpindleSpeed_RPM * INT_TO_REAL(iToolFluteCount)) / 60.0;
    rToothPassingPeriod_s := 1.0 / rToothPassingFreq_Hz;
    rSpindleRotFreq_Hz := rVotedSpindleSpeed_RPM / 60.0;
    
    (* Circular Delay Length in Synchronous Scan Ticks (tau / Ts) *)
    iDelayLength := REAL_TO_INT(rToothPassingPeriod_s / c_ScanTime_Ts_s);
    IF iDelayLength < 2 THEN
        iDelayLength := 2;
    ELSIF iDelayLength > 120 THEN
        iDelayLength := 120;
    END_IF;
ELSE
    rToothPassingFreq_Hz := 0.0;
    rToothPassingPeriod_s := 0.010;
    iDelayLength := 10;
END_IF;

(* Advance Circular Delay Pointer & Extract Delayed Tool Displacement z(t - tau) *)
iDelayIndex := iDelayIndex + 1;
IF iDelayIndex > iDelayLength THEN
    iDelayIndex := 1;
END_IF;
rDelayedSurfaceZ_um := rDelayLine_Z[iDelayIndex];

(* Estimate Current Tool Tip Axial Compliance Displacement from Voted Acceleration *)
rCurrentSurfaceZ_um := (rVotedVibration_Z_m_s2 / ((2.0 * c_Pi * 1250.0) * (2.0 * c_Pi * 1250.0))) * 1000000.0;
rDelayLine_Z[iDelayIndex] := rCurrentSurfaceZ_um;

(* Regenerative Dynamic Chip Thickness Formulation (Altintas & Budak Orthogonal Model) *)
IF bInCutSignalFromCNC AND (rProgrammedCutDepth_mm > 0.01) THEN
    rNominalChipThickness_um := (rCommandFeedrate_mmpm / (rVotedSpindleSpeed_RPM * INT_TO_REAL(iToolFluteCount))) * 1000.0;
    rDynamicChipThickness_um := rNominalChipThickness_um - (rCurrentSurfaceZ_um - rDelayedSurfaceZ_um);
    IF rDynamicChipThickness_um < 0.0 THEN
        rDynamicChipThickness_um := 0.0; (* Tool Fly-Off Cutting Nonlinearity *)
    END_IF;
    
    (* Dynamic Resultant Tangential Cutting Force *)
    rEstimatedCuttingForce_N := (c_CutCoeff_Kt_N_mm2 * (rProgrammedCutDepth_mm * (rDynamicChipThickness_um * 0.001)));
ELSE
    rNominalChipThickness_um := 0.0;
    rDynamicChipThickness_um := 0.0;
    rEstimatedCuttingForce_N := 0.0;
END_IF;

(* 2nd-Order IIR Digital Bandpass Filtering of Voted Radial Vibration (rVotedVibration_X_m_s2) *)
(* Band 1: Spindle 1X Rotational Harmonic Filter (Narrowband around f_s) *)
rIIR_B1_Output := (0.0450 * rVotedVibration_X_m_s2) - (0.0450 * rIIR_B1_x2) - 
                  (-1.8540 * rIIR_B1_y1) - (0.9100 * rIIR_B1_y2);
rIIR_B1_x2 := rIIR_B1_x1;
rIIR_B1_x1 := rVotedVibration_X_m_s2;
rIIR_B1_y2 := rIIR_B1_y1;
rIIR_B1_y1 := rIIR_B1_Output;
rRMS_Band1_1X := (rRMS_Band1_1X * 0.990) + (ABS(rIIR_B1_Output) * 0.010);

(* Band 2: Tooth Passing Frequency Harmonic Filter (Narrowband around f_t) *)
rIIR_B2_Output := (0.0620 * rVotedVibration_X_m_s2) - (0.0620 * rIIR_B2_x2) - 
                  (-1.6210 * rIIR_B2_y1) - (0.8760 * rIIR_B2_y2);
rIIR_B2_x2 := rIIR_B2_x1;
rIIR_B2_x1 := rVotedVibration_X_m_s2;
rIIR_B2_y2 := rIIR_B2_y1;
rIIR_B2_y1 := rIIR_B2_Output;
rRMS_Band2_ToothPass := (rRMS_Band2_ToothPass * 0.990) + (ABS(rIIR_B2_Output) * 0.010);

(* Band 3: Spindle Cantilever First Bending Resonance Mode (Centered at 1,250 Hz) *)
rIIR_B3_Output := (0.0880 * rVotedVibration_X_m_s2) - (0.0880 * rIIR_B3_x2) - 
                  (-1.2150 * rIIR_B3_y1) - (0.8240 * rIIR_B3_y2);
rIIR_B3_x2 := rIIR_B3_x1;
rIIR_B3_x1 := rVotedVibration_X_m_s2;
rIIR_B3_y2 := rIIR_B3_y1;
rIIR_B3_y1 := rIIR_B3_Output;
rRMS_Band3_Mode1 := (rRMS_Band3_Mode1 * 0.985) + (ABS(rIIR_B3_Output) * 0.015);

(* Band 4: Toolholder/Cutter Second Flexural Bending Mode (Centered at 2,450 Hz) *)
rIIR_B4_Output := (0.1050 * rVotedVibration_X_m_s2) - (0.1050 * rIIR_B4_x2) - 
                  (-0.3540 * rIIR_B4_y1) - (0.7900 * rIIR_B4_y2);
rIIR_B4_x2 := rIIR_B4_x1;
rIIR_B4_x1 := rVotedVibration_X_m_s2;
rIIR_B4_y2 := rIIR_B4_y1;
rIIR_B4_y1 := rIIR_B4_Output;
rRMS_Band4_Mode2 := (rRMS_Band4_Mode2 * 0.985) + (ABS(rIIR_B4_Output) * 0.015);

(* Total Multi-Band Vibration Power & Chatter Severity Index Synthesis *)
rTotalRMS_Vibration := rRMS_Band1_1X + rRMS_Band2_ToothPass + rRMS_Band3_Mode1 + rRMS_Band4_Mode2 + 0.001;
rChatterRatio := (rRMS_Band3_Mode1 + rRMS_Band4_Mode2) / rTotalRMS_Vibration;
rChatterSeverityIndex := (rChatterSeverityIndex * 0.980) + (rChatterRatio * 0.020);

(* Dominant Chatter Frequency Determination *)
IF (rRMS_Band3_Mode1 >= rRMS_Band4_Mode2) AND (rRMS_Band3_Mode1 >= rRMS_Band2_ToothPass) THEN
    rDominantChatterFreq_Hz := 1250.0;
ELSIF (rRMS_Band4_Mode2 >= rRMS_Band3_Mode1) AND (rRMS_Band4_Mode2 >= rRMS_Band2_ToothPass) THEN
    rDominantChatterFreq_Hz := 2450.0;
ELSE
    rDominantChatterFreq_Hz := rToothPassingFreq_Hz;
END_IF;

(* Chatter Tripping & Escalation Logic *)
IF rChatterSeverityIndex > rChatterThreshold_Severe THEN
    bChatterSevereFlag := TRUE;
    bChatterActiveFlag := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Bit 0: Critical Regenerative Chatter Trip *)
ELSIF rChatterSeverityIndex > rChatterThreshold_Warning THEN
    bChatterActiveFlag := TRUE;
    bChatterSevereFlag := FALSE;
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* Bit 0: Chatter Inception Warning *)
ELSE
    bChatterActiveFlag := FALSE;
    bChatterSevereFlag := FALSE;
END_IF;
""")

    # =========================================================================
    # 8. PHASE 5: 16x16 DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 5: 16x16 DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC CONTROLLER           === *)
(* ================================================================================================= *)
(* Fully initializes and unrolls 16x16 discrete state matrix A, 16x8 input matrix B, observation C,  *)
(* and direct feedthrough D. Propagates system state x[k+1] = A*x[k] + B*u[k] and executes online   *)
(* projected gradient descent to optimize piezo forces, spindle speed trim, and feedrate pacing.     *)

IF NOT bMatricesInitialized THEN
    (* 1. Initialize State Matrix A (16x16) to Identity Baseline *)
    FOR iRow := 1 TO 16 DO
        FOR iCol := 1 TO 16 DO
            IF iRow = iCol THEN
                A_mat[iRow, iCol] := 0.9950;
            ELSE
                A_mat[iRow, iCol] := 0.0000;
            END_IF;
        END_FOR;
    END_FOR;

    (* Structural Compliance Dynamics (Axial z, Radial x, Radial y) *)
    A_mat[1, 1]  := 0.9820; A_mat[1, 2]  := 0.00095; A_mat[1, 14] := -0.000045;
    A_mat[2, 1]  := -35.20; A_mat[2, 2]  := 0.9580;  A_mat[2, 14] := -0.0480;
    A_mat[3, 3]  := 0.9780; A_mat[3, 4]  := 0.00092; A_mat[3, 7]  := 0.000125;
    A_mat[4, 3]  := -48.50; A_mat[4, 4]  := 0.9450;  A_mat[4, 7]  := 0.1450;
    A_mat[5, 5]  := 0.9780; A_mat[5, 6]  := 0.00092; A_mat[5, 8]  := 0.000125;
    A_mat[6, 5]  := -48.50; A_mat[6, 6]  := 0.9450;  A_mat[6, 8]  := 0.1450;

    (* Piezoelectric Stack Actuator Dynamics (States 7, 8) *)
    A_mat[7, 7]  := 0.9250; A_mat[7, 4]  := -0.0035;
    A_mat[8, 8]  := 0.9250; A_mat[8, 6]  := -0.0035;

    (* Thermal Node Deviations (Front Bearing 9, Rear Bearing 10, Stator Core 11, Thermal Growth 12) *)
    A_mat[9, 9]   := 0.9985; A_mat[9, 15] := 0.00018; A_mat[9, 16] := -0.000085;
    A_mat[10, 10] := 0.9988; A_mat[10, 15] := 0.00012; A_mat[10, 16] := -0.000065;
    A_mat[11, 11] := 0.9975; A_mat[11, 15] := 0.00045; A_mat[11, 16] := -0.000320;
    A_mat[12, 9]  := 0.0380; A_mat[12, 10] := 0.0220; A_mat[12, 11] := 0.0550; A_mat[12, 12] := 0.9992;

    (* Regenerative Cutting Delay & Dynamic Force (States 13, 14) *)
    A_mat[13, 1]  := 0.8500; A_mat[13, 13] := 0.1250;
    A_mat[14, 1]  := -125.0; A_mat[14, 13] := 125.0; A_mat[14, 14] := 0.9150;

    (* Spindle Speed Perturbation & Cooling Jacket Heat Extraction (States 15, 16) *)
    A_mat[15, 14] := -0.0085; A_mat[15, 15] := 0.9850;
    A_mat[16, 11] := 1.2500;  A_mat[16, 16] := 0.9650;

    (* 2. Initialize Control Coupling Matrix B (16x8) *)
    FOR iRow := 1 TO 16 DO
        FOR iCol := 1 TO 8 DO
            B_mat[iRow, iCol] := 0.0000;
        END_FOR;
    END_FOR;

    B_mat[3, 1]  := 0.00185; (* u1: Piezo X Voltage -> Radial X Deflection *)
    B_mat[4, 1]  := 1.85000; (* u1: Piezo X Voltage -> Radial X Velocity *)
    B_mat[7, 1]  := 22.5000; (* u1: Piezo X Voltage -> Piezo Force State X *)

    B_mat[5, 2]  := 0.00185; (* u2: Piezo Y Voltage -> Radial Y Deflection *)
    B_mat[6, 2]  := 1.85000; (* u2: Piezo Y Voltage -> Radial Y Velocity *)
    B_mat[8, 2]  := 22.5000; (* u2: Piezo Y Voltage -> Piezo Force State Y *)

    B_mat[1, 3]  := -0.0010; (* u3: Z-Axis Servo Offset Injection -> Spindle Axial Position *)
    B_mat[12, 3] := -0.9850; (* u3: Z-Axis Servo Offset Injection -> Residual Thermal Growth *)

    B_mat[15, 4] := 0.10472; (* u4: Spindle Speed Trim -> Rotational Perturbation *)

    B_mat[14, 5] := 12.5000; (* u5: Feedrate Override -> Cutting Force *)

    B_mat[9, 6]  := -0.0045; (* u6: Chiller Valve -> Front Bearing Temp *)
    B_mat[11, 6] := -0.0185; (* u6: Chiller Valve -> Stator Temp *)
    B_mat[16, 6] := 25.0000; (* u6: Chiller Valve -> Cooling Power Extraction *)

    B_mat[9, 7]  := -0.0125; (* u7: Lube Injection -> Bearing Friction Reduction *)
    B_mat[10, 7] := -0.0085; (* u7: Lube Injection -> Rear Bearing Friction Reduction *)

    B_mat[4, 8]  := -0.1500; (* u8: Active Damping Gain -> Radial X Velocity Damping *)
    B_mat[6, 8]  := -0.1500; (* u8: Active Damping Gain -> Radial Y Velocity Damping *)

    (* 3. Initialize Observation Matrix C (16x16) & Direct Feedthrough D (16x8) *)
    FOR iRow := 1 TO 16 DO
        FOR iCol := 1 TO 16 DO
            IF iRow = iCol THEN
                C_mat[iRow, iCol] := 1.0;
            ELSE
                C_mat[iRow, iCol] := 0.0;
            END_IF;
        END_FOR;
        FOR iCol := 1 TO 8 DO
            D_mat[iRow, iCol] := 0.0;
        END_FOR;
    END_FOR;

    (* 4. MPC Cost Function Weighting Matrices Q, R, P *)
    Q_diag[1]  := 120.0; (* Axial Compliance Error Penalty *)
    Q_diag[2]  := 25.0;  (* Axial Velocity Penalty *)
    Q_diag[3]  := 180.0; (* Radial X Vibration Penalty *)
    Q_diag[4]  := 35.0;  (* Radial X Velocity Penalty *)
    Q_diag[5]  := 180.0; (* Radial Y Vibration Penalty *)
    Q_diag[6]  := 35.0;  (* Radial Y Velocity Penalty *)
    Q_diag[7]  := 15.0;  (* Piezo Force State X Penalty *)
    Q_diag[8]  := 15.0;  (* Piezo Force State Y Penalty *)
    Q_diag[9]  := 85.0;  (* Front Bearing Thermal Overheat Penalty *)
    Q_diag[10] := 60.0;  (* Rear Bearing Thermal Overheat Penalty *)
    Q_diag[11] := 75.0;  (* Stator Thermal Overheat Penalty *)
    Q_diag[12] := 250.0; (* Residual Thermal Expansion Offset Error Penalty *)
    Q_diag[13] := 95.0;  (* Regenerative Surface Wave Suppression Penalty *)
    Q_diag[14] := 45.0;  (* Cutting Force Overload Penalty *)
    Q_diag[15] := 30.0;  (* Spindle Speed Perturbation Penalty *)
    Q_diag[16] := 20.0;  (* Cooling Jacket Mismatch Penalty *)

    R_diag[1]  := 2.50;  (* u1: Piezo X Voltage Effort Penalty *)
    R_diag[2]  := 2.50;  (* u2: Piezo Y Voltage Effort Penalty *)
    R_diag[3]  := 8.00;  (* u3: Z-Axis Servo Offset Injection Effort *)
    R_diag[4]  := 4.50;  (* u4: SSV Speed Trim Effort *)
    R_diag[5]  := 12.00; (* u5: Feedrate Pacing Penalty (Preserve Production Rate) *)
    R_diag[6]  := 3.00;  (* u6: Chiller Valve Movement Effort *)
    R_diag[7]  := 15.00; (* u7: Lube Injection Pulse Cycling Penalty *)
    R_diag[8]  := 6.50;  (* u8: Active Damping Gain Tuning Effort *)

    FOR iRow := 1 TO 16 DO
        P_diag[iRow] := Q_diag[iRow] * 1.85; (* Terminal State Penalties *)
    END_FOR;

    bMatricesInitialized := TRUE;
END_IF;

(* Map Physical Sensor Feedback into System State Vector x_state *)
x_state[1]  := rCurrentSurfaceZ_um;
x_state[2]  := (rVotedVibration_Z_m_s2 / (2.0 * c_Pi * 1250.0)) * 1000.0;
x_state[3]  := (rVotedVibration_X_m_s2 / ((2.0 * c_Pi * 1250.0) * (2.0 * c_Pi * 1250.0))) * 1000000.0;
x_state[4]  := (rVotedVibration_X_m_s2 / (2.0 * c_Pi * 1250.0)) * 1000.0;
x_state[5]  := (rVotedVibration_Y_m_s2 / ((2.0 * c_Pi * 1250.0) * (2.0 * c_Pi * 1250.0))) * 1000000.0;
x_state[6]  := (rVotedVibration_Y_m_s2 / (2.0 * c_Pi * 1250.0)) * 1000.0;
x_state[7]  := rPiezoDemandedForce_X_N;
x_state[8]  := rPiezoDemandedForce_Y_N;
x_state[9]  := rVotedBearingTemp_degC - c_NominalChillerSetpoint_degC;
x_state[10] := rTempRearBearing_degC - c_NominalChillerSetpoint_degC;
x_state[11] := rTempStatorCore_degC - c_NominalChillerSetpoint_degC;
x_state[12] := rFilteredThermalGrowth_um - rZAxisThermalCompOffset_um;
x_state[13] := rDelayedSurfaceZ_um;
x_state[14] := rEstimatedCuttingForce_N;
x_state[15] := (rVotedSpindleSpeed_RPM - rCommandSpindleSpeed_RPM) * 0.10472;
x_state[16] := rChillerHeatExtraction_W;

(* One-Step Ahead State Prediction: x_pred = A * x_state + B * u_mpc *)
FOR iRow := 1 TO 16 DO
    rTempCalc1 := 0.0;
    FOR iCol := 1 TO 16 DO
        rTempCalc1 := rTempCalc1 + (A_mat[iRow, iCol] * x_state[iCol]);
    END_FOR;
    FOR iCol := 1 TO 8 DO
        rTempCalc1 := rTempCalc1 + (B_mat[iRow, iCol] * u_mpc[iCol]);
    END_FOR;
    x_pred[iRow] := rTempCalc1;
    x_err[iRow] := x_pred[iRow] - x_ref[iRow];
END_FOR;

(* Analytical Gradient Calculation: grad_J = B^T * Q * x_err + R * u_mpc *)
FOR iCol := 1 TO 8 DO
    rTempCalc2 := 0.0;
    FOR iRow := 1 TO 16 DO
        rTempCalc2 := rTempCalc2 + (B_mat[iRow, iCol] * Q_diag[iRow] * x_err[iRow]);
    END_FOR;
    grad_J[iCol] := rTempCalc2 + (R_diag[iCol] * u_mpc[iCol]);
    
    (* Diagonal Approximate Hessian: H_ii = B_i^T * Q * B_i + R_i *)
    rTempCalc3 := 0.0;
    FOR iRow := 1 TO 16 DO
        rTempCalc3 := rTempCalc3 + (B_mat[iRow, iCol] * Q_diag[iRow] * B_mat[iRow, iCol]);
    END_FOR;
    H_diag[iCol] := rTempCalc3 + R_diag[iCol] + 0.01;
END_FOR;

(* Projected Gradient Descent Update with Explicit Physical Box Constraints *)
FOR iCol := 1 TO 8 DO
    u_delta[iCol] := -1.0 * (grad_J[iCol] / H_diag[iCol]) * rMpcStepSize;
    u_mpc[iCol] := u_mpc[iCol] + u_delta[iCol];
END_FOR;

(* Constraint Clamping: Actuator Saturation Envelopes *)
(* u1, u2: Piezo Stack Voltages (-20V to +150V) *)
IF u_mpc[1] < c_PiezoVoltageMin_V THEN u_mpc[1] := c_PiezoVoltageMin_V; END_IF;
IF u_mpc[1] > c_PiezoVoltageMax_V THEN u_mpc[1] := c_PiezoVoltageMax_V; END_IF;
IF u_mpc[2] < c_PiezoVoltageMin_V THEN u_mpc[2] := c_PiezoVoltageMin_V; END_IF;
IF u_mpc[2] > c_PiezoVoltageMax_V THEN u_mpc[2] := c_PiezoVoltageMax_V; END_IF;

(* u3: Z-Axis Thermal Offset (-250 um to +250 um) *)
IF u_mpc[3] < -250.0 THEN u_mpc[3] := -250.0; END_IF;
IF u_mpc[3] > 250.0 THEN u_mpc[3] := 250.0; END_IF;

(* u4: SSV Speed Trim (-3000 RPM to +3000 RPM) *)
IF u_mpc[4] < -3000.0 THEN u_mpc[4] := -3000.0; END_IF;
IF u_mpc[4] > 3000.0 THEN u_mpc[4] := 3000.0; END_IF;

(* u5: Feedrate Override (10% to 120%) *)
IF u_mpc[5] < 10.0 THEN u_mpc[5] := 10.0; END_IF;
IF u_mpc[5] > 120.0 THEN u_mpc[5] := 120.0; END_IF;

(* u6: Chiller Valve (0% to 100%) *)
IF u_mpc[6] < 0.0 THEN u_mpc[6] := 0.0; END_IF;
IF u_mpc[6] > 100.0 THEN u_mpc[6] := 100.0; END_IF;

(* u7: Lube Injection Step (0 to 1) *)
IF u_mpc[7] < 0.0 THEN u_mpc[7] := 0.0; END_IF;
IF u_mpc[7] > 1.0 THEN u_mpc[7] := 1.0; END_IF;

(* u8: Active Damping Gain (0 to 3500 N/(um/s)) *)
IF u_mpc[8] < 0.0 THEN u_mpc[8] := 0.0; END_IF;
IF u_mpc[8] > 3500.0 THEN u_mpc[8] := 3500.0; END_IF;
""")

    # =========================================================================
    # 9. PHASE 6: ACTIVE PIEZO DAMPING & SPINDLE SPEED VARIATION (SSV)
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 6: ACTIVE PIEZOELECTRIC COUNTER-DAMPING & SPINDLE SPEED VARIATION (SSV) ACTUATION     === *)
(* ================================================================================================= *)
(* Direct Velocity Feedback (DVFB) active vibration damping generates dynamic counter-forces        *)
(* via orthogonal piezo stack actuators. When regenerative chatter is detected, autonomous SSV      *)
(* modulates spindle speed sinusoidally to break regenerative wave synchronization.                 *)

(* Direct Velocity Feedback Counter-Force Demands (DVFB) *)
IF bPiezoAmplifierReady AND (NOT bPiezoClampActive) THEN
    (* Counter-force proportional to measured bearing vibration velocity and position *)
    rPiezoDemandedForce_X_N := (-1.0 * (rPiezoGain_Velocity_Ns_m * (x_state[4] * 0.001))) - 
                               (rPiezoGain_Position_N_m * (x_state[3] * 0.000001));
    rPiezoDemandedForce_Y_N := (-1.0 * (rPiezoGain_Velocity_Ns_m * (x_state[6] * 0.001))) - 
                               (rPiezoGain_Position_N_m * (x_state[5] * 0.000001));

    (* Bouc-Wen Piezoelectric Hysteresis Model Compensation *)
    rPiezoHysteresisState_X := (rPiezoHysteresisState_X * 0.965) + (rPiezoDemandedForce_X_N * 0.00015);
    rPiezoHysteresisState_Y := (rPiezoHysteresisState_Y * 0.965) + (rPiezoDemandedForce_Y_N * 0.00015);

    (* Convert Dynamic Force Demand to Output Drive Voltage (65.0 V Quiescent DC Bias) *)
    rPiezoVoltage_X_V := 65.0 + (rPiezoDemandedForce_X_N / c_PiezoMaxForce_N) * 75.0 - rPiezoHysteresisState_X;
    rPiezoVoltage_Y_V := 65.0 + (rPiezoDemandedForce_Y_N / c_PiezoMaxForce_N) * 75.0 - rPiezoHysteresisState_Y;

    (* Hard Saturation Limits (-20.0 V to +150.0 V) *)
    IF rPiezoVoltage_X_V < c_PiezoVoltageMin_V THEN rPiezoVoltage_X_V := c_PiezoVoltageMin_V; END_IF;
    IF rPiezoVoltage_X_V > c_PiezoVoltageMax_V THEN rPiezoVoltage_X_V := c_PiezoVoltageMax_V; END_IF;
    IF rPiezoVoltage_Y_V < c_PiezoVoltageMin_V THEN rPiezoVoltage_Y_V := c_PiezoVoltageMin_V; END_IF;
    IF rPiezoVoltage_Y_V > c_PiezoVoltageMax_V THEN rPiezoVoltage_Y_V := c_PiezoVoltageMax_V; END_IF;
ELSE
    rPiezoVoltage_X_V := 0.0;
    rPiezoVoltage_Y_V := 0.0;
    rPiezoDemandedForce_X_N := 0.0;
    rPiezoDemandedForce_Y_N := 0.0;
END_IF;

(* Spindle Speed Variation (SSV) Autonomous Modulation Synthesizer *)
(* Injected whenever chatter severity exceeds warning threshold (State 70 or active in-cut) *)
IF (bChatterActiveFlag OR (iState = 70)) AND (rVotedSpindleSpeed_RPM > 2000.0) THEN
    (* Sinusoidal Continuous Modulation: N(t) = N_0 + Delta_N * sin(2 * pi * f_m * t) *)
    rSSV_Phase_rad := rSSV_Phase_rad + ((2.0 * c_Pi * rSSV_Frequency_Hz) * c_ScanTime_Ts_s);
    IF rSSV_Phase_rad > (2.0 * c_Pi) THEN
        rSSV_Phase_rad := rSSV_Phase_rad - (2.0 * c_Pi);
    END_IF;
    
    rSSV_CalculatedTrim_RPM := (rCommandSpindleSpeed_RPM * rSSV_AmplitudeRatio_RVA) * SIN(rSSV_Phase_rad);
    rSSV_SpeedTrim_RPM := rSSV_CalculatedTrim_RPM;
    
    (* Dynamically Throttle Feedrate Override to Alleviate Cutting Chip Load During SSV *)
    rFeedrateOverride_pct := 85.0;
ELSE
    rSSV_Phase_rad := 0.0;
    rSSV_CalculatedTrim_RPM := 0.0;
    rSSV_SpeedTrim_RPM := 0.0;
    
    (* Restore Normal Nominal Feedrate Override *)
    IF NOT bSpindleDriveSTO_Trip THEN
        rFeedrateOverride_pct := u_mpc[5];
    END_IF;
END_IF;
""")

    # =========================================================================
    # 10. PHASE 7: OIL-AIR MICRO-LUBRICATION & PREDICTIVE CHILLER PACING
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 7: CLOSED-LOOP OIL-AIR MICRO-LUBRICATION & PREDICTIVE CHILLER PACING                 === *)
(* ================================================================================================= *)
(* Meters micro-shots (0.03 cm3) of synthetic ester lubricant into high-speed compressed air.        *)
(* Verifies streak sensor passage within timeout window. Solves thermal heat balance and regulates  *)
(* chilled glycol proportional modulating control valve to maintain spindle thermal datum.           *)

(* --- 7.1 Oil-Air Micro-Lubrication Sequencing & Optical Streak Verification --- *)
tLubeCycleTimer(IN := (bEnableSystem AND (NOT bLubricationInjectPulse)), PT := REAL_TO_TIME(rLubeShotInterval_s * 1000.0));
tLubePulseDurationTimer(IN := bLubricationInjectPulse, PT := REAL_TO_TIME(rLubePulseDuration_s * 1000.0));

IF tLubeCycleTimer.Q THEN
    bLubricationInjectPulse := TRUE;
    iLubeTotalShots := iLubeTotalShots + 1;
    rLubeCumulativeVolume_cm3 := rLubeCumulativeVolume_cm3 + 0.030;
    bStreakArrivalLatched := FALSE;
    tStreakDetectionTimeoutTimer(IN := FALSE, PT := REAL_TO_TIME(rStreakTimeoutWindow_s * 1000.0));
END_IF;

IF tLubePulseDurationTimer.Q THEN
    bLubricationInjectPulse := FALSE;
END_IF;

(* Optical Capillary Streak Verification Window *)
tStreakDetectionTimeoutTimer(IN := (NOT bStreakArrivalLatched) AND (iLubeTotalShots > 0), 
                             PT := REAL_TO_TIME(rStreakTimeoutWindow_s * 1000.0));

IF bStreakSensorOilPulse THEN
    bStreakArrivalLatched := TRUE;
    bStreakMissingWarning := FALSE;
END_IF;

IF tStreakDetectionTimeoutTimer.Q AND (NOT bStreakArrivalLatched) THEN
    bStreakMissingWarning := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Bit 1: Oil-Air Droplet Streak Timeout Warning *)
END_IF;

(* Lubrication Film Thickness Ratio Lambda Estimation (Dowson-Higginson EHD Model) *)
IF rVotedSpindleSpeed_RPM > 500.0 THEN
    rBearingLubricationFilm_pct := 95.0 + (5.0 * (1.0 - EXP(-1.0 * (rVotedSpindleSpeed_RPM / 6000.0)))) - 
                                   ((rVotedBearingTemp_degC - 20.0) * 0.45);
    IF rBearingLubricationFilm_pct < 40.0 THEN
        rBearingLubricationFilm_pct := 40.0;
    ELSIF rBearingLubricationFilm_pct > 100.0 THEN
        rBearingLubricationFilm_pct := 100.0;
    END_IF;
ELSE
    rBearingLubricationFilm_pct := 98.0;
END_IF;

(* --- 7.2 Predictive Heat Load Balance & Chiller Pacing PID --- *)
(* Spindle Total Heat Dissipation: P_total = P_mechanical_bearing + P_electrical_stator *)
rEstimatedSpindleLosses_W := (0.000105 * (rSpindleMotorTorque_Nm * rVotedSpindleSpeed_RPM)) + 
                             (3.0 * (rSpindleMotorCurrent_A * rSpindleMotorCurrent_A * 0.085)) + 
                             (0.0025 * rVotedSpindleSpeed_RPM * (rVotedBearingTemp_degC - 18.0));

(* Real-Time Chiller Thermal Extraction Rate: Q_cool = m_dot * C_p * (T_out - T_in) *)
rChillerHeatExtraction_W := ((rChillerFlowRate_lpm / 60.0) * (c_GlycolDensity_kg_m3 * 0.001)) * 
                            c_GlycolSpecificHeat_J_kgK * (rTempChillerOutlet_degC - rTempChillerInlet_degC);
rCoolingHeatExtraction_kW := rChillerHeatExtraction_W * 0.001;

(* Closed-Loop Predictive Feedforward PID Controller *)
rChillerError_degC := rVotedBearingTemp_degC - c_NominalChillerSetpoint_degC;
rChillerIntegralAccum_degC_s := rChillerIntegralAccum_degC_s + (rChillerError_degC * c_ScanTime_Ts_s);

(* Anti-Windup Clamping on Thermal Integral *)
IF rChillerIntegralAccum_degC_s > 500.0 THEN rChillerIntegralAccum_degC_s := 500.0; END_IF;
IF rChillerIntegralAccum_degC_s < -500.0 THEN rChillerIntegralAccum_degC_s := -500.0; END_IF;

rChillerPID_Output_pct := (rEstimatedSpindleLosses_W / 3500.0) * 50.0 + 
                          (rChillerError_degC * 12.5) + 
                          (rChillerIntegralAccum_degC_s * 0.045);

IF rChillerPID_Output_pct < 0.0 THEN rChillerPID_Output_pct := 0.0; END_IF;
IF rChillerPID_Output_pct > 100.0 THEN rChillerPID_Output_pct := 100.0; END_IF;
rChillerValveDemand_pct := rChillerPID_Output_pct;
""")

    # =========================================================================
    # 11. PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 8: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                    === *)
(* ================================================================================================= *)
(* Implements complete supervisory automation lifecycle:                                            *)
(* Stage 10:  Spindle Bearing Lubrication Purge                                                      *)
(* Stage 20:  Chiller Pre-Cooling Stabilization                                                      *)
(* Stage 30:  Cold Spindle Warm-Up Speed Profiling                                                   *)
(* Stage 40:  Static Tool Length Laser Metrology                                                     *)
(* Stage 50:  In-Cut Roughing Chatter Monitoring Active                                              *)
(* Stage 60:  Dynamic Thermal Growth Real-Time Offset Injection                                      *)
(* Stage 70:  Spindle Speed Variation (SSV) Actuation                                                *)
(* Stage 80:  Finish Contouring Precision Hold                                                       *)
(* Stage 90:  Automated Tool Retract & Spindle Brake                                                 *)
(* Stage 100: Tool Wear In-Situ Metrology Check                                                      *)
(* Stage 110: Spindle Controlled Cool-Down                                                           *)
(* Stage 120: Emergency E-Stop Piezo Clamp & Safe Torque Off (STO)                                   *)

(* Track Stage Elapsed Execution Dwell Time *)
IF iState = iPrevState THEN
    rStateElapsedSec := rStateElapsedSec + c_ScanTime_Ts_s;
    iStateCycleCount := iStateCycleCount + 1;
ELSE
    rStateElapsedSec := 0.0;
    iStateCycleCount := 0;
    iSubState := 0;
    iPrevState := iState;
END_IF;

iActiveFSMStage := iState;

CASE iState OF
    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 10: SPINDLE BEARING LUBRICATION PURGE                                                  *)
    (* Pre-charges oil-air distributor, purges trapped air bubbles, and confirms streak detection  *)
    (* --------------------------------------------------------------------------------------------- *)
    10:
        IF (rLubricationPressure_bar >= c_rLubePress_L_bar) AND bLubricationUnitReady THEN
            IF rStateElapsedSec > 15.0 THEN
                (* Purge cycle dwell complete and pressure verified *)
                iState := 20; (* Advance to Chiller Pre-Cooling Stabilization *)
            END_IF;
        ELSE
            dwWarningWord := dwWarningWord OR 16#0000_0004; (* Stage 10 Lube Pressure Inadequate *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 20: CHILLER PRE-COOLING STABILIZATION                                                  *)
    (* Recirculates chilled glycol until spindle core stabilizes to 20.0 +/- 0.2 deg C datum        *)
    (* --------------------------------------------------------------------------------------------- *)
    20:
        IF bChillerUnitReady AND (rChillerFlowRate_lpm >= c_rChillerFlow_L_lpm) THEN
            IF (ABS(rVotedBearingTemp_degC - c_NominalChillerSetpoint_degC) <= 0.35) AND (rStateElapsedSec > 10.0) THEN
                iState := 30; (* Advance to Cold Spindle Warm-Up Profiling *)
            END_IF;
        ELSE
            dwWarningWord := dwWarningWord OR 16#0000_0008; (* Stage 20 Chiller Coolant Flow Low *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 30: COLD SPINDLE WARM-UP SPEED PROFILING                                               *)
    (* Executes stepped ramp: 3,000 -> 10,000 -> 20,000 -> 30,000 RPM verifying bearing equilibrium  *)
    (* --------------------------------------------------------------------------------------------- *)
    30:
        IF bAutoCyclePermissive AND (dwAlarmWord1 = 16#0000_0000) THEN
            CASE iSubState OF
                0: (* Step 1: 3,000 RPM Low-Speed Rolling Film Establishment *)
                    IF rStateElapsedSec > 20.0 THEN
                        iSubState := 1;
                        rStateElapsedSec := 0.0;
                    END_IF;
                1: (* Step 2: 10,000 RPM Mid-Speed Hydrodynamic Stabilization *)
                    IF rStateElapsedSec > 25.0 THEN
                        iSubState := 2;
                        rStateElapsedSec := 0.0;
                    END_IF;
                2: (* Step 3: 20,000 RPM High-Speed Pre-Machining Plateau *)
                    IF rStateElapsedSec > 30.0 THEN
                        iSubState := 3;
                        rStateElapsedSec := 0.0;
                    END_IF;
                3: (* Step 4: 30,000 RPM Maximum Rated Speed Thermal Verification *)
                    IF (rStateElapsedSec > 30.0) AND (rVotedBearingTemp_degC < c_rBearingTemp_H_degC) THEN
                        iState := 40; (* Advance to Static Tool Length Laser Metrology *)
                    END_IF;
            END_CASE;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 40: STATIC TOOL LENGTH LASER METROLOGY                                                 *)
    (* Non-contact optical laser tool setter verifies gage length, diameter, and dynamic runout     *)
    (* --------------------------------------------------------------------------------------------- *)
    40:
        IF bLaserMetrologyReady THEN
            IF rLaserMeasuredToolRunout_um > c_rRunout_HH_um THEN
                dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Tool Dynamic Runout Excessive Trip *)
                iState := 120;
            ELSIF rStateElapsedSec > 5.0 THEN
                iState := 50; (* Advance to In-Cut Roughing Chatter Monitoring *)
            END_IF;
        ELSE
            dwWarningWord := dwWarningWord OR 16#0000_0010; (* Laser Tool Setter Not Ready *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 50: IN-CUT ROUGHING CHATTER MONITORING ACTIVE                                          *)
    (* Full heavy milling cut: active vibration FFT band monitoring and stability lobe evaluation   *)
    (* --------------------------------------------------------------------------------------------- *)
    50:
        IF bChatterSevereFlag THEN
            iState := 70; (* Chatter Severe -> Transition to Spindle Speed Variation (SSV) *)
        ELSIF bInCutSignalFromCNC AND (rCalculatedThermalGrowth_um > 2.50) THEN
            iState := 60; (* Thermal Growth Incurred -> Transition to Dynamic Offset Injection *)
        ELSIF NOT bInCutSignalFromCNC THEN
            IF rProgrammedCutDepth_mm < 0.50 THEN
                iState := 80; (* Transition to Finish Contouring Precision Hold *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 60: DYNAMIC THERMAL GROWTH REAL-TIME OFFSET INJECTION                                  *)
    (* Actively injecting finite-difference Z-axis servo offset and radial drift compensation       *)
    (* --------------------------------------------------------------------------------------------- *)
    60:
        IF bChatterSevereFlag THEN
            iState := 70; (* Priority Escalation: Chatter Suppress Supersedes Thermal Offset *)
        ELSIF (ABS(rFilteredThermalGrowth_um - rZAxisThermalCompOffset_um) < 0.25) AND (NOT bInCutSignalFromCNC) THEN
            iState := 80; (* Advance to Finish Contouring Precision Hold *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 70: SPINDLE SPEED VARIATION (SSV) ACTUATION                                            *)
    (* Sinusoidal modulation of spindle RPM disrupts regenerative chatter wave synchronization       *)
    (* --------------------------------------------------------------------------------------------- *)
    70:
        IF (rChatterSeverityIndex < rChatterThreshold_Warning) AND (rStateElapsedSec > 8.0) THEN
            (* Chatter quenched successfully, return to standard in-cut monitoring *)
            iState := 50;
        ELSIF rStateElapsedSec > 35.0 THEN
            (* Chatter persists despite SSV: Force autonomous feedrate reduction *)
            rFeedrateOverride_pct := 60.0;
            iState := 80;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 80: FINISH CONTOURING PRECISION HOLD                                                   *)
    (* High-precision sub-micron finishing mode: maximum piezo active damping and zero drift lock   *)
    (* --------------------------------------------------------------------------------------------- *)
    80:
        IF NOT bInCutSignalFromCNC THEN
            IF rStateElapsedSec > 10.0 THEN
                iState := 90; (* Advance to Automated Tool Retract & Spindle Brake *)
            END_IF;
        ELSIF bChatterSevereFlag THEN
            iState := 70;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 90: AUTOMATED TOOL RETRACT & SPINDLE BRAKE                                             *)
    (* Controlled regenerative braking down to orient position, activating drawbar air purge       *)
    (* --------------------------------------------------------------------------------------------- *)
    90:
        IF rVotedSpindleSpeed_RPM < 25.0 THEN
            iState := 100; (* Spindle Stopped: Advance to In-Situ Tool Wear Metrology *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 100: TOOL WEAR IN-SITU METROLOGY CHECK                                                 *)
    (* Acoustic emission integration and laser tool tip inspection for chipping/flank wear          *)
    (* --------------------------------------------------------------------------------------------- *)
    100:
        IF rAcousticEmission_dB > c_rAE_ToolBreakage_HH_dB THEN
            bToolWearRetractReq := TRUE;
            dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* In-Situ Cutting Tool Breakage Detected *)
            iState := 110;
        ELSIF rStateElapsedSec > 4.0 THEN
            bToolWearRetractReq := FALSE;
            iState := 110; (* Advance to Spindle Controlled Cool-Down *)
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 110: SPINDLE CONTROLLED COOL-DOWN                                                      *)
    (* Low-RPM idling (1,500 RPM) while chiller extracts heat until bearing returns to datum        *)
    (* --------------------------------------------------------------------------------------------- *)
    110:
        IF (rVotedBearingTemp_degC <= (c_NominalChillerSetpoint_degC + 1.20)) OR (rStateElapsedSec > 60.0) THEN
            IF bAutoCyclePermissive THEN
                iState := 10; (* Loop Back to Standby / Next Workpiece Machining Cycle *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------------------------------- *)
    (* STAGE 120: EMERGENCY E-STOP PIEZO CLAMP & DRIVE SAFE TORQUE OFF (STO)                        *)
    (* Hardware E-Stop clamp state: Safe Torque Off active, piezo clamped, waiting operator reset   *)
    (* --------------------------------------------------------------------------------------------- *)
    120:
        bSpindleDriveSTO_Trip := TRUE;
        bPiezoClampActive := TRUE;
        rPiezoVoltage_X_V := 0.0;
        rPiezoVoltage_Y_V := 0.0;
        rFeedrateOverride_pct := 0.0;
        
        IF bResetAlarms AND (dwAlarmWord1 = 16#0000_0000) AND bEmergencyStop THEN
            iState := 10; (* Acknowledged and Safe: Return to Stage 10 Lubrication Purge *)
        END_IF;
END_CASE;
""")

    # =========================================================================
    # 12. PHASE 9: ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    # =========================================================================
    parts.append("""
(* ================================================================================================= *)
(* === PHASE 9: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC TELEMETRY BIT-PACKING                    === *)
(* ================================================================================================= *)
(* Evaluates secondary process alarms (chatter, runout, tool wear, flow, pressure) with hysteresis,  *)
(* updates master alarm words, and packs complete operational telemetry into dwSystemStatusWord.     *)

(* --- 9.1 High Alarms & Operational Warnings --- *)
(* Bearing Temperature High Advisory (H) *)
IF (rVotedBearingTemp_degC > c_rBearingTemp_H_degC) AND (rVotedBearingTemp_degC <= c_rBearingTemp_HH_degC) THEN
    bAlarm_BearingTemp_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Bit 5: Bearing Temperature Elevated Warning *)
ELSIF rVotedBearingTemp_degC < (c_rBearingTemp_H_degC - c_rBearingTemp_Deadband_degC) THEN
    bAlarm_BearingTemp_H := FALSE;
END_IF;

(* Motor Stator Copper Winding Temperature High Advisory (H) *)
IF (rTempStatorWinding_degC > c_rStatorTemp_H_degC) AND (rTempStatorWinding_degC <= c_rStatorTemp_HH_degC) THEN
    bAlarm_StatorTemp_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Bit 6: Stator Winding Temperature High Warning *)
ELSIF rTempStatorWinding_degC < (c_rStatorTemp_H_degC - c_rStatorTemp_Deadband_degC) THEN
    bAlarm_StatorTemp_H := FALSE;
END_IF;

(* Spindle Bearing Radial Vibration High Advisory (H) *)
IF ((rVotedVibration_X_m_s2 > c_rVib_H_m_s2) OR 
    (rVotedVibration_Y_m_s2 > c_rVib_H_m_s2) OR 
    (rVotedVibration_Z_m_s2 > c_rVib_H_m_s2)) AND 
   (NOT bAlarm_Vibration_HH) THEN
    bAlarm_Vibration_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Bit 7: Spindle Vibration Elevated Warning *)
ELSIF (rVotedVibration_X_m_s2 < (c_rVib_H_m_s2 - c_rVib_Deadband_m_s2)) AND
      (rVotedVibration_Y_m_s2 < (c_rVib_H_m_s2 - c_rVib_Deadband_m_s2)) AND
      (rVotedVibration_Z_m_s2 < (c_rVib_H_m_s2 - c_rVib_Deadband_m_s2)) THEN
    bAlarm_Vibration_H := FALSE;
END_IF;

(* Oil-Air Lubrication Supply Pressure High Advisory (H) *)
IF (rLubricationPressure_bar > c_rLubePress_H_bar) AND (rLubricationPressure_bar <= c_rLubePress_HH_bar) THEN
    bAlarm_LubePress_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0100; (* Bit 8: Lubrication Pressure High Warning *)
ELSIF rLubricationPressure_bar < (c_rLubePress_H_bar - c_rLubePress_Deadband_bar) THEN
    bAlarm_LubePress_H := FALSE;
END_IF;

(* Chilled Glycol Coolant Flow Rate Low Advisory (L) *)
IF (rChillerFlowRate_lpm < c_rChillerFlow_L_lpm) AND (rChillerFlowRate_lpm >= c_rChillerFlow_LL_lpm) THEN
    bAlarm_ChillerFlow_L := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* Bit 9: Chiller Coolant Flow Low Warning *)
ELSIF rChillerFlowRate_lpm > (c_rChillerFlow_L_lpm + c_rChillerFlow_Deadband_lpm) THEN
    bAlarm_ChillerFlow_L := FALSE;
END_IF;

(* In-Situ Acoustic Tool Wear High Warning (H) *)
IF (rAcousticEmission_dB > c_rAE_ToolWear_H_dB) AND (rAcousticEmission_dB <= c_rAE_ToolBreakage_HH_dB) THEN
    bAlarm_AE_ToolWear_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Bit 10: Tool Flank Wear Elevated Warning *)
ELSIF rAcousticEmission_dB < (c_rAE_ToolWear_H_dB - c_rAE_Deadband_dB) THEN
    bAlarm_AE_ToolWear_H := FALSE;
END_IF;

(* Spindle Dynamic Runout High Warning (H) *)
IF (rLaserMeasuredToolRunout_um > c_rRunout_H_um) AND (rLaserMeasuredToolRunout_um <= c_rRunout_HH_um) THEN
    bAlarm_Runout_H := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0800; (* Bit 11: Tool Dynamic Runout Warning *)
ELSIF rLaserMeasuredToolRunout_um < (c_rRunout_H_um - c_rRunout_Deadband_um) THEN
    bAlarm_Runout_H := FALSE;
END_IF;

(* --- 9.2 Critical Alarm Word 2: Process & Machining Quality Trips --- *)
(* Bit 0: Critical Chatter Lobe Violation *)
IF bAlarm_ChatterSevere_HH THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001;
END_IF;

(* Bit 1: Dynamic Tool Runout Destructive Trip *)
IF rLaserMeasuredToolRunout_um > c_rRunout_HH_um THEN
    bAlarm_Runout_HH := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002;
ELSIF bResetAlarms THEN
    bAlarm_Runout_HH := FALSE;
END_IF;

(* Bit 2: In-Situ Acoustic Tool Breakage Fracture Trip *)
IF rAcousticEmission_dB > c_rAE_ToolBreakage_HH_dB THEN
    bAlarm_AE_ToolBreak_HH := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004;
ELSIF bResetAlarms THEN
    bAlarm_AE_ToolBreak_HH := FALSE;
END_IF;

(* Bit 3: Chilled Glycol Complete Flow Loss LL Trip (< 5.0 l/min) *)
IF rChillerFlowRate_lpm < c_rChillerFlow_LL_lpm THEN
    bAlarm_ChillerFlow_LL := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008;
ELSIF rChillerFlowRate_lpm > (c_rChillerFlow_LL_lpm + c_rChillerFlow_Deadband_lpm) THEN
    IF bResetAlarms THEN
        bAlarm_ChillerFlow_LL := FALSE;
    END_IF;
END_IF;

(* Bit 4: Spindle Shaft Severe Axial Thermal Growth Limit Trip (> 180.0 um) *)
IF rCalculatedThermalGrowth_um > 180.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010;
END_IF;

(* Bit 5: Spindle Centerline Resultant Radial Thermal Drift Trip (> 35.0 um) *)
IF rCalculatedRadialDrift_um > 35.0 THEN
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020;
END_IF;

(* --- 9.3 Critical Alarm Word 3: Subsystem Hardware Trips --- *)
(* Bit 0: Oil-Air Lubrication Capillary Streak Missing Persistent Trip *)
IF bStreakMissingWarning AND (rStateElapsedSec > 180.0) THEN
    dwAlarmWord3 := dwAlarmWord3 OR 16#0000_0001;
END_IF;

(* Bit 1: Sensor Triplet Tripped (Loss of Redundancy Safe Trip) *)
IF bAccX_Trip OR bAccY_Trip OR bAccZ_Trip OR bTempB_Trip OR bSpeed_Trip THEN
    bAlarm_SensorFailureTrip_HH := TRUE;
    dwAlarmWord3 := dwAlarmWord3 OR 16#0000_0002;
ELSIF bResetAlarms THEN
    bAlarm_SensorFailureTrip_HH := FALSE;
END_IF;

(* Bit 2: Laser Tool Setter Communication Timeout *)
IF (NOT bLaserMetrologyReady) AND (iState = 40) THEN
    dwAlarmWord3 := dwAlarmWord3 OR 16#0000_0004;
END_IF;

(* --- 9.4 32-Bit System Status Telemetry Word Bit-Packing (ISA-18.2) --- *)
dwSystemStatusWord := 16#0000_0000;

(* Bits 0-3: Current FSM Operating Stage Code (0 to 12) *)
dwSystemStatusWord := dwSystemStatusWord OR DINT_TO_DWORD(INT_TO_DINT(iState / 10));

(* Bit 4: System Functional Safety Enable Permissive Active *)
IF bEnableSystem THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010;
END_IF;

(* Bit 5: Safe Torque Off (STO) Safety Circuit Active *)
IF bSpindleDriveSTO_Trip THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020;
END_IF;

(* Bit 6: Piezoelectric Active Vibration Damping Actuator Active *)
IF (NOT bPiezoClampActive) AND (rVotedSpindleSpeed_RPM > 500.0) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040;
END_IF;

(* Bit 7: Spindle Speed Variation (SSV) Autonomous Modulation Active *)
IF rSSV_CalculatedTrim_RPM <> 0.0 THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080;
END_IF;

(* Bit 8: Z-Axis Servo Thermal Growth Compensation Offset Active *)
IF ABS(rZAxisThermalCompOffset_um) > 0.10 THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100;
END_IF;

(* Bit 9: 2D Radial Centerline Drift Compensation Active *)
IF rCalculatedRadialDrift_um > 0.10 THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200;
END_IF;

(* Bit 10: Oil-Air Micro-Lubrication Solenoid Injection Pulse Active *)
IF bLubricationInjectPulse THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400;
END_IF;

(* Bit 11: Optical Capillary Oil Droplet Streak Verified *)
IF bStreakArrivalLatched THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800;
END_IF;

(* Bit 12: CNC Cutter Actively In-Cut Flag *)
IF bInCutSignalFromCNC THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_1000;
END_IF;

(* Bit 13: 2oo3 Sensor Group Operating in Degraded 1oo2 Mode *)
IF (dwDegradationWord <> 16#0000_0000) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_2000;
END_IF;

(* Bit 14: Master Critical Alarm Summary Active *)
IF (dwAlarmWord1 <> 16#0000_0000) OR (dwAlarmWord2 <> 16#0000_0000) OR (dwAlarmWord3 <> 16#0000_0000) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_4000;
END_IF;

(* Bit 15: Master Operational Advisory Warning Summary Active *)
IF (dwWarningWord <> 16#0000_0000) THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_8000;
END_IF;

END_FUNCTION_BLOCK
""")

    return "".join(parts)

def main():
    st_code = generate_iec_st()
    print(f"Generated IEC ST code length: {len(st_code)} characters")
    
    # Save to JSON
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Machinery & CNC Tooling: 5-Axis High-Speed Machining Center (HSM) with Active Spindle Thermal Expansion Growth Compensation & Piezoelectric Active Chatter Damping**
Function Block Name: FB_CNC_5Axis_SpindleThermalExpansion_ActiveVibrationDamping

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_CNC_5Axis_SpindleThermalExpansion_ActiveVibrationDamping
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [RPM], [deg C], [m/s2], [um], [N], [V], [bar], [l/min], [mm/min], [mm], [dB], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal discrete state-space matrices A, B, C, D, MPC weights, 2oo3 voting vars, timers)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_CNC_5Axis_SpindleThermalExpansion_ActiveVibrationDamping
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_7c2018ea.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Heavy Machinery & CNC Tooling: 5-Axis HSM Spindle Thermal & Chatter Damping"""

    assistant_content = f"```iec-st\n{st_code}\n```"
    print(f"Assistant content total length: {len(assistant_content)} characters")

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_file = "data/swarm_raw/agent_7c2018ea.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved to {target_file}")

if __name__ == "__main__":
    main()
