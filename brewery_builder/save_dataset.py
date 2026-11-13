# brewery_builder/save_dataset.py
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
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Food & Beverage / Industrial Brewery Processing
Function Block Name: FB_FoodBev_Brewery_LauterTun_WortRake_MashBoil

System Scope:
Automated Commercial Brewhouse (500 bbl/brew) Lauter Tun Differential Pressure, Wort Rake Cutting Height & Variable Speed Drive, Vorlauf Recirculation Turbidity Control, Continuous Wort Kettle Boiling with Internal Forced-Circulation Calandria, and Whirlpool Trub Separation.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Grain bed differential pressure Delta P [mbar]
   - Wort clarity/turbidity [EBC/NTU]
   - Runoff flow rate [hL/h]
   - Calandria thermal jacket heat transfer & boiling temperature [deg C]
   - Evaporation rate [%/h] and volatile DMS (dimethyl sulfide) stripping concentration [ppb]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing rake height [mm], rake rotational speed [RPM], wort runoff control valve [%], calandria steam pressure [bar], and wort recirculation [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Lauter tun grain bed differential pressure sensors (DP_Sensors: 1, 2, 3) [mbar]
   - Runoff turbidity optical sensors (Turb_Sensors: 1, 2, 3) [EBC]
   - Wort kettle temperature sensors (Temp_Sensors: 1, 2, 3) [deg C]
   - Kettle level radar transmitters (Level_Sensors: 1, 2, 3) [%]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_PREFILL_FOUNDATION_WATER
   - 2: STATE_MASH_TRANSFER_INFLOW
   - 3: STATE_REST_GRAIN_BED_SETTLING
   - 4: STATE_VORLAUF_RECIRCULATION
   - 5: STATE_FIRST_WORT_RUNOFF_OPTIMIZATION
   - 6: STATE_SPARGING_HOT_WATER_DISTRIBUTION
   - 7: STATE_RAKE_DEEP_CUTTING_SEQUENCE
   - 8: STATE_SWEET_WATER_RUNOFF_CUTOFF
   - 9: STATE_SPENT_GRAIN_EVACUATION
   - 10: STATE_KETTLE_HEATING_CALANDRIA
   - 11: STATE_VIGOROUS_BOIL_EVAPORATION
   - 12: STATE_WHIRLPOOL_TANGENTIAL_INLET_REST
   - 13: STATE_CIP_CAUSTIC_SANITIZATION
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    p1 = part1_header_io.get_part1()
    p2 = part2_var_declarations.get_part2()
    p3 = part3_phase0_init.get_part3()
    p4 = part4_phase1_tmr.get_part4()
    p5 = part5_phase2_state_space.get_part5()
    p6 = part6_phase3_mpc.get_part6()
    p7 = part7_phase4_fsm.get_part7()
    p8 = part8_phase5_alarms.get_part8()

    full_code = "\n".join([p1, p2, p3, p4, p5, p6, p7, p8])

    code_payload = f"```iec-st\n{full_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_payload}
        ]
    }

    # Generate isolated file
    file_id = uuid.uuid4().hex[:8]
    filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{file_id}.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Successfully generated and saved dataset to: {filename}")
    print(f"Character count: {len(code_payload)}")

    # Run validation
    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED ON JSON FILE:")
        for e in errs:
            print("  -", e)
        sys.exit(1)
    else:
        print(f"ALL JSON VALIDATION CHECKS PASSED PERFECTLY FOR agent_{file_id}.json!")
        return filename, file_id, len(code_payload)

if __name__ == "__main__":
    build_dataset()
