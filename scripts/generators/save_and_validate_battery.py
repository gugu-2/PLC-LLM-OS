# Save and validate EV battery CTP laser dispense dataset
import os
import json
import uuid
import generate_ev_battery_cell
import validate_iec

def main():
    st_code = generate_ev_battery_cell.generate_code()
    
    prompt = "Generate an ultra-dense, mathematically rigorous IEC 61131-3 Structured Text FUNCTION_BLOCK for an Automotive EV Battery Cell-to-Pack (CTP) structural adhesive dispensing and 1070nm fiber laser busbar wobble welding cell."
    code = f"```iec-st\n{st_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }
    
    os.makedirs("data/swarm_raw", exist_ok=True)
    filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    print(f"Saved to {filename}")
    
    # Run full json validation
    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED:", errs)
        sys.exit(1)
    else:
        print("PERFECT VALIDATION: JSON and IEC 61131-3 AST checks passed!")
        print(f"File size: {os.path.getsize(filename)} bytes")

if __name__ == "__main__":
    main()
