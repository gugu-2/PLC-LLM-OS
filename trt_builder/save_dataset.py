# trt_builder/save_dataset.py

import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import st_header_io
import st_var
import st_matrices
import st_phase1_tmr
import st_phase2_state_space
import st_phase3_mpc
import st_phase4_fsm
import st_phase5_alarms_diagnostics
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, C, D, K), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Primary Metallurgy & Blast Furnace Energy Recovery (Tier 1 Priority Sector) — Integrated Steel Works Blast Furnace (5,500 m³ Hearth Working Volume), Top Gas Pressure Recovery Turbine (TRT, 25 MW Axial Reaction Expansion Turbine), Dynamic Septum Valve Bank (3-Valve Parallel Bypass & Fine Pressure Trim), Blast Furnace Top Operating Pressure Control (2.50 bar ± 2.0 kPa precision), Dry Bag Filter Differential Pressure Interlocks, and Fast Emergency Bypass Electro-Hydraulic Quick-Closing / Quick-Opening Valves (< 450 ms).**

**Function Block Name**: `FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery`

**Engineering Context & Operational Architecture**:
1. Mathematical Cyber-Physical Rigor:
   - Explicit Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) at Ts = 10 ms modeling blast furnace top gas compressible plenum volume dynamics, turbine inlet variable stator vane (VSV) flow coefficient, septum valve parallel throttling, generator electrical power output, and shaft mechanical inertia.
   - Model Predictive Control (MPC) / Projected Gradient Descent (PGD) unrolled solver to decouple top gas pressure regulation from generator electrical power demand, absorbing sudden blast furnace slip or blow-by pressure surges without lifting safety relief bleeders.
   - 2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) voting across critical instrumentation channels (Top Gas Pressure PT-101A/B/C, Turbine Inlet Pressure PT-201A/B/C, Top Gas Mass Flow FT-301A/B/C, Generator Power Transducers WT-401A/B/C, Shaft Vibration Probes VT-501A/B/C, Bag Filter Differential Pressure DPT-601A/B/C) with bumpless degradation and discrepancy timers.
   - ISA-18.2 Alarm Engine with bit-packed DWORD alarm words, deadband hysteresis, priority escalation, and turbine overspeed / top overpressure SIL-3 emergency trips.
   - Deterministic 14-Stage FSM for Cold System Isolation, Nitrogen Inert Purge, Gas Bag Filter Differential Pressure Qualifying, Septum Valve Throttling Pressure Lock, TRT Lube Oil Pre-Lubrication, Turbine Inlet Emergency Stop Valve Open, Variable Stator Vane (VSV) Soft Acceleration, 3,000 rpm Grid Synchronization, Generator Breaker Close, Parallel Multi-Valve Pressure MPC Tracking, Dust Scouring Spray Sequence, Controlled Turbine Unloading, Emergency Fast Bypass Trip (< 450 ms), and Failsafe Bleeder Venting.

Generate a complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Steel_BlastFurnace_TopGas_TRT_PowerRecovery` with zero placeholders, full mathematical expansions, complete variable declarations, and rigorous physical SI engineering units."""

    st_code = "\n".join([
        st_header_io.get_header_and_io(),
        st_var.get_var_declarations(),
        st_matrices.get_matrices_initialization(),
        st_phase1_tmr.get_phase1_tmr(),
        st_phase2_state_space.get_phase2_state_space(),
        st_phase3_mpc.get_phase3_mpc(),
        st_phase4_fsm.get_phase4_fsm(),
        st_phase5_alarms_diagnostics.get_phase5_alarms_diagnostics()
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
