import json

cids = [
    "4a9df0a4-e87d-4f05-bc79-2b4cf35afda7",
    "03aadc4f-babf-42b9-b695-72e2e8fa8528",
    "2c581ce8-92b1-425c-abfd-7824bffc70bc"
]

for cid in cids:
    path = f"C:/Users/majip/.gemini/antigravity/brain/{cid}/.system_generated/logs/transcript.jsonl"
    try:
        with open(path, "r", encoding="utf-8") as f:
            lines = [l for l in f if "PLANNER_RESPONSE" in l]
        if lines:
            last = json.loads(lines[-1])
            tc = last.get("tool_calls", [])
            calls = []
            for c in tc:
                name = c.get("name")
                params = c.get("parameters", {})
                summary = ""
                if "toolSummary" in params:
                    summary = params["toolSummary"]
                elif "Path" in params:
                    summary = params["Path"]
                elif "CommandLine" in params:
                    summary = params["CommandLine"][:60]
                calls.append((name, summary))
            print(f"Agent {cid}: {calls}")
        else:
            print(f"Agent {cid}: No PLANNER_RESPONSE")
    except Exception as e:
        print(f"Agent {cid}: Error {e}")
