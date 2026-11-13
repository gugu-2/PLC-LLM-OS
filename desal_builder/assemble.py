# desal_builder/assemble.py
import sys
import os

from part1_declarations import get_part1_declarations
from part2_matrix_init import get_part2_matrix_init
from part3_tmr_voting import get_part3_tmr_voting
from part4_thermo_observer import get_part4_thermo_observer
from part5_mpc_pgd import get_part5_mpc_pgd
from part6_fsm_logic import get_part6_fsm_logic
from part7_alarms_diagnostics import get_part7_alarms_diagnostics

p1 = get_part1_declarations()
p2 = get_part2_matrix_init()
p3 = get_part3_tmr_voting()
p4 = get_part4_thermo_observer()
p5 = get_part5_mpc_pgd()
p6 = get_part6_fsm_logic()
p7 = get_part7_alarms_diagnostics()

full_code = f"{p1}\n{p2}\n{p3}\n{p4}\n{p5}\n{p6}\n{p7}"

print(f"Assembly Complete:")
print(f"  Part 1 (Declarations):       {len(p1):>6} chars")
print(f"  Part 2 (Matrix Init):        {len(p2):>6} chars")
print(f"  Part 3 (TMR Voting):         {len(p3):>6} chars")
print(f"  Part 4 (Thermo Observer):    {len(p4):>6} chars")
print(f"  Part 5 (MPC PGD):            {len(p5):>6} chars")
print(f"  Part 6 (FSM Logic):          {len(p6):>6} chars")
print(f"  Part 7 (Alarms Diagnostics): {len(p7):>6} chars")
print(f"  -------------------------------------------")
print(f"  Total Characters:            {len(full_code):>6} chars")
print(f"  Total Lines:                 {len(full_code.splitlines()):>6} lines")

with open("test_desal.st", "w", encoding="utf-8") as f:
    f.write(full_code)

print("Saved raw Structured Text to test_desal.st")
