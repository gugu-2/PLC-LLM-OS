# build_and_validate_dataset.py
import json
import uuid
import os
import subprocess
import generate_stamping_press

USER_PROMPT = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Tier-1 Stamping & Press Shop
### Target System: 2,500-Ton High-Speed Servo Stamping Press Line — Dynamic Hydraulic Die Cushion, 3-Axis Electronic Transfer Feeder Bars & Eccentric Tonnage Balancing
### Function Block Name: `FB_Automotive_Stamping_ServoPress_ElectronicTransfer_Cushion`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Servo Press Kinematics & Deep Drawing Hydro-Mechanical Dynamics**:
   - Direct-drive servo press slide motion profiling: programmable velocity slowdown during blank touch to eliminate impact shock and noise, constant-speed deep-drawing phase, and rapid upward return stroke.
   - 4-cylinder dynamic hydraulic/servo die cushion force profiling: F_cushion(z) = F_base + Delta_F_draw(z), actively holding blank perimeter against wrinkling while preventing tearing in AA6111 aluminum and DP980 dual-phase steel.
   - 3-axis electronic transfer feeder bar motion synchronization via electronic camming (E-CAM): feeder lift, advance, and unclamp envelopes strictly constrained within press crank angle interference windows (Theta_crank in [120 deg, 240 deg]).
   - 4-corner strain gauge eccentric tonnage balance: monitoring total press force (F_total <= 25,000 kN) and calculating center-of-pressure moments: M_x = (F_FL + F_FR) - (F_RL + F_RR), M_y = (F_FL + F_RL) - (F_FR + F_RR) to prevent catastrophic die guide wear.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Slide actual vertical position [mm], x2: Slide vertical velocity [mm/s], x3: Die cushion hydraulic pressure [bar], x4: Total measured press tonnage [kN], x5: Eccentric tilt moment magnitude [kN*m], x6: Transfer bar longitudinal position [mm].
   - Actuators: u1: Servo press main torque command [%], u2: Die cushion proportional relief valve [%], u3: Die cushion pre-acceleration booster valve [%], u4: Transfer feeder X-axis servo speed setpoint [mm/s], u5: Transfer feeder clamp vacuum solenoid [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (slide trajectory and cushion force tracking errors), R (servo motor torque and valve actuation wear penalties), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing press tonnage overload and transfer bar die interference collisions.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 50 ms), and bumpless degradation:
     * Triplicated press slide optical linear scale absolute encoders [mm]
     * Triplicated hydraulic die cushion piezoresistive pressure transmitters [bar]
     * Triplicated tie-rod press frame strain gauge load cells [kN]
     * Triplicated transfer feeder bar linear motor optical encoders [mm]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_DIE_CLAMPING_AND_TOOL_SAFETY_IDENTIFICATION`
     * 2: `STATE_CUSHION_HYDRAULIC_PRE_CHARGE_AND_ZERO_SET`
     * 3: `STATE_TRANSFER_BAR_UNLOAD_FINISHED_PART_AND_ADVANCE`
     * 4: `STATE_TRANSFER_BAR_LOAD_RAW_BLANK_INTO_DIE`
     * 5: `STATE_TRANSFER_BAR_RETRACT_TO_SAFETY_WINDOW`
     * 6: `STATE_SERVO_SLIDE_RAPID_DESCENT_TO_TOUCH_POINT`
     * 7: `STATE_DEEP_DRAW_CONTROLLED_VELOCITY_MPC_RUN`
     * 8: `STATE_DIE_CUSHION_DYNAMIC_FORCE_PROFILING_HOLD`
     * 9: `STATE_BOTTOM_DEAD_CENTER_COINING_DWELL`
     * 10: `STATE_SLIDE_RAPID_UPWARD_RETURN_STROKE`
     * 11: `STATE_CUSHION_CONTROLLED_LIFT_EJECTION_OF_PART`
     * 12: `STATE_TONNAGE_ECCENTRICITY_AUDIT_LOG`
     * 13: `STATE_EMERGENCY_OVERLOAD_OR_TRANSFER_COLLISION_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Automotive_Stamping_ServoPress_ElectronicTransfer_Cushion`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[mm]`, `[mm/s]`, `[bar]`, `[kN]`, `[kN*m]`, `[%]`, `[deg]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!"""

def build_dataset():
    st_code = generate_stamping_press.generate_stamping_press_fb()
    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{agent_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset record to: {filename}")
    print(f"Assistant content character length: {len(assistant_content)}")
    print(f"Inner ST character length: {len(st_code)}")

    # Run validation
    cmd = ["python", "validate_iec.py", filename]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validator Output:\n" + res.stdout)
    if res.stderr:
        print("Validator Stderr:\n" + res.stderr)

    if res.returncode != 0:
        raise RuntimeError("Validation failed!")
    else:
        print("SUCCESS! File perfectly verified with 0 errors.")

    return filename, agent_id, len(assistant_content), len(st_code)

if __name__ == "__main__":
    build_dataset()
