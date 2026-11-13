# cz_silicon_builder/assemble.py
# -*- coding: utf-8 -*-

import os
import json
import uuid
import subprocess
import sys

from cz_silicon_builder.mod_header_io import generate_header_io
from cz_silicon_builder.mod_var_decl import generate_var_decl
from cz_silicon_builder.mod_matrices_init import generate_matrices_init
from cz_silicon_builder.mod_tmr import generate_tmr
from cz_silicon_builder.mod_cyberphysical import generate_cyberphysical
from cz_silicon_builder.mod_mpc import generate_mpc
from cz_silicon_builder.mod_fsm import generate_fsm
from cz_silicon_builder.mod_alarms import generate_alarms

def assemble_code():
    parts = [
        generate_header_io(),
        generate_var_decl(),
        generate_matrices_init(),
        generate_tmr(),
        generate_cyberphysical(),
        generate_mpc(),
        generate_fsm(),
        generate_alarms()
    ]
    return '\n\n'.join(parts)

def main():
    st_code = assemble_code()
    char_count = len(st_code)
    line_count = len(st_code.splitlines())
    print(f"Total Structured Text character count: {char_count}")
    print(f"Total Structured Text line count: {line_count}")

    prompt_text = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following multi-billion-dollar commercial manufacturing domain:

### Commercial Sector: Semiconductor & Microelectronics Manufacturing
### Target System: 300 mm Single-Crystal Silicon Ingot Czochralski (CZ) Puller Furnace (Cusp Magnetic Field Convection Damping, Optical Diameter Pyrometry)
### Function Block Name: `FB_Semiconductor_Czochralski_SiliconIngot_MeltThermal_Puller`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Stefan Boundary Solid-Liquid Interface Dynamics**:
   - Stefan condition governing crystal growth rate: k_s * (dT_s/dz) - k_l * (dT_l/dz) = rho_s * L_f * v_pull, where k_s, k_l are thermal conductivities, rho_s is solid silicon density, L_f is latent heat of fusion, and v_pull is crystal pull rate.
   - Meniscus dynamic angle balance and thermal meniscus height model: h_m = sqrt(2 * gamma_m / (rho_l * g) * (1 - sin(theta_c))).
   - Electromagnetic cusp field coil current modulation for damping chaotic Rayleigh-Benard and Marangoni melt convective turbulence.
   - Ingot diameter optical pyrometer triangulation tracking with sub-millimeter precision (D_target = 300.0 +/- 0.25 mm).
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Ingot diameter at solidification front [mm], x2: Meniscus melt temperature at tri-junction [deg C], x3: Solid silicon crystal temperature gradient [K/mm], x4: Bulk crucible melt average temperature [deg C], x5: Melt convection velocity fluctuation intensity [mm/s], x6: Ingot pull speed deviation [mm/min].
   - Actuators: u1: Crystal pull motor servo speed [mm/min], u2: Main graphite resistance heater thyristor power [kW], u3: Bottom crucible lift motor servo speed [mm/min], u4: Top/bottom cusp magnetic field coil current [A], u5: Crystal seed shaft rotation speed [RPM].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (diameter tracking & gradient penalty), R (pull speed and heater effort), S (slew rate damping), P (terminal state cost).
   - Strict dynamic constraint handling preventing crystal dislocation generation (V/G ratio Voronkov criterion for vacancy vs interstitial point defect clustering).
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 200 ms), and bumpless degradation:
     * Triplicated melt meniscus optical pyrometers [deg C]
     * Triplicated high-speed CCD camera diameter metrology channels [mm]
     * Triplicated seed suspension load cell crystal weight sensors [kg]
     * Triplicated main graphite heater thermocouple arrays [deg C]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_CHAMBER_VACUUM_EVACUATION_AND_LEAK_CHECK`
     * 2: `STATE_ARGON_MELT_PURGE_AND_PRESSURE_STABILIZE`
     * 3: `STATE_POLYSILICON_CHARGE_MELTDOWN_FULL_POWER`
     * 4: `STATE_MELT_EQUILIBRIUM_AND_CUSP_MAGNETIC_LOCK`
     * 5: `STATE_SEED_CRYSTAL_DIP_AND_MELT_WETTING`
     * 6: `STATE_DASH_NECKING_DISLOCATION_ELIMINATION`
     * 7: `STATE_CROWN_EXPANSION_CONE_ANGLE_RAMP`
     * 8: `STATE_SHOULDER_RADIUS_ROLLOVER_TRANSITION`
     * 9: `STATE_BODY_EQUAL_DIAMETER_GROWTH_MPC_ACTIVE`
     * 10: `STATE_TAILOUT_END_CONE_THERMAL_SHOCK_TAPERING`
     * 11: `STATE_CRYSTAL_SEPARATION_AND_LIFT_TO_COOL_CHAMBER`
     * 12: `STATE_RESIDUAL_MELT_COOLDOWN_AND_CRUCIBLE_PURGE`
     * 13: `STATE_EMERGENCY_MELT_LEAK_OR_VACUUM_COLLAPSE_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Semiconductor_Czochralski_SiliconIngot_MeltThermal_Puller`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[deg C]`, `[mm]`, `[mm/min]`, `[kW]`, `[RPM]`, `[mbar]`, `[A]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!"""

    assistant_content = f"```iec-st\n{st_code}\n```"
    record_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{record_id}.json"

    data_payload = {
        "id": f"synthetic_semiconductor_cz_puller_{record_id}",
        "instruction": prompt_text,
        "input": "",
        "output": assistant_content,
        "messages": [
            {"role": "user", "content": prompt_text},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(data_payload, f, indent=2, ensure_ascii=False)

    print(f"Saved dataset record to {output_filename}")

    # Run validation
    val_cmd = [sys.executable, "validate_iec.py", output_filename]
    res = subprocess.run(val_cmd, capture_output=True, text=True)
    print("STDOUT:\n", res.stdout)
    if res.stderr:
        print("STDERR:\n", res.stderr)

    if res.returncode != 0:
        print(f"VALIDATION FAILED with exit code {res.returncode}")
        sys.exit(res.returncode)
    else:
        print(f"VALIDATION PASSED PERFECTLY (0 errors) for {output_filename}")
        with open("latest_agent_file.txt", "w", encoding="utf-8") as lf:
            lf.write(output_filename)

if __name__ == "__main__":
    main()
