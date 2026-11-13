# c:\Users\majip\Downloads\LLM REASEARCH\battery_pack_builder\assemble.py
import sys
import os

from part1_decl import get_part1
from part2_phase0_1 import get_part2
from part3_phase2 import get_part3
from part4_phase3 import get_part4
from part5_phase4 import get_part5
from part6_phase5 import get_part6
from part7_phase6 import get_part7

def assemble_code():
    parts = [
        get_part1(),
        get_part2(),
        get_part3(),
        get_part4(),
        get_part5(),
        get_part6(),
        get_part7()
    ]
    return "\n".join(parts)

if __name__ == "__main__":
    code = assemble_code()
    print(f"Total lines: {len(code.splitlines())}")
    print(f"Total characters: {len(code)}")
