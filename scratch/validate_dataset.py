import json
import re
import sys

filename = "data/swarm_raw/agent_95d534da.json"
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data["messages"]
assert len(messages) == 2, f"Expected 2 messages, got {len(messages)}"
user_msg = messages[0]["content"]
asst_msg = messages[1]["content"]

print(f"User message length: {len(user_msg)}")
print(f"Assistant message length: {len(asst_msg)}")
assert len(asst_msg) >= 60000, f"Assistant content too short: {len(asst_msg)}"

assert asst_msg.startswith("```iec-st\nFUNCTION_BLOCK FB_Marine_ContainerVessel_DualFuelLNG_MEGI_BOG"), "Invalid starting line"
assert asst_msg.strip().endswith("END_FUNCTION_BLOCK\n```"), "Invalid ending line"

# Extract code inside backticks
code = asst_msg[len("```iec-st\n"):-len("\n```")].strip()

# Delimiter parity check
clean = re.sub(r'\(\*[\s\S]*?\*\)', '', code)

tokens = {
    'IF': len(re.findall(r'\bIF\b', clean)),
    'END_IF;': len(re.findall(r'\bEND_IF;', clean)),
    'CASE': len(re.findall(r'\bCASE\b', clean)),
    'END_CASE;': len(re.findall(r'\bEND_CASE;', clean)),
    'FOR': len(re.findall(r'\bFOR\b', clean)),
    'END_FOR;': len(re.findall(r'\bEND_FOR;', clean)),
    'FUNCTION_BLOCK': len(re.findall(r'\bFUNCTION_BLOCK\b', clean)),
    'END_FUNCTION_BLOCK': len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean)),
}

for k, v in tokens.items():
    print(f"{k}: {v}")

assert tokens['IF'] == tokens['END_IF;'], f"IF mismatch: {tokens['IF']} vs {tokens['END_IF;']}"
assert tokens['CASE'] == tokens['END_CASE;'], f"CASE mismatch: {tokens['CASE']} vs {tokens['END_CASE;']}"
assert tokens['FOR'] == tokens['END_FOR;'], f"FOR mismatch: {tokens['FOR']} vs {tokens['END_FOR;']}"
assert tokens['FUNCTION_BLOCK'] == tokens['END_FUNCTION_BLOCK'], "FUNCTION_BLOCK mismatch"

print("ALL VERIFICATION CHECKS PASSED PERFECTLY!")
