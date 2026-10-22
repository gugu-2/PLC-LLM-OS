---
name: plc-swarm-generator
description: Orchestrates concurrent multi-agent swarms (6 to 8 subagents) to generate ultra-dense, mathematically rigorous IEC 61131-3 Structured Text synthetic datasets for massive commercial manufacturing industries.
---

# Commercial PLC Synthetic Data Swarm Skill

Use this skill when the user asks to generate synthetic datasets, start the swarm data loop, or run high-token concurrent subagents for **billion-dollar real-world manufacturing industries**.

---

## 1. Commercial Industry Domain Catalog (Rotate Across 8 Subagents)

When launching an 8-agent swarm wave, assign each agent one of these multi-billion-dollar commercial manufacturing domains:

1. **Automotive EV Battery Cell-to-Pack (CTP)**:
   - System: Automated EV Battery Module Structural Adhesive Dispensing & 1070nm Fiber Laser Busbar Wobble Welding Cell.
   - Function Block: `FB_Automotive_EV_BatteryPack_LaserWeldingDispense`
   - Key Physics: 6-axis robot TCP trajectory velocity feedforward, dual-component polyurethane bead volume metering, laser melt pool pyrometry, and thermal runaway IR detection.
2. **Electronics SMT & Semiconductor Packaging**:
   - System: High-Density Surface Mount Technology (SMT) 12-Zone Convection Reflow Oven with Closed-Loop Nitrogen Atmosphere Control.
   - Function Block: `FB_Electronics_SMT_ReflowOven_12ZoneThermalProfile`
   - Key Physics: 12-zone cascade PID heating, conveyor velocity lead-lag compensation, sub-50 ppm residual oxygen regulation, and thermal shock delta-T protection.
3. **Heavy Mechanical Stamping & Die Cushioning**:
   - System: 2,500-Ton Automotive Body-in-White Servo-Mechanical Stamping Press with Dynamic Hydraulic Die Cushion.
   - Function Block: `FB_Mechanical_HeavyPress_ServoDieCushion_TonnageSync`
   - Key Physics: 4-cylinder proportional servo cushion anti-rebound, strain-gauge eccentric tonnage balancing, and optical light curtain muting.
4. **Plastics & Polymer Injection Molding**:
   - System: 1,200-Ton All-Electric Multi-Cavity Injection Molding Machine with Cavity Pressure V/P Switchover Cascade.
   - Function Block: `FB_Plastics_InjectionMolding_CavityPressureVPOvershoot`
   - Key Physics: Velocity-to-pressure transfer switchover, mold cavity pressure holding cascade, 5-zone barrel ceramic heating, and toggle clamp resolver synchronization.
5. **Food & Beverage Aseptic Packaging**:
   - System: High-Speed (48,000 bph) Continuous Rotary Aseptic Beverage Bottling Carousel with Vaporized Hydrogen Peroxide (VHP) Sterilization.
   - Function Block: `FB_FoodBev_AsepticBottling_RotaryCarouselSterilization`
   - Key Physics: Electromagnetic flowmeter dosing valve interpolation, electronic cam gear carousel synchronization, sterile air overpressure barrier, and CIP caustic wash cycles.
6. **Automotive Powertrain & Engine Assembly**:
   - System: Automated Multi-Cylinder Engine Cold-Test Bench with Crankshaft Torsional Vibration & Oil Gallery Pressure Decay Diagnostics.
   - Function Block: `FB_Automotive_EngineAssembly_ColdTestDiagnostics`
   - Key Physics: AC dynamometer motoring torque ripple analysis, piezoelectric knock sensor FFT harmonics, variable camshaft timing (VCT) dynamic response, and oil pressure decay leak testing.
7. **Precision CNC Tooling & Machining Centers**:
   - System: 5-Axis Gantry High-Speed Machining Center with Real-Time Spindle Thermal Growth Compensation & Laser Tool Wear Observer.
   - Function Block: `FB_Machining_5AxisCNC_ThermalExpansionToolWearObserver`
   - Key Physics: Multi-point cartridge thermocouple thermal growth modeling, non-contact laser tool measurement, tool breakage detection, and spindle vibration chatter avoidance.
8. **End-of-Line High-Speed Packaging & Robotics**:
   - System: Continuous High-Speed Case Packaging Line with Multi-Lane Infeed & Synchronous 4-Axis Delta Robot Collator.
   - Function Block: `FB_Packaging_HighSpeedCartoner_DeltaRobotCollator`
   - Key Physics: Dynamic infeed pacing screw synchronization, vision-guided Delta robot conveyor tracking, hot-melt glue applicator encoder triggering, and carton compression jam detection.

---

## 2. Dynamic 1-Agent = 1-Dataset Lifecycle Rule
* Each subagent generates **exactly one** Function Block dataset file.
* Once the file is written to `data/swarm_raw/agent_<uuid>.json` and validated, that subagent completes its task and is retired.
* The orchestrator spawns a fresh new agent in its place to tackle the next commercial domain.

---

## 3. Real-Time Chatboard Display Requirement
On every cycle, the orchestrator MUST output a Markdown table:

| Agent ID | Commercial Industrial Sector | Specific Automation System | Status | Completed Files |
| :---: | :--- | :--- | :---: | :---: |
| `Agent #01` | Automotive & EV | CTP Laser Busbar Welding & Adhesive Dispensing | `[SYNTHESIZING]` | 1 |
| `Agent #02` | Electronics SMT | 12-Zone Convection Reflow Oven N2 Control | `[VALIDATING]` | 1 |
| `Agent #03` | Heavy Mechanical | 2,500-Ton Servo Stamping Press Die Cushion | `[SAVED]` | 1 |
| ... | ... | ... | ... | ... |
