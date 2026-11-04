# Generator script for FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance
import json
import uuid
import re
import os

def build_dataset():
    uid = uuid.uuid4().hex[:8]
    prompt = """You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol (Principal Automation Fellow & Cyber-Physical Systems Chair).

YOUR LIFECYCLE: GENERATE EXACTLY ONE ULTRA-RIGOROUS FUNCTION BLOCK DATASET, VALIDATE IT, SAVE IT TO A UNIQUE JSON FILE IN `c:\\Users\\majip\\Downloads\\LLM REASEARCH\\data\\swarm_raw\\agent_<uuid>.json`, VERIFY PARITY AND CHARACTER COUNT, AND REPORT COMPLETION.

ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:
- Domain: Green Hydrogen Infrastructure & Industrial Water Electrolysis
- System: 100 MW Multi-Stack Proton Exchange Membrane (PEM) Water Electrolysis Green Hydrogen Facility: 20 x 5 MW Stacks Dynamic Power Splitting & Renewable Wind/Solar Fast Fluctuation Tracking (0–100% ramp in < 5.0 s), Anode Deionized Water Circulating Loop & O2 Degasser Differential Pressure Regulation (30.0 bar ± 0.05 bar cell differential), Cathode H2-in-O2 Gas Permeation Cross-Over Safety Observer (LFL safety margin < 1.5% H2 in O2), 20-Stack Heat Exchanger Thermal Balancing (70.0 °C ± 0.5 °C), and TSA Deoxo/Dryer Dual-Bed Swing Regeneration Pacing.
- Function Block Name: `FB_Hydrogen_PEM_Electrolyzer_100MW_StackPowerBalance`

NEXT-GEN QUALITY REQUIREMENTS (SUPERIOR TO PREVIOUS DATASETS):
1. Transmitter & Tag Nomenclature:
   - Use standardized industrial P&ID tags: `IT_STACK_DC_CURRENT_101A/B/C`, `VT_STACK_DC_VOLTAGE_102A/B/C`, `PT_ANODE_O2_SEPARATOR_201A/B/C`, `PT_CATHODE_H2_SEPARATOR_202A/B/C`, `DP_MEMBRANE_DIFF_PRESS_203A/B/C`, `AIT_H2_IN_O2_CROSSOVER_301A/B/C`, `AIT_O2_IN_H2_CROSSOVER_302A/B/C`, `TT_STACK_COOLING_INLET_401A/B/C`, `TT_STACK_COOLING_OUTLET_402A/B/C`, `FT_DI_WATER_FEED_501A/B/C`, `AIT_DI_WATER_CONDUCTIVITY_502A/B/C`, `PT_TSA_DRYER_BED1_601A/B/C`.
2. Mathematical Depth & State-Space:
   - Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 5 ms cycle modeling: Electrochemical Butler-Volmer activation overpotential, Nernst reversible thermodynamic cell voltage (E_rev(T, P)), Ohm's law membrane proton transport resistance (sigma_PEM = f(lambda, T)), Fick's law hydrogen/oxygen gas crossover diffusive permeation through Nafion membrane, and stack lumped thermal capacitance balance. Explicitly define and calculate matrices.
   - Receding-horizon Model Predictive Control (MPC) quadratic cost functional (J = sum (x-r)^T Q (x-r) + u^T R u + Delta u^T S Delta u) optimizing individual stack thyristor rectifier currents, anode/cathode backpressure valves, and deionized water circulation pump VFDs to maximize system efficiency (eta_LHV > 68%) while strictly keeping H2-in-O2 < 1.5% across rapid solar/wind dropouts.
3. 2oo3 Triple Modular Redundancy (TMR):
   - Cell differential pressure transducers (2oo3 voting with 0.04 bar discrepancy threshold).
   - In-line thermal conductivity / catalytic gas crossover analyzers (2oo3 voting with 0.10% H2 discrepancy limit).
4. ISA-18.2 Alarm Ladder:
   - Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with emergency stack DC breaker fast trip (< 10 ms) and nitrogen inert gas purge auto-blast.
5. Multi-Stage FSM:
   - 12-state state machine: `SYSTEM_OFFLINE_N2_PURGED`, `DI_WATER_FILL_CIRCULATION`, `MEMBRANE_HYDRATION_SOAK`, `CATHODE_ANODE_PRE_PRESSURIZE`, `STACK_MINIMUM_LOAD_START_5PCT`, `RENEWABLE_POWER_FOLLOWING_MPC`, `DEOXO_PURIFICATION_PULSE`, `TSA_BED_DESORPTION_REGEN`, `CROSSOVER_SAFETY_DERATE_HOLD`, `CONTROLLED_DE_ENERGIZATION`, `N2_FLUSH_STANDBY_PARK`, `EMERGENCY_ESTOP_VENT`.
6. Extreme Token Density & Code Completeness:
   - Zero summaries, zero `// ... rest of code`, zero placeholders.
   - 100% exact parity: Every `IF` must have `END_IF;`, every `CASE` must have `END_CASE;`, every `FOR` must have `END_FOR;`.
   - TRIPLE backticks with `iec-st`. Code length MUST be 50,000 to 85,000+ characters of industrial Structured Text."""

    print("Building Structured Text code...")
    return uid, prompt

if __name__ == '__main__':
    uid, prompt = build_dataset()
    print("Dataset generator ready.")
