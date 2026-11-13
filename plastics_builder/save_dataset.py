# plastics_builder/save_dataset.py
import json
import uuid
import os
import subprocess

def main():
    files = [
        'plastics_builder/st_header_and_io.py',
        'plastics_builder/st_var_declarations.py',
        'plastics_builder/st_phase1_tmr.py',
        'plastics_builder/st_phase2_observers.py',
        'plastics_builder/st_phase3_mpc.py',
        'plastics_builder/st_phase4_fsm.py',
        'plastics_builder/st_phase5_alarms.py'
    ]

    st_code = '\n\n'.join(open(f, 'r', encoding='utf-8').read().strip() for f in files)
    
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `data/swarm_raw/agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

### Assignment:
- **Commercial Industry**: Plastics & High-Performance Polymers (Tier 1 Priority Sector)
- **Target Automation System**: 1,600-Ton All-Electric Multi-Cavity Precision Injection Molding Machine
  - In-mold cavity piezoelectric sensor V/P switchover cascade (velocity-to-pressure holding transfer)
  - Tie-bar strain gauge dynamic clamp tonnage balancing & thermal mold expansion compensation
  - 8-Zone ceramic barrel heating with non-linear melt shear viscosity feedforward
  - Servo toggle clamp resolver synchronization & high-speed pneumatic parts ejector array
- **Function Block Name**: `FB_Plastics_InjectionMolding_CavityPressureVPOvershoot`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 8-State discrete state-space formulation ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) at $T_s = 1$ ms for screw injection position, injection velocity, melt pressure, mold cavity pressure, barrel melt temperature, clamp tonnage, tie-bar strain elongation, and hydraulic back pressure.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional ($Q, R, S, P$), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across critical sensor channels (cavity pressure transducers, nozzle melt pressure sensors, tie-bar strain gauges, barrel melt thermocouples, screw position encoders) with discrepancy timers and bumpless degradation.
   - Deterministic 10 to 14-stage operational Finite State Machine (`CASE State OF ... END_CASE`) covering mold close & lock tonnage, injection filling phase, V/P transfer trigger, holding pressure profile, screw plasticizing/dosing, suck-back decompression, cooling timer, mold opening, robot take-out handshake, and cold-slug jam safe abort.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: `[bar]`, `[kN]`, `[mm]`, `[mm/s]`, `[deg C]`, `[cm3]`, `[%]`.
3. **Parity & Validation**:
   - 100% exact parity: `IF`/`END_IF;`, `CASE`/`END_CASE;`, `FOR`/`END_FOR;`, `FUNCTION_BLOCK`/`END_FUNCTION_BLOCK`.
   - Save to isolated JSON file at `data/swarm_raw/agent_<uuid>.json` with user prompt and assistant response.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: `EVOLUTION COMPLETE: Plastics Injection Molding` along with system details, character count, and parity audit results."""

    assistant_content = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    file_id = uuid.uuid4().hex[:8]
    output_path = f"data/swarm_raw/agent_{file_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Generated dataset file: {output_path}")
    print(f"Assistant content character count: {len(assistant_content)}")
    print(f"Pure ST code character count: {len(st_code)}")
    
    # Run validation
    cmd = ["python", "validate_iec.py", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("\nValidator output:")
    print(result.stdout)
    if result.stderr:
        print("Validator errors:")
        print(result.stderr)
        
    if result.returncode == 0:
        print(f"\nSUCCESS: Dataset {output_path} is 100% valid and ready for training!")
    else:
        print(f"\nFAILURE: Validation exited with code {result.returncode}")

if __name__ == "__main__":
    main()
