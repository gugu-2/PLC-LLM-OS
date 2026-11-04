# Builder script for FB_Cable_ContinuousVulcanization_TripleExtrusion_Sag
import os
import sys

def build_code():
    code_parts = []
    
    # -------------------------------------------------------------------------
    # 1. HEADER AND FORMULATIONS
    # -------------------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Cable_ContinuousVulcanization_TripleExtrusion_Sag
(* =====================================================================================================================
 * LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
 * COMMERCIAL INDUSTRIAL SECTOR : Electrical Cable & Wire Manufacturing Machinery
 * SYSTEM                       : High-Voltage (132 kV - 400 kV) Power Cable Continuous Vulcanization (CV) Line
 * LINE SPECIFICATION           : Line Speed: Up to 25.0 m/min, Cable Outer Diameter: 95.0 mm (Insulation + Screens)
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
"""
    code_parts.append(header)
    return "".join(code_parts)

if __name__ == "__main__":
    res = build_code()
    print("Header length:", len(res))
