# Comprehensive System Fix Plan

This implementation plan addresses the 10 code bugs, 8 architectural flaws, and 5 plan execution gaps identified in the deep analysis documents. We will tackle these systemically across five core components.

## User Review Required

> [!IMPORTANT]  
> **Threshold Adjustment (GAP-002)**: I propose lowering the minimum length threshold back to **1500 characters** across all tools. The 3000-character limit discarded 91.6% of the data (including valid, concise utility blocks). Do you approve this threshold to restore a healthy dataset size?

## Proposed Changes

---

### Component 1: Centralized Configuration & Thresholds
Fixes inconsistencies in quality gates across tools.

#### [MODIFY] `Local_Ollama_Evol_Pipeline/scripts/linter.py`
- Revert minimum length check to 1500 chars (Fixes GAP-002).

#### [MODIFY] `pipeline/tools/repair_dataset.py`
- Align minimum length check to 1500 chars (Fixes BUG-006).

---

### Component 2: Dataset Building & Formatting
Resolves formatting contradictions, metadata loss, and double-wrapping.

#### [MODIFY] `pipeline/tools/build_master_dataset.py`
- **Threshold**: Update `MIN_ASSISTANT_LENGTH` to 1500 (Fixes BUG-003, GAP-002).
- **Prompt Alignment**: Replace contradictory prompt instructions like `"DO NOT OUTPUT MARKDOWN"` with `"Output the code enclosed in a ```iec-st markdown code fence."` (Fixes ARCH-003, GAP-001).
- **System Prompt**: Inject the Lumina AI system persona as the first message in every record (Fixes ARCH-002).
- **Double-Fence Bug**: Strip existing backticks before re-wrapping to prevent double-fences (Fixes BUG-007).
- **Provenance**: Remove `strip_metadata()` at the end so `_source` is preserved in the JSONL for traceability (Fixes ARCH-008).

---

### Component 3: Training Pipeline Integration
Ensures the trainer actually uses the correct, clean data without truncating it.

#### [MODIFY] `lumina/training/train_plc_llm.py`
- **Correct Path**: Point `DATASET_PATH` to `data/master/train.jsonl` (Fixes BUG-001, ARCH-001).
- **Token Truncation**: Increase `MAX_SEQ_LENGTH` from 1024 to 8192 (Fixes BUG-002).
- **ChatML Format**: Update `format_chatml()` to properly encode the new system messages.
- **Ignore Metadata**: Ensure the trainer ignores the `_source` key during tokenization.

---

### Component 4: Local Orchestrator & Generation
Improves stability, context management, and timeout resilience.

#### [MODIFY] `Local_Ollama_Evol_Pipeline/scripts/evol_orchestrator.py`
- **Seed Context Limit**: Cap the injected seed text to 10,000 characters to prevent silent token overflow (Fixes BUG-005).
- **Seed Formatting**: Ensure loaded seeds are wrapped in ````iec-st` so the model learns from consistent examples (Fixes ARCH-004).
- **Exception Handling**: Replace `except: pass` in `load_seeds` with specific `except json.JSONDecodeError:` and log warnings (Fixes BUG-008).
- **Temp Filenames**: Use `time.time_ns()` to prevent timestamp collisions (Fixes BUG-010).

#### [MODIFY] `Local_Ollama_Evol_Pipeline/scripts/ollama_client.py`
- **Timeout**: Increase the API timeout from 120s to 600s to allow complex code generation (Fixes BUG-009).

---

### Component 5: Auditing, Cleanup & Swarm Guidelines
Cleans up the remainder of the workspace and fixes audit logic.

#### [MODIFY] `pipeline/tools/audit_all_datasets.py`
- **Math Logic**: Calculate `pass_rate` based on *parseable* records, not total lines, and compute length stats *after* the refusal filter (Fixes ARCH-006, BUG-004).
- **Tier Relaxation**: Relax the TIER_1 requirement slightly to accommodate valid utility functions, reflecting the 1500-char standard (Fixes GAP-004).

#### [NEW] `archive/` (Move operations)
- Move all 13 leftover scripts in `Local_Ollama_Evol_Pipeline/` and the 2 scripts in `scripts/` to the `archive/` directory (Fixes GAP-005).

#### [NEW] `pipeline/tools/SWARM_GUIDELINES.md`
- Document the mandatory use of `safe_append.py` for any future cloud swarm agent runs (Fixes GAP-003).

## Verification Plan
1. Check `git status` to verify file moves.
2. Run `audit_all_datasets.py` and confirm accurate math.
3. Run `build_master_dataset.py` and verify `train.jsonl` has system prompts, aligned user prompts, and preserves `_source`.
4. Run `python -c` script to confirm 0% truncation risk against `MAX_SEQ_LENGTH=8192`.
