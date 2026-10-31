import json
import build_agent_3a819c42 as b

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices ($A, B, C, D$), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electronics & Semiconductor: 12-Zone Convection Reflow Soldering Oven (SAC305 Lead-Free Profile) with Dynamic N2 Inerting & Board Collation Tracking**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Electronics_ReflowOven_12Zone_ThermalProfiling
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [m/min], [deg C], [ppm], [bar], [mm], [A], [RPM], [Hz])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features.
4. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Electronics_ReflowOven_12Zone_ThermalProfiling
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_3a819c42.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
5. REPLY with: EVOLUTION COMPLETE: Electronics & Semiconductor: 12-Zone Convection Reflow Soldering Oven (SAC305 Lead-Free Profile) with Dynamic N2 Inerting & Board Collation Tracking"""

st_code = b.build_full_st_code()
content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": content}
    ]
}

target_file = "data/swarm_raw/agent_3a819c42.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2, ensure_ascii=False)

print(f"Successfully wrote {target_file} with {len(content)} chars in assistant content.")
