# -*- coding: utf-8 -*-
"""
Builder script for generating FB_Biopharma_ContinuousTFF_UltrafiltrationBufferSync
IEC 61131-3 Structured Text dataset.
Target size: 85,000 - 95,000 characters.
"""

import sys

def build_code():
    parts = []

    # -------------------------------------------------------------------------
    # Opening declaration and comprehensive header comments
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Biopharma_ContinuousTFF_UltrafiltrationBufferSync
(* ========================================================================================= *)
(* LUMINA CYBER-PHYSICAL SYSTEMS ARCHITECTURE - BIOPHARMACEUTICAL DOWNSTREAM DIVISION         *)
(* V7 MAX-PERSONA ENGINEERING STANDARD: CGMP ANNEX 1 / ASME BPE-2022 / GAMP 5 CLASS 4        *)
(*                                                                                           *)
(* AUTONOMOUS DUAL-STAGE TANGENTIAL FLOW ULTRAFILTRATION & DIAFILTRATION (UF/DF) ENGINE     *)
(* INTEGRATING:                                                                              *)
(*   1. TRIPLE MODULAR REDUNDANCY (2oo3) TMR SENSOR FUSION (PT, CT, AT_pH, UV-280)           *)
(*   2. TRANSMEMBRANE PRESSURE (TMP) & CROSSFLOW SHEAR RATE DYNAMIC CASCADE CONTROLLER      *)
(*   3. GEL-POLARIZATION BOUNDARY LAYER HYDRAULIC RESISTANCE OBSERVER (DARCY-LEVEQUE-MOONEY) *)
(*   4. CONTINUOUS IN-SITU UV-280nm PROTEIN CONCENTRATION FEEDBACK (BEER-LAMBERT PATH-ADAPT) *)
(*   5. DUAL-STAGE CONDUCTIVITY / pH BUFFER EXCHANGE MODULATION (ISOVOLUMETRIC WASHOUT)      *)
(*   6. 6-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL & REAL-TIME MPC QUADRATIC SOLVER   *)
(*   7. 11-STAGE FINITE STATE MACHINE (FSM) WITH CIP / NWP BASELINING & MEMBRANE RECOVERY   *)
(*   8. GRACEFUL DEGRADATION, HIGH-VISCOSITY FEED DERATE & ACTIVE FOULING CLEARING          *)
(*   9. DETERMINISTIC 32-BIT BIT-PACKED STATUS, ALARM, AND QUALITY METRIC WORDS             *)
(*                                                                                           *)
(* PROCESS NOMENCLATURE & GOVERNING FIRST-PRINCIPLES EQUATIONS:                             *)
(*   - Transmembrane Pressure: TMP = 0.5 * (P_feed + P_ret) - P_perm                         *)
(*   - Channel Crossflow Pressure Drop: Delta_P = P_feed - P_ret                             *)
(*   - Retentate Channel Wall Shear Rate: gamma_w = 6 * Q_feed / (b_ch * h_ch^2)             *)
(*   - Wall Shear Stress: tau_w = mu_ret * gamma_w                                          *)
(*   - Darcy-Starling Total Resistance: J_v = TMP / (mu_perm * R_tot)                        *)
(*   - Series Resistance Partitioning: R_tot = R_m + R_cp + R_gel + R_pore                   *)
(*   - Leveque Mass Transfer Coeff: k_f = 0.819 * (gamma_w * D_ab^2 / L_ch)^(1/3)            *)
(*   - Concentration Polarization: C_w = C_b * EXP(J_v / k_f)                                *)
(*   - Gel Layer Cake Resistance: R_gel = r_spec * m_cake / A_m = r_spec * rho_p * delta_g   *)
(*   - Mooney Concentrated Viscosity: ln(eta_rel) = [eta]*C_b / (1 - (k/nu)*[eta]*C_b)       *)
(*   - Beer-Lambert Solute Absorbance: C_protein = (A_280 - 1.5 * A_340) / (eps_280 * L_opt) *)
(*   - Continuous Diafiltration Washout: d(C_imp)/dt = - (FT_Buf / V_ret) * (1 - R_imp)*C_imp*)
(*   - Nernst Electrode pH Potential: E = E_0 - (2.3026 * R * T / F) * pH                    *)
(* ========================================================================================= *)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* ===================================================================================== *)
    (* PHYSICAL SENSOR INPUTS (WITH STRICT CIMAC / ASME BPE PHYSICAL UNITS)                  *)
    (* ===================================================================================== *)

    (* --- Feed Line Pressure Sensors (2oo3 TMR Bank) --- *)
    rPT_Feed_A_bar                  : REAL;     (* [bar] Sanitary piezoresistive feed pressure transmitter A *)
    rPT_Feed_B_bar                  : REAL;     (* [bar] Sanitary piezoresistive feed pressure transmitter B *)
    rPT_Feed_C_bar                  : REAL;     (* [bar] Sanitary piezoresistive feed pressure transmitter C *)

    (* --- Retentate Line Pressure Sensors (2oo3 TMR Bank) --- *)
    rPT_Ret_A_bar                   : REAL;     (* [bar] Retentate backpressure transmitter A *)
    rPT_Ret_B_bar                   : REAL;     (* [bar] Retentate backpressure transmitter B *)
    rPT_Ret_C_bar                   : REAL;     (* [bar] Retentate backpressure transmitter C *)

    (* --- Permeate Line Pressure Sensors (2oo3 TMR Bank) --- *)
    rPT_Perm_A_bar                  : REAL;     (* [bar] Permeate manifold pressure transmitter A *)
    rPT_Perm_B_bar                  : REAL;     (* [bar] Permeate manifold pressure transmitter B *)
    rPT_Perm_C_bar                  : REAL;     (* [bar] Permeate manifold pressure transmitter C *)

    (* --- Process Volumetric / Mass Flow Transmitters --- *)
    rFT_Feed_Lh                     : REAL;     (* [L/h] Electromagnetic sanitary feed flow transmitter *)
    rFT_Perm_Lh                     : REAL;     (* [L/h] Sanitary Coriolis permeate flow transmitter *)
    rFT_Buf_Lh                      : REAL;     (* [L/h] Diafiltration buffer supply mass flow transmitter *)

    (* --- Retentate In-Line Conductivity Sensors (2oo3 TMR Bank) --- *)
    rCT_Ret_A_mScm                  : REAL;     (* [mS/cm] Toroidal electrodeless conductivity cell A *)
    rCT_Ret_B_mScm                  : REAL;     (* [mS/cm] Toroidal electrodeless conductivity cell B *)
    rCT_Ret_C_mScm                  : REAL;     (* [mS/cm] Toroidal electrodeless conductivity cell C *)

    (* --- Retentate In-Line pH Glass Electrodes (2oo3 TMR Bank) --- *)
    rAT_pH_A                        : REAL;     (* [pH] Pressurized gel-filled sanitary pH electrode A *)
    rAT_pH_B                        : REAL;     (* [pH] Pressurized gel-filled sanitary pH electrode B *)
    rAT_pH_C                        : REAL;     (* [pH] Pressurized gel-filled sanitary pH electrode C *)

    (* --- In-Situ UV-280nm Protein Absorbance Spectrophotometers (2oo3 TMR Bank) --- *)
    rAT_UV280_A_mAU                 : REAL;     (* [mAU] Variable-pathlength UV-280nm optical detector A *)
    rAT_UV280_B_mAU                 : REAL;     (* [mAU] Variable-pathlength UV-280nm optical detector B *)
    rAT_UV280_C_mAU                 : REAL;     (* [mAU] Variable-pathlength UV-280nm optical detector C *)

    (* --- Permeate Line UV-280nm Membrane Integrity Breakthrough Sensor --- *)
    rAT_UV280_Perm_mAU              : REAL;     (* [mAU] Permeate line UV-280nm optical detector for membrane rupture *)

    (* --- Product Stream Physical & Rheological Properties --- *)
    rTT_Prod_DegC                   : REAL;     (* [deg C] Retentate sanitary RTD Pt100 temperature transmitter *)
    rVT_Visc_cP                     : REAL;     (* [cP] Acoustic vibrational in-line rheometer dynamic viscosity *)
    rAI_LabProteinRef_gL            : REAL;     (* [g/L] Laboratory benchtop reference protein concentration calibration *)

    (* --- Engineering & Process Setpoints --- *)
    rTargetProteinConc_gL           : REAL;     (* [g/L] Final target product concentration setpoint (e.g. 150.0 g/L) *)
    rTargetDiafiltrationVols_DV     : REAL;     (* [DV] Target diafiltration turnover volume count (e.g. 7.0 DV) *)
    rTargetConductivity_mScm        : REAL;     (* [mS/cm] Formulation buffer target conductivity setpoint (e.g. 4.2 mS/cm) *)
    rTargetpH                       : REAL;     (* [pH] Formulation buffer target pH setpoint (e.g. 6.00 pH) *)
    rMaxAllowableTMP_bar            : REAL;     (* [bar] Maximum allowable operational TMP before safety backoff *)
    rMaxAllowableWallShear_s1       : REAL;     (* [s^-1] Maximum allowable channel wall shear rate (protein shear limit) *)
    rMembraneArea_m2                : REAL;     (* [m^2] Total active membrane cassette surface area installed *)
    rInitialBatchVolume_L           : REAL;     (* [L] Starting product pool liquid volume in feed skid tank *)

    (* --- Discrete System Command & Safety Interlock Signals --- *)
    bEnable                         : BOOL;     (* Skid master software run enable command *)
    bSafetyRelayOK                  : BOOL;     (* Dual-channel hardwired SIL-3 emergency safety circuit healthy *)
    bEmergencyStop                  : BOOL;     (* Physical E-Stop pushbutton circuit healthy (TRUE = Normal, FALSE = E-Stop) *)
    bResetFaults                    : BOOL;     (* Operator manual fault reset and trip latch clear pushbutton *)
    bStartCycle                     : BOOL;     (* Operator command: initiate automated UF/DF batch recipe sequence *)
    bAbortCycle                     : BOOL;     (* Operator command: immediate controlled abort and sequence termination *)
    bAirBubbleDetected              : BOOL;     (* Ultrasonic feed line bubble sensor (TRUE = bubble ingress detected) *)
    rCycleTime_sec                  : REAL;     (* PLC deterministic execution task cycle interval [s] (e.g. 0.010 s) *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ===================================================================================== *)
    (* ACTUATOR COMMAND OUTPUTS & REVENUE-CRITICAL PROCESS VARIABLES                         *)
    (* ===================================================================================== *)

    (* --- Primary Skid Actuators --- *)
    rFeedPumpSpeed_rpm              : REAL;     (* [rpm] Quaternary diaphragm sanitary feed pump VFD speed demand *)
    rRetentateValve_pct             : REAL;     (* [%] Sanitary proportional retentate backpressure pinch valve (0-100%) *)
    rPermeatePumpSpeed_rpm          : REAL;     (* [rpm] Permeate suction control peristaltic/gear pump speed demand *)
    rPermeateValve_pct              : REAL;     (* [%] Sanitary permeate throttling diaphragm valve position (0-100%) *)
    rBufferPumpA_pct                : REAL;     (* [%] Diafiltration Buffer A (conditioning/wash) metering pump rate *)
    rBufferPumpB_pct                : REAL;     (* [%] Diafiltration Buffer B (formulation) metering pump rate *)

    (* --- Real-Time Observed Physical States & Hydrodynamic Analytics --- *)
    rObservedTMP_bar                : REAL;     (* [bar] Calculated Transmembrane Pressure: 0.5*(P_feed + P_ret) - P_perm *)
    rObservedFlux_LMH               : REAL;     (* [L/(m^2*h)] Permeate volumetric flux normalized to membrane area *)
    rObservedHydraulicResistance_m1 : REAL;     (* [1/m] Total system dynamic hydraulic membrane resistance *)
    rObservedGelLayerResistance_m1  : REAL;     (* [1/m] Estimated boundary layer protein gel layer resistance *)
    rObservedGelLayerThickness_um   : REAL;     (* [um] Estimated protein concentration polarization boundary cake thickness *)
    rCalculatedProteinConc_gL       : REAL;     (* [g/L] Real-time optical UV-280nm verified bulk protein concentration *)
    rDiafiltrationVolumesCompleted_DV:REAL;     (* [DV] Accumulated diafiltration turnover volumes completed *)
    rNormalizedWaterPermeability_LMHbar: REAL;  (* [LMH/bar] Normalized Water Permeability (NWP) standardized to 20 deg C *)
    rCurrentRetentateVolume_L       : REAL;     (* [L] Estimated instantaneous retentate pool liquid volume *)
    rWallShearRate_s1               : REAL;     (* [s^-1] Calculated retentate flow channel wall shear rate *)
    rWallShearStress_Pa             : REAL;     (* [Pa] Calculated fluid boundary wall shear stress *)

    (* --- Discrete Process Status & Interlock Indicators --- *)
    bSystemReady                    : BOOL;     (* System fully initialized, healthy, and ready to accept start command *)
    bSystemRunning                  : BOOL;     (* Automated downstream UF/DF recipe sequence actively running *)
    bSystemTripped                  : BOOL;     (* System tripped due to critical safety interlock or equipment hazard *)
    bConcentrationComplete          : BOOL;     (* Final target protein concentration successfully attained *)
    bDiafiltrationComplete          : BOOL;     (* Diafiltration exchange target DV, conductivity and pH attained *)
    bMembraneFoulingCritical        : BOOL;     (* Boundary layer gel fouling exceeds critical operating limit *)
    bPermeateBreakthroughAlarm      : BOOL;     (* Permeate UV-280nm breakthrough indicates cassette membrane breach *)
    bGelPolarizationWarning         : BOOL;     (* Wall concentration C_w approaching gel precipitation limit *)
    bDegradedSensorMode             : BOOL;     (* Operating under degraded 1oo2 TMR sensor redundancy fallback *)

    (* --- Standardized 32-Bit Telemetry & Diagnostic Registers --- *)
    dwSystemStatusWord              : DWORD;    (* Bit-packed operational FSM state and controller status flags *)
    dwAlarmWord1                    : DWORD;    (* Bit-packed critical safety shutdown trip flags *)
    dwAlarmWord2                    : DWORD;    (* Bit-packed process excursion and product quality fault flags *)
    dwWarningWord                   : DWORD;    (* Bit-packed maintenance, fouling, and sensor deviation warnings *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ===================================================================================== *)
    (* INTERNAL STATE VARIABLES, OBSERVER MATRICES, MPC REGISTERS, AND FSM ENGINE            *)
    (* ===================================================================================== *)

    (* --- Finite State Machine Execution Management --- *)
    iState                          : INT := 0; (* Active FSM sequence state index (0 to 100) *)
    iPreviousState                  : INT := 0; (* Preceding FSM sequence state index for edge detection *)
    iTargetState                    : INT := 0; (* Next scheduled state index during transitions *)
    tStateTimer                     : TON;      (* Standard execution timer tracking time in current state *)
    tStepTimeoutTimer               : TON;      (* Maximum allowable duration watchdog timer per stage *)

    (* --- 2oo3 Triple Modular Redundancy Sensor Voting Registers --- *)
    (* Feed Pressure PT Bank *)
    rVoted_PFeed_bar                : REAL := 0.0;
    bFeedP_Dev_AB                   : BOOL := FALSE;
    bFeedP_Dev_BC                   : BOOL := FALSE;
    bFeedP_Dev_CA                   : BOOL := FALSE;
    bFeedP_SensorA_Fail             : BOOL := FALSE;
    bFeedP_SensorB_Fail             : BOOL := FALSE;
    bFeedP_SensorC_Fail             : BOOL := FALSE;
    bFeedP_Degraded_1oo2            : BOOL := FALSE;
    bFeedP_TotalFailure             : BOOL := FALSE;
    tFeedP_DiscrepancyTimer         : TON;

    (* Retentate Pressure PT Bank *)
    rVoted_PRet_bar                 : REAL := 0.0;
    bRetP_Dev_AB                    : BOOL := FALSE;
    bRetP_Dev_BC                    : BOOL := FALSE;
    bRetP_Dev_CA                    : BOOL := FALSE;
    bRetP_SensorA_Fail              : BOOL := FALSE;
    bRetP_SensorB_Fail              : BOOL := FALSE;
    bRetP_SensorC_Fail              : BOOL := FALSE;
    bRetP_Degraded_1oo2             : BOOL := FALSE;
    bRetP_TotalFailure              : BOOL := FALSE;
    tRetP_DiscrepancyTimer          : TON;

    (* Permeate Pressure PT Bank *)
    rVoted_PPerm_bar                : REAL := 0.0;
    bPermP_Dev_AB                   : BOOL := FALSE;
    bPermP_Dev_BC                   : BOOL := FALSE;
    bPermP_Dev_CA                   : BOOL := FALSE;
    bPermP_SensorA_Fail             : BOOL := FALSE;
    bPermP_SensorB_Fail             : BOOL := FALSE;
    bPermP_SensorC_Fail             : BOOL := FALSE;
    bPermP_Degraded_1oo2            : BOOL := FALSE;
    bPermP_TotalFailure             : BOOL := FALSE;
    tPermP_DiscrepancyTimer         : TON;

    (* In-Line Conductivity CT Bank *)
    rVoted_Cond_mScm                : REAL := 0.0;
    bCond_Dev_AB                    : BOOL := FALSE;
    bCond_Dev_BC                    : BOOL := FALSE;
    bCond_Dev_CA                    : BOOL := FALSE;
    bCond_SensorA_Fail              : BOOL := FALSE;
    bCond_SensorB_Fail              : BOOL := FALSE;
    bCond_SensorC_Fail              : BOOL := FALSE;
    bCond_Degraded_1oo2             : BOOL := FALSE;
    bCond_TotalFailure              : BOOL := FALSE;
    tCond_DiscrepancyTimer          : TON;

    (* In-Line pH Electrode AT Bank *)
    rVoted_pH                       : REAL := 7.0;
    bpH_Dev_AB                      : BOOL := FALSE;
    bpH_Dev_BC                      : BOOL := FALSE;
    bpH_Dev_CA                      : BOOL := FALSE;
    bpH_SensorA_Fail                : BOOL := FALSE;
    bpH_SensorB_Fail                : BOOL := FALSE;
    bpH_SensorC_Fail                : BOOL := FALSE;
    bpH_Degraded_1oo2               : BOOL := FALSE;
    bpH_TotalFailure                : BOOL := FALSE;
    tpH_DiscrepancyTimer            : TON;

    (* In-Situ UV-280nm Spectrophotometer AT Bank *)
    rVoted_UV280_mAU                : REAL := 0.0;
    bUV_Dev_AB                      : BOOL := FALSE;
    bUV_Dev_BC                      : BOOL := FALSE;
    bUV_Dev_CA                      : BOOL := FALSE;
    bUV_SensorA_Fail                : BOOL := FALSE;
    bUV_SensorB_Fail                : BOOL := FALSE;
    bUV_SensorC_Fail                : BOOL := FALSE;
    bUV_Degraded_1oo2               : BOOL := FALSE;
    bUV_TotalFailure                : BOOL := FALSE;
    tUV_DiscrepancyTimer            : TON;

    (* --- First-Order Low-Pass Signal Conditioning Filters --- *)
    rFiltered_FeedFlow_Lh           : REAL := 0.0;
    rFiltered_PermFlow_Lh           : REAL := 0.0;
    rFiltered_BufFlow_Lh            : REAL := 0.0;
    rFiltered_Visc_cP               : REAL := 1.0;
    rFiltered_Temp_DegC             : REAL := 20.0;
    rFiltered_PermBreakthrough_mAU  : REAL := 0.0;

    (* Filter Smoothing Coefficients (Alpha = dt / (RC + dt)) *)
    rAlphaFlow                      : REAL := 0.095;
    rAlphaVisc                      : REAL := 0.048;
    rAlphaTemp                      : REAL := 0.024;
    rAlphaUV                        : REAL := 0.120;

    (* --- Cassette Fluid Dynamics & Crossflow Geometry Constants --- *)
    rChannelWidth_m                 : REAL := 0.150;    (* [m] Width of rectangular feed channel *)
    rChannelHeight_m                : REAL := 0.0005;   (* [m] Channel screen-spacer clearance height (0.5 mm) *)
    rChannelLength_m                : REAL := 0.400;    (* [m] Total flow path channel length across cassette *)
    rDiffusivity_m2s                : REAL := 4.2E-11;  (* [m^2/s] Stokes-Einstein diffusion coefficient for 150 kDa mAb *)
    rProteinGelConc_gL              : REAL := 280.0;    (* [g/L] Protein gel-layer consolidation concentration C_gel *)
    rSpecificCakeResistance_mkg     : REAL := 1.85E14;  (* [m/kg] Specific protein cake filtration resistance r_spec *)
    rProteinDensity_kgm3            : REAL := 1350.0;   (* [kg/m^3] Hydrated protein density rho_p *)
    rCleanMembraneResistance_m1     : REAL := 2.45E11;  (* [1/m] Baseline intrinsic membrane resistance R_m at 20 deg C *)

    (* --- Mooney & Arrhenius Rheological Parameters --- *)
    rIntrinsicViscosity_Lg          : REAL := 0.0035;   (* [L/g] Intrinsic viscosity [eta] for globular monoclonal antibody *)
    rCrowdingFactor                 : REAL := 0.45;     (* [dimensionless] Self-crowding packing coefficient k/nu *)
    rViscWater20C_cP                : REAL := 1.002;    (* [cP] Pure water dynamic viscosity at reference 20.0 deg C *)

    (* --- Optical Beer-Lambert Spectroscopy Calibration --- *)
    rExtinctionCoeff_L_g_cm         : REAL := 1.45;     (* [L/(g*cm)] Specific mass extinction coefficient epsilon_280 *)
    rFlowCellPathlength_cm          : REAL := 0.050;    (* [cm] Fixed variable-pathlength flow cell optical gap (0.5 mm) *)
    rBaselineTurbidityOffset_mAU    : REAL := 12.5;     (* [mAU] Compensated optical turbidity offset at 340 nm *)
    rRLS_Gain                       : REAL := 0.015;    (* Recursive least-squares adaptation factor for lab calibration *)

    (* --- Gel-Polarization Boundary Layer Hydraulic Observer Registers --- *)
    rState_Rm_m1                    : REAL := 2.45E11;  (* Clean membrane resistance state R_m *)
    rState_Rcp_m1                   : REAL := 0.0;      (* Dynamic concentration polarization resistance state R_cp *)
    rState_Rgel_m1                  : REAL := 0.0;      (* Reversible gel-polarization cake resistance state R_gel *)
    rState_Rpore_m1                 : REAL := 0.0;      (* Irreversible pore adsorption / constriction resistance state R_pore *)
    rState_WallConc_gL              : REAL := 0.0;      (* Estimated membrane wall protein concentration C_w *)
    rState_GelThickness_m           : REAL := 0.0;      (* Dynamic gel cake thickness delta_gel *)
    rObs_MassTransferCoeff_ms       : REAL := 0.0;      (* Leveque mass transfer coefficient k_f [m/s] *)
    rObs_PermeateVelocity_ms        : REAL := 0.0;      (* Superficial permeate flux velocity v_w [m/s] *)
    rObs_PecletNumber               : REAL := 0.0;      (* Boundary layer convective Peclet number Pe = v_w / k_f *)
    rPermeateWaterViscosity_cP      : REAL := 1.0;      (* Permeate buffer dynamic viscosity at current temperature *)
    rRetentateFluidViscosity_cP     : REAL := 1.0;      (* Retentate bulk dynamic viscosity calculated via Mooney model *)

    (* Observer Innovation & Luenberger Gain Parameters *)
    rObs_Innovation_bar             : REAL := 0.0;      (* Difference between measured TMP and hydraulic model TMP *)
    rLuenbergerGain_Rgel            : REAL := 4.5E9;    (* Observer update gain for gel layer resistance [m^-1 / bar] *)
    rLuenbergerGain_Rpore           : REAL := 1.2E8;    (* Observer update gain for pore fouling resistance [m^-1 / bar] *)

    (* --- Diafiltration Mass Balance & Continuous Titration Registers --- *)
    rAccumulatedPermeateVolume_L    : REAL := 0.0;      (* Total integrated permeate liquid volume collected *)
    rAccumulatedBufferVolume_L      : REAL := 0.0;      (* Total integrated diafiltration buffer dosed *)
    rAccumulatedFeedVolume_L        : REAL := 0.0;      (* Total integrated raw product feed pumped into skid *)
    rCurrentRetentateMass_kg        : REAL := 0.0;      (* Current product batch mass in loop and feed tank *)
    rBufferExchangeEfficiency_pct   : REAL := 100.0;    (* Practical buffer exchange washout efficiency *)
    rTheoreticalDV_Required         : REAL := 7.0;      (* DV required to clear impurities below target limit *)
    rBufferA_TargetRatio            : REAL := 1.0;      (* Fractional setpoint for Conditioning Buffer A (0.0 to 1.0) *)
    rBufferB_TargetRatio            : REAL := 0.0;      (* Fractional setpoint for Formulation Buffer B (0.0 to 1.0) *)

    (* Titration Decoupling PID Internals *)
    rPID_Cond_Integral              : REAL := 0.0;
    rPID_Cond_PrevError             : REAL := 0.0;
    rPID_pH_Integral                : REAL := 0.0;
    rPID_pH_PrevError               : REAL := 0.0;

    (* --- 6-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL MATRICES --- *)
    (* State vector: x = [C_b, C_w, R_gel, J_v, Cond, pH]^T             *)
    (* Control input vector: u = [N_feed, V_ret, N_perm, BufA, BufB]^T   *)
    (* Disturbance / Parameter Vector: d = [Visc, Temp, DV]^T           *)
    x_state                         : ARRAY[1..6] OF REAL := [5.0, 5.0, 0.0, 45.0, 15.0, 7.2];
    x_hat                           : ARRAY[1..6] OF REAL := [5.0, 5.0, 0.0, 45.0, 15.0, 7.2];
    x_error                         : ARRAY[1..6] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    u_control                       : ARRAY[1..5] OF REAL := [1200.0, 50.0, 150.0, 0.0, 0.0];
    u_prev                          : ARRAY[1..5] OF REAL := [1200.0, 50.0, 150.0, 0.0, 0.0];
    delta_u                         : ARRAY[1..5] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0];

    (* Linearized Discrete System Matrix A_d (6x6) sampled at dt = 10ms *)
    A_d                             : ARRAY[1..6, 1..6] OF REAL := [
        [0.99982,  0.00000, -1.20E-14, 0.00015,  0.00000,  0.00000],
        [0.00145,  0.98520, -4.50E-13, 0.00280,  0.00000,  0.00000],
        [0.00000,  1.85E9,   0.99200,  0.00000,  0.00000,  0.00000],
        [-0.0120, -0.0450,  -8.50E-12, 0.94500,  0.00000,  0.00000],
        [0.00000,  0.00000,  0.00000,  0.00000,  0.99850,  0.00000],
        [0.00000,  0.00000,  0.00000,  0.00000,  0.00000,  0.99910]
    ];

    (* Linearized Discrete Input Coupling Matrix B_d (6x5) *)
    B_d                             : ARRAY[1..6, 1..5] OF REAL := [
        [ 0.000012, -0.000045, -0.000085,  0.000000,  0.000000],
        [-0.000085,  0.000120,  0.000450,  0.000000,  0.000000],
        [-4.50E6,    1.25E7,    3.80E7,    0.000000,  0.000000],
        [ 0.001500,  0.008500, -0.018500,  0.000000,  0.000000],
        [ 0.000000,  0.000000,  0.000000, -0.004500,  0.007800],
        [ 0.000000,  0.000000,  0.000000,  0.000850, -0.001200]
    ];

    (* Measurement Output Matrix C_d (6x6) *)
    C_d                             : ARRAY[1..6, 1..6] OF REAL := [
        [1.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 1.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 1.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 1.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0, 1.0]
    ];

    (* Direct Transmission Feedthrough Matrix D_d (6x5) *)
    D_d                             : ARRAY[1..6, 1..5] OF REAL := [
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0],
        [0.0, 0.0, 0.0, 0.0, 0.0]
    ];

    (* MPC Quadratic Performance Index Weighting Diagonal Matrices *)
    Q_diag                          : ARRAY[1..6] OF REAL := [18.0, 8.5, 1.5E-18, 5.0, 12.0, 25.0];
    R_diag                          : ARRAY[1..5] OF REAL := [0.0015, 0.025, 0.045, 0.085, 0.085];
    rMPC_GradientStepSize           : REAL := 0.0085;
    bMpcInOptimization              : BOOL := FALSE;

    (* --- Dynamic Slew-Rate Limiters & Actuator Clamps --- *)
    rFeedPumpSpeed_Internal_rpm     : REAL := 0.0;
    rRetentateValve_Internal_pct    : REAL := 0.0;
    rPermeatePump_Internal_rpm      : REAL := 0.0;
    rPermeateValve_Internal_pct     : REAL := 0.0;
    rBufferPumpA_Internal_pct       : REAL := 0.0;
    rBufferPumpB_Internal_pct       : REAL := 0.0;

    rMaxSlew_FeedPump_rpms          : REAL := 150.0;    (* Max feed pump acceleration [rpm/s] *)
    rMaxSlew_RetValve_pcts          : REAL := 15.0;     (* Max retentate valve stroke slew [%/s] *)
    rMaxSlew_PermPump_rpms          : REAL := 50.0;     (* Max permeate pump acceleration [rpm/s] *)
    rMaxSlew_BufferPumps_pcts       : REAL := 20.0;     (* Max buffer pump dosing slew [%/s] *)

    (* --- Safety Watchdog Timers & Flush Clocks --- *)
    tCIPFlushTimer                  : TON;
    tIntegrityAirTimer              : TON;
    tProductPrimingTimer            : TON;
    tAirBubbleDebounceTimer         : TON;
    tPermeateBreakthroughTimer      : TON;
    tOverpressureDebounceTimer      : TON;
    tHighShearDebounceTimer         : TON;
    tOverTempDebounceTimer          : TON;
    tCleanWaterFluxTimer            : TON;

    (* Loop Indexing Internals *)
    iRow                            : INT := 1;
    iCol                            : INT := 1;
    rTempSum                        : REAL := 0.0;
    rTempGrad                       : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # Main logic: Section 1.0 SIL-3 Hardwired Safety Evaluation
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 1.0 SIL-3 HARDWIRED SAFETY INTERLOCK EVALUATION & EMERGENCY TRIPPING                      *)
(* ========================================================================================= *)
(* Primary functional safety: evaluates hardwired safety relays, E-stops, and ultra-critical *)
(* equipment-protection constraints. Instantaneous execution precedes all other logic blocks.*)

(* Evaluate Emergency Stop and Safety Relays *)
IF (NOT bSafetyRelayOK) OR (NOT bEmergencyStop) THEN
    bSystemRunning := FALSE;
    bSystemReady := FALSE;
    bSystemTripped := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0001; (* E-Stop / Safety Relay Tripped *)
    iState := 100; (* Jump immediately to Emergency Depressurization / Safe Park state *)
END_IF;

(* Evaluate Software Abort Command *)
IF bAbortCycle AND bSystemRunning THEN
    bSystemRunning := FALSE;
    bSystemReady := FALSE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0002; (* Operator Abort Command Latched *)
    iState := 100;
END_IF;

(* Ultrasonic Air Bubble Intrusion Ingress Check (Prevents Membrane Drying & Protein Shearing) *)
tAirBubbleDebounceTimer(IN := bAirBubbleDetected, PT := T#150MS);
IF tAirBubbleDebounceTimer.Q THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0004; (* Severe Air Entrainment In Feed Line *)
    IF bSystemRunning THEN
        iState := 100;
    END_IF;
END_IF;

(* Critical Retentate Fluid Over-Temperature Check (Prevents Monoclonal Antibody Thermal Denaturation) *)
tOverTempDebounceTimer(IN := (rTT_Prod_DegC > 28.5), PT := T#500MS);
IF tOverTempDebounceTimer.Q THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0008; (* Protein Thermal Inactivation Trip (> 28.5 deg C) *)
    IF bSystemRunning THEN
        iState := 100;
    END_IF;
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 2.0 2oo3 TMR Voting Logic
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 2.0 TRIPLE MODULAR REDUNDANCY (2oo3) SENSOR VOTING ALGORITHMS                             *)
(* ========================================================================================= *)
(* Deterministic median selection across three redundant instruments with cross-channel      *)
(* discrepancy evaluation, sensor failure flagging, and seamless 2oo3-to-1oo2 degradation.   *)

(* --- 2.1 FEED LINE PRESSURE TRANSMITTERS (PT-101A/B/C) --- *)
bFeedP_Dev_AB := ABS(rPT_Feed_A_bar - rPT_Feed_B_bar) > 0.25;
bFeedP_Dev_BC := ABS(rPT_Feed_B_bar - rPT_Feed_C_bar) > 0.25;
bFeedP_Dev_CA := ABS(rPT_Feed_C_bar - rPT_Feed_A_bar) > 0.25;

(* Out-of-range physical plausibility checks [0.0 - 6.0 bar] *)
bFeedP_SensorA_Fail := (rPT_Feed_A_bar < -0.2) OR (rPT_Feed_A_bar > 6.0);
bFeedP_SensorB_Fail := (rPT_Feed_B_bar < -0.2) OR (rPT_Feed_B_bar > 6.0);
bFeedP_SensorC_Fail := (rPT_Feed_C_bar < -0.2) OR (rPT_Feed_C_bar > 6.0);

IF (NOT bFeedP_SensorA_Fail) AND (NOT bFeedP_SensorB_Fail) AND (NOT bFeedP_SensorC_Fail) THEN
    (* All 3 sensors healthy: Median Selection *)
    IF (rPT_Feed_A_bar >= rPT_Feed_B_bar AND rPT_Feed_A_bar <= rPT_Feed_C_bar) OR 
       (rPT_Feed_A_bar <= rPT_Feed_B_bar AND rPT_Feed_A_bar >= rPT_Feed_C_bar) THEN
        rVoted_PFeed_bar := rPT_Feed_A_bar;
    ELSIF (rPT_Feed_B_bar >= rPT_Feed_A_bar AND rPT_Feed_B_bar <= rPT_Feed_C_bar) OR 
          (rPT_Feed_B_bar <= rPT_Feed_A_bar AND rPT_Feed_B_bar >= rPT_Feed_C_bar) THEN
        rVoted_PFeed_bar := rPT_Feed_B_bar;
    ELSE
        rVoted_PFeed_bar := rPT_Feed_C_bar;
    END_IF;
    bFeedP_Degraded_1oo2 := FALSE;
    bFeedP_TotalFailure := FALSE;
ELSIF bFeedP_SensorA_Fail AND (NOT bFeedP_SensorB_Fail) AND (NOT bFeedP_SensorC_Fail) THEN
    (* Sensor A failed: Average B and C *)
    rVoted_PFeed_bar := 0.5 * (rPT_Feed_B_bar + rPT_Feed_C_bar);
    bFeedP_Degraded_1oo2 := TRUE;
ELSIF bFeedP_SensorB_Fail AND (NOT bFeedP_SensorA_Fail) AND (NOT bFeedP_SensorC_Fail) THEN
    (* Sensor B failed: Average A and C *)
    rVoted_PFeed_bar := 0.5 * (rPT_Feed_A_bar + rPT_Feed_C_bar);
    bFeedP_Degraded_1oo2 := TRUE;
ELSIF bFeedP_SensorC_Fail AND (NOT bFeedP_SensorA_Fail) AND (NOT bFeedP_SensorB_Fail) THEN
    (* Sensor C failed: Average A and B *)
    rVoted_PFeed_bar := 0.5 * (rPT_Feed_A_bar + rPT_Feed_B_bar);
    bFeedP_Degraded_1oo2 := TRUE;
ELSE
    (* Multiple sensor failure: Safety shutdown trip *)
    bFeedP_TotalFailure := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0010; (* Feed Pressure TMR Critical Loss *)
END_IF;

tFeedP_DiscrepancyTimer(IN := (bFeedP_Dev_AB OR bFeedP_Dev_BC OR bFeedP_Dev_CA), PT := T#2S);
IF tFeedP_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0001; (* PT_Feed Cross-Channel Drift Warning *)
END_IF;

(* --- 2.2 RETENTATE LINE PRESSURE TRANSMITTERS (PT-102A/B/C) --- *)
bRetP_Dev_AB := ABS(rPT_Ret_A_bar - rPT_Ret_B_bar) > 0.25;
bRetP_Dev_BC := ABS(rPT_Ret_B_bar - rPT_Ret_C_bar) > 0.25;
bRetP_Dev_CA := ABS(rPT_Ret_C_bar - rPT_Ret_A_bar) > 0.25;

bRetP_SensorA_Fail := (rPT_Ret_A_bar < -0.2) OR (rPT_Ret_A_bar > 6.0);
bRetP_SensorB_Fail := (rPT_Ret_B_bar < -0.2) OR (rPT_Ret_B_bar > 6.0);
bRetP_SensorC_Fail := (rPT_Ret_C_bar < -0.2) OR (rPT_Ret_C_bar > 6.0);

IF (NOT bRetP_SensorA_Fail) AND (NOT bRetP_SensorB_Fail) AND (NOT bRetP_SensorC_Fail) THEN
    IF (rPT_Ret_A_bar >= rPT_Ret_B_bar AND rPT_Ret_A_bar <= rPT_Ret_C_bar) OR 
       (rPT_Ret_A_bar <= rPT_Ret_B_bar AND rPT_Ret_A_bar >= rPT_Ret_C_bar) THEN
        rVoted_PRet_bar := rPT_Ret_A_bar;
    ELSIF (rPT_Ret_B_bar >= rPT_Ret_A_bar AND rPT_Ret_B_bar <= rPT_Ret_C_bar) OR 
          (rPT_Ret_B_bar <= rPT_Ret_A_bar AND rPT_Ret_B_bar >= rPT_Ret_C_bar) THEN
        rVoted_PRet_bar := rPT_Ret_B_bar;
    ELSE
        rVoted_PRet_bar := rPT_Ret_C_bar;
    END_IF;
    bRetP_Degraded_1oo2 := FALSE;
    bRetP_TotalFailure := FALSE;
ELSIF bRetP_SensorA_Fail AND (NOT bRetP_SensorB_Fail) AND (NOT bRetP_SensorC_Fail) THEN
    rVoted_PRet_bar := 0.5 * (rPT_Ret_B_bar + rPT_Ret_C_bar);
    bRetP_Degraded_1oo2 := TRUE;
ELSIF bRetP_SensorB_Fail AND (NOT bRetP_SensorA_Fail) AND (NOT bRetP_SensorC_Fail) THEN
    rVoted_PRet_bar := 0.5 * (rPT_Ret_A_bar + rPT_Ret_C_bar);
    bRetP_Degraded_1oo2 := TRUE;
ELSIF bRetP_SensorC_Fail AND (NOT bRetP_SensorA_Fail) AND (NOT bRetP_SensorB_Fail) THEN
    rVoted_PRet_bar := 0.5 * (rPT_Ret_A_bar + rPT_Ret_B_bar);
    bRetP_Degraded_1oo2 := TRUE;
ELSE
    bRetP_TotalFailure := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0020; (* Retentate Pressure TMR Critical Loss *)
END_IF;

tRetP_DiscrepancyTimer(IN := (bRetP_Dev_AB OR bRetP_Dev_BC OR bRetP_Dev_CA), PT := T#2S);
IF tRetP_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0002; (* PT_Ret Cross-Channel Drift Warning *)
END_IF;

(* --- 2.3 PERMEATE LINE PRESSURE TRANSMITTERS (PT-103A/B/C) --- *)
bPermP_Dev_AB := ABS(rPT_Perm_A_bar - rPT_Perm_B_bar) > 0.20;
bPermP_Dev_BC := ABS(rPT_Perm_B_bar - rPT_Perm_C_bar) > 0.20;
bPermP_Dev_CA := ABS(rPT_Perm_C_bar - rPT_Perm_A_bar) > 0.20;

bPermP_SensorA_Fail := (rPT_Perm_A_bar < -0.2) OR (rPT_Perm_A_bar > 4.0);
bPermP_SensorB_Fail := (rPT_Perm_B_bar < -0.2) OR (rPT_Perm_B_bar > 4.0);
bPermP_SensorC_Fail := (rPT_Perm_C_bar < -0.2) OR (rPT_Perm_C_bar > 4.0);

IF (NOT bPermP_SensorA_Fail) AND (NOT bPermP_SensorB_Fail) AND (NOT bPermP_SensorC_Fail) THEN
    IF (rPT_Perm_A_bar >= rPT_Perm_B_bar AND rPT_Perm_A_bar <= rPT_Perm_C_bar) OR 
       (rPT_Perm_A_bar <= rPT_Perm_B_bar AND rPT_Perm_A_bar >= rPT_Perm_C_bar) THEN
        rVoted_PPerm_bar := rPT_Perm_A_bar;
    ELSIF (rPT_Perm_B_bar >= rPT_Perm_A_bar AND rPT_Perm_B_bar <= rPT_Perm_C_bar) OR 
          (rPT_Perm_B_bar <= rPT_Perm_A_bar AND rPT_Perm_B_bar >= rPT_Perm_C_bar) THEN
        rVoted_PPerm_bar := rPT_Perm_B_bar;
    ELSE
        rVoted_PPerm_bar := rPT_Perm_C_bar;
    END_IF;
    bPermP_Degraded_1oo2 := FALSE;
    bPermP_TotalFailure := FALSE;
ELSIF bPermP_SensorA_Fail AND (NOT bPermP_SensorB_Fail) AND (NOT bPermP_SensorC_Fail) THEN
    rVoted_PPerm_bar := 0.5 * (rPT_Perm_B_bar + rPT_Perm_C_bar);
    bPermP_Degraded_1oo2 := TRUE;
ELSIF bPermP_SensorB_Fail AND (NOT bPermP_SensorA_Fail) AND (NOT bPermP_SensorC_Fail) THEN
    rVoted_PPerm_bar := 0.5 * (rPT_Perm_A_bar + rPT_Perm_C_bar);
    bPermP_Degraded_1oo2 := TRUE;
ELSIF bPermP_SensorC_Fail AND (NOT bPermP_SensorA_Fail) AND (NOT bPermP_SensorB_Fail) THEN
    rVoted_PPerm_bar := 0.5 * (rPT_Perm_A_bar + rPT_Perm_B_bar);
    bPermP_Degraded_1oo2 := TRUE;
ELSE
    bPermP_TotalFailure := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0040; (* Permeate Pressure TMR Critical Loss *)
END_IF;

tPermP_DiscrepancyTimer(IN := (bPermP_Dev_AB OR bPermP_Dev_BC OR bPermP_Dev_CA), PT := T#2S);
IF tPermP_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0004; (* PT_Perm Cross-Channel Drift Warning *)
END_IF;

(* --- 2.4 IN-LINE CONDUCTIVITY SENSORS (CT-105A/B/C) --- *)
bCond_Dev_AB := ABS(rCT_Ret_A_mScm - rCT_Ret_B_mScm) > 0.85;
bCond_Dev_BC := ABS(rCT_Ret_B_mScm - rCT_Ret_C_mScm) > 0.85;
bCond_Dev_CA := ABS(rCT_Ret_C_mScm - rCT_Ret_A_mScm) > 0.85;

bCond_SensorA_Fail := (rCT_Ret_A_mScm < 0.0) OR (rCT_Ret_A_mScm > 150.0);
bCond_SensorB_Fail := (rCT_Ret_B_mScm < 0.0) OR (rCT_Ret_B_mScm > 150.0);
bCond_SensorC_Fail := (rCT_Ret_C_mScm < 0.0) OR (rCT_Ret_C_mScm > 150.0);

IF (NOT bCond_SensorA_Fail) AND (NOT bCond_SensorB_Fail) AND (NOT bCond_SensorC_Fail) THEN
    IF (rCT_Ret_A_mScm >= rCT_Ret_B_mScm AND rCT_Ret_A_mScm <= rCT_Ret_C_mScm) OR 
       (rCT_Ret_A_mScm <= rCT_Ret_B_mScm AND rCT_Ret_A_mScm >= rCT_Ret_C_mScm) THEN
        rVoted_Cond_mScm := rCT_Ret_A_mScm;
    ELSIF (rCT_Ret_B_mScm >= rCT_Ret_A_mScm AND rCT_Ret_B_mScm <= rCT_Ret_C_mScm) OR 
          (rCT_Ret_B_mScm <= rCT_Ret_A_mScm AND rCT_Ret_B_mScm >= rCT_Ret_C_mScm) THEN
        rVoted_Cond_mScm := rCT_Ret_B_mScm;
    ELSE
        rVoted_Cond_mScm := rCT_Ret_C_mScm;
    END_IF;
    bCond_Degraded_1oo2 := FALSE;
    bCond_TotalFailure := FALSE;
ELSIF bCond_SensorA_Fail AND (NOT bCond_SensorB_Fail) AND (NOT bCond_SensorC_Fail) THEN
    rVoted_Cond_mScm := 0.5 * (rCT_Ret_B_mScm + rCT_Ret_C_mScm);
    bCond_Degraded_1oo2 := TRUE;
ELSIF bCond_SensorB_Fail AND (NOT bCond_SensorA_Fail) AND (NOT bCond_SensorC_Fail) THEN
    rVoted_Cond_mScm := 0.5 * (rCT_Ret_A_mScm + rCT_Ret_C_mScm);
    bCond_Degraded_1oo2 := TRUE;
ELSIF bCond_SensorC_Fail AND (NOT bCond_SensorA_Fail) AND (NOT bCond_SensorB_Fail) THEN
    rVoted_Cond_mScm := 0.5 * (rCT_Ret_A_mScm + rCT_Ret_B_mScm);
    bCond_Degraded_1oo2 := TRUE;
ELSE
    bCond_TotalFailure := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0001; (* Conductivity TMR Critical Loss *)
END_IF;

tCond_DiscrepancyTimer(IN := (bCond_Dev_AB OR bCond_Dev_BC OR bCond_Dev_CA), PT := T#3S);
IF tCond_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0008; (* CT_Ret Cross-Channel Drift Warning *)
END_IF;

(* --- 2.5 IN-LINE pH ELECTRODES (AT-106A/B/C) --- *)
bpH_Dev_AB := ABS(rAT_pH_A - rAT_pH_B) > 0.15;
bpH_Dev_BC := ABS(rAT_pH_B - rAT_pH_C) > 0.15;
bpH_Dev_CA := ABS(rAT_pH_C - rAT_pH_A) > 0.15;

bpH_SensorA_Fail := (rAT_pH_A < 1.0) OR (rAT_pH_A > 14.0);
bpH_SensorB_Fail := (rAT_pH_B < 1.0) OR (rAT_pH_B > 14.0);
bpH_SensorC_Fail := (rAT_pH_C < 1.0) OR (rAT_pH_C > 14.0);

IF (NOT bpH_SensorA_Fail) AND (NOT bpH_SensorB_Fail) AND (NOT bpH_SensorC_Fail) THEN
    IF (rAT_pH_A >= rAT_pH_B AND rAT_pH_A <= rAT_pH_C) OR 
       (rAT_pH_A <= rAT_pH_B AND rAT_pH_A >= rAT_pH_C) THEN
        rVoted_pH := rAT_pH_A;
    ELSIF (rAT_pH_B >= rAT_pH_A AND rAT_pH_B <= rAT_pH_C) OR 
          (rAT_pH_B <= rAT_pH_A AND rAT_pH_B >= rAT_pH_C) THEN
        rVoted_pH := rAT_pH_B;
    ELSE
        rVoted_pH := rAT_pH_C;
    END_IF;
    bpH_Degraded_1oo2 := FALSE;
    bpH_TotalFailure := FALSE;
ELSIF bpH_SensorA_Fail AND (NOT bpH_SensorB_Fail) AND (NOT bpH_SensorC_Fail) THEN
    rVoted_pH := 0.5 * (rAT_pH_B + rAT_pH_C);
    bpH_Degraded_1oo2 := TRUE;
ELSIF bpH_SensorB_Fail AND (NOT bpH_SensorA_Fail) AND (NOT bpH_SensorC_Fail) THEN
    rVoted_pH := 0.5 * (rAT_pH_A + rAT_pH_C);
    bpH_Degraded_1oo2 := TRUE;
ELSIF bpH_SensorC_Fail AND (NOT bpH_SensorA_Fail) AND (NOT bpH_SensorB_Fail) THEN
    rVoted_pH := 0.5 * (rAT_pH_A + rAT_pH_B);
    bpH_Degraded_1oo2 := TRUE;
ELSE
    bpH_TotalFailure := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0002; (* pH Electrode TMR Critical Loss *)
END_IF;

tpH_DiscrepancyTimer(IN := (bpH_Dev_AB OR bpH_Dev_BC OR bpH_Dev_CA), PT := T#3S);
IF tpH_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0010; (* AT_pH Cross-Channel Drift Warning *)
END_IF;

(* --- 2.6 IN-SITU UV-280nm PROTEIN SPECTROPHOTOMETERS (AT-104A/B/C) --- *)
bUV_Dev_AB := ABS(rAT_UV280_A_mAU - rAT_UV280_B_mAU) > 45.0;
bUV_Dev_BC := ABS(rAT_UV280_B_mAU - rAT_UV280_C_mAU) > 45.0;
bUV_Dev_CA := ABS(rAT_UV280_C_mAU - rAT_UV280_A_mAU) > 45.0;

bUV_SensorA_Fail := (rAT_UV280_A_mAU < -5.0) OR (rAT_UV280_A_mAU > 3200.0);
bUV_SensorB_Fail := (rAT_UV280_B_mAU < -5.0) OR (rAT_UV280_B_mAU > 3200.0);
bUV_SensorC_Fail := (rAT_UV280_C_mAU < -5.0) OR (rAT_UV280_C_mAU > 3200.0);

IF (NOT bUV_SensorA_Fail) AND (NOT bUV_SensorB_Fail) AND (NOT bUV_SensorC_Fail) THEN
    IF (rAT_UV280_A_mAU >= rAT_UV280_B_mAU AND rAT_UV280_A_mAU <= rAT_UV280_C_mAU) OR 
       (rAT_UV280_A_mAU <= rAT_UV280_B_mAU AND rAT_UV280_A_mAU >= rAT_UV280_C_mAU) THEN
        rVoted_UV280_mAU := rAT_UV280_A_mAU;
    ELSIF (rAT_UV280_B_mAU >= rAT_UV280_A_mAU AND rAT_UV280_B_mAU <= rAT_UV280_C_mAU) OR 
          (rAT_UV280_B_mAU <= rAT_UV280_A_mAU AND rAT_UV280_B_mAU >= rAT_UV280_C_mAU) THEN
        rVoted_UV280_mAU := rAT_UV280_B_mAU;
    ELSE
        rVoted_UV280_mAU := rAT_UV280_C_mAU;
    END_IF;
    bUV_Degraded_1oo2 := FALSE;
    bUV_TotalFailure := FALSE;
ELSIF bUV_SensorA_Fail AND (NOT bUV_SensorB_Fail) AND (NOT bUV_SensorC_Fail) THEN
    rVoted_UV280_mAU := 0.5 * (rAT_UV280_B_mAU + rAT_UV280_C_mAU);
    bUV_Degraded_1oo2 := TRUE;
ELSIF bUV_SensorB_Fail AND (NOT bUV_SensorA_Fail) AND (NOT bUV_SensorC_Fail) THEN
    rVoted_UV280_mAU := 0.5 * (rAT_UV280_A_mAU + rAT_UV280_C_mAU);
    bUV_Degraded_1oo2 := TRUE;
ELSIF bUV_SensorC_Fail AND (NOT bUV_SensorA_Fail) AND (NOT bUV_SensorB_Fail) THEN
    rVoted_UV280_mAU := 0.5 * (rAT_UV280_A_mAU + rAT_UV280_B_mAU);
    bUV_Degraded_1oo2 := TRUE;
ELSE
    bUV_TotalFailure := TRUE;
    dwAlarmWord2 := dwAlarmWord2 OR 16#0000_0004; (* UV-280 Spectrophotometer TMR Critical Loss *)
END_IF;

tUV_DiscrepancyTimer(IN := (bUV_Dev_AB OR bUV_Dev_BC OR bUV_Dev_CA), PT := T#3S);
IF tUV_DiscrepancyTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0020; (* AT_UV280 Cross-Channel Drift Warning *)
END_IF;

(* --- 2.7 FIRST-ORDER LOW-PASS FILTERING FOR CONTINUOUS FLOWS & TEMPERATURE --- *)
rFiltered_FeedFlow_Lh := rFiltered_FeedFlow_Lh + rAlphaFlow * (rFT_Feed_Lh - rFiltered_FeedFlow_Lh);
rFiltered_PermFlow_Lh := rFiltered_PermFlow_Lh + rAlphaFlow * (rFT_Perm_Lh - rFiltered_PermFlow_Lh);
rFiltered_BufFlow_Lh  := rFiltered_BufFlow_Lh + rAlphaFlow * (rFT_Buf_Lh - rFiltered_BufFlow_Lh);
rFiltered_Visc_cP     := rFiltered_Visc_cP + rAlphaVisc * (rVT_Visc_cP - rFiltered_Visc_cP);
rFiltered_Temp_DegC   := rFiltered_Temp_DegC + rAlphaTemp * (rTT_Prod_DegC - rFiltered_Temp_DegC);
rFiltered_PermBreakthrough_mAU := rFiltered_PermBreakthrough_mAU + rAlphaUV * (rAT_UV280_Perm_mAU - rFiltered_PermBreakthrough_mAU);

(* Permeate UV Breakthrough Integrity Alarm (Filter Cassette Integrity Breach / Ruptured Membrane) *)
tPermeateBreakthroughTimer(IN := (rFiltered_PermBreakthrough_mAU > 35.0), PT := T#1S);
IF tPermeateBreakthroughTimer.Q THEN
    bPermeateBreakthroughAlarm := TRUE;
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0080; (* Cassette Integrity Rupture: Protein In Permeate *)
    IF bSystemRunning THEN
        iState := 100;
    END_IF;
ELSE
    bPermeateBreakthroughAlarm := FALSE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 3.0 Fluid Dynamics & Crossflow Shear Rate
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 3.0 CASSETTE HYDRODYNAMICS, TRANSMEMBRANE PRESSURE (TMP) & CHANNEL WALL SHEAR RATE         *)
(* ========================================================================================= *)
(* Calculates real-time Transmembrane Pressure (TMP), channel axial pressure drop Delta_P,   *)
(* channel wall shear rate gamma_w, and boundary fluid wall shear stress tau_w.               *)

(* 3.1 Transmembrane Pressure (TMP) Calculation *)
(* Standard Definition: TMP = 0.5 * (P_feed + P_retentate) - P_permeate *)
rObservedTMP_bar := 0.5 * (rVoted_PFeed_bar + rVoted_PRet_bar) - rVoted_PPerm_bar;
IF rObservedTMP_bar < 0.0 THEN
    rObservedTMP_bar := 0.0; (* Negative TMP clamp to prevent non-physical reverse flux *)
END_IF;

(* Overpressure Safety Trip *)
tOverpressureDebounceTimer(IN := (rObservedTMP_bar > (rMaxAllowableTMP_bar + 0.35)) OR (rVoted_PFeed_bar > 4.5), PT := T#250MS);
IF tOverpressureDebounceTimer.Q THEN
    dwAlarmWord1 := dwAlarmWord1 OR 16#0000_0100; (* Overpressure / Rupture Disk Hazard Trip *)
    IF bSystemRunning THEN
        iState := 100;
    END_IF;
END_IF;

(* 3.2 Channel Wall Shear Rate & Shear Stress (ASME BPE Rectangular Channel Slot Flow) *)
(* Shear rate for laminar flow in thin slit: gamma_w = 6 * Q / (W * H^2) *)
(* Converting Q [L/h] to [m^3/s]: Q_m3s = Q_Lh / (3600.0 * 1000.0) *)
IF (rChannelWidth_m > 0.001) AND (rChannelHeight_m > 0.0001) THEN
    rWallShearRate_s1 := (6.0 * (rFiltered_FeedFlow_Lh / 3600000.0)) / (rChannelWidth_m * rChannelHeight_m * rChannelHeight_m);
ELSE
    rWallShearRate_s1 := 1000.0;
END_IF;

(* Calculate Wall Shear Stress: tau_w = mu_ret * gamma_w *)
(* Viscosity conversion: 1 cP = 0.001 Pa*s *)
rWallShearStress_Pa := (rFiltered_Visc_cP * 0.001) * rWallShearRate_s1;

(* High Shear Stress Warning (Protects fragile mAb quaternary structures from shear denaturation) *)
tHighShearDebounceTimer(IN := (rWallShearRate_s1 > rMaxAllowableWallShear_s1), PT := T#500MS);
IF tHighShearDebounceTimer.Q THEN
    dwWarningWord := dwWarningWord OR 16#0000_0040; (* Excessive Wall Shear Rate Warning *)
END_IF;

(* 3.3 Permeate Volumetric Flux Calculation: J_v = FT_Perm / Membrane Area [LMH] *)
IF rMembraneArea_m2 > 0.01 THEN
    rObservedFlux_LMH := rFiltered_PermFlow_Lh / rMembraneArea_m2;
ELSE
    rObservedFlux_LMH := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 4.0 Gel-Polarization Boundary Layer Observer
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 4.0 GEL-POLARIZATION BOUNDARY LAYER & HYDRAULIC RESISTANCE OBSERVER                       *)
(* ========================================================================================= *)
(* First-principles Darcy-Starling resistance partitioning combined with Leveque mass        *)
(* transfer theory and dynamic Luenberger observer for online gel layer estimation.          *)

(* 4.1 Temperature-Compensated Permeate Viscosity (Empirical Water Viscosity Equation) *)
(* mu_w(T) = 1.784 / (1.0 + 0.0337*T + 0.000221*T^2) [cP] *)
IF rFiltered_Temp_DegC > 0.0 THEN
    rPermeateWaterViscosity_cP := 1.784 / (1.0 + 0.0337 * rFiltered_Temp_DegC + 0.000221 * rFiltered_Temp_DegC * rFiltered_Temp_DegC);
ELSE
    rPermeateWaterViscosity_cP := 1.002;
END_IF;

(* 4.2 Mooney Rheological High-Concentration Viscosity Formulation *)
(* Calculates expected bulk viscosity as protein concentrates up to 200 g/L *)
(* ln(eta_rel) = ([eta]*C) / (1 - (k/nu)*[eta]*C) *)
IF (rCalculatedProteinConc_gL > 0.1) AND ((1.0 - rCrowdingFactor * rIntrinsicViscosity_Lg * rCalculatedProteinConc_gL) > 0.05) THEN
    rRetentateFluidViscosity_cP := rPermeateWaterViscosity_cP * EXP(
        (rIntrinsicViscosity_Lg * rCalculatedProteinConc_gL) / 
        (1.0 - rCrowdingFactor * rIntrinsicViscosity_Lg * rCalculatedProteinConc_gL)
    );
ELSE
    rRetentateFluidViscosity_cP := rPermeateWaterViscosity_cP;
END_IF;

(* 4.3 Total Hydraulic Resistance Calculation (Darcy's Law) *)
(* J_v [m/s] = J_v [LMH] / 3600000.0 *)
(* R_tot = (TMP [Pa]) / (mu [Pa*s] * J_v [m/s]) *)
rObs_PermeateVelocity_ms := rObservedFlux_LMH / 3600000.0;
IF (rObs_PermeateVelocity_ms > 1.0E-7) AND (rObservedTMP_bar > 0.01) THEN
    rObservedHydraulicResistance_m1 := (rObservedTMP_bar * 100000.0) / ((rPermeateWaterViscosity_cP * 0.001) * rObs_PermeateVelocity_ms);
ELSE
    rObservedHydraulicResistance_m1 := rCleanMembraneResistance_m1;
END_IF;

(* 4.4 Leveque Boundary Layer Mass Transfer Coefficient *)
(* k_f = 0.819 * (gamma_w * D_ab^2 / L_ch)^(1/3) [m/s] *)
IF (rWallShearRate_s1 > 10.0) AND (rChannelLength_m > 0.05) THEN
    rObs_MassTransferCoeff_ms := 0.819 * EXPT(
        (rWallShearRate_s1 * rDiffusivity_m2s * rDiffusivity_m2s) / rChannelLength_m, 
        0.333333
    );
ELSE
    rObs_MassTransferCoeff_ms := 1.5E-5;
END_IF;

(* 4.5 Membrane Wall Protein Concentration (Stagnant Film Model) *)
(* Peclet Number: Pe = v_w / k_f *)
IF rObs_MassTransferCoeff_ms > 1.0E-7 THEN
    rObs_PecletNumber := rObs_PermeateVelocity_ms / rObs_MassTransferCoeff_ms;
    IF rObs_PecletNumber > 4.5 THEN rObs_PecletNumber := 4.5; END_IF; (* Upper bound to avoid numerical explosion *)
    rState_WallConc_gL := rCalculatedProteinConc_gL * EXP(rObs_PecletNumber);
ELSE
    rState_WallConc_gL := rCalculatedProteinConc_gL;
END_IF;

(* Concentration Polarization Resistance Estimation: R_cp *)
(* Osmotic backpressure / polarization resistance scaling *)
IF rState_WallConc_gL > rCalculatedProteinConc_gL THEN
    rState_Rcp_m1 := rCleanMembraneResistance_m1 * 0.45 * ((rState_WallConc_gL - rCalculatedProteinConc_gL) / 50.0);
ELSE
    rState_Rcp_m1 := 0.0;
END_IF;

(* 4.6 Reversible Gel Cake Consolidation & Dynamic Luenberger Observer *)
(* Gel layer begins precipitating when wall concentration C_w >= C_gel (e.g. 280 g/L) *)
IF rState_WallConc_gL >= rProteinGelConc_gL THEN
    bGelPolarizationWarning := TRUE;
    dwWarningWord := dwWarningWord OR 16#0000_0080; (* Gel Boundary Layer Polarization Warning *)
    
    (* Growth rate of gel cake thickness proportional to convective flux minus back-diffusion *)
    rState_GelThickness_m := rState_GelThickness_m + (
        ((rObs_PermeateVelocity_ms * rState_WallConc_gL) - (rObs_MassTransferCoeff_ms * (rState_WallConc_gL - rCalculatedProteinConc_gL))) /
        (rProteinDensity_kgm3 * 1000.0)
    ) * rCycleTime_sec;
    
    IF rState_GelThickness_m < 0.0 THEN rState_GelThickness_m := 0.0; END_IF;
    IF rState_GelThickness_m > 0.0001 THEN rState_GelThickness_m := 0.0001; END_IF; (* Max 100 um cake *)
    
    (* Cake resistance: R_gel = r_spec * rho_p * delta_gel *)
    rState_Rgel_m1 := rSpecificCakeResistance_mkg * rProteinDensity_kgm3 * rState_GelThickness_m;
ELSE
    bGelPolarizationWarning := FALSE;
    (* Cake relaxation / shear erosion under tangential crossflow *)
    IF rState_GelThickness_m > 0.0 THEN
        rState_GelThickness_m := rState_GelThickness_m - (0.0000005 * rWallShearStress_Pa * rCycleTime_sec);
        IF rState_GelThickness_m < 0.0 THEN rState_GelThickness_m := 0.0; END_IF;
        rState_Rgel_m1 := rSpecificCakeResistance_mkg * rProteinDensity_kgm3 * rState_GelThickness_m;
    ELSE
        rState_Rgel_m1 := 0.0;
    END_IF;
END_IF;

(* Luenberger Resistance Correction: Innovation between measured and modeled resistance *)
rTempSum := rState_Rm_m1 + rState_Rcp_m1 + rState_Rgel_m1 + rState_Rpore_m1;
IF (rObservedHydraulicResistance_m1 > 1.0E10) AND (rTempSum > 1.0E10) THEN
    rObs_Innovation_bar := (rObservedHydraulicResistance_m1 - rTempSum) * 1.0E-11;
    (* Update slow-moving irreversible pore fouling state R_pore *)
    rState_Rpore_m1 := rState_Rpore_m1 + (rLuenbergerGain_Rpore * rObs_Innovation_bar * rCycleTime_sec);
    IF rState_Rpore_m1 < 0.0 THEN rState_Rpore_m1 := 0.0; END_IF;
END_IF;

(* Export observed resistance and cake thickness metrics to block outputs *)
rObservedGelLayerResistance_m1 := rState_Rgel_m1;
rObservedGelLayerThickness_um  := rState_GelThickness_m * 1.0E6; (* Convert [m] to [um] *)

(* Critical Membrane Fouling Flag *)
bMembraneFoulingCritical := (rObservedHydraulicResistance_m1 > 1.2E12) OR (rState_Rgel_m1 > 6.5E11);
IF bMembraneFoulingCritical THEN
    dwWarningWord := dwWarningWord OR 16#0000_0100; (* Severe Membrane Hydraulic Fouling Active *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 5.0 UV-280 Spectrophotometric Protein Concentration
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 5.0 IN-SITU UV-280nm SPECTROPHOTOMETRIC PROTEIN CONCENTRATION FEEDBACK                    *)
(* ========================================================================================= *)
(* Precision Beer-Lambert optical absorbance processing with 340nm baseline Rayleigh         *)
(* scattering turbidity correction and dynamic recursive least-squares (RLS) calibration.    *)

(* 5.1 Rayleigh Scattering Turbidity Subtraction *)
(* Net Absorbance = A_280 - Baseline Offset [mAU] *)
rTempSum := rVoted_UV280_mAU - rBaselineTurbidityOffset_mAU;
IF rTempSum < 0.0 THEN
    rTempSum := 0.0;
END_IF;

(* 5.2 Beer-Lambert Protein Concentration Calculation *)
(* A = epsilon * b * C  -->  C [g/L] = (Net_mAU / 1000.0) / (epsilon [L/(g*cm)] * b [cm]) *)
IF (rExtinctionCoeff_L_g_cm > 0.1) AND (rFlowCellPathlength_cm > 0.001) THEN
    rCalculatedProteinConc_gL := (rTempSum / 1000.0) / (rExtinctionCoeff_L_g_cm * rFlowCellPathlength_cm);
ELSE
    rCalculatedProteinConc_gL := 0.0;
END_IF;

(* 5.3 Recursive Least Squares (RLS) Offline Lab Calibration Offset Adaptation *)
(* When an offline analytical lab reference is injected (> 0.5 g/L), adapt the optical baseline *)
IF (rAI_LabProteinRef_gL > 0.5) AND (bSystemRunning) THEN
    rTempGrad := rAI_LabProteinRef_gL - rCalculatedProteinConc_gL;
    IF ABS(rTempGrad) < 25.0 THEN (* Plausibility gate *)
        rBaselineTurbidityOffset_mAU := rBaselineTurbidityOffset_mAU - (rTempGrad * rRLS_Gain * 10.0 * rCycleTime_sec);
        IF rBaselineTurbidityOffset_mAU < 0.0 THEN rBaselineTurbidityOffset_mAU := 0.0; END_IF;
        IF rBaselineTurbidityOffset_mAU > 150.0 THEN rBaselineTurbidityOffset_mAU := 150.0; END_IF;
    END_IF;
END_IF;

(* Optical Saturation Warning (Detector nearing non-linear photodiode regime > 2800 mAU) *)
IF rVoted_UV280_mAU > 2800.0 THEN
    dwWarningWord := dwWarningWord OR 16#0000_0200; (* UV Spectrophotometer Optical Saturation Warning *)
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 6.0 Dual-Stage Conductivity & pH Buffer Exchange
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 6.0 DUAL-STAGE CONDUCTIVITY & pH DIAFILTRATION BUFFER EXCHANGE MODULATION                 *)
(* ========================================================================================= *)
(* Manages continuous isovolumetric diafiltration, integrating turnover volumes (DV),        *)
(* analytical solute clearance, and feedforward-feedback decoupling PID ratio titration.    *)

(* 6.1 Volume Integration & Batch Mass Balance *)
(* Integrated Volumes in Liters: V = Integral(Flow [L/h] / 3600.0 * dt) *)
rAccumulatedPermeateVolume_L := rAccumulatedPermeateVolume_L + (rFiltered_PermFlow_Lh / 3600.0) * rCycleTime_sec;
rAccumulatedBufferVolume_L   := rAccumulatedBufferVolume_L + (rFiltered_BufFlow_Lh / 3600.0) * rCycleTime_sec;
rAccumulatedFeedVolume_L     := rAccumulatedFeedVolume_L + (rFiltered_FeedFlow_Lh / 3600.0) * rCycleTime_sec;

(* Real-Time Retentate Batch Pool Volume Tracking *)
(* V_ret(t) = V_initial + V_feed_in - V_permeate_out + V_buffer_in *)
rCurrentRetentateVolume_L := rInitialBatchVolume_L + rAccumulatedFeedVolume_L - rAccumulatedPermeateVolume_L + rAccumulatedBufferVolume_L;
IF rCurrentRetentateVolume_L < 5.0 THEN
    rCurrentRetentateVolume_L := 5.0; (* Physical minimum skid hold-up limit *)
END_IF;

(* 6.2 Diafiltration Volumes (DV) Turnovers Completed *)
(* DV = Total Diafiltration Buffer Dosed / Current Retentate Volume *)
IF rCurrentRetentateVolume_L > 1.0 THEN
    rDiafiltrationVolumesCompleted_DV := rAccumulatedBufferVolume_L / rCurrentRetentateVolume_L;
ELSE
    rDiafiltrationVolumesCompleted_DV := 0.0;
END_IF;

(* 6.3 Decoupled Titration Control for Dual Buffers (Buffer A: Wash, Buffer B: Formulation) *)
(* Dual PID modulates Buffer A / B dosing ratio to track target conductivity and target pH *)
IF (iState = 50) THEN (* Actively in Diafiltration State *)
    (* Conductivity Error: e_cond = Target - Voted *)
    rTempGrad := rTargetConductivity_mScm - rVoted_Cond_mScm;
    rPID_Cond_Integral := rPID_Cond_Integral + (rTempGrad * 0.05 * rCycleTime_sec);
    IF rPID_Cond_Integral > 1.0 THEN rPID_Cond_Integral := 1.0; END_IF;
    IF rPID_Cond_Integral < -1.0 THEN rPID_Cond_Integral := -1.0; END_IF;

    (* pH Error: e_pH = Target - Voted *)
    rTempSum := rTargetpH - rVoted_pH;
    rPID_pH_Integral := rPID_pH_Integral + (rTempSum * 0.02 * rCycleTime_sec);
    IF rPID_pH_Integral > 1.0 THEN rPID_pH_Integral := 1.0; END_IF;
    IF rPID_pH_Integral < -1.0 THEN rPID_pH_Integral := -1.0; END_IF;

    (* Decoupled Ratio Calculation: Buffer B targets formulation conductivity/pH *)
    rBufferB_TargetRatio := 0.50 + (0.15 * rTempGrad) + rPID_Cond_Integral + (0.25 * rTempSum) + rPID_pH_Integral;
    IF rBufferB_TargetRatio > 1.0 THEN rBufferB_TargetRatio := 1.0; END_IF;
    IF rBufferB_TargetRatio < 0.0 THEN rBufferB_TargetRatio := 0.0; END_IF;
    rBufferA_TargetRatio := 1.0 - rBufferB_TargetRatio;

    (* Isovolumetric matching: Buffer dosing pump must equal permeate flow rate exactly *)
    (* FT_Buf_demand = FT_Perm_measured *)
    rBufferPumpA_Internal_pct := (rFiltered_PermFlow_Lh / 120.0) * rBufferA_TargetRatio * 100.0;
    rBufferPumpB_Internal_pct := (rFiltered_PermFlow_Lh / 120.0) * rBufferB_TargetRatio * 100.0;

    (* Diafiltration Completion Criteria *)
    IF (rDiafiltrationVolumesCompleted_DV >= rTargetDiafiltrationVols_DV) AND
       (ABS(rVoted_Cond_mScm - rTargetConductivity_mScm) < 0.35) AND
       (ABS(rVoted_pH - rTargetpH) < 0.10) THEN
        bDiafiltrationComplete := TRUE;
    END_IF;
ELSE
    rBufferPumpA_Internal_pct := 0.0;
    rBufferPumpB_Internal_pct := 0.0;
    rPID_Cond_Integral := 0.0;
    rPID_pH_Integral := 0.0;
END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 7.0 6-State Multivariable State-Space & Real-Time MPC
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 7.0 6-STATE MULTIVARIABLE STATE-SPACE DISCRETE MODEL & REAL-TIME MPC OPTIMIZATION         *)
(* ========================================================================================= *)
(* Continuous state estimation via discrete matrices A_d, B_d, C_d followed by real-time     *)
(* Model Predictive Control (MPC) quadratic cost minimization with actuator constraints.     *)

(* 7.1 Assemble Active State Vector from Voted / Observed Quantities *)
x_state[1] := rCalculatedProteinConc_gL;
x_state[2] := rState_WallConc_gL;
x_state[3] := rState_Rgel_m1 * 1.0E-11; (* Scale for numerical matrix conditioning *)
x_state[4] := rObservedFlux_LMH;
x_state[5] := rVoted_Cond_mScm;
x_state[6] := rVoted_pH;

(* 7.2 State-Space One-Step Ahead Prediction: x_hat(k+1) = A_d * x(k) + B_d * u(k) *)
FOR iRow := 1 TO 6 DO
    rTempSum := 0.0;
    FOR iCol := 1 TO 6 DO
        rTempSum := rTempSum + (A_d[iRow, iCol] * x_state[iCol]);
    END_FOR;
    FOR iCol := 1 TO 5 DO
        rTempSum := rTempSum + (B_d[iRow, iCol] * u_control[iCol]);
    END_FOR;
    x_hat[iRow] := rTempSum;
END_FOR;

(* 7.3 Real-Time Model Predictive Control Quadratic Cost Optimization *)
(* Solves: min J = (x_hat - x_sp)^T * Q * (x_hat - x_sp) + delta_u^T * R * delta_u *)
bMpcInOptimization := TRUE;

(* Calculate State Tracking Errors *)
x_error[1] := rTargetProteinConc_gL - x_hat[1];
x_error[2] := (rProteinGelConc_gL - 15.0) - x_hat[2]; (* Maintain wall conc 15 g/L below gelation *)
x_error[3] := 0.0 - x_hat[3];                         (* Desire zero gel cake resistance *)
x_error[4] := 55.0 - x_hat[4];                        (* Target optimal permeate flux 55 LMH *)
x_error[5] := rTargetConductivity_mScm - x_hat[5];
x_error[6] := rTargetpH - x_hat[6];

(* Gradient Descent Step on Actuator Demands *)
(* delta_u_j = - alpha * sum_i( 2 * Q_i * x_error_i * B_d[i, j] ) *)
FOR iCol := 1 TO 5 DO
    rTempGrad := 0.0;
    FOR iRow := 1 TO 6 DO
        rTempGrad := rTempGrad + (2.0 * Q_diag[iRow] * x_error[iRow] * B_d[iRow, iCol]);
    END_FOR;
    (* Apply damping regularization R_diag *)
    rTempGrad := rTempGrad - (2.0 * R_diag[iCol] * delta_u[iCol]);
    
    (* Update control change increment *)
    delta_u[iCol] := rMPC_GradientStepSize * rTempGrad;
    
    (* Slew rate and authority clamping on delta_u *)
    IF delta_u[iCol] > 15.0 THEN delta_u[iCol] := 15.0; END_IF;
    IF delta_u[iCol] < -15.0 THEN delta_u[iCol] := -15.0; END_IF;
    
    (* Advance actuator demand *)
    u_control[iCol] := u_control[iCol] + delta_u[iCol];
END_FOR;

(* Apply Physical Bound Constraints to State-Space Actuators *)
(* u[1]: Feed Pump Speed [rpm] (400 - 3200 rpm) *)
IF u_control[1] > 3200.0 THEN u_control[1] := 3200.0; END_IF;
IF u_control[1] < 400.0 THEN u_control[1] := 400.0; END_IF;

(* u[2]: Retentate Valve [pct] (5 - 95%) *)
IF u_control[2] > 95.0 THEN u_control[2] := 95.0; END_IF;
IF u_control[2] < 5.0 THEN u_control[2] := 5.0; END_IF;

(* u[3]: Permeate Control [rpm / pct] (0 - 600 rpm) *)
IF u_control[3] > 600.0 THEN u_control[3] := 600.0; END_IF;
IF u_control[3] < 0.0 THEN u_control[3] := 0.0; END_IF;

(* u[4], u[5]: Buffer Pumps A and B (0 - 100%) *)
IF u_control[4] > 100.0 THEN u_control[4] := 100.0; END_IF;
IF u_control[4] < 0.0 THEN u_control[4] := 0.0; END_IF;
IF u_control[5] > 100.0 THEN u_control[5] := 100.0; END_IF;
IF u_control[5] < 0.0 THEN u_control[5] := 0.0; END_IF;

bMpcInOptimization := FALSE;
""")

    # -------------------------------------------------------------------------
    # Section 8.0 Finite State Machine
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 8.0 MULTI-STAGE FINITE STATE MACHINE (FSM) SEQUENCE ENGINE                                *)
(* ========================================================================================= *)
(* 11-Stage autonomous sequence managing complete downstream UF/DF recipe lifecycle:         *)
(*   0: IDLE / SYSTEM PURGED & READY                                                         *)
(*  10: PRE-USE WFI RINSE & MEMBRANE INTEGRITY CHECK                                         *)
(*  20: BUFFER EQUILIBRATION & NWP BASELINE CALIBRATION                                      *)
(*  30: LOW-SHEAR PRODUCT PRIMING & AIR PURGE                                                *)
(*  40: PRIMARY CONCENTRATION (UF-1 FED-BATCH)                                               *)
(*  50: CONTINUOUS DIAFILTRATION (DF-1 ISOVOLUMETRIC BUFFER EXCHANGE)                         *)
(*  60: SECONDARY FINAL CONCENTRATION (UF-2 TARGET FORMULATION)                              *)
(*  70: PRODUCT HARVEST & BUFFER DISPLACEMENT CHASE                                          *)
(*  80: CLEAN-IN-PLACE (CIP) CAUSTIC SANITIZATION                                            *)
(*  90: POST-CIP WATER PERMEABILITY VALIDATION (NWP VERIFICATION)                            *)
(* 100: EMERGENCY TRIP & AUTOMATED DEPRESSURIZATION                                          *)

tStateTimer(IN := (iState = iPreviousState), PT := T#24H);
iPreviousState := iState;

CASE iState OF

    0: (* STATE 0: IDLE / SYSTEM PURGED & READY *)
        bSystemRunning := FALSE;
        bSystemReady := bSafetyRelayOK AND bEmergencyStop AND (NOT bSystemTripped) AND
                        (NOT bFeedP_TotalFailure) AND (NOT bRetP_TotalFailure);
        bConcentrationComplete := FALSE;
        bDiafiltrationComplete := FALSE;

        (* Park all actuators in safe neutral position *)
        rFeedPumpSpeed_Internal_rpm := 0.0;
        rRetentateValve_Internal_pct := 100.0; (* Fully open retentate loop *)
        rPermeatePump_Internal_rpm := 0.0;
        rPermeateValve_Internal_pct := 0.0;   (* Permeate line isolated *)
        rBufferPumpA_Internal_pct := 0.0;
        rBufferPumpB_Internal_pct := 0.0;

        IF bStartCycle AND bSystemReady THEN
            dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; (* Batch Started *)
            iState := 10; (* Advance to WFI Rinse & Integrity Test *)
        END_IF;

    10: (* STATE 10: PRE-USE WFI RINSE & MEMBRANE INTEGRITY CHECK *)
        bSystemRunning := TRUE;
        bSystemReady := FALSE;

        (* Gentle WFI flush to wet membrane and purge storage solution *)
        rFeedPumpSpeed_Internal_rpm := 850.0;
        rRetentateValve_Internal_pct := 70.0;
        rPermeateValve_Internal_pct := 40.0;
        rPermeatePump_Internal_rpm := 120.0;

        tIntegrityAirTimer(IN := TRUE, PT := T#120S);
        IF tIntegrityAirTimer.Q THEN
            tIntegrityAirTimer(IN := FALSE);
            iState := 20; (* Advance to Buffer Equilibration *)
        END_IF;

    20: (* STATE 20: BUFFER EQUILIBRATION & NWP BASELINE CALIBRATION *)
        bSystemRunning := TRUE;

        (* Flush with Conditioning Buffer A to calibrate baseline membrane resistance R_m *)
        rFeedPumpSpeed_Internal_rpm := 1450.0;
        rRetentateValve_Internal_pct := 55.0;
        rPermeateValve_Internal_pct := 60.0;
        rPermeatePump_Internal_rpm := 220.0;
        rBufferPumpA_Internal_pct := 45.0;

        tCleanWaterFluxTimer(IN := TRUE, PT := T#90S);
        IF tCleanWaterFluxTimer.Q THEN
            tCleanWaterFluxTimer(IN := FALSE);
            (* Capture Baseline Normalized Water Permeability (NWP) standardized to 20 deg C *)
            IF rObservedTMP_bar > 0.1 THEN
                rNormalizedWaterPermeability_LMHbar := (rObservedFlux_LMH / rObservedTMP_bar) * (rPermeateWaterViscosity_cP / rViscWater20C_cP);
                rCleanMembraneResistance_m1 := rObservedHydraulicResistance_m1;
                rState_Rm_m1 := rCleanMembraneResistance_m1;
            END_IF;
            iState := 30; (* Advance to Product Priming *)
        END_IF;

    30: (* STATE 30: LOW-SHEAR PRODUCT PRIMING & AIR PURGE *)
        bSystemRunning := TRUE;

        (* Low-shear displacement of buffer pool by incoming protein feed *)
        rFeedPumpSpeed_Internal_rpm := 600.0;
        rRetentateValve_Internal_pct := 90.0;
        rPermeateValve_Internal_pct := 0.0; (* Permeate closed during priming to prevent foul shock *)
        rPermeatePump_Internal_rpm := 0.0;

        tProductPrimingTimer(IN := TRUE, PT := T#60S);
        IF tProductPrimingTimer.Q AND (rCalculatedProteinConc_gL > 3.0) THEN
            tProductPrimingTimer(IN := FALSE);
            iState := 40; (* Advance to Primary Ultrafiltration *)
        END_IF;

    40: (* STATE 40: PRIMARY CONCENTRATION (UF-1 FED-BATCH) *)
        bSystemRunning := TRUE;

        (* Modulate feed pump and retentate valve via MPC controller demand *)
        rFeedPumpSpeed_Internal_rpm := u_control[1];
        rRetentateValve_Internal_pct := u_control[2];
        rPermeatePump_Internal_rpm := u_control[3];
        rPermeateValve_Internal_pct := 80.0;
        rBufferPumpA_Internal_pct := 0.0;
        rBufferPumpB_Internal_pct := 0.0;

        (* Target intermediate concentration (e.g. 45 g/L) before diafiltration *)
        IF (rCalculatedProteinConc_gL >= 45.0) OR (rCurrentRetentateVolume_L <= (rInitialBatchVolume_L * 0.35)) THEN
            iState := 50; (* Advance to Continuous Diafiltration *)
        END_IF;

    50: (* STATE 50: CONTINUOUS DIAFILTRATION (DF-1 ISOVOLUMETRIC BUFFER EXCHANGE) *)
        bSystemRunning := TRUE;

        (* Maintain constant volume buffer exchange while stripping host cell impurities *)
        rFeedPumpSpeed_Internal_rpm := u_control[1];
        rRetentateValve_Internal_pct := u_control[2];
        rPermeatePump_Internal_rpm := u_control[3];
        rPermeateValve_Internal_pct := 80.0;

        (* Buffer dosing managed dynamically in Section 6.0 *)
        IF bDiafiltrationComplete THEN
            iState := 60; (* Advance to Final Target Ultrafiltration *)
        END_IF;

    60: (* STATE 60: SECONDARY FINAL CONCENTRATION (UF-2 TARGET FORMULATION) *)
        bSystemRunning := TRUE;

        (* High-concentration ultrafiltration targeting final formulation concentration *)
        rFeedPumpSpeed_Internal_rpm := u_control[1];
        rRetentateValve_Internal_pct := u_control[2];
        rPermeatePump_Internal_rpm := u_control[3];
        rPermeateValve_Internal_pct := 75.0;
        rBufferPumpA_Internal_pct := 0.0;
        rBufferPumpB_Internal_pct := 0.0;

        IF rCalculatedProteinConc_gL >= rTargetProteinConc_gL THEN
            bConcentrationComplete := TRUE;
            iState := 70; (* Advance to Harvest & Product Recovery *)
        END_IF;

    70: (* STATE 70: PRODUCT HARVEST & BUFFER DISPLACEMENT CHASE *)
        bSystemRunning := TRUE;

        (* Drain retentate loop and displace product hold-up into bulk formulation tank *)
        rFeedPumpSpeed_Internal_rpm := 450.0;
        rRetentateValve_Internal_pct := 100.0;
        rPermeateValve_Internal_pct := 0.0;
        rPermeatePump_Internal_rpm := 0.0;
        rBufferPumpB_Internal_pct := 25.0; (* Small buffer chase volume *)

        tCIPFlushTimer(IN := TRUE, PT := T#45S);
        IF tCIPFlushTimer.Q THEN
            tCIPFlushTimer(IN := FALSE);
            iState := 80; (* Advance to Cleaning-In-Place *)
        END_IF;

    80: (* STATE 80: CLEAN-IN-PLACE (CIP) CAUSTIC SANITIZATION *)
        bSystemRunning := TRUE;

        (* Recirculate 0.5M NaOH at elevated temperature to dissolve fouling protein cake *)
        rFeedPumpSpeed_Internal_rpm := 1800.0;
        rRetentateValve_Internal_pct := 40.0;
        rPermeateValve_Internal_pct := 70.0;
        rPermeatePump_Internal_rpm := 300.0;

        tCIPFlushTimer(IN := TRUE, PT := T#180S);
        IF tCIPFlushTimer.Q THEN
            tCIPFlushTimer(IN := FALSE);
            iState := 90; (* Advance to Post-CIP NWP Verification *)
        END_IF;

    90: (* STATE 90: POST-CIP WATER PERMEABILITY VALIDATION (NWP VERIFICATION) *)
        bSystemRunning := TRUE;

        (* Verify membrane hydraulic permeability recovery > 90% *)
        rFeedPumpSpeed_Internal_rpm := 1450.0;
        rRetentateValve_Internal_pct := 55.0;
        rPermeateValve_Internal_pct := 60.0;
        rPermeatePump_Internal_rpm := 220.0;

        tCleanWaterFluxTimer(IN := TRUE, PT := T#60S);
        IF tCleanWaterFluxTimer.Q THEN
            tCleanWaterFluxTimer(IN := FALSE);
            IF rObservedTMP_bar > 0.1 THEN
                rNormalizedWaterPermeability_LMHbar := (rObservedFlux_LMH / rObservedTMP_bar) * (rPermeateWaterViscosity_cP / rViscWater20C_cP);
            END_IF;
            bSystemRunning := FALSE;
            iState := 0; (* Cycle complete: return to Idle standby *)
        END_IF;

    100: (* STATE 100: EMERGENCY TRIP & AUTOMATED DEPRESSURIZATION *)
        bSystemRunning := FALSE;
        bSystemReady := FALSE;
        bSystemTripped := TRUE;

        (* Immediate failsafe open of retentate line, isolate permeate, kill all pumps *)
        rFeedPumpSpeed_Internal_rpm := 0.0;
        rPermeatePump_Internal_rpm := 0.0;
        rBufferPumpA_Internal_pct := 0.0;
        rBufferPumpB_Internal_pct := 0.0;
        rPermeateValve_Internal_pct := 0.0;   (* Fast closure of permeate valve *)
        rRetentateValve_Internal_pct := 100.0; (* Failsafe wide open retentate backpressure *)

        (* Fault Reset and Unlatch Evaluation *)
        IF bResetFaults AND bSafetyRelayOK AND bEmergencyStop AND (dwAlarmWord1 = 16#0000_0000) THEN
            bSystemTripped := FALSE;
            iState := 0; (* Return to Idle *)
        END_IF;

END_CASE;
""")

    # -------------------------------------------------------------------------
    # Section 9.0 Graceful Degradation & Derate Management
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 9.0 GRACEFUL DEGRADATION, FOULING MITIGATION & ACTUATOR SLEW GOVERNOR                     *)
(* ========================================================================================= *)
(* Enforces protective derates, prevents pump cavitation under ultra-high fluid viscosity,   *)
(* smooths actuator mechanical transients, and manages degraded sensor redundancy.          *)

(* 9.1 Sensor Redundancy Degradation Warning Flag *)
bDegradedSensorMode := bFeedP_Degraded_1oo2 OR bRetP_Degraded_1oo2 OR bPermP_Degraded_1oo2 OR
                       bCond_Degraded_1oo2 OR bpH_Degraded_1oo2 OR bUV_Degraded_1oo2;

IF bDegradedSensorMode THEN
    dwWarningWord := dwWarningWord OR 16#0000_0400; (* Running in Degraded 1oo2 Sensor Mode *)
END_IF;

(* 9.2 High-Viscosity Feed Pump Speed Derate (Cavitation Protection) *)
(* As fluid viscosity rises above 8 cP, derate max feed pump speed to prevent NPSH starvation *)
IF rFiltered_Visc_cP > 8.0 THEN
    rTempSum := 3200.0 - ((rFiltered_Visc_cP - 8.0) * 120.0);
    IF rTempSum < 1000.0 THEN rTempSum := 1000.0; END_IF;
    IF rFeedPumpSpeed_Internal_rpm > rTempSum THEN
        rFeedPumpSpeed_Internal_rpm := rTempSum;
        dwWarningWord := dwWarningWord OR 16#0000_0800; (* Viscosity Speed Derate Active *)
    END_IF;
END_IF;

(* 9.3 Dynamic TMP Backoff on Boundary Layer Gel Encroachment *)
(* If wall concentration C_w exceeds 260 g/L, open retentate valve 10% to scour membrane *)
IF rState_WallConc_gL > 260.0 THEN
    rRetentateValve_Internal_pct := rRetentateValve_Internal_pct + 10.0;
    IF rRetentateValve_Internal_pct > 100.0 THEN rRetentateValve_Internal_pct := 100.0; END_IF;
END_IF;

(* 9.4 Slew-Rate Limiting on Actuator Commands *)
(* Feed Pump Slew *)
IF (rFeedPumpSpeed_Internal_rpm - rFeedPumpSpeed_rpm) > (rMaxSlew_FeedPump_rpms * rCycleTime_sec) THEN
    rFeedPumpSpeed_rpm := rFeedPumpSpeed_rpm + (rMaxSlew_FeedPump_rpms * rCycleTime_sec);
ELSIF (rFeedPumpSpeed_rpm - rFeedPumpSpeed_Internal_rpm) > (rMaxSlew_FeedPump_rpms * rCycleTime_sec) THEN
    rFeedPumpSpeed_rpm := rFeedPumpSpeed_rpm - (rMaxSlew_FeedPump_rpms * rCycleTime_sec);
ELSE
    rFeedPumpSpeed_rpm := rFeedPumpSpeed_Internal_rpm;
END_IF;

(* Retentate Valve Slew *)
IF (rRetentateValve_Internal_pct - rRetentateValve_pct) > (rMaxSlew_RetValve_pcts * rCycleTime_sec) THEN
    rRetentateValve_pct := rRetentateValve_pct + (rMaxSlew_RetValve_pcts * rCycleTime_sec);
ELSIF (rRetentateValve_pct - rRetentateValve_Internal_pct) > (rMaxSlew_RetValve_pcts * rCycleTime_sec) THEN
    rRetentateValve_pct := rRetentateValve_pct - (rMaxSlew_RetValve_pcts * rCycleTime_sec);
ELSE
    rRetentateValve_pct := rRetentateValve_Internal_pct;
END_IF;

(* Permeate Pump Slew *)
IF (rPermeatePump_Internal_rpm - rPermeatePumpSpeed_rpm) > (rMaxSlew_PermPump_rpms * rCycleTime_sec) THEN
    rPermeatePumpSpeed_rpm := rPermeatePumpSpeed_rpm + (rMaxSlew_PermPump_rpms * rCycleTime_sec);
ELSIF (rPermeatePumpSpeed_rpm - rPermeatePump_Internal_rpm) > (rMaxSlew_PermPump_rpms * rCycleTime_sec) THEN
    rPermeatePumpSpeed_rpm := rPermeatePumpSpeed_rpm - (rMaxSlew_PermPump_rpms * rCycleTime_sec);
ELSE
    rPermeatePumpSpeed_rpm := rPermeatePump_Internal_rpm;
END_IF;

(* Permeate Throttling Valve Position Transfer *)
rPermeateValve_pct := rPermeateValve_Internal_pct;

(* Buffer Metering Pumps Slew *)
IF (rBufferPumpA_Internal_pct - rBufferPumpA_pct) > (rMaxSlew_BufferPumps_pcts * rCycleTime_sec) THEN
    rBufferPumpA_pct := rBufferPumpA_pct + (rMaxSlew_BufferPumps_pcts * rCycleTime_sec);
ELSIF (rBufferPumpA_pct - rBufferPumpA_Internal_pct) > (rMaxSlew_BufferPumps_pcts * rCycleTime_sec) THEN
    rBufferPumpA_pct := rBufferPumpA_pct - (rMaxSlew_BufferPumps_pcts * rCycleTime_sec);
ELSE
    rBufferPumpA_pct := rBufferPumpA_Internal_pct;
END_IF;

IF (rBufferPumpB_Internal_pct - rBufferPumpB_pct) > (rMaxSlew_BufferPumps_pcts * rCycleTime_sec) THEN
    rBufferPumpB_pct := rBufferPumpB_pct + (rMaxSlew_BufferPumps_pcts * rCycleTime_sec);
ELSIF (rBufferPumpB_pct - rBufferPumpB_Internal_pct) > (rMaxSlew_BufferPumps_pcts * rCycleTime_sec) THEN
    rBufferPumpB_pct := rBufferPumpB_pct - (rMaxSlew_BufferPumps_pcts * rCycleTime_sec);
ELSE
    rBufferPumpB_pct := rBufferPumpB_Internal_pct;
END_IF;

(* Actuator Physical Clamping (0.0 to 100.0% / Max RPMs) *)
IF rFeedPumpSpeed_rpm < 0.0 THEN rFeedPumpSpeed_rpm := 0.0; END_IF;
IF rFeedPumpSpeed_rpm > 3500.0 THEN rFeedPumpSpeed_rpm := 3500.0; END_IF;
IF rRetentateValve_pct < 0.0 THEN rRetentateValve_pct := 0.0; END_IF;
IF rRetentateValve_pct > 100.0 THEN rRetentateValve_pct := 100.0; END_IF;
IF rPermeatePumpSpeed_rpm < 0.0 THEN rPermeatePumpSpeed_rpm := 0.0; END_IF;
IF rPermeatePumpSpeed_rpm > 800.0 THEN rPermeatePumpSpeed_rpm := 800.0; END_IF;
IF rPermeateValve_pct < 0.0 THEN rPermeateValve_pct := 0.0; END_IF;
IF rPermeateValve_pct > 100.0 THEN rPermeateValve_pct := 100.0; END_IF;
IF rBufferPumpA_pct < 0.0 THEN rBufferPumpA_pct := 0.0; END_IF;
IF rBufferPumpA_pct > 100.0 THEN rBufferPumpA_pct := 100.0; END_IF;
IF rBufferPumpB_pct < 0.0 THEN rBufferPumpB_pct := 0.0; END_IF;
IF rBufferPumpB_pct > 100.0 THEN rBufferPumpB_pct := 100.0; END_IF;
""")

    # -------------------------------------------------------------------------
    # Section 10.0 Bit-Packed Status Word & Alarm Assembly
    # -------------------------------------------------------------------------
    parts.append("""(* ========================================================================================= *)
(* 10.0 BIT-PACKED STATUS WORD & ALARM ASSEMBLY                                              *)
(* ========================================================================================= *)
(* Encodes skid operating state, sub-loop active flags, sensor health, and batch quality     *)
(* indicators into standardized 32-bit DWORD registers for SCADA / MES telemetry.           *)

dwSystemStatusWord := 16#0000_0000;
IF bSystemRunning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0001; END_IF;
IF bSystemReady THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0002; END_IF;
IF bSystemTripped THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0004; END_IF;
IF bConcentrationComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0008; END_IF;
IF bDiafiltrationComplete THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0010; END_IF;
IF bMembraneFoulingCritical THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0020; END_IF;
IF bPermeateBreakthroughAlarm THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0040; END_IF;
IF bGelPolarizationWarning THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0080; END_IF;
IF bDegradedSensorMode THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0100; END_IF;
IF bMpcInOptimization THEN dwSystemStatusWord := dwSystemStatusWord OR 16#0000_0200; END_IF;

(* Encode FSM State in upper word bits [16..26] *)
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

    return "\n".join(parts)

if __name__ == "__main__":
    code = build_code()
    print("Generated code length:", len(code))
