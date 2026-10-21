# -*- coding: utf-8 -*-
"""
Exhaustive Builder for IEC 61131-3 Superfluid He-II Cryostat Synthetic Dataset Record.
"""

def generate_iec_st():
    parts = []
    
    # Header block
    parts.append("""FUNCTION_BLOCK FB_CryoHelium_SuperfluidHeII_LambdaTransition
(*
========================================================================================================================
CYBER-PHYSICAL SUPERFLUID HELIUM (He-II) SUB-LAMBDA TRANSITION CRYOSTAT CONTROLLER
========================================================================================================================
Architect: Principal Automation Fellow & Cyber-Physical Systems Chair
Target Hardware: Ultra-High-Reliability Safety PLC / PAC (IEC 61131-3 3rd Edition Compliant)
Domain: Cryogenic Liquid Helium (4.2 K to 1.8 K) Superfluid Transition Cryostat
Operational Focus:
  - Sub-Lambda Point (T_lambda = 2.1768 K, P_lambda = 50.418 mbar) Pressure-Temperature Equilibrium
  - Joule-Thomson Valve Sub-Millibar Backpressure Regulation & Flash Evaporation Optimization
  - Gorter-Mellink Superfluid Heat Flux Mutual Friction Transport Estimation & Quantum Vortex Dynamics
  - Thermomechanical London Fountain Effect Pressure Balancing across Porous Superleak Plugs
  - Triple Modular Redundancy (2oo3 TMR) Fault-Tolerant Voting Architecture with Graceful Degradation
  - Constrained Model Predictive Control (MPC) with 4x4 State-Space Model & Analytical Quadratic Optimization

THERMODYNAMIC & QUANTUM HYDRODYNAMIC FOUNDATION:
  1. Tisza-Landau Two-Fluid Hydrodynamic Model:
     Liquid Helium below the lambda transition behaves as an intimate mixture of two interpenetrating fluids:
       rho = rho_n(T) + rho_s(T)
     where normal fluid component rho_n possesses finite dynamic shear viscosity eta_n and carries the entire entropy s(T),
     whereas the superfluid component rho_s possesses identically zero viscosity (eta_s = 0), carries zero entropy (s_s = 0),
     and moves under the gradient of the chemical potential mu:
       d(v_s)/dt = - grad(mu) = - (1/rho) * grad(P) + s * grad(T)
     The temperature dependence of the superfluid density fraction is governed by:
       rho_s(T) / rho = 1.0 - (T / T_lambda)^5.6   [for 1.2 K <= T <= T_lambda]
       rho_n(T) / rho = (T / T_lambda)^5.6

  2. Lambda Transition Logarithmic Singularity:
     At the lambda temperature T_lambda = 2.1768 K, the specific heat C_p diverges logarithmically:
       C_p(T) = A_pm * ln|1.0 - T / T_lambda| + B_pm
     Crossing this boundary requires dynamic deceleration of the vacuum pumpdown derivative (dP/dt) to prevent violent
     cryogenic flash boiling, bubble collapse, and severe thermo-acoustic oscillations (Taconis oscillations).

  3. Gorter-Mellink Turbulent Mutual Friction & Quantum Vortex Dynamics:
     At heat fluxes exceeding the critical threshold q_c, relative counterflow velocity w = |v_n - v_s| generates
     a dense tangle of quantized vortex lines of Feynman-Onsager circulation quantum kappa = h / m_He = 9.97e-8 m2/s.
     The mutual friction force between superfluid vortices and normal fluid excitations (phonons/rotons) is:
       F_sn = A_GM * rho_s * rho_n * (v_n - v_s)^3
     The turbulent internal counterflow heat transport is governed by the non-linear Gorter-Mellink heat conductivity function:
       q = [ (1.0 / f(T)) * (dT / dx) ]^(1/3)   [W/cm2]
       f(T) = (A_GM * rho_n) / (rho_s^3 * s(T)^4 * T^3)
     Film boiling onset occurs when q exceeds the critical heat flux q_crit (approx 1.85 W/cm2 at 1.80 K).

  4. London Thermomechanical Fountain Effect:
     In a porous superleak plug with pore radius r_p << mean free path of excitations (typically r_p ~ 10-20 nm),
     the viscous normal fluid is immobilized (v_n = 0) by Poiseuille impedance, while frictionless superfluid flows
     freely. Under a temperature differential Delta_T, chemical potential equilibrium (Delta_mu = 0) establishes a hydrostatic
     fountain pressure differential:
       Delta_P_F = INTEGRAL_{T1}^{T2} [ rho * s(T) ] dT
     Active electric heating on the downstream side produces controllable cryogenic pumping pressure.

  5. Triple Modular Redundancy (2oo3 TMR) Architecture:
     Cryogenic sensors (calibrated Cernox CX-1050 RTDs and MKS Baratron capacitance manometers) are evaluated via
     pairwise variance, median selection, dynamic excitation I^2*R self-heating compensation, and automated degradation
     across operational modes: 2oo3 Normal -> 1oo2 Degraded -> Simplex Fallback -> Fail-Safe Quench Interlock.

  6. Discrete-Time State-Space Representation & Constrained MPC Formulation:
     x(k+1) = A * x(k) + B * u(k) + E * w(k)
     y(k)   = C * x(k) + D * u(k)
     where:
       x = [ delta_T_bath [K], delta_P_vapor [mbar], delta_L_level [mm], delta_m_boiloff [g/s] ]^T
       u = [ delta_u_JT [%], delta_u_Blower [rpm], delta_u_FountainHeater [W] ]^T
       w = [ q_SRF_pulsed [W], q_static_leak [W] ]^T
     The MPC optimizer computes unconstrained Newton step via full 3x3 Hessian inversion, followed by active-set
     actuator rate and saturation projection.
========================================================================================================================
*)
""")

    # VAR_INPUT
    parts.append("""VAR_INPUT
    (* =========================================================================
       PRIMARY PROCESS MEASUREMENT CHANNELS (WITH PHYSICAL UNITS)
       ========================================================================= *)
    rTempCernox_A_K             : REAL;     (* [K] Cryostat bath temperature sensor channel A - Cernox CX-1050 RTD *)
    rTempCernox_B_K             : REAL;     (* [K] Cryostat bath temperature sensor channel B - Cernox CX-1050 RTD *)
    rTempCernox_C_K             : REAL;     (* [K] Cryostat bath temperature sensor channel C - Cernox CX-1050 RTD *)
    rPressureBaratron_A_mbar    : REAL;     (* [mbar] Saturated vapor head pressure channel A - MKS Baratron 0-100 mbar *)
    rPressureBaratron_B_mbar    : REAL;     (* [mbar] Saturated vapor head pressure channel B - MKS Baratron 0-100 mbar *)
    rPressureBaratron_C_mbar    : REAL;     (* [mbar] Saturated vapor head pressure channel C - MKS Baratron 0-100 mbar *)
    rMassFlowPumpingLine_gps    : REAL;     (* [g/s] Cold vacuum pumping line Coriolis/thermal mass flow rate *)
    rHeatFluxDensitySRF_W_cm2   : REAL;     (* [W/cm2] Superconducting RF cavity transient surface heat flux density *)
    rPressureRampRate_mbar_s    : REAL;     (* [mbar/s] Commanded pumpdown backpressure rate limit setpoint *)
    rHeliumLiquidLevel_mm       : REAL;     (* [mm] Cryostat liquid helium-II bath level via superconducting NbTi wire probe *)
    rMagnetCurrent_A            : REAL;     (* [A] Superconducting magnet / SRF cavity quadrupole transport current *)
    rSensorExcitationVolt_V     : REAL;     (* [V] Precision AC resistance bridge sensor excitation drive voltage *)
    rJTSupplyPressure_mbar      : REAL;     (* [mbar] Liquid helium high-pressure feed line supply pressure upstream of JT valve *)
    rTargetTempSetpoint_K       : REAL;     (* [K] Supervisory target temperature setpoint (Nominal 1.800 K) *)

    (* =========================================================================
       SUPERVISORY CONTROL SIGNALS & SAFETY INTERLOCKS
       ========================================================================= *)
    bSystemEnable               : BOOL;     (* System master enable permissive signal *)
    bEmergencyStop              : BOOL;     (* SIL-3 Hardwired Cryogenic Emergency Dump / Cryo-Quench Interlock *)
    bResetAlarms                : BOOL;     (* Manual fault reset acknowledgment *)
    bAcknowledgeQuench          : BOOL;     (* Operator manual quench acknowledgment *)
    bManualModeSelect           : BOOL;     (* Manual maintenance bypass switch *)
    rManualJTPos_pct            : REAL;     (* [%] Manual JT valve position command 0.0 - 100.0% *)
    rManualBlowerRpm            : REAL;     (* [rpm] Manual vacuum blower speed command 0.0 - 6000.0 rpm *)
    rManualHeaterPwr_W          : REAL;     (* [W] Manual fountain heater power command 0.0 - 35.0 W *)
END_VAR
""")

    # VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* =========================================================================
       ACTUATOR COMMAND OUTPUTS (WITH ENGINEERING UNITS)
       ========================================================================= *)
    rJTOpeningPercent                   : REAL;     (* [%] Joule-Thomson expansion throttling valve position command 0.0 - 100.0% *)
    rVacuumPumpingSpeedCmd_rpm          : REAL;     (* [rpm] Cold roots vacuum blower pump VFD rotational frequency speed command *)
    rFountainPumpHeaterPwr_W            : REAL;     (* [W] Thermomechanical fountain effect superleak heater drive power command *)

    (* =========================================================================
       CALCULATED CRYOGENIC DIAGNOSTICS & QUANTUM HYDRODYNAMIC METRICS
       ========================================================================= *)
    rGorterMellinkHeatConductance_W_K   : REAL;     (* [W/K] Instantaneous Gorter-Mellink mutual friction effective thermal conductance *)
    rHeII_SuperfluidFraction_pct        : REAL;     (* [%] Calculated superfluid density fraction (rho_s / rho * 100.0) *)
    rFountainPressureDiff_mbar          : REAL;     (* [mbar] London thermomechanical fountain pressure differential across superleak plug *)
    rEvaporationBoiloffRate_gps         : REAL;     (* [g/s] Calculated latent heat equilibrium evaporation rate *)
    rVotedBathTemp_K                    : REAL;     (* [K] 2oo3 TMR voted cryostat bath temperature *)
    rVotedHeadPressure_mbar             : REAL;     (* [mbar] 2oo3 TMR voted cryostat vapor pressure *)
    rObservedThermalConductivity_W_mK   : REAL;     (* [W/m.K] Apparent He-II bulk thermal conductivity *)
    rSatPressureEquilibriumErr_mbar     : REAL;     (* [mbar] Deviation between voted pressure and theoretical ITS-90 saturation pressure *)
    rCriticalHeatFluxMargin_pct         : REAL;     (* [%] Operating heat flux margin relative to Gorter-Mellink peak flux q_crit *)
    rVortexLineDensity_m2               : REAL;     (* [m^-2] Estimated Feynman quantum vortex line tangle density in He-II bath *)
    rLondonFountainMassFlow_gps         : REAL;     (* [g/s] Superfluid mass flow induced by thermomechanical fountain pressure *)

    (* =========================================================================
       SUPERVISORY STATUS WORDS & SAFETY BITMASKS
       ========================================================================= *)
    wCryostatStatusWord                 : WORD;     (* Cryostat operational state & supervisory machine bitmask *)
    wAlarmVectorHigh                    : DWORD;    (* High-priority critical safety alarm bitmask word *)
    wAlarmVectorLow                     : DWORD;    (* Low-priority advisory and maintenance alarm bitmask word *)
    bSuperfluidRegimeActive             : BOOL;     (* True when T < T_lambda and pressure is within sub-lambda saturation envelope *)
    bLambdaTransitionComplete           : BOOL;     (* Latent/specific heat peak anomaly safely crossed and verified *)
    bThermalRunawayQuenchRisk           : BOOL;     (* Critical heat flux threshold exceeded in Gorter-Mellink regime *)
    bCryostatSafetyInterlockTripped     : BOOL;     (* Hardwired or soft safety interlock trip status *)
    bTaconisOscillationDetected         : BOOL;     (* Thermo-acoustic pressure resonance detected in cryogenic sense line *)
END_VAR
""")

    # VAR
    parts.append("""VAR
    (* =========================================================================
       PHYSICAL & THERMODYNAMIC HELIUM-4 CONSTANTS
       ========================================================================= *)
    c_T_lambda                          : REAL := 2.1768;       (* [K] Lambda transition critical temperature *)
    c_P_lambda                          : REAL := 50.418;       (* [mbar] Saturated vapor pressure at lambda point *)
    c_T_nominal_superfluid              : REAL := 1.8000;       (* [K] Target deep superfluid operating temperature *)
    c_P_nominal_superfluid              : REAL := 16.380;       (* [mbar] ITS-90 saturated vapor pressure at 1.800 K *)
    c_Density_HeI                       : REAL := 0.1250;       (* [g/cm3] Normal liquid helium density at 4.2 K *)
    c_Density_HeII                      : REAL := 0.1455;       (* [g/cm3] Superfluid liquid helium density at 1.8 K *)
    c_LatentHeat_4K2                    : REAL := 20.72;        (* [J/g] Latent heat of vaporization at 4.22 K *)
    c_LatentHeat_1K8                    : REAL := 23.45;        (* [J/g] Latent heat of vaporization at 1.80 K *)
    c_LatentHeat_Lambda                 : REAL := 22.38;        (* [J/g] Latent heat of vaporization at T_lambda *)
    c_QuantumCirculation_kappa          : REAL := 9.97E-8;      (* [m2/s] Feynman-Onsager quantum circulation unit h/m_He *)
    c_A_GM_FrictionConst                : REAL := 85.0;         (* [m.s/kg] Gorter-Mellink mutual friction coefficient *)
    c_SuperleakPoreDiameter_nm          : REAL := 15.0;         (* [nm] Vycor porous glass superleak average pore diameter *)
    c_SuperleakFlowArea_cm2             : REAL := 12.56;        (* [cm2] Cross-sectional surface area of porous superleak plug *)
    c_SuperleakLength_cm                : REAL := 4.50;         (* [cm] Physical length of superleak plug *)
    c_SampleTime_s                      : REAL := 0.050;        (* [s] Controller loop sample period (20 Hz cycle) *)
    c_MaxBlowerRpm                      : REAL := 6000.0;       (* [rpm] Maximum rotational speed of cold Roots blower *)
    c_MinBlowerRpm                      : REAL := 300.0;        (* [rpm] Minimum idling speed of cold Roots blower *)
    c_MaxJTValveOpening_pct             : REAL := 100.0;        (* [%] Maximum mechanical valve stroke position *)
    c_MinJTValveOpening_pct             : REAL := 0.0;          (* [%] Fully seated shutoff position *)
    c_MaxFountainHeaterPwr_W            : REAL := 35.0;         (* [W] Maximum electrical heating power to fountain driver *)
    c_CriticalHeatFlux_1K8_W_cm2        : REAL := 1.85;         (* [W/cm2] Critical Gorter-Mellink heat flux at 1.80 K *)
    c_VortexCoreRadius_a0_nm            : REAL := 0.147;        (* [nm] Effective quantum vortex core radius *)

    (* =========================================================================
       TRIPLE MODULAR REDUNDANCY (2oo3) VOTING SYSTEM VARIABLES
       ========================================================================= *)
    bSensorValid_T_A                    : BOOL := TRUE;
    bSensorValid_T_B                    : BOOL := TRUE;
    bSensorValid_T_C                    : BOOL := TRUE;
    bSensorValid_P_A                    : BOOL := TRUE;
    bSensorValid_P_B                    : BOOL := TRUE;
    bSensorValid_P_C                    : BOOL := TRUE;
    
    rDelta_T_AB                         : REAL := 0.0;
    rDelta_T_BC                         : REAL := 0.0;
    rDelta_T_CA                         : REAL := 0.0;
    rDelta_P_AB                         : REAL := 0.0;
    rDelta_P_BC                         : REAL := 0.0;
    rDelta_P_CA                         : REAL := 0.0;

    rMaxAllowedDev_T_K                  : REAL := 0.025;        (* [K] Max allowable temperature inter-sensor deviation *)
    rMaxAllowedDev_P_mbar               : REAL := 0.350;        (* [mbar] Max allowable pressure inter-sensor deviation *)
    
    iHealthCount_T_A                    : INT := 100;
    iHealthCount_T_B                    : INT := 100;
    iHealthCount_T_C                    : INT := 100;
    iHealthCount_P_A                    : INT := 100;
    iHealthCount_P_B                    : INT := 100;
    iHealthCount_P_C                    : INT := 100;

    iTMRMode_Temp                       : INT := 3;             (* 3 = 2oo3 Normal, 2 = 1oo2 Degraded, 1 = Simplex, 0 = Fail *)
    iTMRMode_Press                      : INT := 3;             (* 3 = 2oo3 Normal, 2 = 1oo2 Degraded, 1 = Simplex, 0 = Fail *)

    rSelfHeatingCorr_T_A_K              : REAL := 0.0;          (* Dynamic I^2 * R self-heating bias correction *)
    rSelfHeatingCorr_T_B_K              : REAL := 0.0;
    rSelfHeatingCorr_T_C_K              : REAL := 0.0;

    (* =========================================================================
       DISCRETE-TIME 4x4 STATE-SPACE MODEL MATRICES & VECTORS
       Operating Point: T = 1.800 K, P = 16.38 mbar, Level = 650 mm, m_dot = 2.4 g/s
       Sampling Time Ts = 0.050 s
       ========================================================================= *)
    (* State Vector: x = [ delta_T [K], delta_P [mbar], delta_Level [mm], delta_MassFlow [g/s] ]^T *)
    aMatrix_A                           : ARRAY[1..4, 1..4] OF REAL := [
        0.9852,  0.0145, -0.0003, -0.0284,
        0.0421,  0.9610, -0.0012, -0.0892,
        0.0001,  0.0008,  0.9992, -0.0125,
        0.0182,  0.0845, -0.0001,  0.9230
    ];

    (* Control Input Matrix: u = [ delta_u_JT [%], delta_u_Blower [rpm], delta_u_FountainHeater [W] ]^T *)
    aMatrix_B                           : ARRAY[1..4, 1..3] OF REAL := [
       -0.0042, -0.000082,  0.0124,
       -0.0156, -0.000450,  0.0482,
        0.0820, -0.000015, -0.0035,
        0.0210,  0.000320,  0.0650
    ];

    (* Output Matrix: y = C * x + D * u *)
    aMatrix_C                           : ARRAY[1..4, 1..4] OF REAL := [
        1.0, 0.0, 0.0, 0.0,
        0.0, 1.0, 0.0, 0.0,
        0.0, 0.0, 1.0, 0.0,
        0.0, 0.0, 0.0, 1.0
    ];

    (* Direct Feedthrough Matrix *)
    aMatrix_D                           : ARRAY[1..4, 1..3] OF REAL := [
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0,
        0.0, 0.0, 0.0
    ];

    (* Disturbance Coupling Matrix: w = [ q_SRF_pulsed [W], q_static_leak [W] ]^T *)
    aMatrix_E                           : ARRAY[1..4, 1..2] OF REAL := [
        0.0085,  0.0042,
        0.0321,  0.0150,
       -0.0018, -0.0009,
        0.0440,  0.0215
    ];

    aState_x                            : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];
    aState_x_pred                       : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];
    aState_x_ref                        : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];
    aControl_u                          : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    aControl_u_prev                     : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    aDisturbance_w                      : ARRAY[1..2] OF REAL := [0.0, 0.0];
    aState_error                        : ARRAY[1..4] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* =========================================================================
       MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION VARIABLES
       ========================================================================= *)
    aWeight_Q                           : ARRAY[1..4] OF REAL := [250.0, 45.0, 1.2, 5.0]; (* State error penalties *)
    aWeight_R                           : ARRAY[1..3] OF REAL := [0.85, 0.00045, 1.8];    (* Control effort penalties *)
    aWeight_R_rate                      : ARRAY[1..3] OF REAL := [5.2, 0.0028, 8.5];      (* Control slew rate penalties *)
    
    aHessian_H                          : ARRAY[1..3, 1..3] OF REAL;
    aHessian_inv                        : ARRAY[1..3, 1..3] OF REAL;
    rDetHessian                         : REAL := 1.0;
    aGradient_g                         : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    aDelta_u_opt                        : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    aDelta_u_unconstrained              : ARRAY[1..3] OF REAL := [0.0, 0.0, 0.0];
    
    rSlewLimit_JT_pct_s                 : REAL := 5.0;          (* [%/s] Maximum JT valve movement velocity *)
    rSlewLimit_Blower_rpm_s             : REAL := 150.0;        (* [rpm/s] Maximum Blower VFD ramp rate *)
    rSlewLimit_Heater_W_s               : REAL := 10.0;         (* [W/s] Maximum fountain heater power ramp rate *)

    rTargetBathLevel_mm                 : REAL := 650.0;        (* [mm] Target nominal liquid helium level *)
    rTargetMassFlow_gps                 : REAL := 2.45;         (* [g/s] Base equilibrium evaporation pumping rate *)

    (* =========================================================================
       SUPERVISORY FINITE STATE MACHINE (SFSM) MANAGEMENT
       ========================================================================= *)
    iOperatingState                     : INT := 0;
    iPreviousState                      : INT := -1;
    tStateTimer                         : TON;
    tLambdaCrossingTimer                : TON;
    tSensorDisagreementTimer            : TON;
    tQuenchReliefTimer                  : TON;
    tPulseHeatHoldTimer                 : TON;
    tTaconisFilterTimer                 : TON;
    
    rStateTimeSeconds                   : REAL := 0.0;
    bTransitionTrigger                  : BOOL := FALSE;
    bStateFirstScan                     : BOOL := TRUE;

    (* =========================================================================
       FILTERING, DIFFERENTIATORS & OBSERVERS
       ========================================================================= *)
    rFiltTemp_K                         : REAL := 4.200;
    rFiltPressure_mbar                  : REAL := 1013.25;
    rFiltMassFlow_gps                   : REAL := 0.0;
    rFiltLevel_mm                       : REAL := 0.0;
    
    rPrevTemp_K                         : REAL := 4.200;
    rPrevPressure_mbar                  : REAL := 1013.25;
    
    rDerivativeTemp_K_s                 : REAL := 0.0;
    rDerivativePressure_mbar_s          : REAL := 0.0;

    rFilterAlpha_Fast                   : REAL := 0.25;
    rFilterAlpha_Slow                   : REAL := 0.05;

    (* Taconis Thermo-Acoustic Oscillation Detection Ring Accumulator *)
    aPressBuffer                        : ARRAY[1..16] OF REAL;
    iPressBufIdx                        : INT := 1;
    rPressAcousticMean                  : REAL := 0.0;
    rPressAcousticVariance              : REAL := 0.0;
    rPressAcousticRMS                   : REAL := 0.0;
    rTaconisAcousticThreshold_mbar      : REAL := 0.280;

    (* =========================================================================
       GORTER-MELLINK & LONDON THERMOMECHANICAL INTERMEDIATES
       ========================================================================= *)
    rEntropy_s_J_gK                     : REAL := 0.0;
    rSuperfluidDensity_g_cm3            : REAL := 0.0;
    rNormalFluidDensity_g_cm3           : REAL := 0.0;
    rGorterMellink_f_inv                : REAL := 0.0;
    rHeatFlux_q_calc                    : REAL := 0.0;
    rFountainTempDifference_K           : REAL := 0.0;
    rBathVolume_Liters                  : REAL := 180.0;
    rVortexCirculationThreshold         : REAL := 0.0;
    rCounterflowVelocity_cm_s           : REAL := 0.0;

    (* Gauss-Simpson Numerical Quadrature Integration Nodes for London Integral *)
    aQuadNodeTemp                       : ARRAY[1..5] OF REAL;
    aQuadNodeEntropy                    : ARRAY[1..5] OF REAL;
    aQuadNodeDensity                    : ARRAY[1..5] OF REAL;
    rQuadIntegralAcc                    : REAL := 0.0;

    (* Loop Index Counters *)
    iRow                                : INT := 1;
    iCol                                : INT := 1;
    iIter                               : INT := 1;
    iNode                               : INT := 1;
END_VAR
""")

    # SECTION 1: Interlocks & Preprocessing
    parts.append("""
(*
========================================================================================================================
SECTION 1: HARDWIRED SAFETY INTERLOCKS & PRIMARY STATUS PRE-PROCESSING
========================================================================================================================
The Cryostat Safety Matrix coordinates SIL-3 hardwired cryogenic dump valves, vacuum rupture discs,
and superconducting magnet/cavity fast energy extraction systems.
*)
IF NOT bEmergencyStop OR NOT bSystemEnable THEN
    // Immediate de-energization to intrinsically safe shutdown configuration
    rJTOpeningPercent                   := 0.0;
    rVacuumPumpingSpeedCmd_rpm          := 0.0;
    rFountainPumpHeaterPwr_W            := 0.0;
    bSuperfluidRegimeActive             := FALSE;
    bLambdaTransitionComplete           := FALSE;
    bThermalRunawayQuenchRisk           := FALSE;
    bCryostatSafetyInterlockTripped     := TRUE;
    
    // Set status word to Safety Trip State (Bit 0)
    wCryostatStatusWord                 := 16#0001;
    wAlarmVectorHigh                    := wAlarmVectorHigh OR 16#00000001; // Bit 0: Emergency Stop Tripped
    
    iOperatingState                     := 99; // Transition directly to Cryogenic Quench / Safe Shutdown
    RETURN;
ELSE
    bCryostatSafetyInterlockTripped     := FALSE;
    wAlarmVectorHigh                    := wAlarmVectorHigh AND NOT 16#00000001;
END_IF;

// Manual alarm acknowledgment and latch reset handling
IF bResetAlarms THEN
    wAlarmVectorHigh                    := 16#00000000;
    wAlarmVectorLow                     := 16#00000000;
END_IF;
""")

    # SECTION 2: 2oo3 TMR Voting
    parts.append("""
(*
========================================================================================================================
SECTION 2: TRIPLE MODULAR REDUNDANCY (2oo3) VOTING FOR TEMPERATURE & PRESSURE
========================================================================================================================
Dynamic Excitation Joule Self-Heating Correction:
  At sub-lambda temperatures (T < 2.1768 K), even microwatt electrical power dissipated in the Cernox RTD
  generates a thermal gradient across the Kapitza boundary resistance R_K:
    Delta_T_self_heating = (V_exc^2 / R_sensor) / (h_Kapitza * A_contact)
  Here calibrated: R_sensor ~ 3500 Ohm at 1.8 K, effective conductance alpha ~ 0.015 W/K.
*)
IF rSensorExcitationVolt_V > 0.0001 THEN
    rSelfHeatingCorr_T_A_K := (rSensorExcitationVolt_V * rSensorExcitationVolt_V / 3500.0) / 0.015;
    rSelfHeatingCorr_T_B_K := (rSensorExcitationVolt_V * rSensorExcitationVolt_V / 3500.0) / 0.015;
    rSelfHeatingCorr_T_C_K := (rSensorExcitationVolt_V * rSensorExcitationVolt_V / 3500.0) / 0.015;
ELSE
    rSelfHeatingCorr_T_A_K := 0.0;
    rSelfHeatingCorr_T_B_K := 0.0;
    rSelfHeatingCorr_T_C_K := 0.0;
END_IF;

// Physical Bounds and Plausibility Validation for Cernox RTDs [1.0 K to 320.0 K]
bSensorValid_T_A := (rTempCernox_A_K >= 1.0) AND (rTempCernox_A_K <= 320.0);
bSensorValid_T_B := (rTempCernox_B_K >= 1.0) AND (rTempCernox_B_K <= 320.0);
bSensorValid_T_C := (rTempCernox_C_K >= 1.0) AND (rTempCernox_C_K <= 320.0);

// Physical Bounds and Plausibility Validation for Baratrons [0.01 mbar to 1200.0 mbar]
bSensorValid_P_A := (rPressureBaratron_A_mbar >= 0.01) AND (rPressureBaratron_A_mbar <= 1200.0);
bSensorValid_P_B := (rPressureBaratron_B_mbar >= 0.01) AND (rPressureBaratron_B_mbar <= 1200.0);
bSensorValid_P_C := (rPressureBaratron_C_mbar >= 0.01) AND (rPressureBaratron_C_mbar <= 1200.0);

// Pairwise Difference Evaluation for Discrepancy Diagnostics
rDelta_T_AB := ABS((rTempCernox_A_K - rSelfHeatingCorr_T_A_K) - (rTempCernox_B_K - rSelfHeatingCorr_T_B_K));
rDelta_T_BC := ABS((rTempCernox_B_K - rSelfHeatingCorr_T_B_K) - (rTempCernox_C_K - rSelfHeatingCorr_T_C_K));
rDelta_T_CA := ABS((rTempCernox_C_K - rSelfHeatingCorr_T_C_K) - (rTempCernox_A_K - rSelfHeatingCorr_T_A_K));

rDelta_P_AB := ABS(rPressureBaratron_A_mbar - rPressureBaratron_B_mbar);
rDelta_P_BC := ABS(rPressureBaratron_B_mbar - rPressureBaratron_C_mbar);
rDelta_P_CA := ABS(rPressureBaratron_C_mbar - rPressureBaratron_A_mbar);

// Temperature 2oo3 TMR Voting Algorithm & Graceful Degradation Logic
IF bSensorValid_T_A AND bSensorValid_T_B AND bSensorValid_T_C THEN
    iTMRMode_Temp := 3; // Fully Redundant 2oo3 Operation
    
    // Check if channel A drifted outside allowable envelope
    IF (rDelta_T_AB > rMaxAllowedDev_T_K) AND (rDelta_T_CA > rMaxAllowedDev_T_K) THEN
        rVotedBathTemp_K := ((rTempCernox_B_K - rSelfHeatingCorr_T_B_K) + (rTempCernox_C_K - rSelfHeatingCorr_T_C_K)) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000002; // Bit 1: Cernox Channel A Deviation
        IF iHealthCount_T_A > 0 THEN iHealthCount_T_A := iHealthCount_T_A - 1; END_IF;
    ELSIF (rDelta_T_AB > rMaxAllowedDev_T_K) AND (rDelta_T_BC > rMaxAllowedDev_T_K) THEN
        rVotedBathTemp_K := ((rTempCernox_A_K - rSelfHeatingCorr_T_A_K) + (rTempCernox_C_K - rSelfHeatingCorr_T_C_K)) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000004; // Bit 2: Cernox Channel B Deviation
        IF iHealthCount_T_B > 0 THEN iHealthCount_T_B := iHealthCount_T_B - 1; END_IF;
    ELSIF (rDelta_T_BC > rMaxAllowedDev_T_K) AND (rDelta_T_CA > rMaxAllowedDev_T_K) THEN
        rVotedBathTemp_K := ((rTempCernox_A_K - rSelfHeatingCorr_T_A_K) + (rTempCernox_B_K - rSelfHeatingCorr_T_B_K)) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000008; // Bit 3: Cernox Channel C Deviation
        IF iHealthCount_T_C > 0 THEN iHealthCount_T_C := iHealthCount_T_C - 1; END_IF;
    ELSE
        // Healthy 2oo3 Triplet: Select Median Sensor
        IF ((rTempCernox_A_K >= rTempCernox_B_K) AND (rTempCernox_A_K <= rTempCernox_C_K)) OR 
           ((rTempCernox_A_K <= rTempCernox_B_K) AND (rTempCernox_A_K >= rTempCernox_C_K)) THEN
            rVotedBathTemp_K := rTempCernox_A_K - rSelfHeatingCorr_T_A_K;
        ELSIF ((rTempCernox_B_K >= rTempCernox_A_K) AND (rTempCernox_B_K <= rTempCernox_C_K)) OR 
              ((rTempCernox_B_K <= rTempCernox_A_K) AND (rTempCernox_B_K >= rTempCernox_C_K)) THEN
            rVotedBathTemp_K := rTempCernox_B_K - rSelfHeatingCorr_T_B_K;
        ELSE
            rVotedBathTemp_K := rTempCernox_C_K - rSelfHeatingCorr_T_C_K;
        END_IF;
    END_IF;

ELSIF bSensorValid_T_A AND bSensorValid_T_B THEN
    iTMRMode_Temp := 2; // Degraded 1oo2 Mode (A + B)
    rVotedBathTemp_K := ((rTempCernox_A_K - rSelfHeatingCorr_T_A_K) + (rTempCernox_B_K - rSelfHeatingCorr_T_B_K)) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000010; // Bit 4: Temp TMR Degraded to 1oo2
ELSIF bSensorValid_T_B AND bSensorValid_T_C THEN
    iTMRMode_Temp := 2; // Degraded 1oo2 Mode (B + C)
    rVotedBathTemp_K := ((rTempCernox_B_K - rSelfHeatingCorr_T_B_K) + (rTempCernox_C_K - rSelfHeatingCorr_T_C_K)) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000010;
ELSIF bSensorValid_T_A AND bSensorValid_T_C THEN
    iTMRMode_Temp := 2; // Degraded 1oo2 Mode (A + C)
    rVotedBathTemp_K := ((rTempCernox_A_K - rSelfHeatingCorr_T_A_K) + (rTempCernox_C_K - rSelfHeatingCorr_T_C_K)) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000010;
ELSIF bSensorValid_T_A THEN
    iTMRMode_Temp := 1; // Simplex Fallback Mode (Channel A Only)
    rVotedBathTemp_K := rTempCernox_A_K - rSelfHeatingCorr_T_A_K;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00000020; // Bit 5: Critical Temp Redundancy Lost
ELSIF bSensorValid_T_B THEN
    iTMRMode_Temp := 1; // Simplex Fallback Mode (Channel B Only)
    rVotedBathTemp_K := rTempCernox_B_K - rSelfHeatingCorr_T_B_K;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00000020;
ELSIF bSensorValid_T_C THEN
    iTMRMode_Temp := 1; // Simplex Fallback Mode (Channel C Only)
    rVotedBathTemp_K := rTempCernox_C_K - rSelfHeatingCorr_T_C_K;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00000020;
ELSE
    iTMRMode_Temp := 0; // Total Sensor Failure
    rVotedBathTemp_K := 4.200; // Fail-Safe Conservative Substitution
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00000040; // Bit 6: Total Temp Sensor Failure
END_IF;

// Pressure 2oo3 TMR Voting Algorithm & Graceful Degradation Logic
IF bSensorValid_P_A AND bSensorValid_P_B AND bSensorValid_P_C THEN
    iTMRMode_Press := 3; // Fully Redundant 2oo3 Operation
    
    IF (rDelta_P_AB > rMaxAllowedDev_P_mbar) AND (rDelta_P_CA > rMaxAllowedDev_P_mbar) THEN
        rVotedHeadPressure_mbar := (rPressureBaratron_B_mbar + rPressureBaratron_C_mbar) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000100; // Bit 8: Baratron Channel A Fault
        IF iHealthCount_P_A > 0 THEN iHealthCount_P_A := iHealthCount_P_A - 1; END_IF;
    ELSIF (rDelta_P_AB > rMaxAllowedDev_P_mbar) AND (rDelta_P_BC > rMaxAllowedDev_P_mbar) THEN
        rVotedHeadPressure_mbar := (rPressureBaratron_A_mbar + rPressureBaratron_C_mbar) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000200; // Bit 9: Baratron Channel B Fault
        IF iHealthCount_P_B > 0 THEN iHealthCount_P_B := iHealthCount_P_B - 1; END_IF;
    ELSIF (rDelta_P_BC > rMaxAllowedDev_P_mbar) AND (rDelta_P_CA > rMaxAllowedDev_P_mbar) THEN
        rVotedHeadPressure_mbar := (rPressureBaratron_A_mbar + rPressureBaratron_B_mbar) * 0.5;
        wAlarmVectorLow := wAlarmVectorLow OR 16#00000400; // Bit 10: Baratron Channel C Fault
        IF iHealthCount_P_C > 0 THEN iHealthCount_P_C := iHealthCount_P_C - 1; END_IF;
    ELSE
        // Healthy Median Selection
        IF ((rPressureBaratron_A_mbar >= rPressureBaratron_B_mbar) AND (rPressureBaratron_A_mbar <= rPressureBaratron_C_mbar)) OR 
           ((rPressureBaratron_A_mbar <= rPressureBaratron_B_mbar) AND (rPressureBaratron_A_mbar >= rPressureBaratron_C_mbar)) THEN
            rVotedHeadPressure_mbar := rPressureBaratron_A_mbar;
        ELSIF ((rPressureBaratron_B_mbar >= rPressureBaratron_A_mbar) AND (rPressureBaratron_B_mbar <= rPressureBaratron_C_mbar)) OR 
              ((rPressureBaratron_B_mbar <= rPressureBaratron_A_mbar) AND (rPressureBaratron_B_mbar >= rPressureBaratron_C_mbar)) THEN
            rVotedHeadPressure_mbar := rPressureBaratron_B_mbar;
        ELSE
            rVotedHeadPressure_mbar := rPressureBaratron_C_mbar;
        END_IF;
    END_IF;

ELSIF bSensorValid_P_A AND bSensorValid_P_B THEN
    iTMRMode_Press := 2; // Degraded 1oo2 Mode (A + B)
    rVotedHeadPressure_mbar := (rPressureBaratron_A_mbar + rPressureBaratron_B_mbar) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000800; // Bit 11: Pressure TMR Degraded
ELSIF bSensorValid_P_B AND bSensorValid_P_C THEN
    iTMRMode_Press := 2; // Degraded 1oo2 Mode (B + C)
    rVotedHeadPressure_mbar := (rPressureBaratron_B_mbar + rPressureBaratron_C_mbar) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000800;
ELSIF bSensorValid_P_A AND bSensorValid_P_C THEN
    iTMRMode_Press := 2; // Degraded 1oo2 Mode (A + C)
    rVotedHeadPressure_mbar := (rPressureBaratron_A_mbar + rPressureBaratron_C_mbar) * 0.5;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00000800;
ELSIF bSensorValid_P_A THEN
    iTMRMode_Press := 1; // Simplex Fallback Mode (Channel A Only)
    rVotedHeadPressure_mbar := rPressureBaratron_A_mbar;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00001000; // Bit 12: Critical Pressure Redundancy Lost
ELSIF bSensorValid_P_B THEN
    iTMRMode_Press := 1; // Simplex Fallback Mode (Channel B Only)
    rVotedHeadPressure_mbar := rPressureBaratron_B_mbar;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00001000;
ELSIF bSensorValid_P_C THEN
    iTMRMode_Press := 1; // Simplex Fallback Mode (Channel C Only)
    rVotedHeadPressure_mbar := rPressureBaratron_C_mbar;
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00001000;
ELSE
    iTMRMode_Press := 0; // Total Pressure Sensor Failure
    rVotedHeadPressure_mbar := 1013.25; // Atmospheric Conservative Default
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00002000; // Bit 13: Total Pressure Sensor Failure
END_IF;

// Primary Signal Conditioning: Exponential Moving Average Filters & Numerical Derivatives
rFiltTemp_K := (rFilterAlpha_Fast * rVotedBathTemp_K) + ((1.0 - rFilterAlpha_Fast) * rFiltTemp_K);
rFiltPressure_mbar := (rFilterAlpha_Fast * rVotedHeadPressure_mbar) + ((1.0 - rFilterAlpha_Fast) * rFiltPressure_mbar);
rFiltMassFlow_gps := (rFilterAlpha_Slow * rMassFlowPumpingLine_gps) + ((1.0 - rFilterAlpha_Slow) * rFiltMassFlow_gps);
rFiltLevel_mm := (rFilterAlpha_Slow * rHeliumLiquidLevel_mm) + ((1.0 - rFilterAlpha_Slow) * rFiltLevel_mm);

rDerivativeTemp_K_s := (rFiltTemp_K - rPrevTemp_K) / c_SampleTime_s;
rDerivativePressure_mbar_s := (rFiltPressure_mbar - rPrevPressure_mbar) / c_SampleTime_s;

rPrevTemp_K := rFiltTemp_K;
rPrevPressure_mbar := rFiltPressure_mbar;

// Taconis Thermo-Acoustic Oscillation Detection in Cryogenic Sensing Taps
// Circular buffer statistical variance evaluation across last 16 cycles (0.80 s window)
aPressBuffer[iPressBufIdx] := rVotedHeadPressure_mbar;
iPressBufIdx := iPressBufIdx + 1;
IF iPressBufIdx > 16 THEN iPressBufIdx := 1; END_IF;

rPressAcousticMean := 0.0;
FOR iNode := 1 TO 16 DO
    rPressAcousticMean := rPressAcousticMean + aPressBuffer[iNode];
END_FOR;
rPressAcousticMean := rPressAcousticMean * 0.0625; // Divide by 16

rPressAcousticVariance := 0.0;
FOR iNode := 1 TO 16 DO
    rPressAcousticVariance := rPressAcousticVariance + ((aPressBuffer[iNode] - rPressAcousticMean) * (aPressBuffer[iNode] - rPressAcousticMean));
END_FOR;
rPressAcousticRMS := SQRT(rPressAcousticVariance * 0.0625);

IF rPressAcousticRMS > rTaconisAcousticThreshold_mbar THEN
    bTaconisOscillationDetected := TRUE;
    wAlarmVectorLow := wAlarmVectorLow OR 16#00040000; // Bit 18: Taconis Oscillation Detected
ELSE
    bTaconisOscillationDetected := FALSE;
    wAlarmVectorLow := wAlarmVectorLow AND NOT 16#00040000;
END_IF;
""")

    # SECTION 3: Thermodynamic Engine & Superfluid Mechanics
    parts.append("""
(*
========================================================================================================================
SECTION 3: THERMODYNAMIC He-4 PROPERTY ENGINE & SUPERFLUID QUANTUM HYDRODYNAMICS
========================================================================================================================
ITS-90 He-4 Saturated Vapor Pressure Equation & Landau Two-Fluid Partitioning:
  Below T_lambda = 2.1768 K, normal fluid density decreases precipitously as T^5.6, leaving nearly 100% superfluid
  at T = 1.0 K.
*)
VAR_TEMP
    rTheoryP_sat            : REAL;
    rTempRatio              : REAL;
    rTempRatio5_6           : REAL;
    rDeltaT_node            : REAL;
    rNodeT                  : REAL;
    rNodeRatio              : REAL;
    rNodeRatio5_6           : REAL;
    rNodeEntropy            : REAL;
    rNodeDensity            : REAL;
END_VAR

IF rFiltTemp_K > 0.5 THEN
    // Sub-lambda saturation pressure calculation (ITS-90 polynomial fit)
    // Range 1.25 K <= T <= 2.1768 K:
    IF rFiltTemp_K <= c_T_lambda THEN
        // He-II cubic Taylor expansion around T = 1.800 K (P_sat = 16.380 mbar)
        rTheoryP_sat := 16.380 * (1.0 + 3.120 * (rFiltTemp_K - 1.800) + 
                                  3.850 * (rFiltTemp_K - 1.800) * (rFiltTemp_K - 1.800) + 
                                  2.100 * (rFiltTemp_K - 1.800) * (rFiltTemp_K - 1.800) * (rFiltTemp_K - 1.800));
    ELSE
        // Normal fluid He-I region expansion around T_lambda = 2.1768 K (P_sat = 50.418 mbar)
        rTheoryP_sat := 50.418 * (1.0 + 2.850 * (rFiltTemp_K - c_T_lambda) + 
                                  1.950 * (rFiltTemp_K - c_T_lambda) * (rFiltTemp_K - c_T_lambda) + 
                                  0.420 * (rFiltTemp_K - c_T_lambda) * (rFiltTemp_K - c_T_lambda) * (rFiltTemp_K - c_T_lambda));
    END_IF;
    
    rSatPressureEquilibriumErr_mbar := rFiltPressure_mbar - rTheoryP_sat;
ELSE
    rTheoryP_sat := 16.380;
    rSatPressureEquilibriumErr_mbar := 0.0;
END_IF;

// Tisza-Landau Two-Fluid Hydrodynamic Model Calculations (for T < T_lambda)
IF rFiltTemp_K < c_T_lambda THEN
    bSuperfluidRegimeActive := TRUE;
    rTempRatio := rFiltTemp_K / c_T_lambda;
    
    // (T / T_lambda)^5.6 evaluation via power decomposition: x^5.6 = x^5 * (0.4 + 0.6 * x)
    rTempRatio5_6 := (rTempRatio * rTempRatio * rTempRatio * rTempRatio * rTempRatio) * (0.4 + 0.6 * rTempRatio);
    IF rTempRatio5_6 > 1.0 THEN
        rTempRatio5_6 := 1.0;
    END_IF;
    
    // Superfluid and Normal fluid fractions and densities
    rHeII_SuperfluidFraction_pct := (1.0 - rTempRatio5_6) * 100.0;
    rSuperfluidDensity_g_cm3     := c_Density_HeII * (1.0 - rTempRatio5_6);
    rNormalFluidDensity_g_cm3    := c_Density_HeII * rTempRatio5_6;
    
    // Helium-II Specific Entropy: s(T) ~ s_lambda * (T/T_lambda)^5.6 [J/(g*K)]
    rEntropy_s_J_gK := 1.55 * rTempRatio5_6;
    
    // London Thermomechanical Fountain Pressure Integral:
    // Delta_P_F = Integral_{T_target}^{T_actual} [ rho * s(T) ] dT
    // Evaluated via 5-Point Composite Simpson Numerical Quadrature:
    rFountainTempDifference_K := rFiltTemp_K - rTargetTempSetpoint_K;
    rDeltaT_node := rFountainTempDifference_K * 0.25;
    
    FOR iNode := 1 TO 5 DO
        rNodeT := rTargetTempSetpoint_K + (INT_TO_REAL(iNode - 1) * rDeltaT_node);
        IF rNodeT < 0.5 THEN rNodeT := 0.5; ELSIF rNodeT > c_T_lambda THEN rNodeT := c_T_lambda; END_IF;
        
        rNodeRatio := rNodeT / c_T_lambda;
        rNodeRatio5_6 := (rNodeRatio * rNodeRatio * rNodeRatio * rNodeRatio * rNodeRatio) * (0.4 + 0.6 * rNodeRatio);
        IF rNodeRatio5_6 > 1.0 THEN rNodeRatio5_6 := 1.0; END_IF;
        
        aQuadNodeEntropy[iNode] := 1.55 * rNodeRatio5_6; // [J/(g*K)]
        aQuadNodeDensity[iNode] := c_Density_HeII * 1000.0; // [kg/m3]
    END_FOR;
    
    // Composite Simpson's 1/3 Rule: Integral = (h/3) * (f0 + 4*f1 + 2*f2 + 4*f3 + f4)
    // Unit conversion: 1 Pa = 0.01 mbar; rho [kg/m3] * s [J/(kg*K)] = [Pa/K]
    rQuadIntegralAcc := (rDeltaT_node / 3.0) * (
        (aQuadNodeDensity[1] * aQuadNodeEntropy[1] * 1000.0) + 
        (4.0 * aQuadNodeDensity[2] * aQuadNodeEntropy[2] * 1000.0) + 
        (2.0 * aQuadNodeDensity[3] * aQuadNodeEntropy[3] * 1000.0) + 
        (4.0 * aQuadNodeDensity[4] * aQuadNodeEntropy[4] * 1000.0) + 
        (aQuadNodeDensity[5] * aQuadNodeEntropy[5] * 1000.0)
    );
    rFountainPressureDiff_mbar := rQuadIntegralAcc * 0.01; // Convert Pa to mbar
    
    // Superfluid mass flow induced through porous superleak by fountain pressure (Darcy flow):
    // m_dot = rho_s * K_perm * A / L * Delta_P
    rLondonFountainMassFlow_gps := (rSuperfluidDensity_g_cm3 * c_SuperleakFlowArea_cm2 / c_SuperleakLength_cm) * 
                                  (rFountainPressureDiff_mbar * 0.125);

    // Gorter-Mellink Mutual Friction Thermal Transport Function:
    // f(T)^-1 = (rho_s^3 * s^4 * T^3) / (A_GM * rho_n)
    IF rNormalFluidDensity_g_cm3 > 0.0005 THEN
        rGorterMellink_f_inv := ((rSuperfluidDensity_g_cm3 * rSuperfluidDensity_g_cm3 * rSuperfluidDensity_g_cm3) * 
                                 (rEntropy_s_J_gK * rEntropy_s_J_gK * rEntropy_s_J_gK * rEntropy_s_J_gK) * 
                                 (rFiltTemp_K * rFiltTemp_K * rFiltTemp_K)) / 
                                (c_A_GM_FrictionConst * rNormalFluidDensity_g_cm3 * 1.0E-3);
    ELSE
        rGorterMellink_f_inv := 1.0E6; // Near zero normal fluid -> infinite Gorter-Mellink conductance
    END_IF;
    
    // Instantaneous Effective Thermal Conductance [W/K] for cryostat cooling duct:
    rGorterMellinkHeatConductance_W_K := (c_SuperleakFlowArea_cm2 / c_SuperleakLength_cm) * (rGorterMellink_f_inv * 0.085);
    
    // Bulk Apparent Thermal Conductivity [W/(m*K)]
    rObservedThermalConductivity_W_mK := rGorterMellinkHeatConductance_W_K * (c_SuperleakLength_cm * 0.01) / (c_SuperleakFlowArea_cm2 * 0.0001);
    
    // Feynman Quantum Vortex Tangle Line Density Estimation:
    // L_0 = gamma(T)^2 * (v_n - v_s - v_0)^2; here counterflow velocity is proportional to heat flux q:
    // v_counter = q / (rho_s * s * T)
    IF (rSuperfluidDensity_g_cm3 > 0.001) AND (rEntropy_s_J_gK > 0.001) THEN
        rCounterflowVelocity_cm_s := (rHeatFluxDensitySRF_W_cm2) / (rSuperfluidDensity_g_cm3 * rEntropy_s_J_gK * rFiltTemp_K);
        // Critical Feynman velocity for vortex creation: v_c = (kappa / (4*pi*d)) * ln(d / a0)
        rVortexCirculationThreshold := (c_QuantumCirculation_kappa / (4.0 * 3.14159 * c_SuperleakPoreDiameter_nm * 1.0E-9)) * 4.62;
        IF rCounterflowVelocity_cm_s > (rVortexCirculationThreshold * 100.0) THEN
            rVortexLineDensity_m2 := 1.45E8 * (rCounterflowVelocity_cm_s - (rVortexCirculationThreshold * 100.0)) * 
                                              (rCounterflowVelocity_cm_s - (rVortexCirculationThreshold * 100.0));
        ELSE
            rVortexLineDensity_m2 := 0.0;
        END_IF;
    ELSE
        rVortexLineDensity_m2 := 0.0;
    END_IF;

    // Equilibrium Latent Heat Evaporation Rate [g/s]
    rEvaporationBoiloffRate_gps := ((rHeatFluxDensitySRF_W_cm2 * 50.0) + (rFountainPumpHeaterPwr_W)) / c_LatentHeat_1K8;
    
    // Critical Heat Flux Margin Monitoring (Onset of Film Boiling at Nb Cavity Wall)
    IF c_CriticalHeatFlux_1K8_W_cm2 > 0.001 THEN
        rCriticalHeatFluxMargin_pct := (1.0 - (rHeatFluxDensitySRF_W_cm2 / c_CriticalHeatFlux_1K8_W_cm2)) * 100.0;
        IF rCriticalHeatFluxMargin_pct < 15.0 THEN
            bThermalRunawayQuenchRisk := TRUE;
            wAlarmVectorHigh := wAlarmVectorHigh OR 16#00010000; // Bit 16: SRF Thermal Quench Warning
        ELSE
            bThermalRunawayQuenchRisk := FALSE;
            wAlarmVectorHigh := wAlarmVectorHigh AND NOT 16#00010000;
        END_IF;
    END_IF;

ELSE
    // Normal Fluid He-I Regime (T >= T_lambda)
    bSuperfluidRegimeActive             := FALSE;
    rHeII_SuperfluidFraction_pct        := 0.0;
    rSuperfluidDensity_g_cm3            := 0.0;
    rNormalFluidDensity_g_cm3           := c_Density_HeI;
    rEntropy_s_J_gK                     := 1.65 + 1.20 * (rFiltTemp_K - c_T_lambda);
    rFountainPressureDiff_mbar          := 0.0; // Fountain effect nonexistent in He-I
    rLondonFountainMassFlow_gps         := 0.0;
    rGorterMellinkHeatConductance_W_K   := 0.15; // Low conventional thermal conduction
    rObservedThermalConductivity_W_mK   := 0.025; // Standard liquid helium-I conductivity
    rVortexLineDensity_m2               := 0.0;
    rEvaporationBoiloffRate_gps         := ((rHeatFluxDensitySRF_W_cm2 * 50.0) + 1.5) / c_LatentHeat_4K2;
    rCriticalHeatFluxMargin_pct         := 100.0;
    bThermalRunawayQuenchRisk           := FALSE;
END_IF;

// Lambda Transition Complete Verification Flag
bLambdaTransitionComplete := (rFiltTemp_K < (c_T_lambda - 0.015)) AND (rFiltPressure_mbar < (c_P_lambda - 1.50));
""")

    # SECTION 4: State-Space Observer
    parts.append("""
(*
========================================================================================================================
SECTION 4: 4x4 DISCRETE STATE-SPACE MODEL PREDICTOR & OBSERVER UPDATE
========================================================================================================================
Linearized State-Space System Matrices:
  x(k+1) = A * x(k) + B * u(k) + E * w(k)
  y(k)   = C * x(k) + D * u(k)
States:
  x[1] = delta_T_bath      (rFiltTemp_K - rTargetTempSetpoint_K)           [K]
  x[2] = delta_P_vapor     (rFiltPressure_mbar - c_P_nominal_superfluid)   [mbar]
  x[3] = delta_Level       (rFiltLevel_mm - rTargetBathLevel_mm)           [mm]
  x[4] = delta_MassFlow    (rFiltMassFlow_gps - rTargetMassFlow_gps)       [g/s]
Controls:
  u[1] = delta_JT_opening  (rJTOpeningPercent - 25.0)                      [%]
  u[2] = delta_Blower_rpm  (rVacuumPumpingSpeedCmd_rpm - 3600.0)           [rpm]
  u[3] = delta_FountainPwr (rFountainPumpHeaterPwr_W - 5.0)                [W]
Disturbances:
  w[1] = rHeatFluxDensitySRF_W_cm2 * 25.0                                  [W]
  w[2] = 1.25 (Cryostat static radiation and conduction heat leak)        [W]
*)
aState_x[1] := rFiltTemp_K - rTargetTempSetpoint_K;
aState_x[2] := rFiltPressure_mbar - c_P_nominal_superfluid;
aState_x[3] := rFiltLevel_mm - rTargetBathLevel_mm;
aState_x[4] := rFiltMassFlow_gps - rTargetMassFlow_gps;

aState_x_ref[1] := 0.0;
aState_x_ref[2] := 0.0;
aState_x_ref[3] := 0.0;
aState_x_ref[4] := 0.0;

aDisturbance_w[1] := rHeatFluxDensitySRF_W_cm2 * 25.0;
aDisturbance_w[2] := 1.25;

aControl_u[1] := rJTOpeningPercent - 25.0;
aControl_u[2] := rVacuumPumpingSpeedCmd_rpm - 3600.0;
aControl_u[3] := rFountainPumpHeaterPwr_W - 5.0;

// One-Step-Ahead State Prediction: x_pred = A * x + B * u + E * w
FOR iRow := 1 TO 4 DO
    aState_x_pred[iRow] := 0.0;
    
    FOR iCol := 1 TO 4 DO
        aState_x_pred[iRow] := aState_x_pred[iRow] + (aMatrix_A[iRow, iCol] * aState_x[iCol]);
    END_FOR;
    
    FOR iCol := 1 TO 3 DO
        aState_x_pred[iRow] := aState_x_pred[iRow] + (aMatrix_B[iRow, iCol] * aControl_u[iCol]);
    END_FOR;
    
    FOR iCol := 1 TO 2 DO
        aState_x_pred[iRow] := aState_x_pred[iRow] + (aMatrix_E[iRow, iCol] * aDisturbance_w[iCol]);
    END_FOR;
END_FOR;

// Compute Tracking Error Vector
FOR iRow := 1 TO 4 DO
    aState_error[iRow] := aState_x[iRow] - aState_x_ref[iRow];
END_FOR;
""")

    # SECTION 5: MPC Solver with Full 3x3 Hessian Inversion
    parts.append("""
(*
========================================================================================================================
SECTION 5: CONSTRAINED MPC QUADRATIC PROGRAMMING OPTIMIZER (EXPLICIT 3x3 HESSIAN INVERSION)
========================================================================================================================
Cost Function:
  J(u) = (x_pred - x_ref)^T * Q * (x_pred - x_ref) + delta_u^T * R * delta_u + (u - u_nominal)^T * R_rate * (u - u_nominal)

Analytical 3x3 Hessian Matrix Construction:
  H = 2.0 * [ B^T * Q * B + diag(R) + diag(R_rate) ]
*)
VAR_TEMP
    rDeltaJTMax         : REAL;
    rDeltaBlowerMax     : REAL;
    rDeltaHeaterMax     : REAL;
    rH11                : REAL;
    rH12                : REAL;
    rH13                : REAL;
    rH21                : REAL;
    rH22                : REAL;
    rH23                : REAL;
    rH31                : REAL;
    rH32                : REAL;
    rH33                : REAL;
END_VAR

// Assemble Full 3x3 Symmetric Hessian Matrix
FOR iRow := 1 TO 3 DO
    FOR iCol := 1 TO 3 DO
        aHessian_H[iRow, iCol] := 2.0 * (
            (aMatrix_B[1, iRow] * aMatrix_B[1, iCol] * aWeight_Q[1]) + 
            (aMatrix_B[2, iRow] * aMatrix_B[2, iCol] * aWeight_Q[2]) + 
            (aMatrix_B[3, iRow] * aMatrix_B[3, iCol] * aWeight_Q[3]) + 
            (aMatrix_B[4, iRow] * aMatrix_B[4, iCol] * aWeight_Q[4])
        );
        IF iRow = iCol THEN
            aHessian_H[iRow, iCol] := aHessian_H[iRow, iCol] + (2.0 * (aWeight_R[iRow] + aWeight_R_rate[iRow]));
        END_IF;
    END_FOR;
END_FOR;

// Compute Gradient Vector g = 2.0 * B^T * Q * error + 2.0 * diag(R) * u
FOR iCol := 1 TO 3 DO
    aGradient_g[iCol] := 0.0;
    FOR iRow := 1 TO 4 DO
        aGradient_g[iCol] := aGradient_g[iCol] + (2.0 * aMatrix_B[iRow, iCol] * aWeight_Q[iRow] * aState_error[iRow]);
    END_FOR;
    aGradient_g[iCol] := aGradient_g[iCol] + (2.0 * aWeight_R[iCol] * aControl_u[iCol]);
END_FOR;

// Exact Analytical Determinant of 3x3 Hessian Matrix
rH11 := aHessian_H[1, 1]; rH12 := aHessian_H[1, 2]; rH13 := aHessian_H[1, 3];
rH21 := aHessian_H[2, 1]; rH22 := aHessian_H[2, 2]; rH23 := aHessian_H[2, 3];
rH31 := aHessian_H[3, 1]; rH32 := aHessian_H[3, 2]; rH33 := aHessian_H[3, 3];

rDetHessian := (rH11 * (rH22 * rH33 - rH23 * rH32)) - 
               (rH12 * (rH21 * rH33 - rH23 * rH31)) + 
               (rH13 * (rH21 * rH32 - rH22 * rH31));

// Compute Inverse Hessian Matrix using Classical Adjugate Method
IF ABS(rDetHessian) > 1.0E-9 THEN
    aHessian_inv[1, 1] :=  (rH22 * rH33 - rH23 * rH32) / rDetHessian;
    aHessian_inv[1, 2] := -(rH12 * rH33 - rH13 * rH32) / rDetHessian;
    aHessian_inv[1, 3] :=  (rH12 * rH23 - rH13 * rH22) / rDetHessian;

    aHessian_inv[2, 1] := -(rH21 * rH33 - rH23 * rH31) / rDetHessian;
    aHessian_inv[2, 2] :=  (rH11 * rH33 - rH13 * rH31) / rDetHessian;
    aHessian_inv[2, 3] := -(rH11 * rH23 - rH13 * rH21) / rDetHessian;

    aHessian_inv[3, 1] :=  (rH21 * rH32 - rH22 * rH31) / rDetHessian;
    aHessian_inv[3, 2] := -(rH11 * rH32 - rH12 * rH31) / rDetHessian;
    aHessian_inv[3, 3] :=  (rH11 * rH22 - rH12 * rH21) / rDetHessian;

    // Unconstrained Optimal Newton Step: delta_u_opt = - H^-1 * g
    FOR iRow := 1 TO 3 DO
        aDelta_u_unconstrained[iRow] := -(
            (aHessian_inv[iRow, 1] * aGradient_g[1]) + 
            (aHessian_inv[iRow, 2] * aGradient_g[2]) + 
            (aHessian_inv[iRow, 3] * aGradient_g[3])
        );
    END_FOR;
ELSE
    // Determinant singularity fallback: Simple diagonal decoupled descent
    aDelta_u_unconstrained[1] := -aGradient_g[1] / (rH11 + 0.1);
    aDelta_u_unconstrained[2] := -aGradient_g[2] / (rH22 + 0.001);
    aDelta_u_unconstrained[3] := -aGradient_g[3] / (rH33 + 0.1);
END_IF;

// Active Set Projection onto Physical Actuator Rate Limits
rDeltaJTMax := rSlewLimit_JT_pct_s * c_SampleTime_s;
rDeltaBlowerMax := rSlewLimit_Blower_rpm_s * c_SampleTime_s;
rDeltaHeaterMax := rSlewLimit_Heater_W_s * c_SampleTime_s;

// Input 1 Clamping (Joule-Thomson Valve Throttling)
IF aDelta_u_unconstrained[1] > rDeltaJTMax THEN
    aDelta_u_opt[1] := rDeltaJTMax;
ELSIF aDelta_u_unconstrained[1] < -rDeltaJTMax THEN
    aDelta_u_opt[1] := -rDeltaJTMax;
ELSE
    aDelta_u_opt[1] := aDelta_u_unconstrained[1];
END_IF;

// Input 2 Clamping (Cold Vacuum Roots Blower VFD Speed)
IF aDelta_u_unconstrained[2] > rDeltaBlowerMax THEN
    aDelta_u_opt[2] := rDeltaBlowerMax;
ELSIF aDelta_u_unconstrained[2] < -rDeltaBlowerMax THEN
    aDelta_u_opt[2] := -rDeltaBlowerMax;
ELSE
    aDelta_u_opt[2] := aDelta_u_unconstrained[2];
END_IF;

// Input 3 Clamping (London Thermomechanical Fountain Heater Power)
IF aDelta_u_unconstrained[3] > rDeltaHeaterMax THEN
    aDelta_u_opt[3] := rDeltaHeaterMax;
ELSIF aDelta_u_unconstrained[3] < -rDeltaHeaterMax THEN
    aDelta_u_opt[3] := -rDeltaHeaterMax;
ELSE
    aDelta_u_opt[3] := aDelta_u_unconstrained[3];
END_IF;
""")

    # SECTION 6: Multi-Stage State Machine
    parts.append("""
(*
========================================================================================================================
SECTION 6: SUPERVISORY FINITE STATE MACHINE (SFSM) - 11 THERMODYNAMIC STAGES
========================================================================================================================
Cryostat Operating Sequence:
   0: COLD_IDLE_SELFTEST_STANDBY
  10: LHE4_SUPERCRITICAL_FILL_AND_PURGE (300 K -> 4.2 K)
  20: EQUILIBRATION_4K2_BATH_SVP_REFERENCE
  30: VACUUM_ROOSTER_PUMP_CASCADE_CHILLDOWN
  40: CONTROLLED_SUB_MILLIBAR_PUMPDOWN_APPROACH (4.2 K -> 2.30 K)
  50: PRE_LAMBDA_EXPANSION_CRITICAL_DECELERATION (2.30 K -> 2.18 K)
  60: LAMBDA_TRANSITION_CROSSING_SINGULARITY_WINDOW (2.18 K -> 2.16 K)
  70: SUPERFLUID_HE_II_1K8_STEADY_STATE_REGIME (1.800 K +/- 0.5 mK)
  80: SUPERCONDUCTING_RF_CAVITY_HEAT_LOAD_FEEDFORWARD
  90: CONTROLLED_THERMAL_RECUPERATION_AND_WARMUP
  99: CRYOGENIC_QUENCH_RELIEF_EMERGENCY_DEGRADATION
*)
// Maintain state dwell timer
tStateTimer(IN := (iOperatingState = iPreviousState), PT := T#86400S);
IF iOperatingState <> iPreviousState THEN
    iPreviousState := iOperatingState;
    bStateFirstScan := TRUE;
    rStateTimeSeconds := 0.0;
ELSE
    bStateFirstScan := FALSE;
    rStateTimeSeconds := TIME_TO_REAL(tStateTimer.ET) * 0.001;
END_IF;

CASE iOperatingState OF

    (* -------------------------------------------------------------------------
       STATE 0: COLD IDLE SELF TEST & SYSTEM STANDBY
       ------------------------------------------------------------------------- *)
    0:
        wCryostatStatusWord := 16#0000;
        rJTOpeningPercent := 0.0;
        rVacuumPumpingSpeedCmd_rpm := 0.0;
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Permissive self-test evaluation: sensor bridge health check
        IF bSystemEnable AND (iTMRMode_Temp >= 2) AND (iTMRMode_Press >= 2) THEN
            IF rFiltTemp_K > 77.0 THEN
                iOperatingState := 10; // Warm cryostat: Precool and transfer fill required
            ELSIF rFiltTemp_K <= 4.5 THEN
                iOperatingState := 20; // Cold bath already full: Proceed to equilibration
            ELSE
                iOperatingState := 10;
            END_IF;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 10: LIQUID HELIUM-4 TRANSFER & CAVITY PRECOOL (4.2 K, 1013 mbar)
       ------------------------------------------------------------------------- *)
    10:
        wCryostatStatusWord := 16#0010;
        // Thermal stress mitigation: regulate cooldown rate < 15 K/hour on high-purity SRF Niobium
        IF rDerivativeTemp_K_s < -0.00416 THEN // Exceeds 15 K/hr limit
            rJTOpeningPercent := rJTOpeningPercent - (0.5 * c_SampleTime_s);
        ELSE
            rJTOpeningPercent := rJTOpeningPercent + (0.2 * c_SampleTime_s);
        END_IF;
        
        // Pumping line isolated during 1 bar atmospheric transfer fill
        rVacuumPumpingSpeedCmd_rpm := 0.0;
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Completion criterion: Liquid level reaches 500 mm and temperature stabilizes at 4.2 K
        IF (rFiltTemp_K <= 4.25) AND (rFiltLevel_mm >= 500.0) THEN
            iOperatingState := 20;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 20: 4.2 K BATH LEVEL & PRESSURE EQUILIBRATION
       ------------------------------------------------------------------------- *)
    20:
        wCryostatStatusWord := 16#0020;
        // Regulate liquid helium level to nominal 650 mm setpoint
        IF rFiltLevel_mm < rTargetBathLevel_mm THEN
            rJTOpeningPercent := rJTOpeningPercent + (0.5 * c_SampleTime_s);
        ELSE
            rJTOpeningPercent := rJTOpeningPercent - (0.5 * c_SampleTime_s);
        END_IF;
        
        rVacuumPumpingSpeedCmd_rpm := 0.0;
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Stabilize for 60 seconds at saturated 4.2 K before vacuum line chilldown
        IF (rStateTimeSeconds >= 60.0) AND (ABS(rFiltLevel_mm - rTargetBathLevel_mm) < 15.0) THEN
            iOperatingState := 30;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 30: VACUUM ROOTS BLOWER CASCADE CHILLDOWN & PURGE
       ------------------------------------------------------------------------- *)
    30:
        wCryostatStatusWord := 16#0030;
        // Spool vacuum blower to idling speed (500 rpm) to evaluate seal purge and line delta-P
        rVacuumPumpingSpeedCmd_rpm := 500.0;
        rJTOpeningPercent := 18.0; // Maintain steady flash make-up liquid flow
        rFountainPumpHeaterPwr_W := 0.0;
        
        IF rStateTimeSeconds >= 30.0 THEN
            iOperatingState := 40; // Engage active pumpdown
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 40: CONTROLLED SUB-MILLIBAR PUMPDOWN (4.2 K -> 2.30 K)
       ------------------------------------------------------------------------- *)
    40:
        wCryostatStatusWord := 16#0040;
        // Follow target pressure ramp rate (nominal 1.5 mbar/s)
        IF rDerivativePressure_mbar_s > -1.5 THEN
            rVacuumPumpingSpeedCmd_rpm := rVacuumPumpingSpeedCmd_rpm + (rSlewLimit_Blower_rpm_s * c_SampleTime_s);
        ELSIF rDerivativePressure_mbar_s < -2.2 THEN
            rVacuumPumpingSpeedCmd_rpm := rVacuumPumpingSpeedCmd_rpm - (rSlewLimit_Blower_rpm_s * c_SampleTime_s);
        END_IF;
        
        rJTOpeningPercent := 15.0 + aDelta_u_opt[1];
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Approaching lambda transition zone (T <= 2.30 K or P <= 68 mbar) -> Decelerate
        IF (rFiltTemp_K <= 2.300) OR (rFiltPressure_mbar <= 68.0) THEN
            iOperatingState := 50;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 50: PRE-LAMBDA EXPANSION CRITICAL DECELERATION (2.30 K -> 2.18 K)
       ------------------------------------------------------------------------- *)
    50:
        wCryostatStatusWord := 16#0050;
        // Decelerate pumpdown derivative to 0.25 mbar/s to mitigate C_p singularity divergence
        IF rDerivativePressure_mbar_s < -0.25 THEN
            rVacuumPumpingSpeedCmd_rpm := rVacuumPumpingSpeedCmd_rpm - (rSlewLimit_Blower_rpm_s * c_SampleTime_s);
        ELSE
            rVacuumPumpingSpeedCmd_rpm := rVacuumPumpingSpeedCmd_rpm + (10.0 * c_SampleTime_s);
        END_IF;
        
        rJTOpeningPercent := 12.0 + aDelta_u_opt[1];
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Singularity boundary threshold reached
        IF rFiltTemp_K <= 2.180 THEN
            iOperatingState := 60;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 60: LAMBDA TRANSITION CROSSING SINGULARITY WINDOW (2.18 K -> 2.16 K)
       ------------------------------------------------------------------------- *)
    60:
        wCryostatStatusWord := 16#0060;
        // Phase transition crossing window: holding blower steady to avoid acoustic cavitation
        tLambdaCrossingTimer(IN := TRUE, PT := T#45S);
        
        rJTOpeningPercent := 10.0; // Stabilize JT inlet
        rFountainPumpHeaterPwr_W := 0.0;
        
        // Detect phase transition crossing completion: T < 2.165 K and P < 48.5 mbar
        IF (rFiltTemp_K <= 2.165) AND (rFiltPressure_mbar <= 48.5) THEN
            tLambdaCrossingTimer(IN := FALSE);
            iOperatingState := 70; // Transition to Deep Superfluid He-II Steady State
        ELSIF tLambdaCrossingTimer.Q THEN
            // Singularity stall timeout: slowly assist with small blower increment
            rVacuumPumpingSpeedCmd_rpm := rVacuumPumpingSpeedCmd_rpm + 25.0;
            tLambdaCrossingTimer(IN := FALSE);
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 70: DEEP SUPERFLUID HE-II 1.8 K STEADY-STATE REGIME
       ------------------------------------------------------------------------- *)
    70:
        wCryostatStatusWord := 16#0070;
        // Fully engage Constrained Model Predictive Control (MPC) optimization
        IF NOT bManualModeSelect THEN
            rJTOpeningPercent := 25.0 + aControl_u[1] + aDelta_u_opt[1];
            rVacuumPumpingSpeedCmd_rpm := 3600.0 + aControl_u[2] + aDelta_u_opt[2];
            rFountainPumpHeaterPwr_W := 5.0 + aControl_u[3] + aDelta_u_opt[3];
        ELSE
            rJTOpeningPercent := rManualJTPos_pct;
            rVacuumPumpingSpeedCmd_rpm := rManualBlowerRpm;
            rFountainPumpHeaterPwr_W := rManualHeaterPwr_W;
        END_IF;
        
        // Detect superconducting RF cavity pulsed heat load activation
        IF rHeatFluxDensitySRF_W_cm2 > 0.15 THEN
            iOperatingState := 80;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 80: SUPERCONDUCTING RF CAVITY HEAT LOAD FEEDFORWARD BALANCING
       ------------------------------------------------------------------------- *)
    80:
        wCryostatStatusWord := 16#0080;
        // Anticipatory feedforward pulse balancing
        tPulseHeatHoldTimer(IN := (rHeatFluxDensitySRF_W_cm2 <= 0.05), PT := T#15S);
        
        rVacuumPumpingSpeedCmd_rpm := 3600.0 + (rHeatFluxDensitySRF_W_cm2 * 850.0) + aDelta_u_opt[2];
        rJTOpeningPercent := 25.0 + (rHeatFluxDensitySRF_W_cm2 * 12.0) + aDelta_u_opt[1];
        rFountainPumpHeaterPwr_W := 2.0; // Lower background heater to absorb RF dissipation
        
        IF tPulseHeatHoldTimer.Q THEN
            tPulseHeatHoldTimer(IN := FALSE);
            iOperatingState := 70; // Return to baseline steady state
        END_IF;
        
        // Critical heat flux violation check
        IF bThermalRunawayQuenchRisk THEN
            iOperatingState := 99; // Abort to Emergency Quench Relief
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 90: CONTROLLED THERMAL RECUPERATION & WARMUP
       ------------------------------------------------------------------------- *)
    90:
        wCryostatStatusWord := 16#0090;
        rJTOpeningPercent := 0.0;
        rVacuumPumpingSpeedCmd_rpm := 0.0;
        rFountainPumpHeaterPwr_W := 15.0; // Gentle warm-up heater
        
        IF rFiltTemp_K >= 4.2 THEN
            rFountainPumpHeaterPwr_W := 0.0;
            IF rFiltTemp_K >= 280.0 THEN
                iOperatingState := 0; // Return to room temperature standby
            END_IF;
        END_IF;

    (* -------------------------------------------------------------------------
       STATE 99: CRYOGENIC QUENCH RELIEF EMERGENCY DEGRADATION
       ------------------------------------------------------------------------- *)
    99:
        wCryostatStatusWord := 16#0099;
        // Hard slam JT valve shut to prevent feeding liquid into quenching vessel
        rJTOpeningPercent := 0.0;
        // Trip Roots blower to prevent overpressure back-spin
        rVacuumPumpingSpeedCmd_rpm := 0.0;
        // De-energize all electrical heaters immediately
        rFountainPumpHeaterPwr_W := 0.0;
        
        tQuenchReliefTimer(IN := TRUE, PT := T#300S);
        wAlarmVectorHigh := wAlarmVectorHigh OR 16#00080000; // Bit 19: Cryogenic Quench State Active
        
        IF bAcknowledgeQuench AND tQuenchReliefTimer.Q AND (rFiltPressure_mbar < 1050.0) THEN
            tQuenchReliefTimer(IN := FALSE);
            iOperatingState := 0; // Transition to safe standby
        END_IF;

END_CASE;
""")

    # SECTION 7: Actuator Clamping, Alarm Bitmasking, and Status Words
    parts.append("""
(*
========================================================================================================================
SECTION 7: FINAL ACTUATOR CLAMPING, SLEW LIMITING & 64-BIT DIAGNOSTIC MATRIX
========================================================================================================================
High-Priority Safety Alarm Vector (wAlarmVectorHigh):
  Bit  0: Emergency Stop Interlock Tripped
  Bit  1: Cernox Channel A Deviation Fault
  Bit  2: Cernox Channel B Deviation Fault
  Bit  3: Cernox Channel C Deviation Fault
  Bit  4: Temp TMR Degraded to 1oo2
  Bit  5: Critical Temperature Sensor Redundancy Lost (Simplex Fallback)
  Bit  6: Total Temperature Sensor Failure
  Bit  7: Reserved / Sensor Excitation Bridge Open-Circuit
  Bit  8: Baratron Channel A Disparity Fault
  Bit  9: Baratron Channel B Disparity Fault
  Bit 10: Baratron Channel C Disparity Fault
  Bit 11: Pressure TMR Degraded to 1oo2
  Bit 12: Critical Pressure Sensor Redundancy Lost (Simplex Fallback)
  Bit 13: Total Pressure Sensor Failure
  Bit 14: Reserved
  Bit 15: Cryostat Liquid Helium Level Below Low-Low Trip (< 150 mm)
  Bit 16: SRF Cavity Thermal Runaway Quench Risk (Gorter-Mellink Breakdown)
  Bit 17: Cryostat Vacuum Insulation Degradation
  Bit 18: Taconis Thermo-Acoustic Oscillation Detected
  Bit 19: Superconducting Magnet / RF Cavity Quench Relief Active
  Bit 20: Joule-Thomson Cryogenic Stem Freezing / Mechanical Jam
  Bit 21: Cold Roots Blower Excessive Vibration / Bearing Temp High
  Bit 22: Vacuum Pumping Line Sub-Atmospheric Air Ingress Interlock
  Bit 23: Porous Superleak Sinter Breakthrough / Normal Fluid Contamination
  Bit 24: Helium-4 Lambda Singularity Crossing Velocity Limit Exceeded
  Bit 25: Magnet Transport Current Ramp Rate Mismatch
  Bit 26: Fountain Pump Heater Thermal Runaway Cutoff
  Bit 27: Liquid Helium Bath Overflow Warning (> 920 mm)
  Bit 28: Cold Return Mass Flow Meter Differential Low / Line Choked
  Bit 29: Cryostat Overpressure Relief Lift Event
  Bit 30: Safety Controller Watchdog Refresh Timing Jitter
  Bit 31: SIL-3 Master Hardware Interlock Trip Vector
*)
// Additional Physical Threshold Alarms
IF rFiltLevel_mm < 150.0 THEN
    wAlarmVectorHigh := wAlarmVectorHigh OR 16#00008000; // Bit 15: Low-Low Liquid Helium Level
END_IF;
IF rFiltLevel_mm > 920.0 THEN
    wAlarmVectorLow := wAlarmVectorLow OR 16#08000000; // Bit 27: Liquid Helium Overflow
END_IF;
IF (rFiltTemp_K < c_T_lambda) AND (rFiltPressure_mbar > 55.0) THEN
    wAlarmVectorLow := wAlarmVectorLow OR 16#01000000; // Bit 24: Superheated He-II / Non-Equilibrium
END_IF;

// Joule-Thomson Actuator Physical Limits [0.0% to 100.0%]
IF rJTOpeningPercent > c_MaxJTValveOpening_pct THEN
    rJTOpeningPercent := c_MaxJTValveOpening_pct;
ELSIF rJTOpeningPercent < c_MinJTValveOpening_pct THEN
    rJTOpeningPercent := c_MinJTValveOpening_pct;
END_IF;

// Roots Vacuum Blower Speed Physical Limits [0.0 to 6000.0 rpm]
IF iOperatingState >= 30 AND iOperatingState < 90 THEN
    IF rVacuumPumpingSpeedCmd_rpm > c_MaxBlowerRpm THEN
        rVacuumPumpingSpeedCmd_rpm := c_MaxBlowerRpm;
    ELSIF rVacuumPumpingSpeedCmd_rpm < c_MinBlowerRpm THEN
        rVacuumPumpingSpeedCmd_rpm := c_MinBlowerRpm;
    END_IF;
ELSE
    IF iOperatingState = 90 OR iOperatingState = 99 OR iOperatingState = 0 THEN
        rVacuumPumpingSpeedCmd_rpm := 0.0;
    END_IF;
END_IF;

// Fountain Pump Heater Power Physical Limits [0.0 W to 35.0 W]
IF rFountainPumpHeaterPwr_W > c_MaxFountainHeaterPwr_W THEN
    rFountainPumpHeaterPwr_W := c_MaxFountainHeaterPwr_W;
ELSIF rFountainPumpHeaterPwr_W < 0.0 THEN
    rFountainPumpHeaterPwr_W := 0.0;
END_IF;

// Supervisory Status Word Bit-Packing:
// Bit 0: Emergency Stop Tripped
// Bit 1: Superfluid Regime Active (T < 2.1768 K)
// Bit 2: Lambda Transition Complete
// Bit 3: Thermal Quench Risk
// Bit 4-7: Operating State Nibble
// Bit 8-9: Temperature TMR Status (3=2oo3, 2=1oo2, 1=Simplex, 0=Fail)
// Bit 10-11: Pressure TMR Status
IF bSuperfluidRegimeActive THEN
    wCryostatStatusWord := wCryostatStatusWord OR 16#0002;
END_IF;
IF bLambdaTransitionComplete THEN
    wCryostatStatusWord := wCryostatStatusWord OR 16#0004;
END_IF;
IF bThermalRunawayQuenchRisk THEN
    wCryostatStatusWord := wCryostatStatusWord OR 16#0008;
END_IF;
wCryostatStatusWord := wCryostatStatusWord OR SHL(INT_TO_WORD(iOperatingState / 10), 4);
wCryostatStatusWord := wCryostatStatusWord OR SHL(INT_TO_WORD(iTMRMode_Temp), 8);
wCryostatStatusWord := wCryostatStatusWord OR SHL(INT_TO_WORD(iTMRMode_Press), 10);

END_FUNCTION_BLOCK
""")

    code_text = "".join(parts)
    return code_text

if __name__ == "__main__":
    code = generate_iec_st()
    print("Character count:", len(code))
    lines = code.splitlines()
    print("First line:", lines[0])
    print("Last line:", lines[-1])
