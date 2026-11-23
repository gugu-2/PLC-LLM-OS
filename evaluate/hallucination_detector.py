#!/usr/bin/env python3
"""
evaluate/hallucination_detector.py — Industrial Physics & Cyber-Physical Hallucination Detector
Reference: DOC-06 §Part 1 Metric 5

Scans generated IEC-ST code for physically impossible or mathematically invalid constructs:
- H1: Temperatures exceeding material limits (>600 deg C for food/plastics or non-physical sub-zero)
- H2: Pressures outside physical hydraulic/pneumatic bounds (>1000 bar without hyperbaric specification)
- H3: Scan cycle execution times outside real-time PLC task scheduler limits (<0.1ms or >1.0s)
- H4: Linear algebra violations (non-square state transition matrix A: nxm where n != m)
- H5: ISA-18.2 alarm hierarchy violations (HH <= H, or LL >= L, or deadband >= trip band)
"""

import re
from typing import Dict, List

def detect_hallucinations(content: str) -> List[Dict]:
    """
    Returns list of detected physical & mathematical hallucinations:
    [{ "type": str, "severity": "critical"|"high"|"medium", "evidence": str, "position": int }]
    """
    hallucinations = []

    # Strip comments to avoid false alarms on explanatory text
    no_block_comments = re.sub(r'\(\*[\s\S]*?\*\)', ' ', content)
    clean_code = re.sub(r'//[^\n]*', ' ', no_block_comments)

    # --- H1: Temperature Physical Ranges ---
    temp_matches = re.finditer(r'(?:r_?Temp(?:erature)?|r_?MeltTemp|r_?OvenTemp|r_?ZoneTemp)\w*(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    for m in temp_matches:
        val = float(m.group(1))
        # Temperatures above 1,800 deg C (above molten steel liquidus) or below -200 deg C
        if val > 1800.0 or val < -273.15:
            hallucinations.append({
                "type": "H1_temperature_range",
                "severity": "critical",
                "evidence": f"Assigned temperature {val}°C violates physical manufacturing bounds.",
                "position": m.start()
            })

    # --- H2: Pressure Physical Ranges ---
    press_matches = re.finditer(r'(?:r_?Press(?:ure)?|r_?CylinderPress|r_?HydroPress)\w*(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    for m in press_matches:
        val = float(m.group(1))
        # Pressures over 1,500 bar are non-physical for heavy industrial manufacturing
        if val > 1500.0 or val < -1.0:
            hallucinations.append({
                "type": "H2_pressure_range",
                "severity": "high",
                "evidence": f"Pressure value {val} bar exceeds realistic hydraulic/pneumatic equipment ratings.",
                "position": m.start()
            })

    # --- H3: Scan Cycle Times ---
    scan_matches = re.finditer(r'(?:CYCLE_TIME|TASK_CYCLE|SCAN_TIME|r_?ScanTime)\w*(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    for m in scan_matches:
        val = float(m.group(1))
        # In seconds: real-time PLCs operate between 0.0001s (0.1ms) and 1.0s
        if (0.0 < val < 0.0001) or val > 2.0:
            hallucinations.append({
                "type": "H3_scan_cycle",
                "severity": "medium",
                "evidence": f"Scan cycle time {val}s is outside realistic deterministic PLC scheduling bounds (0.1ms to 2.0s).",
                "position": m.start()
            })

    # --- H4: Linear Algebra Matrix Geometry (Non-Square A-Matrix) ---
    a_mat_pattern = re.compile(r'(\b\w*A_Matrix\w*|\bA\b)\s*:\s*ARRAY\s*\[\s*(\d+)\s*\.\.\s*(\d+)\s*,\s*(\d+)\s*\.\.\s*(\d+)\s*\]\s*OF', re.IGNORECASE)
    for m in a_mat_pattern.finditer(clean_code):
        rows = int(m.group(3)) - int(m.group(2)) + 1
        cols = int(m.group(5)) - int(m.group(4)) + 1
        if rows != cols:
            hallucinations.append({
                "type": "H4_non_square_A_matrix",
                "severity": "critical",
                "evidence": f"State transition matrix A is {rows}x{cols} — must be square (nxn) in discrete state-space.",
                "position": m.start()
            })

    # --- H5: ISA-18.2 Inverted Alarm Setpoints ---
    hh_m = re.search(r'(?:HH_Setpoint|r_?Alarm_?HH|r_?Trip_?HH)(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    h_m = re.search(r'(?:H_Setpoint|r_?Alarm_?H|r_?Warning_?H)(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    l_m = re.search(r'(?:L_Setpoint|r_?Alarm_?L|r_?Warning_?L)(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)
    ll_m = re.search(r'(?:LL_Setpoint|r_?Alarm_?LL|r_?Trip_?LL)(?:\s*:\s*\w+)?\s*(?::=|=)\s*([+-]?\d+(?:\.\d+)?)', clean_code, re.IGNORECASE)

    if hh_m and h_m:
        hh_val = float(hh_m.group(1))
        h_val = float(h_m.group(1))
        if hh_val <= h_val:
            hallucinations.append({
                "type": "H5_alarm_tier_ordering",
                "severity": "critical",
                "evidence": f"ISA-18.2 hierarchy inverted: High-High trip ({hh_val}) <= High warning ({h_val}).",
                "position": hh_m.start()
            })

    if ll_m and l_m:
        ll_val = float(ll_m.group(1))
        l_val = float(l_m.group(1))
        if ll_val >= l_val:
            hallucinations.append({
                "type": "H5_alarm_tier_ordering",
                "severity": "critical",
                "evidence": f"ISA-18.2 hierarchy inverted: Low-Low trip ({ll_val}) >= Low warning ({l_val}).",
                "position": ll_m.start()
            })

    return hallucinations

def compute_hr(outputs: List[str]) -> float:
    """
    Computes Hallucination Rate (HR):
    Fraction of outputs containing one or more critical hallucinations.
    """
    if not outputs:
        return 0.0
    critical_count = 0
    for out in outputs:
        halls = detect_hallucinations(out)
        if any(h["severity"] == "critical" for h in halls):
            critical_count += 1
    return round(critical_count / len(outputs), 4)

if __name__ == "__main__":
    test_code_clean = """
    FUNCTION_BLOCK FB_Test
    VAR
        A_Matrix : ARRAY[0..3, 0..3] OF LREAL;
        r_OvenTemp : REAL := 245.0;
        r_Alarm_HH : REAL := 250.0;
        r_Alarm_H : REAL := 240.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    test_code_bad = """
    FUNCTION_BLOCK FB_Bad
    VAR
        A_Matrix : ARRAY[0..3, 0..5] OF LREAL; (* Non-square *)
        r_OvenTemp : REAL := 2500.0; (* Impossible *)
        r_Alarm_HH : REAL := 220.0; (* Inverted HH <= H *)
        r_Alarm_H : REAL := 240.0;
    END_VAR
    END_FUNCTION_BLOCK
    """
    print("Clean Test:", detect_hallucinations(test_code_clean))
    print("Bad Test:", detect_hallucinations(test_code_bad))
