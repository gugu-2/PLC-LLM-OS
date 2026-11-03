# build_dyno_coldtest.py
import re
import json
import uuid
import os
import sys

def get_code():
    # Part 1: Header and Declarations
    from st_part1 import PART1_DECLARATIONS
    from st_part2 import PART2_LOGIC
    from st_part3 import PART3_LOGIC
    return PART1_DECLARATIONS + PART2_LOGIC + PART3_LOGIC

print("Import test")
