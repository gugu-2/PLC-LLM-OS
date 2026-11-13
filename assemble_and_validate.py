import os
import sys
import json
import uuid
import re

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import phase generators
from build_headbox_header import generate_iec_code
from test_phase0 import build_phase0
from test_phase1 import build_phase1
from test_phase2 import build_phase2
from test_phase3 import build_phase3
from test_phase4 import build_phase4
from test_phase5 import build_phase5
from test_phase6 import build_phase6

def assemble_code():
    header_var = generate_iec_code()
    full_code = []
    full_code.extend(header_var)
    full_code.append(build_phase0())
    full_code.append(build_phase1())
    full_code.append(build_phase2())
    full_code.append(build_phase3())
    full_code.append(build_phase4())
    full_code.append(build_phase5())
    full_code.append(build_phase6())
    return "".join(full_code)

def main():
    st_code = assemble_code()
    print(f"Total Structured Text character count: {len(st_code)}")

    # Check first line and last line
    lines = [l.strip() for l in st_code.strip().splitlines() if l.strip()]
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")

    # Build prompt
    prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following multi-billion-dollar commercial manufacturing domain:

### Commercial Sector: Pulp, Paper & Continuous Web Processing
### Target System: 1,800 m/min High-Speed Fourdrinier Paper Machine Hydraulic Headbox (64 Cross-Direction Thermal Micro-Expansion Slice Actuators, Jet-to-Wire Sync)
### Function Block Name: `FB_PulpPaper_Fourdrinier_Headbox_SliceLip_BasisWeight`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Hydraulic Headbox Dynamics & Stock Flow Mechanics**:
   - Total head equation: H_total = P_air / (rho_stock * g) + h_liquid, where P_air is compressed air pad pressure, rho_stock is fiber slurry density, and h_liquid is stock pond level.
   - Slice jet exit velocity: v_jet = C_discharge * sqrt(2 * g * H_total).
   - Jet-to-Wire speed ratio: J_W = v_jet / v_wire (strictly controlled around 1.025 to optimize fiber orientation anisotropy and tensile strength).
   - Cross-Direction (CD) basis weight profile control across 64 thermal micro-expansion slice lip spindle actuators with Gaussian/Toeplitz spatial cross-coupling attenuation matrix: Delta_w = G * Delta_u_slice.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Total hydraulic head [mm H2O], x2: Stock pond liquid level [mm], x3: Jet-to-wire speed differential [m/min], x4: Mean basis weight [g/m2], x5: Fiber consistency in headbox [g/L], x6: Air pad pressure [kPa].
   - Actuators: u1: Primary fan pump VFD speed [%], u2: Air cushion bleed/charge proportional valve [%], u3: Attenuation slice lip average opening [mm], u4: Dilution profiling header total valve [%], u5: Stock recirculation overflow valve [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (head and level tracking), R (fan pump and air valve effort), S (slew rate damping), P (terminal state cost).
   - Dynamic decoupling between total head (fast pressure dynamics) and liquid level (slow integrator dynamics).
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 150 ms), and bumpless degradation:
     * Triplicated total head piezoresistive pressure transmitters [kPa]
     * Triplicated stock pond microwave/radar level sensors [mm]
     * Triplicated dilution header electromagnetic flowmeters [m3/h]
     * Triplicated forming wire optical encoder speed sensors [m/min]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_HEADBOX_FLUSH_AND_WHITE_WATER_WARMUP`
     * 2: `STATE_AIR_CUSHION_PRESSURIZATION_AND_SEAL`
     * 3: `STATE_PRIMARY_FAN_PUMP_RAMP_TO_MINIMUM_SPEED`
     * 4: `STATE_STOCK_POND_LEVEL_CLOSED_LOOP_LOCK`
     * 5: `STATE_TOTAL_HEAD_PRESSURE_STABILIZATION`
     * 6: `STATE_JET_TO_WIRE_SPEED_SYNCHRONIZATION`
     * 7: `STATE_CD_SLICE_LIP_THERMAL_PROFILE_BASELINE`
     * 8: `STATE_NOMINAL_HIGH_SPEED_WEB_PRODUCTION_MPC`
     * 9: `STATE_ONLINE_GRADE_CHANGE_TRANSITION_RAMP`
     * 10: `STATE_SHEET_BREAK_EMERGENCY_SLURRY_DIVERSION`
     * 11: `STATE_CONTROLLED_WIRE_RAMPDOWN_AND_HEADBOX_FLOAT`
     * 12: `STATE_POST_RUN_ACID_CAUSTIC_CLEANING_CYCLE`
     * 13: `STATE_EMERGENCY_PUMP_CAVITATION_OR_STOCK_RUNOUT_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_PulpPaper_Fourdrinier_Headbox_SliceLip_BasisWeight`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[kPa]`, `[mm]`, `[m/min]`, `[g/m2]`, `[m3/h]`, `[%]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!"""

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    # Generate isolated file
    file_id = uuid.uuid4().hex[:8]
    out_dir = os.path.join("data", "swarm_raw")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, f"agent_{file_id}.json")

    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Generated dataset successfully saved to: {out_path}")
    print(f"File size on disk: {os.path.getsize(out_path)} bytes")
    return out_path

if __name__ == "__main__":
    main()
