# ==============================================================================
# Lumina PLC-LLM Swarm Setup Script for Windows PowerShell
# ==============================================================================

Write-Host "============================================================" -ForegroundColor Cyan
Write-Host "🚀 SETTING UP LUMINA PLC-LLM SWARM ON NEW COMPUTER" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan

# 1. Verify Python
$pythonCmd = Get-Command python -ErrorAction SilentlyContinue
if (-not $pythonCmd) {
    Write-Host "❌ Python was not found on PATH. Please install Python 3.10+ and re-run." -ForegroundColor Red
    Exit 1
}

$pyVersion = python --version
Write-Host "✔ Found Python: $pyVersion" -ForegroundColor Green

# 2. Setup Virtual Environment
if (-not (Test-Path ".venv")) {
    Write-Host "Creating Python virtual environment (.venv)..." -ForegroundColor Yellow
    python -m venv .venv
}

Write-Host "Activating virtual environment..." -ForegroundColor Yellow
& ".\.venv\Scripts\Activate.ps1"

# 3. Upgrade pip and install requirements
Write-Host "Installing requirements..." -ForegroundColor Yellow
python -m pip install --upgrade pip
if (Test-Path "requirements.txt") {
    pip install -r requirements.txt
}

# 4. Ensure Directory Structures Exist
$dirs = @("data\swarm_raw", "data\logs", "scripts", "scratch")
foreach ($d in $dirs) {
    if (-not (Test-Path $d)) {
        New-Item -ItemType Directory -Path $d -Force | Out-Null
        Write-Host "Created directory: $d" -ForegroundColor Gray
    }
}

# 5. Check Git Remote
Write-Host "`nGit Status & Remote:" -ForegroundColor Yellow
git status --short
git remote -v

# 6. Verify existing dataset count
$rawCount = (Get-ChildItem -Path "data\swarm_raw\*.json" -ErrorAction SilentlyContinue).Count
Write-Host "`n✔ Total Raw Datasets in data\swarm_raw: $rawCount" -ForegroundColor Green

Write-Host "`n============================================================" -ForegroundColor Cyan
Write-Host "✔ SETUP COMPLETE! Workspace is ready for AI Swarm generation." -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Cyan
