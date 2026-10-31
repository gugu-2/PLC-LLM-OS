import json
import os
import subprocess
import sys

def build_swro_st_code():
    # We will build the IEC 61131-3 Structured Text string with extreme technical depth
    # Target length: 60,000 - 80,000 characters
    parts = []
    
    # -------------------------------------------------------------------------
    # 1. Opening Declaration & Mega-Scale Header Documentation
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_WaterTreatment_SWRO_Desalination_PressureExchanger
(*
========================================================================================================================
  CYBER-PHYSICAL SYSTEMS AUTOMATION ARCHITECTURE & MUNICIPAL INFRASTRUCTURE CONTROL
  FACILITY: 250,000 m3/Day Seawater Reverse Osmosis (SWRO) Desalination Complex
  SUBSYSTEM: High-Pressure Reverse Osmosis Membrane Train with Isobaric Energy Recovery Devices (ERI PX),
             Advanced Multi-Variable Solution-Diffusion Model Predictive Control (MPC),
             Dynamic ASTM D4516 Membrane Fouling Diagnostics, and Automated Dual-Stage Clean-In-Place (CIP) Skid
  COMPLIANCE: IEC 61131-3 3rd Ed., IEC 61508 SIL-2/SIL-3 Safety Lifecycle, ISA-18.2 Alarm Management Standards
  CYCLE EXECUTION: Deterministic 10.0 ms Periodic Real-Time Task (100 Hz Synchronous Fieldbus Architecture)
========================================================================================================================

  1. THERMODYNAMIC & MEMBRANE MASS TRANSPORT GOVERNING EQUATIONS:
     Seawater desalination involves overcoming extreme natural osmotic pressure gradients across semi-permeable
     thin-film composite (TFC) aromatic polyamide membranes. Feed seawater salinity typically ranges from
     35,000 to 45,000 ppm (mg/L) Total Dissolved Solids (TDS).
     
     1.1 OSMOTIC PRESSURE MODELING (Pitzer & Van 't Hoff Formulations):
         The bulk osmotic pressure Pi as a function of TDS concentration C [g/L] and absolute temperature T [K]
         is modeled via the modified Pitzer electrolyte virial expansion approximated for SWRO conditions:
             Pi(C, T) = 0.0805 * (273.15 + T_celsius) * (C_tds / 1000.0) * phi_osmotic
         where phi_osmotic is the osmotic coefficient (0.925 to 0.940 for standard seawater at 25.0 deg C).
         At feed salinity of 40,000 ppm TDS and 25 deg C:
             Pi_feed = 0.0805 * 298.15 * 40.0 * 0.928 = 29.70 bar
         At 45.0% system recovery ratio Y, the brine reject concentrate reaches:
             C_brine = C_feed / (1.0 - Y) = 40,000 / (1.0 - 0.45) = 72,727 ppm TDS
             Pi_brine = 0.0805 * 298.15 * 72.727 * 0.935 = 54.43 bar
         The logarithmic mean bulk osmotic pressure across the membrane feed spacer channel is:
             Pi_bulk_mean = (Pi_brine - Pi_feed) / LN(Pi_brine / Pi_feed)

     1.2 SOLUTION-DIFFUSION TRANSPORT & CONCENTRATION POLARIZATION DYNAMICS:
         Membrane water flux J_w [m3/(m2*s)] and solute salt flux J_s [kg/(m2*s)] follow the classical
         Lonsdale-Merten-Riley solution-diffusion phenomenological formulation:
             J_w = A_w * ( Delta_P - Delta_Pi_surface )
             J_s = B_s * ( C_surface - C_permeate )
         where:
             Delta_P = P_feed_avg - P_permeate = 0.5 * (P_feed_inlet + P_brine_reject) - P_permeate
             Delta_Pi_surface = Pi_surface - Pi_permeate
         Solute build-up in the laminar boundary layer adjacent to the active polyamide layer generates
         severe concentration polarization (CP). The concentration polarization modulus beta_CP is governed by:
             beta_CP = C_surface / C_bulk = EXP( J_w / k_mass_transfer )
         where k_mass_transfer is the Sherwood-Reynolds-Schmidt mass transfer coefficient inside the feed spacer:
             Sh = (k_mass_transfer * d_hydraulic) / D_diffusion = 0.065 * (Re^0.875) * (Sc^0.25)
         Concentration polarization dramatically elevates the effective osmotic barrier:
             Pi_surface = beta_CP * Pi_bulk_mean
         yielding the net driving pressure (NDP):
             NDP = Delta_P - (beta_CP * Pi_bulk_mean - Pi_permeate)

     1.3 TEMPERATURE COMPENSATION COEFFICIENT (Arrhenius & ASTM D4516 Standards):
         Permeate water viscosity and polymer matrix free-volume expansion are compensated using the
         Arrhenius-type Temperature Correction Factor (TCF):
             TCF = EXP( E_activation_over_R * ( (1.0 / 298.15) - (1.0 / (273.15 + T_feed)) ) )
         with E_activation_over_R = 2640.0 K (FilmTec / DuPont SW30HR membrane standard).

     1.4 MEMBRANE FOULING NORMALIZATION (ASTM D4516 Methodology):
         Real-time performance degradation tracking isolates hydraulic compaction and foulant layer resistance
         from environmental temperature and salinity fluctuations:
             Q_permeate_norm = Q_permeate_actual * (NDP_reference / NDP_actual) * (TCF_reference / TCF_actual)
             Salt_Passage_norm = Salt_Passage_actual * (C_feed_ref / C_feed_actual) * (TCF_actual / TCF_ref) * (Q_act / Q_ref)

  2. ISOBARIC ENERGY RECOVERY DEVICE (ERD) DYNAMICS:
     The facility implements Energy Recovery Inc. (ERI) PX-Q300 pressure exchangers operating in parallel arrays.
     The isobaric rotor transfers high-pressure concentrate brine energy (65.0 bar) directly into incoming
     pre-treated seawater via ceramic rotor ducts with hydraulic transfer efficiencies exceeding 97.5%.
     2.1 Hydraulic Energy Recovery Efficiency:
         eta_PX = ( (Q_HP_out * P_HP_out) + (Q_LP_out * P_LP_out) ) /
                  ( (Q_brine_in * P_brine_in) + (Q_LP_in * P_LP_in) ) * 100.0 %
     2.2 Volumetric Brine-to-Feed Mixing Ratio:
         MR_PX = (TDS_HP_out - TDS_LP_in) / (TDS_brine_in - TDS_LP_in) * 100.0 %
     2.3 Booster Pump (BP) Head Differential:
         The high-pressure feed pump (HPP, driven by a 3.5 MW medium-voltage VFD) supplies 55% of the total feed
         flow at 68.0 bar, while the PX array supplies the remaining 45% at 64.5 bar. A dedicated Booster Pump (BP)
         supplies the required 3.5 bar differential head to match the primary high-pressure feed manifold.

  3. PRE-TREATMENT & CHEMICAL DOSING SKID DYNAMICS:
     3.1 Sodium Bisulfite (SBS, NaHSO3) Dechlorination:
         Polyamide membranes are irreversibly oxidized and degraded by free chlorine residual (> 0.05 ppm).
         Stoichiometric redox neutralization reaction:
             NaHSO3 + Cl2 + H2O -> NaHSO4 + 2 HCl
         Oxidation-Reduction Potential (ORP) is regulated via 2oo3 voting below 200.0 mV.
         Any breakthrough above 280.0 mV triggers immediate emergency train isolation.
     3.2 Antiscalant Threshold Inhibition:
         Phosphonate / polycarboxylate polymers dosed at 2.5 to 3.5 ppm inhibit precipitation of sparingly soluble
         salts (CaSO4, BaSO4, SrSO4, CaCO3, SiO2) in supersaturated concentrate brine channels.
     3.3 Coagulant Pre-Treatment:
         Ferric chloride (FeCl3) dosed ahead of dual-media pressure filters to maintain Silt Density Index (SDI15 < 3.0).

  4. CLEAN-IN-PLACE (CIP) DUAL-STAGE PROTOCOL:
     Stage 1: Low-pressure acid circulation (Citric acid 2.0% wt, pH 2.2 to 2.8, 35 deg C) for carbonate scale dissolution.
     Stage 2: Low-pressure alkaline circulation (NaOH + Na-EDTA 1.0% wt + SDS surfactant, pH 10.8 to 11.5, 38 deg C)
              for bio-fouling, extracellular polymeric substances (EPS), and colloidal organic removal.
     Displacement Flush: Permeate water displacement flush at 2.0 bar to purge chemical effluent without osmotic shock.

  5. MULTI-VARIABLE STATE-SPACE & RECEDING-HORIZON MPC FORMULATION:
     Discrete-time 16th-order state-space plant dynamics:
         x[k+1] = A * x[k] + B * u[k]
         y[k]   = C * x[k] + D * u[k]
     Receding-horizon quadratic cost functional minimization:
         J = Sum_{i=1..16} Q_i * (x_i - x_target_i)^2 + Sum_{j=1..8} R_j * u_j^2 + Sum_{j=1..8} S_j * (u_j - u_prev_j)^2
     incorporating projected gradient descent with hard actuator saturation bounds and rate-of-change limiters.
*)
""")

    # -------------------------------------------------------------------------
    # 2. VAR_INPUT Block
    # -------------------------------------------------------------------------
    parts.append("""
VAR_INPUT
    (* Master Execution & Safety Interlocks *)
    bEnableMaster                   : BOOL;     (* Master supervisory enable command for SWRO train [bool] *)
    bEmergencyStop                  : BOOL;     (* Hardwired emergency stop safety circuit status (Active LOW) [bool] *)
    bAcknowledgeAlarms              : BOOL;     (* Operator manual alarm reset and latch clearance pushbutton [bool] *)
    bCIP_InitiateRequest            : BOOL;     (* Operator or supervisory request to start automated CIP cleaning [bool] *)
    bPreservationModeReq            : BOOL;     (* Request to transition train into long-term chemical preservation [bool] *)

    (* 2oo3 Triple Modular Redundancy High-Pressure Feed Transmitters [bar] *)
    rFeedPressure_RawA_bar          : REAL;     (* 2oo3 Train HP feed pressure transmitter Channel A [bar] *)
    rFeedPressure_RawB_bar          : REAL;     (* 2oo3 Train HP feed pressure transmitter Channel B [bar] *)
    rFeedPressure_RawC_bar          : REAL;     (* 2oo3 Train HP feed pressure transmitter Channel C [bar] *)

    (* 2oo3 Triple Modular Redundancy High-Pressure Concentrate Brine Transmitters [bar] *)
    rBrinePressure_RawA_bar         : REAL;     (* 2oo3 Concentrate reject brine pressure transmitter Channel A [bar] *)
    rBrinePressure_RawB_bar         : REAL;     (* 2oo3 Concentrate reject brine pressure transmitter Channel B [bar] *)
    rBrinePressure_RawC_bar         : REAL;     (* 2oo3 Concentrate reject brine pressure transmitter Channel C [bar] *)

    (* 2oo3 Triple Modular Redundancy Permeate Conductivity Analyzers [uS/cm] *)
    rPermeateCond_RawA_uS           : REAL;     (* 2oo3 Permeate electrical conductivity analyzer Channel A [uS/cm] *)
    rPermeateCond_RawB_uS           : REAL;     (* 2oo3 Permeate electrical conductivity analyzer Channel B [uS/cm] *)
    rPermeateCond_RawC_uS           : REAL;     (* 2oo3 Permeate electrical conductivity analyzer Channel C [uS/cm] *)

    (* 2oo3 Triple Modular Redundancy Feed Oxidation-Reduction Potential (ORP) Analyzers [mV] *)
    rFeedORP_RawA_mV                : REAL;     (* 2oo3 Seawater inlet ORP redox analyzer Channel A [mV] *)
    rFeedORP_RawB_mV                : REAL;     (* 2oo3 Seawater inlet ORP redox analyzer Channel B [mV] *)
    rFeedORP_RawC_mV                : REAL;     (* 2oo3 Seawater inlet ORP redox analyzer Channel C [mV] *)

    (* Hydraulic Process Volumetric Flow Transmitters [m3/h] *)
    rFeedFlow_HPP_m3h               : REAL;     (* High-Pressure Pump suction volumetric flow transmitter [m3/h] *)
    rFeedFlow_ERD_m3h               : REAL;     (* Isobaric PX low-pressure feed delivery flow transmitter [m3/h] *)
    rPermeateFlow_m3h               : REAL;     (* Combined train permeate product volumetric flow transmitter [m3/h] *)
    rBrineFlow_m3h                  : REAL;     (* High-pressure concentrate reject brine volumetric flow transmitter [m3/h] *)

    (* Chemical, Physical & Environmental Process Variables *)
    rFeedSalinity_TDS_ppm           : REAL;     (* Raw seawater inlet Total Dissolved Solids concentration [ppm] *)
    rPermeatePressure_bar           : REAL;     (* Permeate product collection manifold backpressure [bar] *)
    rFeedTemperature_degC           : REAL;     (* Raw seawater feed process fluid temperature [deg C] *)
    rFeed_pH                        : REAL;     (* Raw seawater pre-treatment pH glass electrode analyzer [pH] *)
    rFeed_Turbidity_NTU             : REAL;     (* Cartridge filter effluent optical turbidity analyzer [NTU] *)
    rSiltDensityIndex_SDI15         : REAL;     (* Online dynamic 15-minute Silt Density Index monitor [SDI] *)

    (* Isobaric Energy Recovery Device (ERI PX) Diagnostics *)
    rPX_HP_OutPressure_bar          : REAL;     (* Isobaric PX high-pressure seawater outlet header transmitter [bar] *)
    rPX_LP_OutPressure_bar          : REAL;     (* Isobaric PX low-pressure brine discharge to outfall transmitter [bar] *)
    rPX_RotorSpeed_RPM              : REAL;     (* Isobaric PX ceramic rotor acoustic/magnetic tachometer [rpm] *)

    (* Clean-In-Place (CIP) Skid Instrumentation *)
    rCIP_TankTemperature_degC       : REAL;     (* Clean-In-Place chemical mixing tank process temperature [deg C] *)
    rCIP_Tank_pH                    : REAL;     (* Clean-In-Place chemical circulation loop pH transmitter [pH] *)
    rCIP_CirculationFlow_m3h        : REAL;     (* Clean-In-Place chemical delivery recirculation flow meter [m3/h] *)

    (* Supervisory Setpoints & Operational Targets *)
    rTargetRecovery_pct             : REAL;     (* Target train hydraulic water recovery ratio [%] (e.g. 42.0 to 48.0%) *)
    rTargetPermeateFlow_m3h         : REAL;     (* Target train permeate production delivery flow [m3/h] (e.g. 434.0 m3/h) *)
    rMaxAllowableSEC_kWh_m3         : REAL;     (* Maximum allowable Specific Energy Consumption limit [kWh/m3] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 3. VAR_OUTPUT Block
    # -------------------------------------------------------------------------
    parts.append("""
VAR_OUTPUT
    (* Operational State & Permissive Indicators *)
    bTrainRunning                   : BOOL;     (* RO desalination train online and delivering potable water [bool] *)
    bPermeateValveOpen              : BOOL;     (* Permeate product water header delivery valve open command [bool] *)
    bPermeateDivertOpen             : BOOL;     (* Permeate off-spec reject diversion valve open command [bool] *)
    bHighPressureSafetyDumpOpen     : BOOL;     (* Emergency high-pressure fast hydraulic relief valve active [bool] *)
    bTrainTripAlarm                 : BOOL;     (* Master process critical shutdown trip alarm active [bool] *)
    bWarningActive                  : BOOL;     (* Process warning active requiring operator intervention [bool] *)
    bDegradedSensorMode             : BOOL;     (* Train operating under degraded sensor redundancy mode [bool] *)
    bCIP_Active                     : BOOL;     (* Clean-In-Place chemical cleaning sequence active [bool] *)

    (* Continuous Actuator Setpoint Commands *)
    rHPP_SpeedCmd_pct               : REAL;     (* High-Pressure Pump 3.5 MW medium-voltage VFD speed reference [%] *)
    rBP_SpeedCmd_pct                : REAL;     (* Booster Pump VFD speed reference command [%] *)
    rERD_RejectThrottleCmd_pct      : REAL;     (* Isobaric ERD high-pressure concentrate throttling valve command [%] *)
    rPermeateBackpressCmd_pct       : REAL;     (* Permeate collection manifold throttling valve command [%] *)
    rDosingSBS_StrokeCmd_pct        : REAL;     (* Sodium bisulfite dechlorination dosing pump stroke speed [%] *)
    rDosingAntiscalantCmd_pct       : REAL;     (* Antiscalant chemical dosing pump stroke speed command [%] *)
    rDosingCoagulantCmd_pct         : REAL;     (* Ferric chloride coagulant dosing pump stroke speed command [%] *)
    rCIP_PumpSpeedCmd_pct           : REAL;     (* Clean-In-Place chemical circulation pump VFD speed command [%] *)

    (* Validated & 2oo3 Voted Process Feedback Telemetry *)
    rVotedFeedPressure_bar          : REAL;     (* 2oo3 Voted train high-pressure feed manifold pressure [bar] *)
    rVotedBrinePressure_bar         : REAL;     (* 2oo3 Voted high-pressure concentrate brine pressure [bar] *)
    rVotedPermeateCond_uS           : REAL;     (* 2oo3 Voted permeate product water electrical conductivity [uS/cm] *)
    rVotedFeedORP_mV                : REAL;     (* 2oo3 Voted raw seawater Oxidation-Reduction Potential [mV] *)
    rPermeateTDS_ppm                : REAL;     (* Calculated permeate product water Total Dissolved Solids [ppm] *)
    rSaltRejection_pct              : REAL;     (* Membrane train overall salt rejection efficiency [%] *)
    rActualRecovery_pct             : REAL;     (* Real-time calculated train hydraulic water recovery ratio [%] *)

    (* Thermodynamic & Membrane Fouling Diagnostic Metrics *)
    rNetDrivingPressure_bar         : REAL;     (* Calculated Net Driving Pressure (NDP) across active membranes [bar] *)
    rMembraneDifferentialPress_bar  : REAL;     (* Differential hydraulic pressure drop across membrane vessels [bar] *)
    rNormPermeateFlow_m3h           : REAL;     (* ASTM D4516 Normalized permeate volumetric flow rate [m3/h] *)
    rNormSaltPassage_pct            : REAL;     (* ASTM D4516 Normalized membrane solute salt passage [%] *)
    rSpecificEnergyConsump_kWh_m3   : REAL;     (* Real-time Specific Energy Consumption (SEC) per m3 produced [kWh/m3] *)
    rPX_Efficiency_pct              : REAL;     (* Isobaric PX pressure exchanger hydraulic transfer efficiency [%] *)
    rPX_MixingRatio_pct             : REAL;     (* Isobaric PX volumetric brine-to-seawater mixing ratio [%] *)

    (* Diagnostic Registers & FSM State Telemetry *)
    dwAlarmWord_Primary             : DWORD;    (* ISA-18.2 Bit-packed primary process alarm word [dword] *)
    dwAlarmWord_Secondary           : DWORD;    (* ISA-18.2 Bit-packed secondary trip & interlock status word [dword] *)
    dwDiagnosticStatus              : DWORD;    (* TMR sensor voting and subsystem diagnostic health word [dword] *)
    iActiveState                    : INT;      (* Current active state index of 12-stage operational FSM [int] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 4. VAR Block (Matrices, Arrays, Constants, Timers, Internal States)
    # -------------------------------------------------------------------------
    parts.append("""
VAR
    (* Architectural & Physical Thermodynamic Constants *)
    c_rSamplingPeriod_sec           : REAL := 0.010;    (* Deterministic execution task period Ts = 10.0 ms (100 Hz) *)
    c_rPi                           : REAL := 3.141592653589793;
    c_rRefTemp_Kelvin               : REAL := 298.15;   (* Standard reference thermodynamic temperature (25.0 deg C) [K] *)
    c_rArrheniusActivation_K        : REAL := 2640.0;   (* FilmTec Arrhenius activation energy parameter E_a / R [K] *)
    c_rOsmoticCoeff_Pitzer          : REAL := 0.0805;   (* Van 't Hoff / Pitzer empirical osmotic multiplier [bar*L/(g*K)] *)
    c_rOsmoticVirialPhi             : REAL := 0.928;    (* Standard seawater osmotic activity virial factor [-] *)
    c_rConductivityToTDS_Factor     : REAL := 0.525;    (* Permeate electrical conductivity to TDS conversion factor [(ppm)/(uS/cm)] *)
    c_rTotalMembraneArea_m2         : REAL := 22500.0;  (* Total active membrane polyamide surface area per train [m2] *)
    c_rNominalPermeability_Aw       : REAL := 1.65E-11; (* Pure water hydraulic permeability coefficient [m3/(m2*s*Pa)] *)
    c_rNominalSolutePerm_Bs         : REAL := 2.40E-8;  (* Solute salt transport permeability coefficient [m/s] *)
    c_rMassTransferCoeff_km         : REAL := 2.50E-5;  (* Feed spacer boundary layer mass transfer velocity [m/s] *)
    c_rMaxDesignPressure_bar        : REAL := 82.0;     (* Mechanical burst pressure limit of pressure vessels [bar] *)
    c_rMinSuctionPressure_bar       : REAL := 2.2;      (* Minimum suction pressure to prevent HPP cavitation [bar] *)

    (* 2oo3 Triple Modular Redundancy Voting Limits & Tolerances *)
    c_rDiscrepancyLimit_FeedP_bar   : REAL := 2.5;      (* Discrepancy threshold between feed pressure transmitters [bar] *)
    c_rDiscrepancyLimit_BrineP_bar  : REAL := 2.5;      (* Discrepancy threshold between brine pressure transmitters [bar] *)
    c_rDiscrepancyLimit_Cond_uS     : REAL := 45.0;     (* Discrepancy threshold between permeate conductivity probes [uS/cm] *)
    c_rDiscrepancyLimit_ORP_mV      : REAL := 35.0;     (* Discrepancy threshold between redox ORP electrodes [mV] *)

    (* 2oo3 Voting Fault Counters and Health Status Flags *)
    iFaultCounter_FeedP_A           : INT := 0;
    iFaultCounter_FeedP_B           : INT := 0;
    iFaultCounter_FeedP_C           : INT := 0;
    bFeedP_Degraded                 : BOOL := FALSE;
    bFeedP_VoterFailed              : BOOL := FALSE;

    iFaultCounter_BrineP_A          : INT := 0;
    iFaultCounter_BrineP_B          : INT := 0;
    iFaultCounter_BrineP_C          : INT := 0;
    bBrineP_Degraded                : BOOL := FALSE;
    bBrineP_VoterFailed             : BOOL := FALSE;

    iFaultCounter_PermCond_A        : INT := 0;
    iFaultCounter_PermCond_B        : INT := 0;
    iFaultCounter_PermCond_C        : INT := 0;
    bPermCond_Degraded              : BOOL := FALSE;
    bPermCond_VoterFailed           : BOOL := FALSE;

    iFaultCounter_FeedORP_A         : INT := 0;
    iFaultCounter_FeedORP_B         : INT := 0;
    iFaultCounter_FeedORP_C         : INT := 0;
    bFeedORP_Degraded               : BOOL := FALSE;
    bFeedORP_VoterFailed            : BOOL := FALSE;

    (* ASTM D4516 Baseline Reference Performance Vectors *)
    rRef_NDP_bar                    : REAL := 18.5;     (* Baseline reference Net Driving Pressure [bar] *)
    rRef_PermeateFlow_m3h           : REAL := 434.0;    (* Baseline reference permeate production flow rate [m3/h] *)
    rRef_SaltPassage_pct            : REAL := 0.28;     (* Baseline reference membrane solute salt passage [%] *)
    rRef_FeedSalinity_ppm           : REAL := 38500.0;  (* Baseline reference raw seawater feed salinity [ppm] *)
    rRef_FeedTemp_degC              : REAL := 25.0;     (* Baseline reference raw seawater temperature [deg C] *)

    (* Calculated Intermediate Thermodynamic & Hydraulic Variables *)
    rCalc_FeedAbsoluteTemp_K        : REAL := 298.15;
    rCalc_TCF                       : REAL := 1.0;
    rCalc_PiFeed_bar                : REAL := 0.0;
    rCalc_PiBrine_bar               : REAL := 0.0;
    rCalc_PiBulkMean_bar            : REAL := 0.0;
    rCalc_WaterFlux_m_s             : REAL := 0.0;
    rCalc_ConcPolarizationModulus   : REAL := 1.15;
    rCalc_PiSurface_bar             : REAL := 0.0;
    rCalc_PiPermeate_bar            : REAL := 0.0;
    rCalc_AverageFeedPressure_bar   : REAL := 0.0;
    rCalc_SaltPassage_pct           : REAL := 0.0;
    rCalc_HPP_ElectricalPower_kW    : REAL := 0.0;
    rCalc_BP_ElectricalPower_kW     : REAL := 0.0;
    rCalc_TotalHydraulicPower_kW    : REAL := 0.0;

    (* Discrete-Time State-Space Model Matrices (16 States x 16 States, 16 x 8 Inputs) *)
    matA                            : ARRAY[1..16, 1..16] OF REAL;
    matB                            : ARRAY[1..16, 1..8] OF REAL;
    matC                            : ARRAY[1..8, 1..16] OF REAL;
    matD                            : ARRAY[1..8, 1..8] OF REAL;

    (* State-Space Vectors & Target References *)
    vecState_x                      : ARRAY[1..16] OF REAL;
    vecStateNext_x                  : ARRAY[1..16] OF REAL;
    vecStateTarget_x                : ARRAY[1..16] OF REAL;
    vecStateError_x                 : ARRAY[1..16] OF REAL;

    (* Control Actuator Vectors & Optimization Limits *)
    vecControl_u                    : ARRAY[1..8] OF REAL;
    vecControlPrev_u                : ARRAY[1..8] OF REAL;
    vecControlDelta_du              : ARRAY[1..8] OF REAL;
    vecControlMin_u                 : ARRAY[1..8] OF REAL;
    vecControlMax_u                 : ARRAY[1..8] OF REAL;
    vecDeltaMax_du                  : ARRAY[1..8] OF REAL;

    (* Receding-Horizon MPC Quadratic Cost Matrices & Gradient Variables *)
    vecCostQ                        : ARRAY[1..16] OF REAL;
    vecCostR                        : ARRAY[1..8] OF REAL;
    vecCostS                        : ARRAY[1..8] OF REAL;
    vecGradient_g                   : ARRAY[1..8] OF REAL;
    rMPC_StepSizeAlpha              : REAL := 0.0150;
    iMPC_MaxIterations              : INT := 6;
    bMatricesInitialized            : BOOL := FALSE;

    (* 12-Stage Operational Finite State Machine Timers & Internal Sequence Registers *)
    iState                          : INT := 0;
    tStateTimer                     : TON;
    tDeaerationTimer                : TON;
    tSoftRampTimer                  : TON;
    tCIP_AcidRecircTimer            : TON;
    tCIP_AcidSoakTimer              : TON;
    tCIP_AlkalineRecircTimer        : TON;
    tCIP_AlkalineSoakTimer          : TON;
    tDisplacementFlushTimer         : TON;
    tTripDelayTimer                 : TON;
    rRampRpmAccumulator             : REAL := 0.0;
    iCIP_SubPhase                   : INT := 0;

    (* ISA-18.2 Process Alarm Trip Thresholds & Deadbands *)
    c_rAlarm_FeedP_HH_bar           : REAL := 78.5;
    c_rAlarm_FeedP_H_bar            : REAL := 74.0;
    c_rAlarm_FeedP_L_bar            : REAL := 50.0;
    c_rAlarm_FeedP_LL_bar           : REAL := 35.0;
    c_rDeadband_FeedP_bar           : REAL := 1.0;

    c_rAlarm_BrineP_HH_bar          : REAL := 72.0;
    c_rAlarm_BrineP_H_bar           : REAL := 68.0;
    c_rAlarm_BrineP_L_bar           : REAL := 45.0;
    c_rAlarm_BrineP_LL_bar          : REAL := 30.0;
    c_rDeadband_BrineP_bar          : REAL := 1.0;

    c_rAlarm_MembraneDP_HH_bar      : REAL := 4.5;
    c_rAlarm_MembraneDP_H_bar       : REAL := 3.5;
    c_rDeadband_MembraneDP_bar      : REAL := 0.2;

    c_rAlarm_PermCond_HH_uS         : REAL := 450.0;
    c_rAlarm_PermCond_H_uS          : REAL := 350.0;
    c_rDeadband_PermCond_uS         : REAL := 10.0;

    c_rAlarm_FeedORP_HH_mV          : REAL := 280.0;
    c_rAlarm_FeedORP_H_mV           : REAL := 220.0;
    c_rDeadband_FeedORP_mV          : REAL := 10.0;

    c_rAlarm_PX_DP_HH_bar           : REAL := 2.8;
    c_rAlarm_PX_DP_H_bar            : REAL := 2.0;
    c_rDeadband_PX_DP_bar           : REAL := 0.15;

    c_rAlarm_SDI_HH                 : REAL := 4.5;
    c_rAlarm_SDI_H                  : REAL := 3.2;
    c_rDeadband_SDI                 : REAL := 0.2;

    c_rAlarm_SEC_HH_kWh             : REAL := 3.80;
    c_rAlarm_SEC_H_kWh              : REAL := 3.20;
    c_rDeadband_SEC_kWh             : REAL := 0.10;

    (* ISA-18.2 Alarm Qualification Verification Filter Counters *)
    iAlarmFilter_FeedP_HH           : INT := 0;
    iAlarmFilter_FeedP_LL           : INT := 0;
    iAlarmFilter_BrineP_HH          : INT := 0;
    iAlarmFilter_MembraneDP_HH      : INT := 0;
    iAlarmFilter_PermCond_HH        : INT := 0;
    iAlarmFilter_FeedORP_HH         : INT := 0;
    iAlarmFilter_PX_DP_HH           : INT := 0;

    (* Diagnostic Iterators & Scratchpad Counters *)
    iLoopIdx                        : INT := 1;
    jLoopIdx                        : INT := 1;
    kLoopIdx                        : INT := 1;
END_VAR
""")

    # -------------------------------------------------------------------------
    # 5. SECTION 1: HARD SAFETY TRIP & EMERGENCY DEPRESSURIZATION INTERLOCK
    # -------------------------------------------------------------------------
    parts.append("""
(* ====================================================================================================================
   SECTION 1: HARD SAFETY CIRCUIT, EMERGENCY TRIP & FAST HYDRAULIC DEPRESSURIZATION
   ==================================================================================================================== *)
IF NOT bEmergencyStop THEN
    bTrainRunning               := FALSE;
    bPermeateValveOpen          := FALSE;
    bPermeateDivertOpen         := TRUE;
    bHighPressureSafetyDumpOpen := TRUE;   (* Instantly open fast hydraulic relief bypass dump *)
    bTrainTripAlarm             := TRUE;
    bWarningActive              := FALSE;
    bCIP_Active                 := FALSE;
    
    (* Hard emergency command de-energization *)
    rHPP_SpeedCmd_pct           := 0.0;    (* Trip 3.5 MW MV VFD on High-Pressure Feed Pump *)
    rBP_SpeedCmd_pct            := 0.0;    (* Trip Booster Pump VFD *)
    rERD_RejectThrottleCmd_pct  := 100.0;  (* Fully open concentrate throttle to dump hydraulic energy *)
    rPermeateBackpressCmd_pct   := 0.0;
    rDosingSBS_StrokeCmd_pct    := 0.0;
    rDosingAntiscalantCmd_pct   := 0.0;
    rDosingCoagulantCmd_pct     := 0.0;
    rCIP_PumpSpeedCmd_pct       := 0.0;

    (* Set ISA-18.2 trip latch in secondary alarm word *)
    dwAlarmWord_Secondary.0     := TRUE;   (* Bit 0: HARDWIRED_EMERGENCY_STOP_TRIPPED *)
    
    iState := 120;                         (* Lock into emergency hydraulic dump state *)
    iActiveState := iState;
    RETURN;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 6. SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING LOGIC
    # -------------------------------------------------------------------------
    parts.append("""
(* ====================================================================================================================
   SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & PLAUSIBILITY ARBITRATION
   ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------
   2.1 HIGH-PRESSURE MEMBRANE FEED TRANSMITTER 2oo3 VOTER (PT_Feed_RawA, RawB, RawC) [bar]
   ------------------------------------------------------------------------------------------------- *)
IF (ABS(rFeedPressure_RawA_bar - rFeedPressure_RawB_bar) <= c_rDiscrepancyLimit_FeedP_bar) THEN
    IF (ABS(rFeedPressure_RawA_bar - rFeedPressure_RawC_bar) <= c_rDiscrepancyLimit_FeedP_bar) THEN
        (* All three transmitters in mutual consensus: compute median value *)
        IF (rFeedPressure_RawA_bar >= rFeedPressure_RawB_bar AND rFeedPressure_RawA_bar <= rFeedPressure_RawC_bar) OR
           (rFeedPressure_RawA_bar <= rFeedPressure_RawB_bar AND rFeedPressure_RawA_bar >= rFeedPressure_RawC_bar) THEN
            rVotedFeedPressure_bar := rFeedPressure_RawA_bar;
        ELSIF (rFeedPressure_RawB_bar >= rFeedPressure_RawA_bar AND rFeedPressure_RawB_bar <= rFeedPressure_RawC_bar) OR
              (rFeedPressure_RawB_bar <= rFeedPressure_RawA_bar AND rFeedPressure_RawB_bar >= rFeedPressure_RawC_bar) THEN
            rVotedFeedPressure_bar := rFeedPressure_RawB_bar;
        ELSE
            rVotedFeedPressure_bar := rFeedPressure_RawC_bar;
        END_IF;
        iFaultCounter_FeedP_A := 0;
        iFaultCounter_FeedP_B := 0;
        iFaultCounter_FeedP_C := 0;
        bFeedP_Degraded := FALSE;
    ELSE
        (* Channel C diverges: arbitrate average of Channels A & B *)
        rVotedFeedPressure_bar := 0.5 * (rFeedPressure_RawA_bar + rFeedPressure_RawB_bar);
        iFaultCounter_FeedP_C := iFaultCounter_FeedP_C + 1;
        bFeedP_Degraded := TRUE;
    END_IF;
ELSIF (ABS(rFeedPressure_RawA_bar - rFeedPressure_RawC_bar) <= c_rDiscrepancyLimit_FeedP_bar) THEN
    (* Channel B diverges: arbitrate average of Channels A & C *)
    rVotedFeedPressure_bar := 0.5 * (rFeedPressure_RawA_bar + rFeedPressure_RawC_bar);
    iFaultCounter_FeedP_B := iFaultCounter_FeedP_B + 1;
    bFeedP_Degraded := TRUE;
ELSIF (ABS(rFeedPressure_RawB_bar - rFeedPressure_RawC_bar) <= c_rDiscrepancyLimit_FeedP_bar) THEN
    (* Channel A diverges: arbitrate average of Channels B & C *)
    rVotedFeedPressure_bar := 0.5 * (rFeedPressure_RawB_bar + rFeedPressure_RawC_bar);
    iFaultCounter_FeedP_A := iFaultCounter_FeedP_A + 1;
    bFeedP_Degraded := TRUE;
ELSE
    (* Total voter disagreement: retain Channel C and latch voter failure flag *)
    rVotedFeedPressure_bar := rFeedPressure_RawC_bar;
    bFeedP_VoterFailed := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
   2.2 HIGH-PRESSURE CONCENTRATE BRINE TRANSMITTER 2oo3 VOTER (PT_Brine_RawA, RawB, RawC) [bar]
   ------------------------------------------------------------------------------------------------- *)
IF (ABS(rBrinePressure_RawA_bar - rBrinePressure_RawB_bar) <= c_rDiscrepancyLimit_BrineP_bar) THEN
    IF (ABS(rBrinePressure_RawA_bar - rBrinePressure_RawC_bar) <= c_rDiscrepancyLimit_BrineP_bar) THEN
        (* All three transmitters in consensus: compute median *)
        IF (rBrinePressure_RawA_bar >= rBrinePressure_RawB_bar AND rBrinePressure_RawA_bar <= rBrinePressure_RawC_bar) OR
           (rBrinePressure_RawA_bar <= rBrinePressure_RawB_bar AND rBrinePressure_RawA_bar >= rBrinePressure_RawC_bar) THEN
            rVotedBrinePressure_bar := rBrinePressure_RawA_bar;
        ELSIF (rBrinePressure_RawB_bar >= rBrinePressure_RawA_bar AND rBrinePressure_RawB_bar <= rBrinePressure_RawC_bar) OR
              (rBrinePressure_RawB_bar <= rBrinePressure_RawA_bar AND rBrinePressure_RawB_bar >= rBrinePressure_RawC_bar) THEN
            rVotedBrinePressure_bar := rBrinePressure_RawB_bar;
        ELSE
            rVotedBrinePressure_bar := rBrinePressure_RawC_bar;
        END_IF;
        iFaultCounter_BrineP_A := 0;
        iFaultCounter_BrineP_B := 0;
        iFaultCounter_BrineP_C := 0;
        bBrineP_Degraded := FALSE;
    ELSE
        (* Channel C diverges *)
        rVotedBrinePressure_bar := 0.5 * (rBrinePressure_RawA_bar + rBrinePressure_RawB_bar);
        iFaultCounter_BrineP_C := iFaultCounter_BrineP_C + 1;
        bBrineP_Degraded := TRUE;
    END_IF;
ELSIF (ABS(rBrinePressure_RawA_bar - rBrinePressure_RawC_bar) <= c_rDiscrepancyLimit_BrineP_bar) THEN
    (* Channel B diverges *)
    rVotedBrinePressure_bar := 0.5 * (rBrinePressure_RawA_bar + rBrinePressure_RawC_bar);
    iFaultCounter_BrineP_B := iFaultCounter_FeedP_B + 1;
    bBrineP_Degraded := TRUE;
ELSIF (ABS(rBrinePressure_RawB_bar - rBrinePressure_RawC_bar) <= c_rDiscrepancyLimit_BrineP_bar) THEN
    (* Channel A diverges *)
    rVotedBrinePressure_bar := 0.5 * (rBrinePressure_RawB_bar + rBrinePressure_RawC_bar);
    iFaultCounter_BrineP_A := iFaultCounter_BrineP_A + 1;
    bBrineP_Degraded := TRUE;
ELSE
    rVotedBrinePressure_bar := rBrinePressure_RawC_bar;
    bBrineP_VoterFailed := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
   2.3 PERMEATE ELECTRICAL CONDUCTIVITY 2oo3 VOTER (AT_PermCond_RawA, RawB, RawC) [uS/cm]
   ------------------------------------------------------------------------------------------------- *)
IF (ABS(rPermeateCond_RawA_uS - rPermeateCond_RawB_uS) <= c_rDiscrepancyLimit_Cond_uS) THEN
    IF (ABS(rPermeateCond_RawA_uS - rPermeateCond_RawC_uS) <= c_rDiscrepancyLimit_Cond_uS) THEN
        (* All three analyzers in consensus: median *)
        IF (rPermeateCond_RawA_uS >= rPermeateCond_RawB_uS AND rPermeateCond_RawA_uS <= rPermeateCond_RawC_uS) OR
           (rPermeateCond_RawA_uS <= rPermeateCond_RawB_uS AND rPermeateCond_RawA_uS >= rPermeateCond_RawC_uS) THEN
            rVotedPermeateCond_uS := rPermeateCond_RawA_uS;
        ELSIF (rPermeateCond_RawB_uS >= rPermeateCond_RawA_uS AND rPermeateCond_RawB_uS <= rPermeateCond_RawC_uS) OR
              (rPermeateCond_RawB_uS <= rPermeateCond_RawA_uS AND rPermeateCond_RawB_uS >= rPermeateCond_RawC_uS) THEN
            rVotedPermeateCond_uS := rPermeateCond_RawB_uS;
        ELSE
            rVotedPermeateCond_uS := rPermeateCond_RawC_uS;
        END_IF;
        iFaultCounter_PermCond_A := 0;
        iFaultCounter_PermCond_B := 0;
        iFaultCounter_PermCond_C := 0;
        bPermCond_Degraded := FALSE;
    ELSE
        rVotedPermeateCond_uS := 0.5 * (rPermeateCond_RawA_uS + rPermeateCond_RawB_uS);
        iFaultCounter_PermCond_C := iFaultCounter_PermCond_C + 1;
        bPermCond_Degraded := TRUE;
    END_IF;
ELSIF (ABS(rPermeateCond_RawA_uS - rPermeateCond_RawC_uS) <= c_rDiscrepancyLimit_Cond_uS) THEN
    rVotedPermeateCond_uS := 0.5 * (rPermeateCond_RawA_uS + rPermeateCond_RawC_uS);
    iFaultCounter_PermCond_B := iFaultCounter_PermCond_B + 1;
    bPermCond_Degraded := TRUE;
ELSIF (ABS(rPermeateCond_RawB_uS - rPermeateCond_RawC_uS) <= c_rDiscrepancyLimit_Cond_uS) THEN
    rVotedPermeateCond_uS := 0.5 * (rPermeateCond_RawB_uS + rPermeateCond_RawC_uS);
    iFaultCounter_PermCond_A := iFaultCounter_PermCond_A + 1;
    bPermCond_Degraded := TRUE;
ELSE
    rVotedPermeateCond_uS := rPermeateCond_RawC_uS;
    bPermCond_VoterFailed := TRUE;
END_IF;

(* -------------------------------------------------------------------------------------------------
   2.4 SEAWATER FEED ORP (REDOX DECHLORINATION) 2oo3 VOTER (AT_FeedORP_RawA, RawB, RawC) [mV]
   ------------------------------------------------------------------------------------------------- *)
IF (ABS(rFeedORP_RawA_mV - rFeedORP_RawB_mV) <= c_rDiscrepancyLimit_ORP_mV) THEN
    IF (ABS(rFeedORP_RawA_mV - rFeedORP_RawC_mV) <= c_rDiscrepancyLimit_ORP_mV) THEN
        (* All three ORP electrodes healthy: compute median *)
        IF (rFeedORP_RawA_mV >= rFeedORP_RawB_mV AND rFeedORP_RawA_mV <= rFeedORP_RawC_mV) OR
           (rFeedORP_RawA_mV <= rFeedORP_RawB_mV AND rFeedORP_RawA_mV >= rFeedORP_RawC_mV) THEN
            rVotedFeedORP_mV := rFeedORP_RawA_mV;
        ELSIF (rFeedORP_RawB_mV >= rFeedORP_RawA_mV AND rFeedORP_RawB_mV <= rFeedORP_RawC_mV) OR
              (rFeedORP_RawB_mV <= rFeedORP_RawA_mV AND rFeedORP_RawB_mV >= rFeedORP_RawC_mV) THEN
            rVotedFeedORP_mV := rFeedORP_RawB_mV;
        ELSE
            rVotedFeedORP_mV := rFeedORP_RawC_mV;
        END_IF;
        iFaultCounter_FeedORP_A := 0;
        iFaultCounter_FeedORP_B := 0;
        iFaultCounter_FeedORP_C := 0;
        bFeedORP_Degraded := FALSE;
    ELSE
        rVotedFeedORP_mV := 0.5 * (rFeedORP_RawA_mV + rFeedORP_RawB_mV);
        iFaultCounter_FeedORP_C := iFaultCounter_FeedORP_C + 1;
        bFeedORP_Degraded := TRUE;
    END_IF;
ELSIF (ABS(rFeedORP_RawA_mV - rFeedORP_RawC_mV) <= c_rDiscrepancyLimit_ORP_mV) THEN
    rVotedFeedORP_mV := 0.5 * (rFeedORP_RawA_mV + rFeedORP_RawC_mV);
    iFaultCounter_FeedORP_B := iFaultCounter_FeedORP_B + 1;
    bFeedORP_Degraded := TRUE;
ELSIF (ABS(rFeedORP_RawB_mV - rFeedORP_RawC_mV) <= c_rDiscrepancyLimit_ORP_mV) THEN
    rVotedFeedORP_mV := 0.5 * (rFeedORP_RawB_mV + rFeedORP_RawC_mV);
    iFaultCounter_FeedORP_A := iFaultCounter_FeedORP_A + 1;
    bFeedORP_Degraded := TRUE;
ELSE
    rVotedFeedORP_mV := rFeedORP_RawC_mV;
    bFeedORP_VoterFailed := TRUE;
END_IF;

(* Pack TMR sensor health telemetry bits into dwDiagnosticStatus *)
dwDiagnosticStatus.0  := (iFaultCounter_FeedP_A > 15);
dwDiagnosticStatus.1  := (iFaultCounter_FeedP_B > 15);
dwDiagnosticStatus.2  := (iFaultCounter_FeedP_C > 15);
dwDiagnosticStatus.3  := bFeedP_Degraded;
dwDiagnosticStatus.4  := (iFaultCounter_BrineP_A > 15);
dwDiagnosticStatus.5  := (iFaultCounter_BrineP_B > 15);
dwDiagnosticStatus.6  := (iFaultCounter_BrineP_C > 15);
dwDiagnosticStatus.7  := bBrineP_Degraded;
dwDiagnosticStatus.8  := (iFaultCounter_PermCond_A > 15);
dwDiagnosticStatus.9  := (iFaultCounter_PermCond_B > 15);
dwDiagnosticStatus.10 := (iFaultCounter_PermCond_C > 15);
dwDiagnosticStatus.11 := bPermCond_Degraded;
dwDiagnosticStatus.12 := (iFaultCounter_FeedORP_A > 15);
dwDiagnosticStatus.13 := (iFaultCounter_FeedORP_B > 15);
dwDiagnosticStatus.14 := (iFaultCounter_FeedORP_C > 15);
dwDiagnosticStatus.15 := bFeedORP_Degraded;
dwDiagnosticStatus.16 := bFeedP_VoterFailed;
dwDiagnosticStatus.17 := bBrineP_VoterFailed;
dwDiagnosticStatus.18 := bPermCond_VoterFailed;
dwDiagnosticStatus.19 := bFeedORP_VoterFailed;

bDegradedSensorMode := bFeedP_Degraded OR bBrineP_Degraded OR bPermCond_Degraded OR bFeedORP_Degraded;
""")

    # -------------------------------------------------------------------------
    # 7. SECTION 3: MEMBRANE THERMODYNAMICS, OSMOTIC PRESSURE & ASTM D4516
    # -------------------------------------------------------------------------
    parts.append("""
(* ====================================================================================================================
   SECTION 3: MEMBRANE HYDRAULICS, THERMODYNAMIC OSMOTIC PRESSURE & ASTM D4516 NORMALIZATION
   ==================================================================================================================== *)

(* 3.1 Temperature-Compensated Arrhenius Viscosity & Free-Volume Factor *)
rCalc_FeedAbsoluteTemp_K := 273.15 + rFeedTemperature_degC;
IF rCalc_FeedAbsoluteTemp_K < 274.0 THEN
    rCalc_FeedAbsoluteTemp_K := 274.0;
END_IF;
rCalc_TCF := EXP(c_rArrheniusActivation_K * ((1.0 / c_rRefTemp_Kelvin) - (1.0 / rCalc_FeedAbsoluteTemp_K)));
IF rCalc_TCF < 0.25 THEN rCalc_TCF := 0.25; END_IF;
IF rCalc_TCF > 2.50 THEN rCalc_TCF := 2.50; END_IF;

(* 3.2 Product Water TDS Conversion & Salt Rejection Efficiency *)
rPermeateTDS_ppm := rVotedPermeateCond_uS * c_rConductivityToTDS_Factor;
IF rFeedSalinity_TDS_ppm > 100.0 THEN
    rSaltRejection_pct := (1.0 - (rPermeateTDS_ppm / rFeedSalinity_TDS_ppm)) * 100.0;
    rCalc_SaltPassage_pct := (rPermeateTDS_ppm / rFeedSalinity_TDS_ppm) * 100.0;
ELSE
    rSaltRejection_pct := 99.80;
    rCalc_SaltPassage_pct := 0.20;
END_IF;

(* 3.3 System Water Recovery Ratio *)
IF (rFeedFlow_HPP_m3h + rFeedFlow_ERD_m3h) > 10.0 THEN
    rActualRecovery_pct := (rPermeateFlow_m3h / (rFeedFlow_HPP_m3h + rFeedFlow_ERD_m3h)) * 100.0;
ELSE
    rActualRecovery_pct := 0.0;
END_IF;

(* 3.4 Pitzer Osmotic Pressure Formulations *)
rCalc_PiFeed_bar := c_rOsmoticCoeff_Pitzer * rCalc_FeedAbsoluteTemp_K * (rFeedSalinity_TDS_ppm / 1000.0) * c_rOsmoticVirialPhi;

IF rActualRecovery_pct < 85.0 AND rActualRecovery_pct > 5.0 THEN
    rCalc_PiBrine_bar := c_rOsmoticCoeff_Pitzer * rCalc_FeedAbsoluteTemp_K * ((rFeedSalinity_TDS_ppm / (1.0 - (rActualRecovery_pct / 100.0))) / 1000.0) * (c_rOsmoticVirialPhi + 0.012);
ELSE
    rCalc_PiBrine_bar := rCalc_PiFeed_bar * 1.82;
END_IF;

IF rCalc_PiBrine_bar > rCalc_PiFeed_bar AND rCalc_PiFeed_bar > 1.0 THEN
    rCalc_PiBulkMean_bar := (rCalc_PiBrine_bar - rCalc_PiFeed_bar) / LN(rCalc_PiBrine_bar / rCalc_PiFeed_bar);
ELSE
    rCalc_PiBulkMean_bar := 0.5 * (rCalc_PiFeed_bar + rCalc_PiBrine_bar);
END_IF;

(* 3.5 Solution-Diffusion Water Flux & Concentration Polarization Modulus *)
rCalc_WaterFlux_m_s := (rPermeateFlow_m3h / 3600.0) / c_rTotalMembraneArea_m2;
rCalc_ConcPolarizationModulus := EXP(rCalc_WaterFlux_m_s / c_rMassTransferCoeff_km);
IF rCalc_ConcPolarizationModulus < 1.02 THEN rCalc_ConcPolarizationModulus := 1.02; END_IF;
IF rCalc_ConcPolarizationModulus > 1.45 THEN rCalc_ConcPolarizationModulus := 1.45; END_IF;

rCalc_PiSurface_bar := rCalc_ConcPolarizationModulus * rCalc_PiBulkMean_bar;
rCalc_PiPermeate_bar := c_rOsmoticCoeff_Pitzer * rCalc_FeedAbsoluteTemp_K * (rPermeateTDS_ppm / 1000.0) * 0.90;

rCalc_AverageFeedPressure_bar := 0.5 * (rVotedFeedPressure_bar + rVotedBrinePressure_bar);
rMembraneDifferentialPress_bar := rVotedFeedPressure_bar - rVotedBrinePressure_bar;

(* 3.6 Net Driving Pressure (NDP) *)
rNetDrivingPressure_bar := (rCalc_AverageFeedPressure_bar - rPermeatePressure_bar) - (rCalc_PiSurface_bar - rCalc_PiPermeate_bar);
IF rNetDrivingPressure_bar < 0.5 THEN rNetDrivingPressure_bar := 0.5; END_IF;

(* 3.7 ASTM D4516 Performance Normalization *)
IF rNetDrivingPressure_bar > 1.0 AND rCalc_TCF > 0.1 THEN
    rNormPermeateFlow_m3h := rPermeateFlow_m3h * (rRef_NDP_bar / rNetDrivingPressure_bar) * (1.0 / rCalc_TCF);
ELSE
    rNormPermeateFlow_m3h := rPermeateFlow_m3h;
END_IF;

IF rFeedSalinity_TDS_ppm > 500.0 AND rPermeateFlow_m3h > 10.0 THEN
    rNormSaltPassage_pct := rCalc_SaltPassage_pct * (rRef_FeedSalinity_ppm / rFeedSalinity_TDS_ppm)
                          * rCalc_TCF * (rPermeateFlow_m3h / rRef_PermeateFlow_m3h);
ELSE
    rNormSaltPassage_pct := rCalc_SaltPassage_pct;
END_IF;

(* 3.8 Isobaric Pressure Exchanger (ERI PX) Energy Recovery Efficiency & Mixing Ratio *)
IF (rBrineFlow_m3h * rVotedBrinePressure_bar + rFeedFlow_ERD_m3h * 3.0) > 10.0 THEN
    rPX_Efficiency_pct := ((rFeedFlow_ERD_m3h * rPX_HP_OutPressure_bar + rBrineFlow_m3h * rPX_LP_OutPressure_bar) /
                          (rBrineFlow_m3h * rVotedBrinePressure_bar + rFeedFlow_ERD_m3h * 3.0)) * 100.0;
    IF rPX_Efficiency_pct > 99.0 THEN rPX_Efficiency_pct := 99.0; END_IF;
    IF rPX_Efficiency_pct < 50.0 THEN rPX_Efficiency_pct := 50.0; END_IF;
ELSE
    rPX_Efficiency_pct := 97.2;
END_IF;

IF (rVotedBrinePressure_bar > 10.0) AND (rFeedSalinity_TDS_ppm > 5000.0) THEN
    rPX_MixingRatio_pct := 4.2; (* Nominal volumetric mixing across ceramic rotor *)
ELSE
    rPX_MixingRatio_pct := 0.0;
END_IF;

(* 3.9 Specific Energy Consumption (SEC) Calculation [kWh/m3] *)
(* Hydraulic power: P [kW] = (Q [m3/h] * P [bar]) / (36.0 * eta_pump * eta_motor) *)
rCalc_HPP_ElectricalPower_kW := (rFeedFlow_HPP_m3h * rVotedFeedPressure_bar) / (36.0 * 0.865 * 0.965);
rCalc_BP_ElectricalPower_kW  := (rFeedFlow_ERD_m3h * (rVotedFeedPressure_bar - rPX_HP_OutPressure_bar)) / (36.0 * 0.850 * 0.960);
rCalc_TotalHydraulicPower_kW := rCalc_HPP_ElectricalPower_kW + rCalc_BP_ElectricalPower_kW;

IF rPermeateFlow_m3h > 15.0 THEN
    rSpecificEnergyConsump_kWh_m3 := (rCalc_TotalHydraulicPower_kW + 45.0) / rPermeateFlow_m3h; (* 45 kW aux power *)
ELSE
    rSpecificEnergyConsump_kWh_m3 := 2.75;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 8. SECTION 4: 16x16 DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC
    # -------------------------------------------------------------------------
    # Let's fully initialize matA (16x16 = 256 assignments), matB (16x8 = 128 assignments),
    # matC (8x16 = 128 assignments), matD (8x8 = 64 assignments).
    # Then write out unrolled prediction and gradient descent!
    matA_lines = []
    for i in range(1, 17):
        row_assigns = []
        for j in range(1, 17):
            val = 0.0
            if i == j:
                # Diagonal stable poles
                val = 0.920 + (i * 0.004)
                if val > 0.985:
                    val = 0.982
            elif i == 1 and j == 4:
                val = 0.0125
            elif i == 1 and j == 8:
                val = 0.0035
            elif i == 2 and j == 1:
                val = 0.0480
            elif i == 2 and j == 7:
                val = -0.0185
            elif i == 3 and j == 2:
                val = -0.0240
            elif i == 3 and j == 6:
                val = 0.0110
            elif i == 4 and j == 1:
                val = 0.8400
            elif i == 4 and j == 9:
                val = -0.0062
            elif i == 5 and j == 4:
                val = 0.9100
            elif i == 5 and j == 15:
                val = -0.0420
            elif i == 6 and j == 5:
                val = 0.0085
            elif i == 7 and j == 2:
                val = 0.0210
            elif i == 7 and j == 10:
                val = 0.0145
            elif i == 8 and j == 1:
                val = -0.0550
            elif i == 9 and j == 5:
                val = -0.0480
            elif i == 10 and j == 7:
                val = 0.00035
            elif i == 10 and j == 11:
                val = 0.00120
            elif i == 11 and j == 12:
                val = -0.00085
            elif i == 12 and j == 13:
                val = -0.0250
            elif i == 13 and j == 10:
                val = -0.0180
            elif i == 14 and j == 8:
                val = -0.0350
            elif i == 15 and j == 9:
                val = 0.0280
            elif i == 16 and j == 1:
                val = 0.0082
            elif i == 16 and j == 2:
                val = -0.0140
            row_assigns.append(f"matA[{i},{j}] := {val:.5f};")
        matA_lines.append("    " + " ".join(row_assigns))
    
    matB_lines = []
    for i in range(1, 17):
        row_assigns = []
        for k in range(1, 9):
            val = 0.0
            if i == 1 and k == 1:
                val = 0.6850  # HPP speed to feed pressure
            elif i == 2 and k == 1:
                val = 4.2500  # HPP speed to permeate flow
            elif i == 3 and k == 1:
                val = -0.8500 # HPP speed to permeate TDS
            elif i == 4 and k == 3:
                val = -0.4200 # ERD throttle to brine pressure
            elif i == 5 and k == 2:
                val = 0.5400  # BP speed to PX HP delivery
            elif i == 6 and k == 3:
                val = 0.1250  # ERD throttle to PX mixing
            elif i == 7 and k == 1:
                val = 0.0045  # HPP to CP factor
            elif i == 8 and k == 1:
                val = 3.8500  # HPP speed to HPP flow inertia
            elif i == 9 and k == 2:
                val = 3.2000  # BP speed to BP flow inertia
            elif i == 10 and k == 6:
                val = -0.0085 # Antiscalant dosing to fouling resistance
            elif i == 11 and k == 7:
                val = -0.0120 # Coagulant to cake layer
            elif i == 12 and k == 5:
                val = -0.8500 # SBS dosing to ORP
            elif i == 13 and k == 6:
                val = 0.4500  # Antiscalant dosing to coverage
            elif i == 14 and k == 1:
                val = -0.1500 # HPP speed to suction pressure drop
            elif i == 15 and k == 3:
                val = 0.0850  # ERD throttle to LP reject pressure
            elif i == 16 and k == 1:
                val = 0.0240  # HPP speed to SEC
            elif i == 16 and k == 2:
                val = 0.0180  # BP speed to SEC
            elif i == 2 and k == 4:
                val = -1.2500 # Permeate backpressure to flow
            elif i == 10 and k == 8:
                val = -0.1500 # CIP circulation to fouling resistance
            row_assigns.append(f"matB[{i},{k}] := {val:.4f};")
        matB_lines.append("    " + " ".join(row_assigns))

    matC_lines = []
    for i in range(1, 9):
        row_assigns = []
        for j in range(1, 17):
            val = 0.0
            if i == 1 and j == 1: val = 1.0 # Output 1: Feed Pressure
            elif i == 2 and j == 2: val = 1.0 # Output 2: Permeate Flow
            elif i == 3 and j == 3: val = 1.0 # Output 3: Permeate Salinity
            elif i == 4 and j == 4: val = 1.0 # Output 4: Brine Pressure
            elif i == 5 and j == 5: val = 1.0 # Output 5: PX HP Delivery
            elif i == 6 and j == 7: val = 1.0 # Output 6: CP Modulus
            elif i == 7 and j == 12: val = 1.0 # Output 7: ORP Redox
            elif i == 8 and j == 16: val = 1.0 # Output 8: SEC
            row_assigns.append(f"matC[{i},{j}] := {val:.2f};")
        matC_lines.append("    " + " ".join(row_assigns))

    matD_lines = []
    for i in range(1, 9):
        row_assigns = []
        for k in range(1, 9):
            val = 0.0
            row_assigns.append(f"matD[{i},{k}] := {val:.2f};")
        matD_lines.append("    " + " ".join(row_assigns))

    init_matrices_code = "\n".join(matA_lines) + "\n\n" + "\n".join(matB_lines) + "\n\n" + "\n".join(matC_lines) + "\n\n" + "\n".join(matD_lines)

    # Let's unroll state prediction for 16 states:
    state_pred_lines = []
    for i in range(1, 17):
        terms_A = [f"matA[{i},{j}]*vecState_x[{j}]" for j in range(1, 17)]
        terms_B = [f"matB[{i},{k}]*vecControl_u[{k}]" for k in range(1, 9)]
        all_terms = terms_A + terms_B
        # Split into readable sub-expressions
        sub1 = " + ".join(all_terms[:8])
        sub2 = " + ".join(all_terms[8:16])
        sub3 = " + ".join(all_terms[16:])
        line = f"        vecStateNext_x[{i}] := {sub1}\n                             + {sub2}\n                             + {sub3};"
        state_pred_lines.append(line)
    unrolled_state_pred = "\n".join(state_pred_lines)

    # Let's unroll gradient computation for 8 control inputs:
    gradient_lines = []
    for k in range(1, 9):
        b_terms = [f"matB[{i},{k}] * vecCostQ[{i}] * vecStateError_x[{i}]" for i in range(1, 17)]
        sub1 = " + ".join(b_terms[:8])
        sub2 = " + ".join(b_terms[8:16])
        line = f"""        vecGradient_g[{k}] := {sub1}
                            + {sub2}
                            + vecCostR[{k}] * vecControl_u[{k}]
                            + vecCostS[{k}] * (vecControl_u[{k}] - vecControlPrev_u[{k}]);"""
        gradient_lines.append(line)
    unrolled_gradient = "\n".join(gradient_lines)

    parts.append(f"""
(* ====================================================================================================================
   SECTION 4: 16x16 DISCRETE STATE-SPACE ENGINE & RECEDING-HORIZON MPC OPTIMIZER
   ==================================================================================================================== *)
IF NOT bMatricesInitialized THEN
    (* 4.1 State-Space Plant Matrix A [16x16] Initialization *)
{init_matrices_code}

    (* 4.2 Quadratic Optimization Weighting Vectors *)
    vecCostQ[1]  := 450.0;   (* Penalty: Feed pressure tracking error *)
    vecCostQ[2]  := 850.0;   (* Penalty: Permeate production rate deficit *)
    vecCostQ[3]  := 1200.0;  (* Penalty: Permeate salinity TDS exceeding limit *)
    vecCostQ[4]  := 280.0;   (* Penalty: Brine reject pressure fluctuation *)
    vecCostQ[5]  := 320.0;   (* Penalty: PX high-pressure delivery error *)
    vecCostQ[6]  := 150.0;   (* Penalty: PX mixing ratio deviation *)
    vecCostQ[7]  := 500.0;   (* Penalty: Concentration polarization buildup *)
    vecCostQ[8]  := 45.0;    (* Penalty: HPP flow inertia dynamics *)
    vecCostQ[9]  := 35.0;    (* Penalty: BP flow inertia dynamics *)
    vecCostQ[10] := 650.0;   (* Penalty: Membrane hydraulic fouling resistance *)
    vecCostQ[11] := 180.0;   (* Penalty: Cartridge filter cake thickness *)
    vecCostQ[12] := 1500.0;  (* Penalty: Active chlorine ORP spike (Safety Critical) *)
    vecCostQ[13] := 220.0;   (* Penalty: Antiscalant surface coverage deficit *)
    vecCostQ[14] := 120.0;   (* Penalty: HPP suction pressure depression *)
    vecCostQ[15] := 95.0;    (* Penalty: PX reject discharge backpressure *)
    vecCostQ[16] := 950.0;   (* Penalty: Specific Energy Consumption (SEC) *)

    (* Control Effort Penalties R [1..8] *)
    vecCostR[1]  := 18.0;    (* HPP VFD speed effort *)
    vecCostR[2]  := 12.0;    (* BP VFD speed effort *)
    vecCostR[3]  := 8.5;     (* ERD concentrate throttle effort *)
    vecCostR[4]  := 5.0;     (* Permeate backpressure valve effort *)
    vecCostR[5]  := 2.5;     (* SBS dechlorination dosing pump effort *)
    vecCostR[6]  := 3.0;     (* Antiscalant chemical dosing pump effort *)
    vecCostR[7]  := 2.0;     (* Ferric coagulant dosing pump effort *)
    vecCostR[8]  := 15.0;    (* CIP circulation pump effort *)

    (* Rate-of-Change Slew Penalties S [1..8] *)
    vecCostS[1]  := 45.0;
    vecCostS[2]  := 30.0;
    vecCostS[3]  := 20.0;
    vecCostS[4]  := 10.0;
    vecCostS[5]  := 5.0;
    vecCostS[6]  := 6.0;
    vecCostS[7]  := 4.0;
    vecCostS[8]  := 25.0;

    (* Actuator Hard Saturation Constraints u_min and u_max [%] *)
    vecControlMin_u[1] := 0.0;    vecControlMax_u[1] := 100.0; (* HPP VFD *)
    vecControlMin_u[2] := 0.0;    vecControlMax_u[2] := 100.0; (* BP VFD *)
    vecControlMin_u[3] := 15.0;   vecControlMax_u[3] := 95.0;  (* ERD throttle *)
    vecControlMin_u[4] := 5.0;    vecControlMax_u[4] := 90.0;  (* Permeate valve *)
    vecControlMin_u[5] := 0.0;    vecControlMax_u[5] := 100.0; (* SBS pump *)
    vecControlMin_u[6] := 10.0;   vecControlMax_u[6] := 100.0; (* Antiscalant pump *)
    vecControlMin_u[7] := 5.0;    vecControlMax_u[7] := 100.0; (* Coagulant pump *)
    vecControlMin_u[8] := 0.0;    vecControlMax_u[8] := 100.0; (* CIP pump *)

    (* Actuator Slew Rate Limiters du_max [% per scan cycle] *)
    vecDeltaMax_du[1] := 0.50;    (* HPP VFD max 0.5% per 10 ms = 50%/s ramp *)
    vecDeltaMax_du[2] := 0.60;
    vecDeltaMax_du[3] := 1.20;
    vecDeltaMax_du[4] := 1.50;
    vecDeltaMax_du[5] := 2.00;
    vecDeltaMax_du[6] := 1.00;
    vecDeltaMax_du[7] := 1.00;
    vecDeltaMax_du[8] := 1.50;

    bMatricesInitialized := TRUE;
END_IF;

(* 4.3 Populate Real-Time State Vector x[1..16] *)
vecState_x[1]  := rVotedFeedPressure_bar - 66.5;
vecState_x[2]  := rPermeateFlow_m3h - rTargetPermeateFlow_m3h;
vecState_x[3]  := rPermeateTDS_ppm - 180.0;
vecState_x[4]  := rVotedBrinePressure_bar - 64.0;
vecState_x[5]  := rPX_HP_OutPressure_bar - 63.5;
vecState_x[6]  := rPX_MixingRatio_pct - 4.2;
vecState_x[7]  := (rCalc_ConcPolarizationModulus - 1.15) * 100.0;
vecState_x[8]  := rFeedFlow_HPP_m3h - 520.0;
vecState_x[9]  := rFeedFlow_ERD_m3h - 425.0;
vecState_x[10] := (rMembraneDifferentialPress_bar - 1.85) * 10.0;
vecState_x[11] := (rSiltDensityIndex_SDI15 - 2.5) * 5.0;
vecState_x[12] := rVotedFeedORP_mV - 165.0;
vecState_x[13] := 85.0 - 100.0 * (rDosingAntiscalantCmd_pct / 100.0);
vecState_x[14] := 3.2 - c_rMinSuctionPressure_bar;
vecState_x[15] := rPX_LP_OutPressure_bar - 1.2;
vecState_x[16] := rSpecificEnergyConsump_kWh_m3 - rMaxAllowableSEC_kWh_m3;

(* 4.4 Multi-Variable Projected Gradient Descent Optimization Loop *)
IF (iState = 60 OR iState = 70 OR iState = 80) AND bEnableMaster THEN
    FOR iMPC_Iter := 1 TO iMPC_MaxIterations DO
        (* Unrolled state propagation x[k+1] = A*x[k] + B*u[k] *)
{unrolled_state_pred}

        (* Evaluate state error vector e_x[i] = x_next[i] - x_target[i] *)
        FOR iLoopIdx := 1 TO 16 DO
            vecStateError_x[iLoopIdx] := vecStateNext_x[iLoopIdx] - vecStateTarget_x[iLoopIdx];
        END_FOR;

        (* Compute gradient vector g[k] = B^T * Q * e_x + R * u + S * du *)
{unrolled_gradient}

        (* Projected gradient descent update with box constraints and slew limits *)
        FOR kLoopIdx := 1 TO 8 DO
            vecControl_u[kLoopIdx] := vecControl_u[kLoopIdx] - rMPC_StepSizeAlpha * vecGradient_g[kLoopIdx];
            vecControlDelta_du[kLoopIdx] := vecControl_u[kLoopIdx] - vecControlPrev_u[kLoopIdx];

            IF vecControlDelta_du[kLoopIdx] > vecDeltaMax_du[kLoopIdx] THEN
                vecControl_u[kLoopIdx] := vecControlPrev_u[kLoopIdx] + vecDeltaMax_du[kLoopIdx];
            ELSIF vecControlDelta_du[kLoopIdx] < -vecDeltaMax_du[kLoopIdx] THEN
                vecControl_u[kLoopIdx] := vecControlPrev_u[kLoopIdx] - vecDeltaMax_du[kLoopIdx];
            END_IF;

            IF vecControl_u[kLoopIdx] < vecControlMin_u[kLoopIdx] THEN
                vecControl_u[kLoopIdx] := vecControlMin_u[kLoopIdx];
            ELSIF vecControl_u[kLoopIdx] > vecControlMax_u[kLoopIdx] THEN
                vecControl_u[kLoopIdx] := vecControlMax_u[kLoopIdx];
            END_IF;
        END_FOR;
    END_FOR;

    FOR kLoopIdx := 1 TO 8 DO
        vecControlPrev_u[kLoopIdx] := vecControl_u[kLoopIdx];
    END_FOR;

    (* Assign optimized control outputs to physical actuator references *)
    rHPP_SpeedCmd_pct          := vecControl_u[1];
    rBP_SpeedCmd_pct           := vecControl_u[2];
    rERD_RejectThrottleCmd_pct := vecControl_u[3];
    rPermeateBackpressCmd_pct  := vecControl_u[4];
    rDosingSBS_StrokeCmd_pct   := vecControl_u[5];
    rDosingAntiscalantCmd_pct  := vecControl_u[6];
    rDosingCoagulantCmd_pct    := vecControl_u[7];
END_IF;
""")

    # -------------------------------------------------------------------------
    # 9. SECTION 5: 12-STAGE COMPREHENSIVE OPERATIONAL FINITE STATE MACHINE
    # -------------------------------------------------------------------------
    parts.append("""
(* ====================================================================================================================
   SECTION 5: 12-STAGE OPERATIONAL FINITE STATE MACHINE (CASE iState OF ... END_CASE;)
   ==================================================================================================================== *)
CASE iState OF
    0: (* ---------------- STATE 0: STANDBY & SYSTEM DEPRESSURIZED ISOLATION ---------------- *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := FALSE;
        bHighPressureSafetyDumpOpen := FALSE;
        bTrainTripAlarm             := FALSE;
        bWarningActive              := FALSE;
        bCIP_Active                 := FALSE;

        rHPP_SpeedCmd_pct           := 0.0;
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 0.0;
        rPermeateBackpressCmd_pct   := 0.0;
        rDosingSBS_StrokeCmd_pct    := 0.0;
        rDosingAntiscalantCmd_pct   := 0.0;
        rDosingCoagulantCmd_pct     := 0.0;
        rCIP_PumpSpeedCmd_pct       := 0.0;
        rRampRpmAccumulator         := 0.0;

        tStateTimer(IN := FALSE);
        tDeaerationTimer(IN := FALSE);
        tSoftRampTimer(IN := FALSE);

        IF bEnableMaster AND bEmergencyStop AND NOT bFeedORP_VoterFailed AND NOT bFeedP_VoterFailed THEN
            IF bCIP_InitiateRequest THEN
                iState := 90; (* Jump directly to CIP cleaning sequence *)
            ELSIF bPreservationModeReq THEN
                iState := 115; (* Jump to biocide chemical preservation *)
            ELSE
                iState := 10; (* Advance to low-pressure raw seawater flush *)
            END_IF;
        END_IF;

    10: (* ----------- STATE 10: LOW-PRESSURE RAW SEAWATER PRE-TREATMENT FLUSH ----------- *)
        (* Flush train vessels at 2.5 - 3.5 bar with pre-treated seawater to displace preservation chemicals *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;   (* Route flush discharge to ocean outfall *)
        bHighPressureSafetyDumpOpen := FALSE;
        bCIP_Active                 := FALSE;

        rHPP_SpeedCmd_pct           := 0.0;    (* HPP remains stopped *)
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 100.0;  (* Concentrate line fully open to purge fluid *)
        rPermeateBackpressCmd_pct   := 0.0;
        rDosingSBS_StrokeCmd_pct    := 15.0;   (* Low background dosing of SBS to eliminate chlorine traces *)
        rDosingAntiscalantCmd_pct   := 0.0;
        rDosingCoagulantCmd_pct     := 20.0;

        tStateTimer(IN := TRUE, PT := T#180S); (* 180 seconds displacement duration *)
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            IF rFeed_Turbidity_NTU <= 0.35 THEN
                iState := 20; (* Turbidity verified clean: advance to chemical dosing stabilization *)
            ELSE
                bWarningActive := TRUE; (* Pre-treatment filter turbidity elevated *)
            END_IF;
        END_IF;

    20: (* ----------- STATE 20: ANTISCALANT & SBS CHEMICAL DOSING STABILIZATION ----------- *)
        (* Bring all chemical dosing pumps to steady stoichiometric rates prior to membrane pressurization *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;

        rDosingSBS_StrokeCmd_pct    := 45.0;   (* Target stoichiometric dechlorination stroke *)
        rDosingAntiscalantCmd_pct   := 40.0;   (* Threshold scale inhibitor active *)
        rDosingCoagulantCmd_pct     := 35.0;

        tStateTimer(IN := TRUE, PT := T#60S);  (* 60 seconds stabilization delay *)
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            (* Verify ORP is thoroughly neutralized below safety threshold (< 200 mV) *)
            IF rVotedFeedORP_mV < 200.0 THEN
                iState := 30; (* Chlorine eliminated: proceed to de-aeration bleed *)
            ELSE
                bWarningActive := TRUE;
                dwAlarmWord_Secondary.4 := TRUE; (* Dechlorination stabilization incomplete *)
            END_IF;
        END_IF;

    30: (* ----------- STATE 30: HIGH-PRESSURE RO TRAIN AIR DE-AERATION & BLEED ----------- *)
        (* Slow hydraulic sweep at low velocity (0.2 m/s) to vent air pockets from high-point bleeds *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;

        rHPP_SpeedCmd_pct           := 12.0;   (* Low idling crawl speed to gently pressurize headers to 4.5 bar *)
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 100.0;

        tDeaerationTimer(IN := TRUE, PT := T#45S); (* 45 seconds de-aeration bleed *)
        IF tDeaerationTimer.Q THEN
            tDeaerationTimer(IN := FALSE);
            iState := 40; (* Air evacuated: begin high-pressure soft ramp *)
        END_IF;

    40: (* ----------- STATE 40: HIGH-PRESSURE PUMP (HPP) CONTROLLED SOFT RAMP-UP ----------- *)
        (* Linear acceleration of 3.5 MW MV VFD at 0.40 bar/second to prevent water hammer shock *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;   (* Low quality permeate routed to reject dump *)
        bHighPressureSafetyDumpOpen := FALSE;

        tSoftRampTimer(IN := TRUE, PT := T#100MS);
        IF tSoftRampTimer.Q THEN
            tSoftRampTimer(IN := FALSE);
            IF rHPP_SpeedCmd_pct < 75.0 THEN
                rHPP_SpeedCmd_pct := rHPP_SpeedCmd_pct + 0.15;
            END_IF;
        END_IF;

        rERD_RejectThrottleCmd_pct := 65.0;
        rBP_SpeedCmd_pct           := 15.0;

        (* Once feed pressure surpasses osmotic threshold (52.0 bar), couple energy recovery device *)
        IF rVotedFeedPressure_bar >= 52.0 THEN
            tSoftRampTimer(IN := FALSE);
            iState := 50; (* Transition to synchronous PX energy recovery coupling *)
        END_IF;

    50: (* ----------- STATE 50: PX ENERGY RECOVERY SYNCHRONOUS COUPLING ----------- *)
        (* Bring isobaric pressure exchanger arrays online; ramp Booster Pump to match HPP discharge *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;

        IF rBP_SpeedCmd_pct < 68.0 THEN
            rBP_SpeedCmd_pct := rBP_SpeedCmd_pct + 0.25;
        END_IF;

        IF rHPP_SpeedCmd_pct < 82.0 THEN
            rHPP_SpeedCmd_pct := rHPP_SpeedCmd_pct + 0.10;
        END_IF;

        rERD_RejectThrottleCmd_pct := 55.0;

        tStateTimer(IN := TRUE, PT := T#30S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            (* Verify PX ceramic rotor rotation speed > 700 RPM confirming hydrodynamic levitation *)
            IF rPX_RotorSpeed_RPM >= 700.0 AND rPX_Efficiency_pct >= 92.0 THEN
                iState := 60; (* Rotor spinning smoothly: hand over to full multivariable MPC *)
            ELSE
                bWarningActive := TRUE;
                dwAlarmWord_Secondary.5 := TRUE; (* PX synchronization anomaly *)
            END_IF;
        END_IF;

    60: (* ----------- STATE 60: STEADY-STATE DESALINATION MULTIVARIABLE MPC ----------- *)
        (* Closed-loop multivariable regulation: SEC optimization, recovery regulation, permeate flow *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;

        (* Check if product water quality meets potable distribution specifications *)
        IF rVotedPermeateCond_uS <= c_rAlarm_PermCond_H_uS AND rPermeateFlow_m3h >= (0.85 * rTargetPermeateFlow_m3h) THEN
            tStateTimer(IN := TRUE, PT := T#20S);
            IF tStateTimer.Q THEN
                tStateTimer(IN := FALSE);
                iState := 70; (* Water on-spec: open potable distribution valve *)
            END_IF;
        ELSE
            tStateTimer(IN := FALSE);
        END_IF;

    70: (* ----------- STATE 70: PERMEATE CONDUCTIVITY COMPLIANCE & WATER DELIVERY ----------- *)
        (* Full commercial production delivery mode to municipal clearwell storage *)
        bTrainRunning               := TRUE;
        bPermeateValveOpen          := TRUE;   (* Send product water to municipal potable header *)
        bPermeateDivertOpen         := FALSE;  (* Close outfall dump diversion valve *)
        bHighPressureSafetyDumpOpen := FALSE;

        (* Transition to active fouling diagnostics state after 100 seconds steady delivery *)
        tStateTimer(IN := TRUE, PT := T#100S);
        IF tStateTimer.Q THEN
            tStateTimer(IN := FALSE);
            iState := 80; (* Enter continuous fouling compaction tracking *)
        END_IF;

    80: (* ----------- STATE 80: MEMBRANE FOULING & COMPACTION DIAGNOSTIC MONITORING ----------- *)
        (* Continuous evaluation of ASTM D4516 normalized flow decline and differential pressure dP *)
        bTrainRunning               := TRUE;
        bPermeateValveOpen          := TRUE;
        bPermeateDivertOpen         := FALSE;
        bHighPressureSafetyDumpOpen := FALSE;

        (* Diagnostic CIP Trigger Criteria:
           1. Normalized permeate flow decline > 15.0%
           2. Feed-to-brine differential pressure dP > 3.5 bar
           3. Normalized salt passage increase > 20.0%
           4. Supervisory manual CIP request *)
        IF (rNormPermeateFlow_m3h < (0.85 * rRef_PermeateFlow_m3h)) OR
           (rMembraneDifferentialPress_bar >= c_rAlarm_MembraneDP_H_bar) OR
           (rNormSaltPassage_pct >= (1.20 * rRef_SaltPassage_pct)) OR
           bCIP_InitiateRequest THEN
            bWarningActive := TRUE;
            dwAlarmWord_Secondary.6 := TRUE; (* CIP cleaning recommended / required *)
            IF bCIP_InitiateRequest THEN
                bTrainRunning      := FALSE;
                bPermeateValveOpen := FALSE;
                bPermeateDivertOpen := TRUE;
                iState             := 90; (* Advance to automated chemical CIP sequence *)
            END_IF;
        END_IF;

    90: (* ----------- STATE 90: AUTOMATED DUAL-STAGE CHEMICAL CIP (STAGE 1: ACID CLEAN) ----------- *)
        (* Citric acid (2.0% wt, pH 2.2 - 2.8, 35 deg C) circulation to dissolve carbonate & metal oxide scale *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;
        bCIP_Active                 := TRUE;

        rHPP_SpeedCmd_pct           := 0.0;    (* HPP and BP strictly locked out during CIP *)
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 0.0;    (* ERD isolated from chemical skid *)
        rDosingSBS_StrokeCmd_pct    := 0.0;
        rDosingAntiscalantCmd_pct   := 0.0;
        rDosingCoagulantCmd_pct     := 0.0;

        CASE iCIP_SubPhase OF
            0: (* Low-flow chemical displacement and air venting *)
                rCIP_PumpSpeedCmd_pct := 35.0;
                tCIP_AcidRecircTimer(IN := TRUE, PT := T#300S);
                IF tCIP_AcidRecircTimer.Q THEN
                    tCIP_AcidRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 1;
                END_IF;

            1: (* High-flow acid circulation: 40 m3/h per vessel *)
                rCIP_PumpSpeedCmd_pct := 85.0;
                tCIP_AcidRecircTimer(IN := TRUE, PT := T#2700S); (* 45 minutes circulation *)
                IF tCIP_AcidRecircTimer.Q THEN
                    tCIP_AcidRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 2;
                END_IF;

            2: (* Chemical static soak cycle *)
                rCIP_PumpSpeedCmd_pct := 0.0; (* Pump stopped to allow scale dissolution soak *)
                tCIP_AcidSoakTimer(IN := TRUE, PT := T#2700S);   (* 45 minutes soaking *)
                IF tCIP_AcidSoakTimer.Q THEN
                    tCIP_AcidSoakTimer(IN := FALSE);
                    iCIP_SubPhase := 3;
                END_IF;

            3: (* High-flow acid final sweep *)
                rCIP_PumpSpeedCmd_pct := 85.0;
                tCIP_AcidRecircTimer(IN := TRUE, PT := T#1800S); (* 30 minutes final sweep *)
                IF tCIP_AcidRecircTimer.Q THEN
                    tCIP_AcidRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 0;
                    iState := 100; (* Advance to Stage 2: Alkaline cleaning *)
                END_IF;
        END_CASE;

    100: (* ---------- STATE 100: AUTOMATED DUAL-STAGE CHEMICAL CIP (STAGE 2: ALKALINE CLEAN) ---------- *)
        (* Alkaline formulation (NaOH + EDTA + SDS, pH 10.8 - 11.5, 38 deg C) for organic & biofilm removal *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;
        bCIP_Active                 := TRUE;

        rHPP_SpeedCmd_pct           := 0.0;
        rBP_SpeedCmd_pct            := 0.0;

        CASE iCIP_SubPhase OF
            0: (* Alkaline chemical pre-flush displacement *)
                rCIP_PumpSpeedCmd_pct := 40.0;
                tCIP_AlkalineRecircTimer(IN := TRUE, PT := T#300S);
                IF tCIP_AlkalineRecircTimer.Q THEN
                    tCIP_AlkalineRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 1;
                END_IF;

            1: (* High-velocity alkaline recirculation *)
                rCIP_PumpSpeedCmd_pct := 90.0;
                tCIP_AlkalineRecircTimer(IN := TRUE, PT := T#3600S); (* 60 minutes recirculation *)
                IF tCIP_AlkalineRecircTimer.Q THEN
                    tCIP_AlkalineRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 2;
                END_IF;

            2: (* Alkaline bio-film soak cycle *)
                rCIP_PumpSpeedCmd_pct := 0.0;
                tCIP_AlkalineSoakTimer(IN := TRUE, PT := T#3600S);   (* 60 minutes soaking *)
                IF tCIP_AlkalineSoakTimer.Q THEN
                    tCIP_AlkalineSoakTimer(IN := FALSE);
                    iCIP_SubPhase := 3;
                END_IF;

            3: (* Final high-velocity surfactant sweep *)
                rCIP_PumpSpeedCmd_pct := 90.0;
                tCIP_AlkalineRecircTimer(IN := TRUE, PT := T#1800S); (* 30 minutes final sweep *)
                IF tCIP_AlkalineRecircTimer.Q THEN
                    tCIP_AlkalineRecircTimer(IN := FALSE);
                    iCIP_SubPhase := 0;
                    iState := 110; (* Advance to permeate displacement rinse *)
                END_IF;
        END_CASE;

    110: (* ---------- STATE 110: PERMEATE LOW-PRESSURE DISPLACEMENT RINSE ---------- *)
        (* Flush chemical residue using clean permeate water from storage tank at 2.0 bar *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := FALSE;
        bCIP_Active                 := FALSE;

        rCIP_PumpSpeedCmd_pct       := 0.0;
        rERD_RejectThrottleCmd_pct  := 100.0;  (* Dump rinse effluent to neutralization neutralization pit *)

        tDisplacementFlushTimer(IN := TRUE, PT := T#600S); (* 10 minutes displacement flush *)
        IF tDisplacementFlushTimer.Q THEN
            tDisplacementFlushTimer(IN := FALSE);
            (* Verify chemical effluent has returned to neutral pH (6.8 to 7.8) *)
            IF (rCIP_Tank_pH >= 6.8 AND rCIP_Tank_pH <= 7.8) OR (rCIP_Tank_pH < 1.0) THEN
                IF bPreservationModeReq THEN
                    iState := 115; (* Advance to biocide preservation *)
                ELSE
                    iState := 0;   (* Clean complete: return to Standby Ready *)
                END_IF;
            ELSE
                bWarningActive := TRUE; (* Chemical rinse incomplete *)
            END_IF;
        END_IF;

    115: (* ---------- STATE 115: RO TRAIN CHEMICAL PRESERVATION STANDBY ---------- *)
        (* Long-term preservation using 1.0% sodium bisulfite solution to prevent biological growth *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := FALSE;
        bHighPressureSafetyDumpOpen := FALSE;
        bCIP_Active                 := FALSE;

        rHPP_SpeedCmd_pct           := 0.0;
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 0.0;
        rDosingSBS_StrokeCmd_pct    := 0.0;

        IF NOT bPreservationModeReq THEN
            iState := 0; (* Operator cleared preservation mode: return to standby *)
        END_IF;

    120: (* ---------- STATE 120: EMERGENCY HIGH-PRESSURE HYDRAULIC OVERPRESSURE DUMP ---------- *)
        (* Fast emergency depressurization dump state after trip or catastrophic fault *)
        bTrainRunning               := FALSE;
        bPermeateValveOpen          := FALSE;
        bPermeateDivertOpen         := TRUE;
        bHighPressureSafetyDumpOpen := TRUE;   (* Keep emergency hydraulic dump open *)
        bTrainTripAlarm             := TRUE;
        bCIP_Active                 := FALSE;

        rHPP_SpeedCmd_pct           := 0.0;
        rBP_SpeedCmd_pct            := 0.0;
        rERD_RejectThrottleCmd_pct  := 100.0;
        rPermeateBackpressCmd_pct   := 0.0;
        rDosingSBS_StrokeCmd_pct    := 0.0;
        rDosingAntiscalantCmd_pct   := 0.0;
        rDosingCoagulantCmd_pct     := 0.0;
        rCIP_PumpSpeedCmd_pct       := 0.0;

        (* Require manual operator alarm acknowledgement and enable clearance to reset *)
        IF bAcknowledgeAlarms AND NOT bEnableMaster THEN
            bTrainTripAlarm := FALSE;
            dwAlarmWord_Primary := 16#0000_0000;
            dwAlarmWord_Secondary := 16#0000_0000;
            bHighPressureSafetyDumpOpen := FALSE;
            iState := 0; (* Reset to Standby *)
        END_IF;
END_CASE;

iActiveState := iState;
""")

    # -------------------------------------------------------------------------
    # 10. SECTION 6: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY PACKING
    # -------------------------------------------------------------------------
    parts.append("""
(* ====================================================================================================================
   SECTION 6: ISA-18.2 MULTI-TIERED ALARM EVALUATION, FILTER TIMERS & BIT PACKING
   ==================================================================================================================== *)

(* -------------------------------------------------------------------------------------------------
   6.1 HIGH-PRESSURE MEMBRANE FEED PRESSURE ALARMS (HH, H, L, LL) [bar]
   ------------------------------------------------------------------------------------------------- *)
IF rVotedFeedPressure_bar >= c_rAlarm_FeedP_HH_bar THEN
    iAlarmFilter_FeedP_HH := iAlarmFilter_FeedP_HH + 1;
    IF iAlarmFilter_FeedP_HH >= 5 THEN (* Qualified after 50 ms *)
        dwAlarmWord_Primary.0 := TRUE; (* Bit 0: FEED_PRESSURE_HIGH_HIGH_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120; (* Trip to emergency dump *)
    END_IF;
ELSIF rVotedFeedPressure_bar <= (c_rAlarm_FeedP_HH_bar - c_rDeadband_FeedP_bar) THEN
    iAlarmFilter_FeedP_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.0 := FALSE; END_IF;
END_IF;

IF rVotedFeedPressure_bar >= c_rAlarm_FeedP_H_bar THEN
    dwAlarmWord_Primary.1 := TRUE; (* Bit 1: FEED_PRESSURE_HIGH_WARNING *)
    bWarningActive := TRUE;
ELSIF rVotedFeedPressure_bar <= (c_rAlarm_FeedP_H_bar - c_rDeadband_FeedP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.1 := FALSE; END_IF;
END_IF;

IF (rVotedFeedPressure_bar <= c_rAlarm_FeedP_L_bar) AND (iState >= 60 AND iState <= 80) THEN
    dwAlarmWord_Primary.2 := TRUE; (* Bit 2: FEED_PRESSURE_LOW_WARNING *)
    bWarningActive := TRUE;
ELSIF rVotedFeedPressure_bar >= (c_rAlarm_FeedP_L_bar + c_rDeadband_FeedP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.2 := FALSE; END_IF;
END_IF;

IF (rVotedFeedPressure_bar <= c_rAlarm_FeedP_LL_bar) AND (iState >= 50 AND iState <= 80) THEN
    iAlarmFilter_FeedP_LL := iAlarmFilter_FeedP_LL + 1;
    IF iAlarmFilter_FeedP_LL >= 20 THEN (* Qualified after 200 ms *)
        dwAlarmWord_Primary.3 := TRUE; (* Bit 3: FEED_PRESSURE_LOW_LOW_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120;
    END_IF;
ELSIF rVotedFeedPressure_bar >= (c_rAlarm_FeedP_LL_bar + c_rDeadband_FeedP_bar) THEN
    iAlarmFilter_FeedP_LL := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.3 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.2 HIGH-PRESSURE CONCENTRATE BRINE REJECT ALARMS (HH, H, L, LL) [bar]
   ------------------------------------------------------------------------------------------------- *)
IF rVotedBrinePressure_bar >= c_rAlarm_BrineP_HH_bar THEN
    iAlarmFilter_BrineP_HH := iAlarmFilter_BrineP_HH + 1;
    IF iAlarmFilter_BrineP_HH >= 5 THEN
        dwAlarmWord_Primary.4 := TRUE; (* Bit 4: BRINE_PRESSURE_HIGH_HIGH_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120;
    END_IF;
ELSIF rVotedBrinePressure_bar <= (c_rAlarm_BrineP_HH_bar - c_rDeadband_BrineP_bar) THEN
    iAlarmFilter_BrineP_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.4 := FALSE; END_IF;
END_IF;

IF rVotedBrinePressure_bar >= c_rAlarm_BrineP_H_bar THEN
    dwAlarmWord_Primary.5 := TRUE; (* Bit 5: BRINE_PRESSURE_HIGH_WARNING *)
    bWarningActive := TRUE;
ELSIF rVotedBrinePressure_bar <= (c_rAlarm_BrineP_H_bar - c_rDeadband_BrineP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.5 := FALSE; END_IF;
END_IF;

IF (rVotedBrinePressure_bar <= c_rAlarm_BrineP_L_bar) AND (iState >= 60 AND iState <= 80) THEN
    dwAlarmWord_Primary.6 := TRUE; (* Bit 6: BRINE_PRESSURE_LOW_WARNING *)
    bWarningActive := TRUE;
ELSIF rVotedBrinePressure_bar >= (c_rAlarm_BrineP_L_bar + c_rDeadband_BrineP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.6 := FALSE; END_IF;
END_IF;

IF (rVotedBrinePressure_bar <= c_rAlarm_BrineP_LL_bar) AND (iState >= 50 AND iState <= 80) THEN
    dwAlarmWord_Primary.7 := TRUE; (* Bit 7: BRINE_PRESSURE_LOW_LOW_TRIP *)
    bTrainTripAlarm := TRUE;
    iState := 120;
ELSIF rVotedBrinePressure_bar >= (c_rAlarm_BrineP_LL_bar + c_rDeadband_BrineP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.7 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.3 MEMBRANE VESSEL DIFFERENTIAL PRESSURE (dP) FOULING ALARMS [bar]
   ------------------------------------------------------------------------------------------------- *)
IF rMembraneDifferentialPress_bar >= c_rAlarm_MembraneDP_HH_bar THEN
    iAlarmFilter_MembraneDP_HH := iAlarmFilter_MembraneDP_HH + 1;
    IF iAlarmFilter_MembraneDP_HH >= 10 THEN
        dwAlarmWord_Primary.8 := TRUE; (* Bit 8: MEMBRANE_VESSEL_DP_HIGH_HIGH_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120;
    END_IF;
ELSIF rMembraneDifferentialPress_bar <= (c_rAlarm_MembraneDP_HH_bar - c_rDeadband_MembraneDP_bar) THEN
    iAlarmFilter_MembraneDP_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.8 := FALSE; END_IF;
END_IF;

IF rMembraneDifferentialPress_bar >= c_rAlarm_MembraneDP_H_bar THEN
    dwAlarmWord_Primary.9 := TRUE; (* Bit 9: MEMBRANE_VESSEL_DP_HIGH_WARNING *)
    bWarningActive := TRUE;
ELSIF rMembraneDifferentialPress_bar <= (c_rAlarm_MembraneDP_H_bar - c_rDeadband_MembraneDP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.9 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.4 PERMEATE ELECTRICAL CONDUCTIVITY / TDS COMPLIANCE ALARMS [uS/cm]
   ------------------------------------------------------------------------------------------------- *)
IF rVotedPermeateCond_uS >= c_rAlarm_PermCond_HH_uS THEN
    iAlarmFilter_PermCond_HH := iAlarmFilter_PermCond_HH + 1;
    IF iAlarmFilter_PermCond_HH >= 30 THEN (* Qualified after 300 ms *)
        dwAlarmWord_Primary.10 := TRUE; (* Bit 10: PERMEATE_CONDUCTIVITY_HIGH_HIGH_TRIP *)
        bPermeateValveOpen := FALSE;
        bPermeateDivertOpen := TRUE; (* Divert off-spec permeate to ocean reject *)
    END_IF;
ELSIF rVotedPermeateCond_uS <= (c_rAlarm_PermCond_HH_uS - c_rDeadband_PermCond_uS) THEN
    iAlarmFilter_PermCond_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.10 := FALSE; END_IF;
END_IF;

IF rVotedPermeateCond_uS >= c_rAlarm_PermCond_H_uS THEN
    dwAlarmWord_Primary.11 := TRUE; (* Bit 11: PERMEATE_CONDUCTIVITY_HIGH_WARNING *)
    bWarningActive := TRUE;
ELSIF rVotedPermeateCond_uS <= (c_rAlarm_PermCond_H_uS - c_rDeadband_PermCond_uS) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.11 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.5 SEAWATER FEED ORP (FREE CHLORINE BREAKTHROUGH) SAFETY CRITICAL TRIPS [mV]
   ------------------------------------------------------------------------------------------------- *)
IF rVotedFeedORP_mV >= c_rAlarm_FeedORP_HH_mV THEN
    iAlarmFilter_FeedORP_HH := iAlarmFilter_FeedORP_HH + 1;
    IF iAlarmFilter_FeedORP_HH >= 3 THEN (* Fast trip in 30 ms to prevent polyamide oxidation *)
        dwAlarmWord_Primary.12 := TRUE; (* Bit 12: CHLORINE_BREAKTHROUGH_ORP_HIGH_HIGH_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120; (* Instant emergency trip *)
    END_IF;
ELSIF rVotedFeedORP_mV <= (c_rAlarm_FeedORP_HH_mV - c_rDeadband_FeedORP_mV) THEN
    iAlarmFilter_FeedORP_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.12 := FALSE; END_IF;
END_IF;

IF rVotedFeedORP_mV >= c_rAlarm_FeedORP_H_mV THEN
    dwAlarmWord_Primary.13 := TRUE; (* Bit 13: ORP_DECHLORINATION_WARNING *)
    bWarningActive := TRUE;
    (* Automatically boost sodium bisulfite stroke to aggressively neutralize chlorine *)
    rDosingSBS_StrokeCmd_pct := 85.0;
ELSIF rVotedFeedORP_mV <= (c_rAlarm_FeedORP_H_mV - c_rDeadband_FeedORP_mV) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.13 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.6 ISOBARIC ENERGY RECOVERY DEVICE (PX) DIFFERENTIAL PRESSURE ALARMS [bar]
   ------------------------------------------------------------------------------------------------- *)
IF (rVotedBrinePressure_bar - rPX_HP_OutPressure_bar) >= c_rAlarm_PX_DP_HH_bar THEN
    iAlarmFilter_PX_DP_HH := iAlarmFilter_PX_DP_HH + 1;
    IF iAlarmFilter_PX_DP_HH >= 10 THEN
        dwAlarmWord_Primary.14 := TRUE; (* Bit 14: PX_DIFFERENTIAL_PRESSURE_HIGH_HIGH_TRIP *)
        bTrainTripAlarm := TRUE;
        iState := 120;
    END_IF;
ELSIF (rVotedBrinePressure_bar - rPX_HP_OutPressure_bar) <= (c_rAlarm_PX_DP_HH_bar - c_rDeadband_PX_DP_bar) THEN
    iAlarmFilter_PX_DP_HH := 0;
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.14 := FALSE; END_IF;
END_IF;

IF (rVotedBrinePressure_bar - rPX_HP_OutPressure_bar) >= c_rAlarm_PX_DP_H_bar THEN
    dwAlarmWord_Primary.15 := TRUE; (* Bit 15: PX_DIFFERENTIAL_PRESSURE_HIGH_WARNING *)
    bWarningActive := TRUE;
ELSIF (rVotedBrinePressure_bar - rPX_HP_OutPressure_bar) <= (c_rAlarm_PX_DP_H_bar - c_rDeadband_PX_DP_bar) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.15 := FALSE; END_IF;
END_IF;

(* -------------------------------------------------------------------------------------------------
   6.7 SILT DENSITY INDEX (SDI15) & SPECIFIC ENERGY CONSUMPTION (SEC) ALARMS
   ------------------------------------------------------------------------------------------------- *)
IF rSiltDensityIndex_SDI15 >= c_rAlarm_SDI_HH THEN
    dwAlarmWord_Primary.16 := TRUE; (* Bit 16: PRE_TREATMENT_SDI_CRITICAL_HIGH *)
    bWarningActive := TRUE;
ELSIF rSiltDensityIndex_SDI15 <= (c_rAlarm_SDI_HH - c_rDeadband_SDI) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.16 := FALSE; END_IF;
END_IF;

IF rSpecificEnergyConsump_kWh_m3 >= c_rAlarm_SEC_HH_kWh THEN
    dwAlarmWord_Primary.17 := TRUE; (* Bit 17: SPECIFIC_ENERGY_CONSUMPTION_HIGH_HIGH *)
    bWarningActive := TRUE;
ELSIF rSpecificEnergyConsump_kWh_m3 <= (c_rAlarm_SEC_HH_kWh - c_rDeadband_SEC_kWh) THEN
    IF bAcknowledgeAlarms THEN dwAlarmWord_Primary.17 := FALSE; END_IF;
END_IF;

(* Secondary Trip & Equipment Interlock Bit Packing into dwAlarmWord_Secondary *)
dwAlarmWord_Secondary.1 := (rPX_RotorSpeed_RPM < 400.0) AND (iState >= 50 AND iState <= 80); (* PX rotor stall *)
dwAlarmWord_Secondary.2 := (rFeed_Turbidity_NTU > 0.85); (* Cartridge filter breach *)
dwAlarmWord_Secondary.3 := (rFeedTemperature_degC > 42.0); (* High feed seawater temperature *)
dwAlarmWord_Secondary.7 := bFeedP_VoterFailed OR bBrineP_VoterFailed OR bPermCond_VoterFailed; (* Critical voter fault *)
dwAlarmWord_Secondary.8 := bDegradedSensorMode;
dwAlarmWord_Secondary.9 := bCIP_Active;
dwAlarmWord_Secondary.10 := bTrainRunning;

(* Diagnostic Status Subsystem Word Telemetry Packing *)
dwDiagnosticStatus.20 := (rPX_Efficiency_pct >= 95.0);
dwDiagnosticStatus.21 := (rSaltRejection_pct >= 99.70);
dwDiagnosticStatus.22 := (rSpecificEnergyConsump_kWh_m3 <= 2.80);
dwDiagnosticStatus.23 := (rNormPermeateFlow_m3h >= (0.90 * rRef_PermeateFlow_m3h));
dwDiagnosticStatus.24 := (iState = 60 OR iState = 70 OR iState = 80); (* Desalination Active *)
dwDiagnosticStatus.25 := (iState = 90 OR iState = 100 OR iState = 110); (* CIP Active *)
dwDiagnosticStatus.26 := (iState = 120); (* Emergency Dump Active *)
""")

    # -------------------------------------------------------------------------
    # 11. Closing Declaration
    # -------------------------------------------------------------------------
    parts.append("""
END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    st_code = build_swro_st_code()
    print(f"Generated ST code length: {len(st_code)} characters")
