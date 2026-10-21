import sys
import os
import json
import uuid

# Helper to verify balance of IF/END_IF, CASE/END_CASE, FOR/END_FOR, WHILE/END_WHILE
def verify_st_parity(code_text):
    import re
    # Strip comments (* ... *)
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', code_text)
    # Strip strings '...'
    clean_code = re.sub(r'\'[^\']*\'', '', clean_code)
    
    # Check IF vs END_IF
    # Note: ELSIF does not introduce a new END_IF
    # Match IF not preceded by END_ or ELS
    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    
    # Check CASE vs END_CASE
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

    # Check FOR vs END_FOR
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))

    # Check WHILE vs END_WHILE
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))

    # Check FUNCTION_BLOCK vs END_FUNCTION_BLOCK
    fb_start = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_end = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))

    print(f"Parity Audit:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_start} | END_FUNCTION_BLOCK: {fb_end} (Match: {fb_start == fb_end})")

    assert ifs == end_ifs, f"IF / END_IF mismatch: {ifs} vs {end_ifs}"
    assert cases == end_cases, f"CASE / END_CASE mismatch: {cases} vs {end_cases}"
    assert fors == end_fors, f"FOR / END_FOR mismatch: {fors} vs {end_fors}"
    assert whiles == end_whiles, f"WHILE / END_WHILE mismatch: {whiles} vs {end_whiles}"
    assert fb_start == 1 and fb_end == 1, f"FUNCTION_BLOCK mismatch: {fb_start} vs {fb_end}"
    print("ALL PARITY CHECKS PASSED!")

print("Parity verification module ready")
