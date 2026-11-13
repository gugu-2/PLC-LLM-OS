# copper_flotation_gen/check_size.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

import part1_header_io
import part2_var_declarations
import part3_phase0_init
import part4_phase1_tmr
import part5_phase2_state_space
import part6_phase3_mpc
import part7_phase4_fsm
import part8_phase5_alarms

st_code = (
    part1_header_io.get_header_and_io() + "\n" +
    part2_var_declarations.get_var_declarations() + "\n" +
    part3_phase0_init.get_phase0_init() + "\n" +
    part4_phase1_tmr.get_phase1_tmr() + "\n" +
    part5_phase2_state_space.get_phase2_state_space() + "\n" +
    part6_phase3_mpc.get_phase3_mpc() + "\n" +
    part7_phase4_fsm.get_phase4_fsm() + "\n" +
    part8_phase5_alarms.get_phase5_alarms()
)

print(f"Total ST code length: {len(st_code)} characters")
print(f"Total lines: {len(st_code.splitlines())}")
