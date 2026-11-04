import os
import sys
import json
import uuid
import re

# We will generate the Function Block code in chunks to ensure maximum engineering rigor,
# extreme token density, zero placeholders, and exact delimiter parity.

def generate_iec_code():
    chunks = []
    
    # -------------------------------------------------------------------------
    # 1. HEADER & DECLARATION
    # -------------------------------------------------------------------------
    chunks.append("""FUNCTION_BLOCK FB_Aerospace_HypersonicTunnel_CryoAir_PebbleHeater
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: CPS-AERO-HYPERSONIC-M7-PEBBLE-CRYO-001
  INDUSTRY DOMAIN: AEROSPACE DEFENSE & HIGH-ENTHALPY GROUND TEST FACILITIES
  EQUIPMENT DESIGNATION: MACH 7 CONTINUOUS BLOWDOWN HYPERSONIC WIND TUNNEL HIGH-ENTHALPY FACILITY
====================================================================================================
  FACILITY ARCHITECTURAL OVERVIEW:
  This Function Block executes the real-time deterministic cyber-physical control, state-space
  estimation, triple modular redundant (2oo3 TMR) instrumentation voting, receding-horizon model
  predictive control (MPC), and ISA-18.2 compliant safety trip logic for a high-enthalpy continuous
  blowdown Mach 7 hypersonic wind tunnel facility.

  CORE PROCESS SUBSYSTEMS INTEGRATED:
  1. Ultra-High Pressure/High Temperature Zirconia (ZrO2) Pebble-Bed Regenerative Storage Heater:
     - Operating Stagnation Pressure: up to 150.0 bar [15.0 MPa]
     - Operating Stagnation Temperature: up to 2,200.0 K (1,926.85 deg C)
     - Core Thermal Storage: 45.0 GJ sensible heat stored in high-purity yttria-stabilized zirconia
       spheres (19 mm diameter, bed void fraction eps = 0.40, total bed height 8.5 m).
     - Axial Multi-Node Schumann Regenerative Gas-Solid Heat Transfer Finite Difference Engine.
  2. Actively Cryogenic-Cooled Convergent-Divergent Contoured Hypersonic Nozzle Throat:
     - Nozzle Throat Diameter: 100.0 mm (Area A* = 0.007854 m^2). Contoured expansion to 1.0 m^2 exit.
     - Active Aerodynamic Heat Flux: up to 18.0 MW/m^2 under Mach 7 high-enthalpy stagnation.
     - Liquid Nitrogen (LN2) High-Pressure Micro-Channel Cooling Jacket (T_sat = 77.4 K at 1.0 bar).
     - Bartz Empirical Convective Heat Transfer Equation & Kutateladze Boiling Burnout Observer.
  3. Fast Electro-Hydraulic Throttle Valve Actuator:
     - Full-Stroke Travel Time: < 150.0 ms with high-bandwidth servo-hydraulic spool valve.
     - Aerodynamic Mass Flow Regulation up to 120.0 kg/s choked hot air.
  4. Multi-Stage Steam Ejector Vacuum Sphere Backpressure Matching Subsystem:
     - Downstream 5,000 m^3 Vacuum Receiver Sphere (evacuation down to 5.0 mbar absolute).
     - Second-throat supersonic variable-geometry diffuser backpressure matching.
  5. High-Speed Optical Schlieren Oblique Shockwave Angle Observer:
     - Calibrated 15.0 deg Half-Angle Diamond Wedge Model mounted in test cabin.
     - High-speed camera frame rate 50 kHz with optical edge detection measuring shock wave angle beta.
     - Closed-form and Newton-Raphson inverse theta-beta-Mach shock relation observer.
  6. ISA-84 / IEC 61508 SIL-3 Hardwired and Fast-Trip Software Interlocks:
     - Hypersonic Supersonic Diffuser Unstart Detachment Fast-Trip (< 5.0 ms reaction time).
     - Throat Thermal Runaway and Leidenfrost Film Boiling Burnout Protection.

  DETERMINISTIC EXECUTION TIME BASE: 500 us (Microseconds) per PLC Cycle.
====================================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # 2. VAR_INPUT
    # -------------------------------------------------------------------------
    chunks.append("""VAR_INPUT
    (* === P&ID TRANSMITTER CHANNELS: 2oo3 TRIPLE MODULAR REDUNDANCY TRIPLETS === *)
    (* Pebble Bed Storage Heater Top Dome Pressure Transmitters [bar] *)
    PT_PEBBLE_BED_TOP_101A             : REAL; (* [bar] Pebble Bed Pressure Top Channel A (0.0 to 200.0 bar) *)
    PT_PEBBLE_BED_TOP_101B             : REAL; (* [bar] Pebble Bed Pressure Top Channel B (0.0 to 200.0 bar) *)
    PT_PEBBLE_BED_TOP_101C             : REAL; (* [bar] Pebble Bed Pressure Top Channel C (0.0 to 200.0 bar) *)

    (* Pebble Bed Core High-Enthalpy Ceramic Thermocouple Triplets [K] *)
    TT_PEBBLE_BED_CORE_201A            : REAL; (* [K] Pebble Bed Core Temperature Channel A (300.0 to 2500.0 K) *)
    TT_PEBBLE_BED_CORE_201B            : REAL; (* [K] Pebble Bed Core Temperature Channel B (300.0 to 2500.0 K) *)
    TT_PEBBLE_BED_CORE_201C            : REAL; (* [K] Pebble Bed Core Temperature Channel C (300.0 to 2500.0 K) *)

    (* Nozzle Stagnation Chamber Total Pressure Transducers [bar] *)
    PT_NOZZLE_STAGNATION_301A          : REAL; (* [bar] Stagnation Chamber Pressure P_0 Channel A (0.0 to 180.0 bar) *)
    PT_NOZZLE_STAGNATION_301B          : REAL; (* [bar] Stagnation Chamber Pressure P_0 Channel B (0.0 to 180.0 bar) *)
    PT_NOZZLE_STAGNATION_301C          : REAL; (* [bar] Stagnation Chamber Pressure P_0 Channel C (0.0 to 180.0 bar) *)

    (* Nozzle Throat Inner Copper Wall Thermocouple Arrays [K] *)
    TT_NOZZLE_THROAT_WALL_401A         : REAL; (* [K] Nozzle Throat Inner Wall Temp Channel A (70.0 to 800.0 K) *)
    TT_NOZZLE_THROAT_WALL_401B         : REAL; (* [K] Nozzle Throat Inner Wall Temp Channel B (70.0 to 800.0 K) *)
    TT_NOZZLE_THROAT_WALL_401C         : REAL; (* [K] Nozzle Throat Inner Wall Temp Channel C (70.0 to 800.0 K) *)

    (* Cryogenic Liquid Nitrogen (LN2) Jacket Coolant Coriolis Mass Flow [kg/s] *)
    FT_LN2_COOLANT_501A                : REAL; (* [kg/s] Cryo LN2 Coolant Mass Flow Channel A (0.0 to 40.0 kg/s) *)
    FT_LN2_COOLANT_501B                : REAL; (* [kg/s] Cryo LN2 Coolant Mass Flow Channel B (0.0 to 40.0 kg/s) *)
    FT_LN2_COOLANT_501C                : REAL; (* [kg/s] Cryo LN2 Coolant Mass Flow Channel C (0.0 to 40.0 kg/s) *)

    (* Supersonic Diffuser Exit Recovery Static Pressure [bar] *)
    PT_DIFFUSER_EXIT_601A              : REAL; (* [bar] Diffuser Exit Static Pressure Channel A (0.001 to 2.0 bar) *)
    PT_DIFFUSER_EXIT_601B              : REAL; (* [bar] Diffuser Exit Static Pressure Channel B (0.001 to 2.0 bar) *)
    PT_DIFFUSER_EXIT_601C              : REAL; (* [bar] Diffuser Exit Static Pressure Channel C (0.001 to 2.0 bar) *)

    (* Test Section Cabin Supersonic Free-Stream Static Pressure Transducers [bar] *)
    PT_TEST_CABIN_STATIC_701A          : REAL; (* [bar] Test Cabin Static Wall Pressure Channel A (0.0001 to 0.50 bar) *)
    PT_TEST_CABIN_STATIC_701B          : REAL; (* [bar] Test Cabin Static Wall Pressure Channel B (0.0001 to 0.50 bar) *)
    PT_TEST_CABIN_STATIC_701C          : REAL; (* [bar] Test Cabin Static Wall Pressure Channel C (0.0001 to 0.50 bar) *)

    (* High-Speed Schlieren Oblique Shockwave Angle Optical Transmitters [deg] *)
    AIT_SCHLIEREN_SHOCK_ANGLE_801A     : REAL; (* [deg] High-Speed Schlieren Oblique Shock Angle A (15.0 to 45.0 deg) *)
    AIT_SCHLIEREN_SHOCK_ANGLE_801B     : REAL; (* [deg] High-Speed Schlieren Oblique Shock Angle B (15.0 to 45.0 deg) *)
    AIT_SCHLIEREN_SHOCK_ANGLE_801C     : REAL; (* [deg] High-Speed Schlieren Oblique Shock Angle C (15.0 to 45.0 deg) *)

    (* === FACILITY OPERATIONAL COMMANDS & PERMISSIVE INPUTS === *)
    bEmergencyStop                     : BOOL; (* [bool] Facility Hardwired SIL-3 Safety Circuit Emergency Trip *)
    bStartBlowdownSequence             : BOOL; (* [bool] Operator Trigger: Initiate Automated Mach 7 Blowdown *)
    bAbortBlowdownSequence             : BOOL; (* [bool] Operator Trigger: Manual Controlled Blowdown Abort *)
    bAcknowledgeAlarms                 : BOOL; (* [bool] Operator Alarm & Trip Manual Acknowledgment Pushbutton *)
    bEnablePitchSweep                  : BOOL; (* [bool] Enable Dynamic Aerodynamic Pitch AoA Model Sector Sweep *)
    rTargetMachNumber                  : REAL; (* [-] Commanded Free-Stream Test Mach Number Setpoint (Nominal 7.00) *)
    rTargetStagnationPressure          : REAL; (* [bar] Commanded Nozzle Total Pressure P_0 (50.0 to 150.0 bar) *)
    rTargetStagnationTemperature       : REAL; (* [K] Commanded Total Temperature T_0 (1200.0 to 2200.0 K) *)
    rTestCabinAoA_Command              : REAL; (* [deg] Desired Model Pitch Angle of Attack (-5.0 to +25.0 deg) *)
    rVacuumSpherePressure              : REAL; (* [bar] Downstream Vacuum Receiver Sphere Absolute Static Pressure *)
    rSteamBoilerSupplyPressure         : REAL; (* [bar] Multi-Stage Motive Steam Supply Header Pressure (10.0 to 40.0 bar) *)
    rAtmosphericPressure               : REAL; (* [bar] Ambient Atmospheric Barometric Reference Pressure *)
    tCycleTime                         : TIME; (* [ms] Controller Deterministic Task Cycle Time Base (0.5 to 1.0 ms) *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 3. VAR_OUTPUT
    # -------------------------------------------------------------------------
    chunks.append("""VAR_OUTPUT
    (* === HIGH-BANDWIDTH ACTUATOR ANALOG COMMAND SIGNALS (0.0 to 100.0 %) === *)
    rActuator_ThrottleValve_Cmd        : REAL; (* [%] Fast Electro-Hydraulic Main Throttle Valve Position (0-100%) *)
    rActuator_LN2CoolantValve_Cmd      : REAL; (* [%] Cryogenic LN2 Jacket Injection Proportional Control Valve (0-100%) *)
    rActuator_SteamEjector_Cmd         : REAL; (* [%] Multi-Stage Motive Steam Ejector Supply Pressure Valve (0-100%) *)
    rActuator_DiffuserThroat_Cmd       : REAL; (* [%] Supersonic Diffuser Second Throat Variable Geometry Ram (0-100%) *)
    rActuator_PreheaterThyristor_Cmd   : REAL; (* [%] Zirconia Pebble Bed Electrical Resistance Heater Bank (0-100%) *)
    rActuator_FastDumpValve_Cmd        : REAL; (* [%] Emergency Fast Overpressure Safety Vent Valve (0-100%) *)
    rActuator_IsolationValve_Cmd       : REAL; (* [%] Main Fast-Acting High-Enthalpy Isolation Gate Valve (0-100%) *)

    (* === SYNTHESIZED AERODYNAMIC & THERMAL OBSERVER TELEMETRY === *)
    rObserved_MachNumber               : REAL; (* [-] Real-Time Calculated Test Section Core Free-Stream Mach Number *)
    rObserved_ThroatHeatFlux_MWm2      : REAL; (* [MW/m2] Real-Time Bartz-Equation Calculated Throat Heat Flux *)
    rObserved_SchlierenShockAngle      : REAL; (* [deg] Validated Optical Schlieren Diamond Wedge Shock Angle *)
    rObserved_TotalMassFlow_kgs        : REAL; (* [kg/s] Total Choked Air Mass Flow through Nozzle Throat *)
    rObserved_DynamicPressure_kPa      : REAL; (* [kPa] Hypersonic Test Section Free-Stream Dynamic Pressure q_inf *)
    rObserved_ReynoldsUnit_per_m       : REAL; (* [1/m] Unit Reynolds Number in Hypersonic Test Cabin (Re/L) *)
    rObserved_PebbleBedEnthalpy_MJ     : REAL; (* [MJ] Usable Thermal Enthalpy Remaining in Ceramic Storage Matrix *)
    rObserved_NozzleWallSafetyMargin   : REAL; (* [%] Thermal Stress Margin before Copper Throat Material Yield *)
    rObserved_DiffuserPressureRatio    : REAL; (* [-] Diffuser Static Pressure Recovery Ratio (P_diff / P_cabin) *)
    rModel_PitchAngle_Actual           : REAL; (* [deg] Model Actuation Sector Current Pitch Angle Telemetry *)

    (* === DISCRETE STATUS, INTERLOCKS & FSM TELEMETRY === *)
    bTunnelUnstart_TripActive          : BOOL; (* [bool] Hypersonic Supersonic Diffuser Unstart Fast-Trip Active *)
    bThroatThermalRunaway_TripActive   : BOOL; (* [bool] Nozzle Throat Critical Heat Flux Burnout Fast-Trip Active *)
    bBlowdownRun_Active                : BOOL; (* [bool] Steady-State High-Enthalpy Blowdown Testing In Progress *)
    bFacilityReadyForBlowdown          : BOOL; (* [bool] All Facility Permissives Satisfied for Blowdown Initiation *)
    bSystemHealthy                     : BOOL; (* [bool] Master Facility Status: Normal Operation, No SIL Trips *)
    iCurrentFSM_State                  : INT;  (* [-] Current Operational FSM State Identifier (0 to 11) *)

    (* === ISA-18.2 DIAGNOSTIC & ALARM PACKED BITFIELDS === *)
    dwSystemStatusWord                 : DWORD; (* [-] 32-Bit Operational Automation Status Bitmask *)
    dwAlarmWord_Critical               : DWORD; (* [-] ISA-18.2 Priority 1 / SIL-3 Emergency Trip Bitfield *)
    dwAlarmWord_HighWarning            : DWORD; (* [-] ISA-18.2 Priority 2 / Severe Warning Bitfield *)
    dwAlarmWord_LowWarning             : DWORD; (* [-] ISA-18.2 Priority 3 / Low Advisory Warning Bitfield *)
    dwSensorHealthWord                 : DWORD; (* [-] TMR 2oo3 Sensor Subsystem Health and Discrepancy Bitfield *)
    dwActuatorStatusWord               : DWORD; (* [-] Actuator Servo Health and Clamping Saturation Bitfield *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 4. VAR - State space, MPC, TMR structures, FSM variables
    # -------------------------------------------------------------------------
    chunks.append("""VAR
    (* =========================================================================
       INTERNAL STATE-SPACE MATRICES & VECTORS (8x8 State-Space Formulation)
       x[k+1] = A * x[k] + B * u[k]
       y[k]   = C * x[k] + D * u[k]
       State Vector x (8 Dimensions):
         x[1] = P_0: Nozzle Stagnation Total Pressure [bar]
         x[2] = T_0: Nozzle Stagnation Total Temperature [K]
         x[3] = T_throat: Nozzle Throat Inner Copper Wall Temperature [K]
         x[4] = P_cabin: Test Cabin Free-Stream Static Wall Pressure [bar]
         x[5] = P_diff: Supersonic Diffuser Exit Recovery Pressure [bar]
         x[6] = Beta_shock: Oblique Shock Wave Attachment Angle [deg]
         x[7] = T_ln2_film: LN2 Coolant Film Temperature at Throat Jacket [K]
         x[8] = T_pebble_core: Pebble Bed Ceramic Matrix Core Temperature [K]
       Control Input Vector u (6 Dimensions):
         u[1] = u_throttle: Electro-Hydraulic Throttle Valve Position [%]
         u[2] = u_ln2: Cryogenic LN2 Jacket Injection Control Valve [%]
         u[3] = u_ejector: Multi-Stage Motive Steam Ejector Pressure Valve [%]
         u[4] = u_diffuser: Diffuser Second Throat Variable Geometry Ram [%]
         u[5] = u_preheat: Pebble Bed Electrical Resistance Heater Power [%]
         u[6] = u_dump: Emergency Overpressure Fast Vent Dump Valve [%]
       ========================================================================= *)
    matA                               : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix A (8x8) *)
    matB                               : ARRAY[1..8, 1..6] OF REAL; (* Discrete Control Input Matrix B (8x6) *)
    matC                               : ARRAY[1..8, 1..8] OF REAL; (* Measurement Output Matrix C (8x8) *)
    matD                               : ARRAY[1..8, 1..6] OF REAL; (* Direct Feedforward Transmission Matrix D (8x6) *)
    matL                               : ARRAY[1..8, 1..8] OF REAL; (* Discrete Luenberger / Kalman Observer Gain Matrix (8x8) *)

    vecX_hat                           : ARRAY[1..8] OF REAL; (* Current Estimated Continuous State Vector x_hat *)
    vecX_pred                          : ARRAY[1..8] OF REAL; (* One-Step Ahead Discrete Predicted State Vector *)
    vecY_meas                          : ARRAY[1..8] OF REAL; (* Validated 2oo3 TMR Sensor Measurement Vector y *)
    vecY_est                           : ARRAY[1..8] OF REAL; (* Observer Estimated Output Vector y_hat = C * x_hat *)
    vecY_err                           : ARRAY[1..8] OF REAL; (* Innovation Residual Vector e = y - y_hat *)
    vecX_ref                           : ARRAY[1..8] OF REAL; (* Dynamic State Trajectory Reference Vector r *)
    vecU_cmd                           : ARRAY[1..6] OF REAL; (* Current Optimal Control Command Vector u *)
    vecU_prev                          : ARRAY[1..6] OF REAL; (* Previous Cycle Control Command Vector u[k-1] *)
    vecDeltaU                          : ARRAY[1..6] OF REAL; (* Actuator Rate Slew Increment Vector delta_u *)

    (* Model Predictive Control (MPC) Cost Weighting Arrays *)
    vecQ_diag                          : ARRAY[1..8] OF REAL; (* State Tracking Error Quadratic Penalty Diagonal Q *)
    vecR_diag                          : ARRAY[1..6] OF REAL; (* Control Actuation Effort Quadratic Penalty Diagonal R *)
    vecS_diag                          : ARRAY[1..6] OF REAL; (* Actuator Slew Rate Increment Penalty Diagonal S *)
    vecP_diag                          : ARRAY[1..8] OF REAL; (* Terminal State Cost Horizon Penalty Diagonal P *)

    (* Receding-Horizon MPC Optimization Scratchpad (Horizon N = 5 Steps) *)
    arrMPC_X_traj                      : ARRAY[1..5, 1..8] OF REAL; (* Predicted State Trajectory across Horizon *)
    arrMPC_U_traj                      : ARRAY[1..5, 1..6] OF REAL; (* Optimized Control Input Sequence *)
    arrMPC_Lambda                      : ARRAY[1..5, 1..8] OF REAL; (* Costate / Lagrange Multiplier Backward Trajectory *)
    arrMPC_GradU                       : ARRAY[1..5, 1..6] OF REAL; (* Projected Gradient Sequence dJ/du *)
    vecU_min                           : ARRAY[1..6] OF REAL; (* Lower Bound Box Actuator Constraints [%] *)
    vecU_max                           : ARRAY[1..6] OF REAL; (* Upper Bound Box Actuator Constraints [%] *)
    vecSlew_max                        : ARRAY[1..6] OF REAL; (* Maximum Allowable Slew Rate [% / sec] *)

    (* =========================================================================
       2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING STRUCTURES & DISCREPANCY TIMERS
       ========================================================================= *)
    (* Channel 1: Pebble Bed Top Dome Pressure (PT-101) *)
    rVoted_PT101                       : REAL;
    bFault_PT101A                      : BOOL;
    bFault_PT101B                      : BOOL;
    bFault_PT101C                      : BOOL;
    bDegraded_PT101                    : BOOL;
    bTrip_PT101                        : BOOL;
    rTimer_PT101_AB                    : REAL;
    rTimer_PT101_BC                    : REAL;
    rTimer_PT101_CA                    : REAL;

    (* Channel 2: Pebble Bed Core Temperature (TT-201) *)
    rVoted_TT201                       : REAL;
    bFault_TT201A                      : BOOL;
    bFault_TT201B                      : BOOL;
    bFault_TT201C                      : BOOL;
    bDegraded_TT201                    : BOOL;
    bTrip_TT201                        : BOOL;
    rTimer_TT201_AB                    : REAL;
    rTimer_TT201_BC                    : REAL;
    rTimer_TT201_CA                    : REAL;

    (* Channel 3: Nozzle Stagnation Total Pressure (PT-301) *)
    rVoted_PT301                       : REAL;
    bFault_PT301A                      : BOOL;
    bFault_PT301B                      : BOOL;
    bFault_PT301C                      : BOOL;
    bDegraded_PT301                    : BOOL;
    bTrip_PT301                        : BOOL;
    rTimer_PT301_AB                    : REAL;
    rTimer_PT301_BC                    : REAL;
    rTimer_PT301_CA                    : REAL;

    (* Channel 4: Nozzle Throat Inner Wall Temperature (TT-401) *)
    rVoted_TT401                       : REAL;
    bFault_TT401A                      : BOOL;
    bFault_TT401B                      : BOOL;
    bFault_TT401C                      : BOOL;
    bDegraded_TT401                    : BOOL;
    bTrip_TT401                        : BOOL;
    rTimer_TT401_AB                    : REAL;
    rTimer_TT401_BC                    : REAL;
    rTimer_TT401_CA                    : REAL;

    (* Channel 5: LN2 Coolant Mass Flow Rate (FT-501) *)
    rVoted_FT501                       : REAL;
    bFault_FT501A                      : BOOL;
    bFault_FT501B                      : BOOL;
    bFault_FT501C                      : BOOL;
    bDegraded_FT501                    : BOOL;
    bTrip_FT501                        : BOOL;
    rTimer_FT501_AB                    : REAL;
    rTimer_FT501_BC                    : REAL;
    rTimer_FT501_CA                    : REAL;

    (* Channel 6: Supersonic Diffuser Exit Static Pressure (PT-601) *)
    rVoted_PT601                       : REAL;
    bFault_PT601A                      : BOOL;
    bFault_PT601B                      : BOOL;
    bFault_PT601C                      : BOOL;
    bDegraded_PT601                    : BOOL;
    bTrip_PT601                        : BOOL;
    rTimer_PT601_AB                    : REAL;
    rTimer_PT601_BC                    : REAL;
    rTimer_PT601_CA                    : REAL;

    (* Channel 7: Test Cabin Free-Stream Static Wall Pressure (PT-701) *)
    rVoted_PT701                       : REAL;
    bFault_PT701A                      : BOOL;
    bFault_PT701B                      : BOOL;
    bFault_PT701C                      : BOOL;
    bDegraded_PT701                    : BOOL;
    bTrip_PT701                        : BOOL;
    rTimer_PT701_AB                    : REAL;
    rTimer_PT701_BC                    : REAL;
    rTimer_PT701_CA                    : REAL;

    (* Channel 8: High-Speed Schlieren Oblique Shock Angle (AIT-801) *)
    rVoted_AIT801                      : REAL;
    bFault_AIT801A                     : BOOL;
    bFault_AIT801B                     : BOOL;
    bFault_AIT801C                     : BOOL;
    bDegraded_AIT801                   : BOOL;
    bTrip_AIT801                       : BOOL;
    rTimer_AIT801_AB                   : REAL;
    rTimer_AIT801_BC                   : REAL;
    rTimer_AIT801_CA                   : REAL;

    (* =========================================================================
       HIGH-ENTHALPY THERMODYNAMIC & GAS DYNAMICS OBSERVER INTERNAL VARIABLES
       ========================================================================= *)
    (* High-Temperature Real Air Equilibrium Properties *)
    rAirGasConstant_R                  : REAL := 287.058; (* [J/(kg*K)] Individual Gas Constant for Air *)
    rAirGamma_Ratio                    : REAL;            (* [-] Real-Gas Temperature-Dependent Specific Heat Ratio *)
    rAirCp_SpecHeat                    : REAL;            (* [J/(kg*K)] Real-Gas Isobaric Specific Heat *)
    rAirDynamicViscosity_mu            : REAL;            (* [Pa*s] Real Dynamic Viscosity via Sutherland's Law *)
    rAirSonicSpeed_Throat              : REAL;            (* [m/s] Critical Speed of Sound at Choked Throat a* *)
    rAirCriticalPressure_Pstar         : REAL;            (* [bar] Critical Choking Pressure at Nozzle Throat P* *)
    rAirCriticalDensity_rhostar        : REAL;            (* [kg/m^3] Critical Choking Density at Nozzle Throat rho* *)
    rAirChokedMassFlow_mdot            : REAL;            (* [kg/s] Theoretical Isentropic Choked Air Mass Flow *)

    (* 5-Node Discretized Schumann Model for Regenerative Ceramic Pebble Bed *)
    (* Spatial Nodes 0 (Bed Bottom Cold Entry) to 4 (Bed Top High-Enthalpy Discharge) *)
    arrPebble_T_gas                    : ARRAY[0..4] OF REAL; (* [K] Fluid Gas Temperature at Spatial Slices *)
    arrPebble_T_solid                  : ARRAY[0..4] OF REAL; (* [K] Zirconia Pebble Solid Matrix Temp Slices *)
    arrPebble_P_slice                  : ARRAY[0..4] OF REAL; (* [bar] Pressure Profile across Bed Slices *)
    rPebble_VoidFraction               : REAL := 0.40;        (* [-] Packed Bed Interstitial Porosity *)
    rPebble_Diameter_dp                : REAL := 0.019;       (* [m] Spherical Ceramic Pebble Diameter (19 mm) *)
    rPebble_BedDiameter                : REAL := 1.50;        (* [m] Internal Diameter of Insulated Storage Vessel *)
    rPebble_BedArea                    : REAL := 1.7671;      (* [m^2] Vessel Cross-Sectional Area *)
    rPebble_SliceHeight                : REAL := 1.70;        (* [m] Axial Spatial Step Height (8.5 m / 5 nodes) *)
    rPebble_SliceVolume                : REAL := 3.0041;      (* [m^3] Volume per Spatial Discretization Slice *)
    rPebble_SolidDensity_rho           : REAL := 5680.0;      (* [kg/m^3] Density of Yttria-Stabilized Zirconia *)
    rPebble_SolidSpecHeat_Cs           : REAL := 550.0;       (* [J/(kg*K)] Specific Heat of Zirconia at High Temp *)
    rPebble_VolumetricHeatTransfer_hv  : REAL;                (* [W/(m^3*K)] Interfacial Heat Transfer Coefficient *)

    (* Bartz Empirical Throat Aerodynamic Convective Heat Flux Parameters *)
    rNozzle_ThroatDiameter             : REAL := 0.100;       (* [m] Throat Inner Diameter (100 mm) *)
    rNozzle_ThroatArea                 : REAL := 0.007854;    (* [m^2] Throat Cross-Section Area A* *)
    rNozzle_CurvatureRadius            : REAL := 0.150;       (* [m] Radius of Curvature at Throat Contouring *)
    rNozzle_ExitArea                   : REAL := 1.000;       (* [m^2] Hypersonic Test Cabin Exit Area A_exit *)
    rNozzle_AreaRatio                  : REAL := 127.3236;    (* [-] Geometric Expansion Ratio A_exit / A* *)
    rNozzle_RecoveryFactor_r           : REAL := 0.890;       (* [-] Turbulent Boundary Layer Recovery Factor *)
    rNozzle_AdiabaticWallTemp_Taw      : REAL;                (* [K] Adiabatic Wall Recovery Temperature *)
    rNozzle_BartzHeatTransferCoeff_hg  : REAL;                (* [W/(m^2*K)] Convective Heat Transfer Coeff at Throat *)
    rNozzle_CalculatedHeatFlux_qw      : REAL;                (* [W/m^2] Local Aerodynamic Heat Flux at Throat *)
    rNozzle_ThroatCopperYieldTemp      : REAL := 680.0;       (* [K] Thermal Stress Yield Threshold for CuCrZr Alloy *)

    (* Liquid Nitrogen (LN2) Jacket Cryogenic Cooling Thermodynamics *)
    rLN2_SaturationTemp_Tsat           : REAL := 77.36;       (* [K] Atmospheric Saturation Temperature of N2 *)
    rLN2_LatentHeatVap_hfg             : REAL := 199300.0;    (* [J/kg] Latent Heat of Vaporization *)
    rLN2_LiquidDensity_rho             : REAL := 808.0;       (* [kg/m^3] Subcooled Liquid Nitrogen Density *)
    rLN2_CriticalHeatFlux_CHF          : REAL := 22.5;        (* [MW/m^2] Kutateladze-Zuber Peak Nucleate Boiling CHF *)
    rLN2_CoolingPowerAbsorbed          : REAL;                (* [W] Total Thermal Heat Removed by LN2 Jacket *)

    (* Real-Time Optical Schlieren Diamond Wedge Aerodynamic Observer *)
    rWedge_HalfAngle_Theta_deg         : REAL := 15.0;        (* [deg] Diamond Calibration Wedge Half-Angle *)
    rWedge_HalfAngle_Theta_rad         : REAL := 0.261799;    (* [rad] Diamond Wedge Half-Angle in Radians *)
    rSchlieren_Beta_rad                : REAL;                (* [rad] Validated Oblique Shockwave Angle *)
    rSchlieren_InferredMach            : REAL;                (* [-] Aerodynamically Inverted Free-Stream Mach Number *)
    rSchlieren_BoundaryLayer_Disp      : REAL := 0.0018;      (* [m] Boundary Layer Displacement Thickness delta* *)

    (* Supersonic Diffuser Unstart Detachment Criterion *)
    rDiffuser_CriticalRecoveryRatio    : REAL := 0.185;       (* [-] Maximum Backpressure Ratio before Unstart *)
    rDiffuser_PressureDerivative       : REAL;                (* [bar/s] Rate of Change of Cabin Wall Pressure *)
    rDiffuser_PrevCabinPressure        : REAL;                (* [bar] Stored Previous Cycle Cabin Pressure *)

    (* =========================================================================
       12-STATE HYPERSONIC WIND TUNNEL FINITE STATE MACHINE (FSM)
       ========================================================================= *)
    iMachineState                      : INT := 0;            (* Current Internal Operational State Index *)
    iPreviousState                     : INT := 0;            (* State Retained from Preceding PLC Cycle *)
    rStateTimer_sec                    : REAL := 0.0;         (* Elapsed Residence Time within Current State [s] *)
    rStepWatchdog_sec                  : REAL := 0.0;         (* State-Specific Timeout Watchdog Monitor [s] *)
    rBlowdownElapsed_sec               : REAL := 0.0;         (* Active Hypersonic Blowdown Run Duration [s] *)
    rBlowdownMaxRunTime_sec            : REAL := 45.0;        (* Maximum Permissible High-Enthalpy Run Time [s] *)
    bStateFirstScan                    : BOOL := TRUE;        (* One-Shot Pulse on State Entry Transition *)
    bPreheatPermissiveMet              : BOOL := FALSE;       (* Permissive: Ceramic Core Storage Heated *)
    bChilldownPermissiveMet            : BOOL := FALSE;       (* Permissive: Nozzle Throat Jacket Subcooled *)
    bVacuumPermissiveMet               : BOOL := FALSE;       (* Permissive: Sphere Evacuated & Ejectors Ready *)

    (* Dynamic Model Pitch Angle Sector Sweep Profile *)
    rPitch_CurrentAngle                : REAL := 0.0;         (* Current Model Pitch AoA Telemetry [deg] *)
    rPitch_TargetAngle                 : REAL := 0.0;         (* Commanded Model Pitch Target [deg] *)
    rPitch_RateLimit_deg_s             : REAL := 2.50;        (* Maximum Model Angular Pitch Rate [deg/s] *)

    (* =========================================================================
       ISA-18.2 ALARM ENGINE: 5-TIER MULTI-VARIABLE MONITORING BLOCKS
       Variables Monitored:
         1: PT-101 (Pebble Bed Top Pressure, bar)
         2: TT-201 (Pebble Bed Core Temperature, K)
         3: PT-301 (Nozzle Stagnation Total Pressure, bar)
         4: TT-401 (Nozzle Throat Inner Wall Temp, K)
         5: FT-501 (Cryo LN2 Coolant Flow, kg/s)
         6: PT-601 (Diffuser Exit Static Pressure, bar)
         7: PT-701 (Test Cabin Free-Stream Pressure, bar)
         8: AIT-801 (Schlieren Oblique Shock Angle, deg)
       ========================================================================= *)
    (* Alarm Trip Limits: HI_HI, HI, LO, LO_LO, Rate-of-Change (ROC), Deadband *)
    rAlarm_PT101_HH                    : REAL := 168.0; (* [bar] *)
    rAlarm_PT101_H                     : REAL := 158.0; (* [bar] *)
    rAlarm_PT101_L                     : REAL := 20.0;  (* [bar] *)
    rAlarm_PT101_LL                    : REAL := 8.0;   (* [bar] *)
    rAlarm_PT101_ROC                   : REAL := 40.0;  (* [bar/s] *)
    rAlarm_PT101_DB                    : REAL := 2.0;   (* [bar] *)
    rAlarm_PT101_Prev                  : REAL;

    rAlarm_TT201_HH                    : REAL := 2350.0; (* [K] *)
    rAlarm_TT201_H                     : REAL := 2250.0; (* [K] *)
    rAlarm_TT201_L                     : REAL := 800.0;  (* [K] *)
    rAlarm_TT201_LL                    : REAL := 400.0;  (* [K] *)
    rAlarm_TT201_ROC                   : REAL := 50.0;   (* [K/min] *)
    rAlarm_TT201_DB                    : REAL := 15.0;   (* [K] *)
    rAlarm_TT201_Prev                  : REAL;

    rAlarm_PT301_HH                    : REAL := 162.0; (* [bar] *)
    rAlarm_PT301_H                     : REAL := 154.0; (* [bar] *)
    rAlarm_PT301_L                     : REAL := 45.0;  (* [bar] *)
    rAlarm_PT301_LL                    : REAL := 25.0;  (* [bar] *)
    rAlarm_PT301_ROC                   : REAL := 60.0;  (* [bar/s] *)
    rAlarm_PT301_DB                    : REAL := 1.5;   (* [bar] *)
    rAlarm_PT301_Prev                  : REAL;

    rAlarm_TT401_HH                    : REAL := 650.0; (* [K] Critical Copper Yield Margin *)
    rAlarm_TT401_H                     : REAL := 580.0; (* [K] High Thermal Surge *)
    rAlarm_TT401_L                     : REAL := 65.0;  (* [K] *)
    rAlarm_TT401_LL                    : REAL := 50.0;  (* [K] Cryogenic Freezing *)
    rAlarm_TT401_ROC                   : REAL := 150.0; (* [K/s] Thermal Shock Gradient *)
    rAlarm_TT401_DB                    : REAL := 8.0;   (* [K] *)
    rAlarm_TT401_Prev                  : REAL;

    rAlarm_FT501_HH                    : REAL := 38.0;  (* [kg/s] *)
    rAlarm_FT501_H                     : REAL := 32.0;  (* [kg/s] *)
    rAlarm_FT501_L                     : REAL := 6.0;   (* [kg/s] Insufficient Throat Cooling *)
    rAlarm_FT501_LL                    : REAL := 2.5;   (* [kg/s] Critical Loss of Coolant *)
    rAlarm_FT501_ROC                   : REAL := 18.0;  (* [kg/s^2] *)
    rAlarm_FT501_DB                    : REAL := 0.5;   (* [kg/s] *)
    rAlarm_FT501_Prev                  : REAL;

    rAlarm_PT601_HH                    : REAL := 0.90;  (* [bar] Imminent Diffuser Breakdown *)
    rAlarm_PT601_H                     : REAL := 0.65;  (* [bar] Diffuser Backpressure High *)
    rAlarm_PT601_L                     : REAL := 0.04;  (* [bar] *)
    rAlarm_PT601_LL                    : REAL := 0.005; (* [bar] *)
    rAlarm_PT601_ROC                   : REAL := 2.5;   (* [bar/s] *)
    rAlarm_PT601_DB                    : REAL := 0.02;  (* [bar] *)
    rAlarm_PT601_Prev                  : REAL;

    rAlarm_PT701_HH                    : REAL := 0.160; (* [bar] Hypersonic Unstart Static Pressure Surge *)
    rAlarm_PT701_H                     : REAL := 0.085; (* [bar] Cabin Flow Separation Warning *)
    rAlarm_PT701_L                     : REAL := 0.003; (* [bar] *)
    rAlarm_PT701_LL                    : REAL := 0.0005;(* [bar] *)
    rAlarm_PT701_ROC                   : REAL := 0.65;  (* [bar/s] Fast Unstart Gradient *)
    rAlarm_PT701_DB                    : REAL := 0.005; (* [bar] *)
    rAlarm_PT701_Prev                  : REAL;

    rAlarm_AIT801_HH                   : REAL := 26.5;  (* [deg] Shock Wave Detached from Diamond Wedge *)
    rAlarm_AIT801_H                    : REAL := 24.0;  (* [deg] Mach Number Deceleration Warning *)
    rAlarm_AIT801_L                    : REAL := 17.5;  (* [deg] Low Oblique Shock Angle *)
    rAlarm_AIT801_LL                   : REAL := 15.5;  (* [deg] Near-Mach-Wave Limit *)
    rAlarm_AIT801_ROC                  : REAL := 9.0;   (* [deg/s] Schlieren Angle Instability *)
    rAlarm_AIT801_DB                   : REAL := 0.3;   (* [deg] *)
    rAlarm_AIT801_Prev                 : REAL;

    (* Active Alarm Condition Bit Latches *)
    bAlarm_PT101_Trip                  : BOOL := FALSE;
    bAlarm_TT201_Trip                  : BOOL := FALSE;
    bAlarm_PT301_Trip                  : BOOL := FALSE;
    bAlarm_TT401_Trip                  : BOOL := FALSE;
    bAlarm_FT501_Trip                  : BOOL := FALSE;
    bAlarm_PT601_Trip                  : BOOL := FALSE;
    bAlarm_PT701_Trip                  : BOOL := FALSE;
    bAlarm_AIT801_Trip                 : BOOL := FALSE;

    (* Loop Counter Index Variables *)
    iIdx                               : INT;
    jIdx                               : INT;
    kIdx                               : INT;
    mIdx                               : INT;
    rDt_sec                            : REAL;
    rTempCalc                          : REAL;
    rDiffAB                            : REAL;
    rDiffBC                            : REAL;
    rDiffCA                            : REAL;
    rSumCost                           : REAL;
END_VAR
""")

    # -------------------------------------------------------------------------
    # 5. BODY: PHASE 1 - 2oo3 TMR SENSOR VOTING
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  EXECUTION CYCLE ENTRY: REAL-TIME TIMESTEP CALCULATION & INITIALIZATION
====================================================================================================
*)
rDt_sec := TIME_TO_REAL(tCycleTime) / 1000.0;
IF (rDt_sec <= 0.00001) THEN
    rDt_sec := 0.0005; (* Default 500 us task cycle fallback *)
END_IF;

(*
====================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY ANALYSIS
  Standardized P&ID Transmitters with 0.8 bar (Stagnation) and 0.02 bar (Cabin Static) Tolerances.
  Degradation Sequence: 2oo3 Normal -> 1oo2 Bumpless -> 1oo1 Degraded Advisory -> 0oo3 SIL Fail-Safe
====================================================================================================
*)

(* --- CHANNEL 1: PEBBLE BED TOP DOME PRESSURE (PT-101) [Threshold: 1.20 bar, Timer: 100 ms] --- *)
rDiffAB := ABS(PT_PEBBLE_BED_TOP_101A - PT_PEBBLE_BED_TOP_101B);
rDiffBC := ABS(PT_PEBBLE_BED_TOP_101B - PT_PEBBLE_BED_TOP_101C);
rDiffCA := ABS(PT_PEBBLE_BED_TOP_101C - PT_PEBBLE_BED_TOP_101A);

IF (rDiffAB > 1.20) THEN rTimer_PT101_AB := rTimer_PT101_AB + rDt_sec; ELSE rTimer_PT101_AB := 0.0; END_IF;
IF (rDiffBC > 1.20) THEN rTimer_PT101_BC := rTimer_PT101_BC + rDt_sec; ELSE rTimer_PT101_BC := 0.0; END_IF;
IF (rDiffCA > 1.20) THEN rTimer_PT101_CA := rTimer_PT101_CA + rDt_sec; ELSE rTimer_PT101_CA := 0.0; END_IF;

bFault_PT101A := (rTimer_PT101_AB > 0.100) AND (rTimer_PT101_CA > 0.100);
bFault_PT101B := (rTimer_PT101_AB > 0.100) AND (rTimer_PT101_BC > 0.100);
bFault_PT101C := (rTimer_PT101_BC > 0.100) AND (rTimer_PT101_CA > 0.100);

IF (NOT bFault_PT101A AND NOT bFault_PT101B AND NOT bFault_PT101C) THEN
    (* 2oo3 Normal Median Voting *)
    IF ((PT_PEBBLE_BED_TOP_101A >= PT_PEBBLE_BED_TOP_101B AND PT_PEBBLE_BED_TOP_101A <= PT_PEBBLE_BED_TOP_101C) OR
        (PT_PEBBLE_BED_TOP_101A <= PT_PEBBLE_BED_TOP_101B AND PT_PEBBLE_BED_TOP_101A >= PT_PEBBLE_BED_TOP_101C)) THEN
        rVoted_PT101 := PT_PEBBLE_BED_TOP_101A;
    ELSIF ((PT_PEBBLE_BED_TOP_101B >= PT_PEBBLE_BED_TOP_101A AND PT_PEBBLE_BED_TOP_101B <= PT_PEBBLE_BED_TOP_101C) OR
           (PT_PEBBLE_BED_TOP_101B <= PT_PEBBLE_BED_TOP_101A AND PT_PEBBLE_BED_TOP_101B >= PT_PEBBLE_BED_TOP_101C)) THEN
        rVoted_PT101 := PT_PEBBLE_BED_TOP_101B;
    ELSE
        rVoted_PT101 := PT_PEBBLE_BED_TOP_101C;
    END_IF;
    bDegraded_PT101 := FALSE;
    bTrip_PT101 := FALSE;
ELSIF (bFault_PT101A AND NOT bFault_PT101B AND NOT bFault_PT101C) THEN
    rVoted_PT101 := 0.5 * (PT_PEBBLE_BED_TOP_101B + PT_PEBBLE_BED_TOP_101C);
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSIF (NOT bFault_PT101A AND bFault_PT101B AND NOT bFault_PT101C) THEN
    rVoted_PT101 := 0.5 * (PT_PEBBLE_BED_TOP_101A + PT_PEBBLE_BED_TOP_101C);
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSIF (NOT bFault_PT101A AND NOT bFault_PT101B AND bFault_PT101C) THEN
    rVoted_PT101 := 0.5 * (PT_PEBBLE_BED_TOP_101A + PT_PEBBLE_BED_TOP_101B);
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSIF (NOT bFault_PT101A AND bFault_PT101B AND bFault_PT101C) THEN
    rVoted_PT101 := PT_PEBBLE_BED_TOP_101A;
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSIF (bFault_PT101A AND NOT bFault_PT101B AND bFault_PT101C) THEN
    rVoted_PT101 := PT_PEBBLE_BED_TOP_101B;
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSIF (bFault_PT101A AND bFault_PT101B AND NOT bFault_PT101C) THEN
    rVoted_PT101 := PT_PEBBLE_BED_TOP_101C;
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := FALSE;
ELSE
    rVoted_PT101 := 0.0;
    bDegraded_PT101 := TRUE;
    bTrip_PT101 := TRUE; (* Complete 0oo3 Failure *)
END_IF;

(* --- CHANNEL 2: PEBBLE BED CORE TEMPERATURE (TT-201) [Threshold: 20.0 K, Timer: 250 ms] --- *)
rDiffAB := ABS(TT_PEBBLE_BED_CORE_201A - TT_PEBBLE_BED_CORE_201B);
rDiffBC := ABS(TT_PEBBLE_BED_CORE_201B - TT_PEBBLE_BED_CORE_201C);
rDiffCA := ABS(TT_PEBBLE_BED_CORE_201C - TT_PEBBLE_BED_CORE_201A);

IF (rDiffAB > 20.0) THEN rTimer_TT201_AB := rTimer_TT201_AB + rDt_sec; ELSE rTimer_TT201_AB := 0.0; END_IF;
IF (rDiffBC > 20.0) THEN rTimer_TT201_BC := rTimer_TT201_BC + rDt_sec; ELSE rTimer_TT201_BC := 0.0; END_IF;
IF (rDiffCA > 20.0) THEN rTimer_TT201_CA := rTimer_TT201_CA + rDt_sec; ELSE rTimer_TT201_CA := 0.0; END_IF;

bFault_TT201A := (rTimer_TT201_AB > 0.250) AND (rTimer_TT201_CA > 0.250);
bFault_TT201B := (rTimer_TT201_AB > 0.250) AND (rTimer_TT201_BC > 0.250);
bFault_TT201C := (rTimer_TT201_BC > 0.250) AND (rTimer_TT201_CA > 0.250);

IF (NOT bFault_TT201A AND NOT bFault_TT201B AND NOT bFault_TT201C) THEN
    IF ((TT_PEBBLE_BED_CORE_201A >= TT_PEBBLE_BED_CORE_201B AND TT_PEBBLE_BED_CORE_201A <= TT_PEBBLE_BED_CORE_201C) OR
        (TT_PEBBLE_BED_CORE_201A <= TT_PEBBLE_BED_CORE_201B AND TT_PEBBLE_BED_CORE_201A >= TT_PEBBLE_BED_CORE_201C)) THEN
        rVoted_TT201 := TT_PEBBLE_BED_CORE_201A;
    ELSIF ((TT_PEBBLE_BED_CORE_201B >= TT_PEBBLE_BED_CORE_201A AND TT_PEBBLE_BED_CORE_201B <= TT_PEBBLE_BED_CORE_201C) OR
           (TT_PEBBLE_BED_CORE_201B <= TT_PEBBLE_BED_CORE_201A AND TT_PEBBLE_BED_CORE_201B >= TT_PEBBLE_BED_CORE_201C)) THEN
        rVoted_TT201 := TT_PEBBLE_BED_CORE_201B;
    ELSE
        rVoted_TT201 := TT_PEBBLE_BED_CORE_201C;
    END_IF;
    bDegraded_TT201 := FALSE;
    bTrip_TT201 := FALSE;
ELSIF (bFault_TT201A AND NOT bFault_TT201B AND NOT bFault_TT201C) THEN
    rVoted_TT201 := 0.5 * (TT_PEBBLE_BED_CORE_201B + TT_PEBBLE_BED_CORE_201C);
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSIF (NOT bFault_TT201A AND bFault_TT201B AND NOT bFault_TT201C) THEN
    rVoted_TT201 := 0.5 * (TT_PEBBLE_BED_CORE_201A + TT_PEBBLE_BED_CORE_201C);
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSIF (NOT bFault_TT201A AND NOT bFault_TT201B AND bFault_TT201C) THEN
    rVoted_TT201 := 0.5 * (TT_PEBBLE_BED_CORE_201A + TT_PEBBLE_BED_CORE_201B);
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSIF (NOT bFault_TT201A AND bFault_TT201B AND bFault_TT201C) THEN
    rVoted_TT201 := TT_PEBBLE_BED_CORE_201A;
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSIF (bFault_TT201A AND NOT bFault_TT201B AND bFault_TT201C) THEN
    rVoted_TT201 := TT_PEBBLE_BED_CORE_201B;
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSIF (bFault_TT201A AND bFault_TT201B AND NOT bFault_TT201C) THEN
    rVoted_TT201 := TT_PEBBLE_BED_CORE_201C;
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := FALSE;
ELSE
    rVoted_TT201 := 300.0;
    bDegraded_TT201 := TRUE;
    bTrip_TT201 := TRUE;
END_IF;

(* --- CHANNEL 3: NOZZLE STAGNATION TOTAL PRESSURE (PT-301) [Threshold: 0.80 bar, Timer: 50 ms] --- *)
rDiffAB := ABS(PT_NOZZLE_STAGNATION_301A - PT_NOZZLE_STAGNATION_301B);
rDiffBC := ABS(PT_NOZZLE_STAGNATION_301B - PT_NOZZLE_STAGNATION_301C);
rDiffCA := ABS(PT_NOZZLE_STAGNATION_301C - PT_NOZZLE_STAGNATION_301A);

IF (rDiffAB > 0.80) THEN rTimer_PT301_AB := rTimer_PT301_AB + rDt_sec; ELSE rTimer_PT301_AB := 0.0; END_IF;
IF (rDiffBC > 0.80) THEN rTimer_PT301_BC := rTimer_PT301_BC + rDt_sec; ELSE rTimer_PT301_BC := 0.0; END_IF;
IF (rDiffCA > 0.80) THEN rTimer_PT301_CA := rTimer_PT301_CA + rDt_sec; ELSE rTimer_PT301_CA := 0.0; END_IF;

bFault_PT301A := (rTimer_PT301_AB > 0.050) AND (rTimer_PT301_CA > 0.050);
bFault_PT301B := (rTimer_PT301_AB > 0.050) AND (rTimer_PT301_BC > 0.050);
bFault_PT301C := (rTimer_PT301_BC > 0.050) AND (rTimer_PT301_CA > 0.050);

IF (NOT bFault_PT301A AND NOT bFault_PT301B AND NOT bFault_PT301C) THEN
    IF ((PT_NOZZLE_STAGNATION_301A >= PT_NOZZLE_STAGNATION_301B AND PT_NOZZLE_STAGNATION_301A <= PT_NOZZLE_STAGNATION_301C) OR
        (PT_NOZZLE_STAGNATION_301A <= PT_NOZZLE_STAGNATION_301B AND PT_NOZZLE_STAGNATION_301A >= PT_NOZZLE_STAGNATION_301C)) THEN
        rVoted_PT301 := PT_NOZZLE_STAGNATION_301A;
    ELSIF ((PT_NOZZLE_STAGNATION_301B >= PT_NOZZLE_STAGNATION_301A AND PT_NOZZLE_STAGNATION_301B <= PT_NOZZLE_STAGNATION_301C) OR
           (PT_NOZZLE_STAGNATION_301B <= PT_NOZZLE_STAGNATION_301A AND PT_NOZZLE_STAGNATION_301B >= PT_NOZZLE_STAGNATION_301C)) THEN
        rVoted_PT301 := PT_NOZZLE_STAGNATION_301B;
    ELSE
        rVoted_PT301 := PT_NOZZLE_STAGNATION_301C;
    END_IF;
    bDegraded_PT301 := FALSE;
    bTrip_PT301 := FALSE;
ELSIF (bFault_PT301A AND NOT bFault_PT301B AND NOT bFault_PT301C) THEN
    rVoted_PT301 := 0.5 * (PT_NOZZLE_STAGNATION_301B + PT_NOZZLE_STAGNATION_301C);
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSIF (NOT bFault_PT301A AND bFault_PT301B AND NOT bFault_PT301C) THEN
    rVoted_PT301 := 0.5 * (PT_NOZZLE_STAGNATION_301A + PT_NOZZLE_STAGNATION_301C);
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSIF (NOT bFault_PT301A AND NOT bFault_PT301B AND bFault_PT301C) THEN
    rVoted_PT301 := 0.5 * (PT_NOZZLE_STAGNATION_301A + PT_NOZZLE_STAGNATION_301B);
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSIF (NOT bFault_PT301A AND bFault_PT301B AND bFault_PT301C) THEN
    rVoted_PT301 := PT_NOZZLE_STAGNATION_301A;
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSIF (bFault_PT301A AND NOT bFault_PT301B AND bFault_PT301C) THEN
    rVoted_PT301 := PT_NOZZLE_STAGNATION_301B;
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSIF (bFault_PT301A AND bFault_PT301B AND NOT bFault_PT301C) THEN
    rVoted_PT301 := PT_NOZZLE_STAGNATION_301C;
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := FALSE;
ELSE
    rVoted_PT301 := 0.0;
    bDegraded_PT301 := TRUE;
    bTrip_PT301 := TRUE;
END_IF;

(* --- CHANNEL 4: NOZZLE THROAT INNER WALL TEMPERATURE (TT-401) [Threshold: 15.0 K, Timer: 100 ms] --- *)
rDiffAB := ABS(TT_NOZZLE_THROAT_WALL_401A - TT_NOZZLE_THROAT_WALL_401B);
rDiffBC := ABS(TT_NOZZLE_THROAT_WALL_401B - TT_NOZZLE_THROAT_WALL_401C);
rDiffCA := ABS(TT_NOZZLE_THROAT_WALL_401C - TT_NOZZLE_THROAT_WALL_401A);

IF (rDiffAB > 15.0) THEN rTimer_TT401_AB := rTimer_TT401_AB + rDt_sec; ELSE rTimer_TT401_AB := 0.0; END_IF;
IF (rDiffBC > 15.0) THEN rTimer_TT401_BC := rTimer_TT401_BC + rDt_sec; ELSE rTimer_TT401_BC := 0.0; END_IF;
IF (rDiffCA > 15.0) THEN rTimer_TT401_CA := rTimer_TT401_CA + rDt_sec; ELSE rTimer_TT401_CA := 0.0; END_IF;

bFault_TT401A := (rTimer_TT401_AB > 0.100) AND (rTimer_TT401_CA > 0.100);
bFault_TT401B := (rTimer_TT401_AB > 0.100) AND (rTimer_TT401_BC > 0.100);
bFault_TT401C := (rTimer_TT401_BC > 0.100) AND (rTimer_TT401_CA > 0.100);

IF (NOT bFault_TT401A AND NOT bFault_TT401B AND NOT bFault_TT401C) THEN
    IF ((TT_NOZZLE_THROAT_WALL_401A >= TT_NOZZLE_THROAT_WALL_401B AND TT_NOZZLE_THROAT_WALL_401A <= TT_NOZZLE_THROAT_WALL_401C) OR
        (TT_NOZZLE_THROAT_WALL_401A <= TT_NOZZLE_THROAT_WALL_401B AND TT_NOZZLE_THROAT_WALL_401A >= TT_NOZZLE_THROAT_WALL_401C)) THEN
        rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401A;
    ELSIF ((TT_NOZZLE_THROAT_WALL_401B >= TT_NOZZLE_THROAT_WALL_401A AND TT_NOZZLE_THROAT_WALL_401B <= TT_NOZZLE_THROAT_WALL_401C) OR
           (TT_NOZZLE_THROAT_WALL_401B <= TT_NOZZLE_THROAT_WALL_401A AND TT_NOZZLE_THROAT_WALL_401B >= TT_NOZZLE_THROAT_WALL_401C)) THEN
        rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401B;
    ELSE
        rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401C;
    END_IF;
    bDegraded_TT401 := FALSE;
    bTrip_TT401 := FALSE;
ELSIF (bFault_TT401A AND NOT bFault_TT401B AND NOT bFault_TT401C) THEN
    rVoted_TT401 := 0.5 * (TT_NOZZLE_THROAT_WALL_401B + TT_NOZZLE_THROAT_WALL_401C);
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSIF (NOT bFault_TT401A AND bFault_TT401B AND NOT bFault_TT401C) THEN
    rVoted_TT401 := 0.5 * (TT_NOZZLE_THROAT_WALL_401A + TT_NOZZLE_THROAT_WALL_401C);
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSIF (NOT bFault_TT401A AND NOT bFault_TT401B AND bFault_TT401C) THEN
    rVoted_TT401 := 0.5 * (TT_NOZZLE_THROAT_WALL_401A + TT_NOZZLE_THROAT_WALL_401B);
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSIF (NOT bFault_TT401A AND bFault_TT401B AND bFault_TT401C) THEN
    rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401A;
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSIF (bFault_TT401A AND NOT bFault_TT401B AND bFault_TT401C) THEN
    rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401B;
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSIF (bFault_TT401A AND bFault_TT401B AND NOT bFault_TT401C) THEN
    rVoted_TT401 := TT_NOZZLE_THROAT_WALL_401C;
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := FALSE;
ELSE
    rVoted_TT401 := 293.15;
    bDegraded_TT401 := TRUE;
    bTrip_TT401 := TRUE;
END_IF;

(* --- CHANNEL 5: CRYO LN2 COOLANT MASS FLOW (FT-501) [Threshold: 0.60 kg/s, Timer: 80 ms] --- *)
rDiffAB := ABS(FT_LN2_COOLANT_501A - FT_LN2_COOLANT_501B);
rDiffBC := ABS(FT_LN2_COOLANT_501B - FT_LN2_COOLANT_501C);
rDiffCA := ABS(FT_LN2_COOLANT_501C - FT_LN2_COOLANT_501A);

IF (rDiffAB > 0.60) THEN rTimer_FT501_AB := rTimer_FT501_AB + rDt_sec; ELSE rTimer_FT501_AB := 0.0; END_IF;
IF (rDiffBC > 0.60) THEN rTimer_FT501_BC := rTimer_FT501_BC + rDt_sec; ELSE rTimer_FT501_BC := 0.0; END_IF;
IF (rDiffCA > 0.60) THEN rTimer_FT501_CA := rTimer_FT501_CA + rDt_sec; ELSE rTimer_FT501_CA := 0.0; END_IF;

bFault_FT501A := (rTimer_FT501_AB > 0.080) AND (rTimer_FT501_CA > 0.080);
bFault_FT501B := (rTimer_FT501_AB > 0.080) AND (rTimer_FT501_BC > 0.080);
bFault_FT501C := (rTimer_FT501_BC > 0.080) AND (rTimer_FT501_CA > 0.080);

IF (NOT bFault_FT501A AND NOT bFault_FT501B AND NOT bFault_FT501C) THEN
    IF ((FT_LN2_COOLANT_501A >= FT_LN2_COOLANT_501B AND FT_LN2_COOLANT_501A <= FT_LN2_COOLANT_501C) OR
        (FT_LN2_COOLANT_501A <= FT_LN2_COOLANT_501B AND FT_LN2_COOLANT_501A >= FT_LN2_COOLANT_501C)) THEN
        rVoted_FT501 := FT_LN2_COOLANT_501A;
    ELSIF ((FT_LN2_COOLANT_501B >= FT_LN2_COOLANT_501A AND FT_LN2_COOLANT_501B <= FT_LN2_COOLANT_501C) OR
           (FT_LN2_COOLANT_501B <= FT_LN2_COOLANT_501A AND FT_LN2_COOLANT_501B >= FT_LN2_COOLANT_501C)) THEN
        rVoted_FT501 := FT_LN2_COOLANT_501B;
    ELSE
        rVoted_FT501 := FT_LN2_COOLANT_501C;
    END_IF;
    bDegraded_FT501 := FALSE;
    bTrip_FT501 := FALSE;
ELSIF (bFault_FT501A AND NOT bFault_FT501B AND NOT bFault_FT501C) THEN
    rVoted_FT501 := 0.5 * (FT_LN2_COOLANT_501B + FT_LN2_COOLANT_501C);
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSIF (NOT bFault_FT501A AND bFault_FT501B AND NOT bFault_FT501C) THEN
    rVoted_FT501 := 0.5 * (FT_LN2_COOLANT_501A + FT_LN2_COOLANT_501C);
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSIF (NOT bFault_FT501A AND NOT bFault_FT501B AND bFault_FT501C) THEN
    rVoted_FT501 := 0.5 * (FT_LN2_COOLANT_501A + FT_LN2_COOLANT_501B);
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSIF (NOT bFault_FT501A AND bFault_FT501B AND bFault_FT501C) THEN
    rVoted_FT501 := FT_LN2_COOLANT_501A;
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSIF (bFault_FT501A AND NOT bFault_FT501B AND bFault_FT501C) THEN
    rVoted_FT501 := FT_LN2_COOLANT_501B;
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSIF (bFault_FT501A AND bFault_FT501B AND NOT bFault_FT501C) THEN
    rVoted_FT501 := FT_LN2_COOLANT_501C;
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := FALSE;
ELSE
    rVoted_FT501 := 0.0;
    bDegraded_FT501 := TRUE;
    bTrip_FT501 := TRUE;
END_IF;

(* --- CHANNEL 6: SUPERSONIC DIFFUSER EXIT PRESSURE (PT-601) [Threshold: 0.05 bar, Timer: 50 ms] --- *)
rDiffAB := ABS(PT_DIFFUSER_EXIT_601A - PT_DIFFUSER_EXIT_601B);
rDiffBC := ABS(PT_DIFFUSER_EXIT_601B - PT_DIFFUSER_EXIT_601C);
rDiffCA := ABS(PT_DIFFUSER_EXIT_601C - PT_DIFFUSER_EXIT_601A);

IF (rDiffAB > 0.05) THEN rTimer_PT601_AB := rTimer_PT601_AB + rDt_sec; ELSE rTimer_PT601_AB := 0.0; END_IF;
IF (rDiffBC > 0.05) THEN rTimer_PT601_BC := rTimer_PT601_BC + rDt_sec; ELSE rTimer_PT601_BC := 0.0; END_IF;
IF (rDiffCA > 0.05) THEN rTimer_PT601_CA := rTimer_PT601_CA + rDt_sec; ELSE rTimer_PT601_CA := 0.0; END_IF;

bFault_PT601A := (rTimer_PT601_AB > 0.050) AND (rTimer_PT601_CA > 0.050);
bFault_PT601B := (rTimer_PT601_AB > 0.050) AND (rTimer_PT601_BC > 0.050);
bFault_PT601C := (rTimer_PT601_BC > 0.050) AND (rTimer_PT601_CA > 0.050);

IF (NOT bFault_PT601A AND NOT bFault_PT601B AND NOT bFault_PT601C) THEN
    IF ((PT_DIFFUSER_EXIT_601A >= PT_DIFFUSER_EXIT_601B AND PT_DIFFUSER_EXIT_601A <= PT_DIFFUSER_EXIT_601C) OR
        (PT_DIFFUSER_EXIT_601A <= PT_DIFFUSER_EXIT_601B AND PT_DIFFUSER_EXIT_601A >= PT_DIFFUSER_EXIT_601C)) THEN
        rVoted_PT601 := PT_DIFFUSER_EXIT_601A;
    ELSIF ((PT_DIFFUSER_EXIT_601B >= PT_DIFFUSER_EXIT_601A AND PT_DIFFUSER_EXIT_601B <= PT_DIFFUSER_EXIT_601C) OR
           (PT_DIFFUSER_EXIT_601B <= PT_DIFFUSER_EXIT_601A AND PT_DIFFUSER_EXIT_601B >= PT_DIFFUSER_EXIT_601C)) THEN
        rVoted_PT601 := PT_DIFFUSER_EXIT_601B;
    ELSE
        rVoted_PT601 := PT_DIFFUSER_EXIT_601C;
    END_IF;
    bDegraded_PT601 := FALSE;
    bTrip_PT601 := FALSE;
ELSIF (bFault_PT601A AND NOT bFault_PT601B AND NOT bFault_PT601C) THEN
    rVoted_PT601 := 0.5 * (PT_DIFFUSER_EXIT_601B + PT_DIFFUSER_EXIT_601C);
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSIF (NOT bFault_PT601A AND bFault_PT601B AND NOT bFault_PT601C) THEN
    rVoted_PT601 := 0.5 * (PT_DIFFUSER_EXIT_601A + PT_DIFFUSER_EXIT_601C);
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSIF (NOT bFault_PT601A AND NOT bFault_PT601B AND bFault_PT601C) THEN
    rVoted_PT601 := 0.5 * (PT_DIFFUSER_EXIT_601A + PT_DIFFUSER_EXIT_601B);
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSIF (NOT bFault_PT601A AND bFault_PT601B AND bFault_PT601C) THEN
    rVoted_PT601 := PT_DIFFUSER_EXIT_601A;
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSIF (bFault_PT601A AND NOT bFault_PT601B AND bFault_PT601C) THEN
    rVoted_PT601 := PT_DIFFUSER_EXIT_601B;
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSIF (bFault_PT601A AND bFault_PT601B AND NOT bFault_PT601C) THEN
    rVoted_PT601 := PT_DIFFUSER_EXIT_601C;
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := FALSE;
ELSE
    rVoted_PT601 := 1.0;
    bDegraded_PT601 := TRUE;
    bTrip_PT601 := TRUE;
END_IF;

(* --- CHANNEL 7: TEST CABIN SUPERSONIC STATIC WALL PRESSURE (PT-701) [Threshold: 0.02 bar, Timer: 20 ms] --- *)
rDiffAB := ABS(PT_TEST_CABIN_STATIC_701A - PT_TEST_CABIN_STATIC_701B);
rDiffBC := ABS(PT_TEST_CABIN_STATIC_701B - PT_TEST_CABIN_STATIC_701C);
rDiffCA := ABS(PT_TEST_CABIN_STATIC_701C - PT_TEST_CABIN_STATIC_701A);

IF (rDiffAB > 0.02) THEN rTimer_PT701_AB := rTimer_PT701_AB + rDt_sec; ELSE rTimer_PT701_AB := 0.0; END_IF;
IF (rDiffBC > 0.02) THEN rTimer_PT701_BC := rTimer_PT701_BC + rDt_sec; ELSE rTimer_PT701_BC := 0.0; END_IF;
IF (rDiffCA > 0.02) THEN rTimer_PT701_CA := rTimer_PT701_CA + rDt_sec; ELSE rTimer_PT701_CA := 0.0; END_IF;

bFault_PT701A := (rTimer_PT701_AB > 0.020) AND (rTimer_PT701_CA > 0.020);
bFault_PT701B := (rTimer_PT701_AB > 0.020) AND (rTimer_PT701_BC > 0.020);
bFault_PT701C := (rTimer_PT701_BC > 0.020) AND (rTimer_PT701_CA > 0.020);

IF (NOT bFault_PT701A AND NOT bFault_PT701B AND NOT bFault_PT701C) THEN
    IF ((PT_TEST_CABIN_STATIC_701A >= PT_TEST_CABIN_STATIC_701B AND PT_TEST_CABIN_STATIC_701A <= PT_TEST_CABIN_STATIC_701C) OR
        (PT_TEST_CABIN_STATIC_701A <= PT_TEST_CABIN_STATIC_701B AND PT_TEST_CABIN_STATIC_701A >= PT_TEST_CABIN_STATIC_701C)) THEN
        rVoted_PT701 := PT_TEST_CABIN_STATIC_701A;
    ELSIF ((PT_TEST_CABIN_STATIC_701B >= PT_TEST_CABIN_STATIC_701A AND PT_TEST_CABIN_STATIC_701B <= PT_TEST_CABIN_STATIC_701C) OR
           (PT_TEST_CABIN_STATIC_701B <= PT_TEST_CABIN_STATIC_701A AND PT_TEST_CABIN_STATIC_701B >= PT_TEST_CABIN_STATIC_701C)) THEN
        rVoted_PT701 := PT_TEST_CABIN_STATIC_701B;
    ELSE
        rVoted_PT701 := PT_TEST_CABIN_STATIC_701C;
    END_IF;
    bDegraded_PT701 := FALSE;
    bTrip_PT701 := FALSE;
ELSIF (bFault_PT701A AND NOT bFault_PT701B AND NOT bFault_PT701C) THEN
    rVoted_PT701 := 0.5 * (PT_TEST_CABIN_STATIC_701B + PT_TEST_CABIN_STATIC_701C);
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSIF (NOT bFault_PT701A AND bFault_PT701B AND NOT bFault_PT701C) THEN
    rVoted_PT701 := 0.5 * (PT_TEST_CABIN_STATIC_701A + PT_TEST_CABIN_STATIC_701C);
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSIF (NOT bFault_PT701A AND NOT bFault_PT701B AND bFault_PT701C) THEN
    rVoted_PT701 := 0.5 * (PT_TEST_CABIN_STATIC_701A + PT_TEST_CABIN_STATIC_701B);
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSIF (NOT bFault_PT701A AND bFault_PT701B AND bFault_PT701C) THEN
    rVoted_PT701 := PT_TEST_CABIN_STATIC_701A;
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSIF (bFault_PT701A AND NOT bFault_PT701B AND bFault_PT701C) THEN
    rVoted_PT701 := PT_TEST_CABIN_STATIC_701B;
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSIF (bFault_PT701A AND bFault_PT701B AND NOT bFault_PT701C) THEN
    rVoted_PT701 := PT_TEST_CABIN_STATIC_701C;
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := FALSE;
ELSE
    rVoted_PT701 := 0.05;
    bDegraded_PT701 := TRUE;
    bTrip_PT701 := TRUE;
END_IF;

(* --- CHANNEL 8: SCHLIEREN OBLIQUE SHOCK ANGLE (AIT-801) [Threshold: 0.35 deg, Timer: 40 ms] --- *)
rDiffAB := ABS(AIT_SCHLIEREN_SHOCK_ANGLE_801A - AIT_SCHLIEREN_SHOCK_ANGLE_801B);
rDiffBC := ABS(AIT_SCHLIEREN_SHOCK_ANGLE_801B - AIT_SCHLIEREN_SHOCK_ANGLE_801C);
rDiffCA := ABS(AIT_SCHLIEREN_SHOCK_ANGLE_801C - AIT_SCHLIEREN_SHOCK_ANGLE_801A);

IF (rDiffAB > 0.35) THEN rTimer_AIT801_AB := rTimer_AIT801_AB + rDt_sec; ELSE rTimer_AIT801_AB := 0.0; END_IF;
IF (rDiffBC > 0.35) THEN rTimer_AIT801_BC := rTimer_AIT801_BC + rDt_sec; ELSE rTimer_AIT801_BC := 0.0; END_IF;
IF (rDiffCA > 0.35) THEN rTimer_AIT801_CA := rTimer_AIT801_CA + rDt_sec; ELSE rTimer_AIT801_CA := 0.0; END_IF;

bFault_AIT801A := (rTimer_AIT801_AB > 0.040) AND (rTimer_AIT801_CA > 0.040);
bFault_AIT801B := (rTimer_AIT801_AB > 0.040) AND (rTimer_AIT801_BC > 0.040);
bFault_AIT801C := (rTimer_AIT801_BC > 0.040) AND (rTimer_AIT801_CA > 0.040);

IF (NOT bFault_AIT801A AND NOT bFault_AIT801B AND NOT bFault_AIT801C) THEN
    IF ((AIT_SCHLIEREN_SHOCK_ANGLE_801A >= AIT_SCHLIEREN_SHOCK_ANGLE_801B AND AIT_SCHLIEREN_SHOCK_ANGLE_801A <= AIT_SCHLIEREN_SHOCK_ANGLE_801C) OR
        (AIT_SCHLIEREN_SHOCK_ANGLE_801A <= AIT_SCHLIEREN_SHOCK_ANGLE_801B AND AIT_SCHLIEREN_SHOCK_ANGLE_801A >= AIT_SCHLIEREN_SHOCK_ANGLE_801C)) THEN
        rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801A;
    ELSIF ((AIT_SCHLIEREN_SHOCK_ANGLE_801B >= AIT_SCHLIEREN_SHOCK_ANGLE_801A AND AIT_SCHLIEREN_SHOCK_ANGLE_801B <= AIT_SCHLIEREN_SHOCK_ANGLE_801C) OR
           (AIT_SCHLIEREN_SHOCK_ANGLE_801B <= AIT_SCHLIEREN_SHOCK_ANGLE_801A AND AIT_SCHLIEREN_SHOCK_ANGLE_801B >= AIT_SCHLIEREN_SHOCK_ANGLE_801C)) THEN
        rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801B;
    ELSE
        rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801C;
    END_IF;
    bDegraded_AIT801 := FALSE;
    bTrip_AIT801 := FALSE;
ELSIF (bFault_AIT801A AND NOT bFault_AIT801B AND NOT bFault_AIT801C) THEN
    rVoted_AIT801 := 0.5 * (AIT_SCHLIEREN_SHOCK_ANGLE_801B + AIT_SCHLIEREN_SHOCK_ANGLE_801C);
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSIF (NOT bFault_AIT801A AND bFault_AIT801B AND NOT bFault_AIT801C) THEN
    rVoted_AIT801 := 0.5 * (AIT_SCHLIEREN_SHOCK_ANGLE_801A + AIT_SCHLIEREN_SHOCK_ANGLE_801C);
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSIF (NOT bFault_AIT801A AND NOT bFault_AIT801B AND bFault_AIT801C) THEN
    rVoted_AIT801 := 0.5 * (AIT_SCHLIEREN_SHOCK_ANGLE_801A + AIT_SCHLIEREN_SHOCK_ANGLE_801B);
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSIF (NOT bFault_AIT801A AND bFault_AIT801B AND bFault_AIT801C) THEN
    rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801A;
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSIF (bFault_AIT801A AND NOT bFault_AIT801B AND bFault_AIT801C) THEN
    rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801B;
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSIF (bFault_AIT801A AND bFault_AIT801B AND NOT bFault_AIT801C) THEN
    rVoted_AIT801 := AIT_SCHLIEREN_SHOCK_ANGLE_801C;
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := FALSE;
ELSE
    rVoted_AIT801 := 20.0;
    bDegraded_AIT801 := TRUE;
    bTrip_AIT801 := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 6. BODY: PHASE 2 - HIGH-ENTHALPY THERMODYNAMICS & GAS DYNAMICS OBSERVER
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 2: REAL-GAS HIGH-ENTHALPY THERMODYNAMICS & GAS DYNAMICS OBSERVER ENGINE
  - Real-gas equilibrium gamma(T) and Cp(T) polynomial approximations (vibrational excitation).
  - Sutherland equation for dynamic viscosity mu(T).
  - Isentropic and critical choking throat flow equations.
  - Multi-node Schumann regenerative pebble bed heat transfer finite difference model.
  - Bartz empirical convective throat heat flux observer (18 MW/m^2 peak).
  - Optical Schlieren diamond wedge theta-beta-Mach iterative shockwave observer.
  - Supersonic diffuser shock detachment and fast-unstart gradient detection.
====================================================================================================
*)

(* --- 1. Real-Gas Temperature-Dependent Specific Heat Cp(T) and Gamma(T) --- *)
(* Stagnation Temperature T_0 calculation from core storage *)
rTempCalc := rVoted_TT201;
IF (rTempCalc < 300.0) THEN
    rTempCalc := 300.0;
ELSIF (rTempCalc > 2500.0) THEN
    rTempCalc := 2500.0;
END_IF;

(* Empirical 4th-order polynomial for High-Enthalpy Dry Air Cp(T) [J/(kg*K)] *)
rAirCp_SpecHeat := 1005.0 + 0.0514 * (rTempCalc - 300.0) + 0.000185 * (rTempCalc - 300.0) * (rTempCalc - 300.0)
                   - 6.2e-8 * (rTempCalc - 300.0) * (rTempCalc - 300.0) * (rTempCalc - 300.0);
IF (rAirCp_SpecHeat < 1005.0) THEN
    rAirCp_SpecHeat := 1005.0;
END_IF;

(* Real Ratio of Specific Heats gamma(T) = Cp / (Cp - R) *)
rAirGamma_Ratio := rAirCp_SpecHeat / (rAirCp_SpecHeat - rAirGasConstant_R);
IF (rAirGamma_Ratio > 1.401) THEN
    rAirGamma_Ratio := 1.400;
ELSIF (rAirGamma_Ratio < 1.280) THEN
    rAirGamma_Ratio := 1.280; (* High temperature vibrational relaxation limit *)
END_IF;

(* --- 2. Dynamic Viscosity via Sutherland's Law [Pa*s] --- *)
(* mu = mu_ref * (T / T_ref)^1.5 * (T_ref + S) / (T + S) with S = 110.4 K, T_ref = 273.15 K, mu_ref = 1.716e-5 Pa*s *)
rAirDynamicViscosity_mu := 0.00001716 * EXPT((rTempCalc / 273.15), 1.5) * ((273.15 + 110.4) / (rTempCalc + 110.4));

(* --- 3. Critical Sonic Choking Conditions at Nozzle Throat --- *)
(* P* = P_0 * (1 + (gamma-1)/2)^(-gamma/(gamma-1)) *)
rAirCriticalPressure_Pstar := rVoted_PT301 * EXPT(1.0 + 0.5 * (rAirGamma_Ratio - 1.0), (-rAirGamma_Ratio / (rAirGamma_Ratio - 1.0)));

(* T* = T_0 / (1 + (gamma-1)/2) *)
rAirSonicSpeed_Throat := SQRT(rAirGamma_Ratio * rAirGasConstant_R * (rTempCalc / (1.0 + 0.5 * (rAirGamma_Ratio - 1.0))));

(* Critical density rho* = P* / (R * T_star) [kg/m^3] (Note: P* converted from bar to Pa: 1 bar = 1e5 Pa) *)
rAirCriticalDensity_rhostar := (rAirCriticalPressure_Pstar * 100000.0) / (rAirGasConstant_R * (rTempCalc / (1.0 + 0.5 * (rAirGamma_Ratio - 1.0))));

(* Choked Mass Flow Rate m_dot = rho* * A* * a* [kg/s] *)
rAirChokedMassFlow_mdot := rAirCriticalDensity_rhostar * rNozzle_ThroatArea * rAirSonicSpeed_Throat;
rObserved_TotalMassFlow_kgs := rAirChokedMassFlow_mdot;

(* --- 4. 5-Node Axial Schumann Regenerative Ceramic Pebble Bed Heat Transfer Engine --- *)
(* Volumetric Heat Transfer Coefficient hv = 0.255 * (k_gas / dp) * Rep^0.7 * Pr^0.33 * (6*(1-eps)/dp) *)
rPebble_VolumetricHeatTransfer_hv := 1420.0 * EXPT((rAirChokedMassFlow_mdot / 100.0), 0.7);
IF (rPebble_VolumetricHeatTransfer_hv < 250.0) THEN
    rPebble_VolumetricHeatTransfer_hv := 250.0;
END_IF;

(* Axial Convective Energy Balance across Bed Slices *)
(* Node 0 is bottom inlet (air enters cold from storage compressor bottles at 300 K) *)
arrPebble_T_gas[0] := 300.0;
FOR iIdx := 1 TO 4 DO
    (* Gas enthalpy rise: m_dot * Cp * dTg/dz = hv * V_slice * (T_solid - T_gas) *)
    IF (rAirChokedMassFlow_mdot > 0.5) THEN
        arrPebble_T_gas[iIdx] := arrPebble_T_gas[iIdx - 1] +
            ((rPebble_VolumetricHeatTransfer_hv * rPebble_SliceVolume) / (rAirChokedMassFlow_mdot * rAirCp_SpecHeat)) *
            (arrPebble_T_solid[iIdx] - arrPebble_T_gas[iIdx - 1]);
    ELSE
        arrPebble_T_gas[iIdx] := arrPebble_T_solid[iIdx];
    END_IF;

    (* Solid thermal depletion: (1-eps) * rho_s * Cs * V_slice * dTs/dt = -hv * V_slice * (T_solid - T_gas) *)
    IF (iMachineState = 5 OR iMachineState = 6 OR iMachineState = 7) THEN
        arrPebble_T_solid[iIdx] := arrPebble_T_solid[iIdx] -
            (rDt_sec * rPebble_VolumetricHeatTransfer_hv * (arrPebble_T_solid[iIdx] - arrPebble_T_gas[iIdx])) /
            ((1.0 - rPebble_VoidFraction) * rPebble_SolidDensity_rho * rPebble_SolidSpecHeat_Cs);
    END_IF;
END_FOR;

(* Total Remaining Pebble Bed Usable Enthalpy [MJ] *)
rObserved_PebbleBedEnthalpy_MJ := 0.0;
FOR iIdx := 0 TO 4 DO
    rObserved_PebbleBedEnthalpy_MJ := rObserved_PebbleBedEnthalpy_MJ +
        ((1.0 - rPebble_VoidFraction) * rPebble_SolidDensity_rho * rPebble_SolidSpecHeat_Cs * rPebble_SliceVolume *
         (arrPebble_T_solid[iIdx] - 300.0)) / 1000000.0;
END_FOR;

(* --- 5. Bartz Convective Heat Flux Equation at Nozzle Throat (Active Heat Flux 18 MW/m^2) --- *)
(* Adiabatic Recovery Temperature Taw = T_0 * (1 + r*(gamma-1)/2) / (1 + (gamma-1)/2) *)
rNozzle_AdiabaticWallTemp_Taw := rTempCalc * (1.0 + rNozzle_RecoveryFactor_r * 0.5 * (rAirGamma_Ratio - 1.0)) /
                               (1.0 + 0.5 * (rAirGamma_Ratio - 1.0));

(* Characteristic Velocity c* = P_0 * A* / m_dot [m/s] *)
IF (rAirChokedMassFlow_mdot > 0.1) THEN
    rTempCalc := (rVoted_PT301 * 100000.0 * rNozzle_ThroatArea) / rAirChokedMassFlow_mdot;
ELSE
    rTempCalc := 1250.0;
END_IF;

(* Bartz Coefficient h_g [W/(m^2*K)] *)
rNozzle_BartzHeatTransferCoeff_hg := (0.026 / EXPT(rNozzle_ThroatDiameter, 0.2)) *
    (EXPT(rAirDynamicViscosity_mu, 0.2) * rAirCp_SpecHeat / EXPT(0.71, 0.6)) *
    EXPT((rVoted_PT301 * 100000.0 / rTempCalc), 0.8) *
    EXPT((rNozzle_ThroatDiameter / rNozzle_CurvatureRadius), 0.1);

(* Total Throat Aerodynamic Heat Flux q_w = h_g * (T_aw - T_throat_wall) [W/m^2] *)
rNozzle_CalculatedHeatFlux_qw := rNozzle_BartzHeatTransferCoeff_hg * (rNozzle_AdiabaticWallTemp_Taw - rVoted_TT401);
IF (rNozzle_CalculatedHeatFlux_qw < 0.0) THEN
    rNozzle_CalculatedHeatFlux_qw := 0.0;
END_IF;
rObserved_ThroatHeatFlux_MWm2 := rNozzle_CalculatedHeatFlux_qw / 1000000.0;

(* Copper Throat Structural Yield Margin (%) *)
IF (rNozzle_ThroatCopperYieldTemp > rVoted_TT401) THEN
    rObserved_NozzleWallSafetyMargin := ((rNozzle_ThroatCopperYieldTemp - rVoted_TT401) / rNozzle_ThroatCopperYieldTemp) * 100.0;
ELSE
    rObserved_NozzleWallSafetyMargin := 0.0;
END_IF;

(* --- 6. Real-Time Optical Schlieren Diamond Wedge Aerodynamic Observer --- *)
(* Inverting theta-beta-Mach relation: tan(theta) = 2*cot(beta)*(M^2*sin^2(beta) - 1) / (M^2*(gamma + cos(2*beta)) + 2) *)
rSchlieren_Beta_rad := rVoted_AIT801 * 3.14159265 / 180.0;
rWedge_HalfAngle_Theta_rad := rWedge_HalfAngle_Theta_deg * 3.14159265 / 180.0;

(* Algebraic Inversion for M_infinity from Schlieren Angle beta *)
rTempCalc := SIN(rSchlieren_Beta_rad) * SIN(rSchlieren_Beta_rad) -
             TAN(rWedge_HalfAngle_Theta_rad) * COS(2.0 * rSchlieren_Beta_rad) * (COS(rSchlieren_Beta_rad) / SIN(rSchlieren_Beta_rad)) -
             rAirGamma_Ratio * TAN(rWedge_HalfAngle_Theta_rad) * (COS(rSchlieren_Beta_rad) / SIN(rSchlieren_Beta_rad));

IF (ABS(rTempCalc) > 0.0001) THEN
    rSchlieren_InferredMach := SQRT(ABS(2.0 * (TAN(rWedge_HalfAngle_Theta_rad) * (COS(rSchlieren_Beta_rad) / SIN(rSchlieren_Beta_rad)) + 1.0) / rTempCalc));
ELSE
    rSchlieren_InferredMach := 7.00;
END_IF;

(* Clamp to Realistic Facility Hypersonic Regimes (Mach 5.5 to 8.5) *)
IF (rSchlieren_InferredMach < 5.5) THEN
    rSchlieren_InferredMach := 5.5;
ELSIF (rSchlieren_InferredMach > 8.5) THEN
    rSchlieren_InferredMach := 8.5;
END_IF;
rObserved_MachNumber := rSchlieren_InferredMach;
rObserved_SchlierenShockAngle := rVoted_AIT801;

(* Dynamic Pressure q_inf = 0.5 * gamma * P_cabin * M^2 [kPa] *)
rObserved_DynamicPressure_kPa := 0.5 * rAirGamma_Ratio * (rVoted_PT701 * 100.0) * rObserved_MachNumber * rObserved_MachNumber;

(* Unit Reynolds Number Re/L = (P_cabin / (R * T_inf)) * (M * a_inf) / mu [1/m] *)
IF (rAirDynamicViscosity_mu > 0.000001) THEN
    rObserved_ReynoldsUnit_per_m := ((rVoted_PT701 * 100000.0) / (rAirGasConstant_R * 220.0)) *
                                    (rObserved_MachNumber * SQRT(1.4 * 287.058 * 220.0)) / rAirDynamicViscosity_mu;
ELSE
    rObserved_ReynoldsUnit_per_m := 1.5e7;
END_IF;

(* --- 7. Supersonic Diffuser Unstart Detachment & Pressure Rate Observer --- *)
rDiffuser_PressureDerivative := (rVoted_PT701 - rDiffuser_PrevCabinPressure) / rDt_sec;
rDiffuser_PrevCabinPressure := rVoted_PT701;

rObserved_DiffuserPressureRatio := 0.0;
IF (rVoted_PT701 > 0.0001) THEN
    rObserved_DiffuserPressureRatio := rVoted_PT601 / rVoted_PT701;
END_IF;

(* FAST-TRIP UNSTART DETECTOR (< 5.0 ms Trigger): Unstart if pressure ratio breaches critical or cabin surges *)
IF ((rObserved_DiffuserPressureRatio > 45.0) OR (rDiffuser_PressureDerivative > 0.85) OR (rVoted_PT701 > rAlarm_PT701_HH)) AND
   (iMachineState = 5 OR iMachineState = 6 OR iMachineState = 7) THEN
    bTunnelUnstart_TripActive := TRUE;
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0001; (* Bit 0: Hypersonic Diffuser Unstart Trip *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # 7. BODY: PHASE 3 - 8x8 DISCRETE STATE-SPACE OBSERVER
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 3: 8x8 DISCRETE STATE-SPACE OBSERVER ESTIMATION & KALMAN INNOVATION
  State-space formulation at 500 us execution cycle:
    x_pred[k+1] = A * x_hat[k] + B * u[k]
    y_err[k]    = y_meas[k] - (C * x_pred[k+1] + D * u[k])
    x_hat[k+1]  = x_pred[k+1] + L * y_err[k]
====================================================================================================
*)

(* Pack Validated TMR 2oo3 Measurements into Output Vector y_meas *)
vecY_meas[1] := rVoted_PT301;
vecY_meas[2] := rVoted_TT201;
vecY_meas[3] := rVoted_TT401;
vecY_meas[4] := rVoted_PT701;
vecY_meas[5] := rVoted_PT601;
vecY_meas[6] := rVoted_AIT801;
vecY_meas[7] := rVoted_TT401 - 220.0; (* Estimated cryogenic film temperature *)
vecY_meas[8] := rVoted_TT201;

(* Set Reference Target Trajectory Vector *)
vecX_ref[1] := rTargetStagnationPressure;
vecX_ref[2] := rTargetStagnationTemperature;
vecX_ref[3] := 420.0; (* Controlled throat wall temperature setpoint [K] *)
vecX_ref[4] := 0.025; (* Test cabin target static pressure [bar] *)
vecX_ref[5] := 0.350; (* Diffuser exit target backpressure [bar] *)
vecX_ref[6] := 20.85; (* Ideal Mach 7.00 shock angle on 15 deg wedge *)
vecX_ref[7] := 115.0; (* LN2 boundary layer film temp target [K] *)
vecX_ref[8] := rTargetStagnationTemperature;

(* Step 1: Discrete State Propagation x_pred = A * x_hat + B * u *)
FOR iIdx := 1 TO 8 DO
    vecX_pred[iIdx] := 0.0;
    FOR jIdx := 1 TO 8 DO
        vecX_pred[iIdx] := vecX_pred[iIdx] + matA[iIdx, jIdx] * vecX_hat[jIdx];
    END_FOR;
    FOR jIdx := 1 TO 6 DO
        vecX_pred[iIdx] := vecX_pred[iIdx] + matB[iIdx, jIdx] * vecU_cmd[jIdx];
    END_FOR;
END_FOR;

(* Step 2: Output Estimation y_est = C * x_pred + D * u *)
FOR iIdx := 1 TO 8 DO
    vecY_est[iIdx] := 0.0;
    FOR jIdx := 1 TO 8 DO
        vecY_est[iIdx] := vecY_est[iIdx] + matC[iIdx, jIdx] * vecX_pred[jIdx];
    END_FOR;
    FOR jIdx := 1 TO 6 DO
        vecY_est[iIdx] := vecY_est[iIdx] + matD[iIdx, jIdx] * vecU_cmd[jIdx];
    END_FOR;
    (* Innovation error *)
    vecY_err[iIdx] := vecY_meas[iIdx] - vecY_est[iIdx];
END_FOR;

(* Step 3: Measurement Update with Kalman Gain L: x_hat = x_pred + L * y_err *)
FOR iIdx := 1 TO 8 DO
    vecX_hat[iIdx] := vecX_pred[iIdx];
    FOR jIdx := 1 TO 8 DO
        vecX_hat[iIdx] := vecX_hat[iIdx] + matL[iIdx, jIdx] * vecY_err[jIdx];
    END_FOR;
END_FOR;
""")

    # -------------------------------------------------------------------------
    # 8. BODY: PHASE 4 - RECEDING-HORIZON MPC SOLVER
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION SOLVER
  Formulation:
    Minimize J = Sum_{k=1..N} [ (x_k - r_k)^T Q (x_k - r_k) + u_k^T R u_k + (u_k - u_{k-1})^T S (u_k - u_{k-1}) ]
                 + (x_N - r_N)^T P (x_N - r_N)
  Constraints:
    u_min <= u_k <= u_max
    |u_k - u_{k-1}| <= Rate_max * dt
  Horizon: N = 5 Steps | Optimization: Multi-Pass Projected Gradient Descent
====================================================================================================
*)

(* Initialize Optimization Trajectory with Previous Cycle Commands *)
FOR kIdx := 1 TO 5 DO
    FOR mIdx := 1 TO 6 DO
        arrMPC_U_traj[kIdx, mIdx] := vecU_cmd[mIdx];
    END_FOR;
END_FOR;

(* Multi-Pass Projected Gradient Iterations *)
FOR iIdx := 1 TO 3 DO
    (* Forward State Simulation across Horizon N = 5 *)
    FOR kIdx := 1 TO 5 DO
        FOR mIdx := 1 TO 8 DO
            arrMPC_X_traj[kIdx, mIdx] := 0.0;
            IF (kIdx = 1) THEN
                FOR jIdx := 1 TO 8 DO
                    arrMPC_X_traj[kIdx, mIdx] := arrMPC_X_traj[kIdx, mIdx] + matA[mIdx, jIdx] * vecX_hat[jIdx];
                END_FOR;
            ELSE
                FOR jIdx := 1 TO 8 DO
                    arrMPC_X_traj[kIdx, mIdx] := arrMPC_X_traj[kIdx, mIdx] + matA[mIdx, jIdx] * arrMPC_X_traj[kIdx - 1, jIdx];
                END_FOR;
            END_IF;
            FOR jIdx := 1 TO 6 DO
                arrMPC_X_traj[kIdx, mIdx] := arrMPC_X_traj[kIdx, mIdx] + matB[mIdx, jIdx] * arrMPC_U_traj[kIdx, jIdx];
            END_FOR;
        END_FOR;
    END_FOR;

    (* Backward Adjoint Costate Vector Recursion *)
    (* Terminal Costate lambda_N = P * (x_N - r_N) *)
    FOR mIdx := 1 TO 8 DO
        arrMPC_Lambda[5, mIdx] := vecP_diag[mIdx] * (arrMPC_X_traj[5, mIdx] - vecX_ref[mIdx]);
    END_FOR;

    FOR kIdx := 4 DOWNTO 1 DO
        FOR mIdx := 1 TO 8 DO
            arrMPC_Lambda[kIdx, mIdx] := vecQ_diag[mIdx] * (arrMPC_X_traj[kIdx, mIdx] - vecX_ref[mIdx]);
            FOR jIdx := 1 TO 8 DO
                (* Transpose multiplication A^T * lambda_{k+1} *)
                arrMPC_Lambda[kIdx, mIdx] := arrMPC_Lambda[kIdx, mIdx] + matA[jIdx, mIdx] * arrMPC_Lambda[kIdx + 1, jIdx];
            END_FOR;
        END_FOR;
    END_FOR;

    (* Projected Gradient Update: grad = R * u + S * delta_u + B^T * lambda *)
    FOR kIdx := 1 TO 5 DO
        FOR mIdx := 1 TO 6 DO
            arrMPC_GradU[kIdx, mIdx] := vecR_diag[mIdx] * arrMPC_U_traj[kIdx, mIdx];
            IF (kIdx = 1) THEN
                arrMPC_GradU[kIdx, mIdx] := arrMPC_GradU[kIdx, mIdx] + vecS_diag[mIdx] * (arrMPC_U_traj[kIdx, mIdx] - vecU_prev[mIdx]);
            ELSE
                arrMPC_GradU[kIdx, mIdx] := arrMPC_GradU[kIdx, mIdx] + vecS_diag[mIdx] * (arrMPC_U_traj[kIdx, mIdx] - arrMPC_U_traj[kIdx - 1, mIdx]);
            END_IF;
            FOR jIdx := 1 TO 8 DO
                (* Transpose multiplication B^T * lambda *)
                arrMPC_GradU[kIdx, mIdx] := arrMPC_GradU[kIdx, mIdx] + matB[jIdx, mIdx] * arrMPC_Lambda[kIdx, jIdx];
            END_FOR;

            (* Gradient Step with step size alpha = 0.0008 *)
            arrMPC_U_traj[kIdx, mIdx] := arrMPC_U_traj[kIdx, mIdx] - 0.0008 * arrMPC_GradU[kIdx, mIdx];

            (* Enforce Box Constraints u_min <= u <= u_max *)
            IF (arrMPC_U_traj[kIdx, mIdx] > vecU_max[mIdx]) THEN
                arrMPC_U_traj[kIdx, mIdx] := vecU_max[mIdx];
            ELSIF (arrMPC_U_traj[kIdx, mIdx] < vecU_min[mIdx]) THEN
                arrMPC_U_traj[kIdx, mIdx] := vecU_min[mIdx];
            END_IF;
        END_FOR;
    END_FOR;
END_FOR;

(* Extract First Horizon Control Action u_opt = arrMPC_U_traj[1, :] with Slew Limiting *)
FOR mIdx := 1 TO 6 DO
    vecDeltaU[mIdx] := arrMPC_U_traj[1, mIdx] - vecU_prev[mIdx];
    (* Maximum slew rate enforcement *)
    rTempCalc := vecSlew_max[mIdx] * rDt_sec;
    IF (vecDeltaU[mIdx] > rTempCalc) THEN
        vecDeltaU[mIdx] := rTempCalc;
    ELSIF (vecDeltaU[mIdx] < -rTempCalc) THEN
        vecDeltaU[mIdx] := -rTempCalc;
    END_IF;

    vecU_cmd[mIdx] := vecU_prev[mIdx] + vecDeltaU[mIdx];

    (* Final Clamping to Physical Range 0.0 - 100.0 % *)
    IF (vecU_cmd[mIdx] > 100.0) THEN
        vecU_cmd[mIdx] := 100.0;
    ELSIF (vecU_cmd[mIdx] < 0.0) THEN
        vecU_cmd[mIdx] := 0.0;
    END_IF;
END_FOR;
""")

    # -------------------------------------------------------------------------
    # 9. BODY: PHASE 5 - 12-STAGE FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 5: 12-STAGE HYPERSONIC WIND TUNNEL FINITE STATE MACHINE (FSM)
  States:
    0:  STANDBY_FACILITY_MONITOR
    1:  PEBBLE_BED_ELECTRIC_PREHEAT
    2:  CRYOGENIC_NOZZLE_CHILLDOWN
    3:  VACUUM_SPHERE_PUMPDOWN
    4:  ISOLATION_VALVE_FAST_OPEN
    5:  MACH_7_BLOWDOWN_STEADY_RUN
    6:  DYNAMIC_PITCH_AOA_SWEEP
    7:  NOZZLE_THERMAL_SURGE_REGULATION
    8:  TUNNEL_UNSTART_ABORT_TRIP
    9:  NORMAL_BLOWDOWN_TERMINATION
    10: PURGE_AND_COOLING_FLUSH
    11: EMERGENCY_DEPRESSURIZATION
====================================================================================================
*)

(* Hardwired Safety Circuit / E-Stop Overrides All States *)
IF bEmergencyStop THEN
    iMachineState := 11; (* Direct abort to EMERGENCY_DEPRESSURIZATION *)
END_IF;

(* Diffuser Unstart Trip Override *)
IF bTunnelUnstart_TripActive AND (iMachineState <> 8) AND (iMachineState <> 11) THEN
    iMachineState := 8; (* Direct abort to TUNNEL_UNSTART_ABORT_TRIP *)
END_IF;

(* FSM State Timer Increment *)
IF (iMachineState = iPreviousState) THEN
    rStateTimer_sec := rStateTimer_sec + rDt_sec;
    bStateFirstScan := FALSE;
ELSE
    rStateTimer_sec := 0.0;
    bStateFirstScan := TRUE;
    iPreviousState := iMachineState;
END_IF;

CASE iMachineState OF

    0: (* --- STATE 0: STANDBY_FACILITY_MONITOR --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_LN2CoolantValve_Cmd := 2.0; (* Trickle purge to prevent moisture ingress *)
        rActuator_SteamEjector_Cmd := 0.0;
        rActuator_DiffuserThroat_Cmd := 0.0;
        rActuator_PreheaterThyristor_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;

        (* Check Facility Permissives for Automated Blowdown *)
        bPreheatPermissiveMet := (rVoted_TT201 >= (rTargetStagnationTemperature - 50.0));
        bChilldownPermissiveMet := (rVoted_TT401 <= 95.0);
        bVacuumPermissiveMet := (rVacuumSpherePressure <= 0.020);
        bFacilityReadyForBlowdown := bPreheatPermissiveMet AND bChilldownPermissiveMet AND bVacuumPermissiveMet;

        IF bStartBlowdownSequence THEN
            IF NOT bPreheatPermissiveMet THEN
                iMachineState := 1; (* Sequence step: heat pebble bed *)
            ELSIF NOT bChilldownPermissiveMet THEN
                iMachineState := 2; (* Sequence step: cool nozzle *)
            ELSIF NOT bVacuumPermissiveMet THEN
                iMachineState := 3; (* Sequence step: evacuate vacuum receiver *)
            ELSE
                iMachineState := 4; (* All permissives satisfied: initiate blowdown run *)
            END_IF;
        END_IF;

    1: (* --- STATE 1: PEBBLE_BED_ELECTRIC_PREHEAT --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 0.0;

        (* Proportional Thermal Ramp: max heating rate 3.5 K/min to protect zirconia pebbles *)
        IF (rVoted_TT201 < rTargetStagnationTemperature) THEN
            rTempCalc := (rTargetStagnationTemperature - rVoted_TT201) * 0.25;
            IF (rTempCalc > 100.0) THEN rTempCalc := 100.0; END_IF;
            rActuator_PreheaterThyristor_Cmd := rTempCalc;
        ELSE
            rActuator_PreheaterThyristor_Cmd := 5.0; (* Thermal maintenance holding power *)
            bPreheatPermissiveMet := TRUE;
            IF bStartBlowdownSequence THEN
                iMachineState := 2; (* Proceed to Cryogenic Nozzle Chilldown *)
            ELSE
                iMachineState := 0; (* Return to standby *)
            END_IF;
        END_IF;

        IF bAbortBlowdownSequence THEN
            iMachineState := 0;
        END_IF;

    2: (* --- STATE 2: CRYOGENIC_NOZZLE_CHILLDOWN --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;

        (* Ramp LN2 injection to chill nozzle throat down to < 90 K prior to high-enthalpy exposure *)
        IF (rVoted_TT401 > 90.0) THEN
            rActuator_LN2CoolantValve_Cmd := 45.0 + (rVoted_TT401 - 90.0) * 0.25;
            IF (rActuator_LN2CoolantValve_Cmd > 100.0) THEN rActuator_LN2CoolantValve_Cmd := 100.0; END_IF;
        ELSE
            rActuator_LN2CoolantValve_Cmd := 12.0; (* Steady-state cryogenic subcooled blanket *)
            bChilldownPermissiveMet := TRUE;
            IF bStartBlowdownSequence THEN
                iMachineState := 3; (* Proceed to Vacuum Sphere Evacuation *)
            ELSE
                iMachineState := 0;
            END_IF;
        END_IF;

        (* Chilldown Timeout Watchdog (15 minutes) *)
        IF (rStateTimer_sec > 900.0) THEN
            dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0002;
            iMachineState := 0;
        END_IF;

    3: (* --- STATE 3: VACUUM_SPHERE_PUMPDOWN --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;

        (* Engage Motive Steam to Multi-Stage Ejectors *)
        IF (rSteamBoilerSupplyPressure >= 15.0) THEN
            rActuator_SteamEjector_Cmd := 85.0;
            rActuator_DiffuserThroat_Cmd := 50.0; (* Position diffuser second-throat for pumpdown *)
        ELSE
            rActuator_SteamEjector_Cmd := 0.0;
            dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0004; (* Motive Steam Pressure Low *)
        END_IF;

        IF (rVacuumSpherePressure <= 0.015) THEN
            bVacuumPermissiveMet := TRUE;
            IF bStartBlowdownSequence THEN
                iMachineState := 4; (* All Ready: Open Main Isolation Valve *)
            ELSE
                iMachineState := 0;
            END_IF;
        END_IF;

        IF bAbortBlowdownSequence THEN
            iMachineState := 0;
        END_IF;

    4: (* --- STATE 4: ISOLATION_VALVE_FAST_OPEN --- *)
        bBlowdownRun_Active := TRUE;
        rActuator_IsolationValve_Cmd := 100.0; (* Fast hydraulic open stroke < 250 ms *)
        rActuator_SteamEjector_Cmd := 100.0;   (* Full ejector vacuum pull *)
        rActuator_LN2CoolantValve_Cmd := 75.0;  (* Pre-emptive coolant flow surge *)
        rActuator_DiffuserThroat_Cmd := 70.0;  (* Second-throat supersonic started geometry *)

        (* Wait for Full Isolation Valve Mechanical Opening Confirmation (350 ms) *)
        IF (rStateTimer_sec >= 0.350) THEN
            iMachineState := 5; (* Transition to Mach 7 Blowdown Steady Run *)
        END_IF;

        IF bAbortBlowdownSequence THEN
            iMachineState := 9; (* Normal abort termination *)
        END_IF;

    5: (* --- STATE 5: MACH_7_BLOWDOWN_STEADY_RUN --- *)
        bBlowdownRun_Active := TRUE;
        rBlowdownElapsed_sec := rBlowdownElapsed_sec + rDt_sec;

        (* Assign MPC-Optimized Commands to Critical Actuators *)
        rActuator_ThrottleValve_Cmd := vecU_cmd[1];
        rActuator_LN2CoolantValve_Cmd := vecU_cmd[2];
        rActuator_SteamEjector_Cmd := vecU_cmd[3];
        rActuator_DiffuserThroat_Cmd := vecU_cmd[4];
        rActuator_PreheaterThyristor_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 100.0;

        (* Autonomous Transition to Pitch Sweep if requested and flow is established *)
        IF bEnablePitchSweep AND (rStateTimer_sec > 2.5) AND (ABS(rObserved_MachNumber - rTargetMachNumber) < 0.25) THEN
            iMachineState := 6; (* Transition to Dynamic Pitch AoA Sweep *)
        END_IF;

        (* Thermal Surge Monitor: If throat wall exceeds 560 K, intervene immediately *)
        IF (rVoted_TT401 > 560.0) THEN
            iMachineState := 7; (* Transition to Thermal Surge Regulation *)
        END_IF;

        (* Maximum Blowdown Run Duration Limit Reached *)
        IF (rBlowdownElapsed_sec >= rBlowdownMaxRunTime_sec) OR bAbortBlowdownSequence THEN
            iMachineState := 9; (* Transition to Normal Termination *)
        END_IF;

    6: (* --- STATE 6: DYNAMIC_PITCH_AOA_SWEEP --- *)
        bBlowdownRun_Active := TRUE;
        rBlowdownElapsed_sec := rBlowdownElapsed_sec + rDt_sec;

        (* Maintain Aerodynamic MPC Choked Blowdown Regulation *)
        rActuator_ThrottleValve_Cmd := vecU_cmd[1];
        rActuator_LN2CoolantValve_Cmd := vecU_cmd[2];
        rActuator_SteamEjector_Cmd := vecU_cmd[3];
        rActuator_DiffuserThroat_Cmd := vecU_cmd[4];

        (* Execute Pitch Angle-of-Attack Slew Profile *)
        IF (rModel_PitchAngle_Actual < rTestCabinAoA_Command) THEN
            rModel_PitchAngle_Actual := rModel_PitchAngle_Actual + (rPitch_RateLimit_deg_s * rDt_sec);
            IF (rModel_PitchAngle_Actual > rTestCabinAoA_Command) THEN
                rModel_PitchAngle_Actual := rTestCabinAoA_Command;
            END_IF;
        ELSIF (rModel_PitchAngle_Actual > rTestCabinAoA_Command) THEN
            rModel_PitchAngle_Actual := rModel_PitchAngle_Actual - (rPitch_RateLimit_deg_s * rDt_sec);
            IF (rModel_PitchAngle_Actual < rTestCabinAoA_Command) THEN
                rModel_PitchAngle_Actual := rTestCabinAoA_Command;
            END_IF;
        END_IF;

        (* Check for Thermal Runaway *)
        IF (rVoted_TT401 > 560.0) THEN
            iMachineState := 7;
        END_IF;

        IF (rBlowdownElapsed_sec >= rBlowdownMaxRunTime_sec) OR bAbortBlowdownSequence THEN
            iMachineState := 9;
        END_IF;

    7: (* --- STATE 7: NOZZLE_THERMAL_SURGE_REGULATION --- *)
        bBlowdownRun_Active := TRUE;
        rBlowdownElapsed_sec := rBlowdownElapsed_sec + rDt_sec;

        (* Maximize LN2 Coolant Jacket Injection to 100% Full Bore *)
        rActuator_LN2CoolantValve_Cmd := 100.0;

        (* Modulate Throttle Valve Downward by 25% to Reduce Active Aerodynamic Heat Flux *)
        rActuator_ThrottleValve_Cmd := vecU_cmd[1] * 0.75;
        rActuator_SteamEjector_Cmd := vecU_cmd[3];
        rActuator_DiffuserThroat_Cmd := vecU_cmd[4];

        (* Recovery Condition *)
        IF (rVoted_TT401 < 480.0) THEN
            iMachineState := 5; (* Return to steady blowdown *)
        END_IF;

        (* Unrecoverable Thermal Runaway -> Trip *)
        IF (rVoted_TT401 > rAlarm_TT401_HH) THEN
            bThroatThermalRunaway_TripActive := TRUE;
            dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0008;
            iMachineState := 8; (* Unstart / Thermal Abort *)
        END_IF;

        IF (rBlowdownElapsed_sec >= rBlowdownMaxRunTime_sec) OR bAbortBlowdownSequence THEN
            iMachineState := 9;
        END_IF;

    8: (* --- STATE 8: TUNNEL_UNSTART_ABORT_TRIP --- *)
        bBlowdownRun_Active := FALSE;
        (* Fast Emergency Protective Clamping (< 5.0 ms Response) *)
        rActuator_ThrottleValve_Cmd := 0.0;      (* Hydraulic Fast Close < 150 ms *)
        rActuator_IsolationValve_Cmd := 0.0;     (* Immediate Isolation Close *)
        rActuator_FastDumpValve_Cmd := 100.0;    (* Open High-Speed Vent Dump *)
        rActuator_LN2CoolantValve_Cmd := 100.0;  (* Quench Thermal Shock *)
        rActuator_SteamEjector_Cmd := 50.0;      (* Retain Ejector Draft *)
        rActuator_DiffuserThroat_Cmd := 100.0;   (* Fully Open Second Throat to Clear Shock *)
        rActuator_PreheaterThyristor_Cmd := 0.0;

        (* Reset Model Pitch to Neutral 0.0 deg *)
        rModel_PitchAngle_Actual := 0.0;

        (* Maintain Quench Venting for 5.0 seconds before proceeding to cooling flush *)
        IF (rStateTimer_sec >= 5.0) THEN
            iMachineState := 10; (* Purge & Cooling Flush *)
        END_IF;

    9: (* --- STATE 9: NORMAL_BLOWDOWN_TERMINATION --- *)
        bBlowdownRun_Active := FALSE;
        (* Controlled Deceleration Ramp *)
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;
        rActuator_LN2CoolantValve_Cmd := 40.0;   (* Sustained Cooling Post-Run *)
        rActuator_SteamEjector_Cmd := 25.0;      (* Soft Vacuum Rampdown *)
        rActuator_DiffuserThroat_Cmd := 20.0;
        rActuator_PreheaterThyristor_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 0.0;

        (* Return Model Sector to Zero Angle *)
        rModel_PitchAngle_Actual := 0.0;
        rBlowdownElapsed_sec := 0.0;

        IF (rStateTimer_sec >= 8.0) THEN
            iMachineState := 10; (* Proceed to Purge and Post-Test Coolant Flush *)
        END_IF;

    10: (* --- STATE 10: PURGE_AND_COOLING_FLUSH --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 0.0;
        rActuator_SteamEjector_Cmd := 0.0;
        rActuator_PreheaterThyristor_Cmd := 0.0;

        (* Coolant Flush until Nozzle Copper Wall is safely below 150 K *)
        IF (rVoted_TT401 > 150.0) THEN
            rActuator_LN2CoolantValve_Cmd := 25.0;
        ELSE
            rActuator_LN2CoolantValve_Cmd := 2.0; (* Safe standby trickle *)
            IF bAcknowledgeAlarms THEN
                bTunnelUnstart_TripActive := FALSE;
                bThroatThermalRunaway_TripActive := FALSE;
                iMachineState := 0; (* Return to Facility Standby *)
            END_IF;
        END_IF;

    11: (* --- STATE 11: EMERGENCY_DEPRESSURIZATION (SIL-3 E-STOP) --- *)
        bBlowdownRun_Active := FALSE;
        rActuator_ThrottleValve_Cmd := 0.0;
        rActuator_IsolationValve_Cmd := 0.0;
        rActuator_FastDumpValve_Cmd := 100.0;   (* Depressurize high-pressure storage *)
        rActuator_LN2CoolantValve_Cmd := 100.0; (* Full nozzle protection flow *)
        rActuator_SteamEjector_Cmd := 0.0;
        rActuator_DiffuserThroat_Cmd := 100.0;  (* Open wide to vent *)
        rActuator_PreheaterThyristor_Cmd := 0.0;(* De-energize high-power thyristors *)
        rModel_PitchAngle_Actual := 0.0;

        dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#8000_0000; (* Hardwired E-Stop Trip Bit *)

        (* Can only clear with E-Stop released and manual operator acknowledgment *)
        IF (NOT bEmergencyStop) AND bAcknowledgeAlarms THEN
            rActuator_FastDumpValve_Cmd := 0.0;
            iMachineState := 10; (* Transition to Post-Purge Safe State *)
        END_IF;

ELSE
    iMachineState := 0; (* Fail-safe state fallback *)
END_CASE;

iCurrentFSM_State := iMachineState;
""")

    # -------------------------------------------------------------------------
    # 10. BODY: PHASE 6 - ACTUATOR PROFILING & SLEW-RATE LIMITING
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 6: ACTUATOR CONTROL, SLEW-RATE LIMITING & HYDRAULIC VALVE PROFILING
  - Fast Electro-Hydraulic Throttle Valve Non-Linear Equal-Percentage Flow Characteristic.
  - Slew-rate clamping ensuring valve movements adhere to physical dynamic limitations.
====================================================================================================
*)

(* Fast Hydraulic Throttle Valve Stroke Clamping (< 150 ms full stroke = 667 %/sec max rate) *)
IF (rActuator_ThrottleValve_Cmd > 100.0) THEN
    rActuator_ThrottleValve_Cmd := 100.0;
ELSIF (rActuator_ThrottleValve_Cmd < 0.0) THEN
    rActuator_ThrottleValve_Cmd := 0.0;
END_IF;

(* LN2 Coolant Valve Clamping (0 - 100 %) *)
IF (rActuator_LN2CoolantValve_Cmd > 100.0) THEN
    rActuator_LN2CoolantValve_Cmd := 100.0;
ELSIF (rActuator_LN2CoolantValve_Cmd < 0.0) THEN
    rActuator_LN2CoolantValve_Cmd := 0.0;
END_IF;

(* Steam Ejector Valve Clamping *)
IF (rActuator_SteamEjector_Cmd > 100.0) THEN
    rActuator_SteamEjector_Cmd := 100.0;
ELSIF (rActuator_SteamEjector_Cmd < 0.0) THEN
    rActuator_SteamEjector_Cmd := 0.0;
END_IF;

(* Diffuser Throat Actuator Clamping *)
IF (rActuator_DiffuserThroat_Cmd > 100.0) THEN
    rActuator_DiffuserThroat_Cmd := 100.0;
ELSIF (rActuator_DiffuserThroat_Cmd < 0.0) THEN
    rActuator_DiffuserThroat_Cmd := 0.0;
END_IF;

(* Preheater Thyristor Clamping *)
IF (rActuator_PreheaterThyristor_Cmd > 100.0) THEN
    rActuator_PreheaterThyristor_Cmd := 100.0;
ELSIF (rActuator_PreheaterThyristor_Cmd < 0.0) THEN
    rActuator_PreheaterThyristor_Cmd := 0.0;
END_IF;

(* Fast Dump Overpressure Vent Clamping *)
IF (rActuator_FastDumpValve_Cmd > 100.0) THEN
    rActuator_FastDumpValve_Cmd := 100.0;
ELSIF (rActuator_FastDumpValve_Cmd < 0.0) THEN
    rActuator_FastDumpValve_Cmd := 0.0;
END_IF;

(* Save Control Outputs for Next Cycle's MPC Incremental Differential *)
vecU_prev[1] := rActuator_ThrottleValve_Cmd;
vecU_prev[2] := rActuator_LN2CoolantValve_Cmd;
vecU_prev[3] := rActuator_SteamEjector_Cmd;
vecU_prev[4] := rActuator_DiffuserThroat_Cmd;
vecU_prev[5] := rActuator_PreheaterThyristor_Cmd;
vecU_prev[6] := rActuator_FastDumpValve_Cmd;
""")

    # -------------------------------------------------------------------------
    # 11. BODY: PHASE 7 - ISA-18.2 ALARMS & DIAGNOSTIC WORD PACKING
    # -------------------------------------------------------------------------
    chunks.append("""(*
====================================================================================================
  PHASE 7: ISA-18.2 ALARMS ENGINE & DIAGNOSTIC WORD BITFIELD PACKING
  5-Tier Severity Evaluation: HI_HI (SIL-3 Trip), HI (Warning), LO (Warning), LO_LO (SIL-3 Trip),
  and Rate-of-Change (ROC) fast-trip interlock with deadband hysteresis.
====================================================================================================
*)

(* --- 1. PEBBLE BED TOP DOME PRESSURE (PT-101) ALARM EVALUATION --- *)
rTempCalc := (rVoted_PT101 - rAlarm_PT101_Prev) / rDt_sec;
rAlarm_PT101_Prev := rVoted_PT101;

IF (rVoted_PT101 >= rAlarm_PT101_HH) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0010;
    bAlarm_PT101_Trip := TRUE;
ELSIF (rVoted_PT101 <= (rAlarm_PT101_HH - rAlarm_PT101_DB)) AND NOT (rVoted_PT101 <= rAlarm_PT101_LL) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_0010; bAlarm_PT101_Trip := FALSE; END_IF;
END_IF;

IF (rVoted_PT101 >= rAlarm_PT101_H) AND (rVoted_PT101 < rAlarm_PT101_HH) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0010;
ELSIF (rVoted_PT101 <= (rAlarm_PT101_H - rAlarm_PT101_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_HighWarning := dwAlarmWord_HighWarning AND NOT 16#0000_0010; END_IF;
END_IF;

IF (ABS(rTempCalc) >= rAlarm_PT101_ROC) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0020; (* Pressure Transient ROC *)
END_IF;

(* --- 2. PEBBLE BED CORE TEMPERATURE (TT-201) ALARM EVALUATION --- *)
rTempCalc := (rVoted_TT201 - rAlarm_TT201_Prev) / (rDt_sec * 60.0);
rAlarm_TT201_Prev := rVoted_TT201;

IF (rVoted_TT201 >= rAlarm_TT201_HH) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0040;
    bAlarm_TT201_Trip := TRUE;
ELSIF (rVoted_TT201 <= (rAlarm_TT201_HH - rAlarm_TT201_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_0040; bAlarm_TT201_Trip := FALSE; END_IF;
END_IF;

IF (rVoted_TT201 >= rAlarm_TT201_H) AND (rVoted_TT201 < rAlarm_TT201_HH) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0040;
ELSIF (rVoted_TT201 <= (rAlarm_TT201_H - rAlarm_TT201_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_HighWarning := dwAlarmWord_HighWarning AND NOT 16#0000_0040; END_IF;
END_IF;

(* --- 3. NOZZLE STAGNATION TOTAL PRESSURE (PT-301) ALARM EVALUATION --- *)
rTempCalc := (rVoted_PT301 - rAlarm_PT301_Prev) / rDt_sec;
rAlarm_PT301_Prev := rVoted_PT301;

IF (rVoted_PT301 >= rAlarm_PT301_HH) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0100;
    bAlarm_PT301_Trip := TRUE;
ELSIF (rVoted_PT301 <= (rAlarm_PT301_HH - rAlarm_PT301_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_0100; bAlarm_PT301_Trip := FALSE; END_IF;
END_IF;

IF (rVoted_PT301 >= rAlarm_PT301_H) AND (rVoted_PT301 < rAlarm_PT301_HH) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0100;
ELSIF (rVoted_PT301 <= (rAlarm_PT301_H - rAlarm_PT301_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_HighWarning := dwAlarmWord_HighWarning AND NOT 16#0000_0100; END_IF;
END_IF;

(* --- 4. NOZZLE THROAT INNER WALL TEMPERATURE (TT-401) ALARM EVALUATION --- *)
rTempCalc := (rVoted_TT401 - rAlarm_TT401_Prev) / rDt_sec;
rAlarm_TT401_Prev := rVoted_TT401;

IF (rVoted_TT401 >= rAlarm_TT401_HH) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0200;
    bAlarm_TT401_Trip := TRUE;
ELSIF (rVoted_TT401 <= (rAlarm_TT401_HH - rAlarm_TT401_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_0200; bAlarm_TT401_Trip := FALSE; END_IF;
END_IF;

IF (rVoted_TT401 >= rAlarm_TT401_H) AND (rVoted_TT401 < rAlarm_TT401_HH) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0200;
ELSIF (rVoted_TT401 <= (rAlarm_TT401_H - rAlarm_TT401_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_HighWarning := dwAlarmWord_HighWarning AND NOT 16#0000_0200; END_IF;
END_IF;

IF (rTempCalc >= rAlarm_TT401_ROC) THEN
    dwAlarmWord_HighWarning := dwAlarmWord_HighWarning OR 16#0000_0400; (* Thermal Shock Gradient Warning *)
END_IF;

(* --- 5. CRYO LN2 COOLANT FLOW (FT-501) ALARM EVALUATION --- *)
IF (rVoted_FT501 <= rAlarm_FT501_LL) AND (iMachineState = 5 OR iMachineState = 6 OR iMachineState = 7) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_0800;
    bAlarm_FT501_Trip := TRUE;
ELSIF (rVoted_FT501 >= (rAlarm_FT501_LL + rAlarm_FT501_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_0800; bAlarm_FT501_Trip := FALSE; END_IF;
END_IF;

IF (rVoted_FT501 <= rAlarm_FT501_L) AND (rVoted_FT501 > rAlarm_FT501_LL) AND (iMachineState >= 4) THEN
    dwAlarmWord_LowWarning := dwAlarmWord_LowWarning OR 16#0000_0800;
ELSIF (rVoted_FT501 >= (rAlarm_FT501_L + rAlarm_FT501_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_LowWarning := dwAlarmWord_LowWarning AND NOT 16#0000_0800; END_IF;
END_IF;

(* --- 6. SUPERSONIC DIFFUSER EXIT STATIC PRESSURE (PT-601) ALARM EVALUATION --- *)
IF (rVoted_PT601 >= rAlarm_PT601_HH) AND (iMachineState >= 4) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_1000;
    bAlarm_PT601_Trip := TRUE;
ELSIF (rVoted_PT601 <= (rAlarm_PT601_HH - rAlarm_PT601_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_1000; bAlarm_PT601_Trip := FALSE; END_IF;
END_IF;

(* --- 7. TEST CABIN SUPERSONIC STATIC WALL PRESSURE (PT-701) ALARM EVALUATION --- *)
IF (rVoted_PT701 >= rAlarm_PT701_HH) AND (iMachineState = 5 OR iMachineState = 6 OR iMachineState = 7) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_2000;
    bAlarm_PT701_Trip := TRUE;
ELSIF (rVoted_PT701 <= (rAlarm_PT701_HH - rAlarm_PT701_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_2000; bAlarm_PT701_Trip := FALSE; END_IF;
END_IF;

(* --- 8. SCHLIEREN OBLIQUE SHOCK ANGLE (AIT-801) ALARM EVALUATION --- *)
IF (rVoted_AIT801 >= rAlarm_AIT801_HH) AND (iMachineState = 5 OR iMachineState = 6) THEN
    dwAlarmWord_Critical := dwAlarmWord_Critical OR 16#0000_4000;
    bAlarm_AIT801_Trip := TRUE;
ELSIF (rVoted_AIT801 <= (rAlarm_AIT801_HH - rAlarm_AIT801_DB)) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Critical := dwAlarmWord_Critical AND NOT 16#0000_4000; bAlarm_AIT801_Trip := FALSE; END_IF;
END_IF;

(* --- TMR 2oo3 SENSOR SUBSYSTEM HEALTH BITFIELD PACKING (dwSensorHealthWord) --- *)
dwSensorHealthWord := 16#0000_0000;
IF bDegraded_PT101 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0001; END_IF;
IF bTrip_PT101 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0002; END_IF;
IF bDegraded_TT201 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0004; END_IF;
IF bTrip_TT201 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0008; END_IF;
IF bDegraded_PT301 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0010; END_IF;
IF bTrip_PT301 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0020; END_IF;
IF bDegraded_TT401 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0040; END_IF;
IF bTrip_TT401 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0080; END_IF;
IF bDegraded_FT501 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0100; END_IF;
IF bTrip_FT501 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0200; END_IF;
IF bDegraded_PT601 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0400; END_IF;
IF bTrip_PT601 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_0800; END_IF;
IF bDegraded_PT701 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_1000; END_IF;
IF bTrip_PT701 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_2000; END_IF;
IF bDegraded_AIT801 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_4000; END_IF;
IF bTrip_AIT801 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0000_8000; END_IF;

(* Individual Channel Discrepancy Fault Bits *)
IF bFault_PT101A THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0001_0000; END_IF;
IF bFault_PT101B THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0002_0000; END_IF;
IF bFault_PT101C THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0004_0000; END_IF;
IF bFault_PT301A THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0008_0000; END_IF;
IF bFault_PT301B THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0010_0000; END_IF;
IF bFault_PT301C THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0020_0000; END_IF;
IF bFault_TT401A THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0040_0000; END_IF;
IF bFault_TT401B THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0080_0000; END_IF;
IF bFault_TT401C THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0100_0000; END_IF;
IF bFault_PT701A THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0200_0000; END_IF;
IF bFault_PT701B THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0400_0000; END_IF;
IF bFault_PT701C THEN dwSensorHealthWord := dwSensorHealthWord OR 16#0800_0000; END_IF;

(* --- 32-BIT SYSTEM OPERATIONAL STATUS REGISTER PACKING (dwSystemStatusWord) --- *)
dwSystemStatusWord := 16#0000_0000;
IF bBlowdownRun_Active THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bPreheatPermissiveMet THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bChilldownPermissiveMet THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bVacuumPermissiveMet THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bFacilityReadyForBlowdown THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bTunnelUnstart_TripActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bThroatThermalRunaway_TripActive THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF bEmergencyStop THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;

(* Pack Current State into Bits 8..11 *)
dwSystemStatusWord := dwSystemStatusWord OR SHL(INT_TO_DWORD(iMachineState), 8);

(* Pack Actuator Saturation Bits into Bits 16..21 *)
IF (rActuator_ThrottleValve_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0001_0000; END_IF;
IF (rActuator_LN2CoolantValve_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0002_0000; END_IF;
IF (rActuator_SteamEjector_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0004_0000; END_IF;
IF (rActuator_DiffuserThroat_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0008_0000; END_IF;
IF (rActuator_PreheaterThyristor_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0010_0000; END_IF;
IF (rActuator_FastDumpValve_Cmd >= 99.5) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0020_0000; END_IF;

(* Master Healthy Evaluation *)
bSystemHealthy := (dwAlarmWord_Critical = 16#0000_0000) AND NOT bEmergencyStop AND NOT bTunnelUnstart_TripActive;
IF bSystemHealthy THEN
    dwSystemStatusWord := dwSystemStatusWord OR 16#8000_0000;
END_IF;

(* Clear Warnings on Manual Operator Acknowledgment *)
IF bAcknowledgeAlarms THEN
    dwAlarmWord_LowWarning := 16#0000_0000;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 12. END OF FUNCTION BLOCK
    # -------------------------------------------------------------------------
    chunks.append("END_FUNCTION_BLOCK\n")

    return "".join(chunks)

print("Generator definition complete.")
