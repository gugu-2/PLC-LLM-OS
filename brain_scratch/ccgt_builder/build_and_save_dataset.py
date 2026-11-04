# brain_scratch/ccgt_builder/build_and_save_dataset.py
import os
import sys
import json

from header_and_io import get_header_and_io
from var_declarations import get_var_declarations
from phases_1_to_3 import get_phases_1_to_3
from phase_4_thermo import get_phase_4_thermo
from phases_5_and_6 import get_phases_5_and_6

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..")))
from validate_iec import validate_json_file

AGENT_UUID = "3179478f"
OUTPUT_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "data", "swarm_raw", f"agent_{AGENT_UUID}.json"))

user_prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Power Generation & Turbomachinery Automation (Tier 1 Global High-Demand Industrial Automation)
- System: 450 MW Combined Cycle Gas Turbine (CCGT) & Triple-Pressure Heat Recovery Steam Generator (HRSG) Steam Turbine Bypass Complex: High-Pressure (130 bar, 565°C) & Intermediate-Pressure (35 bar, 565°C) Steam Turbine Fast-Acting Electro-Hydraulic Bypass Valves (< 120 ms full-stroke opening for full load rejection grid decoupling without boiler trip), Water-to-Steam Desuperheating Spray Water Pressure Cascade (Thermal shock protection maintaining steam temperature within ±3°C of saturation limits), Gas Turbine Variable Inlet Guide Vane (VIGV) Airflow Optimization & DLN (Dry Low NOx) Fuel Gas Wobbe Index Splitter, Drum Boiler Shrink-and-Swell Dynamic Three-Element Level Control (Triple steam flow, feedwater flow, and drum differential pressure transmitters), and Selective Catalytic Reduction (SCR) Ammonia Injection Grid NOx Emission Trim.
- Function Block Name: `FB_PowerGen_CCGT_HRSG_SteamTurbineBypass`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing HP steam drum pressure, HP drum water level with non-linear shrink/swell bubble dynamics, steam temperature at HP bypass outlet, spray desuperheater water mass flow, turbine chest metal temperature, gas turbine exhaust temperature (TAT), SCR bed NOx reduction efficiency, and generator MW grid load.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing HP steam pressure excursions ($Q$), hydraulic bypass valve slew rate ($R$), and steam-to-metal thermal stress differential ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on HP steam pressure transmitters, boiler drum level dp cells, and steam temperature RTDs.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Plant Pre-Start Hydraulic Permissive Check, GT Cranking & Purge Sequence, HRSG Cold Start Warming Ramp, Low-Pressure Steam Production & Condenser Sparging, Intermediate Steam Pressure Hold, High-Pressure Steam Drum Pressure Build, Steam Turbine Chest Metal Pre-Warming, Fast Grid Synchronization & Bypass Closure Modulation, Base Load Combined Cycle Power Generation, Generator Load Rejection Full Bypass Fast-Trip Dump, Controlled Turbine Steam Cooldown, and Post-Trip Hydraulic Lockout.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_PowerGen_CCGT_HRSG_SteamTurbineBypass`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

header = get_header_and_io()
var_decl = get_var_declarations()
p1_3 = get_phases_1_to_3()
p4 = get_phase_4_thermo()
p5_6 = get_phases_5_and_6()

inner_st = f"{header}\n{var_decl}\n{p1_3}\n{p4}\n{p5_6}"
assistant_content = f"```iec-st\n{inner_st}\n```"

record = {
    "id": f"agent_{AGENT_UUID}",
    "messages": [
        {"role": "user", "content": user_prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

os.makedirs(os.path.dirname(OUTPUT_FILE), exist_ok=True)
with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset saved to: {OUTPUT_FILE}")
print(f"Assistant content character count: {len(assistant_content)}")
print(f"Inner ST character count: {len(inner_st)}")
print(f"File size on disk: {os.path.getsize(OUTPUT_FILE)} bytes")

print("\n--- Running validate_json_file ---")
errors = validate_json_file(OUTPUT_FILE)
if errors:
    print("VALIDATION FAILED with errors:")
    for e in errors:
        print(" -", e)
    sys.exit(1)
else:
    print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
    sys.exit(0)
