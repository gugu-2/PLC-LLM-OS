# brain_scratch/ccgt_builder/test_assemble.py
import sys
import os

from header_and_io import get_header_and_io
from var_declarations import get_var_declarations
from phases_1_to_3 import get_phases_1_to_3
from phase_4_thermo import get_phase_4_thermo
from phases_5_and_6 import get_phases_5_and_6

# Add parent directory to sys.path to import validate_iec
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from validate_iec import validate_iec_st

header = get_header_and_io()
var_decl = get_var_declarations()
p1_3 = get_phases_1_to_3()
p4 = get_phase_4_thermo()
p5_6 = get_phases_5_and_6()

full_st = f"{header}\n{var_decl}\n{p1_3}\n{p4}\n{p5_6}"

print(f"Total characters: {len(full_st)}")
print(f"Total lines: {len(full_st.splitlines())}")

errors = validate_iec_st(full_st)
if errors:
    print("ERRORS FOUND:")
    for e in errors:
        print(" -", e)
else:
    print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
