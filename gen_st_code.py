# gen_st_code.py - Full Structured Text Assembler for FB_Pharma_Lyophilizer_FreezeDrying_Sublimation

import re
import json
import os

def generate_header():
    return """FUNCTION_BLOCK FB_Pharma_Lyophilizer_FreezeDrying_Sublimation
(*
========================================================================================================================
LUMINA CYBER-PHYSICAL AUTOMATION ENGINE - SYNTHETIC DATASET V7 MAX-PERSONA
PHARMACEUTICALS & BIOPROCESS DIVISION - INDUSTRIAL ASEPTIC PRODUCTION FREEZE DRYER (LYOPHILIZER)
========================================================================================================================
SYSTEM SPECIFICATION:
  - Equipment Architecture:
    * Production-Scale Industrial Freeze Dryer with 50.0 m2 Total Usable Shelf Surface Area.
    * Ten (10) 316L Stainless Steel Internal Heat Transfer Shelves (5.0 m2 per shelf, 1000 mm x 5000 mm).
    * Holding Capacity: 150,000 Standard 10R Type I Borosilicate Glass Tubing Vials (approx. 450 Liters liquid drug).
    * Biopharmaceutical Formulation: High-Concentration Monoclonal Antibody (mAb) in Sucrose/Mannitol Lyo Cake.
    * Critical Formulation Metrics:
        - Glass Transition Temperature of Maximally Freeze-Concentrated Solute (Tg_prime): -30.0 deg C.
        - Critical Viscoelastic Product Collapse Temperature (T_collapse): -28.5 deg C.
        - Target Sublimation Front Temperature Setpoint: -31.5 deg C (Safety margin > 3.0 deg C below collapse).
        - Target Final Residual Moisture Content: < 1.0% w/w bound moisture.
  - Thermal Fluid Circulation & Refrigeration Skid:
    * Silicone Oil (Polydimethylsiloxane Syltherm XLT) Recirculating Circuit (Total Inventory: 1,850 Liters).
    * Inflow Circulation Pumps: Dual Hermetic Canned Motor Pumps delivering up to 450 L/min at 4.2 bar.
    * Shelf Temperature Operating Range: -55.0 deg C to +60.0 deg C with ramp rates up to 1.5 deg C/min.
    * Shelf Temperature Spatial Uniformity: Within +/- 0.50 deg C across all 50.0 m2 shelf surface area.
    * Primary Refrigeration: Dual-Stage Semi-Hermetic Screw Compressors with Economizer and Stepless Slide Valve.
    * Rapid Cooling Cryogenic Booster: Direct Liquid Nitrogen (LN2) Plate Heat Exchanger Injection Module.
    * Primary Heating Skid: 72.0 kW Modulated SCR Thyristor Electric In-Line Heat Exchanger.
  - High-Vacuum Condensing Chamber & Ice Condenser Vessel:
    * Cylindrical External Ice Condenser Vessel with Heavy-Duty 316L Coils (Sublimation Capacity > 800 kg Ice).
    * Condenser Coil Operating Temperature: Down to -80.0 deg C (Direct Expansion Cascade / Cryogenic R23/R404A).
    * Main Isolation Valve: DN600 Stainless Steel Electro-Hydraulic Mushroom Poppet Isolation Valve.
    * Vacuum Pumping Train: Two-Stage Dry Roots Mechanical Booster Blowers + Rotary Multi-Lobe Dry Screw Pumps.
    * Ultimate Base Chamber Vacuum: < 0.008 mbar (8.0 ubar); Operational Control Range: 0.040 to 0.300 mbar.
  - Dynamic Chamber Pressure Regulation (Sterile Micro-Bleed Gas Dosing):
    * High-Purity Dry Nitrogen (Grade 5.0, H2O < 2 ppm, O2 < 1 ppm) dosed through sterile 0.22 um hydrophobic PTFE filters.
    * Modulated Proportional Piezoelectric / Solenoid Needle Bleed Valve for precision chamber pressure setpoint control.
    * Elevates convective vial heat transfer coefficient (Kv) while strictly preventing vapor choking in the duct.
  - In-Situ Dual-Gauge Metrology & Sublimation Endpoint Determination:
    * Triple Modular Redundant (2oo3 TMR) Temperature-Controlled Heated Capacitance Manometers (MKS Baratron 45 deg C).
    * Triple Modular Redundant (2oo3 TMR) Thermal Conductivity Pirani Vacuum Gauges (Calibrated against Dry N2).
    * Metrology Physics: Pirani gauge detects higher apparent pressure during primary drying due to the higher thermal
      conductivity of water vapor relative to nitrogen (approx 1.6x higher). Primary drying endpoint is mathematically
      established when Pirani indication drops and converges onto Capacitance Manometer reading (Delta_P < 0.005 mbar).
    * Automated Chamber Pressure Rise Rate Test (PRT) verification executed upon endpoint convergence detection.
  - Controlled Ice Nucleation Technology:
    * Depressurization Ice Fog / Sterile Nitrogen Bubbling module inducing instantaneous crystallization at -5.0 deg C.
    * Synchronizes ice crystal formation across all 150,000 vials to yield uniform pore structure and fast sublimation.
  - In-Chamber Automated Hydraulic Stoppering Ram:
    * Electro-Hydraulic Power Unit (210 to 250 bar line pressure) driving a vertical stainless steel bellows-sealed ram.
    * Collapsible telescoping tie-rods compress all 10 shelves downwards to fully insert fluted rubber stoppers.
    * Triple Load Cell Array ensuring balanced, validated stoppering compaction force (200 to 260 kN total force).
  - 16x16 Discrete State-Space Model & Receding-Horizon Model Predictive Control (MPC):
    * Fully models shelf oil convective heat transfer, vial bottom contact resistance, ice cake sublimation front kinetics,
      chamber vapor transport resistance, ice condenser frost layer insulation, and Pirani gas mixture dynamics.
  - ISA-18.2 Multi-Tiered Alarm Matrix with Deadband Hysteresis & Diagnostic Telemetry Word Packing.
========================================================================================================================
*)
"""

print("Header generator loaded.")
