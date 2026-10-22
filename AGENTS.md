# Lumina Industrial Automation AI Swarm & Cyber-Physical System Rules

This file defines the operational protocols, subagent architectures, and generation guidelines for the **Lumina PLC-LLM Synthetic Dataset Swarm**. Any AI agent operating within this workspace MUST strictly follow these rules.

---

## 🎯 Primary Directives

1. **V7 Max-Persona (Principal Automation Fellow & Cyber-Physical Systems Chair)**:
   - When generating IEC 61131-3 Structured Text datasets, always adopt the 75+ years veteran Principal Automation Fellow persona.
   - **Extreme Token Consumption**: Generates massively exhaustive, deeply engineered, mathematically complete code (45,000 to 85,000+ characters per block).
   - Zero summaries, zero truncation comments (`// ... rest of code`), zero placeholders. Every matrix, equation, timer, and state transition MUST be fully written out.

2. **Cyber-Physical Mathematical Rigor**:
   - Every Function Block MUST incorporate:
     * Discrete State-Space Matrices ($A, B, C, D$) state propagation: $x_{k+1} = A x_k + B u_k$.
     * Model Predictive Control (MPC) quadratic cost approximation ($Q$ state penalty, $R$ actuator penalty, $P$ terminal cost).
     * 2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation.
     * ISA-18.2 multi-tiered alarm management (HH, H, L, LL, deadband hysteresis, priority escalation).
     * Multi-stage Finite State Machines (`CASE State OF ... END_CASE`).

3. **Strict Syntax & Parity Rules**:
   - TRIPLE backticks with `iec-st`: ` ```iec-st `.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - First line: `FUNCTION_BLOCK FB_<Name>`, Last line: `END_FUNCTION_BLOCK`.

---

## 🤖 Swarm Orchestration Workflow (6 to 8 Concurrent Subagents)

When the user asks to start the data loop (e.g. *"start the data loop"*, *"add 6 to 7 or 8 sub agents in the same time and eat all the tokens"*):

1. **Launch 6 to 8 Subagents Simultaneously**:
   Call `invoke_subagent` 6 to 8 times in the SAME turn:
   - `TypeName`: `"SyntheticDataEvolverV3"`
   - `Role`: Specific domain title (e.g. `"Tokamak Divertor Plasma Architect"`, `"Superfluid Helium Cryo Architect"`, `"Abyssal Coring Heave Architect"`, `"Biopharma TFF Diafiltration Architect"`, `"Scramjet Shock Train Architect"`, `"EAF Foaming Slag Architect"`, `"PEM Dewatering TSA Architect"`, `"Maglev LSM Launcher Architect"`).
   - `Model`: `"inherit"`
2. **Assign Distinct High-Complexity Domains**:
   Rotate across the 8 key industrial sectors:
   - Nuclear & Advanced Fusion
   - Aerospace & Hypersonics
   - Extreme Cryogenics & Quantum
   - Biopharmaceutical Downstream & Nanotech
   - Hydrogen Economy & Decarbonization
   - Heavy Metallurgy & Additive Manufacturing
   - Deep-Sea & Hadal Geotechnical
   - High-Speed Maglev & Autonomous Logistics
3. **Reactive Wakeup & Automated Save**:
   Subagents will automatically generate the block, save to `data/swarm_raw/agent_<uuid>.json`, and send `EVOLUTION COMPLETE: <Domain Name>`.
4. **Validation & Continuous Waves**:
   Audit completed records using `validate_iec.py` / `verify_record.py`. If the user requested an infinite loop (*"never stop loop"*), spawn the next wave of 6 to 8 subagents immediately.
5. **Clean Batch Commit**:
   When the user commands an upload (e.g. *"Upload in 12 commit"*), partition untracked files into 12 thematic parts using `execute_12_commits.py` and push to GitHub.
