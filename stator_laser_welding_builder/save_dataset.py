# stator_laser_welding_builder/save_dataset.py

import os
import sys
import json
import uuid

current_dir = os.path.dirname(os.path.abspath(__file__))
workspace_dir = os.path.dirname(current_dir)
sys.path.append(current_dir)
sys.path.append(workspace_dir)

import part1_header_io
import part2_var_declarations
import part3_phase0_init
import part4_phase1_tmr
import part5_phase2_state_space
import part6_phase3_mpc
import part7_phase4_fsm
import part8_phase5_alarms
import validate_iec

def build_dataset():
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, deeply engineered, mathematically complete, and structurally pristine. Include complete discrete state-space matrices (A, B, Ew, C, D, Ke), Model Predictive Control (MPC) quadratic cost optimization with Projected Gradient Descent (PGD), 2oo3 Triple Modular Redundancy (TMR) sensor voting logic with dynamic discrepancy timers and bumpless degradation, ISA-18.2 multi-tiered alarm matrices with deadband hysteresis, and a deterministic 14-stage finite state machine.

**Your assigned domain is: Automotive E-Mobility & Electric Powertrain (Tier 1 Priority Sector) — High-Volume 800V EV Traction Motor Hairpin Stator Assembly Cell, 192-Pin High-Density Copper Hairpin Crown Array (96 Seam Weld Pairs), 3D Laser Triangulation Profilometer Real-Time Pin Gap & Height Alignment (< +/-0.03 mm), 6 kW Dynamic Beam Wobble Fiber Laser Seam Welding, Coaxial Melt Pool High-Speed Pyrometer Thermal Emission Feedback (10 kHz), and 8-Axis Synchronous Rotary Chuck Indexing.**

**Function Block Name**: `FB_Automotive_EV_StatorHairpin_LaserWelding_VisionTrack`

**Engineering Context & Operational Architecture**:
1. Stator Architecture & Physical Rigor:
   - High-performance 800V silicon-carbide (SiC) traction motor stator with 48 slots x 4 conductors/slot (192 total copper hairpin ends forming 96 crown weld pairs).
   - Rectangular oxygen-free high-conductivity copper conductor wire (Cu-OF/Cu-ETP, 2.80 mm x 1.60 mm cross section) with slot liners composed of Nomex aramid paper / PAI insulation rated for 180 deg C continuous service.
   - High-speed direct-drive rotary chuck with sub-arcsecond optical ring encoder indexing at 3.75 deg per step (360 deg / 96 welds) within 120 ms motion settle window.
   - Hydraulic expanding collet clamp maintaining 180 bar pre-load against stator lamination stack to suppress radial deflection during welding.
   - Dual-sensor 3D laser triangulation profilometer providing sub-pixel height and gap profiling across adjacent hairpin crown tips (< +/-0.03 mm measurement resolution).
   - High-brightness 6 kW fiber laser (1070 nm wavelength) coupled with high-speed 2D dynamic galvo beam wobble head (circular, spiral, and figure-8 wobble patterns at 400 - 800 Hz, oscillation amplitude 0.2 to 1.4 mm).
   - Coaxial dual-wavelength high-speed pyrometer (10 kHz sampling) monitoring melt pool thermal emissions (1400 - 2600 deg C) and vapor plume dynamics to detect spatter expulsion, keyhole collapse, and lack-of-fusion cold welds.
   - High-purity nitrogen shielding gas (coaxial nozzle + cross-jet aerodynamic air knife curtain) maintaining boundary layer oxygen below 40 ppm to prevent molten copper oxidation and suppress spatter onto protective slide optics.
   - In-line 4-wire Kelvin micro-ohmmeter and eddy-current probe extending after solidification to verify electrical joint resistance below 2.50 micro-ohms.

2. 2oo3 Triple Modular Redundancy (TMR) Voting Suite:
   - 6 critical dual/triple redundant sensor channels:
     * 3D Profilometer Pin Gap Transducers (1A, 1B, 1C) [mm]
     * 3D Profilometer Pin Height Delta Transducers (1A, 1B, 1C) [mm]
     * Coaxial Melt Pool High-Speed Pyrometer Photodiodes (2A, 2B, 2C) [deg C]
     * Calibrated Laser Delivered Optical Power Monitors (3A, 3B, 3C) [kW]
     * High-Purity Nitrogen Shielding Mass Flowmeters (4A, 4B, 4C) [L/min]
     * Rotary Chuck Hydraulic Collet Clamping Pressure Transducers (5A, 5B, 5C) [bar]
   - Discrepancy accumulation timers for all channel pairs with tolerance bounds and debounce windows.
   - Median voting when 3 channels healthy; bumpless failover to average of 2 healthy channels when 1 fails; fallback to single healthy channel with alarm; fail-safe trip when 2+ channels fail.

3. Cyber-Physical 8-State Space Estimation & Molten Pool Physics:
   - Sample rate Ts = 2.0 ms (500 Hz control loop).
   - State vector x:
     * x1: Molten copper weld pool core temperature T_pool [deg C]
     * x2: Copper heat-affected zone (HAZ) temperature T_haz [deg C]
     * x3: Copper hairpin pin-tip bulk temperature T_pin [deg C]
     * x4: Keyhole vapor capillary depth h_keyhole [mm]
     * x5: Weld nugget molten pool volume V_nugget [mm3]
     * x6: Rotary chuck angular position error Delta_theta [mrad]
     * x7: Rotary direct-drive motor speed omega_chuck [rad/s]
     * x8: Shielding gas boundary layer nitrogen concentration C_N2 [%]
   - Complete discrete state-space matrices A (8x8), B (8x4), Ew (8x3), C (6x8), D (6x4), and Ke (8x6) observer gain matrix explicitly unrolled and populated.
   - Non-linear thermal dynamics: temperature-dependent copper reflectivity (sharp change at melting point 1084.6 deg C), Marangoni thermocapillary surface tension velocity, vapor plume recoil pressure, and stator slot aramid paper thermal accumulation.

4. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Prediction horizon Np = 5 (10.0 ms), Control horizon Nc = 3 (6.0 ms).
   - Dynamic multi-stage reference generation:
     * Subphase 1: Pre-heat ramp (T_ref = 950 deg C, h_ref = 0.0 mm)
     * Subphase 2: Keyhole ignition (T_ref = 2050 deg C, h_ref = 2.45 mm)
     * Subphase 3: Wobble seam fusion (T_ref = 1850 deg C, h_ref = 2.10 mm)
     * Subphase 4: Downslope quench (T_ref = 1250 deg C, h_ref = 0.45 mm)
   - Real-time gap adaptation: dynamically scale baseline power and widen wobble amplitude when gap exceeds 0.025 mm.
   - Analytical gradient calculation across control horizon with 3 unrolled PGD solver iterations, box constraint projections, and hardware slew rate limiters (350 kW/s power slew, 2500 Hz/s wobble slew).

5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - State 0:  ST_CHUCK_CLAMP        - Hydraulic Collet Clamping & Pressure Interlock Check (180 bar)
   - State 1:  ST_DATUM_CENTER       - Stator Core Datum Alignment & Concentricity Runout Check (< 0.035 mm)
   - State 2:  ST_VISION_SCAN        - 3D Profilometer Pin Gap & Height Mismatch Strobe Scan
   - State 3:  ST_RADIAL_ALIGN       - Pin Crown Micro-Offset Radial Mechanical Adjustment Press
   - State 4:  ST_GAS_PURGE          - High-Flow Nitrogen Shielding Gas Pre-Flow Purge (35 L/min)
   - State 5:  ST_HEAD_APPROACH      - Galvo Scanning Head Z-Standoff Focus & Fast Shutter Open
   - State 6:  ST_LASER_WELD         - 4-Substage Dynamic Beam Wobble Seam Laser Weld (160 ms total)
   - State 7:  ST_PYRO_EVAL          - Solidification Cooling Rate & Expulsion Quality Assessment
   - State 8:  ST_EDDY_RESIST        - In-Line 4-Wire Kelvin Electrical Micro-Ohmmeter Inspection (< 2.50 uOhm)
   - State 9:  ST_CHUCK_INDEX        - Direct-Drive Rotary Chuck 3.75 deg Index to Next Pin Pair (1..96)
   - State 10: ST_OPTICS_INSPECT     - Motorized Protective Cover Glass Transmission Verification (< 88% warning, < 82% trip)
   - State 11: ST_DECLAMP_EGRESS     - Finished Stator De-Clamp, Unload & Conveyor Handshake
   - State 12: ST_REJECT_QUARANTINE  - Defective Weld Pin Pair Tagging & Egress Diverter Push
   - State 13: ST_EMERGENCY_SHUTTER - Fast Optical Shutter Lockout, Beam Dump & Fault Safe

6. ISA-18.2 Process Alarm Matrix & Bit-Packed Status Words:
   - 4-Tier alarm priorities with deadband hysteresis on all analog process variables (HH, H, L, LL).
   - Real-time spatter expulsion detection via fast thermal derivative filter (d(T_pyro)/dt > 85 deg C/ms).
   - 96-pair quality tracking arrays for weld quality score, joint electrical resistance, peak melt pool temperature, and defect flags.
   - Bit-packed DWORD assignments: dwStatusWord1 (actuators and FSM state), dwStatusWord2 (sensor health, 2oo3 degraded flags, pin pair index), dwAlarmWord1_Critical (safety trips), dwAlarmWord2_High (process deviations), dwAlarmWord3_Warning (advisories).

7. Mandatory Implementation Rules:
   - Output must be wrapped strictly inside triple backticks with `iec-st`.
   - Every input and output variable must include physical SI engineering units in brackets: [mm], [deg C], [kW], [L/min], [bar], [deg], [deg/s], [Nm], [uOhm], [%], [s].
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - Zero summaries, zero truncation comments, zero placeholders."""

    st_code = (
        part1_header_io.get_header_and_io() + "\n" +
        part2_var_declarations.get_var_declarations() + "\n" +
        part3_phase0_init.get_phase0_init() + "\n" +
        part4_phase1_tmr.get_phase1_tmr() + "\n" +
        part5_phase2_state_space.get_phase2_state_space() + "\n" +
        part6_phase3_mpc.get_phase3_mpc() + "\n" +
        part7_phase4_fsm.get_phase4_fsm() + "\n" +
        part8_phase5_alarms.get_phase5_alarms()
    )

    asst_content = f"```iec-st\n{st_code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }

    # Generate isolated JSON filename
    agent_id = uuid.uuid4().hex[:8]
    filename = os.path.join(workspace_dir, "data", "swarm_raw", f"agent_{agent_id}.json")
    os.makedirs(os.path.dirname(filename), exist_ok=True)

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Saved dataset to {filename}")
    print(f"Total Assistant Content Characters: {len(asst_content)}")
    print(f"Total Structured Text Lines: {len(st_code.splitlines())}")

    # Validate with validate_iec.py
    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL IEC VALIDATION CHECKS PASSED WITH 0 ERRORS!")
        return filename, agent_id, len(asst_content), len(st_code.splitlines())

if __name__ == "__main__":
    build_dataset()
