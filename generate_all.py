# generate_all.py
import json
import os
import subprocess

import module_decl
import module_phases_0_3
import module_phases_4_5
import module_phases_6_7

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Bio-Pharmaceuticals & Life Sciences: 500-Liter Single-Use Perfusion Bioreactor (SUB) with Tangential Flow Filtration (TFF) Cell Retention & 4-Gas Mass Flow Blending**

Task: Implement the production-grade Function Block `FB_Biotech_SingleUse_PerfusionBioreactor_500L` governing:
1. 500L Single-Use Bioreactor vessel with jacketed thermal bag warming and bottom magnetic levitation impeller (agitation speed 30–250 RPM, power input per volume P/V calculation).
2. 4-Gas mass flow controller (MFC) manifold (O2, N2, CO2, Air) with micro-sparger and drilled-hole macro-sparger dynamic gas blending for dissolved oxygen (DO setpoint 40–50%) and pCO2 stripping.
3. Dual optical/electrochemical pH control via pulsed CO2 gas sparging (acidifying) and variable-rate peristaltic sodium bicarbonate (base) addition with anti-windup deadbands.
4. Tangential Flow Filtration (TFF) / Alternating Tangential Flow (ATF) hollow-fiber membrane cell retention system: dynamic transmembrane pressure (TMP) calculation, backflush pacing, and permeate flux regulation to maintain viable cell density (VCD > 80 x 10^6 cells/mL) with continuous bleed pump chemostat pacing.
5. Off-gas paramagnetic O2 and NDIR CO2 analysis for real-time Oxygen Uptake Rate (OUR), Carbon Dioxide Evolution Rate (CER), and Respiratory Quotient (RQ) metabolic tracking.
6. Discrete State-Space Model (12x12 state matrix A, 12x8 B, C, D) incorporating Monod/Michaelis-Menten cell growth kinetics, substrate glucose/glutamine consumption, lactate/ammonia accumulation, and oxygen mass transfer coefficient (kLa).
7. Receding-horizon MPC for multivariable control of DO, pH, temperature, and perfusion bleed/harvest balance.
8. 2oo3 Triple Modular Redundancy (TMR) voting across optical DO probes, pH probes, load cell vessel weight transmitters, and permeate pressure sensors.
9. 12-Stage Operational FSM (Single-Use Bag Leak Test, Media Pre-Fill & Heat Conditioning, Probe Calibration & Inoculation, Batch Exponential Growth Phase, Perfusion Feed Ramp-Up, Steady-State Continuous Perfusion Chemostat, Filter Automated Backflush & Permeate Cycling, High-Density Cell Bleed Adjustment, Product Harvest Collection, Harvest End-of-Run Terminate, In-line CIP Waste Neutralization, System Standby).
10. ISA-18.2 multi-tiered alarm matrix (DO critical LL, pH excursion, TMP membrane fouling HH, vessel overpressure, foaming level sensor trip with automated antifoam injection) with bit-packed telemetry DWORDs.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

parts = [
    module_decl.get_header(),
    module_decl.get_var_input(),
    module_decl.get_var_output(),
    module_decl.get_var(),
    module_phases_0_3.get_phase0_safety(),
    module_phases_0_3.get_phase1_tmr(),
    module_phases_0_3.get_phase2_offgas(),
    module_phases_0_3.get_phase3_hydrodynamics(),
    module_phases_4_5.get_phase4_statespace(),
    module_phases_4_5.get_phase5_mpc(),
    module_phases_6_7.get_phase6_fsm(),
    module_phases_6_7.get_phase7_alarms()
]

st_code = "\n".join(parts)
assistant_content = f"```iec-st\n{st_code}\n```"

print(f"Total assistant_content length: {len(assistant_content)} characters")

target_file = "data/swarm_raw/agent_a9410cb2.json"
record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

os.makedirs(os.path.dirname(target_file), exist_ok=True)
with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully written to {target_file}")
