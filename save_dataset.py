# save_dataset.py
import os
import sys
import json
import uuid

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "valve_body_builder"))
from assemble import assemble
import validate_iec

prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following heavy automotive manufacturing domain:

### Commercial Sector: Automotive Manufacturing / Automatic & Dual-Clutch Transmission Systems
### Target System: Automotive Transmission Electro-Hydraulic Valve Body EOL Testing & Solenoid Calibration (Multi-Channel Spool Valve Hydrodynamics, Dynamic Pressure Cavity Response, Solenoid Hysteresis Calibration, Cross-Port Leakage & EEPROM Flash Offset)
### Function Block Name: `FB_Automotive_Transmission_ValveBody_HydraulicTest_SolenoidCalib`

---

## 1. Architectural & Cyber-Physical Requirements:
1. **Electro-Hydraulic Spool Valve Hydrodynamics & Solenoid Electromagnetic Flux Dynamics**:
   - Multi-channel spool valve hydrodynamics, flow forces (Bernoulli steady-state and transient hydrodynamic forces), orifice discharge coefficient C_d, fluid compressibility with effective bulk modulus beta_eff(P, T, air_fraction).
   - Solenoid electromagnetic dynamics: coil resistance R_coil(T) with copper thermal coefficient, flux linkage lambda, magnetic hysteresis, and PWM drive with 200 Hz dither injection.
2. **Discrete State-Space Model (6x6 A, B, C, D)**:
   - x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k.
   - States:
     * x1: Main supply rail pressure P_rail [bar]
     * x2: Regulated clutch cavity dynamic pressure P_cavity [bar]
     * x3: Proportional spool displacement x_spool [mm]
     * x4: Valve spool velocity v_spool [m/s]
     * x5: Solenoid drive coil current I_sol [mA]
     * x6: ATF manifold oil temperature T_atf [deg C]
   - Actuators:
     * u1: Main hydraulic pump servo rail pressure valve command [bar]
     * u2: Proportional solenoid driver current command I_cmd [mA]
     * u3: Thermal conditioning heat exchanger proportional cooling valve [%]
   - Measurements / Outputs:
     * y1: Measured supply rail pressure P_rail,meas [bar]
     * y2: Measured clutch cavity pressure P_cavity,meas [bar]
     * y3: Solenoid current feedback I_sol,meas [mA]
     * y4: Manifold oil temperature T_atf,meas [deg C]
     * y5: Internal spool leakage flow Q_leak,meas [mL/min]
     * y6: Dynamic spool shift response velocity v_shift,meas [m/s]
   - Observer Innovation: x_hat_{k+1} = A*x_hat_k + B*u_k + L*(y_k - C*x_hat_k) (6x6 L gain matrix fully expanded).
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Optimizing ATF supply rail pressure [bar], proportional solenoid dither current [mA], and oil thermal heat exchanger flow [L/min].
   - Explicit quadratic cost matrices: Q (state error penalties), R (actuator control penalties), S (slew-rate penalties), P (terminal Riccati Lyapunov cost).
   - Unrolled forward state propagation over N=5 horizon, backward adjoint costate recursion (lambda), and projected gradient updates with hard boundary saturation and slew limits.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Logic**:
   - 4 independent sensor channels with median voting, rate-of-change spike rejection, discrepancy persistence timers (50 ms), and bumpless degradation (2oo3 -> 1oo2 -> 1oo1 -> Fail-Safe Trip):
     * Channel 1: Supply rail piezoresistive pressure transmitter (CH_A, CH_B, CH_C) [bar]
     * Channel 2: Spool cavity high-speed dynamic pressure sensor (CH_A, CH_B, CH_C) [bar]
     * Channel 3: Solenoid shunt resistor current transducer (CH_A, CH_B, CH_C) [mA]
     * Channel 4: ATF oil manifold RTD sensor (CH_A, CH_B, CH_C) [deg C]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - CASE iState OF covering:
     * 0: STATE_UNINITIALIZED
     * 1: STATE_FIXTURE_DOCKING_HYDRAULIC_CLAMP
     * 2: STATE_ATF_OIL_PREHEATING_TEMPERATURE_SOAK
     * 3: STATE_HIGH_PRESSURE_AIR_EVACUATION_VACUUM
     * 4: STATE_MAIN_SUPPLY_RAIL_PRIME_PURGE
     * 5: STATE_BASELINE_INTERNAL_LEAKAGE_PRESSURE_DECAY
     * 6: STATE_PROPORTIONAL_SOLENOID_PWM_SWEEP_ASCENT
     * 7: STATE_SOLENOID_HYSTERESIS_SWEEP_DESCENT
     * 8: STATE_DYNAMIC_SPOOL_SHIFT_RESPONSE_TIME_AUDIT
     * 9: STATE_COLD_HOT_COMPENSATION_OFFSET_FLASH
     * 10: STATE_CLUTCH_APPLY_CAVITY_CROSS_LEAK_CHECK
     * 11: STATE_PRESSURE_RELIEF_OIL_SCAVENGE_DRAIN
     * 12: STATE_FIXTURE_UNCLAMP_AUTOMATED_BARCODE_ETCH
     * 13: STATE_ESTOP_VENT_FAILSAFE_DUMP
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Bit-Packed Telemetry Registers**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis for all key process variables.
   - Bit-packed DWORDs: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Automotive_Transmission_ValveBody_HydraulicTest_SolenoidCalib`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- Bracketed SI physical units on all I/O variables: [bar], [deg C], [mA], [mL/min], [ms], [mm], [m/s], [%], [N], [L/min].
- TARGET LENGTH: 110,000 to 150,000+ characters. Zero truncation comments, zero placeholders!"""

st_code = assemble()
formatted_code = f"```iec-st\n{st_code}\n```"

record = {
    "instruction": prompt,
    "input": "",
    "output": formatted_code,
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": formatted_code}
    ]
}

os.makedirs("data/swarm_raw", exist_ok=True)
agent_uuid = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_uuid}.json"

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully saved dataset to {filename}")
print(f"ST Code character count: {len(st_code)}")
print(f"Assistant message character count: {len(formatted_code)}")

# Now run validation
errors = validate_iec.validate_json_file(filename)
if errors:
    print("VALIDATION FAILED:")
    for err in errors:
        print(" -", err)
    sys.exit(1)
else:
    print("ALL VALIDATION CHECKS PASSED PERFECTLY WITH ZERO ERRORS!")
    sys.exit(0)
