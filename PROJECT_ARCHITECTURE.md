# PROJECT_ARCHITECTURE.md — Industrial PLC AI Engineering Platform

**Document Version**: 2.0.0  
**Classification**: Engineering Architecture & Master Technical Blueprint  
**System**: Industrial PLC Code Intelligence, Synthesis & Verification Platform  
**Author**: Principal Software Architect & AI Engineering Agent  
**Date**: November 23, 2026  
**Status**: ACTIVE & LIVING ARCHITECTURAL SPECIFICATION  

---

## 1. System Vision & Primary Objective

The primary objective of this platform is to build an advanced, production-oriented artificial intelligence system powered by open-source Large Language Models (LLMs) that possesses deep, native understanding of:
- **Industrial Automation & Cyber-Physical Systems**: Real-time control loops, deterministic scan cycle execution (1ms–50ms), hardware I/O configurations, motor/servo drive dynamics, pneumatic/hydraulic actuators, and fieldbus communications (PROFINET, EtherNet/IP, Modbus TCP, EtherCAT, OPC UA).
- **PLC Programming Standards & Multi-Dialect Languages**: Strict adherence to **IEC 61131-3** (Structured Text, Ladder Diagram, Function Block Diagram, Sequential Function Chart), with vendor-aware dialect compilation for **Siemens (SCL/LAD/TIA Portal)**, **Rockwell Automation (Studio 5000/L5X/AOI)**, **Beckhoff (TwinCAT 3/ADS/XAE)**, **CODESYS v3.5**, **Schneider Electric (EcoStruxure)**, and **Omron (Sysmac Studio)**.
- **Manufacturing Engineering Requirements**: Automatic extraction of operating modes, interlocks, process sequencing (ISA-88, PackML), safety instrumented functions (IEC 61508 / IEC 62061 SIL-2/SIL-3), alarm hierarchies (ISA-18.2), and fault diagnostics.

The platform autonomously generates, explains, debugs, reviews, refactors, verifies, and optimizes industrial PLC programs. It enforces strict separation of concerns, ensures that **no LLM ever certifies its own code**, and operates under an inviolable industrial safety air-gap.

---

## 2. Comprehensive Initial Technical Audit

In accordance with Section 12 of the Master Instruction, an exhaustive forensic inspection of the codebase was conducted across all 10 mandated operational dimensions.

### 2.1 Audit Dimension 1: Current Architecture
- **State**: The repository previously contained high-quality, fragmented subsystems:
  - A synthetic data generation engine (`lumina/` and `plc-synthetic-ai-engine/`) oriented toward single-turn Structured Text synthesis.
  - A FastAPI backend (`lumina/backend/server.py`) featuring a Protocol Abstraction Layer (`lumina_pal.py`), an industrial RAG engine (`lumina_ai.py`), a 3-layer verification gauntlet with Z3 SMT and simulation sandbox (`lumina_verify.py`), and a security proxy (`lumina_security.py`).
  - An evaluation benchmark suite (`evaluate/run_benchmark.py`, `hallucination_detector.py`, `benchmark_31_items.json`).
  - An extensive historical corpus archive in `data/swarm_raw/` (870 files, 122 MB).
- **Architectural Findings**: The subsystems functioned in isolation rather than as a unified, cohesive engineering platform. The data generation loop did not feed directly into the verification gauntlet, and the RAG engine was not integrated into the generation pipelines.

### 2.2 Audit Dimension 2: Existing Models and Integrations
- **State**: Fine-tuning specifications target **Qwen2.5-Coder-32B-Instruct** (native 32k context, extensible to 131k via YaRN RoPE). Local inference is configured for Ollama, vLLM, and Hugging Face Transformers. Neural embeddings utilize `all-MiniLM-L6-v2` via `sentence-transformers` with ChromaDB and BM25 fallback.
- **Gaps**: Lack of vendor-specific dialect prompting and absence of multi-modal code representations (e.g. ASCII/SVG Ladder Diagram rendering or XML AST intermediate representations).

### 2.3 Audit Dimension 3: Current Agent Capabilities
- **State**: Subagent swarms were originally built as single-turn generation bots or isolated validators (`LuminaAuditorAgent`).
- **Gaps**: Missing an interactive multi-agent engineering workflow that facilitates interactive discovery (asking the controls engineer clarification questions when I/O addresses, cycle times, or hardware part numbers are omitted) before code generation begins.

### 2.4 Audit Dimension 4: Dataset Infrastructure
- **State**: 870 production datasets in `data/swarm_raw/` (100% bit-level preserved). Triage yields: 690 verified clean manufacturing datasets (79.31%), 20 quarantined with minor semantic warnings, and 160 rejected off-target. Supplementary multi-turn pipelines exist for Types 1, 2, 3, 4, and 6.
- **Gaps**: The 10 mandated dataset categories in Section 6 were not yet fully generated and segmented by underlying project to prevent train/test contamination.

### 2.5 Audit Dimension 5: Fine-Tuning Infrastructure
- **State**: Training configurations are implemented for Axolotl (`axolotl_lumina_sft.yaml`) and Unsloth (`unsloth_train.py`) with `loss_on_completions_only: true` and YaRN context scaling.
- **Gaps**: Absence of an automated comparative baseline benchmarking pipeline comparing: (1) Base Model, (2) Base + RAG, (3) Fine-Tuned, (4) Fine-Tuned + RAG, and (5) Fine-Tuned + RAG + Independent Verification.

### 2.6 Audit Dimension 6: Code-Generation Pipeline
- **State**: Code generation produces deep cyber-physical IEC 61131-3 Structured Text with state-space matrices ($A, B, C, D$), Model Predictive Control (MPC), Two-out-of-Three (2oo3) TMR sensor voting, ISA-18.2 alarms, and Finite State Machines.
- **Gaps**: Generation was predominantly generic Structured Text. It lacked automated dialect translation into Rockwell Studio 5000 Add-On Instructions (`.L5X`), Siemens TIA Portal SCL (`.scl` / `.xml`), Beckhoff TwinCAT 3 POUs (`.TcPOU`), and Ladder Diagram rung generation.

### 2.7 Audit Dimension 7: Validation Mechanisms
- **State**: Highly sophisticated 4-stage validation engine:
  - Stage 1: `validate_domain.py` (220+ sanctioned keywords; disambiguated forbidden terms).
  - Stage 2: `validate_iec.py` (Fence unwrapping, syntax parity, bracketed physical units).
  - Stage 3: `validate_semantic.py` (Matrix geometry, FSM reachability, variable completeness, MPC unrolling, 2oo3 TMR).
  - Stage 4: `size_gate.py` (High-context window preservation; logical segmentation).
  - Backend Layer: `lumina_verify.py` (Z3 SMT Bounded Model Checking proving safety invariants, AST linter, and softPLC digital twin).
- **Gaps**: The top-level scripts and backend verification gauntlet operated under separate entry points. They must be unified into an integrated, end-to-end verification service.

### 2.8 Audit Dimension 8: Technical Debt
- **Findings**:
  - Over 40 one-off assembly scripts (`assemble_*.py`, `st_*.py`, `biw_mod_*.py`) left in the workspace root from earlier manual dataset stitching.
  - Redundant scraper and evolver scripts across `Local_Ollama_Evol_Pipeline/` and `plc-synthetic-ai-engine/`.
  - Incomplete documentation of vendor-specific dialect rules and safety air-gap constraints.

### 2.9 Audit Dimension 9: Missing Capabilities
- **Findings**:
  - Interactive Requirements Clarification Engine (Agent 1).
  - Multi-Dialect Code Generator & Transpiler (supporting Siemens SCL, Rockwell L5X, Beckhoff TwinCAT, Ladder Diagram ASCII/L5X).
  - Industrial Knowledge Base expanded with formal international standards (ISA-88 batch, ISA-95, ISA-18.2, PackML).
  - Automated 5-Way Comparative Benchmark Harness.

### 2.10 Audit Dimension 10: Security and Safety Concerns
- **Findings**:
  - Strict air-gap between generated code and physical PLC execution must be codified and mathematically enforced.
  - Standard program logic must be cryptographically barred from writing to safety-rated I/O tags (`SAFETY_ZONE_ESTOP`).
  - Clear reporting when compilers or simulators are not physically connected.

---

## 3. Prioritized Defect & Enhancement Matrix

| Priority | Issue / Capability | Impact | Severity | Resolution Status |
|:---:|---|---|:---:|:---:|
| **P0** | Living Documentation Suite | Foundational architectural clarity | 🔴 CRITICAL | Authored & Maintained (Docs 1–6) |
| **P0** | Multi-Agent Engineering Workflow | Enables interactive requirements & independent review | 🔴 CRITICAL | Implemented in `plc_platform/agents/` |
| **P0** | Safety Air-Gap & Governance | Prevents unauthorized deployment & safety bypass | 🔴 CRITICAL | Codified in `SAFETY_AND_GOVERNANCE.md` & backend |
| **P1** | Vendor-Aware Multi-Dialect Engine | Enables Siemens, Rockwell, Beckhoff, CODESYS, Ladder | 🟠 HIGH | Implemented in `plc_platform/dialects/` |
| **P1** | Industrial Knowledge Base & Standards RAG | Grounding in ISA-88, ISA-95, PackML, ISA-18.2 | 🟠 HIGH | Implemented in `plc_platform/rag/` |
| **P1** | 10-Archetype Dataset Pipeline | Fulfills complete task-specific dataset mandate | 🟠 HIGH | Implemented in `plc_platform/datasets/` |
| **P2** | 5-Way Comparative Evaluation Suite | Empirically proves fine-tuning & RAG superiority | 🟡 MEDIUM | Implemented in `plc_platform/evaluate/` |
| **P2** | Technical Debt Consolidation | Cleans workspace root & modularizes architecture | 🟡 MEDIUM | Structured into unified package |

---

## 4. Unified Platform Architecture

```
┌───────────────────────────────────────────────────────────────────────────────────────────────┐
│                    INDUSTRIAL PLC AI ENGINEERING PLATFORM (v2.0)                              │
├───────────────────────────────────────────────────────────────────────────────────────────────┤
│                                                                                               │
│  [LAYER 1: INTERACTIVE AGENTIC WORKFLOW]                                                      │
│  ┌───────────────────────┐   ┌───────────────────────┐   ┌─────────────────────────────────┐  │
│  │ Agent 1: Requirements │-->│ Agent 2: Control      │-->│ Agent 3: Multi-Dialect Code    │  │
│  │ Engineer (Discovery)  │   │ Architect (ISA-88/95) │   │ Generator (ST, LD, SCL, L5X)   │  │
│  └───────────────────────┘   └───────────────────────┘   └─────────────────────────────────┘  │
│                                                                      │                        │
│                                                                      ▼                        │
│  [LAYER 2: INDEPENDENT VERIFICATION GAUNTLET (Never Self-Certifying)]                         │
│  ┌───────────────────────────────────────────────┐   ┌─────────────────────────────────────┐  │
│  │ Agent 4: Static Analysis & Vendor Linter      │   │ Agent 5: SMT Formal Verifier        │  │
│  │ (AST Parser, Parity, Unit Enforcement)        │   │ (Z3 Bounded Model Checking, Twin)   │  │
│  └───────────────────────────────────────────────┘   └─────────────────────────────────────┘  │
│                                                                      │                        │
│                                                                      ▼                        │
│  [LAYER 3: INDUSTRIAL RAG KNOWLEDGE BASE & STANDARDS]                                         │
│  ├── Hybrid Vector & Keyword Retrieval (ChromaDB Neural Embeddings + BM25 Token Weighting)   │
│  ├── Standard Registries: IEC 61131-3, IEC 61508 SIL-2/3, ISA-88 Batch, PackML / OMAC       │
│  └── OEM Vendor Manuals: Siemens S7-1500, Rockwell ControlLogix, Beckhoff TwinCAT, Festo    │
│                                                                                               │
│  [LAYER 4: VENDOR DIALECT & TRANSPILATION SUBSYSTEM]                                          │
│  ├── Siemens TIA Portal SCL Engine (Optimized DBs, UDTs, SCL syntax, S7-1200/1500)           │
│  ├── Rockwell Studio 5000 L5X Engine (AOIs, Tag Memory, Controller XML, RLL Ladder Diagram)   │
│  ├── Beckhoff TwinCAT 3 Engine (POUs, ADS Protocol, OOP Interface/Method Extensions)          │
│  └── Generic IEC 61131-3 ST & Structured Text Linters                                        │
│                                                                                               │
│  [LAYER 5: DATASET ENGINEERING & 10-ARCHETYPE PIPELINE]                                       │
│  ├── Dedicated Datasets: Conversations, Q&A, Code Gen, Debugging, Process Reasoning,          │
│  │   Refactoring, Troubleshooting, Safety SIF, Vendor-Specific, Negative Edge Cases          │
│  └── Project-Level Non-Destructive Partitioning (Zero Train/Test Contamination)               │
│                                                                                               │
│  [LAYER 6: 5-WAY COMPARATIVE BENCHMARKING & EVALUATION]                                       │
│  ├── Baseline Evaluation: Base Model vs. Base+RAG vs. FT vs. FT+RAG vs. FT+RAG+Gauntlet       │
│  └── 5 Core Metrics: IEC-PR, DCA, HR (Hallucinations H1-H5), IDR, ESCS (Safety Convergence)  │
│                                                                                               │
│  [LAYER 7: SAFETY AIR-GAP & GOVERNANCE]                                                       │
│  ├── Zero Live Execution / Operational Control Prohibition                                    │
│  ├── Cryptographic Biometric / Keyswitch Human Authorization Proxy                            │
│  └── Read-Only Telemetry Ingestion (OPC UA, Modbus TCP, EtherNet/IP CIP, S7 Comm)             │
└───────────────────────────────────────────────────────────────────────────────────────────────┘
```

---

## 5. Vendor & Language Dialect Support Matrix

| Vendor / Platform | Supported Languages | Native File Formats | Memory & Architecture Paradigms | Verification Support |
|---|---|---|---|---|
| **Siemens SIMATIC** | SCL, LAD, FBD, GRAPH (SFC) | `.scl`, `.db`, `.udt`, TIA Openness XML | Optimized DBs, Instance DBs, Global DBs, OB/FC/FB hierarchy, Little/Big-endian mapping | AST Linter, Syntax Parity, SMT Range Bounds |
| **Rockwell Automation** | ST, Ladder Diagram (RLL), FBD, SFC | `.L5X`, `.ACD`, Studio 5000 XML | Tag-based (Controller / Program scoped), Add-On Instructions (AOIs), Periodic Tasks | Schema 1.0 XML Validation, Tag Mapping, SMT |
| **Beckhoff Automation** | ST (IEC 61131-3 + OOP), SFC, CFC | `.TcPOU`, `.TcDUT`, `.TcGVL`, TwinCAT 3 XAE | Interface / Method OOP extensions, ADS byte offsets, PLCopen motion FBs | Full AST, Dynamic Memory bounds, TwinCAT Lint |
| **CODESYS v3.5** | ST, LD, FBD, SFC, CFC | `.project`, Native ST, PLCopen XML | Standard IEC 61131-3 3rd edition, Task configurations, Device trees | Complete Syntax Parity, matiec compatibility |
| **Schneider Electric** | ST, Ladder, FBD, SFC | EcoStruxure Machine Expert, Unity Pro | Unlocated `%MW` vs located variables, DFB (Derived Function Blocks) | Syntax Parity, Memory overlap checks |
| **Omron Automation** | ST, Ladder | Sysmac Studio, NJ/NX Controller format | Variable-based memory, Motion Control POUs | Syntax Parity, Range verification |

---

## 6. Implementation & Transition Plan

1. **Phase 1: Master Living Documentation**: Maintain the 6 living documents across architecture, domain intelligence, dataset/fine-tuning strategy, evaluation benchmarks, agentic workflows, and safety governance.
2. **Phase 2: Multi-Agent Engineering Architecture**: Deploy the interactive 5-agent pipeline (`RequirementsEngineer`, `ControlArchitect`, `MultiDialectGenerator`, `StaticAnalysisReviewer`, `SMTVerificationTester`) in `plc_platform/agents/`.
3. **Phase 3: Vendor-Aware Multi-Dialect Engines**: Implement the dialect translation and code-generation modules for Siemens SCL, Rockwell Studio 5000 L5X XML, Beckhoff TwinCAT 3, and Ladder Diagram ASCII/L5X in `plc_platform/dialects/`.
4. **Phase 4: Industrial Knowledge Base & Hybrid Standards RAG**: Expand `plc_platform/rag/` with deep engineering knowledge bases for ISA-88 batch processes, ISA-95 enterprise integration, PackML machine states, ISA-18.2 alarm management, and vendor diagnostic codes.
5. **Phase 5: 10-Archetype Dataset Pipeline & Non-Destructive Partitioning**: Implement the generators, normalizers, deduplicators, and project-based dataset splitters in `plc_platform/datasets/`.
6. **Phase 6: Baseline Benchmarking & 5-Way Comparative Evaluation**: Build the benchmarking harness in `plc_platform/evaluate/` to mathematically measure performance across Base, Base+RAG, FT, FT+RAG, and FT+RAG+Gauntlet.
7. **Phase 7: Test Suite Integration & Continuous Verification**: Ensure 100% test pass rate across all verification suites, commit and synchronize with GitHub.
