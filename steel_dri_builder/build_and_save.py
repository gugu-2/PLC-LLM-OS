# steel_dri_builder/build_and_save.py
import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import part1_header_io
import part2_var_declarations
import part3_phase0_init
import part4_phase1_tmr
import part5_phase2_state_space
import part6_phase3_mpc
import part7_phase4_fsm
import part8_phase5_alarms
import validate_iec

def main():
    user_prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Primary Metallurgy & Sustainable Steelmaking (Direct Reduced Iron - DRI Shaft Reduction Furnace, Green Hydrogen & Syngas Metallization Kinetics & Burden Descent Control)
FUNCTION BLOCK NAME: FB_Steel_DRI_ShaftFurnace_HydrogenSyngas_Reduction

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 25 ms):
   - 8-State model of gas-solid iron ore reduction kinetics (Fe2O3 -> Fe3O4 -> FeO -> Fe), bustle reduction gas thermal dynamics (950 degC), shaft burden descending velocity, top gas recycling equilibrium, methane reforming / carbon deposition, and cooling cone gas exchange:
     States: x1=Bustle Reduction Gas Inlet Temperature [degC], x2=Mid-Shaft Reduction Zone Metallization Degree [% Fe], x3=Shaft Upper-to-Lower Differential Pressure [kPa], x4=Top Gas H2/CO Molar Ratio [ratio], x5=Top Gas CO2 Concentration [% vol], x6=Discharged DRI Carbon Content [wt% C], x7=Cooling Zone Bottom Gas Discharge Temperature [degC], x8=Discharge Screw Feeder Linear Mass Extraction Rate [t/h].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic Hydrogen / Syngas Gas Mix Decoupling: coordinated control of green Hydrogen injection valve, reformed syngas heater valve, natural gas carbon trim injection, and discharge feeder speed to hold metallization > 94.5% while preventing burden clustering / sticking.
   - Actuator constraints: Green Hydrogen feed valve [0..100%], reformed syngas main valve [0..100%], process gas heater fuel modulation [0..100%], natural gas enrichment injection [0..100%], cooling gas recycle blower VFD [0..100%], bottom rotary discharge feeder speed [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Bustle Pipe Thermocouple Rings (TT_BUSTLE_101A/B/C) [degC]
     * Shaft Differential Pressure Transmitters (PDT_SHAFT_201A/B/C) [kPa]
     * In-line Laser / Mass Spectrometer Gas Analyzers (AT_GAS_301A/B/C) [% H2/CO]
     * Radar Burden Level Surface Profilers (LT_BURDEN_401A/B/C) [m]
     * Discharged DRI Product Optical Pyrometers (TT_DRI_501A/B/C) [degC]
   - Discrepancy accumulation timers (threshold 250 ms) and bumpless degradation.

4. Deterministic 14-Stage Steelmaking State Machine (FSM):
   - CASE eState OF:
     0: FURNACE_COLD_NITROGEN_INERT_STANDBY
     1: PROCESS_GAS_HEATER_WARMUP_RAMP (to 950 degC)
     2: REDUCING_GAS_INJECTION_AND_HEAVY_PURGE
     3: IRON_ORE_PELLET_GRAVITY_CHARGING_INIT
     4: THERMAL_EQUILIBRIUM_AND_BED_HEATING
     5: GREEN_HYDROGEN_ENRICHMENT_RAMPUP (to 70% H2)
     6: FULL_METALLIZATION_OPTIMAL_MPC_RUN (>94% Fe)
     7: PRODUCT_CARBON_CONTROL_ENRICHMENT
     8: BOTTOM_COOLING_GAS_RECYCLE_LOCK
     9: HOT_DRI_CONTINUOUS_PNEUMATIC_DISCHARGE
     10: BURDEN_STICKING_CHUNKING_VIBRATION_PULSE
     11: PROCESS_GAS_TURNDOWN_RECYCLE_HOLD
     12: EMERGENCY_NITROGEN_SNORT_DUMP (<50 ms)
     13: SIL-3_DOUBLE_BLOCK_BLEED_GAS_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Oxygen Ingress / Deflagration SIL-3 Interlock & 32-Bit Telemetry:
   - Oxygen ingress detection in hydrogen reduction loop (<20 ms double-block-and-bleed).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Steel_DRI_ShaftFurnace_HydrogenSyngas_Reduction`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    st_code = "\n".join([
        part1_header_io.get_header_and_io().strip(),
        part2_var_declarations.get_var_declarations().strip(),
        part3_phase0_init.get_phase0_init().strip(),
        part4_phase1_tmr.get_phase1_tmr().strip(),
        part5_phase2_state_space.get_phase2_state_space().strip(),
        part6_phase3_mpc.get_phase3_mpc().strip(),
        part7_phase4_fsm.get_phase4_fsm().strip(),
        part8_phase5_alarms.get_phase5_alarms().strip()
    ])

    assistant_content = f"```iec-st\n{st_code}\n```"
    total_chars = len(assistant_content)
    print(f"Generated IEC ST assistant content length: {total_chars} characters")

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    raw_dir = os.path.join(workspace_dir, "data", "swarm_raw")
    os.makedirs(raw_dir, exist_ok=True)
    file_id = uuid.uuid4().hex[:8]
    output_filename = f"agent_{file_id}.json"
    output_path = os.path.join(raw_dir, output_filename)

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset record to {output_path}")

    # Validate output
    errors = validate_iec.validate_json_file(output_path)
    if errors:
        print("VALIDATION FAILED with errors:")
        for err in errors:
            print(" -", err)
        sys.exit(1)
    else:
        print(f"SUCCESS: {output_filename} passed all IEC validation checks with 0 errors!")
        return output_filename, total_chars

if __name__ == "__main__":
    main()
