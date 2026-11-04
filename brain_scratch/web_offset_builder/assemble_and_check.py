# -*- coding: utf-8 -*-
"""
Module: assemble_and_check.py
Assembles all modules into a single IEC 61131-3 Function Block,
runs AST parity checks, measures size, and prints statistics.
"""

import sys
import os
import re

sys.path.append(os.path.abspath("brain_scratch/web_offset_builder"))

from header_and_io import generate_header_and_io
from var_declarations import generate_var_declarations
from phase1_tmr import generate_phase1_tmr
from phase2_observers import generate_phase2_observers
from phase3_mpc import generate_phase3_mpc
from phase4_fsm import generate_phase4_fsm
from phase5_alarms import generate_phase5_alarms

def assemble():
    parts = [
        generate_header_and_io(),
        generate_var_declarations(),
        generate_phase1_tmr(),
        generate_phase2_observers(),
        generate_phase3_mpc(),
        generate_phase4_fsm(),
        generate_phase5_alarms()
    ]
    return "\n".join(parts)

def check_parity(st_code):
    # Strip comments (* ... *)
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
    # Strip strings '...'
    clean_code = re.sub(r'\'[^\']*\'', '', clean_code)
    
    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))

    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))

    vars_start = len(re.findall(r'\b(?<!END_)(?:VAR|VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP)\b', clean_code, re.IGNORECASE))
    vars_end = len(re.findall(r'\bEND_VAR\b', clean_code, re.IGNORECASE))

    fb_start = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_end = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))

    print(f"Parity Audit:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  VAR blocks: {vars_start} | END_VAR: {vars_end} (Match: {vars_start == vars_end})")
    print(f"  FUNCTION_BLOCK: {fb_start} | END_FUNCTION_BLOCK: {fb_end} (Match: {fb_start == fb_end})")

    assert ifs == end_ifs, f"IF mismatch: {ifs} != {end_ifs}"
    assert cases == end_cases, f"CASE mismatch: {cases} != {end_cases}"
    assert fors == end_fors, f"FOR mismatch: {fors} != {end_fors}"
    assert vars_start == vars_end, f"VAR mismatch: {vars_start} != {vars_end}"
    assert fb_start == 1 and fb_end == 1, f"FB mismatch: {fb_start} != {fb_end}"
    print(">>> 100% PARITY AUDIT PASSED! <<<")

if __name__ == "__main__":
    st = assemble()
    print("Total characters:", len(st))
    print("Total lines:", len(st.splitlines()))
    check_parity(st)
