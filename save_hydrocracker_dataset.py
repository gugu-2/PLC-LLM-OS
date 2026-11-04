# -*- coding: utf-8 -*-
"""
Save script for Hydrocracker dataset
"""

import os
import sys
import uuid
import json

sys.path.insert(0, "scripts/hydrocracker_builder")
from assemble_and_validate import assemble_st

def generate_and_save():
    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Petrochemicals & Heavy Chemical Refining (Tier 1 Global High-Demand Industrial Automation) - High-Pressure Catalytic Hydrocracker & Fractionation Reactor Complex (180 bar operating pressure, 420°C reaction temperature): 4-Bed Fixed Trickle-Bed Hydroprocessing Reactor with Multi-Point Hydrogen Quench Gas Injection (Dynamic exotherm suppression, bed delta-T runaway protection > 15°C/min with automatic emergency depressurization slam-shut valves), High-Pressure Gas-Liquid Separator (Cold/Hot High-Pressure Separators with nuclear level gauges and dual letdown valves), Sour Gas Amine Absorption Scrubber (Closed-loop H2S stripping with rich/lean amine circulation), and Atmospheric Fractionation Column (Dynamic reflux ratio and furnace reboiler heat integration for naphtha, diesel, and heavy gas oil cuts).**

Task: Implement the production-grade Function Block FB_Chemicals_Hydrocracker_TrickleBed_HydrogenQuench governing:
1. Discrete State-Space Matrices (A, B, C, D) capturing 4-bed catalyst zone temperatures, hydrogen quench mass flow rate, reactor overall differential pressure, separator liquid levels, amine absorber H2S concentration, column reboiler duty, and fractionation overhead vapor pressure: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost approximation penalizing catalyst bed peak temperature overshoot (Q), hydrogen quench control valve slew rate (R), and separator letdown valve pressure drop deviation (P).
3. 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on multi-point multipoint thermocouple assemblies (MTA), high-pressure separator nuclear level transmitters, and reactor inlet/outlet differential pressure cells.
4. Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change > 15°C/min) with hysteresis and 32-bit packed diagnostic alarm words.
5. Deterministic 12-Stage Finite State Machine covering Inert Nitrogen Purge & Leak Tightness Test, Hydrogen Circulation & Catalyst Sulfiding Pre-Heat, Hydrocarbon Feed Cut-In & Low-Rate Wetting, Exotherm Detection & Quench Gas Flow Calibration, Full Load Hydrocracking Run, Amine Treating Absorption Balancing, Fractionation Cut Separation, Bed Temperature Rate-of-Change Runaway Trip, High-Pressure Emergency Depressurization (Blowdown to Flare), Catalyst Hydrogen Stripping, Controlled Nitrogen Cooldown, and Cold Idle Safe Hold.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = assemble_st()
    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "id": f"agent_{agent_id}",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"Saved dataset to {filename}")
    print(f"Assistant code length: {len(assistant_content)} characters")
    return filename

if __name__ == "__main__":
    fn = generate_and_save()
