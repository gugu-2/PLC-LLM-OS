# -*- coding: utf-8 -*-
"""
Build, validate, and save the complete synthetic dataset JSON for FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding.
"""

import os
import sys
import json
import uuid
import re

sys.path.append('brain_scratch')
from generate_port_crane_block import generate_full_block

def run():
    st_code = generate_full_block()
    
    # Verify mandatory IEC 61131-3 structure
    assert st_code.startswith("FUNCTION_BLOCK FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding"), "Opening declaration failed!"
    assert st_code.strip().endswith("END_FUNCTION_BLOCK"), "Closing declaration failed!"
    assert "VAR_INPUT" in st_code, "VAR_INPUT missing!"
    assert "VAR_OUTPUT" in st_code, "VAR_OUTPUT missing!"
    assert "VAR" in st_code, "VAR missing!"
    assert "END_VAR" in st_code, "END_VAR missing!"
    
    # Parity checks
    clean = re.sub(r'\(\*.*?\*\)', '', st_code, flags=re.DOTALL)
    clean = re.sub(r'\'.*?\'', '', clean)
    
    assert len(re.findall(r'\bFUNCTION_BLOCK\b', clean)) == len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean)), "FB parity mismatch!"
    assert len(re.findall(r'\bVAR\b|\bVAR_INPUT\b|\bVAR_OUTPUT\b', clean)) == len(re.findall(r'\bEND_VAR\b', clean)), "VAR parity mismatch!"
    assert len(re.findall(r'\bIF\b', clean)) == len(re.findall(r'\bEND_IF\b', clean)), "IF parity mismatch!"
    assert len(re.findall(r'\bCASE\b', clean)) == len(re.findall(r'\bEND_CASE\b', clean)), "CASE parity mismatch!"
    assert len(re.findall(r'\bFOR\b', clean)) == len(re.findall(r'\bEND_FOR\b', clean)), "FOR parity mismatch!"
    
    # Form output fenced code
    fenced_output = f"```iec-st\n{st_code}\n```"
    char_count = len(fenced_output)
    line_count = len(fenced_output.splitlines())
    
    print(f"Fenced output characters: {char_count}")
    print(f"Fenced output lines: {line_count}")
    assert char_count >= 50000, f"Character count {char_count} < 50000!"
    
    instruction = """You are generating a SINGLE ultra-dense, mathematically rigorous IEC 61131-3 Structured Text dataset for the **Heavy Maritime Port Logistics & Automated Container Terminals** industry.

**Domain**: Heavy Maritime Port Logistics & Automated Container Terminals: 65-Ton Twin-Lift Automated Ship-to-Shore (STS) Mega-Gantry Container Crane: Active Real-Time Pendulum Wire-Rope Anti-Sway & Skew Damping Control (residual sway angle < 0.10° at 4.0 m/s trolley speed and 1.2 m/s² deceleration), Dual-Hoist 4-Drum Closed-Loop Resolver Leveling Synchronization (1,200 kW vector inverter drives), Laser Lidar Spreader-to-Cell-Guide Dynamic Trajectory Landing & Collision Avoidance, 4-Corner Hydraulic Twistlock Seated & Locked Interlock Verification, and High-Wind Gust Storm Rail Clamp Hydraulic Interlocks.

**Function Block Name**: `FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding`

**Engineering Context & Operational Architecture**:
- 65-Ton twin-lift automated Ship-to-Shore (STS) mega-gantry container crane handling dual 20-foot or single 40/45-foot containers across 65-meter outreach over post-Panamax container vessels.
- Active non-linear spherical pendulum anti-sway control with variable wire rope payout length L(t) and Coriolis acceleration coupling.
- 4-wire reeving torsional skew damping with active headblock hydraulic trim cylinder actuation.
- Dual-hoist 4-drum closed-loop leveling synchronization driven by dual 1,200 kW flux-vector inverters with high-speed resolver feedback.
- 2D laser Lidar spreader centering and collision avoidance for container cell guide entry and quay AGV/chassis landing.
- 4-Corner hydraulic twistlock seated and locked verification at 180 bar manifold pressure with fail-safe mechanical interlocks.
- Multi-tier emergency shutdown with fast (< 50 ms) caliper disc brake drop and high-wind storm rail clamp hydraulic deployment.

**Transmitter & Tag Nomenclature**:
- Standard industrial P&ID tags: `ZT_TROLLEY_ENCODER_101A/B/C`, `ST_TROLLEY_MOTOR_RPM_102A/B/C`, `ZT_HOIST_ROPE_LENGTH_201A/B/C`, `ST_HOIST_MOTOR_RPM_202A/B/C`, `OPT_SPREADER_SWAY_ANGLE_301A/B/C`, `OPT_SPREADER_SKEW_ANGLE_302A/B/C`, `LIDAR_CELL_GUIDE_DIST_401A/B/C`, `WT_SPREADER_LOAD_CELL_501A/B/C`, `PT_TWISTLOCK_HYDR_PRESS_601A/B/C`, `AIT_ANEMOMETER_WIND_SPEED_701A/B/C`, `ZT_RAIL_CLAMP_STATUS_801A/B/C`.

**Required Mathematical Depth & State-Space Formulations**:
1. Discrete State-Space 8x8 Matrix Dynamics (x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k) at 10 ms cycle time.
2. Non-linear spherical pendulum rope dynamics with variable rope length L(t) (ddot{theta} + (2*dot{L}/L)*dot{theta} + (g/L)*sin(theta) = -(ddot{x}/L)*cos(theta) - F_wind/(M*L)).
3. Bluff-body aerodynamic drag modeling on high-cube containers (F_drag = 0.5 * rho_air * C_d * A_proj * (v_wind - v_trolley)^2).
4. 4-wire reeving torsional skew restoring stiffness (K_tors = M_total * g * W^2 / (4*L)).
5. Receding-Horizon Model Predictive Control (MPC) with 3-iteration Projected Gradient Descent.
6. 2oo3 Triple Modular Redundancy (TMR) sensor voting across 11 transducer triplets with discrepancy timers and bumpless degradation.
7. ISA-18.2 5-tier process alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with bit packing into 4 diagnostic words.
8. 12-Stage Operational Finite State Machine (FSM)."""

    uid = uuid.uuid4().hex[:8]
    record_id = f"synthetic_v3_{uid}"
    filename = f"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_{uid}.json"
    
    payload = {
        "id": record_id,
        "instruction": instruction,
        "input": "",
        "output": fenced_output,
        "messages": [
            {"role": "user", "content": instruction},
            {"role": "assistant", "content": fenced_output}
        ],
        "metadata": {
            "domain": "Port_Logistics_Gantry_Cranes",
            "function_block": "FB_Port_STS_GantryCrane_AntiSway_SpreaderLanding",
            "version": "v3_cyberphysical_max",
            "lines": line_count,
            "characters": char_count,
            "validated": True
        }
    }
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)
        
    print(f"SUCCESS: Saved record to {filename}")
    
    # Reload and test json integrity
    with open(filename, "r", encoding="utf-8") as f:
        check = json.load(f)
        assert check["metadata"]["validated"] == True
        assert len(check["output"]) == char_count
        print(f"VERIFIED: JSON load confirmed. Size on disk: {os.path.getsize(filename)} bytes")
        
    return filename, char_count, line_count

if __name__ == "__main__":
    run()
