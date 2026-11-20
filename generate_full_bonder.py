# -*- coding: utf-8 -*-
"""
Generator for FB_Semiconductor_WireBonding_ThermoSonic_Sync
Dataset Target: data/swarm_raw/agent_41e92a8c.json
"""
import os, sys, json, re, math

USER_PROMPT = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair (V7 Max-Persona, 75+ years veteran industrial engineer).
Your mission is to generate a massive, ultra-rigorous, production-ready, fully unrolled IEC 61131-3 Structured Text dataset for heavy commercial manufacturing: Semiconductor Assembly & Advanced IC Packaging.

TARGET DOMAIN:
- Sector: Heavy Commercial Manufacturing - Semiconductor Assembly & Advanced IC Packaging
- System: High-Speed Automatic Thermo-Sonic Ball & Wedge Wire Bonder (35 um ultra-fine pitch, 18 wires/sec, EFO spark generator, piezoelectric ultrasonic transducer resonance tracking, voice-coil bond head force control)
- Function Block Name: FB_Semiconductor_WireBonding_ThermoSonic_Sync
- Target Output File: data/swarm_raw/agent_41e92a8c.json

CYBER-PHYSICAL MATHEMATICAL RIGOR & ARCHITECTURAL MANDATES:
1. Discrete State-Space Model (12 States, 4 Inputs, 6 Outputs):
   - 12 States: Bond head Z-position (um), Z-velocity (um/ms), voice coil current (mA), impact contact force (mN), ultrasonic transducer electrical impedance Z_us (Ohm), horn vibration amplitude (um), Free Air Ball (FAB) diameter (um), heated capillary tip temperature (deg C), leadframe substrate temperature (deg C), wire tail elongation strain (um/mm), wire loop apex height (um), capillary wear factor (dim).
   - 4 Inputs: Voice coil current drive command (mA), Ultrasonic generator power command (W), EFO spark discharge current (mA), Capillary heating element PWM duty cycle (%).
   - 6 Outputs: Measured bond head Z-position (um), Measured contact bond force (mN), Measured ultrasonic transducer impedance (Ohm), Measured ultrasonic vibration amplitude (um), Measured capillary tip temperature (deg C), Measured leadframe temperature (deg C).
   - Fully unrolled matrix update: x_{k+1} = A * x_k + B * u_k, y_k = C * x_k + D * u_k.
   - Discrete steady-state Kalman Filter: x_hat_{k|k} = x_hat_{k|k-1} + L * (y_meas - C * x_hat_{k|k-1}).
2. Model Predictive Control (MPC):
   - Unrolled 10-step horizon Projected Gradient Descent (PGD).
   - Quadratic stage cost: (x - x_ref)^T * Q * (x - x_ref) + u^T * R * u + delta_u^T * S * delta_u.
   - Explicit voice coil force slew rate and ultrasonic power saturation limits.
3. Triple Modular Redundant (TMR) 2oo3 Voting Logic:
   - 4 safety-critical channels: Capillary Z-Axis Optical Linear Encoder (ChA, ChB, ChC), Voice-Coil Piezoelectric Dynamic Impact Force Sensor (ChA, ChB, ChC), Leadframe Heated Vacuum Anvil Pyrometers (ChA, ChB, ChC), Ultrasonic Generator RF Phase/Current Pickoff (ChA, ChB, ChC).
   - Discrepancy timers (10ms), bumpless degradation to 1oo2, and fail-safe capillary retract on dual disagreement.
4. 14-Stage Production FSM:
   - CASE State OF:
     0: IDLE_SAFE_STANDBY
     1: LEADFRAME_INDEXING_VACUUM_CLAMP
     2: DUAL_CAMERA_PR_DIE_ALIGNMENT
     3: HIGH_VOLTAGE_EFO_SPARK_BALL_FORMATION
     4: RAPID_TRAVERSE_Z_SEARCH_TOUCHDOWN
     5: FIRST_BOND_DIE_PAD_THERMOSONIC_SCRUB
     6: CONTROLLED_WIRE_LOOPING_TRAJECTORY
     7: SECOND_BOND_LEAD_WEDGE_STITCH_FORMATION
     8: WIRE_CLAMP_PULL_TAIL_BREAK_OFF
     9: OPTICAL_POST_BOND_WIRE_INTEGRITY_CHECK
     10: LEADFRAME_UNCLAMP_INDEX_STEP
     11: EMERGENCY_CAPILLARY_LIFT_RECOVERY
     12: CALIBRATION_EFO_SPARK_ENERGY_TARE
     13: MANUAL_TEACH_SUPERVISORY_ALIGN
   - Fully detailed transitions, interlocks, timeout fault traps, and diagnostic tracking.
5. ANSI/ISA-18.2 Multi-Tiered Alarm Engine:
   - HH (Trip), H (Warning), L (Low Warning), LL (Low Trip) for all critical physical variables.
   - Configurable hysteresis deadbands, persistence timers, alarm suppression during startup, and bit-packed DWORD alarm registers.
6. 100% Exact Syntax & Parity:
   - Triple backticks with `iec-st`.
   - First line: FUNCTION_BLOCK FB_Semiconductor_WireBonding_ThermoSonic_Sync
   - Last line: END_FUNCTION_BLOCK
   - Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
"""

print("Prompt defined.")
