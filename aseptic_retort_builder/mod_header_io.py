# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/mod_header_io.py
Declares Header, VAR_INPUT, and VAR_OUTPUT for FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization.
"""

def generate_header_io():
    return '''FUNCTION_BLOCK FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Commercial Food & Beverage Processing (Tier 1 Priority Sector)
 * SUBSYSTEM                    : Continuous Overpressure Industrial Rotary Retort Autoclave Sterilizer
 * FUNCTION BLOCK               : FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization
 * DESIGN STANDARDS             : IEC 61131-3 3rd Ed., US FDA 21 CFR Part 113 (LACF), NFPA 86, ISA-18.2, ASME Section VIII Div 1
 * CYBER-PHYSICAL RIGOR         : 6x6 Discrete State-Space Model (A, B, C, D), Receding-Horizon Decoupled MPC with
 *                                10-Iteration Unrolled Projected Gradient Descent (PGD), 4-Channel 2oo3 TMR Voting Logic,
 *                                Bigelow/Arrhenius Microbial Thermal Death Time Inactivation (F0 >= 6.0 min),
 *                                Dynamic Steam-Air Overpressure Differential Stress Regulation (|Delta_P| < 0.12 bar),
 *                                Multi-Zone Cooling Water Cascade, Continuous Rotary Drum Agitation Speed Regulation,
 *                                Deterministic 14-Stage Production FSM (States 0..13), and 32-Bit Bit-Packed Status Words.
 * RATED CAPACITY               : 1,200 cans/min or pouches, 4.0 bar Design Pressure, 140 deg C Design Temperature
 * ===================================================================================================================== *)

VAR_INPUT
    (* ==================== 2oo3 TRIPLE MODULAR REDUNDANT SENSORS (TMR) ==================== *)
    rTemp_Sensor1_degC              : REAL; (* Retort Chamber Dual-Element Class A Pt100 RTD Channel 1 [deg C] *)
    rTemp_Sensor2_degC              : REAL; (* Retort Chamber Dual-Element Class A Pt100 RTD Channel 2 [deg C] *)
    rTemp_Sensor3_degC              : REAL; (* Retort Chamber Dual-Element Class A Pt100 RTD Channel 3 [deg C] *)

    rPress_Sensor1_bar              : REAL; (* Retort Shell Piezoresistive Pressure Transmitter Channel 1 [bar] *)
    rPress_Sensor2_bar              : REAL; (* Retort Shell Piezoresistive Pressure Transmitter Channel 2 [bar] *)
    rPress_Sensor3_bar              : REAL; (* Retort Shell Piezoresistive Pressure Transmitter Channel 3 [bar] *)

    rLevel_Sensor1_mm               : REAL; (* Vessel Condensate / Sump Level Differential Pressure Channel 1 [mm] *)
    rLevel_Sensor2_mm               : REAL; (* Vessel Condensate / Sump Level Differential Pressure Channel 2 [mm] *)
    rLevel_Sensor3_mm               : REAL; (* Vessel Condensate / Sump Level Differential Pressure Channel 3 [mm] *)

    rPouch_Press1_bar               : REAL; (* Container Internal Pressure Wireless Telemetry Transponder 1 [bar] *)
    rPouch_Press2_bar               : REAL; (* Container Internal Pressure Wireless Telemetry Transponder 2 [bar] *)
    rPouch_Press3_bar               : REAL; (* Container Internal Pressure Wireless Telemetry Transponder 3 [bar] *)

    (* ==================== AUXILIARY PROCESS SENSORS & TRANSDUCERS ==================== *)
    rSteamHeaderPress_bar           : REAL; (* Plant Culinary Saturated Steam Supply Header Pressure [bar] *)
    rAirHeaderPress_bar             : REAL; (* Plant High-Pressure Compressed Air Supply Header Pressure [bar] *)
    rCoolingWaterSupplyPress_bar    : REAL; (* Plant Sterile Cascade Cooling Water Supply Pressure [bar] *)
    rCoolingWaterSupplyTemp_degC    : REAL; (* Plant Cooling Water Supply Inflow Temperature [deg C] *)
    rCoolingWaterDrainTemp_degC     : REAL; (* Recirculation Cooling Water Outflow Drain Temperature [deg C] *)
    rCoolingWaterFlow_m3h           : REAL; (* Cascade Cooling Water Recirculation Flow Rate [m3/h] *)
    rSteamMassFlow_kgh              : REAL; (* Retort Saturated Steam Mass Injection Flow Rate [kg/h] *)
    rRotaryDrumSpeed_RPM            : REAL; (* Rotary Agitation Drum Rotor Speed Encoder Feedback [RPM] *)
    rCanFeedRate_cpm                : REAL; (* Continuous Infeed Pouch / Can Throughput Rate [cans/min] *)
    rDoorSealPress_bar              : REAL; (* Chamber Inflatable Pneumatic Elastomer Gasket Pressure [bar] *)

    (* ==================== DIGITAL INTERLOCKS & HARDWIRED DISCRETES ==================== *)
    bDI_SafetyDoorClosed_ZS1        : BOOL; (* Retort Safety Shell Infeed/Access Door Closed Limit Switch [-] *)
    bDI_SafetyDoorLocked_ZS2        : BOOL; (* Retort Hydraulic Locking Ring / Safety Pin Engaged Limit Switch [-] *)
    bDI_GasketSealPressOK_PS1       : BOOL; (* Door Inflatable Gasket Pressure Switch Interlock (>= 5.0 bar) [-] *)
    bDI_EmergencyStop_PB            : BOOL; (* Control Console Main Hardwired Emergency Stop Pushbutton [-] *)
    bDI_SafetyReliefPoppetOpen_ZS   : BOOL; (* ASME Section VIII Overpressure Safety Relief Valve Lift Switch [-] *)
    bDI_CondensateDrainClosed_ZS    : BOOL; (* Sump Rapid Drain Isolation Valve Closed Proximity Switch [-] *)

    (* ==================== OPERATOR COMMANDS & RECIPE SETPOINTS ==================== *)
    bCmd_StartContinuousCycle       : BOOL; (* Operator Command: Initiate Automated Retort Sterilization Cycle [-] *)
    bCmd_StopCycle                  : BOOL; (* Operator Command: Initiate Controlled Cooldown and Safe Discharge [-] *)
    bCmd_EmergencyTripReset         : BOOL; (* Operator Command: Reset Latched Alarms and Safety Lockouts [-] *)
    bCmd_AcknowledgeAlarm           : BOOL; (* Operator Command: Acknowledge Active ISA-18.2 Process Alarms [-] *)
    bCmd_ManualOverride             : BOOL; (* Operator Command: Enable Manual Actuator Maintenance Positioning [-] *)

    rSet_SterilizationTemp_degC     : REAL; (* Recipe Scheduled Cook Temperature Setpoint [deg C] *)
    rSet_RetortOverpressure_bar     : REAL; (* Recipe Total Steam-Air Target Chamber Pressure Setpoint [bar] *)
    rSet_TargetF0_min               : REAL; (* Minimum Required Microbial Inactivation Lethality Target [min] *)
    rSet_MaxCanDeltaP_bar           : REAL; (* Maximum Allowable Container Differential Stress Limit [bar] *)
    rSet_ComeUpRampRate_degCpm      : REAL; (* Thermal Come-Up Heating Ramp Rate Setpoint [deg C/min] *)
    rSet_TargetCoolingTemp_degC     : REAL; (* Final Container Discharge Chilldown Temperature Setpoint [deg C] *)
    rSet_NominalDrumSpeed_RPM       : REAL; (* Nominal Continuous Rotary Drum Agitation Speed [RPM] *)
    rSet_TargetThroughput_cpm       : REAL; (* Production Nominal Container Throughput Target [cans/min] *)
END_VAR

VAR_OUTPUT
    (* ==================== MODULATING ACTUATOR COMMANDS ==================== *)
    rCmd_SteamModValve_pct          : REAL; (* Modulating Saturated Steam Inflow Control Valve Command [%] *)
    rCmd_AirOverpressValve_pct      : REAL; (* Modulating Compressed Air Overpressure Injection Valve [%] *)
    rCmd_ExhaustVentValve_pct       : REAL; (* Modulating Chamber Top Exhaust Steam-Air Vent Valve [%] *)
    rCmd_CoolingWaterCascadeValve_pct:REAL; (* Modulating Multi-Zone Cascade Cooling Water Valve Command [%] *)
    rCmd_RotaryDrumSpeed_RPM        : REAL; (* Rotary Drum Agitation VFD Speed Setpoint Output [RPM] *)
    rCmd_DischargeConveyorSpeed_pct : REAL; (* Sterile Container Discharge Outfeed Conveyor Speed [%] *)

    (* ==================== DISCRETE ACTUATOR COMMANDS ==================== *)
    bCmd_DrainValveOpen             : BOOL; (* Bottom Vessel Rapid Condensate & Quench Drain Valve Command [-] *)
    bCmd_DoorSealInflate            : BOOL; (* Vessel Door Inflatable Pneumatic Gasket Solenoid Command [-] *)
    bCmd_SafetyReliefPilotOpen      : BOOL; (* Controlled Emergency Chamber Depressurization Solenoid [-] *)

    (* ==================== CYBER-PHYSICAL PROCESS ESTIMATES ==================== *)
    rEst_ChamberTemp_degC           : REAL; (* Voted & State-Space Estimated Retort Chamber Temperature [deg C] *)
    rEst_CanCoreTemp_degC           : REAL; (* Thermal Resistance Estimated Container Core Cold-Spot Temp [deg C] *)
    rEst_ChamberPress_bar           : REAL; (* Voted & State-Space Estimated Retort Total Shell Pressure [bar] *)
    rEst_PouchInternalPress_bar     : REAL; (* Telemetry & Dalton Estimated Container Internal Vapor Pressure [bar] *)
    rEst_ContainerDeltaP_bar        : REAL; (* Net Container Wall Stress Differential (P_internal - P_retort) [bar] *)
    rCalc_AccumulatedF0_min         : REAL; (* Real-Time Bigelow Arrhenius Microbial Lethality F0 Integral [min] *)
    rCalc_AccumulatedC0_min         : REAL; (* Real-Time Cook Quality Degradation C0 Retention Index [min] *)
    rCalc_TransitDwellTime_min      : REAL; (* Container Transit Dwell Exposure Time Inside Rotary Helix [min] *)
    rCalc_ContainerThroughput_cpm   : REAL; (* Calibrated Real-Time Finished Packaging Throughput Rate [cans/min] *)

    (* ==================== AUTOMATION STATE & DIAGNOSTIC TELEMETRY ==================== *)
    iCurrentState                   : INT;  (* Active Deterministic Operational FSM State Index (0..13) [-] *)
    dwStatusWord                    : DWORD;(* 32-Bit Bit-Packed Subsystem Operational Status Telemetry Word [-] *)
    dwWarningWord                   : DWORD;(* 32-Bit Bit-Packed ISA-18.2 Process Advisory Warning Word [-] *)
    dwFaultWord                     : DWORD;(* 32-Bit Bit-Packed Critical Safety Interlock Trip & Fault Word [-] *)
    dwQualitySterilityWord          : DWORD;(* 32-Bit Bit-Packed US FDA 21 CFR Part 113 Regulatory Compliance Word [-] *)
    bCycleComplete_Sterile          : BOOL; (* Batch / Continuous Retort Sterility Target Fully Attained [-] *)
    bEmergencyAbortActive           : BOOL; (* Emergency Trip Active / System in Safe Cooldown Containment [-] *)
END_VAR'''
