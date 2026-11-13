# assemble_and_save.py
import json
import uuid
import os
import subprocess
import build_imm_dataset
import phase_generators
import phase_generators_pt1
import phase_generators_pt2
import phase_generators_pt3
import phase_generators_pt4

user_prompt = """DOMAIN: Plastics & Polymer Processing (2,500-Ton All-Electric High-Precision Injection Molding Machine - Multi-Cavity Automotive Lens Molding, Real-Time V/P Transfer Point & Dynamic Cavity Pressure Holding)
FUNCTION BLOCK NAME: FB_Plastics_AllElectric_IMM_VPTransfer_CavityPressure

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 1.0 ms):
   - 8-State model covering melt non-Newtonian shear-thinning rheology (Cross-WLF equation), screw servo linear velocity, nozzle melt pressure dynamics, multi-cavity direct piezoelectric pressure transmission, mold deflection/clamping tonnage balance, and gate freeze-off skin layer growth:
     States: x1=Screw Linear Velocity [mm/s], x2=Nozzle Melt Dynamic Pressure [bar], x3=Cavity 1 Direct Piezoelectric Pressure [bar], x4=Cavity 4 Direct Piezoelectric Pressure [bar], x5=Clamping Unit 4-Tie-Bar Total Tonnage [kN], x6=Mold Cavity Surface Temperature [deg C], x7=Gate Solidification Skin Thickness [um], x8=Screw Hydraulic/Electric Backpressure [bar].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic V/P (Velocity-to-Pressure) Transfer Point Decoupling: switchover from speed control to holding pressure control within a sub-0.1 mm position window or 0.5 ms cavity pressure peak derivative trigger.
   - Actuator constraints: Injection servo drive current command [-100%..+100%], holding pressure servo command [0..2200 bar], plasticizing screw rotation motor speed [0..350 rpm], backpressure proportional valve [0..250 bar], mold oil temperature control valve [0..100%], clamping toggle servo [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Nozzle Direct Melt Pressure Transducers (PT_NOZZLE_101A/B/C) [bar]
     * Cavity Direct Quartz Piezoelectric Sensors (PT_CAV_201A/B/C) [bar]
     * Screw Linear Optical Scale Encoders (ST_SCREW_301A/B/C) [mm]
     * Tie-Bar Piezoelectric Strain Gauges (WT_TONNAGE_401A/B/C) [kN]
     * Mold Tooling Core Thermocouples (TT_MOLD_501A/B/C) [deg C]
   - Discrepancy accumulation timers (threshold 100 ms) and bumpless degradation.

4. Deterministic 14-Stage Production State Machine (FSM):
   - CASE eState OF:
     0: MACHINE_IDLE_AND_SAFETY_GATE_LOCK
     1: MOLD_HIGH_SPEED_CLOSE_AND_LOW_PRESSURE_PROTECT
     2: TOGGLE_LOCKUP_AND_TONNAGE_BUILD (25,000 kN)
     3: INJECTION_CARRIAGE_FORWARD_AND_TOUCH
     4: SERVO_INJECTION_PHASE1_FAST_FILL (to 95% volume)
     5: VP_TRANSFER_SWITCH_AND_DECELERATION
     6: MULTI_STAGE_PACKING_AND_HOLDING_PRESSURE
     7: GATE_FREEZE_OFF_ENDPOINT_DETECTION
     8: SCREW_PLASTICIZING_ROTATION_AND_BACKPRESSURE
     9: MELT_DECOMPRESSION_SUCKBACK_SEQUENCE
     10: INJECTION_UNIT_RETRACT_CARRIAGE
     11: MOLD_OPEN_SOFT_DECELERATION_AND_INDEX
     12: MULTI_PIN_SERVO_EJECTION_AND_PART_DROP_CHECK
     13: EMERGENCY_OVERPRESSURE_DIE_FLASH_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Mold Flash & Tie-Bar Asymmetry Interlock & 32-Bit Telemetry:
   - Die flash / mold separation ultra-fast detection (<1 ms) with immediate injection servo dump.
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord."""

parts = [
    build_imm_dataset.generate_header(),
    build_imm_dataset.generate_var_input(),
    build_imm_dataset.generate_var_output(),
    build_imm_dataset.generate_var(),
    phase_generators.generate_phase0(),
    phase_generators_pt1.generate_phase1(),
    phase_generators_pt1.generate_phase2(),
    phase_generators_pt2.generate_phase3(),
    phase_generators_pt2.generate_phase4(),
    phase_generators_pt3.generate_phase5(),
    phase_generators_pt3.generate_phase6(),
    phase_generators_pt4.generate_phase7()
]

iec_st_code = "".join(parts).strip()
assistant_content = f"```iec-st\n{iec_st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ],
    "output": assistant_content
}

agent_id = uuid.uuid4().hex[:8]
output_dir = "data/swarm_raw"
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, f"agent_{agent_id}.json")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"File successfully created: {filename}")
print(f"Total Assistant Content Characters: {len(assistant_content)}")
print(f"Total IEC-ST Raw Characters: {len(iec_st_code)}")
