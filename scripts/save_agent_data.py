# -*- coding: utf-8 -*-
"""
Execution and verification script to save the generated IEC 61131-3 dataset record
into data/swarm_raw/agent_<uuid>.json
"""

import json
import uuid
import os
import re
from build_awe_code import build_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Megawatt High-Pressure Alkaline Water Electrolysis (AWE, 30 bar, 80°C, 30 wt% KOH): Dynamic Anode-Cathode Differential Pressure Cross-Permeation Nulling, Gas-Liquid Separator Lye Level Float Balancing, Catalytic De-Oxo Hydrogen Purification Thermal Sync, and Fast Renewable Power Ramp Rate Limiting**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Hydrogen_AWE_HighPressure_SeparatorSync
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [mbar], [deg C], [kA], [V], [m3/h], [%], [ppm])
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
FUNCTION_BLOCK FB_Hydrogen_AWE_HighPressure_SeparatorSync
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Megawatt High-Pressure Alkaline Water Electrolysis (AWE, 30 bar, 80°C, 30 wt% KOH): Dynamic Anode-Cathode Differential Pressure Cross-Permeation Nulling, Gas-Liquid Separator Lye Level Float Balancing, Catalytic De-Oxo Hydrogen Purification Thermal Sync, and Fast Renewable Power Ramp Rate Limiting"""

# Generate the Structured Text code
raw_code = build_code().strip()
wrapped_code = f"```iec-st\n{raw_code}\n```"

# Quality Checks
lines = raw_code.split('\n')
assert lines[0].strip().startswith("FUNCTION_BLOCK FB_Hydrogen_AWE_HighPressure_SeparatorSync"), f"Failed start line: {lines[0]}"
assert lines[-1].strip() == "END_FUNCTION_BLOCK", f"Failed end line: {lines[-1]}"
assert "VAR_INPUT" in raw_code and "END_VAR" in raw_code
assert "VAR_OUTPUT" in raw_code
assert "VAR" in raw_code
assert "CASE iState OF" in raw_code and "END_CASE;" in raw_code

ifs = len(re.findall(r'\bIF\b', raw_code))
end_ifs = len(re.findall(r'\bEND_IF\b', raw_code))
cases = len(re.findall(r'\bCASE\b', raw_code))
end_cases = len(re.findall(r'\bEND_CASE\b', raw_code))
fors = len(re.findall(r'\bFOR\b', raw_code))
end_fors = len(re.findall(r'\bEND_FOR\b', raw_code))

print(f"Parity: IF: {ifs} vs END_IF: {end_ifs}")
print(f"Parity: CASE: {cases} vs END_CASE: {end_cases}")
print(f"Parity: FOR: {fors} vs END_FOR: {end_fors}")
assert ifs == end_ifs, f"IF parity mismatch: {ifs} != {end_ifs}"
assert cases == end_cases, f"CASE parity mismatch: {cases} != {end_cases}"
assert fors == end_fors, f"FOR parity mismatch: {fors} != {end_fors}"

print(f"Raw code length: {len(raw_code)}")
print(f"Wrapped code length: {len(wrapped_code)}")
assert len(wrapped_code) >= 60000, f"Code too short: {len(wrapped_code)}"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": wrapped_code}
    ]
}

agent_id = uuid.uuid4().hex[:8]
output_filename = f"data/swarm_raw/agent_{agent_id}.json"

os.makedirs("data/swarm_raw", exist_ok=True)
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Saved successfully to {output_filename}")

# Verify file reading and parsing
with open(output_filename, "r", encoding="utf-8") as f:
    verified = json.load(f)

assert len(verified["messages"]) == 2
assert verified["messages"][0]["role"] == "user"
assert verified["messages"][1]["role"] == "assistant"
assert verified["messages"][1]["content"].startswith("```iec-st\nFUNCTION_BLOCK FB_Hydrogen_AWE_HighPressure_SeparatorSync")
assert verified["messages"][1]["content"].endswith("END_FUNCTION_BLOCK\n```")
print("VERIFICATION COMPLETE: File is 100% compliant and valid!")
