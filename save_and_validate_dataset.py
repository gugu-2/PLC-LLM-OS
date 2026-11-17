# save_and_validate_dataset.py

import json
import uuid
import os
import subprocess
import build_gigapress_full as bg
import test_var_block as tv
import section0_and_1 as s01
import section2_physics as s2
import section3_mpc as s3
import section4_fsm as s4
import section5_6_7 as s567

# 1. Exact prompt from user/parent
prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Heavy Foundry & Structural Mega-Casting
### Target System: 9,000-Ton Ultra-Large High-Pressure Die Casting Machine (Giga-Press) — Real-Time Closed-Loop Shot Control, Vacuum Extraction & 4-Tie-Bar Tonnage Balancing
### Function Block Name: `FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Multi-Phase Injection Shot Hydraulics & Vacuum Dynamics**:
   - 3-Phase high-speed injection hydraulic dynamics:
     * Phase 1 (Slow shot): Plunger advances at v1 = 0.25 m/s to gently gather molten aluminum alloy (A380/AlSi10MnMg, 110 kg dose) without creating wave turbulence or trapping air pockets.
     * Phase 2 (Fast shot): High-acceleration transition (a_shot >= 45 m/s^2, v2 = 8.5 m/s) filling complex thin-walled rear underbody cavity in < 40 ms.
     * Phase 3 (Intensification): Hydraulic pressure multiplier spike (P_intens = 1,400 bar) squeezing out solidification shrinkage porosity before gate freeze.
   - High-vacuum cavity extraction system: multi-stage Roots vacuum blowers pulling mold cavity below 25 mbar, with hydraulic chill-block shutoff valve closing in < 8 ms before molten metal reaches vacuum lines.
   - 4-Tie-Bar hydraulic pre-stress clamping tonnage balancing: dynamic strain gauge feedback across four 750 mm diameter tie-bars (Total clamping force = 90,000 kN +/- 2%), preventing die flash and tie-bar thermal asymmetry.
   - Multi-channel pressurized die thermal regulation: water/oil cooling and electric cartridge heaters tracking mold surface temperature (220 °C to 280 °C).
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Plunger injection velocity [m/s], x2: Hydraulic shot cylinder head pressure [bar], x3: Mold cavity vacuum pressure [mbar], x4: Total tie-bar clamping force [kN], x5: Die face cavity temperature [deg C], x6: Cast part solidification thickness [mm].
   - Actuators: u1: Servo injection proportional pilot valve [%], u2: Hydraulic accumulator fast-discharge poppet valve [%], u3: Intensifier multiplier cylinder pilot valve [%], u4: Vacuum line high-speed extraction valve [%], u5: Die thermal tempering oil circulating pump speed [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (plunger velocity, intensification pressure, and vacuum errors), R (hydraulic valve actuation and pump power penalties), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing molten metal flash blowout, cold shuts, and gas porosity defects.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 20 ms), and bumpless degradation:
     * Triplicated shot cylinder magnetostrictive linear velocity transducers [m/s]
     * Triplicated hydraulic shot pressure piezoresistive sensors [bar]
     * Triplicated mold cavity vacuum Pirani/capacitance transmitters [mbar]
     * Triplicated tie-bar strain gauge extensometer load cells [kN]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_DIE_SAFETY_DOOR_LOCK_AND_PARTING_AGENT_SPRAY`
     * 2: `STATE_4_TIE_BAR_HYDRAULIC_CLAMP_TO_90000KN`
     * 3: `STATE_LADLE_ROBOT_MOLTEN_ALUMINUM_POUR_INTO_SLEEVE`
     * 4: `STATE_MOLD_CAVITY_HIGH_VACUUM_EVACUATION_BELOW_25MBAR`
     * 5: `STATE_PHASE1_SLOW_SHOT_WAVE_SURGE_SUPPRESSION`
     * 6: `STATE_PHASE2_FAST_SHOT_HIGH_ACCELERATION_CAVITY_FILL`
     * 7: `STATE_VACUUM_CHILL_BLOCK_VALVE_FAST_SHUTOFF`
     * 8: `STATE_PHASE3_INTENSIFICATION_PRESSURE_SQUEEZE_1400BAR`
     * 9: `STATE_IN_DIE_SOLIDIFICATION_COOLING_HOLD`
     * 10: `STATE_TIE_BAR_DECOMPRESSION_AND_DIE_OPEN_STROKE`
     * 11: `STATE_HYDRAULIC_EJECTOR_PINS_MULTI_POINT_PUSH`
     * 12: `STATE_EXTRACTOR_ROBOT_PART_GRIP_AND_LASER_METROLOGY`
     * 13: `STATE_EMERGENCY_FLASH_BLOWOUT_OR_TIE_BAR_OVERSTRAIN_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Automotive_MegaCasting_9000Ton_RealTimeShot_Vacuum`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[m/s]`, `[bar]`, `[mbar]`, `[kN]`, `[deg C]`, `[mm]`, `[%]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!"""

# 2. Assemble ST code
st_code = (
    bg.get_header().strip() + "\n" +
    bg.get_var_input().strip() + "\n" +
    bg.get_var_output().strip() + "\n" +
    tv.get_var_block().strip() + "\n" +
    s01.get_section0().strip() + "\n" +
    s01.get_section1().strip() + "\n" +
    s2.get_section2().strip() + "\n" +
    s3.get_section3().strip() + "\n" +
    s4.get_section4().strip() + "\n" +
    s567.get_section5_6_7().strip()
)

# 3. Wrap in code fence
asst_content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": asst_content}
    ]
}

file_uuid = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{file_uuid}.json"
os.makedirs("data/swarm_raw", exist_ok=True)

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset saved to: {filename}")
print(f"Total Assistant Content Length: {len(asst_content)} characters")
print(f"Total Structured Text Length: {len(st_code)} characters")

# 4. Run validate_iec.py
import validate_iec
errs = validate_iec.validate_json_file(filename)
if errs:
    print("VALIDATION FAILED:")
    for e in errs:
        print(" -", e)
    sys.exit(1)
else:
    print("VALIDATION SUCCESS: 0 errors detected!")
