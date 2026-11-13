import json
import uuid
import subprocess
import sys
from generator_full import generate_iec_block

user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Biopharmaceutical Continuous Processing - Commercial 25,000-L Mammalian Cell Monoclonal Antibody Bioreactor & ATF Perfusion Skid with Alternating Tangential Flow Hollow-Fiber Membrane Cell Retention, Dynamic TMP Backpulse Antifouling, 4-Gas Mass Flow Cascade Sparging (O2, N2, CO2, Air), Respirometric Off-Gas Mass Spectrometer (OUR, CER, RQ), and In-Line Laser Raman Spectroscopy (VCD > 90 million cells/mL, Glucose/Lactate Metabolite Control).**

Task: Implement the production-grade Function Block `FB_Biopharma_PerfusionBioreactor_ATF_OffGas` governing:
1. Discrete State-Space Matrices (A, B, C, D) modeling bulk broth temperature, dissolved oxygen percentage, broth pH, viable cell density (VCD), glucose substrate concentration, lactate metabolite accumulation, ATF membrane transmembrane pressure (TMP), and off-gas carbon dioxide evolution rate (CER): x_{k+1} = A*x_k + B*u_k.
2. Model Predictive Control (MPC) quadratic cost functional optimizing jacket thermal valve, sparging gases (O2, CO2, Air), alkali base addition, nutrient feed rate, ATF cycle frequency, and permeate harvest rate to maintain homeostatic cell viability at VCD > 90x10^6 cells/mL with controlled TMP < 0.45 bar.
3. 2oo3 TMR voting logic on optical dissolved oxygen sensors, pressurized glass gel pH probes, Pt100 RTD broth temperature elements, ATF retentate/permeate pressure transmitters, and off-gas mass spectrometer analyzers with discrepancy timers and bumpless degradation.
4. ISA-18.2 multi-tiered alarm matrix (Critical HH, Warning H, Low L, Low-Low LL, Rate-of-Change) with high-speed sterile containment isolation and automated membrane backpulse triggers.
5. 14-stage FSM (OFFLINE_STANDBY, CIP_CLEAN_IN_PLACE, SIP_THERMAL_STERILIZATION, POST_SIP_ASEPTIC_COOLDOWN, STERILE_MEDIA_BATCH_FILL, INOCULATION_SEED_TRANSFER, BATCH_EXPONENTIAL_GROWTH, FED_BATCH_TRANSITION, PERFUSION_CUT_IN_RAMP, STEADY_STATE_HIGH_DENSITY, MEMBRANE_BACKPULSE_ANTIFOULING, BLEED_CELL_DENSITY_STABILIZATION, FINAL_HARVEST_CONCENTRATION, BIOKILL_THERMAL_DEACTIVATION, EMERGENCY_VENT_SAFE_STOP).

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

def package_and_validate():
    raw_st = generate_iec_block()
    assistant_content = f"```iec-st\n{raw_st}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    agent_id = uuid.uuid4().hex[:8]
    filepath = f"data/swarm_raw/agent_{agent_id}.json"
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"Dataset successfully saved to: {filepath}")
    print(f"Total file size: {len(assistant_content)} characters in assistant block.")
    
    # Run validate_iec.py
    cmd = [sys.executable, "validate_iec.py", filepath]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validator Output:\n" + res.stdout)
    if res.stderr:
        print("Validator Stderr:\n" + res.stderr)
        
    if res.returncode != 0:
        print(f"Validation FAILED with return code {res.returncode}")
        sys.exit(1)
    else:
        print("SUCCESS! File validated with 0 errors.")
        return filepath, len(assistant_content), agent_id

if __name__ == "__main__":
    package_and_validate()
