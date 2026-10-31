# -*- coding: utf-8 -*-
import json
import os
import sys

# User prompt matching exactly the V7 persona
user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Automated Multi-Level Mechanical Parking Systems (APS Shuttles): FB_AutomatedParking_MultiLevel_ShuttleHoist - Vertical Traction Hoist Dynamics, Counterweight Cable Elasticity Vibration, Laser-Guided Horizontal Shuttle Acceleration, Jerk-Limited S-Curve Profiling, Sub-Millimeter Floor Leveling Alignment, Regenerative Braking Energy Capture, 2oo3 TMR Optical Laser Distance & Rotary Encoders, SIL 3 Pallet Transfer FSM, and ISA-18.2 Multi-Tiered Safety Matrix**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_AutomatedParking_MultiLevel_ShuttleHoist
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [mm], [m/s], [m/s2], [m/s3], [kg], [kN], [deg C], [V], [A], [kW], [bar])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 45,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_AutomatedParking_MultiLevel_ShuttleHoist
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Automated Multi-Level Mechanical Parking Systems (APS Shuttles)"""

print("Writing parts...")
