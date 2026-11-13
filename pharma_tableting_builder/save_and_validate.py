# c:\Users\majip\Downloads\LLM REASEARCH\pharma_tableting_builder\save_and_validate.py
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

from assemble_pharma import assemble_code
import validate_iec

def main():
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_id}.json"
    output_path = os.path.join(root_dir, "data", "swarm_raw", output_filename)
    
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Pharmaceutical Oral Solid Dosage (OSD) & Continuous Manufacturing (Tier 1 Priority Sector)
- System: Continuous Twin-Screw Wet Granulation, Multi-Cell Fluid Bed Drying & Rotary Tableting Line
  - Loss-in-weight twin-screw continuous wet granulator with liquid binder peristaltic micro-pump cascade
  - Multi-cell continuous fluid bed dryer with in-line microwave resonance / NIR loss-on-drying (LOD) moisture tracking
  - High-speed rotary tablet press (250,000 tablets/h) with pre-compression & main compression instrumented punch load cells (0 to 100 kN)
  - Single-tablet dynamic weight / thickness / hardness de-coupling observer with high-speed pneumatic blow-off reject gate (< 10 ms)
- Function Block Name: FB_Pharma_ContinuousTableting_Granulation_TabletPress

NEXT-GEN QUALITY REQUIREMENTS:
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters). Zero placeholders, zero ellipses, every equation, matrix element, and state transition fully coded.
2. First-Principles Cyber-Physical Formulation:
   - 8-State discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 2 ms for powder mass feed rate, granulator liquid-to-solid ratio (L/S), granule mean particle diameter (d50), fluid bed moisture content (% LOD), fluidization air temperature, turret rotational speed, main compression punch peak force, and tablet tensile strength / porosity.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (twin loss-in-weight feeder load cells, microwave moisture resonance cavity probes, rotary press piezoelectric punch load cells, turret resolver shaft encoders, fluid bed plenum differential pressure transmitters) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (CASE State OF ... END_CASE) covering recipe parameter handshake, twin-screw granulator dry run pre-blend, liquid binder cut-in, fluid bed warmup, multi-cell granule transport, rotary press feeder shoe fill, pre-compression de-aeration, main compression coining, individual tablet outfeed reject monitoring, automated punch lubrication, production batch drain, and punch overpressure / die jam emergency stop.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [kg/h], [%], [um], [deg C], [rpm], [kN], [N], [mm], [mbar], [g/min], [m3/h].
3. Strict Syntax & Parity Rules:
   - Triple backticks with iec-st: ```iec-st ... ```
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - First line: FUNCTION_BLOCK FB_Pharma_ContinuousTableting_Granulation_TabletPress
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
