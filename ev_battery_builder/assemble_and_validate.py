# ev_battery_builder/assemble_and_validate.py
import json
import os
import sys
import uuid
import re

# Add parent directory to path to import validate_iec
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
sys.path.insert(0, os.path.dirname(__file__))

from generate_dataset import generate_iec_st
import validate_iec

def main():
    agent_uid = uuid.uuid4().hex[:8]
    json_filename = f"agent_{agent_uid}.json"
    target_path = os.path.join("data", "swarm_raw", json_filename)

    user_prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Automotive & Commercial Vehicles (EV Prismatic/Pouch Battery Cell Laser Busbar Welding & 2K Thermal Interface Material Dispensing Cell)
FUNCTION BLOCK NAME: FB_Automotive_EV_BatteryModule_LaserBusbar_ThermalDispense

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 2.0 ms):
   - 8-State model covering laser keyhole thermal diffusion, copper/aluminum melt pool dynamics, Marangoni convection, 2-component thermal gap filler dispensing pressure/flow dynamics, pneumatic nozzle travel, and fixture thermal expansion:
     States: x1=Laser Weld Keyhole Depth [um], x2=Melt Pool Temperature [degC], x3=Copper-Aluminum Intermetallic Diffusion Layer Thickness [um], x4=2K TIM Dispensing Fluid Line Dynamic Pressure [bar], x5=Dispensing Flow Velocity [mL/s], x6=Dispensed Bead Width Profile [mm], x7=Clamping Nest Pneumatic Differential Force [N], x8=Battery Cell Carrier Thermal Expansion Displacement [um].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Laser beam power wobble dynamic modulation and dispensing servo pump volumetric feedforward tracking.
   - Actuator constraints: Fiber laser power [0..6000 W], wobble frequency [0..1000 Hz], wobble amplitude [0..5.0 mm], 2K gear pump servo speed [0..3000 rpm], mixing ratio valve [0..100%], robot motion speed override [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Coaxial High-Speed Pyrometer Melt Pool Temperatures (TT_PYRO_101A/B/C) [degC]
     * 3D Optical Weld Seam Profile Height/Gap Sensors (LT_SEAM_201A/B/C) [um]
     * 2K TIM Fluid Pressure Transmitters (PT_DISP_301A/B/C) [bar]
     * Inline Coriolis Mass Flowmeters (FT_TIM_401A/B/C) [g/s]
     * Pneumatic Nest Clamping Load Cells (WT_CLAMP_501A/B/C) [N]
   - Discrepancy accumulation timers (threshold 150 ms) and bumpless degradation.

4. Deterministic 14-Stage Production State Machine (FSM):
   - CASE eState OF:
     0: CELL_MODULE_NEST_RECEIVE_AND_IDLE
     1: PNEUMATIC_MODULE_CLAMPING_AND_DATUM_LOCK
     2: 3D_VISION_BUSBAR_GAP_AND_HEIGHT_INSPECTION
     3: LASER_OPTICAL_COVER_SLIDE_AND_GAS_PURGE
     4: SURFACE_PLASMA_DEOXIDATION_TREATMENT
     5: LASER_BUSBAR_WELDING_DYNAMIC_WOBBLE_RUN
     6: POST_WELD_OCT_KEYHOLE_DEPTH_VERIFICATION
     7: WELD_SEAM_RESISTANCE_KELVIN_TEST (<10 uOhm)
     8: 2K_TIM_AUTO_CALIBRATION_AND_PURGE_SHOT
     9: DISPENSING_BEAD_ROBOT_SYNCHRONOUS_RUN
     10: 2D_LASER_TRIANGULATION_BEAD_INSPECTION
     11: MODULE_NEST_UNCLAMP_AND_OUTFEED
     12: TIM_POT_LIFE_ANTI_GEL_AUTOMATIC_FLUSH
     13: EMERGENCY_LASER_SHUTTER_AND_QUENCH_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Laser Safety SIL-3 Interlock & 32-Bit Telemetry:
   - Fast spatter ejection detection (<5 ms) and weld blowout emergency trip.
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: FUNCTION_BLOCK FB_Automotive_EV_BatteryModule_LaserBusbar_ThermalDispense
- Last line: END_FUNCTION_BLOCK
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero // ... rest of code. Every line fully written."""

    st_code = generate_iec_st()
    print(f"Generated Structured Text length: {len(st_code)} characters")

    # Format assistant response with triple backticks and iec-st
    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {
                "role": "user",
                "content": user_prompt
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ]
    }

    # Save to JSON
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset record to {target_path}")

    # Validate using validate_iec
    errors = validate_iec.validate_json_file(target_path)
    if errors:
        print("VALIDATION FAILED with errors:")
        for err in errors:
            print(f" - {err}")
        sys.exit(1)
    else:
        print(">>> SUCCESS: ALL VALIDATION CHECKS PASSED WITH 0 ERRORS! <<<")
        print(f"File path: {os.path.abspath(target_path)}")
        print(f"Total Assistant Content Length: {len(assistant_content)} characters")

if __name__ == "__main__":
    main()
