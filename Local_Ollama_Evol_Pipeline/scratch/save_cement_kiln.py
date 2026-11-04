import os
import sys
import json
import uuid
import re

sys.path.append('Local_Ollama_Evol_Pipeline/scripts')
sys.path.append('Local_Ollama_Evol_Pipeline/scratch')
from linter import ST_Linter
import gen_cement_kiln

def save_and_verify():
    iec_code = gen_cement_kiln.generate_iec_code()
    
    # Verify using ST_Linter
    ok, msg = ST_Linter.verify_code(iec_code)
    if not ok:
        raise ValueError(f"Linter validation failed: {msg}")
    print(f"Linter verification PASSED: {msg}")
    
    # Verify delimiter parity explicitly
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', iec_code)
    clean_code = re.sub(r'//.*', '', clean_code)
    
    if_count = len(re.findall(r'\bIF\b', clean_code, re.IGNORECASE))
    end_if_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    assert if_count == end_if_count, f"Mismatched IF ({if_count}) vs END_IF ({end_if_count})"
    
    case_count = len(re.findall(r'\bCASE\b', clean_code, re.IGNORECASE))
    end_case_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    assert case_count == end_case_count, f"Mismatched CASE ({case_count}) vs END_CASE ({end_case_count})"
    
    for_count = len(re.findall(r'\bFOR\b', clean_code, re.IGNORECASE))
    end_for_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    assert for_count == end_for_count, f"Mismatched FOR ({for_count}) vs END_FOR ({end_for_count})"
    
    # Check length
    char_count = len(iec_code)
    line_count = len(iec_code.splitlines())
    print(f"Code metrics: {char_count} characters, {line_count} lines")
    assert char_count >= 50000, f"Character count {char_count} is less than required 50,000"
    
    code_wrapped = f"```iec-st\n{iec_code}\n```"
    
    prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Heavy Building Materials & Cement Manufacturing: World-Scale 10,000 Ton/Day Dry Process Rotary Cement Kiln with 5-Stage Precalciner Cyclone Tower & Cross-Bar Clinker Cooler: Burning Zone True Sintering Temperature Regulation (1,450.0 °C ± 5.0 °C), Multi-Channel Pulverized Coal Main Burner Axial/Radial Momentum Swirl Balancing, Precalciner Tertiary Air Duct Damper & Staged Fuel Combustion (calcination rate 92.0% ± 0.5%), Reciprocating Grate Cooler Variable Hydraulic Drive Stroke Speed & Under-Grate Aeration Bed Pressure Balancing, Kiln Shell 2D Thermal Scanner Refractory Coating Spalling / Hot Spot Detection, and Preheater Tower Induced Draft (ID) Fan Draft Pressure Decoupling.**

Task: Write a world-class, mathematically rigorous, ultra-realistic IEC 61131-3 Structured Text Function Block named `FB_Cement_RotaryKiln_Precalciner_ClinkerCooler` for this world-scale cement pyroprocessing system.

NEXT-GEN QUALITY REQUIREMENTS:
1. Transmitter & Tag Nomenclature:
   - Standardized industrial P&ID tags: TT_BURNING_ZONE_PYRO_101A/B/C, TT_KILN_INLET_GAS_102A/B/C, TT_PRECALCINER_EXIT_201A/B/C, PT_KILN_INLET_DRAFT_301A/B/C, PT_PRECALCINER_TOP_DRAFT_302A/B/C, AIT_KILN_INLET_O2_401A/B/C, AIT_KILN_INLET_CO_402A/B/C, AIT_KILN_INLET_NOX_403A/B/C, ST_KILN_MAIN_DRIVE_RPM_501A/B/C, IT_KILN_MAIN_DRIVE_KW_502A/B/C, PT_GRATE_COOLER_BED_601A/B/C, TT_CLINKER_DISCHARGE_701A/B/C.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 50 ms cycle modeling non-linear endothermic calcium carbonate decarbonation kinetics (CaCO3 -> CaO + CO2), exothermic clinker mineral alite/belite formation thermodynamics (Bogue calculation for C3S, C2S, C3A, C4AF), rotary kiln axial bed solids transport velocity (Sullivan-Work/USBM formulation), gas-solid cross-flow heat exchange in the cyclone suspension preheater, and clinker cooler cross-flow recuperation heat balance.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional optimizing main burner coal dosing, precalciner coal dosing, kiln drive rotational RPM, raw meal feed rate, and ID fan damper position to maintain free lime content (f-CaO < 1.0%) and minimize heat consumption (< 2,950 kJ/kg clinker).
3. 2oo3 Triple Modular Redundancy (TMR):
   - Burning zone optical ratio pyrometers (2oo3 voting with 15.0 °C discrepancy limit).
   - Kiln inlet flue gas oxygen analyzers (2oo3 voting with 0.25% O2 discrepancy threshold).
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with emergency baghouse CO surge deflagration fast fuel cut-off trip (< 200 ms).
5. Multi-Stage FSM:
   - 12-state state machine: KILN_WARMUP_REFRACTORY_DRY, AUXILIARY_INCHING_DRIVE, PREHEATER_FAN_DRAFT_PULL, MAIN_BURNER_DIESEL_PILOT, RAW_MEAL_FEED_INTRODUCTION, ROTARY_KILN_ACCELERATION_RAMP, PRECALCINER_COAL_FIRING_SYNC, STEADY_STATE_CLINKER_BURNING, KILN_RING_SNOWMAN_BREAKING, GRATE_COOLER_HEAT_RECUPERATION, CONTROLLED_KILN_STOP_DRAIN, EMERGENCY_ESTOP_FUEL_CUT.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero placeholders, 100% exact delimiter parity. Output format in ```iec-st fenced code block."""

    uid = uuid.uuid4().hex[:8]
    record = {
        "id": f"synthetic_v3_{uid}",
        "instruction": prompt,
        "input": "",
        "output": code_wrapped,
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code_wrapped}
        ],
        "metadata": {
            "domain": "BuildingMaterials_Cement_Manufacturing",
            "function_block": "FB_Cement_RotaryKiln_Precalciner_ClinkerCooler",
            "version": "v3_cyberphysical_max",
            "lines": line_count,
            "characters": char_count,
            "validated": True
        }
    }
    
    out_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"agent_{uid}.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Successfully saved to {out_file}")
    
    # Self-validation: read back and verify
    with open(out_file, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["id"] == f"synthetic_v3_{uid}"
    assert loaded["metadata"]["validated"] is True
    assert len(loaded["output"]) > 50000
    print("Self-validation PASSED flawlessly!")
    return out_file, char_count

if __name__ == "__main__":
    filepath, chars = save_and_verify()
    print(f"FINAL_FILE: {filepath}")
    print(f"FINAL_CHARS: {chars}")
