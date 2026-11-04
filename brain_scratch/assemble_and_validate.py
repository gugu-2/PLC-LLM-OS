import os
import sys
import json
import uuid
import re

from part1_decl import get_part1
from part2_tmr import get_part2
from part3_physics import get_part3
from part4_mpc_fsm_alarms import get_part4

# User prompt
USER_PROMPT = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Construction Materials & Heavy Ceramics
- System: Automated Ceramic Tile & Technical Porcelain Manufacturing Complex: 2,000-Ton Hydraulic Dry-Powder Compaction Press (Proportional Servo Filling Feeder, Multi-Stage Proportional Tonnage De-Airing Stroke, Cavity Laser Thickness Profiler), High-Speed 4-Axis Setting/De-Hacking Robotic Gantry with Vacuum Foam Suction Gripper, and 120-Meter Continuous Roller Hearth Kiln (1,220°C Peak Firing, 48 Burner Groups with Oxygen Trim & Pressure Balance, Tile Skew / Breakage Optical Triangulation Detection, Rapid Air Quench & Slow Annealing Cooling Zones).
- Function Block Name: FB_Ceramics_HydraulicPress_RollerHearthKiln

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) capturing press hydraulic cylinder pressure, green tile density/thickness, kiln pre-heating/firing/cooling thermal profiles, and roller drive velocity.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing tile shrinkage deviation (Q), burner gas valve movements (R), and hydraulic pressure overshoot (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on press hydraulic transducers, optical tile thickness gauges, kiln thermocouples, and roller speed tachometers.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Hydraulic Burst HH, Kiln Over-Temperature HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering powder hopper charge, die fill, de-airing pre-compression, main compaction, tile ejection, robotic transfer, kiln pre-heating, vitrification firing, air quench, slow annealing, kiln exit sorting, and emergency hydraulic/gas slam-shut.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with iec-st.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;. Zero unmatched delimiters.
   - Zero summaries, zero placeholders (// ... rest of code).
4. Save directly as a standard JSON dataset to data/swarm_raw/agent_<uuid>.json containing id, messages (user prompt, assistant response with fenced iec-st code), and metadata. Validate with python validate_iec.py and report final character count."""

def assemble():
    p1 = get_part1()
    p2 = get_part2()
    p3 = get_part3()
    p4 = get_part4()
    
    full_st_code = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}"
    
    print(f"Total Structured Text character count: {len(full_st_code)} characters")
    
    # Internal Parity Audit
    open_c = full_st_code.count("(*")
    close_c = full_st_code.count("*)")
    print(f"Comments: (* = {open_c}, *) = {close_c}")
    assert open_c == close_c, f"Comment mismatch: {open_c} != {close_c}"
    
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', full_st_code)
    clean_code = re.sub(r'\'[^\']*\'', '', no_comments)
    
    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))
    fb_starts = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_ends = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    
    print(f"Parity Audit Results:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_starts} | END_FUNCTION_BLOCK: {fb_ends} (Match: {fb_starts == fb_ends})")
    
    assert ifs == end_ifs, f"IF/END_IF mismatch: {ifs} != {end_ifs}"
    assert cases == end_cases, f"CASE/END_CASE mismatch: {cases} != {end_cases}"
    assert fors == end_fors, f"FOR/END_FOR mismatch: {fors} != {end_fors}"
    assert whiles == end_whiles, f"WHILE/END_WHILE mismatch: {whiles} != {end_whiles}"
    assert fb_starts == fb_ends, f"FUNCTION_BLOCK/END_FUNCTION_BLOCK mismatch: {fb_starts} != {fb_ends}"
    
    # Assistant response format
    assistant_content = f"```iec-st\n{full_st_code}\n```"
    
    agent_id = "agent_2a7a703e"
    json_path = os.path.join(r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw", f"{agent_id}.json")
    
    data = {
        "id": agent_id,
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": assistant_content}
        ],
        "metadata": {
            "domain": "Construction Materials & Heavy Ceramics",
            "system": "Automated Ceramic Tile & Technical Porcelain Manufacturing Complex: 2,000-Ton Hydraulic Compaction Press & 120m Continuous Roller Hearth Kiln",
            "function_block": "FB_Ceramics_HydraulicPress_RollerHearthKiln",
            "character_count": len(assistant_content),
            "st_code_character_count": len(full_st_code),
            "model_architecture": "Discrete 8x8 State-Space + 5-Horizon Receding MPC + 2oo3 TMR + 12-State FSM + ISA-18.2"
        }
    }
    
    with open(json_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully saved dataset to: {json_path}")
    print(f"Assistant content character count: {len(assistant_content)}")
    return json_path

if __name__ == "__main__":
    assemble()
