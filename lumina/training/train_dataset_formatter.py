"""
Lumina Dataset Formatter & Ingestion Engine
===========================================
Prepares, cleans, tokenizes, and splits industrial PLC datasets into standard
ChatML / Alpaca instruction-tuning datasets ready for SFT & DPO training.
"""

import os
import json
import random
from typing import List, Dict, Any, Tuple


def format_instruction_record(user_prompt: str, assistant_code: str, system_prompt: str = None) -> Dict[str, Any]:
    """Formats an industrial prompt-response pair into ChatML schema."""
    if system_prompt is None:
        system_prompt = (
            "You are Lumina AI, an expert industrial automation and IEC 61131-3 controls engineer. "
            "Generate mathematically verifiable, deterministic Structured Text (ST), Siemens SCL, or Rockwell L5X code. "
            "Ensure all arrays are bounded, all memory addresses are typed, and safety invariants are strictly preserved."
        )
    return {
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_code}
        ]
    }


def prepare_training_split(
    raw_records: List[Dict[str, Any]],
    output_dir: str = "lumina/training/data",
    train_ratio: float = 0.9,
    seed: int = 42
) -> Tuple[str, str]:
    """Splits formatted dataset into train.jsonl and val.jsonl."""
    os.makedirs(output_dir, exist_ok=True)
    random.seed(seed)
    random.shuffle(raw_records)

    split_idx = int(len(raw_records) * train_ratio)
    train_data = raw_records[:split_idx]
    val_data = raw_records[split_idx:]

    train_path = os.path.join(output_dir, "train.jsonl")
    val_path = os.path.join(output_dir, "val.jsonl")

    with open(train_path, "w", encoding="utf-8") as f:
        for item in train_data:
            f.write(json.dumps(item) + "\n")

    with open(val_path, "w", encoding="utf-8") as f:
        for item in val_data:
            f.write(json.dumps(item) + "\n")

    print(f"[DATASET] Prepared {len(train_data)} training records -> {train_path}")
    print(f"[DATASET] Prepared {len(val_data)} validation records -> {val_path}")
    return train_path, val_path


if __name__ == "__main__":
    # Example generator test
    sample_records = [
        format_instruction_record(
            user_prompt="Write a Siemens SCL function block for rotary capper torque monitoring with debounce.",
            assistant_code="""FUNCTION_BLOCK FB_RotaryCapperTorque
VAR_INPUT
    bExecute : BOOL;
    rTorqueMeasured_Nm : REAL;
    rTorqueMaxLimit_Nm : REAL := 12.5;
END_VAR
VAR_OUTPUT
    bTorqueFault : BOOL;
    bCappingPermitted : BOOL;
END_VAR
VAR
    tDebounceTimer : TON;
END_VAR
BEGIN
    tDebounceTimer(IN := (rTorqueMeasured_Nm > rTorqueMaxLimit_Nm), PT := T#50MS);
    IF tDebounceTimer.Q THEN
        bTorqueFault := TRUE;
        bCappingPermitted := FALSE;
    ELSE
        bTorqueFault := FALSE;
        bCappingPermitted := bExecute;
    END_IF;
END_FUNCTION_BLOCK"""
        )
    ]
    prepare_training_split(sample_records)
