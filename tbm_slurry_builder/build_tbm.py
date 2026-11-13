# -*- coding: utf-8 -*-
"""
Script: build_tbm.py
Assembles the complete dataset JSON object for FB_Tunneling_SlurryTBM_Cutterhead_BentoniteBalance,
validates the result using validate_iec.py, and saves it to data/swarm_raw/agent_<uuid>.json.
"""

import sys
import os
import json
import uuid

# Ensure module path is included
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from mod_header_io import get_header_and_io
from mod_var_decl import get_var_declarations
from mod_phase0_matrices import get_phase0_matrices
from mod_phase1_tmr import get_phase1_tmr
from mod_phase2_cyberphysical import get_phase2_cyberphysical
from mod_phase3_mpc import get_phase3_mpc
from mod_phase4_fsm import get_phase4_fsm
from mod_phase5_alarms import get_phase5_alarms

def generate_tbm_dataset():
    prompt = (
        "You are generating a SINGLE ultra-dense, mathematically rigorous IEC 61131-3 Structured Text dataset for the "
        "**Civil Infrastructure & Heavy Underground Tunneling** industry (Tier 1 Priority Sector - Mega Tunnel Boring Machines).\n\n"
        "**Domain**: Civil Infrastructure & Heavy Underground Tunneling: 15.2-Meter Mega-Diameter Slurry Shield Tunnel Boring Machine "
        "(Mixshield TBM), Multi-Motor Variable Speed Cutterhead Drive (3,500 kW, 14 x 250 kW Inverters), Compressed Air Bubble Regulated "
        "Bentonite Slurry Excavation Face Pressure Balance (hydro-geological overburden balance within +/- 5 kPa), Synchronized 4-Quadrant "
        "Advance Thrust Cylinder Group Pressure & Trajectory Steering (total thrust 250,000 kN), Dual-Component Fast-Setting Annular Tail Void "
        "Grout Injection Pressure & Volume Control, Continuous Slurry Feed/Discharge Flow and Real-Time Dry Muck Mass Extraction Balance, "
        "and ISO 13849-1 Cat 4 / PL e & ISA-18.2 Catastrophic Face Stability Interlocks.\n\n"
        "**Function Block Name**: `FB_Tunneling_SlurryTBM_Cutterhead_BentoniteBalance`\n\n"
        "**Engineering Context & Operational Architecture**:\n"
        "- 15.2-Meter Mega-Diameter Mixshield TBM operating in high-permeability, saturated gravel and alluvial strata under 25-45 m overburden depth.\n"
        "- Submerged diaphragm wall creating an excavation chamber and a rear working chamber with a regulated compressed air cushion buffer.\n"
        "- 10 Triplet Sensor Groups voted via 2oo3 Triple Modular Redundancy (TMR) with dynamic discrepancy accumulation timers and bumpless degradation (PT-101A/B/C, PT-201A/B/C, LT-202A/B/C, FT-301A/B/C, FT-302A/B/C, DT-401A/B/C, DT-402A/B/C, LC-601A/B/C, TT-501A/B/C, PT-701A/B/C).\n"
        "- Full 8x8 discrete state-space formulation (x[k+1] = A*x[k] + B*u[k]) at Ts = 50 ms modeling hydrodynamic excavation face pressure decay, pneumatic air cushion polytropic expansion (gamma = 1.25), working chamber slurry level interface, closed-loop slurry flow imbalance, muck density differential, thrust hydraulic compliance, cutterhead torsional damping, and tail void grout filtration.\n"
        "- Receding-horizon Model Predictive Control (MPC) quadratic cost functional minimized via unrolled Projected Gradient Descent (PGD) with box actuator saturation constraints and slew rate limiting to maintain excavation crown pressure within +/- 5 kPa (+/- 0.05 bar) of in-situ geotechnical target.\n"
        "- Deterministic 14-stage operational Finite State Machine (FSM) sequencing across Standby Idle, Slurry Line Circulation Prime, Air Bubble Regulated Pressurization, Cutterhead Rotation Soft-Start, Synchronized Ring Advance Thrust, Geological Density Balancing, Advance Stroke Completion, Thrust Cylinder Group Retraction, Segment Ring Placement Permissive, Tail Void Grout Injection, Muck Slurry Scour Cycle, Cutter Tool Wear Inspection Mode, Surface Heave/Settlement Emergency Abort, and Emergency Face Support Lock.\n"
        "- Full ISA-18.2 4-tier alarm engine with 4 x 32-bit bit-packed diagnostic alarm words (Catastrophic Blowout/Cave-in, Slurry Circuit & Thrust Hydraulics, Cutterhead Drive & Tail Grout, TMR Sensor Redundancy & Master Trip) with deadband hysteresis.\n"
        "- Real-time cyber-physical observers: In-situ Jacky K0 earth pressure with arching, 2-phase dry muck mass balance extraction ratio, specific rock cutting energy, boulder impact probability filter, and cumulative annular void grout fill ratio."
    )

    parts = [
        get_header_and_io(),
        get_var_declarations(),
        get_phase0_matrices(),
        get_phase1_tmr(),
        get_phase2_cyberphysical(),
        get_phase3_mpc(),
        get_phase4_fsm(),
        get_phase5_alarms(),
        "END_FUNCTION_BLOCK"
    ]
    raw_st = "\n\n".join(parts)
    code_content = f"```iec-st\n{raw_st}\n```"

    agent_id = f"agent_{uuid.uuid4().hex[:8]}"
    out_filename = f"data/swarm_raw/{agent_id}.json"

    dataset_record = {
        "id": agent_id,
        "instruction": prompt,
        "input": "",
        "output": code_content,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_content}
        ],
        "metadata": {
            "domain": "Civil Infrastructure & Heavy Underground Tunneling",
            "function_block": "FB_Tunneling_SlurryTBM_Cutterhead_BentoniteBalance",
            "system": "15.2-Meter Slurry Shield Tunnel Boring Machine (TBM)",
            "standards": ["IEC 61131-3 3rd Ed", "ISA-18.2", "DAUB Guidelines", "ISO 13849-1 Cat 4 / PL e"],
            "raw_characters": len(raw_st),
            "total_content_characters": len(code_content)
        }
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(out_filename, "w", encoding="utf-8") as f:
        json.dump(dataset_record, f, ensure_ascii=False, indent=2)

    print(f"Generated dataset successfully: {out_filename}")
    print(f"Code character length: {len(code_content)}")
    print(f"Raw ST character length: {len(raw_st)}")
    return out_filename

if __name__ == "__main__":
    filepath = generate_tbm_dataset()
