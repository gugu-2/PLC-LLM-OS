"""
local_swarm_generator.py
========================
Offline Local PLC Synthetic Dataset Generator
Uses Ollama + Qwen2.5-Coder:7B (or DeepSeek-Coder-V2:16B)

RTX 4060 (8GB VRAM) benchmarks:
  - qwen2.5-coder:7b  => ~7-10 sec/record  (~400/hr)
  - deepseek-coder-v2:16b-lite-instruct-q3_K_S => ~18-25 sec/record (~170/hr)

Usage:
  python local_pipeline/local_swarm_generator.py
  python local_pipeline/local_swarm_generator.py --model deepseek-coder-v2:16b-lite-instruct-q3_K_S --count 100
"""

import json
import uuid
import time
import random
import logging
import argparse
import re
from pathlib import Path
from datetime import datetime

import requests

# ─────────────────────────────────────────────────────────────
# Setup
# ─────────────────────────────────────────────────────────────
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)
logger = logging.getLogger("LocalSwarm")

BASE_DIR  = Path(__file__).resolve().parent.parent
OUT_DIR   = BASE_DIR / "data" / "local_raw"
OUT_DIR.mkdir(parents=True, exist_ok=True)

OLLAMA_URL  = "http://localhost:11434/api/chat"
OLLAMA_HOST = "http://localhost:11434"

# ─────────────────────────────────────────────────────────────
# 80+ ultra-complex industrial domains (same tier as cloud swarm)
# ─────────────────────────────────────────────────────────────
DOMAINS = [
    ("Offshore Wind Farm Pitch Controller",
     "Collective and individual pitch control with LiDAR feed-forward, extreme load shedding, and blade resonance avoidance"),
    ("Hydrogen PEM Electrolyzer Stack",
     "Multi-stack current density balancing, membrane hydration management, and dynamic power ramp-rate limiting"),
    ("EV Gigafactory Battery Module Assembly",
     "Laser welding seam tracking, cell voltage pre-screening, and module press-fit force profiling"),
    ("Subsea Blowout Preventer (BOP) Control",
     "Hydraulic shear ram closure, deadband annular pressure regulation, and acoustic backup trigger"),
    ("Pharmaceutical Lyophilizer Primary Drying",
     "Shelf temperature multi-zone glycol cascade, Pirani gauge sublimation endpoint, and controlled nucleation"),
    ("Semiconductor RIE Plasma Etch Chamber",
     "RF power impedance auto-matching, endpoint interferometry etch depth, and chlorine mass flow control"),
    ("Aerospace Thrust Vector Control (TVC) Gimbal",
     "EHA asymmetric cylinder equalization, flex-nozzle thermal derating, and high-frequency jitter damping"),
    ("Industrial Direct Air Capture (DAC) Contactor",
     "KOH moisture swing humidity control, CO2-loaded slurry calciner, and fan energy minimization"),
    ("Advanced Continuous Casting Tundish",
     "Stopper rod auto-gauging, electromagnetic stirring frequency sweep, and breakout detection thermometry"),
    ("Cryogenic LNG Cascade Liquefaction Train",
     "Mixed refrigerant compressor surge prevention, expander sub-cooling Joule-Thomson letdown, BOG reliquefaction"),
    ("Autonomous Mining Haul Truck Retarder",
     "Regenerative braking energy recovery, payload-adaptive descent speed, and tire thermal overload protection"),
    ("Advanced Solid Oxide Fuel Cell (SOFC) Stack",
     "800C ceramic electrolyte gradient minimization, reformer methane mass flow, and tail-gas combustor"),
    ("Industrial Carbon Fiber Oxidation Oven",
     "Exothermic cross-linking thermal runaway prevention, tension-controlled tow stretching, and VOC incineration"),
    ("Advanced Geothermal Binary Cycle (ORC)",
     "Isobutane supercritical flashing, downhole hydraulic fracture pressure mapping, NCG reinjection"),
    ("Semiconductor HDP-CVD Chamber",
     "ECR microwave impedance matching, multi-zone ESC helium backside cooling, SiH4/O2 stoichiometry"),
    ("Biopharmaceutical mAb Protein A Chromatography",
     "UV breakthrough peak detection, gradient elution buffer blending, and SMB column switching"),
    ("Offshore FPSO Water Injection Pump",
     "Centrifugal pump variable speed anti-surge, seawater filtration backwash, and subsea tree pressure balance"),
    ("Airborne Wind Energy (AWE) Kite Tether",
     "Winch torque control figure-eight crosswind trajectory, tether tension limiting, and emergency descent"),
    ("Advanced Maglev (EMS) Gap Control",
     "Multi-magnet active electromagnetic levitation at 10mm gap, guideway joint impact, and coil fault isolation"),
    ("PEM Fuel Cell Vehicle Drive Inverter",
     "Three-phase SVPWM current vector control, hydrogen crossover detection, and cold-start membrane hydration"),
    ("Industrial Scale Vertical Farm LED Lighting",
     "Multi-spectral PPFD canopy uniformity, circadian rhythm DLI scheduling, and power factor correction"),
    ("Subsea Pipeline Pigging Operations",
     "Bidirectional pig trap pressure equalization, launcher receiver interlock sequence, and debris detector"),
    ("Aerospace Environmental Control System (ECS)",
     "Bleed air temperature mixing valve, cabin altitude pressurization schedule, and recirculation filter delta-P"),
    ("Ultra-High Vacuum Ion Beam Sputter Deposition",
     "Glow discharge plasma ignition, target erosion uniformity rotation, and quartz crystal microbalance rate control"),
    ("Industrial Explosive Forming (EXF) Chamber",
     "Detonator firing sequence interlock, standoff distance servo, and shock wave pressure impulse monitoring"),
    ("Advanced Laser Powder Bed Fusion (L-PBF) Printer",
     "Galvanometer dual-laser melt pool pyrometry, argon crossflow spatter removal, recoater anomaly detection"),
    ("Continuous Pharmaceutical Hot Melt Extrusion",
     "API super-saturation dispersion, twin-screw torque ripple compensation, and melt pressure feed-forward"),
    ("Offshore Floating Storage & Regasification Unit (FSRU)",
     "Submerged combustion vaporizer (SCV) water bath control, send-out pressure letdown, and BOG management"),
    ("High-Power Industrial Ultrasonic Welding Press",
     "Amplitude modulation through resonance crossing, energy-to-depth weld collapse control, and stack bond health"),
    ("Next-Gen Autonomous Port Container Crane",
     "Anti-sway predictive trajectory generation, load cell dynamic compensation, and spreader twist-lock sensing"),
]

SYSTEM_PROMPT = """You are Lumina AI, an expert IEC 61131-3 automation engineer with 40+ years of experience.
Generate extremely complex, mathematically rigorous Structured Text that includes:
- Multi-layered PID with anti-windup, setpoint ramping, and derivative filtering
- Full state-machine with at minimum 5 states including fault and safe states
- Sensor noise filtering (exponential moving average or Kalman)
- Multi-channel safety interlocks with voted redundancy
- Realistic engineering units, comments, and variable naming"""

# ─────────────────────────────────────────────────────────────
# Validation (same rules as build_master_dataset.py)
# ─────────────────────────────────────────────────────────────
FB_PATTERN         = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
END_FB_PATTERN     = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
LOGIC_PATTERN      = re.compile(r'\bEND_IF\b|\bEND_CASE\b', re.IGNORECASE)
VAR_INPUT_PATTERN  = re.compile(r'\bVAR_INPUT\b', re.IGNORECASE)
VAR_OUTPUT_PATTERN = re.compile(r'\bVAR_OUTPUT\b', re.IGNORECASE)
REFUSAL_PHRASES    = ["cannot provide", "cannot fulfill", "must decline", "i cannot"]

def validate(content: str) -> tuple[bool, str]:
    """Return (is_valid, reason). Enforce all 5 IEC 61131-3 structural rules."""
    if len(content) < 1500:
        return False, f"Too short ({len(content)} chars, need 1500+)"
    if any(p in content.lower() for p in REFUSAL_PHRASES):
        return False, "Contains refusal phrase"
    fb_count = len(FB_PATTERN.findall(content))
    if fb_count == 0:
        return False, "Missing FUNCTION_BLOCK"
    if fb_count > 1:
        return False, "Double FUNCTION_BLOCK bug"
    if not END_FB_PATTERN.search(content):
        return False, "Missing END_FUNCTION_BLOCK"
    if not VAR_INPUT_PATTERN.search(content):
        return False, "Missing VAR_INPUT"
    if not VAR_OUTPUT_PATTERN.search(content):
        return False, "Missing VAR_OUTPUT"
    if not LOGIC_PATTERN.search(content):
        return False, "Missing END_IF/END_CASE"
    return True, "OK"


# ─────────────────────────────────────────────────────────────
# Ollama Client
# ─────────────────────────────────────────────────────────────
def check_ollama() -> bool:
    try:
        r = requests.get(OLLAMA_HOST, timeout=3)
        return r.status_code == 200
    except Exception:
        return False


def generate(model: str, domain: str, scenario: str, temperature: float = 0.75) -> str:
    user_prompt = f"""Generate a complete, ultra-complex IEC 61131-3 Structured Text FUNCTION_BLOCK for:

**Domain:** {domain}
**Scenario details:** {scenario}

STRICT REQUIREMENTS:
1. Start with: FUNCTION_BLOCK FB_{domain.replace(' ', '_').replace('(', '').replace(')', '').replace('-', '_')[:30]}
2. VAR_INPUT section with minimum 6 typed inputs with inline comments
3. VAR_OUTPUT section with minimum 4 typed outputs with inline comments
4. VAR section with local variables (PIDs, timers, state machine)
5. Full implementation body with:
   - State machine (CASE statement with minimum 5 states: INIT, IDLE, RUNNING, FAULT, SAFE_SHUTDOWN)
   - PID control loops with anti-windup and derivative filtering
   - Exponential moving average sensor noise filter
   - Safety interlock chain (2oo3 vote or dual-redundant)
   - Engineering unit comments throughout
6. End with: END_FUNCTION_BLOCK
7. Enclose ALL code in a ```iec-st code fence
8. Minimum 1500 characters total

Write the most elite, realistic, production-grade IEC 61131-3 code possible."""

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user",   "content": user_prompt},
    ]
    payload = {
        "model": model,
        "messages": messages,
        "stream": False,
        "options": {
            "num_ctx":      16384,
            "num_predict":  4096,
            "temperature":  temperature,
            "top_p":        0.92,
            "repeat_penalty": 1.05,
        }
    }

    try:
        resp = requests.post(OLLAMA_URL, json=payload, timeout=300)
        resp.raise_for_status()
        return resp.json().get("message", {}).get("content", "")
    except requests.Timeout:
        logger.error("Ollama timed out (>5 min). GPU may be overloaded.")
        return ""
    except Exception as e:
        logger.error(f"Ollama error: {e}")
        return ""


# ─────────────────────────────────────────────────────────────
# Save
# ─────────────────────────────────────────────────────────────
def save_record(user_prompt: str, assistant_content: str) -> Path:
    record = {
        "messages": [
            {"role": "system",    "content": SYSTEM_PROMPT},
            {"role": "user",      "content": user_prompt},
            {"role": "assistant", "content": assistant_content},
        ]
    }
    out_path = OUT_DIR / f"agent_{uuid.uuid4().hex[:8]}.json"
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
    return out_path


# ─────────────────────────────────────────────────────────────
# Main Loop
# ─────────────────────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="Local Offline PLC Dataset Generator")
    parser.add_argument("--model", default="qwen2.5-coder:7b",
                        help="Ollama model name (default: qwen2.5-coder:7b)")
    parser.add_argument("--count", type=int, default=0,
                        help="Number of records to generate (0 = run forever)")
    parser.add_argument("--temperature", type=float, default=0.75,
                        help="LLM temperature (default: 0.75)")
    args = parser.parse_args()

    logger.info("=" * 60)
    logger.info("  Lumina AI LOCAL SWARM GENERATOR")
    logger.info(f"  Model    : {args.model}")
    logger.info(f"  Output   : {OUT_DIR}")
    logger.info(f"  Target   : {'Infinite' if args.count == 0 else args.count} records")
    logger.info("=" * 60)

    # Check Ollama is running
    if not check_ollama():
        logger.error("❌ Ollama is not running! Start it with: ollama serve")
        logger.error("   Then pull model: ollama pull " + args.model)
        return

    logger.info(f"✅ Ollama detected. Starting generation...")

    generated = 0
    skipped   = 0
    domain_pool = DOMAINS.copy()
    random.shuffle(domain_pool)
    domain_idx = 0

    while args.count == 0 or generated < args.count:
        # Cycle through domains
        domain, scenario = domain_pool[domain_idx % len(domain_pool)]
        domain_idx += 1

        logger.info(f"\n[{generated+1}] Generating: {domain}")
        t_start = time.time()

        content = generate(args.model, domain, scenario, args.temperature)
        elapsed = time.time() - t_start

        if not content:
            skipped += 1
            logger.warning(f"  ⚠️  Empty response. Skipping.")
            time.sleep(2)
            continue

        valid, reason = validate(content)
        if not valid:
            skipped += 1
            logger.warning(f"  ⚠️  Invalid ({reason}). Skipping.")
            continue

        user_prompt = f"Generate a complex IEC 61131-3 FUNCTION_BLOCK for: {domain}. {scenario}"
        out_path = save_record(user_prompt, content)
        generated += 1

        speed = len(content.split()) / elapsed if elapsed > 0 else 0
        logger.info(f"  ✅ Saved: {out_path.name} | {len(content):,} chars | {elapsed:.1f}s | {speed:.0f} w/s")
        logger.info(f"  📊 Progress: {generated} generated, {skipped} skipped")

        # Small rest between generations to prevent GPU thermal throttle
        time.sleep(0.5)

    logger.info("\n" + "=" * 60)
    logger.info(f"  DONE: {generated} records saved to {OUT_DIR}")
    logger.info(f"  Run build_master_dataset.py to merge into train.jsonl")
    logger.info("=" * 60)


if __name__ == "__main__":
    main()
