import json
import uuid
import os
import subprocess
import sys
from generate_furnace import generate_iec_st

def main():
    agent_id = uuid.uuid4().hex[:8]
    json_filename = f"data/swarm_raw/agent_{agent_id}.json"
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Petrochemicals, Olefins & Ethylene Steam Cracking (Tier 1 Priority Sector): 150,000 tpy Gas/Liquid Ethylene Pyrolysis Furnace & TLE Quenching.**
- 8-Pass radiant coil outlet temperature (COT ~845 °C) balancing with low-NOx hearth burner firing
- Hydrocarbon feed (ethane/naphtha) to dilution steam mass ratio dynamic cross-limiting cascade
- Transfer Line Exchanger (TLE) ultra-fast primary oil/water quench to freeze secondary reactions (< 40 ms residence)
- Radiant tube metal temperature (TMT < 1,100 °C) laser pyrometry & internal coke layer thickness thermal resistance observer

**Function Block Name**: `FB_Petrochem_Ethylene_PyrolysisFurnace_TLE`

**Engineering Context & Operational Architecture**:
1. 8-Pass Radiant Coil Cracking & Temperature Distribution:
   - 8 independent radiant coils with individual feed trim valves and 2oo3 TMR thermocouple rakes at each coil outlet.
   - Target average Coil Outlet Temperature (COT) ~845 °C with pass-to-pass deviation constrained to < 2 °C.
   - High-temperature cracking kinetics: endothermic conversion of ethane/naphtha to ethylene, propylene, and byproducts.
2. Hydrocarbon Feed to Dilution Steam Dynamic Cross-Limiting Ratio Cascade:
   - Dynamic lead-lag cross-limiting ensuring dilution steam leads on feed increase and lags on feed decrease.
   - Nominal steam-to-hydrocarbon ratio 0.35 kg steam / kg HC to lower partial pressure and inhibit carbon deposition.
3. Transfer Line Exchanger (TLE) Primary & Secondary Quenching:
   - Ultra-fast quenching of cracked process gas from 845 °C down to ~400 °C within < 40 ms residence time to freeze secondary olefin degradation reactions.
   - Saturated high-pressure steam generation (110 bar) into plant steam drum, with online fouling factor surveillance and emergency quench oil injection.
4. Radiant Tube Skin Pyrometry & Sundaram-Froment Coking Observer:
   - Laser pyrometry peak Tube Metal Temperature (TMT) tracking with metallurgical safety alarm at 1,065 °C and emergency trip at 1,085 °C.
   - Online thermal resistance observer estimating internal pyrolytic coke layer thickness and remaining operating hours to decoking shutdown.
5. First-Principles State-Space Modeling & Receding-Horizon MPC:
   - Discrete state-space matrices (A, B, C, D) discretized at Ts = 20 ms with 8 states, 6 inputs, and 8 outputs.
   - Kalman filter observer innovation and state correction.
   - Receding-horizon multi-objective quadratic cost functional (Q, R, S, P) solved via Projected Gradient Descent (PGD) with physical box saturation and slew rate limiting.
6. Deterministic 14-Stage Production Finite State Machine:
   - Operational states spanning safe standby, N2 purge, pilot ignition, refractory ramp, steam circulation, feed cut-in, pass balancing, normal cracking MPC, high-severity cracking, coking surveillance, decoking air/steam burn, hot idle slump, emergency AFT fast fuel shutoff, and furnace cooldown.
7. ISA-18.2 Multi-Tier Alarm Management:
   - 16 distinct process channels with HH, H, L, LL, Rate of Change, and deadband hysteresis.
   - Bit-packed 32-bit status and alarm words (dwAlarmWord1, dwAlarmWord2, dwStatusWord1, dwStatusWord2).

Provide the complete, un-truncated, mathematically rigorous IEC 61131-3 Structured Text implementation inside a single ```iec-st code block."""

    st_code = generate_iec_st()
    assistant_content = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(json_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully wrote dataset to {json_filename}")
    print(f"Character count of assistant content: {len(assistant_content)}")
    
    # Run validate_iec.py
    cmd = [sys.executable, "validate_iec.py", json_filename]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validator Output:\n", res.stdout)
    if res.stderr:
        print("Validator Stderr:\n", res.stderr)
        
    if res.returncode != 0:
        print("VALIDATION FAILED!")
        sys.exit(1)
    else:
        print("VALIDATION SUCCESSFUL!")
        print(f"File verified: {json_filename}")
        return json_filename, len(assistant_content), agent_id

if __name__ == "__main__":
    main()
