# -*- coding: utf-8 -*-
"""
Assembles the complete dataset for FB_Electronics_SMT_ReflowOven_14ZoneNitrogenVacuum
and saves to data/swarm_raw/agent_<uuid>.json
Validates using validate_iec.py.
"""

import os
import json
import uuid

import build_smt_14zone_reflow as b1
import build_smt_part2 as b2
import build_smt_part3 as b3
import build_smt_part4 as b4
import build_smt_part5 as b5
import validate_iec

def main():
    prompt = b1.generate_user_prompt()
    
    p1 = b1.build_code()
    p2 = b2.get_part2()
    p3 = b3.get_part3()
    p4 = b4.get_part4()
    p5 = b5.get_part5()
    
    full_st_code = f"```iec-st\n{p1}\n{p2}\n{p3}\n{p4}\n{p5}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": full_st_code}
        ]
    }
    
    # Save to data/swarm_raw/agent_feafa9fd.json
    agent_id = "feafa9fd"
    target_path = f"data/swarm_raw/agent_{agent_id}.json"
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    with open(target_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    
    print(f"Dataset successfully saved to: {target_path}")
    print(f"User prompt length: {len(prompt)} characters")
    print(f"Assistant response length: {len(full_st_code)} characters")
    
    # Run validation
    errs = validate_iec.validate_json_file(target_path)
    if errs:
        print("VALIDATION ERRORS FOUND:")
        for e in errs:
            print(" -", e)
        raise SystemExit(1)
    else:
        print("PERFECT VALIDATION: 0 ERRORS!")

if __name__ == "__main__":
    main()
