# -*- coding: utf-8 -*-
"""
Full Generator for FB_Biopharma_PerfusionBioreactor_ATF_OffGas
"""

import sys
import os
import json
import re

def build_code():
    parts = []
    
    # 1. Header & Title
    parts.append("""FUNCTION_BLOCK FB_Biopharma_PerfusionBioreactor_ATF_OffGas
(*
 ====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - ULTRA-RIGOROUS SYNTHETIC DATASET V7 MAX-PERSONA
  DOMAIN: BIOTECHNOLOGY & BIOPHARMACEUTICAL PROCESSING (TIER 1 GLOBAL HIGH-DEMAND AUTOMATION)
  SYSTEM: 20,000-LITER COMMERCIAL MAMMALIAN CELL CULTURE PERFUSION BIOREACTOR COMPLEX:
          - ALTERNATING TANGENTIAL FLOW (ATF) HOLLOW-FIBER MEMBRANE CELL RETENTION SYSTEM
            (DIAPHRAGM PUMP CYCLIC VACUUM/PRESSURE OSCILLATION WITH DYNAMIC TMP CONTROL AND
             AUTOMATED ANTIFOULING REVERSE PERMEATE BACKPULSE)
          - 4-GAS MASS FLOW CONTROLLER CASCADE SPARGING (O2, N2, CO2, AIR FOR DISSOLVED OXYGEN
            dO2 REGULATION 30.0% TO 60.0% AIR SAT AND pH 6.90 TO 7.20 VIA CO2 ACID TRIM AND
            SODIUM BICARBONATE BASE DOSING)
          - IN-LINE LASER RAMAN SPECTROSCOPY & CAPACITANCE BIOMASS PROBE (REAL-TIME VIABLE CELL
            DENSITY VCD > 80.0 x 10^6 CELLS/ML, GLUCOSE, GLUTAMINE, LACTATE & AMMONIUM MONITORING)
          - RESPIROMETRIC OFF-GAS MASS SPECTROMETER (CONTINUOUS CALCULATION OF OXYGEN UPTAKE RATE OUR,
            CARBON DIOXIDE EVOLUTION RATE CER, AND RESPIRATORY QUOTIENT RQ)
          - PRECISION THERMAL CIRCULATION JACKET (+/- 0.05 deg C TEMPERATURE STABILITY AT 37.0 deg C)
  MODULE: FB_Biopharma_PerfusionBioreactor_ATF_OffGas
 ====================================================================================================
  MATHEMATICAL FOUNDATION & BIOPROCESS KINETICS:
   1. CELL GROWTH & METABOLISM KINETICS (EXTENDED MONOD / LUEDEKING-PIRET):
      - Specific growth rate mu [1/h]:
        mu = mu_max * (S_glc / (K_s_glc + S_glc)) * (K_i_lac / (K_i_lac + S_lac)) *
             (S_gln / (K_s_gln + S_gln)) * (K_i_amm / (K_i_amm + S_amm)) - k_death
      - Viable Cell Density (VCD) mass balance:
        d(VCD)/dt = (mu - D_bleed) * VCD - k_lysis * VCD
      - Glucose consumption rate:
        q_glc = (1 / Y_x_glc) * mu + m_glc
      - Lactate generation and consumption kinetics:
        q_lac = Y_lac_glc * q_glc - q_lac_uptake * (S_glc_threshold / (S_glc + S_glc_threshold))
   2. RESPIROMETRY & GAS TRANSFER DYNAMICS:
      - Oxygen Uptake Rate (OUR) [mmol/(L*h)]:
        OUR = (F_in / V_L) * (C_in_O2 - ((1 - y_in_O2 - y_in_CO2)/(1 - y_out_O2 - y_out_CO2)) * y_out_O2)
      - Carbon Dioxide Evolution Rate (CER) [mmol/(L*h)]:
        CER = (F_in / V_L) * (((1 - y_in_O2 - y_in_CO2)/(1 - y_out_O2 - y_out_CO2)) * y_out_CO2 - C_in_CO2)
      - Respiratory Quotient (RQ):
        RQ = CER / OUR
      - Specific Oxygen Uptake Rate (qO2) [pmol/(cell*h)]:
        qO2 = (OUR * 10^9) / (VCD * 10^6 * 1000)
      - Volumetric mass transfer coefficient kLa [1/h]:
        OTR = kLa * (C_star_O2 - C_L_O2) = OUR + d(C_L_O2)/dt
   3. ALTERNATING TANGENTIAL FLOW (ATF) FILTRATION & DARCY MEMBRANE HYDRODYNAMICS:
      - Transmembrane Pressure (TMP) [bar]:
        TMP = (P_ret_inlet + P_ret_outlet) / 2.0 - P_permeate
      - Darcy's Permeate Flux Law:
        J_v = TMP / (mu_viscosity * (R_membrane + R_cake_layer + R_pore_blocking))
      - Alternating Diaphragm Cycle:
        * Pressure Stroke: Diaphragm pushed upward by pneumatic air, expelling retentate into bioreactor
          at high tangential shear rate (gamma_w > 2500 s^-1) scouring membrane lumen.
        * Exhaust/Vacuum Stroke: Diaphragm drawn downward by vacuum header, aspirating broth into ATF bulb.
      - Dynamic Antifouling Backpulse:
        Triggered when TMP > TMP_backpulse_threshold, reversing permeate flow for t_bp seconds.
   4. 4-GAS MFC CASCADE SPARGING & DISSOLVED CO2 / pH TRIM:
      - Henry's Law equilibrium: [CO2_aq] = K_H * P_CO2_headspace
      - Carbonic acid / bicarbonate buffer equilibrium:
        pH = pKa + log10([HCO3-] / [CO2_aq])
      - Decoupled dual-action pH control:
        * pH > SP: Acid trim by sparging CO2 gas micro-bubbles.
        * pH < SP: Base addition by sodium bicarbonate (0.5 M NaHCO3) peristaltic dosing.
   5. PRECISION THERMAL CIRCULATION JACKET:
      - Bioreactor thermal mass M_broth = 20,000 kg, C_p = 4.184 kJ/(kg*K).
      - Jacket heat exchange UA = 18.5 kW/K.
      - Dual modulating split-range valves: Steam injection for heating and chilled water (4.0 deg C)
        for metabolic heat removal.
   6. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING:
      - 5 critical transducer triplets (15 physical sensors):
        dO2 (Optical fluorescence), pH (Pressurized gel), Broth Temp (Pt100 4-wire RTD),
        ATF Retentate Pressure, ATF Permeate Pressure.
      - Pairwise discrepancy debouncing (500 ms to 1500 ms) and bumpless fallback (2oo3 -> 1oo2 -> Fail-Safe).
   7. MULTIVARIABLE DISCRETE STATE-SPACE MODEL & RECEDING-HORIZON MPC:
      - 8-State Formulation @ Ts = 10 ms:
        x1: Broth Temperature [deg C] (Nominal 37.00 deg C)
        x2: Dissolved Oxygen dO2 [% air sat] (Nominal 50.00 %)
        x3: Liquid Broth pH [-] (Nominal 7.050)
        x4: Viable Cell Density VCD [10^6 cells/mL] (Nominal 85.00 x 10^6 cells/mL)
        x5: Glucose Substrate Concentration [g/L] (Nominal 4.50 g/L)
        x6: Lactate Concentration [g/L] (Nominal 1.20 g/L)
        x7: Transmembrane Pressure TMP [bar] (Nominal 0.180 bar)
        x8: Carbon Dioxide Evolution Rate CER [mmol/(L*h)] (Nominal 18.50 mmol/(L*h))
      - 6 Actuator Controls:
        u1: Sparger O2 Mass Flow [SLPM]
        u2: Sparger CO2 Mass Flow [SLPM]
        u3: Fresh Perfusion Feed Pump Speed [RPM]
        u4: Permeate Harvest Pump Speed [RPM]
        u5: Thermal Jacket Coolant Control Valve [%]
        u6: Base Dosing Metering Pump Speed [RPM]
      - Receding Horizon MPC with Projected Gradient Descent quadratic cost optimization.
   8. DETERMINISTIC 12-STAGE FINITE STATE MACHINE (FSM):
      - State 0:  STATE_VESSEL_CIP_SIP_HOLD
      - State 1:  STATE_STERILE_MEDIA_FILL_EQUILIBRATION
      - State 2:  STATE_INOCULATION_SEED_GROWTH
      - State 3:  STATE_EXPONENTIAL_GROWTH_TRANSITION
      - State 4:  STATE_ATF_PERFUSION_CUTIN
      - State 5:  STATE_STEADY_STATE_HIGH_DENSITY_CHEMOSTAT
      - State 6:  STATE_NUTRIENT_FEED_OPTIMIZATION
      - State 7:  STATE_ANTIFOAM_MICRODOSING
      - State 8:  STATE_MEMBRANE_ANTIFOULING_BACKPULSE
      - State 9:  STATE_HARVEST_CLARIFICATION_CONCENTRATION
      - State 10: STATE_POST_HARVEST_THERMAL_DEACTIVATION
      - State 11: STATE_STERILE_VESSEL_HOLD_DRAIN
 ====================================================================================================
*)""")
    return parts

print("build_code initialized.")
