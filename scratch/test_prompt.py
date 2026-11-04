# Python generator script for FB_Bakery_ContinuousTunnelOven_MultiZone_Humidity
# Lumina Swarm V7 Max-Persona Protocol
import json
import uuid
import os
import sys

def build_tunnel_oven_dataset():
    # 1. User Prompt
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Food Processing / Commercial Industrial Bakery - 6-Zone Continuous Commercial Bakery Tunnel Oven (L = 60 m, throughput 5,000 kg/h baked dough): Independent Zone Upper and Lower Modulating Burner Air-to-Fuel Ratio Control (180 deg C to 260 deg C zone gradient), Zone 1 Steam Deposition Chamber with Saturated Steam Pulse Injection, Dynamic Exhaust Humidity Damper Regulation (High-Temperature Zirconia Moisture Sensor feedback, relative humidity 40% to 75%), Variable Speed Wire-Mesh Conveyor Belt Drive with Active Pneumatic Belt Tracking & Edge Tension Centering, Zone Thermal Radiation & Convection Heat Transfer Observer, and Flame Failure NFPA 86 Combustion Safety Interlocks (< 1.0 s slam-shut).**

CRITICAL RULES:
1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).
2. STRUCTURE:
   a. First line: FUNCTION_BLOCK FB_Bakery_ContinuousTunnelOven_MultiZone_Humidity
   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [deg C], [mbar], [m/min], [kg/h], [bar], [%], [Nm], [kW])
   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)
   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)
   e. Multi-stage CASE machine with END_CASE;
   f. Last line: END_FUNCTION_BLOCK
3. LENGTH: Assistant content MUST be >= 3500 characters total (target 75,000 to 125,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.
4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE.
5. SAVE using this exact Python:
   import json, uuid
   prompt = \"\"\"<copy this exact user prompt here>\"\"\"
   code = \"\"\"```iec-st
FUNCTION_BLOCK FB_Bakery_ContinuousTunnelOven_MultiZone_Humidity
//...
END_FUNCTION_BLOCK
```\"\"\"
   record = {"messages": [{"role": "user", "content": prompt}, {"role": "assistant", "content": code}]}
   with open(f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json", "w", encoding="utf-8") as f:
       json.dump(record, f, ensure_ascii=False)
6. REPLY with: EVOLUTION COMPLETE: Food Processing / Commercial Industrial Bakery"""

    # We will construct the ST code section by section in pure Structured Text.
    # Let's ensure everything is complete, exhaustive, without any shortcuts.
    return user_prompt

if __name__ == "__main__":
    p = build_tunnel_oven_dataset()
    print(f"Prompt length: {len(p)}")
