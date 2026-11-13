# ammonia_refrigeration_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_HVAC_Industrial_AmmoniaRefrigeration_CompressorRack
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL HVAC-R HEAVY INDUSTRY DIVISION - INDUSTRIAL AMMONIA COLD CHAIN INFRASTRUCTURE
========================================================================================================================
SYSTEM ARCHITECTURE:
    Industrial Ammonia (NH3 / R717) Multi-Stage Screw Compressor Rack with Economizer Liquid Subcooling,
    Floating Head Pressure Evaporative Condenser Control, and 4-Zone Reverse Hot-Gas Defrost Management.
    
FACILITY PROFILE:
    - Target Application: Central Cold Storage Distribution Logistics Hub & Blast Freezer Facility
    - Design Refrigeration Capacity: 4,500 kW (1,280 Tons of Refrigeration, TR) @ -32.0 deg C Evaporating Temp
    - Primary Refrigerant: Pure Anhydrous Ammonia (NH3 / R717, GWP = 0, ODP = 0, Molecular Mass = 17.03 g/mol)
    - Primary Compression Train:
        * Compressor 1 (Lead / Trim): 450 kW Semi-Hermetic Industrial Twin-Screw with VFD (30.0 Hz to 60.0 Hz)
        * Compressor 2 (Base Load 1): 550 kW Open-Drive Twin-Screw with Dual-Speed Soft Starter & Slide Valve
        * Compressor 3 (Base Load 2 / Swing): 550 kW Open-Drive Twin-Screw with Continuous Slide Valve & Auto-Vi
    - Economizer Subcooling System:
        * Shell-and-Plate Direct Expansion Liquid Subcooler Vessel with Dual Stepper Electronic Expansion Valves (EEV)
        * Vapor Injection to Compressor Intermediate Cavity Ports for +18.5% Cycle Thermodynamic Efficiency
    - Heat Rejection Train:
        * 3-Cell Induced Draft Evaporative Condenser with EC Fan VFDs and Dual Sump Spray Water Recirculation Pumps
        * Advanced Dynamic Floating Head Pressure Control Tracking Wet-Bulb Temperature with 8.5 bar Safety Floor
    - Oil Management Subsystem:
        * High-Efficiency Multi-Stage Coalescent Demister Oil Separators (< 3 ppm oil carryover)
        * Dual Variable-Speed Pre-Lube & Auxiliary Oil Injection Lubrication Pumps
        * Thermosyphon & 3-Way Thermostatic Mixing Valve Oil Cooling Loop maintaining 45.0 - 55.0 deg C Oil Temperature
    - Evaporator Defrost Subsystem:
        * 4-Zone Sequenced Reverse Hot-Gas Defrost with 4-Stage Soft Repressurization Bleed Management to Prevent
          Hydraulic Shock, Water Hammer, and Thermal Stress Induced Ammonia Pipe Ruptures.
    - Life Safety & Environmental Protection:
        * ANSI/IIAR 2-2021, ANSI/ASHRAE 15-2022, and OSHA 29 CFR 1910.119 PSM Compliant Architecture
        * 2oo3 Triple Modular Redundancy (TMR) Life-Safety Ambient Ammonia Gas Detection (AT-401A/B/C)
        * Automatic Emergency Two-Stage Acid Packed-Bed Scrubber and Emergency Dilution Ventilation Fan Interlocks

CONTROL & ESTIMATION METHODOLOGY:
    1. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Engine with Dynamic Discrepancy Fault Isolation:
       - Suction Header Pressure [bar] (PT-101A/B/C)
       - Compressor Discharge Temperature [deg C] (TT-201A/B/C)
       - Lubricating Oil Differential Pressure [bar] (PDT-301A/B/C)
       - Life-Safety Machinery Room Ammonia Ambient Concentration [ppm] (AT-401A/B/C)
       - Economizer Intermediate Pressure [bar] (PT-501A/B/C)
       - Condenser High-Pressure Discharge [bar] (PT-601A/B/C)
       - Ambient Wet-Bulb Temperature [deg C] (TT-602A/B/C)
    2. Discrete State-Space Cyber-Physical Estimator (8 States, 6 Control Inputs, 3 Disturbances, 8 Outputs):
       - State Propagation: x[k+1] = A * x[k] + B * u[k] + Ew * w[k]
       - Observer Innovation: x_hat[k] = x[k] + K * (y_meas[k] - C * x[k])
       - Thermodynamic Saturation Polynomials: Real-time calculation of R717 Tsat, Superheat, Enthalpy, and COP.
    3. Receding-Horizon Model Predictive Control (MPC) Solver:
       - Projected Gradient Descent (PGD) with Box Saturation and Dynamic Slew Rate Limiters
       - Cost Function: J = sum( (x - r)^T * Q * (x - r) + u^T * R * u + Delta_u^T * S * Delta_u )
       - Minimizes specific energy consumption [kW/TR] while respecting minimum suction pressure constraints.
    4. Deterministic 14-Stage Production Finite State Machine (FSM):
       - Comprehensive sequence covering Cold Initialization, Pre-Lube, Standby, Lead Soft-Start, Base Modulation,
         Lag Staging Up/Down, Economizer Port Injection, Floating Head Tracking, Defrost 4-Step Cycle, and Emergency Venting.
    5. ISA-18.2 Multi-Tiered Alarm Engine and Bit-Packed 32-Bit Telemetry Diagnostics.
========================================================================================================================
*)
VAR_INPUT
    (* ================================================================================================================ *)
    (* MASTER DIGITAL PERMISSIVES & SAFETY HARDWARE INTERLOCKS                                                          *)
    (* ================================================================================================================ *)
    bMasterSystemEnable               : BOOL := FALSE;    (* Master Rack Enable System Run Permissive [BOOL] *)
    bEmergencyStopCircuit_NC          : BOOL := TRUE;     (* Dual-Channel Safety Relay E-Stop Normally Closed [BOOL] *)
    bMachineryRoomFireAlarm_NC        : BOOL := TRUE;     (* Central Facility Fire & Toxic Gas System NC Contact [BOOL] *)
    bAcknowledgeFaultReset            : BOOL := FALSE;    (* Operator Master Alarm Silence & Fault Reset Latch [BOOL] *)
    bAutomaticModeSelect              : BOOL := TRUE;     (* System Auto Modulation (TRUE) / Manual Trim (FALSE) [BOOL] *)
    bEconomizerSubcoolingPermissive   : BOOL := TRUE;     (* Subcooler Plate Heat Exchanger Permissive [BOOL] *)
    bCondenserWaterSumpHeaterPermissive: BOOL := TRUE;    (* Evaporative Condenser Freeze Protection Sump Heater [BOOL] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): SUCTION HEADER PRESSURE TRANSMITTERS (PT-101A/B/C) [bar]                  *)
    (* ================================================================================================================ *)
    PT_SUCTION_HDR_101A               : REAL := 2.35;     (* Suction Header Pressure Transmitter Channel A [bar] *)
    PT_SUCTION_HDR_101B               : REAL := 2.35;     (* Suction Header Pressure Transmitter Channel B [bar] *)
    PT_SUCTION_HDR_101C               : REAL := 2.35;     (* Suction Header Pressure Transmitter Channel C [bar] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): COMPRESSOR DISCHARGE TEMPERATURE TRANSMITTERS (TT-201A/B/C) [deg C]        *)
    (* ================================================================================================================ *)
    TT_DISCHARGE_HDR_201A             : REAL := 82.5;     (* Common High-Pressure Discharge Gas Temp Ch A [deg C] *)
    TT_DISCHARGE_HDR_201B             : REAL := 82.5;     (* Common High-Pressure Discharge Gas Temp Ch B [deg C] *)
    TT_DISCHARGE_HDR_201C             : REAL := 82.5;     (* Common High-Pressure Discharge Gas Temp Ch C [deg C] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): LUBRICATING OIL DIFFERENTIAL PRESSURE TRANSMITTERS (PDT-301A/B/C) [bar]    *)
    (* ================================================================================================================ *)
    PDT_OIL_DIFF_301A                 : REAL := 3.20;     (* Oil Manifold to Suction Differential Pressure Ch A [bar] *)
    PDT_OIL_DIFF_301B                 : REAL := 3.20;     (* Oil Manifold to Suction Differential Pressure Ch B [bar] *)
    PDT_OIL_DIFF_301C                 : REAL := 3.20;     (* Oil Manifold to Suction Differential Pressure Ch C [bar] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): MACHINERY ROOM AMMONIA AMBIENT DETECTORS (AT-401A/B/C) [ppm]              *)
    (* ================================================================================================================ *)
    AT_NH3_AMBIENT_401A               : REAL := 4.5;      (* Machinery Room Life-Safety NH3 Detector Ch A [ppm] *)
    AT_NH3_AMBIENT_401B               : REAL := 4.5;      (* Machinery Room Life-Safety NH3 Detector Ch B [ppm] *)
    AT_NH3_AMBIENT_401C               : REAL := 4.5;      (* Machinery Room Life-Safety NH3 Detector Ch C [ppm] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): ECONOMIZER INTERMEDIATE PRESSURE TRANSMITTERS (PT-501A/B/C) [bar]          *)
    (* ================================================================================================================ *)
    PT_ECONOMIZER_501A                : REAL := 5.80;     (* Economizer Subcooler Intermediate Flash Pressure Ch A [bar] *)
    PT_ECONOMIZER_501B                : REAL := 5.80;     (* Economizer Subcooler Intermediate Flash Pressure Ch B [bar] *)
    PT_ECONOMIZER_501C                : REAL := 5.80;     (* Economizer Subcooler Intermediate Flash Pressure Ch C [bar] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): CONDENSER DISCHARGE PRESSURE TRANSMITTERS (PT-601A/B/C) [bar]              *)
    (* ================================================================================================================ *)
    PT_CONDENSER_DISCH_601A           : REAL := 11.85;    (* Evaporative Condenser Inlet Manifold Pressure Ch A [bar] *)
    PT_CONDENSER_DISCH_601B           : REAL := 11.85;    (* Evaporative Condenser Inlet Manifold Pressure Ch B [bar] *)
    PT_CONDENSER_DISCH_601C           : REAL := 11.85;    (* Evaporative Condenser Inlet Manifold Pressure Ch C [bar] *)

    (* ================================================================================================================ *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR): METEOROLOGICAL AMBIENT WET-BULB TEMPERATURE TRANSMITTERS [deg C]           *)
    (* ================================================================================================================ *)
    TT_AMBIENT_WETBULB_602A           : REAL := 18.2;     (* Psychrometric Ambient Wet-Bulb Temperature Ch A [deg C] *)
    TT_AMBIENT_WETBULB_602B           : REAL := 18.2;     (* Psychrometric Ambient Wet-Bulb Temperature Ch B [deg C] *)
    TT_AMBIENT_WETBULB_602C           : REAL := 18.2;     (* Psychrometric Ambient Wet-Bulb Temperature Ch C [deg C] *)

    (* ================================================================================================================ *)
    (* ADDITIONAL PROCESS TRANSMITTERS & THERMO-PHYSICAL SENSORS                                                        *)
    (* ================================================================================================================ *)
    TT_SUCTION_ACCUMULATOR_GAS        : REAL := -28.5;    (* Low-Pressure Liquid Accumulator Vapor Temperature [deg C] *)
    TT_OIL_SEPARATOR_SUMP             : REAL := 52.0;     (* High-Pressure Oil Separator Bulk Sump Temperature [deg C] *)
    TT_SUBCOOLED_LIQUID_OUTLET        : REAL := -12.0;    (* Subcooled High-Pressure Liquid Line to Evaporators [deg C] *)
    TT_CONDENSER_SUMP_WATER           : REAL := 22.4;     (* Evaporative Condenser Basin Water Temperature [deg C] *)
    LT_SUCTION_ACCUMULATOR_LEVEL      : REAL := 34.5;     (* Liquid Level in Low-Pressure Ammonia Accumulator [%] *)
    LT_OIL_SEPARATOR_LEVEL            : REAL := 55.0;     (* Lubricating Oil Level in Main Separator Reservoir [%] *)
    PDT_OIL_COALESCER_FILTER          : REAL := 0.42;     (* Oil Coalescent Filter Differential Pressure [bar] *)

    (* ================================================================================================================ *)
    (* COMPRESSOR SLIDE-VALVE POSITION FEEDBACKS & MOTOR DRIVES                                                         *)
    (* ================================================================================================================ *)
    rComp1_SlideValve_Feedback        : REAL := 50.0;     (* Compressor 1 Slide-Valve Linear Position [0.0..100.0 %] *)
    rComp2_SlideValve_Feedback        : REAL := 75.0;     (* Compressor 2 Slide-Valve Linear Position [0.0..100.0 %] *)
    rComp3_SlideValve_Feedback        : REAL := 0.0;      (* Compressor 3 Slide-Valve Linear Position [0.0..100.0 %] *)
    rComp1_Vi_Slide_Feedback          : REAL := 3.2;      (* Compressor 1 Variable Volume Ratio Slide Feedback [-] *)
    rComp2_Vi_Slide_Feedback          : REAL := 3.2;      (* Compressor 2 Variable Volume Ratio Slide Feedback [-] *)
    rComp3_Vi_Slide_Feedback          : REAL := 3.2;      (* Compressor 3 Variable Volume Ratio Slide Feedback [-] *)
    rComp1_VFD_ActualSpeed_Hz         : REAL := 45.0;     (* Compressor 1 Inverter Actual Motor Speed [Hz] *)
    rComp1_MotorCurrent_Amps          : REAL := 485.0;    (* Compressor 1 Stator Line Current [A] *)
    rComp2_MotorCurrent_Amps          : REAL := 610.0;    (* Compressor 2 Stator Line Current [A] *)
    rComp3_MotorCurrent_Amps          : REAL := 0.0;      (* Compressor 3 Stator Line Current [A] *)
    bComp1_RunningFeedback            : BOOL := TRUE;     (* Compressor 1 Auxiliary Contactor Feedback [BOOL] *)
    bComp2_RunningFeedback            : BOOL := TRUE;     (* Compressor 2 Auxiliary Contactor Feedback [BOOL] *)
    bComp3_RunningFeedback            : BOOL := FALSE;    (* Compressor 3 Auxiliary Contactor Feedback [BOOL] *)

    (* ================================================================================================================ *)
    (* 4-ZONE EVAPORATOR DEFROST DEMAND & COIL PRESSURE SENSORS                                                         *)
    (* ================================================================================================================ *)
    bZone1_DefrostRequest             : BOOL := FALSE;    (* Blast Freezer Evaporator Zone 1 Defrost Request [BOOL] *)
    bZone2_DefrostRequest             : BOOL := FALSE;    (* Cold Storage Room Evaporator Zone 2 Defrost Request [BOOL] *)
    bZone3_DefrostRequest             : BOOL := FALSE;    (* Frozen Food Warehouse Zone 3 Defrost Request [BOOL] *)
    bZone4_DefrostRequest             : BOOL := FALSE;    (* Dock Loading Staging Evaporator Zone 4 Defrost Request [BOOL] *)
    PT_ZONE1_COIL_PRESSURE            : REAL := 2.20;     (* Zone 1 Evaporator Internal Coil Pressure [bar] *)
    PT_ZONE2_COIL_PRESSURE            : REAL := 2.20;     (* Zone 2 Evaporator Internal Coil Pressure [bar] *)
    PT_ZONE3_COIL_PRESSURE            : REAL := 2.20;     (* Zone 3 Evaporator Internal Coil Pressure [bar] *)
    PT_ZONE4_COIL_PRESSURE            : REAL := 2.20;     (* Zone 4 Evaporator Internal Coil Pressure [bar] *)

    (* ================================================================================================================ *)
    (* OPERATOR SETPOINTS & RECIPE CONSTRAINTS                                                                          *)
    (* ================================================================================================================ *)
    rSet_SuctionPressure_Target_bar   : REAL := 2.25;     (* Operating Suction Header Target Setpoint [bar] *)
    rSet_FloatingHead_Approach_degC   : REAL := 4.50;     (* Floating Head Condenser Approach to Wet-Bulb [deg C] *)
    rSet_MinDischargePressure_bar     : REAL := 8.50;     (* Minimum Allowed Floating Discharge Pressure Floor [bar] *)
    rSet_MaxDischargePressure_bar     : REAL := 15.50;    (* Maximum Operating High-Pressure Safety Ceiling [bar] *)
    rSet_TargetOilTemp_degC           : REAL := 48.0;     (* Lubricating Sump Target Oil Temperature Setpoint [deg C] *)
    rSet_EconomizerSuperheatTarget_K  : REAL := 5.0;      (* Economizer Subcooler EEV Suction Superheat Target [K] *)
    rSet_DefrostSupplyPressure_bar    : REAL := 6.20;     (* Evaporator Hot-Gas Defrost Regulated Pressure [bar] *)
    rSet_DefrostMaxDuration_sec       : REAL := 1200.0;   (* Maximum Permitted Hot-Gas Defrost Time Out [s] *)
    rSet_DefrostSoftRepressTime_sec   : REAL := 180.0;    (* Soft Repressurization Bleed Valve Duration [s] *)
    rCycleTime_dt_sec                 : REAL := 0.100;    (* Execution Cycle Period Delta-T [s] *)
END_VAR
VAR_OUTPUT
    (* ================================================================================================================ *)
    (* COMPRESSOR ACTUATION & CAPACITY MODULATION COMMANDS                                                              *)
    (* ================================================================================================================ *)
    rComp1_VFD_SpeedCommand_Hz        : REAL := 0.0;      (* Compressor 1 VFD Speed Inverter Output [Hz] *)
    rComp1_SlideValve_Command_Pct     : REAL := 0.0;      (* Compressor 1 Hydraulic Slide-Valve Position [0.0..100.0 %] *)
    rComp2_SlideValve_Command_Pct     : REAL := 0.0;      (* Compressor 2 Hydraulic Slide-Valve Position [0.0..100.0 %] *)
    rComp3_SlideValve_Command_Pct     : REAL := 0.0;      (* Compressor 3 Hydraulic Slide-Valve Position [0.0..100.0 %] *)
    rComp1_Vi_Command                 : REAL := 3.2;      (* Compressor 1 Optimum Volume Ratio Actuator Setting [-] *)
    rComp2_Vi_Command                 : REAL := 3.2;      (* Compressor 2 Optimum Volume Ratio Actuator Setting [-] *)
    rComp3_Vi_Command                 : REAL := 3.2;      (* Compressor 3 Optimum Volume Ratio Actuator Setting [-] *)
    bComp1_StartCommand               : BOOL := FALSE;    (* Compressor 1 Main Contactor Run Relay [BOOL] *)
    bComp2_StartCommand               : BOOL := FALSE;    (* Compressor 2 Main Contactor Run Relay [BOOL] *)
    bComp3_StartCommand               : BOOL := FALSE;    (* Compressor 3 Main Contactor Run Relay [BOOL] *)

    (* ================================================================================================================ *)
    (* OIL MANAGEMENT & THERMAL REGULATION COMMANDS                                                                     *)
    (* ================================================================================================================ *)
    bPreLubeOilPump_Command           : BOOL := FALSE;    (* Auxiliary Pre-Lube & Injection Oil Pump Contactor [BOOL] *)
    rOilCooler3WayValve_Command_Pct   : REAL := 0.0;      (* Oil Cooler 3-Way Thermostatic Mixing Valve [0.0..100.0 %] *)
    rOilSumpHeater_DutyCycle_Pct      : REAL := 0.0;      (* Oil Sump Immersion Heater PWM Duty Cycle [0.0..100.0 %] *)

    (* ================================================================================================================ *)
    (* ECONOMIZER & CONDENSER CONTROL ACTUATION                                                                        *)
    (* ================================================================================================================ *)
    rEconomizer_EEV_Opening_Pct       : REAL := 0.0;      (* Economizer Stepper Expansion Valve Position [0.0..100.0 %] *)
    rCondenser_FanBank_Speed_Pct      : REAL := 0.0;      (* Evaporative Condenser EC Fan Bank Speed [0.0..100.0 %] *)
    bCondenser_SprayPump1_Command     : BOOL := FALSE;    (* Condenser Water Recirculation Spray Pump 1 [BOOL] *)
    bCondenser_SprayPump2_Command     : BOOL := FALSE;    (* Condenser Water Recirculation Spray Pump 2 [BOOL] *)
    bCondenser_SumpDrain_Command      : BOOL := FALSE;    (* Evaporative Basin Freeze Protection Automated Drain [BOOL] *)

    (* ================================================================================================================ *)
    (* 4-ZONE REVERSE HOT-GAS DEFROST SOLENOID INTERLOCKS                                                               *)
    (* ================================================================================================================ *)
    bZone1_HotGasSupplyValve          : BOOL := FALSE;    (* Zone 1 Main Hot Gas Feed Solenoid Valve [BOOL] *)
    bZone1_SoftBleedValve             : BOOL := FALSE;    (* Zone 1 Soft Equalization Bleed Solenoid Valve [BOOL] *)
    bZone1_LiquidSupplyValve          : BOOL := TRUE;     (* Zone 1 Main Liquid Ammonia Injection Solenoid [BOOL] *)
    bZone1_SuctionStopValve           : BOOL := TRUE;     (* Zone 1 Main Evaporator Wet Suction Stop Valve [BOOL] *)
    bZone2_HotGasSupplyValve          : BOOL := FALSE;    (* Zone 2 Main Hot Gas Feed Solenoid Valve [BOOL] *)
    bZone2_SoftBleedValve             : BOOL := FALSE;    (* Zone 2 Soft Equalization Bleed Solenoid Valve [BOOL] *)
    bZone2_LiquidSupplyValve          : BOOL := TRUE;     (* Zone 2 Main Liquid Ammonia Injection Solenoid [BOOL] *)
    bZone2_SuctionStopValve           : BOOL := TRUE;     (* Zone 2 Main Evaporator Wet Suction Stop Valve [BOOL] *)
    bZone3_HotGasSupplyValve          : BOOL := FALSE;    (* Zone 3 Main Hot Gas Feed Solenoid Valve [BOOL] *)
    bZone3_SoftBleedValve             : BOOL := FALSE;    (* Zone 3 Soft Equalization Bleed Solenoid Valve [BOOL] *)
    bZone3_LiquidSupplyValve          : BOOL := TRUE;     (* Zone 3 Main Liquid Ammonia Injection Solenoid [BOOL] *)
    bZone3_SuctionStopValve           : BOOL := TRUE;     (* Zone 3 Main Evaporator Wet Suction Stop Valve [BOOL] *)
    bZone4_HotGasSupplyValve          : BOOL := FALSE;    (* Zone 4 Main Hot Gas Feed Solenoid Valve [BOOL] *)
    bZone4_SoftBleedValve             : BOOL := FALSE;    (* Zone 4 Soft Equalization Bleed Solenoid Valve [BOOL] *)
    bZone4_LiquidSupplyValve          : BOOL := TRUE;     (* Zone 4 Main Liquid Ammonia Injection Solenoid [BOOL] *)
    bZone4_SuctionStopValve           : BOOL := TRUE;     (* Zone 4 Main Evaporator Wet Suction Stop Valve [BOOL] *)

    (* ================================================================================================================ *)
    (* LIFE-SAFETY & EMERGENCY MITIGATION INTERLOCKS                                                                    *)
    (* ================================================================================================================ *)
    bEmergencyVentilationFan1         : BOOL := FALSE;    (* Machinery Room Toxic Gas Emergency Exhaust Fan 1 [BOOL] *)
    bEmergencyVentilationFan2         : BOOL := FALSE;    (* Machinery Room Toxic Gas Emergency Exhaust Fan 2 [BOOL] *)
    bEmergencyScrubberCircPump        : BOOL := FALSE;    (* Dilute Sulfuric Acid / Water Packed Scrubber Pump [BOOL] *)
    bEmergencyLiquidLineKingValveShut : BOOL := FALSE;    (* High-Pressure Liquid Header Main Shutoff Interlock [BOOL] *)
    bAudibleVisualHornStrobeAlarm     : BOOL := FALSE;    (* Life Safety Toxic Gas Flashing Strobe & Siren [BOOL] *)

    (* ================================================================================================================ *)
    (* REAL-TIME THERMODYNAMIC METRICS & PROCESS MONITORS                                                               *)
    (* ================================================================================================================ *)
    rVoted_SuctionPressure_bar        : REAL := 2.35;     (* 2oo3 Filtered Suction Header Pressure [bar] *)
    rVoted_DischargeTemp_degC         : REAL := 82.5;     (* 2oo3 Filtered High-Pressure Discharge Temp [deg C] *)
    rVoted_OilDiffPressure_bar        : REAL := 3.20;     (* 2oo3 Filtered Lubricating Oil Differential [bar] *)
    rVoted_AmbientNH3_ppm             : REAL := 4.5;      (* 2oo3 Filtered Ambient Ammonia Concentration [ppm] *)
    rVoted_EconomizerPressure_bar     : REAL := 5.80;     (* 2oo3 Filtered Economizer Intermediate Pressure [bar] *)
    rVoted_CondenserPressure_bar      : REAL := 11.85;    (* 2oo3 Filtered Condenser Discharge Pressure [bar] *)
    rVoted_WetBulbTemp_degC           : REAL := 18.2;     (* 2oo3 Filtered Ambient Wet-Bulb Temperature [deg C] *)
    rCalc_SuctionSaturationTemp_degC  : REAL := -31.4;    (* Computed Saturation Temp from Suction Pressure [deg C] *)
    rCalc_SuctionSuperheat_K          : REAL := 2.9;      (* Computed Suction Vapor Superheat [K] *)
    rCalc_CondensingSaturationTemp_degC: REAL := 30.6;    (* Computed Saturation Temp from Condenser Pressure [deg C] *)
    rCalc_FloatingHeadTarget_bar      : REAL := 9.45;     (* Dynamically Computed Target Floating Head Pressure [bar] *)
    rCalc_TotalThermalCapacity_kW     : REAL := 0.0;      (* Real-Time Estimated Net Refrigeration Capacity [kW] *)
    rCalc_TotalElectricalPower_kW     : REAL := 0.0;      (* Real-Time Estimated Compressor Rack Power Draw [kW] *)
    rCalc_CoefficientOfPerformance_COP: REAL := 0.0;      (* Instantaneous Thermodynamic Cycle COP [-] *)
    rCalc_SpecificPower_kW_per_TR     : REAL := 0.0;      (* Energy Efficiency Metric Specific Power [kW/TR] *)

    (* ================================================================================================================ *)
    (* ISA-18.2 TELEMETRY & 32-BIT BIT-PACKED STATUS WORDS                                                             *)
    (* ================================================================================================================ *)
    iFSM_CurrentState                 : INT := 0;         (* Active Finite State Machine Operational Stage [0..14] *)
    dwStatusWord_General              : DWORD := 16#00000000; (* General System Health & Operating Mode Word [DWORD] *)
    dwAlarmWord_Critical              : DWORD := 16#00000000; (* ISA-18.2 Critical Trip Latched Alarms Word [DWORD] *)
    dwAlarmWord_Warning               : DWORD := 16#00000000; (* ISA-18.2 Warning & Deviation Alarms Word [DWORD] *)
    dwInterlockWord                   : DWORD := 16#00000000; (* Hardware & Permissive Interlock Status Word [DWORD] *)
    dwSensorDegradationWord           : DWORD := 16#00000000; (* 2oo3 TMR Sensor Health & Isolation Word [DWORD] *)
END_VAR
"""
