# assemble.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from header_io import generate_header_io
from var_internal import generate_var_internal
from phase0_matrices import generate_phase0
from phase1_tmr import generate_phase1
from phase2_cyber_physical import generate_phase2
from phase3_mpc import generate_phase3
from phase4_fsm import generate_phase4
from phase5_alarms import generate_phase5

def assemble_code():
    parts = [
        generate_header_io(),
        generate_var_internal(),
        generate_phase0(),
        generate_phase1(),
        generate_phase2(),
        generate_phase3(),
        generate_phase4(),
        generate_phase5()
    ]
    full_code = "\n".join(parts)
    return full_code

if __name__ == "__main__":
    code = assemble_code()
    lines = code.splitlines()
    print(f"Total lines: {len(lines)}")
    print(f"Total characters: {len(code)}")
