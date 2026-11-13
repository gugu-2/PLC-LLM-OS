# -*- coding: utf-8 -*-
import json
import uuid
import os
import subprocess

prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Automotive & Commercial Vehicle Manufacturing / Automated Robotic Paint Finishing
Function Block Name: FB_Automotive_Paint_RoboticElectrostatic_BellApplicator_Airflow

System Scope:
Automotive Exterior Robotic Paint Booth (Clearcoat / Basecoat Line, 65 jobs/hour). Coordinated regulation of high-speed electrostatic rotary bell cup atomizers (up to 70,000 RPM air turbine drive), 100 kV direct electrostatic cascade charging, dual shaping air ring aerodynamic shroud shaping (Inner Shaping Air SA1 for pattern width, Outer Shaping Air SA2 for atomization containment), positive-displacement micro-gear paint flow metering pump, downdraft air booth laminar velocity balance, and fast color-change solvent purge sequence.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Bell turbine rotational speed dynamic slip & bearing load [RPM]
   - Atomized paint droplet Sauter Mean Diameter (SMD d32) [um]
   - Electrostatic transfer efficiency [%] and space-charge cloud potential [kV]
   - Shaping air shroud pattern fan width [mm] and edge spray sharpness [N/m2]
   - Paint fluid delivery dynamic pressure [bar] and gear pump volumetric flow [cc/min]
   - Booth downdraft airflow laminar velocity [m/s] and relative humidity [% RH]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing bell air turbine drive air proportional valve [%], high-voltage cascade setpoint [kV], inner shaping air valve [%], outer shaping air valve [%], paint servo gear pump speed [RPM], and paint fluid pressure regulator [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Bell air turbine optical fiber frequency speed tachometers (Tach_Sensors: 1, 2, 3) [RPM]
   - Cascade high voltage divider feedback sensors (HV_Voltage: 1, 2, 3) [kV]
   - Cascade load current feedback transducers (HV_Current: 1, 2, 3) [uA]
   - Paint fluid Coriolis mass flow meters (Paint_Flow: 1, 2, 3) [cc/min]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_BOOTH_LAMINAR_VENTILATION_LOCK
   - 2: STATE_COLOR_FEED_LINE_PRESSURIZATION
   - 3: STATE_TURBINE_BEARING_AIR_LIFT_LOCK
   - 4: STATE_BELL_TURBINE_SPEED_RAMP_ACCEL
   - 5: STATE_SHAPING_AIR_AERODYNAMIC_SHROUD_ESTABLISH
   - 6: STATE_HIGH_VOLTAGE_RAMP_AND_LEAK_CHECK
   - 7: STATE_TRIGGER_PAINT_SPRAY_PRODUCTION_RUN
   - 8: STATE_DYNAMIC_PATH_CORNERING_OVERFLOW_COMPENSATION
   - 9: STATE_INTER_COAT_STANDBY_IDLE_HOLD
   - 10: STATE_HIGH_VOLTAGE_DECAY_AND_DISCHARGE
   - 11: STATE_RAPID_SOLVENT_PURGE_AND_COLOR_CHANGE
   - 12: STATE_TURBINE_DYNAMIC_BRAKING_DECEL
   - 13: STATE_EMERGENCY_HV_SPARK_DETECTED_FAST_SHUTDOWN
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

st_path = r"c:\Users\majip\Downloads\LLM REASEARCH\scratch\FB_Automotive_Paint_RoboticElectrostatic_BellApplicator_Airflow.st"
with open(st_path, "r", encoding="utf-8") as f:
    st_code = f.read()

assistant_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
target_json = f"data/swarm_raw/agent_{agent_id}.json"
with open(target_json, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully written to {target_json}")
print(f"Assistant Content Length: {len(assistant_content)} characters")
