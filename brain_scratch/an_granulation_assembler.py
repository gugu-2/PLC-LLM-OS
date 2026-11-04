# -*- coding: utf-8 -*-
import sys
import os

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.getcwd())

from builder_part1 import get_header_and_vars
from builder_part2 import get_phase1_tmr
from builder_part3 import get_phase2_observers
from builder_part4 import get_phase3_mpc
from builder_part5 import get_phase4_fsm
from builder_part6 import get_phase5_alarms
from validate_iec import validate_iec_st

def assemble_an_granulation():
    p1 = get_header_and_vars()
    p2 = get_phase1_tmr()
    p3 = get_phase2_observers()
    p4 = get_phase3_mpc()
    p5 = get_phase4_fsm()
    p6 = get_phase5_alarms()

    full_st = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n\n{p5}\n\n{p6}"
    return full_st

if __name__ == "__main__":
    st_code = assemble_an_granulation()
    print(f"Total lines: {len(st_code.splitlines())}")
    print(f"Total characters: {len(st_code)}")
    errs = validate_iec_st(st_code)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print("  -", e)
    else:
        print("SUCCESS: ALL IEC ST CHECKS PASSED!")
