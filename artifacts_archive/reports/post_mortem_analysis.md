# Post-Mortem: Architecture Errors, Plan Failures & Plan Drift
*Analysis Date: 2026-08-28 | Project: LLM REASEARCH / PLC-LLM-OS*

---

> [!NOTE]
> This is a **read-only analysis document**. No code has been changed. Every finding below is backed by direct evidence from the current codebase. The purpose is to give you a clear picture of what actually happened vs. what was planned, so you can decide what matters and what to fix next.

---

## Section 1: Architecture Errors

These are structural problems that **exist in the code right now**, independent of the plan. They make the system behave incorrectly or unpredictably.

---

### ARC-001 — The Master Dataset Has a Massive Format Inconsistency Problem (Critical)

**What was claimed:** The `build_master_dataset.py` walkthrough said:
> *"All records formatted consistently using standard ChatML formatting and `iec-st` code blocks."*

**What is actually true:**

Running the verification check against `data/master/train.jsonl` (990 records):

| Metric | Count | % |
|---|---|---|
| Records WITH `` ```iec-st `` or `` ```st `` fence | **210** | **21%** |
| Records WITHOUT any code fence (raw code) | **780** | **79%** |

**79% of the master training dataset is raw code with no markdown fence.** This means the model being trained will see two completely different response formats and will not know which one it should produce. This is a direct contradiction of the stated goal of the plan ("100% consistent format before fine-tuning").

**Root cause:** The `build_master_dataset.py` script loads `evol_instruct_dataset.jsonl` (790 records contributed) but **never normalizes the format** of its records. The evol baseline dataset has **1,597 out of 1,632 records (97.9%) in raw code format** with no code fence. These all passed the quality gate unchanged and were injected into the master dataset.

**Why it matters for fine-tuning:** The model will be trained on inconsistent output formats. It will randomly produce raw code sometimes and markdown-fenced code other times. This confusion directly degrades fine-tune quality.

---

### ARC-002 — Seeds Directory is Polluted with Append Scripts, Not Seeds (Medium)

**Expected:** The `Local_Ollama_Evol_Pipeline/seeds/tier1_enterprise_grade/` directory should contain only `.jsonl` data files that the orchestrator reads for few-shot RAG context.

**Actual:** The directory contains **27 `.py` scripts** mixed in with 3 actual `.jsonl` files:
```
seeds/tier1_enterprise_grade/
  ├── append.py, append_amine_scrubber.py, append_cbtc.py ... (27 scripts!)
  ├── synthetic_evol_1634.jsonl    ← actual seed data
  ├── oscat_library_363.jsonl      ← actual seed data
  └── siemens_lgf_8.jsonl          ← actual seed data
```

The `load_seeds()` function in `evol_orchestrator.py` uses `tier_dir.glob("*.jsonl")`, so the `.py` scripts are silently ignored — but the directory is completely disorganized and confusing. A developer trying to add new seed data would have no idea the `.py` files should not be there.

Also: `seeds/tier1_enterprise_grade/temp_evolved.jsonl` (11 KB) is a temp file sitting in what should be the gold-standard seed tier.

---

### ARC-003 — Data Directory Still Contains Append Scripts and Temp Files (Medium)

**What the plan said:** Phase 5 was to clean up the workspace. The root would have `< 20 files`.

**What exists in `data/` right now:**
```
data/
  ├── append.py            ← raw append script, should not be here
  ├── append_aseptic_evol.py
  ├── append_evol.py
  ├── append_job.py
  ├── append_platooning.py
  ├── append_tokamak.py
  ├── write_haps.py
  ├── write_json.py        ← 8 Python scripts inside the data directory
  └── temp.json            ← temp file still here
```

**8 Python generation scripts** are sitting inside `data/`, and the temp file `data/temp.json` was never deleted despite being explicitly listed in the cleanup plan.

---

### ARC-004 — Local Pipeline Seeds Directory Has JSONL Files That Duplicate `data/` (Low)

The seeds directory contains copies of datasets:
- `seeds/tier1_enterprise_grade/synthetic_evol_1634.jsonl` — 3.9 MB copy of `evol_instruct_dataset.jsonl`
- `seeds/tier2_verified_github/github_direct_v2_1555.jsonl` — 3.1 MB
- `seeds/tier3_bulk_github/github_bulk_v3_2186.jsonl` — 3.7 MB

These are **not documented** anywhere. There is no record of whether these are deduplicated against the master, whether they are clean, or what their quality tier is. The `github_bulk_v3_2186.jsonl` in tier3 is in the folder the orchestrator reads as seeds — but it came from `github_raw_code.jsonl`, which was flagged in the analysis as **TIER_3 (raw, unverified)**. The model is currently being trained on raw, unverified scraped GitHub code as part of its seed context.

---

### ARC-005 — Linter Threshold Set to 1500 Chars But Plan Specified 3000 Chars (Low)

**Implementation plan (Step 3.2):**
> `+ Check 8: Minimum code length >= 3000 chars (anything shorter is a truncated or trivial response)`

**Actual linter (line 75-76 of `linter.py`):**
```python
if len(code_str.strip()) < 1500:
    return False, f"Code size too small ({len(code_str.strip())} chars). Minimum allowed is 1500."
```

The plan said 3000 chars minimum. The implementation used 1500 chars. The same 1500 threshold was used in `build_master_dataset.py`. As a result, **616 records in the master train set are under 3000 characters** — which was the originally intended quality bar. 

This is a borderline issue, but worth noting: the plan said records under 3000 chars were "truncated or trivial responses." The final dataset includes 62% of records below that threshold.

---

### ARC-006 — The Orchestrator Has No Mechanism to Resume from a Checkpoint (Medium)

The `run_evolution_loop()` function runs `iterations` cycles and at the end calls `merge_temp_files()`. If the script crashes at cycle 80 of 100, all 80 generated `.json` temp files sit in `temp_scratch/` but are never merged. On the next run, the orchestrator does NOT check for leftover temp files and merge them first — it just starts new iterations and merges at the end of **that** run. The leftover temp files from the crashed run remain orphaned in `temp_scratch/` indefinitely.

There is no `--resume` flag or checkpoint mechanism.

---

### ARC-007 — `github_raw_code.jsonl` Was Mislabeled TIER_1 in the Data Catalog (High)

**Data Catalog says:**
```
github_raw_code.jsonl | 4.61 MB | 400 | 400 | TIER_1 ✅ Safe for fine-tuning
```

**What the audit script actually found:**
- FUNCTION_BLOCK present: **19 / 400 (4.75%)**
- VAR_INPUT/OUTPUT present: **17 / 400 (4.25%)**
- END_IF/END_CASE present: **17 / 400 (4.25%)**

**A file where only 5% of records contain IEC 61131-3 FUNCTION_BLOCK was given a TIER_1 rating.** This happened because the audit script's TIER calculation was based on **JSON parse errors and refusal count**, not on IEC 61131-3 content quality. The file is perfectly valid JSON, so it passed as TIER_1 — but the actual code inside is mostly raw GitHub snippets, not properly structured function blocks. This directly contradicts the original deep analysis (Problem #8) which flagged `github_raw_code.jsonl` as raw unverified data that should NOT be included in fine-tuning.

---

## Section 2: Plan Failures

These are items that were explicitly promised in the implementation plan but were **not implemented**.

---

### PLN-FAIL-001 — No `.env` File Was Created (Phase 2, Step 2.1)

**Plan said:**
```
2. Create a .env file in project root:
     GCP_KEY_PATH=C:\Users\majip\.config\gcp\service_key.json
3. Any script that uses the GCP key should read:
     key_path = os.environ.get("GCP_KEY_PATH")
```

**Actual state:** `.env` does not exist. No script was updated to read the key from an environment variable. The GCP key was moved to the right location, but the integration step (making scripts use it via env vars) was never completed. Any cloud API call will still fail until the path is hardcoded or the env var set manually.

---

### PLN-FAIL-002 — `pipeline/__init__.py` Was Never Created (Phase 5, Step 5.1)

**Plan said:**
```
pipeline/
  ├── __init__.py          ← NEW
  ├── tools/
  └── README.md
```

**Actual state:** `pipeline/__init__.py` does not exist. The `pipeline/` directory is not a Python package — it's just a folder. This means `from pipeline.tools import repair_dataset` would fail. The scripts cannot be imported; they can only be run directly as standalone scripts.

---

### PLN-FAIL-003 — `data/raw_archive/` Subdirectory Was Never Created (Phase 5, Step 5.1)

**Plan said:**
```
data/
  ├── raw_archive/         ← NEW: Move raw/unverified here
  │   ├── github_raw_code.jsonl
  │   ├── oscat_raw.jsonl
  │   └── forum_raw_code.jsonl
```

**Actual state:** `data/raw_archive/` does not exist. `github_raw_code.jsonl`, `oscat_raw.jsonl`, and `forum_raw_code.jsonl` are still sitting in the root of `data/` alongside the clean TIER_1 files. There is no visual or structural separation between raw unverified data and production-ready data in the `data/` directory.

---

### PLN-FAIL-004 — Format Normalization Was Not Applied to the Baseline Dataset

**Plan said (Phase 1, Step 1.1, Step C):**
```
Step C - Format Normalizer:
  - If FORMAT_A (raw code, no fence): Wrap the code in ```iec-st\n{code}\n```
  - Update the user prompt to be mega-prompt style
```

**Actual state:** The `repair_dataset.py` was correctly written and correctly normalized the 247 records in `synthetic_generation_v3_enterprise_CLEAN.jsonl`. However, **the 1,632 records in `evol_instruct_dataset.jsonl` were never normalized** — they were pulled directly into the master dataset with their original raw format. The plan described normalizing the early-style records, but the `build_master_dataset.py` only ran a quality gate (length, refusals, IEC keywords), not a format normalization step. Result: 79% of the master dataset is in the wrong format (see ARC-001).

---

### PLN-FAIL-005 — The Safe Atomic Append Function Was Not Implemented

**Plan said (Phase 3, Step 3.3):**
```python
def safe_append_record(filepath: Path, record: dict) -> bool:
    """Atomically append a single record to a JSONL file."""
    ...
    f.seek(0, 2)  # Check last char for newline before appending
```

**Actual state:** This function was never written. The orchestrator instead implements `merge_temp_files()` (Strategy A), which is a good and different approach — but the explicitly planned `safe_append_record()` function does not exist. The plan listed both: fix the append AND add Strategy A. Only Strategy A was added. If for any reason Strategy A is bypassed (e.g., someone writes a new append script directly), the concatenation problem will recur.

---

### PLN-FAIL-006 — Root Directory Still Has 7 Files; Plan Verified With `< 20 files`

**Plan verification check:**
> `Confirm root directory has < 20 files (down from 125)`

**Actual state:** Root directory now has 7 files (good!), but the verification command was never actually run and reported in the walkthrough. More critically, the `data/` directory now contains **8 Python scripts and 1 temp file** that were missed during the cleanup sweep. The `Local_Ollama_Evol_Pipeline/` directory still has **15 files** at its root (many are old append scripts that should have been archived).

---

## Section 3: Plan Drift — Executed But in a Different Direction

These are cases where the plan was executed but the actual outcome is **different from what would be useful** for the actual goal (fine-tuning a PLC AI model).

---

### DRIFT-001 — The Master Dataset Includes the Wrong Sources

**What the plan said to include:**
```
1. synthetic_generation_v3_enterprise_CLEAN.jsonl  (~125 records, TIER_1)
2. evol_instruct_dataset.jsonl (1648 records)
3. verified_github_code.jsonl (after audit, TIER_2 filtered)
4. verified_oscat.jsonl (after audit, TIER_2 filtered)
```

**What was actually included and how much each contributed:**

| Source | Records Contributed | Notes |
|---|---|---|
| `synthetic_generation_v3_enterprise_CLEAN.jsonl` | 247 | ✅ Good |
| `evol_instruct_dataset.jsonl` | 790 | ⚠️ 97.9% have no code fence, avg 1,665 chars |
| `verified_github_code.jsonl` | 14 | ✅ Small but clean |
| `verified_oscat.jsonl` | 51 | ⚠️ Avg 943 chars (mostly too short for complex tasks) |

The 790 records from `evol_instruct_dataset.jsonl` dominate the dataset (71%). But this file was rated TIER_1 in the catalog primarily because it had few parse errors — not because it was actually high-quality IEC 61131-3 training data. It has 838 records under 1500 chars (if you apply the 1500-char filter, only 790 survive). The format is almost entirely unfenced raw code. This is the largest contributor and it is pulling the dataset quality down, not up.

Meanwhile, the `final_verified_dataset.jsonl` (5,919 records, 11.7 MB, TIER_1) was **completely ignored** by `build_master_dataset.py` — it was not in the `APPROVED_SOURCES` list. This is the largest and likely highest-quality dataset in the project and it was left out of the master entirely.

---

### DRIFT-002 — The Audit Script Gave Misleading TIER Ratings

**The audit in `audit_all_datasets.py` graded files on:**
- JSON parse error rate
- Refusal rate
- Presence of any IEC keyword

**What TIER_1 actually means here:** "This file has valid JSON and few refusals." It does **not** mean "this file is high-quality IEC 61131-3 training data."

**Evidence of the mismatch:**
- `github_raw_code.jsonl` — 400 records, rated TIER_1, but only **4.75% have FUNCTION_BLOCK**. It is raw scraped code.
- `forum_raw_code.jsonl` — 11 records, rated TIER_1, but **0% have FUNCTION_BLOCK or VAR_INPUT/OUTPUT**. Avg length is 713 chars.
- `verified_oscat.jsonl` — rated TIER_1, but avg length is **943 chars** (way below the 1500-char minimum for meaningful code).

The TIER system as implemented is a JSON validity checker, not an IEC 61131-3 quality checker. Anyone reading `DATA_CATALOG.md` would reasonably assume TIER_1 means "safe for fine-tuning without further filtering." That assumption is incorrect for several files.

---

### DRIFT-003 — Strategy A Is Implemented But Only for the Local Pipeline; Cloud Swarms Still Write Directly

The subagents that generated the `synthetic_generation_v3_enterprise.jsonl` file were writing directly to a shared file with no locking. Strategy A (write to temp files, merge at end) was implemented in `evol_orchestrator.py` for the **local Ollama pipeline only**.

The cloud swarm subagents (which produced the bulk of the V3 enterprise data) still write to the shared file using raw append operations. If the cloud swarms are ever used again in parallel, the corruption problem will recur. The fix was applied to the local tool but not to the architecture that originally caused the problem.

---

### DRIFT-004 — The Deep Analysis Said to Improve the Process; The Plan Fixed the Output, Not the Process

The original analysis question from the user was:
> *"Is the synthetic data generation process good or not? If it is good, can we make it better?"*

The deep analysis correctly identified that the **process** needed these improvements:
1. JSON validation gate in append scripts (so corruption never happens at write time)
2. Refusal detection in the subagent prompt/output pipeline
3. Format standardization enforced at generation time (not just at repair time)
4. Domain pre-screening before agent spawning

**What actually happened:** The plan focused heavily on **repairing the already-corrupt output** and doing cleanup. The actual cloud swarm subagent architecture that generates data was not modified — no JSON gate was added to the subagent append scripts, no refusal detection was added to the subagent pipeline, and no format enforcement was added to the swarm prompts.

The swarm architecture is unchanged. If you run it again tomorrow, you will get the same corruption pattern.

---

## Summary Table

| ID | Category | Issue | Severity |
|---|---|---|---|
| ARC-001 | Architecture | 79% of master dataset has no code fence — format is inconsistent | 🔴 Critical |
| ARC-002 | Architecture | Seeds directory polluted with 27 Python scripts | 🟡 Medium |
| ARC-003 | Architecture | `data/` has 8 Python scripts and `temp.json` not cleaned up | 🟡 Medium |
| ARC-004 | Architecture | Unverified `github_bulk_v3` used as tier3 seeds (raw scraped data) | 🟠 High |
| ARC-005 | Architecture | Linter uses 1500 char threshold; plan specified 3000 | 🟡 Low |
| ARC-006 | Architecture | No resume/checkpoint mechanism in local orchestrator | 🟡 Medium |
| ARC-007 | Architecture | `github_raw_code.jsonl` mislabeled TIER_1 (only 5% have FUNCTION_BLOCK) | 🟠 High |
| PLN-FAIL-001 | Plan Failure | `.env` file never created; GCP scripts not updated to use env vars | 🟡 Medium |
| PLN-FAIL-002 | Plan Failure | `pipeline/__init__.py` never created; pipeline is not a Python package | 🟡 Low |
| PLN-FAIL-003 | Plan Failure | `data/raw_archive/` never created; raw files not separated from clean | 🟠 High |
| PLN-FAIL-004 | Plan Failure | Format normalization applied to V3 CLEAN only, not to 1,632 baseline records | 🔴 Critical |
| PLN-FAIL-005 | Plan Failure | `safe_append_record()` never implemented; only Strategy A was applied | 🟡 Low |
| PLN-FAIL-006 | Plan Failure | Cleanup sweep missed `data/` scripts and Local_Ollama_Pipeline root files | 🟡 Low |
| DRIFT-001 | Plan Drift | `final_verified_dataset.jsonl` (5,919 records) excluded from master | 🟠 High |
| DRIFT-002 | Plan Drift | Audit TIER system checks JSON validity, not IEC 61131-3 quality | 🟠 High |
| DRIFT-003 | Plan Drift | Strategy A only implemented in local pipeline; cloud swarms still use raw append | 🟠 High |
| DRIFT-004 | Plan Drift | Data repaired after the fact; source generation process never fixed | 🟠 High |

---

## What This Means For Fine-Tuning

If you start fine-tuning on `data/master/train.jsonl` right now:

- ✅ Zero JSON parse errors (the DataLoader will not crash)
- ✅ Zero LLM refusals in training data
- ❌ **79% of records will train the model to output raw code without any code fence**
- ❌ **62% of records are under 3000 chars** (the original quality bar was 3000)
- ❌ The model will learn two contradictory output styles (raw vs. fenced code)
- ⚠️ The `final_verified_dataset.jsonl` with 5,919 high-quality records was not included
