# -*- coding: utf-8 -*-
"""
Builder and validator for FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum
Generates a complete, ultra-dense, mathematically rigorous IEC 61131-3 dataset.
"""

import sys
import os
import json
import uuid
import re

# Import workspace validator directly
import validate_iec

def create_dataset():
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electronics SMT & Semiconductor Packaging (Tier 1 Priority Sector): High-Precision 14-Zone Convection Reflow Soldering Oven with Closed-Loop Nitrogen Inerting (< 35 ppm O2), Dual-Chamber Gas Seals, Dual-Lane Conveyor Speed Synchronization & Thermal Load Feedforward, 14-Zone Cascade PID Heating with Multi-Thermocouple Delta-T Thermal Shock Protection, and Integrated Vacuum Voiding Chamber (< 1% BGA/QFN Solder Voiding) with Controlled Pressure Ramp Rate.**

**Function Block Name**: `FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum`

**Engineering Context & Operational Architecture**:
1. Convection Tunnel & 14-Zone Cascade Thermal Control:
   - 14 independently controlled upper and lower heating plenums (28 heat cells) with variable frequency convection impellers.
   - First-principles forced convection Nusselt/Reynolds heat transfer modeling, multi-layer PCBA thermal capacitance absorption dynamics, and multi-thermocouple Delta-T thermal shock protection (max heating rate +2.0 °C/s, max cooling rate -3.5 °C/s).
   - SAC305 lead-free profile tracking: 140-190 °C flux activation soak, 217 °C liquidus crossing, 245 °C peak reflow, and 60-75 s Time Above Liquidus (TAL).
2. Closed-Loop Liquid Nitrogen (N2) Inerting & Dual Gas Seals:
   - High-purity N2 continuous blanket maintaining residual atmospheric oxygen < 35 ppm O2 (target 15 to 25 ppm) across soak and reflow zones to minimize solder paste oxidation and eliminate Head-in-Pillow (HIP) defects.
   - Dual-chamber entrance and exit labyrinth gas curtains with dynamic exhaust damper differential pressure balance (+0.25 mbar internal tunnel overpressure) preventing cleanroom air ingress.
   - 2oo3 Triple Modular Redundancy (TMR) Zirconia (ZrO2) solid-state electrochemical potentiometric O2 sensors with automatic electrode fouling drift compensation.
3. Integrated Deep Vacuum Solder Voiding Chamber:
   - Positioned immediately between Peak Reflow (Zone 11) and Controlled Cooling (Zone 12).
   - Pneumatic hermetic sealing gate valves, roots booster dry vacuum pump package, and dual capacitance manometers (2oo3 TMR).
   - Controlled sub-millibar evacuation ramp down to 15 mbar while solder is molten, extracting entrapped volatile flux gases from BGA/QFN joints to achieve < 1.0% void area per IPC-7095 Class 3, followed by a controlled N2 backfill ramp.
4. Dual-Lane Dynamic Speed Synchronization & Board Mass Feedforward:
   - Lane 1 and Lane 2 independent mesh belt pin chain servos with optical tachometers (2oo3 TMR).
   - Thermal load feedforward computing incoming board mass flow and substrate layer count to pre-compensate zone heating duty cycles before convective thermal dip.
5. 8-State Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E d_k$):
   - 8 states: Mean preheat bulk gas temp (Z1-Z4), Mean soak plateau bulk gas temp (Z5-Z8), Mean peak reflow bulk gas temp (Z9-Z11), Mean cooling bulk gas temp (Z12-Z14), PCBA core absorbed temperature, Internal residual O2 concentration, Vacuum chamber absolute pressure, and Tunnel differential pressure vs ambient.
   - 8 control inputs: Zone group heater PWM duties, cooling N2 valve, main N2 purge valve, labyrinth seal trim, vacuum throttle, and vacuum N2 backfill valve.
6. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) with physical box saturation and dynamic slew rate limiters.
7. Deterministic 14-Stage Production Finite State Machine (FSM):
   - From initial N2 purge, O2 stabilization, cascade heating ramp, soak equilibration, dual-lane infeed sync, active convection reflow, vacuum chamber transfer, pumpdown degassing, N2 backfill, cooling outfeed, to recipe transitions and thermal abort.
8. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance hysteresis and 32-bit status/diagnostic words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    return user_prompt

if __name__ == "__main__":
    print("Test prompt created")
