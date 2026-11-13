# pwr_sg_builder/generate_dataset.py
import sys
import os
import json
import uuid

# Add current folder to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.append(current_dir)

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phase1_tmr
import build_st_phase2_thermo_state_space
import build_st_phase3_mpc
import build_st_phase4_fsm
import build_st_phase5_alarms_telemetry

def generate():
    parts = [
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_init(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_thermo_state_space.get_phase2_thermo_state_space(),
        build_st_phase3_mpc.get_phase3_mpc(),
        build_st_phase4_fsm.get_phase4_fsm(),
        build_st_phase5_alarms_telemetry.get_phase5_alarms_telemetry()
    ]
    st_code = "\n".join(parts)
    
    # Prompt text
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Nuclear Power Generation & Safety-Critical Thermo-Hydraulics (PWR Pressurized Water Reactor Steam Generator Level Control)
FUNCTION BLOCK NAME: FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 25 ms):
   - Minimum 8-state model capturing steam generator thermo-hydraulics, non-minimum phase zero (reverse level swell on cold feedwater injection, shrink on steam load increase), thermal lag, downcomer recirculation, void fraction dynamics, and mass balance:
     States: x1=Narrow-Range Level [mm], x2=Downcomer Flow Rate [kg/s], x3=Boiling Riser Average Void Fraction [ratio 0..1], x4=Primary-to-Secondary Heat Transfer Rate [MW], x5=Steam Drum Pressure [bar], x6=Cold Leg Temperature [deg C], x7=Feedwater Valve Trim Position [%], x8=Steam Line Non-Minimum Phase Dynamic Lead/Lag State [mm].
   - Provide explicit, non-zero system matrices: A (8x8), B (8x5), C (5x8), D (5x5).
   - Write out state propagation explicitly: x[k+1] = A * x[k] + B * u[k].
   - Provide Kalman filter observer equations with gain matrix L (8x5).

2. Receding Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Horizon N = 5 steps, 5 iterations of unrolled projected gradient descent.
   - Dynamic inverse response compensation (cancelling non-minimum phase shrink/swell illusion using steam flow / feedwater flow feedforward ratio).
   - Quadratic cost function: Q state penalty matrix, R control effort penalty matrix, P terminal penalty matrix.
   - Actuator constraints: Feedwater regulating valve (MFRV) [0..100%], low-power bypass valve [0..100%], slew rate limits [5%/s].

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting for:
     * Steam Generator Narrow Range Level (LT_NR_101A, LT_NR_101B, LT_NR_101C) [mm]
     * Steam Generator Wide Range Level (LT_WR_102A, LT_WR_102B, LT_WR_102C) [mm]
     * Main Steam Drum Pressure (PT_MS_201A, PT_MS_201B, PT_MS_201C) [bar]
     * Main Steam Mass Flow Rate (FT_MS_301A, FT_MS_301B, FT_MS_301C) [t/h]
     * Main Feedwater Mass Flow Rate (FT_FW_401A, FT_FW_401B, FT_FW_401C) [t/h]
   - Discrepancy accumulation timers (threshold 500 ms) and bumpless degradation (3 healthy -> 2 healthy 1oo2 -> 1 healthy 1oo1 warning -> 0 healthy reactor trip/failsafe).

4. Deterministic 14-Stage Nuclear State Machine (FSM):
   - CASE eState OF:
     0: COLD_SHUTDOWN_HOT_STANDBY_TRANSFER
     1: STARTUP_LOW_POWER_BYPASS_CONTROL (<15% FP)
     2: MAIN_REGULATING_VALVE_TRANSFER_BUMPLESS
     3: AT_POWER_CASCADE_FEEDFORWARD_STABILIZED (15% - 50% FP)
     4: FULL_POWER_OPTIMAL_MPC_TRACKING (50% - 100% FP)
     5: RAPID_LOAD_REJECTION_TURBINE_RUNBACK (-5%/min)
     6: MAIN_STEAM_ISOLATION_VALVE_FAST_CLOSURE
     7: STEAM_GENERATOR_TUBE_RUPTURE_DIAGNOSTIC (SGTR leak rate radiation check)
     8: AUXILIARY_FEEDWATER_MOTOR_DRIVEN_START
     9: AUXILIARY_FEEDWATER_TURBINE_DRIVEN_AUTO_INIT
     10: DRY_OUT_PROTECTION_RAPID_COOLDOWN
     11: OVERFILL_PROTECTION_MAIN_FEEDWATER_ISOLATION
     12: REACTOR_PROTECTION_SYSTEM_SCRAM_OVERRIDE
     13: POST_SCRAM_DECAY_HEAT_THERMAL_EQUILIBRIUM
   - Fully implement every single state transition and logic.

5. ISA-18.2 Nuclear Class 1E Process Alarms & 32-Bit Telemetry:
   - HH (Reactor Trip SCRAM), H (Turbine Runback / Alert), L (Low Water Warning), LL (Aux Feedwater Auto-Start SCRAM).
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & LENGTH MANDATE
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Nuclear_PWR_SteamGenerator_NarrowRangeLevel_ShrinkSwell`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration, e.g. `rLevel_NR_A : REAL; (* Narrow Range Level Sensor A [mm] *)`.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    code_content = f"```iec-st\n{st_code}\n```"

    record = {
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
