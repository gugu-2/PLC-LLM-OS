# Deep Technical Audit: Dataset Errors, Syntax Parity & Schema Anomalies

**Audit Date**: November 1, 2026  
**Auditor**: Lumina Cyber-Physical Systems & Automation Architecture Team  
**Scope**: All synthetic datasets in `data/swarm_raw/`, master splits in `data/master/`, and legacy `.jsonl` repositories in `data/` and `Local_Ollama_Evol_Pipeline/data/`.

---

## 1. Executive Summary: Dataset Health Matrix

| Dataset Category | Total Records Analyzed | Valid Records | Corrupt / Anomalous | Pass Rate | Primary Failure Modes |
|---|---|---|---|---|---|
| **Swarm Raw Datasets (`data/swarm_raw/*.json`)** | 429 | 378 (AST perfect) | **51** (11 syntax, 40 unit warnings) | 88.1% (strict) / 97.4% (structural) | Parity mismatch (FOR/IF), truncated headers, missing unit annotations |
| **Legacy Enterprise JSONL (`synthetic_generation_v3_enterprise.jsonl`)** | 289 | 169 | **120** | **58.5%** | Malformed JSON strings, unescaped newlines, broken brackets |
| **Evol-Instruct Baseline (`evol_instruct_dataset.jsonl`)** | 1,645 | 1,632 | **13** | 99.2% | JSON delimiter errors, unexpected EOF |
| **Curated Legacy Logic (`final_verified_dataset.jsonl`)** | 5,928 | 5,919 | **9** | 99.8% | `Extra data` at line endings, broken delimiter |
| **Verified OSCAT Library (`verified_oscat.jsonl`)** | 363 | 363 (Valid JSON) | **363 dropped by builder** | **0.0% pipeline utilization** | Hardcoded 1,500-char threshold rejects standard concise industrial logic |
| **Local Pipeline Data (`Local_Ollama_Evol_Pipeline/data/*.jsonl`)** | 35 | 27 | **8** | 77.1% | JSON serialization errors during Ollama stream capture |

---

## 2. Critical Finding: The 11 Syntax-Corrupted Datasets in `data/swarm_raw/`

During exhaustive Abstract Syntax Tree (AST) parity verification using `validate_iec.py`, **11 specific swarm-generated datasets** were identified with real syntax or structure parity violations. These occurred primarily during earlier swarm pulses before strict deterministic parity gates were enforced:

### Detailed Breakdown of the 11 Defective Files:

```text
1. data/swarm_raw/agent_24d49626.json
   - Defect: FOR loop parity mismatch. Contains 7 FOR statements, but 0 END_FOR statements.
   - Root Cause: Agent generated nested matrix iterations without closing blocks before token limit.

2. data/swarm_raw/agent_34034682.json
   - Defect: Header truncation. File begins abruptly with "VAR_INPUT", missing the mandatory "FUNCTION_BLOCK FB_<Name>" declaration.
   - Last Line Mismatch: Contains trailing markdown fences "\n```" instead of "END_FUNCTION_BLOCK".
   - FUNCTION_BLOCK count: 0 (Declaration missing).

3. data/swarm_raw/agent_3df981b7.json
   - Defect: Multiple parity violations.
     * IF: 65 vs END_IF: 64 (Unclosed IF block).
     * FOR: 20 vs END_FOR: 13 (7 unclosed FOR loops in state propagation).

4. data/swarm_raw/agent_865ca322.json
   - Defect: FOR loop parity mismatch. Contains 6 FOR statements, but 0 END_FOR statements.

5. data/swarm_raw/agent_88be15b6.json
   - Defect: Dual parity mismatch.
     * IF: 12 vs END_IF: 11.
     * FOR: 5 vs END_FOR: 0.

6. data/swarm_raw/agent_8efa91e3.json
   - Defect: Unbalanced comment delimiters.
     * (* count: 430 vs *) count: 431. Causes IEC compiler parser crash on orphan comment termination.

7. data/swarm_raw/agent_9cbbf0a3.json
   - Defect: Unbalanced comment delimiters.
     * (* count: 454 vs *) count: 452 (2 unclosed multiline comments).

8. data/swarm_raw/agent_c67fd469.json
   - Defect: Header truncation. Starts at "VAR_INPUT", missing "FUNCTION_BLOCK FB_<Name>".
   - Last Line Mismatch: Trailing backtick artifacts.

9. data/swarm_raw/agent_ca5e1383.json
   - Defect: FOR loop parity mismatch. Contains 7 FOR statements, 0 END_FOR statements.

10. data/swarm_raw/agent_d9d63fe7.json
    - Defect: Severe block parity imbalance.
      * IF: 15 vs END_IF: 12 (3 unclosed conditional blocks).
      * FOR: 6 vs END_FOR: 0 (6 unclosed loop blocks).

11. data/swarm_raw/agent_dae496dd.json
    - Defect: FOR loop parity mismatch. Contains 1 FOR statement, 0 END_FOR statement.
```

> [!WARNING]
> **Action Required**: These 11 datasets must either be:
> 1. Patched with an automated regex/AST repair script (`repair_iec_parity.py`).
> 2. Regenerated using the latest `SyntheticDataEvolverV3` persona with strict AST validation.
> 3. Quarantined to `data/swarm_quarantine/` so they do not contaminate the PyTorch training split.

---

## 3. Aggregation Pipeline Bug: False-Positive LLM Refusal Gate

In `pipeline/tools/build_master_dataset.py`, lines 58-61 define:
```python
REFUSAL_PHRASES = [
    "cannot provide", "cannot fulfill", "must decline",
    "safety guidelines", "i cannot", "not able to provide actionable"
]
```

### The Bug:
In industrial automation, high-reliability control code (SIL 3, ISO 13849, IEC 61508) frequently includes comments referencing **"safety guidelines"**, such as:
`(* Emergency shutdown executed in accordance with plant safety guidelines *)`

Because `"safety guidelines"` is included as a refusal phrase, `build_master_dataset.py` dropped **`agent_fa9cce23.json`** (EV Battery Calendering Controller, 71,164 chars, 100% AST valid) with `loaded 0, skipped 1`.

### Remediation:
Update `REFUSAL_PHRASES` to check conversational refusal patterns rather than generic engineering terms:
```python
REFUSAL_PHRASES = [
    "i cannot provide", "i cannot fulfill", "i must decline",
    "as an ai", "against my safety guidelines", "i am unable to generate"
]
```

---

## 4. Pipeline Bias: Complete Rejection of OSCAT Industrial Standard Library

In `pipeline/tools/build_master_dataset.py`, line 57 enforces:
```python
MIN_ASSISTANT_LENGTH = 1500  # chars
```

### The Problem:
`data/verified_oscat.jsonl` contains 363 verified industrial function blocks from the open-source OSCAT library (e.g., `DRIVER_1`, `DRIVER_4`, `FILTER_I`, `TIMER_P`). These blocks are mathematically verified, deterministic, and widely used across Siemens, CODESYS, and Beckhoff PLCs.
However, because standard single-purpose utility blocks naturally range between 800 and 1,400 characters, **100% of all 363 OSCAT records were rejected during the master build**:
```text
Loading: verified_oscat.jsonl
verified_oscat.jsonl: loaded 0, skipped 363
```

### Remediation:
Implement tiered length thresholds:
- Tier 1 (Ultra-complex plant controllers): `MIN_LENGTH = 1500`
- Tier 2 (Standard industrial library functions & drivers): `MIN_LENGTH = 300` if `verified_oscat` or `verified_github`.

---

## 5. Corrupted Lines in Legacy Training Datasets

### 1. `data/synthetic_generation_v3_enterprise.jsonl`
- **Total Lines**: 289
- **Corrupt Lines**: **120 (41.5%)**
- **Symptoms**: Lines contain unescaped raw newlines embedded within JSON string values, causing `json.loads` to terminate with `Unterminated string` or `Extra data`.
- **Mitigation Status**: `synthetic_generation_v3_enterprise_CLEAN.jsonl` was generated to recover 247 clean lines, but the corrupted master file still sits in the main `data/` directory and is repeatedly processed by tools.

### 2. `data/final_verified_dataset.jsonl`
- **Total Lines**: 5,928
- **Corrupt Lines**: **9** (Lines 263, 349, 595, 701, 816, etc.)
- **Error**: `json.decoder.JSONDecodeError: Extra data: line 1 column 2194`
- **Root Cause**: Two JSON objects concatenated on the same line without a newline separator.

### 3. `data/evol_instruct_dataset.jsonl`
- **Total Lines**: 1,645
- **Corrupt Lines**: **13**
- **Error**: Broken delimiters and truncated JSON payloads from interrupted scraper runs.

---

## 6. Heuristic Warning: Physical Engineering Unit Density

In `validate_iec.py`:
```python
bracket_units = re.findall(r'\[[a-zA-Z0-9/%^°\-_ ]+\]', code_text)
if len(bracket_units) < 5:
    errors.append(f"Too few physical units found in comments ({len(bracket_units)} found, expected at least 5)")
```
- **43 swarm datasets** were flagged because their variable comments used plain text (e.g., `// Temperature in deg C`, `// Pressure bar`) rather than bracketed format `[deg C]`, `[bar]`.
- **Verdict**: Non-critical heuristic warning. The ST code itself is syntactically sound, but lacks standardized bracketed notation.
