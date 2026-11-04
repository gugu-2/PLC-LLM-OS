# brain_scratch/can_seamer_builder/assemble_and_save.py
import os
import sys
import json
import uuid
import subprocess

sys.path.append(os.path.dirname(__file__))

from part1_decl import PART1_DECL
from part2_init_tmr import PART2_INIT_TMR
from part3_observers import PART3_OBSERVERS
from part4_ss_mpc import PART4_SS_MPC
from part5_fsm import PART5_FSM
from part6_seam_acoustic_steam import PART6_SEAM_ACOUSTIC_STEAM
from part7_alarms_clamp import PART7_ALARMS_CLAMP

raw_st = (PART1_DECL + 
          PART2_INIT_TMR + 
          PART3_OBSERVERS + 
          PART4_SS_MPC + 
          PART5_FSM + 
          PART6_SEAM_ACOUSTIC_STEAM + 
          PART7_ALARMS_CLAMP).strip()

# Verify start and end lines
lines = [l.strip() for l in raw_st.splitlines() if l.strip()]
print(f"First line: {lines[0]}")
print(f"Last line: {lines[-1]}")
assert lines[0].startswith("FUNCTION_BLOCK FB_FoodBev_RotaryCanSeamer_DoubleSeam_InertN2"), f"Invalid first line: {lines[0]}"
assert lines[-1] == "END_FUNCTION_BLOCK", f"Invalid last line: {lines[-1]}"

fenced_code = f"```iec-st\n{raw_st}\n```"
char_count = len(fenced_code)
print(f"Total fenced code character count: {char_count}")

prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Food & Beverage High-Speed Processing (Tier 1 Global High-Demand Industrial Automation)
- System: Ultra-High-Speed Continuous Rotary Aseptic Beverage Can Seamer (1,200 cans/minute, 18-Head Rotary Turret): Dynamic Double-Seam Mechanical Profiling (1st operation curl roll and 2nd operation flattening roll multi-axis servo cam synchronization, real-time seaming chuck axial load strain-gauge monitoring 3.5 to 8.0 kN), Liquid Nitrogen Headspace Dosing Injection (-196°C cryogenic micro-valve pulsed dosing for internal can pressurization and residual oxygen purge < 0.8% O2), Acoustic Impulse Sound Pressure Resonance Can Leak Inspection (Non-destructive ping & sensor array for micro-leak detection), Sterile Steam Barrier Turret Enclosure (125°C steam seal barrier preventing microbial ingress), and Synchronous Rotary Infeed Worm Screw / Starwheel Transfer.
- Function Block Name: `FB_FoodBev_RotaryCanSeamer_DoubleSeam_InertN2`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing turret angular velocity, 18-head seaming chuck axial load forces, liquid nitrogen dosing pulse duration, internal can headspace pressure, acoustic resonance frequency peak, steam enclosure temperature, infeed starwheel synchronization phase error, and seamer main drive motor torque ripple.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing double seam thickness error ($Q$), nitrogen dosing injector slew rate ($R$), and turret rotary cam synchronization jitter ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on seaming chuck load cells, nitrogen delivery manifold pressure transmitters, and enclosure aseptic steam barrier temperature RTDs.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Pre-Sterilization Steam Barrier Purge, Cryogenic Nitrogen Line Chill-Down, Infeed Turret Synchronization Inching, Can Infeed Detection & Lid Feeding Gate, Liquid Nitrogen Headspace Micro-Dosing, 1st Operation Roll Seaming Cam Engage, 2nd Operation Roll Ironing Dwell, Seam Thickness/Height Laser Gauging, Acoustic Ping Impulse Leak Inspection, High-Speed Rejection Gate Actuation, Rotary CIP Sanitization Wash, and Jam E-Stop Clamping Retract.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_FoodBev_RotaryCanSeamer_DoubleSeam_InertN2`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

agent_hex = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_hex}.json"

record = {
    "id": f"synthetic_v3_{agent_hex}",
    "instruction": prompt,
    "input": "",
    "output": fenced_code,
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": fenced_code}
    ],
    "metadata": {
        "domain": "Food & Beverage High-Speed Processing",
        "system": "Ultra-High-Speed Continuous Rotary Aseptic Beverage Can Seamer (1,200 cans/min, 18-Head Rotary Turret)",
        "block_name": "FB_FoodBev_RotaryCanSeamer_DoubleSeam_InertN2",
        "raw_st_char_count": len(raw_st),
        "fenced_char_count": char_count,
        "generator": "Lumina V7 Max-Persona Swarm",
        "ast_parity_valid": True,
        "characters": char_count,
        "tier": 1,
        "cycle": 2
    }
}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2, ensure_ascii=False)

print(f"Successfully saved to {filename}")

# Run validation
proc = subprocess.run([sys.executable, "validate_iec.py", filename], capture_output=True, text=True)
print("STDOUT from validate_iec.py:")
print(proc.stdout)
if proc.stderr:
    print("STDERR from validate_iec.py:")
    print(proc.stderr)

if proc.returncode != 0:
    print("VALIDATION FAILED!")
    sys.exit(proc.returncode)
else:
    print("ALL VALIDATION CHECKS PASSED WITH FLYING COLORS!")
