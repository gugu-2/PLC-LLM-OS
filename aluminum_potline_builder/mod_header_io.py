# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/mod_header_io.py
Declares Header, VAR_INPUT, and VAR_OUTPUT for FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance.
"""

def generate_header_io():
    return '''FUNCTION_BLOCK FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Heavy Non-Ferrous Smelting & Primary Metals (Tier 1 Global Refining)
 * TARGET INDUSTRIAL SYSTEM     : 500 kA Hall-Heroult Prebake Carbon Anode Reduction Cell / Potline Automation
 * FUNCTION BLOCK               : FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance
 * DESIGN STANDARDS             : IEC 61131-3 3rd Ed., IEEE 841, NFPA 70E, ISA-18.2, ANSI/ISA-88 Batch/Discrete States
 * CYBER-PHYSICAL RIGOR         : 6x6 Discrete Electrochemical State-Space Model (A, B, C, D) with Innovation Observer (L),
 *                                Receding-Horizon Decoupled MPC with 10-Iteration Unrolled Projected Gradient Descent (PGD),
 *                                Quadruple 2oo3 Triple Modular Redundancy (TMR) Sensor Suites with 300 ms Discrepancy Timers,
 *                                Dynamic Pseudo-Resistance (R_pot = (V_cell - E_emf) / I_line), Faradaic Alumina Dissolution,
 *                                Superheat and Cryolite Ratio (CR) Equilibrium Tracking, Rolling Polynomial AE Slope Observer,
 *                                Dynamic Anode Beam Rocking Sequence, 14-Stage Production FSM (States 0..13), and 32-Bit Telemetry.
 * RATED CELL SPECIFICATIONS    : 500 kA Line Current, 4.15 V Nominal Cell Voltage, 955 deg C Electrolyte Temperature,
 *                                2.2 - 2.8 wt% Alumina Band, 40-45 mm Anode-Cathode Distance (ACD), 4 Point Feeders per Pot.
 * ===================================================================================================================== *)

VAR_INPUT
    (* ==================== 2oo3 TRIPLE MODULAR REDUNDANT SENSORS (TMR) ==================== *)
    rCellVoltage_CH1_V              : REAL; (* Pot Cathode-to-Anode Cell Voltage Tap Transmitter Channel 1 [V] *)
    rCellVoltage_CH2_V              : REAL; (* Pot Cathode-to-Anode Cell Voltage Tap Transmitter Channel 2 [V] *)
    rCellVoltage_CH3_V              : REAL; (* Pot Cathode-to-Anode Cell Voltage Tap Transmitter Channel 3 [V] *)

    rLineCurrent_CH1_kA             : REAL; (* Potline 500 kA DC Transductor / Rogowski Sensor Channel 1 [kA] *)
    rLineCurrent_CH2_kA             : REAL; (* Potline 500 kA DC Transductor / Rogowski Sensor Channel 2 [kA] *)
    rLineCurrent_CH3_kA             : REAL; (* Potline 500 kA DC Transductor / Rogowski Sensor Channel 3 [kA] *)

    rBathTemp_CH1_degC              : REAL; (* Molten Cryolite Immersion Thermocouple / Pyrometer Channel 1 [deg C] *)
    rBathTemp_CH2_degC              : REAL; (* Molten Cryolite Immersion Thermocouple / Pyrometer Channel 2 [deg C] *)
    rBathTemp_CH3_degC              : REAL; (* Molten Cryolite Immersion Thermocouple / Pyrometer Channel 3 [deg C] *)

    rBeamPos_CH1_mm                 : REAL; (* Anode Beam Absolute Linear Optical Encoder Channel 1 [mm] *)
    rBeamPos_CH2_mm                 : REAL; (* Anode Beam Absolute Linear Optical Encoder Channel 2 [mm] *)
    rBeamPos_CH3_mm                 : REAL; (* Anode Beam Absolute Linear Optical Encoder Channel 3 [mm] *)

    (* ==================== AUXILIARY PROCESS SENSORS & TRANSDUCERS ==================== *)
    rCathodeMetalLevel_cm           : REAL; (* Liquid Molten Aluminum Metal Pad Ultrasonic/Manual Sounding Level [cm] *)
    rFeederAirSupplyPress_bar       : REAL; (* Point Feeder Pneumatic Actuation Air Header Pressure [bar] *)
    rExhaustDuctDeltaP_Pa           : REAL; (* Cell Gas Hooding Exhaust Ductwork Differential Pressure [Pa] *)
    rExhaustGasTemp_degC            : REAL; (* Dry Scrubbing Cell Offgas Exhaust Duct Temperature [deg C] *)
    rAlF3HopperWeight_kg            : REAL; (* Cell Aluminum Fluoride (AlF3) Gravity Metering Hopper Load Cell [kg] *)
    rAluminaSiloLevel_pct           : REAL; (* Secondary Smelter Alumina Local Intermediate Day-Bin Level [%] *)
    rAnodeCurrentDistribution_pct   : REAL; (* Anode Rod Individual Current Uniformity Balance Index [%] *)
    rCathodeShellTemp_degC          : REAL; (* External Carbon/Steel Pot Shell Skin Thermal Sensor [deg C] *)

    (* ==================== DIGITAL INTERLOCKS & HARDWIRED DISCRETES ==================== *)
    bDI_AnodeHoistUpperLimit_LS     : BOOL; (* Anode Beam Mechanical Upper Travel Limit Hardwired Proximity Switch [-] *)
    bDI_AnodeHoistLowerLimit_LS     : BOOL; (* Anode Beam Mechanical Lower Travel Limit Hardwired Proximity Switch [-] *)
    bDI_AnodeHoistMotorOverload     : BOOL; (* Anode Beam Hoist Motor Thermal-Magnetic Overload Contactor Trip [-] *)
    bDI_PotBypassSwitchClosed       : BOOL; (* Potline High-Current Shorting Busbar Bypass Wedge Engaged Switch [-] *)
    bDI_TappingSuctionWandEngaged   : BOOL; (* Vacuum Crucible Siphon Tapping Wand Positioned in Metal Pad [-] *)
    bDI_AnodeChangerCraneInPotArea  : BOOL; (* Overhead Multi-Purpose Pot Tending Crane Zone Interlock Flag [-] *)
    bDI_EmergencyStop_PB            : BOOL; (* Local Pot Control Cubicle Main Hardwired Emergency Stop E-Stop [-] *)
    bDI_PointFeederCrustBreaker1_Jam: BOOL; (* Pneumatic Point Feeder #1 Crust Breaker Chisel Jam Alarm [-] *)
    bDI_PointFeederCrustBreaker2_Jam: BOOL; (* Pneumatic Point Feeder #2 Crust Breaker Chisel Jam Alarm [-] *)
    bDI_PointFeederCrustBreaker3_Jam: BOOL; (* Pneumatic Point Feeder #3 Crust Breaker Chisel Jam Alarm [-] *)
    bDI_PointFeederCrustBreaker4_Jam: BOOL; (* Pneumatic Point Feeder #4 Crust Breaker Chisel Jam Alarm [-] *)

    (* ==================== OPERATOR COMMANDS & RECIPE SETPOINTS ==================== *)
    bCmd_AutoModeEnable             : BOOL; (* Potline Central SCADA Supervisory Auto Control Enable [-] *)
    bCmd_StartElectrolysis          : BOOL; (* Operator Command: Initiate Pot Electrolysis Sequence [-] *)
    bCmd_StopCycle                  : BOOL; (* Operator Command: Initiate Controlled De-energization / Standby [-] *)
    bCmd_AnodeChangeRequest         : BOOL; (* Operator Command: Enter Carbon Anode Block Replacement Protocol [-] *)
    bCmd_MetalTapRequest            : BOOL; (* Operator Command: Enter Vacuum Crucible Metal Tapping Protocol [-] *)
    bCmd_SuppressAnodeEffectManual  : BOOL; (* Operator Command: Trigger Immediate Manual Anode Effect Suppress [-] *)
    bCmd_ResetTrip                  : BOOL; (* Operator Command: Reset Latched Process Trips and Fault Lockouts [-] *)
    bCmd_AcknowledgeAlarm           : BOOL; (* Operator Command: Acknowledge Active ISA-18.2 Process Alarms [-] *)
    bCmd_ManualOverride             : BOOL; (* Operator Command: Enable Manual Jogging & Feeder Pulse Overrides [-] *)

    rSet_TargetResistance_uOhm      : REAL; (* Recipe Baseline Target Pot Pseudo-Resistance Setpoint [micro-Ohm] *)
    rSet_TargetAlumina_pct          : REAL; (* Recipe Nominal Dissolved Alumina Concentration Setpoint [wt%] *)
    rSet_TargetBathTemp_degC        : REAL; (* Recipe Nominal Molten Electrolyte Bath Temperature Setpoint [deg C] *)
    rSet_TargetACD_mm               : REAL; (* Recipe Target Anode-Cathode Distance Base Setpoint [mm] *)
    rSet_AnodeBeamManualJog_mm      : REAL; (* Operator Manual Increment Jog Step Command for Hoist [mm] *)
    rSet_AlF3AdditionRatio_pct      : REAL; (* Recipe AlF3 Chemical Addition Target Trim Ratio [%] *)
    rCycleTime_sec                  : REAL; (* Discrete Execution Task Period / Scan Time Delta-T [s] *)
END_VAR

VAR_OUTPUT
    (* ==================== ACTUATOR POSITIONING & FIRING COMMANDS ==================== *)
    rCmd_AnodeBeamHoistPulse_mm     : REAL; (* Electromechanical Hoist Motor Incremental Travel Position Command [mm] *)
    bCmd_AnodeBeamHoistUp           : BOOL; (* Discrete Hoist Inverter Upward Travel Contactor Command [-] *)
    bCmd_AnodeBeamHoistDown         : BOOL; (* Discrete Hoist Inverter Downward Travel Contactor Command [-] *)
    rCmd_PointFeederPulseRate_ppm   : REAL; (* Alumina Point Feeder Modulated Pulse Firing Frequency [pulses/min] *)
    bCmd_PointFeederFire1           : BOOL; (* Solenoid Valve Pulse: Volumetric Alumina Feeder Shot #1 [-] *)
    bCmd_PointFeederFire2           : BOOL; (* Solenoid Valve Pulse: Volumetric Alumina Feeder Shot #2 [-] *)
    bCmd_PointFeederFire3           : BOOL; (* Solenoid Valve Pulse: Volumetric Alumina Feeder Shot #3 [-] *)
    bCmd_PointFeederFire4           : BOOL; (* Solenoid Valve Pulse: Volumetric Alumina Feeder Shot #4 [-] *)
    bCmd_CrustBreakerPunch1         : BOOL; (* High-Force Pneumatic Chisel Punch Cylinder #1 Command [-] *)
    bCmd_CrustBreakerPunch2         : BOOL; (* High-Force Pneumatic Chisel Punch Cylinder #2 Command [-] *)
    bCmd_CrustBreakerPunch3         : BOOL; (* High-Force Pneumatic Chisel Punch Cylinder #3 Command [-] *)
    bCmd_CrustBreakerPunch4         : BOOL; (* High-Force Pneumatic Chisel Punch Cylinder #4 Command [-] *)
    rCmd_AlF3AdditionDose_pct       : REAL; (* Aluminum Fluoride Gravity Hopper Vibratory Feeder PWM Duty [%] *)
    rCmd_ExhaustDamperPosition_pct  : REAL; (* Cell Gas Exhaust Modulating Butterfly Damper Actuator Position [%] *)
    bCmd_PotlineBypassShuntWedgeFire: BOOL; (* Emergency Potline Circuit Shunting Bypass Actuator Command [-] *)
    bCmd_AnodeEffectHornStrobe      : BOOL; (* High-Priority Anode Effect Audible Horn & Flashing Strobe Command [-] *)

    (* ==================== SYNTHESIZED PROCESS TELEMETRY & STATE ESTIMATION ==================== *)
    rPot_VotedCellVoltage_V         : REAL; (* TMR Voted Cell Operating Voltage [V] *)
    rPot_VotedLineCurrent_kA        : REAL; (* TMR Voted Potline 500 kA Total DC Current [kA] *)
    rPot_VotedBathTemp_degC         : REAL; (* TMR Voted Molten Cryolite Electrolyte Bath Temperature [deg C] *)
    rPot_VotedBeamPos_mm            : REAL; (* TMR Voted Anode Beam Elevation Position [mm] *)
    rPot_CalculatedResistance_uOhm  : REAL; (* Instantaneous Pot Pseudo-Resistance: R_pot = (V - E_emf) / I [micro-Ohm] *)
    rPot_FilteredResistance_uOhm    : REAL; (* Low-Pass Butterworth Filtered Pot Pseudo-Resistance [micro-Ohm] *)
    rPot_EstAluminaConcentration_pct: REAL; (* State-Space Observer Dissolved Alumina Concentration Estimate [wt%] *)
    rPot_EstSuperheat_degC          : REAL; (* Calculated Molten Electrolyte Superheat (T_bath - T_liquidus) [deg C] *)
    rPot_EstLiquidusTemp_degC       : REAL; (* Estimated Cryolite Bath Liquidus Freezing Temperature [deg C] *)
    rPot_EstCurrentEfficiency_pct   : REAL; (* Estimated Instantaneous Faradaic Cathodic Current Efficiency [%] *)
    rPot_ResistanceSlope_uOhm_min   : REAL; (* Rolling Polynomial 1st Derivative Resistance Slope dR/dt [micro-Ohm/min] *)
    rPot_ResistanceCurvature_uOhm_s2: REAL; (* 2nd Derivative Resistance Acceleration d2R/dt2 [micro-Ohm/s^2] *)
    rPot_BubbleNoiseVariance_uOhm2  : REAL; (* High-Frequency Anode Gas Bubble Resistance Noise Variance [micro-Ohm^2] *)
    rPot_EstAnodeCathodeDist_mm     : REAL; (* First-Principles Estimated Real Anode-Cathode Distance ACD [mm] *)
    rPot_EstGasBubbleCoverage_pct   : REAL; (* Estimated Bottom Anode Surface Gas Polarization Coverage [%] *)
    rPot_EstMetalPadLevel_cm        : REAL; (* Estimated Liquid Aluminum Metal Pad Reservoir Level [cm] *)

    (* ==================== FSM & OPERATIONAL STATUS FLAGS ==================== *)
    nFSM_CurrentState               : INT;  (* Deterministic 14-Stage Production FSM Active State (0..13) [-] *)
    bPot_InAnodeEffect              : BOOL; (* Pot Anode Effect Full Flash Voltage Spike Active Flag [-] *)
    bPot_EarlyAnodeEffectWarning    : BOOL; (* Predictive Early Anode Effect Slope / Curvature Warning Flag [-] *)
    bPot_FeedingModeUnderfeed       : BOOL; (* Feeder Controller in Scheduled Slope Diagnostic Underfeed Mode [-] *)
    bPot_FeedingModeOverfeed        : BOOL; (* Feeder Controller in Rapid Alumina Depletion Overfeed Mode [-] *)
    bPot_FeedingModeNominal         : BOOL; (* Feeder Controller in Balanced Faradaic Tracking Feed Mode [-] *)
    bPot_BeamRockingActive          : BOOL; (* Anode Beam High-Speed Oscillatory Gas Film Rocking Move Active [-] *)
    bPot_EmergencyTripped           : BOOL; (* Potline Cell Latched Emergency Safety Shutdown Trip Active [-] *)

    (* ==================== ISA-18.2 ALARMS & BIT-PACKED TELEMETRY DWORDS ==================== *)
    dwStatusWord1                   : DWORD; (* Primary Subsystem Operational Status Bitfield Telemetry [-] *)
    dwStatusWord2                   : DWORD; (* Secondary Subsystem Automation Modes & Interlock Bitfield [-] *)
    dwAlarmWord1                    : DWORD; (* High-High and High Process Severity Latched Alarm Bitfield [-] *)
    dwAlarmWord2                    : DWORD; (* Low-Low, Low, and Sensor TMR Discrepancy Latched Alarm Bitfield [-] *)
    dwFirstOutWord                  : DWORD; (* Deterministic First-Out Safety Trip Cause Capture Bitfield [-] *)
END_VAR'''
