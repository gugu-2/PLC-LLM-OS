# scratch/assemble_and_validate.py
import os
import sys
import json
import uuid
import re
import subprocess

from parts_builder import get_header
from gen_declarations import get_declarations
from gen_phase1 import get_phase1
from gen_phase2 import get_phase2
from gen_phase3 import get_phase3
from gen_phase4 import get_phase4
from gen_phase5 import get_phase5

def main():
    print("Assembling IEC 61131-3 Function Block...")
    header = get_header()
    decl = get_declarations()
    p1 = get_phase1()
    p2 = get_phase2()
    p3 = get_phase3()
    p4 = get_phase4()
    p5 = get_phase5()

    code = header + decl + p1 + p2 + p3 + p4 + p5
    code = code.strip()

    print(f"Total Structured Text character count: {len(code)}")

    # Check parity and basic rules locally
    lines = [l.strip() for l in code.splitlines() if l.strip()]
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")

    if not lines[0].startswith("FUNCTION_BLOCK FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell"):
        print("ERROR: First line does not match expected declaration!")
        sys.exit(1)

    if lines[-1] != "END_FUNCTION_BLOCK":
        print(f"ERROR: Last line is '{lines[-1]}', expected 'END_FUNCTION_BLOCK'!")
        sys.exit(1)

    # Parity check
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
    clean_code = re.sub(r'\'[^\']*\'', '', no_comments)

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

    print(f"Parity Audit:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_starts} | END_FUNCTION_BLOCK: {fb_ends} (Match: {fb_starts == fb_ends})")

    if ifs != end_ifs or cases != end_cases or fors != end_fors or fb_starts != fb_ends:
        print("ERROR: Parity mismatch detected!")
        sys.exit(1)

    # Prompt text
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Nuclear Power Generation & Safety-Critical Thermo-Hydraulics (PWR Pressurized Water Reactor Steam Generator Level Control & Shrink/Swell Compensation)
FUNCTION BLOCK NAME: FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 25 ms):
   - 8-State model capturing steam generator thermo-hydraulics, non-minimum phase zero (reverse level swell on cold feedwater injection, shrink on steam load increase), thermal lag, downcomer recirculation, void fraction dynamics, and mass balance:
     States: x1=Narrow-Range Level [mm], x2=Downcomer Flow Rate [kg/s], x3=Boiling Riser Average Void Fraction [ratio 0..1], x4=Primary-to-Secondary Heat Transfer Rate [MW], x5=Steam Drum Pressure [bar], x6=Cold Leg Temperature [degC], x7=Feedwater Valve Trim Position [%], x8=Steam Line Non-Minimum Phase Dynamic Lead/Lag State [mm].
   - Provide explicit, non-zero system matrices: A (8x8), B (8x5), C (5x8), D (5x5).
   - Write out state propagation explicitly: x[k+1] = A * x[k] + B * u[k].
   - Provide Kalman filter observer equations with gain matrix L (8x5).

2. Receding Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Horizon N = 5 steps, 6 iterations of unrolled projected gradient descent.
   - Dynamic inverse response compensation (cancelling non-minimum phase shrink/swell illusion using steam flow / feedwater flow feedforward ratio).
   - Quadratic cost function: Q state penalty matrix, R control effort penalty matrix, P terminal penalty matrix.
   - Actuator constraints: Feedwater regulating valve (MFRV) [0..100%], low-power bypass valve [0..100%], slew rate limits [5%/s].

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Steam Generator Narrow Range Level (LT_NR_101A/B/C) [mm]
     * Steam Generator Wide Range Level (LT_WR_102A/B/C) [mm]
     * Main Steam Drum Pressure (PT_MS_201A/B/C) [bar]
     * Main Steam Mass Flow Rate (FT_MS_301A/B/C) [t/h]
     * Main Feedwater Mass Flow Rate (FT_FW_401A/B/C) [t/h]
   - Discrepancy accumulation timers (threshold 500 ms) and bumpless degradation.

4. Deterministic 14-Stage Nuclear State Machine (FSM):
   - CASE eState OF:
     0: COLD_SHUTDOWN_HOT_STANDBY_TRANSFER
     1: STARTUP_LOW_POWER_BYPASS_CONTROL (<15% FP)
     2: MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS
     3: AT_POWER_CASCADE_FEEDFORWARD_STABILIZED (15% - 50% FP)
     4: FULL_POWER_OPTIMAL_MPC_TRACKING (50% - 100% FP)
     5: RAPID_LOAD_REJECTION_TURBINE_RUNBACK (-5%/min)
     6: MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE
     7: STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC (SGTR leak rate radiation check)
     8: AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START
     9: AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT
     10: DRY_OUT_PROTECTION_RAPID_COOLDOWN
     11: OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION
     12: REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE
     13: POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM
   - Fully implement every single state transition and logic.

5. ISA-18.2 Nuclear Class 1E Process Alarms & 32-Bit Telemetry:
   - HH (Reactor Trip SCRAM), H (Turbine Runback / Alert), L (Low Water Warning), LL (Aux Feedwater Auto-Start SCRAM).
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    assistant_content = f"```iec-st\n{code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ],
        "output": assistant_content
    }

    raw_dir = "data/swarm_raw"
    os.makedirs(raw_dir, exist_ok=True)
    file_id = uuid.uuid4().hex[:8]
    output_filename = os.path.join(raw_dir, f"agent_{file_id}.json")

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset file to: {output_filename}")
    print(f"Assistant content length: {len(assistant_content)} characters")

    # Run validate_iec.py
    cmd = [sys.executable, "validate_iec.py", output_filename]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("validate_iec.py output:")
    print(res.stdout)
    if res.stderr:
        print("validate_iec.py stderr:")
        print(res.stderr)

    if res.returncode != 0:
        print(f"Validation FAILED with exit code {res.returncode}")
        sys.exit(res.returncode)
    else:
        print("Validation SUCCESSFUL!")

if __name__ == "__main__":
    main()
