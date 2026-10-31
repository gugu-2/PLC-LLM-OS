import json
import os
import sys

# Ensure scratch is on path
sys.path.insert(0, os.path.abspath("scratch"))
from generate_cmp_dataset import build_cmp_iec_st

def main():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electronics & Semiconductor: 300mm Wafer Chemical Mechanical Planarization (CMP) & Pad Conditioning Tool. Multi-zone flexible membrane carrier head pressure distribution (Zone 1 center to Zone 7 retaining ring boundary), Preston's removal rate kinetics (MRR = kp * P * V), Arrhenius chemical etching acceleration, diamond pad conditioner oscillating sweep micro-wear, receding-horizon MPC active bladder pressure leveling (WIWNU < 1.5%), 2oo3 TMR optical spectro-reflectometry end-point detection (EPD), platen eddy current friction torque sensors, carrier differential membrane pressure transmitters, cleanroom sub-10nm master CMP FSM (wafer chuck load, slurry prime, head descent, soft-landing, high-pressure polish, overpolish trim, DI water megasonic rinse, N2 peel de-chuck), and ISA-18.2 multi-tiered alarm matrix.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Semiconductor_CMP_ChemicalMechanicalPlanarization_PadConditioner with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    code_body = build_cmp_iec_st()
    assistant_content = f"```iec-st\n{code_body}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    outfile = "data/swarm_raw/agent_4c8109bf.json"
    with open(outfile, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False)

    print(f"Successfully generated {outfile}")
    print(f"Assistant content character count: {len(assistant_content)}")

if __name__ == "__main__":
    main()
