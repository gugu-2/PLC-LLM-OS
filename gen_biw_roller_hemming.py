# gen_biw_roller_hemming.py - Complete generator for FB_Automotive_BIW_RollerHemming_DoorClosure
import os
import json
import uuid
import re

def build_roller_hemming_dataset():
    lines = []
    
    # Line 1 must be FUNCTION_BLOCK FB_Automotive_BIW_RollerHemming_DoorClosure
    lines.append("FUNCTION_BLOCK FB_Automotive_BIW_RollerHemming_DoorClosure")
    
    # Architectural Header Comment
    lines.append("""(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-AUTO-BIW-HEM-ROBCELL-DUAL6AXIS-FORCE-LASER-V7
  DOMAIN ASSIGNMENT: Automotive & BIW Closures: Multi-Robot Synchronized Roller Hemming Cell for Car Doors & Hoods
  PRIMARY FUNCTION: Dynamic Normal Force Regulation, Sheet Metal Springback Suppression & Laser Seam Profiling
========================================================================================================================
  SUBSYSTEM ARCHITECTURE & PHYSICAL PROCESS DERIVATIONS:
    1. Dual 6-Axis Industrial Robots (Leading Robot 1 Upper Contour, Trailing Robot 2 Lower Contour)
       Synchronized toolpath motion with dynamic corner feedrate pacing along complex 3D door perimeter.
    2. Multi-Roller Hemming Head with Automated Indexing Turret:
       - Roller Station 1: Pre-Hemming Roll (Conical 45 deg Flange Bending)
       - Roller Station 2: Final Hemming Roll (Cylindrical 0 deg Flat Compression)
       - Roller Station 3: Corner Specialty Coin Roll (Spherical Crown for Tight Corner Radii R < 15 mm)
    3. Active Toolholder Compliance Actuation:
       Pneumatic/Piezoelectric high-frequency normal force regulation loop maintaining contact normal force
       (Pre-hem nominal 1,500 N [1,200 - 1,800 N], Final hem nominal 2,800 N [2,200 - 3,200 N] +/- 50 N).
    4. Elastic-Plastic Bending Deformation & Springback Mechanics:
       Continuous formulation for outer automotive skin (AA6016-T4 Aluminum / BH210 Bake Hardening Steel)
       accounting for plastic moment curvature, tangent modulus, neutral axis shift, and angular springback:
       Delta_Theta = Theta_0 * ( 1 - 3*(sigma_y * R_curv)/(E * t) + 4*((sigma_y * R_curv)/(E * t))^3 ).
    5. Part Nesting Fixture Tooling:
       - Multi-point vacuum suction cups with 2oo3 manifold vacuum transducer voting (-0.85 bar nominal).
       - 16-point pneumatic toggle edge clamps with dual inductive position confirmation.
       - 4-point servo-driven locating pins with precision linear encoders (+/- 0.05 mm repeatability).
       - In-plane sheet metal slippage detection using redundant high-resolution LVDTs.
    6. In-Line Optical Triangulation Laser Profiler:
       - Real-time seam profile measurement at 1 kHz: hem thickness (target 2.20 mm +/- 0.10 mm),
         gap width (target 3.50 mm +/- 0.50 mm), flushness (target 0.00 mm +/- 0.40 mm), and roll-in/roll-out.
    7. Cyber-Physical Discrete State-Space Model:
       16-State State Transition Matrix (A: 16x16), Input Coupling Matrix (B: 16x8), Output Matrix (C: 8x16),
       and Feedthrough Matrix (D: 8x8) governing robot arm structural compliance, roller contact Hertzian stiffness,
       sheet metal plastic moment, adhesive squeeze-out flow, and pneumatic compliance cylinder response.
    8. Receding-Horizon Model Predictive Control (MPC):
       Unrolled quadratic cost minimization with diagonal state weight Q (16x16), input weight R (8x8),
       rate penalty S (8x8), terminal cost P (16x16), and box-constrained gradient descent optimization.
    9. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite:
       Redundant voting across Robot 1 force load cells, Robot 2 force load cells, vacuum pressure switches,
       fixture part slippage LVDTs, and laser seam thickness profilers with bumpless degradation.
   10. 12-Stage Operational Finite State Machine (FSM):
       Stage 1: Inner/Outer Panel Nesting Infeed Verification
       Stage 2: Servo Pin Locating, Vacuum Cup Pull-down & Toggle Clamping
       Stage 3: Dual Robot Approach, Flange Datum Alignment & Search
       Stage 4: Pre-Hemming Pass (45 Deg) Trajectory Execution with Force Regulation
       Stage 5: Tool Head Automatic Roller Turret Indexing
       Stage 6: Final Hemming Pass (0 Deg) Full Force Compression Execution
       Stage 7: Corner Specialty Hemming Coin & Sharp Radius Pacing
       Stage 8: In-Line Optical Laser Triangulation Gap/Flushness/Thickness Scan
       Stage 9: Fixture Clamp Depressurization, Vacuum Release & Part Lifter Upstroke
       Stage 10: Finished Door Transfer to Assembly Conveyor
       Stage 11: Roller Bearing Lubrication & Cleaning Wipe
       Stage 12: Emergency E-Stop Fast Tool Retract
   11. ISA-18.2 Multi-Tiered Alarm Matrix and Bit-Packed Diagnostic Telemetry:
       Four-tiered process alarms (LL, L, H, HH) with hysteresis deadbands, priority escalation,
       and real-time bit packing into 32-bit status and diagnostic DWORD registers.
========================================================================================================================

                  AUTOMOTIVE BIW ROLLER HEMMING CELL - MECHATRONIC TOPOLOGY
                  
                     +-------------------------------------------------------+
                     |    MASTER LINE PLC / CELL COORDINATION CONTROLLER     |
                     |  Safety Zone PLC (ISO 13849-1 Cat 4 / PL e Interlock) |
                     +---------------------------+---------------------------+
                                                 | Industrial Real-Time Ethernet
                                                 V
         +===============================================================================+
         |               BIW DOOR ROLLER HEMMING GEOMETRIC NESTING FIXTURE               |
         |  - 4x Servo Locating Pins (X/Y datum +/-0.05 mm)                              |
         |  - 8-Zone High-Flow Vacuum Manifold (-0.85 bar)                               |
         |  - 16x Toggle Power Clamps with Integrated Inductive Proximity Sensors        |
         |  - 3x Redundant LVDT Sheet Slippage Transducers                               |
         +===============================================================================+
                    |                                                         |
         Leading Robot Arm Path                                   Trailing Robot Arm Path
                    V                                                         V
     +----------------------------------+                      +----------------------------------+
     |   ROBOT 1 (UPPER SASH CONTOUR)   |                      |  ROBOT 2 (LOWER FLANGE CONTOUR)  |
     | 6-Axis High-Rigidity Articulated |                      | 6-Axis High-Rigidity Articulated |
     | Multi-Roller Hemming Head:       |                      | Multi-Roller Hemming Head:       |
     |  [45 Pre-Hem | 0 Final | Coin]   |                      |  [45 Pre-Hem | 0 Final | Coin]   |
     | Piezo-Pneumatic Active Compliance|                      | Piezo-Pneumatic Active Compliance|
     | 3-Ch Redundant Force Load Cell   |                      | 3-Ch Redundant Force Load Cell   |
     | Blue Laser Triangulation Profiler|                      | Blue Laser Triangulation Profiler|
     +----------------------------------+                      +----------------------------------+
                    |                                                         |
                    +--------------------+               +--------------------+
                                         |               |
                                         V               V
         +===============================================================================+
         |                   CONTINUOUS CYBER-PHYSICAL HEMMING ZONE                      |
         |  - Hemming Normal Force: Pre-Hem 1500 N (+/-50 N) -> Final Hem 2800 N (+/-50 N)|
         |  - Corner Deceleration: Feedrate 350 mm/s -> 60 mm/s when Corner Radius < 15mm |
         |  - Sheet Elastic-Plastic Bending & AA6016 Springback Active Angle Over-Bending |
         |  - Real-Time Seam Profile: Thickness 2.20 mm +/-0.10 mm, Gap 3.50 mm +/-0.50mm|
         +===============================================================================+
*)""")

    # VAR_INPUT Block
    lines.append("""VAR_INPUT
    (* Master Safety & System Automation Signals *)
    bMasterEnable                   : BOOL;    (* Master Cell Automation Run Permit [TRUE/FALSE] *)
    bSafetyFenceInterlockOK         : BOOL;    (* Perimeter Safety Light Curtain & Access Gate Chain [TRUE/FALSE] *)
    bEmergencyStopHealthy           : BOOL;    (* Redundant Emergency Stop Circuit Relay Contact Status [TRUE/FALSE] *)
    bAcknowledgeFaults              : BOOL;    (* Global Operator HMI Fault Reset & Alarm Silence Command [TRUE/FALSE] *)
    bPartPresentInfeedSwitch        : BOOL;    (* Optical Inductive Sensor Sensing Unhemmed Door Assembly at Infeed [TRUE/FALSE] *)
    bTransferConveyorReady          : BOOL;    (* Downstream Body Assembly Transfer Shuttle Clearance Handshake [TRUE/FALSE] *)
    
    (* Process Parameters & Material Selection *)
    nSelectedMaterialRecipe         : INT;     (* Material Recipe: 1=AA6016-T4 Aluminum, 2=BH210 Bake Hardening Steel, 3=DX54D Deep Draw Steel [-] *)
    fDoorContourCurvature_invM      : REAL;    (* Real-time 3D Flange Edge Geometric Curvature (kappa = 1/R) [1/m] *)
    fOuterSkinThickness_mm          : REAL;    (* Nominal Thickness of Outer Stamped Skin Panel [mm] *)
    fInnerPanelThickness_mm         : REAL;    (* Nominal Thickness of Inner Door Structural Panel [mm] *)
    fScanCycleTime_ms               : REAL;    (* Deterministic Task Execution Interval [ms] *)
    fMainPneumaticPressure_bar      : REAL;    (* Tool Compliance Auxiliary Pneumatic Supply Line Pressure [bar] *)
    fFixtureClampPressure_bar       : REAL;    (* Pneumatic Header Pressure to 16-Point Toggle Clamps [bar] *)
    
    (* 2oo3 Redundant Sensor Channels - Robot 1 (Upper Sash) Normal Force Load Cells *)
    fRobot1_HemForceRaw_ChA_N       : REAL;    (* Robot 1 Hemming Normal Force Load Cell - Transducer Channel A [N] *)
    fRobot1_HemForceRaw_ChB_N       : REAL;    (* Robot 1 Hemming Normal Force Load Cell - Transducer Channel B [N] *)
    fRobot1_HemForceRaw_ChC_N       : REAL;    (* Robot 1 Hemming Normal Force Load Cell - Transducer Channel C [N] *)
    
    (* 2oo3 Redundant Sensor Channels - Robot 2 (Lower Flange) Normal Force Load Cells *)
    fRobot2_HemForceRaw_ChA_N       : REAL;    (* Robot 2 Hemming Normal Force Load Cell - Transducer Channel A [N] *)
    fRobot2_HemForceRaw_ChB_N       : REAL;    (* Robot 2 Hemming Normal Force Load Cell - Transducer Channel B [N] *)
    fRobot2_HemForceRaw_ChC_N       : REAL;    (* Robot 2 Hemming Normal Force Load Cell - Transducer Channel C [N] *)
    
    (* 2oo3 Redundant Sensor Channels - Fixture Vacuum System *)
    fFixtureVacuum_ChA_bar          : REAL;    (* Fixture Multi-Cup Manifold Vacuum Transducer Channel A [bar] *)
    fFixtureVacuum_ChB_bar          : REAL;    (* Fixture Multi-Cup Manifold Vacuum Transducer Channel B [bar] *)
    fFixtureVacuum_ChC_bar          : REAL;    (* Fixture Multi-Cup Manifold Vacuum Transducer Channel C [bar] *)
    
    (* 2oo3 Redundant Sensor Channels - Fixture Sheet Slippage LVDTs *)
    fFixturePartSlippage_ChA_mm     : REAL;    (* Nesting Fixture LVDT Part Slippage Sensor Channel A [mm] *)
    fFixturePartSlippage_ChB_mm     : REAL;    (* Nesting Fixture LVDT Part Slippage Sensor Channel B [mm] *)
    fFixturePartSlippage_ChC_mm     : REAL;    (* Nesting Fixture LVDT Part Slippage Sensor Channel C [mm] *)
    
    (* 2oo3 Redundant Sensor Channels - In-Line Optical Laser Profiler Hem Thickness *)
    fLaserHemThickness_ChA_mm       : REAL;    (* Optical Laser Triangulation Profiler Hem Thickness Channel A [mm] *)
    fLaserHemThickness_ChB_mm       : REAL;    (* Optical Laser Triangulation Profiler Hem Thickness Channel B [mm] *)
    fLaserHemThickness_ChC_mm       : REAL;    (* Optical Laser Triangulation Profiler Hem Thickness Channel C [mm] *)
    
    (* Robot Kinematic Feedback & Toolhead Diagnostics *)
    fRobot1_FeedrateActual_mms      : REAL;    (* Robot 1 Actual Tool Center Point Tangential Velocity [mm/s] *)
    fRobot2_FeedrateActual_mms      : REAL;    (* Robot 2 Actual Tool Center Point Tangential Velocity [mm/s] *)
    fLaserGapWidth_mm               : REAL;    (* Laser Profiler Measured Door-to-Frame Hem Margin Gap [mm] *)
    fLaserFlushness_mm              : REAL;    (* Laser Profiler Measured Outer Panel Surface Flushness Deviation [mm] *)
    fRollerBearingTemp_degC         : REAL;    (* Hemming Toolhead Roller Precision Spindle Bearing Temperature [deg C] *)
    bRobot1_PathMotionActive        : BOOL;    (* Robot 1 Motion Controller Path Interpolator Executing [TRUE/FALSE] *)
    bRobot2_PathMotionActive        : BOOL;    (* Robot 2 Motion Controller Path Interpolator Executing [TRUE/FALSE] *)
    bTurretIndexed_PreHem           : BOOL;    (* Toolhead Turret Proximity Sensor - Pre-Hem 45 Deg Roller Engaged [TRUE/FALSE] *)
    bTurretIndexed_FinalHem         : BOOL;    (* Toolhead Turret Proximity Sensor - Final 0 Deg Flat Roller Engaged [TRUE/FALSE] *)
    bTurretIndexed_Corner           : BOOL;    (* Toolhead Turret Proximity Sensor - Corner Coin Roller Engaged [TRUE/FALSE] *)
END_VAR""")

    # VAR_OUTPUT Block
    lines.append("""VAR_OUTPUT
    (* Cell Execution Status & Handshake Flags *)
    bCellHealthy                    : BOOL;    (* Roller Hemming Cell Global Operational Readiness Status [TRUE/FALSE] *)
    bCycleRunning                   : BOOL;    (* Hemming Automation Active Process Cycle Executing [TRUE/FALSE] *)
    bCycleComplete                  : BOOL;    (* Door Panel Closure Hemming Cycle Finished Strobe Pulse [TRUE/FALSE] *)
    nActiveFSM_Stage                : INT;     (* Current 12-Stage Hemming Sequence Execution Stage Index (1 to 12) [-] *)
    
    (* Dynamic Robot Actuator Commands & Trajectory Setpoints *)
    fRobot1_ForceSetpoint_N         : REAL;    (* Robot 1 Active Toolholder Normal Hemming Force Setpoint [N] *)
    fRobot2_ForceSetpoint_N         : REAL;    (* Robot 2 Active Toolholder Normal Hemming Force Setpoint [N] *)
    fRobot1_FeedrateOverride_pct    : REAL;    (* Robot 1 Trajectory Corner Velocity Scaling Dynamic Command [%] *)
    fRobot2_FeedrateOverride_pct    : REAL;    (* Robot 2 Trajectory Corner Velocity Scaling Dynamic Command [%] *)
    fRobot1_ToolAttackAngle_deg     : REAL;    (* Robot 1 Dynamic Springback Pre-Tilt Angle Actuation [deg] *)
    fRobot2_ToolAttackAngle_deg     : REAL;    (* Robot 2 Dynamic Springback Pre-Tilt Angle Actuation [deg] *)
    
    (* Tooling Fixture & Actuator Commands *)
    bFixtureVacuumValveCmd          : BOOL;    (* Solenoid Pilot Command for Fixture Vacuum Generator Venturi [TRUE/FALSE] *)
    bFixtureClampCylindersCmd       : BOOL;    (* Solenoid Pilot Command for 16-Point Toggle Edge Clamps [TRUE/FALSE] *)
    bFixtureLocatingPinsCmd         : BOOL;    (* Servo Pin Linear Positioning Actuator Engage Command [TRUE/FALSE] *)
    bFixtureLifterRaiseCmd          : BOOL;    (* Finished Door Panel Pneumatic Lifter Shuttle Upstroke Command [TRUE/FALSE] *)
    nRollerTurretIndexCmd           : INT;     (* Hemming Head Roller Turret Index: 1=PreHem 45deg, 2=Final 0deg, 3=Corner Coin [-] *)
    bAutoLubricationPulse           : BOOL;    (* High-Pressure Grease Dosing Pump Valve Pulse to Roller Spindle [TRUE/FALSE] *)
    bRollerCleaningAirKnife         : BOOL;    (* Compressed Air Sheet Clean Knife Blast for Swarf Removal [TRUE/FALSE] *)
    bLaserProfilerActiveScan        : BOOL;    (* Optical Blue Laser Seam Profiler Synchronized Trigger Enable [TRUE/FALSE] *)
    
    (* Process Quality Acceptance & Voted Sensor Diagnostics *)
    bHemQualityAccept               : BOOL;    (* Integrated Seam Quality Acceptance Verified Against Tolerances [TRUE/FALSE] *)
    bHemQualityReject               : BOOL;    (* Hem Thickness, Gap or Flushness Out-of-Tolerance Reject Strobe [TRUE/FALSE] *)
    fVotedHemForce_R1_N             : REAL;    (* 2oo3 TMR Voted Normal Contact Force for Robot 1 [N] *)
    fVotedHemForce_R2_N             : REAL;    (* 2oo3 TMR Voted Normal Contact Force for Robot 2 [N] *)
    fVotedVacuumPressure_bar        : REAL;    (* 2oo3 TMR Voted Fixture Vacuum Level [bar] *)
    fVotedPartSlippage_mm           : REAL;    (* 2oo3 TMR Voted Sheet Metal Slippage Displacement [mm] *)
    fVotedHemThickness_mm           : REAL;    (* 2oo3 TMR Voted In-Line Seam Hem Thickness [mm] *)
    
    (* Bit-Packed Industrial Telemetry & ISA-18.2 Alarms *)
    dwStatus_General                : DWORD;   (* Bit-Packed Operational State and Subsystem Handshake Telemetry [HEX] *)
    dwStatus_Robotics               : DWORD;   (* Bit-Packed Multi-Robot Motion Sync and Tool Turret Telemetry [HEX] *)
    dwAlarm_Process_HighHigh        : DWORD;   (* ISA-18.2 Critical High-High Process Violation Register [HEX] *)
    dwAlarm_Process_High            : DWORD;   (* ISA-18.2 Warning High Process Deviation Register [HEX] *)
    dwAlarm_Process_Low             : DWORD;   (* ISA-18.2 Warning Low Process Deviation Register [HEX] *)
    dwAlarm_Process_LowLow          : DWORD;   (* ISA-18.2 Critical Low-Low Process Violation Register [HEX] *)
    dwAlarm_Hardware_TMR            : DWORD;   (* Sensor Discrepancy & Voting Degradation Diagnostic Register [HEX] *)
END_VAR""")

    # VAR Block
    lines.append("""VAR
    (* Internal System Initialization Flag *)
    bInitialized                    : BOOL := FALSE;
    
    (* Discrete State-Space System Matrices (16 States x 16 States, 16 States x 8 Inputs) *)
    matA                            : ARRAY [1..16, 1..16] OF REAL; (* Discrete System Transition Matrix A *)
    matB                            : ARRAY [1..16, 1..8] OF REAL;  (* Discrete Control Input Matrix B *)
    matC                            : ARRAY [1..8, 1..16] OF REAL;  (* Discrete Output Measurement Matrix C *)
    matD                            : ARRAY [1..8, 1..8] OF REAL;   (* Discrete Direct Transmission Matrix D *)
    
    (* State Vectors & Optimization Registers *)
    arrState_x                      : ARRAY [1..16] OF REAL;        (* Current State Vector x[k] *)
    arrStatePred_x                  : ARRAY [1..16] OF REAL;        (* Predicted State Vector x[k+1] *)
    arrControl_u                    : ARRAY [1..8] OF REAL;         (* Control Input Vector u[k] *)
    arrControl_u_prev               : ARRAY [1..8] OF REAL;         (* Previous Control Input Vector u[k-1] *)
    arrOutput_y                     : ARRAY [1..8] OF REAL;         (* Predicted Process Output Vector y[k] *)
    arrGrad_J                       : ARRAY [1..8] OF REAL;         (* MPC Quadratic Cost Gradient Vector *)
    
    (* Receding-Horizon MPC Quadratic Cost Weighting Diagonal Matrices *)
    arrMPC_Q_diag                   : ARRAY [1..16] OF REAL;        (* State Deviation Penalty Diagonal Weights Q *)
    arrMPC_R_diag                   : ARRAY [1..8] OF REAL;         (* Actuator Effort Penalty Diagonal Weights R *)
    arrMPC_P_diag                   : ARRAY [1..16] OF REAL;        (* Terminal State Penalty Diagonal Weights P *)
    arrMPC_S_diag                   : ARRAY [1..8] OF REAL;         (* Actuator Slew Rate Penalty Diagonal Weights S *)
    
    (* Sheet Metal Plasticity & Springback Mechanics Parameters *)
    fMatYieldStrength_MPa           : REAL := 130.0;                (* Elastic Yield Strength sigma_y [MPa] *)
    fMatYoungsModulus_GPa           : REAL := 70.0;                 (* Elastic Modulus E [GPa] *)
    fMatTensileStrength_MPa         : REAL := 220.0;                (* Ultimate Tensile Strength sigma_uts [MPa] *)
    fNominalFlangeLength_mm         : REAL := 12.0;                 (* Standing Flange Width [mm] *)
    fTotalHemThicknessNominal_mm    : REAL := 2.20;                 (* Outer + Inner + Adhesive Nominal Pack Thickness [mm] *)
    fPlasticBendingMoment_Nmm       : REAL := 0.0;                  (* Fully Plastic Cross-Section Bending Moment [N*mm] *)
    fTheoreticalSpringback_deg      : REAL := 0.0;                  (* Elastic Angular Springback Recovery [deg] *)
    fActiveOverbendCompensation_deg : REAL := 0.0;                  (* Dynamic Tool Tilt Overbend Compensation [deg] *)
    fCurrentCurvatureRadius_mm      : REAL := 1000.0;               (* Real-Time Edge Radius of Curvature R = 1/kappa [mm] *)
    fCornerPacingVelocityFactor     : REAL := 1.0;                  (* Dynamic Corner Velocity Deceleration Scaling Factor *)
    fHertzianContactWidth_mm        : REAL := 0.0;                  (* Roller-to-Flange Hertzian Contact Patch Width [mm] *)
    fHertzianContactPressure_MPa    : REAL := 0.0;                  (* Peak Compressive Normal Pressure [MPa] *)
    
    (* Force Closed-Loop Regulation Registers *)
    fForceIntegral_R1               : REAL := 0.0;                  (* Robot 1 Normal Force Error Integral Accumulator [N*s] *)
    fForceIntegral_R2               : REAL := 0.0;                  (* Robot 2 Normal Force Error Integral Accumulator [N*s] *)
    fForcePropGain                  : REAL := 0.45;                 (* Force Loop Proportional Gain [N/N] *)
    fForceIntegGain                 : REAL := 1.25;                 (* Force Loop Integral Gain [N/(N*s)] *)
    fNominalForceRef_R1             : REAL := 1500.0;               (* Active Force Reference Setpoint Robot 1 [N] *)
    fNominalForceRef_R2             : REAL := 1500.0;               (* Active Force Reference Setpoint Robot 2 [N] *)
    
    (* 2oo3 TMR Voting Intermediate Variables & Discrepancy Diagnostics *)
    bTMR_R1Force_Degraded           : BOOL := FALSE;                (* Robot 1 Force 2oo3 Degraded to 1oo2 Status *)
    bTMR_R2Force_Degraded           : BOOL := FALSE;                (* Robot 2 Force 2oo3 Degraded to 1oo2 Status *)
    bTMR_Vacuum_Degraded            : BOOL := FALSE;                (* Fixture Vacuum 2oo3 Degraded to 1oo2 Status *)
    bTMR_Slippage_Degraded          : BOOL := FALSE;                (* Fixture Slippage 2oo3 Degraded to 1oo2 Status *)
    bTMR_Laser_Degraded             : BOOL := FALSE;                (* Laser Seam Profiler 2oo3 Degraded to 1oo2 Status *)
    fDev_R1Force_AB                 : REAL := 0.0;                  (* Channel A-B Load Cell Discrepancy Robot 1 [N] *)
    fDev_R1Force_BC                 : REAL := 0.0;                  (* Channel B-C Load Cell Discrepancy Robot 1 [N] *)
    fDev_R1Force_CA                 : REAL := 0.0;                  (* Channel C-A Load Cell Discrepancy Robot 1 [N] *)
    fDev_R2Force_AB                 : REAL := 0.0;                  (* Channel A-B Load Cell Discrepancy Robot 2 [N] *)
    fDev_R2Force_BC                 : REAL := 0.0;                  (* Channel B-C Load Cell Discrepancy Robot 2 [N] *)
    fDev_R2Force_CA                 : REAL := 0.0;                  (* Channel C-A Load Cell Discrepancy Robot 2 [N] *)
    fDev_Vacuum_AB                  : REAL := 0.0;                  (* Channel A-B Vacuum Discrepancy [bar] *)
    fDev_Vacuum_BC                  : REAL := 0.0;                  (* Channel B-C Vacuum Discrepancy [bar] *)
    fDev_Vacuum_CA                  : REAL := 0.0;                  (* Channel C-A Vacuum Discrepancy [bar] *)
    fDev_Slippage_AB                : REAL := 0.0;                  (* Channel A-B Slippage Discrepancy [mm] *)
    fDev_Slippage_BC                : REAL := 0.0;                  (* Channel B-C Slippage Discrepancy [mm] *)
    fDev_Slippage_CA                : REAL := 0.0;                  (* Channel C-A Slippage Discrepancy [mm] *)
    fDev_Laser_AB                   : REAL := 0.0;                  (* Channel A-B Laser Discrepancy [mm] *)
    fDev_Laser_BC                   : REAL := 0.0;                  (* Channel B-C Laser Discrepancy [mm] *)
    fDev_Laser_CA                   : REAL := 0.0;                  (* Channel C-A Laser Discrepancy [mm] *)
    
    (* 12-Stage Operational Finite State Machine Registers *)
    nFSM_State                      : INT := 0;                     (* Current Operational State Machine Index *)
    nFSM_PreviousState              : INT := 0;                     (* Preceding Cycle State Index for Transition Edge *)
    bFSM_StateEntry                 : BOOL := TRUE;                 (* Strobe Flag Indicating State Entry Cycle *)
    fFSM_StateElapsedTime_s         : REAL := 0.0;                  (* Accumulated Dwell Time in Current State [s] *)
    
    (* Industrial Timers for Multi-Stage Sequence & Fault Debounce *)
    tonFSM_StageTimer               : TON;                          (* General State Dwell Timekeeper *)
    tonVacuumPullDown               : TON;                          (* Fixture Vacuum Evacuation Dwell Timer *)
    tonClampLock                    : TON;                          (* Toggle Clamp Hydraulic/Pneumatic Lock Timer *)
    tonLocatingPins                 : TON;                          (* Precision Servo Pin Insertion Timer *)
    tonApproachDwell                : TON;                          (* Robot Seam Contact Approach Lead-in Timer *)
    tonPreHemTrajectory             : TON;                          (* Pre-Hemming 45 Deg Pass Duration Timer *)
    tonTurretIndex                  : TON;                          (* Toolhead Rotary Turret Indexing Dwell Timer *)
    tonFinalHemTrajectory           : TON;                          (* Final Hemming 0 Deg Flat Pass Duration Timer *)
    tonCornerCoinTrajectory         : TON;                          (* Corner Specialty Coin Pass Duration Timer *)
    tonLaserScanWindow              : TON;                          (* Laser Seam Profiler Traversal Inspection Window *)
    tonLifterUpstroke               : TON;                          (* Pneumatic Part Lifter Cylinder Traverse Timer *)
    tonTransferConveyor             : TON;                          (* Outfeed Assembly Conveyor Transfer Dwell *)
    tonLubePumpPulse                : TON;                          (* Bearing Automated Greasing Shot Timer *)
    tonAirKnifeBlow                 : TON;                          (* Compressed Air Roller Cleaning Knife Timer *)
    tonDiscrep_R1Force              : TON;                          (* Robot 1 Load Cell TMR Discrepancy Filter *)
    tonDiscrep_R2Force              : TON;                          (* Robot 2 Load Cell TMR Discrepancy Filter *)
    tonDiscrep_Vacuum               : TON;                          (* Vacuum Pressure TMR Discrepancy Filter *)
    tonDiscrep_Slippage             : TON;                          (* Part Slippage LVDT TMR Discrepancy Filter *)
    tonDiscrep_Laser                : TON;                          (* Laser Profiler TMR Discrepancy Filter *)
    tonAlarmDebounce_HH             : TON;                          (* Critical High-High Alarm Debounce Filter *)
    tonAlarmDebounce_LL             : TON;                          (* Critical Low-Low Alarm Debounce Filter *)
    
    (* Iterative Algorithm Index Counters & Math Registers *)
    nIdx_i                          : INT;                          (* Outer Loop Matrix Row Index *)
    nIdx_j                          : INT;                          (* Inner Loop Matrix Column Index *)
    nIdx_k                          : INT;                          (* Actuator Vector Loop Index *)
    nIdx_m                          : INT;                          (* Output Measurement Row Index *)
    fTempSum                        : REAL;                         (* Matrix Dot-Product Accumulator *)
    fTempGrad                       : REAL;                         (* Gradient Scalar Accumulator *)
    fGradStep                       : REAL;                         (* Gradient Descent Optimization Step Size *)
END_VAR""")

    # PHASE 0: Matrices Definition
    lines.append("""(* ==================================================================================================== *)
(* PHASE 0: COLD-START PARAMETER INITIALIZATION & SYSTEM MATRICES DEFINITION                           *)
(* ==================================================================================================== *)
IF NOT bInitialized THEN
    (* 0.1 Material Recipe Configuration: AA6016-T4 Aluminum vs BH210 / DX54D Steels *)
    IF nSelectedMaterialRecipe = 1 THEN
        (* AA6016-T4 Automotive Sheet Aluminum Outer Skin *)
        fMatYieldStrength_MPa := 130.0;
        fMatYoungsModulus_GPa := 70.0;
        fMatTensileStrength_MPa := 220.0;
    ELSIF nSelectedMaterialRecipe = 2 THEN
        (* BH210 Bake Hardening Steel Outer Skin *)
        fMatYieldStrength_MPa := 210.0;
        fMatYoungsModulus_GPa := 210.0;
        fMatTensileStrength_MPa := 340.0;
    ELSE
        (* DX54D Deep Drawing Automotive Grade Steel *)
        fMatYieldStrength_MPa := 160.0;
        fMatYoungsModulus_GPa := 205.0;
        fMatTensileStrength_MPa := 300.0;
    END_IF;

    (* 0.2 Discrete State-Space System Matrix matA (16x16) Initialization *)
    (* Governing robot arm compliance, Hertzian contact, plastic moment, vacuum, slippage & thermals *)""")

    state_names = [
        "x1: Robot 1 Normal Force Tracking Error [N]",
        "x2: Robot 1 Compliance Toolholder Displacement [mm]",
        "x3: Robot 1 Toolpath Tangential Velocity Error [mm/s]",
        "x4: Robot 1 Arm Flexural Deflection Mode [mm]",
        "x5: Robot 2 Normal Force Tracking Error [N]",
        "x6: Robot 2 Compliance Toolholder Displacement [mm]",
        "x7: Robot 2 Toolpath Tangential Velocity Error [mm/s]",
        "x8: Robot 2 Arm Flexural Deflection Mode [mm]",
        "x9: Outer Skin Plastic Bending Residual Strain [deg]",
        "x10: Sheet Metal Dynamic Springback Curvature Moment [N*mm]",
        "x11: Nesting Fixture Panel In-Plane Slippage [mm]",
        "x12: Fixture Vacuum Manifold Pressure Dynamics [bar]",
        "x13: Laser Measured Hem Seam Thickness Deviation [mm]",
        "x14: Laser Measured Outer Panel Flushness Deviation [mm]",
        "x15: Roller Bearing Thermal Viscous Heat Rise [deg C]",
        "x16: Adhesive Squeeze-Out Damping Dynamic Resistance [N]"
    ]

    for i in range(1, 17):
        for j in range(1, 17):
            if i == j:
                val = 0.8800 + ((i * 7) % 9) * 0.0100
            elif (i == 1 and j == 2) or (i == 5 and j == 6):
                val = 42.5000
            elif (i == 2 and j == 1) or (i == 6 and j == 5):
                val = -0.0018
            elif (i == 1 and j == 4) or (i == 5 and j == 8):
                val = 18.2500
            elif (i == 3 and j == 4) or (i == 7 and j == 8):
                val = 2.1500
            elif (i == 9 and j == 1) or (i == 9 and j == 5):
                val = 0.0042
            elif (i == 9 and j == 10):
                val = -0.0012
            elif (i == 10 and j == 9):
                val = 3.6500
            elif (i == 11 and j == 1) or (i == 11 and j == 5):
                val = 0.00015
            elif (i == 11 and j == 12):
                val = -0.0450
            elif (i == 13 and j == 1) or (i == 13 and j == 5):
                val = -0.00035
            elif (i == 13 and j == 9):
                val = 0.0280
            elif (i == 14 and j == 10):
                val = 0.0150
            elif (i == 14 and j == 11):
                val = 0.8500
            elif (i == 15 and j == 3) or (i == 15 and j == 7):
                val = 0.0035
            elif (i == 16 and j == 3) or (i == 16 and j == 7):
                val = 0.0850
            elif (i == 1 and j == 16) or (i == 5 and j == 16):
                val = 0.1250
            else:
                val = 0.0000

            comment = f"matA[{i},{j}]: {state_names[i-1][:24]} <- {state_names[j-1][:24]}"
            lines.append(f"    matA[{i}, {j}] := {val:.4f}; (* {comment} *)")

    lines.append("""
    (* 0.3 Discrete Control Input Matrix matB (16x8) Initialization *)
    (* Inputs: u1:R1_ForceBias, u2:R1_FeedScale, u3:R1_AttackAngle, u4:R2_ForceBias, u5:R2_FeedScale, u6:R2_AttackAngle, u7:VacuumBoost, u8:LubePulse *)""")

    input_names = [
        "u1: R1 Force Bias Command [N]",
        "u2: R1 Feedrate Speed Scaling [%]",
        "u3: R1 Tool Attack Tilt Angle [deg]",
        "u4: R2 Force Bias Command [N]",
        "u5: R2 Feedrate Speed Scaling [%]",
        "u6: R2 Tool Attack Tilt Angle [deg]",
        "u7: Vacuum Booster Throttle [%]",
        "u8: Bearing Lube/Cooling Valve [%]"
    ]

    for i in range(1, 17):
        for k in range(1, 9):
            if (i == 1 and k == 1) or (i == 5 and k == 4):
                val = 0.8500
            elif (i == 2 and k == 1) or (i == 6 and k == 4):
                val = 0.0045
            elif (i == 3 and k == 2) or (i == 7 and k == 5):
                val = 2.4500
            elif (i == 9 and k == 3) or (i == 9 and k == 6):
                val = 0.7800
            elif (i == 10 and k == 3) or (i == 10 and k == 6):
                val = -1.2500
            elif (i == 12 and k == 7):
                val = -0.0065
            elif (i == 15 and k == 8):
                val = -0.1500
            elif (i == 13 and k == 1) or (i == 13 and k == 4):
                val = -0.00025
            elif (i == 14 and k == 3) or (i == 14 and k == 6):
                val = -0.0450
            else:
                val = 0.0000

            comment = f"matB[{i},{k}]: {state_names[i-1][:22]} <- {input_names[k-1][:22]}"
            lines.append(f"    matB[{i}, {k}] := {val:.4f}; (* {comment} *)")

    lines.append("""
    (* 0.4 Discrete Output Measurement Matrix matC (8x16) Initialization *)
    (* Outputs: y1:R1_Force, y2:R2_Force, y3:FlangeAngle, y4:RetentionMargin, y5:HemThickness, y6:GapMargin, y7:BearingTemp, y8:Waviness *)""")

    output_names = [
        "y1: R1 Contact Normal Force [N]",
        "y2: R2 Contact Normal Force [N]",
        "y3: Residual Flange Hem Angle [deg]",
        "y4: Fixture Retention Margin [N]",
        "y5: Seam Hem Thickness [mm]",
        "y6: Outer Flange Seam Gap [mm]",
        "y7: Spindle Thermal State [deg C]",
        "y8: Seam Edge Waviness [mm]"
    ]

    for m in range(1, 9):
        for j in range(1, 17):
            if (m == 1 and j == 1) or (m == 2 and j == 5):
                val = 1.0000
            elif (m == 1 and j == 2) or (m == 2 and j == 6):
                val = 25.0000
            elif (m == 3 and j == 9):
                val = 1.0000
            elif (m == 3 and j == 10):
                val = 0.0850
            elif (m == 4 and j == 11):
                val = -500.0000
            elif (m == 4 and j == 12):
                val = -1200.0000
            elif (m == 5 and j == 13):
                val = 1.0000
            elif (m == 6 and j == 14):
                val = 1.0000
            elif (m == 7 and j == 15):
                val = 1.0000
            elif (m == 8 and j == 4) or (m == 8 and j == 8):
                val = 0.3500
            elif (m == 8 and j == 11):
                val = 0.5000
            else:
                val = 0.0000

            comment = f"matC[{m},{j}]: {output_names[m-1][:22]} <- {state_names[j-1][:22]}"
            lines.append(f"    matC[{m}, {j}] := {val:.4f}; (* {comment} *)")

    lines.append("""
    (* 0.5 Discrete Direct Feedthrough Matrix matD (8x8) Initialization *)""")

    for m in range(1, 9):
        for k in range(1, 9):
            if (m == 1 and k == 1) or (m == 2 and k == 4):
                val = 0.0500
            elif (m == 5 and k == 1) or (m == 5 and k == 4):
                val = -0.0001
            elif (m == 7 and k == 8):
                val = -0.0200
            else:
                val = 0.0000

            comment = f"matD[{m},{k}]: {output_names[m-1][:20]} <- {input_names[k-1][:20]}"
            lines.append(f"    matD[{m}, {k}] := {val:.4f}; (* {comment} *)")

    lines.append("""
    (* 0.6 Receding-Horizon MPC Quadratic Cost Diagonal Matrices Initialization *)
    (* Penalty weights: Q = State deviation, R = Actuator effort, P = Terminal, S = Slew rate *)""")

    q_weights = [12.5, 4.0, 2.5, 18.0, 12.5, 4.0, 2.5, 18.0, 25.0, 15.0, 45.0, 8.0, 35.0, 30.0, 1.5, 5.0]
    for i in range(1, 17):
        lines.append(f"    arrMPC_Q_diag[{i}] := {q_weights[i-1]:.2f}; (* Q[{i}]: Penalty for {state_names[i-1][:26]} *)")

    r_weights = [0.08, 0.15, 1.20, 0.08, 0.15, 1.20, 0.05, 0.02]
    for k in range(1, 9):
        lines.append(f"    arrMPC_R_diag[{k}] := {r_weights[k-1]:.2f}; (* R[{k}]: Actuator penalty {input_names[k-1][:24]} *)")

    for i in range(1, 17):
        p_val = q_weights[i-1] * 2.8
        lines.append(f"    arrMPC_P_diag[{i}] := {p_val:.2f}; (* P[{i}]: Terminal penalty {state_names[i-1][:26]} *)")

    s_weights = [0.25, 0.40, 3.50, 0.25, 0.40, 3.50, 0.10, 0.05]
    for k in range(1, 9):
        lines.append(f"    arrMPC_S_diag[{k}] := {s_weights[k-1]:.2f}; (* S[{k}]: Slew rate penalty {input_names[k-1][:24]} *)")

    lines.append("""
    (* Cold Start Initialization Latch *)
    bInitialized := TRUE;
END_IF;""")

    # PHASE 1: 2oo3 TMR Voting
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR HEALTH DIAGNOSTICS                   *)
(* ==================================================================================================== *)
(* 1.1 Robot 1 Hemming Force Load Cell 2oo3 Voting Suite *)
fDev_R1Force_AB := ABS(fRobot1_HemForceRaw_ChA_N - fRobot1_HemForceRaw_ChB_N);
fDev_R1Force_BC := ABS(fRobot1_HemForceRaw_ChB_N - fRobot1_HemForceRaw_ChC_N);
fDev_R1Force_CA := ABS(fRobot1_HemForceRaw_ChC_N - fRobot1_HemForceRaw_ChA_N);

tonDiscrep_R1Force(IN := (fDev_R1Force_AB > 120.0) OR (fDev_R1Force_BC > 120.0) OR (fDev_R1Force_CA > 120.0), PT := T#50MS);
IF tonDiscrep_R1Force.Q THEN
    bTMR_R1Force_Degraded := TRUE;
END_IF;

IF (fRobot1_HemForceRaw_ChA_N >= fRobot1_HemForceRaw_ChB_N AND fRobot1_HemForceRaw_ChA_N <= fRobot1_HemForceRaw_ChC_N) OR
   (fRobot1_HemForceRaw_ChA_N >= fRobot1_HemForceRaw_ChC_N AND fRobot1_HemForceRaw_ChA_N <= fRobot1_HemForceRaw_ChB_N) THEN
    fVotedHemForce_R1_N := fRobot1_HemForceRaw_ChA_N;
ELSIF (fRobot1_HemForceRaw_ChB_N >= fRobot1_HemForceRaw_ChA_N AND fRobot1_HemForceRaw_ChB_N <= fRobot1_HemForceRaw_ChC_N) OR
      (fRobot1_HemForceRaw_ChB_N >= fRobot1_HemForceRaw_ChC_N AND fRobot1_HemForceRaw_ChB_N <= fRobot1_HemForceRaw_ChA_N) THEN
    fVotedHemForce_R1_N := fRobot1_HemForceRaw_ChB_N;
ELSE
    fVotedHemForce_R1_N := fRobot1_HemForceRaw_ChC_N;
END_IF;

(* 1.2 Robot 2 Hemming Force Load Cell 2oo3 Voting Suite *)
fDev_R2Force_AB := ABS(fRobot2_HemForceRaw_ChA_N - fRobot2_HemForceRaw_ChB_N);
fDev_R2Force_BC := ABS(fRobot2_HemForceRaw_ChB_N - fRobot2_HemForceRaw_ChC_N);
fDev_R2Force_CA := ABS(fRobot2_HemForceRaw_ChC_N - fRobot2_HemForceRaw_ChA_N);

tonDiscrep_R2Force(IN := (fDev_R2Force_AB > 120.0) OR (fDev_R2Force_BC > 120.0) OR (fDev_R2Force_CA > 120.0), PT := T#50MS);
IF tonDiscrep_R2Force.Q THEN
    bTMR_R2Force_Degraded := TRUE;
END_IF;

IF (fRobot2_HemForceRaw_ChA_N >= fRobot2_HemForceRaw_ChB_N AND fRobot2_HemForceRaw_ChA_N <= fRobot2_HemForceRaw_ChC_N) OR
   (fRobot2_HemForceRaw_ChA_N >= fRobot2_HemForceRaw_ChC_N AND fRobot2_HemForceRaw_ChA_N <= fRobot2_HemForceRaw_ChB_N) THEN
    fVotedHemForce_R2_N := fRobot2_HemForceRaw_ChA_N;
ELSIF (fRobot2_HemForceRaw_ChB_N >= fRobot2_HemForceRaw_ChA_N AND fRobot2_HemForceRaw_ChB_N <= fRobot2_HemForceRaw_ChC_N) OR
      (fRobot2_HemForceRaw_ChB_N >= fRobot2_HemForceRaw_ChC_N AND fRobot2_HemForceRaw_ChB_N <= fRobot2_HemForceRaw_ChA_N) THEN
    fVotedHemForce_R2_N := fRobot2_HemForceRaw_ChB_N;
ELSE
    fVotedHemForce_R2_N := fRobot2_HemForceRaw_ChC_N;
END_IF;

(* 1.3 Fixture Multi-Cup Vacuum Pressure Transducers 2oo3 Voting Suite *)
fDev_Vacuum_AB := ABS(fFixtureVacuum_ChA_bar - fFixtureVacuum_ChB_bar);
fDev_Vacuum_BC := ABS(fFixtureVacuum_ChB_bar - fFixtureVacuum_ChC_bar);
fDev_Vacuum_CA := ABS(fFixtureVacuum_ChC_bar - fFixtureVacuum_ChA_bar);

tonDiscrep_Vacuum(IN := (fDev_Vacuum_AB > 0.08) OR (fDev_Vacuum_BC > 0.08) OR (fDev_Vacuum_CA > 0.08), PT := T#100MS);
IF tonDiscrep_Vacuum.Q THEN
    bTMR_Vacuum_Degraded := TRUE;
END_IF;

IF (fFixtureVacuum_ChA_bar >= fFixtureVacuum_ChB_bar AND fFixtureVacuum_ChA_bar <= fFixtureVacuum_ChC_bar) OR
   (fFixtureVacuum_ChA_bar >= fFixtureVacuum_ChC_bar AND fFixtureVacuum_ChA_bar <= fFixtureVacuum_ChB_bar) THEN
    fVotedVacuumPressure_bar := fFixtureVacuum_ChA_bar;
ELSIF (fFixtureVacuum_ChB_bar >= fFixtureVacuum_ChA_bar AND fFixtureVacuum_ChB_bar <= fFixtureVacuum_ChC_bar) OR
      (fFixtureVacuum_ChB_bar >= fFixtureVacuum_ChC_bar AND fFixtureVacuum_ChB_bar <= fFixtureVacuum_ChA_bar) THEN
    fVotedVacuumPressure_bar := fFixtureVacuum_ChB_bar;
ELSE
    fVotedVacuumPressure_bar := fFixtureVacuum_ChC_bar;
END_IF;

(* 1.4 Fixture In-Plane Part Slippage LVDT Transducers 2oo3 Voting Suite *)
fDev_Slippage_AB := ABS(fFixturePartSlippage_ChA_mm - fFixturePartSlippage_ChB_mm);
fDev_Slippage_BC := ABS(fFixturePartSlippage_ChB_mm - fFixturePartSlippage_ChC_mm);
fDev_Slippage_CA := ABS(fFixturePartSlippage_ChC_mm - fFixturePartSlippage_ChA_mm);

tonDiscrep_Slippage(IN := (fDev_Slippage_AB > 0.035) OR (fDev_Slippage_BC > 0.035) OR (fDev_Slippage_CA > 0.035), PT := T#80MS);
IF tonDiscrep_Slippage.Q THEN
    bTMR_Slippage_Degraded := TRUE;
END_IF;

IF (fFixturePartSlippage_ChA_mm >= fFixturePartSlippage_ChB_mm AND fFixturePartSlippage_ChA_mm <= fFixturePartSlippage_ChC_mm) OR
   (fFixturePartSlippage_ChA_mm >= fFixturePartSlippage_ChC_mm AND fFixturePartSlippage_ChA_mm <= fFixturePartSlippage_ChB_mm) THEN
    fVotedPartSlippage_mm := fFixturePartSlippage_ChA_mm;
ELSIF (fFixturePartSlippage_ChB_mm >= fFixturePartSlippage_ChA_mm AND fFixturePartSlippage_ChB_mm <= fFixturePartSlippage_ChC_mm) OR
      (fFixturePartSlippage_ChB_mm >= fFixturePartSlippage_ChC_mm AND fFixturePartSlippage_ChB_mm <= fFixturePartSlippage_ChA_mm) THEN
    fVotedPartSlippage_mm := fFixturePartSlippage_ChB_mm;
ELSE
    fVotedPartSlippage_mm := fFixturePartSlippage_ChC_mm;
END_IF;

(* 1.5 Optical Laser Seam Profiler Hem Thickness 2oo3 Voting Suite *)
fDev_Laser_AB := ABS(fLaserHemThickness_ChA_mm - fLaserHemThickness_ChB_mm);
fDev_Laser_BC := ABS(fLaserHemThickness_ChB_mm - fLaserHemThickness_ChC_mm);
fDev_Laser_CA := ABS(fLaserHemThickness_ChC_mm - fLaserHemThickness_ChA_mm);

tonDiscrep_Laser(IN := (fDev_Laser_AB > 0.060) OR (fDev_Laser_BC > 0.060) OR (fDev_Laser_CA > 0.060), PT := T#50MS);
IF tonDiscrep_Laser.Q THEN
    bTMR_Laser_Degraded := TRUE;
END_IF;

IF (fLaserHemThickness_ChA_mm >= fLaserHemThickness_ChB_mm AND fLaserHemThickness_ChA_mm <= fLaserHemThickness_ChC_mm) OR
   (fLaserHemThickness_ChA_mm >= fLaserHemThickness_ChC_mm AND fLaserHemThickness_ChA_mm <= fLaserHemThickness_ChB_mm) THEN
    fVotedHemThickness_mm := fLaserHemThickness_ChA_mm;
ELSIF (fLaserHemThickness_ChB_mm >= fLaserHemThickness_ChA_mm AND fLaserHemThickness_ChB_mm <= fLaserHemThickness_ChC_mm) OR
      (fLaserHemThickness_ChB_mm >= fLaserHemThickness_ChC_mm AND fLaserHemThickness_ChB_mm <= fLaserHemThickness_ChA_mm) THEN
    fVotedHemThickness_mm := fLaserHemThickness_ChB_mm;
ELSE
    fVotedHemThickness_mm := fLaserHemThickness_ChC_mm;
END_IF;""")

    # PHASE 2: State-Space Estimation & Propagation
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 2: STATE-SPACE ESTIMATION & DISCRETE TIME PROPAGATION                                         *)
(* ==================================================================================================== *)
(* 2.1 Physics Derivation: Elastic-Plastic Flange Moment, Curvature & Springback *)
IF fDoorContourCurvature_invM > 0.001 THEN
    fCurrentCurvatureRadius_mm := 1000.0 / fDoorContourCurvature_invM;
ELSE
    fCurrentCurvatureRadius_mm := 1000.0;
END_IF;

(* Plastic Moment: M_p = sigma_y * (w * t^2) / 4 *)
fPlasticBendingMoment_Nmm := fMatYieldStrength_MPa * (fNominalFlangeLength_mm * fOuterSkinThickness_mm * fOuterSkinThickness_mm) / 4.0;

(* Springback Formulation: Delta_Theta = Theta_0 * (1 - 3*(sigma_y*R)/(E*t) + 4*((sigma_y*R)/(E*t))^3) *)
IF (fMatYoungsModulus_GPa > 10.0) AND (fOuterSkinThickness_mm > 0.1) THEN
    fTheoreticalSpringback_deg := 45.0 * (1.0 - (3.0 * fMatYieldStrength_MPa * fCurrentCurvatureRadius_mm) / (fMatYoungsModulus_GPa * 1000.0 * fOuterSkinThickness_mm));
    IF fTheoreticalSpringback_deg < 0.0 THEN
        fTheoreticalSpringback_deg := 0.25;
    ELSIF fTheoreticalSpringback_deg > 6.5 THEN
        fTheoreticalSpringback_deg := 6.5;
    END_IF;
ELSE
    fTheoreticalSpringback_deg := 1.25;
END_IF;
fActiveOverbendCompensation_deg := fTheoreticalSpringback_deg * 1.12;

(* Hertzian Contact Patch Width: b = SQRT(4 * F * R_roller / (pi * E_eff)) *)
IF fVotedHemForce_R1_N > 50.0 THEN
    fHertzianContactWidth_mm := 0.045 * SQRT(fVotedHemForce_R1_N);
    fHertzianContactPressure_MPa := fVotedHemForce_R1_N / (fHertzianContactWidth_mm * 15.0 + 0.001);
ELSE
    fHertzianContactWidth_mm := 0.20;
    fHertzianContactPressure_MPa := 10.0;
END_IF;

(* 2.2 Assemble Continuous Physical Measurements into Discrete State Vector arrState_x *)
arrState_x[1] := fVotedHemForce_R1_N - fNominalForceRef_R1;
arrState_x[2] := (fVotedHemForce_R1_N / 350.0) - 4.28;
arrState_x[3] := fRobot1_FeedrateActual_mms - 250.0;
arrState_x[4] := 0.025 * SIN(fFSM_StateElapsedTime_s * 12.56);
arrState_x[5] := fVotedHemForce_R2_N - fNominalForceRef_R2;
arrState_x[6] := (fVotedHemForce_R2_N / 350.0) - 4.28;
arrState_x[7] := fRobot2_FeedrateActual_mms - 250.0;
arrState_x[8] := 0.022 * COS(fFSM_StateElapsedTime_s * 12.56);
arrState_x[9] := fActiveOverbendCompensation_deg - fTheoreticalSpringback_deg;
arrState_x[10] := fPlasticBendingMoment_Nmm * (fTheoreticalSpringback_deg / 45.0);
arrState_x[11] := fVotedPartSlippage_mm;
arrState_x[12] := fVotedVacuumPressure_bar - (-0.85);
arrState_x[13] := fVotedHemThickness_mm - fTotalHemThicknessNominal_mm;
arrState_x[14] := fLaserFlushness_mm;
arrState_x[15] := fRollerBearingTemp_degC - 35.0;
arrState_x[16] := (fRobot1_FeedrateActual_mms + fRobot2_FeedrateActual_mms) * 0.12;

(* 2.3 Discrete State Transition Propagation: x[k+1] = matA * x[k] + matB * u[k] *)
FOR nIdx_i := 1 TO 16 DO
    fTempSum := 0.0;
    FOR nIdx_j := 1 TO 16 DO
        fTempSum := fTempSum + (matA[nIdx_i, nIdx_j] * arrState_x[nIdx_j]);
    END_FOR;
    FOR nIdx_k := 1 TO 8 DO
        fTempSum := fTempSum + (matB[nIdx_i, nIdx_k] * arrControl_u[nIdx_k]);
    END_FOR;
    arrStatePred_x[nIdx_i] := fTempSum;
END_FOR;

(* 2.4 Measurement Output Matrix Propagation: y[k] = matC * x_pred[k+1] + matD * u[k] *)
FOR nIdx_m := 1 TO 8 DO
    fTempSum := 0.0;
    FOR nIdx_j := 1 TO 16 DO
        fTempSum := fTempSum + (matC[nIdx_m, nIdx_j] * arrStatePred_x[nIdx_j]);
    END_FOR;
    FOR nIdx_k := 1 TO 8 DO
        fTempSum := fTempSum + (matD[nIdx_m, nIdx_k] * arrControl_u[nIdx_k]);
    END_FOR;
    arrOutput_y[nIdx_m] := fTempSum;
END_FOR;""")

    # PHASE 3: Receding-Horizon MPC & Corner Pacing
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 3: RECEDING-HORIZON MPC CONTROL ACTION & TRAJECTORY CORNER PACING                             *)
(* ==================================================================================================== *)
(* 3.1 Receding-Horizon Projected Gradient Descent Optimizer *)
(* Cost Function: J = x^T * Q * x + u^T * R * u + delta_u^T * S * delta_u + x_N^T * P * x_N *)
FOR nIdx_k := 1 TO 8 DO
    fTempGrad := (2.0 * arrMPC_R_diag[nIdx_k] * arrControl_u[nIdx_k]) +
                 (2.0 * arrMPC_S_diag[nIdx_k] * (arrControl_u[nIdx_k] - arrControl_u_prev[nIdx_k]));
    FOR nIdx_i := 1 TO 16 DO
        fTempGrad := fTempGrad + (2.0 * matB[nIdx_i, nIdx_k] * arrMPC_Q_diag[nIdx_i] * arrStatePred_x[nIdx_i]);
    END_FOR;
    arrGrad_J[nIdx_k] := fTempGrad;
    
    (* Projected Gradient Step *)
    fGradStep := 0.0022 * arrGrad_J[nIdx_k];
    arrControl_u_prev[nIdx_k] := arrControl_u[nIdx_k];
    arrControl_u[nIdx_k] := arrControl_u[nIdx_k] - fGradStep;
END_FOR;

(* 3.2 Actuator Box Constraint Saturation *)
(* u1, u4: Normal Force Offset (-250.0 to +250.0 N) *)
IF arrControl_u[1] > 250.0 THEN arrControl_u[1] := 250.0; ELSIF arrControl_u[1] < -250.0 THEN arrControl_u[1] := -250.0; END_IF;
IF arrControl_u[4] > 250.0 THEN arrControl_u[4] := 250.0; ELSIF arrControl_u[4] < -250.0 THEN arrControl_u[4] := -250.0; END_IF;

(* u2, u5: Toolpath Feedrate Speed Scaling Factor (15.0 to 115.0 %) *)
IF arrControl_u[2] > 115.0 THEN arrControl_u[2] := 115.0; ELSIF arrControl_u[2] < 15.0 THEN arrControl_u[2] := 15.0; END_IF;
IF arrControl_u[5] > 115.0 THEN arrControl_u[5] := 115.0; ELSIF arrControl_u[5] < 15.0 THEN arrControl_u[5] := 15.0; END_IF;

(* u3, u6: Flange Overbend Attack Tilt Angle (-4.5 to +4.5 deg) *)
IF arrControl_u[3] > 4.5 THEN arrControl_u[3] := 4.5; ELSIF arrControl_u[3] < -4.5 THEN arrControl_u[3] := -4.5; END_IF;
IF arrControl_u[6] > 4.5 THEN arrControl_u[6] := 4.5; ELSIF arrControl_u[6] < -4.5 THEN arrControl_u[6] := -4.5; END_IF;

(* u7: Vacuum Booster Throttle (0.0 to 100.0 %) *)
IF arrControl_u[7] > 100.0 THEN arrControl_u[7] := 100.0; ELSIF arrControl_u[7] < 0.0 THEN arrControl_u[7] := 0.0; END_IF;

(* u8: Tool Lubrication Blast Valve (0.0 to 100.0 %) *)
IF arrControl_u[8] > 100.0 THEN arrControl_u[8] := 100.0; ELSIF arrControl_u[8] < 0.0 THEN arrControl_u[8] := 0.0; END_IF;

(* 3.3 Dynamic Corner Radius Feedrate Pacing (R < 15 mm) *)
IF fCurrentCurvatureRadius_mm < 15.0 THEN
    fCornerPacingVelocityFactor := fCurrentCurvatureRadius_mm / 15.0;
    IF fCornerPacingVelocityFactor < 0.22 THEN
        fCornerPacingVelocityFactor := 0.22;
    END_IF;
ELSE
    fCornerPacingVelocityFactor := 1.0;
END_IF;

(* 3.4 Active Normal Force PI Compensation *)
fForceIntegral_R1 := fForceIntegral_R1 + (fNominalForceRef_R1 - fVotedHemForce_R1_N) * (fScanCycleTime_ms * 0.001);
IF fForceIntegral_R1 > 400.0 THEN fForceIntegral_R1 := 400.0; ELSIF fForceIntegral_R1 < -400.0 THEN fForceIntegral_R1 := -400.0; END_IF;

fForceIntegral_R2 := fForceIntegral_R2 + (fNominalForceRef_R2 - fVotedHemForce_R2_N) * (fScanCycleTime_ms * 0.001);
IF fForceIntegral_R2 > 400.0 THEN fForceIntegral_R2 := 400.0; ELSIF fForceIntegral_R2 < -400.0 THEN fForceIntegral_R2 := -400.0; END_IF;

fRobot1_ForceSetpoint_N := fNominalForceRef_R1 + arrControl_u[1] +
                           (fForcePropGain * (fNominalForceRef_R1 - fVotedHemForce_R1_N)) +
                           (fForceIntegGain * fForceIntegral_R1);

fRobot2_ForceSetpoint_N := fNominalForceRef_R2 + arrControl_u[4] +
                           (fForcePropGain * (fNominalForceRef_R2 - fVotedHemForce_R2_N)) +
                           (fForceIntegGain * fForceIntegral_R2);

fRobot1_FeedrateOverride_pct := arrControl_u[2] * fCornerPacingVelocityFactor;
fRobot2_FeedrateOverride_pct := arrControl_u[5] * fCornerPacingVelocityFactor;

fRobot1_ToolAttackAngle_deg := arrControl_u[3] + fActiveOverbendCompensation_deg;
fRobot2_ToolAttackAngle_deg := arrControl_u[6] + fActiveOverbendCompensation_deg;""")

    # PHASE 4: 12-Stage Finite State Machine
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 4: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                             *)
(* ==================================================================================================== *)
IF NOT bEmergencyStopHealthy OR NOT bSafetyFenceInterlockOK THEN
    nFSM_State := 12; (* Emergency Fast Tool Retract *)
END_IF;

IF nFSM_State <> nFSM_PreviousState THEN
    bFSM_StateEntry := TRUE;
    fFSM_StateElapsedTime_s := 0.0;
    nFSM_PreviousState := nFSM_State;
ELSE
    bFSM_StateEntry := FALSE;
    fFSM_StateElapsedTime_s := fFSM_StateElapsedTime_s + (fScanCycleTime_ms * 0.001);
END_IF;

CASE nFSM_State OF
    0: (* ------------------------------------------------------------------------- *)
       (* STAGE 0: CELL IDLE & INITIALIZATION STANDBY                               *)
       (* ------------------------------------------------------------------------- *)
       bCellHealthy := TRUE;
       bCycleRunning := FALSE;
       bCycleComplete := FALSE;
       nActiveFSM_Stage := 0;
       bFixtureVacuumValveCmd := FALSE;
       bFixtureClampCylindersCmd := FALSE;
       bFixtureLocatingPinsCmd := FALSE;
       bFixtureLifterRaiseCmd := FALSE;
       nRollerTurretIndexCmd := 1;
       bAutoLubricationPulse := FALSE;
       bRollerCleaningAirKnife := FALSE;
       bLaserProfilerActiveScan := FALSE;
       bHemQualityAccept := FALSE;
       bHemQualityReject := FALSE;
       fNominalForceRef_R1 := 0.0;
       fNominalForceRef_R2 := 0.0;
       
       IF bMasterEnable AND bSafetyFenceInterlockOK AND bEmergencyStopHealthy THEN
           IF bPartPresentInfeedSwitch THEN
               nFSM_State := 1; (* Advance to Infeed Verification *)
           END_IF;
       END_IF;

    1: (* ------------------------------------------------------------------------- *)
       (* STAGE 1: INNER & OUTER PANEL NESTING INFEED VERIFICATION                  *)
       (* ------------------------------------------------------------------------- *)
       bCycleRunning := TRUE;
       bCycleComplete := FALSE;
       nActiveFSM_Stage := 1;
       bFixtureLifterRaiseCmd := FALSE;
       
       tonApproachDwell(IN := TRUE, PT := T#500MS);
       IF tonApproachDwell.Q THEN
           tonApproachDwell(IN := FALSE);
           IF bPartPresentInfeedSwitch AND (fVotedPartSlippage_mm < 0.08) THEN
               nFSM_State := 2; (* Advance to Fixture Engagement *)
           END_IF;
       END_IF;

    2: (* ------------------------------------------------------------------------- *)
       (* STAGE 2: SERVO PIN LOCATING, VACUUM PULL-DOWN & TOGGLE CLAMPING           *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 2;
       bFixtureLocatingPinsCmd := TRUE;
       bFixtureVacuumValveCmd := TRUE;
       
       tonVacuumPullDown(IN := TRUE, PT := T#800MS);
       IF tonVacuumPullDown.Q AND (fVotedVacuumPressure_bar < -0.75) THEN
           bFixtureClampCylindersCmd := TRUE;
           tonClampLock(IN := TRUE, PT := T#600MS);
           IF tonClampLock.Q AND (fFixtureClampPressure_bar > 5.2) THEN
               tonVacuumPullDown(IN := FALSE);
               tonClampLock(IN := FALSE);
               nFSM_State := 3; (* Advance to Robot Approach *)
           END_IF;
       END_IF;

    3: (* ------------------------------------------------------------------------- *)
       (* STAGE 3: DUAL ROBOT APPROACH, FLANGE DATUM ALIGNMENT & SEARCH             *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 3;
       nRollerTurretIndexCmd := 1; (* Pre-Hem 45 Deg Roller *)
       fNominalForceRef_R1 := 350.0; (* Light Touchdown Search Force *)
       fNominalForceRef_R2 := 350.0;
       
       tonApproachDwell(IN := TRUE, PT := T#1200MS);
       IF tonApproachDwell.Q THEN
           tonApproachDwell(IN := FALSE);
           IF bTurretIndexed_PreHem AND bRobot1_PathMotionActive AND bRobot2_PathMotionActive THEN
               nFSM_State := 4; (* Advance to Pre-Hemming Pass *)
           END_IF;
       END_IF;

    4: (* ------------------------------------------------------------------------- *)
       (* STAGE 4: PRE-HEMMING PASS (45 DEG) TRAJECTORY EXECUTION                   *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 4;
       nRollerTurretIndexCmd := 1;
       fNominalForceRef_R1 := 1500.0; (* Pre-Hemming Normal Force: 1,500 N Nominal *)
       fNominalForceRef_R2 := 1500.0;
       
       tonPreHemTrajectory(IN := TRUE, PT := T#4500MS);
       IF tonPreHemTrajectory.Q THEN
           tonPreHemTrajectory(IN := FALSE);
           IF (fVotedPartSlippage_mm < 0.12) AND NOT bRobot1_PathMotionActive THEN
               nFSM_State := 5; (* Advance to Roller Turret Indexing *)
           END_IF;
       END_IF;

    5: (* ------------------------------------------------------------------------- *)
       (* STAGE 5: TOOL HEAD AUTOMATIC ROLLER TURRET INDEXING (0 DEG FINAL)         *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 5;
       fNominalForceRef_R1 := 0.0;
       fNominalForceRef_R2 := 0.0;
       nRollerTurretIndexCmd := 2; (* Index to Final Hem 0 Deg Flat Roller *)
       
       tonTurretIndex(IN := TRUE, PT := T#1500MS);
       IF tonTurretIndex.Q THEN
           tonTurretIndex(IN := FALSE);
           IF bTurretIndexed_FinalHem THEN
               nFSM_State := 6; (* Advance to Final Hemming Pass *)
           END_IF;
       END_IF;

    6: (* ------------------------------------------------------------------------- *)
       (* STAGE 6: FINAL HEMMING PASS (0 DEG) FULL FORCE COMPRESSION EXECUTION      *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 6;
       nRollerTurretIndexCmd := 2;
       fNominalForceRef_R1 := 2800.0; (* Final Hemming Normal Force: 2,800 N Nominal *)
       fNominalForceRef_R2 := 2800.0;
       
       tonFinalHemTrajectory(IN := TRUE, PT := T#5500MS);
       IF tonFinalHemTrajectory.Q THEN
           tonFinalHemTrajectory(IN := FALSE);
           IF NOT bRobot1_PathMotionActive AND NOT bRobot2_PathMotionActive THEN
               nFSM_State := 7; (* Advance to Corner Specialty Coin *)
           END_IF;
       END_IF;

    7: (* ------------------------------------------------------------------------- *)
       (* STAGE 7: CORNER SPECIALTY HEMMING COIN & SHARP RADIUS PACING              *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 7;
       nRollerTurretIndexCmd := 3; (* Spherical Crown Coin Roller *)
       fNominalForceRef_R1 := 3200.0; (* Coining Pressure for Door Flange Corners *)
       fNominalForceRef_R2 := 3200.0;
       
       tonCornerCoinTrajectory(IN := TRUE, PT := T#2500MS);
       IF tonCornerCoinTrajectory.Q THEN
           tonCornerCoinTrajectory(IN := FALSE);
           IF NOT bRobot1_PathMotionActive THEN
               nFSM_State := 8; (* Advance to Optical Laser Inspection *)
           END_IF;
       END_IF;

    8: (* ------------------------------------------------------------------------- *)
       (* STAGE 8: IN-LINE OPTICAL LASER TRIANGULATION GAP/FLUSHNESS SCAN           *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 8;
       fNominalForceRef_R1 := 0.0;
       fNominalForceRef_R2 := 0.0;
       bLaserProfilerActiveScan := TRUE;
       
       tonLaserScanWindow(IN := TRUE, PT := T#2000MS);
       IF tonLaserScanWindow.Q THEN
           tonLaserScanWindow(IN := FALSE);
           bLaserProfilerActiveScan := FALSE;
           
           (* Seam Quality Acceptance Criteria:
              Hem Thickness: 2.20 mm +/- 0.12 mm
              Gap Width: 3.50 mm +/- 0.45 mm
              Flushness: 0.00 mm +/- 0.35 mm *)
           IF (fVotedHemThickness_mm >= 2.08) AND (fVotedHemThickness_mm <= 2.32) AND
              (fLaserGapWidth_mm >= 3.05) AND (fLaserGapWidth_mm <= 3.95) AND
              (ABS(fLaserFlushness_mm) <= 0.35) THEN
               bHemQualityAccept := TRUE;
               bHemQualityReject := FALSE;
               nFSM_State := 9; (* Advance to Fixture Release *)
           ELSE
               bHemQualityAccept := FALSE;
               bHemQualityReject := TRUE;
               nFSM_State := 9; (* Still release for reject staging *)
           END_IF;
       END_IF;

    9: (* ------------------------------------------------------------------------- *)
       (* STAGE 9: FIXTURE CLAMP RELEASE, VACUUM VENT & PART LIFTER UPSTROKE        *)
       (* ------------------------------------------------------------------------- *)
       nActiveFSM_Stage := 9;
       bFixtureClampCylindersCmd := FALSE;
       bFixtureVacuumValveCmd := FALSE;
       bFixtureLocatingPinsCmd := FALSE;
       
       tonLifterDwell(IN := TRUE, PT := T#1200MS);
       IF tonLifterDwell.Q THEN
           bFixtureLifterRaiseCmd := TRUE;
           tonApproachDwell(IN := TRUE, PT := T#1000MS);
           IF tonApproachDwell.Q THEN
               tonLifterDwell(IN := FALSE);
               tonApproachDwell(IN := FALSE);
               nFSM_State := 10; (* Advance to Transfer Conveyor *)
           END_IF;
       END_IF;

    10: (* ------------------------------------------------------------------------- *)
        (* STAGE 10: FINISHED DOOR TRANSFER TO ASSEMBLY CONVEYOR                     *)
        (* ------------------------------------------------------------------------- *)
        nActiveFSM_Stage := 10;
        
        tonTransferConveyor(IN := TRUE, PT := T#1800MS);
        IF tonTransferConveyor.Q THEN
            tonTransferConveyor(IN := FALSE);
            IF bTransferConveyorReady THEN
                bFixtureLifterRaiseCmd := FALSE;
                nFSM_State := 11; (* Advance to Roller Cleaning & Maintenance *)
            END_IF;
        END_IF;

    11: (* ------------------------------------------------------------------------- *)
        (* STAGE 11: ROLLER BEARING LUBRICATION & CLEANING AIR KNIFE WIPE            *)
        (* ------------------------------------------------------------------------- *)
        nActiveFSM_Stage := 11;
        bRollerCleaningAirKnife := TRUE;
        bAutoLubricationPulse := TRUE;
        
        tonLubePumpPulse(IN := TRUE, PT := T#1200MS);
        IF tonLubePumpPulse.Q THEN
            tonLubePumpPulse(IN := FALSE);
            bAutoLubricationPulse := FALSE;
            bRollerCleaningAirKnife := FALSE;
            bCycleComplete := TRUE;
            bCycleRunning := FALSE;
            nFSM_State := 0; (* Return to Idle / Standby *)
        END_IF;

    12: (* ------------------------------------------------------------------------- *)
        (* STAGE 12: EMERGENCY E-STOP FAST TOOL RETRACT & SAFE PARK                  *)
        (* ------------------------------------------------------------------------- *)
        bCellHealthy := FALSE;
        bCycleRunning := FALSE;
        nActiveFSM_Stage := 12;
        fNominalForceRef_R1 := 0.0;
        fNominalForceRef_R2 := 0.0;
        fRobot1_ForceSetpoint_N := 0.0;
        fRobot2_ForceSetpoint_N := 0.0;
        bFixtureVacuumValveCmd := TRUE; (* Maintain vacuum for safety hold *)
        bFixtureClampCylindersCmd := TRUE; (* Keep clamps locked *)
        bLaserProfilerActiveScan := FALSE;
        bAutoLubricationPulse := FALSE;
        bRollerCleaningAirKnife := FALSE;
        
        IF bAcknowledgeFaults AND bEmergencyStopHealthy AND bSafetyFenceInterlockOK THEN
            nFSM_State := 0; (* Reset to Idle *)
        END_IF;

ELSE
    nFSM_State := 0;
END_CASE;""")

    # PHASE 5: ISA-18.2 Alarms & Bit-Packing
    lines.append("""
(* ==================================================================================================== *)
(* PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & BIT-PACKED TELEMETRY DWORDS                                 *)
(* ==================================================================================================== *)
(* 5.1 Initialize Diagnostic Alarm Bit Registers *)
dwAlarm_Process_HighHigh := 16#00000000;
dwAlarm_Process_High     := 16#00000000;
dwAlarm_Process_Low      := 16#00000000;
dwAlarm_Process_LowLow   := 16#00000000;
dwAlarm_Hardware_TMR     := 16#00000000;

(* 5.2 ISA-18.2 Four-Tiered Alarm Trip Points & Latching *)
(* Pre-Hemming / Final Hemming Force Shortfall & Excess *)
IF nActiveFSM_Stage = 4 THEN
    (* Pre-Hem Phase Trip Points: LL < 1100 N, L < 1350 N, H > 1650 N, HH > 1950 N *)
    IF fVotedHemForce_R1_N < 1100.0 THEN dwAlarm_Process_LowLow := dwAlarm_Process_LowLow OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N < 1350.0 THEN dwAlarm_Process_Low    := dwAlarm_Process_Low    OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N > 1650.0 THEN dwAlarm_Process_High   := dwAlarm_Process_High   OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N > 1950.0 THEN dwAlarm_Process_HighHigh := dwAlarm_Process_HighHigh OR 16#00000001; END_IF;
ELSIF (nActiveFSM_Stage = 6) OR (nActiveFSM_Stage = 7) THEN
    (* Final Hem Phase Trip Points: LL < 2100 N, L < 2500 N, H > 3100 N, HH > 3500 N *)
    IF fVotedHemForce_R1_N < 2100.0 THEN dwAlarm_Process_LowLow := dwAlarm_Process_LowLow OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N < 2500.0 THEN dwAlarm_Process_Low    := dwAlarm_Process_Low    OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N > 3100.0 THEN dwAlarm_Process_High   := dwAlarm_Process_High   OR 16#00000001; END_IF;
    IF fVotedHemForce_R1_N > 3500.0 THEN dwAlarm_Process_HighHigh := dwAlarm_Process_HighHigh OR 16#00000001; END_IF;
END_IF;

(* Fixture Vacuum Level Alarms: LL > -0.65 bar (loss of vacuum), L > -0.75 bar *)
IF fVotedVacuumPressure_bar > -0.65 THEN
    dwAlarm_Process_LowLow := dwAlarm_Process_LowLow OR 16#00000004;
ELSIF fVotedVacuumPressure_bar > -0.75 THEN
    dwAlarm_Process_Low := dwAlarm_Process_Low OR 16#00000004;
END_IF;

(* Fixture Part In-Plane Slippage Alarms: H > 0.06 mm, HH > 0.12 mm *)
IF fVotedPartSlippage_mm > 0.12 THEN
    dwAlarm_Process_HighHigh := dwAlarm_Process_HighHigh OR 16#00000008;
ELSIF fVotedPartSlippage_mm > 0.06 THEN
    dwAlarm_Process_High := dwAlarm_Process_High OR 16#00000008;
END_IF;

(* Optical Laser Profiler Hem Thickness Alarms: LL < 1.95 mm, L < 2.08 mm, H > 2.32 mm, HH > 2.45 mm *)
IF fVotedHemThickness_mm < 1.95 THEN
    dwAlarm_Process_LowLow := dwAlarm_Process_LowLow OR 16#00000010;
ELSIF fVotedHemThickness_mm < 2.08 THEN
    dwAlarm_Process_Low := dwAlarm_Process_Low OR 16#00000010;
END_IF;
IF fVotedHemThickness_mm > 2.45 THEN
    dwAlarm_Process_HighHigh := dwAlarm_Process_HighHigh OR 16#00000010;
ELSIF fVotedHemThickness_mm > 2.32 THEN
    dwAlarm_Process_High := dwAlarm_Process_High OR 16#00000010;
END_IF;

(* Roller Bearing Precision Spindle Temperature Alarms: H > 70 deg C, HH > 85 deg C *)
IF fRollerBearingTemp_degC > 85.0 THEN
    dwAlarm_Process_HighHigh := dwAlarm_Process_HighHigh OR 16#00000020;
ELSIF fRollerBearingTemp_degC > 70.0 THEN
    dwAlarm_Process_High := dwAlarm_Process_High OR 16#00000020;
END_IF;

(* Main Auxiliary Pneumatic Supply Low Trip *)
IF fMainPneumaticPressure_bar < 4.8 THEN
    dwAlarm_Process_LowLow := dwAlarm_Process_LowLow OR 16#00000040;
END_IF;

(* 5.3 Hardware TMR Voting Degradation Diagnostic Packing *)
IF bTMR_R1Force_Degraded THEN
    dwAlarm_Hardware_TMR := dwAlarm_Hardware_TMR OR 16#00000001;
END_IF;
IF bTMR_R2Force_Degraded THEN
    dwAlarm_Hardware_TMR := dwAlarm_Hardware_TMR OR 16#00000002;
END_IF;
IF bTMR_Vacuum_Degraded THEN
    dwAlarm_Hardware_TMR := dwAlarm_Hardware_TMR OR 16#00000004;
END_IF;
IF bTMR_Slippage_Degraded THEN
    dwAlarm_Hardware_TMR := dwAlarm_Hardware_TMR OR 16#00000008;
END_IF;
IF bTMR_Laser_Degraded THEN
    dwAlarm_Hardware_TMR := dwAlarm_Hardware_TMR OR 16#00000010;
END_IF;

(* 5.4 General & Robotics Telemetry Status Packing *)
dwStatus_General := 16#00000000;
IF bCellHealthy THEN dwStatus_General := dwStatus_General OR 16#00000001; END_IF;
IF bCycleRunning THEN dwStatus_General := dwStatus_General OR 16#00000002; END_IF;
IF bCycleComplete THEN dwStatus_General := dwStatus_General OR 16#00000004; END_IF;
IF bHemQualityAccept THEN dwStatus_General := dwStatus_General OR 16#00000008; END_IF;
IF bHemQualityReject THEN dwStatus_General := dwStatus_General OR 16#00000010; END_IF;
IF bFixtureVacuumValveCmd THEN dwStatus_General := dwStatus_General OR 16#00000020; END_IF;
IF bFixtureClampCylindersCmd THEN dwStatus_General := dwStatus_General OR 16#00000040; END_IF;
IF bFixtureLocatingPinsCmd THEN dwStatus_General := dwStatus_General OR 16#00000080; END_IF;
IF bFixtureLifterRaiseCmd THEN dwStatus_General := dwStatus_General OR 16#00000100; END_IF;
IF bLaserProfilerActiveScan THEN dwStatus_General := dwStatus_General OR 16#00000200; END_IF;
IF bAutoLubricationPulse THEN dwStatus_General := dwStatus_General OR 16#00000400; END_IF;
IF bRollerCleaningAirKnife THEN dwStatus_General := dwStatus_General OR 16#00000800; END_IF;

dwStatus_Robotics := 16#00000000;
IF bRobot1_PathMotionActive THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000001; END_IF;
IF bRobot2_PathMotionActive THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000002; END_IF;
IF bTurretIndexed_PreHem THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000004; END_IF;
IF bTurretIndexed_FinalHem THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000008; END_IF;
IF bTurretIndexed_Corner THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000010; END_IF;
IF fCurrentCurvatureRadius_mm < 15.0 THEN dwStatus_Robotics := dwStatus_Robotics OR 16#00000020; END_IF;""")

    # Closing line
    lines.append("\nEND_FUNCTION_BLOCK")
    
    code = "\n".join(lines)
    return code

if __name__ == "__main__":
    code = build_roller_hemming_dataset()
    print(f"Total Structured Text generated length: {len(code)} characters")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Automotive & BIW Closures: Multi-Robot Synchronized Roller Hemming Cell for Car Doors & Hoods with Dynamic Normal Force Regulation & Laser Seam Profiling**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Automotive_BIW_RollerHemming_DoorClosure
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [N], [kN], [mm], [m/s], [deg], [bar], [deg C], [%], [1/m], [mm/s], [ms])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Automotive_BIW_RollerHemming_DoorClosure
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(\"data/swarm_raw/agent_7f8109db.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Automotive & BIW Closures: Multi-Robot Synchronized Roller Hemming Cell for Car Doors & Hoods with Dynamic Normal Force Regulation & Laser Seam Profiling"""

    assistant_content = f"```iec-st\n{code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    out_file = "data/swarm_raw/agent_7f8109db.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(assistant_content)} characters to {out_file}")
