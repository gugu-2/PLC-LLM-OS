import json
import build_full_thermoform

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Plastics & Polymer Processing: 4-Station Rotary Carousel Heavy Sheet Thermoforming Machine (Automotive Door Trims / Refrigerator Liners) with Multi-Zone Quartz Radiant Heating & Servo Plug Assist.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Plastics_RotaryThermoforming_MultiStation with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

st_code = build_full_thermoform.build_full_dataset()
assistant_content = "```iec-st\n" + st_code + "\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_7c9104ba.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully saved {target_file} with content length {len(assistant_content)}")
