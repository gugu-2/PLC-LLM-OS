# hpdc_megacasting_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Foundry_HighPressureDieCasting_RealTimeInjection_Thermal
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Advanced Foundry, Metallurgy & Mega-Die Casting (Tier 1 Global Priority Commercial Sector)
 * COMMERCIAL SYSTEM    : 4,000-Ton (40,000 kN) High-Pressure Die Casting (HPDC) Machine for Automotive Gigacasting
 *                       (Structural EV Underbody Castings, Aluminum Alloy AlSi10MnMg / Aural-2)
 * CORE SUBSYSTEMS      :
 *   1. Real-Time Closed-Loop Plunger Shot Injection System:
 *      - Phase 1: Slow wave advancement (0.15 - 0.70 m/s) with parabolic wave crest suppression to eliminate air entrapment
 *      - Phase 2: Ultra-high-speed cavity filling (up to 10.0 m/s, acceleration up to 450 m/s^2, filling within 25 - 55 ms)
 *      - Phase 3: Sub-15 ms ultra-fast intensification pressure rise to 800 bar specific metal pressure for shrinkage compaction
 *   2. Triple Modular Redundant (2oo3 TMR) Instrumentation Architecture:
 *      - Injection Cylinder Head Pressure PT-101A/B/C [bar]
 *      - Injection Cylinder Rod Pressure PT-201A/B/C [bar]
 *      - Optical Absolute High-Speed Plunger Linear Encoders ENC-301A/B/C [mm]
 *      - Cavity Vacuum Absolute Transducers VPT-401A/B/C [mbar]
 *      - Hydraulic Accumulator High-Pressure Transducers PT-501A/B/C [bar]
 *      - Main Tie-Bar Clamping Tonnage Strain Load Cells LC-601A/B/C [kN]
 *      - Melt Shot Sleeve Temperature Thermocouples TT-701A/B/C [deg C]
 *   3. Cyber-Physical Discrete State-Space Estimation & Model Predictive Control (MPC):
 *      - Explicit 8-state, 6-input, 3-disturbance discrete state-space model at Ts = 1.0 ms
 *      - Steady-state Kalman filter innovation update for unmeasured hydraulic and thermal states
 *      - Receding-horizon MPC with unrolled Projected Gradient Descent (PGD) for bumpless velocity-to-pressure switchover
 *   4. Multi-Zone Thermal Die Balancing & In-Mold Solidification Regulation:
 *      - 12 independent pressurized water/oil thermal die tempering zones (Zones 1-6 Fixed Half, Zones 7-12 Moving Half)
 *      - Dynamic internal pulsed cooling channel modulation and robot thermal spray release agent application
 *   5. Deterministic 14-Stage Production Finite State Machine (FSM):
 *      - Complete gigacasting sequence from safety lockup, vacuum evacuation, 3-phase shot, core pull, ejection, to spray
 *   6. ISA-18.2 Multi-Tiered Alarm Engine & Statistical Process Control (SPC):
 *      - Critical HH/H/L/LL trip points, deadbands, bit-packed telemetry, and 30-shot rolling Cp/Cpk quality verification
 *
 * GOVERNING CODES      : IEC 61131-3 3rd Ed., ISA-18.2 Alarm Management, NADCA High Pressure Die Casting Standards
 * CONTROLLER SCAN TIME : Ts = 1.0 ms (1,000 Hz deterministic servo task cycle)
 * ===================================================================================================================== *)

VAR_INPUT
    (* --- 2oo3 TMR Sensor Channels: Shot Cylinder Head Pressure (PT-101) --- *)
    rCylHeadPres_PT101A_In       : REAL;    (* Injection Cylinder Head Hydraulic Pressure Transducer Channel A [bar] *)
    rCylHeadPres_PT101B_In       : REAL;    (* Injection Cylinder Head Hydraulic Pressure Transducer Channel B [bar] *)
    rCylHeadPres_PT101C_In       : REAL;    (* Injection Cylinder Head Hydraulic Pressure Transducer Channel C [bar] *)

    (* --- 2oo3 TMR Sensor Channels: Shot Cylinder Rod Pressure (PT-201) --- *)
    rCylRodPres_PT201A_In        : REAL;    (* Injection Cylinder Rod Hydraulic Pressure Transducer Channel A [bar] *)
    rCylRodPres_PT201B_In        : REAL;    (* Injection Cylinder Rod Hydraulic Pressure Transducer Channel B [bar] *)
    rCylRodPres_PT201C_In        : REAL;    (* Injection Cylinder Rod Hydraulic Pressure Transducer Channel C [bar] *)

    (* --- 2oo3 TMR Sensor Channels: Plunger Axial Linear Position (ENC-301) --- *)
    rPlungerPos_ENC301A_In       : REAL;    (* Plunger Rod Optical Linear Absolute Scale Channel A [mm] *)
    rPlungerPos_ENC301B_In       : REAL;    (* Plunger Rod Optical Linear Absolute Scale Channel B [mm] *)
    rPlungerPos_ENC301C_In       : REAL;    (* Plunger Rod Optical Linear Absolute Scale Channel C [mm] *)

    (* --- 2oo3 TMR Sensor Channels: Cavity Vacuum Absolute Pressure (VPT-401) --- *)
    rCavityVac_VPT401A_In        : REAL;    (* Die Cavity Vacuum Absolute Transducer Channel A [mbar] *)
    rCavityVac_VPT401B_In        : REAL;    (* Die Cavity Vacuum Absolute Transducer Channel B [mbar] *)
    rCavityVac_VPT401C_In        : REAL;    (* Die Cavity Vacuum Absolute Transducer Channel C [mbar] *)

    (* --- 2oo3 TMR Sensor Channels: Hydraulic Accumulator Pressure (PT-501) --- *)
    rAccumPres_PT501A_In         : REAL;    (* High-Speed Piston Accumulator Nitrogen Pressure Channel A [bar] *)
    rAccumPres_PT501B_In         : REAL;    (* High-Speed Piston Accumulator Nitrogen Pressure Channel B [bar] *)
    rAccumPres_PT501C_In         : REAL;    (* High-Speed Piston Accumulator Nitrogen Pressure Channel C [bar] *)

    (* --- 2oo3 TMR Sensor Channels: Main Clamping Force Load Cells (LC-601) --- *)
    rClampForce_LC601A_In        : REAL;    (* Main Die Clamping Tonnage Piezo Load Cell Channel A [kN] *)
    rClampForce_LC601B_In        : REAL;    (* Main Die Clamping Tonnage Piezo Load Cell Channel B [kN] *)
    rClampForce_LC601C_In        : REAL;    (* Main Die Clamping Tonnage Piezo Load Cell Channel C [kN] *)

    (* --- 2oo3 TMR Sensor Channels: Shot Sleeve Melt Temperature (TT-701) --- *)
    rSleeveTemp_TT701A_In        : REAL;    (* Molten Alloy Shot Sleeve Thermocouple Channel A [deg C] *)
    rSleeveTemp_TT701B_In        : REAL;    (* Molten Alloy Shot Sleeve Thermocouple Channel B [deg C] *)
    rSleeveTemp_TT701C_In        : REAL;    (* Molten Alloy Shot Sleeve Thermocouple Channel C [deg C] *)

    (* --- 12-Zone Multi-Channel Thermal Die Balancing Temperatures --- *)
    rDieTemp_Zone01_Fixed_In     : REAL;    (* Fixed Die Half Zone 1 Lower Runner Surface Temperature [deg C] *)
    rDieTemp_Zone02_Fixed_In     : REAL;    (* Fixed Die Half Zone 2 Lower Ingate Region Temperature [deg C] *)
    rDieTemp_Zone03_Fixed_In     : REAL;    (* Fixed Die Half Zone 3 Main Structural Cavity Center [deg C] *)
    rDieTemp_Zone04_Fixed_In     : REAL;    (* Fixed Die Half Zone 4 Upper Cavity Thin Wall Area [deg C] *)
    rDieTemp_Zone05_Fixed_In     : REAL;    (* Fixed Die Half Zone 5 Heavy Shock-Tower Boss Node [deg C] *)
    rDieTemp_Zone06_Fixed_In     : REAL;    (* Fixed Die Half Zone 6 Perimeter Chill Vent Flange [deg C] *)
    rDieTemp_Zone07_Moving_In    : REAL;    (* Moving Die Half Zone 7 Biscuit Ejection Cup Region [deg C] *)
    rDieTemp_Zone08_Moving_In    : REAL;    (* Moving Die Half Zone 8 Lower Structural Rib Area [deg C] *)
    rDieTemp_Zone09_Moving_In    : REAL;    (* Moving Die Half Zone 9 Core Slide Interlock Face A [deg C] *)
    rDieTemp_Zone10_Moving_In    : REAL;    (* Moving Die Half Zone 10 Core Slide Interlock Face B [deg C] *)
    rDieTemp_Zone11_Moving_In    : REAL;    (* Moving Die Half Zone 11 Center Ejector Pin Cluster [deg C] *)
    rDieTemp_Zone12_Moving_In    : REAL;    (* Moving Die Half Zone 12 Vacuum Valve Chill Block [deg C] *)

    (* --- 4-Tie-Bar Structural Strain Extensometers (Platen Tilt / Deflection) --- *)
    rTieBar_Strain_Col1_In       : REAL;    (* Tie-Bar Column 1 Top-Operator Dynamic Strain Extensometer [um] *)
    rTieBar_Strain_Col2_In       : REAL;    (* Tie-Bar Column 2 Top-NonOperator Dynamic Strain Extensometer [um] *)
    rTieBar_Strain_Col3_In       : REAL;    (* Tie-Bar Column 3 Bottom-Operator Dynamic Strain Extensometer [um] *)
    rTieBar_Strain_Col4_In       : REAL;    (* Tie-Bar Column 4 Bottom-NonOperator Dynamic Strain Extensometer [um] *)

    (* --- Hydraulic Auxiliary & Motion Transducers --- *)
    rClampCyl_HydraulicPres_In   : REAL;    (* Main Hydraulic Clamping Cylinder Line Pressure [bar] *)
    rCoreA_HydraulicPres_In      : REAL;    (* Core Slide A Hydraulic Operating Line Pressure [bar] *)
    rCoreB_HydraulicPres_In      : REAL;    (* Core Slide B Hydraulic Operating Line Pressure [bar] *)
    rCoreC_HydraulicPres_In      : REAL;    (* Core Slide C Hydraulic Operating Line Pressure [bar] *)
    rCoreD_HydraulicPres_In      : REAL;    (* Core Slide D Hydraulic Operating Line Pressure [bar] *)
    rEjector_Position_In         : REAL;    (* Hydraulic Multi-Pin Ejector Plate Linear Position [mm] *)
    rEjector_HydraulicPres_In    : REAL;    (* Hydraulic Ejector Cylinder Forward Drive Pressure [bar] *)
    rVacuum_Valve_Position_In    : REAL;    (* High-Speed Hydraulic Chill Vacuum Valve Spool Position [%] *)
    rHydraulic_OilTemp_In        : REAL;    (* Main Hydraulic Power Unit Sump Oil Temperature [deg C] *)
    rHydraulic_TankLevel_In      : REAL;    (* Main Hydraulic Reservoir Fluid Level [%] *)

    (* --- Automation Handshake & Proximity Digital Inputs --- *)
    bCoreA_Extended_LS_In        : BOOL;    (* Core Pull Slide A Fully Inserted Limit Switch [bool] *)
    bCoreA_Retracted_LS_In       : BOOL;    (* Core Pull Slide A Fully Retracted Limit Switch [bool] *)
    bCoreB_Extended_LS_In        : BOOL;    (* Core Pull Slide B Fully Inserted Limit Switch [bool] *)
    bCoreB_Retracted_LS_In       : BOOL;    (* Core Pull Slide B Fully Retracted Limit Switch [bool] *)
    bCoreC_Extended_LS_In        : BOOL;    (* Core Pull Slide C Fully Inserted Limit Switch [bool] *)
    bCoreC_Retracted_LS_In       : BOOL;    (* Core Pull Slide C Fully Retracted Limit Switch [bool] *)
    bCoreD_Extended_LS_In        : BOOL;    (* Core Pull Slide D Fully Inserted Limit Switch [bool] *)
    bCoreD_Retracted_LS_In       : BOOL;    (* Core Pull Slide D Fully Retracted Limit Switch [bool] *)
    bLadle_Robot_Home_In         : BOOL;    (* Dosing Pouring Ladle Robot Arm Retracted to Safe Home [bool] *)
    bLadle_Pour_Completed_In     : BOOL;    (* Dosing Pouring Ladle Cycle Completed Strobe [bool] *)
    rLadle_Poured_Mass_In        : REAL;    (* Measured Dosed Molten Aluminum Ingot Mass [kg] *)
    bExtract_Robot_Clear_In      : BOOL;    (* 6-Axis Casting Extraction Robot Fully Clear of Die Space [bool] *)
    bExtract_Part_Gripped_In     : BOOL;    (* Extraction Robot Vacuum / Mechanical Gripper Confirmed [bool] *)
    bSpray_Robot_Clear_In        : BOOL;    (* Thermal Spray Lubrication Robot Arm Fully Clear of Die Space [bool] *)

    (* --- Safety Enclosure & Interlocks --- *)
    bSafetyGate_Front_Closed_In  : BOOL;    (* Front Perimeter Heavy Protective Safety Door Closed [bool] *)
    bSafetyGate_Rear_Closed_In   : BOOL;    (* Rear Guard Heavy Protective Enclosure Door Closed [bool] *)
    bEmergency_Stop_OK_In        : BOOL;    (* Hardwired Category 4 E-Stop Circuit Healthy [bool] *)
    bHydraulic_Motor_Running_In  : BOOL;    (* Main 350 kW Hydraulic Pump Drive Contactor Running [bool] *)

    (* --- Operator Commands & Mode Selectors --- *)
    bCmd_AutoCycle_Start_In      : BOOL;    (* Automatic Casting Cycle Master Start Command [bool] *)
    bCmd_Cycle_Abort_In          : BOOL;    (* Master Cycle Abort / Graceful Shot Termination [bool] *)
    bCmd_Reset_Alarms_In         : BOOL;    (* Master Alarm Acknowledge and Fault Clear Command [bool] *)
    bCmd_Manual_PlungerFwd_In    : BOOL;    (* Manual Plunger JOG Forward Inching Pushbutton [bool] *)
    bCmd_Manual_PlungerRev_In    : BOOL;    (* Manual Plunger JOG Retract Pushbutton [bool] *)

    (* --- Metallurgical Recipe & Setpoint Parameters --- *)
    rRecipe_Phase1_Velocity_In   : REAL;    (* Phase 1 Slow Wave Plunger Velocity Setpoint [m/s] *)
    rRecipe_Phase1_Stroke_In     : REAL;    (* Phase 1 Slow Shot Cutoff Stroke Position [mm] *)
    rRecipe_Phase2_Velocity_In   : REAL;    (* Phase 2 Ultra-High-Speed Cavity Fill Velocity Setpoint [m/s] *)
    rRecipe_Phase2_CutoffPos_In  : REAL;    (* Phase 2 Injection Complete / Intensification Trigger Stroke [mm] *)
    rRecipe_Phase3_IntensPres_In : REAL;    (* Phase 3 Target Specific Metal Intensification Pressure [bar] *)
    rRecipe_Phase3_RiseTime_In   : REAL;    (* Phase 3 Maximum Permissible Pressure Rise Time Setpoint [ms] *)
    rRecipe_Phase3_DwellTime_In  : REAL;    (* Phase 3 Squeeze / Intensification Holding Duration [s] *)
    rRecipe_TargetClampForce_In  : REAL;    (* Target Die Lockup Clamping Tonnage Setpoint [kN] *)
    rRecipe_TargetBiscuit_In     : REAL;    (* Nominal Target Solidified Biscuit Thickness Setpoint [mm] *)
    rRecipe_VacuumSetpoint_In    : REAL;    (* Target Cavity Evacuation Absolute Pressure Limit [mbar] *)
    rRecipe_CoolingDuration_In   : REAL;    (* In-Die Solidification Cooling Cycle Duration [s] *)
END_VAR

VAR_OUTPUT
    (* --- Real-Time Servo Actuator Analog Output Commands --- *)
    rServo_ShotSpool_Cmd_Out     : REAL;    (* Closed-Loop High-Response Shot Servo Valve Spool Position Command [%] *)
    rFastValv_Cartridge_Cmd_Out  : REAL;    (* High-Speed Accumulator Dump Cartridge Proportional Throttle [%] *)
    rIntensifier_Valve_Cmd_Out   : REAL;    (* Ultra-Fast Intensifier Multiplier Actuation Valve Command [%] *)
    rVacuum_Isolation_Cmd_Out    : REAL;    (* High-Flow Vacuum Line Proportional Isolation Valve Command [%] *)
    rClamp_Proportional_Cmd_Out  : REAL;    (* Main Die Clamping Proportional Hydraulic Pressure Command [%] *)
    rEjector_Servo_Cmd_Out       : REAL;    (* Hydraulic Multi-Pin Ejector Forward Velocity/Force Command [%] *)

    (* --- Multi-Zone Die Thermal Balancing Valve Outputs (PWM Duty Cycle %) --- *)
    rDieCooling_PWM_Zone01_Out   : REAL;    (* Thermal Channel Zone 1 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone02_Out   : REAL;    (* Thermal Channel Zone 2 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone03_Out   : REAL;    (* Thermal Channel Zone 3 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone04_Out   : REAL;    (* Thermal Channel Zone 4 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone05_Out   : REAL;    (* Thermal Channel Zone 5 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone06_Out   : REAL;    (* Thermal Channel Zone 6 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone07_Out   : REAL;    (* Thermal Channel Zone 7 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone08_Out   : REAL;    (* Thermal Channel Zone 8 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone09_Out   : REAL;    (* Thermal Channel Zone 9 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone10_Out   : REAL;    (* Thermal Channel Zone 10 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone11_Out   : REAL;    (* Thermal Channel Zone 11 Solenoid Cooling Valve Duty Cycle [%] *)
    rDieCooling_PWM_Zone12_Out   : REAL;    (* Thermal Channel Zone 12 Solenoid Cooling Valve Duty Cycle [%] *)

    (* --- Digital Actuation Commands & Robot Interlocks --- *)
    bVacuum_Pump_Start_Out       : BOOL;    (* High-Volume Multi-Stage Vacuum Pump Run Command [bool] *)
    bChillVent_SealValve_Out     : BOOL;    (* Hydraulic Chill Vent Rapid Seal Valve Actuation [bool] *)
    bCoreA_Insert_Cmd_Out        : BOOL;    (* Hydraulic Core Slide A Advance Insert Directional Solenoid [bool] *)
    bCoreA_Retract_Cmd_Out       : BOOL;    (* Hydraulic Core Slide A Retract Directional Solenoid [bool] *)
    bCoreB_Insert_Cmd_Out        : BOOL;    (* Hydraulic Core Slide B Advance Insert Directional Solenoid [bool] *)
    bCoreB_Retract_Cmd_Out       : BOOL;    (* Hydraulic Core Slide B Retract Directional Solenoid [bool] *)
    bCoreC_Insert_Cmd_Out        : BOOL;    (* Hydraulic Core Slide C Advance Insert Directional Solenoid [bool] *)
    bCoreC_Retract_Cmd_Out       : BOOL;    (* Hydraulic Core Slide C Retract Directional Solenoid [bool] *)
    bCoreD_Insert_Cmd_Out        : BOOL;    (* Hydraulic Core Slide D Advance Insert Directional Solenoid [bool] *)
    bCoreD_Retract_Cmd_Out       : BOOL;    (* Hydraulic Core Slide D Retract Directional Solenoid [bool] *)
    bLadle_Robot_Permissive_Out  : BOOL;    (* Handshake Permissive to Dosing Robot to Pour Melt [bool] *)
    bExtract_Robot_Permissive_Out: BOOL;    (* Handshake Permissive to 6-Axis Robot to Extract Casting [bool] *)
    bSpray_Robot_Permissive_Out  : BOOL;    (* Handshake Permissive to Spray Robot to Apply Lubricant [bool] *)
    bAccumulator_Dump_Safe_Out   : BOOL;    (* Emergency Nitrogen Accumulator Hydraulic Dump De-energize [bool] *)

    (* --- Process Quality Telemetry & Casting Verification Metrics --- *)
    rBiscuitThickness_Meas_Out   : REAL;    (* Final Solidified Biscuit Measured Thickness [mm] *)
    rPeakShotVelocity_Meas_Out   : REAL;    (* Measured Maximum Plunger Velocity Achieved in Phase 2 [m/s] *)
    rIntensRiseTime_Meas_Out     : REAL;    (* Measured Pressure Rise Time from P2 to P3 Target [ms] *)
    rPeakIntensPres_Meas_Out     : REAL;    (* Measured Peak Specific Metal Intensification Pressure [bar] *)
    rCavityVacuum_AtShot_Out     : REAL;    (* Measured Absolute Cavity Vacuum at Plunger Launch [mbar] *)
    rCycleDuration_Seconds_Out   : REAL;    (* Total Elapsed Cycle Time from Clamp Lockup to Eject [s] *)
    bPartQuality_Accept_Out      : BOOL;    (* Statistical Process Control Casting Acceptable Verdict [bool] *)
    bPartQuality_Scrap_Out       : BOOL;    (* Casting Out-of-Tolerance Scrap Reject Flag [bool] *)

    (* --- ISA-18.2 Bit-Packed Diagnostic and Status Telemetry Words --- *)
    dwStatus_FSM_Phase_Out       : DWORD;   (* 32-Bit FSM State and Sequence Operational Word [dword] *)
    dwStatus_Motion_State_Out    : DWORD;   (* 32-Bit Real-Time Motion and Hydraulic Actuator Telemetry [dword] *)
    dwAlarm_Critical_Trips_Out   : DWORD;   (* 32-Bit ISA-18.2 Priority 1 Critical Safety Shutdown Alarms [dword] *)
    dwAlarm_Warnings_Out         : DWORD;   (* 32-Bit ISA-18.2 Priority 2/3 Process Deviation Warnings [dword] *)
    dwTMR_Sensor_Health_Out      : DWORD;   (* 32-Bit 2oo3 Triple Modular Redundancy Sensor Channel Status [dword] *)
    dwSPC_Quality_Flags_Out      : DWORD;   (* 32-Bit Statistical Process Quality Classification Flags [dword] *)
END_VAR
"""
