"""
Lumina Dataset Cleaning & IEC 61131-3 Syntax Validator
======================================================
Validates, cleans, and deduplicates raw industrial automation datasets across:
  - Structured Text (IEC 61131-3 ST / Siemens SCL)
  - Rockwell Studio 5000 Ladder Logic & L5X XML
  - Siemens Statement List (AWL / STL)
"""

import json
import re
import sys
import os
from typing import Dict, Any

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../backend")))
from lumina_verify import VerificationGauntlet


def is_valid_plc_code(content: str) -> bool:
    """Multi-dialect validation for IEC 61131-3 Structured Text, L5X, and STL."""
    if not content or len(content.strip()) < 15:
        return False

    # Check for Rockwell Studio 5000 L5X XML
    if "RSLogix5000Content" in content or "<Routine" in content:
        return True

    # Check for IEC structural keywords
    has_struct = bool(re.search(r'(?i)\b(function|function_block|program|end_function|end_function_block|end_program|var|var_input|var_output|var_in_out|end_var)\b', content))
    
    # Check for IEC logic keywords & Ladder / STL instructions
    has_logic = bool(re.search(r'(?i)\b(if|then|else|elsif|case|for|while|repeat|until|end_if|end_case|end_for|end_while|end_repeat|xic|xio|ote|otl|otu|ton|tof|equ|geq|mov|jmp)\b', content))
    has_stl = bool(re.search(r'(?i)\b(a|an|o|on|l|t|jc|ju|bec|call)\s+[A-Z0-9_\.%#]+', content))
    has_assign = ":=" in content

    # Noise and non-PLC language filters
    invalid_keywords = [
        '#include <iostream>', 'printf(', 'System.out.println', 'public static void main',
        'import React', '<html>', '<script>', 'def __init__(self', 'namespace std'
    ]
    has_invalid = any(kw in content for kw in invalid_keywords)

    if (has_struct or has_logic or has_stl or has_assign) and not has_invalid:
        tokens = len(content.split())
        logic_matches = len(re.findall(r'(?i)\b(if|then|else|elsif|case|for|while|repeat|until|end_if|xic|xio|ote|ton|mov|a|an|l|t)\b', content))
        logic_density = logic_matches / max(1, tokens)
        return logic_density >= 0.015
    return False


def clean_dataset_file(input_file: str, output_file: str) -> Dict[str, int]:
    valid_count = 0
    total_count = 0

    # Initialize the Verification Gauntlet for strict mathematical dataset filtering
    gauntlet = VerificationGauntlet()
    # Define a set of standard safety invariants that all dataset code must inherently pass
    standard_invariants = [
        "If Start is pressed, system must eventually run.",
        "Loop iterators must be strictly bounded."
    ]

    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if not line.strip():
                continue
            total_count += 1
            try:
                data = json.loads(line)
                
                # Extract code based on the dataset schema (ChatML or Flat)
                code_to_check = ""
                if "messages" in data:
                    for msg in data["messages"]:
                        if msg.get("role") == "assistant":
                            code_to_check = msg.get("content", "")
                            break
                else:
                    code_to_check = data.get("content", "") or data.get("code", "") or data.get("body", "")
                
                # Step 1: Strip XML Boilerplate (TwinCAT / Rockwell)
                # If it's a TwinCAT TcPOU, extract only the Declaration and ST blocks
                import re
                if "<TcPlcObject" in code_to_check:
                    declarations = re.findall(r'<Declaration><!\[CDATA\[(.*?)\]\]></Declaration>', code_to_check, re.DOTALL)
                    implementations = re.findall(r'<ST><!\[CDATA\[(.*?)\]\]></ST>', code_to_check, re.DOTALL)
                    extracted_code = ""
                    if declarations:
                        extracted_code += declarations[0].strip() + "\n"
                    if implementations:
                        extracted_code += implementations[0].strip() + "\n"
                    
                    if extracted_code:
                        code_to_check = extracted_code
                        # Update the JSON payload with the clean code
                        if "messages" in data:
                            for msg in data["messages"]:
                                if msg.get("role") == "assistant":
                                    msg["content"] = code_to_check
                        else:
                            data["content"] = code_to_check
                
                # Step 2: Logic Density Heuristics
                if is_valid_plc_code(code_to_check):
                    # Step 3: Z3 Mathematical Verification
                    verify_result = gauntlet.verify(code_to_check, variables={}, transition_rules=[], safety_invariants=standard_invariants)
                    
                    # We only accept code that passes the Static Linter and SMT proofs
                    # (We don't strictly require Layer 3 Digital Twin passing for raw dataset chunks)
                    if verify_result.passed or verify_result.layer_failed == "LAYER_3_DIGITAL_TWIN_SIMULATION":
                        f_out.write(json.dumps(data) + '\n')
                        valid_count += 1
            except json.JSONDecodeError:
                continue

    return {
        "total_read": total_count,
        "valid_kept": valid_count,
        "filtered_out": total_count - valid_count
    }


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 2:
        input_f = sys.argv[1]
        output_f = sys.argv[2]
        print(f"[*] Running Z3-Verified Dataset Cleaning on {input_f}...")
        results = clean_dataset_file(input_f, output_f)
        print(f"[OK] Cleaning complete. Results: {results}")
    else:
        print("[*] Running Dataset Cleaning Validation on sample...")
        sample_scl = "FUNCTION_BLOCK FB_Test\nVAR\n nVal : INT := 10;\nEND_VAR\nBEGIN\n IF nVal > 5 THEN\n nVal := 0;\n END_IF;\nEND_FUNCTION_BLOCK"
        assert is_valid_plc_code(sample_scl) is True
        print("[OK] Dataset cleaner heuristics operational.")
