import json
import os

subagents = [
    ("af27f2f3-b0e7-448b-bd6e-6f1e687bc553", "Hairpin Stator Bending Fellow", "Automotive"),
    ("55159cc5-002b-4cee-b14d-ba4bd20534ec", "LSR Injection Molding Fellow", "Plastics"),
    ("43041c1e-417f-4783-88d1-d4fe4a87dad1", "Retort Autoclave Fellow", "Food & Bev"),
    ("2b43670e-40a0-40a7-87ac-5328ac821383", "Chassis Nutrunner Fellow", "Automotive"),
    ("d9e2372d-298d-49a0-a45a-74511b8ac527", "Deep Draw Press Fellow", "Mechanical"),
    ("cbda4c2e-e3c6-49cc-9d6b-5d8843fa6683", "Rotary Thermoforming Fellow", "Plastics"),
    ("7e925591-143f-491d-ac53-468a12fe3bae", "SMT Chip Shooter Fellow", "Electronics"),
    ("90804b53-3a67-429c-ba8e-ece6dff6696c", "Ladle Refining Furnace Fellow", "Heavy Metal")
]

for cid, role, sector in subagents:
    tpath = f"C:/Users/majip/.gemini/antigravity/brain/{cid}/.system_generated/logs/transcript.jsonl"
    if os.path.exists(tpath):
        lines = open(tpath, "r", encoding="utf-8").readlines()
        print(f"\n=== {role} ({cid[:8]}) ===")
        # Look backwards for last PLANNER_RESPONSE or USER_INPUT
        for line in reversed(lines[-5:]):
            step = json.loads(line)
            stype = step.get("type")
            tcalls = step.get("tool_calls", [])
            content = step.get("content", "")
            tcall_names = [tc.get("tool_name", "") for tc in tcalls] if tcalls else []
            print(f"  Step {step.get('step_index')}: type={stype}, status={step.get('status')}, tools={tcall_names}")
            if content and len(content) > 0:
                print(f"    Content preview: {repr(content[:120])}")
