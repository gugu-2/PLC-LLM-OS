import json
import os
import re
from test_builder import build_code
import validate_iec

prompt = """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in heavy commercial EV battery gigafactory automation and precision laser joining systems.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Automotive & EV Gigafactory: High-Speed Pouch Cell Automated Z-Folding Stacking, Tab Trimming & Dual-Wavelength Laser Tab Welding**
Function Block Name: FB_EVBattery_PouchCell_LaserTabWelding_Stacking
Target File: data/swarm_raw/agent_6c19a04f.json

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - High-speed Z-folding separator separator foil web tensioning and cathode/anode pouch cell vacuum stacking table (stacking accuracy +/- 0.1 mm at 0.15 s per layer).
   - Precision servo mechanical tab trim die with optical edge-guiding sensor and burr height inspection.
   - Dual-wavelength hybrid laser welding (Green 515 nm for high copper absorption + Infrared 1070 nm for penetration depth) or multi-beam wobbling laser welding of multi-layer copper and aluminum tabs (up to 60 foil tab layers).
   - In-line coaxial OCT (Optical Coherence Tomography) keyhole depth tracking and photodiode melt-pool emission pyrometry.
   - Discrete State-Space Model (12x12 state matrix A, 12x8 B, C, D) incorporating multi-layer thermal conduction, keyhole vapor recoil pressure dynamics, and servo clamping pressure kinematics.
   - Receding-horizon MPC for synchronized laser power modulation vs galvo mirror scan velocity and active clamping force regulation preventing spatter and blow-through.
   - 2oo3 Triple Modular Redundancy (TMR) voting across OCT laser keyhole sensors, coaxial pyrometers, and pneumatic/piezoelectric clamping force load cells.
   - 12-Stage Operational FSM (Separator Web Unwind & Dancer Tensioning, Cathode/Anode Alternating Pick-and-Place, Z-Fold Stacking Table Index, Stack Height & Optical Alignment Inspection, Ultrasonic Pre-Bonding, Mechanical Tab Trim & Slag Extraction, Multi-Layer Pneumatic Clamp Engagement, Dual-Wavelength Wobble Laser Seam Welding, Real-Time OCT Keyhole Depth Verification, In-Line Hi-Pot Insulation Check, Cell Stack Egress to Module Assembly, System Standby/Maintenance).
   - ISA-18.2 multi-tiered alarm matrix (Laser keyhole over-penetration HH, tab misregistration, clamping force shortfall, optical window fouling, emergency laser safety shutter interlock) with bit-packed telemetry DWORDs.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_EVBattery_PouchCell_LaserTabWelding_Stacking
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely (do not use *) inside comments; write tau_star instead of tau*)."""

code = build_code().strip()
asst_content = f"```iec-st\n{code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": asst_content}
    ]
}

target_file = "data/swarm_raw/agent_6c19a04f.json"
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully assembled and written to: {target_file}")
print(f"Assistant content character count: {len(asst_content)}")
print(f"Raw code character count: {len(code)}")

errs = validate_iec.validate_json_file(target_file)
if errs:
    print("VALIDATION FAILED with errors:")
    for e in errs:
        print(" -", e)
    exit(1)
else:
    print(">>> ALL VALIDATION CHECKS PASSED WITH 100% PARITY! <<<")
