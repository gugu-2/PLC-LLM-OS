import os, sys, json, uuid, re

workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scratch"))
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scripts"))

from gen_tvac_dataset import generate_full_st_code
from linter import ST_Linter

# Generate ST code
code_st = generate_full_st_code()

# Deep Parity Verification
clean_code = re.sub(r'\(\*.*?\*\)', '', code_st, flags=re.DOTALL)
clean_code = re.sub(r'//.*', '', clean_code)

if_count = len(re.findall(r'\bIF\b', clean_code, re.IGNORECASE))
endif_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
for_count = len(re.findall(r'\bFOR\b', clean_code, re.IGNORECASE))
endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
case_count = len(re.findall(r'\bCASE\b', clean_code, re.IGNORECASE))
endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

assert if_count == endif_count, f"Mismatched IF/END_IF: {if_count} vs {endif_count}"
assert for_count == endfor_count, f"Mismatched FOR/END_FOR: {for_count} vs {endfor_count}"
assert case_count == endcase_count, f"Mismatched CASE/END_CASE: {case_count} vs {endcase_count}"

valid, msg = ST_Linter.verify_code(code_st)
assert valid, f"Linter error: {msg}"

output_fenced = f"```iec-st\n{code_st}\n```"

instruction_prompt = (
    "Design and implement a mathematically rigorous, deterministic IEC 61131-3 Structured Text FUNCTION_BLOCK "
    "named FB_Aerospace_Spacecraft_TVAC_ThermalVacuumTesting for a Commercial Heavy Aerospace & Satellite Ground Test Systems "
    "Spacecraft Thermal Vacuum Chamber (TVAC) Environmental Simulation Facility (-180.0 °C to +150.0 °C at 10^-6 mbar high vacuum).\n\n"
    "TECHNICAL REQUIREMENTS:\n"
    "1. Standardized P&ID Transmitters (2oo3 Triple Modular Redundancy across 13 channel sets):\n"
    "   - PT_CHAMBER_ROUGH_VAC_101A/B/C [mbar]: Chamber Roughing Vacuum Transmitters (0.50 decade / 25 mbar threshold)\n"
    "   - PT_CHAMBER_HIGH_VAC_PENNING_102A/B/C [mbar]: High-Vacuum Penning Cold Cathode Ionization Gauges (0.20 decade logarithmic threshold)\n"
    "   - TT_SHROUD_ZONE1_TEMP_201A/B/C [deg C]: Thermal Shroud Zone 1 (Floor/Base Plate) Multi-point Cryo Pt100 RTDs (1.0 deg C threshold)\n"
    "   - TT_SHROUD_ZONE2_TEMP_202A/B/C [deg C]: Thermal Shroud Zone 2 (Lower Cylindrical Shell) Pt100 RTDs (1.0 deg C threshold)\n"
    "   - TT_SHROUD_ZONE3_TEMP_203A/B/C [deg C]: Thermal Shroud Zone 3 (Upper Cylindrical Shell) Pt100 RTDs (1.0 deg C threshold)\n"
    "   - TT_SHROUD_ZONE6_TEMP_206A/B/C [deg C]: Thermal Shroud Zone 6 (Zenith/Top Dome) Pt100 RTDs (1.0 deg C threshold)\n"
    "   - TT_PAYLOAD_SKIN_301A/B/C [deg C]: Spacecraft Specimen External MLI Radiator Skin Pt100 RTDs (1.0 deg C threshold)\n"
    "   - TT_PAYLOAD_INTERNAL_302A/B/C [deg C]: Spacecraft Specimen Internal Avionics Core Payload Pt100 RTDs (1.0 deg C threshold)\n"
    "   - QCM_OUTGASSING_RATE_401A/B/C [Hz/h]: Multi-Channel Thermoelectric Quartz Crystal Microbalance In-Situ Outgassing Rate (0.50 Hz/h threshold)\n"
    "   - RAD_SOLAR_SIM_FLUX_501A/B/C [W/m2]: Solar Simulator Xenon Beam Collimated Radiance Pyranometers (15.0 W/m2 threshold)\n"
    "   - FT_LN2_SHROUD_SUPPLY_601A/B/C [kg/h]: Cryogenic Subcooled LN2 Supply Mass Flow Meters (50.0 kg/h threshold)\n"
    "   - PT_GN2_HEATING_LOOP_602A/B/C [bar]: Pressurized GN2 Closed Conditioning Heating Circuit Pressure (0.25 bar threshold)\n"
    "   - ST_TURBOPUMP_ROTOR_RPM_701A/B/C [RPM]: Magnetic Levitation High-Vacuum Turbomolecular Pump Speed (300.0 RPM threshold)\n\n"
    "2. Cyber-Physical Mathematical Formulations & Discrete 8x8 State-Space:\n"
    "   - Full 8x8 discrete state-space formulation (x[k+1] = A x[k] + B u[k], y[k] = C x[k] + D u[k]) at 100 ms cycle time (Ts = 0.100 s):\n"
    "     * Stefan-Boltzmann 4th-power radiative heat transfer in high vacuum (q_rad = eps_eff * sigma * A * (T_shroud^4 - T_skin^4)).\n"
    "     * Multi-surface specular/diffuse enclosure radiosity calculation with Oppenheim radiation network resistance.\n"
    "     * Single-phase subcooled liquid nitrogen boiling heat transfer suppression (Nusselt-Dittus-Boelter Nu = 0.023*Re^0.8*Pr^0.4 inside copper distribution tubes).\n"
    "     * Sauerbrey equation for QCM microbalance volatile mass deposition (Delta_f = -Cf * Delta_m).\n"
    "     * High-vacuum molecular flow conductance (Knudsen number Kn > 1.0, C_duct = (1/12)*pi*v_bar*D^3/L).\n"
    "     * Discrete steady-state Kalman filter observer update for all 8 physical states.\n\n"
    "3. Receding-Horizon Model Predictive Control (MPC):\n"
    "   - Prediction horizon Np = 3, multi-candidate perturbation search across actuator channels.\n"
    "   - Quadratic cost functional J = sum (x - r)^T Q (x - r) + sum (u^T R u + Delta_u^T S Delta_u) + terminal cost.\n"
    "   - Actuator optimization: Subcooled LN2 cryogenic injection valve [0..100%], GN2 electric trim circulation heaters [0..150 kW], "
    "xenon solar simulator thyristor phase [0..100%], turbomolecular pump speed [0..48,000 RPM], and controlled GN2 repressurization valve [0..100%].\n"
    "   - Hard thermal shock barrier constraint: Specimen thermal slew rate strictly limited to |dT/dt| < 2.0 °C/min (0.0333 °C/s).\n\n"
    "4. 12-Stage Operational Finite State Machine (FSM):\n"
    "   - 0: STANDBY_FACILITY_VERIFICATION\n"
    "   - 1: CHAMBER_ROUGHING_PUMPDOWN (to 0.05 mbar)\n"
    "   - 2: CRYOPUMP_HIGH_VACUUM_CROSSOVER (to < 1.0E-5 mbar)\n"
    "   - 3: DEEP_SPACE_COLD_SOAK_CHILLDOWN (Shroud -180 °C with slew limiter)\n"
    "   - 4: COLD_BALANCE_EQUILIBRIUM (|dT/dt| < 0.2 °C/h for > 2 hours)\n"
    "   - 5: ORBITAL_SUNRISE_SOLAR_SIM_RAMP (1.0 Solar Constant 1,366 W/m² ± 1.5%)\n"
    "   - 6: HOT_BALANCE_EQUILIBRIUM (+120 to +150 °C hot case equilibrium)\n"
    "   - 7: THERMAL_CYCLE_TRANSITION_SLEW (Multi-cycle orbital eclipse stress testing)\n"
    "   - 8: OUTGASSING_BAKEOUT_MONITOR (Bakeout at +80 to +125 °C until outgassing rate < 1.5 Hz/h)\n"
    "   - 9: CONTROLLED_GN2_REPRESSURIZATION (Shroud warmed to +15 °C, dry GN2 bleed at dP/dt < 25 mbar/min to 1,013 mbar)\n"
    "   - 10: CLEANROOM_DOOR_UNLOCK_SAFE (Equalized at 1,013 mbar, cleanroom positive pressure permissive, door seal unlock)\n"
    "   - 11: EMERGENCY_DEPRESSURIZATION_ABORT (Fast isolation < 100 ms, heater/solar trip, satellite bus power disconnect, emergency dry GN2 purge)\n\n"
    "5. ISA-18.2 Process Alarms & Diagnostic Status Word Packing:\n"
    "   - 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with deadband hysteresis.\n"
    "   - Emergency safety trips with automatic interlock latching.\n"
    "   - 4x 16-bit diagnostic status words (wDiagnosticWord01..04) bit-packing sensor health, critical trips, operational warnings, and FSM/safety margins.\n\n"
    "OUTPUT FORMAT:\n"
    "Enclose the complete, fully written out IEC 61131-3 Structured Text FUNCTION_BLOCK within triple backticks tagged with iec-st. Zero placeholders or summaries."
)

unique_id = uuid.uuid4().hex[:8]
filename = os.path.join(workspace, "data", "swarm_raw", f"agent_{unique_id}.json")

lines_count = len(code_st.splitlines())
char_count = len(code_st)

record = {
    "id": f"synthetic_v3_{unique_id}",
    "instruction": instruction_prompt,
    "input": "",
    "output": output_fenced,
    "messages": [
        {"role": "user", "content": instruction_prompt},
        {"role": "assistant", "content": output_fenced}
    ],
    "metadata": {
        "domain": "Aerospace_Satellite_Testing_TVAC",
        "function_block": "FB_Aerospace_Spacecraft_TVAC_ThermalVacuumTesting",
        "version": "v3_cyberphysical_max",
        "lines": lines_count,
        "characters": char_count,
        "validated": True
    }
}

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and saved:")
print(f"File: {filename}")
print(f"Lines: {lines_count}")
print(f"Characters: {char_count}")
print(f"Record Keys: {list(record.keys())}")
