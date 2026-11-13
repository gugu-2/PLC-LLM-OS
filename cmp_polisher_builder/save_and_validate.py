# cmp_polisher_builder/save_and_validate.py
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

from assemble_cmp import assemble_code
import validate_iec

def main():
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_id}.json"
    output_path = os.path.join(root_dir, "data", "swarm_raw", output_filename)
    
    prompt = """You are assigned to generate ONE production-grade, ultra-dense, mathematically complete IEC 61131-3 Structured Text synthetic training dataset.

### Assignment:
- **Commercial Industry**: Semiconductor Silicon Fabrication & Wafer Processing (Tier 1 Priority Sector)
- **Target Automation System**: 300mm Silicon Wafer Chemical Mechanical Planarization (CMP) Polishing Station
  - Multi-zone carrier head (5 independent air/membrane pressure zones + retaining ring) dynamic force profile
  - In-line optical reflectance spectrometry & eddy current copper thickness endpoint detection (EPD < 20 Å accuracy)
  - Pad surface diamond conditioner oscillation sweep profile with acoustic emission friction wear monitoring
  - Multi-channel abrasive chemical slurry injection with real-time pH, redox potential, and temperature cascade
- **Function Block Name**: `FB_Semiconductor_CMP_300mm_WaferPolishing`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 8-State discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 5 ms for platen rotational speed, wafer carrier rotational speed, zone membrane pressure profile, remaining Cu/oxide film thickness, polishing pad surface temperature, friction torque, slurry chemical flow rate, and diamond pad cut rate.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (spectrometric optical reflectance intensity, eddy current thickness probes, platen torque load cells, membrane zone pressure sensors, polishing pad infrared pyrometers) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (CASE State OF ... END_CASE) covering wafer vacuum pickup & load cup handshake, platen sweep approach, low-pressure touch-down, multi-zone bulk polish ramp, optical endpoint detection lock, soft landing over-polish, chemical slurry de-ionized water flush, carrier vacuum unclamp & lift, pad diamond re-conditioning, and broken wafer vacuum loss emergency trip.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [rpm], [psi], [Angstrom], [deg C], [Nm], [mL/min], [um/h], [%].
3. **Parity & Validation**:
   - 100% exact parity: IF/END_IF;, CASE/END_CASE;, FOR/END_FOR;, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
   - Save to isolated JSON file at data/swarm_raw/agent_<uuid>.json with user prompt and assistant response.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: EVOLUTION COMPLETE: Semiconductor 300mm CMP Wafer Polishing along with system details, character count, and parity audit results."""

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
    
    errors = validate_iec.validate_json_file(output_path)
    if errors:
        print("VALIDATION FAILED:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return output_path, len(asst_content)

if __name__ == "__main__":
    main()
