# twin_screw_builder/save_dataset.py
import json
import uuid
import os
import subprocess
import sys

def main():
    files = [
        'twin_screw_builder/st_header_and_io.py',
        'twin_screw_builder/st_var_declarations.py',
        'twin_screw_builder/st_phase1_tmr.py',
        'twin_screw_builder/st_phase2_observers.py',
        'twin_screw_builder/st_phase3_mpc.py',
        'twin_screw_builder/st_phase4_fsm.py',
        'twin_screw_builder/st_phase5_alarms.py'
    ]

    st_code = '\n\n'.join(open(f, 'r', encoding='utf-8').read().strip() for f in files)
    
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `data/swarm_raw/agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

### Assignment:
- **Commercial Industry**: Plastics, Polymers & Advanced Compounding (Tier 1 Priority Sector)
- **Target Automation System**: High-Output Co-Rotating Twin-Screw Extruder (133 mm Screw Diameter, 48:1 L/D Ratio) for Engineering Plastics Compounding (PA66 + 30% Glass Fiber + Flame Retardant):
  - 12-Zone induction/ceramic barrel heating cascade with dynamic non-linear viscous shear heating feedforward decoupling
  - 5-Feeder gravimetric loss-in-weight (LIW) continuous ratio dosing (primary resin, impact modifier, flame retardant, color masterbatch, downstream glass fiber side-feeder)
  - Positive displacement melt gear pump (450 cm3/rev) synchronous speed and suction pressure closed-loop MPC stabilization (45.0 bar +/- 1.0 bar)
  - Zone 9 high-vacuum volatile degassing skid (-0.95 bar) with moisture/monomer trap monitoring
  - Underwater strand / pelletizer system (UWP) with 2,500 rpm cutter hub, tempered water circulation loop (65 °C), hydraulic water box clamping, and 3-way bypass diverter valve
- **Function Block Name**: `FB_Plastics_TwinScrewExtrusion_Compounding_MeltPressure`

### Quality Directives (V7 Max-Persona Protocol):
1. **Extreme Token & Character Density**: Target 75,000 to 125,000+ characters. Zero placeholders, zero ellipses, every equation, matrix, timer, and state transition fully coded.
2. **First-Principles Cyber-Physical Formulation**:
   - 16-State discrete state-space formulation (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) at Ts = 20 ms for 12 barrel zone temperatures, bulk polymer melt temperature, die melt pressure, screw shaft torque, and gear pump suction pressure.
   - Receding-horizon Model Predictive Control (MPC) with 6 unrolled Projected Gradient Descent (PGD) optimization iterations, actuator box constraints, and dynamic acceleration slew rate limiters.
   - Dynamic viscous dissipation decoupling feedforward subtracting mechanical shear power from barrel heating zones to eliminate thermal runaway.
   - 2oo3 Triple Modular Redundancy (TMR) voting across 4 critical sensor triplets (Die Melt Pressure PT-101A/B/C, Adapter Melt Temp TT-201A/B/C, Screw Torque TT-301A/B/C, Pelletizer Water Temp TT-401A/B/C) with leaky-bucket persistence timers and bumpless degradation.
   - Deterministic 14-stage operational Finite State Machine (CASE uiCurrentState OF ... END_CASE) covering cold soak pre-heat, equilibrium hold (1800 s dwell), feeder tare check, screw inching purge, primary polymer ramp, glass fiber side-feed intro, vacuum pull, die pressure build-up, gear pump synchronization, underwater pelletizer spin and clamp, continuous high-rate compounding, die flush purge transition, controlled cooling ramp, and emergency torque overload trip.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: `[bar]`, `[°C]`, `[rpm]`, `[kg/h]`, `[kW]`, `[Nm]`, `[m3/h]`, `[%]`, `[BOOL]`, `[DWORD]`.
3. **Parity & Validation**:
   - 100% exact delimiter parity: `IF`/`END_IF;`, `CASE`/`END_CASE;`, `FOR`/`END_FOR;`, `FUNCTION_BLOCK`/`END_FUNCTION_BLOCK`.
   - Save to isolated JSON file at `data/swarm_raw/agent_<uuid>.json` with user prompt and assistant response.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 0 errors.
4. **Completion Message**:
   Reply to the parent agent with: `EVOLUTION COMPLETE: Plastics Twin-Screw Extrusion Compounding` along with system details, character count, and parity audit results."""

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
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Dataset successfully created at: {output_path}")
    print(f"Total Assistant Content Length: {len(assistant_content)} characters")
    
    # Run validation script
    cmd = [sys.executable, "validate_iec.py", output_path]
    print(f"Running validation: {' '.join(cmd)}")
    res = subprocess.run(cmd, capture_output=True, text=True)
    print(res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)
        
    if res.returncode == 0:
        print(">>> ALL VERIFICATION CRITERIA PERFECTLY SATISFIED <<<")
    else:
        print(">>> VALIDATION FAILED! <<<")
        sys.exit(1)

if __name__ == "__main__":
    main()
