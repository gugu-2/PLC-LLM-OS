# build_and_save_dataset.py
import json
import uuid
import subprocess
import sys
import os

sys.path.insert(0, os.path.abspath("hot_stamping_builder"))

from part1_header_and_vars import get_part1
from part2_init_and_tmr import get_part2
from part3_kinetics_and_observer import get_part3
from part4_mpc_pgd import get_part4
from part5_fsm_and_cooling import get_part5
from part6_alarms_telemetry import get_part6

prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Tier-1 Structural Hot Stamping
### Target System: 1,200-Ton Roller Hearth Furnace Hot Stamping & Die Quenching Press Line — Austenitization (930 °C), Fast Transfer (< 4s) & Martensitic Press Hardening (>= 30 K/s)
### Function Block Name: `FB_Automotive_Stamping_HotPressHardening_FurnaceQuench`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Metallurgical Phase Transformation & Thermal Quench Kinetics**:
   - Austenitization kinetics in roller hearth continuous furnace (heating 22MnB5 Boron steel to 930 °C with Al-Si protective coating intermetallic alloying: Fe2Al5 layer formation).
   - High-speed robotic feeder transfer trajectory kinematics: transferring red-hot blank from furnace exit into water-cooled die in < 3.8 seconds (T_blank >= 780 °C upon die closure to prevent ferrite/pearlite formation).
   - High-pressure hydraulic press clamping dwell and active die cooling channel heat extraction: quenching rate dT/dt >= 30 K/s exceeding critical cooling velocity to transform austenite completely into lath martensite (tensile strength R_m >= 1,500 MPa, yield strength R_p0.2 >= 1,050 MPa).
   - Martensite start (M_s = 400 °C) and martensite finish (M_f = 280 °C) thermal monitoring with internal die water flow temperature rise balance.
   - Dynamic 4-corner die contact pressure distribution (P_contact = 15.0 +/- 2.0 MPa) ensuring uniform heat transfer across 3D complex B-pillar geometry.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Blank center core temperature [deg C], x2: In-die quenching cooling rate [K/s], x3: Hydraulic press slide clamping force [kN], x4: Die tool steel surface temperature [deg C], x5: Die internal cooling water flow rate [m3/h], x6: Martensitic transformation fraction [%].
   - Actuators: u1: Hydraulic main press proportional tonnage valve [%], u2: Die internal cooling water booster pump VFD [%], u3: Robotic transfer feeder X-axis acceleration multiplier [%], u4: Roller hearth furnace zone 6 trim heating thyristor [%], u5: Nitrogen purge curtain solenoid valve [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (temperature, cooling rate, and tonnage errors), R (hydraulic valve and pump power penalties), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing soft spots (incomplete martensite), die thermal cracking, and Al-Si coating build-up on die surfaces.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 50 ms), and bumpless degradation:
     * Triplicated optical two-color pyrometers at furnace exit [deg C]
     * Triplicated fast-response infrared thermal imaging sensors in press bed [deg C]
     * Triplicated hydraulic press cylinder piezoresistive pressure transmitters [bar]
     * Triplicated die cooling channel electromagnetic flowmeters [m3/h]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_FURNACE_ZONE_AUSTENITIZATION_TEMPERATURE_LOCK`
     * 2: `STATE_DIE_COOLING_WATER_CHILLER_CIRCULATION_VERIFY`
     * 3: `STATE_FURNACE_DISCHARGE_DOOR_RAPID_OPEN`
     * 4: `STATE_HIGH_SPEED_ROBOTIC_FEEDER_BLANK_EXTRACTION`
     * 5: `STATE_SUB_4_SECOND_PRESS_BED_TRANSFER_TRAJECTORY`
     * 6: `STATE_DIE_CAVITY_BLANK_LOCATING_PIN_ENGAGEMENT`
     * 7: `STATE_PRESS_SLIDE_FAST_DESCENT_TO_BLANK_TOUCH`
     * 8: `STATE_HIGH_TONNAGE_12000KN_CLAMP_AND_HOLD_MPC_RUN`
     * 9: `STATE_IN_DIE_PRESS_HARDENING_QUENCH_TO_200C`
     * 10: `STATE_PRESS_DECOMPRESSION_AND_SLIDE_RETURN`
     * 11: `STATE_PART_LIFT_EJECTION_AND_UNLOAD_ROBOT_PICK`
     * 12: `STATE_THERMAL_IMAGING_PART_QUALITY_AND_HARDNESS_AUDIT`
     * 13: `STATE_EMERGENCY_TRANSFER_TIMEOUT_OR_DIE_CHILL_LOSS_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Automotive_Stamping_HotPressHardening_FurnaceQuench`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[deg C]`, `[K/s]`, `[kN]`, `[m3/h]`, `[bar]`, `[MPa]`, `[%]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!

---

## 3. EXECUTION STEPS:
1. Write a python script to assemble and output the complete record to `data/swarm_raw/agent_<uuid>.json`.
2. Validate with `python validate_iec.py data/swarm_raw/agent_<uuid>.json`. Ensure 0 errors!
3. Send a message to parent reporting completion details (Function Block name, filename, character count, and parity audit)."""

p1 = get_part1()
p2 = get_part2()
p3 = get_part3()
p4 = get_part4()
p5 = get_part5()
p6 = get_part6()

full_st = p1 + p2 + p3 + p4 + p5 + p6

# Strip whitespace and format fenced code
formatted_code = f"```iec-st\n{full_st.strip()}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt.strip()},
        {"role": "assistant", "content": formatted_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Generated dataset successfully saved to: {filename}")
print(f"Prompt character count: {len(prompt.strip())}")
print(f"Assistant content character count: {len(formatted_code)}")
print(f"Raw Structured Text character count: {len(full_st.strip())}")

# Run validate_iec.py
res = subprocess.run(["python", "validate_iec.py", filename], capture_output=True, text=True)
print("\n--- Validation Output ---")
print(res.stdout)
if res.stderr:
    print("Errors / Stderr:")
    print(res.stderr)

if res.returncode != 0:
    print(f"VALIDATION FAILED with return code {res.returncode}")
    sys.exit(res.returncode)
else:
    print(f"VALIDATION PERFECT! Return code: 0")
