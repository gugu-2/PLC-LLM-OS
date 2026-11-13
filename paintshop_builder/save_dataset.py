# paintshop_builder/save_dataset.py

import os
import sys
import json
import uuid

# Add current workspace and builder directory to sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import build_st_header_io
import build_st_var
import build_st_matrices
import build_st_phases_1_to_3
import build_st_phases_4_to_6
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete state-space matrices (A, B, C, D, Ew, K_obs), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Automotive Manufacturing & Surface Finishing (Tier 1 Priority Sector) — Automotive Robotic Paint Application Booth: High-Speed Electrostatic Bell Rotary Atomizers (65,000 rpm air turbine, -90 kV high voltage electrostatic cascade), Micro-Gear Pump Closed-Loop Paint Flow Dosing (50-600 mL/min), Downdraft Recirculation Laminar Air Flow Balancing (0.35 m/s ± 0.02 m/s, delta-P 12.5 Pa), Regenerative Thermal Oxidizer (RTO) VOC Abatement Interlocks, Rapid Color-Change Valve Block (CCV) Chop-Chop Solvent Purge (< 12 s), and Sub-5 ms Fast Electrostatic Arc Flash Quench / Voltage Collapse Interlocks.**

**Function Block Name**: `FB_Automotive_PaintShop_RoboticBellAtomizer_AirFlowBalance`

**Engineering Context & Operational Architecture**:
1. Automotive Paint Shop Robotic Bell Atomizer Workcell Specifications:
   - Body-in-White (BIW) / Clearcoat robotic application booth handling continuous conveyor lines at 60 jobs per hour (JPH).
   - High-Speed Air Turbine Bell Atomizers operating between 10,000 and 65,000 rpm with dynamic proportional drive and brake air pressure regulation.
   - Electrostatic High-Voltage Cascade delivering -30.0 to -90.0 kV direct potential with integrated microamp return leakage current monitoring (0 to 500 uA) and sub-5 ms arc detection.
   - Closed-Loop Paint Volumetric Dosing: Precision positive-displacement micro-gear pump (1.2 to 2.4 cc/rev) with servo drive delivering 50.0 to 600.0 mL/min, verified by inline micro-Coriolis mass flowmeters.
   - Dual Shaping Air Shrouds: Inner shaping shroud air (0.5 to 5.0 bar) focusing droplet cloud and preventing cup rim back-contamination, and Outer shaping shroud air (0.5 to 5.0 bar) controlling spray pattern fan width (100 to 450 mm) and panel overlap.
   - Downdraft Recirculation Laminar Air Balancing: Conditioned cleanroom ceiling plenum pushing air downward at 0.35 m/s ± 0.02 m/s across floor grating to water scrubber / dry separation box, maintaining 12.5 Pa differential pressure via variable air volume (VAV) dampers and exhaust recirc VFDs.
   - Rapid Color-Change Valve Block (CCV): Robot arm-mounted manifold performing alternating solvent/air "chop-chop" purge, high-velocity air drying, and fast paint pre-fill in under 12 seconds with minimum paint loss (< 15 mL).
   - Regenerative Thermal Oxidizer (RTO) VOC Abatement: Real-time volatile solvent emission tracking with dilution damper modulation, keeping booth exhaust solvent vapor below 25% LEL with immediate safety interlock trip at 40% LEL.
2. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting Suite:
   - Median calculation, deviation calculation, discrepancy timers (250 ms threshold), and bumpless degradation across 4 critical sensor channel groups:
     * Channel Group 1: High-Speed Optical Bell Turbine Speed Pickups ST-101A/B/C [rpm]
     * Channel Group 2: High-Voltage Electrostatic Cascade Dividers VT-201A/B/C [kV]
     * Channel Group 3: Micro-Coriolis Mass Flowmeter Dosing Transmitters FT-301A/B/C [mL/min]
     * Channel Group 4: Downdraft Static Differential Pressure Transmitters PT-401A/B/C [Pa]
3. Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E_w w_k, y_k = C x_k + D u_k$) at Ts = 0.010 s (10 ms):
   - 8 states: Bell turbine speed deviation, Electrostatic voltage deviation, Paint line pressure deviation, Paint flow rate deviation, Inner shaping air deviation, Outer shaping air deviation, Downdraft static pressure drop deviation, Exhaust VOC flammability concentration deviation.
   - 6 controls: Turbine drive air command %, High voltage cascade PWM command %, Micro-gear pump speed rpm, Inner shaping air pressure bar, Outer shaping air pressure bar, Downdraft VAV damper command %.
   - 3 disturbances: Robot TCP centrifugal acceleration / fluid head surge, Paint dynamic viscosity fluctuation, Booth draft velocity disturbance.
   - Steady-state Kalman observer innovation update: $x_{hat} = x_{pred} + K_{obs} (y_{meas} - C x_{pred} - D u)$.
   - Real-time hydrodynamic atomization models: Bell cup rim linear velocity, Weber number, droplet Sauter Mean Diameter D32 empirical correlation, electrostatic field strength, specific charge-to-mass ratio, electrostatic transfer efficiency, spray fan width, real-time Dry Film Thickness (DFT) observer (35 μm ± 2 μm target), and RTO VOC mass emission rate.
4. Receding-Horizon Model Predictive Control (MPC):
   - Unrolled Projected Gradient Descent (PGD) optimization (6 iterations) minimizing quadratic cost $J = sum( (x - r)^T Q (x - r) + u^T R u + Delta_u^T S Delta_u ) + (x_N - r_N)^T P (x_N - r_N)$, with dynamic edge wrap and recess compensation setpoint modification, actuator box constraints, and physical slew rate limiting.
5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - Stages 0 to 13: FSM_BOOT_IDLE, FSM_PREPURGE_VENTILATION, FSM_DOWNDRAFT_AIR_BALANCE_LOCK, FSM_HV_CASCADE_DIAGNOSTICS, FSM_COLOR_BLOCK_SOLVENT_FLUSH, FSM_HIGH_VELOCITY_AIR_DRY, FSM_PAINT_FLUID_FAST_PREFILL, FSM_BELL_TURBINE_RAMPUP, FSM_HV_CHARGE_ENABLE, FSM_CAR_BODY_ROBOT_SPRAY, FSM_EDGE_WRAP_RECESS_COMPENSATION, FSM_BELL_CUP_TIP_WASH, FSM_RTO_VOC_BURNER_MODULATION, FSM_SPARK_ARC_QUENCH_TRIP.
6. ISA-18.2 Multi-Tiered Process Alarm Engine & Bit-Packed Telemetry:
   - High-High, High, Low, Low-Low trip points with clearance deadbands and first-out fault latching.
   - Sub-5 ms electrostatic arc flash detection ($dI/dt \ge 120\text{ uA/ms}$ or $I \ge 380\text{ uA}$) triggering instantaneous voltage collapse, hardware crowbar safety grounding, dynamic turbine braking, and fluid line dump.
   - 32-bit status, alarm, and interlock telemetry word packaging.

Generate a complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Automotive_PaintShop_RoboticBellAtomizer_AirFlowBalance` with zero placeholders, full mathematical expansions, and complete variable declarations."""

    print("Assembling Structured Text code...")
    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phases_1_to_3.get_phases_1_to_3(),
        build_st_phases_4_to_6.get_phases_4_to_6()
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

    print(f"Dataset successfully written to {filename}")
    print(f"Assistant content character count: {len(assistant_content)}")

    print("\nRunning official validate_iec.py file check...")
    file_errs = validate_iec.validate_json_file(filename)
    if file_errs:
        print("OFFICIAL JSON VALIDATION FAILED:")
        for e in file_errs:
            print(" -", e)
        sys.exit(1)
    print("OFFICIAL JSON VALIDATION PASSED PERFECTLY!")
    return filename, len(assistant_content), agent_id

if __name__ == "__main__":
    build_dataset()
