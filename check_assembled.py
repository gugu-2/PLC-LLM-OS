# check_assembled.py
import sys
sys.path.append("tubular_gen")

from part1_header_io import header_io_text
from part2_vars import vars_text
from part3_tmr_kinetics import tmr_kinetics_text
from part4_mpc import mpc_text
from part5_fsm import fsm_text
from part6_dump_alarms import dump_alarms_text

full_code = header_io_text.strip() + "\n\n" + \
            vars_text.strip() + "\n\n" + \
            tmr_kinetics_text.strip() + "\n\n" + \
            mpc_text.strip() + "\n\n" + \
            fsm_text.strip() + "\n\n" + \
            dump_alarms_text.strip()

print(f"Total ST code length: {len(full_code)} characters")
print(f"Total lines: {len(full_code.splitlines())}")

from validate_iec import validate_iec_st
errs = validate_iec_st(full_code)
if errs:
    print("Validation errors:")
    for e in errs:
        print(" -", e)
else:
    print("validate_iec_st PASSED with zero errors!")
