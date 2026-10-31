# Python generator for FB_Pharma_Lyophilizer_FreezeDrying_Sublimation
# Target: data/swarm_raw/agent_5c4019ae.json

import json
import re
import os
import sys

# User prompt
prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Pharmaceuticals & Bioprocess: Large-Scale Industrial Production Lyophilizer (Freeze Dryer, 50 m2 Shelf Area) with Dual-Stage Sublimation, Pirani-Capacitance End-Point Metrology & Automated Hydraulic Vial Stoppering**

Task: Implement the production-grade Function Block `FB_Pharma_Lyophilizer_FreezeDrying_Sublimation` governing:
1. Discrete State-Space Matrices (A, B, C, D) 16x16 state matrix A, 16x8 matrix B, C, D incorporating ice sublimation heat of vaporization, shelf silicone oil convective heat transfer, ice condenser frosting layer thickness thermal resistance, and Pirani gas composition dynamics: x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost optimization governing shelf thermal fluid heating/cooling, refrigeration screw compressor slide valve, and sterile nitrogen micro-bleed dosing to maximize sublimation rate while strictly preventing product cake collapse (T_prod < T_collapse).
3. 2oo3 Triple Modular Redundancy (TMR) voting logic on shelf RTDs, vial thermocouple clusters, capacitance manometers (Baratron), Pirani gauges, condenser coil RTDs, and hydraulic load cells with bumpless degradation.
4. Dual-gauge endpoint determination metrology comparing thermal conductivity Pirani indication with absolute capacitance manometer readings (Delta_P < 0.005 mbar) combined with dynamic pressure rise test verification.
5. 12-Stage Operational Finite State Machine (CIP_SIP_VERIFICATION, AUTO_VIAL_LOADING, CONTROLLED_FREEZING_ANNEAL, CONTROLLED_ICE_NUCLEATION_PULSE, VACUUM_PUMPDOWN, PRIMARY_DRYING_SUBLIMATION, PIRANI_CM_ENDPOINT_DETECTION, SECONDARY_DRYING_DESORPTION, CHAMBER_BACKFILL_STERILE_N2, HYDRAULIC_SHELF_STOPPERING, AUTO_VIAL_UNLOADING, CONDENSER_ICE_DEFROST_CYCLE).
6. ISA-18.2 multi-tiered alarm matrix (Product collapse danger HH, vacuum loss HH, condenser high temp H/HH, compressor discharge head, hydraulic stoppering force shortfall) with bit-packed telemetry DWORDs.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

print("Building code parts...")
