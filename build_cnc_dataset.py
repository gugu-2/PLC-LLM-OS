# -*- coding: utf-8 -*-
"""
Builder script for 5-Axis Heavy Gantry CNC Spindle Active Thermal Growth Compensation & 120-Tool ATC.
Target Output: data/swarm_raw/agent_6f90123a.json
"""

import json
import os
import validate_iec

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Mechanical Engineering & Heavy Machinery: 5-Axis Heavy Gantry CNC Spindle Active Thermal Growth Compensation & 120-Tool ATC: FB_CNC_Gantry5Axis_SpindleActiveThermalComp_Changer - 24,000 RPM Motorized High-Torque Spindle Rotor/Stator Heat Generation, Ceramic Hybrid Bearing Friction Dissipation, Multi-Axis Structural Volumetric Thermal Deformation (Axial Z-Growth, Radial Tilt), Receding-Horizon MPC Chiller Bypass Proportional Valve Pacing (Spindle Delta-T < 0.2°C under 45 kW Cutting Loads), Real-Time 5-Axis TCP Coordinate Offset Injection, 2oo3 TMR Sensor Voting (Embedded Fiber Bragg Grating FBG Strain/Temp, Front/Rear Bearing Pt100 RTDs, Non-Contact Capacitive Nose Displacement Probes), Multi-Stage Heavy Machining & Tool Management FSM (Spindle Warm-Up Profile, Active Thermal Compensation, 120-Pocket Matrix Tool Magazine Servomotor Positioning, Dual-Gripper High-Speed Tool Change Arm Exchange < 1.8s Chip-to-Chip, Taper Blow-Off, Tool Clamped Proximity Verification, Laser Broken Tool Detection), and ISA-18.2 Multi-Tiered Alarm Matrix.**"""

def build_code():
    # Let's assemble the ST code
    parts = []
    
    # Header block
    parts.append("""FUNCTION_BLOCK FB_CNC_Gantry5Axis_SpindleActiveThermalComp_Changer
(*
====================================================================================================
PROJECT:        5-AXIS HEAVY GANTRY CNC MILLING MACHINING CENTER CYBER-PHYSICAL CONTROL
SUBSYSTEM:      MOTORIZED HIGH-SPEED SPINDLE ACTIVE THERMAL COMPENSATION & 120-POCKET MATRIX ATC
MODULE:         FB_CNC_Gantry5Axis_SpindleActiveThermalComp_Changer
ARCHITECTURE:   DISCRETE STATE-SPACE OBSERVER + RECEDING-HORIZON MPC + 2oo3 TMR SENSOR FUSION +
                120-POCKET MATRIX SERVO ATC + ISA-18.2 MULTI-TIERED INTEGRATED ALARM TREE
AUTHOR:         LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECT (75+ YRS VETERAN FELLOW SPECIFICATION)
STANDARDS:      IEC 61131-3 3RD ED, ISO 230-3 (THERMAL EFFECTS ON CNC), ISO 10791 (MACHINING CENTERS),
                ISO 13849-1 (PL-d/SIL-2 SAFETY), ISA-18.2 (ALARM MANAGEMENT), DIN 69893 (HSK-A63 TAPER)
====================================================================================================

MATHEMATICAL AND CYBER-PHYSICAL CONTROL OVERVIEW:
----------------------------------------------------------------------------------------------------
1. THERMODYNAMIC & VOLUMETRIC THERMAL DRIFT PHENOMENOLOGY:
   High-speed 5-axis gantry milling of titanium (Ti-6Al-4V) and nickel superalloys (Inconel 718)
   requires high spindle rotational velocities (up to 24,000 RPM) combined with cutting powers up to
   45.0 kW continuous / 55.0 kW peak. The severe localized thermo-mechanical loads originate from:
     - Stator electromagnetic copper winding Joule losses (I^2 * R_cu(T)) and laminated stator core
       iron losses (eddy current and hysteresis: k_fe * f_e^1.6 * B^2).
     - Synchronous permanent magnet rotor losses (rotor surface eddy currents induced by high-frequency
       PWM inverter harmonics and windage air friction drag: P_windage = k_w * rho * omega^3 * R^4 * L).
     - Front tandem ceramic hybrid angular contact ball bearings (Si3N4 ceramic balls, Cronidur 30 steel
       rings) operating at 2.4 million DN value, dissipating frictional torque:
       M_total = M_0(v*n)^0.67 * d_m^3 + M_1 * P_1 * d_m + M_preload.
     - Rear floating hybrid ceramic bearing friction under axial thermal expansion sliding.
     - Structural volumetric thermal distortion: Axial thermal growth along the Z-axis (delta Z up to
       120 um uncompensated) and asymmetric radial bending drift (delta X, delta Y, and tilt angles A, B)
       due to structural heat migration into the machine ram and gantry cross-beam.

2. DISCRETE 7-STATE THERMAL-MECHANICAL STATE-SPACE PROPAGATION:
   Continuous-time lumped parameter thermal network discretized via zero-order hold (ZOH) at Ts = 50 ms:
     x[k+1] = A * x[k] + B * u[k] + L * (y[k] - (C * x[k] + D * u[k]))
   State vector x in R^7:
     x[1] : Spindle synchronous rotor core temperature [deg C]
     x[2] : Stator winding and lamination stack temperature [deg C]
     x[3] : Front ceramic hybrid bearing outer ring / cage temperature [deg C]
     x[4] : Rear ceramic hybrid bearing outer ring / cage temperature [deg C]
     x[5] : Spindle nose cartridge structural housing temperature [deg C]
     x[6] : Axial Z-axis spindle nose thermal expansion displacement [um]
     x[7] : Volumetric radial tilt / deflection vector magnitude [um]
   Actuation/Input vector u in R^4:
     u[1] : Spindle motor electrical and frictional heat dissipation rate [kW]
     u[2] : Closed-loop refrigeration chiller bypass proportional valve command [0..100 %]
     u[3] : Oil-air micro-lubrication pulse injection rate [0.2..5.0 Hz]
     u[4] : Machine bed cast iron structural reference temperature [deg C]
   Measurement vector y in R^4:
     y[1] : 2oo3 voted front bearing cage Pt100 RTD temperature [deg C]
     y[2] : 2oo3 voted rear bearing cage Pt100 RTD temperature [deg C]
     y[3] : 2oo3 voted embedded Fiber Bragg Grating (FBG) cartridge temperature [deg C]
     y[4] : 2oo3 voted non-contact capacitive spindle nose axial displacement [um]

3. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & 5-AXIS TCP COMPENSATION:
   A receding horizon N_p = 5 cost function minimizes thermal gradients and actuation slew:
     J = sum_{i=1}^{Np} (x_{k+i} - x_ref)^T * Q * (x_{k+i} - x_ref) + sum_{j=0}^{Nc-1} delta_u_{k+j}^T * R * delta_u_{k+j}
   The active thermal stabilization targets spindle cartridge temperature delta-T relative to the
   gantry reference bed casting <= 0.2 deg C under aggressive cutting load variations.
   Simultaneously, the estimated thermal displacement states (x[6], x[7]) synthesize real-time
   tool center point (TCP) compensation offsets injected into the numerical controller CNC coordinate
   interpolator (delta Z_tcp, delta X_tcp, delta Y_tcp, tilt A_tcp, tilt B_tcp) with sub-micron precision.

4. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
   Four dedicated sensor triplets guarantee mission-critical reliability and fail-operational safety:
     - Triplet 1: Embedded Fiber Bragg Grating (FBG) optical wavelength shift temperature sensors.
     - Triplet 2: Front ceramic bearing cage 4-wire Pt100 RTD precision elements.
     - Triplet 3: Rear ceramic bearing cage 4-wire Pt100 RTD precision elements.
     - Triplet 4: Non-contact high-bandwidth capacitive spindle nose axial displacement transducers.
   Each triplet executes cross-channel deviation auditing, integrating discrepancy timers, ISA-18.2
   discrepancy alarm annunciation, and deterministic mode degradation (2oo3 -> 1oo2 -> 1oo1 -> Trip).

5. 120-POCKET MATRIX TOOL MAGAZINE & DUAL-ARM ATC CHOREOGRAPHY:
   Precision management of high-capacity 120-pocket matrix tool magazine (10 rows x 12 columns):
     - Servomotor positioning in X (horizontal rack) and Y (vertical elevator) axes with S-curve profiles.
     - Shortest path pocket dispatch and pneumatic shot-pin mechanical pocket locking.
     - Ultra-fast cam-driven dual-gripper arm exchange (< 1.8 s chip-to-chip cycle time).
     - Hydraulic drawbar 18 kN HSK-A63 clamping with analog LVDT stroke and dual proximity verification.
     - Dual-pressure pneumatic sequence: 6.0 bar high-pressure taper purge blast during unclamp,
       switching to 0.5 bar continuous labyrinth sealing air during rotation.
     - Non-contact laser broken tool detection and tool table length wear updating at 1,000 RPM.
====================================================================================================
*)
VAR_INPUT
    (* =====================================================================================
       SECTION 1: SYSTEM CONTROL, SUPERVISORY & TIMING INTERFACES
       ===================================================================================== *)
    bEnable                         : BOOL := FALSE;    (* Master System Automation Enable Interlock [TRUE=Active] *)
    bReset                          : BOOL := FALSE;    (* Master Fault Reset and Alarm Acknowledge [TRUE=Reset] *)
    bAutoWarmupCmd                  : BOOL := FALSE;    (* Initiate Automated Cold-Start Spindle Warm-Up Profile [TRUE=Start] *)
    rSampleTime_s                   : REAL := 0.050;    (* Discrete Cyclic Execution Task Sample Time [s] *)

    (* =====================================================================================
       SECTION 2: SPINDLE DRIVE SENSOR FEEDBACK (24,000 RPM / 45 kW)
       ===================================================================================== *)
    rSpindleActualSpeed_RPM         : REAL := 0.0;      (* Motorized Spindle Actual Rotational Speed Feedback [RPM] *)
    rSpindleCommandSpeed_RPM        : REAL := 0.0;      (* Numerical Controller Commanded Target Speed [RPM] *)
    rSpindleMotorTorque_Nm          : REAL := 0.0;      (* Motor Shaft Actual Mechanical Torque [Nm] *)
    rSpindleMotorCurrent_A          : REAL := 0.0;      (* Stator 3-Phase Inverter RMS Current [A] *)
    rSpindleActivePower_kW          : REAL := 0.0;      (* Total Spindle Active Electrical Power Draw [kW] *)
    bSpindleOrientedLock            : BOOL := FALSE;    (* Spindle M19 Mechanical/Servo Angular Lock Signal [TRUE=Oriented] *)
    rSpindleAngularPosition_deg     : REAL := 0.0;      (* Spindle High-Resolution Optical Encoder Position [deg] *)

    (* =====================================================================================
       SECTION 3: MACHINE STRUCTURE & REFRIGERATION CHILLER SENSORS
       ===================================================================================== *)
    rMachineBedReferenceTemp_degC   : REAL := 20.0;     (* Machine Gantry Heavy Cast Iron Structural Bed Temp [deg C] *)
    rAmbientAirTemp_degC            : REAL := 20.0;     (* Machine Enclosure Ambient Air Temperature [deg C] *)
    rChillerInletTemp_degC          : REAL := 20.0;     (* Refrigeration Chiller Glycol Supply Temperature [deg C] *)
    rChillerReturnTemp_degC         : REAL := 20.5;     (* Refrigeration Chiller Glycol Return Temperature [deg C] *)
    rChillerFlowRate_Lpm            : REAL := 25.0;     (* Chiller Cooling Jacket Volumetric Flow Rate [L/min] *)
    rChillerLinePressure_bar        : REAL := 4.50;     (* Chiller Supply Circuit Fluid Hydraulic Pressure [bar] *)

    (* =====================================================================================
       SECTION 4: PNEUMATIC & HYDRAULIC FLUID SUBSYSTEM SENSORS
       ===================================================================================== *)
    rLubricationAirPressure_bar     : REAL := 3.20;     (* Spindle Bearing Oil-Air Micro-Lubrication Pressure [bar] *)
    rTaperPurgeAirPressure_bar      : REAL := 6.00;     (* Tool Holder Taper Cleaning Blast Air Pressure [bar] *)
    rSealingAirPressure_bar         : REAL := 0.50;     (* Spindle Nose Labyrinth Sealing Air Pressure [bar] *)
    rDrawbarHydraulicPressure_bar   : REAL := 120.0;    (* Tool Unclamp Hydraulic Actuation Pressure [bar] *)

    (* =====================================================================================
       SECTION 5: HSK-A63 TOOL CLAMPING & DRAWBAR TRANSDUCERS
       ===================================================================================== *)
    rDrawbarStrokeLVDT_mm           : REAL := 0.0;      (* Analog LVDT Tool Drawbar Clamping Stroke [mm] *)
    bDrawbarClampedProx1            : BOOL := TRUE;     (* Tool Clamped Inductive Proximity Sensor Channel 1 [TRUE=Clamped] *)
    bDrawbarClampedProx2            : BOOL := TRUE;     (* Tool Clamped Inductive Proximity Sensor Channel 2 [TRUE=Clamped] *)
    bDrawbarUnclampedProx           : BOOL := FALSE;    (* Tool Unclamped Inductive Proximity Sensor [TRUE=Unclamped] *)
    bToolPresentInSpindle           : BOOL := TRUE;     (* Tool Holder Seated Detection Optical/Air Sensor [TRUE=Present] *)

    (* =====================================================================================
       SECTION 6: 120-POCKET MATRIX ATC & SERVO INTERFACES
       ===================================================================================== *)
    bExecuteToolChange              : BOOL := FALSE;    (* CNC M06 Tool Change Execution Trigger Command [TRUE=Execute] *)
    nRequestedToolNumber            : INT := 1;         (* CNC Commanded Tool Index for Next Machining Operation [1..120] *)
    rMagazineActualPosX_mm          : REAL := 0.0;      (* Tool Magazine Matrix X-Axis Carriage Position [mm] *)
    rMagazineActualPosY_mm          : REAL := 0.0;      (* Tool Magazine Matrix Y-Axis Elevator Position [mm] *)
    bMagazineServoInPosition        : BOOL := TRUE;     (* Tool Magazine Servos Synchronized in Pocket Position [TRUE=Ready] *)
    bMagazinePocketLocked           : BOOL := TRUE;     (* Tool Magazine Mechanical Pocket Shot-Pin Engaged [TRUE=Locked] *)
    bAtcShutterDoorClosed           : BOOL := TRUE;     (* ATC Enclosure Protective Shutter Door Closed [TRUE=Closed] *)
    bAtcShutterDoorOpened           : BOOL := FALSE;    (* ATC Enclosure Protective Shutter Door Opened [TRUE=Opened] *)
    bAtcArmAtParkPosition           : BOOL := TRUE;     (* Dual-Gripper ATC Arm Parked in Safe Home Position [TRUE=Parked] *)
    bAtcGripper1ToolClamped         : BOOL := FALSE;    (* ATC Arm Gripper 1 Claw Locked on Tool Flange [TRUE=Clamped] *)
    bAtcGripper2ToolClamped         : BOOL := FALSE;    (* ATC Arm Gripper 2 Claw Locked on Tool Flange [TRUE=Clamped] *)

    (* =====================================================================================
       SECTION 7: NON-CONTACT DUAL-BEAM LASER TOOL SETTER
       ===================================================================================== *)
    bLaserToolSetterReady           : BOOL := TRUE;     (* Non-Contact Laser Tool Setter Self-Test Healthy [TRUE=Ready] *)
    bLaserBeamBlocked               : BOOL := FALSE;    (* Laser Optical Photodetector Beam Interruption [TRUE=Blocked] *)
    rLaserToolLengthMeasured_mm     : REAL := 150.000;  (* Laser Tool Setter Real-Time Dynamic Measured Length [mm] *)
    rLaserToolNominalLength_mm      : REAL := 150.000;  (* CNC Tool Registry Table Nominal Tool Gauge Length [mm] *)
    rLaserToolBreakageLimit_mm      : REAL := 0.350;    (* Maximum Allowable Axial Deviation Before Broken Trip [mm] *)

    (* =====================================================================================
       SECTION 8: 2oo3 TMR REDUNDANT SENSOR TRIPLET 1 - HOUSING FBG SENSORS
       ===================================================================================== *)
    rFBG_HousingTemp_ChA_degC       : REAL := 20.0;     (* Housing Fiber Bragg Grating Sensor Channel A [deg C] *)
    rFBG_HousingTemp_ChB_degC       : REAL := 20.0;     (* Housing Fiber Bragg Grating Sensor Channel B [deg C] *)
    rFBG_HousingTemp_ChC_degC       : REAL := 20.0;     (* Housing Fiber Bragg Grating Sensor Channel C [deg C] *)

    (* =====================================================================================
       SECTION 9: 2oo3 TMR REDUNDANT SENSOR TRIPLET 2 - FRONT BEARING Pt100 RTDS
       ===================================================================================== *)
    rFrontBearingTemp_ChA_degC      : REAL := 20.0;     (* Front Ceramic Bearing Cage Pt100 RTD Channel A [deg C] *)
    rFrontBearingTemp_ChB_degC      : REAL := 20.0;     (* Front Ceramic Bearing Cage Pt100 RTD Channel B [deg C] *)
    rFrontBearingTemp_ChC_degC      : REAL := 20.0;     (* Front Ceramic Bearing Cage Pt100 RTD Channel C [deg C] *)

    (* =====================================================================================
       SECTION 10: 2oo3 TMR REDUNDANT SENSOR TRIPLET 3 - REAR BEARING Pt100 RTDS
       ===================================================================================== *)
    rRearBearingTemp_ChA_degC       : REAL := 20.0;     (* Rear Ceramic Bearing Cage Pt100 RTD Channel A [deg C] *)
    rRearBearingTemp_ChB_degC       : REAL := 20.0;     (* Rear Ceramic Bearing Cage Pt100 RTD Channel B [deg C] *)
    rRearBearingTemp_ChC_degC       : REAL := 20.0;     (* Rear Ceramic Bearing Cage Pt100 RTD Channel C [deg C] *)

    (* =====================================================================================
       SECTION 11: 2oo3 TMR REDUNDANT SENSOR TRIPLET 4 - CAPACITIVE NOSE DISPLACEMENT
       ===================================================================================== *)
    rCapacitiveNoseDisp_ChA_um      : REAL := 0.0;      (* Spindle Nose Capacitive Displacement Probe Ch A [um] *)
    rCapacitiveNoseDisp_ChB_um      : REAL := 0.0;      (* Spindle Nose Capacitive Displacement Probe Ch B [um] *)
    rCapacitiveNoseDisp_ChC_um      : REAL := 0.0;      (* Spindle Nose Capacitive Displacement Probe Ch C [um] *)
END_VAR
VAR_OUTPUT
    (* =====================================================================================
       SECTION 12: SPINDLE SYSTEM OPERATIONAL STATUS & CUTTING PERMISSIVES
       ===================================================================================== *)
    bSpindleReadyForCut             : BOOL := FALSE;    (* Spindle Thermally Stabilized & Cutting Permissive [TRUE=Ready] *)
    bWarmupInProgress               : BOOL := FALSE;    (* Automated Spindle Warm-Up Ramping Sequence Active [TRUE=Warmup] *)
    bWarmupComplete                 : BOOL := FALSE;    (* Automated Spindle Warm-Up Profile Completed [TRUE=Complete] *)
    bThermalEquilibriumAchieved     : BOOL := FALSE;    (* Spindle Core-to-Bed Temperature Delta-T <= 0.2 deg C [TRUE=Stable] *)

    (* =====================================================================================
       SECTION 13: 120-POCKET MATRIX ATC ACTUATION COMMANDS & STATUS
       ===================================================================================== *)
    bToolChangeInProgress           : BOOL := FALSE;    (* ATC Tool Change Cycle Currently Executing [TRUE=Active] *)
    bToolChangeComplete             : BOOL := FALSE;    (* ATC Tool Change Completed Successfully Pulse [TRUE=Done] *)
    bToolBrokenAlarm                : BOOL := FALSE;    (* Non-Contact Laser Broken Tool Inspection Tripped [TRUE=Broken] *)
    nCurrentSpindleTool             : INT := 1;         (* Pocket/Tool Number Currently Clamped in Spindle [1..120] *)
    nMagazineTargetPocket           : INT := 1;         (* Target Matrix Magazine Pocket Dispatched [1..120] *)
    rMagazineTargetPosX_mm          : REAL := 0.0;      (* Target Commanded X-Axis Carriage Coordinate [mm] *)
    rMagazineTargetPosY_mm          : REAL := 0.0;      (* Target Commanded Y-Axis Elevator Coordinate [mm] *)
    bDrawbarClampCommand            : BOOL := TRUE;     (* Solenoid Valve Command to Clamp HSK Drawbar [TRUE=Clamp] *)
    bDrawbarUnclampCommand          : BOOL := FALSE;    (* Hydraulic Valve Command to Unclamp HSK Drawbar [TRUE=Unclamp] *)
    bTaperPurgeBlastCommand         : BOOL := FALSE;    (* High-Pressure 6-bar Taper Cleaning Air Solenoid [TRUE=Blow] *)
    bSealingAirCommand              : BOOL := TRUE;     (* Continuous 0.5-bar Spindle Nose Sealing Air [TRUE=On] *)
    bAtcShutterDoorOpenCmd          : BOOL := FALSE;    (* ATC Protective Shutter Door Open Command [TRUE=Open] *)
    bAtcArmDriveCommand             : BOOL := FALSE;    (* Dual-Gripper ATC Arm Cam Indexer Motor Run [TRUE=Drive] *)
    bMagazinePocketPinLockCmd       : BOOL := TRUE;     (* Tool Magazine Matrix Mechanical Shot-Pin Command [TRUE=Lock] *)

    (* =====================================================================================
       SECTION 14: RECEDING-HORIZON MPC ACTUATOR SIGNALS
       ===================================================================================== *)
    rChillerProportionalValve_Pct   : REAL := 35.0;     (* Chiller Cooling Jacket Bypass Valve Output [0.0..100.0 %] *)
    rLubePulseFrequency_Hz          : REAL := 1.00;     (* Spindle Bearing Oil-Air Micro-Lube Pulse Command [Hz] *)
    rEstimatedSpindleDeltaT_degC    : REAL := 0.0;      (* Spindle Housing Core to Machine Bed Temp Delta [deg C] *)

    (* =====================================================================================
       SECTION 15: REAL-TIME 5-AXIS CNC COORDINATE INJECTION OFFSETS
       ===================================================================================== *)
    rTcpOffsetDeltaZ_um             : REAL := 0.0;      (* Real-Time Axial Z-Axis Thermal Offset Compensation [um] *)
    rTcpOffsetDeltaX_um             : REAL := 0.0;      (* Real-Time Radial X-Axis Thermal Drift Compensation [um] *)
    rTcpOffsetDeltaY_um             : REAL := 0.0;      (* Real-Time Radial Y-Axis Thermal Drift Compensation [um] *)
    rTcpOffsetTiltA_mdeg            : REAL := 0.0;      (* Real-Time Angular Spindle Axis Pitch Compensation [mdeg] *)
    rTcpOffsetTiltB_mdeg            : REAL := 0.0;      (* Real-Time Angular Spindle Axis Yaw Compensation [mdeg] *)

    (* =====================================================================================
       SECTION 16: 2oo3 TMR VOTED SENSOR SIGNALS & DEGRADATION STATES
       ===================================================================================== *)
    rVotedHousingTemp_degC          : REAL := 20.0;     (* 2oo3 Voted Spindle Cartridge Housing Temperature [deg C] *)
    rVotedFrontBearingTemp_degC     : REAL := 20.0;     (* 2oo3 Voted Front Ceramic Bearing Temperature [deg C] *)
    rVotedRearBearingTemp_degC      : REAL := 20.0;     (* 2oo3 Voted Rear Ceramic Bearing Temperature [deg C] *)
    rVotedNoseDisplacement_um       : REAL := 0.0;      (* 2oo3 Voted Non-Contact Nose Axial Displacement [um] *)
    nTmrDegradedModeHousing         : INT := 3;         (* Housing FBG Mode (3=2oo3, 2=1oo2, 1=1oo1, 0=Fault) *)
    nTmrDegradedModeFrontBrg        : INT := 3;         (* Front Bearing Mode (3=2oo3, 2=1oo2, 1=1oo1, 0=Fault) *)
    nTmrDegradedModeRearBrg         : INT := 3;         (* Rear Bearing Mode (3=2oo3, 2=1oo2, 1=1oo1, 0=Fault) *)
    nTmrDegradedModeCapNose         : INT := 3;         (* Nose Capacitive Mode (3=2oo3, 2=1oo2, 1=1oo1, 0=Fault) *)

    (* =====================================================================================
       SECTION 17: ISA-18.2 ALARM WORDS & MACHINE STATUS PACKING
       ===================================================================================== *)
    dwIsaAlarmWord1                 : DWORD := 16#00000000; (* Priority 1 & 2 Alarms: Spindle Bearing & Stator Thermal Trips *)
    dwIsaAlarmWord2                 : DWORD := 16#00000000; (* Priority 2 & 3 Alarms: ATC Drawbar, Pocket, Laser, Fluid Systems *)
    dwIsaAlarmWord3                 : DWORD := 16#00000000; (* Priority 4 Alarms: 2oo3 TMR Discrepancy & Sensor Channel Faults *)
    dwMachineStatusWord             : DWORD := 16#00000000; (* Comprehensive Machine Operating Status & Subsystem Health *)
END_VAR
VAR
    (* =====================================================================================
       SECTION 18: DISCRETE 7-STATE THERMAL-MECHANICAL STATE-SPACE MATRICES
       ===================================================================================== *)
    matA                            : ARRAY[1..7, 1..7] OF REAL; (* Discrete State Transition Matrix A (7x7) *)
    matB                            : ARRAY[1..7, 1..4] OF REAL; (* Discrete Actuation Input Matrix B (7x4) *)
    matC                            : ARRAY[1..4, 1..7] OF REAL; (* Discrete Observation Matrix C (4x7) *)
    matD                            : ARRAY[1..4, 1..4] OF REAL; (* Direct Transmission Feedforward Matrix D (4x4) *)
    matL                            : ARRAY[1..7, 1..4] OF REAL; (* Discrete Luenberger Observer Feedback Gain Matrix (7x4) *)

    (* State, Control, Measurement & Innovation Vectors *)
    aStateX                         : ARRAY[1..7] OF REAL;       (* Filtered Estimated States x[k] *)
    aStateX_Pred                    : ARRAY[1..7] OF REAL;       (* Prior Predicted State Vector x_pred[k+1] *)
    aControlU                       : ARRAY[1..4] OF REAL;       (* Actuation & Exogenous Input Vector u[k] *)
    aControlU_Prev                  : ARRAY[1..4] OF REAL;       (* Previous Cycle Actuation Vector u[k-1] *)
    aMeasY                          : ARRAY[1..4] OF REAL;       (* Physical Sensor Measurement Vector y[k] *)
    aOutputY                        : ARRAY[1..4] OF REAL;       (* Observer Synthetic Measurement Vector y_hat[k] *)
    aInnovY                         : ARRAY[1..4] OF REAL;       (* Innovation Residual Vector (y - y_hat) *)
    aStateRef                       : ARRAY[1..7] OF REAL;       (* Dynamic Tracking Reference States x_ref[k] *)

    (* =====================================================================================
       SECTION 19: RECEDING-HORIZON MPC OPTIMIZER ARRAYS & WEIGHTS
       ===================================================================================== *)
    vecQ                            : ARRAY[1..7] OF REAL;       (* Quadratic State Penalty Weights Diagonal Matrix *)
    vecR                            : ARRAY[1..4] OF REAL;       (* Quadratic Actuator Slew Rate Penalties Diagonal Matrix *)
    vecP                            : ARRAY[1..7] OF REAL;       (* Terminal Horizon State Penalty Weights Diagonal Matrix *)
    aPredHorizonX                   : ARRAY[1..5, 1..7] OF REAL; (* 5-Step Receding Horizon State Trajectory Predictions *)
    aSimHorizonU                    : ARRAY[1..5, 1..4] OF REAL; (* Horizon Control Trajectory Candidate Steps *)
    rGradCostChiller                : REAL := 0.0;               (* Analytical Gradient of MPC Cost w.r.t Chiller Valve *)
    rGradCostLube                   : REAL := 0.0;               (* Analytical Gradient of MPC Cost w.r.t Lube Pulse *)
    rMpcStepSizeChiller             : REAL := 0.450;             (* Gradient Descent Optimizer Learning Rate for Valve *)
    rMpcStepSizeLube                : REAL := 0.080;             (* Gradient Descent Optimizer Learning Rate for Lube *)
    rChillerValveSlewLimit_PctPerS  : REAL := 4.0;               (* Maximum Allowable Chiller Valve Slew Rate [%/s] *)

    (* TCP Spatial Geometry & Low-Pass Filter Constants *)
    rSpindleGaugeLength_mm          : REAL := 280.0;             (* Effective Spindle Front Gauge Line to Pivot Length [mm] *)
    rTcpFilterGain                  : REAL := 0.120;             (* Exponential Smoothing Filter Alpha for Injected TCP Offsets *)
    rFiltTcpOffsetDeltaZ_um         : REAL := 0.0;               (* Smoothed Axial Z-Offset Compensation [um] *)
    rFiltTcpOffsetDeltaX_um         : REAL := 0.0;               (* Smoothed Radial X-Drift Compensation [um] *)
    rFiltTcpOffsetDeltaY_um         : REAL := 0.0;               (* Smoothed Radial Y-Drift Compensation [um] *)

    (* =====================================================================================
       SECTION 20: 2oo3 TMR VOTING VARIABLES - HOUSING FBG SENSORS
       ===================================================================================== *)
    bHousing_ChA_Valid              : BOOL := TRUE;
    bHousing_ChB_Valid              : BOOL := TRUE;
    bHousing_ChC_Valid              : BOOL := TRUE;
    rHousing_Diff_AB                : REAL := 0.0;
    rHousing_Diff_BC                : REAL := 0.0;
    rHousing_Diff_CA                : REAL := 0.0;
    rHousing_DiscTimer_A_s          : REAL := 0.0;
    rHousing_DiscTimer_B_s          : REAL := 0.0;
    rHousing_DiscTimer_C_s          : REAL := 0.0;
    bHousing_DiscAlarm_A            : BOOL := FALSE;
    bHousing_DiscAlarm_B            : BOOL := FALSE;
    bHousing_DiscAlarm_C            : BOOL := FALSE;
    rHousing_TolLimit_degC          : REAL := 1.80;              (* FBG Optical Cross-Channel Discrepancy Tolerance [deg C] *)

    (* =====================================================================================
       SECTION 21: 2oo3 TMR VOTING VARIABLES - FRONT BEARING Pt100 RTDS
       ===================================================================================== *)
    bFrontBrg_ChA_Valid             : BOOL := TRUE;
    bFrontBrg_ChB_Valid             : BOOL := TRUE;
    bFrontBrg_ChC_Valid             : BOOL := TRUE;
    rFrontBrg_Diff_AB               : REAL := 0.0;
    rFrontBrg_Diff_BC               : REAL := 0.0;
    rFrontBrg_Diff_CA               : REAL := 0.0;
    rFrontBrg_DiscTimer_A_s         : REAL := 0.0;
    rFrontBrg_DiscTimer_B_s         : REAL := 0.0;
    rFrontBrg_DiscTimer_C_s         : REAL := 0.0;
    bFrontBrg_DiscAlarm_A           : BOOL := FALSE;
    bFrontBrg_DiscAlarm_B           : BOOL := FALSE;
    bFrontBrg_DiscAlarm_C           : BOOL := FALSE;
    rFrontBrg_TolLimit_degC         : REAL := 2.50;              (* Bearing Cage RTD Cross-Channel Discrepancy Tolerance [deg C] *)

    (* =====================================================================================
       SECTION 22: 2oo3 TMR VOTING VARIABLES - REAR BEARING Pt100 RTDS
       ===================================================================================== *)
    bRearBrg_ChA_Valid              : BOOL := TRUE;
    bRearBrg_ChB_Valid              : BOOL := TRUE;
    bRearBrg_ChC_Valid              : BOOL := TRUE;
    rRearBrg_Diff_AB                : REAL := 0.0;
    rRearBrg_Diff_BC                : REAL := 0.0;
    rRearBrg_Diff_CA                : REAL := 0.0;
    rRearBrg_DiscTimer_A_s          : REAL := 0.0;
    rRearBrg_DiscTimer_B_s          : REAL := 0.0;
    rRearBrg_DiscTimer_C_s          : REAL := 0.0;
    bRearBrg_DiscAlarm_A            : BOOL := FALSE;
    bRearBrg_DiscAlarm_B            : BOOL := FALSE;
    bRearBrg_DiscAlarm_C            : BOOL := FALSE;
    rRearBrg_TolLimit_degC          : REAL := 2.50;              (* Rear Bearing RTD Cross-Channel Discrepancy Tolerance [deg C] *)

    (* =====================================================================================
       SECTION 23: 2oo3 TMR VOTING VARIABLES - NOSE CAPACITIVE DISPLACEMENT
       ===================================================================================== *)
    bCapNose_ChA_Valid              : BOOL := TRUE;
    bCapNose_ChB_Valid              : BOOL := TRUE;
    bCapNose_ChC_Valid              : BOOL := TRUE;
    rCapNose_Diff_AB                : REAL := 0.0;
    rCapNose_Diff_BC                : REAL := 0.0;
    rCapNose_Diff_CA                : REAL := 0.0;
    rCapNose_DiscTimer_A_s          : REAL := 0.0;
    rCapNose_DiscTimer_B_s          : REAL := 0.0;
    rCapNose_DiscTimer_C_s          : REAL := 0.0;
    bCapNose_DiscAlarm_A            : BOOL := FALSE;
    bCapNose_DiscAlarm_B            : BOOL := FALSE;
    bCapNose_DiscAlarm_C            : BOOL := FALSE;
    rCapNose_TolLimit_um            : REAL := 4.00;              (* Capacitive Nose Displacement Discrepancy Tolerance [um] *)
    rTmrTripTimeLimit_s             : REAL := 3.00;              (* Discrepancy Accumulation Trip Threshold Time [s] *)

    (* =====================================================================================
       SECTION 24: 120-POCKET MATRIX ATC MOTION & SEQUENCER INTERNALS
       ===================================================================================== *)
    nFsmState                       : INT := 0;                  (* Master FSM Active Operational Stage Index *)
    nPreviousFsmState               : INT := -1;                 (* Previous Operational Stage Index for Edge Detection *)
    rStateTimer_s                   : REAL := 0.0;               (* Universal Stage Elapsed Timer [s] *)
    rWarmupStepTimer_s              : REAL := 0.0;               (* Dedicated Spindle Warm-Up Stage Residence Timer [s] *)
    rAtcSubTimer_s                  : REAL := 0.0;               (* High-Speed ATC Sub-Sequence Micro-Timer [s] *)
    nTargetRow                      : INT := 1;                  (* Computed Matrix Magazine Target Row [1..10] *)
    nTargetCol                      : INT := 1;                  (* Computed Matrix Magazine Target Column [1..12] *)
    rPocketPitchX_mm                : REAL := 125.0;             (* Matrix Tool Pocket Horizontal Grid Center Distance [mm] *)
    rPocketPitchY_mm                : REAL := 140.0;             (* Matrix Tool Pocket Vertical Grid Center Distance [mm] *)
    rDrawbarClampedNominal_mm       : REAL := 0.00;              (* HSK-A63 Drawbar Clamped Nominal LVDT Position [mm] *)
    rDrawbarUnclampedNominal_mm     : REAL := 10.50;             (* HSK-A63 Drawbar Unclamped Nominal LVDT Position [mm] *)
    rDrawbarTolerance_mm            : REAL := 0.25;              (* Allowable Drawbar LVDT Clamping Position Tolerance [mm] *)
    bDrawbarStrokeInTolerance       : BOOL := TRUE;              (* LVDT Position Matches Expected Mechanically Seated Envelope *)

    (* =====================================================================================
       SECTION 25: ISA-18.2 TRIP LIMITS & SENSOR RATE-OF-RISE FILTERING
       ===================================================================================== *)
    rFrontBearingTemp_H_degC        : REAL := 55.0;              (* Front Bearing High Temperature Warning Level [deg C] *)
    rFrontBearingTemp_HH_degC       : REAL := 68.0;              (* Front Bearing High-High Temperature E-Stop Trip Level [deg C] *)
    rRearBearingTemp_H_degC         : REAL := 52.0;              (* Rear Bearing High Temperature Warning Level [deg C] *)
    rRearBearingTemp_HH_degC        : REAL := 65.0;              (* Rear Bearing High-High Temperature E-Stop Trip Level [deg C] *)
    rStatorWindingTemp_H_degC       : REAL := 90.0;              (* Motor Stator High Temperature Warning Level [deg C] *)
    rStatorWindingTemp_HH_degC      : REAL := 115.0;             (* Motor Stator High-High Temperature E-Stop Trip Level [deg C] *)
    rChillerFlowRate_L_Lpm          : REAL := 15.0;              (* Chiller Coolant Low Flow Rate Warning Level [L/min] *)
    rChillerFlowRate_LL_Lpm         : REAL := 8.0;               (* Chiller Coolant Low-Low Flow E-Stop Trip Level [L/min] *)
    rNoseGrowth_HH_um               : REAL := 120.0;             (* Axial Nose Thermal Expansion Maximum Safety Limit [um] *)
    rBearingTempRateLimit_degCpS    : REAL := 1.50;              (* Bearing Dynamic Rate-of-Rise Trip Limit [deg C/s] *)
    rFrontBearingRateOfRise_degCpS  : REAL := 0.0;              (* Real-Time Differentiated Bearing Temperature Gradient *)
    rPrevFrontBearingTemp_degC      : REAL := 20.0;              (* Previous Cycle Bearing Temperature for Differentiation *)
    rAlarmHysteresis_degC           : REAL := 1.20;              (* Temperature Alarm Reset Deadband Hysteresis [deg C] *)

    (* Algorithmic Iterators & One-Shot Initializer *)
    bFirstScan                      : BOOL := TRUE;              (* Cold System Power-Up First Execution Cycle Flag *)
    i                               : INT := 1;                  (* Outer Loop Dimension Iterator *)
    j                               : INT := 1;                  (* Inner Loop Dimension Iterator *)
    k                               : INT := 1;                  (* Actuator Dimension Iterator *)
    m                               : INT := 1;                  (* Observation Dimension Iterator *)
    p                               : INT := 1;                  (* Horizon Prediction Dimension Iterator *)
END_VAR
""")

    # Initialization on First Scan
    parts.append("""
(* ==========================================================================================
   INITIALIZATION: COLD-START DISCRETE MATRICES & MPC PENALTY INITIALIZATION
   ========================================================================================== *)
IF bFirstScan THEN
    (* --------------------------------------------------------------------------------------
       DISCRETE 7x7 STATE TRANSITION MATRIX matA (Sampling Time Ts = 50 ms)
       Derived from physical thermal capacitances (C_rot, C_stat, C_brg, C_hous) and
       inter-nodal thermal conductances (G_gap, G_jacket, G_raceway, G_contact, G_air).
       -------------------------------------------------------------------------------------- *)
    matA[1, 1] := 0.994200; matA[1, 2] := 0.003500; matA[1, 3] := 0.001800; matA[1, 4] := 0.000400; matA[1, 5] := 0.000100; matA[1, 6] := 0.000000; matA[1, 7] := 0.000000;
    matA[2, 1] := 0.004100; matA[2, 2] := 0.988200; matA[2, 3] := 0.002200; matA[2, 4] := 0.000800; matA[2, 5] := 0.004600; matA[2, 6] := 0.000000; matA[2, 7] := 0.000000;
    matA[3, 1] := 0.002800; matA[3, 2] := 0.001900; matA[3, 3] := 0.989500; matA[3, 4] := 0.000200; matA[3, 5] := 0.005500; matA[3, 6] := 0.000000; matA[3, 7] := 0.000000;
    matA[4, 1] := 0.001100; matA[4, 2] := 0.001500; matA[4, 3] := 0.000300; matA[4, 4] := 0.991200; matA[4, 5] := 0.005800; matA[4, 6] := 0.000000; matA[4, 7] := 0.000000;
    matA[5, 1] := 0.000200; matA[5, 2] := 0.005200; matA[5, 3] := 0.004800; matA[5, 4] := 0.004400; matA[5, 5] := 0.984500; matA[5, 6] := 0.000000; matA[5, 7] := 0.000000;
    matA[6, 1] := 0.012500; matA[6, 2] := 0.008400; matA[6, 3] := 0.024500; matA[6, 4] := 0.006200; matA[6, 5] := 0.038200; matA[6, 6] := 0.986000; matA[6, 7] := 0.000000;
    matA[7, 1] := 0.001500; matA[7, 2] := 0.004200; matA[7, 3] := 0.008800; matA[7, 4] := 0.003100; matA[7, 5] := 0.006500; matA[7, 6] := 0.000000; matA[7, 7] := 0.982000;

    (* --------------------------------------------------------------------------------------
       DISCRETE 7x4 INPUT MATRIX matB
       u[1] = Power Dissipation [kW], u[2] = Chiller Bypass Valve [%],
       u[3] = Oil-Air Lube Pulse [Hz], u[4] = Bed Reference Casting Temp [deg C]
       -------------------------------------------------------------------------------------- *)
    matB[1, 1] := 0.048500; matB[1, 2] := -0.000850; matB[1, 3] := -0.001200; matB[1, 4] := 0.000050;
    matB[2, 1] := 0.082000; matB[2, 2] := -0.012400; matB[2, 3] := -0.000300; matB[2, 4] := 0.000200;
    matB[3, 1] := 0.036500; matB[3, 2] := -0.006800; matB[3, 3] := -0.024500; matB[3, 4] := 0.000150;
    matB[4, 1] := 0.028000; matB[4, 2] := -0.005200; matB[4, 3] := -0.018500; matB[4, 4] := 0.000100;
    matB[5, 1] := 0.012500; matB[5, 2] := -0.018500; matB[5, 3] := -0.002500; matB[5, 4] := 0.001250;
    matB[6, 1] := 0.095000; matB[6, 2] := -0.045000; matB[6, 3] := -0.015000; matB[6, 4] := -0.003500;
    matB[7, 1] := 0.022000; matB[7, 2] := -0.011000; matB[7, 3] := -0.005500; matB[7, 4] := 0.000800;

    (* --------------------------------------------------------------------------------------
       DISCRETE 4x7 MEASUREMENT OBSERVATION MATRIX matC
       y[1] = Front Bearing RTD, y[2] = Rear Bearing RTD,
       y[3] = Cartridge FBG Temp, y[4] = Capacitive Spindle Nose Growth
       -------------------------------------------------------------------------------------- *)
    matC[1, 1] := 0.000000; matC[1, 2] := 0.000000; matC[1, 3] := 1.000000; matC[1, 4] := 0.000000; matC[1, 5] := 0.000000; matC[1, 6] := 0.000000; matC[1, 7] := 0.000000;
    matC[2, 1] := 0.000000; matC[2, 2] := 0.000000; matC[2, 3] := 0.000000; matC[2, 4] := 1.000000; matC[2, 5] := 0.000000; matC[2, 6] := 0.000000; matC[2, 7] := 0.000000;
    matC[3, 1] := 0.000000; matC[3, 2] := 0.000000; matC[3, 3] := 0.000000; matC[3, 4] := 0.000000; matC[3, 5] := 1.000000; matC[3, 6] := 0.000000; matC[3, 7] := 0.000000;
    matC[4, 1] := 0.000000; matC[4, 2] := 0.000000; matC[4, 3] := 0.000000; matC[4, 4] := 0.000000; matC[4, 5] := 0.000000; matC[4, 6] := 1.000000; matC[4, 7] := 0.000000;

    (* --------------------------------------------------------------------------------------
       DISCRETE 4x4 DIRECT FEEDTHROUGH MATRIX matD
       Zero direct transmission under strictly proper thermodynamic heat conduction dynamics.
       -------------------------------------------------------------------------------------- *)
    matD[1, 1] := 0.000000; matD[1, 2] := 0.000000; matD[1, 3] := 0.000000; matD[1, 4] := 0.000000;
    matD[2, 1] := 0.000000; matD[2, 2] := 0.000000; matD[2, 3] := 0.000000; matD[2, 4] := 0.000000;
    matD[3, 1] := 0.000000; matD[3, 2] := 0.000000; matD[3, 3] := 0.000000; matD[3, 4] := 0.000000;
    matD[4, 1] := 0.000000; matD[4, 2] := 0.000000; matD[4, 3] := 0.000000; matD[4, 4] := 0.000000;

    (* --------------------------------------------------------------------------------------
       DISCRETE 7x4 LUENBERGER OBSERVER GAIN MATRIX matL
       Designed via pole placement ensuring asymptotic error convergence faster than open loop.
       -------------------------------------------------------------------------------------- *)
    matL[1, 1] := 0.055000; matL[1, 2] := 0.015000; matL[1, 3] := 0.025000; matL[1, 4] := 0.002000;
    matL[2, 1] := 0.042000; matL[2, 2] := 0.018000; matL[2, 3] := 0.085000; matL[2, 4] := 0.001500;
    matL[3, 1] := 0.185000; matL[3, 2] := 0.006000; matL[3, 3] := 0.045000; matL[3, 4] := 0.004000;
    matL[4, 1] := 0.008000; matL[4, 2] := 0.175000; matL[4, 3] := 0.038000; matL[4, 4] := 0.002500;
    matL[5, 1] := 0.035000; matL[5, 2] := 0.025000; matL[5, 3] := 0.220000; matL[5, 4] := 0.008500;
    matL[6, 1] := 0.012000; matL[6, 2] := 0.008000; matL[6, 3] := 0.015000; matL[6, 4] := 0.280000;
    matL[7, 1] := 0.006000; matL[7, 2] := 0.004000; matL[7, 3] := 0.009000; matL[7, 4] := 0.065000;

    (* --------------------------------------------------------------------------------------
       RECEDING-HORIZON MPC COST WEIGHTING PENALTY VECTORS (Q, R, P)
       -------------------------------------------------------------------------------------- *)
    vecQ[1] := 1.500;   (* Rotor Core Thermal Drift Penalty *)
    vecQ[2] := 2.500;   (* Stator Winding Thermal Drift Penalty *)
    vecQ[3] := 8.000;   (* Front Bearing Cage Overheat Penalty *)
    vecQ[4] := 6.000;   (* Rear Bearing Cage Overheat Penalty *)
    vecQ[5] := 12.000;  (* Spindle Housing Core-to-Bed Delta-T Tracking Penalty *)
    vecQ[6] := 20.000;  (* Axial Nose Expansion Displacement Penalty *)
    vecQ[7] := 15.000;  (* Radial Bending Tilt Penalty *)

    vecR[1] := 0.050;   (* Power Modulation Penalty (virtual) *)
    vecR[2] := 1.200;   (* Chiller Proportional Bypass Valve Slew Penalty *)
    vecR[3] := 2.800;   (* Micro-Lubrication Pulse Slew Penalty *)
    vecR[4] := 0.000;   (* Ambient Bed Temperature (uncontrolled disturbance) *)

    vecP[1] := 2.500;   (* Terminal State Penalties *)
    vecP[2] := 4.000;
    vecP[3] := 14.000;
    vecP[4] := 10.000;
    vecP[5] := 22.000;
    vecP[6] := 35.000;
    vecP[7] := 25.000;

    (* Initialize State Vector to Machine Bed Reference Casting Temperature *)
    FOR i := 1 TO 5 DO
        aStateX[i] := rMachineBedReferenceTemp_degC;
        aStateRef[i] := rMachineBedReferenceTemp_degC;
    END_FOR;
    aStateX[6] := 0.0; aStateRef[6] := 0.0;
    aStateX[7] := 0.0; aStateRef[7] := 0.0;

    aControlU[1] := 0.0; aControlU_Prev[1] := 0.0;
    aControlU[2] := 35.0; aControlU_Prev[2] := 35.0;
    aControlU[3] := 1.0; aControlU_Prev[3] := 1.0;
    aControlU[4] := rMachineBedReferenceTemp_degC; aControlU_Prev[4] := rMachineBedReferenceTemp_degC;

    nFsmState := 0;
    nPreviousFsmState := -1;
    rPrevFrontBearingTemp_degC := rMachineBedReferenceTemp_degC;
    bFirstScan := FALSE;
END_IF;
""")

    # Phase 1: 2oo3 TMR Sensor Voting
    parts.append("""
(* ==========================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING
   Four independent physical sensor triplets guarantee high-integrity instrumentation.
   Modes: 3=Full 2oo3 Median Voting; 2=Degraded 1oo2 Average; 1=Degraded 1oo1 Single; 0=Fault Trip
   ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
   TRIPLET 1: SPINDLE CARTRIDGE HOUSING FIBER BRAGG GRATING (FBG) OPTICAL SENSORS [deg C]
   ------------------------------------------------------------------------------------------ *)
bHousing_ChA_Valid := (rFBG_HousingTemp_ChA_degC >= 5.0) AND (rFBG_HousingTemp_ChA_degC <= 125.0);
bHousing_ChB_Valid := (rFBG_HousingTemp_ChB_degC >= 5.0) AND (rFBG_HousingTemp_ChB_degC <= 125.0);
bHousing_ChC_Valid := (rFBG_HousingTemp_ChC_degC >= 5.0) AND (rFBG_HousingTemp_ChC_degC <= 125.0);

rHousing_Diff_AB := ABS(rFBG_HousingTemp_ChA_degC - rFBG_HousingTemp_ChB_degC);
rHousing_Diff_BC := ABS(rFBG_HousingTemp_ChB_degC - rFBG_HousingTemp_ChC_degC);
rHousing_Diff_CA := ABS(rFBG_HousingTemp_ChC_degC - rFBG_HousingTemp_ChA_degC);

IF bHousing_ChA_Valid AND bHousing_ChB_Valid AND (rHousing_Diff_AB > rHousing_TolLimit_degC) THEN
    rHousing_DiscTimer_A_s := rHousing_DiscTimer_A_s + rSampleTime_s;
ELSE
    rHousing_DiscTimer_A_s := MAX(0.0, rHousing_DiscTimer_A_s - (rSampleTime_s * 2.0));
END_IF;

IF bHousing_ChB_Valid AND bHousing_ChC_Valid AND (rHousing_Diff_BC > rHousing_TolLimit_degC) THEN
    rHousing_DiscTimer_B_s := rHousing_DiscTimer_B_s + rSampleTime_s;
ELSE
    rHousing_DiscTimer_B_s := MAX(0.0, rHousing_DiscTimer_B_s - (rSampleTime_s * 2.0));
END_IF;

IF bHousing_ChC_Valid AND bHousing_ChA_Valid AND (rHousing_Diff_CA > rHousing_TolLimit_degC) THEN
    rHousing_DiscTimer_C_s := rHousing_DiscTimer_C_s + rSampleTime_s;
ELSE
    rHousing_DiscTimer_C_s := MAX(0.0, rHousing_DiscTimer_C_s - (rSampleTime_s * 2.0));
END_IF;

bHousing_DiscAlarm_A := (rHousing_DiscTimer_A_s >= rTmrTripTimeLimit_s);
bHousing_DiscAlarm_B := (rHousing_DiscTimer_B_s >= rTmrTripTimeLimit_s);
bHousing_DiscAlarm_C := (rHousing_DiscTimer_C_s >= rTmrTripTimeLimit_s);

IF bHousing_ChA_Valid AND bHousing_ChB_Valid AND bHousing_ChC_Valid AND
   (NOT bHousing_DiscAlarm_A) AND (NOT bHousing_DiscAlarm_B) AND (NOT bHousing_DiscAlarm_C) THEN
    nTmrDegradedModeHousing := 3;
    IF ((rFBG_HousingTemp_ChA_degC >= rFBG_HousingTemp_ChB_degC) AND (rFBG_HousingTemp_ChA_degC <= rFBG_HousingTemp_ChC_degC)) OR
       ((rFBG_HousingTemp_ChA_degC <= rFBG_HousingTemp_ChB_degC) AND (rFBG_HousingTemp_ChA_degC >= rFBG_HousingTemp_ChC_degC)) THEN
        rVotedHousingTemp_degC := rFBG_HousingTemp_ChA_degC;
    ELSIF ((rFBG_HousingTemp_ChB_degC >= rFBG_HousingTemp_ChA_degC) AND (rFBG_HousingTemp_ChB_degC <= rFBG_HousingTemp_ChC_degC)) OR
          ((rFBG_HousingTemp_ChB_degC <= rFBG_HousingTemp_ChA_degC) AND (rFBG_HousingTemp_ChB_degC >= rFBG_HousingTemp_ChC_degC)) THEN
        rVotedHousingTemp_degC := rFBG_HousingTemp_ChB_degC;
    ELSE
        rVotedHousingTemp_degC := rFBG_HousingTemp_ChC_degC;
    END_IF;
ELSIF bHousing_ChA_Valid AND bHousing_ChB_Valid AND (NOT bHousing_DiscAlarm_A) THEN
    nTmrDegradedModeHousing := 2;
    rVotedHousingTemp_degC := 0.50 * (rFBG_HousingTemp_ChA_degC + rFBG_HousingTemp_ChB_degC);
ELSIF bHousing_ChB_Valid AND bHousing_ChC_Valid AND (NOT bHousing_DiscAlarm_B) THEN
    nTmrDegradedModeHousing := 2;
    rVotedHousingTemp_degC := 0.50 * (rFBG_HousingTemp_ChB_degC + rFBG_HousingTemp_ChC_degC);
ELSIF bHousing_ChC_Valid AND bHousing_ChA_Valid AND (NOT bHousing_DiscAlarm_C) THEN
    nTmrDegradedModeHousing := 2;
    rVotedHousingTemp_degC := 0.50 * (rFBG_HousingTemp_ChC_degC + rFBG_HousingTemp_ChA_degC);
ELSIF bHousing_ChA_Valid THEN
    nTmrDegradedModeHousing := 1;
    rVotedHousingTemp_degC := rFBG_HousingTemp_ChA_degC;
ELSIF bHousing_ChB_Valid THEN
    nTmrDegradedModeHousing := 1;
    rVotedHousingTemp_degC := rFBG_HousingTemp_ChB_degC;
ELSIF bHousing_ChC_Valid THEN
    nTmrDegradedModeHousing := 1;
    rVotedHousingTemp_degC := rFBG_HousingTemp_ChC_degC;
ELSE
    nTmrDegradedModeHousing := 0;
    rVotedHousingTemp_degC := rMachineBedReferenceTemp_degC;
END_IF;

(* ------------------------------------------------------------------------------------------
   TRIPLET 2: FRONT CERAMIC HYBRID BEARING CAGE Pt100 RTD SENSORS [deg C]
   ------------------------------------------------------------------------------------------ *)
bFrontBrg_ChA_Valid := (rFrontBearingTemp_ChA_degC >= 5.0) AND (rFrontBearingTemp_ChA_degC <= 140.0);
bFrontBrg_ChB_Valid := (rFrontBearingTemp_ChB_degC >= 5.0) AND (rFrontBearingTemp_ChB_degC <= 140.0);
bFrontBrg_ChC_Valid := (rFrontBearingTemp_ChC_degC >= 5.0) AND (rFrontBearingTemp_ChC_degC <= 140.0);

rFrontBrg_Diff_AB := ABS(rFrontBearingTemp_ChA_degC - rFrontBearingTemp_ChB_degC);
rFrontBrg_Diff_BC := ABS(rFrontBearingTemp_ChB_degC - rFrontBearingTemp_ChC_degC);
rFrontBrg_Diff_CA := ABS(rFrontBearingTemp_ChC_degC - rFrontBearingTemp_ChA_degC);

IF bFrontBrg_ChA_Valid AND bFrontBrg_ChB_Valid AND (rFrontBrg_Diff_AB > rFrontBrg_TolLimit_degC) THEN
    rFrontBrg_DiscTimer_A_s := rFrontBrg_DiscTimer_A_s + rSampleTime_s;
ELSE
    rFrontBrg_DiscTimer_A_s := MAX(0.0, rFrontBrg_DiscTimer_A_s - (rSampleTime_s * 2.0));
END_IF;

IF bFrontBrg_ChB_Valid AND bFrontBrg_ChC_Valid AND (rFrontBrg_Diff_BC > rFrontBrg_TolLimit_degC) THEN
    rFrontBrg_DiscTimer_B_s := rFrontBrg_DiscTimer_B_s + rSampleTime_s;
ELSE
    rFrontBrg_DiscTimer_B_s := MAX(0.0, rFrontBrg_DiscTimer_B_s - (rSampleTime_s * 2.0));
END_IF;

IF bFrontBrg_ChC_Valid AND bFrontBrg_ChA_Valid AND (rFrontBrg_Diff_CA > rFrontBrg_TolLimit_degC) THEN
    rFrontBrg_DiscTimer_C_s := rFrontBrg_DiscTimer_C_s + rSampleTime_s;
ELSE
    rFrontBrg_DiscTimer_C_s := MAX(0.0, rFrontBrg_DiscTimer_C_s - (rSampleTime_s * 2.0));
END_IF;

bFrontBrg_DiscAlarm_A := (rFrontBrg_DiscTimer_A_s >= rTmrTripTimeLimit_s);
bFrontBrg_DiscAlarm_B := (rFrontBrg_DiscTimer_B_s >= rTmrTripTimeLimit_s);
bFrontBrg_DiscAlarm_C := (rFrontBrg_DiscTimer_C_s >= rTmrTripTimeLimit_s);

IF bFrontBrg_ChA_Valid AND bFrontBrg_ChB_Valid AND bFrontBrg_ChC_Valid AND
   (NOT bFrontBrg_DiscAlarm_A) AND (NOT bFrontBrg_DiscAlarm_B) AND (NOT bFrontBrg_DiscAlarm_C) THEN
    nTmrDegradedModeFrontBrg := 3;
    IF ((rFrontBearingTemp_ChA_degC >= rFrontBearingTemp_ChB_degC) AND (rFrontBearingTemp_ChA_degC <= rFrontBearingTemp_ChC_degC)) OR
       ((rFrontBearingTemp_ChA_degC <= rFrontBearingTemp_ChB_degC) AND (rFrontBearingTemp_ChA_degC >= rFrontBearingTemp_ChC_degC)) THEN
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChA_degC;
    ELSIF ((rFrontBearingTemp_ChB_degC >= rFrontBearingTemp_ChA_degC) AND (rFrontBearingTemp_ChB_degC <= rFrontBearingTemp_ChC_degC)) OR
          ((rFrontBearingTemp_ChB_degC <= rFrontBearingTemp_ChA_degC) AND (rFrontBearingTemp_ChB_degC >= rFrontBearingTemp_ChC_degC)) THEN
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChB_degC;
    ELSE
        rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChC_degC;
    END_IF;
ELSIF bFrontBrg_ChA_Valid AND bFrontBrg_ChB_Valid AND (NOT bFrontBrg_DiscAlarm_A) THEN
    nTmrDegradedModeFrontBrg := 2;
    rVotedFrontBearingTemp_degC := 0.50 * (rFrontBearingTemp_ChA_degC + rFrontBearingTemp_ChB_degC);
ELSIF bFrontBrg_ChB_Valid AND bFrontBrg_ChC_Valid AND (NOT bFrontBrg_DiscAlarm_B) THEN
    nTmrDegradedModeFrontBrg := 2;
    rVotedFrontBearingTemp_degC := 0.50 * (rFrontBearingTemp_ChB_degC + rFrontBearingTemp_ChC_degC);
ELSIF bFrontBrg_ChC_Valid AND bFrontBrg_ChA_Valid AND (NOT bFrontBrg_DiscAlarm_C) THEN
    nTmrDegradedModeFrontBrg := 2;
    rVotedFrontBearingTemp_degC := 0.50 * (rFrontBearingTemp_ChC_degC + rFrontBearingTemp_ChA_degC);
ELSIF bFrontBrg_ChA_Valid THEN
    nTmrDegradedModeFrontBrg := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChA_degC;
ELSIF bFrontBrg_ChB_Valid THEN
    nTmrDegradedModeFrontBrg := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChB_degC;
ELSIF bFrontBrg_ChC_Valid THEN
    nTmrDegradedModeFrontBrg := 1;
    rVotedFrontBearingTemp_degC := rFrontBearingTemp_ChC_degC;
ELSE
    nTmrDegradedModeFrontBrg := 0;
    rVotedFrontBearingTemp_degC := rMachineBedReferenceTemp_degC;
END_IF;

(* ------------------------------------------------------------------------------------------
   TRIPLET 3: REAR CERAMIC HYBRID BEARING CAGE Pt100 RTD SENSORS [deg C]
   ------------------------------------------------------------------------------------------ *)
bRearBrg_ChA_Valid := (rRearBearingTemp_ChA_degC >= 5.0) AND (rRearBearingTemp_ChA_degC <= 140.0);
bRearBrg_ChB_Valid := (rRearBearingTemp_ChB_degC >= 5.0) AND (rRearBearingTemp_ChB_degC <= 140.0);
bRearBrg_ChC_Valid := (rRearBearingTemp_ChC_degC >= 5.0) AND (rRearBearingTemp_ChC_degC <= 140.0);

rRearBrg_Diff_AB := ABS(rRearBearingTemp_ChA_degC - rRearBearingTemp_ChB_degC);
rRearBrg_Diff_BC := ABS(rRearBearingTemp_ChB_degC - rRearBearingTemp_ChC_degC);
rRearBrg_Diff_CA := ABS(rRearBearingTemp_ChC_degC - rRearBearingTemp_ChA_degC);

IF bRearBrg_ChA_Valid AND bRearBrg_ChB_Valid AND (rRearBrg_Diff_AB > rRearBrg_TolLimit_degC) THEN
    rRearBrg_DiscTimer_A_s := rRearBrg_DiscTimer_A_s + rSampleTime_s;
ELSE
    rRearBrg_DiscTimer_A_s := MAX(0.0, rRearBrg_DiscTimer_A_s - (rSampleTime_s * 2.0));
END_IF;

IF bRearBrg_ChB_Valid AND bRearBrg_ChC_Valid AND (rRearBrg_Diff_BC > rRearBrg_TolLimit_degC) THEN
    rRearBrg_DiscTimer_B_s := rRearBrg_DiscTimer_B_s + rSampleTime_s;
ELSE
    rRearBrg_DiscTimer_B_s := MAX(0.0, rRearBrg_DiscTimer_B_s - (rSampleTime_s * 2.0));
END_IF;

IF bRearBrg_ChC_Valid AND bRearBrg_ChA_Valid AND (rRearBrg_Diff_CA > rRearBrg_TolLimit_degC) THEN
    rRearBrg_DiscTimer_C_s := rRearBrg_DiscTimer_C_s + rSampleTime_s;
ELSE
    rRearBrg_DiscTimer_C_s := MAX(0.0, rRearBrg_DiscTimer_C_s - (rSampleTime_s * 2.0));
END_IF;

bRearBrg_DiscAlarm_A := (rRearBrg_DiscTimer_A_s >= rTmrTripTimeLimit_s);
bRearBrg_DiscAlarm_B := (rRearBrg_DiscTimer_B_s >= rTmrTripTimeLimit_s);
bRearBrg_DiscAlarm_C := (rRearBrg_DiscTimer_C_s >= rTmrTripTimeLimit_s);

IF bRearBrg_ChA_Valid AND bRearBrg_ChB_Valid AND bRearBrg_ChC_Valid AND
   (NOT bRearBrg_DiscAlarm_A) AND (NOT bRearBrg_DiscAlarm_B) AND (NOT bRearBrg_DiscAlarm_C) THEN
    nTmrDegradedModeRearBrg := 3;
    IF ((rRearBearingTemp_ChA_degC >= rRearBearingTemp_ChB_degC) AND (rRearBearingTemp_ChA_degC <= rRearBearingTemp_ChC_degC)) OR
       ((rRearBearingTemp_ChA_degC <= rRearBearingTemp_ChB_degC) AND (rRearBearingTemp_ChA_degC >= rRearBearingTemp_ChC_degC)) THEN
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChA_degC;
    ELSIF ((rRearBearingTemp_ChB_degC >= rRearBearingTemp_ChA_degC) AND (rRearBearingTemp_ChB_degC <= rRearBearingTemp_ChC_degC)) OR
          ((rRearBearingTemp_ChB_degC <= rRearBearingTemp_ChA_degC) AND (rRearBearingTemp_ChB_degC >= rRearBearingTemp_ChC_degC)) THEN
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChB_degC;
    ELSE
        rVotedRearBearingTemp_degC := rRearBearingTemp_ChC_degC;
    END_IF;
ELSIF bRearBrg_ChA_Valid AND bRearBrg_ChB_Valid AND (NOT bRearBrg_DiscAlarm_A) THEN
    nTmrDegradedModeRearBrg := 2;
    rVotedRearBearingTemp_degC := 0.50 * (rRearBearingTemp_ChA_degC + rRearBearingTemp_ChB_degC);
ELSIF bRearBrg_ChB_Valid AND bRearBrg_ChC_Valid AND (NOT bRearBrg_DiscAlarm_B) THEN
    nTmrDegradedModeRearBrg := 2;
    rVotedRearBearingTemp_degC := 0.50 * (rRearBearingTemp_ChB_degC + rRearBearingTemp_ChC_degC);
ELSIF bRearBrg_ChC_Valid AND bRearBrg_ChA_Valid AND (NOT bRearBrg_DiscAlarm_C) THEN
    nTmrDegradedModeRearBrg := 2;
    rVotedRearBearingTemp_degC := 0.50 * (rRearBearingTemp_ChC_degC + rRearBearingTemp_ChA_degC);
ELSIF bRearBrg_ChA_Valid THEN
    nTmrDegradedModeRearBrg := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChA_degC;
ELSIF bRearBrg_ChB_Valid THEN
    nTmrDegradedModeRearBrg := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChB_degC;
ELSIF bRearBrg_ChC_Valid THEN
    nTmrDegradedModeRearBrg := 1;
    rVotedRearBearingTemp_degC := rRearBearingTemp_ChC_degC;
ELSE
    nTmrDegradedModeRearBrg := 0;
    rVotedRearBearingTemp_degC := rMachineBedReferenceTemp_degC;
END_IF;

(* ------------------------------------------------------------------------------------------
   TRIPLET 4: NON-CONTACT CAPACITIVE SPINDLE NOSE AXIAL DISPLACEMENT PROBES [um]
   ------------------------------------------------------------------------------------------ *)
bCapNose_ChA_Valid := (rCapacitiveNoseDisp_ChA_um >= -20.0) AND (rCapacitiveNoseDisp_ChA_um <= 200.0);
bCapNose_ChB_Valid := (rCapacitiveNoseDisp_ChB_um >= -20.0) AND (rCapacitiveNoseDisp_ChB_um <= 200.0);
bCapNose_ChC_Valid := (rCapacitiveNoseDisp_ChC_um >= -20.0) AND (rCapacitiveNoseDisp_ChC_um <= 200.0);

rCapNose_Diff_AB := ABS(rCapacitiveNoseDisp_ChA_um - rCapacitiveNoseDisp_ChB_um);
rCapNose_Diff_BC := ABS(rCapacitiveNoseDisp_ChB_um - rCapacitiveNoseDisp_ChC_um);
rCapNose_Diff_CA := ABS(rCapacitiveNoseDisp_ChC_um - rCapacitiveNoseDisp_ChA_um);

IF bCapNose_ChA_Valid AND bCapNose_ChB_Valid AND (rCapNose_Diff_AB > rCapNose_TolLimit_um) THEN
    rCapNose_DiscTimer_A_s := rCapNose_DiscTimer_A_s + rSampleTime_s;
ELSE
    rCapNose_DiscTimer_A_s := MAX(0.0, rCapNose_DiscTimer_A_s - (rSampleTime_s * 2.0));
END_IF;

IF bCapNose_ChB_Valid AND bCapNose_ChC_Valid AND (rCapNose_Diff_BC > rCapNose_TolLimit_um) THEN
    rCapNose_DiscTimer_B_s := rCapNose_DiscTimer_B_s + rSampleTime_s;
ELSE
    rCapNose_DiscTimer_B_s := MAX(0.0, rCapNose_DiscTimer_B_s - (rSampleTime_s * 2.0));
END_IF;

IF bCapNose_ChC_Valid AND bCapNose_ChA_Valid AND (rCapNose_Diff_CA > rCapNose_TolLimit_um) THEN
    rCapNose_DiscTimer_C_s := rCapNose_DiscTimer_C_s + rSampleTime_s;
ELSE
    rCapNose_DiscTimer_C_s := MAX(0.0, rCapNose_DiscTimer_C_s - (rSampleTime_s * 2.0));
END_IF;

bCapNose_DiscAlarm_A := (rCapNose_DiscTimer_A_s >= rTmrTripTimeLimit_s);
bCapNose_DiscAlarm_B := (rCapNose_DiscTimer_B_s >= rTmrTripTimeLimit_s);
bCapNose_DiscAlarm_C := (rCapNose_DiscTimer_C_s >= rTmrTripTimeLimit_s);

IF bCapNose_ChA_Valid AND bCapNose_ChB_Valid AND bCapNose_ChC_Valid AND
   (NOT bCapNose_DiscAlarm_A) AND (NOT bCapNose_DiscAlarm_B) AND (NOT bCapNose_DiscAlarm_C) THEN
    nTmrDegradedModeCapNose := 3;
    IF ((rCapacitiveNoseDisp_ChA_um >= rCapacitiveNoseDisp_ChB_um) AND (rCapacitiveNoseDisp_ChA_um <= rCapacitiveNoseDisp_ChC_um)) OR
       ((rCapacitiveNoseDisp_ChA_um <= rCapacitiveNoseDisp_ChB_um) AND (rCapacitiveNoseDisp_ChA_um >= rCapacitiveNoseDisp_ChC_um)) THEN
        rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChA_um;
    ELSIF ((rCapacitiveNoseDisp_ChB_um >= rCapacitiveNoseDisp_ChA_um) AND (rCapacitiveNoseDisp_ChB_um <= rCapacitiveNoseDisp_ChC_um)) OR
          ((rCapacitiveNoseDisp_ChB_um <= rCapacitiveNoseDisp_ChA_um) AND (rCapacitiveNoseDisp_ChB_um >= rCapacitiveNoseDisp_ChC_um)) THEN
        rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChB_um;
    ELSE
        rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChC_um;
    END_IF;
ELSIF bCapNose_ChA_Valid AND bCapNose_ChB_Valid AND (NOT bCapNose_DiscAlarm_A) THEN
    nTmrDegradedModeCapNose := 2;
    rVotedNoseDisplacement_um := 0.50 * (rCapacitiveNoseDisp_ChA_um + rCapacitiveNoseDisp_ChB_um);
ELSIF bCapNose_ChB_Valid AND bCapNose_ChC_Valid AND (NOT bCapNose_DiscAlarm_B) THEN
    nTmrDegradedModeCapNose := 2;
    rVotedNoseDisplacement_um := 0.50 * (rCapacitiveNoseDisp_ChB_um + rCapacitiveNoseDisp_ChC_um);
ELSIF bCapNose_ChC_Valid AND bCapNose_ChA_Valid AND (NOT bCapNose_DiscAlarm_C) THEN
    nTmrDegradedModeCapNose := 2;
    rVotedNoseDisplacement_um := 0.50 * (rCapacitiveNoseDisp_ChC_um + rCapacitiveNoseDisp_ChA_um);
ELSIF bCapNose_ChA_Valid THEN
    nTmrDegradedModeCapNose := 1;
    rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChA_um;
ELSIF bCapNose_ChB_Valid THEN
    nTmrDegradedModeCapNose := 1;
    rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChB_um;
ELSIF bCapNose_ChC_Valid THEN
    nTmrDegradedModeCapNose := 1;
    rVotedNoseDisplacement_um := rCapacitiveNoseDisp_ChC_um;
ELSE
    nTmrDegradedModeCapNose := 0;
    rVotedNoseDisplacement_um := 0.0;
END_IF;
""")

    # Phase 2: State-Space Propagation & Luenberger Observer
    parts.append("""
(* ==========================================================================================
   PHASE 2: DISCRETE STATE-SPACE THERMAL-MECHANICAL MODEL & LUENBERGER OBSERVER
   x[k+1] = A * x[k] + B * u[k] + L * (y[k] - (C * x[k] + D * u[k]))
   ========================================================================================== *)

(* ------------------------------------------------------------------------------------------
   PHYSICAL INPUT VECTOR COMPUTATION: POWER LOSSES & EXOGENOUS EXCITATIONS
   ------------------------------------------------------------------------------------------ *)
(* Ceramic hybrid bearing frictional dissipation: P = M_fric * omega *)
aControlU[1] := (0.000185 * EXPT(MAX(100.0, rSpindleActualSpeed_RPM), 1.35) / 1000.0) +
                (0.0450 * rSpindleMotorCurrent_A) +
                (0.0150 * rSpindleActivePower_kW); (* Total Thermal Heat Generation [kW] *)

aControlU[2] := rChillerProportionalValve_Pct;  (* Chiller Proportional Valve Command [%] *)
aControlU[3] := rLubePulseFrequency_Hz;         (* Micro-lubrication Pulse Frequency [Hz] *)
aControlU[4] := rMachineBedReferenceTemp_degC;  (* Gantry Cast Iron Reference Casting [deg C] *)

(* Map Sensor Vector y[k] from 2oo3 Voted Outputs *)
aMeasY[1] := rVotedFrontBearingTemp_degC;       (* Front Bearing Pt100 RTD [deg C] *)
aMeasY[2] := rVotedRearBearingTemp_degC;        (* Rear Bearing Pt100 RTD [deg C] *)
aMeasY[3] := rVotedHousingTemp_degC;            (* Cartridge Housing FBG Optical [deg C] *)
aMeasY[4] := rVotedNoseDisplacement_um;         (* Non-Contact Capacitive Nose Growth [um] *)

(* Step 1: Compute Model Outputs y_hat[k] = C * x[k] + D * u[k] *)
FOR m := 1 TO 4 DO
    aOutputY[m] := 0.0000;
    FOR j := 1 TO 7 DO
        aOutputY[m] := aOutputY[m] + (matC[m, j] * aStateX[j]);
    END_FOR;
    FOR k := 1 TO 4 DO
        aOutputY[m] := aOutputY[m] + (matD[m, k] * aControlU[k]);
    END_FOR;
END_FOR;

(* Step 2: Compute Innovation Residuals Innov = y_meas - y_hat *)
FOR m := 1 TO 4 DO
    aInnovY[m] := aMeasY[m] - aOutputY[m];
END_FOR;

(* Step 3: A-Priori State Dynamic Propagation x_pred[k+1] = A * x[k] + B * u[k] *)
FOR i := 1 TO 7 DO
    aStateX_Pred[i] := 0.0000;
    FOR j := 1 TO 7 DO
        aStateX_Pred[i] := aStateX_Pred[i] + (matA[i, j] * aStateX[j]);
    END_FOR;
    FOR k := 1 TO 4 DO
        aStateX_Pred[i] := aStateX_Pred[i] + (matB[i, k] * aControlU[k]);
    END_FOR;
END_FOR;

(* Step 4: Observer State Update with Innovation Correction x[k+1] = x_pred + L * Innov *)
FOR i := 1 TO 7 DO
    aStateX[i] := aStateX_Pred[i];
    FOR m := 1 TO 4 DO
        aStateX[i] := aStateX[i] + (matL[i, m] * aInnovY[m]);
    END_FOR;
END_FOR;

(* State Enveloping & Boundary Saturation *)
aStateX[1] := LIMIT(5.0, aStateX[1], 150.0);    (* Rotor Core Limit [deg C] *)
aStateX[2] := LIMIT(5.0, aStateX[2], 140.0);    (* Stator Winding Limit [deg C] *)
aStateX[3] := LIMIT(5.0, aStateX[3], 120.0);    (* Front Bearing Cage Limit [deg C] *)
aStateX[4] := LIMIT(5.0, aStateX[4], 120.0);    (* Rear Bearing Cage Limit [deg C] *)
aStateX[5] := LIMIT(5.0, aStateX[5], 90.0);     (* Cartridge Housing Limit [deg C] *)
aStateX[6] := LIMIT(-10.0, aStateX[6], 180.0);  (* Axial Z Growth Limit [um] *)
aStateX[7] := LIMIT(0.0, aStateX[7], 80.0);     (* Radial Volumetric Tilt Limit [um] *)

(* Compute Core-to-Bed Temperature Deviation *)
rEstimatedSpindleDeltaT_degC := aStateX[5] - rMachineBedReferenceTemp_degC;
bThermalEquilibriumAchieved := (ABS(rEstimatedSpindleDeltaT_degC) <= 0.20);
""")

    # Phase 3: Receding-Horizon MPC & TCP Coordinate Offset Injection
    parts.append("""
(* ==========================================================================================
   PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & TCP OFFSET INJECTION
   Paces chiller bypass proportional valve to maintain Delta-T < 0.2 deg C,
   and injects real-time 5-axis TCP coordinate offsets (X, Y, Z, A, B) into the CNC.
   ========================================================================================== *)

(* Store Prior Control Vector *)
FOR k := 1 TO 4 DO
    aControlU_Prev[k] := aControlU[k];
END_FOR;

(* Setup Dynamic Reference Vector: Spindle Target = Bed Reference Casting Temperature *)
FOR i := 1 TO 5 DO
    aStateRef[i] := rMachineBedReferenceTemp_degC;
END_FOR;
aStateRef[6] := 0.0; (* Target zero axial thermal expansion *)
aStateRef[7] := 0.0; (* Target zero radial tilt *)

(* Multi-Step Forward Horizon Simulation (Np = 5) *)
FOR p := 1 TO 5 DO
    FOR i := 1 TO 7 DO
        IF (p = 1) THEN
            aPredHorizonX[p, i] := aStateX[i];
        ELSE
            aPredHorizonX[p, i] := 0.0;
            FOR j := 1 TO 7 DO
                aPredHorizonX[p, i] := aPredHorizonX[p, i] + (matA[i, j] * aPredHorizonX[p - 1, j]);
            END_FOR;
            FOR k := 1 TO 4 DO
                aPredHorizonX[p, i] := aPredHorizonX[p, i] + (matB[i, k] * aControlU[k]);
            END_FOR;
        END_IF;
    END_FOR;
END_FOR;

(* Analytical MPC Gradient Evaluation w.r.t Chiller Proportional Valve & Lubrication *)
rGradCostChiller := 0.0;
rGradCostLube := 0.0;

FOR p := 1 TO 5 DO
    (* Housing delta-T sensitivity gradient: dJ/du_chiller *)
    rGradCostChiller := rGradCostChiller +
        (vecQ[5] * (aPredHorizonX[p, 5] - aStateRef[5]) * matB[5, 2]) +
        (vecQ[6] * (aPredHorizonX[p, 6] - aStateRef[6]) * matB[6, 2]);

    (* Bearing cage temperature sensitivity gradient: dJ/du_lube *)
    rGradCostLube := rGradCostLube +
        (vecQ[3] * (aPredHorizonX[p, 3] - aStateRef[3]) * matB[3, 3]) +
        (vecQ[4] * (aPredHorizonX[p, 4] - aStateRef[4]) * matB[4, 3]);
END_FOR;

(* Add Slew Rate Penalties *)
rGradCostChiller := rGradCostChiller + (vecR[2] * (aControlU[2] - aControlU_Prev[2]));
rGradCostLube    := rGradCostLube    + (vecR[3] * (aControlU[3] - aControlU_Prev[3]));

(* Receding Horizon Control Updates with Gradient Step & Slew Projection *)
IF (nFsmState = 30) OR (nFsmState = 24) OR (nFsmState = 26) THEN
    (* Active Milling or High Warm-Up: Execute Closed-Loop Optimization *)
    rChillerProportionalValve_Pct := rChillerProportionalValve_Pct - (rMpcStepSizeChiller * rGradCostChiller);
    rLubePulseFrequency_Hz        := rLubePulseFrequency_Hz        - (rMpcStepSizeLube * rGradCostLube);
ELSIF (nFsmState = 20) THEN
    (* Low-Speed Warm-up: Baseline Minimum Chilling *)
    rChillerProportionalValve_Pct := 20.0;
    rLubePulseFrequency_Hz        := 1.20;
ELSIF (nFsmState = 22) THEN
    (* Medium-Speed Warm-up: Intermediate Chilling *)
    rChillerProportionalValve_Pct := 35.0;
    rLubePulseFrequency_Hz        := 1.80;
ELSE
    (* Standby or ATC Exchange: Idling Chiller Circulation *)
    rChillerProportionalValve_Pct := 25.0;
    rLubePulseFrequency_Hz        := 0.50;
END_IF;

(* Rate-of-Change Clamping to Prevent Thermal Shock to Ceramic Hybrid Bearings *)
rChillerProportionalValve_Pct := LIMIT(
    aControlU_Prev[2] - (rChillerValveSlewLimit_PctPerS * rSampleTime_s),
    rChillerProportionalValve_Pct,
    aControlU_Prev[2] + (rChillerValveSlewLimit_PctPerS * rSampleTime_s)
);

(* Actuator Physical Saturation Limits *)
rChillerProportionalValve_Pct := LIMIT(0.0, rChillerProportionalValve_Pct, 100.0);
rLubePulseFrequency_Hz        := LIMIT(0.20, rLubePulseFrequency_Hz, 5.00);

(* ------------------------------------------------------------------------------------------
   REAL-TIME 5-AXIS TOOL CENTER POINT (TCP) COORDINATE OFFSET SYNTHESIS
   Compensates axial Z growth, radial X/Y drift, and gantry pitch/yaw angles in real time.
   ------------------------------------------------------------------------------------------ *)
(* Unfiltered Offset Formulation: Invert structural deformation vector *)
rFiltTcpOffsetDeltaZ_um := rFiltTcpOffsetDeltaZ_um + (rTcpFilterGain * ((-1.0 * aStateX[6]) - rFiltTcpOffsetDeltaZ_um));
rFiltTcpOffsetDeltaX_um := rFiltTcpOffsetDeltaX_um + (rTcpFilterGain * ((-0.65 * aStateX[7]) - rFiltTcpOffsetDeltaX_um));
rFiltTcpOffsetDeltaY_um := rFiltTcpOffsetDeltaY_um + (rTcpFilterGain * ((-0.45 * aStateX[7]) - rFiltTcpOffsetDeltaY_um));

rTcpOffsetDeltaZ_um := rFiltTcpOffsetDeltaZ_um;
rTcpOffsetDeltaX_um := rFiltTcpOffsetDeltaX_um;
rTcpOffsetDeltaY_um := rFiltTcpOffsetDeltaY_um;

(* Angular Pitch (A) and Yaw (B) Tilt Offsets [mdeg] *)
rTcpOffsetTiltA_mdeg := -1.0 * (rTcpOffsetDeltaY_um / rSpindleGaugeLength_mm) * 57.29578;
rTcpOffsetTiltB_mdeg := -1.0 * (rTcpOffsetDeltaX_um / rSpindleGaugeLength_mm) * 57.29578;
""")

    # Phase 4: 120-Pocket Matrix ATC Finite State Machine
    parts.append("""
(* ==========================================================================================
   PHASE 4: HEAVY MACHINING & 120-POCKET MATRIX ATC FINITE STATE MACHINE
   Manages automated spindle warm-up, active thermal machining, matrix pocket servo seek,
   dual-gripper high-speed arm tool exchange (< 1.8 s), and non-contact laser tool inspection.
   ========================================================================================== *)

(* Universal State Machine Step Timer *)
IF (nFsmState = nPreviousFsmState) THEN
    rStateTimer_s := rStateTimer_s + rSampleTime_s;
ELSE
    rStateTimer_s := 0.0;
    rAtcSubTimer_s := 0.0;
    nPreviousFsmState := nFsmState;
END_IF;

CASE nFsmState OF
    (* --------------------------------------------------------------------------------------
       STATE 0: SYSTEM INITIALIZATION & PERMISSIVE VERIFICATION
       -------------------------------------------------------------------------------------- *)
    0:
        bSpindleReadyForCut         := FALSE;
        bWarmupInProgress           := FALSE;
        bWarmupComplete             := FALSE;
        bToolChangeInProgress       := FALSE;
        bToolChangeComplete         := FALSE;
        bDrawbarClampCommand        := TRUE;
        bDrawbarUnclampCommand      := FALSE;
        bTaperPurgeBlastCommand     := FALSE;
        bSealingAirCommand          := TRUE;
        bAtcShutterDoorOpenCmd      := FALSE;
        bAtcArmDriveCommand         := FALSE;
        bMagazinePocketPinLockCmd   := TRUE;

        IF bEnable AND (NOT bReset) THEN
            IF bAutoWarmupCmd THEN
                nFsmState := 20; (* Branch to Warm-up Profile *)
            ELSE
                nFsmState := 10; (* Transition to Standby Ready *)
            END_IF;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 10: STANDBY IDLE & CHILLER BASELINE CIRCULATION
       -------------------------------------------------------------------------------------- *)
    10:
        bSpindleReadyForCut         := (ABS(rEstimatedSpindleDeltaT_degC) <= 0.50);
        bWarmupInProgress           := FALSE;
        bToolChangeInProgress       := FALSE;
        bDrawbarClampCommand        := TRUE;
        bDrawbarUnclampCommand      := FALSE;
        bTaperPurgeBlastCommand     := FALSE;
        bSealingAirCommand          := TRUE;
        bAtcShutterDoorOpenCmd      := FALSE;
        bAtcArmDriveCommand         := FALSE;
        bMagazinePocketPinLockCmd   := TRUE;

        IF (NOT bEnable) THEN
            nFsmState := 0;
        ELSIF bAutoWarmupCmd THEN
            nFsmState := 20; (* Cold Start Warm-Up Triggered *)
        ELSIF bExecuteToolChange THEN
            nFsmState := 40; (* ATC Tool Change Requested *)
        ELSIF (rSpindleActualSpeed_RPM > 200.0) THEN
            nFsmState := 30; (* Active Cutting Machining *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 20: SPINDLE WARM-UP RAMP 1 - LOW SPEED (4,000 RPM, GREASE REDISTRIBUTION)
       -------------------------------------------------------------------------------------- *)
    20:
        bSpindleReadyForCut   := FALSE;
        bWarmupInProgress     := TRUE;
        bWarmupComplete       := FALSE;
        bToolChangeInProgress := FALSE;
        rWarmupStepTimer_s    := rWarmupStepTimer_s + rSampleTime_s;

        IF (rWarmupStepTimer_s >= 60.0) THEN (* 60 s grease distribution dwell *)
            rWarmupStepTimer_s := 0.0;
            nFsmState := 22;
        ELSIF (NOT bEnable) THEN
            nFsmState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 22: SPINDLE WARM-UP RAMP 2 - MEDIUM SPEED (12,000 RPM, GRADIENT EQUALIZATION)
       -------------------------------------------------------------------------------------- *)
    22:
        bSpindleReadyForCut   := FALSE;
        bWarmupInProgress     := TRUE;
        bWarmupComplete       := FALSE;
        bToolChangeInProgress := FALSE;
        rWarmupStepTimer_s    := rWarmupStepTimer_s + rSampleTime_s;

        IF (rWarmupStepTimer_s >= 90.0) THEN (* 90 s thermal gradient stabilization *)
            rWarmupStepTimer_s := 0.0;
            nFsmState := 24;
        ELSIF (NOT bEnable) THEN
            nFsmState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 24: SPINDLE WARM-UP RAMP 3 - HIGH SPEED (20,000 RPM, THERMAL EQUILIBRIUM SOAK)
       -------------------------------------------------------------------------------------- *)
    24:
        bSpindleReadyForCut   := FALSE;
        bWarmupInProgress     := TRUE;
        bWarmupComplete       := FALSE;
        bToolChangeInProgress := FALSE;
        rWarmupStepTimer_s    := rWarmupStepTimer_s + rSampleTime_s;

        IF (rWarmupStepTimer_s >= 120.0) THEN (* 120 s high-speed equilibrium soak *)
            rWarmupStepTimer_s := 0.0;
            nFsmState := 26;
        ELSIF (NOT bEnable) THEN
            nFsmState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 26: SPINDLE WARM-UP THERMAL STABILITY VERIFICATION
       -------------------------------------------------------------------------------------- *)
    26:
        bSpindleReadyForCut   := FALSE;
        bWarmupInProgress     := TRUE;
        bWarmupComplete       := FALSE;

        IF (ABS(rEstimatedSpindleDeltaT_degC) <= 0.20) AND (rFrontBearingRateOfRise_degCpS <= 0.02) THEN
            bWarmupInProgress := FALSE;
            bWarmupComplete   := TRUE;
            nFsmState         := 10; (* Return to Standby Ready *)
        ELSIF (rStateTimer_s >= 180.0) THEN
            (* Timeout: Accept best-effort stabilization *)
            bWarmupInProgress := FALSE;
            bWarmupComplete   := TRUE;
            nFsmState         := 10;
        ELSIF (NOT bEnable) THEN
            nFsmState := 0;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 30: ACTIVE HEAVY MILLING & REAL-TIME THERMAL COMPENSATION
       -------------------------------------------------------------------------------------- *)
    30:
        bSpindleReadyForCut         := TRUE;
        bWarmupInProgress           := FALSE;
        bToolChangeInProgress       := FALSE;
        bDrawbarClampCommand        := TRUE;
        bDrawbarUnclampCommand      := FALSE;
        bTaperPurgeBlastCommand     := FALSE;
        bSealingAirCommand          := TRUE;
        bAtcShutterDoorOpenCmd      := FALSE;
        bAtcArmDriveCommand         := FALSE;
        bMagazinePocketPinLockCmd   := TRUE;

        IF (NOT bEnable) THEN
            nFsmState := 0;
        ELSIF bExecuteToolChange THEN
            nFsmState := 40; (* ATC Requested During Machining *)
        ELSIF (rSpindleActualSpeed_RPM <= 50.0) AND (rStateTimer_s > 2.0) THEN
            nFsmState := 10; (* Spindle Stopped: Return to Standby *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 40: ATC STAGE 1 - M19 SPINDLE DECELERATION & ORIENTATION LOCK
       -------------------------------------------------------------------------------------- *)
    40:
        bSpindleReadyForCut     := FALSE;
        bToolChangeInProgress   := TRUE;
        bToolChangeComplete     := FALSE;
        bDrawbarClampCommand    := TRUE;
        bDrawbarUnclampCommand  := FALSE;
        bTaperPurgeBlastCommand := FALSE;
        bSealingAirCommand      := TRUE;

        (* Await Spindle Stop (<= 2 RPM) and M19 Angular Orientation Lock *)
        IF (rSpindleActualSpeed_RPM <= 2.0) AND bSpindleOrientedLock THEN
            nFsmState := 50; (* Proceed to Tool Magazine Matrix Dispatch *)
        ELSIF (rStateTimer_s >= 6.00) THEN
            (* M19 Spindle Orientation Timeout Trip *)
            nFsmState := 120;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 50: ATC STAGE 2 - 120-POCKET MATRIX TOOL MAGAZINE SERVO DISPATCH
       -------------------------------------------------------------------------------------- *)
    50:
        bToolChangeInProgress     := TRUE;
        bMagazinePocketPinLockCmd := FALSE; (* Disengage shot-pin for travel *)
        nMagazineTargetPocket     := LIMIT(1, nRequestedToolNumber, 120);

        (* Compute 2D Matrix Coordinates: 10 rows x 12 columns *)
        nTargetRow := ((nMagazineTargetPocket - 1) / 12) + 1;
        nTargetCol := ((nMagazineTargetPocket - 1) MOD 12) + 1;
        rMagazineTargetPosX_mm := INT_TO_REAL(nTargetCol - 1) * rPocketPitchX_mm;
        rMagazineTargetPosY_mm := INT_TO_REAL(nTargetRow - 1) * rPocketPitchY_mm;

        IF bMagazineServoInPosition AND
           (ABS(rMagazineActualPosX_mm - rMagazineTargetPosX_mm) <= 0.15) AND
           (ABS(rMagazineActualPosY_mm - rMagazineTargetPosY_mm) <= 0.15) THEN
            nFsmState := 55; (* Matrix Pocket Position Reached *)
        ELSIF (rStateTimer_s >= 8.00) THEN
            (* Magazine Servo Positioning Timeout Trip *)
            nFsmState := 120;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 55: ATC STAGE 3 - MAGAZINE POCKET SHOT-PIN MECHANICAL LOCK
       -------------------------------------------------------------------------------------- *)
    55:
        bToolChangeInProgress     := TRUE;
        bMagazinePocketPinLockCmd := TRUE; (* Engage shot-pin into pocket disc *)

        IF bMagazinePocketLocked THEN
            nFsmState := 60; (* Pocket Locked: Open Shutter Door *)
        ELSIF (rStateTimer_s >= 2.00) THEN
            nFsmState := 120; (* Shot-Pin Engage Timeout *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 60: ATC STAGE 4 - ATC PROTECTIVE SHUTTER DOOR OPEN
       -------------------------------------------------------------------------------------- *)
    60:
        bToolChangeInProgress  := TRUE;
        bAtcShutterDoorOpenCmd := TRUE;

        IF bAtcShutterDoorOpened THEN
            nFsmState := 70; (* Shutter Door Open: Swing Dual-Gripper Arm *)
        ELSIF (rStateTimer_s >= 2.50) THEN
            nFsmState := 120; (* Door Open Failure Timeout *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 70: ATC STAGE 5 - DUAL-GRIPPER HIGH-SPEED ARM SWING 90 DEG (GRIP TOOLS)
       -------------------------------------------------------------------------------------- *)
    70:
        bToolChangeInProgress := TRUE;
        bAtcArmDriveCommand   := TRUE;
        rAtcSubTimer_s        := rAtcSubTimer_s + rSampleTime_s;

        (* Cam indexer rotates arm 90 deg into tool collars *)
        IF (rAtcSubTimer_s >= 0.35) AND bAtcGripper1ToolClamped AND bAtcGripper2ToolClamped THEN
            rAtcSubTimer_s := 0.0;
            nFsmState := 75; (* Both Tool Flanges Mechanically Gripped *)
        ELSIF (rStateTimer_s >= 2.00) THEN
            nFsmState := 120; (* Gripper Lock Timeout Trip *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 75: ATC STAGE 6 - HSK DRAWBAR HYDRAULIC UNCLAMP & TAPER AIR BLAST
       -------------------------------------------------------------------------------------- *)
    75:
        bToolChangeInProgress   := TRUE;
        bDrawbarClampCommand    := FALSE;
        bDrawbarUnclampCommand  := TRUE;  (* Hydraulic 120 bar unclamp cylinder *)
        bTaperPurgeBlastCommand := TRUE;  (* 6.0 bar air blast to purge taper cone *)
        bSealingAirCommand      := FALSE;

        (* Verify Drawbar Analog LVDT Stroke (10.5 mm +- 0.25 mm) and Unclamp Prox *)
        bDrawbarStrokeInTolerance := (ABS(rDrawbarStrokeLVDT_mm - rDrawbarUnclampedNominal_mm) <= rDrawbarTolerance_mm);

        IF bDrawbarUnclampedProx AND bDrawbarStrokeInTolerance THEN
            nFsmState := 80; (* Unclamp Complete: Execute 180 Deg Arm Swap *)
        ELSIF (rStateTimer_s >= 1.50) THEN
            nFsmState := 120; (* Drawbar Unclamp Timeout Trip *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 80: ATC STAGE 7 - DUAL ARM EXTRACT, 180 DEG SWAP & INSERT (< 0.45 s)
       -------------------------------------------------------------------------------------- *)
    80:
        bToolChangeInProgress   := TRUE;
        bDrawbarClampCommand    := FALSE;
        bDrawbarUnclampCommand  := TRUE;
        bTaperPurgeBlastCommand := TRUE;
        rAtcSubTimer_s          := rAtcSubTimer_s + rSampleTime_s;

        (* Cam mechanism pulls tools 100 mm along Z, rotates 180 deg, and reseats tools *)
        IF (rAtcSubTimer_s >= 0.45) THEN
            rAtcSubTimer_s := 0.0;
            nFsmState := 85; (* Arm Swapped: Re-clamp Spindle Drawbar *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 85: ATC STAGE 8 - HSK DRAWBAR SPRING CLAMP & LVDT STROKE VERIFY
       -------------------------------------------------------------------------------------- *)
    85:
        bToolChangeInProgress   := TRUE;
        bDrawbarClampCommand    := TRUE;  (* Hydraulic pressure released: 18 kN disc spring clamp *)
        bDrawbarUnclampCommand  := FALSE;
        bTaperPurgeBlastCommand := FALSE; (* Stop blast air *)
        bSealingAirCommand      := TRUE;  (* Re-engage continuous labyrinth sealing air *)

        (* Verify Drawbar Clamped Position: LVDT at 0.0 mm +- 0.25 mm and Dual Prox 1 & 2 *)
        bDrawbarStrokeInTolerance := (ABS(rDrawbarStrokeLVDT_mm - rDrawbarClampedNominal_mm) <= rDrawbarTolerance_mm);

        IF bDrawbarClampedProx1 AND bDrawbarClampedProx2 AND bDrawbarStrokeInTolerance AND bToolPresentInSpindle THEN
            nCurrentSpindleTool := nMagazineTargetPocket;
            nFsmState := 90; (* Tool Clamped Perfectly: Retract Dual Arm *)
        ELSIF (rStateTimer_s >= 1.50) THEN
            nFsmState := 120; (* Tool Clamping Failure Trip *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 90: ATC STAGE 9 - DUAL-GRIPPER ARM RETRACT TO PARK POSITION
       -------------------------------------------------------------------------------------- *)
    90:
        bToolChangeInProgress := TRUE;
        bAtcArmDriveCommand   := FALSE;

        IF bAtcArmAtParkPosition THEN
            nFsmState := 95; (* Arm Safely Parked: Close Shutter Door *)
        ELSIF (rStateTimer_s >= 2.00) THEN
            nFsmState := 120; (* Arm Park Timeout Trip *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 95: ATC STAGE 10 - ATC SHUTTER PROTECTIVE DOOR CLOSE
       -------------------------------------------------------------------------------------- *)
    95:
        bToolChangeInProgress  := TRUE;
        bAtcShutterDoorOpenCmd := FALSE;

        IF bAtcShutterDoorClosed THEN
            nFsmState := 100; (* Door Closed: Proceed to Laser Tool Setter *)
        ELSIF (rStateTimer_s >= 2.50) THEN
            nFsmState := 120; (* Door Close Failure Timeout *)
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 100: ATC STAGE 11 - NON-CONTACT LASER BROKEN TOOL INSPECTION
       -------------------------------------------------------------------------------------- *)
    100:
        bToolChangeInProgress := TRUE;

        IF bLaserToolSetterReady THEN
            (* Check measured tool length against allowable breakage deviation *)
            IF (ABS(rLaserToolLengthMeasured_mm - rLaserToolNominalLength_mm) > rLaserToolBreakageLimit_mm) OR
               (NOT bLaserBeamBlocked) THEN
                bToolBrokenAlarm := TRUE;
                nFsmState        := 120; (* Broken Tool Detected Trip! *)
            ELSE
                bToolBrokenAlarm := FALSE;
                nFsmState        := 105; (* Tool Tip Healthy: Update Offset *)
            END_IF;
        ELSE
            (* Laser Setter Offline: Skip Inspection with Warning *)
            nFsmState := 110;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 105: ATC STAGE 12 - CNC TOOL TABLE GAUGE LENGTH OFFSET SYNC
       -------------------------------------------------------------------------------------- *)
    105:
        bToolChangeInProgress := TRUE;
        nFsmState             := 110;

    (* --------------------------------------------------------------------------------------
       STATE 110: ATC STAGE 13 - ATC CYCLE COMPLETE & CNC HANDSHAKE
       -------------------------------------------------------------------------------------- *)
    110:
        bToolChangeInProgress := FALSE;
        bToolChangeComplete   := TRUE;

        IF (NOT bExecuteToolChange) THEN
            bToolChangeComplete := FALSE;
            nFsmState           := 10; (* Return to Standby Ready *)
        ELSIF (rStateTimer_s >= 1.00) THEN
            bToolChangeComplete := FALSE;
            nFsmState           := 10;
        END_IF;

    (* --------------------------------------------------------------------------------------
       STATE 120: EMERGENCY SAFETY LOCKOUT & FAULT TRIP
       -------------------------------------------------------------------------------------- *)
    120:
        bSpindleReadyForCut     := FALSE;
        bWarmupInProgress       := FALSE;
        bToolChangeInProgress   := FALSE;
        bDrawbarUnclampCommand  := FALSE;
        bDrawbarClampCommand    := TRUE;
        bTaperPurgeBlastCommand := FALSE;
        bSealingAirCommand      := TRUE;
        bAtcShutterDoorOpenCmd  := FALSE;
        bAtcArmDriveCommand     := FALSE;

        IF bReset THEN
            bToolBrokenAlarm := FALSE;
            nFsmState        := 0; (* Reset Lockout *)
        END_IF;
END_CASE;
""")

    # Phase 5: ISA-18.2 Multi-Tiered Alarms & Bitfield Packing
    parts.append("""
(* ==========================================================================================
   PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & DIAGNOSTIC WORD BITFIELD PACKING
   Evaluates over-temperature, thermal growth, unclamp-in-motion safety violation,
   and sensor discrepancy alarms, packing into standardized 32-bit status words.
   ========================================================================================== *)

(* Differentiate Front Bearing Temperature Rate of Rise [deg C/s] *)
rFrontBearingRateOfRise_degCpS := ABS(rVotedFrontBearingTemp_degC - rPrevFrontBearingTemp_degC) / rSampleTime_s;
rPrevFrontBearingTemp_degC := rVotedFrontBearingTemp_degC;

(* ------------------------------------------------------------------------------------------
   ISA-18.2 ALARM WORD 1: BEARING & STATOR THERMAL TRIPS (CRITICAL PRIORITY 1 & 2)
   ------------------------------------------------------------------------------------------ *)
(* Bit 0: Front Bearing High-High Temperature E-Stop Trip (68 deg C) *)
IF (rVotedFrontBearingTemp_degC >= rFrontBearingTemp_HH_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000001;
ELSIF bReset OR (rVotedFrontBearingTemp_degC < (rFrontBearingTemp_HH_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFFE;
END_IF;

(* Bit 1: Front Bearing High Temperature Warning (55 deg C) *)
IF (rVotedFrontBearingTemp_degC >= rFrontBearingTemp_H_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000002;
ELSIF bReset OR (rVotedFrontBearingTemp_degC < (rFrontBearingTemp_H_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFFD;
END_IF;

(* Bit 2: Rear Bearing High-High Temperature E-Stop Trip (65 deg C) *)
IF (rVotedRearBearingTemp_degC >= rRearBearingTemp_HH_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000004;
ELSIF bReset OR (rVotedRearBearingTemp_degC < (rRearBearingTemp_HH_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFFB;
END_IF;

(* Bit 3: Rear Bearing High Temperature Warning (52 deg C) *)
IF (rVotedRearBearingTemp_degC >= rRearBearingTemp_H_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000008;
ELSIF bReset OR (rVotedRearBearingTemp_degC < (rRearBearingTemp_H_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFF7;
END_IF;

(* Bit 4: Stator Winding High-High Temperature E-Stop Trip (115 deg C) *)
IF (aStateX[2] >= rStatorWindingTemp_HH_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000010;
ELSIF bReset OR (aStateX[2] < (rStatorWindingTemp_HH_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFEF;
END_IF;

(* Bit 5: Stator Winding High Temperature Warning (90 deg C) *)
IF (aStateX[2] >= rStatorWindingTemp_H_degC) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000020;
ELSIF bReset OR (aStateX[2] < (rStatorWindingTemp_H_degC - rAlarmHysteresis_degC)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFDF;
END_IF;

(* Bit 6: Spindle Bearing Temperature Dynamic Rate-of-Rise Trip (> 1.5 deg C/s) *)
IF (rFrontBearingRateOfRise_degCpS >= rBearingTempRateLimit_degCpS) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000040;
ELSIF bReset THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFFBF;
END_IF;

(* Bit 7: Axial Nose Thermal Growth Maximum Safety Trip (> 120 um) *)
IF (rVotedNoseDisplacement_um >= rNoseGrowth_HH_um) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000080;
ELSIF bReset OR (rVotedNoseDisplacement_um < (rNoseGrowth_HH_um - 10.0)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFF7F;
END_IF;

(* Bit 8: Chiller Coolant Low-Low Flow E-Stop Trip (< 8 L/min) *)
IF (rChillerFlowRate_Lpm <= rChillerFlowRate_LL_Lpm) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000100;
ELSIF bReset OR (rChillerFlowRate_Lpm > (rChillerFlowRate_LL_Lpm + 2.0)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFEFF;
END_IF;

(* Bit 9: Chiller Coolant Low Flow Warning (< 15 L/min) *)
IF (rChillerFlowRate_Lpm <= rChillerFlowRate_L_Lpm) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000200;
ELSIF bReset OR (rChillerFlowRate_Lpm > (rChillerFlowRate_L_Lpm + 2.0)) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFDFF;
END_IF;

(* Bit 10: Spindle Delta-T Excessive Deviation (> 1.2 deg C from Bed) *)
IF (ABS(rEstimatedSpindleDeltaT_degC) >= 1.20) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 OR 16#00000400;
ELSIF bReset OR (ABS(rEstimatedSpindleDeltaT_degC) < 0.30) THEN
    dwIsaAlarmWord1 := dwIsaAlarmWord1 AND 16#FFFFFBFF;
END_IF;

(* ------------------------------------------------------------------------------------------
   ISA-18.2 ALARM WORD 2: ATC, MECHANICAL & FLUID SYSTEMS TRIPS (PRIORITY 2 & 3)
   ------------------------------------------------------------------------------------------ *)
(* Bit 0: CRITICAL SAFETY INTERLOCK: Spindle Unclamp Attempted While Rotating (> 5 RPM) *)
IF bDrawbarUnclampCommand AND (rSpindleActualSpeed_RPM > 5.0) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000001;
    nFsmState       := 120; (* Immediate E-Stop Lockout! *)
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFFE;
END_IF;

(* Bit 1: Drawbar Unclamp Stroke LVDT Out-of-Tolerance Failure *)
IF (nFsmState = 75) AND (NOT bDrawbarStrokeInTolerance) AND (rStateTimer_s > 1.2) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000002;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFFD;
END_IF;

(* Bit 2: Drawbar Clamp Stroke LVDT Out-of-Tolerance Failure *)
IF (nFsmState = 85) AND (NOT bDrawbarStrokeInTolerance) AND (rStateTimer_s > 1.2) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000004;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFFB;
END_IF;

(* Bit 3: Non-Contact Laser Broken Tool Inspection Tripped *)
IF bToolBrokenAlarm THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000008;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFF7;
END_IF;

(* Bit 4: Taper Purge Air Pressure Low Warning (< 4.5 bar) *)
IF (rTaperPurgeAirPressure_bar < 4.50) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000010;
ELSIF bReset OR (rTaperPurgeAirPressure_bar >= 5.00) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFEF;
END_IF;

(* Bit 5: Bearing Micro-Lubrication Air Pressure Low (< 2.2 bar) *)
IF (rLubricationAirPressure_bar < 2.20) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000020;
ELSIF bReset OR (rLubricationAirPressure_bar >= 2.80) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFDF;
END_IF;

(* Bit 6: Spindle Nose Sealing Air Pressure Low (< 0.35 bar) *)
IF (rSealingAirPressure_bar < 0.35) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000040;
ELSIF bReset OR (rSealingAirPressure_bar >= 0.45) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFFBF;
END_IF;

(* Bit 7: Magazine Matrix Pocket Mechanical Shot-Pin Timeout *)
IF (nFsmState = 55) AND (rStateTimer_s >= 1.80) AND (NOT bMagazinePocketLocked) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000080;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFF7F;
END_IF;

(* Bit 8: ATC Shutter Protective Door Interlock Failure *)
IF (nFsmState = 60) AND (rStateTimer_s >= 2.20) AND (NOT bAtcShutterDoorOpened) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000100;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFEFF;
END_IF;

(* Bit 9: Dual-Gripper Arm Mechanical Cam Indexer Timeout *)
IF (nFsmState = 70) AND (rStateTimer_s >= 1.80) AND ((NOT bAtcGripper1ToolClamped) OR (NOT bAtcGripper2ToolClamped)) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000200;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFDFF;
END_IF;

(* Bit 10: Tool Missing or Unseated in Spindle Taper *)
IF (nFsmState = 85) AND (NOT bToolPresentInSpindle) AND (rStateTimer_s > 1.0) THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 OR 16#00000400;
ELSIF bReset THEN
    dwIsaAlarmWord2 := dwIsaAlarmWord2 AND 16#FFFFFBFF;
END_IF;

(* ------------------------------------------------------------------------------------------
   ISA-18.2 ALARM WORD 3: 2oo3 TMR SENSOR DISCREPANCY & CHANNEL FAULTS (PRIORITY 4)
   ------------------------------------------------------------------------------------------ *)
IF bHousing_DiscAlarm_A  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000001; END_IF;
IF bHousing_DiscAlarm_B  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000002; END_IF;
IF bHousing_DiscAlarm_C  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000004; END_IF;
IF (nTmrDegradedModeHousing = 0) THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000008; END_IF;

IF bFrontBrg_DiscAlarm_A THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000010; END_IF;
IF bFrontBrg_DiscAlarm_B THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000020; END_IF;
IF bFrontBrg_DiscAlarm_C THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000040; END_IF;
IF (nTmrDegradedModeFrontBrg = 0) THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000080; END_IF;

IF bRearBrg_DiscAlarm_A  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000100; END_IF;
IF bRearBrg_DiscAlarm_B  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000200; END_IF;
IF bRearBrg_DiscAlarm_C  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000400; END_IF;
IF (nTmrDegradedModeRearBrg = 0) THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00000800; END_IF;

IF bCapNose_DiscAlarm_A  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00001000; END_IF;
IF bCapNose_DiscAlarm_B  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00002000; END_IF;
IF bCapNose_DiscAlarm_C  THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00004000; END_IF;
IF (nTmrDegradedModeCapNose = 0) THEN dwIsaAlarmWord3 := dwIsaAlarmWord3 OR 16#00008000; END_IF;

IF bReset THEN
    dwIsaAlarmWord3 := 16#00000000;
END_IF;

(* ------------------------------------------------------------------------------------------
   MACHINE STATUS WORD PACKING
   ------------------------------------------------------------------------------------------ *)
dwMachineStatusWord := 16#00000000;
dwMachineStatusWord := dwMachineStatusWord OR INT_TO_DWORD(nFsmState AND 16#00FF);
IF bSpindleReadyForCut         THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00000100; END_IF;
IF bWarmupInProgress           THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00000200; END_IF;
IF bWarmupComplete             THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00000400; END_IF;
IF bThermalEquilibriumAchieved THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00000800; END_IF;
IF bToolChangeInProgress       THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00001000; END_IF;
IF bToolChangeComplete         THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00002000; END_IF;
IF bToolBrokenAlarm            THEN dwMachineStatusWord := dwMachineStatusWord OR 16#00004000; END_IF;
IF (nTmrDegradedModeHousing < 3) OR (nTmrDegradedModeFrontBrg < 3) OR
   (nTmrDegradedModeRearBrg < 3) OR (nTmrDegradedModeCapNose < 3) THEN
    dwMachineStatusWord := dwMachineStatusWord OR 16#00008000; (* Sensor TMR Degraded Mode Active *)
END_IF;
dwMachineStatusWord := dwMachineStatusWord OR SHL(INT_TO_DWORD(nCurrentSpindleTool AND 16#00FF), 16);

(* Interlock Trip to Emergency Lockout if Priority 1 Alarm Active *)
IF ((dwIsaAlarmWord1 AND 16#00000155) <> 16#00000000) OR
   ((dwIsaAlarmWord2 AND 16#0000000B) <> 16#00000000) THEN
    nFsmState := 120;
END_IF;

END_FUNCTION_BLOCK
""")

    code_str = "".join(parts)
    return code_str

def main():
    code_body = build_code()
    full_content = "```iec-st\n" + code_body.strip() + "\n```"
    
    print(f"Generated ST code character count: {len(full_content)}")
    
    # Run in-memory validation
    errs = validate_iec.validate_iec_st(code_body)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        return False
    else:
        print("IN-MEMORY VALIDATION PASSED!")

    # Write JSON record
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": full_content}
        ]
    }
    
    out_path = "data/swarm_raw/agent_6f90123a.json"
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Saved dataset successfully to {out_path}")
    
    # Validate written file
    file_errs = validate_iec.validate_json_file(out_path)
    if file_errs:
        print("FILE VALIDATION ERRORS:")
        for e in file_errs:
            print(" -", e)
        return False
    else:
        print("FILE VALIDATION PASSED COMPLETELY!")
        return True

if __name__ == "__main__":
    main()
