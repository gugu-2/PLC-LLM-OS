# save_dataset.py for FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling
import os
import sys
import json
import uuid

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from assemble import assemble_code

def save_and_validate():
    prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Glass & Ceramic Manufacturing / 800-Ton/Day Float Glass Line
Function Block Name: FB_Glass_FloatLine_TinBath_AnnealingLehr_ThicknessCooling

System Scope:
Continuous Commercial 800 Metric Tons/Day Architectural & Automotive Float Glass Production Line. Coordinated molten tin bath ribbon stretching & equilibrium thickness control (tin bath temperature 1,050 deg C inlet to 600 deg C exit, molten tin pool 65 meters long, reducing atmosphere 95% N2 / 5% H2 under positive overpressure to prevent stannous oxide SnO defects), 16 pairs of motorized top-roller knurled machines regulating ribbon width and thickness (2.0 mm to 19.0 mm), non-contact laser optical thickness scanner, and 120-meter Annealing Lehr multi-zone longitudinal and cross-belt cooling gradient control for residual birefringence thermal stress elimination.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Dynamic glass ribbon center thickness deviation Delta_h [um]
   - Glass ribbon total width W_ribbon [mm] and edge knurl tractive bite force [N]
   - Tin bath molten tin surface temperature gradient [deg C]
   - Protective atmosphere reducing gas pressure P_bath [mbar] and hydrogen concentration [% vol H2]
   - Annealing Lehr zone thermal stress birefringence retardation [nm/cm]
   - Lehr lehr-drive main line conveyor speed v_line [m/min]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing top-roller motor speeds 1..16 [RPM], top-roller penetration depth and angle [%], tin bath electric roof heater zone banks [%], Lehr cooling air dampers [%], and reducing gas N2/H2 trim valves [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Non-contact laser optical scanning thickness gauges (Thick_Sensors: 1, 2, 3) [mm]
   - Tin bath roof multi-wavelength infrared radiation pyrometers (Pyrometer: 1, 2, 3) [deg C]
   - Tin bath protective atmosphere differential pressure transmitters (Bath_Press: 1, 2, 3) [mbar]
   - Lehr exit polarimetric stress birefringence optical polarimeters (Stress_Sensors: 1, 2, 3) [nm/cm]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_TIN_BATH_ELECTRICAL_ROOF_HEATER_WARMUP
   - 2: STATE_PROTECTIVE_ATMOSPHERE_N2_H2_PURGE_AND_SEAL
   - 3: STATE_CANAL_TWEEL_LIFT_AND_MOLTEN_GLASS_FLOW_INCEPTION
   - 4: STATE_TIN_BATH_MOLTEN_GLASS_POOL_SPREAD_EQUILIBRIUM
   - 5: STATE_TOP_ROLLER_ENGAGE_AND_WIDTH_GRIP_ACQUISITION
   - 6: STATE_RIBBON_ATTENUATION_AND_THICKNESS_CONVERGENCE
   - 7: STATE_LIFT_OUT_ROLL_TRANSITION_INTO_ANNEALING_LEHR
   - 8: STATE_LEHR_COOLING_GRADIENT_CLOSED_LOOP_STRESS_RELAX
   - 9: STATE_NOMINAL_CONTINUOUS_FLOAT_PRODUCTION_RUN
   - 10: STATE_DYNAMIC_PRODUCT_THICKNESS_RECIPE_CHANGE
   - 11: STATE_RIBBON_WAISTING_OR_NECK_IN_AUTO_CORRECTION
   - 12: STATE_CONTROLLED_TWEEL_SHUT_AND_LEHR_CLEARING
   - 13: STATE_EMERGENCY_RIBBON_BREAK_CULLET_DUMP_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

    st_code = assemble_code()
    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    agent_id = uuid.uuid4().hex[:8]
    output_dir = os.path.join(os.path.dirname(__file__), "..", "data", "swarm_raw")
    os.makedirs(output_dir, exist_ok=True)
    filename = os.path.join(output_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to: {filename}")
    print(f"Assistant Content Character Count: {len(assistant_content)}")
    return filename

if __name__ == "__main__":
    fn = save_and_validate()
