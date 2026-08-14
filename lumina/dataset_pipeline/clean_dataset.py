import os
import json
import re
import hashlib

def is_valid_plc_code(content):
    lower_content = content.lower()
    
    # Flags that highly suggest it's NOT PLC code
    invalid_keywords = ['def _mk_pb2', 'bazel', 'import os', 'import sys', 'public class', 'namespace', '<?xml', '<html', '<p>', '<code>', '<br>']
    for kw in invalid_keywords:
        if kw in lower_content:
            return False
            
    # Calculate Logic Density (how many logic operators exist relative to length)
    # Good PLC code has assignments, logic, math, structural blocks.
    logic_matches = len(re.findall(r'(?i)\b(if|then|else|elsif|case|for|while|repeat|until|end_if|end_case|end_for|end_while|end_repeat|:=|=>|\+|-|\*|/|and|or|not|xor)\b', content))
    
    # If the file is reasonably large but has zero logic (e.g. just a 10,000 line list of variable declarations), drop it.
    if len(content) > 500 and logic_matches < 3:
        return False
        
    # Advanced Regex heuristic: looking for structural PLC logic
    has_struct = bool(re.search(r'(?i)\b(program|function|function_block|data_block)\b.*?\b(end_program|end_function|end_function_block|end_data_block)\b', content, re.DOTALL))
    has_logic = logic_matches > 0
    has_var = bool(re.search(r'(?i)\bvar(_input|_output|_in_out|_temp)?\b.*?\bend_var\b', content, re.DOTALL))
    
    has_assign = ":=" in content
    
    if has_struct or has_logic or has_var or has_assign:
        return True
        
    return False

def clean_dataset(input_file="data/train.jsonl", output_file="data/train_clean.jsonl"):
    if not os.path.exists(input_file):
        print(f"{input_file} not found.")
        return
        
    print(f"Cleaning {input_file}...")
    removed_count = 0
    kept_count = 0
    duplicate_count = 0
    
    seen_hashes = set()
    
    with open(input_file, 'r', encoding='utf-8') as infile, open(output_file, 'w', encoding='utf-8') as outfile:
        for line in infile:
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                removed_count += 1
                continue
                
            # Find assistant response
            content = ""
            for msg in record.get("messages", []):
                if msg["role"] == "assistant":
                    content = msg["content"]
                    break
                    
            # Deduplication Check
            content_hash = hashlib.md5(content.strip().encode('utf-8')).hexdigest()
            if content_hash in seen_hashes:
                duplicate_count += 1
                continue
                
            if is_valid_plc_code(content):
                seen_hashes.add(content_hash)
                outfile.write(line)
                kept_count += 1
            else:
                removed_count += 1
                
    print(f"Clean complete.")
    print(f"Kept records: {kept_count}")
    print(f"Removed for low-quality/noise: {removed_count}")
    print(f"Removed exact duplicates: {duplicate_count}")

if __name__ == "__main__":
    clean_dataset()
