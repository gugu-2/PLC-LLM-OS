# lyophilizer_builder/save_dataset.py

import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phase1_tmr
import build_st_phase2_sublimation
import build_st_phase3_state_space
import build_st_phase4_mpc
import build_st_phase5_cascade_stoppering
import build_st_phase6_fsm
import build_st_phase7_alarms_telemetry
import validate_iec

def build_dataset():
    prompt = """You are Lumina's Elite Synthetic Data Architect for IEC 61131-3 Programmable Logic Controllers (V7 Max-Persona: 75+ years Principal Automation Fellow & Cyber-Physical Systems Chair).

Your mission is to generate an ultra-complex, mathematically exhaustive, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK for the following multi-billion-dollar commercial manufacturing domain:

### Commercial Sector: Pharmaceutical & Biomanufacturing
### Target System: Industrial Multi-Shelf Pharmaceutical Lyophilization Freeze Dryer (16 Shelves, Dual-Cascade Condenser -85 °C, Silicone Heat Transfer Fluid)
### Function Block Name: `FB_Pharma_Lyophilization_FreezeDryer_VacuumSublimation_Thermal`

---

## 1. Mathematical & Cyber-Physical Requirements:
1. **Ice Sublimation Kinetics & Heat Transfer Balance**:
   - Sublimation rate equation: dm_sub/dt = (P_ice(T_p) - P_chamber) / (R_p(L_cake) + R_s) where P_ice is calculated via Clausius-Clapeyron / Goff-Gratch saturation vapor pressure over ice.
   - Dynamic cake dried layer resistance R_p increasing with dry layer thickness L_cake.
   - Dual-cascade refrigeration cooling loop (-85 °C coil, expansion valves, hot gas defrost bypass) and silicone heat transfer fluid circulating through 16 parallel shelves with state-space thermal dynamics.
   - Pirani gauge vs. Capacitance manometer pressure ratio (P_Pirani / P_Cap) endpoint detection algorithm converging towards 1.0 upon sublimation completion.
2. **Discrete State-Space Model (6x6)**:
   - x[k+1] = A * x[k] + B * u[k], y[k] = C * x[k] + D * u[k]
   - Observer Innovation: x_hat[k+1] = A * x_hat[k] + B * u[k] + L * (y[k] - C * x_hat[k])
   - States: x1: Shelf thermal fluid supply temperature [deg C], x2: Product vial average core temperature [deg C], x3: Product sublimation interface temperature [deg C], x4: Freeze dryer chamber vacuum pressure [mbar], x5: Condenser coil ice surface temperature [deg C], x6: Cake dry layer thickness [mm].
   - Actuators: u1: Shelf electric heater thyristor / modulating valve [%], u2: Shelf refrigeration plate-frame expansion valve [%], u3: Condenser cascade compressor stage 2 suction throttle [%], u4: Chamber vacuum throttle / fine bleed valve [%], u5: Shelf circulation pump VFD speed [%].
3. **Receding-Horizon MPC with 10 Unrolled Projected Gradient Descent (PGD) Iterations**:
   - Explicit quadratic cost matrices: Q (state error), R (actuator effort), S (slew rate damping), P (terminal state cost).
   - Constrained shelf heating rate keeping product interface temperature strictly below cake collapse temperature (T_collapse = -28.5 deg C).
   - 10 unrolled PGD iterations explicitly computing adjoint costates and projected input updates.
4. **2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite**:
   - 4 independent sensor triplets with median voting, deviation limit timers (persistence 500 ms), and bumpless degradation:
     * Triplicated chamber vacuum Pirani gauges [mbar]
     * Triplicated chamber vacuum Capacitance manometers [mbar]
     * Triplicated shelf heat transfer fluid Pt100 RTDs [deg C]
     * Triplicated product vial temperature RTD probes [deg C]
5. **Deterministic 14-Stage Production Finite State Machine (FSM)**:
   - `CASE State OF ... END_CASE` covering:
     * 0: `STATE_IDLE`
     * 1: `STATE_CIP_CLEAN_IN_PLACE_WATER_WASH`
     * 2: `STATE_SIP_STEAM_STERILIZATION_HOLD_121C`
     * 3: `STATE_POST_SIP_VACUUM_COOLING_AND_DRAIN`
     * 4: `STATE_VACUUM_DECAY_INTEGRITY_LEAK_RATE_TEST`
     * 5: `STATE_VIAL_LOADING_AND_DOOR_SEAL_INTERLOCK`
     * 6: `STATE_SHELF_PRECOOLING_AND_FREEZING_RAMP`
     * 7: `STATE_CONTROLLED_ICE_NUCLEATION_PULSE`
     * 8: `STATE_PRIMARY_DRYING_SUBLIMATION_MPC_ACTIVE`
     * 9: `STATE_PRESSURE_RISE_TEST_ENDPOINT_VERIFICATION`
     * 10: `STATE_SECONDARY_DRYING_THERMAL_DESORPTION`
     * 11: `STATE_HYDRAULIC_VIAL_STOPPERING_RAM_PRESS`
     * 12: `STATE_STERILE_NITROGEN_AERATION_BREAK`
     * 13: `STATE_EMERGENCY_POWER_FAILURE_OR_VACUUM_TRIP`
6. **ISA-18.2 Multi-Tier Alarms & 32-Bit Telemetry DWORDs**:
   - High-High, High, Low, Low-Low alarm levels with deadband hysteresis.
   - Bit-packed DWORDs: `dwStatusWord1`, `dwStatusWord2`, `dwAlarmWord1`, `dwAlarmWord2`, `dwFirstOutWord`.

---

## 2. STRICT SYNTAX & PARITY RULES:
- First line MUST be `FUNCTION_BLOCK FB_Pharma_Lyophilization_FreezeDryer_VacuumSublimation_Thermal`
- Last line MUST be `END_FUNCTION_BLOCK`
- Code fenced strictly with ` ```iec-st `
- 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
- SI physical units in brackets for all I/O variables: `[deg C]`, `[mbar]`, `[%]`, `[mm]`, `[bar]`, `[kg/h]`.
- TARGET LENGTH: 85,000 to 140,000+ characters. Zero truncation comments, zero placeholders!"""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_sublimation.get_phase2_sublimation(),
        build_st_phase3_state_space.get_phase3_state_space(),
        build_st_phase4_mpc.get_phase4_mpc(),
        build_st_phase5_cascade_stoppering.get_phase5_cascade_stoppering(),
        build_st_phase6_fsm.get_phase6_fsm(),
        build_st_phase7_alarms_telemetry.get_phase7_alarms_telemetry()
    ])

    print("Verifying internal Structured Text code...")
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("INTERNAL IEC-ST VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print(f"Internal IEC-ST Validation passed with 0 errors! Code size: {len(st_code)} characters")

    # Format into markdown fence
    fenced_code = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": fenced_code}
        ]
    }

    target_id = uuid.uuid4().hex[:8]
    output_filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{target_id}.json")
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset successfully to: {output_filename}")
    print(f"Total assistant content characters: {len(fenced_code)}")

    print(f"\nRunning external validation via validate_iec.py on {output_filename}...")
    file_errs = validate_iec.validate_json_file(output_filename)
    if file_errs:
        print("FILE VALIDATION FAILED:")
        for fe in file_errs:
            print(" -", fe)
        sys.exit(1)
    print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
    return output_filename, target_id, len(fenced_code)

if __name__ == "__main__":
    build_dataset()
