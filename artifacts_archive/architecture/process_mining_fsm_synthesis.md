# AI Process Mining & FSM Synthesis

## 1. Brownfield Legacy Code Discovery
Lumina is frequently deployed into "Brownfield" environments—factories with 20-year-old PLCs running undocumented, spaghetti Ladder Logic. 

## 2. The Alpha Miner Heuristic
Instead of trying to decompile obsolete binary PLC files, Lumina utilizes **Process Mining** on the raw network event logs.
- The `ProcessMiner` class ingests raw telemetry sequences (e.g., `StartBtn -> ConveyorRun -> SensorA -> Stop`).
- It applies the **Alpha Miner Heuristic** to map causal dependencies (if A always precedes B, A causes B).
- It identifies concurrent processes (C and D happen simultaneously without affecting each other).

## 3. Finite State Machine (FSM) Synthesis
Once the causal map is formed, the AI synthesizes a deterministic **Finite State Machine (FSM)**.
- The FSM represents the *actual* behavior of the legacy plant.
- The Qwen2.5-Coder LLM then reads this FSM graph and re-writes the 20-year-old logic into modern, object-oriented Structured Text (ST) / IEC 61131-3 code.
- This effectively allows Lumina to autonomously upgrade legacy factories by observing them, without needing the original source code.
