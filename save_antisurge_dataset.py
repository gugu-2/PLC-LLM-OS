# save_antisurge_dataset.py
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_antisurge_st import build_antisurge_block

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Multi-Stage Centrifugal Gas Compressor Dynamic Surge Line Observer & Fast Recycle Valve Loop. Distance from surge limit line (SLL), molecular weight / polytropic head observer, fast-opening recirculation valve (< 300 ms full stroke) with dynamic deceleration ramp, and 2oo3 TMR pressure/temperature voting (Emerson DeltaV SIS / Triconex TMR 2oo3 architecture).**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Turbomachinery_CentrifugalCompressor_DynamicAntiSurge
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [mbar], [rpm], [mm/s], [kg/kmol], [%], [s])
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
FUNCTION_BLOCK FB_Turbomachinery_CentrifugalCompressor_DynamicAntiSurge
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_b0089a0c.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Turbomachinery Dynamic AntiSurge | File: data/swarm_raw/agent_b0089a0c.json | Chars: <count>"""

st_code = build_antisurge_block()
assistant_code = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_code}
    ]
}

filename = "data/swarm_raw/agent_b0089a0c.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Saved dataset to {filename}")
print(f"Assistant content character count: {len(assistant_code)}")
