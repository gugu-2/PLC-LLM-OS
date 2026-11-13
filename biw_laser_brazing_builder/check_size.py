# biw_laser_brazing_builder/check_size.py
import os
import sys

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

p1 = part1_header_io.get_header_and_io()
p2 = part2_var_declarations.get_var_declarations()
p3 = part3_phase0_init.get_phase0_init()
p4 = part4_phase1_tmr.get_phase1_tmr()
p5 = part5_phase2_state_space.get_phase2_state_space()
p6 = part6_phase3_mpc.get_phase3_mpc()
p7 = part7_phase4_fsm.get_phase4_fsm()
p8 = part8_phase5_alarms.get_phase5_alarms()

total = p1 + "\n" + p2 + "\n" + p3 + "\n" + p4 + "\n" + p5 + "\n" + p6 + "\n" + p7 + "\n" + p8

print(f"Part 1 Header & IO: {len(p1)} chars")
print(f"Part 2 Declarations: {len(p2)} chars")
print(f"Part 3 Init: {len(p3)} chars")
print(f"Part 4 TMR: {len(p4)} chars")
print(f"Part 5 State Space: {len(p5)} chars")
print(f"Part 6 MPC: {len(p6)} chars")
print(f"Part 7 FSM: {len(p7)} chars")
print(f"Part 8 Alarms: {len(p8)} chars")
print(f"TOTAL: {len(total)} chars")
