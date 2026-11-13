# build_and_save_swro.py
import json
import uuid
import os
import sys

import scripts.generate_all as ga
import scripts.generate_sections as gs
import scripts.generate_fsm_and_alarms as gfa
from scripts.build_full_swro import build_iec_code
from validate_iec import validate_json_file

def main():
    # 1. Assemble ST code
    part_head = build_iec_code()
    part_p01  = gs.generate_phase0_and_phase1()
    part_p2   = ga.build_phase2()
    part_p3   = ga.build_phase3()
    part_p4   = gfa.build_phase4()
    part_p5   = gfa.build_phase5()
    
    st_code = part_head + part_p01 + part_p2 + part_p3 + part_p4 + part_p5
    st_code = st_code.strip()
    
    wrapped_code = f"```iec-st\n{st_code}\n```"
    
    user_prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Industrial Water Treatment & Advanced Desalination (100,000 m3/day Seawater Reverse Osmosis SWRO Desalination Train with Isobaric Energy Recovery Device PX)
FUNCTION BLOCK NAME: FB_Water_Desalination_SWRO_EnergyRecovery_PX

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 20 ms):
   - 8-State model covering high-pressure RO membrane solution-diffusion transport, osmotic pressure scaling (van 't Hoff / Pitzer model), isobaric pressure exchanger (PX) volumetric rotor mixing, high-pressure booster pump hydraulic head, permeate conductivity TDS leakage, concentration polarization beta factor, membrane compaction flux decline, and concentrate brine header backpressure:
     States: x1=High-Pressure Membrane Feed Header Pressure [bar], x2=Permeate Volumetric Production Flux [LMH], x3=Energy Recovery Device PX Ceramic Rotor Speed [rpm], x4=High-Pressure Brine Concentrate Return Pressure [bar], x5=Permeate Total Dissolved Solids Conductivity TDS [uS/cm], x6=Membrane Wall Concentration Polarization Factor Beta [ratio], x7=Membrane Element Net Driving Pressure NDP [bar], x8=Booster Pump Discharge Volumetric Flow Rate [m3/h].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic HP Pump & Energy Recovery Decoupling: coordinate primary high-pressure pump VFD (75 bar) and PX booster pump VFD to balance volumetric brine displacement and eliminate hydraulic pressure shockwaves across polyamide membrane leaves.
   - Actuator constraints: Main HP pump VFD [0..3000 rpm], PX booster pump VFD [0..3000 rpm], concentrate brine control valve [0..100%], antiscalant metering pump [0..100%], permeate divert dump valve [0..100%], low-pressure flush valve [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * High-Pressure Feed Pressure Transmitters (PT_HP_101A/B/C) [bar]
     * Permeate Coriolis Mass Flowmeters (FT_PERM_201A/B/C) [m3/h]
     * Brine Concentrate Pressure Transmitters (PT_BRINE_301A/B/C) [bar]
     * Permeate Toroidal Conductivity Analyzers (AT_COND_401A/B/C) [uS/cm]
     * Isobaric Energy Recovery Rotor Magnetic Speed Pickups (ST_PX_501A/B/C) [rpm]
   - Discrepancy accumulation timers (threshold 200 ms) and bumpless degradation.

4. Deterministic 14-Stage Desalination State Machine (FSM):
   - CASE eState OF:
     0: SWRO_TRAIN_STANDBY_AND_INSTRUMENT_LOCK
     1: LOW_PRESSURE_DE-AERATION_AND_FLUSH_RUN
     2: ANTISCALANT_AND_SODIUM_BISULFITE_PRIME
     3: HP_PUMP_VARIABLE_FREQUENCY_SOFT_START
     4: PX_ISOBARIC_ROTOR_SPINUP_AND_FILL
     5: MEMBRANE_PRESSURE_RAMPUP (1.5 bar/s to 65 bar)
     6: FULL_DESALINATION_OPTIMAL_ENERGY_MPC_RUN
     7: SALINITY_SPIKE_RECOVERY_RATIO_TRIM
     8: FLUX_NORMALIZATION_AND_FOULING_LOG
     9: OFF_SPEC_PERMEATE_AUTOMATIC_DIVERT
     10: LOW_PRESSURE_PRODUCT_WATER_DISPLACEMENT
     11: MEMBRANE_CIP_CHEMICAL_WASH_SEQUENCE
     12: PRESERVATIVE_SBS_FLUSH_AND_SEAL
     13: EMERGENCY_WATER_HAMMER_MEMBRANE_TRIP
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, PX Cavitation & Water Hammer SIL-3 Interlock & 32-Bit Telemetry:
   - Membrane high differential pressure (>3.5 bar) fast shutdown (<15 ms).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: FUNCTION_BLOCK FB_Water_Desalination_SWRO_EnergyRecovery_PX
- Last line: END_FUNCTION_BLOCK
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero // ... rest of code. Every line fully written."""

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": wrapped_code}
        ]
    }
    
    file_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{file_id}.json"
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Generated dataset saved to: {output_filename}")
    print(f"Assistant Content Character Count: {len(wrapped_code)}")
    print(f"Raw Structured Text Character Count: {len(st_code)}")
    
    # Run validation
    errs = validate_json_file(output_filename)
    if errs:
        print("VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        print(f"FILE READY: {output_filename}")

if __name__ == "__main__":
    main()
