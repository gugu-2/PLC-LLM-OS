import json

with open("temp_payload.json", "r", encoding="utf-8") as f:
    data = json.load(f)

file_path = "data/synthetic_generation_v3_enterprise.jsonl"
with open(file_path, "a", encoding="utf-8") as f:
    f.write(json.dumps(data) + "\n")

print(f"Appended successfully to {file_path}")
