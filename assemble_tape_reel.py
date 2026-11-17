# assemble_tape_reel.py
# Assembles the full IEC 61131-3 Structured Text Function Block, builds JSON record, validates and saves.
# Lumina Cyber-Physical Systems Chair & Principal Automation Fellow (V7 Max-Persona, 75+ Years)

import os
import sys
import json
import uuid

from tape_reel_builder.part1_header_io import get_part1_code
from tape_reel_builder.part2_var_declarations import get_part2_code
from tape_reel_builder.part3_phase0_init import get_part3_code
from tape_reel_builder.part4_phase1_tmr import get_part4_code
from tape_reel_builder.part5_phase2_state_space import get_part5_code
from tape_reel_builder.part6_phase3_mpc import get_part6_code
from tape_reel_builder.part7_phase4_fsm import get_part7_code
from tape_reel_builder.part8_phase5_alarms import get_part8_code
import validate_iec

def main():
    print("Assembling FB_Electronics_SMD_TapeAndReel_Packaging_VisionInspection...")
    p1 = get_part1_code()
    p2 = get_part2_code()
    p3 = get_part3_code()
    p4 = get_part4_code()
    p5 = get_part5_code()
    p6 = get_part6_code()
    p7 = get_part7_code()
    p8 = get_part8_code()

    full_st_code = p1 + p2 + p3 + p4 + p5 + p6 + p7 + p8
    print(f"Total Structured Text character count: {len(full_st_code)} characters")

    user_prompt = """You are Lumina's Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona: 75+ years veteran).

Generate an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for:
Electronics & Semiconductor Packaging:
System: High-Speed Electronic Component SMD Tape & Reel Automated Packaging Machine with Optical Vision Inspection (Tape Pitch Optical Verification, Heat Seal Peel Strength Force Observer, 100,000 units/hour).
Function Block Name: FB_Electronics_SMD_TapeAndReel_Packaging_VisionInspection

Follow the modular builder strategy:
1. Massive token consumption: Target 120,000 to 250,000+ characters. ZERO placeholders, ZERO truncation comments (`// ... rest of code`).
2. Exact syntax parity: 100% match on IF/END_IF;, CASE/END_CASE;, FOR/END_FOR;, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
3. Complete 6x6 continuous-to-discrete state-space matrices (Ts = 0.002s) with 6x4 Kalman innovation gain L.
4. Receding-Horizon Model Predictive Control (MPC) with 10 unrolled Projected Gradient Descent (PGD) optimization iterations, analytical gradients, Q, R, P, S quadratic weighting matrices, hard actuator box limits, and maximum slew rate limits.
5. 4-Channel 2oo3 TMR sensor voting logic with median selection, 50 ms discrepancy debouncing timers, and bumpless fallback degradation (2oo3 -> 1oo2 -> 1oo1 -> Kalman Observer prediction fallback).
6. 14-Stage deterministic production Finite State Machine (FSM).
7. ANSI/ISA-18.2 multi-tiered alarms (HH, H, L, LL, hysteresis) and 32-bit fieldbus telemetry status registers.
8. Validate with `python validate_iec.py <saved_file>` and ensure 0 errors.
9. Save to `data/swarm_raw/agent_<uuid>.json` using `chr(96)*3` for markdown fences, clean up intermediate builder files if needed, and report completion back to parent agent."""

    fence = chr(96) * 3
    assistant_content = f"{fence}iec-st\n{full_st_code.strip()}\n{fence}"
    print(f"Assistant message content character count: {len(assistant_content)} characters")

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_uuid = uuid.uuid4().hex[:8]
    out_dir = "data/swarm_raw"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"agent_{target_uuid}.json")

    print(f"Writing dataset to {out_file}...")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"File saved successfully. Now validating with validate_iec.py...")
    errs = validate_iec.validate_json_file(out_file)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        print(f"Artifact successfully certified: {out_file}")
        print(f"UUID: {target_uuid}")
        print(f"Total Assistant Content Size: {len(assistant_content)} characters")

if __name__ == "__main__":
    main()
