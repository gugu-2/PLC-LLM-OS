"""
Lumina Industrial AI: Evol-Instruct Synthetic Data Generation Engine
=====================================================================
Generates complex, multi-layered PLC training data using the Evol-Instruct
methodology - the same technique used by DeepSeek and Alibaba (Qwen).

Process:
1. Load 100 seed prompts from seeds.json
2. Mutate each seed through 4 complexity levels via Gemini API
3. Save every prompt/code pair to the dataset in ChatML format
"""

import os
import json
import time
import logging
import random
from pathlib import Path
import google.generativeai as genai

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EvolInstruct")

# === CONFIGURATION ===
BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data")))
SEEDS_FILE = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "seeds.json")))
OUTPUT_FILE = BASE_DIR / "evol_instruct_dataset.jsonl"
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY")

# 4 Mutation levels that progressively make the problem harder
MUTATION_TEMPLATES = [
    # Mutation 1: Add Depth (add one critical sub-system)
    "Take this PLC programming task and make it significantly harder by adding one critical sub-system. Keep the same platform. Original task: {seed}",
    
    # Mutation 2: Add Breadth (integrate industrial communications + diagnostics)
    "Upgrade this PLC task to also include industrial communication (Profinet/EtherCAT/Ethernet-IP), a detailed fault diagnostic system with alarm codes, and a production counter. Task: {seed}",
    
    # Mutation 3: Add Reasoning (add safety + failover + SCADA integration)
    "Make this PLC task enterprise-grade by adding: IEC 62443 cybersecurity considerations, a hot-standby failover mechanism, SCADA integration via OPC UA, and a comprehensive operator HMI data structure. Task: {seed}",
    
    # Mutation 4: Add Adversarial Thinking (inject failure + recovery logic)
    "This is the ultimate version of the task. Add sensor drift detection and auto-calibration, a hardware-in-the-loop digital twin synchronization block, predictive maintenance counters, and a self-test routine that runs at startup. Task: {seed}"
]

SYSTEM_PROMPT = """You are a world-class Senior PLC & Industrial Automation Engineer with 25 years of experience.
When writing code:
1. Write COMPLETE, fully functional, production-ready IEC 61131-3 Structured Text code.
2. Include ALL variable declarations in a proper VAR block.
3. Add professional, detailed comments explaining every logical section.
4. Use industry-standard naming conventions (e.g. xMotorRun, rTemperature, nCounter).
5. Never write placeholder code or use '...' ellipsis. Always write the complete implementation.
6. Return ONLY the raw code. No markdown fences. No preamble. Just pure Structured Text."""

def setup_gemini():
    """Initializes the Gemini model."""
    if not GEMINI_API_KEY:
        logger.error("GEMINI_API_KEY environment variable not set!")
        return None
    genai.configure(api_key=GEMINI_API_KEY)
    model = genai.GenerativeModel(
        model_name="gemini-1.5-pro",
        system_instruction=SYSTEM_PROMPT
    )
    return model

def write_chatml(prompt: str, code: str):
    """Writes a prompt/code pair to the output JSONL file."""
    record = {
        "messages": [
            {"role": "user", "content": prompt},
            {"role": "assistant", "content": code}
        ]
    }
    with open(OUTPUT_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")

def generate_evolved_data(model, seed: dict) -> int:
    """Takes one seed and runs it through all 4 Evol-Instruct mutations."""
    generated = 0
    seed_prompt = seed["prompt"]
    
    # First save the original seed itself
    logger.info(f"  [SEED] Generating base code for: '{seed_prompt[:60]}...'")
    try:
        response = model.generate_content(seed_prompt)
        code = response.text.strip()
        if len(code) > 100:
            write_chatml(seed_prompt, code)
            generated += 1
    except Exception as e:
        logger.error(f"  [SEED ERROR] {e}")
    time.sleep(4.1)

    # Run through all 4 mutation levels
    for i, mutation_template in enumerate(MUTATION_TEMPLATES):
        mutation_prompt = mutation_template.format(seed=seed_prompt)
        logger.info(f"  [MUTATION {i+1}/4] Evolving complexity...")
        try:
            response = model.generate_content(mutation_prompt)
            code = response.text.strip()
            if len(code) > 100:
                # Save the mutation prompt + evolved code as a training pair
                write_chatml(mutation_prompt, code)
                generated += 1
        except Exception as e:
            logger.error(f"  [MUTATION {i+1} ERROR] {e}")
        time.sleep(4.1)
        
    return generated

def main():
    logger.info("=" * 60)
    logger.info("  LUMINA EVOL-INSTRUCT SYNTHETIC DATA ENGINE")
    logger.info("=" * 60)
    
    if not SEEDS_FILE.exists():
        logger.error(f"Seeds file not found at {SEEDS_FILE}")
        return
    
    model = setup_gemini()
    if not model:
        return

    with open(SEEDS_FILE, "r") as f:
        seed_data = json.load(f)
    
    seeds = seed_data["seeds"]
    total_generated = 0
    
    logger.info(f"Loaded {len(seeds)} seeds. Beginning Evol-Instruct generation...")
    logger.info(f"Expected output: ~{len(seeds) * 5} training pairs (1 base + 4 mutations per seed)")
    logger.info(f"Estimated time: ~{(len(seeds) * 5 * 4.5) / 3600:.1f} hours on Free Tier")
    logger.info("-" * 60)
    
    # Shuffle seeds so each run produces diverse data even if interrupted
    random.shuffle(seeds)
    
    for idx, seed in enumerate(seeds):
        logger.info(f"\n[Seed {idx+1}/{len(seeds)}] Category: {seed['category']} | Platform: {seed['platform']}")
        count = generate_evolved_data(model, seed)
        total_generated += count
        logger.info(f"  Seed complete. Generated {count} pairs. Total so far: {total_generated}")

    logger.info("\n" + "=" * 60)
    logger.info(f"  GENERATION COMPLETE. Total pairs saved: {total_generated}")
    logger.info(f"  Output file: {OUTPUT_FILE}")
    logger.info("=" * 60)

if __name__ == "__main__":
    main()
