# Comprehensive Generator for FB_Asphalt_BatchPlant_AggregateDrying_BitumenInjection
import json
import uuid
import re

def generate_iec_st():
    parts = []

    # =========================================================================
    # 1. HEADER & SYSTEM ARCHITECTURE
    # =========================================================================
    parts.append("""FUNCTION_BLOCK FB_Asphalt_BatchPlant_AggregateDrying_BitumenInjection
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION RESEARCH - IEC 61131-3 3RD EDITION COMPLIANT
 * ARCHITECTURE: CONTINUOUS ASPHALT BATCH MIXING PLANT (320 TONNES / HOUR)
 * SYSTEM SPECIFICATION:
 *   - 6-Bin Cold Aggregate Feeders with Variable Frequency Speed Dosing Belts & Master Weighing Conveyor
 *   - Counterflow Rotary Aggregate Drying Drum (3.0 m dia x 12.0 m length, 160 deg C - 190 deg C discharge)
 *   - Modulating Dual-Fuel Burner (Heavy Fuel Oil / Natural Gas) with Combustion Air & Flue Gas Oxygen Trim
 *   - High-Efficiency Reverse Pulse-Jet Baghouse Dust Collector with LEL Flue Hydrocarbon Watchdog
 *   - Heavy-Duty Hot Aggregate Bucket Elevator (350 t/h capacity) & 6-Deck Inclined Vibrating Screen
 *   - 6-Compartment Thermally Insulated Hot Aggregate Storage Bins with Microwave Continuous Level Sensors
 *   - High-Precision Gravimetric Pugmill Batch Weigh Hoppers (Aggregates, Reclaimed Filler, Mineral Dust)
 *   - Bitumen Thermal Oil Jacketed Storage & High-Pressure Viscosity-Compensated Metered Spray Bar Injection
 *   - Twin-Shaft Forced-Action Pugmill Mixer (4,000 kg batch capacity) with Dynamic Torque Surge Observer
 *   - S-Curve Velocity Profile Controlled Skip Hoist Carriage & Heated Storage Silo Distribution Flaps
 *
 * CYBER-PHYSICAL FOUNDATIONS:
 *   1. Full 8-State Discrete State-Space Propagation: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
 *      - x1: Rotary drum shell temperature deviation [deg C]
 *      - x2: Flue gas exit duct temperature deviation [deg C]
 *      - x3: Aggregate moisture evaporation mass rate [kg/s]
 *      - x4: Hot aggregate bucket elevator motor load [%]
 *      - x5: Baghouse filter fabric differential pressure drop [mbar]
 *      - x6: Bitumen thermal oil heating jacket temperature [deg C]
 *      - x7: Twin-shaft pugmill dynamic mixing torque [Nm]
 *      - x8: Skip hoist vertical carriage travel velocity [m/s]
 *   2. Receding-Horizon Model Predictive Control (MPC) Quadratic Optimization:
 *      - Minimizes cost functional J = sum(e^T * Q * e) + sum(u^T * R * u) + sum(du^T * S * du) + e_N^T * P * e_N
 *      - Solved via 3-iteration Projected Gradient Descent (PGD) with physical actuator saturation bounds
 *   3. 2oo3 Triple Modular Redundancy (TMR) Voting Engine with Discrepancy Timers & Dynamic Health Grading:
 *      - TMR 1: Rotary Dryer Aggregate Exit Pyrometers (TT-101A, TT-101B, TT-101C) [deg C]
 *      - TMR 2: Gravimetric Pugmill Batch Weigh Hopper Load Cells (WT-201A, WT-201B, WT-201C) [kg]
 *      - TMR 3: Bitumen Injection Pressurized Coriolis Mass Flow Meters (FT-301A, FT-301B, FT-301C) [kg/s]
 *   4. Multi-Physics Cyber-Physical Observers:
 *      - Thermodynamic Rotary Dryer Heat & Mass Balance Evaporation Observer (2257 kJ/kg latent heat)
 *      - Aggregate Bed Flighting Curtain & Radiative Heat Transfer Observer (LMTD & Stefan-Boltzmann radiation)
 *      - Baghouse Filter Cake Resistance & Darcy-Ergun Pressure Drop Observer with Acid Dew Point Watchdog
 *      - Bitumen Walther-Andrade Non-Newtonian Dynamic Viscosity-Temperature Observer (ASTM D341)
 *      - Adaptive Gravimetric In-Flight Material Fall Cutoff Predictor (Kalman EMA update per bin)
 *      - Twin-Shaft Pugmill Shear Work & Asphalt Homogeneity Coating Index Observer
 *      - 7-Segment Jerk-Limited S-Curve Kinematic Motion Trajectory Generator for Skip Hoist
 *   5. Deterministic 12-Stage Operational Finite State Machine (FSM):
 *      - ST_PREPURGE_IGNITION (10) -> ST_COLD_FEED_PROPORTION (20) -> ST_DRUM_DRYING_BURNER_MOD (30) ->
 *        ST_HOT_SCREEN_BIN_STORAGE (40) -> ST_AGG_WEIGH_HOPPER_DOSING (50) -> ST_FILLER_DUST_ADDITION (60) ->
 *        ST_BITUMEN_PRESSURIZED_INJECTION (70) -> ST_TWINSHAFT_WET_MIX (80) -> ST_PUGMILL_DISCHARGE_GATE (90) ->
 *        ST_SKIP_HOIST_TRANSIT (100) -> ST_RECIPE_CHANGEOVER (110) -> ST_POST_COOLING_PURGE (120)
 *   6. Comprehensive ISA-18.2 Multi-Tiered Alarm Hierarchy:
 *      - HH, H, L, LL, Rate of Change (RoC) detection with positive/negative deadband hysteresis
 *      - 4 x 32-bit Packed Diagnostic Bit Registers (Process, Sensors, Actuators, Safety ESD)
 * =================================================================================================================== *)
""")

    # =========================================================================
    # 2. VAR_INPUT
    # =========================================================================
    parts.append("""VAR_INPUT
    (* Master Supervisory Commands & Operating Modes *)
    bEnable : BOOL; (* Master Automation Enable Interlock Signal [-] *)
    bEStop : BOOL; (* Emergency Stop Safety Circuit NC Contact [-] *)
    bAutoMode : BOOL; (* Fully Automatic Supervisory Sequencing Mode Selection [-] *)
    bStartCycle : BOOL; (* Start Production Batch Cycle Command [-] *)
    bStopCycle : BOOL; (* Normal Controlled Production Stop Command [-] *)
    bAcknowledgeFaults : BOOL; (* Operator Alarm & Trip Acknowledge Pulse [-] *)
    rCycleTime_s : REAL := 0.1; (* PLC Controller Deterministic Scan Task Period [s] *)

    (* Cold Aggregate Feeders & Moisture Inputs *)
    rColdBin1_BeltSpeed_Act : REAL; (* Cold Bin 1 (0-4mm Sand) Belt Feeder Speed Feedback [%] *)
    rColdBin2_BeltSpeed_Act : REAL; (* Cold Bin 2 (4-8mm Grit) Belt Feeder Speed Feedback [%] *)
    rColdBin3_BeltSpeed_Act : REAL; (* Cold Bin 3 (8-11mm Stone) Belt Feeder Speed Feedback [%] *)
    rColdBin4_BeltSpeed_Act : REAL; (* Cold Bin 4 (11-16mm Stone) Belt Feeder Speed Feedback [%] *)
    rColdBin5_BeltSpeed_Act : REAL; (* Cold Bin 5 (16-22mm Aggregate) Belt Feeder Speed Feedback [%] *)
    rColdBin6_BeltSpeed_Act : REAL; (* Cold Bin 6 (22-32mm Base Stone) Belt Feeder Speed Feedback [%] *)
    rColdMasterBelt_Flow_tph : REAL; (* Total Cold Feed Weighing Conveyor Mass Flow Rate [t/h] *)
    rAggregate_Moisture_In_pct : REAL; (* Cold Raw Aggregate Infeed Laboratory Moisture Content [%] *)
    rAmbient_AirTemp_degC : REAL := 20.0; (* Ambient Weather Atmospheric Air Temperature [deg C] *)
    rAmbient_AtmPressure_mbar : REAL := 1013.25; (* Barometric Ambient Pressure [mbar] *)

    (* Rotary Dryer & Modulating Burner TMR Channels & Static Pressures *)
    rDrum_Temp_Pyrometer_A_degC : REAL; (* Dryer Discharge Aggregate Temp Optical Pyrometer Ch A [deg C] *)
    rDrum_Temp_Pyrometer_B_degC : REAL; (* Dryer Discharge Aggregate Temp Optical Pyrometer Ch B [deg C] *)
    rDrum_Temp_Pyrometer_C_degC : REAL; (* Dryer Discharge Aggregate Temp Optical Pyrometer Ch C [deg C] *)
    bDrum_Temp_Pyrometer_A_WireBreak : BOOL; (* Optical Pyrometer Ch A Wire-Break Open-Circuit Fault [-] *)
    bDrum_Temp_Pyrometer_B_WireBreak : BOOL; (* Optical Pyrometer Ch B Wire-Break Open-Circuit Fault [-] *)
    bDrum_Temp_Pyrometer_C_WireBreak : BOOL; (* Optical Pyrometer Ch C Wire-Break Open-Circuit Fault [-] *)
    rDrum_Shell_Temp_degC : REAL; (* External Rotary Drum Steel Shell Surface Temperature [deg C] *)
    rDrum_FlueGas_ExitTemp_degC : REAL; (* Rotary Dryer Flue Gas Exit Breeching Temperature [deg C] *)
    rDrum_Burner_FuelPressure_bar : REAL; (* Dual-Fuel Burner Fuel Supply Manifold Pressure [bar] *)
    rDrum_Burner_FuelTemp_degC : REAL := 85.0; (* Heavy Fuel Oil Preheater Supply Temperature [deg C] *)
    rDrum_Burner_FlameIntensity_pct : REAL; (* Burner UV / IR Optical Flame Scanner Signal [%] *)
    rDrum_InternalDraft_mbar : REAL; (* Dryer Drum Combustion Chamber Static Pressure Draft [mbar] *)
    rDrum_Drive_Current_A : REAL; (* Rotary Dryer Trunnion Roller Drive Motor Current [A] *)

    (* Baghouse Dust Collector & Exhaust Gas Stream *)
    rBaghouse_DeltaP_mbar : REAL; (* Baghouse Filter Fabric Differential Pressure Drop [mbar] *)
    rBaghouse_InletTemp_degC : REAL; (* Baghouse Flue Gas Intake Temperature [deg C] *)
    rBaghouse_Exhaust_LEL_pct : REAL; (* Exhaust Flue Gas Combustible Hydrocarbon LEL Concentration [%] *)
    rBaghouse_PulseAir_Pressure_bar : REAL := 6.5; (* Baghouse Reverse Pulse-Jet Compressed Air Header [bar] *)
    rExhaust_Fan_Current_A : REAL; (* Exhaust Induced Draft (ID) Fan Electric Motor Current [A] *)
    rExhaust_Gas_O2_pct : REAL := 8.5; (* Flue Gas Zirconia Oxygen Analyzer Concentration [%] *)

    (* Hot Elevator, Vibrating Screen & Hot Bins *)
    rHotElevator_MotorPower_kW : REAL; (* Hot Aggregate Bucket Elevator Electric Motor Power [kW] *)
    rHotElevator_Speed_rpm : REAL; (* Hot Elevator Head Shaft Tachometer Speed [rpm] *)
    rHotElevator_ChainTension_kN : REAL := 45.0; (* Bucket Elevator Dynamic Chain Tension Load Cell [kN] *)
    rScreen_Vibration_RMS_mms : REAL; (* 6-Deck Vibrating Screen Accelerometer Vibration Velocity [mm/s] *)
    rScreen_Drive_Current_A : REAL; (* Vibrating Screen Dual Ecciter Motor Current [A] *)
    arrHotBin_Level_pct : ARRAY[1..6] OF REAL; (* Hot Storage Bins 1..6 Microwave Continuous Level [%] *)
    arrHotBin_Temp_degC : ARRAY[1..6] OF REAL; (* Hot Storage Bins 1..6 Core Temperature Probes [deg C] *)

    (* Gravimetric Pugmill Batch Scales TMR Load Cell Triad *)
    rWeighHopper_LoadCell_A_kg : REAL; (* Pugmill Aggregate Weigh Hopper Load Cell Triad Ch A [kg] *)
    rWeighHopper_LoadCell_B_kg : REAL; (* Pugmill Aggregate Weigh Hopper Load Cell Triad Ch B [kg] *)
    rWeighHopper_LoadCell_C_kg : REAL; (* Pugmill Aggregate Weigh Hopper Load Cell Triad Ch C [kg] *)
    bWeighHopper_LC_A_Fault : BOOL; (* Load Cell Channel A Hardware Sensor Fault [-] *)
    bWeighHopper_LC_B_Fault : BOOL; (* Load Cell Channel B Hardware Sensor Fault [-] *)
    bWeighHopper_LC_C_Fault : BOOL; (* Load Cell Channel C Hardware Sensor Fault [-] *)
    rFillerScale_Weight_kg : REAL; (* Mineral Filler & Reclaimed Dust Weigh Hopper Scale [kg] *)
    rFillerSilo_Level_pct : REAL := 65.0; (* Imported Fresh Mineral Dust Silo Level [%] *)
    rReclaimedFiller_Level_pct : REAL := 45.0; (* Baghouse Reclaimed Dust Intermediate Hopper Level [%] *)

    (* Bitumen Storage, Jacketed Heating & Pressurized Injection *)
    rBitumen_StorageTank_Temp_degC : REAL; (* Bitumen Bulk Storage Tank Core Temperature [deg C] *)
    rBitumen_ThermalOilJacket_degC : REAL; (* Bitumen Piping & Tank Thermal Oil Heating Jacket Temp [deg C] *)
    rBitumen_Spray_Pressure_bar : REAL; (* Bitumen Injection Manifold Delivery Pressure [bar] *)
    rBitumen_Flow_Coriolis_A_kgs : REAL; (* Bitumen Coriolis Mass Flow Meter Channel A [kg/s] *)
    rBitumen_Flow_Coriolis_B_kgs : REAL; (* Bitumen Coriolis Mass Flow Meter Channel B [kg/s] *)
    rBitumen_Flow_Coriolis_C_kgs : REAL; (* Bitumen Coriolis Mass Flow Meter Channel C [kg/s] *)
    bBitumen_Flow_Coriolis_A_Fault : BOOL; (* Coriolis Meter Ch A Diagnostic Transducer Fault [-] *)
    bBitumen_Flow_Coriolis_B_Fault : BOOL; (* Coriolis Meter Ch B Diagnostic Transducer Fault [-] *)
    bBitumen_Flow_Coriolis_C_Fault : BOOL; (* Coriolis Meter Ch C Diagnostic Transducer Fault [-] *)
    rBitumen_Density_kgm3 : REAL; (* Bitumen Fluid Real-Time Density from Coriolis Sensor [kg/m3] *)

    (* Twin-Shaft Pugmill Mixer & Skip Hoist Transducers *)
    rPugmill_Drive_Torque_Nm : REAL; (* Twin-Shaft Pugmill Drive Shaft Dynamic Mechanical Torque [Nm] *)
    rPugmill_Drive_Power_kW : REAL; (* Pugmill Dual Drive Motor Total Active Power [kW] *)
    rPugmill_BearingTemp_degC : REAL := 55.0; (* Pugmill Drive Shaft Heavy Spherical Roller Bearing Temp [deg C] *)
    rPugmill_Gate_Position_pct : REAL; (* Pneumatic Clam-Shell Discharge Gate Linear Position Feedback [%] *)
    bPugmill_Gate_Closed_LS : BOOL; (* Pugmill Clam-Shell Discharge Gate Fully Closed Limit Switch [-] *)
    bPugmill_Gate_Open_LS : BOOL; (* Pugmill Clam-Shell Discharge Gate Fully Open Limit Switch [-] *)
    rSkipHoist_Position_m : REAL; (* Asphalt Skip Hoist Carriage Track Linear Position [m] *)
    rSkipHoist_Velocity_ms : REAL; (* Skip Hoist Winch Absolute Travel Velocity [m/s] *)
    rSkipHoist_RopeTension_kN : REAL := 28.5; (* Skip Hoist Hoisting Cable Strain Gauge Tension [kN] *)
    bSkipHoist_Bottom_LS : BOOL; (* Skip Hoist Bottom Loading Position Proximity Switch [-] *)
    bSkipHoist_Top_LS : BOOL; (* Skip Hoist Top Silo Discharge Position Proximity Switch [-] *)
    bSkipHoist_SlackRope_Fault : BOOL; (* Skip Hoist Cable Slack Rope / Overtorque Safety Switch [-] *)
    iSelectedSilo_Bay : INT; (* Selected Finished Asphalt Storage Silo Compartment (1..4) [-] *)

    (* Recipe & Supervisory Production Target Setpoints *)
    rSP_Aggregate_ExitTemp_degC : REAL := 175.0; (* Recipe Aggregate Exit Target Temperature [deg C] *)
    rSP_TotalPlantThroughput_tph : REAL := 300.0; (* Desired Production Plant Mass Rate [t/h] *)
    rSP_BatchSize_kg : REAL := 4000.0; (* Standard Gravimetric Asphalt Pugmill Batch Weight [kg] *)
    arrRecipe_AggPercent : ARRAY[1..6] OF REAL; (* Cold/Hot Aggregate Size Fraction Recipe Distribution [%] *)
    rRecipe_FillerPercent : REAL := 5.0; (* Reclaimed & Mineral Filler Proportion in Recipe [%] *)
    rRecipe_BitumenPercent : REAL := 5.2; (* Optimum Bitumen Binder Proportion in Recipe [%] *)
    rRecipe_DryMixTime_s : REAL := 6.0; (* Dry Aggregate Homogenization Time in Pugmill [s] *)
    rRecipe_WetMixTime_s : REAL := 32.0; (* Wet Asphalt Binder Shear Dispersion Mixing Time [s] *)
END_VAR
""")

    # =========================================================================
    # 3. VAR_OUTPUT
    # =========================================================================
    parts.append("""VAR_OUTPUT
    (* Supervisory Status & State Machine Telemetry *)
    bPlantReady : BOOL; (* Asphalt Batch Plant Ready for Continuous Automatic Production [-] *)
    bPlantRunning : BOOL; (* Asphalt Batch Plant Active in Batching Sequence [-] *)
    iPlantState_Out : INT; (* Current 12-Stage Plant Finite State Machine Stage Number [-] *)
    iActiveBatchNumber : DINT; (* Cumulative Plant Batch Counter Identifier [-] *)
    rBatchCycleProgress_pct : REAL; (* Current Batch Execution Overall Progress Percentage [%] *)
    rTotalProductionMass_tonnes : REAL; (* Cumulative Asphalt Production Totalizer [t] *)

    (* Burner & Dryer Modulating Demands *)
    rBurner_FuelValve_Demand_pct : REAL; (* Modulating Burner Fuel Control Valve Command [%] *)
    rBurner_CombAir_VFD_Hz : REAL; (* Burner Forced Draft Combustion Air Fan Speed Reference [Hz] *)
    bBurner_PilotGas_Solenoid : BOOL; (* Burner Ignition Pilot Gas Safety Solenoid Energize [-] *)
    bBurner_Ignition_Spark : BOOL; (* High Voltage Ignition Transformer Spark Arc Request [-] *)
    rDrum_Drive_Speed_rpm : REAL; (* Rotary Dryer Drum Trunnion Roller Drive Speed Target [rpm] *)
    rExhaust_IDFan_Damper_pct : REAL; (* Exhaust Induced Draft Fan Modulation Damper / VFD [%] *)
    rBurner_AirFuel_Ratio : REAL; (* Calculated Stoichiometric Combustion Air to Fuel Ratio [-] *)
    rCalculated_FuelRate_kgh : REAL; (* Real-Time Instantaneous Fuel Mass Consumption Rate [kg/h] *)

    (* Baghouse Pulse-Jet & Emergency Bypass Solenoids *)
    bBaghouse_PulseValve_Fire : BOOL; (* Compressed Air Pulse-Jet Diaphragm Solenoid Manifold Fire Pulse [-] *)
    iBaghouse_ActiveRow : INT; (* Currently Pulsed Baghouse Filter Element Row Index (1..16) [-] *)
    bBaghouse_EmergencyBypass_Open : BOOL; (* Baghouse High-Temperature Gas Bypass Damper Trip Open [-] *)
    rBaghouse_ResidualResistance : REAL; (* Estimated Filter Fabric Permeability Resistance [1/m] *)

    (* Cold Dosing Belts & Master Feeder Demands *)
    arrColdBin_BeltSpeed_Cmd : ARRAY[1..6] OF REAL; (* Cold Bin 1..6 Variable Dosing Speed Commands [%] *)
    rColdMasterBelt_Speed_Cmd : REAL; (* Cold Aggregate Master Transfer Conveyor VFD Speed [%] *)
    rColdFeed_DryMassFlow_tph : REAL; (* Moisture-Compensated Net Dry Aggregate Flow Rate [t/h] *)

    (* Hot Bucket Elevator & Vibrating Screen Drives *)
    bHotElevator_Run_Cmd : BOOL; (* Hot Aggregate Bucket Elevator Main Drive Contactor Command [-] *)
    bScreen_Drive_Run_Cmd : BOOL; (* Multi-Deck Vibrating Screen Dual Eccentric Exciters Run [-] *)
    rElevator_SlipPercentage : REAL; (* Bucket Elevator Head-to-Tail Shaft Speed Slip Ratio [%] *)

    (* Gravimetric Hopper & Dosing Gates *)
    arrHotBin_Gate_Coarse_Cmd : ARRAY[1..6] OF BOOL; (* Hot Bin Discharge Clam-Shell Coarse Dosing Gate Cmd [-] *)
    arrHotBin_Gate_Fine_Cmd : ARRAY[1..6] OF BOOL; (* Hot Bin Discharge Clam-Shell Fine Dribble Gate Cmd [-] *)
    bWeighHopper_DischargeGate_Cmd : BOOL; (* Aggregate Weigh Hopper Bottom Rapid Discharge Flap Valve [-] *)
    bFiller_DosingScrew_Run_Cmd : BOOL; (* Mineral Filler Variable Pitch Metering Screw Feeder Run [-] *)
    bFiller_BlowpadFluidize_Cmd : BOOL; (* Filler Hopper Aeration Pad Fluidizing Solenoid [-] *)

    (* Bitumen Injection System Actuators *)
    rBitumen_Pump_Speed_Cmd_pct : REAL; (* Bitumen Metering Gear Pump Inverter Speed Command [%] *)
    bBitumen_SprayBar_Valve_Cmd : BOOL; (* High-Pressure Bitumen Spray Bar Pneumatic Diverter Valve [-] *)
    bBitumen_Recirc_Valve_Cmd : BOOL; (* Bitumen Continuous Heated Ring Line Recirculation Valve [-] *)
    rBitumen_InjectedTotal_kg : REAL; (* Measured Total Injected Bitumen Mass for Current Batch [kg] *)
    rBitumen_Viscosity_Feedback_cP : REAL; (* Dynamic Process Viscosity at Spray Nozzle Header [cP] *)

    (* Twin-Shaft Pugmill Mixer & Skip Hoist Actuation *)
    rPugmill_Drive_Speed_Hz : REAL; (* Twin-Shaft Pugmill Synchronized Drives Frequency Inverter [Hz] *)
    bPugmill_Discharge_Open_Cmd : BOOL; (* Pugmill Double Clam-Shell Bottom Discharge Gate Open Cmd [-] *)
    rPugmill_SpecificEnergy_kWht : REAL; (* Batch Specific Mechanical Mixing Energy Dissipated [kWh/t] *)
    rPugmill_Homogeneity_Index : REAL; (* Bitumen Binder Aggregate Film Homogeneity Index (0.0 to 1.0) [-] *)
    rSkipHoist_Drive_Speed_Cmd_pct : REAL; (* Skip Hoist Winch Closed-Loop Vector Drive Reference [%] *)
    bSkipHoist_Brake_Release_Cmd : BOOL; (* Skip Hoist Fail-Safe Mechanical Disc Brake Release Solenoid [-] *)
    bSkipHoist_DischargeFlap_Cmd : BOOL; (* Skip Hoist Silo Distributor Flap Valve Open Command [-] *)
    rSkipHoist_InstantaneousPower_kW : REAL; (* Mechanical Hoist Motor Shaft Power [kW] *)

    (* ISA-18.2 Diagnostic Alarm Registers & Safety Trips *)
    dwAlarmWord0_Process : DWORD; (* ISA-18.2 Process Parameter Diagnostic Bit Register [HEX] *)
    dwAlarmWord1_SensorsTMR : DWORD; (* 2oo3 TMR Sensor Redundancy & Transducer Fault Word [HEX] *)
    dwAlarmWord2_ActuatorsInterlocks : DWORD; (* Mechanical Actuator, Drive & Interlock Fault Word [HEX] *)
    dwAlarmWord3_SafetyESD : DWORD; (* Emergency Safety Shutdown & Permissive Interlock Word [HEX] *)
    bMasterPlantTrip : BOOL; (* Master Critical Plant Emergency Safety Interlock Trip [-] *)
END_VAR
""")

    # =========================================================================
    # 4. VAR (INTERNAL DATA STRUCTURES)
    # =========================================================================
    parts.append("""VAR
    (* ---------------------------------------------------------------------------------------------------------------
     * Internal State Flags & Mathematical Constants
     * --------------------------------------------------------------------------------------------------------------- *)
    bInitDone : BOOL := FALSE; (* Deterministic First-Scan Initialization Flag *)
    c_rCp_Stone : REAL := 0.880; (* Specific Heat Capacity of Dry Granite/Basalt Aggregate [kJ/(kg*K)] *)
    c_rCp_Water : REAL := 4.184; (* Specific Heat Capacity of Liquid Water [kJ/(kg*K)] *)
    c_rDeltaH_Vap : REAL := 2257.0; (* Latent Heat of Evaporative Vaporization of Water at 100 deg C [kJ/kg] *)
    c_rCp_Steam : REAL := 2.010; (* Specific Heat Capacity of Superheated Water Vapor [kJ/(kg*K)] *)
    c_rAirDensity_Std : REAL := 1.204; (* Dry Air Density at Standard Temperature and Pressure [kg/m3] *)
    c_rGravity : REAL := 9.80665; (* Standard Acceleration of Gravity [m/s2] *)
    c_rGasConstant_R : REAL := 8.314; (* Universal Molar Gas Constant [J/(mol*K)] *)
    c_rStefanBoltzmann : REAL := 5.67037E-8; (* Stefan-Boltzmann Radiation Constant [W/(m2*K4)] *)
    c_rFuelNetCalorific_MJkg : REAL := 42.5; (* Net Lower Heating Value of Heavy Fuel Oil [MJ/kg] *)

    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete State-Space (8x8) System Matrices & MPC Variables
     * States x: [1:DrumShellTemp, 2:FlueGasTemp, 3:MoistEvapRate, 4:ElevatorLoad, 5:BaghouseDP, 6:BitumenJacketTemp, 7:PugmillTorque, 8:SkipVelocity]
     * Inputs u: [1:BurnerFuelCmd, 2:CombAirHz, 3:ColdFeedRate, 4:IDFanDamper, 5:ThermalOilValve, 6:PugmillSpeedHz]
     * --------------------------------------------------------------------------------------------------------------- *)
    arrA : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix A (8x8) *)
    arrB : ARRAY[1..8, 1..6] OF REAL; (* Discrete Input Coupling Matrix B (8x6) *)
    arrC : ARRAY[1..8, 1..8] OF REAL; (* Discrete Output Mapping Matrix C (8x8) *)
    arrD : ARRAY[1..8, 1..6] OF REAL; (* Discrete Direct Feedthrough Matrix D (8x6) *)

    arrX_state : ARRAY[1..8] OF REAL; (* Current State Deviation Vector x[k] *)
    arrX_pred : ARRAY[1..8] OF REAL; (* 1-Step Predictive State Vector x[k+1] *)
    arrX_ref : ARRAY[1..8] OF REAL; (* State Reference Trajectory Vector x_ref *)
    arrU_control : ARRAY[1..6] OF REAL; (* Control Action Vector u[k] *)
    arrU_prev : ARRAY[1..6] OF REAL; (* Previous Control Action Vector u[k-1] *)
    arrU_delta : ARRAY[1..6] OF REAL; (* Control Slew Rate Vector delta_u[k] *)
    arrGrad_u : ARRAY[1..6] OF REAL; (* Analytical Cost Gradient Vector dJ/du *)
    arrY_output : ARRAY[1..8] OF REAL; (* Simulated Output Vector y[k] *)

    (* MPC Quadratic Cost Penalties *)
    arrQ_Weight : ARRAY[1..8] OF REAL; (* State Error Quadratic Penalty Weights Q *)
    arrR_Weight : ARRAY[1..6] OF REAL; (* Control Effort Penalty Weights R *)
    arrS_Weight : ARRAY[1..6] OF REAL; (* Control Rate Slew Penalty Weights S *)
    arrP_TerminalWeight : ARRAY[1..8] OF REAL; (* Terminal State Penalty Weights P *)
    c_rMPC_Alpha : REAL := 0.0125; (* Projected Gradient Descent (PGD) Step Size Alpha *)

    (* Detailed Cost Tracking for MPC Diagnostics *)
    rMPC_Cost_State : REAL := 0.0; (* Accumulated State Deviation Cost J_Q *)
    rMPC_Cost_Control : REAL := 0.0; (* Control Effort Energy Cost J_R *)
    rMPC_Cost_Slew : REAL := 0.0; (* Control Slew Rate Cost J_S *)
    rMPC_Cost_Terminal : REAL := 0.0; (* Horizon Terminal State Penalty J_P *)
    rMPC_Cost_Total : REAL := 0.0; (* Total Quadratic Objective Cost J *)

    (* ---------------------------------------------------------------------------------------------------------------
     * 2oo3 Triple Modular Redundancy (TMR) Structures
     * --------------------------------------------------------------------------------------------------------------- *)
    (* TMR 1: Rotary Dryer Aggregate Exit Optical Pyrometers [deg C] *)
    rVoted_DrumExitTemp_degC : REAL; (* Voted Aggregate Exit Temperature [deg C] *)
    bTMR1_FaultA : BOOL; (* Pyrometer Channel A Discrepancy Fault Latch *)
    bTMR1_FaultB : BOOL; (* Pyrometer Channel B Discrepancy Fault Latch *)
    bTMR1_FaultC : BOOL; (* Pyrometer Channel C Discrepancy Fault Latch *)
    tTMR1_TimerA : REAL; (* Channel A Discrepancy Accumulation Timer [s] *)
    tTMR1_TimerB : REAL; (* Channel B Discrepancy Accumulation Timer [s] *)
    tTMR1_TimerC : REAL; (* Channel C Discrepancy Accumulation Timer [s] *)
    iTMR1_HealthGrade : INT := 3; (* TMR1 Redundancy Health (3:Triple, 2:Dual, 1:Single, 0:Tripped) *)
    c_rTMR1_DiscrepancyLimit_degC : REAL := 12.0; (* Allowable Inter-Channel Temperature Discrepancy [deg C] *)
    c_rTMR1_FaultDelay_s : REAL := 2.5; (* Channel Fault Confirmation Time Delay [s] *)

    (* TMR 2: Pugmill Aggregate Weigh Hopper Gravimetric Load Cells [kg] *)
    rVoted_WeighHopper_kg : REAL; (* Voted Gravimetric Aggregate Mass [kg] *)
    bTMR2_FaultA : BOOL; (* Load Cell Channel A Discrepancy Fault Latch *)
    bTMR2_FaultB : BOOL; (* Load Cell Channel B Discrepancy Fault Latch *)
    bTMR2_FaultC : BOOL; (* Load Cell Channel C Discrepancy Fault Latch *)
    tTMR2_TimerA : REAL; (* Load Cell A Discrepancy Timer [s] *)
    tTMR2_TimerB : REAL; (* Load Cell B Discrepancy Timer [s] *)
    tTMR2_TimerC : REAL; (* Load Cell C Discrepancy Timer [s] *)
    iTMR2_HealthGrade : INT := 3; (* TMR2 Redundancy Health Grade *)
    c_rTMR2_DiscrepancyLimit_kg : REAL := 25.0; (* Allowable Inter-Channel Mass Discrepancy [kg] *)
    c_rTMR2_FaultDelay_s : REAL := 1.8; (* Load Cell Fault Delay [s] *)

    (* TMR 3: Bitumen High-Pressure Coriolis Mass Flow Meters [kg/s] *)
    rVoted_BitumenFlow_kgs : REAL; (* Voted Bitumen Mass Flow Rate [kg/s] *)
    bTMR3_FaultA : BOOL; (* Bitumen Coriolis Ch A Discrepancy Fault Latch *)
    bTMR3_FaultB : BOOL; (* Bitumen Coriolis Ch B Discrepancy Fault Latch *)
    bTMR3_FaultC : BOOL; (* Bitumen Coriolis Ch C Discrepancy Fault Latch *)
    tTMR3_TimerA : REAL; (* Bitumen Ch A Discrepancy Timer [s] *)
    tTMR3_TimerB : REAL; (* Bitumen Ch B Discrepancy Timer [s] *)
    tTMR3_TimerC : REAL; (* Bitumen Ch C Discrepancy Timer [s] *)
    iTMR3_HealthGrade : INT := 3; (* TMR3 Redundancy Health Grade *)
    c_rTMR3_DiscrepancyLimit_kgs : REAL := 0.75; (* Allowable Inter-Channel Flow Discrepancy [kg/s] *)
    c_rTMR3_FaultDelay_s : REAL := 1.5; (* Bitumen Coriolis Fault Delay [s] *)

    (* ---------------------------------------------------------------------------------------------------------------
     * Cyber-Physical Process Observers & Numerical Model State
     * --------------------------------------------------------------------------------------------------------------- *)
    (* 1. Rotary Dryer Coupled Heat & Mass Balance Evaporation Observer *)
    rObs_AggregateMassFlow_kgs : REAL; (* Calculated Dry Aggregate Throughput [kg/s] *)
    rObs_WaterMassFlow_kgs : REAL; (* Calculated Raw Moisture Evaporation Mass Rate [kg/s] *)
    rObs_EnthalpyStone_kW : REAL; (* Sensible Thermal Power Required to Heat Mineral Aggregates [kW] *)
    rObs_EnthalpyWater_kW : REAL; (* Latent + Sensible Thermal Power to Vaporize Aggregate Moisture [kW] *)
    rObs_ShellLossRadiation_kW : REAL; (* External Shell Radiative and Convective Thermal Loss [kW] *)
    rObs_TotalThermalPowerReq_kW : REAL; (* Net Theoretical Burner Thermal Duty Requirement [kW] *)
    rObs_BurnerFiringRate_Theoretical_pct : REAL; (* Theoretical Feedforward Burner Modulation Demand [%] *)
    rObs_ThermalEfficiency_pct : REAL := 82.5; (* Estimated Drum Thermal Efficiency [%] *)

    (* 2. Aggregate Bed Flighting Curtain & Radiative Heat Transfer Observer *)
    rObs_DrumCurtainDensity_kgm3 : REAL; (* Cascading Mineral Stone Curtain Volumetric Density [kg/m3] *)
    rObs_FlameTemp_Estimated_degC : REAL; (* Burner Core Combustion Flame Temperature Estimate [deg C] *)
    rObs_RadiationHeatFlux_kWm2 : REAL; (* Radiative Heat Flux from Flame Core to Cascade Stone [kW/m2] *)
    rObs_LMTD_Counterflow_K : REAL; (* Logarithmic Mean Temperature Difference across Rotary Drum [K] *)

    (* 3. Baghouse Filter Cake Resistance & Darcy-Ergun Observer *)
    rObs_FilterFaceVelocity_ms : REAL; (* Flue Gas Interstitial Filtration Face Velocity [m/s] *)
    rObs_DustCakeMass_kg : REAL; (* Estimated Accumulation of Dust Cake on Filter Fabric [kg] *)
    rObs_DarcyPermeability : REAL := 1.85E-11; (* Clean Fabric Darcy Permeability [m2] *)
    rObs_CakeSpecificResistance : REAL := 4.25E8; (* Specific Resistance of Limestone Dust Cake [m/kg] *)
    rObs_CalculatedDeltaP_mbar : REAL; (* Observer Predicted Fabric Pressure Drop [mbar] *)
    rObs_FlueGas_AcidDewPoint_degC : REAL; (* Calculated Sulfuric Acid / Water Dew Point [deg C] *)
    tPulseJet_Timer : REAL := 0.0; (* Pulse-Jet Periodic Sequencing Timer [s] *)
    rPulseJet_Interval_s : REAL := 15.0; (* Dynamic Pulse-Jet Cleaning Interval [s] *)

    (* 4. Bitumen Walther-Andrade Non-Newtonian Dynamic Viscosity Observer *)
    rObs_BitumenDynamicViscosity_cP : REAL; (* Real-Time Temperature-Corrected Dynamic Viscosity [cP] *)
    rObs_BitumenKinematicViscosity_cSt : REAL; (* Real-Time Kinematic Viscosity [cSt] *)
    rObs_WaltherLogTerm : REAL; (* Walther Equation Intermediate Logarithmic Variable *)
    rObs_ViscositySprayIndex : REAL; (* Dimensionless Atomization Spray Index *)
    rObs_SauterMeanDiameter_um : REAL; (* Estimated Spray Droplet Sauter Mean Diameter SMD [um] *)

    (* 5. Adaptive Gravimetric In-Flight Material Fall Cutoff Predictor *)
    arrInflightComp_Agg_kg : ARRAY[1..6] OF REAL; (* Dynamic In-Flight Mass Estimation per Hot Bin [kg] *)
    rInflightComp_Filler_kg : REAL := 12.5; (* Dynamic In-Flight Mass for Mineral Dust Screw [kg] *)
    rInflightComp_Bitumen_kg : REAL := 3.2; (* Dynamic In-Flight Bitumen Spray Mass [kg] *)
    c_rInflight_Alpha : REAL := 0.15; (* Exponential Moving Average Adaptive Learning Rate *)

    (* 6. Twin-Shaft Pugmill Dynamic Mixing Work & Homogeneity Coating Observer *)
    rObs_PugmillAngularVelocity_rads : REAL; (* Dual Shaft Rotational Angular Velocity [rad/s] *)
    rObs_PugmillMechanicalPower_kW : REAL; (* Computed Net Shaft Dynamic Mechanical Power [kW] *)
    rObs_CumulativeMixEnergy_kJ : REAL; (* Accumulated Mechanical Shear Energy Input to Batch [kJ] *)
    rObs_AsphaltHomogeneityIndex : REAL; (* Dimensionless Binder Film Uniformity Coating Index (0.0 to 1.0) *)
    rObs_TorqueRateOfChange_Nms : REAL; (* Instantaneous Rate of Torque Change d(tau)/dt [Nm/s] *)
    rPrev_PugmillTorque_Nm : REAL; (* Previous Scan Mixing Torque [Nm] *)

    (* 7. Skip Hoist 7-Segment Jerk-Limited S-Curve Kinematic Trajectory Generator *)
    rTraj_PosCmd_m : REAL; (* Commanded Skip Hoist Carriage Position [m] *)
    rTraj_VelCmd_ms : REAL; (* Commanded Skip Hoist Carriage Velocity [m/s] *)
    rTraj_AccCmd_ms2 : REAL; (* Commanded Skip Hoist Carriage Acceleration [m/s2] *)
    rSkip_TargetPos_m : REAL := 0.0; (* Target Elevation for Current Silo Selection [m] *)
    iSkip_MotionSegment : INT := 0; (* Active S-Curve Kinematic Segment (0..7) *)
    tSkip_SegmentTimer : REAL := 0.0; (* S-Curve Segment Elapsed Timer [s] *)
    c_rSkip_MaxVel_ms : REAL := 2.2; (* Maximum Rated Skip Hoist Travel Velocity [m/s] *)
    c_rSkip_MaxAcc_ms2 : REAL := 0.85; (* Maximum Kinematic Linear Acceleration [m/s2] *)
    c_rSkip_MaxJerk_ms3 : REAL := 1.50; (* Maximum Kinematic Rate of Acceleration Change (Jerk) [m/s3] *)

    (* ---------------------------------------------------------------------------------------------------------------
     * 12-Stage Deterministic Operational Finite State Machine (FSM) Variables
     * --------------------------------------------------------------------------------------------------------------- *)
    iPlantState : INT := 10; (* Current Active Plant Operational State *)
    iPreviousState : INT := 10; (* Previous Scan Operational State *)
    tStateTimer_s : REAL := 0.0; (* Current Operational State Elapsed Time [s] *)
    iActiveDosingBin : INT := 1; (* Currently Metering Aggregate Hot Bin (1..6) *)
    rDosingBin_TargetWeight_kg : REAL := 0.0; (* Target Net Cumulative Weight for Current Dosing Bin [kg] *)
    rDosingBin_CutoffWeight_kg : REAL := 0.0; (* Calculated Gate Cutoff Weight with In-Flight Drop [kg] *)
    rBatchAgg_Accumulated_kg : REAL := 0.0; (* Measured Total Aggregate Mass Loaded into Hopper [kg] *)
    rBatchFiller_Accumulated_kg : REAL := 0.0; (* Measured Total Mineral Filler Loaded [kg] *)
    rBatchBitumen_Accumulated_kg : REAL := 0.0; (* Measured Total Injected Bitumen Mass [kg] *)
    tDryMix_Timer_s : REAL := 0.0; (* Dry Aggregate Mixing Phase Elapsed Timer [s] *)
    tWetMix_Timer_s : REAL := 0.0; (* Wet Asphalt Binder Mixing Phase Elapsed Timer [s] *)
    tDischarge_Timer_s : REAL := 0.0; (* Pugmill Discharge Gate Open Elapsed Timer [s] *)

    (* FSM State Enumeration Constants *)
    c_ST_PREPURGE_IGNITION : INT := 10;
    c_ST_COLD_FEED_PROPORTION : INT := 20;
    c_ST_DRUM_DRYING_BURNER_MOD : INT := 30;
    c_ST_HOT_SCREEN_BIN_STORAGE : INT := 40;
    c_ST_AGG_WEIGH_HOPPER_DOSING : INT := 50;
    c_ST_FILLER_DUST_ADDITION : INT := 60;
    c_ST_BITUMEN_PRESSURIZED_INJECTION : INT := 70;
    c_ST_TWINSHAFT_WET_MIX : INT := 80;
    c_ST_PUGMILL_DISCHARGE_GATE : INT := 90;
    c_ST_SKIP_HOIST_TRANSIT : INT := 100;
    c_ST_RECIPE_CHANGEOVER : INT := 110;
    c_ST_POST_COOLING_PURGE : INT := 120;

    (* ---------------------------------------------------------------------------------------------------------------
     * ISA-18.2 Multi-Tiered Alarm Engine Registers & Thresholds
     * --------------------------------------------------------------------------------------------------------------- *)
    (* Alarm Limit Thresholds *)
    c_rDrumExitTemp_HH_degC : REAL := 210.0;
    c_rDrumExitTemp_H_degC : REAL := 195.0;
    c_rDrumExitTemp_L_degC : REAL := 145.0;
    c_rDrumExitTemp_LL_degC : REAL := 130.0;
    c_rDrumExitTemp_Deadband : REAL := 3.0;

    c_rBaghouseInletTemp_HH_degC : REAL := 215.0;
    c_rBaghouseInletTemp_H_degC : REAL := 198.0;
    c_rBaghouseDeltaP_HH_mbar : REAL := 22.0;
    c_rBaghouseDeltaP_H_mbar : REAL := 16.5;
    c_rBaghouseLEL_HH_pct : REAL := 25.0;
    c_rBaghouseLEL_H_pct : REAL := 15.0;

    c_rBitumenTemp_HH_degC : REAL := 190.0;
    c_rBitumenTemp_H_degC : REAL := 180.0;
    c_rBitumenTemp_L_degC : REAL := 140.0;
    c_rBitumenTemp_LL_degC : REAL := 125.0;

    c_rPugmillTorque_HH_Nm : REAL := 8500.0;
    c_rPugmillTorque_H_Nm : REAL := 7200.0;

    (* Alarm State Latches *)
    bAlarm_DrumTemp_HH : BOOL := FALSE;
    bAlarm_DrumTemp_H : BOOL := FALSE;
    bAlarm_DrumTemp_L : BOOL := FALSE;
    bAlarm_DrumTemp_LL : BOOL := FALSE;
    bAlarm_DrumTemp_RoC : BOOL := FALSE;
    bAlarm_BaghouseTemp_HH : BOOL := FALSE;
    bAlarm_BaghouseTemp_H : BOOL := FALSE;
    bAlarm_BaghouseDeltaP_HH : BOOL := FALSE;
    bAlarm_BaghouseDeltaP_H : BOOL := FALSE;
    bAlarm_BaghouseDeltaP_RoC : BOOL := FALSE;
    bAlarm_BaghouseLEL_HH : BOOL := FALSE;
    bAlarm_BaghouseLEL_H : BOOL := FALSE;
    bAlarm_BitumenTemp_HH : BOOL := FALSE;
    bAlarm_BitumenTemp_H : BOOL := FALSE;
    bAlarm_BitumenTemp_L : BOOL := FALSE;
    bAlarm_BitumenTemp_LL : BOOL := FALSE;
    bAlarm_PugmillTorque_HH : BOOL := FALSE;
    bAlarm_PugmillTorque_H : BOOL := FALSE;
    bAlarm_FlameFailure : BOOL := FALSE;
    bAlarm_DrumDraftLoss : BOOL := FALSE;
    bAlarm_HotElevatorSlip : BOOL := FALSE;
    bAlarm_ScreenBlinding : BOOL := FALSE;
    bAlarm_BitumenPressure_L : BOOL := FALSE;
    bAlarm_PulseAirPressure_L : BOOL := FALSE;

    (* Previous Value Tracking for Rate of Change (RoC) Alarms *)
    rPrev_DrumExitTemp_degC : REAL;
    rRateOfChange_DrumExitTemp : REAL;
    rPrev_BaghouseDeltaP_mbar : REAL;
    rRateOfChange_BaghouseDeltaP : REAL;

    (* General Purpose Loop Iterators *)
    kStateIdx : INT;
    mInIdx : INT;
    iMatRow : INT;
    iMatCol : INT;
    iterMPC : INT;
    iBinIdx : INT;
    rTempSum : REAL;
    rTempGrad : REAL;
END_VAR
""")

    # =========================================================================
    # 5. PHASE 0: DETERMINISTIC INITIALIZATION OF MATRICES
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 0: DETERMINISTIC INITIALIZATION OF DISCRETE STATE-SPACE (8x8) & MPC MATRICES
 * =================================================================================================================== *)
IF NOT bInitDone THEN
    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete State Transition Matrix A (8x8) Discretized at Ts = 0.1 s
     * States: 1:DrumShellTemp, 2:FlueGasExitTemp, 3:MoistEvaporationRate, 4:ElevatorLoad,
     *         5:BaghouseDeltaP, 6:BitumenJacketTemp, 7:PugmillTorque, 8:SkipVelocity
     * --------------------------------------------------------------------------------------------------------------- *)
    arrA[1, 1] := 0.99850; arrA[1, 2] := 0.00120; arrA[1, 3] := -0.00045; arrA[1, 4] := 0.00000; arrA[1, 5] := 0.00000; arrA[1, 6] := 0.00000; arrA[1, 7] := 0.00000; arrA[1, 8] := 0.00000;
    arrA[2, 1] := 0.00210; arrA[2, 2] := 0.99580; arrA[2, 3] := -0.00850; arrA[2, 4] := 0.00000; arrA[2, 5] := 0.00015; arrA[2, 6] := 0.00000; arrA[2, 7] := 0.00000; arrA[2, 8] := 0.00000;
    arrA[3, 1] := 0.00050; arrA[3, 2] := 0.00110; arrA[3, 3] := 0.98200; arrA[3, 4] := 0.00000; arrA[3, 5] := 0.00000; arrA[3, 6] := 0.00000; arrA[3, 7] := 0.00000; arrA[3, 8] := 0.00000;
    arrA[4, 1] := 0.00000; arrA[4, 2] := 0.00000; arrA[4, 3] := 0.00000; arrA[4, 4] := 0.99650; arrA[4, 5] := 0.00000; arrA[4, 6] := 0.00000; arrA[4, 7] := 0.00000; arrA[4, 8] := 0.00000;
    arrA[5, 1] := 0.00000; arrA[5, 2] := 0.00085; arrA[5, 3] := 0.00240; arrA[5, 4] := 0.00000; arrA[5, 5] := 0.99820; arrA[5, 6] := 0.00000; arrA[5, 7] := 0.00000; arrA[5, 8] := 0.00000;
    arrA[6, 1] := 0.00000; arrA[6, 2] := 0.00000; arrA[6, 3] := 0.00000; arrA[6, 4] := 0.00000; arrA[6, 5] := 0.00000; arrA[6, 6] := 0.99910; arrA[6, 7] := 0.00000; arrA[6, 8] := 0.00000;
    arrA[7, 1] := 0.00000; arrA[7, 2] := 0.00000; arrA[7, 3] := 0.00000; arrA[7, 4] := 0.00000; arrA[7, 5] := 0.00000; arrA[6, 6] := 0.00000; arrA[7, 7] := 0.99450; arrA[7, 8] := 0.00000;
    arrA[8, 1] := 0.00000; arrA[8, 2] := 0.00000; arrA[8, 3] := 0.00000; arrA[8, 4] := 0.00000; arrA[8, 5] := 0.00000; arrA[8, 6] := 0.00000; arrA[8, 7] := 0.00000; arrA[8, 8] := 0.99700;

    (* ---------------------------------------------------------------------------------------------------------------
     * Discrete Input Coupling Matrix B (8x6) Discretized at Ts = 0.1 s
     * Inputs: 1:BurnerFuelCmd [%], 2:CombAirHz [Hz], 3:ColdFeedRate [t/h], 4:IDFanDamper [%],
     *         5:ThermalOilValve [%], 6:PugmillSpeedHz [Hz]
     * --------------------------------------------------------------------------------------------------------------- *)
    arrB[1, 1] := 0.00850; arrB[1, 2] := -0.00120; arrB[1, 3] := -0.00220; arrB[1, 4] := -0.00080; arrB[1, 5] := 0.00000; arrB[1, 6] := 0.00000;
    arrB[2, 1] := 0.02450; arrB[2, 2] := -0.00480; arrB[2, 3] := -0.00760; arrB[2, 4] := 0.00650; arrB[2, 5] := 0.00000; arrB[2, 6] := 0.00000;
    arrB[3, 1] := 0.01120; arrB[3, 2] := 0.00210; arrB[3, 3] := 0.01540; arrB[3, 4] := 0.00180; arrB[3, 5] := 0.00000; arrB[3, 6] := 0.00000;
    arrB[4, 1] := 0.00000; arrB[4, 2] := 0.00000; arrB[4, 3] := 0.04500; arrB[4, 4] := 0.00000; arrB[4, 5] := 0.00000; arrB[4, 6] := 0.00000;
    arrB[5, 1] := 0.00140; arrB[5, 2] := 0.00280; arrB[5, 3] := 0.00850; arrB[5, 4] := 0.01250; arrB[5, 5] := 0.00000; arrB[5, 6] := 0.00000;
    arrB[6, 1] := 0.00000; arrB[6, 2] := 0.00000; arrB[6, 3] := 0.00000; arrB[6, 4] := 0.00000; arrB[6, 5] := 0.01850; arrB[6, 6] := 0.00000;
    arrB[7, 1] := 0.00000; arrB[7, 2] := 0.00000; arrB[7, 3] := 0.00000; arrB[7, 4] := 0.00000; arrB[7, 5] := 0.00000; arrB[7, 6] := 14.85000;
    arrB[8, 1] := 0.00000; arrB[8, 2] := 0.00000; arrB[8, 3] := 0.00000; arrB[8, 4] := 0.00000; arrB[8, 5] := 0.00000; arrB[8, 6] := 0.00000;

    (* Output Mapping Matrix C (8x8) Identity Matrix *)
    FOR iMatRow := 1 TO 8 DO
        FOR iMatCol := 1 TO 8 DO
            IF iMatRow = iMatCol THEN
                arrC[iMatRow, iMatCol] := 1.0;
            ELSE
                arrC[iMatRow, iMatCol] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* Direct Feedthrough Matrix D (8x6) Zero Matrix *)
    FOR iMatRow := 1 TO 8 DO
        FOR mInIdx := 1 TO 6 DO
            arrD[iMatRow, mInIdx] := 0.0;
        END_FOR;
    END_FOR;

    (* MPC Quadratic Weights *)
    arrQ_Weight[1] := 1.5; (* Drum shell temp *)
    arrQ_Weight[2] := 2.8; (* Flue gas exit temp *)
    arrQ_Weight[3] := 4.2; (* Moisture evaporation rate *)
    arrQ_Weight[4] := 0.5; (* Bucket elevator load *)
    arrQ_Weight[5] := 3.6; (* Baghouse differential pressure *)
    arrQ_Weight[6] := 2.2; (* Bitumen jacket temp *)
    arrQ_Weight[7] := 1.8; (* Pugmill torque *)
    arrQ_Weight[8] := 0.8; (* Skip hoist velocity *)

    arrR_Weight[1] := 0.25; (* Fuel valve command *)
    arrR_Weight[2] := 0.15; (* Combustion air Hz *)
    arrR_Weight[3] := 0.40; (* Cold aggregate feed rate *)
    arrR_Weight[4] := 0.18; (* ID fan damper *)
    arrR_Weight[5] := 0.12; (* Thermal oil valve *)
    arrR_Weight[6] := 0.10; (* Pugmill frequency *)

    arrS_Weight[1] := 0.65; (* Slew penalty fuel *)
    arrS_Weight[2] := 0.35; (* Slew penalty air *)
    arrS_Weight[3] := 0.80; (* Slew penalty cold feed *)
    arrS_Weight[4] := 0.45; (* Slew penalty ID fan *)
    arrS_Weight[5] := 0.30; (* Slew penalty thermal oil *)
    arrS_Weight[6] := 0.20; (* Slew penalty pugmill *)

    arrP_TerminalWeight[1] := 3.5;
    arrP_TerminalWeight[2] := 5.2;
    arrP_TerminalWeight[3] := 8.4;
    arrP_TerminalWeight[4] := 1.0;
    arrP_TerminalWeight[5] := 7.0;
    arrP_TerminalWeight[6] := 4.5;
    arrP_TerminalWeight[7] := 3.6;
    arrP_TerminalWeight[8] := 1.6;

    (* Initial In-Flight Dropping Masses *)
    arrInflightComp_Agg_kg[1] := 32.0;
    arrInflightComp_Agg_kg[2] := 28.0;
    arrInflightComp_Agg_kg[3] := 25.0;
    arrInflightComp_Agg_kg[4] := 22.0;
    arrInflightComp_Agg_kg[5] := 18.0;
    arrInflightComp_Agg_kg[6] := 15.0;

    bInitDone := TRUE;
END_IF;
""")

    # =========================================================================
    # 6. PHASE 1: 2oo3 TMR SENSOR VOTING ENGINE
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINE
 * =================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------
 * TMR 1: Rotary Dryer Aggregate Exit Optical Pyrometers (A, B, C) [deg C]
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Calculate Inter-Channel Discrepancies and Detect Wire-Breaks *)
IF bDrum_Temp_Pyrometer_A_WireBreak OR rDrum_Temp_Pyrometer_A_degC < 0.0 OR rDrum_Temp_Pyrometer_A_degC > 350.0 THEN
    bTMR1_FaultA := TRUE;
ELSIF ABS(rDrum_Temp_Pyrometer_A_degC - rDrum_Temp_Pyrometer_B_degC) > c_rTMR1_DiscrepancyLimit_degC AND
      ABS(rDrum_Temp_Pyrometer_A_degC - rDrum_Temp_Pyrometer_C_degC) > c_rTMR1_DiscrepancyLimit_degC THEN
    tTMR1_TimerA := tTMR1_TimerA + rCycleTime_s;
    IF tTMR1_TimerA >= c_rTMR1_FaultDelay_s THEN
        bTMR1_FaultA := TRUE;
    END_IF;
ELSE
    tTMR1_TimerA := MAX(0.0, tTMR1_TimerA - (1.5 * rCycleTime_s));
END_IF;

IF bDrum_Temp_Pyrometer_B_WireBreak OR rDrum_Temp_Pyrometer_B_degC < 0.0 OR rDrum_Temp_Pyrometer_B_degC > 350.0 THEN
    bTMR1_FaultB := TRUE;
ELSIF ABS(rDrum_Temp_Pyrometer_B_degC - rDrum_Temp_Pyrometer_A_degC) > c_rTMR1_DiscrepancyLimit_degC AND
      ABS(rDrum_Temp_Pyrometer_B_degC - rDrum_Temp_Pyrometer_C_degC) > c_rTMR1_DiscrepancyLimit_degC THEN
    tTMR1_TimerB := tTMR1_TimerB + rCycleTime_s;
    IF tTMR1_TimerB >= c_rTMR1_FaultDelay_s THEN
        bTMR1_FaultB := TRUE;
    END_IF;
ELSE
    tTMR1_TimerB := MAX(0.0, tTMR1_TimerB - (1.5 * rCycleTime_s));
END_IF;

IF bDrum_Temp_Pyrometer_C_WireBreak OR rDrum_Temp_Pyrometer_C_degC < 0.0 OR rDrum_Temp_Pyrometer_C_degC > 350.0 THEN
    bTMR1_FaultC := TRUE;
ELSIF ABS(rDrum_Temp_Pyrometer_C_degC - rDrum_Temp_Pyrometer_A_degC) > c_rTMR1_DiscrepancyLimit_degC AND
      ABS(rDrum_Temp_Pyrometer_C_degC - rDrum_Temp_Pyrometer_B_degC) > c_rTMR1_DiscrepancyLimit_degC THEN
    tTMR1_TimerC := tTMR1_TimerC + rCycleTime_s;
    IF tTMR1_TimerC >= c_rTMR1_FaultDelay_s THEN
        bTMR1_FaultC := TRUE;
    END_IF;
ELSE
    tTMR1_TimerC := MAX(0.0, tTMR1_TimerC - (1.5 * rCycleTime_s));
END_IF;

(* 2oo3 Median Voting & Bumpless Degradation *)
IF NOT bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    iTMR1_HealthGrade := 3;
    IF (rDrum_Temp_Pyrometer_A_degC >= rDrum_Temp_Pyrometer_B_degC AND rDrum_Temp_Pyrometer_A_degC <= rDrum_Temp_Pyrometer_C_degC) OR
       (rDrum_Temp_Pyrometer_A_degC >= rDrum_Temp_Pyrometer_C_degC AND rDrum_Temp_Pyrometer_A_degC <= rDrum_Temp_Pyrometer_B_degC) THEN
        rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_A_degC;
    ELSIF (rDrum_Temp_Pyrometer_B_degC >= rDrum_Temp_Pyrometer_A_degC AND rDrum_Temp_Pyrometer_B_degC <= rDrum_Temp_Pyrometer_C_degC) OR
          (rDrum_Temp_Pyrometer_B_degC >= rDrum_Temp_Pyrometer_C_degC AND rDrum_Temp_Pyrometer_B_degC <= rDrum_Temp_Pyrometer_A_degC) THEN
        rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_B_degC;
    ELSE
        rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_C_degC;
    END_IF;
ELSIF bTMR1_FaultA AND NOT bTMR1_FaultB AND NOT bTMR1_FaultC THEN
    iTMR1_HealthGrade := 2;
    rVoted_DrumExitTemp_degC := 0.5 * (rDrum_Temp_Pyrometer_B_degC + rDrum_Temp_Pyrometer_C_degC);
ELSIF bTMR1_FaultB AND NOT bTMR1_FaultA AND NOT bTMR1_FaultC THEN
    iTMR1_HealthGrade := 2;
    rVoted_DrumExitTemp_degC := 0.5 * (rDrum_Temp_Pyrometer_A_degC + rDrum_Temp_Pyrometer_C_degC);
ELSIF bTMR1_FaultC AND NOT bTMR1_FaultA AND NOT bTMR1_FaultB THEN
    iTMR1_HealthGrade := 2;
    rVoted_DrumExitTemp_degC := 0.5 * (rDrum_Temp_Pyrometer_A_degC + rDrum_Temp_Pyrometer_B_degC);
ELSIF NOT bTMR1_FaultA AND bTMR1_FaultB AND bTMR1_FaultC THEN
    iTMR1_HealthGrade := 1;
    rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_A_degC;
ELSIF NOT bTMR1_FaultB AND bTMR1_FaultA AND bTMR1_FaultC THEN
    iTMR1_HealthGrade := 1;
    rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_B_degC;
ELSIF NOT bTMR1_FaultC AND bTMR1_FaultA AND bTMR1_FaultB THEN
    iTMR1_HealthGrade := 1;
    rVoted_DrumExitTemp_degC := rDrum_Temp_Pyrometer_C_degC;
ELSE
    iTMR1_HealthGrade := 0;
    rVoted_DrumExitTemp_degC := rSP_Aggregate_ExitTemp_degC; (* Fail-safe default *)
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TMR 2: Pugmill Aggregate Weigh Hopper Load Cell Triad (A, B, C) [kg]
 * ------------------------------------------------------------------------------------------------------------------- *)
IF bWeighHopper_LC_A_Fault OR rWeighHopper_LoadCell_A_kg < -100.0 OR rWeighHopper_LoadCell_A_kg > 6000.0 THEN
    bTMR2_FaultA := TRUE;
ELSIF ABS(rWeighHopper_LoadCell_A_kg - rWeighHopper_LoadCell_B_kg) > c_rTMR2_DiscrepancyLimit_kg AND
      ABS(rWeighHopper_LoadCell_A_kg - rWeighHopper_LoadCell_C_kg) > c_rTMR2_DiscrepancyLimit_kg THEN
    tTMR2_TimerA := tTMR2_TimerA + rCycleTime_s;
    IF tTMR2_TimerA >= c_rTMR2_FaultDelay_s THEN
        bTMR2_FaultA := TRUE;
    END_IF;
ELSE
    tTMR2_TimerA := MAX(0.0, tTMR2_TimerA - (1.5 * rCycleTime_s));
END_IF;

IF bWeighHopper_LC_B_Fault OR rWeighHopper_LoadCell_B_kg < -100.0 OR rWeighHopper_LoadCell_B_kg > 6000.0 THEN
    bTMR2_FaultB := TRUE;
ELSIF ABS(rWeighHopper_LoadCell_B_kg - rWeighHopper_LoadCell_A_kg) > c_rTMR2_DiscrepancyLimit_kg AND
      ABS(rWeighHopper_LoadCell_B_kg - rWeighHopper_LoadCell_C_kg) > c_rTMR2_DiscrepancyLimit_kg THEN
    tTMR2_TimerB := tTMR2_TimerB + rCycleTime_s;
    IF tTMR2_TimerB >= c_rTMR2_FaultDelay_s THEN
        bTMR2_FaultB := TRUE;
    END_IF;
ELSE
    tTMR2_TimerB := MAX(0.0, tTMR2_TimerB - (1.5 * rCycleTime_s));
END_IF;

IF bWeighHopper_LC_C_Fault OR rWeighHopper_LoadCell_C_kg < -100.0 OR rWeighHopper_LoadCell_C_kg > 6000.0 THEN
    bTMR2_FaultC := TRUE;
ELSIF ABS(rWeighHopper_LoadCell_C_kg - rWeighHopper_LoadCell_A_kg) > c_rTMR2_DiscrepancyLimit_kg AND
      ABS(rWeighHopper_LoadCell_C_kg - rWeighHopper_LoadCell_B_kg) > c_rTMR2_DiscrepancyLimit_kg THEN
    tTMR2_TimerC := tTMR2_TimerC + rCycleTime_s;
    IF tTMR2_TimerC >= c_rTMR2_FaultDelay_s THEN
        bTMR2_FaultC := TRUE;
    END_IF;
ELSE
    tTMR2_TimerC := MAX(0.0, tTMR2_TimerC - (1.5 * rCycleTime_s));
END_IF;

IF NOT bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 3;
    IF (rWeighHopper_LoadCell_A_kg >= rWeighHopper_LoadCell_B_kg AND rWeighHopper_LoadCell_A_kg <= rWeighHopper_LoadCell_C_kg) OR
       (rWeighHopper_LoadCell_A_kg >= rWeighHopper_LoadCell_C_kg AND rWeighHopper_LoadCell_A_kg <= rWeighHopper_LoadCell_B_kg) THEN
        rVoted_WeighHopper_kg := rWeighHopper_LoadCell_A_kg;
    ELSIF (rWeighHopper_LoadCell_B_kg >= rWeighHopper_LoadCell_A_kg AND rWeighHopper_LoadCell_B_kg <= rWeighHopper_LoadCell_C_kg) OR
          (rWeighHopper_LoadCell_B_kg >= rWeighHopper_LoadCell_C_kg AND rWeighHopper_LoadCell_B_kg <= rWeighHopper_LoadCell_A_kg) THEN
        rVoted_WeighHopper_kg := rWeighHopper_LoadCell_B_kg;
    ELSE
        rVoted_WeighHopper_kg := rWeighHopper_LoadCell_C_kg;
    END_IF;
ELSIF bTMR2_FaultA AND NOT bTMR2_FaultB AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 2;
    rVoted_WeighHopper_kg := 0.5 * (rWeighHopper_LoadCell_B_kg + rWeighHopper_LoadCell_C_kg);
ELSIF bTMR2_FaultB AND NOT bTMR2_FaultA AND NOT bTMR2_FaultC THEN
    iTMR2_HealthGrade := 2;
    rVoted_WeighHopper_kg := 0.5 * (rWeighHopper_LoadCell_A_kg + rWeighHopper_LoadCell_C_kg);
ELSIF bTMR2_FaultC AND NOT bTMR2_FaultA AND NOT bTMR2_FaultB THEN
    iTMR2_HealthGrade := 2;
    rVoted_WeighHopper_kg := 0.5 * (rWeighHopper_LoadCell_A_kg + rWeighHopper_LoadCell_B_kg);
ELSIF NOT bTMR2_FaultA AND bTMR2_FaultB AND bTMR2_FaultC THEN
    iTMR2_HealthGrade := 1;
    rVoted_WeighHopper_kg := rWeighHopper_LoadCell_A_kg;
ELSIF NOT bTMR2_FaultB AND bTMR2_FaultA AND bTMR2_FaultC THEN
    iTMR2_HealthGrade := 1;
    rVoted_WeighHopper_kg := rWeighHopper_LoadCell_B_kg;
ELSIF NOT bTMR2_FaultC AND bTMR2_FaultA AND bTMR2_FaultB THEN
    iTMR2_HealthGrade := 1;
    rVoted_WeighHopper_kg := rWeighHopper_LoadCell_C_kg;
ELSE
    iTMR2_HealthGrade := 0;
    rVoted_WeighHopper_kg := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * TMR 3: Bitumen High-Pressure Coriolis Mass Flow Meters (A, B, C) [kg/s]
 * ------------------------------------------------------------------------------------------------------------------- *)
IF bBitumen_Flow_Coriolis_A_Fault OR rBitumen_Flow_Coriolis_A_kgs < -0.5 OR rBitumen_Flow_Coriolis_A_kgs > 30.0 THEN
    bTMR3_FaultA := TRUE;
ELSIF ABS(rBitumen_Flow_Coriolis_A_kgs - rBitumen_Flow_Coriolis_B_kgs) > c_rTMR3_DiscrepancyLimit_kgs AND
      ABS(rBitumen_Flow_Coriolis_A_kgs - rBitumen_Flow_Coriolis_C_kgs) > c_rTMR3_DiscrepancyLimit_kgs THEN
    tTMR3_TimerA := tTMR3_TimerA + rCycleTime_s;
    IF tTMR3_TimerA >= c_rTMR3_FaultDelay_s THEN
        bTMR3_FaultA := TRUE;
    END_IF;
ELSE
    tTMR3_TimerA := MAX(0.0, tTMR3_TimerA - (1.5 * rCycleTime_s));
END_IF;

IF bBitumen_Flow_Coriolis_B_Fault OR rBitumen_Flow_Coriolis_B_kgs < -0.5 OR rBitumen_Flow_Coriolis_B_kgs > 30.0 THEN
    bTMR3_FaultB := TRUE;
ELSIF ABS(rBitumen_Flow_Coriolis_B_kgs - rBitumen_Flow_Coriolis_A_kgs) > c_rTMR3_DiscrepancyLimit_kgs AND
      ABS(rBitumen_Flow_Coriolis_B_kgs - rBitumen_Flow_Coriolis_C_kgs) > c_rTMR3_DiscrepancyLimit_kgs THEN
    tTMR3_TimerB := tTMR3_TimerB + rCycleTime_s;
    IF tTMR3_TimerB >= c_rTMR3_FaultDelay_s THEN
        bTMR3_FaultB := TRUE;
    END_IF;
ELSE
    tTMR3_TimerB := MAX(0.0, tTMR3_TimerB - (1.5 * rCycleTime_s));
END_IF;

IF bBitumen_Flow_Coriolis_C_Fault OR rBitumen_Flow_Coriolis_C_kgs < -0.5 OR rBitumen_Flow_Coriolis_C_kgs > 30.0 THEN
    bTMR3_FaultC := TRUE;
ELSIF ABS(rBitumen_Flow_Coriolis_C_kgs - rBitumen_Flow_Coriolis_A_kgs) > c_rTMR3_DiscrepancyLimit_kgs AND
      ABS(rBitumen_Flow_Coriolis_C_kgs - rBitumen_Flow_Coriolis_B_kgs) > c_rTMR3_DiscrepancyLimit_kgs THEN
    tTMR3_TimerC := tTMR3_TimerC + rCycleTime_s;
    IF tTMR3_TimerC >= c_rTMR3_FaultDelay_s THEN
        bTMR3_FaultC := TRUE;
    END_IF;
ELSE
    tTMR3_TimerC := MAX(0.0, tTMR3_TimerC - (1.5 * rCycleTime_s));
END_IF;

IF NOT bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 3;
    IF (rBitumen_Flow_Coriolis_A_kgs >= rBitumen_Flow_Coriolis_B_kgs AND rBitumen_Flow_Coriolis_A_kgs <= rBitumen_Flow_Coriolis_C_kgs) OR
       (rBitumen_Flow_Coriolis_A_kgs >= rBitumen_Flow_Coriolis_C_kgs AND rBitumen_Flow_Coriolis_A_kgs <= rBitumen_Flow_Coriolis_B_kgs) THEN
        rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_A_kgs;
    ELSIF (rBitumen_Flow_Coriolis_B_kgs >= rBitumen_Flow_Coriolis_A_kgs AND rBitumen_Flow_Coriolis_B_kgs <= rBitumen_Flow_Coriolis_C_kgs) OR
          (rBitumen_Flow_Coriolis_B_kgs >= rBitumen_Flow_Coriolis_C_kgs AND rBitumen_Flow_Coriolis_B_kgs <= rBitumen_Flow_Coriolis_A_kgs) THEN
        rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_B_kgs;
    ELSE
        rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_C_kgs;
    END_IF;
ELSIF bTMR3_FaultA AND NOT bTMR3_FaultB AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 2;
    rVoted_BitumenFlow_kgs := 0.5 * (rBitumen_Flow_Coriolis_B_kgs + rBitumen_Flow_Coriolis_C_kgs);
ELSIF bTMR3_FaultB AND NOT bTMR3_FaultA AND NOT bTMR3_FaultC THEN
    iTMR3_HealthGrade := 2;
    rVoted_BitumenFlow_kgs := 0.5 * (rBitumen_Flow_Coriolis_A_kgs + rBitumen_Flow_Coriolis_C_kgs);
ELSIF bTMR3_FaultC AND NOT bTMR3_FaultA AND NOT bTMR3_FaultB THEN
    iTMR3_HealthGrade := 2;
    rVoted_BitumenFlow_kgs := 0.5 * (rBitumen_Flow_Coriolis_A_kgs + rBitumen_Flow_Coriolis_B_kgs);
ELSIF NOT bTMR3_FaultA AND bTMR3_FaultB AND bTMR3_FaultC THEN
    iTMR3_HealthGrade := 1;
    rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_A_kgs;
ELSIF NOT bTMR3_FaultB AND bTMR3_FaultA AND bTMR3_FaultC THEN
    iTMR3_HealthGrade := 1;
    rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_B_kgs;
ELSIF NOT bTMR3_FaultC AND bTMR3_FaultA AND bTMR3_FaultB THEN
    iTMR3_HealthGrade := 1;
    rVoted_BitumenFlow_kgs := rBitumen_Flow_Coriolis_C_kgs;
ELSE
    iTMR3_HealthGrade := 0;
    rVoted_BitumenFlow_kgs := 0.0;
END_IF;
""")

    # =========================================================================
    # 7. PHASE 2: CYBER-PHYSICAL OBSERVERS
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 2: CYBER-PHYSICAL OBSERVERS, THERMAL MASS BALANCES & ADAPTIVE COMPENSATION
 * =================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 1: Rotary Dryer Coupled Heat & Mass Balance Evaporation Observer
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Convert aggregate flow from tonnes/hour to kg/s and calculate moisture-compensated dry mass *)
rColdFeed_DryMassFlow_tph := rColdMasterBelt_Flow_tph / (1.0 + (rAggregate_Moisture_In_pct / 100.0));
rObs_AggregateMassFlow_kgs := (rColdFeed_DryMassFlow_tph * 1000.0) / 3600.0;

(* Water mass flow rate evaporated from aggregate moisture [kg/s] *)
rObs_WaterMassFlow_kgs := rObs_AggregateMassFlow_kgs * (rAggregate_Moisture_In_pct / 100.0);

(* Sensible heat to raise aggregate mineral stone from ambient to exit setpoint [kW] *)
rObs_EnthalpyStone_kW := rObs_AggregateMassFlow_kgs * c_rCp_Stone * (rSP_Aggregate_ExitTemp_degC - rAmbient_AirTemp_degC);

(* Thermal heat to raise moisture to 100 deg C, vaporize, and superheat steam to exit flue temp [kW] *)
rObs_EnthalpyWater_kW := rObs_WaterMassFlow_kgs * (
    (c_rCp_Water * (100.0 - rAmbient_AirTemp_degC)) +
    c_rDeltaH_Vap +
    (c_rCp_Steam * (rDrum_FlueGas_ExitTemp_degC - 100.0))
);

(* External rotary drum steel shell surface radiative and natural convective losses [kW] *)
rObs_ShellLossRadiation_kW := (
    (c_rStefanBoltzmann * 0.85 * 3.14159 * 3.0 * 12.0 *
     (EXPT(rDrum_Shell_Temp_degC + 273.15, 4.0) - EXPT(rAmbient_AirTemp_degC + 273.15, 4.0))) +
    (15.2 * 3.14159 * 3.0 * 12.0 * (rDrum_Shell_Temp_degC - rAmbient_AirTemp_degC))
) / 1000.0;

(* Total theoretical thermal duty in kW considering shell loss and thermal efficiency *)
rObs_TotalThermalPowerReq_kW := (rObs_EnthalpyStone_kW + rObs_EnthalpyWater_kW + rObs_ShellLossRadiation_kW) / (rObs_ThermalEfficiency_pct / 100.0);

(* Theoretical Burner Firing Rate percentage (assuming 24 MW burner maximum capacity) *)
rObs_BurnerFiringRate_Theoretical_pct := LIMIT(0.0, (rObs_TotalThermalPowerReq_kW / 24000.0) * 100.0, 100.0);

(* Calculated instantaneous fuel mass consumption rate [kg/h] *)
rCalculated_FuelRate_kgh := (rObs_TotalThermalPowerReq_kW * 3600.0) / (c_rFuelNetCalorific_MJkg * 1000.0);

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 2: Aggregate Bed Flighting Curtain & Radiative Heat Transfer Observer
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Cascading mineral stone curtain volumetric density inside rotary drum [kg/m3] *)
rObs_DrumCurtainDensity_kgm3 := LIMIT(5.0, (rObs_AggregateMassFlow_kgs * 18.0) / (3.14159 * 1.5 * 1.5 * 12.0), 85.0);

(* Estimate flame core temperature based on burner firing rate and excess air *)
rObs_FlameTemp_Estimated_degC := 1150.0 + (rBurner_FuelValve_Demand_pct * 4.5) - (rExhaust_Gas_O2_pct * 25.0);

(* Radiative heat flux from flame core to stone curtain [kW/m2] *)
rObs_RadiationHeatFlux_kWm2 := (c_rStefanBoltzmann * 0.88 *
    (EXPT(rObs_FlameTemp_Estimated_degC + 273.15, 4.0) - EXPT(rVoted_DrumExitTemp_degC + 273.15, 4.0))) / 1000.0;

(* Counterflow Logarithmic Mean Temperature Difference LMTD [K] *)
rObs_LMTD_Counterflow_K := (
    (rObs_FlameTemp_Estimated_degC - rVoted_DrumExitTemp_degC) -
    (rDrum_FlueGas_ExitTemp_degC - rAmbient_AirTemp_degC)
) / MAX(0.05, LN(MAX(1.05, (rObs_FlameTemp_Estimated_degC - rVoted_DrumExitTemp_degC) /
                            MAX(1.0, rDrum_FlueGas_ExitTemp_degC - rAmbient_AirTemp_degC))));

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 3: Baghouse Filter Cake Resistance & Darcy-Ergun Observer
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Flue gas volumetric face velocity [m/s] *)
rObs_FilterFaceVelocity_ms := LIMIT(0.01, (rExhaust_Fan_Current_A / 320.0) * (rExhaust_IDFan_Damper_pct / 100.0) * 1.85, 2.50);

(* Estimate particulate cake accumulation on fabric based on aggregate throughput and dust fraction *)
IF iPlantState = c_ST_DRUM_DRYING_BURNER_MOD THEN
    rObs_DustCakeMass_kg := rObs_DustCakeMass_kg + (rObs_AggregateMassFlow_kgs * 0.0035 * rCycleTime_s);
END_IF;

(* Darcy flow pressure drop across fabric and porous dust cake [mbar] *)
rObs_CalculatedDeltaP_mbar := (
    (1.25E-5 * rObs_FilterFaceVelocity_ms / rObs_DarcyPermeability) +
    (rObs_CakeSpecificResistance * (rObs_DustCakeMass_kg / 850.0) * rObs_FilterFaceVelocity_ms)
) * 0.00001;
rBaghouse_ResidualResistance := (rBaghouse_DeltaP_mbar * 100.0) / MAX(0.001, rObs_FilterFaceVelocity_ms);

(* Acid Dew Point Observer (Verhoff-Banchero correlation for SO3/H2O condensation) *)
rObs_FlueGas_AcidDewPoint_degC := 100.0 + (15.5 * LN(MAX(0.01, rObs_WaterMassFlow_kgs))) + (8.2 * LN(MAX(0.001, rDrum_Burner_FuelPressure_bar * 0.02)));

(* Pulse-Jet Periodic Cleaning Cycle Execution *)
tPulseJet_Timer := tPulseJet_Timer + rCycleTime_s;
IF rBaghouse_DeltaP_mbar > 15.0 THEN
    rPulseJet_Interval_s := 8.0; (* Accelerate pulsing under heavy differential pressure *)
ELSE
    rPulseJet_Interval_s := 16.0;
END_IF;

IF tPulseJet_Timer >= rPulseJet_Interval_s THEN
    bBaghouse_PulseValve_Fire := TRUE;
    iBaghouse_ActiveRow := iBaghouse_ActiveRow + 1;
    IF iBaghouse_ActiveRow > 16 THEN
        iBaghouse_ActiveRow := 1;
    END_IF;
    (* Pulse-jet dislodges particulate cake, reducing accumulated mass *)
    rObs_DustCakeMass_kg := MAX(25.0, rObs_DustCakeMass_kg - 18.5);
    tPulseJet_Timer := 0.0;
ELSE
    bBaghouse_PulseValve_Fire := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 4: Bitumen Walther-Andrade Non-Newtonian Dynamic Viscosity Observer
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Walther ASTM D341 empirical formulation: log(log(nu + 0.7)) = A - B * log(T_K) *)
rObs_WaltherLogTerm := 10.54 - (3.82 * LN(MAX(1.0, rBitumen_StorageTank_Temp_degC + 273.15)));
rObs_BitumenKinematicViscosity_cSt := LIMIT(25.0, EXP(EXP(LIMIT(-1.0, rObs_WaltherLogTerm, 3.5))) - 0.7, 4500.0);

(* Dynamic Viscosity mu = nu * density [cP] *)
rObs_BitumenDynamicViscosity_cP := rObs_BitumenKinematicViscosity_cSt * (MAX(900.0, rBitumen_Density_kgm3) / 1000.0);
rBitumen_Viscosity_Feedback_cP := rObs_BitumenDynamicViscosity_cP;

(* Dimensionless Spray Quality Index (Target 1.0 at ideal injection viscosity 150 cP, range 150-170 deg C) *)
rObs_ViscositySprayIndex := LIMIT(0.2, 150.0 / MAX(10.0, rObs_BitumenDynamicViscosity_cP), 2.5);

(* Sauter Mean Diameter SMD of atomized bitumen droplet spray [um] *)
rObs_SauterMeanDiameter_um := LIMIT(45.0, 185.0 * EXPT(MAX(1.0, rBitumen_Spray_Pressure_bar), -0.42) * EXPT(rObs_BitumenDynamicViscosity_cP / 150.0, 0.28), 650.0);

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 5: Twin-Shaft Pugmill Dynamic Mixing Work & Homogeneity Coating Observer
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Dual synchronous shafts rotating at nominal 54 rpm (5.655 rad/s) at 50 Hz *)
rObs_PugmillAngularVelocity_rads := (rPugmill_Drive_Speed_Hz / 50.0) * 5.65487;

(* Net mechanical power transmitted to asphalt mixture [kW] *)
rObs_PugmillMechanicalPower_kW := (rPugmill_Drive_Torque_Nm * rObs_PugmillAngularVelocity_rads) / 1000.0;

(* Torque derivative d(tau)/dt [Nm/s] *)
rObs_TorqueRateOfChange_Nms := (rPugmill_Drive_Torque_Nm - rPrev_PugmillTorque_Nm) / rCycleTime_s;
rPrev_PugmillTorque_Nm := rPugmill_Drive_Torque_Nm;

(* Integrate cumulative mixing shear work during wet mixing phase *)
IF iPlantState = c_ST_TWINSHAFT_WET_MIX THEN
    rObs_CumulativeMixEnergy_kJ := rObs_CumulativeMixEnergy_kJ + (rObs_PugmillMechanicalPower_kW * rCycleTime_s);
    (* Homogeneity index approaches 1.0 asymptotically as shear energy reaches 850 kJ for 4,000 kg batch *)
    rObs_AsphaltHomogeneityIndex := LIMIT(0.0, 1.0 - EXP(-rObs_CumulativeMixEnergy_kJ / 320.0), 1.0);
ELSE
    IF iPlantState = c_ST_PUGMILL_DISCHARGE_GATE THEN
        (* Preserve index during discharge *)
    ELSE
        rObs_CumulativeMixEnergy_kJ := 0.0;
        rObs_AsphaltHomogeneityIndex := 0.0;
    END_IF;
END_IF;

rPugmill_Homogeneity_Index := rObs_AsphaltHomogeneityIndex;
rPugmill_SpecificEnergy_kWht := rObs_CumulativeMixEnergy_kJ / (3600.0 * MAX(0.5, rSP_BatchSize_kg / 1000.0));

(* Bucket Elevator Slip Ratio *)
IF rHotElevator_Run_Cmd THEN
    rElevator_SlipPercentage := LIMIT(0.0, ((65.0 - rHotElevator_Speed_rpm) / 65.0) * 100.0, 100.0);
ELSE
    rElevator_SlipPercentage := 0.0;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * Observer 6: Skip Hoist 7-Segment Jerk-Limited S-Curve Kinematic Trajectory Generator
 * ------------------------------------------------------------------------------------------------------------------- *)
(* Select target elevation based on active silo compartment (Bay 1=12m, Bay 2=18m, Bay 3=24m, Bay 4=30m) *)
CASE iSelectedSilo_Bay OF
    1: rSkip_TargetPos_m := 12.0;
    2: rSkip_TargetPos_m := 18.0;
    3: rSkip_TargetPos_m := 24.0;
    4: rSkip_TargetPos_m := 30.0;
ELSE
    rSkip_TargetPos_m := 12.0;
END_CASE;

IF iPlantState = c_ST_SKIP_HOIST_TRANSIT THEN
    tSkip_SegmentTimer := tSkip_SegmentTimer + rCycleTime_s;
    (* S-Curve Phase 1: Jerk ramp-up to max acceleration *)
    IF rTraj_PosCmd_m < (rSkip_TargetPos_m * 0.15) THEN
        rTraj_AccCmd_ms2 := MIN(c_rSkip_MaxAcc_ms2, rTraj_AccCmd_ms2 + (c_rSkip_MaxJerk_ms3 * rCycleTime_s));
        rTraj_VelCmd_ms := MIN(c_rSkip_MaxVel_ms, rTraj_VelCmd_ms + (rTraj_AccCmd_ms2 * rCycleTime_s));
    (* S-Curve Phase 2: Constant cruising velocity *)
    ELSIF rTraj_PosCmd_m >= (rSkip_TargetPos_m * 0.15) AND rTraj_PosCmd_m < (rSkip_TargetPos_m * 0.80) THEN
        rTraj_AccCmd_ms2 := 0.0;
        rTraj_VelCmd_ms := c_rSkip_MaxVel_ms;
    (* S-Curve Phase 3: Deceleration and soft creep positioning *)
    ELSIF rTraj_PosCmd_m >= (rSkip_TargetPos_m * 0.80) AND rTraj_PosCmd_m < rSkip_TargetPos_m THEN
        rTraj_AccCmd_ms2 := -c_rSkip_MaxAcc_ms2;
        rTraj_VelCmd_ms := MAX(0.20, rTraj_VelCmd_ms + (rTraj_AccCmd_ms2 * rCycleTime_s));
    ELSE
        rTraj_AccCmd_ms2 := 0.0;
        rTraj_VelCmd_ms := 0.0;
    END_IF;
    rTraj_PosCmd_m := rTraj_PosCmd_m + (rTraj_VelCmd_ms * rCycleTime_s);
    rSkipHoist_InstantaneousPower_kW := (rSkipHoist_RopeTension_kN * rTraj_VelCmd_ms);
ELSE
    IF bSkipHoist_Bottom_LS THEN
        rTraj_PosCmd_m := 0.0;
        rTraj_VelCmd_ms := 0.0;
        rTraj_AccCmd_ms2 := 0.0;
        tSkip_SegmentTimer := 0.0;
        rSkipHoist_InstantaneousPower_kW := 0.0;
    END_IF;
END_IF;
""")

    # =========================================================================
    # 8. PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC)
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 3: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) & PROJECTED GRADIENT DESCENT
 * =================================================================================================================== *)

(* Construct Normalized Dynamic State Error Vector x[1..8] *)
arrX_state[1] := rDrum_Shell_Temp_degC - 165.0;
arrX_state[2] := rDrum_FlueGas_ExitTemp_degC - 180.0;
arrX_state[3] := rObs_WaterMassFlow_kgs - 3.80;
arrX_state[4] := (rHotElevator_MotorPower_kW / 90.0) * 100.0 - 75.0;
arrX_state[5] := rBaghouse_DeltaP_mbar - 12.0;
arrX_state[6] := rBitumen_ThermalOilJacket_degC - 165.0;
arrX_state[7] := rPugmill_Drive_Torque_Nm - 4800.0;
arrX_state[8] := rSkipHoist_Velocity_ms - rTraj_VelCmd_ms;

(* Target Reference State Vector *)
FOR kStateIdx := 1 TO 8 DO
    arrX_ref[kStateIdx] := 0.0;
END_FOR;

(* Projected Gradient Descent (PGD) Iterative Receding Horizon Solver (3 Iterations per 0.1 s Cycle) *)
FOR iterMPC := 1 TO 3 DO
    (* 1. Propagate 1-Step Predictive State Vector: x_pred = A * x + B * u *)
    FOR iMatRow := 1 TO 8 DO
        rTempSum := 0.0;
        FOR iMatCol := 1 TO 8 DO
            rTempSum := rTempSum + (arrA[iMatRow, iMatCol] * arrX_state[iMatCol]);
        END_FOR;
        FOR mInIdx := 1 TO 6 DO
            rTempSum := rTempSum + (arrB[iMatRow, mInIdx] * arrU_control[mInIdx]);
        END_FOR;
        arrX_pred[iMatRow] := rTempSum;
    END_FOR;

    (* 2. Evaluate Analytical Gradient dJ/du across all 6 Actuators *)
    FOR mInIdx := 1 TO 6 DO
        rTempGrad := 0.0;
        (* State tracking & terminal cost sensitivity: 2 * sum((Q + P) * (x_pred - x_ref) * B) *)
        FOR iMatRow := 1 TO 8 DO
            rTempGrad := rTempGrad + (2.0 * (arrQ_Weight[iMatRow] + arrP_TerminalWeight[iMatRow]) *
                                      (arrX_pred[iMatRow] - arrX_ref[iMatRow]) * arrB[iMatRow, mInIdx]);
        END_FOR;
        (* Control effort quadratic regularization: 2 * R * u *)
        rTempGrad := rTempGrad + (2.0 * arrR_Weight[mInIdx] * arrU_control[mInIdx]);
        (* Control slew rate penalty: 2 * S * (u - u_prev) *)
        rTempGrad := rTempGrad + (2.0 * arrS_Weight[mInIdx] * (arrU_control[mInIdx] - arrU_prev[mInIdx]));
        arrGrad_u[mInIdx] := rTempGrad;

        (* 3. Update Actuator Control via Gradient Step *)
        arrU_control[mInIdx] := arrU_control[mInIdx] - (c_rMPC_Alpha * arrGrad_u[mInIdx]);

        (* 4. Enforce Physical Actuator Saturation Constraints *)
        CASE mInIdx OF
            1: arrU_control[1] := LIMIT(15.0, arrU_control[1], 100.0); (* Burner Fuel Valve Demand [%] *)
            2: arrU_control[2] := LIMIT(20.0, arrU_control[2], 55.0);  (* Burner Comb Air Fan [Hz] *)
            3: arrU_control[3] := LIMIT(0.0, arrU_control[3], 320.0);  (* Cold Master Feed Rate [t/h] *)
            4: arrU_control[4] := LIMIT(25.0, arrU_control[4], 100.0); (* ID Fan Damper [%] *)
            5: arrU_control[5] := LIMIT(0.0, arrU_control[5], 100.0);  (* Thermal Oil Valve [%] *)
            6: arrU_control[6] := LIMIT(0.0, arrU_control[6], 55.0);   (* Pugmill Inverter [Hz] *)
        END_CASE;
    END_FOR;
END_FOR;

(* Calculate Diagnostic Quadratic Cost J *)
rMPC_Cost_State := 0.0;
rMPC_Cost_Terminal := 0.0;
FOR iMatRow := 1 TO 8 DO
    rMPC_Cost_State := rMPC_Cost_State + (arrQ_Weight[iMatRow] * EXPT(arrX_pred[iMatRow] - arrX_ref[iMatRow], 2.0));
    rMPC_Cost_Terminal := rMPC_Cost_Terminal + (arrP_TerminalWeight[iMatRow] * EXPT(arrX_pred[iMatRow] - arrX_ref[iMatRow], 2.0));
END_FOR;

rMPC_Cost_Control := 0.0;
rMPC_Cost_Slew := 0.0;
FOR mInIdx := 1 TO 6 DO
    rMPC_Cost_Control := rMPC_Cost_Control + (arrR_Weight[mInIdx] * EXPT(arrU_control[mInIdx], 2.0));
    rMPC_Cost_Slew := rMPC_Cost_Slew + (arrS_Weight[mInIdx] * EXPT(arrU_control[mInIdx] - arrU_prev[mInIdx], 2.0));
END_FOR;
rMPC_Cost_Total := rMPC_Cost_State + rMPC_Cost_Control + rMPC_Cost_Slew + rMPC_Cost_Terminal;

(* Store control action for slew rate penalization in next scan *)
FOR mInIdx := 1 TO 6 DO
    arrU_delta[mInIdx] := arrU_control[mInIdx] - arrU_prev[mInIdx];
    arrU_prev[mInIdx] := arrU_control[mInIdx];
END_FOR;

(* Simulated Output Vector y = C * x + D * u *)
FOR iMatRow := 1 TO 8 DO
    rTempSum := 0.0;
    FOR iMatCol := 1 TO 8 DO
        rTempSum := rTempSum + (arrC[iMatRow, iMatCol] * arrX_pred[iMatCol]);
    END_FOR;
    arrY_output[iMatRow] := rTempSum;
END_FOR;
""")

    # =========================================================================
    # 9. PHASE 4: 12-STAGE FINITE STATE MACHINE (FSM)
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 4: 12-STAGE DETERMINISTIC OPERATIONAL FINITE STATE MACHINE (FSM)
 * =================================================================================================================== *)

(* Advance State Elapsed Timer *)
tStateTimer_s := tStateTimer_s + rCycleTime_s;

CASE iPlantState OF

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 10: PLANT PRE-PURGE / IGNITION STANDBY
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_PREPURGE_IGNITION:
        bPlantReady := FALSE;
        bPlantRunning := FALSE;
        rBatchCycleProgress_pct := 0.0;
        bHotElevator_Run_Cmd := TRUE; (* Clear bucket elevator before feeding *)
        bScreen_Drive_Run_Cmd := TRUE; (* Run vibrating screen *)
        rDrum_Drive_Speed_rpm := 6.5; (* Rotary dryer trunnions rotating *)
        rExhaust_IDFan_Damper_pct := 80.0; (* Prepurge drum and baghouse of unburnt hydrocarbons *)

        IF tStateTimer_s < 20.0 THEN
            bBurner_PilotGas_Solenoid := FALSE;
            bBurner_Ignition_Spark := FALSE;
            rBurner_FuelValve_Demand_pct := 0.0;
            rBurner_CombAir_VFD_Hz := 45.0;
        ELSIF tStateTimer_s >= 20.0 AND tStateTimer_s < 30.0 THEN
            (* Pilot Ignition Spark Request *)
            bBurner_PilotGas_Solenoid := TRUE;
            bBurner_Ignition_Spark := TRUE;
            rBurner_CombAir_VFD_Hz := 25.0;
        ELSIF tStateTimer_s >= 30.0 AND tStateTimer_s < 45.0 THEN
            bBurner_Ignition_Spark := FALSE;
            IF rDrum_Burner_FlameIntensity_pct > 65.0 THEN
                (* Main Flame Established at Low Fire *)
                rBurner_FuelValve_Demand_pct := 22.0;
                bPlantReady := TRUE;
            END_IF;
        ELSE
            IF bStartCycle AND bPlantReady AND NOT bMasterPlantTrip THEN
                iPreviousState := iPlantState;
                iPlantState := c_ST_COLD_FEED_PROPORTION;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 20: COLD AGGREGATE PROPORTIONING FEED
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_COLD_FEED_PROPORTION:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 10.0;
        (* Distribute Cold Feed Speeds based on Recipe Proportions *)
        FOR iBinIdx := 1 TO 6 DO
            arrColdBin_BeltSpeed_Cmd[iBinIdx] := (rSP_TotalPlantThroughput_tph / 320.0) * arrRecipe_AggPercent[iBinIdx];
        END_FOR;
        rColdMasterBelt_Speed_Cmd := LIMIT(20.0, (rSP_TotalPlantThroughput_tph / 320.0) * 100.0, 100.0);

        IF rColdMasterBelt_Flow_tph >= (rSP_TotalPlantThroughput_tph * 0.85) OR tStateTimer_s > 15.0 THEN
            iPreviousState := iPlantState;
            iPlantState := c_ST_DRUM_DRYING_BURNER_MOD;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 30: ROTARY DRUM DRYING & BURNER MODULATION
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_DRUM_DRYING_BURNER_MOD:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 25.0;
        (* Closed-loop Burner Fuel & Air Modulation via MPC output + Feedforward duty *)
        rBurner_FuelValve_Demand_pct := LIMIT(20.0, arrU_control[1] + (rObs_BurnerFiringRate_Theoretical_pct * 0.35), 98.0);
        rBurner_CombAir_VFD_Hz := LIMIT(22.0, arrU_control[2] + (rBurner_FuelValve_Demand_pct * 0.32), 52.0);
        rExhaust_IDFan_Damper_pct := LIMIT(35.0, arrU_control[4], 95.0);
        rBurner_AirFuel_Ratio := (rBurner_CombAir_VFD_Hz / 50.0 * 22000.0) / MAX(1.0, rCalculated_FuelRate_kgh * 14.2);

        (* Verify Aggregate Reaches Desired Drying Temperature *)
        IF rVoted_DrumExitTemp_degC >= (rSP_Aggregate_ExitTemp_degC - 5.0) AND tStateTimer_s > 25.0 THEN
            iPreviousState := iPlantState;
            iPlantState := c_ST_HOT_SCREEN_BIN_STORAGE;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 40: HOT SCREENING & INSULATED BIN STORAGE
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_HOT_SCREEN_BIN_STORAGE:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 35.0;
        bHotElevator_Run_Cmd := TRUE;
        bScreen_Drive_Run_Cmd := TRUE;

        (* Check hot bin storage levels before batching *)
        IF arrHotBin_Level_pct[1] > 20.0 AND arrHotBin_Level_pct[2] > 20.0 AND arrHotBin_Level_pct[3] > 20.0 THEN
            iActiveDosingBin := 1;
            rBatchAgg_Accumulated_kg := 0.0;
            iPreviousState := iPlantState;
            iPlantState := c_ST_AGG_WEIGH_HOPPER_DOSING;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 50: AGGREGATES WEIGH HOPPER GRAVIMETRIC DOSING (BINS 1 TO 6 SEQUENTIAL)
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_AGG_WEIGH_HOPPER_DOSING:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 45.0;

        (* Calculate Target Cumulative Weight for Active Bin *)
        rDosingBin_TargetWeight_kg := rBatchAgg_Accumulated_kg + (rSP_BatchSize_kg * (arrRecipe_AggPercent[iActiveDosingBin] / 100.0));
        rDosingBin_CutoffWeight_kg := rDosingBin_TargetWeight_kg - arrInflightComp_Agg_kg[iActiveDosingBin];

        (* Coarse & Fine Feed Gate Actuation with In-Flight Drop Compensation *)
        IF rVoted_WeighHopper_kg < (rDosingBin_CutoffWeight_kg - 50.0) THEN
            arrHotBin_Gate_Coarse_Cmd[iActiveDosingBin] := TRUE;
            arrHotBin_Gate_Fine_Cmd[iActiveDosingBin] := TRUE;
        ELSIF rVoted_WeighHopper_kg >= (rDosingBin_CutoffWeight_kg - 50.0) AND rVoted_WeighHopper_kg < rDosingBin_CutoffWeight_kg THEN
            arrHotBin_Gate_Coarse_Cmd[iActiveDosingBin] := FALSE;
            arrHotBin_Gate_Fine_Cmd[iActiveDosingBin] := TRUE; (* Fine dribble feed *)
        ELSE
            arrHotBin_Gate_Coarse_Cmd[iActiveDosingBin] := FALSE;
            arrHotBin_Gate_Fine_Cmd[iActiveDosingBin] := FALSE;

            (* Update Adaptive In-Flight Material Fall Model *)
            arrInflightComp_Agg_kg[iActiveDosingBin] := arrInflightComp_Agg_kg[iActiveDosingBin] +
                c_rInflight_Alpha * ((rVoted_WeighHopper_kg - rDosingBin_CutoffWeight_kg) - arrInflightComp_Agg_kg[iActiveDosingBin]);

            rBatchAgg_Accumulated_kg := rVoted_WeighHopper_kg;
            iActiveDosingBin := iActiveDosingBin + 1;

            IF iActiveDosingBin > 6 THEN
                iPreviousState := iPlantState;
                iPlantState := c_ST_FILLER_DUST_ADDITION;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 60: FILLER / MINERAL DUST GRAVIMETRIC ADDITION
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_FILLER_DUST_ADDITION:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 55.0;
        bFiller_BlowpadFluidize_Cmd := TRUE;

        (* Target Filler Mass (e.g., 5% of 4000 kg = 200 kg) *)
        IF rFillerScale_Weight_kg < ((rSP_BatchSize_kg * (rRecipe_FillerPercent / 100.0)) - rInflightComp_Filler_kg) THEN
            bFiller_DosingScrew_Run_Cmd := TRUE;
        ELSE
            bFiller_DosingScrew_Run_Cmd := FALSE;
            bFiller_BlowpadFluidize_Cmd := FALSE;
            rBatchFiller_Accumulated_kg := rFillerScale_Weight_kg;
            iPreviousState := iPlantState;
            iPlantState := c_ST_BITUMEN_PRESSURIZED_INJECTION;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 70: BITUMEN HIGH-PRESSURE METERED INJECTION
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_BITUMEN_PRESSURIZED_INJECTION:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 65.0;

        (* Transfer Dry Aggregates & Filler into Pugmill *)
        bWeighHopper_DischargeGate_Cmd := TRUE;
        rPugmill_Drive_Speed_Hz := 50.0;

        (* Calculate Bitumen Batch Mass Demand (e.g., 5.2% of 4000 kg = 208 kg) *)
        IF rBitumen_InjectedTotal_kg < ((rSP_BatchSize_kg * (rRecipe_BitumenPercent / 100.0)) - rInflightComp_Bitumen_kg) THEN
            rBitumen_Pump_Speed_Cmd_pct := 85.0 * rObs_ViscositySprayIndex;
            bBitumen_SprayBar_Valve_Cmd := TRUE;
            bBitumen_Recirc_Valve_Cmd := FALSE;
            rBitumen_InjectedTotal_kg := rBitumen_InjectedTotal_kg + (rVoted_BitumenFlow_kgs * rCycleTime_s);
        ELSE
            rBitumen_Pump_Speed_Cmd_pct := 25.0;
            bBitumen_SprayBar_Valve_Cmd := FALSE;
            bBitumen_Recirc_Valve_Cmd := TRUE; (* Recirculate heated bitumen in loop *)
            bWeighHopper_DischargeGate_Cmd := FALSE;
            rBatchBitumen_Accumulated_kg := rBitumen_InjectedTotal_kg;
            tWetMix_Timer_s := 0.0;
            iPreviousState := iPlantState;
            iPlantState := c_ST_TWINSHAFT_WET_MIX;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 80: TWIN-SHAFT WET MIXING CYCLE
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_TWINSHAFT_WET_MIX:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 75.0;
        rPugmill_Drive_Speed_Hz := 52.0;
        tWetMix_Timer_s := tWetMix_Timer_s + rCycleTime_s;

        (* Wet mix continues until recipe time elapsed and homogeneity coating index exceeds 0.95 *)
        IF tWetMix_Timer_s >= rRecipe_WetMixTime_s AND rObs_AsphaltHomogeneityIndex >= 0.92 THEN
            bPugmill_Discharge_Open_Cmd := TRUE;
            tDischarge_Timer_s := 0.0;
            iPreviousState := iPlantState;
            iPlantState := c_ST_PUGMILL_DISCHARGE_GATE;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 90: PUGMILL DISCHARGE GATE OPERATION
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_PUGMILL_DISCHARGE_GATE:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 85.0;
        bPugmill_Discharge_Open_Cmd := TRUE;
        tDischarge_Timer_s := tDischarge_Timer_s + rCycleTime_s;

        (* Pugmill empty verification via torque drop and timer *)
        IF tDischarge_Timer_s >= 8.0 AND rPugmill_Drive_Torque_Nm < 2500.0 THEN
            bPugmill_Discharge_Open_Cmd := FALSE;
            rBitumen_InjectedTotal_kg := 0.0;
            iActiveBatchNumber := iActiveBatchNumber + 1;
            rTotalProductionMass_tonnes := rTotalProductionMass_tonnes + (rSP_BatchSize_kg / 1000.0);
            iPreviousState := iPlantState;
            iPlantState := c_ST_SKIP_HOIST_TRANSIT;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 100: SKIP HOIST TRANSIT TO STORAGE SILO
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_SKIP_HOIST_TRANSIT:
        bPlantRunning := TRUE;
        rBatchCycleProgress_pct := 95.0;
        bSkipHoist_Brake_Release_Cmd := TRUE;
        rSkipHoist_Drive_Speed_Cmd_pct := (rTraj_VelCmd_ms / c_rSkip_MaxVel_ms) * 100.0;

        (* Top limit reached: discharge asphalt into designated heated storage compartment *)
        IF bSkipHoist_Top_LS OR rSkipHoist_Position_m >= (rSkip_TargetPos_m - 0.2) THEN
            bSkipHoist_DischargeFlap_Cmd := TRUE;
            IF tStateTimer_s > 12.0 THEN
                bSkipHoist_DischargeFlap_Cmd := FALSE;
                IF bStopCycle THEN
                    iPreviousState := iPlantState;
                    iPlantState := c_ST_POST_COOLING_PURGE;
                ELSE
                    iPreviousState := iPlantState;
                    iPlantState := c_ST_COLD_FEED_PROPORTION; (* Cycle to next batch *)
                END_IF;
                tStateTimer_s := 0.0;
            END_IF;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 110: BATCH RECIPE CHANGEOVER
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_RECIPE_CHANGEOVER:
        bPlantRunning := FALSE;
        rBatchCycleProgress_pct := 0.0;
        rBurner_FuelValve_Demand_pct := 20.0;
        rColdMasterBelt_Speed_Cmd := 0.0;
        FOR iBinIdx := 1 TO 6 DO
            arrColdBin_BeltSpeed_Cmd[iBinIdx] := 0.0;
        END_FOR;

        IF tStateTimer_s > 5.0 THEN
            iPreviousState := iPlantState;
            iPlantState := c_ST_COLD_FEED_PROPORTION;
            tStateTimer_s := 0.0;
        END_IF;

    (* ---------------------------------------------------------------------------------------------------------------
     * STAGE 120: CONTROLLED BURNER POST-COOLING PURGE
     * --------------------------------------------------------------------------------------------------------------- *)
    c_ST_POST_COOLING_PURGE:
        bPlantRunning := FALSE;
        rBatchCycleProgress_pct := 100.0;
        rBurner_FuelValve_Demand_pct := 0.0;
        bBurner_PilotGas_Solenoid := FALSE;
        bBurner_Ignition_Spark := FALSE;
        rBurner_CombAir_VFD_Hz := 35.0; (* Forced cooling air *)
        rExhaust_IDFan_Damper_pct := 50.0;
        rDrum_Drive_Speed_rpm := 3.5; (* Slow rotation to avoid thermal warping of drum shell *)

        IF rDrum_Shell_Temp_degC < 85.0 OR tStateTimer_s > 300.0 THEN
            rDrum_Drive_Speed_rpm := 0.0;
            rBurner_CombAir_VFD_Hz := 0.0;
            rExhaust_IDFan_Damper_pct := 0.0;
            bHotElevator_Run_Cmd := FALSE;
            bScreen_Drive_Run_Cmd := FALSE;
            iPreviousState := iPlantState;
            iPlantState := c_ST_PREPURGE_IGNITION;
            tStateTimer_s := 0.0;
        END_IF;

ELSE
    iPlantState := c_ST_PREPURGE_IGNITION;
    tStateTimer_s := 0.0;
END_CASE;

iPlantState_Out := iPlantState;
""")

    # =========================================================================
    # 10. PHASE 5: ISA-18.2 MULTI-TIERED ALARMS & BIT PACKING
    # =========================================================================
    parts.append("""(* ===================================================================================================================
 * PHASE 5: ISA-18.2 MULTI-TIERED ALARM ENGINE & DIAGNOSTIC WORD BIT-PACKING
 * =================================================================================================================== *)

(* Calculate Rates of Change (RoC) *)
rRateOfChange_DrumExitTemp := (rVoted_DrumExitTemp_degC - rPrev_DrumExitTemp_degC) / rCycleTime_s;
rPrev_DrumExitTemp_degC := rVoted_DrumExitTemp_degC;

rRateOfChange_BaghouseDeltaP := (rBaghouse_DeltaP_mbar - rPrev_BaghouseDeltaP_mbar) / rCycleTime_s;
rPrev_BaghouseDeltaP_mbar := rBaghouse_DeltaP_mbar;

(* -------------------------------------------------------------------------------------------------------------------
 * Rotary Dryer Temperature Alarms (HH, H, L, LL, RoC) with Positive/Negative Hysteresis
 * ------------------------------------------------------------------------------------------------------------------- *)
IF rVoted_DrumExitTemp_degC >= c_rDrumExitTemp_HH_degC THEN
    bAlarm_DrumTemp_HH := TRUE;
ELSIF rVoted_DrumExitTemp_degC <= (c_rDrumExitTemp_HH_degC - c_rDrumExitTemp_Deadband) THEN
    bAlarm_DrumTemp_HH := FALSE;
END_IF;

IF rVoted_DrumExitTemp_degC >= c_rDrumExitTemp_H_degC THEN
    bAlarm_DrumTemp_H := TRUE;
ELSIF rVoted_DrumExitTemp_degC <= (c_rDrumExitTemp_H_degC - c_rDrumExitTemp_Deadband) THEN
    bAlarm_DrumTemp_H := FALSE;
END_IF;

IF rVoted_DrumExitTemp_degC <= c_rDrumExitTemp_LL_degC THEN
    bAlarm_DrumTemp_LL := TRUE;
ELSIF rVoted_DrumExitTemp_degC >= (c_rDrumExitTemp_LL_degC + c_rDrumExitTemp_Deadband) THEN
    bAlarm_DrumTemp_LL := FALSE;
END_IF;

IF rVoted_DrumExitTemp_degC <= c_rDrumExitTemp_L_degC THEN
    bAlarm_DrumTemp_L := TRUE;
ELSIF rVoted_DrumExitTemp_degC >= (c_rDrumExitTemp_L_degC + c_rDrumExitTemp_Deadband) THEN
    bAlarm_DrumTemp_L := FALSE;
END_IF;

IF ABS(rRateOfChange_DrumExitTemp) > 4.5 THEN
    bAlarm_DrumTemp_RoC := TRUE;
ELSE
    bAlarm_DrumTemp_RoC := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * Baghouse Temperature & Differential Pressure Alarms
 * ------------------------------------------------------------------------------------------------------------------- *)
IF rBaghouse_InletTemp_degC >= c_rBaghouseInletTemp_HH_degC THEN
    bAlarm_BaghouseTemp_HH := TRUE;
    bBaghouse_EmergencyBypass_Open := TRUE; (* Open emergency thermal bypass damper *)
ELSIF rBaghouse_InletTemp_degC <= (c_rBaghouseInletTemp_HH_degC - 5.0) THEN
    bAlarm_BaghouseTemp_HH := FALSE;
    bBaghouse_EmergencyBypass_Open := FALSE;
END_IF;

IF rBaghouse_InletTemp_degC >= c_rBaghouseInletTemp_H_degC THEN
    bAlarm_BaghouseTemp_H := TRUE;
ELSIF rBaghouse_InletTemp_degC <= (c_rBaghouseInletTemp_H_degC - 4.0) THEN
    bAlarm_BaghouseTemp_H := FALSE;
END_IF;

IF rBaghouse_DeltaP_mbar >= c_rBaghouseDeltaP_HH_mbar THEN
    bAlarm_BaghouseDeltaP_HH := TRUE;
ELSIF rBaghouse_DeltaP_mbar <= (c_rBaghouseDeltaP_HH_mbar - 1.5) THEN
    bAlarm_BaghouseDeltaP_HH := FALSE;
END_IF;

IF rBaghouse_DeltaP_mbar >= c_rBaghouseDeltaP_H_mbar THEN
    bAlarm_BaghouseDeltaP_H := TRUE;
ELSIF rBaghouse_DeltaP_mbar <= (c_rBaghouseDeltaP_H_mbar - 1.0) THEN
    bAlarm_BaghouseDeltaP_H := FALSE;
END_IF;

IF ABS(rRateOfChange_BaghouseDeltaP) > 2.0 THEN
    bAlarm_BaghouseDeltaP_RoC := TRUE;
ELSE
    bAlarm_BaghouseDeltaP_RoC := FALSE;
END_IF;

IF rBaghouse_Exhaust_LEL_pct >= c_rBaghouseLEL_HH_pct THEN
    bAlarm_BaghouseLEL_HH := TRUE;
ELSIF rBaghouse_Exhaust_LEL_pct <= (c_rBaghouseLEL_HH_pct - 2.0) THEN
    bAlarm_BaghouseLEL_HH := FALSE;
END_IF;

IF rBaghouse_Exhaust_LEL_pct >= c_rBaghouseLEL_H_pct THEN
    bAlarm_BaghouseLEL_H := TRUE;
ELSIF rBaghouse_Exhaust_LEL_pct <= (c_rBaghouseLEL_H_pct - 1.5) THEN
    bAlarm_BaghouseLEL_H := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * Bitumen Temperature & Pugmill Torque Alarms
 * ------------------------------------------------------------------------------------------------------------------- *)
IF rBitumen_StorageTank_Temp_degC >= c_rBitumenTemp_HH_degC THEN
    bAlarm_BitumenTemp_HH := TRUE;
ELSIF rBitumen_StorageTank_Temp_degC <= (c_rBitumenTemp_HH_degC - 3.0) THEN
    bAlarm_BitumenTemp_HH := FALSE;
END_IF;

IF rBitumen_StorageTank_Temp_degC >= c_rBitumenTemp_H_degC THEN
    bAlarm_BitumenTemp_H := TRUE;
ELSIF rBitumen_StorageTank_Temp_degC <= (c_rBitumenTemp_H_degC - 2.5) THEN
    bAlarm_BitumenTemp_H := FALSE;
END_IF;

IF rBitumen_StorageTank_Temp_degC <= c_rBitumenTemp_LL_degC THEN
    bAlarm_BitumenTemp_LL := TRUE;
ELSIF rBitumen_StorageTank_Temp_degC >= (c_rBitumenTemp_LL_degC + 3.0) THEN
    bAlarm_BitumenTemp_LL := FALSE;
END_IF;

IF rBitumen_StorageTank_Temp_degC <= c_rBitumenTemp_L_degC THEN
    bAlarm_BitumenTemp_L := TRUE;
ELSIF rBitumen_StorageTank_Temp_degC >= (c_rBitumenTemp_L_degC + 2.5) THEN
    bAlarm_BitumenTemp_L := FALSE;
END_IF;

IF rBitumen_Spray_Pressure_bar < 2.5 AND bBitumen_SprayBar_Valve_Cmd THEN
    bAlarm_BitumenPressure_L := TRUE;
ELSE
    bAlarm_BitumenPressure_L := FALSE;
END_IF;

IF rBaghouse_PulseAir_Pressure_bar < 4.5 THEN
    bAlarm_PulseAirPressure_L := TRUE;
ELSE
    bAlarm_PulseAirPressure_L := FALSE;
END_IF;

IF rPugmill_Drive_Torque_Nm >= c_rPugmillTorque_HH_Nm THEN
    bAlarm_PugmillTorque_HH := TRUE;
ELSIF rPugmill_Drive_Torque_Nm <= (c_rPugmillTorque_HH_Nm - 400.0) THEN
    bAlarm_PugmillTorque_HH := FALSE;
END_IF;

IF rPugmill_Drive_Torque_Nm >= c_rPugmillTorque_H_Nm THEN
    bAlarm_PugmillTorque_H := TRUE;
ELSIF rPugmill_Drive_Torque_Nm <= (c_rPugmillTorque_H_Nm - 300.0) THEN
    bAlarm_PugmillTorque_H := FALSE;
END_IF;

(* Flame Failure Detection *)
IF (iPlantState >= c_ST_DRUM_DRYING_BURNER_MOD) AND (rDrum_Burner_FlameIntensity_pct < 25.0) THEN
    bAlarm_FlameFailure := TRUE;
ELSE
    bAlarm_FlameFailure := FALSE;
END_IF;

(* Drum Internal Draft Loss *)
IF rDrum_InternalDraft_mbar > 0.5 THEN
    bAlarm_DrumDraftLoss := TRUE;
ELSE
    bAlarm_DrumDraftLoss := FALSE;
END_IF;

(* Bucket Elevator Slip *)
IF rElevator_SlipPercentage > 15.0 THEN
    bAlarm_HotElevatorSlip := TRUE;
ELSE
    bAlarm_HotElevatorSlip := FALSE;
END_IF;

(* Screen Blinding Detection *)
IF rScreen_Vibration_RMS_mms > 12.0 OR rScreen_Vibration_RMS_mms < 2.0 THEN
    bAlarm_ScreenBlinding := TRUE;
ELSE
    bAlarm_ScreenBlinding := FALSE;
END_IF;

(* Master Plant Trip Interlock Logic *)
bMasterPlantTrip := NOT bEStop OR
                    bAlarm_DrumTemp_HH OR
                    bAlarm_BaghouseTemp_HH OR
                    bAlarm_BaghouseLEL_HH OR
                    bAlarm_PugmillTorque_HH OR
                    bAlarm_FlameFailure OR
                    bSkipHoist_SlackRope_Fault OR
                    (iTMR1_HealthGrade = 0) OR
                    (iTMR2_HealthGrade = 0) OR
                    (iTMR3_HealthGrade = 0);

(* -------------------------------------------------------------------------------------------------------------------
 * ISA-18.2 Diagnostic Alarm Word 0: Process Alarms
 * ------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord0_Process := 16#00000000;
IF bAlarm_DrumTemp_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000001; END_IF;
IF bAlarm_DrumTemp_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000002; END_IF;
IF bAlarm_DrumTemp_L THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000004; END_IF;
IF bAlarm_DrumTemp_LL THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000008; END_IF;
IF bAlarm_DrumTemp_RoC THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000010; END_IF;
IF bAlarm_BaghouseTemp_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000020; END_IF;
IF bAlarm_BaghouseTemp_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000040; END_IF;
IF bAlarm_BaghouseDeltaP_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000080; END_IF;
IF bAlarm_BaghouseDeltaP_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000100; END_IF;
IF bAlarm_BaghouseDeltaP_RoC THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000200; END_IF;
IF bAlarm_BaghouseLEL_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000400; END_IF;
IF bAlarm_BaghouseLEL_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00000800; END_IF;
IF bAlarm_BitumenTemp_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00001000; END_IF;
IF bAlarm_BitumenTemp_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00002000; END_IF;
IF bAlarm_BitumenTemp_L THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00004000; END_IF;
IF bAlarm_BitumenTemp_LL THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00008000; END_IF;
IF bAlarm_PugmillTorque_HH THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00010000; END_IF;
IF bAlarm_PugmillTorque_H THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00020000; END_IF;
IF bAlarm_BitumenPressure_L THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00040000; END_IF;
IF bAlarm_PulseAirPressure_L THEN dwAlarmWord0_Process := dwAlarmWord0_Process OR 16#00080000; END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * ISA-18.2 Diagnostic Alarm Word 1: Sensor & TMR Redundancy Faults
 * ------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord1_SensorsTMR := 16#00000000;
IF bTMR1_FaultA THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000001; END_IF;
IF bTMR1_FaultB THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000002; END_IF;
IF bTMR1_FaultC THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000004; END_IF;
IF iTMR1_HealthGrade = 2 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000008; END_IF;
IF iTMR1_HealthGrade = 1 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000010; END_IF;
IF iTMR1_HealthGrade = 0 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000020; END_IF;
IF bTMR2_FaultA THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000040; END_IF;
IF bTMR2_FaultB THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000080; END_IF;
IF bTMR2_FaultC THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000100; END_IF;
IF iTMR2_HealthGrade = 2 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000200; END_IF;
IF iTMR2_HealthGrade = 1 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000400; END_IF;
IF iTMR2_HealthGrade = 0 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00000800; END_IF;
IF bTMR3_FaultA THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00001000; END_IF;
IF bTMR3_FaultB THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00002000; END_IF;
IF bTMR3_FaultC THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00004000; END_IF;
IF iTMR3_HealthGrade = 2 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00008000; END_IF;
IF iTMR3_HealthGrade = 1 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00010000; END_IF;
IF iTMR3_HealthGrade = 0 THEN dwAlarmWord1_SensorsTMR := dwAlarmWord1_SensorsTMR OR 16#00020000; END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * ISA-18.2 Diagnostic Alarm Word 2: Actuator & Interlock Faults
 * ------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord2_ActuatorsInterlocks := 16#00000000;
IF bAlarm_FlameFailure THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000001; END_IF;
IF bAlarm_DrumDraftLoss THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000002; END_IF;
IF bAlarm_HotElevatorSlip THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000004; END_IF;
IF bAlarm_ScreenBlinding THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000008; END_IF;
IF bSkipHoist_SlackRope_Fault THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000010; END_IF;
IF rDrum_Drive_Current_A > 115.0 THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000020; END_IF;
IF rExhaust_Fan_Current_A > 340.0 THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000040; END_IF;
IF rPugmill_BearingTemp_degC > 85.0 THEN dwAlarmWord2_ActuatorsInterlocks := dwAlarmWord2_ActuatorsInterlocks OR 16#00000080; END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * ISA-18.2 Diagnostic Alarm Word 3: Safety Shutdown (ESD) Word
 * ------------------------------------------------------------------------------------------------------------------- *)
dwAlarmWord3_SafetyESD := 16#00000000;
IF NOT bEStop THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000001; END_IF;
IF bMasterPlantTrip THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000002; END_IF;
IF bBaghouse_EmergencyBypass_Open THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000004; END_IF;
IF bAlarm_BaghouseLEL_HH THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000008; END_IF;
IF bAlarm_DrumTemp_HH THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000010; END_IF;
IF bAlarm_PugmillTorque_HH THEN dwAlarmWord3_SafetyESD := dwAlarmWord3_SafetyESD OR 16#00000020; END_IF;

(* Fault Acknowledgment Logic *)
IF bAcknowledgeFaults THEN
    bTMR1_FaultA := FALSE;
    bTMR1_FaultB := FALSE;
    bTMR1_FaultC := FALSE;
    bTMR2_FaultA := FALSE;
    bTMR2_FaultB := FALSE;
    bTMR2_FaultC := FALSE;
    bTMR3_FaultA := FALSE;
    bTMR3_FaultB := FALSE;
    bTMR3_FaultC := FALSE;
    bAlarm_DrumTemp_HH := FALSE;
    bAlarm_DrumTemp_LL := FALSE;
    bAlarm_BaghouseTemp_HH := FALSE;
    bAlarm_BaghouseDeltaP_HH := FALSE;
    bAlarm_BaghouseLEL_HH := FALSE;
    bAlarm_BitumenTemp_HH := FALSE;
    bAlarm_BitumenTemp_LL := FALSE;
    bAlarm_PugmillTorque_HH := FALSE;
END_IF;

(* -------------------------------------------------------------------------------------------------------------------
 * Emergency Trip Overrides
 * ------------------------------------------------------------------------------------------------------------------- *)
IF bMasterPlantTrip THEN
    rBurner_FuelValve_Demand_pct := 0.0;
    bBurner_PilotGas_Solenoid := FALSE;
    bBurner_Ignition_Spark := FALSE;
    rColdMasterBelt_Speed_Cmd := 0.0;
    FOR iBinIdx := 1 TO 6 DO
        arrColdBin_BeltSpeed_Cmd[iBinIdx] := 0.0;
        arrHotBin_Gate_Coarse_Cmd[iBinIdx] := FALSE;
        arrHotBin_Gate_Fine_Cmd[iBinIdx] := FALSE;
    END_FOR;
    rBitumen_Pump_Speed_Cmd_pct := 0.0;
    bBitumen_SprayBar_Valve_Cmd := FALSE;
    bBitumen_Recirc_Valve_Cmd := TRUE;
    bFiller_DosingScrew_Run_Cmd := FALSE;
    rSkipHoist_Drive_Speed_Cmd_pct := 0.0;
    bSkipHoist_Brake_Release_Cmd := FALSE; (* Set mechanical brake *)
END_IF;
""")

    # =========================================================================
    # 11. FOOTER
    # =========================================================================
    parts.append("""END_FUNCTION_BLOCK\n""")

    return "".join(parts)

if __name__ == "__main__":
    code = generate_iec_st()
    print("Generated code length:", len(code))
    
    # Check delimiters
    lines = code.splitlines()
    print("First line:", lines[0])
    print("Last line:", lines[-1])
