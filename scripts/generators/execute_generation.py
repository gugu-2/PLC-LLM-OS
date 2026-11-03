# Master execution script to assemble, validate, and save the dataset
import json
import uuid
import os
import re

import gen_part1
import gen_part2
import gen_part3
import gen_part4
import gen_part5
import gen_part6
import gen_part7
import gen_part8

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Renewable Power Generation & Heavy Hydro Turbomachinery: 450 MW Francis Hydroelectric Turbine & High-Head Penstock Surge Tank with Dynamic Hydraulic Water Hammer Surge Arrestor & Guide Vane (Wicket Gate) Servomotor Governing**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_PowerGen_Hydro_FrancisTurbine_WaterHammerSurge
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [%], [m3/s], [deg C], [rpm], [MW], [mm/s], [Hz])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 65,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_PowerGen_Hydro_FrancisTurbine_WaterHammerSurge
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Renewable Power Generation & Heavy Hydro Turbomachinery: 450 MW Francis Hydroelectric Turbine & High-Head Penstock Surge Tank with Dynamic Hydraulic Water Hammer Surge Arrestor & Guide Vane (Wicket Gate) Servomotor Governing"""

raw_st_code = (
    gen_part1.get_header().strip() + "\n" +
    gen_part2.get_var_input().strip() + "\n" +
    gen_part2.get_var_output().strip() + "\n" +
    gen_part3.get_var_internal().strip() + "\n\n" +
    gen_part4.get_phase1_tmr_voting().strip() + "\n\n" +
    gen_part5.get_phase2_state_space().strip() + "\n\n" +
    gen_part6.get_phase3_mpc_control().strip() + "\n\n" +
    gen_part7.get_phase4_fsm().strip() + "\n\n" +
    gen_part8.get_phase5_alarms().strip()
)

# Format assistant response with triple backticks and iec-st
assistant_content = f"```iec-st\n{raw_st_code}\n```"

# Validation
clean_code = re.sub(r'\(\*.*?\*\)', '', raw_st_code, flags=re.DOTALL)
if_count = len(re.findall(r'\bIF\b', clean_code))
end_if_count = len(re.findall(r'\bEND_IF;', clean_code))
case_count = len(re.findall(r'\bCASE\b', clean_code))
end_case_count = len(re.findall(r'\bEND_CASE;', clean_code))
for_count = len(re.findall(r'\bFOR\b', clean_code))
end_for_count = len(re.findall(r'\bEND_FOR;', clean_code))

var_in = len(re.findall(r'\bVAR_INPUT\b', clean_code))
var_out = len(re.findall(r'\bVAR_OUTPUT\b', clean_code))
var_only = len(re.findall(r'\bVAR\b', clean_code))
end_vars = len(re.findall(r'\bEND_VAR\b', clean_code))

print("=== VALIDATION REPORT ===")
print(f"IF / END_IF: {if_count} / {end_if_count}")
print(f"CASE / END_CASE: {case_count} / {end_case_count}")
print(f"FOR / END_FOR: {for_count} / {end_for_count}")
print(f"VAR blocks (IN/OUT/VAR/END): {var_in} / {var_out} / {var_only} / {end_vars}")
print(f"Raw ST character count: {len(raw_st_code)}")
print(f"Assistant total character count: {len(assistant_content)}")

assert if_count == end_if_count, f"IF parity error: {if_count} != {end_if_count}"
assert case_count == end_case_count, f"CASE parity error: {case_count} != {end_case_count}"
assert for_count == end_for_count, f"FOR parity error: {for_count} != {end_for_count}"
assert var_in == 1 and var_out == 1 and var_only == 1 and end_vars == 3, "VAR parity error"
assert raw_st_code.startswith("FUNCTION_BLOCK FB_PowerGen_Hydro_FrancisTurbine_WaterHammerSurge")
assert raw_st_code.endswith("END_FUNCTION_BLOCK")
assert len(assistant_content) >= 60000, f"Length too short: {len(assistant_content)}"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
output_filename = f"data/swarm_raw/agent_{agent_id}.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(output_filename)
print(f"SUCCESSFULLY SAVED DATASET: {output_filename}")
print(f"File size on disk: {file_size} bytes")
print(f"Agent ID: {agent_id}")
