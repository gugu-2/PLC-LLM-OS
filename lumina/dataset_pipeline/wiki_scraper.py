import json
import os
import requests
from bs4 import BeautifulSoup

def format_as_chatml(title, content):
    return {
        "messages": [
            {"role": "user", "content": f"Explain {title} in the context of industrial automation."},
            {"role": "assistant", "content": content}
        ]
    }

def scrape_wikipedia(topics, output_file="data/wiki_domain_knowledge.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Scraping Wikipedia domain knowledge for topics: {topics}...")
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for topic in topics:
            url = f"https://en.wikipedia.org/wiki/{topic}"
            print(f"Fetching {url}")
            headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                soup = BeautifulSoup(resp.text, 'html.parser')
                content_div = soup.find('div', {'id': 'mw-content-text'})
                
                # Extract text from all paragraphs
                paragraphs = content_div.find_all('p')
                full_text = "\n\n".join([p.get_text().strip() for p in paragraphs if len(p.get_text().strip()) > 50])
                
                if full_text:
                    record = format_as_chatml(topic.replace('_', ' '), full_text)
                    f.write(json.dumps(record) + "\n")
                    total_records += 1
            else:
                print(f"Failed to fetch {topic} - Status {resp.status_code}")
                
    print(f"Saved to {output_file} with {total_records} domain knowledge records.")

if __name__ == "__main__":
    topics = [
        "Programmable_logic_controller", 
        "IEC_61131-3", 
        "Structured_text", 
        "SCADA",
        "Modbus",
        "Profibus",
        "OPC_Unified_Architecture",
        "Programmable_automation_controller",
        "Industrial_control_system",
        "PID_controller"
    ]
    scrape_wikipedia(topics)
