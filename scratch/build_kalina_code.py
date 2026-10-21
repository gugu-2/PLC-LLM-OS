# -*- coding: utf-8 -*-
"""
Full builder script for FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine.
Generates the comprehensive IEC 61131-3 Structured Text block.
"""

import json
import uuid
import re
import os

prompt_text = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Geothermal Binary Kalina Cycle Power Generation (Ammonia-Water, 165°C Brine): Variable Working Fluid Concentration Dynamic Fractionation Distillation, Variable-Geometry Radial Inflow Turbine Synchronous Governor Tuning, Recuperator Preheater Condensation Float Balance, and Non-Condensable Gas Purge Vacuum Lock**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [deg C], [bar], [kg/s], [mol/mol], [rpm], [kW], [kPa], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 60,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Geothermal Binary Kalina Cycle Power Generation (Ammonia-Water, 165°C Brine): Variable Working Fluid Concentration Dynamic Fractionation Distillation, Variable-Geometry Radial Inflow Turbine Synchronous Governor Tuning, Recuperator Preheater Condensation Float Balance, and Non-Condensable Gas Purge Vacuum Lock"""

parts = []

# PART 1: FUNCTION BLOCK DECLARATION AND ARCHITECTURE HEADER
parts.append("""FUNCTION_BLOCK FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
(*
 ====================================================================================================
  PROJECT:       165.0°C ENTHALPY GEOTHERMAL BRINE BINARY KALINA CYCLE POWER GENERATION SYSTEM
  MODULE:        FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
  DISCIPLINE:    CYBER-PHYSICAL AUTOMATION / ADVANCED PROCESS CONTROL / TURBOMACHINERY & THERMODYNAMICS
  STANDARDS:     IEC 61131-3 3RD EDITION, IEC 61508 (SIL-3 HARDWARE/SOFTWARE), API 612 / API 670, ASME PTC 46
  AUTHOR:        LUMINA AI CLOUD SWARM - PRINCIPAL AUTOMATION FELLOW & CPS CHAIR (V7 MAX)
  SYSTEM CLASS:  KALINA CYCLE SYSTEM 11 (KCS-11) WITH DYNAMIC BASIC WORKING FLUID COMPOSITION SHIFT
  HEAT SOURCE:   GEOTHERMAL PRESSURIZED LIQUID BRINE AT 165.0°C (18.5 BAR, 140.0 KG/S NOMINAL FLOW)
  EXPANDER TYPE: VARIABLE-GEOMETRY RADIAL INFLOW TURBINE (VGRIT) WITH ACTIVE NOZZLE GUIDE VANE (VGV)
  WORKING FLUID: ZEOTROPIC AMMONIA-WATER MIXTURE (NH3 / H2O) WITH ADAPTIVE BASIC FRACTION (0.70 TO 0.85)
 ----------------------------------------------------------------------------------------------------
  CORE ARCHITECTURAL AND THERMODYNAMIC OBJECTIVES:
   1. Dynamic Fractionation Distillation & VLE Balancing:
      Exploits the variable boiling glide of the binary NH3-H2O mixture to match the heat release 
      profile of 165°C geothermal brine, minimizing triangular exergy destruction in the evaporator.
      Controls separation of the superheated rich vapor stream (x_v = 0.92 to 0.98 mol/mol) feeding 
      the turbine expander and lean liquid stream (x_l = 0.40 to 0.55 mol/mol) recycled to recuperators.
   2. Variable Working Fluid Concentration Dynamic Shifting:
      Continuously tracks ambient wet-bulb temperature and cooling tower heat rejection capability. 
      Dynamically trims the basic working fluid concentration (x_b) via distillation inventory shift 
      between low-pressure receiver and high-pressure separator to maximize cycle net work output.
   3. Variable-Geometry Radial Inflow Turbine (VGRIT) Synchronous Governor Tuning:
      Directs electro-hydraulic variable nozzle guide vane (VGV) positioning to maintain optimal 
      nozzle velocity ratio (u / c0 ~ 0.68 to 0.72) across varying brine thermal duty. Implements 
      high-precision synchronous speed governing with 4.0% droop characteristic, isochronous islanding, 
      and fast anti-overspeed bypass coordination during grid load rejection events.
   4. Recuperator Preheater Condensation Float Balance:
      Maintains rigorous multi-element dynamic liquid level equilibrium across the High-Temperature 
      Recuperator (HTR), Low-Temperature Recuperator (LTR), Preheater, and Separator Bottoms. 
      Prevents catastrophic vapor blow-through into liquid lines and liquid droplet carry-over into 
      the turbine expander blading via active float trim modulating valves.
   5. Non-Condensable Gas (NCG) Purge Vacuum Lock:
      Mitigates degradation of condenser/absorber overall heat transfer coefficient (U) caused by 
      dissolved non-condensable gas accumulation (N2, H2, CH4, CO2, and atmospheric ingress). 
      Executes an autonomous 6-phase differential pressure lock-hopper cycle equipped with a cold-water 
      ammonia scrubber to safely vent purified NCGs to atmosphere without ammonia emissions.
   6. Cyber-Physical Deterministic Model Predictive Control (MPC):
      Solves an embedded discrete-time 6-state, 4-control quadratic optimization problem at 50 ms scan 
      intervals using projected gradient descent with explicit Box constraints, rate limiters, 
      and analytical Hessian approximation.
   7. Triple Modular Redundancy (2oo3 TMR) Voting & SIL-3 Diagnostic Integrity:
      Performs real-time median voting, drift delta monitoring, and graceful sensor degradation 
      (2oo3 -> 1oo2 -> Fail-Safe Trip) across all safety-critical thermal, pressure, speed, and 
      concentration measurement channels.
 ====================================================================================================
*)
""")

print("Part 1 appended.")
