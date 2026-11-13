import json
import os
import sys
from builder_smt_pnp import generate_code

def main():
    st_code = generate_code()
    wrapped_code = f"```iec-st\n{st_code}\n```"
    
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, C, D, L), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Electronics & Semiconductor Packaging (Tier 1 Priority Commercial Sector) — Ultra-High-Speed 65,000 cph Multi-Gantry SMT Pick-and-Place Machine, Flying Vision Component Alignment & Placement Impact Force Control.**

**Function Block Name**: `FB_Electronics_SMT_HighSpeed_PickAndPlace_VisionMotion`

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 0.5 ms):
   - 8-State model covering dual linear motor gantry kinematics, spindle theta rotary alignment, nozzle vacuum level dynamics, component placement contact impact stiffness, PCB substrate dynamic deflection, and linear scale thermal drift:
     States: x1=Gantry Master X-Axis Linear Position [mm], x2=Gantry Slave X-Axis Position Skew [um], x3=Pick Head Spindle Theta Rotation Angle [deg], x4=Nozzle Vacuum Suction Pressure [kPa], x5=Placement Z-Axis Contact Force [N], x6=PCB Substrate Dynamic Deflection [um], x7=Linear Scale Thermal Expansion Offset [um], x8=Vacuum Blow-off Pressure Wave Transient [kPa].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic Jerk-Limited S-Curve Contour Optimization: eliminate master-slave gantry skew (<5 um) and control Z-axis touchdown force (<3.0 N ± 0.2 N) to prevent microscopic die cracking.
   - Actuator constraints: X-master linear motor current command [-100%..+100%], X-slave linear motor current command [-100%..+100%], Theta direct-drive motor torque [-100%..+100%], Z-voice coil actuator current [-100%..+100%], vacuum proportional valve [0..100%], blow-off pulse solenoid [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Master/Slave Optical Linear Scale Encoders (ST_SCALE_101A/B/C) [um]
     * Nozzle Fast Piezoresistive Vacuum Sensors (PT_VAC_201A/B/C) [kPa]
     * Z-Axis Piezoelectric Placement Force Sensors (WT_FORCE_301A/B/C) [N]
     * Gantry Carriage Triaxial Accelerometers (AT_ACC_401A/B/C) [m/s2]
     * Machine Bed Invar Reference Thermistors (TT_BED_501A/B/C) [degC]
   - Discrepancy accumulation timers (threshold 50 ms) and bumpless degradation.

4. Deterministic 14-Stage Production State Machine (FSM):
   - CASE eState OF:
     0: MACHINE_IDLE_AND_INTERLOCK_VERIFY
     1: GANTRY_GANTRY_SKEW_CALIBRATION_AND_HOMING
     2: FEEDER_TAPE_INDEX_AND_POCKET_ALIGN
     3: MULTI_NOZZLE_PARALLEL_VACUUM_PICK
     4: FLYING_VISION_ON_THE_FLY_OPTICAL_CAPTURE
     5: COMPONENT_THETA_AND_XY_OFFSET_CALCULATE
     6: PCB_INSPECTION_AND_GLOBAL_FIDUCIAL_ALIGN
     7: HIGH_SPEED_GANTRY_TRAJECTORY_S_CURVE_RUN
     8: SOFT_TOUCHDOWN_PLACEMENT_FORCE_DECELERATION
     9: POSITIVE_PRESSURE_AIR_BLOW_OFF_RELEASE
     10: POST_PLACEMENT_VISION_CO-PLANARITY_CHECK
     11: FEEDER_EMPTY_AUTO_SPLICE_OR_RELOAD_ALERT
     12: NOZZLE_ULTRASONIC_TIP_CLEAN_CYCLE
     13: EMERGENCY_DYNAMIC_BRAKE_COLLISION_LOCKOUT
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Die Crack & Gantry Skew Interlock & 32-Bit Telemetry:
   - Placement impact force spike fast interrupt (<0.5 ms dynamic brake firing).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Electronics_SMT_HighSpeed_PickAndPlace_VisionMotion` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    filename = "data/swarm_raw/agent_77e534b5.json"
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": wrapped_code}
        ],
        "output": wrapped_code
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully wrote {filename}")
    print(f"Total JSON file size: {os.path.getsize(filename):,} bytes")
    print(f"Assistant code character length: {len(wrapped_code):,} chars")

if __name__ == "__main__":
    main()
