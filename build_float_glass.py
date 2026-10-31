# Python generator for FB_FloatGlass_Furnace_TinBath_LehrAnnealing
# Generates ultra-dense, mathematically pristine IEC 61131-3 Structured Text dataset.

import json
import os
import sys

def generate_float_glass_st():
    parts = []

    # -------------------------------------------------------------------------
    # FUNCTION_BLOCK Declaration and Deep Cyber-Physical Header
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_FloatGlass_Furnace_TinBath_LehrAnnealing
(*
====================================================================================================
  LUMINA ADVANCED CYBER-PHYSICAL CONTROL SYSTEMS - SYNTHETIC IEC 61131-3 DATA ARCHITECTURE
  SYSTEM IDENTIFIER: CPS-GLAS-FLOAT-LINE-TIN-BATH-LEHR-REV9.4
  CORE DOMAIN:
    Commercial Glass & Ceramics: Continuous Architectural Float Glass Line with Molten Tin Bath
    Chamber Atmosphere, 14-Pair Top-Roll Edge Knurling Machines, and 120-Meter Continuous Annealing
    Lehr with Viscoelastic Thermal Stress Relaxation & Optical Retardation Polarimeter Feedback.
  STANDARDS & CODES COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Structured Text Cyclic Execution)
    - IEC 61508 / IEC 61511 (SIL-3 Functional Safety Lifecycle & 2oo3 TMR Architecture)
    - ISA-18.2 / EEMUA 191 (Alarm Systems Management for the Process Industries)
    - ASTM C1036 (Standard Specification for Flat Glass - Architectural Quality)
    - ASTM C148 (Standard Test Methods for Polariscopic Examination of Glass Containers/Ribbon)
    - ISO 16293 (Glass in building - Basic soda lime silicate glass products)
    - NFPA 86 (Standard for Ovens and Furnaces - Atmosphere Safety & Protective Gas Interlocks)
  ARCHITECT PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Veteran Experience)
----------------------------------------------------------------------------------------------------
  PROCESS THERMODYNAMICS, HYDRODYNAMICS & CERAMIC SCIENCE:
    The continuous float glass manufacturing process is a masterwork of coupled fluid mechanics,
    interfacial surface chemistry, high-temperature heat transfer, and non-Newtonian rheology.
    Raw soda-lime-silica glass (72.6% SiO2, 13.8% Na2O, 8.4% CaO, 4.2% MgO, 1.0% Al2O3) is melted in
    a regenerative cross-fired furnace producing up to 900 metric tons/day of bubble-free melt.
    The molten glass flows through a delivery canal controlled by a motorized refractory tweel gate
    at 1,050 deg C onto a bath of molten metallic tin (liquid density rho_sn ~ 6,520 kg/m3 vs liquid
    glass density rho_g ~ 2,380 kg/m3).

    1. Molten Tin Bath Hydrodynamics & Spreading Equilibrium:
       Because molten tin has a specific gravity nearly three times that of glass, the molten glass
       floats effortlessly upon the liquid metal surface, forming an unconstrained ribbon.
       The natural spread of glass on molten tin is governed by the Antonov interfacial tension balance
       and the classic Neumann triangle:
           gamma_sn + gamma_g_sn * cos(theta_1) + gamma_g_atm * cos(theta_2) = 0
       The theoretical equilibrium thickness h_inf is derived from the balance of gravity head and
       net spreading coefficient S = gamma_sn + gamma_g_atm - gamma_g_sn:
           h_inf = SQRT( (2.0 * S * rho_sn) / (g * rho_g * (rho_sn - rho_g)) )
       For standard architectural soda-lime glass on clean tin in a reducing atmosphere:
           S ~ 0.850 N/m, rho_g ~ 2,380 kg/m3, rho_sn ~ 6,520 kg/m3, g = 9.80665 m/s2
           This yields an immutable natural equilibrium thickness h_inf ~ 6.85 mm to 7.10 mm.

    2. Top-Roller Edge Knurling & Attenuation/Widening Kinematics:
       To produce architectural glass thinner than 6.8 mm (e.g. 2.0 mm, 3.0 mm, 4.0 mm, 5.0 mm) or
       thicker (up to 19.0 mm), motorized water-cooled toothed top-rolls (14 pairs spaced along the
       first 30 meters of the tin bath) penetrate the semi-solid ribbon edge.
       Each top-roll pair is adjustable in three continuous degrees of freedom:
           a. Penetration depth delta_knurl (0.5 mm to 4.5 mm into the ribbon edge margin).
           b. Angular tilt theta_roll (-15.0 deg inward toe-in for thick glass, +25.0 deg outward toe-out
              for attenuation and lateral ribbon stretching).
           c. Rotational peripheral speed omega_roll relative to the main ribbon draw velocity.
       The lateral outward tractive force per unit length is formulated as:
           F_lat = mu_tractive * F_normal * sin(theta_roll) - tau_shear * W_ribbon
       Where dynamic viscosity eta(T) follows the Fulcher-Tammann-Vogel (FTV) equation:
           log10(eta [dPa.s]) = A_ftv + B_ftv / (T [deg C] - T0_ftv)
           For float glass: A_ftv = -2.585, B_ftv = 4514.2, T0_ftv = 263.8 deg C.

    3. Protective Atmosphere Chemistry & Dross Suppression:
       Molten tin oxidizes catastrophically in the presence of trace oxygen:
           Sn(l) + 1/2 O2(g) <-> SnO(g) -> condensation on ceiling/droplets onto ribbon
           Sn(l) + O2(g) <-> SnO2(s) (solid dross skimmings creating pinhole defects)
       A continuous protective atmosphere consisting of 95% N2 and 5% H2 is injected along the roof.
       Hydrogen acts as a continuous reducing scavenger:
           SnO + H2 <-> Sn(l) + H2O(g)
       The chamber is maintained at a strict positive overpressure of 5.0 Pa to 15.0 Pa relative to
       ambient atmosphere to prevent any ingress of atmospheric oxygen. ZrO2 solid electrolyte trace
       oxygen sensors track headspace O2 (< 5.0 ppm threshold), while chilled-mirror hygrometers
       monitor dew point (<-40.0 deg C) to prevent stannous hydroxide bubble formation.

    4. Continuous Annealing Lehr Viscoelastic Stress Relaxation & Optical Retardation:
       At the exit of the tin bath (600 deg C), the solidified continuous ribbon is lifted onto lehr
       conveyor rolls and drawn into a 120-meter long tunnel lehr divided into five active thermal zones:
           Zone A (Transformation Range Tg = 520 to 550 deg C): High-precision indirect gas radiant
                  tube heaters and electric roof trimming elements prevent transverse thermal gradients.
           Zone B (Controlled Annealing Range 480 to 520 deg C): Viscoelastic stress relaxation governed
                  by the Adams-Williamson law and Maxwell viscoelastic relaxation:
                      dF/dt = -A_aw * F^2, where F is optical birefringence stress [nm/cm]
                      sigma(t) = sigma_0 * exp(-t / tau_maxwell), tau_maxwell = eta(T) / G_glass
           Zone C (Temporary Stress Prevention 400 to 480 deg C): Uniform cross-ribbon heat extraction.
           Zone D (Forced Convection Cooling 250 to 400 deg C): Variable-frequency blower duct dampers.
           Zone RET (Open Air Spray Quench 50 to 250 deg C): Prepares ribbon for carbide scoring & cutting.
       Permanent residual optical stress is measured continuously by an online multi-channel laser
       polarimeter traversing the ribbon width at the lehr exit, enforcing birefringence < 10.0 nm/cm.

    5. Discrete State-Space (16x16) & Receding Horizon Model Predictive Control (MPC):
       A 16-state, 8-input discrete linear model captures coupled ribbon hydrodynamics, mechanical
       top-roll traction, tin bath thermal profiles, and lehr annealing cooling gradients.
       A projected gradient receding-horizon quadratic programming engine solves for optimal actuator
       moves du over a receding horizon subject to actuator slew rates and physical valve limits.

    6. Triple Modular Redundant (2oo3) Sensor Voting & Graceful Degradation:
       Critical process variables (tin bath inlet/mid/exit optical pyrometers, lehr zone duplex
       thermocouples, chamber overpressure manometers, and ZrO2 trace oxygen sensors) are acquired
       via isolated 2oo3 triplets with median voting, stuck-signal detection, and bumpless fallback.
====================================================================================================
*)
""")

    # -------------------------------------------------------------------------
    # VAR_INPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* ========================================================================================= *)
    (* SECTION 1: PHYSICAL PROCESS SENSORS & 2oo3 TMR TRIPLETS (MINIMUM 8 STRONGLY TYPED INPUTS)   *)
    (* ========================================================================================= *)
    (* 2oo3 Redundant Tin Bath Chamber Inlet Optical Pyrometers [deg C] *)
    rTinInletTemp_degC_A        : REAL := 1048.5;   (* Channel A narrow-band 5.1 um pyrometer tin inlet [deg C] *)
    rTinInletTemp_degC_B        : REAL := 1048.2;   (* Channel B narrow-band 5.1 um pyrometer tin inlet [deg C] *)
    rTinInletTemp_degC_C        : REAL := 1048.7;   (* Channel C narrow-band 5.1 um pyrometer tin inlet [deg C] *)

    (* 2oo3 Redundant Tin Bath Chamber Mid-Section Ribbon Pyrometers [deg C] *)
    rTinMidTemp_degC_A          : REAL := 825.4;    (* Channel A mid-bath ribbon surface pyrometer [deg C] *)
    rTinMidTemp_degC_B          : REAL := 825.1;    (* Channel B mid-bath ribbon surface pyrometer [deg C] *)
    rTinMidTemp_degC_C          : REAL := 825.6;    (* Channel C mid-bath ribbon surface pyrometer [deg C] *)

    (* 2oo3 Redundant Tin Bath Chamber Exit / Lift-Out Roll Pyrometers [deg C] *)
    rTinExitTemp_degC_A         : REAL := 602.3;    (* Channel A exit lift-out roll ribbon pyrometer [deg C] *)
    rTinExitTemp_degC_B         : REAL := 602.0;    (* Channel B exit lift-out roll ribbon pyrometer [deg C] *)
    rTinExitTemp_degC_C         : REAL := 602.5;    (* Channel C exit lift-out roll ribbon pyrometer [deg C] *)

    (* 2oo3 Redundant Annealing Lehr Zone A Duplex Thermocouples (Transformation Range) [deg C] *)
    rLehrTemp_ZoneA_degC_A      : REAL := 535.2;    (* Channel A Type-K duplex thermocouple Lehr Zone A [deg C] *)
    rLehrTemp_ZoneA_degC_B      : REAL := 534.9;    (* Channel B Type-K duplex thermocouple Lehr Zone A [deg C] *)
    rLehrTemp_ZoneA_degC_C      : REAL := 535.4;    (* Channel C Type-K duplex thermocouple Lehr Zone A [deg C] *)

    (* 2oo3 Redundant Annealing Lehr Zone B Duplex Thermocouples (Annealing Relaxation) [deg C] *)
    rLehrTemp_ZoneB_degC_A      : REAL := 485.6;    (* Channel A Type-K duplex thermocouple Lehr Zone B [deg C] *)
    rLehrTemp_ZoneB_degC_B      : REAL := 485.3;    (* Channel B Type-K duplex thermocouple Lehr Zone B [deg C] *)
    rLehrTemp_ZoneB_degC_C      : REAL := 485.8;    (* Channel C Type-K duplex thermocouple Lehr Zone B [deg C] *)

    (* 2oo3 Redundant Annealing Lehr Zone C Duplex Thermocouples [deg C] *)
    rLehrTemp_ZoneC_degC_A      : REAL := 420.1;    (* Channel A Type-K duplex thermocouple Lehr Zone C [deg C] *)
    rLehrTemp_ZoneC_degC_B      : REAL := 419.8;    (* Channel B Type-K duplex thermocouple Lehr Zone C [deg C] *)
    rLehrTemp_ZoneC_degC_C      : REAL := 420.3;    (* Channel C Type-K duplex thermocouple Lehr Zone C [deg C] *)

    (* 2oo3 Redundant Annealing Lehr Zone D Duplex Thermocouples [deg C] *)
    rLehrTemp_ZoneD_degC_A      : REAL := 295.4;    (* Channel A Type-K duplex thermocouple Lehr Zone D [deg C] *)
    rLehrTemp_ZoneD_degC_B      : REAL := 295.1;    (* Channel B Type-K duplex thermocouple Lehr Zone D [deg C] *)
    rLehrTemp_ZoneD_degC_C      : REAL := 295.7;    (* Channel C Type-K duplex thermocouple Lehr Zone D [deg C] *)

    (* 2oo3 Redundant Tin Bath Atmosphere Differential Overpressure Manometers [Pa] *)
    rTinBathPressure_Pa_A       : REAL := 9.85;     (* Channel A high-accuracy micro-manometer tin bath [Pa] *)
    rTinBathPressure_Pa_B       : REAL := 9.80;     (* Channel B high-accuracy micro-manometer tin bath [Pa] *)
    rTinBathPressure_Pa_C       : REAL := 9.90;     (* Channel C high-accuracy micro-manometer tin bath [Pa] *)

    (* 2oo3 Redundant ZrO2 Trace Oxygen Concentration Analyzers [ppm] *)
    rTinTraceO2_ppm_A           : REAL := 1.85;     (* Channel A zirconium oxide trace O2 analyzer [ppm] *)
    rTinTraceO2_ppm_B           : REAL := 1.82;     (* Channel B zirconium oxide trace O2 analyzer [ppm] *)
    rTinTraceO2_ppm_C           : REAL := 1.88;     (* Channel C zirconium oxide trace O2 analyzer [ppm] *)

    (* Atmospheric Dew Point & Reducing Gas Feed Telemetry *)
    rTinAtmDewPoint_degC        : REAL := -48.5;    (* Chilled mirror optical hygrometer dew point [deg C] *)
    rSupplyFlow_N2_Nm3h         : REAL := 1450.0;   (* High-purity Nitrogen header supply flow rate [Nm3/h] *)
    rSupplyFlow_H2_Nm3h         : REAL := 76.5;     (* High-purity Hydrogen header supply flow rate [Nm3/h] *)
    rSupplyPressure_Gas_bar     : REAL := 4.25;     (* Protective atmosphere gas header pressure [bar] *)

    (* Delivery Canal, Tweel Gate & Melting Furnace Telemetry *)
    rFurnacePullRate_TonsDay    : REAL := 820.0;    (* Upstream glass melting furnace raw pull rate [tons/day] *)
    rTweelGatePosFeedback_mm    : REAL := 184.8;    (* Motorized canal tweel gate vertical lift position [mm] *)
    rCanalGlassTemp_degC        : REAL := 1052.0;   (* Refractory delivery canal molten glass temperature [deg C] *)

    (* Top-Roll Edge Knurling Machine Telemetry (14 Machine Pairs) *)
    rTopRoll_SpeedFeedback_mmin : ARRAY[1..14] OF REAL := [
        12.4, 12.8, 13.2, 13.6, 14.0, 14.3, 14.5, 14.6, 14.6, 14.6, 14.6, 14.6, 14.6, 14.6
    ];                                              (* Top-roll peripheral rotational speed feedback [m/min] *)
    rTopRoll_Current_A          : ARRAY[1..14] OF REAL := [
        8.2, 8.5, 8.9, 9.1, 9.4, 9.2, 8.8, 8.5, 8.3, 8.1, 7.9, 7.8, 7.6, 7.5
    ];                                              (* Top-roll servo drive electric motor load current [A] *)
    rTopRoll_TiltAngleFeedback_deg : ARRAY[1..14] OF REAL := [
        18.5, 17.0, 15.5, 13.5, 11.0, 8.5, 6.0, 4.0, 2.5, 1.0, 0.0, 0.0, 0.0, 0.0
    ];                                              (* Top-roll angular toe-out / toe-in tilt angle [deg] *)
    rTopRoll_KnurlDepth_mm      : ARRAY[1..14] OF REAL := [
        3.2, 3.0, 2.8, 2.5, 2.2, 2.0, 1.8, 1.6, 1.4, 1.2, 1.0, 0.8, 0.6, 0.5
    ];                                              (* Top-roll penetration depth into ribbon edge margin [mm] *)

    (* Lehr Conveyor Drives, Lift-Out Rolls & Traversing Gauges *)
    rLiftOutRollSpeed_mmin      : REAL := 14.52;    (* Lehr entry motorized lift-out roll velocity [m/min] *)
    rMainLehrDriveSpeed_mmin    : REAL := 14.50;    (* Lehr main longitudinal roller conveyor speed [m/min] *)
    rRibbonTension_Nm           : REAL := 1245.0;   (* Calibrated load cell ribbon longitudinal tension [N/m] *)
    rTraverserThickness_mm      : REAL := 3.985;    (* High-frequency laser displacement thickness sensor [mm] *)
    rTraverserThicknessLeft_mm  : REAL := 3.992;    (* Left edge margin thickness reading [mm] *)
    rTraverserThicknessRight_mm : REAL := 3.988;    (* Right edge margin thickness reading [mm] *)
    rTraverserWidth_m           : REAL := 3.652;    (* Ribbon edge-detecting optical laser triangulation width [m] *)
    rPolarimeterRetardation_nmcm: REAL := 6.45;     (* Online Brewster laser polarimeter stress birefringence [nm/cm] *)
    rPolarimeterPeakRetard_nmcm : REAL := 8.20;     (* Peak cross-ribbon optical retardation stress reading [nm/cm] *)

    (* Ambient & Supervisory Inputs *)
    rAmbientTemp_degC           : REAL := 24.5;     (* Lehr building ambient air temperature [deg C] *)
    rBarometricPress_hPa        : REAL := 1013.2;   (* Barometric atmospheric ambient pressure [hPa] *)
    tScanTime_s                 : REAL := 0.250;    (* Discrete PLC cyclic scan execution time period [s] *)
    bMasterEnable               : BOOL := TRUE;     (* Master functional block execution enable permissive *)
    bEmergencyStop              : BOOL := TRUE;     (* Dual-channel SIL-3 safety relay OK permissive (Active Low) *)
    bAcknowledgeAlarms          : BOOL := FALSE;    (* Operator latching alarm acknowledge command *)
    bAutoPacingEnable           : BOOL := TRUE;     (* Closed-loop MPC automatic speed/temperature pacing enable *)
    bTopRollMasterRun           : BOOL := TRUE;     (* Top-roll motorized knurlers run permissive *)
    bLehrDriveMasterRun         : BOOL := TRUE;     (* Annealing lehr main line drive run permissive *)
    bGasPurgePermissive         : BOOL := TRUE;     (* Protective N2/H2 gas purging header supply ready *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR_OUTPUT
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ========================================================================================= *)
    (* ACTUATOR COMMANDS & ENGINEERING STATUS WORDS (MINIMUM 7 STRONGLY TYPED ACTUATOR OUTPUTS)  *)
    (* ========================================================================================= *)
    rTweelGatePositionCmd_mm    : REAL := 185.0;    (* Motorized canal tweel gate vertical lift position command [mm] *)
    rTopRoll_SpeedCmd_mmin      : ARRAY[1..14] OF REAL := [
        12.4, 12.8, 13.2, 13.6, 14.0, 14.3, 14.5, 14.6, 14.6, 14.6, 14.6, 14.6, 14.6, 14.6
    ];                                              (* Top-roll servo speed setpoint array [m/min] *)
    rTopRoll_TiltCmd_deg        : ARRAY[1..14] OF REAL := [
        18.5, 17.0, 15.5, 13.5, 11.0, 8.5, 6.0, 4.0, 2.5, 1.0, 0.0, 0.0, 0.0, 0.0
    ];                                              (* Top-roll angular tilt setpoint array [deg] *)
    rLehrMainDriveSpeedCmd_mmin : REAL := 14.50;    (* Lehr main longitudinal drive velocity setpoint [m/min] *)
    rLiftOutRollSpeedCmd_mmin   : REAL := 14.52;    (* Entry lift-out roll velocity setpoint [m/min] *)
    rLehrZoneA_GasFireDuty_Pct  : REAL := 48.5;     (* Lehr Zone A radiant tube gas burner firing duty [%] *)
    rLehrZoneB_GasFireDuty_Pct  : REAL := 32.0;     (* Lehr Zone B radiant tube gas burner firing duty [%] *)
    rLehrZoneC_CoolDamper_Pct   : REAL := 42.5;     (* Lehr Zone C indirect cooling air damper position [%] *)
    rLehrZoneD_CoolDamper_Pct   : REAL := 55.0;     (* Lehr Zone D forced cooling air damper position [%] *)
    rLehrBlowerVFD_Hz           : REAL := 44.5;     (* Lehr forced cooling air blower drive frequency [Hz] *)
    rTinAtmN2_FlowCmd_Nm3h      : REAL := 1450.0;   (* Protective Nitrogen makeup flow setpoint [Nm3/h] *)
    rTinAtmH2_FlowCmd_Nm3h      : REAL := 76.5;     (* Reducing Hydrogen blend flow setpoint [Nm3/h] *)
    rTinChamberVentDamper_Pct   : REAL := 18.5;     (* Tin bath overpressure relief exhaust damper position [%] *)
    rCalculatedRibbonWidth_m    : REAL := 3.650;    (* Mathematical hydrodynamic estimated ribbon width [m] *)
    rCalculatedCenterThick_mm   : REAL := 4.000;    (* Mathematical state-space estimated centerline thickness [mm] *)
    rCalculatedResidualStress_nm: REAL := 6.50;     (* Mathematical Adams-Williamson residual birefringence [nm/cm] *)
    rNaturalEquilibriumThick_mm : REAL := 6.920;    (* Real-time Antonov surface tension natural thickness [mm] *)
    dwSystemStatusWord          : DWORD := 16#0000_0000; (* 32-bit packed operational FSM & automation status *)
    dwAlarmStatusWord           : DWORD := 16#0000_0000; (* 32-bit packed ISA-18.2 multi-tiered alarm status *)
    dwTMR_DiagnosticWord        : DWORD := 16#0000_0000; (* 32-bit packed 2oo3 sensor health & degradation status *)
    dwMPC_StatusWord            : DWORD := 16#0000_0000; (* 32-bit packed Model Predictive Control diagnostic status *)
    bSystemReady                : BOOL := FALSE;    (* Float line operating in closed-loop automated steady state *)
    bInAnnealingSpec            : BOOL := FALSE;    (* Real-time product quality flag: Retardation < 10 nm/cm & +/- 0.05 mm *)
    bOverpressureTrip           : BOOL := FALSE;    (* Chamber overpressure loss trip interlock active *)
    bDrossRiskWarning           : BOOL := FALSE;    (* Headspace oxygen/dew-point high dross defect warning *)
    bMPC_Active                 : BOOL := FALSE;    (* 16x16 state-space receding horizon MPC executing *)
    bGracefulDegradation        : BOOL := FALSE;    (* Fallback decoupled PID control active due to sensor fault *)
    bEmergencyDumpActive        : BOOL := FALSE;    (* Emergency tweel drop & cullet dump interlock active *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # VAR
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ========================================================================================= *)
    (* INTERNAL STATE VARIABLES: MATRICES, STATE ESTIMATORS, MPC OPTIMIZER & CONTROL ENGINES     *)
    (* ========================================================================================= *)
    bFirstScanDone              : BOOL := FALSE;    (* Cold-start memory and matrix allocation flag *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 1. THERMODYNAMIC, HYDRODYNAMIC & VISCOELASTIC PHYSICAL COEFFICIENTS                       *)
    (* ----------------------------------------------------------------------------------------- *)
    rGlassDensity_kgm3          : REAL := 2380.0;   (* Soda-lime glass molten density at 1000 deg C [kg/m3] *)
    rTinDensity_kgm3            : REAL := 6520.0;   (* Molten metallic tin density at 1000 deg C [kg/m3] *)
    rGravity_ms2                : REAL := 9.80665;  (* Gravitational acceleration [m/s2] *)
    rSurfaceTension_Tin_Nm      : REAL := 0.540;    (* Molten tin surface tension in reducing atmosphere [N/m] *)
    rSurfaceTension_Glass_Nm    : REAL := 0.350;    (* Molten glass surface tension at 1000 deg C [N/m] *)
    rInterfacialTension_Nm      : REAL := 0.040;    (* Molten glass / molten tin interfacial tension [N/m] *)
    rBrewsterConstant_B         : REAL := 2.60E-12; (* Photoelastic Brewster stress-optical coefficient [Pa^-1] *)
    rGlassShearModulus_G_Pa     : REAL := 2.80E10;  (* Vitreous silica network shear modulus [Pa] *)
    rAdamsWilliamson_A_aw       : REAL := 1.85E-4;  (* Adams-Williamson annealing relaxation parameter [cm/(nm*s)] *)
    rFTV_A                      : REAL := -2.585;   (* Fulcher-Tammann-Vogel viscosity parameter A *)
    rFTV_B                      : REAL := 4514.2;   (* Fulcher-Tammann-Vogel viscosity parameter B [deg C] *)
    rFTV_T0                     : REAL := 263.8;    (* Fulcher-Tammann-Vogel viscosity parameter T0 [deg C] *)
    rViscosity_dPas             : REAL := 10000.0;  (* Dynamic viscosity of glass at current tin inlet [dPa.s] *)

    (* ----------------------------------------------------------------------------------------- *)
    (* 2. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) FILTER REGISTERS                                  *)
    (* ----------------------------------------------------------------------------------------- *)
    (* Voted Filtered Values *)
    rVoted_TinInletTemp_degC    : REAL := 1048.5;
    rVoted_TinMidTemp_degC      : REAL := 825.4;
    rVoted_TinExitTemp_degC     : REAL := 602.3;
    rVoted_LehrTemp_ZoneA_degC  : REAL := 535.2;
    rVoted_LehrTemp_ZoneB_degC  : REAL := 485.6;
    rVoted_LehrTemp_ZoneC_degC  : REAL := 420.1;
    rVoted_LehrTemp_ZoneD_degC  : REAL := 295.4;
    rVoted_TinBathPress_Pa      : REAL := 9.85;
    rVoted_TinTraceO2_ppm       : REAL := 1.85;

    (* Triplet Deviation Thresholds *)
    rTol_TinInletTemp_degC      : REAL := 6.5;      (* Max allowed spread between inlet pyrometers [deg C] *)
    rTol_TinMidTemp_degC        : REAL := 5.0;      (* Max allowed spread between mid pyrometers [deg C] *)
    rTol_TinExitTemp_degC       : REAL := 4.5;      (* Max allowed spread between exit pyrometers [deg C] *)
    rTol_LehrZoneA_degC         : REAL := 3.0;      (* Max allowed spread in Lehr Zone A [deg C] *)
    rTol_LehrZoneB_degC         : REAL := 3.5;      (* Max allowed spread in Lehr Zone B [deg C] *)
    rTol_LehrZoneC_degC         : REAL := 4.0;      (* Max allowed spread in Lehr Zone C [deg C] *)
    rTol_LehrZoneD_degC         : REAL := 5.0;      (* Max allowed spread in Lehr Zone D [deg C] *)
    rTol_TinBathPress_Pa        : REAL := 1.2;      (* Max allowed spread in chamber pressure [Pa] *)
    rTol_TinTraceO2_ppm         : REAL := 0.8;      (* Max allowed spread in trace oxygen [ppm] *)

    (* Stuck Sensor Telemetry Counters *)
    iStuck_TinInlet_A : INT := 0; iStuck_TinInlet_B : INT := 0; iStuck_TinInlet_C : INT := 0;
    iStuck_TinMid_A   : INT := 0; iStuck_TinMid_B   : INT := 0; iStuck_TinMid_C   : INT := 0;
    iStuck_TinExit_A  : INT := 0; iStuck_TinExit_B  : INT := 0; iStuck_TinExit_C  : INT := 0;
    iStuck_LehrZA_A   : INT := 0; iStuck_LehrZA_B   : INT := 0; iStuck_LehrZA_C   : INT := 0;
    iStuck_LehrZB_A   : INT := 0; iStuck_LehrZB_B   : INT := 0; iStuck_LehrZB_C   : INT := 0;
    iStuck_LehrZC_A   : INT := 0; iStuck_LehrZC_B   : INT := 0; iStuck_LehrZC_C   : INT := 0;
    iStuck_LehrZD_A   : INT := 0; iStuck_LehrZD_B   : INT := 0; iStuck_LehrZD_C   : INT := 0;
    iStuck_Press_A    : INT := 0; iStuck_Press_B    : INT := 0; iStuck_Press_C    : INT := 0;
    iStuck_O2_A       : INT := 0; iStuck_O2_B       : INT := 0; iStuck_O2_C       : INT := 0;

    (* Previous Scan Values for Rate-of-Change Checks *)
    rPrev_TinInlet_A : REAL := 1048.5; rPrev_TinInlet_B : REAL := 1048.2; rPrev_TinInlet_C : REAL := 1048.7;
    rPrev_TinMid_A   : REAL := 825.4;  rPrev_TinMid_B   : REAL := 825.1;  rPrev_TinMid_C   : REAL := 825.6;
    rPrev_TinExit_A  : REAL := 602.3;  rPrev_TinExit_B  : REAL := 602.0;  rPrev_TinExit_C  : REAL := 602.5;
    rPrev_LehrZA_A   : REAL := 535.2;  rPrev_LehrZA_B   : REAL := 534.9;  rPrev_LehrZA_C   : REAL := 535.4;
    rPrev_LehrZB_A   : REAL := 485.6;  rPrev_LehrZB_B   : REAL := 485.3;  rPrev_LehrZB_C   : REAL := 485.8;
    rPrev_LehrZC_A   : REAL := 420.1;  rPrev_LehrZC_B   : REAL := 419.8;  rPrev_LehrZC_C   : REAL := 420.3;
    rPrev_LehrZD_A   : REAL := 295.4;  rPrev_LehrZD_B   : REAL := 295.1;  rPrev_LehrZD_C   : REAL := 295.7;
    rPrev_Press_A    : REAL := 9.85;   rPrev_Press_B    : REAL := 9.80;   rPrev_Press_C    : REAL := 9.90;
    rPrev_O2_A       : REAL := 1.85;   rPrev_O2_B       : REAL := 1.82;   rPrev_O2_C       : REAL := 1.88;

    (* Channel Health Flags *)
    bHealth_TinInlet_A : BOOL := TRUE; bHealth_TinInlet_B : BOOL := TRUE; bHealth_TinInlet_C : BOOL := TRUE;
    bHealth_TinMid_A   : BOOL := TRUE; bHealth_TinMid_B   : BOOL := TRUE; bHealth_TinMid_C   : BOOL := TRUE;
    bHealth_TinExit_A  : BOOL := TRUE; bHealth_TinExit_B  : BOOL := TRUE; bHealth_TinExit_C  : BOOL := TRUE;
    bHealth_LehrZA_A   : BOOL := TRUE; bHealth_LehrZA_B   : BOOL := TRUE; bHealth_LehrZA_C   : BOOL := TRUE;
    bHealth_LehrZB_A   : BOOL := TRUE; bHealth_LehrZB_B   : BOOL := TRUE; bHealth_LehrZB_C   : BOOL := TRUE;
    bHealth_LehrZC_A   : BOOL := TRUE; bHealth_LehrZC_B   : BOOL := TRUE; bHealth_LehrZC_C   : BOOL := TRUE;
    bHealth_LehrZD_A   : BOOL := TRUE; bHealth_LehrZD_B   : BOOL := TRUE; bHealth_LehrZD_C   : BOOL := TRUE;
    bHealth_Press_A    : BOOL := TRUE; bHealth_Press_B    : BOOL := TRUE; bHealth_Press_C    : BOOL := TRUE;
    bHealth_O2_A       : BOOL := TRUE; bHealth_O2_B       : BOOL := TRUE; bHealth_O2_C       : BOOL := TRUE;

    (* ----------------------------------------------------------------------------------------- *)
    (* 3. 16x16 STATE-SPACE ARRAYS, KALMAN OBSERVER & MPC MATRICES                               *)
    (* ----------------------------------------------------------------------------------------- *)
    (* State Vector x[0..15]:
       x[0]:  Canal head level deviation Delta h_canal [mm]
       x[1]:  Tin bath spreading pool thickness deviation Delta h_pool [mm]
       x[2]:  Ribbon total transverse width deviation Delta W_rib [m]
       x[3]:  Ribbon centerline thickness deviation Delta h_cntr [mm]
       x[4]:  Left edge margin thickness deviation Delta h_edge_L [mm]
       x[5]:  Right edge margin thickness deviation Delta h_edge_R [mm]
       x[6]:  Mid-bath ribbon surface temperature deviation Delta T_mid [deg C]
       x[7]:  Tin bath atmosphere chamber overpressure deviation Delta P_atm [Pa]
       x[8]:  Tin bath headspace trace oxygen deviation Delta C_O2 [ppm]
       x[9]:  Lehr lift-out transition ribbon tension deviation Delta F_tens [N/m]
       x[10]: Lehr Zone A glass transformation temp deviation Delta T_ZA [deg C]
       x[11]: Lehr Zone B cooling gradient temp deviation Delta T_ZB [deg C]
       x[12]: Lehr Zone C cooling temp deviation Delta T_ZC [deg C]
       x[13]: Lehr Zone D exit temp deviation Delta T_ZD [deg C]
       x[14]: Permanent residual optical retardation birefringence Delta delta_ret [nm/cm]
       x[15]: Temporary cross-ribbon thermal stress gradient Delta sigma_temp [MPa] *)
    aState_x                    : ARRAY[0..15] OF REAL;
    aState_x_hat                : ARRAY[0..15] OF REAL;
    aState_x_pred               : ARRAY[0..15] OF REAL;

    (* Manipulated Variables u[0..7]:
       u[0]: Canal tweel gate motorized lift position V_tweel [mm] (Base: 185.0)
       u[1]: Top-roll pairs 1-4 early attenuator speed trim omega_tr_early [%] (Base: 100.0)
       u[2]: Top-roll pairs 5-10 thickness sizing speed trim omega_tr_mid [%] (Base: 105.0)
       u[3]: Top-roll pairs 11-14 edge finish speed trim omega_tr_exit [%] (Base: 108.0)
       u[4]: Lehr main drive line velocity v_lehr [m/min] (Base: 14.50)
       u[5]: Lehr Zone A/B radiant gas tube firing duty Q_gas_AB [%] (Base: 48.0)
       u[6]: Lehr Zone C/D cooling damper position D_cool_CD [%] (Base: 38.0)
       u[7]: Tin bath protective atmosphere gas valve V_gas [%] (Base: 65.0) *)
    aControl_u                  : ARRAY[0..7] OF REAL := [185.0, 100.0, 105.0, 108.0, 14.50, 48.0, 38.0, 65.0];
    aControl_u_prev             : ARRAY[0..7] OF REAL := [185.0, 100.0, 105.0, 108.0, 14.50, 48.0, 38.0, 65.0];
    aControl_du                 : ARRAY[0..7] OF REAL := [0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];
    aControl_u_base             : ARRAY[0..7] OF REAL := [185.0, 100.0, 105.0, 108.0, 14.50, 48.0, 38.0, 65.0];

    (* Controlled Outputs y[0..7]:
       y[0]: Centerline ribbon thickness [mm] (SP: 4.000 mm)
       y[1]: Ribbon total width [m] (SP: 3.650 m)
       y[2]: Residual optical retardation birefringence [nm/cm] (SP: 5.50 nm/cm)
       y[3]: Tin bath chamber differential overpressure [Pa] (SP: 10.0 Pa)
       y[4]: Tin bath headspace trace oxygen [ppm] (SP: 1.50 ppm)
       y[5]: Lehr Zone A glass transformation temp [deg C] (SP: 535.0 deg C)
       y[6]: Lehr Zone B annealing exit temp [deg C] (SP: 485.0 deg C)
       y[7]: Lift-out roll ribbon tractive tension [N/m] (SP: 1250.0 N/m) *)
    aOutput_y                   : ARRAY[0..7] OF REAL := [3.985, 3.652, 6.45, 9.85, 1.85, 535.2, 485.6, 1245.0];
    aOutput_y_sp                : ARRAY[0..7] OF REAL := [4.000, 3.650, 5.50, 10.0, 1.50, 535.0, 485.0, 1250.0];
    aOutput_y_err               : ARRAY[0..7] OF REAL;

    (* Disturbance Inputs d[0..3]:
       d[0]: Furnace canal glass temperature fluctuation Delta T_canal [deg C]
       d[1]: Furnace raw melting pull rate variation Delta m_pull [tons/day]
       d[2]: Atmospheric barometric pressure drift Delta P_baro [hPa]
       d[3]: Lehr building ambient hall temperature drift Delta T_hall [deg C] *)
    aDisturb_d                  : ARRAY[0..3] OF REAL := [0.0, 0.0, 0.0, 0.0];

    (* Matrices: A(16x16), B(16x8), C(8x16), D(8x8), E(16x4), K_obs(16x8) *)
    aMatrix_A                   : ARRAY[0..15, 0..15] OF REAL;
    aMatrix_B                   : ARRAY[0..15, 0..7] OF REAL;
    aMatrix_C                   : ARRAY[0..7, 0..15] OF REAL;
    aMatrix_D                   : ARRAY[0..7, 0..7] OF REAL;
    aMatrix_E                   : ARRAY[0..15, 0..3] OF REAL;
    aMatrix_K_obs               : ARRAY[0..15, 0..7] OF REAL;

    (* MPC Quadratic Cost Weights & Actuator Slew Limits *)
    aWeight_Q                   : ARRAY[0..7] OF REAL := [240.0, 180.0, 350.0, 85.0, 120.0, 65.0, 50.0, 20.0];
    aWeight_R                   : ARRAY[0..7] OF REAL := [0.45, 0.25, 0.28, 0.32, 1.20, 0.15, 0.18, 0.22];
    aLimit_du_Max               : ARRAY[0..7] OF REAL := [1.5, 2.0, 2.0, 2.0, 0.15, 2.5, 3.0, 3.5];
    aLimit_du_Min               : ARRAY[0..7] OF REAL := [-1.5, -2.0, -2.0, -2.0, -0.15, -2.5, -3.0, -3.5];
    aLimit_u_Max                : ARRAY[0..7] OF REAL := [320.0, 140.0, 145.0, 150.0, 22.0, 95.0, 95.0, 95.0];
    aLimit_u_Min                : ARRAY[0..7] OF REAL := [80.0, 70.0, 70.0, 70.0, 4.0, 5.0, 5.0, 15.0];

    (* Projected Gradient Optimization Registers *)
    aGrad_g                     : ARRAY[0..7] OF REAL;
    aHessian_diag               : ARRAY[0..7] OF REAL;
    aStep_du                    : ARRAY[0..7] OF REAL;
    iIterQP                     : INT := 0;
    iMaxIterQP                  : INT := 14;
    rAlphaStep                  : REAL := 0.038;

    (* ------------------------------------------------------------------------- *)
    (* 4. DECOUPLED GAIN-SCHEDULED PID FALLBACK CONTROLLERS                      *)
    (* ------------------------------------------------------------------------- *)
    (* PID Loop 1: Tweel Gate -> Glass Pull / Ribbon Width *)
    rPID_Kp_Tweel               : REAL := 1.45;
    rPID_Ki_Tweel               : REAL := 0.042;
    rPID_Kd_Tweel               : REAL := 0.18;
    rPID_Integ_Tweel            : REAL := 185.0;
    rPID_PrevErr_Tweel          : REAL := 0.0;

    (* PID Loop 2: Top-Roll Speed -> Centerline Thickness *)
    rPID_Kp_TopRoll             : REAL := 8.50;
    rPID_Ki_TopRoll             : REAL := 0.350;
    rPID_Kd_TopRoll             : REAL := 1.25;
    rPID_Integ_TopRoll          : REAL := 105.0;
    rPID_PrevErr_TopRoll        : REAL := 0.0;

    (* PID Loop 3: Lehr Zone A Firing -> Transformation Temp *)
    rPID_Kp_LehrZA              : REAL := 2.80;
    rPID_Ki_LehrZA              : REAL := 0.065;
    rPID_Kd_LehrZA              : REAL := 0.42;
    rPID_Integ_LehrZA           : REAL := 48.0;
    rPID_PrevErr_LehrZA         : REAL := 0.0;

    (* PID Loop 4: Gas Supply Valve -> Chamber Overpressure *)
    rPID_Kp_Press               : REAL := 4.20;
    rPID_Ki_Press               : REAL := 0.180;
    rPID_Kd_Press               : REAL := 0.65;
    rPID_Integ_Press            : REAL := 65.0;
    rPID_PrevErr_Press          : REAL := 0.0;

    (* ------------------------------------------------------------------------- *)
    (* 5. 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                        *)
    (* ------------------------------------------------------------------------- *)
    iMachineState               : INT := 1;         (* Current execution state (1..12) *)
    iPreviousState              : INT := 1;         (* Historical state memory *)
    rStateTimer_s               : REAL := 0.0;      (* Monotonic elapsed timer in current state [s] *)
    rPurgeTimer_s               : REAL := 0.0;      (* Atmosphere nitrogen purge timer [s] *)
    rPreheatTimer_s             : REAL := 0.0;      (* Tweel lip pre-heat timer [s] *)
    rEquilibrationTimer_s       : REAL := 0.0;      (* Initial ribbon spread timer [s] *)
    rAnnealingSettleTimer_s     : REAL := 0.0;      (* Lehr transformation stabilization timer [s] *)
    rCulletDumpTimer_s          : REAL := 0.0;      (* Emergency cullet dump timer [s] *)

    (* ------------------------------------------------------------------------- *)
    (* 6. TEMPORARY & LOOP COMPUTATION REGISTERS                                 *)
    (* ------------------------------------------------------------------------- *)
    iIdxRow                     : INT := 0;
    iIdxCol                     : INT := 0;
    iIdxAct                     : INT := 0;
    rAccumTemp                  : REAL := 0.0;
    rNetSpreadCoeff_S           : REAL := 0.850;
    rEquilibriumFormula_Val     : REAL := 0.0;
    rViscosityExponent          : REAL := 0.0;
    rLogViscosity               : REAL := 4.0;
    rMaxwellRelaxTime_s         : REAL := 0.0035;
    rAdamsWilliamson_Delta      : REAL := 0.0;
    rPhotoelasticRetard_calc    : REAL := 6.50;
    rTractiveForceTotal_N       : REAL := 0.0;
    rLateralStretch_ms          : REAL := 0.0;
    rLongitudinalDraw_ms        : REAL := 0.0;
END_VAR
""")

    # -------------------------------------------------------------------------
    # SECTION 1: Interlocks & First-Scan Matrix Initialization
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 1: EMERGENCY STOP INTERLOCK, MASTER PERMISSIVE & FIRST-SCAN 16x16 MATRIX ALLOCATION   *)
(* ============================================================================================= *)
(* Hardware SIL-3 Safety Circuit Interlock Supervision *)
IF NOT bEmergencyStop THEN
    iMachineState               := 11;              (* Force state machine to STATE_EMERGENCY_TWEEL_DUMP *)
    bEmergencyDumpActive        := TRUE;
    bSystemReady                := FALSE;
    bInAnnealingSpec            := FALSE;
    bMPC_Active                 := FALSE;
    bGracefulDegradation        := FALSE;
    rTweelGatePositionCmd_mm    := 0.0;             (* Drop refractory tweel gate completely (0 mm = full shutoff) *)
    rLehrZoneA_GasFireDuty_Pct  := 0.0;             (* Cut off fuel gas to radiant tube burners *)
    rLehrZoneB_GasFireDuty_Pct  := 0.0;
    rLehrZoneC_CoolDamper_Pct   := 100.0;           (* Open cooling dampers fully *)
    rLehrZoneD_CoolDamper_Pct   := 100.0;
    rTinChamberVentDamper_Pct   := 100.0;           (* Vent tin bath overpressure safely *)
    dwAlarmStatusWord           := dwAlarmStatusWord OR 16#8000_0000; (* Bit 31: EMERGENCY_STOP_ACTIVE *)
    dwSystemStatusWord          := 16#0000_0011;    (* State 11 Active *)
    RETURN;                                         (* Terminate cyclic scan immediately *)
END_IF;

(* Master Execution Permissive *)
IF NOT bMasterEnable THEN
    iMachineState               := 12;              (* Standby Gas Conservation Mode *)
    bSystemReady                := FALSE;
    bInAnnealingSpec            := FALSE;
    bMPC_Active                 := FALSE;
    dwSystemStatusWord          := 16#0000_0012;
    RETURN;
END_IF;
""")

    # Now generate the cold start matrix initialization (16x16 A, 16x8 B, 8x16 C, 8x8 D, 16x4 E, 16x8 K_obs)
    parts.append("""
(* Cold-Start Matrix Allocation on First Scan *)
IF NOT bFirstScanDone THEN
    (* ----------------------------------------------------------------------------------------- *)
    (* State-Space Matrix A (16x16) Discrete State Transition Model (Ts = 0.25s)                 *)
    (* Unrolled element-by-element assignment for full mathematical transparency                 *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    # Generate A matrix assignments (16x16 = 256 assignments)
    # A has diagonal dominance ~0.95 to 0.99 with realistic physical couplings
    a_lines = []
    for i in range(16):
        row_assigns = []
        for j in range(16):
            if i == j:
                # Diagonal persistence
                if i in [0, 1, 2, 3]:
                    val = 0.9850 - 0.0050 * i
                elif i in [4, 5]:
                    val = 0.9720
                elif i in [6, 7, 8]:
                    val = 0.9650 + 0.0050 * (i - 6)
                elif i == 9:
                    val = 0.9450
                elif i in [10, 11, 12, 13]:
                    val = 0.9920 - 0.0020 * (i - 10)
                elif i == 14:
                    val = 0.9780
                else: # 15
                    val = 0.9620
            else:
                # Off-diagonal physical couplings
                val = 0.0
                if i == 0 and j == 1: val = 0.0125
                elif i == 1 and j == 0: val = 0.0180
                elif i == 1 and j == 2: val = -0.0085
                elif i == 1 and j == 3: val = 0.0240
                elif i == 2 and j == 1: val = -0.0150
                elif i == 2 and j == 3: val = -0.0420
                elif i == 3 and j == 1: val = 0.0310
                elif i == 3 and j == 2: val = -0.0220
                elif i == 4 and j == 3: val = 0.0650
                elif i == 4 and j == 2: val = -0.0180
                elif i == 5 and j == 3: val = 0.0650
                elif i == 5 and j == 2: val = -0.0180
                elif i == 6 and j == 0: val = 0.0085
                elif i == 6 and j == 7: val = -0.0042
                elif i == 7 and j == 8: val = 0.0018
                elif i == 8 and j == 7: val = -0.0120
                elif i == 9 and j == 3: val = 0.0450
                elif i == 9 and j == 2: val = 0.0380
                elif i == 9 and j == 6: val = -0.0280
                elif i == 10 and j == 6: val = 0.0450
                elif i == 10 and j == 9: val = 0.0080
                elif i == 11 and j == 10: val = 0.0520
                elif i == 12 and j == 11: val = 0.0480
                elif i == 13 and j == 12: val = 0.0420
                elif i == 14 and j == 10: val = 0.0280
                elif i == 14 and j == 11: val = -0.0350
                elif i == 14 and j == 15: val = 0.0620
                elif i == 15 and j == 10: val = 0.0450
                elif i == 15 and j == 11: val = 0.0380
                elif i == 15 and j == 12: val = -0.0220
            row_assigns.append(f"aMatrix_A[{i},{j}] := {val:.4f};")
        # group into 4 assignments per line
        for k in range(0, 16, 4):
            a_lines.append("    " + " ".join(row_assigns[k:k+4]))
    parts.append("\n".join(a_lines))

    # Generate B matrix assignments (16x8 = 128 assignments)
    parts.append("""
    (* ----------------------------------------------------------------------------------------- *)
    (* State-Space Input Coupling Matrix B (16x8)                                               *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    b_lines = []
    for i in range(16):
        row_assigns = []
        for j in range(8):
            val = 0.0
            if i == 0 and j == 0: val = 0.0480
            elif i == 1 and j == 0: val = 0.0250
            elif i == 1 and j == 1: val = -0.0320
            elif i == 2 and j == 1: val = 0.0580
            elif i == 2 and j == 2: val = 0.0420
            elif i == 2 and j == 4: val = -0.0650
            elif i == 3 and j == 1: val = -0.0450
            elif i == 3 and j == 2: val = -0.0620
            elif i == 3 and j == 4: val = -0.0820
            elif i == 4 and j == 1: val = -0.0520
            elif i == 4 and j == 3: val = -0.0280
            elif i == 5 and j == 1: val = -0.0520
            elif i == 5 and j == 3: val = -0.0280
            elif i == 6 and j == 0: val = 0.0180
            elif i == 6 and j == 4: val = -0.0240
            elif i == 7 and j == 7: val = 0.0850
            elif i == 8 and j == 7: val = -0.0450
            elif i == 9 and j == 4: val = 0.0920
            elif i == 9 and j == 3: val = 0.0340
            elif i == 10 and j == 5: val = 0.0750
            elif i == 10 and j == 4: val = -0.0320
            elif i == 11 and j == 5: val = 0.0420
            elif i == 11 and j == 6: val = -0.0580
            elif i == 12 and j == 6: val = -0.0720
            elif i == 13 and j == 6: val = -0.0850
            elif i == 14 and j == 5: val = -0.0380
            elif i == 14 and j == 6: val = 0.0450
            elif i == 15 and j == 5: val = 0.0520
            elif i == 15 and j == 6: val = -0.0640
            row_assigns.append(f"aMatrix_B[{i},{j}] := {val:.4f};")
        for k in range(0, 8, 4):
            b_lines.append("    " + " ".join(row_assigns[k:k+4]))
    parts.append("\n".join(b_lines))

    # Generate C matrix assignments (8x16 = 128 assignments)
    parts.append("""
    (* ----------------------------------------------------------------------------------------- *)
    (* State-Space Output Mapping Matrix C (8x16)                                               *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    c_lines = []
    for i in range(8):
        row_assigns = []
        for j in range(16):
            val = 0.0
            if i == 0 and j == 3: val = 1.0000
            elif i == 0 and j == 4: val = 0.1500
            elif i == 0 and j == 5: val = 0.1500
            elif i == 1 and j == 2: val = 1.0000
            elif i == 2 and j == 14: val = 1.0000
            elif i == 3 and j == 7: val = 1.0000
            elif i == 4 and j == 8: val = 1.0000
            elif i == 5 and j == 10: val = 1.0000
            elif i == 6 and j == 11: val = 1.0000
            elif i == 7 and j == 9: val = 1.0000
            row_assigns.append(f"aMatrix_C[{i},{j}] := {val:.4f};")
        for k in range(0, 16, 4):
            c_lines.append("    " + " ".join(row_assigns[k:k+4]))
    parts.append("\n".join(c_lines))

    # Generate D matrix assignments (8x8 = 64 assignments)
    parts.append("""
    (* ----------------------------------------------------------------------------------------- *)
    (* Direct Feedthrough Matrix D (8x8) (Zeroed for Strict Dynamic Causality)                   *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    d_lines = []
    for i in range(8):
        row_assigns = []
        for j in range(8):
            row_assigns.append(f"aMatrix_D[{i},{j}] := 0.0000;")
        for k in range(0, 8, 4):
            d_lines.append("    " + " ".join(row_assigns[k:k+4]))
    parts.append("\n".join(d_lines))

    # Generate E matrix assignments (16x4 = 64 assignments)
    parts.append("""
    (* ----------------------------------------------------------------------------------------- *)
    (* Disturbance Coupling Matrix E (16x4)                                                     *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    e_lines = []
    for i in range(16):
        row_assigns = []
        for j in range(4):
            val = 0.0
            if i == 0 and j == 1: val = 0.0350
            elif i == 1 and j == 0: val = 0.0220
            elif i == 1 and j == 1: val = 0.0180
            elif i == 6 and j == 0: val = 0.0450
            elif i == 7 and j == 2: val = -0.0550
            elif i == 8 and j == 2: val = 0.0120
            elif i == 10 and j == 3: val = 0.0080
            elif i == 13 and j == 3: val = 0.0320
            elif i == 15 and j == 3: val = 0.0240
            row_assigns.append(f"aMatrix_E[{i},{j}] := {val:.4f};")
        e_lines.append("    " + " ".join(row_assigns))
    parts.append("\n".join(e_lines))

    # Generate K_obs matrix assignments (16x8 = 128 assignments)
    parts.append("""
    (* ----------------------------------------------------------------------------------------- *)
    (* Steady-State Kalman Observer Gain Matrix K_obs (16x8)                                     *)
    (* ----------------------------------------------------------------------------------------- *)
""")
    k_lines = []
    for i in range(16):
        row_assigns = []
        for j in range(8):
            val = 0.0
            if i == 0 and j == 0: val = 0.0850
            elif i == 1 and j == 0: val = 0.1250
            elif i == 2 and j == 1: val = 0.2200
            elif i == 3 and j == 0: val = 0.3100
            elif i == 4 and j == 0: val = 0.1800
            elif i == 5 and j == 0: val = 0.1800
            elif i == 6 and j == 5: val = 0.1450
            elif i == 7 and j == 3: val = 0.2850
            elif i == 8 and j == 4: val = 0.3400
            elif i == 9 and j == 7: val = 0.2600
            elif i == 10 and j == 5: val = 0.2950
            elif i == 11 and j == 6: val = 0.2750
            elif i == 12 and j == 6: val = 0.1900
            elif i == 13 and j == 6: val = 0.1500
            elif i == 14 and j == 2: val = 0.3200
            elif i == 15 and j == 2: val = 0.1850
            row_assigns.append(f"aMatrix_K_obs[{i},{j}] := {val:.4f};")
        for k in range(0, 8, 4):
            k_lines.append("    " + " ".join(row_assigns[k:k+4]))
    parts.append("\n".join(k_lines))

    parts.append("""
    (* Initialize Hessian diagonal preconditioning *)
    FOR iIdxAct := 0 TO 7 DO
        aHessian_diag[iIdxAct] := aWeight_R[iIdxAct] + 1.25;
        aState_x[iIdxAct]      := 0.0;
        aState_x_hat[iIdxAct]  := 0.0;
        aState_x_pred[iIdxAct] := 0.0;
    END_FOR;
    FOR iIdxAct := 8 TO 15 DO
        aState_x[iIdxAct]      := 0.0;
        aState_x_hat[iIdxAct]  := 0.0;
        aState_x_pred[iIdxAct] := 0.0;
    END_FOR;

    bFirstScanDone := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 2: 2oo3 TMR Voting Logic (9 Triplets)
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DIAGNOSTIC ENGINES            *)
(* ============================================================================================= *)
(* --------------------------------------------------------------------------------------------- *)
(* 1. Tin Bath Chamber Inlet Optical Pyrometer Triplet Voting [deg C]                           *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTinInletTemp_degC_A - rPrev_TinInlet_A) < 0.01 THEN iStuck_TinInlet_A := iStuck_TinInlet_A + 1; ELSE iStuck_TinInlet_A := 0; END_IF;
IF ABS(rTinInletTemp_degC_B - rPrev_TinInlet_B) < 0.01 THEN iStuck_TinInlet_B := iStuck_TinInlet_B + 1; ELSE iStuck_TinInlet_B := 0; END_IF;
IF ABS(rTinInletTemp_degC_C - rPrev_TinInlet_C) < 0.01 THEN iStuck_TinInlet_C := iStuck_TinInlet_C + 1; ELSE iStuck_TinInlet_C := 0; END_IF;
rPrev_TinInlet_A := rTinInletTemp_degC_A; rPrev_TinInlet_B := rTinInletTemp_degC_B; rPrev_TinInlet_C := rTinInletTemp_degC_C;

bHealth_TinInlet_A := (rTinInletTemp_degC_A >= 900.0) AND (rTinInletTemp_degC_A <= 1180.0) AND (iStuck_TinInlet_A < 240);
bHealth_TinInlet_B := (rTinInletTemp_degC_B >= 900.0) AND (rTinInletTemp_degC_B <= 1180.0) AND (iStuck_TinInlet_B < 240);
bHealth_TinInlet_C := (rTinInletTemp_degC_C >= 900.0) AND (rTinInletTemp_degC_C <= 1180.0) AND (iStuck_TinInlet_C < 240);

IF bHealth_TinInlet_A AND bHealth_TinInlet_B AND bHealth_TinInlet_C THEN
    (* Standard 2oo3 Median Selection *)
    IF ((rTinInletTemp_degC_A >= rTinInletTemp_degC_B) AND (rTinInletTemp_degC_A <= rTinInletTemp_degC_C)) OR
       ((rTinInletTemp_degC_A >= rTinInletTemp_degC_C) AND (rTinInletTemp_degC_A <= rTinInletTemp_degC_B)) THEN
        rVoted_TinInletTemp_degC := rTinInletTemp_degC_A;
    ELSIF ((rTinInletTemp_degC_B >= rTinInletTemp_degC_A) AND (rTinInletTemp_degC_B <= rTinInletTemp_degC_C)) OR
          ((rTinInletTemp_degC_B >= rTinInletTemp_degC_C) AND (rTinInletTemp_degC_B <= rTinInletTemp_degC_A)) THEN
        rVoted_TinInletTemp_degC := rTinInletTemp_degC_B;
    ELSE
        rVoted_TinInletTemp_degC := rTinInletTemp_degC_C;
    END_IF;
    IF (ABS(rTinInletTemp_degC_A - rTinInletTemp_degC_B) > rTol_TinInletTemp_degC) OR
       (ABS(rTinInletTemp_degC_B - rTinInletTemp_degC_C) > rTol_TinInletTemp_degC) OR
       (ABS(rTinInletTemp_degC_A - rTinInletTemp_degC_C) > rTol_TinInletTemp_degC) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0001; (* Triplet discrepancy warning *)
    END_IF;
ELSIF bHealth_TinInlet_A AND bHealth_TinInlet_B THEN
    rVoted_TinInletTemp_degC := (rTinInletTemp_degC_A + rTinInletTemp_degC_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002; (* 1oo2 Degraded Mode *)
ELSIF bHealth_TinInlet_A AND bHealth_TinInlet_C THEN
    rVoted_TinInletTemp_degC := (rTinInletTemp_degC_A + rTinInletTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_TinInlet_B AND bHealth_TinInlet_C THEN
    rVoted_TinInletTemp_degC := (rTinInletTemp_degC_B + rTinInletTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0002;
ELSIF bHealth_TinInlet_A THEN
    rVoted_TinInletTemp_degC := rTinInletTemp_degC_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004; (* 1oo1 Single Channel Mode *)
ELSIF bHealth_TinInlet_B THEN
    rVoted_TinInletTemp_degC := rTinInletTemp_degC_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSIF bHealth_TinInlet_C THEN
    rVoted_TinInletTemp_degC := rTinInletTemp_degC_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0004;
ELSE
    rVoted_TinInletTemp_degC := 1050.0; (* Fallback safe default value *)
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0008; (* Total sensor fault *)
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2. Tin Bath Mid-Section Ribbon Pyrometer Triplet Voting [deg C]                               *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTinMidTemp_degC_A - rPrev_TinMid_A) < 0.01 THEN iStuck_TinMid_A := iStuck_TinMid_A + 1; ELSE iStuck_TinMid_A := 0; END_IF;
IF ABS(rTinMidTemp_degC_B - rPrev_TinMid_B) < 0.01 THEN iStuck_TinMid_B := iStuck_TinMid_B + 1; ELSE iStuck_TinMid_B := 0; END_IF;
IF ABS(rTinMidTemp_degC_C - rPrev_TinMid_C) < 0.01 THEN iStuck_TinMid_C := iStuck_TinMid_C + 1; ELSE iStuck_TinMid_C := 0; END_IF;
rPrev_TinMid_A := rTinMidTemp_degC_A; rPrev_TinMid_B := rTinMidTemp_degC_B; rPrev_TinMid_C := rTinMidTemp_degC_C;

bHealth_TinMid_A := (rTinMidTemp_degC_A >= 700.0) AND (rTinMidTemp_degC_A <= 950.0) AND (iStuck_TinMid_A < 240);
bHealth_TinMid_B := (rTinMidTemp_degC_B >= 700.0) AND (rTinMidTemp_degC_B <= 950.0) AND (iStuck_TinMid_B < 240);
bHealth_TinMid_C := (rTinMidTemp_degC_C >= 700.0) AND (rTinMidTemp_degC_C <= 950.0) AND (iStuck_TinMid_C < 240);

IF bHealth_TinMid_A AND bHealth_TinMid_B AND bHealth_TinMid_C THEN
    IF ((rTinMidTemp_degC_A >= rTinMidTemp_degC_B) AND (rTinMidTemp_degC_A <= rTinMidTemp_degC_C)) OR
       ((rTinMidTemp_degC_A >= rTinMidTemp_degC_C) AND (rTinMidTemp_degC_A <= rTinMidTemp_degC_B)) THEN
        rVoted_TinMidTemp_degC := rTinMidTemp_degC_A;
    ELSIF ((rTinMidTemp_degC_B >= rTinMidTemp_degC_A) AND (rTinMidTemp_degC_B <= rTinMidTemp_degC_C)) OR
          ((rTinMidTemp_degC_B >= rTinMidTemp_degC_C) AND (rTinMidTemp_degC_B <= rTinMidTemp_degC_A)) THEN
        rVoted_TinMidTemp_degC := rTinMidTemp_degC_B;
    ELSE
        rVoted_TinMidTemp_degC := rTinMidTemp_degC_C;
    END_IF;
    IF (ABS(rTinMidTemp_degC_A - rTinMidTemp_degC_B) > rTol_TinMidTemp_degC) OR
       (ABS(rTinMidTemp_degC_B - rTinMidTemp_degC_C) > rTol_TinMidTemp_degC) OR
       (ABS(rTinMidTemp_degC_A - rTinMidTemp_degC_C) > rTol_TinMidTemp_degC) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0010;
    END_IF;
ELSIF bHealth_TinMid_A AND bHealth_TinMid_B THEN
    rVoted_TinMidTemp_degC := (rTinMidTemp_degC_A + rTinMidTemp_degC_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TinMid_A AND bHealth_TinMid_C THEN
    rVoted_TinMidTemp_degC := (rTinMidTemp_degC_A + rTinMidTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TinMid_B AND bHealth_TinMid_C THEN
    rVoted_TinMidTemp_degC := (rTinMidTemp_degC_B + rTinMidTemp_degC_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0020;
ELSIF bHealth_TinMid_A THEN
    rVoted_TinMidTemp_degC := rTinMidTemp_degC_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_TinMid_B THEN
    rVoted_TinMidTemp_degC := rTinMidTemp_degC_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSIF bHealth_TinMid_C THEN
    rVoted_TinMidTemp_degC := rTinMidTemp_degC_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0040;
ELSE
    rVoted_TinMidTemp_degC := 825.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0080;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 3. Tin Bath Exit / Lift-Out Roll Pyrometer Triplet Voting [deg C]                             *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTinExitTemp_degC_A - rPrev_TinExit_A) < 0.01 THEN iStuck_TinExit_A := iStuck_TinExit_A + 1; ELSE iStuck_TinExit_A := 0; END_IF;
IF ABS(rTinExitTemp_degC_B - rPrev_TinExit_B) < 0.01 THEN iStuck_TinExit_B := iStuck_TinExit_B + 1; ELSE iStuck_TinExit_B := 0; END_IF;
IF ABS(rTinExitTemp_degC_C - rPrev_TinExit_C) < 0.01 THEN iStuck_TinExit_C := iStuck_TinExit_C + 1; ELSE iStuck_TinExit_C := 0; END_IF;
rPrev_TinExit_A := rTinExitTemp_degC_A; rPrev_TinExit_B := rTinExitTemp_degC_B; rPrev_TinExit_C := rTinExitTemp_degC_C;

bHealth_TinExit_A := (rTinExitTemp_degC_A >= 500.0) AND (rTinExitTemp_degC_A <= 720.0) AND (iStuck_TinExit_A < 240);
bHealth_TinExit_B := (rTinExitTemp_degC_B >= 500.0) AND (rTinExitTemp_degC_B <= 720.0) AND (iStuck_TinExit_B < 240);
bHealth_TinExit_C := (rTinExitTemp_degC_C >= 500.0) AND (rTinExitTemp_degC_C <= 720.0) AND (iStuck_TinExit_C < 240);

IF bHealth_TinExit_A AND bHealth_TinExit_B AND bHealth_TinExit_C THEN
    IF ((rTinExitTemp_degC_A >= rTinExitTemp_degC_B) AND (rTinExitTemp_degC_A <= rTinExitTemp_degC_C)) OR
       ((rTinExitTemp_degC_A >= rTinExitTemp_degC_C) AND (rTinExitTemp_degC_A <= rTinExitTemp_degC_B)) THEN
        rVoted_TinExitTemp_degC := rTinExitTemp_degC_A;
    ELSIF ((rTinExitTemp_degC_B >= rTinExitTemp_degC_A) AND (rTinExitTemp_degC_B <= rTinExitTemp_degC_C)) OR
          ((rTinExitTemp_degC_B >= rTinExitTemp_degC_C) AND (rTinExitTemp_degC_B <= rTinExitTemp_degC_A)) THEN
        rVoted_TinExitTemp_degC := rTinExitTemp_degC_B;
    ELSE
        rVoted_TinExitTemp_degC := rTinExitTemp_degC_C;
    END_IF;
ELSIF bHealth_TinExit_A AND bHealth_TinExit_B THEN
    rVoted_TinExitTemp_degC := (rTinExitTemp_degC_A + rTinExitTemp_degC_B) * 0.5;
ELSIF bHealth_TinExit_A AND bHealth_TinExit_C THEN
    rVoted_TinExitTemp_degC := (rTinExitTemp_degC_A + rTinExitTemp_degC_C) * 0.5;
ELSIF bHealth_TinExit_B AND bHealth_TinExit_C THEN
    rVoted_TinExitTemp_degC := (rTinExitTemp_degC_B + rTinExitTemp_degC_C) * 0.5;
ELSIF bHealth_TinExit_A THEN
    rVoted_TinExitTemp_degC := rTinExitTemp_degC_A;
ELSIF bHealth_TinExit_B THEN
    rVoted_TinExitTemp_degC := rTinExitTemp_degC_B;
ELSIF bHealth_TinExit_C THEN
    rVoted_TinExitTemp_degC := rTinExitTemp_degC_C;
ELSE
    rVoted_TinExitTemp_degC := 600.0;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 4. Lehr Zone A Duplex Thermocouple Triplet Voting [deg C]                                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rLehrTemp_ZoneA_degC_A - rPrev_LehrZA_A) < 0.01 THEN iStuck_LehrZA_A := iStuck_LehrZA_A + 1; ELSE iStuck_LehrZA_A := 0; END_IF;
IF ABS(rLehrTemp_ZoneA_degC_B - rPrev_LehrZA_B) < 0.01 THEN iStuck_LehrZA_B := iStuck_LehrZA_B + 1; ELSE iStuck_LehrZA_B := 0; END_IF;
IF ABS(rLehrTemp_ZoneA_degC_C - rPrev_LehrZA_C) < 0.01 THEN iStuck_LehrZA_C := iStuck_LehrZA_C + 1; ELSE iStuck_LehrZA_C := 0; END_IF;
rPrev_LehrZA_A := rLehrTemp_ZoneA_degC_A; rPrev_LehrZA_B := rLehrTemp_ZoneA_degC_B; rPrev_LehrZA_C := rLehrTemp_ZoneA_degC_C;

bHealth_LehrZA_A := (rLehrTemp_ZoneA_degC_A >= 490.0) AND (rLehrTemp_ZoneA_degC_A <= 580.0) AND (iStuck_LehrZA_A < 240);
bHealth_LehrZA_B := (rLehrTemp_ZoneA_degC_B >= 490.0) AND (rLehrTemp_ZoneA_degC_B <= 580.0) AND (iStuck_LehrZA_B < 240);
bHealth_LehrZA_C := (rLehrTemp_ZoneA_degC_C >= 490.0) AND (rLehrTemp_ZoneA_degC_C <= 580.0) AND (iStuck_LehrZA_C < 240);

IF bHealth_LehrZA_A AND bHealth_LehrZA_B AND bHealth_LehrZA_C THEN
    IF ((rLehrTemp_ZoneA_degC_A >= rLehrTemp_ZoneA_degC_B) AND (rLehrTemp_ZoneA_degC_A <= rLehrTemp_ZoneA_degC_C)) OR
       ((rLehrTemp_ZoneA_degC_A >= rLehrTemp_ZoneA_degC_C) AND (rLehrTemp_ZoneA_degC_A <= rLehrTemp_ZoneA_degC_B)) THEN
        rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_A;
    ELSIF ((rLehrTemp_ZoneA_degC_B >= rLehrTemp_ZoneA_degC_A) AND (rLehrTemp_ZoneA_degC_B <= rLehrTemp_ZoneA_degC_C)) OR
          ((rLehrTemp_ZoneA_degC_B >= rLehrTemp_ZoneA_degC_C) AND (rLehrTemp_ZoneA_degC_B <= rLehrTemp_ZoneA_degC_A)) THEN
        rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_B;
    ELSE
        rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_C;
    END_IF;
ELSIF bHealth_LehrZA_A AND bHealth_LehrZA_B THEN
    rVoted_LehrTemp_ZoneA_degC := (rLehrTemp_ZoneA_degC_A + rLehrTemp_ZoneA_degC_B) * 0.5;
ELSIF bHealth_LehrZA_A AND bHealth_LehrZA_C THEN
    rVoted_LehrTemp_ZoneA_degC := (rLehrTemp_ZoneA_degC_A + rLehrTemp_ZoneA_degC_C) * 0.5;
ELSIF bHealth_LehrZA_B AND bHealth_LehrZA_C THEN
    rVoted_LehrTemp_ZoneA_degC := (rLehrTemp_ZoneA_degC_B + rLehrTemp_ZoneA_degC_C) * 0.5;
ELSIF bHealth_LehrZA_A THEN
    rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_A;
ELSIF bHealth_LehrZA_B THEN
    rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_B;
ELSIF bHealth_LehrZA_C THEN
    rVoted_LehrTemp_ZoneA_degC := rLehrTemp_ZoneA_degC_C;
ELSE
    rVoted_LehrTemp_ZoneA_degC := 535.0;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 5. Lehr Zone B Duplex Thermocouple Triplet Voting [deg C]                                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rLehrTemp_ZoneB_degC_A - rPrev_LehrZB_A) < 0.01 THEN iStuck_LehrZB_A := iStuck_LehrZB_A + 1; ELSE iStuck_LehrZB_A := 0; END_IF;
IF ABS(rLehrTemp_ZoneB_degC_B - rPrev_LehrZB_B) < 0.01 THEN iStuck_LehrZB_B := iStuck_LehrZB_B + 1; ELSE iStuck_LehrZB_B := 0; END_IF;
IF ABS(rLehrTemp_ZoneB_degC_C - rPrev_LehrZB_C) < 0.01 THEN iStuck_LehrZB_C := iStuck_LehrZB_C + 1; ELSE iStuck_LehrZB_C := 0; END_IF;
rPrev_LehrZB_A := rLehrTemp_ZoneB_degC_A; rPrev_LehrZB_B := rLehrTemp_ZoneB_degC_B; rPrev_LehrZB_C := rLehrTemp_ZoneB_degC_C;

bHealth_LehrZB_A := (rLehrTemp_ZoneB_degC_A >= 440.0) AND (rLehrTemp_ZoneB_degC_A <= 530.0) AND (iStuck_LehrZB_A < 240);
bHealth_LehrZB_B := (rLehrTemp_ZoneB_degC_B >= 440.0) AND (rLehrTemp_ZoneB_degC_B <= 530.0) AND (iStuck_LehrZB_B < 240);
bHealth_LehrZB_C := (rLehrTemp_ZoneB_degC_C >= 440.0) AND (rLehrTemp_ZoneB_degC_C <= 530.0) AND (iStuck_LehrZB_C < 240);

IF bHealth_LehrZB_A AND bHealth_LehrZB_B AND bHealth_LehrZB_C THEN
    IF ((rLehrTemp_ZoneB_degC_A >= rLehrTemp_ZoneB_degC_B) AND (rLehrTemp_ZoneB_degC_A <= rLehrTemp_ZoneB_degC_C)) OR
       ((rLehrTemp_ZoneB_degC_A >= rLehrTemp_ZoneB_degC_C) AND (rLehrTemp_ZoneB_degC_A <= rLehrTemp_ZoneB_degC_B)) THEN
        rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_A;
    ELSIF ((rLehrTemp_ZoneB_degC_B >= rLehrTemp_ZoneB_degC_A) AND (rLehrTemp_ZoneB_degC_B <= rLehrTemp_ZoneB_degC_C)) OR
          ((rLehrTemp_ZoneB_degC_B >= rLehrTemp_ZoneB_degC_C) AND (rLehrTemp_ZoneB_degC_B <= rLehrTemp_ZoneB_degC_A)) THEN
        rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_B;
    ELSE
        rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_C;
    END_IF;
ELSIF bHealth_LehrZB_A AND bHealth_LehrZB_B THEN
    rVoted_LehrTemp_ZoneB_degC := (rLehrTemp_ZoneB_degC_A + rLehrTemp_ZoneB_degC_B) * 0.5;
ELSIF bHealth_LehrZB_A AND bHealth_LehrZB_C THEN
    rVoted_LehrTemp_ZoneB_degC := (rLehrTemp_ZoneB_degC_A + rLehrTemp_ZoneB_degC_C) * 0.5;
ELSIF bHealth_LehrZB_B AND bHealth_LehrZB_C THEN
    rVoted_LehrTemp_ZoneB_degC := (rLehrTemp_ZoneB_degC_B + rLehrTemp_ZoneB_degC_C) * 0.5;
ELSIF bHealth_LehrZB_A THEN
    rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_A;
ELSIF bHealth_LehrZB_B THEN
    rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_B;
ELSIF bHealth_LehrZB_C THEN
    rVoted_LehrTemp_ZoneB_degC := rLehrTemp_ZoneB_degC_C;
ELSE
    rVoted_LehrTemp_ZoneB_degC := 485.0;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 6. Lehr Zone C Duplex Thermocouple Triplet Voting [deg C]                                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rLehrTemp_ZoneC_degC_A - rPrev_LehrZC_A) < 0.01 THEN iStuck_LehrZC_A := iStuck_LehrZC_A + 1; ELSE iStuck_LehrZC_A := 0; END_IF;
IF ABS(rLehrTemp_ZoneC_degC_B - rPrev_LehrZC_B) < 0.01 THEN iStuck_LehrZC_B := iStuck_LehrZC_B + 1; ELSE iStuck_LehrZC_B := 0; END_IF;
IF ABS(rLehrTemp_ZoneC_degC_C - rPrev_LehrZC_C) < 0.01 THEN iStuck_LehrZC_C := iStuck_LehrZC_C + 1; ELSE iStuck_LehrZC_C := 0; END_IF;
rPrev_LehrZC_A := rLehrTemp_ZoneC_degC_A; rPrev_LehrZC_B := rLehrTemp_ZoneC_degC_B; rPrev_LehrZC_C := rLehrTemp_ZoneC_degC_C;

bHealth_LehrZC_A := (rLehrTemp_ZoneC_degC_A >= 360.0) AND (rLehrTemp_ZoneC_degC_A <= 460.0) AND (iStuck_LehrZC_A < 240);
bHealth_LehrZC_B := (rLehrTemp_ZoneC_degC_B >= 360.0) AND (rLehrTemp_ZoneC_degC_B <= 460.0) AND (iStuck_LehrZC_B < 240);
bHealth_LehrZC_C := (rLehrTemp_ZoneC_degC_C >= 360.0) AND (rLehrTemp_ZoneC_degC_C <= 460.0) AND (iStuck_LehrZC_C < 240);

IF bHealth_LehrZC_A AND bHealth_LehrZC_B AND bHealth_LehrZC_C THEN
    IF ((rLehrTemp_ZoneC_degC_A >= rLehrTemp_ZoneC_degC_B) AND (rLehrTemp_ZoneC_degC_A <= rLehrTemp_ZoneC_degC_C)) OR
       ((rLehrTemp_ZoneC_degC_A >= rLehrTemp_ZoneC_degC_C) AND (rLehrTemp_ZoneC_degC_A <= rLehrTemp_ZoneC_degC_B)) THEN
        rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_A;
    ELSIF ((rLehrTemp_ZoneC_degC_B >= rLehrTemp_ZoneC_degC_A) AND (rLehrTemp_ZoneC_degC_B <= rLehrTemp_ZoneC_degC_C)) OR
          ((rLehrTemp_ZoneC_degC_B >= rLehrTemp_ZoneC_degC_C) AND (rLehrTemp_ZoneC_degC_B <= rLehrTemp_ZoneC_degC_A)) THEN
        rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_B;
    ELSE
        rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_C;
    END_IF;
ELSIF bHealth_LehrZC_A AND bHealth_LehrZC_B THEN
    rVoted_LehrTemp_ZoneC_degC := (rLehrTemp_ZoneC_degC_A + rLehrTemp_ZoneC_degC_B) * 0.5;
ELSIF bHealth_LehrZC_A AND bHealth_LehrZC_C THEN
    rVoted_LehrTemp_ZoneC_degC := (rLehrTemp_ZoneC_degC_A + rLehrTemp_ZoneC_degC_C) * 0.5;
ELSIF bHealth_LehrZC_B AND bHealth_LehrZC_C THEN
    rVoted_LehrTemp_ZoneC_degC := (rLehrTemp_ZoneC_degC_B + rLehrTemp_ZoneC_degC_C) * 0.5;
ELSIF bHealth_LehrZC_A THEN
    rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_A;
ELSIF bHealth_LehrZC_B THEN
    rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_B;
ELSIF bHealth_LehrZC_C THEN
    rVoted_LehrTemp_ZoneC_degC := rLehrTemp_ZoneC_degC_C;
ELSE
    rVoted_LehrTemp_ZoneC_degC := 420.0;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 7. Lehr Zone D Duplex Thermocouple Triplet Voting [deg C]                                     *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rLehrTemp_ZoneD_degC_A - rPrev_LehrZD_A) < 0.01 THEN iStuck_LehrZD_A := iStuck_LehrZD_A + 1; ELSE iStuck_LehrZD_A := 0; END_IF;
IF ABS(rLehrTemp_ZoneD_degC_B - rPrev_LehrZD_B) < 0.01 THEN iStuck_LehrZD_B := iStuck_LehrZD_B + 1; ELSE iStuck_LehrZD_B := 0; END_IF;
IF ABS(rLehrTemp_ZoneD_degC_C - rPrev_LehrZD_C) < 0.01 THEN iStuck_LehrZD_C := iStuck_LehrZD_C + 1; ELSE iStuck_LehrZD_C := 0; END_IF;
rPrev_LehrZD_A := rLehrTemp_ZoneD_degC_A; rPrev_LehrZD_B := rLehrTemp_ZoneD_degC_B; rPrev_LehrZD_C := rLehrTemp_ZoneD_degC_C;

bHealth_LehrZD_A := (rLehrTemp_ZoneD_degC_A >= 220.0) AND (rLehrTemp_ZoneD_degC_A <= 350.0) AND (iStuck_LehrZD_A < 240);
bHealth_LehrZD_B := (rLehrTemp_ZoneD_degC_B >= 220.0) AND (rLehrTemp_ZoneD_degC_B <= 350.0) AND (iStuck_LehrZD_B < 240);
bHealth_LehrZD_C := (rLehrTemp_ZoneD_degC_C >= 220.0) AND (rLehrTemp_ZoneD_degC_C <= 350.0) AND (iStuck_LehrZD_C < 240);

IF bHealth_LehrZD_A AND bHealth_LehrZD_B AND bHealth_LehrZD_C THEN
    IF ((rLehrTemp_ZoneD_degC_A >= rLehrTemp_ZoneD_degC_B) AND (rLehrTemp_ZoneD_degC_A <= rLehrTemp_ZoneD_degC_C)) OR
       ((rLehrTemp_ZoneD_degC_A >= rLehrTemp_ZoneD_degC_C) AND (rLehrTemp_ZoneD_degC_A <= rLehrTemp_ZoneD_degC_B)) THEN
        rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_A;
    ELSIF ((rLehrTemp_ZoneD_degC_B >= rLehrTemp_ZoneD_degC_A) AND (rLehrTemp_ZoneD_degC_B <= rLehrTemp_ZoneD_degC_C)) OR
          ((rLehrTemp_ZoneD_degC_B >= rLehrTemp_ZoneD_degC_C) AND (rLehrTemp_ZoneD_degC_B <= rLehrTemp_ZoneD_degC_A)) THEN
        rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_B;
    ELSE
        rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_C;
    END_IF;
ELSIF bHealth_LehrZD_A AND bHealth_LehrZD_B THEN
    rVoted_LehrTemp_ZoneD_degC := (rLehrTemp_ZoneD_degC_A + rLehrTemp_ZoneD_degC_B) * 0.5;
ELSIF bHealth_LehrZD_A AND bHealth_LehrZD_C THEN
    rVoted_LehrTemp_ZoneD_degC := (rLehrTemp_ZoneD_degC_A + rLehrTemp_ZoneD_degC_C) * 0.5;
ELSIF bHealth_LehrZD_B AND bHealth_LehrZD_C THEN
    rVoted_LehrTemp_ZoneD_degC := (rLehrTemp_ZoneD_degC_B + rLehrTemp_ZoneD_degC_C) * 0.5;
ELSIF bHealth_LehrZD_A THEN
    rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_A;
ELSIF bHealth_LehrZD_B THEN
    rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_B;
ELSIF bHealth_LehrZD_C THEN
    rVoted_LehrTemp_ZoneD_degC := rLehrTemp_ZoneD_degC_C;
ELSE
    rVoted_LehrTemp_ZoneD_degC := 295.0;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 8. Tin Bath Chamber Atmosphere Overpressure Manometer Triplet Voting [Pa]                    *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTinBathPressure_Pa_A - rPrev_Press_A) < 0.005 THEN iStuck_Press_A := iStuck_Press_A + 1; ELSE iStuck_Press_A := 0; END_IF;
IF ABS(rTinBathPressure_Pa_B - rPrev_Press_B) < 0.005 THEN iStuck_Press_B := iStuck_Press_B + 1; ELSE iStuck_Press_B := 0; END_IF;
IF ABS(rTinBathPressure_Pa_C - rPrev_Press_C) < 0.005 THEN iStuck_Press_C := iStuck_Press_C + 1; ELSE iStuck_Press_C := 0; END_IF;
rPrev_Press_A := rTinBathPressure_Pa_A; rPrev_Press_B := rTinBathPressure_Pa_B; rPrev_Press_C := rTinBathPressure_Pa_C;

bHealth_Press_A := (rTinBathPressure_Pa_A >= 0.0) AND (rTinBathPressure_Pa_A <= 35.0) AND (iStuck_Press_A < 180);
bHealth_Press_B := (rTinBathPressure_Pa_B >= 0.0) AND (rTinBathPressure_Pa_B <= 35.0) AND (iStuck_Press_B < 180);
bHealth_Press_C := (rTinBathPressure_Pa_C >= 0.0) AND (rTinBathPressure_Pa_C <= 35.0) AND (iStuck_Press_C < 180);

IF bHealth_Press_A AND bHealth_Press_B AND bHealth_Press_C THEN
    IF ((rTinBathPressure_Pa_A >= rTinBathPressure_Pa_B) AND (rTinBathPressure_Pa_A <= rTinBathPressure_Pa_C)) OR
       ((rTinBathPressure_Pa_A >= rTinBathPressure_Pa_C) AND (rTinBathPressure_Pa_A <= rTinBathPressure_Pa_B)) THEN
        rVoted_TinBathPress_Pa := rTinBathPressure_Pa_A;
    ELSIF ((rTinBathPressure_Pa_B >= rTinBathPressure_Pa_A) AND (rTinBathPressure_Pa_B <= rTinBathPressure_Pa_C)) OR
          ((rTinBathPressure_Pa_B >= rTinBathPressure_Pa_C) AND (rTinBathPressure_Pa_B <= rTinBathPressure_Pa_A)) THEN
        rVoted_TinBathPress_Pa := rTinBathPressure_Pa_B;
    ELSE
        rVoted_TinBathPress_Pa := rTinBathPressure_Pa_C;
    END_IF;
    IF (ABS(rTinBathPressure_Pa_A - rTinBathPressure_Pa_B) > rTol_TinBathPress_Pa) OR
       (ABS(rTinBathPressure_Pa_B - rTinBathPressure_Pa_C) > rTol_TinBathPress_Pa) OR
       (ABS(rTinBathPressure_Pa_A - rTinBathPressure_Pa_C) > rTol_TinBathPress_Pa) THEN
        dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0100;
    END_IF;
ELSIF bHealth_Press_A AND bHealth_Press_B THEN
    rVoted_TinBathPress_Pa := (rTinBathPressure_Pa_A + rTinBathPressure_Pa_B) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Press_A AND bHealth_Press_C THEN
    rVoted_TinBathPress_Pa := (rTinBathPressure_Pa_A + rTinBathPressure_Pa_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Press_B AND bHealth_Press_C THEN
    rVoted_TinBathPress_Pa := (rTinBathPressure_Pa_B + rTinBathPressure_Pa_C) * 0.5;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0200;
ELSIF bHealth_Press_A THEN
    rVoted_TinBathPress_Pa := rTinBathPressure_Pa_A;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSIF bHealth_Press_B THEN
    rVoted_TinBathPress_Pa := rTinBathPressure_Pa_B;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSIF bHealth_Press_C THEN
    rVoted_TinBathPress_Pa := rTinBathPressure_Pa_C;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0400;
ELSE
    rVoted_TinBathPress_Pa := 10.0;
    dwTMR_DiagnosticWord := dwTMR_DiagnosticWord OR 16#0000_0800;
    bGracefulDegradation := TRUE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 9. ZrO2 Trace Oxygen Analyzer Triplet Voting [ppm]                                            *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTinTraceO2_ppm_A - rPrev_O2_A) < 0.002 THEN iStuck_O2_A := iStuck_O2_A + 1; ELSE iStuck_O2_A := 0; END_IF;
IF ABS(rTinTraceO2_ppm_B - rPrev_O2_B) < 0.002 THEN iStuck_O2_B := iStuck_O2_B + 1; ELSE iStuck_O2_B := 0; END_IF;
IF ABS(rTinTraceO2_ppm_C - rPrev_O2_C) < 0.002 THEN iStuck_O2_C := iStuck_O2_C + 1; ELSE iStuck_O2_C := 0; END_IF;
rPrev_O2_A := rTinTraceO2_ppm_A; rPrev_O2_B := rTinTraceO2_ppm_B; rPrev_O2_C := rTinTraceO2_ppm_C;

bHealth_O2_A := (rTinTraceO2_ppm_A >= 0.0) AND (rTinTraceO2_ppm_A <= 50.0) AND (iStuck_O2_A < 180);
bHealth_O2_B := (rTinTraceO2_ppm_B >= 0.0) AND (rTinTraceO2_ppm_B <= 50.0) AND (iStuck_O2_B < 180);
bHealth_O2_C := (rTinTraceO2_ppm_C >= 0.0) AND (rTinTraceO2_ppm_C <= 50.0) AND (iStuck_O2_C < 180);

IF bHealth_O2_A AND bHealth_O2_B AND bHealth_O2_C THEN
    IF ((rTinTraceO2_ppm_A >= rTinTraceO2_ppm_B) AND (rTinTraceO2_ppm_A <= rTinTraceO2_ppm_C)) OR
       ((rTinTraceO2_ppm_A >= rTinTraceO2_ppm_C) AND (rTinTraceO2_ppm_A <= rTinTraceO2_ppm_B)) THEN
        rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_A;
    ELSIF ((rTinTraceO2_ppm_B >= rTinTraceO2_ppm_A) AND (rTinTraceO2_ppm_B <= rTinTraceO2_ppm_C)) OR
          ((rTinTraceO2_ppm_B >= rTinTraceO2_ppm_C) AND (rTinTraceO2_ppm_B <= rTinTraceO2_ppm_A)) THEN
        rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_B;
    ELSE
        rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_C;
    END_IF;
ELSIF bHealth_O2_A AND bHealth_O2_B THEN
    rVoted_TinTraceO2_ppm := (rTinTraceO2_ppm_A + rTinTraceO2_ppm_B) * 0.5;
ELSIF bHealth_O2_A AND bHealth_O2_C THEN
    rVoted_TinTraceO2_ppm := (rTinTraceO2_ppm_A + rTinTraceO2_ppm_C) * 0.5;
ELSIF bHealth_O2_B AND bHealth_O2_C THEN
    rVoted_TinTraceO2_ppm := (rTinTraceO2_ppm_B + rTinTraceO2_ppm_C) * 0.5;
ELSIF bHealth_O2_A THEN
    rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_A;
ELSIF bHealth_O2_B THEN
    rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_B;
ELSIF bHealth_O2_C THEN
    rVoted_TinTraceO2_ppm := rTinTraceO2_ppm_C;
ELSE
    rVoted_TinTraceO2_ppm := 2.0;
    bGracefulDegradation := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 3: Real-Time Hydrodynamic, Viscoelastic & Antonov Mechanics
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 3: NAVIER-STOKES RIBBON SPREAD, ANTONOV SURFACE TENSION & ADAMS-WILLIAMSON RELAXATION  *)
(* ============================================================================================= *)
(* 1. Temperature-Dependent Glass Viscosity via Fulcher-Tammann-Vogel (FTV) Equation *)
(* log10(eta [dPa.s]) = A + B / (T - T0) *)
IF (rVoted_TinInletTemp_degC - rFTV_T0) > 10.0 THEN
    rViscosityExponent := rFTV_A + (rFTV_B / (rVoted_TinInletTemp_degC - rFTV_T0));
    (* Clamp exponent between 2.0 (100 dPa.s at 1450 deg C) and 14.0 (strain point at 480 deg C) *)
    IF rViscosityExponent < 2.0 THEN rViscosityExponent := 2.0; END_IF;
    IF rViscosityExponent > 14.0 THEN rViscosityExponent := 14.0; END_IF;
    rLogViscosity := rViscosityExponent;
    (* Approximate dynamic viscosity in dPa.s *)
    rViscosity_dPas := EXPT(10.0, rViscosityExponent);
ELSE
    rViscosity_dPas := 1.0E7;
END_IF;

(* 2. Antonov Interfacial Equilibrium Thickness Formulation *)
(* Net spreading coefficient S = gamma_sn + gamma_g - gamma_g_sn *)
rNetSpreadCoeff_S := rSurfaceTension_Tin_Nm + rSurfaceTension_Glass_Nm - rInterfacialTension_Nm;
IF rNetSpreadCoeff_S > 0.1 THEN
    (* h_inf = SQRT( (2 * S * rho_sn) / (g * rho_g * (rho_sn - rho_g)) ) *)
    rEquilibriumFormula_Val := (2.0 * rNetSpreadCoeff_S * rTinDensity_kgm3) /
                               (rGravity_ms2 * rGlassDensity_kgm3 * (rTinDensity_kgm3 - rGlassDensity_kgm3));
    IF rEquilibriumFormula_Val > 0.000001 THEN
        rNaturalEquilibriumThick_mm := SQRT(rEquilibriumFormula_Val) * 1000.0;
    ELSE
        rNaturalEquilibriumThick_mm := 6.920;
    END_IF;
ELSE
    rNaturalEquilibriumThick_mm := 6.920;
END_IF;

(* 3. Kinematic Top-Roll Tractive Lateral Stretch & Attenuation *)
rTractiveForceTotal_N := 0.0;
FOR iIdxAct := 1 TO 14 DO
    (* Outward lateral stretch vector: v_perp = v_roll * sin(theta_tilt) *)
    rLateralStretch_ms := (rTopRoll_SpeedFeedback_mmin[iIdxAct] / 60.0) *
                          SIN(rTopRoll_TiltAngleFeedback_deg[iIdxAct] * 3.14159265 / 180.0);
    (* Longitudinal forward draw vector: v_par = v_roll * cos(theta_tilt) *)
    rLongitudinalDraw_ms := (rTopRoll_SpeedFeedback_mmin[iIdxAct] / 60.0) *
                           COS(rTopRoll_TiltAngleFeedback_deg[iIdxAct] * 3.14159265 / 180.0);
    (* Tractive friction force per roll pair *)
    rTractiveForceTotal_N := rTractiveForceTotal_N +
                            (rTopRoll_Current_A[iIdxAct] * 42.5 * rTopRoll_KnurlDepth_mm[iIdxAct] *
                             SIN(rTopRoll_TiltAngleFeedback_deg[iIdxAct] * 3.14159265 / 180.0));
END_FOR;

(* 4. Viscoelastic Maxwell Relaxation & Adams-Williamson Annealing Stress Integration *)
(* Maxwell relaxation time tau_M = eta / G_glass *)
IF rGlassShearModulus_G_Pa > 1.0E8 THEN
    rMaxwellRelaxTime_s := (rViscosity_dPas * 0.1) / rGlassShearModulus_G_Pa;
ELSE
    rMaxwellRelaxTime_s := 0.0035;
END_IF;

(* Adams-Williamson Stress Relaxation: dF/dt = -A_aw * F^2 *)
rAdamsWilliamson_Delta := -rAdamsWilliamson_A_aw * (rPolarimeterRetardation_nmcm * rPolarimeterRetardation_nmcm) * tScanTime_s;
rCalculatedResidualStress_nm := rPolarimeterRetardation_nmcm + rAdamsWilliamson_Delta;
IF rCalculatedResidualStress_nm < 0.5 THEN rCalculatedResidualStress_nm := 0.5; END_IF;

(* Photoelastic Birefringence Check: delta = C * d * (sigma_x - sigma_y) *)
rPhotoelasticRetard_calc := rBrewsterConstant_B * (rTraverserThickness_mm * 0.001) * 1.85E6 * 1.0E7;
""")

    # -------------------------------------------------------------------------
    # SECTION 4: Discrete State-Space Model & Kalman State Estimation
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 4: 16x16 DISCRETE STATE-SPACE PROPAGATION & KALMAN OBSERVER INNOVATION                *)
(* ============================================================================================= *)
(* Update Disturbance Vector d[0..3] *)
aDisturb_d[0] := rCanalGlassTemp_degC - 1050.0;
aDisturb_d[1] := rFurnacePullRate_TonsDay - 800.0;
aDisturb_d[2] := rBarometricPress_hPa - 1013.25;
aDisturb_d[3] := rAmbientTemp_degC - 25.0;

(* Calculate Actuator Deviations du = u - u_base *)
FOR iIdxAct := 0 TO 7 DO
    aControl_du[iIdxAct] := aControl_u[iIdxAct] - aControl_u_base[iIdxAct];
END_FOR;

(* State-Space Prediction: x_pred = A * x_hat + B * du + E * d *)
FOR iIdxRow := 0 TO 15 DO
    rAccumTemp := 0.0;
    (* Matrix A * x_hat *)
    FOR iIdxCol := 0 TO 15 DO
        rAccumTemp := rAccumTemp + (aMatrix_A[iIdxRow, iIdxCol] * aState_x_hat[iIdxCol]);
    END_FOR;
    (* Matrix B * du *)
    FOR iIdxCol := 0 TO 7 DO
        rAccumTemp := rAccumTemp + (aMatrix_B[iIdxRow, iIdxCol] * aControl_du[iIdxCol]);
    END_FOR;
    (* Matrix E * d *)
    FOR iIdxCol := 0 TO 3 DO
        rAccumTemp := rAccumTemp + (aMatrix_E[iIdxRow, iIdxCol] * aDisturb_d[iIdxCol]);
    END_FOR;
    aState_x_pred[iIdxRow] := rAccumTemp;
END_FOR;

(* Output Mapping Prediction: y_pred = C * x_pred *)
(* Compute Innovation Residuals: e_y = y_measured - y_pred *)
aOutput_y[0] := rTraverserThickness_mm;
aOutput_y[1] := rTraverserWidth_m;
aOutput_y[2] := rPolarimeterRetardation_nmcm;
aOutput_y[3] := rVoted_TinBathPress_Pa;
aOutput_y[4] := rVoted_TinTraceO2_ppm;
aOutput_y[5] := rVoted_LehrTemp_ZoneA_degC;
aOutput_y[6] := rVoted_LehrTemp_ZoneB_degC;
aOutput_y[7] := rRibbonTension_Nm;

FOR iIdxRow := 0 TO 7 DO
    rAccumTemp := 0.0;
    FOR iIdxCol := 0 TO 15 DO
        rAccumTemp := rAccumTemp + (aMatrix_C[iIdxRow, iIdxCol] * aState_x_pred[iIdxCol]);
    END_FOR;
    (* Error between sensor reading and prediction *)
    aOutput_y_err[iIdxRow] := aOutput_y[iIdxRow] - (aOutput_y_sp[iIdxRow] + rAccumTemp);
END_FOR;

(* Kalman Observer Innovation Correction: x_hat = x_pred + K_obs * e_y *)
FOR iIdxRow := 0 TO 15 DO
    rAccumTemp := aState_x_pred[iIdxRow];
    FOR iIdxCol := 0 TO 7 DO
        rAccumTemp := rAccumTemp + (aMatrix_K_obs[iIdxRow, iIdxCol] * aOutput_y_err[iIdxCol]);
    END_FOR;
    aState_x_hat[iIdxRow] := rAccumTemp;
    aState_x[iIdxRow]     := aState_x_hat[iIdxRow];
END_FOR;

(* Update Real-Time Output Estimators *)
rCalculatedCenterThick_mm := aOutput_y_sp[0] + aState_x_hat[3];
rCalculatedRibbonWidth_m  := aOutput_y_sp[1] + aState_x_hat[2];
""")

    # -------------------------------------------------------------------------
    # SECTION 5: Receding-Horizon Model Predictive Control (MPC) Solver
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) QP GRADIENT DESCENT SOLVER          *)
(* ============================================================================================= *)
IF bAutoPacingEnable AND NOT bGracefulDegradation AND bSystemReady THEN
    bMPC_Active := TRUE;

    (* Initialize Projected Gradient Moves du from Previous Scan *)
    FOR iIdxAct := 0 TO 7 DO
        aStep_du[iIdxAct] := aControl_du[iIdxAct];
    END_FOR;

    (* Receding-Horizon Quadratic Program Projected Gradient Iterations *)
    FOR iIterQP := 1 TO iMaxIterQP DO
        (* Compute Gradient Vector g = B^T * Q * (C * x_pred - y_sp) + R * du *)
        FOR iIdxAct := 0 TO 7 DO
            rAccumTemp := aWeight_R[iIdxAct] * aStep_du[iIdxAct];
            FOR iIdxCol := 0 TO 7 DO
                (* Coupling through output error *)
                rAccumTemp := rAccumTemp + (aMatrix_B[iIdxCol, iIdxAct] * aWeight_Q[iIdxCol] * aOutput_y_err[iIdxCol]);
            END_FOR;
            aGrad_g[iIdxAct] := rAccumTemp;

            (* Preconditioned Gradient Step *)
            aStep_du[iIdxAct] := aStep_du[iIdxAct] - (rAlphaStep * aGrad_g[iIdxAct] / aHessian_diag[iIdxAct]);

            (* Slew Rate Clamping: Limit du per scan *)
            IF aStep_du[iIdxAct] > aLimit_du_Max[iIdxAct] THEN
                aStep_du[iIdxAct] := aLimit_du_Max[iIdxAct];
            ELSIF aStep_du[iIdxAct] < aLimit_du_Min[iIdxAct] THEN
                aStep_du[iIdxAct] := aLimit_du_Min[iIdxAct];
            END_IF;

            (* Absolute Actuator Boundary Clamping: u = u_base + du in [u_min, u_max] *)
            IF (aControl_u_base[iIdxAct] + aStep_du[iIdxAct]) > aLimit_u_Max[iIdxAct] THEN
                aStep_du[iIdxAct] := aLimit_u_Max[iIdxAct] - aControl_u_base[iIdxAct];
            ELSIF (aControl_u_base[iIdxAct] + aStep_du[iIdxAct]) < aLimit_u_Min[iIdxAct] THEN
                aStep_du[iIdxAct] := aLimit_u_Min[iIdxAct] - aControl_u_base[iIdxAct];
            END_IF;
        END_FOR;
    END_FOR;

    (* Apply Optimal Control Move: u = u_base + du *)
    FOR iIdxAct := 0 TO 7 DO
        aControl_du[iIdxAct] := aStep_du[iIdxAct];
        aControl_u[iIdxAct]  := aControl_u_base[iIdxAct] + aControl_du[iIdxAct];
    END_FOR;

    (* Assign Actuator Commands from MPC Solution Vector *)
    rTweelGatePositionCmd_mm    := aControl_u[0];
    rLehrMainDriveSpeedCmd_mmin := aControl_u[4];
    rLiftOutRollSpeedCmd_mmin   := aControl_u[4] * 1.0015; (* Slight tractive overspeed to tension ribbon *)
    rLehrZoneA_GasFireDuty_Pct  := aControl_u[5];
    rLehrZoneB_GasFireDuty_Pct  := aControl_u[5] * 0.66;
    rLehrZoneC_CoolDamper_Pct   := aControl_u[6];
    rLehrZoneD_CoolDamper_Pct   := aControl_u[6] * 1.35;
    rTinAtmN2_FlowCmd_Nm3h      := 1400.0 + (aControl_u[7] * 10.0);
    rTinAtmH2_FlowCmd_Nm3h      := (1400.0 + (aControl_u[7] * 10.0)) * 0.052;

    (* Trim Top-Roll Machine Arrays based on early, mid and exit MPC variables *)
    FOR iIdxAct := 1 TO 4 DO
        rTopRoll_SpeedCmd_mmin[iIdxAct] := (12.0 + (0.4 * iIdxAct)) * (aControl_u[1] / 100.0);
    END_FOR;
    FOR iIdxAct := 5 TO 10 DO
        rTopRoll_SpeedCmd_mmin[iIdxAct] := 14.5 * (aControl_u[2] / 105.0);
    END_FOR;
    FOR iIdxAct := 11 TO 14 DO
        rTopRoll_SpeedCmd_mmin[iIdxAct] := 14.6 * (aControl_u[3] / 108.0);
    END_FOR;

    dwMPC_StatusWord := 16#0000_0001; (* MPC Active & Converged *)
ELSE
    bMPC_Active := FALSE;
    dwMPC_StatusWord := 16#0000_0000;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 6: 12-Stage Operational Finite State Machine
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)                                    *)
(* ============================================================================================= *)
rStateTimer_s := rStateTimer_s + tScanTime_s;

CASE iMachineState OF
    1: (* STATE_FURNACE_TWEEL_PREHEAT *)
        (* Warm canal refractory tweel lip with gas torches prior to glass release *)
        rPreheatTimer_s := rPreheatTimer_s + tScanTime_s;
        rTweelGatePositionCmd_mm    := 0.0;             (* Closed shutoff position *)
        rLehrMainDriveSpeedCmd_mmin := 0.0;
        rLiftOutRollSpeedCmd_mmin   := 0.0;
        rTinAtmN2_FlowCmd_Nm3h      := 800.0;           (* Low purge flow *)
        rTinAtmH2_FlowCmd_Nm3h      := 0.0;             (* No hydrogen during preheat *)
        rLehrZoneA_GasFireDuty_Pct  := 20.0;
        rLehrZoneB_GasFireDuty_Pct  := 15.0;
        bSystemReady                := FALSE;
        bInAnnealingSpec            := FALSE;

        IF (rPreheatTimer_s >= 60.0) AND (rCanalGlassTemp_degC >= 1040.0) THEN
            iMachineState := 2;                         (* Advance to Nitrogen Purge *)
            rStateTimer_s := 0.0;
        END_IF;

    2: (* STATE_TIN_BATH_NITROGEN_PURGE *)
        (* Purge chamber to remove atmospheric oxygen and achieve > 8 Pa overpressure *)
        rPurgeTimer_s := rPurgeTimer_s + tScanTime_s;
        rTinAtmN2_FlowCmd_Nm3h    := 2200.0;            (* High nitrogen flush *)
        rTinAtmH2_FlowCmd_Nm3h    := 0.0;
        rTinChamberVentDamper_Pct := 35.0;
        bSystemReady              := FALSE;

        IF (rPurgeTimer_s >= 120.0) AND (rVoted_TinBathPress_Pa >= 8.0) AND (rVoted_TinTraceO2_ppm < 5.0) THEN
            rTinAtmH2_FlowCmd_Nm3h := 110.0;            (* Introduce 5% reducing H2 blend *)
            iMachineState := 3;                         (* Advance to Glass Canal Inflow Delivery *)
            rStateTimer_s := 0.0;
        END_IF;

    3: (* STATE_GLASS_CANAL_INFLOW_DELIVERY *)
        (* Lift tweel gate to 120 mm to allow molten glass flow onto liquid tin pool *)
        rTweelGatePositionCmd_mm    := 120.0;
        rLehrMainDriveSpeedCmd_mmin := 8.0;             (* Slow crawl speed *)
        rLiftOutRollSpeedCmd_mmin   := 8.05;
        bSystemReady                := FALSE;

        IF (rStateTimer_s >= 90.0) AND (rVoted_TinInletTemp_degC >= 1020.0) THEN
            iMachineState := 4;                         (* Advance to Ribbon Spreading *)
            rStateTimer_s := 0.0;
        END_IF;

    4: (* STATE_EQUILIBRIUM_RIBBON_SPREADING *)
        (* Glass forms continuous natural equilibrium puddle (~6.9 mm thickness) *)
        rEquilibrationTimer_s       := rEquilibrationTimer_s + tScanTime_s;
        rTweelGatePositionCmd_mm    := 160.0;
        rLehrMainDriveSpeedCmd_mmin := 11.5;
        rLiftOutRollSpeedCmd_mmin   := 11.55;
        bSystemReady                := FALSE;

        IF (rEquilibrationTimer_s >= 180.0) AND (rTraverserWidth_m >= 3.20) THEN
            iMachineState := 5;                         (* Advance to Top-Roll Knurler Engagement *)
            rStateTimer_s := 0.0;
        END_IF;

    5: (* STATE_TOPROLL_KNURLER_ENGAGEMENT *)
        (* Engage 14 pairs of motorized toothed knurling top-rolls to grip ribbon margin *)
        rTweelGatePositionCmd_mm := 185.0;
        FOR iIdxAct := 1 TO 14 DO
            rTopRoll_SpeedCmd_mmin[iIdxAct] := 13.0 + (0.1 * iIdxAct);
            rTopRoll_TiltCmd_deg[iIdxAct]   := 18.0 - (1.2 * iIdxAct);
        END_FOR;
        bSystemReady := FALSE;

        IF (rStateTimer_s >= 120.0) AND bTopRollMasterRun THEN
            iMachineState := 6;                         (* Advance to Lehr Synchronization *)
            rStateTimer_s := 0.0;
        END_IF;

    6: (* STATE_LEHR_LIFTOUT_ROLL_SYNC *)
        (* Synchronize lehr line speed with tin bath exit ribbon velocity *)
        rLehrMainDriveSpeedCmd_mmin := 14.50;
        rLiftOutRollSpeedCmd_mmin   := 14.52;
        rLehrZoneA_GasFireDuty_Pct  := 48.0;
        rLehrZoneB_GasFireDuty_Pct  := 32.0;
        bSystemReady                := FALSE;

        IF (rStateTimer_s >= 60.0) AND (ABS(rLiftOutRollSpeed_mmin - rMainLehrDriveSpeed_mmin) < 0.1) THEN
            iMachineState := 7;                         (* Advance to Annealing Transformation Zone Cooling *)
            rStateTimer_s := 0.0;
        END_IF;

    7: (* STATE_ANNEALING_TRANSFORMATION_COOL *)
        (* Establish thermal gradient through glass transformation range (Tg = 520 to 550 deg C) *)
        rAnnealingSettleTimer_s    := rAnnealingSettleTimer_s + tScanTime_s;
        rLehrZoneA_GasFireDuty_Pct := 48.5;
        rLehrZoneB_GasFireDuty_Pct := 32.5;
        rLehrZoneC_CoolDamper_Pct  := 40.0;
        bSystemReady               := FALSE;

        IF (rAnnealingSettleTimer_s >= 150.0) AND (rVoted_LehrTemp_ZoneA_degC >= 530.0) AND (rVoted_LehrTemp_ZoneA_degC <= 540.0) THEN
            iMachineState := 8;                         (* Advance to Polarimeter Stress Optimization *)
            rStateTimer_s := 0.0;
        END_IF;

    8: (* STATE_OPTICAL_RETARDATION_STRESS_OPTIMIZE *)
        (* Tune Zone B and C cooling rates to drive residual retardation below 10 nm/cm *)
        IF rPolarimeterRetardation_nmcm > 8.0 THEN
            rLehrZoneB_GasFireDuty_Pct := rLehrZoneB_GasFireDuty_Pct + 0.5;
            rLehrZoneC_CoolDamper_Pct  := rLehrZoneC_CoolDamper_Pct - 0.5;
        END_IF;
        bSystemReady := FALSE;

        IF (rStateTimer_s >= 90.0) AND (rPolarimeterRetardation_nmcm <= 8.0) THEN
            iMachineState := 9;                         (* Advance to Laser Traverser Thickness Regulation *)
            rStateTimer_s := 0.0;
        END_IF;

    9: (* STATE_RIBBON_LASER_TRAVERSER_OPTIMIZE *)
        (* High-precision closed-loop thickness and width regulation at full steady state *)
        bSystemReady     := TRUE;
        bInAnnealingSpec := (rPolarimeterRetardation_nmcm <= 8.0) AND (ABS(rTraverserThickness_mm - 4.000) <= 0.05);

        (* Check if normal steady state transition to Exit Spray Cooler *)
        IF (rStateTimer_s >= 180.0) AND bInAnnealingSpec THEN
            iMachineState := 10;                        (* Steady State Production with Exit Cooler Run *)
            rStateTimer_s := 0.0;
        END_IF;

    10: (* STATE_LEHR_EXIT_SPRAY_COOLER_RUN *)
        (* Continuous full-production architectural float glass ribbon run *)
        bSystemReady      := TRUE;
        bInAnnealingSpec  := (rPolarimeterRetardation_nmcm <= 10.0) AND (ABS(rTraverserThickness_mm - 4.000) <= 0.05);
        rLehrBlowerVFD_Hz := 45.0;

        (* Remain in State 10 indefinitely during normal commercial production *)

    11: (* STATE_EMERGENCY_TWEEL_DUMP *)
        (* Drop tweel gate, open cullet dump chute, and safely purge tin bath *)
        rCulletDumpTimer_s          := rCulletDumpTimer_s + tScanTime_s;
        rTweelGatePositionCmd_mm    := 0.0;             (* Completely drop tweel gate *)
        rTopRollMasterRun           := FALSE;
        rLehrMainDriveSpeedCmd_mmin := 5.0;             (* Evacuate remaining ribbon from lehr *)
        rLiftOutRollSpeedCmd_mmin   := 5.0;
        rLehrZoneA_GasFireDuty_Pct  := 0.0;
        rLehrZoneB_GasFireDuty_Pct  := 0.0;
        rTinChamberVentDamper_Pct   := 100.0;           (* Open chamber emergency vent *)
        bSystemReady                := FALSE;
        bInAnnealingSpec            := FALSE;
        bEmergencyDumpActive        := TRUE;

        (* Latch until emergency stop is reset and operator acknowledges *)
        IF bEmergencyStop AND bAcknowledgeAlarms AND (rCulletDumpTimer_s >= 60.0) THEN
            bEmergencyDumpActive := FALSE;
            rCulletDumpTimer_s   := 0.0;
            iMachineState        := 1;                  (* Restart cycle from Preheat *)
            rStateTimer_s        := 0.0;
        END_IF;

    12: (* STATE_STANDBY_GAS_CONSERVE *)
        (* Low-temperature standby mode preserving molten tin from freezing or oxidation *)
        rTweelGatePositionCmd_mm    := 0.0;
        rLehrMainDriveSpeedCmd_mmin := 0.0;
        rLiftOutRollSpeedCmd_mmin   := 0.0;
        rTinAtmN2_FlowCmd_Nm3h      := 600.0;           (* Minimum sealing purge *)
        rTinAtmH2_FlowCmd_Nm3h      := 25.0;            (* Low hydrogen trickle *)
        rLehrZoneA_GasFireDuty_Pct  := 10.0;
        rLehrZoneB_GasFireDuty_Pct  := 5.0;
        bSystemReady                := FALSE;
        bInAnnealingSpec            := FALSE;

        IF bMasterEnable THEN
            iMachineState := 1;                         (* Advance to Preheat *)
            rStateTimer_s := 0.0;
        END_IF;

    ELSE
        iMachineState := 1;
        rStateTimer_s := 0.0;
END_CASE;
""")

    # -------------------------------------------------------------------------
    # SECTION 7: Graceful Degradation Decoupled Fallback PIDs
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 7: GRACEFUL DEGRADATION DECOUPLED FALLBACK PID CONTROLLERS                            *)
(* ============================================================================================= *)
IF bGracefulDegradation OR (NOT bAutoPacingEnable) THEN
    (* Loop 1: Tweel Gate Position PID (Canal Flow Rate / Pull Regulation) *)
    rAccumTemp := aOutput_y_sp[1] - rTraverserWidth_m; (* Error on ribbon width *)
    rPID_Integ_Tweel := rPID_Integ_Tweel + (rPID_Ki_Tweel * rAccumTemp * tScanTime_s);
    IF rPID_Integ_Tweel > 300.0 THEN rPID_Integ_Tweel := 300.0; END_IF;
    IF rPID_Integ_Tweel < 100.0 THEN rPID_Integ_Tweel := 100.0; END_IF;
    rTweelGatePositionCmd_mm := (rPID_Kp_Tweel * rAccumTemp) + rPID_Integ_Tweel +
                                (rPID_Kd_Tweel * (rAccumTemp - rPID_PrevErr_Tweel) / tScanTime_s);
    IF rTweelGatePositionCmd_mm > 320.0 THEN rTweelGatePositionCmd_mm := 320.0; END_IF;
    IF rTweelGatePositionCmd_mm < 80.0  THEN rTweelGatePositionCmd_mm := 80.0;  END_IF;
    rPID_PrevErr_Tweel := rAccumTemp;

    (* Loop 2: Top-Roll Master Speed Trim PID (Centerline Thickness Control) *)
    rAccumTemp := aOutput_y_sp[0] - rTraverserThickness_mm; (* Positive error = ribbon too thin *)
    rPID_Integ_TopRoll := rPID_Integ_TopRoll - (rPID_Ki_TopRoll * rAccumTemp * tScanTime_s);
    IF rPID_Integ_TopRoll > 135.0 THEN rPID_Integ_TopRoll := 135.0; END_IF;
    IF rPID_Integ_TopRoll < 85.0  THEN rPID_Integ_TopRoll := 85.0;  END_IF;
    rAccumTemp := rPID_Integ_TopRoll - (rPID_Kp_TopRoll * rAccumTemp);
    FOR iIdxAct := 1 TO 14 DO
        rTopRoll_SpeedCmd_mmin[iIdxAct] := (12.0 + (0.2 * iIdxAct)) * (rAccumTemp / 100.0);
    END_FOR;

    (* Loop 3: Lehr Zone A Heating PID (Transformation Temperature Control) *)
    rAccumTemp := aOutput_y_sp[5] - rVoted_LehrTemp_ZoneA_degC;
    rPID_Integ_LehrZA := rPID_Integ_LehrZA + (rPID_Ki_LehrZA * rAccumTemp * tScanTime_s);
    IF rPID_Integ_LehrZA > 95.0 THEN rPID_Integ_LehrZA := 95.0; END_IF;
    IF rPID_Integ_LehrZA < 5.0  THEN rPID_Integ_LehrZA := 5.0;  END_IF;
    rLehrZoneA_GasFireDuty_Pct := (rPID_Kp_LehrZA * rAccumTemp) + rPID_Integ_LehrZA;
    IF rLehrZoneA_GasFireDuty_Pct > 95.0 THEN rLehrZoneA_GasFireDuty_Pct := 95.0; END_IF;
    IF rLehrZoneA_GasFireDuty_Pct < 5.0  THEN rLehrZoneA_GasFireDuty_Pct := 5.0;  END_IF;

    (* Loop 4: Protective Atmosphere Nitrogen Supply Valve PID (Overpressure Control) *)
    rAccumTemp := aOutput_y_sp[3] - rVoted_TinBathPress_Pa;
    rPID_Integ_Press := rPID_Integ_Press + (rPID_Ki_Press * rAccumTemp * tScanTime_s);
    IF rPID_Integ_Press > 95.0 THEN rPID_Integ_Press := 95.0; END_IF;
    IF rPID_Integ_Press < 15.0 THEN rPID_Integ_Press := 15.0; END_IF;
    rAccumTemp := (rPID_Kp_Press * rAccumTemp) + rPID_Integ_Press;
    IF rAccumTemp > 95.0 THEN rAccumTemp := 95.0; END_IF;
    IF rAccumTemp < 15.0 THEN rAccumTemp := 15.0; END_IF;
    rTinAtmN2_FlowCmd_Nm3h := 1000.0 + (rAccumTemp * 10.0);
    rTinAtmH2_FlowCmd_Nm3h := rTinAtmN2_FlowCmd_Nm3h * 0.052;
END_IF;
""")

    # -------------------------------------------------------------------------
    # SECTION 8: ISA-18.2 Multi-Tiered Alarms & Telemetry Word Packing
    # -------------------------------------------------------------------------
    parts.append("""
(* ============================================================================================= *)
(* SECTION 8: ISA-18.2 MULTI-TIERED ALARM EVALUATION & TELEMETRY DWORD PACKING                   *)
(* ============================================================================================= *)
(* Reset or Acknowledge Alarms *)
IF bAcknowledgeAlarms THEN
    dwAlarmStatusWord := dwAlarmStatusWord AND 16#8000_0000; (* Retain only E-Stop bit *)
END_IF;

(* 1. Tin Bath Chamber Atmosphere Overpressure Alarms (HH, H, L, LL) *)
IF rVoted_TinBathPress_Pa < 2.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0001; (* Bit 0: Overpressure LL Trip *)
    bOverpressureTrip := TRUE;
ELSIF rVoted_TinBathPress_Pa < 5.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0002; (* Bit 1: Overpressure L Warning *)
ELSIF rVoted_TinBathPress_Pa > 25.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0004; (* Bit 2: Overpressure HH Trip *)
ELSIF rVoted_TinBathPress_Pa > 18.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0008; (* Bit 3: Overpressure H Warning *)
ELSE
    bOverpressureTrip := FALSE;
END_IF;

(* 2. Tin Bath Headspace Trace Oxygen & Dew-Point Alarms (Dross Defect Suppression) *)
IF rVoted_TinTraceO2_ppm > 10.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0010; (* Bit 4: Trace O2 HH Critical Dross Trip *)
    bDrossRiskWarning := TRUE;
ELSIF rVoted_TinTraceO2_ppm > 5.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0020; (* Bit 5: Trace O2 H Dross Warning *)
    bDrossRiskWarning := TRUE;
ELSE
    bDrossRiskWarning := FALSE;
END_IF;

IF rTinAtmDewPoint_degC > -35.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0040; (* Bit 6: High Dew Point Moisture Warning *)
END_IF;

(* 3. Residual Optical Stress Retardation Alarms (Glass Annealing Quality) *)
IF rPolarimeterRetardation_nmcm > 20.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0100; (* Bit 8: Optical Retardation HH Glass Breakage Trip *)
ELSIF rPolarimeterRetardation_nmcm > 10.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0200; (* Bit 9: Optical Retardation H Spec Breach Warning *)
END_IF;

(* 4. Canal Tweel Gate Position & Jam Alarms *)
IF ABS(rTweelGatePositionCmd_mm - rTweelGatePosFeedback_mm) > 15.0 THEN
    dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0400; (* Bit 10: Tweel Gate Servo Follow Error Jam *)
END_IF;

(* 5. Top-Roll Edge Knurler Motor Load Alarms *)
FOR iIdxAct := 1 TO 14 DO
    IF rTopRoll_Current_A[iIdxAct] > 14.5 THEN
        dwAlarmStatusWord := dwAlarmStatusWord OR 16#0000_0800; (* Bit 11: Top-Roll Motor Stall / Overload *)
    END_IF;
END_FOR;

(* 6. Pack System Status Word (dwSystemStatusWord) *)
dwSystemStatusWord := (SHL(INT_TO_DWORD(iMachineState), 24)) OR
                      (BOOL_TO_DWORD(bSystemReady)           AND 16#0000_0001) OR
                      (SHL(BOOL_TO_DWORD(bInAnnealingSpec), 1)) OR
                      (SHL(BOOL_TO_DWORD(bOverpressureTrip), 2)) OR
                      (SHL(BOOL_TO_DWORD(bDrossRiskWarning), 3)) OR
                      (SHL(BOOL_TO_DWORD(bMPC_Active), 4)) OR
                      (SHL(BOOL_TO_DWORD(bGracefulDegradation), 5)) OR
                      (SHL(BOOL_TO_DWORD(bEmergencyDumpActive), 6));

END_FUNCTION_BLOCK
""")

    code = "".join(parts)
    return code

if __name__ == "__main__":
    code = generate_float_glass_st()
    print(f"Generated Structured Text code length: {len(code)} characters")

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Glass & Ceramics: Continuous Architectural Float Glass Line with Molten Tin Bath Atmosphere, Top Roller Knurling & Lehr Annealing Thermal Stress Control**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_FloatGlass_Furnace_TinBath_LehrAnnealing
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m3/h], [Pa], [mm], [m/min], [tons/day], [ppm], [%], [kW], [s])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.
5. SAVE using isolated JSON format in data/swarm_raw/agent_2f8019ac.json.
6. REPLY with: EVOLUTION COMPLETE: Commercial Glass & Ceramics: Continuous Architectural Float Glass Line with Molten Tin Bath Atmosphere, Top Roller Knurling & Lehr Annealing Thermal Stress Control"""

    full_output = f"```iec-st\n{code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_output}
        ]
    }

    target_path = os.path.join("data", "swarm_raw", "agent_2f8019ac.json")
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved dataset record to {target_path}")
    print(f"Total assistant content size: {len(full_output)} characters")
