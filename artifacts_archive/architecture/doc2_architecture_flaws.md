# Architectural Flaws Analysis

> This document describes systemic, structural problems in the PLC-LLM pipeline. Unlike code bugs (which are wrong lines that can be patched), architectural flaws are **design decisions** that make the entire system fragile, inconsistent, or unobservable. Fixing them requires changes to how components relate to each other, not just how individual lines of code behave.

---

## Severity Scale

| Rating | Meaning |
|--------|---------|
| 🔴 **CRITICAL** | The flaw directly undermines the output quality of the trained model |
| 🟠 **HIGH** | The flaw produces incorrect or misleading artifacts that affect downstream decisions |
| 🟡 **MEDIUM** | The flaw creates fragility, confusion, or observability gaps |
| 🟢 **LOW** | Technical debt with indirect impact on maintainability |

---

## Flaw Index

| ID | Name | Severity |
|----|------|----------|
| [ARCH-001](#arch-001) | No Single Source of Truth for the Dataset | 🔴 CRITICAL |
| [ARCH-002](#arch-002) | No System Message in Master Dataset — 3-Message Format Mismatch | 🔴 CRITICAL |
| [ARCH-003](#arch-003) | Prompt-Response Format Inconsistency | 🔴 CRITICAL |
| [ARCH-004](#arch-004) | Seeds Pipeline Feeds Inconsistent Format to Orchestrator | 🟠 HIGH |
| [ARCH-005](#arch-005) | No Feedback Loop — Failed Linter Output Never Improves Future Prompts | 🟠 HIGH |
| [ARCH-006](#arch-006) | Audit Tool Has a Pass Rate Logic Error | 🟡 MEDIUM |
| [ARCH-007](#arch-007) | No Training Validation Metric or Feedback Loop Back to Dataset Generation | 🟠 HIGH |
| [ARCH-008](#arch-008) | Source Provenance Stripped from Master Dataset | 🟡 MEDIUM |

---

## ARCH-001

**Severity:** 🔴 CRITICAL
**Name:** No Single Source of Truth for the Dataset
**Affected Components:** `train_plc_llm.py`, `build_master_dataset.py`, `train_dataset_formatter.py`, `data/master/train.jsonl`, `data/final_verified_dataset.jsonl`, `lumina/training/data/`

### Description

There are **three separate, fully disconnected dataset pipelines** in the same repository, each pointing to a different data source:

| Pipeline | Script | Output / Source |
|----------|--------|----------------|
| Master builder | `pipeline/tools/build_master_dataset.py` | Writes to `data/master/train.jsonl` |
| Fine-tune trainer | `lumina/training/train_plc_llm.py` | Reads from `data/final_verified_dataset.jsonl` |
| Training formatter | `lumina/training/train_dataset_formatter.py` | Has own `prepare_training_split()` that writes to `lumina/training/data/` |

These three components **do not reference each other**. There is no shared constant, no configuration file, and no contract that links them into a single pipeline. A developer who runs `build_master_dataset.py` to update the master dataset and then immediately runs `train_plc_llm.py` to train the model is silently training on a **completely different dataset** — the old, unfiltered raw file.

```
Developer intent:
  build_master_dataset.py  →  data/master/train.jsonl  →  [train on this]

Actual code path:
  build_master_dataset.py  →  data/master/train.jsonl  (never read by trainer)
  train_plc_llm.py         →  data/final_verified_dataset.jsonl  (unrelated file)
  train_dataset_formatter.py → lumina/training/data/  (third separate path)
```

### Impact

- Every fine-tuning run trains on the wrong data — the cleaned master is never used
- Three copies of "the dataset" exist with no version control or synchronization mechanism
- Adding a new record to one pipeline has no effect on the others
- The system appears to work (no crash, no error) while producing incorrect model weights

### Root Cause

The training code and the data pipeline code were built independently (likely by different agents at different times) and were never integrated. There is no single `DATASET_PATH` constant, no dataset registry, and no build system that enforces the linkage.

### Fix Direction

Define a single canonical dataset path constant in a shared config file and enforce its use across all three components. The master builder, formatter, and trainer must all read from and write to the same location.

---

## ARCH-002

**Severity:** 🔴 CRITICAL
**Name:** No System Message in Master Dataset — 3-Message Format Mismatch
**Affected Components:** `data/master/train.jsonl` (all 545 records), `train_dataset_formatter.py`, `train_plc_llm.py`

### Description

Every record in `data/master/train.jsonl` has exactly **2 messages**:

```json
{
  "messages": [
    {"role": "user",      "content": "Write a FUNCTION_BLOCK for..."},
    {"role": "assistant", "content": "```iec-st\nFUNCTION_BLOCK..."}
  ]
}
```

There is **no system message** in any of the 545 records. Zero records include a `{"role": "system", ...}` turn.

However, `train_dataset_formatter.py` always injects a system message containing the **Lumina AI persona** before the user turn:

```json
{
  "messages": [
    {"role": "system",    "content": "You are Lumina AI, an expert IEC 61131-3..."},
    {"role": "user",      "content": "Write a FUNCTION_BLOCK for..."},
    {"role": "assistant", "content": "```iec-st\nFUNCTION_BLOCK..."}
  ]
}
```

The training formatter and the dataset builder **disagree on the message format**. When `train_plc_llm.py`'s `format_chatml()` processes 2-message records directly (without the formatter's persona injection), the model is trained on prompts that never include a system message. The Lumina AI persona — the product identity — is never seen during training.

### Impact

- The trained model **has no knowledge of the Lumina AI persona** — it was never in the training data
- If the formatter is used in inference but not training, there is a train/serve mismatch: the model sees a format at inference time it never encountered during training
- All 545 records are affected — this is not an edge case
- The product's core identity cannot be instilled via fine-tuning with the current dataset structure

### Root Cause

The dataset was built from raw scraped and generated data that was never prepended with a persona. The formatter was written to add the persona at training time, but the trainer bypasses the formatter and reads the raw records directly (see ARCH-001). Even if the trainer used the formatter, the persona injection at training time rather than data-build time means the dataset itself has no canonical format.

---

## ARCH-003

**Severity:** 🔴 CRITICAL
**Name:** Prompt-Response Format Inconsistency Persists in a Different Way
**Affected Components:** `data/master/train.jsonl` (all 545 records), V3 swarm-generated records (247), `build_master_dataset.py`

### Description

The training data contains a **systematic contradiction between what prompts ask for and what responses demonstrate**. This occurs in two distinct ways:

#### Problem A — "No markdown" prompts with fenced responses

The V3 swarm prompts explicitly instruct the model:

> *"OUTPUT ONLY THE RAW CODE. DO NOT OUTPUT MARKDOWN."*

But `build_master_dataset.py`'s normalizer then wraps every response in a ` ```iec-st ` markdown fence. The result for 247 records:

| Prompt says | Response shows |
|------------|----------------|
| "Do NOT use markdown fences" | ` ```iec-st\n...\n``` ` |

The model is trained on 247 examples that directly contradict their own instructions.

#### Problem B — Prompts with no format guidance

| Format guidance in prompt | Record count | % of total |
|--------------------------|--------------|-----------|
| Prompts mentioning `iec-st` explicitly | 43 | 7.9% |
| V3 prompts saying "no markdown" but with fenced response | 247 | 45.3% |
| Prompts with no format guidance at all | 502 | 92.1% |

502 of 545 prompts say nothing about output format. The model receives no signal about when to fence vs. when not to fence from 92% of its training examples.

### Impact

The model learns conflicting format behaviors simultaneously:
- From 247 records: "My instructions said no fence, but the answer had a fence" → learn to ignore format instructions
- From 502 records: "No format guidance was given, but the answer always has a fence" → learn to always fence regardless of instructions
- The net result: **the model will output fenced code unconditionally**, regardless of what the user asks

This is architecturally harmful for a production system where raw code output (without fence markers) is often needed for direct PLC upload or copy-paste into engineering tools.

### Root Cause

Normalization was applied only to the **response** side of the dataset. The **prompt** side was never updated to be consistent with the response format. The fix was applied to only one half of the training pair.

---

## ARCH-004

**Severity:** 🟠 HIGH
**Name:** Seeds Pipeline Feeds Inconsistent Format to Orchestrator
**Affected Components:** `evol_orchestrator.py`, seed tier directories (Tier 1–4)

### Description

The local orchestrator loads seeds from all 4 tier directories. These seeds come from two distinct sources with fundamentally different formats:

| Source | Count | Format |
|--------|-------|--------|
| Raw/unformatted seed records | 3,752 | No code fence — raw ST code |
| Normalized seed records | 40 | With ` ```iec-st ` fence |

When the orchestrator selects 2 seeds as "VERIFIED EXAMPLES" and injects them into the generation prompt, the model sees raw code examples. The generation prompt simultaneously says "DO NOT OUTPUT MARKDOWN" (V3 style) or says nothing about format. The examples themselves are all raw code.

But the **dataset builder** will later normalize the output by wrapping it in a fence. So:

```
Seed examples show:  raw code, no fence
Prompt demands:      high-quality, complex structure
Dataset builder:     adds fence to response after generation
```

The model generating new code has no clear signal about output format because the examples it sees (raw) do not match what the dataset builder expects (fenced). This is why the model **sometimes outputs raw code and sometimes outputs fenced code** between runs — its in-context examples are inconsistent.

### Impact

- Generation quality is non-deterministic across runs beyond what temperature alone explains
- The orchestrator's linter must handle both raw and fenced outputs, adding complexity
- Records that come out raw are fence-wrapped by the builder, creating the ARCH-003 mismatch
- The example injection RAG step actively teaches the wrong format to the generation model

### Root Cause

The seed files were loaded directly from source without format normalization. The normalization step was only applied to the master dataset output, not to the seeds used as in-context examples during generation.

---

## ARCH-005

**Severity:** 🟠 HIGH
**Name:** No Feedback Loop — Failed Linter Output Never Improves Future Prompts
**Affected Components:** `evol_orchestrator.py`, linter, domain inventor, seed selection

### Description

The current generation pipeline is a **pure open-loop system** at the record level:

```
Domain Inventor → Prompt → Ollama → Linter
                                        ↓
                               PASS → save record
                               FAIL → retry (up to 3×)
                                        ↓
                               FAIL × 3 → DISCARD
                                        (error logged only)
```

When all 3 retries fail, the error is written to the log and the iteration ends. **Nothing about this failure is used to improve future iterations.** Specifically:

- The domain that caused failures is not blacklisted or deprioritized
- The seeds that were selected for the failing prompt are not marked as poor examples
- The linter error message (e.g., "mismatched IF/END_IF", "missing VAR_INPUT block") is not fed back to the prompt
- The next iteration begins from scratch with no memory of what failed

### Impact

Over a long run, the orchestrator will repeatedly attempt the same failure-prone domain types with the same seeds, fail in the same ways, and discard the results — wasting GPU hours. The failure rate will be stable or worsen over time rather than improving as the run progresses.

A minimal feedback loop would:
1. Track per-domain and per-seed-pair failure rates
2. Reduce sampling probability for high-failure domains
3. Pass the last linter error back to the model as a correction hint on retry 2+

### Root Cause

Designing a stateful feedback loop is significantly more complex than the current stateless retry logic. The orchestrator was built for correctness (retries) but not for learning (feedback). Adding a feedback loop requires maintaining per-run state and modifying the prompt construction logic.

---

## ARCH-006

**Severity:** 🟡 MEDIUM
**Name:** Audit Tool Has a Pass Rate Logic Error
**Affected Components:** `audit_all_datasets.py`, `DATA_CATALOG`

### Description

`audit_all_datasets.py` computes `pass_rate` as:

```python
pass_rate = good_records / total_non_empty_lines
```

The denominator `total_non_empty_lines` includes:
- Records with JSON parse errors
- Records with structural issues (fewer than 2 messages)
- Records identified as refusals
- Records that are too short
- Records that actually pass IEC quality checks

Only the last category counts as `good_records`. All others are in the denominator but not the numerator.

**Example:** A dataset file with 100 records where 50 have JSON parse errors and 50 are valid IEC ST records:
- `total_non_empty_lines = 100`
- `good_records = 50`
- `pass_rate = 50%` → **Tier 2**
- But the real quality of parseable records is **100%** (50/50 valid)

The tier assignment is driven by a misleading denominator.

### Impact

- Datasets with many broken records appear lower quality than they are
- Datasets may be wrongly demoted to TIER_3 ("Archive Only") status when their actual IEC content quality is high
- The `DATA_CATALOG` tier assignments are not comparable across files with different proportions of parse errors vs. IEC failures
- Developers making decisions about which datasets to include or exclude are working from incorrect quality metrics

### Root Cause

The denominator should be `parseable_records` (records that were successfully parsed as JSON with valid structure), not `total_non_empty_lines`. The bug is subtle because "lines with content" seems like a reasonable denominator until you account for the fact that some lines are structurally broken before IEC validation even begins.

---

## ARCH-007

**Severity:** 🟠 HIGH
**Name:** No Training Validation Metric or Feedback Loop Back to Dataset Generation
**Affected Components:** Entire pipeline (data generation → training → inference)

### Description

The complete pipeline flow is:

```
Seeds → Evol Orchestrator → Generated Records → Master Builder → train_plc_llm.py → Model Weights
                                                                                           ↓
                                                                                    [PIPELINE ENDS]
```

There is **no step after model weights**. The pipeline does not:
- Run the trained model against a benchmark or held-out test set
- Measure where the model fails (which IEC domains, which code patterns)
- Feed that failure information back to the orchestrator to generate more data for weak domains
- Evaluate whether fine-tuning actually improved on a meaningful baseline

The system is **completely open-loop at the pipeline level**: it generates data, trains, and stops. The only feedback is human inspection of model outputs, which requires manual effort and does not connect back to the data generation step.

### Impact

| Consequence | Detail |
|------------|--------|
| No objective quality measure | There is no way to know if fine-tuning improved the model |
| No weak-domain identification | There is no mechanism to identify which IEC domains are underrepresented or undertrained |
| No iterative improvement | Each new training run starts from scratch with the same data distribution |
| Resources misdirected | GPU hours cannot be directed toward areas of model weakness because those areas are never measured |

### Root Cause

Building a closed-loop evaluation system requires: a benchmark dataset, an evaluation script, a mechanism to route results back to the orchestrator, and a domain-tagging system on training records. All of these are absent. The pipeline was built to produce data and train — not to measure training effectiveness.

---

## ARCH-008

**Severity:** 🟡 MEDIUM
**Name:** Source Provenance Stripped from Master Dataset (Observability Gap)
**Affected Components:** `build_master_dataset.py` (`strip_metadata()`), `data/master/train.jsonl`

### Description

`build_master_dataset.py` calls `strip_metadata()` on every record before writing it to `data/master/train.jsonl`. This function removes the `_source` field — the field that records which upstream file the record came from:

```python
# build_master_dataset.py — strip_metadata()
def strip_metadata(record):
    cleaned = {k: v for k, v in record.items() if not k.startswith('_')}
    return cleaned  # _source, _tier, _original_file all removed
```

Once `data/master/train.jsonl` is written, it is **impossible to determine which of the 545 records came from which source file** without rebuilding the entire master from scratch.

### Impact

| Scenario | Consequence Without Provenance |
|----------|-------------------------------|
| A bad record is found in training | Cannot trace it to its source file to fix the upstream data |
| A source file needs to be quarantined | Cannot remove only its records from master — must full rebuild |
| A source file is found to be low quality | Cannot measure how many master records it contributed |
| An audit reveals a category of bad records | Cannot identify which pipeline produced them |

The master dataset is a **black box**: 545 records of unknown origin, with no audit trail connecting them to the source pipelines that generated them.

### Root Cause

The `strip_metadata()` function was designed to produce a clean, minimal JSONL file for training. However, the provenance metadata was stripped rather than moved to a separate sidecar file. The correct approach is to strip `_source` from the training JSONL but write it to a `data/master/provenance.jsonl` manifest alongside `train.jsonl`.

### Fix Direction

```python
# When building master, write a parallel provenance file:
provenance = {
    'record_hash': sha256(json.dumps(record['messages'])),
    '_source': record.get('_source'),
    '_tier': record.get('_tier'),
    '_original_file': record.get('_original_file'),
}
# Write stripped record to train.jsonl
# Write provenance to provenance.jsonl (same index = same record)
```

This preserves full traceability without polluting the training file format.

---

*Document generated: 2026-08-28. All flaws verified against codebase architecture at time of writing.*
