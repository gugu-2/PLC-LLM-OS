import json

with open('data/swarm_raw/agent_0e3b6aa4.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

code = data['messages'][1]['content']
print("END REPR:")
print(repr(code[-50:]))
