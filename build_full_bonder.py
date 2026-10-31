# build_full_bonder.py
# Generator for FB_Semiconductor_Thermosonic_WireBonder_HighSpeed
import json
import os
import subprocess
import sys

import st_header_and_io
import st_var_declarations
import st_matrices_init
import st_phases_1_to_5
import st_phases_6_to_11

def build_dataset():
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Electronics & Semiconductor Packaging: Ultra-High-Speed Dual-Head Thermosonic Gold Wire Bonder (22 Wires/Sec, 35 um Pitch) with Electronic Flame-Off (EFO) Spark & Voice Coil Z-Drive**

Task: Implement the production-grade Function Block FB_Semiconductor_Thermosonic_WireBonder_HighSpeed governing:
1. High-throughput thermosonic wire bonder (22 wires/second, bonding 15-25 um Au/Cu wire across high-density leadframes and BGA substrates with 35 um fine pitch).
2. High-speed voice coil motor (VCM) Z-axis drive with linear optical encoder (10 nm resolution, 150g peak acceleration, dynamic impact soft-landing detection < 0.15 N).
3. Electronic Flame-Off (EFO) spark discharge generator: programmable micro-joule capacitive discharge creating Free Air Ball (FAB) with closed-loop optical diameter verification (+/- 0.5 um sphericity).
4. Piezoelectric ultrasonic transducer (60 kHz or 120 kHz / 138 kHz dual-frequency resonance): dynamic phase-locked loop (PLL) tracking electrical impedance resonance dip during 1st bond (ball bond on die pad) and 2nd bond (stitch/crescent bond on leadframe).
5. Heated vacuum workholder stage with multi-zone PID substrate heating (150-220 deg C +/- 1.0 deg C) and mechanical indexing clamp.
6. Wire looping trajectory generator: reverse motion, kink forming, trapezoidal/B-spline wire loop profiles maintaining consistent loop height (+/- 2.0 um) without wire sag or neck crack.
7. In-line optical Pattern Recognition (PR) vision compensating for die placement rotation (Delta X, Delta Y, Delta Theta) in sub-millisecond cycles.
8. Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating capillary voice coil dynamics, ultrasonic transducer mechanical horn vibration, wire intermetallic Au-Al / Cu-Al diffusion growth, and stage thermal expansion.
9. Receding-horizon MPC for voice coil soft-landing velocity trajectory and ultrasonic power burst profile.
10. 2oo3 Triple Modular Redundancy (TMR) voting across Z-axis optical scale encoders, bond force load cells, and ultrasonic power feedback with bumpless degradation.
11. 12-Stage Operational FSM (Substrate Leadframe Indexing & Vacuum Clamp, Optical Pattern Recognition Die Alignment, EFO Spark Free Air Ball Discharge, Ball Formation Optical Check, High-Speed Approach & Contact Soft Landing, 1st Bond Ultrasonic/Force Burst, Programmable Looping Trajectory Generation, 2nd Bond Leadframe Contact & Ultrasonic Stitch, Wire Clamp Tear & Tail Feed, Capillary Z-Retract & Tail Length Metrology, Leadframe Egress to Output Magazine, Emergency E-Stop Voice Coil Retract & Ultrasonic Safe Stop).
12. ISA-18.2 multi-tiered alarm matrix (EFO spark open-circuit HH, missing ball detection, wire drag/tail length short, ultrasonic impedance detuning trip, stage vacuum lost) with bit-packed telemetry DWORDs.

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st.
2. EXACT AST PARITY: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
3. First line: FUNCTION_BLOCK FB_Semiconductor_Thermosonic_WireBonder_HighSpeed, Last line: END_FUNCTION_BLOCK.
4. Total length >= 55,000 characters (zero placeholders, zero truncation comments)."""

    header = st_header_and_io.get_header_and_io()
    var_decl = st_var_declarations.get_var_declarations()
    mat_init = st_matrices_init.get_matrices_init()
    p1_5 = st_phases_1_to_5.get_phases_1_to_5()
    p6_11 = st_phases_6_to_11.get_phases_6_to_11()
    end_fb = "END_FUNCTION_BLOCK\n"

    full_st = "\n".join([header, var_decl, mat_init, p1_5, p6_11, end_fb])
    assistant_content = f"```iec-st\n{full_st}```"

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_file = "data/swarm_raw/agent_7a409cb1.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset saved successfully to {target_file}")
    print(f"Assistant content character count: {len(assistant_content)}")
    print(f"Total file size: {os.path.getsize(target_file)} bytes")

if __name__ == "__main__":
    build_dataset()
