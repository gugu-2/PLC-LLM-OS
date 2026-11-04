import os
import json
import uuid
import generate_aerospace_dataset
import validate_iec

USER_PROMPT = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Aerospace Defense & Ground Test Facilities** industry.

**Domain**: Mach 7 Continuous Blowdown Hypersonic Wind Tunnel High-Enthalpy Air Storage Facility: Zirconia Pebble-Bed Regenerative Storage Heater (stagnation temperature T_0 = 2,200 K, pressure P_0 = 150 bar), Liquid Nitrogen (LN2) Cryogenic Cooled Convergent-Divergent Contoured Nozzle Throat (active heat flux 18 MW/m²), Fast Electro-Hydraulic Throttle Valve (stroke time < 150 ms), Vacuum Sphere Multi-Stage Steam Ejector Backpressure Matching, and Real-Time Optical Schlieren Shockwave Angle Observer.

**Function Block Name**: `FB_Aerospace_HypersonicTunnel_CryoAir_PebbleHeater`

**Engineering Context & Industrial Requirements**:
1. Transmitter & Tag Nomenclature:
   - Standardized industrial P&ID tags: `PT_PEBBLE_BED_TOP_101A/B/C`, `TT_PEBBLE_BED_CORE_201A/B/C`, `PT_NOZZLE_STAGNATION_301A/B/C`, `TT_NOZZLE_THROAT_WALL_401A/B/C`, `FT_LN2_COOLANT_501A/B/C`, `PT_DIFFUSER_EXIT_601A/B/C`, `PT_TEST_CABIN_STATIC_701A/B/C`, `AIT_SCHLIEREN_SHOCK_ANGLE_801A/B/C`.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 500 µs cycle modeling: Compressible 1D Euler gas dynamics with real-gas equilibrium chemistry (isentropic expansion, Mach-Reynolds-Prandtl number coupling), regenerative ceramic pebble heat transfer (Schumann model), nozzle throat cryo boiling heat transfer, and vacuum diffuser supersonic unstart shockwave propagation.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional (J = \\sum (x-r)^T Q (x-r) + u^T R u + \\Delta u^T S \\Delta u) optimizing high-pressure supply throttle valve profile, LN2 nozzle jacket coolant flow, and diffuser bypass ejector flow to maintain stable Mach 7 test conditions without nozzle throat thermal yield or flow breakdown.
3. 2oo3 Triple Modular Redundancy (TMR):
   - Stagnation pressure piezo-resistive transducers (2oo3 voting with 0.8 bar discrepancy threshold).
   - Test cabin supersonic static wall pressure sensors (2oo3 voting with 0.02 bar threshold).
   - Discrepancy timers, bumpless degradation.
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with hypersonic tunnel unstart fast-trip protection (< 5 ms trigger).
5. Multi-Stage FSM:
   - 12-state state machine: `STANDBY_FACILITY_MONITOR`, `PEBBLE_BED_ELECTRIC_PREHEAT`, `CRYOGENIC_NOZZLE_CHILLDOWN`, `VACUUM_SPHERE_PUMPDOWN`, `ISOLATION_VALVE_FAST_OPEN`, `MACH_7_BLOWDOWN_STEADY_RUN`, `DYNAMIC_PITCH_AOA_SWEEP`, `NOZZLE_THERMAL_SURGE_REGULATION`, `TUNNEL_UNSTART_ABORT_TRIP`, `NORMAL_BLOWDOWN_TERMINATION`, `PURGE_AND_COOLING_FLUSH`, `EMERGENCY_DEPRESSURIZATION`.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Code length MUST be 50,000 to 85,000+ characters of industrial Structured Text.
"""

def main():
    print("Generating Structured Text for FB_Aerospace_HypersonicTunnel_CryoAir_PebbleHeater...")
    st_code = generate_aerospace_dataset.generate_iec_code()
    print(f"Generated Structured Text character length: {len(st_code)}")

    # Format assistant content
    assistant_content = f"```iec-st\n{st_code}```"
    print(f"Total assistant message length: {len(assistant_content)}")

    record = {
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_path = f"data/swarm_raw/agent_{agent_id}.json"

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset file to: {output_path}")

    # Validate JSON
    errs = validate_iec.validate_json_file(output_path)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        return False
    else:
        print(">>> SUCCESS: ALL VALIDATION AUDITS PASSED PERFECTLY! <<<")
        print(f"Agent ID: agent_{agent_id}")
        print(f"File: {output_path}")
        print(f"File Size: {os.path.getsize(output_path)} bytes")
        print(f"Total Assistant Content Chars: {len(assistant_content)}")
        return True

if __name__ == "__main__":
    main()
