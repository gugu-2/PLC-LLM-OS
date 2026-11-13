# blown_film_builder/save_dataset.py
import json
import uuid
import os
import subprocess
from blown_film_builder.st_header_and_io import get_header_and_io
from blown_film_builder.st_var_declarations import get_var_declarations
from blown_film_builder.st_phase1_tmr import get_phase1_tmr
from blown_film_builder.st_phase2_observers import get_phase2_observers
from blown_film_builder.st_phase3_mpc import get_phase3_mpc
from blown_film_builder.st_phase4_fsm import get_phase4_fsm
from blown_film_builder.st_phase5_alarms import get_phase5_alarms

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

Commercial Sector: Plastics & Advanced Polymers / 7-Layer Barrier Blown Film Extrusion
Function Block Name: FB_Plastics_BlownFilm_7Layer_AirRing_ThicknessProfile

System Scope:
Commercial 7-Layer Barrier Blown Film Co-Extrusion Line (EVOH, PA/Nylon, Tie, PE structure for aseptic food packaging, bubble lay-flat width 2,600 mm, line speed 150 m/min). Real-time coordinated regulation of segmented dual-lip non-contact air ring with 128 thermal expansion bolt servo zones, Internal Bubble Cooling (IBC) ultrasonic non-contact bubble diameter regulation, non-contact rotating capacitive/beta-gauge thickness sensor, and haul-off cage oscillating nip roll tension.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Dynamic 2D spatial film thickness profile gauge deviation [um]
   - IBC internal bubble diameter & air exchange differential pressure [Pa]
   - Bubble frost-line height (FLH) [mm]
   - Melt temperature across 7 extruder die rings [deg C]
   - Primary air ring blower flow velocity [m/s] and secondary lip chill temperature [deg C]
   - Haul-off nip draw ratio and oscillating web tension [N]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing 128-zone thermal bolt heater power trim [%], IBC supply/exhaust blower VFD speeds [RPM], primary cooling air ring flow valve [%], extruder screw speed trims across 7 extruders [RPM], and haul-off line speed [m/min].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - IBC ultrasonic non-contact bubble diameter transducers (IBC_Sensors: 1, 2, 3) [mm]
   - Frost-line optical infrared camera height sensors (FLH_Sensors: 1, 2, 3) [mm]
   - Die exit total melt pressure transducers (Melt_Press: 1, 2, 3) [bar]
   - Web tension load cells at oscillating haul-off unit (Tension_Sensors: 1, 2, 3) [N]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_DIE_TOOLING_AND_BARREL_THERMAL_SOAK
   - 2: STATE_EXTRUDER_SCREW_START_AND_LOW_SPEED_MELT
   - 3: STATE_BUBBLE_INCEPTION_MANUAL_INFLATION
   - 4: STATE_IBC_AUTOMATIC_DIAMETER_ACQUISITION
   - 5: STATE_FROST_LINE_STABILIZATION_RAMP
   - 6: STATE_ROTATING_THICKNESS_GAUGE_CALIBRATION
   - 7: STATE_INITIAL_PROFILE_MAPPING_AND_MAPPING_MATRIX
   - 8: STATE_CLOSED_LOOP_128ZONE_AIR_RING_CONTROL
   - 9: STATE_NOMINAL_HIGH_SPEED_PRODUCTION_STEADY
   - 10: STATE_DYNAMIC_RECIPE_WIDTH_OR_THICKNESS_CHANGE
   - 11: STATE_BUBBLE_BREATHE_INSTABILITY_DAMPING
   - 12: STATE_AUTOMATED_COORDINATED_LINE_RAMPDOWN
   - 13: STATE_BUBBLE_COLLAPSE_OR_TEAR_EMERGENCY_STOP
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
