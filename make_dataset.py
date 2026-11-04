# Part 1 of Water Reclamation Generator: Setup and VAR blocks
import os
import sys
import json
import uuid
import re

PROMPT = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Advanced Water Treatment & Water Reclamation (Tier 1 Global High-Demand Industrial Automation)
- System: Municipal & Industrial Advanced Wastewater Water Reclamation Complex (100 MLD): Membrane Aerated Biofilm Reactor (MABR) with Oxygen Permeable Hollow-Fiber Gas Transfer (Simultaneous nitrification/denitrification with dynamic biofilm thickness observer), Submerged Ultrafiltration (UF) Membrane Trains (Transmembrane pressure TMP cascade, cyclic air scour bubbling, and automated hydraulic backpulse with sodium hypochlorite / citric acid CIP injection), High-Pressure Dual-Stage Reverse Osmosis (RO) Trains with Isobaric Energy Recovery Devices (ERD Pressure Exchangers > 97% recovery efficiency, feed brine pressure 65 bar), and Real-Time Feed SDI (Silt Density Index), Permeate Conductivity, and UV Disinfection Transmittance Validation.
- Function Block Name: `FB_Water_MABR_Ultrafiltration_RO_Reclamation`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model (x[k+1] = A*x[k] + B*u[k], y[k] = C*x[k] + D*u[k]) capturing MABR bulk liquid dissolved oxygen, ammonium nitrogen concentration, nitrate/nitrite concentration, UF transmembrane pressure (TMP), membrane foulant resistance cake layer thickness, RO feed pressure, permeate electrical conductivity, and ERD rotor rotational speed.
   - Model Predictive Control (MPC) quadratic cost approximation penalizing effluent total nitrogen error (Q), high-pressure RO feed pump VFD slew rate (R), and UF membrane fouling acceleration rate (P).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on ion-selective ammonium/nitrate electrodes, UF differential pressure transmitters, and high-pressure RO feed pressure cells.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (CASE State OF ... END_CASE) covering Plant Wetting & Line Purge, MABR Low-Flow Inoculation, Continuous MABR Nitrification/Denitrification Chemostat, UF Filtration Forward Flow, UF Air-Scour & Fast Water Flush, UF Chemically Enhanced Backwash (CEB), RO High-Pressure Soft Ramp & ERD Synchronization, Steady-State RO Desalination & Permeate Blending, Membrane Clean-in-Place (CIP) Recirculation, RO Permeate Flush & Preservation Hold, Effluent Water Quality Violation Diversion, and Emergency High-Pressure Rupture Lockout.
3. 100% Strict Syntax & Delimiter Parity:
   - Every IF must have END_IF;
   - Every CASE must have END_CASE;
   - Every FOR must have END_FOR;
   - First line: FUNCTION_BLOCK FB_Water_MABR_Ultrafiltration_RO_Reclamation, Last line: END_FUNCTION_BLOCK
   - Triple backticks with iec-st: ```iec-st ... ```
4. Validation & Delivery:
   - Save your dataset to data/swarm_raw/agent_<uuid>.json with complete user/assistant message structure.
   - Run python validate_iec.py data/swarm_raw/agent_<uuid>.json to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

print("PROMPT prepared, length:", len(PROMPT))
