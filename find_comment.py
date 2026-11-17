import json

with open("data/swarm_raw/agent_8e1b12a4.json", "r", encoding="utf-8") as f:
    data = json.load(f)

content = data["messages"][1]["content"]
lines = content.split("\n")

total_open = 0
total_close = 0

for idx, line in enumerate(lines):
    o = line.count("(*")
    c = line.count("*)")
    total_open += o
    total_close += c
    if idx > 40 and total_open != total_close:
        print(f"Mismatch at Line {idx+1}: total_open={total_open}, total_close={total_close}")
        print(f"Content: {line}")
        break
