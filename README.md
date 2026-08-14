# Project Lumina — Autonomous PLC Operating System & Management Engine

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/Python-3.10%2B-brightgreen.svg)](https://www.python.org/)
[![Z3 SMT Solver](https://img.shields.io/badge/Formal%20Verification-Z3%20SMT-orange.svg)](https://github.com/Z3Prover/z3)
[![Design System](https://img.shields.io/badge/Design%20System-Replicate-ea2804.svg)](https://replicate.com)

**Project Lumina** is an autonomous industrial operating system for IEC 61131-3 PLC code generation, formal mathematical verification, legacy process mining, brownfield protocol abstraction, and zero-trust runtime protection.

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
│   ├── v2_research_aiml_architecture.md    # AI/ML & RAG Architecture
│   ├── v2_research_business_strategy.md    # Business, Pricing & Liability Strategy
│   ├── v2_research_industrial_automation.md# OT Integration & Protocol Abstraction
│   ├── v2_research_product_ux.md           # Product UX & Glass Box Interface
│   └── v2_research_systems_security.md     # Systems Architecture & ICS Security
├── lumina/
│   ├── backend/
│   │   ├── lumina_pal.py                   # Protocol Abstraction Layer (S7, Modbus, CIP)
│   │   ├── lumina_verify.py                # 3-Layer Verification Gauntlet (Z3 SMT + Linter)
│   │   ├── lumina_ai.py                    # Industrial RAG, Causal Narratives, SCL Synthesizer
│   │   ├── lumina_security.py              # Hardware Deployment Proxy & Golden Vault
│   │   ├── simulated_plant.py              # Multi-machine continuous plant simulator
│   │   └── server.py                       # FastAPI master server with 5Hz WebSockets
│   ├── frontend/
│   │   └── index.html                      # Replicate-styled Glass Box Web Dashboard
│   ├── tests/
│   │   ├── test_lumina_core.py             # Unit tests for PAL, Z3 model checking, linter
│   │   ├── test_security_proxy.py          # Security tests for air-gap & burst limits
│   │   └── test_agent_harness.py           # Multi-agent closed-loop benchmark runner
│   └── WALKTHROUGH.md                      # Detailed system walkthrough
├── DESIGN.md                               # Replicate Design System Specification
└── README.md
```

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
