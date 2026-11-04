# build_full_st.py
import json
import uuid
import re
import os
import sys

from st_declarations import get_declarations
from st_phase0_1 import get_phase0_1
from st_phase2_3 import get_phase2_3
from st_phase4_5_6_7 import get_phase4_5_6_7

def build_and_validate():
    # 1. Assemble Full Structured Text
    part1 = get_declarations()
    part2 = get_phase0_1()
    part3 = get_phase2_3()
    part4 = get_phase4_5_6_7()
    
    full_code = part1 + "\n" + part2 + "\n" + part3 + "\n" + part4
    
    # 2. Check basic character and line count
    char_count = len(full_code)
    line_count = len(full_code.splitlines())
    print(f"Total characters: {char_count}")
    print(f"Total lines: {line_count}")
    
    # 3. Delimiter Parity Checks (strip comments and strings first to avoid false counts)
    # Strip comments (* ... *)
    code_no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', full_code)
    
    # Check IF vs END_IF
    # Pattern for IF (not ELSIF, not END_IF)
    ifs = len(re.findall(r'\bIF\b', code_no_comments))
    end_ifs = len(re.findall(r'\bEND_IF\b', code_no_comments))
    elsifs = len(re.findall(r'\bELSIF\b', code_no_comments))
    print(f"IF: {ifs}, END_IF: {end_ifs}, ELSIF: {elsifs}")
    if ifs != end_ifs:
        print(f"ERROR: IF count ({ifs}) != END_IF count ({end_ifs})")
        sys.exit(1)
        
    # Check CASE vs END_CASE
    cases = len(re.findall(r'\bCASE\b', code_no_comments))
    end_cases = len(re.findall(r'\bEND_CASE\b', code_no_comments))
    print(f"CASE: {cases}, END_CASE: {end_cases}")
    if cases != end_cases:
        print(f"ERROR: CASE count ({cases}) != END_CASE count ({end_cases})")
        sys.exit(1)
        
    # Check FOR vs END_FOR
    fors = len(re.findall(r'\bFOR\b', code_no_comments))
    end_fors = len(re.findall(r'\bEND_FOR\b', code_no_comments))
    print(f"FOR: {fors}, END_FOR: {end_fors}")
    if fors != end_fors:
        print(f"ERROR: FOR count ({fors}) != END_FOR count ({end_fors})")
        sys.exit(1)
        
    # Check FUNCTION_BLOCK vs END_FUNCTION_BLOCK
    fb = len(re.findall(r'\bFUNCTION_BLOCK\b', code_no_comments))
    end_fb = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', code_no_comments))
    print(f"FUNCTION_BLOCK: {fb}, END_FUNCTION_BLOCK: {end_fb}")
    if fb != end_fb or fb != 1:
        print(f"ERROR: FUNCTION_BLOCK count ({fb}) != END_FUNCTION_BLOCK count ({end_fb})")
        sys.exit(1)
        
    # 4. Check prompt instruction
    instruction = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Green Hydrogen Infrastructure & Industrial Water Electrolysis
- System: 100 MW Multi-Stack Proton Exchange Membrane (PEM) Water Electrolysis Green Hydrogen Facility: 20 x 5 MW Stacks Dynamic Power Splitting & Renewable Wind/Solar Fast Fluctuation Tracking (0–100% ramp in < 5.0 s), Anode Deionized Water Circulating Loop & O2 Degasser Differential Pressure Regulation (30.0 bar ± 0.05 bar cell differential), Cathode H2-in-O2 Gas Permeation Cross-Over Safety Observer (LFL safety margin < 1.5% H2 in O2), 20-Stack Heat Exchanger Thermal Balancing (70.0 °C ± 0.5 °C), and TSA Deoxo/Dryer Dual-Bed Swing Regeneration Pacing.
- Function Block Name: `FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID tags: `IT_STACK_DC_CURRENT_101A/B/C`, `VT_STACK_DC_VOLTAGE_102A/B/C`, `PT_ANODE_O2_SEPARATOR_201A/B/C`, `PT_CATHODE_H2_SEPARATOR_202A/B/C`, `DP_MEMBRANE_DIFF_PRESS_203A/B/C`, `AIT_H2_IN_O2_CROSSOVER_301A/B/C`, `AIT_O2_IN_H2_CROSSOVER_302A/B/C`, `TT_STACK_COOLING_INLET_401A/B/C`, `TT_STACK_COOLING_OUTLET_402A/B/C`, `FT_DI_WATER_FEED_501A/B/C`, `AIT_DI_WATER_CONDUCTIVITY_502A/B/C`, `PT_TSA_DRYER_BED1_601A/B/C`.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 5 ms cycle modeling: Electrochemical Butler-Volmer activation overpotential, Nernst reversible thermodynamic cell voltage (E_rev(T, P)), Ohm's law membrane proton transport resistance (sigma_PEM = f(lambda, T)), Fick's law hydrogen/oxygen gas crossover diffusive permeation through Nafion membrane, and stack lumped thermal capacitance balance. Explicitly define and calculate matrices.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional (J = sum (x-r)^T Q (x-r) + u^T R u + Delta u^T S Delta u) optimizing individual stack thyristor rectifier currents, anode/cathode backpressure valves, and deionized water circulation pump VFDs to maximize system efficiency (eta_LHV > 68%) while strictly keeping H2-in-O2 < 1.5% across rapid solar/wind dropouts.
3. 2oo3 Triple Modular Redundancy (TMR):
   - Cell differential pressure transducers (2oo3 voting with 0.04 bar discrepancy threshold).
   - In-line thermal conductivity / catalytic gas crossover analyzers (2oo3 voting with 0.10% H2 discrepancy limit).
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with emergency stack DC breaker fast trip (< 10 ms) and nitrogen inert gas purge auto-blast.
5. Multi-Stage FSM:
   - 12-state state machine: `SYSTEM_OFFLINE_N2_PURGED`, `DI_WATER_FILL_CIRCULATION`, `MEMBRANE_HYDRATION_SOAK`, `CATHODE_ANODE_PRE_PRESSURIZE`, `STACK_MINIMUM_LOAD_START_5PCT`, `RENEWABLE_POWER_FOLLOWING_MPC`, `DEOXO_PURIFICATION_PULSE`, `TSA_BED_DESORPTION_REGEN`, `CROSSOVER_SAFETY_DERATE_HOLD`, `CONTROLLED_DE_ENERGIZATION`, `N2_FLUSH_STANDBY_PARK`, `EMERGENCY_ESTOP_VENT`.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Code length MUST be 50,000 to 85,000+ characters of industrial Structured Text."""

    # 5. Build record
    raw_uid = uuid.uuid4().hex[:8]
    json_id = f"synthetic_v3_{raw_uid}"
    
    record = {
        "id": json_id,
        "instruction": instruction,
        "input": "",
        "output": full_code,
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": full_code}
        ],
        "metadata": {
            "domain": "Green Hydrogen Infrastructure & Industrial Water Electrolysis",
            "function_block": "FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance",
            "version": "v3_cyberphysical_max",
            "lines": line_count,
            "characters": char_count,
            "validated": True
        }
    }
    
    # 6. Save to data/swarm_raw/agent_<uuid>.json
    out_dir = r"c:\Users\majip\Downloads\LLM REASEARCH\data\swarm_raw"
    os.makedirs(out_dir, exist_ok=True)
    out_file = os.path.join(out_dir, f"agent_{raw_uid}.json")
    
    with open(out_file, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    print(f"SUCCESSFULLY SAVED TO: {out_file}")
    print(f"File size on disk: {os.path.getsize(out_file)} bytes")
    return out_file, char_count, line_count

if __name__ == "__main__":
    build_and_validate()
