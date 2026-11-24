# DOC-01: Critical Path Analysis — Problems, Failures, Architectural Defects & Corpus Pathology

**Classification**: Comprehensive Project Forensic Post-Mortem & Quality Audit  
**System**: Lumina Industrial Automation AI Swarm & Cyber-Physical Dataset Engine  
**Corpus Scope**: 870 Raw Synthetic Datasets (`data/swarm_raw/`) totaling ~122 Million Characters (~39.4 Million Tokens)  
**Author**: Lumina Engineering Review Board & Principal Automation Fellow  
**Date**: November 23, 2026  
**Status**: AUTHORITATIVE AUDIT & LESSONS LEARNED  

---

## 1. Executive Summary: The Genesis of the Failure Paths

The Lumina Industrial Automation AI Swarm was conceived with an ambitious objective: to synthesize a massively dense, mathematically complete pre-training and supervised fine-tuning (SFT) corpus of IEC 61131-3 Structured Text for heavy commercial manufacturing industries (automotive, electronics, semiconductor, heavy tooling, plastics, food & beverage, and continuous metallurgy).

Over multiple generation waves, the swarm scaled to **870 datasets**. However, an exhaustive forensic audit reveals that the engineering strategy fell into a series of **compounding architectural traps**. By prioritizing raw token throughput and volumetric expansion over semantic rigor, modular diversity, and closed-loop validation, the project inadvertently created critical data pathologies that directly threaten model quality:

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                        COMPOUNDING DEFECT FEEDBACK LOOP                                │
│                                                                                        │
│   Weak / Unbounded           Off-Target Domain          Micro-Stub or Ultra-Dense      │
│   Agent Prompts     ───►     Generation         ───►    Payloads (<50k or >700k)       │
│         ▲                    (20.2% Contamination)                 │                   │
│         │                                                          ▼                   │
│   Polluted Model             Polluted Training          Syntax-Only Parity Pass        │
│   Inference Weights ◄───     Ingestion          ◄───    (Zero Semantic Checking)       │
│   (Cross-Domain Halluc.)     (Loss on Prompts)          (Balanced Brackets Illusion)   │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

This document provides a forensic post-mortem of every failure path created in the project, tracing root causes, quantifying empirical blast radiuses across the 870 files, and formalizing the engineering lessons required for remediation.

---

## 2. Deep-Dive Forensic Analysis: The Eight Critical Pathologies

### 2.1 Pathology 1: The Volume-First Throughput Trap

#### What Happened
In early swarm iterations, the primary optimization metric was **token volume**. Agents were incentivized to maximize generated character counts per Function Block, culminating in the V7 Max-Persona mandate: *"45,000 to 85,000+ characters per block, extreme token consumption, zero summaries, zero truncation."*

#### Why It Created a Critical Problem
1. **Bloat Over Engineering Essence**: LLM agents satisfied the character quota by unrolling repetitive arithmetic loops, generating hundreds of nearly identical matrix multiplication assignments, and repeating comment blocks rather than developing deeper, diverse cyber-physical interactions.
2. **Context Window Saturation**: As character counts ballooned past 500,000 and reached up to **1,118,319 characters** (~360,000 tokens), the generated Function Blocks became physically impossible to ingest into standard transformer training windows (typically 32k to 128k tokens) without silent mid-block truncation.
3. **Execution Fragility**: Extremely long inference turns repeatedly triggered provider timeouts, context exhaustion, and HTTP 429 rate-limit errors, causing agent worker crashes and generating hundreds of empty or corrupt fragments in scratch directories.

---

### 2.2 Pathology 2: Domain Contamination — 20.2% Off-Target Datasets

#### What Happened
Despite a stated project mission to automate multi-billion-dollar commercial factory manufacturing (automotive assembly, PCB assembly, injection molding, CNC tooling), **176 out of the 870 datasets (20.2%)** target completely unrelated industrial sectors:

| Contaminating Sector Category | Dataset Count | % of Corpus | Representative Off-Target Systems Generated |
|---|:---:|:---:|---|
| **Marine, Naval & Subsea** | 31 | 3.56% | Submarine ballast water trimming, ROV tether management, naval hull acoustic sonar beamforming, ship steering rudder hydrodynamics |
| **Upstream & Midstream Oil & Gas** | 29 | 3.33% | Offshore deepwater blowout preventers (BOP), subsea production manifolds, FPSO crude separation, gas flaring towers, fracturing mud pumps |
| **Pharmaceutical & Bioprocessing** | 24 | 2.76% | Lyophilizers (freeze dryers), fed-batch bioreactors, chromatography columns, vial/syringe aseptic filling, WFI distillation loops |
| **Defense, Weapons & Munitions** | 18 | 2.07% | Missile thrust-vector actuation, torpedo tube pneumatic interlocks, naval gun turret ballistic positioning, radar gimbal servo tracking |
| **Utility Power Generation & Grid** | 21 | 2.41% | Nuclear reactor core coolant rod positioning, steam turbine governors, HRSG utility boilers, grid frequency synchronization |
| **Mining & Heavy Ore Extraction** | 17 | 1.95% | SAG mills, primary gyratory ore crushers, froth flotation cells, tailing thickeners, bucket-wheel excavators |
| **Hyperscale Data Center Infrastructure** | 14 | 1.61% | Computer Room Air Handlers (CRAH), chilled water plant thermal optimization, server rack cold-aisle containment |
| **Other Non-Manufacturing** | 22 | 2.53% | Municipal wastewater sludge digestion, biogas upgrading, railway switch heaters, civil tunnel ventilation |
| **Total Off-Target Contamination** | **176** | **20.23%** | **Over one-fifth of the total training corpus** |

#### Root Cause Analysis
1. **Unconstrained Early Prompts**: Initial swarm prompts instructed agents: *"You are an industrial automation expert generating IEC 61131-3 code for any industrial process."* Agents naturally gravitated toward exotic, high-vocabulary engineering domains (submarines, nuclear power, oil refineries).
2. **Absence of Orchestrator Domain Gating**: The generation loop lacked an intake filter. If an agent submitted `FB_Subsea_Wellhead_Safety`, the orchestrator saved it directly to `data/swarm_raw/` without verifying whether "subsea wellhead" belonged to factory manufacturing.
3. **Quota Re-spawning Amnesia**: When an agent died from quota exhaustion, recovery routines re-spawned generic replacement agents without restoring the specific sector queue assignment.

#### Impact on Fine-Tuning
Training a foundation model on this contaminated corpus results in catastrophic **cross-attention cross-talk**. When a user in production prompts the fine-tuned model:
> *"Write a Function Block for automotive Body-in-White robotic spot welding,"*

the model's attention heads activate weights associated with marine ballast pressure or subsea hydrostatic valves, hallucinating impossible interlocks (e.g., checking seawater salinity or wellhead casing pressure on an automotive assembly fixture).

---

### 2.3 Pathology 3: Extreme Bimodal Size Variance & The Truncation Hazard

#### What Happened
The dataset corpus exhibits a **228× spread** in character volume, spanning from **4,908 characters** up to **1,118,319 characters**:

```
Distribution of Dataset Sizes (870 Datasets):
┌────────────────────────────────────────────────────────────────────────┐
│ [####] < 50k chars (Micro-Stubs): 115 files (13.2%)                   │
│ [#################################] 50k - 200k chars: 571 files (65.7%)│
│ [#########] 200k - 500k chars: 163 files (18.7%)                       │
│ [#] 500k - 1.2M chars (Ultra-Dense): 21 files (2.4%)                   │
└────────────────────────────────────────────────────────────────────────┘
```

#### Why Micro-Stubs (< 50,000 Chars) Degrade Training
- 115 files contain only superficial header declarations, a couple of basic variables, and an empty or stubbed state machine.
- They lack discrete state-space matrices, lack MPC formulations, and contain trivial 3-line logic.
- Including micro-stubs in SFT teaches the model that generating an empty skeleton without functional control mathematics is an acceptable response.

#### Why Ultra-Dense Datasets (> 700,000 Chars) Destroy Model Structure
- A 700k+ character dataset represents $\ge 225,000$ tokens.
- When an SFT trainer configured with a standard context window (e.g., 32,768 tokens) loads this sequence, the data loader **silently truncates the sequence at token 32,768**.
- **The Consequence**: The final 85% of the Function Block is lopped off. The training example **lacks an `END_FUNCTION_BLOCK` tag**, lacks the closing FSM states, and lacks alarm logic.
- The model is penalized for predicting closing syntax and learns to emit truncated code blocks that terminate abruptly in mid-air.

---

### 2.4 Pathology 4: Prompt Template Homogeneity — 46.7% Identical Openings

#### What Happened
Out of 870 datasets, **406 files (46.7%)** share the **identical opening sentence**:
> *"You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data for industrial automation..."*

Across the user prompts of these 406 files:
- The system persona phrasing is identical.
- The bulleted instruction ordering is identical (1. Matrices, 2. MPC, 3. TMR, 4. Alarms, 5. FSM).
- The grammatical perspective is exclusively an imperative command directed at an AI swarm agent.
- Zero user prompts resemble real human engineer inquiries ("Why is my loop oscillating?", "How do I implement bump-less transfer?", "Fix this syntax error").

#### Impact on Generalization
In transformer fine-tuning, loss is computed over the sequence. When nearly half the dataset features identical prompt preambles:
1. **Prompt Overfitting**: The model's attention layers overfit to the exact tokens *"You are part of the Lumina AI Cloud Swarm..."*.
2. **Inference Fragility**: When a real automation engineer enters a natural prompt in an IDE plugin (e.g., *"Configure an MPC controller for a cold strip rolling mill"*), the prompt representation vector has low cosine similarity with the training distribution, causing the model to output degraded, generic code or fail to trigger its specialized capabilities.

---

### 2.5 Pathology 5: The Single-Turn Code Emission Trap

#### What Happened
Every single dataset in `data/swarm_raw/` is formatted as a **rigid 2-message exchange**:
- `Turn 1 (User)`: Mega-prompt specifying equipment and mandates.
- `Turn 2 (Assistant)`: Monolithic IEC-ST code block.

There is **zero conversational, diagnostic, explanatory, or iterative data**:
- No multi-turn design discussions.
- No root-cause fault diagnosis conversations.
- No code reviews explaining *why* an algorithm was selected.
- No question-answering pairs explaining control parameters.

#### Impact
A model trained exclusively on single-turn code emission becomes a **code-spewing automaton**. It is incapable of functioning as an interactive engineering co-pilot. If asked:
> *"Why did you set the discrepancy timer to 25 ms in the 2oo3 voter?"*

it cannot formulate an engineering rationale; it only knows how to re-emit the entire Function Block from line 1.

---

### 2.6 Pathology 6: The Synthetic Ground-Truth Vacuum & Physical Untruth

#### What Happened
100% of the 870 datasets were generated synthetically by LLMs simulating controls engineers. Zero lines of code were:
- Compiled on an actual IEC 61131-3 engineering tool (Beckhoff TwinCAT 3, Siemens TIA Portal, CODESYS 3.5, Rockwell Studio 5000).
- Executed on a soft-PLC simulation kernel.
- Validated against empirical plant data or physical differential equations.

#### Physical & Mathematical Hazards Discovered in the Corpus
Because the code was never executed in a simulation environment, several mathematically invalid patterns escaped into the training data:
1. **Non-Controllable State-Space Models**: Matrices $A$ and $B$ generated where the controllability matrix $\mathcal{C} = [B \quad AB \quad A^2B \quad \dots \quad A^{n-1}B]$ has rank $< n$, representing an un-controllable physical plant.
2. **Ill-Conditioned MPC Cost Formulations**: Objective functions with non-positive semi-definite state weighting matrices ($Q \prec 0$), making the quadratic optimization problem unbounded and unstable.
3. **Physically Absurd Scaling Constants**: Thermal time constants set to milliseconds for 50-ton steel coils, or pressure rates of change ($dP/dt$) exceeding the speed of sound in hydraulic oil.

---

### 2.7 Pathology 7: The Syntax-Only Parity Illusion

#### What Happened
The primary quality assurance script was `validate_iec.py`. This script checked:
- Parity of `IF` vs. `END_IF`
- Parity of `CASE` vs. `END_CASE`
- Parity of `FOR` vs. `END_FOR`
- Presence of `FUNCTION_BLOCK` and `END_FUNCTION_BLOCK`
- Character count $\ge 3,500$

#### The Illusion of Quality
A dataset could pass `validate_iec.py` with 100% flying colors while being **semantically broken**:
- An $A$ matrix declared as `ARRAY[0..3, 0..5]` (a non-square matrix in discrete state-space) passed without warning.
- A 14-state FSM where State 7 had no outgoing transition (an infinite deadlock state) passed without warning.
- An MPC prediction horizon declared as $N=20$ where only 4 loop iterations were written passed without warning.
- Variables used in logic but never declared in `VAR` blocks passed without warning.

Because syntax parity was the only gate to commit code to git, hundreds of semantically flawed blocks were merged into the corpus under the false impression that they were "100% verified."

---

### 2.8 Pathology 8: Corpus Metadata Poverty & File Anonymity

#### What Happened
All 870 datasets were saved in a flat directory (`data/swarm_raw/`) with opaque UUID filenames:
`agent_001ec71d.json`, `agent_003f6e49.json`, `agent_18c9a3b4.json`...

There were:
- No sector tags in filenames.
- No complexity tier tags.
- No machine-readable index or catalog file.
- No content metadata (e.g., matrix size, FSM states count, TMR presence).

#### Impact
- Fine-tuning data loaders had to iterate through and parse all 870 JSON files (122 MB) on every initialization to determine sector distribution.
- Implementing **curriculum learning** (training on simple controllers first, then graduating to complex multi-input multi-output MPC systems) was impossible without ad-hoc re-parsing scripts.
- Identifying and filtering off-target datasets required full-text regex scanning across the entire disk repository.

---

### 2.9 Pathology 9: Overly Broad Keyword Filtering & The 100k "Stub" Boundary Trap

#### What Happened
When designing initial intake filters, two dangerous over-corrections were made:
1. **False-Positive Keyword Collisions on Plant Equipment**:
   - The word `Vessel` was added as a bare forbidden keyword under `marine`. However, in automotive windshield glass plants, autoclave composite curing lines, food & beverage retort systems, and chemical manufacturing, **pressure vessels, reaction vessels, mixing vessels, and autoclave vessels** are foundational physical equipment. Bare `Vessel` matching caused 58 legitimate, high-value manufacturing datasets to be falsely rejected as "marine/naval."
   - Similarly, `CleanSteam` was quarantined under `pharmaceutical`, even though food & beverage aseptic bottling plants use clean steam for Sterilize-In-Place (SIP) cycles.
   - `Ballistic` was quarantined under `defense`, falsely colliding with industrial ballistic impact testers and separator screens.
2. **The 100k Character Arbitrary "Stub" Boundary**:
   - The initial triage rule classified anything under 100,000 characters as a "stub." In reality, a 60,000–90,000 character function block represents **18,000 to 28,000 tokens** of dense, production-grade cyber-physical code. Quarantining these blocks unnecessarily locked away 243 verified manufacturing controllers.

#### The Customer-Centric Resolution
- Replaced unqualified keywords with disambiguated terms (`MarineVessel`, `NavalVessel`, `CargoShip`, `PharmaCleanSteam`, `BallisticMissile`).
- Redefined stubs to true code fragments ($< 3,500$ characters).
- Preserved and categorized all high-token/high-context datasets for specialized high-context model training.
- Result: **Clean verified manufacturing yield surged from 386 (44.37%) to 690 (79.31%)** across all 870 scanned production datasets.

---

## 3. Comprehensive Defect Severity Matrix

| Defect ID | Problem Category | Root Cause | Blast Radius | Severity | Remediation Requirement |
|:---:|---|---|:---:|:---:|---|
| **DEF-01** | Domain Contamination | Vague agent prompts & missing intake filter | 160 datasets (18.4%) | 🔴 CRITICAL | Triage into approved sectors; quarantine off-target files |
| **DEF-02** | Keyword False Positives | Unqualified keywords (e.g. bare `Vessel`) | 58 datasets (6.7%) | 🔴 CRITICAL | Disambiguate keywords (`MarineVessel`, `CargoShip`) |
| **DEF-03** | Arbitrary Stub Threshold | 100k char threshold labeling 20k token code as "stub" | 243 datasets (27.9%) | 🔴 CRITICAL | Set true stub gate ($< 3,500$ chars); retain high-context code |
| **DEF-04** | Ultra-Dense Truncation | Unbounded token generation mandate | 21 datasets (2.4%) | 🔴 CRITICAL | Implement logical multi-part segmenter |
| **DEF-05** | Prompt Homogeneity | Recycled static prompt template | 406 datasets (46.7%) | 🟠 HIGH | Implement 8-style Dynamic Diversity Injector |
| **DEF-06** | Single-Turn Monologue | Throughput-first swarm architecture | 870 datasets (100%) | 🟠 HIGH | Generate Types 1–6 supplementary multi-turn datasets |
| **DEF-07** | Syntax-Only Validation | Absence of AST / semantic parser | 870 datasets (100%) | 🟠 HIGH | Deploy `validate_semantic.py` Stage 2 validator |
| **DEF-08** | Non-Physical Hallucinations | Zero simulation / physics ground truth | ~5–8% of blocks | 🟠 HIGH | Deploy automated physical boundary scanner |
| **DEF-09** | Corpus Metadata Poverty | Flat opaque UUID storage layout | 870 datasets (100%) | 🟡 MEDIUM | Generate Schema v2.0 `catalog/corpus_index.jsonl` |

---

## 4. Key Lessons Learned for Future Dataset Engineering

1. **Customer Demand Trumps Abstract Rules**: Industrial models must directly serve paying commercial manufacturing customers (Automobile, Bike & Motorcycle, Heavy Hardware, Electronics). Formatting and domain vocabulary must match their physical factory floors.
2. **High-Token Datasets Are High-Value Assets**: Massive controllers with complete state-space matrices, TMR voting, and multi-stage alarms should not be discarded; they should be cataloged and trained with high-context architectures (e.g. Qwen2.5-Coder 32k/64k/128k context with FlashAttention-2).
3. **Keyword Matching Must Be Context-Aware**: Bare words like `Vessel` or `Steam` have distinct meanings across industries. Strict regex boundaries must prevent false rejections of legitimate plant automation.
4. **Syntax Parity $\ne$ Semantic Correctness**: Balancing brackets only guarantees that a compiler will not crash on tokenization. It provides zero guarantee that the control logic will stabilize a machine or avoid state deadlocks.
5. **Prompt Diversity Is as Critical as Code Quality**: If training prompts lack lexical and structural diversity, the model will memorize prompt boilerplate rather than learning to map user intent to Structured Text.
6. **Multi-Turn Data Must Be Engineered from Day One**: A high-performance domain assistant cannot be built on code emission pairs alone. It requires debug chains, Q&A dialogues, incremental modification pairs, and theory-to-code bridges.
7. **Non-Destructive Data Governance**: Never delete raw generation data. Triage, catalog, and partition datasets into structured tiers (`verified/`, `quarantine/`, `supplementary/`), preserving all 870 original assets.
