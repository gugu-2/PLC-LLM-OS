#!/usr/bin/env python3
"""
scripts/generate_type2_debug.py — 3-Turn Fault Diagnosis & Debug Chain Generator
Reference: DOC-04 §Dataset Type 2

Generates realistic 3-turn debugging datasets:
Turn 1: Automation engineer submits broken or unstable PLC code with observed plant fault symptoms.
Turn 2: Senior specialist identifies compounding root causes (anti-windup, derivative kick, valve slew saturation).
Turn 3: Complete, production-grade corrected Structured Text Function Block snippet.
"""

import os
import sys
import json
import uuid
import argparse
from pathlib import Path
from typing import Dict, List

SAMPLE_DEBUG_CHAINS = [
    {
        "fault_type": "Integral_Windup_Press_Overshoot",
        "sector": "heavy_machinery",
        "system": "2,500-Ton Servo Stamping Press Coining Stage",
        "messages": [
            {
                "role": "user",
                "content": (
                    "We are commissioning a 2,500-ton servo press. During the coining stroke (FSM Stage 6), "
                    "the press experiences a 14% force overshoot above the 22 MN setpoint before stabilizing. "
                    "This is causing micro-cracking in the automotive stamping dies. "
                    "Here is the excerpt from our current Structured Text logic:\n\n"
                    "```iec-st\n"
                    "(* Stage 6: Coining Force Hold *)\n"
                    "6: \n"
                    "    r_ForceError := r_TargetCoinForce - r_MeasuredForce_TMR;\n"
                    "    r_ForceIntegral := r_ForceIntegral + (r_ForceError * r_Ki * r_CycleTime);\n"
                    "    r_ServoCmd := (r_ForceError * r_Kp) + r_ForceIntegral;\n"
                    "    r_HydraulicValveOutput := r_ServoCmd;\n"
                    "```\n\n"
                    "What is causing this overshoot and how do we eliminate it?"
                )
            },
            {
                "role": "assistant",
                "content": (
                    "I have identified **three compounding flaws** in this control implementation that directly explain the 14% die overshoot:\n\n"
                    "### 1. Unbounded Integral Accumulation (Integral Windup)\n"
                    "During the rapid ram advance (Stage 4 and 5), the workpiece contact has not yet occurred. "
                    "The force error ($r\\_TargetCoinForce - r\\_MeasuredForce$) remains massive (~22 MN) for several hundred milliseconds. "
                    "Because `r_ForceIntegral` is unclamped, it accumulates an enormous value before contact. "
                    "When the die strikes the sheet metal, the integral cannot discharge instantly, driving the hydraulic valve "
                    "to full flow and causing the 14% over-tonnage.\n\n"
                    "### 2. Lack of Derivative Lead for Contact Impact\n"
                    "Sheet metal contact is a discontinuous stiffness transition (from air resistance to 22 MN die stiffness in < 30 ms). "
                    "A pure PI loop reacts only after the error develops. You need a derivative of force ($dF/dt$) to provide "
                    "immediate counter-braking the instant contact velocity slows.\n\n"
                    "### 3. Missing Valve Slew Rate Limiter\n"
                    "Your proportional servo valve has a physical spool bandwidth limit (typically 120–180 bar/s). "
                    "Driving `r_HydraulicValveOutput` directly from the raw PID output causes spool cavitation and secondary pressure resonance."
                )
            },
            {
                "role": "user",
                "content": "Please rewrite the Stage 6 logic in IEC 61131-3 with all three issues corrected."
            },
            {
                "role": "assistant",
                "content": (
                    "Here is the corrected, production-grade Stage 6 control logic:\n\n"
                    "```iec-st\n"
                    "(* Stage 6: Coining Force Hold with Anti-Windup, Derivative Lead, and Slew-Limiter *)\n"
                    "6: \n"
                    "    r_ForceError := r_TargetCoinForce - r_MeasuredForce_TMR;\n"
                    "    \n"
                    "    (* FIX 1: Clamped Anti-Windup Integration *)\n"
                    "    r_ForceIntegral := LIMIT(\n"
                    "        -r_MaxIntegralClamp_MN,\n"
                    "        r_ForceIntegral + (r_ForceError * r_Ki_Force * r_ScanTime_s),\n"
                    "        r_MaxIntegralClamp_MN\n"
                    "    );\n"
                    "    \n"
                    "    (* FIX 2: Contact Derivative Lead (dF/dt with 1st-order low-pass filter) *)\n"
                    "    r_dF_dt_raw := (r_MeasuredForce_TMR - r_MeasuredForce_Prev) / r_ScanTime_s;\n"
                    "    r_dF_dt_filtered := r_dF_dt_filtered + (r_ScanTime_s / (r_FilterTimeConst_s + r_ScanTime_s)) * (r_dF_dt_raw - r_dF_dt_filtered);\n"
                    "    r_MeasuredForce_Prev := r_MeasuredForce_TMR;\n"
                    "    \n"
                    "    (* PID Output Synthesis *)\n"
                    "    r_ServoCmd_Raw := (r_ForceError * r_Kp_Force) \n"
                    "                    + r_ForceIntegral \n"
                    "                    - (r_dF_dt_filtered * r_Kd_Force);\n"
                    "    \n"
                    "    (* FIX 3: Slew Rate Limiter to Protect Hydraulic Spool *)\n"
                    "    r_ValveDelta := LIMIT(-r_MaxValveSlew_PerScan, r_ServoCmd_Raw - r_HydraulicValveOutput, r_MaxValveSlew_PerScan);\n"
                    "    r_HydraulicValveOutput := r_HydraulicValveOutput + r_ValveDelta;\n"
                    "    \n"
                    "    (* Deterministic Coining Dwell Timer *)\n"
                    "    IF r_MeasuredForce_TMR >= (r_TargetCoinForce * 0.985) THEN\n"
                    "        ton_CoiningDwell(IN := TRUE, PT := t_CoiningDwellTime);\n"
                    "        IF ton_CoiningDwell.Q THEN\n"
                    "            ton_CoiningDwell(IN := FALSE);\n"
                    "            State := 7; (* Advance to controlled hydraulic decompression *)\n"
                    "        END_IF;\n"
                    "    ELSE\n"
                    "        ton_CoiningDwell(IN := FALSE);\n"
                    "    END_IF;\n"
                    "```"
                )
            }
        ]
    }
]

def generate_type2_dataset(out_dir: Path, count: int = 2) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    for idx in range(count):
        sample = SAMPLE_DEBUG_CHAINS[idx % len(SAMPLE_DEBUG_CHAINS)]
        file_id = uuid.uuid4().hex[:8]
        filename = f"debug_chain_{sample['sector']}_{sample['fault_type']}_{file_id}.json"
        filepath = out_dir / filename

        payload = {
            "id": filepath.stem,
            "dataset_type": "type_2_debug_chain",
            "fault_type": sample["fault_type"],
            "sector": sample["sector"],
            "system": sample["system"],
            "schema_version": "2.0",
            "messages": sample["messages"]
        }

        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)

        generated.append(filepath)

    return generated

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Type 2 Debug Chain Generator")
    parser.add_argument("--out-dir", default="data/supplementary/type_2_debug", help="Output directory")
    parser.add_argument("--count", type=int, default=2, help="Number of datasets to generate")
    args = parser.parse_args()

    files = generate_type2_dataset(Path(args.out_dir), count=args.count)
    print(f"Generated {len(files)} Type 2 Debug Chain datasets in {args.out_dir}:")
    for f in files:
        print(f"  {f.name}")
