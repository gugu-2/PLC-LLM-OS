# Generator for FB_Semiconductor_ALD_PrecursorPulse_SusceptorHeater
import json
import uuid
import os
import re

agent_id = "17312e6d"
json_path = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{agent_id}.json"

user_prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Advanced Semiconductor Fabrication — Thin Film Atomic Layer Deposition** industry.

**Domain**: 300 mm Single-Wafer Thermal Atomic Layer Deposition (ALD, High-k HfO2 Gate Dielectric): Millisecond Precursor Gas Injection Fast Pulse Solenoid Valves (TEMAHf & H2O/O3), High-Speed Inert N2 Purge, 4-Zone Resistance Heated Susceptor with Closed-Loop Multi-Channel Thermocouple Voting, and Downstream Heated Throttle Valve Automatic Pressure Control.

**Function Block Name**: `FB_Semiconductor_ALD_PrecursorPulse_SusceptorHeater`

**Engineering Context**:
- 300 mm single-wafer cold-wall ALD reactor depositing ultra-thin high-k gate dielectric hafnium dioxide (HfO2) films for advanced FinFET / GAA nanosheet transistors.
- Metal precursor: Tetrakis(ethylmethylamido)hafnium [Hf(NEtMe)4, TEMAHf] heated delivery cylinder at 120°C with argon/nitrogen carrier gas bubbling and sub-millisecond fast pulse ALD solenoid injection.
- Co-reactant oxidant: High-purity vaporized H2O or Ozone (O3) with separate fast-pulse injection delivery.
- Inert purge gas: Ultra-high purity N2 (99.9999%) ballast and purge manifold with mass flow controllers and high-speed bypass valves.
- Susceptor heating: 4 concentric resistance heating zones (Zone 1: Center, Zone 2: Mid-Inner, Zone 3: Mid-Outer, Zone 4: Edge) with active thermal cross-talk decoupling, maintaining 300 mm wafer at 300°C ± 0.15°C temperature uniformity.
- Downstream heated throttle valve (0-90° butterfly position) maintaining reactor vacuum from 0.05 to 5.0 Torr during continuous ALD cycles, backed by dry roots booster and mechanical dry screw pump.
- In-situ optical / quartz crystal microbalance / saturation observer verifying self-terminating monolayer growth per cycle (GPC ~ 0.95 Å/cycle).

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** (8-state, 8-input, 6-output at 1 ms sampling cycle):
   - State vector x = [T_zone1_center, T_zone2_mid_in, T_zone3_mid_out, T_zone4_edge, theta_adsorbed_TEMAHf, theta_surface_hydroxyl, P_chamber_torr, T_foreline_degC]
   - Full numerical discrete state-space matrices A (8x8) and B (8x8) accounting for inter-zone conduction, radiation to cold chamber walls, Langmuir adsorption-desorption surface reaction kinetics, and dynamic chamber pressure mass balance: V * dP/dt = Q_in - S_eff * P.
   - Observer state correction: x_{k+1} = A*x_k + B*u_k + L*(y_meas - C*x_k) evaluated at 1 kHz task execution.
2. **Model Predictive Control (MPC) Quadratic Cost Functional**:
   - Multi-zone thermal decoupling and pressure stabilization: Cost J = sum (x - r)^T * Q * (x - r) + u^T * R * u + delta_u^T * S * delta_u.
   - Matrices Q (8x8 state penalty), R (8x8 actuator slew penalty), S (8x8 rate penalty), and Terminal cost P_term (8x8).
   - Unrolled projected gradient descent solver (10 iterations) directly enforcing PWM limits [0.0%, 100.0%] and throttle angle constraints [0.0°, 90.0°].
3. **2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR)**:
   - 3 Dual-Range Capacitance Manometers (MKS Baratron 1 Torr / 10 Torr) with discrepancy voting (< 0.005 Torr threshold) and sensor fault isolation.
   - 4-Zone Susceptor Embedded Thermocouple Arrays (3 mineral-insulated Type-N thermocouples per zone = 12 sensors total) with emissivity polynomial compensation, median selection, and discrepancy diagnostic timers.
   - Redundant toxic precursor gas sniffers (0.01 ppm threshold) and scrubbed exhaust pressure monitoring.
4. **ALD Super-Cycle Sub-Millisecond Sequencing**:
   - 4-Phase ALD cycle execution: Phase A (TEMAHf Pulse 20 ms), Phase B (N2 Purge 500 ms), Phase C (Oxidant Pulse 30 ms), Phase D (N2 Purge 500 ms).
   - Strict hardware-enforced gas pulse overlap interlock preventing simultaneous precursor and oxidant valve actuation (preventing dangerous CVD gas-phase reactions).
   - Langmuir surface coverage tracking and Growth-Per-Cycle (GPC) accumulation.
5. **ISA-18.2 Multi-Tiered Alarm Hierarchy**:
   - Susceptor over-temperature: HH (> 400°C emergency abort), H (> 350°C), L (< 250°C), LL (< 200°C).
   - Precursor delivery line temperature: LL (< 110°C condensation warning), HH (> 160°C thermal decomposition abort).
   - Vacuum base pressure high alarm (> 5.0e-3 Torr).
   - Toxic exhaust leak trip and throttle position tracking error.
6. **Multi-Stage Finite State Machine (FSM)**:
   - 10+ operational states: CHAMBER_STANDBY_VACUUM_BASE (0), PRECURSOR_LINE_HEAT_TRACE_SOAK (10), SUSCEPTOR_TEMPERATURE_RAMP_UNIFORM (20), ROBOTIC_WAFER_TRANSFER_PADDLE (30), WAFER_PULLDOWN_PNEUMATIC_PIN_LOWER (40), STEADY_STATE_ALD_CYCLE_PULSING (50), THICKNESS_END_OF_CYCLE_VERIFY (60), POST_PROCESS_HIGH_FLOW_PURGE (70), WAFER_UNLOAD_TRANSFER_CHAMBER (80), CHAMBER_CLEAN_NF3_PLASMA_ETCH (90), EMERGENCY_ABORT_SAFETY_PURGE (99).

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Semiconductor_ALD_PrecursorPulse_SusceptorHeater`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 65,000 to 90,000+ characters of deeply engineered Structured Text.
"""
print("User prompt length:", len(user_prompt))
