import os
import json
import sys

from gen_modules.header import get_header
from gen_modules.var_input import get_var_input
from gen_modules.var_output import get_var_output
from gen_modules.var_internal import get_var_internal
from gen_modules.matrices import get_matrices_code
from gen_modules.tmr_kinematics import get_tmr_kinematics_code
from gen_modules.tracking_fsm import get_tracking_fsm_code

def main():
    parts = []
    parts.append(get_header().strip())
    parts.append(get_var_input().strip())
    parts.append(get_var_output().strip())
    parts.append(get_var_internal().strip())
    parts.append(get_matrices_code().strip())
    parts.append(get_tmr_kinematics_code().strip())
    parts.append(get_tracking_fsm_code().strip())
    parts.append("END_FUNCTION_BLOCK")
    
    st_code = "\n\n".join(parts) + "\n"
    code_fenced = "```iec-st\n" + st_code + "```"
    
    print(f"Structured Text raw length: {len(st_code)} characters")
    print(f"Code fenced length: {len(code_fenced)} characters")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Packaging & Logistics Robotics: High-Speed Aseptic Packaging Collation Cell with 4 Synchronized Parallel Delta Kinematics Robots & Vision Tracking**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Packaging_HighSpeed_MultiDeltaRobot_CasePacker
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [kPa], [mm], [mm/s], [deg], [deg/s], [A], [V], [pulses/rev], [packages/min], [units], [ms], [%])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 60,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Packaging_HighSpeed_MultiDeltaRobot_CasePacker
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Commercial Packaging & Logistics Robotics: High-Speed Aseptic Packaging Collation Cell with 4 Synchronized Parallel Delta Kinematics Robots & Vision Tracking"""

    record = {
        "instruction": prompt,
        "input": "",
        "output": code_fenced,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_fenced}
        ]
    }
    
    target_file = "data/swarm_raw/agent_5e8201fa.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Saved dataset to {target_file}")

if __name__ == "__main__":
    main()
