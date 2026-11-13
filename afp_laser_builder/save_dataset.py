# Saver and Validator for FB_Aerospace_Composite_AFP_LaserCompaction
import os
import json
import uuid
import sys
sys.path.insert(0, os.path.abspath("."))
sys.path.insert(0, os.path.abspath("afp_laser_builder"))
from test_gen import generate_st_code
from validate_iec import validate_json_file

def save_and_validate():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Aerospace, Defense & Advanced Composites Manufacturing (Tier 1 Priority Sector): Automated Fiber Placement (AFP) 8-Axis Robotic Cell for CFRP Aircraft Wing/Fuselage Skins, featuring multi-tow (16 to 32 tows) carbon fiber prepreg dynamic feed, cut, clamp, and add mechanism, high-power continuous diode laser compaction heating (12 kW, 980 nm) with dual optical thermal cameras & surface emissivity compensation, compliant segmented silicone compaction roller (60 Shore A) with multi-axis pneumatic force balancing (0 to 3,000 N), in-line optical coherence / laser triangulation defect inspection (gaps, overlaps, tow twist, bridging), and dynamic prepreg tow tension control.**

**Function Block Name**: `FB_Aerospace_Composite_AFP_LaserCompaction`

**Engineering Context & Operational Architecture**:
1. Multi-Tow Dynamic Feed, Cut, Clamp & Creel Payout Management:
   - Dynamic handling of up to 32 independent carbon prepreg tows (1/4 inch / 6.35 mm width) fed from temperature- and humidity-controlled creel enclosure.
   - Ultra-fast pneumatic guillotine anvil cutting (< 45 ms stroke) and high-speed stepper capstan feed insertion (< 65 ms handover) for on-the-fly ply boundary tailoring.
   - Magnetic particle brake tension regulation across all 32 spools preventing web slackness, tow snap, or prepreg twist.
2. High-Power Diode Laser Compaction Heating & Optics Homogenization:
   - 12.0 kW continuous diode laser bank (980 nm) with multi-zone variable spot zoom homogenizer optics impinging at prepreg/mandrel nip point.
   - First-principles transient 2D thermal conduction (Eulerian moving coordinate frame) and Beer-Lambert anisotropic absorption.
   - Dynamic surface emissivity compensation as a function of instantaneous prepreg consolidation temperature, ply fiber direction, and laser incidence angle.
   - Dual pyrometric optical thermal cameras and deionized water chiller flow interlocks (SIL-3 laser safety shutter snap shut < 15 ms).
3. Compliant Segmented Silicone Compaction Roller Mechanics:
   - 8-segment silicone elastomer roller (60 Shore A, E = 3.8 MPa) providing compliant contact across complex curved wing skin aerodynamic profiles.
   - Hertzian viscoelastic contact mechanics footprint and contact dwell calculation.
   - 8-zone closed-loop proportional pneumatic cylinder force balancing (up to 3,000 N total compaction force) with active differential tilt and camber compensation.
4. Prepreg Resin Rheology & In-Situ Consolidation Kinetics:
   - Arrhenius-type resin viscosity dynamics coupled with autocatalytic epoxy cure reaction kinetics.
   - Lee-Springer intimate contact degree and polymer reptation autohesion healing degree tracking.
5. In-Line High-Speed 2D Laser Triangulation Metrology:
   - Dual blue laser sheet profilometers scanning immediately behind compaction roller at 2.0 kHz.
   - Sub-millimeter detection and classification of tow spacing gaps (> 0.38 mm), overlaps (> 0.50 mm), cross-sectional twists (> 1.5 deg), and bridging delamination (> 0.35 mm) per AS9100D and Boeing D6-83074 specs.
6. 8-State Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$ at $T_s = 5$ ms):
   - 8 states: Nip point consolidation temp, Compaction roller normal force, Prepreg tow tension, Robotic kinematic TCP tool velocity, Underlying CFRP substrate thermal accumulation, Prepreg dynamic resin viscosity, Diode laser power output, and In-line measured inter-tow mean gap width.
   - 6 control inputs: Laser power setpoint demand, Roller pneumatic pressure setpoint, Spool magnetic brake torque, Robot velocity override setpoint, Roller differential tilt pressure balance, and Dynamic tow feed assist velocity offset.
7. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) with physical box saturation and dynamic slew rate limiters.
8. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - 6 critical sensor triplets (Pyrometer nip temp, Roller normal force, Tow tension, Standoff distance, Robot TCP velocity, In-line defect gap) with discrepancy timers and bumpless degradation.
9. Deterministic 14-Stage Production Finite State Machine (FSM):
   - E-Stop Safe, Mandrel Homing & Calibration, Vacuum Chuck Hold-Down, Laser Optics Warm-Up, Tow Threading & Clamping, Approach Touchdown, Nip Preheat Ramp, Steady Laydown Compaction, Dynamic Cut/Add, End-Course Dwell, Roller Lift & Retreat, In-Line Inspection Scan, Course Complete Indexing, and Emergency Laser Safety Shutter Trip.
10. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Status Words:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance hysteresis deadbands and 32-bit status, alarm, and diagnostic telemetry words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Aerospace_Composite_AFP_LaserCompaction` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    print("Generating IEC 61131-3 code...")
    st_code = generate_st_code()
    assistant_content = f"```iec-st\n{st_code}\n```"
    
    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Dataset successfully saved to: {filename}")
    print(f"File size: {os.path.getsize(filename)} bytes")
    print(f"Assistant content character count: {len(assistant_content)}")
    
    print("\nExecuting validation audit via validate_iec.py...")
    errs = validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(f"  - {e}")
        sys.exit(1)
    else:
        print("ALL IEC VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return filename, agent_id, len(assistant_content)

if __name__ == "__main__":
    save_and_validate()
