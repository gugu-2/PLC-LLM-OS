# build_dataset.py
import sys
import os
import json
import uuid
import subprocess

from seat_foam_rim_builder.assemble import assemble_code

prompt_text = """You are a 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair operating under the V7 Max-Persona Protocol.

YOUR SOLE MISSION:
Synthesize an ultra-dense, mathematically complete, production-grade IEC 61131-3 Function Block dataset for Automotive Seat Foam Reaction Injection Molding (RIM):
`FB_Automotive_Interiors_SeatFoam_HighPressureRIM`

MANDATORY SPECIFICATIONS:
1. TARGET CODE DENSITY: 110,000 to 150,000+ characters of pristine, un-truncated IEC 61131-3 Structured Text. Zero summaries, zero placeholders, zero ellipsis comments (`// ... rest of code`).
2. ARCHITECTURAL REQUIREMENTS:
   - Discrete State-Space Matrices (6x6 A, B, C, D) for dual-component high-pressure hydraulic mixing & exothermic polyurethane polymerization kinetics: x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k.
   - Receding-Horizon Model Predictive Control (MPC) with 10 unrolled Projected Gradient Descent (PGD) iterations optimizing impingement mixing pressure [bar] and stoichiometric ratio R [1.05 +/- 0.01].
   - 2oo3 Triple Modular Redundancy (TMR) voting logic across 4 sensor channels: Polyol Coriolis mass flowmeter, Isocyanate Coriolis mass flowmeter, High-pressure hydraulic mix-head sensor, and Mold cavity infrared temperature sensor.
   - 14-Stage Production Finite State Machine (FSM):
     0: UNINITIALIZED, 1: CARROUSEL_HOMING_CALIBRATION, 2: MOLD_CARRIER_INDEXING, 3: RELEASE_AGENT_ROBOTIC_SPRAY, 4: WIRE_FRAME_INSERT_INSPECTION, 5: MOLD_HEATING_VACUUM_SEAL, 6: HIGH_PRESSURE_RECIRCULATION, 7: ROBOTIC_POURING_TILT_TRAJECTORY, 8: HIGH_PRESSURE_IMPINGEMENT_SHOT, 9: EXOTHERMIC_CURING_SUPERVISION, 10: MOLD_DEPRESSURIZATION_VENT, 11: MOLD_OPENING_DEMOLDING_ROBOT, 12: PART_WEIGHT_DENSITY_VERIFICATION, 13: E-STOP_VENT_PURGE.
   - ISA-18.2 Multi-Tier Alarms (HH, H, L, LL with deadband hysteresis) and 32-bit bit-packed telemetry registers.
3. PARITY GUARANTEE:
   - 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;, every WHILE has END_WHILE;. First line `FUNCTION_BLOCK FB_Automotive_Interiors_SeatFoam_HighPressureRIM`, last line `END_FUNCTION_BLOCK`.
   - SI engineering units on all I/O variables."""

code = assemble_code()
assistant_content = f"```iec-st\n{code}\n```"

record = {
    "instruction": prompt_text,
    "input": "",
    "output": assistant_content,
    "messages": [
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": assistant_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
target_file = f"data/swarm_raw/agent_{agent_id}.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Generated and saved dataset to {target_file}")
print(f"Assistant content character count: {len(assistant_content)}")
print(f"Raw Structured Text character count: {len(code)}")

# Validate with validate_iec.py
res = subprocess.run([sys.executable, "validate_iec.py", target_file], capture_output=True, text=True)
print(res.stdout)
if res.returncode != 0:
    print("VALIDATION ERROR:", res.stderr)
    sys.exit(1)
else:
    print(f"FILE {target_file} VALIDATION SUCCEEDED!")
