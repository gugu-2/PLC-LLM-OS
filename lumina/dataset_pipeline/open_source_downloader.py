import os
import json
import subprocess
from pathlib import Path

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

class DatasetDownloader:
    def __init__(self, base_dir="data"):
        self.base_dir = Path(base_dir)
        self.repos_dir = self.base_dir / "repos"
        self.repos_dir.mkdir(parents=True, exist_ok=True)
        
        # Define the three distinct data sources
        self.datasets = {
            "oscat": {
                "url": "https://github.com/mihaiginta/TcOscatBasic.git", # Working OSCAT Basic Library mirror (TwinCAT port)
                "extensions": [".st", ".exp", ".scl", ".tcpou"],
                "raw_output": self.base_dir / "oscat_raw.jsonl",
                "verified_output": self.base_dir / "verified_oscat.jsonl"
            },
            "tcopen": {
                "url": "https://github.com/TcOpenGroup/TcOpen.git", # Beckhoff OOP Framework
                "extensions": [".st"],
                "raw_output": self.base_dir / "tcopen_raw.jsonl",
                "verified_output": self.base_dir / "verified_tcopen.jsonl"
            },
            "siemens_lgf": {
                "url": "https://github.com/OttoMeister/Siemens-Tia-Portal-PID-Controller.git", # Proxy for Siemens libraries
                "extensions": [".scl", ".awl"],
                "raw_output": self.base_dir / "siemens_lgf_raw.jsonl",
                "verified_output": self.base_dir / "verified_siemens_lgf.jsonl"
            }
        }

    def _clone_repo(self, name, url):
        target_dir = self.repos_dir / name
        if not target_dir.exists():
            print(f"[*] Cloning {name} from {url}...")
            try:
                subprocess.run(["git", "clone", "--depth", "1", url, str(target_dir)], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
                print(f"[OK] Successfully cloned {name}.")
            except subprocess.CalledProcessError:
                print(f"[!] Failed to clone {name}. It may require manual download.")
        else:
            print(f"[*] {name} already exists. Skipping clone.")
        return target_dir

    def process_dataset(self, name, config):
        print(f"\n======================================")
        print(f" Processing Dataset: {name.upper()}")
        print(f"======================================")
        
        repo_dir = self._clone_repo(name, config["url"])
        if not repo_dir.exists():
            return
            
        total_extracted = 0
        
        # Extract files and convert to ChatML format for the LLM
        with open(config["raw_output"], 'w', encoding='utf-8') as f_out:
            for root, _, files in os.walk(repo_dir):
                for file in files:
                    if any(file.lower().endswith(ext.lower()) for ext in config["extensions"]):
                        file_path = Path(root) / file
                        try:
                            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f_in:
                                content = f_in.read()
                                
                            if len(content.strip()) < 50:
                                continue # Skip empty files
                                
                            # Create a high-quality instruction prompt
                            instruction = f"Write the PLC logic implementation for the '{file_path.stem}' function block/module."
                            record = format_as_chatml(instruction, content)
                            
                            f_out.write(json.dumps(record) + "\n")
                            total_extracted += 1
                        except Exception as e:
                            pass
                            
        print(f"[OK] {name.upper()} raw extraction complete. {total_extracted} files saved to {config['raw_output']}.")
        print(f"[*] Next step: Run `python lumina/dataset_pipeline/clean_dataset.py {config['raw_output']} {config['verified_output']}`")

    def run_all(self):
        # We process them strictly independently as requested
        for name, config in self.datasets.items():
            self.process_dataset(name, config)

if __name__ == "__main__":
    downloader = DatasetDownloader()
    downloader.run_all()
