# -*- coding: utf-8 -*-
import json

with open("data/swarm_raw/agent_557030a4.json", "r", encoding="utf-8") as f:
    data = json.load(f)

messages = data["messages"]
assert len(messages) == 2
user_msg = messages[0]
asst_msg = messages[1]

assert user_msg["role"] == "user"
assert asst_msg["role"] == "assistant"

content = asst_msg["content"]
print(f"Length of assistant content: {len(content)}")
assert len(content) >= 3500

fence_start = "```iec-st\n"
fence_end = "\n```"

assert content.startswith(fence_start), f"Does not start with {repr(fence_start)}, starts with {repr(content[:20])}"
assert content.endswith(fence_end), f"Does not end with {repr(fence_end)}, ends with {repr(content[-20:])}"

inner_code = content[len(fence_start):-len(fence_end)]
lines = inner_code.strip().splitlines()

print(f"First line: {lines[0]}")
print(f"Last line: {lines[-1]}")

assert lines[0] == "FUNCTION_BLOCK FB_SubseaMining_DiamondWire_VentCutter"
assert lines[-1] == "END_FUNCTION_BLOCK"

assert "VAR_INPUT" in inner_code
assert "VAR_OUTPUT" in inner_code
assert "END_IF;" in inner_code
assert "END_CASE;" in inner_code

print("ALL VERIFICATIONS PASSED 100%!")
