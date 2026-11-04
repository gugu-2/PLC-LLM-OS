# save_and_verify_wte.py
import os
import json
import uuid
import re

from wte_generator.part1_header_io import get_part1_header_io
from wte_generator.part2_var import get_part2_var
from wte_generator.part3_init_tmr import get_part3_init_tmr
from wte_generator.part4_physics_statespace import get_part4_physics_statespace
from wte_generator.part5_fsm_alarms import get_part5_fsm_alarms

def main():
    agent_uuid = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_uuid}.json"
    output_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
    output_path = os.path.join(output_dir, output_filename)

    p1 = get_part1_header_io()
    p2 = get_part2_var()
    p3 = get_part3_init_tmr()
    p4 = get_part4_physics_statespace()
    p5 = get_part5_fsm_alarms()

    full_st_code = f"{p1}\n{p2}\n{p3}\n{p4}\n{p5}"
    
    # Parity verification
    clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', full_st_code)
    if_count = len(re.findall(r'\bIF\b', clean_code))
    endif_count = len(re.findall(r'\bEND_IF\b', clean_code))
    case_count = len(re.findall(r'\bCASE\b', clean_code))
    endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code))
    for_count = len(re.findall(r'\bFOR\b', clean_code))
    endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code))
    fb_count = len(re.findall(r'\bFUNCTION_BLOCK\b', clean_code))
    endfb_count = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code))

    assert if_count == endif_count, f"IF parity mismatch: {if_count} != {endif_count}"
    assert case_count == endcase_count, f"CASE parity mismatch: {case_count} != {endcase_count}"
    assert for_count == endfor_count, f"FOR parity mismatch: {for_count} != {endfor_count}"
    assert fb_count == endfb_count == 1, f"FB parity mismatch: {fb_count} != {endfb_count}"

    char_count = len(full_st_code)
    lines_count = len(full_st_code.splitlines())
    assert char_count > 50000, f"Code length too short: {char_count} <= 50000"

    formatted_output = f"```iec-st\n{full_st_code}\n```"

    instruction_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Municipal Waste-to-Energy & Advanced Environmental Engineering**
**System: 1,500 Ton/Day Continuous Moving Grate Waste-to-Energy (WtE) Incinerator & Flue Gas Treatment Plant: 4-Zone Hydraulic Grate Stoker Stroke Speed & Primary/Secondary Combustion Air Staged Oxygen Decoupling (combustion chamber temperature 950.0 °C to 1,050.0 °C with >= 2.0 s residence time per EU Directive 2010/75/EU), SNCR/SCR Urea/Ammonia Injection & In-Situ Laser Spectrometry DeNOx Observer (NOx < 80 mg/Nm³, NH3 slip < 3 mg/Nm³), Semi-Dry Spray Absorber Slaked Lime Ca(OH)2 Slurry Atomizer Acid Gas (HCl, SO2) Neutralization, Activated Carbon Heavy Metal / Dioxin Adsorption Pacing, and Boiler Superheater Tube Metal Corrosion Acoustic Thickness Monitoring.**
**Function Block Name: FB_WasteToEnergy_MovingGrate_SCR_FlueGasCleaning**

NEXT-GEN QUALITY REQUIREMENTS:
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID tags: TT_COMBUSTION_CHAMBER_101A/B/C, TT_POST_COMBUSTION_2SEC_102A/B/C, ZT_GRATE_ZONE1_STROKE_201A/B/C, ZT_GRATE_ZONE4_STROKE_204A/B/C, FT_PRIMARY_AIR_FLOW_301A/B/C, FT_SECONDARY_AIR_FLOW_302A/B/C, AIT_FLUEGAS_NOX_INLET_401A/B/C, AIT_STACK_NOX_OUTLET_402A/B/C, AIT_STACK_NH3_SLIP_403A/B/C, FT_UREA_INJECTION_501A/B/C, AIT_FLUEGAS_HCL_601A/B/C, AIT_FLUEGAS_SO2_602A/B/C, FT_LIME_SLURRY_FEED_701A/B/C.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 50 ms cycle modeling: Heterogeneous solid bed waste drying, pyrolysis, gasification, and char burnout thermodynamics, Arrhenius gas-phase thermal NOx / fuel NOx formation kinetics, Selective Non-Catalytic Reduction (SNCR) temperature window kinetic selectivity (DeNOx vs. NH3 slip tradeoff between 850 °C and 1,050 °C), and spray dryer droplet evaporative mass transfer. Explicitly define and calculate matrices.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional (J = sum (x-r)^T Q (x-r) + u^T R u + Delta u^T S Delta u) optimizing 4-zone grate drive hydraulic speeds, primary/secondary forced draft fans, urea dosing pump stroke, and lime atomizer slurry feed to maintain steam generation stability while eliminating emissions exceedances.
3. 2oo3 Triple Modular Redundancy (TMR):
   - Post-combustion 2-second acoustic pyrometric temperature sensors (2oo3 voting with 15.0 °C discrepancy threshold).
   - Continuous Emission Monitoring System (CEMS) stack NOx/SO2 infrared analyzers (2oo3 voting with 3.0 mg/Nm³ discrepancy limit).
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with legal emission breach automated trip (< 1.0 s latching) and grate hydraulic jam fast reverse cycle.
5. Multi-Stage FSM:
   - 12-state state machine: SYSTEM_OFFLINE_COLD_INSPECTION, REFRACTORY_PREHEAT_AUX_BURNER, WASTE_FEED_CHUTE_PRIME, GRATE_IGNITION_BED_ESTABLISH, SECONDARY_AIR_O2_STABILIZATION, FULL_LOAD_AUTONOMOUS_INCINERATION, DENOX_AMMONIA_OPTIMIZATION, ACID_GAS_SCRUBBER_TRIM, SLAG_DISCHARGE_EXTRACTOR_SYNC, CONTROLLED_BURN_OUT_SHUTDOWN, EMERGENCY_FEED_CUT_SMOKE_STOP, SAFETY_INTERRUPT_ID_FAN_RUNAWAY.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero // ... rest of code, zero placeholders.
   - 100% exact parity: Every IF must have END_IF;, every CASE must have END_CASE;, every FOR must have END_FOR;.
   - TRIPLE backticks with iec-st. Code length MUST be 50,000 to 85,000+ characters of industrial Structured Text."""

    record = {
        "id": f"synthetic_v3_{agent_uuid}",
        "instruction": instruction_prompt,
        "input": "",
        "output": formatted_output,
        "messages": [
            {"role": "user", "content": instruction_prompt},
            {"role": "assistant", "content": formatted_output}
        ],
        "metadata": {
            "domain": "Environmental_WasteToEnergy_Incineration",
            "function_block": "FB_WasteToEnergy_MovingGrate_SCR_FlueGasCleaning",
            "version": "v3_cyberphysical_max",
            "lines": lines_count,
            "characters": char_count,
            "validated": True
        }
    }

    os.makedirs(output_dir, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"Successfully generated and written: {output_path}")
    print(f"File size on disk: {os.path.getsize(output_path):,} bytes")
    print(f"Structured Text Characters: {char_count:,}")
    print(f"Structured Text Lines: {lines_count:,}")

    # Re-read and verify parseability
    with open(output_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
    assert loaded["id"] == f"synthetic_v3_{agent_uuid}"
    assert len(loaded["output"]) > 50000
    assert loaded["metadata"]["validated"] is True
    print("Verification complete: 100% SUCCESS!")

if __name__ == "__main__":
    main()
