import sys
import os
import re

sys.path.insert(0, os.path.abspath("st_sections"))
from sec1_header import get_sec1_header
from sec2_vars import get_sec2_vars
from sec3_logic_p1 import get_sec3_logic_p1
from sec4_logic_p2 import get_sec4_logic_p2
from sec5_fsm import get_sec5_fsm

st_code = "\n".join([
    get_sec1_header(),
    get_sec2_vars(),
    get_sec3_logic_p1(),
    get_sec4_logic_p2(),
    get_sec5_fsm()
])

full_assistant_content = f"```iec-st\n{st_code}\n```"

print(f"Total assistant content characters: {len(full_assistant_content)}")
print(f"ST code characters: {len(st_code)}")

# Check structural rules
lines = st_code.strip().split("\n")
first_line = lines[0].strip()
last_line = lines[-1].strip()

print(f"First line: {first_line}")
print(f"Last line: {last_line}")

# Verify parity of control statements outside of comments
# Strip comments (* ... *)
code_no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
# Also strip // comments if any
code_no_comments = re.sub(r'//.*', '', code_no_comments)

if_count = len(re.findall(r'\bIF\b', code_no_comments, re.IGNORECASE))
endif_count = len(re.findall(r'\bEND_IF\b', code_no_comments, re.IGNORECASE))
case_count = len(re.findall(r'\bCASE\b', code_no_comments, re.IGNORECASE))
endcase_count = len(re.findall(r'\bEND_CASE\b', code_no_comments, re.IGNORECASE))
for_count = len(re.findall(r'\bFOR\b', code_no_comments, re.IGNORECASE))
endfor_count = len(re.findall(r'\bEND_FOR\b', code_no_comments, re.IGNORECASE))

print(f"IF count: {if_count}, END_IF count: {endif_count}")
print(f"CASE count: {case_count}, END_CASE count: {endcase_count}")
print(f"FOR count: {for_count}, END_FOR count: {endfor_count}")

assert first_line == "FUNCTION_BLOCK FB_HydrogenPipeline_CentrifugalCompressorAntiSurge", "First line mismatch!"
assert last_line == "END_FUNCTION_BLOCK", "Last line mismatch!"
assert if_count == endif_count, f"IF/END_IF mismatch: {if_count} vs {endif_count}"
assert case_count == endcase_count, f"CASE/END_CASE mismatch: {case_count} vs {endcase_count}"
assert for_count == endfor_count, f"FOR/END_FOR mismatch: {for_count} vs {endfor_count}"
print("All assertions passed!")
