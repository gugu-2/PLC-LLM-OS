import sys
from build_agent_4b8109d1 import get_user_prompt, build_iec_code
from generate_full_code import get_var_block
from gen_parts import get_phase1_tmr, get_phase2_state_space, get_phase3_mpc_pinion, get_phase4_fsm, get_phase5_alarms
import json

header_io = build_iec_code()
var_block = get_var_block()
p1 = get_phase1_tmr()
p2 = get_phase2_state_space()
p3 = get_phase3_mpc_pinion()
p4 = get_phase4_fsm()
p5 = get_phase5_alarms()

full_st_code = f"{header_io}\n{var_block}\n{p1}\n{p2}\n{p3}\n{p4}\n{p5}"
full_content = f"```iec-st\n{full_st_code}\n```"

user_prompt = get_user_prompt()

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": full_content}
    ]
}

target_path = "data/swarm_raw/agent_4b8109d1.json"
with open(target_path, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"File generated successfully: {target_path}")
print(f"ST Code Character count: {len(full_st_code)}")
print(f"Assistant Content Character count: {len(full_content)}")
print(f"Total JSON file size: {len(json.dumps(record, ensure_ascii=False, indent=2))} bytes")
