# -*- coding: utf-8 -*-
"""
Builder for FB_FoodBev_Dairy_FallingFilm_MVR_SprayDryer
Lumina Cyber-Physical Automation Swarm V7 Max-Persona
"""
import json
import uuid
import os
import sys

# Import builder parts
from dairy_mvr_spraydryer_builder.part1_declarations import get_part1_declarations
from dairy_mvr_spraydryer_builder.part2_matrix_init import get_part2_matrix_init
from dairy_mvr_spraydryer_builder.part3_tmr_voting import get_part3_tmr_voting
from dairy_mvr_spraydryer_builder.part4_mass_energy_observer import get_part4_mass_energy_observer
from dairy_mvr_spraydryer_builder.part5_mpc_pgd import get_part5_mpc_pgd
from dairy_mvr_spraydryer_builder.part6_fsm_logic import get_part6_fsm_logic
from dairy_mvr_spraydryer_builder.part7_alarms import get_part7_alarms
from validate_iec import validate_json_file

def main():
    p1 = get_part1_declarations().strip()
    p2 = get_part2_matrix_init().strip()
    p3 = get_part3_tmr_voting().strip()
    p4 = get_part4_mass_energy_observer().strip()
    p5 = get_part5_mpc_pgd().strip()
    p6 = get_part6_fsm_logic().strip()
    p7 = get_part7_alarms().strip()

    st_code = f"{p1}\n\n{p2}\n\n{p3}\n\n{p4}\n\n{p5}\n\n{p6}\n\n{p7}"
    print(f"Total Structured Text character count: {len(st_code)}")

    fence_start = "```iec-st\n"
    fence_end = "\n```"
    assistant_content = f"{fence_start}{st_code}{fence_end}"

    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Food & Beverage / Dairy Processing (Industrial 50,000 kg/h Multi-Stage Falling Film MVR Evaporator & Spray Dryer Powder Tower)
FUNCTION BLOCK NAME: FB_FoodBev_Dairy_FallingFilm_MVR_SprayDryer

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 20 ms):
   - 8-State model of thin-film evaporation, boiling point elevation (BPE), vapor recompression compressor thermodynamics, droplet atomization drying kinetics, and powder moisture equilibrium:
     States: x1=Calandria 1st Effect Sump Level [m], x2=Calandria Concentrated Brix Solids Content [% TS], x3=MVR Centrifugal Vapor Compressor Differential Pressure [kPa], x4=Compressor Saturated Suction Temperature [degC], x5=Drying Chamber Inlet Air Temperature [degC], x6=Exhaust Air Relative Humidity [% RH], x7=Final Milk Powder Moisture Content [% w/w], x8=Evaporator Falling Film Recirculation Velocity [m/s].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Non-linear Boiling Point Elevation (BPE) dynamic compensation and MVR compressor anti-surge coordinated decoupling.
   - Actuator constraints: Feed rate valve [0..100%], MVR VFD speed [3,000..12,000 rpm], steam injection valve [0..100%], high-pressure rotary atomizer pressure [150..250 bar], burner gas modulation [0..100%], main exhaust fan damper [0..100%]. Slew rate limits on all outputs.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Calandria 1st Effect Liquid Level (LT_101A/B/C) [mm]
     * In-line Optical Brix / Refractometer Concentration (DT_201A/B/C) [% Brix]
     * MVR Compressor Differential Pressure Transmitters (PDT_301A/B/C) [kPa]
     * Spray Dryer Exhaust Air Temperature (TT_401A/B/C) [degC]
     * Spray Dryer Cyclone Spark Infrared Detectors (IRT_501A/B/C) [counts/s]
   - Discrepancy accumulation timers (threshold 400 ms) and bumpless degradation.

4. Deterministic 14-Stage Commercial Dairy State Machine (FSM):
   - CASE eState OF:
     0: SANITARY_IDLE_PRECHECK
     1: CIP_CAUSTIC_ACID_PREWASH_VERIFICATION
     2: WATER_BALANCE_THERMAL_PREHEAT_RECIRCULATION
     3: MILK_FEED_INTRODUCTION_BUMPLESS_SWITCH
     4: CONCENTRATION_RAMPUP_EFFECTS_1_2_3
     5: MVR_COMPRESSOR_SPINUP_AND_COUPLING
     6: SPRAY_DRYER_BURNER_AIR_PREHEAT (Inlet 190 degC)
     7: HIGH_PRESSURE_ATOMIZATION_SLURRY_FEED
     8: FLUIDIZED_BED_SECONDARY_DRYING_AND_COOLING
     9: POWDER_DENSE_PHASE_PNEUMATIC_CONVEYING
     10: FLASH_CONCENTRATE_DIVERT_OUT_OF_SPEC
     11: WATER_FLUSH_SYSTEM_EMPTY_SEQUENCE
     12: FOULING_BURNOUT_OR_EMERGENCY_SHUTDOWN
     13: EXPLOSION_VENT_ISOLATION_FIRE_DELUGE_INTERLOCK
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, NFPA 68/69 Explosion Protection & 32-Bit Telemetry:
   - High-High chamber pressure fast explosion suppression barrier firing (<10 ms).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord."""

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

    print(f"Dataset successfully generated and saved to: {filename}")
    errs = validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(f" - {e}")
        sys.exit(1)
    else:
        print("PERFECTION: ALL IEC VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return filename

if __name__ == "__main__":
    main()
