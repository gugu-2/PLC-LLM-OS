# DOC-01: Critical Path Analysis — Problems, Failures & Defects

> **Classification**: Project Post-Mortem & Quality Audit  
> **Scope**: Full codebase, pipeline architecture, and corpus health  
> **Date**: 2026-11-21  
> **Analyst**: Lumina Engineering Review Board

---

## Executive Summary

After 870 datasets and multiple swarm cycles, the Lumina PLC-LLM corpus exhibits seven categories of critical problems. Many of these are compounding: a weak prompt template produces a small dataset, which escapes validation because the parity checker is syntax-only, which then pollutes a fine-tuning run. Each failure path is documented below with root-cause analysis and severity classification.

---

## 1. Domain Contamination — 20.2% Off-Target Data

### What Happened
The swarm was originally instructed to generate datasets across **any industrial automation domain** (early waves). Later instructions restricted scope to 5 heavy manufacturing sectors. However, **176 out of 870 datasets (20.2%)** target domains outside the declared manufacturing focus:

| Contaminating Domain | Dataset Count |
|---|---|
| Marine / Subsea / LNG Shipping | 31 |
| Oil, Gas & Petrochemical Refining | 29 |
| Pharmaceutical / Biopharma / Lyophilization | 24 |
| Defense / Military / Sonar / Weapons | 18 |
| Power Generation / HRSG / Grid / Hydro | 21 |
| Mining & Mineral Processing | 17 |
| Data Centers / HVAC / Cooling | 14 |
| Other (Biogas, Civil, Railway, etc.) | 22 |

### Why It Happened
- Early agent prompts used vague persona language: *"any industrial automation sector"*
- No domain guardrail existed during swarm spawning — domain was chosen by the agent, not enforced by the orchestrator
- Quota exhaustion events caused agent re-spawning with stale or generic prompts, reverting to broad domain coverage

### Impact
A model fine-tuned on this corpus will hallucinate marine or pharmaceutical PLC code when asked for automotive manufacturing code. The domain confusion directly degrades task-specific accuracy.

### Severity: 🔴 CRITICAL

---

## 2. Extreme Size Variance — Corpus Incoherence

### What Happened
Dataset character counts range from **4,908** to **1,118,319** — a 228× spread. Distribution:

| Size Bucket | Count | % |
|---|---|---|
| < 50,000 chars (micro/incomplete) | 115 | 13.2% |
| 50,000 – 200,000 chars (acceptable) | 571 | 65.7% |
| 200,000 – 500,000 chars (deep) | 163 | 18.7% |
| 500,000 – 1,200,000 chars (ultra-dense) | 21 | 2.4% |

### Why It Happened
- Quota exhaustion mid-generation causes agents to submit partial or truncated Function Blocks
- Some early-generation agents (V1–V3 persona) were only instructed to produce 10,000–30,000 characters
- No **minimum character count gate** existed in `validate_iec.py` — parity checks pass even on 5,000-character stubs
- Ultra-dense 1M+ char datasets cannot be tokenized in a single training sequence (exceeds 256K context tokens for most fine-tuning frameworks)

### Impact
- Micro-datasets (< 50K chars) teach nothing about deep control logic — they represent system header boilerplate only
- Ultra-dense datasets cannot fit in a training window without truncation, causing context mid-block loss which produces malformed training signal
- The model learns wildly inconsistent output length expectations

### Severity: 🔴 CRITICAL

---

## 3. Prompt Template Homogeneity — 46.7% Share One Template

### What Happened
406 of 870 datasets (46.7%) were generated from the **exact same prompt template opening**: *"You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data..."*

The user-side of the training pair carries **almost no semantic variety**:
- Same persona phrasing
- Same instruction ordering
- Same required subsystem list (TMR, MPC, FSM, ISA-18.2)
- Only the `FUNCTION_BLOCK` name and sector tag differ

### Why It Happened
- The orchestrator recycled the same `PlcDataEvolverV4` prompt template for all agents in later waves
- No prompt diversity system (paraphrase injection, perspective switching, task decomposition) was implemented
- User messages are essentially labels, not questions — they carry no conversational intent

### Impact
During fine-tuning, the model learns that **this exact prompt text → IEC-ST code**. It will fail to generalize to:
- Different instruction phrasings
- Real user queries ("How do I implement MPC in a hot strip mill?")
- Multi-turn debugging conversations
- Explanation-first vs. code-first responses

### Severity: 🟠 HIGH

---

## 4. Single-Turn Only — Zero Conversational or Diagnostic Data

### What Happened
Every dataset in the corpus is **exactly 2 messages**: one user prompt, one assistant code block. There is no:
- Multi-turn debugging conversation
- Error explanation followed by correction
- Code review exchange
- Incremental modification of an existing Function Block
- Question-answering about a generated block

### Why It Happened
- The swarm was optimized for token-volume throughput, not conversational utility
- 1-Agent = 1-Dataset lifecycle enforcement prevented any multi-turn accumulation
- No second-pass "reflection" or "critique" agent was designed

### Impact
A model fine-tuned only on this corpus will be a **code emission machine**, not an automation engineering assistant. It will not be able to:
- Explain why it made a design choice
- Debug a provided code snippet
- Answer "what does this FSM stage do?"
- Engage in iterative design refinement

### Severity: 🟠 HIGH

---

## 5. Synthetic-Only Ground Truth — Zero Real-World Anchor

### What Happened
100% of the 870 datasets were generated by LLMs impersonating automation engineers. No datasets were sourced from:
- Real PLC project archives
- IEC 61131-3 standard body examples
- Academic publications with verified code
- Open-source industrial automation repositories (e.g., `tc-open`, `OSCAT`)

### Why It Happened
- Real PLC code is largely proprietary (Siemens, Rockwell, Beckhoff)
- The project strategy relied on synthetic generation as a shortcut to corpus scale
- No data licensing or procurement budget was established

### Impact
The corpus has **no calibration point**. Mathematically rigorous-looking code may contain:
- Physically impossible state-space matrices (non-controllable, non-observable systems)
- MPC cost functions with negative definite Q matrices (unconditionally unstable)
- TMR logic that votes incorrectly under specific sensor failure patterns
- FSM transitions that create deadlocks under fault conditions

The validator (`validate_iec.py`) checks **syntax only** — it cannot catch semantic errors. The model will learn to produce syntactically valid but potentially incorrect control logic.

### Severity: 🟠 HIGH

---

## 6. Missing Semantic Validation Layer

### What Happened
`validate_iec.py` checks:
- `IF` / `END_IF` count parity
- `CASE` / `END_CASE` count parity
- `FOR` / `END_FOR` count parity
- `FUNCTION_BLOCK` / `END_FUNCTION_BLOCK` count parity
- Character count

It does **not** check:
- Variable declaration completeness (every used variable declared in `VAR` blocks)
- Matrix dimension consistency (A is 12×12 but only 6×6 elements written)
- State machine reachability (all 14 states have entry transitions)
- MPC horizon validity (N=10 unrolled but only 5 iterations present in code)
- Physical unit dimensional consistency ([m/s] ÷ [m] ≠ [s])
- Duplicate variable names
- Circular FSM transitions (state A → state B → state A with no break condition)

### Impact
Datasets pass validation but contain semantic errors. The model learns incorrect engineering patterns as valid training signal.

### Severity: 🟠 HIGH

---

## 7. Corpus Organization & Metadata Poverty

### What Happened
All 870 datasets are stored as flat JSON files in `data/swarm_raw/` with UUID-derived filenames (`agent_<8hex>.json`). There is:
- No index or catalog
- No sector tag in the filename
- No metadata sidecar (sector, complexity tier, character count, generation date, agent ID, validator version)
- No versioning of individual datasets
- No cross-reference between datasets covering related systems (e.g., all automotive BIW datasets)

### Why It Happened
- Pipeline was optimized for throughput, not future discoverability
- No schema design was done before generation began

### Impact
- Fine-tuning pipelines must re-parse all 870 JSON files to filter, split, or weight the dataset
- Cannot perform curriculum learning (easy → complex) without re-scanning character counts
- Cannot build retrieval-augmented systems without knowing what each dataset covers
- Impossible to audit for coverage gaps without ad-hoc scripting

### Severity: 🟡 MEDIUM

---

## Summary Severity Matrix

| # | Problem | Severity | Datasets Affected |
|---|---|---|---|
| 1 | Domain contamination (20.2% off-target) | 🔴 CRITICAL | 176 |
| 2 | Extreme size variance (13.2% micro/incomplete) | 🔴 CRITICAL | 115 |
| 3 | Prompt template homogeneity (46.7% identical) | 🟠 HIGH | 406 |
| 4 | Single-turn only, no conversation data | 🟠 HIGH | 870 |
| 5 | Synthetic-only, no real-world anchor | 🟠 HIGH | 870 |
| 6 | Syntax-only validation, no semantic check | 🟠 HIGH | 870 |
| 7 | Corpus metadata poverty, no indexing | 🟡 MEDIUM | 870 |
