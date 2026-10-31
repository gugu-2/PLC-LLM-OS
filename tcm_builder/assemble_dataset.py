# tcm_builder/assemble_dataset.py
import json
import os
import sys
from generate_tcm import generate_iec_code

def main():
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Heavy Metallurgy & Flat Steel Processing - 5-Stand 6-High Tandem Cold Rolling Mill (TCM) for Automotive Sheet (Dynamic Hydraulic Gap Control HGC, Continuous Variable Crown CVC Work/Intermediate Roll Bending & Shifting, Laser Velocimeter Strip Tension Regulation, X-Ray Thickness Automatic Gauge Control AGC Feedforward/Feedback/Monitor, Roll Eccentricity Filtering REC, Strip Flatness Shapemeter Roll)**

Task: Implement the production-grade Function Block `FB_Steel_TandemColdMill_5Stand_AGC_Flatness` governing:
1. Discrete State-Space Matrices (16x16 State Matrix A, 16x8 Input Matrix B, 8x16 Output Matrix C, 8x8 Feedforward Matrix D) modeling inter-stand strip elasticity tension dynamics, roll bite plastic deformation (Bland-Ford-Ellis equations), mill stand housing modulus elongation, HGC cylinder servo dynamics, intermediate roll shifting cross-coupling, and laser Doppler speed strip slip: x_{k+1} = A*x_k + B*u_k.
2. Receding-Horizon Model Predictive Control (MPC) quadratic cost optimization governing optimal HGC roll gap positions (microns), roll bending pressures (bar), and main motor speeds (RPM) to maintain exit thickness within +/- 0.5% and strip flatness within 5 I-Units.
3. 2oo3 Triple Modular Redundancy (TMR) voting logic on inter-stand tensiometers, X-ray thickness gauges, and laser Doppler strip velocimeters with discrepancy timers and bumpless degradation.
4. 12-stage operational Finite State Machine (FSM) covering coil loading, bite detection, cascaded threading, wrapper lock, mill acceleration to 1,500 m/min, AGC/flatness hold, REC active compensation, flying gauge change, tail-out deceleration, flying shear trigger, coil unloading, and emergency strip break trip.
5. ISA-18.2 multi-tiered alarm matrix with explicit 32-bit DWORD telemetry words (dwAlarmWord_1, dwAlarmWord_2, dwTMR_Diagnostic_1) tracking sudden strip snap, bearing oil pressure drop, roll gap asymmetry tilt, X-ray beam faults, and roll bite fire hazard.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    code = generate_iec_code()
    assistant_content = f"```iec-st\n{code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    out_path = os.path.join("data", "swarm_raw", "agent_9a204cb1.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset to {out_path}")
    print(f"Assistant content character count: {len(assistant_content)}")

if __name__ == "__main__":
    main()
