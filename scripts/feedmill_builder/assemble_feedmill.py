# scripts/feedmill_builder/assemble_feedmill.py
# -*- coding: utf-8 -*-

import os
import sys

from part1_header_io import get_header_and_io
from part2_var import get_var_block
from part3_phase0_init import get_phase0_block
from part4_phase1_tmr import get_phase1_block
from part5_phase2_physics import get_phase2_block
from part6_phase3_mpc import get_phase3_block
from part7_phase4_fsm import get_phase4_block
from part8_phase5_alarms import get_phase5_block

def assemble_st_code():
    parts = [
        get_header_and_io(),
        get_var_block(),
        get_phase0_block(),
        get_phase1_block(),
        get_phase2_block(),
        get_phase3_block(),
        get_phase4_block(),
        get_phase5_block()
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_st_code()
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total characters: {len(code)}")
