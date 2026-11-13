# trt_builder/st_header_io.py
"""
Header and VAR_INPUT / VAR_OUTPUT declarations for FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
COMMERCIAL INDUSTRIAL SECTOR: Primary Metallurgy & Blast Furnace Energy Recovery (Tier 1 Priority)
SYSTEM IDENTIFIER           : Integrated Steel Works Blast Furnace Top Gas Energy Recovery Island
EQUIPMENT TAG               : BF-TRT-ISLAND-5500M3
HEARTH WORKING VOLUME       : 5,500 m3 Heavy Blast Furnace Reactor
TURBINE SPECIFICATION       : 25.0 MW Axial Multi-Stage Reaction Expansion Turbine (TRT)
ROTATIONAL SPEED            : 3,000 rpm Synchronous Rotor (50.0 Hz Grid Intertie)
GAS PRESSURE CONTROL BAND   : Nominal 250.0 kPa gauge (2.50 bar) +/- 2.0 kPa Closed-Loop Precision
DYNAMIC SEPTUM VALVE BANK   : 3-Valve Parallel Throttling Array (Coarse V1, Intermediate V2, Fine Trim V3)
EMERGENCY BYPASS SYSTEM     : Fast Electro-Hydraulic Quick-Opening Bypass Valve (< 450 ms Stroke Time)
FAST ISOLATION STOP VALVE   : Spring-Assisted Electro-Hydraulic Emergency Stop Valve (< 150 ms Trip Time)
GAS CLEANING INTERLOCKS     : Dry Bag Filter High-Temp Membrane Array (Low/High dP & Temp Interlocks)
ROTOR SCOURING SYSTEM       : Automated High-Pressure Fluid Wash for Sub-Micron Dust Anti-Accretion
MATHEMATICAL FOUNDATION     : Discrete State-Space Luenberger Observer (Ts = 10 ms, 8 States, 5 Inputs)
ADVANCED CONTROL PARADIGM   : Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent
INSTRUMENTATION ARCHITECTURE: 2oo3 Triple Modular Redundancy (TMR) Voting with Bumpless Sensor Degradation
SAFETY ARCHITECTURE         : ISA-18.2 Multi-Tier Alarm Engine with SIL-3 Hardware Trip Integration
====================================================================================================
*)

VAR_INPUT
    (* Execution & Master Supervisory Controls *)
    bExecute                        : BOOL := FALSE;    (* Master Execution Enable Command [BOOL] *)
    bReset                          : BOOL := FALSE;    (* Master Alarm & Trip Reset Acknowledge [BOOL] *)
    bAutoMode                       : BOOL := FALSE;    (* Auto Closed-Loop Coordination Enable [BOOL] *)
    bEmergencyTripManual            : BOOL := FALSE;    (* Manual Operator Emergency Trip Pushbutton [BOOL] *)
    bStartSequence                  : BOOL := FALSE;    (* Sequence Initiate Command for TRT Start [BOOL] *)
    bStopSequence                   : BOOL := FALSE;    (* Sequence Initiate Command for Controlled Unload [BOOL] *)
    bGridBreakerClosed_Feedback     : BOOL := FALSE;    (* 52G Generator Grid Intertie Breaker Aux Closed Contact [BOOL] *)
    bSynchronizerPermissive         : BOOL := FALSE;    (* Automatic Grid Synchronizer Interlock Permissive [BOOL] *)

    (* Triple Modular Redundant (2oo3) Channel 1: Blast Furnace Top Gas Plenum Pressure [kPa] *)
    rTopGasPressure_PT101A          : REAL := 250.0;    (* BF Top Gas Pressure Transmitter PT-101A [kPa] *)
    rTopGasPressure_PT101B          : REAL := 250.0;    (* BF Top Gas Pressure Transmitter PT-101B [kPa] *)
    rTopGasPressure_PT101C          : REAL := 250.0;    (* BF Top Gas Pressure Transmitter PT-101C [kPa] *)

    (* Triple Modular Redundant (2oo3) Channel 2: TRT Turbine Inlet Nozzle Chest Pressure [kPa] *)
    rTurbineInletPressure_PT201A    : REAL := 245.0;    (* TRT Inlet Pressure Transmitter PT-201A [kPa] *)
    rTurbineInletPressure_PT201B    : REAL := 245.0;    (* TRT Inlet Pressure Transmitter PT-201B [kPa] *)
    rTurbineInletPressure_PT201C    : REAL := 245.0;    (* TRT Inlet Pressure Transmitter PT-201C [kPa] *)

    (* Triple Modular Redundant (2oo3) Channel 3: Blast Furnace Top Gas Total Mass Flow Rate [kg/s] *)
    rTopGasMassFlow_FT301A          : REAL := 210.0;    (* BF Top Gas Venturi Mass Flow Transmitter FT-301A [kg/s] *)
    rTopGasMassFlow_FT301B          : REAL := 210.0;    (* BF Top Gas Venturi Mass Flow Transmitter FT-301B [kg/s] *)
    rTopGasMassFlow_FT301C          : REAL := 210.0;    (* BF Top Gas Venturi Mass Flow Transmitter FT-301C [kg/s] *)

    (* Triple Modular Redundant (2oo3) Channel 4: Generator Active Electrical Power Output [MW] *)
    rGeneratorPower_WT401A          : REAL := 0.0;      (* Generator Active Power High-Speed Transducer WT-401A [MW] *)
    rGeneratorPower_WT401B          : REAL := 0.0;      (* Generator Active Power High-Speed Transducer WT-401B [MW] *)
    rGeneratorPower_WT401C          : REAL := 0.0;      (* Generator Active Power High-Speed Transducer WT-401C [MW] *)

    (* Triple Modular Redundant (2oo3) Channel 5: Turbine Bearing Radial Vibration Displacement [um] *)
    rTurbineVibration_VT501A        : REAL := 12.0;     (* TRT Journal Bearing Radial Proximity Probe VT-501A [um] *)
    rTurbineVibration_VT501B        : REAL := 12.0;     (* TRT Journal Bearing Radial Proximity Probe VT-501B [um] *)
    rTurbineVibration_VT501C        : REAL := 12.0;     (* TRT Journal Bearing Radial Proximity Probe VT-501C [um] *)

    (* Triple Modular Redundant (2oo3) Channel 6: Dry Bag Filter Differential Pressure [kPa] *)
    rBagFilterDiffPress_DPT601A     : REAL := 5.2;      (* Dry Bag Filter Array Differential Pressure DPT-601A [kPa] *)
    rBagFilterDiffPress_DPT601B     : REAL := 5.2;      (* Dry Bag Filter Array Differential Pressure DPT-601B [kPa] *)
    rBagFilterDiffPress_DPT601C     : REAL := 5.2;      (* Dry Bag Filter Array Differential Pressure DPT-601C [kPa] *)

    (* Thermodynamic & Process Temperatures [deg C] *)
    rTopGasInletTemp_TT102          : REAL := 165.0;    (* BF Top Gas Temperature at Bag Filter Inlet [deg C] *)
    rTurbineExhaustTemp_TT202       : REAL := 85.0;     (* TRT Turbine Exhaust Gas Temperature [deg C] *)
    rTurbineBearingTemp_TT502A      : REAL := 58.0;     (* Turbine Drive-End Radial Bearing Metal Temp [deg C] *)
    rTurbineBearingTemp_TT502B      : REAL := 59.0;     (* Turbine Non-Drive-End Radial Bearing Metal Temp [deg C] *)
    rTurbineThrustBearingTemp_TT503 : REAL := 62.0;     (* Turbine Active Thrust Collar Bearing Metal Temp [deg C] *)
    rGeneratorBearingTemp_TT402     : REAL := 55.0;     (* Generator DE/NDE Bearing Metal Temperature [deg C] *)

    (* Auxiliary Systems Pressures & Transducers *)
    rLubeOilSupplyPress_PT801       : REAL := 3.2;      (* Hydrodynamic Bearing Lubrication Oil Pressure [bar] *)
    rJackingOilPress_PT802          : REAL := 125.0;    (* Hydrostatic Rotor Jacking Lift Oil Pressure [bar] *)
    rHydraulicSupplyPress_PT803     : REAL := 185.0;    (* Electro-Hydraulic Fast Actuator Main Pressure [bar] *)
    rFastBypassAccumPress_PT804     : REAL := 175.0;    (* Fast Bypass Nitrogen Accumulator Header Pressure [bar] *)
    rN2SealGasDiffPress_DPT901      : REAL := 22.0;     (* Labyrinth Shaft Nitrogen Seal Differential Pressure [kPa] *)
    rCleanGasHeaderPress_PT302      : REAL := 15.0;     (* Clean Gas Downstream Network Backpressure [kPa] *)
    rGasOxygenConcentration_AT101   : REAL := 0.25;     (* Top Gas Volumetric Oxygen Content [vol %] *)

    (* High-Speed Rotational Speed Pickups [rpm] *)
    rTurbineSpeed_ST101A            : REAL := 0.0;      (* Redundant Magnetic Hall-Effect Rotor Speed Pickup A [rpm] *)
    rTurbineSpeed_ST101B            : REAL := 0.0;      (* Redundant Magnetic Hall-Effect Rotor Speed Pickup B [rpm] *)

    (* Physical Valve Position Feedbacks [%] *)
    rVSV_PositionFeedback           : REAL := 0.0;      (* Variable Stator Vane (VSV) Actual Position [%] *)
    rSeptumV1_PositionFeedback      : REAL := 35.0;     (* Septum Valve 1 (Coarse Throttling) Actual Position [%] *)
    rSeptumV2_PositionFeedback      : REAL := 25.0;     (* Septum Valve 2 (Intermediate) Actual Position [%] *)
    rSeptumV3_PositionFeedback      : REAL := 15.0;     (* Septum Valve 3 (Fine Trim) Actual Position [%] *)
    rFastBypass_PositionFeedback    : REAL := 0.0;      (* Fast Emergency Bypass Valve Actual Position [%] *)
    rInletESV_PositionFeedback      : REAL := 0.0;      (* TRT Inlet Emergency Stop Valve Actual Position [%] *)

    (* Setpoints & Tuning Parameters *)
    rTopGasPressure_Setpoint        : REAL := 250.0;    (* Blast Furnace Top Pressure Target Setpoint [kPa] *)
    rGeneratorPower_Setpoint        : REAL := 22.5;     (* Target Active Electrical Power Recovery Setpoint [MW] *)
    rTurbineSpeed_Nominal           : REAL := 3000.0;   (* Synchronous Rotor Speed Base Reference [rpm] *)
    rMaxAllowedPressureDev          : REAL := 4.0;      (* Maximum Allowed BF Pressure Deviation Window [kPa] *)
    rVSV_MaxSlewRatePctSec          : REAL := 2.5;      (* Maximum Permitted VSV Slew Rate [%/s] *)
    rSeptum3_MaxSlewRatePctSec      : REAL := 25.0;     (* Fast Trim Septum Valve 3 Slew Rate [%/s] *)

    (* Hardware Status & Interlock Contacts *)
    bGoggleValveUpstream_Open       : BOOL := TRUE;     (* Upstream Isolation Goggle Valve Limit Open [BOOL] *)
    bGoggleValveDownstream_Open     : BOOL := TRUE;     (* Downstream Isolation Goggle Valve Limit Open [BOOL] *)
    bBagFilterPulseJet_Running      : BOOL := TRUE;     (* Bag Filter Online Nitrogen Reverse-Pulse Status [BOOL] *)
    bScouringSprayHeader_PressOK    : BOOL := TRUE;     (* Rotor Scouring Water Wash Pressure Permissive [BOOL] *)
    bLubeOilPumpsRunning            : BOOL := TRUE;     (* Auxiliary AC Lube Oil Pumps Healthy & Running [BOOL] *)
    bJackingOilPumpRunning          : BOOL := FALSE;    (* Hydrostatic Rotor Lift Pump Running Status [BOOL] *)
    bGeneratorElectricalProtectionOK: BOOL := TRUE;     (* Generator ANSI 87/51/40/32 Protective Relay Healthy [BOOL] *)
    bTurbineTripSolenoidsHealthy    : BOOL := TRUE;     (* 2oo3 De-Energize-to-Trip Hydraulic Solenoid Line Integrity [BOOL] *)
END_VAR

VAR_OUTPUT
    (* Primary Actuator Continuous Position Demands [%] *)
    rVSV_PositionDemand             : REAL := 0.0;      (* Variable Stator Vane Position Modulation Command [%] *)
    rSeptumV1_PositionDemand        : REAL := 35.0;     (* Septum Valve 1 (Coarse Bypass) Position Command [%] *)
    rSeptumV2_PositionDemand        : REAL := 25.0;     (* Septum Valve 2 (Intermediate) Position Command [%] *)
    rSeptumV3_PositionDemand        : REAL := 15.0;     (* Septum Valve 3 (Fine Pressure Trim) Position Command [%] *)

    (* Discrete SIL-3 Protection & Emergency Actuation Commands *)
    bFastBypassValve_TripOpen       : BOOL := FALSE;    (* Fast Electro-Hydraulic Bypass Valve Snap Open Command [BOOL] *)
    bInletESV_TripClose             : BOOL := FALSE;    (* TRT Inlet Quick-Closing Emergency Stop Valve Snap Shut [BOOL] *)
    bBleederValves_EmergencyCrackOpen:BOOL := FALSE;    (* Blast Furnace Top Bleeder Safety Pressure Relief Open [BOOL] *)
    bGeneratorBreaker_TripOpen      : BOOL := FALSE;    (* 52G Generator Breaker Emergency Trip Command [BOOL] *)
    bGeneratorBreaker_ClosePermissive:BOOL:= FALSE;     (* 52G Generator Synchronizer Breaker Close Interlock Permissive [BOOL] *)

    (* Auxiliary Systems Control Outputs *)
    bJackingOilPump_StartCommand    : BOOL := FALSE;    (* Hydrostatic Rotor Lift Jacking Pump Run Command [BOOL] *)
    bAuxLubeOilPump_StartCommand    : BOOL := FALSE;    (* Auxiliary Lubrication Oil Pump Start Command [BOOL] *)
    bScouringSpraySolenoid_Open     : BOOL := FALSE;    (* Anti-Accretion Rotor Blade Scouring Wash Solenoid [BOOL] *)
    bCasingN2Purge_Solenoid_Open    : BOOL := FALSE;    (* TRT Casing Nitrogen Inert Purge Valve Solenoid [BOOL] *)
    bBagFilterPulseJet_BoostDemand  : BOOL := FALSE;    (* Bag Filter Nitrogen Pulse-Jet Aggressive Clean Trigger [BOOL] *)

    (* Voted Cyber-Physical Process Telemetry *)
    rVoted_TopGasPressure           : REAL := 250.0;    (* 2oo3 Triple Modular Voted Top Gas Plenum Pressure [kPa] *)
    rVoted_TurbineInletPressure     : REAL := 245.0;    (* 2oo3 Triple Modular Voted Turbine Inlet Pressure [kPa] *)
    rVoted_TopGasMassFlow           : REAL := 210.0;    (* 2oo3 Triple Modular Voted Top Gas Mass Flow Rate [kg/s] *)
    rVoted_GeneratorActivePower     : REAL := 0.0;      (* 2oo3 Triple Modular Voted Active Power Output [MW] *)
    rVoted_TurbineVibration         : REAL := 12.0;     (* 2oo3 Triple Modular Voted Shaft Radial Vibration [um] *)
    rVoted_BagFilterDiffPress       : REAL := 5.2;      (* 2oo3 Triple Modular Voted Bag Filter dP [kPa] *)
    rTurbineSpeed_Filtered          : REAL := 0.0;      (* Validated & Rate-Filtered Rotor Speed [rpm] *)
    rTopGasPressure_Deviation       : REAL := 0.0;      (* Control Error: Top Pressure Minus Setpoint [kPa] *)
    rTopGasPressure_ROC             : REAL := 0.0;      (* Real-Time Pressure Rate-of-Change (Furnace Slip) [kPa/s] *)
    rTurbineRecoveredEnergy_MWh     : REAL := 0.0;      (* Cumulative Megawatt-Hours Thermal Energy Recovered [MWh] *)
    rCalculatedAerodynamicPower     : REAL := 0.0;      (* Aerodynamic Isentropic Expansion Power Yield [MW] *)
    rExpansionPolytropicEfficiency  : REAL := 0.86;     (* Dynamic Thermodynamic Polytropic Efficiency [ratio] *)

    (* Supervisory Diagnostics, Telemetry & Alarm Bit-Vectors *)
    nActiveFSMState                 : INT := 0;         (* Active Operational Finite State Machine Stage (0-13) [INT] *)
    bSystemReadyToStart             : BOOL := FALSE;    (* System Preconditions & Interlocks Fully Satisfied [BOOL] *)
    bClosedLoopPressureLocked       : BOOL := FALSE;    (* Blast Furnace Top Pressure Stabilized in Target Band [BOOL] *)
    bTRT_PowerRecoveryActive        : BOOL := FALSE;    (* TRT Synchronized & Generating Electrical Base Load [BOOL] *)
    bEmergencyMasterTripActive      : BOOL := FALSE;    (* Master SIL-3 Trip Latch Currently Engaged [BOOL] *)

    udwStatusWord                   : DWORD := 16#00000000; (* 32-Bit Bit-Packed Supervisory Operating Status Word [DWORD] *)
    udwAlarmWord1                   : DWORD := 16#00000000; (* 32-Bit Bit-Packed Critical Process Alarms & Trips [DWORD] *)
    udwAlarmWord2                   : DWORD := 16#00000000; (* 32-Bit Bit-Packed Secondary Warnings & Equipment Alarms [DWORD] *)
    udwTMRDiagWord                  : DWORD := 16#00000000; (* 32-Bit Bit-Packed 2oo3 Sensor Channel Health Diagnostics [DWORD] *)
    udwFirstOutTripWord             : DWORD := 16#00000000; (* 32-Bit Bit-Packed First-Out Emergency Trip Cause Register [DWORD] *)
END_VAR
"""
