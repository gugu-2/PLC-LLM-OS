# builder script for FB_Automotive_Paint_RoboticBell_Electrostatic_PlenumFlow
import os
import sys
import json
import uuid

def generate_code():
    parts = []
    
    # ---------------------------------------------------------------------------------------------------
    # PART 1: HEADER & EXTENSIVE THEORETICAL FOUNDATION
    # ---------------------------------------------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Automotive_Paint_RoboticBell_Electrostatic_PlenumFlow
(*
========================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET ARCHITECTURE V7 MAX-PERSONA
  COMMERCIAL INDUSTRIAL SECTOR : Automotive & Heavy Commercial Vehicles (Class-A Topcoat / Clearcoat)
  SYSTEM CLASSIFICATION        : Automated Robotic Paint Finishing Booth with High-Speed Rotary Bell
                                 Atomizer (65,000 RPM), 70 kV Electrostatic Cascade Charge Generator,
                                 Dual-Ring Aerodynamic Shaping Air Ring, Closed-Loop Cleanroom Downdraft
                                 Plenum Air Handling (0.35 m/s), and Regenerative Thermal Oxidizer (RTO)
                                 VOC Abatement / Lower Explosive Limit (LEL) Scavenging System.
  SAFETY INTEGRITY LEVEL       : SIL 2 / Cat 3 (PL d) Functional Safety Engine (IEC 61508 / ISO 13849-1)
  HAZARDOUS AREA COMPLIANCE    : Zone 1 / Class I, Division 1, Group D Explosive Atmosphere (ATEX / NFPA 33)
  STANDARDS & SPECIFICATIONS   : NFPA 33 (Standard for Spray Application Using Flammable or Combustible Materials)
                                 NFPA 79 (Electrical Standard for Industrial Machinery)
                                 EN 50050 / EN 50176 (Electrostatic Hand-held & Automatic Spray Equipment)
                                 ISO 2812 (Paints and Varnishes - Determination of Resistance to Liquids)
                                 ISO 4628 (Paints and Varnishes - Evaluation of Degradation of Coatings)
  AUTHOR                       : Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Exp)
========================================================================================================

  THEORETICAL FOUNDATIONS & FIRST-PRINCIPLES CYBER-PHYSICAL DYNAMICS:
  ------------------------------------------------------------------------------------------------------
  1. ROTARY BELL HIGH-SPEED ATOMIZATION & LIGAMENT BREAKUP MECHANICS:
     - Atomization is achieved by feeding liquid coating (solvent-borne / waterborne acrylic, polyurethane,
       or polyester clearcoat) onto the inner dish of a cup rotating at angular velocity omega_bell up to
       65,000 RPM (6806.7 rad/s) driven by an impulse micro-air turbine on ceramic gas-bearings.
     - Centrifugal acceleration a_cent = r_cup * omega_bell^2 forces the liquid to spread radially outward
       across the serrated bell edge in a high-shear micro-film of thickness delta_film < 15 [um].
     - Liquid leaves the serrated serrations as discrete cylindrical filaments/ligaments that undergo
       high-velocity aerodynamic Weber-number Rayleigh-Taylor and Kelvin-Helmholtz instabilities,
       breaking up into micro-droplets governed by the modified Sauter Mean Diameter (SMD / D32) equation:
           SMD = C_bell * (omega_bell)^(-0.6) * (Q_paint)^(0.2) * (sigma_liquid / rho_liquid)^(0.1)  [um]
       where:
         C_bell       : Empirical serrated cup geometric atomization constant (~ 185.0 to 220.0)
         omega_bell   : Cup rotational frequency [RPM]
         Q_paint      : Volumetric paint delivery flow rate [mL/min]
         sigma_liquid : Surface tension of liquid paint formulation [mN/m]
         rho_liquid   : Density of liquid coating [kg/m^3]
     - Tight atomization distribution (SMD target 18.0 to 28.0 um) is paramount: droplets > 45 um cause
       orange-peel defects and gravitational sag, whereas droplets < 10 um lead to solvent flash evaporation
       dry spray and excessive booth overspray contamination.

  2. HIGH-VOLTAGE DIRECT-CHARGE ELECTROSTATIC TRANSFER MECHANICS:
     - A 70.0 [kV] DC negative polarity Cockcroft-Walton cascade power generator embedded in the robot
       wrist charges the conductive paint cup or external charging electrodes, creating an intense
       electrostatic space-charge field E = -grad(V) between the bell atomizer and the earthed car body.
     - Paint droplets acquire a surface electrostatic charge q_drop governed by Pauthenier limit saturation:
           q_drop = 4 * pi * epsilon_0 * p * r_drop^2 * E_local
       where p = 3 * epsilon_r / (epsilon_r + 2), and epsilon_r is the relative dielectric constant.
     - The Coulombic electrodynamic driving force F_elec = q_drop * E accelerates charged droplets toward
       the grounded vehicle sheet metal, creating the electrostatic 'wrap-around' effect on edges, seams,
       and recessed cavities.
     - Overall Transfer Efficiency (TE, eta_transfer) exceeds 85.0 % (compared to 35-45% for non-electrostatic
       air spray guns) governed by the exponential high-voltage field enhancement model:
           eta_transfer = eta_base + Delta_eta_max * (1.0 - EXP(-k_volt * V_electrostatic_kV))  [%]
       where:
         eta_base         : Aerodynamic base transfer efficiency without voltage (~ 48.0 %)
         Delta_eta_max    : Maximum electrostatic transfer gain (~ 42.0 %)
         k_volt           : Voltage ionization field coupling coefficient (~ 0.045 kV^-1)
         V_electrostatic  : Applied cascade tip potential [0.0 to 70.0 kV]
     - Strict spark detection and fast hardware quenching: Ionization current I_hv is sampled at 1 kHz;
       any dI_hv/dt > 500 [uA/ms] or absolute current > 180 [uA] trips the cascade PWM in < 2.0 [ms] to
       prevent incendiary electrostatic discharge in Class I Div 1 explosive atmospheres (NFPA 33 limit < 0.24 mJ).

  3. DUAL-RING SHAPING AIR (INNER / OUTER PATTERN AIR) AERODYNAMICS:
     - High-speed swirling paint clouds emerging from the cup edge are aerodynamically contained and
       collimated by two concentric coaxial micro-nozzle rings behind the cup shroud:
         a. Inner Shaping Air (P_inner [0.5 - 4.5 bar]): Directs high-velocity jet streams axially over
            the bell serrations to detach paint ligaments, prevent back-splattering onto the bell shroud,
            and control near-field droplet trajectory.
         b. Outer Shaping Air (P_outer [0.5 - 5.0 bar]): Provides a protective annular curtain that focuses
            the spray cone footprint width W_pattern between 150 [mm] (cut-in / pillar painting) and
            450 [mm] (broad hood / roof painting) governed by:
                W_pattern = W_0 * (1.0 + k_p_outer * P_outer - k_p_inner * P_inner) * (v_down / v_down_nom)^(-0.25)

  4. CLOSED-LOOP MICRO-GEAR DOSING PUMP & PURGE HYDRAULICS:
     - Fluid paint is metered into the hollow atomizer drive shaft by an ultra-precision positive displacement
       micro-gear dosing pump driven by an explosion-proof synchronous AC servomotor.
     - Volumetric flow rate equation:
           Q_actual = N_pump * V_displacement * eta_volumetric  [mL/min]
       where:
         N_pump         : Pump shaft servo rotational speed [RPM]
         V_displacement : Fixed geometric cavity displacement per revolution (e.g. 0.60 or 1.20 mL/rev)
         eta_volumetric : Volumetric efficiency accounting for Poiseuille back-leakage slip across gear teeth:
                          eta_volumetric = 1.0 - (C_slip * Delta_P_fluid) / (mu_paint * N_pump)
     - Color change cycle: High-speed servo-pneumatic color changer block switches between 24 paint colors
       and solvent/air push lines within 4.5 [s], utilizing rapid push-out, solvent scrubbing, and compressed
       air dry-blow phases.

  5. CLEANROOM DOWNDRAFT AIRFLOW PLENUM BALANCE & RTO VOC RECOVERY:
     - The automotive spray booth operates under strict vertical laminar downdraft airflow (v_down = 0.35 +/- 0.03 m/s)
       filtered through ceiling diffusion media (EN 779 F5/ISO ePM10 85%) and drawn through floor grating
       into scrubber water wash / dry overspray separation plenums.
     - Air handling unit (AHU) closed-loop maintains tight psychrometric tolerances:
         Temperature: 23.0 +/- 0.5 [deg C], Relative Humidity: 65.0 +/- 2.0 [% RH]
       preventing paint solvent pre-evaporation or moisture blushing.
     - Flammable solvent VOCs (butyl acetate, xylene, PMA, ethylbenzene) evaporated from the applied paint
       film are continuously exhausted to a Regenerative Thermal Oxidizer (RTO) operating at 850 [deg C].
     - Lower Explosive Limit (LEL) concentration in exhaust plenums is actively regulated:
         LEL_actual < 20.0 [% LEL] (NFPA 33 safety mandate: automatic spray interlock trip at >= 25.0 % LEL).

  6. 6-STATE CYBER-PHYSICAL STATE-SPACE FORMULATION (Ts = 0.010 [s] / 10 [ms]):
     - State Vector x[6]:
         x[1] = Delta_Q_flow    : Paint volumetric flow rate deviation [mL/min]
         x[2] = Delta_N_bell    : Bell turbine rotational speed deviation [RPM]
         x[3] = Delta_V_hv      : Electrostatic cascade high-voltage deviation [kV]
         x[4] = Delta_v_down    : Booth vertical downdraft air velocity deviation [m/s]
         x[5] = Delta_W_pattern : Spray pattern footprint width deviation [mm]
         x[6] = Delta_LEL_voc   : Exhaust plenum solvent VOC concentration deviation [% LEL]
     - Control Input Vector u[6]:
         u[1] = Servo_Pump_RPM  : Micro-gear dosing pump servo motor speed command [0.0 - 500.0 RPM]
         u[2] = Turbine_Drive_% : Bell air turbine proportional drive valve command [0.0 - 100.0 %]
         u[3] = Cascade_PWM_%   : High-voltage cascade PWM duty cycle command [0.0 - 100.0 %]
         u[4] = OuterAir_Valv_% : Outer shaping air pressure proportioning valve command [0.0 - 100.0 %]
         u[5] = InnerAir_Valv_% : Inner shaping air pressure proportioning valve command [0.0 - 100.0 %]
         u[6] = Plenum_VFD_%    : Booth supply/exhaust plenum fan VFD speed command [0.0 - 100.0 %]
     - Disturbance Vector w[6]:
         w[1] = Paint viscosity drift due to shear-thinning thixotropic breakdown
         w[2] = Turbine air supply header pressure fluctuations
         w[3] = Car body geometry surface curvature and grounding resistance variance
         w[4] = Floor filter media paint sludge particulate loading resistance
         w[5] = Robot wrist motion speed and centrifugal Coriolis fluid deflection
         w[6] = Solvent evaporation rate variance from fast-changing vehicle surface area
*)
"""
    parts.append(header)
    return parts

if __name__ == "__main__":
    p = generate_code()
    print("Header lines:", len(p[0].splitlines()))
