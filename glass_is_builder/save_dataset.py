import os
import sys
import json
import uuid

# Add current dir to sys.path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble import assemble_code

def save_and_validate():
    prompt = """You are assigned to generate ONE production-grade, ultra-dense, mathematically complete IEC 61131-3 Structured Text synthetic training dataset.

### Assignment:
- **Commercial Industry**: Glass, Ceramics & Container Manufacturing (Tier 1 Priority Sector)
- **Target Automation System**: High-Speed Glass Forehearth & 12-Section Quad-Gob Individual Section (IS) Machine
  - Forehearth oxy-fuel multi-zone thermal conditioning & gob feeder plunger stroke servo synchronization
  - Dual high-speed optical vision pyrometry for gob weight / drop shape verification & pneumatic shear cut-off
  - 12-Section electronic timing drum (parison blow-and-blow / press-and-blow) with servo invert/take-out mechanism
  - Continuous annealing lehr heating/cooling zone gradient temperature control & cullet conveyor recycling
- **Function Block Name**: `FB_Glass_IS_Machine_ForehearthGobShear_LehrAnneal`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 8-State discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 5 ms for forehearth glass melt temperature profile, gob mass, shear blade velocity, blank mold contact time, parison internal pressure, blow mold reheat rate, take-out transfer angular position, and lehr belt annealing stress.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (forehearth tri-level Pt/Rh thermocouples, optical infrared pyrometers, gob weight high-speed laser scanners, blow air pressure transmitters, section servo resolver angles) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (CASE State OF ... END_CASE) covering forehearth thermal soak, gob feeder plunge, shear cut, delivery trough chute, blank mold settle blow, baffle seal & counter blow, invert swing, final blow mold expansion, take-out deadplate transfer, cross-conveyor stacker push, lehr tunnel annealing, and emergency shear lock / cullet drop abort.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [deg C], [g], [bar], [mm/s], [gobs/min], [deg], [MPa], [%].
3. **Parity & Validation**:
   - 100% exact parity: IF/END_IF;, CASE/END_CASE;, FOR/END_FOR;, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
   - Save to isolated JSON file at data/swarm_raw/agent_<uuid>.json with user prompt and assistant response.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 0 errors."""

    st_code = assemble_code()
    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "swarm_raw")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {filename}")
    print(f"Assistant Content Character Count: {len(assistant_content)}")
    return filename

if __name__ == "__main__":
    fn = save_and_validate()
