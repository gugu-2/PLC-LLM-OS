# cbw_tunnel_washer_builder/save_and_validate.py
import sys
import os
import json
import uuid

# Read full ST code
with open("test_cbw.st", "r", encoding="utf-8") as f:
    st_code = f.read()

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Commercial Textile & Heavy Industrial Laundry (Tier 1 Priority Commercial Sector): Industrial Continuous Batch Tunnel Washer (CBW, 16-Compartment Drum, 60 kg/compartment batch size, 2,000 kg/h dry linen throughput), Counter-Flow Water Filtration & Heat Exchanger Reclamation Loops, Dynamic Live Steam Direct Injection Temperature Profiles (Pre-wash, Main Wash 85°C, Bleach 70°C, Rinse), 50-Bar Hydraulic Press Extractor Cake Dewatering Synchronization, Micro-Peristaltic Alkali/Detergent/Acid Neutralizer Chemical Dosing, 2oo3 TMR Sensor Suite, 14-Stage Production FSM, and ISA-18.2 Process Alarms.**

**Function Block Name**: `FB_Textile_ContinuousTunnelWasher_WaterEnergyRecovery`

**Engineering Context & Operational Architecture**:
1. Facility Architecture & Washer Drum Hydraulics:
   - 16-compartment continuous batch tunnel washer (CBW) processing 60 kg dry linen per compartment batch, achieving 2,000 kg/h dry linen production throughput.
   - Compartment distribution: Compartments 1-3 Pre-Wash zone (soil wetting, flush, 35-40°C), Compartments 4-8 Main Wash zone (saponification, alkali/detergent injection, direct live steam injection to 85°C thermal disinfection), Compartments 9-10 Bleach / Disinfection zone (oxygen bleach/PAA, 70°C), Compartments 11-14 Counter-Flow Rinse zone (clean water & recovered press water counter-flow cascade), Compartments 15-16 Finish / Souring zone (acid neutralizer souring to pH 5.5-6.5, softening agent).
   - Counter-flow water filtration with rotary lint screen, press water collection buffer tank, and shell-and-tube heat exchanger recovering dirty effluent thermal energy to preheat fresh makeup water.
2. 50-Bar High-Tonnage Hydraulic Cake Press Extractor:
   - High-pressure hydraulic ram press extracting water from linen cake discharged from compartment #16.
   - Multi-stage linear pressure profiling: Phase A (rapid downward travel to cake contact), Phase B (compaction ramp to 20 bar), Phase C (extraction ramp to 50 bar), Phase D (dwell hold at 50 bar for target moisture retention < 48%), and Phase E (decompression and ram retract to TDC).
   - Pneumatic bottom pusher ejector ring and synchronized shuttle conveyor transfer to downstream continuous tumble dryers.
3. 2oo3 Triple Modular Redundancy (TMR) Voting Suite:
   - 4 primary critical 2oo3 transmitter triplets: Main Wash Temperature (TT-101A/B/C), Rinse Conductivity (AT-201A/B/C), Press Hydraulic Pressure (PT-301A/B/C), and Cold Freshwater Flow (FT-401A/B/C).
   - Pairwise discrepancy debouncing timers (1.5 to 2.5 s threshold), automated outlier invalidation, median voting when triple-healthy, averaging on single sensor degradation, single-channel fallback, and fail-safe defaults with bumpless slew rate filtering.
   - Dual-redundant auxiliary telemetry: Drum Drive Torque (ST-501A/B), Linen Cake Height Laser (LT-601A/B), and Heat Exchanger Clean Effluent Temperature (TT-701A/B).
4. 10-State Cyber-Physical Discrete State-Space Model (Ts = 100 ms):
   - 10 states: [1] Pre-Wash Temp T_pre [deg C], [2] Main Wash Core Temp T_main [deg C], [3] Bleach Temp T_blc [deg C], [4] Rinse Conductivity C_rns [mS/cm], [5] Main Wash Active Alkali C_alk [g/L], [6] Heat Exchanger Preheat Temp T_rec [deg C], [7] Hydraulic Press Pressure P_prs [bar], [8] Extracted Linen Cake Moisture M_cake [%], [9] Drum Drive Motor Torque Load Tau_drum [N*m], [10] Press Recovery Buffer Level L_rec [%].
   - 6 control inputs: Main Wash Steam Valve Cmd [%], Bleach Direct Steam Valve Cmd [%], Freshwater Makeup Valve Cmd [%], Counter-Flow Recirculation Pump VFD [%], Hydraulic Press Proportional Pressure [bar], Chemical Dosing Pulse Rate [%].
   - Complete discrete system matrices A (10x10), B (10x6), C (8x10), D (8x6), and Luenberger observer innovation gain matrix L (10x8).
5. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) over prediction and control horizons.
   - Optimizes steam and freshwater valve commands while penalizing energy/water consumption and enforcing slew-rate limits.
6. Deterministic 14-Stage Production Finite State Machine (FSM):
   - [0] Standby Readiness, [1] Cold Pre-Fill & Network Charge, [2] Counter-Current Recirculation Prime & Lint Screen Purge, [3] Bath Temperature Steaming Ramp, [4] Chemical Dosing Pulse Synchronization, [5] Main Detergent Soak & Saponification (85°C), [6] Oxygen Bleach Activation (70°C), [7] High-Rate Counter-Flow Rinse, [8] Acid Neutralizer Souring Rinse (pH 5.5-6.5), [9] Archimedian Screw Linen Transfer Indexing, [10] Hydraulic Press Basket Load, [11] Multi-Stage Dewatering (up to 50 bar), [12] Cake Shuttle Conveyor Egress & Moisture Audit, [13] Automated Lint Filter Backwash & Energy Recovery Reclamation.
7. ISA-18.2 Process Alarms & 32-Bit Bit-Packed Registers:
   - High-High, High, Low, Low-Low alarm thresholds with clearance deadband hysteresis.
   - Bit-packed DWORDs: dwSystemStatusWord, dwAlarmWordProcess, dwAlarmWordSensors.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Textile_ContinuousTunnelWasher_WaterEnergyRecovery` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full 14-stage FSM execution, and ISA-18.2 alarm matrix."""

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
