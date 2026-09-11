# Local Offline PLC Dataset Generator
## For NVIDIA RTX 4060 (8GB VRAM)

## RECOMMENDED MODEL: qwen2.5-coder:7b

### Speed on your RTX 4060:
- Qwen2.5-Coder:7B Q4_K_M  --> ~7-10 seconds per record  (~400 records/hour)
- DeepSeek-Coder-V2:16B Q3  --> ~18-25 seconds per record (~170 records/hour)

### Quality vs Cloud:
- Qwen2.5-Coder:7B = ~60-70% of Gemini Pro quality
- DeepSeek:16B Q3  = ~70-75% of Gemini Pro quality

### Setup:
1. winget install Ollama.Ollama
2. ollama pull qwen2.5-coder:7b
3. python local_pipeline/local_swarm_generator.py --model qwen2.5-coder:7b
