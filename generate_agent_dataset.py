# Complete dataset generator for 15 MW Offshore Wind Turbine
import json
import os
import re
import sys


def generate_header():
    return """FUNCTION_BLOCK FB_WindTurbine_Offshore15MW_PitchYaw_LiDAR
(* ======================================================================================================================
   LUMINA CYBER-PHYSICAL SYSTEMS & ADVANCED PROCESS CONTROL SPECIFICATION
   System: Commercial Power & Renewable Energy: 15 MW Offshore Wind Turbine Individual Pitch Control (IPC) & Active Yaw
           System with Nacelle LiDAR Inflow Wind Feed-Forward
   Reference Architecture: IEA 15-MW Offshore Reference Wind Turbine (RWT) Monopile / Semi-Submersible Floating Foundation
   Target PLC Architecture: IEC 61131-3 Structured Text High-Performance Deterministic Cyclic Task (50 ms)
   Author: V7 Principal Automation Fellow & Cyber-Physical Systems Chair
   Operational Standards: IEC 61400-1 / IEC 61400-3-1 / IEC 61400-25 / DNV-ST-0437 / GL2010 / ISA-18.2 / IEEE 1547-2018
   ======================================================================================================================
   PHYSICAL PARAMETERS SUMMARY:
   - Rated Electrical Power: 15,000.0 kW (15.0 MW), Rated Mechanical Shaft Power: 15,716.0 kW
   - Rotor Diameter: 240.0 m, Swept Area: 45,238.93 m^2, Hub Height: 150.0 m Above Mean Sea Level (MSL)
   - Blade Length: 118.0 m, Tip Mass: 65,250 kg per blade, Drivetrain Inertia J_rotor: 3.10E+08 kg*m^2
   - Direct-Drive Permanent Magnet Synchronous Generator (PMSG) 4-Quadrant Back-to-Back MV Converter
   - Rated Rotor Speed: 7.55 rpm (0.7906 rad/s), Cut-In Speed: 3.0 m/s, Rated Wind Speed: 10.59 m/s, Cut-Out: 25.0 m/s
   - Individual Pitch Control (IPC): Multiblade Coordinate Coleman Transformation (d-q Axis) for 1P Tilt/Yaw Cancellation
   - Forward-Looking Nacelle Doppler LiDAR: 2.50 s Look-Ahead Preview (50-200 m Upstream Inflow Velocity Profile)
   - Active Yaw Drive: 8 Synchronized Planetary Azimuth Pinions with Proportional Hydraulic Caliper Counter-Torque
   - Active Tower Resonance Damping: 1st Fore-Aft (0.22 Hz) & Side-to-Side (0.21 Hz) Wave Resonance Mitigation
   - 16x16 Coupled Aeroelastic / Structural State-Space Model with Receding-Horizon MPC Quadratic Minimization
   - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting across 6 Critical Feedback Triads with Discrepancy Auditing
   - 12-Stage Deterministic Finite State Machine (FSM) with Bumpless Mode Transitions and ISA-18.2 Diagnostics
   ====================================================================================================================== *)
"""

def generate_var_input():
    return """VAR_INPUT
    (* Master Line Supervision & Safety Circuitry *)
    bEnableMaster                   : BOOL := FALSE;    (* [bool] Master turbine supervisory run permissive gate *)
    bEmergencyStopDualCh            : BOOL := TRUE;     (* [bool] Hardwired dual-channel active-low fail-safe E-stop *)
    bResetAlarms                    : BOOL := FALSE;    (* [bool] Manual / Remote supervisory alarm reset command pulse *)
    bAutoModeSelector               : BOOL := TRUE;     (* [bool] Autonomous closed-loop generation mode (TRUE=Auto, FALSE=Manual) *)
    bGridTiePermissive              : BOOL := FALSE;    (* [bool] Substation MV 66 kV collector bus synchronization permissive *)
    bRemoteCurtailmentEnable        : BOOL := FALSE;    (* [bool] Utility Transmission System Operator (TSO) curtailment active *)
    rCurtailmentLimit_kW            : REAL := 15000.0;  (* [kW] Maximum allowable active electrical power setpoint [kW] *)
    tTaskScanCycleTime              : TIME := T#50MS;   (* [ms] Deterministic cyclic controller task execution interval [ms] *)

    (* Substation 66 kV Medium-Voltage Electrical Grid Signals *)
    rGridVoltage_kV                 : REAL := 66.0;     (* [kV] 3-Phase line-to-line collector bus RMS voltage [kV] *)
    rGridFrequency_Hz               : REAL := 50.0;     (* [Hz] Electrical utility grid fundamental operating frequency [Hz] *)
    bLVRT_ActiveEvent               : BOOL := FALSE;    (* [bool] Low-Voltage Ride-Through fault trigger from converter protection *)
    bHVRT_ActiveEvent               : BOOL := FALSE;    (* [bool] High-Voltage Ride-Through overvoltage transient active *)

    (* Rotor Shaft Incremental Optical Pulse Encoders (2oo3 TMR Triad) *)
    rRotorSpeed_EncA_rpm            : REAL := 0.0;      (* [rpm] Low-speed rotor shaft optical encoder channel A [rpm] *)
    rRotorSpeed_EncB_rpm            : REAL := 0.0;      (* [rpm] Low-speed rotor shaft optical encoder channel B [rpm] *)
    rRotorSpeed_EncC_rpm            : REAL := 0.0;      (* [rpm] Low-speed rotor shaft optical encoder channel C [rpm] *)

    (* Direct-Drive PMSG Generator Rotor Speed Encoders (2oo3 TMR Triad) *)
    rGenSpeed_EncA_rpm              : REAL := 0.0;      (* [rpm] PMSG direct-drive rotor magnetic encoder channel A [rpm] *)
    rGenSpeed_EncB_rpm              : REAL := 0.0;      (* [rpm] PMSG direct-drive rotor magnetic encoder channel B [rpm] *)
    rGenSpeed_EncC_rpm              : REAL := 0.0;      (* [rpm] PMSG direct-drive rotor magnetic encoder channel C [rpm] *)

    (* Absolute Rotor Azimuth Angle Resolvers (2oo3 TMR Triad) *)
    rRotorAzimuth_ResA_deg          : REAL := 0.0;      (* [deg] Drivetrain absolute mechanical azimuth resolver channel A [deg] *)
    rRotorAzimuth_ResB_deg          : REAL := 0.0;      (* [deg] Drivetrain absolute mechanical azimuth resolver channel B [deg] *)
    rRotorAzimuth_ResC_deg          : REAL := 0.0;      (* [deg] Drivetrain absolute mechanical azimuth resolver channel C [deg] *)

    (* Blade Pitch Actuator Position & Hydraulic Pressure Feedbacks *)
    rBladePitch_ActPos_B1_deg       : REAL := 90.0;     (* [deg] Blade 1 absolute measured pitch angle from hub encoder [deg] *)
    rBladePitch_ActPos_B2_deg       : REAL := 90.0;     (* [deg] Blade 2 absolute measured pitch angle from hub encoder [deg] *)
    rBladePitch_ActPos_B3_deg       : REAL := 90.0;     (* [deg] Blade 3 absolute measured pitch angle from hub encoder [deg] *)
    rBladePitch_Pressure_B1_bar     : REAL := 210.0;    (* [bar] Blade 1 electrohydraulic pitch cylinder rail pressure [bar] *)
    rBladePitch_Pressure_B2_bar     : REAL := 210.0;    (* [bar] Blade 2 electrohydraulic pitch cylinder rail pressure [bar] *)
    rBladePitch_Pressure_B3_bar     : REAL := 210.0;    (* [bar] Blade 3 electrohydraulic pitch cylinder rail pressure [bar] *)
    rBladePitch_MotorCurrent_B1_A   : REAL := 0.0;      (* [A] Blade 1 backup electric pitch motor current feedback [A] *)
    rBladePitch_MotorCurrent_B2_A   : REAL := 0.0;      (* [A] Blade 2 backup electric pitch motor current feedback [A] *)
    rBladePitch_MotorCurrent_B3_A   : REAL := 0.0;      (* [A] Blade 3 backup electric pitch motor current feedback [A] *)

    (* Blade Root Optical Fiber Bragg Grating (FBG) Flapwise Strain 2oo3 TMR Triads *)
    rStrain_Flap_B1_ChA_ue          : REAL := 0.0;      (* [ue] Blade 1 root flapwise structural strain FBG sensor A [ue] *)
    rStrain_Flap_B1_ChB_ue          : REAL := 0.0;      (* [ue] Blade 1 root flapwise structural strain FBG sensor B [ue] *)
    rStrain_Flap_B1_ChC_ue          : REAL := 0.0;      (* [ue] Blade 1 root flapwise structural strain FBG sensor C [ue] *)
    rStrain_Flap_B2_ChA_ue          : REAL := 0.0;      (* [ue] Blade 2 root flapwise structural strain FBG sensor A [ue] *)
    rStrain_Flap_B2_ChB_ue          : REAL := 0.0;      (* [ue] Blade 2 root flapwise structural strain FBG sensor B [ue] *)
    rStrain_Flap_B2_ChC_ue          : REAL := 0.0;      (* [ue] Blade 2 root flapwise structural strain FBG sensor C [ue] *)
    rStrain_Flap_B3_ChA_ue          : REAL := 0.0;      (* [ue] Blade 3 root flapwise structural strain FBG sensor A [ue] *)
    rStrain_Flap_B3_ChB_ue          : REAL := 0.0;      (* [ue] Blade 3 root flapwise structural strain FBG sensor B [ue] *)
    rStrain_Flap_B3_ChC_ue          : REAL := 0.0;      (* [ue] Blade 3 root flapwise structural strain FBG sensor C [ue] *)
    rStrain_Edge_B1_ue              : REAL := 0.0;      (* [ue] Blade 1 root in-plane edgewise gravity bending strain [ue] *)
    rStrain_Edge_B2_ue              : REAL := 0.0;      (* [ue] Blade 2 root in-plane edgewise gravity bending strain [ue] *)
    rStrain_Edge_B3_ue              : REAL := 0.0;      (* [ue] Blade 3 root in-plane edgewise gravity bending strain [ue] *)

    (* Nacelle Met-Mast & Ultrasonic Environmental Feedbacks *)
    rWindSpeed_Cup_mps              : REAL := 8.5;      (* [m/s] Nacelle rear met-mast calibrated cup anemometer wind speed [m/s] *)
    rWindSpeed_Sonic_mps            : REAL := 8.5;      (* [m/s] Nacelle rear 3D ultrasonic anemometer horizontal wind speed [m/s] *)
    rWindDirection_Vane_deg         : REAL := 0.0;      (* [deg] Nacelle ultrasonic relative wind direction angle [deg] *)
    rAmbientAirTemp_degC            : REAL := 15.0;     (* [deg C] Offshore ambient dry-bulb atmospheric air temperature [deg C] *)
    rAirDensity_kg_m3               : REAL := 1.225;    (* [kg/m3] Corrected atmospheric air density at hub altitude [kg/m3] *)

    (* Nacelle Forward-Looking Pulsed Doppler LiDAR Preview Channels (2oo3 TMR) *)
    rLiDAR_WindSpeed_ChA_mps        : REAL := 8.5;      (* [m/s] Nacelle pulsed LiDAR preview horizontal velocity channel A [m/s] *)
    rLiDAR_WindSpeed_ChB_mps        : REAL := 8.5;      (* [m/s] Nacelle pulsed LiDAR preview horizontal velocity channel B [m/s] *)
    rLiDAR_WindSpeed_ChC_mps        : REAL := 8.5;      (* [m/s] Nacelle pulsed LiDAR preview horizontal velocity channel C [m/s] *)
    rLiDAR_FocalDistance_m          : REAL := 120.0;    (* [m] Configured upstream optical preview sensing focal distance [m] *)
    rLiDAR_ShearExponent_alpha      : REAL := 0.14;     (* [dim] Vertical wind shear profile power-law exponent alpha *)
    rLiDAR_GustPeak_mps             : REAL := 8.5;      (* [m/s] Incoming gust front estimated peak velocity amplitude [m/s] *)
    rLiDAR_TimeToImpact_s           : REAL := 2.50;     (* [s] Real-time calculated gust arrival preview horizon time [s] *)
    bLiDAR_DataValid                : BOOL := TRUE;     (* [bool] LiDAR optical transceiver signal-to-noise ratio health flag *)

    (* Tower Top & Offshore Substructure Dynamic Accelerometers (2oo3 TMR) *)
    rTowerAcc_FA_ChA_mps2           : REAL := 0.0;      (* [m/s^2] Tower top fore-aft seismic accelerometer channel A [m/s^2] *)
    rTowerAcc_FA_ChB_mps2           : REAL := 0.0;      (* [m/s^2] Tower top fore-aft seismic accelerometer channel B [m/s^2] *)
    rTowerAcc_FA_ChC_mps2           : REAL := 0.0;      (* [m/s^2] Tower top fore-aft seismic accelerometer channel C [m/s^2] *)
    rTowerAcc_SS_ChA_mps2           : REAL := 0.0;      (* [m/s^2] Tower top side-to-side seismic accelerometer channel A [m/s^2] *)
    rTowerAcc_SS_ChB_mps2           : REAL := 0.0;      (* [m/s^2] Tower top side-to-side seismic accelerometer channel B [m/s^2] *)
    rTowerAcc_SS_ChC_mps2           : REAL := 0.0;      (* [m/s^2] Tower top side-to-side seismic accelerometer channel C [m/s^2] *)
    rPlatformPitchAngle_deg         : REAL := 0.0;      (* [deg] Offshore semi-submersible platform pitch inclination [deg] *)
    rPlatformRollAngle_deg          : REAL := 0.0;      (* [deg] Offshore semi-submersible platform roll inclination [deg] *)

    (* Active Yaw Drive Azimuth System Feedbacks *)
    rNacelleHeading_deg             : REAL := 0.0;      (* [deg] Nacelle compass absolute geographic azimuth heading [deg] *)
    rCableTwist_deg                 : REAL := 0.0;      (* [deg] Down-tower droop cable accumulated torsion twist angle [deg] *)
    rYawBrakePressure_bar           : REAL := 160.0;    (* [bar] Yaw hydraulic friction brake caliper rail pressure [bar] *)
    rYawMotorCurrent_Avg_A          : REAL := 0.0;      (* [A] 8x yaw drive planetary gear motors average stator current [A] *)

    (* PMSG Generator & Converter Thermal / Electrical Feedback *)
    rBearingTemp_DE_degC            : REAL := 45.0;     (* [deg C] Direct-drive main bearing drive-end radial RTD temp [deg C] *)
    rBearingTemp_NDE_degC           : REAL := 43.0;     (* [deg C] Direct-drive main bearing non-drive-end RTD temp [deg C] *)
    rStatorWindingTemp_degC         : REAL := 65.0;     (* [deg C] PMSG multi-phase stator copper winding embedded RTD [deg C] *)
    rConverter_Vdc_V                : REAL := 1150.0;   (* [V] Full-scale back-to-back converter intermediate DC link [V] *)
    rConverter_Temp_IGBT_degC       : REAL := 55.0;     (* [deg C] Converter 4-quadrant IGBT power module junction temp [deg C] *)
END_VAR
"""

def generate_var_output():
    return """VAR_OUTPUT
    (* Converter Electrical Power & Torque Setpoint Commands *)
    bSystemReady                    : BOOL := FALSE;    (* [bool] Master turbine automated operation permissive healthy *)
    bTurbineTripped                 : BOOL := FALSE;    (* [bool] Hard emergency trip latch active, safety shutdown executed *)
    rGenTorque_Cmd_kNm              : REAL := 0.0;      (* [kN*m] Demanded electromagnetic generator airgap counter-torque [kN*m] *)
    rActivePower_Cmd_kW             : REAL := 0.0;      (* [kW] Demanded active power setpoint to 4-quadrant converter [kW] *)
    rReactivePower_Cmd_kVAR         : REAL := 0.0;      (* [kVAR] Demanded reactive power setpoint for grid voltage support [kVAR] *)
    bMainCircuitBreaker_ClosePermit : BOOL := FALSE;    (* [bool] Substation MV 66 kV main circuit breaker close command *)

    (* Individual Blade Pitch Actuator Actuation Demands *)
    rPitchCmd_Blade1_deg            : REAL := 90.0;     (* [deg] Fully unrolled pitch position setpoint blade 1 [deg] *)
    rPitchCmd_Blade2_deg            : REAL := 90.0;     (* [deg] Fully unrolled pitch position setpoint blade 2 [deg] *)
    rPitchCmd_Blade3_deg            : REAL := 90.0;     (* [deg] Fully unrolled pitch position setpoint blade 3 [deg] *)
    rPitchCmd_Collective_deg        : REAL := 90.0;     (* [deg] Baseline collective pitch angle demand [deg] *)
    rPitchOffset_IPC_B1_deg         : REAL := 0.0;      (* [deg] Coleman d-q multiblade IPC load reduction offset blade 1 [deg] *)
    rPitchOffset_IPC_B2_deg         : REAL := 0.0;      (* [deg] Coleman d-q multiblade IPC load reduction offset blade 2 [deg] *)
    rPitchOffset_IPC_B3_deg         : REAL := 0.0;      (* [deg] Coleman d-q multiblade IPC load reduction offset blade 3 [deg] *)
    rPitchOffset_LiDAR_FF_deg       : REAL := 0.0;      (* [deg] Inflow LiDAR preview feed-forward pitch bias command [deg] *)
    rPitchOffset_TowerFA_deg        : REAL := 0.0;      (* [deg] Active tower fore-aft damping pitch trimming offset [deg] *)
    rTorqueOffset_TowerSS_kNm       : REAL := 0.0;      (* [kN*m] Active tower side-to-side damping torque trimming offset [kN*m] *)

    (* Active Yaw Drive System Commands *)
    bYawDriveCW_Enable              : BOOL := FALSE;    (* [bool] Command to yaw nacelle clockwise toward positive azimuth *)
    bYawDriveCCW_Enable             : BOOL := FALSE;    (* [bool] Command to yaw nacelle counter-clockwise toward negative azimuth *)
    rYawRate_Cmd_degps              : REAL := 0.0;      (* [deg/s] Commanded nacelle azimuthal slewing rotational rate [deg/s] *)
    rYawMotorTorque_Cmd_kNm         : REAL := 0.0;      (* [kN*m] Total drive torque commanded across 8 yaw drive pinions [kN*m] *)
    rYawBrakePressure_Cmd_bar       : REAL := 160.0;    (* [bar] Dynamic hydraulic caliper backpressure regulation command [bar] *)
    bMechanicalLock_Engage          : BOOL := TRUE;     (* [bool] High-speed emergency rotor caliper mechanical brake engage *)
    bCableUntwistActive             : BOOL := FALSE;    (* [bool] Automated droop cable unwinding sequence executing *)

    (* Multiblade Coordinate IPC Load Metrics *)
    rTiltMoment_1P_kNm              : REAL := 0.0;      (* [kN*m] Aerodynamic tilt bending moment on main hub bearing (d-axis) [kN*m] *)
    rYawMoment_1P_kNm               : REAL := 0.0;      (* [kN*m] Aerodynamic yaw bending moment on main hub bearing (q-axis) [kN*m] *)
    rPitch_d_axis_deg               : REAL := 0.0;      (* [deg] Coleman multiblade d-axis (tilt cancellation) pitch demand [deg] *)
    rPitch_q_axis_deg               : REAL := 0.0;      (* [deg] Coleman multiblade q-axis (yaw cancellation) pitch demand [deg] *)

    (* Inflow LiDAR Preview & Structural Velocities *)
    bLiDAR_GustDetected             : BOOL := FALSE;    (* [bool] High-amplitude gust front detected upstream by preview filter *)
    rLiDAR_PreviewWindSpeed_mps     : REAL := 0.0;      (* [m/s] Synchronized look-ahead inflow wind velocity at rotor plane [m/s] *)
    rTowerTopVelocity_FA_mps        : REAL := 0.0;      (* [m/s] Estimated tower top fore-aft structural deflection velocity [m/s] *)
    rTowerTopVelocity_SS_mps        : REAL := 0.0;      (* [m/s] Estimated tower top side-to-side structural deflection velocity [m/s] *)

    (* TMR 2oo3 Sensor Voted Output Values *)
    rVoted_RotorSpeed_rpm           : REAL := 0.0;      (* [rpm] TMR voted low-speed rotor rotational velocity [rpm] *)
    rVoted_GenSpeed_rpm             : REAL := 0.0;      (* [rpm] TMR voted PMSG direct-drive generator rotor speed [rpm] *)
    rVoted_LiDAR_WindSpeed_mps      : REAL := 0.0;      (* [m/s] TMR voted upstream preview wind velocity [m/s] *)
    rVoted_TowerAcc_FA_mps2         : REAL := 0.0;      (* [m/s^2] TMR voted tower top fore-aft acceleration [m/s^2] *)
    rVoted_TowerAcc_SS_mps2         : REAL := 0.0;      (* [m/s^2] TMR voted tower top side-to-side acceleration [m/s^2] *)
    rVoted_Strain_Flap_B1_ue        : REAL := 0.0;      (* [ue] TMR voted blade 1 flapwise root bending strain [ue] *)
    rVoted_Strain_Flap_B2_ue        : REAL := 0.0;      (* [ue] TMR voted blade 2 flapwise root bending strain [ue] *)
    rVoted_Strain_Flap_B3_ue        : REAL := 0.0;      (* [ue] TMR voted blade 3 flapwise root bending strain [ue] *)

    (* Operational State & ISA-18.2 Bit-Packed Diagnostic Words *)
    iOperatingFSMState              : INT := 0;         (* [enum] Master FSM state index (0..11) *)
    iControlRegion                  : INT := 0;         (* [enum] Aerodynamic operational region (1, 2, 25, 3) *)
    dwTurbineStatusWord1            : DWORD := 16#00000000; (* [dword] Subsystem operating status telemetry flags *)
    dwTurbineStatusWord2            : DWORD := 16#00000000; (* [dword] IPC, LiDAR preview, and active yaw status flags *)
    dwAlarmWord_Critical            : DWORD := 16#00000000; (* [dword] ISA-18.2 Category 1 emergency trip shutdown alarms *)
    dwAlarmWord_Warning             : DWORD := 16#00000000; (* [dword] ISA-18.2 Category 2 operational warning and derating alarms *)
    dwSensorDegradedMask            : DWORD := 16#00000000; (* [dword] 2oo3 TMR sensor redundancy channel degradation mask *)
END_VAR
"""

def generate_var():
    return """VAR
    (* Discrete State-Space Model 16x16 State Matrices & Vectors *)
    matA                            : ARRAY[1..16, 1..16] OF REAL;  (* Discrete transition state matrix A (16x16) *)
    matB                            : ARRAY[1..16, 1..8] OF REAL;   (* Input distribution matrix B (16x8) *)
    matC                            : ARRAY[1..8, 1..16] OF REAL;   (* Measurement output matrix C (8x16) *)
    matD                            : ARRAY[1..8, 1..8] OF REAL;    (* Direct feedthrough matrix D (8x8) *)
    vecX                            : ARRAY[1..16] OF REAL;         (* Current estimated state vector x[k] *)
    vecX_next                       : ARRAY[1..16] OF REAL;         (* Propagated next state vector x[k+1] *)
    vecX_pred                       : ARRAY[1..16] OF REAL;         (* Multi-step predicted state vector x_pred *)
    vecU                            : ARRAY[1..8] OF REAL;          (* Current plant control/disturbance input vector u[k] *)
    vecY                            : ARRAY[1..8] OF REAL;          (* Calculated output measurement vector y[k] *)
    vecU_min                        : ARRAY[1..8] OF REAL;          (* Actuator lower saturation constraints u_min *)
    vecU_max                        : ARRAY[1..8] OF REAL;          (* Actuator upper saturation constraints u_max *)
    vecX_min                        : ARRAY[1..16] OF REAL;         (* State physical lower safety boundaries x_min *)
    vecX_max                        : ARRAY[1..16] OF REAL;         (* State physical upper safety boundaries x_max *)
    bMatricesInitialized           : BOOL := FALSE;                (* Initialization latch flag for state-space matrices *)

    (* Model Predictive Control (MPC) Receding-Horizon Quadratic Optimization *)
    vecQ                            : ARRAY[1..16] OF REAL;         (* Diagonal state regulation penalty weights Q *)
    vecR                            : ARRAY[1..8] OF REAL;          (* Diagonal actuator effort penalty weights R *)
    vecP                            : ARRAY[1..16] OF REAL;         (* Diagonal terminal state penalty weights P *)
    vecGradient                     : ARRAY[1..8] OF REAL;          (* Quadratic cost objective gradient vector *)
    vecU_opt                        : ARRAY[1..8] OF REAL;          (* Optimal control action vector from projected gradient *)
    rMPC_StepSize                   : REAL := 0.015;                (* Projected gradient descent step size alpha *)
    rMPC_CostCurrent                : REAL := 0.0;                  (* Evaluated quadratic cost function value *)
    rMPC_CostPrevious               : REAL := 0.0;                  (* Previous iteration objective value for convergence check *)
    iMPC_Iter                       : INT := 0;                     (* Internal solver iteration loop index *)
    iHorizonStep                    : INT := 0;                     (* Receding prediction horizon stage index (1..5) *)
    idx_i                           : INT := 0;                     (* General purpose matrix row iterator *)
    idx_j                           : INT := 0;                     (* General purpose matrix column iterator *)
    idx_k                           : INT := 0;                     (* General purpose vector element iterator *)

    (* Nacelle Forward-Looking Pulsed Doppler LiDAR 50-Stage Preview Ring Buffer *)
    aLiDAR_PreviewBuffer            : ARRAY[0..49] OF REAL;         (* Inflow wind velocity preview delay ring buffer (50x50ms=2.5s) *)
    iLiDAR_WriteIdx                 : INT := 0;                     (* Ring buffer incoming data insertion pointer *)
    iLiDAR_BufferCount              : INT := 0;                     (* Total populated preview samples count *)
    rLiDAR_PrevFilteredSpeed        : REAL := 8.5;                  (* Previous cycle low-pass filtered LiDAR velocity [m/s] *)
    rLiDAR_Acceleration_mps2        : REAL := 0.0;                  (* Inflow gust front acceleration dv/dt [m/s^2] *)
    rLiDAR_TargetDelay_s            : REAL := 2.50;                 (* Dynamic preview delay based on focal distance and speed [s] *)
    iLiDAR_DelaySamples             : INT := 50;                    (* Calculated discrete buffer delay steps *)
    iLiDAR_ReadIdx                  : INT := 0;                     (* Synchronized playback extraction pointer *)
    rLiDAR_Sensitivity_deg_per_mps  : REAL := 1.450;                (* Region III aerodynamic pitch sensitivity dTheta/dv [deg/(m/s)] *)
    rLiDAR_BoostGain                : REAL := 0.850;                (* Dynamic gust acceleration pitch rate booster coefficient *)

    (* Multiblade Coordinate Coleman Transformation (1P Individual Pitch Control) *)
    rAzimuth_Rad                    : REAL := 0.0;                  (* Voted rotor mechanical azimuth angle in radians [rad] *)
    rPsi_B1                         : REAL := 0.0;                  (* Blade 1 instantaneous azimuthal position angle [rad] *)
    rPsi_B2                         : REAL := 0.0;                  (* Blade 2 instantaneous azimuthal position angle [rad] *)
    rPsi_B3                         : REAL := 0.0;                  (* Blade 3 instantaneous azimuthal position angle [rad] *)
    rCos_B1                         : REAL := 1.0;                  (* cos(psi_1) Coleman multiblade basis function *)
    rSin_B1                         : REAL := 0.0;                  (* sin(psi_1) Coleman multiblade basis function *)
    rCos_B2                         : REAL := -0.5;                 (* cos(psi_2) Coleman multiblade basis function *)
    rSin_B2                         : REAL := 0.866025;             (* sin(psi_2) Coleman multiblade basis function *)
    rCos_B3                         : REAL := -0.5;                 (* cos(psi_3) Coleman multiblade basis function *)
    rSin_B3                         : REAL := -0.866025;            (* sin(psi_3) Coleman multiblade basis function *)
    rMoment_B1_kNm                  : REAL := 0.0;                  (* Reconstructed root flapwise moment blade 1 [kN*m] *)
    rMoment_B2_kNm                  : REAL := 0.0;                  (* Reconstructed root flapwise moment blade 2 [kN*m] *)
    rMoment_B3_kNm                  : REAL := 0.0;                  (* Reconstructed root flapwise moment blade 3 [kN*m] *)
    rTilt_Error_kNm                 : REAL := 0.0;                  (* D-axis multiblade tilt bending moment error [kN*m] *)
    rYaw_Error_kNm                  : REAL := 0.0;                  (* Q-axis multiblade yaw bending moment error [kN*m] *)
    rIPC_Tilt_Integral              : REAL := 0.0;                  (* D-axis multiblade integral accumulator [deg] *)
    rIPC_Yaw_Integral               : REAL := 0.0;                  (* Q-axis multiblade integral accumulator [deg] *)
    rIPC_Kp                         : REAL := 0.00045;              (* Coleman IPC proportional gain [deg/(kN*m)] *)
    rIPC_Ki                         : REAL := 0.00015;              (* Coleman IPC integral gain [deg/(kN*m*s)] *)
    rIPC_MaxOffset_deg              : REAL := 3.50;                 (* Individual pitch saturation limit authority (+/- 3.5 deg) *)

    (* Active Offshore Substructure / Tower Resonance Damping *)
    rTower_FA_FilterState1          : REAL := 0.0;                  (* Fore-aft 2nd-order bandpass resonance filter state 1 *)
    rTower_FA_FilterState2          : REAL := 0.0;                  (* Fore-aft 2nd-order bandpass resonance filter state 2 *)
    rTower_SS_FilterState1          : REAL := 0.0;                  (* Side-to-side 2nd-order bandpass resonance filter state 1 *)
    rTower_SS_FilterState2          : REAL := 0.0;                  (* Side-to-side 2nd-order bandpass resonance filter state 2 *)
    rTower_Omega_FA                 : REAL := 1.3823;               (* 1st fore-aft natural frequency: 0.22 Hz * 2*pi [rad/s] *)
    rTower_Zeta_FA                  : REAL := 0.150;                (* Fore-aft active damping target damping ratio *)
    rTower_Omega_SS                 : REAL := 1.3195;               (* 1st side-to-side natural frequency: 0.21 Hz * 2*pi [rad/s] *)
    rTower_Zeta_SS                  : REAL := 0.150;                (* Side-to-side active damping target damping ratio *)
    rGain_TowerDamping_FA           : REAL := 0.850;                (* Fore-aft collective pitch damping gain [deg/(m/s)] *)
    rGain_TowerDamping_SS           : REAL := 450.0;                (* Side-to-side generator torque damping gain [kN*m/(m/s)] *)

    (* Active Yaw Drive Azimuth Alignment & Friction Brake Coordination *)
    rWindDir_Filtered_deg           : REAL := 0.0;                  (* Low-pass filtered wind direction relative to nacelle [deg] *)
    rYawTrackingError_deg           : REAL := 0.0;                  (* Angular difference between nacelle heading and wind vector [deg] *)
    tYawMisalignmentTimer           : TON;                          (* Yaw misalignment deadband integration timer *)
    tYawDurationTimer               : TON;                          (* Yaw active movement execution timer *)
    tCableUntwistTimer              : TON;                          (* Cable unwinding sequence execution timer *)
    bYawActive                      : BOOL := FALSE;                (* Active yaw azimuth slew drive motion in progress *)
    rYawRate_Nominal_degps          : REAL := 0.50;                 (* Nominal azimuthal slew speed (0.50 deg/s) *)
    rYawHoldingPressure_bar         : REAL := 160.0;                (* Caliper static holding friction clamping pressure [bar] *)
    rYawSlippingPressure_bar        : REAL := 35.0;                 (* Caliper dynamic anti-backlash counter-torque pressure [bar] *)
    rRotorInertia_kgm2              : REAL := 3.10E+08;             (* Rotor polar moment of inertia J_rotor [kg*m^2] *)
    rGyroscopicTiltTorque_kNm       : REAL := 0.0;                  (* Calculated gyroscopic precessional moment during yawing [kN*m] *)

    (* Collective Pitch Speed / Power Regulation Controller *)
    rSpeed_Error_rpm                : REAL := 0.0;                  (* Rotor rotational speed tracking error (rated - actual) [rpm] *)
    rPitch_Integral_deg             : REAL := 0.0;                  (* Region III collective pitch integrator state [deg] *)
    rPitch_Kp                       : REAL := 3.250;                (* Collective pitch gain-scheduled proportional gain [deg/rpm] *)
    rPitch_Ki                       : REAL := 0.950;                (* Collective pitch gain-scheduled integral gain [deg/(rpm*s)] *)
    rPitch_Rated_deg                : REAL := 0.0;                  (* Region II fine pitch angle optimal benchmark [deg] *)
    rPitch_Feather_deg              : REAL := 90.0;                 (* Aerodynamic feathered shutdown parking pitch [deg] *)
    rPitchRateLimit_degps           : REAL := 8.0;                  (* Maximum electrohydraulic pitch actuator slewing rate [deg/s] *)
    rPrevPitchCmd_deg               : REAL := 90.0;                 (* Prior cycle collective pitch demand memory for rate limiting *)

    (* Region II Aerodynamic Maximum Power Cp Tracking (K_opt * Omega^2) *)
    rK_opt                          : REAL := 31800.0;              (* Aerodynamic torque tracking coefficient [kN*m/(rad/s)^2] *)
    rRotorSpeed_radps               : REAL := 0.0;                  (* Rotor speed converted to angular velocity [rad/s] *)
    rTorque_Opt_kNm                 : REAL := 0.0;                  (* Region II calculated aerodynamic target torque [kN*m] *)
    rRatedTorque_kNm                : REAL := 19878.0;              (* Continuous rated generator electromagnetic torque [kN*m] *)
    rRatedRotorSpeed_rpm            : REAL := 7.550;                (* Continuous rated rotor rotational speed [rpm] *)
    rRatedPower_kW                  : REAL := 15000.0;              (* Continuous rated electrical power output [kW] *)

    (* 2oo3 TMR Sensor Redundancy Verification Structures & Discrepancy Timers *)
    tDiscrepancy_RotorSpeed         : TON;                          (* Rotor speed encoder discrepancy timer *)
    tDiscrepancy_GenSpeed           : TON;                          (* Generator speed encoder discrepancy timer *)
    tDiscrepancy_LiDAR              : TON;                          (* LiDAR preview channels discrepancy timer *)
    tDiscrepancy_TowerAccFA         : TON;                          (* Tower fore-aft accelerometer discrepancy timer *)
    tDiscrepancy_TowerAccSS         : TON;                          (* Tower side-to-side accelerometer discrepancy timer *)
    tDiscrepancy_StrainB1           : TON;                          (* Blade 1 strain gauges discrepancy timer *)
    tDiscrepancy_StrainB2           : TON;                          (* Blade 2 strain gauges discrepancy timer *)
    tDiscrepancy_StrainB3           : TON;                          (* Blade 3 strain gauges discrepancy timer *)
    bDegraded_RotorSpeed            : BOOL := FALSE;                (* 1oo2 fail-operational mode flag rotor speed *)
    bDegraded_GenSpeed              : BOOL := FALSE;                (* 1oo2 fail-operational mode flag generator speed *)
    bDegraded_LiDAR                 : BOOL := FALSE;                (* 1oo2 fail-operational mode flag LiDAR preview *)
    bDegraded_TowerAccFA            : BOOL := FALSE;                (* 1oo2 fail-operational mode flag tower fore-aft *)
    bDegraded_TowerAccSS            : BOOL := FALSE;                (* 1oo2 fail-operational mode flag tower side-to-side *)
    bDegraded_StrainB1              : BOOL := FALSE;                (* 1oo2 fail-operational mode flag blade 1 strain *)
    bDegraded_StrainB2              : BOOL := FALSE;                (* 1oo2 fail-operational mode flag blade 2 strain *)
    bDegraded_StrainB3              : BOOL := FALSE;                (* 1oo2 fail-operational mode flag blade 3 strain *)

    (* Operational State Machine Timers & Coordination *)
    tFSM_StateTimer                 : TON;                          (* General state dwell and timeout timer *)
    tFSM_GridSyncTimer              : TON;                          (* Grid tie synchronization timeout monitor *)
    tFSM_SpinUpTimer                : TON;                          (* Rotor idling spin-up acceleration monitor *)
    tFSM_BrakingTimer               : TON;                          (* Aerodynamic braking deceleration timeout monitor *)
    tFSM_FRTTimer                   : TON;                          (* Fault ride-through event duration monitor *)
    rWindSpeed_Filtered_mps         : REAL := 8.5;                  (* 10-second moving average wind velocity [m/s] *)
    bStormCutOutLatched             : BOOL := FALSE;                (* High wind storm cut-out hysteresis trip latch *)

    (* ISA-18.2 Multi-Tiered Alarms & Protection Trip Parameters *)
    c_rOverspeed_HH_rpm             : REAL := 8.682;                (* 115% Rated rotor speed critical trip limit [rpm] *)
    c_rOverspeed_H_rpm              : REAL := 8.154;                (* 108% Rated rotor speed warning derate limit [rpm] *)
    c_rTowerAcc_HH_mps2             : REAL := 2.450;                (* 0.25 g Peak tower vibration emergency trip limit [m/s^2] *)
    c_rTowerAcc_H_mps2              : REAL := 1.750;                (* Tower vibration warning threshold [m/s^2] *)
    c_rMainBearingTemp_HH_degC      : REAL := 85.0;                 (* Main PMSG bearing overtemperature trip limit [deg C] *)
    c_rMainBearingTemp_H_degC       : REAL := 75.0;                 (* Main PMSG bearing high warning threshold [deg C] *)
    c_rStatorTemp_HH_degC           : REAL := 125.0;                (* PMSG multi-phase stator winding trip limit [deg C] *)
    c_rStatorTemp_H_degC            : REAL := 105.0;                (* PMSG multi-phase stator winding warning threshold [deg C] *)
    c_rConverterVdc_HH_V            : REAL := 1350.0;               (* Converter DC link overvoltage emergency trip [V] *)
    c_rConverterVdc_LL_V            : REAL := 850.0;                (* Converter DC link undervoltage trip [V] *)
    c_rPitchDiscrepancy_Max_deg     : REAL := 1.80;                 (* Maximum allowable pitch tracking discrepancy [deg] *)
    tPitchDiscrepancyTimer          : TON;                          (* Pitch discrepancy fault integration timer *)
END_VAR
"""

def generate_phase0():
    lines = []
    lines.append("""(* ======================================================================================================================
   PHASE 0: DISCRETE STATE-SPACE MATRICES & OPTIMIZATION BOUNDS INITIALIZATION
   Coupled 16x16 Aeroelastic, Torsional Drivetrain, Multi-Blade Flapwise, Tower Top and Floating Spar Dynamics
   Sample Interval Ts = 50 ms (0.050 s). Calibrated to IEA 15-MW Offshore Reference Wind Turbine.
   ====================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* Matrix A Initialization: 16x16 Continuous-to-Discrete State Matrix (Ts = 50 ms) *)""")

    # 16 states:
    # 1: Rotor speed deviation [rad/s]
    # 2: Generator rotor speed deviation [rad/s]
    # 3: Drivetrain shaft torsional deflection [rad]
    # 4: Blade 1 flapwise deflection [m]
    # 5: Blade 1 flapwise velocity [m/s]
    # 6: Blade 2 flapwise deflection [m]
    # 7: Blade 2 flapwise velocity [m/s]
    # 8: Blade 3 flapwise deflection [m]
    # 9: Blade 3 flapwise velocity [m/s]
    # 10: Tower top fore-aft displacement [m]
    # 11: Tower top fore-aft velocity [m/s]
    # 12: Tower top side-to-side displacement [m]
    # 13: Tower top side-to-side velocity [m/s]
    # 14: Nacelle yaw misalignment [rad]
    # 15: Floating platform pitch tilt [rad]
    # 16: Floating platform pitch rate [rad/s]

    # Generate all 256 entries of matA with realistic values
    for i in range(1, 17):
        for j in range(1, 17):
            val = 0.0
            comment = ""
            if i == j:
                # Diagonal terms
                if i in [1, 2]: val = 0.985420; comment = "Rotational speed self-decay"
                elif i == 3: val = 0.992150; comment = "Shaft twist damping retention"
                elif i in [4, 6, 8]: val = 0.978200; comment = "Flapwise displacement modal decay"
                elif i in [5, 7, 9]: val = 0.965400; comment = "Flapwise velocity aerodynamic damping"
                elif i in [10, 12]: val = 0.994300; comment = "Tower displacement modal decay"
                elif i in [11, 13]: val = 0.981200; comment = "Tower velocity structural damping"
                elif i == 14: val = 0.999500; comment = "Yaw alignment kinematic persistence"
                elif i == 15: val = 0.996800; comment = "Platform hydrostatic pitch stiffness"
                elif i == 16: val = 0.987500; comment = "Platform hydrodynamic radiation damping"
            elif (i == 1 and j == 3): val = -0.014250; comment = "Rotor speed torque reaction from shaft twist"
            elif (i == 2 and j == 3): val = 0.042850; comment = "Generator speed torque reaction from shaft twist"
            elif (i == 3 and j == 1): val = 0.050000; comment = "Kinematic integration: dTheta = Omega_r - Omega_g"
            elif (i == 3 and j == 2): val = -0.050000; comment = "Kinematic integration: dTheta = Omega_r - Omega_g"
            elif (i == 4 and j == 5): val = 0.050000; comment = "Blade 1 kinematic integration: dz = v * dt"
            elif (i == 5 and j == 4): val = -0.182400; comment = "Blade 1 flapwise 1st mode stiffness"
            elif (i == 6 and j == 7): val = 0.050000; comment = "Blade 2 kinematic integration: dz = v * dt"
            elif (i == 7 and j == 6): val = -0.182400; comment = "Blade 2 flapwise 1st mode stiffness"
            elif (i == 8 and j == 9): val = 0.050000; comment = "Blade 3 kinematic integration: dz = v * dt"
            elif (i == 9 and j == 8): val = -0.182400; comment = "Blade 3 flapwise 1st mode stiffness"
            elif (i == 10 and j == 11): val = 0.050000; comment = "Tower FA displacement kinematic integration"
            elif (i == 11 and j == 10): val = -0.095400; comment = "Tower FA 1st eigenmode stiffness (0.22 Hz)"
            elif (i == 12 and j == 13): val = 0.050000; comment = "Tower SS displacement kinematic integration"
            elif (i == 13 and j == 12): val = -0.087200; comment = "Tower SS 1st eigenmode stiffness (0.21 Hz)"
            elif (i == 11 and j in [4, 6, 8]): val = 0.008450; comment = "Rotor total thrust coupling into tower FA"
            elif (i == 15 and j == 16): val = 0.050000; comment = "Platform pitch kinematic integration"
            elif (i == 16 and j == 15): val = -0.024500; comment = "Platform hydrostatic righting moment"
            elif (i == 16 and j == 11): val = 0.003150; comment = "Tower-foundation surge-pitch coupling"
            else:
                val = 0.0
                comment = "Uncoupled state coordinate"
            lines.append(f"    matA[{i}, {j}] := {val:.6f}; (* {comment} *)")

    lines.append("\n    (* Matrix B Initialization: 16x8 Input Distribution Matrix *)")
    # 8 inputs:
    # 1: T_gen [kNm]
    # 2: Theta_1 [deg]
    # 3: Theta_2 [deg]
    # 4: Theta_3 [deg]
    # 5: Tau_yaw [kNm]
    # 6: V_LiDAR [m/s]
    # 7: Alpha_shear [-]
    # 8: M_wave [kNm]
    for i in range(1, 17):
        for k in range(1, 9):
            val = 0.0
            comment = ""
            if (i == 2 and k == 1): val = -0.000315; comment = "Generator torque load decel on PMSG rotor"
            elif (i == 1 and k in [2, 3, 4]): val = -0.001850; comment = "Aerodynamic torque reduction per pitch deg"
            elif (i == 5 and k == 2): val = -0.085400; comment = "Blade 1 flapwise thrust shed per pitch deg"
            elif (i == 7 and k == 3): val = -0.085400; comment = "Blade 2 flapwise thrust shed per pitch deg"
            elif (i == 9 and k == 4): val = -0.085400; comment = "Blade 3 flapwise thrust shed per pitch deg"
            elif (i == 11 and k in [2, 3, 4]): val = -0.021500; comment = "Tower FA thrust relief from collective pitch"
            elif (i == 13 and k == 1): val = 0.000125; comment = "Tower SS reaction torque from generator"
            elif (i == 14 and k == 5): val = 0.000450; comment = "Active yaw drive slewing torque authority"
            elif (i == 1 and k == 6): val = 0.014200; comment = "Inflow wind velocity aerodynamic torque drive"
            elif (i in [5, 7, 9] and k == 6): val = 0.048200; comment = "Inflow gust dynamic thrust force on blades"
            elif (i == 11 and k == 6): val = 0.028500; comment = "Tower FA base shear from preview wind gust"
            elif (i == 5 and k == 7): val = 0.012500; comment = "Vertical wind shear gradient cyclic thrust B1"
            elif (i == 7 and k == 7): val = -0.006250; comment = "Vertical wind shear gradient cyclic thrust B2"
            elif (i == 9 and k == 7): val = -0.006250; comment = "Vertical wind shear gradient cyclic thrust B3"
            elif (i == 16 and k == 8): val = 0.000085; comment = "Hydrodynamic wave moment pitching acceleration"
            else:
                val = 0.0
                comment = "Zero direct input feed"
            lines.append(f"    matB[{i}, {k}] := {val:.6f}; (* {comment} *)")

    lines.append("\n    (* Matrix C Initialization: 8x16 Measurement Output Matrix *)")
    for m in range(1, 9):
        for i in range(1, 17):
            val = 0.0
            comment = ""
            if (m == 1 and i == 1): val = 9.549296; comment = "Rotor speed rad/s to rpm conversion (60 / 2pi)"
            elif (m == 2 and i == 2): val = 9.549296; comment = "Gen speed rad/s to rpm conversion (60 / 2pi)"
            elif (m == 3 and i == 4): val = 800.000000; comment = "Blade 1 root flapwise moment from tip deflection"
            elif (m == 4 and i == 6): val = 800.000000; comment = "Blade 2 root flapwise moment from tip deflection"
            elif (m == 5 and i == 8): val = 800.000000; comment = "Blade 3 root flapwise moment from tip deflection"
            elif (m == 6 and i == 11): val = 1.000000; comment = "Tower top fore-aft seismic acceleration"
            elif (m == 7 and i == 13): val = 1.000000; comment = "Tower top side-to-side seismic acceleration"
            elif (m == 8 and i == 15): val = 57.295780; comment = "Platform pitch radians to degrees"
            else:
                val = 0.0
                comment = "Unobserved state in output channel"
            lines.append(f"    matC[{m}, {i}] := {val:.6f}; (* {comment} *)")

    lines.append("\n    (* Matrix D Initialization: 8x8 Direct Feedthrough Matrix *)")
    for m in range(1, 9):
        for k in range(1, 9):
            val = 0.0
            comment = "Zero direct feedthrough"
            if (m == 6 and k == 6): val = 0.012500; comment = "High-frequency aerodynamic thrust feedthrough"
            lines.append(f"    matD[{m}, {k}] := {val:.6f}; (* {comment} *)")

    lines.append("\n    (* MPC Diagonal State Regulation Penalty Weights Q (16 States) *)")
    q_weights = [
        ("vecQ[1]", 120.0, "Rotor speed deviation penalty"),
        ("vecQ[2]", 100.0, "Generator speed deviation penalty"),
        ("vecQ[3]", 85.0, "Drivetrain shaft twist stress penalty"),
        ("vecQ[4]", 45.0, "Blade 1 flapwise deflection penalty"),
        ("vecQ[5]", 25.0, "Blade 1 flapwise velocity penalty"),
        ("vecQ[6]", 45.0, "Blade 2 flapwise deflection penalty"),
        ("vecQ[7]", 25.0, "Blade 2 flapwise velocity penalty"),
        ("vecQ[8]", 45.0, "Blade 3 flapwise deflection penalty"),
        ("vecQ[9]", 25.0, "Blade 3 flapwise velocity penalty"),
        ("vecQ[10]", 150.0, "Tower FA displacement fatigue penalty"),
        ("vecQ[11]", 90.0, "Tower FA velocity kinetic penalty"),
        ("vecQ[12]", 130.0, "Tower SS displacement fatigue penalty"),
        ("vecQ[13]", 80.0, "Tower SS velocity kinetic penalty"),
        ("vecQ[14]", 60.0, "Nacelle yaw tracking error penalty"),
        ("vecQ[15]", 110.0, "Platform pitch inclination penalty"),
        ("vecQ[16]", 75.0, "Platform pitch velocity penalty")
    ]
    for name, w, c in q_weights:
        lines.append(f"    {name} := {w:.1f}; (* {c} *)")

    lines.append("\n    (* MPC Diagonal Actuator Effort Penalty Weights R (8 Inputs) *)")
    r_weights = [
        ("vecR[1]", 0.000025, "Generator torque rate-of-change penalty"),
        ("vecR[2]", 0.150000, "Blade 1 pitch actuator effort penalty"),
        ("vecR[3]", 0.150000, "Blade 2 pitch actuator effort penalty"),
        ("vecR[4]", 0.150000, "Blade 3 pitch actuator effort penalty"),
        ("vecR[5]", 0.005000, "Yaw drive motor torque effort penalty"),
        ("vecR[6]", 0.000000, "LiDAR preview disturbance weight (unpenalized)"),
        ("vecR[7]", 0.000000, "Wind shear disturbance weight (unpenalized)"),
        ("vecR[8]", 0.000000, "Hydrodynamic wave moment weight (unpenalized)")
    ]
    for name, w, c in r_weights:
        lines.append(f"    {name} := {w:.6f}; (* {c} *)")

    lines.append("\n    (* MPC Diagonal Terminal State Penalty Weights P (16 States) *)")
    for i in range(1, 17):
        p_val = q_weights[i-1][1] * 3.5
        lines.append(f"    vecP[{i}] := {p_val:.1f}; (* Terminal cost weight state {i} *)")

    lines.append("\n    (* Actuator Physical Lower & Upper Saturation Boundaries [u_min, u_max] *)")
    u_bounds = [
        ("vecU_min[1]", 0.0, "vecU_max[1]", 24000.0, "Generator airgap torque [kN*m]"),
        ("vecU_min[2]", -1.0, "vecU_max[2]", 90.0, "Blade 1 pitch angle [deg]"),
        ("vecU_min[3]", -1.0, "vecU_max[3]", 90.0, "Blade 2 pitch angle [deg]"),
        ("vecU_min[4]", -1.0, "vecU_max[4]", 90.0, "Blade 3 pitch angle [deg]"),
        ("vecU_min[5]", -4500.0, "vecU_max[5]", 4500.0, "Yaw drive total torque [kN*m]"),
        ("vecU_min[6]", 0.0, "vecU_max[6]", 50.0, "LiDAR inflow velocity [m/s]"),
        ("vecU_min[7]", 0.0, "vecU_max[7]", 0.50, "Vertical shear exponent [-]"),
        ("vecU_min[8]", -15000.0, "vecU_max[8]", 15000.0, "Wave pitching moment [kN*m]")
    ]
    for umin_n, umin_v, umax_n, umax_v, c in u_bounds:
        lines.append(f"    {umin_n} := {umin_v:.1f}; {umax_n} := {umax_v:.1f}; (* {c} *)")

    lines.append("\n    (* State Vector Physical Lower & Upper Safety Envelope [x_min, x_max] *)")
    x_bounds = [
        (-0.50, 0.50, "Rotor speed deviation [rad/s]"),
        (-0.50, 0.50, "Generator speed deviation [rad/s]"),
        (-0.10, 0.10, "Shaft torsional deflection [rad]"),
        (-8.0, 15.0, "Blade 1 flapwise deflection [m]"),
        (-12.0, 12.0, "Blade 1 flapwise velocity [m/s]"),
        (-8.0, 15.0, "Blade 2 flapwise deflection [m]"),
        (-12.0, 12.0, "Blade 2 flapwise velocity [m/s]"),
        (-8.0, 15.0, "Blade 3 flapwise deflection [m]"),
        (-12.0, 12.0, "Blade 3 flapwise velocity [m/s]"),
        (-1.50, 2.50, "Tower FA displacement [m]"),
        (-2.0, 2.0, "Tower FA velocity [m/s]"),
        (-1.20, 1.20, "Tower SS displacement [m]"),
        (-1.50, 1.50, "Tower SS velocity [m/s]"),
        (-0.35, 0.35, "Nacelle yaw error [rad]"),
        (-0.15, 0.15, "Platform pitch tilt [rad]"),
        (-0.10, 0.10, "Platform pitch angular rate [rad/s]")
    ]
    for i, (xmin_v, xmax_v, c) in enumerate(x_bounds, 1):
        lines.append(f"    vecX_min[{i}] := {xmin_v:.2f}; vecX_max[{i}] := {xmax_v:.2f}; (* {c} *)")

    lines.append("""
    bMatricesInitialized := TRUE;
END_IF;
""")
    return "\n".join(lines)

def generate_phase1():
    return """(* ======================================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY AUDITING
   Deterministic verification across 6 mission-critical feedback triads with bumpless 1oo2 fail-operational fallback
   ====================================================================================================================== *)

(* Triad 1: Low-Speed Rotor Shaft Speed Optical Pulse Encoders *)
IF (ABS(rRotorSpeed_EncA_rpm - rRotorSpeed_EncB_rpm) <= 0.250) AND
   (ABS(rRotorSpeed_EncB_rpm - rRotorSpeed_EncC_rpm) <= 0.250) AND
   (ABS(rRotorSpeed_EncC_rpm - rRotorSpeed_EncA_rpm) <= 0.250) THEN
    (* Full 3-channel healthy consensus: Median value selection *)
    IF ((rRotorSpeed_EncA_rpm >= rRotorSpeed_EncB_rpm) AND (rRotorSpeed_EncA_rpm <= rRotorSpeed_EncC_rpm)) OR
       ((rRotorSpeed_EncA_rpm <= rRotorSpeed_EncB_rpm) AND (rRotorSpeed_EncA_rpm >= rRotorSpeed_EncC_rpm)) THEN
        rVoted_RotorSpeed_rpm := rRotorSpeed_EncA_rpm;
    ELSIF ((rRotorSpeed_EncB_rpm >= rRotorSpeed_EncA_rpm) AND (rRotorSpeed_EncB_rpm <= rRotorSpeed_EncC_rpm)) OR
          ((rRotorSpeed_EncB_rpm <= rRotorSpeed_EncA_rpm) AND (rRotorSpeed_EncB_rpm >= rRotorSpeed_EncC_rpm)) THEN
        rVoted_RotorSpeed_rpm := rRotorSpeed_EncB_rpm;
    ELSE
        rVoted_RotorSpeed_rpm := rRotorSpeed_EncC_rpm;
    END_IF;
    bDegraded_RotorSpeed := FALSE;
    tDiscrepancy_RotorSpeed(IN := FALSE);
ELSIF (ABS(rRotorSpeed_EncA_rpm - rRotorSpeed_EncB_rpm) <= 0.250) THEN
    (* Channel C drifted: 1oo2 degraded operation with A and B *)
    rVoted_RotorSpeed_rpm := (rRotorSpeed_EncA_rpm + rRotorSpeed_EncB_rpm) * 0.50;
    bDegraded_RotorSpeed := TRUE;
    tDiscrepancy_RotorSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_RotorSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000001;
    END_IF;
ELSIF (ABS(rRotorSpeed_EncB_rpm - rRotorSpeed_EncC_rpm) <= 0.250) THEN
    (* Channel A drifted: 1oo2 degraded operation with B and C *)
    rVoted_RotorSpeed_rpm := (rRotorSpeed_EncB_rpm + rRotorSpeed_EncC_rpm) * 0.50;
    bDegraded_RotorSpeed := TRUE;
    tDiscrepancy_RotorSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_RotorSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000002;
    END_IF;
ELSIF (ABS(rRotorSpeed_EncC_rpm - rRotorSpeed_EncA_rpm) <= 0.250) THEN
    (* Channel B drifted: 1oo2 degraded operation with C and A *)
    rVoted_RotorSpeed_rpm := (rRotorSpeed_EncC_rpm + rRotorSpeed_EncA_rpm) * 0.50;
    bDegraded_RotorSpeed := TRUE;
    tDiscrepancy_RotorSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_RotorSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000004;
    END_IF;
ELSE
    (* Total 2oo3 voting collapse: All channels mutually discordant *)
    rVoted_RotorSpeed_rpm := (rRotorSpeed_EncA_rpm + rRotorSpeed_EncB_rpm + rRotorSpeed_EncC_rpm) / 3.0;
    bDegraded_RotorSpeed := TRUE;
    tDiscrepancy_RotorSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_RotorSpeed.Q THEN
        bTurbineTripped := TRUE;
        dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000001;
    END_IF;
END_IF;

(* Triad 2: Direct-Drive PMSG Generator Speed Encoders *)
IF (ABS(rGenSpeed_EncA_rpm - rGenSpeed_EncB_rpm) <= 0.250) AND
   (ABS(rGenSpeed_EncB_rpm - rGenSpeed_EncC_rpm) <= 0.250) AND
   (ABS(rGenSpeed_EncC_rpm - rGenSpeed_EncA_rpm) <= 0.250) THEN
    IF ((rGenSpeed_EncA_rpm >= rGenSpeed_EncB_rpm) AND (rGenSpeed_EncA_rpm <= rGenSpeed_EncC_rpm)) OR
       ((rGenSpeed_EncA_rpm <= rGenSpeed_EncB_rpm) AND (rGenSpeed_EncA_rpm >= rGenSpeed_EncC_rpm)) THEN
        rVoted_GenSpeed_rpm := rGenSpeed_EncA_rpm;
    ELSIF ((rGenSpeed_EncB_rpm >= rGenSpeed_EncA_rpm) AND (rGenSpeed_EncB_rpm <= rGenSpeed_EncC_rpm)) OR
          ((rGenSpeed_EncB_rpm <= rGenSpeed_EncA_rpm) AND (rGenSpeed_EncB_rpm >= rGenSpeed_EncC_rpm)) THEN
        rVoted_GenSpeed_rpm := rGenSpeed_EncB_rpm;
    ELSE
        rVoted_GenSpeed_rpm := rGenSpeed_EncC_rpm;
    END_IF;
    bDegraded_GenSpeed := FALSE;
    tDiscrepancy_GenSpeed(IN := FALSE);
ELSIF (ABS(rGenSpeed_EncA_rpm - rGenSpeed_EncB_rpm) <= 0.250) THEN
    rVoted_GenSpeed_rpm := (rGenSpeed_EncA_rpm + rGenSpeed_EncB_rpm) * 0.50;
    bDegraded_GenSpeed := TRUE;
    tDiscrepancy_GenSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_GenSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000008;
    END_IF;
ELSIF (ABS(rGenSpeed_EncB_rpm - rGenSpeed_EncC_rpm) <= 0.250) THEN
    rVoted_GenSpeed_rpm := (rGenSpeed_EncB_rpm + rGenSpeed_EncC_rpm) * 0.50;
    bDegraded_GenSpeed := TRUE;
    tDiscrepancy_GenSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_GenSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000010;
    END_IF;
ELSIF (ABS(rGenSpeed_EncC_rpm - rGenSpeed_EncA_rpm) <= 0.250) THEN
    rVoted_GenSpeed_rpm := (rGenSpeed_EncC_rpm + rGenSpeed_EncA_rpm) * 0.50;
    bDegraded_GenSpeed := TRUE;
    tDiscrepancy_GenSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_GenSpeed.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000020;
    END_IF;
ELSE
    rVoted_GenSpeed_rpm := (rGenSpeed_EncA_rpm + rGenSpeed_EncB_rpm + rGenSpeed_EncC_rpm) / 3.0;
    bDegraded_GenSpeed := TRUE;
    tDiscrepancy_GenSpeed(IN := TRUE, PT := T#200MS);
    IF tDiscrepancy_GenSpeed.Q THEN
        bTurbineTripped := TRUE;
        dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000002;
    END_IF;
END_IF;

(* Triad 3: Forward-Looking Nacelle Doppler LiDAR Inflow Velocity Preview Channels *)
IF (ABS(rLiDAR_WindSpeed_ChA_mps - rLiDAR_WindSpeed_ChB_mps) <= 1.200) AND
   (ABS(rLiDAR_WindSpeed_ChB_mps - rLiDAR_WindSpeed_ChC_mps) <= 1.200) AND
   (ABS(rLiDAR_WindSpeed_ChC_mps - rLiDAR_WindSpeed_ChA_mps) <= 1.200) THEN
    IF ((rLiDAR_WindSpeed_ChA_mps >= rLiDAR_WindSpeed_ChB_mps) AND (rLiDAR_WindSpeed_ChA_mps <= rLiDAR_WindSpeed_ChC_mps)) OR
       ((rLiDAR_WindSpeed_ChA_mps <= rLiDAR_WindSpeed_ChB_mps) AND (rLiDAR_WindSpeed_ChA_mps >= rLiDAR_WindSpeed_ChC_mps)) THEN
        rVoted_LiDAR_WindSpeed_mps := rLiDAR_WindSpeed_ChA_mps;
    ELSIF ((rLiDAR_WindSpeed_ChB_mps >= rLiDAR_WindSpeed_ChA_mps) AND (rLiDAR_WindSpeed_ChB_mps <= rLiDAR_WindSpeed_ChC_mps)) OR
          ((rLiDAR_WindSpeed_ChB_mps <= rLiDAR_WindSpeed_ChA_mps) AND (rLiDAR_WindSpeed_ChB_mps >= rLiDAR_WindSpeed_ChC_mps)) THEN
        rVoted_LiDAR_WindSpeed_mps := rLiDAR_WindSpeed_ChB_mps;
    ELSE
        rVoted_LiDAR_WindSpeed_mps := rLiDAR_WindSpeed_ChC_mps;
    END_IF;
    bDegraded_LiDAR := FALSE;
    tDiscrepancy_LiDAR(IN := FALSE);
ELSIF (ABS(rLiDAR_WindSpeed_ChA_mps - rLiDAR_WindSpeed_ChB_mps) <= 1.200) THEN
    rVoted_LiDAR_WindSpeed_mps := (rLiDAR_WindSpeed_ChA_mps + rLiDAR_WindSpeed_ChB_mps) * 0.50;
    bDegraded_LiDAR := TRUE;
    tDiscrepancy_LiDAR(IN := TRUE, PT := T#500MS);
    IF tDiscrepancy_LiDAR.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000040;
    END_IF;
ELSIF (ABS(rLiDAR_WindSpeed_ChB_mps - rLiDAR_WindSpeed_ChC_mps) <= 1.200) THEN
    rVoted_LiDAR_WindSpeed_mps := (rLiDAR_WindSpeed_ChB_mps + rLiDAR_WindSpeed_ChC_mps) * 0.50;
    bDegraded_LiDAR := TRUE;
    tDiscrepancy_LiDAR(IN := TRUE, PT := T#500MS);
    IF tDiscrepancy_LiDAR.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000080;
    END_IF;
ELSIF (ABS(rLiDAR_WindSpeed_ChC_mps - rLiDAR_WindSpeed_ChA_mps) <= 1.200) THEN
    rVoted_LiDAR_WindSpeed_mps := (rLiDAR_WindSpeed_ChC_mps + rLiDAR_WindSpeed_ChA_mps) * 0.50;
    bDegraded_LiDAR := TRUE;
    tDiscrepancy_LiDAR(IN := TRUE, PT := T#500MS);
    IF tDiscrepancy_LiDAR.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000100;
    END_IF;
ELSE
    (* LiDAR voting fault: Fall back to nacelle ultrasonic anemometer without tripping *)
    rVoted_LiDAR_WindSpeed_mps := rWindSpeed_Sonic_mps;
    bDegraded_LiDAR := TRUE;
    tDiscrepancy_LiDAR(IN := TRUE, PT := T#500MS);
    IF tDiscrepancy_LiDAR.Q THEN
        dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000001;
    END_IF;
END_IF;

(* Triad 4: Tower Top Fore-Aft Seismic Accelerometers *)
IF (ABS(rTowerAcc_FA_ChA_mps2 - rTowerAcc_FA_ChB_mps2) <= 0.150) AND
   (ABS(rTowerAcc_FA_ChB_mps2 - rTowerAcc_FA_ChC_mps2) <= 0.150) AND
   (ABS(rTowerAcc_FA_ChC_mps2 - rTowerAcc_FA_ChA_mps2) <= 0.150) THEN
    IF ((rTowerAcc_FA_ChA_mps2 >= rTowerAcc_FA_ChB_mps2) AND (rTowerAcc_FA_ChA_mps2 <= rTowerAcc_FA_ChC_mps2)) OR
       ((rTowerAcc_FA_ChA_mps2 <= rTowerAcc_FA_ChB_mps2) AND (rTowerAcc_FA_ChA_mps2 >= rTowerAcc_FA_ChC_mps2)) THEN
        rVoted_TowerAcc_FA_mps2 := rTowerAcc_FA_ChA_mps2;
    ELSIF ((rTowerAcc_FA_ChB_mps2 >= rTowerAcc_FA_ChA_mps2) AND (rTowerAcc_FA_ChB_mps2 <= rTowerAcc_FA_ChC_mps2)) OR
          ((rTowerAcc_FA_ChB_mps2 <= rTowerAcc_FA_ChA_mps2) AND (rTowerAcc_FA_ChB_mps2 >= rTowerAcc_FA_ChC_mps2)) THEN
        rVoted_TowerAcc_FA_mps2 := rTowerAcc_FA_ChB_mps2;
    ELSE
        rVoted_TowerAcc_FA_mps2 := rTowerAcc_FA_ChC_mps2;
    END_IF;
    bDegraded_TowerAccFA := FALSE;
    tDiscrepancy_TowerAccFA(IN := FALSE);
ELSIF (ABS(rTowerAcc_FA_ChA_mps2 - rTowerAcc_FA_ChB_mps2) <= 0.150) THEN
    rVoted_TowerAcc_FA_mps2 := (rTowerAcc_FA_ChA_mps2 + rTowerAcc_FA_ChB_mps2) * 0.50;
    bDegraded_TowerAccFA := TRUE;
    tDiscrepancy_TowerAccFA(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccFA.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000200;
    END_IF;
ELSIF (ABS(rTowerAcc_FA_ChB_mps2 - rTowerAcc_FA_ChC_mps2) <= 0.150) THEN
    rVoted_TowerAcc_FA_mps2 := (rTowerAcc_FA_ChB_mps2 + rTowerAcc_FA_ChC_mps2) * 0.50;
    bDegraded_TowerAccFA := TRUE;
    tDiscrepancy_TowerAccFA(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccFA.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000400;
    END_IF;
ELSIF (ABS(rTowerAcc_FA_ChC_mps2 - rTowerAcc_FA_ChA_mps2) <= 0.150) THEN
    rVoted_TowerAcc_FA_mps2 := (rTowerAcc_FA_ChC_mps2 + rTowerAcc_FA_ChA_mps2) * 0.50;
    bDegraded_TowerAccFA := TRUE;
    tDiscrepancy_TowerAccFA(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccFA.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00000800;
    END_IF;
ELSE
    rVoted_TowerAcc_FA_mps2 := (rTowerAcc_FA_ChA_mps2 + rTowerAcc_FA_ChB_mps2 + rTowerAcc_FA_ChC_mps2) / 3.0;
    bDegraded_TowerAccFA := TRUE;
    tDiscrepancy_TowerAccFA(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccFA.Q THEN
        bTurbineTripped := TRUE;
        dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000004;
    END_IF;
END_IF;

(* Triad 5: Tower Top Side-to-Side Seismic Accelerometers *)
IF (ABS(rTowerAcc_SS_ChA_mps2 - rTowerAcc_SS_ChB_mps2) <= 0.150) AND
   (ABS(rTowerAcc_SS_ChB_mps2 - rTowerAcc_SS_ChC_mps2) <= 0.150) AND
   (ABS(rTowerAcc_SS_ChC_mps2 - rTowerAcc_SS_ChA_mps2) <= 0.150) THEN
    IF ((rTowerAcc_SS_ChA_mps2 >= rTowerAcc_SS_ChB_mps2) AND (rTowerAcc_SS_ChA_mps2 <= rTowerAcc_SS_ChC_mps2)) OR
       ((rTowerAcc_SS_ChA_mps2 <= rTowerAcc_SS_ChB_mps2) AND (rTowerAcc_SS_ChA_mps2 >= rTowerAcc_SS_ChC_mps2)) THEN
        rVoted_TowerAcc_SS_mps2 := rTowerAcc_SS_ChA_mps2;
    ELSIF ((rTowerAcc_SS_ChB_mps2 >= rTowerAcc_SS_ChA_mps2) AND (rTowerAcc_SS_ChB_mps2 <= rTowerAcc_SS_ChC_mps2)) OR
          ((rTowerAcc_SS_ChB_mps2 <= rTowerAcc_SS_ChA_mps2) AND (rTowerAcc_SS_ChB_mps2 >= rTowerAcc_SS_ChC_mps2)) THEN
        rVoted_TowerAcc_SS_mps2 := rTowerAcc_SS_ChB_mps2;
    ELSE
        rVoted_TowerAcc_SS_mps2 := rTowerAcc_SS_ChC_mps2;
    END_IF;
    bDegraded_TowerAccSS := FALSE;
    tDiscrepancy_TowerAccSS(IN := FALSE);
ELSIF (ABS(rTowerAcc_SS_ChA_mps2 - rTowerAcc_SS_ChB_mps2) <= 0.150) THEN
    rVoted_TowerAcc_SS_mps2 := (rTowerAcc_SS_ChA_mps2 + rTowerAcc_SS_ChB_mps2) * 0.50;
    bDegraded_TowerAccSS := TRUE;
    tDiscrepancy_TowerAccSS(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccSS.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00001000;
    END_IF;
ELSIF (ABS(rTowerAcc_SS_ChB_mps2 - rTowerAcc_SS_ChC_mps2) <= 0.150) THEN
    rVoted_TowerAcc_SS_mps2 := (rTowerAcc_SS_ChB_mps2 + rTowerAcc_SS_ChC_mps2) * 0.50;
    bDegraded_TowerAccSS := TRUE;
    tDiscrepancy_TowerAccSS(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccSS.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00002000;
    END_IF;
ELSIF (ABS(rTowerAcc_SS_ChC_mps2 - rTowerAcc_SS_ChA_mps2) <= 0.150) THEN
    rVoted_TowerAcc_SS_mps2 := (rTowerAcc_SS_ChC_mps2 + rTowerAcc_SS_ChA_mps2) * 0.50;
    bDegraded_TowerAccSS := TRUE;
    tDiscrepancy_TowerAccSS(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccSS.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00004000;
    END_IF;
ELSE
    rVoted_TowerAcc_SS_mps2 := (rTowerAcc_SS_ChA_mps2 + rTowerAcc_SS_ChB_mps2 + rTowerAcc_SS_ChC_mps2) / 3.0;
    bDegraded_TowerAccSS := TRUE;
    tDiscrepancy_TowerAccSS(IN := TRUE, PT := T#150MS);
    IF tDiscrepancy_TowerAccSS.Q THEN
        bTurbineTripped := TRUE;
        dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000008;
    END_IF;
END_IF;

(* Triad 6: Blade 1 Root Optical FBG Flapwise Strain Sensors *)
IF (ABS(rStrain_Flap_B1_ChA_ue - rStrain_Flap_B1_ChB_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B1_ChB_ue - rStrain_Flap_B1_ChC_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B1_ChC_ue - rStrain_Flap_B1_ChA_ue) <= 85.0) THEN
    IF ((rStrain_Flap_B1_ChA_ue >= rStrain_Flap_B1_ChB_ue) AND (rStrain_Flap_B1_ChA_ue <= rStrain_Flap_B1_ChC_ue)) OR
       ((rStrain_Flap_B1_ChA_ue <= rStrain_Flap_B1_ChB_ue) AND (rStrain_Flap_B1_ChA_ue >= rStrain_Flap_B1_ChC_ue)) THEN
        rVoted_Strain_Flap_B1_ue := rStrain_Flap_B1_ChA_ue;
    ELSIF ((rStrain_Flap_B1_ChB_ue >= rStrain_Flap_B1_ChA_ue) AND (rStrain_Flap_B1_ChB_ue <= rStrain_Flap_B1_ChC_ue)) OR
          ((rStrain_Flap_B1_ChB_ue <= rStrain_Flap_B1_ChA_ue) AND (rStrain_Flap_B1_ChB_ue >= rStrain_Flap_B1_ChC_ue)) THEN
        rVoted_Strain_Flap_B1_ue := rStrain_Flap_B1_ChB_ue;
    ELSE
        rVoted_Strain_Flap_B1_ue := rStrain_Flap_B1_ChC_ue;
    END_IF;
    bDegraded_StrainB1 := FALSE;
    tDiscrepancy_StrainB1(IN := FALSE);
ELSIF (ABS(rStrain_Flap_B1_ChA_ue - rStrain_Flap_B1_ChB_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B1_ue := (rStrain_Flap_B1_ChA_ue + rStrain_Flap_B1_ChB_ue) * 0.50;
    bDegraded_StrainB1 := TRUE;
    tDiscrepancy_StrainB1(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB1.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00008000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B1_ChB_ue - rStrain_Flap_B1_ChC_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B1_ue := (rStrain_Flap_B1_ChB_ue + rStrain_Flap_B1_ChC_ue) * 0.50;
    bDegraded_StrainB1 := TRUE;
    tDiscrepancy_StrainB1(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB1.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00010000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B1_ChC_ue - rStrain_Flap_B1_ChA_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B1_ue := (rStrain_Flap_B1_ChC_ue + rStrain_Flap_B1_ChA_ue) * 0.50;
    bDegraded_StrainB1 := TRUE;
    tDiscrepancy_StrainB1(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB1.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00020000;
    END_IF;
ELSE
    rVoted_Strain_Flap_B1_ue := (rStrain_Flap_B1_ChA_ue + rStrain_Flap_B1_ChB_ue + rStrain_Flap_B1_ChC_ue) / 3.0;
    bDegraded_StrainB1 := TRUE;
    tDiscrepancy_StrainB1(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB1.Q THEN
        dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000002;
    END_IF;
END_IF;

(* Blade 2 Root Optical FBG Flapwise Strain Sensors *)
IF (ABS(rStrain_Flap_B2_ChA_ue - rStrain_Flap_B2_ChB_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B2_ChB_ue - rStrain_Flap_B2_ChC_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B2_ChC_ue - rStrain_Flap_B2_ChA_ue) <= 85.0) THEN
    IF ((rStrain_Flap_B2_ChA_ue >= rStrain_Flap_B2_ChB_ue) AND (rStrain_Flap_B2_ChA_ue <= rStrain_Flap_B2_ChC_ue)) OR
       ((rStrain_Flap_B2_ChA_ue <= rStrain_Flap_B2_ChB_ue) AND (rStrain_Flap_B2_ChA_ue >= rStrain_Flap_B2_ChC_ue)) THEN
        rVoted_Strain_Flap_B2_ue := rStrain_Flap_B2_ChA_ue;
    ELSIF ((rStrain_Flap_B2_ChB_ue >= rStrain_Flap_B2_ChA_ue) AND (rStrain_Flap_B2_ChB_ue <= rStrain_Flap_B2_ChC_ue)) OR
          ((rStrain_Flap_B2_ChB_ue <= rStrain_Flap_B2_ChA_ue) AND (rStrain_Flap_B2_ChB_ue >= rStrain_Flap_B2_ChC_ue)) THEN
        rVoted_Strain_Flap_B2_ue := rStrain_Flap_B2_ChB_ue;
    ELSE
        rVoted_Strain_Flap_B2_ue := rStrain_Flap_B2_ChC_ue;
    END_IF;
    bDegraded_StrainB2 := FALSE;
    tDiscrepancy_StrainB2(IN := FALSE);
ELSIF (ABS(rStrain_Flap_B2_ChA_ue - rStrain_Flap_B2_ChB_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B2_ue := (rStrain_Flap_B2_ChA_ue + rStrain_Flap_B2_ChB_ue) * 0.50;
    bDegraded_StrainB2 := TRUE;
    tDiscrepancy_StrainB2(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB2.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00040000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B2_ChB_ue - rStrain_Flap_B2_ChC_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B2_ue := (rStrain_Flap_B2_ChB_ue + rStrain_Flap_B2_ChC_ue) * 0.50;
    bDegraded_StrainB2 := TRUE;
    tDiscrepancy_StrainB2(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB2.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00080000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B2_ChC_ue - rStrain_Flap_B2_ChA_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B2_ue := (rStrain_Flap_B2_ChC_ue + rStrain_Flap_B2_ChA_ue) * 0.50;
    bDegraded_StrainB2 := TRUE;
    tDiscrepancy_StrainB2(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB2.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00100000;
    END_IF;
ELSE
    rVoted_Strain_Flap_B2_ue := (rStrain_Flap_B2_ChA_ue + rStrain_Flap_B2_ChB_ue + rStrain_Flap_B2_ChC_ue) / 3.0;
    bDegraded_StrainB2 := TRUE;
    tDiscrepancy_StrainB2(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB2.Q THEN
        dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000004;
    END_IF;
END_IF;

(* Blade 3 Root Optical FBG Flapwise Strain Sensors *)
IF (ABS(rStrain_Flap_B3_ChA_ue - rStrain_Flap_B3_ChB_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B3_ChB_ue - rStrain_Flap_B3_ChC_ue) <= 85.0) AND
   (ABS(rStrain_Flap_B3_ChC_ue - rStrain_Flap_B3_ChA_ue) <= 85.0) THEN
    IF ((rStrain_Flap_B3_ChA_ue >= rStrain_Flap_B3_ChB_ue) AND (rStrain_Flap_B3_ChA_ue <= rStrain_Flap_B3_ChC_ue)) OR
       ((rStrain_Flap_B3_ChA_ue <= rStrain_Flap_B3_ChB_ue) AND (rStrain_Flap_B3_ChA_ue >= rStrain_Flap_B3_ChC_ue)) THEN
        rVoted_Strain_Flap_B3_ue := rStrain_Flap_B3_ChA_ue;
    ELSIF ((rStrain_Flap_B3_ChB_ue >= rStrain_Flap_B3_ChA_ue) AND (rStrain_Flap_B3_ChB_ue <= rStrain_Flap_B3_ChC_ue)) OR
          ((rStrain_Flap_B3_ChB_ue <= rStrain_Flap_B3_ChA_ue) AND (rStrain_Flap_B3_ChB_ue >= rStrain_Flap_B3_ChC_ue)) THEN
        rVoted_Strain_Flap_B3_ue := rStrain_Flap_B3_ChB_ue;
    ELSE
        rVoted_Strain_Flap_B3_ue := rStrain_Flap_B3_ChC_ue;
    END_IF;
    bDegraded_StrainB3 := FALSE;
    tDiscrepancy_StrainB3(IN := FALSE);
ELSIF (ABS(rStrain_Flap_B3_ChA_ue - rStrain_Flap_B3_ChB_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B3_ue := (rStrain_Flap_B3_ChA_ue + rStrain_Flap_B3_ChB_ue) * 0.50;
    bDegraded_StrainB3 := TRUE;
    tDiscrepancy_StrainB3(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB3.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00200000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B3_ChB_ue - rStrain_Flap_B3_ChC_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B3_ue := (rStrain_Flap_B3_ChB_ue + rStrain_Flap_B3_ChC_ue) * 0.50;
    bDegraded_StrainB3 := TRUE;
    tDiscrepancy_StrainB3(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB3.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00400000;
    END_IF;
ELSIF (ABS(rStrain_Flap_B3_ChC_ue - rStrain_Flap_B3_ChA_ue) <= 85.0) THEN
    rVoted_Strain_Flap_B3_ue := (rStrain_Flap_B3_ChC_ue + rStrain_Flap_B3_ChA_ue) * 0.50;
    bDegraded_StrainB3 := TRUE;
    tDiscrepancy_StrainB3(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB3.Q THEN
        dwSensorDegradedMask := dwSensorDegradedMask OR 16#00800000;
    END_IF;
ELSE
    rVoted_Strain_Flap_B3_ue := (rStrain_Flap_B3_ChA_ue + rStrain_Flap_B3_ChB_ue + rStrain_Flap_B3_ChC_ue) / 3.0;
    bDegraded_StrainB3 := TRUE;
    tDiscrepancy_StrainB3(IN := TRUE, PT := T#250MS);
    IF tDiscrepancy_StrainB3.Q THEN
        dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000008;
    END_IF;
END_IF;
"""

print("Phase 0 and Phase 1 ready.")

def generate_phase2():
    return """(* ======================================================================================================================
   PHASE 2: ACTIVE OFFSHORE SUBSTRUCTURE / TOWER RESONANCE DAMPING
   Active damping of 1st tower fore-aft (0.22 Hz) and side-to-side (0.21 Hz) hydrodynamic wave excitation modes
   ====================================================================================================================== *)

(* Discrete 2nd-order state-variable bandpass filter for fore-aft acceleration *)
rTower_FA_FilterState1 := rTower_FA_FilterState1 + (0.050 * rTower_FA_FilterState2);
rTower_FA_FilterState2 := rTower_FA_FilterState2 + 0.050 * (rVoted_TowerAcc_FA_mps2 -
                         (2.0 * rTower_Zeta_FA * rTower_Omega_FA * rTower_FA_FilterState2) -
                         (rTower_Omega_FA * rTower_Omega_FA * rTower_FA_FilterState1));
rTowerTopVelocity_FA_mps := rTower_FA_FilterState1;

(* Fore-aft collective pitch trimming offset for aerodynamic thrust modulation *)
IF (iOperatingFSMState = 6) OR (iOperatingFSMState = 7) OR (iOperatingFSMState = 8) THEN
    rPitchOffset_TowerFA_deg := -1.0 * rGain_TowerDamping_FA * rTowerTopVelocity_FA_mps;
    IF rPitchOffset_TowerFA_deg > 1.50 THEN
        rPitchOffset_TowerFA_deg := 1.50;
    ELSIF rPitchOffset_TowerFA_deg < -1.50 THEN
        rPitchOffset_TowerFA_deg := -1.50;
    END_IF;
ELSE
    rPitchOffset_TowerFA_deg := 0.0;
END_IF;

(* Discrete 2nd-order state-variable bandpass filter for side-to-side acceleration *)
rTower_SS_FilterState1 := rTower_SS_FilterState1 + (0.050 * rTower_SS_FilterState2);
rTower_SS_FilterState2 := rTower_SS_FilterState2 + 0.050 * (rVoted_TowerAcc_SS_mps2 -
                         (2.0 * rTower_Zeta_SS * rTower_Omega_SS * rTower_SS_FilterState2) -
                         (rTower_Omega_SS * rTower_Omega_SS * rTower_SS_FilterState1));
rTowerTopVelocity_SS_mps := rTower_SS_FilterState1;

(* Side-to-side generator electromagnetic reaction counter-torque damping offset *)
IF (iOperatingFSMState = 4) OR (iOperatingFSMState = 5) OR (iOperatingFSMState = 6) OR
   (iOperatingFSMState = 7) OR (iOperatingFSMState = 8) THEN
    rTorqueOffset_TowerSS_kNm := -1.0 * rGain_TowerDamping_SS * rTowerTopVelocity_SS_mps;
    IF rTorqueOffset_TowerSS_kNm > 1200.0 THEN
        rTorqueOffset_TowerSS_kNm := 1200.0;
    ELSIF rTorqueOffset_TowerSS_kNm < -1200.0 THEN
        rTorqueOffset_TowerSS_kNm := -1200.0;
    END_IF;
ELSE
    rTorqueOffset_TowerSS_kNm := 0.0;
END_IF;
"""

def generate_phase3():
    return """(* ======================================================================================================================
   PHASE 3: NACELLE FORWARD-LOOKING PULSED DOPPLER LIDAR PREVIEW & FEED-FORWARD
   Dynamic 50-sample ring buffer tracking upstream inflow velocity and gust acceleration profile (2.50 s horizon)
   ====================================================================================================================== *)

(* Insert current voted LiDAR measurement into circular preview memory *)
aLiDAR_PreviewBuffer[iLiDAR_WriteIdx] := rVoted_LiDAR_WindSpeed_mps;
iLiDAR_WriteIdx := (iLiDAR_WriteIdx + 1) MOD 50;
IF iLiDAR_BufferCount < 50 THEN
    iLiDAR_BufferCount := iLiDAR_BufferCount + 1;
END_IF;

(* Calculate inflow gust front acceleration *)
rLiDAR_Acceleration_mps2 := (rVoted_LiDAR_WindSpeed_mps - rLiDAR_PrevFilteredSpeed) / 0.050;
rLiDAR_PrevFilteredSpeed := (0.90 * rLiDAR_PrevFilteredSpeed) + (0.10 * rVoted_LiDAR_WindSpeed_mps);

(* Calculate dynamic look-ahead transit time based on focal distance and inflow velocity *)
IF rVoted_LiDAR_WindSpeed_mps > 1.50 THEN
    rLiDAR_TargetDelay_s := rLiDAR_FocalDistance_m / rVoted_LiDAR_WindSpeed_mps;
ELSE
    rLiDAR_TargetDelay_s := 2.50;
END_IF;

IF rLiDAR_TargetDelay_s > 2.50 THEN
    rLiDAR_TargetDelay_s := 2.50;
ELSIF rLiDAR_TargetDelay_s < 0.25 THEN
    rLiDAR_TargetDelay_s := 0.25;
END_IF;

iLiDAR_DelaySamples := REAL_TO_INT(rLiDAR_TargetDelay_s / 0.050);
IF iLiDAR_DelaySamples > 49 THEN
    iLiDAR_DelaySamples := 49;
ELSIF iLiDAR_DelaySamples < 1 THEN
    iLiDAR_DelaySamples := 1;
END_IF;

(* Extract synchronized playback preview velocity *)
iLiDAR_ReadIdx := (iLiDAR_WriteIdx - iLiDAR_DelaySamples + 50) MOD 50;
rLiDAR_PreviewWindSpeed_mps := aLiDAR_PreviewBuffer[iLiDAR_ReadIdx];

(* Upstream gust detection logic *)
IF ((rVoted_LiDAR_WindSpeed_mps - rWindSpeed_Filtered_mps) > 2.20) OR (rLiDAR_Acceleration_mps2 > 1.25) THEN
    bLiDAR_GustDetected := TRUE;
ELSE
    bLiDAR_GustDetected := FALSE;
END_IF;

(* Region III Aerodynamic Pitch Feed-Forward Offset Calculation *)
IF bLiDAR_DataValid AND (rLiDAR_PreviewWindSpeed_mps > 10.590) AND
   ((iOperatingFSMState = 6) OR (iOperatingFSMState = 7) OR (iOperatingFSMState = 8)) THEN
    rPitchOffset_LiDAR_FF_deg := rLiDAR_Sensitivity_deg_per_mps * (rLiDAR_PreviewWindSpeed_mps - 10.590);
    IF bLiDAR_GustDetected THEN
        rPitchOffset_LiDAR_FF_deg := rPitchOffset_LiDAR_FF_deg + (rLiDAR_BoostGain * rLiDAR_Acceleration_mps2);
    END_IF;
ELSE
    rPitchOffset_LiDAR_FF_deg := 0.0;
END_IF;

IF rPitchOffset_LiDAR_FF_deg > 12.0 THEN
    rPitchOffset_LiDAR_FF_deg := 12.0;
ELSIF rPitchOffset_LiDAR_FF_deg < 0.0 THEN
    rPitchOffset_LiDAR_FF_deg := 0.0;
END_IF;
"""

def generate_phase4():
    return """(* ======================================================================================================================
   PHASE 4: MULTIBLADE COORDINATE COLEMAN TRANSFORMATION (1P INDIVIDUAL PITCH CONTROL)
   D-Q Axis decomposition of blade root flapwise bending moments to eliminate asymmetric tilt and yaw moments
   ====================================================================================================================== *)

(* Transform mechanical azimuth resolver feedback into radians and calculate blade positions *)
rAzimuth_Rad := rRotorAzimuth_ResA_deg * 0.0174532925;
rPsi_B1 := rAzimuth_Rad;
rPsi_B2 := rAzimuth_Rad + 2.094395102; (* + 120 degrees *)
rPsi_B3 := rAzimuth_Rad + 4.188790205; (* + 240 degrees *)

rCos_B1 := COS(rPsi_B1); rSin_B1 := SIN(rPsi_B1);
rCos_B2 := COS(rPsi_B2); rSin_B2 := SIN(rPsi_B2);
rCos_B3 := COS(rPsi_B3); rSin_B3 := SIN(rPsi_B3);

(* Reconstruct blade root flapwise bending moments from voted FBG strain feedbacks (2.450 kNm / microstrain) *)
rMoment_B1_kNm := rVoted_Strain_Flap_B1_ue * 2.450;
rMoment_B2_kNm := rVoted_Strain_Flap_B2_ue * 2.450;
rMoment_B3_kNm := rVoted_Strain_Flap_B3_ue * 2.450;

(* Forward Coleman Transformation: Rotating blade frame to stationary hub frame (d-axis tilt, q-axis yaw) *)
rTiltMoment_1P_kNm := 0.6666667 * ((rMoment_B1_kNm * rCos_B1) + (rMoment_B2_kNm * rCos_B2) + (rMoment_B3_kNm * rCos_B3));
rYawMoment_1P_kNm  := 0.6666667 * ((rMoment_B1_kNm * rSin_B1) + (rMoment_B2_kNm * rSin_B2) + (rMoment_B3_kNm * rSin_B3));

(* Multiblade D-Q Axis Proportional-Integral Controllers with Anti-Windup Saturation *)
rTilt_Error_kNm := 0.0 - rTiltMoment_1P_kNm;
rYaw_Error_kNm  := 0.0 - rYawMoment_1P_kNm;

IF (iOperatingFSMState = 7) OR (iOperatingFSMState = 6) OR (iOperatingFSMState = 8) THEN
    rIPC_Tilt_Integral := rIPC_Tilt_Integral + (rIPC_Ki * rTilt_Error_kNm * 0.050);
    rIPC_Yaw_Integral  := rIPC_Yaw_Integral  + (rIPC_Ki * rYaw_Error_kNm * 0.050);
    
    IF rIPC_Tilt_Integral > rIPC_MaxOffset_deg THEN
        rIPC_Tilt_Integral := rIPC_MaxOffset_deg;
    ELSIF rIPC_Tilt_Integral < -rIPC_MaxOffset_deg THEN
        rIPC_Tilt_Integral := -rIPC_MaxOffset_deg;
    END_IF;
    
    IF rIPC_Yaw_Integral > rIPC_MaxOffset_deg THEN
        rIPC_Yaw_Integral := rIPC_MaxOffset_deg;
    ELSIF rIPC_Yaw_Integral < -rIPC_MaxOffset_deg THEN
        rIPC_Yaw_Integral := -rIPC_MaxOffset_deg;
    END_IF;
    
    rPitch_d_axis_deg := (rIPC_Kp * rTilt_Error_kNm) + rIPC_Tilt_Integral;
    rPitch_q_axis_deg := (rIPC_Kp * rYaw_Error_kNm)  + rIPC_Yaw_Integral;
    
    IF rPitch_d_axis_deg > rIPC_MaxOffset_deg THEN
        rPitch_d_axis_deg := rIPC_MaxOffset_deg;
    ELSIF rPitch_d_axis_deg < -rIPC_MaxOffset_deg THEN
        rPitch_d_axis_deg := -rIPC_MaxOffset_deg;
    END_IF;
    
    IF rPitch_q_axis_deg > rIPC_MaxOffset_deg THEN
        rPitch_q_axis_deg := rIPC_MaxOffset_deg;
    ELSIF rPitch_q_axis_deg < -rIPC_MaxOffset_deg THEN
        rPitch_q_axis_deg := -rIPC_MaxOffset_deg;
    END_IF;
ELSE
    rIPC_Tilt_Integral := 0.0;
    rIPC_Yaw_Integral  := 0.0;
    rPitch_d_axis_deg  := 0.0;
    rPitch_q_axis_deg  := 0.0;
END_IF;

(* Inverse Coleman Transformation: Stationary d-q coordinates back to rotating blade pitch offsets *)
rPitchOffset_IPC_B1_deg := (rPitch_d_axis_deg * rCos_B1) + (rPitch_q_axis_deg * rSin_B1);
rPitchOffset_IPC_B2_deg := (rPitch_d_axis_deg * rCos_B2) + (rPitch_q_axis_deg * rSin_B2);
rPitchOffset_IPC_B3_deg := (rPitch_d_axis_deg * rCos_B3) + (rPitch_q_axis_deg * rSin_B3);
"""

def generate_phase5():
    return """(* ======================================================================================================================
   PHASE 5: DISCRETE STATE-SPACE PROPAGATION & RECEDING-HORIZON MPC OPTIMIZATION
   Execution of state observer update x[k+1] = A*x[k] + B*u[k] and 5-step receding-horizon projected gradient descent
   ====================================================================================================================== *)

(* Populate current plant control input vector u[k] *)
vecU[1] := rGenTorque_Cmd_kNm;
vecU[2] := rPitchCmd_Blade1_deg;
vecU[3] := rPitchCmd_Blade2_deg;
vecU[4] := rPitchCmd_Blade3_deg;
vecU[5] := rYawMotorTorque_Cmd_kNm;
vecU[6] := rVoted_LiDAR_WindSpeed_mps;
vecU[7] := rLiDAR_ShearExponent_alpha;
vecU[8] := 0.0; (* Hydrodynamic wave excitation pitching moment *)

(* Construct current state observation vector x[k] from redundant sensor outputs *)
vecX[1]  := (rVoted_RotorSpeed_rpm - rRatedRotorSpeed_rpm) * 0.104719755;
vecX[2]  := (rVoted_GenSpeed_rpm - rRatedRotorSpeed_rpm) * 0.104719755;
vecX[3]  := vecX[1] - vecX[2];
vecX[4]  := rVoted_Strain_Flap_B1_ue * 0.001250;
vecX[5]  := (vecX[4] - vecX_pred[4]) / 0.050;
vecX[6]  := rVoted_Strain_Flap_B2_ue * 0.001250;
vecX[7]  := (vecX[6] - vecX_pred[6]) / 0.050;
vecX[8]  := rVoted_Strain_Flap_B3_ue * 0.001250;
vecX[9]  := (vecX[8] - vecX_pred[8]) / 0.050;
vecX[10] := rTower_FA_FilterState1;
vecX[11] := rTower_FA_FilterState2;
vecX[12] := rTower_SS_FilterState1;
vecX[13] := rTower_SS_FilterState2;
vecX[14] := rYawTrackingError_deg * 0.0174532925;
vecX[15] := rPlatformPitchAngle_deg * 0.0174532925;
vecX[16] := 0.0;

(* Matrix state propagation: x[k+1] = A * x[k] + B * u[k] *)
FOR idx_i := 1 TO 16 DO
    vecX_next[idx_i] := 0.0;
    FOR idx_j := 1 TO 16 DO
        vecX_next[idx_i] := vecX_next[idx_i] + (matA[idx_i, idx_j] * vecX[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 8 DO
        vecX_next[idx_i] := vecX_next[idx_i] + (matB[idx_i, idx_k] * vecU[idx_k]);
    END_FOR;
END_FOR;

(* Matrix output observation: y[k] = C * x[k] + D * u[k] *)
FOR idx_i := 1 TO 8 DO
    vecY[idx_i] := 0.0;
    FOR idx_j := 1 TO 16 DO
        vecY[idx_i] := vecY[idx_i] + (matC[idx_i, idx_j] * vecX[idx_j]);
    END_FOR;
    FOR idx_k := 1 TO 8 DO
        vecY[idx_i] := vecY[idx_i] + (matD[idx_i, idx_k] * vecU[idx_k]);
    END_FOR;
END_FOR;

(* Receding-Horizon Model Predictive Control (MPC) Solver *)
FOR idx_k := 1 TO 8 DO
    vecU_opt[idx_k] := vecU[idx_k];
END_FOR;

FOR iMPC_Iter := 1 TO 8 DO
    FOR idx_i := 1 TO 16 DO
        vecX_pred[idx_i] := vecX[idx_i];
    END_FOR;
    rMPC_CostCurrent := 0.0;
    
    (* Receding horizon 5-stage forward simulation *)
    FOR iHorizonStep := 1 TO 5 DO
        FOR idx_i := 1 TO 16 DO
            vecX_next[idx_i] := 0.0;
            FOR idx_j := 1 TO 16 DO
                vecX_next[idx_i] := vecX_next[idx_i] + (matA[idx_i, idx_j] * vecX_pred[idx_j]);
            END_FOR;
            FOR idx_k := 1 TO 8 DO
                vecX_next[idx_i] := vecX_next[idx_i] + (matB[idx_i, idx_k] * vecU_opt[idx_k]);
            END_FOR;
            vecX_pred[idx_i] := vecX_next[idx_i];
            rMPC_CostCurrent := rMPC_CostCurrent + (vecQ[idx_i] * vecX_pred[idx_i] * vecX_pred[idx_i]);
        END_FOR;
        
        FOR idx_k := 1 TO 8 DO
            rMPC_CostCurrent := rMPC_CostCurrent + (vecR[idx_k] * vecU_opt[idx_k] * vecU_opt[idx_k]);
        END_FOR;
    END_FOR;
    
    (* Terminal state penalty accumulation *)
    FOR idx_i := 1 TO 16 DO
        rMPC_CostCurrent := rMPC_CostCurrent + (vecP[idx_i] * vecX_pred[idx_i] * vecX_pred[idx_i]);
    END_FOR;
    
    (* Compute objective gradient and perform projected descent *)
    FOR idx_k := 1 TO 8 DO
        vecGradient[idx_k] := (2.0 * vecR[idx_k] * vecU_opt[idx_k]);
        FOR idx_i := 1 TO 16 DO
            vecGradient[idx_k] := vecGradient[idx_k] + (2.0 * matB[idx_i, idx_k] * vecQ[idx_i] * vecX_pred[idx_i]);
        END_FOR;
        
        vecU_opt[idx_k] := vecU_opt[idx_k] - (rMPC_StepSize * vecGradient[idx_k]);
        
        (* Enforce physical box saturation boundaries *)
        IF vecU_opt[idx_k] > vecU_max[idx_k] THEN
            vecU_opt[idx_k] := vecU_max[idx_k];
        ELSIF vecU_opt[idx_k] < vecU_min[idx_k] THEN
            vecU_opt[idx_k] := vecU_min[idx_k];
        END_IF;
    END_FOR;
END_FOR;
"""

def generate_phase6():
    return """(* ======================================================================================================================
   PHASE 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
   Comprehensive management of all wind turbine generation states, transition smoothing, and safety interlocks
   ====================================================================================================================== *)

(* Calculate continuous low-pass filtered wind velocity for state transitions *)
rWindSpeed_Filtered_mps := (0.980 * rWindSpeed_Filtered_mps) + (0.020 * rWindSpeed_Sonic_mps);

CASE iOperatingFSMState OF
    0: (* FSM_STANDBY_PARKED: Caliper brake engaged, full aerodynamic feathering 90 deg *)
        bSystemReady                    := FALSE;
        bMainCircuitBreaker_ClosePermit := FALSE;
        bMechanicalLock_Engage          := TRUE;
        rPitchCmd_Collective_deg        := 90.0;
        rGenTorque_Cmd_kNm              := 0.0;
        rActivePower_Cmd_kW             := 0.0;
        rReactivePower_Cmd_kVAR         := 0.0;
        iControlRegion                  := 0;
        
        IF bEnableMaster AND bEmergencyStopDualCh AND NOT bTurbineTripped AND NOT bStormCutOutLatched THEN
            tFSM_StateTimer(IN := TRUE, PT := T#5S);
            IF tFSM_StateTimer.Q THEN
                tFSM_StateTimer(IN := FALSE);
                iOperatingFSMState := 1; (* Proceed to Grid Synchronization Check *)
            END_IF;
        ELSE
            tFSM_StateTimer(IN := FALSE);
        END_IF;

    1: (* FSM_GRID_SYNC_CHECK: Verify 66 kV substation bus voltage and frequency stability *)
        bSystemReady                    := FALSE;
        bMechanicalLock_Engage          := TRUE;
        rPitchCmd_Collective_deg        := 90.0;
        rGenTorque_Cmd_kNm              := 0.0;
        iControlRegion                  := 0;
        
        tFSM_GridSyncTimer(IN := TRUE, PT := T#10S);
        IF (rGridVoltage_kV >= 59.4) AND (rGridVoltage_kV <= 72.6) AND
           (rGridFrequency_Hz >= 49.5) AND (rGridFrequency_Hz <= 50.5) AND
           bGridTiePermissive THEN
            bMainCircuitBreaker_ClosePermit := TRUE;
            tFSM_GridSyncTimer(IN := FALSE);
            iOperatingFSMState := 2; (* Advance to Brake Release & Idling Spin-Up *)
        ELSIF tFSM_GridSyncTimer.Q THEN
            tFSM_GridSyncTimer(IN := FALSE);
            bMainCircuitBreaker_ClosePermit := FALSE;
            dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000010;
            iOperatingFSMState := 0; (* Abort to Standby *)
        END_IF;

    2: (* FSM_BRAKE_RELEASE_SPINUP: Depressurize caliper brake, idle blades to assess free rotation *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        rPitchCmd_Collective_deg        := 82.0; (* Slight aerodynamic idling pitch bias *)
        rGenTorque_Cmd_kNm              := 0.0;
        iControlRegion                  := 1;
        
        tFSM_SpinUpTimer(IN := TRUE, PT := T#45S);
        IF (rWindSpeed_Filtered_mps >= 3.00) AND (rVoted_RotorSpeed_rpm >= 1.20) THEN
            tFSM_SpinUpTimer(IN := FALSE);
            iOperatingFSMState := 3; (* Enter Region 1 Cut-In Ramp *)
        ELSIF (rWindSpeed_Filtered_mps < 2.50) OR tFSM_SpinUpTimer.Q THEN
            tFSM_SpinUpTimer(IN := FALSE);
            iOperatingFSMState := 0; (* Insufficient wind or timeout, return to standby *)
        END_IF;

    3: (* FSM_REGION_1_CUTIN_RAMP: Controlled ramp from feathered position to 0 deg fine pitch *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        iControlRegion                  := 1;
        
        (* Pitch ramp rate of 1.5 deg/s *)
        IF rPitchCmd_Collective_deg > 0.0 THEN
            rPitchCmd_Collective_deg := rPitchCmd_Collective_deg - (1.50 * 0.050);
            IF rPitchCmd_Collective_deg < 0.0 THEN
                rPitchCmd_Collective_deg := 0.0;
            END_IF;
        END_IF;
        
        rGenTorque_Cmd_kNm := 500.0; (* Initial gentle electrical excitation torque *)
        
        IF (rVoted_RotorSpeed_rpm >= 3.50) AND (rPitchCmd_Collective_deg <= 2.0) THEN
            iOperatingFSMState := 4; (* Enter Region 2 Maximum Cp Tracking *)
        ELSIF rWindSpeed_Filtered_mps < 2.80 THEN
            iOperatingFSMState := 2; (* Spin-down fallback *)
        END_IF;

    4: (* FSM_REGION_2_CP_MAX_TRACK: Partial load optimal aerodynamic torque tracking K_opt * Omega^2 *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        rPitchCmd_Collective_deg        := 0.0; (* Optimal 0.0 deg fine pitch benchmark *)
        iControlRegion                  := 2;
        
        rRotorSpeed_radps := rVoted_RotorSpeed_rpm * 0.104719755;
        rTorque_Opt_kNm := rK_opt * rRotorSpeed_radps * rRotorSpeed_radps;
        
        IF rTorque_Opt_kNm > rRatedTorque_kNm THEN
            rTorque_Opt_kNm := rRatedTorque_kNm;
        END_IF;
        rGenTorque_Cmd_kNm := rTorque_Opt_kNm;
        
        IF (rVoted_RotorSpeed_rpm >= 7.20) OR (rWindSpeed_Filtered_mps >= 10.20) THEN
            iOperatingFSMState := 5; (* Transition to Region 2.5 *)
        ELSIF rWindSpeed_Filtered_mps < 2.70 THEN
            iOperatingFSMState := 3; (* Return to cut-in *)
        END_IF;

    5: (* FSM_REGION_2_5_TRANSITION: Knee-point smoothing between torque control and pitch regulation *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        iControlRegion                  := 25;
        
        (* Smooth torque approach to rated 19,878 kNm *)
        rRotorSpeed_radps := rVoted_RotorSpeed_rpm * 0.104719755;
        rTorque_Opt_kNm := rRatedTorque_kNm * (rVoted_RotorSpeed_rpm / rRatedRotorSpeed_rpm);
        IF rTorque_Opt_kNm > rRatedTorque_kNm THEN
            rTorque_Opt_kNm := rRatedTorque_kNm;
        END_IF;
        rGenTorque_Cmd_kNm := rTorque_Opt_kNm;
        
        (* Initiate minor collective pitch shedding if speed approaches 7.55 rpm *)
        IF rVoted_RotorSpeed_rpm >= rRatedRotorSpeed_rpm THEN
            rPitch_Integral_deg := 0.20;
            iOperatingFSMState := 6; (* Enter Region 3 Rated Pitch Regulation *)
        ELSIF rVoted_RotorSpeed_rpm < 6.80 THEN
            iOperatingFSMState := 4; (* Return to Region 2 *)
        END_IF;

    6: (* FSM_REGION_3_RATED_REGULATION: Constant 15 MW full power regulation via collective pitch PI *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        rGenTorque_Cmd_kNm              := rRatedTorque_kNm;
        iControlRegion                  := 3;
        
        rSpeed_Error_rpm := rVoted_RotorSpeed_rpm - rRatedRotorSpeed_rpm;
        rPitch_Integral_deg := rPitch_Integral_deg + (rPitch_Ki * rSpeed_Error_rpm * 0.050);
        
        IF rPitch_Integral_deg > 35.0 THEN
            rPitch_Integral_deg := 35.0;
        ELSIF rPitch_Integral_deg < 0.0 THEN
            rPitch_Integral_deg := 0.0;
        END_IF;
        
        rPitchCmd_Collective_deg := (rPitch_Kp * rSpeed_Error_rpm) + rPitch_Integral_deg;
        IF rPitchCmd_Collective_deg < 0.0 THEN
            rPitchCmd_Collective_deg := 0.0;
        END_IF;
        
        (* Evaluate branching into active IPC load mitigation or LiDAR gust feed-forward *)
        IF (ABS(rTiltMoment_1P_kNm) > 850.0) OR (ABS(rYawMoment_1P_kNm) > 850.0) THEN
            iOperatingFSMState := 7; (* Active IPC Asymmetric Load Mitigation *)
        ELSIF bLiDAR_GustDetected THEN
            iOperatingFSMState := 8; (* LiDAR Feed-Forward Active *)
        ELSIF rWindSpeed_Filtered_mps > 25.00 THEN
            iOperatingFSMState := 9; (* High Wind Storm Cut-Out *)
        ELSIF rVoted_RotorSpeed_rpm < 7.00 THEN
            iOperatingFSMState := 5; (* Return to Region 2.5 *)
        END_IF;

    7: (* FSM_IPC_ACTIVE_LOAD_REDUCTION: Multiblade Coleman d-q IPC engaged concurrently with collective pitch *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        rGenTorque_Cmd_kNm              := rRatedTorque_kNm;
        iControlRegion                  := 3;
        
        rSpeed_Error_rpm := rVoted_RotorSpeed_rpm - rRatedRotorSpeed_rpm;
        rPitch_Integral_deg := rPitch_Integral_deg + (rPitch_Ki * rSpeed_Error_rpm * 0.050);
        IF rPitch_Integral_deg > 35.0 THEN
            rPitch_Integral_deg := 35.0;
        ELSIF rPitch_Integral_deg < 0.0 THEN
            rPitch_Integral_deg := 0.0;
        END_IF;
        rPitchCmd_Collective_deg := (rPitch_Kp * rSpeed_Error_rpm) + rPitch_Integral_deg;
        
        IF bLiDAR_GustDetected THEN
            iOperatingFSMState := 8; (* LiDAR gust priority *)
        ELSIF (ABS(rTiltMoment_1P_kNm) <= 400.0) AND (ABS(rYawMoment_1P_kNm) <= 400.0) THEN
            iOperatingFSMState := 6; (* Moments suppressed, return to baseline Region 3 *)
        ELSIF rWindSpeed_Filtered_mps > 25.00 THEN
            iOperatingFSMState := 9; (* High Wind Storm Cut-Out *)
        END_IF;

    8: (* FSM_LIDAR_PREVIEW_FEEDFORWARD: Inflow preview gust suppression active *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        rGenTorque_Cmd_kNm              := rRatedTorque_kNm;
        iControlRegion                  := 3;
        
        rSpeed_Error_rpm := rVoted_RotorSpeed_rpm - rRatedRotorSpeed_rpm;
        rPitch_Integral_deg := rPitch_Integral_deg + (rPitch_Ki * rSpeed_Error_rpm * 0.050);
        IF rPitch_Integral_deg > 35.0 THEN
            rPitch_Integral_deg := 35.0;
        ELSIF rPitch_Integral_deg < 0.0 THEN
            rPitch_Integral_deg := 0.0;
        END_IF;
        rPitchCmd_Collective_deg := (rPitch_Kp * rSpeed_Error_rpm) + rPitch_Integral_deg;
        
        IF NOT bLiDAR_GustDetected AND (ABS(rLiDAR_Acceleration_mps2) < 0.35) THEN
            IF (ABS(rTiltMoment_1P_kNm) > 600.0) OR (ABS(rYawMoment_1P_kNm) > 600.0) THEN
                iOperatingFSMState := 7;
            ELSE
                iOperatingFSMState := 6;
            END_IF;
        ELSIF rWindSpeed_Filtered_mps > 25.00 THEN
            iOperatingFSMState := 9;
        END_IF;

    9: (* FSM_STORM_CUTOUT_HYSTERESIS: Sustained wind > 25 m/s, progressive pitch feathering *)
        bSystemReady                    := FALSE;
        bMechanicalLock_Engage          := FALSE;
        iControlRegion                  := 0;
        bStormCutOutLatched             := TRUE;
        
        (* Feather pitch at steady 2.5 deg/s *)
        IF rPitchCmd_Collective_deg < 90.0 THEN
            rPitchCmd_Collective_deg := rPitchCmd_Collective_deg + (2.50 * 0.050);
            IF rPitchCmd_Collective_deg > 90.0 THEN
                rPitchCmd_Collective_deg := 90.0;
            END_IF;
        END_IF;
        
        (* Ramp down electrical generator torque *)
        IF rGenTorque_Cmd_kNm > 0.0 THEN
            rGenTorque_Cmd_kNm := rGenTorque_Cmd_kNm - (2000.0 * 0.050);
            IF rGenTorque_Cmd_kNm < 0.0 THEN
                rGenTorque_Cmd_kNm := 0.0;
            END_IF;
        END_IF;
        
        IF (rPitchCmd_Collective_deg >= 89.0) AND (rVoted_RotorSpeed_rpm < 1.00) THEN
            bMechanicalLock_Engage := TRUE;
            bMainCircuitBreaker_ClosePermit := FALSE;
            IF rWindSpeed_Filtered_mps < 22.00 THEN
                bStormCutOutLatched := FALSE;
                iOperatingFSMState := 0; (* Storm passed, return to standby *)
            END_IF;
        END_IF;

    10: (* FSM_FAST_AERODYNAMIC_BRAKE: Emergency trip overspeed or safety loop drop *)
        bSystemReady                    := FALSE;
        bMainCircuitBreaker_ClosePermit := FALSE;
        iControlRegion                  := 0;
        
        (* Fast feathering at maximum rate 8.0 deg/s *)
        IF rPitchCmd_Collective_deg < 90.0 THEN
            rPitchCmd_Collective_deg := rPitchCmd_Collective_deg + (rPitchRateLimit_degps * 0.050);
            IF rPitchCmd_Collective_deg > 90.0 THEN
                rPitchCmd_Collective_deg := 90.0;
            END_IF;
        END_IF;
        
        rGenTorque_Cmd_kNm := 0.0;
        
        tFSM_BrakingTimer(IN := TRUE, PT := T#30S);
        IF (rVoted_RotorSpeed_rpm <= 0.60) OR tFSM_BrakingTimer.Q THEN
            tFSM_BrakingTimer(IN := FALSE);
            bMechanicalLock_Engage := TRUE;
            IF NOT bTurbineTripped AND bResetAlarms THEN
                iOperatingFSMState := 0; (* Reset to Standby *)
            END_IF;
        END_IF;

    11: (* FSM_FAULT_RIDE_THROUGH_FRT: Grid LVRT/HVRT voltage anomaly ride-through *)
        bSystemReady                    := TRUE;
        bMechanicalLock_Engage          := FALSE;
        iControlRegion                  := 3;
        
        (* Curtail torque to balance reduced grid power evacuation *)
        rGenTorque_Cmd_kNm := rRatedTorque_kNm * (rGridVoltage_kV / 66.0);
        IF rGenTorque_Cmd_kNm < 2500.0 THEN
            rGenTorque_Cmd_kNm := 2500.0;
        END_IF;
        
        (* Fast pitch assist to prevent rotor aerodynamic acceleration during grid fault *)
        IF rPitchCmd_Collective_deg < 25.0 THEN
            rPitchCmd_Collective_deg := rPitchCmd_Collective_deg + (4.00 * 0.050);
        END_IF;
        
        tFSM_FRTTimer(IN := TRUE, PT := T#3500MS);
        IF (NOT bLVRT_ActiveEvent AND NOT bHVRT_ActiveEvent) OR tFSM_FRTTimer.Q THEN
            tFSM_FRTTimer(IN := FALSE);
            IF rWindSpeed_Filtered_mps >= 10.50 THEN
                iOperatingFSMState := 6;
            ELSE
                iOperatingFSMState := 4;
            END_IF;
        END_IF;

END_CASE;

iOperatingFSMState := iOperatingFSMState;
"""

def generate_phase7():
    return """(* ======================================================================================================================
   PHASE 7: ACTIVE YAW CONTROL & GYROSCOPIC PRECESSION COMPENSATION
   Yaw azimuth regulation, proportional hydraulic caliper back-torque, and gyroscopic tilt moment feed-forward
   ====================================================================================================================== *)

(* Wrap ultrasonic relative wind direction to [-180.0, +180.0] degrees *)
rYawTrackingError_deg := rWindDirection_Vane_deg;
WHILE rYawTrackingError_deg > 180.0 DO
    rYawTrackingError_deg := rYawTrackingError_deg - 360.0;
END_WHILE;
WHILE rYawTrackingError_deg < -180.0 DO
    rYawTrackingError_deg := rYawTrackingError_deg + 360.0;
END_WHILE;

(* 30-Second first-order low pass filter on wind direction to eliminate turbulent noise *)
rWindDir_Filtered_deg := (0.99833 * rWindDir_Filtered_deg) + (0.00167 * rYawTrackingError_deg);

(* Evaluate yaw alignment deadband (+/- 3.50 degrees) with 15-second integration delay *)
IF ABS(rWindDir_Filtered_deg) > 3.50 THEN
    tYawMisalignmentTimer(IN := TRUE, PT := T#15S);
ELSE
    tYawMisalignmentTimer(IN := FALSE);
END_IF;

(* Automatic droop cable untwisting sequence evaluation *)
IF ABS(rCableTwist_deg) >= 720.0 THEN
    bCableUntwistActive := TRUE;
END_IF;

IF bCableUntwistActive THEN
    (* Execute automated cable unwinding when parked or during low wind idling *)
    IF (iOperatingFSMState = 0) OR (iOperatingFSMState = 1) OR (rWindSpeed_Filtered_mps < 4.00) THEN
        rYawBrakePressure_Cmd_bar := rYawSlippingPressure_bar;
        IF rCableTwist_deg > 15.0 THEN
            bYawDriveCW_Enable  := FALSE;
            bYawDriveCCW_Enable := TRUE;
            rYawRate_Cmd_degps  := rYawRate_Nominal_degps;
            rYawMotorTorque_Cmd_kNm := -3200.0;
        ELSIF rCableTwist_deg < -15.0 THEN
            bYawDriveCW_Enable  := TRUE;
            bYawDriveCCW_Enable := FALSE;
            rYawRate_Cmd_degps  := rYawRate_Nominal_degps;
            rYawMotorTorque_Cmd_kNm := 3200.0;
        ELSE
            bYawDriveCW_Enable  := FALSE;
            bYawDriveCCW_Enable := FALSE;
            rYawRate_Cmd_degps  := 0.0;
            rYawMotorTorque_Cmd_kNm := 0.0;
            rYawBrakePressure_Cmd_bar := rYawHoldingPressure_bar;
            bCableUntwistActive := FALSE;
        END_IF;
    ELSE
        bYawDriveCW_Enable  := FALSE;
        bYawDriveCCW_Enable := FALSE;
        rYawRate_Cmd_degps  := 0.0;
        rYawMotorTorque_Cmd_kNm := 0.0;
        rYawBrakePressure_Cmd_bar := rYawHoldingPressure_bar;
    END_IF;

ELSIF tYawMisalignmentTimer.Q AND NOT bMechanicalLock_Engage THEN
    bYawActive := TRUE;
    rYawBrakePressure_Cmd_bar := rYawSlippingPressure_bar; (* Caliper slips at 35 bar to damp gear teeth backlash *)
    
    IF rWindDir_Filtered_deg > 0.0 THEN
        bYawDriveCW_Enable  := TRUE;
        bYawDriveCCW_Enable := FALSE;
        rYawRate_Cmd_degps  := rYawRate_Nominal_degps;
        rYawMotorTorque_Cmd_kNm := 2850.0;
    ELSE
        bYawDriveCW_Enable  := FALSE;
        bYawDriveCCW_Enable := TRUE;
        rYawRate_Cmd_degps  := rYawRate_Nominal_degps;
        rYawMotorTorque_Cmd_kNm := -2850.0;
    END_IF;
    
    (* Calculate gyroscopic precessional moment: M_gyro = J_rotor * Omega_rotor * Omega_yaw *)
    rGyroscopicTiltTorque_kNm := (rRotorInertia_kgm2 * (rVoted_RotorSpeed_rpm * 0.104719755) *
                                 (rYawRate_Cmd_degps * 0.0174532925)) * 0.001;
    
    (* Check for yaw completion *)
    IF ABS(rWindDir_Filtered_deg) <= 0.80 THEN
        bYawActive := FALSE;
        bYawDriveCW_Enable  := FALSE;
        bYawDriveCCW_Enable := FALSE;
        rYawRate_Cmd_degps  := 0.0;
        rYawMotorTorque_Cmd_kNm := 0.0;
        rYawBrakePressure_Cmd_bar := rYawHoldingPressure_bar;
        tYawMisalignmentTimer(IN := FALSE);
    END_IF;

ELSE
    bYawActive := FALSE;
    bYawDriveCW_Enable  := FALSE;
    bYawDriveCCW_Enable := FALSE;
    rYawRate_Cmd_degps  := 0.0;
    rYawMotorTorque_Cmd_kNm := 0.0;
    rYawBrakePressure_Cmd_bar := rYawHoldingPressure_bar;
    rGyroscopicTiltTorque_kNm := 0.0;
END_IF;
"""

def generate_phase8():
    return """(* ======================================================================================================================
   PHASE 8: ACTUATOR COORDINATION, PITCH RATE LIMITING & COMMAND ASSEMBLY
   Synthesis of collective, IPC, LiDAR preview, and tower damping components into independent blade demands
   ====================================================================================================================== *)

(* Rate-limit baseline collective pitch demand (+/- 8.0 deg/s = 0.40 deg per 50 ms cycle) *)
IF (rPitchCmd_Collective_deg - rPrevPitchCmd_deg) > (rPitchRateLimit_degps * 0.050) THEN
    rPitchCmd_Collective_deg := rPrevPitchCmd_deg + (rPitchRateLimit_degps * 0.050);
ELSIF (rPitchCmd_Collective_deg - rPrevPitchCmd_deg) < (-1.0 * rPitchRateLimit_degps * 0.050) THEN
    rPitchCmd_Collective_deg := rPrevPitchCmd_deg - (rPitchRateLimit_degps * 0.050);
END_IF;
rPrevPitchCmd_deg := rPitchCmd_Collective_deg;

(* Assemble individual blade pitch demands *)
rPitchCmd_Blade1_deg := rPitchCmd_Collective_deg + rPitchOffset_IPC_B1_deg + rPitchOffset_LiDAR_FF_deg + rPitchOffset_TowerFA_deg;
rPitchCmd_Blade2_deg := rPitchCmd_Collective_deg + rPitchOffset_IPC_B2_deg + rPitchOffset_LiDAR_FF_deg + rPitchOffset_TowerFA_deg;
rPitchCmd_Blade3_deg := rPitchCmd_Collective_deg + rPitchOffset_IPC_B3_deg + rPitchOffset_LiDAR_FF_deg + rPitchOffset_TowerFA_deg;

(* Saturate commands to absolute physical pitch travel envelope [-1.0 deg, 90.0 deg] *)
IF rPitchCmd_Blade1_deg > 90.0 THEN rPitchCmd_Blade1_deg := 90.0; ELSIF rPitchCmd_Blade1_deg < -1.0 THEN rPitchCmd_Blade1_deg := -1.0; END_IF;
IF rPitchCmd_Blade2_deg > 90.0 THEN rPitchCmd_Blade2_deg := 90.0; ELSIF rPitchCmd_Blade2_deg < -1.0 THEN rPitchCmd_Blade2_deg := -1.0; END_IF;
IF rPitchCmd_Blade3_deg > 90.0 THEN rPitchCmd_Blade3_deg := 90.0; ELSIF rPitchCmd_Blade3_deg < -1.0 THEN rPitchCmd_Blade3_deg := -1.0; END_IF;

(* Generator airgap electromagnetic torque final assembly *)
rGenTorque_Cmd_kNm := rGenTorque_Cmd_kNm + rTorqueOffset_TowerSS_kNm;
IF rGenTorque_Cmd_kNm > 22000.0 THEN
    rGenTorque_Cmd_kNm := 22000.0;
ELSIF rGenTorque_Cmd_kNm < 0.0 THEN
    rGenTorque_Cmd_kNm := 0.0;
END_IF;

(* Electrical active power setpoint calculation (P = Tau * Omega * Efficiency) *)
rActivePower_Cmd_kW := (rGenTorque_Cmd_kNm * (rVoted_GenSpeed_rpm * 0.104719755)) * 0.955;
IF bRemoteCurtailmentEnable AND (rActivePower_Cmd_kW > rCurtailmentLimit_kW) THEN
    rActivePower_Cmd_kW := rCurtailmentLimit_kW;
END_IF;

(* Grid Fault Ride-Through Reactive Power Injection (Q = K_FRT * (1 - V_grid) * P_rated) *)
IF bLVRT_ActiveEvent AND (rGridVoltage_kV < 66.0) THEN
    rReactivePower_Cmd_kVAR := 2.0 * (1.0 - (rGridVoltage_kV / 66.0)) * 15000.0;
    IF rReactivePower_Cmd_kVAR > 6600.0 THEN
        rReactivePower_Cmd_kVAR := 6600.0;
    END_IF;
ELSE
    rReactivePower_Cmd_kVAR := 0.0;
END_IF;
"""

def generate_phase9():
    return """(* ======================================================================================================================
   PHASE 9: ISA-18.2 MULTI-TIERED ALARM EVALUATION, TRIP LATCHES & BIT-PACKED DIAGNOSTICS
   Comprehensive safety trip matrix, warning annunciations, and SCADA telemetry packing
   ====================================================================================================================== *)

(* Pitch actuator tracking discrepancy monitor *)
IF (ABS(rPitchCmd_Blade1_deg - rBladePitch_ActPos_B1_deg) > c_rPitchDiscrepancy_Max_deg) OR
   (ABS(rPitchCmd_Blade2_deg - rBladePitch_ActPos_B2_deg) > c_rPitchDiscrepancy_Max_deg) OR
   (ABS(rPitchCmd_Blade3_deg - rBladePitch_ActPos_B3_deg) > c_rPitchDiscrepancy_Max_deg) THEN
    tPitchDiscrepancyTimer(IN := TRUE, PT := T#200MS);
ELSE
    tPitchDiscrepancyTimer(IN := FALSE);
END_IF;

(* Reset alarms logic *)
IF bResetAlarms THEN
    bTurbineTripped := FALSE;
    dwAlarmWord_Critical := 16#00000000;
    dwAlarmWord_Warning := 16#00000000;
END_IF;

(* --- ISA-18.2 CATEGORY 1: EMERGENCY SAFETY SHUTDOWN TRIPS --- *)

(* Bit 0: Rotor Shaft Overspeed HH (>= 8.682 rpm / 115%) *)
IF rVoted_RotorSpeed_rpm >= c_rOverspeed_HH_rpm THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000001;
END_IF;

(* Bit 1: PMSG Generator Overspeed HH (>= 8.682 rpm) *)
IF rVoted_GenSpeed_rpm >= c_rOverspeed_HH_rpm THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000002;
END_IF;

(* Bit 2: Tower Top Vibration Peak Seismic Acceleration HH (>= 2.45 m/s^2) *)
IF (rVoted_TowerAcc_FA_mps2 >= c_rTowerAcc_HH_mps2) OR (rVoted_TowerAcc_SS_mps2 >= c_rTowerAcc_HH_mps2) THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000004;
END_IF;

(* Bit 3: Direct-Drive Main Bearing Overtemperature HH (>= 85.0 deg C) *)
IF (rBearingTemp_DE_degC >= c_rMainBearingTemp_HH_degC) OR (rBearingTemp_NDE_degC >= c_rMainBearingTemp_HH_degC) THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000008;
END_IF;

(* Bit 4: PMSG Multi-Phase Stator Winding Overtemperature HH (>= 125.0 deg C) *)
IF rStatorWindingTemp_degC >= c_rStatorTemp_HH_degC THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000010;
END_IF;

(* Bit 5: Converter DC Link Overvoltage HH (>= 1350 V) or Undervoltage LL (<= 850 V) *)
IF (rConverter_Vdc_V >= c_rConverterVdc_HH_V) OR (rConverter_Vdc_V <= c_rConverterVdc_LL_V) THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000020;
END_IF;

(* Bit 6: Blade Pitch Tracking Discrepancy Fault Timeout *)
IF tPitchDiscrepancyTimer.Q THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000040;
END_IF;

(* Bit 7: Hardwired Dual-Channel Emergency Stop Loop Interrupted *)
IF NOT bEmergencyStopDualCh THEN
    bTurbineTripped := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#00000080;
END_IF;

(* Immediate transition to Fast Aerodynamic Braking upon trip condition *)
IF bTurbineTripped AND (iOperatingFSMState <> 10) THEN
    iOperatingFSMState := 10;
END_IF;

(* --- ISA-18.2 CATEGORY 2: OPERATIONAL WARNINGS & DERATES --- *)

(* Bit 0: Rotor Speed Warning H (>= 8.154 rpm / 108%) *)
IF rVoted_RotorSpeed_rpm >= c_rOverspeed_H_rpm THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000001;
END_IF;

(* Bit 1: Tower Top Vibration Warning H (>= 1.75 m/s^2) *)
IF (rVoted_TowerAcc_FA_mps2 >= c_rTowerAcc_H_mps2) OR (rVoted_TowerAcc_SS_mps2 >= c_rTowerAcc_H_mps2) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000002;
END_IF;

(* Bit 2: Main Bearing High Temperature Warning H (>= 75.0 deg C) *)
IF (rBearingTemp_DE_degC >= c_rMainBearingTemp_H_degC) OR (rBearingTemp_NDE_degC >= c_rMainBearingTemp_H_degC) THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000004;
END_IF;

(* Bit 3: Stator Winding High Temperature Warning H (>= 105.0 deg C) *)
IF rStatorWindingTemp_degC >= c_rStatorTemp_H_degC THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000008;
END_IF;

(* Bit 4: Converter IGBT Power Module High Temperature H (>= 75.0 deg C) *)
IF rConverter_Temp_IGBT_degC >= 75.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000010;
END_IF;

(* Bit 5: Down-Tower Droop Cable High Torsion Angle (>= 540.0 deg) *)
IF ABS(rCableTwist_deg) >= 540.0 THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000020;
END_IF;

(* Bit 6: LiDAR Optical Preview Signal-to-Noise Ratio Invalid *)
IF NOT bLiDAR_DataValid THEN
    dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#00000040;
END_IF;

(* --- TELEMETRY STATUS WORD PACKING --- *)
dwTurbineStatusWord1 := 16#00000000;
IF bSystemReady                    THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000001; END_IF;
IF NOT bMechanicalLock_Engage      THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000002; END_IF;
IF bMainCircuitBreaker_ClosePermit THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000004; END_IF;
IF bYawActive                      THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000008; END_IF;
IF bCableUntwistActive             THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000010; END_IF;
IF bLiDAR_GustDetected             THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000020; END_IF;
IF bStormCutOutLatched             THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000040; END_IF;
IF bTurbineTripped                 THEN dwTurbineStatusWord1 := dwTurbineStatusWord1 OR 16#00000080; END_IF;

dwTurbineStatusWord2 := 16#00000000;
dwTurbineStatusWord2 := dwTurbineStatusWord2 OR INT_TO_DWORD(iOperatingFSMState);
dwTurbineStatusWord2 := dwTurbineStatusWord2 OR SHL(INT_TO_DWORD(iControlRegion), 8);
IF bDegraded_RotorSpeed OR bDegraded_GenSpeed OR bDegraded_LiDAR OR
   bDegraded_TowerAccFA OR bDegraded_TowerAccSS OR bDegraded_StrainB1 OR
   bDegraded_StrainB2   OR bDegraded_StrainB3 THEN
    dwTurbineStatusWord2 := dwTurbineStatusWord2 OR 16#00010000;
END_IF;

END_FUNCTION_BLOCK
"""

def assemble_all():
    code = "".join([
        generate_header(),
        generate_var_input(),
        generate_var_output(),
        generate_var(),
        generate_phase0(),
        generate_phase1(),
        generate_phase2(),
        generate_phase3(),
        generate_phase4(),
        generate_phase5(),
        generate_phase6(),
        generate_phase7(),
        generate_phase8(),
        generate_phase9()
    ])
    return code

if __name__ == "__main__":
    st_code = assemble_all()
    print(f"Total Structured Text character count: {len(st_code)}")
    print(f"Total lines: {st_code.count(chr(10))}")
