import sys
import os
import json
import uuid

# Add current directory to path
sys.path.append(os.path.abspath("scratch"))

import lyo_part1_header_io
import lyo_part2_matrices_vars
import lyo_part3_tmr_observers
import lyo_part4_mpc_fsm
import lyo_part5_alarms_actuators

def build_full_st_code():
    p1 = lyo_part1_header_io.get_part1()
    p2 = lyo_part2_matrices_vars.get_part2()
    p3 = lyo_part3_tmr_observers.get_part3()
    p4 = lyo_part4_mpc_fsm.get_part4()
    p5 = lyo_part5_alarms_actuators.get_part5()
    
    code = f"{p1}\n{p2}\n{p3}\n{p4}\n{p5}"
    return code

def main():
    st_code = build_full_st_code()
    print(f"Total Structured Text character count: {len(st_code)}")
    
    # Check delimiters and basic rules
    lines = st_code.strip().splitlines()
    print(f"First line: {lines[0]}")
    print(f"Last line: {lines[-1]}")
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Pharmaceutical & Biopharmaceutical Freeze Drying (Lyophilization) - Production-Scale Industrial Sterile Freeze Dryer (Bulk Lyophilizer, 40 m² shelf area): Multi-Zone Thermal Fluid Shelf Heat Exchanger (Silicone oil circulation -55°C to +80°C with dynamic heating/cooling cascade PID and thermal uniformity within ±0.5°C across 16 shelves), Dual Mechanical Condenser Refrigeration Circuit (Cascade -85°C coil freezing, hot gas bypass defrosting), Ultra-High Vacuum Sublimation Control (Two-stage dry screw vacuum pumps, dual Pirani gauge vs. Capacitance Manometer sublimation end-point detection / comparative pressure measurement, controlled nitrogen gas micro-dosing bleed valve 0.05 to 0.2 mbar), Automatic Clean-in-Place (CIP) / Steam-in-Place (SIP) Sterilization (121.1°C at 2.1 bar abs with F0 lethality integration), and Hydraulic Shelf Stoppering Mechanism with dynamic tonnage monitoring.**

Task: Implement the production-grade Function Block FB_Pharma_BulkLyophilizer_CapacitanceManometer_Pirani governing:
1. Discrete State-Space Matrices (A, B, C, D) modeling silicone oil supply/return temperatures, condenser surface ice accumulation thickness, chamber pressure (Pirani vs Capacitance Manometer differential), sublimation drying front velocity, product cake core temperature, nitrogen micro-bleed mass flow rate, and hydraulic stoppering cylinder pressure: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost optimization governing shelf thermal fluid heating/cooling, nitrogen micro-bleed valve, vacuum isolation throttle, condenser refrigeration expansion valves, and hydraulic stoppering proportional pressure relief valve.
3. 2oo3 TMR voting logic on all critical transmitters (shelf product RTDs, chamber capacitance manometers, condenser refrigeration suction pressure transmitters, shelf silicone oil supply temperature probes, chamber thermal conductivity Pirani gauges, and hydraulic cylinder pressure transducers).
4. Cyber-physical observers: Pikal sublimation drying front kinetics & dynamic dry layer cake resistance, comparative pressure ratio (Pirani / Capacitance Manometer) convergence observer, Manometric Temperature Measurement (MTM) / Pressure Rise Test (PRT) ice interface estimator, Steam-in-Place (SIP) F0 thermal lethality accumulator, multi-zone shelf-to-shelf thermal uniformity gradient observer, and hydraulic stoppering vial compaction force observer.
5. 12-stage operational FSM (LYO_STATE_IDLE_STERILE_HOLD through LYO_STATE_CIP_SIP_STERILIZATION).
6. Controlled nitrogen micro-bleed pressure control with acoustic flow throttling, dynamic hydraulic stoppering tonnage ramp with glass vial crush prevention, and hot-gas bypass condenser defrosting cycle.
7. ISA-18.2 multi-tiered alarm hierarchy with vacuum loss trips, eutectic collapse thermal interlocks, hydraulic overpressure dump, and 32-bit diagnostic status word packing.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

    formatted_content = f"```iec-st\n{st_code}\n```"
    
    unique_id = uuid.uuid4().hex[:8]
    raw_filename = f"agent_{unique_id}.json"
    full_path = os.path.join("data", "swarm_raw", raw_filename)
    
    record = {
        "id": f"agent_{unique_id}",
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": formatted_content}
        ]
    }
    
    with open(full_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Successfully generated and wrote dataset to {full_path}")
    print(f"Assistant content character count: {len(formatted_content)}")
    return full_path

if __name__ == "__main__":
    main()
