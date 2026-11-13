# semi_scrubber_builder/check_size.py
import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from mod_header_io import get_header_and_io
from mod_var_decl import get_var_declarations
from mod_phase0_matrices import get_phase0_code
from mod_phase1_tmr import get_phase1_code
from mod_phase2_cyber_physical import get_phase2_code
from mod_phase3_mpc import get_phase3_code
from mod_phase4_fsm import get_phase4_code
from mod_phase5_alarms import get_phase5_code
import validate_iec

def assemble():
    parts = [
        get_header_and_io(),
        get_var_declarations(),
        get_phase0_code(),
        get_phase1_code(),
        get_phase2_code(),
        get_phase3_code(),
        get_phase4_code(),
        get_phase5_code()
    ]
    return "\n\n".join(parts)

if __name__ == "__main__":
    code = assemble()
    lines = code.splitlines()
    print(f"Total lines: {len(lines)}")
    print(f"Total characters: {len(code)}")
    
    errs = validate_iec.validate_iec_st(code)
    if errs:
        print("Validation Errors:")
        for e in errs:
            print(" -", e)
    else:
        print("PERFECT VALIDATION: 0 errors!")
