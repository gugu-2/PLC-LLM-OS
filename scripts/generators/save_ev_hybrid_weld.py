import os, json, uuid
import build_ev_hybrid_weld
import validate_iec

prompt = """You are generating a SINGLE ultra-dense IEC 61131-3 Structured Text dataset for the **Automotive EV Chassis & Lightweight Materials** industry.

**Domain**: Automated Electric Vehicle (EV) Skateboard Chassis High-Strength Aluminum Subframe Robot Laser-GMAW Hybrid Welding Cell with 3D Seam Tracking & Molten Pool Thermography.

**Function Block Name**: `FB_Automotive_EV_Chassis_LaserArcHybridWelding`

**Engineering Context**:
- Structural 6000/7000-series high-strength extruded aluminum alloy front/rear suspension subframe welding for 800V EV platforms
- Laser-GMAW (Gas Metal Arc Welding) hybrid process: 8 kW fiber laser (1070 nm) combined with cold metal transfer (CMT) wire feed (1.2 mm AlMg5 wire, wire feed speed 6 to 14 m/min)
- 6-axis articulated welding robot (payload 165 kg) synchronized with 2-axis servo positioning tilt-rotator table (coordinated motion velocity up to 2.5 m/min)
- Laser optical triangulation seam tracker (Scansonic / Servo-Robot) running 20 mm ahead of TCP providing dynamic trajectory offset corrections (resolution 0.05 mm)
- Real-time melt pool co-axial pyrometry and high-speed CMOS vision tracking keyhole stability and root penetration
- Shielding gas composition management (Ar/He gas mix, 25 to 45 L/min) with thermal mass flow controller
- AWS D1.2 / ISO 15614-14 structural aluminum welding standards compliance, EN ISO 13849-1 Cat 4 / PLe safety logic

**Required Mathematical Rigor** (ALL must be explicitly coded with complete equations and matrix constants):
1. **Discrete State-Space Matrix Model** for weld seam tracking error, thermal dissipation & wire feed arc current:
   - State vector x = [tracking_lateral_error_mm, tracking_vertical_error_mm, weld_pool_peak_temp_deg, arc_current_amperes]
   - Full numerical matrices A (4×4) and B (4×3 robot TCP trim / wire feed speed / laser power commands)
   - Dynamic propagation: x_{k+1} = A*x_k + B*u_k evaluated at 2ms fast welding loop
2. **Model Predictive Control (MPC) Quadratic Cost Approximation**:
   - Weld penetration depth and seam tracking minimization across variable gap joint tolerances (0.2 to 1.8 mm root opening)
   - Q matrix (4×4 seam error penalty) and R matrix (3×3 laser power and wire speed slew rate penalty)
   - Terminal cost matrix P (4×4)
3. **2oo3 (Two-out-of-Three) Triple Modular Redundant (TMR) Voting**:
   - 3 optical laser triangulation tracking profile samples across the weld joint groove
   - Discrepancy trip (0.25 mm limit) with automated trajectory hold and optical cover glass spatter clean cycle
4. **ISA-18.2 Multi-Tiered Alarm Ladder**:
   - Arc current stability deviation: HH (320 A burn-through trip), H (280 A), LL (95 A arc blowout abort)
   - Optical cover slide transmission: L (75% spatter warning), LL (60% immediate laser shutter close)
   - Shielding gas flow: LL (< 18 L/min porosity risk trip)
5. **Multi-Stage Finite State Machine (FSM)**:
   - States: CELL_STANDBY_IDLE (0) -> SUBFRAME_FIXTURE_CLAMP (10) -> SEAM_TRACKER_LASER_SEARCH (20) -> GAS_PRE_PURGE_FLOW (30) -> HYBRID_ARC_STRIKE_KEYHOLE (40) -> CONTINUOUS_HYBRID_WELD_TRAJECTORY (50) -> CRATER_FILL_DECEL (60) -> GAS_POST_PURGE_FLOW (70) -> POST_WELD_OPTICAL_AUDIT (80) -> FIXTURE_UNCLAMP_DISCHARGE (90) -> ARC_BLOWOUT_EMERGENCY_ESTOP (99)

**Output Format**:
- Code fenced with TRIPLE backticks and `iec-st`: ` ```iec-st `
- First line: `FUNCTION_BLOCK FB_Automotive_EV_Chassis_LaserArcHybridWelding`
- Last line: `END_FUNCTION_BLOCK`
- Minimum length: 45,000 to 75,000+ characters of deeply engineered Structured Text."""

code_st = build_ev_hybrid_weld.get_code()
assistant_content = f"```iec-st\n{code_st}\n```"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": assistant_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
filename = f"data/swarm_raw/agent_{agent_id}.json"
os.makedirs("data/swarm_raw", exist_ok=True)
with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and written to {filename}")
print(f"Assistant content character count: {len(assistant_content)}")

# Validate the generated file with validate_iec
errs = validate_iec.validate_json_file(filename)
if errs:
    print("VALIDATION ERRORS FOUND:")
    for e in errs:
        print(" -", e)
    sys.exit(1)
else:
    print(f"VALIDATION PASSED PERFECTLY FOR {filename}!")
    with open("LAST_SAVED_FILENAME.txt", "w") as lf:
        lf.write(filename)
