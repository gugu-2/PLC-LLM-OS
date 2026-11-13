# -*- coding: utf-8 -*-
"""
Module: aseptic_retort_builder/assemble.py
Assembles FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization,
validates syntax, delimiter parity, and character count with validate_iec.py,
and saves the validated synthetic record to data/swarm_raw/agent_<uuid>.json.
"""

import os
import json
import uuid
import subprocess
import sys

from aseptic_retort_builder.mod_header_io import generate_header_io
from aseptic_retort_builder.mod_var_decl import generate_var_decl
from aseptic_retort_builder.mod_matrices_init import generate_matrices_init
from aseptic_retort_builder.mod_tmr import generate_tmr
from aseptic_retort_builder.mod_cyberphysical import generate_cyberphysical
from aseptic_retort_builder.mod_mpc import generate_mpc
from aseptic_retort_builder.mod_fsm import generate_fsm
from aseptic_retort_builder.mod_alarms import generate_alarms

def assemble_code():
    parts = [
        generate_header_io(),
        generate_var_decl(),
        generate_matrices_init(),
        generate_tmr(),
        generate_cyberphysical(),
        generate_mpc(),
        generate_fsm(),
        generate_alarms()
    ]
    return '\n\n'.join(parts)

def main():
    st_code = assemble_code()
    char_count = len(st_code)
    line_count = len(st_code.splitlines())
    print(f"Total Structured Text character count: {char_count}")
    print(f"Total Structured Text line count: {line_count}")

    prompt_text = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Food & Beverage / Continuous Overpressure Industrial Retort Sterilization
Function Block Name: FB_FoodBev_Aseptic_ContinuousRetort_SteamAir_Sterilization

System Scope:
Commercial Continuous Overpressure Rotary Retort Autoclave (1,200 cans/min or pouches, 4.0 bar design pressure, 140 deg C). Real-time mathematical thermal death time lethality F0 value calculation (Arrhenius / Bigelow kinetics, z=10.0 deg C, T_ref=121.1 deg C for Clostridium botulinum inactivation, target F0 >= 6.0 min), dynamic steam-air mixture overpressure regulation to prevent flexible pouch rupture or can buckling (Delta_P < 0.12 bar), multi-zone cooling water cascade, and dynamic rotary drum speed regulation.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Retort chamber internal temperature T_retort [deg C] and container core temperature T_core [deg C]
   - Retort steam-air total pressure P_retort [bar] and container internal vapor pressure P_internal [bar]
   - Accumulated thermal lethality F0 value [min] and cook value C0 [min]
   - Compressed air overpressure ratio [%] and steam injection mass flow [kg/h]
   - Cooling water circulation flow rate [m3/h] and drain temperature [deg C]
   - Rotary drum rotational speed [RPM] and container transit dwell time [min]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing saturated steam modulating valve [%], compressed air overpressure injection valve [%], retort top exhaust vent valve [%], cooling water cascade injection valve [%], and rotary drum VFD speed [RPM].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Retort chamber dual-element Class A Pt100 RTDs (Temp_Sensors: 1, 2, 3) [deg C]
   - Retort shell piezoresistive pressure transmitters (Press_Sensors: 1, 2, 3) [bar]
   - Vessel condensate level differential pressure transmitters (Level_Sensors: 1, 2, 3) [mm]
   - Container internal pressure wireless telemetry transponders (Pouch_Press: 1, 2, 3) [bar]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_CHAMBER_LOAD_AND_SAFETY_DOOR_INTERLOCK_LOCK
   - 2: STATE_VENTING_AIR_DISPLACEMENT_STEAM_PURGE
   - 3: STATE_COME_UP_HEATING_RAMP_TO_121C
   - 4: STATE_STEAM_AIR_OVERPRESSURE_EQUILIBRIUM_LOCK
   - 5: STATE_NOMINAL_STERILIZATION_HOLD_LETHALITY_ACCUM
   - 6: STATE_TARGET_F0_REACHED_HEATING_CUTOFF
   - 7: STATE_PRESSURE_MAINTAINED_PRE_COOL_WATER_INJECTION
   - 8: STATE_FULL_IMMERSION_TEMPERED_COOLING_CASCADE
   - 9: STATE_FINAL_COLD_WATER_CHILLDOWN_TO_40C
   - 10: STATE_CONTROLLED_DEPRESSURIZATION_AND_DRAIN
   - 11: STATE_SAFETY_AIR_VENT_AND_DOOR_UNLATCH
   - 12: STATE_STERILE_CONTAINER_DISCHARGE_CONVEYOR_RUN
   - 13: STATE_EMERGENCY_OVERPRESSURE_OR_UNDERPROCESSING_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json'."""

    assistant_content = f"```iec-st\n{st_code}\n```"

    record_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{record_id}.json"

    data_payload = {
        "id": f"synthetic_foodbev_aseptic_continuous_retort_{record_id}",
        "instruction": prompt_text,
        "input": "",
        "output": assistant_content,
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated and saved dataset record to {output_filename}")

    # Validate with validate_iec.py
    val_cmd = [sys.executable, "validate_iec.py", output_filename]
    res = subprocess.run(val_cmd, capture_output=True, text=True)
    print("STDOUT:", res.stdout)
    if res.stderr:
        print("STDERR:", res.stderr)

    if res.returncode != 0:
        print(f"VALIDATION FAILED with exit code {res.returncode}")
        sys.exit(res.returncode)
    else:
        print(f"VALIDATION PASSED PERFECTLY (0 errors) for {output_filename}")
        with open("latest_agent_file.txt", "w", encoding="utf-8") as lf:
            lf.write(output_filename)

if __name__ == "__main__":
    main()
