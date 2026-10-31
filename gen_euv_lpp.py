# gen_euv_lpp.py
import sys
import os
import json

from euv_builder.euv_header import get_header
from euv_builder.euv_vars import get_var_input, get_var_output, get_var
from euv_builder.euv_phase1 import get_phase1
from euv_builder.euv_phase2 import get_phase2
from euv_builder.euv_phase3 import get_phase3
from euv_builder.euv_phase4 import get_phase4
from euv_builder.euv_phase5 import get_phase5

def main():
    prompt = """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in cutting-edge semiconductor lithography, Extreme Ultraviolet (EUV, 13.5 nm) light sources, laser-produced plasma (LPP), and multi-kilowatt CO2 drive lasers.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Semiconductor Fabrication: Extreme Ultraviolet (EUV, 13.5 nm) Laser-Produced Plasma (LPP) Light Source (500 W In-Band) with High-Frequency (50 kHz) Molten Tin Droplet Generator & Hydrogen Debris Mitigation**
Function Block Name: FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror
Target File: data/swarm_raw/agent_9e201b4c.json

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - High-power EUV source (500 W in-band 13.5 nm at intermediate focus IF): 50 kHz high-velocity molten tin droplet generator (droplet diameter 20–27 um, velocity 60–100 m/s, positional jitter < 1.5 um).
   - High-power pulsed CO2 laser system (40 kW master oscillator power amplifier MOPA chain, 10.6 um wavelength): pre-pulse laser shaping spherical tin droplet into flat pancake disk followed by main-pulse ionization into highly charged tin plasma (Sn10+ to Sn14+ at electron temperature 30–40 eV).
   - Ellipsoidal multi-layer Mo/Si collector mirror (diameter 660 mm, high EUV reflectivity > 68%): temperature conditioning via multi-zone cooling channels holding mirror surface within +/- 0.2 deg C under intense plasma radiation heat loads.
   - Hydrogen (H2) buffer gas flow & debris mitigation: high-flow molecular hydrogen (up to 200 slpm) combined with magnetic field deflection (0.8 to 1.5 Tesla superconducting magnet) decelerating and sweeping fast tin ions, and chemical etching (forming volatile stannane gas SnH4 pumped away by vacuum turbopumps) to prevent collector mirror reflective degradation.
   - Optical droplet detection & laser steering: in-line laser backlight shadowgraph cameras detecting droplet coordinates (X, Y, Z, t) commanding 2-axis piezo-electric galvo steering mirrors in real time (< 20 us response).
   - Vacuum vessel pressure regulation: maintaining 1.0 to 10.0 Pa H2 buffer gas pressure under dynamic gas injection and high-throughput turbomolecular pumps.
   - Discrete State-Space Model (16x16 state matrix A, 16x8 B, C, D) incorporating tin droplet acoustic Rayleigh break-up kinetics, laser plasma expansion hydrodynamics, collector mirror thermal diffusion, and stannane chemical reaction mass balance.
   - Receding-horizon MPC for joint pre-pulse/main-pulse laser timing, droplet generator piezo drive frequency/amplitude, and hydrogen gas flow modulation.
   - 2oo3 Triple Modular Redundancy (TMR) voting across droplet shadowgraph camera coordinates, collector mirror surface pyrometers, vessel vacuum capacitance manometers, and intermediate focus EUV energy sensors with bumpless degradation.
   - 12-Stage Operational FSM (Vessel Vacuum Pump-Down & Inert Gas Purge, Molten Tin Reservoir Melting & Heating to 260 deg C, Piezo Nozzle Acoustic Frequency Tuning, High-Velocity Droplet Stream Jetting, Droplet Flight Trajectory Verification & Shadowgraph Calibration, Hydrogen Gas Buffer Flow & Magnetic Field Ramp, Low-Power Laser Alignment Pre-Pulse Strike, Main-Pulse Plasma Ignition & In-Band EUV Light Generation, Closed-Loop In-Band 500W Power Stabilization MPC, Collector Mirror Thermal & Stannane Etch Cleaning, Laser Safe Shutter Close & Tin Jet Extinguish, Emergency Hydrogen Safe Snuff & Vessel Vacuum Lockout).
   - ISA-18.2 / SEMI S2 multi-tiered alarm matrix (Collector mirror temperature runaway HH trip, droplet positional loss trip, vessel overpressure, hydrogen gas leak LEL trip, laser beam steering misalignment) with bit-packed telemetry DWORDs.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely (do not use `*)` inside comments; write `tau_star` instead of `tau*`).
   - Strongly typed bracketed physical units in VAR_INPUT comments: `[um]`, `[m/s]`, `[W]`, `[kW]`, `[deg C]`, `[Pa]`, `[kHz]`, `[slpm]`, `[Tesla]`, `[%]`, etc.
4. Dataset File Format:
   Save to `data/swarm_raw/agent_9e201b4c.json` in JSON format:
   {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "```iec-st\\n...\\n```"}]}
5. Self-Validation:
   Execute `python validate_iec.py data/swarm_raw/agent_9e201b4c.json` to verify that AST parity and code fences are 100% valid."""

    print("Assembling IEC 61131-3 Structured Text for EUV LPP Light Source...")
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

    target_file = "data/swarm_raw/agent_9e201b4c.json"
    os.makedirs(os.path.dirname(target_file), exist_ok=True)
    with open(target_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to {target_file}")
    print(f"Total ST code length: {len(code_body)} chars")
    print(f"Total assistant content length: {len(full_output)} chars")

if __name__ == "__main__":
    main()
