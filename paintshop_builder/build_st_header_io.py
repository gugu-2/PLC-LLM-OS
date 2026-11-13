# paintshop_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Automotive_PaintShop_RoboticBellAtomizer_AirFlowBalance
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
SYSTEM: AUTOMOTIVE HIGH-VOLUME MANUFACTURING (BODY-IN-WHITE / CLEARCOAT PAINT SHOP)
SUBSYSTEMS:
  - HIGH-SPEED ELECTROSTATIC ROTARY BELL ATOMIZERS (65,000 [rpm] AIR TURBINE, -90 [kV] DC CASCADE)
  - CLOSED-LOOP POSITIVE DISPLACEMENT MICRO-GEAR PUMP PAINT FLOW DOSING (50 - 600 [mL/min])
  - DUAL SHAPING AIR SHROUDS (INNER PATTERN FOCUS / OUTER SPRAY ENVELOPE OVERLAP 0.5 - 5.0 [bar])
  - DOWNDRAFT RECIRCULATION LAMINAR AIR FLOW BALANCING (0.35 [m/s] +/- 0.02 [m/s], DELTA-P 12.5 [Pa])
  - REGENERATIVE THERMAL OXIDIZER (RTO) VOC ABATEMENT EMISSION MONITORING (< 25% LEL SAFETY INTERLOCK)
  - RAPID COLOR-CHANGE VALVE BLOCK (CCV) CHOP-CHOP SOLVENT PURGE & HIGH-VELOCITY AIR DRY (< 12 [s])
  - SUB-5 [ms] FAST ELECTROSTATIC SPARK ARC FLASH QUENCH & VOLTAGE COLLAPSE SUPPRESSION
  - FIRST-PRINCIPLES CYBER-PHYSICAL DISCRETE STATE-SPACE MODEL (8-STATE, 6-INPUT, 3-DISTURBANCE)
  - MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD) FOR DFT (35 [um] +/- 2 [um])
  - 2oo3 TRIPLE MODULAR REDUNDANT (TMR) SENSOR VOTING WITH DYNAMIC DISCREPANCY TIMERS
  - DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
  - ISA-18.2 MULTI-TIER PROCESS ALARM HIERARCHY WITH BIT-PACKED 32-BIT STATUS & FAULT WORDS
====================================================================================================
*)

VAR_INPUT
    (* Digital Supervisory Commands & Master Safety Permissives *)
    bEnable                         : BOOL;         (* Master Execution Enable & Execution Scheduler Permissive [-] *)
    bBoothPrePurgeCmd               : BOOL;         (* Initiate Booth Ventilation 4-Volume Pre-Purge Sequence [-] *)
    bStartCycleCmd                  : BOOL;         (* Automatic Body-in-White Spray Cycle Start Command [-] *)
    bStopCycleCmd                   : BOOL;         (* Orderly Cycle Stop & Bell Cup Cleaning Sequence Command [-] *)
    bEmergencyStop                  : BOOL;         (* Safety Instrumented System (SIS) Hardwired E-Stop Active Low [-] *)
    bResetFaults                    : BOOL;         (* Alarm Acknowledge & First-Out Latch Reset Command [-] *)
    bAckAlarm                       : BOOL;         (* ISA-18.2 Process Alarm Silence & Acknowledge Pushbutton [-] *)
    bColorChangeReq                 : BOOL;         (* Initiate High-Speed Color Change Valve (CCV) Purge (< 12 s) [-] *)
    bTipWashReq                     : BOOL;         (* Atomizer Bell Cup Tip Wash & Spin Dry Request [-] *)
    bRobotTriggerPermissive         : BOOL;         (* Articulated 6-Axis Robot Contouring In-Position Permissive [-] *)
    bEdgeWrapCompensationEnable     : BOOL;         (* Enable Dynamic Edge Wrap & Faraday Cage Recess Compensation [-] *)
    bRecessZoneActive               : BOOL;         (* Robot TCP Inside Body Cavity (A/B/C Pillar / Trunk Gutter) [-] *)
    bMaintenancePurgeOverride       : BOOL;         (* Maintenance Manual Solvent Line Purge Mode Permissive [-] *)

    (* Real-Time Setpoints & Process Targets *)
    rTurbineSpeedSP_rpm             : REAL;         (* Bell Cup Turbine Target Rotational Velocity: 10000 - 65000 [rpm] *)
    rHighVoltageSP_kV               : REAL;         (* Electrostatic Cascade Direct Potential Setpoint: -30.0 - -90.0 [kV] *)
    rPaintFlowSP_mlpm               : REAL;         (* Closed-Loop Paint Volumetric Dosing Target: 50.0 - 600.0 [mL/min] *)
    rInnerShapingAirSP_bar          : REAL;         (* Inner Shroud Shaping Air Pressure Setpoint: 0.50 - 5.00 [bar] *)
    rOuterShapingAirSP_bar          : REAL;         (* Outer Shroud Shaping Air Pressure Setpoint: 0.50 - 5.00 [bar] *)
    rDowndraftVelocitySP_mps        : REAL;         (* Target Downdraft Recirculation Laminar Velocity: 0.35 [m/s] *)
    rDowndraftPressSP_Pa            : REAL;         (* Ceiling Plenum to Grating Differential Static Pressure: 12.5 [Pa] *)
    rTargetDFT_um                   : REAL;         (* Automotive Body Target Cured Dry Film Thickness: 35.0 [um] *)
    rRobotTCPVelocity_mps           : REAL;         (* Robot Tool Center Point Vector Linear Velocity: 0.10 - 2.00 [m/s] *)
    rRobotTCPDistance_mm            : REAL;         (* Bell Cup Atomizer Rim to Metal Substrate Standoff Distance: 150 - 300 [mm] *)
    rPaintSolidsContent_pct         : REAL;         (* Clearcoat / Basecoat Solids Volume Fraction: 30.0 - 65.0 [%] *)
    rPaintViscosity_mPas            : REAL;         (* Real-Time Inline Fluid Dynamic Viscosity: 40.0 - 180.0 [mPa.s] *)
    rPaintDensity_kgpm3             : REAL;         (* Wet Paint Density at Application Temperature: 950.0 - 1250.0 [kg/m3] *)
    rPaintResistivity_MOhmcm        : REAL;         (* Paint Bulk Electrical Specific Resistivity: 0.10 - 15.00 [MOhm.cm] *)
    rRtoCoreTemp_degC               : REAL;         (* Regenerative Thermal Oxidizer Combustion Core Temp: 750.0 - 950.0 [deg C] *)

    (* Primary 2oo3 Triple Modular Redundancy (TMR) Analog Sensor Channels *)
    (* Channel Group 1: High-Speed Optical Bell Turbine Speed Pickups ST-101A/B/C *)
    rST_101A_TurbineSpeed_rpm       : REAL;         (* Bell Turbine Optical Pulse Frequency Transmitter 101A [rpm] *)
    rST_101B_TurbineSpeed_rpm       : REAL;         (* Bell Turbine Optical Pulse Frequency Transmitter 101B [rpm] *)
    rST_101C_TurbineSpeed_rpm       : REAL;         (* Bell Turbine Optical Pulse Frequency Transmitter 101C [rpm] *)

    (* Channel Group 2: High-Voltage Electrostatic Cascade Divider VT-201A/B/C *)
    rVT_201A_HighVoltage_kV         : REAL;         (* Electrostatic High Voltage Divider Cell 201A [kV] *)
    rVT_201B_HighVoltage_kV         : REAL;         (* Electrostatic High Voltage Divider Cell 201B [kV] *)
    rVT_201C_HighVoltage_kV         : REAL;         (* Electrostatic High Voltage Divider Cell 201C [kV] *)

    (* Channel Group 3: Coriolis Micro-Flow Mass & Density Transmitters FT-301A/B/C *)
    rFT_301A_PaintFlow_mlpm         : REAL;         (* Micro-Coriolis Mass Flowmeter Transmitter 301A [mL/min] *)
    rFT_301B_PaintFlow_mlpm         : REAL;         (* Micro-Coriolis Mass Flowmeter Transmitter 301B [mL/min] *)
    rFT_301C_PaintFlow_mlpm         : REAL;         (* Micro-Coriolis Mass Flowmeter Transmitter 301C [mL/min] *)

    (* Channel Group 4: Downdraft Static Differential Pressure Transmitters PT-401A/B/C *)
    rPT_401A_DowndraftPress_Pa      : REAL;         (* Cleanroom Plenum to Under-Grating Delta-P Cell 401A [Pa] *)
    rPT_401B_DowndraftPress_Pa      : REAL;         (* Cleanroom Plenum to Under-Grating Delta-P Cell 401B [Pa] *)
    rPT_401C_DowndraftPress_Pa      : REAL;         (* Cleanroom Plenum to Under-Grating Delta-P Cell 401C [Pa] *)

    (* Secondary Process Transducers & Facility Safety Telemetry *)
    rIT_202_HVCurrent_uA            : REAL;         (* High Voltage Return Leakage & Corona Current: 0.0 - 500.0 [uA] *)
    rPT_302_PaintLinePress_bar      : REAL;         (* Dosing Gear Pump Discharge Hydraulic Line Pressure: 0.0 - 25.0 [bar] *)
    rPT_501_DriveAirPress_bar       : REAL;         (* Atomizer Turbine Drive Air Header Regulated Supply: 0.0 - 10.0 [bar] *)
    rPT_502_BrakeAirPress_bar       : REAL;         (* Atomizer Turbine Dynamic Braking Air Header Supply: 0.0 - 10.0 [bar] *)
    rAT_601_ExhaustVOC_LEL_pct      : REAL;         (* Booth Exhaust Duct Flammable Solvent Concentration: 0.0 - 100.0 [%LEL] *)
    rTT_602_BoothTemp_degC          : REAL;         (* Conditioned Paint Booth Air Temperature: 18.0 - 30.0 [deg C] *)
    rRH_603_BoothHumidity_pct       : REAL;         (* Conditioned Paint Booth Air Relative Humidity: 40.0 - 85.0 [%] *)
    rVT_701_DowndraftVelocity_mps   : REAL;         (* Anemometer Array Cross-Sectional Downward Air Speed: 0.0 - 1.00 [m/s] *)
    rSolventSupplyPress_bar         : REAL;         (* Rapid Color Change Block Solvent Supply Pressure: 2.0 - 12.0 [bar] *)
    rPurgeAirSupplyPress_bar        : REAL;         (* Rapid Color Change Block Air Purge Supply Pressure: 2.0 - 10.0 [bar] *)
END_VAR

VAR_OUTPUT
    (* Operational State Flags & Sequence Status *)
    bSystemReady                    : BOOL;         (* All Environmental, Safety & Turbine Permissives Satisfied [-] *)
    bCycleActive                    : BOOL;         (* Automotive Body Spray Execution Active [-] *)
    bCycleComplete                  : BOOL;         (* Car Body Trajectory Application Successfully Concluded [-] *)
    bPrePurgeDone                   : BOOL;         (* Booth Ventilation 4-Exchange Volume Pre-Purge Certified [-] *)
    bColorChangeActive              : BOOL;         (* Rapid Color Change Valve Block Flush/Chop Cycle Active [-] *)
    bTipWashActive                  : BOOL;         (* Atomizer Bell Cup Tip Wash Sequence In Progress [-] *)
    bArcQuenchTripped               : BOOL;         (* Fast Electrostatic Arc Flash Detection & Hard Quench Tripped [-] *)
    bMasterFault                    : BOOL;         (* Master Safety or Unrecoverable Hardware Fault Active [-] *)
    bWarningActive                  : BOOL;         (* Non-Critical Degraded Mode or Process Parameter Deviation Active [-] *)
    nFSMState                       : INT;          (* Current Active 14-Stage Deterministic FSM State Identifier [0..13] [-] *)

    (* Analog Actuator Control References *)
    rTurbineDriveAirCmd_pct         : REAL;         (* Proportional Drive Air Pressure Control Valve Output: 0.0 - 100.0 [%] *)
    rTurbineBrakeAirCmd_pct         : REAL;         (* Proportional Dynamic Braking Air Control Valve Output: 0.0 - 100.0 [%] *)
    rHighVoltageCmd_pct             : REAL;         (* High Voltage Cascade Solid-State PWM Regulator Reference: 0.0 - 100.0 [%] *)
    rGearPumpSpeedCmd_rpm           : REAL;         (* Micro-Dosing Gear Pump Precision Servo Speed Command: 0.0 - 250.0 [rpm] *)
    rInnerShapingAirCmd_bar         : REAL;         (* Inner Shroud Shaping Air Closed-Loop Regulator Setpoint: 0.0 - 6.0 [bar] *)
    rOuterShapingAirCmd_bar         : REAL;         (* Outer Shroud Shaping Air Closed-Loop Regulator Setpoint: 0.0 - 6.0 [bar] *)
    rDowndraftDamperCmd_pct         : REAL;         (* Cleanroom Recirculation / Makeup VAV Air Damper Position: 0.0 - 100.0 [%] *)
    rRtoPurgeDamperCmd_pct          : REAL;         (* RTO VOC Abatement Exhaust Dilution Fresh Air Damper: 0.0 - 100.0 [%] *)

    (* Digital Solenoid Actuator Commands *)
    bPaintTriggerValve              : BOOL;         (* Bell Atomizer Fluid Delivery Tip Needle Trigger Valve Open [-] *)
    bSolventFlushValve              : BOOL;         (* CCV Fast Solvent Flush Injection Solenoid Valve Open [-] *)
    bPushOutAirValve                : BOOL;         (* CCV High-Velocity Push-Out Drying Compressed Air Valve Open [-] *)
    bDumpWasteValve                 : BOOL;         (* CCV Solvent/Paint Sludge Dump Valve to Recovery Sump Open [-] *)
    bTipWashSolventValve            : BOOL;         (* External Bell Cup Circumferential Solvent Needle Valve Open [-] *)
    bTipWashAirDryValve             : BOOL;         (* External Bell Cup High-Pressure Air Drying Blast Solenoid Open [-] *)
    bSafetyGroundRelay              : BOOL;         (* High Voltage Direct Bleed-Down Discharge Safety Relay Closed [-] *)
    bBoothPurgeFanRun               : BOOL;         (* Cleanroom Makeup & Recirculation Fan VFD Run Command [-] *)
    bExhaustRtoFanRun               : BOOL;         (* Exhaust Duct VOC Extraction Fan VFD Run Command [-] *)

    (* Cyber-Physical Process Observers & KPIs *)
    rVotedTurbineSpeed_rpm          : REAL;         (* Validated 2oo3 TMR High-Speed Bell Turbine Angular Velocity [rpm] *)
    rVotedHighVoltage_kV            : REAL;         (* Validated 2oo3 TMR Electrostatic Potential Across Substrate Gap [kV] *)
    rVotedPaintFlow_mlpm            : REAL;         (* Validated 2oo3 TMR Mass Flow Dosing Rate to Atomizer [mL/min] *)
    rVotedDowndraftPress_Pa         : REAL;         (* Validated 2oo3 TMR Downdraft Plenum Static Pressure Drop [Pa] *)
    rEstimatedDFT_um                : REAL;         (* First-Principles Cyber-Physical Estimated Dry Film Thickness [um] *)
    rTransferEfficiency_pct         : REAL;         (* Computed Real-Time Electrostatic Paint Transfer Efficiency [%] *)
    rDropletSauterDia_um            : REAL;         (* Hydrodynamic Droplet Atomization Sauter Mean Diameter D32 [um] *)
    rSprayFanWidth_mm               : REAL;         (* Hydrodynamic Spray Pattern Outer Diameter at Substrate [mm] *)
    rVOCExhaustRate_gpm             : REAL;         (* Real-Time Solvent Volatile Organic Carbon Emission Rate [g/min] *)
    rPaintMassDelivered_g           : REAL;         (* Totalized Wet Paint Mass Delivered During Active Pass [g] *)
    rSolventVolPurged_mL            : REAL;         (* Totalized Solvent Volume Purged During Color Change [mL] *)
    rColorChangeCycleTime_s         : REAL;         (* Elapsed Execution Duration of Rapid Color Change Sequence [s] *)

    (* Bit-Packed 32-Bit Telemetry, Health & ISA-18.2 Alarm Words *)
    dwStatusWord1                   : DWORD;        (* System Permissives, Robot Handshake & FSM Operating Telemetry *)
    dwStatusWord2                   : DWORD;        (* TMR Sensor Channel Health, Degraded States & Override Flags *)
    dwAlarmWord1                    : DWORD;        (* ISA-18.2 Process Parameter Alarms (Turbine, HV, Flow, Pressure) *)
    dwAlarmWord2                    : DWORD;        (* ISA-18.2 Environmental, Safety & Abatement Alarms (VOC, RTO, Arc) *)
    dwFirstOutWord                  : DWORD;        (* Latched First-Out Process Trip & Emergency Shutdown Root Cause *)
END_VAR
"""
