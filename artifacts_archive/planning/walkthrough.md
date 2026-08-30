# System Refactor Walkthrough

I have executed a comprehensive refactoring of the entire dataset and training pipeline, resolving 23 systemic issues (10 bugs, 8 architectural flaws, and 5 plan execution gaps).

## 1. Quality Thresholds & Dataset Resurgence
- **The Problem**: The previous 3000-character constraint was excessively strict, filtering out 91.6% of valid IEC 61131-3 logic (utility blocks, timers, converters).
- **The Fix**: Standardized the minimum length threshold to **1500 characters** across `linter.py`, `repair_dataset.py`, and `build_master_dataset.py`.
- **The Result**: The master training dataset rebounded from **545 records** up to **1,619 high-quality unique records**. 

## 2. Training Pipeline Stability
- **The Problem**: `train_plc_llm.py` was pointing directly to the old, unverified `data/final_verified_dataset.jsonl` instead of the clean master dataset, and applying a catastrophic `MAX_SEQ_LENGTH` of 1024, silently truncating 91% of our codebase.
- **The Fix**: 
  - Redirected `train_plc_llm.py` to `data/master/train.jsonl`.
  - Raised `MAX_SEQ_LENGTH` to **8192 tokens**.
  - Updated `format_chatml` to support the `system` role so the model actually learns the Lumina AI persona.

## 3. The Dataset Formatting & Prompts Overhaul
- **The Problem**: 247 user prompts told the model `"DO NOT OUTPUT MARKDOWN"`, but the expected answer had an `iec-st` markdown fence. We were actively teaching the model to ignore formatting rules.
- **The Fix**: 
  - `build_master_dataset.py` now dynamically replaces `"DO NOT OUTPUT MARKDOWN"` with `"Output the code enclosed in a ```iec-st markdown code fence."`
  - Fixed the double-fence wrapping bug where records would become ```` ```iec-st\n```iec-st ````.
  - Stopped stripping the `_source` metadata, restoring full audit traceability to the final JSONL files.

## 4. Local Evol Pipeline Hardening
- **The Problem**: The `evol_orchestrator.py` was brittle. Context lengths exploded past 32K tokens, timeouts crashed long generations, and temp file timestamps collided.
- **The Fix**: 
  - Enforced a hard 10,000-character limit on the RAG seed context.
  - Formatted loaded seeds with `iec-st` fences to provide consistent examples to the model.
  - Increased `ollama_client.py` timeout to **600 seconds**.
  - Switched temp filename generation to `time.time_ns()` combined with `uuid` hex strings to guarantee zero collisions.

## 5. Housekeeping
- Created `pipeline/tools/SWARM_GUIDELINES.md` to prevent future agents from introducing JSON corruption.
- Archived the 15 remaining throwaway scripts scattered across `Local_Ollama_Evol_Pipeline/` and `scripts/`.
- Repaired the `audit_all_datasets.py` pass rate math so that refusals and empty lines are handled correctly.
