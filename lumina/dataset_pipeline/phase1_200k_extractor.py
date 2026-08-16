"""
Lumina Phase 1 Data Extractor
=============================
Massive 200,000-row natural data extraction orchestrator.
Targets GitHub GraphQL API and specific Enterprise Libraries (OSCAT, TcOpen).
Outputs raw, unverified ChatML blocks for offline Z3 processing later.
"""

import os
import json
import time
import requests
import base64
import logging
from pathlib import Path

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("Phase1Extractor")

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data")))
OUTPUT_FILE = BASE_DIR / "phase1_200k_raw.jsonl"
GITHUB_PAT = os.environ.get("GITHUB_PAT") # Set via environment variable for security
TARGET_ROWS = 200000

HEADERS = {
    "Authorization": f"token {GITHUB_PAT}",
    "Accept": "application/vnd.github.v3+json"
}

def write_chatml(instruction: str, code: str, filepath: Path):
    record = {
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": code}
        ]
    }
    with open(filepath, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def check_rate_limit():
    """Checks the GitHub API rate limit and sleeps if necessary."""
    try:
        response = requests.get("https://api.github.com/rate_limit", headers=HEADERS)
        if response.status_code == 200:
            data = response.json()
            remaining = data['resources']['core']['remaining']
            reset_time = data['resources']['core']['reset']
            if remaining < 100:
                sleep_seconds = max(0, reset_time - int(time.time())) + 10
                logger.warning(f"Rate limit extremely low ({remaining} left). Sleeping for {sleep_seconds} seconds.")
                time.sleep(sleep_seconds)
    except Exception as e:
        logger.error(f"Failed to check rate limit: {e}")

def scrape_github_search(query: str, target_count: int, file_ext: str, current_total: int) -> int:
    """Uses GitHub REST API to search for code snippets and extracts them."""
    page = 1
    extracted_here = 0
    
    while current_total + extracted_here < target_count:
        check_rate_limit()
        
        search_url = f"https://api.github.com/search/code?q={query}&per_page=100&page={page}"
        logger.info(f"Fetching GitHub Page {page} for query: {query}")
        
        try:
            response = requests.get(search_url, headers=HEADERS)
            if response.status_code == 403: # Rate limit hit during search
                logger.warning("Search API rate limit hit. Sleeping for 60 seconds.")
                time.sleep(60)
                continue
            if response.status_code != 200:
                logger.error(f"Search failed with code {response.status_code}: {response.text}")
                break
                
            items = response.json().get('items', [])
            if not items:
                break # No more results
                
            for item in items:
                # We need to fetch the actual file content
                content_url = item.get("url") # This is the API URL for the file content
                if content_url:
                    content_resp = requests.get(content_url, headers=HEADERS)
                    if content_resp.status_code == 200:
                        file_data = content_resp.json()
                        if 'content' in file_data:
                            try:
                                raw_code = base64.b64decode(file_data['content']).decode('utf-8')
                                if len(raw_code.strip()) > 50:
                                    filename = item.get("name", f"module{file_ext}")
                                    instruction = f"Write the PLC implementation for '{filename}'."
                                    write_chatml(instruction, raw_code, OUTPUT_FILE)
                                    extracted_here += 1
                                    
                                    if (current_total + extracted_here) % 1000 == 0:
                                        logger.info(f"Progress: {current_total + extracted_here} / {TARGET_ROWS} rows extracted.")
                                        
                                    if current_total + extracted_here >= target_count:
                                        return extracted_here
                            except Exception:
                                pass # Base64 decode errors
                    time.sleep(0.5) # Slight delay to avoid triggering abuse mechanism
            page += 1
        except Exception as e:
            logger.error(f"Exception during GitHub scrape: {e}")
            time.sleep(10)
            
    return extracted_here

def main():
    logger.info("Initializing Phase 1: 200K Natural Data Extraction...")
    
    total_extracted = 0
    
    # Check current file size if we are resuming
    if OUTPUT_FILE.exists():
        with open(OUTPUT_FILE, 'r', encoding='utf-8') as f:
            total_extracted = sum(1 for _ in f)
        logger.info(f"Resuming extraction. Current row count: {total_extracted}")
        
    # Define search targets for high-quality PLC code
    search_queries = [
        ("extension:scl size:>50", ".scl"),
        ("extension:st size:>50", ".st"),
        ("extension:L5X size:>500", ".L5X"),
        ("extension:awl size:>50", ".awl"),
        ("extension:exp size:>50", ".exp")
    ]
    
    for query, ext in search_queries:
        if total_extracted >= TARGET_ROWS:
            break
            
        logger.info(f"Starting extraction for {ext} files...")
        count = scrape_github_search(query, TARGET_ROWS, ext, total_extracted)
        total_extracted += count
        
    logger.info(f"Phase 1 Operation Halted. Total Extracted: {total_extracted} rows.")

if __name__ == "__main__":
    main()
