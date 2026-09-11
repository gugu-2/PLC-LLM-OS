# setup_local.ps1
# Run this script ONCE to set up the local offline PLC generator
# Usage: .\local_pipeline\setup_local.ps1

Write-Host ""
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host "  Lumina AI - Local Offline Generator Setup" -ForegroundColor Cyan
Write-Host "  NVIDIA RTX 4060 (8GB VRAM)" -ForegroundColor Cyan
Write-Host "======================================================" -ForegroundColor Cyan
Write-Host ""

# Step 1: Check if Ollama is installed
Write-Host "[1/4] Checking Ollama installation..." -ForegroundColor Yellow
$ollamaPath = Get-Command ollama -ErrorAction SilentlyContinue
if (-not $ollamaPath) {
    Write-Host "  Ollama not found. Installing..." -ForegroundColor Red
    Write-Host "  Please download from: https://ollama.com/download/windows" -ForegroundColor White
    Write-Host "  OR run: winget install Ollama.Ollama" -ForegroundColor White
    Start-Process "https://ollama.com/download/windows"
    exit 1
} else {
    Write-Host "  ✅ Ollama found: $($ollamaPath.Source)" -ForegroundColor Green
}

# Step 2: Start Ollama server
Write-Host ""
Write-Host "[2/4] Starting Ollama server..." -ForegroundColor Yellow
Start-Process -FilePath "ollama" -ArgumentList "serve" -WindowStyle Hidden
Start-Sleep 3
Write-Host "  ✅ Ollama server started in background" -ForegroundColor Green

# Step 3: Pull recommended model
Write-Host ""
Write-Host "[3/4] Pulling Qwen2.5-Coder:7B (recommended model)..." -ForegroundColor Yellow
Write-Host "  This will download ~4.5 GB. Please wait..." -ForegroundColor White
ollama pull qwen2.5-coder:7b
Write-Host "  ✅ Model ready!" -ForegroundColor Green

# Step 4: Install Python dependencies
Write-Host ""
Write-Host "[4/4] Installing Python dependencies..." -ForegroundColor Yellow
pip install requests tqdm --quiet
Write-Host "  ✅ Dependencies installed!" -ForegroundColor Green

Write-Host ""
Write-Host "======================================================" -ForegroundColor Green
Write-Host "  SETUP COMPLETE! Your system is ready." -ForegroundColor Green
Write-Host "======================================================" -ForegroundColor Green
Write-Host ""
Write-Host "  Start generating with:" -ForegroundColor White
Write-Host "  python local_pipeline\local_swarm_generator.py" -ForegroundColor Cyan
Write-Host ""
Write-Host "  For DeepSeek-V2 (higher quality, slower):" -ForegroundColor White
Write-Host "  ollama pull deepseek-coder-v2:16b-lite-instruct-q3_K_S" -ForegroundColor Cyan
Write-Host "  python local_pipeline\local_swarm_generator.py --model deepseek-coder-v2:16b-lite-instruct-q3_K_S" -ForegroundColor Cyan
Write-Host ""
Write-Host "  Speed estimates (RTX 4060):" -ForegroundColor White
Write-Host "    Qwen2.5-Coder:7B  -> 7-10 sec/record  (~400 records/hour)" -ForegroundColor Yellow
Write-Host "    DeepSeek-V2:16B   -> 18-25 sec/record (~170 records/hour)" -ForegroundColor Yellow
Write-Host ""
