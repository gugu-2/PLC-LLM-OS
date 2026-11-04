import json

with open('data/swarm_raw/agent_92192045.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

code = data['output']

assert code.startswith('```iec-st\n'), 'Start mismatch'
assert code.endswith('\n```'), 'End mismatch'

open_comments = code.count('(*')
close_comments = code.count('*)')
print(f'Comments: (* = {open_comments}, *) = {close_comments}')
assert open_comments == close_comments

tags = [
    'IT_STACK_DC_CURRENT_101A', 'VT_STACK_DC_VOLTAGE_102A', 'PT_ANODE_O2_SEPARATOR_201A',
    'PT_CATHODE_H2_SEPARATOR_202A', 'DP_MEMBRANE_DIFF_PRESS_203A', 'AIT_H2_IN_O2_CROSSOVER_301A',
    'AIT_O2_IN_H2_CROSSOVER_302A', 'TT_STACK_COOLING_INLET_401A', 'TT_STACK_COOLING_OUTLET_402A',
    'FT_DI_WATER_FEED_501A', 'AIT_DI_WATER_CONDUCTIVITY_502A', 'PT_TSA_DRYER_BED1_601A'
]
for t in tags:
    assert t in code, f'Missing tag {t}'
print('All required P&ID tags confirmed present!')

states = [
    'SYSTEM_OFFLINE_N2_PURGED', 'DI_WATER_FILL_CIRCULATION', 'MEMBRANE_HYDRATION_SOAK',
    'CATHODE_ANODE_PRE_PRESSURIZE', 'STACK_MINIMUM_LOAD_START_5PCT', 'RENEWABLE_POWER_FOLLOWING_MPC',
    'DEOXO_PURIFICATION_PULSE', 'TSA_BED_DESORPTION_REGEN', 'CROSSOVER_SAFETY_DERATE_HOLD',
    'CONTROLLED_DE_ENERGIZATION', 'N2_FLUSH_STANDBY_PARK', 'EMERGENCY_ESTOP_VENT'
]
for s in states:
    assert s in code, f'Missing state {s}'
print('All 12 FSM states confirmed present!')

print('Dataset metadata:', data['metadata'])
print('Code character length:', len(code))
print('Code line count:', len(code.splitlines()))
