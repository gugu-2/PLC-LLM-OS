# brewery_builder/check_size.py
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

p1 = part1_header_io.get_part1()
p2 = part2_var_declarations.get_part2()
p3 = part3_phase0_init.get_part3()
p4 = part4_phase1_tmr.get_part4()
p5 = part5_phase2_state_space.get_part5()
p6 = part6_phase3_mpc.get_part6()
p7 = part7_phase4_fsm.get_part7()
p8 = part8_phase5_alarms.get_part8()

full_code = "\n".join([p1, p2, p3, p4, p5, p6, p7, p8])

print(f"Part 1: {len(p1)} chars")
print(f"Part 2: {len(p2)} chars")
print(f"Part 3: {len(p3)} chars")
print(f"Part 4: {len(p4)} chars")
print(f"Part 5: {len(p5)} chars")
print(f"Part 6: {len(p6)} chars")
print(f"Part 7: {len(p7)} chars")
print(f"Part 8: {len(p8)} chars")
print(f"Total full_code length: {len(full_code)} characters")
