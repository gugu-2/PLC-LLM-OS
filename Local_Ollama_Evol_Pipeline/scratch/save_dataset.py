# save_dataset.py
import os
import sys
import uuid
import json

sys.path.insert(0, 'Local_Ollama_Evol_Pipeline/scratch')
from gen_part1_vars import get_part1_vars
from gen_part2_tmr import get_part2_tmr
from gen_part3_ss_mpc import get_part3_ss_mpc
from gen_part4_fsm import get_part4_fsm
from gen_part5_alarms import get_part5_alarms

code_body = get_part1_vars().strip() + "\n\n" + \
            get_part2_tmr().strip() + "\n\n" + \
            get_part3_ss_mpc().strip() + "\n\n" + \
            get_part4_fsm().strip() + "\n\n" + \
            get_part5_alarms().strip()

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Food & Beverage Mass Continuous Packaging - Ultra-High-Speed (90,000 cph / 1,500 cans/min) Continuous Rotary Aseptic Beverage Canning Machine: Twin-Turret Electronic Camming Hermetic Double-Seamer with 1st & 2nd Operation Roll Force Feedback, In-Seam Inert Liquid Nitrogen (LN2) Micro-Dosing (pressure generation 1.5–2.5 bar), In-Line High-Speed 360° Eddy-Current / Acoustic Tap Resonance Leak Inspection, and Vaporized Peracetic Acid (PAA) Chamber Isolator Barrier Sterilization.**

Task: Implement the production-grade Function Block `FB_FoodBev_AsepticCanning_DoubleSeamer_LeakInspect` governing:
1. Discrete State-Space Matrices (A, B, C, D) modeling metal sheet elastic-plastic seam interlock deformation (seam thickness, body hook, cover hook, overlap ratio), high-speed electronic camming trajectory tracking error, LN2 vaporization flash thermodynamics, and acoustic impulse resonance damping: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost functional optimizing seaming roll servomotor feed position profile, electronic cam spindle speed, and LN2 cryogenic injection valve duration to maintain seam overlap hermeticity > 85% at zero micro-leaks.
3. 2oo3 TMR voting logic on acoustic tap impulse frequency analyzers (120 Hz discrepancy trip) and double-seam chuck load cell transducers (35 N discrepancy threshold).
4. ISA-18.2 multi-tiered alarm matrix (Critical HH, Warning H, Low L, Low-Low LL, Rate-of-Change leak detection) with rapid automatic can-reject diversion gate actuation (< 2 ms latency).
5. 12-stage FSM (STERILIZATION_CIP_PAA, PRESSURE_BARRIER_ESTABLISH, INLET_STARWHEEL_PACING, CAN_ELEVATOR_LIFTER_ENGAGE, LN2_IN_SEAM_CRYODOSE, FIRST_OPERATION_CURL_SEAM, SECOND_OPERATION_HERMETIC_CRIMP, ACOUSTIC_TAP_LEAK_TEST, HIGH_SPEED_PNEUMATIC_REJECT, DISCHARGE_SYNCHRONIZATION, JAM_DETECTION_CONTROLLED_STOP, EMERGENCY_DEPRESSURIZATION).

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

# Triple backticks explicitly
formatted_code = "```iec-st\n" + code_body + "\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": formatted_code}
    ]
}

# Overwrite agent_011dafac.json
filename = "data/swarm_raw/agent_011dafac.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully saved to {filename}")
print(f"Code chars: {len(code_body)}")
print(f"Assistant content start: {repr(formatted_code[:25])}")
print(f"Assistant content end: {repr(formatted_code[-25:])}")

sys.path.insert(0, 'Local_Ollama_Evol_Pipeline/scripts')
from linter import ST_Linter
passed, msg = ST_Linter.verify_code(code_body)
print(f"Static AST Verification: {passed} | {msg}")
