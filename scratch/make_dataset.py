# scratch/make_dataset.py
import json
import uuid
import re
import os
import sys

def build_iec_code():
    code_parts = []
    
    # -------------------------------------------------------------------------
    # 1. HEADER & FUNCTION BLOCK DECLARATION
    # -------------------------------------------------------------------------
    code_parts.append("""FUNCTION_BLOCK FB_Energy_Hydrogen_PEM_Electrolyzer_SafetyBalance
(*
========================================================================================================================
  LUMINA AI CYBER-PHYSICAL SYSTEMS & ADVANCED INDUSTRIAL AUTOMATION ARCHITECTURE GROUP
  CRITICAL GREEN HYDROGEN & CLEAN ENERGY TRANSITION REFERENCE IMPLEMENTATION — SYNTHETIC DATASET ENGINE V7
  
  SYSTEM DESIGNATION : 20 MW MULTI-STACK PEM WATER ELECTROLYSIS FACILITY
  POWER MANAGEMENT  : 12/24-PULSE ACTIVE FRONT END THYRISTOR RECTIFIERS WITH RENEWABLE RAMP TRACKING (< 5%/s)
  FLUIDIC MATRIX    : CLOSED-LOOP ANODE DE-IONIZED WATER CIRCULATION WITH POLISHER RESIN RECIRCULATION
  SEPARATION SYSTEM : ANODE O2 & CATHODE H2 HIGH-PRESSURE GAS-LIQUID SEPARATORS (3-ELEMENT DRUM CASCADE)
  MEMBRANE BALANCE  : CATALYST-COATED MEMBRANE (CCM) DIFFERENTIAL PRESSURE BALANCING (< 200 mbar DELTA-P)
  GAS SAFETY MATRIX : TRACE O2-IN-H2 & H2-IN-O2 COMBUSTIBLE GAS ANALYZERS (2oo3 TMR TCD & TDLAS)
  SAFETY INTEGRITY  : IEC 61508 / IEC 61511 SIL-3 HIGH-INTEGRITY PRESSURE PROTECTION & EMERGENCY NITROGEN PURGE
  APPLICABLE NORMS   : ISO 22734 (HYDROGEN GENERATORS USING WATER ELECTROLYSIS PROCESS), NFPA 2 HYDROGEN TECHNOLOGIES,
                       CGA G-5.5 HYDROGEN VENT SYSTEMS, IEC 60079 EXPLOSIVE ATMOSPHERES (ATEX / HAZLOC ZONE 1 / 2),
                       ISA-18.2 / IEC 62682 MANAGEMENT OF INDUSTRIAL ALARMS, ASME SECTION VIII BOILER & PRESSURE VESSEL,
                       DIN EN 61010-1 SAFETY REQUIREMENTS FOR ELECTRICAL EQUIPMENT FOR MEASUREMENT AND CONTROL.
  AUTHOR             : 75+ YEARS VETERAN PRINCIPAL AUTOMATION FELLOW & CYBER-PHYSICAL SYSTEMS CHAIR
========================================================================================================================

  THEORETICAL & CYBER-PHYSICAL ELECTROCHEMICAL FOUNDATIONS:
  ----------------------------------------------------------------------------------------------------------------------
  1. ELECTROCHEMICAL THERMODYNAMICS & CELL VOLTAGE DECOMPOSITION:
     - In high-pressure Proton Exchange Membrane (PEM) water electrolysis, liquid demineralized water is electrochemically
       split into gaseous oxygen, hydrogen ions (protons), and electrons at the anode catalyst-coated membrane (CCM):
           Anode (Oxygen Evolution Reaction - OER)   : 2 H2O(l) -> O2(g) + 4 H+(aq) + 4 e-       (E0 = +1.229 V vs SHE)
           Cathode (Hydrogen Evolution Reaction - HER) : 4 H+(aq) + 4 e- -> 2 H2(g)                (E0 =  0.000 V vs SHE)
           Global Reaction                            : 2 H2O(l) -> 2 H2(g) + O2(g)               (Delta H0 = +285.83 kJ/mol)
     - The thermodynamic reversible open-circuit cell voltage E_rev(T, P) is governed by the Nernst equation:
           E_rev(T, P) = E0_rev(T) + [R * T / (2 * F)] * LN[ (a_H2 * a_O2^0.5) / a_H2O ]
       where:
           E0_rev(T) = 1.2291 - 0.0008456 * (T - 298.15) [V]
           R         = 8.314462 J/(mol*K) (Universal Gas Constant)
           F         = 96485.33 C/mol (Faraday Constant)
           a_i       = Fugacity activity of species i (p_i * gamma_i / P0)
     - Under load, the terminal individual cell voltage V_cell(j, T, P) deviates from E_rev due to irreversible kinetic,
       ohmic, and mass-transport overpotentials:
           V_cell = E_rev(T, P) + eta_act,anode(j, T) + eta_act,cathode(j, T) + eta_ohmic(j, T, lambda) + eta_mass(j, T)
     - Activation overpotentials eta_act are characterized by the non-linear Butler-Volmer equation:
           j = j0_anode * [ EXP( alpha_a * F * eta_act,a / (R * T) ) - EXP( -(1 - alpha_a) * F * eta_act,a / (R * T) ) ]
       Inverted via high-field hyperbolic arcsine approximation:
           eta_act,a = [ R * T / (alpha_a * F) ] * ARCSINH[ j / (2 * j0_a) ]
           eta_act,c = [ R * T / (alpha_c * F) ] * ARCSINH[ j / (2 * j0_c) ]
     - Ohmic overpotential eta_ohmic is dominated by proton transport resistance through the hydrated perfluorosulfonic
       acid (PFSA, e.g. Nafion 117 / Aquivion) ionomer membrane:
           eta_ohmic = j * ( R_membrane + R_hardware + R_interfacial )
           R_membrane = t_membrane / sigma_membrane(T, lambda_mem)
           sigma_membrane = (0.005139 * lambda_mem - 0.00326) * EXP[ 1268 * ( 1/303.15 - 1/T_Kelvin ) ] [S/cm]
       where lambda_mem is the membrane hydration state (water activity ratio: mol H2O / mol SO3- sulfonic acid groups).
     - Mass transport overpotential eta_mass accounts for boundary-layer liquid water depletion and two-phase gas bubble
       screening at high current densities approaching diffusion limiting current j_lim:
           eta_mass = - [ R * T / (2 * F) ] * LN( 1 - j / j_lim )

  2. FARADAIC EFFICIENCY, HYDROGEN PRODUCTION RATE & SPECIFIC ENERGY CONSUMPTION:
     - The net molar hydrogen generation rate is governed by Faraday's Law adjusted for parasitic current loss and gas
       crossover permeability:
           n_dot_H2 = eta_Faraday * [ N_cells * I_stack / (2 * F) ] [mol/s]
           V_dot_H2 = n_dot_H2 * V_molar_norm * 3600.0 [Nm3/h]
       where:
           V_molar_norm = 0.022414 m3/mol at normal reference conditions (0 deg C, 1.01325 bar)
           N_cells      = 3200 total active cells across 4 parallel/series 5 MW skid stacks
           eta_Faraday  = [ (j / j_ref)^2 / ( f_corr + (j / j_ref)^2 ) ] * (1.0 - beta_crossover)
     - Total 20 MW facility power consumption P_electrolyzer:
           P_electrolyzer = V_stack_total * I_stack_total + P_auxiliaries [kW]
           Specific Energy Consumption = P_electrolyzer / V_dot_H2 [kWh / Nm3 H2]
           Target High-Efficiency Range: 4.1 to 4.7 kWh / Nm3 H2 (50.5 to 44.0 kWh / kg H2).

  3. GAS-LIQUID SEPARATOR 3-ELEMENT CASCADE & MASS-MOMENTUM BALANCE:
     - The Anode O2 Separator and Cathode H2 Separator operate under dynamic two-phase bubbly-slug flow regimes.
     - Water is continually transported across the membrane to the cathode via electro-osmotic drag:
           n_dot_drag = n_drag_coeff(lambda_mem) * [ N_cells * I_stack / F ] [mol H2O/s]
           n_drag_coeff = 0.0029 * lambda_mem^2 + 0.05 * lambda_mem
     - Cathode separator liquid inventory accumulates from electro-osmotic carryover and condensation, requiring continuous
       3-element cascade modulation of the bottom drain valve:
           e_3elem = K_p_level * (L_actual - L_setpoint) + K_f_feed * (F_water_in - F_nominal) - K_d_drain * (F_water_drain - F_nominal)
     - Eliminates "shrink and swell" false level excursions caused by dissolved gas effervescence during rapid pressure
       or electrical ramp fluctuations.

  4. CATALYST-COATED MEMBRANE (CCM) DIFFERENTIAL PRESSURE BALANCING:
     - The ultra-thin (50 to 175 um) Nafion composite membrane separating the high-pressure cathode H2 header (up to 30 bar)
       and anode O2 header possesses finite mechanical tensile and burst strength.
     - Viscoelastic creep, hydration plasticization, and cyclic differential pressure Delta-P = P_H2 - P_O2 induce shear
       stress at the active area perimeter and microporous layer (MPL) interface.
     - Rupture criteria governed by Von Mises yield envelope:
           sigma_vm = SQRT( sigma_x^2 - sigma_x*sigma_y + sigma_y^2 + 3*tau_xy^2 ) <= sigma_yield(T, lambda_mem) / SF
     - Allowable operational envelope: |Delta-P| <= 150 mbar. Hard safety interlock trip: |Delta-P| >= 200 mbar.
     - Dual electro-pneumatic dome-loaded back-pressure control valves (PCV_H2 and PCV_O2) execute tight coupled
       pressure balancing with feedforward decoupling from rectifier current slew rate dI/dt.

  5. TRACE GAS CROSS-PERMEATION KINETICS & SAFETY INTEGRITY (O2-IN-H2 & H2-IN-O2):
     - Dissolved molecular gases permeate through the aqueous channels of the polymer membrane driven by partial pressure
       differentials according to Fickian diffusion and convective pressure filtration:
           J_O2_cross = [ D_O2(T, lambda) * S_O2(T) / t_mem ] * ( P_O2_anode - P_O2_cathode )
           J_H2_cross = [ D_H2(T, lambda) * S_H2(T) / t_mem ] * ( P_H2_cathode - P_H2_anode )
     - Gas crossover concentration in product hydrogen stream:
           C_O2_in_H2 = [ J_O2_cross * A_active_total / ( n_dot_H2_prod + J_O2_cross * A_active_total ) ] * 1.0E6 [ppm]
     - Lower Flammability Limit (LFL) for O2 in H2 is 4.0% vol (40,000 ppm).
       NFPA 2 and ISO 22734 mandate automatic safety rampdown at 25% LFL (10,000 ppm) and emergency SIL-3 trip at 37.5% LFL
       (15,000 ppm / 1.5% vol).
     - At low current densities (turndown < 15%), n_dot_H2 approaches zero while J_O2_cross remains roughly constant,
       causing exponential rise in C_O2_in_H2. Active turndown clamping and nitrogen ballast dilution are strictly required.

  6. 8-STATE CYBER-PHYSICAL DISCRETE STATE-SPACE FORMULATION (Ts = 10 ms):
     - State Vector x[k] in R^8:
         x[1] : Cell Overpotential / Polarization Variation Delta_eta [V]
         x[2] : Volumetric Hydrogen Production Rate Variation Delta_V_dot_H2 [Nm3/h]
         x[3] : Polymer Membrane Hydration Water Activity Delta_lambda [-]
         x[4] : Stack Coolant Outlet Bulk Temperature Variation Delta_T_stack [deg C]
         x[5] : Cathode Gas-Liquid Separator Vessel Liquid Level Variation Delta_L_sep [%]
         x[6] : Anode-to-Cathode Membrane Differential Pressure Delta_P_diff [mbar]
         x[7] : Trace Oxygen-in-Hydrogen Gas Concentration Delta_C_O2_in_H2 [ppm]
         x[8] : Stack DC Current Density Variation Delta_j_DC [A/cm2]
     - Control Input Vector u[k] in R^8:
         u[1] : DC Rectifier Current Setpoint Command I_cmd [kA]
         u[2] : Anode DI Water Recirculation Pump Speed Command omega_pump [%]
         u[3] : Coolant Heat Exchanger 3-Way Modulating Bypass Valve Cmd u_cool [%]
         u[4] : Cathode Separator Condensate Drain Valve Cmd u_drain [%]
         u[5] : Cathode H2 High-Pressure Back-Pressure Control Valve Cmd u_PCV_H2 [%]
         u[6] : Anode O2 High-Pressure Back-Pressure Control Valve Cmd u_PCV_O2 [%]
         u[7] : Mixed-Bed Ion Exchange Polisher Loop Throttle Valve Cmd u_polish [%]
         u[8] : Nitrogen Inerting Safety Purge Header Injection Valve Cmd u_N2 [%]
     - Disturbance Vector d[k] in R^4:
         d[1] : Renewable Grid Power Available Ramp Request P_grid_avail [MW]
         d[2] : Demineralized Feedwater Supply Bulk Temperature T_DI_feed [deg C]
         d[3] : Export Hydrogen Transmission Pipeline Back-Pressure P_export_pipe [bar]
         d[4] : Secondary Heat Exchanger Cooling Water Supply Temp T_cool_inlet [deg C]
     - System Evolution:
         x[k+1] = A * x[k] + B * u[k] + E_dist * d[k]
         y[k]   = C * x[k] + D * u[k]
         x_hat[k+1] = x[k+1] + L_obs * ( y_meas[k] - y_est[k] )

  7. RECEDING-HORIZON MODEL PREDICTIVE CONTROL WITH PROJECTED GRADIENT DESCENT:
     - Multi-objective quadratic objective functional:
         J = SUM(k=0..Np-1) [ (x[k] - x_ref)^T * Q * (x[k] - x_ref) + (u[k] - u_ref)^T * R * (u[k] - u_ref)
                            + Delta_u[k]^T * S * Delta_u[k] ] + (x[Np] - x_ref)^T * P * (x[Np] - x_ref)
     - Solved in real-time within the 10 ms PLC deterministic task cycle using Projected Gradient Descent (PGD) with
       box actuator clamping and slew rate saturation limiters.

  8. 2oo3 TRIPLE MODULAR REDUNDANCY VOTING & MARKOVIAN SENSOR DEGRADATION:
     - Critical instruments (Stack Voltage, Stack Current, Cathode Level, Anode Level, Membrane Delta-P, Trace O2-in-H2,
       Trace H2-in-O2, Coolant Temperature, DI Resistivity) deployed in triplicate A/B/C channels.
     - Discrepancy timers detect out-of-tolerance sensor drift, frozen signals, or high-frequency jitter.
     - Graceful degradation: 2oo3 Normal Voting -> 1oo2 Average/Conservative -> 1oo1 Emergency Run -> Fail-Safe Trip.

  9. DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE:
     - Stage 0 : STATE_OFFLINE_DEENERGIZED              - Rectifier de-energized, valves fail-safe closed
     - Stage 1 : STATE_NITROGEN_INERTING_PURGE          - Inerting gas purge until O2 < 0.2% vol in all lines
     - Stage 2 : STATE_WATER_CIRCULATION_RESISTIVITY_QUAL- DI pumps running, polisher active, resistivity > 18 MOhm-cm
     - Stage 3 : STATE_SYSTEM_PREPRESSURIZATION         - N2/H2 pad pressurization to 5 bar, DP balancing active
     - Stage 4 : STATE_STACK_CONDITIONING_POLARIZATION  - Low current trickle (5-10%), membrane hydration, CVM check
     - Stage 5 : STATE_WARMUP_RAMP_HEATING              - Current ramp at 2%/s, coolant bypass closed, warming to 60 C
     - Stage 6 : STATE_RENEWABLE_RAMP_FOLLOWING         - Dynamic tracking of fluctuating wind/solar MW setpoints
     - Stage 7 : STATE_STEADY_STATE_PEAK_PRODUCTION     - Rated 20 MW generation at 30 bar(g), full 3-element cascade
     - Stage 8 : STATE_TURNDOWN_LOW_POWER_RESERVE       - Minimum stable load 10-15%, anti-crossover dilution active
     - Stage 9 : STATE_MEMBRANE_DP_STABILIZATION        - Transient pressure lock if |Delta-P| exceeds 120 mbar deadband
     - Stage 10: STATE_CONTROLLED_RAMPDOWN_SHUTDOWN     - Orderly current rampdown at 5%/s to 0 kA, venting product gas
     - Stage 11: STATE_STACK_DEPOLARIZATION_COOLDOWN    - Active depolarization resistor, coolant circulation to 35 C
     - Stage 12: STATE_POST_SHUTDOWN_N2_SAFETY_PURGE    - Automatic N2 flush displacing residual combustible gas
     - Stage 13: STATE_EMERGENCY_FAST_TRIP_VENT         - SIL-3 fast trip: rectifier breaker trip, blowdown venting
*)
""")

    # -------------------------------------------------------------------------
    # 2. VAR_INPUT BLOCK
    # -------------------------------------------------------------------------
    code_parts.append("""VAR_INPUT
    (* === MASTER SYSTEM COMMANDS & DISCRETE SUPERVISORY SIGNALS === *)
    bSystemEnable                 : BOOL;   (* System Master Run Enable Command [-] *)
    bEmergencyStop                : BOOL;   (* Hardwired Emergency Stop Pushbutton Circuit (Active Low NC) [-] *)
    bAlarmReset                   : BOOL;   (* Operator Master Alarm Acknowledge and Reset Pulse [-] *)
    bManualOverride               : BOOL;   (* Engineering Manual Valve & Rectifier Override Mode [-] *)
    bAutoStart                    : BOOL;   (* Auto Sequence Start Command [-] *)
    bControlledStop               : BOOL;   (* Controlled Normal Rampdown Shutdown Command [-] *)
    bNitrogenPurgePermissive      : BOOL;   (* Site Nitrogen Supply Pressure & Purity Permissive Valid [-] *)
    bCoolingWaterAvailable        : BOOL;   (* Secondary Utility Cooling Water Circulation Ready [-] *)
    bVentFlareHeaderReady         : BOOL;   (* Atmospheric Hydrogen Flare / Deox Vent Header Ready [-] *)
    bDownstreamConsumerReady      : BOOL;   (* Downstream Hydrogen Compression / Pipeline Intake Ready [-] *)

    (* === ANALOG PROCESS DEMANDS & SETPOINTS === *)
    rRenewablePowerAvailable      : REAL;   (* Grid / Solar / Wind Available Power Setpoint [MW] *)
    rHydrogenDemandFlow           : REAL;   (* Downstream Customer Hydrogen Production Demand [Nm3/h] *)
    rTargetCathodePressure        : REAL;   (* Cathode Header Target Operating Pressure [bar] *)
    rTargetStackTemperature       : REAL;   (* Stack Coolant Target Operating Temperature [deg C] *)
    rDownstreamPipelinePressure   : REAL;   (* Export Hydrogen Pipeline Header Pressure [bar] *)
    rCoolingWaterSupplyTemp       : REAL;   (* Secondary Heat Exchanger Cooling Water Inlet Temp [deg C] *)
    rRawWaterFeedPressure         : REAL;   (* Upstream Demineralized Feedwater Supply Pressure [bar] *)
    rRawWaterFeedTemp             : REAL;   (* Demineralized Water Storage Tank Temperature [deg C] *)

    (* === 2oo3 TMR SENSOR CHANNEL A TRIPLICATE INPUTS === *)
    rStackVoltage_ChA             : REAL;   (* Total Stack Terminal Voltage Transmitter Channel A [V] *)
    rStackCurrent_ChA             : REAL;   (* DC Rectifier Current Shunt/Hall Sensor Channel A [kA] *)
    rCathodeLevel_ChA             : REAL;   (* H2 Cathode Separator Vessel Liquid Level Channel A [%] *)
    rAnodeLevel_ChA               : REAL;   (* O2 Anode Separator Vessel Liquid Level Channel A [%] *)
    rDiffPressure_ChA             : REAL;   (* Anode-Cathode Membrane Differential Pressure Channel A [mbar] *)
    rO2_in_H2_ChA                 : REAL;   (* Trace Oxygen in Hydrogen Stream Analyzer Channel A [ppm] *)
    rH2_in_O2_ChA                 : REAL;   (* Trace Hydrogen in Oxygen Stream Analyzer Channel A [ppm] *)
    rStackTemp_ChA                : REAL;   (* Stack Core Coolant Outlet RTD Sensor Channel A [deg C] *)
    rDI_Resistivity_ChA           : REAL;   (* Demineralized Water Resistivity Probe Channel A [MOhm-cm] *)

    (* === 2oo3 TMR SENSOR CHANNEL B TRIPLICATE INPUTS === *)
    rStackVoltage_ChB             : REAL;   (* Total Stack Terminal Voltage Transmitter Channel B [V] *)
    rStackCurrent_ChB             : REAL;   (* DC Rectifier Current Shunt/Hall Sensor Channel B [kA] *)
    rCathodeLevel_ChB             : REAL;   (* H2 Cathode Separator Vessel Liquid Level Channel B [%] *)
    rAnodeLevel_ChB               : REAL;   (* O2 Anode Separator Vessel Liquid Level Channel B [%] *)
    rDiffPressure_ChB             : REAL;   (* Anode-Cathode Membrane Differential Pressure Channel B [mbar] *)
    rO2_in_H2_ChB                 : REAL;   (* Trace Oxygen in Hydrogen Stream Analyzer Channel B [ppm] *)
    rH2_in_O2_ChB                 : REAL;   (* Trace Hydrogen in Oxygen Stream Analyzer Channel B [ppm] *)
    rStackTemp_ChB                : REAL;   (* Stack Core Coolant Outlet RTD Sensor Channel B [deg C] *)
    rDI_Resistivity_ChB           : REAL;   (* Demineralized Water Resistivity Probe Channel B [MOhm-cm] *)

    (* === 2oo3 TMR SENSOR CHANNEL C TRIPLICATE INPUTS === *)
    rStackVoltage_ChC             : REAL;   (* Total Stack Terminal Voltage Transmitter Channel C [V] *)
    rStackCurrent_ChC             : REAL;   (* DC Rectifier Current Shunt/Hall Sensor Channel C [kA] *)
    rCathodeLevel_ChC             : REAL;   (* H2 Cathode Separator Vessel Liquid Level Channel C [%] *)
    rAnodeLevel_ChC               : REAL;   (* O2 Anode Separator Vessel Liquid Level Channel C [%] *)
    rDiffPressure_ChC             : REAL;   (* Anode-Cathode Membrane Differential Pressure Channel C [mbar] *)
    rO2_in_H2_ChC                 : REAL;   (* Trace Oxygen in Hydrogen Stream Analyzer Channel C [ppm] *)
    rH2_in_O2_ChC                 : REAL;   (* Trace Hydrogen in Oxygen Stream Analyzer Channel C [ppm] *)
    rStackTemp_ChC                : REAL;   (* Stack Core Coolant Outlet RTD Sensor Channel C [deg C] *)
    rDI_Resistivity_ChC           : REAL;   (* Demineralized Water Resistivity Probe Channel C [MOhm-cm] *)

    (* === CELL VOLTAGE MONITORING (CVM) & AUXILIARY TRANSMITTERS === *)
    rMaxCellVoltageCVM            : REAL;   (* Cell Voltage Monitoring System Max Observed Cell Voltage [V] *)
    rMinCellVoltageCVM            : REAL;   (* Cell Voltage Monitoring System Min Observed Cell Voltage [V] *)
    rAvgCellVoltageCVM            : REAL;   (* Cell Voltage Monitoring System Average Cell Voltage [V] *)
    rN2SupplyPressure             : REAL;   (* Nitrogen Inerting Header Supply Header Pressure [bar] *)
    rCathodeGasPressure           : REAL;   (* Hydrogen Separator Head Absolute Pressure [bar] *)
    rAnodeGasPressure             : REAL;   (* Oxygen Separator Head Absolute Pressure [bar] *)
    rWaterCirculationFlow         : REAL;   (* Anode Loop De-ionized Water Recirculation Mass Flow [m3/h] *)
    rCathodeDrainFlow             : REAL;   (* Cathode Gas-Liquid Separator Condensate Drain Flow [m3/h] *)
    rAmbientEnclosureTemp         : REAL;   (* Electrolyzer Skid Ambient Blast Enclosure Temperature [deg C] *)
    rRectifierTransformerTemp     : REAL;   (* 24-Pulse Rectifier Transformer Winding Hotspot Temp [deg C] *)
    bRectifierThyristorHealth     : BOOL;   (* Rectifier SCR/IGBT Active Front End Health OK Flag [-] *)
    bCathodeDrainPumpRunning      : BOOL;   (* Cathode Condensate Return Pump Auxiliary Contact [-] *)
    bAnodeRecircPumpRunning       : BOOL;   (* Anode Loop High-Flow DI Circulation Pump Running [-] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 3. VAR_OUTPUT BLOCK
    # -------------------------------------------------------------------------
    code_parts.append("""VAR_OUTPUT
    (* === MASTER STATUS & DISCRETE OPERATIONAL FLAGS === *)
    bSystemRunning                : BOOL;   (* Electrolyzer Facility In Active Operation State [-] *)
    bSystemTripped                : BOOL;   (* Master Safety Shutdown / Emergency Trip Latched [-] *)
    bWarningActive                : BOOL;   (* Non-Trip Preventive Maintenance Warning Flag [-] *)
    bProductionReady              : BOOL;   (* Stack Ready For Full Hydrogen Production Loading [-] *)
    bNitrogenPurging              : BOOL;   (* System Headers Under Nitrogen Inerting Flush [-] *)
    bDepolarizationActive         : BOOL;   (* Stack Depolarization Resistor Contactor Closed [-] *)
    bStandbyReserveActive         : BOOL;   (* Stack Maintaining Low-Power Hot Standby Reserve [-] *)
    nOperatingState               : INT;    (* Active Finite State Machine Operational Stage (0-13) [-] *)

    (* === ACTUATOR COMMAND SETPOINTS & MODULATING SIGNALS === *)
    rRectifierCurrentCmd          : REAL;   (* DC Thyristor Rectifier Current Setpoint Command [kA] *)
    rCirculationPumpSpeedCmd      : REAL;   (* Anode DI Circulation Pump VFD Speed Setpoint [%] *)
    rCoolantBypassValveCmd        : REAL;   (* 3-Way Heat Exchanger Modulating Bypass Valve Cmd [%] *)
    rCathodeDrainValveCmd         : REAL;   (* Cathode Separator Water Drain Modulating Valve Cmd [%] *)
    rCathodePCV_Cmd               : REAL;   (* Cathode H2 Back-Pressure Control Valve Setpoint [%] *)
    rAnodePCV_Cmd                 : REAL;   (* Anode O2 Back-Pressure Control Valve Setpoint [%] *)
    rPolisherBypassValveCmd       : REAL;   (* Mixed-Bed Ion Exchange Polisher Loop Throttle Valve [%] *)
    rN2PurgeValveCmd              : REAL;   (* Nitrogen Inerting Purge Header Solenoid/Modulating Valve [%] *)
    rFastVentValveCmd_H2          : REAL;   (* Emergency Hydrogen Fast Depressurization Vent Valve [%] *)
    rFastVentValveCmd_O2          : REAL;   (* Emergency Oxygen Fast Depressurization Vent Valve [%] *)

    (* === FIRST-PRINCIPLES CALCULATED METRICS & STATE ESTIMATES === *)
    rCurrentDensityActual         : REAL;   (* Estimated Stack Active Current Density [A/cm2] *)
    rHydrogenFlowActual           : REAL;   (* Real-Time Hydrogen Volumetric Production Rate [Nm3/h] *)
    rOxygenFlowActual             : REAL;   (* Real-Time Oxygen Volumetric Production Rate [Nm3/h] *)
    rFaradaicEfficiency           : REAL;   (* Calculated Stack Faradaic Current Efficiency [%] *)
    rSpecificEnergyConsumption    : REAL;   (* Specific Electrical Energy Consumption [kWh/Nm3] *)
    rElectrochemicalEfficiency    : REAL;   (* Higher Heating Value (HHV) Thermal Stack Efficiency [%] *)
    rMembraneHydrationEst         : REAL;   (* State Observer Estimated Membrane Water Activity [-] *)
    rCellVoltageMargin            : REAL;   (* CVM Max Allowable Margin Before Degradation Limit [V] *)

    (* === 2oo3 TMR VOTED PROCESS VALUES === *)
    rVotedDifferentialPressure   : REAL;   (* 2oo3 TMR Voted Membrane Differential Pressure [mbar] *)
    rVotedO2_in_H2                : REAL;   (* 2oo3 TMR Voted Oxygen-in-Hydrogen Concentration [ppm] *)
    rVotedH2_in_O2                : REAL;   (* 2oo3 TMR Voted Hydrogen-in-Oxygen Concentration [ppm] *)
    rVotedCathodeLevel            : REAL;   (* 2oo3 TMR Voted Cathode Separator Liquid Level [%] *)
    rVotedAnodeLevel              : REAL;   (* 2oo3 TMR Voted Anode Separator Liquid Level [%] *)
    rVotedStackTemp               : REAL;   (* 2oo3 TMR Voted Stack Core Coolant Temperature [deg C] *)
    rVotedStackVoltage            : REAL;   (* 2oo3 TMR Voted Stack Terminal Total Voltage [V] *)
    rVotedStackCurrent            : REAL;   (* 2oo3 TMR Voted Stack DC Rectifier Current [kA] *)
    rVotedResistivity             : REAL;   (* 2oo3 TMR Voted DI Water Loop Resistivity [MOhm-cm] *)

    (* === 32-BIT BIT-PACKED STATUS & DIAGNOSTIC WORDS === *)
    dwStatusWord                  : DWORD;  (* 32-Bit Bit-Packed Facility Operational Status Word [-] *)
    dwFaultWord                   : DWORD;  (* 32-Bit Bit-Packed Facility Master Trip Fault Word [-] *)
    dwWarningWord                 : DWORD;  (* 32-Bit Bit-Packed Facility Warning and Advisory Word [-] *)
    dwSensorHealthWord            : DWORD;  (* 32-Bit Bit-Packed 2oo3 TMR Sensor Health & Degradation Word [-] *)
END_VAR
""")

    # -------------------------------------------------------------------------
    # 4. VAR BLOCK (INTERNAL MATRICES, VARIABLES, ALARMS, PID, MPC)
    # -------------------------------------------------------------------------
    code_parts.append("""VAR
    (* === CONSTANTS FOR FIRST-PRINCIPLES CYBER-PHYSICAL MODELING === *)
    c_R_gas                       : REAL := 8.314462;       (* Universal Gas Constant [J/(mol*K)] *)
    c_F_faraday                   : REAL := 96485.33;       (* Faraday Constant [C/mol] *)
    c_V_mol_norm                  : REAL := 0.022414;       (* Normal Molar Gas Volume at STP [m3/mol] *)
    c_N_cells                     : REAL := 3200.0;         (* Total Active Electrochemical Cells across 4 Skids [-] *)
    c_A_cell_cm2                  : REAL := 2000.0;         (* Active Geometric Membrane Area per Cell [cm2] *)
    c_Ts_sec                      : REAL := 0.010;          (* Deterministic PLC Scan Sample Time Ts = 10 ms [s] *)
    c_HHV_H2_MJ_kg                : REAL := 141.86;         (* Hydrogen Higher Heating Value [MJ/kg] *)
    c_rho_H2_norm                 : REAL := 0.08988;        (* Hydrogen Normal Density at STP [kg/Nm3] *)

    (* === DISCRETE STATE-SPACE MODEL MATRICES (8x8, 8x8, 8x8, 8x8, 8x4) === *)
    A                             : ARRAY[1..8, 1..8] OF REAL; (* Discrete State Transition Matrix *)
    B                             : ARRAY[1..8, 1..8] OF REAL; (* Discrete Control Input Matrix *)
    C_mat                         : ARRAY[1..8, 1..8] OF REAL; (* Discrete Measurement Output Matrix *)
    D_mat                         : ARRAY[1..8, 1..8] OF REAL; (* Direct Feedthrough Matrix *)
    E_dist                        : ARRAY[1..8, 1..4] OF REAL; (* Disturbance Coupling Matrix *)
    L_obs                         : ARRAY[1..8] OF REAL;       (* Luenberger State Observer Gain Vector *)

    (* === INTERNAL STATE, ESTIMATE, PREDICTION & CONTROL VECTORS === *)
    x_state                       : ARRAY[1..8] OF REAL;       (* Estimated State Vector x[k] *)
    x_pred                        : ARRAY[1..8] OF REAL;       (* One-Step Ahead Predicted State x[k+1|k] *)
    x_ref                         : ARRAY[1..8] OF REAL;       (* Reference Setpoint State Vector *)
    y_meas                        : ARRAY[1..8] OF REAL;       (* Measured Process Output Vector *)
    y_est                         : ARRAY[1..8] OF REAL;       (* Estimated Output Vector *)
    u_cmd                         : ARRAY[1..8] OF REAL;       (* Current Optimization Control Vector u[k] *)
    u_prev                        : ARRAY[1..8] OF REAL;       (* Previous Control Actuator Vector u[k-1] *)
    u_min                         : ARRAY[1..8] OF REAL;       (* Physical Lower Box Actuator Limits *)
    u_max                         : ARRAY[1..8] OF REAL;       (* Physical Upper Box Actuator Limits *)
    delta_u_max                   : ARRAY[1..8] OF REAL;       (* Maximum Allowable Slew Rate per 10 ms *)
    d_dist                        : ARRAY[1..4] OF REAL;       (* External Disturbance Vector *)

    (* === MPC QUADRATIC WEIGHT MATRICES & OPTIMIZATION STORAGE === *)
    Q_weight                      : ARRAY[1..8] OF REAL;       (* State Tracking Penalty Diagonal *)
    R_weight                      : ARRAY[1..8] OF REAL;       (* Control Effort Penalty Diagonal *)
    S_weight                      : ARRAY[1..8] OF REAL;       (* Control Rate Slew Penalty Diagonal *)
    P_weight                      : ARRAY[1..8] OF REAL;       (* Terminal State Penalty Diagonal *)
    grad_J                        : ARRAY[1..8] OF REAL;       (* Projected Gradient Descent Gradient Vector *)
    u_trial                       : ARRAY[1..8] OF REAL;       (* PGD Iteration Trial Vector *)
    rAlphaPGD                     : REAL := 0.035;             (* PGD Fixed Step Size Parameter *)
    bStateMatricesInitialized     : BOOL := FALSE;             (* Cold-Start Matrix Initialization Sentinel *)

    (* === 2oo3 TMR VOTING VARIABLES FOR 9 CRITICAL CHANNELS === *)
    (* Channel 1: Stack Total Voltage *)
    rTol_StackVoltage             : REAL := 25.0;              (* Channel Discrepancy Tolerance [V] *)
    nDiscrepancyTimer_StackVolt   : INT := 0;                  (* Discrepancy Timer [cycles] *)
    bDiscrepancyTrip_StackVolt    : BOOL := FALSE;             (* Discrepancy Fault Latched *)
    bHealthyA_StackVolt           : BOOL := TRUE;
    bHealthyB_StackVolt           : BOOL := TRUE;
    bHealthyC_StackVolt           : BOOL := TRUE;
    nDegradedMode_StackVolt       : INT := 3;                  (* 3: 2oo3, 2: 1oo2, 1: 1oo1, 0: Fault *)

    (* Channel 2: Stack DC Current *)
    rTol_StackCurrent             : REAL := 0.35;              (* Channel Discrepancy Tolerance [kA] *)
    nDiscrepancyTimer_StackCurr   : INT := 0;
    bDiscrepancyTrip_StackCurr    : BOOL := FALSE;
    bHealthyA_StackCurr           : BOOL := TRUE;
    bHealthyB_StackCurr           : BOOL := TRUE;
    bHealthyC_StackCurr           : BOOL := TRUE;
    nDegradedMode_StackCurr       : INT := 3;

    (* Channel 3: Cathode Separator Liquid Level *)
    rTol_CathodeLevel             : REAL := 5.0;               (* Channel Discrepancy Tolerance [%] *)
    nDiscrepancyTimer_CathLevel   : INT := 0;
    bDiscrepancyTrip_CathLevel    : BOOL := FALSE;
    bHealthyA_CathLevel           : BOOL := TRUE;
    bHealthyB_CathLevel           : BOOL := TRUE;
    bHealthyC_CathLevel           : BOOL := TRUE;
    nDegradedMode_CathLevel       : INT := 3;

    (* Channel 4: Anode Separator Liquid Level *)
    rTol_AnodeLevel               : REAL := 5.0;               (* Channel Discrepancy Tolerance [%] *)
    nDiscrepancyTimer_AnodeLevel  : INT := 0;
    bDiscrepancyTrip_AnodeLevel   : BOOL := FALSE;
    bHealthyA_AnodeLevel          : BOOL := TRUE;
    bHealthyB_AnodeLevel          : BOOL := TRUE;
    bHealthyC_AnodeLevel          : BOOL := TRUE;
    nDegradedMode_AnodeLevel      : INT := 3;

    (* Channel 5: Membrane Differential Pressure *)
    rTol_DiffPressure             : REAL := 15.0;              (* Channel Discrepancy Tolerance [mbar] *)
    nDiscrepancyTimer_DiffPress   : INT := 0;
    bDiscrepancyTrip_DiffPress    : BOOL := FALSE;
    bHealthyA_DiffPress           : BOOL := TRUE;
    bHealthyB_DiffPress           : BOOL := TRUE;
    bHealthyC_DiffPress           : BOOL := TRUE;
    nDegradedMode_DiffPress       : INT := 3;

    (* Channel 6: Trace Oxygen in Hydrogen (O2-in-H2) *)
    rTol_O2_in_H2                 : REAL := 450.0;             (* Channel Discrepancy Tolerance [ppm] *)
    nDiscrepancyTimer_O2_in_H2    : INT := 0;
    bDiscrepancyTrip_O2_in_H2     : BOOL := FALSE;
    bHealthyA_O2_in_H2            : BOOL := TRUE;
    bHealthyB_O2_in_H2            : BOOL := TRUE;
    bHealthyC_O2_in_H2            : BOOL := TRUE;
    nDegradedMode_O2_in_H2        : INT := 3;

    (* Channel 7: Trace Hydrogen in Oxygen (H2-in-O2) *)
    rTol_H2_in_O2                 : REAL := 500.0;             (* Channel Discrepancy Tolerance [ppm] *)
    nDiscrepancyTimer_H2_in_O2    : INT := 0;
    bDiscrepancyTrip_H2_in_O2     : BOOL := FALSE;
    bHealthyA_H2_in_O2            : BOOL := TRUE;
    bHealthyB_H2_in_O2            : BOOL := TRUE;
    bHealthyC_H2_in_O2            : BOOL := TRUE;
    nDegradedMode_H2_in_O2        : INT := 3;

    (* Channel 8: Stack Coolant Outlet Temperature *)
    rTol_StackTemp                : REAL := 2.5;               (* Channel Discrepancy Tolerance [deg C] *)
    nDiscrepancyTimer_StackTemp   : INT := 0;
    bDiscrepancyTrip_StackTemp    : BOOL := FALSE;
    bHealthyA_StackTemp           : BOOL := TRUE;
    bHealthyB_StackTemp           : BOOL := TRUE;
    bHealthyC_StackTemp           : BOOL := TRUE;
    nDegradedMode_StackTemp       : INT := 3;

    (* Channel 9: Demineralized Water Resistivity *)
    rTol_DI_Resistivity           : REAL := 1.2;               (* Channel Discrepancy Tolerance [MOhm-cm] *)
    nDiscrepancyTimer_DI_Resist   : INT := 0;
    bDiscrepancyTrip_DI_Resist    : BOOL := FALSE;
    bHealthyA_DI_Resist           : BOOL := TRUE;
    bHealthyB_DI_Resist           : BOOL := TRUE;
    bHealthyC_DI_Resist           : BOOL := TRUE;
    nDegradedMode_DI_Resist       : INT := 3;

    (* Rate of Change Previous Storage *)
    rPrev_DiffPressure            : REAL := 0.0;
    rRoC_DiffPressure             : REAL := 0.0;
    rPrev_O2_in_H2                : REAL := 0.0;
    rRoC_O2_in_H2                 : REAL := 0.0;
    rPrev_H2_in_O2                : REAL := 0.0;
    rRoC_H2_in_O2                 : REAL := 0.0;

    (* === 3-ELEMENT SEPARATOR LEVEL CASCADE CONTROLLERS === *)
    rCathLevel_Integral           : REAL := 0.0;
    rCathLevel_PrevError          : REAL := 0.0;
    rAnodeLevel_Integral          : REAL := 0.0;
    rAnodeLevel_PrevError         : REAL := 0.0;

    (* === FINITE STATE MACHINE (FSM) TIMERS & SEQUENCING === *)
    nFSM_State                    : INT := 0;                  (* Operational State Identifier *)
    nFSM_PrevState                : INT := 0;                  (* Previous Scan Operational State *)
    nStateScanTimer               : DINT := 0;                 (* State In-Duration Scan Step Counter *)
    nPurgeStep                    : INT := 0;                  (* Sub-step Counter for Nitrogen Flushing *)
    nPolarizationStep             : INT := 0;                  (* Sub-step Counter for Stack Polarization *)
    rWarmupRampSetpoint           : REAL := 0.0;               (* Dynamic Current Ramp Target during Warmup *)
    rTargetPressureRamp           : REAL := 1.0;               (* Dynamic Pressure Pad Ramp Setpoint *)
    bMembraneDP_Locked            : BOOL := FALSE;             (* Transient Differential Pressure Freeze Flag *)

    (* === ISA-18.2 MULTI-TIER ALARM TRIP THRESHOLDS & DEADBANDS === *)
    (* Differential Pressure Alarms *)
    rTrip_DP_HH                   : REAL := 200.0;             (* High-High Trip Threshold [mbar] *)
    rTrip_DP_H                    : REAL := 120.0;             (* High Warning Threshold [mbar] *)
    rTrip_DP_L                    : REAL := -120.0;            (* Low Warning Threshold [mbar] *)
    rTrip_DP_LL                   : REAL := -200.0;            (* Low-Low Trip Threshold [mbar] *)
    rDeadband_DP                  : REAL := 15.0;              (* Alarm Clear Deadband [mbar] *)
    bAlarm_DP_HH                  : BOOL := FALSE;
    bAlarm_DP_H                   : BOOL := FALSE;
    bAlarm_DP_L                   : BOOL := FALSE;
    bAlarm_DP_LL                  : BOOL := FALSE;

    (* O2-in-H2 Combustible Gas Alarms *)
    rTrip_O2inH2_HH               : REAL := 15000.0;           (* High-High SIL-3 Fast Trip [ppm] *)
    rTrip_O2inH2_H                : REAL := 8000.0;            (* High Turndown Warning [ppm] *)
    rTrip_O2inH2_RoC              : REAL := 300.0;             (* High Rate-of-Change Trip [ppm/s] *)
    rDeadband_O2inH2              : REAL := 500.0;             (* Clear Deadband [ppm] *)
    bAlarm_O2inH2_HH              : BOOL := FALSE;
    bAlarm_O2inH2_H               : BOOL := FALSE;
    bAlarm_O2inH2_RoC             : BOOL := FALSE;

    (* H2-in-O2 Combustible Gas Alarms *)
    rTrip_H2inO2_HH               : REAL := 15000.0;           (* High-High SIL-3 Fast Trip [ppm] *)
    rTrip_H2inO2_H                : REAL := 8000.0;            (* High Warning Threshold [ppm] *)
    rTrip_H2inO2_RoC              : REAL := 300.0;             (* High Rate-of-Change Trip [ppm/s] *)
    rDeadband_H2inO2              : REAL := 500.0;             (* Clear Deadband [ppm] *)
    bAlarm_H2inO2_HH              : BOOL := FALSE;
    bAlarm_H2inO2_H               : BOOL := FALSE;
    bAlarm_H2inO2_RoC             : BOOL := FALSE;

    (* DI Water Resistivity Alarms *)
    rTrip_Resist_LL               : REAL := 10.0;              (* Low-Low Contamination Trip [MOhm-cm] *)
    rTrip_Resist_L                : REAL := 15.0;              (* Low Polisher Exhaustion Warning [MOhm-cm] *)
    rDeadband_Resist              : REAL := 1.0;               (* Clear Deadband [MOhm-cm] *)
    bAlarm_Resist_LL              : BOOL := FALSE;
    bAlarm_Resist_L               : BOOL := FALSE;

    (* Stack Coolant Temperature Alarms *)
    rTrip_StackTemp_HH            : REAL := 82.0;              (* High-High Over-Temp Trip [deg C] *)
    rTrip_StackTemp_H             : REAL := 75.0;              (* High Temperature Warning [deg C] *)
    rTrip_StackTemp_L             : REAL := 45.0;              (* Low Temperature Efficiency Flag [deg C] *)
    rTrip_StackTemp_LL            : REAL := 25.0;              (* Low-Low Freezing/Freeze Lockout [deg C] *)
    rDeadband_StackTemp           : REAL := 2.0;               (* Clear Deadband [deg C] *)
    bAlarm_StackTemp_HH           : BOOL := FALSE;
    bAlarm_StackTemp_H            : BOOL := FALSE;
    bAlarm_StackTemp_L            : BOOL := FALSE;
    bAlarm_StackTemp_LL           : BOOL := FALSE;

    (* Separator Level Alarms (Cathode) *)
    rTrip_CathLevel_HH            : REAL := 88.0;              (* High-High Gas Entrainment Trip [%] *)
    rTrip_CathLevel_H             : REAL := 72.0;              (* High Level Warning [%] *)
    rTrip_CathLevel_L             : REAL := 28.0;              (* Low Level Warning [%] *)
    rTrip_CathLevel_LL            : REAL := 12.0;              (* Low-Low Gas Blow-Through Trip [%] *)
    rDeadband_Level               : REAL := 3.0;               (* Clear Deadband [%] *)
    bAlarm_CathLevel_HH           : BOOL := FALSE;
    bAlarm_CathLevel_H            : BOOL := FALSE;
    bAlarm_CathLevel_L            : BOOL := FALSE;
    bAlarm_CathLevel_LL           : BOOL := FALSE;

    (* CVM Cell Voltage Alarms *)
    rTrip_CellVolt_HH             : REAL := 2.35;              (* High-High Cell Overvoltage Trip [V] *)
    rTrip_CellVolt_H              : REAL := 2.18;              (* High Degradation Warning [V] *)
    rTrip_CellVolt_LL             : REAL := 1.15;              (* Low-Low Short Circuit Trip [V] *)
    bAlarm_CellVolt_HH            : BOOL := FALSE;
    bAlarm_CellVolt_H             : BOOL := FALSE;
    bAlarm_CellVolt_LL            : BOOL := FALSE;

    (* Master Latch Bits *)
    bLatchedEmergencyTrip         : BOOL := FALSE;
    bLatchedProcessWarning        : BOOL := FALSE;

    (* Loop Counters *)
    i                             : INT := 1;
    j                             : INT := 1;
    m                             : INT := 1;
    iterPGD                       : INT := 1;
END_VAR
""")

    # -------------------------------------------------------------------------
    # 5. BODY: PHASE 1 — 2oo3 TMR SENSOR VOTING WITH DISCREPANCY TIMERS
    # -------------------------------------------------------------------------
    code_parts.append("""
(*
========================================================================================================================
  PHASE 1: 2oo3 TRIPLE MODULAR REDUNDANCY (TMR) SENSOR VOTING WITH DISCREPANCY TIMERS
  Each triplicate channel (A, B, C) is cross-evaluated against allowable noise tolerances. If a channel drifts
  beyond tolerance for > 50 consecutive scans (500 ms), it is marked unhealthy, raising an advisory alarm and
  initiating graceful mathematical degradation (2oo3 -> 1oo2 Conservative -> 1oo1 Emergency -> Trip).
========================================================================================================================
*)

(* --- Channel 1: Stack Total Voltage [V] --- *)
IF ABS(rStackVoltage_ChA - rStackVoltage_ChB) > rTol_StackVoltage OR
   ABS(rStackVoltage_ChB - rStackVoltage_ChC) > rTol_StackVoltage OR
   ABS(rStackVoltage_ChA - rStackVoltage_ChC) > rTol_StackVoltage THEN
    nDiscrepancyTimer_StackVolt := nDiscrepancyTimer_StackVolt + 1;
    IF nDiscrepancyTimer_StackVolt > 50 THEN
        bDiscrepancyTrip_StackVolt := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_StackVolt > 0 THEN
        nDiscrepancyTimer_StackVolt := nDiscrepancyTimer_StackVolt - 1;
    END_IF;
    IF nDiscrepancyTimer_StackVolt = 0 THEN
        bDiscrepancyTrip_StackVolt := FALSE;
    END_IF;
END_IF;

bHealthyA_StackVolt := (rStackVoltage_ChA >= 0.0) AND (rStackVoltage_ChA <= 2500.0);
bHealthyB_StackVolt := (rStackVoltage_ChB >= 0.0) AND (rStackVoltage_ChB <= 2500.0);
bHealthyC_StackVolt := (rStackVoltage_ChC >= 0.0) AND (rStackVoltage_ChC <= 2500.0);

IF bHealthyA_StackVolt AND bHealthyB_StackVolt AND bHealthyC_StackVolt THEN
    nDegradedMode_StackVolt := 3; (* Full 2oo3 Median Voting *)
    IF (rStackVoltage_ChA >= rStackVoltage_ChB AND rStackVoltage_ChA <= rStackVoltage_ChC) OR
       (rStackVoltage_ChA >= rStackVoltage_ChC AND rStackVoltage_ChA <= rStackVoltage_ChB) THEN
        rVotedStackVoltage := rStackVoltage_ChA;
    ELSIF (rStackVoltage_ChB >= rStackVoltage_ChA AND rStackVoltage_ChB <= rStackVoltage_ChC) OR
          (rStackVoltage_ChB >= rStackVoltage_ChC AND rStackVoltage_ChB <= rStackVoltage_ChA) THEN
        rVotedStackVoltage := rStackVoltage_ChB;
    ELSE
        rVotedStackVoltage := rStackVoltage_ChC;
    END_IF;
ELSIF bHealthyA_StackVolt AND bHealthyB_StackVolt THEN
    nDegradedMode_StackVolt := 2; (* 1oo2 Average Mode *)
    rVotedStackVoltage := (rStackVoltage_ChA + rStackVoltage_ChB) * 0.5;
ELSIF bHealthyB_StackVolt AND bHealthyC_StackVolt THEN
    nDegradedMode_StackVolt := 2;
    rVotedStackVoltage := (rStackVoltage_ChB + rStackVoltage_ChC) * 0.5;
ELSIF bHealthyA_StackVolt AND bHealthyC_StackVolt THEN
    nDegradedMode_StackVolt := 2;
    rVotedStackVoltage := (rStackVoltage_ChA + rStackVoltage_ChC) * 0.5;
ELSIF bHealthyA_StackVolt THEN
    nDegradedMode_StackVolt := 1; (* 1oo1 Emergency Run *)
    rVotedStackVoltage := rStackVoltage_ChA;
ELSIF bHealthyB_StackVolt THEN
    nDegradedMode_StackVolt := 1;
    rVotedStackVoltage := rStackVoltage_ChB;
ELSIF bHealthyC_StackVolt THEN
    nDegradedMode_StackVolt := 1;
    rVotedStackVoltage := rStackVoltage_ChC;
ELSE
    nDegradedMode_StackVolt := 0; (* All Channels Failed *)
    rVotedStackVoltage := 0.0;
    bLatchedEmergencyTrip := TRUE;
END_IF;


(* --- Channel 2: Stack DC Current [kA] --- *)
IF ABS(rStackCurrent_ChA - rStackCurrent_ChB) > rTol_StackCurrent OR
   ABS(rStackCurrent_ChB - rStackCurrent_ChC) > rTol_StackCurrent OR
   ABS(rStackCurrent_ChA - rStackCurrent_ChC) > rTol_StackCurrent THEN
    nDiscrepancyTimer_StackCurr := nDiscrepancyTimer_StackCurr + 1;
    IF nDiscrepancyTimer_StackCurr > 50 THEN
        bDiscrepancyTrip_StackCurr := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_StackCurr > 0 THEN
        nDiscrepancyTimer_StackCurr := nDiscrepancyTimer_StackCurr - 1;
    END_IF;
    IF nDiscrepancyTimer_StackCurr = 0 THEN
        bDiscrepancyTrip_StackCurr := FALSE;
    END_IF;
END_IF;

bHealthyA_StackCurr := (rStackCurrent_ChA >= -0.2) AND (rStackCurrent_ChA <= 12.0);
bHealthyB_StackCurr := (rStackCurrent_ChB >= -0.2) AND (rStackCurrent_ChB <= 12.0);
bHealthyC_StackCurr := (rStackCurrent_ChC >= -0.2) AND (rStackCurrent_ChC <= 12.0);

IF bHealthyA_StackCurr AND bHealthyB_StackCurr AND bHealthyC_StackCurr THEN
    nDegradedMode_StackCurr := 3;
    IF (rStackCurrent_ChA >= rStackCurrent_ChB AND rStackCurrent_ChA <= rStackCurrent_ChC) OR
       (rStackCurrent_ChA >= rStackCurrent_ChC AND rStackCurrent_ChA <= rStackCurrent_ChB) THEN
        rVotedStackCurrent := rStackCurrent_ChA;
    ELSIF (rStackCurrent_ChB >= rStackCurrent_ChA AND rStackCurrent_ChB <= rStackCurrent_ChC) OR
          (rStackCurrent_ChB >= rStackCurrent_ChC AND rStackCurrent_ChB <= rStackCurrent_ChA) THEN
        rVotedStackCurrent := rStackCurrent_ChB;
    ELSE
        rVotedStackCurrent := rStackCurrent_ChC;
    END_IF;
ELSIF bHealthyA_StackCurr AND bHealthyB_StackCurr THEN
    nDegradedMode_StackCurr := 2;
    rVotedStackCurrent := (rStackCurrent_ChA + rStackCurrent_ChB) * 0.5;
ELSIF bHealthyB_StackCurr AND bHealthyC_StackCurr THEN
    nDegradedMode_StackCurr := 2;
    rVotedStackCurrent := (rStackCurrent_ChB + rStackCurrent_ChC) * 0.5;
ELSIF bHealthyA_StackCurr AND bHealthyC_StackCurr THEN
    nDegradedMode_StackCurr := 2;
    rVotedStackCurrent := (rStackCurrent_ChA + rStackCurrent_ChC) * 0.5;
ELSIF bHealthyA_StackCurr THEN
    nDegradedMode_StackCurr := 1;
    rVotedStackCurrent := rStackCurrent_ChA;
ELSIF bHealthyB_StackCurr THEN
    nDegradedMode_StackCurr := 1;
    rVotedStackCurrent := rStackCurrent_ChB;
ELSIF bHealthyC_StackCurr THEN
    nDegradedMode_StackCurr := 1;
    rVotedStackCurrent := rStackCurrent_ChC;
ELSE
    nDegradedMode_StackCurr := 0;
    rVotedStackCurrent := 0.0;
    bLatchedEmergencyTrip := TRUE;
END_IF;


(* --- Channel 3: Cathode Separator Liquid Level [%] --- *)
IF ABS(rCathodeLevel_ChA - rCathodeLevel_ChB) > rTol_CathodeLevel OR
   ABS(rCathodeLevel_ChB - rCathodeLevel_ChC) > rTol_CathodeLevel OR
   ABS(rCathodeLevel_ChA - rCathodeLevel_ChC) > rTol_CathodeLevel THEN
    nDiscrepancyTimer_CathLevel := nDiscrepancyTimer_CathLevel + 1;
    IF nDiscrepancyTimer_CathLevel > 50 THEN
        bDiscrepancyTrip_CathLevel := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_CathLevel > 0 THEN
        nDiscrepancyTimer_CathLevel := nDiscrepancyTimer_CathLevel - 1;
    END_IF;
    IF nDiscrepancyTimer_CathLevel = 0 THEN
        bDiscrepancyTrip_CathLevel := FALSE;
    END_IF;
END_IF;

bHealthyA_CathLevel := (rCathodeLevel_ChA >= -2.0) AND (rCathodeLevel_ChA <= 102.0);
bHealthyB_CathLevel := (rCathodeLevel_ChB >= -2.0) AND (rCathodeLevel_ChB <= 102.0);
bHealthyC_CathLevel := (rCathodeLevel_ChC >= -2.0) AND (rCathodeLevel_ChC <= 102.0);

IF bHealthyA_CathLevel AND bHealthyB_CathLevel AND bHealthyC_CathLevel THEN
    nDegradedMode_CathLevel := 3;
    IF (rCathodeLevel_ChA >= rCathodeLevel_ChB AND rCathodeLevel_ChA <= rCathodeLevel_ChC) OR
       (rCathodeLevel_ChA >= rCathodeLevel_ChC AND rCathodeLevel_ChA <= rCathodeLevel_ChB) THEN
        rVotedCathodeLevel := rCathodeLevel_ChA;
    ELSIF (rCathodeLevel_ChB >= rCathodeLevel_ChA AND rCathodeLevel_ChB <= rCathodeLevel_ChC) OR
          (rCathodeLevel_ChB >= rCathodeLevel_ChC AND rCathodeLevel_ChB <= rCathodeLevel_ChA) THEN
        rVotedCathodeLevel := rCathodeLevel_ChB;
    ELSE
        rVotedCathodeLevel := rCathodeLevel_ChC;
    END_IF;
ELSIF bHealthyA_CathLevel AND bHealthyB_CathLevel THEN
    nDegradedMode_CathLevel := 2;
    rVotedCathodeLevel := (rCathodeLevel_ChA + rCathodeLevel_ChB) * 0.5;
ELSIF bHealthyB_CathLevel AND bHealthyC_CathLevel THEN
    nDegradedMode_CathLevel := 2;
    rVotedCathodeLevel := (rCathodeLevel_ChB + rCathodeLevel_ChC) * 0.5;
ELSIF bHealthyA_CathLevel AND bHealthyC_CathLevel THEN
    nDegradedMode_CathLevel := 2;
    rVotedCathodeLevel := (rCathodeLevel_ChA + rCathodeLevel_ChC) * 0.5;
ELSIF bHealthyA_CathLevel THEN
    nDegradedMode_CathLevel := 1;
    rVotedCathodeLevel := rCathodeLevel_ChA;
ELSIF bHealthyB_CathLevel THEN
    nDegradedMode_CathLevel := 1;
    rVotedCathodeLevel := rCathodeLevel_ChB;
ELSIF bHealthyC_CathLevel THEN
    nDegradedMode_CathLevel := 1;
    rVotedCathodeLevel := rCathodeLevel_ChC;
ELSE
    nDegradedMode_CathLevel := 0;
    rVotedCathodeLevel := 50.0;
    bLatchedEmergencyTrip := TRUE;
END_IF;


(* --- Channel 4: Anode Separator Liquid Level [%] --- *)
IF ABS(rAnodeLevel_ChA - rAnodeLevel_ChB) > rTol_AnodeLevel OR
   ABS(rAnodeLevel_ChB - rAnodeLevel_ChC) > rTol_AnodeLevel OR
   ABS(rAnodeLevel_ChA - rAnodeLevel_ChC) > rTol_AnodeLevel THEN
    nDiscrepancyTimer_AnodeLevel := nDiscrepancyTimer_AnodeLevel + 1;
    IF nDiscrepancyTimer_AnodeLevel > 50 THEN
        bDiscrepancyTrip_AnodeLevel := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_AnodeLevel > 0 THEN
        nDiscrepancyTimer_AnodeLevel := nDiscrepancyTimer_AnodeLevel - 1;
    END_IF;
    IF nDiscrepancyTimer_AnodeLevel = 0 THEN
        bDiscrepancyTrip_AnodeLevel := FALSE;
    END_IF;
END_IF;

bHealthyA_AnodeLevel := (rAnodeLevel_ChA >= -2.0) AND (rAnodeLevel_ChA <= 102.0);
bHealthyB_AnodeLevel := (rAnodeLevel_ChB >= -2.0) AND (rAnodeLevel_ChB <= 102.0);
bHealthyC_AnodeLevel := (rAnodeLevel_ChC >= -2.0) AND (rAnodeLevel_ChC <= 102.0);

IF bHealthyA_AnodeLevel AND bHealthyB_AnodeLevel AND bHealthyC_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 3;
    IF (rAnodeLevel_ChA >= rAnodeLevel_ChB AND rAnodeLevel_ChA <= rAnodeLevel_ChC) OR
       (rAnodeLevel_ChA >= rAnodeLevel_ChC AND rAnodeLevel_ChA <= rAnodeLevel_ChB) THEN
        rVotedAnodeLevel := rAnodeLevel_ChA;
    ELSIF (rAnodeLevel_ChB >= rAnodeLevel_ChA AND rAnodeLevel_ChB <= rAnodeLevel_ChC) OR
          (rAnodeLevel_ChB >= rAnodeLevel_ChC AND rAnodeLevel_ChB <= rAnodeLevel_ChA) THEN
        rVotedAnodeLevel := rAnodeLevel_ChB;
    ELSE
        rVotedAnodeLevel := rAnodeLevel_ChC;
    END_IF;
ELSIF bHealthyA_AnodeLevel AND bHealthyB_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 2;
    rVotedAnodeLevel := (rAnodeLevel_ChA + rAnodeLevel_ChB) * 0.5;
ELSIF bHealthyB_AnodeLevel AND bHealthyC_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 2;
    rVotedAnodeLevel := (rAnodeLevel_ChB + rAnodeLevel_ChC) * 0.5;
ELSIF bHealthyA_AnodeLevel AND bHealthyC_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 2;
    rVotedAnodeLevel := (rAnodeLevel_ChA + rAnodeLevel_ChC) * 0.5;
ELSIF bHealthyA_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 1;
    rVotedAnodeLevel := rAnodeLevel_ChA;
ELSIF bHealthyB_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 1;
    rVotedAnodeLevel := rAnodeLevel_ChB;
ELSIF bHealthyC_AnodeLevel THEN
    nDegradedMode_AnodeLevel := 1;
    rVotedAnodeLevel := rAnodeLevel_ChC;
ELSE
    nDegradedMode_AnodeLevel := 0;
    rVotedAnodeLevel := 50.0;
    bLatchedEmergencyTrip := TRUE;
END_IF;


(* --- Channel 5: Membrane Differential Pressure [mbar] (CRITICAL SAFETY) --- *)
IF ABS(rDiffPressure_ChA - rDiffPressure_ChB) > rTol_DiffPressure OR
   ABS(rDiffPressure_ChB - rDiffPressure_ChC) > rTol_DiffPressure OR
   ABS(rDiffPressure_ChA - rDiffPressure_ChC) > rTol_DiffPressure THEN
    nDiscrepancyTimer_DiffPress := nDiscrepancyTimer_DiffPress + 1;
    IF nDiscrepancyTimer_DiffPress > 30 THEN (* 300 ms fast discrepancy trip *)
        bDiscrepancyTrip_DiffPress := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_DiffPress > 0 THEN
        nDiscrepancyTimer_DiffPress := nDiscrepancyTimer_DiffPress - 1;
    END_IF;
    IF nDiscrepancyTimer_DiffPress = 0 THEN
        bDiscrepancyTrip_DiffPress := FALSE;
    END_IF;
END_IF;

bHealthyA_DiffPress := (rDiffPressure_ChA >= -350.0) AND (rDiffPressure_ChA <= 350.0);
bHealthyB_DiffPress := (rDiffPressure_ChB >= -350.0) AND (rDiffPressure_ChB <= 350.0);
bHealthyC_DiffPress := (rDiffPressure_ChC >= -350.0) AND (rDiffPressure_ChC <= 350.0);

IF bHealthyA_DiffPress AND bHealthyB_DiffPress AND bHealthyC_DiffPress THEN
    nDegradedMode_DiffPress := 3;
    IF (rDiffPressure_ChA >= rDiffPressure_ChB AND rDiffPressure_ChA <= rDiffPressure_ChC) OR
       (rDiffPressure_ChA >= rDiffPressure_ChC AND rDiffPressure_ChA <= rDiffPressure_ChB) THEN
        rVotedDifferentialPressure := rDiffPressure_ChA;
    ELSIF (rDiffPressure_ChB >= rDiffPressure_ChA AND rDiffPressure_ChB <= rDiffPressure_ChC) OR
          (rDiffPressure_ChB >= rDiffPressure_ChC AND rDiffPressure_ChB <= rDiffPressure_ChA) THEN
        rVotedDifferentialPressure := rDiffPressure_ChB;
    ELSE
        rVotedDifferentialPressure := rDiffPressure_ChC;
    END_IF;
ELSIF bHealthyA_DiffPress AND bHealthyB_DiffPress THEN
    nDegradedMode_DiffPress := 2;
    (* Conservative: choose maximum absolute excursion to protect membrane *)
    IF ABS(rDiffPressure_ChA) >= ABS(rDiffPressure_ChB) THEN
        rVotedDifferentialPressure := rDiffPressure_ChA;
    ELSE
        rVotedDifferentialPressure := rDiffPressure_ChB;
    END_IF;
ELSIF bHealthyB_DiffPress AND bHealthyC_DiffPress THEN
    nDegradedMode_DiffPress := 2;
    IF ABS(rDiffPressure_ChB) >= ABS(rDiffPressure_ChC) THEN
        rVotedDifferentialPressure := rDiffPressure_ChB;
    ELSE
        rVotedDifferentialPressure := rDiffPressure_ChC;
    END_IF;
ELSIF bHealthyA_DiffPress AND bHealthyC_DiffPress THEN
    nDegradedMode_DiffPress := 2;
    IF ABS(rDiffPressure_ChA) >= ABS(rDiffPressure_ChC) THEN
        rVotedDifferentialPressure := rDiffPressure_ChA;
    ELSE
        rVotedDifferentialPressure := rDiffPressure_ChC;
    END_IF;
ELSIF bHealthyA_DiffPress THEN
    nDegradedMode_DiffPress := 1;
    rVotedDifferentialPressure := rDiffPressure_ChA;
ELSIF bHealthyB_DiffPress THEN
    nDegradedMode_DiffPress := 1;
    rVotedDifferentialPressure := rDiffPressure_ChB;
ELSIF bHealthyC_DiffPress THEN
    nDegradedMode_DiffPress := 1;
    rVotedDifferentialPressure := rDiffPressure_ChC;
ELSE
    nDegradedMode_DiffPress := 0;
    rVotedDifferentialPressure := 250.0; (* Trigger fail-safe trip immediately *)
    bLatchedEmergencyTrip := TRUE;
END_IF;

(* Rate of Change Evaluation for Differential Pressure [mbar/s] *)
rRoC_DiffPressure := (rVotedDifferentialPressure - rPrev_DiffPressure) / c_Ts_sec;
rPrev_DiffPressure := rVotedDifferentialPressure;


(* --- Channel 6: Trace Oxygen in Hydrogen (O2-in-H2) [ppm] (LEL COMBUSTIBLE SAFETY) --- *)
IF ABS(rO2_in_H2_ChA - rO2_in_H2_ChB) > rTol_O2_in_H2 OR
   ABS(rO2_in_H2_ChB - rO2_in_H2_ChC) > rTol_O2_in_H2 OR
   ABS(rO2_in_H2_ChA - rO2_in_H2_ChC) > rTol_O2_in_H2 THEN
    nDiscrepancyTimer_O2_in_H2 := nDiscrepancyTimer_O2_in_H2 + 1;
    IF nDiscrepancyTimer_O2_in_H2 > 40 THEN
        bDiscrepancyTrip_O2_in_H2 := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_O2_in_H2 > 0 THEN
        nDiscrepancyTimer_O2_in_H2 := nDiscrepancyTimer_O2_in_H2 - 1;
    END_IF;
    IF nDiscrepancyTimer_O2_in_H2 = 0 THEN
        bDiscrepancyTrip_O2_in_H2 := FALSE;
    END_IF;
END_IF;

bHealthyA_O2_in_H2 := (rO2_in_H2_ChA >= 0.0) AND (rO2_in_H2_ChA <= 50000.0);
bHealthyB_O2_in_H2 := (rO2_in_H2_ChB >= 0.0) AND (rO2_in_H2_ChB <= 50000.0);
bHealthyC_O2_in_H2 := (rO2_in_H2_ChC >= 0.0) AND (rO2_in_H2_ChC <= 50000.0);

IF bHealthyA_O2_in_H2 AND bHealthyB_O2_in_H2 AND bHealthyC_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 3;
    IF (rO2_in_H2_ChA >= rO2_in_H2_ChB AND rO2_in_H2_ChA <= rO2_in_H2_ChC) OR
       (rO2_in_H2_ChA >= rO2_in_H2_ChC AND rO2_in_H2_ChA <= rO2_in_H2_ChB) THEN
        rVotedO2_in_H2 := rO2_in_H2_ChA;
    ELSIF (rO2_in_H2_ChB >= rO2_in_H2_ChA AND rO2_in_H2_ChB <= rO2_in_H2_ChC) OR
          (rO2_in_H2_ChB >= rO2_in_H2_ChC AND rO2_in_H2_ChB <= rO2_in_H2_ChA) THEN
        rVotedO2_in_H2 := rO2_in_H2_ChB;
    ELSE
        rVotedO2_in_H2 := rO2_in_H2_ChC;
    END_IF;
ELSIF bHealthyA_O2_in_H2 AND bHealthyB_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 2;
    (* Conservative selection: maximum combustible gas concentration *)
    IF rO2_in_H2_ChA >= rO2_in_H2_ChB THEN rVotedO2_in_H2 := rO2_in_H2_ChA; ELSE rVotedO2_in_H2 := rO2_in_H2_ChB; END_IF;
ELSIF bHealthyB_O2_in_H2 AND bHealthyC_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 2;
    IF rO2_in_H2_ChB >= rO2_in_H2_ChC THEN rVotedO2_in_H2 := rO2_in_H2_ChB; ELSE rVotedO2_in_H2 := rO2_in_H2_ChC; END_IF;
ELSIF bHealthyA_O2_in_H2 AND bHealthyC_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 2;
    IF rO2_in_H2_ChA >= rO2_in_H2_ChC THEN rVotedO2_in_H2 := rO2_in_H2_ChA; ELSE rVotedO2_in_H2 := rO2_in_H2_ChC; END_IF;
ELSIF bHealthyA_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 1;
    rVotedO2_in_H2 := rO2_in_H2_ChA;
ELSIF bHealthyB_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 1;
    rVotedO2_in_H2 := rO2_in_H2_ChB;
ELSIF bHealthyC_O2_in_H2 THEN
    nDegradedMode_O2_in_H2 := 1;
    rVotedO2_in_H2 := rO2_in_H2_ChC;
ELSE
    nDegradedMode_O2_in_H2 := 0;
    rVotedO2_in_H2 := 20000.0; (* Trip failsafe *)
    bLatchedEmergencyTrip := TRUE;
END_IF;

rRoC_O2_in_H2 := (rVotedO2_in_H2 - rPrev_O2_in_H2) / c_Ts_sec;
rPrev_O2_in_H2 := rVotedO2_in_H2;


(* --- Channel 7: Trace Hydrogen in Oxygen (H2-in-O2) [ppm] --- *)
IF ABS(rH2_in_O2_ChA - rH2_in_O2_ChB) > rTol_H2_in_O2 OR
   ABS(rH2_in_O2_ChB - rH2_in_O2_ChC) > rTol_H2_in_O2 OR
   ABS(rH2_in_O2_ChA - rH2_in_O2_ChC) > rTol_H2_in_O2 THEN
    nDiscrepancyTimer_H2_in_O2 := nDiscrepancyTimer_H2_in_O2 + 1;
    IF nDiscrepancyTimer_H2_in_O2 > 40 THEN
        bDiscrepancyTrip_H2_in_O2 := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_H2_in_O2 > 0 THEN
        nDiscrepancyTimer_H2_in_O2 := nDiscrepancyTimer_H2_in_O2 - 1;
    END_IF;
    IF nDiscrepancyTimer_H2_in_O2 = 0 THEN
        bDiscrepancyTrip_H2_in_O2 := FALSE;
    END_IF;
END_IF;

bHealthyA_H2_in_O2 := (rH2_in_O2_ChA >= 0.0) AND (rH2_in_O2_ChA <= 50000.0);
bHealthyB_H2_in_O2 := (rH2_in_O2_ChB >= 0.0) AND (rH2_in_O2_ChB <= 50000.0);
bHealthyC_H2_in_O2 := (rH2_in_O2_ChC >= 0.0) AND (rH2_in_O2_ChC <= 50000.0);

IF bHealthyA_H2_in_O2 AND bHealthyB_H2_in_O2 AND bHealthyC_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 3;
    IF (rH2_in_O2_ChA >= rH2_in_O2_ChB AND rH2_in_O2_ChA <= rH2_in_O2_ChC) OR
       (rH2_in_O2_ChA >= rH2_in_O2_ChC AND rH2_in_O2_ChA <= rH2_in_O2_ChB) THEN
        rVotedH2_in_O2 := rH2_in_O2_ChA;
    ELSIF (rH2_in_O2_ChB >= rH2_in_O2_ChA AND rH2_in_O2_ChB <= rH2_in_O2_ChC) OR
          (rH2_in_O2_ChB >= rH2_in_O2_ChC AND rH2_in_O2_ChB <= rH2_in_O2_ChA) THEN
        rVotedH2_in_O2 := rH2_in_O2_ChB;
    ELSE
        rVotedH2_in_O2 := rH2_in_O2_ChC;
    END_IF;
ELSIF bHealthyA_H2_in_O2 AND bHealthyB_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 2;
    IF rH2_in_O2_ChA >= rH2_in_O2_ChB THEN rVotedH2_in_O2 := rH2_in_O2_ChA; ELSE rVotedH2_in_O2 := rH2_in_O2_ChB; END_IF;
ELSIF bHealthyB_H2_in_O2 AND bHealthyC_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 2;
    IF rH2_in_O2_ChB >= rH2_in_O2_ChC THEN rVotedH2_in_O2 := rH2_in_O2_ChB; ELSE rVotedH2_in_O2 := rH2_in_O2_ChC; END_IF;
ELSIF bHealthyA_H2_in_O2 AND bHealthyC_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 2;
    IF rH2_in_O2_ChA >= rH2_in_O2_ChC THEN rVotedH2_in_O2 := rH2_in_O2_ChA; ELSE rVotedH2_in_O2 := rH2_in_O2_ChC; END_IF;
ELSIF bHealthyA_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 1;
    rVotedH2_in_O2 := rH2_in_O2_ChA;
ELSIF bHealthyB_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 1;
    rVotedH2_in_O2 := rH2_in_O2_ChB;
ELSIF bHealthyC_H2_in_O2 THEN
    nDegradedMode_H2_in_O2 := 1;
    rVotedH2_in_O2 := rH2_in_O2_ChC;
ELSE
    nDegradedMode_H2_in_O2 := 0;
    rVotedH2_in_O2 := 20000.0;
    bLatchedEmergencyTrip := TRUE;
END_IF;

rRoC_H2_in_O2 := (rVotedH2_in_O2 - rPrev_H2_in_O2) / c_Ts_sec;
rPrev_H2_in_O2 := rVotedH2_in_O2;


(* --- Channel 8: Stack Coolant Outlet Temperature [deg C] --- *)
IF ABS(rStackTemp_ChA - rStackTemp_ChB) > rTol_StackTemp OR
   ABS(rStackTemp_ChB - rStackTemp_ChC) > rTol_StackTemp OR
   ABS(rStackTemp_ChA - rStackTemp_ChC) > rTol_StackTemp THEN
    nDiscrepancyTimer_StackTemp := nDiscrepancyTimer_StackTemp + 1;
    IF nDiscrepancyTimer_StackTemp > 50 THEN
        bDiscrepancyTrip_StackTemp := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_StackTemp > 0 THEN
        nDiscrepancyTimer_StackTemp := nDiscrepancyTimer_StackTemp - 1;
    END_IF;
    IF nDiscrepancyTimer_StackTemp = 0 THEN
        bDiscrepancyTrip_StackTemp := FALSE;
    END_IF;
END_IF;

bHealthyA_StackTemp := (rStackTemp_ChA >= 5.0) AND (rStackTemp_ChA <= 115.0);
bHealthyB_StackTemp := (rStackTemp_ChB >= 5.0) AND (rStackTemp_ChB <= 115.0);
bHealthyC_StackTemp := (rStackTemp_ChC >= 5.0) AND (rStackTemp_ChC <= 115.0);

IF bHealthyA_StackTemp AND bHealthyB_StackTemp AND bHealthyC_StackTemp THEN
    nDegradedMode_StackTemp := 3;
    IF (rStackTemp_ChA >= rStackTemp_ChB AND rStackTemp_ChA <= rStackTemp_ChC) OR
       (rStackTemp_ChA >= rStackTemp_ChC AND rStackTemp_ChA <= rStackTemp_ChB) THEN
        rVotedStackTemp := rStackTemp_ChA;
    ELSIF (rStackTemp_ChB >= rStackTemp_ChA AND rStackTemp_ChB <= rStackTemp_ChC) OR
          (rStackTemp_ChB >= rStackTemp_ChC AND rStackTemp_ChB <= rStackTemp_ChA) THEN
        rVotedStackTemp := rStackTemp_ChB;
    ELSE
        rVotedStackTemp := rStackTemp_ChC;
    END_IF;
ELSIF bHealthyA_StackTemp AND bHealthyB_StackTemp THEN
    nDegradedMode_StackTemp := 2;
    IF rStackTemp_ChA >= rStackTemp_ChB THEN rVotedStackTemp := rStackTemp_ChA; ELSE rVotedStackTemp := rStackTemp_ChB; END_IF;
ELSIF bHealthyB_StackTemp AND bHealthyC_StackTemp THEN
    nDegradedMode_StackTemp := 2;
    IF rStackTemp_ChB >= rStackTemp_ChC THEN rVotedStackTemp := rStackTemp_ChB; ELSE rVotedStackTemp := rStackTemp_ChC; END_IF;
ELSIF bHealthyA_StackTemp AND bHealthyC_StackTemp THEN
    nDegradedMode_StackTemp := 2;
    IF rStackTemp_ChA >= rStackTemp_ChC THEN rVotedStackTemp := rStackTemp_ChA; ELSE rVotedStackTemp := rStackTemp_ChC; END_IF;
ELSIF bHealthyA_StackTemp THEN
    nDegradedMode_StackTemp := 1;
    rVotedStackTemp := rStackTemp_ChA;
ELSIF bHealthyB_StackTemp THEN
    nDegradedMode_StackTemp := 1;
    rVotedStackTemp := rStackTemp_ChB;
ELSIF bHealthyC_StackTemp THEN
    nDegradedMode_StackTemp := 1;
    rVotedStackTemp := rStackTemp_ChC;
ELSE
    nDegradedMode_StackTemp := 0;
    rVotedStackTemp := 90.0; (* Failsafe over-temp indication *)
    bLatchedEmergencyTrip := TRUE;
END_IF;


(* --- Channel 9: Demineralized Water Resistivity [MOhm-cm] --- *)
IF ABS(rDI_Resistivity_ChA - rDI_Resistivity_ChB) > rTol_DI_Resistivity OR
   ABS(rDI_Resistivity_ChB - rDI_Resistivity_ChC) > rTol_DI_Resistivity OR
   ABS(rDI_Resistivity_ChA - rDI_Resistivity_ChC) > rTol_DI_Resistivity THEN
    nDiscrepancyTimer_DI_Resist := nDiscrepancyTimer_DI_Resist + 1;
    IF nDiscrepancyTimer_DI_Resist > 60 THEN
        bDiscrepancyTrip_DI_Resist := TRUE;
    END_IF;
ELSE
    IF nDiscrepancyTimer_DI_Resist > 0 THEN
        nDiscrepancyTimer_DI_Resist := nDiscrepancyTimer_DI_Resist - 1;
    END_IF;
    IF nDiscrepancyTimer_DI_Resist = 0 THEN
        bDiscrepancyTrip_DI_Resist := FALSE;
    END_IF;
END_IF;

bHealthyA_DI_Resist := (rDI_Resistivity_ChA >= 0.01) AND (rDI_Resistivity_ChA <= 25.0);
bHealthyB_DI_Resist := (rDI_Resistivity_ChB >= 0.01) AND (rDI_Resistivity_ChB <= 25.0);
bHealthyC_DI_Resist := (rDI_Resistivity_ChC >= 0.01) AND (rDI_Resistivity_ChC <= 25.0);

IF bHealthyA_DI_Resist AND bHealthyB_DI_Resist AND bHealthyC_DI_Resist THEN
    nDegradedMode_DI_Resist := 3;
    IF (rDI_Resistivity_ChA >= rDI_Resistivity_ChB AND rDI_Resistivity_ChA <= rDI_Resistivity_ChC) OR
       (rDI_Resistivity_ChA >= rDI_Resistivity_ChC AND rDI_Resistivity_ChA <= rDI_Resistivity_ChB) THEN
        rVotedResistivity := rDI_Resistivity_ChA;
    ELSIF (rDI_Resistivity_ChB >= rDI_Resistivity_ChA AND rDI_Resistivity_ChB <= rDI_Resistivity_ChC) OR
          (rDI_Resistivity_ChB >= rDI_Resistivity_ChC AND rDI_Resistivity_ChB <= rDI_Resistivity_ChA) THEN
        rVotedResistivity := rDI_Resistivity_ChB;
    ELSE
        rVotedResistivity := rDI_Resistivity_ChC;
    END_IF;
ELSIF bHealthyA_DI_Resist AND bHealthyB_DI_Resist THEN
    nDegradedMode_DI_Resist := 2;
    (* Conservative mode: lower resistivity represents worse contamination *)
    IF rDI_Resistivity_ChA <= rDI_Resistivity_ChB THEN rVotedResistivity := rDI_Resistivity_ChA; ELSE rVotedResistivity := rDI_Resistivity_ChB; END_IF;
ELSIF bHealthyB_DI_Resist AND bHealthyC_DI_Resist THEN
    nDegradedMode_DI_Resist := 2;
    IF rDI_Resistivity_ChB <= rDI_Resistivity_ChC THEN rVotedResistivity := rDI_Resistivity_ChB; ELSE rVotedResistivity := rDI_Resistivity_ChC; END_IF;
ELSIF bHealthyA_DI_Resist AND bHealthyC_DI_Resist THEN
    nDegradedMode_DI_Resist := 2;
    IF rDI_Resistivity_ChA <= rDI_Resistivity_ChC THEN rVotedResistivity := rDI_Resistivity_ChA; ELSE rVotedResistivity := rDI_Resistivity_ChC; END_IF;
ELSIF bHealthyA_DI_Resist THEN
    nDegradedMode_DI_Resist := 1;
    rVotedResistivity := rDI_Resistivity_ChA;
ELSIF bHealthyB_DI_Resist THEN
    nDegradedMode_DI_Resist := 1;
    rVotedResistivity := rDI_Resistivity_ChB;
ELSIF bHealthyC_DI_Resist THEN
    nDegradedMode_DI_Resist := 1;
    rVotedResistivity := rDI_Resistivity_ChC;
ELSE
    nDegradedMode_DI_Resist := 0;
    rVotedResistivity := 5.0; (* Contaminated trip condition *)
    bLatchedEmergencyTrip := TRUE;
END_IF;
""")

    # -------------------------------------------------------------------------
    # 6. BODY: PHASE 2 — FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION
    # -------------------------------------------------------------------------
    code_parts.append("""
(*
========================================================================================================================
  PHASE 2: FIRST-PRINCIPLES CYBER-PHYSICAL STATE-SPACE ESTIMATION
  Discretized Linearized Matrix System:
    x[k+1] = A * x[k] + B * u[k] + E_dist * d[k]
    y[k]   = C_mat * x[k] + D_mat * u[k]
  Augmented by First-Principles Non-Linear Electrochemical Kinetic Updates:
    - Butler-Volmer Overpotentials & High-Field Hyperbolic Arcsine Kinetics
    - Nafion 117 / Aquivion Temperature & Hydration Dependent Membrane Conductivity
    - Dynamic Faradaic Efficiency with Parasitic Shunt & Crossover Correction
    - Electro-Osmotic Water Drag & Gas-Liquid Equilibrium Equations
========================================================================================================================
*)

IF NOT bStateMatricesInitialized THEN
    (* -------------------------------------------------------------------------
       Discrete State Transition Matrix A (8x8) at Ts = 0.010 s (10 ms)
       States:
         x1: Cell Overpotential [V]
         x2: Hydrogen Production Rate [Nm3/h]
         x3: Membrane Water Activity lambda [-]
         x4: Stack Coolant Bulk Temp [deg C]
         x5: Cathode Separator Liquid Level [%]
         x6: Membrane Differential Pressure [mbar]
         x7: Trace O2-in-H2 Concentration [ppm]
         x8: Stack DC Current Density [A/cm2]
       ------------------------------------------------------------------------- *)
    A[1,1] := 0.98500; A[1,2] := 0.00000; A[1,3] := -0.01250; A[1,4] := -0.00840; A[1,5] := 0.00000; A[1,6] := 0.00010; A[1,7] := 0.00000; A[1,8] := 0.04500;
    A[2,1] := 0.00000; A[2,2] := 0.99100; A[2,3] := 0.00120;  A[2,4] := 0.05200;  A[2,5] := 0.00000; A[2,6] := -0.00250; A[2,7] := 0.00000; A[2,8] := 18.5200;
    A[3,1] := 0.00000; A[3,2] := 0.00000; A[3,3] := 0.99600;  A[3,4] := -0.00180; A[3,5] := 0.00000; A[3,6] := 0.00000;  A[3,7] := 0.00000; A[3,8] := 0.00350;
    A[4,1] := 1.25000; A[4,2] := 0.00000; A[4,3] := -0.00500; A[4,4] := 0.99450;  A[4,5] := 0.00000; A[4,6] := 0.00000;  A[4,7] := 0.00000; A[4,8] := 0.85000;
    A[5,1] := 0.00000; A[5,2] := 0.00420; A[5,3] := 0.00150;  A[5,4] := 0.00000;  A[5,5] := 0.99800; A[5,6] := -0.00150; A[5,7] := 0.00000; A[5,8] := 0.00850;
    A[6,1] := 0.00000; A[6,2] := 0.03500; A[6,3] := 0.00000;  A[6,4] := 0.00000;  A[6,5] := 0.00000; A[6,6] := 0.98200;  A[6,7] := 0.00000; A[6,8] := 0.05500;
    A[7,1] := 0.00000; A[7,2] := -0.02500; A[7,3] := 0.01500; A[7,4] := 0.08200;  A[7,5] := 0.00000; A[7,6] := 0.01200;  A[7,7] := 0.98900; A[7,8] := -0.04500;
    A[8,1] := -0.01500; A[8,2] := 0.00000; A[8,3] := 0.00000; A[8,4] := 0.00000;  A[8,5] := 0.00000; A[8,6] := 0.00000;  A[8,7] := 0.00000; A[8,8] := 0.95000;

    (* -------------------------------------------------------------------------
       Discrete Control Input Matrix B (8x8) at Ts = 0.010 s (10 ms)
       Inputs:
         u1: Rectifier Current Setpoint [kA]
         u2: DI Water Pump Speed [%]
         u3: Coolant 3-Way Valve [%]
         u4: Cathode Drain Valve [%]
         u5: Cathode PCV H2 Valve [%]
         u6: Anode PCV O2 Valve [%]
         u7: Polisher Bypass Valve [%]
         u8: N2 Purge Injection Valve [%]
       ------------------------------------------------------------------------- *)
    B[1,1] := 0.01250; B[1,2] := 0.00000; B[1,3] := 0.00000; B[1,4] := 0.00000; B[1,5] := 0.00000; B[1,6] := 0.00000; B[1,7] := 0.00000; B[1,8] := 0.00000;
    B[2,1] := 5.25000; B[2,2] := 0.00000; B[2,3] := 0.00000; B[2,4] := 0.00000; B[2,5] := -0.01500; B[2,6] := 0.00000; B[2,7] := 0.00000; B[2,8] := 0.00000;
    B[3,1] := 0.00120; B[3,2] := 0.00450; B[3,3] := 0.00000; B[3,4] := 0.00000; B[3,5] := 0.00000; B[3,6] := 0.00000; B[3,7] := 0.00000; B[3,8] := 0.00000;
    B[4,1] := 0.15000; B[4,2] := -0.08500; B[4,3] := -0.12500; B[4,4] := 0.00000; B[4,5] := 0.00000; B[4,6] := 0.00000; B[4,7] := 0.00000; B[4,8] := 0.00000;
    B[5,1] := 0.00250; B[5,2] := 0.00000; B[5,3] := 0.00000; B[5,4] := -0.06500; B[5,5] := 0.00000; B[5,6] := 0.00000; B[5,7] := 0.00000; B[5,8] := 0.00000;
    B[6,1] := 0.01800; B[6,2] := 0.00000; B[6,3] := 0.00000; B[6,4] := 0.00000; B[6,5] := -0.15000; B[6,6] := 0.14800; B[6,7] := 0.00000; B[6,8] := 0.00000;
    B[7,1] := -0.05500; B[7,2] := 0.00000; B[7,3] := 0.00000; B[7,4] := 0.00000; B[7,5] := 0.00000; B[7,6] := 0.00000; B[7,7] := 0.00000; B[7,8] := -0.25000;
    B[8,1] := 0.28500; B[8,2] := 0.00000; B[8,3] := 0.00000; B[8,4] := 0.00000; B[8,5] := 0.00000; B[8,6] := 0.00000; B[8,7] := 0.00000; B[8,8] := 0.00000;

    (* -------------------------------------------------------------------------
       Discrete Output Matrix C_mat (8x8) - Direct Sensor Mapping
       ------------------------------------------------------------------------- *)
    FOR i := 1 TO 8 DO
        FOR j := 1 TO 8 DO
            IF i = j THEN
                C_mat[i,j] := 1.0;
                D_mat[i,j] := 0.0;
            ELSE
                C_mat[i,j] := 0.0;
                D_mat[i,j] := 0.0;
            END_IF;
        END_FOR;
    END_FOR;

    (* -------------------------------------------------------------------------
       Disturbance Coupling Matrix E_dist (8x4)
       Disturbances:
         d1: Renewable Power Available [MW]
         d2: DI Water Feed Temp [deg C]
         d3: Export Pipeline Back-Pressure [bar]
         d4: Secondary Cooling Water Supply Temp [deg C]
       ------------------------------------------------------------------------- *)
    E_dist[1,1] := 0.0000; E_dist[1,2] := -0.0015; E_dist[1,3] := 0.0005; E_dist[1,4] := 0.0000;
    E_dist[2,1] := 0.4500; E_dist[2,2] := 0.0080;  E_dist[2,3] := -0.1200; E_dist[2,4] := 0.0000;
    E_dist[3,1] := 0.0000; E_dist[3,2] := 0.0020;  E_dist[3,3] := 0.0000;  E_dist[3,4] := 0.0000;
    E_dist[4,1] := 0.0250; E_dist[4,2] := 0.0450;  E_dist[4,3] := 0.0000;  E_dist[4,4] := 0.0750;
    E_dist[5,1] := 0.0000; E_dist[5,2] := 0.0000;  E_dist[5,3] := -0.0080; E_dist[5,4] := 0.0000;
    E_dist[6,1] := 0.0000; E_dist[6,2] := 0.0000;  E_dist[6,3] := 0.0450;  E_dist[6,4] := 0.0000;
    E_dist[7,1] := -0.0150; E_dist[7,2] := 0.0120; E_dist[7,3] := 0.0080;  E_dist[7,4] := 0.0000;
    E_dist[8,1] := 0.0500; E_dist[8,2] := 0.0000;  E_dist[8,3] := 0.0000;  E_dist[8,4] := 0.0000;

    (* -------------------------------------------------------------------------
       Luenberger State Observer Gain Vector L_obs (8x1)
       ------------------------------------------------------------------------- *)
    L_obs[1] := 0.1250;
    L_obs[2] := 0.1850;
    L_obs[3] := 0.0650;
    L_obs[4] := 0.1450;
    L_obs[5] := 0.2200;
    L_obs[6] := 0.3500;
    L_obs[7] := 0.2800;
    L_obs[8] := 0.4500;

    (* -------------------------------------------------------------------------
       MPC Quadratic Cost Weights (Q, R, S, P)
       ------------------------------------------------------------------------- *)
    Q_weight[1] := 15.0;  (* Cell Overpotential penalty *)
    Q_weight[2] := 25.0;  (* Hydrogen Production Rate penalty *)
    Q_weight[3] := 8.0;   (* Membrane Hydration penalty *)
    Q_weight[4] := 12.0;  (* Stack Coolant Temp penalty *)
    Q_weight[5] := 20.0;  (* Cathode Level penalty *)
    Q_weight[6] := 50.0;  (* Differential Pressure penalty (HIGH PRIORITY SAFETY) *)
    Q_weight[7] := 40.0;  (* Trace O2 in H2 penalty (HIGH PRIORITY SAFETY) *)
    Q_weight[8] := 10.0;  (* Current density tracking *)

    R_weight[1] := 2.5;   (* Rectifier Current Effort *)
    R_weight[2] := 0.5;   (* Pump Speed Effort *)
    R_weight[3] := 0.8;   (* Coolant Valve Effort *)
    R_weight[4] := 1.2;   (* Drain Valve Effort *)
    R_weight[5] := 3.5;   (* Cathode PCV Effort *)
    R_weight[6] := 3.5;   (* Anode PCV Effort *)
    R_weight[7] := 0.2;   (* Polisher Valve Effort *)
    R_weight[8] := 5.0;   (* N2 Injection Effort (Resource Conservation) *)

    S_weight[1] := 8.0;   (* Slew Rate Penalties *)
    S_weight[2] := 1.5;
    S_weight[3] := 2.0;
    S_weight[4] := 3.0;
    S_weight[5] := 10.0;
    S_weight[6] := 10.0;
    S_weight[7] := 0.5;
    S_weight[8] := 12.0;

    FOR i := 1 TO 8 DO
        P_weight[i] := Q_weight[i] * 2.5; (* Terminal Cost Riccati Approximation *)
    END_FOR;

    (* Physical Box Actuator Saturation Limits *)
    u_min[1] := 0.0;    u_max[1] := 8.5;   (* Rectifier Current: 0.0 to 8.5 kA *)
    u_min[2] := 10.0;   u_max[2] := 100.0; (* DI Pump Speed: 10% to 100% *)
    u_min[3] := 0.0;    u_max[3] := 100.0; (* Coolant Valve: 0% to 100% *)
    u_min[4] := 0.0;    u_max[4] := 100.0; (* Drain Valve: 0% to 100% *)
    u_min[5] := 0.0;    u_max[5] := 100.0; (* Cathode PCV: 0% to 100% *)
    u_min[6] := 0.0;    u_max[6] := 100.0; (* Anode PCV: 0% to 100% *)
    u_min[7] := 0.0;    u_max[7] := 100.0; (* Polisher Valve: 0% to 100% *)
    u_min[8] := 0.0;    u_max[8] := 100.0; (* N2 Purge Valve: 0% to 100% *)

    (* Actuator Slew Rate Box Limits (per 10 ms cycle) *)
    delta_u_max[1] := 0.0425; (* Rectifier: max 4.25 kA/s slew *)
    delta_u_max[2] := 0.5000; (* Pump: max 50%/s slew *)
    delta_u_max[3] := 0.4000; (* Coolant Valve: max 40%/s slew *)
    delta_u_max[4] := 0.6000; (* Drain Valve: max 60%/s slew *)
    delta_u_max[5] := 1.2000; (* Fast PCV: max 120%/s slew *)
    delta_u_max[6] := 1.2000; (* Fast PCV: max 120%/s slew *)
    delta_u_max[7] := 0.5000; (* Polisher Valve: max 50%/s slew *)
    delta_u_max[8] := 2.0000; (* Fast Solenoid N2 Purge: max 200%/s slew *)

    (* Initialize states to nominal equilibrium *)
    x_state[1] := 1.85;     (* Nominal Cell Overpotential [V] *)
    x_state[2] := 0.0;      (* Hydrogen Flow [Nm3/h] *)
    x_state[3] := 14.0;     (* Membrane Hydration lambda [-] *)
    x_state[4] := 25.0;     (* Stack Temperature [deg C] *)
    x_state[5] := 50.0;     (* Cathode Level [%] *)
    x_state[6] := 0.0;      (* Differential Pressure [mbar] *)
    x_state[7] := 200.0;    (* Trace O2 in H2 [ppm] *)
    x_state[8] := 0.0;      (* Current Density [A/cm2] *)

    FOR i := 1 TO 8 DO
        u_cmd[i] := u_min[i];
        u_prev[i] := u_min[i];
    END_FOR;

    bStateMatricesInitialized := TRUE;
END_IF;

(* Pack Disturbance Vector d[k] *)
d_dist[1] := rRenewablePowerAvailable;
d_dist[2] := rRawWaterFeedTemp;
d_dist[3] := rDownstreamPipelinePressure;
d_dist[4] := rCoolingWaterSupplyTemp;

(* Map 2oo3 Voted Outputs to y_meas Vector *)
y_meas[1] := rAvgCellVoltageCVM;
y_meas[2] := rHydrogenFlowActual;
y_meas[3] := x_state[3]; (* Unmeasured internal state, observer estimated *)
y_meas[4] := rVotedStackTemp;
y_meas[5] := rVotedCathodeLevel;
y_meas[6] := rVotedDifferentialPressure;
y_meas[7] := rVotedO2_in_H2;
y_meas[8] := (rVotedStackCurrent * 1000.0) / c_A_cell_cm2; (* Current density A/cm2 *)

(* Compute Estimated Output y_est = C_mat * x_state *)
FOR i := 1 TO 8 DO
    y_est[i] := 0.0;
    FOR j := 1 TO 8 DO
        y_est[i] := y_est[i] + C_mat[i,j] * x_state[j];
    END_FOR;
END_FOR;

(* Propagate One-Step Ahead State Model: x_pred = A * x_state + B * u_cmd + E_dist * d_dist *)
FOR i := 1 TO 8 DO
    x_pred[i] := 0.0;
    FOR j := 1 TO 8 DO
        x_pred[i] := x_pred[i] + A[i,j] * x_state[j] + B[i,j] * u_cmd[j];
    END_FOR;
    FOR m := 1 TO 4 DO
        x_pred[i] := x_pred[i] + E_dist[i,m] * d_dist[m];
    END_FOR;
END_FOR;

(* Apply Luenberger Observer Innovation: x_state[k+1] = x_pred + L_obs * (y_meas - y_est) *)
FOR i := 1 TO 8 DO
    x_state[i] := x_pred[i] + L_obs[i] * (y_meas[i] - y_est[i]);
END_FOR;

(* First-Principles Non-Linear Corrections *)
(* 1. Current Density *)
rCurrentDensityActual := (rVotedStackCurrent * 1000.0) / c_A_cell_cm2;
x_state[8] := rCurrentDensityActual;

(* 2. Dynamic Faradaic Efficiency Calculation *)
IF rCurrentDensityActual > 0.05 THEN
    rFaradaicEfficiency := ((rCurrentDensityActual / 2.0) * (rCurrentDensityActual / 2.0)) /
                           (0.0025 + ((rCurrentDensityActual / 2.0) * (rCurrentDensityActual / 2.0))) *
                           (1.0 - (x_state[7] / 1.0E6)) * 100.0;
    IF rFaradaicEfficiency > 99.8 THEN rFaradaicEfficiency := 99.8; END_IF;
ELSE
    rFaradaicEfficiency := 0.0;
END_IF;

(* 3. Faraday's Law Net Hydrogen Volumetric Generation Rate [Nm3/h] *)
rHydrogenFlowActual := (rFaradaicEfficiency / 100.0) *
                       ((c_N_cells * (rVotedStackCurrent * 1000.0)) / (2.0 * c_F_faraday)) *
                       c_V_mol_norm * 3600.0;
x_state[2] := rHydrogenFlowActual;

(* 4. Oxygen Production Rate (Stoichiometric 2:1 Ratio) [Nm3/h] *)
rOxygenFlowActual := rHydrogenFlowActual * 0.50;

(* 5. Specific Electrical Energy Consumption [kWh/Nm3 H2] *)
IF rHydrogenFlowActual > 10.0 THEN
    rSpecificEnergyConsumption := (rVotedStackVoltage * rVotedStackCurrent) / rHydrogenFlowActual;
    (* Electrochemical HHV Efficiency [%] = (HHV_H2_MJ_kg * rho_norm / (SEC * 3.6)) * 100 *)
    rElectrochemicalEfficiency := ((c_HHV_H2_MJ_kg * c_rho_H2_norm) / (rSpecificEnergyConsumption * 3.6)) * 100.0;
ELSE
    rSpecificEnergyConsumption := 0.0;
    rElectrochemicalEfficiency := 0.0;
END_IF;

(* 6. State Observer Membrane Hydration Water Activity Estimation *)
rMembraneHydrationEst := x_state[3];
IF rMembraneHydrationEst < 2.0 THEN rMembraneHydrationEst := 2.0; END_IF;
IF rMembraneHydrationEst > 24.0 THEN rMembraneHydrationEst := 24.0; END_IF;

(* 7. Cell Voltage Safety Margin [V] *)
rCellVoltageMargin := rTrip_CellVolt_HH - rMaxCellVoltageCVM;
""")

    # -------------------------------------------------------------------------
    # 7. BODY: PHASE 3 — RECEDING-HORIZON MPC OPTIMIZATION WITH PGD & SLEW LIMITS
    # -------------------------------------------------------------------------
    code_parts.append("""
(*
========================================================================================================================
  PHASE 3: RECEDING-HORIZON MPC OPTIMIZATION WITH PROJECTED GRADIENT DESCENT (PGD)
  Multi-Objective Quadratic Performance Functional:
    Min J(u) = 1/2 * e_x^T * Q * e_x + 1/2 * e_u^T * R * e_u + 1/2 * Delta_u^T * S * Delta_u + 1/2 * e_xN^T * P * e_xN
  Subject to:
    u_min <= u[k] <= u_max  (Box Actuator Bounds)
    |u[k] - u_prev[k]| <= delta_u_max  (Dynamic Slew Rate Limits)
========================================================================================================================
*)

(* Compute Reference Trajectory x_ref Based on Active Production Demand *)
IF nOperatingState = 7 (* Peak Production *) OR nOperatingState = 6 (* Renewable Tracking *) THEN
    (* Target Current based on Renewable MW Setpoint and Max Stack Rating *)
    IF rRenewablePowerAvailable > 0.5 THEN
        x_ref[8] := (rRenewablePowerAvailable * 1.0E6) / (rVotedStackVoltage * c_A_cell_cm2);
        IF x_ref[8] > 2.5 THEN x_ref[8] := 2.5; END_IF; (* Clamped to max design current density 2.5 A/cm2 *)
    ELSE
        x_ref[8] := 0.25; (* Minimum 10% turndown *)
    END_IF;
    x_ref[1] := 1.92;                      (* Target mean cell operating voltage [V] *)
    x_ref[2] := rHydrogenDemandFlow;       (* Target Hydrogen production flow [Nm3/h] *)
    x_ref[3] := 18.0;                      (* Target fully hydrated membrane activity lambda *)
    x_ref[4] := rTargetStackTemperature;   (* Nominal 65.0 deg C *)
    x_ref[5] := 50.0;                      (* Separator Mid-Level 50.0% *)
    x_ref[6] := 0.0;                       (* Zero Differential Pressure Target [mbar] *)
    x_ref[7] := 350.0;                     (* Residual O2 in H2 baseline [ppm] *)
ELSIF nOperatingState = 8 THEN (* Low Power Reserve *)
    x_ref[8] := 0.20;                      (* Low current hot reserve 0.2 A/cm2 *)
    x_ref[1] := 1.55;
    x_ref[2] := 400.0;
    x_ref[3] := 14.0;
    x_ref[4] := 55.0;
    x_ref[5] := 50.0;
    x_ref[6] := 0.0;
    x_ref[7] := 850.0;
ELSE
    x_ref[8] := 0.0;
    x_ref[1] := 1.23;
    x_ref[2] := 0.0;
    x_ref[3] := 12.0;
    x_ref[4] := 30.0;
    x_ref[5] := 50.0;
    x_ref[6] := 0.0;
    x_ref[7] := 50.0;
END_IF;

(* Projected Gradient Descent Iterative Loop (6 Iterations per Scan) *)
FOR iterPGD := 1 TO 6 DO
    (* Calculate Analytical Gradient:
       grad_J[i] = R[i] * (u_cmd[i] - u_ref[i]) + S[i] * (u_cmd[i] - u_prev[i]) + SUM_j( B[j,i] * Q[j] * (x_state[j] - x_ref[j]) )
    *)
    FOR i := 1 TO 8 DO
        grad_J[i] := R_weight[i] * (u_cmd[i] - u_min[i]) + S_weight[i] * (u_cmd[i] - u_prev[i]);
        FOR j := 1 TO 8 DO
            grad_J[i] := grad_J[i] + B[j,i] * Q_weight[j] * (x_state[j] - x_ref[j]);
        END_FOR;
    END_FOR;

    (* Gradient Step with Projection onto Feasible Actuator Box & Slew Bounds *)
    FOR i := 1 TO 8 DO
        u_trial[i] := u_cmd[i] - rAlphaPGD * grad_J[i];

        (* Dynamic Slew Rate Clamping *)
        IF (u_trial[i] - u_prev[i]) > delta_u_max[i] THEN
            u_trial[i] := u_prev[i] + delta_u_max[i];
        ELSIF (u_trial[i] - u_prev[i]) < -delta_u_max[i] THEN
            u_trial[i] := u_prev[i] - delta_u_max[i];
        END_IF;

        (* Physical Box Boundary Clamping *)
        IF u_trial[i] > u_max[i] THEN
            u_trial[i] := u_max[i];
        ELSIF u_trial[i] < u_min[i] THEN
            u_trial[i] := u_min[i];
        END_IF;

        u_cmd[i] := u_trial[i];
    END_FOR;
END_FOR;

(* 3-Element Level Control Feedforward Cascade for Separator Drain Valve *)
rCathLevel_Integral := rCathLevel_Integral + (rVotedCathodeLevel - 50.0) * c_Ts_sec;
IF rCathLevel_Integral > 20.0 THEN rCathLevel_Integral := 20.0; END_IF;
IF rCathLevel_Integral < -20.0 THEN rCathLevel_Integral := -20.0; END_IF;

(* Modulate u_cmd[4] (Drain Valve) using 3-element Level Cascade *)
u_cmd[4] := 25.0 + 1.25 * (rVotedCathodeLevel - 50.0) +
            0.15 * rCathLevel_Integral +
            0.85 * (rCathodeDrainFlow - 0.25 * rWaterCirculationFlow);
IF u_cmd[4] > 100.0 THEN u_cmd[4] := 100.0; END_IF;
IF u_cmd[4] < 0.0 THEN u_cmd[4] := 0.0; END_IF;

(* Anode & Cathode Back-Pressure Differential Trimming *)
IF bMembraneDP_Locked THEN
    (* Freeze backpressure commands to arrest pressure surges *)
    u_cmd[5] := u_prev[5];
    u_cmd[6] := u_prev[6];
ELSE
    (* Dynamic DP trim: if H2 > O2 (positive Delta-P), open H2 PCV or close O2 PCV *)
    u_cmd[5] := u_cmd[5] + 0.045 * rVotedDifferentialPressure;
    u_cmd[6] := u_cmd[6] - 0.045 * rVotedDifferentialPressure;
    IF u_cmd[5] > 100.0 THEN u_cmd[5] := 100.0; END_IF;
    IF u_cmd[5] < 0.0 THEN u_cmd[5] := 0.0; END_IF;
    IF u_cmd[6] > 100.0 THEN u_cmd[6] := 100.0; END_IF;
    IF u_cmd[6] < 0.0 THEN u_cmd[6] := 0.0; END_IF;
END_IF;

(* Store Historical Control Vector for Slew Evaluation in Next Cycle *)
FOR i := 1 TO 8 DO
    u_prev[i] := u_cmd[i];
END_FOR;
""")

    # -------------------------------------------------------------------------
    # 8. BODY: PHASE 4 — DETERMINISTIC 14-STAGE FINITE STATE MACHINE (FSM)
    # -------------------------------------------------------------------------
    code_parts.append("""
(*
========================================================================================================================
  PHASE 4: DETERMINISTIC 14-STAGE PRODUCTION FINITE STATE MACHINE (FSM)
  Strict deterministic sequence governing commercial green hydrogen production:
    Stage 0 : STATE_OFFLINE_DEENERGIZED              Stage 7 : STATE_STEADY_STATE_PEAK_PRODUCTION
    Stage 1 : STATE_NITROGEN_INERTING_PURGE          Stage 8 : STATE_TURNDOWN_LOW_POWER_RESERVE
    Stage 2 : STATE_WATER_CIRCULATION_RESISTIVITY    Stage 9 : STATE_MEMBRANE_DP_STABILIZATION
    Stage 3 : STATE_SYSTEM_PREPRESSURIZATION         Stage 10: STATE_CONTROLLED_RAMPDOWN_SHUTDOWN
    Stage 4 : STATE_STACK_CONDITIONING_POLARIZATION  Stage 11: STATE_STACK_DEPOLARIZATION_COOLDOWN
    Stage 5 : STATE_WARMUP_RAMP_HEATING              Stage 12: STATE_POST_SHUTDOWN_N2_SAFETY_PURGE
    Stage 6 : STATE_RENEWABLE_RAMP_FOLLOWING         Stage 13: STATE_EMERGENCY_FAST_TRIP_VENT
========================================================================================================================
*)

(* Master Emergency Trip Override Guard *)
IF bLatchedEmergencyTrip OR NOT bEmergencyStop THEN
    nFSM_State := 13; (* Immediate transition to SIL-3 Fast Trip *)
END_IF;

(* Track State Dwell Duration Timer *)
IF nFSM_State = nFSM_PrevState THEN
    nStateScanTimer := nStateScanTimer + 1;
ELSE
    nStateScanTimer := 0;
    nFSM_PrevState := nFSM_State;
END_IF;

CASE nFSM_State OF

    0: (* STATE_OFFLINE_DEENERGIZED *)
        bSystemRunning := FALSE;
        bProductionReady := FALSE;
        bNitrogenPurging := FALSE;
        bDepolarizationActive := FALSE;
        bStandbyReserveActive := FALSE;
        bMembraneDP_Locked := FALSE;

        rRectifierCurrentCmd := 0.0;
        rCirculationPumpSpeedCmd := 0.0;
        rCoolantBypassValveCmd := 0.0;
        rCathodeDrainValveCmd := 0.0;
        rCathodePCV_Cmd := 0.0;
        rAnodePCV_Cmd := 0.0;
        rPolisherBypassValveCmd := 0.0;
        rN2PurgeValveCmd := 0.0;
        rFastVentValveCmd_H2 := 0.0;
        rFastVentValveCmd_O2 := 0.0;

        IF bSystemEnable AND bAutoStart AND NOT bLatchedEmergencyTrip THEN
            IF bNitrogenPurgePermissive AND bCoolingWaterAvailable THEN
                nPurgeStep := 0;
                nFSM_State := 1; (* Proceed to Nitrogen Purge *)
            END_IF;
        END_IF;


    1: (* STATE_NITROGEN_INERTING_PURGE *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bNitrogenPurging := TRUE;
        bDepolarizationActive := FALSE;

        rRectifierCurrentCmd := 0.0;
        rCirculationPumpSpeedCmd := 15.0; (* Low DI purge flow *)
        rCathodePCV_Cmd := 75.0;          (* Open gas vent paths *)
        rAnodePCV_Cmd := 75.0;
        rFastVentValveCmd_H2 := 10.0;
        rFastVentValveCmd_O2 := 10.0;
        rN2PurgeValveCmd := 85.0;         (* High volume N2 blanket flush *)

        (* Purge dwell: 1000 scans = 10.0 seconds of inerting displacement *)
        IF nStateScanTimer > 1000 THEN
            IF rVotedO2_in_H2 < 200.0 AND rVotedH2_in_O2 < 200.0 THEN
                rN2PurgeValveCmd := 0.0;
                rFastVentValveCmd_H2 := 0.0;
                rFastVentValveCmd_O2 := 0.0;
                nFSM_State := 2; (* Advance to Water Circulation & Resistivity *)
            END_IF;
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    2: (* STATE_WATER_CIRCULATION_RESISTIVITY_QUAL *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bNitrogenPurging := FALSE;

        rCirculationPumpSpeedCmd := 65.0; (* Full circulation through deox & resin bed *)
        rPolisherBypassValveCmd := 100.0; (* 100% flow through mixed-bed polisher *)
        rCathodePCV_Cmd := 10.0;
        rAnodePCV_Cmd := 10.0;
        rCoolantBypassValveCmd := 100.0;  (* Bypass heat exchanger to conserve heat *)

        (* Qualify DI Water: Resistivity must exceed 18.0 MOhm-cm for at least 5 seconds *)
        IF rVotedResistivity >= 18.0 AND bAnodeRecircPumpRunning THEN
            IF nStateScanTimer > 500 THEN
                nFSM_State := 3; (* Advance to System Pre-pressurization *)
            END_IF;
        ELSE
            (* Reset timer if resistivity dips *)
            IF rVotedResistivity < 18.0 THEN
                nStateScanTimer := 0;
            END_IF;
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    3: (* STATE_SYSTEM_PREPRESSURIZATION *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;

        rCirculationPumpSpeedCmd := 50.0;
        rTargetPressureRamp := 1.0 + (DINT_TO_REAL(nStateScanTimer) * 0.004); (* Ramp up to 5.0 bar *)
        IF rTargetPressureRamp > 5.0 THEN rTargetPressureRamp := 5.0; END_IF;

        (* Backpressure valves hold header pressure *)
        IF rCathodeGasPressure < rTargetPressureRamp THEN
            rCathodePCV_Cmd := 5.0;
        ELSE
            rCathodePCV_Cmd := 25.0;
        END_IF;

        IF rAnodeGasPressure < rTargetPressureRamp THEN
            rAnodePCV_Cmd := 5.0;
        ELSE
            rAnodePCV_Cmd := 25.0;
        END_IF;

        (* Verify differential pressure remains strictly balanced *)
        IF ABS(rVotedDifferentialPressure) < 50.0 AND rCathodeGasPressure >= 4.8 THEN
            IF nStateScanTimer > 800 THEN
                nFSM_State := 4; (* Advance to Stack Polarization Conditioning *)
            END_IF;
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    4: (* STATE_STACK_CONDITIONING_POLARIZATION *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bStandbyReserveActive := FALSE;

        (* Low-current trickle conditioning: 0.5 kA (approx 6% load) *)
        rRectifierCurrentCmd := 0.50;
        rCirculationPumpSpeedCmd := 60.0;
        rPolisherBypassValveCmd := 50.0;

        (* Validate Cell Voltage Monitoring (CVM): all cells must be between 1.35 V and 1.85 V *)
        IF rMinCellVoltageCVM > 1.35 AND rMaxCellVoltageCVM < 1.95 AND rAvgCellVoltageCVM > 1.45 THEN
            IF nStateScanTimer > 600 THEN (* 6 seconds conditioning *)
                nFSM_State := 5; (* Proceed to Warmup Ramp *)
            END_IF;
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    5: (* STATE_WARMUP_RAMP_HEATING *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;

        (* Ramp current up to 30% load at 1.5%/s while warming the stack *)
        rWarmupRampSetpoint := 0.50 + (DINT_TO_REAL(nStateScanTimer) * 0.0015);
        IF rWarmupRampSetpoint > 2.50 THEN rWarmupRampSetpoint := 2.50; END_IF;
        rRectifierCurrentCmd := rWarmupRampSetpoint;

        rCirculationPumpSpeedCmd := 70.0;
        rCoolantBypassValveCmd := 90.0; (* Keep coolant in bypass to heat up stack *)

        (* Warmup criteria: Stack coolant temperature reaches 55.0 deg C *)
        IF rVotedStackTemp >= 55.0 AND rCathodeGasPressure >= 15.0 THEN
            bProductionReady := TRUE;
            IF rRenewablePowerAvailable > 2.0 THEN
                nFSM_State := 6; (* Renewable Ramp Following *)
            ELSE
                nFSM_State := 7; (* Steady State Peak Production *)
            END_IF;
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    6: (* STATE_RENEWABLE_RAMP_FOLLOWING *)
        bSystemRunning := TRUE;
        bProductionReady := TRUE;
        bStandbyReserveActive := FALSE;

        (* Rectifier directly governed by MPC u_cmd[1] tracking renewable profile *)
        rRectifierCurrentCmd := u_cmd[1];
        rCirculationPumpSpeedCmd := u_cmd[2];
        rCoolantBypassValveCmd := u_cmd[3];
        rCathodeDrainValveCmd := u_cmd[4];
        rCathodePCV_Cmd := u_cmd[5];
        rAnodePCV_Cmd := u_cmd[6];
        rPolisherBypassValveCmd := u_cmd[7];

        (* Dynamic transition checks *)
        IF ABS(rVotedDifferentialPressure) > 120.0 THEN
            nFSM_State := 9; (* Membrane DP Stabilization *)
        ELSIF rRenewablePowerAvailable < 1.0 AND rHydrogenDemandFlow < 500.0 THEN
            nFSM_State := 8; (* Turndown Low Power Reserve *)
        ELSIF ABS(rRenewablePowerAvailable - 20.0) < 1.5 THEN
            nFSM_State := 7; (* Peak Production *)
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    7: (* STATE_STEADY_STATE_PEAK_PRODUCTION *)
        bSystemRunning := TRUE;
        bProductionReady := TRUE;
        bStandbyReserveActive := FALSE;

        (* Rated 20 MW Peak Production: full MPC execution at 30 bar *)
        rRectifierCurrentCmd := u_cmd[1];
        rCirculationPumpSpeedCmd := u_cmd[2];
        rCoolantBypassValveCmd := u_cmd[3];
        rCathodeDrainValveCmd := u_cmd[4];
        rCathodePCV_Cmd := u_cmd[5];
        rAnodePCV_Cmd := u_cmd[6];
        rPolisherBypassValveCmd := u_cmd[7];

        IF ABS(rVotedDifferentialPressure) > 120.0 THEN
            nFSM_State := 9; (* Divert to Membrane DP Stabilization *)
        ELSIF rRenewablePowerAvailable < 18.0 THEN
            nFSM_State := 6; (* Return to Renewable Ramp Following *)
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    8: (* STATE_TURNDOWN_LOW_POWER_RESERVE *)
        bSystemRunning := TRUE;
        bProductionReady := TRUE;
        bStandbyReserveActive := TRUE;

        (* Minimum stable load 10-15% (0.8 kA) to prevent severe O2-in-H2 crossover *)
        rRectifierCurrentCmd := 0.85;
        rCirculationPumpSpeedCmd := 40.0;
        rCoolantBypassValveCmd := 80.0;

        (* If trace O2-in-H2 rises above 2500 ppm, pulse N2 dilution *)
        IF rVotedO2_in_H2 > 2500.0 THEN
            rN2PurgeValveCmd := 15.0;
        ELSE
            rN2PurgeValveCmd := 0.0;
        END_IF;

        IF rRenewablePowerAvailable >= 2.5 THEN
            bStandbyReserveActive := FALSE;
            nFSM_State := 6; (* Ramp back up to Renewable Following *)
        END_IF;

        IF bControlledStop THEN
            nFSM_State := 10;
        END_IF;


    9: (* STATE_MEMBRANE_DP_STABILIZATION *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bMembraneDP_Locked := TRUE;

        (* Lock current at conservative 2.0 kA while balancing pressures *)
        IF rRectifierCurrentCmd > 2.0 THEN
            rRectifierCurrentCmd := rRectifierCurrentCmd - 0.02;
        END_IF;

        (* Fast active differential pressure correction *)
        IF rVotedDifferentialPressure > 0.0 THEN
            (* H2 pressure higher than O2: vent H2, hold O2 *)
            rCathodePCV_Cmd := rCathodePCV_Cmd + 1.5;
            rAnodePCV_Cmd := rAnodePCV_Cmd - 1.0;
        ELSE
            (* O2 pressure higher than H2: vent O2, hold H2 *)
            rAnodePCV_Cmd := rAnodePCV_Cmd + 1.5;
            rCathodePCV_Cmd := rCathodePCV_Cmd - 1.0;
        END_IF;

        IF rCathodePCV_Cmd > 100.0 THEN rCathodePCV_Cmd := 100.0; END_IF;
        IF rCathodePCV_Cmd < 0.0 THEN rCathodePCV_Cmd := 0.0; END_IF;
        IF rAnodePCV_Cmd > 100.0 THEN rAnodePCV_Cmd := 100.0; END_IF;
        IF rAnodePCV_Cmd < 0.0 THEN rAnodePCV_Cmd := 0.0; END_IF;

        (* Differential pressure recovered within +/- 40 mbar deadband *)
        IF ABS(rVotedDifferentialPressure) < 40.0 THEN
            bMembraneDP_Locked := FALSE;
            nFSM_State := 6; (* Return to active production *)
        END_IF;

        (* If DP does not resolve within 15 seconds (1500 scans), trigger controlled abort *)
        IF nStateScanTimer > 1500 THEN
            nFSM_State := 10;
        END_IF;


    10: (* STATE_CONTROLLED_RAMPDOWN_SHUTDOWN *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bStandbyReserveActive := FALSE;

        (* Slew current to 0 kA at controlled rate of 5%/s *)
        IF rRectifierCurrentCmd > 0.05 THEN
            rRectifierCurrentCmd := rRectifierCurrentCmd - 0.035;
        ELSE
            rRectifierCurrentCmd := 0.0;
        END_IF;

        rCirculationPumpSpeedCmd := 50.0;
        rCoolantBypassValveCmd := 0.0; (* Full cooling water to remove decay heat *)

        (* Once current reaches zero, depressurize headers to flare *)
        IF rRectifierCurrentCmd <= 0.001 THEN
            rCathodePCV_Cmd := 40.0;
            rAnodePCV_Cmd := 40.0;
            IF rCathodeGasPressure < 2.0 AND rAnodeGasPressure < 2.0 THEN
                nFSM_State := 11; (* Proceed to Depolarization *)
            END_IF;
        END_IF;


    11: (* STATE_STACK_DEPOLARIZATION_COOLDOWN *)
        bSystemRunning := TRUE;
        bProductionReady := FALSE;
        bDepolarizationActive := TRUE;

        rRectifierCurrentCmd := 0.0;
        rCirculationPumpSpeedCmd := 45.0;
        rCoolantBypassValveCmd := 0.0;

        (* Allow residual electrochemical capacitive charge to bleed off *)
        IF rVotedStackVoltage < 100.0 AND rVotedStackTemp < 38.0 THEN
            bDepolarizationActive := FALSE;
            nFSM_State := 12; (* Proceed to Post-Shutdown Safety Flush *)
        END_IF;


    12: (* STATE_POST_SHUTDOWN_N2_SAFETY_PURGE *)
        bSystemRunning := FALSE;
        bProductionReady := FALSE;
        bNitrogenPurging := TRUE;

        rRectifierCurrentCmd := 0.0;
        rCirculationPumpSpeedCmd := 20.0;
        rN2PurgeValveCmd := 75.0;
        rCathodePCV_Cmd := 80.0;
        rAnodePCV_Cmd := 80.0;
        rFastVentValveCmd_H2 := 15.0;
        rFastVentValveCmd_O2 := 15.0;

        (* Flush until all combustible gas is completely evacuated (< 50 ppm) *)
        IF nStateScanTimer > 1200 THEN
            IF rVotedO2_in_H2 < 50.0 AND rVotedH2_in_O2 < 50.0 THEN
                rN2PurgeValveCmd := 0.0;
                rFastVentValveCmd_H2 := 0.0;
                rFastVentValveCmd_O2 := 0.0;
                rCathodePCV_Cmd := 0.0;
                rAnodePCV_Cmd := 0.0;
                rCirculationPumpSpeedCmd := 0.0;
                bNitrogenPurging := FALSE;
                nFSM_State := 0; (* Return to Clean Offline De-energized State *)
            END_IF;
        END_IF;


    13: (* STATE_EMERGENCY_FAST_TRIP_VENT (SIL-3 FAST SHUTDOWN) *)
        bSystemRunning := FALSE;
        bProductionReady := FALSE;
        bNitrogenPurging := TRUE;
        bSystemTripped := TRUE;

        (* Instant Breaker Trip *)
        rRectifierCurrentCmd := 0.0;
        rCirculationPumpSpeedCmd := 0.0;
        rCoolantBypassValveCmd := 0.0;
        rPolisherBypassValveCmd := 0.0;

        (* Emergency Fast Vent Blowdown to Safe Flare / Atmospheric Stacks *)
        rFastVentValveCmd_H2 := 100.0;
        rFastVentValveCmd_O2 := 100.0;
        rCathodePCV_Cmd := 100.0;
        rAnodePCV_Cmd := 100.0;

        (* Immediate Nitrogen Blast to Smother Explosive Mixtures *)
        rN2PurgeValveCmd := 100.0;

        (* Latch until manual physical operator reset *)
        IF bAlarmReset AND bEmergencyStop THEN
            IF rCathodeGasPressure < 1.2 AND rAnodeGasPressure < 1.2 AND
               rVotedO2_in_H2 < 1000.0 AND rVotedH2_in_O2 < 1000.0 THEN
                bLatchedEmergencyTrip := FALSE;
                bSystemTripped := FALSE;
                rFastVentValveCmd_H2 := 0.0;
                rFastVentValveCmd_O2 := 0.0;
                rN2PurgeValveCmd := 0.0;
                bNitrogenPurging := FALSE;
                nFSM_State := 0;
            END_IF;
        END_IF;

END_CASE;

nOperatingState := nFSM_State;
""")

    # -------------------------------------------------------------------------
    # 9. BODY: PHASE 5 — ISA-18.2 MULTI-TIER ALARMS & 32-BIT BIT-PACKED STATUS
    # -------------------------------------------------------------------------
    code_parts.append("""
(*
========================================================================================================================
  PHASE 5: ISA-18.2 MULTI-TIER ALARM SYSTEM & 32-BIT BIT-PACKED STATUS WORDS
  Rigorous alarm evaluation covering:
    - High-High (HH) Safety Trips (SIL-3 fast response)
    - High (H) Advisory & Load Turndown Warnings
    - Low (L) Sub-Optimal Process Indicators
    - Low-Low (LL) Equipment Protection Trips
    - Rate-of-Change (RoC) Surge / Fast Leak Detectors
    - Deadband Clearance Hysteresis
  Packing into 32-bit DWORDs:
    - dwStatusWord        : State machine flags, subsystem run states
    - dwFaultWord         : Fatal shutdown interlocks and trip latches
    - dwWarningWord       : Process warnings and advisory alarms
    - dwSensorHealthWord  : 2oo3 TMR degradation flags and discrepancy alarms
========================================================================================================================
*)

(* --- 1. Membrane Differential Pressure Alarms [mbar] --- *)
IF rVotedDifferentialPressure >= rTrip_DP_HH THEN
    bAlarm_DP_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedDifferentialPressure <= (rTrip_DP_HH - rDeadband_DP) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_DP_HH := FALSE;
END_IF;

IF rVotedDifferentialPressure >= rTrip_DP_H THEN
    bAlarm_DP_H := TRUE;
ELSIF rVotedDifferentialPressure <= (rTrip_DP_H - rDeadband_DP) THEN
    bAlarm_DP_H := FALSE;
END_IF;

IF rVotedDifferentialPressure <= rTrip_DP_L THEN
    bAlarm_DP_L := TRUE;
ELSIF rVotedDifferentialPressure >= (rTrip_DP_L + rDeadband_DP) THEN
    bAlarm_DP_L := FALSE;
END_IF;

IF rVotedDifferentialPressure <= rTrip_DP_LL THEN
    bAlarm_DP_LL := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedDifferentialPressure >= (rTrip_DP_LL + rDeadband_DP) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_DP_LL := FALSE;
END_IF;


(* --- 2. Trace Oxygen in Hydrogen (O2-in-H2) Alarms [ppm] --- *)
IF rVotedO2_in_H2 >= rTrip_O2inH2_HH THEN
    bAlarm_O2inH2_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedO2_in_H2 <= (rTrip_O2inH2_HH - rDeadband_O2inH2) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_O2inH2_HH := FALSE;
END_IF;

IF rVotedO2_in_H2 >= rTrip_O2inH2_H THEN
    bAlarm_O2inH2_H := TRUE;
ELSIF rVotedO2_in_H2 <= (rTrip_O2inH2_H - rDeadband_O2inH2) THEN
    bAlarm_O2inH2_H := FALSE;
END_IF;

IF rRoC_O2_in_H2 >= rTrip_O2inH2_RoC THEN
    bAlarm_O2inH2_RoC := TRUE;
ELSE
    bAlarm_O2inH2_RoC := FALSE;
END_IF;


(* --- 3. Trace Hydrogen in Oxygen (H2-in-O2) Alarms [ppm] --- *)
IF rVotedH2_in_O2 >= rTrip_H2inO2_HH THEN
    bAlarm_H2inO2_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedH2_in_O2 <= (rTrip_H2inO2_HH - rDeadband_H2inO2) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_H2inO2_HH := FALSE;
END_IF;

IF rVotedH2_in_O2 >= rTrip_H2inO2_H THEN
    bAlarm_H2inO2_H := TRUE;
ELSIF rVotedH2_in_O2 <= (rTrip_H2inO2_H - rDeadband_H2inO2) THEN
    bAlarm_H2inO2_H := FALSE;
END_IF;

IF rRoC_H2_in_O2 >= rTrip_H2inO2_RoC THEN
    bAlarm_H2inO2_RoC := TRUE;
ELSE
    bAlarm_H2inO2_RoC := FALSE;
END_IF;


(* --- 4. Demineralized Water Resistivity Alarms [MOhm-cm] --- *)
IF rVotedResistivity <= rTrip_Resist_LL THEN
    bAlarm_Resist_LL := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedResistivity >= (rTrip_Resist_LL + rDeadband_Resist) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_Resist_LL := FALSE;
END_IF;

IF rVotedResistivity <= rTrip_Resist_L THEN
    bAlarm_Resist_L := TRUE;
ELSIF rVotedResistivity >= (rTrip_Resist_L + rDeadband_Resist) THEN
    bAlarm_Resist_L := FALSE;
END_IF;


(* --- 5. Stack Coolant Outlet Temperature Alarms [deg C] --- *)
IF rVotedStackTemp >= rTrip_StackTemp_HH THEN
    bAlarm_StackTemp_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedStackTemp <= (rTrip_StackTemp_HH - rDeadband_StackTemp) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_StackTemp_HH := FALSE;
END_IF;

IF rVotedStackTemp >= rTrip_StackTemp_H THEN
    bAlarm_StackTemp_H := TRUE;
ELSIF rVotedStackTemp <= (rTrip_StackTemp_H - rDeadband_StackTemp) THEN
    bAlarm_StackTemp_H := FALSE;
END_IF;

IF rVotedStackTemp <= rTrip_StackTemp_L THEN
    bAlarm_StackTemp_L := TRUE;
ELSIF rVotedStackTemp >= (rTrip_StackTemp_L + rDeadband_StackTemp) THEN
    bAlarm_StackTemp_L := FALSE;
END_IF;

IF rVotedStackTemp <= rTrip_StackTemp_LL THEN
    bAlarm_StackTemp_LL := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedStackTemp >= (rTrip_StackTemp_LL + rDeadband_StackTemp) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_StackTemp_LL := FALSE;
END_IF;


(* --- 6. Separator Liquid Level Alarms (Cathode) [%] --- *)
IF rVotedCathodeLevel >= rTrip_CathLevel_HH THEN
    bAlarm_CathLevel_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedCathodeLevel <= (rTrip_CathLevel_HH - rDeadband_Level) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_CathLevel_HH := FALSE;
END_IF;

IF rVotedCathodeLevel >= rTrip_CathLevel_H THEN
    bAlarm_CathLevel_H := TRUE;
ELSIF rVotedCathodeLevel <= (rTrip_CathLevel_H - rDeadband_Level) THEN
    bAlarm_CathLevel_H := FALSE;
END_IF;

IF rVotedCathodeLevel <= rTrip_CathLevel_L THEN
    bAlarm_CathLevel_L := TRUE;
ELSIF rVotedCathodeLevel >= (rTrip_CathLevel_L + rDeadband_Level) THEN
    bAlarm_CathLevel_L := FALSE;
END_IF;

IF rVotedCathodeLevel <= rTrip_CathLevel_LL THEN
    bAlarm_CathLevel_LL := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rVotedCathodeLevel >= (rTrip_CathLevel_LL + rDeadband_Level) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_CathLevel_LL := FALSE;
END_IF;


(* --- 7. Cell Voltage Monitoring (CVM) Alarms [V] --- *)
IF rMaxCellVoltageCVM >= rTrip_CellVolt_HH THEN
    bAlarm_CellVolt_HH := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rMaxCellVoltageCVM <= (rTrip_CellVolt_HH - 0.05) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_CellVolt_HH := FALSE;
END_IF;

IF rMaxCellVoltageCVM >= rTrip_CellVolt_H THEN
    bAlarm_CellVolt_H := TRUE;
ELSIF rMaxCellVoltageCVM <= (rTrip_CellVolt_H - 0.05) THEN
    bAlarm_CellVolt_H := FALSE;
END_IF;

IF rMinCellVoltageCVM <= rTrip_CellVolt_LL THEN
    bAlarm_CellVolt_LL := TRUE;
    bLatchedEmergencyTrip := TRUE;
ELSIF rMinCellVoltageCVM >= (rTrip_CellVolt_LL + 0.05) AND NOT bLatchedEmergencyTrip THEN
    bAlarm_CellVolt_LL := FALSE;
END_IF;


(* Determine Master Warning Flag *)
bWarningActive := bAlarm_DP_H OR bAlarm_DP_L OR bAlarm_O2inH2_H OR bAlarm_H2inO2_H OR
                  bAlarm_Resist_L OR bAlarm_StackTemp_H OR bAlarm_StackTemp_L OR
                  bAlarm_CathLevel_H OR bAlarm_CathLevel_L OR bAlarm_CellVolt_H OR
                  bDiscrepancyTrip_DiffPress OR bDiscrepancyTrip_O2_in_H2 OR bDiscrepancyTrip_H2_in_O2;

bSystemTripped := bLatchedEmergencyTrip;


(* =========================================================================
   32-BIT BIT-PACKED STATUS WORD (dwStatusWord)
   ========================================================================= *)
dwStatusWord := 16#00000000;
IF bSystemRunning THEN dwStatusWord := dwStatusWord OR 16#00000001; END_IF;          (* Bit 0: System In Run State *)
IF bProductionReady THEN dwStatusWord := dwStatusWord OR 16#00000002; END_IF;        (* Bit 1: Production Load Ready *)
IF bNitrogenPurging THEN dwStatusWord := dwStatusWord OR 16#00000004; END_IF;        (* Bit 2: Nitrogen Purge Active *)
IF bDepolarizationActive THEN dwStatusWord := dwStatusWord OR 16#00000008; END_IF;   (* Bit 3: Depolarization Active *)
IF bStandbyReserveActive THEN dwStatusWord := dwStatusWord OR 16#00000010; END_IF;   (* Bit 4: Standby Low Reserve *)
IF bMembraneDP_Locked THEN dwStatusWord := dwStatusWord OR 16#00000020; END_IF;      (* Bit 5: Membrane DP Locked *)
IF bManualOverride THEN dwStatusWord := dwStatusWord OR 16#00000040; END_IF;         (* Bit 6: Manual Override Active *)
IF bAnodeRecircPumpRunning THEN dwStatusWord := dwStatusWord OR 16#00000080; END_IF; (* Bit 7: Anode Recirc Pump On *)
IF bCathodeDrainPumpRunning THEN dwStatusWord := dwStatusWord OR 16#00000100; END_IF;(* Bit 8: Cathode Drain Pump On *)
IF bRectifierThyristorHealth THEN dwStatusWord := dwStatusWord OR 16#00000200; END_IF;(* Bit 9: Rectifier SCR OK *)
IF bCoolingWaterAvailable THEN dwStatusWord := dwStatusWord OR 16#00000400; END_IF;  (* Bit 10: Cooling Utility OK *)
IF bDownstreamConsumerReady THEN dwStatusWord := dwStatusWord OR 16#00000800; END_IF;(* Bit 11: Export Header OK *)

(* Bits 16..20: Encode 5-bit FSM Operational Stage *)
dwStatusWord := dwStatusWord OR SHL(INT_TO_DWORD(nOperatingState AND 16#1F), 16);


(* =========================================================================
   32-BIT BIT-PACKED FAULT TRIP WORD (dwFaultWord)
   ========================================================================= *)
dwFaultWord := 16#00000000;
IF NOT bEmergencyStop THEN dwFaultWord := dwFaultWord OR 16#00000001; END_IF;        (* Bit 0: Emergency E-Stop Pushbutton *)
IF bAlarm_DP_HH THEN dwFaultWord := dwFaultWord OR 16#00000002; END_IF;              (* Bit 1: Membrane DP High-High (>200 mbar) *)
IF bAlarm_DP_LL THEN dwFaultWord := dwFaultWord OR 16#00000004; END_IF;              (* Bit 2: Membrane DP Low-Low (<-200 mbar) *)
IF bAlarm_O2inH2_HH THEN dwFaultWord := dwFaultWord OR 16#00000008; END_IF;          (* Bit 3: O2-in-H2 High-High (>15000 ppm) *)
IF bAlarm_H2inO2_HH THEN dwFaultWord := dwFaultWord OR 16#00000010; END_IF;          (* Bit 4: H2-in-O2 High-High (>15000 ppm) *)
IF bAlarm_Resist_LL THEN dwFaultWord := dwFaultWord OR 16#00000020; END_IF;          (* Bit 5: DI Water Resistivity Low-Low *)
IF bAlarm_StackTemp_HH THEN dwFaultWord := dwFaultWord OR 16#00000040; END_IF;       (* Bit 6: Stack Temp High-High (>82 C) *)
IF bAlarm_StackTemp_LL THEN dwFaultWord := dwFaultWord OR 16#00000080; END_IF;       (* Bit 7: Stack Temp Low-Low (<25 C) *)
IF bAlarm_CathLevel_HH THEN dwFaultWord := dwFaultWord OR 16#00000100; END_IF;       (* Bit 8: Cathode Level High-High (>88%) *)
IF bAlarm_CathLevel_LL THEN dwFaultWord := dwFaultWord OR 16#00000200; END_IF;       (* Bit 9: Cathode Level Low-Low (<12%) *)
IF bAlarm_CellVolt_HH THEN dwFaultWord := dwFaultWord OR 16#00000400; END_IF;        (* Bit 10: CVM Cell Overvoltage (>2.35 V) *)
IF bAlarm_CellVolt_LL THEN dwFaultWord := dwFaultWord OR 16#00000800; END_IF;        (* Bit 11: CVM Short Circuit (<1.15 V) *)
IF nDegradedMode_DiffPress = 0 THEN dwFaultWord := dwFaultWord OR 16#00001000; END_IF; (* Bit 12: DP All Sensors Failed *)
IF nDegradedMode_O2_in_H2 = 0 THEN dwFaultWord := dwFaultWord OR 16#00002000; END_IF;  (* Bit 13: O2-in-H2 All Sensors Failed *)
IF nDegradedMode_H2_in_O2 = 0 THEN dwFaultWord := dwFaultWord OR 16#00004000; END_IF;  (* Bit 14: H2-in-O2 All Sensors Failed *)
IF nDegradedMode_StackVolt = 0 THEN dwFaultWord := dwFaultWord OR 16#00008000; END_IF; (* Bit 15: Stack Volt All Sensors Failed *)
IF nDegradedMode_StackCurr = 0 THEN dwFaultWord := dwFaultWord OR 16#00010000; END_IF; (* Bit 16: Stack Curr All Sensors Failed *)
IF bAlarm_O2inH2_RoC THEN dwFaultWord := dwFaultWord OR 16#00020000; END_IF;        (* Bit 17: O2-in-H2 Rate of Change Trip *)
IF bAlarm_H2inO2_RoC THEN dwFaultWord := dwFaultWord OR 16#00040000; END_IF;        (* Bit 18: H2-in-O2 Rate of Change Trip *)


(* =========================================================================
   32-BIT BIT-PACKED WARNING WORD (dwWarningWord)
   ========================================================================= *)
dwWarningWord := 16#00000000;
IF bAlarm_DP_H THEN dwWarningWord := dwWarningWord OR 16#00000001; END_IF;           (* Bit 0: Membrane DP High (>120 mbar) *)
IF bAlarm_DP_L THEN dwWarningWord := dwWarningWord OR 16#00000002; END_IF;           (* Bit 1: Membrane DP Low (<-120 mbar) *)
IF bAlarm_O2inH2_H THEN dwWarningWord := dwWarningWord OR 16#00000004; END_IF;       (* Bit 2: O2-in-H2 High (>8000 ppm) *)
IF bAlarm_H2inO2_H THEN dwWarningWord := dwWarningWord OR 16#00000008; END_IF;       (* Bit 3: H2-in-O2 High (>8000 ppm) *)
IF bAlarm_Resist_L THEN dwWarningWord := dwWarningWord OR 16#00000010; END_IF;       (* Bit 4: DI Water Resistivity Low Warning *)
IF bAlarm_StackTemp_H THEN dwWarningWord := dwWarningWord OR 16#00000020; END_IF;    (* Bit 5: Stack Temp High (>75 C) *)
IF bAlarm_StackTemp_L THEN dwWarningWord := dwWarningWord OR 16#00000040; END_IF;    (* Bit 6: Stack Temp Low (<45 C) *)
IF bAlarm_CathLevel_H THEN dwWarningWord := dwWarningWord OR 16#00000080; END_IF;    (* Bit 7: Cathode Level High (>72%) *)
IF bAlarm_CathLevel_L THEN dwWarningWord := dwWarningWord OR 16#00000100; END_IF;    (* Bit 8: Cathode Level Low (<28%) *)
IF bAlarm_CellVolt_H THEN dwWarningWord := dwWarningWord OR 16#00000200; END_IF;     (* Bit 9: CVM Cell High Degradation (>2.18 V) *)
IF rN2SupplyPressure < 4.0 THEN dwWarningWord := dwWarningWord OR 16#00000400; END_IF; (* Bit 10: Nitrogen Supply Low *)
IF rDownstreamPipelinePressure > 32.0 THEN dwWarningWord := dwWarningWord OR 16#00000800; END_IF; (* Bit 11: Export Backpressure High *)


(* =========================================================================
   32-BIT BIT-PACKED SENSOR HEALTH & DEGRADATION WORD (dwSensorHealthWord)
   ========================================================================= *)
dwSensorHealthWord := 16#00000000;
IF bDiscrepancyTrip_StackVolt THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000001; END_IF; (* Bit 0: Volt Discrepancy *)
IF bDiscrepancyTrip_StackCurr THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000002; END_IF; (* Bit 1: Curr Discrepancy *)
IF bDiscrepancyTrip_CathLevel THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000004; END_IF; (* Bit 2: Cath Lvl Discrepancy *)
IF bDiscrepancyTrip_AnodeLevel THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000008; END_IF;(* Bit 3: Anode Lvl Discrepancy *)
IF bDiscrepancyTrip_DiffPress THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000010; END_IF; (* Bit 4: DP Discrepancy *)
IF bDiscrepancyTrip_O2_in_H2 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000020; END_IF;  (* Bit 5: O2-in-H2 Discrepancy *)
IF bDiscrepancyTrip_H2_in_O2 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000040; END_IF;  (* Bit 6: H2-in-O2 Discrepancy *)
IF bDiscrepancyTrip_StackTemp THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000080; END_IF; (* Bit 7: Temp Discrepancy *)
IF bDiscrepancyTrip_DI_Resist THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000100; END_IF; (* Bit 8: Resist Discrepancy *)

IF nDegradedMode_DiffPress < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000200; END_IF; (* Bit 9: DP Degraded *)
IF nDegradedMode_O2_in_H2 < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000400; END_IF;  (* Bit 10: O2-in-H2 Degraded *)
IF nDegradedMode_H2_in_O2 < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00000800; END_IF;  (* Bit 11: H2-in-O2 Degraded *)
IF nDegradedMode_StackTemp < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00001000; END_IF; (* Bit 12: Temp Degraded *)
IF nDegradedMode_CathLevel < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00002000; END_IF; (* Bit 13: Level Degraded *)
IF nDegradedMode_StackVolt < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00004000; END_IF; (* Bit 14: Volt Degraded *)
IF nDegradedMode_StackCurr < 3 THEN dwSensorHealthWord := dwSensorHealthWord OR 16#00008000; END_IF; (* Bit 15: Curr Degraded *)
""")

    # -------------------------------------------------------------------------
    # 10. CLOSING DECLARATION
    # -------------------------------------------------------------------------
    code_parts.append("""
END_FUNCTION_BLOCK
""")

    return "".join(code_parts)

def save_and_validate():
    raw_st = build_iec_code().strip()
    # Format with triple backtick fences strictly
    fence_open = "```iec-st\n"
    fence_close = "\n```"
    code_with_fence = fence_open + raw_st + fence_close

    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Green Hydrogen & Clean Energy Transition (Tier 1 Priority Sector): 20 MW Multi-Stack PEM Water Electrolysis Facility with Dynamic De-ionized Water Circulation Loop, High-Current DC Thyristor Rectifier Power Management, Anode Oxygen & Cathode Hydrogen Gas-Liquid Separator Vessel Liquid Level 3-Element Cascade, High-Pressure Differential Pressure Cell Balancing Across PEM Catalyst-Coated Membranes (< 200 mbar delta-P), and Trace Oxygen-in-Hydrogen (O2-in-H2) & Hydrogen-in-Oxygen (H2-in-O2) Safety Gas Analyzers.**

**Function Block Name**: `FB_Energy_Hydrogen_PEM_Electrolyzer_SafetyBalance`

**Engineering Context & Operational Architecture**:
1. Multi-Stack Electrolyzer Skid & Power Rectifier:
   - 20 MW total nominal electrical rating across 4 high-pressure Proton Exchange Membrane (PEM) cell stacks.
   - 12-pulse/24-pulse thyristor rectifier power conversion delivering up to 8.5 kA DC per stack with active harmonic mitigation and fast renewable ramp-following (< 5%/s slew rate).
   - Cell Voltage Monitoring (CVM) with multi-channel electrochemical polarization tracking (1.4 V to 2.3 V per cell) and pinhole/degradation anomaly detection.
2. De-Ionized (DI) Water Circulation & Thermal Management:
   - Anode circulation loop providing stoichiometric reactant water and stack core heat dissipation.
   - Redundant variable-speed DI circulation pumps, plate heat exchangers, 3-way modulating bypass temperature control valves (55 °C to 75 °C operating range), and continuous online resistivity monitoring (> 18.0 MOhm-cm threshold with mixed-bed resin polishing bypass).
3. Gas-Liquid Separators & 3-Element Level Control Cascade:
   - Anode O2 and Cathode H2 high-pressure separation vessels separating entrained liquid water from product gases.
   - 3-element cascade level regulation incorporating vessel liquid level, water inlet mass flow, and drain/feed mass flow to eliminate swell and shrink effects during rapid pressure and load transients.
4. High-Pressure Differential Pressure Cell Balancing:
   - Anode and cathode gas manifolds operating at up to 30 bar(g).
   - Dynamic membrane differential pressure control maintaining |P_H2 - P_O2| < 150 mbar (trip threshold at 200 mbar) via high-speed dome-loaded back-pressure control valves to prevent mechanical tear or rupture of the ultra-thin catalyst-coated membranes (CCM).
5. Cross-Permeation Gas Safety Analyzers:
   - 2oo3 Triple Modular Redundancy (TMR) thermal conductivity (TCD) and optical laser absorption (TDLAS) analyzers monitoring trace O2-in-H2 and trace H2-in-O2.
   - Rigorous safety interlocks executing fast rampdown and emergency nitrogen purge upon approaching 1.5% vol LEL limits (with flammability limit at 4.0% vol).
6. 8-State Cyber-Physical Discrete State-Space Model (x[k+1] = A x[k] + B u[k] + E d[k]):
   - 8 states: Cell overpotential, Hydrogen production rate, Membrane hydration water activity, Stack coolant temperature, Cathode separator liquid level, Membrane differential pressure, Trace O2-in-H2 gas concentration, and DC current density.
   - 8 control inputs: Rectifier DC current command, DI circulation pump speed, Coolant 3-way valve position, Separator liquid drain valve, H2 back-pressure valve, O2 back-pressure valve, Mixed-bed polishing valve, and Nitrogen inerting purge valve.
   - 4 disturbance inputs: Renewable grid power ramp request, DI water supply feed temperature, Downstream hydrogen pipeline back-pressure, and Ambient cooling water temperature.
7. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) solved via Projected Gradient Descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
8. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Operational states: Nitrogen Inerting Purge, DI Water Resistivity Qualification, System Pre-pressurization, Stack Polarization Conditioning, Warmup Ramp Heating, Renewable Ramp Following, Peak Generation (30 bar H2), Turndown Low-Power Reserve, Membrane DP Stabilization, Controlled Rampdown Shutdown, Stack Depolarization Cooldown, Post-Shutdown N2 Safety Flush, and Emergency Fast Trip Vent.
9. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance deadbands and 32-bit status, fault, warning, and sensor health words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Energy_Hydrogen_PEM_Electrolyzer_SafetyBalance` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": code_with_fence}
        ]
    }

    file_id = uuid.uuid4().hex[:8]
    output_path = f"data/swarm_raw/agent_{file_id}.json"
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"File successfully created: {output_path}")
    print(f"Assistant content character count: {len(code_with_fence)}")
    return output_path

if __name__ == "__main__":
    path = save_and_validate()
    print(f"Now validating {path}...")
    import validate_iec
    errs = validate_iec.validate_json_file(path)
    if errs:
        print("Validation FAILED:", errs)
        sys.exit(1)
    else:
        print("Validation PASSED PERFECTLY with 0 errors!")
