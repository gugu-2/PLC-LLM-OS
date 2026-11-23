#!/usr/bin/env python3
"""
validate_iec.py — Enhanced IEC 61131-3 Syntax & Parity Validator
Reference: DOC-01, DOC-02, DOC-05

Performs rigorous structural syntax and balance checks on Structured Text Function Blocks:
- Balanced IF/END_IF, CASE/END_CASE, FOR/END_FOR, WHILE/END_WHILE
- Balanced (* *) comment blocks
- Top-level FUNCTION_BLOCK FB_... and END_FUNCTION_BLOCK bounds
- Physical units presence in comments [bar], [deg C], [kN], etc.
- Configurable minimum/maximum character gates to prevent stub datasets
"""

import sys
import json
import re
import os
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Union

DEFAULT_MIN_CHARS = 100_000
DEFAULT_MAX_CHARS = 700_000

def check_parity(code_text: str, min_chars: int = 3_500, max_chars: Optional[int] = None) -> Dict:
    """
    Core parity verification on raw IEC Structured Text.
    Returns: {"verdict": "PASS" | "FAIL", "errors": list, "warnings": list, "counts": dict}
    """
    errors = []
    warnings = []
    
    char_count = len(code_text)
    
    # Strip enclosing markdown code block fences if present
    stripped_text = code_text.strip()
    if stripped_text.startswith("```"):
        first_newline = stripped_text.find("\n")
        if first_newline != -1:
            stripped_text = stripped_text[first_newline + 1:]
    if stripped_text.endswith("```"):
        last_backticks = stripped_text.rfind("```")
        if last_backticks != -1:
            stripped_text = stripped_text[:last_backticks]
            
    lines = [l.strip() for l in stripped_text.strip().splitlines() if l.strip()]
    if not lines:
        return {
            "verdict": "FAIL",
            "errors": ["Code text is empty"],
            "warnings": [],
            "counts": {"char_count": 0}
        }
        
    if char_count < min_chars:
        errors.append(f"Character count ({char_count:,}) is below required minimum threshold ({min_chars:,}).")
    if max_chars and char_count > max_chars:
        warnings.append(f"Character count ({char_count:,}) exceeds recommended maximum ({max_chars:,}) - truncation hazard.")

    # 1. First line
    first_line = lines[0].strip()
    if not re.match(r'^FUNCTION_BLOCK\s+FB_\w+', first_line, re.IGNORECASE):
        errors.append(f"First line does not start with 'FUNCTION_BLOCK FB_': {first_line[:80]}")

    # 2. Last line
    last_line = lines[-1].strip()
    if not re.match(r'^END_FUNCTION_BLOCK\s*;?$', last_line, re.IGNORECASE):
        errors.append(f"Last line mismatch: '{last_line}', expected 'END_FUNCTION_BLOCK'")

    # 3. Check blocks
    if not re.search(r'\bVAR_INPUT\b', code_text, re.IGNORECASE) or not re.search(r'\bEND_VAR\b', code_text, re.IGNORECASE):
        errors.append("VAR_INPUT block missing")
    if not re.search(r'\bVAR_OUTPUT\b', code_text, re.IGNORECASE):
        errors.append("VAR_OUTPUT block missing")
    if not re.search(r'\bVAR\b', code_text, re.IGNORECASE):
        errors.append("Internal VAR block missing")

    # 4. Check physical units in comments
    bracket_units = re.findall(r'\[[a-zA-Z0-9/%^°\-_ ]+\]', code_text)
    if len(bracket_units) < 5:
        errors.append(f"Too few physical units found in comments ({len(bracket_units)} found, expected >= 5)")

    # 5. Comment parity
    open_comments = code_text.count("(*")
    close_comments = code_text.count("*)")
    if open_comments != close_comments:
        errors.append(f"Comment mismatch: (* count ({open_comments}) != *) count ({close_comments})")

    # 6. Balanced control structure parities (ignoring comments and strings)
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', ' ', code_text)
    clean_code = re.sub(r'\'[^\']*\'', "''", no_comments)

    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))
    fb_starts = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_ends = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))

    counts = {
        "char_count": char_count,
        "IF": ifs, "END_IF": end_ifs,
        "CASE": cases, "END_CASE": end_cases,
        "FOR": fors, "END_FOR": end_fors,
        "WHILE": whiles, "END_WHILE": end_whiles,
        "FUNCTION_BLOCK": fb_starts, "END_FUNCTION_BLOCK": fb_ends,
        "physical_units": len(bracket_units)
    }

    if ifs != end_ifs:
        errors.append(f"IF ({ifs}) and END_IF ({end_ifs}) count mismatch!")
    if cases != end_cases:
        errors.append(f"CASE ({cases}) and END_CASE ({end_cases}) count mismatch!")
    if fors != end_fors:
        errors.append(f"FOR ({fors}) and END_FOR ({end_fors}) count mismatch!")
    if whiles != end_whiles:
        errors.append(f"WHILE ({whiles}) and END_WHILE ({end_whiles}) count mismatch!")
    if fb_starts != fb_ends:
        errors.append(f"FUNCTION_BLOCK ({fb_starts}) and END_FUNCTION_BLOCK ({fb_ends}) count mismatch!")

    verdict = "FAIL" if errors else "PASS"
    return {
        "verdict": verdict,
        "errors": errors,
        "warnings": warnings,
        "counts": counts
    }

def validate_iec_st(code_text: str, min_chars: int = 3_500, max_chars: Optional[int] = None) -> List[str]:
    """Backward-compatible function returning error list."""
    res = check_parity(code_text, min_chars=min_chars, max_chars=max_chars)
    return res["errors"]

def validate_json_file(filepath: Union[str, Path], min_chars: int = 3_500, max_chars: Optional[int] = None) -> List[str]:
    """Validate a JSON dataset file (single-turn or multi-turn)."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        try:
            data = json.load(f)
        except Exception as e:
            return [f"Corrupt JSON: {e}"]

    if "messages" not in data or not isinstance(data["messages"], list) or len(data["messages"]) < 2:
        return ["Invalid structure: messages array must contain at least 2 items"]

    # Gather all assistant messages with code blocks
    assistant_codes = []
    for msg in data["messages"]:
        if msg.get("role") == "assistant":
            c = msg.get("content", "").replace("\r\n", "\n")
            # Extract code between iec-st blocks if present
            blocks = re.findall(r'```(?:iec-st)?\s*([\s\S]*?)```', c)
            if blocks:
                for b in blocks:
                    assistant_codes.append(b.strip())
            else:
                assistant_codes.append(c.strip())

    if not assistant_codes:
        return ["No assistant code content found in dataset"]

    all_errors = []
    for idx, code in enumerate(assistant_codes):
        # Only enforce FUNCTION_BLOCK boundaries if it starts as FB or is full-FB dataset
        if "FUNCTION_BLOCK" in code:
            errs = validate_iec_st(code, min_chars=min_chars, max_chars=max_chars)
            if errs:
                all_errors.extend([f"[Block {idx+1}] {e}" for e in errs])

    return all_errors

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina IEC 61131-3 Syntax Validator")
    parser.add_argument("target", nargs="?", default=None, help="File or directory path")
    parser.add_argument("--min-chars", type=int, default=3_500, help="Minimum character threshold")
    parser.add_argument("--max-chars", type=int, default=None, help="Maximum character threshold")
    parser.add_argument("--all", action="store_true", help="Validate all datasets in specified target directory")
    parser.add_argument("--json", action="store_true", help="Output summary in JSON")
    args = parser.parse_args()

    if not args.target:
        print("Usage: python validate_iec.py <path_to_json_or_st> [--min-chars N] [--all]")
        sys.exit(1)

    target_path = Path(args.target)
    if not target_path.exists():
        print(f"Error: Target path {target_path} not found.")
        sys.exit(1)

    if target_path.is_file():
        if target_path.suffix.lower() == ".json":
            errs = validate_json_file(target_path, min_chars=args.min_chars, max_chars=args.max_chars)
        else:
            with open(target_path, "r", encoding="utf-8", errors="replace") as f:
                errs = validate_iec_st(f.read(), min_chars=args.min_chars, max_chars=args.max_chars)

        if errs:
            print("VALIDATION FAILED with errors:")
            for e in errs:
                print(" -", e)
            sys.exit(1)
        else:
            print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
            sys.exit(0)

    # Directory validation
    json_files = list(target_path.glob("*.json"))
    print(f"Validating {len(json_files)} datasets in {target_path}...")
    passed = 0
    failed = 0
    failures = {}

    for jf in json_files:
        errs = validate_json_file(jf, min_chars=args.min_chars, max_chars=args.max_chars)
        if not errs:
            passed += 1
        else:
            failed += 1
            failures[jf.name] = errs

    print(f"Total: {len(json_files)} | PASSED: {passed} | FAILED: {failed}")
    if args.json:
        print(json.dumps({"total": len(json_files), "passed": passed, "failed": failed, "failures": failures}, indent=2))
        
    sys.exit(0 if failed == 0 else 1)
