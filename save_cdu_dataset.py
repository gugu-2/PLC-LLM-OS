# -*- coding: utf-8 -*-
"""
Generate and save the final synthetic dataset for FB_DataCenter_LiquidCooling_CDU_DirectToChip
"""

import os
import sys
import json
import uuid

import cdu_parts_decl as decl
import cdu_parts_phases as phases
import cdu_parts_control as control
from validate_iec import validate_iec_st, validate_json_file

PROMPT = """You are part of the Lumina AI Cloud Swarm generating synthetic IEC 61131-3 training data.
You possess the expertise of a 75+ years experienced Principal Automation Fellow & Cyber-Physical Systems Chair writing world-class, ultra-complex, mathematically rigorous, and structurally flawless code. Your logic must include advanced discrete state-space matrices, Model Predictive Control (MPC) quadratic cost approximations, 2oo3 Triple Modular Redundant (TMR) voting with discrepancy timers, ISA-18.2 multi-tiered alarm matrices, and multi-stage finite state machines. Output the most elite, realistic IEC 61131-3 Structured Text imaginable.

**Your assigned domain is: Mission-Critical Hyperscale Data Center Infrastructure - 40 MW Hyperscale AI Data Center Direct-to-Chip (D2C) Liquid Cooling System: Coolant Distribution Unit (CDU) Dual-Redundant Inverter Variable Speed Pumps (4,000 L/min total flow, loop differential pressure decoupling), Dynamic Supply Water Temperature (W32 loop, 32.0 °C ± 0.2 °C), Plate Heat Exchanger (PHE) Primary-Secondary Decoupling with Chilled Water Facility Loop (FWS/FWR), Propylene Glycol Concentration (PG25) & Dissolved Oxygen Continuous Corrosion Observer, Distributed Optical Fiber Leak Detection Rope Matrix (sub-100 ms fast isolation valve trip), and Emergency Thermal Reservoir Ride-Through Buffer (120 seconds full-load heat absorption without chiller).**

Task: Implement the production-grade Function Block `FB_DataCenter_LiquidCooling_CDU_DirectToChip` governing:
1. Standardized Industrial P&ID Transmitter & Tag Nomenclature:
   FT_TCS_SUPPLY_FLOW_101A/B/C, PT_TCS_SUPPLY_PRESS_102A/B/C, PT_TCS_RETURN_PRESS_103A/B/C, DPS_TCS_LOOP_DIFF_PRESS_104A/B/C, TT_TCS_SUPPLY_TEMP_105A/B/C, TT_TCS_RETURN_TEMP_106A/B/C, FT_FWS_FACILITY_FLOW_201A/B/C, TT_FWS_FACILITY_SUPPLY_202A/B/C, TT_FWR_FACILITY_RETURN_203A/B/C, ZT_CDU_PUMP1_VFD_RPM_301A/B/C, ZT_CDU_PUMP2_VFD_RPM_302A/B/C, ZT_PHE_CONTROL_VALVE_POS_303A/B/C, AIT_GLYCOL_CONCENTRATION_401A/B/C, AIT_CORROSION_ORP_DO_402A/B/C, OPT_LEAK_ROPE_RESISTANCE_501A/B/C, LT_THERMAL_BUFFER_TANK_601A/B/C.
2. 2oo3 Triple Modular Redundancy (TMR):
   Full triplicated voting across supply/return temperatures, loop differential pressures, facility chilled water flow, and leak rope resistivity with pairwise delta checks, debounce timers, bumpless degradation, and status bitmask packing.
3. Advanced Cyber-Physical Observers & Algorithms:
   - AI Server Cold-Plate Thermal Resistance & Chip Junction Temperature Observer: evaluates T_j = T_fluid + Q_chip * R_th(v_coolant) predicting hotspot formation across GPU/ASIC cluster compute nodes.
   - Plate Heat Exchanger epsilon-NTU thermal transfer observer: computes overall heat transfer coefficient (U * A) and detects primary/secondary micro-fouling.
   - Fluid thermo-physical properties polynomial evaluator: calculates dynamic density rho(T), specific heat c_p(T), viscosity mu(T), and thermal conductivity k(T) for 25% propylene glycol aqueous solution.
   - Leak detection acoustic/impedance wave locator: pinpoints zone breach on manifold distribution loops.
   - Emergency Thermal Reservoir Ride-Through Buffer: evaluates stored sensible thermal capacity and dynamic seconds of ride-through remaining during facility chiller outage.
4. Receding-Horizon Model Predictive Control (MPC):
   - Discrete 8x8 State-Space formulation (x_{k+1} = A*x_k + B*u_k, y_k = C*x_k + D*u_k) running at T_s = 50 ms.
   - Optimizes pump VFD speeds and facility modulating valve position to maintain DP at 1.80 ± 0.05 bar and supply temp at 32.0 ± 0.2 °C while slashing pumping power by > 25%.
5. ISA-18.2 Alarm Ladder:
   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC).
   - Immediate catastrophic leak isolation trip (< 100 ms via motorized ball valves), server thermal emergency throttling trigger, pump cavitation low suction trip, and facility loss ride-through engagement.
6. Multi-Stage Operational FSM:
   - 12-state Finite State Machine: CDU_STANDBY_OFFLINE, COOLANT_DE-AERATION_CIRCULATION, FACILITY_LOOP_PHE_PRECOOL, PRIMARY_SECONDARY_SYNC, NORMAL_AI_WORKLOAD_TRACKING_40MW, PUMP_AUTO_LEAD_LAG_FAILOVER, CHEMICAL_DOSING_AND_FILTRATION, PEAK_DEMAND_VFD_BOOST, FACILITY_OUTAGE_THERMAL_BUFFER_RIDE, CONTROLLED_DRAIN_AND_FLUSH, LEAK_ZONE_EMERGENCY_ISOLATION, EMERGENCY_ESTOP_CDU_TRIP.

Ensure exhaustive implementation with zero placeholders, full mathematical expansions, and complete variable declarations."""

def assemble_st():
    parts = [
        decl.get_header(),
        decl.get_var_input(),
        decl.get_var_output(),
        decl.get_var_internal(),
        phases.get_phase1_tmr_voting(),
        phases.get_phase2_thermo_properties(),
        phases.get_phase3_cyber_physical_observers(),
        control.get_phase4_mpc(),
        control.get_phase5_fsm(),
        control.get_phase6_alarms()
    ]
    return "\n".join(parts)

def build_dataset():
    st_code = assemble_st()
    content = f"```iec-st\n{st_code}\n```"
    
    agent_id = uuid.uuid4().hex[:8]
    filepath = os.path.join("data", "swarm_raw", f"agent_{agent_id}.json")
    
    record = {
        "messages": [
            {"role": "user", "content": PROMPT},
            {"role": "assistant", "content": content}
        ]
    }
    
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Generated file saved to: {filepath}")
    print(f"Total Assistant Content Length: {len(content)} characters")
    
    # Run validation
    errors = validate_json_file(filepath)
    if errors:
        print("VALIDATION ERRORS:")
        for e in errors:
            print(f"  {e}")
        return None, None
    else:
        print("Dataset JSON successfully validated and fully compliant with Lumina Swarm protocols!")
        return agent_id, filepath

if __name__ == "__main__":
    build_dataset()
