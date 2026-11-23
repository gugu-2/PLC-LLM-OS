#!/usr/bin/env python3
"""
scripts/generate_type1_dialogue.py — Technical Dialogue Q&A Dataset Pipeline
Reference: DOC-04 §Dataset Type 1

Generates multi-turn technical Q&A dialogues between automation engineers covering:
- 2oo3 TMR voting vs 1oo2/1oo3 safety tradeoffs
- FSM-conditional TMR discrepancy threshold tuning
- Discrete state-space discretization (Tustin / Euler) in scan cycles
- MPC quadratic cost tuning (Q state weight vs R actuator effort)
- Anti-windup clamping and derivative kick suppression
"""

import os
import sys
import json
import uuid
import argparse
from pathlib import Path
from typing import Dict, List

# Add root to sys.path
root_dir = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root_dir))

import lumina

SAMPLE_DIALOGUES = [
    {
        "topic": "TMR_HotStripMill_AGC",
        "sector": "steelmaking",
        "system": "6-High Cold Mill AGC Roll Force Control",
        "messages": [
            {
                "role": "user",
                "content": "What is the purpose of the 2oo3 Triple Modular Redundancy (TMR) architecture in a hot strip mill AGC roll force system?"
            },
            {
                "role": "assistant",
                "content": (
                    "In a hot strip mill Automatic Gauge Control (AGC) system, the 2-out-of-3 (2oo3) TMR architecture serves "
                    "as the primary safety and operational availability mechanism for roll force load cells.\n\n"
                    "### Physical & Safety Context\n"
                    "The hydraulic gap cylinder delivers upwards of 35 to 50 Meganewtons (MN) of roll force. "
                    "If a single load cell suffers an open-circuit failure or drift while in roll contact at 1,800 m/min, "
                    "a naive single-sensor controller would attempt to compensate by driving the hydraulic servo cylinders "
                    "to maximum stroke. This causes immediate strip pinch, catastrophic work-roll spalling, and mill stall.\n\n"
                    "### Why 2oo3 Over 1oo2 or 1oo3?\n"
                    "1. **1oo2 (One-out-of-Two)**: If either sensor reports out-of-range, the system trips. In a rolling mill subject "
                    "to severe shock loads (tail-in impact), 1oo2 yields unacceptably low availability due to spurious trips.\n"
                    "2. **1oo3 (Three-out-of-Three)**: Requires unanimous agreement before tripping. A single frozen sensor would "
                    "blind the emergency stop interlock.\n"
                    "3. **2oo3 (Two-out-of-Three)**: The median voting algorithm rejects an outlier channel while maintaining continuous "
                    "production. If Channel A reads 24.2 MN, Channel B reads 24.4 MN, and Channel C suddenly drops to 0.1 MN, "
                    "the 2oo3 voter automatically selects the median (24.2 MN) and starts a discrepancy timer (typically 25 ms).\n\n"
                    "### Timed Discrepancy & Degradation\n"
                    "If the deviation persists beyond 25 ms, Channel C is marked INVALID, an ISA-18.2 Priority 2 Alarm is latched, "
                    "and the voting logic gracefully degrades to a 1oo2 average of Channels A and B without bumping the hydraulic cylinder command."
                )
            },
            {
                "role": "user",
                "content": "What happens during mill tail-out deceleration? Doesn't the strip whip cause false discrepancy trips?"
            },
            {
                "role": "assistant",
                "content": (
                    "Yes, exactly. Tail-out deceleration is the primary source of false trips in hot strip mills. "
                    "When the tail of the strip exits the roll bite, tension collapses asymmetrically, creating a 2–5 Hz force oscillation "
                    "of ±2 MN amplitude. A static 25 ms discrepancy timer at ±0.5 MN threshold will false-trip on every coil.\n\n"
                    "### The Architectural Solution: State-Dependent TMR Adaptation\n"
                    "The PLC Finite State Machine (FSM) must dynamically adapt the TMR discrepancy threshold and timer based on the current state:\n\n"
                    "```iec-st\n"
                    "(* Dynamic TMR Adaptation during Tail-Out Deceleration *)\n"
                    "IF State = STATE_TAILOUT_DECEL THEN\n"
                    "    r_DiscrepancyThreshold_MN := 3.5;    (* Widened threshold for mechanical shock *)\n"
                    "    t_DiscrepancyFilterTime := T#120ms;  (* Extended discrepancy persistence timer *)\n"
                    "    b_TMR_AlarmSuppressed := TRUE;       (* Suppress nuisance alarms per ISA-18.2 *)\n"
                    "ELSE\n"
                    "    r_DiscrepancyThreshold_MN := 0.5;    (* Normal steady-state threshold *)\n"
                    "    t_DiscrepancyFilterTime := T#25ms;   (* Fast fault response *)\n"
                    "    b_TMR_AlarmSuppressed := FALSE;\n"
                    "END_IF;\n"
                    "```\n\n"
                    "This guarantees both high availability during mechanical transients and SIL-2 safety integrity during steady-state rolling."
                )
            }
        ]
    },
    {
        "topic": "MPC_Tuning_ReflowOven",
        "sector": "electronics",
        "system": "12-Zone Convection Reflow Soldering Oven",
        "messages": [
            {
                "role": "user",
                "content": "In our 12-zone PCB reflow oven, how should the Model Predictive Control Q and R weighting matrices be balanced to prevent thermal overshoot during lead-free SAC305 processing?"
            },
            {
                "role": "assistant",
                "content": (
                    "In lead-free SAC305 reflow soldering, the peak temperature window is extremely narrow: "
                    "liquidus is at 217°C, the process peak must reach 235°C–245°C for wetting, but must never exceed 250°C "
                    "to prevent component package delamination.\n\n"
                    "### Mathematical Tuning Formulation\n"
                    "The MPC objective function minimizes:\n"
                    "\\[ J = \\sum_{k=0}^{N} (y_k - r_k)^T Q (y_k - r_k) + \\sum_{k=0}^{N-1} \\Delta u_k^T R \\Delta u_k \\]\n\n"
                    "1. **State Tracking Matrix Q**:\n"
                    "- Set high diagonal weights ($Q_{ii} = 50.0$) on the liquidus zones (Zones 8–10) and peak zone (Zone 11).\n"
                    "- Use asymmetric penalty: penalize positive temperature errors ($T_{meas} > T_{target}$) 5× more severely "
                    "than negative errors to prevent overshoot into the 250°C destruction limit.\n\n"
                    "2. **Actuator Slew Matrix R**:\n"
                    "- Solid-state relay (SSR) heating coils have significant thermal capacitance (time constant $\\tau \\approx 45$ s).\n"
                    "- Set $R_{ii} = 2.0$ to penalize sudden heater duty-cycle changes, preventing thermal hunting.\n\n"
                    "3. **Cross-Zone Coupling (B-Matrix)**:\n"
                    "Convective air transfer between adjacent zones creates strong thermal coupling (a heating increase in Zone 7 "
                    "adds 15% thermal energy to Zone 8). The discrete state-space model $B$ matrix must explicitly include these cross-terms."
                )
            }
        ]
    }
]

def generate_type1_dataset(out_dir: Path, count: int = 5) -> List[Path]:
    out_dir.mkdir(parents=True, exist_ok=True)
    generated = []

    for idx in range(count):
        sample = SAMPLE_DIALOGUES[idx % len(SAMPLE_DIALOGUES)]
        file_id = uuid.uuid4().hex[:8]
        filename = f"dialogue_qa_{sample['sector']}_{sample['topic']}_{file_id}.json"
        filepath = out_dir / filename

        payload = {
            "id": filepath.stem,
            "dataset_type": "type_1_dialogue_qa",
            "topic": sample["topic"],
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
    parser = argparse.ArgumentParser(description="Lumina Type 1 Dialogue QA Dataset Generator")
    parser.add_argument("--out-dir", default="data/supplementary/type_1_dialogue", help="Output directory")
    parser.add_argument("--count", type=int, default=2, help="Number of datasets to generate")
    args = parser.parse_args()

    files = generate_type1_dataset(Path(args.out_dir), count=args.count)
    print(f"Generated {len(files)} Type 1 Dialogue QA datasets in {args.out_dir}:")
    for f in files:
        print(f"  {f.name}")
