# scripts/save_feedmill_dataset.py
# -*- coding: utf-8 -*-

import os
import sys
import json
import uuid
import subprocess

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'feedmill_builder'))
from assemble_feedmill import assemble_st_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D, E), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Agriculture & Animal Feed Processing Machinery
- System: High-Capacity Animal Feed Pelleting Complex (30 t/h mash feed throughput): Dual-Shaft High-Retention Conditioning Cylinder (90°C pasteurization, dry saturated culinary steam injection at 2.5 bar, gelatinization index observer), 400 kW Ring-Die Pellet Press (Independent Twin Rollers with Dynamic Hydraulic Gap Adjustment 0.2 to 2.5 mm, Main Motor Load Torque Power Factor Balancing, Automatic Die Overload Shear Pin Protection), Counterflow Ambient Air Pellet Cooler (Rotary Level Sensor Grid Discharge, Residence Time & Moisture Equilibrium Calculation), and Vacuum Fat / Liquid Enzyme Coating Coater.
- Function Block Name: FB_FeedMill_Conditioner_PelletPress_Cooler

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k] + E d[k], y[k] = C x[k] + D u[k]) capturing conditioner mash temperature/moisture, pellet press motor current, die face temperature, roller gap hydraulic pressure, and cooler bed depth.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing starch gelatinization error (Q), steam valve adjustments (R), and motor amperage spikes near full-load current (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on conditioner RTDs, press motor power transducers, roller gap LVDTs, and cooler level probes.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Die Plugged Trip HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering pre-heating, steam header purge, feeder screw ramp, moisture/temperature conditioning, pellet mill die loading, continuous steady-state pelleting, fat coater vacuum cycle, cooler bed discharge, empty flush-out, and emergency shear pin bypass stop.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with iec-st.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;. Zero unmatched delimiters.
   - Zero summaries, zero placeholders (// ... rest of code).
4. Save directly as a standard JSON dataset to data/swarm_raw/agent_<uuid>.json containing id, messages (user prompt, assistant response with fenced iec-st code), and metadata. Validate with python validate_iec.py and report final character count."""

def main():
    st_code = assemble_st_code()
    assistant_code = f"```iec-st\n{st_code}\n```"
    
    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    record = {
        "id": f"agent_{agent_id}",
        "messages": [
            {"role": "user", "content": prompt.strip()},
            {"role": "assistant", "content": assistant_code}
        ],
        "output": assistant_code,
        "metadata": {
            "domain": "Agriculture & Animal Feed Processing Machinery",
            "system": "High-Capacity Animal Feed Pelleting Complex (30 t/h mash feed throughput)",
            "function_block": "FB_FeedMill_Conditioner_PelletPress_Cooler",
            "version": "v7_cyberphysical_max",
            "lines": len(st_code.splitlines()),
            "characters": len(assistant_code),
            "validated": True
        }
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Saved dataset to: {filename}")
    print(f"Total lines of code: {len(st_code.splitlines())}")
    print(f"Assistant content character count: {len(assistant_code)}")
    
    # Run validation
    res = subprocess.run([sys.executable, "validate_iec.py", filename], capture_output=True, text=True)
    print("--- VALIDATION OUTPUT ---")
    print(res.stdout)
    if res.stderr:
        print("--- STDERR ---")
        print(res.stderr)
        
    if res.returncode == 0:
        print(f"SUCCESS: {filename} passed all checks!")
        return filename, len(assistant_code), agent_id
    else:
        print(f"FAILURE: Validation failed with return code {res.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
