# package_json.py
import json
import uuid

with open('chloralkali_assembled.st', 'r', encoding='utf-8') as f:
    st_code = f.read().strip()

prompt = """You are the Principal Automation Fellow & Cyber-Physical Systems Chair.
Your directive is to generate ONE single, ultra-dense, mathematically rigorous, completely implemented IEC 61131-3 Structured Text dataset for the Lumina PLC-LLM project.

DOMAIN: Chemical & Petrochemical / Chlor-Alkali Industrial Plant
FUNCTION BLOCK NAME: FB_Chemical_ChlorAlkali_MembraneElectrolyzer_DPControl

### SYSTEM SCOPE & INDUSTRIAL PROCESS
Commercial Chlor-Alkali Membrane Cell Electrolyzer System (2.5 kA/m2 current density, bipolar membrane electrolyzers producing Chlorine Gas Cl2, Hydrogen Gas H2, and 32-35 wt% Sodium Hydroxide NaOH). Differential pressure balancing between anolyte compartment (Cl2) and catholyte compartment (H2) must be strictly maintained within +/- 3.0 mbar to prevent irreversible ion-exchange membrane mechanical rupture or catastrophic H2-in-Cl2 explosive cross-contamination.

### MATHEMATICAL & CYBER-PHYSICAL REQUIREMENTS
1. First-Principles Discrete State-Space Model (Ts = 20 ms):
   - 6-State coupled electro-chemo-hydrodynamic model:
     x1 = Catholyte-to-Anolyte differential pressure Delta P [mbar]
     x2 = Chlorine header pressure P_Cl2 [bar gauge]
     x3 = Hydrogen header pressure P_H2 [bar gauge]
     x4 = Anolyte brine feed saturation concentration [g/L NaCl] and depletion rate
     x5 = Catholyte caustic concentration [wt% NaOH] and soft water dilution flow [m3/h]
     x6 = Cell stack bulk temperature [deg C] and polarization voltage drop [V/cell]
   - Explicit non-zero matrices: A (6x6), B (6x5), C (6x6), D (6x5).
   - Luenberger state observer innovation gain matrix L (6x6) with steady-state Kalman filter gains.
2. Receding-Horizon Model Predictive Control (MPC) with Projected Gradient Descent (PGD):
   - Horizon N = 5 steps, 10 unrolled iterations of PGD.
   - 5 Actuator control channels: Hydrogen backpressure control valve [%], Chlorine header vent/scrubber valve [%], soft water catholyte dilution valve [%], anolyte feed brine trim valve [%], and DC rectifier load current setpoint [kA].
   - Actuator physical constraints [u_min, u_max], slew rate limits [Delta u_max], state penalty matrix Q (6x6), terminal state penalty P (6x6), control effort R (5x5), and rate-of-change penalty R_delta (5x5).
3. 2oo3 Triple Modular Redundancy (TMR) Sensor Voting:
   - 2oo3 voting across critical sensor channels:
     * Cell differential pressure transmitters (PDT_Cell_DP_1A/B/C) [mbar]
     * Chlorine header pressure transmitters (PT_Cl2_Header_2A/B/C) [bar]
     * Hydrogen header pressure transmitters (PT_H2_Header_3A/B/C) [bar]
     * Inline Hydrogen-in-Chlorine photometer/analyzers (AT_H2_in_Cl2_4A/B/C) [% vol]
     * Anolyte depleted brine concentration analyzers (AT_Anolyte_NaCl_5A/B/C) [g/L]
     * Catholyte caustic concentration analyzers (AT_Catholyte_NaOH_6A/B/C) [wt%]
   - Discrepancy accumulation timers (threshold 300 ms), degraded 2oo2 voting, 1oo1 single fallback, and fail-safe trip latches.
4. 14-Stage Deterministic Production Finite State Machine (FSM):
   - 0: STATE_IDLE
   - 1: STATE_NITROGEN_PURGE_AND_LEAK_CHECK
   - 2: STATE_BRINE_WARMUP_CIRCULATION
   - 3: STATE_RECTIFIER_POLARIZATION_CURRENT_INIT
   - 4: STATE_RAMP_CURRENT_LOW_LOAD_25PCT
   - 5: STATE_PRESSURE_EQUILIBRATION_TRANSITION
   - 6: STATE_NOMINAL_BASELOAD_PRODUCTION
   - 7: STATE_CAUSTIC_CONCENTRATION_CONTROL_LOOP
   - 8: STATE_BRINE_DEPLETION_FEED_CONTROL
   - 9: STATE_MEMBRANE_HEALTH_VOLTAGE_MONITORING
   - 10: STATE_CONTROLLED_RAMP_DOWN_TURNDOWN
   - 11: STATE_AUTOMATED_SHUTDOWN_POLARIZATION_HOLD
   - 12: STATE_EMERGENCY_DEPRESSURIZATION_SCRUBBER_TRIP
   - 13: STATE_POST_TRIP_NITROGEN_INERT_BLANKET
   - Complete implementation of every transition, permissive check, timer, and action.
5. ISA-18.2 Multi-Tier Process Alarms, Diagnostics & 32-Bit Telemetry:
   - 4-Tier alarm matrix (HH, H, L, LL) with deadband clearance hysteresis for DP, Cl2 pressure, H2 pressure, H2-in-Cl2 analyzer, brine depletion, caustic concentration, cell temperature, and cell voltage.
   - First-out latching root cause mechanism.
   - Bit-packed DWORD telemetry: dwStatusWord1, dwStatusWord2, dwAlarmWord1, dwAlarmWord2, dwFirstOutWord.

### SYNTAX & QUALITY REQUIREMENTS
- Structured Text inside ```iec-st ... ```.
- First line: FUNCTION_BLOCK FB_Chemical_ChlorAlkali_MembraneElectrolyzer_DPControl
- Last line: END_FUNCTION_BLOCK
- 100% exact parity: Every IF has END_IF;, every CASE has END_CASE;, every FOR has END_FOR;.
- SI physical unit brackets on every single variable declaration.
- Massive, exhaustive implementation (target >= 85,000 to 140,000+ characters).
- Zero placeholders, zero truncation comments."""

fence = "```"
asst_content = f"{fence}iec-st\n{st_code}\n{fence}"

record = {
    "messages": [
        {"role": "user", "content": prompt},
        {"role": "assistant", "content": asst_content}
    ]
}

agent_id = uuid.uuid4().hex[:8]
output_filename = f"data/swarm_raw/agent_{agent_id}.json"
with open(output_filename, "w", encoding="utf-8") as f:
    json.dump(record, f, indent=2, ensure_ascii=False)

print(f"Saved dataset to {output_filename}")
print(f"Assistant content length: {len(asst_content)}")
with open("latest_agent_file.txt", "w", encoding="utf-8") as f:
    f.write(output_filename)
