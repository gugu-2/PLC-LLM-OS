# steel_dri_builder/part1_header_io.py
"""
Part 1: Header documentation and VAR_INPUT / VAR_OUTPUT declarations
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Steel_DRI_ShaftFurnace_HydrogenSyngas_Reduction
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT HIGH-ORDER ENGINE
DOMAIN: PRIMARY METALLURGY & SUSTAINABLE STEELMAKING
PROCESS: DIRECT REDUCED IRON (DRI) MOVING-BED SHAFT REDUCTION FURNACE
TECHNOLOGY: GREEN HYDROGEN (H2) & REFORMED SYNGAS METALLIZATION WITH CARBURIZATION & BURDEN DESCENT
CYBER-PHYSICAL SPECIFICATION:
  - 8-STATE DISCRETE CYBER-PHYSICAL KINETIC STATE-SPACE MODEL (Ts = 25 ms)
  - RECEDING-HORIZON MODEL PREDICTIVE CONTROLLER (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
    * HORIZON N = 5, 6 UNROLLED ITERATIONS, DYNAMIC H2 / SYNGAS / CH4 DECOUPLING
  - 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING ACROSS 5 CRITICAL SENSOR ARRAYS (250 ms TIMERS)
  - DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) WITH BURDEN STICKING / SNORT DUMP LOGIC
  - SIL-3 SAFETY INSTRUMENTED DOUBLE-BLOCK-AND-BLEED TRIP & ISA-18.2 MULTI-TIER ALARM MATRIX
====================================================================================================
*)
VAR_INPUT
    (* Furnace Master Supervisory Controls *)
    bEnable                             : BOOL := FALSE;       (* Master Functional Block Enable Permissive [binary] *)
    bReset                              : BOOL := FALSE;       (* Master Alarm and Interlock Reset Command [binary] *)
    bEmergencyStop                      : BOOL := FALSE;       (* Safety Hardwired E-Stop Pushbutton Trip [binary] *)
    bAutoMode                           : BOOL := FALSE;       (* Auto / Supervisory Closed-Loop Coordination [binary] *)
    bAcknowledgeAlarms                  : BOOL := FALSE;       (* ISA-18.2 Operator Alarm Acknowledge Request [binary] *)
    bStartWarmup                        : BOOL := FALSE;       (* Command to Initiate Process Gas Heater Warmup [binary] *)
    bStartHydrogenRamp                  : BOOL := FALSE;       (* Command to Transition from Syngas to Green H2 [binary] *)
    bStartDischarge                     : BOOL := FALSE;       (* Command to Engage Rotary Feeder Discharge [binary] *)
    bInitiateHold                       : BOOL := FALSE;       (* Command to Put Furnace into Hot Turndown Hold [binary] *)
    bManualSnortDump                    : BOOL := FALSE;       (* Operator Manual Shaft Snort Valve Quick Depressurize [binary] *)
    bManualClusterBreakerPulse          : BOOL := FALSE;       (* Operator Manual Pneumatic Pulsing of Cluster Breakers [binary] *)

    (* 2oo3 TMR Channel 1: Bustle Pipe Reduction Gas Thermocouple Array *)
    rTT_Bustle_101A                     : REAL := 950.0;       (* Bustle Pipe Gas Temperature Ring Sensor A [deg C] *)
    rTT_Bustle_101B                     : REAL := 950.0;       (* Bustle Pipe Gas Temperature Ring Sensor B [deg C] *)
    rTT_Bustle_101C                     : REAL := 950.0;       (* Bustle Pipe Gas Temperature Ring Sensor C [deg C] *)
    bTT_Bustle_101A_Valid               : BOOL := TRUE;        (* Bustle Temp Sensor A 4-20mA Loop Health Status [binary] *)
    bTT_Bustle_101B_Valid               : BOOL := TRUE;        (* Bustle Temp Sensor B 4-20mA Loop Health Status [binary] *)
    bTT_Bustle_101C_Valid               : BOOL := TRUE;        (* Bustle Temp Sensor C 4-20mA Loop Health Status [binary] *)

    (* 2oo3 TMR Channel 2: Shaft Reduction Zone Differential Pressure Transmitters *)
    rPDT_Shaft_201A                     : REAL := 52.0;        (* Shaft Upper-to-Lower Differential Pressure A [kPa] *)
    rPDT_Shaft_201B                     : REAL := 52.0;        (* Shaft Upper-to-Lower Differential Pressure B [kPa] *)
    rPDT_Shaft_201C                     : REAL := 52.0;        (* Shaft Upper-to-Lower Differential Pressure C [kPa] *)
    bPDT_Shaft_201A_Valid               : BOOL := TRUE;        (* Shaft DP Sensor A Hart Health Status [binary] *)
    bPDT_Shaft_201B_Valid               : BOOL := TRUE;        (* Shaft DP Sensor B Hart Health Status [binary] *)
    bPDT_Shaft_201C_Valid               : BOOL := TRUE;        (* Shaft DP Sensor C Hart Health Status [binary] *)

    (* 2oo3 TMR Channel 3: In-Line Top Gas Spectrometric Gas Analyzers (H2/CO Molar Ratio) *)
    rAT_Gas_301A_H2CO                   : REAL := 2.85;        (* Top Gas Offtake Spectrometer A H2/CO Ratio [ratio] *)
    rAT_Gas_301B_H2CO                   : REAL := 2.85;        (* Top Gas Offtake Spectrometer B H2/CO Ratio [ratio] *)
    rAT_Gas_301C_H2CO                   : REAL := 2.85;        (* Top Gas Offtake Spectrometer C H2/CO Ratio [ratio] *)
    bAT_Gas_301A_Valid                  : BOOL := TRUE;        (* Spectrometer A Optics & Purge Health Flag [binary] *)
    bAT_Gas_301B_Valid                  : BOOL := TRUE;        (* Spectrometer B Optics & Purge Health Flag [binary] *)
    bAT_Gas_301C_Valid                  : BOOL := TRUE;        (* Spectrometer C Optics & Purge Health Flag [binary] *)

    (* 2oo3 TMR Channel 4: Continuous Top Gas CO2 Infrared Absorption Cells *)
    rAT_Gas_302A_CO2                    : REAL := 15.2;        (* Top Gas NDIR Sensor A Carbon Dioxide Fraction [% vol] *)
    rAT_Gas_302B_CO2                    : REAL := 15.2;        (* Top Gas NDIR Sensor B Carbon Dioxide Fraction [% vol] *)
    rAT_Gas_302C_CO2                    : REAL := 15.2;        (* Top Gas NDIR Sensor C Carbon Dioxide Fraction [% vol] *)
    bAT_Gas_302A_Valid                  : BOOL := TRUE;        (* NDIR Sensor A Diagnostic Flag [binary] *)
    bAT_Gas_302B_Valid                  : BOOL := TRUE;        (* NDIR Sensor B Diagnostic Flag [binary] *)
    bAT_Gas_302C_Valid                  : BOOL := TRUE;        (* NDIR Sensor C Diagnostic Flag [binary] *)

    (* 2oo3 TMR Channel 5: Shaft Top Iron Ore Burden Level Radar Profilers *)
    rLT_Burden_401A                     : REAL := 18.5;        (* Burden Level Radar Transmitter Array A [m] *)
    rLT_Burden_401B                     : REAL := 18.5;        (* Burden Level Radar Transmitter Array B [m] *)
    rLT_Burden_401C                     : REAL := 18.5;        (* Burden Level Radar Transmitter Array C [m] *)
    bLT_Burden_401A_Valid               : BOOL := TRUE;        (* Radar Transmitter A Echo S/N Ratio OK [binary] *)
    bLT_Burden_401B_Valid               : BOOL := TRUE;        (* Radar Transmitter B Echo S/N Ratio OK [binary] *)
    bLT_Burden_401C_Valid               : BOOL := TRUE;        (* Radar Transmitter C Echo S/N Ratio OK [binary] *)

    (* 2oo3 TMR Channel 6: Discharged Hot DRI Dual-Wavelength Optical Pyrometers *)
    rTT_DRI_501A                        : REAL := 680.0;       (* Lower Discharge Cone DRI Pyrometer A [deg C] *)
    rTT_DRI_501B                        : REAL := 680.0;       (* Lower Discharge Cone DRI Pyrometer B [deg C] *)
    rTT_DRI_501C                        : REAL := 680.0;       (* Lower Discharge Cone DRI Pyrometer C [deg C] *)
    bTT_DRI_501A_Valid                  : BOOL := TRUE;        (* Pyrometer A Lens Purge / Signal Quality [binary] *)
    bTT_DRI_501B_Valid                  : BOOL := TRUE;        (* Pyrometer B Lens Purge / Signal Quality [binary] *)
    bTT_DRI_501C_Valid                  : BOOL := TRUE;        (* Pyrometer C Lens Purge / Signal Quality [binary] *)

    (* SIL-3 Safety Instrumented System (SIS) Ingress Oxygen Detectors *)
    rAT_O2_Inlet_601A                   : REAL := 0.02;        (* H2 Supply Gas Trace Oxygen Fast Zirconia Cell A [% vol] *)
    rAT_O2_Inlet_601B                   : REAL := 0.02;        (* H2 Supply Gas Trace Oxygen Fast Zirconia Cell B [% vol] *)
    rAT_O2_TopGas_602A                  : REAL := 0.04;        (* Recycled Process Gas Trace Oxygen Cell A [% vol] *)
    rAT_O2_TopGas_602B                  : REAL := 0.04;        (* Recycled Process Gas Trace Oxygen Cell B [% vol] *)

    (* Auxiliary Process & Laboratory Measurements *)
    rPT_CoolingGas_701                  : REAL := 180.0;       (* Cooling Zone Gas Loop Recirculation Header Pressure [kPa] *)
    rTT_CoolingGas_702                  : REAL := 65.0;        (* Cooling Zone Bottom Gas Discharge Temperature [deg C] *)
    rFT_PelletFeed_801                  : REAL := 155.0;       (* Iron Ore Pellet Feed Gravimetric Belt Weigher [t/h] *)
    rAT_Carbon_901                      : REAL := 2.15;        (* Discharged DRI Online Laser Induced Carburization [wt% C] *)
    rFT_CoolingBlower_Flow              : REAL := 42000.0;     (* Lower Cone Cooling Gas Recirculation Flow [Nm3/h] *)
    rFT_TopGas_TotalFlow                : REAL := 135000.0;    (* Furnace Shaft Total Top Gas Exhaust Rate [Nm3/h] *)

    (* Actuator Position Feedback Loops *)
    rZ_GreenH2_Valve_FB                 : REAL := 0.0;         (* Green Hydrogen Primary Modulating Valve Feedback [%] *)
    rZ_Syngas_Valve_FB                  : REAL := 0.0;         (* Reformed Syngas Main Modulation Valve Feedback [%] *)
    rZ_Heater_Fuel_FB                   : REAL := 0.0;         (* Process Gas Preheater Fuel Gas Modulating Valve FB [%] *)
    rZ_NatGas_Trim_FB                   : REAL := 0.0;         (* Natural Gas Carburization Injection Trim Valve FB [%] *)
    rS_CoolingBlower_VFD_FB             : REAL := 0.0;         (* Cooling Gas Recycle Blower VFD Tachometer Speed FB [%] *)
    rS_Feeder_Speed_FB                  : REAL := 0.0;         (* Bottom Rotary Eccentric Discharge Feeder Speed FB [%] *)

    (* Supervisory Setpoint References *)
    rSP_BustleTemp                      : REAL := 950.0;       (* Bustle Pipe Reduction Gas Inlet Temperature Target [deg C] *)
    rSP_Metallization                   : REAL := 95.0;        (* Target Degree of Iron Ore Reduction / Metallization [% Fe] *)
    rSP_TopGasH2CO                      : REAL := 2.85;        (* Optimal Shaft Top Offtake H2/CO Ratio Setpoint [ratio] *)
    rSP_ProductCarbon                   : REAL := 2.20;        (* Target Bound Carbon / Cementite in Finished DRI [wt% C] *)
    rSP_BurdenLevel                     : REAL := 18.5;        (* Dynamic Burden Bed Surface Height Setpoint [m] *)
    rSP_DischargeRate                   : REAL := 150.0;       (* Target Hot DRI Mass Production Discharge Rate [t/h] *)
    rSP_MaxShaftDP                      : REAL := 72.0;        (* Maximum Permissible Shaft Differential Pressure [kPa] *)

    (* Execution Timing and Voting Bounds *)
    tSampleTime                         : TIME := T#25ms;      (* Discrete Execution Cycle Sample Period [ms] *)
    tTmrDiscrepancyLimit                : TIME := T#250ms;     (* 2oo3 Discrepancy Failure Accumulation Threshold [ms] *)
    rTMR_Tol_BustleTemp                 : REAL := 25.0;        (* Bustle Pipe Thermocouple Discrepancy Tolerance [deg C] *)
    rTMR_Tol_ShaftDP                    : REAL := 6.5;         (* Shaft Differential Pressure Discrepancy Tolerance [kPa] *)
    rTMR_Tol_GasH2CO                    : REAL := 0.35;        (* Top Gas H2/CO Ratio Discrepancy Tolerance [ratio] *)
    rTMR_Tol_GasCO2                     : REAL := 1.8;         (* Top Gas CO2 Discrepancy Tolerance [% vol] *)
    rTMR_Tol_BurdenLevel                : REAL := 0.8;         (* Burden Surface Radar Discrepancy Tolerance [m] *)
    rTMR_Tol_DRITemp                    : REAL := 40.0;        (* Optical Pyrometer Discrepancy Tolerance [deg C] *)
END_VAR
VAR_OUTPUT
    (* Primary Actuator Continuous Command Outputs [0..100%] *)
    rCV_GreenH2_Valve_Cmd               : REAL := 0.0;         (* Green Hydrogen Flow Control Modulating Valve Command [%] *)
    rCV_Syngas_Valve_Cmd                : REAL := 0.0;         (* Reformed Syngas Flow Control Valve Command [%] *)
    rCV_Heater_Fuel_Cmd                 : REAL := 0.0;         (* Process Gas Preheater Fuel Firing Modulation [%] *)
    rCV_NatGas_Trim_Cmd                 : REAL := 0.0;         (* Natural Gas Lower-Cone Carburization Trim Valve [%] *)
    rCV_CoolingBlower_VFD_Cmd           : REAL := 0.0;         (* Cooling Gas Recycle Blower Inverter Speed Output [%] *)
    rCV_Feeder_Speed_Cmd                : REAL := 0.0;         (* Bottom Rotary Discharge Feeder Variable Speed Output [%] *)

    (* Fast-Acting Discrete Safety & Interlock Actuators *)
    bESD_GasTrip_SlamShut               : BOOL := FALSE;       (* SIL-3 Double Block & Bleed Gas Emergency Slam-Shut [binary] *)
    bESD_Vent_Bleed_Open                : BOOL := FALSE;       (* SIL-3 Fast Emergency Vent Bleed Solenoid Open [binary] *)
    bRoof_Snort_Dump_Open               : BOOL := FALSE;       (* Roof Top-Gas Snort Quick Depressurization Valve [binary] *)
    bNitrogen_Purge_Valve_Cmd           : BOOL := TRUE;        (* Emergency / Standby High-Pressure N2 Purge Valve [binary] *)
    bCluster_Breaker_Vibrator_Cmd       : BOOL := FALSE;       (* Pneumatic Sticking-Cluster Breaker Pulse Blast [binary] *)
    bPellet_Feed_Permissive             : BOOL := FALSE;       (* Permissive to Charge Feeder Conveyor System [binary] *)
    bDischarge_Feeder_Permissive        : BOOL := FALSE;       (* Permissive to Bottom DRI Discharge Mechanism [binary] *)
    bHeater_Ignition_Permissive         : BOOL := FALSE;       (* Burner Management Permissive to Gas Heater [binary] *)

    (* Voted Cyber-Physical Process Telemetry *)
    rPV_BustleTemp_Voted                : REAL := 950.0;       (* 2oo3 Robustly Voted Bustle Gas Temperature [deg C] *)
    rPV_ShaftDP_Voted                   : REAL := 52.0;        (* 2oo3 Robustly Voted Shaft Differential Pressure [kPa] *)
    rPV_TopGasH2CO_Voted                : REAL := 2.85;        (* 2oo3 Robustly Voted Top Gas H2/CO Ratio [ratio] *)
    rPV_TopGasCO2_Voted                 : REAL := 15.2;        (* 2oo3 Robustly Voted Top Gas CO2 Fraction [% vol] *)
    rPV_BurdenLevel_Voted               : REAL := 18.5;        (* 2oo3 Robustly Voted Burden Bed Height [m] *)
    rPV_DRITemp_Voted                   : REAL := 680.0;       (* 2oo3 Robustly Voted DRI Pyrometer Temperature [deg C] *)

    (* State-Space Cyber-Physical Estimator Outputs *)
    rPV_Estimated_Metallization         : REAL := 95.0;        (* First-Principles Luenberger Estimated Reduction [% Fe] *)
    rPV_Estimated_Carbon                : REAL := 2.15;        (* Dynamic Model Carburized Product Carbon Fraction [wt% C] *)
    rPV_Estimated_DescendVelocity       : REAL := 2.85;        (* Calibrated Burden Solid Descent Velocity [m/h] *)
    rPV_Estimated_ReductionReactionRate : REAL := 0.185;       (* Kinetic Wüstite-to-Fe Conversion Velocity [mol/(m3*s)] *)
    rPV_Estimated_InternalThermalBed    : REAL := 895.0;       (* Core Shaft Reduction Bed Core Temperature [deg C] *)
    rPV_MPC_CostFunctionJ               : REAL := 0.0;         (* Receding Horizon MPC Normalized Objective Cost [dimless] *)

    (* Process Supervisory Status Flags *)
    eFurnaceState                       : INT := 0;            (* Current Active 14-Stage FSM State Index [enum 0..13] *)
    bFurnaceReady                       : BOOL := FALSE;       (* Furnace Preheated and Ready for Full Pellet Reduction [binary] *)
    bMPC_OptimalActive                  : BOOL := FALSE;       (* Receding Horizon Controller Active in Optimal Domain [binary] *)
    bClusterStickingWarning             : BOOL := FALSE;       (* Burden Clustering & Sticking Hanging Warning [binary] *)
    bOxygenIngressTrip                  : BOOL := FALSE;       (* High-Speed Oxygen Ingress Deflagration Trip [binary] *)
    bTMR_DegradedAlarm                  : BOOL := FALSE;       (* At Least One 2oo3 Channel in 1oo2 Degraded Mode [binary] *)
    bTMR_CriticalFailureAlarm           : BOOL := FALSE;       (* 2oo3 Channel Total Sensor Loss (All Sensors Faulty) [binary] *)

    (* 32-Bit Bit-Packed Supervisory Telemetry & Diagnostics *)
    dwStatusWord1                       : DWORD := 16#00000000;(* Bit-Packed Primary System State Telemetry [dword] *)
    dwStatusWord2                       : DWORD := 16#00000000;(* Bit-Packed Actuator Saturation & FSM Modes [dword] *)
    dwAlarmWord1                        : DWORD := 16#00000000;(* ISA-18.2 Process High and High-High Alarms [dword] *)
    dwAlarmWord2                        : DWORD := 16#00000000;(* ISA-18.2 Low, Low-Low & Sensor Fault Alarms [dword] *)
    dwFirstOutWord                      : DWORD := 16#00000000 (* Latched SIL-3 / First-Out Trip Cause Indicator [dword] *)
END_VAR
"""
