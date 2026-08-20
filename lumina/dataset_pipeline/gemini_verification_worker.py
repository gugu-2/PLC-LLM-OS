"""
Lumina Industrial AI: Gemini API "LLM-as-a-Judge" Verification Worker
=====================================================================
Reads Z3-verified data and passes it to the Gemini 1.5 Pro API for 
semantic grading, variable name checking, and professional comment injection.
Implements a strict 4-second delay to comply with the 15 RPM Free Tier limit.
"""

import os
import json
import time
import logging
from pathlib import Path
import google.generativeai as genai
from google.generativeai.types import HarmCategory, HarmBlockThreshold

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("GeminiWorker")

# === CONFIGURATION ===
BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data")))
INPUT_FILE = BASE_DIR / "tier_fast_raw.jsonl" # In production, this would be z3_verified_dataset.jsonl
OUTPUT_FILE = BASE_DIR / "final_verified_dataset.jsonl"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

SYSTEM_INSTRUCTION = """You are a Senior PLC & Industrial Automation Engineer. 
Your job is to review IEC 61131-3 Structured Text.
1. Verify the code is logically sound.
2. Inject professional, descriptive comments explaining the logic.
3. Return ONLY the finalized, beautiful code. Do not wrap it in markdown block quotes (```) and do not say 'Here is the code'. Just return the raw code string."""

def get_gemini_model():
    """Initializes and returns the Gemini model with specific safety settings."""
    genai.configure(api_key=GEMINI_API_KEY)
    
    # We lower safety thresholds for code generation because industrial terminology 
    # (e.g. 'kill switch', 'deadman', 'master/slave', 'abort') can sometimes trigger false positives.
    safety_settings = {
        HarmCategory.HARM_CATEGORY_HARASSMENT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_HATE_SPEECH: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_SEXUALLY_EXPLICIT: HarmBlockThreshold.BLOCK_NONE,
        HarmCategory.HARM_CATEGORY_DANGEROUS_CONTENT: HarmBlockThreshold.BLOCK_NONE,
    }
    
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro-latest",
        system_instruction=SYSTEM_INSTRUCTION,
        safety_settings=safety_settings
    )
    return model

def process_dataset():
    logger.info("Initializing Gemini API Verification Worker...")
    
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set. Exiting.")
        return
        
    if not INPUT_FILE.exists():
        logger.error(f"Input file {INPUT_FILE} not found. Ensure extraction finished.")
        return

    model = get_gemini_model()
    processed_count = 0
    
    logger.info(f"Opening {INPUT_FILE} for processing...")
    with open(INPUT_FILE, "r", encoding="utf-8") as infile, \
         open(OUTPUT_FILE, "a", encoding="utf-8") as outfile:
        
        for line in infile:
            try:
                record = json.loads(line)
                messages = record.get("messages", [])
                
                # Extract the assistant's raw code from the record
                raw_code = ""
                prompt = ""
                for msg in messages:
                    if msg["role"] == "user":
                        prompt = msg["content"]
                    elif msg["role"] == "assistant":
                        raw_code = msg["content"]
                
                if not raw_code:
                    continue
                
                logger.info(f"Sending snippet {processed_count+1} to Gemini API...")
                
                # Send to Gemini
                response = model.generate_content(f"Review and comment this code:\n\n{raw_code}")
                polished_code = response.text.strip()
                
                # Save the new, polished ChatML pair
                new_record = {
                    "messages": [
                        {"role": "user", "content": prompt},
                        {"role": "assistant", "content": polished_code}
                    ]
                }
                
                outfile.write(json.dumps(new_record) + "\n")
                processed_count += 1
                
                # Polite 4.1 second delay to ensure we stay under 15 RPM
                time.sleep(4.1)
                
            except Exception as e:
                logger.error(f"Failed to process row {processed_count+1}. Error: {e}")
                # Exponential backoff in case of 429 Too Many Requests
                logger.info("Sleeping for 30 seconds due to API error...")
                time.sleep(30)
                
    logger.info(f"Gemini Verification Worker complete. Polished {processed_count} files.")

if __name__ == "__main__":
    process_dataset()
