# Saver script for Paper Machine Dataset
import os
import sys
import json
import uuid

# Ensure local imports work
sys.path.insert(0, os.path.dirname(__file__))
from assemble_test import assemble

def save():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.

DOMAIN & SPECIFICATION:
- Commercial Industry: Pulp, Paper & Continuous Web Converting (Tier 1 Priority Sector)
- Target Automation System: 1,800 m/min Multi-Ply Fourdrinier High-Speed Paper Machine
  - Hydraulic headbox jet-to-wire velocity ratio (J/W) cascade & 48-zone slice lip micro-actuator cross-direction (CD) basis weight profiling
  - Multi-cylinder cascade steam drainage & thermocompressor differential pressure drying optimization
  - In-line beta-gauge basis weight, microwave moisture, and laser caliper continuous scanner frame synchronization
  - Sectional multi-motor drive web tension load cell draw-ratio speed control and dry-end calendar nip roll hydraulic crown compensation
- Function Block Name: FB_Paper_Fourdrinier_Headbox_MoistureCDProfile

QUALITY DIRECTIVES:
1. First-Principles Cyber-Physical Formulation:
   - 8-State discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at Ts = 10 ms for headbox stock pressure/consistency, wire speed, dry-line position, moisture percentage, dry basis weight, steam dryer header pressure, and web draw tension.
   - Receding-horizon Model Predictive Control (MPC) with multi-objective quadratic cost functional (Q, R, S, P), projected gradient descent (PGD) with physical actuator box saturation and dynamic slew rate limiters.
   - 2oo3 Triple Modular Redundancy (TMR) voting across 7 critical sensor channels (headbox total head transmitters, stock consistency optical sensors, wire section speed encoders, scanner beta-radiation basis weight probes, microwave moisture sensors, tension load cells, steam dryer header pressure) with discrepancy timers and bumpless degradation.
   - 48-zone cross-direction (CD) basis weight slice lip micro-actuator profiling algorithm with spatial smoothing FIR filter, parabolic web shrinkage compensation, anti-windup PI control, and mechanical upper slice lip bending limit interlocks.
   - Deterministic 14-stage operational Finite State Machine (CASE eCurrentFsmState OF ... END_CASE) covering wire washup, headbox stock pressurization, jet-to-wire sync, couch vacuum seal, press section nip loading, dryer group steam warmup, paper tail threading, full sheet widening, scanner profiling loop lock, calender crown compensation, reel drum turnup, and wet/dry-end sheet break auto-dump recovery.
   - ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL) with clearance deadbands and bit-packed DWORD status/diagnostic words.
   - Physical engineering units in brackets for all I/O variables: [m/min], [g/m2], [%], [kPa], [bar], [kN/m], [N/m], [um].
2. Code Completeness & Parity:
   - Zero summaries, zero placeholders, zero ellipses, every equation and state transition fully coded.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - First line: FUNCTION_BLOCK FB_Paper_Fourdrinier_Headbox_MoistureCDProfile, Last line: END_FUNCTION_BLOCK."""

    raw_code = assemble()
    assistant_content = f"```iec-st\n{raw_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "swarm_raw")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to: {filename}")
    print(f"Assistant content character count: {len(assistant_content)}")
    return filename

if __name__ == "__main__":
    fn = save()
