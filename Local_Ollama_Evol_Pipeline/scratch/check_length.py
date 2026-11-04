import os, sys

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
    get_header() + "\n" +
    get_io() + "\n" +
    get_vars() + "\n" +
    get_init_logic() + "\n" +
    get_tmr_logic() + "\n" +
    get_observers_logic() + "\n" +
    get_ss_mpc_logic() + "\n" +
    get_fsm_logic() + "\n" +
    get_alarms_logic()
)

print(f"Total lines: {len(code_st.splitlines())}")
print(f"Total characters: {len(code_st)}")

valid, msg = ST_Linter.verify_code(code_st)
print(f"Linter result: valid={valid}, msg='{msg}'")
