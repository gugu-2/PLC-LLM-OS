import json
import os
import re

def verify_dataset(input_file="data/train_clean.jsonl"):
    if not os.path.exists(input_file):
        print(f"File {input_file} not found.")
        return
        
    total_records = 0
    html_violations = 0
    short_violations = 0
    bazel_violations = 0
    
    print(f"Verifying {input_file}...")
    
    html_pattern = re.compile(r'<p>|<code>|<br\s*/?>', re.IGNORECASE)
    
    with open(input_file, 'r', encoding='utf-8') as f:
        for line in f:
            total_records += 1
            record = json.loads(line)
            
            content = ""
            for msg in record.get("messages", []):
                if msg["role"] == "assistant":
                    content = msg["content"]
                    break
                    
            if html_pattern.search(content):
                html_violations += 1
                
            if len(content.strip()) < 20:
                short_violations += 1
                
            if "def _mk_pb2" in content or "bazel" in content.lower():
                bazel_violations += 1
                
    print(f"Verification complete for {total_records} records.")
    print(f"HTML tags found in {html_violations} records.")
    print(f"Too short responses found in {short_violations} records.")
    print(f"Bazel/Protobuf artifacts found in {bazel_violations} records.")
    
    if html_violations == 0 and short_violations == 0 and bazel_violations == 0:
        print("\nSUCCESS: Dataset passed all quality checks!")
    else:
        print("\nWARNING: Dataset has quality violations.")

if __name__ == "__main__":
    verify_dataset()
