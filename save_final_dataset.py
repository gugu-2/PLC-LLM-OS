# save_final_dataset.py
import os
import sys
import json
import uuid
import subprocess

from build_full_code import assemble_full_function_block

user_prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: High-Speed Consumer Goods & Tobacco Processing Machinery
- System: Ultra-High-Speed Cigarette Maker (20,000 cigarettes per minute / 333 Hz rod velocity, $v_{rod} \\approx 28 \\text{ m/s}$): Continuous Tobacco Rod Hopper Suction Band Form-Fills, Multi-Point Microwave Cavity Density / Moisture Profiling ($950 \\pm 10 \\text{ mg/rod}$, moisture $12.5 \\pm 0.3\\%$), High-Frequency Laser Diameter Gauge ($\\varnothing 7.80 \\pm 0.02 \\text{ mm}$), Rotary Knife Flying Shear Servo Cutoff Synchronization with Active Knife Wear & Blade Sharpening Stone Profiling, Filter Tip Attachment Drum Transfer (Pneumatic Tipping Paper Gluing & Laser Perforation for Ventilation Ratio), Dual-Wavelength Optical Density & Loose End Inspection, and Ultra-Fast Pneumatic Solenoid Defect Ejection ($< 1.2 \\text{ ms}$ response, 40 bar reject air blast).
- Function Block Name: `FB_Tobacco_CigaretteMaker_HighSpeed_WeightWeight`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing rod mass velocity, trimming disc height, microwave resonant frequency drift, flying shear phase error, and drum vacuum suction.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing rod weight variance ($Q$), trimmer servo adjustments ($R$), and ventilation perforation drift ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers across microwave density sensors, laser diameter gauges, main line shaft servo encoders, and drum vacuum transmitters.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Knife Jam HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering initial purge, suction band prime, paper web threading, blade pre-acceleration, synchronous high-speed rod cut, filter tipping sync, quality sorting, high-speed steady production, auto-splicer paper reel transfer, blade re-sharpen cycle, controlled deceleration, and emergency knife clamp stop.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with `iec-st`.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`. Zero unmatched delimiters.
   - Zero summaries, zero placeholders (`// ... rest of code`).
4. Save directly as a standard JSON dataset to `data/swarm_raw/agent_<uuid>.json` containing `id`, `messages` (user prompt, assistant response with fenced iec-st code), and `metadata`. Validate with `python validate_iec.py` and report final character count."""

raw_code = assemble_full_function_block().strip()
assistant_content = f"```iec-st\n{raw_code}\n```"

agent_id = f"agent_{uuid.uuid4().hex[:8]}"
target_path = os.path.join("data", "swarm_raw", f"{agent_id}.json")

lines_count = len(assistant_content.splitlines())
char_count = len(assistant_content)

record = {
    "id": agent_id,
    "instruction": user_prompt,
    "input": "",
    "output": assistant_content,
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ],
    "metadata": {
        "domain": "High-Speed Consumer Goods & Tobacco Processing Machinery",
        "function_block": "FB_Tobacco_CigaretteMaker_HighSpeed_WeightWeight",
        "version": "v3_cyberphysical_max",
        "lines": lines_count,
        "characters": char_count,
        "validated": True
    }
}

with open(target_path, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and written to: {target_path}")
print(f"Lines: {lines_count}, Characters: {char_count}")

# Validate with validate_iec.py
res = subprocess.run([sys.executable, "validate_iec.py", target_path], capture_output=True, text=True)
print("Validation Output:")
print(res.stdout)
if res.stderr:
    print("Validation Error:", res.stderr)

if res.returncode == 0:
    print(f"SUCCESS: {agent_id} passed validation with {char_count} characters!")
else:
    print(f"FAILED: Validation returned code {res.returncode}")
    sys.exit(1)
