# -*- coding: utf-8 -*-
"""
Save and validate dataset for FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber
"""
import sys
import os
import json
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

from an_granulation_assembler import assemble_an_granulation
from validate_iec import validate_json_file

def main():
    raw_st = assemble_an_granulation()
    fenced_code = f"```iec-st\n{raw_st}\n```"

    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Agrochemicals & Heavy Chemical Processing
- System: Ammonium Nitrate (AN) & NPK Industrial Fertilizer Granulation Complex: High-Capacity Rotary Granulation Drum ($D = 4.2$ m, $L = 18$ m, 120 t/h), Dual-Fluid Molten Slurry Spray Nozzle Atomization ($175 \\ ^\\circ\\text{C}$, 6.5 bar), Rotary Flighted Co-Current Dryer with Natural Gas Burner Air-to-Fuel Ratio Control, Counter-Current Fluidized Bed Granule Cooler (4-Chamber Active Aeration), Multi-Stage Tail-Gas Venturi Acid Scrubber ($\\Delta P$ regulation, pH neutralisation loop with continuous 93% nitric acid trim, particulate emissions $< 15 \\text{ mg/Nm}^3$), Granule Moisture/Crush Strength Observer, Oversize/Undersize Double-Deck Vibratory Screen Recycle Ratio Closed-Loop Balancing, and Thermal Runaway Decomposition Deluge Interlocks.
- Function Block Name: `FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing drum bed temperature, granule moisture, fluid bed cooling zones, scrubber acid concentration, and recycle ratio dynamics.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing granule size distribution deviation ($Q$), slurry spray valve adjustments ($R$), and scrubber emission spikes ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on bed temperature transmitters, scrubber differential pressure sensors, burner flame scanners, and stack particulate analyzers.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Emergency Deluge HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering purge, pre-heat, recycle loop establishment, slurry atomization start, continuous steady-state granulation, product specification adjustment, controlled ramp-down, and emergency deluge flood.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with `iec-st`.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`. Zero unmatched delimiters.
   - Zero summaries, zero placeholders (`// ... rest of code`).
4. Save directly as a standard JSON dataset to `data/swarm_raw/agent_<uuid>.json` containing `id`, `messages` (user prompt, assistant response with fenced iec-st code), and `metadata`. Validate with `python validate_iec.py` and report final character count."""

    agent_hex = uuid.uuid4().hex[:8]
    dataset_id = f"synthetic_v3_{agent_hex}"
    filename = f"data/swarm_raw/agent_{agent_hex}.json"

    record = {
        "id": dataset_id,
        "instruction": prompt,
        "input": "",
        "output": fenced_code,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": fenced_code}
        ],
        "metadata": {
            "domain": "Agrochemicals & Heavy Chemical Processing",
            "system": "Ammonium Nitrate (AN) & NPK Industrial Fertilizer Granulation Complex (120 t/h Capacity)",
            "block_name": "FB_Fertilizer_AmmoniumNitrate_Granulation_Scrubber",
            "raw_st_char_count": len(raw_st),
            "fenced_char_count": len(fenced_code),
            "generator": "Lumina V7 Max-Persona Swarm",
            "ast_parity_valid": True
        }
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to: {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    print(f"Assistant content character count: {len(fenced_code)}")

    # Validate saved file
    errors = validate_json_file(filename)
    if errors:
        print("VALIDATION FAILED with errors:")
        for e in errors:
            print("  -", e)
        sys.exit(1)
    else:
        print("PERFECT: JSON DATASET VALIDATION PASSED COMPLETELY!")
        return filename, len(fenced_code)

if __name__ == "__main__":
    main()
