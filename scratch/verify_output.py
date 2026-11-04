import json

with open('data/swarm_raw/agent_150de0a3.json', 'r', encoding='utf-8') as f:
    d = json.load(f)

out = d['output']
assert out.startswith("```iec-st\n"), "Does not start with ```iec-st\\n"
assert out.endswith("\n```"), "Does not end with \\n```"

code = out[len("```iec-st\n"):-len("\n```")].strip()
lines = code.splitlines()

assert lines[0] == "FUNCTION_BLOCK FB_Aerospace_RocketEngine_LOX_Methane_TestStand", f"First line unexpected: {lines[0]}"
assert lines[-1] == "END_FUNCTION_BLOCK", f"Last line unexpected: {lines[-1]}"

print("Exact match on code start:", lines[0])
print("Exact match on code end:", lines[-1])
print("Total code characters:", len(code))
print("Total code lines:", len(lines))
print("ALL ASSERTIONS PASSED!")
