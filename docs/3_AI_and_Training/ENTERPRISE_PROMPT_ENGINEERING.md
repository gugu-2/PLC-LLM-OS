# Enterprise Prompt Engineering: Forcing Industrial AI to the Limits

This document outlines the strategy used to force a local LLM to generate ultra-high-grade, mission-critical industrial automation code. 

## The Problem with Basic Prompts
If you prompt an LLM with: *"Write a PLC code for a motor"*, it will give you a basic, junior-level script (start button, stop button, motor coil). This is useless for training an enterprise-grade AI.

## The Solution: The "Role-Based Mega-Prompt"
To extract the deepest knowledge from the LLM, we must construct prompts that look identical to internal engineering specification sheets from companies like Tesla, ASML, and CERN. 

An Enterprise Prompt consists of three layers:
1.  **The Identity Layer:** Force the AI into a senior, mission-critical role.
2.  **The Task Layer:** Define an extreme edge-case application.
3.  **The Constraint Layer:** Demand specific advanced IEC 61131-3 techniques (PID, electronic camming, SIL-4 interlocks, etc.).

### Example 1: Tesla Giga Press (Die Casting)
> **Identity:** Principal Controls Engineer at a Tier-1 Automotive Gigafactory.
> **Task:** High-Pressure Aluminum Die-Casting (Giga Press) Controller.
> **Constraints:** Multi-stage hydraulic injection profiling, tie-bar strain gauge parallelism checks (<0.05mm deviation), vacuum block evacuation, PackML standards.

### Example 2: ASML (Semiconductor Lithography)
> **Identity:** Lead Mechatronics Architect at a top-tier Semiconductor firm.
> **Task:** Extreme Ultraviolet (EUV) Lithography Vacuum Chamber.
> **Constraints:** UHV pump sequencing (turbo to cryopump), 6-DOF MIMO maglev reticle staging, SECS/GEM host communications.

### Example 3: CERN (High-Energy Physics)
> **Identity:** Lead Cryogenics Controls Engineer at CERN.
> **Task:** Superconducting Magnet Helium Cryogenics Ring Controller.
> **Constraints:** Liquid Helium (LHe) supercritical phase tracking at 1.9K, Quench Detection heaters, magnetic bearing cold compressor VFDs.

## The Results
By using these hyper-specific prompts against high-quality seed code (from 	ier1_enterprise_grade), the generated synthetic dataset will train your final fine-tuned model to inherently understand complex math, safety protocols, and massive state machines, making it the most advanced industrial coding AI on the market.
