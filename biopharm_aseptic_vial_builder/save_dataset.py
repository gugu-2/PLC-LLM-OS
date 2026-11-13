# biopharm_aseptic_vial_builder/save_dataset.py

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
import build_st_phase5_pumps_dosing
import build_st_phase6_alarms_spc
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, Ew, C, D, K), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Biopharmaceutical Aseptic Manufacturing (Tier 1 Priority Sector) — High-Speed Aseptic Vial Liquid Filling & Stoppering Line (400 vials/min, EU GMP Annex 1 Grade A Closed Restricted Access Barrier / Isolator), 10-Head Ceramic Rotary Valveless Piston Dosing Pumps (0.1–50.0 mL, ±0.25% fill volume accuracy), In-line High-Speed EMFR 100% Tare/Gross Checkweighing, Automated Peristaltic Micro-Volume Compensation, Dynamic Continuous Vaporized Hydrogen Peroxide (VHP) Sterilization, and Vacuum Stoppering Insertion / Cap Crimping Integrity.**

**Function Block Name**: `FB_Pharma_AsepticFilling_RotaryPistonPump_IsolatorVHP`

**Engineering Context & Operational Architecture**:
1. 400 Vials/Minute Monoblock Continuous / Indexing Architecture:
   - High-throughput aseptic fill-finish for parenteral biologics, monoclonal antibodies (mAbs), and sterile injectable vaccines.
   - Closed isolator system maintaining Grade A / ISO 14644-1 Class 5 laminar air conditions with active continuous positive differential pressure (+45 Pa relative to Grade B background).
2. 10-Head Ceramic Rotary Valveless Piston Dosing Pumps:
   - Valveless ceramic piston and cylinder liner pairs (alumina/zirconia) with precision diamond-lapped clearance (2.0 to 3.0 um).
   - Combined rotary oscillating porting motion (intake port open 0-180 deg, discharge port open 180-360 deg) and linear axial displacement delivering 0.1 to 50.0 mL with +/-0.25% volumetric repeatability.
   - Non-Newtonian liquid formulation shear thinning corrections and ceramic friction thermal compensation.
3. 2oo3 Triple Modular Redundancy (TMR) Instrumentation Across 7 Critical CQA Sensor Banks:
   - Dual-pan EMFR (Electro-Magnetic Force Restoration) high-speed tare balances LC-101A/B/C [mg].
   - Dual-pan EMFR high-speed gross balances LC-102A/B/C [mg].
   - Grade A isolator differential pressure transducers PT-201A/B/C [Pa].
   - UV-spectrophotometric vaporized hydrogen peroxide (VHP) concentration sensors AT-301A/B/C [ppm].
   - Glove port dynamic wireless pressure decay leak sensors PT-401A/B/C [Pa].
   - Hot-wire anemometers for vertical laminar airflow velocity VT-501A/B/C [m/s].
   - Piezoelectric quartz dynamic crimp sealing force load cells FT-601A/B/C [N].
   - Pairwise discrepancy timers, tolerance checks, latched faults, and bumpless fallback (2oo3 -> 1oo2 -> 1oo1 -> Failsafe).
4. Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E_w w_k, y_k = C x_k + D u_k$) at Ts = 5 ms:
   - 12 states: Ceramic piston linear stroke, piston velocity, rotary valve angle, chamber dynamic fluid pressure, diving needle vertical position, needle vertical velocity, vial liquid meniscus elevation, EMFR coil current error, isolator differential pressure, vertical laminar airflow velocity, VHP vapor concentration, chamber relative humidity.
   - 8 control inputs: Linear piston stroke servo %, rotary valve servo %, diving needle servo %, peristaltic micro-trim stroke %, supply air blower VFD %, exhaust damper %, VHP flash vaporizer rate %, capper servo force %.
   - 4 disturbances: Formulation viscosity drift, manifold pulsation ripple, glove port displacement surge, ambient barometric pressure variation.
   - 8 measurement outputs with steady-state Kalman filter innovation update matrix K (12x8).
5. Receding-Horizon Model Predictive Control (MPC):
   - Unrolled Projected Gradient Descent (PGD) with 8 iterations minimizing quadratic tracking cost Q on needle clearance (2.5 mm above rising liquid meniscus) and isolator pressure (+45 Pa), effort cost R, slew cost S, and terminal cost P.
   - Completely eliminates needle submergence droplet contamination and liquid splashing / aerosol generation at 400 vials/min.
6. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stage 0: Isolator Automated Pressure Decay Leak Rate Test (ISO 10648-2 Class 1/2)
   - Stage 1: VHP Bio-Decontamination Conditioning (Heating to 30 deg C, Dehumidification < 25% RH)
   - Stage 2: H2O2 Vapor Injection & Bio-Decontamination Dwell (1,200 ppm, 6-log Spore Kill)
   - Stage 3: Catalytic Aeration & Residual Gas Purge (< 0.80 ppm)
   - Stage 4: Grade A Unidirectional Laminar Airflow Stabilization (+45 Pa Lock)
   - Stage 5: Continuous Vial Infeed Starwheel Electronic Cam Synchronization (400 VPM)
   - Stage 6: In-Line 100% Dual-Pan EMFR Tare Weighing
   - Stage 7: Synchronous Bottom-Up Needle Dive & 10-Head Ceramic Piston Dosing
   - Stage 8: Needle Retract with Anti-Drip Reverse Suckback & Headspace N2 Purging
   - Stage 9: In-Line 100% Gross Checkweighing & Real-Time Trend Volume Trimming
   - Stage 10: 24-Pocket Rotary Vacuum Stopper Pick & Seat Insertion
   - Stage 11: 16-Head Rotary Aluminum Cap Servo Crimping & RSF Integrity Verification
   - Stage 12: Outfeed Defect Starwheel Pneumatic Air-Puff 3-Bin Ejection Dispatch
   - Stage 13: Isolator Barrier Breach Emergency Containment Lockdown
7. Statistical Process Control (SPC) & Quality Assurance:
   - 30-vial circular history buffers computing moving Mean, Variance, Standard Deviation (sigma), Cp, and Cpk in real-time.
   - Closed-loop PI feedback to 10 independent micro-peristaltic compensator pumps for zero-drift long-run production.
8. ISA-18.2 Multi-Tiered Alarm Engine & Bit-Packed Telemetry:
   - Bit-packed DWORDs: dwStatus_FSM_Phase, dwStatus_Pumps_Active, dwAlarm_Critical_Trips, dwAlarm_Process_Warnings, dwTMR_Sensor_Health, dwSPC_Quality_Flags.

Generate a complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Pharma_AsepticFilling_RotaryPistonPump_IsolatorVHP` with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phase1_tmr.get_phase1_tmr(),
        build_st_phase2_state_space.get_phase2_state_space(),
        build_st_phase3_mpc.get_phase3_mpc(),
        build_st_phase4_fsm.get_phase4_fsm(),
        build_st_phase5_pumps_dosing.get_phase5_pumps_dosing(),
        build_st_phase6_alarms_spc.get_phase6_alarms_spc()
    ])

    print("Verifying internal Structured Text code...")
    errs = validate_iec.validate_iec_st(st_code)
    if errs:
        print("INTERNAL IEC-ST VALIDATION FAILED:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    print(f"Internal IEC-ST Validation passed with 0 errors! Code size: {len(st_code)} characters")

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

    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{agent_id}.json"
    os.makedirs(os.path.dirname(output_filename), exist_ok=True)

    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset successfully written to {output_filename}")
    print(f"Total file size on disk: {os.path.getsize(output_filename)} bytes")
    print(f"Assistant content character count: {len(assistant_content)}")

    print(f"Executing external validation script on {output_filename}...")
    val_errs = validate_iec.validate_json_file(output_filename)
    if val_errs:
        print("EXTERNAL JSON VALIDATION FAILED:")
        for e in val_errs:
            print(" -", e)
        sys.exit(1)
    print("EXTERNAL JSON VALIDATION PASSED WITH 0 ERRORS!")
    return output_filename, len(assistant_content), agent_id

if __name__ == "__main__":
    fn, chars, aid = build_dataset()
    print(f"\nSUCCESS: Agent {aid} generated {chars} characters in {fn}")
