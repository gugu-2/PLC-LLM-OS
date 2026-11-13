# hpdc_megacasting_builder/test_length.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phase1_tmr
import build_st_phase2_state_space
import build_st_phase3_mpc
import build_st_phase4_fsm
import build_st_phase5_thermal_die
import build_st_phase6_alarms_spc
import validate_iec

st_code = "\n".join([
    build_st_header_io.get_header_and_io(),
    build_st_var.get_var_declarations(),
    build_st_matrices.get_matrices_initialization(),
    build_st_phase1_tmr.get_phase1_tmr(),
    build_st_phase2_state_space.get_phase2_state_space(),
    build_st_phase3_mpc.get_phase3_mpc(),
    build_st_phase4_fsm.get_phase4_fsm(),
    build_st_phase5_thermal_die.get_phase5_thermal_die(),
    build_st_phase6_alarms_spc.get_phase6_alarms_spc()
])

print(f"Total Structured Text character count: {len(st_code)}")
print(f"Total lines: {len(st_code.splitlines())}")

errors = validate_iec.validate_iec_st(st_code)
if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(" -", e)
else:
    print("ALL IEC ST CHECKS PASSED WITH 0 ERRORS!")
