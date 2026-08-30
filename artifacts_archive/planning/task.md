# System Fix Execution Tasks

## Phase 1: Cleanup & Thresholds
- [x] Move 13 scripts from `Local_Ollama_Evol_Pipeline/` to `archive/`
- [x] Move 2 scripts from `scripts/` to `archive/`
- [x] Update `linter.py` threshold to 1500
- [x] Update `repair_dataset.py` threshold to 1500
- [x] Update `audit_all_datasets.py` pass rate math and stats logic

## Phase 2: Dataset Builder Overhaul
- [x] Update `build_master_dataset.py`:
  - Threshold to 1500
  - Strip existing fences before re-wrapping (Double-fence fix)
  - Align user prompts to ask for markdown
  - Inject Lumina AI System Prompt
  - Preserve `_source` metadata (Remove `strip_metadata` step)
- [x] Run `repair_dataset.py`, `audit_all_datasets.py`, and `build_master_dataset.py`

## Phase 3: Training Pipeline Integration
- [x] Update `train_plc_llm.py`:
  - Fix `DATASET_PATH` to `data/master/train.jsonl`
  - Increase `MAX_SEQ_LENGTH` to 8192
  - Add system role handling to `format_chatml`

## Phase 4: Local Pipeline Stability
- [x] Update `evol_orchestrator.py`:
  - Enforce 10,000 char seed context limit
  - Ensure loaded seeds have fences
  - Catch explicit `json.JSONDecodeError`
  - Use `time.time_ns()` for temp filenames
- [x] Update `ollama_client.py` timeout to 600s
- [x] Create `pipeline/tools/SWARM_GUIDELINES.md`
