import json, re

filename = 'data/swarm_raw/agent_226d636f.json'
with open(filename, 'r', encoding='utf-8') as f:
    data = json.load(f)

user_msg = data['messages'][0]['content']
ast_msg = data['messages'][1]['content']

print('JSON loaded successfully.')
print('User message len:', len(user_msg))
print('Assistant message len:', len(ast_msg))

assert ast_msg.startswith('```iec-st\n'), 'Must start with ```iec-st'
assert ast_msg.endswith('\n```') or ast_msg.endswith('```'), 'Must end with ```'

code = ast_msg.strip()
lines = [l.strip() for l in code.splitlines()]

assert lines[1] == 'FUNCTION_BLOCK FB_Chemical_CCR_Hydrotreater_ThermalQuenchCompressor', f'Unexpected first code line: {lines[1]}'
assert lines[-2] == 'END_FUNCTION_BLOCK', f'Unexpected last code line: {lines[-2]}'

bad_patterns = ['// ...', '(* ...', 'TODO', 'REPLACE_ME', 'FIXME', '/* ... */']
for bp in bad_patterns:
    assert bp not in ast_msg, f'Found placeholder pattern {bp}!'

required_tokens = [
    'FB_Chemical_CCR_Hydrotreater_ThermalQuenchCompressor',
    'VAR_INPUT', 'VAR_OUTPUT', 'VAR', 'END_VAR', 'END_FUNCTION_BLOCK',
    'mA : ARRAY[1..4, 1..4] OF REAL',
    'mB : ARRAY[1..4, 1..4] OF REAL',
    'mQ_diag', 'mR_diag', 'mP_diag',
    'rDP_RecycleOrifice_A_mbar', 'rDP_RecycleOrifice_B_mbar', 'rDP_RecycleOrifice_C_mbar',
    'rTMR_Tolerance_mbar',
    'rTEMP_HH_TRIP_DEGC', 'rTEMP_H_WARN_DEGC',
    'rROR_HH_TRIP_DEGC_MIN', 'rROR_H_WARN_DEGC_MIN',
    'rSURGE_LL_TRIP_PCT', 'rSURGE_L_WARN_PCT',
    'rVIB_HH_TRIP_UM', 'rVIB_H_WARN_UM',
    'N2_PURGE_BLANKET', 'H2_PRESSURIZATION', 'REACTOR_PREHEAT', 'NAPHTHA_FEED_CUT_IN',
    'NORMAL_HYDROTREATING_RUN', 'THERMAL_QUENCH_ACTIVE', 'CATALYST_REGEN_CYCLE',
    'EMERGENCY_DEPRESSURIZE', 'CONTROLLED_SHUTDOWN', 'SURGE_RECOVERY_LOCKED',
    'dwAlarmWord_ISA18_2', 'wReactorStatusWord', 'wTurbineStatusWord'
]

for tok in required_tokens:
    assert tok in ast_msg, f'Missing required token: {tok}'

clean_code = re.sub(r'\(\*.*?\*\)', '', ast_msg, flags=re.DOTALL)
if_c = len(re.findall(r'\bIF\b', clean_code))
endif_c = len(re.findall(r'\bEND_IF\b', clean_code))
case_c = len(re.findall(r'\bCASE\b', clean_code))
endcase_c = len(re.findall(r'\bEND_CASE\b', clean_code))
for_c = len(re.findall(r'\bFOR\b', clean_code))
endfor_c = len(re.findall(r'\bEND_FOR\b', clean_code))

assert if_c == endif_c, f'IF mismatch: {if_c} vs {endif_c}'
assert case_c == endcase_c, f'CASE mismatch: {case_c} vs {endcase_c}'
assert for_c == endfor_c, f'FOR mismatch: {for_c} vs {endfor_c}'

print('All verification assertions passed flawlessly!')
print(f'Final Character Count: {len(ast_msg):,} characters')
