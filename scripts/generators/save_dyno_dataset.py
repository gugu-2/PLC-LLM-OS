# save_dyno_dataset.py
import json
import uuid
import os
from st_part1 import PART1_DECLARATIONS
from st_part2 import PART2_LOGIC
from st_part3 import PART3_LOGIC

prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Automotive Powertrain & Commercial Vehicles** industry.

**Domain**: Automated Commercial Vehicle Multi-Cylinder Engine Cold-Test Dynamometer Bench with Crankshaft Torsional Vibration & High-Speed Oil Pressure Decay Diagnostics.

**Function Block Name**: `FB_Automotive_EngineAssembly_ColdTestDiagnostics`

**Engineering Context**:
- End-of-line robotic engine assembly cold-test cell for heavy-duty 6-cylinder diesel/hybrid engines
- 160 kW low-inertia AC dynamometer motor driving the unfueled engine from 0 to 2,000 RPM
- Crankshaft optical encoder (1,800 PPR + index) resolved to 0.2° crank angle for sub-revolution torque ripple analysis
- Dual piezoresistive dynamic cylinder pressure transducers installed in glow plug ports
- High-speed oil gallery pressure decay leak testing with multi-port pneumatic seal tooling
- Piezoelectric accelerometer vibration FFT harmonic order tracking (orders 0.5, 1.0, 1.5, 3.0, 6.0)
- Variable Camshaft Timing (VCT) phaser oil pressure dynamic response & valve lash clearance verification

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** for engine motoring friction torque & oil pressure build:
   - State vector x = [dyno_torque_error, crankshaft_speed_jitter, oil_gallery_pressure, vct_phase_angle]
   - Full numerical matrices A (4×4) and B (4×2) explicitly written out row-by-row
   - Propagation: x_{k+1} = A*x_k + B*u_k evaluated at 1ms crank-synchronous interrupt
2. **Model Predictive Control (MPC) Quadratic Cost Approximation**:
   - Dyno motoring speed profile tracking with torque ripple cancellation
   - Q matrix (4×4 error penalty) and R matrix (2×2 dyno inverter command slew penalty)
   - Terminal cost matrix P (4×4)
3. **2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) Voting**:
   - 3 dynamic oil gallery pressure transducers checking engine main journal lubrication circuit
   - Sensor deviation threshold (0.2 bar) with automated sensor isolation
4. **ISA-18.2 Multi-Tiered Alarm Ladder**:
   - Motoring torque limit: HH (550 Nm mechanical seizure abort), H (480 Nm tight bearing warning)
   - Oil pressure build delay: HH (> 3.5s no oil pressure abort), H (> 2.5s warn)
   - Torsional vibration order 3.0: HH (18 mm/s peak fault), H (12 mm/s warn)
5. **Multi-Stage Finite State Machine (FSM)**:
   - States: ENGINE_LOADED_DOCK (0) -> TOOLING_COUPLING_ENGAGE (10) -> OIL_CIRCUIT_PREFILL (20) -> STATIC_LEAK_DECAY (30) -> CRANKING_TORQUE_TEST_300RPM (40) -> VCT_PHASER_SWEEP_800RPM (50) -> HIGH_SPEED_VIBRATION_TEST_1800RPM (60) -> VALVE_TIMING_LASER_VERIFY (70) -> ENGINE_DECEL_PARK (80) -> ENGINE_PASS_UNCLAMP (90) -> ENGINE_FAIL_REJECT_GATE (99)

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Automotive_EngineAssembly_ColdTestDiagnostics`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 45,000 to 75,000+ characters of deeply engineered Structured Text.

Save output to `data/swarm_raw/agent_<uuid>.json` and reply: `EVOLUTION COMPLETE: Automotive Engine Cold Test Diagnostics`"""

raw_code = (PART1_DECLARATIONS + PART2_LOGIC + PART3_LOGIC).strip()
code = f"```iec-st\n{raw_code}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": code}
    ]
}

agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"

os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Saved to {filename}")
print(f"Raw ST Code characters: {len(raw_code)}")
print(f"Assistant fenced characters: {len(code)}")
print(f"File size in bytes: {os.path.getsize(filename)}")
