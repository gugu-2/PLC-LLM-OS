# mega_casting_builder/save_dataset.py

import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import test_build
import validate_iec

def save_and_validate():
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Heavy Machinery & Automotive Mega-Casting / High-Pressure Die Casting (HPDC)
Function Block Name: FB_Machining_DieCasting_ColdChamber_RealTimeInjection_PorosityControl

System Scope:
Commercial 6,000-Ton Giga-Casting Cold Chamber High-Pressure Die Casting (HPDC) Cell for single-piece aluminum structural rear underbody casting. Dynamic 4-stage real-time injection cylinder profile (Phase 1: Slow shot wave-free plunger motion, Phase 2: Ultra-fast cavity fill up to 9.5 m/s, Phase 3: High-pressure intensification up to 1,200 bar within 15 ms, Phase 4: Biscuit deceleration & holding), dual vacuum evacuation system (<25 mbar), hydraulic toggle lockup (60,000 kN), and multi-circuit mold thermal oil temperature regulation.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Plunger position x_p [mm] and plunger instantaneous velocity v_p [m/s]
   - Hydraulic shot cylinder head pressure P_head [bar] and rod pressure P_rod [bar]
   - Molten aluminum cavity pressure P_cavity [bar] and acoustic fill front shock [bar/ms]
   - Vacuum valve evacuation chamber pressure P_vac [mbar] and leak rate [mbar/s]
   - Die cavity metal temperature [deg C] and thermal oil circulation temperature [deg C]
   - Tie-bar dynamic strain stretch [um] and total clamping tonnage [kN]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing ultra-fast servo-proportional hydraulic injection valve [%], accumulator pilot pressure trim [%], intensification booster valve [%], vacuum exhaust throttle [%], and core pull sequence timing.
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Plunger magnetostrictive linear position transducers (Pos_Sensors: 1, 2, 3) [mm]
   - Hydraulic injection cylinder head pressure transducers (Head_Press: 1, 2, 3) [bar]
   - Die cavity piezo-electric quartz pressure transducers (Cavity_Press: 1, 2, 3) [bar]
   - Die parting plane vacuum capacitive vacuum transducers (Vac_Sensors: 1, 2, 3) [mbar]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_MOLD_DIE_PREHEAT_OIL_BALANCE
   - 2: STATE_LADLE_POUR_MOLTEN_ALUMINUM_SHOT_SLEEVE
   - 3: STATE_TOGGLE_CLAMP_LOCKUP_60000KN
   - 4: STATE_VACUUM_EVACUATION_DRAWDOWN_25MBAR
   - 5: STATE_PHASE1_SLOW_SHOT_WAVE_FREE_ACCEL
   - 6: STATE_PHASE2_FAST_SHOT_GATE_INJECTION_RUN
   - 7: STATE_PHASE3_INSTANT_INTENSIFICATION_SPIKE
   - 8: STATE_PHASE4_BISCUIT_HOLD_AND_SOLIDIFICATION
   - 9: STATE_VACUUM_VENT_AND_CORE_PULL_RETRACT
   - 10: STATE_DIE_CLAMP_OPEN_AND_DECEL_CUSHION
   - 11: STATE_SERVO_EJECTOR_CASTING_DEMOLD
   - 12: STATE_ROBOTIC_EXTRACTOR_AND_DIE_SPRAY_COAT
   - 13: STATE_EMERGENCY_METAL_FLASH_OR_PRESSURE_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    raw_code = test_build.assemble_code()
    formatted_content = f"```iec-st\n{raw_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": formatted_content}
        ]
    }
    
    agent_id = uuid.uuid4().hex[:8]
    output_filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{agent_id}.json")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Saved dataset to: {output_filename}")
    print(f"Structured Text length: {len(raw_code)} characters")
    print(f"Assistant content length: {len(formatted_content)} characters")
    
    # Run validation
    errs = validate_iec.validate_json_file(output_filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
        return output_filename, agent_id, len(raw_code)

if __name__ == "__main__":
    save_and_validate()
