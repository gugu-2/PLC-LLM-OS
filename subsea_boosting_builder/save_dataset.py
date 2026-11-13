# subsea_boosting_builder/save_dataset.py
import json
import uuid
import os
import subprocess
from subsea_boosting_builder.st_header_and_io import get_header_and_io
from subsea_boosting_builder.st_var_declarations import get_var_declarations
from subsea_boosting_builder.st_phase1_tmr import get_phase1_tmr
from subsea_boosting_builder.st_phase2_thermo_observers import get_phase2_observers
from subsea_boosting_builder.st_phase3_mpc import get_phase3_mpc
from subsea_boosting_builder.st_phase4_fsm import get_phase4_fsm
from subsea_boosting_builder.st_phase5_alarms import get_phase5_alarms

def main():
    parts = [
        get_header_and_io().strip(),
        get_var_declarations().strip(),
        get_phase1_tmr().strip(),
        get_phase2_observers().strip(),
        get_phase3_mpc().strip(),
        get_phase4_fsm().strip(),
        get_phase5_alarms().strip()
    ]

    st_code = '\n\n'.join(parts)
    
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Energy & Offshore Petrochemical / Subsea 3,000-Meter Multiphase Boosting & Anti-Surge
Function Block Name: FB_OilGas_Subsea_MultiphaseTwinScrew_Boosting_AntiSurge

System Scope:
Deepwater Subsea Multiphase Boosting Station (3,000-meter water depth, dual 4.5 MW variable-speed twin-screw helico-axial pumps). Severe dynamic multiphase slug flow mitigation (Gas Volume Fraction GVF from 10% to 98%), subsea pressurized barrier fluid seal closed loop (350 bar differential over seabed ambient), dynamic mono-ethylene glycol (MEG) thermodynamic hydrate inhibitor injection, pump thermal differential growth compensation, and high-speed subsea hydraulic anti-surge kickback recycle valve (<1.2 s stroke).

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Suction header dynamic pressure P_suction [bar] and discharge pressure P_discharge [bar]
   - Multiphase mixture Gas Volume Fraction (GVF) [%] and mixture acoustic speed [m/s]
   - Twin-screw differential pressure Delta_P [bar] and pump hydraulic absorbed torque [kNm]
   - Pressurized barrier fluid seal differential pressure Delta_P_seal [bar] and leak rate [mL/min]
   - Subsea pump casing & screw thermal differential expansion [um]
   - Multiphase flow slug mass acceleration & acoustic vibration RMS [m/s2]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing subsea VFD motor speed [RPM], hydraulic anti-surge kickback recycle valve [%], high-pressure MEG inhibitor metering valve [%], barrier fluid accumulator charge valve [%], and production choke trim [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Subsea suction manifold quartz pressure transmitters (Suction_Press: 1, 2, 3) [bar]
   - Subsea discharge manifold quartz pressure transmitters (Discharge_Press: 1, 2, 3) [bar]
   - Gamma-ray multiphase inline water-liquid-gas fraction meters (GVF_Sensors: 1, 2, 3) [%]
   - Barrier fluid seal differential pressure transmitters (Seal_DP: 1, 2, 3) [bar]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_BARRIER_FLUID_SEAL_PRESSURIZATION_LOCK
   - 2: STATE_MEG_HYDRATE_INHIBITOR_PRIME_FLUSH
   - 3: STATE_ANTI_SURGE_KICKBACK_VALVE_FULL_OPEN_UNLOAD
   - 4: STATE_SUBSEA_VFD_MOTOR_SPINUP_AND_LUBE_CHECK
   - 5: STATE_MINIMUM_STABLE_FLOW_CIRCULATION_RUN
   - 6: STATE_CONTROLLED_KICKBACK_VALVE_CLOSING_RAMP
   - 7: STATE_NOMINAL_MULTIPHASE_BOOSTING_MPC_RUN
   - 8: STATE_GAS_SLUG_ATTENUATION_AND_SPEED_SURGE_CUT
   - 9: STATE_THERMAL_EXPANSION_CLEARANCE_BALANCING
   - 10: STATE_HIGH_GVF_MIST_COOLING_LIQUID_RECYCLE
   - 11: STATE_CONTROLLED_WELLHEAD_TURNDOWN_AND_FLUSH
   - 12: STATE_SAFE_DEPRESSURIZATION_AND_INERT_SEAL_HOLD
   - 13: STATE_EMERGENCY_SUBSEA_SEAL_LOSS_OR_SURGE_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    assistant_content = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    file_id = uuid.uuid4().hex[:8]
    output_path = f"data/swarm_raw/agent_{file_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Generated dataset file: {output_path}")
    print(f"Assistant content character count: {len(assistant_content)}")
    print(f"Pure ST code character count: {len(st_code)}")
    
    # Run validation
    cmd = ["python", "validate_iec.py", output_path]
    result = subprocess.run(cmd, capture_output=True, text=True)
    print("\nValidator output:")
    print(result.stdout)
    if result.stderr:
        print("Validator errors:")
        print(result.stderr)
        
    if result.returncode == 0:
        print(f"\nSUCCESS: Dataset {output_path} is 100% valid!")
        return output_path, len(assistant_content), True
    else:
        print(f"\nFAILURE: Validation failed with return code {result.returncode}")
        return output_path, len(assistant_content), False

if __name__ == "__main__":
    main()
