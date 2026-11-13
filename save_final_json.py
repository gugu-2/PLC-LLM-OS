import json
import uuid
import os
import sys
import subprocess
import test_build

def main():
    prompt = """You are assigned to generate ONE production-grade, ultra-dense, mathematically complete IEC 61131-3 Structured Text synthetic training dataset.

### Assignment:
- **Commercial Industry**: Mining, Heavy Mineral Processing & Beneficiation (Tier 1 Priority Sector)
- **Target Automation System**: 40-Foot Semi-Autogenous Grinding (SAG) & Ball Mill Closed Circuit
  - 28 MW gearless ring motor drive with frozen charge detection & angle-torque acoustic impact monitoring
  - Hydrostatic trunnion bearing lubrication lift pressure & Reynolds viscosity dynamic oil temperature regulation
  - 14-Cyclone hydrocyclone manifold classification with slurry density Coriolis & ultrasonic particle size ($P_{80} \\sim 75\\ \\mu\\text{m}$)
  - Pebble crusher circuit variable recycle ratio & dynamic mill volumetric slurry pool level observer
- **Function Block Name**: `FB_Mining_SAG_BallMill_ComminutionClassification`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 8-State discrete state-space formulation ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) at $T_s = 50$ ms for SAG mill total charge mass, internal slurry volumetric holdup, toe impact angle, motor power draw, cyclone feed sump level, overflow slurry density, ball mill circulating load, and product particle size $P_{80}$.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional ($Q, R, S, P$), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (feed/discharge trunnion bearing pressure transducers, acoustic shell impact microphones, gearless motor torque/power meters, cyclone feed density nuclear/Coriolis gauges, sump ultrasonic level sensors) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (`CASE State OF ... END_CASE`) covering trunnion jacking oil permissive, inching drive disengage, mill slow acceleration ramp, water-to-ore feed ratio lock, pebble recycle cut-in, acoustic shell liner protection (direct impact prevention), cyclone manifold staging, slurry overfilling cutback, controlled grind-out flush, and frozen charge emergency trip.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: `[t/h]`, `[kW]`, `[bar]`, `[rpm]`, `[deg]`, `[um]`, `[m3/h]`, `[%]`.
3. **Parity & Validation**:
   - 100% exact parity: `IF`/`END_IF;`, `CASE`/`END_CASE;`, `FOR`/`END_FOR;`, `FUNCTION_BLOCK`/`END_FUNCTION_BLOCK`.
   - Save to isolated JSON file at `data/swarm_raw/agent_<uuid>.json` with user prompt and assistant response.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: `EVOLUTION COMPLETE: Mining SAG Ball Mill Grinding` along with system details, character count, and parity audit results."""

    iec_code = test_build.build()
    assistant_content = f"```iec-st\n{iec_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    file_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{file_id}.json"
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully created and saved to: {filename}")
    print(f"Total Assistant Content Length: {len(assistant_content)} characters")
    return filename

if __name__ == "__main__":
    fn = main()
    print("Testing validation on saved JSON file...")
    import subprocess
    res = subprocess.run([sys.executable, "validate_iec.py", fn], capture_output=True, text=True)
    print("Validator Output:\n", res.stdout)
    if res.stderr:
        print("Validator Stderr:\n", res.stderr)
    if res.returncode != 0:
        print("Validation Failed!")
        sys.exit(1)
    else:
        print("Validation Succeeded with 0 errors!")
