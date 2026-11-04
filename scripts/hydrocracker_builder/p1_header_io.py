# -*- coding: utf-8 -*-
"""
Part 1: Header, Architectural Process Description, and I/O Declarations
for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
(* ==========================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - IEC 61131-3 HIGH-PERFORMANCE STRUCTURED TEXT
 * ARCHITECTURE: HIGH-PRESSURE CATALYTIC HYDROCRACKER & ATMOSPHERIC FRACTIONATION COMPLEX
 * SYSTEM: 4-BED FIXED TRICKLE-BED REACTOR WITH MULTI-POINT HYDROGEN QUENCH GAS INJECTION
 * DISCIPLINE: ADVANCED PETROCHEMICAL REFINING & CRITICAL SAFETY INSTRUMENTED SYSTEMS (SIL-3)
 * OPERATING CONDITIONS: P = 180.0 bar gauge, T = 380.0 .. 430.0 deg C, H2/HC = 1200 Nm3/m3
 * ==========================================================================================
 *
 * 1.0 SCIENTIFIC & PROCESS PHENOMENOLOGY OVERVIEW:
 * ------------------------------------------------------------------------------------------
 * Catalytic hydrocracking of heavy vacuum gas oils (VGO) and atmospheric residues represents
 * one of the most severe, energy-dense, and exothermic continuous catalytic processes in modern
 * petroleum refining. Hydrocarbon feedstocks containing refractory condensed polyaromatic rings,
 * organic sulfur (thiophenes, dibenzothiophenes), and organic nitrogen (pyridines, quinolines,
 * indoles, carbazoles) undergo simultaneous catalytic hydrogenation, hydrodesulfurization (HDS),
 * hydrodenitrogenation (HDN), and carbon-carbon bond cleavage over bifunctional acidic-zeolitic /
 * noble metal (Ni-Mo / Ni-W supported on amorphous silica-alumina and USY zeolite) catalysts.
 *
 * 1.1 REACTION THERMODYNAMICS & EXOTHERM SUPPRESSION DYNAMICS:
 * ------------------------------------------------------------------------------------------
 * The net reaction network is intensely exothermic, releasing between 1,200 kJ/kg and 1,800 kJ/kg
 * of reacted hydrocarbon:
 *   - Hydrodesulfurization (HDS): R-S-R' + 2 H2 --> R-H + R'-H + H2S           [Delta H ~ -280 kJ/mol]
 *   - Hydrodenitrogenation (HDN): R-N-R' + 3 H2 --> R-H + R'-H + NH3           [Delta H ~ -320 kJ/mol]
 *   - Aromatic Saturation:        Ar-Ring + 3 H2 --> Cycloalkane               [Delta H ~ -210 kJ/mol]
 *   - Hydrocracking (C-C fission): R-CH2-CH2-R' + H2 --> R-CH3 + R'-CH3        [Delta H ~ -55 kJ/mol]
 *
 * Because the activation energy of cracking is significantly higher than that of olefin/aromatic
 * saturation, an unquenched thermal rise produces positive feedback in reaction rate:
 *       r_crack(T) = k0 * exp(-Ea / (R * T)) * C_hc^alpha * P_H2^beta
 * An uncontrolled thermal runaway can elevate bed temperatures beyond 450 deg C within seconds,
 * triggering catalyst sintering, rapid coking, heavy metals deposition, and in extreme cases,
 * catastrophic metallurgical embrittlement or reactor vessel breach at 180 bar.
 *
 * To maintain an isothermal profile across the 4 catalyst beds, cold high-pressure hydrogen quench
 * gas (approx 45.0 .. 60.0 deg C) is dynamically injected through specialized inter-bed quench
 * distribution trays situated between Bed 1-2, Bed 2-3, and Bed 3-4.
 *
 * 1.2 MULTI-STAGE CYBER-PHYSICAL SUBSYSTEMS GOVERNED:
 * ------------------------------------------------------------------------------------------
 *  1. 4-Bed Trickle-Bed Hydroprocessing Reactor:
 *     - Multi-point radial/axial thermocouple arrays (MTA) per bed with 2oo3 TMR voting.
 *     - Dynamic rate-of-change runaway trip detector: dT/dt > 15.0 deg C/min automatic blowdown.
 *     - Two-phase gas-liquid trickle flow regime monitoring via modified Ergun pressure drop.
 *  2. High-Pressure Separator Complex (Hot High-Pressure Separator & Cold High-Pressure Separator):
 *     - Dual-redundant nuclear level measurement with 2oo3 voting.
 *     - Multi-stage cavitation-free high-pressure letdown valves to intermediate pressure flash drum.
 *  3. Sour Gas Amine Absorption Scrubber:
 *     - Closed-loop counter-current H2S mass transfer into lean aqueous MDEA / DEA solution.
 *     - Dynamic circulation balancing to maintain overhead recycle gas H2S < 20 ppm vol.
 *  4. Atmospheric Fractionation Column:
 *     - Side-stream draw temperature profiling for Light Naphtha, Heavy Naphtha, Kerosene/Jet-A1,
 *       Ultra-Low Sulfur Diesel (ULSD), and Unconverted Oil (UCO) recycle bottoms.
 *     - Heat integration between reactor effluent exchangers and fractionation fired reboiler.
 *  5. SIL-3 Emergency Depressurization System (EDP):
 *     - Dual-train fail-open emergency slam-shut blowdown valves to high-pressure flare header.
 *     - Controlled depressurization gradient: Target 20.0 bar/min according to API RP 521.
 * ========================================================================================== *)

VAR_INPUT
    (* Master Operational & Safety Supervisory Controls *)
    bEnable                         : BOOL;     (* Master Subsystem Automation Enable [TRUE=Active, FALSE=Safe Halt] *)
    bReset                          : BOOL;     (* Global System Master Fault & Latched Interlock Clear [pulse] *)
    bAutoMode                       : BOOL;     (* Recipe Sequence Governor Mode [TRUE=Cascade MPC, FALSE=Manual Hold] *)
    bEmergencyStop                  : BOOL;     (* Hardware SIL-3 Emergency Stop Pushbutton [FALSE=Tripped, TRUE=Healthy] *)
    bStartSequence                  : BOOL;     (* Master Process Unit Startup Sequence Initiation [pulse] *)
    bAckAlarms                      : BOOL;     (* ISA-18.2 Operator Alarm Acknowledge Command [pulse] *)
    bFlareHeaderReady               : BOOL;     (* Downstream High-Pressure Safety Flare Header Permissive [TRUE=Ready] *)
    bNitrogenPurgePermissive        : BOOL;     (* Utility Nitrogen Supply Header Pressure Permissive [TRUE=Ready] *)
    bHydrogenMakeUpReady            : BOOL;     (* Upstream Hydrogen Generation / PSA Plant Ready [TRUE=Ready] *)

    (* Hydrocarbon Feedstock Physical Properties & Flow Targets *)
    rFeedFlow_m3h                   : REAL;     (* Hydrocarbon Raw Feed Flow Rate [m3/h] (Range 0.0 .. 350.0, Nom 220.0) *)
    rFeedDensity_kgm3               : REAL;     (* Raw Feed Specific Density at 15 deg C [kg/m3] (Nominal 890.0 .. 940.0) *)
    rFeedSulfur_wtPct               : REAL;     (* Feed Total Sulfur Content [wt%] (Range 0.5 .. 3.5 wt%) *)
    rFeedNitrogen_ppm               : REAL;     (* Feed Basic & Total Organic Nitrogen Content [ppm] (Range 200 .. 2500) *)
    rTargetConversion_pct           : REAL;     (* Target Net Hydrocracking Conversion Setpoint [%] (Nominal 65.0 .. 82.0) *)
    rH2toHCDeliveryRatio_Nm3m3      : REAL;     (* Hydrogen-to-Hydrocarbon Treat Gas Ratio [Nm3/m3] (Nominal 1200.0) *)
    rQuenchGasSupplyTemp_degC       : REAL;     (* High-Pressure Cold Hydrogen Quench Header Temp [deg C] (Nominal 48.0) *)
    rQuenchGasSupplyPress_bar       : REAL;     (* High-Pressure Hydrogen Quench Header Pressure [bar] (Nominal 195.0) *)

    (* 2oo3 TMR Group 1: Bed 1 Multi-Point Radial Core Thermocouples [deg C] *)
    rTemp_Bed1_TE101A               : REAL;     (* Bed 1 Core Temperature Channel A (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed1_TE101B               : REAL;     (* Bed 1 Core Temperature Channel B (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed1_TE101C               : REAL;     (* Bed 1 Core Temperature Channel C (Dual Type K) [deg C] (0.0 .. 600.0) *)

    (* 2oo3 TMR Group 2: Bed 2 Multi-Point Radial Core Thermocouples [deg C] *)
    rTemp_Bed2_TE102A               : REAL;     (* Bed 2 Core Temperature Channel A (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed2_TE102B               : REAL;     (* Bed 2 Core Temperature Channel B (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed2_TE102C               : REAL;     (* Bed 2 Core Temperature Channel C (Dual Type K) [deg C] (0.0 .. 600.0) *)

    (* 2oo3 TMR Group 3: Bed 3 Multi-Point Radial Core Thermocouples [deg C] *)
    rTemp_Bed3_TE103A               : REAL;     (* Bed 3 Core Temperature Channel A (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed3_TE103B               : REAL;     (* Bed 3 Core Temperature Channel B (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed3_TE103C               : REAL;     (* Bed 3 Core Temperature Channel C (Dual Type K) [deg C] (0.0 .. 600.0) *)

    (* 2oo3 TMR Group 4: Bed 4 Multi-Point Radial Core Thermocouples [deg C] *)
    rTemp_Bed4_TE104A               : REAL;     (* Bed 4 Core Temperature Channel A (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed4_TE104B               : REAL;     (* Bed 4 Core Temperature Channel B (Dual Type K) [deg C] (0.0 .. 600.0) *)
    rTemp_Bed4_TE104C               : REAL;     (* Bed 4 Core Temperature Channel C (Dual Type K) [deg C] (0.0 .. 600.0) *)

    (* 2oo3 TMR Group 5: High-Pressure Separator Nuclear Level Transmitters [%] *)
    rLevel_HPSep_LT201A             : REAL;     (* Cold HP Separator Nuclear Radiometric Level Channel A [%] (0.0 .. 100.0) *)
    rLevel_HPSep_LT201B             : REAL;     (* Cold HP Separator Nuclear Radiometric Level Channel B [%] (0.0 .. 100.0) *)
    rLevel_HPSep_LT201C             : REAL;     (* Cold HP Separator Nuclear Radiometric Level Channel C [%] (0.0 .. 100.0) *)

    (* 2oo3 TMR Group 6: Reactor Total Differential Pressure Cells [bar] *)
    rDP_Reactor_DPT301A             : REAL;     (* Reactor Overall DP Transmitter Channel A [bar] (Range 0.0 .. 20.0) *)
    rDP_Reactor_DPT301B             : REAL;     (* Reactor Overall DP Transmitter Channel B [bar] (Range 0.0 .. 20.0) *)
    rDP_Reactor_DPT301C             : REAL;     (* Reactor Overall DP Transmitter Channel C [bar] (Range 0.0 .. 20.0) *)

    (* 2oo3 TMR Group 7: Reactor Inlet Pressure Transmitters [bar] *)
    rPress_Inlet_PT401A             : REAL;     (* Reactor Top Head Pressure Transmitter Channel A [bar] (0.0 .. 250.0) *)
    rPress_Inlet_PT401B             : REAL;     (* Reactor Top Head Pressure Transmitter Channel B [bar] (0.0 .. 250.0) *)
    rPress_Inlet_PT401C             : REAL;     (* Reactor Top Head Pressure Transmitter Channel C [bar] (0.0 .. 250.0) *)

    (* 2oo3 TMR Group 8: Amine Absorber Overhead Sour Gas H2S Analyzers [ppm] *)
    rConc_OverheadH2S_AT501A        : REAL;     (* Recycle Gas Amine Column Exit H2S UV-Photometer A [ppm] (0.0 .. 500.0) *)
    rConc_OverheadH2S_AT501B        : REAL;     (* Recycle Gas Amine Column Exit H2S UV-Photometer B [ppm] (0.0 .. 500.0) *)
    rConc_OverheadH2S_AT501C        : REAL;     (* Recycle Gas Amine Column Exit H2S UV-Photometer C [ppm] (0.0 .. 500.0) *)

    (* Aux Process Analog Transmitters *)
    rTemp_FurnaceOutlet_degC        : REAL;     (* Combined Feed Fired Charge Heater Coil Exit Temp [deg C] (0.0 .. 450.0) *)
    rFlow_RecycleGas_Nm3h           : REAL;     (* Centrifugal Recycle Hydrogen Compressor Discharge Flow [Nm3/h] (0 .. 400000) *)
    rFlow_MakeUpHydrogen_Nm3h       : REAL;     (* Fresh Make-Up Hydrogen Flow Rate from PSA [Nm3/h] (0 .. 150000) *)
    rPress_HotHPSep_bar             : REAL;     (* Hot High-Pressure Separator Operating Pressure [bar] (0.0 .. 250.0) *)
    rTemp_HotHPSep_degC             : REAL;     (* Hot High-Pressure Separator Operating Temperature [deg C] (0.0 .. 350.0) *)
    rLevel_HotHPSep_pct             : REAL;     (* Hot High-Pressure Separator Hydrostatic Level [%] (0.0 .. 100.0) *)
    rLevel_AmineSump_pct            : REAL;     (* Sour Gas Scrubber Bottom Rich Amine Sump Level [%] (0.0 .. 100.0) *)
    rFlow_LeanAmine_m3h             : REAL;     (* Lean MDEA Solution Supply Flow Rate to Absorber [m3/h] (0.0 .. 250.0) *)
    rPress_FractionatorOverhead_bar : REAL;     (* Atmospheric Fractionation Tower Top Gauge Pressure [bar] (0.0 .. 5.0) *)
    rTemp_FractionatorOverhead_degC : REAL;     (* Fractionator Overhead Vapor Temperature [deg C] (50.0 .. 180.0) *)
    rTemp_DieselDraw_degC           : REAL;     (* Fractionator Side-Stream Ultra-Low Sulfur Diesel Draw Temp [deg C] *)
    rTemp_ReboilerFurnace_degC      : REAL;     (* Fractionation Tower Bottom Fired Reboiler Return Temp [deg C] *)
    rFlow_DMDS_Injection_Lh         : REAL;     (* Catalyst Pre-Sulfiding Dimethyl Disulfide (DMDS) Dosing Rate [L/h] *)

    (* Discrete Hardware Limit & Proximity Interlocks *)
    bPermissive_FlareKODrumLevel    : BOOL;     (* High-Pressure Flare Knock-Out Drum Liquid Level Safe [TRUE=Permitted] *)
    bPermissive_RecycleCompressor   : BOOL;     (* Recycle Hydrogen Gas Centrifugal Compressor Running Healthy [TRUE=Run] *)
    bPermissive_WashWaterInjection  : BOOL;     (* Effluent Air Cooler Ammonium Bisulfide Wash Water Flow Healthy [TRUE=OK] *)
    bPermissive_FurnaceDraft        : BOOL;     (* Charge Heater Induced Draft Fan & Damper Interlock Healthy [TRUE=OK] *)
    bPermissive_AmineRegenerator    : BOOL;     (* Downstream Amine Stripping & Sulfur Recovery Unit Permissive [TRUE=OK] *)
    rDeltaTime_s                    : REAL;     (* Deterministic PLC Task Cycle Time Delta [s] (Nominal 0.020 s, 20 ms scan) *)
END_VAR

VAR_OUTPUT
    (* Modulating Analog Actuator Commands [%] *)
    rValve_QuenchBed1_pct           : REAL;     (* Cold Quench Gas Injection Valve into Bed 1/2 Plena [%] (0.0 .. 100.0) *)
    rValve_QuenchBed2_pct           : REAL;     (* Cold Quench Gas Injection Valve into Bed 2/3 Plena [%] (0.0 .. 100.0) *)
    rValve_QuenchBed3_pct           : REAL;     (* Cold Quench Gas Injection Valve into Bed 3/4 Plena [%] (0.0 .. 100.0) *)
    rValve_ChargeFurnaceFuel_pct    : REAL;     (* Combined Feed Charge Heater Fuel Gas Control Valve [%] (0.0 .. 100.0) *)
    rValve_HPSep_LetdownA_pct       : REAL;     (* Cold HP Separator Liquid Level Letdown Valve Train A [%] (0.0 .. 100.0) *)
    rValve_HPSep_LetdownB_pct       : REAL;     (* Cold HP Separator Liquid Level Letdown Valve Train B [%] (0.0 .. 100.0) *)
    rValve_HotHPSep_Letdown_pct     : REAL;     (* Hot HP Separator Heavy Oil Letdown Valve [%] (0.0 .. 100.0) *)
    rPump_LeanAmine_Speed_pct       : REAL;     (* Lean MDEA Absorber Feed High-Pressure Pump VFD Speed [%] (0.0 .. 100.0) *)
    rValve_RichAmineLetdown_pct     : REAL;     (* Sour Gas Scrubber Bottom Rich Amine Letdown Valve [%] (0.0 .. 100.0) *)
    rValve_DynamicReflux_pct        : REAL;     (* Fractionator Overhead Top Reflux Modulating Valve [%] (0.0 .. 100.0) *)
    rValve_FractionatorReboiler_pct : REAL;     (* Fractionation Tower Bottom Reboiler Firing Rate [%] (0.0 .. 100.0) *)
    rPump_DMDS_Dosing_Speed_pct     : REAL;     (* Sulfiding Catalyst Activation Chemical Metering Pump Speed [%] *)

    (* Discrete Safety Solenoids & Emergency Trip Actuators *)
    bValve_EmergencyBlowdownA_Open  : BOOL;     (* SIL-3 High-Pressure Flare Blowdown Depressurization Slam Valve A [TRUE=Dump] *)
    bValve_EmergencyBlowdownB_Open  : BOOL;     (* SIL-3 High-Pressure Flare Blowdown Depressurization Slam Valve B [TRUE=Dump] *)
    bValve_ReactorFeed_EmergencyShut: BOOL;     (* Reactor Combined Feed Emergency Fast-Acting Isolation Valve [TRUE=Tripped/Shut] *)
    bValve_QuenchFastDump_Open      : BOOL;     (* Emergency Cold Hydrogen Quench Flood Valve to Bed Headers [TRUE=Open] *)
    bValve_MakeupH2_EmergencyShut   : BOOL;     (* Make-Up Hydrogen Battery Limit Emergency Shutoff Valve [TRUE=Tripped/Shut] *)
    bIgniter_ChargeFurnace_Kill     : BOOL;     (* Charge Heater Fuel Safety Shutoff Solenoids & Flame Kill [TRUE=Tripped/Killed] *)

    (* Cyber-Physical Observer Status & Key Process Variables *)
    iCurrentState                   : INT;      (* 12-Stage Operational Finite State Machine State Code [0 .. 11] *)
    sCurrentStateName               : STRING(48);(* Descriptive Human-Machine Interface Operational State Description *)
    rObserved_Bed1_dTdt_degCmin     : REAL;     (* Real-Time Derivative Rate-of-Change Bed 1 Core Temp [deg C/min] *)
    rObserved_Bed2_dTdt_degCmin     : REAL;     (* Real-Time Derivative Rate-of-Change Bed 2 Core Temp [deg C/min] *)
    rObserved_Bed3_dTdt_degCmin     : REAL;     (* Real-Time Derivative Rate-of-Change Bed 3 Core Temp [deg C/min] *)
    rObserved_Bed4_dTdt_degCmin     : REAL;     (* Real-Time Derivative Rate-of-Change Bed 4 Core Temp [deg C/min] *)
    rObserved_PeakCatalystTemp_degC : REAL;     (* Maximum Observed Hotspot Temperature Across All 4 Catalyst Beds [deg C] *)
    rObserved_ReactorDeltaP_bar     : REAL;     (* Instantaneous Voted Reactor Overall Pressure Drop [bar] *)
    rObserved_TrickleLiquidHoldup   : REAL;     (* Two-Phase Trickle-Bed Hydrodynamic Liquid Holdup Fraction [%] *)
    rObserved_ReactionHeatRelease_MW: REAL;     (* Total Net Catalyst Exotherm Thermal Release [MW thermal] *)
    rObserved_H2Consumption_Nm3m3  : REAL;     (* Calculated Specific Hydrogen Chemical Consumption [Nm3/m3 feed] *)
    rEstimatedConversion_pct       : REAL;     (* Bifunctional Zeolitic Kinetic Model Estimated Heavy Fraction Conversion [%] *)
    rDepressurizationRate_bar_min   : REAL;     (* Active Unit Emergency Blowdown Gradient [bar/min] (Target 20.0 bar/min) *)

    (* ISA-18.2 Alarms & Serialized Status Words *)
    dwSystemStatusWord              : DWORD;    (* Master Supervisory Automation Operating Bitmask *)
    dwTMRStatusWord                 : DWORD;    (* 2oo3 Triple Modular Redundancy Subsystem Health Bitmask *)
    dwAlarmWord1_Critical           : DWORD;    (* ISA-18.2 Priority 1 Unacknowledged Critical Safety & Trip Alarms *)
    dwAlarmWord2_Process            : DWORD;    (* ISA-18.2 Priority 2 Process Deviations & Dynamic Warnings *)
    dwAlarmWord3_TMR                : DWORD;    (* ISA-18.2 Priority 3 Sensor Voting Discrepancy & Channel Faults *)
    dwActuatorStatusWord            : DWORD;    (* Output Solenoid & Actuator Positional Command Echo Bitmask *)
    bAlarm_RunawayTripActive        : BOOL;     (* Bed Exotherm Thermal Runaway Emergency Depressurization Latched *)
    bAlarm_AnyCritical              : BOOL;     (* Master Safety Trip Active Flag [TRUE=Emergency Shutdown] *)
    bAlarm_AnyWarning               : BOOL;     (* Global Process Warning Active Flag [TRUE=Process Degradation] *)
    bUnitInRunState                 : BOOL;     (* Unit Confirmed Operating in Normal Full Load Hydrocracking Run [TRUE] *)
    bReadyForHydrocarbonFeed        : BOOL;     (* Pre-Heat, Sulfiding & Permissives Confirmed Ready for Oil Feed Cut-In *)
END_VAR
"""
