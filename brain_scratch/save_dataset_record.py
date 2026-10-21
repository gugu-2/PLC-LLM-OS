import json
import uuid
import os
import sys

# Import the builder
sys.path.append("brain_scratch")
from generate_full_dle import build_iec_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Supercritical Geothermal Brine Direct Lithium Extraction (DLE, 220°C, 25 bar): Multi-Column Sorbent (Al-Li / Ti-O) Bed Carousel Dynamic Adsorption Front Tracking, High-Pressure Acid Elution Wash Profile, Silica Scaling Polymerization Seed Inhibitor Dosing, and Hydraulic Energy Recovery Turbine Speed Control**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m3/h], [mg/L], [pH], [rpm], [kW], [mS/cm])
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
FUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Supercritical Geothermal Brine Direct Lithium Extraction (DLE, 220°C, 25 bar): Multi-Column Sorbent (Al-Li / Ti-O) Bed Carousel Dynamic Adsorption Front Tracking, High-Pressure Acid Elution Wash Profile, Silica Scaling Polymerization Seed Inhibitor Dosing, and Hydraulic Energy Recovery Turbine Speed Control"""

raw_st = build_iec_code()
code = f"```iec-st\n{raw_st}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"SUCCESS: Saved {len(code)} chars of assistant code to {filename}")
print(f"File size on disk: {os.path.getsize(filename)} bytes")
