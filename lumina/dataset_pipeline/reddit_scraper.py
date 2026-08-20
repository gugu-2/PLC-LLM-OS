import os
import json
import time
import random
import cloudscraper
from fake_useragent import UserAgent

def scrape_reddit(subreddit="PLC", limit=50, output_file="data/reddit_raw.jsonl"):
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    print(f"Scraping top posts from r/{subreddit} using human emulation...")
    
    # Use Cloudscraper to bypass Cloudflare anti-bot
    scraper = cloudscraper.create_scraper(browser={'browser': 'chrome', 'platform': 'windows', 'mobile': False})
    ua = UserAgent()
    
    url = f"https://www.reddit.com/r/{subreddit}/top.json?t=all&limit={limit}"
    
    total_records = 0
    with open(output_file, 'a', encoding='utf-8') as f:
        try:
            # Emulate human delay before requesting
            time.sleep(random.uniform(2.5, 6.2))
            
            headers = {
                'User-Agent': ua.random,
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
                'Accept-Language': 'en-US,en;q=0.5',
            }
            
            resp = scraper.get(url, headers=headers)
            if resp.status_code == 200:
                data = resp.json()
                children = data.get('data', {}).get('children', [])
                
                for child in children:
                    post = child['data']
                    title = post.get('title', '')
                    selftext = post.get('selftext', '')
                    
                    if len(selftext) > 100:
                        record = {
                            "messages": [
                                {"role": "user", "content": f"Discuss the following industrial automation topic: {title}"},
                                {"role": "assistant", "content": selftext}
                            ]
                        }
                        f.write(json.dumps(record) + "\n")
                        total_records += 1
            else:
                print(f"Failed to fetch Reddit API for r/{subreddit} - Status {resp.status_code}")
        except Exception as e:
            print(f"Exception during Reddit scraping: {e}")
            
    print(f"Saved to {output_file} with {total_records} records.")

if __name__ == "__main__":
    # Add severe randomized delays between subreddit scrapes
    scrape_reddit("PLC")
    print("Human emulation sleep...")
    time.sleep(random.uniform(15.2, 28.7)) 
    scrape_reddit("Scada")
