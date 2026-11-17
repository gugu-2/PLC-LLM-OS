# package_dataset.py
import json
import uuid
import os
import subprocess
from generate_ecu_smt_fb import generate_st_code

prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Electronics Manufacturing / High-Speed SMT Factory
### Target System: 120,000 CPH High-Speed Dual-Gantry Dual-Lane SMT Pick-and-Place Machine for Automotive ECUs — Linear Motors Jerk Limiting, Multi-Nozzle Vacuum Decay & On-the-Fly 3D Vision Alignment
### Function Block Name: `FB_Electronics_AutomotiveECU_SMT_PickAndPlace_VisionMotion`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **High-Speed Linear Motor Motion Dynamics & Vacuum Pickup Physics**:
   - Dual-gantry linear motor motion synthesis with 5th-order polynomial S-curve jerk limiting: j_max = 250 m/s^3, a_max = 50 m/s^2, minimizing mechanical structural vibration settling time (< 8 ms) during ultra-high-speed placement (120,000 components per hour).
   - Multi-nozzle rotary vacuum manifold pneumatic decay dynamics: micro-piezoresistive vacuum sensor decay analysis detecting missed pickups, component tombstoning, and nozzle air leakage (P_vac <= -75 kPa threshold for 0201 passives to automotive BGA/QFN chips).
   - On-the-fly high-speed strobe vision camera image acquisition and sub-pixel optical edge processing: calculating Cartesian offsets (Delta_x, Delta_y, Delta_theta) during travel from feeder to PCB.
   - Dual-lane conveyor PCB dynamic clamping, board warpage laser height sensor triangulation compensation (Z_offset), and thermal expansion thermal drift correction.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Gantry X-axis position tracking error [um], x2: Gantry Y-axis position tracking error [um], x3: Placement head rotary nozzle vacuum pressure [kPa], x4: Placement component Z-axis contact force [N], x5: Placement angular theta offset [mrad], x6: Structural gantry vibration RMS acceleration [m/s2].
   - Actuators: u1: Linear motor X-axis drive current [%], u2: Linear motor Y-axis drive current [%], u3: Rotary placement head voice coil Z-axis force servo [%], u4: Multi-nozzle vacuum venturi solenoid [%], u5: High-speed positive pressure blow-off puff valve [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (X, Y, theta tracking and vacuum errors), R (linear motor current and voice coil force penalties), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing automotive semiconductor die micro-cracking (F_placement <= 2.5 N) and avoiding solder paste displacement.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 20 ms), and bumpless degradation:
     * Triplicated optical linear scale encoders on X/Y gantry axes [um]
     * Triplicated micro-piezoresistive vacuum pressure sensors [kPa]
     * Triplicated placement nozzle piezoelectric touch contact force load cells [N]
     * Triplicated 3-axis machine frame structural accelerometers [m/s2]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_DUAL_LANE_CONVEYOR_PCB_FEED_AND_WARPAGE_SCAN`
     * 2: `STATE_PCB_HYDRAULIC_BOTTOM_SUPPORT_PIN_ENGAGEMENT`
     * 3: `STATE_GANTRY_HIGH_SPEED_SLEW_TO_FEEDER_BANK`
     * 4: `STATE_MULTI_NOZZLE_SIMULTANEOUS_PICKUP_DESCENT`
     * 5: `STATE_VACUUM_LEVEL_VERIFICATION_AND_TOMBSTONE_CHECK`
     * 6: `STATE_HIGH_SPEED_TRAVERSE_OVER_FLYING_VISION_CAMERA`
     * 7: `STATE_ON_THE_FLY_OPTICAL_ALIGNMENT_OFFSET_COMPUTATION`
     * 8: `STATE_ROTARY_NOZZLE_THETA_ORIENTATION_CORRECTION`
     * 9: `STATE_PRECISION_PLACEMENT_DESCENT_MPC_RUN`
     * 10: `STATE_CONTROLLED_CONTACT_FORCE_LANDING_AND_PUFF_RELEASE`
     * 11: `STATE_NOZZLE_RAPID_RETRACT_AND_OPTICAL_AOI_INSPECT`
     * 12: `STATE_FINISHED_PCB_UNCLAMP_AND_LANE_DISCHARGE`
     * 13: `STATE_EMERGENCY_HEAD_COLLISION_OR_VACUUM_LOSS_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`."""

st_code = generate_st_code()
assistant_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset saved to {filename}")
print(f"Assistant content character count: {len(assistant_content)}")

# Validate with validate_iec.py
res = subprocess.run(["python", "validate_iec.py", filename], capture_output=True, text=True)
print(res.stdout)
if res.stderr:
    print("STDERR:", res.stderr)
if res.returncode != 0:
    print("VALIDATION FAILED!")
    exit(1)
else:
    print(f"SUCCESS: agent_{agent_id}.json PASSED ALL CHECKS!")
    with open("latest_agent_file.txt", "w", encoding="utf-8") as f:
        f.write(filename)
