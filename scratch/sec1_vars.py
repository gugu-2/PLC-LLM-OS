# Section 1: Header, VAR_INPUT, VAR_OUTPUT, VAR declarations

def get_sec1():
    return """FUNCTION_BLOCK FB_Cable_ContinuousVulcanization_TripleExtrusion_Sag
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Electrical Cable & Wire Manufacturing Machinery
 * SYSTEM                       : High-Voltage (132 kV - 400 kV) Power Cable Continuous Vulcanization (CV) Line
 * LINE SPECIFICATION           : Line Speed: Up to 25.0 m/min, Cable Outer Diameter: 95.0 mm (Insulation + Semi-Con Screens)
 * INTEGRATED SUBSYSTEMS        : - Triple-Head Co-Extrusion System (Conductor Screen, XLPE Insulation, Insulation Screen)
 *                                - 150-Meter Nitrogen-Pressurized Catenary Vulcanization Heating & Telescopic Tube
 *                                - 4-Zone Radiant Electric Curing Heaters (380.0 deg C to 420.0 deg C)
 *                                - 10.0 bar High-Purity Dry Nitrogen (N2) Overpressure Atmosphere
 *                                - Continuous Non-Contact X-Ray Sag & Catenary Position Sensor (+/- 2.0 mm Centering)
 *                                - High-Pressure Recirculating Water Quench Cooling Leg with Hydrostatic Boundary Seal
 *                                - Dual-Wheel Caterpillar Capstan Line Speed & Tension Synchronizer (120 kN Pulling Force)
 *                                - In-Line 8-Axis Ultrasonic Wall Thickness & Concentricity / Eccentricity Scanner
 *                                - 8x8 Multivariable Discrete State-Space Cyber-Physical Dynamics (20.0 ms Discrete Cycle)
 *                                - Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD)
 *                                - 2oo3 Triple Modular Redundancy (TMR) Sensor Voting with Discrepancy Debounce Across 11 Groups
 *                                - ISA-18.2 5-Tier Process Alarm Hierarchy (HH, H, L, LL, ROC) & Bit-Packed Status Words
 *                                - 12-Stage Deterministic Production Finite State Machine (FSM)
 * =====================================================================================================================
 * CYBER-PHYSICAL CATENARY KINEMATICS, POLYMER RHEOLOGY & THERMODYNAMIC EQUATIONS:
 * 1. Hyperbolic Cosine Catenary Trajectory & Tube Clearance Observer:
 *    The heavy high-voltage power cable (total linear mass w_cable approx 18.5 to 24.0 kg/m) hangs freely inside the
 *    150-meter inclined catenary vulcanization tube under longitudinal tension H [N] applied by the haul-off capstan:
 *      y(x) = a * (COSH(x / a) - 1.0)
 *    where the catenary parameter a is defined as:
 *      a = H / (w_cable * g)
 *    For x / a << 1, the parabolic Maclaurin series approximation yields:
 *      y(x) approx (w_cable * g * x^2) / (2.0 * H) + (w_cable^3 * g^3 * x^4) / (24.0 * H^3)
 *    The non-contact X-ray sag sensor is stationed at x_sens = 28.5 m from the triple-head crosshead die exit.
 *    The nominal sag setpoint y_set = 142.5 mm centers the cable coaxially inside the 250.0 mm inner diameter tube liner.
 *    The vertical clearance margins to the upper and lower tube walls are continuously evaluated:
 *      Clearance_Top(x)    = (D_tube_inner / 2.0) - y(x) - (D_cable_outer / 2.0)
 *      Clearance_Bottom(x) = (D_tube_inner / 2.0) + y(x) - (D_cable_outer / 2.0)
 *    Tube contact hazard trip occurs instantaneously if min(Clearance_Top, Clearance_Bottom) <= 12.0 mm.
 *    The analytical sensitivity of cable sag with respect to capstan pulling tension is:
 *      dy_sag / dH = - (w_cable * g * x_sens^2) / (2.0 * H^2) = - y_sag / H
 *    Dynamic cable thermal expansion elongation inside the 400 deg C heating tube adds to geometric sag:
 *      Delta_L_thermal = Integral_0^L [ alpha_Cu * Delta_T_cond(x) + alpha_XLPE * Delta_T_insul(x) ] dx
 *
 * 2. Cross-Linked Polyethylene (XLPE) Peroxide Cross-Linking Kinetics & Gel Fraction:
 *    High-purity low-density polyethylene is formulated with 1.5 to 2.0 wt% Dicumyl Peroxide (DCP) cross-linking agent.
 *    Thermal decomposition of DCP generates cumyloxy and methyl radicals, initiating cross-linking between polymer chains:
 *      ROOR -> 2 RO* -> R* + R* -> R-R (Cross-linked Network)
 *    The cross-linking reaction rate follows first-order Arrhenius kinetics:
 *      d_alpha / dt = k_0 * EXP(-E_a / (R_gas * T_melt(t))) * (1.0 - alpha)^n_order
 *    where:
 *      k_0     = 4.85e14 s^-1 (Pre-exponential frequency factor)
 *      E_a     = 142.5 kJ/mol (Activation energy of DCP decomposition)
 *      R_gas   = 8.31446 J/(mol*K) (Universal gas constant)
 *      n_order = 1.0 (First-order reaction order)
 *    The cross-linking degree (Gel Fraction alpha) must reach at least 82.0% across the entire insulation wall thickness
 *    prior to entering the water quench cooling leg to prevent thermal creep deformation and guarantee electrical endurance.
 *
 * 3. Dry Nitrogen (N2) High-Pressure Overpressure & Micro-Void Nucleation Suppression:
 *    During DCP thermal decomposition, volatile hydrocarbon byproducts are formed: acetophenone, cumyl alcohol, and methane.
 *    At atmospheric pressure, these volatile species vaporize and nucleate microscopic gas cavities (micro-voids 5 to 50 um)
 *    within the molten XLPE matrix. Under high electrical stress (132 kV to 400 kV, field strength > 15 kV/mm), micro-voids
 *    trigger partial discharge (PD) inception and electrical water treeing, leading to catastrophic dielectric breakdown.
 *    Maintaining a continuous 10.0 bar dry nitrogen gas overpressure raises the local boiling points of volatile byproducts,
 *    forcing them to remain completely dissolved in the molten polymer until crystallization occurs in the quench leg:
 *      P_N2_min >= P_sat_acetophenone(T_max) + P_sat_cumylalcohol(T_max) + P_sol_methane
 *    Dynamic nitrogen gas inventory inside the 150-meter tube follows the compressible mass conservation equation:
 *      V_tube * (d_P_N2 / dt) = (m_dot_N2_in - m_dot_N2_vent - m_dot_N2_seal_leak) * (R_gas * T_tube_mean / M_N2)
 *
 * 4. Hydrostatic Quench Seal Boundary & Controlled Forced Convection Cooling:
 *    The boundary between the 10.0 bar hot nitrogen vulcanization section and the pressurized water quench leg is
 *    sealed via a dynamic hydrostatic labyrinth boundary seal. The differential pressure across the boundary seal:
 *      Delta_P_seal = P_water_leg - P_N2_tube
 *    must be regulated within the tight operational boundary window of +0.15 bar <= Delta_P_seal <= +0.35 bar.
 *    If Delta_P_seal drops below +0.05 bar, hot nitrogen gas blows through into the cooling leg, causing cavitation;
 *    if Delta_P_seal exceeds +0.50 bar, cold water back-floods into the 400 deg C curing zone, creating a steam explosion risk.
 *    Forced convective cooling in the quench leg reduces cable temperature from 205 deg C to < 70 deg C, traversing the
 *    critical XLPE semi-crystalline solidification phase transition (108 deg C to 118 deg C) under constant pressure.
 *
 * 5. In-Line 8-Axis Ultrasonic Wall Thickness & Concentricity / Eccentricity Observer:
 *    Eight piezo-composite immersion ultrasonic transducers positioned circumferentially at 45-degree angular spacing:
 *      theta_i = [0, 45, 90, 135, 180, 225, 270, 315] degrees
 *    measure the ultrasonic pulse time-of-flight Delta_t_i across the XLPE insulation wall. The acoustic propagation
 *    velocity in molten/solidifying XLPE exhibits strong negative temperature dependence:
 *      c_XLPE(T) = c_0 - beta_T * (T_insul - 20.0)   [m/s]
 *    where c_0 = 1965.0 m/s and beta_T = 3.25 m/(s*deg C).
 *    The local radial wall thickness at probe i is calculated as:
 *      d_wall_i = 0.5 * c_XLPE(T) * Delta_t_i
 *    The spatial eccentricity vector components (e_x, e_y) and eccentricity percentage E_pct are obtained via:
 *      e_x   = (1.0 / 4.0) * Sum_{i=0..7} [ d_wall_i * COS(theta_i) ]
 *      e_y   = (1.0 / 4.0) * Sum_{i=0..7} [ d_wall_i * SIN(theta_i) ]
 *      E_pct = ((d_wall_max - d_wall_min) / d_wall_max) * 100.0 %
 *    To ensure HV cable certification (IEC 60840 / IEC 62067), E_pct must remain strictly <= 5.0%.
 *
 * 6. Dual Caterpillar Capstan Synchronization & Electronic Line Shaft:
 *    The infeed metering capstan (at the extruder crosshead entry) and the haul-off pulling capstan (at the tube exit)
 *    are electronically synchronized to maintain uniform cable linear speed v_line = 25.0 m/min and hold line tension H:
 *      H_actual = FT_HAULOFF_TENSION_601 - F_friction_guides - (w_cable * g * Delta_z_elevation)
 *    The haul-off pulling capstan provides active tension trim via high-bandwidth servo torque regulation:
 *      Delta_v_hauloff = K_tension_p * (H_set - H_actual) + K_tension_i * Integral(H_set - H_actual) dt
 *
 * 7. Receding-Horizon Model Predictive Control (MPC) Formulation:
 *    A discrete 8-state, 7-control multivariable state-space model is formulated at scan time T_s = 20.0 ms:
 *      x[k+1] = A * x[k] + B * u[k]
 *      y[k]   = C * x[k] + D * u[k]
 *    The optimal control increment Delta_u is solved via Projected Gradient Descent (PGD) over a receding horizon:
 *      Cost J = Sum_{i=1..N} [ (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u + Delta_u^T * S * Delta_u ] + x_N^T * P * x_N
 *    penalizing catenary sag deviations, nitrogen pressure fluctuations, radiant temperature errors, and tension surges.
 * =====================================================================================================================
 *)

VAR_INPUT
    (* ========================================================================================= *)
    (* 1. MASTER SUPERVISORY PERMISSIVES, SAFETY GATES & OPERATION MODES                         *)
    (* ========================================================================================= *)
    bMasterPowerOn                      : BOOL := FALSE;    (* Line Master 400V 3-Phase Main Supply Permissive [BOOL] *)
    bSystemAutoEnable                   : BOOL := FALSE;    (* Automatic Closed-Loop CV Line Production Sequence Enable [BOOL] *)
    bEmergencyStop_NC                   : BOOL := TRUE;     (* Dual-Channel Hardwired Safety Circuit Active Low [BOOL] *)
    bFaultReset                         : BOOL := FALSE;    (* Operator Master Fault Reset & Trip Latch Acknowledge [BOOL] *)
    bNitrogenSupplyHeaderOk             : BOOL := TRUE;     (* High-Purity Dry Nitrogen Bulk Header Permissive (P >= 15 bar) [BOOL] *)
    bCoolingWaterHeaderOk               : BOOL := TRUE;     (* Pressurized Water Quench Cooling Header Permissive [BOOL] *)
    bExtruderHeatersPermissive          : BOOL := TRUE;     (* Triple-Head Extruder Barrel & Die Heating Interlock [BOOL] *)
    bConductorSpliceClear               : BOOL := TRUE;     (* Conductor Stringing Splice Detector Clear Gate [BOOL] *)
    bTakeUpSpoolReady                   : BOOL := TRUE;     (* Downstream Continuous Take-Up Turret Spool Ready [BOOL] *)
    bPayoffTensionPermissive            : BOOL := TRUE;     (* Bare Conductor Payoff Back-Tension Dancer Clear [BOOL] *)
    tDeterministicScanTime              : TIME := T#20MS;   (* Deterministic Control Task Scan Period (20 ms) [TIME] *)

    (* ========================================================================================= *)
    (* 2. CABLE RECIPE SETPOINTS, GEOMETRIC TARGETS & KINEMATIC CONSTRAINTS                      *)
    (* ========================================================================================= *)
    rSet_LineSpeed_Target_mpm           : REAL := 25.00;    (* Target Continuous Vulcanization Line Speed [m/min] *)
    rSet_InsulMeltTemp_Target_degC      : REAL := 132.50;   (* Extruder 2 XLPE Melt Temperature Target [deg C] *)
    rSet_InsulMeltPress_Target_bar      : REAL := 385.00;   (* Extruder 2 XLPE Melt Pressure Target at Die Entry [bar] *)
    rSet_CatenarySagTarget_mm           : REAL := 142.50;   (* Target X-Ray Sag Measurement for Tube Centering [mm] *)
    rSet_TubeN2PressTarget_bar          : REAL := 10.000;   (* 150m Vulcanization Tube N2 Overpressure Setpoint [bar] *)
    rSet_Zone1_TempTarget_degC          : REAL := 390.00;   (* Radiant Heating Zone 1 Temperature Setpoint [deg C] *)
    rSet_Zone2_TempTarget_degC          : REAL := 415.00;   (* Radiant Heating Zone 2 Temperature Setpoint [deg C] *)
    rSet_Zone3_TempTarget_degC          : REAL := 410.00;   (* Radiant Heating Zone 3 Temperature Setpoint [deg C] *)
    rSet_Zone4_TempTarget_degC          : REAL := 385.00;   (* Radiant Heating Zone 4 Temperature Setpoint [deg C] *)
    rSet_QuenchWaterLevel_mm            : REAL := 2100.0;   (* Hydrostatic Water Quench Boundary Level Target [mm] *)
    rSet_HaulOffTension_kN              : REAL := 62.50;    (* Haul-Off Caterpillar Capstan Line Tension Target [kN] *)
    rSet_NominalWallThickness_mm        : REAL := 22.50;    (* Nominal High-Voltage XLPE Insulation Wall Thickness [mm] *)
    rSet_MaxAllowableEccentricity_pct   : REAL := 5.000;    (* Maximum Allowable Insulation Eccentricity Threshold [%] *)
    rSet_MinGelFraction_pct             : REAL := 82.00;    (* Minimum Required XLPE Cross-Linking Gel Fraction [%] *)
    rSet_MaxSagDeviationTolerance_mm   : REAL := 2.000;    (* Maximum Allowable Catenary Centering Sag Error [mm] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) FIELD INSTRUMENTATION (11 TRANSMITTER TRIPLETS)   *)
    (* ========================================================================================= *)
    (* PT_EXTRUDER_MELT_PRESS_101: Triplicated Melt Pressure Transducers at Die Adapter Entry [bar] *)
    PT_EXTRUDER_MELT_PRESS_101A         : REAL := 385.00;   (* XLPE Melt Pressure Transducer Channel A [bar] *)
    PT_EXTRUDER_MELT_PRESS_101B         : REAL := 385.00;   (* XLPE Melt Pressure Transducer Channel B [bar] *)
    PT_EXTRUDER_MELT_PRESS_101C         : REAL := 385.00;   (* XLPE Melt Pressure Transducer Channel C [bar] *)

    (* TT_EXTRUDER_MELT_TEMP_102: Triplicated Melt Immersion Thermocouples in Crosshead Stream [deg C] *)
    TT_EXTRUDER_MELT_TEMP_102A          : REAL := 132.50;   (* XLPE Melt Immersion Sensor Channel A [deg C] *)
    TT_EXTRUDER_MELT_TEMP_102B          : REAL := 132.50;   (* XLPE Melt Immersion Sensor Channel B [deg C] *)
    TT_EXTRUDER_MELT_TEMP_102C          : REAL := 132.50;   (* XLPE Melt Immersion Sensor Channel C [deg C] *)

    (* ZT_CATENARY_SAG_XRAY_201: Triplicated Non-Contact X-Ray Vertical Cable Sag Position Transducers [mm] *)
    ZT_CATENARY_SAG_XRAY_201A           : REAL := 142.50;   (* X-Ray Non-Contact Sag Sensor Channel A [mm] *)
    ZT_CATENARY_SAG_XRAY_201B           : REAL := 142.50;   (* X-Ray Non-Contact Sag Sensor Channel B [mm] *)
    ZT_CATENARY_SAG_XRAY_201C           : REAL := 142.50;   (* X-Ray Non-Contact Sag Sensor Channel C [mm] *)

    (* PT_TUBE_N2_PRESS_301: Triplicated Vulcanization Tube Nitrogen Static Overpressure Transmitters [bar] *)
    PT_TUBE_N2_PRESS_301A               : REAL := 10.000;   (* CV Tube Nitrogen Pressure Transmitter Channel A [bar] *)
    PT_TUBE_N2_PRESS_301B               : REAL := 10.000;   (* CV Tube Nitrogen Pressure Transmitter Channel B [bar] *)
    PT_TUBE_N2_PRESS_301C               : REAL := 10.000;   (* CV Tube Nitrogen Pressure Transmitter Channel C [bar] *)

    (* TE_TUBE_ZONE1_TEMP_401: Triplicated Radiant Curing Heating Zone 1 Embedded Thermocouples [deg C] *)
    TE_TUBE_ZONE1_TEMP_401A             : REAL := 390.00;   (* Radiant Heating Zone 1 Thermocouple Channel A [deg C] *)
    TE_TUBE_ZONE1_TEMP_401B             : REAL := 390.00;   (* Radiant Heating Zone 1 Thermocouple Channel B [deg C] *)
    TE_TUBE_ZONE1_TEMP_401C             : REAL := 390.00;   (* Radiant Heating Zone 1 Thermocouple Channel C [deg C] *)

    (* TE_TUBE_ZONE2_TEMP_402: Triplicated Radiant Curing Heating Zone 2 Peak Thermocouples [deg C] *)
    TE_TUBE_ZONE2_TEMP_402A             : REAL := 415.00;   (* Radiant Heating Zone 2 Thermocouple Channel A [deg C] *)
    TE_TUBE_ZONE2_TEMP_402B             : REAL := 415.00;   (* Radiant Heating Zone 2 Thermocouple Channel B [deg C] *)
    TE_TUBE_ZONE2_TEMP_402C             : REAL := 415.00;   (* Radiant Heating Zone 2 Thermocouple Channel C [deg C] *)

    (* LT_WATER_QUENCH_LVL_501: Triplicated Hydrostatic Quench Water Boundary Level Radar Transmitters [mm] *)
    LT_WATER_QUENCH_LVL_501A            : REAL := 2100.0;   (* Quench Boundary Level Radar Channel A [mm] *)
    LT_WATER_QUENCH_LVL_501B            : REAL := 2100.0;   (* Quench Boundary Level Radar Channel B [mm] *)
    LT_WATER_QUENCH_LVL_501C            : REAL := 2100.0;   (* Quench Boundary Level Radar Channel C [mm] *)

    (* FT_HAULOFF_TENSION_601: Triplicated Haul-Off Caterpillar Capstan Line Tension Load Cells [kN] *)
    FT_HAULOFF_TENSION_601A             : REAL := 62.50;    (* Haul-Off Capstan Load Cell Channel A [kN] *)
    FT_HAULOFF_TENSION_601B             : REAL := 62.50;    (* Haul-Off Capstan Load Cell Channel B [kN] *)
    FT_HAULOFF_TENSION_601C             : REAL := 62.50;    (* Haul-Off Capstan Load Cell Channel C [kN] *)

    (* WT_WALL_THICKNESS_701: Triplicated In-Line Ultrasonic Mean Wall Thickness Telemetry [mm] *)
    WT_WALL_THICKNESS_701A              : REAL := 22.50;    (* In-Line Ultrasonic Mean Wall Thickness Ch A [mm] *)
    WT_WALL_THICKNESS_701B              : REAL := 22.50;    (* In-Line Ultrasonic Mean Wall Thickness Ch B [mm] *)
    WT_WALL_THICKNESS_701C              : REAL := 22.50;    (* In-Line Ultrasonic Mean Wall Thickness Ch C [mm] *)

    (* ST_LINE_PULL_SPEED_801: Triplicated Caterpillar Capstan Optical Rotary Encoders [m/min] *)
    ST_LINE_PULL_SPEED_801A             : REAL := 25.00;    (* Capstan Line Linear Speed Tachometer Ch A [m/min] *)
    ST_LINE_PULL_SPEED_801B             : REAL := 25.00;    (* Capstan Line Linear Speed Tachometer Ch B [m/min] *)
    ST_LINE_PULL_SPEED_801C             : REAL := 25.00;    (* Capstan Line Linear Speed Tachometer Ch C [m/min] *)

    (* PT_SEAL_DIFF_PRESS_901: Triplicated Hydrostatic Quench Seal Differential Pressure Transmitters [bar] *)
    PT_SEAL_DIFF_PRESS_901A             : REAL := 0.250;    (* Hydrostatic Boundary Seal Diff Press Ch A [bar] *)
    PT_SEAL_DIFF_PRESS_901B             : REAL := 0.250;    (* Hydrostatic Boundary Seal Diff Press Ch B [bar] *)
    PT_SEAL_DIFF_PRESS_901C             : REAL := 0.250;    (* Hydrostatic Boundary Seal Diff Press Ch C [bar] *)

    (* ========================================================================================= *)
    (* 4. 8-AXIS ULTRASONIC SCANNER RAW TRANSIT TIME TELEMETRY & AUXILIARY INPUTS                *)
    (* ========================================================================================= *)
    rUS_TransitTime_000deg_us           : REAL := 25.32;    (* Ultrasonic Pulse Echo Time-of-Flight 0 deg [us] *)
    rUS_TransitTime_045deg_us           : REAL := 25.36;    (* Ultrasonic Pulse Echo Time-of-Flight 45 deg [us] *)
    rUS_TransitTime_090deg_us           : REAL := 25.40;    (* Ultrasonic Pulse Echo Time-of-Flight 90 deg [us] *)
    rUS_TransitTime_135deg_us           : REAL := 25.35;    (* Ultrasonic Pulse Echo Time-of-Flight 135 deg [us] *)
    rUS_TransitTime_180deg_us           : REAL := 25.31;    (* Ultrasonic Pulse Echo Time-of-Flight 180 deg [us] *)
    rUS_TransitTime_225deg_us           : REAL := 25.28;    (* Ultrasonic Pulse Echo Time-of-Flight 225 deg [us] *)
    rUS_TransitTime_270deg_us           : REAL := 25.25;    (* Ultrasonic Pulse Echo Time-of-Flight 270 deg [us] *)
    rUS_TransitTime_315deg_us           : REAL := 25.29;    (* Ultrasonic Pulse Echo Time-of-Flight 315 deg [us] *)
    bTelescopicSpliceBoxLatched         : BOOL := TRUE;     (* Telescopic Entry Splice Box Pneumatic Clamp Latched [BOOL] *)
    bWaterQuenchCoolerFlowOk            : BOOL := TRUE;     (* Quench Water Heat Exchanger Circulation Flow Switch [BOOL] *)
    rPayoffConductorBackTension_kN      : REAL := 18.50;    (* Bare Copper Conductor Payoff Stand Back-Tension [kN] *)
    rExtruder1_CondScreen_RPM           : REAL := 42.00;    (* Extruder 1 Conductor Semi-Con Screen Screw Speed [RPM] *)
    rExtruder3_InsScreen_RPM            : REAL := 38.50;    (* Extruder 3 Insulation Semi-Con Screen Screw Speed [RPM] *)
    rAmbientTemperature_degC           : REAL := 24.50;    (* CV Line Extruder Hall Ambient Air Temperature [deg C] *)
    rConductorCoreCrossSection_mm2      : REAL := 1200.0;   (* Compacted Stranded Copper Conductor Area [mm2] *)
    AIT_TUBE_O2_PPM_1001                : REAL := 28.5;     (* Nitrogen Tube Oxygen Gas Concentration Analyzer [ppm] *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================= *)
    (* 1. PRIMARY SYSTEM OPERATION & INTERLOCK STATUS FLAGS                                      *)
    (* ========================================================================================= *)
    bSystemReady                        : BOOL := FALSE;    (* Master CV Line Automation Ready Permissive [BOOL] *)
    bSystemRunning                      : BOOL := FALSE;    (* Active High-Voltage Cable Vulcanization Line Running [BOOL] *)
    bEmergencyTripped                   : BOOL := FALSE;    (* Master Critical Safety Shutdown Latched Trip [BOOL] *)
    bCatenarySagCenteringOk             : BOOL := FALSE;    (* Cable Centered Inside Catenary Tube (+/- 2.0 mm) [BOOL] *)
    bTubeContactHazardActive            : BOOL := FALSE;    (* Critical Cable-to-Tube Liner Wall Clearance Hazard [BOOL] *)
    bCrossLinkingTargetAchieved         : BOOL := FALSE;    (* XLPE Insulation Curing Gel Fraction >= 82.0% Achieved [BOOL] *)
    bEccentricityAlarmActive            : BOOL := FALSE;    (* Cable Insulation Concentricity Out-of-Tolerance (> 5%) [BOOL] *)
    bHydrostaticSealBalanced            : BOOL := TRUE;     (* Quench Leg Hydrostatic Seal Differential Pressure Ok [BOOL] *)
    bSpoolTransferPermissive            : BOOL := FALSE;    (* Dual Take-Up Turret Flying Splice Transfer Permissive [BOOL] *)
    nActiveFSM_State                    : INT  := 0;        (* Current Operational 12-Stage Finite State Machine Step [0..11] *)

    (* ========================================================================================= *)
    (* 2. CLOSED-LOOP ACTUATOR COMMANDS & VALVE SETPOINTS                                        *)
    (* ========================================================================================= *)
    rCmd_Extruder2_XLPE_RPM             : REAL := 0.0;      (* Main Extruder 2 XLPE Screw Speed Command [RPM] *)
    rCmd_Extruder1_CondScreen_RPM       : REAL := 0.0;      (* Extruder 1 Conductor Screen Screw Speed Command [RPM] *)
    rCmd_Extruder3_InsScreen_RPM        : REAL := 0.0;      (* Extruder 3 Insulation Screen Screw Speed Command [RPM] *)
    rCmd_HaulOffCapstan_Speed_mpm       : REAL := 0.0;      (* Haul-Off Pulling Capstan Linear Velocity Command [m/min] *)
    rCmd_HaulOffCapstan_TensionTrim_kN  : REAL := 0.0;      (* Haul-Off Capstan Electronic Line Shaft Tension Trim [kN] *)
    rCmd_InfeedCapstan_Speed_mpm        : REAL := 0.0;      (* Infeed Metering Caterpillar Capstan Speed Command [m/min] *)
    rCmd_Zone1_SCR_Duty_pct             : REAL := 0.0;      (* Zone 1 Radiant Electric Heater SCR Power Duty [0..100%] *)
    rCmd_Zone2_SCR_Duty_pct             : REAL := 0.0;      (* Zone 2 Radiant Electric Heater SCR Power Duty [0..100%] *)
    rCmd_Zone3_SCR_Duty_pct             : REAL := 0.0;      (* Zone 3 Radiant Electric Heater SCR Power Duty [0..100%] *)
    rCmd_Zone4_SCR_Duty_pct             : REAL := 0.0;      (* Zone 4 Radiant Electric Heater SCR Power Duty [0..100%] *)
    rCmd_N2_InjectionValve_pct          : REAL := 0.0;      (* High-Pressure N2 Header Supply Servo Valve [0..100%] *)
    rCmd_N2_VentValve_pct               : REAL := 0.0;      (* Tube N2 Overpressure Regulating Exhaust Valve [0..100%] *)
    rCmd_QuenchWaterInflowValve_pct     : REAL := 0.0;      (* Quench Leg High-Pressure Water Supply Valve [0..100%] *)
    rCmd_QuenchWaterDrainValve_pct      : REAL := 0.0;      (* Quench Leg Hydrostatic Level Modulating Drain Valve [0..100%] *)
    rCmd_PayoffBrakeTorque_Nm           : REAL := 0.0;      (* Bare Conductor Payoff Tension Brake Torque [N*m] *)
    bCmd_EmergencyN2FastVent            : BOOL := FALSE;    (* Emergency High-Capacity Pneumatic N2 Blowdown Dump [BOOL] *)
    bCmd_CaterpillarPneumaticBrakeClamp : BOOL := FALSE;    (* 120 kN Caterpillar Capstan Mechanical Emergency Clamp [BOOL] *)
    bCmd_TelescopicSealIsolate          : BOOL := FALSE;    (* Telescopic Crosshead Entry Splice Box Seal Isolation [BOOL] *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTED TELEMETRY OUTPUTS                           *)
    (* ========================================================================================= *)
    rVoted_ExtruderMeltPress_bar        : REAL := 385.00;   (* 2oo3 Voted XLPE Melt Pressure at Die Adapter [bar] *)
    rVoted_ExtruderMeltTemp_degC        : REAL := 132.50;   (* 2oo3 Voted XLPE Crosshead Melt Temperature [deg C] *)
    rVoted_CatenarySag_mm               : REAL := 142.50;   (* 2oo3 Voted Non-Contact X-Ray Vertical Cable Sag [mm] *)
    rVoted_TubeN2Press_bar              : REAL := 10.000;   (* 2oo3 Voted Vulcanization Tube Nitrogen Pressure [bar] *)
    rVoted_Zone1Temp_degC               : REAL := 390.00;   (* 2oo3 Voted Radiant Curing Zone 1 Heating Temp [deg C] *)
    rVoted_Zone2Temp_degC               : REAL := 415.00;   (* 2oo3 Voted Radiant Curing Zone 2 Heating Temp [deg C] *)
    rVoted_QuenchWaterLvl_mm            : REAL := 2100.0;   (* 2oo3 Voted Hydrostatic Quench Water Level [mm] *)
    rVoted_HaulOffTension_kN            : REAL := 62.50;    (* 2oo3 Voted Haul-Off Caterpillar Capstan Line Tension [kN] *)
    rVoted_WallThickness_mm             : REAL := 22.50;    (* 2oo3 Voted Ultrasonic Mean Insulation Wall Thickness [mm] *)
    rVoted_LinePullSpeed_mpm            : REAL := 25.00;    (* 2oo3 Voted Caterpillar Capstan Linear Line Speed [m/min] *)
    rVoted_SealDiffPress_bar            : REAL := 0.250;    (* 2oo3 Voted Hydrostatic Quench Seal Differential Press [bar] *)

    (* ========================================================================================= *)
    (* 4. CYBER-PHYSICAL OBSERVERS, KINEMATIC & THERMODYNAMIC METRICS                            *)
    (* ========================================================================================= *)
    rCalculated_CatenaryClearance_Top_mm: REAL := 43.75;    (* Upper Vertical Clearance to Tube Liner [mm] *)
    rCalculated_CatenaryClearance_Bot_mm: REAL := 33.75;    (* Lower Vertical Clearance to Tube Liner [mm] *)
    rCalculated_GelFraction_pct         : REAL := 84.62;    (* Observed Cumulative XLPE Cross-Linking Gel Fraction [%] *)
    rCalculated_InstantCrosslinkRate    : REAL := 0.00185;  (* Instantaneous DCP Reaction Rate d_alpha/dt [s^-1] *)
    rCalculated_MeltViscosity_Pas       : REAL := 1250.0;   (* Carreau-Yasuda Rheological Melt Apparent Viscosity [Pa*s] *)
    rCalculated_WallEccentricity_pct    : REAL := 2.850;    (* In-Line 8-Axis Ultrasonic Eccentricity Ratio [%] *)
    rCalculated_EccentricityVector_X_mm : REAL := 0.285;    (* Spatial Eccentricity Vector Component X [mm] *)
    rCalculated_EccentricityVector_Y_mm : REAL := 0.192;    (* Spatial Eccentricity Vector Component Y [mm] *)
    rCalculated_CableUnitWeight_kgm     : REAL := 21.840;   (* Cumulative Linear Cable Weight with Insulation [kg/m] *)
    rCalculated_N2MassFlowLeak_kgh      : REAL := 1.250;    (* Observed Total Nitrogen Seal Leakage Flow Rate [kg/h] *)
    rCalculated_QuenchCoolingDuty_kW    : REAL := 285.50;   (* Thermal Heat Removal Rate in Pressurized Quench Leg [kW] *)
    rCalculated_SuppressionMargin_bar   : REAL := 6.820;    (* Dynamic Margin Over Volatile Micro-Void Vapor Pressure [bar] *)
    rMPC_QuadraticCost_J                : REAL := 0.000;    (* Receding-Horizon Optimal Quadratic Cost Objective J [-] *)

    (* ========================================================================================= *)
    (* 5. ISA-18.2 BIT-PACKED DIAGNOSTIC & TELEMETRY STATUS WORDS                                *)
    (* ========================================================================================= *)
    dwStatusWord_CVLine                 : DWORD := 16#0000_0000; (* Bit-Packed Operational State, Interlocks & Permissives *)
    dwStatusWord_Extruders              : DWORD := 16#0000_0000; (* Bit-Packed Triple Extrusion & Capstan Synchronization *)
    dwAlarmWord_Trip                    : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 1 Fast Emergency Trips *)
    dwAlarmWord_Warning                 : DWORD := 16#0000_0000; (* Bit-Packed ISA-18.2 Priority 2 Process Deviations *)
    dwSensorHealthMask_Low              : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Channel 1..6 Fault Isolation Bits *)
    dwSensorHealthMask_High             : DWORD := 16#0000_0000; (* Bit-Packed 2oo3 TMR Channel 7..11 Fault Isolation Bits *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* 1. DISCRETE TASK CYCLE & PHYSICAL / THERMODYNAMIC CONSTANTS                               *)
    (* ========================================================================================= *)
    c_rTs                               : REAL := 0.020;    (* Deterministic PLC Execution Task Period (20 ms) [s] *)
    c_rPi                               : REAL := 3.141592653589793; (* Circle Circumference Constant Pi *)
    c_rGravity                          : REAL := 9.80665;  (* Standard Acceleration of Gravity [m/s2] *)
    c_rUniversalGasConstant_R           : REAL := 8.31446;  (* Universal Molar Gas Constant [J/(mol*K)] *)
    c_rNitrogenMolarMass_kgmol          : REAL := 0.028013; (* Dry Nitrogen Molar Mass M_N2 [kg/mol] *)
    c_rTubeTotalLength_m                : REAL := 150.00;   (* Total Continuous Vulcanization Tube Length [m] *)
    c_rHeatingZoneLength_m              : REAL := 75.00;    (* Radiant Heating Vulcanization Curing Section Length [m] *)
    c_rQuenchCoolingLength_m            : REAL := 75.00;    (* Pressurized Water Quench Cooling Section Length [m] *)
    c_rTubeInnerDiameter_mm             : REAL := 250.00;   (* Stainless Steel Heating Tube Inner Liner Diameter [mm] *)
    c_rCableOuterDiameter_mm            : REAL := 95.00;    (* Finished Cable Outer Diameter over Insulation Screen [mm] *)
    c_rXRaySensorDistance_m             : REAL := 28.50;    (* Longitudinal Position of X-Ray Non-Contact Sag Sensor [m] *)
    c_rCopperDensity_kg_m3              : REAL := 8960.0;   (* Compacted Stranded Copper Conductor Density [kg/m3] *)
    c_rXLPEDensity_kg_m3                : REAL := 925.0;    (* Cross-Linkable Polyethylene Melt Density [kg/m3] *)
    c_rSemiConDensity_kg_m3             : REAL := 1150.0;   (* Semi-Conductive Carbon-Black Loaded PE Density [kg/m3] *)
    c_rDCP_ActivationEnergy_Jmol        : REAL := 142500.0; (* Dicumyl Peroxide Cross-Linking Activation Energy [J/mol] *)
    c_rDCP_PreExponential_s1            : REAL := 4.85e14;  (* Dicumyl Peroxide Thermal Decomposition Factor k0 [s^-1] *)
    c_rXLPE_AcousticVelocity_c0         : REAL := 1965.0;   (* Speed of Sound in Solid XLPE at 20 deg C [m/s] *)
    c_rXLPE_AcousticTempSlope_beta      : REAL := 3.250;    (* Sound Speed Negative Temperature Drift [m/(s*deg C)] *)
    c_rXLPE_SpecificHeat_J_kgK          : REAL := 2350.0;   (* XLPE Isobaric Specific Heat Capacity [J/(kg*K)] *)
    c_rCopperSpecificHeat_J_kgK         : REAL := 385.0;    (* Copper Conductor Specific Heat Capacity [J/(kg*K)] *)
    c_rWaterDensity_kg_m3               : REAL := 1000.0;   (* Quench Water Fluid Density [kg/m3] *)
    c_rCVTubeInternalVolume_m3          : REAL := 7.363;    (* Geometric Internal Volume of 150m x 250mm Tube [m3] *)

    (* ========================================================================================= *)
    (* 2. 8x8 MULTIVARIABLE STATE-SPACE MATRICES & RECEDING-HORIZON MPC REGISTERS                *)
    (* States x[1..8]:                                                                           *)
    (*   x[1]: Extruder 2 XLPE Melt Pressure Deviation Delta_P_melt [bar]                        *)
    (*   x[2]: Extruder 2 XLPE Melt Temperature Deviation Delta_T_melt [deg C]                   *)
    (*   x[3]: Catenary Sag Vertical Deviation Delta_y_sag [mm]                                  *)
    (*   x[4]: Radiant Heating Zone 1 Temperature Deviation Delta_T_zone1 [deg C]                *)
    (*   x[5]: 150m Tube Nitrogen Overpressure Deviation Delta_P_N2 [bar]                        *)
    (*   x[6]: Hydrostatic Water Quench Boundary Level Deviation Delta_L_quench [mm]             *)
    (*   x[7]: Haul-Off Caterpillar Capstan Line Tension Deviation Delta_H_tension [kN]          *)
    (*   x[8]: Ultrasonic Mean Wall Thickness Deviation Delta_W_wall [mm]                        *)
    (* Controls u[1..7]:                                                                         *)
    (*   u[1]: Main Extruder 2 XLPE Screw Speed Command u_screw_rpm [RPM]                        *)
    (*   u[2]: Haul-Off Caterpillar Line Speed Trim Command u_speed_trim [m/min]                 *)
    (*   u[3]: Radiant Heating Zone 1 SCR Electrical Power Duty u_scr1 [%]                       *)
    (*   u[4]: High-Pressure N2 Injection Supply Servo Valve u_n2_inj [%]                        *)
    (*   u[5]: Tube N2 Exhaust Regulating Blowdown Valve u_n2_vent [%]                           *)
    (*   u[6]: Quench Water High-Pressure Inflow Valve u_water_in [%]                            *)
    (*   u[7]: Haul-Off Capstan Electronic Line Shaft Tension Trim Command u_tension_trim [kN]   *)
    (* ========================================================================================= *)
    bMatricesInitialized                : BOOL := FALSE;
    aA                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete System Transition Matrix A (8x8) *)
    aB                                  : ARRAY[1..8, 1..7] OF REAL; (* Discrete Actuator Coupling Matrix B (8x7) *)
    aC                                  : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Measurement Matrix C (8x8) *)
    aD                                  : ARRAY[1..8, 1..7] OF REAL; (* Discrete Direct Feedthrough Matrix D (8x7) *)
    ax_state                            : ARRAY[1..8] OF REAL;       (* Current Discrete State Vector x[k] *)
    ax_next                             : ARRAY[1..8] OF REAL;       (* Projected Next State Vector x[k+1] *)
    ax_ref                              : ARRAY[1..8] OF REAL;       (* Reference Setpoint State Vector r[k] *)
    au_control                          : ARRAY[1..7] OF REAL;       (* Optimal Actuator Control Vector u[k] *)
    au_prev                             : ARRAY[1..7] OF REAL;       (* Prior Actuator Control Vector u[k-1] *)
    au_delta                            : ARRAY[1..7] OF REAL;       (* Control Incremental Slew Rate Delta_u[k] *)
    ay_output                           : ARRAY[1..8] OF REAL;       (* Reconstructed Measurement Vector y[k] *)

    (* Model Predictive Control (MPC) Cost Weighting & Actuator Bounds *)
    aQ_Weight                           : ARRAY[1..8] OF REAL;       (* State Tracking Penalty Diagonal Diag(Q) *)
    aR_Weight                           : ARRAY[1..7] OF REAL;       (* Actuator Magnitude Penalty Diagonal Diag(R) *)
    aS_Weight                           : ARRAY[1..7] OF REAL;       (* Actuator Slew Rate Penalty Diagonal Diag(S) *)
    aP_TerminalWeight                   : ARRAY[1..8] OF REAL;       (* Terminal Horizon Cost Penalty Diag(P) *)
    au_min                              : ARRAY[1..7] OF REAL;       (* Hard Lower Actuator Saturation Bounds *)
    au_max                              : ARRAY[1..7] OF REAL;       (* Hard Upper Actuator Saturation Bounds *)
    adelta_u_max                        : ARRAY[1..7] OF REAL;       (* Maximum Allowable Slew Rate per 20 ms *)
    aGrad_u                             : ARRAY[1..7] OF REAL;       (* Projected Gradient Descent Vector nabla_u J *)
    aPredictedState                     : ARRAY[1..8] OF REAL;       (* 1-Step Horizon State Projection Register *)
    c_rPGD_Alpha                        : REAL := 0.00032;           (* Projected Gradient Descent Learning Rate Alpha *)
    rMPC_QuadraticCostAccum             : REAL := 0.0;               (* Instantaneous Quadratic Cost Functional J *)

    (* ========================================================================================= *)
    (* 3. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) DISCREPANCY TIMERS & HEALTH LATCHES               *)
    (* ========================================================================================= *)
    c_rTol_MeltPress_bar                : REAL := 6.500;    (* Extruder Melt Pressure Discrepancy Gate [bar] *)
    c_rTol_MeltTemp_degC                : REAL := 1.500;    (* Extruder Melt Temperature Discrepancy Gate [deg C] *)
    c_rTol_CatenarySag_mm               : REAL := 1.250;    (* X-Ray Cable Sag Discrepancy Gate [mm] *)
    c_rTol_TubeN2Press_bar              : REAL := 0.120;    (* Tube N2 Overpressure Discrepancy Gate [bar] *)
    c_rTol_Zone1Temp_degC               : REAL := 3.000;    (* Radiant Heating Zone 1 Temp Discrepancy Gate [deg C] *)
    c_rTol_Zone2Temp_degC               : REAL := 3.000;    (* Radiant Heating Zone 2 Temp Discrepancy Gate [deg C] *)
    c_rTol_QuenchWaterLvl_mm            : REAL := 35.00;    (* Quench Water Boundary Level Discrepancy Gate [mm] *)
    c_rTol_HaulOffTension_kN            : REAL := 1.500;    (* Haul-Off Capstan Line Tension Discrepancy Gate [kN] *)
    c_rTol_WallThickness_mm             : REAL := 0.350;    (* Ultrasonic Wall Thickness Discrepancy Gate [mm] *)
    c_rTol_LineSpeed_mpm                : REAL := 0.250;    (* Caterpillar Line Speed Discrepancy Gate [m/min] *)
    c_rTol_SealDiffPress_bar            : REAL := 0.040;    (* Hydrostatic Seal Diff Press Discrepancy Gate [bar] *)
    c_rTMR_PersistencyTimeout_s         : REAL := 0.060;    (* Maximum Allowable Discrepancy Persistency Window (60 ms) [s] *)

    (* Discrepancy Accumulation Chronometers *)
    rTimer_MeltPress_Disc_s             : REAL := 0.0;
    rTimer_MeltTemp_Disc_s              : REAL := 0.0;
    rTimer_CatenarySag_Disc_s           : REAL := 0.0;
    rTimer_TubeN2Press_Disc_s           : REAL := 0.0;
    rTimer_Zone1Temp_Disc_s             : REAL := 0.0;
    rTimer_Zone2Temp_Disc_s             : REAL := 0.0;
    rTimer_QuenchWaterLvl_Disc_s        : REAL := 0.0;
    rTimer_HaulOffTension_Disc_s        : REAL := 0.0;
    rTimer_WallThickness_Disc_s         : REAL := 0.0;
    rTimer_LineSpeed_Disc_s             : REAL := 0.0;
    rTimer_SealDiffPress_Disc_s         : REAL := 0.0;

    (* Channel Health Isolation Latches (TRUE = Channel Quarantined as Outlier) *)
    bIso_MeltPress_ChA                  : BOOL := FALSE;
    bIso_MeltPress_ChB                  : BOOL := FALSE;
    bIso_MeltPress_ChC                  : BOOL := FALSE;
    bIso_MeltTemp_ChA                   : BOOL := FALSE;
    bIso_MeltTemp_ChB                   : BOOL := FALSE;
    bIso_MeltTemp_ChC                   : BOOL := FALSE;
    bIso_CatenarySag_ChA                : BOOL := FALSE;
    bIso_CatenarySag_ChB                : BOOL := FALSE;
    bIso_CatenarySag_ChC                : BOOL := FALSE;
    bIso_TubeN2Press_ChA                : BOOL := FALSE;
    bIso_TubeN2Press_ChB                : BOOL := FALSE;
    bIso_TubeN2Press_ChC                : BOOL := FALSE;
    bIso_Zone1Temp_ChA                  : BOOL := FALSE;
    bIso_Zone1Temp_ChB                  : BOOL := FALSE;
    bIso_Zone1Temp_ChC                  : BOOL := FALSE;
    bIso_Zone2Temp_ChA                  : BOOL := FALSE;
    bIso_Zone2Temp_ChB                  : BOOL := FALSE;
    bIso_Zone2Temp_ChC                  : BOOL := FALSE;
    bIso_QuenchWaterLvl_ChA             : BOOL := FALSE;
    bIso_QuenchWaterLvl_ChB             : BOOL := FALSE;
    bIso_QuenchWaterLvl_ChC             : BOOL := FALSE;
    bIso_HaulOffTension_ChA             : BOOL := FALSE;
    bIso_HaulOffTension_ChB             : BOOL := FALSE;
    bIso_HaulOffTension_ChC             : BOOL := FALSE;
    bIso_WallThickness_ChA              : BOOL := FALSE;
    bIso_WallThickness_ChB              : BOOL := FALSE;
    bIso_WallThickness_ChC              : BOOL := FALSE;
    bIso_LineSpeed_ChA                  : BOOL := FALSE;
    bIso_LineSpeed_ChB                  : BOOL := FALSE;
    bIso_LineSpeed_ChC                  : BOOL := FALSE;
    bIso_SealDiffPress_ChA              : BOOL := FALSE;
    bIso_SealDiffPress_ChB              : BOOL := FALSE;
    bIso_SealDiffPress_ChC              : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 4. CYBER-PHYSICAL OBSERVER INTERNAL ACCUMULATORS & REGISTERS                              *)
    (* ========================================================================================= *)
    (* 4.1 Catenary Trajectory Mechanics & Cable Clearance Registers *)
    rObs_CableLinearMass_kgm            : REAL := 21.840;   (* Total Unit Weight per Meter w_cable [kg/m] *)
    rObs_CatenaryParameter_a_m          : REAL := 291.80;   (* Parameter a = H / (w_cable * g) [m] *)
    rObs_CatenarySagAtSensor_mm         : REAL := 142.50;   (* Calculated Sag at x = 28.5 m [mm] *)
    rObs_ClearanceTop_mm                : REAL := 43.75;    (* Clearance to Top Tube Liner [mm] *)
    rObs_ClearanceBottom_mm             : REAL := 33.75;    (* Clearance to Bottom Tube Liner [mm] *)
    rObs_ThermalElongation_m            : REAL := 0.285;    (* Dynamic Thermal Expansion Elongation [m] *)

    (* 4.2 XLPE Cross-Linking Arrhenius Kinetics & Gel Fraction *)
    rObs_CumulativeGelFraction_pct      : REAL := 84.62;    (* Numerically Integrated Gel Fraction alpha [%] *)
    rObs_ArrheniusRateConstant_s1       : REAL := 0.00185;  (* Arrhenius Reaction Rate Constant k_rxn [s^-1] *)
    rObs_ResidenceTimeInHeatZone_s      : REAL := 180.00;   (* Residence Time Inside 75m Heating Tube [s] *)

    (* 4.3 Nitrogen Atmosphere Mass Balance & Volatile Micro-Void Suppression *)
    rObs_TotalN2Inventory_kg            : REAL := 68.45;    (* Total Nitrogen Mass Inventory Inside 150m Tube [kg] *)
    rObs_ByproductVaporPressure_bar     : REAL := 3.180;    (* Total Saturation Vapor Pressure of Volatile Byproducts [bar] *)
    rObs_DynamicSuppressionMargin_bar   : REAL := 6.820;    (* N2 Overpressure Margin Over Vapor Pressure [bar] *)
    rObs_CalculatedSealLeakRate_kgh     : REAL := 1.250;    (* Nitrogen Leakage Rate Through Mechanical Seals [kg/h] *)

    (* 4.4 Hydrostatic Quench Seal Boundary & Forced Convection Heat Transfer *)
    rObs_QuenchWaterHeatDuty_kW         : REAL := 285.50;   (* Removed Enthalpy Flow in Quench Water Leg [kW] *)
    rObs_QuenchOutletCableTemp_degC     : REAL := 58.50;    (* Estimated Cable Outer Skin Temp at Quench Exit [deg C] *)

    (* 4.5 8-Axis Ultrasonic Scanner & Eccentricity Vector Registers *)
    aUS_WallThickness_mm                : ARRAY[0..7] OF REAL; (* Circumferential Wall Thickness Probes 0..7 [mm] *)
    rUS_SpeedOfSound_mps                : REAL := 1624.5;   (* Speed of Sound Corrected for Melt Temperature [m/s] *)
    rUS_MinWallThickness_mm             : REAL := 22.10;    (* Minimum Radial Wall Thickness Detected [mm] *)
    rUS_MaxWallThickness_mm             : REAL := 22.85;    (* Maximum Radial Wall Thickness Detected [mm] *)
    rUS_MeanWallThickness_mm            : REAL := 22.50;    (* Arithmetic Mean Insulation Wall Thickness [mm] *)
    rUS_EccentricityVector_X_mm         : REAL := 0.285;    (* Spatial Eccentricity Vector Component X [mm] *)
    rUS_EccentricityVector_Y_mm         : REAL := 0.192;    (* Spatial Eccentricity Vector Component Y [mm] *)
    rUS_EccentricityRatio_pct           : REAL := 2.850;    (* Concentricity Deviation Ratio E_pct [%] *)

    (* 4.6 Dual Caterpillar Capstan Tension & Electronic Line Shaft Registers *)
    rCapstan_InfeedActualSpeed_mpm      : REAL := 25.00;    (* Measured Infeed Metering Caterpillar Speed [m/min] *)
    rCapstan_HaulOffActualSpeed_mpm     : REAL := 25.00;    (* Measured Haul-Off Pulling Caterpillar Speed [m/min] *)
    rCapstan_ElectronicShaftError_mpm   : REAL := 0.000;    (* Speed Synchronization Mismatch [m/min] *)
    rCapstan_TensionIntegralAccum_kN    : REAL := 0.000;    (* Tension Closed-Loop Integral Error Accumulator [kN*s] *)

    (* ========================================================================================= *)
    (* 5. ISA-18.2 MULTI-TIERED ALARM THRESHOLDS & HYSTERESIS DEADBANDS                          *)
    (* ========================================================================================= *)
    c_rTrip_MeltPress_HH_bar            : REAL := 480.00;   (* Extruder Rupture High-Pressure Fast Trip [bar] *)
    c_rAlarm_MeltPress_H_bar            : REAL := 440.00;   (* Elevated Extruder Head Pressure Warning [bar] *)
    c_rAlarm_MeltPress_L_bar            : REAL := 280.00;   (* Low Extruder Head Pressure Warning [bar] *)
    c_rTrip_MeltPress_LL_bar            : REAL := 220.00;   (* Extruder Starvation / Void Formation Trip [bar] *)
    c_rDeadband_MeltPress_bar           : REAL := 5.000;    (* Melt Pressure Alarm Hysteresis Deadband [bar] *)

    c_rTrip_CatenarySag_HH_mm           : REAL := 150.50;   (* Tube Wall Contact Bottom Hazard Trip [mm] *)
    c_rAlarm_CatenarySag_H_mm           : REAL := 146.50;   (* Catenary Sag High Warning (Sagging) [mm] *)
    c_rAlarm_CatenarySag_L_mm           : REAL := 138.50;   (* Catenary Sag Low Warning (Over-Tensioned) [mm] *)
    c_rTrip_CatenarySag_LL_mm           : REAL := 134.50;   (* Tube Wall Contact Top Hazard Trip [mm] *)
    c_rDeadband_CatenarySag_mm          : REAL := 0.500;    (* Catenary Sag Alarm Hysteresis Deadband [mm] *)

    c_rTrip_TubeN2Press_HH_bar          : REAL := 12.000;   (* CV Tube Overpressure Relief Trip [bar] *)
    c_rAlarm_TubeN2Press_H_bar          : REAL := 10.600;   (* Elevated Tube Nitrogen Pressure Warning [bar] *)
    c_rAlarm_TubeN2Press_L_bar          : REAL := 9.400;    (* Low Tube Nitrogen Pressure Warning [bar] *)
    c_rTrip_TubeN2Press_LL_bar          : REAL := 8.200;    (* Loss of N2 Overpressure Micro-Void Trip [bar] *)
    c_rDeadband_TubeN2Press_bar         : REAL := 0.150;    (* Tube N2 Pressure Alarm Hysteresis Deadband [bar] *)

    c_rTrip_Zone1Temp_HH_degC           : REAL := 435.00;   (* Radiant Heating Zone 1 Thermal Overheat Trip [deg C] *)
    c_rAlarm_Zone1Temp_H_degC           : REAL := 425.00;   (* Radiant Heating Zone 1 High Advisory [deg C] *)
    c_rAlarm_Zone1Temp_L_degC           : REAL := 375.00;   (* Radiant Heating Zone 1 Low Advisory [deg C] *)
    c_rTrip_Zone1Temp_LL_degC           : REAL := 350.00;   (* Insufficient Vulcanization Cross-Linking Trip [deg C] *)
    c_rDeadband_Zone1Temp_degC          : REAL := 2.500;    (* Zone 1 Temperature Alarm Deadband [deg C] *)

    c_rTrip_QuenchWaterLvl_HH_mm        : REAL := 2700.0;   (* Quench Leg High Level Back-Flood Risk Trip [mm] *)
    c_rAlarm_QuenchWaterLvl_H_mm        : REAL := 2450.0;   (* Quench Leg High Water Level Warning [mm] *)
    c_rAlarm_QuenchWaterLvl_L_mm        : REAL := 1550.0;   (* Quench Leg Low Water Level Warning [mm] *)
    c_rTrip_QuenchWaterLvl_LL_mm        : REAL := 1300.0;   (* Quench Leg Low Level Seal Blow-Through Trip [mm] *)
    c_rDeadband_QuenchWaterLvl_mm       : REAL := 30.00;    (* Quench Water Level Deadband [mm] *)

    c_rTrip_HaulOffTension_HH_kN        : REAL := 115.00;   (* Conductor Tensile Rupture Hazard Fast Trip [kN] *)
    c_rAlarm_HaulOffTension_H_kN        : REAL := 95.00;    (* High Haul-Off Line Tension Warning [kN] *)
    c_rAlarm_HaulOffTension_L_kN        : REAL := 20.00;    (* Low Haul-Off Line Tension Warning [kN] *)
    c_rTrip_HaulOffTension_LL_kN        : REAL := 10.00;    (* Conductor Slack / Capstan Slip Trip [kN] *)
    c_rDeadband_HaulOffTension_kN       : REAL := 1.500;    (* Haul-Off Tension Alarm Deadband [kN] *)

    c_rAlarm_Eccentricity_H_pct         : REAL := 4.200;    (* Cable Wall Eccentricity Pre-Warning [%] *)
    c_rTrip_Eccentricity_HH_pct         : REAL := 5.000;    (* Cable Wall Eccentricity Rejection Trip [%] *)

    (* ISA-18.2 First Derivative Rate-of-Change (ROC) Registers *)
    rPrevMeltPress_bar                  : REAL := 385.00;
    rROC_MeltPress_bar_per_s            : REAL := 0.000;
    rPrevCatenarySag_mm                 : REAL := 142.50;
    rROC_CatenarySag_mm_per_s           : REAL := 0.000;
    rPrevTubeN2Press_bar                : REAL := 10.000;
    rROC_TubeN2Press_bar_per_s          : REAL := 0.000;
    rPrevHaulOffTension_kN              : REAL := 62.50;
    rROC_HaulOffTension_kN_per_s        : REAL := 0.000;

    (* Latched Active Alarm Status Bits *)
    bAlarm_MeltPress_HH                 : BOOL := FALSE;
    bAlarm_MeltPress_H                  : BOOL := FALSE;
    bAlarm_MeltPress_L                  : BOOL := FALSE;
    bAlarm_MeltPress_LL                 : BOOL := FALSE;
    bAlarm_MeltPress_ROC                : BOOL := FALSE;
    bAlarm_CatenarySag_HH               : BOOL := FALSE;
    bAlarm_CatenarySag_H                : BOOL := FALSE;
    bAlarm_CatenarySag_L                : BOOL := FALSE;
    bAlarm_CatenarySag_LL               : BOOL := FALSE;
    bAlarm_CatenarySag_ROC              : BOOL := FALSE;
    bAlarm_TubeN2Press_HH               : BOOL := FALSE;
    bAlarm_TubeN2Press_H                : BOOL := FALSE;
    bAlarm_TubeN2Press_L                : BOOL := FALSE;
    bAlarm_TubeN2Press_LL               : BOOL := FALSE;
    bAlarm_TubeN2Press_ROC              : BOOL := FALSE;
    bAlarm_Zone1Temp_HH                 : BOOL := FALSE;
    bAlarm_Zone1Temp_H                  : BOOL := FALSE;
    bAlarm_Zone1Temp_L                  : BOOL := FALSE;
    bAlarm_Zone1Temp_LL                 : BOOL := FALSE;
    bAlarm_QuenchWaterLvl_HH            : BOOL := FALSE;
    bAlarm_QuenchWaterLvl_H             : BOOL := FALSE;
    bAlarm_QuenchWaterLvl_L             : BOOL := FALSE;
    bAlarm_QuenchWaterLvl_LL            : BOOL := FALSE;
    bAlarm_HaulOffTension_HH            : BOOL := FALSE;
    bAlarm_HaulOffTension_H             : BOOL := FALSE;
    bAlarm_HaulOffTension_L             : BOOL := FALSE;
    bAlarm_HaulOffTension_LL            : BOOL := FALSE;
    bAlarm_Eccentricity_HH              : BOOL := FALSE;
    bAlarm_Eccentricity_H               : BOOL := FALSE;
    bAlarm_TMR_MajorDivergence          : BOOL := FALSE;

    (* ========================================================================================= *)
    (* 6. 12-STAGE OPERATIONAL FINITE STATE MACHINE REGISTERS & TIMERS                           *)
    (* ========================================================================================= *)
    rStateTimer_s                       : REAL := 0.0;      (* Active FSM State Duration Chronometer [s] *)
    rRampTimer_s                        : REAL := 0.0;      (* Line Acceleration Ramp Chronometer [s] *)
    rPurgeTimer_s                       : REAL := 0.0;      (* Nitrogen Purge Oxygen Flushing Chronometer [s] *)
    rDepressurizeTimer_s                : REAL := 0.0;      (* Controlled Tube Depressurization Chronometer [s] *)
    rCooldownTimer_s                    : REAL := 0.0;      (* Radiant Heater Cooling Down Chronometer [s] *)
    bStateFirstScan                     : BOOL := TRUE;     (* Edge Trigger for State Initialization *)
    nFSM_PreviousState                  : INT  := 0;        (* Diagnostic Tracking of Prior State *)
    rRampTargetLineSpeed_mpm            : REAL := 0.0;      (* Dynamic Target Speed for Smooth Ramp Profiles [m/min] *)

    (* Miscellaneous Iteration & Temporary Math Registers *)
    nLoop_i                             : INT := 1;
    nLoop_j                             : INT := 1;
    rTempSum                            : REAL := 0.0;
    rTempDiffAB                         : REAL := 0.0;
    rTempDiffBC                         : REAL := 0.0;
    rTempDiffCA                         : REAL := 0.0;
    rMathCosine                         : REAL := 0.0;
    rMathSine                           : REAL := 0.0;
    rCatenaryTerm                       : REAL := 0.0;
END_VAR
"""

if __name__ == "__main__":
    s1 = get_sec1()
    print("Section 1 Length:", len(s1))
