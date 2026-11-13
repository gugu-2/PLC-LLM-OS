# -*- coding: utf-8 -*-
"""
smt_builder/header_io.py
Generates the FUNCTION_BLOCK declaration, comprehensive engineering documentation,
VAR_INPUT and VAR_OUTPUT blocks with physical SI units.
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Electronics_SMT_HighSpeed_PickAndPlace_VisionMotion
(*
========================================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - V7 MAX-PERSONA REFERENCE IMPLEMENTATION
  CORE INDUSTRY   : HIGH-SPEED ELECTRONICS MANUFACTURING & ADVANCED SMT PACKAGING (TIER 1 PRIORITY)
  SYSTEM TARGET   : DUAL-GANTRY 16-SPINDLE ULTRA-HIGH-SPEED SMT PICK-AND-PLACE ASSEMBLY CELL
  KINEMATICS      : CO-PLANAR DUAL-DRIVE LINEAR MOTOR GANTRY (X1/X2, Y1/Y2) WITH ACTIVE YAW COMPENSATION
  HEAD TOPOLOGY   : 16-SPINDLE REVOLVING STAR TURRET WITH INDIVIDUAL VOICE COIL Z-AXIS & DIRECT-DRIVE THETA
  VISION SUBSYSTEM: ON-THE-FLY HIGH-SPEED FLY-BY OPTICAL RECOGNITION WITH HARDWARE POSITION-COMPARE STROBE
  PNEUMATICS      : DYNAMIC PIEZORESISTIVE VACUUM SENSING (-85 kPa) & POSITIVE PRESSURE MICRO-BLOW-OFF RELEASE
  THERMAL CONTROL : MULTI-POINT INVAR/ZERODUR OPTICAL LINEAR SCALE THERMAL GRADIENT EXPANSION COMPENSATION
  SAFETY NORMS    : IEC 61508 / IEC 62061 SIL-3, ISO 13849-1 PLe CATEGORY 4 DUAL-CHANNEL SAFETY INTERLOCK
  PROCESS SPECS   : IPC-A-610 CLASS 3 HIGH RELIABILITY, IPC-7351B SMT LAND PATTERNS, IPC-9850 PLACEMENT ACCURACY
  THROUGHPUT SPEC : UP TO 100,000 CPH (COMPONENTS PER HOUR) PER DUAL-GANTRY SYSTEM WITH 36 ms COMPONENT CYCLE
  AUTHOR          : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  CYBER-PHYSICAL KINEMATICS, ELECTRO-PNEUMATIC & OPTICAL FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. DUAL-GANTRY LINEAR MOTOR KINEMATICS & RESONANT STRUCTURAL FLEXURE:
     - The high-speed SMT assembly platform utilizes dual parallel linear motor tracks for the X-axis (X1 primary and
       X2 secondary drives) spanning a length of 1,800 mm, with a cross-beam Y-axis driven by ironless core linear motors
       to eliminate magnetic cogging forces. The total moving payload of each gantry carriage, including the 16-spindle
       rotary placement head, optical vision optics, pneumatic manifolds, and cable carriers, equals M_total = 42.5 kg.
     - To achieve 100,000 CPH placement throughput across high-density mobile and automotive computing PCBAs, gantry
       translational accelerations reach up to a_max = 50.0 m/s^2 (5.1 g), with jerk rates bounded at j_max = 500.0 m/s^3.
     - At these aggressive dynamic kinematic levels, mechanical flexure between the optical linear encoder readhead on
       the carriage base and the actual tool-center-point (TCP) at the nozzle tip introduces structural vibration resonance:
           M_car * d^2(x_car)/dt^2 + C_flex * (d(x_car)/dt - d(x_tcp)/dt) + K_flex * (x_car - x_tcp) = F_linear_drive
           M_tcp * d^2(x_tcp)/dt^2 + C_flex * (d(x_tcp)/dt - d(x_car)/dt) + K_flex * (x_tcp - x_car) = -F_ext
       where K_flex = 2.45e7 N/m (structural stiffness) and C_flex = 820.0 N*s/m (damping coefficient).
     - Without active vibration dampening and model-based predictive state feedback, the residual vibration delta_tcp
       causes component placement offset errors exceeding +/- 65 um, far exceeding IPC Class 3 limits (+/- 25 um).

  2. 16-SPINDLE REVOLVING STAR TURRET HEAD & INDIVIDUAL VOICE COIL Z-AXIS MECHANICS:
     - The placement head consists of 16 identical pick-and-place spindles mounted radially on a high-precision rotary
       drum indexing turret. A central direct-drive torque motor indexes the head in 22.5 degree angular increments.
     - Each spindle incorporates:
       * An independent voice-coil linear actuator for Z-axis landing motion (0 to 30 mm stroke, 1.0 um position resolution).
         Voice-coil actuators provide frictionless, low-inertia direct drive, enabling programmable soft-touch landing
         impact forces adjustable between 0.5 N and 8.0 N (+/- 0.1 N precision) to prevent silicon die micro-cracking.
       * An independent hollow-shaft brushless direct-drive theta motor capable of continuous 360 degree rotation at
         up to 3,000 RPM with 0.001 degree optical encoder feedback for rotational component alignment.
       * An internal pneumatic vacuum and positive-pressure conduit routed through a frictionless rotary air union.

  3. ON-THE-FLY FLY-BY OPTICAL VISION INSPECTION & DYNAMIC OFFSET INJECTION:
     - Rather than stopping the placement head over an inspection camera, components are inspected "on-the-fly" as the
       gantry traverses from the feeder bank to the PCBA placement site at flight speeds up to v_flight = 2.5 m/s.
     - A gigabit Ethernet CMOS area-scan camera equipped with ultra-fast pulsed LED strobes (pulse duration 1.5 to 3.0 us)
       is triggered by a hardware Position Event Verification (PEV) comparator circuit matching linear encoder ticks.
     - Advanced sub-pixel blob and feature detection algorithms extract:
       * Centroid position translation errors: Delta_X_vision [mm] and Delta_Y_vision [mm]
       * Component rotational angular skew: Delta_Theta_vision [deg]
       * Micro-BGA solder ball array coplanarity and missing ball detection via structured laser line triangulation
       * Passive chip tombstoning, standing chips, bent QFP leads, and silicon die perimeter micro-chipping.
     - The calculated corrections (Delta_X, Delta_Y, Delta_Theta) are dynamically combined with the kinematic trajectory
       and injected into the linear motor servo loops and spindle theta motors before the head reaches the landing target.

  4. DYNAMIC PIEZORESISTIVE VACUUM SENSING & POSITIVE-PRESSURE BLOW-OFF DYNAMICS:
     - Each of the 16 spindles features a dedicated high-bandwidth piezoresistive pressure transducer (response time < 0.2 ms)
       monitoring vacuum suction chamber pressure. Process classification criteria:
       * Component Pick Failure / Dropped Component: P_vac > -20.0 kPa (insufficient differential pressure)
       * Tombstoning / Partial Seal Leak: -20.0 kPa >= P_vac > -52.0 kPa (air ingress around misaligned component)
       * Proper Seal / Component Securely Held: -52.0 kPa >= P_vac > -82.0 kPa (optimal retention force)
       * Clogged Nozzle Bore / Blocked Orifice: P_vac <= -82.0 kPa (debris in nozzle tip with or without part).
     - Component Release Dynamics: Solder paste surface tension and electrostatic stiction can cause components to adhere
       to the nozzle tip after vacuum release. The system fires a calibrated micro-pulse of positive blow-off pressure
       (+35.0 to +55.0 kPa, pulse duration 4.0 to 8.0 ms) immediately following voice-coil touchdown. The pressure decay
       profile is actively regulated to ensure clean component release without disturbing wet solder paste deposits.

  5. MULTI-POINT INVAR/ZERODUR OPTICAL LINEAR SCALE THERMAL COMPENSATION:
     - Linear motor coil heat dissipation (up to 1,200 W per axis under continuous 5g duty) and ambient cleanroom temperature
       swings induce thermal expansion across the cast-iron gantry base and ceramic encoder scales.
     - Four PT100 RTD temperature sensors measure:
       * T_scale_X1: Primary X-axis optical scale temperature [deg C]
       * T_scale_X2: Secondary X-axis optical scale temperature [deg C]
       * T_scale_Y : Cross-beam Y-axis optical scale temperature [deg C]
       * T_head    : Placement turret drum mounting plate temperature [deg C].
     - Real-time thermal expansion compensation applies first-principles linear and gradient expansion modeling:
           Delta_L_x = alpha_scale * L_x * (T_scale_X1 - T_ref) + 0.5 * beta_grad * (T_scale_X1 - T_scale_X2) * L_x
           Delta_L_y = alpha_scale * L_y * (T_scale_Y  - T_ref) + gamma_drum * (T_head - T_ref)
       where alpha_scale = 1.1e-6 /K (Invar scale CTE) and T_ref = 20.0 deg C. Compensations are applied every PLC cycle.
*)
VAR_INPUT
    (* Master Operational & Safety Commands *)
    bExecute_CycleStart             : BOOL;     (* System master automatic cycle start command [bool] *)
    bReset_Fault                    : BOOL;     (* Master fault reset and alarm clear command [bool] *)
    bEStop_SafetyInterlock          : BOOL;     (* Dual-channel hardware safety circuit status (TRUE = Healthy) [bool] *)
    bManualMode_Select              : BOOL;     (* Manual jog / maintenance calibration mode select [bool] *)
    bDryRun_NoParts_Enable          : BOOL;     (* Diagnostic dry-run mode without feeder pickup [bool] *)

    (* 2oo3 TMR Triplet 1: Gantry X-Axis Linear Optical Encoders (Renishaw 50 nm resolution) *)
    rEnc_Gantry_X_ChA               : REAL;     (* Gantry X-axis linear optical encoder Channel A [mm] *)
    rEnc_Gantry_X_ChB               : REAL;     (* Gantry X-axis linear optical encoder Channel B [mm] *)
    rEnc_Gantry_X_ChC               : REAL;     (* Gantry X-axis linear optical encoder Channel C [mm] *)

    (* 2oo3 TMR Triplet 2: Gantry Y-Axis Crossbeam Linear Optical Encoders *)
    rEnc_Gantry_Y_ChA               : REAL;     (* Gantry Y-axis linear optical encoder Channel A [mm] *)
    rEnc_Gantry_Y_ChB               : REAL;     (* Gantry Y-axis linear optical encoder Channel B [mm] *)
    rEnc_Gantry_Y_ChC               : REAL;     (* Gantry Y-axis linear optical encoder Channel C [mm] *)

    (* 2oo3 TMR Triplet 3: Spindle Turret Master Theta Encoders (Hollow-Shaft Rotary) *)
    rEnc_Head_Theta_ChA             : REAL;     (* 16-Spindle Head Master Theta rotary encoder Channel A [deg] *)
    rEnc_Head_Theta_ChB             : REAL;     (* 16-Spindle Head Master Theta rotary encoder Channel B [deg] *)
    rEnc_Head_Theta_ChC             : REAL;     (* 16-Spindle Head Master Theta rotary encoder Channel C [deg] *)

    (* 2oo3 TMR Triplet 4: Vacuum Manifold Differential Pressure Transducers *)
    rPT_VacuumManifold_ChA          : REAL;     (* Main vacuum distribution manifold pressure Channel A [kPa] *)
    rPT_VacuumManifold_ChB          : REAL;     (* Main vacuum distribution manifold pressure Channel B [kPa] *)
    rPT_VacuumManifold_ChC          : REAL;     (* Main vacuum distribution manifold pressure Channel C [kPa] *)

    (* 2oo3 TMR Triplet 5: Triangulation Laser PCB Surface Warpage Profile Gauges *)
    rLaser_WarpageHeight_ChA        : REAL;     (* Triangulation laser PCB surface warpage sensor Channel A [mm] *)
    rLaser_WarpageHeight_ChB        : REAL;     (* Triangulation laser PCB surface warpage sensor Channel B [mm] *)
    rLaser_WarpageHeight_ChC        : REAL;     (* Triangulation laser PCB surface warpage sensor Channel C [mm] *)

    (* Thermal Scale Expansion Sensor Network *)
    rTemp_LinearScale_X1            : REAL;     (* Primary X-axis Invar linear scale RTD temperature [deg C] *)
    rTemp_LinearScale_X2            : REAL;     (* Secondary X-axis Invar linear scale RTD temperature [deg C] *)
    rTemp_LinearScale_Y             : REAL;     (* Crossbeam Y-axis Invar linear scale RTD temperature [deg C] *)
    rTemp_SpindleDrum               : REAL;     (* 16-Spindle rotary turret drum core RTD temperature [deg C] *)

    (* Pneumatic Supply & Regulated Pressure Channels *)
    rSupplyAirPressure              : REAL;     (* Main pneumatic plant header inlet pressure [kPa] *)
    rBlowOffPositivePressure        : REAL;     (* Regulated positive pressure for puff blow-off release [kPa] *)
    rActiveSpindleVacuumPressure    : REAL;     (* Dynamic piezoresistive pressure of currently indexed spindle [kPa] *)

    (* On-the-Fly Fly-By Optical Vision System Interface *)
    bVision_TriggerAck              : BOOL;     (* Fly-by camera FPGA hardware trigger handshake pulse [bool] *)
    bVision_DataReady               : BOOL;     (* Fly-by optical vision processing complete & data ready [bool] *)
    rVision_OffsetX                 : REAL;     (* Vision measured component centroid offset dX [mm] *)
    rVision_OffsetY                 : REAL;     (* Vision measured component centroid offset dY [mm] *)
    rVision_OffsetTheta             : REAL;     (* Vision measured component rotational angular skew dTheta [deg] *)
    bVision_LeadCoplanarPass        : BOOL;     (* Vision component 3D lead coplanarity / BGA ball inspection pass [bool] *)
    bVision_DefectRejectFlag        : BOOL;     (* Vision defect classification (tombstone, chipped silicon, bent pin) [bool] *)

    (* Conveyor Clamping & PCB Alignment Status *)
    bConveyor_PCB_Clamped           : BOOL;     (* PCB conveyor dual-clamp lift table clamped and locked [bool] *)
    bGlobalFiducialsAligned         : BOOL;     (* PCB global optical fiducial marks acquired and board skew mapped [bool] *)
    rPCB_Global_SkewAngle           : REAL;     (* Measured PCB rotational mounting skew angle relative to conveyor [deg] *)

    (* Smart Tape Feeder Bank Interface *)
    bFeederBank_Ready               : BOOL;     (* Tape & reel electronic smart feeder bank ready & indexed [bool] *)
    bFeeder_TapeAdvanceDone         : BOOL;     (* Tape feeder micro-stepper advance pitch completed [bool] *)
    iFeeder_ComponentID             : INT;      (* Active feeder lane component part number identifier [id] *)

    (* Recipe Target CAD Coordinates for Current Placement Operation *)
    rTarget_Placement_X             : REAL;     (* Recipe target CAD placement coordinate X [mm] *)
    rTarget_Placement_Y             : REAL;     (* Recipe target CAD placement coordinate Y [mm] *)
    rTarget_Placement_Theta         : REAL;     (* Recipe target CAD placement angle Theta [deg] *)
    rTarget_Placement_Z             : REAL;     (* Recipe target CAD placement landing depth Z [mm] *)
    rNominalLandingForce            : REAL;     (* Programmable voice-coil landing touch force [N] *)
    rMaxAllowableZTouchdownSpeed    : REAL;     (* Maximum velocity allowed at nozzle component contact [mm/s] *)

    (* Task Timing *)
    tCycleDeltaT                    : TIME;     (* PLC cyclic task execution interval [ms] *)
END_VAR
VAR_OUTPUT
    (* Primary System Status & Handshakes *)
    bSystemReady                    : BOOL;     (* High-speed SMT placement block ready for production [bool] *)
    bCycleBusy                      : BOOL;     (* Placement cycle currently executing [bool] *)
    bCycleComplete                  : BOOL;     (* Placement batch / PCB complete handshake pulse [bool] *)
    bGeneralFault                   : BOOL;     (* System general trip / emergency condition active [bool] *)

    (* Multi-Axis Servo Actuator Command Outputs *)
    rCmd_Gantry_X_Force             : REAL;     (* Command force demand to Gantry X linear motor drive [N] *)
    rCmd_Gantry_Y_Force             : REAL;     (* Command force demand to Gantry Y linear motor drive [N] *)
    rCmd_Head_Theta_Torque          : REAL;     (* Command torque demand to Spindle Theta rotary servo drive [mN*m] *)
    rCmd_VoiceCoil_Z_Current        : REAL;     (* Command current demand to active spindle Z voice coil [mA] *)

    (* Pneumatic Solenoid & Fast Valve Commands *)
    rCmd_VacuumValve_PWM            : REAL;     (* Dynamic proportional vacuum pickup valve PWM command [%] *)
    bCmd_PneumaticBlowOff_Pulse     : BOOL;     (* High-speed solenoid puff blow-off discharge pulse [bool] *)
    bCmd_VacuumSupply_Enable        : BOOL;     (* Master vacuum venturi / pump valve solenoid enable [bool] *)

    (* Optical Vision & Actuator Synchronization Signals *)
    bCmd_VisionCamera_Strobe        : BOOL;     (* High-speed LED strobe trigger signal for fly-by camera [bool] *)
    bCmd_RejectPart_Gate            : BOOL;     (* Reject divert chute solenoid actuator command [bool] *)
    bCmd_NozzleToolExchange         : BOOL;     (* Auto nozzle changer station index command [bool] *)
    bCmd_Conveyor_ReleasePCB        : BOOL;     (* Conveyor clamp unclamp and PCB downstream release [bool] *)
    bCmd_Feeder_IndexNext           : BOOL;     (* Feeder bank tape micro-pitch advance trigger command [bool] *)

    (* Voted & Compensated Feedback Telemetry *)
    rActual_Gantry_X_Pos            : REAL;     (* Thermally compensated and voted Gantry X position [mm] *)
    rActual_Gantry_Y_Pos            : REAL;     (* Thermally compensated and voted Gantry Y position [mm] *)
    rActual_Head_Theta_Deg          : REAL;     (* Voted spindle head orientation angle [deg] *)
    rActual_VacuumPressure_kPa      : REAL;     (* Voted pickup vacuum pressure [kPa] *)
    rActual_PCB_Surface_Z_mm        : REAL;     (* Laser triangulation dynamic warpage compensated PCB height [mm] *)

    (* Cyber-Physical Observer & Model Predictive Control Estimations *)
    rEstimated_TCP_Vibration_um     : REAL;     (* State-space estimated TCP flexure vibration deflection [um] *)
    rEstimated_Gantry_Yaw_mrad      : REAL;     (* State-space estimated dual-drive gantry yaw skew angle [mrad] *)
    rEstimated_LandingForce_N       : REAL;     (* Voice coil dynamic touch landing force [N] *)
    rCalculated_ThermalComp_X_um    : REAL;     (* Real-time thermal expansion compensation applied to X-axis [um] *)
    rCalculated_ThermalComp_Y_um    : REAL;     (* Real-time thermal expansion compensation applied to Y-axis [um] *)

    (* Production Performance & Quality Telemetry *)
    rActual_PlacementRate_CPH       : REAL;     (* Real-time calculated placement throughput [cph] *)
    rComponent_Tombstone_RiskIndex  : REAL;     (* Vacuum decay tombstone / tilt risk metric (0.0 to 1.0) [idx] *)
    iActive_Spindle_Index           : INT;      (* Currently indexed spindle number (1 to 16) [int] *)
    iCurrent_FSM_State              : INT;      (* Deterministic FSM current state identifier [enum] *)

    (* Bit-Packed 32-Bit Industrial Diagnostic & Status Words *)
    dwStatus_GantryMotion           : DWORD;    (* Bit-packed gantry kinematics and servo status word [dword] *)
    dwStatus_HeadSpindles           : DWORD;    (* Bit-packed 16-spindle part presence and vacuum status [dword] *)
    dwStatus_VisionInspection       : DWORD;    (* Bit-packed optical vision inspection status word [dword] *)
    dwAlarmWord1_ISA_CriticalTrips  : DWORD;    (* ISA-18.2 Severity 1 Critical Emergency Trip Word [dword] *)
    dwAlarmWord2_ISA_ProcessWarnings: DWORD;    (* ISA-18.2 Severity 2 Process Warnings and Auto-Rejects [dword] *)
    dwDiagnostic_FeederHealth       : DWORD;    (* Smart feeder bank and tape advance diagnostic word [dword] *)

    (* Cumulative Production Statistical Counters *)
    udiTotalPartsPlacedCount        : UDINT;    (* Cumulative successfully placed component count [parts] *)
    udiTotalPartsRejectedCount      : UDINT;    (* Cumulative vision/vacuum rejected component count [parts] *)
    udiConsecutivePickFailsCount    : UDINT;    (* Consecutive component pick failure tally [count] *)
END_VAR
"""
