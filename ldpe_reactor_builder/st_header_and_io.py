# ldpe_reactor_builder/st_header_and_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Chemical_Polymers_HighPressure_LDPE_TubularReactor_Pulsation
(*
====================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION KERNEL - IEC 61131-3 STRUCTURED TEXT
DOMAIN: CHEMICAL & POLYMER SYNTHESIS / EXTREME HIGH-PRESSURE POLYOLEFINS
PROCESS: COMMERCIAL 3,200-BAR HIGH-PRESSURE LOW-DENSITY POLYETHYLENE (LDPE / EVA) TUBULAR REACTOR
ANNUAL PRODUCTION CAPACITY: 450,000 METRIC TONS PER ANNUM
REACTOR GEOMETRY: 1,500 METERS LENGTH, MULTI-ZONE SHRINK-FIT HIGH-ALLOY INNER BORE (45 - 60 MM)

CRITICAL CYBER-PHYSICAL SUBSYSTEMS:
  1. DYNAMIC MULTI-ZONE ORGANIC PEROXIDE FREE-RADICAL INITIATOR MICRO-METERING INJECTION:
     - 4 INDEPENDENT HIGH-PRESSURE INJECTION POINTS ALONG THE 1,500 M TUBE (ZONES 1 TO 4)
     - MULTI-COMPONENT ORGANIC PEROXIDE COCKTAILS (LOW, MEDIUM, HIGH HALF-LIFE TEMPERATURES)
     - DISSOLVED IN HYDROCARBON SOLVENT (ISODODECANE) TO CONTROL RADICAL GENERATION RATES
  2. SUPERCRITICAL ETHYLENE REACTION EXOTHERM PEAK TRACKING:
     - HEAT OF POLYMERIZATION: -95 TO -102 KJ/MOL ETHYLENE (~3.4 TO 3.6 MJ/KG)
     - SUPERCRITICAL DENSITY: 520 TO 560 KG/M3 AT 3,000 BAR
     - ADIABATIC TEMPERATURE RISE OF ~13 DEG C PER 1% ETHYLENE CONVERSION
     - REAL-TIME AXIAL SPATIAL LOCATION (Z_PEAK) TRACKING FROM 250 M TO 1,450 M
  3. HIGH-PRESSURE CYCLIC LETDOWN VALVE (HPLDV) PULSE DEPRESSURIZATION CYCLING:
     - HYDRAULIC SERVO-ACTUATED LETDOWN VALVE MODULATING UNDER 2,800 BAR PRESSURE DROP
     - 250-BAR NEGATIVE PRESSURE PULSE GENERATED EVERY 20 SECONDS (PULSE DURATION 0.85 S)
     - ACOUSTIC HYDRAULIC EXPANSION WAVE PROPAGATES AT ~1,900 M/S UPSTREAM TO SCOUR
       INSULATING POLYMER GEL FOULING BOUNDARY LAYERS (R_FOUL) FROM INNER TUBE WALLS
  4. MULTI-JACKET PRESSURIZED HOT WATER COOLING CASCADES:
     - CLOSED-LOOP PRESSURIZED TEMPERED WATER CIRCULATION AT 180 TO 240 DEG C (40 BARG SYSTEM)
     - INDEPENDENT DUAL-ZONE JACKET WATER TEMPERING CONTROL WITH RAPID BOOSTER BLENDING
  5. SUB-5 MS EXPLOSIVE DECOMPOSITION ("DECOMP") PROTECTION & FAST SNORT DUMP VENTING:
     - ETHYLENE THERMAL DISSOCIATION RUNAWAY: C2H4 -> C(SOOT) + CH4 + H2 + MASSIVE HEAT
     - FAST QUARTZ PIEZORESISTIVE DP/DT (> 1,500 BAR/S) & FAST THERMOCOUPLE DT/DT (> 50 K/S)
     - ACOUSTIC EMISSION HIGH-FREQUENCY CRACKING DETECTOR PRECURSOR COUPLING (> 110 DB)
     - FIRING HIGH-SPEED HYDRAULIC EXPLOSIVE SNORT DUMP VALVES IN < 30 MS INTO QUENCH SILO
  6. DISCRETE STATE-SPACE OBSERVER (6X6 SYSTEM) TRACKING T_PEAK, Z_PEAK, P_IN, P_OUT, X_CONV, MFI
  7. RECEDING-HORIZON MPC WITH 10 UNROLLED ITERATIONS OF PROJECTED GRADIENT DESCENT (PGD)
  8. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS ACROSS 4 CLUSTERS
  9. DETERMINISTIC 14-STAGE FINITE STATE MACHINE (STATES 0 TO 13)
 10. ISA-18.2 MULTI-TIER ALARM MANAGEMENT WITH 32-BIT PACKED TELEMETRY REGISTERS
====================================================================================================
*)
VAR_INPUT
    (* Master Supervisory Commands & Timing *)
    bEnable                         : BOOL;         (* Master Function Block Enable Signal [-] *)
    bAutoMode                       : BOOL;         (* Automatic Supervisory Closed-Loop Mode [-] *)
    bStartProduction                : BOOL;         (* Sequence Command: Initiate Reaction Ignition [-] *)
    bControlledTurndown             : BOOL;         (* Sequence Command: Controlled Production Rampdown [-] *)
    bEmergencyTrip                  : BOOL;         (* Emergency Fast Shutdown & Snort Vent Command [-] *)
    bResetAlarms                    : BOOL;         (* Master Alarm Acknowledge & First-Out Latch Reset [-] *)
    tScanCycleTime_s                : REAL := 0.005;(* PLC Discrete Scan Cycle Time Period [s] *)

    (* Production Recipe Setpoint Targets *)
    rRecipe_TargetReactorPressure_bar : REAL := 3050.0; (* Target Inlet Operating Pressure [bar] *)
    rRecipe_PeakTemp_Target_degC    : REAL := 302.0; (* Peak Reaction Exotherm Temperature Setpoint [deg C] *)
    rRecipe_PeakLocation_Target_m   : REAL := 720.0; (* Target Spatial Location of Reaction Peak [m] *)
    rRecipe_TargetConversion_pct    : REAL := 32.5;  (* Target Single-Pass Ethylene Monomer Conversion [%] *)
    rRecipe_TargetMFI_g10min        : REAL := 2.10;  (* Target Polyethylene Melt Flow Index [g/10min] *)
    rRecipe_EthyleneFeedRate_tph    : REAL := 115.0; (* Target Fresh + Recycle Ethylene Feed Rate [t/h] *)
    rRecipe_HPLDV_PulseAmplitude_bar: REAL := 250.0; (* Target Letdown Cyclic Pulsation Pressure Drop [bar] *)
    rRecipe_HPLDV_PulseInterval_s   : REAL := 20.0;  (* Cyclic Letdown Scour Pulse Period Interval [s] *)
    rRecipe_HPLDV_PulseDuration_s   : REAL := 0.85;  (* Letdown Valve Step Open Pulse Duration [s] *)
    rRecipe_JacketWaterTemp_degC    : REAL := 185.0; (* Pressurized Hot Water Cascade Jacket Supply Temp [deg C] *)
    rRecipe_CTA_Concentration_ppm   : REAL := 450.0; (* Chain Transfer Agent (Propylene/Propionaldehyde) [ppm] *)
    rRecipe_EVA_VinylAcetateRatio_pct : REAL := 0.0; (* Vinyl Acetate Monomer (VAM) Comonomer Ratio [%] *)

    (* Channel Cluster 1: 2oo3 Ultra-High-Pressure Quartz Transducers (Rated 4,000 bar) [bar] *)
    rPress_Transducer_1_bar         : REAL := 3048.5;(* 4,000-Bar Piezoresistive Quartz Sensor Ch1 [bar] *)
    rPress_Transducer_2_bar         : REAL := 3051.2;(* 4,000-Bar Piezoresistive Quartz Sensor Ch2 [bar] *)
    rPress_Transducer_3_bar         : REAL := 3049.8;(* 4,000-Bar Piezoresistive Quartz Sensor Ch3 [bar] *)

    (* Channel Cluster 2: 2oo3 Thick-Walled Multi-Junction Type K Thermocouples [deg C] *)
    rTemp_Thermocouple_1_degC       : REAL := 301.8; (* Thick-Wall Sheathed Fast-Response Type K Ch1 [deg C] *)
    rTemp_Thermocouple_2_degC       : REAL := 302.4; (* Thick-Wall Sheathed Fast-Response Type K Ch2 [deg C] *)
    rTemp_Thermocouple_3_degC       : REAL := 301.9; (* Thick-Wall Sheathed Fast-Response Type K Ch3 [deg C] *)

    (* Channel Cluster 3: 2oo3 Optical Absorption Coriolis Peroxide Dosing Flowmeters [kg/h] *)
    rPeroxide_FlowMeter_1_kgh       : REAL := 48.5;  (* Dual-Tube Coriolis Micro-Dosing Mass Meter Ch1 [kg/h] *)
    rPeroxide_FlowMeter_2_kgh       : REAL := 48.2;  (* Dual-Tube Coriolis Micro-Dosing Mass Meter Ch2 [kg/h] *)
    rPeroxide_FlowMeter_3_kgh       : REAL := 48.6;  (* Dual-Tube Coriolis Micro-Dosing Mass Meter Ch3 [kg/h] *)

    (* Channel Cluster 4: 2oo3 Tube Wall Acoustic Emission Decomposition Sensors [dB] *)
    rAcoustic_Emission_1_dB         : REAL := 42.0;  (* High-Frequency Resonant Acoustic Wave Sensor Ch1 [dB] *)
    rAcoustic_Emission_2_dB         : REAL := 43.5;  (* High-Frequency Resonant Acoustic Wave Sensor Ch2 [dB] *)
    rAcoustic_Emission_3_dB         : REAL := 41.8;  (* High-Frequency Resonant Acoustic Wave Sensor Ch3 [dB] *)

    (* Axial Temperature Profiling Sensors Along 1,500 m Reactor Tube [deg C] *)
    rTemp_InletZone_degC            : REAL := 165.0; (* Preheating Zone Temperature (0 - 300 m) [deg C] *)
    rTemp_Zone1_Reaction_degC       : REAL := 295.0; (* Reaction Zone 1 Temperature (300 - 600 m) [deg C] *)
    rTemp_Zone2_Reaction_degC       : REAL := 302.0; (* Reaction Zone 2 Temperature (600 - 900 m) [deg C] *)
    rTemp_Zone3_Reaction_degC       : REAL := 288.0; (* Reaction Zone 3 Temperature (900 - 1200 m) [deg C] *)
    rTemp_Zone4_Reaction_degC       : REAL := 272.0; (* Reaction Zone 4 Temperature (1200 - 1500 m) [deg C] *)
    rTemp_DischargeOutlet_degC      : REAL := 245.0; (* Reactor Discharge Before Letdown Valve [deg C] *)

    (* Hyper-Compressor & Hydraulic Recycle Measurements *)
    rHyperComp_SuctionPress_bar     : REAL := 245.0; (* Secondary Compressor Inter-Stage Suction [bar] *)
    rHyperComp_DischargePress_bar   : REAL := 3150.0;(* Secondary Compressor Discharge Header Pressure [bar] *)
    rHyperComp_PlungerMotorPower_kW : REAL := 18500.0;(* 12-Plunger Hyper-Compressor Motor Load [kW] *)
    rHyperComp_SealOilDiffPress_bar : REAL := 125.0; (* Plunger High-Pressure Seal Oil Delta-P [bar] *)
    rHPLDV_ActualPosition_pct       : REAL := 28.5;  (* High-Pressure Letdown Valve Stem Position [%] *)
    rRecycleGasFlowRate_tph         : REAL := 78.5;  (* High-Pressure Separator Recycle Gas Flow [t/h] *)
    rSeparatorPress_HPS_bar         : REAL := 255.0; (* High-Pressure Separator Gas/Polymer Vessel [bar] *)

    (* Pressurized Hot Water Cascade Cooling Subsystems *)
    rJacketWater_SupplyPress_bar    : REAL := 38.5;  (* Pressurized Water Circulation Loop Pressure [bar] *)
    rJacketWater_SupplyTemp_degC    : REAL := 182.0; (* Cooling Jacket Master Water Supply Temp [deg C] *)
    rJacketWater_ReturnTemp_degC    : REAL := 212.0; (* Cooling Jacket Master Water Return Temp [deg C] *)
    rJacketWater_CirculationFlow_m3h: REAL := 620.0; (* Hot Water Closed-Loop Recirculation Flow [m3/h] *)

    (* Multi-Zone Peroxide Micro-Metering Pump Stroke Feedbacks [1/min] *)
    rPeroxide_Pump1_StrokeRate_spm  : REAL := 125.0; (* Zone 1 Triplex Diaphragm Metering Pump [1/min] *)
    rPeroxide_Pump2_StrokeRate_spm  : REAL := 142.0; (* Zone 2 Triplex Diaphragm Metering Pump [1/min] *)
    rPeroxide_Pump3_StrokeRate_spm  : REAL := 118.0; (* Zone 3 Triplex Diaphragm Metering Pump [1/min] *)
    rPeroxide_Pump4_StrokeRate_spm  : REAL := 95.0;  (* Zone 4 Triplex Diaphragm Metering Pump [1/min] *)
END_VAR
VAR_OUTPUT
    (* Actuator Modulation Demands & Trims *)
    rCmd_HyperComp_SpeedTrim_pct    : REAL;         (* Hyper-Compressor Stepless Throughput Trim [%] *)
    rCmd_PeroxidePump1_Stroke_pct   : REAL;         (* Zone 1 Peroxide Micro-Metering Stroke Demand [%] *)
    rCmd_PeroxidePump2_Stroke_pct   : REAL;         (* Zone 2 Peroxide Micro-Metering Stroke Demand [%] *)
    rCmd_PeroxidePump3_Stroke_pct   : REAL;         (* Zone 3 Peroxide Micro-Metering Stroke Demand [%] *)
    rCmd_PeroxidePump4_Stroke_pct   : REAL;         (* Zone 4 Peroxide Micro-Metering Stroke Demand [%] *)
    rCmd_HPLDV_Position_pct         : REAL;         (* High-Pressure Letdown Valve Baseline Position [%] *)
    rCmd_JacketWater_TemperingValve_pct: REAL;      (* Pressurized Water Cooling Blending Valve Demand [%] *)
    rCmd_JacketWater_BoosterPump_pct: REAL;         (* Hot Water Circulation Booster Pump Speed Demand [%] *)
    rCmd_CTA_DosingPump_pct         : REAL;         (* Chain Transfer Agent Modulating Dosing Demand [%] *)

    (* Safety Interlock & Fast Trip Actuation Outputs *)
    bCmd_SnortValve_EmergencyDump   : BOOL;         (* Fast Hydraulic Snort Vent Valves Firing Signal [-] *)
    bCmd_HyperComp_EmergencyTrip    : BOOL;         (* Hardwired Trip Command to Secondary Compressor [-] *)
    bCmd_Peroxide_EmergencyBlockBleed: BOOL;        (* Initiator Dosing Double Block and Bleed Isolation [-] *)
    bCmd_JacketWater_ColdDelugeTrip : BOOL;         (* Emergency Cold Water High-Volume Deluge Injection [-] *)
    bCmd_HPLDV_PulseActive          : BOOL;         (* Letdown Valve Cyclic Wall Scouring Pulse Trigger [-] *)

    (* Validated & Filtered 2oo3 Sensor Process Values *)
    rVoted_ReactorPressure_bar      : REAL;         (* 2oo3 Voted Reactor Operating Pressure [bar] *)
    rVoted_PeakTemperature_degC     : REAL;         (* 2oo3 Voted Peak Exotherm Reaction Temp [deg C] *)
    rVoted_PeroxideFlow_kgh         : REAL;         (* 2oo3 Voted Initiator Master Flow Rate [kg/h] *)
    rVoted_AcousticEmission_dB      : REAL;         (* 2oo3 Voted High-Frequency Acoustic Noise [dB] *)

    (* Discrete State-Space & Cyber-Physical Observer Telemetry *)
    rEst_PeakExothermLocation_m     : REAL;         (* Estimated Axial Peak Spatial Location Z_peak [m] *)
    rEst_EthyleneConversion_pct     : REAL;         (* Estimated Monomer Single-Pass Conversion X_conv [%] *)
    rEst_PolyethyleneMFI_g10min     : REAL;         (* Estimated Polyethylene Melt Flow Index MFI [g/10min] *)
    rEst_FoulingResistance_m2K_kW   : REAL;         (* Estimated Inner Tube Wall Gel Resistance [m2 K/kW] *)
    rEst_WallGelThickness_um        : REAL;         (* Estimated Polymer Gel Boundary Layer Thickness [um] *)
    rEst_RateOfPressureRise_bar_s   : REAL;         (* Real-Time Derivative dP/dt Pressure Rise Rate [bar/s] *)
    rEst_RateOfTempRise_K_s         : REAL;         (* Real-Time Derivative dT/dt Temperature Rise Rate [K/s] *)
    rEst_HPLDV_PulseAmplitude_bar   : REAL;         (* Measured Cyclic Scouring Pulse Amplitude [bar] *)

    (* Diagnostic Flags, State Machine, and Packed Telemetry *)
    iActiveStateNumber              : INT;          (* Active 14-Stage FSM State Enumeration (0..13) [-] *)
    bDecompDetected                 : BOOL;         (* Explosive Ethylene Decomposition Event Detected [-] *)
    bPulsePhaseActive               : BOOL;         (* Wall De-Fouling Scouring Pressure Wave Active [-] *)
    bTMR_DiscrepancyAlarm           : BOOL;         (* Sensor Voting Discrepancy Fault Latched [-] *)
    rTMR_Health_Overall_pct         : REAL;         (* Total Sensor Instrument Health Reliability [%] *)
    dwAlarmWord1_Decomposition      : DWORD;        (* 32-Bit Decomposition & Extreme Pressure Alarms [-] *)
    dwAlarmWord2_ProcessExcursions  : DWORD;        (* 32-Bit Thermal Exotherm & Flow Process Alarms [-] *)
    dwAlarmWord3_SensorDiagnostics  : DWORD;        (* 32-Bit 2oo3 TMR Transducer Discrepancy Alarms [-] *)
    dwStatusWord1_FSM_Permissives   : DWORD;        (* 32-Bit State Machine & Safety Permissive Status [-] *)
    dwStatusWord2_Subsystems_Interlocks: DWORD;     (* 32-Bit Compressor, Pumps & Letdown Interlocks [-] *)
END_VAR
"""
