import json

with open('data/swarm_raw/agent_0e3b6aa4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

msgs = data['messages']
assert len(msgs) == 2
assert msgs[0]['role'] == 'user'
assert msgs[1]['role'] == 'assistant'
code = msgs[1]['content']

assert code.startswith('```iec-st\nFUNCTION_BLOCK FB_GeothermalDLE_IonExchange_ElutionCycle')
assert code.strip().endswith('END_FUNCTION_BLOCK\n```')
print('Validation SUCCESS: Length =', len(code))
