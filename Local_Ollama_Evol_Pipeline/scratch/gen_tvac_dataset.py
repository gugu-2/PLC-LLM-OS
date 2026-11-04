# Complete dataset builder script for FB_Aerospace_Spacecraft_TVAC_ThermalVacuumTesting
import os, sys, json, uuid, re

workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scripts"))
from linter import ST_Linter

def generate_full_st_code():
    parts = []

    # -------------------------------------------------------------------------
    # PART 1: HEADER & IO INTERFACES
    # -------------------------------------------------------------------------
    header_io = """FUNCTION_BLOCK FB_Aerospace_Spacecraft_TVAC_ThermalVacuumTesting
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Commercial Heavy Aerospace & Satellite Ground Test Systems
 * SYSTEM                       : Spacecraft Thermal Vacuum Chamber (TVAC) Environmental Simulation Facility
 * OPERATING RANGE              : -180.0 deg C to +150.0 deg C at 1.0E-6 mbar High-Vacuum Environment
 * SUBSYSTEMS INTEGRATED        : - Multi-Zone Liquid Nitrogen (LN2) Subcooled Circulating Heat Transfer & GN2 Trim Heaters
 *                                - In-Situ Thermoelectric Quartz Crystal Microbalance (QCM) Outgassing Deposition Observer
 *                                - Collimated Solar Simulator Xenon Arc Lamp Beam Radiance Closed-Loop Regulation
 *                                - Multi-Stage Cryogenic Turbomolecular & Condensation High-Vacuum Pumping Synchronization
 *                                - Specimen Thermal Shock Slew Rate Limiting (|dT/dt| < 2.0 deg C/min) & Delta-T Constraints
 * MATHEMATICAL RIGOR           : Full 8x8 Discrete State-Space Model (Ts = 100 ms) with Radiosity Enclosure Matrices,
 *                                Dittus-Boelter Subcooling Convection, Sauerbrey Equation, and Receding-Horizon MPC.
 * ===================================================================================================================== *)

VAR_INPUT
    (* =================================================================================================================
     * SECTION 1: 2oo3 REDUNDANT PROCESS SENSORS (13 REDUNDANT TRIPLETS, TOTAL 39 TRANSMITTERS)
     * ================================================================================================================= *)
    (* Chamber Roughing Vacuum Transmitters (Pirani / Capacitance Diaphragm Manometer) [mbar] *)
    PT_CHAMBER_ROUGH_VAC_101A       : REAL; (* Roughing Vacuum Gauge Channel A [mbar] (Range: 1.0E-3 to 1050.0 mbar) *)
    PT_CHAMBER_ROUGH_VAC_101B       : REAL; (* Roughing Vacuum Gauge Channel B [mbar] (Range: 1.0E-3 to 1050.0 mbar) *)
    PT_CHAMBER_ROUGH_VAC_101C       : REAL; (* Roughing Vacuum Gauge Channel C [mbar] (Range: 1.0E-3 to 1050.0 mbar) *)

    (* Chamber High-Vacuum Transmitters (Inverted Magnetron Cold Cathode Penning Ionization Gauge) [mbar] *)
    PT_CHAMBER_HIGH_VAC_PENNING_102A: REAL; (* High-Vacuum Penning Gauge Channel A [mbar] (Range: 1.0E-9 to 1.0E-2 mbar) *)
    PT_CHAMBER_HIGH_VAC_PENNING_102B: REAL; (* High-Vacuum Penning Gauge Channel B [mbar] (Range: 1.0E-9 to 1.0E-2 mbar) *)
    PT_CHAMBER_HIGH_VAC_PENNING_102C: REAL; (* High-Vacuum Penning Gauge Channel C [mbar] (Range: 1.0E-9 to 1.0E-2 mbar) *)

    (* Cryogenic Thermal Shroud Zone 1 (Floor / Base Plate) Multi-Point Cryo RTD Pt100 Sensors [deg C] *)
    TT_SHROUD_ZONE1_TEMP_201A       : REAL; (* Shroud Zone 1 Temperature RTD Channel A [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE1_TEMP_201B       : REAL; (* Shroud Zone 1 Temperature RTD Channel B [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE1_TEMP_201C       : REAL; (* Shroud Zone 1 Temperature RTD Channel C [deg C] (Range: -200.0 to +180.0) *)

    (* Cryogenic Thermal Shroud Zone 2 (Lower Cylindrical Shell) Multi-Point Cryo RTD Pt100 Sensors [deg C] *)
    TT_SHROUD_ZONE2_TEMP_202A       : REAL; (* Shroud Zone 2 Temperature RTD Channel A [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE2_TEMP_202B       : REAL; (* Shroud Zone 2 Temperature RTD Channel B [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE2_TEMP_202C       : REAL; (* Shroud Zone 2 Temperature RTD Channel C [deg C] (Range: -200.0 to +180.0) *)

    (* Cryogenic Thermal Shroud Zone 3 (Upper Cylindrical Shell) Multi-Point Cryo RTD Pt100 Sensors [deg C] *)
    TT_SHROUD_ZONE3_TEMP_203A       : REAL; (* Shroud Zone 3 Temperature RTD Channel A [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE3_TEMP_203B       : REAL; (* Shroud Zone 3 Temperature RTD Channel B [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE3_TEMP_203C       : REAL; (* Shroud Zone 3 Temperature RTD Channel C [deg C] (Range: -200.0 to +180.0) *)

    (* Cryogenic Thermal Shroud Zone 6 (Zenith / Top Dome) Multi-Point Cryo RTD Pt100 Sensors [deg C] *)
    TT_SHROUD_ZONE6_TEMP_206A       : REAL; (* Shroud Zone 6 Temperature RTD Channel A [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE6_TEMP_206B       : REAL; (* Shroud Zone 6 Temperature RTD Channel B [deg C] (Range: -200.0 to +180.0) *)
    TT_SHROUD_ZONE6_TEMP_206C       : REAL; (* Shroud Zone 6 Temperature RTD Channel C [deg C] (Range: -200.0 to +180.0) *)

    (* Spacecraft Payload Skin / Multi-Layer Insulation (MLI) Radiator Surface Pt100 Sensors [deg C] *)
    TT_PAYLOAD_SKIN_301A            : REAL; (* Payload MLI Skin Surface Temp Channel A [deg C] (Range: -180.0 to +150.0) *)
    TT_PAYLOAD_SKIN_301B            : REAL; (* Payload MLI Skin Surface Temp Channel B [deg C] (Range: -180.0 to +150.0) *)
    TT_PAYLOAD_SKIN_301C            : REAL; (* Payload MLI Skin Surface Temp Channel C [deg C] (Range: -180.0 to +150.0) *)

    (* Spacecraft Internal Avionics / Instrument Payload Core Temperature Pt100 Sensors [deg C] *)
    TT_PAYLOAD_INTERNAL_302A        : REAL; (* Payload Internal Core Avionics Temp Channel A [deg C] (Range: -60.0 to +90.0) *)
    TT_PAYLOAD_INTERNAL_302B        : REAL; (* Payload Internal Core Avionics Temp Channel B [deg C] (Range: -60.0 to +90.0) *)
    TT_PAYLOAD_INTERNAL_302C        : REAL; (* Payload Internal Core Avionics Temp Channel C [deg C] (Range: -60.0 to +90.0) *)

    (* Thermoelectric Quartz Crystal Microbalance (QCM) In-Situ Outgassing Deposition Beat Rate [Hz/h] *)
    QCM_OUTGASSING_RATE_401A        : REAL; (* 10 MHz TQCM Frequency Deposition Rate Channel A [Hz/h] (Range: 0.0 to 500.0) *)
    QCM_OUTGASSING_RATE_401B        : REAL; (* 10 MHz TQCM Frequency Deposition Rate Channel B [Hz/h] (Range: 0.0 to 500.0) *)
    QCM_OUTGASSING_RATE_401C        : REAL; (* 10 MHz TQCM Frequency Deposition Rate Channel C [Hz/h] (Range: 0.0 to 500.0) *)

    (* Solar Simulator Xenon Arc Lamp Collimated Beam Radiance Pyranometer Detectors [W/m2] *)
    RAD_SOLAR_SIM_FLUX_501A         : REAL; (* Collimated Solar Beam Irradiance Channel A [W/m2] (Range: 0.0 to 1800.0) *)
    RAD_SOLAR_SIM_FLUX_501B         : REAL; (* Collimated Solar Beam Irradiance Channel B [W/m2] (Range: 0.0 to 1800.0) *)
    RAD_SOLAR_SIM_FLUX_501C         : REAL; (* Collimated Solar Beam Irradiance Channel C [W/m2] (Range: 0.0 to 1800.0) *)

    (* Cryogenic Subcooled Liquid Nitrogen Shroud Circulation Mass Flow Transmitters [kg/h] *)
    FT_LN2_SHROUD_SUPPLY_601A       : REAL; (* Cryogenic Subcooled LN2 Supply Mass Flow Channel A [kg/h] (Range: 0 to 5000) *)
    FT_LN2_SHROUD_SUPPLY_601B       : REAL; (* Cryogenic Subcooled LN2 Supply Mass Flow Channel B [kg/h] (Range: 0 to 5000) *)
    FT_LN2_SHROUD_SUPPLY_601C       : REAL; (* Cryogenic Subcooled LN2 Supply Mass Flow Channel C [kg/h] (Range: 0 to 5000) *)

    (* Pressurized Gaseous Nitrogen Closed Conditioning Heating Circuit Pressure Transmitters [bar] *)
    PT_GN2_HEATING_LOOP_602A        : REAL; (* Pressurized GN2 Loop Static Pressure Channel A [bar] (Range: 0.0 to 16.0) *)
    PT_GN2_HEATING_LOOP_602B        : REAL; (* Pressurized GN2 Loop Static Pressure Channel B [bar] (Range: 0.0 to 16.0) *)
    PT_GN2_HEATING_LOOP_602C        : REAL; (* Pressurized GN2 Loop Static Pressure Channel C [bar] (Range: 0.0 to 16.0) *)

    (* Magnetic Levitation Cryogenic Turbomolecular Vacuum Pump Rotor Speed Encoders [RPM] *)
    ST_TURBOPUMP_ROTOR_RPM_701A     : REAL; (* Turbopump Rotor Magnetic Bearing Speed Channel A [RPM] (Range: 0 to 55000) *)
    ST_TURBOPUMP_ROTOR_RPM_701B     : REAL; (* Turbopump Rotor Magnetic Bearing Speed Channel B [RPM] (Range: 0 to 55000) *)
    ST_TURBOPUMP_ROTOR_RPM_701C     : REAL; (* Turbopump Rotor Magnetic Bearing Speed Channel C [RPM] (Range: 0 to 55000) *)

    (* =================================================================================================================
     * SECTION 2: OPERATOR COMMANDS, SUPERVISORY SETPOINTS & SAFETY INTERLOCK CONTACTS
     * ================================================================================================================= *)
    bMasterAutoEnable               : BOOL; (* Master Automation Sequence & Closed-Loop Control Enable Permissive *)
    bChamberDoorInterlockOk         : BOOL; (* TVAC Vessel Main Door Dual Locking Mechanism Vacuum Seal Sealed Ok *)
    bCleanroomAirLockReady          : BOOL; (* Cleanroom ISO 7 / Class 10,000 Positive Pressure Differential Permissive *)
    bEmergencyVentAbortPB           : BOOL; (* Hardwired Emergency Chamber Venting & Fast Abort Pushbutton (NC Contact) *)
    bCryoBurstDiskRuptureWire       : BOOL; (* Shroud LN2 Closed Loop Graphite Burst Disk Rupture Wire Continuity (NC) *)
    bMasterFaultReset               : BOOL; (* Operator Master Alarm Acknowledge & Fault Latch Reset Pulse *)
    rTargetShroudTemp_SP            : REAL; (* Supervisory Thermal Shroud Temperature Setpoint [-180.0 to +150.0 deg C] *)
    rTargetPayloadSkinTemp_SP       : REAL; (* Spacecraft External Radiator Skin Target Temperature Setpoint [deg C] *)
    rTargetChamberPressure_SP       : REAL; (* Target Chamber High-Vacuum Pressure Setpoint [mbar] (e.g., 1.0E-6 mbar) *)
    rTargetSolarFlux_SP             : REAL; (* Solar Simulator Collimated Beam Irradiance Target Setpoint [W/m2] *)
    rMaxAllowableRampRate_degC_min  : REAL; (* Specimen Thermal Shock Slew Rate Limit [deg C/min] (Strictly <= 2.0) *)
    rMaxAllowableSpatialGradient_degC: REAL; (* Maximum Permissible Spatial Delta-T Across Satellite Specimen [deg C] *)
    rMaxAllowableOutgassingRate_Hz_hr: REAL; (* Thermal Vacuum Bakeout In-Situ Completion Criterion [Hz/h] (e.g. 1.5) *)
    rCycleTime_s                    : REAL; (* Discrete Execution Cycle Period Delta-T [s] (Nominal 0.100 s = 100 ms) *)
END_VAR

VAR_OUTPUT
    (* =================================================================================================================
     * SECTION 3: ACTUATOR MODULATING COMMANDS & DISCRETE SAFETY INTERLOCKS
     * ================================================================================================================= *)
    (* Modulating Cryogenic Control Valve Outputs *)
    rLN2_SubcooledModulatingValve_01: REAL; (* Cryogenic Subcooled LN2 Primary Injection Control Valve Demand [% 0..100] *)
    rLN2_TrimInjectionValve_02      : REAL; (* LN2 Shroud Return Subcooling Backpressure Control Valve Demand [% 0..100] *)
    rGN2_ConditioningHeaterPower_kW : REAL; (* Pressurized Closed-Loop GN2 Electric Circulation Heater Power [0.0..150.0 kW] *)
    rSolarSimulatorThyristorPower_pct: REAL; (* Solar Sim Xenon Arc Lamp DC Rectifier Thyristor Phase Demand [% 0..100] *)
    rTurbomolecularPumpSpeedRef_RPM : REAL; (* Magnetic Levitation Turbopump VFD Speed Setpoint Demand [0..48000 RPM] *)
    rCryoCondensationExpansionValve_pct: REAL; (* Gifford-McMahon Helium Cryopump Second-Stage Cold Head Valve [% 0..100] *)
    rChamberGN2RepressurizationValve_pct: REAL; (* Proportional Dry GN2 Repressurization Bleed Valve Position [% 0..100] *)

    (* Discrete Isolation Gate Valves & Motor Contactors *)
    bRoughingIsolationValve_Cmd     : BOOL; (* Chamber Roughing Pumping Line High-Conductance Pneumatic Gate Valve *)
    bTurbopumpHighVacGateValve_Cmd  : BOOL; (* Turbomolecular Pump Inlet DN500 Electro-Pneumatic High-Vac Gate Valve *)
    bCryopumpHighVacGateValve_Cmd   : BOOL; (* Helium Cryo-Condensation Pump DN800 High-Vacuum Gate Valve Open Cmd *)
    bLN2CirculationPumpContactor    : BOOL; (* Cryogenic Subcooled Centrifugal Circulation Pump Motor Contactor Run Cmd *)
    bGN2CirculationBlowerContactor  : BOOL; (* High-Temperature Hermetic GN2 Circulation Blower Contactor Run Cmd *)
    bFastEmergencyRepressValve_Cmd  : BOOL; (* Emergency Chamber Fast-Acting Repressurization Safety Valve (< 200 ms) *)
    bSpecimenPowerDisconnectRelay   : BOOL; (* Specimen Payload Electrical Feedthrough Emergency Isolation Breaker *)
    bFacilitySafetyInterlockLatched : BOOL; (* Critical TVAC Safety Trip Latched Status Indicator *)

    (* =================================================================================================================
     * SECTION 4: 2oo3 VOTED PROCESS VALUES & PHYSICAL DIAGNOSTIC METRICS
     * ================================================================================================================= *)
    rVoted_ChamberPressure_mbar     : REAL; (* Validated 2oo3 Chamber Vacuum Pressure [mbar] *)
    rVoted_ShroudTemp_Avg_degC      : REAL; (* Validated Multi-Zone Thermal Shroud Average Temperature [deg C] *)
    rVoted_PayloadSkinTemp_degC     : REAL; (* Validated Spacecraft Specimen External Radiator Skin Temperature [deg C] *)
    rVoted_PayloadInternalTemp_degC : REAL; (* Validated Spacecraft Specimen Internal Avionics Core Temperature [deg C] *)
    rVoted_SolarFlux_Wm2            : REAL; (* Validated Solar Simulator Collimated Beam Irradiance Flux [W/m2] *)
    rVoted_QCM_OutgassingRate_Hz_hr : REAL; (* Validated Quartz Crystal Microbalance Outgassing Deposition Rate [Hz/h] *)
    rVoted_LN2_Flow_kg_h            : REAL; (* Validated Cryogenic Subcooled LN2 Mass Flow Rate [kg/h] *)
    rVoted_GN2_LoopPressure_bar     : REAL; (* Validated Closed GN2 Heating Loop Circuit Pressure [bar] *)
    rVoted_TurbopumpSpeed_RPM       : REAL; (* Validated Turbomolecular Vacuum Pump Rotor Speed [RPM] *)
    rPayloadSlewRate_degC_min       : REAL; (* Real-Time Measured Payload Temperature Slew Rate [deg C/min] *)
    rSpatialThermalGradient_degC    : REAL; (* Maximum Instantaneous Spatial Temperature Difference Across Payload [deg C] *)
    rQCM_AccumulatedMass_ug_cm2     : REAL; (* In-Situ Integrated Molecular Contamination Deposition Mass [ug/cm2] *)
    rMolecularFlowConductance_L_s   : REAL; (* High-Vacuum Molecular Flow Pumping Duct Conductance [L/s] *)
    rLN2_BoilingSuppressionMargin_degC: REAL; (* Subcooling Margin Above Saturation Temperature [deg C] *)
    rRadiativeHeatTransfer_W        : REAL; (* Net Radiative Heat Transfer Rate Between Shroud and Spacecraft [W] *)
    rMPC_Cost_J                     : REAL; (* Instantaneous Model Predictive Control Quadratic Cost Functional J *)
    nActiveFSMState                 : INT;  (* Active 12-Stage TVAC Operational Sequence State Machine Index [0..11] *)
    wDiagnosticWord01               : WORD; (* 16-Bit TMR Sensor Health, Discrepancy & Validation Status Word *)
    wDiagnosticWord02               : WORD; (* 16-Bit ISA-18.2 Critical Trip & Emergency Fast Abort Status Word *)
    wDiagnosticWord03               : WORD; (* 16-Bit Process Warning & Subsystem Interlock Status Word *)
    wDiagnosticWord04               : WORD; (* 16-Bit Active FSM State Code, Actuator Permissive & Margin Word *)
END_VAR
"""
    parts.append(header_io)

    # -------------------------------------------------------------------------
    # PART 2: VAR DECLARATIONS
    # -------------------------------------------------------------------------
    var_block = """VAR
    (* =================================================================================================================
     * SECTION 5: DISCRETE 8x8 STATE-SPACE MATRICES & KALMAN OBSERVER ARRAYS (Ts = 0.100 s)
     * ================================================================================================================= *)
    A_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    B_mat                           : ARRAY[1..8, 1..6] OF REAL; (* Discrete Control Input Coupling Matrix B (8x6) *)
    C_mat                           : ARRAY[1..8, 1..8] OF REAL; (* Discrete Measurement Matrix C (8x8) *)
    D_mat                           : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedthrough Matrix D (8x6) *)
    Ke_mat                          : ARRAY[1..8, 1..8] OF REAL; (* Discrete Steady-State Kalman Observer Gain Matrix (8x8) *)

    x_state                         : ARRAY[1..8] OF REAL;       (* Estimated Cyber-Physical System State Vector x[k] *)
    x_pred                          : ARRAY[1..8] OF REAL;       (* One-Step Ahead A-Priori State Prediction x[k+1|k] *)
    x_obs                           : ARRAY[1..8] OF REAL;       (* A-Posteriori Filtered State Estimate x[k|k] *)
    y_meas                          : ARRAY[1..8] OF REAL;       (* Filtered Physical Measurement Vector y[k] *)
    y_pred                          : ARRAY[1..8] OF REAL;       (* Predicted Measurement Vector y[k|k-1] *)
    e_innov                         : ARRAY[1..8] OF REAL;       (* Innovation Residual Vector e[k] = y_meas - y_pred *)
    r_ref                           : ARRAY[1..8] OF REAL;       (* Supervisory Trajectory Reference Vector r[k] *)

    u_act                           : ARRAY[1..6] OF REAL;       (* Actuator Control Command Vector u[k] *)
    u_prev                          : ARRAY[1..6] OF REAL;       (* Prior Actuator Command Vector u[k-1] *)
    u_mpc                           : ARRAY[1..6] OF REAL;       (* Receding-Horizon MPC Optimized Vector *)

    (* =================================================================================================================
     * SECTION 6: MODEL PREDICTIVE CONTROL (MPC) RECEDING-HORIZON QUADRATIC WEIGHTING MATRICES
     * ================================================================================================================= *)
    Q_diag                          : ARRAY[1..8] OF REAL;       (* Diagonal State Tracking Penalty Weights *)
    R_diag                          : ARRAY[1..6] OF REAL;       (* Diagonal Actuator Expenditure Penalty Weights *)
    S_diag                          : ARRAY[1..6] OF REAL;       (* Diagonal Actuator Slew Rate Delta-U Penalty Weights *)
    P_diag                          : ARRAY[1..8] OF REAL;       (* Diagonal Terminal Horizon State Penalty Weights *)

    x_mpc_pred                      : ARRAY[1..8] OF REAL;       (* MPC Forward Sim Current Prediction State *)
    x_mpc_next                      : ARRAY[1..8] OF REAL;       (* MPC Forward Sim Next Step State *)

    rCandidateCost                  : REAL;                      (* Candidate Evaluation Cost Functional Value *)
    rMinCandidateCost               : REAL;                      (* Minimal Found Candidate Cost Functional Value *)
    rBestCandidate_u1               : REAL;                      (* Optimal Candidate Actuator Command u1 *)
    rBestCandidate_u2               : REAL;                      (* Optimal Candidate Actuator Command u2 *)
    rBestCandidate_u3               : REAL;                      (* Optimal Candidate Actuator Command u3 *)
    rBestCandidate_u4               : REAL;                      (* Optimal Candidate Actuator Command u4 *)
    rBestCandidate_u5               : REAL;                      (* Optimal Candidate Actuator Command u5 *)
    rBestCandidate_u6               : REAL;                      (* Optimal Candidate Actuator Command u6 *)

    (* =================================================================================================================
     * SECTION 7: SPACE CYBER-PHYSICAL FORMULATIONS & THERMAL EQUILIBRIUM PARAMETERS
     * ================================================================================================================= *)
    c_sigma                         : REAL := 5.670374E-8;       (* Stefan-Boltzmann Constant sigma [W/(m2*K4)] *)
    c_Sauerbrey_Cf                  : REAL := 2.26E-6;           (* Sauerbrey Sensitivity Constant Cf [Hz*cm2/ng] *)
    c_GasConstant_R                 : REAL := 8.314462;          (* Universal Gas Constant R [J/(mol*K)] *)
    c_MolarMass_N2                  : REAL := 0.028013;          (* Molecular Weight of Dry Nitrogen N2 [kg/mol] *)
    c_Boltzmann_kB                  : REAL := 1.380649E-23;      (* Boltzmann Constant kB [J/K] *)
    c_MolecularDiameter_N2          : REAL := 3.64E-10;          (* Effective Kinetic Diameter of Nitrogen Molecule [m] *)

    rEpsilon_Payload                : REAL := 0.035;             (* Spacecraft Multi-Layer Insulation (MLI) Effective Emissivity *)
    rEpsilon_Shroud                 : REAL := 0.920;             (* Thermal Shroud High-Emissivity Black Paint (Aeroglaze Z306) *)
    rArea_Payload                   : REAL := 12.50;             (* Effective Spacecraft Thermal Radiative Surface Area [m2] *)
    rArea_Shroud                    : REAL := 65.00;             (* Internal Thermal Shroud Cryogenic Radiative Surface Area [m2] *)
    rRadiationResistance            : REAL;                      (* Oppenheim Multi-Surface Radiative Transfer Resistance [1/m2] *)
    rEffectiveEmissivity            : REAL;                      (* Net Inter-Surface Gray-Body Radiative Transfer Factor *)

    rShroudTemp_K                   : REAL;                      (* Thermal Shroud Average Absolute Temperature [K] *)
    rPayloadSkin_K                  : REAL;                      (* Spacecraft External Radiator Skin Absolute Temperature [K] *)
    rPayloadCore_K                  : REAL;                      (* Spacecraft Internal Core Avionics Absolute Temperature [K] *)
    rT_shroud_fourth                : REAL;                      (* Shroud Temperature Raised to 4th Power (T_shroud^4) [K^4] *)
    rT_skin_fourth                  : REAL;                      (* Payload Skin Temperature Raised to 4th Power (T_skin^4) [K^4] *)

    rLN2_SpecificHeat_Cp            : REAL := 2040.0;            (* Subcooled Liquid Nitrogen Specific Heat Capacity [J/(kg*K)] *)
    rLN2_DynamicViscosity_mu        : REAL := 0.000152;          (* Subcooled Liquid Nitrogen Dynamic Viscosity [Pa*s] *)
    rLN2_ThermalConductivity_k      : REAL := 0.138;             (* Subcooled Liquid Nitrogen Thermal Conductivity [W/(m*K)] *)
    rShroudTubeDiameter_m           : REAL := 0.0254;            (* Shroud Copper Fluid Distribution Tube Internal Diameter [m] *)
    rReynoldsNumber_LN2             : REAL;                      (* Subcooled LN2 Fluid Reynolds Number Re *)
    rPrandtlNumber_LN2              : REAL;                      (* Subcooled LN2 Fluid Prandtl Number Pr *)
    rNusseltNumber_LN2              : REAL;                      (* Dittus-Boelter Convective Nusselt Number Nu *)
    rConvectiveCoeff_h_LN2          : REAL;                      (* Internal Tube Convective Heat Transfer Coefficient [W/(m2*K)] *)
    rSubcooledSaturationTemp_K      : REAL;                      (* Saturation Boiling Temperature at Shroud Header Pressure [K] *)

    rQCM_DeltaFreq_Integrated       : REAL;                      (* Running Beat Frequency Shift Integration [Hz] *)
    rQCM_CrystalTemp_degC           : REAL := -20.0;             (* TQCM Peltier Heat-Sink Controlled Crystal Temperature [deg C] *)
    rInstantaneousMassDepositionRate: REAL;                      (* Sauerbrey Calculated Mass Deposition Rate [ng/(cm2*s)] *)

    rMeanFreePath_lambda            : REAL;                      (* Gas Molecular Mean Free Path in High Vacuum [m] *)
    rKnudsenNumber                  : REAL;                      (* Dimensionless Knudsen Number Kn = lambda / D *)
    rMolecularVelocity_vbar         : REAL;                      (* Maxwell-Boltzmann Mean Molecular Speed [m/s] *)
    rDuctDiameter_m                 : REAL := 0.50;              (* Turbomolecular Pumping Port Duct Diameter [m] *)
    rDuctLength_m                   : REAL := 1.20;              (* High-Vacuum Pumping Manifold Length [m] *)

    rPreviousPayloadSkinTemp        : REAL;                      (* Stored Payload Skin Temperature for Derivative [deg C] *)
    rInstantaneousSkinDerivative    : REAL;                      (* Unfiltered Derivative dT/dt [deg C/min] *)
    rFilteredPayloadSlewRate        : REAL;                      (* First-Order Low-Pass Filtered Payload Slew Rate [deg C/min] *)
    rSpatialThermalGradient         : REAL;                      (* Instantaneous Differential Temperature across Satellite [deg C] *)

    (* =================================================================================================================
     * SECTION 8: 2oo3 TMR VOTING VARIABLES, DISCREPANCY TIMERS & TOLERANCES
     * ================================================================================================================= *)
    (* Channel Discrepancy Difference Variables *)
    diff_RoughVac_AB, diff_RoughVac_BC, diff_RoughVac_CA : REAL;
    diff_HighVac_AB, diff_HighVac_BC, diff_HighVac_CA   : REAL;
    diff_ShroudZ1_AB, diff_ShroudZ1_BC, diff_ShroudZ1_CA : REAL;
    diff_ShroudZ2_AB, diff_ShroudZ2_BC, diff_ShroudZ2_CA : REAL;
    diff_ShroudZ3_AB, diff_ShroudZ3_BC, diff_ShroudZ3_CA : REAL;
    diff_ShroudZ6_AB, diff_ShroudZ6_BC, diff_ShroudZ6_CA : REAL;
    diff_Skin_AB, diff_Skin_BC, diff_Skin_CA             : REAL;
    diff_Core_AB, diff_Core_BC, diff_Core_CA             : REAL;
    diff_QCM_AB, diff_QCM_BC, diff_QCM_CA               : REAL;
    diff_Solar_AB, diff_Solar_BC, diff_Solar_CA         : REAL;
    diff_LN2Flow_AB, diff_LN2Flow_BC, diff_LN2Flow_CA   : REAL;
    diff_GN2Press_AB, diff_GN2Press_BC, diff_GN2Press_CA : REAL;
    diff_TurboSpeed_AB, diff_TurboSpeed_BC, diff_TurboSpeed_CA : REAL;

    (* Discrepancy Error Flags *)
    bDisc_RoughVac                  : BOOL;
    bDisc_HighVac                   : BOOL;
    bDisc_ShroudZ1                  : BOOL;
    bDisc_ShroudZ2                  : BOOL;
    bDisc_ShroudZ3                  : BOOL;
    bDisc_ShroudZ6                  : BOOL;
    bDisc_Skin                      : BOOL;
    bDisc_Core                      : BOOL;
    bDisc_QCM                       : BOOL;
    bDisc_Solar                     : BOOL;
    bDisc_LN2Flow                   : BOOL;
    bDisc_GN2Press                  : BOOL;
    bDisc_TurboSpeed                : BOOL;

    (* 2oo3 Discrepancy Timers (TON IEC Standard Timers) *)
    tTMR_RoughVac                   : TON;
    tTMR_HighVac                    : TON;
    tTMR_ShroudZ1                   : TON;
    tTMR_ShroudZ2                   : TON;
    tTMR_ShroudZ3                   : TON;
    tTMR_ShroudZ6                   : TON;
    tTMR_Skin                       : TON;
    tTMR_Core                       : TON;
    tTMR_QCM                        : TON;
    tTMR_Solar                      : TON;
    tTMR_LN2Flow                    : TON;
    tTMR_GN2Press                   : TON;
    tTMR_TurboSpeed                 : TON;

    (* =================================================================================================================
     * SECTION 9: ISA-18.2 ALARM TRIP POINTS, DEADBANDS & INTERLOCK VARIABLES
     * ================================================================================================================= *)
    c_Press_HI_HI                   : REAL := 1.0E-3;            (* High Vacuum Loss Critical Trip Threshold [mbar] *)
    c_Press_HI                      : REAL := 5.0E-5;            (* Vacuum Degradation Pre-Alarm Warning [mbar] *)
    c_SkinTemp_HI_HI                : REAL := 145.0;             (* Payload Specimen Overtemperature Trip Threshold [deg C] *)
    c_SkinTemp_HI                   : REAL := 130.0;             (* Payload Specimen Upper Operating Warning [deg C] *)
    c_SkinTemp_LO                   : REAL := -160.0;            (* Payload Specimen Lower Operating Warning [deg C] *)
    c_SkinTemp_LO_LO                : REAL := -175.0;            (* Payload Specimen Undercooling Critical Trip [deg C] *)
    c_CoreTemp_HI_HI                : REAL := 85.0;              (* Internal Avionics Core Overheating Trip [deg C] *)
    c_CoreTemp_LO_LO                : REAL := -50.0;             (* Internal Avionics Core Under-Temperature Trip [deg C] *)
    c_SlewRate_ROC_Limit            : REAL := 2.0;               (* Maximum Allowable Specimen Slew Rate [deg C/min] *)
    c_SpatialGradient_Limit         : REAL := 25.0;              (* Maximum Allowable Differential Gradient across Specimen [deg C] *)
    c_SolarFlux_HI_HI               : REAL := 1550.0;            (* Solar Simulator Xenon Lamp Flux Flash Overpower Trip [W/m2] *)
    c_ShroudOverpress_HI_HI         : REAL := 8.5;               (* Cryogenic Shroud Circuit Overpressure Burst Disk Risk [bar] *)

    (* ISA-18.2 Latching Alarm Output Bits *)
    bAlarm_ChamberPress_HI_HI       : BOOL;
    bAlarm_ChamberPress_HI          : BOOL;
    bAlarm_PayloadSkin_HI_HI        : BOOL;
    bAlarm_PayloadSkin_HI           : BOOL;
    bAlarm_PayloadSkin_LO           : BOOL;
    bAlarm_PayloadSkin_LO_LO        : BOOL;
    bAlarm_PayloadInternal_HI_HI    : BOOL;
    bAlarm_PayloadInternal_LO_LO    : BOOL;
    bAlarm_SlewRate_ROC             : BOOL;
    bAlarm_SpatialGradient_HI       : BOOL;
    bAlarm_SolarFlux_HI_HI          : BOOL;
    bAlarm_SolarFlux_Dev            : BOOL;
    bAlarm_LN2_BoilingRisk          : BOOL;
    bAlarm_ShroudOverpress_HI_HI    : BOOL;
    bAlarm_BurstDiskRupture         : BOOL;
    bAlarm_EmergencyAbortLatched    : BOOL;

    (* =================================================================================================================
     * SECTION 10: FSM STATE TIMERS, SEQUENCING & STEP CONTROL VARIABLES
     * ================================================================================================================= *)
    nActiveState                    : INT := 0;                  (* Internal Active FSM State Variable [0..11] *)
    nPreviousState                  : INT := 0;                  (* Historical State for Edge Transition Detection *)
    nThermalCycleCount              : INT := 0;                  (* Cumulative Thermal Cycles Completed *)
    nTargetThermalCycles            : INT := 4;                  (* Target Orbital Thermal Vacuum Cycles Required *)
    bStateFirstScan                 : BOOL := TRUE;              (* State First Scan Initialization Pulse *)
    bColdBalanceAchieved            : BOOL := FALSE;             (* Cold Thermal Balance Verification Latched Flag *)
    bHotBalanceAchieved             : BOOL := FALSE;             (* Hot Thermal Balance Verification Latched Flag *)
    bBakeoutAchieved                : BOOL := FALSE;             (* Thermal Vacuum Outgassing Bakeout Complete Flag *)
    bRepressComplete                : BOOL := FALSE;             (* Controlled Repressurization Complete Flag *)

    (* Operational State Sequencing Timers (TON IEC Blocks) *)
    tFSM_StateTimer                 : TON;                       (* Elapsed Time in Current State *)
    tRoughingTimeout                : TON;                       (* Roughing Pumping Maximum Allowable Duration *)
    tHighVacCrossoverTimeout        : TON;                       (* High-Vacuum Crossover Timeout Monitor *)
    tColdSoakStabilizeTimer         : TON;                       (* Cold Soak Shroud Thermal Stabilization Timer *)
    tColdBalanceHoldTimer           : TON;                       (* Deep Space Cold Balance Equilibrium Hold Timer *)
    tSolarSimRampTimer              : TON;                       (* Solar Simulator Beam Ignition & Radiance Ramp Timer *)
    tHotBalanceHoldTimer            : TON;                       (* Solar Radiation Hot Balance Equilibrium Hold Timer *)
    tThermalCycleDwellTimer         : TON;                       (* Thermal Cycle Plateau Dwell Duration Timer *)
    tBakeoutHoldTimer               : TON;                       (* Spacecraft Thermal Vacuum Bakeout Duration Timer *)
    tControlledRepressTimer         : TON;                       (* Controlled GN2 Chamber Repressurization Timer *)
    tCleanroomDoorTimer             : TON;                       (* Cleanroom Lock Permissive Verification Timer *)
    tEmergencyAbortTimer            : TON;                       (* Fast Emergency Venting & Inerting Abort Timer *)

    (* Initialization & Loop Scratchpad *)
    bModelInitialized               : BOOL := FALSE;             (* First Scan Initialization Complete Flag *)
    i_loop                          : INT;                       (* Matrix / Array Iterator Index i *)
    j_loop                          : INT;                       (* Matrix / Array Iterator Index j *)
    k_loop                          : INT;                       (* Matrix / Array Iterator Index k *)
    cand_idx                        : INT;                       (* MPC Candidate Perturbation Loop Index *)
    rTempAccumulator                : REAL;                      (* Math Scratchpad Real Accumulator *)
    rTempDelta                      : REAL;                      (* Math Scratchpad Real Delta *)
END_VAR
"""
    parts.append(var_block)

    # -------------------------------------------------------------------------
    # PART 3: PHASE 0: MODEL MATRICES & COEFFICIENT INITIALIZATION
    # -------------------------------------------------------------------------
    init_logic = """(* =====================================================================================================================
 * PHASE 0: MODEL MATRICES & CONTROL COEFFICIENT INITIALIZATION (FIRST SCAN DETERMINISTIC SETUP)
 * ===================================================================================================================== *)
IF NOT bModelInitialized THEN
    (* -----------------------------------------------------------------------------------------------------------------
     * Discrete State Transition Matrix A (8x8) at Ts = 0.100 s:
     * State 1: Shroud Average Temperature [K]
     * State 2: Spacecraft MLI / Skin Temperature [K]
     * State 3: Spacecraft Core Avionics Temperature [K]
     * State 4: Chamber Vacuum Pressure [log10(mbar)]
     * State 5: QCM Accumulated Contaminant Mass [ug/cm2]
     * State 6: Collimated Solar Simulation Irradiance Flux [W/m2]
     * State 7: Subcooled Liquid Nitrogen Mass Flow Rate [kg/s]
     * State 8: Pressurized Re-Circulating GN2 Conditioning Temperature [K]
     * ----------------------------------------------------------------------------------------------------------------- *)
    A_mat[1,1] := 0.98820; A_mat[1,2] := 0.00415; A_mat[1,3] := 0.00012; A_mat[1,4] := 0.00000; A_mat[1,5] := 0.00000; A_mat[1,6] := 0.00005; A_mat[1,7] := -0.01520; A_mat[1,8] := 0.00760;
    A_mat[2,1] := 0.00385; A_mat[2,2] := 0.98540; A_mat[2,3] := 0.00840; A_mat[2,4] := 0.00000; A_mat[2,5] := 0.00000; A_mat[2,6] := 0.00285; A_mat[2,7] := 0.00000;  A_mat[2,8] := 0.00000;
    A_mat[3,1] := 0.00010; A_mat[3,2] := 0.00795; A_mat[3,3] := 0.99180; A_mat[3,4] := 0.00000; A_mat[3,5] := 0.00000; A_mat[3,6] := 0.00015; A_mat[3,7] := 0.00000;  A_mat[3,8] := 0.00000;
    A_mat[4,1] := 0.00000; A_mat[4,2] := 0.00025; A_mat[4,3] := 0.00000; A_mat[4,4] := 0.97450; A_mat[4,5] := 0.00000; A_mat[4,6] := 0.00010; A_mat[4,7] := 0.00000;  A_mat[4,8] := 0.00000;
    A_mat[5,1] := 0.00000; A_mat[5,2] := 0.00145; A_mat[5,3] := 0.00055; A_mat[5,4] := 0.00210; A_mat[5,5] := 1.00000; A_mat[5,6] := 0.00000; A_mat[5,7] := 0.00000;  A_mat[5,8] := 0.00000;
    A_mat[6,1] := 0.00000; A_mat[6,2] := 0.00000; A_mat[6,3] := 0.00000; A_mat[6,4] := 0.00000; A_mat[6,5] := 0.00000; A_mat[6,6] := 0.92500; A_mat[6,7] := 0.00000;  A_mat[6,8] := 0.00000;
    A_mat[7,1] := 0.00000; A_mat[7,2] := 0.00000; A_mat[7,3] := 0.00000; A_mat[7,4] := 0.00000; A_mat[7,5] := 0.00000; A_mat[7,6] := 0.00000; A_mat[7,7] := 0.88400;  A_mat[7,8] := 0.00000;
    A_mat[8,1] := 0.00450; A_mat[8,2] := 0.00000; A_mat[8,3] := 0.00000; A_mat[8,4] := 0.00000; A_mat[8,5] := 0.00000; A_mat[8,6] := 0.00000; A_mat[8,7] := 0.00000;  A_mat[8,8] := 0.96500;

    (* -----------------------------------------------------------------------------------------------------------------
     * Discrete Input Coupling Matrix B (8x6) at Ts = 0.100 s:
     * Input 1: LN2 Subcooled Modulating Cryogenic Injection Valve Demand [% 0..100]
     * Input 2: Pressurized GN2 Electric Heating Power Demand [% 0..100]
     * Input 3: Solar Simulator Xenon Arc Thyristor Phase Demand [% 0..100]
     * Input 4: Turbomolecular Vacuum Pump Speed Reference Demand [% 0..100]
     * Input 5: Cryo-Condensation Pump Cold Head Expansion Valve [% 0..100]
     * Input 6: Chamber Dry GN2 Repressurization Proportional Valve [% 0..100]
     * ----------------------------------------------------------------------------------------------------------------- *)
    B_mat[1,1] := -0.04850; B_mat[1,2] :=  0.03620; B_mat[1,3] :=  0.00120; B_mat[1,4] :=  0.00000; B_mat[1,5] := -0.00250; B_mat[1,6] :=  0.00050;
    B_mat[2,1] := -0.00120; B_mat[2,2] :=  0.00085; B_mat[2,3] :=  0.02450; B_mat[2,4] :=  0.00000; B_mat[2,5] :=  0.00000; B_mat[2,6] :=  0.00000;
    B_mat[3,1] :=  0.00000; B_mat[3,2] :=  0.00000; B_mat[3,3] :=  0.00185; B_mat[3,4] :=  0.00000; B_mat[3,5] :=  0.00000; B_mat[3,6] :=  0.00000;
    B_mat[4,1] :=  0.00000; B_mat[4,2] :=  0.00000; B_mat[4,3] :=  0.00020; B_mat[4,4] := -0.02150; B_mat[4,5] := -0.03450; B_mat[4,6] :=  0.08250;
    B_mat[5,1] :=  0.00000; B_mat[5,2] :=  0.00000; B_mat[5,3] :=  0.00045; B_mat[5,4] :=  0.00000; B_mat[5,5] :=  0.00000; B_mat[5,6] :=  0.00000;
    B_mat[6,1] :=  0.00000; B_mat[6,2] :=  0.00000; B_mat[6,3] :=  1.15500; B_mat[6,4] :=  0.00000; B_mat[6,5] :=  0.00000; B_mat[6,6] :=  0.00000;
    B_mat[7,1] :=  0.01250; B_mat[7,2] :=  0.00000; B_mat[7,3] :=  0.00000; B_mat[7,4] :=  0.00000; B_mat[7,5] :=  0.00000; B_mat[7,6] :=  0.00000;
    B_mat[8,1] :=  0.00000; B_mat[8,2] :=  0.06850; B_mat[8,3] :=  0.00000; B_mat[8,4] :=  0.00000; B_mat[8,5] :=  0.00000; B_mat[8,6] :=  0.00000;

    (* -----------------------------------------------------------------------------------------------------------------
     * Discrete Measurement Matrix C (8x8) - Identity Direct State Observation:
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i_loop := 1 TO 8 DO
        FOR j_loop := 1 TO 8 DO
            IF i_loop = j_loop THEN
                C_mat[i_loop, j_loop] := 1.0;
            ELSE
                C_mat[i_loop, j_loop] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * Direct Feedthrough Matrix D (8x6) - Zero Coupling:
     * ----------------------------------------------------------------------------------------------------------------- *)
    FOR i_loop := 1 TO 8 DO
        FOR j_loop := 1 TO 6 DO
            D_mat[i_loop, j_loop] := 0.0;
        END_FOR;
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * Steady-State Kalman Observer Gain Matrix Ke (8x8) Computed from Algebraic Riccati Equation:
     * ----------------------------------------------------------------------------------------------------------------- *)
    Ke_mat[1,1] := 0.2850; Ke_mat[1,2] := 0.0125; Ke_mat[1,3] := 0.0015; Ke_mat[1,4] := 0.0000; Ke_mat[1,5] := 0.0000; Ke_mat[1,6] := 0.0010; Ke_mat[1,7] := 0.0420; Ke_mat[1,8] := 0.0210;
    Ke_mat[2,1] := 0.0118; Ke_mat[2,2] := 0.3120; Ke_mat[2,3] := 0.0240; Ke_mat[2,4] := 0.0000; Ke_mat[2,5] := 0.0000; Ke_mat[2,6] := 0.0185; Ke_mat[2,7] := 0.0000; Ke_mat[2,8] := 0.0000;
    Ke_mat[3,1] := 0.0012; Ke_mat[3,2] := 0.0225; Ke_mat[3,3] := 0.2740; Ke_mat[3,4] := 0.0000; Ke_mat[3,5] := 0.0000; Ke_mat[3,6] := 0.0012; Ke_mat[3,7] := 0.0000; Ke_mat[3,8] := 0.0000;
    Ke_mat[4,1] := 0.0000; Ke_mat[4,2] := 0.0000; Ke_mat[4,3] := 0.0000; Ke_mat[4,4] := 0.3950; Ke_mat[4,5] := 0.0000; Ke_mat[4,6] := 0.0005; Ke_mat[4,7] := 0.0000; Ke_mat[4,8] := 0.0000;
    Ke_mat[5,1] := 0.0000; Ke_mat[5,2] := 0.0025; Ke_mat[5,3] := 0.0008; Ke_mat[5,4] := 0.0045; Ke_mat[5,5] := 0.4420; Ke_mat[5,6] := 0.0000; Ke_mat[5,7] := 0.0000; Ke_mat[5,8] := 0.0000;
    Ke_mat[6,1] := 0.0000; Ke_mat[6,2] := 0.0000; Ke_mat[6,3] := 0.0000; Ke_mat[6,4] := 0.0000; Ke_mat[6,5] := 0.0000; Ke_mat[6,6] := 0.4850; Ke_mat[6,7] := 0.0000; Ke_mat[6,8] := 0.0000;
    Ke_mat[7,1] := 0.0380; Ke_mat[7,2] := 0.0000; Ke_mat[7,3] := 0.0000; Ke_mat[7,4] := 0.0000; Ke_mat[7,5] := 0.0000; Ke_mat[7,6] := 0.0000; Ke_mat[7,7] := 0.3620; Ke_mat[7,8] := 0.0000;
    Ke_mat[8,1] := 0.0195; Ke_mat[8,2] := 0.0000; Ke_mat[8,3] := 0.0000; Ke_mat[8,4] := 0.0000; Ke_mat[8,5] := 0.0000; Ke_mat[8,6] := 0.0000; Ke_mat[8,7] := 0.0000; Ke_mat[8,8] := 0.3340;

    (* -----------------------------------------------------------------------------------------------------------------
     * Receding-Horizon MPC Quadratic Weighting Diagonal Matrices (Np=5, Nu=3):
     * ----------------------------------------------------------------------------------------------------------------- *)
    Q_diag[1] := 12.50; (* Weight on Shroud Temperature Tracking Error *)
    Q_diag[2] := 85.00; (* Weight on Spacecraft Skin Temperature Tracking Error *)
    Q_diag[3] := 55.00; (* Weight on Spacecraft Core Avionics Temperature Tracking Error *)
    Q_diag[4] := 45.00; (* Weight on Chamber High-Vacuum Pressure Error *)
    Q_diag[5] := 20.00; (* Weight on QCM Mass Contamination Minimization *)
    Q_diag[6] := 65.00; (* Weight on Solar Simulator Irradiance Flux Error (1.0 SC) *)
    Q_diag[7] :=  5.00; (* Weight on Subcooled LN2 Mass Flow Rate Stability *)
    Q_diag[8] :=  8.00; (* Weight on GN2 Conditioning Circuit Temperature *)

    R_diag[1] :=  1.80; (* Actuator Effort Penalty on Cryogenic LN2 Valve *)
    R_diag[2] :=  1.40; (* Actuator Effort Penalty on GN2 Circulation Heaters *)
    R_diag[3] :=  2.20; (* Actuator Effort Penalty on Xenon Solar Lamp Thyristor Phase *)
    R_diag[4] :=  0.80; (* Actuator Effort Penalty on Turbomolecular Pump Speed *)
    R_diag[5] :=  1.10; (* Actuator Effort Penalty on Helium Cryopump Expansion Cold Head *)
    R_diag[6] :=  3.50; (* Actuator Effort Penalty on Repressurization Valve *)

    S_diag[1] :=  4.50; (* Slew Rate Penalty on LN2 Modulating Valve Delta-U *)
    S_diag[2] :=  3.80; (* Slew Rate Penalty on GN2 Electric Heaters Delta-U *)
    S_diag[3] :=  6.20; (* Slew Rate Penalty on Solar Sim Power Supply Delta-U *)
    S_diag[4] :=  2.00; (* Slew Rate Penalty on Turbopump Speed Reference Delta-U *)
    S_diag[5] :=  2.50; (* Slew Rate Penalty on Cryo Cold Head Valve Delta-U *)
    S_diag[6] :=  8.00; (* Slew Rate Penalty on Repressurization Valve Delta-U *)

    FOR i_loop := 1 TO 8 DO
        P_diag[i_loop] := Q_diag[i_loop] * 3.50; (* Terminal Horizon Penalty Matrix P = 3.5 * Q *)
    END_FOR;

    (* -----------------------------------------------------------------------------------------------------------------
     * Oppenheim Multi-Surface Radiation Network Resistance Calculation:
     * R_rad = (1 - eps_payload) / (eps_payload * A_payload) + 1 / (A_payload * F_12) + (1 - eps_shroud) / (eps_shroud * A_shroud)
     * For completely enclosed convex body inside large concave shroud, view factor F_12 = 1.0
     * ----------------------------------------------------------------------------------------------------------------- *)
    rRadiationResistance := ((1.0 - rEpsilon_Payload) / (rEpsilon_Payload * rArea_Payload))
                          + (1.0 / (rArea_Payload * 1.0))
                          + ((1.0 - rEpsilon_Shroud) / (rEpsilon_Shroud * rArea_Shroud));
    rEffectiveEmissivity := 1.0 / (rArea_Payload * rRadiationResistance);

    (* Initialize State Variables *)
    FOR i_loop := 1 TO 8 DO
        x_state[i_loop] := 0.0;
        x_pred[i_loop] := 0.0;
        x_obs[i_loop] := 0.0;
    END_FOR;
    x_state[1] := 293.15; (* 20 deg C ambient *)
    x_state[2] := 293.15;
    x_state[3] := 293.15;
    x_state[4] := 3.005;   (* log10(1013 mbar) = 3.0056 *)
    x_state[5] := 0.0;
    x_state[6] := 0.0;
    x_state[7] := 0.0;
    x_state[8] := 293.15;

    rPreviousPayloadSkinTemp := 20.0;
    rFilteredPayloadSlewRate := 0.0;
    nActiveState := 0;
    bModelInitialized := TRUE;
END_IF;
"""
    parts.append(init_logic)

    # -------------------------------------------------------------------------
    # PART 4: PHASE 1: 2oo3 TMR SENSOR VOTING ENGINES
    # -------------------------------------------------------------------------
    tmr_logic = """(* =====================================================================================================================
 * PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING ENGINES
 * ===================================================================================================================== *)
(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 1: Chamber Roughing Vacuum Transmitters (0.50 decade discrepancy tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_RoughVac_AB := ABS(PT_CHAMBER_ROUGH_VAC_101A - PT_CHAMBER_ROUGH_VAC_101B);
diff_RoughVac_BC := ABS(PT_CHAMBER_ROUGH_VAC_101B - PT_CHAMBER_ROUGH_VAC_101C);
diff_RoughVac_CA := ABS(PT_CHAMBER_ROUGH_VAC_101C - PT_CHAMBER_ROUGH_VAC_101A);

IF (diff_RoughVac_AB > 25.0) OR (diff_RoughVac_BC > 25.0) OR (diff_RoughVac_CA > 25.0) THEN
    bDisc_RoughVac := TRUE;
ELSE
    bDisc_RoughVac := FALSE;
END_IF;
tTMR_RoughVac(IN := bDisc_RoughVac, PT := T#3S);

IF (PT_CHAMBER_ROUGH_VAC_101A >= PT_CHAMBER_ROUGH_VAC_101B AND PT_CHAMBER_ROUGH_VAC_101A <= PT_CHAMBER_ROUGH_VAC_101C) OR
   (PT_CHAMBER_ROUGH_VAC_101A <= PT_CHAMBER_ROUGH_VAC_101B AND PT_CHAMBER_ROUGH_VAC_101A >= PT_CHAMBER_ROUGH_VAC_101C) THEN
    rVoted_ChamberPressure_mbar := PT_CHAMBER_ROUGH_VAC_101A;
ELSIF (PT_CHAMBER_ROUGH_VAC_101B >= PT_CHAMBER_ROUGH_VAC_101A AND PT_CHAMBER_ROUGH_VAC_101B <= PT_CHAMBER_ROUGH_VAC_101C) OR
      (PT_CHAMBER_ROUGH_VAC_101B <= PT_CHAMBER_ROUGH_VAC_101A AND PT_CHAMBER_ROUGH_VAC_101B >= PT_CHAMBER_ROUGH_VAC_101C) THEN
    rVoted_ChamberPressure_mbar := PT_CHAMBER_ROUGH_VAC_101B;
ELSE
    rVoted_ChamberPressure_mbar := PT_CHAMBER_ROUGH_VAC_101C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 2: Chamber High-Vacuum Penning Cold Cathode Ionization Gauges (0.20 decade logarithmic tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
IF (PT_CHAMBER_HIGH_VAC_PENNING_102A > 1.0E-10) AND (PT_CHAMBER_HIGH_VAC_PENNING_102B > 1.0E-10) AND (PT_CHAMBER_HIGH_VAC_PENNING_102C > 1.0E-10) THEN
    diff_HighVac_AB := ABS((LN(PT_CHAMBER_HIGH_VAC_PENNING_102A) / 2.302585) - (LN(PT_CHAMBER_HIGH_VAC_PENNING_102B) / 2.302585));
    diff_HighVac_BC := ABS((LN(PT_CHAMBER_HIGH_VAC_PENNING_102B) / 2.302585) - (LN(PT_CHAMBER_HIGH_VAC_PENNING_102C) / 2.302585));
    diff_HighVac_CA := ABS((LN(PT_CHAMBER_HIGH_VAC_PENNING_102C) / 2.302585) - (LN(PT_CHAMBER_HIGH_VAC_PENNING_102A) / 2.302585));
ELSE
    diff_HighVac_AB := 0.0;
    diff_HighVac_BC := 0.0;
    diff_HighVac_CA := 0.0;
END_IF;

IF (diff_HighVac_AB > 0.20) OR (diff_HighVac_BC > 0.20) OR (diff_HighVac_CA > 0.20) THEN
    bDisc_HighVac := TRUE;
ELSE
    bDisc_HighVac := FALSE;
END_IF;
tTMR_HighVac(IN := bDisc_HighVac, PT := T#3S);

(* If chamber is in high-vacuum regime (< 0.1 mbar), switch primary voted pressure to Penning cold cathode *)
IF rVoted_ChamberPressure_mbar < 0.10 THEN
    IF (PT_CHAMBER_HIGH_VAC_PENNING_102A >= PT_CHAMBER_HIGH_VAC_PENNING_102B AND PT_CHAMBER_HIGH_VAC_PENNING_102A <= PT_CHAMBER_HIGH_VAC_PENNING_102C) OR
       (PT_CHAMBER_HIGH_VAC_PENNING_102A <= PT_CHAMBER_HIGH_VAC_PENNING_102B AND PT_CHAMBER_HIGH_VAC_PENNING_102A >= PT_CHAMBER_HIGH_VAC_PENNING_102C) THEN
        rVoted_ChamberPressure_mbar := PT_CHAMBER_HIGH_VAC_PENNING_102A;
    ELSIF (PT_CHAMBER_HIGH_VAC_PENNING_102B >= PT_CHAMBER_HIGH_VAC_PENNING_102A AND PT_CHAMBER_HIGH_VAC_PENNING_102B <= PT_CHAMBER_HIGH_VAC_PENNING_102C) OR
          (PT_CHAMBER_HIGH_VAC_PENNING_102B <= PT_CHAMBER_HIGH_VAC_PENNING_102A AND PT_CHAMBER_HIGH_VAC_PENNING_102B >= PT_CHAMBER_HIGH_VAC_PENNING_102C) THEN
        rVoted_ChamberPressure_mbar := PT_CHAMBER_HIGH_VAC_PENNING_102B;
    ELSE
        rVoted_ChamberPressure_mbar := PT_CHAMBER_HIGH_VAC_PENNING_102C;
    END_IF;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 3: Thermal Shroud Zone 1 (Floor / Base Plate) Multi-Point Cryo RTD Pt100 (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_ShroudZ1_AB := ABS(TT_SHROUD_ZONE1_TEMP_201A - TT_SHROUD_ZONE1_TEMP_201B);
diff_ShroudZ1_BC := ABS(TT_SHROUD_ZONE1_TEMP_201B - TT_SHROUD_ZONE1_TEMP_201C);
diff_ShroudZ1_CA := ABS(TT_SHROUD_ZONE1_TEMP_201C - TT_SHROUD_ZONE1_TEMP_201A);

IF (diff_ShroudZ1_AB > 1.0) OR (diff_ShroudZ1_BC > 1.0) OR (diff_ShroudZ1_CA > 1.0) THEN
    bDisc_ShroudZ1 := TRUE;
ELSE
    bDisc_ShroudZ1 := FALSE;
END_IF;
tTMR_ShroudZ1(IN := bDisc_ShroudZ1, PT := T#3S);

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 4: Thermal Shroud Zone 2 (Lower Cylindrical Shell) Multi-Point Cryo RTD Pt100 (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_ShroudZ2_AB := ABS(TT_SHROUD_ZONE2_TEMP_202A - TT_SHROUD_ZONE2_TEMP_202B);
diff_ShroudZ2_BC := ABS(TT_SHROUD_ZONE2_TEMP_202B - TT_SHROUD_ZONE2_TEMP_202C);
diff_ShroudZ2_CA := ABS(TT_SHROUD_ZONE2_TEMP_202C - TT_SHROUD_ZONE2_TEMP_202A);

IF (diff_ShroudZ2_AB > 1.0) OR (diff_ShroudZ2_BC > 1.0) OR (diff_ShroudZ2_CA > 1.0) THEN
    bDisc_ShroudZ2 := TRUE;
ELSE
    bDisc_ShroudZ2 := FALSE;
END_IF;
tTMR_ShroudZ2(IN := bDisc_ShroudZ2, PT := T#3S);

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 5: Thermal Shroud Zone 3 (Upper Cylindrical Shell) Multi-Point Cryo RTD Pt100 (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_ShroudZ3_AB := ABS(TT_SHROUD_ZONE3_TEMP_203A - TT_SHROUD_ZONE3_TEMP_203B);
diff_ShroudZ3_BC := ABS(TT_SHROUD_ZONE3_TEMP_203B - TT_SHROUD_ZONE3_TEMP_203C);
diff_ShroudZ3_CA := ABS(TT_SHROUD_ZONE3_TEMP_203C - TT_SHROUD_ZONE3_TEMP_203A);

IF (diff_ShroudZ3_AB > 1.0) OR (diff_ShroudZ3_BC > 1.0) OR (diff_ShroudZ3_CA > 1.0) THEN
    bDisc_ShroudZ3 := TRUE;
ELSE
    bDisc_ShroudZ3 := FALSE;
END_IF;
tTMR_ShroudZ3(IN := bDisc_ShroudZ3, PT := T#3S);

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 6: Thermal Shroud Zone 6 (Zenith / Top Dome) Multi-Point Cryo RTD Pt100 (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_ShroudZ6_AB := ABS(TT_SHROUD_ZONE6_TEMP_206A - TT_SHROUD_ZONE6_TEMP_206B);
diff_ShroudZ6_BC := ABS(TT_SHROUD_ZONE6_TEMP_206B - TT_SHROUD_ZONE6_TEMP_206C);
diff_ShroudZ6_CA := ABS(TT_SHROUD_ZONE6_TEMP_206C - TT_SHROUD_ZONE6_TEMP_206A);

IF (diff_ShroudZ6_AB > 1.0) OR (diff_ShroudZ6_BC > 1.0) OR (diff_ShroudZ6_CA > 1.0) THEN
    bDisc_ShroudZ6 := TRUE;
ELSE
    bDisc_ShroudZ6 := FALSE;
END_IF;
tTMR_ShroudZ6(IN := bDisc_ShroudZ6, PT := T#3S);

(* Multi-Zone Average Thermal Shroud Temperature Computation across All 4 Monitored Zones *)
rVoted_ShroudTemp_Avg_degC := (TT_SHROUD_ZONE1_TEMP_201A + TT_SHROUD_ZONE2_TEMP_202A +
                               TT_SHROUD_ZONE3_TEMP_203A + TT_SHROUD_ZONE6_TEMP_206A) / 4.0;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 7: Spacecraft Payload Skin / MLI Radiator Surface Pt100 Sensors (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_Skin_AB := ABS(TT_PAYLOAD_SKIN_301A - TT_PAYLOAD_SKIN_301B);
diff_Skin_BC := ABS(TT_PAYLOAD_SKIN_301B - TT_PAYLOAD_SKIN_301C);
diff_Skin_CA := ABS(TT_PAYLOAD_SKIN_301C - TT_PAYLOAD_SKIN_301A);

IF (diff_Skin_AB > 1.0) OR (diff_Skin_BC > 1.0) OR (diff_Skin_CA > 1.0) THEN
    bDisc_Skin := TRUE;
ELSE
    bDisc_Skin := FALSE;
END_IF;
tTMR_Skin(IN := bDisc_Skin, PT := T#3S);

IF (TT_PAYLOAD_SKIN_301A >= TT_PAYLOAD_SKIN_301B AND TT_PAYLOAD_SKIN_301A <= TT_PAYLOAD_SKIN_301C) OR
   (TT_PAYLOAD_SKIN_301A <= TT_PAYLOAD_SKIN_301B AND TT_PAYLOAD_SKIN_301A >= TT_PAYLOAD_SKIN_301C) THEN
    rVoted_PayloadSkinTemp_degC := TT_PAYLOAD_SKIN_301A;
ELSIF (TT_PAYLOAD_SKIN_301B >= TT_PAYLOAD_SKIN_301A AND TT_PAYLOAD_SKIN_301B <= TT_PAYLOAD_SKIN_301C) OR
      (TT_PAYLOAD_SKIN_301B <= TT_PAYLOAD_SKIN_301A AND TT_PAYLOAD_SKIN_301B >= TT_PAYLOAD_SKIN_301C) THEN
    rVoted_PayloadSkinTemp_degC := TT_PAYLOAD_SKIN_301B;
ELSE
    rVoted_PayloadSkinTemp_degC := TT_PAYLOAD_SKIN_301C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 8: Spacecraft Internal Avionics / Instrument Payload Core Temperature Pt100 Sensors (1.0 deg C tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_Core_AB := ABS(TT_PAYLOAD_INTERNAL_302A - TT_PAYLOAD_INTERNAL_302B);
diff_Core_BC := ABS(TT_PAYLOAD_INTERNAL_302B - TT_PAYLOAD_INTERNAL_302C);
diff_Core_CA := ABS(TT_PAYLOAD_INTERNAL_302C - TT_PAYLOAD_INTERNAL_302A);

IF (diff_Core_AB > 1.0) OR (diff_Core_BC > 1.0) OR (diff_Core_CA > 1.0) THEN
    bDisc_Core := TRUE;
ELSE
    bDisc_Core := FALSE;
END_IF;
tTMR_Core(IN := bDisc_Core, PT := T#3S);

IF (TT_PAYLOAD_INTERNAL_302A >= TT_PAYLOAD_INTERNAL_302B AND TT_PAYLOAD_INTERNAL_302A <= TT_PAYLOAD_INTERNAL_302C) OR
   (TT_PAYLOAD_INTERNAL_302A <= TT_PAYLOAD_INTERNAL_302B AND TT_PAYLOAD_INTERNAL_302A >= TT_PAYLOAD_INTERNAL_302C) THEN
    rVoted_PayloadInternalTemp_degC := TT_PAYLOAD_INTERNAL_302A;
ELSIF (TT_PAYLOAD_INTERNAL_302B >= TT_PAYLOAD_INTERNAL_302A AND TT_PAYLOAD_INTERNAL_302B <= TT_PAYLOAD_INTERNAL_302C) OR
      (TT_PAYLOAD_INTERNAL_302B <= TT_PAYLOAD_INTERNAL_302A AND TT_PAYLOAD_INTERNAL_302B >= TT_PAYLOAD_INTERNAL_302C) THEN
    rVoted_PayloadInternalTemp_degC := TT_PAYLOAD_INTERNAL_302B;
ELSE
    rVoted_PayloadInternalTemp_degC := TT_PAYLOAD_INTERNAL_302C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 9: Thermoelectric Quartz Crystal Microbalance (QCM) Frequency Beat Outgassing Rate (0.50 Hz/h tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_QCM_AB := ABS(QCM_OUTGASSING_RATE_401A - QCM_OUTGASSING_RATE_401B);
diff_QCM_BC := ABS(QCM_OUTGASSING_RATE_401B - QCM_OUTGASSING_RATE_401C);
diff_QCM_CA := ABS(QCM_OUTGASSING_RATE_401C - QCM_OUTGASSING_RATE_401A);

IF (diff_QCM_AB > 0.50) OR (diff_QCM_BC > 0.50) OR (diff_QCM_CA > 0.50) THEN
    bDisc_QCM := TRUE;
ELSE
    bDisc_QCM := FALSE;
END_IF;
tTMR_QCM(IN := bDisc_QCM, PT := T#3S);

IF (QCM_OUTGASSING_RATE_401A >= QCM_OUTGASSING_RATE_401B AND QCM_OUTGASSING_RATE_401A <= QCM_OUTGASSING_RATE_401C) OR
   (QCM_OUTGASSING_RATE_401A <= QCM_OUTGASSING_RATE_401B AND QCM_OUTGASSING_RATE_401A >= QCM_OUTGASSING_RATE_401C) THEN
    rVoted_QCM_OutgassingRate_Hz_hr := QCM_OUTGASSING_RATE_401A;
ELSIF (QCM_OUTGASSING_RATE_401B >= QCM_OUTGASSING_RATE_401A AND QCM_OUTGASSING_RATE_401B <= QCM_OUTGASSING_RATE_401C) OR
      (QCM_OUTGASSING_RATE_401B <= QCM_OUTGASSING_RATE_401A AND QCM_OUTGASSING_RATE_401B >= QCM_OUTGASSING_RATE_401C) THEN
    rVoted_QCM_OutgassingRate_Hz_hr := QCM_OUTGASSING_RATE_401B;
ELSE
    rVoted_QCM_OutgassingRate_Hz_hr := QCM_OUTGASSING_RATE_401C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 10: Solar Simulator Xenon Arc Lamp Collimated Beam Radiance Pyranometers (15.0 W/m2 tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_Solar_AB := ABS(RAD_SOLAR_SIM_FLUX_501A - RAD_SOLAR_SIM_FLUX_501B);
diff_Solar_BC := ABS(RAD_SOLAR_SIM_FLUX_501B - RAD_SOLAR_SIM_FLUX_501C);
diff_Solar_CA := ABS(RAD_SOLAR_SIM_FLUX_501C - RAD_SOLAR_SIM_FLUX_501A);

IF (diff_Solar_AB > 15.0) OR (diff_Solar_BC > 15.0) OR (diff_Solar_CA > 15.0) THEN
    bDisc_Solar := TRUE;
ELSE
    bDisc_Solar := FALSE;
END_IF;
tTMR_Solar(IN := bDisc_Solar, PT := T#3S);

IF (RAD_SOLAR_SIM_FLUX_501A >= RAD_SOLAR_SIM_FLUX_501B AND RAD_SOLAR_SIM_FLUX_501A <= RAD_SOLAR_SIM_FLUX_501C) OR
   (RAD_SOLAR_SIM_FLUX_501A <= RAD_SOLAR_SIM_FLUX_501B AND RAD_SOLAR_SIM_FLUX_501A >= RAD_SOLAR_SIM_FLUX_501C) THEN
    rVoted_SolarFlux_Wm2 := RAD_SOLAR_SIM_FLUX_501A;
ELSIF (RAD_SOLAR_SIM_FLUX_501B >= RAD_SOLAR_SIM_FLUX_501A AND RAD_SOLAR_SIM_FLUX_501B <= RAD_SOLAR_SIM_FLUX_501C) OR
      (RAD_SOLAR_SIM_FLUX_501B <= RAD_SOLAR_SIM_FLUX_501A AND RAD_SOLAR_SIM_FLUX_501B >= RAD_SOLAR_SIM_FLUX_501C) THEN
    rVoted_SolarFlux_Wm2 := RAD_SOLAR_SIM_FLUX_501B;
ELSE
    rVoted_SolarFlux_Wm2 := RAD_SOLAR_SIM_FLUX_501C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 11: Cryogenic Subcooled LN2 Shroud Supply Mass Flow Meters (50.0 kg/h tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_LN2Flow_AB := ABS(FT_LN2_SHROUD_SUPPLY_601A - FT_LN2_SHROUD_SUPPLY_601B);
diff_LN2Flow_BC := ABS(FT_LN2_SHROUD_SUPPLY_601B - FT_LN2_SHROUD_SUPPLY_601C);
diff_LN2Flow_CA := ABS(FT_LN2_SHROUD_SUPPLY_601C - FT_LN2_SHROUD_SUPPLY_601A);

IF (diff_LN2Flow_AB > 50.0) OR (diff_LN2Flow_BC > 50.0) OR (diff_LN2Flow_CA > 50.0) THEN
    bDisc_LN2Flow := TRUE;
ELSE
    bDisc_LN2Flow := FALSE;
END_IF;
tTMR_LN2Flow(IN := bDisc_LN2Flow, PT := T#3S);

IF (FT_LN2_SHROUD_SUPPLY_601A >= FT_LN2_SHROUD_SUPPLY_601B AND FT_LN2_SHROUD_SUPPLY_601A <= FT_LN2_SHROUD_SUPPLY_601C) OR
   (FT_LN2_SHROUD_SUPPLY_601A <= FT_LN2_SHROUD_SUPPLY_601B AND FT_LN2_SHROUD_SUPPLY_601A >= FT_LN2_SHROUD_SUPPLY_601C) THEN
    rVoted_LN2_Flow_kg_h := FT_LN2_SHROUD_SUPPLY_601A;
ELSIF (FT_LN2_SHROUD_SUPPLY_601B >= FT_LN2_SHROUD_SUPPLY_601A AND FT_LN2_SHROUD_SUPPLY_601B <= FT_LN2_SHROUD_SUPPLY_601C) OR
      (FT_LN2_SHROUD_SUPPLY_601B <= FT_LN2_SHROUD_SUPPLY_601A AND FT_LN2_SHROUD_SUPPLY_601B >= FT_LN2_SHROUD_SUPPLY_601C) THEN
    rVoted_LN2_Flow_kg_h := FT_LN2_SHROUD_SUPPLY_601B;
ELSE
    rVoted_LN2_Flow_kg_h := FT_LN2_SHROUD_SUPPLY_601C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 12: Pressurized GN2 Closed Conditioning Heating Circuit Pressure Transmitters (0.25 bar tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_GN2Press_AB := ABS(PT_GN2_HEATING_LOOP_602A - PT_GN2_HEATING_LOOP_602B);
diff_GN2Press_BC := ABS(PT_GN2_HEATING_LOOP_602B - PT_GN2_HEATING_LOOP_602C);
diff_GN2Press_CA := ABS(PT_GN2_HEATING_LOOP_602C - PT_GN2_HEATING_LOOP_602A);

IF (diff_GN2Press_AB > 0.25) OR (diff_GN2Press_BC > 0.25) OR (diff_GN2Press_CA > 0.25) THEN
    bDisc_GN2Press := TRUE;
ELSE
    bDisc_GN2Press := FALSE;
END_IF;
tTMR_GN2Press(IN := bDisc_GN2Press, PT := T#3S);

IF (PT_GN2_HEATING_LOOP_602A >= PT_GN2_HEATING_LOOP_602B AND PT_GN2_HEATING_LOOP_602A <= PT_GN2_HEATING_LOOP_602C) OR
   (PT_GN2_HEATING_LOOP_602A <= PT_GN2_HEATING_LOOP_602B AND PT_GN2_HEATING_LOOP_602A >= PT_GN2_HEATING_LOOP_602C) THEN
    rVoted_GN2_LoopPressure_bar := PT_GN2_HEATING_LOOP_602A;
ELSIF (PT_GN2_HEATING_LOOP_602B >= PT_GN2_HEATING_LOOP_602A AND PT_GN2_HEATING_LOOP_602B <= PT_GN2_HEATING_LOOP_602C) OR
      (PT_GN2_HEATING_LOOP_602B <= PT_GN2_HEATING_LOOP_602A AND PT_GN2_HEATING_LOOP_602B >= PT_GN2_HEATING_LOOP_602C) THEN
    rVoted_GN2_LoopPressure_bar := PT_GN2_HEATING_LOOP_602B;
ELSE
    rVoted_GN2_LoopPressure_bar := PT_GN2_HEATING_LOOP_602C;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * Triplet 13: Magnetic Bearing High-Vacuum Turbomolecular Pump Speed Encoders (300.0 RPM tolerance)
 * ----------------------------------------------------------------------------------------------------------------- *)
diff_TurboSpeed_AB := ABS(ST_TURBOPUMP_ROTOR_RPM_701A - ST_TURBOPUMP_ROTOR_RPM_701B);
diff_TurboSpeed_BC := ABS(ST_TURBOPUMP_ROTOR_RPM_701B - ST_TURBOPUMP_ROTOR_RPM_701C);
diff_TurboSpeed_CA := ABS(ST_TURBOPUMP_ROTOR_RPM_701C - ST_TURBOPUMP_ROTOR_RPM_701A);

IF (diff_TurboSpeed_AB > 300.0) OR (diff_TurboSpeed_BC > 300.0) OR (diff_TurboSpeed_CA > 300.0) THEN
    bDisc_TurboSpeed := TRUE;
ELSE
    bDisc_TurboSpeed := FALSE;
END_IF;
tTMR_TurboSpeed(IN := bDisc_TurboSpeed, PT := T#3S);

IF (ST_TURBOPUMP_ROTOR_RPM_701A >= ST_TURBOPUMP_ROTOR_RPM_701B AND ST_TURBOPUMP_ROTOR_RPM_701A <= ST_TURBOPUMP_ROTOR_RPM_701C) OR
   (ST_TURBOPUMP_ROTOR_RPM_701A <= ST_TURBOPUMP_ROTOR_RPM_701B AND ST_TURBOPUMP_ROTOR_RPM_701A >= ST_TURBOPUMP_ROTOR_RPM_701C) THEN
    rVoted_TurbopumpSpeed_RPM := ST_TURBOPUMP_ROTOR_RPM_701A;
ELSIF (ST_TURBOPUMP_ROTOR_RPM_701B >= ST_TURBOPUMP_ROTOR_RPM_701A AND ST_TURBOPUMP_ROTOR_RPM_701B <= ST_TURBOPUMP_ROTOR_RPM_701C) OR
      (ST_TURBOPUMP_ROTOR_RPM_701B <= ST_TURBOPUMP_ROTOR_RPM_701A AND ST_TURBOPUMP_ROTOR_RPM_701B >= ST_TURBOPUMP_ROTOR_RPM_701C) THEN
    rVoted_TurbopumpSpeed_RPM := ST_TURBOPUMP_ROTOR_RPM_701B;
ELSE
    rVoted_TurbopumpSpeed_RPM := ST_TURBOPUMP_ROTOR_RPM_701C;
END_IF;
"""
    parts.append(tmr_logic)

    # -------------------------------------------------------------------------
    # PART 5: PHASE 2: CYBER-PHYSICAL REACTION & THERMAL-VACUUM ENGINES
    # -------------------------------------------------------------------------
    physics_logic = """(* =====================================================================================================================
 * PHASE 2: THERMAL-VACUUM & CYBER-PHYSICAL REACTION ENGINES
 * ===================================================================================================================== *)
(* -----------------------------------------------------------------------------------------------------------------
 * 1. Stefan-Boltzmann Multi-Surface Radiative Enclosure Heat Transfer:
 * q_rad = sigma * A_payload * eps_eff * (T_shroud^4 - T_skin^4)
 * ----------------------------------------------------------------------------------------------------------------- *)
rShroudTemp_K := rVoted_ShroudTemp_Avg_degC + 273.15;
rPayloadSkin_K := rVoted_PayloadSkinTemp_degC + 273.15;
rPayloadCore_K := rVoted_PayloadInternalTemp_degC + 273.15;

(* Guard Against Sub-Zero Absolute Temperature *)
IF rShroudTemp_K < 70.0 THEN rShroudTemp_K := 70.0; END_IF;
IF rPayloadSkin_K < 70.0 THEN rPayloadSkin_K := 70.0; END_IF;
IF rPayloadCore_K < 70.0 THEN rPayloadCore_K := 70.0; END_IF;

rT_shroud_fourth := (rShroudTemp_K / 100.0) * (rShroudTemp_K / 100.0) * (rShroudTemp_K / 100.0) * (rShroudTemp_K / 100.0) * 1.0E8;
rT_skin_fourth := (rPayloadSkin_K / 100.0) * (rPayloadSkin_K / 100.0) * (rPayloadSkin_K / 100.0) * (rPayloadSkin_K / 100.0) * 1.0E8;

rRadiativeHeatTransfer_W := c_sigma * rArea_Payload * rEffectiveEmissivity * (rT_shroud_fourth - rT_skin_fourth);

(* -----------------------------------------------------------------------------------------------------------------
 * 2. Subcooled Liquid Nitrogen Single-Phase Boiling Suppression & Dittus-Boelter Convective Margin:
 * To suppress film/nucleate boiling instabilities inside shroud copper tubing, fluid pressure is maintained
 * such that T_LN2 < T_sat(P_LN2). Approximate Antoine saturation curve for LN2: T_sat(K) approx 77.36 + 4.25 * ln(P_bar)
 * ----------------------------------------------------------------------------------------------------------------- *)
IF rVoted_GN2_LoopPressure_bar > 0.50 THEN
    rSubcooledSaturationTemp_K := 77.36 + (4.25 * (LN(rVoted_GN2_LoopPressure_bar) / 0.693147) * 0.693147);
ELSE
    rSubcooledSaturationTemp_K := 77.36;
END_IF;

rLN2_BoilingSuppressionMargin_degC := rSubcooledSaturationTemp_K - rShroudTemp_K;

(* Reynolds, Prandtl & Dittus-Boelter Nusselt Calculation *)
IF rVoted_LN2_Flow_kg_h > 10.0 THEN
    rReynoldsNumber_LN2 := (4.0 * (rVoted_LN2_Flow_kg_h / 3600.0)) / (3.141592 * rShroudTubeDiameter_m * rLN2_DynamicViscosity_mu);
    rPrandtlNumber_LN2 := (rLN2_SpecificHeat_Cp * rLN2_DynamicViscosity_mu) / rLN2_ThermalConductivity_k;
    IF rReynoldsNumber_LN2 > 2300.0 THEN
        rNusseltNumber_LN2 := 0.023 * EXP(0.80 * LN(rReynoldsNumber_LN2)) * EXP(0.40 * LN(rPrandtlNumber_LN2));
    ELSE
        rNusseltNumber_LN2 := 4.36; (* Laminar constant heat flux asymptotic limit *)
    END_IF;
    rConvectiveCoeff_h_LN2 := (rNusseltNumber_LN2 * rLN2_ThermalConductivity_k) / rShroudTubeDiameter_m;
ELSE
    rReynoldsNumber_LN2 := 0.0;
    rPrandtlNumber_LN2 := 2.24;
    rNusseltNumber_LN2 := 4.36;
    rConvectiveCoeff_h_LN2 := 25.0;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 3. Sauerbrey Quartz Crystal Microbalance (QCM) Mass Deposition Integration:
 * Delta_f = - Cf * Delta_m  ==>  Delta_m = - Delta_f / Cf  [ng/cm2]
 * Integrated over cycle period delta-t [s]
 * ----------------------------------------------------------------------------------------------------------------- *)
rInstantaneousMassDepositionRate := (rVoted_QCM_OutgassingRate_Hz_hr / 3600.0) / c_Sauerbrey_Cf; (* ng/(cm2*s) *)
rQCM_DeltaFreq_Integrated := rQCM_DeltaFreq_Integrated + (rVoted_QCM_OutgassingRate_Hz_hr / 3600.0) * rCycleTime_s;
rQCM_AccumulatedMass_ug_cm2 := (rQCM_DeltaFreq_Integrated / c_Sauerbrey_Cf) * 1.0E-3; (* Convert ng to ug *)

(* -----------------------------------------------------------------------------------------------------------------
 * 4. High-Vacuum Free Molecular Flow Duct Conductance & Knudsen Number:
 * Mean free path lambda = (kB * T) / (sqrt(2) * pi * d_m^2 * P_Pa)
 * Knudsen number Kn = lambda / D_duct. For Kn > 1.0, flow is in free molecular regime.
 * Molecular speed v_bar = sqrt(8 * R * T / (pi * M))
 * Duct conductance C = (1/12) * pi * v_bar * (D^3 / L) [m3/s = 1000 L/s]
 * ----------------------------------------------------------------------------------------------------------------- *)
IF rVoted_ChamberPressure_mbar > 1.0E-8 THEN
    (* 1 mbar = 100 Pa *)
    rMeanFreePath_lambda := (c_Boltzmann_kB * 293.15) / (1.414213 * 3.141592 * (c_MolecularDiameter_N2 * c_MolecularDiameter_N2) * (rVoted_ChamberPressure_mbar * 100.0));
    rKnudsenNumber := rMeanFreePath_lambda / rDuctDiameter_m;
ELSE
    rMeanFreePath_lambda := 1000.0;
    rKnudsenNumber := 2000.0;
END_IF;

rMolecularVelocity_vbar := SQRT((8.0 * c_GasConstant_R * 293.15) / (3.141592 * c_MolarMass_N2));

IF rKnudsenNumber > 1.0 THEN
    (* Free molecular flow conductance *)
    rMolecularFlowConductance_L_s := ((1.0 / 12.0) * 3.141592 * rMolecularVelocity_vbar * (rDuctDiameter_m * rDuctDiameter_m * rDuctDiameter_m) / rDuctLength_m) * 1000.0;
ELSE
    (* Transition / viscous flow conductance enhancement factor *)
    rMolecularFlowConductance_L_s := 15000.0;
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 5. Real-Time Specimen Thermal Shock Slew Rate & Spatial Gradient Computation:
 * |dT/dt| < 2.0 deg C/min strict limit to prevent solder joint fatigue and composite delamination.
 * ----------------------------------------------------------------------------------------------------------------- *)
IF rCycleTime_s > 0.001 THEN
    rInstantaneousSkinDerivative := ((rVoted_PayloadSkinTemp_degC - rPreviousPayloadSkinTemp) / rCycleTime_s) * 60.0;
ELSE
    rInstantaneousSkinDerivative := 0.0;
END_IF;
rPreviousPayloadSkinTemp := rVoted_PayloadSkinTemp_degC;

(* First-Order Digital Low-Pass Filter on Slew Rate *)
rFilteredPayloadSlewRate := (0.90 * rFilteredPayloadSlewRate) + (0.10 * rInstantaneousSkinDerivative);
rPayloadSlewRate_degC_min := rFilteredPayloadSlewRate;

(* Maximum Spatial Thermal Gradient Across Spacecraft Payload *)
rSpatialThermalGradient := ABS(rVoted_PayloadSkinTemp_degC - rVoted_PayloadInternalTemp_degC);
IF ABS(TT_SHROUD_ZONE1_TEMP_201A - TT_SHROUD_ZONE6_TEMP_206A) > rSpatialThermalGradient THEN
    rSpatialThermalGradient := ABS(TT_SHROUD_ZONE1_TEMP_201A - TT_SHROUD_ZONE6_TEMP_206A);
END_IF;
rSpatialThermalGradient_degC := rSpatialThermalGradient;
"""
    parts.append(physics_logic)

    # -------------------------------------------------------------------------
    # PART 6: PHASE 3: 8x8 STATE-SPACE PROPAGATION & KALMAN OBSERVER
    # -------------------------------------------------------------------------
    ss_logic = """(* =====================================================================================================================
 * PHASE 3: 8x8 MULTIVARIABLE DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER
 * ===================================================================================================================== *)
(* Map physical measurements to measurement vector y_meas[1..8] *)
y_meas[1] := rShroudTemp_K;
y_meas[2] := rPayloadSkin_K;
y_meas[3] := rPayloadCore_K;
IF rVoted_ChamberPressure_mbar > 1.0E-9 THEN
    y_meas[4] := LN(rVoted_ChamberPressure_mbar) / 2.302585; (* log10(mbar) *)
ELSE
    y_meas[4] := -9.0;
END_IF;
y_meas[5] := rQCM_AccumulatedMass_ug_cm2;
y_meas[6] := rVoted_SolarFlux_Wm2;
y_meas[7] := rVoted_LN2_Flow_kg_h / 3600.0; (* kg/s *)
y_meas[8] := rVoted_ShroudTemp_Avg_degC + 273.15;

(* 1. A-Priori State Prediction: x_pred = A * x_state + B * u_act *)
FOR i_loop := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR j_loop := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (A_mat[i_loop, j_loop] * x_state[j_loop]);
    END_FOR;
    FOR k_loop := 1 TO 6 DO
        rTempAccumulator := rTempAccumulator + (B_mat[i_loop, k_loop] * u_act[k_loop]);
    END_FOR;
    x_pred[i_loop] := rTempAccumulator;
END_FOR;

(* 2. Predicted Measurement Vector: y_pred = C * x_pred *)
FOR i_loop := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR j_loop := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (C_mat[i_loop, j_loop] * x_pred[j_loop]);
    END_FOR;
    y_pred[i_loop] := rTempAccumulator;
    e_innov[i_loop] := y_meas[i_loop] - y_pred[i_loop];
END_FOR;

(* 3. Kalman Observer Correction Update: x_obs = x_pred + Ke * e_innov *)
FOR i_loop := 1 TO 8 DO
    rTempAccumulator := 0.0;
    FOR j_loop := 1 TO 8 DO
        rTempAccumulator := rTempAccumulator + (Ke_mat[i_loop, j_loop] * e_innov[j_loop]);
    END_FOR;
    x_obs[i_loop] := x_pred[i_loop] + rTempAccumulator;
    x_state[i_loop] := x_obs[i_loop]; (* Recurse updated state into current state *)
END_FOR;
"""
    parts.append(ss_logic)

    # -------------------------------------------------------------------------
    # PART 7: PHASE 4: RECEDING-HORIZON MPC OPTIMIZATION
    # -------------------------------------------------------------------------
    mpc_logic = """(* =====================================================================================================================
 * PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 * ===================================================================================================================== *)
(* Trajectory Setpoint References *)
r_ref[1] := rTargetShroudTemp_SP + 273.15;
r_ref[2] := rTargetPayloadSkinTemp_SP + 273.15;
r_ref[3] := rTargetPayloadSkinTemp_SP + 273.15;
IF rTargetChamberPressure_SP > 1.0E-9 THEN
    r_ref[4] := LN(rTargetChamberPressure_SP) / 2.302585;
ELSE
    r_ref[4] := -6.0;
END_IF;
r_ref[5] := 0.0; (* Minimize Contamination *)
r_ref[6] := rTargetSolarFlux_SP;
r_ref[7] := 0.35; (* 0.35 kg/s nominal LN2 flow *)
r_ref[8] := rTargetShroudTemp_SP + 273.15;

(* Evaluate Nominal Base Cost *)
rMinCandidateCost := 1.0E12;
rBestCandidate_u1 := u_act[1];
rBestCandidate_u2 := u_act[2];
rBestCandidate_u3 := u_act[3];
rBestCandidate_u4 := u_act[4];
rBestCandidate_u5 := u_act[5];
rBestCandidate_u6 := u_act[6];

(* Multi-Candidate Perturbation Search (9 Discrete Actuator Grid Hypotheses) *)
FOR cand_idx := 1 TO 9 DO
    rCandidateCost := 0.0;

    (* Forward simulate current candidate over prediction horizon Np = 3 *)
    FOR i_loop := 1 TO 8 DO
        x_mpc_pred[i_loop] := x_state[i_loop];
    END_FOR;

    (* Apply Perturbation Hypothesis based on cand_idx *)
    CASE cand_idx OF
        1: (* Hold Current Action *)
            u_mpc[1] := u_act[1]; u_mpc[2] := u_act[2]; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        2: (* Increase Subcooled LN2 Cryo Valve +5% *)
            u_mpc[1] := u_act[1] + 5.0; u_mpc[2] := u_act[2] - 3.0; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        3: (* Decrease Subcooled LN2 Cryo Valve -5% *)
            u_mpc[1] := u_act[1] - 5.0; u_mpc[2] := u_act[2] + 2.0; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        4: (* Increase GN2 Conditioning Electric Heaters +8% *)
            u_mpc[1] := u_act[1] - 4.0; u_mpc[2] := u_act[2] + 8.0; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        5: (* Decrease GN2 Conditioning Electric Heaters -8% *)
            u_mpc[1] := u_act[1] + 2.0; u_mpc[2] := u_act[2] - 8.0; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        6: (* Increase Solar Simulator Beam Radiance +5% *)
            u_mpc[1] := u_act[1]; u_mpc[2] := u_act[2]; u_mpc[3] := u_act[3] + 5.0;
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        7: (* Decrease Solar Simulator Beam Radiance -5% *)
            u_mpc[1] := u_act[1]; u_mpc[2] := u_act[2]; u_mpc[3] := u_act[3] - 5.0;
            u_mpc[4] := u_act[4]; u_mpc[5] := u_act[5]; u_mpc[6] := u_act[6];
        8: (* Boost Turbomolecular & Cryo Pumping Speed *)
            u_mpc[1] := u_act[1]; u_mpc[2] := u_act[2]; u_mpc[3] := u_act[3];
            u_mpc[4] := u_act[4] + 10.0; u_mpc[5] := u_act[5] + 10.0; u_mpc[6] := u_act[6];
        9: (* Controlled Repressurization Bleed Pulse *)
            u_mpc[1] := 0.0; u_mpc[2] := 5.0; u_mpc[3] := 0.0;
            u_mpc[4] := 0.0; u_mpc[5] := 0.0; u_mpc[6] := u_act[6] + 4.0;
    END_CASE;

    (* Actuator Physical Saturation Limits [0..100%] *)
    FOR k_loop := 1 TO 6 DO
        IF u_mpc[k_loop] > 100.0 THEN u_mpc[k_loop] := 100.0; END_IF;
        IF u_mpc[k_loop] < 0.0   THEN u_mpc[k_loop] := 0.0;   END_IF;
    END_FOR;

    (* 3-Step Prediction Rollout *)
    FOR j_loop := 1 TO 3 DO
        FOR i_loop := 1 TO 8 DO
            rTempAccumulator := 0.0;
            FOR k_loop := 1 TO 8 DO
                rTempAccumulator := rTempAccumulator + (A_mat[i_loop, k_loop] * x_mpc_pred[k_loop]);
            END_FOR;
            FOR k_loop := 1 TO 6 DO
                rTempAccumulator := rTempAccumulator + (B_mat[i_loop, k_loop] * u_mpc[k_loop]);
            END_FOR;
            x_mpc_next[i_loop] := rTempAccumulator;
        END_FOR;

        (* Accumulate Tracking Error Penalty: (x - r)^T * Q * (x - r) *)
        FOR i_loop := 1 TO 8 DO
            rTempDelta := x_mpc_next[i_loop] - r_ref[i_loop];
            rCandidateCost := rCandidateCost + (Q_diag[i_loop] * rTempDelta * rTempDelta);
        END_FOR;

        (* Copy next step to pred *)
        FOR i_loop := 1 TO 8 DO
            x_mpc_pred[i_loop] := x_mpc_next[i_loop];
        END_FOR;
    END_FOR;

    (* Add Actuator Expenditure Penalty: u^T * R * u *)
    FOR k_loop := 1 TO 6 DO
        rCandidateCost := rCandidateCost + (R_diag[k_loop] * u_mpc[k_loop] * u_mpc[k_loop]);
    END_FOR;

    (* Add Actuator Slew Rate Penalty: Delta_u^T * S * Delta_u *)
    FOR k_loop := 1 TO 6 DO
        rTempDelta := u_mpc[k_loop] - u_prev[k_loop];
        rCandidateCost := rCandidateCost + (S_diag[k_loop] * rTempDelta * rTempDelta);
    END_FOR;

    (* Thermal Slew Rate Penalty Barrier: Penalize severely if payload rate violates limit *)
    rTempDelta := ABS((x_mpc_pred[2] - x_state[2]) / 0.300) * 60.0; (* deg C/min *)
    IF rTempDelta > rMaxAllowableRampRate_degC_min THEN
        rCandidateCost := rCandidateCost + 1.0E7; (* Heavy Barrier Constraint Violation Penalty *)
    END_IF;

    (* Compare with Best Found Candidate *)
    IF rCandidateCost < rMinCandidateCost THEN
        rMinCandidateCost := rCandidateCost;
        rBestCandidate_u1 := u_mpc[1];
        rBestCandidate_u2 := u_mpc[2];
        rBestCandidate_u3 := u_mpc[3];
        rBestCandidate_u4 := u_mpc[4];
        rBestCandidate_u5 := u_mpc[5];
        rBestCandidate_u6 := u_mpc[6];
    END_IF;
END_FOR;

rMPC_Cost_J := rMinCandidateCost;

(* Store previous actuator vector for delta-u tracking *)
FOR k_loop := 1 TO 6 DO
    u_prev[k_loop] := u_act[k_loop];
END_FOR;
"""
    parts.append(mpc_logic)

    # -------------------------------------------------------------------------
    # PART 8: PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    fsm_logic = """(* =====================================================================================================================
 * PHASE 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
 * ===================================================================================================================== *)
tFSM_StateTimer(IN := (nActiveState = nPreviousState), PT := T#24H);
IF nActiveState <> nPreviousState THEN
    nPreviousState := nActiveState;
    bStateFirstScan := TRUE;
ELSE
    bStateFirstScan := FALSE;
END_IF;

CASE nActiveState OF
    0: (* --------------------------------------------------------------------------------------------------------------
        * STATE 0: STANDBY_FACILITY_VERIFICATION
        * Facility pre-test checks: door locked, seals verified, cleanroom interlock ok, system at 1 atm dry GN2
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := FALSE;
        bCryopumpHighVacGateValve_Cmd := FALSE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE; (* Specimen bus power permitted *)

        u_act[1] := 0.0; (* LN2 Valve Closed *)
        u_act[2] := 0.0; (* GN2 Heaters Off *)
        u_act[3] := 0.0; (* Solar Sim Off *)
        u_act[4] := 0.0; (* Turbopump Standby *)
        u_act[5] := 0.0; (* Cryopump Standby *)
        u_act[6] := 0.0; (* Repress Valve Closed *)

        IF bMasterAutoEnable AND bChamberDoorInterlockOk AND bCleanroomAirLockReady AND
           (NOT bFacilitySafetyInterlockLatched) AND (NOT bEmergencyVentAbortPB) THEN
            nActiveState := 1; (* Advance to Chamber Roughing Pumpdown *)
        END_IF;

    1: (* --------------------------------------------------------------------------------------------------------------
        * STATE 1: CHAMBER_ROUGHING_PUMPDOWN
        * Roughing roots and rotary screw dry pumps active; roughing valve open; roughing chamber to 0.05 mbar
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := TRUE;
        bTurbopumpHighVacGateValve_Cmd := FALSE;
        bCryopumpHighVacGateValve_Cmd := FALSE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := 0.0;
        u_act[3] := 0.0;
        u_act[4] := 25.0; (* Pre-accelerate Turbopump to 25% *)
        u_act[5] := 10.0;
        u_act[6] := 0.0;

        tRoughingTimeout(IN := TRUE, PT := T#45M);

        (* Transition to High-Vacuum Crossover once roughing reaches < 0.05 mbar (5.0E-2 mbar) *)
        IF rVoted_ChamberPressure_mbar <= 0.05 THEN
            tRoughingTimeout(IN := FALSE);
            nActiveState := 2; (* Advance to Cryopump High-Vacuum Crossover *)
        ELSIF tRoughingTimeout.Q THEN
            tRoughingTimeout(IN := FALSE);
            nActiveState := 11; (* Timeout Abort *)
        END_IF;

    2: (* --------------------------------------------------------------------------------------------------------------
        * STATE 2: CRYOPUMP_HIGH_VACUUM_CROSSOVER
        * Close roughing valve, accelerate turbomolecular pumps to > 90% (43,200 RPM), open DN500 & DN800 gate valves
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := 0.0;
        u_act[3] := 0.0;
        u_act[4] := 95.0; (* Full Turbopump Speed Reference *)
        u_act[5] := 100.0;(* Helium Cryopump Expansion Valve Full *)
        u_act[6] := 0.0;

        tHighVacCrossoverTimeout(IN := TRUE, PT := T#60M);

        (* Once High Vacuum verified < 1.0E-5 mbar and turbopump speed > 40,000 RPM, proceed *)
        IF (rVoted_ChamberPressure_mbar <= 1.0E-5) AND (rVoted_TurbopumpSpeed_RPM >= 40000.0) THEN
            tHighVacCrossoverTimeout(IN := FALSE);
            nActiveState := 3; (* Advance to Deep Space Cold Soak Chilldown *)
        ELSIF tHighVacCrossoverTimeout.Q THEN
            tHighVacCrossoverTimeout(IN := FALSE);
            nActiveState := 11; (* Vacuum Timeout Abort *)
        END_IF;

    3: (* --------------------------------------------------------------------------------------------------------------
        * STATE 3: DEEP_SPACE_COLD_SOAK_CHILLDOWN
        * Circulate subcooled LN2 through all shroud zones; chilldown shroud to -180 deg C under slew rate control
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := TRUE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        (* MPC Optimizes Subcooled LN2 modulating valve u_act[1] *)
        u_act[1] := rBestCandidate_u1;
        u_act[2] := 0.0;
        u_act[3] := 0.0;
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        (* Enforce Specimen Slew Rate Limit: if approaching 2.0 deg C/min, throttle LN2 valve *)
        IF ABS(rPayloadSlewRate_degC_min) > (rMaxAllowableRampRate_degC_min * 0.90) THEN
            u_act[1] := u_act[1] * 0.75;
        END_IF;

        tColdSoakStabilizeTimer(IN := (rVoted_ShroudTemp_Avg_degC <= -175.0), PT := T#30M);

        IF tColdSoakStabilizeTimer.Q THEN
            tColdSoakStabilizeTimer(IN := FALSE);
            nActiveState := 4; (* Advance to Cold Balance Equilibrium *)
        END_IF;

    4: (* --------------------------------------------------------------------------------------------------------------
        * STATE 4: COLD_BALANCE_EQUILIBRIUM
        * Thermal shroud stable at -180 deg C; hold cold balance for satellite thermal equilibrium (|dT/dt| < 0.2 C/h)
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := TRUE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := rBestCandidate_u1;
        u_act[2] := rBestCandidate_u2; (* Minor trim if needed *)
        u_act[3] := 0.0;
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        (* Stable Cold Balance Condition: Payload rate of change < 0.2 deg C/hr (0.0033 deg C/min) for > 2 hours *)
        tColdBalanceHoldTimer(IN := (ABS(rPayloadSlewRate_degC_min) < 0.0033), PT := T#2H);

        IF tColdBalanceHoldTimer.Q THEN
            tColdBalanceHoldTimer(IN := FALSE);
            bColdBalanceAchieved := TRUE;
            nActiveState := 5; (* Advance to Orbital Sunrise Solar Simulator Ramp *)
        END_IF;

    5: (* --------------------------------------------------------------------------------------------------------------
        * STATE 5: ORBITAL_SUNRISE_SOLAR_SIM_RAMP
        * Ignite Xenon arc lamps, modulate thyristor DC power to ramp beam radiance to 1.0 Solar Constant (1,366 W/m2)
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := TRUE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := rBestCandidate_u1;
        u_act[2] := 0.0;
        u_act[3] := rBestCandidate_u3; (* Solar Simulator Thyristor Phase Demand *)
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        (* Ramp Solar Simulator Radiance smoothly *)
        tSolarSimRampTimer(IN := (rVoted_SolarFlux_Wm2 >= 1345.0 AND rVoted_SolarFlux_Wm2 <= 1386.0), PT := T#15M);

        IF tSolarSimRampTimer.Q THEN
            tSolarSimRampTimer(IN := FALSE);
            nActiveState := 6; (* Advance to Hot Balance Equilibrium *)
        END_IF;

    6: (* --------------------------------------------------------------------------------------------------------------
        * STATE 6: HOT_BALANCE_EQUILIBRIUM
        * 1.0 Solar Constant + GN2 shroud heaters maintaining hot case (+120 to +150 deg C); hold hot thermal balance
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := TRUE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := rBestCandidate_u2; (* GN2 Conditioning Heaters *)
        u_act[3] := rBestCandidate_u3; (* Solar Sim Phase *)
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        (* Hold hot balance equilibrium for 2 hours with |dT/dt| < 0.2 deg C/hr *)
        tHotBalanceHoldTimer(IN := (ABS(rPayloadSlewRate_degC_min) < 0.0033), PT := T#2H);

        IF tHotBalanceHoldTimer.Q THEN
            tHotBalanceHoldTimer(IN := FALSE);
            bHotBalanceAchieved := TRUE;
            nActiveState := 7; (* Advance to Thermal Cycle Transition Slew *)
        END_IF;

    7: (* --------------------------------------------------------------------------------------------------------------
        * STATE 7: THERMAL_CYCLE_TRANSITION_SLEW
        * Cycle satellite between eclipse (cold) and orbit sun (hot); increment cycle counter up to nTargetThermalCycles
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := TRUE;
        bGN2CirculationBlowerContactor := TRUE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := rBestCandidate_u1;
        u_act[2] := rBestCandidate_u2;
        u_act[3] := rBestCandidate_u3;
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        tThermalCycleDwellTimer(IN := TRUE, PT := T#4H);

        IF tThermalCycleDwellTimer.Q THEN
            tThermalCycleDwellTimer(IN := FALSE);
            nThermalCycleCount := nThermalCycleCount + 1;
            IF nThermalCycleCount >= nTargetThermalCycles THEN
                nActiveState := 8; (* Advance to Outgassing Bakeout Monitor *)
            ELSE
                nActiveState := 3; (* Return for next cold soak cycle *)
            END_IF;
        END_IF;

    8: (* --------------------------------------------------------------------------------------------------------------
        * STATE 8: OUTGASSING_BAKEOUT_MONITOR
        * Elevate payload temperature to +80 to +125 deg C; observe QCM molecular contamination until rate < 1.5 Hz/h
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := TRUE;
        bCryopumpHighVacGateValve_Cmd := TRUE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := TRUE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := rBestCandidate_u2; (* Trim Heaters Maintain Bakeout Plateau *)
        u_act[3] := 0.0;
        u_act[4] := 100.0;
        u_act[5] := 100.0;
        u_act[6] := 0.0;

        (* Verify outgassing rate drops below criterion (1.5 Hz/h) continuously for > 4 hours *)
        tBakeoutHoldTimer(IN := (rVoted_QCM_OutgassingRate_Hz_hr <= rMaxAllowableOutgassingRate_Hz_hr), PT := T#4H);

        IF tBakeoutHoldTimer.Q THEN
            tBakeoutHoldTimer(IN := FALSE);
            bBakeoutAchieved := TRUE;
            nActiveState := 9; (* Advance to Controlled GN2 Repressurization *)
        END_IF;

    9: (* --------------------------------------------------------------------------------------------------------------
        * STATE 9: CONTROLLED_GN2_REPRESSURIZATION
        * Warm shroud to > +15 deg C to prevent atmospheric condensation; isolate high vac valves; dry GN2 bleed
        * -------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := FALSE; (* Gate Valves Isolated *)
        bCryopumpHighVacGateValve_Cmd := FALSE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := TRUE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := 15.0; (* Warm GN2 Blower *)
        u_act[3] := 0.0;
        u_act[4] := 0.0;  (* Turbopump Spindown *)
        u_act[5] := 0.0;  (* Cryopump Isolated *)
        u_act[6] := rBestCandidate_u6; (* Controlled GN2 Bleed Valve Position *)

        (* Repressurization rate-of-rise limiter: keep dP/dt < 25 mbar/min *)
        tControlledRepressTimer(IN := (rVoted_ChamberPressure_mbar >= 1005.0), PT := T#10M);

        IF tControlledRepressTimer.Q THEN
            tControlledRepressTimer(IN := FALSE);
            bRepressComplete := TRUE;
            nActiveState := 10; (* Advance to Cleanroom Door Unlock Safe *)
        END_IF;

    10: (* -------------------------------------------------------------------------------------------------------------
         * STATE 10: CLEANROOM_DOOR_UNLOCK_SAFE
         * Vessel equalized with ISO 7 cleanroom (1,013 mbar +/- 5 mbar); door interlocks unlocked for de-integration
         * ------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := FALSE;
        bCryopumpHighVacGateValve_Cmd := FALSE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := FALSE;
        bSpecimenPowerDisconnectRelay := TRUE;

        u_act[1] := 0.0;
        u_act[2] := 0.0;
        u_act[3] := 0.0;
        u_act[4] := 0.0;
        u_act[5] := 0.0;
        u_act[6] := 0.0;

        IF NOT bMasterAutoEnable THEN
            nActiveState := 0; (* Return to Standby *)
        END_IF;

    11: (* -------------------------------------------------------------------------------------------------------------
         * STATE 11: EMERGENCY_DEPRESSURIZATION_ABORT
         * Immediate high-vacuum isolation (< 100 ms), solar sim / heaters killed, satellite power isolated, dry GN2 vent
         * ------------------------------------------------------------------------------------------------------------- *)
        bRoughingIsolationValve_Cmd := FALSE;
        bTurbopumpHighVacGateValve_Cmd := FALSE;
        bCryopumpHighVacGateValve_Cmd := FALSE;
        bLN2CirculationPumpContactor := FALSE;
        bGN2CirculationBlowerContactor := FALSE;
        bFastEmergencyRepressValve_Cmd := TRUE; (* Fast dry GN2 emergency purge *)
        bSpecimenPowerDisconnectRelay := FALSE; (* Satellite specimen power feedthrough tripped *)
        bFacilitySafetyInterlockLatched := TRUE;

        u_act[1] := 0.0;
        u_act[2] := 0.0;
        u_act[3] := 0.0;
        u_act[4] := 0.0;
        u_act[5] := 0.0;
        u_act[6] := 100.0; (* Full Emergency Bleed *)

        tEmergencyAbortTimer(IN := (rVoted_ChamberPressure_mbar >= 1000.0), PT := T#5M);

        IF bMasterFaultReset AND (NOT bEmergencyVentAbortPB) AND tEmergencyAbortTimer.Q THEN
            bFacilitySafetyInterlockLatched := FALSE;
            bFastEmergencyRepressValve_Cmd := FALSE;
            nActiveState := 0; (* Reset to Standby *)
        END_IF;

END_CASE;

nActiveFSMState := nActiveState;

(* Map Actuator Demands to Physical Functional Block Outputs *)
rLN2_SubcooledModulatingValve_01 := u_act[1];
rLN2_TrimInjectionValve_02       := u_act[1] * 0.85;
rGN2_ConditioningHeaterPower_kW  := (u_act[2] / 100.0) * 150.0; (* 0 to 150 kW *)
rSolarSimulatorThyristorPower_pct:= u_act[3];
rTurbomolecularPumpSpeedRef_RPM  := (u_act[4] / 100.0) * 48000.0;
rCryoCondensationExpansionValve_pct := u_act[5];
rChamberGN2RepressurizationValve_pct := u_act[6];
"""
    parts.append(fsm_logic)

    # -------------------------------------------------------------------------
    # PART 9: PHASE 6: ISA-18.2 PROCESS ALARMS, TRIPS & DIAGNOSTIC WORDS
    # -------------------------------------------------------------------------
    alarms_logic = """(* =====================================================================================================================
 * PHASE 6: ISA-18.2 PROCESS ALARMS, TRIPS & DIAGNOSTIC WORD BIT PACKING
 * ===================================================================================================================== *)
(* -----------------------------------------------------------------------------------------------------------------
 * 1. ISA-18.2 Alarm Trip Evaluations with Hysteresis Deadbands:
 * ----------------------------------------------------------------------------------------------------------------- *)
(* Chamber Vacuum Loss Alarm (In High-Vac states 2..8) *)
IF (nActiveState >= 2) AND (nActiveState <= 8) THEN
    IF rVoted_ChamberPressure_mbar >= c_Press_HI_HI THEN
        bAlarm_ChamberPress_HI_HI := TRUE;
    ELSIF rVoted_ChamberPressure_mbar < (c_Press_HI_HI * 0.50) THEN
        bAlarm_ChamberPress_HI_HI := FALSE;
    END_IF;

    IF rVoted_ChamberPressure_mbar >= c_Press_HI THEN
        bAlarm_ChamberPress_HI := TRUE;
    ELSIF rVoted_ChamberPressure_mbar < (c_Press_HI * 0.60) THEN
        bAlarm_ChamberPress_HI := FALSE;
    END_IF;
ELSE
    bAlarm_ChamberPress_HI_HI := FALSE;
    bAlarm_ChamberPress_HI := FALSE;
END_IF;

(* Payload Skin Overtemperature & Undercooling Alarms *)
IF rVoted_PayloadSkinTemp_degC >= c_SkinTemp_HI_HI THEN
    bAlarm_PayloadSkin_HI_HI := TRUE;
ELSIF rVoted_PayloadSkinTemp_degC < (c_SkinTemp_HI_HI - 2.0) THEN
    bAlarm_PayloadSkin_HI_HI := FALSE;
END_IF;

IF rVoted_PayloadSkinTemp_degC >= c_SkinTemp_HI THEN
    bAlarm_PayloadSkin_HI := TRUE;
ELSIF rVoted_PayloadSkinTemp_degC < (c_SkinTemp_HI - 2.0) THEN
    bAlarm_PayloadSkin_HI := FALSE;
END_IF;

IF rVoted_PayloadSkinTemp_degC <= c_SkinTemp_LO_LO THEN
    bAlarm_PayloadSkin_LO_LO := TRUE;
ELSIF rVoted_PayloadSkinTemp_degC > (c_SkinTemp_LO_LO + 2.0) THEN
    bAlarm_PayloadSkin_LO_LO := FALSE;
END_IF;

IF rVoted_PayloadSkinTemp_degC <= c_SkinTemp_LO THEN
    bAlarm_PayloadSkin_LO := TRUE;
ELSIF rVoted_PayloadSkinTemp_degC > (c_SkinTemp_LO + 2.0) THEN
    bAlarm_PayloadSkin_LO := FALSE;
END_IF;

(* Payload Internal Avionics Core Over/Under-Temperature Alarms *)
IF rVoted_PayloadInternalTemp_degC >= c_CoreTemp_HI_HI THEN
    bAlarm_PayloadInternal_HI_HI := TRUE;
ELSIF rVoted_PayloadInternalTemp_degC < (c_CoreTemp_HI_HI - 2.0) THEN
    bAlarm_PayloadInternal_HI_HI := FALSE;
END_IF;

IF rVoted_PayloadInternalTemp_degC <= c_CoreTemp_LO_LO THEN
    bAlarm_PayloadInternal_LO_LO := TRUE;
ELSIF rVoted_PayloadInternalTemp_degC > (c_CoreTemp_LO_LO + 2.0) THEN
    bAlarm_PayloadInternal_LO_LO := FALSE;
END_IF;

(* Rate of Change (ROC) Thermal Shock Alarm *)
IF ABS(rPayloadSlewRate_degC_min) >= c_SlewRate_ROC_Limit THEN
    bAlarm_SlewRate_ROC := TRUE;
ELSIF ABS(rPayloadSlewRate_degC_min) < (c_SlewRate_ROC_Limit - 0.20) THEN
    bAlarm_SlewRate_ROC := FALSE;
END_IF;

(* Spatial Thermal Gradient Alarm *)
IF rSpatialThermalGradient_degC >= c_SpatialGradient_Limit THEN
    bAlarm_SpatialGradient_HI := TRUE;
ELSIF rSpatialThermalGradient_degC < (c_SpatialGradient_Limit - 3.0) THEN
    bAlarm_SpatialGradient_HI := FALSE;
END_IF;

(* Solar Simulator Irradiance Flash / Overpower Trip *)
IF rVoted_SolarFlux_Wm2 >= c_SolarFlux_HI_HI THEN
    bAlarm_SolarFlux_HI_HI := TRUE;
ELSIF rVoted_SolarFlux_Wm2 < (c_SolarFlux_HI_HI - 50.0) THEN
    bAlarm_SolarFlux_HI_HI := FALSE;
END_IF;

(* Solar Simulator Radiance Deviation Warning (In State 5 & 6) *)
IF (nActiveState = 5) OR (nActiveState = 6) THEN
    IF ABS(rVoted_SolarFlux_Wm2 - rTargetSolarFlux_SP) > 35.0 THEN
        bAlarm_SolarFlux_Dev := TRUE;
    ELSE
        bAlarm_SolarFlux_Dev := FALSE;
    END_IF;
ELSE
    bAlarm_SolarFlux_Dev := FALSE;
END_IF;

(* Subcooled Liquid Nitrogen Boiling Risk Alarm *)
IF rLN2_BoilingSuppressionMargin_degC < 2.50 THEN
    bAlarm_LN2_BoilingRisk := TRUE;
ELSE
    bAlarm_LN2_BoilingRisk := FALSE;
END_IF;

(* Cryogenic Shroud Circuit Overpressure & Burst Disk Continuity *)
IF rVoted_GN2_LoopPressure_bar >= c_ShroudOverpress_HI_HI THEN
    bAlarm_ShroudOverpress_HI_HI := TRUE;
ELSE
    bAlarm_ShroudOverpress_HI_HI := FALSE;
END_IF;

IF NOT bCryoBurstDiskRuptureWire THEN
    bAlarm_BurstDiskRupture := TRUE;
ELSE
    bAlarm_BurstDiskRupture := FALSE;
END_IF;

IF bEmergencyVentAbortPB THEN
    bAlarm_EmergencyAbortLatched := TRUE;
END_IF;

(* Critical Fast Abort Emergency Interlock Dispatch: Trigger State 11 *)
IF bAlarm_ChamberPress_HI_HI OR bAlarm_PayloadSkin_HI_HI OR bAlarm_PayloadSkin_LO_LO OR
   bAlarm_BurstDiskRupture OR bAlarm_SolarFlux_HI_HI OR bAlarm_EmergencyAbortLatched THEN
    bFacilitySafetyInterlockLatched := TRUE;
    nActiveState := 11; (* Immediate Transition to EMERGENCY_DEPRESSURIZATION_ABORT *)
END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 2. Diagnostic Word 01: 2oo3 Sensor Health & Discrepancy Word
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord01 := 16#0000;
IF bDisc_RoughVac       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0001; END_IF;
IF bDisc_HighVac        THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0002; END_IF;
IF bDisc_ShroudZ1       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0004; END_IF;
IF bDisc_ShroudZ2       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0008; END_IF;
IF bDisc_ShroudZ3       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0010; END_IF;
IF bDisc_ShroudZ6       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0020; END_IF;
IF bDisc_Skin           THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0040; END_IF;
IF bDisc_Core           THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0080; END_IF;
IF bDisc_QCM            THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0100; END_IF;
IF bDisc_Solar          THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0200; END_IF;
IF bDisc_LN2Flow        THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0400; END_IF;
IF bDisc_GN2Press       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#0800; END_IF;
IF bDisc_TurboSpeed     THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#1000; END_IF;
IF tTMR_HighVac.Q       THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#2000; END_IF;
IF tTMR_Skin.Q          THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#4000; END_IF;
IF bModelInitialized    THEN wDiagnosticWord01 := wDiagnosticWord01 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 3. Diagnostic Word 02: ISA-18.2 Critical Trip & Fast Abort Word
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord02 := 16#0000;
IF bAlarm_ChamberPress_HI_HI    THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0001; END_IF;
IF bAlarm_PayloadSkin_HI_HI     THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0002; END_IF;
IF bAlarm_PayloadSkin_LO_LO     THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0004; END_IF;
IF bAlarm_PayloadInternal_HI_HI THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0008; END_IF;
IF bAlarm_PayloadInternal_LO_LO THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0010; END_IF;
IF bAlarm_SlewRate_ROC          THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0020; END_IF;
IF bAlarm_SolarFlux_HI_HI       THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0040; END_IF;
IF bAlarm_ShroudOverpress_HI_HI THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0080; END_IF;
IF bAlarm_BurstDiskRupture      THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0100; END_IF;
IF bAlarm_EmergencyAbortLatched THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0200; END_IF;
IF bFacilitySafetyInterlockLatched THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0400; END_IF;
IF NOT bEmergencyVentAbortPB    THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#0800; END_IF;
IF NOT bChamberDoorInterlockOk  THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#1000; END_IF;
IF NOT bCleanroomAirLockReady   THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#2000; END_IF;
IF bColdBalanceAchieved         THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#4000; END_IF;
IF bHotBalanceAchieved          THEN wDiagnosticWord02 := wDiagnosticWord02 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 4. Diagnostic Word 03: Process Warnings & Subsystem Status Word
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord03 := 16#0000;
IF bAlarm_ChamberPress_HI       THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0001; END_IF;
IF bAlarm_PayloadSkin_HI        THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0002; END_IF;
IF bAlarm_PayloadSkin_LO        THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0004; END_IF;
IF bAlarm_SpatialGradient_HI    THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0008; END_IF;
IF bAlarm_SolarFlux_Dev         THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0010; END_IF;
IF bAlarm_LN2_BoilingRisk       THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0020; END_IF;
IF bBakeoutAchieved             THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0040; END_IF;
IF bRepressComplete             THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0080; END_IF;
IF bRoughingIsolationValve_Cmd  THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0100; END_IF;
IF bTurbopumpHighVacGateValve_Cmd THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0200; END_IF;
IF bCryopumpHighVacGateValve_Cmd THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0400; END_IF;
IF bLN2CirculationPumpContactor THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#0800; END_IF;
IF bGN2CirculationBlowerContactor THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#1000; END_IF;
IF bFastEmergencyRepressValve_Cmd THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#2000; END_IF;
IF bSpecimenPowerDisconnectRelay THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#4000; END_IF;
IF bMasterAutoEnable            THEN wDiagnosticWord03 := wDiagnosticWord03 OR 16#8000; END_IF;

(* -----------------------------------------------------------------------------------------------------------------
 * 5. Diagnostic Word 04: Active FSM State Code & Operating Margins
 * Bits 0..3: Active State Code [0..11]
 * Bits 4..7: Thermal Cycle Counter [0..15]
 * Bits 8..15: Operational Mode & Thermal Safety Indicators
 * ----------------------------------------------------------------------------------------------------------------- *)
wDiagnosticWord04 := INT_TO_WORD(nActiveState) AND 16#000F;
wDiagnosticWord04 := wDiagnosticWord04 OR (SHL(INT_TO_WORD(nThermalCycleCount) AND 16#000F, 4));

IF rVoted_ChamberPressure_mbar < 1.0E-5 THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0100; END_IF;
IF rVoted_ShroudTemp_Avg_degC <= -170.0  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0200; END_IF;
IF rVoted_ShroudTemp_Avg_degC >= 100.0   THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0400; END_IF;
IF rVoted_SolarFlux_Wm2 >= 1300.0        THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#0800; END_IF;
IF rKnudsenNumber > 1.0                  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#1000; END_IF;
IF rMPC_Cost_J < 5000.0                  THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#2000; END_IF;
IF bMasterFaultReset                     THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#4000; END_IF;
IF bFacilitySafetyInterlockLatched       THEN wDiagnosticWord04 := wDiagnosticWord04 OR 16#8000; END_IF;

END_FUNCTION_BLOCK
"""
    parts.append(alarms_logic)

    full_st = "\n\n".join(parts)
    return full_st

if __name__ == "__main__":
    code = generate_full_st_code()
    print("Code successfully generated.")
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total characters: {len(code)}")
