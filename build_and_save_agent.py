import os
import json
import uuid
import sys

import fccu_builder.part1_header_io as p1
import fccu_builder.part2_var_declarations as p2
import fccu_builder.part3_init_and_phase1_tmr as p3
import fccu_builder.part4_phase2_observer_and_phase3_mpc as p4
import fccu_builder.part5_phase4_fsm_logic as p5
import fccu_builder.part6_phase5_actuators_and_phase6_alarms_telemetry as p6
from validate_iec import validate_json_file

def main():
    s1 = p1.get_part1_header_io()
    s2 = p2.get_part2_var_declarations()
    s3 = p3.get_part3_init_and_phase1_tmr()
    s4 = p4.get_part4_phase2_observer_and_phase3_mpc()
    s5 = p5.get_part5_phase4_fsm_logic()
    s6 = p6.get_part6_phase5_actuators_and_phase6_alarms_telemetry()

    code_st = s1 + "\n" + s2 + "\n" + s3 + "\n" + s4 + "\n" + s5 + "\n" + s6
    print(f"Generated IEC ST character count: {len(code_st)}")
    print(f"Generated IEC ST line count: {len(code_st.splitlines())}")

    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, C, D, L), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Chemical & Petrochemical Refining (Fluid Catalytic Cracking Unit - FCCU Riser Reactor & Two-Stage Regenerator Catalyst Slide Valve Pressure Balance)**

**Function Block Name**: `FB_Petrochem_FCC_RiserRegenerator_SlideValve_PressureBalance`

**Engineering Context & Operational Architecture**:
1. Fluid Catalytic Cracking (FCCU) Hydrodynamics & Reaction Kinetics:
   - High-throughput 85,000 BPD continuous catalytic cracking unit converting heavy vacuum gas oil (VGO) and atmospheric residue into high-octane gasoline, C3/C4 olefins (LPG), and light cycle oil (LCO).
   - Short-contact-time (SCT) vertical pneumatic transport riser reactor (height 38 m, diameter 1.4 m) operating with hot fluidized zeolitic catalyst (USY / RE-Y zeolite, Geldart Group A, mean particle diameter 70 microns, particle density 1400 kg/m3).
   - Endothermic catalytic cracking kinetics absorbing 380 - 520 kJ/kg feed vaporized, supplied by sensible heat of circulating regenerated catalyst (680 - 740 deg C).
   - Dynamic catalyst-to-oil (C/O) ratio (5.5 - 9.5 wt/wt) driven by Regenerated Catalyst Slide Valve (RCSV) position and Spent Catalyst Slide Valve (SCSV) position.
   - Two-stage fluidized regenerator burning coke deposit (0.85 - 1.45 wt% on spent catalyst down to 0.05 - 0.12 wt% on regenerated catalyst) with compressed air from combustion air blower.
   - Anti-deflagration hydraulic pressure lock: slide valve differential pressure (dP) across RCSV and SCSV must be strictly maintained between 35.0 kPa and 70.0 kPa. If slide valve dP drops below 20.0 kPa, an instantaneous (<50 ms) reverse flow safety interlock closes both slide valves and isolates feed to prevent air/hydrocarbon cross-contamination.

2. 2oo3 Triple Modular Redundancy (TMR) Voting Suite:
   - 5 critical process transmitter triplets:
     * Riser Top Temperature Transmitters (TT_RISER_101A/B/C) [deg C]
     * Regenerator Dense Bed Temperature Transmitters (TT_REGEN_201A/B/C) [deg C]
     * Spent Catalyst Slide Valve Differential Pressure (PDT_SCSV_301A/B/C) [kPa]
     * Regenerated Catalyst Slide Valve Differential Pressure (PDT_RCSV_401A/B/C) [kPa]
     * Flue Gas Zirconia Oxygen Analyzers (AT_O2_501A/B/C) [% O2]
   - Discrepancy accumulation timers (300 ms persistence threshold), channel deviation limit checking, median voting when 3 channels healthy, average voting when 1 channel faulted, fallback to single healthy channel, and model observer fallback when all 3 channels fail.

3. Cyber-Physical 8-State Space Estimation & Observer Model (Ts = 25 ms):
   - 8-State discrete cyber-physical plant representation:
     * x1: Riser Outlet Temperature [deg C]
     * x2: Riser Top Differential Pressure [kPa]
     * x3: Regenerator 1st Stage Dense Bed Temperature [deg C]
     * x4: Regenerator 2nd Stage Dense Bed Temperature [deg C]
     * x5: Spent Catalyst Slide Valve Differential Pressure (dP_SCSV) [kPa]
     * x6: Regenerated Catalyst Slide Valve Differential Pressure (dP_RCSV) [kPa]
     * x7: Regenerator Flue Gas Excess Oxygen Content [% O2]
     * x8: Combustion Flue Gas Carbon Monoxide Concentration [ppmv]
   - Fully populated discrete matrices: Plant transition matrix A (8x8), Input coupling matrix B (8x6), Output extraction matrix C (6x8), Direct feedthrough matrix D (6x6), and steady-state Luenberger observer innovation gain matrix L (8x6).
   - Real-time thermodynamic computations: riser endothermic heat absorption power [MW], fluidized catalyst mass circulation flux [t/h], catalyst-to-oil ratio [wt/wt], regenerator coke combustion exothermic heat release [MW], and regenerator cyclone afterburn temperature differential [deg C].

4. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps (indices k = 0..4), 6 unrolled iterations of PGD solver.
   - Dynamic slide valve differential pressure balance decoupling: slide valve dP strictly maintained between 35 kPa and 70 kPa with non-linear barrier penalties.
   - 6 Manipulated Actuators:
     * u1: Regenerated catalyst slide valve position (RCSV) [0..100%]
     * u2: Spent catalyst slide valve position (SCSV) [0..100%]
     * u3: Combustion air blower VFD / guide vane [0..100%]
     * u4: Torch oil injection fuel control valve [0..100%]
     * u5: Riser base lift steam control valve [0..100%]
     * u6: Flue gas double-disc slide valve backpressure [0..100%]
   - Slew rate limits and physical box constraints on all actuators.

5. Deterministic 14-Stage Refinery Finite State Machine (FSM):
   - State 0:  COLD_REFRACTORY_DRYOUT_STANDBY
   - State 1:  AIR_PREHEATER_AND_BLOWER_STARTUP
   - State 2:  TORCH_OIL_CATALYST_BED_LIGHTOFF (>370 deg C)
   - State 3:  REGENERATOR_CATALYST_INVENTORY_FLUIDIZATION
   - State 4:  SLIDE_VALVE_HYDRAULIC_DP_PRESSURE_LOCK (dP > 35 kPa)
   - State 5:  RISER_LIFT_STEAM_THERMAL_EQUILIBRIUM
   - State 6:  GASOIL_FEED_INJECTION_RAMPUP (Bumpless Cut-in)
   - State 7:  FULL_CRACKING_OPTIMAL_MPC_COUPLED_RUN
   - State 8:  HEAVY_SLURRY_RECYCLE_MAXIMIZATION
   - State 9:  AIR_BLOWER_SURGE_OR_O2_ENRICHMENT_CONTROL
   - State 10: SLIDE_VALVE_DP_REVERSAL_EMERGENCY_ISOLATION (<20 kPa)
   - State 11: FEED_CUT_EMERGENCY_STRIPPING_STEAM_PURGE
   - State 12: REGENERATOR_AFTERBURNING_THERMAL_RUNAWAY_QUENCH
   - State 13: EMERGENCY_CATALYST_DUMP_AND_SAFE_PARK
   - Explicit transitions, timers, interlocks, ramps, and recovery paths for every state.

6. ISA-18.2 Process Alarm Matrix, Reverse Flow SIL-3 Interlock & 32-Bit Telemetry:
   - Reverse differential pressure fast interlock (<50 ms closure of RCSV/SCSV on dP < 20 kPa).
   - 4-Tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis for temperatures, pressures, oxygen, CO, and afterburn.
   - Bit-packed DWORD telemetry: dwStatusWord1 (modes & interlocks), dwStatusWord2 (observer health & margins), dwAlarmWord1 (critical trips), dwAlarmWord2 (warnings & TMR discrepancies), and dwFirstOutWord (first-out trip cause).

7. Mandatory Implementation Rules:
   - Output must be wrapped strictly inside triple backticks with `iec-st`.
   - Every input and output variable must include physical SI engineering units in brackets: [bar], [deg C], [kPa], [t/h], [% O2], [ppmv], [kg/s], [kg/h], [m], [m3/h], [%], [s].
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - Zero summaries, zero truncation comments, zero placeholders."""

    asst_content = f"```iec-st\n{code_st}\n```"

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }

    raw_dir = os.path.join("data", "swarm_raw")
    os.makedirs(raw_dir, exist_ok=True)
    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(raw_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully saved to: {filename}")
    print(f"File size on disk: {os.path.getsize(filename)} bytes")

    # Run validation
    print("\nExecuting validate_json_file...")
    errs = validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
