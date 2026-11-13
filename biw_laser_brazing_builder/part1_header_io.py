# biw_laser_brazing_builder/part1_header_io.py
"""
Part 1: Header and I/O Variable Declarations
Function Block: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Automotive_BIW_LaserBrazing_StructuralAdhesive
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - PRODUCTION SPECIFICATION V7.8
DOMAIN: Automotive & Commercial Vehicles (Body-in-White BIW Laser Roof Ditch Brazing & Structural Epoxy Framing Cell)
TARGET ARCHITECTURE: IEC 61131-3 Industrial Real-Time Fieldbus Controller (Ts = 2.0 ms Synchronous Task)
FUNCTION BLOCK: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive

PLANT CYBER-PHYSICAL ARCHITECTURE OVERVIEW:
----------------------------------------------------------------------------------------------------
This production-grade Function Block governs the multi-physics cyber-physical execution of an
ultra-high-speed robotic Body-in-White (BIW) Geo-Framing and Joining Station. The station performs:
  1. Precision Roof Ditch Laser Brazing: Continuous deposition of CuSi3 (Copper-Silicon 3%) filler wire
     into the narrow, high-aspect-ratio joint between the stamped hydroformed roof panel and the hot-stamped
     boron steel (22MnB5) bodyside outer panel using a 5.0 kW multi-mode solid-state continuous-wave fiber laser.
     Robot contouring velocities operate up to 120 mm/s under tactile/optical coaxial laser seam-tracking.
  2. Coordinated Structural Epoxy Adhesive Dispensing: Concurrent or staged deposition of crash-durable,
     high-viscosity toughened structural epoxy (200,000 to 500,000 mPa*s) along the cant rail / roof ditch
     underbody flange using an electric servo-driven positive displacement gear pump and heated delivery lines.
  3. Pneumatic/Servo Framing Geo-Clamping: Multi-point pneumatic toggle clamps and hydraulic datum locating
     pins locking the body-in-white structure to +/- 0.05 mm geometric repeat precision under thermal strain.

MATHEMATICAL CORES EMBEDDED:
  - First-Principles 8-State Cyber-Physical Discrete State-Space Model (Ts = 2.0 ms, A, B, C, D)
  - 8x6 Steady-State Luenberger Observer with Kalman Innovation Injection (L)
  - 5-Step Receding Horizon Model Predictive Control (MPC) with 6-iteration Projected Gradient Descent (PGD)
  - Dynamic Laser Power & Wire Feed Cross-Coupling Decoupling with Anti-Stubbing / Anti-Keyhole Control
  - Non-Newtonian Power-Law Adhesive Hydrodynamics with Dynamic Pressure-Flow Lead-Lag Compensation
  - 2oo3 (Two-Out-Of-Three) Triple Modular Redundant (TMR) Sensor Voting across 5 Triplicated Instrument Groups
  - 14-Stage Deterministic Production Finite State Machine (FSM) with Millisecond-Level Error Trapping
  - ISA-18.2 Process Alarm Matrix (HH, H, L, LL) with Dynamic Deadband Hysteresis
  - SIL-3 Certified Fast Laser Quench (< 3.0 ms) Hardware Interlock on Wire Feed Motor Stall / Slip
====================================================================================================
*)
VAR_INPUT
    (* ---------------- System Supervisory Commands & Interlocks ---------------- *)
    bEnable                         : BOOL := FALSE;    (* Master Block Execution Enable Signal [1=Run, 0=Disabled] *)
    bReset                          : BOOL := FALSE;    (* Master Supervisory Alarm Reset Pushbutton [1=Pulse Reset] *)
    bAutoMode                       : BOOL := FALSE;    (* Operational Mode Select [1=Fully Automated Sequence, 0=Manual/Step] *)
    bCycleStart                     : BOOL := FALSE;    (* Cycle Start Trigger Pulse [1=Initiate Station Run] *)
    bCycleStop                      : BOOL := FALSE;    (* Cycle Stop Request [1=Orderly Cycle Termination] *)
    bEmergencyStopOk                : BOOL := FALSE;    (* SIL-3 Safety Circuit Emergency Stop Healthy [1=Healthy, 0=Tripped] *)
    bSafetyFenceClosed              : BOOL := FALSE;    (* Laser Class 4 Enclosure Guard Interlock [1=Locked, 0=Interrupted] *)
    bLaserSourceReady               : BOOL := FALSE;    (* Fiber Laser Generator Ready for Emission [1=Ready, 0=Fault] *)
    bLaserChillerTempOk             : BOOL := FALSE;    (* Laser & Optic Deionized Water Cooling Temp Ok [1=Permissive, 0=Overheat] *)
    bLaserOpticsInterlockOk         : BOOL := FALSE;    (* Coaxial Optics Fiber Connection & Pyrometer Interlock [1=Ok, 0=Fault] *)
    
    (* ---------------- 2oo3 TMR Channel 1: Coaxial Optical Pyrometers [deg C] ---------------- *)
    rTT_Pyro_101A                   : REAL := 25.0;     (* Coaxial Optical Pyrometer Sensor A Melt Pool Temp [deg C] *)
    rTT_Pyro_101B                   : REAL := 25.0;     (* Coaxial Optical Pyrometer Sensor B Melt Pool Temp [deg C] *)
    rTT_Pyro_101C                   : REAL := 25.0;     (* Coaxial Optical Pyrometer Sensor C Melt Pool Temp [deg C] *)

    (* ---------------- 2oo3 TMR Channel 2: 3D Laser Seam Triangulation Profilometers [um] ---------------- *)
    rLT_Seam_201A                   : REAL := 0.0;      (* Optical 3D Seam Triangulation Sensor A Lateral Gap Deviation [um] *)
    rLT_Seam_201B                   : REAL := 0.0;      (* Optical 3D Seam Triangulation Sensor B Lateral Gap Deviation [um] *)
    rLT_Seam_201C                   : REAL := 0.0;      (* Optical 3D Seam Triangulation Sensor C Lateral Gap Deviation [um] *)

    (* ---------------- 2oo3 TMR Channel 3: Adhesive High-Pressure Transducers [bar] ---------------- *)
    rPT_Adh_301A                    : REAL := 0.0;      (* High-Pressure Adhesive Nozzle Manifold Pressure Sensor A [bar] *)
    rPT_Adh_301B                    : REAL := 0.0;      (* High-Pressure Adhesive Nozzle Manifold Pressure Sensor B [bar] *)
    rPT_Adh_301C                    : REAL := 0.0;      (* High-Pressure Adhesive Nozzle Manifold Pressure Sensor C [bar] *)

    (* ---------------- 2oo3 TMR Channel 4: In-line Coriolis Mass Flowmeters [g/s] ---------------- *)
    rFT_Adh_401A                    : REAL := 0.0;      (* In-line Coriolis Mass Flowmeter Sensor A Adhesive Mass Rate [g/s] *)
    rFT_Adh_401B                    : REAL := 0.0;      (* In-line Coriolis Mass Flowmeter Sensor B Adhesive Mass Rate [g/s] *)
    rFT_Adh_401C                    : REAL := 0.0;      (* In-line Coriolis Mass Flowmeter Sensor C Adhesive Mass Rate [g/s] *)

    (* ---------------- 2oo3 TMR Channel 5: Framing Geo-Clamp Pneumatic Load Cells [N] ---------------- *)
    rWT_Clamp_501A                  : REAL := 0.0;      (* Geo-Framing Toggle Clamp Cylinder A Clamping Reaction Force [N] *)
    rWT_Clamp_501B                  : REAL := 0.0;      (* Geo-Framing Toggle Clamp Cylinder B Clamping Reaction Force [N] *)
    rWT_Clamp_501C                  : REAL := 0.0;      (* Geo-Framing Toggle Clamp Cylinder C Clamping Reaction Force [N] *)

    (* ---------------- Wire Feeder & Consumable Auxiliary Telemetry ---------------- *)
    rWireFeedActualSpeed            : REAL := 0.0;      (* CuSi3 Wire Feed Auxiliary Optical Encoder Velocity [mm/s] *)
    rWireFeedMotorCurrent           : REAL := 0.0;      (* Push-Pull Wire Feeder Brushless Servo Torque Current [A] *)
    rWireReelRemaining              : REAL := 1500.0;   (* Drum Wire Payoff Spool Remaining Wire Quantity [m] *)
    bWireEndDetected                : BOOL := FALSE;    (* Wire Payoff Conduit Optical Wire Runout Sensor [1=Exhausted, 0=Ok] *)
    bWireJamDetected                : BOOL := FALSE;    (* Cold Wire Liner Conduit Micro-Switch Buckling Detector [1=Jam, 0=Ok] *)

    (* ---------------- Gas, Optics Purge & Environmental Inputs ---------------- *)
    rShieldGasPressure              : REAL := 5.5;      (* Pure Argon Shielding Gas Supply Manifold Pressure [bar] *)
    rShieldGasFlowRate              : REAL := 22.0;     (* Shielding Gas Volumetric Flow Rate [L/min] *)
    rCrossJetAirPressure            : REAL := 6.0;      (* High-Velocity Cross-Jet Air Knife Pressure [bar] *)
    rOpticsGlassTransmission        : REAL := 98.5;     (* Protective Cover Slide Transmissivity Photodiode Index [%] *)

    (* ---------------- Multi-Axis Articulated Robot Real-Time Telemetry ---------------- *)
    rRobotContourSpeed              : REAL := 0.0;      (* Robot Tool Center Point (TCP) Trajectory Path Velocity [mm/s] *)
    rRobotPathPosition              : REAL := 0.0;      (* Robot Current Linear Arc Distance Along Roof Ditch [mm] *)
    bRobotInMotion                  : BOOL := FALSE;    (* Robot Controller Trajectory Executing Status [1=Moving, 0=At Rest] *)
    bRobotInContourZone             : BOOL := FALSE;    (* Robot Tool Center Point Inside Active Brazing Envelope [1=Inside, 0=Clear] *)
    bRobotEgressPermit              : BOOL := FALSE;    (* Robot Home / Transfer Clear Handshake Signal [1=Permissive, 0=Blocked] *)

    (* ---------------- Structural Adhesive Fluid Condition Inputs ---------------- *)
    rAdhManifoldTemp                : REAL := 45.0;     (* Temperature Controlled Dispense Manifold Body [deg C] *)
    rAdhHoseTemp                    : REAL := 42.0;     (* Heated Flexible High-Pressure Core Hose Temp [deg C] *)
    rBarrel1Pressure                : REAL := 180.0;    (* Hydraulic Ram Barrel Pump 1 High Pressure [bar] *)
    rBarrel2Pressure                : REAL := 180.0;    (* Hydraulic Ram Barrel Pump 2 High Pressure [bar] *)
    bBarrel1LowLevel                : BOOL := FALSE;    (* Drum 1 200L Follower Plate Low Level Warning [1=Low, 0=Normal] *)
    bBarrel2LowLevel                : BOOL := FALSE;    (* Drum 2 200L Follower Plate Low Level Warning [1=Low, 0=Normal] *)

    (* ---------------- Tooling, Tool Clamping & Skid Proximity Inputs ---------------- *)
    bSkidInStation                  : BOOL := FALSE;    (* Bodyside Underbody Roller Skid Docked Proximity Sensor [1=In Place, 0=Empty] *)
    bDatumPinsLocked                : BOOL := FALSE;    (* Hydraulic Precision Locating Datum Pins Extended & Locked [1=Locked, 0=Retracted] *)
    bGeoClampsClosed                : BOOL := FALSE;    (* Roof Ditch Pneumatic Over-Center Clamps Closed Sensor [1=Closed, 0=Opened] *)
    bGeoClampsOpened                : BOOL := FALSE;    (* Roof Ditch Pneumatic Clamps Retracted Proximity Sensor [1=Retracted, 0=Extended] *)
    
    (* ---------------- Operator HMI Maintenance Pushbuttons ---------------- *)
    bManualPurgeAdhesiveCmd         : BOOL := FALSE;    (* HMI Manual Adhesive Station Purge Cycle Trigger [1=Trigger, 0=Off] *)
    bManualScourNozzleCmd           : BOOL := FALSE;    (* HMI Manual Solvent/Flushing Anti-Curing Scour Trigger [1=Trigger, 0=Off] *)
    bManualWireInchForward          : BOOL := FALSE;    (* Jog Wire Feeder Forward Pushbutton [1=Jog, 0=Stop] *)
    bManualWireInchRetract          : BOOL := FALSE     (* Jog Wire Feeder Reverse Pushbutton [1=Jog, 0=Stop] *)
END_VAR
VAR_OUTPUT
    (* ---------------- Real-Time Primary Actuator Modulations ---------------- *)
    bLaserEnable                    : BOOL := FALSE;    (* Fiber Laser Emission Active Permissive Gate [1=Emission Permitted, 0=Quenched] *)
    bLaserShutterRelease            : BOOL := FALSE;    (* Laser Optical Safety Shutter Open Command [1=Shutter Open, 0=Closed] *)
    bFastLaserQuenchSIL3            : BOOL := FALSE;    (* Sub-3ms Hardwired Safety Laser Quench Output [1=Laser Quenched, 0=Normal] *)
    rLaserPowerCmd                  : REAL := 0.0;      (* Fiber Laser Commanded Continuous Wave Optical Power [W] *)
    rWireFeedSpeedCmd               : REAL := 0.0;      (* Push-Pull Wire Feed Synchronous Speed Command [mm/s] *)
    bWireFeedForwardCmd             : BOOL := FALSE;    (* Wire Feeder Drive Run Forward Motor Contactor [1=Forward, 0=Halt] *)
    bWireFeedRetractCmd             : BOOL := FALSE;    (* Wire Feeder Drive Reverse Retract Motor Contactor [1=Reverse, 0=Halt] *)
    rSeamTrackingOffsetCmd          : REAL := 0.0;      (* Seam Tracker High-Speed Lateral Cross-Slide Correction [um] *)
    rSeamTrackingHeightCmd          : REAL := 0.0;      (* Seam Tracker Vertical Stand-Off Height Correction [um] *)
    bSeamTrackingActive             : BOOL := FALSE;    (* Seam Tracking Laser Vision Sensor Active Status [1=Tracking, 0=Idle] *)

    (* ---------------- Adhesive Dispense Actuator Commands ---------------- *)
    rAdhPumpSpeedCmd                : REAL := 0.0;      (* Adhesive Positive Displacement Servo Gear Pump Target Speed [rpm] *)
    rAdhHeaterDutyCmd               : REAL := 0.0;      (* Nozzle Tip Resistive Heating Element PWM Duty Cycle [%] *)
    bAdhTipNeedleValveCmd           : BOOL := FALSE;    (* High-Pressure Pneumatic Extrusion Needle Valve Actuator [1=Dispense, 0=Closed] *)
    bAdhRecircValveCmd              : BOOL := FALSE;    (* Internal High-Pressure Fluid Recirculation Dump Valve [1=Recirc, 0=Off] *)

    (* ---------------- Station Tooling & Pneumatic Auxiliary Outputs ---------------- *)
    rRobotSpeedOverrideCmd          : REAL := 100.0;    (* Dynamic Contouring Path Speed Override to Robot Controller [%] *)
    rClampPressureCmd               : REAL := 6.0;      (* Framing Station Proportional Pressure Regulator Command [bar] *)
    bShieldGasValveCmd              : BOOL := FALSE;    (* Pure Argon Shielding Gas High-Flow Solenoid Valve [1=Open, 0=Closed] *)
    bCrossJetAirValveCmd            : BOOL := FALSE;    (* High-Pressure Air Knife Optics Protection Solenoid [1=Open, 0=Closed] *)
    bClampLockCmd                   : BOOL := FALSE;    (* Framing Geo-Clamp Over-Center Solenoid Close Command [1=Lock, 0=Release] *)
    bClampReleaseCmd                : BOOL := FALSE;    (* Framing Geo-Clamp Solenoid Open Command [1=Release, 0=Lock] *)
    bDatumPinLockCmd                : BOOL := FALSE;    (* Hydraulic Underbody Datum Positioning Pins Extend [1=Extend, 0=Retract] *)
    bDatumPinRetractCmd             : BOOL := FALSE;    (* Hydraulic Underbody Datum Positioning Pins Retract [1=Retract, 0=Extend] *)

    (* ---------------- Production Supervisory & Cycle Handshake Telemetry ---------------- *)
    bStationBusy                    : BOOL := FALSE;    (* Framing Station Processing Active Cycle [1=Busy, 0=Ready] *)
    bStationComplete                : BOOL := FALSE;    (* Station Cycle Successfully Finalized [1=Complete, 0=Running] *)
    bEgressReady                    : BOOL := FALSE;    (* Bodyside Transfer Skid Clear to Depart Handshake [1=Clear, 0=Retained] *)
    bGeneralFaultTrip               : BOOL := FALSE;    (* Station Critical Master Safety / Process Trip [1=Tripped, 0=Healthy] *)
    bWarningActive                  : BOOL := FALSE;    (* Non-Tripping Maintenance / Tolerance Exceedance Warning [1=Active, 0=Clear] *)
    nActiveState                    : INT := 0;         (* 14-Stage Production State Machine Active Index [0..13] *)
    nActiveSubState                 : INT := 0;         (* State Internal Micro-Step Execution Sequencer Index [0..99] *)
    tCycleElapsedTime               : TIME := T#0s;     (* Monitored Active Cycle Duration From Station Lock [TIME] *)
    rBrazePorosityScore             : REAL := 0.0;      (* Post-Braze Optical Seam Porosity / Defect Index [%] *)
    rAdhBeadVolumeCompliance        : REAL := 100.0;    (* Adhesive Dispense Volumetric Cross-Section Compliance [%] *)

    (* ---------------- ISA-18.2 Bit-Packed 32-Bit Industrial Telemetry ---------------- *)
    dwStatusWord1                   : DWORD := 16#00000000; (* Primary Cyber-Physical Station Status Telemetry Bitmask [DWORD] *)
    dwStatusWord2                   : DWORD := 16#00000000; (* Secondary Robotic Subsystem Coordination Bitmask [DWORD] *)
    dwAlarmWord1                    : DWORD := 16#00000000; (* ISA-18.2 High-Priority Process Alarms Bitmask [DWORD] *)
    dwAlarmWord2                    : DWORD := 16#00000000; (* Hardware / Communication / Sensor Health Bitmask [DWORD] *)
    dwFirstOutWord                  : DWORD := 16#00000000  (* First-Out Latching Trip Identifier Code [DWORD] *)
END_VAR
"""
"""
Let's verify that this part has proper comments and physical units.
Physical units present: [deg C], [um], [bar], [g/s], [N], [mm/s], [A], [m], [L/min], [%], [mm], [rpm], [TIME], [W], etc.
All units are in square brackets.
"""
