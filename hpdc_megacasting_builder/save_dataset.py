# hpdc_megacasting_builder/save_dataset.py

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
import build_st_phase2_state_space
import build_st_phase3_mpc
import build_st_phase4_fsm
import build_st_phase5_thermal_die
import build_st_phase6_alarms_spc
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, Ew, C, D, K), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Foundry, Metallurgy & Mega-Die Casting (Tier 1 Priority Commercial Sector) — 4,000-Ton High-Pressure Die Casting (HPDC) Machine (Automotive Gigacasting / Structural EV Castings), Real-Time Closed-Loop Plunger Shot Injection (Phase 1 slow wave, Phase 2 high-speed filling up to 10 m/s, Phase 3 < 15 ms intensification pressure rise to 800 bar), Multi-Zone Thermal Die Balancing, Vacuum Assist Evacuation, and Automated Multi-Axis Core Pull / Part Ejection.**

**Function Block Name**: `FB_Foundry_HighPressureDieCasting_RealTimeInjection_Thermal`

**Engineering Context & Operational Architecture**:
1. 4,000-Ton (40,000 kN) Clamping Force & Structural Rigor:
   - Mega-die casting machine for single-piece aluminum EV front/rear floor underbody structures (AlSi10MnMg / Aural-2).
   - 4-column tie-bar dynamic strain extensometers for real-time platen tilt parallelism monitoring and eccentric loading prevention.
2. Real-Time Closed-Loop Plunger Shot Injection:
   - Phase 1 Slow Shot: 0.15 - 0.70 m/s with parabolic wave crest suppression to eliminate air entrapment in the shot sleeve prior to covering the pour hole.
   - Phase 2 Fast Shot: Ultra-high-speed cavity filling up to 10.0 m/s with acceleration up to 450 m/s^2, filling complex gigacasting thin walls in 25 - 55 ms before premature chilling.
   - Phase 3 Intensification: Sub-15 ms ultra-fast pressure rise to 800 bar specific metal pressure for shrinkage feeding and microporosity compaction.
3. Triple Modular Redundant (2oo3 TMR) Instrumentation:
   - Median voting, deviation thresholds, discrepancy timers, and bumpless degradation across 7 channels:
     * Cylinder Head Pressure PT-101A/B/C [bar]
     * Cylinder Rod Pressure PT-201A/B/C [bar]
     * Plunger Optical Linear Absolute Encoder ENC-301A/B/C [mm]
     * Cavity Vacuum Transducers VPT-401A/B/C [mbar]
     * Hydraulic Piston Accumulator PT-501A/B/C [bar]
     * Main Clamping Force Load Cells LC-601A/B/C [kN]
     * Melt Shot Sleeve Thermocouples TT-701A/B/C [deg C]
4. Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E_w w_k, y_k = C x_k + D u_k$) at Ts = 1.0 ms:
   - 8 states: Plunger position deviation, plunger velocity, head pressure, rod pressure, in-cavity dynamic metal pressure, cavity vacuum level, average die surface temperature, intensifier intermediate pressure.
   - 6 control inputs: Shot servo valve spool %, fast accumulator cartridge %, intensifier spool %, vacuum throttle %, clamp line pressure, die cooling flow %.
   - 3 disturbances: Molten alloy viscosity/temp variation, mold thermal fatigue/flow resistance, hydraulic supply ripple.
   - Steady-state Kalman observer innovation update with gain matrix K (8x6).
5. Receding-Horizon Model Predictive Control (MPC):
   - Unrolled Projected Gradient Descent (PGD) with 6 iterations minimizing quadratic cost with output tracking penalties Q, control effort penalties R, and slew penalties S.
   - Slew-rate limiting and anti-stiction dither injection.
6. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stages 0 to 14: Idle & Interlocks Check, Die Lockup & Tonnage Build, Ladle Robotic Pouring, Biscuit Slow Shot Advance, Vacuum Assist Evacuation, High-Speed Cavity Injection, Ultra-Fast Intensification Pressure Hold, In-Die Solidification Cooling, Vacuum Vent & Pressure Equalization, Hydraulic Core Slide Retract, Die De-Clamp & Open, Hydraulic Ejector Knockout, Robot Part Extraction, Multi-Zone Die Thermal Spray Lubrication, Emergency Hydraulic Dump Failsafe.
7. Multi-Zone Thermal Die Balancing Subsystem:
   - 12 independent pressurized water/thermal oil tempering zones (Zones 1-6 Fixed Half, Zones 7-12 Moving Half) with PID temperature regulation, energy extraction calculation, and 1,000 ms PWM duty cycle solenoid drivers.
8. ISA-18.2 Multi-Tiered Alarms & Statistical Process Control (SPC):
   - Critical HH/H/L/LL trip points, clearance deadbands, first-out latching.
   - Circular buffer history for last 30 shots tracking biscuit thickness, peak shot velocity, intensification rise time, and peak squeeze pressure, computing Mean, Variance, Sigma, Cp, and Cpk.
   - 32-bit bit-packed telemetry words: Status FSM Phase, Status Motion State, Alarm Critical Trips, Alarm Warnings, TMR Sensor Health, and SPC Quality Flags.

Generate a complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Foundry_HighPressureDieCasting_RealTimeInjection_Thermal` with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_state_space.get_phase2_state_space(),
        build_st_phase3_mpc.get_phase3_mpc(),
        build_st_phase4_fsm.get_phase4_fsm(),
        build_st_phase5_thermal_die.get_phase5_thermal_die(),
        build_st_phase6_alarms_spc.get_phase6_alarms_spc()
    ])

    print("Verifying internal Structured Text code...")
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("INTERNAL IEC-ST VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print("Internal IEC-ST Validation passed with 0 errors!")

    assistant_content = f"```iec-st\n{st_code}\n```"

    record = {
        "instruction": prompt,
        "input": "",
        "output": assistant_content,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    raw_dir = os.path.join(workspace_dir, "data", "swarm_raw")
    os.makedirs(raw_dir, exist_ok=True)
    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(raw_dir, f"agent_{agent_id}.json")

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"\nDataset successfully written to: {filename}")
    print(f"Assistant content character count: {len(assistant_content)}")

    print("\nRunning official validate_iec.py file check...")
    file_errs = validate_iec.validate_json_file(filename)
    if file_errs:
        print("OFFICIAL JSON VALIDATION FAILED:")
        for e in file_errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("OFFICIAL JSON VALIDATION PASSED WITH 0 ERRORS!")

    return filename, len(assistant_content), agent_id

if __name__ == "__main__":
    build_dataset()
