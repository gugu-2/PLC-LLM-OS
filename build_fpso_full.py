# Python script to build the complete FPSO Topside Gas Compression & TEG Dehydration dataset
import json
import uuid
import os
import sys

def build():
    # Prompt text
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Offshore Oil & Gas Floating Production (FPSO Topside Facilities, Tier 1 Priority): FPSO Topside 3-Stage Centrifugal Gas Compression Train (60 MW Variable Speed Drive, 250 bar export pressure), Anti-Surge Closed-Loop Recycle Valve Cascade (< 1.2 s stroke), Triethylene Glycol (TEG) High-Pressure Absorption Contactor Tower & Stripping Reboiler Still Column, Molecular Sieve Moisture Tracking, Marine Hull 6-DOF Pitch/Roll Wave Motion Decoupling, and SIL-3 Emergency Depressurization (EDP) to Flare.**

**Function Block Name**: `FB_OilGas_FPSO_TopsideGasCompression_TEGDehydration`

**Engineering Context & Operational Architecture**:
1. FPSO Topside 3-Stage Centrifugal Compression Train (60 MW VFD, 250 bar export):
   - Multi-stage barrel centrifugal compressor driven by high-voltage 60 MW variable frequency drive motor.
   - Stage 1: 25 bar suction to 62 bar intermediate discharge; Stage 2: 60 bar suction to 135 bar; Stage 3: 132 bar to 250 bar export pipeline injection.
   - Polytropic head thermodynamic equations based on real gas compressibility factor Z and polytropic efficiency.
2. Anti-Surge Closed-Loop Recycle Valve Cascade (< 1.2 s full stroke):
   - Dedicated fast-acting pneumatic/hydraulic anti-surge recycle valves with fail-open geometry across each stage.
   - Dynamic Surge Limit Line (SLL) and Surge Control Line (SCL) calculation: Ss = DeltaP_orifice / (K_surge * (P_d - P_s)).
   - Dynamic surge safety margin bias tracking negative volumetric flow derivatives (dF/dt) and vessel pitch/roll dynamic acceleration.
3. Triethylene Glycol (TEG) High-Pressure Absorption Contactor & Stripping Reboiler:
   - High-pressure countercurrent contactor tower operating at 130 bar dehydrating wet hydrocarbon gas to export pipeline specification (moisture <= 30 ppmv).
   - Rich glycol regenerator with stripping gas column, reboiler at 204 °C, monitoring thermal degradation limits and glycol circulation ratios.
4. Marine Hull 6-DOF Pitch/Roll Wave Motion Decoupling:
   - Floating production platform 6-DOF dynamic inertial acceleration (roll, pitch, heave) decoupled from liquid-gas separation and contactor tray hydraulics.
   - Dynamic compensation for contactor liquid sloshing, scrubber mist carryover risk, and compressor shaft gyroscopic precession bearing loads.
5. 6-State Cyber-Physical Discrete State-Space Model (x[k+1] = A x[k] + B u[k] + Ew w[k]):
   - States: Suction pressure deviation, Discharge pressure deviation, Mass flow rate deviation, Shaft speed deviation, TEG moisture loading deviation, Recycle header pressure deviation.
   - Inputs: Stage 1 Anti-Surge Valve demand [%], Stage 2 Anti-Surge Valve demand [%], Stage 3 Anti-Surge Valve demand [%], VFD Speed Reference deviation [rpm].
   - Disturbances: Pipeline backpressure fluctuation, Wave heave acceleration, Feed gas moisture saturation.
   - Full Luenberger state observer / Kalman filter correction.
6. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent:
   - Multi-objective quadratic cost functional (Q, R, S, P) over prediction horizon Np = 5.
   - Asymmetric barrier penalty for surge line proximity to guarantee Ss >= 1.10.
   - Strict actuator slew rate limiters (83.3 %/s for anti-surge valves) and box constraints.
7. 2oo3 Triple Modular Redundant (TMR) Sensor Voting:
   - Suction Pressure PT-101A/B/C [bar].
   - Discharge Pressure PT-201A/B/C [bar].
   - Venturi Orifice Differential Pressure PDT-301A/B/C [mbar].
   - Drive-End Shaft Radial Vibration Probes VT-401A/B/C [um].
   - Export Gas Moisture Analyzers AT-501A/B/C [ppmv].
   - Pairwise discrepancy tolerance checking, time integration, channel isolation, and graceful 3->2->1->0 degradation.
8. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stage 10: STATE_NITROGEN_INERT_TEST
   - Stage 20: STATE_LUBEOIL_SEALGAS_LOCK
   - Stage 30: STATE_VFD_WARMUP_INCH
   - Stage 40: STATE_HC_INFEED_PURGE
   - Stage 50: STATE_ANTISURGE_PRIME_OPEN
   - Stage 60: STATE_HP_COMPRESSION_RAMP
   - Stage 70: STATE_TEG_CIRCULATION_LOCK
   - Stage 80: STATE_EXPORT_SYNC_BALANCE
   - Stage 90: STATE_NORMAL_EXPORT_MPC
   - Stage 100: STATE_QUENCH_TURNDOWN_RECYCLE
   - Stage 110: STATE_WAVE_CHOKE_DAMPENING
   - Stage 120: STATE_DERATE_HOT_RECYCLE_IDLE
   - Stage 130: STATE_SIL3_EMERGENCY_DEPRESS
   - Stage 140: STATE_SAFE_MECHANICAL_TRIP
9. ISA-18.2 Multi-Tier Alarms & 32-Bit Bit-Packed Telemetry:
   - Critical SIL-3 trip interlocks, high/low warnings, deadband hysteresis, and DWORD telemetry registers.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_OilGas_FPSO_TopsideGasCompression_TEGDehydration` with zero placeholders, complete state-space matrices, unrolled MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""
    return prompt

print("Prompt builder ready.")
