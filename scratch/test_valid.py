# scratch/test_valid.py
import json
import re

with open('data/swarm_raw/agent_1e6e30c1.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

messages = data['messages']
print('Messages count:', len(messages))
print('User prompt length:', len(messages[0]['content']))
assistant_code = messages[1]['content']
print('Assistant code length:', len(assistant_code))

prefix = "```iec-st\nFUNCTION_BLOCK FB_PlasmaGasification_SyngasRatio_ChokeSync"
suffix = "END_FUNCTION_BLOCK\n```"
assert assistant_code.startswith(prefix), f"Prefix mismatch: {repr(assistant_code[:60])}"
assert assistant_code.rstrip().endswith(suffix), f"Suffix mismatch: {repr(assistant_code[-60:])}"

clean_code = re.sub(r'\(\*.*?\*\)', '', assistant_code, flags=re.DOTALL)
if_count = len(re.findall(r'\bIF\b', clean_code))
endif_count = len(re.findall(r'\bEND_IF\b', clean_code))
case_count = len(re.findall(r'\bCASE\b', clean_code))
endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code))

print(f'IF: {if_count}, END_IF: {endif_count}')
print(f'CASE: {case_count}, END_CASE: {endcase_count}')
assert if_count == endif_count, f"IF/END_IF mismatch: {if_count} != {endif_count}"
assert case_count == endcase_count, f"CASE/END_CASE mismatch: {case_count} != {endcase_count}"

required_units = ['[deg C]', '[kW]', '[Nm3/h]', '[bar]', '[mol/mol]', '[MJ/Nm3]', '[mbar]', '[kg/h]']
for u in required_units:
    assert u in assistant_code, f'Missing unit {u}'
print('All required units verified!')

print('DATASET VALIDATION 100% SUCCESS!')
