# pharma_tableting_builder/assemble_pharma.py
import os
import sys

pkg_dir = os.path.dirname(os.path.abspath(__file__))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)

from part1_decl import get_part1
from part2_init_matrices import get_part2
from part3_tmr_voting import get_part3
from part4_state_space_mpc import get_part4
from part5_fsm import get_part5
from part6_compaction_reject import get_part6
from part7_alarms_diagnostics import get_part7

def assemble_code():
    parts = [
        get_part1(),
        get_part2(),
        get_part3(),
        get_part4(),
        get_part5(),
        get_part6(),
        get_part7()
    ]
    return "\n\n".join(parts)

if __name__ == "__main__":
    code = assemble_code()
    print(f"Total IEC ST Code Characters: {len(code)}")
    print(f"Total Lines: {len(code.splitlines())}")
