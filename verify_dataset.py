import json
import re

with open('data/swarm_raw/agent_e217271f.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

user_msg = data['messages'][0]['content']
asst_msg = data['messages'][1]['content']

print(f"User message length: {len(user_msg)}")
print(f"Assistant message length: {len(asst_msg)}")

assert asst_msg.startswith("```iec-st\n"), "Fence error at start"
assert asst_msg.endswith("\n```"), "Fence error at end"

inner_code = asst_msg[len("```iec-st\n"):-len("\n```")].strip()
lines = inner_code.split('\n')

print(f"Total code lines: {len(lines)}")
print(f"First line: '{lines[0]}'")
print(f"Last line: '{lines[-1]}'")

assert lines[0] == "FUNCTION_BLOCK FB_HybridManufacturing_DED_CNC_CoordinateSync"
assert lines[-1] == "END_FUNCTION_BLOCK"

# Parity checks
code_no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', inner_code)
if_count = len(re.findall(r'\bIF\b', code_no_comments))
endif_count = len(re.findall(r'\bEND_IF\b', code_no_comments))
case_count = len(re.findall(r'\bCASE\b', code_no_comments))
endcase_count = len(re.findall(r'\bEND_CASE\b', code_no_comments))
for_count = len(re.findall(r'\bFOR\b', code_no_comments))
endfor_count = len(re.findall(r'\bEND_FOR\b', code_no_comments))

print(f"IF: {if_count}, END_IF: {endif_count}")
print(f"CASE: {case_count}, END_CASE: {endcase_count}")
print(f"FOR: {for_count}, END_FOR: {endfor_count}")

assert if_count == endif_count
assert case_count == endcase_count
assert for_count == endfor_count
print("ALL RIGOROUS CHECKS PASSED PERFECTLY!")
