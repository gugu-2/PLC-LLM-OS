import json

d = json.load(open("data/swarm_raw/agent_57011aca.json", "r", encoding="utf-8"))
content = d["messages"][1]["content"]
lines = content.splitlines()

# Track comment nesting
depth = 0
for i, line in enumerate(lines):
    # scan characters
    j = 0
    while j < len(line) - 1:
        if line[j:j+2] == "(*":
            depth += 1
            j += 2
        elif line[j:j+2] == "*)":
            depth -= 1
            if depth < 0:
                print(f"Negative comment depth at line {i+1}: {line}")
                depth = 0
            j += 2
        else:
            j += 1
print(f"Final comment depth: {depth}")
