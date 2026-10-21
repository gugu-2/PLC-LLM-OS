# -*- coding: utf-8 -*-
"""
Assemble and verify script for FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine.
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

# Read header from build_kalina_code.py
part1_header = """FUNCTION_BLOCK FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine
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
"""

part2_io = open("scratch/part2_io.txt", "r", encoding="utf-8").read()
part3_var = open("scratch/part3_var.txt", "r", encoding="utf-8").read()
part4_logic_a = open("scratch/part4_logic_a.txt", "r", encoding="utf-8").read()
part4_logic_b = open("scratch/part4_logic_b.txt", "r", encoding="utf-8").read()
part4_logic_c = open("scratch/part4_logic_c.txt", "r", encoding="utf-8").read()

raw_code = f"{part1_header}\n{part2_io}\n{part3_var}\n{part4_logic_a}\n{part4_logic_b}\n{part4_logic_c}".strip()

# Verification checks
code_lines = raw_code.splitlines()
print(f"Total lines of code: {len(code_lines)}")
first_line = code_lines[0].strip()
last_line = code_lines[-1].strip()
print(f"First line: '{first_line}'")
print(f"Last line:  '{last_line}'")

assert first_line == "FUNCTION_BLOCK FB_GeothermalKalina_AmmoniaWater_ExpansionTurbine", f"First line mismatch: {first_line}"
assert last_line == "END_FUNCTION_BLOCK", f"Last line mismatch: {last_line}"

# Check required physical units in VAR_INPUT
required_units = ["[deg C]", "[bar]", "[kg/s]", "[mol/mol]", "[rpm]", "[kW]", "[kPa]", "[%]"]
var_input_match = re.search(r"VAR_INPUT(.*?)END_VAR", raw_code, re.DOTALL)
assert var_input_match, "VAR_INPUT block not found!"
var_input_text = var_input_match.group(1)
for u in required_units:
    assert u in var_input_text, f"Unit {u} missing from VAR_INPUT!"
print("All 8 physical units confirmed in VAR_INPUT.")

# Check required VAR_OUTPUT
var_output_match = re.search(r"VAR_OUTPUT(.*?)END_VAR", raw_code, re.DOTALL)
assert var_output_match, "VAR_OUTPUT block not found!"
var_output_text = var_output_match.group(1)
output_vars = [line for line in var_output_text.splitlines() if ":" in line and not line.strip().startswith("(*")]
print(f"Number of VAR_OUTPUT declarations: {len(output_vars)} (required min 7)")
assert len(output_vars) >= 7, "Insufficient VAR_OUTPUT variables!"

# Check VAR block
var_match = re.search(r"\nVAR\s*(.*?)END_VAR", raw_code, re.DOTALL)
assert var_match, "VAR block not found!"
print("VAR block confirmed.")

# Check CASE statements
case_count = len(re.findall(r"\bCASE\b", raw_code))
end_case_count = len(re.findall(r"\bEND_CASE\b", raw_code))
print(f"CASE count: {case_count}, END_CASE count: {end_case_count}")
assert case_count == end_case_count, f"CASE/END_CASE mismatch: {case_count} vs {end_case_count}"
assert case_count >= 1, "At least one CASE machine required!"

# Check IF statements parity
# Count IF occurrences that open an IF block (IF ... THEN)
# Note: ELSIF does not open a new block, it continues an existing IF
if_open = len(re.findall(r"(?<!ELS)\bIF\b", raw_code))
if_close = len(re.findall(r"\bEND_IF\b", raw_code))
print(f"IF count: {if_open}, END_IF count: {if_close}")
assert if_open == if_close, f"IF/END_IF parity mismatch: {if_open} vs {if_close}"

# Format assistant response with TRIPLE backticks and iec-st
full_assistant_content = f"```iec-st\n{raw_code}\n```"
char_count = len(full_assistant_content)
print(f"Full assistant content length: {char_count} characters (target: >= 3500, ideally 60,000 - 85,000+)")
assert char_count >= 3500, f"Length {char_count} too short!"

# Check Triple backticks
assert full_assistant_content.startswith("```iec-st\n"), "Assistant content must start with ```iec-st"
assert full_assistant_content.endswith("\n```"), "Assistant content must end with ```"
assert not full_assistant_content.startswith("`iec-st"), "Must not start with single backtick"

# Save using exact required python format
uid = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{uid}.json"

record = {
    "messages": [
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": full_assistant_content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Successfully saved to {filename}")

# Re-read and test JSON validity
with open(filename, "r", encoding="utf-8") as f:
    loaded = json.load(f)
assert len(loaded["messages"]) == 2
assert loaded["messages"][0]["role"] == "user"
assert loaded["messages"][1]["role"] == "assistant"
assert len(loaded["messages"][1]["content"]) == char_count

print("JSON record verified successfully!")
print(f"AGENT ID: {uid}")
