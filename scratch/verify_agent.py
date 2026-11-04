import json

with open("data/swarm_raw/agent_a3df7732.json", "r", encoding="utf-8") as f:
    data = json.load(f)

msgs = data["messages"]
c = msgs[1]["content"]
print(f"Content length: {len(c)}")
print(f"Starts with ```iec-st\\n: {c.startswith('```iec-st\\n')}")
print(f"Ends with ```: {c.strip().endswith('```')}")
inner = c[len("```iec-st\n"):].rstrip()
if inner.endswith("```"):
    inner = inner[:-3].rstrip()
lines = inner.splitlines()
print(f"First line: {lines[0]}")
print(f"Last line: {lines[-1]}")
assert lines[0] == "FUNCTION_BLOCK FB_Pharma_BulkLyophilizer_CapacitanceManometer_Pirani"
assert lines[-1] == "END_FUNCTION_BLOCK"
print("SUCCESSFULLY VERIFIED ALL METRICS!")
