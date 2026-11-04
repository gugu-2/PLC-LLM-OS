import os, sys, json, uuid, re

workspace = r"c:\Users\majip\Downloads\LLM REASEARCH"
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scratch"))
sys.path.append(os.path.join(workspace, "Local_Ollama_Evol_Pipeline", "scripts"))

from gen_part1_header import get_header
from gen_part2_io import get_io
from gen_part3_vars import get_vars
from gen_part4_init import get_init_logic
from gen_part5_tmr import get_tmr_logic
from gen_part6_observers import get_observers_logic
from gen_part7_ss_mpc import get_ss_mpc_logic
from gen_part8_fsm import get_fsm_logic
from gen_part9_alarms import get_alarms_logic
from linter import ST_Linter

# Build raw ST code
code_st = (
    get_header().strip() + "\n\n" +
    get_io().strip() + "\n\n" +
    get_vars().strip() + "\n\n" +
    get_init_logic().strip() + "\n\n" +
    get_tmr_logic().strip() + "\n\n" +
    get_observers_logic().strip() + "\n\n" +
    get_ss_mpc_logic().strip() + "\n\n" +
    get_fsm_logic().strip() + "\n\n" +
    get_alarms_logic().strip()
)

# Deep parity checks
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
    "You are an autonomous Senior IEC 61131-3 Synthesis Agent operating under the Lumina Swarm V7 Max-Persona Protocol "
    "(Principal Automation Fellow & Cyber-Physical Systems Chair).\n\n"
    "ASSIGNED DOMAIN & INDUSTRIAL SPECIFICATION:\n"
    "- Domain: Heavy Mining & Mineral Processing\n"
    "- System: 40-Foot 28 MW Gearless Semi-Autogenous Grinding (SAG) Mill & Cyclone Classification Circuit: "
    "Acoustic Shell Ear Microphone Array (dynamic grinding toe position & ball-on-liner impact detection to prevent catastrophic liner fracture), "
    "Ring Motor Direct Torque & Variable Speed Control (6.5–10.2 RPM), Trunnion Bearing High-Pressure Hydraulic Jacking Lift Oil Film Pressure Total Mill Weight Measurement (0.1 ton precision), "
    "Cyclone Feed Sump Slurry Level & Variable Speed Pump Decoupled Flow/Density Control, and 12-Hydrocyclone Battery Cluster Ro-Tap d50 Classification Optimization.\n"
    "- Function Block Name: `FB_Mining_SAGMill_GrindingCircuit_AcousticEar`\n\n"
    "NEXT-GEN QUALITY REQUIREMENTS:\n"
    "1. Transmitter & Tag Nomenclature: Standardized industrial P&ID tags (WT_SAG_FEED_CONVEYOR_101A/B/C, PT_TRUNNION_INLET_BEARING_201A/B/C, "
    "PT_TRUNNION_OUTLET_BEARING_202A/B/C, AIT_ACOUSTIC_EAR_TOE_301A/B/C, AIT_ACOUSTIC_EAR_SHOULDER_302A/B/C, ST_SAG_RING_MOTOR_RPM_401A/B/C, "
    "IT_SAG_MOTOR_POWER_402A/B/C, LT_CYCLONE_SUMP_LEVEL_501A/B/C, DT_CYCLONE_FEED_DENSITY_502A/B/C, PT_CYCLONE_MANIFOLD_503A/B/C).\n"
    "2. Mathematical Depth & State-Space: Full 8x8 discrete state-space formulation (x_{k+1} = A x_k + B u_k, y_k = C x_k + D u_k) at 10 ms cycle modeling "
    "non-linear comminution breakage kinetics (Austin-Herbst grinding rate equation), slurry transport rheology, Plitt hydrocyclone classification efficiency curve (d50c, sharpness index), "
    "and gearless motor electromechanical torsional inertia. Receding-horizon MPC quadratic cost functional (Q, R, S, P) optimizing SAG feed ore rate, mill water addition ratio, ring motor RPM, and cyclone feed pump speed.\n"
    "3. 2oo3 Triple Modular Redundancy (TMR): Trunnion bearing hydraulic lift pressure transmitters (1.8 bar discrepancy threshold), Cyclone feed slurry nuclear gamma density gauges (0.025 SG discrepancy limit), Acoustic sensors, etc.\n"
    "4. ISA-18.2 Alarm Ladder: Full 5-tier alarm hierarchy (HI_HI, HI, LO, LO_LO, ROC) with mill over-filling slurry spill fast trip and acoustic severe shell liner impact auto-slowdown.\n"
    "5. Multi-Stage FSM: 12-state state machine: SYSTEM_OFFLINE_LUBRICATION_WARM, INCHING_DRIVE_ALIGNMENT, RING_MOTOR_ACCELERATION, WATER_FLUSH_STARTUP, LOW_FEED_HOMOGENIZATION, FULL_PRODUCTION_AUTO_MPC, "
    "ACOUSTIC_IMPACT_AUTO_MITIGATION, CYCLONE_CLUSTER_RO_TAP_RECONFIG, SUMP_SURGE_DAMPING, CONTROLLED_GRIND_OUT_SEQUENCE, MILL_CRADLE_PARK, EMERGENCY_ESTOP.\n"
    "6. Extreme Token Density & Code Completeness: Zero summaries, zero placeholders, 100% exact parity, fenced with ```iec-st ... ```."
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
        "domain": "Mining_MineralProcessing",
        "function_block": "FB_Mining_SAGMill_GrindingCircuit_AcousticEar",
        "version": "v3_cyberphysical_max",
        "lines": lines_count,
        "characters": char_count,
        "validated": True
    }
}

with open(filename, "w", encoding="utf-8") as f:
    json.dump(record, f, ensure_ascii=False, indent=2)

print(f"Dataset successfully created and verified!")
print(f"File Path: {filename}")
print(f"Total Lines: {lines_count}")
print(f"Total Characters: {char_count}")
print(f"Parity stats: IF={if_count}, FOR={for_count}, CASE={case_count}")
