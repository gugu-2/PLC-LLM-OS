# semiconductor_tcb_builder/save_dataset.py

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
import build_st_phase2_state_space
import build_st_phase3_mpc
import build_st_phase4_fsm
import build_st_phase5_actuators_thermal
import build_st_phase6_alarms_diagnostics
import validate_iec

def build_dataset():
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Semiconductor Manufacturing & Advanced Packaging / 3D Chiplet Thermo-Compression Bonding
Function Block Name: FB_Semiconductor_AdvancedPackaging_TCB_ThermalCompression_Bonding

System Scope:
Advanced 2.5D/3D Chiplet Heterogeneous Integration Thermo-Compression Bonder (TCB) for HBM (High Bandwidth Memory) and CoWoS packaging. Sub-micron multi-axis placement alignment (<0.5 um), dynamic 6-axis piezo-electric chuck leveling, ceramic pulse heater rapid thermal ramp (>250 deg C/s to 420 deg C peak), closed-loop bond head voice-coil/piezo force regulation (5 N to 450 N +/- 1.0 N), and formic acid (HCOOH) vapor deoxidation gas shroud atmosphere.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Dynamic bond force error & piezo load cell response [N]
   - Bond head Z-axis thermal expansion elongation [um]
   - Micro-bump solder collapse height & squeeze-out thickness [um]
   - Pulse heater substrate interface temperature [deg C]
   - Vacuum chuck holding differential pressure [kPa]
   - 6-Axis chuck co-planarity tilt error [urad]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing piezo micro-actuator displacement trim [um], voice coil linear motor current [A], ceramic pulse heater duty cycle [%], cooling nitrogen gas blast valve [%], and formic acid purge flow [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Multi-axis piezo quartz bond force sensors (Force_Sensors: 1, 2, 3) [N]
   - Ceramic heater ultra-fast thin-film thermocouples (Temp_Sensors: 1, 2, 3) [deg C]
   - Bond head optical linear glass scale encoders (Z_Pos_Sensors: 1, 2, 3) [um]
   - Chuck vacuum capacitance diaphragm gauges (Vac_Sensors: 1, 2, 3) [kPa]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_CHUCK_THERMAL_SOAK_AND_VACUUM_LOCK
   - 2: STATE_OPTICAL_FIDUCIAL_3D_COPLANARITY_ALIGN
   - 3: STATE_FORMIC_ACID_DEOXIDATION_PURGE
   - 4: STATE_CHIPLET_PICKUP_AND_FORCE_VERIFY
   - 5: STATE_FAST_APPROACH_TRAJECTORY_DECEL
   - 6: STATE_INITIAL_TOUCH_SOFT_LANDING_5N
   - 7: STATE_RAPID_THERMAL_PULSE_MELT_RAMP
   - 8: STATE_CONTROLLED_SOLDER_COLLAPSE_FORCE_HOLD
   - 9: STATE_SOLIDIFICATION_NITROGEN_CHILL_QUENCH
   - 10: STATE_VACUUM_RELEASE_AND_HEAD_LIFT_OFF
   - 11: STATE_POST_BOND_ACOUSTIC_POROSITY_CHECK
   - 12: STATE_COLD_INERT_PURGE_AND_PURGE_EXHAUST
   - 13: STATE_EMERGENCY_FORCE_OVERLOAD_OR_THERMAL_RUNAWAY_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_state_space.get_phase2_state_space(),
        build_st_phase3_mpc.get_phase3_mpc(),
        build_st_phase4_fsm.get_phase4_fsm(),
        build_st_phase5_actuators_thermal.get_phase5_actuators_thermal(),
        build_st_phase6_alarms_diagnostics.get_phase6_alarms_diagnostics()
    ])

    print("Verifying internal Structured Text code...")
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("INTERNAL IEC-ST VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print(f"Internal IEC-ST Validation passed with 0 errors! Code size: {len(st_code)} characters")

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "instruction": prompt,
        "input": "",
        "output": assistant_content,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{agent_id}.json")
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to {output_filename}")
    print(f"Total file size on disk: {os.path.getsize(output_filename)} bytes")
    print(f"Assistant content character count: {len(assistant_content)}")

    print(f"Executing external validation script on {output_filename}...")
    val_errs = validate_iec.validate_json_file(output_filename)
    if val_errs:
        print("EXTERNAL JSON VALIDATION FAILED:")
        for e in val_errs:
            print(" -", e)
        sys.exit(1)
    print("EXTERNAL JSON VALIDATION PASSED WITH 0 ERRORS!")
    return output_filename, len(assistant_content), agent_id

if __name__ == "__main__":
    fn, chars, aid = build_dataset()
    print(f"\nSUCCESS: Agent {aid} generated {chars} characters in {fn}")
