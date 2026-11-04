# Python script to generate complete FB_Cable_ContinuousVulcanization_TripleExtrusion_Sag
import json
import uuid
import re
import sys
import os

def create_dataset():
    uid = uuid.uuid4().hex[:8]
    
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Electrical Cable & Wire Manufacturing Machinery
- System: High-Voltage (132 kV - 400 kV) Power Cable Continuous Vulcanization (CV) Line (Line Speed: 25.0 m/min): Triple-Head Extruder System (Conductor Screen, High-Purity Cross-Linked Polyethylene XLPE Insulation $\\varnothing 95 \\text{ mm}$, Insulation Screen with Melt Pressure Transducers up to 500 bar and Melt Temperature Zones), 150-Meter Nitrogen-Pressurized Catenary Vulcanization Heating & Telescopic Tube (10.0 bar $N_2$ overpressure, $380^\\circ\\text{C}$ to $420^\\circ\\text{C}$ zone radiant electric heaters), Continuous Non-Contact X-Ray Sag & Catenary Position Sensor ($\\Delta y_{sag} \\le \\pm 2.0\\text{ mm}$ centering avoidance of tube wall contact), High-Pressure Recirculating Water Quench Cooling Leg with Hydrostatic Boundary Seal, Dual-Wheel Caterpillar Capstan Line Speed / Tension Synchronizer ($120\\text{ kN}$ pulling force), and In-Line 8-Axis Ultrasonic Wall Thickness & Eccentricity Scanner.
- Function Block Name: `FB_Cable_ContinuousVulcanization_TripleExtrusion_Sag`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing extruder melt pressure, melt temperature, catenary sag position, heating zone temperatures, nitrogen pressure, water quench level, and capstan tension.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing catenary sag deviation ($Q$), nitrogen pressure variations ($R$), and line tension oscillations ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on extruder melt pressure transducers, catenary sag laser/X-ray sensors, nitrogen tube pressure transmitters, and zone heating thermocouples.
   - ISA-18.2 multi-tiered alarm hierarchy (Critical Tube Contact Hazard HH, Overpressure HH, Warning H/L, Diagnostic, Priority Escalation).
   - 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering tube nitrogen purge, heating zone preheat, conductor stringing tension, triple-head melt prime, line speed ramp-up, catenary sag auto-centering, continuous steady-state curing, spool changeover, purge-out, controlled tube depressurization, cool-down, and emergency E-stop line clamp.
3. Strict Syntax & Parity Rules:
   - TRIPLE backticks with `iec-st`.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`. Zero unmatched delimiters.
   - Zero summaries, zero placeholders (`// ... rest of code`).
4. Save directly as a standard JSON dataset to `data/swarm_raw/agent_<uuid>.json` containing `id`, `messages` (user prompt, assistant response with fenced iec-st code), and `metadata`. Validate with `python validate_iec.py` and report final character count."""

    # We will assemble code piece by piece
    with open("scratch/st_sections.py", "w", encoding="utf-8") as f:
        f.write("# Helper module containing Structured Text sections\n")
    
    print("Beginning generation...")

if __name__ == "__main__":
    create_dataset()
