import os
import json
import random
import time
import logging
import re
from pathlib import Path
from ollama_client import OllamaClient
from linter import ST_Linter

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")
logger = logging.getLogger("EvolOrchestrator")

BASE_DIR = Path(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
SEEDS_DIR = BASE_DIR / "seeds"
VAULT_DIR = BASE_DIR / "generated_vault"
OUTPUT_FILE = VAULT_DIR / "synthetic_generation_v3_enterprise.jsonl"
TEMP_DIR = VAULT_DIR / "temp_scratch"

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
                        except json.JSONDecodeError as e:
                            logger.warning(f"Corrupt JSON seed skipped in {jsonl_file}: {e}")
                        except Exception as e:
                            logger.error(f"Unexpected error loading seed: {e}")
        logger.info(f"Loaded {tier_count} records from {tier_dir.name}")
        
    logger.info(f"Total seeds loaded: {len(seeds)}")
    return seeds

def extract_code_block(response: str) -> str:
    """
    Extract ST code from a markdown-fenced code block using regex.
    Handles ```iec-st, ```st, ```pascal, or generic ``` fences.
    """
    pattern = r'```(?:iec-st|iec61131|st|pascal|structured.text)?\s*\n(.*?)```'
    match = re.search(pattern, response, re.DOTALL | re.IGNORECASE)
    if match:
        return match.group(1).strip()
    
    # Fallback to any triple backtick block
    pattern_generic = r'```\s*\n(.*?)```'
    match = re.search(pattern_generic, response, re.DOTALL)
    if match:
        return match.group(1).strip()
        
    return response.strip()

def ensure_newline_at_eof(filepath: Path):
    """Checks if file exists and ends with a newline. If not, appends one."""
    if not filepath.exists() or filepath.stat().st_size == 0:
        return
    try:
        with open(filepath, 'rb+') as f:
            f.seek(-1, 2)
            last_char = f.read(1)
            if last_char != b'\n':
                f.write(b'\n')
    except Exception as e:
        logger.warning(f"Could not verify EOF newline: {e}")

def merge_temp_files(temp_dir: Path, output_file: Path):
    """Safely merges all temp JSON files into the single master JSONL file."""
    if not temp_dir.exists():
        return
        
    temp_files = list(temp_dir.glob("*.json"))
    if not temp_files:
        logger.info("No temporary files to merge.")
        return
        
    logger.info(f"Merging {len(temp_files)} generated records into {output_file.name}...")
    ensure_newline_at_eof(output_file)
        
    with open(output_file, 'a', encoding='utf-8') as dest:
        for tf in temp_files:
            try:
                with open(tf, 'r', encoding='utf-8') as src:
                    data = json.load(src)
                dest.write(json.dumps(data, ensure_ascii=False) + "\n")
                tf.unlink() # Delete temp file
            except Exception as e:
                logger.error(f"Failed to merge file {tf.name}: {e}")
                
    logger.info("Merge and cleanup complete.")

DOMAIN_INVENTOR_PROMPT = """
You are a world-class industrial automation consultant.
Invent ONE completely new and specific industrial, scientific, space, or military-defense (defensive/navigational only) domain for a PLC control challenge. 
Output ONLY a raw JSON object with this exact schema (no markdown formatting, no other text):
{
  "role": "<specific job title at a specific type of facility>",
  "system": "<specific machine or process being controlled>",
  "constraint": "<3 specific, advanced technical requirements>",
  "function_block_name": "<FB_CamelCase_Name>"
}
"""

BLOCKED_DOMAIN_PATTERNS = [
    "nuclear reactor", "uranium", "plutonium", "enrichment",
    "centrifuge cascade", "weapons grade", "explosive", 
    "nerve agent", "bioweapon", "pathogen synthesis",
    "inertial confinement", "thermonuclear"
]

def is_domain_safe(domain: dict) -> bool:
    """Pre-screen a domain before wasting an LLM call on it."""
    text = f"{domain.get('role','') or ''} {domain.get('system','') or ''} {domain.get('constraint','') or ''}".lower()
    for blocked in BLOCKED_DOMAIN_PATTERNS:
        if blocked in text:
            logger.warning(f"Domain pre-screened out (safety): {blocked}")
            return False
    return True

def invent_new_domain(client: OllamaClient, used_domains: set, failed_domains: list = None) -> dict:
    """Ask the local LLM to invent a fresh domain on the fly, learning from failures."""
    prompt = DOMAIN_INVENTOR_PROMPT
    if failed_domains:
        recent_failures = ", ".join(failed_domains[-10:])
        prompt += f"\n\nCRITICAL FEEDBACK: Do NOT invent anything similar to these previously FAILED systems: {recent_failures}."
        
    messages = [{"role": "user", "content": prompt}]
    response = client.generate_chat(messages, temperature=0.9)
    try:
        # Strip code fences if the model included them
        clean_resp = re.sub(r'^```[a-zA-Z0-9-]*\n', '', response.strip())
        clean_resp = re.sub(r'\n```$', '', clean_resp.strip()).strip()
        domain = json.loads(clean_resp)
        key = domain.get("function_block_name", "")
        if key in used_domains:
            return None
        if not is_domain_safe(domain):
            return None
        used_domains.add(key)
        return domain
    except Exception as e:
        logger.debug(f"Failed to invent domain: {e}")
        return None

def run_evolution_loop(client: OllamaClient, linter: ST_Linter, seeds: list, iterations: int = 100):
    os.makedirs(VAULT_DIR, exist_ok=True)
    os.makedirs(TEMP_DIR, exist_ok=True)
    
    # Check for and merge any orphaned temp files from a previously crashed run
    logger.info("Checking for orphaned temp files from previous runs...")
    merge_temp_files(TEMP_DIR, OUTPUT_FILE)
    
    # Enterprise V3 Dynamic Prompt Engine (Fallback lists)
    roles = [
        "Principal Controls Engineer at a Tier-1 Automotive Gigafactory",
        "Lead Mechatronics Architect at a top-tier Semiconductor firm",
        "Senior Systems Integrator for a Global E-Commerce Logistics Hub",
        "Chief Nuclear Engineer at a High-Energy Physics lab",
        "Lead Process Automation Engineer for a Mega-scale Chemical Refinery",
        "Chief Marine Automation Officer for a Deepwater Drillship",
        "Lead Aerospace Systems Engineer at a private spaceflight company"
    ]
    
    systems = [
        "an Extreme Ultraviolet (EUV) Lithography Vacuum Chamber",
        "a High-Pressure Aluminum Die-Casting (Giga Press) Controller",
        "a High-Speed Cross-Belt Sorter with Machine Vision",
        "a Tokamak Plasma Magnetic Confinement Controller",
        "a Superconducting Magnet Helium Cryogenics Ring Controller",
        "a Dynamic Positioning Class 3 (DP3) Thruster Allocation Matrix",
        "a Rocket Engine Test Stand with Thrust Vector Gimballing"
    ]
    
    constraints = [
        "Include ultra-high vacuum pump sequencing, magnetic levitation control, and strict SECS/GEM host communications.",
        "Include multi-stage hydraulic injection profiling, tie-bar strain gauge monitoring, and strict PackML standards.",
        "Include a TCP/IP socket connection block, dynamic FIFO shift registers, and induction cell synchronization.",
        "Include Liquid Helium (LHe) supercritical phase tracking, quench detection heaters, and VFD sequencing.",
        "Include Kalman filter position matrices, triple-modular redundancy voting logic, and harmonic resonance avoidance.",
        "Include PID-driven thermal runaway mitigation, Arrhenius temperature correction, and cross-coupled safety interlocks."
    ]
    
    used_domains = set()
    failed_domains = []
    successful_generations = 0
    
    for i in range(iterations):
        logger.info(f"--- Starting Enterprise Evolution Cycle {i+1}/{iterations} ---")
        
        # Try to invent a fresh domain first
        domain = invent_new_domain(client, used_domains, failed_domains)
        if domain:
            role = domain["role"]
            system = domain["system"]
            constraint = domain["constraint"]
            fb_name = domain.get("function_block_name", "FB_Controller")
            logger.info(f"Invented new domain: {role} -> {system}")
        else:
            # Fallback to static lists
            role = random.choice(roles)
            system = random.choice(systems)
            constraint = random.choice(constraints)
            fb_name = "FB_Controller"
            logger.info("Using fallback static domain.")

        if seeds:
            selected_seeds = random.sample(seeds, min(2, len(seeds)))
            
            # Format seeds with fences (ARCH-004) and enforce limit (BUG-005)
            formatted_seeds = []
            for seed in selected_seeds:
                s = seed.strip()
                if not s.startswith("```"):
                    s = f"```iec-st\n{s}\n```"
                formatted_seeds.append(s)
                
            seed_context = "\n\n=== VERIFIED EXAMPLE ===\n".join(formatted_seeds)
            if len(seed_context) > 10000:
                seed_context = seed_context[:10000] + "\n...[TRUNCATED FOR LENGTH]...\n```"
        else:
            seed_context = "No seeds available. Relying on base weights."
            
        # Dynamically assemble the Mega-Prompt
        system_prompt = (
            f"You are acting as a {role}. Your objective is to design the control architecture for {system}.\n\n"
            f"Technical Specifications required in the ST code:\n{constraint}\n\n"
            "You must write highly deterministic, production-ready IEC 61131-3 Structured Text (ST).\n\n"
            f"=== REFERENCE KNOWLEDGE ===\n{seed_context}\n\n"
            "=== INSTRUCTION ===\n"
            f"Write a complete FUNCTION_BLOCK named {fb_name}. Include complete VAR declarations, physical I/O mapping, and the operational logic. "
            "Output the code enclosed in a ```iec-st markdown code fence. DO NOT APOLOGIZE. DO NOT EXPLAIN."
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
                        {"role": "user", "content": system_prompt},
                        {"role": "assistant", "content": code}
                    ]
                }
                
                # Strategy A: Write to separate file
                # 4. Save to vault (Strategy A: Temp files)
                import time, uuid
                temp_file = TEMP_DIR / f"gen_{time.time_ns()}_{uuid.uuid4().hex[:6]}.json"
                try:
                    with open(temp_file, "w", encoding="utf-8") as f:
                        json.dump(record, f, ensure_ascii=False)
                except Exception as e:
                    logger.error(f"Failed to write temp file: {e}")
                
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
            if domain and "system" in domain:
                failed_domains.append(domain["system"])
                logger.info(f"Added '{domain['system']}' to failed_domains blacklist for future feedback.")
        
        time.sleep(2) # Cooldown GPU
        
    logger.info(f"Evolution Complete. Successfully synthesized {successful_generations} pristine records.")
    merge_temp_files(TEMP_DIR, OUTPUT_FILE)

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

