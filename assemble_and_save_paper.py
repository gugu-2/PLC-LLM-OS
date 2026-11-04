# assemble_and_save_paper.py
import os
import sys
import json
import uuid
import re
import generate_paper_dataset

def main():
    agent_uuid = uuid.uuid4().hex[:8]
    output_filename = f"agent_{agent_uuid}.json"
    output_dir = os.path.join(os.getcwd(), "data", "swarm_raw")
    os.makedirs(output_dir, exist_ok=True)
    output_path = os.path.join(output_dir, output_filename)
    
    # 1. Generate IEC 61131-3 ST Code
    st_code = generate_paper_dataset.generate_iec_code()
    lines_count = len(st_code.splitlines())
    char_count = len(st_code)
    
    print(f"Generated IEC 61131-3 ST Code:")
    print(f"  Lines: {lines_count}")
    print(f"  Characters: {char_count}")
    
    # 2. Check AST Delimiter Parity
    ok, parity_results = generate_paper_dataset.check_parity(st_code)
    print("\nParity Verification:")
    for k, v in parity_results.items():
        status = "PASS" if v[2] else "FAIL"
        print(f"  {k:25}: {v[0]:4} vs {v[1]:4} -> [{status}]")
        
    if not ok:
        print("\n[ERROR] AST delimiter parity verification failed! Aborting.")
        sys.exit(1)
        
    if char_count < 50000:
        print(f"\n[ERROR] Character count {char_count} is less than required 50,000! Aborting.")
        sys.exit(1)
        
    print("\n[SUCCESS] Code structure and character length validated.")
    
    # 3. Create instruction prompt
    instruction_prompt = """Design and implement a mathematically rigorous, deterministic IEC 61131-3 Structured Text FUNCTION_BLOCK named FB_PulpPaper_Fourdrinier_Headbox_ShoePress_Dryer for a World-Scale 1,800 m/min Multi-Ply Fourdrinier Paper Machine.

TECHNICAL REQUIREMENTS & INDUSTRIAL SPECIFICATION:
1. Industrial Sector & Machine Architecture:
   - Sector: Pulp & Paper Heavy Process Manufacturing (Mass Continuous Web Production).
   - Machine Width: 8,500 mm nominal trim width operating up to 1,800 m/min (30.0 m/s web speed).
   - Subsystems Integrated:
     * Hydraulic Headbox Multi-Channel Consistency Dilution Profiling with Jet-to-Wire Speed Ratio (v_jet / v_wire ~ 1.015) Synchronization and Air Cushion / Liquid Pond Decoupling.
     * Dynamic Slice Lip Thermal Expansion Micro-Actuator Array (8,500 mm wide, 32 CD zones) coupled with CD Thin Stock Consistency Dilution Injection Headers.
     * Multi-Zone Wire Vacuum Dewatering Suction Boxes (Forming Board, Low-Vac, High-Vac Flat Boxes & Suction Couch Roll).
     * Multi-Nip Extended Shoe Press (ENP) Dynamic Linear Load (1,500 kN/m) Balancing with Hydrodynamic Oil Lubrication Film Observer (Vogel Viscosity-Temperature Model).
     * 6-Section 60-Cylinder Steam Dryer Cascade with Stationary Siphon Condensate Evacuation & Blow-Through Steam Recompression Energy Optimization.
     * Cross-Direction (CD) Decoupling: Radiometric Beta-Ray Basis Weight (g/m2) and Infrared Moisture Scanners (32 CD zones).
     * Multi-Roll Soft Calender Induction Thermal Roll Camber Profiling & High-Speed Reel Web Tension Control (450 N/m).

2. Standardized P&ID Transmitters (2oo3 Triple Modular Redundancy across 12 Channel Sets):
   - PT_HEADBOX_TOTAL_HEAD_101A/B/C [kPa]: Headbox Total Head Pressure
   - FT_STOCK_FEED_PUMP_102A/B/C [m3/h]: Stock Fan Pump Volumetric Flow
   - AIT_THIN_STOCK_CONSISTENCY_103A/B/C [%]: Thin Stock Consistency
   - ST_FORMING_WIRE_SPEED_104A/B/C [m/min]: Forming Wire Drive Velocity
   - DPS_WIRE_SUCTION_BOX_201A/B/C [kPa]: Wire Suction Flat Box Vacuum
   - PT_SHOE_PRESS_HYD_PRESSURE_301A/B/C [bar]: Shoe Press Hydraulic Header Pressure
   - WT_SHOE_PRESS_NIP_LOAD_302A/B/C [kN/m]: Shoe Press Linear Nip Load
   - PT_DRYER_SEC1_STEAM_PRESS_401A/B/C [bar]: Dryer Section 1 Steam Pressure
   - PT_DRYER_SEC4_STEAM_PRESS_404A/B/C [bar]: Dryer Section 4 Steam Pressure
   - DPS_DRYER_SIPHON_DIFF_PRESS_407A/B/C [kPa]: Siphon Condensate Evacuation Diff Pressure
   - WT_SCANNER_BASIS_WEIGHT_501A/B/C [g/m2]: Scanner Beta-Ray Basis Weight
   - AT_SCANNER_IR_MOISTURE_502A/B/C [%]: Scanner Infrared Moisture
   - WT_REEL_WEB_TENSION_601A/B/C [N/m]: Reel Web Tension Loadcells
   - OPT_WEB_BREAK_OPTICAL_701A/B/C [BOOL]: Fast Optical Sheet Break Reflectance Sensors

3. Advanced Cyber-Physical Observers & Mathematical Algorithms:
   - Bernoulli Jet Velocity & Jet-to-Wire Speed Ratio Observer:
     * v_jet = Cd * sqrt(2 * g * H_total) where H_total = P_total / (rho * g)
     * Real-time tracking of Jet-to-Wire ratio (target 1.015 +/- 0.005) to control fiber orientation and MD/CD tensile strength ratio.
   - Shoe Press Hydrodynamic Oil Film Observer:
     * Vogel temperature-dependent dynamic viscosity: mu(T) = mu_0 * exp(Beta / (T + T_0)) [Pa*s]
     * In-nip floating belt fluid film thickness: h_film = K_hydro * sqrt(mu * v / P_spec) [um]
     * Critical protection against rubber belt delamination or metal shoe rubbing.
   - Multi-Cylinder Dryer Enthalpy & Evaporative Mass Balance:
     * Latent heat Delta H_vap(P) = 2257.0 - 2.45 * (T_sat - 100.0) [kJ/kg]
     * Evaporation flux m_dot_evap = U * A * (T_steam - T_sheet) / Delta H_vap
     * Sheet dry solids progression tracking: 20% entering press -> 48.5% exiting press -> 94.5% at reel.
   - Cross-Direction (CD) Decoupling & 32-Zone Profile Control:
     * 3-point Toeplitz spatial response model decoupling basis weight dilution valves from moisture.
     * Soft calender induction thermal camber control (16 induction zones).

4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 multivariable state-space formulation (x[k+1] = A x[k] + B u[k]) at Ts = 10 ms.
   - States x in R^8: Headbox Total Head, Pond Level, Consistency, Jet-to-Wire Ratio, Shoe Press Load, Dryer Sec 1-3 Steam, Dryer Sec 4-6 Steam, Reel Basis Weight.
   - Inputs u in R^8: Fan Pump VFD Trim, Air Pad Pressure Valve, Dilution Header Valve, Wire Speed Trim, Shoe Press Proportional Valve, Dryer Steam Valves, Slice Lip Thermal Master.
   - Projected gradient descent optimization with actuator rate penalties and hard saturation constraints.

5. 12-Stage Operational Finite State Machine (FSM):
   - 1: STANDBY_WARM_CIRCULATION
   - 2: DRYER_SECTION_PREHEAT_STEAM
   - 3: WIRE_FABRIC_WASH_AND_START
   - 4: HEADBOX_TOTAL_HEAD_PRIME
   - 5: STOCK_JET_ENGAGEMENT_ON_WIRE
   - 6: VACUUM_DEWATERING_STEPUP
   - 7: SHOE_PRESS_NIP_ENGAGEMENT
   - 8: TAIL_THREADING_VACUUM_TRANSFER
   - 9: FULL_WIDTH_1800MPM_PRODUCTION
   - 10: CROSS_DIRECTION_PROFILE_OPTIMIZE
   - 11: BROKE_RECOVERY_AND_FLUSH
   - 12: EMERGENCY_ESTOP_WEB_BREAK_DUMP

6. ISA-18.2 Process Alarms & Fast Emergency Safeguards:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis.
   - Ultra-fast optical web break interlock (< 15 ms detection):
     * Stock fan pump bypass / fast divert valve to broke pulper
     * Shoe press hydraulic nip emergency opening (< 80 ms fast separation)
     * Dryer steam pressure rapid reduction & blow-through venting
     * Calender roll rapid separation
   - Bit-packed DWORD diagnostic words (Critical Trips, Warnings, Advisory, Machine Health).

OUTPUT FORMAT:
Enclose the complete, fully written out IEC 61131-3 Structured Text FUNCTION_BLOCK within triple backticks tagged with iec-st. Zero placeholders or summaries."""

    formatted_output = f"```iec-st\n{st_code}\n```"
    
    # 4. Construct JSON Record with dual schema compatibility
    record = {
        "id": f"synthetic_v3_{agent_uuid}",
        "instruction": instruction_prompt,
        "input": "",
        "output": formatted_output,
        "messages": [
            {"role": "user", "content": instruction_prompt},
            {"role": "assistant", "content": formatted_output}
        ],
        "metadata": {
            "domain": "Pulp_Paper_Heavy_Process_Manufacturing",
            "system": "World-Scale 1,800 m/min Multi-Ply Fourdrinier Paper Machine",
            "function_block": "FB_PulpPaper_Fourdrinier_Headbox_ShoePress_Dryer",
            "version": "v3_cyberphysical_max",
            "lines": lines_count,
            "characters": char_count,
            "validated": True
        }
    }
    
    # 5. Write to isolated JSON file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)
        
    file_size = os.path.getsize(output_path)
    print(f"\nSuccessfully written dataset to: {output_path}")
    print(f"File size on disk: {file_size} bytes")
    
    # 6. Re-read and verify parseability
    with open(output_path, "r", encoding="utf-8") as f:
        loaded = json.load(f)
        
    assert loaded["id"] == f"synthetic_v3_{agent_uuid}"
    assert len(loaded["output"]) > 50000
    assert len(loaded["messages"]) == 2
    assert loaded["metadata"]["validated"] is True
    print("\nVerification of written JSON file: 100% OK!")
    print(f"SUMMARY: agent_{agent_uuid}.json | Chars: {char_count} | Lines: {lines_count} | Parity: 100% PASS")

if __name__ == "__main__":
    main()
