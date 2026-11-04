import json
import uuid
import os
import re
from build_pharma_dataset import build_full_st_code

prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Biopharmaceutical & Advanced Nanomedicine Manufacturing - Continuous mRNA-Lipid Nanoparticle (mRNA-LNP) Encapsulation Unit: Staggered Herringbone Microfluidic Impingement Mixer (flow velocity 0.5–3.0 m/s, Reynolds number 150–450, total flow rate ratio 3:1 aqueous to ethanol), In-Line Multi-Angle Dynamic Light Scattering (DLS) Particle Size & Polydispersity Index (PDI < 0.12) Monitoring, In-Line Tangential Flow Filtration (TFF) Ultrafiltration/Diafiltration for Ethanol Clearance (< 50 ppm), and Multi-Zone Peltier Cryogenic Quench Heat Exchanger (-20 °C to +4 °C)**

Task: Implement the production-grade Function Block `FB_Pharma_mRNA_LNP_MicrofluidicMixer_DLS` governing:
1. Standardized industrial P&ID tags: FT_AQUEOUS_MRNA_101A/B/C, FT_ETHANOL_LIPID_102A/B/C, PT_MICROFLUIDIC_INLET_201A/B/C, PT_TFF_FEED_301A/B/C, PT_TFF_RETENTATE_302A/B/C, PT_TFF_PERMEATE_303A/B/C, AIT_DLS_PARTICLE_DIAMETER_401A/B/C, AIT_DLS_PDI_402A/B/C, TT_CRYO_PELTIER_501A/B/C, AIT_RESIDUAL_ETHANOL_601A/B/C.
2. Discrete State-Space Matrices (A, B, C, D) 8x8 formulation at 5 ms cycle modeling Dean vortex microchannel convective mass transport, nanoprecipitation nucleation kinetics (Arrhenius supersaturation rate), TFF membrane concentration polarization gel layer dynamics, and Peltier thermoelectric heat pumping: x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k.
3. Receding-Horizon Model Predictive Control (MPC) quadratic cost functional optimizing aqueous/organic dual syringe servo flow ratio, TFF transmembrane pressure (TMP), and Peltier cooling current to maintain PDI < 0.10 and particle diameter 75 ± 3 nm.
4. 2oo3 Triple Modular Redundancy (TMR) voting logic on in-line laser DLS hydrodynamic diameter photon correlator (3.5 nm discrepancy limit) and TFF feed pressure transducer triplex (0.05 bar discrepancy limit).
5. ISA-18.2 multi-tiered alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis and anti-chatter filters.
6. 12-state FSM: SYSTEM_FLUSH_WFI, PRIME_MICRO_CHANNELS, TEMPERATURE_STABILIZATION, ORGANIC_AQUEOUS_SYNC_RAMP, STEADY_STATE_ENCAPSULATION, DLS_IN_LINE_QUALIFICATION, TFF_BUFFER_EXCHANGE_DIAFILTRATION, CRYO_PELTIER_QUENCH, OFF_SPEC_DIVERSION_HOLD, SYSTEM_SIP_CIP_CYCLE, CONTAINMENT_ISOLATION_ABORT, CONTROLLED_SHUTDOWN.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

raw_st_code = build_full_st_code()
code_with_fence = f"```iec-st\n{raw_st_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code_with_fence}
    ]
}

file_uuid = uuid.uuid4().hex[:8]
output_dir = "data/swarm_raw"
os.makedirs(output_dir, exist_ok=True)
filename = os.path.join(output_dir, f"agent_{file_uuid}.json")

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

file_size = os.path.getsize(filename)
code_chars = len(raw_st_code)
fence_chars = len(code_with_fence)

print(f"FILE_SAVED: {filename}")
print(f"FILE_SIZE_BYTES: {file_size}")
print(f"RAW_CODE_CHARS: {code_chars}")
print(f"FENCED_CHARS: {fence_chars}")
print(f"EST_TOKENS: {code_chars // 4}")
