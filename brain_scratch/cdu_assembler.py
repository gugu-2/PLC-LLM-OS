# -*- coding: utf-8 -*-
"""
Assembler and Parity Validator for FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace
"""

import sys
import os
import json
import uuid
import re

# Add both current dir and parent dir to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if parent_dir not in sys.path:
    sys.path.insert(0, parent_dir)

import generate_cdu_dataset_full as cdu_base
import cdu_phase1_tmr as cdu_p1
import cdu_phase2_observers as cdu_p2
import cdu_phase3_mpc as cdu_p3
import cdu_phase4_fsm as cdu_p4
import cdu_phase5_alarms as cdu_p5

def check_parity(st_text):
    print("Running Delimiter Parity Verification...")
    
    # Remove block comments (* ... *)
    clean_text = re.sub(r'\(\*[\s\S]*?\*\)', ' ', st_text)
    # Remove line comments // ...
    clean_text = re.sub(r'//.*', ' ', clean_text)
    # Remove string literals '...'
    clean_text = re.sub(r"'[^']*'", ' ', clean_text)
    
    # Tokenize words
    tokens = re.findall(r'\b[A-Za-z_][A-Za-z0-9_]*\b', clean_text)
    
    # Check IF vs END_IF
    if_count = 0
    end_if_count = 0
    case_count = 0
    end_case_count = 0
    for_count = 0
    end_for_count = 0
    while_count = 0
    end_while_count = 0
    var_count = 0
    end_var_count = 0
    fb_count = 0
    end_fb_count = 0
    
    # We should iterate through tokens carefully
    for t in tokens:
        tu = t.upper()
        if tu == 'IF':
            if_count += 1
        elif tu == 'END_IF':
            end_if_count += 1
        elif tu == 'CASE':
            case_count += 1
        elif tu == 'END_CASE':
            end_case_count += 1
        elif tu == 'FOR':
            for_count += 1
        elif tu == 'END_FOR':
            end_for_count += 1
        elif tu == 'WHILE':
            while_count += 1
        elif tu == 'END_WHILE':
            end_while_count += 1
        elif tu in ('VAR', 'VAR_INPUT', 'VAR_OUTPUT', 'VAR_IN_OUT', 'VAR_TEMP', 'VAR_STAT'):
            var_count += 1
        elif tu == 'END_VAR':
            end_var_count += 1
        elif tu == 'FUNCTION_BLOCK':
            fb_count += 1
        elif tu == 'END_FUNCTION_BLOCK':
            end_fb_count += 1
            
    print(f"  FUNCTION_BLOCK: {fb_count} | END_FUNCTION_BLOCK: {end_fb_count}")
    print(f"  VAR sections:   {var_count} | END_VAR:            {end_var_count}")
    print(f"  IF:             {if_count} | END_IF:             {end_if_count}")
    print(f"  CASE:           {case_count} | END_CASE:           {end_case_count}")
    print(f"  FOR:            {for_count} | END_FOR:            {end_for_count}")
    print(f"  WHILE:          {while_count} | END_WHILE:          {end_while_count}")
    
    assert fb_count == 1, f"FB count mismatch: {fb_count}"
    assert end_fb_count == 1, f"END_FB count mismatch: {end_fb_count}"
    assert var_count == end_var_count, f"VAR count mismatch: {var_count} vs {end_var_count}"
    assert if_count == end_if_count, f"IF count mismatch: {if_count} vs {end_if_count}"
    assert case_count == end_case_count, f"CASE count mismatch: {case_count} vs {end_case_count}"
    assert for_count == end_for_count, f"FOR count mismatch: {for_count} vs {end_for_count}"
    assert while_count == end_while_count, f"WHILE count mismatch: {while_count} vs {end_while_count}"
    print(">>> PARITY VERIFICATION PASSED PERFECTLY (100% EXACT PARITY) <<<")

def assemble():
    print("Assembling complete function block...")
    part0 = cdu_base.get_header_and_interfaces()
    part1 = cdu_p1.generate_phase1()
    part2 = cdu_p2.generate_phase2()
    part3 = cdu_p3.generate_phase3()
    part4 = cdu_p4.generate_phase4()
    part5 = cdu_p5.generate_phase5()
    
    st_code = f"{part0}\n{part1}\n{part2}\n{part3}\n{part4}\n{part5}"
    
    # Parity check
    check_parity(st_code)
    
    full_code = f"```iec-st\n{st_code}\n```"
    
    # Formulate Prompt
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Petrochemical Refining & Continuous Atmospheric Distillation - World-Scale 350,000 BPD Crude Distillation Unit (CDU) Atmospheric Pipestill & Multi-Zone Fired Heater: 120 MW Fuel Gas/Oil Multi-Burner Combustion, Decoupled Coil Outlet Temperature (COT) Control with Flue Gas O2 & CO Trim, Side-Stream Strippers for Heavy Naphtha, Kerosene, Diesel, and Atmospheric Gas Oil (AGO), Column Internal Vapor-Liquid Hydraulics & Flooding Observer, Overflash Zone Liquid Entrainment Prevention, Pumparound Dynamic Enthalpy Duty Balancing, and Desalter Crude Emulsion Water-in-Oil Fast Electrostatic Grid Tripping**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m3/h], [vol%], [ppm], [MW], [kV], [mA], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 60,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}
   with open(f\"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json\", \"w\", encoding=\"utf-8\") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Petrochemical Refining & Continuous Atmospheric Distillation"""

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_code}
        ]
    }
    
    # Target file
    unique_id = uuid.uuid4().hex[:8]
    out_dir = os.path.abspath("data/swarm_raw")
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"agent_{unique_id}.json")
    
    print(f"Writing dataset record to {out_file}...")
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"SUCCESS: Saved {len(full_code)} characters to {out_file}")
    
    # Reload and test
    with open(out_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["messages"]) == 2
    assert loaded["messages"][1]["content"].startswith("```iec-st\nFUNCTION_BLOCK FB_OilGas_ContinuousCrudeDistillation_CDU_AtmosphericFurnace")
    assert loaded["messages"][1]["content"].endswith("END_FUNCTION_BLOCK\n\n```")
    print(f"Verification completed successfully! JSON file valid and fully conforming.")
    return unique_id, len(full_code), out_file

if __name__ == "__main__":
    assemble()
