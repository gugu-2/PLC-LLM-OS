import os
import json
import uuid
import math

def build_dataset():
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Plastics & Polymer Processing Automation (Tier 1 Global High-Demand Industrial Automation)
- System: 7-Layer High-Barrier Blown Film Extrusion Complex (EVOH / Polyamide / PE barrier film for food & medical packaging): 7 Grooved-Feed Extruders with Multi-Component Gravimetric Loss-in-Weight Loss Batch Dosing, Internal Bubble Cooling (IBC) Ultrasonic Closed-Loop Diameter & Frost-Line Height Regulation (High-frequency ultrasonic transducers detecting bubble wall deflection, modulating inverter supply and exhaust air blowers with vacuum lock), 360-Degree Oscillating Die Head & Reversing Haul-Off Tower (Continuous distribution of gauge variations), Automatic Air Ring Segmented Multi-Zone Heating Cartridges (In-line non-contact capacitive thickness profile scanner with real-time profile thickness control algorithm < ±2.0% gauge variance across 2.5m layflat width), and Dual Turret Surface/Center Gap Rewinder with Automatic Flying Knife Cross-Cut Splice.
- Function Block Name: `FB_Plastics_BlownFilm_7Layer_IBC_AirRing`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing bubble diameter, frost-line axial height, bubble internal pressure, average film thickness, thickness spatial standard deviation, air ring cooling air velocity, haul-off nip roll speed, and melt pressure at 7-layer feedblock.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing film gauge thickness error ($Q$), air ring segmented thermal cartridge control adjustments ($R$), and bubble diameter oscillation ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on IBC ultrasonic bubble diameter sensors, melt pressure transducers, and capacitive thickness profile sensors.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Extruder Barrel & Die Zone Pre-Heating (PID thermal soak), Resin Gravimetric Feeder Purge, Multi-Extruder Synchronous Melt Pumping, Die Lip Manual Bubble Inflation, IBC Ultrasonic Automatic Lock-In, Haul-Off Tower Collapsing Frame Speed Synchronization, Capacitive Thickness Gauge Rotary Scanning, Automatic Air Ring Segmented Profile Control, Edge Trim Slitter Engage, Dual Turret Rewind Core Loading, Flying Knife Auto-Splice Roll Transfer, and Bubble Collapse E-Stop Depressurization.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_Plastics_BlownFilm_7Layer_IBC_AirRing`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

    print("Generating FB_Plastics_BlownFilm_7Layer_IBC_AirRing...")

if __name__ == "__main__":
    build_dataset()
