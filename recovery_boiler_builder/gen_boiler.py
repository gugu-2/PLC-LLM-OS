# recovery_boiler_builder/gen_boiler.py
"""
Lumina Swarm Synthetic Data Architect - Generator for:
COMMERCIAL INDUSTRIAL SECTOR: Heavy Pulp & Paper Manufacturing / Chemical Recovery Islands
SYSTEM: Kraft Pulp Mill High-Pressure Chemical Recovery Boiler & Smelt Dissolving Island
FUNCTION BLOCK: FB_Paper_Kraft_RecoveryBoiler_BlackLiquor_Combustion
OUTPUT: data/swarm_raw/agent_4c2019ea.json
"""

import sys
import os
import json
import re

def build_prompt():
    return """You are a veteran Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona) specializing in heavy chemical pulp & paper manufacturing, Kraft recovery cycles, high-pressure chemical recovery boilers, and smelt dissolving tank operations.

YOUR MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Structured Text dataset row for:
**Heavy Pulp & Paper Manufacturing: Kraft Pulp Mill High-Pressure Chemical Recovery Boiler & Smelt Dissolving Island (Combustion of Concentrated Black Liquor at 80% Dry Solids, 3-Tier Staged Combustion Air for Total Reduced Sulfur TRS Suppression, Char Bed Temperature & Reduction Efficiency Optimization, Smelt Spout Water-Cooled Shatter Jets, Green Liquor TTA Density Closed Loop, Rapid Emergency Drain System REDS Acoustic Water Leak Interlock)**
Function Block Name: FB_Paper_Kraft_RecoveryBoiler_BlackLiquor_Combustion
Target File: data/swarm_raw/agent_4c2019ea.json

SPECIFICATIONS & REQUIREMENTS:
1. Target Character Length: 55,000 to 85,000+ characters for the IEC 61131-3 ST output. Zero placeholders, zero summaries, zero truncation comments like '// ... rest of code'. Every single state, matrix, loop, and formula must be completely unrolled and coded.
2. Technical Cyber-Physical Depth:
   - Kraft chemical recovery boiler with heavy black liquor firing system (multi-oscillator liquor spray nozzles, 75-82% dry solids, 115-135 deg C firing temp, 1.8-3.5 bar header pressure), bottom furnace char bed, 3-tier combustion air (Primary 40%, Secondary 35%, Tertiary 25%), superheater/boiler bank/economizer passes, smelt spouts with high-pressure medium-pressure steam shatter jets, and smelt dissolving tank with green liquor recirculation and weak wash density control.
   - Discrete State-Space Model (16x16 state matrix A, 16x8 B, 8x16 C, 8x8 D) modeling black liquor droplet flight, drying, devolatilization, and char bed combustion kinetics, sodium/sulfur inorganic smelt reduction efficiency (Na2SO4 + 2C -> Na2S + 2CO2), char bed temperature (950 deg C to 1,050 deg C), 3-tier staged air distribution, flue gas CO / O2 / TRS (Total Reduced Sulfur, H2S, methyl mercaptan) emission dynamics, and dissolving tank Total Titratable Alkali (TTA) density dynamics. Fully explicit unrolled matrix-vector state propagation: x_{k+1} = A*x_k + B*u_k.
   - Receding-horizon MPC for multivariable control of black liquor header pressure (bar), liquor temperature trim (deg C), primary/secondary/tertiary air damper positions (%), shatter jet steam pressure (bar), and dissolving tank weak wash flow rate (m3/h) to maintain reduction efficiency > 92.5%, lower bed temperature in safe operating window, dissolving tank density at setpoint (115-125 g/L Na2O equivalent TTA), and stack TRS < 5.0 ppm.
   - 2oo3 Triple Modular Redundancy (TMR) voting across:
     (1) Lower furnace char bed optical infrared pyrometers (3 sensors),
     (2) Acoustic leak detection sensor array for boiler pressure part water/steam leaks into furnace (3 channels),
     (3) Flue gas TRS emission analyzers (3 channels), with discrepancy timers, fault latches, and bumpless degradation.
   - 12-Stage Operational FSM:
     Stage 0: IDLE / COLD_STANDBY
     Stage 1: NFPA 85 PRE_PURGE & ID FAN DRAFT BALANCING
     Stage 2: AUXILIARY GAS/OIL WARM_UP BURNER FIRING
     Stage 3: CHAR BED REFRACTORY BASE ESTABLISHMENT & SOAK
     Stage 4: HEAVY BLACK LIQUOR HEADER CIRCULATION & FIRING TRANSITION
     Stage 5: 3_TIER STAGED COMBUSTION AIR PACING
     Stage 6: STEADY_STATE CHEMICAL RECOVERY & SMELT REDUCTION OPTIMIZATION
     Stage 7: GREEN LIQUOR DENSITY & WEAK WASH STABILIZATION
     Stage 8: SOOTBLOWER SEQUENTIAL STEAM LANCING & HEAT TRANSFER BALANCE
     Stage 9: LIQUOR GUN MECHANICAL OSCILLATION & PORT RODDER CLEANOUT
     Stage 10: AUXILIARY FUEL CO_FIRING & HIGH-LOAD TRIM
     Stage 11: CONTROLLED CHAR BED BURN_DOWN & BOILER BOTTLING
     Stage 12: SIL-3 RAPID EMERGENCY DRAIN SYSTEM (REDS) SMELT-WATER EXPLOSION TRIP
   - Smelt spout water-cooled jacket temperature monitoring and steam shatter jet acoustic feedback (preventing smelt run-away pool explosions).
   - ISA-18.2 multi-tiered alarm matrix with bit-packed telemetry DWORDs (dwAlarmWord_1, dwAlarmWord_2, dwTMR_Diagnostic_1, dwSystemStatusWord), tracking acoustic tube leak detection (immediate REDS actuation to avoid catastrophic smelt-water steam explosion), stack TRS exceedance (> 10 ppm), char bed blackout risk (< 900 deg C), smelt spout freezing / pluggage, and dissolving tank violent steam hammer vibration.
3. Strict Syntax & AST Parity:
   - Enclose the Structured Text in TRIPLE BACKTICKS with iec-st:
   ```iec-st
   FUNCTION_BLOCK FB_Paper_Kraft_RecoveryBoiler_BlackLiquor_Combustion
   ...
   END_FUNCTION_BLOCK
   ```
   - 100% exact matching parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;.
   - Ensure comments do not accidentally close prematurely.
4. Dataset File Format:
   Save to data/swarm_raw/agent_4c2019ea.json in JSON format:
   {"messages": [{"role": "user", "content": "..."}, {"role": "assistant", "content": "```iec-st\\n...\\n```"}]}
5. Self-Validation:
   Execute python validate_iec.py data/swarm_raw/agent_4c2019ea.json to verify that AST parity and code fences are 100% valid."""

print("Prompt builder ready.")
