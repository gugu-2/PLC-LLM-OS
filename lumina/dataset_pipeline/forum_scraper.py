import os
import json
import time
import requests
from bs4 import BeautifulSoup
import urllib.parse

def format_as_chatml(instruction, response):
    return {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": response}
        ]
    }

class PLCSNetScraper:
    """Scrapes Q&A threads from PLCS.net."""
    def __init__(self, output_file="data/forum_raw_code.jsonl"):
        self.base_url = "http://www.plctalk.net/qanda/forumdisplay.php?f=2"
        self.thread_base = "http://www.plctalk.net/qanda/"
        self.output_file = output_file
        os.makedirs(os.path.dirname(output_file), exist_ok=True)

    def scrape(self, pages_to_scrape=2):
        print(f"[*] Starting PLCS.net scrape for {pages_to_scrape} pages...")
        total_extracted = 0
        
        with open(self.output_file, 'a', encoding='utf-8') as f:
            for page in range(1, pages_to_scrape + 1):
                try:
                    print(f"[*] Fetching PLCS.net Page {page}...")
                    response = requests.get(self.base_url, timeout=10)
                    soup = BeautifulSoup(response.text, 'html.parser')
                    
                    for link in soup.find_all('a', href=True):
                        href = link['href']
                        if "showthread.php?t=" in href:
                            thread_title = link.text.strip()
                            thread_url = urllib.parse.urljoin(self.thread_base, href)
                            
                            extracted = self._scrape_thread(thread_url, thread_title)
                            if extracted:
                                f.write(json.dumps(extracted) + "\n")
                                total_extracted += 1
                                
                            time.sleep(3)
                except Exception as e:
                    print(f"[!] Error scraping PLCS.net page {page}: {e}")
                    
        print(f"[*] PLCS.net scrape complete. Extracted {total_extracted} code snippets.")

    def _scrape_thread(self, url, title):
        try:
            res = requests.get(url, timeout=10)
            soup = BeautifulSoup(res.text, 'html.parser')
            
            code_blocks = soup.find_all(['pre', 'code'])
            if code_blocks:
                code_content = code_blocks[0].get_text(strip=True)
                if len(code_content) > 30 and ("IF " in code_content or "XIC " in code_content or ":=" in code_content):
                    instruction = f"Provide a PLC logic solution for the following scenario: {title}"
                    return format_as_chatml(instruction, code_content)
        except Exception:
            pass
        return None


class StackOverflowScraper:
    """Uses StackExchange API to pull highly-voted PLC questions."""
    def __init__(self, output_file="data/forum_raw_code.jsonl"):
        self.api_url = "https://api.stackexchange.com/2.3/questions"
        self.output_file = output_file

    def scrape(self):
        print(f"[*] Starting StackOverflow API scrape for [plc] tags...")
        params = {
            "order": "desc",
            "sort": "votes",
            "tagged": "plc",
            "site": "stackoverflow",
            "filter": "withbody"
        }
        
        total_extracted = 0
        try:
            res = requests.get(self.api_url, params=params, timeout=10)
            data = res.json()
            
            if "items" in data:
                with open(self.output_file, 'a', encoding='utf-8') as f:
                    for item in data["items"]:
                        title = item.get("title", "")
                        body = item.get("body", "")
                        
                        soup = BeautifulSoup(body, 'html.parser')
                        code_blocks = soup.find_all('code')
                        
                        if code_blocks:
                            best_code = max(code_blocks, key=lambda x: len(x.get_text())).get_text()
                            if len(best_code) > 30:
                                instruction = f"Write PLC code to solve: {title}"
                                record = format_as_chatml(instruction, best_code)
                                f.write(json.dumps(record) + "\n")
                                total_extracted += 1
                                
        except Exception as e:
            print(f"[!] Error querying StackExchange API: {e}")
            
        print(f"[*] StackOverflow scrape complete. Extracted {total_extracted} code snippets.")


if __name__ == "__main__":
    print("==================================================")
    print(" Lumina Multi-Source Industrial Web Scraper")
    print("==================================================")
    output = "data/forum_raw_code.jsonl"
    
    so_scraper = StackOverflowScraper(output_file=output)
    so_scraper.scrape()
    
    plcs_scraper = PLCSNetScraper(output_file=output)
    plcs_scraper.scrape(pages_to_scrape=1)
    
    print(f"\n[*] All scraped data saved to {output}.")
    print("[*] Recommended Next Step: Run this raw data through clean_dataset.py Z3 verification.")
