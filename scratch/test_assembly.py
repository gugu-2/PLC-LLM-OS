import sys
import os
import re

from sec1_vars import get_sec1
from sec2_init_tmr import get_sec2
from sec3_observers import get_sec3
from sec4_mpc import get_sec4
from sec5_fsm import get_sec5
from sec6_alarms import get_sec6

sys.path.append(os.path.abspath("."))
from validate_iec import validate_iec_st

def test_full_st():
    parts = [
        get_sec1(),
        get_sec2(),
        get_sec3(),
        get_sec4(),
        get_sec5(),
        get_sec6()
    ]
    full_code = "".join(parts)
    print("Full ST Code Length (characters):", len(full_code))
    
    errs = validate_iec_st(full_code)
    if errs:
        print("VALIDATION ERRORS FOUND:")
        for e in errs:
            print(" -", e)
    else:
        print("PERFECT! validate_iec_st passed with 0 errors!")

if __name__ == "__main__":
    test_full_st()
