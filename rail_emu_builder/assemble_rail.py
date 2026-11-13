# rail_emu_builder/assemble_rail.py
import sys
import os

from part1_decl import get_part1
from part2_matrices import get_part2
from part3_tmr_observer import get_part3
from part4_mpc import get_part4
from part5_foc_panto_brakes import get_part5
from part6_wssp_fsm import get_part6
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
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_code()
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total characters: {len(code)}")
