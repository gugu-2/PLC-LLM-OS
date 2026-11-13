# c:\Users\majip\Downloads\LLM REASEARCH\battery_pack_builder\save_and_validate.py
import os
import sys
import json
import uuid

pkg_dir = os.path.dirname(os.path.abspath(__file__))
if pkg_dir not in sys.path:
    sys.path.insert(0, pkg_dir)
root_dir = os.path.abspath(os.path.join(pkg_dir, ".."))
if root_dir not in sys.path:
    sys.path.insert(0, root_dir)

from assemble_pack import assemble_code
import validate_iec

def main():
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_id}.json"
    output_path = os.path.join("data", "swarm_raw", output_filename)
    
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Automotive & Electric Vehicle (EV) Manufacturing (Tier 1 Priority Sector)
- System: Mega-Scale Automated Cell-to-Pack (CTP) Battery Assembly Line
  - Dual-component structural polyurethane adhesive dispense with laser profile bead tracking
  - 1070nm multi-kW fiber laser busbar wobble welding with real-time melt pool pyrometry and plume optical feedback
  - High-voltage isolation/hi-pot verification and laser safety interlock enclosure
- Function Block Name: FB_Automotive_EV_BatteryPack_LaserWeldingDispense

NEXT-GEN QUALITY REQUIREMENTS:
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters). Zero placeholders, zero ellipses, every equation, matrix element, and state transition fully coded.
2. First-Principles Cyber-Physical Formulation:
   - 8-State discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 5 ms for adhesive bead rheology, nozzle dispense pressure, robot TCP velocity feedforward, laser weld pool temperature, and weld penetration depth.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (bead height laser, dispense fluid pressure, weld pyrometer temperature, hi-pot leakage current, robot TCP velocity feedback) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (CASE State OF ... END_CASE) covering robot homing, surface plasma pre-treatment, bead vision dispense, laser head wobble alignment, busbar weld sequence, hi-pot test, and safe abort.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [bar], [deg C], [mm/s], [kW], [um], [mA], [%], [kJ], [Hz], [mm], [MPa], [kV].
3. Strict Syntax & Parity Rules:
   - Triple backticks with iec-st: ```iec-st ... ```
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - First line: FUNCTION_BLOCK FB_Automotive_EV_BatteryPack_LaserWeldingDispense
   - Last line: END_FUNCTION_BLOCK
4. Validation & Delivery:
   - Save your dataset to data/swarm_raw/agent_<uuid>.json with complete user/assistant message structure.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

    raw_st = assemble_code()
    asst_content = f"```iec-st\n{raw_st}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Dataset saved to: {output_path}")
    print(f"Assistant content character count: {len(asst_content)}")
    print(f"Running validation...")
    
    errs = validate_iec.validate_json_file(output_path)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        print(f"AGENT_FILE={output_path}")
        print(f"CHAR_COUNT={len(asst_content)}")
        return output_path, len(asst_content)

if __name__ == "__main__":
    main()
