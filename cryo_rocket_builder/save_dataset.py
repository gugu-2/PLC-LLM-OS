# cryo_rocket_builder/save_dataset.py

import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phase1_tmr
import build_st_phase2_thermo_state_space
import build_st_phase3_mpc
import build_st_phase4_fsm
import build_st_phase5_alarms
import validate_iec

def build_dataset():
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Aerospace & Defense / Liquid Rocket Propulsion Cryogenic Test Stand
Function Block Name: FB_Aerospace_Propulsion_CryogenicRocket_Turbopump_TestStand

System Scope:
Liquid Rocket Engine (LRE) High-Pressure Cryogenic Test Stand (Liquid Oxygen LOX at 90 K and Liquid Methane LCH4 at 112 K, feed header pressures up to 300 bar, main chamber thrust 1,500 kN). Coordinated line chilldown thermal transient management, cavitating venturi propellant mass flow metering, turbopump hydraulic cavitation suppression, LOX injector dome purge nitrogen blanket, high-frequency combustion chamber acoustic dynamic pressure monitoring, and sub-10 ms emergency abort hydraulic slam-shut interlocks.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - LOX feedline downstream pressure P_lox [bar] and cryo fluid temperature T_lox [K]
   - LCH4 feedline downstream pressure P_ch4 [bar] and cryo fluid temperature T_ch4 [K]
   - Propellant mixture mass ratio O/F [ratio] and cavitating venturi mass flow [kg/s]
   - Turbopump suction Net Positive Suction Margin (NPSM) [m] and acoustic cavitation index
   - Thrust chamber combustion pressure P_c [bar] and high-frequency combustion roughness [bar RMS]
   - Run tank ullage pressurization helium gaseous mass inventory [kg]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing electro-hydraulic LOX cavitating venturi pintle servo [%], LCH4 venturi pintle servo [%], gaseous helium ullage dome regulator [%], cryogenic chilldown bleed valves [%], and turbopump pre-burner bypass throttle [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - LOX feed manifold cryogenic pressure transmitters (LOX_Press: 1, 2, 3) [bar]
   - LCH4 feed manifold cryogenic pressure transmitters (CH4_Press: 1, 2, 3) [bar]
   - Thrust chamber static pressure transducers (Chamber_Press: 1, 2, 3) [bar]
   - Thrust load cell hexapod measurement array (Thrust_Sensors: 1, 2, 3) [kN]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_RUN_TANK_HELIUM_INERT_PURGE_AND_LEAK_CHECK
   - 2: STATE_LINE_CHILLDOWN_AND_TWO_PHASE_BOILOFF_BLEED
   - 3: STATE_STEADY_STATE_CRYOGENIC_TEMPERATURE_LOCK
   - 4: STATE_ULLAGE_PRESSURIZATION_RAMP_300BAR
   - 5: STATE_MAIN_VALVE_TIMING_AND_TORCH_IGNITER_LIGHTOFF
   - 6: STATE_CHAMBER_BOOTSTRAP_AND_LOW_PRESSURE_RUN
   - 7: STATE_FULL_RATED_THRUST_MPC_PROPELLANT_RATIO_RUN
   - 8: STATE_DYNAMIC_THROTTLING_SWEEP_PROFILE
   - 9: STATE_COMBUSTION_ACOUSTIC_RESONANCE_EVALUATION
   - 10: STATE_CONTROLLED_STEPPED_HOT_FIRE_SHUTDOWN
   - 11: STATE_POST_FIRING_GASEOUS_NITROGEN_CHAMBER_PURGE
   - 12: STATE_RUN_TANK_SAFE_VENT_AND_DEPRESSURIZATION
   - 13: STATE_EMERGENCY_COMBUSTION_UNSTABLE_FAST_ABORT_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    st_sections = [
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_block(),
        build_st_matrices.get_matrices_init(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_thermo_state_space.get_phase2_thermo_state_space(),
        build_st_phase3_mpc.get_phase3_mpc(),
        build_st_phase4_fsm.get_phase4_fsm(),
        build_st_phase5_alarms.get_phase5_alarms(),
        "END_FUNCTION_BLOCK"
    ]
    full_code = "\n\n".join(st_sections)
    asst_content = f"```iec-st\n{full_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }

    raw_dir = os.path.join(workspace_dir, "data", "swarm_raw")
    os.makedirs(raw_dir, exist_ok=True)
    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(raw_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset to {filename}")
    print(f"Total assistant content characters: {len(asst_content)}")

    # Validate generated JSON file
    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION ERRORS FOUND:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"ALL JSON VALIDATION CHECKS PASSED PERFECTLY FOR agent_{agent_id}.json!")
        return filename, agent_id, len(asst_content)

if __name__ == "__main__":
    build_dataset()
