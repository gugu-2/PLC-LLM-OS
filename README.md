# Lumina — Autonomous PLC Operating System & Management Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Z3 SMT Solver](https://img.shields.io/badge/Formal%20Verification-Z3%20SMT-orange.svg)](https://github.com/Z3Prover/z3)
[![Design System](https://img.shields.io/badge/Design%20System-Replicate-ea2804.svg)](https://replicate.com)

**Project Lumina** is an autonomous industrial operating system for IEC 61131-3 PLC code generation, formal mathematical verification, legacy process mining, brownfield protocol abstraction, and zero-trust runtime protection.

---

## 📚 Project Documentation

Detailed technical documentation for the Swarm-based synthetic data engine has been generated:
- [Architecture Overview](docs/ARCHITECTURE.md): The LLM Swarm strategy and PyTorch fine-tuning framework.
- [Data Pipeline](docs/DATA_PIPELINE.md): Folder structures, deduplication, and master dataset compilation logic.
- [Swarm Operations](docs/SWARM_OPERATIONS.md): Cron orchestration, prompt engineering, and safety guardrails.

---

## 🌟 Core Architectural Features

1. **🌤️ Multi-Machine Plant Fleet & Kinematic Oscilloscope**
   - Real-time OEE, predicted 48h uptime, avoided downtime ticker, and continuous HTML5 canvas rendering bottle indexing and harmonic vibration waveforms.
2. **⚡ Controls IDE & Glass Box Causal Narratives**
   - Natural language causal explanations, 3-Layer formal proof badges, syntax-highlighted SCL diffs, and Tier-2 biometric hot-swap deployment.
3. **🔬 Interactive IEC 61131-3 Code Studio & Formal Z3 Prover**
   - Structured Text code editor, custom invariant definitions, real-time Microsoft Z3 SMT solver proving, counterexample trace extraction, and export to **Rockwell Studio 5000 `.L5X` XML** and **Siemens S7 `.SCL`**.
4. **📚 Industrial RAG Knowledge Base**
   - OEM equipment manual library, semantic search with industrial contrastive matching (resolving VFD, PID, Inverter), and dynamic document ingestion.
5. **🔄 Legacy Process Mining Studio**
   - Reconstructs finite state machines from high-frequency I/O transition logs for undocumented brownfield machinery; exports **Functional Mock-up Units (FMU / FMI 2.0)**.
6. **🛠️ AI Commissioning Assistant & AR Loop-Check Terminal**
   - Multi-vendor subnet discovery (Siemens S7, WAGO Modbus, Rockwell CIP), electrical schematic OCR terminal strip mapper, and voice/text field loop-check assistant with digital sign-off certificates.
7. **🛡️ Zero-Trust ICS Security & Hardware Deployment Proxy**
   - SIL 2/3 Safety PLC air-gap rule manager, custom protected tag prefix adder, cognitive burst detector chart, and Golden Master 18.4ms deterministic rollback vault.
8. **📈 C-Suite Financial Command Center & Underwriter**
   - Interactive downtime cost slider, net annual value return modeler ($489,500/yr, 1,020% ROI), and Munich Re / FM Global certified policy underwriter discount metrics (12.5%).

---

## 🏗️ Repository Structure

```
PLC-LLM-OS/
├── AV2/                                    # Universal Master Research Papers (V2)
│   ├── UNIVERSAL_RESEARCH_PAPER.md         # Master Research Synthesis
│   └── v2_research_*.md                    # Modular Research Synthesis docs
├── lumina/                                 # Project Lumina Web Dashboard App
│   ├── backend/                            # FastAPI, PAL, and verification engines
│   ├── frontend/                           # HTML5 dashboard interface
│   └── tests/                              # Core system checks and benchmark harness
├── Local_Ollama_Evol_Pipeline/             # Local GPU synthetic data evolution framework
│   ├── scripts/
│   │   ├── evol_orchestrator.py            # Local generator (dynamic domain invention + thread-safe merge)
│   │   ├── linter.py                       # Upgraded IEC 61131-3 static parser (IF, CASE, FOR, Refusals)
│   │   └── ollama_client.py                # Local Ollama LLM client wrapper
│   └── seeds/                              # RAG seed files divided by quality tier
├── pipeline/                               # Clean dataset management tools
│   └── tools/
│       ├── repair_dataset.py               # Corruption splitter, refusal filter, normalizer
│       ├── audit_all_datasets.py           # Verification and quality tier analysis
│       └── build_master_dataset.py         # Merges approved sources, splits train/val sets
├── data/                                   # Database of synthetic & scraped PLC code
│   ├── master/                             # Target training inputs for LLM fine-tuning
│   │   ├── train.jsonl                     # Shuffled, cleaned ChatML training records
│   │   └── validation.jsonl                # Shuffled, cleaned validation split records
│   ├── DATA_CATALOG.md                     # Complete audit report of all datasets
│   └── synthetic_generation_v3_enterprise_CLEAN.jsonl
├── archive/                                # Consolidated repository of ~110 throwaway scripts
├── DESIGN.md                               # Replicate Design System Specification
└── README.md
```

---
---
## 🚀 Quick Start

### 1. Requirements
* Python 3.10+
* `fastapi`, `uvicorn`, `z3-solver`, `pytest`, `pytest-asyncio`, `websockets`, `pydantic`

### 2. Install Dependencies
```bash
pip install fastapi uvicorn z3-solver pytest pytest-asyncio websockets pydantic
```

### 3. Run Automated Unit & Security Tests
```bash
python -m pytest lumina/tests/test_lumina_core.py lumina/tests/test_security_proxy.py -v
```

### 4. Run Multi-Agent Closed-Loop Benchmark
```bash
python lumina/tests/test_agent_harness.py
```

### 5. Launch the Lumina Server & Interactive Web App
```bash
uvicorn server:app --app-dir lumina/backend --host 127.0.0.1 --port 8000
```
Open **[http://127.0.0.1:8000/](http://127.0.0.1:8000/)** in your web browser.

---

## 📄 License
MIT License.
