# test_assemble_wte.py
import sys
from wte_generator.part1_header_io import get_part1_header_io
from wte_generator.part2_var import get_part2_var
from wte_generator.part3_init_tmr import get_part3_init_tmr
from wte_generator.part4_physics_statespace import get_part4_physics_statespace
from wte_generator.part5_fsm_alarms import get_part5_fsm_alarms

p1 = get_part1_header_io()
p2 = get_part2_var()
p3 = get_part3_init_tmr()
p4 = get_part4_physics_statespace()
p5 = get_part5_fsm_alarms()

full_st = p1 + "\n" + p2 + "\n" + p3 + "\n" + p4 + "\n" + p5

print(f"Total Characters: {len(full_st):,}")
print(f"Total Lines: {len(full_st.splitlines()):,}")

# Check parity
import re

def check_parity(code):
    # Strip comments
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
    
    # Counts
    if_count = len(re.findall(r'\bIF\b', clean_code))
    endif_count = len(re.findall(r'\bEND_IF\b', clean_code))
    
    case_count = len(re.findall(r'\bCASE\b', clean_code))
    endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code))
    
    for_count = len(re.findall(r'\bFOR\b', clean_code))
    endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code))
    
    var_count = len(re.findall(r'\bVAR\b', clean_code))
    var_input_count = len(re.findall(r'\bVAR_INPUT\b', clean_code))
    var_output_count = len(re.findall(r'\bVAR_OUTPUT\b', clean_code))
    end_var_count = len(re.findall(r'\bEND_VAR\b', clean_code))
    
    fb_count = len(re.findall(r'\bFUNCTION_BLOCK\b', clean_code))
    endfb_count = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code))
    
    print(f"IF: {if_count} | END_IF: {endif_count} | Parity: {if_count == endif_count}")
    print(f"CASE: {case_count} | END_CASE: {endcase_count} | Parity: {case_count == endcase_count}")
    print(f"FOR: {for_count} | END_FOR: {endfor_count} | Parity: {for_count == endfor_count}")
    print(f"VAR total sections: {var_count + var_input_count + var_output_count} | END_VAR: {end_var_count}")
    print(f"FUNCTION_BLOCK: {fb_count} | END_FUNCTION_BLOCK: {endfb_count}")
    
    return (if_count == endif_count and case_count == endcase_count and 
            for_count == endfor_count and fb_count == endfb_count)

ok = check_parity(full_st)
print(f"Parity check passed: {ok}")
