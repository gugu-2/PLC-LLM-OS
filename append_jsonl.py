import json
import os

source_file = "c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_c2d111da.json"
target_file = "c:/Users/majip/Downloads/LLM REASEARCH/data/synthetic_generation_v3_enterprise.jsonl"

os.makedirs(os.path.dirname(target_file), exist_ok=True)

with open(source_file, "r", encoding="utf-8") as f:
    record = json.load(f)

with open(target_file, "a", encoding="utf-8") as f:
    f.write(json.dumps(record) + "\n")
