# mine_vod_fan_builder/generate_dataset.py
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
import st_phase2_cyber_physical
import st_phase3_state_space
import st_phase4_mpc
import st_phase5_fsm
import st_phase6_alarms_telemetry

def generate():
    parts = [
        st_header_io.get_header_and_io(),
        st_var.get_var_declarations(),
        st_matrices.get_matrices_init(),
        st_phase1_tmr.get_phase1_tmr(),
        st_phase2_cyber_physical.get_phase2_cyber_physical(),
        st_phase3_state_space.get_phase3_state_space(),
        st_phase4_mpc.get_phase4_mpc(),
        st_phase5_fsm.get_phase5_fsm(),
        st_phase6_alarms_telemetry.get_phase6_alarms_telemetry()
    ]
    st_code = "\n".join(parts)
    
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Mining & Subsurface Extraction / Underground Mine Ventilation on Demand (VOD) & Main Fan Anti-Stall
Function Block Name: FB_Mining_VentilationOnDemand_MainMineFan_AntiStall_ToxicGas

System Scope:
Underground Deep Metal Mine Automated Ventilation on Demand (VOD) and Surface Main Fan Substation (shaft depth 2,400 meters, dual 3.5 MW variable-pitch axial main surface exhaust fans, 24 automated underground branch louvers/air doors). Real-time aerodynamic fan stall margin tracking (operating point distance to rotating stall boundary on pressure-volume characteristic), dynamic toxic gas dispersion clearance (CO, NO2, diesel particulate matter DPM, and post-blast blasting fume clearance), subterranean barometric air density scaling, and underground intake airway fire smoke reversal prevention.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Surface main fan static pressure rise Delta_P [kPa] and total airway mass flow Q_mass [kg/s]
   - Aerodynamic stall margin index SM [%] and dynamic pressure blade tip turbulence [Pa RMS]
   - Underground work-heading toxic gas concentrations [ppm CO / NO2] and DPM soot loading [ug/m3]
   - Subterranean airway shaft differential barometric pressure [kPa]
   - Surface fan blade hydraulic pitch angle [deg] and variable speed motor torque [kNm]
   - Airway acoustic airflow velocity [m/s] and mine thermal wet-bulb globe temperature (WBGT) [deg C]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing surface fan variable frequency drive (VFD) RPM, hydraulic blade pitch servo angle [%], underground active louver damper angles 1..24 [%], auxiliary booster fan speeds [%], and heating/chilling intake coil valves [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Main fan intake differential pressure transmitters (Fan_DP: 1, 2, 3) [kPa]
   - Ultrasonic multi-path airway velocity flowmeters (Air_Vel: 1, 2, 3) [m/s]
   - Multi-gas electrochemical borehole telemetry sensors (Toxic_Gas: 1, 2, 3) [ppm CO]
   - Fan bearing triaxial seismic vibration velocity transducers (Fan_Vib: 1, 2, 3) [mm/s RMS]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_SURFACE_FAN_LUBE_OIL_PRESSURE_LOCK
   - 2: STATE_HYDRAULIC_BLADE_PITCH_ZERO_RETURN
   - 3: STATE_SURFACE_MAIN_MOTOR_SOFT_START_SPINUP
   - 4: STATE_AERODYNAMIC_BLADE_PITCH_MINIMUM_LOAD_RAMP
   - 5: STATE_UNDERGROUND_LOUVER_INITIAL_CALIBRATION_SWEEP
   - 6: STATE_NOMINAL_VOD_CLOSED_LOOP_MPC_RUN
   - 7: STATE_POST_BLAST_CLEARANCE_MAXIMUM_AIRFLOW_PURGE
   - 8: STATE_HEAVY_DIESEL_HAULAGE_LOCAL_BOOST_MODE
   - 9: STATE_AERODYNAMIC_STALL_WARNING_PITCH_RELIEF
   - 10: STATE_AIRWAY_ICE_PREVENTION_INTAKE_COIL_HEAT
   - 11: STATE_CONTROLLED_AIRWAY_RAMPDOWN_AND_FLOAT
   - 12: STATE_SURFACE_FAN_STANDBY_COOLDOWN_PURGE
   - 13: STATE_EMERGENCY_UNDERGROUND_FIRE_SMOKE_ISOLATION_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

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

    raw_dir = os.path.join(os.path.dirname(current_dir), "data", "swarm_raw")
    os.makedirs(raw_dir, exist_ok=True)
    
    unique_id = uuid.uuid4().hex[:8]
    filename = os.path.join(raw_dir, f"agent_{unique_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"Generated dataset file: {filename}")
    print(f"Assistant code length: {len(code_content)} characters")
    return filename

if __name__ == "__main__":
    fn = generate()
