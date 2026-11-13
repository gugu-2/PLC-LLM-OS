import sys
import os
import json
import uuid

prompt_text = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 2 - CYCLE 2):
- Domain: Tunnel Boring, Underground Mining & Heavy Civil Infrastructure (Tier 2 High-Demand Industrial Automation)
- System: 14.5-Meter Mixshield / Slurry Tunnel Boring Machine (TBM) Excavation Complex: Pressurized Bentonite Slurry Chamber Pressure Closed-Loop Regulation (Compressed air bubble cushion, dynamic slurry feed/discharge pump balance maintaining earth support pressure ±0.03 bar to prevent surface ground subsidence), 24-Group Hydraulic Thrust Cylinder Ring Synchronization (250,000 kN total thrust capacity, 350 bar proportional servo valves with active shield pitch/yaw articulation and stroke differential leveling), Multi-Drive Electric Cutterhead (16 x 350 kW variable-frequency drive motors with real-time disc cutter rock impact torque ripple observer), 6-DOF Precast Concrete Segment Erector (Hydraulic gripper position laser docking with vacuum suction pad seal), and Tail Skin Two-Component (A+B) Grout Injection Volume & Pressure Barrier.
- Function Block Name: `FB_Civil_TBM_SlurryShield_ThrustRingSync`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing slurry bubble chamber pressure, bentonite slurry density, cutterhead rotational speed, cutterhead active torque, shield advance rate mm/min, total thrust force kN, shield articulation pitch angle, and tail void grout injection pressure.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing face pressure fluctuation ($Q$), thrust cylinder differential pressure skew ($R$), and shield trajectory alignment deviation ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on excavation chamber membrane pressure transmitters, main thrust cylinder pressure transducers, and laser guidance total station prism receivers.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Slurry Line Circulation & Air Cushion Pre-Charging, Excavation Face Pressure Equalization, Cutterhead Slow Rotation Inching, Synchronous Thrust Advance Ring Extension, Dynamic Articulation Steering Adjustment, Slurry Mud Flow Extraction Balancing, Ring Stroke End & Thrust Pressure Hold, Segment Erector Vacuum Pad Grip, Precast Ring Installation & Key Segment Insertion, Tail Shield Wire Seal Grease & Grout Injection, Guidance Total Station Laser Check, and Face Collapse Overpressure Emergency Halt.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_Civil_TBM_SlurryShield_ThrustRingSync`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

def build_iec_code():
    import test_gen
    raw_code = test_gen.generate_iec_block()
    return f"```iec-st\n{raw_code}\n```"

def main():
    agent_uuid = "33fbd5b4"
    output_filename = f"data/swarm_raw/agent_{agent_uuid}.json"
    
    code = build_iec_code()
    print(f"Total assistant code block length: {len(code)} characters")
    
    record = {
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": code}
        ]
    }
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Successfully wrote dataset to {output_filename}")

if __name__ == "__main__":
    main()
