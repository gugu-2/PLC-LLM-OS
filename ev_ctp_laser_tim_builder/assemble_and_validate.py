# ev_ctp_laser_tim_builder/assemble_and_validate.py
import os
import sys
import json
import uuid
import re

cur_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.abspath(os.path.join(cur_dir, ".."))
if cur_dir not in sys.path:
    sys.path.insert(0, cur_dir)
if parent_dir not in sys.path:
    sys.path.append(parent_dir)

from section_header import build_iec_code
from section_io_var import get_io_and_var
from section_phase0_init import get_phase0_code
from section_phase1_tmr import get_phase1_code
from section_phase2_observer import get_phase2_code
from section_phase3_mpc import get_phase3_code
from section_phase4_fsm import get_phase4_code
from section_phase5_alarms import get_phase5_code
import validate_iec

def assemble_code():
    parts = [
        build_iec_code(),
        get_io_and_var(),
        get_phase0_code(),
        get_phase1_code(),
        get_phase2_code(),
        get_phase3_code(),
        get_phase4_code(),
        get_phase5_code()
    ]
    return "\n".join(parts)

def main():
    agent_uid = uuid.uuid4().hex[:8]
    json_filename = f"agent_{agent_uid}.json"
    target_path = os.path.join(parent_dir, "data", "swarm_raw", json_filename)

    user_prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Automotive & Electric Vehicle (EV) Manufacturing / Cell-to-Pack (CTP) Laser Busbar Welding & TIM Dispensing
Function Block Name: FB_Automotive_EV_BatteryPack_LaserBusbar_ThermalDispensing_Coordinated

System Scope:
High-Throughput Electric Vehicle Cell-to-Pack (CTP) Battery Pack Assembly Cell (800 V architecture, 100 kWh battery pack, prismatic LFP/NMC cells). Coordinated high-speed 3D galvo scanner laser busbar welding (6 kW single-mode fiber laser, copper-to-aluminum intermetallic suppression, in-situ keyhole optical coherence tomography OCT depth tracking), two-component (2K) high-viscosity structural polyurethane thermal interface material (TIM) dispensing, dynamic hose compliance lead-lag flow compensation, and non-contact IR thermography weld defect inspection.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Laser weld keyhole depth dynamic deviation Delta_Z [um] and melt pool temperature T_melt [deg C]
   - Galvo scanner trajectory tracking speed v_weld [mm/s] and laser power P_laser [kW]
   - 2K TIM dynamic metering chamber pressure P_tim [bar] and dispense volumetric flow rate [mL/s]
   - TIM dispensing bead cross-sectional width [mm] and height profile [mm]
   - Battery module cell-tab geo-clamping pneumatic contact force F_clamp [N]
   - Battery cell terminal dynamic electrical resistance R_joint [uOhm]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing laser power modulation [%], 3D galvo scan mirror velocities X/Y [%], 2K servo gear pump speed trims A & B [RPM], dynamic dispense tip snort valve [%], and pneumatic geo-clamping pressure regulator [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - In-situ weld keyhole OCT interferometric depth sensors (OCT_Depth: 1, 2, 3) [um]
   - 2K TIM manifold pressure transducers (TIM_Press: 1, 2, 3) [bar]
   - Pneumatic module geo-clamp load cells (Clamp_Force: 1, 2, 3) [N]
   - Infrared pyrometers measuring molten keyhole radiation (Pyrometer: 1, 2, 3) [deg C]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_PACK_TRAY_DOCKING_AND_RFID_RECIPE_VERIFY
   - 2: STATE_TIM_NOZZLE_AUTOMATIC_PURGE_AND_SCALE_SHOT
   - 3: STATE_ROBOTIC_2K_TIM_STRUCTURAL_BEAD_DISPENSE_RUN
   - 4: STATE_OPTICAL_LASER_TRIANGULATION_TIM_BEAD_INSPECT
   - 5: STATE_CELL_MODULE_INSERTION_AND_PRESS_DOWN
   - 6: STATE_GEO_CLAMPING_TOOL_PNEUMATIC_ENGAGE_AND_LOCK
   - 7: STATE_3D_VISION_BUSBAR_TAB_DATUM_POINT_OFFSET_SCAN
   - 8: STATE_HIGH_SPEED_GALVO_LASER_BUSBAR_WELD_CYCLE
   - 9: STATE_IN_SITU_OCT_WELD_PENETRATION_DEPTH_EVAL
   - 10: STATE_POST_WELD_IR_THERMOGRAPHY_COOLING_INSPECT
   - 11: STATE_CLAMPING_TOOL_DEPRESSURIZE_AND_RETRACT
   - 12: STATE_ELECTRICAL_4WIRE_MILLIOHM_CONTINUITY_CHECK
   - 13: STATE_EMERGENCY_LASER_SHUTTER_DROP_OR_PRESSURE_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    st_code = assemble_code()
    print(f"Generated Structured Text length: {len(st_code)} characters")
    print(f"Generated Structured Text lines: {len(st_code.splitlines())}")

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ]
    }

    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {target_path}")

    # Validate JSON file with validate_iec
    errs = validate_iec.validate_json_file(target_path)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        print(f"UUID: {agent_uid}")
        print(f"File: {target_path}")

if __name__ == "__main__":
    main()
