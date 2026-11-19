import json
import re

d = json.load(open("data/swarm_raw/agent_57011aca.json", "r", encoding="utf-8"))
content = d["messages"][1]["content"]

# Find FOR
for i, line in enumerate(content.splitlines()):
    if re.search(r'\bFOR\b', line, re.IGNORECASE):
        print(f"FOR at line {i+1}: {line}")
    if re.search(r'\bEND_FOR\b', line, re.IGNORECASE):
        print(f"END_FOR at line {i+1}: {line}")

# Check comments
for i, line in enumerate(content.splitlines()):
    c_open = line.count("(*")
    c_close = line.count("*)")
    if c_open != c_close:
        # Check if unbalanced on single line
        pass
