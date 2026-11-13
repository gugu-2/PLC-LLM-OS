# build_semiconductor_dataset.py
# Lumina IEC 61131-3 Generator for High-NA Semiconductor Lithography Wafer Stage
import os
import json
import uuid
import re

def generate_prompt():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Semiconductor Lithography & Advanced Mechatronics (Tier 1 Priority Sector)**
**Function Block Name: `FB_Semiconductor_Lithography_WaferStage_NanometerPositioning`**
**Target System**: High-NA EUV Photolithography Dual-Wafer Stage (TwinScan Architecture), 6-DOF Magnetic Levitation (MagLev) Lorentz Actuator Array (X, Y, Z, Rx, Ry, Rz), Heterodyne Laser Interferometer Position Feedback (sub-0.1 nm resolution), Dynamic Counter-Mass Reaction Force Momentum Balance (15g acceleration, 150 m/s2), Wafer Electrostatic Chuck (ESC) Bipolar Clamp Force & Thermal Helium Backside Cooling (sub-millikelvin regulation), and Grazing-Incidence Laser Focus/Leveling Grid.

**Mandatory Architectural Requirements**:
1. Mathematical Cyber-Physical Rigor:
   - Explicit Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) at Ts = 1 ms modeling 6-DOF rigid body kinematics, mirror block high-frequency structural bending resonances (450 Hz, 820 Hz, 1250 Hz), Lorentz actuator back-EMF, and wafer chuck helium backside thermal expansion.
   - Model Predictive Control (MPC) / Projected Gradient Descent (PGD) unrolled solver to optimize 6-DOF Lorentz coil currents, minimizing wafer scanning overlay error (3-sigma < 1.2 nm) during 15g scanning acceleration ramps and directional reversals.
   - 2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) voting across critical sensor channels (Multi-Axis Laser Interferometers, Capacitive Fine Gap Sensors, Optical Chuck Alignment Sensors, Backside Helium Pressure Transducers) with bumpless degradation and discrepancy timers.
   - ISA-18.2 Alarm Engine with bit-packed DWORD alarm words, deadband hysteresis, priority escalation, and laser interferometer fringe-slip / MagLev coil over-temperature emergency trips.
   - Deterministic 14-Stage FSM for Stage Homing & Laser Interferometer Mirror Calibration, Electrostatic Chuck Pre-Charge, Wafer Robot Load Transfer, Bipolar ESC Clamping & He Pressure Build-up, Global Wafer Alignment Mark Scan, Focus/Leveling Surface Map Ingestion, High-Speed Exposure Scan Synchronization with Reticle Mask, Step-and-Scan Field Indexing, TwinScan Dual Stage Exchange Handshake, ESC Depolarization & He Vent, Wafer Robot Unload Permissive, Thermal Mirror Drift Calibration, Laser Fringe-Slip Recovery, and Severe Collision Magnet Failsafe Drop.

2. Strict IEC 61131-3 Syntax & Parity:
   - TRIPLE backticks with iec-st: ```iec-st
   - 100% exact delimiter parity: IF/END_IF, CASE/END_CASE, FOR/END_FOR, FUNCTION_BLOCK/END_FUNCTION_BLOCK.
   - Every input/output variable must include physical SI engineering units in brackets: [nm], [um], [m/s], [m/s2], [N], [A], [V], [mbar], [mK], [deg C], [ms], [bool], [enum], [%].
   - ZERO placeholders, ZERO ellipses, ZERO truncated matrices.

Generate the complete, fully implemented Function Block code."""
    return prompt

print("Prompt generator defined.")
