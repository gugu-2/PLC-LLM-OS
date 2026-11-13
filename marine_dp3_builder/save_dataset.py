# marine_dp3_builder/save_dataset.py

import os
import sys
import json
import uuid

sys.path.append(os.path.dirname(__file__))
sys.path.append(os.path.abspath("."))

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phases_1_to_3
import build_st_phases_4_to_6
import build_st_phases_7_to_10
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Marine, Offshore & Naval Dynamic Positioning (Tier 1 Priority Sector): Dynamic Positioning Class 3 (DP3) Semi-Submersible Vessel with 8-Azimuth Thruster Hydrodynamic Allocation, Quadratic Thrust-Loss and Azimuth Angle Slew Optimization, 2oo3 Hydrodynamic Extended Kalman Filter (EKF) combining DGPS, HiPAP acoustic transceivers, and MRU motion sensors with Wave Frequency Notch Filtering, Active Hydraulic High-Speed Reversible Anti-Heeling & Anti-Trim Ballast Transfer, and Dynamic Power Management System (PMS) 4-Bus Blackout Prevention & Fast Load Shedding.**

**Function Block Name**: `FB_Marine_Offshore_DP3_ThrusterAllocation_AntiHeeling`

**Engineering Context & Operational Architecture**:
1. DP Class 3 (DP3) Semi-Submersible Vessel Specifications:
   - 48,000-tonne displacement semi-submersible drilling/construction rig with twin pontoons and four stability columns per pontoon.
   - 8 x 3.5 MW azimuth thrusters (5,200 kN total bollard pull) distributed across pontoon extremities.
   - 48.0 MW total generation capacity across 4 independent A/B/C/D switchboard sections with physical A60 fire-and-flood barrier separation per IMO DP3.
2. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - 3 Differential GPS (DGPS) receivers for surface position reference.
   - 3 Hydroacoustic Position Reference (HiPAP) acoustic transceivers for seabed transponder acoustic tracking.
   - 3 Motion Reference Units (MRU) measuring roll, pitch, heave, and 3-axis angular rates.
   - 3 Ultrasonic Wind Anemometers measuring relative wind velocity and azimuth direction.
   - Hydrostatic level transmitters across 8 ballast wing tanks.
   - Inter-channel discrepancy accumulation timers and automatic isolation of degraded sensor channels.
3. Hydrodynamic Extended Kalman Filter (EKF) & Wave Notch Filtering:
   - 2nd-order cascaded biquad notch filter eliminating 1st-order wave-frequency oscillatory motions (peak wave period 10.0 s) to prevent thruster mechanical wear.
   - Extended Kalman Filter estimating low-frequency drift motion states with steady-state Kalman gain matrix K.
4. 8-State Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$):
   - 8 states at Ts = 25 ms: Surge displacement [m], Sway displacement [m], Yaw heading [deg], Surge velocity [m/s], Sway velocity [m/s], Yaw rate [deg/s], Roll angle [deg], Pitch angle [deg].
   - 8 control inputs: Surge force Fx [kN], Sway force Fy [kN], Yaw moment Mz [kNm], Anti-heel flow [m3/h], Anti-trim flow [m3/h], Thruster bias [%], PMS power cap [kW], Roll active damping moment [kNm].
5. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) with physical box saturation and dynamic slew rate limiters.
6. 8-Azimuth Thruster Hydrodynamic Allocation:
   - Dynamic distribution of 3-DOF generalized forces across 8 steerable azimuth thrusters with extended moment arms.
   - Aerodynamic wind feedforward pre-compensation.
   - Shortest path azimuth steering optimization with 16.0 deg/s slew rate limits and 25.0 kN/s thrust ramp limits.
   - Quadratic thruster-thruster wake interaction loss modeling.
   - Forbidden azimuth sector barring to prevent jet wash impingement on moonpool and adjacent thruster Kort nozzles.
   - Opposing counter-biasing to eliminate gear backlash and zero-thrust deadband hunting.
7. Active Hydraulic Anti-Heeling & Anti-Trim Ballast Transfer:
   - High-speed reversible ballast pumps (4 x 1,500 m3/h) cross-connecting 8 wing tanks to counteract thruster overturning moments and deck load shifts.
   - Closed-loop hydrostatic restoring moment compensation for transverse roll and longitudinal pitch.
8. Dynamic Power Management System (PMS) Blackout Prevention:
   - Real-time online generator spinning reserve monitoring across 4 switchboards.
   - 4-stage dynamic load shedding: Stage 1 bias drop, Stage 2 pump derate, Stage 3 fast thrust curtailment, Stage 4 blackout trip protection.
9. Deterministic 14-Stage Production Finite State Machine (FSM):
   - States 0 to 13: Standby Manual, EKF Convergence, Auto-Heading Lock, Full 3-DOF Station Keeping, Weather-Vaning Optimization, High-Sea Swell Counter-Pulse, Rapid Anti-Heeling, Anti-Trim Leveling, Biased Tensioning, Forbidden Zone Avoidance, PMS Power Derating, Quick-Release Disconnect, Blackout Safe-Drift Recovery, Critical System Trip.
10. ISA-18.2 Multi-Tiered Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low alarms with hysteresis clearance deadbands and 32-bit status/diagnostic words.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Marine_Offshore_DP3_ThrusterAllocation_AntiHeeling` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phases_1_to_3.get_phases_1_to_3(),
        build_st_phases_4_to_6.get_phases_4_to_6(),
        build_st_phases_7_to_10.get_phases_7_to_10()
    ])

    print("Verifying internal Structured Text code...")
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("INTERNAL IEC-ST VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print("Internal IEC-ST Validation passed with 0 errors!")

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    raw_dir = "data/swarm_raw"
    os.makedirs(raw_dir, exist_ok=True)
    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(raw_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to {filename}")
    print(f"Assistant content character count: {len(assistant_content)}")

    print("\nRunning official validate_iec.py file check...")
    file_errs = validate_iec.validate_json_file(filename)
    if file_errs:
        print("OFFICIAL JSON VALIDATION FAILED:")
        for e in file_errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("OFFICIAL JSON VALIDATION PASSED WITH 0 ERRORS!")
        return filename, len(assistant_content), agent_id

if __name__ == "__main__":
    fn, chars, aid = build_dataset()
    print(f"DONE! File: {fn}, Characters: {chars}, AgentID: {aid}")
