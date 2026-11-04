import os, sys, json, uuid, re

workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scratch"))
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scripts"))

from gen_part1_header import get_header
from gen_part2_io import get_io
from gen_part3_vars import get_vars
from gen_part4_init import get_init_logic
from gen_part5_tmr import get_tmr_logic
from gen_part6_observers import get_observers_logic
from gen_part7_ss_mpc import get_ss_mpc_logic
from gen_part8_fsm import get_fsm_logic
from gen_part9_alarms import get_alarms_logic
from linter import ST_Linter

code_st = (
    get_header().strip() + "\n\n" +
    get_io().strip() + "\n\n" +
    get_vars().strip() + "\n\n" +
    get_init_logic().strip() + "\n\n" +
    get_tmr_logic().strip() + "\n\n" +
    get_observers_logic().strip() + "\n\n" +
    get_ss_mpc_logic().strip() + "\n\n" +
    get_fsm_logic().strip() + "\n\n" +
    get_alarms_logic().strip()
)

# Detailed AST & Delimiter Parity Checks
clean_code = re.sub(r'\(\*.*?\*\)', '', code_st, flags=re.DOTALL)
clean_code = re.sub(r'//.*', '', clean_code)

if_count = len(re.findall(r'\bIF\b', clean_code, re.IGNORECASE))
endif_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
for_count = len(re.findall(r'\bFOR\b', clean_code, re.IGNORECASE))
endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
case_count = len(re.findall(r'\bCASE\b', clean_code, re.IGNORECASE))
endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

print(f"IF / END_IF: {if_count} / {endif_count}")
print(f"FOR / END_FOR: {for_count} / {endfor_count}")
print(f"CASE / END_CASE: {case_count} / {endcase_count}")

assert if_count == endif_count, f"Mismatched IF/END_IF: {if_count} vs {endif_count}"
assert for_count == endfor_count, f"Mismatched FOR/END_FOR: {for_count} vs {endfor_count}"
assert case_count == endcase_count, f"Mismatched CASE/END_CASE: {case_count} vs {endcase_count}"

first_line = code_st.strip().splitlines()[0]
last_line = code_st.strip().splitlines()[-1]

print(f"First line: '{first_line}'")
print(f"Last line: '{last_line}'")

assert first_line == "FUNCTION_BLOCK FB_Mining_SAGMill_GrindingCircuit_AcousticEar"
assert last_line == "END_FUNCTION_BLOCK"

valid, msg = ST_Linter.verify_code(code_st)
assert valid, f"Linter error: {msg}"

print("All validations PASSED!")
