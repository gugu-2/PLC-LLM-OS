# Test assembly script
import os, sys
sys.path.insert(0, os.path.dirname(__file__))

from build_part1 import generate_code as gen_part1
from build_part2_matrices import generate_matrices as gen_part2
from build_part3_tmr import generate_tmr as gen_part3
from build_part4_physics import generate_physics as gen_part4
from build_part5_mpc import generate_mpc as gen_part5
from build_part6_cd_profile import generate_cd_profile as gen_part6
from build_part7_fsm import generate_fsm as gen_part7
from build_part8_alarms import generate_alarms as gen_part8

def assemble():
    all_lines = []
    all_lines.extend(gen_part1())
    all_lines.extend(gen_part2())
    all_lines.extend(gen_part3())
    all_lines.extend(gen_part4())
    all_lines.extend(gen_part5())
    all_lines.extend(gen_part6())
    all_lines.extend(gen_part7())
    all_lines.extend(gen_part8())
    
    full_text = "\n".join(all_lines)
    print(f"Total lines: {len(all_lines)}")
    print(f"Total character count: {len(full_text)}")
    return full_text

if __name__ == "__main__":
    txt = assemble()
