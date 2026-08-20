import os
import json
import random
import time
import logging
from pathlib import Path
from ollama_client import OllamaClient
from linter import ST_Linter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EvolOrchestrator")

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
SEEDS_DIR = BASE_DIR / "seeds"
VAULT_DIR = BASE_DIR / "generated_vault"
OUTPUT_FILE = VAULT_DIR / "synthetic_generation_v3_enterprise.jsonl"

def load_seeds() -> list:
    """Load the golden seed records to use for RAG/Few-Shot prompting."""
    seeds = []
    logger.info("Loading segregated seed datasets...")
    
    for tier_dir in sorted(SEEDS_DIR.iterdir()):
        if not tier_dir.is_dir():
            continue
        tier_count = 0
        for jsonl_file in tier_dir.glob("*.jsonl"):
            with open(jsonl_file, "r", encoding="utf-8") as f:
                for line in f:
                    if line.strip():
                        try:
                            record = json.loads(line)
                            for msg in record.get("messages", []):
                                if msg["role"] == "assistant":
                                    seeds.append(msg["content"])
                            tier_count += 1
                        except:
                            pass
        logger.info(f"Loaded {tier_count} records from {tier_dir.name}")
        
    logger.info(f"Total seeds loaded: {len(seeds)}")
    return seeds

def extract_code_block(response: str) -> str:
    """Extract code hidden inside Markdown blocks."""
    if "`" in response:
        # Extract everything between the first and last backticks
        parts = response.split("`")
        if len(parts) >= 3:
            # Usually the code is in the second block
            code = parts[1]
            if code.startswith("iec") or code.startswith("st") or code.startswith("pascal"):
                code = code.split("\n", 1)[-1]
            return code.strip()
    return response.strip()

def run_evolution_loop(client: OllamaClient, linter: ST_Linter, seeds: list, iterations: int = 100):
    os.makedirs(VAULT_DIR, exist_ok=True)
    
    scenarios = [
        "a High-Speed Sorting Conveyor with optical sensors",
        "a 3-Axis CNC Router with safety interlocks",
        "a PID-controlled Chemical Mixing Vat with temperature bounds",
        "an Automated Storage and Retrieval System (ASRS)",
        "a Water Treatment Pumping Station with fail-over redundancy"
    ]
    
    successful_generations = 0
    
    with open(OUTPUT_FILE, 'a', encoding='utf-8') as vault_db:
        for i in range(iterations):
            logger.info(f"--- Starting Evolution Cycle {i+1}/{iterations} ---")
            
            # 1. RAG Seed Selection
            if seeds:
                selected_seeds = random.sample(seeds, min(2, len(seeds)))
                seed_context = "\n\n=== VERIFIED EXAMPLE ===\n".join(selected_seeds)
            else:
                seed_context = "No seeds available. Relying on base weights."
                
            scenario = random.choice(scenarios)
            
            # 2. Construct the Master Prompt
            system_prompt = (
                "You are an elite Industrial Automation Engineer. Your task is to write deterministic, "
                "production-ready IEC 61131-3 Structured Text (ST).\n\n"
                f"=== REFERENCE KNOWLEDGE ===\n{seed_context}\n\n"
                "=== INSTRUCTION ===\n"
                f"Using the mathematical rigor and syntax shown in the examples above, write a complete FUNCTION_BLOCK "
                f"to control {scenario}. Include VAR declarations and the operational logic. "
                "OUTPUT ONLY THE RAW CODE. DO NOT OUTPUT MARKDOWN. DO NOT APOLOGIZE. DO NOT EXPLAIN."
            )
            
            messages = [{"role": "user", "content": system_prompt}]
            
            # 3. The Generation & Reflection Loop
            max_retries = 3
            passed = False
            
            for attempt in range(max_retries):
                logger.info(f"Requesting generation from GPU (Attempt {attempt+1})...")
                raw_response = client.generate_chat(messages, temperature=0.7)
                code = extract_code_block(raw_response)
                
                # 4. The Verification Gauntlet
                is_valid, error_msg = linter.verify_code(code)
                
                if is_valid:
                    logger.info("? Code Passed the Z3 Mathematical Gauntlet! Saving to Vault.")
                    
                    # Format as ChatML for future training
                    record = {
                        "messages": [
                            {"role": "user", "content": f"Write a complete IEC 61131-3 FUNCTION_BLOCK to control {scenario}."},
                            {"role": "assistant", "content": code}
                        ]
                    }
                    vault_db.write(json.dumps(record) + "\n")
                    vault_db.flush()
                    
                    # Add to seeds so the AI learns from itself!
                    seeds.append(code)
                    successful_generations += 1
                    passed = True
                    break
                else:
                    logger.warning(f"? Verification Failed: {error_msg}")
                    # AI Reflection: Send the error back to the model so it can fix it
                    messages.append({"role": "assistant", "content": code})
                    messages.append({"role": "user", "content": f"Your code failed verification with this error: '{error_msg}'. Fix the logic and output only the corrected code."})
            
            if not passed:
                logger.error("? Code failed all reflection attempts. Discarding garbage data.")
            
            time.sleep(2) # Cooldown GPU
            
    logger.info(f"Evolution Complete. Successfully synthesized {successful_generations} pristine records.")

if __name__ == "__main__":
    logger.info("Initializing Ollama Client (Checking localhost:11434)...")
    client = OllamaClient(model="qwen2.5-coder:7b")
    
    if not client.check_health():
        logger.error("FATAL: Cannot connect to Ollama. Make sure Ollama is installed and running on your laptop!")
        exit(1)
        
    linter = ST_Linter()
    seed_pool = load_seeds()
    
    logger.info(f"Loaded {len(seed_pool)} Golden Seeds into memory.")
    run_evolution_loop(client, linter, seed_pool, iterations=100)
