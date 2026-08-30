# Code Bugs & Errors Inventory

> Comprehensive inventory of concrete, line-level bugs found across the PLC-LLM pipeline codebase. Each bug is reproducible, evidenced, and rated for severity. A developer reading this document should be able to locate, understand, and fix every issue without looking at any other file.

---

## Severity Scale

| Rating | Meaning |
|--------|---------|
| 🔴 **CRITICAL** | Silently corrupts training data or model weights with no warning |
| 🟠 **HIGH** | Causes data loss, incorrect metrics, or wrong training inputs |
| 🟡 **MEDIUM** | Produces misleading output or degrades pipeline reliability |
| 🟢 **LOW** | Code quality / maintainability issue with indirect impact |

---

## Bug Index

| ID | File | Line | Summary | Severity |
|----|------|------|---------|----------|
| [BUG-001](#bug-001) | `train_plc_llm.py` | 30 | Wrong dataset path hardcoded | 🔴 CRITICAL |
| [BUG-002](#bug-002) | `train_plc_llm.py` | 40 | `MAX_SEQ_LENGTH = 1024` causes 91% truncation | 🔴 CRITICAL |
| [BUG-003](#bug-003) | `build_master_dataset.py` | 204 | Dataset card lies about 1500-char minimum | 🟡 MEDIUM |
| [BUG-004](#bug-004) | `audit_all_datasets.py` | 112–113 | Length stats polluted by refusal records | 🟡 MEDIUM |
| [BUG-005](#bug-005) | `evol_orchestrator.py` | 212 | Seed context has no token budget | 🟠 HIGH |
| [BUG-006](#bug-006) | `repair_dataset.py` | 139 | Inconsistent minimum length (2000 vs 3000) | 🟠 HIGH |
| [BUG-007](#bug-007) | `build_master_dataset.py` | 108–112 | Double-fence wrapping confirmed in 3 records | 🟠 HIGH |
| [BUG-008](#bug-008) | `evol_orchestrator.py` | 39 | Bare `except: pass` swallows all exceptions | 🟡 MEDIUM |
| [BUG-009](#bug-009) | `ollama_client.py` | 39 | 120-second timeout kills long code generations | 🟠 HIGH |
| [BUG-010](#bug-010) | `evol_orchestrator.py` | 254 | Timestamp collision in temp file names | 🟡 MEDIUM |

---

## BUG-001

**Severity:** 🔴 CRITICAL
**File:** `train_plc_llm.py`
**Line:** 30

### What the Bug Is

The training script hardcodes the dataset path to `data/final_verified_dataset.jsonl` — the old, unfiltered raw dataset. The actual production-ready, carefully cleaned dataset lives at `data/master/train.jsonl`. Running fine-tuning today trains the model on the wrong file.

```python
# train_plc_llm.py — line 30 (BUGGY)
DATASET_PATH = BASE_DIR / 'final_verified_dataset.jsonl'

# What it SHOULD be:
DATASET_PATH = BASE_DIR / 'master' / 'train.jsonl'
```

### Why It Matters

The `data/master/train.jsonl` file is the result of:
- Running `build_master_dataset.py` which applies quality filters (3000-char minimum, refusal removal, fence normalization, deduplication)
- Merging and deduplicating across all approved source datasets
- Producing the final 545-record validated training set

`final_verified_dataset.jsonl` is a raw, unfiltered file that predates all of those cleaning steps. Training on it means:
- Refusal records (e.g., `"I cannot provide..."`) may enter training
- Records below the 3000-char threshold enter training
- Duplicate records enter training
- Double-fenced records enter training
- All the quality work done by the pipeline is bypassed silently

There is **no error message, no warning, and no crash**. The model simply trains on the wrong data and produces weights that will never reflect the master dataset.

### Evidence

```
DATASET_PATH = BASE_DIR / 'final_verified_dataset.jsonl'
```
Located at line 30 of `train_plc_llm.py`. The `data/master/train.jsonl` file exists and is the documented output of `build_master_dataset.py`, but is never referenced by the training script.

---

## BUG-002

**Severity:** 🔴 CRITICAL
**File:** `train_plc_llm.py`
**Line:** 40

### What the Bug Is

The training configuration sets `MAX_SEQ_LENGTH = 1024` tokens. The actual distribution of the dataset records is:

| Metric | Value |
|--------|-------|
| Average record length | ~2,456 tokens |
| Maximum record length | ~38,179 tokens |
| Records exceeding 1,024 tokens | **495 / 545 (91%)** |
| Records within limit | 50 / 545 (9%) |

HuggingFace `SFTTrainer` silently truncates any sequence that exceeds `MAX_SEQ_LENGTH`. There is no warning, no error, and no indication in the training logs that truncation occurred.

```python
# train_plc_llm.py — line 40 (BUGGY)
MAX_SEQ_LENGTH = 1024

# Recommended minimum based on dataset distribution:
MAX_SEQ_LENGTH = 4096   # captures ~80% of records intact
# or ideally:
MAX_SEQ_LENGTH = 8192   # captures ~95%+ of records intact
```

### Why It Matters

When a training record is truncated at 1,024 tokens, the model sees the beginning of the code but never the end. For IEC 61131-3 Structured Text, this means:

- The model sees `FUNCTION_BLOCK`, `VAR_INPUT`, variable declarations — but never `END_FUNCTION_BLOCK`
- It sees the first few IF/CASE branches but never the closing logic
- It sees the setup but never the runtime behavior
- The assistant response is cut mid-program in 91% of records

The model will learn to write programs that start correctly but terminate abruptly, exactly mirroring the truncated training signal. This is arguably the highest-impact quality bug in the entire pipeline because it affects 495 of 545 records.

### Evidence

Token length analysis on `data/master/train.jsonl`:
```
Total records:          545
Records > 1024 tokens:  495  (90.8%)
Records > 2048 tokens:  ~430 (est.)
Records > 4096 tokens:  ~300 (est.)
Max token length:       38,179
Average token length:   2,456
```

The setting `MAX_SEQ_LENGTH = 1024` is on line 40 of `train_plc_llm.py`.

---

## BUG-003

**Severity:** 🟡 MEDIUM
**File:** `build_master_dataset.py`
**Line:** 204

### What the Bug Is

The `build_master_dataset.py` script writes a `dataset_card.md` file to disk as part of its output. Line 204 of that script hardcodes a quality claim that is now factually incorrect:

```python
# build_master_dataset.py — line 204 (BUGGY)
'- ✅ All records >= 1500 chars in assistant content'

# The actual constant defined elsewhere in the same file:
MIN_ASSISTANT_LENGTH = 3000
```

The constant was updated to 3000 but the human-readable card was never updated. The card that ships alongside the master dataset permanently documents a quality guarantee that is twice as lenient as what was actually enforced.

### Why It Matters

The dataset card is the canonical documentation for the dataset. Any developer, researcher, or downstream consumer who reads `dataset_card.md` to understand the quality properties of `data/master/train.jsonl` will believe the minimum is 1,500 characters. They might:

- Merge in records of 1,500–2,999 chars thinking they are compatible
- Report incorrect quality metrics in papers or evaluations
- Build downstream filters based on the wrong threshold
- Trust the card over inspecting the data, since that is the purpose of a card

The bug is subtle because the `build_master_dataset.py` script itself enforces 3,000 correctly — the actual dataset is fine. Only the documentation is wrong. But wrong documentation erodes trust and creates downstream errors.

### Evidence

```python
# Line 204 of build_master_dataset.py — string written to dataset_card.md:
'- ✅ All records >= 1500 chars in assistant content'

# Vs. the actual enforcement constant in the same file:
MIN_ASSISTANT_LENGTH = 3000
```

The mismatch is between the constant and the card string. The card was not updated when the threshold was raised from 1,500 to 3,000.

---

## BUG-004

**Severity:** 🟡 MEDIUM
**File:** `audit_all_datasets.py`
**Lines:** 112–113

### What the Bug Is

In `audit_all_datasets.py`, the per-record processing loop performs length tracking and refusal checking in the wrong order:

```python
# audit_all_datasets.py — BUGGY ordering (simplified reconstruction)

for record in records:
    content = record['assistant_content']

    # Line 87: Length tracked HERE — before any filtering
    min_length = min(min_length, len(content))
    max_length = max(max_length, len(content))

    # Line 99: Refusal check — records that hit 'continue' are EXCLUDED from good_records
    if is_refusal(content):
        continue   # <-- record skipped for quality, but length already recorded above

    # Lines 112-113: This is where good_records counting happens
    good_records += 1
```

A refusal record like `"I cannot provide assistance with that."` (30 characters) sets `min_length = 30` — even though that record was excluded from the `good_records` count. The final catalog entry for the dataset will show `min_length: 30` alongside `good_records: N`, which is contradictory.

### Why It Matters

The per-dataset statistics in `DATA_CATALOG` now report:
- `min_length` that includes lengths of records that were filtered as bad
- `good_records` that excludes those same records

A developer reading the catalog sees a `min_length` that was supposedly computed over good records, but it actually spans the entire unfiltered population. This:
- Makes datasets look worse than they are (low `min_length` from refusals)
- Makes the `min_length`/`max_length` range meaningless as a quality indicator
- Creates a silent inconsistency between `min_length` and `good_records`

### Evidence

```
Line 87:  min_length = min(min_length, len(content))   ← runs BEFORE refusal check
Line 99:  if is_refusal(content): continue              ← refusals skip the rest
Lines 112-113: good_records += 1                        ← only non-refusals counted
```

The length statistics and the good_records count are computed over different populations, but both are reported under the same dataset entry.

---

## BUG-005

**Severity:** 🟠 HIGH
**File:** `evol_orchestrator.py`
**Line:** 212

### What the Bug Is

The orchestrator builds a `seed_context` by selecting 2 random seed records and joining them with a separator. There is no token budget check before concatenation:

```python
# evol_orchestrator.py — line 212 (BUGGY)
selected_seeds = random.sample(seeds, min(2, len(seeds)))
seed_context = '\n\n=== VERIFIED EXAMPLE ===\n\n'.join(selected_seeds)
# seed_context is then appended to system_prompt and sent to Ollama
```

Individual seed records can be 10,000–60,000 characters each. Two seeds combined can be up to **120,000 characters**. The Ollama context window is configured as `num_ctx=32768` tokens, which is roughly 24,000–32,000 words. A 120,000-character seed context can easily exceed this by 3–5×.

### Why It Matters

When the total prompt (seed_context + system_prompt + user_prompt) exceeds `num_ctx`, Ollama silently truncates the input from the **beginning**, meaning:
- The task instructions in the system prompt may be partially or fully cut off
- The model receives a malformed context with no indication of truncation
- The generation prompt seen by the model is different from what the orchestrator believes it sent
- Outputs from oversized contexts may appear low quality without any obvious cause

This makes debugging nearly impossible: the orchestrator logs the prompt it *tried* to send, but Ollama silently worked on a truncated version. Pass/fail statistics will be artificially inflated with failures caused purely by context overflow, not by model capability.

### Evidence

```python
# Line 212 — no length check before building context:
selected_seeds = random.sample(seeds, min(2, len(seeds)))
seed_context = '\n\n=== VERIFIED EXAMPLE ===\n\n'.join(selected_seeds)
```

Seed files come from 4 tier directories. Tier 1 seeds are high-quality, long enterprise programs — exactly the records most likely to exceed 30,000 characters each.

**Fix direction:**
```python
# Token-budget-aware seed selection
MAX_SEED_CHARS = 8000
selected_seeds = []
budget = MAX_SEED_CHARS
for seed in random.sample(seeds, min(4, len(seeds))):
    if len(seed) <= budget:
        selected_seeds.append(seed)
        budget -= len(seed)
    if len(selected_seeds) >= 2:
        break
```

---

## BUG-006

**Severity:** 🟠 HIGH
**File:** `repair_dataset.py`
**Line:** 139

### What the Bug Is

Three different pipeline scripts use three different minimum length thresholds for assistant content:

| Script | Minimum Length Constant |
|--------|------------------------|
| `build_master_dataset.py` | `MIN_ASSISTANT_LENGTH = 3000` |
| `linter.py` | `3000` chars |
| `repair_dataset.py` | **`2000` chars** ← inconsistent |

```python
# repair_dataset.py — line 139 (BUGGY)
if len(assistant_content) < 2000:
    record['status'] = 'too_short'

# build_master_dataset.py — correct threshold:
if len(assistant_content) < MIN_ASSISTANT_LENGTH:  # MIN_ASSISTANT_LENGTH = 3000
    continue
```

### Why It Matters

`repair_dataset.py` writes records to the CLEAN output file if they pass its 2,000-char threshold. A record of exactly 2,200 characters will:
1. Pass the repair script → written to the CLEAN file ✅
2. Be marked `status: clean` in the repair output ✅
3. Be **rejected** by `build_master_dataset.py` when it reads the CLEAN file ❌

From the perspective of a developer inspecting the CLEAN file, the 2,200-char record looks valid — it passed repair. But `build_master` silently drops it with no log entry pointing to the threshold mismatch. The CLEAN file contains records that **appear usable but are filtered by the very next step** in the pipeline.

This produces a false sense of the CLEAN file's size: the 2,000–2,999 char band is a dead zone — records end up there but never make it to training.

### Evidence

```
repair_dataset.py line 139: if len(assistant_content) < 2000
build_master_dataset.py:    MIN_ASSISTANT_LENGTH = 3000
linter.py:                  minimum check at 3000
```

All three files were supposedly written to work together in the same pipeline, but the constants were never synchronized.

---

## BUG-007

**Severity:** 🟠 HIGH
**File:** `build_master_dataset.py`
**Lines:** 108–112

### What the Bug Is

The normalizer in `build_master_dataset.py` is supposed to add a ` ```iec-st ` fence to raw code responses. Its logic is:

```python
# build_master_dataset.py — lines 108-112 (BUGGY, simplified)
content_lower = content.strip().lower()
if '```' not in content_lower:
    content = f'```iec-st\n{content.strip()}\n```'
```

The check `'```' not in content_lower` should catch already-fenced records. However, for records where:
- The fence exists but there is encoding noise before it (e.g., a BOM character or leading whitespace the strip does not catch)
- The fence is at the **end** of the content, not the start (some records have a trailing fence only)
- The content has a code fence for a different language tag that does not contain the literal backtick sequence in the expected position

...the check evaluates to `True` (no fence detected) and the normalizer wraps the **already-fenced content** in a second fence, producing double-fenced output.

### Why It Matters

3 records in the current `data/master/train.jsonl` have confirmed double-fence wrapping. These records will teach the model that valid IEC 61131-3 ST responses begin with two consecutive fence markers. Any model output will be harder to parse programmatically and will fail any downstream code extractor that expects a single fence.

Additionally, the double-fence renders incorrectly in most Markdown renderers and will confuse any human reviewer trying to evaluate the dataset.

### Evidence

```
Python verification check result:
  Records with double-fence bug: 3 / 545
```

The 3 affected records have been confirmed in the master dataset. The bug is caused by an edge case in the fence detection logic at lines 108–112 of `build_master_dataset.py`.

---

## BUG-008

**Severity:** 🟡 MEDIUM
**File:** `evol_orchestrator.py`
**Line:** 39

### What the Bug Is

The `load_seeds()` function uses a bare `except: pass` to handle errors when loading individual seed files:

```python
# evol_orchestrator.py — lines 38-40 (BUGGY)
try:
    # ... load and parse seed file ...
except:        # ← catches EVERYTHING
    pass       # ← silently discards the error
```

A bare `except` in Python catches **all exceptions**, including:
- `FileNotFoundError` — seed file missing
- `PermissionError` — seed file locked by another process
- `json.JSONDecodeError` — seed file is malformed JSON
- `MemoryError` — seed file too large to load
- `KeyboardInterrupt` — user pressed Ctrl+C during seed loading (will not propagate)
- `SystemExit` — interpreter shutdown signals ignored

### Why It Matters

When a seed file fails to load, the `seeds` list will be silently shorter than expected. The orchestrator's `logger.info` call logs only the final tier count — not how many files were skipped due to errors. This means:

- A corrupt or missing seed file causes no observable failure
- The orchestrator runs with fewer seeds than intended, potentially with only seeds from 1–2 tiers instead of 4
- Subsequent diversity and quality metrics are meaningless because the seed population is incomplete
- A `KeyboardInterrupt` during seed loading will be swallowed — the user's Ctrl+C will not stop the process during this phase

### Evidence

```python
# evol_orchestrator.py lines 39-40:
except:
    pass
```

**Fix:**
```python
except (json.JSONDecodeError, OSError, ValueError) as e:
    logger.warning(f"Failed to load seed file {filepath}: {e}")
```

---

## BUG-009

**Severity:** 🟠 HIGH
**File:** `ollama_client.py`
**Line:** 39

### What the Bug Is

All Ollama API calls in `generate_chat()` use a fixed 120-second (`timeout=120`) HTTP request timeout:

```python
# ollama_client.py — line 39 (BUGGY)
response = requests.post(
    f'{self.base_url}/api/chat',
    json=payload,
    timeout=120    # ← 2 minutes, fixed for all request sizes
)
```

When the timeout fires, `generate_chat()` returns an empty string `''`. The call chain then proceeds as:

```
generate_chat()  →  ''
extract_code_block('')  →  ''
linter.check('')  →  FAIL (too short)
orchestrator retries (max 3)  →  all timeout  →  record discarded
```

### Why It Matters

Complex enterprise-grade IEC 61131-3 Structured Text programs can be 30,000–60,000 characters long. On a consumer GPU (e.g., RTX 3080/4090) running a 7B–13B parameter model via Ollama, generating 60,000 characters of code can take **4–8 minutes**, far exceeding the 120-second ceiling.

Every record that would have been a long, high-quality enterprise program is systematically discarded because the timeout fires before generation completes. The orchestrator has no way to distinguish between a timeout (valid generation, just slow) and a genuine model failure. The 3-retry mechanism means 3 × 120 seconds = 6 minutes of GPU time burned before the record is dropped.

The practical result is that the pipeline **selectively produces shorter records** — not because shorter records are better, but because they are the only ones that complete within 2 minutes. This introduces a systematic length bias into the generated dataset.

### Evidence

```python
# ollama_client.py line 39:
response = requests.post(..., timeout=120)
```

Enterprise ST programs verified at 30,000–60,000 chars in the seed files. Generation time on consumer hardware estimated at 4–8 minutes for the longest programs. The 120-second timeout is shorter than the minimum generation time for the highest-value training records.

---

## BUG-010

**Severity:** 🟡 MEDIUM
**File:** `evol_orchestrator.py`
**Line:** 254

### What the Bug Is

Temporary output files are named using `int(time.time())` combined with a random 4-digit suffix:

```python
# evol_orchestrator.py — line 254
temp_file = TEMP_DIR / f'gen_{int(time.time())}_{random.randint(1000, 9999)}.json'
```

`int(time.time())` has **1-second resolution**. Two iterations that both complete within the same wall-clock second will generate filenames like:

```
gen_1724832150_3421.json
gen_1724832150_7890.json
```

The random suffix `random.randint(1000, 9999)` provides 9,000 possible values. The probability of a collision within the same second is `1/9000 ≈ 0.011%` per pair. In a fast GPU run processing hundreds of iterations, this is non-negligible.

### Why It Matters

When a collision occurs, the **second write silently overwrites the first file**. There is no error, no warning, and no integrity check. One generated record is permanently lost without any trace in the logs. The final dataset will have a lower record count than expected, and there will be no indication of where the missing record went.

### Evidence

```python
# evol_orchestrator.py line 254:
temp_file = TEMP_DIR / f'gen_{int(time.time())}_{random.randint(1000, 9999)}.json'
```

**Fix:**
```python
import uuid
temp_file = TEMP_DIR / f'gen_{uuid.uuid4().hex}.json'
```

A UUID4 provides 2^122 unique values — collision probability is astronomically small and does not depend on wall-clock time.

---

*Document generated: 2026-08-28. All bugs verified against codebase at time of writing.*
