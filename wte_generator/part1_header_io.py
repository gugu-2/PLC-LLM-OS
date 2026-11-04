# part1_header_io.py

def get_part1_header_io():
    return """FUNCTION_BLOCK FB_WasteToEnergy_MovingGrate_SCR_FlueGasCleaning
(* =====================================================================================================================
 * LUMINA ADVANCED CYBER-PHYSICAL INDUSTRIAL AUTOMATION ENGINE - SYNTHETIC DATA ARCHITECTURE V7 MAX-PERSONA
 * ARCHITECT            : Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Industrial Experience)
 * INDUSTRIAL DOMAIN    : Municipal Waste-to-Energy (WtE) & Advanced Environmental Flue Gas Cleaning Engineering
 * SYSTEM PLANT         : 1,500 Metric Ton/Day Continuous Moving Grate Mass-Burn Municipal Solid Waste (MSW) Incinerator
 * INTEGRATED PROCESSES : - 4-Zone Hydraulic Grate Stoker Drive Stroke Speed & Bed Compaction Pacing
 *                        - Primary / Secondary Combustion Air Staged Oxygen Decoupling & Flue Gas Recirculation (FGR)
 *                        - Statutory Combustion Zone (950.0 °C to 1,050.0 °C, >= 2.0 s Residence Time per EU 2010/75/EU)
 *                        - Selective Non-Catalytic Reduction (SNCR) Multi-Level Aqueous Urea Injection (40 wt% Urea)
 *                        - In-Situ Laser Spectrometry DeNOx Observer (Stack NOx < 80 mg/Nm³, NH3 Slip < 3 mg/Nm³)
 *                        - Semi-Dry Spray Absorber Slaked Lime Ca(OH)2 Rotary Atomizer Acid Gas (HCl, SO2) Neutralization
 *                        - Powdered Activated Carbon (PAC) Pneumatic Injection for Heavy Metal & PCDD/PCDF Dioxin Adsorption
 *                        - Boiler Superheater Tube Metal Chlorine Eutectic Corrosion Acoustic Thickness Monitoring
 *                        - 8x8 Multivariable Discrete State-Space Model (50 ms Discrete Scan Cycle)
 *                        - Receding-Horizon Model Predictive Control (MPC) with Fast Projected Gradient Descent (PGD)
 *                        - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting with Bumpless Dynamic Degradation
 *                        - ISA-18.2 Multi-Tiered Process Alarm Ladder (< 1.0 s Legal Emission Exceedance Trip Latch)
 *                        - 12-Stage Deterministic Incinerator Operational Finite State Machine (FSM)
 * =====================================================================================================================
 * STANDARDIZED INDUSTRIAL P&ID TRANSDUCER & ACTUATOR INSTRUMENTATION MAPPING:
 *  - TT_COMBUSTION_CHAMBER_101A/B/C   : Optical Infrared / Suction Pyrometer Combustion Flame Core Temp [deg C] (2oo3)
 *  - TT_POST_COMBUSTION_2SEC_102A/B/C : Acoustic Pyrometric 2-Second Residence Plane Temperature [deg C] (2oo3, 15°C Tol)
 *  - ZT_GRATE_ZONE1_STROKE_201A/B/C   : Zone 1 Solid Bed Waste Drying Hydraulic Stroke Velocity [strokes/h] (2oo3)
 *  - ZT_GRATE_ZONE2_STROKE_202A/B/C   : Zone 2 Waste Pyrolysis & Ignition Stoker Stroke Velocity [strokes/h] (2oo3)
 *  - ZT_GRATE_ZONE3_STROKE_203A/B/C   : Zone 3 Main Bed Combustion Stoker Stroke Velocity [strokes/h] (2oo3)
 *  - ZT_GRATE_ZONE4_STROKE_204A/B/C   : Zone 4 Char Burnout & Sintering Stoker Stroke Velocity [strokes/h] (2oo3)
 *  - FT_PRIMARY_AIR_FLOW_301A/B/C     : Primary Forced Draft Underfire Air Header Mass Flow [Nm3/h] (2oo3)
 *  - FT_SECONDARY_AIR_FLOW_302A/B/C   : Secondary Overfire Air High-Velocity Injection Mass Flow [Nm3/h] (2oo3)
 *  - AIT_FLUEGAS_NOX_INLET_401A/B/C   : First Pass Radiant Boiler Entrance Raw Flue Gas NOx Analyzer [mg/Nm3] (2oo3)
 *  - AIT_STACK_NOX_OUTLET_402A/B/C    : Stack Continuous Emission Monitoring System (CEMS) NOx [mg/Nm3] (2oo3, 3 mg/Nm3 Tol)
 *  - AIT_STACK_NH3_SLIP_403A/B/C      : Stack Tunable Diode Laser Absorption Spectroscopy (TDLAS) NH3 Slip [mg/Nm3] (2oo3)
 *  - FT_UREA_INJECTION_501A/B/C       : Multi-Lances Aqueous Urea Solution Delivery Mass Flow [kg/h] (2oo3)
 *  - AIT_FLUEGAS_HCL_601A/B/C         : Semi-Dry Absorber Entrance Raw Hydrogen Chloride Spectrometer [mg/Nm3] (2oo3)
 *  - AIT_FLUEGAS_SO2_602A/B/C         : Semi-Dry Absorber Entrance Raw Sulfur Dioxide NDIR Analyzer [mg/Nm3] (2oo3, 3 mg/Nm3 Tol)
 *  - FT_LIME_SLURRY_FEED_701A/B/C     : Rotary Atomizer High-Density Slaked Lime Ca(OH)2 Slurry Feed [kg/h] (2oo3)
 *  - FT_ACTIVATED_CARBON_702A/B/C     : Venturi Duct Powdered Activated Carbon Pneumatic Dosing Flow [kg/h] (2oo3)
 *  - ACOU_SUPERHEATER_CORROSION_801A/B/C : Convective Superheater Tube Bank Acoustic Pulse Thickness [mm] (2oo3)
 *  - PT_FURNACE_DRAFT_103A/B/C        : Furnace Negative Pressure Draft Transmitter [mbar] (2oo3)
 *  - FT_BOILER_STEAM_FLOW_901A/B/C    : Boiler Main Superheated High-Pressure Steam Output Flow [t/h] (2oo3)
 *  - AIT_STACK_O2_404A/B/C            : Stack Dry Basis Residual Oxygen In-Situ Zirconia Analyzer [vol%] (2oo3)
 * =====================================================================================================================
 *)

VAR_INPUT
    (* Master Supervisory Execution & Safety Protection Permissives *)
    bEnable                             : BOOL := FALSE;    (* Master Incineration Line Execution Enable Permissive [BOOL] *)
    bResetFault                         : BOOL := FALSE;    (* Operator Master Fault Acknowledge & Latch Reset Pushbutton [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardwired Safety Relay E-Stop (Active LOW) [BOOL] *)
    bStartAutoIncineration              : BOOL := FALSE;    (* Plant DCS Autonomous MSW Incineration Run Command [BOOL] *)
    bAuxiliaryBurnerAvailable           : BOOL := TRUE;     (* Auxiliary Low-NOx Support Gas/Oil Burner Ready Permissive [BOOL] *)
    bIDFanRunningPermissive             : BOOL := TRUE;     (* Induced Draft (ID) Fan Running & Header Vacuum Healthy [BOOL] *)
    bBaghouseDifferentialPressureOK     : BOOL := TRUE;     (* Fabric Filter Baghouse Pulse-Jet Cleaning Permissive [BOOL] *)
    bSlagExtractorRunning               : BOOL := TRUE;     (* Wet Bottom Ash Extractor Submerged Conveyor Ready [BOOL] *)

    (* Production Recipe Setpoints & Legal Emission Limits *)
    rTargetCombustionTemp_degC          : REAL := 1020.0;   (* Target Flame Core Operating Temperature [deg C] (950..1050) *)
    rTargetPostCombTemp_degC            : REAL := 965.0;    (* Target Post-Combustion 2-Second Temperature [deg C] (>=850) *)
    rTargetExcessO2_pct                 : REAL := 6.50;     (* Target Stack Dry Flue Gas Oxygen Concentration [vol%] *)
    rTargetSteamFlow_th                 : REAL := 72.50;    (* Target Superheated Boiler Steam Evaporation Rate [t/h] *)
    rTargetStackNOx_mgNm3               : REAL := 65.00;    (* Strict In-House Stack NOx Setpoint [mg/Nm3] (Legal Max: 80.0) *)
    rTargetStackNH3Slip_mgNm3           : REAL := 1.80;     (* Target Unreacted Ammonia Slip Limit [mg/Nm3] (Legal Max: 3.0) *)
    rTargetStackSO2_mgNm3               : REAL := 25.00;    (* Target Clean Gas SO2 Concentration [mg/Nm3] (Legal Max: 40.0) *)
    rTargetStackHCl_mgNm3               : REAL := 6.50;     (* Target Clean Gas HCl Concentration [mg/Nm3] (Legal Max: 10.0) *)
    rTargetFurnaceDraft_mbar            : REAL := -2.50;    (* Furnace Combustion Chamber Controlled Depression [mbar] *)

    (* MSW Fuel Characteristics Telemetry *)
    rWasteHeatingValue_LHV_MJkg         : REAL := 9.80;     (* Estimated MSW Lower Heating Value [MJ/kg] (Nominal: 7.5..13.5) *)
    rWasteMoistureContent_pct           : REAL := 42.0;     (* Estimated MSW Bulk Moisture Weight Fraction [%] (25..55) *)

    (* 2oo3 TMR Bank 1: Combustion Flame Core Temperature Triplet [deg C] *)
    TT_COMBUSTION_CHAMBER_101A          : REAL := 1022.5;   (* Infrared Optical Pyrometer Combustion Zone Ch A [deg C] *)
    TT_COMBUSTION_CHAMBER_101B          : REAL := 1018.8;   (* Infrared Optical Pyrometer Combustion Zone Ch B [deg C] *)
    TT_COMBUSTION_CHAMBER_101C          : REAL := 1024.1;   (* Infrared Optical Pyrometer Combustion Zone Ch C [deg C] *)

    (* 2oo3 TMR Bank 2: Post-Combustion 2-Second Residence Temperature Triplet [deg C] (15.0 °C Discrepancy Tol) *)
    TT_POST_COMBUSTION_2SEC_102A        : REAL := 966.2;    (* Acoustic Pyrometric 2-Second Plane Sensor Ch A [deg C] *)
    TT_POST_COMBUSTION_2SEC_102B        : REAL := 964.5;    (* Acoustic Pyrometric 2-Second Plane Sensor Ch B [deg C] *)
    TT_POST_COMBUSTION_2SEC_102C        : REAL := 968.1;    (* Acoustic Pyrometric 2-Second Plane Sensor Ch C [deg C] *)

    (* 2oo3 TMR Bank 3: Zone 1 Solid Bed Drying Grate Stoker Stroke Speed [strokes/h] *)
    ZT_GRATE_ZONE1_STROKE_201A          : REAL := 38.5;     (* Hydraulic Stoker Linear Encoder Zone 1 Ch A [strokes/h] *)
    ZT_GRATE_ZONE1_STROKE_201B          : REAL := 38.2;     (* Hydraulic Stoker Linear Encoder Zone 1 Ch B [strokes/h] *)
    ZT_GRATE_ZONE1_STROKE_201C          : REAL := 38.7;     (* Hydraulic Stoker Linear Encoder Zone 1 Ch C [strokes/h] *)

    (* 2oo3 TMR Bank 4: Zone 4 Char Burnout Grate Stoker Stroke Speed [strokes/h] *)
    ZT_GRATE_ZONE4_STROKE_204A          : REAL := 18.2;     (* Hydraulic Stoker Linear Encoder Zone 4 Ch A [strokes/h] *)
    ZT_GRATE_ZONE4_STROKE_204B          : REAL := 18.4;     (* Hydraulic Stoker Linear Encoder Zone 4 Ch B [strokes/h] *)
    ZT_GRATE_ZONE4_STROKE_204C          : REAL := 18.1;     (* Hydraulic Stoker Linear Encoder Zone 4 Ch C [strokes/h] *)

    (* 2oo3 TMR Bank 5: Primary Underfire Air Flow Transmitters [Nm3/h] *)
    FT_PRIMARY_AIR_FLOW_301A            : REAL := 42500.0;  (* Annubar Differential Pressure Primary Air Ch A [Nm3/h] *)
    FT_PRIMARY_AIR_FLOW_301B            : REAL := 42350.0;  (* Annubar Differential Pressure Primary Air Ch B [Nm3/h] *)
    FT_PRIMARY_AIR_FLOW_301C            : REAL := 42620.0;  (* Annubar Differential Pressure Primary Air Ch C [Nm3/h] *)

    (* 2oo3 TMR Bank 6: Secondary Overfire Air Flow Transmitters [Nm3/h] *)
    FT_SECONDARY_AIR_FLOW_302A          : REAL := 24800.0;  (* Hot-Wire Thermal Mass Secondary Air Ch A [Nm3/h] *)
    FT_SECONDARY_AIR_FLOW_302B          : REAL := 24920.0;  (* Hot-Wire Thermal Mass Secondary Air Ch B [Nm3/h] *)
    FT_SECONDARY_AIR_FLOW_302C          : REAL := 24750.0;  (* Hot-Wire Thermal Mass Secondary Air Ch C [Nm3/h] *)

    (* 2oo3 TMR Bank 7: Boiler Raw Flue Gas NOx Inlet Concentration [mg/Nm3] *)
    AIT_FLUEGAS_NOX_INLET_401A          : REAL := 385.0;    (* In-Situ Ultraviolet Absorption NOx Inlet Ch A [mg/Nm3] *)
    AIT_FLUEGAS_NOX_INLET_401B          : REAL := 388.5;    (* In-Situ Ultraviolet Absorption NOx Inlet Ch B [mg/Nm3] *)
    AIT_FLUEGAS_NOX_INLET_401C          : REAL := 382.4;    (* In-Situ Ultraviolet Absorption NOx Inlet Ch C [mg/Nm3] *)

    (* 2oo3 TMR Bank 8: CEMS Clean Flue Gas NOx Stack Outlet [mg/Nm3] (3.0 mg/Nm3 Discrepancy Tol) *)
    AIT_STACK_NOX_OUTLET_402A           : REAL := 64.2;     (* Stack Chemiluminescence Analyzer Ch A [mg/Nm3] *)
    AIT_STACK_NOX_OUTLET_402B           : REAL := 63.8;     (* Stack Chemiluminescence Analyzer Ch B [mg/Nm3] *)
    AIT_STACK_NOX_OUTLET_402C           : REAL := 64.6;     (* Stack Chemiluminescence Analyzer Ch C [mg/Nm3] *)

    (* 2oo3 TMR Bank 9: TDLAS Stack Unreacted Ammonia Slip [mg/Nm3] *)
    AIT_STACK_NH3_SLIP_403A             : REAL := 1.75;     (* Tunable Diode Laser Absorption NH3 Ch A [mg/Nm3] *)
    AIT_STACK_NH3_SLIP_403B             : REAL := 1.72;     (* Tunable Diode Laser Absorption NH3 Ch B [mg/Nm3] *)
    AIT_STACK_NH3_SLIP_403C             : REAL := 1.78;     (* Tunable Diode Laser Absorption NH3 Ch C [mg/Nm3] *)

    (* 2oo3 TMR Bank 10: SNCR Aqueous Urea Injection Delivery Flow [kg/h] *)
    FT_UREA_INJECTION_501A              : REAL := 285.0;    (* Coriolis Mass Flow Meter Urea Solution Ch A [kg/h] *)
    FT_UREA_INJECTION_501B              : REAL := 286.2;    (* Coriolis Mass Flow Meter Urea Solution Ch B [kg/h] *)
    FT_UREA_INJECTION_501C              : REAL := 284.1;    (* Coriolis Mass Flow Meter Urea Solution Ch C [kg/h] *)

    (* 2oo3 TMR Bank 11: Absorber Inlet Hydrogen Chloride HCl [mg/Nm3] *)
    AIT_FLUEGAS_HCL_601A                : REAL := 820.0;    (* Hot-Wet Infrared Photometer Raw HCl Ch A [mg/Nm3] *)
    AIT_FLUEGAS_HCL_601B                : REAL := 825.0;    (* Hot-Wet Infrared Photometer Raw HCl Ch B [mg/Nm3] *)
    AIT_FLUEGAS_HCL_601C                : REAL := 817.0;    (* Hot-Wet Infrared Photometer Raw HCl Ch C [mg/Nm3] *)

    (* 2oo3 TMR Bank 12: Absorber Inlet Sulfur Dioxide SO2 [mg/Nm3] (3.0 mg/Nm3 Discrepancy Tol) *)
    AIT_FLUEGAS_SO2_602A                : REAL := 345.0;    (* NDIR Optical Sensor Raw Flue Gas SO2 Ch A [mg/Nm3] *)
    AIT_FLUEGAS_SO2_602B                : REAL := 346.5;    (* NDIR Optical Sensor Raw Flue Gas SO2 Ch B [mg/Nm3] *)
    AIT_FLUEGAS_SO2_602C                : REAL := 344.2;    (* NDIR Optical Sensor Raw Flue Gas SO2 Ch C [mg/Nm3] *)

    (* 2oo3 TMR Bank 13: Rotary Atomizer Slaked Lime Ca(OH)2 Slurry Feed [kg/h] *)
    FT_LIME_SLURRY_FEED_701A            : REAL := 480.0;    (* Electromagnetic Slurry Flow Meter Ch A [kg/h] *)
    FT_LIME_SLURRY_FEED_701B            : REAL := 482.5;    (* Electromagnetic Slurry Flow Meter Ch B [kg/h] *)
    FT_LIME_SLURRY_FEED_701C            : REAL := 478.2;    (* Electromagnetic Slurry Flow Meter Ch C [kg/h] *)

    (* 2oo3 TMR Bank 14: Powdered Activated Carbon (PAC) Dosing Flow [kg/h] *)
    FT_ACTIVATED_CARBON_702A            : REAL := 32.5;     (* Loss-In-Weight Gravimetric PAC Dosing Ch A [kg/h] *)
    FT_ACTIVATED_CARBON_702B            : REAL := 32.1;     (* Loss-In-Weight Gravimetric PAC Dosing Ch B [kg/h] *)
    FT_ACTIVATED_CARBON_702C            : REAL := 32.8;     (* Loss-In-Weight Gravimetric PAC Dosing Ch C [kg/h] *)

    (* 2oo3 TMR Bank 15: Convection Superheater Tube Acoustic Thickness [mm] *)
    ACOU_SUPERHEATER_CORROSION_801A     : REAL := 4.82;     (* Continuous High-Temp Acoustic Waveguide Ch A [mm] *)
    ACOU_SUPERHEATER_CORROSION_801B     : REAL := 4.85;     (* Continuous High-Temp Acoustic Waveguide Ch B [mm] *)
    ACOU_SUPERHEATER_CORROSION_801C     : REAL := 4.80;     (* Continuous High-Temp Acoustic Waveguide Ch C [mm] *)

    (* 2oo3 TMR Bank 16: Furnace Draft Negative Pressure [mbar] *)
    PT_FURNACE_DRAFT_103A               : REAL := -2.52;    (* Piezoresistive Furnace Depression Sensor Ch A [mbar] *)
    PT_FURNACE_DRAFT_103B               : REAL := -2.48;    (* Piezoresistive Furnace Depression Sensor Ch B [mbar] *)
    PT_FURNACE_DRAFT_103C               : REAL := -2.55;    (* Piezoresistive Furnace Depression Sensor Ch C [mbar] *)

    (* 2oo3 TMR Bank 17: Boiler High-Pressure Superheated Steam Output [t/h] *)
    FT_BOILER_STEAM_FLOW_901A           : REAL := 72.4;     (* Venturi Nozzle Main Steam Evaporation Ch A [t/h] *)
    FT_BOILER_STEAM_FLOW_901B           : REAL := 72.8;     (* Venturi Nozzle Main Steam Evaporation Ch B [t/h] *)
    FT_BOILER_STEAM_FLOW_901C           : REAL := 72.2;     (* Venturi Nozzle Main Steam Evaporation Ch C [t/h] *)

    (* 2oo3 TMR Bank 18: Stack Clean Gas Residual Oxygen Analyzer [vol%] *)
    AIT_STACK_O2_404A                   : REAL := 6.52;     (* In-Situ Zirconium Dioxide Flue Gas O2 Ch A [vol%] *)
    AIT_STACK_O2_404B                   : REAL := 6.48;     (* In-Situ Zirconium Dioxide Flue Gas O2 Ch B [vol%] *)
    AIT_STACK_O2_404C                   : REAL := 6.55;     (* In-Situ Zirconium Dioxide Flue Gas O2 Ch C [vol%] *)

    (* Hydraulic Stoker Cylinder Pressure & Jam Detection Telemetry *)
    rGrateHydraulicPressure_Zone1_bar   : REAL := 125.0;    (* Zone 1 Stoker Hydraulic Drive Pressure [bar] (Max: 210) *)
    rGrateHydraulicPressure_Zone2_bar   : REAL := 138.0;    (* Zone 2 Stoker Hydraulic Drive Pressure [bar] (Max: 210) *)
    rGrateHydraulicPressure_Zone3_bar   : REAL := 142.0;    (* Zone 3 Stoker Hydraulic Drive Pressure [bar] (Max: 210) *)
    rGrateHydraulicPressure_Zone4_bar   : REAL := 115.0;    (* Zone 4 Stoker Hydraulic Drive Pressure [bar] (Max: 210) *)
END_VAR

VAR_OUTPUT
    (* Primary Grate Stoker Hydraulic Actuator Stroke Commands *)
    rGrateSpeedCmd_Zone1_strokes_h      : REAL := 0.0;      (* Drying Grate Hydraulic Stroke Velocity Setpoint [strokes/h] *)
    rGrateSpeedCmd_Zone2_strokes_h      : REAL := 0.0;      (* Ignition Grate Hydraulic Stroke Velocity Setpoint [strokes/h] *)
    rGrateSpeedCmd_Zone3_strokes_h      : REAL := 0.0;      (* Main Combustion Grate Stroke Velocity Setpoint [strokes/h] *)
    rGrateSpeedCmd_Zone4_strokes_h      : REAL := 0.0;      (* Char Burnout Grate Stroke Velocity Setpoint [strokes/h] *)

    (* Combustion Air & Flue Gas Actuation Setpoints *)
    rPrimaryAirDamperCmd_pct            : REAL := 0.0;      (* Primary Air Individual Under-Grate Damper Position [0..100 %] *)
    rPrimaryAirFanRPMCmd_rpm            : REAL := 0.0;      (* Primary Air Forced Draft (FD) Fan VFD Speed Command [rpm] *)
    rSecondaryAirDamperCmd_pct          : REAL := 0.0;      (* Secondary Overfire Air Multi-Level Damper Position [0..100 %] *)
    rSecondaryAirFanRPMCmd_rpm          : REAL := 0.0;      (* Secondary Air High-Pressure Fan VFD Speed Command [rpm] *)
    rIDF_FanSpeedCmd_rpm                : REAL := 0.0;      (* Induced Draft (ID) Fan Furnace Depression Controller [rpm] *)
    rAuxiliaryBurnerFiringRate_pct      : REAL := 0.0;      (* Auxiliary Low-NOx Burner Thermal Support Modulation [0..100 %] *)

    (* DeNOx SNCR & Flue Gas Scrubbing Chemical Dosing Commands *)
    rUreaDosingPumpSpeedCmd_pct         : REAL := 0.0;      (* SNCR Aqueous Urea Multi-Plunger Injection Pump Stroke [%] *)
    rLimeSlurryAtomizerSpeedCmd_rpm     : REAL := 0.0;      (* Semi-Dry Absorber High-Speed Rotary Atomizer Disc [rpm] *)
    rLimeSlurryFeedPumpCmd_pct          : REAL := 0.0;      (* Ca(OH)2 Slurry Metering Cavity Pump Modulation [0..100 %] *)
    rActivatedCarbonFeederCmd_kgh       : REAL := 0.0;      (* PAC Pneumatic Ejector Dosing Mass Flow Rate Setpoint [kg/h] *)

    (* Plant Operations & Statutory Compliance Indicators *)
    bSystemReady                        : BOOL := FALSE;    (* Incineration Line Permissives Satisfied & Operational *)
    bEU_Directive_2010_75_Compliant     : BOOL := FALSE;    (* Verified T_post >= 850.0 °C for >= 2.0 s with O2 >= 6.0 % *)
    bLegalEmissionBreachTrip            : BOOL := FALSE;    (* Critical Emergency Trip: NOx/SO2/HCl Legal Exceedance *)
    bGrateHydraulicJamReverse           : BOOL := FALSE;    (* Active Fast Reverse Cycle Clears Mechanical Grate Jam *)
    bAuxiliaryBurnerActive              : BOOL := FALSE;    (* Auxiliary Burner Firing to Prevent T_post < 850 °C Breach *)

    (* Voted Telemetry & Key Process Observers *)
    rCombustionChamberTempVoted_degC    : REAL := 0.0;      (* 2oo3 Voted Combustion Flame Core Temperature [deg C] *)
    rPostCombustion2SecTempVoted_degC   : REAL := 0.0;      (* 2oo3 Voted Post-Combustion 2-Second Temperature [deg C] *)
    rPrimaryAirFlowVoted_Nm3h           : REAL := 0.0;      (* 2oo3 Voted Total Primary Underfire Air Flow [Nm3/h] *)
    rSecondaryAirFlowVoted_Nm3h         : REAL := 0.0;      (* 2oo3 Voted Total Secondary Overfire Air Flow [Nm3/h] *)
    rStackNOxVoted_mgNm3                : REAL := 0.0;      (* 2oo3 Voted Stack Clean Gas NOx Concentration [mg/Nm3] *)
    rStackNH3SlipVoted_mgNm3            : REAL := 0.0;      (* 2oo3 Voted Stack Clean Gas Ammonia Slip [mg/Nm3] *)
    rStackSO2Voted_mgNm3                : REAL := 0.0;      (* 2oo3 Voted Semi-Dry Absorber SO2 Concentration [mg/Nm3] *)
    rFlueGasHClVoted_mgNm3              : REAL := 0.0;      (* 2oo3 Voted Semi-Dry Absorber HCl Concentration [mg/Nm3] *)
    rSteamFlowVoted_th                  : REAL := 0.0;      (* 2oo3 Voted Superheated Main Boiler Steam Flow [t/h] *)
    rSuperheaterThicknessVoted_mm       : REAL := 0.0;      (* 2oo3 Voted Superheater Tube Remaining Wall Thickness [mm] *)
    rCorrosionRate_um_per_1000h         : REAL := 0.0;      (* Calculated High-Temp Chlorine Tube Thinning Rate [um/1000h] *)
    rCalculatedFlueGasResidenceTime_s   : REAL := 0.0;      (* Aerodynamic Model Computed Gas Residence Time in Post-Comb [s] *)
    rSNCR_DeNOxEfficiency_pct           : REAL := 0.0;      (* Real-Time DeNOx Conversion Efficiency Across SNCR [%] *)
    rAcidGasNeutralizationEfficiency_pct: REAL := 0.0;      (* Semi-Dry Absorber Total HCl + SO2 Neutralization Yield [%] *)
    rMPC_ObjectiveCost_J                : REAL := 0.0;      (* Receding-Horizon MPC Quadratic Functional Real-Time Cost *)

    (* Deterministic State Register & ISA-18.2 Diagnostic Packed Words *)
    wFSM_CurrentState                   : WORD := 16#0001;  (* Operational Finite State Machine State (1..12) *)
    dwSystemStatusWord                  : DWORD := 16#0000; (* Global Incineration Plant Status Bitmask *)
    dwActuatorStatusWord                : DWORD := 16#0000; (* Stoker Drive, Fans & Dosing Pumps Interlock Word *)
    dwAlarmWord_Trip                    : DWORD := 16#0000; (* ISA-18.2 Category 1 Emergency Trip Bitmask *)
    dwAlarmWord_Warning                 : DWORD := 16#0000; (* ISA-18.2 Category 2 Process Warning Bitmask *)
    dwTMR_DiagnosticWord                : DWORD := 16#0000; (* 2oo3 Sensor Bank Redundancy & Isolation Status Bitmask *)
END_VAR
"""
