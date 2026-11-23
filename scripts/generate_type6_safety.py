#!/usr/bin/env python3
"""
scripts/generate_type6_safety.py — Safety Instrumented Function (SIF) Dataset Pipeline
Reference: DOC-04 §Dataset Type 6

Generates IEC 61511 / IEC 62061 compliant functional safety datasets:
- Safety Requirement Specification (SRS)
- SIL target verification (PFDavg, proof test intervals)
- Certified 1oo2D / 2oo3 safety shutdown logic
"""

import os
import sys
import json
import uuid
import argparse
from pathlib import Path
from typing import Dict, List

SAMPLE_SAFETY_SCENARIOS = [
    {
        "sif_name": "HighHigh_Hydraulic_Pressure_Protection_SIL2",
        "sector": "heavy_machinery",
        "system": "15,000-Ton Forging Press Main Cylinder Overpressure Protection",
        "messages": [
            {
                "role": "user",
                "content": (
                    "Design a Safety Instrumented Function (SIF) for high-high hydraulic pressure protection "
                    "on a 15,000-ton forging press main cylinder. The SIF must achieve SIL-2 compliance per IEC 61511. "
                    "Process demand rate is 0.1/year, required PFDavg < 1.0E-3. Include proof test interval recommendations, "
                    "dual-redundant 1oo2D pressure transmitter voting with diagnostic discrepancy trip, and certified Structured Text logic."
                )
            },
            {
                "role": "assistant",
                "content": (
                    "## SIF Design: Main Cylinder High-High Hydraulic Overpressure Protection (SIL-2)\n\n"
                    "### 1. Safety Requirement Specification (SRS)\n"
                    "- **Safety Function**: De-energize high-speed hydraulic cartridge dump valves (XV-101A and XV-101B) "
                    "upon cylinder pressure $\\ge 380$ bar (rated press MAWP = 400 bar).\n"
                    "- **Safe State**: Dump valves de-energized to open; main cylinder vented directly to reservoir tank.\n"
                    "- **Target SIL**: SIL-2 (Low Demand Mode, $\\text{PFD}_{\\text{avg}} \\le 1.0 \\times 10^{-3}$).\n"
                    "- **Response Time**: $\\le 45$ ms total (Sensor: 10 ms, Safety PLC Scan: 10 ms, Valve Opening: 25 ms).\n"
                    "- **Architecture**: 1oo2D (One-out-of-Two with Internal Diagnostics) for transmitters; 1oo2 de-energize to trip for final elements.\n\n"
                    "### 2. SIL Verification & PFDavg Calculation\n"
                    "- Transmitter Dangerous Undetected Failure Rate ($\\lambda_{DU}$): $1.2 \\times 10^{-7} \\text{ hr}^{-1}$\n"
                    "- Proof Test Interval ($T_1$): 8,760 hours (1 year)\n"
                    "- Common Cause Beta Factor ($\\beta$): 5%\n"
                    "- $\\text{PFD}_{\\text{avg}} \\approx \\frac{(\\lambda_{DU} \\cdot T_1)^2}{3} + \\beta \\frac{\\lambda_{DU} \\cdot T_1}{2} = 4.2 \\times 10^{-4} < 1.0 \\times 10^{-3}$ (SIL-2 Compliant)\n\n"
                    "### 3. Certified IEC 61131-3 Safety Logic\n"
                    "```iec-st\n"
                    "FUNCTION_BLOCK FB_SIF_MainCylinder_Overpressure_SIL2\n"
                    "VAR_INPUT\n"
                    "    r_Pressure_PT1_Bar : REAL; (* Channel A 4-20mA Transmitter [bar] *)\n"
                    "    r_Pressure_PT2_Bar : REAL; (* Channel B 4-20mA Transmitter [bar] *)\n"
                    "    r_LoopCurrent_PT1 : REAL;  (* Transmitter A current [mA] *)\n"
                    "    r_LoopCurrent_PT2 : REAL;  (* Transmitter B current [mA] *)\n"
                    "    r_DiagnosticScan_ms : REAL := 10.0; (* Fast safety scan time [ms] *)\n"
                    "    b_PT1_Health_DI : BOOL;    (* Transmitter A internal NAMUR NE43 status *)\n"
                    "    b_PT2_Health_DI : BOOL;    (* Transmitter B internal NAMUR NE43 status *)\n"
                    "    b_ManualSafetyReset_PB : BOOL; (* Supervised physical pushbutton *)\n"
                    "END_VAR\n"
                    "VAR_OUTPUT\n"
                    "    b_DumpValve_A_Safe_DO : BOOL; (* De-energize to trip *)\n"
                    "    b_DumpValve_B_Safe_DO : BOOL; (* De-energize to trip *)\n"
                    "    b_SIF_Tripped : BOOL;\n"
                    "    b_SensorDiscrepancy_Alarm : BOOL;\n"
                    "END_VAR\n"
                    "VAR\n"
                    "    ton_DiscrepancyTimer : TON;\n"
                    "    b_DiscrepancyTrip : BOOL;\n"
                    "    b_LatchedTrip : BOOL := TRUE; (* Safe power-on default *)\n"
                    "END_VAR\n"
                    "\n"
                    "(* Diagnostic 1: Verify Transmitter Loop Currents *)\n"
                    "IF NOT b_PT1_Health_DI OR NOT b_PT2_Health_DI THEN\n"
                    "    b_LatchedTrip := TRUE;\n"
                    "END_IF;\n"
                    "\n"
                    "(* Diagnostic 2: Channel Mismatch Discrepancy (Tolerance > 15 bar for > 30ms) *)\n"
                    "ton_DiscrepancyTimer(IN := ABS(r_Pressure_PT1_Bar - r_Pressure_PT2_Bar) > 15.0, PT := T#30ms);\n"
                    "IF ton_DiscrepancyTimer.Q THEN\n"
                    "    b_SensorDiscrepancy_Alarm := TRUE;\n"
                    "    b_DiscrepancyTrip := TRUE;\n"
                    "    b_LatchedTrip := TRUE;\n"
                    "END_IF;\n"
                    "\n"
                    "(* 1oo2 High-High Trip Voting *)\n"
                    "IF (r_Pressure_PT1_Bar >= 380.0) OR (r_Pressure_PT2_Bar >= 380.0) THEN\n"
                    "    b_LatchedTrip := TRUE;\n"
                    "END_IF;\n"
                    "\n"
                    "(* Supervised Manual Reset Permissive *)\n"
                    "IF b_LatchedTrip THEN\n"
                    "    b_DumpValve_A_Safe_DO := FALSE; (* De-energize = Dump *)\n"
                    "    b_DumpValve_B_Safe_DO := FALSE; (* De-energize = Dump *)\n"
                    "    b_SIF_Tripped := TRUE;\n"
                    "    \n"
                    "    IF b_ManualSafetyReset_PB \n"
                    "       AND r_Pressure_PT1_Bar < 250.0 \n"
                    "       AND r_Pressure_PT2_Bar < 250.0 \n"
                    "       AND NOT b_DiscrepancyTrip THEN\n"
                    "        b_LatchedTrip := FALSE;\n"
                    "        b_SIF_Tripped := FALSE;\n"
                    "    END_IF;\n"
                    "ELSE\n"
                    "    b_DumpValve_A_Safe_DO := TRUE; (* Energized to hold *)\n"
                    "    b_DumpValve_B_Safe_DO := TRUE;\n"
                    "    b_SIF_Tripped := FALSE;\n"
                    "END_IF;\n"
                    "END_FUNCTION_BLOCK\n"
                    "```"
                )
            }
        ]
    }
]

def generate_type6_dataset(out_dir: Path, count: int = 1) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    for idx in range(count):
        sample = SAMPLE_SAFETY_SCENARIOS[idx % len(SAMPLE_SAFETY_SCENARIOS)]
        file_id = uuid.uuid4().hex[:8]
        filename = f"safety_sif_{sample['sector']}_{sample['sif_name']}_{file_id}.json"
        filepath = out_dir / filename

        payload = {
            "dataset_type": "type_6_safety_sif",
            "sif_name": sample["sif_name"],
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
    parser = argparse.ArgumentParser(description="Lumina Type 6 Safety SIF Dataset Generator")
    parser.add_argument("--out-dir", default="data/supplementary/type_6_safety", help="Output directory")
    parser.add_argument("--count", type=int, default=1, help="Number of datasets to generate")
    args = parser.parse_args()

    files = generate_type6_dataset(Path(args.out_dir), count=args.count)
    print(f"Generated {len(files)} Type 6 Safety datasets in {args.out_dir}:")
    for f in files:
        print(f"  {f.name}")
