# lyophilizer_builder/test_assembly.py

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
import build_st_phase2_sublimation
import build_st_phase3_state_space
import build_st_phase4_mpc
import build_st_phase5_cascade_stoppering
import build_st_phase6_fsm
import build_st_phase7_alarms_telemetry
import validate_iec

st_code = "\n".join([
    build_st_header_io.get_header_and_io(),
    build_st_var.get_var_declarations(),
    build_st_matrices.get_matrices_initialization(),
    build_st_phase1_tmr.get_phase1_tmr(),
    build_st_phase2_sublimation.get_phase2_sublimation(),
    build_st_phase3_state_space.get_phase3_state_space(),
    build_st_phase4_mpc.get_phase4_mpc(),
    build_st_phase5_cascade_stoppering.get_phase5_cascade_stoppering(),
    build_st_phase6_fsm.get_phase6_fsm(),
    build_st_phase7_alarms_telemetry.get_phase7_alarms_telemetry()
])

print(f"Total internal ST code length: {len(st_code)} characters")
errs = validate_iec.validate_iec_st(st_code)
if errs:
    print("VALIDATION ERRORS FOUND:")
    for e in errs:
        print(" -", e)
else:
    print("VALIDATION PASSED WITH 0 ERRORS!")
