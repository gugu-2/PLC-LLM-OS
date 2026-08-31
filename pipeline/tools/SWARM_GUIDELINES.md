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

2. **ALWAYS Use Triple-Backtick iec-st Code Fences — NEVER Single Backtick**
   Your generated assistant response MUST wrap code in TRIPLE backtick fences exactly like this:
   ````
   ```iec-st
   FUNCTION_BLOCK FB_YourName
   ...
   END_FUNCTION_BLOCK
   ```
   ````
   **WRONG** (causes FORMAT-01 error): `` `iec-st ... ` ``  ← single backtick
   **CORRECT**: ` ```iec-st ... ``` ` ← triple backtick

3. **Mandatory IEC 61131-3 Structure — All 4 Elements Required**
   Every generated FUNCTION_BLOCK MUST include ALL of these or it will be rejected by the pipeline:
   - `FUNCTION_BLOCK FB_<Name>` — opening declaration on its own line
   - `VAR_INPUT` / `END_VAR` — at least one input variable section
   - `VAR_OUTPUT` / `END_VAR` — at least one output variable section
   - `END_FUNCTION_BLOCK` — explicit closing declaration on its own line
   - At least one `END_IF;` or `END_CASE;` — control logic required
   - Minimum **1500 characters** in the assistant response

4. **Respect Length and Quality Constraints**
   - The master pipeline (`build_master_dataset.py`) discards any code block under **1500 characters**.
   - Records missing FUNCTION_BLOCK + VAR_INPUT/VAR_OUTPUT will be automatically dropped.

5. **Never Create Temp Files in Root**
   If you need scratch space, use `scratch/` or `.agents/`. Do not pollute the root directory.

6. **Track Provenance**
   Any new file you generate must go into `data/` and must be added to APPROVED_SOURCES in `pipeline/tools/build_master_dataset.py` if you want it included in fine-tuning.

7. **Example of a CORRECT swarm payload**
   ```python
   import json, uuid

   prompt = "Your user engineering task prompt here..."
   code = """```iec-st
FUNCTION_BLOCK FB_ExampleControl
VAR_INPUT
    bEnable : BOOL;
END_VAR
VAR_OUTPUT
    bReady : BOOL;
END_VAR
VAR
    iState : INT := 0;
END_VAR

CASE iState OF
    0:
        bReady := FALSE;
        IF bEnable THEN iState := 10; END_IF;
    10:
        bReady := TRUE;
END_CASE;

END_FUNCTION_BLOCK
```"""

   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   filepath = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
   with open(filepath, "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
   ```
