# Dataset Readiness Audit — Fine-Tuning Perspective
*Audited: 2026-08-28 | File: `data/master/train.jsonl` (990 records)*

---

## The Core Problem in One Sentence

The master training dataset was built to **be valid JSON** but not to **produce a consistent, high-quality fine-tuned model**.

---

## Issue 1: Format Inconsistency (Most Critical for Training)

The plan's #1 stated goal was consistent output format. The dataset fails it.

```
Verification run on data/master/train.jsonl (990 records):
─────────────────────────────────────────────────────────
Records with ` ```iec-st ` or ` ```st ` code fence:    210  (21.2%)
Records with raw code only, NO fence:                  780  (78.8%)
```

**What the model will learn:** Two completely different things. Sometimes it will see a response that looks like:
```
FUNCTION_BLOCK FB_Reactor
VAR_INPUT ...
```
And sometimes it will see:
```
Here is the code:
` ```iec-st `
FUNCTION_BLOCK FB_Reactor
VAR_INPUT ...
` ``` `
```

A fine-tuned LLM trained on this will randomly produce either format, with no consistency. This is unusable for a production coding assistant.

**Source of the problem:** The dominant data source (`evol_instruct_dataset.jsonl`, contributing 790/990 records = 79.8%) uses raw code format. This was never normalized.

---

## Issue 2: Quality Bar — 62% of Records Below Original Threshold

The plan's original quality bar was **3,000 chars minimum** (described as the minimum for a "meaningful, non-trivial response").

```
Records under 3,000 chars in train.jsonl: 616 out of 990 (62.2%)
Records under 1,500 chars in train.jsonl: 0   out of 990 (but linter allows 1,500)
```

The implemented linter uses 1,500 chars. The plan specified 3,000.

**Distribution estimate:**
- `evol_instruct_dataset.jsonl` avg: ~1,665 chars (many short records)
- `verified_oscat.jsonl` avg: ~943 chars (all short)
- `synthetic_generation_v3_enterprise_CLEAN.jsonl` avg: ~10,799 chars (excellent)

The ~247 high-quality swarm records are being diluted in a pool of ~743 short, raw-format records.

---

## Issue 3: The Big Dataset Was Left Out

The largest and potentially richest dataset in the project was not included in the master.

| Dataset | Records | Avg Length | Included in Master? |
|---|---|---|---|
| `final_verified_dataset.jsonl` | 5,919 | 1,517 chars | ❌ Not included |
| `evol_instruct_dataset.jsonl` | 1,632 | 1,665 chars | ✅ 790 records |
| `synthetic_generation_v3_enterprise_CLEAN.jsonl` | 247 | 10,799 chars | ✅ 247 records |

`final_verified_dataset.jsonl` contributes 0 records to the master. It has 99.8% valid records (only 9 parse errors), 0 refusals, and 5,919 usable records. Its origin/format is unknown, but it is the largest TIER_1 file. Whether it should be included requires examination — but it was silently excluded from `APPROVED_SOURCES` without explanation.

---

## Issue 4: `github_raw_code.jsonl` Was Mislabeled and Could Contaminate Seeds

The file `github_raw_code.jsonl` was rated **TIER_1** in `DATA_CATALOG.md`.

**Actual IEC 61131-3 content check:**
- Records with `FUNCTION_BLOCK`: **19 / 400 (4.75%)**
- Records with `VAR_INPUT`/`VAR_OUTPUT`: **17 / 400 (4.25%)**

This is raw scraped GitHub code. The vast majority of its records are partial code snippets, non-ST code, README text, or code fragments. It is not safe for fine-tuning — but `DATA_CATALOG.md` says it is.

Additionally, a copy of this type of data (`github_bulk_v3_2186.jsonl`, 3.7 MB) lives inside `Local_Ollama_Evol_Pipeline/seeds/tier3_bulk_github/` — the tier3 seed bank the local orchestrator uses for few-shot RAG context. The local model's few-shot examples include unverified bulk-scraped code.

---

## Quick Reference: What Is Actually in the Master

```
data/master/train.jsonl  (990 records)
├── 247 records — swarm-generated V3 (avg ~10,799 chars, fully fenced ✅)
├── 790 records — evol_instruct baseline (avg ~1,665 chars, 97% raw format ⚠️)
├──  14 records — verified_github (avg ~6,523 chars, mostly raw ⚠️)
└──  51 records — verified_oscat (avg ~943 chars, raw ⚠️)
```

The 247 swarm records are the only records that meet:
- ✅ Code fence format
- ✅ High average length (>3000 chars)
- ✅ Consistent FUNCTION_BLOCK + VAR_INPUT/OUTPUT structure

Everything else is a compromise.

---

## Fine-Tuning Risk Assessment

| Risk | Level | Description |
|---|---|---|
| Model outputs inconsistent format | 🔴 HIGH | 79% training data has no code fence |
| Model outputs short/trivial code | 🟠 MEDIUM | 62% records under 3000 chars |
| Model confuses raw code vs. markdown | 🔴 HIGH | Two formats mixed without separation |
| Training data has contaminated GitHub raw code in seeds | 🟡 LOW | Affects few-shot quality, not direct training |
| `final_verified_dataset.jsonl` excluded from training | 🟠 MEDIUM | 5,919 records of unknown quality not leveraged |
