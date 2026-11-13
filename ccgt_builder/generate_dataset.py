# ccgt_builder/generate_dataset.py
import sys
import os
import json
import uuid

# Add current folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import st_header_io
import st_var
import st_matrices
import st_phase1_tmr
import st_phase2_thermo_state_space
import st_phase3_mpc
import st_phase4_fsm
import st_phase5_alarms_telemetry

def generate():
    parts = [
        st_header_io.get_header_and_io(),
        st_var.get_var_declarations(),
        st_matrices.get_matrices_init(),
        st_phase1_tmr.get_phase1_tmr(),
        st_phase2_thermo_state_space.get_phase2_thermo_state_space(),
        st_phase3_mpc.get_phase3_mpc(),
        st_phase4_fsm.get_phase4_fsm(),
        st_phase5_alarms_telemetry.get_phase5_alarms_telemetry()
    ]
    st_code = "\n".join(parts)
    
    # Prompt text
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Industrial Power Generation & Thermal Turbomachinery (Combined Cycle Gas Turbine - CCGT Coordinated Load Governor, HRSG High-Pressure Drum Level & Multi-Stage Attemperator Steam Temperature Control)
FUNCTION BLOCK NAME: FB_Power_CCGT_GasTurbine_HRSG_Attemperator_Coordinated

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 20 ms):
   - 8-State model covering gas turbine compressor air flow (variable guide vanes VGV), combustor exhaust gas temperature (EGT / TIT), high-pressure evaporator drum mass balance & void fraction swell, 3-element feedwater dynamics, secondary superheater steam enthalpy, and attemperator spray valve thermal quench response:
     States: x1=Gas Turbine Electrical Power Output [MW], x2=Combustor Exhaust Gas Temperature (EGT) [degC], x3=Compressor Variable Guide Vane (VGV) Position [deg], x4=HRSG High-Pressure Drum Narrow-Range Level [mm], x5=HP Steam Mass Flow Rate [kg/s], x6=Final Superheater Main Steam Temperature [degC], x7=Attemperator Spray Desuperheater Inter-Stage Temperature [degC], x8=Boiler Feedwater Regulating Valve Position [%].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic Coordinated Turbine-Boiler Decoupling: adjusting gas turbine power dynamically changes exhaust waste heat into the HRSG, causing severe thermal lag and drum level swell before steam production stabilizes. MPC coordinates fuel gas valves, VGVs, boiler feedwater valve, and attemperator spray valve simultaneously.
   - Actuator constraints: Main fuel gas control valve [0..100%], VGV position [0..85 deg], boiler feedwater control valve [0..100%], superheater attemperator spray valve [0..100%], high-pressure steam bypass valve to condenser [0..100%], duct burner fuel valve [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Exhaust Gas Thermocouple Rakes (TT_EGT_101A/B/C) [degC]
     * HRSG High-Pressure Drum Narrow-Range Level Transmitters (LT_DRUM_201A/B/C) [mm]
     * Main Steam Exit Temperature Sensors (TT_STEAM_301A/B/C) [degC]
     * High-Pressure Steam Coriolis Mass Flowmeters (FT_STEAM_401A/B/C) [kg/s]
     * Generator Active Power Transducers (WT_POWER_501A/B/C) [MW]
   - Discrepancy accumulation timers (threshold 200 ms) and bumpless degradation.

4. Deterministic 14-Stage Power Plant State Machine (FSM):
   - CASE eState OF:
     0: TURBINE_ISOLATION_AND_PURGE_CYCLE
     1: ROTOR_BARRED_TURNING_GEAR_DISENGAGE
     2: CRANK_MOTOR_ACCELERATION_AND_IGNITION
     3: FLAME_DETECTION_AND_WARMUP_IDLE (1200 rpm)
     4: FULL_SPEED_NO_LOAD_3000RPM_ACCEL
     5: GENERATOR_52G_BREAKER_GRID_SYNC
     6: GAS_TURBINE_MINIMUM_STABLE_LOAD_RUN
     7: DLN_PREMIX_COMBUSTION_MODE_TRANSFER
     8: HRSG_HEAT_ACCUMULATION_AND_DRUM_SWELL_LOCK
     9: STEAM_TURBINE_ADMISSION_AND_COORDINATED_MPC
     10: DUCT_BURNER_PEAKING_FIRE_BOOST
     11: RAPID_GRID_FREQUENCY_PRIMARY_RESPONSE
     12: CONTROLLED_COOLDOWN_AND_TURNDOWN
     13: EMERGENCY_TRIP_MASTER_FUEL_TRIP_MFT
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Drum Dryout SIL-3 Interlock & 32-Bit Telemetry:
   - Drum Low-Low Level (< -250 mm) or High-High Level (> +200 mm) fast MFT trip (<25 ms).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Power_CCGT_GasTurbine_HRSG_Attemperator_Coordinated`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    code_content = f"```iec-st\n{st_code}\n```"

    record = {
        "instruction": prompt,
        "input": "",
        "output": code_content,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{agent_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Generated dataset successfully saved to: {output_filename}")
    print(f"Assistant content character count: {len(code_content)}")
    print(f"Structured Text character count: {len(st_code)}")
    return output_filename

if __name__ == "__main__":
    generate()
