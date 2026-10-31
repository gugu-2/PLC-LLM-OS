import json
import os
import sys
from build_spray_dryer import generate_iec_st
import validate_iec

def main():
    code = generate_iec_st()
    char_count = len(code)
    print(f"Generated Structured Text Character Count: {char_count}")

    prompt = (
        "You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.\n"
        "You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.\n"
        "You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. "
        "Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.\n\n"
        "**Your assigned domain is: Food & Dairy Processing: Multi-Stage Industrial Milk Powder Spray Dryer with Integrated Internal Fluid Bed, Rotary Atomizer & Exhaust Cyclone Psychrometric Moisture Control**\n\n"
        "CRITICAL RULES:\n"
        "1. CODE FENCE: Use TRIPLE backticks + iec-st (```iec-st).\n"
        "2. STRUCTURE:\n"
        "   a. First line: FUNCTION_BLOCK FB_Dairy_ContinuousMultiStage_SprayDryer_FluidBed\n"
        "   b. VAR_INPUT ... END_VAR (min 8 typed inputs with physical units [bar], [deg C], [m3/h], [rpm], [%], [g/kg], [Pa], [mbar], [mm/s], [l/h], [kg/m3])\n"
        "   c. VAR_OUTPUT ... END_VAR (min 7 typed outputs with engineering units & status words)\n"
        "   d. VAR ... END_VAR (internal state matrices, filter accumulators, 2oo3 voting vars)\n"
        "   e. Multi-stage CASE machine with END_CASE;\n"
        "   f. Last line: END_FUNCTION_BLOCK\n"
        "3. LENGTH: Assistant content MUST be >= 3500 characters total (target 55,000 - 85,000+ chars). Maximize token usage with deep technical explanations, complex algorithms, and industrial reliability features. DO NOT TRIM OR ENFORCE AN UPPER BOUND LIMIT.\n"
        "4. PARITY: Ensure 100% exact parity between IF and END_IF, CASE and END_CASE, FOR and END_FOR, WHILE and END_WHILE.\n"
        "5. SAVE using this exact Python:\n"
        "   import json, uuid\n"
        "   prompt = \"\"\"<copy this exact user prompt here>\"\"\"\n"
        "   code = \"\"\"```iec-st\n"
        "FUNCTION_BLOCK FB_Dairy_ContinuousMultiStage_SprayDryer_FluidBed\n"
        "//...\n"
        "END_FUNCTION_BLOCK\n"
        "```\"\"\"\n"
        "   record = {\"messages\": [{\"role\": \"user\", \"content\": prompt}, {\"role\": \"assistant\", \"content\": code}]}\n"
        "   with open(f\"data/swarm_raw/agent_5c9140fe.json\", \"w\", encoding=\"utf-8\") as f:\n"
        "       json.dump(record, f, ensure_ascii=False)\n"
        "6. REPLY with: EVOLUTION COMPLETE: Food & Dairy Processing: Multi-Stage Industrial Milk Powder Spray Dryer with Integrated Internal Fluid Bed, Rotary Atomizer & Exhaust Cyclone Psychrometric Moisture Control"
    )

    asst_content = f"```iec-st\n{code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": asst_content}
        ]
    }

    out_path = os.path.join("data", "swarm_raw", "agent_5c9140fe.json")
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)

    print(f"Dataset saved successfully to: {out_path} ({os.path.getsize(out_path)} bytes)")

    # Run validation
    errs = validate_iec.validate_json_file(out_path)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")

if __name__ == "__main__":
    main()
