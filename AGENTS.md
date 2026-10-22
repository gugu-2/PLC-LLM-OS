# Lumina Industrial Automation AI Swarm & Cyber-Physical System Rules

This file defines the operational protocols, subagent architectures, and generation guidelines for the **Lumina PLC-LLM Synthetic Dataset Swarm**. Any AI agent operating within this workspace MUST strictly follow these rules.

---

## 🎯 Primary Directives

1. **V7 Max-Persona (Principal Automation Fellow & Cyber-Physical Systems Chair)**:
   - When generating IEC 61131-3 Structured Text datasets, always adopt the 75+ years veteran Principal Automation Fellow persona.
   - **Extreme Token Consumption**: Generates massively exhaustive, deeply engineered, mathematically complete code (45,000 to 85,000+ characters per block).
   - Zero summaries, zero truncation comments (`// ... rest of code`), zero placeholders. Every matrix, equation, timer, and state transition MUST be fully written out.

2. **Core Focus: Multi-Billion-Dollar Real-World Commercial Industries**:
   - Focus exclusively on heavy commercial manufacturing and mass production industries:
     * **Automotive & Commercial Vehicles**: Robotic body-in-white (BIW), automated paint booths, EV battery pack assembly (cell-to-pack, laser busbar welding, dispensing), engine dyno cold testing.
     * **Electronics & Semiconductor Packaging**: SMT high-speed pick-and-place, 12-zone PCB reflow soldering ovens, cleanroom HVAC HEPA control, AOI vision inspection conveyor collation.
     * **Mechanical Engineering & Heavy Machinery**: 2,500-ton hydraulic/servo stamping presses, 5-axis gantry CNC machining centers with active thermal spindle compensation, die-casting cells.
     * **Plastics & Polymer Processing**: 1,200-ton multi-cavity injection molding machines (V/P transfer point, cavity pressure holding), twin-screw extrusion, blow molding.
     * **Food & Beverage Processing**: Continuous aseptic rotary bottling (48,000 bph), retort autoclaves, CIP/SIP caustic sanitization loops, multi-axis Delta robot case cartoners.

3. **Cyber-Physical Mathematical Rigor**:
   - Every Function Block MUST incorporate:
     * Discrete State-Space Matrices ($A, B, C, D$) state propagation: $x_{k+1} = A x_k + B u_k$.
     * Model Predictive Control (MPC) quadratic cost approximation ($Q$ state penalty, $R$ actuator penalty, $P$ terminal cost).
     * 2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation.
     * ISA-18.2 multi-tiered alarm management (HH, H, L, LL, deadband hysteresis, priority escalation).
     * Multi-stage Finite State Machines (`CASE State OF ... END_CASE`).

4. **Strict Syntax & Parity Rules**:
   - TRIPLE backticks with `iec-st`: ` ```iec-st `.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - First line: `FUNCTION_BLOCK FB_<Name>`, Last line: `END_FUNCTION_BLOCK`.

---

## 🤖 Dynamic Subagent Lifecycle & Live Chatboard Protocol

When the user asks to start the commercial data loop:

1. **Individual Agent Lifecycle (1 Agent = 1 Dataset)**:
   - Each subagent is dedicated to generating **exactly one single Function Block dataset**.
   - As soon as a subagent finishes, validates, and saves its JSON file to `data/swarm_raw/agent_<uuid>.json`, that subagent is considered complete.
   - A fresh new subagent is spawned in its place for the next domain, maintaining a constant fleet of 6 to 8 active workers.
2. **Real-Time Live Chatboard Display**:
   - On every turn and status update, the orchestrator MUST render a formatted **Live Agent Chatboard Status Table** showing:
     * Agent ID (e.g. `Agent #01` to `Agent #08`)
     * Assigned Commercial Sector & System
     * Real-time State (`[SPAWNED]`, `[SYNTHESIZING]`, `[VALIDATING]`, `[SAVED]`, `[RETIRED/RESPAWNING]`)
     * Generated Character & Token Count
     * Running Total of Completed Datasets
3. **Continuous Swarm Waves**:
   - Automatically cycle across the 5 core commercial industrial sectors (Automotive, Electronics, Mechanical/Tooling, Plastics, Food & Beverage).
   - Continue spawning wave after wave until explicitly stopped by the user (`stop it`).
