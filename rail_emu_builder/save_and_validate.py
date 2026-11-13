# rail_emu_builder/save_and_validate.py
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

from assemble_rail import assemble_code
import validate_iec

def main():
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_id}.json"
    output_path = os.path.join(root_dir, "data", "swarm_raw", output_filename)
    
    prompt = """You are assigned to generate ONE production-grade, ultra-dense, mathematically complete IEC 61131-3 Structured Text synthetic training dataset.

### Assignment:
- **Commercial Industry**: Rail Transit, High-Speed Trains & Locomotive Traction (Tier 1 Priority Sector)
- **Target Automation System**: 350 km/h High-Speed Electric Multiple Unit (EMU) Traction & Braking Control Unit (TCU/BCU)
  - 4-Quadrant AC/DC converter & dynamic induction motor field-oriented vector control (FOC)
  - Microprocessor wheel slip-slide protection (WSSP) with Curtius-Kniffler non-linear rail-wheel adhesion observer
  - Active pneumatic pantograph catenary contact force regulation (120 to 180 N) with aerodynamic uplift compensation
  - Blended electro-dynamic regenerative / pneumatic brake management with axle load dynamic redistribution
- **Function Block Name**: `FB_Rail_HighSpeed_EMU_TractionBraking_WSSP`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 8-State discrete state-space formulation ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) at $T_s = 5$ ms for train longitudinal velocity, 4 bogie axle rotational velocities, catenary contact force, DC link filter capacitor voltage, traction motor electromagnetic torque, brake cylinder pneumatic pressure, and rail-wheel adhesion coefficient.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional ($Q, R, S, P$), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (Doppler radar train ground speed, optical wheel speed encoders, catenary pantograph load cells, DC link differential voltage probes, brake pipe pressure transducers) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (`CASE State OF ... END_CASE`) covering pantograph raise & vacuum circuit breaker (VCB) close, pre-charging line converter, traction motoring standby, automatic train operation (ATO) speed tracking, high-speed cruise, dynamic field-weakening, micro-slip search & adhesion recovery, regenerative service braking, electro-pneumatic blended stop, standstill parking brake clamp, and emergency brake (EB) failsafe de-energize trip.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: `[km/h]`, `[rpm]`, `[kN]`, `[V]`, `[A]`, `[bar]`, `[N]`, `[%]`.
3. **Parity & Validation**:
   - 100% exact parity: `IF`/`END_IF;`, `CASE`/`END_CASE;`, `FOR`/`END_FOR;`, `FUNCTION_BLOCK`/`END_FUNCTION_BLOCK`.
   - Save to isolated JSON file at `data/swarm_raw/agent_<uuid>.json` with user prompt and assistant response.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: `EVOLUTION COMPLETE: High-Speed Rail EMU Traction & Braking` along with system details, character count, and parity audit results."""

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
