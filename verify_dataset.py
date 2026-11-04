# -*- coding: utf-8 -*-
import re
from test_generator import build_code

def check_parity(code):
    # Remove comments (* ... *) before checking tokens
    clean_code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)

    # Remove string literals
    clean_code = re.sub(r"'.*?'", '', clean_code)
    clean_code = re.sub(r'".*?"', '', clean_code)

    # Check tokens
    # Note: ELSIF contains IF if not matching word boundary properly, \bIF\b avoids ELSIF
    # But wait! \bIF\b matches 'IF' in 'END_IF' if not preceded by END_! So let's be very careful:
    # (?<!END_)IF\b
    if_count = len(re.findall(r'(?<!END_)IF\b', clean_code, re.IGNORECASE))
    # Wait, ELSIF has IF! We don't want ELSIF to count as IF:
    # (?<!END_)(?<!ELS)IF\b
    if_count = len(re.findall(r'(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    endif_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))

    case_count = len(re.findall(r'(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

    for_count = len(re.findall(r'(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))

    fb_count = len(re.findall(r'(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    endfb_count = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))

    var_input_count = len(re.findall(r'\bVAR_INPUT\b', clean_code, re.IGNORECASE))
    var_output_count = len(re.findall(r'\bVAR_OUTPUT\b', clean_code, re.IGNORECASE))
    var_internal_count = len(re.findall(r'(?<!END_)\bVAR\b', clean_code, re.IGNORECASE))
    total_var = var_input_count + var_output_count + var_internal_count
    endvar_count = len(re.findall(r'\bEND_VAR\b', clean_code, re.IGNORECASE))

    print(f"IF: {if_count}, END_IF: {endif_count}, Parity: {if_count == endif_count}")
    print(f"CASE: {case_count}, END_CASE: {endcase_count}, Parity: {case_count == endcase_count}")
    print(f"FOR: {for_count}, END_FOR: {endfor_count}, Parity: {for_count == endfor_count}")
    print(f"FUNCTION_BLOCK: {fb_count}, END_FUNCTION_BLOCK: {endfb_count}, Parity: {fb_count == endfb_count}")
    print(f"VAR sections (IN={var_input_count}, OUT={var_output_count}, INTERNAL={var_internal_count}): Total={total_var}, END_VAR: {endvar_count}, Parity: {total_var == endvar_count}")

    passed = (if_count == endif_count and 
              case_count == endcase_count and 
              for_count == endfor_count and 
              fb_count == endfb_count and 
              total_var == endvar_count)
    return passed

if __name__ == "__main__":
    code = build_code()
    print("Testing parity...")
    ok = check_parity(code)
    print("All Delimiters Parity Check Passed:", ok)
