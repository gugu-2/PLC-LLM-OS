import os
import json
import uuid
import re

# Constructing FB_Semiconductor_Cleanroom_ISO3_HVAC_Cascade

def build_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # PART 1: Function Block Declaration & Architectural Specification Header
    # -------------------------------------------------------------------------
    header = """FUNCTION_BLOCK FB_Semiconductor_Cleanroom_ISO3_HVAC_Cascade

(*
========================================================================================================================
 CYBER-PHYSICAL SYSTEM ARCHITECTURAL SPECIFICATION & AEROTHERMODYNAMIC DERIVATION
 DOMAIN: SEMICONDUCTOR & WAFER FAB INFRASTRUCTURE: CLASS 1 (ISO 3) CLEANROOM RECIRCULATING AIR HANDLING UNIT (RAHU)
 SUBSYSTEMS:
   1. Active Laminar Airflow Face Velocity Regulation & Acoustic Vibration Dampening (FFU Matrix)
   2. Critical Differential Pressure Cascade Envelope Hierarchy (Litho Bay > Etch Bay > Gown > Corridor)
   3. Precision Psychrometric Dew-Point and Dry-Bulb Temperature Regulation (Chilled Water, DX Trim, Steam)
   4. Airborne Molecular Contamination (AMC) Adsorption Kinetics & Chemical Filter Life Tracking
   5. Discrete State-Space Model (16x16 State Transition Matrix A, 16x8 Input Matrix B, C, D, E)
   6. Receding-Horizon Model Predictive Control (MPC) with Fast Projected Gradient Descent QP Solver
   7. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite with Bumpless Degradation
   8. 12-Stage Cleanroom Operational Finite State Machine (FSM)
   9. ISA-18.2 Multi-Tiered Alarm Matrix and Bit-Packed Telemetry Words
 STANDARDS COMPLIANCE:
   - ISO 14644-1:2015 Cleanrooms and Associated Controlled Environments (Class 1 / ISO 3, <= 10 particles/m3 @ 0.2 um)
   - SEMI E78-0309: Guide to Assess and Control Electrostatic Discharge (ESD) and Charge-Induced Particle Ingress
   - SEMI F21-95: Classification of Airborne Molecular Contaminants (AMC) in Clean Environments
   - SEMI S2-0715: Environmental, Health, and Safety Guideline for Semiconductor Manufacturing Equipment
   - IEST-RP-CC002.4: Unidirectional Flow Cleanrooms and Air Velocity Uniformity Testing
   - ISA-18.2-2016: Management of Alarm Systems for the Process Industries
========================================================================================================================

                             SEMICONDUCTOR CLASS 1 (ISO 3) RECIRCULATION AIR ARCHITECTURE
                             
                    +--------------------------------------------------------------+
                    |           MAKE-UP AIR UNIT (MAU) OUTSIDE AIR INTAKE          |
                    |     [G4 Pre-Filter + F9 Bag + Chemical Scrubber + Pre-Cool]   |
                    +------------------------------+-------------------------------+
                                                   | Pressurized Make-Up Air Flow [m3/h]
                                                   V
         +========================================================================================+
         |                        RAHU RECIRCULATION CEILING PLENUM (+45 Pa)                      |
         |         Chilled Water Cooling Coil (CW) | Direct Expansion Trim (DX) | Steam Reheat    |
         +========================================================================================+
             |                     |                     |                     |               |
             V                     V                     V                     V               V
       +-----------+         +-----------+         +-----------+         +-----------+   +-----------+
       | FFU 01-04 |         | FFU 05-08 |         | FFU 09-12 |         | FFU 13-16 |   | Bypass /  |
       | EC Motors |         | EC Motors |         | EC Motors |         | EC Motors |   | Relief    |
       | U16 ULPA  |         | U16 ULPA  |         | U16 ULPA  |         | U16 ULPA  |   | Damper    |
       +-----------+         +-----------+         +-----------+         +-----------+   +-----------+
             |                     |                     |                     |               |
             |  Uniform Downward Laminar Piston Airflow: v_face = 0.450 m/s +/- 0.030 m/s      |
             V                     V                     V                     V               V
       +------------------------------------------------------------------------------------------+
       |                      CRITICAL LITHOGRAPHY SCANNER BAY (ZONE 1)                           |
       |   Positive Pressure: +25.0 Pa +/- 1.0 Pa rel. to Ambient | Particles: ISO Class 1 (ISO 3)|
       |   Dry-Bulb Temp: 22.00 deg C +/- 0.05 deg C | Dew-Point Temp: 9.50 deg C +/- 0.10 deg C  |
       |   Micro-Vibration Limit: VC-E (< 0.050 mm/s RMS @ 1 Hz - 100 Hz floor vibration)        |
       +------------------------------------------------------------------------------------------+
               |                     |                     |                             |
               | [Perforated Raised  | [Wafer Transfer     | [Personnel Airlock          |
               |  Pedestal Floor]    |  Pass-Through]      |  Interlock Doors]           |
               V                     V                     V                             |
         +===========+         +===========+         +===========+                       |
         | SUB-FAB   |         | ETCH BAY  |         | GOWN ROOM |                       |
         | RETURN AIR|         | (ZONE 2)  |         | (ZONE 3)  |                       |
         | PLENUM    |         | +15.0 Pa  |         | +10.0 Pa  |                       |
         +===========+         +===========+         +===========+                       |
               |                     |                     |                             |
               |                     +----------+----------+                             |
               |                                |                                        |
               |                                V                                        |
               |                       +=================+                               |
               |                       | MAIN CORRIDOR   |                               |
               |                       | (ZONE 4) +5.0 Pa|                               |
               |                       +=================+                               |
               |                                |                                        |
               |                                V                                        |
               |                       +=================+                               |
               |                       | AMBIENT OUTSIDE |                               |
               |                       | 0.0 Pa REF      |                               |
               |                       +=================+                               |
               |                                                                         |
               +-----------------------------<-------------------------------------------+
                               Recirculation Return Air Risers [m3/h]

------------------------------------------------------------------------------------------------------------------------
 1. FLUID DYNAMICS & AERODYNAMIC RESISTANCE ACROSS ULPA FILTER MEDIA
------------------------------------------------------------------------------------------------------------------------
 In semiconductor photolithography cleanrooms (EUV and ArFi scanners), the cleanroom ceiling comprises 100% filter
 coverage with Ultra-Low Penetration Air (ULPA) filters (EN 1822 Grade U16: 99.99995% MPPS efficiency, or Grade U17).
 The laminar face velocity through the cleanroom envelope is governed by Darcy's Law for porous media flow combined with
 the Forchheimer non-linear inertial extension at high flow velocities:
 
   DeltaP_ULPA / t_media = (mu_air(T) / kappa_Darcy) * v_face + beta_Forchheimer * rho_air * v_face^2
 
 where:
   DeltaP_ULPA      = Static pressure drop across ULPA filter pack [Pa] (Nominal clean: 95 Pa @ 0.45 m/s)
   t_media          = Pleated glass-microfiber media pack effective thickness [m]
   kappa_Darcy      = Darcy media permeability coefficient [m^2] (Nominal: 3.25e-11 m^2)
   beta_Forchheimer = Media inertial form coefficient [m^-1] (Nominal: 1.85e+5 m^-1)
   v_face           = Downward face velocity [m/s] (Target setpoint: 0.450 m/s)
   rho_air          = Moist air density [kg/m^3] = P_baro / (R_da * T_K * (1 + 0.608 * W))
   mu_air(T)        = Dynamic air viscosity [Pa*s], calculated online via Sutherland's equation:
                      mu_air(T) = mu_ref * (T / T_ref)^1.5 * (T_ref + S_c) / (T + S_c)
                      where mu_ref = 1.716e-5 Pa*s, T_ref = 273.15 K, S_c = 110.4 K.
 
 The total cleanroom volumetric flow rate for a 500 m2 cleanroom bay is:
   Q_recirc = Area_ceiling * v_face = 500.0 m2 * 0.45 m/s = 225.0 m3/s = 810,000 m3/h.
 At a cleanroom ceiling height of 3.6 m (bay volume V_bay = 1,800 m3), this produces:
   Air Changes per Hour (ACH) = 810,000 / 1,800 = 450 air changes/hour!
 This extreme recirculating airflow volume flushes all human-borne or robotic wear particulates in under 8.0 seconds.

------------------------------------------------------------------------------------------------------------------------
 2. CRITICAL DIFFERENTIAL PRESSURE CASCADE ENVELOPE HIERARCHY
------------------------------------------------------------------------------------------------------------------------
 Wafer yields are destroyed by cross-contamination if airflow directions ever reverse across physical partitions.
 To enforce absolute unidirectional barrier containment, an active pressure cascade envelope is maintained:
   P_Litho (+25.0 Pa) > P_Etch (+15.0 Pa) > P_Gown (+10.0 Pa) > P_Corridor (+5.0 Pa) > P_Ambient (0.0 Pa)
 
 The air leakage through door perimeters, pass-through slots, and transient open doorways follows the orifice flow equation:
   Q_leak = C_discharge * A_leak * sqrt( 2.0 * |DeltaP| / rho_air ) * sgn(DeltaP)
 
 When a personnel airlock door opens:
   - Door opening area expands from A_leak_sealed = 0.008 m2 to A_door_open = 2.10 m2.
   - Outrush air velocity across door threshold: v_out = sqrt( 2 * (25 - 10) / 1.185 ) = 5.03 m/s.
   - Immediate volumetric outrush loss: Q_out = 0.62 * 2.10 * 5.03 = 6.55 m3/s (23,580 m3/h).
   - If uncompensated, Lithography Bay pressure P_Litho will collapse from +25 Pa to +11 Pa within 420 ms!
   - This control block uses PRE-EMPTIVE FEEDFORWARD BOOSTER ACTION: As soon as the airlock proximity switch signals
     an open request, the Make-Up Air Unit (MAU) booster damper is pulsed open, and FFU speeds are boosted by +85 rpm
     before physical door unsealing, holding the pressure envelope solidly above +22.0 Pa throughout the transit cycle.

------------------------------------------------------------------------------------------------------------------------
 3. PRECISION PSYCHROMETRICS: DRY-BULB & DEW-POINT REGULATION
------------------------------------------------------------------------------------------------------------------------
 Extreme Ultraviolet (EUV) and Deep Ultraviolet (DUV) photolithography scanners require ultra-tight environmental stability:
   - Dry-Bulb Temperature: T_db = 22.00 deg C +/- 0.050 deg C (+/- 0.020 deg C inside scanner enclosure)
   - Relative Humidity:     RH   = 45.0% +/- 0.50% RH
   - Saturated Vapor Pressure P_sat(T) via Magnus-Tetens Formulation:
       P_sat(T) = 610.78 * exp( (17.27 * T) / (T + 237.3) )  [Pa]
   - Partial Vapor Pressure: P_v = (RH / 100.0) * P_sat(T_db) [Pa]
   - Dew-Point Temperature T_dp is determined by inverting Magnus-Tetens:
       gamma(T, RH) = (17.27 * T) / (T + 237.3) + ln(RH / 100.0)
       T_dp = (237.3 * gamma) / (17.27 - gamma)  [deg C]
       At T_db = 22.00 deg C and RH = 45.0%, T_dp = 9.507 deg C.
   - Humidity Ratio W [kg_water / kg_dry_air]:
       W = 0.62198 * P_v / (P_baro - P_v)
   - Specific Enthalpy h_moist [kJ/kg_dry_air]:
       h = 1.006 * T_db + W * (2501.0 + 1.86 * T_db)
 
 Decoupled Thermodynamic Actuation Suite:
   1. Primary Chilled Water Cooling Coil (CW Valve %): Regulates gross sensible heat removal from 350 kW scanner load.
   2. Direct Expansion (DX) Trim Stage (%): Ultra-fast electronic expansion valve modulating refrigerant evaporator
      temperature for high-frequency sub-tenth degree dry-bulb micro-trimming.
   3. Clean Steam Humidifier (%): Pure deionized steam injection to compensate for dry make-up air winter moisture deficits.
   4. Modulating Electric SCR Reheat Coil (%): Counteracts dehumidification subcooling to maintain constant enthalpy.

------------------------------------------------------------------------------------------------------------------------
 4. AIRBORNE MOLECULAR CONTAMINATION (AMC) ADSORPTION DYNAMICS
------------------------------------------------------------------------------------------------------------------------
 Chemical filters (activated carbon with chemical impregnants: phosphoric acid for bases, potassium hydroxide for acids)
 capture airborne molecular contaminants that degrade semiconductor processes:
   - Volatile Organic Compounds (VOCs, e.g. PGMEA, IPA, siloxanes): target < 0.50 ppb
   - Ammonia & Amines (NH3, causes lithographic chemically amplified photoresist "T-topping"): target < 0.10 ppb
   - Acidic Gases (SO2, NOx, HCl, causing scanner lens hazing and copper corrosion): target < 0.10 ppb
 
 Adsorption is modeled online via the Langmuir Isotherm:
   q_adsorbed = q_max * (K_L * C_gas) / (1.0 + K_L * C_gas)  [mg/g carbon]
 Residual chemical filter life is tracked by integrating cumulative mass capture:
   dM_adsorbed/dt = Q_air * (C_upstream - C_downstream) * eta_capture
 As cumulative mass approaches saturation breakthrough capacity M_crit, the FSM triggers filter replacement pacing.

------------------------------------------------------------------------------------------------------------------------
 5. DISCRETE STATE-SPACE FORMULATION (16x16 SYSTEM)
------------------------------------------------------------------------------------------------------------------------
 The cleanroom multi-zone aerothermal plant is represented at discrete sample period T_s = 50 ms (20 Hz):
   x[k+1] = A * x[k] + B * u[k] + E * d[k]
   y[k]   = C * x[k] + D * u[k]
 
 State Vector x in R^16:
   x[1]  = DeltaP_Litho_Pa     : Lithography bay differential pressure relative to ambient [Pa]
   x[2]  = DeltaP_Etch_Pa      : Etch bay differential pressure relative to ambient [Pa]
   x[3]  = DeltaP_Gown_Pa      : Gown room differential pressure relative to ambient [Pa]
   x[4]  = DeltaP_Plenum_Pa    : Recirculation ceiling plenum pressure [Pa]
   x[5]  = v_Laminar_mps       : Cleanroom downward laminar face velocity [m/s]
   x[6]  = T_DryBulb_degC      : Cleanroom dry-bulb air temperature [deg C]
   x[7]  = T_DewPoint_degC     : Cleanroom dew-point temperature [deg C]
   x[8]  = C_VOC_ppb           : Airborne VOC concentration [ppb]
   x[9]  = C_NH3_ppb           : Airborne Ammonia concentration [ppb]
   x[10] = C_SO2_ppb           : Airborne Sulfur Dioxide concentration [ppb]
   x[11] = T_CoilSurf_degC     : Chilled water cooling coil surface temperature [deg C]
   x[12] = T_Reheat_degC       : Reheat electric coil discharge air temperature [deg C]
   x[13] = W_MoistAir_gpkg     : Cleanroom specific humidity ratio [g_water / kg_air]
   x[14] = N_FFU_Avg_rpm       : Average FFU motor rotational speed [rpm]
   x[15] = Flow_MAU_m3ph       : Make-up air intake volumetric flow rate [m3/h]
   x[16] = Vib_RMS_mps2        : FFU ceiling plenum acoustic vibration RMS acceleration [mm/s RMS]
 
 Control Input Vector u in R^8:
   u[1]  = Cmd_FFU_Speed_rpm       : FFU EC fan bank collective speed setpoint [rpm] (0 - 1800 rpm)
   u[2]  = Cmd_MAU_SupplyDamp_pct  : Make-up air supply modulating damper position [%] (0 - 100%)
   u[3]  = Cmd_ExhaustDamp_pct     : Cleanroom relief / exhaust damper position [%] (0 - 100%)
   u[4]  = Cmd_ChilledWaterVlv_pct : Chilled water primary coil modulating valve [%] (0 - 100%)
   u[5]  = Cmd_DX_TrimCoil_pct     : Electronic expansion valve direct-expansion trim [%] (0 - 100%)
   u[6]  = Cmd_SteamHumidifier_pct : Pure clean steam electric humidifier modulating power [%] (0 - 100%)
   u[7]  = Cmd_ReheatCoil_pct      : Electric SCR reheat power [%] (0 - 100%)
   u[8]  = Cmd_AirlockBooster_pct  : Fast-acting airlock pressure pulse booster damper [%] (0 - 100%)
 
 Output Vector y in R^8:
   y[1] = DeltaP_Litho_Pa      : Lithography bay differential pressure [Pa]
   y[2] = DeltaP_Cascade_Pa    : Critical cascade margin (P_Litho - P_Etch) [Pa]
   y[3] = v_Laminar_mps        : Laminar downward face velocity [m/s]
   y[4] = T_DryBulb_degC       : Cleanroom dry-bulb temperature [deg C]
   y[5] = T_DewPoint_degC      : Cleanroom dew-point temperature [deg C]
   y[6] = AMC_Total_ppb        : Aggregated AMC gas concentration [ppb]
   y[7] = Vib_RMS_mps2         : Plenum acoustic vibration level [mm/s RMS]
   y[8] = FilterDeltaP_Pa      : ULPA filter media differential pressure drop [Pa]
 
 Disturbance Vector d in R^6:
   d[1] = Airlock_DoorState_Open   : Airlock door unsealed / opening state factor (0.0 to 1.0)
   d[2] = Ambient_Temp_degC        : Outside ambient dry-bulb temperature [deg C]
   d[3] = Ambient_RH_pct           : Outside ambient relative humidity [%]
   d[4] = Tool_HeatLoad_kW         : Semiconductor scanner & tool sensible heat dissipation [kW]
   d[5] = Fab_ExhaustLoss_m3ph     : Litho track & wet bench scrubbed chemical exhaust draw [m3/h]
   d[6] = Baro_Pressure_Pa         : Outside barometric pressure variation [Pa]

------------------------------------------------------------------------------------------------------------------------
 6. RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) FORMULATION
------------------------------------------------------------------------------------------------------------------------
 An online Model Predictive Controller minimizes the multivariable tracking error while penalizing actuator movement
 and enforcing strict physical and safety constraints:
   J(u) = (x_k - r_k)^T * Q * (x_k - r_k) + Delta_u^T * R * Delta_u + (x_pred - r_k)^T * P * (x_pred - r_k)
 
 The condensed quadratic program (QP) is resolved online at 20 Hz using a projected gradient descent algorithm:
   Grad_J = H * Delta_u + g_k
   Delta_u^(i+1) = Project_{box}( Delta_u^(i) - alpha * Grad_J )
 Actuator slew rate limits [Delta_u_min, Delta_u_max] and absolute travel boundaries [u_min, u_max] are strictly
 maintained. Feedforward anticipatory compensation injects instantaneous damper and fan trims upon door sensor triggers.

------------------------------------------------------------------------------------------------------------------------
 7. TRIPLE MODULAR REDUNDANCY (2oo3 TMR) SENSOR VOTING ARCHITECTURE
------------------------------------------------------------------------------------------------------------------------
 For all safety-critical parameters (Lithography Differential Pressure, Laminar Airflow Face Velocity, Dry-Bulb Air
 Temperature, and Dew-Point Temperature), triple physical sensors are deployed across separate electrical conduits:
   - Median Voting: y_voted = median(Ch_A, Ch_B, Ch_C)
   - Pairwise Deviation Checks: |Ch_A - Ch_B| > Tol, |Ch_B - Ch_C| > Tol, |Ch_C - Ch_A| > Tol
   - Discrepancy Persistence Counters: Faults latch only after consecutive persistence cycles to filter electrical spikes.
   - Graceful Degradation Hierarchy:
       3 Channels Healthy -> 2oo3 Median Voter (Full SIL 3 fault masking)
       1 Channel Faulty   -> 1oo2 Dual-Channel Average Voter with Discrepancy Alert
       2 Channels Faulty   -> 1oo1 Single-Channel Degraded Mode with Conservative Setpoint Clamps
       3 Channels Faulty   -> Safe Fallback Default Actuator Trip to Emergency Recirculation
*)
"""
    parts.append(header)
    
    # -------------------------------------------------------------------------
    # PART 2: VAR_INPUT, VAR_OUTPUT, VAR declarations
    # -------------------------------------------------------------------------
    var_input = """
VAR_INPUT
    (* ========================================================================================= *)
    (* CRITICAL LITHOGRAPHY BAY DIFFERENTIAL PRESSURE SENSORS (2oo3 TMR CHANNELS)               *)
    (* ========================================================================================= *)
    rPressDiff_Litho_ChA_Pa     : REAL;     (* Litho bay vs Ambient differential pressure Ch A [Pa] *)
    rPressDiff_Litho_ChB_Pa     : REAL;     (* Litho bay vs Ambient differential pressure Ch B [Pa] *)
    rPressDiff_Litho_ChC_Pa     : REAL;     (* Litho bay vs Ambient differential pressure Ch C [Pa] *)

    (* ========================================================================================= *)
    (* ADJACENT BAY & CASCADE PRESSURE TRANSDUCERS                                               *)
    (* ========================================================================================= *)
    rPressDiff_Etch_Pa          : REAL;     (* Etch bay vs Ambient differential pressure [Pa] *)
    rPressDiff_Gown_Pa          : REAL;     (* Gown room vs Ambient differential pressure [Pa] *)
    rPressDiff_Corridor_Pa      : REAL;     (* Service corridor vs Ambient differential pressure [Pa] *)
    rPressDiff_Plenum_Pa        : REAL;     (* Recirculation ceiling plenum static pressure [Pa] *)
    rPressDiff_ULPA_Filter_Pa   : REAL;     (* Measured differential pressure across ULPA filter pack [Pa] *)

    (* ========================================================================================= *)
    (* LAMINAR AIRFLOW FACE VELOCITY HOT-WIRE ANEMOMETERS (2oo3 TMR CHANNELS)                    *)
    (* ========================================================================================= *)
    rVelocity_Face_ChA_mps      : REAL;     (* Cleanroom downward laminar face velocity Ch A [m/s] *)
    rVelocity_Face_ChB_mps      : REAL;     (* Cleanroom downward laminar face velocity Ch B [m/s] *)
    rVelocity_Face_ChC_mps      : REAL;     (* Cleanroom downward laminar face velocity Ch C [m/s] *)

    (* ========================================================================================= *)
    (* PRECISION DRY-BULB AIR TEMPERATURE RTD SENSORS (2oo3 TMR CHANNELS)                       *)
    (* ========================================================================================= *)
    rTemp_DryBulb_ChA_degC      : REAL;     (* Cleanroom dry-bulb air temperature Ch A [deg C] *)
    rTemp_DryBulb_ChB_degC      : REAL;     (* Cleanroom dry-bulb air temperature Ch B [deg C] *)
    rTemp_DryBulb_ChC_degC      : REAL;     (* Cleanroom dry-bulb air temperature Ch C [deg C] *)

    (* ========================================================================================= *)
    (* PRECISION DEW-POINT CHILLED MIRROR HYGROMETERS (2oo3 TMR CHANNELS)                        *)
    (* ========================================================================================= *)
    rTemp_DewPoint_ChA_degC     : REAL;     (* Cleanroom chilled mirror dew point Ch A [deg C] *)
    rTemp_DewPoint_ChB_degC     : REAL;     (* Cleanroom chilled mirror dew point Ch B [deg C] *)
    rTemp_DewPoint_ChC_degC     : REAL;     (* Cleanroom chilled mirror dew point Ch C [deg C] *)

    (* ========================================================================================= *)
    (* PSYCHROMETRIC & ENVIRONMENTAL TRANSMITTERS                                                *)
    (* ========================================================================================= *)
    rHumidity_Rel_pct           : REAL;     (* Cleanroom relative humidity [ %RH] *)
    rTemp_Ambient_degC          : REAL;     (* Outside ambient air dry-bulb temperature [deg C] *)
    rHumidity_Ambient_pct       : REAL;     (* Outside ambient air relative humidity [ %RH] *)
    rBaroPressure_hPa           : REAL;     (* Barometric ambient atmospheric pressure [hPa] *)

    (* ========================================================================================= *)
    (* AIRBORNE MOLECULAR CONTAMINATION (AMC) REAL-TIME GAS ANALYZERS                           *)
    (* ========================================================================================= *)
    rConc_VOC_ppb               : REAL;     (* Volatile Organic Compounds gas concentration [ppb] *)
    rConc_NH3_ppb               : REAL;     (* Ammonia / basic gas concentration [ppb] *)
    rConc_SO2_ppb               : REAL;     (* Sulfur Dioxide / acidic gas concentration [ppb] *)

    (* ========================================================================================= *)
    (* HYDRAULIC, FLOW, ACOUSTIC & ELECTRICAL SENSOR TRANSMITTERS                                *)
    (* ========================================================================================= *)
    rFlow_MAU_Supply_m3ph       : REAL;     (* Make-up air intake flow rate [m3/h] *)
    rFlow_ScrubbedExhaust_m3ph  : REAL;     (* Process tool local scrubbed exhaust flow draw [m3/h] *)
    rPress_ChilledWater_bar     : REAL;     (* Chilled water primary supply line pressure [bar] *)
    rTemp_ChilledWaterSupply_degC: REAL;    (* Chilled water supply line temperature [deg C] *)
    rVib_FFU_Plenum_mms_RMS     : REAL;     (* FFU ceiling plenum acoustic vibration [mm/s RMS] *)
    rCurrent_FFU_Matrix_A       : REAL;     (* FFU EC motor bank total current consumption [mA] *)
    rPower_ScannerHeatLoad_kW   : REAL;     (* EUV / DUV Lithography scanner sensible heat load [kW] *)

    (* ========================================================================================= *)
    (* DISCRETE SYSTEM COMMANDS, INTERLOCKS & DOOR SENSORS                                       *)
    (* ========================================================================================= *)
    bMasterEnable               : BOOL;     (* Main Cleanroom HVAC Cascade Master Control Enable *)
    bEmergencyStop              : BOOL;     (* Hardwired Cleanroom Safety Bus Trip (Active Low) *)
    bSmokeToxicGasAlarm         : BOOL;     (* Fab life safety toxic gas / smoke detection trip *)
    bAirlockDoorOpenReq         : BOOL;     (* Personnel airlock transit request button / radar *)
    bAirlockDoorUnsealed        : BOOL;     (* Personnel airlock magnetic seal open status *)
    bPassThroughDoorOpen        : BOOL;     (* Wafer cassette pass-through hatch door open status *)
    bNightSetbackCommand        : BOOL;     (* Fab production night setback / economy mode command *)
    bFilterTareCalibrationReq   : BOOL;     (* Request zero-flow differential pressure tare *)
    bResetLatchedFaults         : BOOL;     (* Latched alarm clear push-button command *)
    tCycleTime_ms               : REAL;     (* PLC Task scan cycle period [ms] *)
END_VAR

VAR_OUTPUT
    (* ========================================================================================= *)
    (* PRIMARY ACTUATOR MODULATION COMMANDS                                                      *)
    (* ========================================================================================= *)
    rCmd_FFU_Speed_rpm          : REAL;     (* Collective FFU EC motor rotational speed setpoint [rpm] *)
    rCmd_MAU_SupplyDamper_pct   : REAL;     (* Make-up Air Unit modulating supply damper [ %] *)
    rCmd_ExhaustDamper_pct      : REAL;     (* Cleanroom relief / exhaust air modulating damper [ %] *)
    rCmd_ChilledWaterValve_pct  : REAL;     (* Primary chilled water cooling coil valve position [ %] *)
    rCmd_DX_TrimCoil_pct        : REAL;     (* Direct expansion micro-trim refrigerant modulation [ %] *)
    rCmd_SteamHumidifier_pct    : REAL;     (* Clean steam electric humidifier power modulation [ %] *)
    rCmd_ElectricReheat_pct     : REAL;     (* Modulating SCR electric reheat coil power [ %] *)
    rCmd_AirlockBooster_pct     : REAL;     (* Airlock dynamic feedforward pressure booster damper [ %] *)

    (* ========================================================================================= *)
    (* PHYSICAL PROCESS ESTIMATES & PERFORMANCE INDICATORS                                       *)
    (* ========================================================================================= *)
    rEst_LithoDiffPress_Pa      : REAL;     (* Voted Litho bay differential pressure estimate [Pa] *)
    rEst_CascadeMargin_Pa       : REAL;     (* Active cascade envelope margin: P_Litho - P_Etch [Pa] *)
    rEst_LaminarFaceVel_mps     : REAL;     (* Voted downward laminar face velocity [m/s] *)
    rEst_DryBulbTemp_degC       : REAL;     (* Voted cleanroom dry-bulb air temperature [deg C] *)
    rEst_DewPointTemp_degC      : REAL;     (* Voted cleanroom dew-point temperature [deg C] *)
    rEst_MoistAirEnthalpy_kJpkg : REAL;     (* Online psychrometric specific enthalpy [kJ/kg] *)
    rEst_AirChangesPerHour_ACH  : REAL;     (* Effective bay volumetric air turnover rate [ACH] *)
    rEst_ULPA_Resistance_Rayl   : REAL;     (* Estimated ULPA filter dynamic specific flow resistance *)
    rEst_ChemicalFilterLife_pct : REAL;     (* Remaining chemical scrubber adsorption media life [ %] *)
    rEst_AcousticVibRMS_mms     : REAL;     (* Filtered FFU acoustic floor vibration level [mm/s RMS] *)

    (* ========================================================================================= *)
    (* ARINC-429 / MODBUS PACKED BITFIELD TELEMETRY WORDS                                        *)
    (* ========================================================================================= *)
    dwSystemStatusWord          : DWORD;    (* Cleanroom Operating State & Mode Bitfield *)
    dwAlarmWord_Critical        : DWORD;    (* Critical Emergency Tripline Bitmask (ISA-18.2 Cat 1) *)
    dwAlarmWord_High            : DWORD;    (* High Priority Alarm Bitmask (ISA-18.2 Cat 2) *)
    dwAlarmWord_Advisory        : DWORD;    (* Advisory Operating Warning Bitmask (ISA-18.2 Cat 3) *)
    dwSensorVotingStatusWord    : DWORD;    (* TMR Sensor Integrity & Discrepancy Bitmask *)

    (* ========================================================================================= *)
    (* DISCRETE SYSTEM STATUS & INTERLOCK FLAGS                                                  *)
    (* ========================================================================================= *)
    bCleanroomReadyForWafer     : BOOL;     (* All Class 1 parameters verified in tight tolerance *)
    bPressureEnvelopeLocked     : BOOL;     (* Full cascade positive pressure hierarchy verified *)
    bLaminarVelocityUniform     : BOOL;     (* Laminar downward piston flow holding within set limits *)
    bDewPointStable             : BOOL;     (* Dry-bulb and dew point holding within +/- 0.05 C *)
    bDegradedSensorFallback     : BOOL;     (* Subsystem operating in 1oo2 or 1oo1 degraded mode *)
    bToxicPurgeActive           : BOOL;     (* 100% full fresh air toxic gas purge mode engaged *)
END_VAR

VAR
    (* ========================================================================================= *)
    (* 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM) VARIABLES                                 *)
    (* ========================================================================================= *)
    iFSM_State                  : INT := 0;     (* Current Operational FSM State Index *)
    iFSM_PrevState              : INT := 0;     (* Previous FSM State Register *)
    rFSM_StateDwellTime_s       : REAL := 0.0;  (* Continuous dwell time within current state [s] *)
    rScanDeltaTime_s            : REAL := 0.05; (* Execution cycle interval in seconds [s] *)

    (* State Enumeration Constants *)
    STATE_COLD_START_PURGE      : INT := 0;     (* Stage 0: Initial cleanroom volumetric air purge *)
    STATE_FILTER_TARE_CALIB     : INT := 1;     (* Stage 1: Zero-flow ULPA filter pressure drop tare *)
    STATE_FFU_SOFT_START        : INT := 2;     (* Stage 2: FFU EC motor gentle ramp & resonance check *)
    STATE_MAU_THERMAL_COND      : INT := 3;     (* Stage 3: Make-up air thermal conditioning *)
    STATE_OVERPRESSURE_LOCK     : INT := 4;     (* Stage 4: Overpressure cascade envelope establishment *)
    STATE_LAMINAR_VEL_STABIL    : INT := 5;     (* Stage 5: Laminar airflow velocity field stabilization *)
    STATE_AMC_SCRUBBER_PACE     : INT := 6;     (* Stage 6: AMC chemical filtration lock & baseline *)
    STATE_PRODUCTION_READY      : INT := 7;     (* Stage 7: Production ready closed-loop steady state *)
    STATE_AIRLOCK_COMPENSATION  : INT := 8;     (* Stage 8: Active airlock cycle transient compensation *)
    STATE_FILTER_REPLACE_FLUSH  : INT := 9;     (* Stage 9: Filter change-out high-flow particle flush *)
    STATE_NIGHT_SETBACK_STANDBY : INT := 10;    (* Stage 10: Night setback energy saving mode *)
    STATE_TOXIC_GAS_PURGE_TRIP  : INT := 11;    (* Stage 11: Emergency toxic gas / smoke purge exhaust *)

    (* FSM Internal Timers *)
    tonColdStartPurge           : TON;          (* Cold start gross volume turnover timer *)
    tonFilterTareSettle         : TON;          (* Filter zero-flow stabilization timer *)
    tonFFURampTimer             : TON;          (* FFU speed acceleration timer *)
    tonThermalSettleTimer       : TON;          (* Chilled water coil enthalpy balance timer *)
    tonPressureLockTimer        : TON;          (* Cascade envelope hold timer *)
    tonVelocityFieldTimer       : TON;          (* Laminar uniformity dwell timer *)
    tonAirlockHoldTimer         : TON;          (* Door opening transient suppression timer *)
    tonFaultResetHold           : TON;          (* Reset pushbutton anti-chatter qualification timer *)

    (* ========================================================================================= *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE DATA                             *)
    (* ========================================================================================= *)
    (* Voted Sensor Values *)
    rVoted_PressDiff_Litho_Pa   : REAL := 25.0;
    rVoted_Velocity_Face_mps    : REAL := 0.45;
    rVoted_Temp_DryBulb_degC    : REAL := 22.0;
    rVoted_Temp_DewPoint_degC   : REAL := 9.5;

    (* Channel Validity Flags *)
    bPress_ChA_Valid            : BOOL := TRUE;
    bPress_ChB_Valid            : BOOL := TRUE;
    bPress_ChC_Valid            : BOOL := TRUE;
    bPress_ChA_LatchedFault     : BOOL := FALSE;
    bPress_ChB_LatchedFault     : BOOL := FALSE;
    bPress_ChC_LatchedFault     : BOOL := FALSE;

    bVel_ChA_Valid              : BOOL := TRUE;
    bVel_ChB_Valid              : BOOL := TRUE;
    bVel_ChC_Valid              : BOOL := TRUE;
    bVel_ChA_LatchedFault       : BOOL := FALSE;
    bVel_ChB_LatchedFault       : BOOL := FALSE;
    bVel_ChC_LatchedFault       : BOOL := FALSE;

    bTemp_ChA_Valid             : BOOL := TRUE;
    bTemp_ChB_Valid             : BOOL := TRUE;
    bTemp_ChC_Valid             : BOOL := TRUE;
    bTemp_ChA_LatchedFault      : BOOL := FALSE;
    bTemp_ChB_LatchedFault      : BOOL := FALSE;
    bTemp_ChC_LatchedFault      : BOOL := FALSE;

    bDewPt_ChA_Valid            : BOOL := TRUE;
    bDewPt_ChB_Valid            : BOOL := TRUE;
    bDewPt_ChC_Valid            : BOOL := TRUE;
    bDewPt_ChA_LatchedFault     : BOOL := FALSE;
    bDewPt_ChB_LatchedFault     : BOOL := FALSE;
    bDewPt_ChC_LatchedFault     : BOOL := FALSE;

    (* Pairwise Discrepancy Counters *)
    iPress_DevCount_AB          : INT := 0;
    iPress_DevCount_BC          : INT := 0;
    iPress_DevCount_CA          : INT := 0;

    iVel_DevCount_AB            : INT := 0;
    iVel_DevCount_BC            : INT := 0;
    iVel_DevCount_CA            : INT := 0;

    iTemp_DevCount_AB           : INT := 0;
    iTemp_DevCount_BC           : INT := 0;
    iTemp_DevCount_CA           : INT := 0;

    iDewPt_DevCount_AB          : INT := 0;
    iDewPt_DevCount_BC          : INT := 0;
    iDewPt_DevCount_CA          : INT := 0;

    (* Discrepancy Tolerances & Persistence Thresholds *)
    rTol_PressDiff_Pa           : REAL := 3.50;     (* Max permissible pressure discrepancy [Pa] *)
    rTol_Velocity_mps           : REAL := 0.06;     (* Max permissible velocity discrepancy [m/s] *)
    rTol_DryBulb_degC           : REAL := 0.18;     (* Max permissible temperature discrepancy [deg C] *)
    rTol_DewPoint_degC          : REAL := 0.35;     (* Max permissible dew point discrepancy [deg C] *)
    iMaxDiscrepancyCycles       : INT := 10;        (* Discrepancy persistence count before latching fault *)

    (* ========================================================================================= *)
    (* PSYCHROMETRIC AND PROCESS EQUATION INTERNAL VARIABLES                                     *)
    (* ========================================================================================= *)
    rSaturatedVaporPress_Pa     : REAL := 2643.0;   (* Saturated vapor pressure at dry-bulb temp [Pa] *)
    rActualVaporPress_Pa        : REAL := 1189.0;   (* Actual water vapor partial pressure [Pa] *)
    rCalculatedDewPoint_degC    : REAL := 9.51;     (* Magnus-Tetens inverted dew point [deg C] *)
    rHumidityRatio_kgpkg        : REAL := 0.00735;  (* Specific humidity ratio [kg_w / kg_da] *)
    rCalculatedMoistAirEnthalpy : REAL := 40.75;    (* Calculated specific moist air enthalpy [kJ/kg] *)
    rDryAirDensity_kgpm3        : REAL := 1.185;    (* Ambient moist air density [kg/m^3] *)
    rMagnus_Gamma               : REAL := 0.0;      (* Intermediate psychrometric variable *)

    (* Dynamic Air Viscosity via Sutherland Law *)
    rAirDynamicViscosity_Pals   : REAL := 1.82e-5;  (* Sutherland calculated dynamic air viscosity [Pa*s] *)
    rSutherland_T0              : REAL := 273.15;   (* Sutherland reference temperature [K] *)
    rSutherland_Mu0             : REAL := 1.716e-5; (* Sutherland reference dynamic viscosity [Pa*s] *)
    rSutherland_S               : REAL := 110.4;    (* Sutherland constant for dry air [K] *)

    (* ULPA Filter Loading & Flow Resistance *)
    rULPA_TareOffset_Pa         : REAL := 0.0;      (* Zero-flow calibration pressure tare [Pa] *)
    rULPA_NetDeltaP_Pa          : REAL := 95.0;     (* Tare-compensated filter pressure drop [Pa] *)
    rULPA_CleanRefDeltaP_Pa     : REAL := 95.0;     (* Baseline clean filter pressure drop at 0.45 m/s [Pa] *)
    rULPA_LoadingFactor         : REAL := 1.0;      (* Particulate loading resistance factor *)

    (* AMC Chemical Filter Media Adsorption Tracking *)
    rAMC_InitialCapacity_g      : REAL := 150000.0; (* Fresh chemical filter adsorption capacity [g] *)
    rAMC_CumulativeCaptured_g   : REAL := 12500.0;  (* Integrated mass of AMC captured to date [g] *)
    rAMC_CaptureRate_gps        : REAL := 0.0;      (* Instantaneous chemical capture mass rate [g/s] *)
    rAMC_RemainingLife_pct      : REAL := 91.6;     (* Calculated residual chemical life [ %] *)

    (* Biquad Acoustic Vibration Bandpass Filter Variables (1 Hz - 100 Hz @ 20 Hz scan) *)
    rVib_BQ_b0                  : REAL := 0.3125;
    rVib_BQ_b1                  : REAL := 0.0;
    rVib_BQ_b2                  : REAL := -0.3125;
    rVib_BQ_a1                  : REAL := -1.1520;
    rVib_BQ_a2                  : REAL := 0.4850;
    rVib_BQ_w1                  : REAL := 0.0;
    rVib_BQ_w2                  : REAL := 0.0;
    rVib_FiltSample             : REAL := 0.0;
    rVib_VarianceAcc            : REAL := 0.0;
    rVib_FilteredRMS            : REAL := 0.025;

    (* ========================================================================================= *)
    (* DISCRETE STATE-SPACE MODEL MATRICES (16 STATES, 8 CONTROLS, 8 OUTPUTS, 6 DISTURBANCES)    *)
    (* ========================================================================================= *)
    (* Discrete State Transition Matrix A (16x16) *)
    aA : ARRAY[1..16, 1..16] OF REAL := [
        0.9125,  0.0350,  0.0150,  0.0450,  0.0820, -0.0120,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0045,  0.0085, -0.0012,
        0.0280,  0.9250,  0.0210,  0.0380,  0.0650, -0.0080,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0035,  0.0065, -0.0008,
        0.0150,  0.0180,  0.9380,  0.0220,  0.0450, -0.0050,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0025,  0.0045, -0.0005,
        0.0650,  0.0550,  0.0450,  0.8850,  0.1250, -0.0250,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0120,  0.0185, -0.0035,
        0.0120,  0.0080,  0.0050,  0.0250,  0.8950, -0.0025,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0028,  0.0015, -0.0018,
       -0.0005, -0.0002, -0.0001, -0.0012, -0.0150,  0.9420,  0.0350,  0.0000,  0.0000,  0.0000,  0.0520,  0.0480,  0.0120,  0.0002, -0.0035,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000, -0.0080,  0.0120,  0.9350,  0.0000,  0.0000,  0.0000,  0.0280,  0.0050,  0.0850,  0.0001, -0.0025,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000, -0.0025,  0.0000,  0.0000,  0.8650,  0.0120,  0.0050,  0.0000,  0.0000,  0.0000,  0.0000,  0.0018,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000, -0.0015,  0.0000,  0.0000,  0.0080,  0.8720,  0.0020,  0.0000,  0.0000,  0.0000,  0.0000,  0.0012,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000, -0.0018,  0.0000,  0.0000,  0.0040,  0.0015,  0.8680,  0.0000,  0.0000,  0.0000,  0.0000,  0.0014,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000,  0.0050,  0.0250,  0.0150,  0.0000,  0.0000,  0.0000,  0.8950,  0.0000,  0.0000,  0.0000, -0.0085,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000,  0.0020,  0.0180,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.8850,  0.0000,  0.0000, -0.0055,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000, -0.0040,  0.0080,  0.0650,  0.0000,  0.0000,  0.0000,  0.0180,  0.0020,  0.9250,  0.0000, -0.0015,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.9150,  0.0000,  0.0000,
        0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.9050,  0.0000,
        0.0005,  0.0002,  0.0001,  0.0015,  0.0085,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0000,  0.0012,  0.0008,  0.8450
    ];

    (* Control Input Matrix B (16x8) *)
    aB : ARRAY[1..16, 1..8] OF REAL := [
        0.0085,   0.0450,  -0.0380,   0.0000,   0.0000,   0.0000,   0.0000,   0.0650,
        0.0062,   0.0320,  -0.0250,   0.0000,   0.0000,   0.0000,   0.0000,   0.0120,
        0.0045,   0.0210,  -0.0180,   0.0000,   0.0000,   0.0000,   0.0000,   0.0050,
        0.0215,   0.0850,  -0.0520,   0.0000,   0.0000,   0.0000,   0.0000,   0.0250,
        0.00085,  0.0025,  -0.0012,   0.0000,   0.0000,   0.0000,   0.0000,   0.0015,
       -0.00015, -0.0050,   0.0025,  -0.0650,  -0.0250,   0.0085,   0.0450,  -0.0012,
       -0.00008, -0.0035,   0.0015,  -0.0450,  -0.0180,   0.0820,  -0.0025,  -0.0008,
       -0.00005, -0.0085,   0.0045,   0.0000,   0.0000,   0.0000,   0.0000,  -0.0015,
       -0.00004, -0.0062,   0.0035,   0.0000,   0.0000,   0.0000,   0.0000,  -0.0010,
       -0.00003, -0.0055,   0.0028,   0.0000,   0.0000,   0.0000,   0.0000,  -0.0008,
        0.0000,   0.0000,   0.0000,  -0.1250,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.1450,   0.0000,
       -0.00005, -0.0025,   0.0010,  -0.0350,  -0.0120,   0.0950,  -0.0018,  -0.0005,
        0.8850,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0000,   0.9250,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0025,   0.0005,  -0.0002,   0.0000,   0.0000,   0.0000,   0.0000,   0.0005
    ];

    (* Disturbance Matrix E (16x6) *)
    aE : ARRAY[1..16, 1..6] OF REAL := [
       -0.1850,   0.0050,   0.0020,  -0.0010,  -0.0250,   0.0150,
       -0.0450,   0.0035,   0.0015,  -0.0008,  -0.0180,   0.0120,
       -0.0250,   0.0020,   0.0010,  -0.0005,  -0.0085,   0.0080,
       -0.0850,   0.0120,   0.0050,  -0.0025,  -0.0420,   0.0250,
       -0.0150,   0.0005,   0.0002,  -0.0002,  -0.0035,   0.0015,
        0.0085,   0.0450,   0.0120,   0.0850,   0.0025,   0.0000,
        0.0055,   0.0280,   0.0650,   0.0150,   0.0018,   0.0000,
        0.0850,   0.0050,   0.0020,   0.0010,   0.0150,   0.0000,
        0.0650,   0.0035,   0.0015,   0.0008,   0.0085,   0.0000,
        0.0550,   0.0028,   0.0010,   0.0005,   0.0065,   0.0000,
        0.0000,   0.0250,   0.0000,   0.0150,   0.0000,   0.0000,
        0.0000,   0.0150,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0045,   0.0180,   0.0520,   0.0085,   0.0012,   0.0000,
        0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000,
        0.0000,   0.0000,   0.0000,   0.0000,   0.0000,   0.0000
    ];

    (* Output Matrix C (8x16) *)
    aC : ARRAY[1..8, 1..16] OF REAL := [
        1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        1.0,-1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0, 1.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 1.0,
       -1.0, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ];

    (* Direct Feedthrough Matrix D (8x8) *)
    aD : ARRAY[1..8, 1..8] OF REAL := [
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0,
        0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0
    ];

    (* State Penalty Weighting Matrix Q (16x16 diagonal) *)
    aQ : ARRAY[1..16, 1..16] OF REAL := [
        120.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,  85.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,  45.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,  30.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0, 250.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0, 450.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0, 380.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,  95.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0, 110.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0, 110.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,  15.0,   0.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,  15.0,   0.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,  40.0,   0.0,   0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.05,  0.0,   0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.01,  0.0,
          0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0,   0.0, 180.0
    ];

    (* Actuator Penalty Weighting Matrix R (8x8 diagonal) *)
    aR : ARRAY[1..8, 1..8] OF REAL := [
        0.0025, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.8500, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.6500, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 1.2500, 0.0000, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 2.1500, 0.0000, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.4500, 0.0000, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 1.6500, 0.0000,
        0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.0000, 0.3500
    ];

    (* Condensed QP Hessian Matrix H (8x8) *)
    aH : ARRAY[1..8, 1..8] OF REAL := [
        0.0385,  0.0042, -0.0025, -0.0008, -0.0004,  0.0002, -0.0005,  0.0085,
        0.0042,  1.9250, -0.4500, -0.0850, -0.0250,  0.0120, -0.0350,  0.1250,
       -0.0025, -0.4500,  1.4850,  0.0420,  0.0150, -0.0080,  0.0180, -0.0850,
       -0.0008, -0.0850,  0.0420,  2.8500,  0.4200, -0.1500, -0.3200, -0.0150,
       -0.0004, -0.0250,  0.0150,  0.4200,  4.6500, -0.0850, -0.1250, -0.0080,
        0.0002,  0.0120, -0.0080, -0.1500, -0.0850,  3.2500,  0.0650,  0.0050,
       -0.0005, -0.0350,  0.0180, -0.3200, -0.1250,  0.0650,  3.6800, -0.0120,
        0.0085,  0.1250, -0.0850, -0.0150, -0.0080,  0.0050, -0.0120,  0.8950
    ];

    (* State, Control, and Disturbance Vectors *)
    aStateX                     : ARRAY[1..16] OF REAL := [16(0.0)];
    aStateX_Next                : ARRAY[1..16] OF REAL := [16(0.0)];
    aStateX_Pred                : ARRAY[1..16] OF REAL := [16(0.0)];
    aStateError                 : ARRAY[1..16] OF REAL := [16(0.0)];
    aControlU                   : ARRAY[1..8] OF REAL := [1250.0, 45.0, 25.0, 42.0, 15.0, 28.0, 12.0, 0.0];
    aControlU_Prev              : ARRAY[1..8] OF REAL := [1250.0, 45.0, 25.0, 42.0, 15.0, 28.0, 12.0, 0.0];
    aDeltaU                     : ARRAY[1..8] OF REAL := [8(0.0)];
    aGradG                      : ARRAY[1..8] OF REAL := [8(0.0)];
    aOutputY                    : ARRAY[1..8] OF REAL := [8(0.0)];
    aSetpointR                  : ARRAY[1..16] OF REAL := [
        25.0, 15.0, 10.0, 45.0, 0.450, 22.00, 9.50, 0.10, 0.05, 0.05, 12.0, 24.0, 7.35, 1250.0, 15000.0, 0.025
    ];
    aDisturbD                   : ARRAY[1..6] OF REAL := [6(0.0)];

    (* Actuator Hard Operating Limits *)
    rFFU_Speed_Min_rpm          : REAL := 0.0;
    rFFU_Speed_Max_rpm          : REAL := 1800.0;
    rMAU_Damper_Min_pct         : REAL := 10.0;
    rMAU_Damper_Max_pct         : REAL := 100.0;
    rExh_Damper_Min_pct         : REAL := 5.0;
    rExh_Damper_Max_pct         : REAL := 100.0;
    rCW_Valve_Min_pct           : REAL := 0.0;
    rCW_Valve_Max_pct           : REAL := 100.0;
    rDX_Trim_Min_pct            : REAL := 0.0;
    rDX_Trim_Max_pct            : REAL := 100.0;
    rSteam_Hum_Min_pct          : REAL := 0.0;
    rSteam_Hum_Max_pct          : REAL := 100.0;
    rReheat_Min_pct             : REAL := 0.0;
    rReheat_Max_pct             : REAL := 100.0;
    rAirlock_Booster_Min_pct    : REAL := 0.0;
    rAirlock_Booster_Max_pct    : REAL := 100.0;

    (* Actuator Maximum Slew Rates (per second) *)
    rFFU_Speed_RateMax_rpmps    : REAL := 150.0;
    rMAU_Damper_RateMax_pctps   : REAL := 25.0;
    rExh_Damper_RateMax_pctps   : REAL := 25.0;
    rCW_Valve_RateMax_pctps     : REAL := 10.0;
    rDX_Trim_RateMax_pctps      : REAL := 35.0;
    rSteam_Hum_RateMax_pctps    : REAL := 15.0;
    rReheat_RateMax_pctps       : REAL := 20.0;
    rAirlock_Booster_RateMax_pctps: REAL := 80.0;

    (* ========================================================================================= *)
    (* ISA-18.2 MULTI-TIERED ALARM SETPOINTS, HYSTERESIS & DEADBANDS                             *)
    (* ========================================================================================= *)
    (* Differential Pressure Alarms [Pa] *)
    rPress_Litho_SP             : REAL := 25.0;
    rPress_Litho_HH_Trip        : REAL := 35.0;
    rPress_Litho_H_Warn         : REAL := 28.5;
    rPress_Litho_L_Warn         : REAL := 21.5;
    rPress_Litho_LL_Trip        : REAL := 18.0;     (* Critical barrier breach trip *)
    rPress_Hysteresis_Pa        : REAL := 0.8;

    (* Cascade Inversion Trip: Litho must stay >= 5 Pa above Etch Bay! *)
    rPress_CascadeMargin_LL_Trip: REAL := 3.0;      (* Pressure cascade reversal emergency *)

    (* Laminar Airflow Face Velocity Alarms [m/s] *)
    rVel_Face_SP                : REAL := 0.450;
    rVel_Face_HH_Trip           : REAL := 0.580;    (* Turbulence / vortex storm *)
    rVel_Face_H_Warn            : REAL := 0.490;
    rVel_Face_L_Warn            : REAL := 0.410;
    rVel_Face_LL_Trip           : REAL := 0.350;    (* Laminar boundary layer stall *)
    rVel_Hysteresis_mps         : REAL := 0.015;

    (* Dry-Bulb Temperature Alarms [deg C] *)
    rTemp_DryBulb_SP            : REAL := 22.00;
    rTemp_DryBulb_HH_Trip       : REAL := 22.35;    (* Scanner thermal expansion distortion *)
    rTemp_DryBulb_H_Warn        : REAL := 22.12;
    rTemp_DryBulb_L_Warn        : REAL := 21.88;
    rTemp_DryBulb_LL_Trip       : REAL := 21.65;
    rTemp_Hysteresis_degC       : REAL := 0.03;

    (* Dew-Point Temperature Alarms [deg C] *)
    rTemp_DewPoint_SP           : REAL := 9.50;
    rTemp_DewPoint_HH_Trip      : REAL := 10.40;    (* Condensation risk on optics / wafer *)
    rTemp_DewPoint_H_Warn       : REAL := 9.90;
    rTemp_DewPoint_L_Warn       : REAL := 9.10;
    rTemp_DewPoint_LL_Trip      : REAL := 8.50;     (* Static electricity ESD charge hazard *)
    rDewPoint_Hysteresis_degC   : REAL := 0.10;

    (* Acoustic Floor Vibration Limit [mm/s RMS] *)
    rVib_Plenum_HH_Trip         : REAL := 0.080;    (* Scanner optical alignment blur *)
    rVib_Plenum_H_Warn          : REAL := 0.050;    (* VC-E threshold advisory *)

    (* ULPA Differential Pressure Saturation [Pa] *)
    rULPA_HighDeltaP_Warn_Pa    : REAL := 185.0;    (* Filter loading advisory *)
    rULPA_MaxDeltaP_Trip_Pa     : REAL := 240.0;    (* Media blowout structural danger *)

    (* AMC Breakthrough Warning [ppb] *)
    rAMC_VOC_Limit_ppb          : REAL := 0.50;
    rAMC_NH3_Limit_ppb          : REAL := 0.10;
    rAMC_SO2_Limit_ppb          : REAL := 0.10;

    (* Alarm Delay & Persistence Timers *)
    tonPressCascadeReversal     : TON;
    tonLaminarVelocityStall     : TON;
    tonThermalExcursionTrip     : TON;
    tonDewPointExcursionTrip    : TON;
    tonAcousticVibExcess        : TON;

    (* Loop Counters & Temporary Math Scratchpad *)
    iIdx                        : INT := 1;
    jIdx                        : INT := 1;
    kIdx                        : INT := 1;
    iQPIter                     : INT := 0;
    rSumAccum                   : REAL := 0.0;
    rGradStep                   : REAL := 0.085;
    rCandidateU                 : REAL := 0.0;
    rRateLimitDelta             : REAL := 0.0;
END_VAR
"""
    parts.append(var_input)
    
    # -------------------------------------------------------------------------
    # PART 3: Code Body - Sections 1 through 7
    # -------------------------------------------------------------------------
    code_body = """
(*
========================================================================================================================
 SECTION 1: EXECUTION CYCLE TIMING, WATCHDOG PRE-CHECK & SAFETY BUS SUPERVISION
========================================================================================================================
*)
IF tCycleTime_ms > 0.001 THEN
    rScanDeltaTime_s := tCycleTime_ms * 0.001;
ELSE
    rScanDeltaTime_s := 0.05; (* Default 50 ms scan (20 Hz) *)
END_IF;

rFSM_StateDwellTime_s := rFSM_StateDwellTime_s + rScanDeltaTime_s;

(* HARDWIRED CLEANROOM SAFETY BUS & EMERGENCY STOP MONITORING *)
IF NOT bEmergencyStop THEN
    bCleanroomReadyForWafer := FALSE;
    bPressureEnvelopeLocked := FALSE;
    bLaminarVelocityUniform := FALSE;
    bDewPointStable := FALSE;
    dwAlarmWord_Critical.0 := TRUE; (* Safety Bus Interlock Relay Open *)
    iFSM_State := STATE_TOXIC_GAS_PURGE_TRIP;
END_IF;

(* LIFE SAFETY TOXIC GAS / FIRE SMOKE PURGE IMMEDIATE OVERRIDE *)
IF bSmokeToxicGasAlarm THEN
    bToxicPurgeActive := TRUE;
    bCleanroomReadyForWafer := FALSE;
    dwAlarmWord_Critical.1 := TRUE; (* Life Safety Gas / Smoke Detection Trip *)
    iFSM_State := STATE_TOXIC_GAS_PURGE_TRIP;
END_IF;

(* MANUAL / DCS FAULT LATCH RESET LOGIC *)
IF bResetLatchedFaults THEN
    tonFaultResetHold(IN := TRUE, PT := T#2S);
    IF tonFaultResetHold.Q THEN
        bPress_ChA_LatchedFault := FALSE;
        bPress_ChB_LatchedFault := FALSE;
        bPress_ChC_LatchedFault := FALSE;
        bVel_ChA_LatchedFault   := FALSE;
        bVel_ChB_LatchedFault   := FALSE;
        bVel_ChC_LatchedFault   := FALSE;
        bTemp_ChA_LatchedFault  := FALSE;
        bTemp_ChB_LatchedFault  := FALSE;
        bTemp_ChC_LatchedFault  := FALSE;
        bDewPt_ChA_LatchedFault := FALSE;
        bDewPt_ChB_LatchedFault := FALSE;
        bDewPt_ChC_LatchedFault := FALSE;
        dwAlarmWord_Critical    := 16#00000000;
        dwAlarmWord_High        := 16#00000000;
        dwAlarmWord_Advisory    := 16#00000000;
        tonFaultResetHold(IN := FALSE);
    END_IF;
ELSE
    tonFaultResetHold(IN := FALSE);
END_IF;

(*
========================================================================================================================
 SECTION 2: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING SUITE
 Mathematical Implementation:
   - Median selection across 3 physically independent channels for all SIL 3 process variables.
   - Pairwise deviation monitoring with persistent error counters.
   - Fault latching with bumpless degradation: 2oo3 (3 healthy) -> 1oo2 (2 healthy) -> 1oo1 (1 healthy) -> Failsafe.
========================================================================================================================
*)
(* --------------------------------------------------------------------------------------------- *)
(* 2.1 CRITICAL LITHOGRAPHY BAY DIFFERENTIAL PRESSURE VOTER                                      *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rPressDiff_Litho_ChA_Pa - rPressDiff_Litho_ChB_Pa) > rTol_PressDiff_Pa THEN
    iPress_DevCount_AB := iPress_DevCount_AB + 1;
ELSE
    IF iPress_DevCount_AB > 0 THEN iPress_DevCount_AB := iPress_DevCount_AB - 1; END_IF;
END_IF;

IF ABS(rPressDiff_Litho_ChB_Pa - rPressDiff_Litho_ChC_Pa) > rTol_PressDiff_Pa THEN
    iPress_DevCount_BC := iPress_DevCount_BC + 1;
ELSE
    IF iPress_DevCount_BC > 0 THEN iPress_DevCount_BC := iPress_DevCount_BC - 1; END_IF;
END_IF;

IF ABS(rPressDiff_Litho_ChC_Pa - rPressDiff_Litho_ChA_Pa) > rTol_PressDiff_Pa THEN
    iPress_DevCount_CA := iPress_DevCount_CA + 1;
ELSE
    IF iPress_DevCount_CA > 0 THEN iPress_DevCount_CA := iPress_DevCount_CA - 1; END_IF;
END_IF;

IF (iPress_DevCount_AB > iMaxDiscrepancyCycles) AND (iPress_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bPress_ChA_LatchedFault := TRUE;
END_IF;
IF (iPress_DevCount_AB > iMaxDiscrepancyCycles) AND (iPress_DevCount_BC > iMaxDiscrepancyCycles) THEN
    bPress_ChB_LatchedFault := TRUE;
END_IF;
IF (iPress_DevCount_BC > iMaxDiscrepancyCycles) AND (iPress_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bPress_ChC_LatchedFault := TRUE;
END_IF;

bPress_ChA_Valid := NOT bPress_ChA_LatchedFault AND (rPressDiff_Litho_ChA_Pa >= -50.0) AND (rPressDiff_Litho_ChA_Pa <= 150.0);
bPress_ChB_Valid := NOT bPress_ChB_LatchedFault AND (rPressDiff_Litho_ChB_Pa >= -50.0) AND (rPressDiff_Litho_ChB_Pa <= 150.0);
bPress_ChC_Valid := NOT bPress_ChC_LatchedFault AND (rPressDiff_Litho_ChC_Pa >= -50.0) AND (rPressDiff_Litho_ChC_Pa <= 150.0);

IF bPress_ChA_Valid AND bPress_ChB_Valid AND bPress_ChC_Valid THEN
    (* 2oo3 Median Selection *)
    IF ((rPressDiff_Litho_ChA_Pa >= rPressDiff_Litho_ChB_Pa) AND (rPressDiff_Litho_ChA_Pa <= rPressDiff_Litho_ChC_Pa)) OR
       ((rPressDiff_Litho_ChA_Pa <= rPressDiff_Litho_ChB_Pa) AND (rPressDiff_Litho_ChA_Pa >= rPressDiff_Litho_ChC_Pa)) THEN
        rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChA_Pa;
    ELSIF ((rPressDiff_Litho_ChB_Pa >= rPressDiff_Litho_ChA_Pa) AND (rPressDiff_Litho_ChB_Pa <= rPressDiff_Litho_ChC_Pa)) OR
          ((rPressDiff_Litho_ChB_Pa <= rPressDiff_Litho_ChA_Pa) AND (rPressDiff_Litho_ChB_Pa >= rPressDiff_Litho_ChC_Pa)) THEN
        rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChB_Pa;
    ELSE
        rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChC_Pa;
    END_IF;
ELSIF bPress_ChA_Valid AND bPress_ChB_Valid THEN
    rVoted_PressDiff_Litho_Pa := (rPressDiff_Litho_ChA_Pa + rPressDiff_Litho_ChB_Pa) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bPress_ChB_Valid AND bPress_ChC_Valid THEN
    rVoted_PressDiff_Litho_Pa := (rPressDiff_Litho_ChB_Pa + rPressDiff_Litho_ChC_Pa) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bPress_ChA_Valid AND bPress_ChC_Valid THEN
    rVoted_PressDiff_Litho_Pa := (rPressDiff_Litho_ChA_Pa + rPressDiff_Litho_ChC_Pa) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bPress_ChA_Valid THEN
    rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChA_Pa;
    bDegradedSensorFallback := TRUE;
ELSIF bPress_ChB_Valid THEN
    rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChB_Pa;
    bDegradedSensorFallback := TRUE;
ELSIF bPress_ChC_Valid THEN
    rVoted_PressDiff_Litho_Pa := rPressDiff_Litho_ChC_Pa;
    bDegradedSensorFallback := TRUE;
ELSE
    rVoted_PressDiff_Litho_Pa := 25.0; (* Safe baseline default *)
    dwAlarmWord_Critical.2 := TRUE;    (* All 3 Pressure Sensors Failed! *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2.2 LAMINAR AIRFLOW FACE VELOCITY VOTER                                                       *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rVelocity_Face_ChA_mps - rVelocity_Face_ChB_mps) > rTol_Velocity_mps THEN
    iVel_DevCount_AB := iVel_DevCount_AB + 1;
ELSE
    IF iVel_DevCount_AB > 0 THEN iVel_DevCount_AB := iVel_DevCount_AB - 1; END_IF;
END_IF;

IF ABS(rVelocity_Face_ChB_mps - rVelocity_Face_ChC_mps) > rTol_Velocity_mps THEN
    iVel_DevCount_BC := iVel_DevCount_BC + 1;
ELSE
    IF iVel_DevCount_BC > 0 THEN iVel_DevCount_BC := iVel_DevCount_BC - 1; END_IF;
END_IF;

IF ABS(rVelocity_Face_ChC_mps - rVelocity_Face_ChA_mps) > rTol_Velocity_mps THEN
    iVel_DevCount_CA := iVel_DevCount_CA + 1;
ELSE
    IF iVel_DevCount_CA > 0 THEN iVel_DevCount_CA := iVel_DevCount_CA - 1; END_IF;
END_IF;

IF (iVel_DevCount_AB > iMaxDiscrepancyCycles) AND (iVel_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bVel_ChA_LatchedFault := TRUE;
END_IF;
IF (iVel_DevCount_AB > iMaxDiscrepancyCycles) AND (iVel_DevCount_BC > iMaxDiscrepancyCycles) THEN
    bVel_ChB_LatchedFault := TRUE;
END_IF;
IF (iVel_DevCount_BC > iMaxDiscrepancyCycles) AND (iVel_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bVel_ChC_LatchedFault := TRUE;
END_IF;

bVel_ChA_Valid := NOT bVel_ChA_LatchedFault AND (rVelocity_Face_ChA_mps >= 0.0) AND (rVelocity_Face_ChA_mps <= 2.50);
bVel_ChB_Valid := NOT bVel_ChB_LatchedFault AND (rVelocity_Face_ChB_mps >= 0.0) AND (rVelocity_Face_ChB_mps <= 2.50);
bVel_ChC_Valid := NOT bVel_ChC_LatchedFault AND (rVelocity_Face_ChC_mps >= 0.0) AND (rVelocity_Face_ChC_mps <= 2.50);

IF bVel_ChA_Valid AND bVel_ChB_Valid AND bVel_ChC_Valid THEN
    IF ((rVelocity_Face_ChA_mps >= rVelocity_Face_ChB_mps) AND (rVelocity_Face_ChA_mps <= rVelocity_Face_ChC_mps)) OR
       ((rVelocity_Face_ChA_mps <= rVelocity_Face_ChB_mps) AND (rVelocity_Face_ChA_mps >= rVelocity_Face_ChC_mps)) THEN
        rVoted_Velocity_Face_mps := rVelocity_Face_ChA_mps;
    ELSIF ((rVelocity_Face_ChB_mps >= rVelocity_Face_ChA_mps) AND (rVelocity_Face_ChB_mps <= rVelocity_Face_ChC_mps)) OR
          ((rVelocity_Face_ChB_mps <= rVelocity_Face_ChA_mps) AND (rVelocity_Face_ChB_mps >= rVelocity_Face_ChC_mps)) THEN
        rVoted_Velocity_Face_mps := rVelocity_Face_ChB_mps;
    ELSE
        rVoted_Velocity_Face_mps := rVelocity_Face_ChC_mps;
    END_IF;
ELSIF bVel_ChA_Valid AND bVel_ChB_Valid THEN
    rVoted_Velocity_Face_mps := (rVelocity_Face_ChA_mps + rVelocity_Face_ChB_mps) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bVel_ChB_Valid AND bVel_ChC_Valid THEN
    rVoted_Velocity_Face_mps := (rVelocity_Face_ChB_mps + rVelocity_Face_ChC_mps) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bVel_ChA_Valid AND bVel_ChC_Valid THEN
    rVoted_Velocity_Face_mps := (rVelocity_Face_ChA_mps + rVelocity_Face_ChC_mps) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bVel_ChA_Valid THEN
    rVoted_Velocity_Face_mps := rVelocity_Face_ChA_mps;
    bDegradedSensorFallback := TRUE;
ELSIF bVel_ChB_Valid THEN
    rVoted_Velocity_Face_mps := rVelocity_Face_ChB_mps;
    bDegradedSensorFallback := TRUE;
ELSIF bVel_ChC_Valid THEN
    rVoted_Velocity_Face_mps := rVelocity_Face_ChC_mps;
    bDegradedSensorFallback := TRUE;
ELSE
    rVoted_Velocity_Face_mps := 0.450;
    dwAlarmWord_Critical.3 := TRUE;    (* All 3 Face Velocity Sensors Failed! *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2.3 PRECISION DRY-BULB AIR TEMPERATURE VOTER                                                  *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTemp_DryBulb_ChA_degC - rTemp_DryBulb_ChB_degC) > rTol_DryBulb_degC THEN
    iTemp_DevCount_AB := iTemp_DevCount_AB + 1;
ELSE
    IF iTemp_DevCount_AB > 0 THEN iTemp_DevCount_AB := iTemp_DevCount_AB - 1; END_IF;
END_IF;

IF ABS(rTemp_DryBulb_ChB_degC - rTemp_DryBulb_ChC_degC) > rTol_DryBulb_degC THEN
    iTemp_DevCount_BC := iTemp_DevCount_BC + 1;
ELSE
    IF iTemp_DevCount_BC > 0 THEN iTemp_DevCount_BC := iTemp_DevCount_BC - 1; END_IF;
END_IF;

IF ABS(rTemp_DryBulb_ChC_degC - rTemp_DryBulb_ChA_degC) > rTol_DryBulb_degC THEN
    iTemp_DevCount_CA := iTemp_DevCount_CA + 1;
ELSE
    IF iTemp_DevCount_CA > 0 THEN iTemp_DevCount_CA := iTemp_DevCount_CA - 1; END_IF;
END_IF;

IF (iTemp_DevCount_AB > iMaxDiscrepancyCycles) AND (iTemp_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bTemp_ChA_LatchedFault := TRUE;
END_IF;
IF (iTemp_DevCount_AB > iMaxDiscrepancyCycles) AND (iTemp_DevCount_BC > iMaxDiscrepancyCycles) THEN
    bTemp_ChB_LatchedFault := TRUE;
END_IF;
IF (iTemp_DevCount_BC > iMaxDiscrepancyCycles) AND (iTemp_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bTemp_ChC_LatchedFault := TRUE;
END_IF;

bTemp_ChA_Valid := NOT bTemp_ChA_LatchedFault AND (rTemp_DryBulb_ChA_degC >= 10.0) AND (rTemp_DryBulb_ChA_degC <= 40.0);
bTemp_ChB_Valid := NOT bTemp_ChB_LatchedFault AND (rTemp_DryBulb_ChB_degC >= 10.0) AND (rTemp_DryBulb_ChB_degC <= 40.0);
bTemp_ChC_Valid := NOT bTemp_ChC_LatchedFault AND (rTemp_DryBulb_ChC_degC >= 10.0) AND (rTemp_DryBulb_ChC_degC <= 40.0);

IF bTemp_ChA_Valid AND bTemp_ChB_Valid AND bTemp_ChC_Valid THEN
    IF ((rTemp_DryBulb_ChA_degC >= rTemp_DryBulb_ChB_degC) AND (rTemp_DryBulb_ChA_degC <= rTemp_DryBulb_ChC_degC)) OR
       ((rTemp_DryBulb_ChA_degC <= rTemp_DryBulb_ChB_degC) AND (rTemp_DryBulb_ChA_degC >= rTemp_DryBulb_ChC_degC)) THEN
        rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChA_degC;
    ELSIF ((rTemp_DryBulb_ChB_degC >= rTemp_DryBulb_ChA_degC) AND (rTemp_DryBulb_ChB_degC <= rTemp_DryBulb_ChC_degC)) OR
          ((rTemp_DryBulb_ChB_degC <= rTemp_DryBulb_ChA_degC) AND (rTemp_DryBulb_ChB_degC >= rTemp_DryBulb_ChC_degC)) THEN
        rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChB_degC;
    ELSE
        rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChC_degC;
    END_IF;
ELSIF bTemp_ChA_Valid AND bTemp_ChB_Valid THEN
    rVoted_Temp_DryBulb_degC := (rTemp_DryBulb_ChA_degC + rTemp_DryBulb_ChB_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bTemp_ChB_Valid AND bTemp_ChC_Valid THEN
    rVoted_Temp_DryBulb_degC := (rTemp_DryBulb_ChB_degC + rTemp_DryBulb_ChC_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bTemp_ChA_Valid AND bTemp_ChC_Valid THEN
    rVoted_Temp_DryBulb_degC := (rTemp_DryBulb_ChA_degC + rTemp_DryBulb_ChC_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bTemp_ChA_Valid THEN
    rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChA_degC;
    bDegradedSensorFallback := TRUE;
ELSIF bTemp_ChB_Valid THEN
    rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChB_degC;
    bDegradedSensorFallback := TRUE;
ELSIF bTemp_ChC_Valid THEN
    rVoted_Temp_DryBulb_degC := rTemp_DryBulb_ChC_degC;
    bDegradedSensorFallback := TRUE;
ELSE
    rVoted_Temp_DryBulb_degC := 22.00;
    dwAlarmWord_Critical.4 := TRUE;    (* All 3 Temperature Sensors Failed! *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 2.4 PRECISION DEW-POINT CHILLED MIRROR HYGROMETER VOTER                                       *)
(* --------------------------------------------------------------------------------------------- *)
IF ABS(rTemp_DewPoint_ChA_degC - rTemp_DewPoint_ChB_degC) > rTol_DewPoint_degC THEN
    iDewPt_DevCount_AB := iDewPt_DevCount_AB + 1;
ELSE
    IF iDewPt_DevCount_AB > 0 THEN iDewPt_DevCount_AB := iDewPt_DevCount_AB - 1; END_IF;
END_IF;

IF ABS(rTemp_DewPoint_ChB_degC - rTemp_DewPoint_ChC_degC) > rTol_DewPoint_degC THEN
    iDewPt_DevCount_BC := iDewPt_DevCount_BC + 1;
ELSE
    IF iDewPt_DevCount_BC > 0 THEN iDewPt_DevCount_BC := iDewPt_DevCount_BC - 1; END_IF;
END_IF;

IF ABS(rTemp_DewPoint_ChC_degC - rTemp_DewPoint_ChA_degC) > rTol_DewPoint_degC THEN
    iDewPt_DevCount_CA := iDewPt_DevCount_CA + 1;
ELSE
    IF iDewPt_DevCount_CA > 0 THEN iDewPt_DevCount_CA := iDewPt_DevCount_CA - 1; END_IF;
END_IF;

IF (iDewPt_DevCount_AB > iMaxDiscrepancyCycles) AND (iDewPt_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bDewPt_ChA_LatchedFault := TRUE;
END_IF;
IF (iDewPt_DevCount_AB > iMaxDiscrepancyCycles) AND (iDewPt_DevCount_BC > iMaxDiscrepancyCycles) THEN
    bDewPt_ChB_LatchedFault := TRUE;
END_IF;
IF (iDewPt_DevCount_BC > iMaxDiscrepancyCycles) AND (iDewPt_DevCount_CA > iMaxDiscrepancyCycles) THEN
    bDewPt_ChC_LatchedFault := TRUE;
END_IF;

bDewPt_ChA_Valid := NOT bDewPt_ChA_LatchedFault AND (rTemp_DewPoint_ChA_degC >= -5.0) AND (rTemp_DewPoint_ChA_degC <= 25.0);
bDewPt_ChB_Valid := NOT bDewPt_ChB_LatchedFault AND (rTemp_DewPoint_ChB_degC >= -5.0) AND (rTemp_DewPoint_ChB_degC <= 25.0);
bDewPt_ChC_Valid := NOT bDewPt_ChC_LatchedFault AND (rTemp_DewPoint_ChC_degC >= -5.0) AND (rTemp_DewPoint_ChC_degC <= 25.0);

IF bDewPt_ChA_Valid AND bDewPt_ChB_Valid AND bDewPt_ChC_Valid THEN
    IF ((rTemp_DewPoint_ChA_degC >= rTemp_DewPoint_ChB_degC) AND (rTemp_DewPoint_ChA_degC <= rTemp_DewPoint_ChC_degC)) OR
       ((rTemp_DewPoint_ChA_degC <= rTemp_DewPoint_ChB_degC) AND (rTemp_DewPoint_ChA_degC >= rTemp_DewPoint_ChC_degC)) THEN
        rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChA_degC;
    ELSIF ((rTemp_DewPoint_ChB_degC >= rTemp_DewPoint_ChA_degC) AND (rTemp_DewPoint_ChB_degC <= rTemp_DewPoint_ChC_degC)) OR
          ((rTemp_DewPoint_ChB_degC <= rTemp_DewPoint_ChA_degC) AND (rTemp_DewPoint_ChB_degC >= rTemp_DewPoint_ChC_degC)) THEN
        rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChB_degC;
    ELSE
        rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChC_degC;
    END_IF;
ELSIF bDewPt_ChA_Valid AND bDewPt_ChB_Valid THEN
    rVoted_Temp_DewPoint_degC := (rTemp_DewPoint_ChA_degC + rTemp_DewPoint_ChB_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bDewPt_ChB_Valid AND bDewPt_ChC_Valid THEN
    rVoted_Temp_DewPoint_degC := (rTemp_DewPoint_ChB_degC + rTemp_DewPoint_ChC_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bDewPt_ChA_Valid AND bDewPt_ChC_Valid THEN
    rVoted_Temp_DewPoint_degC := (rTemp_DewPoint_ChA_degC + rTemp_DewPoint_ChC_degC) * 0.5;
    bDegradedSensorFallback := TRUE;
ELSIF bDewPt_ChA_Valid THEN
    rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChA_degC;
    bDegradedSensorFallback := TRUE;
ELSIF bDewPt_ChB_Valid THEN
    rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChB_degC;
    bDegradedSensorFallback := TRUE;
ELSIF bDewPt_ChC_Valid THEN
    rVoted_Temp_DewPoint_degC := rTemp_DewPoint_ChC_degC;
    bDegradedSensorFallback := TRUE;
ELSE
    rVoted_Temp_DewPoint_degC := 9.50;
    dwAlarmWord_Critical.5 := TRUE;    (* All 3 Dew Point Sensors Failed! *)
END_IF;

(* PACK SENSOR VOTING BITFIELD STATUS *)
dwSensorVotingStatusWord.0 := bPress_ChA_Valid;
dwSensorVotingStatusWord.1 := bPress_ChB_Valid;
dwSensorVotingStatusWord.2 := bPress_ChC_Valid;
dwSensorVotingStatusWord.3 := bVel_ChA_Valid;
dwSensorVotingStatusWord.4 := bVel_ChB_Valid;
dwSensorVotingStatusWord.5 := bVel_ChC_Valid;
dwSensorVotingStatusWord.6 := bTemp_ChA_Valid;
dwSensorVotingStatusWord.7 := bTemp_ChB_Valid;
dwSensorVotingStatusWord.8 := bTemp_ChC_Valid;
dwSensorVotingStatusWord.9 := bDewPt_ChA_Valid;
dwSensorVotingStatusWord.10 := bDewPt_ChB_Valid;
dwSensorVotingStatusWord.11 := bDewPt_ChC_Valid;
dwSensorVotingStatusWord.12 := bDegradedSensorFallback;

(*
========================================================================================================================
 SECTION 3: PSYCHROMETRIC AND PROCESS EQUATIONS ESTIMATION
========================================================================================================================
*)
(* Dynamic air viscosity via Sutherland's Law *)
rAirDynamicViscosity_Pals := rSutherland_Mu0 * EXPT((rVoted_Temp_DryBulb_degC + 273.15) / rSutherland_T0, 1.5) * 
                             (rSutherland_T0 + rSutherland_S) / (rVoted_Temp_DryBulb_degC + 273.15 + rSutherland_S);

(* Magnus-Tetens Saturated Vapor Pressure Equation *)
rSaturatedVaporPress_Pa := 610.78 * EXP((17.27 * rVoted_Temp_DryBulb_degC) / (rVoted_Temp_DryBulb_degC + 237.3));

(* Actual Water Vapor Pressure from Relative Humidity *)
IF rHumidity_Rel_pct > 0.1 THEN
    rActualVaporPress_Pa := (rHumidity_Rel_pct * 0.01) * rSaturatedVaporPress_Pa;
ELSE
    rActualVaporPress_Pa := 1189.0;
END_IF;

(* Magnus-Tetens Inversion for Calculated Dew Point *)
IF rActualVaporPress_Pa > 1.0 THEN
    rMagnus_Gamma := LN(rActualVaporPress_Pa / 610.78);
    rCalculatedDewPoint_degC := (237.3 * rMagnus_Gamma) / (17.27 - rMagnus_Gamma);
ELSE
    rCalculatedDewPoint_degC := 9.50;
END_IF;

(* Psychrometric Humidity Ratio W [kg_water / kg_dry_air] *)
IF rBaroPressure_hPa > 500.0 THEN
    rHumidityRatio_kgpkg := 0.62198 * rActualVaporPress_Pa / ((rBaroPressure_hPa * 100.0) - rActualVaporPress_Pa);
ELSE
    rHumidityRatio_kgpkg := 0.00735;
END_IF;

(* Moist Air Specific Enthalpy h [kJ/kg] *)
rCalculatedMoistAirEnthalpy := 1.006 * rVoted_Temp_DryBulb_degC + rHumidityRatio_kgpkg * (2501.0 + 1.86 * rVoted_Temp_DryBulb_degC);

(* Effective Bay Air Changes per Hour (ACH) *)
(* Area = 500 m2, Height = 3.6 m -> Bay Volume = 1800 m3 *)
rEst_AirChangesPerHour_ACH := (rVoted_Velocity_Face_mps * 500.0 * 3600.0) / 1800.0;

(* ULPA Filter Specific Resistance and Loading Estimation *)
rULPA_NetDeltaP_Pa := rPressDiff_ULPA_Filter_Pa - rULPA_TareOffset_Pa;
IF rVoted_Velocity_Face_mps > 0.05 THEN
    rEst_ULPA_Resistance_Rayl := rULPA_NetDeltaP_Pa / rVoted_Velocity_Face_mps;
    rULPA_LoadingFactor := rULPA_NetDeltaP_Pa / (rULPA_CleanRefDeltaP_Pa * (rVoted_Velocity_Face_mps / 0.450));
ELSE
    rEst_ULPA_Resistance_Rayl := 211.0;
    rULPA_LoadingFactor := 1.0;
END_IF;

(* Airborne Molecular Contamination (AMC) Media Life Integration *)
(* Aggregate AMC = VOC + NH3 + SO2 [ppb] *)
rAMC_CaptureRate_gps := (rConc_VOC_ppb + rConc_NH3_ppb + rConc_SO2_ppb) * 1.0e-9 * (rFlow_MAU_Supply_m3ph * 1.185 / 3600.0);
rAMC_CumulativeCaptured_g := rAMC_CumulativeCaptured_g + (rAMC_CaptureRate_gps * rScanDeltaTime_s * 1000.0);
IF rAMC_InitialCapacity_g > 100.0 THEN
    rAMC_RemainingLife_pct := (1.0 - (rAMC_CumulativeCaptured_g / rAMC_InitialCapacity_g)) * 100.0;
    IF rAMC_RemainingLife_pct < 0.0 THEN rAMC_RemainingLife_pct := 0.0; END_IF;
END_IF;

(* Acoustic Vibration Biquad Bandpass Filter Execution *)
rVib_BQ_w1 := rVib_FFU_Plenum_mms_RMS - (rVib_BQ_a1 * rVib_BQ_w1) - (rVib_BQ_a2 * rVib_BQ_w2);
rVib_FiltSample := (rVib_BQ_b0 * rVib_BQ_w1) + (rVib_BQ_b1 * rVib_BQ_w1) + (rVib_BQ_b2 * rVib_BQ_w2);
rVib_BQ_w2 := rVib_BQ_w1;
rVib_VarianceAcc := (0.95 * rVib_VarianceAcc) + (0.05 * (rVib_FiltSample * rVib_FiltSample));
rVib_FilteredRMS := SQRT(rVib_VarianceAcc);

(*
========================================================================================================================
 SECTION 4: DISCRETE STATE-SPACE MODEL PROPAGATION & KALMAN PREDICTION
 System Equations:
   x[k+1] = A * x[k] + B * u[k] + E * d[k]
   y[k]   = C * x[k] + D * u[k]
========================================================================================================================
*)
(* Populate State Vector x from Sensors & Thermodynamic Estimates *)
aStateX[1]  := rVoted_PressDiff_Litho_Pa;
aStateX[2]  := rPressDiff_Etch_Pa;
aStateX[3]  := rPressDiff_Gown_Pa;
aStateX[4]  := rPressDiff_Plenum_Pa;
aStateX[5]  := rVoted_Velocity_Face_mps;
aStateX[6]  := rVoted_Temp_DryBulb_degC;
aStateX[7]  := rVoted_Temp_DewPoint_degC;
aStateX[8]  := rConc_VOC_ppb;
aStateX[9]  := rConc_NH3_ppb;
aStateX[10] := rConc_SO2_ppb;
aStateX[11] := rTemp_ChilledWaterSupply_degC;
aStateX[12] := rVoted_Temp_DryBulb_degC + 2.0; (* Reheat discharge air estimate *)
aStateX[13] := rHumidityRatio_kgpkg * 1000.0;  (* g/kg *)
aStateX[14] := rCmd_FFU_Speed_rpm;
aStateX[15] := rFlow_MAU_Supply_m3ph;
aStateX[16] := rVib_FilteredRMS;

(* Populate Disturbance Vector d *)
IF bAirlockDoorUnsealed OR bAirlockDoorOpenReq THEN
    aDisturbD[1] := 1.0;
ELSE
    aDisturbD[1] := 0.0;
END_IF;
aDisturbD[2] := rTemp_Ambient_degC;
aDisturbD[3] := rHumidity_Ambient_pct;
aDisturbD[4] := rPower_ScannerHeatLoad_kW;
aDisturbD[5] := rFlow_ScrubbedExhaust_m3ph;
aDisturbD[6] := (rBaroPressure_hPa - 1013.25) * 100.0;

(* Matrix Multiplication: x_next = A * x + B * u + E * d *)
FOR iIdx := 1 TO 16 DO
    rSumAccum := 0.0;
    FOR jIdx := 1 TO 16 DO
        rSumAccum := rSumAccum + (aA[iIdx, jIdx] * aStateX[jIdx]);
    END_FOR;
    FOR jIdx := 1 TO 8 DO
        rSumAccum := rSumAccum + (aB[iIdx, jIdx] * (aControlU[jIdx] - aControlU_Prev[jIdx]));
    END_FOR;
    FOR jIdx := 1 TO 6 DO
        rSumAccum := rSumAccum + (aE[iIdx, jIdx] * aDisturbD[jIdx]);
    END_FOR;
    aStateX_Next[iIdx] := rSumAccum;
END_FOR;

(* Matrix Multiplication: y = C * x + D * u *)
FOR iIdx := 1 TO 8 DO
    rSumAccum := 0.0;
    FOR jIdx := 1 TO 16 DO
        rSumAccum := rSumAccum + (aC[iIdx, jIdx] * aStateX[jIdx]);
    END_FOR;
    FOR jIdx := 1 TO 8 DO
        rSumAccum := rSumAccum + (aD[iIdx, jIdx] * aControlU[jIdx]);
    END_FOR;
    aOutputY[iIdx] := rSumAccum;
END_FOR;

(*
========================================================================================================================
 SECTION 5: RECEDING-HORIZON MODEL PREDICTIVE CONTROL (MPC) OPTIMIZATION
 Condensed Quadratic Programming Solver:
   - Evaluates gradient: Grad_J = H * Delta_u + g_k
   - Executes projected line search with box constraints [u_min, u_max] and slew limits.
   - Injects pre-emptive feedforward compensation for wafer pass-through airlock transients.
========================================================================================================================
*)
(* Compute State Error Vector e = x - r *)
FOR iIdx := 1 TO 16 DO
    aStateError[iIdx] := aStateX[iIdx] - aSetpointR[iIdx];
END_FOR;

(* Compute Linear Term g_k = B^T * Q * e *)
FOR iIdx := 1 TO 8 DO
    rSumAccum := 0.0;
    FOR jIdx := 1 TO 16 DO
        rSumAccum := rSumAccum + (aB[jIdx, iIdx] * aQ[jIdx, jIdx] * aStateError[jIdx]);
    END_FOR;
    aGradG[iIdx] := rSumAccum;
END_FOR;

(* Unrolled Projected Gradient Descent Iteration Loop (5 Iterations @ 20 Hz) *)
FOR iQPIter := 1 TO 5 DO
    FOR iIdx := 1 TO 8 DO
        (* Compute H * Delta_u *)
        rSumAccum := 0.0;
        FOR jIdx := 1 TO 8 DO
            rSumAccum := rSumAccum + (aH[iIdx, jIdx] * aDeltaU[jIdx]);
        END_FOR;
        
        (* Gradient Step *)
        rCandidateU := aDeltaU[iIdx] - (rGradStep * (rSumAccum + aGradG[iIdx]));
        
        (* Projection onto Actuator Slew Rate Bounds *)
        CASE iIdx OF
            1: (* FFU collective speed *)
               rRateLimitDelta := rFFU_Speed_RateMax_rpmps * rScanDeltaTime_s;
            2: (* MAU supply damper *)
               rRateLimitDelta := rMAU_Damper_RateMax_pctps * rScanDeltaTime_s;
            3: (* Exhaust damper *)
               rRateLimitDelta := rExh_Damper_RateMax_pctps * rScanDeltaTime_s;
            4: (* Chilled water valve *)
               rRateLimitDelta := rCW_Valve_RateMax_pctps * rScanDeltaTime_s;
            5: (* DX trim coil *)
               rRateLimitDelta := rDX_Trim_RateMax_pctps * rScanDeltaTime_s;
            6: (* Steam humidifier *)
               rRateLimitDelta := rSteam_Hum_RateMax_pctps * rScanDeltaTime_s;
            7: (* Electric reheat *)
               rRateLimitDelta := rReheat_RateMax_pctps * rScanDeltaTime_s;
            8: (* Airlock booster damper *)
               rRateLimitDelta := rAirlock_Booster_RateMax_pctps * rScanDeltaTime_s;
        END_CASE;
        
        IF rCandidateU > rRateLimitDelta THEN
            rCandidateU := rRateLimitDelta;
        ELSIF rCandidateU < -rRateLimitDelta THEN
            rCandidateU := -rRateLimitDelta;
        END_IF;
        
        aDeltaU[iIdx] := rCandidateU;
    END_FOR;
END_FOR;

(* Apply Incremental Controls to Actuator Commands *)
aControlU[1] := aControlU_Prev[1] + aDeltaU[1];
aControlU[2] := aControlU_Prev[2] + aDeltaU[2];
aControlU[3] := aControlU_Prev[3] + aDeltaU[3];
aControlU[4] := aControlU_Prev[4] + aDeltaU[4];
aControlU[5] := aControlU_Prev[5] + aDeltaU[5];
aControlU[6] := aControlU_Prev[6] + aDeltaU[6];
aControlU[7] := aControlU_Prev[7] + aDeltaU[7];
aControlU[8] := aControlU_Prev[8] + aDeltaU[8];

(* PRE-EMPTIVE FEEDFORWARD AIRLOCK PRESSURE COMPENSATION *)
IF bAirlockDoorOpenReq OR bAirlockDoorUnsealed OR bPassThroughDoorOpen THEN
    (* Inject instantaneous +85 rpm fan speed boost and open booster damper *)
    aControlU[1] := aControlU[1] + 85.0;
    aControlU[8] := 80.0;
    aControlU[2] := aControlU[2] + 15.0; (* Open make-up air damper *)
ELSE
    aControlU[8] := 0.0;
END_IF;

(* Actuator Travel Clamping *)
IF aControlU[1] > rFFU_Speed_Max_rpm THEN aControlU[1] := rFFU_Speed_Max_rpm; END_IF;
IF aControlU[1] < rFFU_Speed_Min_rpm THEN aControlU[1] := rFFU_Speed_Min_rpm; END_IF;

IF aControlU[2] > rMAU_Damper_Max_pct THEN aControlU[2] := rMAU_Damper_Max_pct; END_IF;
IF aControlU[2] < rMAU_Damper_Min_pct THEN aControlU[2] := rMAU_Damper_Min_pct; END_IF;

IF aControlU[3] > rExh_Damper_Max_pct THEN aControlU[3] := rExh_Damper_Max_pct; END_IF;
IF aControlU[3] < rExh_Damper_Min_pct THEN aControlU[3] := rExh_Damper_Min_pct; END_IF;

IF aControlU[4] > rCW_Valve_Max_pct THEN aControlU[4] := rCW_Valve_Max_pct; END_IF;
IF aControlU[4] < rCW_Valve_Min_pct THEN aControlU[4] := rCW_Valve_Min_pct; END_IF;

IF aControlU[5] > rDX_Trim_Max_pct THEN aControlU[5] := rDX_Trim_Max_pct; END_IF;
IF aControlU[5] < rDX_Trim_Min_pct THEN aControlU[5] := rDX_Trim_Min_pct; END_IF;

IF aControlU[6] > rSteam_Hum_Max_pct THEN aControlU[6] := rSteam_Hum_Max_pct; END_IF;
IF aControlU[6] < rSteam_Hum_Min_pct THEN aControlU[6] := rSteam_Hum_Min_pct; END_IF;

IF aControlU[7] > rReheat_Max_pct THEN aControlU[7] := rReheat_Max_pct; END_IF;
IF aControlU[7] < rReheat_Min_pct THEN aControlU[7] := rReheat_Min_pct; END_IF;

IF aControlU[8] > rAirlock_Booster_Max_pct THEN aControlU[8] := rAirlock_Booster_Max_pct; END_IF;
IF aControlU[8] < rAirlock_Booster_Min_pct THEN aControlU[8] := rAirlock_Booster_Min_pct; END_IF;

(*
========================================================================================================================
 SECTION 6: 12-STAGE OPERATIONAL FINITE STATE MACHINE (FSM)
========================================================================================================================
*)
CASE iFSM_State OF

    STATE_COLD_START_PURGE:
        (* Stage 0: Initial gross volume air turnover (50 ACH for 300 seconds) *)
        rCmd_FFU_Speed_rpm          := 900.0;
        rCmd_MAU_SupplyDamper_pct   := 75.0;
        rCmd_ExhaustDamper_pct      := 60.0;
        rCmd_ChilledWaterValve_pct  := 20.0;
        rCmd_DX_TrimCoil_pct        := 0.0;
        rCmd_SteamHumidifier_pct    := 0.0;
        rCmd_ElectricReheat_pct     := 0.0;
        rCmd_AirlockBooster_pct     := 0.0;
        
        bCleanroomReadyForWafer     := FALSE;
        bPressureEnvelopeLocked     := FALSE;
        bLaminarVelocityUniform     := FALSE;
        bDewPointStable             := FALSE;
        
        tonColdStartPurge(IN := TRUE, PT := T#300S);
        IF tonColdStartPurge.Q AND bMasterEnable THEN
            tonColdStartPurge(IN := FALSE);
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_FILTER_TARE_CALIB;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_FILTER_TARE_CALIB:
        (* Stage 1: Zero-flow ULPA filter pressure drop baseline tare *)
        rCmd_FFU_Speed_rpm          := 0.0; (* Fans stopped for tare *)
        rCmd_MAU_SupplyDamper_pct   := 15.0;
        rCmd_ExhaustDamper_pct      := 10.0;
        
        tonFilterTareSettle(IN := TRUE, PT := T#15S);
        IF tonFilterTareSettle.Q THEN
            rULPA_TareOffset_Pa := rPressDiff_ULPA_Filter_Pa;
            tonFilterTareSettle(IN := FALSE);
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_FFU_SOFT_START;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_FFU_SOFT_START:
        (* Stage 2: FFU EC motor controlled ramp to avoid duct resonance & acoustic surge *)
        tonFFURampTimer(IN := TRUE, PT := T#60S);
        rCmd_FFU_Speed_rpm := 300.0 + (950.0 * (rFSM_StateDwellTime_s / 60.0));
        IF rCmd_FFU_Speed_rpm > 1250.0 THEN rCmd_FFU_Speed_rpm := 1250.0; END_IF;
        
        rCmd_MAU_SupplyDamper_pct   := 40.0;
        rCmd_ExhaustDamper_pct      := 25.0;
        
        IF tonFFURampTimer.Q THEN
            tonFFURampTimer(IN := FALSE);
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_MAU_THERMAL_COND;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_MAU_THERMAL_COND:
        (* Stage 3: Make-up air thermal conditioning (Cooling coil & steam lock dew point) *)
        rCmd_FFU_Speed_rpm          := 1250.0;
        rCmd_ChilledWaterValve_pct  := aControlU[4];
        rCmd_DX_TrimCoil_pct        := aControlU[5];
        rCmd_SteamHumidifier_pct    := aControlU[6];
        rCmd_ElectricReheat_pct     := aControlU[7];
        
        tonThermalSettleTimer(IN := TRUE, PT := T#120S);
        IF tonThermalSettleTimer.Q AND (ABS(rVoted_Temp_DryBulb_degC - 22.00) < 0.15) AND 
           (ABS(rVoted_Temp_DewPoint_degC - 9.50) < 0.25) THEN
            tonThermalSettleTimer(IN := FALSE);
            bDewPointStable := TRUE;
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_OVERPRESSURE_LOCK;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_OVERPRESSURE_LOCK:
        (* Stage 4: Cleanroom overpressure cascade envelope lock *)
        (* Enforce: Litho (+25) > Etch (+15) > Gown (+10) > Corridor (+5) *)
        rCmd_MAU_SupplyDamper_pct   := aControlU[2];
        rCmd_ExhaustDamper_pct      := aControlU[3];
        rCmd_FFU_Speed_rpm          := aControlU[1];
        
        tonPressureLockTimer(IN := TRUE, PT := T#45S);
        IF tonPressureLockTimer.Q AND (rVoted_PressDiff_Litho_Pa >= 23.5) AND 
           (rVoted_PressDiff_Litho_Pa - rPressDiff_Etch_Pa >= 7.0) THEN
            tonPressureLockTimer(IN := FALSE);
            bPressureEnvelopeLocked := TRUE;
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_LAMINAR_VEL_STABIL;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_LAMINAR_VEL_STABIL:
        (* Stage 5: Laminar airflow face velocity field stabilization *)
        rCmd_FFU_Speed_rpm := aControlU[1];
        
        tonVelocityFieldTimer(IN := TRUE, PT := T#60S);
        IF tonVelocityFieldTimer.Q AND (ABS(rVoted_Velocity_Face_mps - 0.450) <= 0.030) AND 
           (rVib_FilteredRMS < 0.045) THEN
            tonVelocityFieldTimer(IN := FALSE);
            bLaminarVelocityUniform := TRUE;
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_AMC_SCRUBBER_PACE;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_AMC_SCRUBBER_PACE:
        (* Stage 6: AMC chemical filtration baseline lock *)
        IF (rConc_VOC_ppb < rAMC_VOC_Limit_ppb) AND (rConc_NH3_ppb < rAMC_NH3_Limit_ppb) AND 
           (rConc_SO2_ppb < rAMC_SO2_Limit_ppb) THEN
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_PRODUCTION_READY;
            rFSM_StateDwellTime_s := 0.0;
        ELSIF rFSM_StateDwellTime_s > 180.0 THEN
            (* Bypass after 3 min warning if AMC sensors slightly elevated *)
            dwAlarmWord_Advisory.6 := TRUE; (* AMC baseline elevated *)
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_PRODUCTION_READY;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_PRODUCTION_READY:
        (* Stage 7: Full closed-loop multivariable MPC steady state *)
        bCleanroomReadyForWafer     := bPressureEnvelopeLocked AND bLaminarVelocityUniform AND bDewPointStable;
        
        rCmd_FFU_Speed_rpm          := aControlU[1];
        rCmd_MAU_SupplyDamper_pct   := aControlU[2];
        rCmd_ExhaustDamper_pct      := aControlU[3];
        rCmd_ChilledWaterValve_pct  := aControlU[4];
        rCmd_DX_TrimCoil_pct        := aControlU[5];
        rCmd_SteamHumidifier_pct    := aControlU[6];
        rCmd_ElectricReheat_pct     := aControlU[7];
        rCmd_AirlockBooster_pct     := aControlU[8];
        
        IF bAirlockDoorOpenReq OR bAirlockDoorUnsealed OR bPassThroughDoorOpen THEN
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_AIRLOCK_COMPENSATION;
            rFSM_StateDwellTime_s := 0.0;
        ELSIF bNightSetbackCommand THEN
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_NIGHT_SETBACK_STANDBY;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_AIRLOCK_COMPENSATION:
        (* Stage 8: Active transient pressure boost during wafer transfer pass-through *)
        rCmd_FFU_Speed_rpm          := aControlU[1] + 85.0;
        rCmd_MAU_SupplyDamper_pct   := aControlU[2] + 18.0;
        rCmd_AirlockBooster_pct     := 85.0;
        rCmd_ExhaustDamper_pct      := aControlU[3] * 0.5; (* Throttled exhaust to hold pressure *)
        
        tonAirlockHoldTimer(IN := NOT (bAirlockDoorOpenReq OR bAirlockDoorUnsealed OR bPassThroughDoorOpen), PT := T#8S);
        IF tonAirlockHoldTimer.Q THEN
            tonAirlockHoldTimer(IN := FALSE);
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_PRODUCTION_READY;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_FILTER_REPLACE_FLUSH:
        (* Stage 9: Filter change-out high-flow particle decontamination flush *)
        rCmd_FFU_Speed_rpm          := 1600.0; (* 0.58 m/s flush velocity *)
        rCmd_MAU_SupplyDamper_pct   := 90.0;
        rCmd_ExhaustDamper_pct      := 85.0;
        bCleanroomReadyForWafer     := FALSE;
        
        IF rFSM_StateDwellTime_s > 600.0 THEN
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_LAMINAR_VEL_STABIL;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_NIGHT_SETBACK_STANDBY:
        (* Stage 10: Night setback energy saving mode (v_face = 0.25 m/s, pressure preserved) *)
        rCmd_FFU_Speed_rpm          := 750.0;
        rCmd_MAU_SupplyDamper_pct   := 30.0;
        rCmd_ExhaustDamper_pct      := 15.0;
        rCmd_ChilledWaterValve_pct  := aControlU[4] * 0.6;
        bCleanroomReadyForWafer     := FALSE;
        
        IF NOT bNightSetbackCommand THEN
            iFSM_PrevState := iFSM_State;
            iFSM_State := STATE_LAMINAR_VEL_STABIL;
            rFSM_StateDwellTime_s := 0.0;
        END_IF;

    STATE_TOXIC_GAS_PURGE_TRIP:
        (* Stage 11: Emergency life safety toxic gas / smoke exhaust (100% full fresh air) *)
        rCmd_FFU_Speed_rpm          := 0.0;   (* Shut down recirculation ceiling fans *)
        rCmd_MAU_SupplyDamper_pct   := 100.0; (* 100% outside purge air *)
        rCmd_ExhaustDamper_pct      := 100.0; (* Full open toxic exhaust dampers *)
        rCmd_ChilledWaterValve_pct  := 0.0;
        rCmd_DX_TrimCoil_pct        := 0.0;
        rCmd_SteamHumidifier_pct    := 0.0;
        rCmd_ElectricReheat_pct     := 0.0;
        rCmd_AirlockBooster_pct     := 0.0;
        
        bCleanroomReadyForWafer     := FALSE;
        bPressureEnvelopeLocked     := FALSE;
        bLaminarVelocityUniform     := FALSE;
        bDewPointStable             := FALSE;
        bToxicPurgeActive           := TRUE;

    ELSE
        iFSM_State := STATE_COLD_START_PURGE;
END_CASE;

(*
========================================================================================================================
 SECTION 7: ISA-18.2 MULTI-TIERED ALARM MATRIX & TELEMETRY BITFIELD ENCODING
========================================================================================================================
*)
(* --------------------------------------------------------------------------------------------- *)
(* 7.1 CRITICAL ALARMS (ISA-18.2 CATEGORY 1: IMMEDIATE PROCESS INTERLOCK / TRIP)                *)
(* --------------------------------------------------------------------------------------------- *)
(* Cascade Envelope Inversion Check *)
rEst_CascadeMargin_Pa := rVoted_PressDiff_Litho_Pa - rPressDiff_Etch_Pa;
tonPressCascadeReversal(IN := (rEst_CascadeMargin_Pa < rPress_CascadeMargin_LL_Trip), PT := T#2S);
IF tonPressCascadeReversal.Q THEN
    dwAlarmWord_Critical.6 := TRUE; (* Differential Pressure Cascade Reversal Trip *)
    bPressureEnvelopeLocked := FALSE;
END_IF;

(* Cleanroom Low Pressure LL Trip *)
IF rVoted_PressDiff_Litho_Pa < (rPress_Litho_LL_Trip - rPress_Hysteresis_Pa) THEN
    dwAlarmWord_Critical.7 := TRUE; (* Litho Bay Underpressure Envelope Loss *)
END_IF;

(* Laminar Face Velocity LL Trip *)
tonLaminarVelocityStall(IN := (rVoted_Velocity_Face_mps < rVel_Face_LL_Trip), PT := T#3S);
IF tonLaminarVelocityStall.Q THEN
    dwAlarmWord_Critical.8 := TRUE; (* Laminar Piston Airflow Boundary Stall *)
    bLaminarVelocityUniform := FALSE;
END_IF;

(* Dry-Bulb Thermal Excursion Trip *)
tonThermalExcursionTrip(IN := (ABS(rVoted_Temp_DryBulb_degC - rTemp_DryBulb_SP) > 0.35), PT := T#5S);
IF tonThermalExcursionTrip.Q THEN
    dwAlarmWord_Critical.9 := TRUE; (* Thermal Excursion Exceeds Litho Tolerance *)
    bDewPointStable := FALSE;
END_IF;

(* Dew-Point Excursion Trip *)
tonDewPointExcursionTrip(IN := (ABS(rVoted_Temp_DewPoint_degC - rTemp_DewPoint_SP) > 0.90), PT := T#5S);
IF tonDewPointExcursionTrip.Q THEN
    dwAlarmWord_Critical.10 := TRUE; (* Dew-Point Condensation / ESD Risk Trip *)
    bDewPointStable := FALSE;
END_IF;

(* FFU Plenum Floor Vibration HH Trip *)
tonAcousticVibExcess(IN := (rVib_FilteredRMS > rVib_Plenum_HH_Trip), PT := T#4S);
IF tonAcousticVibExcess.Q THEN
    dwAlarmWord_Critical.11 := TRUE; (* FFU Acoustic Vibration Exceeds VC-E Spec *)
END_IF;

(* ULPA Filter Media Max Differential Pressure Blowout Trip *)
IF rULPA_NetDeltaP_Pa > rULPA_MaxDeltaP_Trip_Pa THEN
    dwAlarmWord_Critical.12 := TRUE; (* ULPA Filter Media Structural Blowout Hazard *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 7.2 HIGH ALARMS (ISA-18.2 CATEGORY 2: OPERATOR ACTION REQUIRED)                              *)
(* --------------------------------------------------------------------------------------------- *)
IF (rVoted_PressDiff_Litho_Pa > rPress_Litho_H_Warn) THEN
    dwAlarmWord_High.0 := TRUE; (* Litho Pressure High Warning *)
ELSIF (rVoted_PressDiff_Litho_Pa < (rPress_Litho_H_Warn - rPress_Hysteresis_Pa)) THEN
    dwAlarmWord_High.0 := FALSE;
END_IF;

IF (rVoted_PressDiff_Litho_Pa < rPress_Litho_L_Warn) THEN
    dwAlarmWord_High.1 := TRUE; (* Litho Pressure Low Warning *)
ELSIF (rVoted_PressDiff_Litho_Pa > (rPress_Litho_L_Warn + rPress_Hysteresis_Pa)) THEN
    dwAlarmWord_High.1 := FALSE;
END_IF;

IF (rVoted_Velocity_Face_mps > rVel_Face_H_Warn) THEN
    dwAlarmWord_High.2 := TRUE; (* Laminar Velocity High Warning *)
ELSIF (rVoted_Velocity_Face_mps < (rVel_Face_H_Warn - rVel_Hysteresis_mps)) THEN
    dwAlarmWord_High.2 := FALSE;
END_IF;

IF (rVoted_Velocity_Face_mps < rVel_Face_L_Warn) THEN
    dwAlarmWord_High.3 := TRUE; (* Laminar Velocity Low Warning *)
ELSIF (rVoted_Velocity_Face_mps > (rVel_Face_L_Warn + rVel_Hysteresis_mps)) THEN
    dwAlarmWord_High.3 := FALSE;
END_IF;

IF (rVoted_Temp_DryBulb_degC > rTemp_DryBulb_H_Warn) THEN
    dwAlarmWord_High.4 := TRUE; (* Dry-Bulb Temperature High Warning *)
ELSIF (rVoted_Temp_DryBulb_degC < (rTemp_DryBulb_H_Warn - rTemp_Hysteresis_degC)) THEN
    dwAlarmWord_High.4 := FALSE;
END_IF;

IF (rVoted_Temp_DryBulb_degC < rTemp_DryBulb_L_Warn) THEN
    dwAlarmWord_High.5 := TRUE; (* Dry-Bulb Temperature Low Warning *)
ELSIF (rVoted_Temp_DryBulb_degC > (rTemp_DryBulb_L_Warn + rTemp_Hysteresis_degC)) THEN
    dwAlarmWord_High.5 := FALSE;
END_IF;

IF (rVoted_Temp_DewPoint_degC > rTemp_DewPoint_H_Warn) THEN
    dwAlarmWord_High.6 := TRUE; (* Dew-Point High Warning *)
ELSIF (rVoted_Temp_DewPoint_degC < (rTemp_DewPoint_H_Warn - rDewPoint_Hysteresis_degC)) THEN
    dwAlarmWord_High.6 := FALSE;
END_IF;

IF (rVoted_Temp_DewPoint_degC < rTemp_DewPoint_L_Warn) THEN
    dwAlarmWord_High.7 := TRUE; (* Dew-Point Low Warning *)
ELSIF (rVoted_Temp_DewPoint_degC > (rTemp_DewPoint_L_Warn + rDewPoint_Hysteresis_degC)) THEN
    dwAlarmWord_High.7 := FALSE;
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 7.3 ADVISORY ALARMS (ISA-18.2 CATEGORY 3: SYSTEM ADVISORY)                                   *)
(* --------------------------------------------------------------------------------------------- *)
IF rULPA_NetDeltaP_Pa > rULPA_HighDeltaP_Warn_Pa THEN
    dwAlarmWord_Advisory.0 := TRUE; (* ULPA Filter High Loading Advisory *)
END_IF;

IF rAMC_RemainingLife_pct < 15.0 THEN
    dwAlarmWord_Advisory.1 := TRUE; (* Chemical Scrubber Filter Life < 15% Remaining *)
END_IF;

IF rVib_FilteredRMS > rVib_Plenum_H_Warn THEN
    dwAlarmWord_Advisory.2 := TRUE; (* Floor Vibration VC-E Advisory *)
END_IF;

IF bDegradedSensorFallback THEN
    dwAlarmWord_Advisory.3 := TRUE; (* Operating in Degraded Sensor Mode *)
END_IF;

IF bAirlockDoorUnsealed OR bAirlockDoorOpenReq THEN
    dwAlarmWord_Advisory.4 := TRUE; (* Airlock Transit Active *)
END_IF;

(* --------------------------------------------------------------------------------------------- *)
(* 7.4 PACK SYSTEM STATUS WORD & MAP OUTPUT VARIABLES                                           *)
(* --------------------------------------------------------------------------------------------- *)
dwSystemStatusWord.0  := bMasterEnable;
dwSystemStatusWord.1  := bCleanroomReadyForWafer;
dwSystemStatusWord.2  := bPressureEnvelopeLocked;
dwSystemStatusWord.3  := bLaminarVelocityUniform;
dwSystemStatusWord.4  := bDewPointStable;
dwSystemStatusWord.5  := bDegradedSensorFallback;
dwSystemStatusWord.6  := bToxicPurgeActive;
dwSystemStatusWord.7  := (iFSM_State = STATE_PRODUCTION_READY);
dwSystemStatusWord.8  := (iFSM_State = STATE_AIRLOCK_COMPENSATION);
dwSystemStatusWord.9  := (iFSM_State = STATE_NIGHT_SETBACK_STANDBY);
dwSystemStatusWord.10 := (iFSM_State = STATE_COLD_START_PURGE);

(* Save Past Control Commands for Bumpless Rate Limiting *)
FOR iIdx := 1 TO 8 DO
    aControlU_Prev[iIdx] := aControlU[iIdx];
END_FOR;

(* Assign Physical Actuator Output Commands *)
rCmd_FFU_Speed_rpm          := aControlU[1];
rCmd_MAU_SupplyDamper_pct   := aControlU[2];
rCmd_ExhaustDamper_pct      := aControlU[3];
rCmd_ChilledWaterValve_pct  := aControlU[4];
rCmd_DX_TrimCoil_pct        := aControlU[5];
rCmd_SteamHumidifier_pct    := aControlU[6];
rCmd_ElectricReheat_pct     := aControlU[7];
rCmd_AirlockBooster_pct     := aControlU[8];

(* Assign Diagnostic and Telemetry Output Estimates *)
rEst_LithoDiffPress_Pa      := rVoted_PressDiff_Litho_Pa;
rEst_LaminarFaceVel_mps     := rVoted_Velocity_Face_mps;
rEst_DryBulbTemp_degC       := rVoted_Temp_DryBulb_degC;
rEst_DewPointTemp_degC      := rVoted_Temp_DewPoint_degC;
rEst_MoistAirEnthalpy_kJpkg := rCalculatedMoistAirEnthalpy;
rEst_ChemicalFilterLife_pct := rAMC_RemainingLife_pct;
rEst_AcousticVibRMS_mms     := rVib_FilteredRMS;

END_FUNCTION_BLOCK
"""
    parts.append(code_body)
    
    return "".join(parts)

if __name__ == "__main__":
    code = build_code()
    print(f"Generated Structured Text length: {len(code)} characters")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Semiconductor & Wafer Fab Infrastructure: Class 1 (ISO 3) Cleanroom Recirculating Air Handling Unit (RAHU) with Active Laminar Airflow Face Velocity, Pressure Cascade Envelope & Dew-Point Reg**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Semiconductor_Cleanroom_ISO3_HVAC_Cascade
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [Pa], [m/s], [deg C], [%RH], [rpm], [m3/h], [bar], [mA], [ppb])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Semiconductor_Cleanroom_ISO3_HVAC_Cascade
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(\"data/swarm_raw/agent_1c8209da.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Semiconductor & Wafer Fab Infrastructure: Class 1 (ISO 3) Cleanroom Recirculating Air Handling Unit (RAHU) with Active Laminar Airflow Face Velocity, Pressure Cascade Envelope & Dew-Point Reg"""

    full_assistant_content = f"```iec-st\n{code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_assistant_content}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    out_file = "data/swarm_raw/agent_1c8209da.json"
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Dataset successfully written to {out_file} (Assistant content: {len(full_assistant_content)} chars)")
