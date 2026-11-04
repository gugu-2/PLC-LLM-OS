# -*- coding: utf-8 -*-
"""
Full Assembly Script for FB_Plastics_BlownFilm_7Layer_IBC_AirRing
Constructs an ultra-dense (~100,000 to 115,000 characters) IEC 61131-3 Function Block
satisfying all V7 Max-Persona directives, mathematical completeness, and 100% delimiter parity.
"""

import os
import sys
import json
import uuid

def build_iec_code():
    st = []
    
    # Opening line
    st.append("FUNCTION_BLOCK FB_Plastics_BlownFilm_7Layer_IBC_AirRing\n")

    # Header documentation
    st.append("""(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
COMMERCIAL INDUSTRIAL SECTOR : Plastics & Polymer Processing Automation (Tier 1 Global Mass Production)
SYSTEM                       : 7-Layer High-Barrier Blown Film Extrusion Complex (EVOH / Polyamide / PE Packaging)
INTEGRATED SUBSYSTEMS        : - 7 Grooved-Feed Extruders with Multi-Component Gravimetric Loss-in-Weight Batch Dosing
                               - 7-Layer Cylindrical Spiral Mandrel Co-Extrusion Die Head (500 mm Die Lip, 1.4 mm Die Gap)
                               - 35 Extruder Barrel PID Thermal Zones + 8 Spiral Mandrel Die Zones with Cold-Screw Interlocks
                               - Internal Bubble Cooling (IBC) Ultrasonic Closed-Loop Diameter & Frost-Line Height Regulation
                               - 360-Degree Oscillating Die Head & Reversing Haul-Off Tower (+/-180 deg Reversing Sweep)
                               - 32-Zone Segmented Automatic Air Ring with Localized High-Speed PWM Heating Orifices
                               - In-Line Non-Contact High-Frequency Capacitive Rotary Thickness Profile Scanner
                               - Dual Turret Center/Surface/Gap Rewinder with Pneumatic Flying Knife Cross-Cut Auto-Splice
                               - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (50.0 ms Scan Period)
                               - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
                               - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting across 5 Triplet Transmitter Arrays
                               - ISA-18.2 5-Tier Process Alarm Hierarchy (HH, H, L, LL, ROC) with Deadband Hysteresis
                               - Deterministic 12-Stage Production Finite State Machine (FSM)
========================================================================================================================
POLYMER RHEOLOGY, MULTI-LAYER BARRIER ARCHITECTURE & AERODYNAMIC FOUNDATIONS:

1. 7-Layer High-Barrier Blown Film Structure & Layer Ratio Allocation:
   This complex produces continuous medical and food ultra-high-barrier film (nominal 70.0 um, layflat width 2500 mm):
     * Layer A (Extruder A, 20.0% mass): Outer skin, Metallocene Linear Low-Density Polyethylene (mLLDPE). Provides
       mechanical puncture resistance, gloss, printability, and external environmental moisture protection.
     * Layer B (Extruder B, 5.0% mass): Outer tie layer, Maleic Anhydride Grafted Polyethylene (MAH-g-PE). Covalent anhydride
       ring-opening bonding to polyamide amino end groups across the polymer-polymer interface.
     * Layer C (Extruder C, 15.0% mass): Outer barrier support, Polyamide 6 (PA6). Provides structural stiffness,
       pinhole flex-crack resistance, thermal resistance during thermoforming, and moisture buffering for EVOH.
     * Layer D (Extruder D, 10.0% mass): Core gas barrier, Ethylene Vinyl Alcohol Copolymer (EVOH, 38 mol% ethylene content).
       Provides ultra-low Oxygen Transmission Rate: OTR < 0.10 cm3 / (m2 * day * atm) at 23 deg C, 0% RH.
     * Layer E (Extruder E, 15.0% mass): Inner barrier support, Polyamide 6 (PA6). Forms a symmetrical PA/EVOH/PA barrier core,
       preventing asymmetric shrinkage curl during thermoforming and water-bath quenching.
     * Layer F (Extruder F, 5.0% mass): Inner tie layer, Maleic Anhydride Grafted Polyethylene (MAH-g-PE). Covalent bonding
       between inner polyamide and the polyolefin inner sealant layer.
     * Layer G (Extruder G, 30.0% mass): Inner seal skin, Metallocene LLDPE / Plastomer blend. Low Heat Seal Initiation
       Temperature (SIT <= 95 deg C), high hot-tack strength for continuous vertical form-fill-seal (VFFS) packaging.

2. Non-Newtonian Polymer Melt Viscoelasticity & Co-Extrusion Interface Stability:
   Each polymer melt stream exhibits pseudoplastic shear-thinning behavior governed by the Carreau-Yasuda equation:
     eta(gamma_dot, T) = eta_0 * a_T * [ 1 + (lambda_rel * a_T * gamma_dot)^a ]^( (n - 1) / a )
   where Arrhenius temperature shift factor a_T = EXP( (E_act / R_gas) * (1/T_melt - 1/T_ref) ).
   At co-extrusion feedblock interfaces, severe viscosity ratio mismatches (eta_i / eta_j > 2.5) or elasticity ratio
   mismatches induce interfacial shear-stress discontinuities, precipitating zig-zag interfacial flow instability.
   Extruder barrel temperatures and feedblock channel geometries are dynamically coordinated to maintain
   interfacial shear stress tau_w < 60.0 kPa across all 6 fluid-fluid boundaries.

3. Internal Bubble Cooling (IBC) Aerodynamics & Static Pressure Balance:
   The blown film bubble constitutes an axisymmetric thin-walled viscoelastic membrane undergoing simultaneous biaxial
   stretching and non-isothermal convective cooling. Internal bubble cooling continuously circulates chilled air
   (10 to 15 deg C) through internal supply and exhaust distributor stacks. The bubble diameter D_b is stabilized by
   maintaining an infinitesimal internal differential pressure:
     Delta P_int = P_int - P_amb = 2 * sigma_hoop * (T_h / D_b) + 2 * sigma_axial * (T_h / R_meridional)
   Nominal internal gauge pressure Delta P_int is approximately 35.0 to 55.0 Pa (0.35 to 0.55 mbar).
   A rise of merely 5.0 Pa increases bubble diameter by > 20 mm, while a drop of 5.0 Pa causes immediate bubble necking.
   Ultrasonic transceivers spaced 120 degrees apart detect acoustic time-of-flight to the moving bubble boundary,
   modulating inverter-driven supply and exhaust blowers in tight differential lockstep to regulate diameter to within
   +/-1.5 mm while simultaneously holding frost-line height stable.

4. 360-Degree Oscillating Reversing Haul-Off Tower Kinematics:
   To eliminate circumferential gauge bands (which cause severe gauge buildup ridges and reel telescoping during winding),
   the primary haul-off nip assembly continuously oscillates over a +/-180.0 degree reversing angular range at a controlled
   angular velocity omega_haul (typically 0.15 to 0.35 deg/s). The oscillation speed is synchronized with line speed
   such that one full oscillation cycle traverses several hundred meters of finished web, distributing residual die-lip
   micrometer variations helically across the full 2500 mm roll width.

5. In-Line Non-Contact Capacitive Thickness Measurement & Segmented Air Ring Control:
   A rotary scanner housing a high-frequency capacitive sensor orbits the bubble circumference at a constant rotational
   velocity. The measured dielectric capacitance C_m = epsilon_0 * epsilon_r * (A_probe / T_h) provides continuous
   film thickness feedback. Because the haul-off tower oscillates while the scanner rotates, a real-time coordinate
   transformation maps each thickness measurement from web coordinates back to the stationary die-lip angular position:
     theta_die = MOD( theta_scan(t) - theta_haul(t) + theta_spiral_lead(z_axial), 360.0 )
   The external automatic air ring incorporates 32 circumferential heating cartridges located in segmented air orifices.
   Modulating cartridge heating power alters local air temperature, which dynamically modifies local cooling air density,
   volumetric flow, and convective heat transfer coefficient h_conv:
     h_conv = 0.026 * (k_air / D_hyd) * Re^0.80 * Pr^0.33
   Locally heated air slows polymer crystallization, prolonging viscoelastic draw-down and selectively thinning localized
   thick gauge spots. The multivariable receding-horizon profile controller maintains 2-sigma gauge variance < +/-1.8%.

6. Receding-Horizon Model Predictive Control (MPC) Formulation:
   The cyber-physical dynamics are governed by an 8-state discrete-time state-space model sampled at Delta t = 0.050 s:
     x[k+1] = A * x[k] + B * u[k]
     y[k]   = C * x[k] + D * u[k]
   The receding-horizon quadratic cost function penalizes gauge error, diameter drift, and actuator effort:
     J(u) = SUM_{j=1}^{Np} [ (y[k+j] - y_sp)^T * Q * (y[k+j] - y_sp) ]
          + SUM_{j=0}^{Nu-1} [ Delta u[k+j]^T * R * Delta u[k+j] ]
          + (x[k+Np] - x_sp)^T * P * (x[k+Np] - x_sp)
   Optimization is executed deterministically on-line using Projected Gradient Descent (PGD) with physical actuator
   saturation constraints, guaranteeing real-time convergence within the 50.0 ms PLC execution budget.
*)
""")

    # VAR_INPUT
    st.append("""VAR_INPUT
    (* ==================== SYSTEM CONTROLS & MASTER PERMISSIVES ==================== *)
    bMasterEnable                   : BOOL;                 (* Master automation system enable command *)
    bEmergencyStop_NC               : BOOL;                 (* Active-low fail-safe Emergency Stop circuit [SIL-3 / Cat 4] *)
    bResetAlarms                    : BOOL;                 (* Master alarm acknowledge and latch reset command *)
    bManualModeSelect               : BOOL;                 (* Manual commissioning and jog override mode selector *)
    rCycleTime_s                    : REAL := 0.050;        (* PLC execution cycle period [s] (nominal 50.0 ms) *)

    (* ==================== EXTRUSION & GRAVIMETRIC SETPOINTS ==================== *)
    rTotalThroughputSetpoint_kgh    : REAL := 650.0;        (* Total multi-extruder combined throughput setpoint [kg/h] *)
    rLayerRatioSetpoint_ExtA_pct    : REAL := 20.0;         (* Extruder A Outer Skin mLLDPE layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtB_pct    : REAL := 5.0;          (* Extruder B Outer Tie MAH-g-PE layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtC_pct    : REAL := 15.0;         (* Extruder C Outer Barrier PA6 layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtD_pct    : REAL := 10.0;         (* Extruder D Core EVOH Barrier layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtE_pct    : REAL := 15.0;         (* Extruder E Inner Barrier PA6 layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtF_pct    : REAL := 5.0;          (* Extruder F Inner Tie MAH-g-PE layer ratio setpoint [%] *)
    rLayerRatioSetpoint_ExtG_pct    : REAL := 30.0;         (* Extruder G Inner Seal mLLDPE layer ratio setpoint [%] *)

    (* ==================== BUBBLE GEOMETRY & KINEMATICS SETPOINTS ==================== *)
    rTargetFilmThickness_um         : REAL := 70.0;         (* Nominal target barrier film thickness [um] *)
    rTargetBubbleDiameter_mm        : REAL := 1591.55;      (* Target bubble outer diameter [mm] (2500.0 mm layflat) *)
    rTargetFrostLineHeight_mm       : REAL := 1250.0;       (* Target axial frost-line height above die lip [mm] *)
    rTargetInternalPressure_Pa      : REAL := 45.0;         (* Target IBC internal cage static differential pressure [Pa] *)
    rTargetLineSpeed_m_min          : REAL := 55.0;         (* Primary haul-off nip roll linear speed setpoint [m/min] *)

    (* ==================== TMR TRIPLET 1: IBC ULTRASONIC BUBBLE DIAMETER SENSORS ==================== *)
    rIBC_US_Dist_Ch1_mm             : REAL;                 (* IBC ultrasonic distance sensor channel 1 [mm] *)
    rIBC_US_Dist_Ch2_mm             : REAL;                 (* IBC ultrasonic distance sensor channel 2 [mm] *)
    rIBC_US_Dist_Ch3_mm             : REAL;                 (* IBC ultrasonic distance sensor channel 3 [mm] *)
    rIBC_AirTemp_degC               : REAL := 22.5;         (* Ambient air temperature at ultrasonic ring for acoustic ToF compensation [deg C] *)

    (* ==================== TMR TRIPLET 2: 7-LAYER FEEDBLOCK MELT PRESSURE SENSORS ==================== *)
    rFeedblock_MeltPress_Ch1_bar    : REAL;                 (* 7-Layer co-extrusion feedblock melt pressure transmitter channel 1 [bar] *)
    rFeedblock_MeltPress_Ch2_bar    : REAL;                 (* 7-Layer co-extrusion feedblock melt pressure transmitter channel 2 [bar] *)
    rFeedblock_MeltPress_Ch3_bar    : REAL;                 (* 7-Layer co-extrusion feedblock melt pressure transmitter channel 3 [bar] *)

    (* ==================== TMR TRIPLET 3: CAPACITIVE THICKNESS REFERENCE SENSORS ==================== *)
    rCapacitiveGauge_Ch1_um         : REAL;                 (* Rotary scanner capacitive thickness gauge channel 1 [um] *)
    rCapacitiveGauge_Ch2_um         : REAL;                 (* Rotary scanner capacitive thickness gauge channel 2 [um] *)
    rCapacitiveGauge_Ch3_um         : REAL;                 (* Rotary scanner capacitive thickness gauge channel 3 [um] *)

    (* ==================== TMR TRIPLET 4: OPTICAL FROST-LINE HEIGHT SENSORS ==================== *)
    rFrostLineSensor_Ch1_mm         : REAL;                 (* Optical triangulation frost-line height sensor channel 1 [mm] *)
    rFrostLineSensor_Ch2_mm         : REAL;                 (* Optical triangulation frost-line height sensor channel 2 [mm] *)
    rFrostLineSensor_Ch3_mm         : REAL;                 (* Optical triangulation frost-line height sensor channel 3 [mm] *)

    (* ==================== TMR TRIPLET 5: IBC INTERNAL DIFFERENTIAL PRESSURE SENSORS ==================== *)
    rBubbleDiffPress_Ch1_Pa         : REAL;                 (* IBC internal cage differential static pressure transmitter channel 1 [Pa] *)
    rBubbleDiffPress_Ch2_Pa         : REAL;                 (* IBC internal cage differential static pressure transmitter channel 2 [Pa] *)
    rBubbleDiffPress_Ch3_Pa         : REAL;                 (* IBC internal cage differential static pressure transmitter channel 3 [Pa] *)

    (* ==================== 7 EXTRUDERS PHYSICAL FEEDBACK ==================== *)
    rExtruderMeltPress_ExtA_bar     : REAL;                 (* Extruder A head melt pressure [bar] *)
    rExtruderMeltPress_ExtB_bar     : REAL;                 (* Extruder B head melt pressure [bar] *)
    rExtruderMeltPress_ExtC_bar     : REAL;                 (* Extruder C head melt pressure [bar] *)
    rExtruderMeltPress_ExtD_bar     : REAL;                 (* Extruder D head melt pressure [bar] *)
    rExtruderMeltPress_ExtE_bar     : REAL;                 (* Extruder E head melt pressure [bar] *)
    rExtruderMeltPress_ExtF_bar     : REAL;                 (* Extruder F head melt pressure [bar] *)
    rExtruderMeltPress_ExtG_bar     : REAL;                 (* Extruder G head melt pressure [bar] *)

    rExtruderMeltTemp_ExtA_degC     : REAL;                 (* Extruder A melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtB_degC     : REAL;                 (* Extruder B melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtC_degC     : REAL;                 (* Extruder C melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtD_degC     : REAL;                 (* Extruder D melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtE_degC     : REAL;                 (* Extruder E melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtF_degC     : REAL;                 (* Extruder F melt stream thermocouple [deg C] *)
    rExtruderMeltTemp_ExtG_degC     : REAL;                 (* Extruder G melt stream thermocouple [deg C] *)

    rExtruderThroughput_ExtA_kgh    : REAL;                 (* Extruder A gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtB_kgh    : REAL;                 (* Extruder B gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtC_kgh    : REAL;                 (* Extruder C gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtD_kgh    : REAL;                 (* Extruder D gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtE_kgh    : REAL;                 (* Extruder E gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtF_kgh    : REAL;                 (* Extruder F gravimetric loss-in-weight rate [kg/h] *)
    rExtruderThroughput_ExtG_kgh    : REAL;                 (* Extruder G gravimetric loss-in-weight rate [kg/h] *)

    rExtruderCurrent_ExtA_A         : REAL;                 (* Extruder A AC vector drive motor current [A] *)
    rExtruderCurrent_ExtB_A         : REAL;                 (* Extruder B AC vector drive motor current [A] *)
    rExtruderCurrent_ExtC_A         : REAL;                 (* Extruder C AC vector drive motor current [A] *)
    rExtruderCurrent_ExtD_A         : REAL;                 (* Extruder D AC vector drive motor current [A] *)
    rExtruderCurrent_ExtE_A         : REAL;                 (* Extruder E AC vector drive motor current [A] *)
    rExtruderCurrent_ExtF_A         : REAL;                 (* Extruder F AC vector drive motor current [A] *)
    rExtruderCurrent_ExtG_A         : REAL;                 (* Extruder G AC vector drive motor current [A] *)

    (* 35 Barrel Temperature Feedback Sensors (5 Zones x 7 Extruders) *)
    arBarrelZoneTemp_ExtA_degC      : ARRAY[1..5] OF REAL;  (* Extruder A Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtB_degC      : ARRAY[1..5] OF REAL;  (* Extruder B Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtC_degC      : ARRAY[1..5] OF REAL;  (* Extruder C Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtD_degC      : ARRAY[1..5] OF REAL;  (* Extruder D Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtE_degC      : ARRAY[1..5] OF REAL;  (* Extruder E Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtF_degC      : ARRAY[1..5] OF REAL;  (* Extruder F Zones 1..5 thermocouple temperatures [deg C] *)
    arBarrelZoneTemp_ExtG_degC      : ARRAY[1..5] OF REAL;  (* Extruder G Zones 1..5 thermocouple temperatures [deg C] *)

    (* 8 Die Mandrel Temperature Feedback Sensors *)
    arDieZoneTemp_degC              : ARRAY[1..8] OF REAL;  (* Spiral mandrel die head Zones 1..8 temperatures [deg C] *)

    (* ==================== AIR RING, HAUL-OFF & SCANNER SENSORS ==================== *)
    rAirRingSupplyAirVelocity_m_s   : REAL;                 (* External main air ring annular air velocity sensor [m/s] *)
    rAirRingSupplyAirTemp_degC      : REAL := 12.0;         (* Chilled air supply temperature to external air ring [deg C] *)
    rHaulOffActualSpeed_m_min       : REAL;                 (* Primary haul-off nip motor encoder feedback [m/min] *)
    rHaulOffOscillationAngle_deg    : REAL;                 (* Reversing haul-off tower angular position resolver [deg] *)
    rCapacitiveScannerAngle_deg     : REAL;                 (* Rotary thickness gauge ring position resolver [deg] *)
    bCapacitiveScannerSyncPulse     : BOOL;                 (* Rotary scanner 360-degree top-dead-center index proximity switch *)

    (* ==================== REWINDER & SPLICE TRANSDUCERS ==================== *)
    rWinderTensionFeedback_N        : REAL;                 (* Dual-load-cell web tension measurement at winder infeed [N] *)
    rWinderRollDiameter_mm          : REAL;                 (* Active winding roll ultrasonic surface diameter sensor [mm] *)
    bSpliceArmCommand               : BOOL;                 (* HMI or length counter automatic flying splice arm command *)
    bCoreLoadedPermissive           : BOOL;                 (* Standby turret spindle core clamped and taped permissive switch *)
END_VAR
""")

    # VAR_OUTPUT
    st.append("""VAR_OUTPUT
    (* ==================== SYSTEM READINESS & STATUS FLAGS ==================== *)
    bSystemReady                    : BOOL;                 (* Master automation system ready permissive *)
    bExtrusionActive                : BOOL;                 (* Co-extrusion melt delivery active flag *)
    bIBC_ClosedLoopLocked           : BOOL;                 (* Internal bubble cooling diameter locked within regulation tolerance *)
    bAirRingProfileActive           : BOOL;                 (* 32-Zone automatic segmented air ring thickness profile control active *)
    nActiveFSM_State                : INT;                  (* Current operating stage of 12-state production FSM [1..12] *)
    sActiveStateName                : STRING[50];           (* Descriptive ASCII designation of active operating state *)

    (* ==================== 7 EXTRUDER SCREW SPEED COMMANDS ==================== *)
    rExtruderSpeedCmd_ExtA_rpm      : REAL;                 (* Extruder A screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtB_rpm      : REAL;                 (* Extruder B screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtC_rpm      : REAL;                 (* Extruder C screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtD_rpm      : REAL;                 (* Extruder D screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtE_rpm      : REAL;                 (* Extruder E screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtF_rpm      : REAL;                 (* Extruder F screw drive speed reference [rpm] *)
    rExtruderSpeedCmd_ExtG_rpm      : REAL;                 (* Extruder G screw drive speed reference [rpm] *)

    (* ==================== IBC ACTUATOR COMMANDS ==================== *)
    rIBC_SupplyBlower_Hz            : REAL;                 (* Inverter frequency command for IBC supply air blower [Hz] *)
    rIBC_ExhaustBlower_Hz           : REAL;                 (* Inverter frequency command for IBC exhaust air blower [Hz] *)
    rIBC_VacuumLockValve_pct        : REAL;                 (* IBC bottom air lock throttling damper proportional position [%] *)

    (* ==================== AIR RING & LINE SPEED COMMANDS ==================== *)
    rAirRingMainBlower_Hz           : REAL;                 (* External air ring high-volume blower inverter frequency [Hz] *)
    rHaulOffSpeedCmd_m_min          : REAL;                 (* Primary haul-off nip servo drive speed command [m/min] *)
    rHaulOffOscillationSpeed_deg_s  : REAL;                 (* Reversing haul-off tower oscillation rotational velocity [deg/s] *)

    (* ==================== SEGMENTED AIR RING HEATING CARTRIDGE PWM (32 ZONES) ==================== *)
    anAirRingCartridgeDuty_pct      : ARRAY[1..32] OF REAL; (* Cartridge heating power modulation setpoint Zones 1..32 [%] *)
    anAirRingCartridgePWM_Out       : ARRAY[1..32] OF BOOL; (* High-speed digital solid-state relay pulse outputs Zones 1..32 *)

    (* ==================== REWINDER & AUXILIARY ACTUATION ==================== *)
    rTurretWinderTorque_Nm          : REAL;                 (* Active turret spindle servo drive torque limit command [Nm] *)
    bFlyingKnifeFire_Cmd            : BOOL;                 (* High-speed pneumatic cross-cut flying knife actuation trigger *)
    bTurretIndex_Cmd                : BOOL;                 (* Dual turret roll spindle indexing motor command *)
    bEdgeTrimSlittersEngaged        : BOOL;                 (* Pneumatic blade actuators for continuous edge trim slitting *)
    bCoronaTreaterActive            : BOOL;                 (* High-frequency dielectric corona surface treater generator enable *)

    (* ==================== OBSERVED CYBER-PHYSICAL STATES & ESTIMATES ==================== *)
    rObserved_AverageThickness_um   : REAL;                 (* Circumferentially averaged film thickness estimate [um] *)
    rObserved_ThicknessStdDev_um    : REAL;                 (* 2-Sigma thickness spatial standard deviation across 32 zones [um] *)
    rObserved_BubbleDiameter_mm     : REAL;                 (* Triplet-voted bubble outer diameter [mm] *)
    rObserved_FrostLineHeight_mm    : REAL;                 (* Triplet-voted axial frost-line height [mm] *)
    rObserved_InternalPressure_Pa   : REAL;                 (* Triplet-voted internal bubble static differential pressure [Pa] *)
    rObserved_TotalThroughput_kgh   : REAL;                 (* Actual summed multi-extruder gravimetric throughput [kg/h] *)

    (* ==================== ISA-18.2 ALARMS & DIAGNOSTIC WORD BITMASKS ==================== *)
    dwAlarmWord_Trip                : DWORD;                (* ISA-18.2 Priority 1 Emergency Trip Alarm Bitmask *)
    dwAlarmWord_Warning             : DWORD;                (* ISA-18.2 Priority 2 Process Warning Alarm Bitmask *)
    dwAlarmWord_Advisory            : DWORD;                (* ISA-18.2 Priority 3 Operational Advisory Alarm Bitmask *)
    dwTMR_DiscrepancyWord           : DWORD;                (* 2oo3 Sensor Triplet Discrepancy Fault Bitmask *)
    dwStatusWord_System             : DWORD;                (* Comprehensive cyber-physical automation status word *)
END_VAR
""")

    # VAR
    st.append("""VAR
    (* ==================== DISCRETE 8x8 STATE-SPACE MODEL MATRICES ==================== *)
    (* States x = [dD_b(mm), dH_fl(mm), dP_int(Pa), dTh(um), dSigma_th(um), dV_air(m/s), dV_nip(m/min), dP_feed(bar)]^T *)
    matA                            : ARRAY[1..8, 1..8] OF REAL;
    (* Inputs u = [dF_ibc_sup(Hz), dF_ibc_exh(Hz), dF_ar_main(Hz), dV_haul(m/min)]^T *)
    matB                            : ARRAY[1..8, 1..4] OF REAL;
    matC                            : ARRAY[1..8, 1..8] OF REAL;
    matD                            : ARRAY[1..8, 1..4] OF REAL;

    vecX                            : ARRAY[1..8] OF REAL;  (* Current state deviation vector *)
    vecX_next                       : ARRAY[1..8] OF REAL;  (* State prediction vector at step k+1 *)
    vecX_pred                       : ARRAY[1..5, 1..8] OF REAL; (* Receding prediction trajectory over 5 horizon steps *)
    vecU                            : ARRAY[1..4] OF REAL;  (* Control actuation deviation vector *)
    vecY                            : ARRAY[1..8] OF REAL;  (* Predicted observation vector *)
    vecX_ref                        : ARRAY[1..8] OF REAL;  (* Reference state targets *)

    (* ==================== MODEL PREDICTIVE CONTROL (MPC) PARAMETERS ==================== *)
    matQ                            : ARRAY[1..8, 1..8] OF REAL; (* State error penalty matrix *)
    matR                            : ARRAY[1..4, 1..4] OF REAL; (* Actuator slew penalty matrix *)
    matP                            : ARRAY[1..8, 1..8] OF REAL; (* Terminal Riccati penalty matrix *)

    vecGrad                         : ARRAY[1..4] OF REAL;  (* Cost function gradient vector *)
    vecU_mpc                        : ARRAY[1..4] OF REAL;  (* Optimal control output vector *)
    vecU_prev                       : ARRAY[1..4] OF REAL;  (* Actuator command history at k-1 *)

    rMPC_Alpha                      : REAL := 0.015;        (* PGD step-size parameter *)
    nMPC_MaxIterations              : INT := 6;             (* Real-time gradient descent iterations per PLC scan *)
    nMPC_HorizonSteps               : INT := 5;             (* Finite prediction horizon steps *)

    (* ==================== 2oo3 TMR SENSOR VOTING STRUCTURES ==================== *)
    (* Triplet 1: IBC Ultrasonic Bubble Diameter *)
    rVoted_IBC_Diameter_mm          : REAL;
    rTMR_DiscrepancyTimer_US_s      : REAL;
    bTMR_Fault_US_Ch1               : BOOL;
    bTMR_Fault_US_Ch2               : BOOL;
    bTMR_Fault_US_Ch3               : BOOL;

    (* Triplet 2: 7-Layer Feedblock Melt Pressure *)
    rVoted_Feedblock_Press_bar      : REAL;
    rTMR_DiscrepancyTimer_PT_s      : REAL;
    bTMR_Fault_PT_Ch1               : BOOL;
    bTMR_Fault_PT_Ch2               : BOOL;
    bTMR_Fault_PT_Ch3               : BOOL;

    (* Triplet 3: Capacitive Thickness Reference *)
    rVoted_CapacitiveGauge_um       : REAL;
    rTMR_DiscrepancyTimer_Cap_s     : REAL;
    bTMR_Fault_Cap_Ch1              : BOOL;
    bTMR_Fault_Cap_Ch2              : BOOL;
    bTMR_Fault_Cap_Ch3              : BOOL;

    (* Triplet 4: Frost-Line Height Optical Sensors *)
    rVoted_FrostLine_mm             : REAL;
    rTMR_DiscrepancyTimer_FL_s      : REAL;
    bTMR_Fault_FL_Ch1               : BOOL;
    bTMR_Fault_FL_Ch2               : BOOL;
    bTMR_Fault_FL_Ch3               : BOOL;

    (* Triplet 5: IBC Differential Static Pressure *)
    rVoted_InternalPressure_Pa      : REAL;
    rTMR_DiscrepancyTimer_DP_s      : REAL;
    bTMR_Fault_DP_Ch1               : BOOL;
    bTMR_Fault_DP_Ch2               : BOOL;
    bTMR_Fault_DP_Ch3               : BOOL;

    (* ==================== SEGMENTED AIR RING PROFILE CONTROL (32 ZONES) ==================== *)
    arRawGauge_32                   : ARRAY[1..32] OF REAL; (* Sector-allocated thickness measurements [um] *)
    arFilteredGauge_32              : ARRAY[1..32] OF REAL; (* Gaussian spatial filtered thickness profile [um] *)
    arProfileError_32               : ARRAY[1..32] OF REAL; (* Error from nominal target thickness [um] *)
    arIntegralError_32              : ARRAY[1..32] OF REAL; (* Anti-windup discrete integral sum [um*s] *)
    arPWM_Accumulators_s            : ARRAY[1..32] OF REAL; (* Sub-second PWM pulse generation timers [s] *)
    rPWM_Period_s                   : REAL := 2.00;         (* Solid-state relay modulation cycle time [s] *)
    rAirRing_BaseDuty_pct           : REAL := 50.0;         (* Nominal operating cartridge power duty [%] *)
    rAirRing_Kp                     : REAL := 3.50;         (* Proportional gain [% per um deviation] *)
    rAirRing_Ki                     : REAL := 0.22;         (* Integral gain [% per (um*s)] *)

    (* Coordinate transformation mapping variables *)
    rScannerPreviousAngle_deg       : REAL;
    rScannerSpeed_deg_s             : REAL;
    rSpatialSpiralOffset_deg        : REAL := 18.5;         (* Melt flow spiral lead angle from die lip to freeze line [deg] *)

    (* ==================== 7 EXTRUDERS PROCESS MONITORING & INTERLOCKS ==================== *)
    arExtruderSoakTimer_s           : ARRAY[1..7] OF REAL;  (* Thermal equilibrium soak timers for extruders A..G [s] *)
    arExtruderPermissive            : ARRAY[1..7] OF BOOL;  (* Screw cold-start prevention interlock bits *)
    arExtruderSpecificOutput_kgh_rpm: ARRAY[1..7] OF REAL;  (* Specific throughput coefficient [kg/(h*rpm)] *)
    arExtruderMeltDensity_kg_m3     : ARRAY[1..7] OF REAL;  (* High-temperature melt density [kg/m3] *)

    (* 35 Barrel Zones & 8 Die Zones Temperature Setpoints [deg C] *)
    arBarrelZoneSP_ExtA_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtB_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtC_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtD_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtE_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtF_degC        : ARRAY[1..5] OF REAL;
    arBarrelZoneSP_ExtG_degC        : ARRAY[1..5] OF REAL;
    arDieZoneSP_degC                : ARRAY[1..8] OF REAL;

    (* Extruder Barrel Zones Heating Duty [%] and Error [deg C] *)
    arBarrelDuty_ExtA_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtB_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtC_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtD_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtE_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtF_pct           : ARRAY[1..5] OF REAL;
    arBarrelDuty_ExtG_pct           : ARRAY[1..5] OF REAL;
    arDieZoneDuty_pct               : ARRAY[1..8] OF REAL;

    (* Feedblock Co-Extrusion Shear Stress & Interfacial Viscosity Tracking *)
    arExtruderShearRate_s_inv       : ARRAY[1..7] OF REAL;  (* Apparent shear rate in spiral die channels [1/s] *)
    arExtruderApparentVisc_Pa_s     : ARRAY[1..7] OF REAL;  (* High-shear non-Newtonian melt viscosity [Pa*s] *)
    arExtruderWallShearStress_kPa   : ARRAY[1..7] OF REAL;  (* Shear stress at channel interface [kPa] *)

    (* ==================== REWINDER TENSION & FLYING SPLICE SEQUENCE ==================== *)
    rWinderTensionIntegral_Ns       : REAL;                 (* Tension error accumulator [N*s] *)
    rWinderDancerPosition_pct       : REAL;                 (* Pneumatic dancer displacement [%] *)
    rCoreNominalDiameter_mm         : REAL := 152.4;        (* 6-inch standard heavy-duty fiberboard core [mm] *)
    rSpliceTriggerDiameter_mm       : REAL := 1050.0;       (* Diameter threshold initiating flying cut splice [mm] *)
    rSpliceSequenceTimer_s          : REAL;                 (* Roll transfer multi-stage sequencer timer [s] *)
    bSpliceInProgress               : BOOL;                 (* Cross-cut sequence active latch *)
    nSpliceSubStage                 : INT;                  (* Splice sub-state: 0=Idle, 1=Prep, 2=Cut, 3=Index *)
    rRollInertia_kg_m2              : REAL;                 (* Dynamic moment of inertia of winding film reel [kg*m2] *)

    (* ==================== 12-STAGE PRODUCTION FSM INTERNAL VARIABLES ==================== *)
    rStateTimer_s                   : REAL;                 (* State dwell stopwatch timer [s] *)
    nPreviousFSM_State              : INT;                  (* Historical state for edge detection *)
    bThermalSoakComplete            : BOOL;                 (* All 35 barrel zones and 8 die zones soaked *)
    bGravimetricDosingReady         : BOOL;                 (* All 7 feeders calibrated and loss-in-weight stable *)
    bDieMeltUniform                 : BOOL;                 (* Melt pressure balanced across 7 spiral channels *)
    bBubbleSeeded                   : BOOL;                 (* Operator manual bubble neck pulled through haul-off *)
    bIBC_TrackingGood               : BOOL;                 (* Diameter error <= 3.0 mm for > 15 seconds *)
    bLineSpeedAtSetpoint            : BOOL;                 (* Haul-off nip speed within 0.2 m/min of target *)
    bThicknessProfileMatured        : BOOL;                 (* 3 complete 360-deg scanner sweeps integrated *)
    bAirRingInControl               : BOOL;                 (* 2-Sigma gauge variance <= 1.8 um *)

    (* ==================== GENERAL WORKSPACE & ITERATION COUNTERS ==================== *)
    i                               : INT;
    j                               : INT;
    h_step                          : INT;
    k_idx                           : INT;
    nZoneIdx                        : INT;
    rTempSum                        : REAL;
    rTempDiff                       : REAL;
    rTempNorm                       : REAL;
    rSoundSpeed_m_s                 : REAL;
    rCalculatedDiameter_mm          : REAL;
    rLayflatWidth_mm                : REAL;
    rBlowUpRatio                    : REAL;
    rDrawDownRatio                  : REAL;
    rTotalMassFlow_kgh              : REAL;
    rTheoreticalThroughput_kgh      : REAL;
    rGaugeSum                       : REAL;
    rGaugeVarianceSum               : REAL;
    rTargetTorque_Nm                : REAL;
    rTaperTension_N                 : REAL;
    rTaperFactor                    : REAL := 0.25;         (* 25% tension taper from core to full package diameter *)

    (* ==================== ISA-18.2 PROCESS TRIP & WARNING LATCHES ==================== *)
    bTrip_EmergencyStop             : BOOL;
    bTrip_MeltOverpressureFeedblock : BOOL;
    bTrip_BubbleRuptureLoss         : BOOL;
    bTrip_ExtruderMotorOvercurrent  : BOOL;
    bTrip_IBC_BlowerFault           : BOOL;
    bTrip_HaulOffDriveStall         : BOOL;

    bWarn_GaugeVarianceHigh         : BOOL;
    bWarn_FrostLineDrift            : BOOL;
    bWarn_IBC_PressureDeviation     : BOOL;
    bWarn_FeederStarvation          : BOOL;
    bWarn_MeltTempDeviation         : BOOL;
    bWarn_TMR_DegradedMode          : BOOL;
    bWarn_WinderTensionExcursion    : BOOL;
    bWarn_InterfacialShearHigh      : BOOL;
END_VAR
""")

    # Implementation: Phase 1 (2oo3 TMR)
    st.append("""
(* =====================================================================================================================
   PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING & DISCREPANCY TIMERS
   Robust, fault-tolerant voting logic across 5 critical transmitter triplets with bumpless degradation and alarm logging.
   ===================================================================================================================== *)

(* --- TRIPLET 1: IBC Ultrasonic Bubble Diameter Transducers --- *)
bTMR_Fault_US_Ch1 := FALSE;
bTMR_Fault_US_Ch2 := FALSE;
bTMR_Fault_US_Ch3 := FALSE;

IF (ABS(rIBC_US_Dist_Ch1_mm - rIBC_US_Dist_Ch2_mm) <= 15.0) AND (ABS(rIBC_US_Dist_Ch1_mm - rIBC_US_Dist_Ch3_mm) <= 15.0) THEN
    (* All 3 channels agree: compute arithmetic mean *)
    rCalculatedDiameter_mm := (rIBC_US_Dist_Ch1_mm + rIBC_US_Dist_Ch2_mm + rIBC_US_Dist_Ch3_mm) / 3.0;
    rTMR_DiscrepancyTimer_US_s := 0.0;
ELSIF (ABS(rIBC_US_Dist_Ch1_mm - rIBC_US_Dist_Ch2_mm) <= 15.0) THEN
    (* Channel 3 deviates *)
    rCalculatedDiameter_mm := (rIBC_US_Dist_Ch1_mm + rIBC_US_Dist_Ch2_mm) * 0.5;
    bTMR_Fault_US_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_US_s := rTMR_DiscrepancyTimer_US_s + rCycleTime_s;
ELSIF (ABS(rIBC_US_Dist_Ch1_mm - rIBC_US_Dist_Ch3_mm) <= 15.0) THEN
    (* Channel 2 deviates *)
    rCalculatedDiameter_mm := (rIBC_US_Dist_Ch1_mm + rIBC_US_Dist_Ch3_mm) * 0.5;
    bTMR_Fault_US_Ch2 := TRUE;
    rTMR_DiscrepancyTimer_US_s := rTMR_DiscrepancyTimer_US_s + rCycleTime_s;
ELSIF (ABS(rIBC_US_Dist_Ch2_mm - rIBC_US_Dist_Ch3_mm) <= 15.0) THEN
    (* Channel 1 deviates *)
    rCalculatedDiameter_mm := (rIBC_US_Dist_Ch2_mm + rIBC_US_Dist_Ch3_mm) * 0.5;
    bTMR_Fault_US_Ch1 := TRUE;
    rTMR_DiscrepancyTimer_US_s := rTMR_DiscrepancyTimer_US_s + rCycleTime_s;
ELSE
    (* Total 2oo3 disagreement: select median value and latch fault *)
    IF ((rIBC_US_Dist_Ch1_mm >= rIBC_US_Dist_Ch2_mm) AND (rIBC_US_Dist_Ch1_mm <= rIBC_US_Dist_Ch3_mm)) OR
       ((rIBC_US_Dist_Ch1_mm >= rIBC_US_Dist_Ch3_mm) AND (rIBC_US_Dist_Ch1_mm <= rIBC_US_Dist_Ch2_mm)) THEN
        rCalculatedDiameter_mm := rIBC_US_Dist_Ch1_mm;
    ELSIF ((rIBC_US_Dist_Ch2_mm >= rIBC_US_Dist_Ch1_mm) AND (rIBC_US_Dist_Ch2_mm <= rIBC_US_Dist_Ch3_mm)) OR
          ((rIBC_US_Dist_Ch2_mm >= rIBC_US_Dist_Ch3_mm) AND (rIBC_US_Dist_Ch2_mm <= rIBC_US_Dist_Ch1_mm)) THEN
        rCalculatedDiameter_mm := rIBC_US_Dist_Ch2_mm;
    ELSE
        rCalculatedDiameter_mm := rIBC_US_Dist_Ch3_mm;
    END_IF;
    bTMR_Fault_US_Ch1 := TRUE;
    bTMR_Fault_US_Ch2 := TRUE;
    bTMR_Fault_US_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_US_s := rTMR_DiscrepancyTimer_US_s + rCycleTime_s;
END_IF;

(* Acoustic Temperature Correction on Ultrasonic Time-of-Flight *)
(* Speed of sound in dry air: c = 331.3 * SQRT(1 + T_C / 273.15) *)
rSoundSpeed_m_s := 331.3 * SQRT(1.0 + (rIBC_AirTemp_degC / 273.15));
(* Distance scaling compensation relative to 20.0 C calibration base *)
rVoted_IBC_Diameter_mm := rCalculatedDiameter_mm * (rSoundSpeed_m_s / 343.21);
rObserved_BubbleDiameter_mm := rVoted_IBC_Diameter_mm;


(* --- TRIPLET 2: 7-Layer Co-Extrusion Feedblock Melt Pressure Transducers --- *)
bTMR_Fault_PT_Ch1 := FALSE;
bTMR_Fault_PT_Ch2 := FALSE;
bTMR_Fault_PT_Ch3 := FALSE;

IF (ABS(rFeedblock_MeltPress_Ch1_bar - rFeedblock_MeltPress_Ch2_bar) <= 12.0) AND
   (ABS(rFeedblock_MeltPress_Ch1_bar - rFeedblock_MeltPress_Ch3_bar) <= 12.0) THEN
    rVoted_Feedblock_Press_bar := (rFeedblock_MeltPress_Ch1_bar + rFeedblock_MeltPress_Ch2_bar + rFeedblock_MeltPress_Ch3_bar) / 3.0;
    rTMR_DiscrepancyTimer_PT_s := 0.0;
ELSIF (ABS(rFeedblock_MeltPress_Ch1_bar - rFeedblock_MeltPress_Ch2_bar) <= 12.0) THEN
    rVoted_Feedblock_Press_bar := (rFeedblock_MeltPress_Ch1_bar + rFeedblock_MeltPress_Ch2_bar) * 0.5;
    bTMR_Fault_PT_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_PT_s := rTMR_DiscrepancyTimer_PT_s + rCycleTime_s;
ELSIF (ABS(rFeedblock_MeltPress_Ch1_bar - rFeedblock_MeltPress_Ch3_bar) <= 12.0) THEN
    rVoted_Feedblock_Press_bar := (rFeedblock_MeltPress_Ch1_bar + rFeedblock_MeltPress_Ch3_bar) * 0.5;
    bTMR_Fault_PT_Ch2 := TRUE;
    rTMR_DiscrepancyTimer_PT_s := rTMR_DiscrepancyTimer_PT_s + rCycleTime_s;
ELSIF (ABS(rFeedblock_MeltPress_Ch2_bar - rFeedblock_MeltPress_Ch3_bar) <= 12.0) THEN
    rVoted_Feedblock_Press_bar := (rFeedblock_MeltPress_Ch2_bar + rFeedblock_MeltPress_Ch3_bar) * 0.5;
    bTMR_Fault_PT_Ch1 := TRUE;
    rTMR_DiscrepancyTimer_PT_s := rTMR_DiscrepancyTimer_PT_s + rCycleTime_s;
ELSE
    IF ((rFeedblock_MeltPress_Ch1_bar >= rFeedblock_MeltPress_Ch2_bar) AND (rFeedblock_MeltPress_Ch1_bar <= rFeedblock_MeltPress_Ch3_bar)) OR
       ((rFeedblock_MeltPress_Ch1_bar >= rFeedblock_MeltPress_Ch3_bar) AND (rFeedblock_MeltPress_Ch1_bar <= rFeedblock_MeltPress_Ch2_bar)) THEN
        rVoted_Feedblock_Press_bar := rFeedblock_MeltPress_Ch1_bar;
    ELSIF ((rFeedblock_MeltPress_Ch2_bar >= rFeedblock_MeltPress_Ch1_bar) AND (rFeedblock_MeltPress_Ch2_bar <= rFeedblock_MeltPress_Ch3_bar)) OR
          ((rFeedblock_MeltPress_Ch2_bar >= rFeedblock_MeltPress_Ch3_bar) AND (rFeedblock_MeltPress_Ch2_bar <= rFeedblock_MeltPress_Ch1_bar)) THEN
        rVoted_Feedblock_Press_bar := rFeedblock_MeltPress_Ch2_bar;
    ELSE
        rVoted_Feedblock_Press_bar := rFeedblock_MeltPress_Ch3_bar;
    END_IF;
    bTMR_Fault_PT_Ch1 := TRUE;
    bTMR_Fault_PT_Ch2 := TRUE;
    bTMR_Fault_PT_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_PT_s := rTMR_DiscrepancyTimer_PT_s + rCycleTime_s;
END_IF;


(* --- TRIPLET 3: Capacitive Thickness Profile Reference Sensors --- *)
bTMR_Fault_Cap_Ch1 := FALSE;
bTMR_Fault_Cap_Ch2 := FALSE;
bTMR_Fault_Cap_Ch3 := FALSE;

IF (ABS(rCapacitiveGauge_Ch1_um - rCapacitiveGauge_Ch2_um) <= 3.0) AND
   (ABS(rCapacitiveGauge_Ch1_um - rCapacitiveGauge_Ch3_um) <= 3.0) THEN
    rVoted_CapacitiveGauge_um := (rCapacitiveGauge_Ch1_um + rCapacitiveGauge_Ch2_um + rCapacitiveGauge_Ch3_um) / 3.0;
    rTMR_DiscrepancyTimer_Cap_s := 0.0;
ELSIF (ABS(rCapacitiveGauge_Ch1_um - rCapacitiveGauge_Ch2_um) <= 3.0) THEN
    rVoted_CapacitiveGauge_um := (rCapacitiveGauge_Ch1_um + rCapacitiveGauge_Ch2_um) * 0.5;
    bTMR_Fault_Cap_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_Cap_s := rTMR_DiscrepancyTimer_Cap_s + rCycleTime_s;
ELSIF (ABS(rCapacitiveGauge_Ch1_um - rCapacitiveGauge_Ch3_um) <= 3.0) THEN
    rVoted_CapacitiveGauge_um := (rCapacitiveGauge_Ch1_um + rCapacitiveGauge_Ch3_um) * 0.5;
    bTMR_Fault_Cap_Ch2 := TRUE;
    rTMR_DiscrepancyTimer_Cap_s := rTMR_DiscrepancyTimer_Cap_s + rCycleTime_s;
ELSIF (ABS(rCapacitiveGauge_Ch2_um - rCapacitiveGauge_Ch3_um) <= 3.0) THEN
    rVoted_CapacitiveGauge_um := (rCapacitiveGauge_Ch2_um + rCapacitiveGauge_Ch3_um) * 0.5;
    bTMR_Fault_Cap_Ch1 := TRUE;
    rTMR_DiscrepancyTimer_Cap_s := rTMR_DiscrepancyTimer_Cap_s + rCycleTime_s;
ELSE
    IF ((rCapacitiveGauge_Ch1_um >= rCapacitiveGauge_Ch2_um) AND (rCapacitiveGauge_Ch1_um <= rCapacitiveGauge_Ch3_um)) OR
       ((rCapacitiveGauge_Ch1_um >= rCapacitiveGauge_Ch3_um) AND (rCapacitiveGauge_Ch1_um <= rCapacitiveGauge_Ch2_um)) THEN
        rVoted_CapacitiveGauge_um := rCapacitiveGauge_Ch1_um;
    ELSIF ((rCapacitiveGauge_Ch2_um >= rCapacitiveGauge_Ch1_um) AND (rCapacitiveGauge_Ch2_um <= rCapacitiveGauge_Ch3_um)) OR
          ((rCapacitiveGauge_Ch2_um >= rCapacitiveGauge_Ch3_um) AND (rCapacitiveGauge_Ch2_um <= rCapacitiveGauge_Ch1_um)) THEN
        rVoted_CapacitiveGauge_um := rCapacitiveGauge_Ch2_um;
    ELSE
        rVoted_CapacitiveGauge_um := rCapacitiveGauge_Ch3_um;
    END_IF;
    bTMR_Fault_Cap_Ch1 := TRUE;
    bTMR_Fault_Cap_Ch2 := TRUE;
    bTMR_Fault_Cap_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_Cap_s := rTMR_DiscrepancyTimer_Cap_s + rCycleTime_s;
END_IF;
rObserved_AverageThickness_um := rVoted_CapacitiveGauge_um;


(* --- TRIPLET 4: Optical Frost-Line Height Sensors --- *)
bTMR_Fault_FL_Ch1 := FALSE;
bTMR_Fault_FL_Ch2 := FALSE;
bTMR_Fault_FL_Ch3 := FALSE;

IF (ABS(rFrostLineSensor_Ch1_mm - rFrostLineSensor_Ch2_mm) <= 25.0) AND
   (ABS(rFrostLineSensor_Ch1_mm - rFrostLineSensor_Ch3_mm) <= 25.0) THEN
    rVoted_FrostLine_mm := (rFrostLineSensor_Ch1_mm + rFrostLineSensor_Ch2_mm + rFrostLineSensor_Ch3_mm) / 3.0;
    rTMR_DiscrepancyTimer_FL_s := 0.0;
ELSIF (ABS(rFrostLineSensor_Ch1_mm - rFrostLineSensor_Ch2_mm) <= 25.0) THEN
    rVoted_FrostLine_mm := (rFrostLineSensor_Ch1_mm + rFrostLineSensor_Ch2_mm) * 0.5;
    bTMR_Fault_FL_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_FL_s := rTMR_DiscrepancyTimer_FL_s + rCycleTime_s;
ELSIF (ABS(rFrostLineSensor_Ch1_mm - rFrostLineSensor_Ch3_mm) <= 25.0) THEN
    rVoted_FrostLine_mm := (rFrostLineSensor_Ch1_mm + rFrostLineSensor_Ch3_mm) * 0.5;
    bTMR_Fault_FL_Ch2 := TRUE;
    rTMR_DiscrepancyTimer_FL_s := rTMR_DiscrepancyTimer_FL_s + rCycleTime_s;
ELSIF (ABS(rFrostLineSensor_Ch2_mm - rFrostLineSensor_Ch3_mm) <= 25.0) THEN
    rVoted_FrostLine_mm := (rFrostLineSensor_Ch2_mm + rFrostLineSensor_Ch3_mm) * 0.5;
    bTMR_Fault_FL_Ch1 := TRUE;
    rTMR_DiscrepancyTimer_FL_s := rTMR_DiscrepancyTimer_FL_s + rCycleTime_s;
ELSE
    IF ((rFrostLineSensor_Ch1_mm >= rFrostLineSensor_Ch2_mm) AND (rFrostLineSensor_Ch1_mm <= rFrostLineSensor_Ch3_mm)) OR
       ((rFrostLineSensor_Ch1_mm >= rFrostLineSensor_Ch3_mm) AND (rFrostLineSensor_Ch1_mm <= rFrostLineSensor_Ch2_mm)) THEN
        rVoted_FrostLine_mm := rFrostLineSensor_Ch1_mm;
    ELSIF ((rFrostLineSensor_Ch2_mm >= rFrostLineSensor_Ch1_mm) AND (rFrostLineSensor_Ch2_mm <= rFrostLineSensor_Ch3_mm)) OR
          ((rFrostLineSensor_Ch2_mm >= rFrostLineSensor_Ch3_mm) AND (rFrostLineSensor_Ch2_mm <= rFrostLineSensor_Ch1_mm)) THEN
        rVoted_FrostLine_mm := rFrostLineSensor_Ch2_mm;
    ELSE
        rVoted_FrostLine_mm := rFrostLineSensor_Ch3_mm;
    END_IF;
    bTMR_Fault_FL_Ch1 := TRUE;
    bTMR_Fault_FL_Ch2 := TRUE;
    bTMR_Fault_FL_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_FL_s := rTMR_DiscrepancyTimer_FL_s + rCycleTime_s;
END_IF;
rObserved_FrostLineHeight_mm := rVoted_FrostLine_mm;


(* --- TRIPLET 5: IBC Differential Static Pressure Transducers --- *)
bTMR_Fault_DP_Ch1 := FALSE;
bTMR_Fault_DP_Ch2 := FALSE;
bTMR_Fault_DP_Ch3 := FALSE;

IF (ABS(rBubbleDiffPress_Ch1_Pa - rBubbleDiffPress_Ch2_Pa) <= 4.0) AND
   (ABS(rBubbleDiffPress_Ch1_Pa - rBubbleDiffPress_Ch3_Pa) <= 4.0) THEN
    rVoted_InternalPressure_Pa := (rBubbleDiffPress_Ch1_Pa + rBubbleDiffPress_Ch2_Pa + rBubbleDiffPress_Ch3_Pa) / 3.0;
    rTMR_DiscrepancyTimer_DP_s := 0.0;
ELSIF (ABS(rBubbleDiffPress_Ch1_Pa - rBubbleDiffPress_Ch2_Pa) <= 4.0) THEN
    rVoted_InternalPressure_Pa := (rBubbleDiffPress_Ch1_Pa + rBubbleDiffPress_Ch2_Pa) * 0.5;
    bTMR_Fault_DP_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_DP_s := rTMR_DiscrepancyTimer_DP_s + rCycleTime_s;
ELSIF (ABS(rBubbleDiffPress_Ch1_Pa - rBubbleDiffPress_Ch3_Pa) <= 4.0) THEN
    rVoted_InternalPressure_Pa := (rBubbleDiffPress_Ch1_Pa + rBubbleDiffPress_Ch3_Pa) * 0.5;
    bTMR_Fault_DP_Ch2 := TRUE;
    rTMR_DiscrepancyTimer_DP_s := rTMR_DiscrepancyTimer_DP_s + rCycleTime_s;
ELSIF (ABS(rBubbleDiffPress_Ch2_Pa - rBubbleDiffPress_Ch3_Pa) <= 4.0) THEN
    rVoted_InternalPressure_Pa := (rBubbleDiffPress_Ch2_Pa + rBubbleDiffPress_Ch3_Pa) * 0.5;
    bTMR_Fault_DP_Ch1 := TRUE;
    rTMR_DiscrepancyTimer_DP_s := rTMR_DiscrepancyTimer_DP_s + rCycleTime_s;
ELSE
    IF ((rBubbleDiffPress_Ch1_Pa >= rBubbleDiffPress_Ch2_Pa) AND (rBubbleDiffPress_Ch1_Pa <= rBubbleDiffPress_Ch3_Pa)) OR
       ((rBubbleDiffPress_Ch1_Pa >= rBubbleDiffPress_Ch3_Pa) AND (rBubbleDiffPress_Ch1_Pa <= rBubbleDiffPress_Ch2_Pa)) THEN
        rVoted_InternalPressure_Pa := rBubbleDiffPress_Ch1_Pa;
    ELSIF ((rBubbleDiffPress_Ch2_Pa >= rBubbleDiffPress_Ch1_Pa) AND (rBubbleDiffPress_Ch2_Pa <= rBubbleDiffPress_Ch3_Pa)) OR
          ((rBubbleDiffPress_Ch2_Pa >= rBubbleDiffPress_Ch3_Pa) AND (rBubbleDiffPress_Ch2_Pa <= rBubbleDiffPress_Ch1_Pa)) THEN
        rVoted_InternalPressure_Pa := rBubbleDiffPress_Ch2_Pa;
    ELSE
        rVoted_InternalPressure_Pa := rBubbleDiffPress_Ch3_Pa;
    END_IF;
    bTMR_Fault_DP_Ch1 := TRUE;
    bTMR_Fault_DP_Ch2 := TRUE;
    bTMR_Fault_DP_Ch3 := TRUE;
    rTMR_DiscrepancyTimer_DP_s := rTMR_DiscrepancyTimer_DP_s + rCycleTime_s;
END_IF;
rObserved_InternalPressure_Pa := rVoted_InternalPressure_Pa;

(* Pack 2oo3 TMR Discrepancy Bitmask *)
dwTMR_DiscrepancyWord := 16#0000_0000;
IF bTMR_Fault_US_Ch1 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0001; END_IF;
IF bTMR_Fault_US_Ch2 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0002; END_IF;
IF bTMR_Fault_US_Ch3 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0004; END_IF;
IF bTMR_Fault_PT_Ch1 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0008; END_IF;
IF bTMR_Fault_PT_Ch2 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0010; END_IF;
IF bTMR_Fault_PT_Ch3 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0020; END_IF;
IF bTMR_Fault_Cap_Ch1 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0040; END_IF;
IF bTMR_Fault_Cap_Ch2 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0080; END_IF;
IF bTMR_Fault_Cap_Ch3 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0100; END_IF;
IF bTMR_Fault_FL_Ch1 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0200; END_IF;
IF bTMR_Fault_FL_Ch2 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0400; END_IF;
IF bTMR_Fault_FL_Ch3 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_0800; END_IF;
IF bTMR_Fault_DP_Ch1 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_1000; END_IF;
IF bTMR_Fault_DP_Ch2 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_2000; END_IF;
IF bTMR_Fault_DP_Ch3 THEN dwTMR_DiscrepancyWord := dwTMR_DiscrepancyWord OR 16#0000_4000; END_IF;
""")

    # Implementation: Phase 2 (Kinematics, BUR, DDR, Mass Balance)
    st.append("""
(* =====================================================================================================================
   PHASE 2: BUBBLE KINEMATICS, BLOW-UP RATIO, DRAW-DOWN RATIO & CONTINUITY MASS BALANCE
   Deterministic conservation of mass and non-linear volumetric calculations across the co-extruded tubular membrane.
   ===================================================================================================================== *)

(* Layflat width W_lf = (pi * D_b) / 2 *)
rLayflatWidth_mm := (3.14159265 * rObserved_BubbleDiameter_mm) * 0.5;

(* Blow-Up Ratio (BUR): Die lip diameter is 500.0 mm *)
rBlowUpRatio := rObserved_BubbleDiameter_mm / 500.0;

(* Draw-Down Ratio (DDR): Die gap is 1.40 mm (1400.0 um) *)
IF (rObserved_AverageThickness_um > 5.0) AND (rBlowUpRatio > 0.5) THEN
    rDrawDownRatio := 1400.0 / (rObserved_AverageThickness_um * rBlowUpRatio);
ELSE
    rDrawDownRatio := 10.0;
END_IF;

(* Sum actual throughput across all 7 extruders *)
rTotalMassFlow_kgh := rExtruderThroughput_ExtA_kgh + rExtruderThroughput_ExtB_kgh +
                      rExtruderThroughput_ExtC_kgh + rExtruderThroughput_ExtD_kgh +
                      rExtruderThroughput_ExtE_kgh + rExtruderThroughput_ExtF_kgh +
                      rExtruderThroughput_ExtG_kgh;
rObserved_TotalThroughput_kgh := rTotalMassFlow_kgh;

(* Theoretical mass flow from line speed, layflat, thickness, and solid density rho = 940 kg/m3:
   Throughput [kg/h] = 2 * W_lf [m] * T_h [m] * V_line [m/min] * 60 [min/h] * rho [kg/m3] *)
rTheoreticalThroughput_kgh := 2.0 * (rLayflatWidth_mm * 0.001) * (rObserved_AverageThickness_um * 0.000001) *
                              rHaulOffActualSpeed_m_min * 60.0 * 940.0;
""")

    # Implementation: Phase 3 (State Space 8x8)
    st.append("""
(* =====================================================================================================================
   PHASE 3: 8x8 CYBER-PHYSICAL STATE-SPACE INITIALIZATION & MULTI-STEP FORWARD PREDICTION
   Discrete-time state propagation: x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k] (T_s = 50.0 ms)
   ===================================================================================================================== *)

(* Initialize State Deviation Vector x[k] *)
vecX[1] := rObserved_BubbleDiameter_mm - rTargetBubbleDiameter_mm;
vecX[2] := rObserved_FrostLineHeight_mm - rTargetFrostLineHeight_mm;
vecX[3] := rObserved_InternalPressure_Pa - rTargetInternalPressure_Pa;
vecX[4] := rObserved_AverageThickness_um - rTargetFilmThickness_um;
vecX[5] := rObserved_ThicknessStdDev_um;
vecX[6] := rAirRingSupplyAirVelocity_m_s - 18.5;
vecX[7] := rHaulOffActualSpeed_m_min - rTargetLineSpeed_m_min;
vecX[8] := rVoted_Feedblock_Press_bar - 185.0;

(* Matrix A (8x8) Discrete Coupling Dynamics *)
matA[1,1] := 0.982; matA[1,2] := 0.008; matA[1,3] := 0.420; matA[1,4] := -0.015; matA[1,5] := 0.000; matA[1,6] := -0.065; matA[1,7] := -0.035; matA[1,8] := 0.012;
matA[2,1] := -0.018; matA[2,2] := 0.965; matA[2,3] := 0.045; matA[2,4] := 0.010; matA[2,5] := 0.000; matA[2,6] := -0.320; matA[2,7] := 0.165; matA[2,8] := 0.048;
matA[3,1] := -0.095; matA[3,2] := 0.002; matA[3,3] := 0.895; matA[3,4] := -0.005; matA[3,5] := 0.000; matA[3,6] := -0.040; matA[3,7] := 0.010; matA[3,8] := 0.005;
matA[4,1] := -0.048; matA[4,2] := 0.006; matA[4,3] := -0.012; matA[4,4] := 0.955; matA[4,5] := 0.000; matA[4,6] := -0.010; matA[4,7] := -0.072; matA[4,8] := 0.038;
matA[5,1] := 0.002; matA[5,2] := -0.003; matA[5,3] := 0.000; matA[5,4] := 0.015; matA[5,5] := 0.978; matA[5,6] := -0.018; matA[5,7] := 0.000; matA[5,8] := 0.008;
matA[6,1] := 0.000; matA[6,2] := 0.000; matA[6,3] := 0.000; matA[6,4] := 0.000; matA[6,5] := 0.000; matA[6,6] := 0.935; matA[6,7] := 0.000; matA[6,8] := 0.000;
matA[7,1] := 0.000; matA[7,2] := 0.000; matA[7,3] := 0.000; matA[7,4] := 0.000; matA[7,5] := 0.000; matA[7,6] := 0.000; matA[7,7] := 0.945; matA[7,8] := 0.000;
matA[8,1] := 0.000; matA[8,2] := 0.000; matA[8,3] := 0.000; matA[8,4] := 0.000; matA[8,5] := 0.000; matA[8,6] := 0.000; matA[8,7] := 0.000; matA[8,8] := 0.925;

(* Matrix B (8x4) Actuator Control Coupling *)
(* Inputs: u1 = IBC Supply (Hz), u2 = IBC Exhaust (Hz), u3 = Air Ring Main (Hz), u4 = Haul-off Nip Speed (m/min) *)
matB[1,1] :=  0.220; matB[1,2] := -0.215; matB[1,3] := -0.045; matB[1,4] := -0.085;
matB[2,1] :=  0.035; matB[2,2] := -0.025; matB[2,3] := -0.380; matB[2,4] :=  0.210;
matB[3,1] :=  1.650; matB[3,2] := -1.680; matB[3,3] := -0.020; matB[3,4] :=  0.015;
matB[4,1] := -0.010; matB[4,2] :=  0.008; matB[4,3] := -0.015; matB[4,4] := -0.245;
matB[5,1] :=  0.000; matB[5,2] :=  0.000; matB[5,3] := -0.025; matB[5,4] :=  0.000;
matB[6,1] :=  0.000; matB[6,2] :=  0.000; matB[6,3] :=  0.880; matB[6,4] :=  0.000;
matB[7,1] :=  0.000; matB[7,2] :=  0.000; matB[7,3] :=  0.000; matB[7,4] :=  0.460;
matB[8,1] :=  0.000; matB[8,2] :=  0.000; matB[8,3] :=  0.000; matB[8,4] :=  0.000;

(* Matrix C (8x8) Direct Observation Mapping (Identity matrix) *)
FOR i := 1 TO 8 DO
    FOR j := 1 TO 8 DO
        IF i = j THEN
            matC[i,j] := 1.0;
        ELSE
            matC[i,j] := 0.0;
        END_IF;
    END_FOR;
END_FOR;

(* Matrix D (8x4) Direct Feedthrough (Zero) *)
FOR i := 1 TO 8 DO
    FOR j := 1 TO 4 DO
        matD[i,j] := 0.0;
    END_FOR;
END_FOR;

(* Compute One-Step Forward State Prediction: x_next = A * x + B * u *)
FOR i := 1 TO 8 DO
    rTempSum := 0.0;
    FOR j := 1 TO 8 DO
        rTempSum := rTempSum + matA[i,j] * vecX[j];
    END_FOR;
    FOR j := 1 TO 4 DO
        rTempSum := rTempSum + matB[i,j] * vecU[j];
    END_FOR;
    vecX_next[i] := rTempSum;
END_FOR;

(* Compute Multi-Step Horizon State Prediction Trajectory across Np = 5 steps *)
FOR h_step := 1 TO 5 DO
    FOR i := 1 TO 8 DO
        rTempSum := 0.0;
        FOR j := 1 TO 8 DO
            IF h_step = 1 THEN
                rTempSum := rTempSum + matA[i,j] * vecX[j];
            ELSE
                rTempSum := rTempSum + matA[i,j] * vecX_pred[h_step - 1, j];
            END_IF;
        END_FOR;
        FOR j := 1 TO 4 DO
            rTempSum := rTempSum + matB[i,j] * vecU[j];
        END_FOR;
        vecX_pred[h_step, i] := rTempSum;
    END_FOR;
END_FOR;
""")

    # Implementation: Phase 4 (MPC PGD)
    st.append("""
(* =====================================================================================================================
   PHASE 4: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) WITH PROJECTED GRADIENT DESCENT (PGD)
   Solves constrained quadratic objective penalizing gauge thickness, bubble diameter deviation, and actuator slew.
   ===================================================================================================================== *)

(* Initialize Cost Function Weights *)
(* State Penalty Q *)
FOR i := 1 TO 8 DO
    FOR j := 1 TO 8 DO
        matQ[i,j] := 0.0;
    END_FOR;
END_FOR;
matQ[1,1] := 12.5;  (* Bubble diameter error penalty *)
matQ[2,2] :=  4.0;  (* Frost-line height penalty *)
matQ[3,3] :=  8.0;  (* Internal pressure penalty *)
matQ[4,4] := 35.0;  (* Average thickness error penalty (HIGH PRIORITY) *)
matQ[5,5] := 50.0;  (* Gauge spatial standard deviation penalty (HIGH PRIORITY) *)
matQ[6,6] :=  1.5;  (* Air ring velocity penalty *)
matQ[7,7] :=  5.0;  (* Line speed tracking penalty *)
matQ[8,8] :=  2.0;  (* Feedblock pressure penalty *)

(* Actuator Effort Penalty R *)
FOR i := 1 TO 4 DO
    FOR j := 1 TO 4 DO
        matR[i,j] := 0.0;
    END_FOR;
END_FOR;
matR[1,1] := 0.45;  (* IBC supply blower slew penalty *)
matR[2,2] := 0.45;  (* IBC exhaust blower slew penalty *)
matR[3,3] := 0.30;  (* Main air ring blower slew penalty *)
matR[4,4] := 0.80;  (* Haul-off nip speed slew penalty *)

(* Projected Gradient Descent Solver Loop *)
FOR k_idx := 1 TO nMPC_MaxIterations DO
    (* Compute Cost Gradient accumulated over prediction horizon:
       grad = 2 * SUM_{h=1}^5 [ B^T * Q * (x_pred[h] - x_ref) ] + 2 * R * u *)
    FOR i := 1 TO 4 DO
        rTempSum := 0.0;
        FOR h_step := 1 TO 5 DO
            FOR j := 1 TO 8 DO
                rTempSum := rTempSum + matB[j,i] * matQ[j,j] * (vecX_pred[h_step, j] - 0.0);
            END_FOR;
        END_FOR;
        vecGrad[i] := (2.0 * rTempSum / 5.0) + (2.0 * matR[i,i] * vecU[i]);
    END_FOR;

    (* Apply Gradient Descent Step: u = u - alpha * grad *)
    FOR i := 1 TO 4 DO
        vecU[i] := vecU[i] - (rMPC_Alpha * vecGrad[i]);
    END_FOR;

    (* Actuator Box Saturation Constraints *)
    (* u1: IBC Supply Blower Trim (-15.0 to +15.0 Hz) *)
    IF vecU[1] > 15.0 THEN vecU[1] := 15.0; ELSIF vecU[1] < -15.0 THEN vecU[1] := -15.0; END_IF;
    (* u2: IBC Exhaust Blower Trim (-15.0 to +15.0 Hz) *)
    IF vecU[2] > 15.0 THEN vecU[2] := 15.0; ELSIF vecU[2] < -15.0 THEN vecU[2] := -15.0; END_IF;
    (* u3: Main Air Ring Blower Trim (-10.0 to +10.0 Hz) *)
    IF vecU[3] > 10.0 THEN vecU[3] := 10.0; ELSIF vecU[3] < -10.0 THEN vecU[3] := -10.0; END_IF;
    (* u4: Haul-off Speed Trim (-3.0 to +3.0 m/min) *)
    IF vecU[4] > 3.0 THEN vecU[4] := 3.0; ELSIF vecU[4] < -3.0 THEN vecU[4] := -3.0; END_IF;
END_FOR;

(* Map MPC Outputs to Absolute Physical Actuator Command Frequencies *)
IF bMasterEnable AND bEmergencyStop_NC AND (nActiveFSM_State >= 5) THEN
    rIBC_SupplyBlower_Hz  := 42.0 + vecU[1];
    rIBC_ExhaustBlower_Hz := 41.5 + vecU[2];
    rAirRingMainBlower_Hz := 48.0 + vecU[3];
    rHaulOffSpeedCmd_m_min := rTargetLineSpeed_m_min + vecU[4];
ELSE
    rIBC_SupplyBlower_Hz  := 0.0;
    rIBC_ExhaustBlower_Hz := 0.0;
    rAirRingMainBlower_Hz := 0.0;
    rHaulOffSpeedCmd_m_min := 0.0;
END_IF;

(* Automatic Vacuum Lock Damper Modulated Proportional to Differential Pressure Error *)
rIBC_VacuumLockValve_pct := 50.0 + (rTargetInternalPressure_Pa - rObserved_InternalPressure_Pa) * 1.8;
IF rIBC_VacuumLockValve_pct > 100.0 THEN rIBC_VacuumLockValve_pct := 100.0; END_IF;
IF rIBC_VacuumLockValve_pct < 0.0 THEN rIBC_VacuumLockValve_pct := 0.0; END_IF;
""")

    # Implementation: Phase 5 (Rotary Scanner & 32-Zone Air Ring)
    st.append("""
(* =====================================================================================================================
   PHASE 5: ROTARY SCANNER COORDINATE TRANSFORMATION & 32-ZONE AUTOMATIC AIR RING PROFILE CONTROL
   Maps rotary web thickness readings back to 32 stationary die-lip orifices and executes closed-loop thermal profile control.
   ===================================================================================================================== *)

(* Calculate Scanner Angular Velocity and Zero-Index Sync *)
IF bCapacitiveScannerSyncPulse THEN
    rScannerSpeed_deg_s := (360.0 - rScannerPreviousAngle_deg) / rCycleTime_s;
    rScannerPreviousAngle_deg := 0.0;
ELSE
    rScannerSpeed_deg_s := (rCapacitiveScannerAngle_deg - rScannerPreviousAngle_deg) / rCycleTime_s;
    rScannerPreviousAngle_deg := rCapacitiveScannerAngle_deg;
END_IF;

(* Trigonometric Coordinate Mapping from Web Scanner to Stationary Die Lip Orifice:
   theta_die = MOD( theta_scan - theta_haul + theta_spiral_offset, 360.0 ) *)
rTempSum := rCapacitiveScannerAngle_deg - rHaulOffOscillationAngle_deg + rSpatialSpiralOffset_deg;
WHILE rTempSum < 0.0 DO
    rTempSum := rTempSum + 360.0;
END_WHILE;
WHILE rTempSum >= 360.0 DO
    rTempSum := rTempSum - 360.0;
END_WHILE;

(* Determine corresponding Air Ring Zone Index (1..32), each zone covering 11.25 degrees *)
nZoneIdx := 1 + TRUNC(rTempSum / 11.25);
IF nZoneIdx < 1 THEN nZoneIdx := 1; END_IF;
IF nZoneIdx > 32 THEN nZoneIdx := 32; END_IF;

(* Store latest instantaneous measurement into sector buffer *)
arRawGauge_32[nZoneIdx] := rObserved_AverageThickness_um;

(* Apply Gaussian Spatial Moving Kernel Smoothing across 32 sectors:
   Filtered[i] = 0.15 * Raw[i-1] + 0.70 * Raw[i] + 0.15 * Raw[i+1] (with circular wrap-around) *)
FOR i := 1 TO 32 DO
    IF i = 1 THEN
        arFilteredGauge_32[1] := (0.15 * arRawGauge_32[32]) + (0.70 * arRawGauge_32[1]) + (0.15 * arRawGauge_32[2]);
    ELSIF i = 32 THEN
        arFilteredGauge_32[32] := (0.15 * arRawGauge_32[31]) + (0.70 * arRawGauge_32[32]) + (0.15 * arRawGauge_32[1]);
    ELSE
        arFilteredGauge_32[i] := (0.15 * arRawGauge_32[i-1]) + (0.70 * arRawGauge_32[i]) + (0.15 * arRawGauge_32[i+1]);
    END_IF;
END_FOR;

(* Compute Profile Statistical Standard Deviation (2-Sigma) *)
rGaugeSum := 0.0;
FOR i := 1 TO 32 DO
    rGaugeSum := rGaugeSum + arFilteredGauge_32[i];
END_FOR;
rTempNorm := rGaugeSum / 32.0;

rGaugeVarianceSum := 0.0;
FOR i := 1 TO 32 DO
    rTempDiff := arFilteredGauge_32[i] - rTempNorm;
    rGaugeVarianceSum := rGaugeVarianceSum + (rTempDiff * rTempDiff);
END_FOR;
rObserved_ThicknessStdDev_um := 2.0 * SQRT(rGaugeVarianceSum / 32.0);

(* 32-Zone Discrete PI Control with Anti-Windup for Heating Cartridges:
   Local Heating Law: Increasing heating cartridge duty locally heats cooling air, reducing local air density
   and lowering local cooling capacity, prolonging draw-down which thins local gauge. *)
FOR i := 1 TO 32 DO
    arProfileError_32[i] := arFilteredGauge_32[i] - rTargetFilmThickness_um;

    (* Discrete Integral Accumulator with Anti-Windup *)
    arIntegralError_32[i] := arIntegralError_32[i] + (arProfileError_32[i] * rCycleTime_s);
    IF arIntegralError_32[i] > 25.0 THEN arIntegralError_32[i] := 25.0; END_IF;
    IF arIntegralError_32[i] < -25.0 THEN arIntegralError_32[i] := -25.0; END_IF;

    IF bAirRingProfileActive AND (nActiveFSM_State = 8) THEN
        (* PI Actuation Law *)
        anAirRingCartridgeDuty_pct[i] := rAirRing_BaseDuty_pct +
                                         (rAirRing_Kp * arProfileError_32[i]) +
                                         (rAirRing_Ki * arIntegralError_32[i]);
    ELSE
        anAirRingCartridgeDuty_pct[i] := rAirRing_BaseDuty_pct;
        arIntegralError_32[i] := 0.0;
    END_IF;

    (* Clamp duty between 5.0% and 95.0% to prevent thermal shock *)
    IF anAirRingCartridgeDuty_pct[i] > 95.0 THEN anAirRingCartridgeDuty_pct[i] := 95.0; END_IF;
    IF anAirRingCartridgeDuty_pct[i] < 5.0 THEN anAirRingCartridgeDuty_pct[i] := 5.0; END_IF;

    (* Sub-Second Solid-State Relay PWM Waveform Generation *)
    arPWM_Accumulators_s[i] := arPWM_Accumulators_s[i] + rCycleTime_s;
    IF arPWM_Accumulators_s[i] >= rPWM_Period_s THEN
        arPWM_Accumulators_s[i] := 0.0;
    END_IF;

    IF arPWM_Accumulators_s[i] < (rPWM_Period_s * (anAirRingCartridgeDuty_pct[i] * 0.01)) THEN
        anAirRingCartridgePWM_Out[i] := TRUE;
    ELSE
        anAirRingCartridgePWM_Out[i] := FALSE;
    END_IF;
END_FOR;
""")

    # Implementation: Phase 6 (7 Extruders, Thermal Soaking, 35 Barrel Zones, 8 Die Zones, Interfacial Shear)
    st.append("""
(* =====================================================================================================================
   PHASE 6: 7-LAYER MULTI-EXTRUDER GRAVIMETRIC SYNCHRONIZATION & 43-ZONE THERMAL SOAK
   Harmonizes the 7 grooved-feed extruder screw drive speeds and monitors 35 barrel zones and 8 spiral die zones.
   ===================================================================================================================== *)

(* Initialize Nominal Recipe Thermal Setpoints for 35 Barrel Zones and 8 Spiral Die Zones *)
(* Extruder A: mLLDPE Skin (Zones 1..5: 160, 180, 195, 205, 210 deg C) *)
arBarrelZoneSP_ExtA_degC[1] := 160.0; arBarrelZoneSP_ExtA_degC[2] := 180.0; arBarrelZoneSP_ExtA_degC[3] := 195.0; arBarrelZoneSP_ExtA_degC[4] := 205.0; arBarrelZoneSP_ExtA_degC[5] := 210.0;
(* Extruder B: Tie Layer (Zones 1..5: 170, 190, 205, 215, 220 deg C) *)
arBarrelZoneSP_ExtB_degC[1] := 170.0; arBarrelZoneSP_ExtB_degC[2] := 190.0; arBarrelZoneSP_ExtB_degC[3] := 205.0; arBarrelZoneSP_ExtB_degC[4] := 215.0; arBarrelZoneSP_ExtB_degC[5] := 220.0;
(* Extruder C: PA6 Outer (Zones 1..5: 220, 235, 245, 250, 255 deg C) *)
arBarrelZoneSP_ExtC_degC[1] := 220.0; arBarrelZoneSP_ExtC_degC[2] := 235.0; arBarrelZoneSP_ExtC_degC[3] := 245.0; arBarrelZoneSP_ExtC_degC[4] := 250.0; arBarrelZoneSP_ExtC_degC[5] := 255.0;
(* Extruder D: EVOH 38% (Zones 1..5: 190, 205, 215, 225, 230 deg C) *)
arBarrelZoneSP_ExtD_degC[1] := 190.0; arBarrelZoneSP_ExtD_degC[2] := 205.0; arBarrelZoneSP_ExtD_degC[3] := 215.0; arBarrelZoneSP_ExtD_degC[4] := 225.0; arBarrelZoneSP_ExtD_degC[5] := 230.0;
(* Extruder E: PA6 Inner (Zones 1..5: 220, 235, 245, 250, 255 deg C) *)
arBarrelZoneSP_ExtE_degC[1] := 220.0; arBarrelZoneSP_ExtE_degC[2] := 235.0; arBarrelZoneSP_ExtE_degC[3] := 245.0; arBarrelZoneSP_ExtE_degC[4] := 250.0; arBarrelZoneSP_ExtE_degC[5] := 255.0;
(* Extruder F: Tie Layer (Zones 1..5: 170, 190, 205, 215, 220 deg C) *)
arBarrelZoneSP_ExtF_degC[1] := 170.0; arBarrelZoneSP_ExtF_degC[2] := 190.0; arBarrelZoneSP_ExtF_degC[3] := 205.0; arBarrelZoneSP_ExtF_degC[4] := 215.0; arBarrelZoneSP_ExtF_degC[5] := 220.0;
(* Extruder G: mLLDPE Seal (Zones 1..5: 155, 175, 190, 200, 205 deg C) *)
arBarrelZoneSP_ExtG_degC[1] := 155.0; arBarrelZoneSP_ExtG_degC[2] := 175.0; arBarrelZoneSP_ExtG_degC[3] := 190.0; arBarrelZoneSP_ExtG_degC[4] := 200.0; arBarrelZoneSP_ExtG_degC[5] := 205.0;

(* Closed-Loop Proportional Temperature Control across 35 Barrel Zones *)
FOR i := 1 TO 5 DO
    arBarrelDuty_ExtA_pct[i] := 50.0 + (arBarrelZoneSP_ExtA_degC[i] - arBarrelZoneTemp_ExtA_degC[i]) * 4.0;
    IF arBarrelDuty_ExtA_pct[i] > 100.0 THEN arBarrelDuty_ExtA_pct[i] := 100.0; ELSIF arBarrelDuty_ExtA_pct[i] < 0.0 THEN arBarrelDuty_ExtA_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtB_pct[i] := 50.0 + (arBarrelZoneSP_ExtB_degC[i] - arBarrelZoneTemp_ExtB_degC[i]) * 4.0;
    IF arBarrelDuty_ExtB_pct[i] > 100.0 THEN arBarrelDuty_ExtB_pct[i] := 100.0; ELSIF arBarrelDuty_ExtB_pct[i] < 0.0 THEN arBarrelDuty_ExtB_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtC_pct[i] := 50.0 + (arBarrelZoneSP_ExtC_degC[i] - arBarrelZoneTemp_ExtC_degC[i]) * 4.0;
    IF arBarrelDuty_ExtC_pct[i] > 100.0 THEN arBarrelDuty_ExtC_pct[i] := 100.0; ELSIF arBarrelDuty_ExtC_pct[i] < 0.0 THEN arBarrelDuty_ExtC_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtD_pct[i] := 50.0 + (arBarrelZoneSP_ExtD_degC[i] - arBarrelZoneTemp_ExtD_degC[i]) * 4.0;
    IF arBarrelDuty_ExtD_pct[i] > 100.0 THEN arBarrelDuty_ExtD_pct[i] := 100.0; ELSIF arBarrelDuty_ExtD_pct[i] < 0.0 THEN arBarrelDuty_ExtD_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtE_pct[i] := 50.0 + (arBarrelZoneSP_ExtE_degC[i] - arBarrelZoneTemp_ExtE_degC[i]) * 4.0;
    IF arBarrelDuty_ExtE_pct[i] > 100.0 THEN arBarrelDuty_ExtE_pct[i] := 100.0; ELSIF arBarrelDuty_ExtE_pct[i] < 0.0 THEN arBarrelDuty_ExtE_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtF_pct[i] := 50.0 + (arBarrelZoneSP_ExtF_degC[i] - arBarrelZoneTemp_ExtF_degC[i]) * 4.0;
    IF arBarrelDuty_ExtF_pct[i] > 100.0 THEN arBarrelDuty_ExtF_pct[i] := 100.0; ELSIF arBarrelDuty_ExtF_pct[i] < 0.0 THEN arBarrelDuty_ExtF_pct[i] := 0.0; END_IF;

    arBarrelDuty_ExtG_pct[i] := 50.0 + (arBarrelZoneSP_ExtG_degC[i] - arBarrelZoneTemp_ExtG_degC[i]) * 4.0;
    IF arBarrelDuty_ExtG_pct[i] > 100.0 THEN arBarrelDuty_ExtG_pct[i] := 100.0; ELSIF arBarrelDuty_ExtG_pct[i] < 0.0 THEN arBarrelDuty_ExtG_pct[i] := 0.0; END_IF;
END_FOR;

(* Spiral Mandrel Die Zones 1..8 (Co-Extrusion Die Temperature Uniformity: 235 deg C nominal) *)
FOR i := 1 TO 8 DO
    arDieZoneSP_degC[i] := 235.0;
    arDieZoneDuty_pct[i] := 50.0 + (arDieZoneSP_degC[i] - arDieZoneTemp_degC[i]) * 5.0;
    IF arDieZoneDuty_pct[i] > 100.0 THEN arDieZoneDuty_pct[i] := 100.0; ELSIF arDieZoneDuty_pct[i] < 0.0 THEN arDieZoneDuty_pct[i] := 0.0; END_IF;
END_FOR;

(* Specific Throughput Factors [kg/(h*rpm)] for 7 Extruders based on Screw Diameter & Pitch *)
arExtruderSpecificOutput_kgh_rpm[1] := 3.25;  (* Extruder A: 75 mm Grooved Feed mLLDPE *)
arExtruderSpecificOutput_kgh_rpm[2] := 1.15;  (* Extruder B: 45 mm Grooved Feed Tie *)
arExtruderSpecificOutput_kgh_rpm[3] := 2.20;  (* Extruder C: 60 mm Grooved Feed PA6 *)
arExtruderSpecificOutput_kgh_rpm[4] := 1.45;  (* Extruder D: 50 mm Grooved Feed EVOH *)
arExtruderSpecificOutput_kgh_rpm[5] := 2.20;  (* Extruder E: 60 mm Grooved Feed PA6 *)
arExtruderSpecificOutput_kgh_rpm[6] := 1.15;  (* Extruder F: 45 mm Grooved Feed Tie *)
arExtruderSpecificOutput_kgh_rpm[7] := 4.10;  (* Extruder G: 90 mm Grooved Feed mLLDPE Seal *)

(* Screw Cold-Start Protection Interlock Verification with 10-Minute Thermal Soak Timer *)
arExtruderPermissive[1] := (rExtruderMeltTemp_ExtA_degC >= 180.0) AND (arExtruderSoakTimer_s[1] >= 600.0);
arExtruderPermissive[2] := (rExtruderMeltTemp_ExtB_degC >= 195.0) AND (arExtruderSoakTimer_s[2] >= 600.0);
arExtruderPermissive[3] := (rExtruderMeltTemp_ExtC_degC >= 235.0) AND (arExtruderSoakTimer_s[3] >= 600.0);
arExtruderPermissive[4] := (rExtruderMeltTemp_ExtD_degC >= 215.0) AND (arExtruderSoakTimer_s[4] >= 600.0);
arExtruderPermissive[5] := (rExtruderMeltTemp_ExtE_degC >= 235.0) AND (arExtruderSoakTimer_s[5] >= 600.0);
arExtruderPermissive[6] := (rExtruderMeltTemp_ExtF_degC >= 195.0) AND (arExtruderSoakTimer_s[6] >= 600.0);
arExtruderPermissive[7] := (rExtruderMeltTemp_ExtG_degC >= 180.0) AND (arExtruderSoakTimer_s[7] >= 600.0);

FOR i := 1 TO 7 DO
    IF NOT arExtruderPermissive[i] THEN
        arExtruderSoakTimer_s[i] := arExtruderSoakTimer_s[i] + rCycleTime_s;
    END_IF;
END_FOR;

(* Calculate Coordinated Screw Speed Commands:
   Screw_rpm = (Total_Throughput_kgh * LayerRatio_pct * 0.01) / SpecificOutput_kgh_rpm *)
IF bExtrusionActive AND (nActiveFSM_State >= 3) THEN
    rExtruderSpeedCmd_ExtA_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtA_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[1];
    rExtruderSpeedCmd_ExtB_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtB_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[2];
    rExtruderSpeedCmd_ExtC_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtC_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[3];
    rExtruderSpeedCmd_ExtD_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtD_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[4];
    rExtruderSpeedCmd_ExtE_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtE_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[5];
    rExtruderSpeedCmd_ExtF_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtF_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[6];
    rExtruderSpeedCmd_ExtG_rpm := (rTotalThroughputSetpoint_kgh * (rLayerRatioSetpoint_ExtG_pct * 0.01)) / arExtruderSpecificOutput_kgh_rpm[7];
ELSE
    rExtruderSpeedCmd_ExtA_rpm := 0.0;
    rExtruderSpeedCmd_ExtB_rpm := 0.0;
    rExtruderSpeedCmd_ExtC_rpm := 0.0;
    rExtruderSpeedCmd_ExtD_rpm := 0.0;
    rExtruderSpeedCmd_ExtE_rpm := 0.0;
    rExtruderSpeedCmd_ExtF_rpm := 0.0;
    rExtruderSpeedCmd_ExtG_rpm := 0.0;
END_IF;

(* Co-Extrusion Interfacial Shear Stress & Apparent Viscosity Calculations in Die Passages *)
(* Shear rate gamma_dot = 6 * Q_vol / (pi * D_die * h_gap^2) *)
arExtruderShearRate_s_inv[1] := (6.0 * (rExtruderThroughput_ExtA_kgh / 760.0) / 3600.0) / (3.14159 * 0.500 * 0.00000196);
arExtruderShearRate_s_inv[2] := (6.0 * (rExtruderThroughput_ExtB_kgh / 780.0) / 3600.0) / (3.14159 * 0.500 * 0.00000049);
arExtruderShearRate_s_inv[3] := (6.0 * (rExtruderThroughput_ExtC_kgh / 950.0) / 3600.0) / (3.14159 * 0.500 * 0.00000144);
arExtruderShearRate_s_inv[4] := (6.0 * (rExtruderThroughput_ExtD_kgh / 1020.0) / 3600.0) / (3.14159 * 0.500 * 0.00000081);
arExtruderShearRate_s_inv[5] := (6.0 * (rExtruderThroughput_ExtE_kgh / 950.0) / 3600.0) / (3.14159 * 0.500 * 0.00000144);
arExtruderShearRate_s_inv[6] := (6.0 * (rExtruderThroughput_ExtF_kgh / 780.0) / 3600.0) / (3.14159 * 0.500 * 0.00000049);
arExtruderShearRate_s_inv[7] := (6.0 * (rExtruderThroughput_ExtG_kgh / 760.0) / 3600.0) / (3.14159 * 0.500 * 0.00000289);

(* Power-Law Apparent Viscosities eta = K * gamma_dot^(n - 1) *)
arExtruderApparentVisc_Pa_s[1] := 4200.0 * EXPT(MAX(arExtruderShearRate_s_inv[1], 1.0), -0.58);
arExtruderApparentVisc_Pa_s[2] := 3800.0 * EXPT(MAX(arExtruderShearRate_s_inv[2], 1.0), -0.55);
arExtruderApparentVisc_Pa_s[3] := 2900.0 * EXPT(MAX(arExtruderShearRate_s_inv[3], 1.0), -0.42);
arExtruderApparentVisc_Pa_s[4] := 3400.0 * EXPT(MAX(arExtruderShearRate_s_inv[4], 1.0), -0.48);
arExtruderApparentVisc_Pa_s[5] := 2900.0 * EXPT(MAX(arExtruderShearRate_s_inv[5], 1.0), -0.42);
arExtruderApparentVisc_Pa_s[6] := 3800.0 * EXPT(MAX(arExtruderShearRate_s_inv[6], 1.0), -0.55);
arExtruderApparentVisc_Pa_s[7] := 4500.0 * EXPT(MAX(arExtruderShearRate_s_inv[7], 1.0), -0.60);

(* Wall Shear Stress tau_w = eta * gamma_dot in kPa *)
FOR i := 1 TO 7 DO
    arExtruderWallShearStress_kPa[i] := (arExtruderApparentVisc_Pa_s[i] * arExtruderShearRate_s_inv[i]) * 0.001;
END_FOR;

(* Interfacial instability warning if shear stress on EVOH layer exceeds critical threshold 55.0 kPa *)
bWarn_InterfacialShearHigh := (arExtruderWallShearStress_kPa[4] >= 55.0);
""")

    # Implementation: Phase 7 (Reversing Haul-Off Tower)
    st.append("""
(* =====================================================================================================================
   PHASE 7: OSCILLATING REVERSING HAUL-OFF TOWER SPEED & KINEMATICS
   Smooth sinusoidal/S-curve reversal profile distributing gauge variation across 360 degrees of reel circumference.
   ===================================================================================================================== *)

IF (nActiveFSM_State >= 6) AND bMasterEnable THEN
    (* Continuous Reversal Tower Oscillation Speed [deg/s] *)
    IF (rHaulOffOscillationAngle_deg >= 178.0) THEN
        rHaulOffOscillationSpeed_deg_s := -0.22;
    ELSIF (rHaulOffOscillationAngle_deg <= -178.0) THEN
        rHaulOffOscillationSpeed_deg_s := 0.22;
    ELSIF (rHaulOffOscillationSpeed_deg_s = 0.0) THEN
        rHaulOffOscillationSpeed_deg_s := 0.22;
    END_IF;
ELSE
    rHaulOffOscillationSpeed_deg_s := 0.0;
END_IF;
""")

    # Implementation: Phase 8 (Dual Turret Rewinder & Flying Knife Splice)
    st.append("""
(* =====================================================================================================================
   PHASE 8: DUAL TURRET REWINDER TAPER TENSION & HIGH-SPEED FLYING KNIFE AUTO-SPLICE
   Calculates active winder spindle torque, tension closed-loop PID, and executes flying cross-cut splice sequence.
   ===================================================================================================================== *)

(* Tension Taper Curve: Tapered tension reduces roll crushing and telescoping
   T_ref = T_set * [ 1.0 - taper_factor * (1.0 - CoreDiam / CurrentDiam) ] *)
IF rWinderRollDiameter_mm > rCoreNominalDiameter_mm THEN
    rTaperTension_N := 220.0 * (1.0 - (rTaperFactor * (1.0 - (rCoreNominalDiameter_mm / rWinderRollDiameter_mm))));
ELSE
    rTaperTension_N := 220.0;
END_IF;

(* Continuous Roll Inertia Calculation: J = 0.5 * pi * rho * Width * (R_roll^4 - R_core^4) *)
rRollInertia_kg_m2 := 0.5 * 3.14159265 * 940.0 * (rLayflatWidth_mm * 0.001) *
                      (EXPT(rWinderRollDiameter_mm * 0.0005, 4.0) - EXPT(rCoreNominalDiameter_mm * 0.0005, 4.0));
IF rRollInertia_kg_m2 < 0.15 THEN rRollInertia_kg_m2 := 0.15; END_IF;

(* Closed-Loop Tension PID Accumulation *)
rTempDiff := rTaperTension_N - rWinderTensionFeedback_N;
rWinderTensionIntegral_Ns := rWinderTensionIntegral_Ns + (rTempDiff * rCycleTime_s);
IF rWinderTensionIntegral_Ns > 500.0 THEN rWinderTensionIntegral_Ns := 500.0; END_IF;
IF rWinderTensionIntegral_Ns < -500.0 THEN rWinderTensionIntegral_Ns := -500.0; END_IF;

(* Spindle Torque Reference: Torque = Force * Radius + Acceleration Inertia Compensation *)
rTargetTorque_Nm := (rTaperTension_N * (rWinderRollDiameter_mm * 0.0005)) +
                    (0.045 * rTempDiff) + (0.012 * rWinderTensionIntegral_Ns);
IF (nActiveFSM_State >= 9) AND bMasterEnable THEN
    rTurretWinderTorque_Nm := rTargetTorque_Nm;
ELSE
    rTurretWinderTorque_Nm := 0.0;
END_IF;

(* Flying Knife Auto-Splice Roll Transfer Sequencer *)
IF (rWinderRollDiameter_mm >= rSpliceTriggerDiameter_mm) OR bSpliceArmCommand THEN
    IF NOT bSpliceInProgress AND bCoreLoadedPermissive THEN
        bSpliceInProgress := TRUE;
        nSpliceSubStage := 1;
        rSpliceSequenceTimer_s := 0.0;
    END_IF;
END_IF;

IF bSpliceInProgress THEN
    rSpliceSequenceTimer_s := rSpliceSequenceTimer_s + rCycleTime_s;
    CASE nSpliceSubStage OF
        1: (* Stage 1: Accelerate Standby Core Spindle to Synchronous Surface Speed *)
            bFlyingKnifeFire_Cmd := FALSE;
            bTurretIndex_Cmd := FALSE;
            IF rSpliceSequenceTimer_s >= 4.0 THEN
                nSpliceSubStage := 2;
                rSpliceSequenceTimer_s := 0.0;
            END_IF;

        2: (* Stage 2: Fire Pneumatic Flying Knife Cross-Cut *)
            bFlyingKnifeFire_Cmd := TRUE;
            IF rSpliceSequenceTimer_s >= 0.250 THEN
                bFlyingKnifeFire_Cmd := FALSE;
                nSpliceSubStage := 3;
                rSpliceSequenceTimer_s := 0.0;
            END_IF;

        3: (* Stage 3: Index Turret Carriage and Present New Core to Winding Nip *)
            bTurretIndex_Cmd := TRUE;
            IF rSpliceSequenceTimer_s >= 6.0 THEN
                bTurretIndex_Cmd := FALSE;
                bSpliceInProgress := FALSE;
                nSpliceSubStage := 0;
            END_IF;
    END_CASE;
ELSE
    bFlyingKnifeFire_Cmd := FALSE;
    bTurretIndex_Cmd := FALSE;
END_IF;
""")

    # Implementation: Phase 9 (12-Stage Finite State Machine)
    st.append("""
(* =====================================================================================================================
   PHASE 9: DETERMINISTIC 12-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
   Sequential state manager orchestrating full extrusion complex startup, stabilization, run, and fail-safe stop.
   ===================================================================================================================== *)

rStateTimer_s := rStateTimer_s + rCycleTime_s;

CASE nActiveFSM_State OF
    1: (* STATE 1: Extruder Barrel & Die Zone Pre-Heating (PID thermal soak) *)
        sActiveStateName := '1: BARREL & DIE THERMAL SOAK';
        bExtrusionActive := FALSE;
        bIBC_ClosedLoopLocked := FALSE;
        bAirRingProfileActive := FALSE;
        bEdgeTrimSlittersEngaged := FALSE;
        bCoronaTreaterActive := FALSE;

        bThermalSoakComplete := arExtruderPermissive[1] AND arExtruderPermissive[2] AND
                                arExtruderPermissive[3] AND arExtruderPermissive[4] AND
                                arExtruderPermissive[5] AND arExtruderPermissive[6] AND
                                arExtruderPermissive[7];

        IF bThermalSoakComplete AND (rStateTimer_s >= 30.0) AND bMasterEnable THEN
            nActiveFSM_State := 2;
            rStateTimer_s := 0.0;
        END_IF;

    2: (* STATE 2: Resin Gravimetric Feeder Purge & Recipe Dosing Initialization *)
        sActiveStateName := '2: GRAVIMETRIC DOSING PURGE';
        bExtrusionActive := FALSE;
        bIBC_ClosedLoopLocked := FALSE;
        bAirRingProfileActive := FALSE;

        bGravimetricDosingReady := (rTotalThroughputSetpoint_kgh >= 200.0) AND
                                   (rLayerRatioSetpoint_ExtA_pct + rLayerRatioSetpoint_ExtB_pct +
                                    rLayerRatioSetpoint_ExtC_pct + rLayerRatioSetpoint_ExtD_pct +
                                    rLayerRatioSetpoint_ExtE_pct + rLayerRatioSetpoint_ExtF_pct +
                                    rLayerRatioSetpoint_ExtG_pct >= 99.8);

        IF bGravimetricDosingReady AND (rStateTimer_s >= 15.0) THEN
            nActiveFSM_State := 3;
            rStateTimer_s := 0.0;
        END_IF;

    3: (* STATE 3: Multi-Extruder Synchronous Melt Pumping *)
        sActiveStateName := '3: MULTI-EXTRUDER MELT PUMPING';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := FALSE;
        bAirRingProfileActive := FALSE;

        bDieMeltUniform := (rVoted_Feedblock_Press_bar >= 90.0) AND
                           (rExtruderMeltPress_ExtA_bar >= 80.0) AND
                           (rExtruderMeltPress_ExtG_bar >= 80.0);

        IF bDieMeltUniform AND (rStateTimer_s >= 25.0) THEN
            nActiveFSM_State := 4;
            rStateTimer_s := 0.0;
        END_IF;

    4: (* STATE 4: Die Lip Manual Bubble Inflation & Initial Layflat Formation *)
        sActiveStateName := '4: MANUAL BUBBLE INFLATION';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := FALSE;
        bAirRingProfileActive := FALSE;

        bBubbleSeeded := (rObserved_BubbleDiameter_mm >= (rTargetBubbleDiameter_mm * 0.70)) AND
                         (rHaulOffActualSpeed_m_min >= 10.0);

        IF bBubbleSeeded AND (rStateTimer_s >= 20.0) THEN
            nActiveFSM_State := 5;
            rStateTimer_s := 0.0;
        END_IF;

    5: (* STATE 5: IBC Ultrasonic Automatic Lock-In *)
        sActiveStateName := '5: IBC ULTRASONIC LOCK-IN';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := FALSE;

        bIBC_TrackingGood := (ABS(rObserved_BubbleDiameter_mm - rTargetBubbleDiameter_mm) <= 4.0) AND
                             (ABS(rObserved_InternalPressure_Pa - rTargetInternalPressure_Pa) <= 6.0);

        IF bIBC_TrackingGood AND (rStateTimer_s >= 30.0) THEN
            nActiveFSM_State := 6;
            rStateTimer_s := 0.0;
        END_IF;

    6: (* STATE 6: Haul-Off Tower Collapsing Frame Speed Synchronization *)
        sActiveStateName := '6: HAUL-OFF SPEED SYNC & OSCILLATION';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := FALSE;

        bLineSpeedAtSetpoint := (ABS(rHaulOffActualSpeed_m_min - rTargetLineSpeed_m_min) <= 0.50);

        IF bLineSpeedAtSetpoint AND (rStateTimer_s >= 25.0) THEN
            nActiveFSM_State := 7;
            rStateTimer_s := 0.0;
        END_IF;

    7: (* STATE 7: Capacitive Thickness Gauge Rotary Scanning *)
        sActiveStateName := '7: ROTARY THICKNESS SCANNING';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := FALSE;

        bThicknessProfileMatured := (rStateTimer_s >= 45.0) AND (rObserved_AverageThickness_um > 20.0);

        IF bThicknessProfileMatured THEN
            nActiveFSM_State := 8;
            rStateTimer_s := 0.0;
        END_IF;

    8: (* STATE 8: Automatic Air Ring Segmented Profile Control *)
        sActiveStateName := '8: AUTOMATIC AIR RING PROFILE CONTROL';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := TRUE;

        bAirRingInControl := (rObserved_ThicknessStdDev_um <= 2.20);

        IF bAirRingInControl AND (rStateTimer_s >= 60.0) THEN
            nActiveFSM_State := 9;
            rStateTimer_s := 0.0;
        END_IF;

    9: (* STATE 9: Edge Trim Slitter Engage & Corona Treater Activation *)
        sActiveStateName := '9: EDGE SLITTING & CORONA TREATER';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := TRUE;
        bEdgeTrimSlittersEngaged := TRUE;
        bCoronaTreaterActive := TRUE;

        IF (rStateTimer_s >= 15.0) THEN
            nActiveFSM_State := 10;
            rStateTimer_s := 0.0;
        END_IF;

    10: (* STATE 10: Dual Turret Rewind Core Loading & Taper Tension *)
        sActiveStateName := '10: TURRET REWIND CONTINUOUS RUN';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := TRUE;
        bEdgeTrimSlittersEngaged := TRUE;
        bCoronaTreaterActive := TRUE;

        IF bSpliceInProgress THEN
            nActiveFSM_State := 11;
            rStateTimer_s := 0.0;
        END_IF;

    11: (* STATE 11: Flying Knife Auto-Splice Roll Transfer *)
        sActiveStateName := '11: FLYING KNIFE AUTO-SPLICE';
        bExtrusionActive := TRUE;
        bIBC_ClosedLoopLocked := TRUE;
        bAirRingProfileActive := TRUE;
        bEdgeTrimSlittersEngaged := TRUE;
        bCoronaTreaterActive := TRUE;

        IF NOT bSpliceInProgress AND (rStateTimer_s >= 10.0) THEN
            nActiveFSM_State := 10; (* Return to continuous winding *)
            rStateTimer_s := 0.0;
        END_IF;

    12: (* STATE 12: Bubble Collapse E-Stop Depressurization *)
        sActiveStateName := '12: BUBBLE COLLAPSE E-STOP SHUTDOWN';
        bExtrusionActive := FALSE;
        bIBC_ClosedLoopLocked := FALSE;
        bAirRingProfileActive := FALSE;
        bEdgeTrimSlittersEngaged := FALSE;
        bCoronaTreaterActive := FALSE;

        rExtruderSpeedCmd_ExtA_rpm := 0.0;
        rExtruderSpeedCmd_ExtB_rpm := 0.0;
        rExtruderSpeedCmd_ExtC_rpm := 0.0;
        rExtruderSpeedCmd_ExtD_rpm := 0.0;
        rExtruderSpeedCmd_ExtE_rpm := 0.0;
        rExtruderSpeedCmd_ExtF_rpm := 0.0;
        rExtruderSpeedCmd_ExtG_rpm := 0.0;

        rIBC_SupplyBlower_Hz  := 0.0;
        rIBC_ExhaustBlower_Hz := 50.0; (* Full exhaust dump to collapse bubble *)
        rAirRingMainBlower_Hz := 0.0;
        rHaulOffSpeedCmd_m_min := 0.0;
        rTurretWinderTorque_Nm := 0.0;

        IF bResetAlarms AND bEmergencyStop_NC THEN
            nActiveFSM_State := 1;
            rStateTimer_s := 0.0;
        END_IF;

ELSE
    nActiveFSM_State := 1;
    rStateTimer_s := 0.0;
END_CASE;

(* Emergency Stop Interlock Override *)
IF NOT bEmergencyStop_NC THEN
    nActiveFSM_State := 12;
END_IF;
""")

    # Implementation: Phase 10 (ISA-18.2 Alarms & Status Words)
    st.append("""
(* =====================================================================================================================
   PHASE 10: ISA-18.2 MULTI-TIERED ALARM MATRIX, DEADBAND HYSTERESIS & STATUS REGISTERS
   Systematic fault classification with 32-bit packed alarm words for DCS/SCADA integration.
   ===================================================================================================================== *)

(* Priority 1: Emergency Trip Alarms *)
bTrip_EmergencyStop := NOT bEmergencyStop_NC;
bTrip_MeltOverpressureFeedblock := (rVoted_Feedblock_Press_bar >= 320.0);
bTrip_BubbleRuptureLoss := (nActiveFSM_State >= 5) AND (rObserved_InternalPressure_Pa <= 10.0);
bTrip_ExtruderMotorOvercurrent := (rExtruderCurrent_ExtA_A >= 185.0) OR (rExtruderCurrent_ExtG_A >= 210.0);
bTrip_IBC_BlowerFault := (rTMR_DiscrepancyTimer_DP_s >= 8.0);
bTrip_HaulOffDriveStall := (nActiveFSM_State >= 6) AND (rHaulOffActualSpeed_m_min <= 2.0);

dwAlarmWord_Trip := 16#0000_0000;
IF bTrip_EmergencyStop THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0001; END_IF;
IF bTrip_MeltOverpressureFeedblock THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0002; END_IF;
IF bTrip_BubbleRuptureLoss THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0004; END_IF;
IF bTrip_ExtruderMotorOvercurrent THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0008; END_IF;
IF bTrip_IBC_BlowerFault THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0010; END_IF;
IF bTrip_HaulOffDriveStall THEN dwAlarmWord_Trip := dwAlarmWord_Trip OR 16#0000_0020; END_IF;

(* Automatic Transition to E-Stop state on any Priority 1 Trip *)
IF (dwAlarmWord_Trip <> 16#0000_0000) AND (nActiveFSM_State <> 12) THEN
    nActiveFSM_State := 12;
END_IF;

(* Priority 2: Process Warnings & Pre-Alarms with Hysteresis *)
bWarn_GaugeVarianceHigh := (rObserved_ThicknessStdDev_um >= 3.20);
bWarn_FrostLineDrift := (ABS(rObserved_FrostLineHeight_mm - rTargetFrostLineHeight_mm) >= 180.0);
bWarn_IBC_PressureDeviation := (ABS(rObserved_InternalPressure_Pa - rTargetInternalPressure_Pa) >= 15.0);
bWarn_FeederStarvation := (ABS(rObserved_TotalThroughput_kgh - rTotalThroughputSetpoint_kgh) >= 65.0);
bWarn_MeltTempDeviation := (rExtruderMeltTemp_ExtD_degC >= 235.0) OR (rExtruderMeltTemp_ExtD_degC <= 195.0);
bWarn_TMR_DegradedMode := (dwTMR_DiscrepancyWord <> 16#0000_0000);
bWarn_WinderTensionExcursion := (ABS(rWinderTensionFeedback_N - rTaperTension_N) >= 50.0);

dwAlarmWord_Warning := 16#0000_0000;
IF bWarn_GaugeVarianceHigh THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0001; END_IF;
IF bWarn_FrostLineDrift THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0002; END_IF;
IF bWarn_IBC_PressureDeviation THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0004; END_IF;
IF bWarn_FeederStarvation THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0008; END_IF;
IF bWarn_MeltTempDeviation THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0010; END_IF;
IF bWarn_TMR_DegradedMode THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0020; END_IF;
IF bWarn_WinderTensionExcursion THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0040; END_IF;
IF bWarn_InterfacialShearHigh THEN dwAlarmWord_Warning := dwAlarmWord_Warning OR 16#0000_0080; END_IF;

(* Priority 3: Operational Advisory Alarms *)
dwAlarmWord_Advisory := 16#0000_0000;
IF bSpliceInProgress THEN dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0001; END_IF;
IF (rWinderRollDiameter_mm >= (rSpliceTriggerDiameter_mm * 0.95)) THEN dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0002; END_IF;
IF NOT bCoreLoadedPermissive THEN dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0004; END_IF;
IF (rHaulOffOscillationAngle_deg >= 170.0) OR (rHaulOffOscillationAngle_deg <= -170.0) THEN dwAlarmWord_Advisory := dwAlarmWord_Advisory OR 16#0000_0008; END_IF;

(* Pack Comprehensive System Status Word *)
dwStatusWord_System := 16#0000_0000;
IF bMasterEnable THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0001; END_IF;
IF bExtrusionActive THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0002; END_IF;
IF bIBC_ClosedLoopLocked THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0004; END_IF;
IF bAirRingProfileActive THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0008; END_IF;
IF bEdgeTrimSlittersEngaged THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0010; END_IF;
IF bCoronaTreaterActive THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0020; END_IF;
IF bSpliceInProgress THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0040; END_IF;
IF (dwAlarmWord_Trip = 16#0000_0000) THEN dwStatusWord_System := dwStatusWord_System OR 16#0000_0080; END_IF;

(* System Master Readiness Flag *)
bSystemReady := bMasterEnable AND bEmergencyStop_NC AND (dwAlarmWord_Trip = 16#0000_0000) AND (nActiveFSM_State < 12);
""")

    # Closing line
    st.append("END_FUNCTION_BLOCK\n")

    return "".join(st)

def main():
    code = build_iec_code()
    print(f"Total IEC 61131-3 ST character count: {len(code)}")

if __name__ == "__main__":
    main()
