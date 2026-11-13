# bof_converter_builder/assemble_bof_dataset.py
"""
Master Assembler for FB_Steel_BOF_Converter_DynamicLance_SublanceEndpoint_Offgas
Validates with validate_iec.py and writes JSON to data/swarm_raw/agent_<uuid>.json
"""

import sys
import os
import json
import uuid
import subprocess

from section_io_var import get_header_and_declarations
from section_phase0_init import get_phase0_code
from section_phase1_tmr import get_phase1_code
from section_phase2_observer import get_phase2_code
from section_phase3_mpc import get_phase3_code
from section_phase4_fsm import get_phase4_code
from section_phase5_alarms import get_phase5_code

def assemble():
    print("Assembling FB_Steel_BOF_Converter_DynamicLance_SublanceEndpoint_Offgas...")
    
    parts = [
        get_header_and_declarations(),
        get_phase0_code(),
        get_phase1_code(),
        get_phase2_code(),
        get_phase3_code(),
        get_phase4_code(),
        get_phase5_code()
    ]
    
    full_st_code = "\n".join(parts)
    print(f"Total Structured Text code length: {len(full_st_code)} characters")
    
    # Save standalone .st file for inspection
    st_filepath = "bof_converter_builder/FB_Steel_BOF_Converter.st"
    with open(st_filepath, "w", encoding="utf-8") as f:
        f.write(full_st_code)
    print(f"Saved standalone ST to {st_filepath}")
    
    # Format assistant message
    assistant_content = f"```iec-st\n{full_st_code}\n```"
    print(f"Total assistant message length: {len(assistant_content)} characters")
    
    user_prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Steel & Heavy Metallurgy / 300-Ton Basic Oxygen Furnace (BOF/LD Converter)
Function Block Name: FB_Steel_BOF_Converter_DynamicLance_SublanceEndpoint_Offgas

System Scope:
Commercial 300-Metric-Ton Basic Oxygen Furnace (BOF / Linz-Donawitz Converter) Primary Steelmaking Vessel. Dynamic supersonic oxygen top lance blowing (Mach 2.2 multi-hole Laval nozzle, 900 Nm3/min O2 flow), dynamic in-blow sublance immersion probe carbon-temperature endpoint tracking, real-time offgas mass spectrometer analysis (CO, CO2, O2, N2, H2) for instantaneous decarburization rate dC/dt and post-combustion ratio, vessel trunnion acoustic accelerometer slag foaming slopping prevention, bottom-stirring inert gas (Ar/N2) porous plug flow coordination, and dry electrostatic precipitator (ESP) CO gas recovery switchover.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Molten steel bath carbon concentration C_bath [wt% C] and bath temperature T_bath [deg C]
   - Decarburization reaction rate dC/dt [%/min] and offgas CO/CO2 ratio
   - Slag FeO content [%] and acoustic shell slag foaming height index [dB]
   - Top oxygen lance height above molten bath Z_lance [mm] and supersonic O2 delivery pressure [bar]
   - Bottom inert gas stirring plug flow rate [Nm3/min] and stirring energy density [W/t]
   - Waste heat boiler hood draft differential pressure [Pa] and offgas evacuation flow [Nm3/h]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing top lance elevation winch VFD [mm/s], main oxygen flow control valve [%], flux addition vibratory feeder gate [% lime / dolomite], bottom argon/nitrogen flow valves [%], and primary offgas damper [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Main oxygen supply header pressure transmitters (O2_Press: 1, 2, 3) [bar]
   - Top lance cooling water inlet/outlet differential temperature RTDs (Delta_T: 1, 2, 3) [deg C]
   - Converter vessel trunnion acoustic slag foaming accelerometers (Acoustic_Slopping: 1, 2, 3) [dB]
   - Offgas analyzer mass spectrometer gas readings (CO_Conc: 1, 2, 3) [% vol CO]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_SCRAP_AND_HOT_METAL_CHARGING_TILT
   - 2: STATE_CONVERTER_VERTICAL_LOCK_AND_HOOD_LOWER
   - 3: STATE_OXYGEN_LANCE_IGNITION_SOFT_BLOW_HIGH_LANCE
   - 4: STATE_SILICON_OXIDATION_AND_FLUX_ADDITION_RUN
   - 5: STATE_MAIN_DECARBURIZATION_SUPERSONIC_DEEP_BLOW
   - 6: STATE_SLAG_FOAMING_CONTROL_AND_SLOPPING_SUPPRESSION
   - 7: STATE_DYNAMIC_SUBLANCE_IMMERSION_SAMPLE_ACQUIRE
   - 8: STATE_ENDPOINT_PREDICTION_FINE_O2_TRIM_BLOW
   - 9: STATE_BOTTOM_STIRRING_HOMOGENIZATION_RINSE
   - 10: STATE_LANCE_RETRACT_AND_BATH_TEMPERATURE_VERIFY
   - 11: STATE_VESSEL_TILT_STEEL_TAPPING_AND_ALLOY_TRIM
   - 12: STATE_SLAG_SPLASHING_REFRACTORY_COATING_CYCLE
   - 13: STATE_EMERGENCY_LANCE_WATER_LEAK_OR_HOOD_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    agent_id = uuid.uuid4().hex[:8]
    output_json_path = f"data/swarm_raw/agent_{agent_id}.json"
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_json_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Saved dataset record to {output_json_path}")
    
    # Run validation
    print("\nRunning validation via validate_iec.py...")
    cmd = [sys.executable, "validate_iec.py", output_json_path]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validation STDOUT:")
    print(res.stdout)
    if res.stderr:
        print("Validation STDERR:")
        print(res.stderr)
        
    if res.returncode == 0:
        print(f"\nSUCCESS! File {output_json_path} passed all validation checks!")
        return output_json_path, len(assistant_content), agent_id
    else:
        print(f"\nFAILED! Validation returned non-zero code {res.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    assemble()
