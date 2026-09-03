"""
generate_local.py
=================
Main local generation loop for the Lumina PLC-LLM dataset.
Uses Qwen2.5-Coder-7B via Ollama to generate IEC 61131-3 training samples
with few-shot prompting from your existing high-quality dataset.

Usage:
    python pipeline/local_gen/generate_local.py
    python pipeline/local_gen/generate_local.py --count 50
    python pipeline/local_gen/generate_local.py --count 0       # unlimited
    python pipeline/local_gen/generate_local.py --model qwen2.5-coder:7b-instruct
    python pipeline/local_gen/generate_local.py --no-skip-covered

Requirements:
    pip install requests pyyaml
    Ollama running with qwen2.5-coder:7b-instruct-q4_K_M pulled
"""

import sys
import json
import time
import uuid
import random
import argparse
import logging
from datetime import datetime
from pathlib import Path

import requests
import yaml

# ── Path setup ────────────────────────────────────────────────────────────────
BASE_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(BASE_DIR / "pipeline" / "local_gen"))

from validator     import validate, summary_line
from repairer      import repair
from few_shot_picker import FewShotPicker
from domain_list   import get_domains

# ── Logging ───────────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
    ],
)
logger = logging.getLogger("LocalGen")

CONFIG_PATH = Path(__file__).parent / "config.yaml"


def load_config() -> dict:
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


# ── Prompt builder ────────────────────────────────────────────────────────────
SYSTEM_PROMPT = (
    "You are Lumina AI, an elite industrial automation and IEC 61131-3 controls engineer. "
    "You generate deterministic, mathematically verifiable Structured Text (ST) FUNCTION_BLOCKs "
    "for industrial control systems. Your code is always complete, compilable, and follows "
    "strict IEC 61131-3 syntax."
)

GENERATION_TEMPLATE = """\
You are part of the Lumina AI training data generation pipeline.

Your assigned industrial domain is: {domain}

Task: Write a complete, highly complex, deterministic IEC 61131-3 Structured Text
FUNCTION_BLOCK for this domain. Include realistic industrial physics, safety interlocks,
and state machine logic.

{few_shot_block}

MANDATORY REQUIREMENTS (ALL must be satisfied):
1. Wrap code in TRIPLE-backtick iec-st fence:
   ```iec-st
   (your code here)
   ```
2. First line of code: FUNCTION_BLOCK FB_<DescriptiveName>
3. Include VAR_INPUT section with >= 4 typed inputs (with engineering unit comments)
4. Include VAR_OUTPUT section with >= 3 typed outputs
5. Include at least one END_IF; or END_CASE; (control logic)
6. Last line of code: END_FUNCTION_BLOCK
7. Minimum 1500 characters total

STYLE GUIDE:
- Use REAL industrial parameter values (pressures in kPa/bar, temps in degC, flows in m3/h)
- Add inline comments explaining the physics/engineering rationale
- Include an E-Stop/safety interlock block using RETURN
- Use TON or TOF timers where appropriate
- Implement a CASE state machine OR complex IF/ELSIF ladder

DO NOT apologize. DO NOT explain. Output ONLY the ```iec-st code fence with the complete code.
"""


def build_prompt(domain: str, few_shot_picker: FewShotPicker) -> tuple[str, str]:
    """
    Build the user prompt and system message for a given domain.
    Returns (system_prompt, user_prompt).
    """
    few_shot_block = few_shot_picker.format_few_shot_block(domain)
    user_prompt    = GENERATION_TEMPLATE.format(
        domain=domain,
        few_shot_block=few_shot_block,
    )
    return SYSTEM_PROMPT, user_prompt


# ── Ollama API call ───────────────────────────────────────────────────────────
def generate(
    system_prompt: str,
    user_prompt: str,
    model: str,
    ollama_url: str,
    cfg: dict,
) -> str | None:
    """
    Call the Ollama API and return the generated text, or None on failure.
    """
    payload = {
        "model": model,
        "system": system_prompt,
        "prompt": user_prompt,
        "stream": False,
        "options": {
            "temperature": cfg.get("temperature", 0.7),
            "top_p":       cfg.get("top_p", 0.9),
            "num_predict": cfg.get("max_tokens", 2048),
            "num_ctx":     cfg.get("num_ctx", 4096),
        },
    }

    try:
        r = requests.post(
            f"{ollama_url}/api/generate",
            json=payload,
            timeout=cfg.get("ollama_timeout", 120),
        )
        if r.status_code == 200:
            return r.json().get("response", "").strip()
        else:
            logger.warning(f"Ollama returned HTTP {r.status_code}: {r.text[:200]}")
    except requests.exceptions.Timeout:
        logger.warning("Ollama request timed out")
    except requests.exceptions.ConnectionError:
        logger.error("Cannot connect to Ollama. Is 'ollama serve' running?")
    except Exception as e:
        logger.warning(f"Ollama error: {e}")

    return None


# ── Save record ───────────────────────────────────────────────────────────────
def save_record(user_prompt: str, assistant_content: str, output_dir: Path) -> Path:
    """Save a validated record as an isolated JSON file."""
    record = {
        "messages": [
            {"role": "user",      "content": user_prompt},
            {"role": "assistant", "content": assistant_content},
        ]
    }
    filename = output_dir / f"local_{uuid.uuid4().hex[:8]}.json"
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return filename


# ── Progress display ──────────────────────────────────────────────────────────
def print_header(model: str, output_dir: Path):
    print()
    print("=" * 68)
    print("  LUMINA LOCAL SYNTHETIC DATA GENERATION")
    print("=" * 68)
    print(f"  Model      : {model}")
    print(f"  Output     : {output_dir}")
    print(f"  Started    : {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("  Press Ctrl+C to stop gracefully.")
    print("=" * 68)
    print()


def print_stats(generated: int, passed: int, repaired: int, skipped: int, t_start: float):
    elapsed = time.time() - t_start
    rate    = generated / (elapsed / 3600) if elapsed > 0 else 0
    pct     = 100 * passed / generated if generated > 0 else 0
    print()
    print(f"  -- Stats -- Generated: {generated}  Passed: {passed} ({pct:.0f}%)"
          f"  Repaired: {repaired}  Skipped: {skipped}"
          f"  Rate: {rate:.0f}/hr  Elapsed: {elapsed/60:.1f}m")
    print()


# ── Main loop ─────────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Lumina Local Data Generator")
    parser.add_argument("--count",          type=int,  default=100,
                        help="Number of samples to generate (0 = unlimited)")
    parser.add_argument("--model",          type=str,  default=None,
                        help="Override the Ollama model name")
    parser.add_argument("--no-skip-covered", action="store_true",
                        help="Include domains already in the corpus")
    parser.add_argument("--temp",           type=float, default=None,
                        help="Override generation temperature")
    args = parser.parse_args()

    # ── Load config ──────────────────────────────────────────────────────────
    cfg        = load_config()
    model      = args.model or cfg["model"]
    ollama_url = cfg["ollama_url"]
    output_dir = BASE_DIR / cfg["output_dir"]
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.temp:
        cfg["temperature"] = args.temp
    if args.count != 100:
        cfg["max_per_run"] = args.count

    max_count   = cfg.get("max_per_run", 100)  # 0 = unlimited
    delay_sec   = cfg.get("delay_between", 1.0)
    max_repairs = cfg.get("max_repair_attempts", 2)

    # ── Load few-shot picker ─────────────────────────────────────────────────
    train_path = BASE_DIR / cfg["train_data"]
    picker     = FewShotPicker(train_path, n_shots=cfg.get("few_shot_count", 3))

    # ── Domain list ──────────────────────────────────────────────────────────
    domains = get_domains(skip_covered=not args.no_skip_covered)
    random.shuffle(domains)
    logger.info(f"Loaded {len(domains)} domains (skip_covered={not args.no_skip_covered})")

    print_header(model, output_dir)

    # ── Counters ─────────────────────────────────────────────────────────────
    generated = 0
    passed    = 0
    repaired  = 0
    skipped   = 0
    t_start   = time.time()

    domain_cycle = iter(domains * 100)  # repeat list to allow unlimited runs

    try:
        while True:
            if max_count > 0 and generated >= max_count:
                break

            # Pick next domain
            try:
                domain = next(domain_cycle)
            except StopIteration:
                logger.info("All domains exhausted. Shuffling and repeating...")
                random.shuffle(domains)
                domain_cycle = iter(domains * 100)
                domain = next(domain_cycle)

            # Build prompt
            sys_prompt, usr_prompt = build_prompt(domain, picker)

            logger.info(f"[{generated+1:04d}] Domain: {domain[:55]}")

            # ── Generate ─────────────────────────────────────────────────────
            raw_output = generate(sys_prompt, usr_prompt, model, ollama_url, cfg)

            if raw_output is None:
                logger.warning("  --> Generation failed, skipping")
                skipped += 1
                time.sleep(delay_sec * 2)
                continue

            # ── Validate ─────────────────────────────────────────────────────
            score, errors, warnings = validate(raw_output)
            content = raw_output

            if errors:
                # Try auto-repair
                for attempt in range(1, max_repairs + 1):
                    fixed, fixes = repair(content, fb_name_hint=f"FB_{domain.replace(' ', '_')[:30]}")
                    score2, errors2, warnings2 = validate(fixed)
                    if not errors2:
                        content  = fixed
                        score    = score2
                        errors   = errors2
                        warnings = warnings2
                        repaired += 1
                        logger.info(f"  --> Repaired ({len(fixes)} fixes applied) -> score={score2}")
                        break
                else:
                    logger.warning(f"  --> Could not fix: {errors} | Skipping")
                    skipped += 1
                    continue

            # ── Save ─────────────────────────────────────────────────────────
            saved_path = save_record(usr_prompt, content, output_dir)
            generated += 1
            passed    += 1
            logger.info(f"  --> {summary_line(score, errors, warnings)} | Saved: {saved_path.name}")

            # ── Stats every 10 ───────────────────────────────────────────────
            if generated % 10 == 0:
                print_stats(generated, passed, repaired, skipped, t_start)

            time.sleep(delay_sec)

    except KeyboardInterrupt:
        print("\n\n  [Ctrl+C] Stopping gracefully...")

    # ── Final summary ─────────────────────────────────────────────────────────
    elapsed  = time.time() - t_start
    rate     = generated / (elapsed / 3600) if elapsed > 0 else 0
    pct      = 100 * passed / max(generated, 1)

    print()
    print("=" * 68)
    print("  GENERATION COMPLETE")
    print("=" * 68)
    print(f"  Samples generated : {generated}")
    print(f"  Pass rate         : {passed}/{generated} ({pct:.1f}%)")
    print(f"  Auto-repaired     : {repaired}")
    print(f"  Skipped (failed)  : {skipped}")
    print(f"  Time elapsed      : {elapsed/60:.1f} minutes")
    print(f"  Rate              : {rate:.0f} samples/hour")
    print(f"  Output dir        : {output_dir}")
    print()
    print("  Next steps:")
    print("  1. python pipeline/tools/build_master_dataset.py  (rebuild dataset)")
    print("  2. python pipeline/tools/audit_all_datasets.py    (verify quality)")
    print("=" * 68)


if __name__ == "__main__":
    main()
