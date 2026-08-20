# Local Ollama Evol Pipeline (RTX 5050 Edition)

This is the complete, self-contained pipeline designed to run on your laptop with the RTX 5050 (8GB VRAM). It takes raw PLC data and uses a local LLM to "evolve" it into a highly-refined synthetic dataset without any API costs.

## Prerequisites (On your Laptop)
1. Install [Ollama](https://ollama.com/)
2. Open terminal and run: ollama run qwen2.5-coder:7b (This will download the 7B coding model)
3. Ensure Python is installed.

## Folder Structure
*   seeds/final_verified_dataset.jsonl -> Your 5,928 flawless human records (we just updated this to the max size!).
*   scripts/ollama_client.py -> The script that talks to localhost:11434.
*   scripts/linter.py -> The mathematical syntax checker.
*   scripts/evol_orchestrator.py -> The main AI self-play loop.
*   generated_vault/ -> Where your new, evolved golden records are saved.

## How to Run It
Simply copy this entire Local_Ollama_Evol_Pipeline folder to your laptop, open a terminal inside the folder, and run:

`ash
python scripts/evol_orchestrator.py
`

## How It Works
1.  **Seed Selection:** The orchestrator randomly picks 2-3 code blocks from the seeds/ folder.
2.  **Evolution:** It asks the local Qwen model to analyze the human code, make it 10x better, add perfect comments, and add error handling.
3.  **Linting:** The AI-generated code is mathematically checked. If it fails, the AI is scolded and told to fix it (Reflection).
4.  **Vault:** If it passes, it is permanently saved in the generated_vault.
