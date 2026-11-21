# DOC-02: Architectural Improvement Roadmap

> **Classification**: Engineering Architecture Decision Record (ADR)  
> **Scope**: Pipeline design, corpus strategy, tooling  
> **Date**: 2026-11-21  
> **Status**: Proposed

---

## Vision

Transform the Lumina PLC-LLM corpus from a **volume-first synthetic code dump** into a **precision-engineered, semantically validated, multi-modal training corpus** that reliably produces a domain-specific LLM capable of real industrial automation engineering assistance.

---

## Architectural Layer 1 — Corpus Governance & Schema

### Current State
870 flat JSON files in `data/swarm_raw/`. No schema enforcement, no metadata, no catalog.

### Target Architecture

```
data/
├── catalog/
│   └── corpus_index.jsonl         # One line per dataset, structured metadata
├── verified/                      # Passed full 3-stage validation
│   ├── automotive/
│   ├── electronics/
│   ├── semiconductor/
│   ├── plastics/
│   ├── foodbev/
│   ├── mechanical/
│   └── steelmaking/
├── quarantine/                    # Failed semantic validation, needs repair
├── rejected/                      # Non-target domain, too small, corrupted
└── raw/                           # Incoming (current swarm_raw location)
```

### Metadata Schema (per dataset)

```json
{
  "id": "agent_18c9a3b4",
  "schema_version": "2.0",
  "function_block": "FB_Automotive_Engine_ColdTest_Dyno_Sync",
  "sector": "automotive",
  "subsector": "powertrain_testing",
  "complexity_tier": 3,
  "char_count": 468842,
  "token_estimate": 117210,
  "generation": {
    "agent_version": "PlcDataEvolverV4",
    "persona": "V7_Max_75yr",
    "timestamp": "2026-11-20T14:15:00Z",
    "swarm_wave": 7
  },
  "validation": {
    "syntax_parity": true,
    "semantic_check": "pending",
    "physical_units": true,
    "domain_verified": true,
    "validator_version": "2.0"
  },
  "content_flags": {
    "has_tmr": true,
    "has_mpc": true,
    "has_state_machine": true,
    "has_kalman": true,
    "has_isa18_alarms": true,
    "fsm_stage_count": 14,
    "matrix_size": "12x12"
  }
}
```

### Implementation Steps
1. Write `scripts/build_corpus_index.py` — scan all 870 files, extract metadata, write `catalog/corpus_index.jsonl`
2. Write `scripts/triage_corpus.py` — classify each dataset into `verified/`, `quarantine/`, or `rejected/` by running 3-stage validation
3. Add pre-commit hook to enforce schema on all new dataset additions

---

## Architectural Layer 2 — Semantic Validation Pipeline

### Current State
`validate_iec.py` checks syntax parity only (IF/END_IF, CASE/END_CASE counts).

### Target: 3-Stage Validation Gate

#### Stage 1: Syntax (existing)
- Parity check (IF/END_IF, CASE/END_CASE, FOR/END_FOR, etc.)
- Minimum character count gate: **reject < 100,000 chars**
- Maximum character count gate: **warn if > 800,000 chars** (truncation risk in training)

#### Stage 2: Structural Semantics (new)
```python
# validate_semantic.py checks:
def check_var_declarations(st_code):
    """Every variable used in logic section must be declared in VAR/VAR_INPUT/VAR_OUTPUT"""

def check_matrix_dimensions(st_code):
    """Extract declared matrix sizes (A_12x12) and count element assignments"""

def check_fsm_completeness(st_code):
    """Count CASE state labels, verify all states have timeout guards"""

def check_mpc_horizon(st_code):
    """Count unrolled MPC iterations, verify >= 10 as declared"""

def check_no_deadlock_patterns(st_code):
    """Detect FSM states that have no transition out except error"""
```

#### Stage 3: Domain Verification (new)
```python
# validate_domain.py checks:
def verify_manufacturing_domain(fb_name, content):
    """Confirm FB targets one of the 7 approved sectors"""
    
def check_no_forbidden_keywords(content):
    """Reject if content contains: Marine, Subsea, Pharma, Defense, Sonar,
    Mining (non-metallic), LNG, FPSO, Power Grid, Lyophilizer"""
```

### New Validation Report Format
```
STAGE 1 SYNTAX: ✅ PASS (IF:843/843, CASE:2/2, chars:818,883)
STAGE 2 SEMANTIC: ⚠️ WARN (VAR declarations: 3 undeclared vars found)
STAGE 3 DOMAIN: ✅ PASS (automotive/heavy_metallurgy confirmed)
OVERALL: ⚠️ QUARANTINE (requires repair before training ingestion)
```

---

## Architectural Layer 3 — Swarm Orchestration Reform

### Current State
Coordinator spawns 8 subagents with slightly varied prompts. Agents operate independently. On quota exhaustion, agents fail silently and must be manually re-detected.

### Target: Stateful Orchestration Engine

#### 3.1 — Domain Rotation Scheduler
```python
class DomainScheduler:
    """
    Maintains a balanced queue of manufacturing subsectors.
    At any given time, maintains exact sector ratio:
    - Automotive: 25% (5 engines BIW / Powertrain / Paint / EV / Chassis)
    - Electronics: 15% (SMT / AXI / Reflow / Wave Solder)
    - Semiconductor: 15% (Wire Bond / Flip Chip / FOWLP / Dicing)
    - Heavy Machinery: 20% (CNC / Press / Forging / Die Casting)
    - Plastics: 10% (IM / Extrusion / Blow Mold / RTM)
    - Food & Beverage: 10% (Aseptic / Retort / Fill Seal / Pasteurize)
    - Steelmaking: 5% (EAF / BOF / Continuous Casting / Cold Mill)
    """
```

#### 3.2 — Quota-Aware Retry with Exponential Backoff
```python
class SwarmAgent:
    max_retries = 3
    backoff_base = 60  # seconds

    def on_quota_exhaustion(self):
        self.retry_count += 1
        wait = self.backoff_base * (2 ** self.retry_count)
        self.logger.warn(f"Agent {self.id} quota exhausted, sleeping {wait}s")
        # Persist agent state to disk before sleeping
        self.save_partial_progress()
```

#### 3.3 — Diversity Injector
Every new subagent receives a **prompt variation seed** that rotates through 8 instruction styles:
1. **Direct command**: "Implement `FB_X` for..."
2. **Engineering brief**: "System specification: [describe the physical plant]..."
3. **Problem statement**: "An EV battery pack line is experiencing [problem]. Design a PLC FB that..."
4. **Incremental extension**: "Here is an existing FB stub [stub]. Extend it to include full TMR voting..."
5. **Review request**: "Review this IEC-ST code and rewrite it with proper MPC and ISA-18.2 alarms..."
6. **Comparison task**: "Compare two control strategies for [system] and implement the superior one..."
7. **Fault scenario**: "During [fault condition], the existing control logic fails. Redesign it..."
8. **Commission question**: "What PLC code is needed to commission a new [machine] from cold start?"

---

## Architectural Layer 4 — Repository & CI/CD

### Current State
Manual git commits, no CI pipeline, no automated testing of datasets.

### Target CI/CD Pipeline

```yaml
# .github/workflows/corpus_validation.yml
name: Corpus Validation Gate
on:
  push:
    paths:
      - 'data/swarm_raw/*.json'
      - 'data/verified/**/*.json'

jobs:
  validate:
    steps:
      - run: python validate_iec.py --all data/swarm_raw/
      - run: python validate_semantic.py --all data/swarm_raw/
      - run: python validate_domain.py --all data/swarm_raw/
      - run: python scripts/build_corpus_index.py
      - run: python scripts/check_sector_balance.py --warn-if-imbalanced 10%

  size_report:
    steps:
      - run: python scripts/corpus_stats.py --output reports/corpus_health.json
```

---

## Architectural Layer 5 — Naming Convention Reform

### Current State
`agent_18c9a3b4.json` — UUID from agent ID, opaque.

### Target Convention
```
{sector}_{subsector}_{system}_{complexity}_{uuid8}.json

Example:
automotive_powertrain_engine_dyno_T3_18c9a3b4.json
electronics_smt_aoi_moire_T2_52d9a10c.json
steelmaking_hot_rolling_7stand_T3_8a391cb4.json
```

Where `T1`=simple (< 100K chars), `T2`=medium (100K–300K), `T3`=deep (300K+).

This allows CLI tools like `ls electronics_*/` to instantly surface all electronics datasets without loading JSON.

---

## Implementation Priority Queue

| Priority | Task | Effort | Impact |
|---|---|---|---|
| P0 | Write `validate_domain.py`, quarantine 176 off-target files | 2 hrs | Removes 20% contamination |
| P0 | Add minimum 100K char gate to `validate_iec.py`, quarantine 115 stubs | 1 hr | Removes weak training signal |
| P1 | Build `scripts/build_corpus_index.py` with full metadata schema | 4 hrs | Enables all downstream tooling |
| P1 | Implement `validate_semantic.py` Stage 2 checks | 1 day | Catches silent logical errors |
| P2 | Implement domain rotation scheduler in orchestrator | 4 hrs | Prevents future imbalance |
| P2 | Implement diversity injector with 8 instruction styles | 4 hrs | Breaks prompt homogeneity |
| P3 | Rename all dataset files to new convention | 2 hrs | Discoverability |
| P3 | Add GitHub Actions CI pipeline | 3 hrs | Automated quality gate |
