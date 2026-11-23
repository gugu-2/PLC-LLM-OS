#!/usr/bin/env python3
"""
validate_semantic.py — Stage 2 Structural Semantics Validator for Lumina PLC-LLM Corpus
Reference: DOC-01, DOC-02, DOC-05

Checks:
1. Variable Declaration Completeness & Duplicate Detection
2. State-Space Matrix Dimension Consistency (A: nxn, B: nxm, C: pxn)
3. FSM State Completeness & Deadlock Transition Detection
4. MPC Prediction Horizon Unroll Verification (N >= 10)
5. 2oo3 Triple Modular Redundancy (TMR) Voter & Discrepancy Timer Verification
"""

import os
import sys
import json
import re
import argparse
from pathlib import Path
from dataclasses import dataclass, field
from typing import Dict, List, Optional, Set, Tuple

@dataclass
class SemanticReport:
    file: str
    fb_name: str
    errors: List[str] = field(default_factory=list)
    warnings: List[str] = field(default_factory=list)
    verdict: str = "PASS"  # PASS | WARN | FAIL
    metrics: Dict = field(default_factory=dict)

    def add_error(self, msg: str):
        self.errors.append(msg)
        self.verdict = "FAIL"

    def add_warning(self, msg: str):
        self.warnings.append(msg)
        if self.verdict == "PASS":
            self.verdict = "WARN"

def clean_st_code(code_text: str) -> str:
    """Remove comments and literal string contents for AST-like parsing."""
    no_block_comments = re.sub(r'\(\*[\s\S]*?\*\)', ' ', code_text)
    no_line_comments = re.sub(r'//[^\n]*', ' ', no_block_comments)
    clean = re.sub(r'\'[^\']*\'', "''", no_line_comments)
    return clean

def check_var_declarations(code_text: str, report: SemanticReport):
    """
    Check 1: Variable declarations and scope verification.
    """
    clean = clean_st_code(code_text)
    
    # 1a. Extract all declared variables across all VAR blocks
    var_block_pattern = re.compile(
        r'\b(?:VAR|VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP|VAR_STAT|VAR_GLOBAL)\b([\s\S]*?)\bEND_VAR\b',
        re.IGNORECASE
    )
    
    declared_vars: Dict[str, str] = {}
    duplicate_vars: List[str] = []
    
    for block in var_block_pattern.finditer(clean):
        block_content = block.group(1)
        # Parse lines: var_name : TYPE;
        statements = block_content.split(';')
        for stmt in statements:
            stmt = stmt.strip()
            if not stmt:
                continue
            # Handle possible AT %... constructs
            colon_idx = stmt.find(':')
            if colon_idx != -1:
                lhs = stmt[:colon_idx].strip()
                rhs = stmt[colon_idx + 1:].strip()
                # May have multiple vars: a, b, c : INT
                var_names = [v.strip().upper() for v in lhs.split(',')]
                for v in var_names:
                    # Remove AT %I* etc
                    v_clean = re.sub(r'\s+AT\s+%.*', '', v).strip()
                    if not v_clean or not re.match(r'^[A-Z_][A-Z0-9_]*$', v_clean):
                        continue
                    if v_clean in declared_vars:
                        duplicate_vars.append(v_clean)
                    else:
                        declared_vars[v_clean] = rhs

    report.metrics["declared_var_count"] = len(declared_vars)

    if len(declared_vars) < 10:
        report.add_error(f"Function Block has abnormally few variables declared ({len(declared_vars)} found, expected >= 10).")

    if duplicate_vars:
        # Filter down unique
        dups_unique = sorted(list(set(duplicate_vars)))
        if len(dups_unique) > 10:
            report.add_warning(f"Multiple duplicate variable declarations ({len(dups_unique)} instances, e.g. {dups_unique[:5]}).")
        else:
            report.add_warning(f"Duplicate variable declarations: {dups_unique}")

def _is_state_matrix(k: str) -> bool:
    if re.search(r'(?:^|_)(?:STATE)(?:_|$)', k):
        return True
    if re.search(r'(?:^|_|MAT(?:RIX)?_)A$', k):
        return True
    if re.match(r'^A(?:_MATRIX|_MAT|_SYS)?$', k):
        return True
    if re.search(r'(?:^|_)MAT(?:RIX)?_A(?:_|$)', k):
        return True
    if re.match(r'^A_?MATRIX_A$', k):
        return True
    return False

def _is_input_matrix(k: str) -> bool:
    if re.search(r'(?:^|_)(?:INPUT)(?:_|$)', k):
        return True
    if re.search(r'(?:^|_|MAT(?:RIX)?_)B$', k):
        return True
    if re.match(r'^B(?:_MATRIX|_MAT|_SYS)?$', k):
        return True
    if re.search(r'(?:^|_)MAT(?:RIX)?_B(?:_|$)', k):
        return True
    if re.match(r'^A_?MATRIX_B$', k):
        return True
    return False

def check_matrix_dimensions(code_text: str, report: SemanticReport):
    """
    Check 2: State-Space Matrix Dimension Consistency.
    A: n x n
    B: n x m
    """
    clean = clean_st_code(code_text)
    
    # Look for Array declarations: A_Matrix : ARRAY[0..N, 0..N] OF LREAL
    matrix_decls = {}
    pattern = re.compile(
        r'(\b\w*Matrix\w*|\b\w*_Mat_\w+|\b[ABCDQRP]\b|\b[ABCD]_\w+|\bSTATE\w*|\bINPUT\w*)\s*:\s*ARRAY\s*\[\s*0\s*\.\.\s*(\d+)\s*,\s*0\s*\.\.\s*(\d+)\s*\]\s*OF',
        re.IGNORECASE
    )
    
    for m in pattern.finditer(clean):
        name = m.group(1).upper()
        r = int(m.group(2)) + 1
        c = int(m.group(3)) + 1
        matrix_decls[name] = (r, c)
        
    report.metrics["matrix_declarations"] = matrix_decls
    
    # Check A matrix
    a_mats = {k: v for k, v in matrix_decls.items() if _is_state_matrix(k)}
    b_mats = {k: v for k, v in matrix_decls.items() if _is_input_matrix(k)}
    
    for a_name, (ar, ac) in a_mats.items():
        if ar != ac:
            report.add_error(f"State matrix '{a_name}' is non-square: {ar}x{ac} (must be nxn).")
        for b_name, (br, bc) in b_mats.items():
            if br != ar:
                report.add_error(f"Dimension mismatch between state matrix '{a_name}' ({ar} rows) and input matrix '{b_name}' ({br} rows).")

def check_fsm_completeness(code_text: str, report: SemanticReport):
    """
    Check 3: FSM State Completeness & Deadlock Transition Detection.
    """
    clean = clean_st_code(code_text)
    
    # Find CASE State OF
    case_blocks = re.findall(r'\bCASE\s+(\w+)\s+OF([\s\S]*?)\bEND_CASE\b', clean, re.IGNORECASE)
    if not case_blocks:
        report.add_error("No CASE State OF state-machine construct found.")
        return

    total_states_found = 0
    deadlock_states = []

    for state_var, case_body in case_blocks:
        # Match case labels e.g. "0:" or "10, 20:" or "STATE_INIT:"
        labels = re.findall(r'^\s*([A-Za-z0-9_,\s]+)\s*:\s*(?!=\s*)', case_body, re.MULTILINE)
        state_list = []
        for l in labels:
            if "ELSE" in l.upper():
                continue
            parts = [p.strip() for p in l.split(',') if p.strip()]
            state_list.extend(parts)

        total_states_found += len(state_list)
        report.metrics[f"fsm_{state_var}_states"] = len(state_list)

        if len(state_list) < 3:
            report.add_warning(f"FSM controlled by '{state_var}' has only {len(state_list)} states (recommended >= 4).")

        # Scan for transitions out of each state branch
        branches = re.split(r'^\s*[A-Za-z0-9_,\s]+:\s*(?!=\s*)', case_body, flags=re.MULTILINE)
        for idx, branch in enumerate(branches[1:]):
            if idx < len(state_list):
                current_state_name = state_list[idx]
                # Check for state transition statement: State := ...
                has_transition = re.search(rf'\b{re.escape(state_var)}\s*:=', branch, re.IGNORECASE)
                if not has_transition and "ERROR" not in current_state_name.upper() and "FAULT" not in current_state_name.upper():
                    deadlock_states.append(current_state_name)

    if deadlock_states and len(deadlock_states) < len(state_list):
        # Only warn if a subset are missing explicit state re-assignments
        report.add_warning(f"FSM state(s) without detected outgoing transition: {deadlock_states[:5]}")

def check_mpc_horizon(code_text: str, report: SemanticReport):
    """
    Check 4: MPC Prediction Horizon Unroll Verification (N >= 10).
    """
    clean = clean_st_code(code_text)
    clean_norm = clean.replace('_', ' ')
    
    has_mpc = bool(re.search(r'\b(?:MPC|ModelPredictive|PRED_HORIZON|N_HORIZON)\b', clean, re.IGNORECASE) or re.search(r'\b(?:MPC|ModelPredictive|PRED_HORIZON|N_HORIZON)\b', clean_norm, re.IGNORECASE))
    if not has_mpc:
        # Check for documented MPC block (excluding negative phrases like 'No MPC')
        has_mpc = bool(re.search(r'\b(?:Model\s+Predictive\s+Control|MPC\s+Formulation|Prediction\s+Horizon)\b', code_text, re.IGNORECASE)
                       and not re.search(r'\b(?:No|Without|Missing)\s+(?:MPC|Model\s*Predictive)\b', code_text, re.IGNORECASE))
    if not has_mpc:
        report.add_warning("No Model Predictive Control (MPC) references detected.")
        return

    # Look for horizon definition (supports typed constants e.g. N_HORIZON : INT := 10;)
    horizon_match = re.search(r'\b(?:N_HORIZON|PRED_HORIZON|MPC_HORIZON|HORIZON_STEPS)\s*(?::\s*\w+)?\s*(?::=|=)\s*(\d+)', clean, re.IGNORECASE)
    declared_n = int(horizon_match.group(1)) if horizon_match else None
    
    # Check for loop unroll or horizon loop
    horizon_loops = len(re.findall(r'\bFOR\s+\w+\s*:=\s*0\s+TO\s+(?:\d+|N_HORIZON|PRED_HORIZON)\b', clean, re.IGNORECASE))
    
    report.metrics["mpc_declared_n"] = declared_n
    report.metrics["mpc_horizon_loops"] = horizon_loops

    if declared_n is not None and declared_n < 10:
        report.add_warning(f"MPC Prediction Horizon is N={declared_n} (recommended N >= 10 for cyber-physical rigor).")

def check_tmr_completeness(code_text: str, report: SemanticReport):
    """
    Check 5: 2oo3 Triple Modular Redundancy (TMR) Voter & Discrepancy Timer Verification.
    """
    clean = clean_st_code(code_text)
    has_tmr = bool(re.search(r'(?:TMR|2oo3|TwoOutOfThree|Voter|TripleRedundant)', clean, re.IGNORECASE))
    if not has_tmr:
        has_tmr = bool(re.search(r'\b(?:2oo3|Triple\s+Modular\s+Redundan\w*|TMR\s+Voter)\b', code_text, re.IGNORECASE)
                       and not re.search(r'\b(?:No|Without|Missing)\s+(?:TMR|2oo3|Triple)\b', code_text, re.IGNORECASE))

    has_discrepancy = bool(re.search(r'(?:Discrepancy|Mismatch|Deviation|Timer_Discrepancy)', clean, re.IGNORECASE))
    if not has_discrepancy:
        has_discrepancy = bool(re.search(r'\b(?:Discrepancy|Deviation|Mismatch)\s*(?:Timer|Limit|Window|Alarm)\b', code_text, re.IGNORECASE)
                               and not re.search(r'\b(?:No|Without|Missing)\s+(?:Discrepancy|Deviation)\b', code_text, re.IGNORECASE))
    
    report.metrics["has_tmr"] = has_tmr
    report.metrics["has_tmr_discrepancy"] = has_discrepancy
    
    if not has_tmr:
        report.add_error("Missing 2oo3 Triple Modular Redundancy (TMR) voting logic.")
    elif not has_discrepancy:
        report.add_warning("TMR voting present, but no discrepancy / deviation timer detected.")

def validate_semantic_st(code_text: str, filepath: str = "memory_buffer") -> SemanticReport:
    """Run all semantic checks on IEC-ST code string."""
    fb_match = re.search(r'\bFUNCTION_BLOCK\s+(\w+)', code_text, re.IGNORECASE)
    fb_name = fb_match.group(1) if fb_match else "FB_UNKNOWN"
    
    report = SemanticReport(file=filepath, fb_name=fb_name)
    
    check_var_declarations(code_text, report)
    check_matrix_dimensions(code_text, report)
    check_fsm_completeness(code_text, report)
    check_mpc_horizon(code_text, report)
    check_tmr_completeness(code_text, report)
    
    return report

def validate_semantic_file(filepath: Path) -> SemanticReport:
    """Validate a single dataset file."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        if filepath.suffix.lower() == ".json":
            try:
                data = json.load(f)
                content = ""
                for msg in data.get("messages", []):
                    if msg.get("role") == "assistant":
                        content = msg.get("content", "")
                        break
            except Exception as e:
                rep = SemanticReport(file=str(filepath), fb_name="CORRUPT")
                rep.add_error(f"Corrupt JSON: {e}")
                return rep
        else:
            content = f.read()

    # Strip markdown fence if present
    fence_match = re.search(r'```(?:iec-st)?\s*([\s\S]*?)```', content)
    st_code = fence_match.group(1) if fence_match else content

    return validate_semantic_st(st_code, str(filepath))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Semantic & Cyber-Physical Validator")
    parser.add_argument("input_path", nargs="?", default="data/swarm_raw", help="Path to file or directory")
    parser.add_argument("--report", default="reports/semantic_validation_report.json", help="Path for JSON report")
    parser.add_argument("--max-files", type=int, default=None, help="Limit number of scanned files")
    args = parser.parse_args()

    input_p = Path(args.input_path)
    if not input_p.exists():
        print(f"Error: Path {input_p} does not exist.")
        sys.exit(1)

    if input_p.is_file():
        rep = validate_semantic_file(input_p)
        print(f"File: {rep.file}")
        print(f"FB: {rep.fb_name}")
        print(f"Verdict: {rep.verdict}")
        print(f"Errors: {json.dumps(rep.errors, indent=2)}")
        print(f"Warnings: {json.dumps(rep.warnings, indent=2)}")
        print(f"Metrics: {json.dumps(rep.metrics, indent=2)}")
        sys.exit(0 if rep.verdict != "FAIL" else 1)

    json_files = list(input_p.glob("*.json"))
    if args.max_files:
        json_files = json_files[:args.max_files]
        
    print(f"Running semantic audit on {len(json_files)} datasets...")
    counts = {"PASS": 0, "WARN": 0, "FAIL": 0}
    all_reports = []

    for fp in json_files:
        rep = validate_semantic_file(fp)
        counts[rep.verdict] += 1
        all_reports.append({
            "file": Path(rep.file).name,
            "fb_name": rep.fb_name,
            "verdict": rep.verdict,
            "errors": rep.errors,
            "warnings": rep.warnings,
            "metrics": rep.metrics
        })

    print("\n--- SEMANTIC VALIDATION AUDIT ---")
    print(f"Total Scanned: {len(json_files)}")
    print(f"PASS: {counts['PASS']}")
    print(f"WARN: {counts['WARN']}")
    print(f"FAIL: {counts['FAIL']}")

    if args.report:
        rep_p = Path(args.report)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as rf:
            json.dump({"summary": counts, "reports": all_reports}, rf, indent=2)
        print(f"Detailed semantic report saved to {rep_p}")
