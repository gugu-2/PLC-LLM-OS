#!/usr/bin/env bash
# ==============================================================================
# Lumina PLC-LLM Swarm Setup Script for Linux / macOS
# ==============================================================================

set -e

echo "============================================================"
echo "🚀 SETTING UP LUMINA PLC-LLM SWARM ON NEW COMPUTER"
echo "============================================================"

# 1. Verify Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 was not found. Please install Python 3.10+ and re-run."
    exit 1
fi

echo "✔ Found Python: $(python3 --version)"

# 2. Setup Virtual Environment (Self-Healing if copied from another PC via USB)
need_recreate=false
if [ -d ".venv" ]; then
    test_prefix=$(.venv/bin/python3 -c "import sys; print(sys.prefix)" 2>/dev/null || true)
    expected_prefix="$(pwd)/.venv"
    if [ "$test_prefix" != "$expected_prefix" ]; then
        echo "⚠️ Detected .venv copied from another computer/path. Rebuilding for this PC..."
        need_recreate=true
    fi
else
    need_recreate=true
fi

if [ "$need_recreate" = true ]; then
    rm -rf .venv
    echo "Creating fresh Python virtual environment (.venv)..."
    python3 -m venv .venv
fi

echo "Activating virtual environment..."
source .venv/bin/activate

# 3. Install requirements
echo "Installing requirements..."
pip install --upgrade pip
if [ -f "requirements.txt" ]; then
    pip install -r requirements.txt
fi

# 4. Ensure Directories
mkdir -p data/swarm_raw data/logs scripts scratch

# 5. Dataset count
raw_count=$(ls -1 data/swarm_raw/*.json 2>/dev/null | wc -l || echo 0)
echo "✔ Total Raw Datasets in data/swarm_raw: $raw_count"

echo "============================================================"
echo "✔ SETUP COMPLETE! Workspace is ready for AI Swarm generation."
echo "============================================================"
