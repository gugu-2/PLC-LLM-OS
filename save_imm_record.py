# -*- coding: utf-8 -*-
"""
Generate and save dataset record to data/swarm_raw/agent_<uuid>.json
"""
import json
import uuid
import os
import re
from generate_imm_dataset import generate_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.

DOMAIN & SPECIFICATION:
- Domain: Heavy Commercial Plastics & High-Tonnage Polymer Processing
- System: 1,200-Ton All-Hydraulic Two-Platen Injection Molding Machine (IMM) for Automotive Bumper Fascia: Closed-Loop Electro-Hydraulic Servo Valve Control, Velocity-to-Pressure (V/P) Bumpless Transfer Point Detection (based on multi-cavity piezoelectric melt pressure sensors, screw position, and hydraulic pressure derivatives), Multi-Stage Dynamic Melt Holding Pressure Profile, 6-Zone Electric Barrel Heating with Ceramic Band PWM Duty Cycling, Tie-Bar Tonnage Strain-Gauge Clamping Force Balancing (preventing mold flash or platen tilt), Hydraulic Ejector Multi-Pulse De-Molding, and High-Speed Hydraulic Accumulator Injection Assist.
- Function Block Name: FB_Plastics_InjectionMolding_1200T_HydraulicServo_VP

MANDATORY REQUIREMENTS:
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID tags: ZT_SCREW_POSITION_101A/B/C, PT_INJECTION_HYD_PRESSURE_102A/B/C, ST_SCREW_ROTATION_RPM_103A/B/C, PT_MOLD_CAVITY_MELT_PRESS_201A/B/C, TT_MELT_NOZZLE_INFRARED_202A/B/C, WT_TIEBAR_1_STRAIN_TONNAGE_301A/B/C, WT_TIEBAR_2_STRAIN_TONNAGE_302A/B/C, WT_TIEBAR_3_STRAIN_TONNAGE_303A/B/C, WT_TIEBAR_4_STRAIN_TONNAGE_304A/B/C, ZT_CLAMP_PLATEN_POSITION_305A/B/C, TT_BARREL_ZONE1_TEMP_401A/B/C through TT_BARREL_ZONE6_TEMP_406A/B/C, PT_ACCUMULATOR_N2_PRECHARGE_501A/B/C, ZT_EJECTOR_PULSE_POS_601A/B/C.
2. 2oo3 Triple Modular Redundancy (TMR):
   - Full triplicated voting across screw position linear transducer triplets, hydraulic injection cylinder pressure transmitters, cavity melt pressure sensors, and tie-bar tonnage strain gauges with pairwise deviation registers, 1 ms fast trip voting, bumpless degradation, and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - Polymer melt rheology & Tait equation-of-state PVT model: calculates instantaneous specific volume v(P, T), polymer compressibility, and thermal contraction shrinkage to optimize holding pressure trajectory.
   - V/P Transfer Point Predictor: evaluates cavity pressure threshold, screw stroke inflection (d^2 z / dt^2), and hydraulic pressure surge (dP/dt > 1,500 bar/s) to achieve sub-millisecond bumpless switch from velocity filling to pressure packing.
   - 4-Corner Tie-bar tonnage balance observer: calculates platen parallelism deflection (Delta delta < 0.05 mm) and modulates individual corner proportional valve pressures to prevent asymmetric mold breathing and part flash.
   - Barrel thermal zone decoupling: state-space thermal conductivity observer predicting conductive shear heating from screw recovery rotation.
4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 State-Space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) running at Ts = 1 ms.
   - Optimizes injection servo valve opening, accumulator discharge proportioning, holding pressure ramp rate, and backpressure during plasticizing.
5. ISA-18.2 Alarm Ladder:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC).
   - Mold safety gate optical barrier intrusion trip, tie-bar overload trip (> 1,350 tons), nozzle cold-slug solidification trip, and hydraulic oil thermal degradation trip.
6. Multi-Stage Operational FSM:
   - 12-state Finite State Machine: IMM_STANDBY_MOLD_OPEN, BARREL_PREHEAT_SOAK_TEMP, MOLD_CLAMP_TONNAGE_BUILD_1200T, HIGH_SPEED_INJECTION_VELOCITY_FILL, VP_TRANSFER_POINT_TRANSITION, DYNAMIC_CAVITY_PRESSURE_PACKING, SCREW_RECOVERY_AND_PLASTICIZING, COOLING_CYCLE_AND_SUCK_BACK, MOLD_OPEN_DECELERATION_SOFT_STOP, HYDRAULIC_EJECTOR_MULTI_PULSE, ROBOT_GRIPPER_PART_TAKEOUT, EMERGENCY_ESTOP_HYDRAULIC_DUMP.
7. Extreme Token Density & Code Completeness:
   - Zero summaries, zero // ... rest of code, zero placeholders.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - TRIPLE backticks with iec-st. Output Structured Text MUST be 50,000 to 85,000+ characters of pristine, industrial Structured Text."""

def main():
    st_code = generate_code()
    
    # Validation checks
    assert st_code.startswith("FUNCTION_BLOCK FB_Plastics_InjectionMolding_1200T_HydraulicServo_VP"), "Invalid first line!"
    assert st_code.rstrip().endswith("END_FUNCTION_BLOCK"), "Invalid last line!"
    
    clean = re.sub(r'\(\*.*?\*\)', '', st_code, flags=re.DOTALL)
    if_count = len(re.findall(r'\bIF\b', clean))
    endif_count = len(re.findall(r'\bEND_IF;', clean))
    assert if_count == endif_count, f"IF/END_IF mismatch: {if_count} vs {endif_count}"
    
    case_count = len(re.findall(r'\bCASE\b', clean))
    endcase_count = len(re.findall(r'\bEND_CASE;', clean))
    assert case_count == endcase_count, f"CASE/END_CASE mismatch: {case_count} vs {endcase_count}"
    
    for_count = len(re.findall(r'\bFOR\b', clean))
    endfor_count = len(re.findall(r'\bEND_FOR;', clean))
    assert for_count == endfor_count, f"FOR/END_FOR mismatch: {for_count} vs {endfor_count}"
    
    print(f"Validation Passed!")
    print(f"Total ST Code Length: {len(st_code)} characters")
    print(f"Total Lines: {len(st_code.splitlines())}")
    print(f"IF: {if_count}, END_IF;: {endif_count}")
    print(f"CASE: {case_count}, END_CASE;: {endcase_count}")
    print(f"FOR: {for_count}, END_FOR;: {endfor_count}")
    
    assistant_content = f"```iec-st\n{st_code.strip()}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    raw_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{raw_id}.json"
    abs_path = os.path.abspath(filename)
    
    with open(abs_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Saved dataset record to {abs_path}")
    print(f"File size on disk: {os.path.getsize(abs_path)} bytes")
    
    # Re-read and verify JSON integrity
    with open(abs_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert len(loaded["messages"]) == 2
    assert loaded["messages"][1]["content"].startswith("```iec-st\nFUNCTION_BLOCK")
    assert loaded["messages"][1]["content"].endswith("END_FUNCTION_BLOCK\n```")
    print("JSON read-back validation completely successful!")
    print(f"DATASET_UUID: agent_{raw_id}")

if __name__ == "__main__":
    main()
