# Verification Gauntlet: Z3 SMT & Digital Twin

## 1. The Core Philosophy
Large Language Models (LLMs) are probabilistic. Physical robotics are deterministic. You cannot deploy probabilistic code to a deterministic machine without catastrophic risk. Lumina bridges this gap with the `VerificationGauntlet` (`lumina_verify.py`).

## 2. Layer 1: Static AST Linter
Before any logic is executed, it is parsed by a Static Linter.
- **Bounds Checking:** It searches the Abstract Syntax Tree (AST) for loops (`WHILE`, `FOR`). If a loop does not have an explicit, hardcoded iteration bound, it is instantly rejected as a potential infinite loop (which would crash a PLC's continuous scan cycle).
- **Type Safety:** Ensures all variable assignments match their declared memory types.

## 3. Layer 2: Z3 SMT Bounded Model Checker (Formal Proofs)
If the code is syntactically sound, it is passed to the **Microsoft Z3 SMT Theorem Prover**.
- Z3 treats the AI's generated code as a mathematical formula.
- The plant's safety invariants (e.g., "The safety door MUST be closed if the motor is spinning") are added as strict mathematical constraints.
- Z3 explores *every possible state permutation* of the logic. If it finds even one hypothetical edge case where the safety door is open while the motor is running, it returns `sat` (satisfiable violation), and the code is rejected. 
- **Result:** We achieve mathematical certainty that the AI's code cannot violate core safety rules.

## 4. Layer 3: Kinematic Digital Twin
Formal proofs ensure logic safety, but they do not ensure physical elegance (e.g., stopping a 500kg robotic arm too fast). 
- The validated logic is compiled and executed against a simulated kinematic plant model (`simulated_plant.py`).
- The simulator tracks velocity, acceleration, jerk, and theoretical mechanical vibration (measured in G-forces).
- If the AI's logic commands a movement that exceeds the physical stress thresholds of the machinery (e.g., `vibration_peak_g > 3.0`), the code is rejected to prevent mechanical wear and tear.
