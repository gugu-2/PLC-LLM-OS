import json
import uuid
import re
import os

prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Advanced Semiconductor Fabrication & Photolithography** industry.

**Domain**: Extreme Ultraviolet (EUV 13.5 nm) Laser-Produced Plasma (LPP) Light Source: 50 kHz Molten Tin (Sn) Droplet Generator, Dual-Pulse CO2 Laser Steering (Pre-pulse & Main-pulse), and Mo/Si Multilayer Collector Mirror Hydrogen Debris Mitigator & Thermal Stabilization.

**Function Block Name**: `FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror`

**Engineering Context**:
- 50 kHz molten tin (Sn) droplet generator (droplet diameter 27 µm, velocity 80 m/s, nozzle temperature 260°C to 280°C, acoustic piezo Rayleigh excitation).
- Dual-pulse CO2 laser irradiation (10.6 µm wavelength): Pre-pulse flattens droplet into thin disk target (~250 µm diameter); Main-pulse ionizes tin into 30-40 eV high-density plasma emitting in-band 13.5 nm EUV radiation.
- Fast steering mirror (FSM) piezo actuators with nanosecond QPD position sensing (< 2 µm spatial jitter at 50,000 droplets/sec).
- 600 mm Mo/Si multilayer normal-incidence ellipsoidal collector mirror with 16-zone microchannel cooling water flow maintaining mirror bulk temperature to 22.00°C ±0.05°C.
- Dynamic hydrogen (H2) buffer gas curtain (> 150 slm) providing ion debris deceleration and tin vapor drag.
- In-situ RF hydrogen radical cleaning observer driving chemical etching: Sn(s) + 4H*(g) -> SnH4(g).
- 2oo3 Triple Modular Redundancy (TMR) across fast quadrant photodiodes (QPD), droplet shadowgraph cameras, and UHV Penning vacuum gauges.
- Ultra-fast laser-droplet spatial mismatch interlock (< 2 µs CO2 main amplifier trigger kill upon > 8 µm deviation).

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** (8x8 at 100 µs / 10 kHz task cycle):
   - State vector x = [delta_X_drop, delta_Vx_drop, delta_Y_drop, delta_P_piezo, theta_FSM_X, theta_FSM_Y, delta_R_mirror, delta_T_mirror]
   - Full numerical matrices A (8x8) and B (8x6) modeling droplet trajectory deflection, piezo acoustic resonance, FSM piezo dynamics, and mirror thermal expansion.
   - Matrices C (8x8) and D (8x6) output equations.
   - Dynamic propagation: x_{k+1} = A*x_k + B*u_k and y_k = C*x_k + D*u_k.
2. **Model Predictive Control (MPC) Quadratic Cost Approximation**:
   - Cost function J = sum (x - r)^T Q (x - r) + u^T R u + delta_u^T S delta_u + (x - r)^T P (x - r).
   - Full weight matrices Q (8x8), R (6x6), S (6x6), terminal penalty P (8x8), and unrolled optimal feedback gain K_mpc (6x8).
3. **2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR)**:
   - 3 Fast Quadrant Photodiodes (QPD A, B, C) for beam position.
   - 3 High-speed optical shadowgraph droplet tracking cameras (Cam A, B, C).
   - 3 Source vessel UHV Penning/Pirani ion vacuum gauges.
   - Discrepancy timers, automated isolation of failing sensors, bumpless degradation modes.
4. **Hydrogen Buffer Gas Curtain, Debris Mitigation & 16-Zone Mirror Thermal Stabilization**:
   - Dynamic H2 curtain flow and ion stopping power calculation.
   - RF hydrogen radical generation and stannane (SnH4) chemical etching kinetics observer.
   - 16-zone microchannel cooling regulation with individual zone flow trims, feedforward heat flux compensation, and ±0.05°C surface uniformity control.
5. **Multi-Stage Finite State Machine (FSM)**:
   - 10 states: TIN_RESERVOIR_MELT_DEGAS (0) -> CHAMBER_UHV_TURBO_ROUGHING (10) -> HYDROGEN_CURTAIN_FLOW_STABLE (20) -> DROPLET_PIEZO_RESONANCE_EXCITE (30) -> OPTICAL_SHADOWGRAPH_SYNC_LOCK (40) -> PREPULSE_LASER_FLATTEN_ACTIVE (50) -> MAINPULSE_EUV_BURST_EMISSION (60) -> COLLECTOR_MIRROR_DEBRIS_PURGE (70) -> BEAM_DEVIATION_INTERLOCK_ABORT (80) -> CONTROLLED_EUV_SOURCE_COOLDOWN (90).
6. **ISA-18.2 Multi-Tiered Alarm Hierarchy**:
   - Spatial mismatch HH (> 8 µm abort), vacuum loss HH (> 5.0e-5 mbar abort), collector mirror over-temp HH (> 65°C abort), tin nozzle freeze-out/over-temp, H2 pressure loss.
   - Alarm and diagnostic DWORD packing, and 21 CFR Part 11 CRC32 calculation.

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Semiconductor_EUV_LPP_TinDroplet_CollectorMirror`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 65,000 to 90,000+ characters of deeply engineered Structured Text."""

print("Prompt defined successfully, length:", len(prompt))
