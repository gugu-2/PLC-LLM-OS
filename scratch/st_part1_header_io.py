# -*- coding: utf-8 -*-

part1_header_io = """FUNCTION_BLOCK FB_AutomatedParking_MultiLevel_ShuttleHoist
(*
 ====================================================================================================
  PROJECT:       COMMERCIAL AUTOMATED MULTI-LEVEL MECHANICAL PARKING SYSTEM (APS SHUTTLES)
  MODULE:        FB_AutomatedParking_MultiLevel_ShuttleHoist
  DISCIPLINE:    CYBER-PHYSICAL ADVANCED AUTOMATION / HIGH-SPEED HOIST & RACK SHUTTLE MOTION CONTROL
  STANDARDS:     DIN EN 14010 (POWER DRIVEN PARKING EQUIPMENT SAFETY), ISO 13849-1 (PL e / CAT 4),
                 IEC 61508 (SIL-3 SAFETY INSTRUMENTED SYSTEMS), ASME A17.1 / CSA B44 (HOIST SAFETY),
                 VDI 4466 (AUTOMATED GUIDED VEHICLES & STORAGE RETRIEVAL MACHINES),
                 ISA-18.2 (ALARM SYSTEMS MANAGEMENT), IEC 60034 (TRACTION MOTOR DYNAMICS)
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  MACHINE CLASS: 15-LEVEL HIGH-BAY AUTOMATED PARKING SILO / 600-VEHICLE HIGH-THROUGHPUT FACILITY
  ACTUATION:     75 kW GEARLESS PERMANENT MAGNET SYNCHRONOUS HOIST (PMSM) WITH 50% CW BALANCE,
                 HIGH-SPEED LASER-GUIDED HORIZONTAL RACK SHUTTLE CART (v_max = 1.8 m/s),
                 DUAL HIGH-PRECISION TELESCOPIC COMB VEHICLE TRANSFER SATELLITE ARMS
  CYCLE TIME:    T_s = 0.005 s (5 MILLISECONDS DETERMINISTIC REAL-TIME MOTION & SAFETY SCAN)
 ----------------------------------------------------------------------------------------------------
  CORE ARCHITECTURAL AND CYBER-PHYSICAL CAPABILITIES:
   1. Triple Modular Redundancy (2oo3 TMR) Voting & Sensor Discrepancy Diagnostics:
      Executes continuous median voting, spread monitoring, and persistent discrepancy integration across:
      - Vertical Hoist Optical Laser Distance Transmitters (Channels A, B, C) [mm]
      - Traction Sheave Incremental/Absolute Optical Encoders (Channels A, B, C) [mm]
      - Horizontal Shuttle Laser Distance Transmitters (Channels A, B, C) [mm]
      - Entry Cabin Vehicle Platform Weigh Scale Load Cells (Channels A, B, C) [kg]
      Features bumpless degradation from 2oo3 to 1oo2 upon single transmitter drift or loss-of-signal,
      plus cross-correlation slip detection between optical distance and rotary sheave feedback.
   2. Discrete State-Space Cyber-Physical Dynamics (Ad, Bd, Cd, Dd):
      Models an 8-state, 4-control continuous-time electro-mechanical dynamics discretized at Ts = 5 ms:
      - x1: Hoist carriage vertical position excursion Delta_z [mm]
      - x2: Hoist carriage vertical velocity excursion Delta_v [mm/s]
      - x3: Steel traction cable longitudinal elastic stretch vibration Delta_delta [mm]
      - x4: Steel traction cable elastic stretch oscillation rate Delta_dot_delta [mm/s]
      - x5: Horizontal rack shuttle position error Delta_x [mm]
      - x6: Horizontal rack shuttle velocity error Delta_v_shuttle [mm/s]
      - x7: PMSM hoist motor electromagnetic air-gap torque deviation Delta_T_elec [N*m]
      - x8: Common DC bus link capacitor potential fluctuation Delta_V_dc [V]
      Driven by 4 control vectors:
      - u1: Hoist traction motor torque demand [N*m]
      - u2: Shuttle rack traction servo speed/torque demand [N*m]
      - u3: Active cable vibration damping feedforward torque injection [N*m]
      - u4: Active Front End (AFE) regenerative braking power feedforward [kW]
   3. Receding-Horizon Model Predictive Control (MPC) Quadratic Optimization:
      Formulates an online quadratic cost objective balancing position tracking error, cable vibration
      suppression, floor leveling precision, and regenerative energy recovery against actuator wear.
      Evaluates analytical gradients g = Bd' * Q * (x_pred - x_ref) + R * u_prev + Rd * Delta_u
      and exact diagonal Hessian terms H_ii to execute projected gradient descent with box constraints.
   4. Jerk-Limited 7-Phase S-Curve Motion Profiling & Sub-Millimeter Floor Docking:
      Generates continuous C2-differentiable trajectory setpoints with bounded jerk (j_max = 2.5 m/s^3),
      acceleration (a_max = 1.2 m/s^2), and cruise velocity (v_max = 3.5 m/s). Features dual-stage terminal
      approach achieving sub-millimeter leveling accuracy (|e_z| < 0.5 mm) prior to sill pin docking.
   5. Active Cable Elasticity Vibration Compensation:
      Synthesizes an active damping control law compensating for cable longitudinal spring-mass resonance
      as a function of instantaneous hoist payload mass and suspended rope free length.
   6. Regenerative Braking Energy Capture & Active Front End DC Link Regulation:
      Coordinates bidirectional active front-end power flow during descending loaded hoist or ascending
      counterweight motion, dynamically pulsing the braking chopper during grid transient overvoltages.
   7. SIL 3 Multi-Stage Finite State Machine Architecture:
      Orchestrates the complete vehicle lifecycle across 11 discrete states: System Boot/Homing, Cabin
      Check-In & Volumetric Profiling, Cabin Vacate Safety Interlock, Mechanical Pallet Locking, High-Speed
      Vertical Ascent/Descent, Sub-Millimeter Floor Docking, Shuttle Aisle Deployment, Rack Bay Comb Transfer,
      Shuttle Retraction, Ground Return, and Emergency Hydraulic Wedge Clamp Lockout.
   8. ISA-18.2 Compliant Multi-Tiered Alarm Matrix:
      Full High-High (HH), High (H), Low (L), Low-Low (LL) hierarchy with deadband hysteresis, priority
      escalation, slack cable trip, overspeed clamp drop, vehicle envelope violation, and 32-bit SCADA words.
 ====================================================================================================
*)
VAR_INPUT
    (* ===================================================================================== *)
    (* 1.0 SYSTEM MASTER DIGITAL PERMISSIVES & OPERATOR COMMANDS                             *)
    (* ===================================================================================== *)
    bEnableSystem                   : BOOL := FALSE;    (* Master Supervisory Automation Enable Permissive *)
    bEmergencyStopCircuitOK         : BOOL := TRUE;     (* Hardwired Dual-Channel SIL-3 Emergency Stop Relay Circuit [Active HIGH = Healthy] *)
    bSafetyCurtainCabinClear        : BOOL := TRUE;     (* Entry Cabin Perimeter Optical Light Curtain Unbroken Status *)
    bCabinVacateMotionCleared       : BOOL := TRUE;     (* Cabin Ground Safety Microwave / PIR Sensors Detect No Human Presence *)
    bManualTripEmergencyClamp       : BOOL := FALSE;    (* Control Room Manual Emergency Hydraulic Wedge Clamp Drop Pushbutton *)
    bMasterAlarmReset               : BOOL := FALSE;    (* Operator Master Alarm Acknowledgement & Trip Reset Command *)
    bExecuteStorageCycle            : BOOL := FALSE;    (* Supervisory WMS Dispatch Command to Initiate Storage Cycle *)
    bExecuteRetrievalCycle          : BOOL := FALSE;    (* Supervisory WMS Dispatch Command to Initiate Vehicle Retrieval Cycle *)
    bActiveFrontEndRegenReady       : BOOL := TRUE;     (* AFE Regenerative Inverter Precharged, Synchronized & Grid-Ready *)
    bDynamicBrakingResistorOK       : BOOL := TRUE;     (* Dynamic Braking Resistor Thermal Overload Switch Closed (Healthy) *)

    (* ===================================================================================== *)
    (* 2.0 MECHANICAL LIMIT SWITCHES & CABIN ACTUATOR STATUS FEEDBACKS                       *)
    (* ===================================================================================== *)
    bCabinShutterDoorClosed         : BOOL := TRUE;     (* Fast Roll-Up Vehicle Entry Shutter Door Fully Closed Limit Switch *)
    bCabinShutterDoorOpened         : BOOL := FALSE;    (* Fast Roll-Up Vehicle Entry Shutter Door Fully Open Limit Switch *)
    bPalletLockEngaged_Feedback     : BOOL := TRUE;     (* Hoist Carriage Mechanical Pallet Locking Centering Pins Engaged *)
    bPalletLockDisengaged_Feedback  : BOOL := FALSE;    (* Hoist Carriage Mechanical Pallet Locking Centering Pins Retracted *)
    bBayDockingPinSeated            : BOOL := FALSE;    (* Target Rack Bay Structural Docking Alignment Pin Seated Sensor *)
    bCombArmsExtended_Feedback      : BOOL := FALSE;    (* Shuttle Telescopic Vehicle Transfer Comb Arms Fully Extended *)
    bCombArmsRetracted_Feedback     : BOOL := TRUE;     (* Shuttle Telescopic Vehicle Transfer Comb Arms Fully Retracted *)
    bVehicleWheelChocksEngaged      : BOOL := TRUE;     (* Pallet Pneumatic / Mechanical Wheel Stopper Chocks Locked *)
    bEmergencyWedgeClampLatched     : BOOL := TRUE;     (* Hoist Guide Rail Hydraulic Safety Wedge Clamps Armed & Latched Open *)
    bSlackCableSwitchTripped        : BOOL := FALSE;    (* Mechanical Limit Switch for Counterweight / Carriage Slack Rope *)

    (* ===================================================================================== *)
    (* 3.0 TRIPLE MODULAR REDUNDANCY (2oo3) HOIST OPTICAL LASER DISTANCE SENSORS             *)
    (* Long-range phase-shift optical laser distance meters measuring hoist carriage height   *)
    (* ===================================================================================== *)
    rHoistLaserDist_A_mm            : REAL := 0.0;      (* Vertical Hoist Laser Distance Meter Channel A [mm] *)
    rHoistLaserDist_B_mm            : REAL := 0.0;      (* Vertical Hoist Laser Distance Meter Channel B [mm] *)
    rHoistLaserDist_C_mm            : REAL := 0.0;      (* Vertical Hoist Laser Distance Meter Channel C [mm] *)

    (* ===================================================================================== *)
    (* 4.0 TRIPLE MODULAR REDUNDANCY (2oo3) HOIST ROTARY TRACTION SHEAVE ENCODERS            *)
    (* High-resolution absolute optical encoders mounted directly on the traction motor shaft *)
    (* ===================================================================================== *)
    rHoistRotaryEncoder_A_mm        : REAL := 0.0;      (* Hoist Traction Sheave Rotary Encoder Channel A [mm] *)
    rHoistRotaryEncoder_B_mm        : REAL := 0.0;      (* Hoist Traction Sheave Rotary Encoder Channel B [mm] *)
    rHoistRotaryEncoder_C_mm        : REAL := 0.0;      (* Hoist Traction Sheave Rotary Encoder Channel C [mm] *)

    (* ===================================================================================== *)
    (* 5.0 TRIPLE MODULAR REDUNDANCY (2oo3) HORIZONTAL RACK SHUTTLE AISLE LASERS            *)
    (* High-speed optical laser distance meters measuring shuttle carriage aisle position   *)
    (* ===================================================================================== *)
    rShuttleLaserDist_A_mm          : REAL := 1800.0;   (* Horizontal Shuttle Laser Distance Channel A [mm] *)
    rShuttleLaserDist_B_mm          : REAL := 1800.0;   (* Horizontal Shuttle Laser Distance Channel B [mm] *)
    rShuttleLaserDist_C_mm          : REAL := 1800.0;   (* Horizontal Shuttle Laser Distance Channel C [mm] *)

    (* ===================================================================================== *)
    (* 6.0 TRIPLE MODULAR REDUNDANCY (2oo3) CABIN ENTRY VEHICLE WEIGH SCALE LOAD CELLS       *)
    (* Precision shear-beam strain gauge load cells under entry cabin transfer platform      *)
    (* ===================================================================================== *)
    rPalletLoadCell_A_kg            : REAL := 0.0;      (* Cabin Platform Vehicle Weigh Scale Channel A [kg] *)
    rPalletLoadCell_B_kg            : REAL := 0.0;      (* Cabin Platform Vehicle Weigh Scale Channel B [kg] *)
    rPalletLoadCell_C_kg            : REAL := 0.0;      (* Cabin Platform Vehicle Weigh Scale Channel C [kg] *)

    (* ===================================================================================== *)
    (* 7.0 ENTRY CABIN VOLUMETRIC VEHICLE DIMENSIONING LIGHT CURTAINS & SCANNERS             *)
    (* Optical beam arrays verifying vehicle clearance against structural silo rack bounds   *)
    (* ===================================================================================== *)
    rVehicleLength_Measured_mm      : REAL := 4650.0;   (* Scanned Total Vehicle Length from Bumper to Bumper [mm] *)
    rVehicleWidth_Measured_mm       : REAL := 1880.0;   (* Scanned Total Vehicle Width Including Side Mirrors [mm] *)
    rVehicleHeight_Measured_mm      : REAL := 1540.0;   (* Scanned Total Vehicle Height Including Roof Racks/Antennas [mm] *)
    rVehicleWheelbase_Measured_mm   : REAL := 2820.0;   (* Ground Ultrasonic Scanners Measured Wheelbase Distance [mm] *)
    bOverhangSensorsClear           : BOOL := TRUE;     (* Front and Rear Longitudinal Overhang Optical Curtain Clear Status *)
    bRoofLuggageClear               : BOOL := TRUE;     (* High-Level Optical Beam Verifying Roof Obstruction Clearance *)

    (* ===================================================================================== *)
    (* 8.0 ELECTRICAL, THERMAL & HYDRAULIC TRANSDUCERS                                       *)
    (* Power conversion, motor winding, disc brake and clamp pressure sensor signals         *)
    (* ===================================================================================== *)
    rTractionMotorCurrent_A         : REAL := 15.0;     (* Hoist 75kW PMSM Stator Phase RMS Current [A] *)
    rTractionMotorVoltage_V         : REAL := 400.0;    (* Inverter Output Line-to-Line Terminal Voltage [V] *)
    rDCLinkVoltage_V                : REAL := 680.0;    (* Common DC Bus Capacitor Link Potential [V] *)
    rTractionMotorWindingTemp_degC  : REAL := 45.0;     (* Hoist PMSM Stator RTD Pt100 Temperature [deg C] *)
    rTractionBrakeDiscTemp_degC     : REAL := 38.0;     (* Mechanical Disc Brake Caliper Infrared Temperature [deg C] *)
    rHydraulicClampPressure_bar     : REAL := 160.0;    (* Emergency Safety Wedge Clamp Hydraulic Actuator Pressure [bar] *)
    rHoistCableTension_kN           : REAL := 48.5;     (* Counterweight Traction Wire Rope Load-Cell Tension [kN] *)
    rCabinAmbientTemp_degC          : REAL := 22.0;     (* APS Parking Silo Internal Ambient Air Temperature [deg C] *)
    rGridFrequency_Hz               : REAL := 50.0;     (* Incoming 400V 3-Phase Utility Grid Frequency [Hz] *)

    (* ===================================================================================== *)
    (* 9.0 SUPERVISORY WMS DISPATCH TARGET SETPOINTS & IDENTIFICATION                        *)
    (* Warehouse Management System coordinate targets and RFID classification data           *)
    (* ===================================================================================== *)
    iTargetLevelNumber              : INT := 1;         (* Target Silo Level Elevation Index [1 to 15] *)
    iTargetBayColumn                : INT := 1;         (* Target Silo Rack Bay Column Index [1 to 24] *)
    iVehicleClassRFID               : INT := 1;         (* RFID Scanned Vehicle Class [1=Standard Sedan, 2=Large SUV, 3=Electric Van] *)
END_VAR

VAR_OUTPUT
    (* ===================================================================================== *)
    (* 1.0 HOIST, SHUTTLE & SATELLITE COMB ACTUATOR RUN COMMANDS                             *)
    (* ===================================================================================== *)
    bHoistMotorRun                  : BOOL := FALSE;    (* Hoist PMSM Inverter Drive Forward/Reverse Run Permissive *)
    bHoistMechanicalBrakeRelease    : BOOL := FALSE;    (* Hoist Electro-Hydraulic Disc Brake Release Solenoid Output *)
    bShuttleMotorRun                : BOOL := FALSE;    (* Shuttle Horizontal Servo Drive Run Permissive *)
    bShuttleBrakeRelease            : BOOL := FALSE;    (* Shuttle Parking Brake Coil Energize Command *)
    bCombArmsExtendCommand          : BOOL := FALSE;    (* Telescopic Vehicle Transfer Comb Arms Extend Actuator Command *)
    bCombArmsRetractCommand         : BOOL := FALSE;    (* Telescopic Vehicle Transfer Comb Arms Retract Actuator Command *)
    bPalletLockEngageCommand        : BOOL := FALSE;    (* Hoist Carriage Mechanical Pallet Locking Centering Solenoid Command *)
    bPalletLockDisengageCommand     : BOOL := FALSE;    (* Hoist Carriage Mechanical Pallet Locking Centering Retract Solenoid *)
    bEmergencyClampDeployCmd        : BOOL := FALSE;    (* Fail-Safe De-Energize to Drop Emergency Hydraulic Wedge Clamps *)
    bCabinShutterDoorOpenCmd        : BOOL := FALSE;    (* Fast Roll-Up Security Door Motorized Open Command *)
    bCabinShutterDoorCloseCmd       : BOOL := FALSE;    (* Fast Roll-Up Security Door Motorized Close Command *)
    bRegenerativeBrakeChopperFire   : BOOL := FALSE;    (* Inverter DC Link Dynamic Braking Chopper Gate Pulse Command *)

    (* ===================================================================================== *)
    (* 2.0 REAL-TIME MOTION SETPOINTS & TORQUE DEMANDS                                       *)
    (* ===================================================================================== *)
    rHoistTorqueDemand_Nm           : REAL := 0.0;      (* Hoist PMSM Vector Control Electromagnetic Torque Demand [N*m] *)
    rHoistVelocitySetpoint_m_s      : REAL := 0.0;      (* Jerk-Limited S-Curve Vertical Hoist Velocity Setpoint [m/s] *)
    rShuttleVelocitySetpoint_m_s    : REAL := 0.0;      (* Jerk-Limited Horizontal Shuttle Cart Velocity Setpoint [m/s] *)
    rActiveDampingTorque_Nm         : REAL := 0.0;      (* Active Cable Elasticity Vibration Compensation Torque [N*m] *)
    rRegenPowerFeedback_kW          : REAL := 0.0;      (* Real-Time Regenerative Braking Power Fed Back to Grid [kW] *)

    (* ===================================================================================== *)
    (* 3.0 CYBER-PHYSICAL TELEMETRY, REDUNDANT VOTED MEASUREMENTS & ESTIMATIONS              *)
    (* ===================================================================================== *)
    rVotedHoistPosition_mm          : REAL := 0.0;      (* 2oo3 TMR Median Voted Vertical Hoist Elevation [mm] *)
    rVotedHoistVelocity_m_s         : REAL := 0.0;      (* Filtered 2nd-Order Backward Difference Hoist Velocity [m/s] *)
    rVotedShuttlePosition_mm        : REAL := 1800.0;   (* 2oo3 TMR Median Voted Horizontal Shuttle Aisle Position [mm] *)
    rVotedVehicleWeight_kg          : REAL := 0.0;      (* 2oo3 TMR Median Voted Vehicle Gross Mass [kg] *)
    rHoistFloorLevelingError_mm     : REAL := 0.0;      (* Real-Time Sub-Millimeter Hoist-to-Floor Sill Vertical Alignment Error [mm] *)
    rCableVibrationAmplitude_mm     : REAL := 0.0;      (* Estimated Dynamic Longitudinal Cable Stretch Oscillation Amplitude [mm] *)
    rPredictedHoistPosition_mm      : REAL := 0.0;      (* Discrete State-Space Model 1-Step Ahead Predicted Hoist Elevation [mm] *)
    rPredictedCableStretch_mm       : REAL := 0.0;      (* Discrete State-Space Model 1-Step Ahead Predicted Cable Stretch [mm] *)
    rPredictedDCLinkVoltage_V       : REAL := 680.0;    (* Discrete State-Space Model 1-Step Ahead Predicted DC Bus Potential [V] *)
    rSimStatorWindingTemp_degC      : REAL := 45.0;     (* Dynamic Electro-Thermal Model Stator Hot-Spot Temperature [deg C] *)
    rSimBrakeDiscTemp_degC          : REAL := 38.0;     (* Kinetic Dissipation Thermal Replica Brake Surface Temperature [deg C] *)

    (* ===================================================================================== *)
    (* 4.0 SUPERVISORY STATE, SAFETY INTERLOCKS & SCADA DIAGNOSTIC WORDS                     *)
    (* ===================================================================================== *)
    bSystemInCycle                  : BOOL := FALSE;    (* Automated Parking or Retrieval Mission Active *)
    bFloorAlignedSubMillimeter      : BOOL := FALSE;    (* Hoist Carriage Elevation Aligned Within +/- 0.50 mm of Target Floor *)
    bSafetyInterlocksSatisfied      : BOOL := FALSE;    (* All Cabin, Hoist, Shuttle, and Clamp Safety Permissives Healthy *)
    bDegradedSensorWarning          : BOOL := FALSE;    (* Sensor Channel Spread Exceeded - Degraded from 2oo3 to 1oo2 Mode *)
    bCriticalSafetyTrip             : BOOL := FALSE;    (* Master Critical Safety Interlock Trip - Wedge Clamp Dropped & Locked *)
    bVehicleProfileAccepted         : BOOL := FALSE;    (* Scanned Vehicle Envelope & Weight Fully Compliant with Bay Category *)
    iOperationalState               : INT := 0;         (* Active Sequence State of APS Master Finite State Machine *)
    dwSystemStatusWord              : DWORD := 16#00000000; (* 32-Bit Telemetry Bitmask of System Operating Modes & Actuators *)
    dwAlarmWord_Safety              : DWORD := 16#00000000; (* 32-Bit ISA-18.2 Priority 1 Safety & Interlock Alarm Bitmask *)
    dwAlarmWord_Process             : DWORD := 16#00000000; (* 32-Bit ISA-18.2 Priority 2 Electrical & Thermal Process Alarm Bitmask *)
    dwDiagnosticsWord               : DWORD := 16#00000000; (* 32-Bit Sensor Redundancy & State-Space Divergence Diagnostic Word *)
END_VAR
"""
