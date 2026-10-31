# -*- coding: utf-8 -*-
import json
import os
from generate_continuous_tunnel_washer import generate_iec_st

def save_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Laundry Continuous Batch Tunnel Washers & High-Speed Ironers (Rank #83). Multi-compartment counter-flow water recycling, thermal energy recovery heat exchangers, continuous linen batch Archimedean screw transfer, 40-bar hydraulic extraction press ram deceleration and fabric shear avoidance, cake breakup shaker, and gas-fired multi-roll chest ironer tension synchronization.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_CommercialLaundry_ContinuousTunnelWasher_Extractor with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    code_st = generate_iec_st().strip()
    assistant_content = f"```iec-st\n{code_st}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_path = os.path.join("data", "swarm_raw", "agent_f58201bc.json")
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully saved to {target_path}")
    print(f"Assistant content character count: {len(assistant_content)}")

if __name__ == "__main__":
    save_dataset()
