import os
import json
import time
from github import Github, RateLimitExceededException

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

def scrape_github_code(extensions, token, output_file="data/github_raw_code.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    g = Github(token)
    print(f"Scraping GitHub for files with extensions: {extensions}...")
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for ext in extensions:
            print(f"Searching for extension: {ext}")
            query = f"extension:{ext.strip('.')}"
            try:
                # We limit to 50 results per extension to avoid aggressive secondary rate limits
                results = g.search_code(query)
                count = 0
                for repo_file in results:
                    if count >= 50:
                        break
                    try:
                        content = repo_file.decoded_content.decode('utf-8', errors='ignore')
                        if len(content.strip()) < 20: continue # skip essentially empty files
                        
                        # Vendor Mapping
                        vendor_map = {
                            "scl": "Siemens Structured Control Language (SCL)",
                            "awl": "Siemens Statement List (AWL/STL)",
                            "tc1po": "Beckhoff TwinCAT",
                            "L5X": "Rockwell/Allen-Bradley XML",
                            "gcode": "CNC G-Code",
                            "st": "IEC 61131-3 Structured Text",
                            "xst": "Schneider Electric Unity Pro / EcoStruxure",
                            "smc2": "Omron Sysmac Studio",
                            "gxw": "Mitsubishi GX Works",
                            "export": "Codesys ST Export"
                        }
                        
                        ext_key = ext.strip('.')
                        vendor_name = vendor_map.get(ext_key, "PLC")
                        
                        instruction = f"Write the {vendor_name} logic for the following program: {repo_file.name}"
                        record = format_as_chatml(instruction, content)
                        f.write(json.dumps(record) + "\n")
                        total_records += 1
                        count += 1
                    except Exception as e:
                        pass
                    # GitHub API requests a sleep between code search item fetches
                    time.sleep(2) 
                    
            except RateLimitExceededException:
                print("Rate limit exceeded. Skipping remaining.")
                break
            except Exception as e:
                print(f"Error searching for {ext}: {e}")
                
    print(f"Saved to {output_file} with {total_records} records.")

if __name__ == "__main__":
    import sys
    token = sys.argv[1] if len(sys.argv) > 1 else None
    if not token:
        print("Please provide a GitHub token as the first argument.")
        sys.exit(1)
        
    extensions_to_scrape = [
        ".scl", ".awl", ".tc1po", ".L5X", ".gcode", 
        ".st", ".xst", ".export", ".smc2", ".gxw"
    ]
    scrape_github_code(extensions_to_scrape, token)
