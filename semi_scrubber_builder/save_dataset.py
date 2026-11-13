# semi_scrubber_builder/save_dataset.py
import os
import sys
import json
import uuid

sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from check_size import assemble
import validate_iec

user_prompt = """Generate a massively comprehensive, production-grade, mathematically complete IEC 61131-3 Structured Text FUNCTION_BLOCK for:

Commercial Sector: Semiconductor Manufacturing & Fab Infrastructure / Ultra-High Purity Toxic Gas & Burn-Wet Scrubber
Function Block Name: FB_Semiconductor_Facility_UltraHighPurity_ToxicGas_BurnWetScrubber

System Scope:
300 mm Semiconductor Fabrication Facility Sub-Fab Hazardous Production Material (HPM) gas delivery system (Silane SiH4, NF3, WF6, Phosphine PH3, Ammonia NH3) and integrated Point-of-Use (POU) Thermal Inward-Fired Burn-Wet Abatement Scrubber. Coaxial double-containment vacuum/nitrogen sweep, methane-oxygen combustion chamber (950 deg C, residence time > 1.2 s, DRE > 99.999%), multi-stage caustic (NaOH) packed-tower scrubbing for HF/HCl/SiF4 absorption, scrubber sump pH and dissolved solids recirculation, and sub-10 ms excess-flow pneumatic emergency shut-off valve (ESOV) interlocks.

Mathematical & Cyber-Physical Requirements:
1. Discrete State-Space Matrices (A, B, C, D) 6x6 system representing:
   - Burn chamber combustion core temperature T_burn [deg C] and heat release [kW]
   - Toxic precursor destruction and removal efficiency DRE [%] and residual effluent [ppb]
   - Scrubber packed-bed differential pressure Delta_P_scrub [Pa] and exhaust draft draft [Pa]
   - Scrubber quench and packed tower caustic recirculation liquid pH [pH]
   - Coaxial gas line outer annulus vacuum/pressure P_annulus [mbar] and leak rate [mbar/min]
   - Gas delivery header mass flow rate [slpm] and cylinder source pressure P_cyl [bar]
2. Receding-Horizon Model Predictive Control (MPC) with unrolled Projected Gradient Descent (PGD) (10 iterations) balancing natural gas / oxygen fuel burner trim valves [%], scrubber caustic dosing metering pump [mL/min], quench cooling water flow valve [%], exhaust draft induced fan VFD [RPM], and coaxial nitrogen purge bleed valve [%].
3. 2oo3 Triple Modular Redundant (TMR) voting logic with discrepancy timers and bumpless degradation across:
   - Burn chamber high-temperature optical infrared pyrometers (Burn_Temp: 1, 2, 3) [deg C]
   - Scrubber exhaust draft differential pressure transmitters (Draft_DP: 1, 2, 3) [Pa]
   - Recirculation sump immersion glass pH electrodes (Sump_pH: 1, 2, 3) [pH]
   - Gas cabinet and valve manifold box toxic gas optical photo-acoustic detectors (Gas_Detect: 1, 2, 3) [ppm]
4. 14-Stage Deterministic Production Finite State Machine:
   - 0: STATE_IDLE
   - 1: STATE_COAXIAL_ANNULUS_VACUUM_HOLD_AND_LEAK_CHECK
   - 2: STATE_SCRUBBER_WATER_FILL_AND_SUMP_PH_PRIME
   - 3: STATE_BURN_CHAMBER_PILOT_SPARK_AND_O2_WARMUP
   - 4: STATE_CHAMBER_TEMPERATURE_EQUILIBRIUM_LOCK_950C
   - 5: STATE_EXHAUST_INDUCED_DRAFT_AIRFLOW_STABILIZATION
   - 6: STATE_GAS_CABINET_PNEUMATIC_ESOV_OPEN_PERMISSIVE
   - 7: STATE_NOMINAL_ABATEMENT_STEADY_STATE_MPC_RUN
   - 8: STATE_HIGH_FLOW_CHAMBER_BURST_TEMPERATURE_BOOST
   - 9: STATE_CAUSTIC_NEUTRALIZATION_DEMAND_SURGE
   - 10: STATE_PROCESS_TOOL_IDLE_TURNDOWN_AND_LOW_FIRE
   - 11: STATE_EMERGENCY_TOOL_TRIP_GAS_VENT_NITROGEN_CHASE
   - 12: STATE_POST_PURGE_BURN_CHAMBER_COOLDOWN
   - 13: STATE_EMERGENCY_TOXIC_GAS_LEAK_OR_FLAME_OUT_TRIP
5. ISA-18.2 Multi-tiered alarm engine (HH, H, L, LL, deadbands) with bit-packed 32-bit DWORD alarm and status words.
6. Target length: >= 85,000 to 140,000+ characters. Zero placeholders, zero truncation comments.
7. Enforce 100% exact delimiter parity: every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
8. Validate code with 'python validate_iec.py' and save the JSON dataset to 'data/swarm_raw/agent_<uuid>.json' using the 3-message schema with system prompt. Report completion when done."""

def main():
    raw_st = assemble()
    code_content = f"```iec-st\n{raw_st}\n```"
    
    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": code_content}
        ]
    }
    
    unique_id = uuid.uuid4().hex[:8]
    filename = f"data/swarm_raw/agent_{unique_id}.json"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, ensure_ascii=False, indent=2)
        
    print(f"Dataset successfully saved to: {filename}")
    print(f"Assistant content character count: {len(code_content)}")
    
    # Run validation
    errs = validate_iec.validate_json_file(filename)
    if errs:
        print("VALIDATION ERRORS:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
        sys.exit(0)

if __name__ == "__main__":
    main()
