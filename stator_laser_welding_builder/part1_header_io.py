# stator_laser_welding_builder/part1_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Automotive_EV_StatorHairpin_LaserWelding_VisionTrack
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
SYSTEM: HIGH-VOLUME 800V EV TRACTION MOTOR HAIRPIN STATOR LASER WELDING CELL
SUBSYSTEMS:
  - 192-PIN HIGH-DENSITY OXYGEN-FREE COPPER (Cu-ETP/Cu-OF) HAIRPIN CROWN ARRAY (96 WELD PAIRS)
  - 3D LASER TRIANGULATION PROFILOMETER REAL-TIME PIN GAP & HEIGHT ALIGNMENT (< +/-0.03 [mm])
  - 6.0 [kW] HIGH-BRIGHTNESS SINGLE-MODE / MULTI-BEAM DYNAMIC WOBBLE FIBER LASER SEAM WELDING
  - 10 [kHz] COAXIAL MELT POOL FAST DUAL-WAVELENGTH PYROMETER THERMAL EMISSION CLOSED-LOOP
  - 8-AXIS HIGH-DYNAMIC SYNCHRONOUS DIRECT-DRIVE ROTARY CHUCK WITH SUB-ARCSECOND ENCODER
  - HIGH-PURITY NITROGEN SHIELDING GAS CO-AXIAL AND CROSS-JET AERODYNAMIC CURTAIN CONTROL
  - MOTORIZED PROTECTIVE GLASS SLIDE CASSETTE WITH REAL-TIME OPTICAL TRANSMISSION MONITORING
  - IN-LINE 4-WIRE KELVIN MICRO-OHMMETER & EDDY CURRENT CONDUCTIVITY VERIFICATION (< 2.5 [uOhm])
  - 8-STATE DISCRETE CYBER-PHYSICAL STATE-SPACE THERMAL-KEYHOLE DYNAMICS MODEL (Ts = 2.0 [ms])
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE ACROSS 5 CRITICAL CHANNELS
  - DETERMINISTIC 14-STAGE AUTOMOTIVE TRACTION MOTOR PRODUCTION FINITE STATE MACHINE (FSM)
  - ISA-18.2 MULTI-TIER PROCESS ALARM HIERARCHY WITH BIT-PACKED STATUS & DIAGNOSTIC DWORDS
====================================================================================================
*)

VAR_INPUT
    (* Master Execution Commands & Safety Permissives *)
    bEnable                         : BOOL;         (* Master Execution Enable [-] *)
    bAutoCycleStart                 : BOOL;         (* Automatic 96-Pair Hairpin Seam Welding Cycle Start [-] *)
    bCycleAbort                     : BOOL;         (* Controlled Process Abort & Retract Command [-] *)
    bEmergencyStop                  : BOOL;         (* Hardwired Cat-4 Safety Circuit Fast De-energize [-] *)
    bResetFault                     : BOOL;         (* Master Alarm & Trip Reset Command [-] *)
    bAckAlarm                       : BOOL;         (* ISA-18.2 Process Alarm Acknowledge Pushbutton [-] *)
    bVisionCalibRequest             : BOOL;         (* 3D Profilometer Spatial Calibration Request [-] *)
    bCoverGlassCleanAck             : BOOL;         (* Protective Cover Glass Replacement Acknowledge [-] *)
    bManualJogPositive              : BOOL;         (* Manual Rotary Chuck Clockwise Jog Command [-] *)
    bManualJogNegative              : BOOL;         (* Manual Rotary Chuck Counter-Clockwise Jog Command [-] *)
    bDryRunMode                     : BOOL;         (* Dry Run Simulation Mode (Laser Output Inhibited) [-] *)
    bEddyCurrentBypass              : BOOL;         (* Bypass In-Line Micro-Ohmmeter Inspection [-] *)

    (* Channel Group 1: 3D Triangulation Profilometer Hairpin Gap Transducers (2oo3 TMR) *)
    rGap_Sensor_1A_mm               : REAL;         (* Profilometer Pin Gap Gauge Channel 1A [mm] *)
    rGap_Sensor_1B_mm               : REAL;         (* Profilometer Pin Gap Gauge Channel 1B [mm] *)
    rGap_Sensor_1C_mm               : REAL;         (* Profilometer Pin Gap Gauge Channel 1C [mm] *)

    (* Channel Group 1 Ext: Hairpin Pin Height Mismatch Transducers (2oo3 TMR) *)
    rHeight_Diff_1A_mm              : REAL;         (* Profilometer Pin Height Delta Channel 1A [mm] *)
    rHeight_Diff_1B_mm              : REAL;         (* Profilometer Pin Height Delta Channel 1B [mm] *)
    rHeight_Diff_1C_mm              : REAL;         (* Profilometer Pin Height Delta Channel 1C [mm] *)

    (* Channel Group 2: Coaxial Melt Pool High-Speed Pyrometer Photodiodes (2oo3 TMR) *)
    rMeltPool_Temp_2A_degC          : REAL;         (* Coaxial Pyrometer Thermal Emission Channel 2A [deg C] *)
    rMeltPool_Temp_2B_degC          : REAL;         (* Coaxial Pyrometer Thermal Emission Channel 2B [deg C] *)
    rMeltPool_Temp_2C_degC          : REAL;         (* Coaxial Pyrometer Thermal Emission Channel 2C [deg C] *)

    (* Channel Group 2 Ext: Keyhole Plume Vapor Emission Intensity *)
    rKeyhole_Plume_2A_pct           : REAL;         (* Vapor Capillary UV/Visible Emission Sensor 2A [%] *)
    rKeyhole_Plume_2B_pct           : REAL;         (* Vapor Capillary UV/Visible Emission Sensor 2B [%] *)
    rKeyhole_Plume_2C_pct           : REAL;         (* Vapor Capillary UV/Visible Emission Sensor 2C [%] *)

    (* Channel Group 3: Calibrated Fiber Laser Delivered Power Monitors (2oo3 TMR) *)
    rLaserPower_Mon_3A_kW           : REAL;         (* Laser Internal Optical Power Photodiode 3A [kW] *)
    rLaserPower_Mon_3B_kW           : REAL;         (* Laser Internal Optical Power Photodiode 3B [kW] *)
    rLaserPower_Mon_3C_kW           : REAL;         (* Laser Internal Optical Power Photodiode 3C [kW] *)

    (* Channel Group 4: High-Purity Shielding Nitrogen Mass Flowmeters (2oo3 TMR) *)
    rShieldGas_Flow_4A_Lmin         : REAL;         (* Shielding Nitrogen Gas Mass Flowmeter 4A [L/min] *)
    rShieldGas_Flow_4B_Lmin         : REAL;         (* Shielding Nitrogen Gas Mass Flowmeter 4B [L/min] *)
    rShieldGas_Flow_4C_Lmin         : REAL;         (* Shielding Nitrogen Gas Mass Flowmeter 4C [L/min] *)

    (* Channel Group 5: Rotary Chuck Hydraulic Collet Clamping Pressure Transducers (2oo3 TMR) *)
    rHyd_ClampPress_5A_bar          : REAL;         (* Stator Chuck Hydraulic Clamping Pressure 5A [bar] *)
    rHyd_ClampPress_5B_bar          : REAL;         (* Stator Chuck Hydraulic Clamping Pressure 5B [bar] *)
    rHyd_ClampPress_5C_bar          : REAL;         (* Stator Chuck Hydraulic Clamping Pressure 5C [bar] *)

    (* Rotary Chuck Direct-Drive High-Resolution Servo Transducers *)
    rChuck_ActualPosition_deg       : REAL;         (* Direct-Drive Rotary Chuck Absolute Angular Position [deg] *)
    rChuck_ActualVelocity_deg_s     : REAL;         (* Direct-Drive Rotary Chuck Rotational Velocity [deg/s] *)
    rChuck_ActualTorque_Nm          : REAL;         (* Direct-Drive Rotary Chuck Servo Electromagnetic Torque [Nm] *)
    bChuck_InPositionFlag           : BOOL;         (* Rotary Chuck Drive In-Position Strobe Flag [-] *)

    (* Stator Alignment, Environmental & Quality Diagnostics Transducers *)
    rStator_DatumRunout_mm          : REAL;         (* Stator Lamination Core Concentricity Radial Runout [mm] *)
    rShieldGas_SupplyPressure_bar   : REAL;         (* Bulk Nitrogen Shielding Gas Supply Manifold Pressure [bar] *)
    rCrossJet_AirPressure_bar       : REAL;         (* Optics Protection Cross-Jet Air Knife Pressure [bar] *)
    rOptics_Transmission_pct        : REAL;         (* Protective Cover Glass Optical Transmission Index [%] *)
    rCollimator_Temp_degC           : REAL;         (* Fiber Laser Collimation Block Thermal Sensor [deg C] *)
    rFocusLens_Temp_degC            : REAL;         (* Galvo Scanning Head F-Theta Focus Lens Temp [deg C] *)
    rChiller_WaterFlow_Lmin         : REAL;         (* Deionized Laser Chiller Coolant Flow Rate [L/min] *)
    rChiller_WaterTemp_degC         : REAL;         (* Deionized Laser Chiller Coolant Supply Temperature [deg C] *)
    rEddyCurrent_Resistance_uOhm    : REAL;         (* 4-Wire Kelvin Weld Joint Electrical Resistance [uOhm] *)
    rStatorSlot_InsulTemp_degC      : REAL;         (* Slot Liner Aramid Paper / PAI Insulation Temperature [deg C] *)
    bPartPresentInChuck             : BOOL;         (* Stator Core Presence Optical Proximity Sensor [-] *)
    bPalletClampedInStation         : BOOL;         (* Transport Pallet Shot-Pin Lock Proximity Switch [-] *)
END_VAR

VAR_OUTPUT
    (* Laser System High-Speed Control Commands *)
    rLaserPower_Cmd_kW              : REAL;         (* Fiber Laser Delivered Power Setpoint Command [kW] *)
    rLaserWobble_Freq_Cmd_Hz        : REAL;         (* Dynamic Galvo Beam Wobble Frequency Command [Hz] *)
    rLaserWobble_Amp_Cmd_mm         : REAL;         (* Dynamic Galvo Beam Wobble Oscillation Amplitude [mm] *)
    bLaserEmission_Enable           : BOOL;         (* High-Speed Laser Gate Modulation Hardware Enable [-] *)
    bLaserFastShutter_Open          : BOOL;         (* Safety Interlocked Fast Optical Shutter Solenoid [-] *)
    bLaserAimingBeam_On             : BOOL;         (* Red Pilot Visible Laser Diode Indicator (635 nm) [-] *)

    (* Direct-Drive Rotary Chuck Motion Commands *)
    rChuck_TargetPosition_deg       : REAL;         (* Rotary Direct-Drive Chuck Motion Target Angle [deg] *)
    rChuck_TargetVelocity_deg_s     : REAL;         (* Rotary Direct-Drive Chuck Motion Profile Velocity [deg/s] *)
    bChuck_MoveExecute              : BOOL;         (* Rotary Chuck Positioning Move Initiate Trigger [-] *)
    bChuck_HoldBrakeRelease         : BOOL;         (* Direct-Drive Chuck Pneumatic Holding Brake Release [-] *)

    (* Hydraulic Collet Clamping & Stator Datum Actuation *)
    bChuck_HydClamp_Sol             : BOOL;         (* Chuck Hydraulic Expanding Collet Clamping Solenoid [-] *)
    bChuck_HydUnclamp_Sol           : BOOL;         (* Chuck Hydraulic Expanding Collet De-Clamping Solenoid [-] *)
    bDatumPin_Extend_Sol            : BOOL;         (* Stator Core Reference Datum Locator Pin Extend [-] *)
    bDatumPin_Retract_Sol           : BOOL;         (* Stator Core Reference Datum Locator Pin Retract [-] *)

    (* Auxiliary Fluids & Optics Protection Actuation *)
    rShieldGas_Flow_Cmd_Lmin        : REAL;         (* Shielding Nitrogen Proportional Flow Valve Command [L/min] *)
    bShieldGas_Purge_Valve          : BOOL;         (* High-Flow Nitrogen Chamber Pre-Flow Purge Valve [-] *)
    bCrossJet_AirKnife_Valve        : BOOL;         (* Optics Protective Air Knife Debris Blast Valve [-] *)
    bCoverGlass_MotorAdvance        : BOOL;         (* Motorized Protective Glass Film Roll Advance Index [-] *)
    bFumeExtraction_FanOn           : BOOL;         (* Laser Fume Evacuation Blower Exhaust Contactor [-] *)

    (* Inspection System Control Triggers *)
    bVision_CaptureStrobe           : BOOL;         (* 3D Profilometer Dual-Sensor Image Capture Strobe [-] *)
    bEddyCurrent_ProbeExtend        : BOOL;         (* 4-Wire Kelvin Inspection Contact Cylinder Extend [-] *)
    bQuarantineDivert_Push          : BOOL;         (* Defect Stator Reject Diverter Cylinder Actuation [-] *)

    (* Real-Time Process State, Quality Indices & Estimations *)
    iCurrentStateIndex              : INT;          (* Deterministic Production FSM Current State Index [-] *)
    iCurrentWeldPairNumber          : INT;          (* Current Hairpin Seam Welding Pair Index (1..96) [-] *)
    iTotalCompletedWelds            : INT;          (* Successfully Welded Hairpin Pairs Count in Stator [-] *)
    rWeldCycleTime_Current_s        : REAL;         (* Active Hairpin Pair Weld Duration Timer [s] *)
    rTotalStatorCycleTime_s         : REAL;         (* Total Stator Floor-to-Floor Processing Duration [s] *)
    rWeldQualityScore_pct           : REAL;         (* Real-Time Multi-Variable Seam Weld Quality Score [%] *)
    rEst_MeltPool_Volume_mm3        : REAL;         (* Cyber-Physical Observer Estimated Molten Nugget Volume [mm3] *)
    rEst_Keyhole_Depth_mm           : REAL;         (* Cyber-Physical Observer Estimated Keyhole Depth [mm] *)
    rEst_JointResistance_uOhm       : REAL;         (* In-Line Estimated Hairpin Weld Joint Resistance [uOhm] *)
    rEst_ThermalInsulMargin_degC    : REAL;         (* Slot Liner Insulation Temperature Safety Margin [deg C] *)

    (* Industrial Status Words & Fault Enunciators *)
    dwStatusWord1                   : DWORD;        (* Subsystem Operational State Bitfield 1 [-] *)
    dwStatusWord2                   : DWORD;        (* Subsystem Operational State Bitfield 2 [-] *)
    dwAlarmWord1_Critical           : DWORD;        (* ISA-18.2 Priority 1 Critical Safety Alarm Bitfield [-] *)
    dwAlarmWord2_High               : DWORD;        (* ISA-18.2 Priority 2 High Process Deviation Bitfield [-] *)
    dwAlarmWord3_Warning            : DWORD;        (* ISA-18.2 Priority 3 Advisory Warning Bitfield [-] *)
    bCellGeneralFault               : BOOL;         (* Master Cell Fault Active Summary Flag [-] *)
    bCellCycleCompleted             : BOOL;         (* Stator 192-Pin (96-Pair) Complete Cycle Done Flag [-] *)
    bCellEmergencyTripped           : BOOL;         (* Safety Circuit or Fast Shutter Emergency Lockout [-] *)
END_VAR
"""
