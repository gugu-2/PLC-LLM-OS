# -*- coding: utf-8 -*-
"""
Assembler, Validator & JSON Generator for FB_Automotive_BIW_GeoFraming_MultiRobotWelding
Agent UUID: f16a9cdb
"""

import os
import sys
import uuid
import json
import re

import biw_mod_io
import biw_mod_var
import biw_mod_phase0_matrices
import biw_mod_phase1_tmr
import biw_mod_phase2_cyberphysical
import biw_mod_phase3_mpc
import biw_mod_phase4_fsm
import biw_mod_phase5_alarms

AGENT_UUID = "f16a9cdb"
OUTPUT_FILE = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{AGENT_UUID}.json"

def verify_st_code(code: str):
    errors = []
    lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
    if not lines[0].startswith("FUNCTION_BLOCK FB_Automotive_BIW_GeoFraming_MultiRobotWelding"):
        errors.append(f"First line must start with 'FUNCTION_BLOCK FB_Automotive_BIW_GeoFraming_MultiRobotWelding', got '{lines[0]}'")
    if not lines[-1].startswith("END_FUNCTION_BLOCK"):
        errors.append(f"Last line must be 'END_FUNCTION_BLOCK', got '{lines[-1]}'")
        
    var_in_count = len(re.findall(r'\bVAR_INPUT\b', code))
    end_var_count = len(re.findall(r'\bEND_VAR\b', code))
    var_out_count = len(re.findall(r'\bVAR_OUTPUT\b', code))
    var_count = len(re.findall(r'\bVAR\b', code))
    
    total_var_opens = var_in_count + var_out_count + var_count
    if total_var_opens != end_var_count:
        errors.append(f"VAR blocks open ({total_var_opens}) != END_VAR ({end_var_count})")
        
    # Check physical units in VAR_INPUT
    bracket_units = re.findall(r'\[[a-zA-Z0-9/%^°\-_ ]+\]', code)
    if len(bracket_units) < 10:
        errors.append(f"Too few physical units found in comments ({len(bracket_units)} found)")
        
    # Comment parity
    open_comments = code.count("(*")
    close_comments = code.count("*)")
    if open_comments != close_comments:
        errors.append(f"Comment mismatch: (* count ({open_comments}) != *) count ({close_comments})")

    # Remove strings and comments before checking IF/CASE/FOR parity
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
    clean_code = re.sub(r'//.*', '', clean_code)
    clean_code = re.sub(r"'[^']*'", '', clean_code)
    clean_code = re.sub(r'"[^"]*"', '', clean_code)
    
    tokens = re.findall(r'\b(?:IF|ELSIF|END_IF|CASE|END_CASE|FOR|END_FOR)\b', clean_code)
    
    if_count = 0
    end_if_count = 0
    case_count = 0
    end_case_count = 0
    for_count = 0
    end_for_count = 0
    
    for t in tokens:
        if t == 'IF':
            if_count += 1
        elif t == 'END_IF':
            end_if_count += 1
        elif t == 'CASE':
            case_count += 1
        elif t == 'END_CASE':
            end_case_count += 1
        elif t == 'FOR':
            for_count += 1
        elif t == 'END_FOR':
            end_for_count += 1
            
    if if_count != end_if_count:
        errors.append(f"IF count ({if_count}) != END_IF count ({end_if_count})")
    if case_count != end_case_count:
        errors.append(f"CASE count ({case_count}) != END_CASE count ({end_case_count})")
    if for_count != end_for_count:
        errors.append(f"FOR count ({for_count}) != END_FOR count ({end_for_count})")
        
    char_count = len(code)
    line_count = len(code.split('\n'))
    
    return errors, char_count, line_count, if_count, end_if_count, case_count, end_case_count, for_count, end_for_count

def build_full_dataset():
    print("Building Structured Text components for FB_Automotive_BIW_GeoFraming_MultiRobotWelding...")
    io_code = biw_mod_io.get_header_and_io()
    var_code = biw_mod_var.get_var_block()
    phase0_code = biw_mod_phase0_matrices.get_phase0_matrices()
    phase1_code = biw_mod_phase1_tmr.get_phase1_tmr()
    phase2_code = biw_mod_phase2_cyberphysical.get_phase2_cyberphysical()
    phase3_code = biw_mod_phase3_mpc.get_phase3_mpc()
    phase4_code = biw_mod_phase4_fsm.get_phase4_fsm()
    phase5_code = biw_mod_phase5_alarms.get_phase5_alarms()

    full_st_code = "\n\n".join([
        io_code,
        var_code,
        phase0_code,
        phase1_code,
        phase2_code,
        phase3_code,
        phase4_code,
        phase5_code
    ])

    print("Verifying IEC 61131-3 syntax and parity...")
    errors, chars, lines, if_c, end_if_c, case_c, end_case_c, for_c, end_for_c = verify_st_code(full_st_code)

    print(f"Total Lines: {lines}")
    print(f"Total Characters: {chars}")
    print(f"IF / END_IF: {if_c} / {end_if_c}")
    print(f"CASE / END_CASE: {case_c} / {end_case_c}")
    print(f"FOR / END_FOR: {for_c} / {end_for_c}")

    if errors:
        print("VERIFICATION FAILED:")
        for e in errors:
            print(f"  - {e}")
        return False

    print("ST code verification PASSED 100%!")

    prompt = (
        "You are generating a SINGLE ultra-dense, mathematically rigorous IEC 61131-3 Structured Text dataset for the "
        "**Automotive Body-in-White (BIW) Manufacturing** industry (Industry Rank #1 - Highest Global PLC Demand).\n\n"
        "**Domain**: Automotive Body-in-White (BIW) Manufacturing: High-Speed Automotive Flexible Body-in-White (BIW) Geo-Framing Station: "
        "14-Robot Coordinated Multi-Spot & Laser Seam Welding Jig (45.0 s cycle time, 0.05 mm structural body framing tolerance), "
        "Multi-Model Roller Skid Conveyor Lifter Pacing (payload 1,850 kg), Dynamic Servo Welding Gun Adaptive Resistance & Expulsion Feedback "
        "(welding current 14.5 kA, dynamic tip force 4.5 kN), Pneumatic Clamp Sequence Monitoring with Inductive Sensor Dual-Channel Discrepancy, "
        "and ISO 13849 PL e / SIL-3 Safety Light Curtain Zone Muting Interlocks.\n\n"
        "**Function Block Name**: `FB_Automotive_BIW_GeoFraming_MultiRobotWelding`\n\n"
        "**Engineering Context & Operational Architecture**:\n"
        "- High-speed flexible framing station coordinating 14 industrial articulating 6-axis manipulators (8 spot welding robots with 7th-axis integrated servo guns, 2 roof seam laser brazing robots with optical seam tracking, and 4 respot geometry reinforcement robots).\n"
        "- Structural framing side gates (3,500 kg each) docking into NC locating datum with 4-point pneumatic/hydraulic wedge pin locks (0.05 mm structural framing tolerance).\n"
        "- Friction roller skid conveyor transporting 1,850 kg vehicle body plus 650 kg pallet (2,500 kg total payload) with synchronous 4-corner servo lifter (650.0 mm lift stroke).\n"
        "- 2oo3 Triple Modular Redundancy (TMR) across 11 critical sensor triplets with configurable discrepancy debounce timers and bumpless degradation.\n"
        "- Full 8x8 discrete state-space formulation (x[k+1] = A*x[k] + B*u[k]) at 2 ms cycle modeling dynamic Joulean heat generation, contact resistance drop, mechanical framing compliance, lifter eccentric momentum, and multi-robot trajectory synchronization.\n"
        "- Receding-horizon Model Predictive Control (MPC) quadratic cost functional with projected gradient descent optimizing servo gun approach speed, dynamic squeeze force profile, and skid lifter deceleration to eliminate spatter expulsion.\n"
        "- 12-stage operational Finite State Machine (FSM) sequencing across ingress, pin lift, clamping, 14-robot welding, laser brazing, unlatching, and egress.\n"
        "- Full ISA-18.2 5-tier alarm ladder (HI_HI, HI, LO, LO_LO, ROC) with bit-packed diagnostic status words.\n"
        "- ISO 13849-1 Category 4 / PL e and IEC 62061 SIL-3 perimeter safety light curtain zone muting and emergency halt interlocks."
    )

    assistant_output = f"```iec-st\n{full_st_code}\n```"

    record = {
        "id": f"synthetic_v3_{AGENT_UUID}",
        "instruction": prompt,
        "input": "",
        "output": assistant_output,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_output}
        ],
        "metadata": {
            "domain": "Automotive Body-in-White (BIW) Manufacturing",
            "function_block": "FB_Automotive_BIW_GeoFraming_MultiRobotWelding",
            "version": "v3_cyberphysical_max",
            "lines": lines,
            "characters": chars,
            "validated": True
        }
    }

    os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {OUTPUT_FILE}")
    print(f"JSON File size: {os.path.getsize(OUTPUT_FILE):,} bytes")
    return True

if __name__ == "__main__":
    success = build_full_dataset()
    if not success:
        sys.exit(1)
