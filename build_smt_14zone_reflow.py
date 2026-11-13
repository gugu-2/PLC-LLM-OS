# -*- coding: utf-8 -*-
"""
Builder and validator for FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum
Generates a complete, ultra-dense, mathematically rigorous IEC 61131-3 dataset.
Target: 80,000 to 120,000+ characters, 100% exact syntax parity, 0 validation errors.
"""

import sys
import os
import json
import uuid
import re

import validate_iec

def generate_user_prompt():
    return """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electronics SMT & Semiconductor Packaging (Tier 1 Priority Sector): High-Precision 14-Zone Convection Reflow Soldering Oven with Closed-Loop Nitrogen Inerting (< 35 ppm O2), Dual-Chamber Gas Seals, Dual-Lane Conveyor Speed Synchronization & Thermal Load Feedforward, 14-Zone Cascade PID Heating with Multi-Thermocouple Delta-T Thermal Shock Protection, and Integrated Vacuum Voiding Chamber (< 1% BGA/QFN Solder Voiding) with Controlled Pressure Ramp Rate.**

**Function Block Name**: `FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum`

**Engineering Context & Operational Architecture**:
1. Convection Tunnel & 14-Zone Cascade Thermal Control:
   - 14 independently controlled upper and lower heating plenums (28 heat cells) with variable frequency convection impellers.
   - First-principles forced convection Nusselt/Reynolds heat transfer modeling, multi-layer PCBA thermal capacitance absorption dynamics, and multi-thermocouple Delta-T thermal shock protection (max heating rate +2.0 °C/s, max cooling rate -3.5 °C/s).
   - SAC305 lead-free profile tracking: 140-190 °C flux activation soak, 217 °C liquidus crossing, 245 °C peak reflow, and 60-75 s Time Above Liquidus (TAL).
2. Closed-Loop Liquid Nitrogen (N2) Inerting & Dual Gas Seals:
   - High-purity N2 continuous blanket maintaining residual atmospheric oxygen < 35 ppm O2 (target 15 to 25 ppm) across soak and reflow zones to minimize solder paste oxidation and eliminate Head-in-Pillow (HIP) defects.
   - Dual-chamber entrance and exit labyrinth gas curtains with dynamic exhaust damper differential pressure balance (+0.25 mbar internal tunnel overpressure) preventing cleanroom air ingress.
   - 2oo3 Triple Modular Redundancy (TMR) Zirconia (ZrO2) solid-state electrochemical potentiometric O2 sensors with automatic electrode fouling drift compensation.
3. Integrated Deep Vacuum Solder Voiding Chamber:
   - Positioned immediately between Peak Reflow (Zone 11) and Controlled Cooling (Zone 12).
   - Pneumatic hermetic sealing gate valves, roots booster dry vacuum pump package, and dual capacitance manometers (2oo3 TMR).
   - Controlled sub-millibar evacuation ramp down to 15 mbar while solder is molten, extracting entrapped volatile flux gases from BGA/QFN joints to achieve < 1.0% void area per IPC-7095 Class 3, followed by a controlled N2 backfill ramp.
4. Dual-Lane Dynamic Speed Synchronization & Board Mass Feedforward:
   - Lane 1 and Lane 2 independent mesh belt pin chain servos with optical tachometers (2oo3 TMR).
   - Thermal load feedforward computing incoming board mass flow and substrate layer count to pre-compensate zone heating duty cycles before convective thermal dip.
5. 8-State Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E d_k$):
   - 8 states: Mean preheat bulk gas temp (Z1-Z4), Mean soak plateau bulk gas temp (Z5-Z8), Mean peak reflow bulk gas temp (Z9-Z11), Mean cooling bulk gas temp (Z12-Z14), PCBA core absorbed temperature, Internal residual O2 concentration, Vacuum chamber absolute pressure, and Tunnel differential pressure vs ambient.
   - 8 control inputs: Zone group heater PWM duties, cooling N2 valve, main N2 purge valve, labyrinth seal trim, vacuum throttle, and vacuum N2 backfill valve.
6. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) with physical box saturation and dynamic slew rate limiters.
7. Deterministic 14-Stage Production Finite State Machine (FSM):
   - From initial N2 purge, O2 stabilization, cascade heating ramp, soak equilibration, dual-lane infeed sync, active convection reflow, vacuum chamber transfer, pumpdown degassing, N2 backfill, cooling outfeed, to recipe transitions and thermal abort.
8. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance hysteresis and 32-bit status/diagnostic words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

def build_code():
    parts = []
    
    # -------------------------------------------------------------------------
    # PART 1: Function Block Header & Cyber-Physical Technical Comments
    # -------------------------------------------------------------------------
    parts.append("""FUNCTION_BLOCK FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CRITICAL ELECTRONICS SMT & SEMICONDUCTOR PACKAGING REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : HIGH-PRECISION 14-ZONE CONVECTION REFLOW SOLDERING OVEN WITH INTEGRATED VACUUM VOIDING
  ATMOSPHERIC MATRIX : HIGH-PURITY NITROGEN (N2) INERT BLANKET WITH SUB-35 PPM RESIDUAL OXYGEN (O2) REGULATION
  VACUUM SUBSYSTEM   : SUB-MILLIBAR IN-LINE VACUUM VOIDING MODULE (< 1.0% BGA/QFN SOLDER VOIDING, IPC-7095 CLASS 3)
  TRANSPORT PLATFORM : DUAL-LANE MESH BELT / PIN CHAIN WITH SPEED SYNCHRONIZATION & BOARD THERMAL MASS FEEDFORWARD
  THERMAL REGULATION : 14-ZONE CASCADE PID HEATING WITH MULTI-THERMOCOUPLE DELTA-T THERMAL SHOCK PROTECTION
  SAFETY INTEGRITY   : IEC 61508 / IEC 61511 SIL-2/SIL-3 REDUNDANT OVEN PROTECTION WITH HARDWIRED OVERTEMP E-STOP
  APPLICABLE NORMS   : IPC-A-610 CLASS 3 (HIGH PERFORMANCE ELECTRONIC ASSEMBLIES), IPC J-STD-004/005 (FLUX & PASTE),
                       IPC-7095 (CRITERIA FOR BGA VOIDING CONTROL), JEDEC J-STD-020E (MOISTURE/REFLOW SENSITIVITY),
                       SEMI S2/S8 ENVIRONMENTAL HEALTH & SAFETY, ISA-18.2 / IEC 62682 MANAGEMENT OF INDUSTRIAL ALARMS,
                       NFPA 86 STANDARD FOR OVENS AND FURNACES, DIN EN 61010-1 SAFETY REQUIREMENTS.
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL THERMODYNAMIC FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. FORCED CONVECTION HEAT TRANSFER IN A 14-ZONE REFLOW TUNNEL:
     - In ultra-high-density SMT manufacturing, printed circuit board assemblies (PCBAs) containing mixed micro-components
       (01005 / 0201 chip passives, 0.3 mm pitch WLCSP, 1500+ pin BGAs, stacked-die SiP, and high thermal mass power inductors)
       must be heated and cooled through a strictly prescribed time-temperature curve without exceeding allowable Delta-T.
     - The 14-zone reflow tunnel is configured with 14 upper and 14 lower convection plenum modules (28 total heating cells).
       Each cell incorporates high-temperature FeCrAl alloy heating elements, a centrifugal impeller blower driven by
       variable frequency drives (VFDs), and precision perforated orifice diffusers delivering high-velocity convection
       gas jets perpendicular to the travelling PCBA surface.
     - The net thermal energy transferred to the board surface per unit area in zone i is governed by coupled convective
       and radiative flux mechanisms:
           q_net_i = q_conv_upper + q_conv_lower + q_rad_upper + q_rad_lower - q_loss
           q_conv  = h_conv(v_gas, T_gas) * (T_gas - T_pcb_surface)
           q_rad   = epsilon_eff * sigma_SB * (T_emitter_K^4 - T_pcb_K^4)
       where:
           h_conv(v_gas) = 2.45 * (k_gas / D_hyd) * (Re_jet^0.68) * (Pr_gas^0.42)
           Re_jet        = (rho_gas * v_gas_jet * D_orifice) / mu_gas
           sigma_SB      = 5.670374e-8 W/(m^2*K^4)  (Stefan-Boltzmann constant)
           epsilon_eff   = Effective emissivity of the solder resist / component envelope (0.84 to 0.92)
           v_gas_jet     = Static pressure head driven convection jet discharge velocity (5.0 to 18.0 m/s)

  2. MULTI-MASS TRANSIENT THERMAL LUMPED CAPACITANCE DYNAMICS:
     - The travelling PCBA is represented by a multi-node lumped capacitance thermal model coupled to the continuous
       longitudinal coordinate z along the oven conveyor length L_oven:
           z(t) = integral_0^t v_conv(tau) dtau
     - Three distinctive thermal masses are simultaneously tracked at each longitudinal section:
       * Node 1: Micro-mass low-capacitance chip passives (e.g. 0201 chip capacitors, R_th = low, C_th = low):
           C_th_micro * (dT_micro / dt) = h_conv_upper * A_micro * (T_gas_upper - T_micro) + q_rad_micro
       * Node 2: Macro-mass high-capacitance semiconductor die (e.g. 1500-pin BGA heat spreader, R_th = high, C_th = high):
           C_th_macro * (dT_macro / dt) = h_conv_eff * A_macro * (T_gas - T_macro) - G_conductive * (T_macro - T_pcb)
       * Node 3: Multi-layer FR4/Copper PCB core substrate (6 to 24 layers, R_th = internal, C_th = distributed):
           C_th_board * (dT_pcb / dt)   = (h_upper*A_pcb*(T_upper - T_pcb) + h_lower*A_pcb*(T_lower - T_pcb)) + G_int*(T_macro - T_pcb)
     - Critical Processing Constraints (IPC-7530A / J-STD-020E):
       a) Maximum Ramp-Up Slope (Thermal Shock Margin):
          dT_pcb / dt <= +2.0 deg C/s (+1.5 to +1.8 deg C/s nominal). Excessive heating rate causes explosive flux outgassing,
          solder spattering, and internal micro-cracking of sensitive MLCC barium titanate dielectric ceramics.
       b) Thermal Equilibrium Soak Plateau (Soak Zones 5-8, 150 deg C to 190 deg C, 60s to 120s):
          Permits temperature equilibrium across large and small components (Delta-T across PCBA <= 4.0 deg C), while
          activating organic acid flux activators (adipic acid, glutaric acid) to reduce tin/copper/nickel oxides.
       c) Time Above Liquidus (TAL) (Reflow Zones 9-11, T > 217.0 deg C for SAC305):
          Must strictly remain within 50.0 to 75.0 seconds. Peak temperature must reach 238.0 deg C to 248.0 deg C (nominal 244 deg C).
          Insufficient TAL (< 45s) leads to cold joints, incomplete intermetallic compound (IMC) formation, and voids.
          Excessive TAL (> 90s) leads to excessive Cu6Sn5 and Cu3Sn brittle intermetallic growth (> 5 um), component degradation,
          and PCB substrate delamination / glass transition degradation (Tg = 170 deg C).
       d) Controlled Cooling Gradient (Cooling Zones 12-14):
          Cooling rate must be governed between -2.0 deg C/s and -3.5 deg C/s (nominal -2.8 deg C/s).
          Too slow (< -1.5 deg C/s) yields coarse dendritic beta-Sn crystal grains and degraded mechanical shear strength.
          Too fast (> -4.5 deg C/s) introduces severe thermal contraction stress, solder fatigue cracking, and component popcorning.

  3. INTEGRATED DEEP VACUUM SOLDER VOIDING EXTRACTION DYNAMICS:
     - Positioned immediately following Peak Reflow Zone 11 while solder joints remain in full molten liquidus state:
       * When solder alloy is in liquidus state (T_solder = 230 to 245 deg C), surface tension creates spherical entrapped
         gas pockets formed by flux outgassing (polyethylene glycol, rosin solvents, activator decomposition).
       * In ambient convection reflow, internal bubble pressure equals external atmospheric pressure plus Laplace pressure:
           P_bubble = P_ambient + (2 * gamma_liquid_solder) / r_void
         where gamma_liquid_solder = 0.48 N/m for SAC305. Small micro-voids (r < 50 um) have very high Laplace pressures
         and cannot escape through viscous molten solder under standard gravity.
       * In the integrated vacuum voiding chamber, external ambient pressure is evacuated from 1013 mbar down to 15 mbar
         via a dry screw roots booster package at a controlled evacuation rate (dP/dt = -30 to -35 mbar/s).
       * As P_chamber drops below P_bubble, the void expands geometrically per the ideal gas law:
           r_expanded = r_initial * (P_initial / P_chamber)^(1/3)
       * The buoyancy force F_buoyancy = (4/3) * pi * r^3 * rho_solder * g increases by the volume expansion factor (approx 65x),
         causing the enlarged gas bubbles to rapidly rise through the molten solder joint to the surface and rupture cleanly.
       * Dwell time at deep vacuum (15 mbar) is precisely timed for 10.0 to 14.0 seconds.
       * A controlled nitrogen backfill ramp (dP/dt = +40 to +45 mbar/s) restores atmospheric pressure smoothly,
         collapsing any residual micro-cavities without disturbing component alignment or causing solder splash.
       * Resulting PCBA joints achieve < 1.0% total voiding area (frequently < 0.5%), completely surpassing IPC-7095 Class 3.

  4. CLOSED-LOOP RESIDUAL OXYGEN (O2) PURITY & GAS SEAL AERODYNAMICS:
     - Ultra-pure nitrogen (N2, 99.999% purity / Grade 5.0) is continuously injected into the reflow tunnel
       to depress residual atmospheric oxygen concentration below 35 ppm O2 (target 15 to 25 ppm O2).
     - The ultra-low oxygen environment reduces molten solder surface tension, accelerates liquidus wetting,
       eliminates head-in-pillow (HIP) solder defects on fine-pitch BGAs, and suppresses dross formation.
     - Mass balance of residual oxygen in the oven chamber volume V_tunnel (approx 6.5 m^3):
           V_tunnel * (dC_O2 / dt) = Q_ingress * C_O2_ambient + Q_N2_purge * C_O2_N2_supply - Q_exhaust * C_O2(t) - R_consumption
       where:
           C_O2_ambient   = 209,500 ppm O2 (20.95 vol% in atmospheric cleanroom air)
           C_O2_N2_supply = 2.0 to 5.0 ppm O2 (residual in commercial cryogenic liquid N2 boil-off)
           Q_ingress      = Ingress leakage rate through entrance and exit board curtains [Nm3/h]
           Q_exhaust      = Volumetric extraction exhaust rate [Nm3/h]
           R_consumption  = Chemical oxygen scavenging consumed by flux acid reactions and organic volatilization.
     - Dual-chamber entrance and exit labyrinth gas curtains maintain positive internal tunnel pressure (+0.20 to +0.35 mbar)
       relative to the cleanroom, establishing a dynamic hydrodynamic gas barrier that repels atmospheric air ingress.
     - 2oo3 Triple Modular Redundancy (TMR) Zirconium Dioxide (ZrO2) solid-state electrochemical potentiometric sensors
       measure residual oxygen via the Nernst relation:
           EMF_cell = (R_gas * T_sensor_K) / (4 * F_const) * ln( P_O2_ambient / P_O2_tunnel )

  5. 8-STATE DISCRETE STATE-SPACE MODEL & EMBEDDED RECEDING-HORIZON MPC:
     - The multi-zone thermal, vacuum, and inert gas dynamics are formulated as a discrete-time state-space system:
           x[k+1] = A * x[k] + B * u[k] + E * d[k]
           y[k]   = C * x[k] + D * u[k]
       State Vector x (8x1):
         x[1]: Mean Preheat Bulk Convection Gas Temp (Zones 1-4)                 [deg C]
         x[2]: Mean Soak Plateau Bulk Convection Gas Temp (Zones 5-8)            [deg C]
         x[3]: Mean Peak Reflow Liquidus Convection Gas Temp (Zones 9-11)        [deg C]
         x[4]: Mean Controlled Cooling Convection Gas Temp (Zones 12-14)         [deg C]
         x[5]: Travelling PCBA Thermal Mass Absorbed Core Temp                   [deg C]
         x[6]: Internal Chamber Residual Oxygen Concentration                    [ppm O2]
         x[7]: Vacuum Voiding Chamber Absolute Pressure                          [mbar]
         x[8]: Tunnel Differential Static Pressure vs Cleanroom                  [mbar]
       Manipulated Control Input Vector u (8x1):
         u[1]: Preheat Zones Master Heating Duty Cycle Command                   [%] (0.0 to 100.0%)
         u[2]: Soak Zones Master Heating Duty Cycle Command                      [%] (0.0 to 100.0%)
         u[3]: Peak Reflow Zones Master Heating Duty Cycle Command               [%] (0.0 to 100.0%)
         u[4]: Cooling Zones Chilled N2 Convection Proportional Valve            [%] (0.0 to 100.0%)
         u[5]: Nitrogen Atmosphere High-Purity Ingress Purge Trim Valve          [%] (0.0 to 100.0%)
         u[6]: Entrance & Exit Dual Labyrinth Gas Seal Curtain Trim Valve        [%] (0.0 to 100.0%)
         u[7]: Vacuum Chamber Roots Throttle Evacuation Valve                    [%] (0.0 to 100.0%)
         u[8]: Vacuum Chamber Nitrogen Backfill Venting Valve                    [%] (0.0 to 100.0%)
       External Disturbance Vector d (4x1):
         d[1]: Dual-Lane Cumulative PCBA Infeed Thermal Mass Flow Rate           [kg/min]
         d[2]: Ambient Cleanroom Air Temperature                                 [deg C]
         d[3]: Cleanroom Static Barometric Pressure Fluctuation                  [mbar]
         d[4]: Solder Paste Volatile Organic Flux Outgassing Generation Rate     [mg/s]
*)
""")

    # -------------------------------------------------------------------------
    # PART 2: VAR_INPUT Block (35 strongly typed inputs with physical units)
    # -------------------------------------------------------------------------
    parts.append("""VAR_INPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM ENABLES, RUN COMMANDS & SAFETY SIGNALS                                           *)
    (* ============================================================================================== *)
    bSystemEnable                       : BOOL;     (* Master System Enable / Hardware Power Permissive *)
    bProductionRunCmd                   : BOOL;     (* Production Run Command from Line Supervisory SCADA *)
    bEmergencyStop                      : BOOL;     (* Hardwired SIL-3 Safety Circuit Status (1=Healthy, 0=Tripped) *)
    bAlarmAcknowledge                   : BOOL;     (* Operator Alarm Acknowledge Pushbutton / HMI Trigger *)
    bAlarmReset                         : BOOL;     (* Master Alarm Reset Pushbutton / HMI Trigger *)
    
    (* ============================================================================================== *)
    (* FLUID SUPPLY & CLEANROOM AMBIENT SENSORS WITH BRACKETED PHYSICAL UNITS                         *)
    (* ============================================================================================== *)
    rSupplyNitrogenPressure_bar         : REAL;     (* Bulk Liquid N2 Vaporizer Delivery Manifold Pressure [bar] *)
    rAmbientCleanroomTemp_degC          : REAL;     (* SMT Cleanroom Ambient Temperature [deg C] *)
    rCleanroomAmbientPressure_mbar      : REAL;     (* SMT Cleanroom Ambient Barometric Pressure [mbar] *)
    rExhaustExtractionFlow_Nm3h         : REAL;     (* Oven Flux Condensation Exhaust Blower Flow Rate [Nm3/h] *)
    rInletCurtainDifferential_mbar      : REAL;     (* Entrance Dual-Chamber Labyrinth Gas Seal Differential [mbar] *)
    rOutletCurtainDifferential_mbar     : REAL;     (* Exit Dual-Chamber Labyrinth Gas Seal Differential [mbar] *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANT (TMR) PRIMARY INSTRUMENTATION CHANNELS                           *)
    (* ============================================================================================== *)
    rO2_Sensor_A_ppm                    : REAL;     (* Zirconia Electrochemical Oxygen Sensor Channel A [ppm] *)
    rO2_Sensor_B_ppm                    : REAL;     (* Zirconia Electrochemical Oxygen Sensor Channel B [ppm] *)
    rO2_Sensor_C_ppm                    : REAL;     (* Zirconia Electrochemical Oxygen Sensor Channel C [ppm] *)
    
    rReflowTemp_Z10_A_degC              : REAL;     (* Peak Reflow Zone 10 Triplicate RTD Sensor Channel A [deg C] *)
    rReflowTemp_Z10_B_degC              : REAL;     (* Peak Reflow Zone 10 Triplicate RTD Sensor Channel B [deg C] *)
    rReflowTemp_Z10_C_degC              : REAL;     (* Peak Reflow Zone 10 Triplicate RTD Sensor Channel C [deg C] *)
    
    rVacGauge_A_mbar                    : REAL;     (* Vacuum Chamber Capacitance Manometer Channel A [mbar] *)
    rVacGauge_B_mbar                    : REAL;     (* Vacuum Chamber Capacitance Manometer Channel B [mbar] *)
    rVacGauge_C_mbar                    : REAL;     (* Vacuum Chamber Capacitance Manometer Channel C [mbar] *)
    
    rBeltSpeed_L1_A_mmpm                : REAL;     (* Lane 1 Mesh Belt Optical Tachometer Channel A [mm/min] *)
    rBeltSpeed_L1_B_mmpm                : REAL;     (* Lane 1 Mesh Belt Optical Tachometer Channel B [mm/min] *)
    rBeltSpeed_L1_C_mmpm                : REAL;     (* Lane 1 Mesh Belt Optical Tachometer Channel C [mm/min] *)
    rBeltSpeed_L2_mmpm                  : REAL;     (* Lane 2 Mesh Belt Optical Tachometer Channel Feedback [mm/min] *)
    
    (* ============================================================================================== *)
    (* 14-ZONE UPPER/LOWER MEAN BULK GAS TEMPERATURE PROCESS VALUES (PV)                             *)
    (* ============================================================================================== *)
    rZoneTemp_PV_01_degC                : REAL;     (* Zone 1 Convection Heating Gas Process Value (Ramp 1) [deg C] *)
    rZoneTemp_PV_02_degC                : REAL;     (* Zone 2 Convection Heating Gas Process Value (Ramp 2) [deg C] *)
    rZoneTemp_PV_03_degC                : REAL;     (* Zone 3 Convection Heating Gas Process Value (Ramp 3) [deg C] *)
    rZoneTemp_PV_04_degC                : REAL;     (* Zone 4 Convection Heating Gas Process Value (Ramp 4) [deg C] *)
    rZoneTemp_PV_05_degC                : REAL;     (* Zone 5 Convection Heating Gas Process Value (Soak 1) [deg C] *)
    rZoneTemp_PV_06_degC                : REAL;     (* Zone 6 Convection Heating Gas Process Value (Soak 2) [deg C] *)
    rZoneTemp_PV_07_degC                : REAL;     (* Zone 7 Convection Heating Gas Process Value (Soak 3) [deg C] *)
    rZoneTemp_PV_08_degC                : REAL;     (* Zone 8 Convection Heating Gas Process Value (Soak 4) [deg C] *)
    rZoneTemp_PV_09_degC                : REAL;     (* Zone 9 Convection Heating Gas Process Value (Reflow 1) [deg C] *)
    rZoneTemp_PV_10_degC                : REAL;     (* Zone 10 Convection Heating Gas Process Value (Reflow Peak 2) [deg C] *)
    rZoneTemp_PV_11_degC                : REAL;     (* Zone 11 Convection Heating Gas Process Value (Reflow Spike 3) [deg C] *)
    rZoneTemp_PV_12_degC                : REAL;     (* Zone 12 Convection Cooling Gas Process Value (Cool 1) [deg C] *)
    rZoneTemp_PV_13_degC                : REAL;     (* Zone 13 Convection Cooling Gas Process Value (Cool 2) [deg C] *)
    rZoneTemp_PV_14_degC                : REAL;     (* Zone 14 Convection Cooling Gas Process Value (Cool 3 Exit) [deg C] *)
    
    (* ============================================================================================== *)
    (* 14-ZONE ACTIVE RECIPE TEMPERATURE SETPOINTS (SP)                                               *)
    (* ============================================================================================== *)
    rZoneTemp_SP_01_degC                : REAL;     (* Recipe Setpoint Zone 1 Initial Preheat Ramp [deg C] *)
    rZoneTemp_SP_02_degC                : REAL;     (* Recipe Setpoint Zone 2 Intermediate Preheat Ramp [deg C] *)
    rZoneTemp_SP_03_degC                : REAL;     (* Recipe Setpoint Zone 3 Upper Preheat Ramp [deg C] *)
    rZoneTemp_SP_04_degC                : REAL;     (* Recipe Setpoint Zone 4 Soak Entry Ramp [deg C] *)
    rZoneTemp_SP_05_degC                : REAL;     (* Recipe Setpoint Zone 5 Soak Plateau Stage 1 [deg C] *)
    rZoneTemp_SP_06_degC                : REAL;     (* Recipe Setpoint Zone 6 Soak Plateau Stage 2 [deg C] *)
    rZoneTemp_SP_07_degC                : REAL;     (* Recipe Setpoint Zone 7 Soak Plateau Stage 3 [deg C] *)
    rZoneTemp_SP_08_degC                : REAL;     (* Recipe Setpoint Zone 8 Soak Plateau Exit Stage 4 [deg C] *)
    rZoneTemp_SP_09_degC                : REAL;     (* Recipe Setpoint Zone 9 Liquidus Transition Ramp [deg C] *)
    rZoneTemp_SP_10_degC                : REAL;     (* Recipe Setpoint Zone 10 Peak Reflow Spike [deg C] *)
    rZoneTemp_SP_11_degC                : REAL;     (* Recipe Setpoint Zone 11 Reflow Vacuum Transition [deg C] *)
    rZoneTemp_SP_12_degC                : REAL;     (* Recipe Setpoint Zone 12 Controlled Cooling Stage 1 [deg C] *)
    rZoneTemp_SP_13_degC                : REAL;     (* Recipe Setpoint Zone 13 Rapid Cooling Stage 2 [deg C] *)
    rZoneTemp_SP_14_degC                : REAL;     (* Recipe Setpoint Zone 14 Final Exit Cooling Stage 3 [deg C] *)
    
    (* ============================================================================================== *)
    (* DUAL-LANE CONVEYOR PACING & PCBA THERMAL LOAD FEEDFORWARD PARAMETERS                           *)
    (* ============================================================================================== *)
    rConveyorNominalSpeed_mmpm          : REAL;     (* Production Recipe Conveyor Speed Setpoint [mm/min] *)
    bBoardPresent_L1_Infeed             : BOOL;     (* Optical Sensor: PCBA Detected at Lane 1 Oven Entry *)
    bBoardPresent_L2_Infeed             : BOOL;     (* Optical Sensor: PCBA Detected at Lane 2 Oven Entry *)
    rBoardMass_L1_grams                 : REAL;     (* Incoming PCBA Mass for Thermal Compensation Lane 1 [grams] *)
    rBoardMass_L2_grams                 : REAL;     (* Incoming PCBA Mass for Thermal Compensation Lane 2 [grams] *)
    rBoardSurfaceArea_L1_cm2            : REAL;     (* Incoming PCBA Effective Convection Area Lane 1 [cm2] *)
    rBoardSurfaceArea_L2_cm2            : REAL;     (* Incoming PCBA Effective Convection Area Lane 2 [cm2] *)
    nBoardCopperLayers_L1               : INT;      (* Internal Copper Layer Count Lane 1 (Thermal Mass Multiplier) *)
    nBoardCopperLayers_L2               : INT;      (* Internal Copper Layer Count Lane 2 (Thermal Mass Multiplier) *)
    
    (* ============================================================================================== *)
    (* INTEGRATED VACUUM VOIDING MODULE HARDWARE LIMITS & RECIPE RECESS                               *)
    (* ============================================================================================== *)
    rVacPumpSpeedFeedback_rpm           : REAL;     (* Roots Booster Dry Vacuum Pump Operating Speed [rpm] *)
    bVacInletGateClosed_LS              : BOOL;     (* Vacuum Chamber Inlet Hermetic Gate Fully Closed Switch *)
    bVacOutletGateClosed_LS             : BOOL;     (* Vacuum Chamber Outlet Hermetic Gate Fully Closed Switch *)
    bVacInletGateOpened_LS              : BOOL;     (* Vacuum Chamber Inlet Hermetic Gate Fully Open Switch *)
    bVacOutletGateOpened_LS             : BOOL;     (* Vacuum Chamber Outlet Hermetic Gate Fully Open Switch *)
    bBoardPresent_VacChamber            : BOOL;     (* Internal High-Temp Optical Sensor: PCBA in Vacuum Cell *)
    rVacTargetPressure_mbar             : REAL;     (* Target Deep Vacuum Solder Voiding Pressure [mbar] *)
    rVacDwellDuration_s                 : REAL;     (* Deep Vacuum Degassing Hold Duration [s] *)
    rVacMaxPumpdownRamp_mbarps          : REAL;     (* Maximum Allowable Evacuation Ramp Rate [mbar/s] *)
    rVacMaxBackfillRamp_mbarps          : REAL;     (* Maximum Allowable N2 Venting Backfill Ramp Rate [mbar/s] *)
    
    (* ============================================================================================== *)
    (* UPSTREAM & DOWNSTREAM SMEMA / IPC-HERMES PRODUCTION HANDSHAKES                                 *)
    (* ============================================================================================== *)
    bSMEMA_InfeedReady_L1               : BOOL;     (* Upstream SMT Pick & Place Infeed Ready Lane 1 *)
    bSMEMA_InfeedReady_L2               : BOOL;     (* Upstream SMT Pick & Place Infeed Ready Lane 2 *)
    bSMEMA_OutfeedReady_L1              : BOOL;     (* Downstream AOI Vision Inspector Ready Lane 1 *)
    bSMEMA_OutfeedReady_L2              : BOOL;     (* Downstream AOI Vision Inspector Ready Lane 2 *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 3: VAR_OUTPUT Block (34 strongly typed outputs with status words)
    # -------------------------------------------------------------------------
    parts.append("""VAR_OUTPUT
    (* ============================================================================================== *)
    (* MASTER SYSTEM STATUS & PRODUCTION SUPERVISORY FLAGS                                           *)
    (* ============================================================================================== *)
    bSystemReady                        : BOOL;     (* Oven Fully Preheated, Purged & Ready for Production *)
    bProductionActive                   : BOOL;     (* Active Continuous Soldering Conveyor & Chamber Operation *)
    bEmergencyTripActive                : BOOL;     (* SIL-3 Safety Emergency Stop or Critical Over-Temp Tripped *)
    nOvenOperationalState               : INT;      (* Current 14-Stage FSM Operational Stage Code (0 to 14) *)
    
    (* ============================================================================================== *)
    (* 2oo3 TMR VALIDATED SENSOR VALUES & INTEGRATED METRICS                                          *)
    (* ============================================================================================== *)
    rVotedOxygenConcentration_ppm       : REAL;     (* 2oo3 TMR Voted Residual Oxygen Concentration [ppm] *)
    rVotedReflowTemp_Z10_degC           : REAL;     (* 2oo3 TMR Voted Peak Reflow Zone 10 Temperature [deg C] *)
    rVotedVacuumPressure_mbar           : REAL;     (* 2oo3 TMR Voted Vacuum Chamber Absolute Pressure [mbar] *)
    rVotedBeltSpeed_L1_mmpm             : REAL;     (* 2oo3 TMR Voted Lane 1 Mesh Belt Speed [mm/min] *)
    rObservedPCBACoreTemp_degC          : REAL;     (* Cyber-Physical State-Space PCBA Core Temp Estimate [deg C] *)
    rEstimatedTimeAboveLiquidus_s       : REAL;     (* Real-Time Computed Time Above 217 deg C Liquidus (TAL) [s] *)
    rPeakDeltaTAcrossOven_degC          : REAL;     (* Maximum Observed Temperature Gradient Across Board [deg C] *)
    
    (* ============================================================================================== *)
    (* 14-ZONE CONVECTION HEATER SOLID STATE RELAY (SSR) PWM DUTY CYCLE COMMANDS (0.0 to 100.0 %)     *)
    (* ============================================================================================== *)
    rZoneHeaterCommand_01_pct           : REAL;     (* Zone 1 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_02_pct           : REAL;     (* Zone 2 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_03_pct           : REAL;     (* Zone 3 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_04_pct           : REAL;     (* Zone 4 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_05_pct           : REAL;     (* Zone 5 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_06_pct           : REAL;     (* Zone 6 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_07_pct           : REAL;     (* Zone 7 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_08_pct           : REAL;     (* Zone 8 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_09_pct           : REAL;     (* Zone 9 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_10_pct           : REAL;     (* Zone 10 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_11_pct           : REAL;     (* Zone 11 Heating Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_12_pct           : REAL;     (* Zone 12 Heating/Cooling Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_13_pct           : REAL;     (* Zone 13 Heating/Cooling Actuator PWM Duty Cycle Output [%] *)
    rZoneHeaterCommand_14_pct           : REAL;     (* Zone 14 Cooling Actuator PWM Duty Cycle Output [%] *)
    
    (* ============================================================================================== *)
    (* 14-ZONE VARIABLE FREQUENCY CONVECTION BLOWER SPEED COMMANDS (Hz)                               *)
    (* ============================================================================================== *)
    rZoneBlowerSpeed_01_Hz              : REAL;     (* Zone 1 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_02_Hz              : REAL;     (* Zone 2 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_03_Hz              : REAL;     (* Zone 3 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_04_Hz              : REAL;     (* Zone 4 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_05_Hz              : REAL;     (* Zone 5 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_06_Hz              : REAL;     (* Zone 6 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_07_Hz              : REAL;     (* Zone 7 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_08_Hz              : REAL;     (* Zone 8 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_09_Hz              : REAL;     (* Zone 9 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_10_Hz              : REAL;     (* Zone 10 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_11_Hz              : REAL;     (* Zone 11 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_12_Hz              : REAL;     (* Zone 12 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_13_Hz              : REAL;     (* Zone 13 Convection Impeller VFD Frequency Command [Hz] *)
    rZoneBlowerSpeed_14_Hz              : REAL;     (* Zone 14 Convection Impeller VFD Frequency Command [Hz] *)
    
    (* ============================================================================================== *)
    (* NITROGEN INERTING, GAS SEALS & EXHAUST DAMPER ACTUATORS                                       *)
    (* ============================================================================================== *)
    rN2_MainPurgeValve_pct              : REAL;     (* Bulk Gaseous N2 Main Flow Control Valve Position [%] *)
    rN2_InletCurtainValve_pct           : REAL;     (* Entrance Dual Labyrinth Gas Curtain Trim Valve [%] *)
    rN2_OutletCurtainValve_pct          : REAL;     (* Exit Dual Labyrinth Gas Curtain Trim Valve [%] *)
    rExhaustDamperPosition_pct          : REAL;     (* Dynamic Flux Exhaust Blower Damper Position [%] *)
    
    (* ============================================================================================== *)
    (* INTEGRATED VACUUM CHAMBER ACTUATOR & VALVE COMMANDS                                           *)
    (* ============================================================================================== *)
    bVacPumpRunCommand                  : BOOL;     (* Dry Screw Roots Booster Vacuum Pump Start Command *)
    rVacRoughingThrottle_pct            : REAL;     (* Vacuum Evacuation Proportional Butterfly Valve [%] *)
    rVacBackfillN2Valve_pct             : REAL;     (* High-Purity N2 Chamber Venting Backfill Valve [%] *)
    bVacInletGateOpenCmd                : BOOL;     (* Vacuum Inlet Hermetic Sealing Gate Open Solenoid *)
    bVacInletGateCloseCmd               : BOOL;     (* Vacuum Inlet Hermetic Sealing Gate Close Solenoid *)
    bVacOutletGateOpenCmd               : BOOL;     (* Vacuum Outlet Hermetic Sealing Gate Open Solenoid *)
    bVacOutletGateCloseCmd              : BOOL;     (* Vacuum Outlet Hermetic Sealing Gate Close Solenoid *)
    
    (* ============================================================================================== *)
    (* DUAL-LANE CONVEYOR SERVO COMMANDS & SMEMA INTERFACE SIGNALS                                   *)
    (* ============================================================================================== *)
    rBeltDriveCommand_L1_Hz             : REAL;     (* Lane 1 Mesh Belt Servo Inverter Speed Setpoint [Hz] *)
    rBeltDriveCommand_L2_Hz             : REAL;     (* Lane 2 Mesh Belt Servo Inverter Speed Setpoint [Hz] *)
    bSMEMA_InfeedAccept_L1              : BOOL;     (* SMEMA Infeed Ready / Accept Board Transfer Lane 1 *)
    bSMEMA_InfeedAccept_L2              : BOOL;     (* SMEMA Infeed Ready / Accept Board Transfer Lane 2 *)
    bSMEMA_OutfeedRequest_L1            : BOOL;     (* SMEMA Outfeed Transfer Request to AOI Lane 1 *)
    bSMEMA_OutfeedRequest_L2            : BOOL;     (* SMEMA Outfeed Transfer Request to AOI Lane 2 *)
    
    (* ============================================================================================== *)
    (* BIT-PACKED STATUS WORDS & ISA-18.2 ALARM GROUPS                                               *)
    (* ============================================================================================== *)
    dwOvenStatusWord                    : DWORD;    (* 32-Bit Machine Operational Status Bitmask *)
    dwOvenDiagnosticWord                : DWORD;    (* 32-Bit Hardware Safety & Fault Diagnostic Word *)
    bAlarmGroupHighHigh_Overtemp        : BOOL;     (* Priority 1 Critical Over-Temperature Alarm *)
    bAlarmGroupHigh_O2_Ingress          : BOOL;     (* Priority 2 Residual Oxygen Concentration Limit Trip *)
    bAlarmGroupLow_N2_Pressure          : BOOL;     (* Priority 2 Bulk Nitrogen Header Pressure Depleted *)
    bAlarmGroup_VacuumDegasFault        : BOOL;     (* Priority 2 Vacuum Degassing Evacuation/Dwell Trip *)
    bAlarmGroup_ConveyorDiscrepancy     : BOOL;     (* Priority 2 Dual Lane Conveyor Pacing / Slip Deviation *)
    bAlarmGroup_ThermalShockViolation   : BOOL;     (* Priority 2 Delta-T Thermal Shock Gradient Limit Trip *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # PART 4: VAR Internal Block (State-space, MPC, TMR, FSM, Alarms, Timers)
    # -------------------------------------------------------------------------
    parts.append("""VAR
    (* ============================================================================================== *)
    (* CONSTANTS & SYSTEM PARAMETERS                                                                  *)
    (* ============================================================================================== *)
    T_CYCLE_SEC                         : REAL := 0.050;    (* Discrete PLC Scan Interval Ts = 50 ms [s] *)
    NUM_ZONES                           : INT := 14;        (* Total Regulated Convection Plenums *)
    NUM_STATES                          : INT := 8;         (* Cyber-Physical State Dimension *)
    NUM_INPUTS                          : INT := 8;         (* Manipulated Control Actuator Dimension *)
    NUM_DISTURBANCES                    : INT := 4;         (* External Disturbance Input Dimension *)
    HORIZON_NP                          : INT := 5;         (* Receding-Horizon Prediction Horizon *)
    
    (* ============================================================================================== *)
    (* DISCRETE STATE-SPACE MATRICES & OBSERVER VARIABLES                                             *)
    (* x[k+1] = A * x[k] + B * u[k] + E * d[k]                                                        *)
    (* y[k]   = C * x[k] + D * u[k]                                                                   *)
    (* ============================================================================================== *)
    a_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Transition Matrix A (8x8) *)
    b_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Input Coupling Matrix B (8x8) *)
    c_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* State Output Matrix C (8x8) *)
    d_mat                               : ARRAY[1..8, 1..8] OF REAL;    (* Direct Feedthrough Matrix D (8x8) *)
    e_mat                               : ARRAY[1..8, 1..4] OF REAL;    (* Disturbance Coupling Matrix E (8x4) *)
    l_observer_gain                     : ARRAY[1..8] OF REAL;          (* Luenberger Observer Correction Gains *)
    
    x_state                             : ARRAY[1..8] OF REAL;          (* Estimated Cyber-Physical State x[k] *)
    x_next                              : ARRAY[1..8] OF REAL;          (* Predicted Next State Vector x[k+1] *)
    y_meas                              : ARRAY[1..8] OF REAL;          (* Filtered Output Measurement Vector y[k] *)
    u_ctrl                              : ARRAY[1..8] OF REAL;          (* Manipulated Control Input Vector u[k] *)
    d_dist                              : ARRAY[1..4] OF REAL;          (* Estimated External Disturbance Vector *)
    x_ref                               : ARRAY[1..8] OF REAL;          (* Reference State Setpoint Trajectory *)
    u_ref                               : ARRAY[1..8] OF REAL;          (* Nominal Equilibrium Actuator Command *)
    u_prev                              : ARRAY[1..8] OF REAL;          (* Previous Step Actuator Command u[k-1] *)
    
    (* ============================================================================================== *)
    (* MODEL PREDICTIVE CONTROL (MPC) COST MATRICES & PROJECTION BOUNDS                               *)
    (* J = sum( (x - x_ref)'*Q*(x - x_ref) + (u - u_ref)'*R*(u - u_ref) + du'*S*du ) + x_N'*P*x_N     *)
    (* ============================================================================================== *)
    q_diag                              : ARRAY[1..8] OF REAL;          (* State Tracking Penalty Diagonal Q *)
    r_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Effort Penalty Diagonal R *)
    s_diag                              : ARRAY[1..8] OF REAL;          (* Actuator Slew Rate Penalty Diagonal S *)
    p_diag                              : ARRAY[1..8] OF REAL;          (* Terminal State Penalty Diagonal P *)
    u_box_min                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Lower Bound Box Sat *)
    u_box_max                           : ARRAY[1..8] OF REAL;          (* Actuator Physical Upper Bound Box Sat *)
    du_slew_max                         : ARRAY[1..8] OF REAL;          (* Max Allowable Actuator Slew [units/step] *)
    
    u_mpc_traj                          : ARRAY[1..5, 1..8] OF REAL;    (* Predicted Control Trajectory *)
    grad_u                              : ARRAY[1..8] OF REAL;          (* Computed Projected Gradient Vector *)
    u_tentative                         : ARRAY[1..8] OF REAL;          (* Candidate Actuator Command *)
    rMpcAlphaStep                       : REAL := 0.085;                (* PGD Optimization Gradient Step Length *)
    rTotalCostFunctional                : REAL;                         (* Accumulated Quadratic Cost J *)
    
    (* ============================================================================================== *)
    (* 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) VOTING & FAULT ISOLATION STRUCTURES                       *)
    (* ============================================================================================== *)
    (* Residual Oxygen Concentration Voting (ZrO2 triplet) *)
    rO2_Delta_AB                        : REAL;     (* |Sensor A - Sensor B| [ppm] *)
    rO2_Delta_BC                        : REAL;     (* |Sensor B - Sensor C| [ppm] *)
    rO2_Delta_CA                        : REAL;     (* |Sensor C - Sensor A| [ppm] *)
    rO2_DiscrepancyLimit_ppm            : REAL := 8.0;      (* Tolerance Window for Channel Discrepancy [ppm] *)
    rO2_DiscrepancyTimer_s              : REAL := 0.0;      (* Cumulative Discrepancy Integrator [s] *)
    bO2_ChannelA_Valid                  : BOOL := TRUE;     (* Channel A Sensor Health Flag *)
    bO2_ChannelB_Valid                  : BOOL := TRUE;     (* Channel B Sensor Health Flag *)
    bO2_ChannelC_Valid                  : BOOL := TRUE;     (* Channel C Sensor Health Flag *)
    nO2_DegradedVotingMode              : INT := 3;         (* 3=2oo3, 2=1oo2 Average, 1=Single, 0=Fail-Safe *)
    
    (* Peak Reflow Zone 10 RTD Triplicate Voting *)
    rReflow_Delta_AB                    : REAL;     (* |RTD A - RTD B| [deg C] *)
    rReflow_Delta_BC                    : REAL;     (* |RTD B - RTD C| [deg C] *)
    rReflow_Delta_CA                    : REAL;     (* |RTD C - RTD A| [deg C] *)
    rReflow_DiscrepancyLimit_degC       : REAL := 3.5;      (* RTD Discrepancy Margin [deg C] *)
    rReflow_DiscrepancyTimer_s          : REAL := 0.0;      (* Reflow RTD Discrepancy Integrator [s] *)
    bReflow_ChannelA_Valid              : BOOL := TRUE;     (* Reflow RTD A Health Flag *)
    bReflow_ChannelB_Valid              : BOOL := TRUE;     (* Reflow RTD B Health Flag *)
    bReflow_ChannelC_Valid              : BOOL := TRUE;     (* Reflow RTD C Health Flag *)
    nReflow_DegradedVotingMode          : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* Vacuum Capacitance Diaphragm Gauge Triplicate Voting *)
    rVac_Delta_AB                       : REAL;     (* |Gauge A - Gauge B| [mbar] *)
    rVac_Delta_BC                       : REAL;     (* |Gauge B - Gauge C| [mbar] *)
    rVac_Delta_CA                       : REAL;     (* |Gauge C - Gauge A| [mbar] *)
    rVac_DiscrepancyLimit_mbar          : REAL := 2.5;      (* Vacuum Gauge Discrepancy Margin [mbar] *)
    rVac_DiscrepancyTimer_s             : REAL := 0.0;      (* Vacuum Gauge Discrepancy Integrator [s] *)
    bVac_ChannelA_Valid                 : BOOL := TRUE;     (* Vacuum Gauge A Health Flag *)
    bVac_ChannelB_Valid                 : BOOL := TRUE;     (* Vacuum Gauge B Health Flag *)
    bVac_ChannelC_Valid                 : BOOL := TRUE;     (* Vacuum Gauge C Health Flag *)
    nVac_DegradedVotingMode             : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* Lane 1 Mesh Belt Optical Tachometer Triplicate Voting *)
    rBelt_Delta_AB                      : REAL;     (* |Tacho A - Tacho B| [mm/min] *)
    rBelt_Delta_BC                      : REAL;     (* |Tacho B - Tacho C| [mm/min] *)
    rBelt_Delta_CA                      : REAL;     (* |Tacho C - Tacho A| [mm/min] *)
    rBelt_DiscrepancyLimit_mmpm         : REAL := 15.0;     (* Belt Speed Discrepancy Margin [mm/min] *)
    rBelt_DiscrepancyTimer_s            : REAL := 0.0;      (* Tachometer Discrepancy Integrator [s] *)
    bBelt_ChannelA_Valid                : BOOL := TRUE;     (* Tachometer Channel A Health Flag *)
    bBelt_ChannelB_Valid                : BOOL := TRUE;     (* Tachometer Channel B Health Flag *)
    bBelt_ChannelC_Valid                : BOOL := TRUE;     (* Tachometer Channel C Health Flag *)
    nBelt_DegradedVotingMode            : INT := 3;         (* 3=2oo3, 2=1oo2, 1=Single, 0=Fail-Safe *)
    
    (* ============================================================================================== *)
    (* 14-ZONE CASCADE PID HEATING/COOLING REGULATORS & FEEDFORWARD POWER ACCUMULATORS                *)
    (* ============================================================================================== *)
    rZone_PV_Array                      : ARRAY[1..14] OF REAL;     (* Normalized Zone PVs [deg C] *)
    rZone_SP_Array                      : ARRAY[1..14] OF REAL;     (* Normalized Zone SPs [deg C] *)
    rZone_Err_Array                     : ARRAY[1..14] OF REAL;     (* Tracking Error Array (SP - PV) [deg C] *)
    rZone_Err_Prev                      : ARRAY[1..14] OF REAL;     (* Prior Error for Derivative [deg C] *)
    rZone_Int_Array                     : ARRAY[1..14] OF REAL;     (* Anti-Windup Integral Accumulators *)
    rZone_Kp                            : ARRAY[1..14] OF REAL;     (* Proportional Gains [ % / deg C ] *)
    rZone_Ki                            : ARRAY[1..14] OF REAL;     (* Integral Gains [ % / (deg C * s) ] *)
    rZone_Kd                            : ARRAY[1..14] OF REAL;     (* Derivative Gains [ % * s / deg C ] *)
    rZone_PID_Raw                       : ARRAY[1..14] OF REAL;     (* Unclamped PID Output [%] *)
    rZone_Duty_Cmd                      : ARRAY[1..14] OF REAL;     (* Clamped Heating Duty Output [%] *)
    rZone_Blower_Cmd                    : ARRAY[1..14] OF REAL;     (* Convection Fan Frequency [Hz] *)
    
    (* Multi-Thermocouple Delta-T Thermal Shock Observers *)
    rZone_Temp_Prev                     : ARRAY[1..14] OF REAL;     (* Temperature at Previous Scan [deg C] *)
    rZone_RampRate_degCps               : ARRAY[1..14] OF REAL;     (* Observed Heating Rate dT/dt [deg C / s] *)
    rMaxHeatingRampLimit_degCps         : REAL := 2.0;              (* Max Safe Heating Gradient [deg C / s] *)
    rMaxCoolingRampLimit_degCps         : REAL := -3.5;             (* Max Safe Cooling Gradient [deg C / s] *)
    
    (* Dual-Lane Thermal Mass Infeed Feedforward Model *)
    rLane1_ThermalMassFlow_W            : REAL;     (* Lane 1 Board Heat Capacity Absorption [Watts] *)
    rLane2_ThermalMassFlow_W            : REAL;     (* Lane 2 Board Heat Capacity Absorption [Watts] *)
    rTotalInfeedFeedforwardPower_pct    : REAL;     (* Feedforward Duty Cycle Pre-compensation [%] *)
    rSpecificHeatCapacity_FR4_JgK       : REAL := 1.25;     (* Substrate Heat Capacity [J / (g * K)] *)
    rCopperMultiplier_L1                : REAL;     (* Layer Count Thermal Multiplier Lane 1 *)
    rCopperMultiplier_L2                : REAL;     (* Layer Count Thermal Multiplier Lane 2 *)
    
    (* ============================================================================================== *)
    (* INTEGRATED VACUUM VOIDING MODULE STATE VARIABLES                                              *)
    (* ============================================================================================== *)
    rVacChamberTarget_mbar              : REAL := 15.0;     (* Target Chamber Pressure [mbar] *)
    rVacChamberRamp_mbar                : REAL := 1013.0;   (* Dynamic Pressure Setpoint Trajectory [mbar] *)
    rVacDwellTimer_s                    : REAL := 0.0;      (* Deep Vacuum Dwell Hold Elapsed Timer [s] *)
    rVacCycleTimer_s                    : REAL := 0.0;      (* Total Vacuum Chamber Cycle Time [s] *)
    rVacPumpdownStartTime_s             : REAL := 0.0;      (* Evacuation Start Timestamp [s] *)
    rVacLeakRate_mbarps                 : REAL := 0.0;      (* Chamber Leak Rate Rate-of-Rise dP/dt [mbar/s] *)
    rVacPressurePrev_mbar               : REAL := 1013.0;   (* Prior Scan Pressure for Leak Analysis [mbar] *)
    bVacSequenceComplete                : BOOL := FALSE;    (* Vacuum Voiding Degas Completed Flag *)
    bVacGateFault_Inlet                 : BOOL := FALSE;    (* Inlet Sealing Gate Position Timeout *)
    bVacGateFault_Outlet                : BOOL := FALSE;    (* Outlet Sealing Gate Position Timeout *)
    rGateMoveTimer_s                    : REAL := 0.0;      (* Gate Pneumatic Actuation Timer [s] *)
    
    (* ============================================================================================== *)
    (* DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM) TIMERS & REGISTERS                          *)
    (* ============================================================================================== *)
    nFsmStateCurrent                    : INT := 0;         (* Active Operational Stage *)
    nFsmStateNext                       : INT := 0;         (* Scheduled Next Stage *)
    rFsmStateTimer_s                    : REAL := 0.0;      (* Active State Elapsed Timer [s] *)
    bFsmStateInit                       : BOOL := TRUE;     (* One-Scan State Initialization Pulse *)
    
    (* FSM Specific Stage Elapsed Timers *)
    rN2PurgeTimer_s                     : REAL := 0.0;      (* High-Volume N2 Blanket Flush Duration [s] *)
    rO2StabilizeTimer_s                 : REAL := 0.0;      (* Oxygen Loop Closed-Loop Trim Timer [s] *)
    rThermalSoakTimer_s                 : REAL := 0.0;      (* Thermal Soak Equilibrium Dwell Timer [s] *)
    rConveyorSyncTimer_s                : REAL := 0.0;      (* Dual Lane Speed Lock Timer [s] *)
    rCooldownExitTimer_s                : REAL := 0.0;      (* Post-Production Element Purge Cooldown [s] *)
    rEmergencyAbortTimer_s              : REAL := 0.0;      (* Emergency Evacuation Crawl Timer [s] *)
    
    (* ============================================================================================== *)
    (* ISA-18.2 ALARM MATRIX DATA STRUCTURES, LIMITS & DEADBANDS                                     *)
    (* ============================================================================================== *)
    rAlarmDeadband_degC                 : REAL := 2.5;      (* Temperature Alarm Clearance Hysteresis [deg C] *)
    rAlarmDeadband_ppm                  : REAL := 5.0;      (* Oxygen Alarm Clearance Hysteresis [ppm] *)
    rAlarmDeadband_mbar                 : REAL := 0.5;      (* Pressure Alarm Clearance Hysteresis [mbar] *)
    
    (* Latched Alarm Bits *)
    bAlarmTrip_Overtemp_HH              : BOOL := FALSE;    (* Zone Over-Temperature High-High Trip *)
    bAlarmTrip_Overtemp_H               : BOOL := FALSE;    (* Zone Over-Temperature High Warning *)
    bAlarmTrip_Undertemp_L              : BOOL := FALSE;    (* Zone Under-Temperature Low Warning *)
    bAlarmTrip_Undertemp_LL             : BOOL := FALSE;    (* Zone Under-Temperature Low-Low Trip *)
    bAlarmTrip_O2_High                  : BOOL := FALSE;    (* Oxygen Ingress High (> 35 ppm) *)
    bAlarmTrip_O2_HighHigh              : BOOL := FALSE;    (* Oxygen Ingress High-High (> 80 ppm) *)
    bAlarmTrip_N2_PressureLow           : BOOL := FALSE;    (* Bulk N2 Vaporizer Header Pressure Low (< 4.0 bar) *)
    bAlarmTrip_N2_PressureLowLow        : BOOL := FALSE;    (* Bulk N2 Vaporizer Header Depleted (< 2.5 bar) *)
    bAlarmTrip_VacPumpTimeout           : BOOL := FALSE;    (* Vacuum Evacuation Timeout (> 12.0 s to 15 mbar) *)
    bAlarmTrip_VacLeakRateHigh          : BOOL := FALSE;    (* Chamber Seal Degraded Leak Rate (> 2.0 mbar/s) *)
    bAlarmTrip_BeltSlip_L1              : BOOL := FALSE;    (* Lane 1 Mesh Belt Tachometer Deviation *)
    bAlarmTrip_BeltSlip_L2              : BOOL := FALSE;    (* Lane 2 Mesh Belt Speed Feedback Slip *)
    bAlarmTrip_ThermalShockRate         : BOOL := FALSE;    (* Board Surface Heating Gradient > +2.0 deg C/s *)
    bAlarmTrip_PlenumDeltaT             : BOOL := FALSE;    (* Upper/Lower Heating Cell Imbalance > 8.0 deg C *)
    bAlarmTrip_ExhaustBlocked           : BOOL := FALSE;    (* Oven Exhaust Vapor Extraction Failure *)
    
    (* Timers for Alarm Debouncing *)
    rAlarmDebounce_O2_s                 : REAL := 0.0;      (* Oxygen Alarm Filter Integrator [s] *)
    rAlarmDebounce_N2_s                 : REAL := 0.0;      (* N2 Supply Header Pressure Integrator [s] *)
    rAlarmDebounce_Belt_s               : REAL := 0.0;      (* Conveyor Slip Filter Integrator [s] *)
    
    (* General Computation & Loop Iterators *)
    i                                   : INT;              (* Primary Outer Loop Counter *)
    j                                   : INT;              (* Secondary Matrix Loop Counter *)
    k                                   : INT;              (* Horizon Prediction Step Counter *)
    z                                   : INT;              (* Zone Loop Index (1 to 14) *)
    rTempAccum                          : REAL;             (* Mathematical Vector Product Accumulator *)
    rTempMin                            : REAL;             (* Auxiliary Real Comparator *)
    rTempMax                            : REAL;             (* Auxiliary Real Comparator *)
    rTempDiff                           : REAL;             (* Auxiliary Real Difference *)
    rTAL_Counter_s                      : REAL := 0.0;      (* Real-Time Accumulator for Time Above Liquidus *)
    bInitializedFirstScan               : BOOL := FALSE;    (* First PLC Scan Cycle Initialized Latch *)
END_VAR
""")

    return "".join(parts)

if __name__ == "__main__":
    p1 = build_code()
    print(f"Header & Declarations length: {len(p1)} characters")
