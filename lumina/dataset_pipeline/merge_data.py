import os
import json
import glob

def merge_jsonl_files(input_dir="data", output_file="data/train.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    input_files = glob.glob(f"{input_dir}/*.jsonl")
    # Exclude output_file safely by resolving absolute paths
    abs_output = os.path.abspath(output_file)
    valid_inputs = [f for f in input_files if os.path.abspath(f) != abs_output]
    input_files = valid_inputs
        
    print(f"Found {len(input_files)} JSONL files to merge.")
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as outfile:
        for fpath in input_files:
            print(f"Merging {fpath}...")
            with open(fpath, 'r', encoding='utf-8') as infile:
                for line in infile:
                    # just basic validation
                    record = json.loads(line)
                    if "messages" in record:
                        outfile.write(json.dumps(record) + "\n")
                        total_records += 1
                        
    print(f"Merge complete! Final dataset '{output_file}' contains {total_records} records.")

if __name__ == "__main__":
    merge_jsonl_files()
