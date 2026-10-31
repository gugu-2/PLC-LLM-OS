import json
import os
import re

def build_dairy_spray_dryer():
    # Construct the IEC 61131-3 Structured Text Function Block
    header = """FUNCTION_BLOCK FB_Dairy_ContinuousMultiStage_SprayDryer_FluidBed
(*
====================================================================================================
  LUMINA CYBER-PHYSICAL AUTOMATION ARCHITECTURE - SYNTHETIC IEC 61131-3 DATASET ENGINE
  SYSTEM DESIGNATION: CPS-DAIRY-SPRAYDRYER-MULTISTAGE-FLUIDBED-V7
  DOMAIN ASSIGNMENT: Food & Dairy Processing: Multi-Stage Industrial Milk Powder Spray Dryer with
                     Integrated Internal Fluid Bed, Rotary Atomizer & Exhaust Cyclone Psychrometric
                     Moisture Control
  STANDARDS COMPLIANCE:
    - IEC 61131-3 3rd Edition (Deterministic Industrial Automation Structured Text)
    - 3-A Sanitary Standards (ANSI/3-A 00-01, 3-A 607-05 Spray Drying Systems for Milk & Milk Products)
    - EHEDG (European Hygienic Engineering & Design Group) Guidelines Doc 3, 17, 26 (Hygienic Powder Plants)
    - NFPA 68 / NFPA 69 (Standard on Explosion Protection by Deflagration Venting & Prevention Systems)
    - ATEX Directive 2014/34/EU (Zone 20 Internal Chamber, Zone 21 Cyclones & Fluid Bed, Zone 22 Surrounding)
    - FDA 21 CFR Part 117 (Current Good Manufacturing Practice for Human Food - Pathogen & Moisture Control)
    - ISO 22000 / FSSC 22000 (Food Safety Management Systems - Dairy Powder Quality Critical Control Points)
    - CODEX STAN 207-1999 (Standard for Milk Powders and Cream Powder - Residual Moisture <= 3.5%)
    - ISA-18.2 / EEMUA 191 (Management of Alarm Systems for the Process Industries)
    - IEC 61508 / IEC 61511 (Functional Safety SIL-2/SIL-3 Safety Instrumented Functions)
  PERSONA:
    Principal Automation Fellow & Cyber-Physical Systems Chair (75+ Years Industrial Systems Tenure)
====================================================================================================
  MATHEMATICAL & CYBER-PHYSICAL PROCESS SPECIFICATION:

  1. MULTI-STAGE SPRAY DRYING THERMODYNAMICS & MASS BALANCE:
     Multi-stage industrial drying of milk concentrate (50% w/w total solids TS) into instantized,
     agglomerated whole/skim milk powder involves three sequential thermo-physical dewatering stages:
     a) Primary Spray Chamber Evaporation:
        Concentrated liquid milk is dispersed into billions of micro-droplets (Sauter mean diameter
        d_32 = 65 - 85 um) by a high-speed rotary wheel atomizer (15,000 - 22,000 RPM, peripheral tip
        speed 150 - 180 m/s). The droplets encounter co-current hot drying air (inlet air 190 - 220 deg C,
        volumetric flow 40,000 - 55,000 m3/h) introduced through ceiling air dispersers.
        Instantaneous surface water flash evaporation cools the surrounding gas envelope down to the
        adiabatic saturation wet-bulb temperature (45 - 52 deg C), protecting milk protein (micellar
        casein and native whey globulins) from thermal denaturation and preserving functional solubility.
        Chamber bulk evaporation rate:
          M_evap [kg/h] = M_feed * (TS_inlet / TS_outlet - 1.0)
     b) Integrated Internal Fluid Bed (IFB):
        Partially dried, sticky milk powder particles (moisture 8.0 - 12.0%) settle gently into the
        static internal fluid bed at the chamber conical bottom. Secondary conditioning air (70 - 85 deg C)
        fluidizes the agglomerate cake, driving moisture down to 4.5 - 6.0% while preventing caramelization.
     c) External Vibrating Fluid Bed (VFB):
        The agglomerates discharge continuously into an external horizontal vibrating fluid bed:
          - Zone 1 (Finish Drying): Warm dry air (70 - 80 deg C) removes bound capillary moisture down
            to the strict target of 3.0 - 3.5%.
          - Zone 2 (Dehumidified Cooling): Chilled, conditioned dehumidified air (15 - 18 deg C, RH < 25%)
            chills powder below its glass transition temperature prior to pneumatic conveying and packing.

  2. PSYCHROMETRIC EXHAUST AIR FORMULATION & ABSOLUTE HUMIDITY INTEGRATION:
     Online tracking of water evaporation relies on exhaust air psychrometric properties.
     Exhaust dry-bulb temperature T_exh [deg C], relative humidity RH_exh [%], and barometric pressure
     P_baro [mbar] are measured via redundant instruments.
     a) Saturated Vapor Pressure P_sat via the Magnus-Tetens Formulation:
          P_sat(T) = 6.1121 * exp( (17.502 * T) / (240.97 + T) )  [mbar]
     b) Partial Water Vapor Pressure P_v:
          P_v = (RH_exh / 100.0) * P_sat(T_exh)  [mbar]
     c) Absolute Humidity Y_out [g H2O / kg dry air]:
          Y_out = 621.98 * P_v / (P_baro - P_v)
     d) Dew Point Temperature T_dew [deg C]:
          alpha_dew = ln( P_v / 6.1121 )
          T_dew = (240.97 * alpha_dew) / (17.502 - alpha_dew)
     e) Humid Specific Heat c_s and Specific Enthalpy h_air:
          c_s = 1.006 + 1.860 * (Y_out / 1000.0)  [kJ / (kg dry air * K)]
          h_air = 1.006 * T_exh + (Y_out / 1000.0) * (2501.0 + 1.860 * T_exh)  [kJ / kg dry air]

  3. AMORPHOUS LACTOSE GLASS TRANSITION & AGGLOMERATE STICKINESS KINETICS:
     Milk powder contains 38 - 52% amorphous lactose. At high moisture and temperature, lactose passes
     from a metastable glassy solid to a sticky rubbery state, causing catastrophic powder plastering
     onto chamber walls and fluid bed clumping.
     The glass transition temperature T_g is modeled via the Gordon-Taylor formulation:
       T_g(w_w) = ( w_s * T_gs + k_gt * w_w * T_gw ) / ( w_s + k_gt * w_w )
     where:
       T_gs = 101.0 deg C (glass transition of anhydrous pure amorphous lactose)
       T_gw = -135.0 deg C (glass transition of pure amorphous water)
       k_gt = 6.70 (Gordon-Taylor empirical curvature constant for dairy matrices)
       w_w  = Water weight fraction [kg water / kg total powder]
       w_s  = Solids weight fraction [1.0 - w_w]
     Sticky Point Boundary:
       T_sticky = T_g(w_w) + Delta_T_stick  (Delta_T_stick = 14.5 deg C)
     The MPC controller continuously maintains powder particle temperature below T_sticky to guarantee
     free-flowing powder discharge and clean chamber walls.
     Water activity a_w is dynamically estimated via the Guggenheim-Anderson-de Boer (GAB) isotherm:
       X_eq(a_w) = (X_m * C_gab * K_gab * a_w) / [ (1 - K_gab * a_w) * (1 - K_gab * a_w + C_gab * K_gab * a_w) ]
     Target shelf-stable milk powder specification: a_w < 0.20, moisture = 3.20 +/- 0.15% w/w.

  4. DISCRETE STATE-SPACE MODEL (16x16 SYSTEM: x[k+1] = A*x[k] + B*u[k]):
     State Vector x (16 states):
       x[1]:  Chamber inlet hot air delivery temperature T_in [deg C]
       x[2]:  Chamber upper evaporative zone gas temperature T_cham [deg C]
       x[3]:  Exhaust duct discharge air temperature T_exh [deg C]
       x[4]:  Exhaust air absolute humidity Y_exh [g H2O / kg dry air]
       x[5]:  Droplet surface moisture content X_surf [% dry basis]
       x[6]:  Chamber cone bulk powder moisture X_cone [% wet basis]
       x[7]:  Chamber wall powder deposition accumulation H_wall [mm]
       x[8]:  Internal fluid bed (IFB) powder core temperature T_ifb [deg C]
       x[9]:  Internal fluid bed (IFB) powder residual moisture X_ifb [%]
       x[10]: IFB fluidization differential pressure drop DP_ifb [mbar]
       x[11]: Vibrating fluid bed Zone 1 finish drying temperature T_vfb1 [deg C]
       x[12]: Vibrating fluid bed Zone 2 cooling powder temperature T_vfb2 [deg C]
       x[13]: Final discharged powder residual moisture X_out [%]
       x[14]: Final discharged powder water activity a_w [-]
       x[15]: Cyclone battery differential pressure drop DP_cyc [mbar]
       x[16]: Chamber static draft vacuum pressure P_draft [Pa] (target -80 Pa)
     Control Input Vector u (8 inputs):
       u[1]: High-pressure milk concentrate feed pump delivery flow Q_feed [l/h]
       u[2]: Indirect gas furnace burner modulating firing command X_gas [%]
       u[3]: Rotary atomizer high-speed spindle VFD speed N_atom [rpm]
       u[4]: Main exhaust ID (induced draft) suction fan speed N_idfan [%]
       u[5]: Main supply FD (forced draft) supply fan speed N_fdfan [%]
       u[6]: Internal fluid bed (IFB) hot air modulating valve command X_ifb [%]
       u[7]: External VFB Zone 2 dehumidified cooling air valve command X_vfb [%]
       u[8]: Cyclone fines return blower rotary feeder speed N_fines [rpm]

  5. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION:
     Solves an unrolled receding-horizon quadratic optimization with input rate and amplitude constraints:
       min_u J = 0.5 * sum_{i=1..16} Q[i] * (x[i] - x_ref[i])^2
               + 0.5 * sum_{j=1..8}  R[j] * (u[j])^2
               + 0.5 * sum_{j=1..8}  Rd[j] * (u[j] - u_prev[j])^2
               + 0.5 * sum_{i=1..16} P[i] * (x_next[i] - x_ref[i])^2
     Gradient descent solver evaluates the multi-variable sensitivity gradient, updating candidate
     inputs while enforcing physical actuator saturation and slew rate limiters. Enforces chamber draft
     vacuum safety envelope (-120 Pa < P_draft < -40 Pa) to prevent toxic hot powder dust leakage or
     chamber wall implosion.

  6. 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) ARCHITECTURE:
     Triplicated sensor arrays for five safety- and quality-critical loops:
       a) Exhaust Air Temperature RTDs (A, B, C) [deg C]
       b) Exhaust Air Relative Humidity Transmitters (A, B, C) [%]
       c) Chamber Explosion Vent Rupture Disc Pressure Sensors (A, B, C) [bar]
       d) Chamber Static Vacuum Draft Transmitters (A, B, C) [Pa]
       e) Rotary Atomizer Spindle Vibration Accelerometers (A, B, C) [mm/s RMS]
     Voting executes middle-value selection (median) when all 3 channels are healthy, degrades to
     average of 2 healthy channels upon single-channel discrepancy timeout (tau = 2.0 s), and latches
     fail-safe trip upon dual-channel failure.
====================================================================================================
*)
"""
    return header

print("Header builder ready")
