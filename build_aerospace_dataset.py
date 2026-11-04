# Build script for FB_Aerospace_FAL_Wingbox_Drilling_Fastening
# Lumina Elite Synthetic Data Architect

import json
import uuid
import re

def verify_parity(st_code: str):
    # Check parity of IF / END_IF, CASE / END_CASE, FOR / END_FOR, WHILE / END_WHILE
    # Remove comments (* ... *)
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', ' ', st_code)
    
    # Tokenize words
    words = re.findall(r'\b[A-Za-z0-9_]+\b', clean_code)
    
    # Check IF vs END_IF
    if_count = 0
    end_if_count = 0
    case_count = 0
    end_case_count = 0
    for_count = 0
    end_for_count = 0
    while_count = 0
    end_while_count = 0
    
    i = 0
    n = len(words)
    while i < n:
        w = words[i].upper()
        if w == 'IF':
            if i > 0 and words[i-1].upper() == 'END':
                pass # Already handled by END_IF if treated as one token, but let's check
            else:
                if_count += 1
        elif w == 'END_IF':
            end_if_count += 1
        elif w == 'CASE':
            case_count += 1
        elif w == 'END_CASE':
            end_case_count += 1
        elif w == 'FOR':
            for_count += 1
        elif w == 'END_FOR':
            end_for_count += 1
        elif w == 'WHILE':
            while_count += 1
        elif w == 'END_WHILE':
            end_while_count += 1
        i += 1
        
    print(f"Parity Audit:")
    print(f"  IF: {if_count} | END_IF: {end_if_count} -> Diff: {if_count - end_if_count}")
    print(f"  CASE: {case_count} | END_CASE: {end_case_count} -> Diff: {case_count - end_case_count}")
    print(f"  FOR: {for_count} | END_FOR: {end_for_count} -> Diff: {for_count - end_for_count}")
    print(f"  WHILE: {while_count} | END_WHILE: {end_while_count} -> Diff: {while_count - end_while_count}")
    
    assert if_count == end_if_count, f"IF parity mismatch: {if_count} vs {end_if_count}"
    assert case_count == end_case_count, f"CASE parity mismatch: {case_count} vs {end_case_count}"
    assert for_count == end_for_count, f"FOR parity mismatch: {for_count} vs {end_for_count}"
    assert while_count == end_while_count, f"WHILE parity mismatch: {while_count} vs {end_while_count}"
    print("ALL PARITY CHECKS PASSED PERFECTLY!")

print("Verifier function ready.")
