import json
import uuid
import os
import subprocess
import build_asphalt_plant

prompt_text = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Road Construction & Asphalt Batch Production
- System: High-Capacity Continuous Asphalt Batch Mixing Plant (320 tonnes/hour): 6-Bin Cold Aggregate Feeders with Variable Speed Dosing Belts, Counterflow Rotary Aggregate Drying Drum with Modulating Heavy Fuel Oil / Natural Gas Burner (160 deg C to 190 deg C aggregate exit temp, exhaust baghouse differential pressure pulse-jet cleaning and LEL monitoring), Hot Aggregate Bucket Elevator & Multi-Deck Vibrating Screen (6 particle size classifications into insulated hot storage bins), High-Precision Gravimetric Batch Hopper Scales (Load cell triad voting with inflight material compensation for aggregates, reclaimed filler, and mineral dust), Bitumen Storage Tank Heating & Pressurized Metered Spray Bar Injection (Viscosity-temperature compensation at 150 deg C to 170 deg C), and Twin-Shaft Pugmill Mixer with active torque motor overload protection and heated discharge skip hoist.
- Function Block Name: `FB_Asphalt_BatchPlant_AggregateDrying_BitumenInjection`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) capturing rotary drum shell temperature, exit gas temperature, aggregate moisture evaporation rate, hot elevator motor load, baghouse pressure drop, bitumen tank jacket temperature, pugmill mixing torque, and skip hoist hoist velocity.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing aggregate exit temperature error (Q), burner fuel valve modulation (R), and bitumen spray injection mass flow accuracy (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on rotary dryer thermocouple pyrometers, pugmill load cell triads, and bitumen Coriolis mass flow meters.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering Plant Pre-Purge/Ignition, Cold Aggregate Proportioning Feed, Rotary Drum Drying & Burner Modulation, Hot Screening & Bin Storage, Aggregates Weigh Hopper Dosing, Filler/Mineral Dust Addition, Bitumen High-Pressure Metered Injection, Twin-Shaft Wet Mixing Cycle, Pugmill Discharge Gate Operation, Skip Hoist Transit to Storage Silo, Batch Recipe Changeover, and Controlled Burner Post-Cooling Purge.
3. 100% Strict Syntax & Delimiter Parity:
   - Every IF must have END_IF;
   - Every CASE must have END_CASE;
   - Every FOR must have END_FOR;
   - First line: FUNCTION_BLOCK FB_Asphalt_BatchPlant_AggregateDrying_BitumenInjection, Last line: END_FUNCTION_BLOCK
   - Triple backticks with iec-st: ```iec-st ... ```
4. Validation & Delivery:
   - Save your dataset to data/swarm_raw/agent_<uuid>.json with complete user/assistant message structure.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

st_code = build_asphalt_plant.generate_iec_st()
assistant_content = f"```iec-st\n{st_code}```"

record = {
    "messages": [
        {"role": "user", "content": prompt_text},
        {"role": "assistant", "content": assistant_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and saved to {filename}")
print(f"Assistant content character count: {len(assistant_content)}")

# Validate with validate_iec.py
res = subprocess.run(["python", "validate_iec.py", filename], capture_output=True, text=True)
print("Validation Output:\n", res.stdout)
if res.stderr:
    print("Validation Error:\n", res.stderr)
print(f"Validation return code: {res.returncode}")
