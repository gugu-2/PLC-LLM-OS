# -*- coding: utf-8 -*-
"""
assemble_vial_filler.py
Assembles all parts for FB_Pharma_AsepticVialFilling_600VPM_Checkweigh,
validates syntax & AST parity, and saves to data/swarm_raw/agent_3d9104ca.json.
"""

import os
import json
import re
import sys

import vial_filler_header_io
import vial_filler_matrices
import vial_filler_phases1_to_4
import vial_filler_phases5_to_8
import vial_filler_phases9_to_10

def assemble_st():
    parts = [
        vial_filler_header_io.get_header_and_io().strip(),
        vial_filler_matrices.get_matrices_code().strip(),
        vial_filler_phases1_to_4.get_phases1_to_4_code().strip(),
        vial_filler_phases5_to_8.get_phases5_to_8_code().strip(),
        vial_filler_phases9_to_10.get_phases9_to_10_code().strip()
    ]
    return "\n\n".join(parts)

def verify_st(st_code):
    print(f"Total IEC 61131-3 ST character length: {len(st_code)}")
    lines = [l.strip() for l in st_code.splitlines() if l.strip()]
    print(f"Total lines: {len(lines)}")
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")

    errors = []
    if not lines[0].startswith("FUNCTION_BLOCK FB_"):
        errors.append(f"First line error: {lines[0]}")
    if lines[-1] != "END_FUNCTION_BLOCK":
        errors.append(f"Last line error: {lines[-1]}")

    open_c = st_code.count("(*")
    close_c = st_code.count("*)")
    print(f"Comments: (* = {open_c}, *) = {close_c}")
    if open_c != close_c:
        errors.append(f"Comment mismatch: (* ({open_c}) != *) ({close_c})")

    # Clean code for parity checks
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
    clean_code = re.sub(r'\'[^\']*\'', '', no_comments)

    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))

    print(f"Parity Check:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")

    if ifs != end_ifs:
        errors.append(f"IF mismatch: {ifs} vs {end_ifs}")
    if cases != end_cases:
        errors.append(f"CASE mismatch: {cases} vs {end_cases}")
    if fors != end_fors:
        errors.append(f"FOR mismatch: {fors} vs {end_fors}")
    if whiles != end_whiles:
        errors.append(f"WHILE mismatch: {whiles} vs {end_whiles}")

    units = re.findall(r'\[[a-zA-Z0-9/%^°\-_ ]+\]', st_code)
    print(f"Physical units found: {len(units)}")
    if len(units) < 5:
        errors.append(f"Too few physical units: {len(units)}")

    return errors

def main():
    st_code = assemble_st()
    errors = verify_st(st_code)
    if errors:
        print("Verification FAILED with errors:")
        for e in errors:
            print(" -", e)
        sys.exit(1)
    print("Verification PASSED!")

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Pharmaceuticals & Sterile Injectables: High-Speed Aseptic Rotary Vial Filling & Stoppering Monoblock (600 Vials/Min) with Multi-Channel Peristaltic Dosing, 100% In-Line Checkweighing & N2 Stoppering.**

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_Pharma_AsepticVialFilling_600VPM_Checkweigh with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    target_file = "data/swarm_raw/agent_3d9104ca.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully written to {target_file}")
    print(f"Total Assistant Content Length: {len(assistant_content)} characters")

if __name__ == "__main__":
    main()
