# Deep Technical Audit: System Architecture, Pipeline Fragmentation & Subsystem Gaps

**Audit Date**: November 1, 2026  
**Auditor**: Lumina Cyber-Physical Systems & Automation Architecture Team  
**Scope**: Full repository architecture, data pipelines, module interconnections, and runtime boundaries.

---

## 1. High-Level Architectural Assessment

The Lumina PLC-LLM-OS architecture was envisioned as a multi-tier cyber-physical automation platform comprising:
1. **Cloud / Autonomous LLM Swarm Engine** (generating synthetic IEC 61131-3 logic).
2. **Local GPU Evolution Pipeline** (Ollama/Qwen2.5-Coder running on RTX hardware).
3. **Formal Verification Core** (Z3 SMT solver & IEC AST syntax parsing).
4. **Data Management & PyTorch Training Engine** (LoRA/QLoRA fine-tuning formatters).
5. **Runtime Security & Brownfield Proxy** (OPC UA / Modbus protocol abstractions).

While individual components demonstrate high domain engineering depth, the codebase currently suffers from **severe structural fragmentation**, **duplicate pipeline trees**, and **decoupled subsystems**.

---

## 2. Core Architectural Flaw: Quadruple Pipeline Fragmentation

There are currently **four competing, non-synchronized pipeline implementations** across the repository:

```mermaid
graph TD
    subgraph Root Scripts [1. Root Level Script Zoo]
        R1[150+ ad-hoc scripts: assemble_*.py, gen_*.py, build_*.py]
        R2[10 Isolated Builders: cz_builder, euv_builder, tcm_builder...]
    end

    subgraph Pipeline Tools [2. pipeline/tools/]
        P1[build_master_dataset.py]
        P2[verify_master_dataset.py]
    end

    subgraph Local Pipeline [3. Local_Ollama_Evol_Pipeline/]
        L1[local_evol_pipeline.py]
        L2[local_worker_daemon.py]
        L3[Dedicated data/ directory with duplicates]
    end

    subgraph Lumina Dataset Pipeline [4. lumina/dataset_pipeline/]
        D1[evol_instruct_engine.py]
        D2[multi_agent_swarm.py]
        D3[github_scraper.py]
    end

    Root Scripts -.->|Writes to| SWARM[data/swarm_raw/]
    Pipeline Tools -->|Reads from| SWARM
    Pipeline Tools -->|Writes to| MASTER[data/master/train.jsonl]
    Local Pipeline -.->|Completely Isolated| LOCAL_DATA[Local_Ollama_Evol_Pipeline/data/]
    Lumina Dataset Pipeline -.->|Dormant / Unused| DORMANT[lumina/data/]
```

### Consequences of Fragmentation:
1. **Redundant Code & Maintenance Debt**:
   - `Local_Ollama_Evol_Pipeline` maintains its own copy of prompt templates, mutation engines, and JSON validation logic, completely detached from `pipeline/tools/` and `lumina/dataset_pipeline/`.
   - The root directory contains **156 standalone python files** (`assemble_*.py`, `gen_*.py`, `build_*.py`), which duplicate logic already present in `gen_modules/` and domain builders (`cz_builder/`, `euv_builder/`).
2. **Data Divergence**:
   - When local evolutions are generated via Ollama, they write to `Local_Ollama_Evol_Pipeline/data/`, which is NOT crawled by default by `pipeline/tools/build_master_dataset.py`.
   - Datasets created in `data/swarm_raw/` do not share state with the local evol pipeline.

---

## 3. Nested Repository Clones & Storage Redundancy

Two full git repositories are cloned directly inside the workspace without submodule registration:

1. **`gugu-2/PLC-LLM-OS/`**:
   - Contains a complete duplicate clone of the remote repository inside itself!
   - Holds 35 python files, duplicate documentation, and an uncompressed copy of `synthetic_generation_v3_enterprise.jsonl`.
2. **`plc-synthetic-ai-engine/`**:
   - Contains 24 python files and 925 JSON/JSONL files.
   - Operates as an untracked external repo footprint inside the workspace.

> [!CAUTION]
> Having git repositories cloned inside working directories creates severe git indexing overhead, potential submodule collisions, and redundant storage bloat.

---

## 4. Submodule Case-Sensitivity Collision on Windows NTFS

In `lumina/data/cloned_repos_v3/Beremiz4uC`:
- The upstream Linux repository tracks two distinct files: `README.md` and `readme.md`.
- On Windows (NTFS), file names are **case-preserving but case-insensitive**. When Git checks out this repository on Windows, `README.md` and `readme.md` collapse into the same physical file on disk.
- **Impact**: Any checkout or git status command continuously reports `Beremiz4uC` as modified or dirty (`Subproject commit ... -dirty`), preventing clean one-step submodule updates.

---

## 5. Formal Verification & Security Proxy Decoupling

The formal verification components (`lumina/verification/` using Z3 SMT solver) and the Brownfield Security Proxy (`lumina/security/`) are structurally sound but **completely decoupled from the synthetic data generation loop**:

1. **No Real-Time Z3 SMT Feedback**:
   - `SyntheticDataEvolverV3` agents rely solely on regex AST checks (`validate_iec.py`).
   - The Z3 solver (`lumina/verification/smt_verifier.py`) is capable of proving safety properties (e.g., absence of division by zero, reachability of emergency stop states, bounded matrix state propagation). However, it is NOT called during swarm generation.
2. **Security Proxy Runtime Isolation**:
   - The zero-trust security proxy (`lumina/security/zero_trust_proxy.py`) implements packet inspection and memory sanitization for PLC tags, but has no integration with the fine-tuning training datasets.

---

## 6. Training Pipeline Disconnection

In `lumina/training/`:
- `train_plc_llm.py` and `train_dataset_formatter.py` were designed to load data using the HuggingFace `datasets` library.
- However, as identified in the code audit, `datasets` relies on `pandas`, which currently fails in Python 3.13 due to a missing `six.moves` dependency in `.venv`.
- Consequently, the official training entry point cannot be run without resolving the virtual environment dependencies or falling back to raw PyTorch `jsonl` loaders.
