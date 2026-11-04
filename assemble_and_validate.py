# -*- coding: utf-8 -*-
"""
Assembles FB_Packaging_Corrugator_SingleFacer_FlyingShear dataset, validates it, and saves to data/swarm_raw/agent_34bc966a.json
"""
import os
import json
import uuid
import re
import subprocess

from corrugator_part1_header_decl import get_part1
from corrugator_part2_tmr_physics import get_part2
from corrugator_part3_mpc_fsm_alarms import get_part3

def main():
    agent_uuid = "34bc966a"
    filename = f"data/swarm_raw/agent_{agent_uuid}.json"

    # Assemble code
    part1 = get_part1()
    part2 = get_part2()
    part3 = get_part3()

    full_st_code = part1.rstrip() + "\n" + part2.strip() + "\n" + part3.strip()
    # Normalize line endings to LF
    full_st_code = full_st_code.replace("\r\n", "\n")

    lines = [l.strip() for l in full_st_code.splitlines() if l.strip()]
    print(f"Total lines of ST code: {len(lines)}")
    print(f"First line: '{lines[0]}'")
    print(f"Last line: '{lines[-1]}'")

    # Format assistant content with triple backtick and iec-st
    assistant_content = f"```iec-st\n{full_st_code}\n```"
    char_count = len(assistant_content)
    line_count = len(assistant_content.splitlines())
    print(f"Total character count: {char_count}")
    print(f"Total line count: {line_count}")

    # Prompt
    prompt_text = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Paper Converting & Heavy Packaging Machinery
- System: High-Speed Corrugated Cardboard Corrugator Line (400 m/min continuous web): Wet-End Single Facer (Flute A/B/C corrugating rolls, steam-heated roll nip pressure 25 bar, starch adhesive film applicator gap servo adjustment 0.15 to 0.35 mm with temperature/viscosity compensation), Bridge Reservoir Web Accumulator & Festoon Tension Balancing (Ultrasonic catenary loop sensors), Double-Backer Steam Chest Multi-Section Temperature Profile (160 deg C to 185 deg C with dynamic ballast shoes), and Dry-End High-Speed Flying Rotary Slitter / Scorer with Servo Cutoff Synchronization (< +/- 0.5 mm sheet length accuracy at 400 m/min).
- Function Block Name: FB_Packaging_Corrugator_SingleFacer_FlyingShear

NEXT-GEN QUALITY REQUIREMENTS:
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) capturing corrugating roll temperatures, starch film thickness, bridge web accumulator level, steam chest heat flux, and flying knife rotary sync phase.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing sheet length error (Q), steam valve adjustments (R), and glue applicator gap errors (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on corrugating roll surface temperature RTDs, web tension load cells, ultrasonic loop sensors, and rotary line encoders.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Web Wrap-Up Jam HH, Steam Overpressure HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering roll pre-heat, glue line prime, paper web threading, slow inching, speed acceleration ramp, bridge accumulation, continuous high-speed corrugating, order changeover flying splice, glue dam flush, roll retraction, controlled cooldown, and emergency web wrap-up fast stop.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with iec-st.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;. Zero unmatched delimiters.
   - Zero summaries, zero placeholders.
4. Save directly as a standard JSON dataset to data/swarm_raw/agent_<uuid>.json containing id, messages (user prompt, assistant response with fenced iec-st code), and metadata. Validate with python validate_iec.py and report final character count."""

    record = {
        "id": f"agent_{agent_uuid}",
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": assistant_content}
        ],
        "metadata": {
            "domain": "Paper Converting & Heavy Packaging Machinery",
            "system": "High-Speed Corrugated Cardboard Corrugator Line (400 m/min continuous web)",
            "function_block": "FB_Packaging_Corrugator_SingleFacer_FlyingShear",
            "characters": char_count,
            "lines": line_count,
            "validated": False,
            "tier": 4,
            "uuid": agent_uuid
        }
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
    print(f"Successfully saved to {filename}")

if __name__ == "__main__":
    main()
