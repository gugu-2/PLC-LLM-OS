import json
import os
import sys

sys.path.insert(0, ".")
sys.path.insert(0, "scratch")

import test_gen

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electric Utility Grid Automated Substation Breaker & STATCOM Controllers (Rank #92). 3-phase high-voltage substation automation, SF6 gas-insulated circuit breaker contact arc extinguishing kinetics and dielectric recovery, synchronous point-on-wave switching, multi-shot auto-reclosing, sub-cycle directional overcurrent (<15 ms), loss-of-mains islanding detection (RoCoF/vector shift), ±100 MVAR Voltage Source Converter (VSC) STATCOM dq-frame reactive power compensation, power factor regulation, automated On-Load Tap Changer (OLTC) coordination, sub-synchronous resonance (SSR) damping, and 2oo3 TMR instrumentation.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_PowerGrid_SubstationBreaker_STATCOM with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

raw_st_code = test_gen.generate_st_code()
assistant_content = f"```iec-st\n{raw_st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
target_path = "data/swarm_raw/agent_a5b9123f.json"

with open(target_path, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2, ensure_ascii=False)

print(f"Successfully generated and wrote {target_path}")
print(f"Assistant content character count: {len(assistant_content)}")
