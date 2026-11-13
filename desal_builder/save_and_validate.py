# desal_builder/save_and_validate.py
import sys
import os
import json
import uuid

# Read full ST code
with open("test_desal.st", "r", encoding="utf-8") as f:
    st_code = f.read()

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Municipal & Industrial Water Desalination (Heavy Infrastructure Tier 1 Priority): 50,000 m3/day Seawater Reverse Osmosis (SWRO) Desalination Train with Multi-Stage High-Pressure Centrifugal Feed Pumps (65-82 bar), Isobaric Energy Recovery Devices (ERD / ERI PX-300 Pressure Exchanger Array), PX Booster Pump Differential Pressure Synchronization, Darcy-Pitzer Osmotic Flux & Polarization Observer, Receding-Horizon MPC Optimization with Projected Gradient Descent, 2oo3 TMR Sensor Suite with Dechlorination ORP Membrane Protection, 14-Stage Production FSM, and ISA-18.2 Alarm Hierarchy.**

**Function Block Name**: `FB_Water_Desalination_SWRO_EnergyRecoveryDevice`

**Engineering Context & Operational Architecture**:
1. Facility Architecture & Membrane Hydraulics:
   - 50,000 m3/day nominal permeate production capacity across parallel high-pressure polyamide thin-film composite (TFC) membrane racks (total membrane surface area 125,000 m2).
   - High-Pressure Multi-Stage Centrifugal Feed Pumps (HPP) supplying 65.0 to 82.0 bar with high-inertia medium-voltage VFDs.
   - Isobaric Rotary Energy Recovery Devices (ERI PX-300 pressure exchanger array) recovering hydraulic pressure from high-salinity concentrate brine (60-78 bar) and pressurizing low-pressure raw seawater with >96% volumetric efficiency.
   - PX Booster Pump VFD adding 2.0 to 4.5 bar differential head to synchronize ERD discharge with the HPP feed header and prevent cross-manifold recirculation.
   - Pitzer-van 't Hoff osmotic pressure thermodynamic model with Arrhenius-Poiseuille water viscosity and salt diffusion temperature compensation (standard temp 25.0 deg C), tracking concentration polarization beta and net driving pressure (NDP).
2. 2oo3 Triple Modular Redundancy (TMR) Voting Suite:
   - 6 critical dual/triple-redundant transmitter channels: Raw Seawater Intake Pressure (PT-101A/B/C), High-Pressure Feed Header Pressure (PT-201A/B/C), Combined Permeate Conductivity Analyzer (AT-301A/B/C), ERD HP Brine Reject Flow (FT-401A/B/C), Feed Dechlorination Redox ORP Analyzer (AT-102A/B/C), and PX Booster Discharge Pressure (PT-501A/B/C).
   - Pairwise discrepancy debouncing timers (1.0 to 3.0 s threshold), automated discordant channel invalidation, median voting when triple-healthy, arithmetic averaging on single failure, single-channel fallback with degraded latching, and fail-safe defaults with bumpless rate filtering.
   - Critical Membrane Safety Interlock: AT-102 ORP voting guards polyamide membranes against free chlorine breakthrough (ORP > 280 mV initiates emergency trip).
3. 8-State Cyber-Physical Discrete State-Space Model (Ts = 10 ms):
   - 8 states: [1] HP Feed Pressure P_feed [bar], [2] Net Driving Pressure NDP [bar], [3] Membrane Permeate Flux J_v [LMH], [4] Surface Osmotic Pressure Pi_bar [bar], [5] ERD HP Brine Pressure P_erd [bar], [6] ERD Salinity Mixing Leak Delta_C_mix [ppm], [7] Permeate Salinity C_perm [uS/cm], [8] Specific Permeability Kw [LMH/bar].
   - 6 control inputs: HPP VFD Frequency, PX Booster VFD Frequency, Brine Throttle Valve Position, Antiscalant Metering Stroke, Sodium Bisulfite Dosing Stroke, Permeate Flush/Divert Valve Position.
   - 6 exogenous disturbances: Seawater TDS, Temperature, Intake LP Pressure, Feed ORP, SDI-15, and pH.
   - Complete discrete state-space propagation and Luenberger state observer innovation update.
4. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) over prediction horizon Np = 5 and control horizon Nc = 3.
   - Optimizes HPP and PX Booster VFD speeds to minimize Specific Energy Consumption (SEC in kWh/m3) subject to recovery bounds (38.0 - 44.5%), permeate conductivity (< 400 uS/cm), and slew-rate limits (0.5 Hz/s).
5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - [0] Standby, [1] LP Intake Priming & Deaeration, [2] Chemical Pre-conditioning (SBS Dechlorination & Antiscalant), [3] LP Flush & Header Equalization, [4] High Pressure Pump Soft Ramp-up (0.5 bar/s), [5] ERD Isobaric Wheel Engagement, [6] PX Booster Pump Sync, [7] Continuous Permeate Production (MPC Active), [8] Salinity Flux Surge Trim, [9] Antiscalant Auto-Tune (S&DSI), [10] Scheduled LP Permeate Flush (1.5 Volume), [11] CIP Acid Cleaning Soak (pH 2.0-2.5), [12] CIP Alkaline Disinfection Soak (pH 11.0-11.5), [13] Fast Emergency Depressurization (FED Trip).
6. ISA-18.2 Multi-Tier Process Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance deadbands and 32-bit status, alarm, and diagnostic DWORDs.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Water_Desalination_SWRO_EnergyRecoveryDevice` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

content = f"```iec-st\n{st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
output_filename = f"data/swarm_raw/agent_{agent_id}.json"

os.makedirs("data/swarm_raw", exist_ok=True)
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and saved to: {output_filename}")
print(f"Assistant content character count: {len(content)}")
print(f"Agent ID: agent_{agent_id}")
