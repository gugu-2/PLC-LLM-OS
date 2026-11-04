import os
import re
import json
import uuid
import sys

# Ensure current working directory is on sys.path
sys.path.append('.')
sys.path.append('Local_Ollama_Evol_Pipeline/scripts')
from linter import ST_Linter
import scratch.build_aerospace_dataset as b

prompt_text = """You are generating a SINGLE ultra-dense, mathematically rigorous IEC 61131-3 Structured Text dataset for the **Commercial Aerospace & Liquid Propulsion Ground Test Facilities** industry.

**Domain**: Commercial Aerospace & Liquid Propulsion Ground Test Facilities: 2.5 MN Cryogenic Liquid Oxygen / Liquid Methane (LOX/LCH4) Full-Flow Staged Combustion (FFSC) Rocket Engine Static Test Stand: Real-Time High-Frequency Acoustic Combustion Instability Observer (100 kHz piezoresistive transducer FFT for chugging, buzzing, screeching modes), Dual Turbopump Cavitation & Shaft Speed Balancing (LOX pump 35,000 RPM, LCH4 pump 42,000 RPM), Regenerative Nozzle Cooling Channel Heat Flux Dynamic Matching (35 MW/m² peak throat heat flux), Dual-Axis Electro-Mechanical Actuator (EMA) Thrust Vector Control (TVC) Frequency Decoupling, and Emergency Nitrogen/Helium Purge Dump Interlock (< 25 ms shutdown latency).

**Function Block Name**: `FB_Aerospace_RocketEngine_LOX_Methane_TestStand`

**Engineering Context & Operational Architecture**:
- 2.5 MN cryogenic Full-Flow Staged Combustion (FFSC) LOX/LCH4 rocket engine static test stand operating at chamber pressure Pc = 250 bar.
- Dual turbopump architecture: Oxidizer-Rich Preburner driving LOX pump at 35,000 RPM, Fuel-Rich Preburner driving CH4 pump at 42,000 RPM.
- High-frequency piezoresistive dynamic pressure transducers sampled at 100 kHz with real-time discrete resonator bank isolating chugging (50-250 Hz), buzzing (400-1200 Hz), and 1T transverse screeching (2500-6500 Hz).
- Fast acoustic abort trip (< 15 ms latency) on peak dynamic pressure > 15 bar.
- Regenerative nozzle cooling using supercritical methane through milled CuCrZr copper alloy channels (peak throat heat flux 35 MW/m²), governed by the Gnielinski correlation.
- Dual-axis EMA thrust vector control with active gyroscopic decoupling compensating for turbopump rotor angular momentum.
- Multi-tier emergency shutdown with 300 bar GHe blast purge and fast depressurization dump in < 25 ms.

**Transmitter & Tag Nomenclature**:
- Standard industrial P&ID tags: `PT_CHAMBER_STATIC_101A/B/C`, `PT_CHAMBER_HIGHFREQ_102A/B/C`, `PT_LOX_DOME_201A/B/C`, `PT_CH4_INJECTOR_202A/B/C`, `ST_TURBOPUMP_LOX_301A/B/C`, `ST_TURBOPUMP_CH4_302A/B/C`, `TT_NOZZLE_THROAT_METAL_401A/B/C`, `FT_LOX_MAIN_CORIOLIS_501A/B/C`, `FT_CH4_MAIN_CORIOLIS_502A/B/C`, `ZT_TVC_ACTUATOR_PITCH_601A/B/C`, `ZT_TVC_ACTUATOR_YAW_602A/B/C`, `WT_THRUST_LOADCELL_701A/B/C`.

**Required Mathematical Depth & State-Space Formulations**:
1. Discrete State-Space 8x8 Matrix Dynamics (x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k) at 100 us cycle time.
2. Sonic throat choking thermodynamics (c* = Pc * At / m_dot, O/F = 3.60).
3. Gnielinski supercritical methane heat transfer correlation (Nu = 0.0214*(Re^0.8 - 100)*Pr^0.4*(Tb/Tw)^0.55).
4. Dual turbopump NPSH cavitation margins with Antoine vapor pressure modeling.
5. Receding-Horizon Model Predictive Control (MPC) with 3-iteration Projected Gradient Descent.
6. 2oo3 Triple Modular Redundancy (TMR) sensor voting across 12 transducer triplets with discrepancy timers and bumpless degradation.
7. ISA-18.2 5-tier process alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with bit packing into 4 diagnostic words.
8. 12-Stage Operational Finite State Machine (FSM).
"""

raw_code = b.generate_aerospace_block()

# Verify code
is_valid, linter_msg = ST_Linter.verify_code(raw_code)
print(f"Linter verification: {is_valid} ({linter_msg})")
if not is_valid:
    raise ValueError(f"Linter failed: {linter_msg}")

wrapped_output = f"```iec-st\n{raw_code}\n```"

agent_uuid = uuid.uuid4().hex[:8]
record_id = f"synthetic_v3_{agent_uuid}"
filename = f"data/swarm_raw/agent_{agent_uuid}.json"

num_lines = len(raw_code.splitlines())
num_chars = len(raw_code)

payload = {
    "id": record_id,
    "instruction": prompt_text.strip(),
    "input": "",
    "output": wrapped_output,
    "messages": [
        {"role": "user", "content": prompt_text.strip()},
        {"role": "assistant", "content": wrapped_output}
    ],
    "metadata": {
        "domain": "Commercial Aerospace & Liquid Propulsion Ground Test Facilities",
        "function_block": "FB_Aerospace_RocketEngine_LOX_Methane_TestStand",
        "version": "v3_cyberphysical_max",
        "lines": num_lines,
        "characters": num_chars,
        "validated": True
    }
}

os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(payload, f, ensure_ascii=False, indent=2)

print(f"SUCCESS: Saved {filename}")
print(f"Total Lines: {num_lines}, Total Code Characters: {num_chars}")
