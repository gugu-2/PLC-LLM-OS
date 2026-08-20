import os
import json
import requests
import time

def scrape_github_snippets(output_file="data/github_snippets_raw.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print("Scraping GitHub for .scl and .st code snippets...")
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Accept': 'application/vnd.github.v3+json'
    }
    
    # We will search for code that has 'FUNCTION_BLOCK' and extension .scl
    queries = [
        "FUNCTION_BLOCK extension:scl",
        "PROGRAM extension:st",
        "FUNCTION extension:st",
        "END_FUNCTION_BLOCK extension:scl"
    ]
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for query in queries:
            print(f"Searching: {query}")
            url = f"https://api.github.com/search/code?q={requests.utils.quote(query)}&per_page=10"
            
            resp = requests.get(url, headers=headers)
            if resp.status_code == 200:
                items = resp.json().get('items', [])
                for item in items:
                    raw_url = item.get('html_url', '').replace('github.com', 'raw.githubusercontent.com').replace('/blob/', '/')
                    if not raw_url: continue
                    
                    # Fetch the raw code
                    time.sleep(1) # Rate limit
                    raw_resp = requests.get(raw_url)
                    if raw_resp.status_code == 200:
                        content = raw_resp.text
                        if len(content.strip()) > 50:
                            record = {
                                "messages": [
                                    {"role": "user", "content": f"Write the PLC logic implementation for {item.get('name')}"},
                                    {"role": "assistant", "content": content}
                                ]
                            }
                            f.write(json.dumps(record) + "\n")
                            total_records += 1
            elif resp.status_code == 403:
                print("GitHub API rate limit exceeded for code search.")
                break
            time.sleep(6) # GitHub search API rate limit is 10/min without auth
            
    print(f"Saved to {output_file} with {total_records} snippets.")

if __name__ == "__main__":
    scrape_github_snippets()
