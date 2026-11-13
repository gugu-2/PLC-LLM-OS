# brewery_builder/test_validate.py
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import part1_header_io
import part2_var_declarations
import part3_phase0_init
import part4_phase1_tmr
import part5_phase2_state_space
import part6_phase3_mpc
import part7_phase4_fsm
import part8_phase5_alarms
import validate_iec

p1 = part1_header_io.get_part1()
p2 = part2_var_declarations.get_part2()
p3 = part3_phase0_init.get_part3()
p4 = part4_phase1_tmr.get_part4()
p5 = part5_phase2_state_space.get_part5()
p6 = part6_phase3_mpc.get_part6()
p7 = part7_phase4_fsm.get_part7()
p8 = part8_phase5_alarms.get_part8()

full_code = "\n".join([p1, p2, p3, p4, p5, p6, p7, p8])

errs = validate_iec.validate_iec_st(full_code)
if errs:
    print("VALIDATION ERRORS:")
    for e in errs:
        print("  -", e)
    sys.exit(1)
else:
    print("ST VALIDATION PASSED PERFECTLY with 0 errors!")
    sys.exit(0)
