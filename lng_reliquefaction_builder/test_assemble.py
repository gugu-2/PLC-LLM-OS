# lng_reliquefaction_builder/test_assemble.py
import sys
import os

from declarations import get_declarations
from phase1_tmr import get_phase1
from phase2_physics import get_phase2
from phase3_mpc import get_phase3
from phase4_fsm import get_phase4
from phase5_alarms import get_phase5

sys.path.append(os.path.abspath("."))
from validate_iec import validate_iec_st

def assemble_code():
    parts = [
        get_declarations(),
        get_phase1(),
        get_phase2(),
        get_phase3(),
        get_phase4(),
        get_phase5()
    ]
    return "\n\n".join(parts)

if __name__ == "__main__":
    code = assemble_code()
    print(f"Total Assembled Code Length: {len(code)} characters")
    print(f"Total Lines: {len(code.splitlines())}")
    errors = validate_iec_st(code)
    if errors:
        print("VALIDATION ERRORS:")
        for err in errors:
            print(" - ", err)
    else:
        print("PERFECT VALIDATION: 0 ERRORS!")
