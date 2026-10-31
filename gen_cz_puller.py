# gen_cz_puller.py
import sys
import os
import json

from cz_builder.cz_header import get_header
from cz_builder.cz_vars import get_var_input, get_var_output, get_var
from cz_builder.cz_phase1 import get_phase1
from cz_builder.cz_phase2 import get_phase2
from cz_builder.cz_phase3 import get_phase3
from cz_builder.cz_phase4 import get_phase4
from cz_builder.cz_phase5 import get_phase5

def main():
    prompt = """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in heavy commercial semiconductor crystal growth and high-temperature vacuum furnace automation.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Semiconductor & Silicon Processing: 300 mm Silicon Single-Crystal Czochralski (Cz) Ingot Puller Furnace with Induction Heating & Melt Meniscus Optical Closed-Loop Control**
Function Block Name: FB_Semiconductor_Czochralski_IngotPuller_Furnace
Target File: data/swarm_raw/agent_9c410b8f.json

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - High-temperature vacuum furnace with multi-zone graphite resistance/induction heaters (Side heaters, Bottom heater) maintaining molten silicon at 1,420 deg C under ultra-pure Argon (Ar) atmosphere (15–30 mbar vacuum).
   - High-precision cable/shaft lift drive (pull speed 0.1–2.5 mm/min with sub-micron jitter) and seed crystal rotation (5–25 RPM).
   - Quartz crucible lift mechanism compensating for melt level drop as crystal mass is extracted, coupled with crucible counter-rotation to homogenize thermal and oxygen distribution.
   - Real-time optical/laser triangulation measuring the bright melt-crystal meniscus ring diameter and solid-liquid phase boundary height.
   - Dash necking stage (dislocation-free crystal initiation at high pull speed ~4–6 mm/min, diameter 3–4 mm), crown shoulder expansion to 300 mm (+/- 0.5 mm), steady-state cylindrical body growth, and tail-off thermal shock prevention.
   - Discrete State-Space Model (12x12 state matrix A, 12x8 B, C, D) incorporating Stefan problem latent heat of fusion release (q_L = rho * L * v_pull), thermal radiation in quartz chamber, Marangoni and buoyancy convection in melt, and crucible heat capacity.
   - Receding-horizon MPC for multivariable control of heater powers, pull velocity, and crucible lift speed to hold diameter within +/- 0.3 mm while maintaining Voronkov ratio (v/G) to suppress point defect clusters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across optical pyrometers, furnace wall thermocouples, and melt level laser sensors.
   - 12-Stage Operational FSM (Furnace Vacuum Pump-Down, Argon Gas Purge Flush, Polysilicon Melting & Doping, Melt Stabilization & Zero Tare, Seed Crystal Dip & Dash Necking, Crown Expansion Shoulder Growth, Body Diameter Stabilization, Steady-State Body Pull, Tail-Off Cone Reduction, Ingot Separation & Lift to Cooling Chamber, Furnace Controlled Cool-Down, Maintenance Turnaround).
   - ISA-18.2 multi-tiered alarm matrix (Crucible leak/burnout HH, Argon purge failure, meniscus lost alarm, heater circuit imbalance, emergency seed lift disconnect) with bit-packed telemetry DWORDs.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_Semiconductor_Czochralski_IngotPuller_Furnace
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely.
4. Dataset File Format:
   Save to data/swarm_raw/agent_9c410b8f.json in JSON format:
   {"instruction": "...", "input": "...", "output": "```iec-st\\n...\\n```"}
5. Self-Validation:
   Execute python validate_iec.py data/swarm_raw/agent_9c410b8f.json to verify that AST parity and code fences are 100% valid."""

    print("Assembling IEC 61131-3 Structured Text...")
    h = get_header()
    vi = get_var_input()
    vo = get_var_output()
    v = get_var()
    p1 = get_phase1()
    p2 = get_phase2()
    p3 = get_phase3()
    p4 = get_phase4()
    p5 = get_phase5()

    code_body = f"{h}\n{vi}\n{vo}\n{v}\n{p1}\n{p2}\n{p3}\n{p4}\n{p5}"
    full_output = f"```iec-st\n{code_body}\n```"

    record = {
        "instruction": prompt,
        "input": "",
        "output": full_output,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_output}
        ]
    }

    target_file = "data/swarm_raw/agent_9c410b8f.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to {target_file}")
    print(f"Total ST code length: {len(code_body)} chars")
    print(f"Total assistant content length: {len(full_output)} chars")

if __name__ == "__main__":
    main()
