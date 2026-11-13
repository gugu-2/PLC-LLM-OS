# mega_casting_builder/test_build.py

import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import build_header_io
import build_var
import build_phase1_init_matrices
import build_phase2_tmr_voting
import build_phase3_state_space_observer
import build_phase4_mpc_pgd
import build_phase5_fsm
import build_phase6_thermal_porosity
import build_phase7_alarms_telemetry
import build_footer
import validate_iec

def assemble_code():
    parts = [
        build_header_io.get_header_and_io(),
        build_var.get_var_declarations(),
        build_phase1_init_matrices.get_phase1_init_matrices(),
        build_phase2_tmr_voting.get_phase2_tmr_voting(),
        build_phase3_state_space_observer.get_phase3_state_space_observer(),
        build_phase4_mpc_pgd.get_phase4_mpc_pgd(),
        build_phase5_fsm.get_phase5_fsm(),
        build_phase6_thermal_porosity.get_phase6_thermal_porosity(),
        build_phase7_alarms_telemetry.get_phase7_alarms_telemetry(),
        build_footer.get_footer()
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_code()
    print(f"Total Structured Text character count: {len(code)}")
    print(f"Total lines: {len(code.splitlines())}")
    
    errs = validate_iec.validate_iec_st(code)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
    else:
        print("ALL IEC ST CHECKS PASSED WITH 0 ERRORS!")
