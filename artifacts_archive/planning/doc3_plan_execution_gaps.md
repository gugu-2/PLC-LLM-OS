# Plan Execution Gaps — Where Plans Went Differently

> This document is an honest post-mortem of cases where the original intent of a plan was sound, but execution produced a different — sometimes worse — outcome. These are not bugs or architectural flaws in isolation. They are **process failures**: situations where the plan was right but the implementation drifted, was incomplete, or produced unintended side effects. Each entry is written so that a developer can understand what was supposed to happen, what actually happened, and why.

---

## Summary Table

| ID | Title | Drift Type | Impact |
|----|-------|-----------|--------|
| [GAP-001](#gap-001) | Format normalization plan introduced a new prompt/response mismatch | Half-done fix | Model learns to ignore format instructions |
| [GAP-002](#gap-002) | Strict 3000-char filter drastically reduced dataset size | Threshold miscalibration | 545-record dataset likely too small for reliable SFT |
| [GAP-003](#gap-003) | Cloud swarm — most productive pipeline — was never fixed | Scope gap | Most powerful generation tool still broken |
| [GAP-004](#gap-004) | Audit tier system was fixed but is now too strict in a different direction | Overcorrection | Catalog says "archive" but builder uses everything anyway |
| [GAP-005](#gap-005) | Archive cleanup was incomplete — scripts/ directory never cleaned | Incomplete sweep | Codebase cleaner but not clean |

---

## GAP-001

**Title:** The Dataset Format Normalization Plan Introduced a New Problem
**Severity:** 🔴 High Impact

### Original Intent

Normalize all records in the master dataset to have consistent ` ```iec-st ` code fences in the assistant response, so the model learns **one output style** consistently. The plan was to eliminate the mixture of raw code and fenced code that had accumulated from different generation pipelines.

### What Actually Happened

The `build_master_dataset.py` normalizer was implemented and applied to the **response side** of every record. All 545 assistant messages in the master dataset now have ` ```iec-st ` fences. This part worked correctly.

However, the **prompt side** was never updated to match. The result:

| Prompt category | Count | % | What prompt says about format |
|----------------|-------|---|-------------------------------|
| V3 swarm prompts | 247 | 45.3% | "DO NOT OUTPUT MARKDOWN" |
| Generic prompts | 502 | 92.1% | Nothing about format |
| Prompts mentioning `iec-st` | 43 | 7.9% | Implicitly expects fence |

Every assistant response now has a fence. But 247 prompts explicitly forbid fences, and 502 prompts say nothing about format. The normalization was **applied to one side of the training pair only**.

### Why It Drifted

The normalization plan was scoped as "fix the response format." Updating the prompts to be consistent with the new response format was a separate concern that was not in scope at the time, and was never picked up afterward. The two halves of the training pair are managed by different functions in the codebase, and there was no mechanism to enforce consistency between them.

### Impact

The model receives contradictory training signals:
- 247 records: "I was told not to use markdown, but the answer has markdown" → the model learns that format instructions can be safely ignored
- 502 records: "I was given no format guidance, but the answer always has a fence" → the model learns to always produce fenced output
- Net result: the model will output fenced code **unconditionally**, regardless of user instructions

This outcome is **worse than having no normalization at all**, because:
1. Before normalization: the model saw mixed formats but at least some prompts and responses were internally consistent
2. After normalization: every record has a deliberate prompt-response contradiction

For a production system, raw code output (no fences) is often required for direct upload to PLC engineering tools. A model that ignores format instructions is less useful, not more.

---

## GAP-002

**Title:** The Strict 3000-Char Filter Drastically Reduced Dataset Size
**Severity:** 🟠 Medium-High Impact

### Original Intent

Raise the quality bar so that only **substantial, meaningful code** enters training. Reject short, trivial records that would teach the model to produce token-padding or boilerplate. The plan was specifically to prevent low-effort records from diluting the training signal.

### What Actually Happened

The `MIN_ASSISTANT_LENGTH = 3000` threshold was applied uniformly across all source datasets. The actual acceptance rates:

| Source Dataset | Total Records | Passed Filter | Acceptance Rate |
|---------------|---------------|---------------|----------------|
| `final_verified_dataset` | 5,919 | 495 | **8.4%** |
| `evol_instruct_dataset` | 1,632 | 153 | **9.4%** |
| V3 CLEAN batch | ~247 | ~247 | ~100% (already long) |
| Other sources | varies | varies | varies |
| **Total → Master** | **~8,000+** | **545** | **~6.8%** |

91.6% of available data was discarded by a single character-count threshold. The master dataset shrank from a potential pool of thousands of records to 545. The validation split is only 60 records — too small for statistically reliable evaluation.

### Why It Drifted

The 3,000-character threshold was chosen to exclude "trivial" code. However, **not all short IEC 61131-3 programs are trivial**. The threshold conflates code *length* with code *complexity*:

- A `TON` timer wrapper FB with proper documentation: ~800 chars → rejected
- A standard `LIMIT` function block with edge cases: ~1,200 chars → rejected
- A PID utility with pre-/post-scaling: ~2,200 chars → rejected
- A 4,000-char record that is mostly a repetitive 50-variable declaration: accepted

The threshold was a blunt instrument applied to a domain where utility functions and library wrappers are legitimately short but high-value for training.

### Impact

| Consequence | Detail |
|------------|--------|
| Dataset too small for reliable SFT | 545 records is below the minimum typically recommended for domain-specific fine-tuning without severe overfitting |
| Overfitting risk | The model will memorize these 545 records rather than generalize |
| Validation set too small | 60 validation records cannot provide statistically reliable loss curves |
| Missing an entire code category | All utility FBs, timer wrappers, and standard library extensions were filtered out |
| Wasted generation cost | Thousands of GPU-hours generated records that were discarded by a threshold set too conservatively |

A well-trained IEC 61131-3 model needs on the order of 5,000–50,000 training examples across all complexity levels. The 3,000-char floor eliminated the bottom 80% of that complexity spectrum.

---

## GAP-003

**Title:** The Cloud Swarm Was the Most Productive Pipeline But Was Never Fixed
**Severity:** 🔴 High Impact

### Original Intent

Fix the data generation process so that **future runs don't produce corrupt data**. After discovering that swarm-generated records had concatenated JSON corruption (multiple JSON objects written to the same file without separators), the plan was to clean up the corruption and prevent it from recurring.

### What Actually Happened

All fixes were applied to the **local Ollama pipeline**:
- `evol_orchestrator.py` — refactored generation loop
- `linter.py` — improved validation
- `ollama_client.py` — retry logic and error handling

The **cloud swarm subagent architecture** — which produced the 247 V3 enterprise records that became the highest-quality training data — was **never touched**. The subagents that ran the cloud swarm still:
- Write to shared output files using raw append operations
- Have no file locking or atomic write guarantees
- Will produce the same concatenated JSON corruption on the next run
- Have no deduplication between parallel agents writing to the same file

The repair/cleanup work (`repair_dataset.py`) was used to salvage the existing corrupt data. But if a new cloud swarm batch is run to generate more high-quality records, the exact same corruption will recur and will require another repair pass.

### Why It Drifted

The local Ollama pipeline is **code we own and can edit** — Python scripts in the repo that can be opened, modified, and tested locally. The cloud swarm runs via **agent invocations** — the "code" is in agent prompt templates and orchestration instructions, not in Python files. Fixing the swarm requires changing agent prompts and coordination logic, which was not addressed as part of the local pipeline repair work.

The scope of the fix was implicitly limited to "files in the repo" when it needed to also include "agent prompts and swarm coordination."

### Impact

| Consequence | Detail |
|------------|--------|
| Most powerful tool still broken | The cloud swarm can generate enterprise-grade, 30,000+ char ST programs that the local Ollama pipeline cannot match in quality |
| Any new swarm batch requires repair | Cannot generate and use new cloud data without another `repair_dataset.py` run |
| Data quality regression risk | If the repaired data is overwritten by a new corrupted run, the only copy of the clean V3 records could be lost |
| Scaling is blocked | Growing the dataset beyond 545 records depends on either the local pipeline (slow, lower quality) or the cloud swarm (fast, high quality, still broken) |

The 247 V3 cloud records are currently the only TIER_1 data in the entire catalog. Fixing the local pipeline while leaving the best data source broken means the pipeline cannot improve its output quality on future runs.

---

## GAP-004

**Title:** The Audit Tier System Was Fixed But Is Now Too Strict in a Different Direction
**Severity:** 🟠 Medium-High Impact

### Original Intent

Fix the audit tool so it **correctly identifies files unsuitable for fine-tuning**. Before the fix, the tier system was based almost entirely on JSON validity — virtually every file received TIER_1 ("Ready for fine-tuning") even if it contained refusals or low-quality code. The plan was to introduce meaningful IEC 61131-3 structural checks.

### What Actually Happened

The tier criteria were updated to require `FUNCTION_BLOCK` AND `VAR_INPUT`/`VAR_OUTPUT` blocks to be present for a record to count as "good." This caused a dramatic reclassification:

| Dataset | Before Fix | After Fix | Pass Rate After |
|---------|-----------|-----------|-----------------|
| `evol_instruct_dataset` | TIER_1 | **TIER_3** | 36.4% |
| `final_verified_dataset` | TIER_1 | **TIER_3** | 27.9% |
| `verified_github` | TIER_1 | **TIER_3** | 8.8% |
| `verified_oscat` | TIER_1 | **TIER_3** | 44.9% |
| V3 CLEAN batch | TIER_1 | **TIER_1** | ~100% |

TIER_3 is defined in the catalog as "Archive Only — Do Not Use for Fine-Tuning." The `DATA_CATALOG` now says `TIER_3 Archive Only` for the main baseline datasets that `build_master_dataset.py` still actively uses as `APPROVED_SOURCES`.

The audit tool and the master builder now give contradictory instructions about the same files:
- **Audit says:** "These are TIER_3 — archive only, do not use"
- **Master builder says:** "These are APPROVED_SOURCES — include in training"

### Why It Drifted

The TIER system in `audit_all_datasets.py` and the `APPROVED_SOURCES` list in `build_master_dataset.py` are **completely independent** — they do not reference each other. When the tier criteria were tightened, no one updated the `APPROVED_SOURCES` list to match. The two tools were designed to inform each other but have no runtime linkage.

Additionally, the new criteria (`FUNCTION_BLOCK` AND `VAR_INPUT`/`VAR_OUTPUT` required) are arguably too strict:
- Valid IEC ST PROGRAM blocks do not have `VAR_INPUT` in the same way
- Utility functions and standard library wrappers use `FUNCTION` not `FUNCTION_BLOCK`
- The OSCAT library (industrial gold standard) is rated TIER_3 — this is a red flag that the criteria may be miscalibrated

### Impact

| Consequence | Detail |
|------------|--------|
| Catalog is misleading in both directions | It said "everything is fine" before; now it says "almost everything is bad" |
| Developer confusion | A developer reading the catalog would not use these datasets — but we are training on them anyway |
| Trust in audit tool is undermined | If the catalog says TIER_3 for the OSCAT library, developers will stop trusting the tier ratings |
| Silent inconsistency persists | The builder and the auditor disagree, but neither raises an error about the disagreement |

The fix overcorrected from "too permissive" to "too strict" without calibrating the criteria against known-good datasets like OSCAT. The correction was applied without a validation step.

---

## GAP-005

**Title:** Archive Cleanup Was Incomplete — Scripts Directory Never Cleaned
**Severity:** 🟢 Low-Medium Impact

### Original Intent

Move all throwaway, one-off, and obsolete scripts to an `archive/` directory so that the **root workspace is clean and navigable**. A developer opening the repo should see only current, maintained code — not a graveyard of append scripts and experiments.

### What Actually Happened

The cleanup swept the root directory and the `data/` directory. Scripts in those locations were successfully moved to `archive/`. However, the sweep did not recurse into subdirectories:

**`scripts/` directory — 2 missed files:**
```
scripts/append_muon.py
scripts/append_pump_evol.py
```

**`Local_Ollama_Evol_Pipeline/` directory root — 10 missed files:**
```
Local_Ollama_Evol_Pipeline/append_auv_data.py
Local_Ollama_Evol_Pipeline/append_dataset.py
Local_Ollama_Evol_Pipeline/append_evol.py
Local_Ollama_Evol_Pipeline/append_laser_evol.py
[+ 6 additional append_*.py scripts]
```

These 12 files are all one-off data append scripts that were used during early pipeline construction and are no longer needed. They are named `append_*.py` — a clear pattern indicating they were run-once utilities, not maintained pipeline tools.

### Why It Drifted

The cleanup sweep explicitly targeted the **root directory** and `data/` as out-of-scope clutter zones. The subdirectory `Local_Ollama_Evol_Pipeline/` was treated as a "source code directory" and was not recursively scanned for cleanup candidates. The `scripts/` directory was also not in scope.

The cleanup was run as a targeted pass rather than a recursive scan of all directories. A `find . -name "append_*.py"` command would have caught all 12 files in one pass.

### Impact

| Consequence | Detail |
|------------|--------|
| Developer confusion in `Local_Ollama_Evol_Pipeline/` | Opening the directory shows 10 append scripts alongside the actual maintained pipeline code |
| Navigation overhead | A new developer must inspect each append script to determine if it is still needed |
| False sense of completion | The cleanup was declared done, but the codebase is cleaner — not clean |
| Git history pollution | These scripts remain as top-level noise in any directory listing |

The practical impact is low because the append scripts are benign — they do not affect any running pipeline. But the intent of the cleanup (a navigable codebase) was not fully achieved.

### Fix

```bash
# Find all remaining append scripts across subdirectories:
find . -name "append_*.py" -not -path "*/archive/*"

# Then move each to archive/:
git mv scripts/append_muon.py archive/one_off_scripts/
git mv scripts/append_pump_evol.py archive/one_off_scripts/
git mv Local_Ollama_Evol_Pipeline/append_*.py archive/one_off_scripts/
```

---

*Document generated: 2026-08-28. All gaps documented based on direct evidence from the codebase and pipeline execution history.*
