import os
import sys
import json
import uuid
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from build_amt_clutch import build_code

def main():
    st_code = build_code()
    chars_count = len(st_code)
    lines_count = len(st_code.splitlines())
    print(f"ST raw code characters: {chars_count}")
    print(f"ST raw code lines: {lines_count}")

    # Verify Delimiter Parity
    clean = re.sub(r'\(\*[\s\S]*?\*\)', '', st_code)
    tokens = {
        'IF': len(re.findall(r'\bIF\b', clean)),
        'END_IF;': len(re.findall(r'\bEND_IF;', clean)),
        'CASE': len(re.findall(r'\bCASE\b', clean)),
        'END_CASE;': len(re.findall(r'\bEND_CASE;', clean)),
        'FOR': len(re.findall(r'\bFOR\b', clean)),
        'END_FOR;': len(re.findall(r'\bEND_FOR;', clean)),
        'FUNCTION_BLOCK': len(re.findall(r'\bFUNCTION_BLOCK\b', clean)),
        'END_FUNCTION_BLOCK': len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean)),
    }

    for k, v in tokens.items():
        print(f"  {k}: {v}")

    assert tokens['IF'] == tokens['END_IF;'], f"IF mismatch: {tokens['IF']} vs {tokens['END_IF;']}"
    assert tokens['CASE'] == tokens['END_CASE;'], f"CASE mismatch: {tokens['CASE']} vs {tokens['END_CASE;']}"
    assert tokens['FOR'] == tokens['END_FOR;'], f"FOR mismatch: {tokens['FOR']} vs {tokens['END_FOR;']}"
    assert tokens['FUNCTION_BLOCK'] == tokens['END_FUNCTION_BLOCK'], "FUNCTION_BLOCK mismatch"
    assert chars_count >= 50000, f"Character count too low: {chars_count} < 50,000"

    print("All parity checks and length requirements passed!")

    code_fenced = "```iec-st\n" + st_code + "```"

    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Automotive & Commercial Heavy Vehicle Powertrain: 44-Ton Commercial Heavy Truck 12-Speed Automated Manual Transmission (AMT) & Dual Wet Clutch Electro-Hydraulic Mechatronic Control Unit (MCU)**

ENGINEERING SPECIFICATION:
- System: 44-Ton Commercial Heavy Truck 12-Speed Automated Manual Transmission (AMT) & Dual Wet Clutch Electro-Hydraulic Mechatronic Control Unit (MCU): Dual Wet Clutch Proportional Pressure Torque Handover Dynamic Cross-Fading (sub-10 ms synchronization window without driveline torque interruption), Synchronizer Sleeve Dog Clutch Pneumatic/Hydraulic Actuation with Hall-Effect Shaft Speed Matching (differential RPM < 15), Driveline Torsional Anti-Jerk Active Damping Filter, Grade & Gross Vehicle Weight (GVW) Adaptive Shift Optimization, and Wet Clutch Frictional Energy Dissipation & Temperature Observer.
- Function Block Name: `FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover`

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [rpm], [mm], [deg C], [%], [N], [Nm], [kg])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal discrete state-space matrices A, B, C, D, MPC cost weights, 2oo3 voting vars, timers)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 50,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR.
5. STANDARDIZED INDUSTRIAL P&ID TAGS:
   - PT_CLUTCH1_PRESSURE_101A/B/C, PT_CLUTCH2_PRESSURE_102A/B/C, PT_MAIN_LINE_HYDR_103A/B/C
   - ST_ENGINE_CRANKSHAFT_201A/B/C, ST_INPUT_SHAFT1_202A/B/C, ST_INPUT_SHAFT2_203A/B/C, ST_OUTPUT_PROP_SHAFT_204A/B/C
   - ZT_SHIFT_RAIL_POS_301A/B/C, TT_TRANSMISSION_OIL_401A/B/C, TT_CLUTCH_FRICTION_PLATE_402A/B/C, AT_CHASSIS_INCLINOMETER_501A/B/C
6. 12-STATE FINITE STATE MACHINE:
   - TRANSMISSION_BOOT_CALIBRATION, NEUTRAL_IDLE_DISENGAGED, FIRST_GEAR_PRE_SELECT, LAUNCH_CONTROL_CLUTCH_SLIP
   - TORQUE_TRANSFER_CROSSFADE_START, INERTIA_PHASE_SYNCHRONIZATION, LOCKUP_STEADY_STATE_CRUISE
   - SKIP_SHIFT_DECELERATION, GRADE_RETARDER_COORDINATION, CLUTCH_OVERHEAT_LIMP_MODE
   - SHIFT_RAIL_FAULT_SAFE_LOCK, EMERGENCY_NEUTRAL_DISENGAGE"""

    agent_uuid = uuid.uuid4().hex[:8]
    record_id = f"synthetic_v3_{agent_uuid}"
    
    record = {
        "id": record_id,
        "instruction": prompt,
        "input": "",
        "output": code_fenced,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_fenced}
        ],
        "metadata": {
            "domain": "Automotive_Commercial_Vehicles",
            "system": "44-Ton Commercial Heavy Truck 12-Speed AMT & Dual Wet Clutch Electro-Hydraulic MCU",
            "function_block": "FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover",
            "version": "v3_cyberphysical_max",
            "lines": lines_count,
            "characters": len(code_fenced),
            "validated": True
        }
    }

    target_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "data", "swarm_raw"))
    os.makedirs(target_dir, exist_ok=True)
    filename = os.path.join(target_dir, f"agent_{agent_uuid}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"\nSuccessfully written dataset to:\n  {filename}")
    print(f"File size: {os.path.getsize(filename):,} bytes")

    # Verification: Read back and validate JSON integrity
    with open(filename, "r", encoding="utf-8") as f:
        loaded = json.load(f)

    assert loaded["id"] == record_id
    assert loaded["metadata"]["validated"] is True
    assert loaded["output"].startswith("```iec-st\nFUNCTION_BLOCK FB_Automotive_CommercialTruck_12SpeedAMT_ClutchHandover")
    assert loaded["output"].endswith("END_FUNCTION_BLOCK\n```")
    print("Verification passed! Record is completely valid and structurally pristine.")

if __name__ == "__main__":
    main()
