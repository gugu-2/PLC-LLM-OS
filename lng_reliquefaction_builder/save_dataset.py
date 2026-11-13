# lng_reliquefaction_builder/save_dataset.py
import os
import sys
import json
import uuid

from declarations import get_declarations
from phase1_tmr import get_phase1
from phase2_physics import get_phase2
from phase3_mpc import get_phase3
from phase4_fsm import get_phase4
from phase5_alarms import get_phase5

sys.path.append(os.path.abspath("."))
from validate_iec import validate_json_file

def assemble_code():
    parts = [
        get_declarations(),
        get_phase1(),
        get_phase2(),
        get_phase3(),
        get_phase4(),
        get_phase5()
    ]
    return "\n\n".join(parts)

def build_and_save():
    code = assemble_code()
    print(f"Assembled IEC ST Code: {len(code)} characters, {len(code.splitlines())} lines.")

    user_prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Commercial Marine & Clean Energy Shipping (174,000 m3 LNG Carrier Boil-Off Gas Re-Liquefaction & Cryogenic Fuel Gas Handling System)
FUNCTION BLOCK NAME: FB_Marine_LNG_BoilOffGas_Reliquefaction_Cascade

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles State-Space Model (Ts = 20 ms):
   - 8-State model of LNG boil-off rate (BOR), tank cargo ullage pressure dynamics, Nitrogen reverse Brayton cycle refrigeration loop, multi-stage centrifugal BOG compressor with anti-surge recycling, and plate-fin cryogenic subcooler heat transfer:
     States: x1=LNG Cargo Tank 1 Ullage Vapor Pressure [kPa gauge], x2=LNG Cargo Tank 4 Ullage Vapor Pressure [kPa gauge], x3=BOG Compressor Stage 1 Suction Temperature [degC], x4=BOG Compressor Stage 2 Discharge Pressure [kPa gauge], x5=Nitrogen Compander Expander Outlet Temperature [degC] (Cryogenic -163 degC), x6=Cold Box Subcooled LNG Condensate Temperature [degC], x7=Subcooled LNG Return Header Flow Rate [kg/h], x8=Nitrogen Cycle Loop Mass Inventory [kg].
   - Explicit non-zero matrices: A (8x8), B (8x6), C (6x8), D (6x6), with state propagation x[k+1] = A * x[k] + B * u[k].
   - Steady-state Luenberger / Kalman observer innovation gain matrix L (8x6).

2. Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Receding horizon N = 5 steps, 6 unrolled iterations of PGD.
   - Dynamic compressor surge limit line decoupling: coordinated control between BOG anti-surge bypass valves, high-pressure fuel gas delivery to dual-fuel engines, and Nitrogen cycle compander speed.
   - Actuator constraints: BOG Stage 1 anti-surge valve [0..100%], BOG Stage 2 anti-surge valve [0..100%], Nitrogen compander guide vanes [0..100%], LNG return condensate valve [0..100%], Gas Combustion Unit (GCU) dump valve [0..100%], BOG compressor VFD speed [0..100%]. Slew rate limits on all actuators.

3. 2oo3 (Two-out-of-Three) Triple Modular Redundancy (TMR) Voting:
   - Implement 2oo3 voting across critical sensor channels:
     * Cargo Tank Ullage Vapor Pressure Transmitters (PT_ULLAGE_101A/B/C) [kPa]
     * BOG Compressor Suction Pressure Transmitters (PT_SUCTION_201A/B/C) [kPa]
     * BOG Compressor Discharge Differential Pressure (PDT_DISCH_301A/B/C) [kPa]
     * Cryogenic Nitrogen Cold Box Temperature Sensors (TT_COLD_401A/B/C) [degC]
     * Subcooled LNG Condensate Coriolis Flowmeters (FT_COND_501A/B/C) [kg/h]
   - Discrepancy accumulation timers (threshold 250 ms) and bumpless degradation.

4. Deterministic 14-Stage Marine Cryogenic State Machine (FSM):
   - CASE eState OF:
     0: PORT_STANDBY_AND_WARM_NITROGEN_INERT
     1: REFRIGERATION_COLD_BOX_NITROGEN_DRY_RUN
     2: BOG_COMPRESSOR_LUBE_OIL_AND_SEAL_GAS_LOCK
     3: CARGO_TANK_PRESSURE_EQUILIBRIUM_CHECK
     4: BOG_COMPRESSOR_STAGE1_SPINUP
     5: BOG_COMPRESSOR_STAGE2_AND_ANTI_SURGE_LOCK
     6: NITROGEN_COMPANDER_EXPANSION_CHILLDOWN (-160 degC)
     7: FULL_CONDENSATE_RELIQUEFACTION_OPTIMAL_MPC
     8: DUAL_FUEL_ENGINE_FUEL_GAS_SENDOUT_COORDINATION
     9: GCU_EXCESS_BOG_THERMAL_BURNING_MODE
     10: ROUGH_SEA_SLOSHING_PRESSURE_SURGE_DAMPING
     11: REFRIGERATION_LOOP_HOT_STANDBY_RECYCLE
     12: EMERGENCY_CARGO_MAST_VENT_ISOLATION
     13: SIL-3_QUICK_CLOSING_SAFETY_SHUTDOWN (ESD-1/2)
   - Fully implement every single state transition and logic.

5. ISA-18.2 Process Alarms, Cargo Overpressure SIL-3 Interlock & 32-Bit Telemetry:
   - Cargo tank high vapor pressure automatic GCU light-off and emergency mast venting.
   - 4-tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & STANDARDIZED DATASET FORMAT
- The IEC 61131-3 Structured Text MUST be 85,000 to 140,000+ characters.
- First line: FUNCTION_BLOCK FB_Marine_LNG_BoilOffGas_Reliquefaction_Cascade
- Last line: END_FUNCTION_BLOCK
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Zero placeholders, zero truncation comments, zero // ... rest of code. Every line fully written."""

    assistant_content = f"```iec-st\n{code}\n```"

    record = {
        "messages": [
            {"role": "user", "content": user_prompt},
            {"role": "assistant", "content": assistant_content}
        ]
    }

    os.makedirs("data/swarm_raw", exist_ok=True)
    filename = f"data/swarm_raw/agent_{uuid.uuid4().hex[:8]}.json"

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(record, f, indent=2, ensure_ascii=False)

    print(f"Successfully saved dataset to {filename}")

    # Validate file
    errs = validate_json_file(filename)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print(f"VALIDATION PASSED PERFECTLY ON {filename}!")
        return filename

if __name__ == "__main__":
    build_and_save()
