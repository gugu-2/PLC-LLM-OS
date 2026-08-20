import os
import json
import time
import google.generativeai as genai
from concurrent.futures import ThreadPoolExecutor, as_completed

# ---------------------------------------------------------
# LUMINA PLC-LLM-OS: INFINITE SWARM DAEMON
# ---------------------------------------------------------
# This script bridges the gap between the Chat UI limit (252)
# and the 50,000+ data point goal using your Gemini 3.1 Pro 
# High credits in the background.
# ---------------------------------------------------------

# Configure your API Key here (or export it to your environment)
API_KEY = os.environ.get("GEMINI_API_KEY")
genai.configure(api_key=API_KEY)

# Use the highest reasoning model available
MODEL_NAME = 'gemini-3.1-pro-preview' 
TARGET_COUNT = 50000
BATCH_SIZE = 10
OUTPUT_FILE = r'C:\Users\majip\Downloads\LLM REASEARCH\data\evol_instruct_dataset.jsonl'

def generate_evol_instruct(seed_prompt):
    """Hits the Gemini API to run the 5-step Evol-Instruct mutation sequence."""
    model = genai.GenerativeModel(MODEL_NAME)
    
    system_prompt = f"""
    You are an autonomous Evol-Instruct Synthetic Data Generator for Industrial Automation (IEC 61131-3).
    Your assigned seed is: "{seed_prompt}"
    
    Task:
    1. Generate Base Code in perfect IEC 61131-3 ST/SCL.
    2. Mutation 1 (Depth): Add a critical sub-system.
    3. Mutation 2 (Breadth): Add Profinet/EtherCAT diagnostics.
    4. Mutation 3 (Reasoning): Add IEC 62443 cybersec & SCADA logic.
    5. Mutation 4 (Adversarial): Add sensor drift, HIL sync, and self-tests.
    
    Return EXACTLY 5 JSON lines in ChatML format: {{"messages": [{{"role": "user", "content": "..."}}, {{"role": "assistant", "content": "..."}}]}}
    Do not wrap in markdown ```json blocks.
    """
    
    try:
        response = model.generate_content(system_prompt)
        return response.text.strip().split('\n')
    except Exception as e:
        print(f"[!] Error generating seed: {e}")
        return []

def main():
    print(f"[START] LUMINA SWARM DAEMON INITIALIZED")
    print(f"Targeting: {TARGET_COUNT} Synthetic Pairs")
    print(f"Using Model: {MODEL_NAME}")
    
    # Check current count
    current_count = 0
    if os.path.exists(OUTPUT_FILE):
        with open(OUTPUT_FILE, 'r') as f:
            current_count = sum(1 for _ in f)
    
    print(f"Starting at count: {current_count}")
    
    # Generic seed list generator (this can be expanded infinitely via another LLM call or random combinations)
    industries = ["Automotive", "Oil & Gas", "Pharma", "Water", "Energy", "Metals"]
    components = ["PID Loop", "State Machine", "VFD Control", "Safety Interlock", "Motion Control"]
    
    def seed_generator():
        while True:
            import random
            yield f"Write a PLC program for {random.choice(industries)} using {random.choice(components)}."

    generator = seed_generator()
    
    while current_count < TARGET_COUNT:
        print(f"\n--- Spawning Batch (Current: {current_count}/{TARGET_COUNT}) ---")
        
        batch_seeds = [next(generator) for _ in range(BATCH_SIZE)]
        
        with ThreadPoolExecutor(max_workers=BATCH_SIZE) as executor:
            future_to_seed = {executor.submit(generate_evol_instruct, seed): seed for seed in batch_seeds}
            
            with open(OUTPUT_FILE, 'a', encoding='utf-8') as f:
                for future in as_completed(future_to_seed):
                    results = future.result()
                    for line in results:
                        if line.startswith('{') and line.endswith('}'):
                            f.write(line + '\n')
                            current_count += 1
                            
        print(f"Batch complete. New Count: {current_count}")
        time.sleep(2) # Rate limit protection

if __name__ == "__main__":
    main()
