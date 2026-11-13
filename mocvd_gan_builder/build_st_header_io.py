# mocvd_gan_builder/build_st_header_io.py

def get_header_and_io():
    return """FUNCTION_BLOCK FB_Semiconductor_MOCVD_GaN_Epitaxy_SusceptorThermal
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * ARCHITECTURAL GRADE : Advanced Semiconductor Manufacturing & Epitaxial Thin-Film Nanotechnology
 * COMMERCIAL SECTOR   : Metal-Organic Chemical Vapor Deposition (MOCVD) Planetary Epitaxial Reactor
 * APPLICATION TARGET  : High-Electron-Mobility Transistor (HEMT) & Multi-Quantum-Well (MQW) Gallium Nitride (GaN)
 * WAFER BATCH SCALE   : Planetary Susceptor 8 x 150 mm (6-inch) or 5 x 200 mm (8-inch) Sapphire / Semi-Insulating SiC
 * OPERATING REGIME    : Multi-Zone RF Induction Heating (Ambient to 1,200.0 deg C), High Vacuum to Low Pressure (50-1000 mbar)
 *
 * CYBER-PHYSICAL SUBSYSTEMS & PROCESS ARCHITECTURE:
 *   1. Multi-Zone Susceptor RF Induction Thermal Dynamics & Dynamic View Factor Decoupling:
 *      - 3 Concentric Graphite Heating Zones: Inner Core, Mid-Annulus, Outer Perimeter.
 *      - Severe high-temperature radiative cross-talk governed by Stefan-Boltzmann Stefan-Schwarz radiation view factors:
 *            q_rad,i = sum_j ( F_ij * sigma_SB * (T_i^4 - T_j^4) )
 *      - Real-time dynamic matrix decoupling K_decouple = (F_rad)^(-1) to eliminate cross-zone thermal interference.
 *      - Strict induction generator slew-rate limiting (max 2.5 %/s) to prevent Zerodur quartz plate thermal fracture.
 *
 *   2. Gas-Phase Chemical Kinetics, Hydrodynamic Boundary Layer & Pyrolysis Kinetics:
 *      - Precursors: Trimethylgallium (TMGa: Ga(CH3)3), Trimethylaluminum (TMA: Al2(CH3)6), Ammonia (NH3), Silane (SiH4),
 *        Bis(cyclopentadienyl)magnesium (Cp2Mg: (C5H5)2Mg), and high-purity carrier gases (Pd-purified H2 and N2).
 *      - Gas-foil aerodynamic levitation: Satellite wafer disks levitated and driven by viscous spiral gas shear (0-120 rpm).
 *      - Mass-transport-limited crystal growth kinetics:
 *            R_growth = k_diff * (P_TMGa / P_total) * exp(-E_a / (R_gas * T_susceptor))
 *      - Parasitic pre-reactions: TMGa:NH3 adduct formation ([Ga(CH3)3:NH3]) suppressed by high linear gas velocity.
 *
 *   3. 2oo3 Triple Modular Redundancy (TMR) Sensor Architecture:
 *      - Inner Pyrometer Triplet: TT_PYRO_IN_101A/B/C [deg C] (High-speed multi-wavelength fiber optic pyrometers)
 *      - Middle Pyrometer Triplet: TT_PYRO_MID_201A/B/C [deg C]
 *      - Outer Pyrometer Triplet: TT_PYRO_OUT_301A/B/C [deg C]
 *      - Chamber Static Pressure Triplet: PT_CHAMBER_401A/B/C [mbar] (Temperature-compensated capacitance manometers)
 *      - In-Situ Laser Reflectometer Triplet: OPT_REFL_501A/B/C [counts] (405 nm Fabry-Perot interference detectors)
 *      - Discrepancy accumulation timers (100 ms limit), bumpless degradation to 2oo2 and 1oo1, failsafe on loss of quorum.
 *
 *   4. Cyber-Physical Discrete State-Space Model & Kalman-Luenberger Observer (Ts = 10 ms):
 *      - 8 Explicit States:
 *          x1: Susceptor Inner Zone Temperature [deg C]
 *          x2: Susceptor Middle Zone Temperature [deg C]
 *          x3: Susceptor Outer Zone Temperature [deg C]
 *          x4: Reactor Chamber Total Static Pressure [mbar]
 *          x5: Planetary Gas-Foil Satellite Wafer Rotation Speed [rpm]
 *          x6: Boundary Layer Ammonia Partial Pressure [mbar]
 *          x7: In-Situ Optical Reflectometry Epilayer Thickness [nm]
 *          x8: GaN Crystal Growth Rate [um/h]
 *      - 6 Actuator Inputs:
 *          u1: Inner Zone RF Power [0..100 %]
 *          u2: Middle Zone RF Power [0..100 %]
 *          u3: Outer Zone RF Power [0..100 %]
 *          u4: Throttle Butterfly Pressure Valve Opening [0..100 %]
 *          u5: TMGa Organometallic Bubbler MFC [0..500 sccm]
 *          u6: Ammonia Precursor MFC [0..50 slm]
 *      - Explicit discrete state transition matrix A (8x8), input matrix B (8x6), output matrix C (6x8), feedthrough D (6x6).
 *      - Steady-state Kalman-Luenberger observer innovation gain matrix L (8x6) executing innovation update:
 *            x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k] - D * u[k])
 *
 *   5. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
 *      - Prediction horizon N = 5 steps, 6 unrolled iterations of PGD per 10 ms cycle.
 *      - Quadratic objective function: min J = sum_k ( (y - y_sp)^T * Q * (y - y_sp) + u^T * R * u + du^T * S * du ).
 *      - Actuator bounds enforcement: Box constraints on power, valve position, and MFC setpoints.
 *      - Real-time thermal gradient minimization across Inner, Middle, and Outer zones (|T_in - T_mid| < 1.0 deg C).
 *
 *   6. Deterministic 14-Stage Epitaxial Finite State Machine (FSM):
 *      - Stage 0: LOAD_LOCK_TRANSFER_AND_BASE_VACUUM (< 1.0e-6 mbar turbomolecular evacuation)
 *      - Stage 1: HYDROGEN_PURGE_AND_GAS_FOIL_LEVITATION_CHECK (Purge H2, verify satellite gas cushion stability)
 *      - Stage 2: GRAPHITE_SUSCEPTOR_ROTATION_RAMPUP (50 rpm planetary orbital spinup)
 *      - Stage 3: THERMAL_DEOXIDATION_BAKEOUT (1,100.0 deg C in H2 for sapphire surface deoxidation)
 *      - Stage 4: PRECURSOR_MASS_FLOW_VENT_RUN_STABILIZATION (Stabilize MO bubbler flows to Vent line)
 *      - Stage 5: SUBSTRATE_NITRIDATION_STEP (NH3 surface conversion at 1,050.0 deg C)
 *      - Stage 6: LOW_TEMP_AlN_OR_GaN_NUCLEATION_LAYER (550.0 deg C, 30 nm nucleation buffer)
 *      - Stage 7: HIGH_TEMP_GaN_BUFFER_GROWTH_MPC_TRACKING (1,050.0 deg C, 2.5 um buffer layer under closed-loop MPC)
 *      - Stage 8: INGaN_MQW_ACTIVE_REGION_SUPERLATTICE_SWITCH (750.0 deg C, rapid run/vent switching for 5-period MQW)
 *      - Stage 9: p_TYPE_GaN_MG_DOPING_AND_CAP_LAYER (950.0 deg C, Cp2Mg doping profile)
 *      - Stage 10: PRECURSOR_FAST_VENT_AND_POST_GROWTH_COOL (Sub-25 ms double-block-and-bleed MO isolation, ramp down)
 *      - Stage 11: AMMONIA_SURFACE_DESORPTION_PREVENTION (NH3 overpressure down to 450.0 deg C to suppress nitrogen loss)
 *      - Stage 12: NITROGEN_PURGE_AND_ROOM_TEMP_EQUILIBRIUM (N2 backfill, susceptor cooldown to < 60.0 deg C, brake)
 *      - Stage 13: EMERGENCY_RF_CROWBAR_AND_RUN_VENT_TRIP (Thyristor crowbar < 2 ms, fast pneumatic vent dump)
 *
 *   7. ISA-18.2 Process Alarm Matrix & Sub-25 ms Fast Pyrophoric Gas Interlock:
 *      - Ultra-fast double-block-and-bleed valve sequencing to dump pyrophoric TMGa/TMA into scrubbed vent lines.
 *      - Multi-tier HH, H, L, LL alarms with deadband hysteresis on pyrometer temps, vacuum, rotation, and hydride flows.
 *      - 32-bit bit-packed telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.
 *
 * GOVERNING STANDARDS: IEC 61131-3 3rd Ed., SEMI S2/S8 Environmental & Safety Guidelines, ISA-18.2 Alarm Systems.
 * CONTROLLER SCAN RATE: Ts = 10.0 ms (100 Hz deterministic real-time kernel task).
 * ===================================================================================================================== *)

VAR_INPUT
    (* === MASTER SYSTEM CLOCK & SCAN SIGNALS === *)
    bScanCyclePulse_10ms                : BOOL := FALSE;      (* Master deterministic 10ms real-time scan pulse [bool] *)
    bSystemEnable                       : BOOL := FALSE;      (* Master software enable interlock signal [bool] *)
    bSafetyInterlocksHealthy            : BOOL := FALSE;      (* Hardwired safety loop status (vacuum, cooling, exhaust) [bool] *)
    bEmergencyStopCircuitHealthy        : BOOL := FALSE;      (* Category 4 / PLe dual-channel E-stop loop status [bool] *)
    bAutoRecipeStartCmd                 : BOOL := FALSE;      (* Operator recipe execution start command [bool] *)
    bRecipeAbortCmd                     : BOOL := FALSE;      (* Immediate recipe abort and graceful cooldown request [bool] *)
    bAlarmAcknowledgeCmd                : BOOL := FALSE;      (* HMI master alarm acknowledge and reset button [bool] *)
    bMaintenanceOverrideActive          : BOOL := FALSE;      (* Certified service maintenance override mode [bool] *)

    (* === TRANSMITTER TRIPLET 1: INNER ZONE OPTICAL PYROMETER (TT_PYRO_IN_101A/B/C) === *)
    TT_PYRO_IN_101A                     : REAL := 25.0;       (* Inner Zone High-Speed Optical Pyrometer Sensor A [deg C] *)
    TT_PYRO_IN_101B                     : REAL := 25.0;       (* Inner Zone High-Speed Optical Pyrometer Sensor B [deg C] *)
    TT_PYRO_IN_101C                     : REAL := 25.0;       (* Inner Zone High-Speed Optical Pyrometer Sensor C [deg C] *)
    bStatus_TT_101A_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 101A [bool] *)
    bStatus_TT_101B_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 101B [bool] *)
    bStatus_TT_101C_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 101C [bool] *)

    (* === TRANSMITTER TRIPLET 2: MIDDLE ZONE OPTICAL PYROMETER (TT_PYRO_MID_201A/B/C) === *)
    TT_PYRO_MID_201A                    : REAL := 25.0;       (* Middle Zone High-Speed Optical Pyrometer Sensor A [deg C] *)
    TT_PYRO_MID_201B                    : REAL := 25.0;       (* Middle Zone High-Speed Optical Pyrometer Sensor B [deg C] *)
    TT_PYRO_MID_201C                    : REAL := 25.0;       (* Middle Zone High-Speed Optical Pyrometer Sensor C [deg C] *)
    bStatus_TT_201A_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 201A [bool] *)
    bStatus_TT_201B_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 201B [bool] *)
    bStatus_TT_201C_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 201C [bool] *)

    (* === TRANSMITTER TRIPLET 3: OUTER ZONE OPTICAL PYROMETER (TT_PYRO_OUT_301A/B/C) === *)
    TT_PYRO_OUT_301A                    : REAL := 25.0;       (* Outer Zone High-Speed Optical Pyrometer Sensor A [deg C] *)
    TT_PYRO_OUT_301B                    : REAL := 25.0;       (* Outer Zone High-Speed Optical Pyrometer Sensor B [deg C] *)
    TT_PYRO_OUT_301C                    : REAL := 25.0;       (* Outer Zone High-Speed Optical Pyrometer Sensor C [deg C] *)
    bStatus_TT_301A_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 301A [bool] *)
    bStatus_TT_301B_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 301B [bool] *)
    bStatus_TT_301C_Healthy             : BOOL := TRUE;       (* Hardware integrity diagnostic bit for Pyrometer 301C [bool] *)

    (* === TRANSMITTER TRIPLET 4: CHAMBER CAPACITANCE DIAPHRAGM MANOMETER (PT_CHAMBER_401A/B/C) === *)
    PT_CHAMBER_401A                     : REAL := 1013.25;    (* Heated Capacitance Diaphragm Vacuum Gauge Sensor A [mbar] *)
    PT_CHAMBER_401B                     : REAL := 1013.25;    (* Heated Capacitance Diaphragm Vacuum Gauge Sensor B [mbar] *)
    PT_CHAMBER_401C                     : REAL := 1013.25;    (* Heated Capacitance Diaphragm Vacuum Gauge Sensor C [mbar] *)
    bStatus_PT_401A_Healthy             : BOOL := TRUE;       (* Manometer transducer 401A hardware health bit [bool] *)
    bStatus_PT_401B_Healthy             : BOOL := TRUE;       (* Manometer transducer 401B hardware health bit [bool] *)
    bStatus_PT_401C_Healthy             : BOOL := TRUE;       (* Manometer transducer 401C hardware health bit [bool] *)

    (* === TRANSMITTER TRIPLET 5: IN-SITU OPTICAL REFLECTOMETER 405 NM INTENSITY (OPT_REFL_501A/B/C) === *)
    OPT_REFL_501A                       : REAL := 1000.0;     (* 405 nm Epitaxial Laser Reflectometer Detector A [counts] *)
    OPT_REFL_501B                       : REAL := 1000.0;     (* 405 nm Epitaxial Laser Reflectometer Detector B [counts] *)
    OPT_REFL_501C                       : REAL := 1000.0;     (* 405 nm Epitaxial Laser Reflectometer Detector C [counts] *)
    bStatus_OPT_501A_Healthy            : BOOL := TRUE;       (* Optical detector 501A hardware diagnostic bit [bool] *)
    bStatus_OPT_501B_Healthy            : BOOL := TRUE;       (* Optical detector 501B hardware diagnostic bit [bool] *)
    bStatus_OPT_501C_Healthy            : BOOL := TRUE;       (* Optical detector 501C hardware diagnostic bit [bool] *)

    (* === AUXILIARY SENSORS & TRANSDUCERS === *)
    PT_BASE_VAC_001                     : REAL := 1.0e-7;     (* High-Vacuum Wide-Range Penning/Pirani Gauge [mbar] *)
    PT_FORELINE_402                     : REAL := 2.5;        (* Dry Vacuum Pump Foreline Exhaust Static Pressure [mbar] *)
    ST_SPINDLE_ENC_502                  : REAL := 0.0;        (* Main Graphite Susceptor Planetary Drive Encoder [rpm] *)
    ST_SATELLITE_TACH_503               : REAL := 0.0;        (* Optical Tachometer for Gas-Foil Satellite Wafer Disk [rpm] *)
    PDT_GAS_FOIL_504                    : REAL := 0.0;        (* Satellite Levitation Gas-Foil Pocket Differential Pressure [mbar] *)
    PT_TMGA_BUBBLER_601                 : REAL := 1020.0;     (* Trimethylgallium Organometallic Bubbler Head Pressure [mbar] *)
    TT_TMGA_BATH_602                    : REAL := -10.0;      (* TMGa Constant Temperature Chiller Bath Temperature [deg C] *)
    PT_TMA_BUBBLER_603                  : REAL := 1020.0;     (* Trimethylaluminum Organometallic Bubbler Head Pressure [mbar] *)
    TT_TMA_BATH_604                     : REAL := 18.0;       (* TMA Constant Temperature Chiller Bath Temperature [deg C] *)
    PT_CP2MG_BUBBLER_605                : REAL := 1020.0;     (* Cp2Mg Solid Dopant Precursor Bubbler Pressure [mbar] *)
    TT_CP2MG_BATH_606                   : REAL := 25.0;       (* Cp2Mg Sublimation Heating Bath Temperature [deg C] *)
    PT_NH3_SUPPLY_701                   : REAL := 3.5;        (* Ultra-High-Purity Ammonia Header Supply Pressure [bar] *)
    PT_H2_CARRIER_702                   : REAL := 4.0;        (* Palladium-Purified Hydrogen Carrier Gas Supply [bar] *)
    PT_N2_CARRIER_703                   : REAL := 4.0;        (* Getter-Purified Nitrogen Carrier Gas Supply [bar] *)
    TT_SCRUBBER_801                     : REAL := 850.0;      (* Thermal Burn-Box Scrubber Combustion Chamber Temp [deg C] *)
    FT_SCRUBBER_H2O_802                 : REAL := 45.0;       (* Wet Scrubbing Column Recirculation Water Flow Rate [l/min] *)
    AT_TOXIC_LEAK_901                   : REAL := 0.0;        (* Hydride (NH3/SiH4) & Pyrophoric Vapor Sniffer Leak Detector [ppm] *)
    bRF_Crowbar_Tripped_In              : BOOL := FALSE;      (* RF Generator Fast Thyristor Crowbar Hardware Trip Status [bool] *)
    bLoadLockCassetteLoaded             : BOOL := FALSE;      (* Substrate wafer transfer robot cassette presence flag [bool] *)
    bLoadLockGateValveOpen              : BOOL := FALSE;      (* High-vacuum gate valve position between load-lock and reactor [bool] *)

    (* === RECIPE SETPOINTS & TARGET TRAJECTORIES === *)
    rSetp_InnerTemp_degC                : REAL := 1050.0;     (* Target Inner Zone Pyrometer Temperature Setpoint [deg C] *)
    rSetp_MiddleTemp_degC               : REAL := 1050.0;     (* Target Middle Zone Pyrometer Temperature Setpoint [deg C] *)
    rSetp_OuterTemp_degC                : REAL := 1050.0;     (* Target Outer Zone Pyrometer Temperature Setpoint [deg C] *)
    rSetp_ChamberPressure_mbar          : REAL := 200.0;      (* Target Reactor Chamber Static Pressure Setpoint [mbar] *)
    rSetp_SusceptorSpeed_rpm            : REAL := 50.0;       (* Target Planetary Main Graphite Plate Rotation Speed [rpm] *)
    rSetp_TMGa_Flow_sccm                : REAL := 120.0;      (* Target TMGa Organometallic Precursor Mass Flow [sccm] *)
    rSetp_NH3_Flow_slm                  : REAL := 25.0;       (* Target Ammonia Precursor Mass Flow [slm] *)
    rSetp_TMA_Flow_sccm                 : REAL := 0.0;        (* Target TMA Precursor Mass Flow for AlN Nucleation [sccm] *)
    rSetp_Cp2Mg_Flow_sccm               : REAL := 0.0;        (* Target Cp2Mg Dopant Precursor Mass Flow [sccm] *)
    rSetp_Carrier_H2_slm                : REAL := 40.0;       (* Target Purified Hydrogen Main Carrier Gas Flow [slm] *)
    rSetp_Carrier_N2_slm                : REAL := 10.0;       (* Target Purified Nitrogen Secondary Carrier Gas Flow [slm] *)
    rTarget_EpilayerThickness_nm        : REAL := 2500.0;     (* Total Final Epitaxial Target Growth Thickness [nm] *)
END_VAR

VAR_OUTPUT
    (* === ANALOG ACTUATOR COMMANDS === *)
    rCmd_RF_Power_InnerZone_Pct         : REAL := 0.0;        (* RF Induction Generator Inner Coil Power Setpoint [0..100 %] *)
    rCmd_RF_Power_MiddleZone_Pct        : REAL := 0.0;        (* RF Induction Generator Middle Coil Power Setpoint [0..100 %] *)
    rCmd_RF_Power_OuterZone_Pct         : REAL := 0.0;        (* RF Induction Generator Outer Coil Power Setpoint [0..100 %] *)
    rCmd_ThrottleValve_Opening_Pct      : REAL := 100.0;      (* Heated Pressure Control Butterfly Throttle Valve Angle [0..100 %] *)
    rCmd_TMGa_MFC_Flow_sccm             : REAL := 0.0;        (* Mass Flow Controller Setpoint for TMGa Bubbler Line [sccm] *)
    rCmd_NH3_MFC_Flow_slm               : REAL := 0.0;        (* Mass Flow Controller Setpoint for Ammonia Feed Line [slm] *)
    rCmd_TMA_MFC_Flow_sccm              : REAL := 0.0;        (* Mass Flow Controller Setpoint for TMA Bubbler Line [sccm] *)
    rCmd_Cp2Mg_MFC_Flow_sccm            : REAL := 0.0;        (* Mass Flow Controller Setpoint for Cp2Mg Line [sccm] *)
    rCmd_H2_Main_Carrier_MFC_slm        : REAL := 0.0;        (* Mass Flow Controller Setpoint for H2 Carrier Gas [slm] *)
    rCmd_N2_Purge_MFC_slm               : REAL := 0.0;        (* Mass Flow Controller Setpoint for N2 Purge Line [slm] *)
    rCmd_Susceptor_Motor_Torque_Nm      : REAL := 0.0;        (* Planetary Spindle Servo Inverter Command Torque [Nm] *)
    rCmd_GasFoil_Levitation_Flow_sccm   : REAL := 0.0;        (* Satellite Pocket Levitation Flow Controller Command [sccm] *)

    (* === DISCRETE ACTUATOR COMMANDS & FAST VALVES === *)
    bCmd_TMGa_RunVent_Solenoid          : BOOL := FALSE;      (* Sub-25ms Double-Block-and-Bleed TMGa Run (True) / Vent (False) [bool] *)
    bCmd_TMA_RunVent_Solenoid           : BOOL := FALSE;      (* Sub-25ms Double-Block-and-Bleed TMA Run (True) / Vent (False) [bool] *)
    bCmd_Cp2Mg_RunVent_Solenoid         : BOOL := FALSE;      (* Fast Run (True) / Vent (False) Valve for Cp2Mg Dopant Line [bool] *)
    bCmd_NH3_FastIsolation_Valve        : BOOL := FALSE;      (* High-Speed Pneumatic Safety Isolation Valve for NH3 Hydride [bool] *)
    bCmd_H2_EmergencyShutoff_Valve      : BOOL := FALSE;      (* Explosive Atmosphere Failsafe Isolation Valve for H2 Feed [bool] *)
    bCmd_N2_FastBallast_Flood_Valve     : BOOL := FALSE;      (* Reactor Chamber Nitrogen Safety Backfill and Ballast Valve [bool] *)
    bCmd_RF_Generator_Enable            : BOOL := FALSE;      (* Master RF Induction Inverter Inhibit / Enable Command [bool] *)
    bCmd_Emergency_Crowbar_Fire         : BOOL := FALSE;      (* Failsafe Fast Trigger for RF Inverter Crowbar Dump [bool] *)
    bCmd_VacuumRoughing_Valve           : BOOL := FALSE;      (* Chamber Vacuum Mechanical Roughing Valve Command [bool] *)
    bCmd_TurboMolecular_Foreline_Valve  : BOOL := FALSE;      (* High-Vacuum Turbomolecular Isolation Valve Command [bool] *)

    (* === FILTERED & 2oo3 VOTED PROCESS VALUES === *)
    rVoted_InnerTemp_degC               : REAL := 25.0;       (* 2oo3 Voted Inner Susceptor Pyrometer Temperature [deg C] *)
    rVoted_MiddleTemp_degC              : REAL := 25.0;       (* 2oo3 Voted Middle Susceptor Pyrometer Temperature [deg C] *)
    rVoted_OuterTemp_degC               : REAL := 25.0;       (* 2oo3 Voted Outer Susceptor Pyrometer Temperature [deg C] *)
    rVoted_ChamberPressure_mbar         : REAL := 1013.25;    (* 2oo3 Voted Chamber Total Static Pressure [mbar] *)
    rVoted_Reflectance_Counts           : REAL := 1000.0;     (* 2oo3 Voted 405 nm Optical Reflectometer Intensity [counts] *)

    (* === CYBER-PHYSICAL STATE ESTIMATES (x_hat) === *)
    rEst_InnerTemp_degC                 : REAL := 25.0;       (* Observer State 1: Inner Susceptor Temperature [deg C] *)
    rEst_MiddleTemp_degC                : REAL := 25.0;       (* Observer State 2: Middle Susceptor Temperature [deg C] *)
    rEst_OuterTemp_degC                 : REAL := 25.0;       (* Observer State 3: Outer Susceptor Temperature [deg C] *)
    rEst_ChamberPressure_mbar           : REAL := 1013.25;    (* Observer State 4: Reactor Total Static Pressure [mbar] *)
    rEst_SatelliteSpeed_rpm             : REAL := 0.0;        (* Observer State 5: Gas-Foil Satellite Wafer Disk Speed [rpm] *)
    rEst_NH3_Boundary_mbar              : REAL := 0.0;        (* Observer State 6: Ammonia Partial Pressure in Boundary Layer [mbar] *)
    rEst_EpilayerThickness_nm           : REAL := 0.0;        (* Observer State 7: In-Situ Integrated Epilayer Thickness [nm] *)
    rEst_GaN_GrowthRate_um_h            : REAL := 0.0;        (* Observer State 8: Real-Time Crystal Deposition Growth Rate [um/h] *)

    (* === TELEMETRY, STATUS & ALARM WORDS === *)
    dwStatusWord1_CoreState             : DWORD := 16#00000000; (* Bit-packed 32-bit Core Operational & Subsystem Status [DWORD] *)
    dwStatusWord2_Subsystem             : DWORD := 16#00000000; (* Bit-packed 32-bit TMR Health & Automation Progression [DWORD] *)
    dwAlarmWord1_CriticalTrips          : DWORD := 16#00000000; (* Bit-packed 32-bit ISA-18.2 Priority 1 Critical Trips [DWORD] *)
    dwAlarmWord2_ProcessWarnings        : DWORD := 16#00000000; (* Bit-packed 32-bit ISA-18.2 Priority 2 Process Warnings [DWORD] *)
    dwFirstOutWord_RootCause            : DWORD := 16#00000000; (* Bit-packed 32-bit Latching First-Out Safety Trip Root Cause [DWORD] *)
    eActiveState_FSM                    : INT := 0;             (* Active Index of 14-Stage Epitaxy Finite State Machine [int] *)
    uiActiveSubStep                     : UINT := 0;            (* Internal Sub-Step Counter of Current Production Stage [uint] *)
    rStageElapsedTime_sec               : REAL := 0.0;          (* Cumulative Execution Time in Active FSM Stage [s] *)
    rTotalRecipeTime_sec                : REAL := 0.0;          (* Cumulative Total Recipe Run Time Since Start [s] *)
    bReactorEpitaxyCycleComplete        : BOOL := FALSE;        (* Handshake Flag Signifying Successful Epilayer Growth [bool] *)
    bEmergencyTripActive                : BOOL := FALSE;        (* Master Safety Trip Active Flag Requiring Operator Reset [bool] *)
END_VAR
"""
