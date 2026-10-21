# -*- coding: utf-8 -*-
"""
Save and validate the dataset record.
"""

import json
import uuid
import os
import generate_cryo_st

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Cryogenic Liquid Helium (4.2K to 1.8K) Superfluid Transition Cryostat: Sub-Lambda Point (T_lambda = 2.17 K) Pressure-Temperature Equilibrium, Joule-Thomson Valve Sub-Millibar Backpressure Regulation, Gorter-Mellink Superfluid Heat Flux Mutual Friction Transport Estimation, and Thermomechanical Fountain Effect Pressure Balancing**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_CryoHelium_SuperfluidHeII_LambdaTransition
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [K], [mbar], [g/s], [W/cm2], [mbar/s], [mm], [A], [V])
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
FUNCTION_BLOCK FB_CryoHelium_SuperfluidHeII_LambdaTransition
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Cryogenic Liquid Helium (4.2K to 1.8K) Superfluid Transition Cryostat: Sub-Lambda Point (T_lambda = 2.17 K) Pressure-Temperature Equilibrium, Joule-Thomson Valve Sub-Millibar Backpressure Regulation, Gorter-Mellink Superfluid Heat Flux Mutual Friction Transport Estimation, and Thermomechanical Fountain Effect Pressure Balancing"""

st_body = generate_cryo_st.generate_iec_st().strip()

# Wrap in triple backticks iec-st
code = f"```iec-st\n{st_body}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"SAVED_FILE={filename}")
print(f"Assistant length: {len(code)} characters")

# Verify the file can be loaded back
with open(filename, "r", encoding="utf-8") as f:
    loaded = json.load(f)

assert len(loaded["messages"]) == 2
assert loaded["messages"][0]["role"] == "user"
assert loaded["messages"][1]["role"] == "assistant"
assistant_text = loaded["messages"][1]["content"]
assert assistant_text.startswith("```iec-st\nFUNCTION_BLOCK FB_CryoHelium_SuperfluidHeII_LambdaTransition")
assert assistant_text.strip().endswith("END_FUNCTION_BLOCK\n```")
print("Validation PASSED successfully!")
