# scratch/build_and_save_dataset.py

import json
import uuid
import os
import sys
import re

sys.path.insert(0, os.path.abspath("."))
from scratch.generate_dataset import test_generation

def run_synthesis_and_save():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Metallurgy & Steel Rolling Mills: 6-Stand Continuous Tandem Cold Rolling Mill (strip width 1,850 mm, entry thickness 4.5 mm, exit thickness 0.18 mm at 1,800 m/min): Hydraulic Automatic Gauge Control (HAGC) with Mill Spring Compensation, Inter-Stand Strip Tension Regulation (Looperless tensiometer roll), Dynamic Roll Eccentricity Filtering (Kalman Filter), Roll Thermal Crown Bending Compensation, and Hydraulic Push-Up Cylinder High-Speed Decoupled Servo Control (1 ms cycle)**

Task: Write a world-class, mathematically rigorous, ultra-realistic IEC 61131-3 Structured Text Function Block named FB_Metals_ColdRolling_6StandTandem_HAGC for this 6-stand continuous tandem cold rolling mill system.

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Metals_ColdRolling_6StandTandem_HAGC
   b. VAR_INPUT ... END_VAR (minimum 8 typed inputs with physical units [bar], [deg C], [kN], [mm], [m/min], [MPa], [m/s2], [%])
   c. VAR_OUTPUT ... END_VAR (minimum 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal discrete state-space matrices A, B, C, D; MPC weights Q, R, S, P; 2oo3 voting variables; timers; FSM states)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 50,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF;, CASE and END_CASE;, FOR and END_FOR;.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Metals_ColdRolling_6StandTandem_HAGC
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Heavy Metallurgy & Steel Rolling Mills"""

    st_code = test_generation()
    assistant_content = f"```iec-st\n{st_code}\n```"

    # Validation
    assert assistant_content.startswith("```iec-st\nFUNCTION_BLOCK FB_Metals_ColdRolling_6StandTandem_HAGC"), "Opening syntax mismatch"
    assert assistant_content.endswith("END_FUNCTION_BLOCK\n```") or assistant_content.endswith("END_FUNCTION_BLOCK\n\n```"), "Closing syntax mismatch"
    
    code_no_comments = re.sub(r'\(\*.*?\*\)', '', st_code, flags=re.DOTALL)
    ifs = len(re.findall(r'\bIF\b', code_no_comments))
    end_ifs = len(re.findall(r'\bEND_IF\b', code_no_comments))
    cases = len(re.findall(r'\bCASE\b', code_no_comments))
    end_cases = len(re.findall(r'\bEND_CASE\b', code_no_comments))
    fors = len(re.findall(r'\bFOR\b', code_no_comments))
    end_fors = len(re.findall(r'\bEND_FOR\b', code_no_comments))
    whiles = len(re.findall(r'\bWHILE\b', code_no_comments))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', code_no_comments))

    assert ifs == end_ifs, f"IF parity error: {ifs} vs {end_ifs}"
    assert cases == end_cases, f"CASE parity error: {cases} vs {end_cases}"
    assert fors == end_fors, f"FOR parity error: {fors} vs {end_fors}"
    assert whiles == end_whiles, f"WHILE parity error: {whiles} vs {end_whiles}"
    assert len(assistant_content) >= 50000, f"Length too short: {len(assistant_content)}"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    out_dir = os.path.abspath("data/swarm_raw")
    os.makedirs(out_dir, exist_ok=True)
    agent_hex = uuid.uuid4().hex[:8]
    filename = os.path.join(out_dir, f"agent_{agent_hex}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    # Verification of written file
    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    loaded_code = loaded["messages"][1]["content"]
    print(f"SUCCESSFULLY SYNTHESIZED AND SAVED DATASET!")
    print(f"Output File: {filename}")
    print(f"Agent UUID: {agent_hex}")
    print(f"Total Assistant Content Length: {len(loaded_code)} characters")
    print(f"Parity Check: IFs={ifs}, END_IFs={end_ifs}, CASEs={cases}, END_CASEs={end_cases}, FORs={fors}, END_FORs={end_fors}")
    return filename, agent_hex, len(loaded_code)

if __name__ == "__main__":
    run_synthesis_and_save()
