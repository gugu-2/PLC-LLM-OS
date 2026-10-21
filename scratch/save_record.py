# scratch/save_record.py
import json
import uuid
import sys
import os

sys.path.insert(0, 'scratch')
import build_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Advanced Plasma Arc Waste-to-Energy Gasification (5,000°C Core, 1.2 MW DC Torch): Dynamic Steam-Oxygen Gasification Stoichiometric Syngas (CO/H2) Ratio Regulation, Slag Taphole Induction Freeze-Lining Thermal Equilibrium, and High-Temperature Ceramic Candle Filter Pulsed-Jet Backwash**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_PlasmaGasification_SyngasRatio_ChokeSync
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [deg C], [kW], [Nm3/h], [bar], [mol/mol], [MJ/Nm3], [mbar], [kg/h])
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
FUNCTION_BLOCK FB_PlasmaGasification_SyngasRatio_ChokeSync
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Advanced Plasma Arc Waste-to-Energy Gasification (5,000°C Core, 1.2 MW DC Torch): Dynamic Steam-Oxygen Gasification Stoichiometric Syngas (CO/H2) Ratio Regulation, Slag Taphole Induction Freeze-Lining Thermal Equilibrium, and High-Temperature Ceramic Candle Filter Pulsed-Jet Backwash"""

raw_code = build_code.build_iec_code()
code = f"```iec-st\n{raw_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False)

print(f"Successfully saved to {filename}")
print(f"File size: {os.path.getsize(filename)} bytes")
