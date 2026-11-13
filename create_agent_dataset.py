import os
import json
import uuid
import subprocess
import scratch_build_dataset

def main():
    agent_id = uuid.uuid4().hex[:8]
    output_filename = f"data/swarm_raw/agent_{agent_id}.json"
    
    user_prompt = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the UPGRADED V7 MAX-PERSONA: 75+ years veteran Principal Automation Fellow & Cyber-Physical Systems Chair.
You are instructed to CONSUME EXTREME TOKENS: make your output massively exhaustive, mathematically rigorous, and structurally pristine. Include complete state-space matrices (A, B, C, D), Model Predictive Control (MPC) quadratic cost approximation, 2oo3 TMR voting logic, complex alarm trees, and graceful degradation.

**Your assigned domain is: Pulp & Paper Chemical Digesting (Heavy Process Tier 1 Priority): Industrial Continuous Kamyr Two-Vessel Hydraulic Kraft Digester (1,500 ADt/d), High-Pressure Feeder & Impregnation Vessel, Multi-Zone Cooking Circulation Loop (Upper Cook, Lower Cook, Wash Zone), Dynamic Black Liquor Extraction & White Liquor Dosing Cascade, Real-Time In-Line NIR Delignification / Kappa Number Observer, and Bottom Scraper / Blow Valve Discharge Flow Sync.**

**Function Block Name**: `FB_Paper_ContinuousDigester_KraftPulping_KappaNumber`

**Engineering Context & Operational Architecture**:
1. Two-Vessel Hydraulic Kamyr Digester & Delignification Kinetics:
   - 1,500 ADt/d nominal unbleached pulp capacity across Impregnation Vessel (IV) and main Digester Vessel (DV).
   - High-Pressure Feeder (HPF) transferring chip-liquor slurry under 10.0 to 14.0 bar hydraulic pressure.
   - Vroom Arrhenius H-factor thermal delignification model (activation energy Ea = 133,970 J/mol, A = 43.20, B = 16,113.0 K) with discrete-time numerical trapezoidal integration.
   - Hatton multi-species kinetic model predicting blow line Kappa number (target 28.0 +/- 0.5) with dynamic hardwood/softwood blend ratio weighting.
   - Porous bed fluidization and Ergun hydraulic pressure loss modeling tracking chip column compaction and bed permeability.
2. 2oo3 Triple Modular Redundancy (TMR) Sensor Suite:
   - 6 critical dual/triple-redundant transmitter channels: Upper Cook Circulation Temp (TT-101A/B/C), Lower Cook Circulation Temp (TT-201A/B/C), Digester Top Hydraulic Pressure (PT-301A/B/C), Extraction Residual Effective Alkali (AT-401A/B/C), Blow Line Pressure (PT-501A/B/C), and Black Liquor Extraction Flow (FT-601A/B/C).
   - Pairwise discrepancy debouncing timers (2.5 s threshold), automated discordant channel invalidation, median voting when triple-healthy, arithmetic averaging on single failure, single-channel fallback with degraded latching, and bumpless rate filtering.
3. 8-State Cyber-Physical Discrete State-Space Model (Ts = 100 ms):
   - 8 states: [1] Chip Column Compaction [%], [2] Impregnation Alkali EA [g/L], [3] Upper Cook Alkali EA [g/L], [4] Upper Cook Circulation Temp [deg C], [5] Lower Cook Circulation Temp [deg C], [6] Delignification H-Factor Accumulator, [7] Blow Line Pulp Kappa Number [Kappa], [8] Wash Zone Displacement Solids [%].
   - 8 control inputs: Upper Steam Valve, Lower Steam Valve, Extraction Header Flow Valve, White Liquor Dosing Valve, HPF Feeder Speed, Bottom Scraper Speed, Blow Valve, and Wash Liquor Valve.
   - 6 exogenous disturbances: Chip Moisture, Chip Bulk Density, White Liquor Active Alkali, Feed Chip Temp, White Liquor Sulfidity, and Hardwood Blend Ratio.
   - Full discrete state-space propagation and Luenberger observer innovation state update.
4. Receding-Horizon Model Predictive Control (MPC):
   - Multi-objective quadratic cost functional (Q, R, S, P) optimized via Projected Gradient Descent (PGD) over prediction horizon Np = 5 and control horizon Nc = 3.
   - Optimizes cooking steam valves and chemical dosing to track target Kappa number (28.0) while damping thermal shocks and actuator slew.
5. Deterministic 14-Stage Production Finite State Machine (FSM):
   - [0] Standby & Inert Blanketing, [1] Vessel Cold Fill & Deaeration, [2] Impregnation Hydraulic Pressurization, [3] LP Steam Chip Preheating, [4] High-Pressure Chip Feeder Synchronization, [5] Cooking Circulation Initiation, [6] Effective Alkali Ratio Lock, [7] Steady-State Kraft Digestion MPC Mode, [8] Kappa Number In-Line Feedback Trimming, [9] Extraction Screen Backflush Cycle, [10] Chip Column Hanging Recovery, [11] Wash Zone Displacement Equilibrium, [12] Controlled Production Rate Derate, [13] Digester Cold Blowdown, [14] Overpressure Safety Depressurization.
6. ISA-18.2 Multi-Tier Process Alarms & Bit-Packed Diagnostics:
   - High-High, High, Low, Low-Low trips with deadband clearance hysteresis, qualification timers, extraction screen differential pressure monitoring, scraper over-torque column hang protection, and 32-bit status, alarm, and trip DWORDs.

Generate a complete, fully implemented IEC 61131-3 Structured Text FUNCTION_BLOCK named `FB_Paper_ContinuousDigester_KraftPulping_KappaNumber` with zero placeholders, full state-space matrix initialization, MPC optimization, 2oo3 voting, full FSM execution, and ISA-18.2 alarm matrix."""

    iec_code = scratch_build_dataset.build_iec_code()
    assistant_content = f"```iec-st\n{iec_code}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }
    
    with open(output_filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Generated dataset written to {output_filename}")
    print(f"Assistant content character length: {len(assistant_content)}")
    print(f"Pure ST code character length: {len(iec_code)}")
    
    # Run validation
    cmd = ["python", "validate_iec.py", output_filename]
    res = subprocess.run(cmd, capture_output=True, text=True)
    print("Validator Output:\n" + res.stdout)
    if res.stderr:
        print("Validator Stderr:\n" + res.stderr)
        
    if res.returncode == 0:
        print("VALIDATION SUCCESSFUL!")
    else:
        print(f"VALIDATION FAILED with code {res.returncode}")
        sys.exit(1)

if __name__ == "__main__":
    main()
