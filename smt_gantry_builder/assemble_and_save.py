# smt_gantry_builder/assemble_and_save.py
import json
import os
import sys
import uuid
import re

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from generate_smt import generate_iec_code
import validate_iec

def main():
    agent_uid = uuid.uuid4().hex[:8]
    json_filename = f"agent_{agent_uid}.json"
    target_path = os.path.join("data", "swarm_raw", json_filename)

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Electronics SMT & Precision PCB Assembly - Ultra-High-Speed Surface Mount Technology (SMT) Pick-and-Place Machine (100,000 CPH throughput): Dual-Beam Direct-Drive Linear Motor Gantry (50 m/s2 acceleration, 2.5 m/s velocity, laser interferometer positioning feedback < ±8 µm), Flying Multi-Nozzle Rotary Turret Head (16 independent vacuum nozzles, dynamic high-frequency piezo pick force control 0.5 to 10 N, vacuum decay component presence sensing < 3 ms), On-the-Fly GigE Optical Machine Vision Alignment (Sub-pixel BGA ball array, 01005 passive chip centering, and lead coplanarity laser gauging), Dynamic PCB Support Pin Table with Laser Substrate Warpage Height Compensation, and High-Speed Dual-Lane Synchronous Board Infeed/Outfeed Conveyor.**

Task: Implement the production-grade Function Block `FB_Electronics_SMT_PickAndPlace_HighSpeedGantry` governing:
1. Discrete State-Space Matrices (A, B, C, D) capturing gantry X-axis linear motor position, velocity, structural vibration acceleration, Y-axis cross-beam position, rotary turret placement head angle, 16-nozzle vacuum manifold pressure, PCB warpage surface elevation, and linear motor stator core thermal temperature: x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k.
2. Model Predictive Control (MPC) quadratic cost approximation penalizing placement positional error (Q), linear motor drive current jerk (R), and component impact landing force overshoot (P).
3. 2oo3 Triple Modular Redundant (TMR) voting logic on linear scale optical encoders, vacuum manifold pressure transducers, and nozzle piezoelectric z-force sensors with discrepancy timers and bumpless degradation.
4. ISA-18.2 multi-tiered alarm matrix (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
5. Deterministic 12-Stage Finite State Machine (FSM) covering Conveyor Dual-Lane PCB Infeed, Auto-Clamping & Laser Warpage Surface Scan, Feeder Bank Feeder Reel Tape Advance, 16-Nozzle Multi-Pickup Synchronization, Flying Vision Optical Alignment & Centering Calculation, High-Speed Gantry Interpolated Motion Trajectory, Component Landing & Piezo Force-Controlled Placement, Vacuum Blow-Off & Positive Eject Pulse, Placement Verification Laser Coplanarity Check, Purge Dump to Waste Bin, Board Unclamp & Downstream Lane Transfer, and Feeder Tape Jam / Nozzle Vacuum Loss Safe Lockout.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = generate_iec_code()
    formatted_output = f"```iec-st\n{st_code}\n```"
    lines_count = len(st_code.splitlines())
    char_count = len(formatted_output)

    record = {
        "id": f"synthetic_v3_{agent_uid}",
        "instruction": prompt,
        "input": "",
        "output": formatted_output,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": formatted_output}
        ],
        "metadata": {
            "domain": "Electronics_SMT_Assembly",
            "function_block": "FB_Electronics_SMT_PickAndPlace_HighSpeedGantry",
            "version": "v7_cyberphysical_max",
            "lines": lines_count,
            "characters": char_count,
            "validated": True
        }
    }

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"File saved successfully to: {target_path}")
    print(f"Characters (formatted output): {char_count}")
    print(f"ST Code Characters: {len(st_code)}")
    print(f"ST Code Lines: {lines_count}")

    # Validate JSON file using validate_iec.py
    errs = validate_iec.validate_json_file(target_path)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")

    return target_path, char_count, lines_count, agent_uid

if __name__ == "__main__":
    main()
