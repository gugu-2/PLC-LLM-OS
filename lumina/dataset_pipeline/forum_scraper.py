import os
import json
import requests
from bs4 import BeautifulSoup

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

def scrape_plcs_net(output_file="data/plcs_net_qa.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("Scraping PLCS.net forum...")
    # Basic outline for scraping PLCS.net
    # In reality, this requires parsing thread HTML, grabbing the original question and accepted/best answer.
    
    with open(output_file, 'w', encoding='utf-8') as f:
        # Example dummy entry
        dummy = format_as_chatml("Why is my TON timer not resetting when IN goes low?", "Check if you have an overlapping M memory bit...")
        f.write(json.dumps(dummy) + "\n")
        
    print(f"Saved to {output_file}")

if __name__ == "__main__":
    scrape_plcs_net()
