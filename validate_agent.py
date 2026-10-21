import json

with open("data/swarm_raw/agent_cdf3fa22.json", "r", encoding="utf-8") as f:
    d = json.load(f)

asst = d["messages"][1]["content"]

assert asst[:9] == "```iec-st", f"Bad prefix: {asst[:9]!r}"
assert asst[-3:] == "```", f"Bad suffix: {asst[-3:]!r}"
assert asst[9] == "\n"
assert asst.splitlines()[1] == "FUNCTION_BLOCK FB_Biopharma_ContinuousLyophilizer_SublimationSync"
assert asst.splitlines()[-2] == "END_FUNCTION_BLOCK"

print("PERFECT! Prefix is triple backticks + iec-st, suffix is triple backticks.")
print("Total length:", len(asst))
