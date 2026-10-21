# st_part1_declarations.py

def get_declarations():
    return """FUNCTION_BLOCK FB_SolarThermal_ZnO_ThermochemicalWaterSplitting
(*
 ====================================================================================================
  PROJECT:       SOLAR HYDROGEN GENERATION & THERMOCHEMICAL WATER-SPLITTING INFRASTRUCTURE
  SUBSYSTEM:     1,800 DEG C HIGH-FLUX SOLAR-THERMAL ZINC OXIDE (ZnO) CAVITY RECEIVER & REDOX CYCLE
  CONTROLLER:    IEC 61131-3 DETERMINISTIC CYBER-PHYSICAL MULTI-VARIABLE SUPERVISOR
  ENGINEER:      PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX-PERSONA)
  STANDARD:      IEC 61131-3 3RD ED, IEC 61508 (SIL-3), ISA-18.2 (ALARM MGMT), ASME PTC 52 (SOLAR)
 ====================================================================================================

  EXECUTIVE ENGINEERING SUMMARY & PROCESS ARCHITECTURE:
  --------------------------------------------------------------------------------------------------
  This Function Block executes hard real-time, deterministic control, dynamic balancing, state-space
  estimation, and fault-tolerant trip supervision for a closed-loop solar-driven zinc oxide / zinc (ZnO/Zn)
  thermochemical two-step water-splitting reactor operating at an ultra-high temperature setpoint of
  1,800.0 deg C (2,073.15 K) under high-flux concentrated solar radiation (1,000 to 5,000 kW/m2).

  The two-step thermochemical water-splitting cycle comprises:
    Step 1 (Solar Endothermic Dissociation):
      ZnO(s) + Concentrated Solar Flux -> Zn(g) + 0.5 O2(g)   [Delta H_298 = +461.3 kJ/mol]
      Operating Envelope: 1,750 deg C - 1,850 deg C; Static Pressure: 0.85 - 1.20 bar absolute.
    Step 2 (Non-Solar Exothermic Hydrolysis / Water-Splitting):
      Zn(s/l) + H2O(g) -> ZnO(s) + H2(g)                      [Delta H_298 = -101.4 kJ/mol]
      Operating Envelope: 350 deg C - 450 deg C; Exothermic off-gas recovery producing ultra-pure green H2.

  The cyber-physical complexity of this reactor demands simultaneous execution of four mission-critical
  high-speed domains:
    1. Cavity Receiver High-Flux Radiant Heat Dynamic Balancing:
       Concentrated solar power from a 2,500-heliostat field delivers up to 5 MWth into an 800 mm aperture.
       Non-uniform irradiance distributions induce catastrophic circumferential thermal gradients across
       the high-purity silicon carbide (SiC) / Hafnia (HfO2) refractory cavity. The FB calculates real-time
       azimuth and elevation trim vectors (mrad) for heliostat aimpoint distribution, controlling mechanical
       water-cooled flux attenuator irises to limit refractory stress < 85 MPa and keep delta-T < 45 deg C.

    2. Zinc Vapor Rapid Condensation Aerodynamic Quench Gas Curtain:
       At 1,800 deg C, dissociation is spontaneous. However, as dissociation products exit the reaction zone,
       the backward recombination reaction (Zn(g) + 0.5 O2(g) -> ZnO(s)) occurs violently within 50 ms if
       the gas mixture cools slowly. To prevent re-oxidation, an annular supersonic De Laval nozzle array
       injects an inert Argon quench gas curtain at velocities between 180 and 320 m/s. This achieves a shock
       chilling cooling gradient exceeding 1.0E+05 K/s, freezing the gas equilibrium and spontaneously nucleating
       submicron zinc metal aerosols (< 250 nm) while suppressing recombination (Damkohler number Da << 0.05).

    3. Non-Stoichiometric Redox Kinetic Observer (ZnO_1-delta):
       High-temperature thermal dissociation is governed by oxygen vacancy (V_O'') defect formation and zinc
       interstitial (Zn_i'') migration within the non-stoichiometric lattice. The FB embeds a discretized
       Luenberger/Kalman state-space kinetic observer that reconstructs the unmeasured non-stoichiometry parameter
       (delta), thermodynamic equilibrium constant Kp(T), dissociation rate (mol/s), and real-time Zn vapor yield.

    4. High-Temperature Quartz Window Protective Gas Sweeping:
       The cavity aperture is sealed by a fused silica (quartz) optical window (800 mm diam, 25 mm thick) to
       maintain an inert reactor atmosphere and capture product gases. If zinc vapor or ZnO dust deposits on the
       quartz, solar absorptivity spikes, causing rapid thermal runaway and catastrophic devitrification into
       cristobalite (phase transition at > 950 deg C) followed by explosive mechanical fracture. A high-swirl
       annular vortex sweeping curtain of high-purity Argon creates an aerodynamic barrier layer (Stokes number
       Stk << 0.01) repelling particles and vapor while monitoring transmissivity and cumulative devitrification.

  REDUNDANCY, SAFETY & REGULATORY COMPLIANCE:
  --------------------------------------------------------------------------------------------------
  - 2oo3 Triple Modular Redundancy (TMR) voting across all primary analog process channels:
      * Cavity Core Pyrometers (Dual-wavelength infrared pyrometry: 0.95 um / 1.05 um)
      * Aperture Incident Solar Calorimeters
      * Quartz Window Infrared Thermopile Sensors
      * Quench Gas Manifold Pressure Transmitters
  - Fully constrained Discrete Model Predictive Control (MPC) quadratic cost approximation with projected
    gradient descent solving for optimal multi-variable actuation.
  - Complete 4x4 state-space continuous and discrete matrices with disturbance modeling.
  - Multi-stage Deterministic Finite State Machine (12 operational states from Cold Shutdown to Solar Water Splitting).
  - ISA-18.2 compliant First-Out latching diagnostic alarm matrix with sub-50 ms emergency shutter trip.
*)

VAR_INPUT
    (* ========================================================================================= *)
    (* SECTION 1: MASTER COMMANDS & SAFETY DISCRETE SIGNALS                                      *)
    (* ========================================================================================= *)
    bSystemEnable                   : BOOL;     (* Master process start enable command [BOOL] *)
    bEmergencyStop                  : BOOL;     (* Hardwired SIL-3 emergency stop circuit (Active Low) [BOOL] *)
    bHeliostatFieldReady            : BOOL;     (* Solar concentrator field tracking locked & interlocked [BOOL] *)

    (* ========================================================================================= *)
    (* SECTION 2: HIGH-FLUX SOLAR RADIATIVE & CAVITY TEMPERATURE SENSORS (TMR 2oo3)               *)
    (* ========================================================================================= *)
    rSolarDirectNormalIrradiance_W_m2 : REAL;   (* Direct Normal Irradiance from primary pyrheliometer [kW/m2] / [W/m2] (0.0 to 1200.0) *)
    rApertureIncidentFlux_A_kW_m2   : REAL;     (* High-flux solar calorimeter pyrometer Ch A [kW/m2] (0.0 to 5000.0) *)
    rApertureIncidentFlux_B_kW_m2   : REAL;     (* High-flux solar calorimeter pyrometer Ch B [kW/m2] (0.0 to 5000.0) *)
    rApertureIncidentFlux_C_kW_m2   : REAL;     (* High-flux solar calorimeter pyrometer Ch C [kW/m2] (0.0 to 5000.0) *)
    rCavityPyrometerTemp_A_degC     : REAL;     (* Cavity receiver optical pyrometer Ch A (2-color 0.95/1.05 um) [deg C] (0.0 to 2200.0) *)
    rCavityPyrometerTemp_B_degC     : REAL;     (* Cavity receiver optical pyrometer Ch B (2-color 0.95/1.05 um) [deg C] (0.0 to 2200.0) *)
    rCavityPyrometerTemp_C_degC     : REAL;     (* Cavity receiver optical pyrometer Ch C (2-color 0.95/1.05 um) [deg C] (0.0 to 2200.0) *)

    (* ========================================================================================= *)
    (* SECTION 3: QUARTZ APERTURE WINDOW INFRARED SENSORS (TMR 2oo3)                             *)
    (* ========================================================================================= *)
    rQuartzWindowTemp_A_degC        : REAL;     (* Fused silica aperture window IR thermopile Ch A [deg C] (0.0 to 1400.0) *)
    rQuartzWindowTemp_B_degC        : REAL;     (* Fused silica aperture window IR thermopile Ch B [deg C] (0.0 to 1400.0) *)
    rQuartzWindowTemp_C_degC        : REAL;     (* Fused silica aperture window IR thermopile Ch C [deg C] (0.0 to 1400.0) *)

    (* ========================================================================================= *)
    (* SECTION 4: FLUID FLOWS, VELOCITIES, PRESSURES & REAGENT FEEDS                             *)
    (* ========================================================================================= *)
    rWindowSweepGasFlow_Nm3_h       : REAL;     (* Argon protective aerodynamic vortex sweep flow [Nm3/h] (0.0 to 500.0) *)
    rQuenchGasCurtainFlow_Nm3_h     : REAL;     (* Argon rapid quench gas curtain mass flow rate [Nm3/h] (0.0 to 2500.0) *)
    rQuenchNozzleInletPress_bar     : REAL;     (* Supersonic quench curtain nozzle manifold pressure [bar] (0.0 to 30.0) *)
    rReactorInternalPress_bar       : REAL;     (* Reactor cavity core static absolute pressure [bar] (0.2 to 5.0) *)
    rZnO_FeedRate_kg_h              : REAL;     (* High-purity micronized ZnO powder feeder delivery rate [kg/h] (0.0 to 250.0) *)
    rQuenchGasCurtainVelocity_m_s   : REAL;     (* Quench curtain nozzle exit gas velocity from pitot [m/s] (0.0 to 350.0) *)

    (* ========================================================================================= *)
    (* SECTION 5: OPTICAL, MECHANICAL & DIAGNOSTIC SENSORY INPUTS                                *)
    (* ========================================================================================= *)
    rQuartzWindowTransmissivity_pct : REAL;     (* Quartz aperture optical transmittance laser ratio [%] (0.0 to 100.0) *)
    rCavityCeramicStrain_microstrain: REAL;     (* SiC refractory fiber optic Bragg grating hoop strain [microstrain] (-5000.0 to +5000.0) *)
    rSteamInjectionRate_kg_h        : REAL;     (* Superheated steam hydrolyzer reagent injection rate [kg/h] (0.0 to 150.0) *)
    rCycleTime_s                    : REAL;     (* Deterministic PLC scan execution task cycle interval [s] (0.005 to 0.100) *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================= *)
    (* SECTION 1: MASTER PROCESS PERMISSIVE & HIGH-SPEED SAFETY ACTUATORS                        *)
    (* ========================================================================================= *)
    bReactorOperational             : BOOL;     (* Reactor operating inside certified safety & process envelope [BOOL] *)
    bFastOpticalShutterClose        : BOOL;     (* Emergency high-speed pneumatic water-cooled aperture shutter trip [BOOL] *)
    bHeliostatDefocusCommand        : BOOL;     (* Emergency heliostat field emergency defocus / beam dump command [BOOL] *)

    (* ========================================================================================= *)
    (* SECTION 2: HELIOSTAT AIMPOINT TRIM & MECHANICAL ATTENUATION                               *)
    (* ========================================================================================= *)
    rHeliostatAimingTrim_X_mrad     : REAL;     (* Solar flux aimpoint azimuth offset adjustment vector [mrad] (-25.0 to +25.0) *)
    rHeliostatAimingTrim_Y_mrad     : REAL;     (* Solar flux aimpoint elevation offset adjustment vector [mrad] (-25.0 to +25.0) *)
    rApertureAttenuatorPosition_pct : REAL;     (* Dynamic mechanical flux attenuation iris position command [%] (0.0 to 100.0) *)

    (* ========================================================================================= *)
    (* SECTION 3: PROCESS MODULATING VALVES & FEED DRIVES                                        *)
    (* ========================================================================================= *)
    rWindowPurgeValveCmd_pct        : REAL;     (* Fused quartz vortex sweep argon flow control valve command [%] (0.0 to 100.0) *)
    rQuenchCurtainValveCmd_pct      : REAL;     (* Supersonic quench aerodynamic gas curtain valve command [%] (0.0 to 100.0) *)
    rZnO_FeederSpeedCmd_pct         : REAL;     (* ZnO particle metering screw / pneumatic feed drive setpoint [%] (0.0 to 100.0) *)

    (* ========================================================================================= *)
    (* SECTION 4: REAL-TIME KINETIC OBSERVER & PHYSICAL STRUCTURAL ESTIMATES                     *)
    (* ========================================================================================= *)
    rEstimatedZnVaporYield_mol_s    : REAL;     (* Real-time non-stoichiometric redox observer Zn vapor yield [mol/s] *)
    rEstimatedDissociationRate_pct  : REAL;     (* Fractional conversion efficiency of ZnO thermolysis [%] (0.0 to 100.0) *)
    rQuartzDevitrificationRisk_pct  : REAL;     (* Cristobalite phase transformation cumulative damage fraction [%] (0.0 to 100.0) *)
    rCeramicRefractoryStress_MPa    : REAL;     (* Maximum computed thermo-mechanical von Mises stress in SiC [MPa] *)

    (* ========================================================================================= *)
    (* SECTION 5: 2oo3 TMR VALIDATED SENSOR MEASUREMENTS                                         *)
    (* ========================================================================================= *)
    rVotedCavityTemp_degC           : REAL;     (* 2oo3 TMR validated cavity receiver temperature [deg C] *)
    rVotedSolarFlux_kW_m2           : REAL;     (* 2oo3 TMR validated solar incident flux [kW/m2] *)
    rVotedWindowTemp_degC           : REAL;     (* 2oo3 TMR validated quartz aperture window temperature [deg C] *)
    rVotedQuenchPress_bar           : REAL;     (* 2oo3 TMR validated quench manifold pressure [bar] *)

    (* ========================================================================================= *)
    (* SECTION 6: STATUS, DIAGNOSTICS & ALARM WORDS                                              *)
    (* ========================================================================================= *)
    wSafetyStatusWord               : WORD;     (* Safety interlocking & permissive status bit-field [WORD] *)
    wSystemWarningWord              : WORD;     (* Process diagnostic warning & sensor health bit-field [WORD] *)
    dwAlarmWordFirstOut             : DWORD;    (* ISA-18.2 compliant First-Out latching trip diagnostic word [DWORD] *)
    iOperationalState               : INT;      (* Deterministic finite state machine operational state code [INT] *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* SECTION 1: EXECUTION INITIALIZATION & FINITE STATE MACHINE (FSM) VARIABLES                *)
    (* ========================================================================================= *)
    bInitialized                    : BOOL := FALSE;
    iState                          : INT := 0;      (* Current operating state index *)
    iPrevState                      : INT := 0;      (* Previous operating state index *)
    rStateTimer_s                   : REAL := 0.0;    (* Dwell time accumulator in current state [s] *)
    rStateTransitionTimer_s         : REAL := 0.0;    (* Dynamic ramp transition timer [s] *)

    (* ========================================================================================= *)
    (* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ENGINE DATA STRUCTURES                    *)
    (* ========================================================================================= *)
    (* Channel Health Flags *)
    bCavityTemp_A_Healthy           : BOOL := TRUE;
    bCavityTemp_B_Healthy           : BOOL := TRUE;
    bCavityTemp_C_Healthy           : BOOL := TRUE;
    bSolarFlux_A_Healthy            : BOOL := TRUE;
    bSolarFlux_B_Healthy            : BOOL := TRUE;
    bSolarFlux_C_Healthy            : BOOL := TRUE;
    bWindowTemp_A_Healthy           : BOOL := TRUE;
    bWindowTemp_B_Healthy           : BOOL := TRUE;
    bWindowTemp_C_Healthy           : BOOL := TRUE;
    bQuenchPress_A_Healthy          : BOOL := TRUE;
    bQuenchPress_B_Healthy          : BOOL := TRUE;
    bQuenchPress_C_Healthy          : BOOL := TRUE;

    (* Channel Deviation Timers [s] *)
    rCavityTemp_DiscrepancyTimer_s  : REAL := 0.0;
    rSolarFlux_DiscrepancyTimer_s   : REAL := 0.0;
    rWindowTemp_DiscrepancyTimer_s  : REAL := 0.0;
    rQuenchPress_DiscrepancyTimer_s : REAL := 0.0;

    (* Channel Drift Filter Accumulators *)
    rCavityTemp_A_Filtered          : REAL := 0.0;
    rCavityTemp_B_Filtered          : REAL := 0.0;
    rCavityTemp_C_Filtered          : REAL := 0.0;
    rSolarFlux_A_Filtered           : REAL := 0.0;
    rSolarFlux_B_Filtered           : REAL := 0.0;
    rSolarFlux_C_Filtered           : REAL := 0.0;

    (* ========================================================================================= *)
    (* SECTION 3: STATE-SPACE CYBER-PHYSICAL MODEL MATRICES (4 STATES, 3 INPUTS, 3 DISTURBANCES)  *)
    (* ========================================================================================= *)
    (* States x:                                                                                 *)
    (*   x[1] = Cavity Refractory Inner Wall Temp [deg C]                                        *)
    (*   x[2] = Fused Quartz Aperture Window Temp [deg C]                                        *)
    (*   x[3] = Zinc Vapor Core Partial Density [g/m3]                                           *)
    (*   x[4] = Quench Boundary Layer Gas Temp [deg C]                                           *)
    (* Inputs u:                                                                                 *)
    (*   u[1] = Aperture Flux Attenuator Position [%]                                            *)
    (*   u[2] = Quench Gas Curtain Mass Flow [%]                                                 *)
    (*   u[3] = Quartz Vortex Sweep Gas Flow [%]                                                 *)
    (* Disturbances d:                                                                           *)
    (*   d[1] = Direct Normal Irradiance Variation [W/m2]                                        *)
    (*   d[2] = ZnO Powder Feed Thermal Load [kg/h]                                              *)
    (*   d[3] = Ambient Convective Dissipation Wind [m/s]                                        *)

    aA_Cont                         : ARRAY[1..4, 1..4] OF REAL; (* Continuous Plant Matrix A *)
    aB_Cont                         : ARRAY[1..4, 1..3] OF REAL; (* Continuous Input Matrix B *)
    aC_Cont                         : ARRAY[1..4, 1..4] OF REAL; (* Continuous Output Matrix C *)
    aD_Cont                         : ARRAY[1..4, 1..3] OF REAL; (* Continuous Feedforward Matrix D *)
    aBd_Cont                        : ARRAY[1..4, 1..3] OF REAL; (* Continuous Disturbance Matrix Bd *)

    aA_Disc                         : ARRAY[1..4, 1..4] OF REAL; (* Discretized Plant Matrix Ad *)
    aB_Disc                         : ARRAY[1..4, 1..3] OF REAL; (* Discretized Input Matrix Bd *)
    aC_Disc                         : ARRAY[1..4, 1..4] OF REAL; (* Discretized Output Matrix Cd *)
    aBd_Disc                        : ARRAY[1..4, 1..3] OF REAL; (* Discretized Disturbance Matrix Bdd *)

    aX_State                        : ARRAY[1..4] OF REAL;       (* Actual Plant State Vector x *)
    aX_Est                          : ARRAY[1..4] OF REAL;       (* Observer Estimated State Vector x_hat *)
    aX_Pred                         : ARRAY[1..4] OF REAL;       (* One-Step Ahead Predicted State x_pred *)
    aY_Meas                         : ARRAY[1..4] OF REAL;       (* Measured Process Output Vector y *)
    aY_Est                          : ARRAY[1..4] OF REAL;       (* Estimated Process Output Vector y_hat *)
    aU_Ctrl                         : ARRAY[1..3] OF REAL;       (* Control Input Vector u *)
    aD_Dist                         : ARRAY[1..3] OF REAL;       (* Disturbance Vector d *)

    (* Observer Gain Matrix L (4x4) *)
    aL_Obs                          : ARRAY[1..4, 1..4] OF REAL;

    (* ========================================================================================= *)
    (* SECTION 4: CONSTRAINED MODEL PREDICTIVE CONTROL (MPC) QUADRATIC PROGRAMMING SOLVER        *)
    (* ========================================================================================= *)
    (* Horizon Np = 3, Nc = 2; Decision vector DeltaU has dimension 6 (3 inputs x 2 steps)       *)
    aQ_Weight                       : ARRAY[1..4, 1..4] OF REAL; (* State Error Weighting Matrix Q *)
    aR_Weight                       : ARRAY[1..3, 1..3] OF REAL; (* Control Increment Weighting Matrix R *)
    aHessian                        : ARRAY[1..6, 1..6] OF REAL; (* Condensed Quadratic Hessian H *)
    aGrad                           : ARRAY[1..6] OF REAL;       (* Linear Cost Gradient Vector g *)
    aDeltaU_Opt                     : ARRAY[1..6] OF REAL;       (* Optimal Incremental Control Vector *)
    aDeltaU_Prev                    : ARRAY[1..6] OF REAL;       (* Previous Slew Solution *)
    aU_Min                          : ARRAY[1..3] OF REAL;       (* Lower Bound on Control Inputs *)
    aU_Max                          : ARRAY[1..3] OF REAL;       (* Upper Bound on Control Inputs *)
    aDeltaU_Min                     : ARRAY[1..3] OF REAL;       (* Minimum Permissible Slew Rate *)
    aDeltaU_Max                     : ARRAY[1..3] OF REAL;       (* Maximum Permissible Slew Rate *)

    (* Setpoint Vector y_ref *)
    aY_Setpoint                     : ARRAY[1..4] OF REAL;

    (* Projected Gradient Optimization Parameters *)
    iMPC_Iteration                  : INT := 0;
    iMPC_MaxIter                    : INT := 12;
    rMPC_StepSize                   : REAL := 0.045;
    rMPC_ConvergenceTol             : REAL := 0.001;
    rMPC_CostValue                  : REAL := 0.0;

    (* ========================================================================================= *)
    (* SECTION 5: NON-STOICHIOMETRIC REDOX KINETIC OBSERVER (ZnO_1-delta)                        *)
    (* ========================================================================================= *)
    rGasConstant_R                  : REAL := 8.31446; (* J/(mol K) *)
    rStdEnthalpy_kJ_mol             : REAL := 461.3;   (* Standard enthalpy of dissociation at 298 K *)
    rStdEntropy_J_molK              : REAL := 288.5;   (* Standard entropy of dissociation at 298 K *)
    rArrheniusPreExp_k0             : REAL := 1.25E+06;(* Pre-exponential kinetic frequency factor [1/s] *)
    rActivationEnergy_Ea            : REAL := 3.12E+05;(* Dissociation activation energy [J/mol] *)
    rDelta_NonStoichiometry         : REAL := 0.0001;  (* Oxygen deficiency parameter delta in ZnO_1-delta *)
    rEquilibriumConstant_Kp         : REAL := 0.0;     (* Thermochemical equilibrium constant Kp(T) *)
    rPartialPress_Zn_bar            : REAL := 0.0;     (* Calculated equilibrium zinc vapor pressure [bar] *)
    rPartialPress_O2_bar            : REAL := 0.0;     (* Calculated equilibrium oxygen partial pressure [bar] *)
    rDissociationReactionRate_mol_s : REAL := 0.0;     (* Instantaneous molar rate of dissociation [mol/s] *)
    rCumulativeZnProduced_kg        : REAL := 0.0;     (* Cumulative synthesized metallic zinc inventory [kg] *)
    rThermodynamicAffinity_kJ_mol   : REAL := 0.0;     (* Chemical affinity driving force A = -Delta G *)

    (* ========================================================================================= *)
    (* SECTION 6: SUPERSONIC AERODYNAMIC QUENCH GAS CURTAIN FLUID MECHANICS                      *)
    (* ========================================================================================= *)
    rArgonHeatCapacityRatio_gamma   : REAL := 1.667;   (* Specific heat ratio for monatomic argon *)
    rArgonMolecularWeight_g_mol     : REAL := 39.948;  (* Molar mass of argon carrier gas [g/mol] *)
    rQuenchMachNumber               : REAL := 1.45;    (* Design De Laval nozzle exit Mach number *)
    rQuenchCurtainMomentumRatio_J   : REAL := 4.8;     (* Momentum flux ratio curtain-to-core gas *)
    rDamkohlerNumber_Da             : REAL := 0.012;   (* Chemical-to-residence time ratio (Da << 0.05) *)
    rQuenchCoolingRate_K_s          : REAL := 1.45E+05;(* Shock-chilling temperature gradient [K/s] *)
    rZincSaturationTemp_degC        : REAL := 907.0;   (* Normal boiling point of zinc metal at 1 atm *)
    rZincSaturationPress_bar        : REAL := 0.0;     (* Vapor pressure from Clausius-Clapeyron [bar] *)
    rZincSupersaturationRatio_S     : REAL := 1.0;     (* Supersaturation ratio S = P_Zn / P_sat *)
    rAerosolNucleationRate_cm3_s    : REAL := 0.0;     (* Homogeneous nucleation rate of submicron aerosol *)

    (* ========================================================================================= *)
    (* SECTION 7: FUSED QUARTZ WINDOW AERODYNAMIC VORTEX SWEEP & DEVITRIFICATION                 *)
    (* ========================================================================================= *)
    rQuartzSwirlNumber_Sw           : REAL := 0.92;    (* Aerodynamic vortex swirl number *)
    rParticleStokesNumber_Stk       : REAL := 0.0035;  (* Particle deflection Stokes number (Stk << 0.01) *)
    rWindowSweepBarrierEfficiency   : REAL := 0.985;   (* Aerodynamic boundary layer repelling efficiency *)
    rCristobaliteNucleationRate     : REAL := 0.0;     (* Devitrification phase transformation rate [1/s] *)
    rCristobaliteCumulativeIntegral : REAL := 0.0;     (* Total cumulative devitrification index [%] *)
    rQuartzRadialTempGradient_degC  : REAL := 0.0;     (* Center-to-rim temperature difference [deg C] *)
    rQuartzThermoMechanicalStress_MPa:REAL := 0.0;     (* Computed tensile thermal stress in quartz [MPa] *)

    (* ========================================================================================= *)
    (* SECTION 8: CERAMIC REFRACTORY MECHANICAL STRESS & THERMAL FATIGUE (SiC CAVITY)            *)
    (* ========================================================================================= *)
    rSiC_YoungsModulus_GPa          : REAL := 410.0;   (* Modulus of elasticity of SiC refractory [GPa] *)
    rSiC_ThermalExpansion_perK      : REAL := 4.5E-06; (* Thermal expansion coefficient [1/K] *)
    rSiC_PoissonsRatio              : REAL := 0.16;    (* Refractory Poisson ratio *)
    rSiC_ThermalConductivity_W_mK   : REAL := 45.0;    (* High-temperature thermal conductivity [W/m K] *)
    rCavityWallThickness_m          : REAL := 0.065;   (* Refractory cavity cylinder wall thickness [m] *)
    rCavityRadialTempDiff_degC      : REAL := 0.0;     (* Inner-to-outer refractory wall delta T [deg C] *)
    rCavityHoopStress_MPa           : REAL := 0.0;     (* Circumferential thermo-mechanical stress [MPa] *)
    rCavityVonMisesStress_MPa       : REAL := 0.0;     (* Equivalent von Mises stress in ceramic [MPa] *)
    rBiotNumber_Bi                  : REAL := 0.18;    (* Conductive-to-convective resistance ratio *)

    (* ========================================================================================= *)
    (* SECTION 9: HELIOSTAT AIMPOINT DISTRIBUTION & RADIANT HEAT BALANCING                      *)
    (* ========================================================================================= *)
    rAimpointAzimuthTrim_mrad       : REAL := 0.0;
    rAimpointElevationTrim_mrad     : REAL := 0.0;
    rCloudTransientDropRate_pct_s   : REAL := 0.0;
    rPrevSolarIrradiance_W_m2       : REAL := 0.0;
    rAttenuatorFeedforwardCmd_pct   : REAL := 0.0;

    (* ========================================================================================= *)
    (* SECTION 10: ACTUATOR SLEW RATE LIMITERS & FILTER ACCUMULATORS                             *)
    (* ========================================================================================= *)
    rAttenuatorPos_Actual_pct       : REAL := 0.0;
    rQuenchValve_Actual_pct         : REAL := 0.0;
    rWindowSweepValve_Actual_pct    : REAL := 0.0;
    rZnO_Feeder_Actual_pct          : REAL := 0.0;

    (* Maximum Actuator Slew Rates [% / s] *)
    rMaxSlew_Attenuator_pct_s       : REAL := 40.0;   (* High-speed water-cooled mechanical shutter *)
    rMaxSlew_QuenchValve_pct_s      : REAL := 50.0;   (* Fast pneumatic positioning valve *)
    rMaxSlew_WindowValve_pct_s      : REAL := 30.0;   (* Vortex purge flow modulating valve *)
    rMaxSlew_Feeder_pct_s           : REAL := 10.0;   (* Powder metering drive acceleration *)

    (* ========================================================================================= *)
    (* SECTION 11: ISA-18.2 ALARM & TRIP FIRST-OUT DIAGNOSTIC REGISTERS                         *)
    (* ========================================================================================= *)
    bTripLatched                    : BOOL := FALSE;
    bFirstOutRecorded               : BOOL := FALSE;
    tFirstOutTimestamp_s            : REAL := 0.0;
    rGlobalProcessRuntime_s         : REAL := 0.0;
END_VAR
"""

print("Declarations module ready.")
