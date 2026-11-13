# -*- coding: utf-8 -*-
"""
smt_builder/test_assemble.py
Assembles all sections and runs validate_iec_st.
"""

from header_io import get_header_and_io
from var_declarations import get_var_declarations
from phase1_tmr import get_phase1_tmr
from phase2_state_space import get_phase2_state_space
from phase3_mpc_pgd import get_phase3_mpc
from phase4_fsm import get_phase4_fsm
from phase5_alarms_status import get_phase5_alarms

import sys
sys.path.append("..")
from validate_iec import validate_iec_st

def assemble_st():
    parts = [
        get_header_and_io(),
        get_var_declarations(),
        get_phase1_tmr(),
        get_phase2_state_space(),
        get_phase3_mpc(),
        get_phase4_fsm(),
        get_phase5_alarms()
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_st()
    print("Total ST Code Length:", len(code), "characters")
    errors = validate_iec_st(code)
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(" -", e)
    else:
        print("SUCCESS! All ST validation checks passed with 0 errors!")
