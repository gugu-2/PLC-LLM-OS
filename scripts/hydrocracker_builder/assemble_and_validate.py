# -*- coding: utf-8 -*-
"""
Assembler and Validator for FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench
"""

import os
import sys

from p1_header_io import get_header_and_io
from p2_vars import get_var_block
from p3_init_and_tmr import get_init_and_tmr_block
from p4_observers_and_statespace import get_observers_and_statespace_block
from p5_mpc import get_mpc_block
from p6_fsm import get_fsm_block
from p7_alarms_and_packing import get_alarms_and_packing_block

def assemble_st():
    parts = [
        get_header_and_io(),
        get_var_block(),
        get_init_and_tmr_block(),
        get_observers_and_statespace_block(),
        get_mpc_block(),
        get_fsm_block(),
        get_alarms_and_packing_block()
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_st()
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total characters: {len(code)}")
