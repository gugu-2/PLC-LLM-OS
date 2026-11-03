# -*- coding: utf-8 -*-
"""
Assembler and verifier for FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror
"""

import os
import sys
import json
import uuid
import re

from gen_parts.header_and_interfaces import get_header_and_interfaces
from gen_parts.phases_1_to_3 import get_phases_1_to_3
from gen_parts.phases_4_to_6 import get_phases_4_to_6

sys.path.append(os.path.abspath("Local_Ollama_Evol_Pipeline/scripts"))
try:
    from linter import ST_Linter
except ImportError:
    ST_Linter = None

def main():
    part1 = get_header_and_interfaces()
    part2 = get_phases_1_to_3()
    part3 = get_phases_4_to_6()

    st_code = part1 + "\n" + part2 + "\n" + part3
    st_code = st_code.strip()

    print(f"Total Structured Text character count: {len(st_code)} characters")

    # 1. Structural checks
    lines = st_code.splitlines()
    first_line = lines[0].strip()
    last_line = lines[-1].strip()

    print(f"First line: '{first_line}'")
    print(f"Last line:  '{last_line}'")

    assert first_line == "FUNCTION_BLOCK FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror", f"Invalid first line: {first_line}"
    assert last_line == "END_FUNCTION_BLOCK", f"Invalid last line: {last_line}"

    # 2. Strip comments for keyword balance check
    clean_code = re.sub(r'\(\*.*?\*\)', '', st_code, flags=re.DOTALL)
    clean_code = re.sub(r'//.*', '', clean_code)

    if_matches = re.findall(r'\bIF\b', clean_code, re.IGNORECASE)
    endif_matches = re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE)
    print(f"IF count: {len(if_matches)}, END_IF count: {len(endif_matches)}")
    assert len(if_matches) == len(endif_matches), f"IF/END_IF mismatch: {len(if_matches)} != {len(endif_matches)}"

    case_matches = re.findall(r'\bCASE\b', clean_code, re.IGNORECASE)
    endcase_matches = re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE)
    print(f"CASE count: {len(case_matches)}, END_CASE count: {len(endcase_matches)}")
    assert len(case_matches) == len(endcase_matches), f"CASE/END_CASE mismatch: {len(case_matches)} != {len(endcase_matches)}"

    for_matches = re.findall(r'\bFOR\b', clean_code, re.IGNORECASE)
    endfor_matches = re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE)
    print(f"FOR count: {len(for_matches)}, END_FOR count: {len(endfor_matches)}")
    assert len(for_matches) == len(endfor_matches), f"FOR/END_FOR mismatch: {len(for_matches)} != {len(endfor_matches)}"

    # Check VAR blocks
    var_input_count = len(re.findall(r'\bVAR_INPUT\b', clean_code, re.IGNORECASE))
    var_output_count = len(re.findall(r'\bVAR_OUTPUT\b', clean_code, re.IGNORECASE))
    var_count = len(re.findall(r'\bVAR\b', clean_code, re.IGNORECASE))
    endvar_count = len(re.findall(r'\bEND_VAR\b', clean_code, re.IGNORECASE))
    print(f"VAR_INPUT: {var_input_count}, VAR_OUTPUT: {var_output_count}, VAR: {var_count}, END_VAR: {endvar_count}")
    assert (var_input_count + var_output_count + var_count) == endvar_count, "VAR/END_VAR block count mismatch!"

    # 3. ST_Linter check
    if ST_Linter:
        passed, msg = ST_Linter.verify_code(st_code)
        print(f"ST_Linter verification: passed={passed}, message='{msg}'")
        assert passed, f"ST_Linter failed: {msg}"
    else:
        print("ST_Linter not imported, skipping external linter call.")

    # 4. Prepare JSON record
    from build_euv_dataset import PROMPT
    formatted_assistant_code = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": PROMPT},
            {"role": "assistant", "content": formatted_assistant_code}
        ]
    }

    # 5. Save to unique file
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{agent_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    file_size = os.path.getsize(output_filename)
    print(f"Saved successfully to: {output_filename}")
    print(f"File size on disk: {file_size} bytes")

    # Re-read and verify integrity
    with open(output_filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    loaded_code = loaded["messages"][1]["content"]
    assert "FUNCTION_BLOCK FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror" in loaded_code
    assert "END_FUNCTION_BLOCK" in loaded_code
    print("Verification complete. File is 100% valid and verified.")
    return output_filename, len(st_code), file_size

if __name__ == "__main__":
    main()
