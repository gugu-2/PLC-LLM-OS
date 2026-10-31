import json
from generate_packaging_st import build_packaging_block

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: End-of-Line High-Speed Robotic Case Palletizing Cell & Cold Stretch Hooder Applicator. Multi-line carton conveyor collation, 4-axis articulated robotic vacuum gripper pattern generation (interlocking layer formation), pallet lift turntable rotation, tubular stretch film pneumatic/hydraulic 4-finger pre-stretch expansion, and vertical hood sleeve descent (Siemens S7-1500 / Fanuc / Krones).**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Packaging_RoboticPalletizer_StretchHooder
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [mbar], [mm], [kg], [N], [deg], [m/s], [rad/s], [s])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 50,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Packaging_RoboticPalletizer_StretchHooder
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open("data/swarm_raw/agent_9007723a.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Packaging Robotic Palletizer StretchHooder | File: data/swarm_raw/agent_9007723a.json | Chars: <count>"""

st_code = build_packaging_block()
assistant_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_9007723a.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2, ensure_ascii=False)

print(f"Saved {len(assistant_content)} characters to {target_file}")
