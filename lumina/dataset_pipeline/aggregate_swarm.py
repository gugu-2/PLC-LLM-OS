import os
import glob
from pathlib import Path

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data")))
SWARM_DIR = BASE_DIR / "swarm_outputs"
OUTPUT_FILE = BASE_DIR / "evol_instruct_dataset.jsonl"

def aggregate():
    jsonl_files = glob.glob(str(SWARM_DIR / "*.jsonl"))
    print(f"Found {len(jsonl_files)} files to aggregate.")
    
    total_appended = 0
    with open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:
        for file in jsonl_files:
            with open(file, "r", encoding="utf-8") as infile:
                for line in infile:
                    if line.strip():
                        outfile.write(line.strip() + "\n")
                        total_appended += 1
            os.remove(file)
                    
    print(f"Successfully aggregated {total_appended} ChatML JSON pairs into {OUTPUT_FILE.name} and cleaned up.")

if __name__ == "__main__":
    aggregate()
