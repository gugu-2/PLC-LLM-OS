# part1_header_io.py
header_io_text = """FUNCTION_BLOCK FB_Petrochem_EthylenePolymerization_3000Bar_Tubular
(*
    ==========================================================================================================
    LUMINA CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE
    Commercial Sector: Petrochemicals, Specialty High-Pressure Polymers & Supercritical Fluids
    Process Unit: Continuous Ultra-High-Pressure (3,000 Bar) Ethylene Polymerization Tubular Reactor (LDPE/EVA)
    System Classification: Ultra-High Pressure Continuous Chemical Reactor (ASME Sec VIII Div 3 / API 510)
    Safety Integrity Level: IEC 61508 / IEC 61511 Safety Instrumented System SIL-3 Capable
    
    MECHANICAL & THERMAL CHARACTERISTICS:
      - Total Tubular Length: 2,150.0 m arranged in 4 distinct thermal/process zones
      - Tube Geometry: Inner Diameter 52.0 mm, Outer Diameter 162.0 mm (Wall Thickness 55.0 mm)
      - Material Metallurgy: Forged Ni-Cr-Mo High-Strength Superalloy, autofrettaged at 7,800 bar
      - Normal Operating Pressure: 2,600.0 to 3,100.0 bar (Design Pressure 3,600.0 bar)
      - Process Operating Temperature: 165.0 to 315.0 deg C (Decomposition threshold: > 325.0 deg C)
      - Maximum Allowable Working Pressure (MAWP): 3,300.0 bar
      - Maximum Allowable Skin Temperature: 330.0 deg C

    PROCESS CHEMISTRY & MULTI-ZONE FREE-RADICAL INITIATION:
      - Monomer Feed: Pure supercritical ethylene (C2H4, purity > 99.98%, O2 < 1.0 ppm, H2O < 2.0 ppm)
      - Co-Monomer Feed: Vinyl Acetate Monomer (VAM, C4H6O2) for Ethylene-Vinyl Acetate (EVA) grades (4-28% wt)
      - Organic Peroxide Initiator Cocktails:
        * Low-Temp Initiator (Zone 1): Tert-butyl peroxypivalate (TBPPI) in isododecane (130-190 deg C)
        * Med-Low Temp Initiator (Zone 2): Tert-butyl peroxy-2-ethylhexanoate (TBPO) (170-240 deg C)
        * Med-High Temp Initiator (Zone 3): Tert-butyl peroxy-3,5,5-trimethylhexanoate (TBPEH) (220-280 deg C)
        * High-Temp Initiator (Zone 4): Di-tert-butyl peroxide (DTBP) (260-315 deg C)
      - Polymerization Thermodynamics: Exothermic enthalpy of propagation Delta H_p = -95.0 kJ/mol C2H4
      - Explosive Decomposition Risk: C2H4 -> C(solid carbon soot) + CH4(g) + Delta H_decomp (-126.0 kJ/mol)
        Runaway reaction triggers catastrophic pressure spike: dP/dt > 1,500.0 bar/s, T > 1,200.0 deg C
      - Emergency Dump System (EDS): 4 Electrohydraulic Dump Valves actuating to flare/catch-tank in < 45 ms

    CONTROL STRATEGY & MATHEMATICAL FORMALISM:
      - 2oo3 Triple Modular Redundancy (TMR) across 8 critical sensor triplets with discrepancy timers
      - Discrete State-Space Model: x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k] (16 states, 8 inputs)
      - Receding-Horizon Model Predictive Control (MPC) quadratic cost optimization with box constraints
      - Non-Newtonian Polymer Melt Rheology (Carreau-Yasuda model) & Supercritical Ethylene Density EOS
      - 12-Stage Operational Finite State Machine (Purge, Pressure Ramp, Exotherm Staging, Steady, Run-down, EDS)
      - ISA-18.2 Multi-Tiered Alarm Matrix with deadband hysteresis and 32-bit packed diagnostic telemetry
    ==========================================================================================================
*)
VAR_INPUT
    (* Master Execution and Safety Permissives *)
    bMasterEnable                   : BOOL;         (* Master system execution permissive flag *)
    bEmergencyStop                  : BOOL;         (* Hardwired E-Stop safety circuit healthy (Active High) *)
    bResetAlarms                    : BOOL;         (* Global operator alarm acknowledgment push-button *)
    bEVA_ModeSelect                 : BOOL;         (* Product Grade Selector: FALSE=LDPE Homopolymer, TRUE=EVA *)
    bAutoTuningEnable               : BOOL;         (* MPC Adaptive Weight Auto-Tuning Enable *)
    tScanCycleTime_ms               : TIME;         (* PLC scan task cycle period [ms] *)

    (* Reactor Inlet Pressure 2oo3 TMR Strain-Gauge Transmitters *)
    rPress_Inlet_ChA_bar            : REAL;         (* Reactor inlet pressure transducer Ch A [bar] *)
    rPress_Inlet_ChB_bar            : REAL;         (* Reactor inlet pressure transducer Ch B [bar] *)
    rPress_Inlet_ChC_bar            : REAL;         (* Reactor inlet pressure transducer Ch C [bar] *)

    (* Zone 1 Process Pressure 2oo3 TMR Transmitters *)
    rPress_Z1_ChA_bar               : REAL;         (* Zone 1 tubular process pressure Ch A [bar] *)
    rPress_Z1_ChB_bar               : REAL;         (* Zone 1 tubular process pressure Ch B [bar] *)
    rPress_Z1_ChC_bar               : REAL;         (* Zone 1 tubular process pressure Ch C [bar] *)

    (* Zone 2 Process Pressure 2oo3 TMR Transmitters *)
    rPress_Z2_ChA_bar               : REAL;         (* Zone 2 tubular process pressure Ch A [bar] *)
    rPress_Z2_ChB_bar               : REAL;         (* Zone 2 tubular process pressure Ch B [bar] *)
    rPress_Z2_ChC_bar               : REAL;         (* Zone 2 tubular process pressure Ch C [bar] *)

    (* Reactor Outlet Pressure before Let-Down Valve 2oo3 TMR Transmitters *)
    rPress_Outlet_ChA_bar           : REAL;         (* Reactor outlet pressure transducer Ch A [bar] *)
    rPress_Outlet_ChB_bar           : REAL;         (* Reactor outlet pressure transducer Ch B [bar] *)
    rPress_Outlet_ChC_bar           : REAL;         (* Reactor outlet pressure transducer Ch C [bar] *)

    (* Hyper-Compressor Plunger Discharge Pressure 2oo3 TMR Transmitters *)
    rPress_HyperDisch_ChA_bar       : REAL;         (* Hyper-compressor 2nd stage discharge pressure Ch A [bar] *)
    rPress_HyperDisch_ChB_bar       : REAL;         (* Hyper-compressor 2nd stage discharge pressure Ch B [bar] *)
    rPress_HyperDisch_ChC_bar       : REAL;         (* Hyper-compressor 2nd stage discharge pressure Ch C [bar] *)

    (* High-Speed Piezo-Quartz Dynamic dP/dt Decomposition Transducers Zone 1 (SIL-3 SIF) *)
    rdPdt_Z1_ChA_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 1 Ch A [bar/s] *)
    rdPdt_Z1_ChB_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 1 Ch B [bar/s] *)
    rdPdt_Z1_ChC_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 1 Ch C [bar/s] *)

    (* High-Speed Piezo-Quartz Dynamic dP/dt Decomposition Transducers Zone 2 (SIL-3 SIF) *)
    rdPdt_Z2_ChA_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 2 Ch A [bar/s] *)
    rdPdt_Z2_ChB_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 2 Ch B [bar/s] *)
    rdPdt_Z2_ChC_bar_s              : REAL;         (* Fast piezo-quartz dP/dt sensor Zone 2 Ch C [bar/s] *)

    (* Multi-Zone Peak Reaction Thermocouples 2oo3 TMR Triplet Arrays *)
    rTemp_Peak1_ChA_degC            : REAL;         (* Zone 1 reaction peak thermocouple Ch A [deg C] *)
    rTemp_Peak1_ChB_degC            : REAL;         (* Zone 1 reaction peak thermocouple Ch B [deg C] *)
    rTemp_Peak1_ChC_degC            : REAL;         (* Zone 1 reaction peak thermocouple Ch C [deg C] *)
    rTemp_Peak2_ChA_degC            : REAL;         (* Zone 2 reaction peak thermocouple Ch A [deg C] *)
    rTemp_Peak2_ChB_degC            : REAL;         (* Zone 2 reaction peak thermocouple Ch B [deg C] *)
    rTemp_Peak2_ChC_degC            : REAL;         (* Zone 2 reaction peak thermocouple Ch C [deg C] *)
    rTemp_Peak3_ChA_degC            : REAL;         (* Zone 3 reaction peak thermocouple Ch A [deg C] *)
    rTemp_Peak3_ChB_degC            : REAL;         (* Zone 3 reaction peak thermocouple Ch B [deg C] *)
    rTemp_Peak3_ChC_degC            : REAL;         (* Zone 3 reaction peak thermocouple Ch C [deg C] *)
    rTemp_Peak4_ChA_degC            : REAL;         (* Zone 4 reaction peak thermocouple Ch A [deg C] *)
    rTemp_Peak4_ChB_degC            : REAL;         (* Zone 4 reaction peak thermocouple Ch B [deg C] *)
    rTemp_Peak4_ChC_degC            : REAL;         (* Zone 4 reaction peak thermocouple Ch C [deg C] *)

    (* Monomer Feed, Initiator & Modifier Mass/Volume Flow Transmitters *)
    rFlow_EthyleneFeed_kg_h         : REAL;         (* Fresh monomer ethylene feed mass flow rate [kg/h] *)
    rFlow_RecycleSuction_kg_h       : REAL;         (* High-pressure recycle ethylene mass flow rate [kg/h] *)
    rFlow_Peroxide_Z1_l_h           : REAL;         (* Zone 1 initiator micro-metering pump flow feedback [l/h] *)
    rFlow_Peroxide_Z2_l_h           : REAL;         (* Zone 2 initiator micro-metering pump flow feedback [l/h] *)
    rFlow_Peroxide_Z3_l_h           : REAL;         (* Zone 3 initiator micro-metering pump flow feedback [l/h] *)
    rFlow_Peroxide_Z4_l_h           : REAL;         (* Zone 4 initiator micro-metering pump flow feedback [l/h] *)
    rFlow_CTA_Propionaldehyde_kg_h  : REAL;         (* Chain Transfer Agent (CTA) modifier mass flow [kg/h] *)
    rFlow_VAM_CoMonomer_kg_h        : REAL;         (* Vinyl Acetate Monomer (VAM) co-feed mass flow [kg/h] *)

    (* Cooling / Heating Jacket Water Loops *)
    rTemp_JacketIn_Z1_degC          : REAL;         (* Zone 1 pressurized hot water jacket supply temp [deg C] *)
    rTemp_JacketIn_Z2_degC          : REAL;         (* Zone 2 pressurized hot water jacket supply temp [deg C] *)
    rTemp_JacketIn_Z3_degC          : REAL;         (* Zone 3 pressurized hot water jacket supply temp [deg C] *)
    rTemp_JacketIn_Z4_degC          : REAL;         (* Zone 4 pressurized hot water jacket supply temp [deg C] *)
    rFlow_Jacket_Z1_m3_h            : REAL;         (* Zone 1 jacket circulating water volumetric flow [m3/h] *)
    rFlow_Jacket_Z2_m3_h            : REAL;         (* Zone 2 jacket circulating water volumetric flow [m3/h] *)
    rFlow_Jacket_Z3_m3_h            : REAL;         (* Zone 3 jacket circulating water volumetric flow [m3/h] *)
    rFlow_Jacket_Z4_m3_h            : REAL;         (* Zone 4 jacket circulating water volumetric flow [m3/h] *)

    (* High-Pressure Let-Down Valve & Separator Process Feedback *)
    rPos_HPLDV_Actual_pct           : REAL;         (* High-Pressure Let-Down Valve actual stem position [%] *)
    rPress_HPS_Separator_bar        : REAL;         (* High-Pressure Product Separator vessel pressure [bar] *)
    rPress_FlareHeader_bar          : REAL;         (* Plant emergency flare header backpressure [bar] *)
    rPress_HydrDumpAccum_bar        : REAL;         (* Fast dump hydraulic accumulator supply pressure [bar] *)

    (* Rotating Equipment Health Monitoring *)
    rVib_HyperCrosshead_RMS_mm_s    : REAL;         (* Hyper-compressor plunger crosshead RMS vibration [mm/s] *)
    rFlow_HyperPackingLeak_kg_h     : REAL;         (* Hyper-compressor plunger packing ethylene leakage [kg/h] *)
    rTemp_HyperBearing_degC         : REAL;         (* Hyper-compressor main shaft bearing temperature [deg C] *)

    (* Supervisory Setpoints from Plant DCS / Historian *)
    rSet_ReactorPressure_bar        : REAL;         (* Supervisory target reactor inlet pressure setpoint [bar] *)
    rSet_PeakTemp_Z1_degC           : REAL;         (* Supervisory target peak reaction temp Zone 1 [deg C] *)
    rSet_PeakTemp_Z2_degC           : REAL;         (* Supervisory target peak reaction temp Zone 2 [deg C] *)
    rSet_PeakTemp_Z3_degC           : REAL;         (* Supervisory target peak reaction temp Zone 3 [deg C] *)
    rSet_PeakTemp_Z4_degC           : REAL;         (* Supervisory target peak reaction temp Zone 4 [deg C] *)
    rSet_Target_MFI_g_10min         : REAL;         (* Polymer Melt Flow Index target setpoint [g/10min] *)
    rSet_Target_VAM_wt_pct          : REAL;         (* Target Vinyl Acetate content setpoint [%] *)
    rMFI_LabValidation_g_10min      : REAL;         (* Laboratory analytical Melt Flow Index validation [g/10min] *)
END_VAR

VAR_OUTPUT
    (* Actuator Speed, Stroke and Position Reference Commands *)
    rCmd_HyperSpeed_rpm             : REAL;         (* Hyper-compressor main drive speed setpoint [rpm] *)
    rCmd_HyperSuctionValve_pct      : REAL;         (* Hyper-compressor suction throttle control valve [%] *)
    rCmd_HPLDV_ServoPos_pct         : REAL;         (* High-Pressure Let-Down Valve electrohydraulic servo [%] *)
    rCmd_PeroxidePump_Z1_Stroke_pct : REAL;         (* Zone 1 initiator micro-metering pump stroke [%] *)
    rCmd_PeroxidePump_Z2_Stroke_pct : REAL;         (* Zone 2 initiator micro-metering pump stroke [%] *)
    rCmd_PeroxidePump_Z3_Stroke_pct : REAL;         (* Zone 3 initiator micro-metering pump stroke [%] *)
    rCmd_PeroxidePump_Z4_Stroke_pct : REAL;         (* Zone 4 initiator micro-metering pump stroke [%] *)
    rCmd_Jacket3WayValve_Z1_pct     : REAL;         (* Zone 1 jacket water mixing/cooling 3-way valve [%] *)
    rCmd_Jacket3WayValve_Z2_pct     : REAL;         (* Zone 2 jacket water mixing/cooling 3-way valve [%] *)
    rCmd_Jacket3WayValve_Z3_pct     : REAL;         (* Zone 3 jacket water mixing/cooling 3-way valve [%] *)
    rCmd_Jacket3WayValve_Z4_pct     : REAL;         (* Zone 4 jacket water mixing/cooling 3-way valve [%] *)
    rCmd_CTA_DosingPump_pct         : REAL;         (* Chain Transfer Agent metering pump displacement [%] *)
    rCmd_VAM_InjectionPump_pct      : REAL;         (* Vinyl Acetate Monomer metering pump displacement [%] *)

    (* SIL-3 Fast Emergency Depressurization (EDS) Tripping Actuators *)
    bCmd_DumpValve_Z1_Fire          : BOOL;         (* Zone 1 fast hydraulic dump valve fire command (<45 ms) *)
    bCmd_DumpValve_Z2_Fire          : BOOL;         (* Zone 2 fast hydraulic dump valve fire command (<45 ms) *)
    bCmd_DumpValve_Z3_Fire          : BOOL;         (* Zone 3 fast hydraulic dump valve fire command (<45 ms) *)
    bCmd_DumpValve_Z4_Fire          : BOOL;         (* Zone 4 fast hydraulic dump valve fire command (<45 ms) *)
    bCmd_HyperTrip_FastStop         : BOOL;         (* SIL-3 Emergency Hyper-Compressor main power trip relay *)
    bCmd_HPS_IsolateValve_Close     : BOOL;         (* High-Pressure Separator letdown emergency isolation *)
    bCmd_FlareCatchTank_Deluge      : BOOL;         (* Catch-tank high-pressure quench water deluge trigger *)
    bCmd_N2_QuenchBarrier_Open      : BOOL;         (* High-pressure nitrogen blanket snuff injection valve *)

    (* 2oo3 TMR Voted Process State Outputs *)
    rVoted_Press_Inlet_bar          : REAL;         (* TMR voted reactor inlet pressure [bar] *)
    rVoted_Press_Z1_bar             : REAL;         (* TMR voted Zone 1 process pressure [bar] *)
    rVoted_Press_Z2_bar             : REAL;         (* TMR voted Zone 2 process pressure [bar] *)
    rVoted_Press_Outlet_bar         : REAL;         (* TMR voted reactor outlet pressure [bar] *)
    rVoted_Press_HyperDisch_bar     : REAL;         (* TMR voted hyper-compressor discharge pressure [bar] *)
    rVoted_Temp_Peak1_degC          : REAL;         (* TMR voted Zone 1 reaction peak temperature [deg C] *)
    rVoted_Temp_Peak2_degC          : REAL;         (* TMR voted Zone 2 reaction peak temperature [deg C] *)
    rVoted_Temp_Peak3_degC          : REAL;         (* TMR voted Zone 3 reaction peak temperature [deg C] *)
    rVoted_Temp_Peak4_degC          : REAL;         (* TMR voted Zone 4 reaction peak temperature [deg C] *)
    rCalculated_dPdt_Max_bar_s      : REAL;         (* Maximum measured process pressure rise rate [bar/s] *)

    (* Cyber-Physical Process Analytics & Polymer Quality Estimates *)
    rMonomerConversion_pct          : REAL;         (* Real-time per-pass ethylene monomer conversion [%] *)
    rProductionRate_ton_h           : REAL;         (* Instantaneous polymer production mass rate [ton/h] *)
    rEst_MeltFlowIndex_g_10min      : REAL;         (* Dynamic state observer estimated product MFI [g/10min] *)
    rEst_VAM_Content_wt_pct         : REAL;         (* Dynamic state observer estimated EVA copolymer VAM [%] *)
    rDecompositionRiskIndex         : REAL;         (* Runaway decomposition probability index [0.0..1.0] *)
    rLetdownCavitationIndex         : REAL;         (* Acoustic shockwave and cavitation severity index *)

    (* Operational State Machine & Safety Interlock Status *)
    iFSM_State                      : INT;          (* Master operational finite state machine state (10..120) *)
    iFSM_SubState                   : INT;          (* Active operational sub-phase sequence step *)
    bSystemHealthy                  : BOOL;         (* Overall automation and safety health indicator *)
    bSIL3_DumpTriggered             : BOOL;         (* Latching emergency decomposition dump trip active *)
    bDegraded_TMR_Active            : BOOL;         (* Sensor triplet operating in degraded 2oo2 or 1oo1 mode *)

    (* Bit-Packed Telemetry and Alarm Status Words *)
    dwStatusWord_01                 : DWORD;        (* System operational status word 1 *)
    dwStatusWord_02                 : DWORD;        (* System operational status word 2 *)
    dwAlarmWord_01                  : DWORD;        (* ISA-18.2 Critical Emergency & High-High Alarms *)
    dwAlarmWord_02                  : DWORD;        (* ISA-18.2 Warning & Deviation Alarms *)
    dwAlarmWord_03                  : DWORD;        (* Equipment, Packing & Mechanical Integrity Alarms *)
    dwDiagnosticWord_01             : DWORD;        (* 2oo3 TMR Sensor diagnostic telemetry word 1 *)
    dwDiagnosticWord_02             : DWORD;        (* Actuator, pump, and valve diagnostic telemetry word 2 *)
END_VAR
"""

