import os
import sys

sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("scratch"))

from generate_tunnel_oven import generate_tunnel_oven_code
from validate_iec import validate_iec_st

st_code = generate_tunnel_oven_code()
errors = validate_iec_st(st_code)

if errors:
    print("VALIDATION ERRORS FOUND:")
    for e in errors:
        print("  -", e)
    sys.exit(1)
else:
    print("ST CODE VALIDATION PASSED COMPLETELY!")
