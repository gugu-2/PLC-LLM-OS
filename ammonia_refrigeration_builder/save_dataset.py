# ammonia_refrigeration_builder/save_dataset.py

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
import build_st_phases_7_to_10
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete state-space matrices (A, B, C, D, Ew, K), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Industrial Cold Chain & Cold Storage (HVAC-R Heavy Industry) — Industrial Anhydrous Ammonia (NH3 / R717) Multi-Stage Screw Compressor Rack: Economizer Flash Plate Subcooling, Floating Head Pressure Evaporative Condenser Tracking Wet-Bulb Temperature with Minimum Safety Floor, 4-Zone Sequenced Reverse Hot-Gas Defrost Management with Soft Equalization Repressurization Bleed, 2oo3 TMR Instrumentation Voting (Suction Header Pressure PT-101A/B/C, Compressor Discharge Temperature TT-201A/B/C, Lubricating Oil Differential Pressure PDT-301A/B/C, Machinery Room Life-Safety Ammonia Gas Detectors AT-401A/B/C, Economizer Intermediate Pressure PT-501A/B/C, Condenser Manifold Pressure PT-601A/B/C, Psychrometric Wet-Bulb Temperature TT-602A/B/C), and ANSI/IIAR 2-2021 & OSHA 1910.119 PSM Compliant Emergency Packed-Bed Acid Scrubber Interlocks.**

**Function Block Name**: `FB_HVAC_Industrial_AmmoniaRefrigeration_CompressorRack`

**Engineering Context & Operational Architecture**:
1. Industrial Ammonia Refrigeration Facility Specifications:
   - Central Cold Storage Distribution Hub & Blast Freezer Facility with 4,500 kW (1,280 TR) design capacity at -32.0 deg C evaporating temperature.
   - Primary Refrigerant: Pure Anhydrous Ammonia (NH3 / R717, GWP = 0, ODP = 0, Molecular Mass = 17.03 g/mol).
   - Compressor Train: Lead Compressor 1 (450 kW semi-hermetic twin-screw with 30-60 Hz VFD and continuous slide valve), Lag Compressor 2 (550 kW open-drive twin-screw base load), Lag Compressor 3 (550 kW open-drive twin-screw swing).
   - Economizer Flash Vessel Subcooler with dual stepper electronic expansion valves (EEV) and intermediate rotor cavity vapor injection (+18.5% COP improvement).
   - Heat Rejection Train: 3-cell induced draft evaporative condenser with EC fan VFDs, dual sump spray water recirculation pumps, and wet-bulb approach floating head control (minimum 8.5 bar floor).
   - Lubrication Loop: Thermosyphon oil cooler with 3-way mixing valve maintaining 45.0-55.0 deg C oil temperature, multi-stage coalescing demisters (< 3 ppm carryover), and dual variable-speed pre-lube pumps.
   - Evaporator Defrost Subsystem: 4-zone sequenced reverse hot-gas defrost with 4-stage soft repressurization bleed management to prevent liquid slugging and hydraulic water-hammer.
   - Life-Safety Architecture: ANSI/IIAR 2-2021, ANSI/ASHRAE 15-2022, and OSHA 29 CFR 1910.119 PSM compliance with two-stage emergency acid scrubber ventilation fan interlocks.
2. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - Median computation, deviation calculation, discrepancy timers (1.0 s trip threshold), and bumpless degradation across 7 channels: Suction Pressure (PT-101), Discharge Temp (TT-201), Oil DP (PDT-301), Ambient NH3 (AT-401), Economizer Pressure (PT-501), Condenser Pressure (PT-601), and Wet-Bulb Temp (TT-602).
3. Cyber-Physical Discrete State-Space Model ($x_{k+1} = A x_k + B u_k + E_w w_k, y_k = C x_k + D u_k$):
   - 8 states: Suction pressure deviation, suction enthalpy deviation, discharge pressure deviation, discharge temperature deviation, oil sump temperature deviation, economizer pressure deviation, condenser basin water temperature deviation, suction superheat deviation.
   - 6 controls: Lead slide valve %, Lead VFD speed Hz, Lag slide valve %, Economizer EEV %, Condenser fan %, Oil 3-way valve %.
   - 3 disturbances: Wet-bulb deviation, warehouse thermal load shock, hot-gas defrost vapor mass flow diversion.
   - Steady-state Kalman observer innovation update: $x_{hat} = x + K (y_{meas} - C x)$.
   - Real-time thermodynamic saturation polynomials: R717 Tsat, superheat, vapor density, compression ratio, swept displacement, mass flow, kW/TR specific power, and COP.
4. Receding-Horizon Model Predictive Control (MPC):
   - Unrolled Projected Gradient Descent (PGD) optimization (6 iterations) minimizing quadratic cost $J = sum( (x - r)^T Q (x - r) + u^T R u + Delta_u^T S Delta_u )$, with dynamic floating head setpoint tracking, actuator box constraints, and physical slew rate limiting.
5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - States 0 to 14: Cold Initialize, Pre-Lube Circulation, Standby Ready, Lead Soft-Start, Base Load Regulation, Lag Stage-Up Sequence, Multi-Compressor Coordination, Economizer Subcooling Active, Floating Condensing Control, Defrost Pump-Down, Defrost Hot-Gas Feed, Defrost Bleed-Down Repressurization, Lag Stage-Down Sequence, Controlled Deceleration Standby, Emergency Ammonia Toxic Ventilation & Acid Scrubber Mitigation.
6. ISA-18.2 Multi-Tiered Alarm Engine & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low trip points with clearance deadbands and first-out fault latching for all process parameters.
   - 32-bit status, alarm, and interlock telemetry word packaging.

Generate a complete, production-grade IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_HVAC_Industrial_AmmoniaRefrigeration_CompressorRack` with zero placeholders, full mathematical expansions, and complete variable declarations."""

    st_code = "\n".join([
        build_st_header_io.get_header_and_io(),
        build_st_var.get_var_declarations(),
        build_st_matrices.get_matrices_initialization(),
        build_st_phases_1_to_3.get_phases_1_to_3(),
        build_st_phases_4_to_6.get_phases_4_to_6(),
        build_st_phases_7_to_10.get_phases_7_to_10()
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
    else:
        print("OFFICIAL JSON VALIDATION PASSED WITH 0 ERRORS!")
        return filename, len(assistant_content), agent_id

if __name__ == "__main__":
    fn, chars, aid = build_dataset()
    print(f"DONE! File: {fn}, Characters: {chars}, AgentID: {aid}")
