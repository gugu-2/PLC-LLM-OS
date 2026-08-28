# Guidelines for Cloud Swarm Agents

If you are a subagent (or the main agent) tasked with running a swarm or evolving data in parallel on the cloud, **YOU MUST FOLLOW THESE RULES**:

1. **Never Append to Shared Datasets (No Mixing)**
   When multiple agents run in parallel, writing to the same file causes JSON corruption and cross-contamination (e.g., `}{`).
   *Solution*: You MUST write your generated data to a completely isolated, uniquely named file.
   *Usage*: 
   ```python
   import uuid, json
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
   with open(filepath, "w", encoding="utf-8") as f:
       json.dump(record, f)
   ```
   The pipeline will safely collect and merge these individual files later.

2. **Always Output Markdown Fences**
   If you are designing prompts for swarm agents to generate IEC 61131-3 code, your prompt MUST tell the model:
   > "Output the code enclosed in a `iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN."
   Do NOT use the old prompt of "OUTPUT ONLY THE RAW CODE" as it breaks the master dataset format normalizer.

3. **Respect Length and Quality Constraints**
   - The master pipeline (uild_master_dataset.py) discards any code block under **1500 characters**.
   - Your generated code must include a FUNCTION_BLOCK and VAR_INPUT/VAR_OUTPUT.
   - If the code is missing these elements, it will be automatically dropped.

4. **Never Create Temp Files in Root**
   If you need scratch space, use scratch/ or .agents/. Do not pollute the root directory.

5. **Track Provenance**
   Any new file you generate must go into data/ and must be added to APPROVED_SOURCES in pipeline/tools/build_master_dataset.py if you want it included in fine-tuning.
