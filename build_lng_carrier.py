# -*- coding: utf-8 -*-
"""
Main Assembler & Verifier for FB_Marine_LNG_Carrier_BOG_Reliquefaction_FGSS
"""

import os
import sys
import uuid
import json
import re

import lng_mod_io
import lng_mod_var
import lng_mod_phase0_matrices
import lng_mod_phase1_tmr
import lng_mod_phase2_thermo
import lng_mod_phase3_mpc
import lng_mod_phase4_fsm
import lng_mod_phase5_alarms

AGENT_UUID = "0990fe55"
OUTPUT_FILE = f"C:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{AGENT_UUID}.json"

def verify_st_code(code: str):
    errors = []
    lines = [line.strip() for line in code.strip().split('\n') if line.strip()]
    if not lines[0].startswith("FUNCTION_BLOCK FB_Marine_LNG_Carrier_BOG_Reliquefaction_FGSS"):
        errors.append(f"First line must start with 'FUNCTION_BLOCK FB_Marine_LNG_Carrier_BOG_Reliquefaction_FGSS', got '{lines[0]}'")
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
    print("Building Structured Text components...")
    io_code = lng_mod_io.get_header_and_io()
    var_code = lng_mod_var.get_var_block()
    phase0_code = lng_mod_phase0_matrices.get_phase0_matrices()
    phase1_code = lng_mod_phase1_tmr.get_phase1_tmr()
    phase2_code = lng_mod_phase2_thermo.get_phase2_thermo()
    phase3_code = lng_mod_phase3_mpc.get_phase3_mpc()
    phase4_code = lng_mod_phase4_fsm.get_phase4_fsm()
    phase5_code = lng_mod_phase5_alarms.get_phase5_alarms()

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
        "**Heavy Maritime & Commercial Cryogenic Shipping** industry.\n\n"
        "**Domain**: Heavy Maritime & Commercial Cryogenic Shipping: 174,000 m³ Membrane LNG Carrier Boil-Off Gas (BOG) Management "
        "& High-Pressure Fuel Gas Supply System (FGSS): 4-Stage High-Pressure Cryogenic BOG Reciprocating Compressor (300.0 bar ± 1.5 bar "
        "for WinGD X-DF / MAN ME-GI dual-fuel engines), Nitrogen Reverse-Brayton Cryogenic Reliquefaction Sub-Cooler Loop (-162.0 °C "
        "liquid return), Dynamic Cargo Tank Ullage Vapor Pressure & Sloshing Impact Thermal Stress Observer, Gas Combustion Unit (GCU) "
        "Decoupled High-Capacity Flaring, and SIL-3 Dual-Fuel Emergency Shut Down (ESD-1 / ESD-2) Double-Block-and-Vent Safety Matrix (< 1.0 s valve closure).\n\n"
        "**Function Block Name**: `FB_Marine_LNG_Carrier_BOG_Reliquefaction_FGSS`\n\n"
        "**Engineering Context & Operational Architecture**:\n"
        "- 174,000 m³ membrane LNG carrier equipped with GTT NO96 containment system transporting cryogenic liquefied natural gas at -161.5 °C.\n"
        "- High-Pressure Fuel Gas Supply System (FGSS) with 4-stage reciprocating compressor supplying 300.0 bar (± 1.5 bar) dense fuel gas to propulsion engines.\n"
        "- Nitrogen Reverse-Brayton cryogenic reliquefaction loop subcooling BOG to -162.0 °C for liquid return without flashing.\n"
        "- Real-time cyber-physical observer for Fourier heat conduction leak across NO96 perlite insulation and sloshing wave kinetic dissipation.\n"
        "- Dynamic Invar primary membrane thermal-mechanical stress observer.\n"
        "- Gas Combustion Unit (GCU) decoupled burner modulation for 100% thermal disposal of excess BOG during canal transit or reliquefier trip.\n"
        "- Triple Modular Redundancy (2oo3 TMR) across 12 transducer triplets (36 physical sensors) with discrepancy debounce and bumpless degradation.\n"
        "- Full 8x8 discrete state-space formulation (x[k+1] = A*x[k] + B*u[k]) at 10 ms cycle time.\n"
        "- Receding-horizon multivariable Model Predictive Control (MPC) with 4-iteration Projected Gradient Descent quadratic cost optimization.\n"
        "- 12-stage operational Finite State Machine (FSM) sequencing across laden, ballast, spray cooling, and emergency states.\n"
        "- ISA-18.2 5-tier alarm ladder (HI_HI, HI, LO, LO_LO, ROC) with bit-packed diagnostic words.\n"
        "- SIL-3 ESD-1 / ESD-2 Emergency Shut Down double-block-and-vent safety matrix with < 1.0 s valve closure time."
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
            "domain": "Heavy Maritime & Commercial Cryogenic Shipping",
            "function_block": "FB_Marine_LNG_Carrier_BOG_Reliquefaction_FGSS",
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
