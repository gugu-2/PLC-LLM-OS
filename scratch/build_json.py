import json
import os
import sys

sys.path.append(r"c:\Users\majip\Downloads\LLM REASEARCH\scratch")
from generate_dataset_628a5bc7 import generate_iec_st

st_code = generate_iec_st()
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Medical Device Automated Syringe Assembly & Cleanroom Needle Bonding (Rank #90). 24-station direct-drive rotary dial indexing dynamics, UV adhesive capillary meniscus flow, piezo dispenser droplet volume transients, MPC dial servo settling time minimization at 120 parts/min, UV LED curing radiometric irradiance pacing, cannula insertion force curve optimization, 2oo3 TMR voting (laser orientation, pull-test load cells, ISO Class 5 laminar airflow velocity), high-speed assembly FSM (barrel singulation, cannula insertion, micro-dispensing, multi-angle UV cure, vision inspection, silicone spray, plunger insertion, bad part reject), and ISA-18.2 multi-tiered alarm matrix.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_MedicalDevice_Cleanroom_SyringeAssembly_NeedleBonding with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

assistant_content = "```iec-st\n" + st_code + "\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw\agent_628a5bc7.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully generated {target_file}")
print(f"Assistant content length: {len(assistant_content)}")
print(f"Assistant starts with: {repr(assistant_content[:20])}")
print(f"Assistant ends with: {repr(assistant_content[-20:])}")
