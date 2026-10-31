# save_mining_dataset.py
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_mining_st import build_mining_block

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: 25-Kilometer Continuous Overland Bulk Ore Conveyor Network. Multi-drive master-follower torque load sharing across 4 x 2,500 kW medium-voltage VFDs, dynamic hydraulic take-up trolley belt tension regulation (preventing belt wave oscillation and sag), belt rip continuous ultrasonic detection, and chute plug level prevention (Rockwell ControlLogix 5580 / ABB Mining PAC).**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Mining_OverlandConveyor_MultiDriveTorque
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [kN], [m/s], [%], [rpm], [m], [bar], [tons/h], [s])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 50,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Mining_OverlandConveyor_MultiDriveTorque
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_7a772101.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Mining Overland Conveyor | File: data/swarm_raw/agent_7a772101.json | Chars: <count>"""

st_code = build_mining_block()
assistant_code = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_code}
    ]
}

filename = "data/swarm_raw/agent_7a772101.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Saved dataset to {filename}")
print(f"Assistant content character count: {len(assistant_code)}")
