# -*- coding: utf-8 -*-
"""
Validation and assembly script for FB_AbyssalGlider_BuoyancyEngine_PitchYawSync
"""

import os
import sys
import json
import uuid
import re

import glider_decl
import glider_tmr_teos
import glider_mpc_control
import glider_state_machine

def assemble_code():
    p1 = glider_decl.get_declarations().strip()
    p2 = glider_tmr_teos.get_tmr_and_teos().strip()
    p3 = glider_mpc_control.get_mpc_and_actuators().strip()
    p4 = glider_state_machine.get_state_machine().strip()
    
    # Combined Structured Text code
    st_code = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n"
    return st_code

def validate_code(st_code):
    print("=== VALIDATION REPORT ===")
    print(f"Total Character Count: {len(st_code)}")
    
    # 1. First line and last line checks
    lines = [l.strip() for l in st_code.strip().splitlines() if l.strip()]
    first_line = lines[0]
    last_line = lines[-1]
    print(f"First Line: {first_line}")
    print(f"Last Line:  {last_line}")
    assert first_line == "FUNCTION_BLOCK FB_AbyssalGlider_BuoyancyEngine_PitchYawSync", f"First line mismatch: {first_line}"
    assert last_line == "END_FUNCTION_BLOCK", f"Last line mismatch: {last_line}"
    
    # 2. Comment parity
    open_comments = st_code.count("(*")
    close_comments = st_code.count("*)")
    print(f"Comments: (* = {open_comments}, *) = {close_comments}")
    assert open_comments == close_comments, f"Comment mismatch: (* {open_comments} != *) {close_comments}"
    
    # Strip comments to validate keywords accurately
    # Regex for (* ... *) non-greedy multiline
    code_no_comments = re.sub(r'\(\*.*?\*\)', '', st_code, flags=re.DOTALL)
    
    # 3. IF / END_IF parity
    # Count IF tokens not inside words
    # Note: ELSIF also contains IF if using naive regex, so match whole word IF, but not ELSIF
    if_count = len(re.findall(r'\bIF\b', code_no_comments))
    elsif_count = len(re.findall(r'\bELSIF\b', code_no_comments))
    endif_count = len(re.findall(r'\bEND_IF\b', code_no_comments))
    print(f"Control Flow: IF = {if_count}, ELSIF = {elsif_count}, END_IF = {endif_count}")
    assert if_count == endif_count, f"IF/END_IF parity mismatch: IF={if_count}, END_IF={endif_count}"
    
    # 4. CASE / END_CASE parity
    case_count = len(re.findall(r'\bCASE\b', code_no_comments))
    endcase_count = len(re.findall(r'\bEND_CASE\b', code_no_comments))
    print(f"Control Flow: CASE = {case_count}, END_CASE = {endcase_count}")
    assert case_count == endcase_count, f"CASE/END_CASE parity mismatch: CASE={case_count}, END_CASE={endcase_count}"
    
    # 5. FOR / END_FOR parity
    for_count = len(re.findall(r'\bFOR\b', code_no_comments))
    endfor_count = len(re.findall(r'\bEND_FOR\b', code_no_comments))
    print(f"Control Flow: FOR = {for_count}, END_FOR = {endfor_count}")
    assert for_count == endfor_count, f"FOR/END_FOR parity mismatch: FOR={for_count}, END_FOR={endfor_count}"
    
    # 6. Physical Units in VAR_INPUT comments:
    # [bar], [m], [m/s], [deg], [mm], [kg/m3], [deg C], [mbar]
    required_units = ["[bar]", "[m]", "[m/s]", "[deg]", "[mm]", "[kg/m3]", "[deg C]", "[mbar]"]
    # Extract VAR_INPUT block
    var_input_match = re.search(r'VAR_INPUT(.*?)END_VAR', st_code, re.DOTALL)
    assert var_input_match, "VAR_INPUT block not found!"
    var_input_text = var_input_match.group(1)
    
    print("\n--- Required Units Check in VAR_INPUT ---")
    for u in required_units:
        found = u in var_input_text
        print(f"Unit {u:10s} : {'FOUND' if found else 'MISSING'}")
        assert found, f"Unit {u} missing from VAR_INPUT!"
        
    # 7. Check VAR_OUTPUT count
    var_output_match = re.search(r'VAR_OUTPUT(.*?)END_VAR', st_code, re.DOTALL)
    assert var_output_match, "VAR_OUTPUT block not found!"
    var_output_text = var_output_match.group(1)
    outputs = [l for l in var_output_text.splitlines() if ":" in l and ";" in l and not l.strip().startswith("(*")]
    print(f"\nTotal VAR_OUTPUT variables found: {len(outputs)} (Required min: 7)")
    assert len(outputs) >= 7, f"Not enough outputs: {len(outputs)}"
    
    # 8. Check VAR_INPUT count
    inputs = [l for l in var_input_text.splitlines() if ":" in l and ";" in l and not l.strip().startswith("(*")]
    print(f"Total VAR_INPUT variables found: {len(inputs)} (Required min: 8)")
    assert len(inputs) >= 8, f"Not enough inputs: {len(inputs)}"
    
    print("\n=== ALL CRITICAL RULES & PARITY CHECKS PASSED SUCCESSFULLY ===")
    return True

if __name__ == "__main__":
    code = assemble_code()
    validate_code(code)
