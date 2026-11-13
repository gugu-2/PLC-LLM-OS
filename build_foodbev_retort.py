# -*- coding: utf-8 -*-
"""
Master Builder: build_foodbev_retort.py
Assembles FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo,
validates syntax & delimiter parity, generates synthetic dataset record,
and saves to data/swarm_raw/agent_<uuid>.json.
"""

import os
import json
import uuid
import subprocess

from retort_builder.mod_header_io import generate_header_io
from retort_builder.mod_var_decl import generate_var_decl
from retort_builder.mod_matrices_init import generate_matrices_init
from retort_builder.mod_tmr import generate_tmr
from retort_builder.mod_cyberphysical import generate_cyberphysical
from retort_builder.mod_mpc import generate_mpc
from retort_builder.mod_ball_fda import generate_ball_fda
from retort_builder.mod_fsm import generate_fsm
from retort_builder.mod_alarms import generate_alarms

def assemble_code():
    parts = [
        generate_header_io(),
        generate_var_decl(),
        generate_matrices_init(),
        generate_tmr(),
        generate_cyberphysical(),
        generate_mpc(),
        generate_ball_fda(),
        generate_fsm(),
        generate_alarms()
    ]
    return '\n\n'.join(parts)

def build_dataset():
    st_code = assemble_code()
    print(f"Total Structured Text character count: {len(st_code)}")
    print(f"Total Structured Text line count: {len(st_code.splitlines())}")

    prompt_text = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following industrial domain and specification:

### ASSIGNED DOMAIN & FUNCTION BLOCK:
- Domain: Commercial Food & Beverage Heavy Processing (Tier 1 Priority Sector)
- Function Block Name: FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo
- Target System: Industrial Continuous Rotary Overpressure Retort Autoclave for Low-Acid Canned Foods (LACF), Lethality F0 & Ball Process Time Tracking, Steam-Air Overpressure Temperature/Pressure Decoupled Cascade Control, and Accelerated Evaporative Cooling with Deflection Counter-Pressure.

### MANDATORY ARCHITECTURAL & CYBER-PHYSICAL SPECIFICATIONS:
1. Mathematical Cyber-Physical Rigor:
   - Explicit Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) at Ts = 100 ms modeling vessel steam temperature Tv, vessel overpressure Pv, core product cold-spot temperature Tcore, container internal pressure Pcan, container wall differential stress DeltaP = Pcan - Pv, instantaneous microbial lethality rate L(Tcore) = 10^((Tcore - 121.11)/z) with z = 10.0 deg C, cumulative thermal lethality integral F0 = integral(L dt) [min], and sump liquid water level Hsump.
   - Receding Horizon Model Predictive Control (MPC) / Projected Gradient Descent (PGD) unrolled solver over prediction horizon N = 5 to optimize culinary steam valve, compressed air overpressure injection, sterile water spray cooling, and vent modulation while decoupling vessel pressure from temperature to eliminate can peaking/bursting or panel buckling.
   - 2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) voting across critical sensor channels (Vessel Temp TT-101A/B/C, Vessel Pressure PT-201A/B/C, Basket Core Simulators TT-301A/B/C, Sump Water Level LT-401A/B/C) with bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Failsafe) and discrepancy debounce timers.
   - US FDA 21 CFR Part 113 Regulatory Compliance: Automated process deviation detector (Tv < scheduled cook - 0.5 deg C), C.O. Ball formula thermal process calculation (B = fh * [log10(jch * Ih) - log10(g)]), and dynamic supplemental cook time extension to guarantee commercial sterility.
   - Deterministic 14-Stage Production FSM:
     Stage 00: STATE_IDLE_STANDBY
     Stage 01: STATE_VESSEL_LOCK_SEAL_INFLATION
     Stage 02: STATE_AIR_VENT_PURGE
     Stage 03: STATE_STEAM_COME_UP_RAMP
     Stage 04: STATE_TEMPERATURE_CUT_IN
     Stage 05: STATE_OVERPRESSURE_STERILIZATION_HOLD
     Stage 06: STATE_BALL_PROCESS_DEVIATION_CATCHUP
     Stage 07: STATE_PRE_COOLING_PRESSURE_EQUALIZATION
     Stage 08: STATE_WATER_SPRAY_CASCADE_COOLING
     Stage 09: STATE_RECIRCULATION_EVAPORATIVE_COOLING
     Stage 10: STATE_OVERPRESSURE_WATER_DRAIN
     Stage 11: STATE_ATMOSPHERIC_VACUUM_BREAK
     Stage 12: STATE_LID_SEAL_DEFLATION_UNLATCH
     Stage 13: STATE_CIP_SIP_SANITATION
     Stage 14: STATE_EMERGENCY_SAFETY_RELIEF_ABORT
   - ISA-18.2 Multi-Tier Alarms (HH, H, L, LL with deadband hysteresis) and 32-bit bit-packed Status, Warning, Fault, and FDA Compliance Words.

2. Mandatory IEC 61131-3 Syntax & Parity:
   - Enclosed strictly in triple backticks with iec-st: ```iec-st ... ```
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - First line: FUNCTION_BLOCK FB_FoodBev_RetortAutoclave_SteamAirSterilization_Fo
   - Last line: END_FUNCTION_BLOCK
   - Bracketed physical engineering SI units on all I/O variables: [deg C], [bar], [mm], [m3/h], [RPM], [min], [s], [%].
   - Zero summaries, zero placeholders, zero truncation comments."""

    assistant_content = f"```iec-st\n{st_code}\n```"

    record_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{record_id}.json"

    data_payload = {
        "id": f"synthetic_foodbev_retort_{record_id}",
        "instruction": prompt_text,
        "input": "",
        "output": assistant_content,
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, ensure_ascii=False, indent=2)

    print(f"Generated dataset record saved to: {output_filename}")
    print(f"File size on disk: {os.path.getsize(output_filename):,} bytes")
    return output_filename

if __name__ == "__main__":
    fn = build_dataset()
