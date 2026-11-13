# trt_builder/test_length.py
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import st_header_io
import st_var
import st_matrices
import st_phase1_tmr
import st_phase2_state_space
import st_phase3_mpc
import st_phase4_fsm
import st_phase5_alarms_diagnostics
import validate_iec

st_code = "\n".join([
    st_header_io.get_header_and_io(),
    st_var.get_var_declarations(),
    st_matrices.get_matrices_initialization(),
    st_phase1_tmr.get_phase1_tmr(),
    st_phase2_state_space.get_phase2_state_space(),
    st_phase3_mpc.get_phase3_mpc(),
    st_phase4_fsm.get_phase4_fsm(),
    st_phase5_alarms_diagnostics.get_phase5_alarms_diagnostics()
])

print(f"Total ST code length: {len(st_code)} characters")
print(f"Total lines: {len(st_code.splitlines())}")

errs = validate_iec.validate_iec_st(st_code)
if errs:
    print("VALIDATION FAILED with errors:")
    for e in errs:
        print(" -", e)
else:
    print("ALL IEC-ST VALIDATION CHECKS PASSED PERFECTLY!")
