# biw_laser_brazing_builder/save_dataset.py
import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import part1_header_io
import part2_var_declarations
import part3_phase0_init
import part4_phase1_tmr
import part5_phase2_state_space
import part6_phase3_mpc
import part7_phase4_fsm
import part8_phase5_alarms
import validate_iec

def build_dataset():
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Automotive & Commercial Vehicles (Robotic Body-in-White BIW Laser Roof Ditch Brazing & Structural Epoxy Adhesive Dispensing Framing Cell)
FUNCTION BLOCK NAME: FB_Automotive_BIW_LaserBrazing_StructuralAdhesive

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 2.0 ms):
   - 8-State model covering laser brazing thermal diffusion (CuSi3 filler wire), keyhole puddle surface tension, seam tracking lateral/vertical offsets, high-viscosity structural epoxy adhesive fluid dynamics, bead cross-sectional area, car body sheet metal thermal distortion, and pneumatic framing clamp pressure:
     States: x1=Laser Brazing Melt Pool Temperature [degC], x2=CuSi3 Filler Wire Linear Feed Velocity [mm/s], x3=Joint Seam Lateral Tracking Deviation [um], x4=Structural Adhesive Dynamic Line Pressure [bar], x5=Adhesive Dispense Volumetric Flux [mL/s], x6=Dispensed Adhesive Bead Cross-Section Area [mm2], x7=Roof Panel Thermal Buckling Displacement [um], x8=Pneumatic Framing Clamping Differential Force [N].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic Laser Power & Wire Feed Coordinated Decoupling: eliminate wire stubbing and melt puddling during high-speed robot contouring (up to 120 mm/s) while coordinating adhesive servo pump speed to prevent bead necking or ballooning.
   - Actuator constraints: Fiber laser power [0..5000 W], cold wire feed servo [0..150 mm/s], seam tracking tactile/optical servo [+/-25 mm], adhesive positive-displacement servo pump [0..2500 rpm], adhesive nozzle heating jacket [0..100%], robot trajectory speed override [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Coaxial Optical Pyrometers (TT_PYRO_101A/B/C) [degC]
     * 3D Laser Seam Triangulation Profilometers (LT_SEAM_201A/B/C) [um]
     * Adhesive High-Pressure Transducers (PT_ADH_301A/B/C) [bar]
     * In-line Coriolis Mass Flowmeters (FT_ADH_401A/B/C) [g/s]
     * Framing Geo-Clamp Pneumatic Load Cells (WT_CLAMP_501A/B/C) [N]
   - Discrepancy accumulation timers (threshold 100 ms) and bumpless degradation.

4. Deterministic 14-Stage Production State Machine (FSM):
   - CASE eState OF:
     0: FRAMING_STATION_RECEIVE_AND_IDLE
     1: PNEUMATIC_GEO_CLAMPING_AND_DATUM_PIN_LOCK
     2: 3D_VISION_ROOF_DITCH_TRAJECTORY_SCAN
     3: LASER_OPTICS_PURGE_AND_SHIELDING_GAS_INIT
     4: SEAM_TRACKER_ENGAGE_AND_ZERO_OFFSET
     5: LASER_BRAZING_COORDINATED_WIRE_RUN (100 mm/s)
     6: POST_BRAZE_OPTICAL_POROSITY_INSPECTION
     7: ADHESIVE_DISPENSE_AUTO_PURGE_SHOT
     8: HIGH_VISCOSITY_STRUCTURAL_BEAD_ROBOT_RUN
     9: 2D_TRIANGULATION_BEAD_PROFILE_VERIFY
     10: FRAMING_CLAMP_DEPRESSURIZE_AND_RETRACT
     11: CAR_BODY_EGRESS_TRANSFER_HANDSHAKE
     12: ADHESIVE_NOZZLE_ANTI_CURING_AUTO_SCOUR
     13: EMERGENCY_LASER_SHUTTER_AND_MOTION_ABORT_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Wire Jam & Braze Blowout SIL-3 Interlock & 32-Bit Telemetry:
   - Fast wire feed motor stall / slip detection (<3 ms laser quench).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Automotive_BIW_LaserBrazing_StructuralAdhesive`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    st_code = (
        part1_header_io.get_header_and_io() + "\n" +
        part2_var_declarations.get_var_declarations() + "\n" +
        part3_phase0_init.get_phase0_init() + "\n" +
        part4_phase1_tmr.get_phase1_tmr() + "\n" +
        part5_phase2_state_space.get_phase2_state_space() + "\n" +
        part6_phase3_mpc.get_phase3_mpc() + "\n" +
        part7_phase4_fsm.get_phase4_fsm() + "\n" +
        part8_phase5_alarms.get_phase5_alarms()
    )

    asst_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ],
        "output": asst_content
    }

    out_dir = os.path.join(workspace_dir, "data", "swarm_raw")
    os.makedirs(out_dir, exist_ok=True)
    file_id = uuid.uuid4().hex[:8]
    filename = f"agent_{file_id}.json"
    filepath = os.path.join(out_dir, filename)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {filepath}")
    print(f"Total assistant characters: {len(asst_content)}")

    errs = validate_iec.validate_json_file(filepath)
    if errs:
        print("CRITICAL: VALIDATION FAILED!")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return filepath, len(asst_content), file_id

if __name__ == "__main__":
    build_dataset()
