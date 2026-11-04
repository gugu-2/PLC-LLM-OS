# -*- coding: utf-8 -*-
"""
Module: build_and_save_final.py
Builds, verifies, and saves the final JSON dataset record into data/swarm_raw/agent_<uuid>.json.
"""

import os
import sys
import json
import uuid
import re

sys.path.append(os.path.abspath("brain_scratch/web_offset_builder"))
from assemble_and_check import assemble, check_parity

USER_PROMPT = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Commercial Printing & High-Speed Web Offset Packaging
- System: Commercial 16-Page Web Offset Printing Press (15.0 m/s web speed, 50,000 cph): 4-Color (CMYK) Blanket-to-Blanket Print Towers with Electronic Line Shaft (ELS) Virtual Master Synchronous Phase Locking, On-Line CCD Color Register Camera Closed-Loop Lateral & Circumferential Alignment (\\Delta x, \\Delta y < 0.02 mm), Continuous Brush Dampening Solution Hydrophilic Emulsion Balance (alcohol-free surfactant regulation), High-Velocity Hot Air (HVHA) Dryer Flue Gas Multi-Zone Temperature Decoupling (280 °C with Lower Explosive Limit / LEL solvent vapor concentration safety observer), 4-Roll Chill Stand Web Condensation & Thermal Shock Conditioning, and Turret Unwind Continuous Flying Splicer Sequence.
- Function Block Name: `FB_Printing_WebOffset_HighSpeed_ColorRegistration_Drying`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID / Automation tags: `ST_VIRTUAL_MASTER_ELS_SPEED_101A/B/C`, `ZT_WEB_INLET_TENSION_DANCER_102A/B/C`, `WT_INFEED_TENSION_LOADCELL_103A/B/C`, `OPT_REGISTER_CYAN_DEV_201A/B/C`, `OPT_REGISTER_MAGENTA_DEV_202A/B/C`, `OPT_REGISTER_YELLOW_DEV_203A/B/C`, `OPT_REGISTER_BLACK_DEV_204A/B/C`, `AIT_DAMPENING_CONDUCTIVITY_301A/B/C`, `TT_DAMPENING_CHILL_TEMP_302A/B/C`, `TT_DRYER_ZONE1_TEMP_401A/B/C` through `TT_DRYER_ZONE4_TEMP_404A/B/C`, `AIT_DRYER_SOLVENT_LEL_405A/B/C`, `TT_CHILL_ROLL_SURFACE_TEMP_501A/B/C`, `ZT_CHILL_WEB_TENSION_502A/B/C`, `ST_SPLICER_NEW_ROLL_RPM_601A/B/C`, `ZT_SPLICER_PASTER_KNIFE_POS_602A/B/C`, `OPT_WEB_BREAK_ULTRASONIC_701A/B/C`.
2. 2oo3 Triple Modular Redundancy (TMR):
   - Full triplicated voting across web tension load cells, CCD register deviations, dryer zone temperatures, LEL solvent analyzers, and chill roll temperatures with pairwise delta checks, debounce timers, bumpless degradation, and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - Web viscoelastic strain propagation & tension decoupling: Kelvin-Voigt dynamic paper web modulus ($E(\\dot{\\epsilon}, T, M)$) under thermal moisture loss in the 280 °C dryer to prevent web snapping or wrinkling.
   - 4-Color registration decoupling observer: dynamic interaction model separating cylinder circumferential lead angle from lateral motor screw adjustments.
   - Ink-water emulsion non-linear boundary layer model: evaluates fountain solution evaporation rate and ink tackiness curve to prevent scumming or emulsification breakdown.
   - Solvent vapor Lower Explosive Limit (LEL) observer: calculates mineral oil solvent evaporation rate from drying inks to modulate exhaust recirculation dampers and hold LEL strictly $< 25\\%$.
4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 State-Space formulation ($x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k$) running at $T_s = 2$ ms.
   - Synchronizes print unit servo phase trim, infeed metering nip VFD, dryer burner fuel valve, and chill stand speed to achieve sub-0.02 mm color registration at 15.0 m/s web velocity.
5. ISA-18.2 Alarm Ladder:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC).
   - Fast web break trip (< 15 ms via optical/ultrasonic detectors with pneumatic blanket wash retract and web catcher clamp firing), dryer high-solvent LEL purge abort, and chill roll condensation trip.
6. Multi-Stage Operational FSM:
   - 12-state Finite State Machine: `PRESS_STANDBY_INCHING`, `INK_WATER_PRE_EMULSIFY`, `WEB_THREADING_LOW_SPEED`, `ELS_VIRTUAL_LINE_SHAFT_LOCK`, `DRYER_AND_CHILL_PREHEAT_RUN`, `SPEED_RAMP_TO_50K_CPH`, `AUTO_REGISTER_CLOSED_LOOP_ACTIVE`, `CONTINUOUS_FLYING_SPLICE_EXEC`, `INK_DENSITY_MICRO_REGULATION`, `CONTROLLED_DECEL_AND_WASH`, `WEB_SEVER_AND_CLAMP_CLEARED`, `EMERGENCY_ESTOP_BLANKET_LIFT`.
7. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Output Structured Text MUST be 50,000 to 85,000+ characters of pristine, industrial Structured Text."""

def main():
    st_raw = assemble()
    check_parity(st_raw)
    
    # Verify mandatory headers and endings
    assert st_raw.startswith("FUNCTION_BLOCK FB_Printing_WebOffset_HighSpeed_ColorRegistration_Drying"), "FB name mismatch!"
    assert st_raw.strip().endswith("END_FUNCTION_BLOCK"), "FB end mismatch!"
    
    assistant_content = f"```iec-st\n{st_raw}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": USER_PROMPT},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    unique_id = uuid.uuid4().hex[:8]
    filename = os.path.abspath(f"data/swarm_raw/agent_{unique_id}.json")
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"File successfully written to: {filename}")
    
    # Verify saved file
    with open(filename, "r", encoding="utf-8") as f:
        reloaded = json.load(f)
        
    loaded_st = reloaded["messages"][1]["content"]
    print("Reload verification:")
    print(f"  Saved JSON File Size : {os.path.getsize(filename):,} bytes")
    print(f"  Assistant ST Length  : {len(loaded_st):,} characters")
    print(f"  Total Lines          : {len(loaded_st.splitlines()):,}")
    print(f"  Agent ID             : agent_{unique_id}")

if __name__ == "__main__":
    main()
