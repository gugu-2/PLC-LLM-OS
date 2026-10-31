import json
import os
import subprocess
import generate_swro
import validate_iec

user_prompt = """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in mega-scale municipal and industrial water treatment, Seawater Reverse Osmosis (SWRO) desalination, isobaric energy recovery devices (ERD / PX), and high-pressure membrane separation.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Water Treatment & Municipal Infrastructure: 250,000 m3/Day Seawater Reverse Osmosis (SWRO) Desalination Plant with Isobaric Pressure Exchanger (PX) Energy Recovery, Membrane Fouling Diagnostics & CIP Flushing**
Function Block Name: `FB_WaterTreatment_SWRO_Desalination_PressureExchanger`
Target File: `data/swarm_raw/agent_4c9104ba.json`

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - Mega-scale SWRO desalination facility (Potable water production rate 250,000 m3/day across multiple parallel high-pressure RO trains; feed seawater salinity 35,000 to 45,000 ppm TDS, recovery ratio 42% to 48%).
   - High-Pressure Feed Pumps (HPP, multi-stage centrifugal pumps driven by 3.5 MW medium-voltage VFDs generating 60 to 75 bar feed pressure) coupled with Booster Pumps (BP).
   - Isobaric energy recovery devices (Energy Recovery Inc. PX pressure exchangers operating at 97.5% hydraulic energy transfer efficiency, transferring high-pressure concentrate brine energy directly into incoming raw seawater).
   - Real-time membrane hydraulics & fouling thermodynamics: normalized permeate flow rate, salt rejection calculation ($R_{\\text{salt}} > 99.7\\%$), temperature-compensated net driving pressure (NDP = Feed Pressure - Osmotic Pressure - Permeate Pressure), and dynamic Silt Density Index (SDI) / membrane compaction coefficient monitoring.
   - Pre-treatment coagulant dosing (ferric chloride), sodium bisulfite (SBS) chlorine neutralization, and antiscalant threshold inhibition.
   - Dual-stage Clean-In-Place (CIP) skid: low-pressure high-flow chemical cleaning (Citric acid inorganic scale removal at pH 2.5, followed by alkaline EDTA/surfactant organic fouling clean at pH 11.0) with automated permeate displacement flush.
   - Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating RO membrane solution-diffusion mass transport, concentration polarization layer dynamics, isobaric rotor mixing leakage, and header hydraulic inertia.
   - Receding-horizon MPC for multivariable control of HPP variable-speed drives, booster pump speeds, ERD concentrate throttling valves, and chemical dosing pumps to minimize specific energy consumption (SEC < 2.8 kWh/m3) while holding permeate TDS < 200 ppm.
   - 2oo3 Triple Modular Redundancy (TMR) voting across high-pressure feed transmitters, permeate conductivity meters, brine reject pressure sensors, and feed pH/ORP electrodes with bumpless degradation.
   - 12-Stage Operational FSM (Low-Pressure Raw Seawater Pre-Treatment Flush, Antiscalant & SBS Dosing Stabilization, High-Pressure RO Train Air De-Aeration Bleed, High-Pressure Pump Soft Ramp-Up, PX Energy Recovery Synchronous Coupling, Steady-State Desalination MPC, Permeate Conductivity Compliance Verification, Membrane Compaction Tracking, Automated Chemical CIP Sequence, Permeate Low-Pressure Displacement Rinse, RO Train Preservation Standby, Emergency High-Pressure Overpressure Hydraulic Dump).
   - ISA-18.2 multi-tiered alarm matrix (Feed pressure HH trip > 80 bar, permeate conductivity high alarm, PX differential pressure high, chlorine breakthrough ORP trip, membrane element integrity breach) with bit-packed telemetry DWORDs.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_WaterTreatment_SWRO_Desalination_PressureExchanger
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely (do not use `*)` inside comments; write `tau_star` instead of `tau*`).
   - Strongly typed bracketed physical units in VAR_INPUT comments: `[bar]`, `[m3/h]`, `[m3/day]`, `[ppm]`, `[deg C]`, `[uS/cm]`, `[rpm]`, `[kWh/m3]`, `[%]`, etc.
4. Dataset File Format:
   Save to `data/swarm_raw/agent_4c9104ba.json` in JSON format:
   {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "```iec-st\\n...\\n```"}]}
5. Self-Validation:
   Execute `python validate_iec.py data/swarm_raw/agent_4c9104ba.json` to verify that AST parity and code fences are 100% valid."""

st_code = generate_swro.build_swro_st_code()
assistant_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = os.path.join("data", "swarm_raw", "agent_4c9104ba.json")
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully wrote {target_file}")
print(f"Assistant content length: {len(assistant_content)} characters")

errs = validate_iec.validate_json_file(target_file)
if errs:
    print("VALIDATION FAILED:", errs)
    sys.exit(1)
else:
    print("VALIDATION PASSED!")
