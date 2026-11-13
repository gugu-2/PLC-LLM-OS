# Package dataset to data/swarm_raw/agent_<uuid>.json
import os, sys, json, uuid
from assemble_dataset import assemble

def package():
    code_text = assemble()
    asst_content = f"```iec-st\n{code_text}\n```"
    
    prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Biopharmaceutical & Life Sciences (Continuous Tangential Flow Filtration - TFF / Cross-Flow Ultrafiltration & Diafiltration for Monoclonal Antibody Downstream Processing)
FUNCTION BLOCK NAME: FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 10 ms):
   - 8-State model covering membrane transmembrane pressure (TMP), concentration polarization gel layer hydrodynamic resistance (film theory model), wall shear rate, permeate flux decline kinetics, retentate protein concentration, diafiltration buffer volume exchange ratio, and cassette hydraulic resistance:
     States: x1=Transmembrane Pressure TMP [bar], x2=Permeate Volumetric Flux [L/m2/h LMH], x3=Retentate Monoclonal Antibody Concentration [g/L], x4=Membrane Gel Polarization Resistance Rg [m-1], x5=Retentate Channel Wall Shear Rate [s-1], x6=Diafiltration Buffer Volume Exchange Counter [DV], x7=Retentate Recirculation Temperature [degC], x8=Buffer Addition Sump Weight Deviation [g].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic TMP & Wall Shear Decoupling: feed pump servo speed dynamically controls wall shear rate while the retentate proportional pinch/diaphragm valve simultaneously modulates TMP without fouling or shearing delicate proteins.
   - Actuator constraints: Feed quaternary diaphragm pump VFD [0..3000 rpm], retentate automated control valve [0..100%], diafiltration buffer metering pump [0..100%], permeate automated control valve [0..100%], heat exchanger chiller glycol valve [0..100%], feed divert recovery valve [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Feed Line Sanitary Diaphragm Pressure Transmitters (PT_FEED_101A/B/C) [bar]
     * Retentate Line Sanitary Pressure Transmitters (PT_RET_201A/B/C) [bar]
     * Permeate Line Sanitary Pressure Transmitters (PT_PERM_301A/B/C) [bar]
     * Inline Optical UV-Vis 280 nm Protein Concentration Sensors (AT_UV_401A/B/C) [g/L]
     * Feed Coriolis Mass Flowmeters (FT_FEED_501A/B/C) [L/h]
   - Discrepancy accumulation timers (threshold 100 ms) and bumpless degradation.

4. Deterministic 14-Stage Bioprocessing State Machine (FSM):
   - CASE eState OF:
     0: SANITARY_STANDBY_AND_INTEGRITY_CHECK
     1: WFI_FLUSH_AND_INITIAL_NWP_BASE_WATER_TEST
     2: EQUILIBRATION_BUFFER_CONDITIONING_PRIME
     3: PROTEIN_BULK_FEED_INTRODUCTION_RAMP
     4: ULTRAFILTRATION_CONCENTRATION_PHASE_1
     5: AUTOMATED_CONSTANT_VOLUME_DIAFILTRATION (7 DV)
     6: ULTRAFILTRATION_FINAL_TARGET_CONCENTRATION
     7: PRODUCT_CHILLDOWN_AND_STABILIZATION (4 degC)
     8: RETENTATE_RECOVERY_DRAIN_AND_WFI_CHASE
     9: AIR_BLOWDOWN_FLUID_RECOVERY_CYCLE
     10: CAUSTIC_CIP_MEMBRANE_CLEANING_RECIRCULATION
     11: POST_CIP_NWP_MEMBRANE_RECOVERY_EVALUATION
     12: PRESERVATIVE_STORAGE_FLUSH (0.1M NaOH)
     13: EMERGENCY_OVERPRESSURE_RUPTURE_DISC_INTERLOCK
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Protein Shear Denaturation & 32-Bit Telemetry:
   - High TMP (>3.5 bar) fast feed pump trip (<10 ms).
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: `FUNCTION_BLOCK FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration`
- Last line: `END_FUNCTION_BLOCK`
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero `// ... rest of code`. Every line fully written."""

    record = {
        "instruction": prompt,
        "input": "",
        "output": asst_content,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }
    
    unique_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{unique_id}.json"
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully wrote dataset file: {filename}")
    print(f"Assistant content character count: {len(asst_content)}")
    return filename

if __name__ == "__main__":
    fname = package()
    print("Validating with validate_iec.py...")
    ret = os.system(f"python validate_iec.py {fname}")
    if ret == 0:
        print("VALIDATION SUCCESSFUL!")
    else:
        print("VALIDATION FAILED!")
        sys.exit(1)
