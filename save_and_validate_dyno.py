# -*- coding: utf-8 -*-
"""
save_and_validate_dyno.py - Assemble, save JSON to data/swarm_raw/agent_<uuid>.json, and run full validation
"""

import os
import sys
import json
import uuid

# Add builder module path
sys.path.append(os.path.abspath("dyno_builder"))
import dyno_header_io
import dyno_vars
import dyno_phase0_init
import dyno_phase1_tmr
import dyno_phase2_state_space
import dyno_phase3_mpc
import dyno_phase4_fsm
import dyno_phase5_alarms

USER_PROMPT = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Final Vehicle Assembly & End-of-Line Testing
### Target System: Automated End-of-Line (EOL) Multi-Axis 4WD Chassis Dynamometer & ADAS Calibration Bench — High-Speed Road Load Simulation, Powertrain NVH Acoustic FFT & Laser Wheel Alignment
### Function Block Name: `FB_Automotive_Assembly_EOL_ChassisDyno_NVH_ADAS_Calibration`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Chassis Dynamometer Road Load Simulation & NVH Acoustics**:
   - 4-wheel independent AC vector dyno roller road load simulation: F_road(v) = F_0 + F_1 * v + F_2 * v^2 + m_veh * (dv/dt), with high-speed AC vector drive torque response (< 8 ms) matching vehicle curb mass (1,800 kg to 3,200 kg EV battery platforms).
   - High-frequency (20 kHz) piezoelectric accelerometer powertrain NVH acoustic analysis: gear whine orders (mesh frequencies), differential hypoid bevel gear tooth contact harmonics, and wheel bearing rumble FFT spectrum.
   - Dynamic wheel wheelbase adjustment (2,600 mm to 3,400 mm) with hydraulic roller centering clamps and pneumatic vehicle restraint belts.
   - Automated non-contact laser optical wheel alignment: measuring toe-in/toe-out (+/- 0.05 deg), camber (+/- 0.1 deg), and thrust angle with automated steering wheel centering servo.
   - Front 77 GHz radar target simulator and stereo camera optical target board positioning via 3-axis servo gantry for ADAS lane keep and adaptive cruise control sensor calibration.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Vehicle forward velocity [km/h], x2: Dyno front roller absorbed torque [N*m], x3: Dyno rear roller absorbed torque [N*m], x4: Powertrain NVH vibration RMS amplitude [m/s2], x5: Wheel toe angle deviation [deg], x6: ADAS radar boresight misalignment angle [mrad].
   - Actuators: u1: Dyno front AC vector drive torque command [%], u2: Dyno rear AC vector drive torque command [%], u3: Roller surface cooling blower fan VFD [%], u4: ADAS target gantry positioner X/Y servo [%], u5: Wheel restraint clamp hydraulic proportional valve [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (velocity, torque, and alignment errors), R (dyno torque slew and gantry position penalties), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing vehicle tire slippage on steel dyno rollers and avoiding vehicle restraint breakaway.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 50 ms), and bumpless degradation:
     * Triplicated dyno roller optical pulse tachometers [RPM]
     * Triplicated dyno roller load cell torque reaction arms [N*m]
     * Triplicated powertrain triaxial piezoelectric accelerometers [g]
     * Triplicated non-contact laser wheel alignment optical receivers [deg]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_VEHICLE_DRIVE_ON_AND_WHEELBASE_ADJUST_DOCK`
     * 2: `STATE_PNEUMATIC_RESTRAINT_STRAP_TENSION_AND_LOCK`
     * 3: `STATE_ROLLER_SURFACE_COOLING_BLOWER_START`
     * 4: `STATE_LASER_WHEEL_ALIGNMENT_DYNAMIC_RUNOUT_MEASURE`
     * 5: `STATE_STEERING_WHEEL_ROBOT_LEVEL_AND_CENTER_HOLD`
     * 6: `STATE_LOW_SPEED_BRAKE_FORCE_AND_ABS_CYCLING_TEST`
     * 7: `STATE_HIGH_SPEED_ROAD_LOAD_SIMULATION_MPC_RUN`
     * 8: `STATE_POWERTRAIN_NVH_ACOUSTIC_FFT_HARMONIC_EVAL`
     * 9: `STATE_ADAS_RADAR_AND_CAMERA_TARGET_BOARD_ALIGN`
     * 10: `STATE_REGENERATIVE_BRAKE_DECELERATION_ENERGY_DUMP`
     * 11: `STATE_WHEEL_RESTRAINT_RELEASE_AND_LIFT_EJECTION`
     * 12: `STATE_EOL_QUALITY_CERTIFICATE_AND_DTC_CLEAR_LOG`
     * 13: `STATE_EMERGENCY_TIRE_SLIP_OR_RESTRAINT_BREAKAWAY_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Automotive_Assembly_EOL_ChassisDyno_NVH_ADAS_Calibration`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[km/h]`, `[N*m]`, `[RPM]`, `[m/s2]`, `[deg]`, `[mrad]`, `[%]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!

---

## 3. EXECUTION STEPS:
1. Write a python script to assemble and output the complete record to `data/swarm_raw/agent_<uuid>.json`.
2. Validate with `python validate_iec.py data/swarm_raw/agent_<uuid>.json`. Ensure 0 errors!
3. Send a message to parent reporting completion details (Function Block name, filename, character count, and parity audit)."""

def assemble_iec_st():
    parts = [
        dyno_header_io.get_header_and_io().rstrip(),
        dyno_vars.get_vars().rstrip(),
        dyno_phase0_init.get_phase0_init().rstrip(),
        dyno_phase1_tmr.get_phase1_tmr().rstrip(),
        dyno_phase2_state_space.get_phase2_state_space().rstrip(),
        dyno_phase3_mpc.get_phase3_mpc().rstrip(),
        dyno_phase4_fsm.get_phase4_fsm().rstrip(),
        dyno_phase5_alarms.get_phase5_alarms().strip()
    ]
    return "\n\n".join(parts)

def main():
    st_code = assemble_iec_st()
    print(f"Total IEC 61131-3 ST character length: {len(st_code)} characters")
    
    code_block = f"```iec-st\n{st_code}\n```"
    record = {
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": code_block}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    file_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{file_id}.json"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully wrote record to {output_filename}")
    
    # Run validate_iec.py
    import validate_iec
    errs = validate_iec.validate_json_file(output_filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        print(f"Validated JSON file: {output_filename}")

if __name__ == "__main__":
    main()
