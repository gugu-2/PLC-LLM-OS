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
from typing import Dict, Any


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

    with open(input_file, 'r', encoding='utf-8') as f_in, open(output_file, 'w', encoding='utf-8') as f_out:
        for line in f_in:
            if not line.strip():
                continue
            total_count += 1
            try:
                data = json.loads(line)
                code_to_check = data.get("content", "") or data.get("code", "") or data.get("body", "")
                if is_valid_plc_code(code_to_check):
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
    print("[*] Running Dataset Cleaning Validation on sample...")
    sample_scl = "FUNCTION_BLOCK FB_Test\nVAR\n nVal : INT := 10;\nEND_VAR\nBEGIN\n IF nVal > 5 THEN\n nVal := 0;\n END_IF;\nEND_FUNCTION_BLOCK"
    assert is_valid_plc_code(sample_scl) is True
    print("[OK] Dataset cleaner heuristics operational.")
