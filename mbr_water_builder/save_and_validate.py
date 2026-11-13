# Save MBR dataset to data/swarm_raw/agent_<uuid>.json and validate
import sys
import os
import json
import uuid

# Read full ST code
with open("test_mbr.st", "r", encoding="utf-8") as f:
    st_code = f.read()

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Advanced Water & Industrial Wastewater Treatment (Tier 1 Priority Sector): 50,000 m3/day Submerged Membrane Bioreactor (MBR) Cassette Facility with Multi-Train PVDF Hollow-Fiber Filtration, Darcy Resistance-In-Series Observer with Dynamic Viscosity Temperature Correction, 2oo3 TMR Critical Instrumentation Voting, Receding-Horizon MPC Optimization with Projected Gradient Descent, 14-Stage Production FSM, and ISA-18.2 Alarm Hierarchy.**

**Function Block Name**: `FB_Water_MBR_MembraneBioreactor_TMP_CIP`

**Engineering Context & Operational Architecture**:
1. Facility Architecture & Membrane Hydraulics:
   - 50,000 m3/day nominal production across 8 parallel submerged filtration trains, each containing 12,500 m2 PVDF hollow-fiber membrane modules (0.04 um pore size).
   - Darcy's law resistance-in-series dynamic fouling model separating intrinsic clean membrane resistance Rm, reversible dynamic cake layer resistance Rc, and irreversible pore fouling Rp.
   - Arrhenius-Poiseuille water viscosity temperature correction model (mu_20 = 1.002 mPa.s) ensuring true normalized TMP (20 deg C) and accurate specific permeability tracking (LMH/bar).
2. 2oo3 Triple Modular Redundancy (TMR) Voting Architecture:
   - 6 critical dual/triple-redundant sensor channels: Permeate Header Suction Pressure (PT-101A/B/C), Bioreactor MLSS Optical Turbidity (AT-102A/B/C), Basin Luminescent Dissolved Oxygen LDO (AT-103A/B/C), Pre-Anoxic Denitrification ORP (AT-104A/B/C), Permeate Discharge Electromagnetic Flowmeters (FT-105A/B/C), and Coarse-Bubble Air Scour Distribution Pressure (PT-106A/B/C).
   - Pairwise discrepancy debouncing timers (2.5 s threshold), automated discordant channel isolation, median voting when triple-healthy, 1oo2 averaging when single-degraded, single sensor fallback on double-degraded, and failsafe defaults with bumpless rate filtering.
3. 8-State Cyber-Physical Discrete State-Space Model (Ts = 25 ms):
   - 8 states: [1] Net Permeate Flux J [LMH], [2] Permeate Suction Pressure P_perm [mbar], [3] Transmembrane Pressure TMP [mbar], [4] Dynamic Cake Resistance Rc [10^11 m^-1], [5] Bioreactor Dissolved Oxygen DO [mg/L], [6] Mixed Liquor Suspended Solids MLSS [mg/L], [7] Nitrate-Nitrogen NO3-N [mg/L], [8] Air Scour Flow Q_air [Nm3/h].
   - 8 control inputs: Suction Pump VFD, Backpulse Pump VFD, Scour Blower VFD, Aeration Fine-Bubble Valve, MLR Recycle Pump, WAS Draw Pump, NaOCl Dosing Pump, Citric Acid Dosing Pump.
   - 8 exogenous disturbances: Water Temp, Hydrostatic Basin Level, Influent COD, Influent TKN, Influent Flow, SVI, EPS, Barometric Pressure.
   - Full discrete state-space propagation and Luenberger state observer innovation update.
4. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) over prediction horizon Np = 5 and control horizon Nc = 3.
   - Physical actuator box constraints [u_min, u_max] and dynamic slew rate limiters (Delta_u_max <= 2.5 %/scan).
5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - [0] Standby, [1] Pre-Fill, [2] Pre-Scour, [3] Flux Ramp, [4] Forward Permeation (540 s), [5] Air Relaxation (60 s), [6] Permeate Backpulse (45 s), [7] Air Scour Boost (30 s), [8] CEB Hypochlorite Soak (1200 s), [9] CEB Citric Acid Soak (1800 s), [10] Displacement Flush (180 s), [11] Aeration DO & SRT Trim, [12] High-TMP Cake Abort, [13] Recovery CIP Drain & Soak.
6. ISA-18.2 Multi-Tier Process Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low, and Rate-of-Change trips with clearance deadbands and 32-bit status, alarm, and diagnostic DWORDs.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Water_MBR_MembraneBioreactor_TMP_CIP` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

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
