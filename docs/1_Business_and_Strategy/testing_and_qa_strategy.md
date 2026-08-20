# Testing & QA Strategy

## 1. The 100% Pass Rate Policy
Lumina OS enforces a **100.0% Perfect Pass Rate** policy on its test suite (`run_tests.py`). Because this software interfaces with physical, life-critical machinery, a 99% pass rate is considered a critical failure. No code can be merged into `main` without a green scorecard.

## 2. Test Suite Architecture
The test suite is built on `pytest` and is divided into core modular verification boundaries:
- **`test_lumina_core.py`:** Tests the foundational elements—PAL hardware abstraction, the 3-Layer Verification Gauntlet, and the Z3 SMT bounded model checker.
- **`test_security_proxy.py`:** Asserts the Cognitive Meta-Monitor correctly rate-limits bursts, rejects bad prefixes, and maintains Golden Master cryptographic integrity.
- **`test_extended_subsystems.py`:** Verifies dynamic RAG ChromaDB semantic queries, Process Mining heuristic mapping, and adaptive burst limiters.
- **`test_training_pipeline.py`:** Ensures the AI training schema (Intermediate DSL), DPO loss functions, and RLVR reward inversion protections are perfectly calibrated.

## 3. Mocking & Hardware Isolation
To ensure the test suite can run in CI/CD pipelines (which lack physical PLCs), the `PALManager` strictly isolates all tests via software mock drivers.
- We utilize dependency injection to ensure `SiemensS7Driver`, `ModbusTCPDriver`, and `RockwellCIPDriver` fallback to mock data states.
- Tests can assert theoretical byte-endianness transformers without requiring an actual PROFINET connection.

## 4. Endurance & Stress Testing
Because Lumina relies heavily on `asyncio` for its 5Hz telemetry loop and WebSocket broadcasting, standard unit tests are insufficient. 
The suite includes long-running asynchronous load tests (e.g., pushing 50,000 UDP packets over 7 minutes) to monitor CPU spikes, packet drop rates, and ensure no memory leaks occur in the `UnidirectionalDiodeRX` continuous loop.
