# -*- coding: utf-8 -*-
"""
Module: aluminum_potline_builder/assemble.py
Assembles FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance,
validates syntax, delimiter parity, and character count with validate_iec.py,
and saves the validated synthetic record to data/swarm_raw/agent_<uuid>.json.
"""

import os
import json
import uuid
import subprocess
import sys

from aluminum_potline_builder.mod_header_io import generate_header_io
from aluminum_potline_builder.mod_var_decl import generate_var_decl
from aluminum_potline_builder.mod_matrices_init import generate_matrices_init
from aluminum_potline_builder.mod_tmr import generate_tmr
from aluminum_potline_builder.mod_cyberphysical import generate_cyberphysical
from aluminum_potline_builder.mod_mpc import generate_mpc
from aluminum_potline_builder.mod_fsm import generate_fsm
from aluminum_potline_builder.mod_alarms import generate_alarms

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

### Commercial Sector: Heavy Non-Ferrous Smelting & Primary Metals
### Target System: 500 kA Hall-Héroult Aluminum Reduction Potline Cell (Anode Beam Servo Positioning, Alumina Point Feeder, Anode Effect Early Detection)
### Function Block Name: `FB_Metals_Aluminum_HallHeroult_Potline_AnodeEffect_Resistance`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Electrochemical Pot Dynamics & Mass/Energy Balance**:
   - Dynamic pseudo-resistance model: R_pot = (V_cell - E_emf) / I_line, where E_emf is pseudo-counter electromotive force (~1.65 V) and I_line is potline DC current (500 kA).
   - Anode-Cathode Distance (ACD) servo adjustment: dR_pot/dACD = rho_bath / A_anode.
   - Alumina dissolution mass balance: dC_alumina/dt = m_feed - (M_Al2O3 / (6 * F)) * I_line * CurrentEfficiency / Mass_bath.
   - Early Anode Effect (AE) predictive slope observer: dR_pot/dt > R_slope_threshold triggering automated alumina overfeed pulsing and anode beam rocking to break gas polarization film.
   - Bath temperature (nominal 955 °C) and cryolite ratio (CR = NaF / AlF3) thermal equilibrium estimator.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Pot pseudo-resistance deviation [micro-Ohm], x2: Dissolved alumina concentration [wt%], x3: Bath electrolyte temperature [deg C], x4: Anode-Cathode Distance ACD [mm], x5: Anode gas bubble coverage fraction [%], x6: Cathode metal pad liquid level [cm].
   - Actuators: u1: Anode beam electromechanical hoist motor pulse command [mm], u2: Point feeder pneumatic pulse frequency [pulses/min], u3: Aluminum fluoride (AlF3) addition hopper pulse [%], u4: Gas exhaust damper positioning [%], u5: Individual anode rod manual trim offset [mm].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (resistance and alumina concentration tracking), R (anode beam movement and feeder cycling wear penalty), S (slew rate damping), P (terminal state cost).
   - Dynamic constraints avoiding localized pot cooling and anode carbon dusting.
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 300 ms), and bumpless degradation:
     * Triplicated individual cell voltage tap transmitters [V]
     * Triplicated potline DC current Rogowski/Hall-effect transductors [kA]
     * Triplicated bath optical/thermocouple temperature sensors [deg C]
     * Triplicated anode beam absolute linear optical encoders [mm]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_COLD_POT_COKE_PREHEAT_CURRENT_RAMP`
     * 2: `STATE_LIQUID_ELECTROLYTE_BATH_TRANSFER`
     * 3: `STATE_POT_STARTUP_AND_INITIAL_ACD_SET`
     * 4: `STATE_NOMINAL_ELECTROLYSIS_CLOSED_LOOP_MPC`
     * 5: `STATE_REGULAR_POINT_FEEDER_PULSE_CYCLE`
     * 6: `STATE_ANODE_BEAM_INCREMENTAL_TRACKING_MOVE`
     * 7: `STATE_EARLY_ANODE_EFFECT_PREDICTION_WARNING`
     * 8: `STATE_ANODE_EFFECT_SUPPRESSION_GAS_DISPERSAL`
     * 9: `STATE_AUTOMATED_CARBON_ANODE_BLOCK_CHANGE`
     * 10: `STATE_VACUUM_CRUCIBLE_LIQUID_ALUMINUM_TAP`
     * 11: `STATE_BATH_CHEMISTRY_ALF3_CORRECTION_CYCLE`
     * 12: `STATE_CONTROLLED_POT_DE-ENERGIZATION_BYPASS`
     * 13: `STATE_EMERGENCY_POT_TAP_LEAK_OR_ACD_COLLAPSE_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`."""

    assistant_content = f"```iec-st\n{st_code}\n```"

    record_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{record_id}.json"

    data_payload = {
        "id": f"synthetic_metals_aluminum_hall_heroult_{record_id}",
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
        json.dump(data_payload, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {output_filename}")
    print(f"Assistant content length: {len(assistant_content)} characters")

    # Validate output
    val_proc = subprocess.run([sys.executable, "validate_iec.py", output_filename], capture_output=True, text=True)
    print("--- VALIDATION STDOUT ---")
    print(val_proc.stdout)
    if val_proc.stderr:
        print("--- VALIDATION STDERR ---")
        print(val_proc.stderr)

    if val_proc.returncode != 0:
        print("Validation failed!")
        sys.exit(1)
    else:
        print("Validation succeeded with 0 errors!")

if __name__ == "__main__":
    main()
