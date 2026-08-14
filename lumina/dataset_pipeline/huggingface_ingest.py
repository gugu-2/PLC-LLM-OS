import os
import json
import requests
import zipfile
import io
import glob

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

def process_plc_beAD(output_file="data/hf_plc_bead.jsonl"):
    print("Downloading PLC-BEAD dataset from GitHub...")
    repo_url = "https://github.com/AICPS/PLCBEAD_PLCEmbed/archive/refs/heads/main.zip"
    
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    # Download the zip file
    response = requests.get(repo_url)
    if response.status_code == 200:
        print("Downloaded zip successfully. Extracting...")
        with zipfile.ZipFile(io.BytesIO(response.content)) as z:
            z.extractall("data/PLCBEAD_repo")
            
        print("Extracting Structured Text files...")
        # Find all ST files
        st_files = glob.glob("data/PLCBEAD_repo/**/*.st", recursive=True)
        print(f"Found {len(st_files)} .st files.")
        
        with open(output_file, 'w', encoding='utf-8') as out_f:
            for st_file in st_files:
                with open(st_file, 'r', encoding='utf-8', errors='ignore') as f:
                    code = f.read()
                    
                if len(code.strip()) < 50:
                    continue # Skip very small or empty files
                    
                # Create a simple completion task
                instruction = f"Complete the following IEC 61131-3 Structured Text program for {os.path.basename(st_file)}:"
                record = format_as_chatml(instruction, code)
                out_f.write(json.dumps(record) + "\n")
                
        print(f"Successfully created dataset at {output_file} with {len(st_files)} records.")
    else:
        print(f"Failed to download dataset. HTTP Status: {response.status_code}")

if __name__ == "__main__":
    process_plc_beAD()
