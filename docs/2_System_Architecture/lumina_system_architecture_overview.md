# Lumina OS: Master System Architecture

## 1. Architectural Philosophy
The Lumina OS is designed around a strictly decoupled, modular architecture. It enforces a hard separation of concerns between the generative AI brains, the web server layer, the physical hardware abstraction layer, and the digital twin simulation. This ensures a memory leak in the LLM cannot crash the physical robotics drivers.

## 2. Core Modules

### `lumina/backend/`
- **`server.py`:** The master FastAPI application. Manages the asyncio event loops, WebSocket broadcasting at 5Hz, and routing HTTP requests from the frontend dashboard.
- **`lumina_pal.py`:** The Protocol Abstraction Layer. Translates standard AI logic outputs into proprietary hardware signals (Snap7 for Siemens, PyModbus, PyComm3 for Rockwell).
- **`lumina_diode.py`:** The Layer-1 UDP Unidirectional Data Diode. Simulates a physical air-gap by ensuring telemetry can flow *up* to the AI, but the AI cannot push data *down* without passing through the Verification Gauntlet.
- **`lumina_ai.py`:** Hosts the ChromaDB RAG system and LLM interfaces.
- **`lumina_security.py`:** The Cognitive Meta-Monitor and Golden Master SHA-256 vault. Rejects anomalous logic payloads.
- **`lumina_verify.py`:** The Z3 Formal Verification Gauntlet.

### `lumina/frontend/`
- **`index.html`:** The zero-build, edge-native dashboard. Features 9 operational tabs and the mobile AR Diagnostics HUD.

### `lumina/training/`
- **`train_plc_llm.py`:** The Qwen2.5-Coder QLoRA fine-tuning script.
- **`train_rlsf_dpo.py`:** The RLVR (Reinforcement Learning with Verifiable Rewards) integration matrix.
- **`train_dataset_formatter.py`:** The intermediate DSL JSON schema validator.

### `lumina/tests/`
- The overarching `pytest` suite ensuring 100% pass rates across all verification and simulation systems.
