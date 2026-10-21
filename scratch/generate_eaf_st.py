import os
import re
import json
import uuid

def build_eaf_st_code():
    # We will assemble the complete Structured Text code in pieces with immense technical detail.
    parts = []
    
    # 1. Header & Function block opening
    parts.append("""FUNCTION_BLOCK FB_EAF_FoamingSlag_MicrowaveRadar_CarbonInject
(*
 ====================================================================================================
  ENTERPRISE HEAVY METALLURGY AUTOMATION ARCHITECTURE - IEC 61131-3 COMPLIANT FUNCTION BLOCK
  SYSTEM:        150-TON HIGH-POWER AC ELECTRIC ARC FURNACE (EAF) - 140 MVA MELTING FACILITY
  SUBSYSTEM:     DYNAMIC FOAMING SLAG OPTIMIZATION & CO-AXIAL SUPERSONIC MULTI-LANCE INJECTION
  INSTRUMENTS:   24 GHz FMCW MICROWAVE RADAR (2oo3 TMR) SLAG THICKNESS & DIELECTRIC PROFILING,
                 SUPERSONIC CO-AXIAL CARBON/OXYGEN LANCE PENETRATION RATIO HYDRODYNAMICS,
                 ARC ACOUSTIC EMISSION & 3-PHASE ELECTRICAL HARMONIC IMPEDANCE SENSOR FUSION,
                 WATER-COOLED DELTA ROOF RADIATIVE THERMAL FLUX NUCLEATE BOILING PROTECTION.
 ----------------------------------------------------------------------------------------------------
  THEORY OF PROCESS OPERATION & CYBER-PHYSICAL KINETICS:
 
  1. METALLURGICAL FOAMING DYNAMICS:
     Slag foaming in high-power AC electric arc furnaces is governed by the generation of carbon
     monoxide (CO) gas bubbles within a molten silicate-iron-oxide slag matrix through the primary
     endothermic reduction reaction:
         (FeO) + C(s) -> Fe(l) + CO(g)   [Delta H = +159 kJ/mol at 1600 deg C]
     supplemented by the in-flight and surface oxidation of injected carbon by supersonic oxygen:
         2 C(s) + O2(g) -> 2 CO(g)       [Delta H = -221 kJ/mol at 1600 deg C]
     The volumetric rate of CO gas generation V_dot_CO [Nm3/s] drives the superficial gas velocity
     j_g = V_dot_CO / A_bath [m/s]. The physical foam layer thickness H_slag [mm] is defined by the
     dynamic Slag Foaming Index Sigma [s] (Bikerman / Ito & Fruehan formulation):
         H_slag = H_liquid_slag + Sigma * j_g
     where Sigma is an intrinsic property of the slag physical chemistry:
         Sigma = (mu_slag) / (SQRT(gamma_slag * rho_slag * g) * d_bubble^1.2)
     in which mu_slag is dynamic viscosity [Pa.s], gamma_slag is surface tension [N/m], rho_slag is
     bulk slag density (~2200-2800 kg/m3), g is gravitational acceleration (9.81 m/s2), and d_bubble
     is the mean Sauter bubble diameter (~5-15 mm). Slag basicity (B2 = %CaO / %SiO2, target 1.8-2.2)
     and MgO saturation (~8-12%) are regulated via lime/dolomitic flux additions to maintain solid
     second-phase dicalcium silicate (C2S) and magnesio-wustite precipitates that dramatically boost
     apparent foam viscosity mu_app without causing crusting or slag freezing.
 
  2. 24 GHz FMCW MICROWAVE RADAR PROFILING:
     Roof-mounted triple modular redundant (2oo3 TMR) 24 GHz K-band Frequency Modulated Continuous
     Wave (FMCW) radar transceivers perform real-time range profiling across the harsh furnace interior.
     With a chirp bandwidth B = 1.5 GHz, the free-space range resolution is Delta_R = c / (2*B) = 100 mm,
     further refined to sub-centimeter accuracy via phase spectral interpolation. The radar signal
     penetrates optical smoke, dust, and non-ionized furnace atmospheres to detect:
       a) Primary reflection boundary: Slag surface meniscus R_surface (gas-foam interface).
       b) Secondary reflection boundary: Dense liquid steel bath meniscus R_steel (foam-steel interface).
     The propagation velocity through the foam is slowed by the effective relative dielectric
     permittivity eps_eff:
       v_prop = c / SQRT(eps_eff)
     where eps_eff is dynamically estimated from off-gas ionization, temperature, and slag void fraction
     (Bruggeman effective medium approximation). The physical foaming slag thickness is calculated as:
       H_slag = (R_steel - R_surface) / SQRT(eps_eff)
     A 2oo3 median voter isolates malfunctioning transceivers caused by optical window fouling,
     thermal drift, or waveguide dielectric breakdown, degrading to 1oo2 or acoustic-impedance mode.
 
  3. SUPERSONIC CO-AXIAL LANCE PENETRATION HYDRODYNAMICS:
     A co-axial water-cooled lance operates with a central Mach 2.15 convergent-divergent Laval nozzle
     delivering high-purity oxygen at 3,000 to 6,500 Nm3/h, enveloped by an annular shroud delivering
     pulverized carbon (anthracite or petcoke) at 20 to 75 kg/min via dense-phase pneumatic conveyance.
     The supersonic jet core length L_core and jet impact dynamic pressure govern the liquid slag cavity
     penetration depth L_p [mm] according to the modified Koria-Lange & Banks-Chandrasekhara model:
       L_p = 0.046 * (P_O2 / P_atm)^0.58 * (d_throat / SIN(theta_lance)) * SQRT(rho_O2 / rho_slag) * (1 + beta_shroud)
     The lance carriage vertical position Z_lance [mm] is continuously actuated to maintain the
     dimensionless Penetration Ratio:
       PR = L_p / H_slag
     strictly within the optimal metallurgical stability window: PR_opt in [0.65, 0.85].
     - If PR < 0.60: Under-penetration occurs. Injected carbon and oxygen react primarily in the freeboard
       or top surface, leading to parasitic CO post-combustion, overheating the off-gas duct, and failing
       to reduce FeO inside the slag bulk.
     - If PR > 0.90: Over-penetration occurs. The supersonic jet punches entirely through the slag layer,
       impinging directly upon the liquid steel bath, causing severe iron splashing, explosive slag boils,
       carbon loss into the metal, and accelerated refractory wear.
 
  4. ARC ACOUSTIC EMISSION & 3-PHASE ELECTRICAL HARMONIC DISTORTION SENSOR FUSION:
     When an electric arc discharges in open atmosphere, it behaves as a non-linear, high-temperature
     acoustic noise generator emitting 112 to 118 dBA of broadband noise and massive odd harmonic
     distortion (3rd harmonic 150 Hz, 5th harmonic 250 Hz) due to cathode-spot instability and voltage
     zero-crossing arc restrikes.
     When the foaming slag expands and submerges the 3-phase graphite electrodes:
       a) Acoustic Attenuation: The multi-phase bubble emulsion attenuates acoustic pressure waves,
          reducing sound pressure levels by 15 to 22 dB (target SPL: 92-96 dBA).
       b) Harmonic Distortion: The hot, ionized, electrically conductive slag envelope provides a
          continuous ionization path, eliminating restrike transients. The Harmonic Distortion Index
          HDI = (V_3rd / V_1st) * 100% drops from >22% down to <4.5%.
       c) Impedance Stabilization: The arc resistance R_arc and reactance X_arc stabilize, drastically
          reducing high-frequency power variance.
     The FB synthesizes a composite Arc Submergence Factor (0 to 100%) by fusing 2oo3 Radar thickness,
     Acoustic Attenuation dB, and 3-Phase HDI, providing redundant feedback even during radar blackouts.
 
  5. WATER-COOLED ROOF DELTA PANEL THERMAL FLUX PROTECTION:
     High-power arcs radiate immense thermal energy (P_rad = sigma * (T_arc^4 - T_roof^4) * F_view).
     With an open, unshielded arc, the radiation view factor F_view to the roof delta panels reaches
     0.42, causing radiant heat fluxes exceeding 350-450 kW/m2. This exposes tubular water-cooled copper
     and steel panels to subcooled nucleate boiling crisis and potential film boiling burnout (DNB),
     introducing catastrophe risks of high-pressure cooling water leaking into molten steel (steam explosion).
     With a fully foaming slag (Submergence Factor > 90%), the arc is physically shielded, dropping F_view
     below 0.03 and roof thermal flux below 120 kW/m2.
     The FB incorporates a 2oo3 TMR heat-flux sensor voter, differential water calorimetry (Delta T * Flow),
     and an active dual-tier safety supervisor:
       - Warning Threshold (280 kW/m2): Initiates automatic carbon injection boost (+25%), oxygen trim,
         and lance elevation adjustment.
       - Critical Emergency Trip Threshold (350 kW/m2): Initiates immediate 50% electrical power derate,
         emergency lance retraction, and emergency purge to preserve panel structural integrity.
 
  6. EMBEDDED REAL-TIME MODEL PREDICTIVE CONTROL (MPC) & DISCRETE STATE-SPACE:
     A discrete 4-state, 3-input, 2-disturbance state-space model is executed at Ts = 50 ms:
       x[k+1] = A * x[k] + B * u[k] + Bd * d[k]
       y[k]   = C * x[k] + D * u[k]
     where states x = [H_slag (m), FeO_pct (%), Q_roof (kW/m2), V_dot_CO (Nm3/s)],
     inputs u = [Flow_O2 (Nm3/h), Feed_Carbon (kg/min), Lance_Z (mm)],
     disturbances d = [Arc_Power (MW), Lime_Dolomite (kg/min)].
     The constrained quadratic objective function:
       J = 0.5 * u^T * H * u + g^T * u
     is solved at every scan via a high-speed projected gradient descent algorithm with active actuator
     rate limits and physical clamping, delivering optimal foaming with minimal refractory wear.
 ====================================================================================================
*)
""")

    # 2. VAR_INPUT
    parts.append("""VAR_INPUT
    (* === MASTER AUTOMATION & SAFETY SYSTEM INTERLOCKS === *)
    bSystemEnable                   : BOOL;     (* Global System Master Enable Permissive from Main EAF Pulpit *)
    bEmergencyStop                  : BOOL;     (* Failsafe Hardwired Safety Relay Circuit Healthy [NC: True = OK] *)
    bResetFaults                    : BOOL;     (* Operator Alarm Acknowledge & Fault Reset Command *)
    rCycleTime_sec                  : REAL := 0.050; (* PLC Cyclic Task Execution Scan Interval [s] *)
    iFurnaceHeatPhase               : INT;      (* EAF Operational Phase (0:Idle, 1:BoreIn, 2:Meltdown, 3:Refining, 4:Tapping) *)

    (* === ELECTRICAL 3-PHASE ARC SENSORS & POWER METRICS [kA, V, MW] === *)
    rArcCurrent_PhaseA_kA           : REAL;     (* Phase A Arc RMS Conductor Current [kA] *)
    rArcCurrent_PhaseB_kA           : REAL;     (* Phase B Arc RMS Conductor Current [kA] *)
    rArcCurrent_PhaseC_kA           : REAL;     (* Phase C Arc RMS Conductor Current [kA] *)
    rArcVoltage_PhaseA_V            : REAL;     (* Phase A Arc Line-to-Neutral RMS Voltage [V] *)
    rArcVoltage_PhaseB_V            : REAL;     (* Phase B Arc Line-to-Neutral RMS Voltage [V] *)
    rArcVoltage_PhaseC_V            : REAL;     (* Phase C Arc Line-to-Neutral RMS Voltage [V] *)
    rActiveElectricalPower_MW       : REAL;     (* Furnace Total Active Real Electric Power [MW] *)

    (* === 24 GHz FMCW MICROWAVE RADAR 2oo3 TMR CHANNELS [mm] === *)
    rRadarDistance_Raw_A_mm         : REAL;     (* FMCW Microwave Radar Channel A Measured Range to Slag [mm] *)
    rRadarDistance_Raw_B_mm         : REAL;     (* FMCW Microwave Radar Channel B Measured Range to Slag [mm] *)
    rRadarDistance_Raw_C_mm         : REAL;     (* FMCW Microwave Radar Channel C Measured Range to Slag [mm] *)

    (* === CO-AXIAL SUPERSONIC LANCE & INJECTION SENSORS [mm, Nm3/h, kg/min] === *)
    rLanceElevation_Current_mm      : REAL;     (* Co-Axial Lance Carriage Current Position Above Steel Bath [mm] *)
    rOxygenFlow_Actual_Nm3h         : REAL;     (* Primary Supersonic Laval Oxygen Actual Volumetric Flow [Nm3/h] *)
    rCarbonInjectionFlow_Actual_kgmin: REAL;    (* Annular Co-Axial Pulverized Carbon Mass Flow Rate [kg/min] *)
    rNitrogenPurgeFlow_Nm3h         : REAL;     (* Radar Antenna Waveguide High-Velocity N2 Purge Flow [Nm3/h] *)
    rLimeDolomiteFeed_kgmin         : REAL;     (* Overhead Gravity Bunker Lime/Dolomitic Flux Feed Rate [kg/min] *)

    (* === ARC ACOUSTIC EMISSION INSTRUMENTATION [dB] === *)
    rArcAcousticEmission_dB         : REAL;     (* Furnace Shell High-Temperature Acoustic Microphone Sound Pressure Level [dB] *)

    (* === WATER-COOLED ROOF DELTA PANEL THERMAL PROTECTION [deg C, kW/m2, m3/h] === *)
    rRoofCoolingWaterTempInlet_degC : REAL;     (* Water-Cooled Roof Delta Panel Supply Water Temperature [deg C] *)
    rRoofCoolingWaterTempOutlet_degC: REAL;     (* Water-Cooled Roof Delta Panel Return Water Temperature [deg C] *)
    rRoofCoolingWaterFlow_m3h       : REAL;     (* Total Water-Cooled Roof Panel Circuit Volumetric Flow [m3/h] *)
    rRoofThermalFlux_Raw_A_kWm2     : REAL;     (* Roof Panel Heat Flux Sensor A Radiant Flux Density [kW/m2] *)
    rRoofThermalFlux_Raw_B_kWm2     : REAL;     (* Roof Panel Heat Flux Sensor B Radiant Flux Density [kW/m2] *)
    rRoofThermalFlux_Raw_C_kWm2     : REAL;     (* Roof Panel Heat Flux Sensor C Radiant Flux Density [kW/m2] *)

    (* === EAF DUCT OFF-GAS COMPOSITION SENSORS [%] === *)
    rOffgasCO_pct                   : REAL;     (* EAF Primary Exhaust Duct CO Volumetric Concentration [%] *)
    rOffgasCO2_pct                  : REAL;     (* EAF Primary Exhaust Duct CO2 Volumetric Concentration [%] *)
    rOffgasO2_pct                   : REAL;     (* EAF Primary Exhaust Duct Free O2 Volumetric Concentration [%] *)
END_VAR
""")

    # 3. VAR_OUTPUT
    parts.append("""VAR_OUTPUT
    (* === PROCESS ACTUATION COMMANDS & DEMAND SIGNALS === *)
    rCarbonFeedRateDemand_kgmin     : REAL;     (* Demanded Pulverized Carbon Injection Feed Rate [kg/min] *)
    rOxygenFlowDemand_Nm3h          : REAL;     (* Demanded Supersonic Oxygen Primary Flow Setpoint [Nm3/h] *)
    rLanceHeightDemand_mm           : REAL;     (* Demanded Co-Axial Lance Carriage Vertical Height Setpoint [mm] *)

    (* === DYNAMIC FOAMING SLAG METRIC ESTIMATES === *)
    rEstimatedSlagThickness_mm     : REAL;     (* 2oo3 Voted & Multi-Sensor Reconciled Dynamic Slag Thickness [mm] *)
    rSlagFoamingIndex_sec           : REAL;     (* Dynamic Slag Foaming Stability Index Sigma [s] *)
    rLancePenetrationRatio          : REAL;     (* Dimensionless Lance Jet Penetration Ratio (L_p / H_slag) [-] *)
    rArcSubmergenceFactor_pct       : REAL;     (* Composite Multi-Sensor Arc Slag Shielding Submergence Factor [%] *)
    rCalculatedRoofHeatFlux_kWm2    : REAL;     (* 2oo3 Voted & Calorimetrically Reconciled Roof Thermal Heat Flux [kW/m2] *)
    rEstimatedSlagFeO_pct           : REAL;     (* Discrete Observer Estimated Slag FeO Mass Concentration [%] *)

    (* === AUTOMATION & SAFETY SYSTEM STATUS DISCRETES === *)
    bSystemRunning                  : BOOL;     (* System Operating Normally in Automatic Slag Optimization Mode *)
    bSystemReady                    : BOOL;     (* All Pre-conditions, Permissives & Calibration Routines Healthy *)
    bSystemTripped                  : BOOL;     (* Critical Process Trip or Safety E-Stop Active *)
    bFoamOptimal_Ready              : BOOL;     (* Slag Foaming is Structurally Optimal (Arc Submerged > 90%) *)
    bRoofThermalAlert               : BOOL;     (* Water-Cooled Roof Delta Thermal Flux High Warning Active *)
    bEmergencyRetractDemand         : BOOL;     (* Failsafe High-Speed Lance Carriage Hoist Retract Command *)

    (* === 32-BIT BIT-PACKED TELEMETRY & ALARM WORDS === *)
    dwSystemStatusWord              : DWORD;    (* Bit-Packed Process States, Controller Modes & Active Interlocks *)
    dwAlarmWord1                    : DWORD;    (* Bit-Packed Critical Category-1 Safety & Thermal Process Alarms *)
    dwAlarmWord2                    : DWORD;    (* Bit-Packed Category-2 Instrument Diagnostic & 2oo3 Fault Alarms *)
    dwWarningWord                   : DWORD;    (* Bit-Packed Operational Advisory Warnings & Process Degradations *)
END_VAR
""")

    # 4. VAR - internal state matrices, constants, 2oo3 variables, MPC variables
    parts.append("""VAR
    (* ============================================================================================= *)
    (* DISCRETE STATE-SPACE MODEL MATRICES (Ts = 50 ms): x[k+1] = A*x[k] + B*u[k] + Bd*d[k]           *)
    (* States x: [1] H_slag [m], [2] FeO_pct [%], [3] Q_roof [kW/m2], [4] V_dot_CO [Nm3/s]          *)
    (* Inputs u: [1] Flow_O2 [Nm3/h], [2] Feed_C [kg/min], [3] Z_lance [mm]                          *)
    (* Disturb d: [1] Arc_Power [MW], [2] Lime_Feed [kg/min]                                         *)
    (* Outputs y: [1] H_slag [mm], [2] HDI [%], [3] Q_roof [kW/m2], [4] Attn_dB [dB]                *)
    (* ============================================================================================= *)
    aA_Matrix                       : ARRAY[1..4, 1..4] OF REAL := [
        [0.9850, -0.0120,  0.0000,  0.0450],   (* dx1/dt: Slag decay, FeO destabilization, CO bubble swell *)
        [0.0000,  0.9910,  0.0000, -0.0025],   (* dx2/dt: FeO slow chemical reduction dynamics *)
        [-0.0850, 0.0420,  0.9400,  0.0000],   (* dx3/dt: Roof flux dampening by foam height, radiant decay *)
        [0.0000,  0.0150,  0.0000,  0.8800]    (* dx4/dt: CO gas generation reaction kinetics *)
    ];

    aB_Matrix                       : ARRAY[1..4, 1..3] OF REAL := [
        [ 0.000045,  0.003800, -0.000085],     (* Input response on H_slag: O2 boost, Carbon feed, Lance depth *)
        [ 0.000082, -0.004100,  0.000010],     (* Input response on FeO: O2 oxidizes Fe, Carbon reduces FeO *)
        [ 0.008500, -0.155000,  0.002200],     (* Input response on Roof flux: Carbon lowers flux, O2 splash *)
        [ 0.000350,  0.028000, -0.000120]      (* Input response on CO rate: Stoichiometric combustion *)
    ];

    aBd_Matrix                      : ARRAY[1..4, 1..2] OF REAL := [
        [ 0.002500,  0.001800],                 (* Disturbance on H_slag: Arc thermal stir, Lime basicity *)
        [-0.000450, -0.001200],                 (* Disturbance on FeO: Arc reduction, Lime dilution *)
        [ 4.850000, -0.025000],                 (* Disturbance on Roof flux: Direct MW power radiation *)
        [ 0.008200,  0.000500]                  (* Disturbance on CO rate: Thermal kinetics acceleration *)
    ];

    aC_Matrix                       : ARRAY[1..4, 1..4] OF REAL := [
        [1000.0,    0.0,    0.0,    0.0],       (* y1: Slag thickness [mm] = 1000 * H_slag [m] *)
        [ -32.5,    0.85,   0.0,   -2.1],       (* y2: Harmonic Distortion Index HDI [%] *)
        [   0.0,    0.0,    1.0,    0.0],       (* y3: Roof Heat Flux [kW/m2] *)
        [  28.0,   -0.45,   0.0,    3.2]        (* y4: Acoustic Attenuation [dB] *)
    ];

    aD_Matrix                       : ARRAY[1..4, 1..3] OF REAL := [
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0]
    ];

    (* === STATE ESTIMATOR & KALMAN OBSERVER REGISTERS === *)
    aState_x                        : ARRAY[1..4] OF REAL := [0.150, 22.0, 180.0, 0.05]; (* Initial state *)
    aState_x_pred                   : ARRAY[1..4] OF REAL;
    aOutput_y_model                 : ARRAY[1..4] OF REAL;
    aOutput_y_meas                  : ARRAY[1..4] OF REAL;
    aResidual_y                     : ARRAY[1..4] OF REAL;
    aKalmanGain_L                   : ARRAY[1..4, 1..4] OF REAL := [
        [0.1250, -0.0012,  0.0001,  0.0025],
        [-0.0050, 0.0850, -0.0002, -0.0015],
        [-0.0850, 0.0250,  0.1850, -0.0150],
        [ 0.0120, -0.0045, 0.0001,  0.0950]
    ];

    (* === MODEL PREDICTIVE CONTROL (MPC) CONSTRAINED QUADRATIC OPTIMIZER === *)
    aMpcHessian_H                   : ARRAY[1..3, 1..3] OF REAL := [
        [0.000850,  0.000120, -0.000045],      (* H(1,1..3): O2 flow quadratic cost Hessian row *)
        [0.000120,  0.045000, -0.001850],      (* H(2,1..3): Carbon feed quadratic cost Hessian row *)
        [-0.000045, -0.001850,  0.001250]      (* H(3,1..3): Lance height quadratic cost Hessian row *)
    ];
    aMpcGradient_g                  : ARRAY[1..3] OF REAL;
    aMpcU_opt                       : ARRAY[1..3] OF REAL := [4200.0, 38.0, 1250.0]; (* Current solution *)
    aMpcU_prev                      : ARRAY[1..3] OF REAL := [4200.0, 38.0, 1250.0];
    aMpcU_target                    : ARRAY[1..3] OF REAL := [4200.0, 38.0, 1250.0];
    aMpcWeights_Q                   : ARRAY[1..4] OF REAL := [0.085, 0.450, 0.025, 0.150]; (* Output penalties *)
    aMpcWeights_R                   : ARRAY[1..3] OF REAL := [0.00025, 0.0120, 0.00085];   (* Actuator penalties *)
    aMpcWeights_DeltaR              : ARRAY[1..3] OF REAL := [0.00150, 0.0850, 0.00650];   (* Actuator rate penalties *)

    (* MPC Actuator Operational Boundaries *)
    rU1_O2_Min_Nm3h                 : REAL := 1200.0;
    rU1_O2_Max_Nm3h                 : REAL := 6200.0;
    rU1_O2_MaxSlew_Nm3h_s           : REAL := 450.0;

    rU2_Carbon_Min_kgmin            : REAL := 0.0;
    rU2_Carbon_Max_kgmin            : REAL := 75.0;
    rU2_Carbon_MaxSlew_kgmin_s      : REAL := 15.0;

    rU3_LanceZ_Min_mm               : REAL := 600.0;
    rU3_LanceZ_Max_mm               : REAL := 2200.0;
    rU3_LanceZ_MaxSlew_mm_s         : REAL := 80.0;

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) RADAR REGISTERS === *)
    rRadarDevThreshold_mm           : REAL := 75.0;  (* Max allowable radar channel inter-deviation [mm] *)
    rRadarSlewLimit_mm_s            : REAL := 250.0; (* Physical max surface velocity check [mm/s] *)
    rRadar_Prev_A_mm                : REAL := 3000.0;
    rRadar_Prev_B_mm                : REAL := 3000.0;
    rRadar_Prev_C_mm                : REAL := 3000.0;
    bRadar_A_Healthy                : BOOL := TRUE;
    bRadar_B_Healthy                : BOOL := TRUE;
    bRadar_C_Healthy                : BOOL := TRUE;
    bRadar_Degraded_1oo2            : BOOL := FALSE;
    bRadar_Complete_Failure         : BOOL := FALSE;
    rVotedRadarDistance_mm          : REAL := 2800.0;
    rFilteredRadarDistance_mm       : REAL := 2800.0;

    (* 24 GHz Microwave Radar Dielectric Compensation *)
    rDielectricPermittivity_eff     : REAL := 5.65;  (* Slag effective relative dielectric constant eps_eff *)
    rSteelBathBaseline_mm           : REAL := 3450.0; (* Furnace hearth steel bath top meniscus baseline [mm] *)
    rRadarRawSlagThickness_mm       : REAL := 550.0;

    (* === 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ROOF THERMAL FLUX REGISTERS === *)
    rFluxDevThreshold_kWm2          : REAL := 45.0;  (* Max allowable thermal flux inter-sensor deviation *)
    rFluxSlewLimit_kWm2_s           : REAL := 95.0;  (* Max radiant heat flux derivative limit *)
    rFlux_Prev_A_kWm2               : REAL := 120.0;
    rFlux_Prev_B_kWm2               : REAL := 120.0;
    rFlux_Prev_C_kWm2               : REAL := 120.0;
    bFlux_A_Healthy                 : BOOL := TRUE;
    bFlux_B_Healthy                 : BOOL := TRUE;
    bFlux_C_Healthy                 : BOOL := TRUE;
    bFlux_Degraded_1oo2             : BOOL := FALSE;
    bFlux_Complete_Failure          : BOOL := FALSE;
    rVotedThermalFlux_kWm2          : REAL := 120.0;
    rFilteredThermalFlux_kWm2       : REAL := 120.0;

    (* === ELECTRICAL HARMONIC DISTORTION & IMPEDANCE REGISTERS === *)
    rArcCurrent_RMS_kA              : REAL;
    rArcVoltage_RMS_V               : REAL;
    rArcImpedance_mOhm              : REAL;
    rArcResistance_mOhm             : REAL;
    rArcReactance_mOhm              : REAL;
    rHarmonic3rd_V_pct              : REAL;
    rHarmonic5th_V_pct              : REAL;
    rCalculatedHDI_pct              : REAL;
    rArcAcousticAttenuation_dB      : REAL;
    rBareArcBaselineAcoustic_dB     : REAL := 115.0; (* Bare arc acoustic reference emission level [dB] *)

    (* === CO-AXIAL SUPERSONIC COMPRESSIBLE FLUID JET CALCULATIONS === *)
    rLavalMachNumber                : REAL := 2.15;  (* Supersonic Laval nozzle expansion Mach number *)
    rO2SupplyPressure_bar           : REAL := 12.5;  (* Oxygen manifold upstream supply pressure [bar] *)
    rSupersonicCoreLength_mm        : REAL;
    rJetPenetrationDepth_Lp_mm      : REAL;
    rCalculatedPenetrationRatio     : REAL;
    rCarbonToOxygenStoichRatio      : REAL;

    (* === WATER-COOLED ROOF ENTHALPY CALORIMETRY === *)
    rWaterSpecificHeat_kJ_kgC       : REAL := 4.186; (* Isobaric specific heat capacity of cooling water *)
    rWaterDensity_kg_m3             : REAL := 990.0; (* Water density at operating temperature *)
    rRoofDeltaT_degC                : REAL;
    rRoofCalorimetricHeatLoad_MW    : REAL;
    rRoofCalorimetricFlux_kWm2      : REAL;
    rRoofEffectiveViewFactor        : REAL;

    (* === FINITE STATE MACHINE MANAGEMENT & CYCLE TIMERS === *)
    iState                          : INT := 0;      (* Active state index *)
    tStateTimer                     : TON;           (* Elapsed time in current operating state *)
    tDegradedTimer                  : TON;           (* Radar degradation confirmation delay timer *)
    tThermalSurgeTimer              : TON;           (* Roof thermal surge soak timer *)
    tEmergencyRetractTimer          : TON;           (* Lance emergency hoist timeout *)
    tPurgeTimer                     : TON;           (* Nitrogen / oxygen purge stabilization timer *)
    tSensorAlarmDebounceTimer       : TON;           (* Transducer diagnostic debounce timer *)

    (* === GENERAL ALGORITHMIC & MATRIX WORKSPACE REGISTERS === *)
    iRow                            : INT;
    iCol                            : INT;
    iIter                           : INT;
    rTempSum                        : REAL;
    rTempA                          : REAL;
    rTempB                          : REAL;
    rTempC                          : REAL;
    rGradStep                       : REAL := 0.085; (* Projected gradient descent step size *)
    rTargetSlagThickness_mm         : REAL := 620.0; (* Target foaming slag physical thickness [mm] *)
    rTargetPenetrationRatio         : REAL := 0.75;  (* Optimal penetration ratio setpoint *)
    rTargetRoofFlux_kWm2            : REAL := 110.0; (* Target ceiling radiant heat flux [kW/m2] *)

    (* === SAFETY TRIP & LATCHED INTERLOCK DISCRETES === *)
    bTripRoofThermalCritical        : BOOL := FALSE;
    bTripWaterCoolingFlowLow        : BOOL := FALSE;
    bTripWaterCoolingDeltaTHigh     : BOOL := FALSE;
    bTripLanceStallDetected         : BOOL := FALSE;
    bTripRadarPurgeLoss             : BOOL := FALSE;
    bTripCombustibleGasExplosionRisk: BOOL := FALSE;
END_VAR
""")

    # 5. Logic Section 1: Safety interlocks & E-Stop
    parts.append("""
(* ================================================================================================= *)
(* 1.0 CRITICAL SAFETY INTERLOCKS, EMERGENCY STOP & FAILSAFE DEPRESSURIZATION                         *)
(* ================================================================================================= *)
(* Verify hardware safety circuit continuity, cooling water flow permissive, and off-gas explosion  *)
(* margins. If any primary safety boundary is violated, the system triggers an emergency lance hoist,*)
(* shuts off supersonic oxygen, initiates inert purge, and latches Category-1 alarms.               *)

(* Calculate differential cooling water temperature across the water-cooled roof delta circuit *)
rRoofDeltaT_degC := rRoofCoolingWaterTempOutlet_degC - rRoofCoolingWaterTempInlet_degC;
IF rRoofDeltaT_degC < 0.0 THEN
    rRoofDeltaT_degC := 0.0;
END_IF;

(* Cooling Water Low Volumetric Flow Trip (< 650 m3/h baseline for 150-ton EAF delta roof) *)
IF (rRoofCoolingWaterFlow_m3h < 650.0) AND (iFurnaceHeatPhase > 0) THEN
    bTripWaterCoolingFlowLow := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* Bit 0: Roof Cooling Water Flow Low Trip *)
END_IF;

(* Cooling Water Delta T Critical Rise (> 28 deg C indicates nucleate boiling risk) *)
IF (rRoofDeltaT_degC > 28.0) AND (iFurnaceHeatPhase > 0) THEN
    bTripWaterCoolingDeltaTHigh := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Bit 1: Roof Water Delta T Critical High *)
END_IF;

(* Combustible Gas Deflagration Hazard: Simultaneous high CO (> 18%) and high free O2 (> 7.5%) in duct *)
IF (rOffgasCO_pct > 18.0) AND (rOffgasO2_pct > 7.5) THEN
    bTripCombustibleGasExplosionRisk := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Bit 2: Off-gas Explosion Hazard *)
END_IF;

(* FMCW Microwave Radar N2 Optical Purge Loss (< 18 Nm3/h risks immediate lens destruction by slag) *)
IF (rNitrogenPurgeFlow_Nm3h < 18.0) AND (iFurnaceHeatPhase > 0) THEN
    bTripRadarPurgeLoss := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Bit 3: Radar Waveguide Purge Flow Loss *)
END_IF;

(* Evaluate Global Safety Permissives and E-Stop Chain *)
IF (NOT bEmergencyStop) OR (NOT bSystemEnable) OR bTripWaterCoolingFlowLow OR
   bTripWaterCoolingDeltaTHigh OR bTripCombustibleGasExplosionRisk OR bTripRadarPurgeLoss THEN
    bSystemReady := FALSE;
    bSystemRunning := FALSE;
    bSystemTripped := TRUE;
    bEmergencyRetractDemand := TRUE;
    
    (* Force all chemical actuator demands to failsafe shutdown state *)
    rOxygenFlowDemand_Nm3h := 0.0;
    rCarbonFeedRateDemand_kgmin := 0.0;
    rLanceHeightDemand_mm := rU3_LanceZ_Max_mm; (* Fully hoisted park elevation *)
    
    iState := 100; (* Jump immediately to EMERGENCY PURGE & FAILSAFE TRIP STATE *)
END_IF;

(* Operator Fault Reset and Interlock Unlatching Sequence *)
IF bResetFaults AND bEmergencyStop AND bSystemEnable THEN
    IF (rRoofCoolingWaterFlow_m3h >= 650.0) THEN
        bTripWaterCoolingFlowLow := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0001;
    END_IF;
    IF (rRoofDeltaT_degC <= 22.0) THEN
        bTripWaterCoolingDeltaTHigh := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0002;
    END_IF;
    IF (rOffgasCO_pct <= 12.0) OR (rOffgasO2_pct <= 4.0) THEN
        bTripCombustibleGasExplosionRisk := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0004;
    END_IF;
    IF (rNitrogenPurgeFlow_Nm3h >= 22.0) THEN
        bTripRadarPurgeLoss := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0008;
    END_IF;
    IF bTripRoofThermalCritical AND (rCalculatedRoofHeatFlux_kWm2 < 250.0) THEN
        bTripRoofThermalCritical := FALSE;
        dwAlarmWord1 := dwAlarmWord1 AND NOT 16#0000_0010;
    END_IF;
    
    (* Clear master trip status if all Category-1 alarms are successfully cleared *)
    IF (dwAlarmWord1 = 16#0000_0000) THEN
        bSystemTripped := FALSE;
        bEmergencyRetractDemand := FALSE;
        IF (iState = 100) THEN
            iState := 0; (* Return to Idle State *)
        END_IF;
    END_IF;
END_IF;
""")

    # 6. Logic Section 2: 2oo3 TMR voting logic
    parts.append("""
(* ================================================================================================= *)
(* 2.0 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & SENSOR VALIDATION                               *)
(* ================================================================================================= *)
(* Evaluates 3 redundant 24 GHz FMCW Radar distance transceivers and 3 Roof Heat Flux transducers.    *)
(* Applies median voting, inter-channel deviation screening, and physical rate-of-change clamping.   *)

(* --- 2.1 FMCW MICROWAVE RADAR 2oo3 TMR PROCESSING --- *)
(* Individual Channel Slew Rate and Range Plausibility Checks *)
IF (rRadarDistance_Raw_A_mm < 1500.0) OR (rRadarDistance_Raw_A_mm > 4000.0) OR
   (ABS(rRadarDistance_Raw_A_mm - rRadar_Prev_A_mm) > (rRadarSlewLimit_mm_s * rCycleTime_sec)) THEN
    bRadar_A_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Radar A Outlier/Fault *)
ELSE
    bRadar_A_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0001;
END_IF;
rRadar_Prev_A_mm := rRadarDistance_Raw_A_mm;

IF (rRadarDistance_Raw_B_mm < 1500.0) OR (rRadarDistance_Raw_B_mm > 4000.0) OR
   (ABS(rRadarDistance_Raw_B_mm - rRadar_Prev_B_mm) > (rRadarSlewLimit_mm_s * rCycleTime_sec)) THEN
    bRadar_B_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* Radar B Outlier/Fault *)
ELSE
    bRadar_B_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0002;
END_IF;
rRadar_Prev_B_mm := rRadarDistance_Raw_B_mm;

IF (rRadarDistance_Raw_C_mm < 1500.0) OR (rRadarDistance_Raw_C_mm > 4000.0) OR
   (ABS(rRadarDistance_Raw_C_mm - rRadar_Prev_C_mm) > (rRadarSlewLimit_mm_s * rCycleTime_sec)) THEN
    bRadar_C_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* Radar C Outlier/Fault *)
ELSE
    bRadar_C_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0004;
END_IF;
rRadar_Prev_C_mm := rRadarDistance_Raw_C_mm;

(* 2oo3 Median Voter & Inter-Channel Deviation Logic *)
IF bRadar_A_Healthy AND bRadar_B_Healthy AND bRadar_C_Healthy THEN
    bRadar_Degraded_1oo2 := FALSE;
    bRadar_Complete_Failure := FALSE;
    
    (* Median Selection Algorithm among 3 Healthy Channels *)
    IF ((rRadarDistance_Raw_A_mm >= rRadarDistance_Raw_B_mm) AND (rRadarDistance_Raw_A_mm <= rRadarDistance_Raw_C_mm)) OR
       ((rRadarDistance_Raw_A_mm <= rRadarDistance_Raw_B_mm) AND (rRadarDistance_Raw_A_mm >= rRadarDistance_Raw_C_mm)) THEN
        rVotedRadarDistance_mm := rRadarDistance_Raw_A_mm;
    ELSIF ((rRadarDistance_Raw_B_mm >= rRadarDistance_Raw_A_mm) AND (rRadarDistance_Raw_B_mm <= rRadarDistance_Raw_C_mm)) OR
          ((rRadarDistance_Raw_B_mm <= rRadarDistance_Raw_A_mm) AND (rRadarDistance_Raw_B_mm >= rRadarDistance_Raw_C_mm)) THEN
        rVotedRadarDistance_mm := rRadarDistance_Raw_B_mm;
    ELSE
        rVotedRadarDistance_mm := rRadarDistance_Raw_C_mm;
    END_IF;
    
    (* Cross-channel spread consistency verification *)
    IF (ABS(rRadarDistance_Raw_A_mm - rRadarDistance_Raw_B_mm) > rRadarDevThreshold_mm) OR
       (ABS(rRadarDistance_Raw_B_mm - rRadarDistance_Raw_C_mm) > rRadarDevThreshold_mm) OR
       (ABS(rRadarDistance_Raw_A_mm - rRadarDistance_Raw_C_mm) > rRadarDevThreshold_mm) THEN
        dwWarningWord := dwWarningWord OR 16#0000_0001; (* Radar 2oo3 Channel Deviation Spread Warning *)
    ELSE
        dwWarningWord := dwWarningWord AND NOT 16#0000_0001;
    END_IF;

ELSIF bRadar_A_Healthy AND bRadar_B_Healthy THEN
    bRadar_Degraded_1oo2 := TRUE;
    bRadar_Complete_Failure := FALSE;
    rVotedRadarDistance_mm := (rRadarDistance_Raw_A_mm + rRadarDistance_Raw_B_mm) * 0.5;
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* Radar Operating in Degraded 1oo2 Mode *)

ELSIF bRadar_B_Healthy AND bRadar_C_Healthy THEN
    bRadar_Degraded_1oo2 := TRUE;
    bRadar_Complete_Failure := FALSE;
    rVotedRadarDistance_mm := (rRadarDistance_Raw_B_mm + rRadarDistance_Raw_C_mm) * 0.5;
    dwWarningWord := dwWarningWord OR 16#0000_0002;

ELSIF bRadar_A_Healthy AND bRadar_C_Healthy THEN
    bRadar_Degraded_1oo2 := TRUE;
    bRadar_Complete_Failure := FALSE;
    rVotedRadarDistance_mm := (rRadarDistance_Raw_A_mm + rRadarDistance_Raw_C_mm) * 0.5;
    dwWarningWord := dwWarningWord OR 16#0000_0002;

ELSE
    (* All or 2-out-of-3 radar transceivers failed: activate acoustic-impedance fallback *)
    bRadar_Degraded_1oo2 := FALSE;
    bRadar_Complete_Failure := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0008; (* Radar Tri-Channel Complete Failure *)
END_IF;

(* First-Order Low-Pass Butterworth Filter on Distance Signal: cutoff fc = 2.0 Hz *)
rFilteredRadarDistance_mm := rFilteredRadarDistance_mm + 
    (0.385 * (rVotedRadarDistance_mm - rFilteredRadarDistance_mm));

(* --- 2.2 WATER-COOLED ROOF THERMAL FLUX 2oo3 TMR PROCESSING --- *)
IF (rRoofThermalFlux_Raw_A_kWm2 < 10.0) OR (rRoofThermalFlux_Raw_A_kWm2 > 500.0) OR
   (ABS(rRoofThermalFlux_Raw_A_kWm2 - rFlux_Prev_A_kWm2) > (rFluxSlewLimit_kWm2_s * rCycleTime_sec)) THEN
    bFlux_A_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0010;
ELSE
    bFlux_A_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0010;
END_IF;
rFlux_Prev_A_kWm2 := rRoofThermalFlux_Raw_A_kWm2;

IF (rRoofThermalFlux_Raw_B_kWm2 < 10.0) OR (rRoofThermalFlux_Raw_B_kWm2 > 500.0) OR
   (ABS(rRoofThermalFlux_Raw_B_kWm2 - rFlux_Prev_B_kWm2) > (rFluxSlewLimit_kWm2_s * rCycleTime_sec)) THEN
    bFlux_B_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0020;
ELSE
    bFlux_B_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0020;
END_IF;
rFlux_Prev_B_kWm2 := rRoofThermalFlux_Raw_B_kWm2;

IF (rRoofThermalFlux_Raw_C_kWm2 < 10.0) OR (rRoofThermalFlux_Raw_C_kWm2 > 500.0) OR
   (ABS(rRoofThermalFlux_Raw_C_kWm2 - rFlux_Prev_C_kWm2) > (rFluxSlewLimit_kWm2_s * rCycleTime_sec)) THEN
    bFlux_C_Healthy := FALSE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0040;
ELSE
    bFlux_C_Healthy := TRUE;
    dwAlarmWord2 := dwAlarmWord2 AND NOT 16#0000_0040;
END_IF;
rFlux_Prev_C_kWm2 := rRoofThermalFlux_Raw_C_kWm2;

(* Median Selection for Thermal Radiant Heat Flux *)
IF bFlux_A_Healthy AND bFlux_B_Healthy AND bFlux_C_Healthy THEN
    bFlux_Degraded_1oo2 := FALSE;
    bFlux_Complete_Failure := FALSE;
    IF ((rRoofThermalFlux_Raw_A_kWm2 >= rRoofThermalFlux_Raw_B_kWm2) AND (rRoofThermalFlux_Raw_A_kWm2 <= rRoofThermalFlux_Raw_C_kWm2)) OR
       ((rRoofThermalFlux_Raw_A_kWm2 <= rRoofThermalFlux_Raw_B_kWm2) AND (rRoofThermalFlux_Raw_A_kWm2 >= rRoofThermalFlux_Raw_C_kWm2)) THEN
        rVotedThermalFlux_kWm2 := rRoofThermalFlux_Raw_A_kWm2;
    ELSIF ((rRoofThermalFlux_Raw_B_kWm2 >= rRoofThermalFlux_Raw_A_kWm2) AND (rRoofThermalFlux_Raw_B_kWm2 <= rRoofThermalFlux_Raw_C_kWm2)) OR
          ((rRoofThermalFlux_Raw_B_kWm2 <= rRoofThermalFlux_Raw_A_kWm2) AND (rRoofThermalFlux_Raw_B_kWm2 >= rRoofThermalFlux_Raw_C_kWm2)) THEN
        rVotedThermalFlux_kWm2 := rRoofThermalFlux_Raw_B_kWm2;
    ELSE
        rVotedThermalFlux_kWm2 := rRoofThermalFlux_Raw_C_kWm2;
    END_IF;
ELSIF bFlux_A_Healthy AND bFlux_B_Healthy THEN
    bFlux_Degraded_1oo2 := TRUE;
    rVotedThermalFlux_kWm2 := (rRoofThermalFlux_Raw_A_kWm2 + rRoofThermalFlux_Raw_B_kWm2) * 0.5;
ELSIF bFlux_B_Healthy AND bFlux_C_Healthy THEN
    bFlux_Degraded_1oo2 := TRUE;
    rVotedThermalFlux_kWm2 := (rRoofThermalFlux_Raw_B_kWm2 + rRoofThermalFlux_Raw_C_kWm2) * 0.5;
ELSIF bFlux_A_Healthy AND bFlux_C_Healthy THEN
    bFlux_Degraded_1oo2 := TRUE;
    rVotedThermalFlux_kWm2 := (rRoofThermalFlux_Raw_A_kWm2 + rRoofThermalFlux_Raw_C_kWm2) * 0.5;
ELSE
    bFlux_Complete_Failure := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0080;
END_IF;

rFilteredThermalFlux_kWm2 := rFilteredThermalFlux_kWm2 + 
    (0.250 * (rVotedThermalFlux_kWm2 - rFilteredThermalFlux_kWm2));
""")

    # 7. Logic Section 3: Radar Dielectric & Physical Thickness profiling
    parts.append("""
(* ================================================================================================= *)
(* 3.0 24 GHz FMCW MICROWAVE RADAR DIELECTRIC & SLAG THICKNESS PROFILING                             *)
(* ================================================================================================= *)
(* Converts electromagnetic echo distance to true physical slag thickness by computing the dynamic  *)
(* dielectric constant of the foaming slag matrix based on temperature, basicity, and void fraction.*)

(* Dielectric Permittivity Model: Liquid slag eps_solid ~ 8.2; CO foam void fraction phi = 0.65-0.85 *)
(* Bruggeman effective medium approximation: eps_eff = eps_slag * (1 - phi)^(3/2)                  *)
(* In practice, higher slag foaming lowers effective permittivity towards eps_eff ~ 3.5 to 5.8      *)
IF (aState_x[1] > 0.400) THEN
    (* Thick foaming slag: higher gas void fraction, lower effective permittivity *)
    rDielectricPermittivity_eff := 4.20 + (0.05 * aState_x[2]); (* Modulated slightly by FeO content *)
ELSE
    (* Dense/collapsed slag: lower void fraction, higher permittivity *)
    rDielectricPermittivity_eff := 6.50 - (2.5 * aState_x[1]);
END_IF;

IF rDielectricPermittivity_eff < 2.5 THEN
    rDielectricPermittivity_eff := 2.5;
END_IF;
IF rDielectricPermittivity_eff > 9.0 THEN
    rDielectricPermittivity_eff := 9.0;
END_IF;

(* Raw Slag Thickness: Difference between static hearth steel meniscus and radar reflection surface *)
rRadarRawSlagThickness_mm := (rSteelBathBaseline_mm - rFilteredRadarDistance_mm) * SQRT(rDielectricPermittivity_eff) * 0.485;

(* Physical Clamping of radar slag thickness to furnace mechanical bounds (0 to 1200 mm) *)
IF rRadarRawSlagThickness_mm < 0.0 THEN
    rRadarRawSlagThickness_mm := 0.0;
END_IF;
IF rRadarRawSlagThickness_mm > 1200.0 THEN
    rRadarRawSlagThickness_mm := 1200.0;
END_IF;
""")

    # 8. Logic Section 4: Electrical Harmonic Impedance & Acoustic Fusion
    parts.append("""
(* ================================================================================================= *)
(* 4.0 ARC ELECTRICAL HARMONIC IMPEDANCE & ACOUSTIC EMISSION SENSOR FUSION                           *)
(* ================================================================================================= *)
(* Evaluates 3-phase arc current, voltage, active power, impedance modulus, and voltage harmonic      *)
(* distortion (HDI). Fuses acoustic sound pressure attenuation to quantify arc slag submergence.     *)

(* 3-Phase Symmetric Component Averages *)
rArcCurrent_RMS_kA := (rArcCurrent_PhaseA_kA + rArcCurrent_PhaseB_kA + rArcCurrent_PhaseC_kA) / 3.0;
rArcVoltage_RMS_V  := (rArcVoltage_PhaseA_V + rArcVoltage_PhaseB_V + rArcVoltage_PhaseC_V) / 3.0;

(* Calculate Arc Impedance, Resistance, and Reactance *)
IF rArcCurrent_RMS_kA > 5.0 THEN
    rArcImpedance_mOhm := (rArcVoltage_RMS_V / (rArcCurrent_RMS_kA * 1000.0)) * 1000.0;
    
    (* Real resistance derived from Active MW Power: P = 3 * I^2 * R *)
    rArcResistance_mOhm := ((rActiveElectricalPower_MW * 1.0E6) / (3.0 * (rArcCurrent_RMS_kA * 1000.0) * (rArcCurrent_RMS_kA * 1000.0))) * 1000.0;
    
    (* Reactance via Pythagorean quadrature: X = SQRT(Z^2 - R^2) *)
    IF rArcImpedance_mOhm > rArcResistance_mOhm THEN
        rArcReactance_mOhm := SQRT((rArcImpedance_mOhm * rArcImpedance_mOhm) - (rArcResistance_mOhm * rArcResistance_mOhm));
    ELSE
        rArcReactance_mOhm := 1.20; (* Baseline secondary loop transformer/bus reactance *)
    END_IF;
ELSE
    rArcImpedance_mOhm := 15.0;
    rArcResistance_mOhm := 10.0;
    rArcReactance_mOhm := 5.0;
END_IF;

(* Voltage Harmonic Distortion Estimation (Odd 3rd and 5th harmonics signify arc non-linearity) *)
(* In open arc, restrikes produce high 3rd harmonic (18-25%); under foam, it decays to < 4%     *)
IF rArcResistance_mOhm > 0.5 THEN
    rHarmonic3rd_V_pct := 22.5 * EXP(-3.5 * aState_x[1]) + (0.12 * aState_x[2]);
    rHarmonic5th_V_pct := 11.2 * EXP(-4.0 * aState_x[1]);
    rCalculatedHDI_pct := SQRT((rHarmonic3rd_V_pct * rHarmonic3rd_V_pct) + (rHarmonic5th_V_pct * rHarmonic5th_V_pct));
ELSE
    rCalculatedHDI_pct := 24.0;
END_IF;

(* Acoustic Sound Pressure Level Attenuation Index *)
(* Bare arc acoustic emission is ~115 dB. Foaming slag acts as an acoustic muffler. *)
rArcAcousticAttenuation_dB := rBareArcBaselineAcoustic_dB - rArcAcousticEmission_dB;
IF rArcAcousticAttenuation_dB < 0.0 THEN
    rArcAcousticAttenuation_dB := 0.0;
END_IF;
IF rArcAcousticAttenuation_dB > 28.0 THEN
    rArcAcousticAttenuation_dB := 28.0;
END_IF;

(* Composite Arc Submergence Factor Synthesis (0 to 100%) *)
(* Weighted fusion: 50% Radar thickness, 30% Acoustic attenuation, 20% Electrical HDI *)
IF NOT bRadar_Complete_Failure THEN
    rArcSubmergenceFactor_pct := (0.50 * (rRadarRawSlagThickness_mm / 6.0)) + 
                                 (0.30 * (rArcAcousticAttenuation_dB * 5.0)) + 
                                 (0.20 * (100.0 - (rCalculatedHDI_pct * 4.0)));
ELSE
    (* Fallback Mode: Radar offline -> Rely 60% on Acoustic and 40% on Electrical HDI *)
    rArcSubmergenceFactor_pct := (0.60 * (rArcAcousticAttenuation_dB * 5.0)) + 
                                 (0.40 * (100.0 - (rCalculatedHDI_pct * 4.0)));
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* Virtual Submergence Fallback Active *)
END_IF;

IF rArcSubmergenceFactor_pct < 0.0 THEN
    rArcSubmergenceFactor_pct := 0.0;
END_IF;
IF rArcSubmergenceFactor_pct > 100.0 THEN
    rArcSubmergenceFactor_pct := 100.0;
END_IF;

(* Optimal Foaming Status Discrete: Arc submerged >= 88% and thickness >= 500 mm *)
bFoamOptimal_Ready := (rArcSubmergenceFactor_pct >= 88.0) AND (aState_x[1] >= 0.500);
""")

    # 9. Logic Section 5: State-Space Kalman Observer
    parts.append("""
(* ================================================================================================= *)
(* 5.0 COMPLETE STATE-SPACE (A,B,Bd,C,D) KALMAN FILTER OBSERVER & METALLURGICAL KINETICS            *)
(* ================================================================================================= *)
(* Discrete Time Execution (Ts = 50 ms): Propagates internal physical states, evaluates innovation   *)
(* residuals, and applies Kalman correction gains. Estimates unmeasurable slag FeO concentration.    *)

(* Assemble Current Input Vector u[k] *)
aInput_u[1] := rOxygenFlow_Actual_Nm3h;
aInput_u[2] := rCarbonInjectionFlow_Actual_kgmin;
aInput_u[3] := rLanceElevation_Current_mm;

(* Assemble Disturbance Vector d[k] *)
aDisturb_d[1] := rActiveElectricalPower_MW;
aDisturb_d[2] := rLimeDolomiteFeed_kgmin;

(* Assemble Real Measured Output Vector y_meas[k] *)
IF NOT bRadar_Complete_Failure THEN
    aOutput_y_meas[1] := rRadarRawSlagThickness_mm;
ELSE
    (* Virtual fallback measurement based on acoustic/impedance proxy *)
    aOutput_y_meas[1] := rArcSubmergenceFactor_pct * 6.2;
END_IF;
aOutput_y_meas[2] := rCalculatedHDI_pct;
aOutput_y_meas[3] := rFilteredThermalFlux_kWm2;
aOutput_y_meas[4] := rArcAcousticAttenuation_dB;

(* --- STEP 1: PRIOR STATE PREDICTION: x_pred = A * x[k] + B * u[k] + Bd * d[k] --- *)
FOR iRow := 1 TO 4 DO
    rTempSum := 0.0;
    (* State transition matrix product: A * x *)
    FOR iCol := 1 TO 4 DO
        rTempSum := rTempSum + (aA_Matrix[iRow, iCol] * aState_x[iCol]);
    END_FOR;
    (* Control input matrix product: B * u *)
    FOR iCol := 1 TO 3 DO
        rTempSum := rTempSum + (aB_Matrix[iRow, iCol] * aInput_u[iCol]);
    END_FOR;
    (* Disturbance matrix product: Bd * d *)
    FOR iCol := 1 TO 2 DO
        rTempSum := rTempSum + (aBd_Matrix[iRow, iCol] * aDisturb_d[iCol]);
    END_FOR;
    aState_x_pred[iRow] := rTempSum;
END_FOR;

(* --- STEP 2: MODEL OUTPUT PREDICTION: y_model = C * x_pred --- *)
FOR iRow := 1 TO 4 DO
    rTempSum := 0.0;
    FOR iCol := 1 TO 4 DO
        rTempSum := rTempSum + (aC_Matrix[iRow, iCol] * aState_x_pred[iCol]);
    END_FOR;
    aOutput_y_model[iRow] := rTempSum;
    (* Calculate Innovation Residual *)
    aResidual_y[iRow] := aOutput_y_meas[iRow] - aOutput_y_model[iRow];
END_FOR;

(* --- STEP 3: MEASUREMENT UPDATE & POSTERIOR CORRECTION: x[k+1] = x_pred + L * residual --- *)
FOR iRow := 1 TO 4 DO
    rTempSum := aState_x_pred[iRow];
    FOR iCol := 1 TO 4 DO
        rTempSum := rTempSum + (aKalmanGain_L[iRow, iCol] * aResidual_y[iCol]);
    END_FOR;
    
    (* Physical State Saturation & Feasibility Bounds *)
    IF (iRow = 1) THEN (* Slag Thickness x1 [m]: 0.05 to 1.20 m *)
        IF rTempSum < 0.050 THEN rTempSum := 0.050; END_IF;
        IF rTempSum > 1.200 THEN rTempSum := 1.200; END_IF;
    ELSIF (iRow = 2) THEN (* Slag FeO x2 [%]: 8.0% to 45.0% *)
        IF rTempSum < 8.0 THEN rTempSum := 8.0; END_IF;
        IF rTempSum > 45.0 THEN rTempSum := 45.0; END_IF;
    ELSIF (iRow = 3) THEN (* Roof Heat Flux x3 [kW/m2]: 20.0 to 480.0 kW/m2 *)
        IF rTempSum < 20.0 THEN rTempSum := 20.0; END_IF;
        IF rTempSum > 480.0 THEN rTempSum := 480.0; END_IF;
    ELSIF (iRow = 4) THEN (* CO Generation Rate x4 [Nm3/s]: 0.0 to 2.50 Nm3/s *)
        IF rTempSum < 0.0 THEN rTempSum := 0.0; END_IF;
        IF rTempSum > 2.50 THEN rTempSum := 2.50; END_IF;
    END_IF;
    
    aState_x[iRow] := rTempSum;
END_FOR;

(* Update Output Registers from Observer States *)
rEstimatedSlagThickness_mm := aState_x[1] * 1000.0;
rEstimatedSlagFeO_pct       := aState_x[2];

(* Dynamic Slag Foaming Stability Index Sigma [s]: Ratio of foam height to superficial gas velocity *)
IF aState_x[4] > 0.010 THEN
    (* Furnace hearth cross-sectional bath area A_bath ~ 36.3 m2 (for 150-ton EAF) *)
    rSlagFoamingIndex_sec := aState_x[1] / (aState_x[4] / 36.3);
    IF rSlagFoamingIndex_sec > 45.0 THEN rSlagFoamingIndex_sec := 45.0; END_IF;
ELSE
    rSlagFoamingIndex_sec := 1.5;
END_IF;
""")

    # 10. Logic Section 6: Co-Axial Supersonic Lance Penetration Hydrodynamics
    parts.append("""
(* ================================================================================================= *)
(* 6.0 SUPERSONIC CO-AXIAL LANCE PENETRATION & COMBUSTION KINETICS                                   *)
(* ================================================================================================= *)
(* Calculates compressible Laval nozzle jet expansion, supersonic potential core length, and cavity *)
(* penetration depth L_p in molten slag. Enforces dynamic Penetration Ratio PR in [0.65, 0.85].      *)

(* Supersonic Oxygen Jet Core Length (Mach 2.15 Laval nozzle, throat diameter dt = 38 mm) *)
(* Annular pulverized carbon carrier co-axial shroud extends core length by 35% *)
rSupersonicCoreLength_mm := 4.2 * 38.0 * (1.0 + (0.38 * (rLavalMachNumber - 1.0))) * 1.35 * 10.0;

(* Oxygen Supply Pressure Ratio relative to atmospheric furnace backpressure (P_atm ~ 1.013 bar) *)
rNozzlePressureRatio := rO2SupplyPressure_bar / 1.013;

(* Penetration Depth L_p [mm] via modified Koria-Lange & Banks Formulation: *)
(* L_p = K * (P_O2 / P_atm)^0.58 * (dt / sin(theta)) * SQRT(rho_jet / rho_slag) * (1 + beta_shroud) *)
(* Lance angle theta = 42 deg to horizontal -> sin(theta) = 0.669 *)
IF (rOxygenFlow_Actual_Nm3h > 500.0) THEN
    rJetPenetrationDepth_Lp_mm := 0.046 * EXPT(rNozzlePressureRatio, 0.58) * (38.0 / 0.669) * 
                                  SQRT(1.42 / 2400.0) * 1000.0 * 1.32;
    
    (* Subtract standoff distance if lance carriage is elevated above slag top surface *)
    IF (rLanceElevation_Current_mm > rEstimatedSlagThickness_mm) THEN
        rJetPenetrationDepth_Lp_mm := rJetPenetrationDepth_Lp_mm - 
            (0.35 * (rLanceElevation_Current_mm - rEstimatedSlagThickness_mm));
    END_IF;
    
    IF rJetPenetrationDepth_Lp_mm < 50.0 THEN
        rJetPenetrationDepth_Lp_mm := 50.0;
    END_IF;
ELSE
    rJetPenetrationDepth_Lp_mm := 0.0;
END_IF;

(* Dimensionless Penetration Ratio: PR = L_p / H_slag *)
IF rEstimatedSlagThickness_mm > 80.0 THEN
    rCalculatedPenetrationRatio := rJetPenetrationDepth_Lp_mm / rEstimatedSlagThickness_mm;
ELSE
    rCalculatedPenetrationRatio := 0.30;
END_IF;
rLancePenetrationRatio := rCalculatedPenetrationRatio;

(* Evaluate Penetration Quality Warnings *)
IF (rCalculatedPenetrationRatio < 0.60) AND (iFurnaceHeatPhase >= 2) AND (iState = 50) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* Lance Under-Penetrating Slag Layer *)
    dwWarningWord := dwWarningWord AND NOT 16#0000_0010;
ELSIF (rCalculatedPenetrationRatio > 0.88) AND (iFurnaceHeatPhase >= 2) AND (iState = 50) THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* Lance Over-Penetrating: Bath Impingement Hazard *)
    dwWarningWord := dwWarningWord AND NOT 16#0000_0008;
ELSE
    dwWarningWord := dwWarningWord AND NOT 16#0000_0018; (* Clear both penetration warnings *)
END_IF;

(* Stoichiometric Carbon-to-Oxygen Mass Combustion Ratio: C + 0.5 O2 -> CO *)
(* Theoretical: 12 kg C reacts with 0.5 kmol O2 (11.2 Nm3) -> 1.07 kg C / Nm3 O2 *)
IF rOxygenFlow_Actual_Nm3h > 100.0 THEN
    rCarbonToOxygenStoichRatio := (rCarbonInjectionFlow_Actual_kgmin * 60.0) / rOxygenFlow_Actual_Nm3h;
ELSE
    rCarbonToOxygenStoichRatio := 0.0;
END_IF;
""")

    # 11. Logic Section 7: MPC Optimizer
    parts.append("""
(* ================================================================================================= *)
(* 7.0 MODEL PREDICTIVE CONTROL (MPC) CONSTRAINED QUADRATIC PROGRAMMING OPTIMIZER                     *)
(* ================================================================================================= *)
(* Solves real-time quadratic cost J = 0.5 * u^T * H * u + g^T * u subject to hard actuator limits    *)
(* and rate-of-change (slew) constraints using a 15-iteration projected gradient descent method.     *)

IF (iState = 50) OR (iState = 40) OR (iState = 60) THEN
    (* Compute Linear Gradient Vector g = S_u^T * Q * (y_pred - y_target) + R * u_prev *)
    (* Target Tracking: y1_target = rTargetSlagThickness_mm, y3_target = rTargetRoofFlux_kWm2 *)
    aMpcGradient_g[1] := (aMpcWeights_Q[1] * (aOutput_y_model[1] - rTargetSlagThickness_mm) * 0.0015) +
                         (aMpcWeights_Q[3] * (aOutput_y_model[3] - rTargetRoofFlux_kWm2) * 0.0045) +
                         (aMpcWeights_R[1] * aMpcU_opt[1]);

    aMpcGradient_g[2] := (aMpcWeights_Q[1] * (aOutput_y_model[1] - rTargetSlagThickness_mm) * -0.0450) +
                         (aMpcWeights_Q[2] * (aState_x[2] - 18.0) * 0.120) + (* Target FeO ~ 18% *)
                         (aMpcWeights_Q[3] * (aOutput_y_model[3] - rTargetRoofFlux_kWm2) * -0.0650) +
                         (aMpcWeights_R[2] * aMpcU_opt[2]);

    aMpcGradient_g[3] := (aMpcWeights_Q[1] * (rCalculatedPenetrationRatio - rTargetPenetrationRatio) * 45.0) +
                         (aMpcWeights_R[3] * (aMpcU_opt[3] - 1200.0) * 0.002);

    (* Projected Gradient Descent Iteration Loop (12 Iterations per PLC scan) *)
    FOR iIter := 1 TO 12 DO
        FOR iRow := 1 TO 3 DO
            (* Compute matrix-vector product: [H * u] *)
            rTempSum := 0.0;
            FOR iCol := 1 TO 3 DO
                rTempSum := rTempSum + (aMpcHessian_H[iRow, iCol] * aMpcU_opt[iCol]);
            END_FOR;
            
            (* Unconstrained gradient update: u_new = u - alpha * (H*u + g) *)
            rTempSum := aMpcU_opt[iRow] - (rGradStep * (rTempSum + aMpcGradient_g[iRow]));
            
            (* --- PROJECTION ONTO FEASIBLE ACTUATOR BOUNDS --- *)
            IF (iRow = 1) THEN (* Actuator 1: Supersonic Oxygen Flow [Nm3/h] *)
                (* Slew Rate Clamping relative to previous scan *)
                IF (rTempSum - aMpcU_prev[1]) > (rU1_O2_MaxSlew_Nm3h_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[1] + (rU1_O2_MaxSlew_Nm3h_s * rCycleTime_sec);
                ELSIF (aMpcU_prev[1] - rTempSum) > (rU1_O2_MaxSlew_Nm3h_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[1] - (rU1_O2_MaxSlew_Nm3h_s * rCycleTime_sec);
                END_IF;
                (* Hard Amplitude Clamping *)
                IF rTempSum < rU1_O2_Min_Nm3h THEN rTempSum := rU1_O2_Min_Nm3h; END_IF;
                IF rTempSum > rU1_O2_Max_Nm3h THEN rTempSum := rU1_O2_Max_Nm3h; END_IF;
                
            ELSIF (iRow = 2) THEN (* Actuator 2: Pulverized Carbon Feed [kg/min] *)
                IF (rTempSum - aMpcU_prev[2]) > (rU2_Carbon_MaxSlew_kgmin_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[2] + (rU2_Carbon_MaxSlew_kgmin_s * rCycleTime_sec);
                ELSIF (aMpcU_prev[2] - rTempSum) > (rU2_Carbon_MaxSlew_kgmin_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[2] - (rU2_Carbon_MaxSlew_kgmin_s * rCycleTime_sec);
                END_IF;
                IF rTempSum < rU2_Carbon_Min_kgmin THEN rTempSum := rU2_Carbon_Min_kgmin; END_IF;
                IF rTempSum > rU2_Carbon_Max_kgmin THEN rTempSum := rU2_Carbon_Max_kgmin; END_IF;
                
            ELSIF (iRow = 3) THEN (* Actuator 3: Lance Elevation Z_lance [mm] *)
                IF (rTempSum - aMpcU_prev[3]) > (rU3_LanceZ_MaxSlew_mm_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[3] + (rU3_LanceZ_MaxSlew_mm_s * rCycleTime_sec);
                ELSIF (aMpcU_prev[3] - rTempSum) > (rU3_LanceZ_MaxSlew_mm_s * rCycleTime_sec) THEN
                    rTempSum := aMpcU_prev[3] - (rU3_LanceZ_MaxSlew_mm_s * rCycleTime_sec);
                END_IF;
                IF rTempSum < rU3_LanceZ_Min_mm THEN rTempSum := rU3_LanceZ_Min_mm; END_IF;
                IF rTempSum > rU3_LanceZ_Max_mm THEN rTempSum := rU3_LanceZ_Max_mm; END_IF;
            END_IF;
            
            aMpcU_opt[iRow] := rTempSum;
        END_FOR;
    END_FOR;
    
    (* Store optimal vector for subsequent scan slew limiting *)
    aMpcU_prev := aMpcU_opt;
    
    (* Transfer MPC Demands to Output Command Ports *)
    rOxygenFlowDemand_Nm3h      := aMpcU_opt[1];
    rCarbonFeedRateDemand_kgmin := aMpcU_opt[2];
    rLanceHeightDemand_mm       := aMpcU_opt[3];
END_IF;
""")

    # 12. Logic Section 8: Roof Thermal Protection & Derate
    parts.append("""
(* ================================================================================================= *)
(* 8.0 WATER-COOLED ROOF THERMAL FLUX PROTECTION & DERATE MANAGEMENT                                *)
(* ================================================================================================= *)
(* Reconciles 2oo3 thermal flux sensors with water enthalpy calorimetry. Protects tubular panels     *)
(* against departure from nucleate boiling (DNB) with a dual-stage safety threshold.                 *)

(* Enthalpy Calorimetry: P_roof [MW] = Q_water [m3/h] * rho [kg/m3] * Cp [kJ/kg.C] * Delta_T / 3.6E6 *)
IF rRoofCoolingWaterFlow_m3h > 100.0 THEN
    rRoofCalorimetricHeatLoad_MW := (rRoofCoolingWaterFlow_m3h * rWaterDensity_kg_m3 * 
                                     rWaterSpecificHeat_kJ_kgC * rRoofDeltaT_degC) / 3600000.0;
    
    (* Roof delta projected area A_roof ~ 28.5 m2 for 150-ton furnace *)
    rRoofCalorimetricFlux_kWm2 := (rRoofCalorimetricHeatLoad_MW * 1000.0) / 28.5;
ELSE
    rRoofCalorimetricHeatLoad_MW := 0.0;
    rRoofCalorimetricFlux_kWm2 := 0.0;
END_IF;

(* Reconcile 2oo3 Sensor measurement with Calorimetric Enthalpy Balance *)
IF NOT bFlux_Complete_Failure THEN
    rCalculatedRoofHeatFlux_kWm2 := (0.75 * rFilteredThermalFlux_kWm2) + (0.25 * rRoofCalorimetricFlux_kWm2);
ELSE
    (* Fallback strictly to calorimetry if all flux transducers fail *)
    rCalculatedRoofHeatFlux_kWm2 := rRoofCalorimetricFlux_kWm2;
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* Calorimetric Flux Fallback Mode *)
END_IF;

(* Radiative View Factor F_view: decays exponentially as slag thickness covers the arc column *)
rRoofEffectiveViewFactor := 0.42 * EXP(-3.8 * aState_x[1]);

(* Dual-Tier Roof Thermal Flux Protection Supervisor *)
(* STAGE 1: HIGH FLUX WARNING (Threshold: 280 kW/m2) *)
IF (rCalculatedRoofHeatFlux_kWm2 >= 280.0) AND (iFurnaceHeatPhase > 0) THEN
    bRoofThermalAlert := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* High Thermal Flux Warning *)
    
    (* Autonomous Thermal Mitigation Override: Boost carbon feed +30%, trim O2 -15% *)
    IF (iState = 50) THEN
        rCarbonFeedRateDemand_kgmin := rCarbonFeedRateDemand_kgmin * 1.30;
        IF rCarbonFeedRateDemand_kgmin > rU2_Carbon_Max_kgmin THEN
            rCarbonFeedRateDemand_kgmin := rU2_Carbon_Max_kgmin;
        END_IF;
        rOxygenFlowDemand_Nm3h := rOxygenFlowDemand_Nm3h * 0.85;
    END_IF;
    
    tThermalSurgeTimer(IN := TRUE, PT := T#4S);
    IF tThermalSurgeTimer.Q THEN
        (* Persistent thermal surge: transition to State 70 (SURGE MITIGATION) *)
        IF (iState = 50) THEN
            iState := 70;
        END_IF;
    END_IF;
ELSE
    bRoofThermalAlert := FALSE;
    dwWarningWord := dwWarningWord AND NOT 16#0000_0040;
    tThermalSurgeTimer(IN := FALSE);
END_IF;

(* STAGE 2: CRITICAL BURNOUT TRIP (Threshold: 350 kW/m2) *)
IF (rCalculatedRoofHeatFlux_kWm2 >= 350.0) AND (iFurnaceHeatPhase > 0) THEN
    bTripRoofThermalCritical := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Roof Thermal Critical Burnout Trip *)
    bEmergencyRetractDemand := TRUE;
    iState := 100; (* Emergency Shutdown Trip *)
END_IF;
""")

    # 13. Logic Section 9: State Machine (11 states)
    parts.append("""
(* ================================================================================================= *)
(* 9.0 MULTI-STAGE FINITE STATE MACHINE (11 OPERATIONAL STATES)                                      *)
(* ================================================================================================= *)
(* Coordinates EAF heat lifecycle: scrap charging, bore-in, flat bath transition, foaming ignition,  *)
(* steady-state submerged MPC optimization, refining, surge recovery, and tapping preparation.       *)

(* Update State Transition Timer *)
tStateTimer(IN := TRUE, PT := T#3600S);

CASE iState OF
    0: (* STATE 0: IDLE / ROOF OPEN / FURNACE CHARGE *)
        bSystemRunning := FALSE;
        bSystemReady := bEmergencyStop AND (dwAlarmWord1 = 16#0000_0000);
        bEmergencyRetractDemand := FALSE;
        
        (* Park all actuators in safe mechanical isolation *)
        rCarbonFeedRateDemand_kgmin := 0.0;
        rOxygenFlowDemand_Nm3h := 0.0;
        rLanceHeightDemand_mm := rU3_LanceZ_Max_mm; (* Fully hoisted to 2200 mm *)
        
        (* Reset state vectors to baseline cold-furnace conditions *)
        aState_x[1] := 0.080; (* 80 mm unfoamed liquid/solid slag base *)
        aState_x[2] := 25.0;  (* Baseline FeO *)
        aState_x[3] := 45.0;  (* Cold roof flux *)
        aState_x[4] := 0.00;
        
        IF bSystemEnable AND bSystemReady AND (iFurnaceHeatPhase = 1) THEN
            tStateTimer(IN := FALSE);
            iState := 10; (* Advance to Bore-In *)
        END_IF;

    10: (* STATE 10: ROOF CLOSED / BORE-IN ARC IGNITION (COLD SCRAP MELTDOWN) *)
        bSystemRunning := TRUE;
        bSystemReady := TRUE;
        
        (* Hold lance retracted above charge basket level during initial electrode arc bore-in *)
        rLanceHeightDemand_mm := 2100.0;
        rOxygenFlowDemand_Nm3h := 800.0; (* Low burner mode for scrap preheating *)
        rCarbonFeedRateDemand_kgmin := 0.0;
        
        (* Transition condition: Electrode bore-in complete, high power active, arc voltage stabilizes *)
        IF (iFurnaceHeatPhase = 2) AND (rActiveElectricalPower_MW > 65.0) THEN
            tStateTimer(IN := FALSE);
            iState := 20; (* Advance to Main Meltdown *)
        END_IF;

    20: (* STATE 20: MAIN MELTING BORE-THROUGH / FLAT BATH TRANSITION *)
        bSystemRunning := TRUE;
        
        (* Advance lance to intermediate standby elevation (1600 mm) *)
        rLanceHeightDemand_mm := 1600.0;
        rOxygenFlowDemand_Nm3h := 2200.0; (* Decarb and scrap melting cutting flame *)
        rCarbonFeedRateDemand_kgmin := 10.0; (* Build initial pool carbon content *)
        
        (* Flat bath detection: Acoustic emission drops below 110 dB and arc impedance stabilizes *)
        IF (rArcAcousticEmission_dB < 108.0) AND (rArcCurrent_RMS_kA > 45.0) AND (tStateTimer.ET > T#45S) THEN
            tStateTimer(IN := FALSE);
            iState := 30; (* Advance to Initial Slag Conditioning *)
        END_IF;

    30: (* STATE 30: SLAG BUILDUP & INITIAL LIME/DOLOMITE CONDITIONING *)
        bSystemRunning := TRUE;
        
        (* Lower lance to slag engagement elevation (1400 mm) *)
        rLanceHeightDemand_mm := 1400.0;
        rOxygenFlowDemand_Nm3h := 3200.0;
        rCarbonFeedRateDemand_kgmin := 22.0;
        
        (* Verify Lime/Dolomite flux feeding has built sufficient basicity *)
        IF (rLimeDolomiteFeed_kgmin > 5.0) OR (tStateTimer.ET > T#60S) THEN
            (* Check if FMCW Radar detects slag meniscus swelling above 250 mm *)
            IF (rRadarRawSlagThickness_mm > 250.0) OR (rArcAcousticAttenuation_dB > 8.0) THEN
                tStateTimer(IN := FALSE);
                iState := 40; (* Advance to Active Foaming Slag Formation *)
            END_IF;
        END_IF;

    40: (* STATE 40: ACTIVE FOAMING SLAG NUCLEATION & RADAR ENGAGEMENT *)
        bSystemRunning := TRUE;
        
        (* Ramp carbon injection aggressively to ignite (FeO) + C -> CO bubble nucleation *)
        rLanceHeightDemand_mm := 1250.0;
        rOxygenFlowDemand_Nm3h := 4000.0;
        rCarbonFeedRateDemand_kgmin := 48.0;
        
        (* Engage MPC control optimization *)
        rTargetSlagThickness_mm := 580.0;
        
        (* Transition to fully submerged operation when foam thickness >= 480 mm and Submergence >= 85% *)
        IF (rEstimatedSlagThickness_mm >= 480.0) AND (rArcSubmergenceFactor_pct >= 85.0) THEN
            tFoamStabilizeTimer(IN := TRUE, PT := T#5S);
            IF tFoamStabilizeTimer.Q THEN
                tFoamStabilizeTimer(IN := FALSE);
                tStateTimer(IN := FALSE);
                iState := 50; (* Advance to Fully Submerged Optimal Foaming *)
            END_IF;
        ELSE
            tFoamStabilizeTimer(IN := FALSE);
        END_IF;

    50: (* STATE 50: FULLY SUBMERGED ARC HIGH-EFFICIENCY HEATING (CLOSED-LOOP MPC) *)
        bSystemRunning := TRUE;
        bFoamOptimal_Ready := TRUE;
        
        (* MPC actively manages rOxygenFlowDemand_Nm3h, rCarbonFeedRateDemand_kgmin, and rLanceHeightDemand_mm *)
        rTargetSlagThickness_mm := 650.0;
        rTargetPenetrationRatio := 0.75;
        rTargetRoofFlux_kWm2    := 105.0;
        
        (* Normal Heat Transition: When meltdown completes and furnace enters refining phase *)
        IF (iFurnaceHeatPhase = 3) THEN
            tStateTimer(IN := FALSE);
            iState := 60; (* Advance to Refining Stage *)
        END_IF;
        
        (* Slag Collapse Detection: If submergence drops below 60% for > 6 seconds *)
        IF (rArcSubmergenceFactor_pct < 60.0) AND (tStateTimer.ET > T#10S) THEN
            tStateTimer(IN := FALSE);
            iState := 80; (* Slag Collapse Recovery *)
        END_IF;

    60: (* STATE 60: REFINING & DEPHOSPHORIZATION / TEMPERATURE HOMOGENIZATION *)
        bSystemRunning := TRUE;
        
        (* During refining, trim oxygen to avoid over-oxidizing steel bath, maintain moderate foam *)
        rTargetSlagThickness_mm := 520.0;
        rTargetPenetrationRatio := 0.70;
        
        (* End of heat trigger: Heat phase advances to tapping (phase 4) *)
        IF (iFurnaceHeatPhase = 4) THEN
            tStateTimer(IN := FALSE);
            iState := 90; (* Advance to End-of-Heat De-Foaming *)
        END_IF;

    70: (* STATE 70: ROOF THERMAL SURGE MITIGATION & EMERGENCY SLAG RECOVERY *)
        bSystemRunning := TRUE;
        bRoofThermalAlert := TRUE;
        
        (* Rapid intervention: Inject maximum carbon surge, cut oxygen to stoichiometric min *)
        rCarbonFeedRateDemand_kgmin := 68.0; (* Maximum carbon swell *)
        rOxygenFlowDemand_Nm3h := 2400.0;     (* Restrict free oxygen to quell combustion *)
        rLanceHeightDemand_mm := 1350.0;     (* Back off lance to avoid bath splash *)
        
        (* Verify recovery: Roof heat flux drops below 220 kW/m2 and submergence recovers > 80% *)
        IF (rCalculatedRoofHeatFlux_kWm2 < 220.0) AND (rArcSubmergenceFactor_pct > 80.0) THEN
            tThermalSurgeTimer(IN := TRUE, PT := T#6S);
            IF tThermalSurgeTimer.Q THEN
                tThermalSurgeTimer(IN := FALSE);
                bRoofThermalAlert := FALSE;
                tStateTimer(IN := FALSE);
                iState := 50; (* Return to Optimal Submerged MPC State *)
            END_IF;
        ELSE
            tThermalSurgeTimer(IN := FALSE);
        END_IF;

    80: (* STATE 80: HIGH FeO FOAM COLLAPSE / REACTION RE-IGNITION *)
        bSystemRunning := TRUE;
        
        (* Foam collapsed due to FeO spike or carbon starvation: execute deep carbon pulse *)
        rLanceHeightDemand_mm := 1150.0;     (* Lower lance deeper into slag layer *)
        rOxygenFlowDemand_Nm3h := 3500.0;
        rCarbonFeedRateDemand_kgmin := 62.0; (* Heavy carbon reduction feed *)
        
        (* Recovery check: Slag thickness expands > 450 mm *)
        IF (rEstimatedSlagThickness_mm > 450.0) AND (rArcSubmergenceFactor_pct > 78.0) THEN
            tStateTimer(IN := FALSE);
            iState := 50; (* Return to Normal Optimal Foaming *)
        END_IF;

    90: (* STATE 90: END OF HEAT / SLAG DE-FOAMING & TAPPING PREPARATION *)
        bSystemRunning := TRUE;
        bFoamOptimal_Ready := FALSE;
        
        (* Shut off carbon injection to allow CO bubbles to disengage and collapse foam before tap *)
        rCarbonFeedRateDemand_kgmin := 0.0;
        rOxygenFlowDemand_Nm3h := 1200.0; (* Soft blow to homogenize bath *)
        rLanceHeightDemand_mm := 1800.0; (* Retract lance towards park *)
        
        (* Slag defoamed (thickness < 180 mm) and lance hoisted -> Heat complete *)
        IF (rEstimatedSlagThickness_mm < 180.0) AND (tStateTimer.ET > T#25S) THEN
            rOxygenFlowDemand_Nm3h := 0.0;
            rLanceHeightDemand_mm := rU3_LanceZ_Max_mm;
            bSystemRunning := FALSE;
            IF (iFurnaceHeatPhase = 0) THEN
                iState := 0; (* Return to Idle State *)
            END_IF;
        END_IF;

    100: (* STATE 100: EMERGENCY CO-AXIAL PURGE & FAILSAFE TRIP *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bSystemTripped := TRUE;
        bEmergencyRetractDemand := TRUE;
        
        (* Fast hoist lance to top mechanical limit switches *)
        rLanceHeightDemand_mm := rU3_LanceZ_Max_mm;
        
        (* Immediate isolation of combustible chemicals *)
        rOxygenFlowDemand_Nm3h := 0.0;
        rCarbonFeedRateDemand_kgmin := 0.0;
        
        (* Latch status words for supervisory DCS capture *)
        dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; (* System Tripped Bit *)
        
        (* State exit handled by Operator Reset logic in Section 1.0 *)
END_CASE;
""")

    # 14. Logic Section 10: Graceful Degradation & Clamping
    parts.append("""
(* ================================================================================================= *)
(* 10.0 GRACEFUL DEGRADATION, SENSOR FAULT MITIGATION & DERATE MANAGEMENT                           *)
(* ================================================================================================= *)
(* Manages graceful multi-tier operational fallback when field instruments degrade or fail, ensuring *)
(* continuous furnace thermal shielding and zero production interruption.                            *)

(* Sensor Degradation Tier Evaluation: *)
(* Tier 1: Triple Radar 2oo3 Normal   (dwSystemStatusWord Bit 8) *)
(* Tier 2: Dual Radar 1oo2 Degraded   (dwSystemStatusWord Bit 9) *)
(* Tier 3: Acoustic/THD Fallback Mode (dwSystemStatusWord Bit 10)*)
(* Tier 4: Open-Loop Historical Feed  (dwSystemStatusWord Bit 11)*)

IF (NOT bRadar_Degraded_1oo2) AND (NOT bRadar_Complete_Failure) THEN
    (* Tier 1: Optimal 2oo3 Radar Operation *)
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100;
    dwSystemStatusWord := dwSystemStatusWord AND NOT 16#0000_0E00;
ELSIF bRadar_Degraded_1oo2 AND (NOT bRadar_Complete_Failure) THEN
    (* Tier 2: Degraded 1oo2 Radar Operation *)
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200;
    dwSystemStatusWord := dwSystemStatusWord AND NOT 16#0000_0D00;
ELSIF bRadar_Complete_Failure AND (rArcCurrent_RMS_kA > 15.0) THEN
    (* Tier 3: Virtual Acoustic & Harmonic Distortion Estimator Active *)
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0400;
    dwSystemStatusWord := dwSystemStatusWord AND NOT 16#0000_0B00;
    
    (* Limit maximum oxygen and carbon slew rates to prevent excitation in blind mode *)
    IF rCarbonFeedRateDemand_kgmin > 55.0 THEN
        rCarbonFeedRateDemand_kgmin := 55.0;
    END_IF;
ELSE
    (* Tier 4: Complete Instrument Blackout - Open-loop conservative heat-profile feeding *)
    dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0800;
    dwSystemStatusWord := dwSystemStatusWord AND NOT 16#0000_0700;
    
    IF (iState = 50) THEN
        rOxygenFlowDemand_Nm3h := 3600.0;
        rCarbonFeedRateDemand_kgmin := 32.0;
        rLanceHeightDemand_mm := 1350.0;
    END_IF;
END_IF;

(* Final Output Actuator Rate & Amplitude Clamping Guard *)
IF rOxygenFlowDemand_Nm3h > rU1_O2_Max_Nm3h THEN
    rOxygenFlowDemand_Nm3h := rU1_O2_Max_Nm3h;
END_IF;
IF (rOxygenFlowDemand_Nm3h < rU1_O2_Min_Nm3h) AND (iState >= 30) AND (iState < 90) THEN
    rOxygenFlowDemand_Nm3h := rU1_O2_Min_Nm3h;
END_IF;

IF rCarbonFeedRateDemand_kgmin > rU2_Carbon_Max_kgmin THEN
    rCarbonFeedRateDemand_kgmin := rU2_Carbon_Max_kgmin;
END_IF;
IF rCarbonFeedRateDemand_kgmin < 0.0 THEN
    rCarbonFeedRateDemand_kgmin := 0.0;
END_IF;

IF rLanceHeightDemand_mm > rU3_LanceZ_Max_mm THEN
    rLanceHeightDemand_mm := rU3_LanceZ_Max_mm;
END_IF;
IF rLanceHeightDemand_mm < rU3_LanceZ_Min_mm THEN
    rLanceHeightDemand_mm := rU3_LanceZ_Min_mm;
END_IF;
""")

    # 15. Logic Section 11: Bit-packed status words & closing
    parts.append("""
(* ================================================================================================= *)
(* 11.0 32-BIT BIT-PACKED STATUS WORDS & TELEMETRY REGISTERS                                         *)
(* ================================================================================================= *)
(* Encodes system operational modes, state indices, safety interlocks, and sensor diagnostics into   *)
(* standardized IEEE/MODBUS DWORD registers for supervisory SCADA/Level-2 DCS integration.           *)

(* Reset dynamic operational bits in dwSystemStatusWord while preserving tier flags *)
dwSystemStatusWord := dwSystemStatusWord AND 16#0000_0F00;

IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bFoamOptimal_Ready THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bRoofThermalAlert THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bEmergencyRetractDemand THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF (rArcSubmergenceFactor_pct >= 90.0) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;

(* Encode Active State Index into Upper Word of dwSystemStatusWord (Bits 16-27) *)
IF (iState = 0)   THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0001_0000; END_IF;
IF (iState = 10)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0002_0000; END_IF;
IF (iState = 20)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0004_0000; END_IF;
IF (iState = 30)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0008_0000; END_IF;
IF (iState = 40)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0010_0000; END_IF;
IF (iState = 50)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0020_0000; END_IF;
IF (iState = 60)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0040_0000; END_IF;
IF (iState = 70)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0080_0000; END_IF;
IF (iState = 80)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0100_0000; END_IF;
IF (iState = 90)  THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0200_0000; END_IF;
IF (iState = 100) THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0400_0000; END_IF;

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    code = build_eaf_st_code()
    print("Code length:", len(code))
    lines = code.splitlines()
    print("First line:", lines[0])
    print("Last line:", lines[-1])
    
    assert lines[0] == "FUNCTION_BLOCK FB_EAF_FoamingSlag_MicrowaveRadar_CarbonInject", "First line mismatch"
    assert lines[-1] == "END_FUNCTION_BLOCK", "Last line mismatch"
    
    # Check IF/END_IF parity
    ifs = len(re.findall(r'\bIF\b', code))
    end_ifs = len(re.findall(r'\bEND_IF\b', code))
    assert ifs == end_ifs, f"IF/END_IF mismatch: {ifs} != {end_ifs}"
    
    # Check CASE/END_CASE parity
    cases = len(re.findall(r'\bCASE\b', code))
    end_cases = len(re.findall(r'\bEND_CASE\b', code))
    assert cases == end_cases, f"CASE/END_CASE mismatch: {cases} != {end_cases}"
    
    # Check FOR/END_FOR parity
    fors = len(re.findall(r'\bFOR\b', code))
    end_fors = len(re.findall(r'\bEND_FOR\b', code))
    assert fors == end_fors, f"FOR/END_FOR mismatch: {fors} != {end_fors}"
    
    # Check required units
    for u in ['[kA]', '[V]', '[mm]', '[Nm3/h]', '[kg/min]', '[dB]', '[deg C]', '[kW/m2]']:
        assert u in code, f"Missing required unit: {u}"

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: 150-Ton Industrial AC Electric Arc Furnace (EAF) Dynamic Foaming Slag Optimization: 24 GHz FMCW Microwave Radar Slag Thickness Profiling, Supersonic Carbon/Oxygen Co-Axial Lance Penetration Ratio, Arc Acoustic Emission Harmonic Distortion Impedance Feedback, and Water-Cooled Roof Thermal Flux Protection**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_EAF_FoamingSlag_MicrowaveRadar_CarbonInject
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [kA], [V], [mm], [Nm3/h], [kg/min], [dB], [deg C], [kW/m2])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 60,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_EAF_FoamingSlag_MicrowaveRadar_CarbonInject
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: 150-Ton Industrial AC Electric Arc Furnace (EAF) Dynamic Foaming Slag Optimization: 24 GHz FMCW Microwave Radar Slag Thickness Profiling, Supersonic Carbon/Oxygen Co-Axial Lance Penetration Ratio, Arc Acoustic Emission Harmonic Distortion Impedance Feedback, and Water-Cooled Roof Thermal Flux Protection"""

    assistant_content = f"```iec-st\n{code}\n```"
    print("Assistant content length:", len(assistant_content))
    assert len(assistant_content) >= 3500, "Assistant content too short"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    file_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{file_id}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False)

    print(f"Saved to {filename}")

