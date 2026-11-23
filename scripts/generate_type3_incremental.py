#!/usr/bin/env python3
"""
scripts/generate_type3_incremental.py — Incremental Modification Dataset Pipeline
Reference: DOC-04 §Dataset Type 3

Generates pairs where an existing Function Block is extended with specialized subsystems:
- Adding 128-cavity piezoelectric pressure imbalance detection to injection molding
- Adding dynamic thermal spindle expansion compensation to 5-axis CNC mills
- Integrating 2oo3 TMR voting into a legacy single-transmitter loop
"""

import os
import sys
import json
import uuid
import argparse
from pathlib import Path
from typing import Dict, List

SAMPLE_INCREMENTAL = [
    {
        "task_name": "Add_Cavity_Imbalance_Monitoring",
        "sector": "plastics",
        "system": "1,200-Ton Injection Molding Machine",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Here is an excerpt from our existing Function Block controlling a 128-cavity PET preform injection molding press:\n\n"
                    "```iec-st\n"
                    "FUNCTION_BLOCK FB_Plastics_PreformInjection\n"
                    "VAR_INPUT\n"
                    "    r_MeltTemp_Barrel : REAL;\n"
                    "    r_InjectionPressure_Main : REAL;\n"
                    "    r_CavityPressure_arr : ARRAY[1..128] OF REAL; (* Bar *)\n"
                    "END_VAR\n"
                    "VAR_OUTPUT\n"
                    "    r_ServoInjectionValve : REAL;\n"
                    "    b_MoldingCycleComplete : BOOL;\n"
                    "END_VAR\n"
                    "```\n\n"
                    "Task: Extend this Function Block to add a 5-tier cavity pressure imbalance detection algorithm. "
                    "Calculate the mean cavity pressure across all 128 channels, detect individual cavity deviations > ±10%, "
                    "and trigger a graduated response: (1) Alarm log, (2) hot runner nozzle temperature trim adjustment (±0.5°C), "
                    "and (3) if more than 8 cavities diverge, raise an emergency cycle hold."
                )
            },
            {
                "role": "assistant",
                "content": (
                    "Here is the modular addition for the 5-tier cavity pressure imbalance detection subsystem, "
                    "designed to insert cleanly into `FB_Plastics_PreformInjection`:\n\n"
                    "```iec-st\n"
                    "(* ========================================================================= *)\n"
                    "(* SECTION: 5-TIER 128-CAVITY PRESSURE IMBALANCE & HOT RUNNER BALANCING      *)\n"
                    "(* ========================================================================= *)\n"
                    "\n"
                    "(* Step 1: Compute Mean Cavity Pressure across all 128 sensors *)\n"
                    "r_CavityPressure_Sum := 0.0;\n"
                    "n_ActiveSensorCount := 0;\n"
                    "\n"
                    "FOR i_cav := 1 TO 128 DO\n"
                    "    (* Reject disconnected or zero channels *)\n"
                    "    IF r_CavityPressure_arr[i_cav] > 5.0 THEN\n"
                    "        r_CavityPressure_Sum := r_CavityPressure_Sum + r_CavityPressure_arr[i_cav];\n"
                    "        n_ActiveSensorCount := n_ActiveSensorCount + 1;\n"
                    "    END_IF;\n"
                    "END_FOR;\n"
                    "\n"
                    "IF n_ActiveSensorCount >= 120 THEN\n"
                    "    r_CavityPressure_Mean := r_CavityPressure_Sum / INT_TO_REAL(n_ActiveSensorCount);\n"
                    "ELSE\n"
                    "    (* Critical sensor loss: raise sensor group fault *)\n"
                    "    b_CavitySensorGroupFault := TRUE;\n"
                    "END_IF;\n"
                    "\n"
                    "(* Step 2: Evaluate Cavity Deviations & Tiered Reaction *)\n"
                    "n_DivergentCavityCount := 0;\n"
                    "r_ImbalanceThreshold_Bar := r_CavityPressure_Mean * 0.10; (* 10% tolerance *)\n"
                    "\n"
                    "FOR i_cav := 1 TO 128 DO\n"
                    "    r_CavityDeviation[i_cav] := r_CavityPressure_arr[i_cav] - r_CavityPressure_Mean;\n"
                    "    \n"
                    "    IF ABS(r_CavityDeviation[i_cav]) > r_ImbalanceThreshold_Bar THEN\n"
                    "        n_DivergentCavityCount := n_DivergentCavityCount + 1;\n"
                    "        b_CavityImbalance_Alarm[i_cav] := TRUE;\n"
                    "        \n"
                    "        (* Tier 2: Dynamic Hot Runner Nozzle Temperature Trim *)\n"
                    "        IF r_CavityDeviation[i_cav] < 0.0 THEN\n"
                    "            (* Cavity underfilled: increase nozzle heater setpoint by 0.5 deg C *)\n"
                    "            r_HotRunnerTrim_SP[i_cav] := LIMIT(-5.0, r_HotRunnerTrim_SP[i_cav] + 0.5, 5.0);\n"
                    "        ELSE\n"
                    "            (* Cavity overpacked: decrease nozzle heater setpoint by 0.5 deg C *)\n"
                    "            r_HotRunnerTrim_SP[i_cav] := LIMIT(-5.0, r_HotRunnerTrim_SP[i_cav] - 0.5, 5.0);\n"
                    "        END_IF;\n"
                    "    ELSE\n"
                    "        b_CavityImbalance_Alarm[i_cav] := FALSE;\n"
                    "    END_IF;\n"
                    "END_FOR;\n"
                    "\n"
                    "(* Tier 3: Emergency Cycle Hold on Multi-Cavity Imbalance *)\n"
                    "IF n_DivergentCavityCount > 8 THEN\n"
                    "    b_EmergencyCycleHold := TRUE;\n"
                    "    r_ServoInjectionValve := 0.0; (* Safe retraction *)\n"
                    "    State := 99; (* Transition to FAULT_HOLD state *)\n"
                    "END_IF;\n"
                    "```"
                )
            }
        ]
    }
]

def generate_type3_dataset(out_dir: Path, count: int = 1) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    for idx in range(count):
        sample = SAMPLE_INCREMENTAL[idx % len(SAMPLE_INCREMENTAL)]
        file_id = uuid.uuid4().hex[:8]
        filename = f"incremental_{sample['sector']}_{sample['task_name']}_{file_id}.json"
        filepath = out_dir / filename

        payload = {
            "id": filepath.stem,
            "dataset_type": "type_3_incremental_modification",
            "task_name": sample["task_name"],
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
    parser = argparse.ArgumentParser(description="Lumina Type 3 Incremental Modification Dataset Generator")
    parser.add_argument("--out-dir", default="data/supplementary/type_3_incremental", help="Output directory")
    parser.add_argument("--count", type=int, default=1, help="Number of datasets to generate")
    args = parser.parse_args()

    files = generate_type3_dataset(Path(args.out_dir), count=args.count)
    print(f"Generated {len(files)} Type 3 Incremental datasets in {args.out_dir}:")
    for f in files:
        print(f"  {f.name}")
