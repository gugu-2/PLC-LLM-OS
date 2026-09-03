"""
setup.py
========
Setup script for the local generation pipeline.
Run this FIRST before generate_local.py.

Checks:
  1. Python dependencies (requests, pyyaml)
  2. Ollama installation and server status
  3. Model availability (pulls if missing)
  4. Output directory creation
  5. Training data availability

Usage:
    python pipeline/local_gen/setup.py
"""
import sys
import subprocess
import json
import time
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent

REQUIRED_MODEL   = "qwen2.5-coder:7b-instruct-q4_K_M"
FALLBACK_MODEL   = "qwen2.5-coder:7b-instruct"
OLLAMA_URL       = "http://localhost:11434"
OUTPUT_DIR       = BASE_DIR / "data" / "local_raw"
TRAIN_JSONL      = BASE_DIR / "data" / "master" / "train.jsonl"


def ok(msg):  print(f"  [OK]   {msg}")
def warn(msg): print(f"  [WARN] {msg}")
def err(msg):  print(f"  [ERR]  {msg}")
def info(msg): print(f"  [-->]  {msg}")


def check_python():
    print("Checking Python version...")
    v = sys.version_info
    if v.major < 3 or (v.major == 3 and v.minor < 10):
        err(f"Python 3.10+ required. You have {v.major}.{v.minor}")
        sys.exit(1)
    ok(f"Python {v.major}.{v.minor}.{v.micro}")


def check_dependencies():
    print("\nChecking Python dependencies...")
    missing = []
    for pkg in ["requests", "yaml"]:
        try:
            __import__(pkg)
            ok(f"  {pkg}")
        except ImportError:
            missing.append(pkg)
            warn(f"  {pkg} not found")

    if missing:
        install_names = {"yaml": "pyyaml"}.get
        pkgs = [install_names(p, p) for p in missing]
        info(f"Installing: {' '.join(pkgs)}")
        subprocess.check_call([sys.executable, "-m", "pip", "install"] + pkgs)
        ok("Dependencies installed")


def check_ollama():
    print("\nChecking Ollama installation...")
    try:
        result = subprocess.run(
            ["ollama", "--version"],
            capture_output=True, text=True, timeout=10
        )
        if result.returncode == 0:
            ok(f"Ollama found: {result.stdout.strip()}")
            return True
    except (FileNotFoundError, subprocess.TimeoutExpired):
        pass

    err("Ollama not found or not in PATH.")
    print()
    print("  ============================================================")
    print("  INSTALL OLLAMA:")
    print("  1. Go to: https://ollama.com/download")
    print("  2. Download the Windows installer")
    print("  3. Run it and follow the prompts")
    print("  4. After install, run: ollama serve")
    print("  5. Then re-run this setup script")
    print("  ============================================================")
    return False


def check_ollama_server():
    print("\nChecking Ollama server (localhost:11434)...")
    import requests
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if r.status_code == 200:
            ok("Ollama server is running")
            return True
    except Exception:
        pass

    warn("Ollama server not responding. Trying to start it...")
    try:
        subprocess.Popen(
            ["ollama", "serve"],
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        time.sleep(3)
        import requests
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=5)
        if r.status_code == 200:
            ok("Ollama server started successfully")
            return True
    except Exception as e:
        pass

    err("Could not start Ollama server.")
    info("Please run 'ollama serve' in a separate terminal, then re-run setup.")
    return False


def check_model():
    print(f"\nChecking model: {REQUIRED_MODEL}")
    import requests
    try:
        r = requests.get(f"{OLLAMA_URL}/api/tags", timeout=10)
        if r.status_code == 200:
            models = [m["name"] for m in r.json().get("models", [])]
            if REQUIRED_MODEL in models:
                ok(f"Model already available: {REQUIRED_MODEL}")
                return REQUIRED_MODEL
            # Try fallback
            if FALLBACK_MODEL in models:
                ok(f"Using available fallback: {FALLBACK_MODEL}")
                return FALLBACK_MODEL

            # Pull the model
            info(f"Model not found. Pulling {REQUIRED_MODEL} (~4.5 GB)...")
            info("This may take 5–15 minutes depending on your internet speed.")
            print()
            result = subprocess.run(
                ["ollama", "pull", REQUIRED_MODEL],
                timeout=1800  # 30 min max
            )
            if result.returncode == 0:
                ok(f"Model pulled: {REQUIRED_MODEL}")
                return REQUIRED_MODEL
            else:
                warn(f"Failed to pull {REQUIRED_MODEL}, trying fallback...")
                result2 = subprocess.run(
                    ["ollama", "pull", FALLBACK_MODEL],
                    timeout=1800
                )
                if result2.returncode == 0:
                    ok(f"Fallback model pulled: {FALLBACK_MODEL}")
                    return FALLBACK_MODEL
    except Exception as e:
        err(f"Error checking/pulling model: {e}")

    return None


def check_output_dir():
    print("\nChecking output directory...")
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    ok(f"Output dir ready: {OUTPUT_DIR}")


def check_train_data():
    print("\nChecking training data for few-shot examples...")
    if TRAIN_JSONL.exists():
        size = TRAIN_JSONL.stat().st_size
        ok(f"Found: {TRAIN_JSONL.name} ({size // 1024:,} KB)")
    else:
        warn(f"Training data not found: {TRAIN_JSONL}")
        info("Run 'python pipeline/tools/build_master_dataset.py' first.")
        info("Few-shot examples will be disabled until training data is available.")


def test_generation(model_name: str):
    print(f"\nRunning a quick generation test with {model_name}...")
    import requests

    prompt = (
        "Write a minimal IEC 61131-3 FUNCTION_BLOCK for a simple conveyor belt. "
        "Output ONLY the code in a ```iec-st code fence. Include FUNCTION_BLOCK, "
        "VAR_INPUT, VAR_OUTPUT, END_IF, and END_FUNCTION_BLOCK."
    )

    try:
        r = requests.post(
            f"{OLLAMA_URL}/api/generate",
            json={
                "model": model_name,
                "prompt": prompt,
                "stream": False,
                "options": {"temperature": 0.7, "num_predict": 500},
            },
            timeout=60,
        )
        if r.status_code == 200:
            response_text = r.json().get("response", "")
            if "FUNCTION_BLOCK" in response_text:
                ok("Test generation PASSED — model is responding correctly")
                return True
            else:
                warn(f"Test generation returned unexpected output: {response_text[:100]}...")
        else:
            err(f"HTTP {r.status_code}: {r.text[:200]}")
    except Exception as e:
        err(f"Test generation failed: {e}")

    return False


def main():
    print("=" * 60)
    print("  LUMINA LOCAL GENERATION PIPELINE — SETUP")
    print("=" * 60)
    print()

    check_python()
    check_dependencies()

    if not check_ollama():
        sys.exit(1)

    if not check_ollama_server():
        sys.exit(1)

    model = check_model()
    if not model:
        err("Could not install required model. Exiting.")
        sys.exit(1)

    check_output_dir()
    check_train_data()
    test_generation(model)

    print()
    print("=" * 60)
    print("  SETUP COMPLETE")
    print("=" * 60)
    print(f"  Model     : {model}")
    print(f"  Output dir: {OUTPUT_DIR}")
    print()
    print("  To start generating data, run:")
    print("    python pipeline/local_gen/generate_local.py")
    print()
    print("  Options:")
    print("    --count 50          Generate 50 samples then stop")
    print("    --count 0           Run indefinitely")
    print("    --model <name>      Override the model")
    print("    --no-skip-covered   Include already-covered domains")
    print("=" * 60)


if __name__ == "__main__":
    main()
