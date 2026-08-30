# Developer Onboarding & Quick Start Guide

Welcome to the Lumina Industrial OS Core Team. This codebase controls physical robotics and life-safety systems. **Code quality is not a suggestion; it is a strict requirement.**

## 1. Local Environment Setup
Lumina requires Python 3.10+ and a CUDA-capable GPU (if running local LLM training).

1. Clone the repository and navigate to the root directory.
2. Install dependencies:
   ```bash
   pip install fastapi uvicorn websockets python-snap7 pymodbus pycomm3 z3-solver chromadb sentence-transformers
   ```

## 2. Running the Edge Server
To spin up the FastAPI edge server and the frontend dashboard:
```bash
python lumina/backend/server.py
```
This will launch the `uvicorn` server on `http://localhost:8000`. Navigate to this URL in any modern browser to view the 9-Tab Dashboard.

## 3. Contributing to the Verification Gauntlet
If you are adding new safety invariants to `lumina_verify.py`:
1. Never use heuristic matching. Use the Microsoft Z3 SMT prover.
2. Define your logic rules mathematically in the `_run_z3_bounded_model_checker()` method.
3. If the Z3 solver returns `unsat` for an invalid state, your test passes.

## 4. Running the Test Suite
Before committing any code, you must execute the master test suite.
```bash
python run_tests.py
```
The suite requires a **100.0% Perfect Pass Rate**. If a single unit test fails, the build is automatically rejected. The test suite includes endurance testing for asyncio task management and memory leaks.
