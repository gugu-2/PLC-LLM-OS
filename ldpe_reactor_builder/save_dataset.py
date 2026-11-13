# ldpe_reactor_builder/save_dataset.py
import json
import uuid
import os
import subprocess
from ldpe_reactor_builder.st_header_and_io import get_header_and_io
from ldpe_reactor_builder.st_var_declarations import get_var_declarations
from ldpe_reactor_builder.st_phase1_tmr import get_phase1_tmr
from ldpe_reactor_builder.st_phase2_observers import get_phase2_observers
from ldpe_reactor_builder.st_phase3_mpc import get_phase3_mpc
from ldpe_reactor_builder.st_phase4_fsm import get_phase4_fsm
from ldpe_reactor_builder.st_phase5_alarms import get_phase5_alarms

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

Commercial Sector: Chemical & Polymer Synthesis / 3,200-Bar Hyper-Compressor LDPE Tubular Reactor
Function Block Name: FB_Chemical_Polymers_HighPressure_LDPE_TubularReactor_Pulsation

System Scope:
Commercial High-Pressure Low-Density Polyethylene (LDPE / EVA Copolymer) Tubular Reactor (1,500 meters long, operating pressure up to 3,200 bar, peak reaction exotherm up to 310 deg C, annual capacity 450,000 tons). Dynamic multi-zone organic peroxide free-radical initiator micro-metering injection, supercritical ethylene reaction exotherm peak location tracking, high-pressure cyclic letdown valve (HPLDV) pulse depressurization cycling (250 bar pressure pulse every 20 seconds to scour polymer wall gel foulants), multi-jacket pressurized hot water cooling cascades, and sub-5 ms explosive decomposition (decomp) detection with fast hydraulically actuated snort valve venting.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Reactor peak exotherm temperature T_peak [deg C] and axial spatial location Z_peak [m]
   - Reactor inlet header hyper-compressor pressure P_inlet [bar] and outlet pressure P_outlet [bar]
   - Free-radical initiator conversion rate [%] and polyethylene melt flow index (MFI) [g/10min]
   - Inner tube polymer fouling boundary layer thermal resistance R_foul [m2 K/kW]
   - High-pressure letdown valve (HPLDV) hydraulic stroke [%] and pulsation amplitude [bar]
   - High-pressure recycle gas return flow rate [t/h] and compressor inter-stage suction pressure [bar]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing hyper-compressor throughput trim [%], organic peroxide initiator injection pump stroke rates across zones 1..4 [mL/h], high-pressure letdown valve baseline trim [%], and pressurized jacket water circulation throttle valves [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Ultra-high-pressure piezoresistive quartz transducers rated for 4,000 bar (Press_Sensors: 1, 2, 3) [bar]
   - Thick-walled multi-junction metal-sheathed Type K thermocouples (Temp_Sensors: 1, 2, 3) [deg C]
   - Optical absorption peroxide cocktail dosing Coriolis mass flowmeters (Peroxide_Flow: 1, 2, 3) [kg/h]
   - Tube wall acoustic emission decomposition precursors sensors (Acoustic_Sensors: 1, 2, 3) [dB]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_JACKET_WATER_PREHEAT_CIRCULATION_WARMUP
   - 2: STATE_ETHYLENE_GAS_PRESSURIZATION_RAMP_1000BAR
   - 3: STATE_HYPER_COMPRESSOR_SPINUP_TO_3000BAR
   - 4: STATE_INITIATOR_COCKTAIL_PRIME_AND_AIR_EXPULSION
   - 5: STATE_FIRST_ZONE_PEROXIDE_INJECTION_IGNITION
   - 6: STATE_NOMINAL_EXOTHERMIC_POLYMERIZATION_RUN
   - 7: STATE_CYCLIC_LETDOWN_PULSE_WALL_DE-FOULING_RUN
   - 8: STATE_DYNAMIC_GRADE_MFI_DENSITY_TRANSITION
   - 9: STATE_PEAK_TEMPERATURE_LIMITING_AUTO_TRIM
   - 10: STATE_CONTROLLED_PRODUCTION_TURNDOWN_AND_FLUSH
   - 11: STATE_ETHYLENE_MONOMER_RECYCLE_AND_DEPRESSURIZE
   - 12: STATE_REACTOR_TUBE_POST_WASH_AND_NITROGEN_SEAL
   - 13: STATE_EMERGENCY_DECOMPOSITION_FAST_SNORT_DUMP_TRIP
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
        print(f"\nFAILURE: Validation exited with code {result.returncode}")
        return output_path, len(assistant_content), False

if __name__ == "__main__":
    main()
