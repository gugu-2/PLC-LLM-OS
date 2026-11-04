# -*- coding: utf-8 -*-
"""
Builder script for FB_Biopharma_PerfusionBioreactor_ATF_OffGas
Generates an ultra-dense, mathematically complete IEC 61131-3 Structured Text dataset.
"""

import json
import os
import re

UUID = "413be94a"
OUTPUT_FILE = f"data/swarm_raw/agent_{UUID}.json"

user_prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION (TIER 1 - CYCLE 2):
- Domain: Biotechnology & Biopharmaceutical Processing (Tier 1 Global High-Demand Industrial Automation)
- System: 20,000-Liter Commercial Mammalian Cell Culture Perfusion Bioreactor Complex: Alternating Tangential Flow (ATF) Hollow-Fiber Membrane Cell Retention System (Diaphragm pump cyclic vacuum/pressure oscillation with dynamic transmembrane pressure TMP control and automated antifouling backpulse), 4-Gas Mass Flow Controller Cascade Sparging (O2, N2, CO2, Air for dissolved oxygen dO2 regulation 30% to 60% air sat and pH 6.9 to 7.2 via CO2 acid trim and sodium bicarbonate base dosing), In-Line Laser Raman Spectroscopy / Capacitance Biomass Probe (Real-time Viable Cell Density VCD > 80 million cells/mL and glucose/glutamine concentration monitoring), Respirometric Off-Gas Mass Spectrometer (Continuous calculation of Oxygen Uptake Rate OUR, Carbon Dioxide Evolution Rate CER, and Respiratory Quotient RQ), and Precision Thermal Circulation Jacket (±0.05°C temperature stability at 37.0°C).
- Function Block Name: `FB_Biopharma_PerfusionBioreactor_ATF_OffGas`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Extreme Token Density & Mathematical Rigor (Target: 75,000 to 125,000+ characters).
2. Cyber-Physical Foundation:
   - Full 8-state Discrete State-Space Model ($x_{k+1} = A x_k + B u_k$, $y_k = C x_k + D u_k$) capturing broth temperature, dissolved oxygen concentration, liquid pH, viable cell density (VCD), glucose nutrient substrate concentration, toxic lactate accumulation, transmembrane pressure (TMP), and off-gas carbon dioxide evolution rate (CER).
   - Model Predictive Control (MPC) quadratic cost approximation penalizing viable cell viability drop ($Q$), nutrient feed pump slew rate ($R$), and sparger gas flow volatility ($P$).
   - 2oo3 Triple Modular Redundancy (TMR) voting with discrepancy timers on optical dissolved oxygen sensors, pressurized glass pH electrodes, and broth temperature Pt100 RTDs.
   - Comprehensive ISA-18.2 multi-tiered alarm hierarchy (HH, H, L, LL, Rate of Change) with hysteresis and 32-bit packed diagnostic alarm words.
   - Deterministic 12-Stage Finite State Machine (`CASE State OF ... END_CASE`) covering Vessel CIP/SIP Sterilization Hold, Sterile Media Fill & Calibration Equilibrations, Inoculation & Batch Seed Growth, Exponential Growth Phase Transition, Continuous ATF Perfusion Cut-In, Steady-State High-Density Chemostat Operation, Nutrient Feed Optimization (Monod/Michaelis-Menten kinetics), Antifoam Micro-Dosing Injection, Membrane Cleaning/Bleed Purge, Harvest Clarification Tangential Pumping, Bioreactor Post-Harvest Thermal Deactivation (65°C kill cycle), and Sterile Vessel Hold.
3. 100% Strict Syntax & Delimiter Parity:
   - Every `IF` must have `END_IF;`
   - Every `CASE` must have `END_CASE;`
   - Every `FOR` must have `END_FOR;`
   - First line: `FUNCTION_BLOCK FB_Biopharma_PerfusionBioreactor_ATF_OffGas`, Last line: `END_FUNCTION_BLOCK`
   - Triple backticks with `iec-st`: ` ```iec-st ` ... ` ``` `
4. Validation & Delivery:
   - Save your dataset to `data/swarm_raw/agent_<uuid>.json` with complete user/assistant message structure.
   - Run `python validate_iec.py data/swarm_raw/agent_<uuid>.json` to verify 100% delimiter parity and char count.
   - Reply with completion details once verified."""

print("Writing generator script...")
