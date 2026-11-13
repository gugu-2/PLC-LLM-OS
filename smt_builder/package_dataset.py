# -*- coding: utf-8 -*-
"""
smt_builder/package_dataset.py
Assembles the complete IEC 61131-3 dataset, packages into JSON, saves to data/swarm_raw/,
and runs validate_iec.py to confirm 100% verification pass.
"""

import os
import sys
import json
import uuid
import subprocess

# Ensure paths
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("smt_builder"))

from test_assemble import assemble_st

PROMPT = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Electronics Manufacturing & High-Speed SMT Automation (Tier 1 Priority Sector): High-Speed Dual-Gantry Surface Mount Technology (SMT) Pick-and-Place Machine, featuring a 16-spindle rotary placement head, on-the-fly fly-by optical vision component alignment, dynamic vacuum sensing (-85 kPa) and calibrated pneumatic puff blow-off release, multi-point Invar/Zerodur optical linear scale thermal expansion compensation, and multi-axis coordinated S-curve motion control with vibration dampening.**

**Function Block Name**: `FB_Electronics_SMT_HighSpeed_PickAndPlace_VisionMotion`

**Engineering Context & Operational Architecture**:
1. Dual-Gantry Linear Motor Kinematics & Resonant Flexure Vibration Dampening:
   - Co-planar dual-drive linear motor tracks for X-axis (X1/X2) and ironless crossbeam Y-axis with active yaw compensation.
   - Moving mass 42.5 kg, translational acceleration up to 50.0 m/s^2 (5.1 g), jerk limit 500.0 m/s^3.
   - Two-mass resonant flexible body model (carriage mass vs tool-center-point TCP mass) with stiffness K_flex = 2.45E7 N/m and damping C_flex = 820.0 N*s/m.
2. 16-Spindle Revolving Star Turret Head & Independent Voice-Coil Z-Axis Mechanics:
   - 16 identical spindles arranged radially on a revolving drum turret indexed by direct-drive torque motor.
   - Individual voice-coil linear actuators per spindle for frictionless, low-inertia Z-motion (0 to 30 mm stroke) with closed-loop programmable soft-touch landing force (0.5 to 8.0 N) preventing die micro-cracking.
   - Individual direct-drive hollow-shaft theta motors for continuous 360 deg rotational alignment.
3. On-the-Fly Fly-By Optical Vision Inspection & Dynamic Offset Injection:
   - GigE CMOS area-scan vision camera with ultra-fast pulsed LED strobes (1.5 to 3.0 us) triggered by hardware Position Event Verification (PEV) encoder match at flight speeds up to 2.5 m/s.
   - Sub-pixel centroid offset (dX, dY), rotational skew (dTheta), lead coplanarity, and silicon defect detection dynamically injected into servo loops.
4. Dynamic Piezoresistive Vacuum Sensing & Micro-Blow-Off Release:
   - Dynamic piezoresistive pressure transducer per spindle monitoring suction chamber vacuum (-85 kPa nominal).
   - Tombstone / partial seal detection (-20 to -52 kPa) and pick failure classification (> -20 kPa).
   - High-speed positive-pressure puff blow-off pulse (+45 kPa, 6.0 ms) neutralizing electrostatic cling without disturbing wet solder paste.
5. Multi-Point Optical Linear Scale Thermal Gradient Expansion Compensation:
   - Invar and Zerodur scales with PT100 RTDs measuring X1, X2, Y, and spindle drum temperatures.
   - First-principles thermal expansion model with dynamic gradient compensation applied every cycle.
6. 10-State Cyber-Physical Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k] + L*e at Ts = 1.0 ms):
   - 10 states: Carriage position, Carriage velocity, TCP flexure vibration displacement, TCP flexure velocity, Spindle rotation angle, Spindle angular velocity, Vacuum chamber pressure, Vacuum acoustic flow, Gantry yaw angle, and Thermal expansion strain.
   - 4 control inputs: Gantry X force, Gantry Y force, Spindle Theta torque, and Vacuum proportional valve command.
   - 6 measurement outputs with full Luenberger observer innovation gain matrix.
7. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized over Np = 5 horizon via unrolled PGD solver with hard box constraints and jerk-bounded slew rate limiters.
8. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - 5 critical sensor triplets (Gantry X linear encoders, Gantry Y linear encoders, Spindle Theta encoders, Vacuum manifold pressure transducers, and Laser PCB warpage gauges) with discrepancy timers and bumpless degradation.
9. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Homing/Self-test, PCB conveyor infeed & clamp, Global optical fiducial alignment, Laser warpage surface mapping, Feeder bank approach, Voice-coil touch pick, Vacuum decay verify, Fly-by vision strobe capture, Offset transformation, High-speed flight, Precision landing, Blow-off release, Defect reject discharge, Nozzle tool exchange, and E-Stop controlled stop.
10. ISA-18.2 Multi-Tier Alarms & Bit-Packed Status Words:
   - High-High, High, Low, Low-Low threshold evaluation with deadband hysteresis, priority escalation, and 32-bit status, alarm, and diagnostic telemetry words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Electronics_SMT_HighSpeed_PickAndPlace_VisionMotion` with zero placeholders, complete state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm engine."""

def package_and_validate():
    st_code = assemble_st()
    assistant_content = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": PROMPT},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    unique_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{unique_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Dataset successfully saved to: {filename}")
    print(f"Assistant content character length: {len(assistant_content)}")
    print(f"Raw ST code length: {len(st_code)}")
    
    # Run validate_iec.py
    cmd = [sys.executable, "validate_iec.py", filename]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validator STDOUT:")
    print(res.stdout)
    if res.stderr:
        print("Validator STDERR:")
        print(res.stderr)
        
    if res.returncode == 0:
        print(f"===> 100% VERIFICATION PASSED for {filename} <===")
        return filename, len(assistant_content), True
    else:
        print(f"===> VALIDATION FAILED (exit code {res.returncode}) <===")
        return filename, len(assistant_content), False

if __name__ == "__main__":
    package_and_validate()
