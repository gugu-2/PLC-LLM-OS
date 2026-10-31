# -*- coding: utf-8 -*-
import json
import os
import generate_brewery
import validate_iec

prompt = """MISSION BRIEFING: CONTINUOUS SWARM FLYWHEEL WAVE
Target Commercial Sector: Industrial Breweries Brewhouse Lauter Tuns & Fermentation Cellars (Rank #71)
System: FB_IndustrialBrewery_LauterTun_FermentationCellar
Destination File: data/swarm_raw/agent_4a67d42b.json

DIRECTIVES:
1. Generate an exhaustive, production-grade IEC 61131-3 Structured Text dataset (target 45,000 - 85,000+ characters).
2. Mathematical Rigor:
   - Discrete State-Space Matrices (A, B, C, D) modeling grain bed differential pressure, mash filtration resistance, and exothermic yeast fermentation kinetics (Arrhenius temperature dependence).
   - MPC quadratic cost formulation for automated lauter tun knife rake height modulation, vorlauf turbidity clearing recirculation, and multi-zone glycol jacket temperature pacing.
   - 2oo3 TMR voting logic for lauter tun false bottom differential pressure transmitters and fermentation cellar vessel core temperature probes.
   - Full CIP/SIP automated sanitization interlocks, sparging water flow pacing, and multi-step infusion mashing profile FSM.
   - ISA-18.2 multi-tiered alarm matrix (HH, H, L, LL, stuck mash differential pressure trip, glycol valve failure escalation).
3. Parity & Validation:
   - Must pass `python validate_iec.py data/swarm_raw/agent_4a67d42b.json` with 100% exact AST parity.
   - Save output in valid JSON schema (`{"messages": [{"role": "user", ...}, {"role": "assistant", ...}]}`).
4. When finished and validated, report completion back immediately. Proceed now!"""

code_body = generate_brewery.build_iec_code()
assistant_content = f"```iec-st\n{code_body}\n\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

target_file = "data/swarm_raw/agent_4a67d42b.json"
os.makedirs(os.path.dirname(target_file), exist_ok=True)

with open(target_file, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Successfully saved to {target_file}")
print(f"Assistant content character count: {len(assistant_content)}")

errs = validate_iec.validate_json_file(target_file)
if errs:
    print("VALIDATION ERRORS:")
    for e in errs:
        print(" -", e)
    sys.exit(1)
else:
    print("VALIDATION PASSED PERFECTLY!")
