# copper_flotation_gen/save_dataset.py
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

def build_dataset():
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Mining & Mineral Extraction / Hydrometallurgy (Industrial 12-Cell Copper Froth Flotation Bank Pulp Level, Air Flow & Froth Recovery Optimisation)
FUNCTION BLOCK NAME: FB_Mining_Copper_FrothFlotation_PulpLevel_AirRecovery

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 20 ms):
   - 8-State model of multi-cell slurry hydrodynamics, pulp-froth phase equilibrium, air holdup, superficial gas velocity (Jg), bubble surface area flux (Sb), xanthate collector dosing kinetics, and concentrate mass pull:
     States: x1=Rougher Cell 1 Pulp Level [mm], x2=Rougher Cell 6 Mid-Bank Pulp Level [mm], x3=Scavenger Cell 12 Tailings Pulp Level [mm], x4=Froth Bed Thickness / Overflow Lip Depth [mm], x5=Dispersed Air Holdup Volume Fraction [% vol], x6=Superficial Gas Velocity Jg [cm/s], x7=Copper Concentrate Grade [% Cu], x8=Cumulative Copper Recovery Efficiency [% Rec].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Non-linear dart valve coupling: moving upstream dart valves dynamically alters hydrostatic head in downstream cells (hydraulic cross-coupling matrix unrolling).
   - Actuator constraints: Dart valve positions 1 to 6 [0..100%], air flow control valves 1 to 6 [0..100%], collector reagent metering pump [0..100%], frother reagent metering pump [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Ultrasonic / Float Pulp Level Transmitters (LT_PULP_101A/B/C) [mm]
     * Visual / Piezoresistive Froth Height Transmitters (LT_FROTH_201A/B/C) [mm]
     * Forced Air Supply Orifice Differential Pressure (PDT_AIR_301A/B/C) [kPa]
     * In-stream X-Ray Fluorescence (XRF) Slurry Copper Grade Analyzers (AT_CU_401A/B/C) [% Cu]
     * Tailings Slurry Nuclear Density Gauges (DT_TAIL_501A/B/C) [g/cm3]
   - Discrepancy accumulation timers (threshold 400 ms) and bumpless degradation.

4. Deterministic 14-Stage Flotation State Machine (FSM):
   - CASE eState OF:
     0: FLOTATION_BANK_IDLE_STANDBY
     1: WATER_CALIBRATION_AND_DART_VALVE_ZEROING
     2: AIR_BLOWER_MANIFOLD_PRESSURIZATION
     3: ORE_SLURRY_FEED_INTRODUCTION (Target 35% Solids)
     4: COLLECTOR_FROTHER_REAGENT_CONDITIONING
     5: FROTH_BED_STABILIZATION_AND_LIP_OVERFLOW
     6: FULL_GRADE_RECOVERY_OPTIMAL_MPC_CONTROL
     7: HIGH_CLAY_GANGUE_ENTRAINMENT_WASHING
     8: MIDDLINGS_RECYCLE_STREAM_BALANCING
     9: FROTH_COLLAPSE_SURFACTANT_BOOST_RECOVERY
     10: FEED_SURGE_DART_VALVE_FAST_REGULATION
     11: TAILINGS_SANDER_UP_PREVENTION_FLUSH
     12: EMERGENCY_SLURRY_DRAIN_AND_DUMP
     13: MECHANICAL_AGITATOR_TORQUE_OVERLOAD_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Dart Valve Anti-Stiction & 32-Bit Telemetry:
   - Cell sanding / impeller torque overload early warning detection.
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Mining_Copper_FrothFlotation_PulpLevel_AirRecovery`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    st_code = (
        part1_header_io.get_header_and_io() + "\n" +
        part2_var_declarations.get_var_declarations() + "\n" +
        part3_phase0_init.get_phase0_init() + "\n" +
        part4_phase1_tmr.get_phase1_tmr() + "\n" +
        part5_phase2_state_space.get_phase2_state_space() + "\n" +
        part6_phase3_mpc.get_phase3_mpc() + "\n" +
        part7_phase4_fsm.get_phase4_fsm() + "\n" +
        part8_phase5_alarms.get_phase5_alarms()
    )

    asst_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{agent_id}.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset to {filename}")
    print(f"Assistant Content Character Count: {len(asst_content)}")
    print(f"Structured Text Line Count: {len(st_code.splitlines())}")

    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL IEC VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return filename, agent_id, len(asst_content), len(st_code.splitlines())

if __name__ == "__main__":
    build_dataset()
