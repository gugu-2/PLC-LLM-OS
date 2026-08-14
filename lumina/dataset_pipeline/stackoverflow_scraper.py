import os
import json
import requests
import time
import html

API_URL = "https://api.stackexchange.com/2.3/search/advanced"

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

def fetch_answers(answer_ids):
    # max 100 ids per request
    ids_str = ";".join(map(str, answer_ids))
    ans_url = f"https://api.stackexchange.com/2.3/answers/{ids_str}?order=desc&sort=activity&site=stackoverflow&filter=withbody"
    resp = requests.get(ans_url)
    if resp.status_code == 200:
        return resp.json().get("items", [])
    return []

def scrape_stackoverflow_plc(tags, output_file="data/so_plc_qa.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    
    print(f"Scraping Stack Overflow for tags: {tags}...")
    
    total_records = 0
    with open(output_file, 'w', encoding='utf-8') as f:
        for tag in tags:
            print(f"Fetching questions for tag: {tag}")
            # Fetch questions with accepted answers
            params = {
                "order": "desc",
                "sort": "votes",
                "accepted": "True",
                "tagged": tag,
                "site": "stackoverflow",
                "filter": "withbody",
                "pagesize": 100
            }
            
            resp = requests.get(API_URL, params=params)
            if resp.status_code == 200:
                data = resp.json()
                items = data.get("items", [])
                print(f"Found {len(items)} questions with accepted answers for tag {tag}")
                
                # We have the question body, but we need the accepted answer body
                accepted_answer_ids = [item["accepted_answer_id"] for item in items if "accepted_answer_id" in item]
                
                # Fetch answers in chunks of 100
                answers_data = {}
                for i in range(0, len(accepted_answer_ids), 100):
                    chunk = accepted_answer_ids[i:i+100]
                    ans_items = fetch_answers(chunk)
                    for ans in ans_items:
                        answers_data[ans["answer_id"]] = ans["body"]
                
                for item in items:
                    q_body_html = html.unescape(item.get("body", ""))
                    q_title = html.unescape(item.get("title", ""))
                    ans_id = item.get("accepted_answer_id")
                    
                    if ans_id in answers_data:
                        from bs4 import BeautifulSoup
                        a_body_html = html.unescape(answers_data[ans_id])
                        
                        # Extract raw text, keeping some separation for readability
                        q_body_text = BeautifulSoup(q_body_html, "html.parser").get_text(separator="\n\n").strip()
                        a_body_text = BeautifulSoup(a_body_html, "html.parser").get_text(separator="\n\n").strip()
                        
                        instruction = f"{q_title}\n\n{q_body_text}"
                        record = format_as_chatml(instruction, a_body_text)
                        f.write(json.dumps(record) + "\n")
                        total_records += 1
                        
            else:
                print(f"Failed to fetch {tag}: {resp.status_code} - {resp.text}")
                
            time.sleep(1) # simple rate limit respect
            
    print(f"Saved to {output_file} with {total_records} records.")

if __name__ == "__main__":
    import sys
    tags_to_scrape = [
        "plc", "structured-text", "siemens-tia-portal", 
        "mitsubishi-plc", "omron", "schneider-electric", "codesys"
    ]
    scrape_stackoverflow_plc(tags_to_scrape)
