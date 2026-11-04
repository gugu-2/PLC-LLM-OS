# -*- coding: utf-8 -*-
import json
import re

filename = "data/swarm_raw/agent_4737b369.json"
with open(filename, "r", encoding="utf-8") as f:
    data = json.load(f)

assert "messages" in data, "messages key missing!"
assert len(data["messages"]) == 2, "must have user and assistant messages!"
assert data["messages"][0]["role"] == "user"
assert data["messages"][1]["role"] == "assistant"

code = data["messages"][1]["content"]

assert code.startswith("```iec-st\n"), "Start fence mismatch"
assert code.strip().endswith("END_FUNCTION_BLOCK\n\n```") or code.strip().endswith("END_FUNCTION_BLOCK\n```"), "End fence mismatch"

# Comments
open_comments = code.count("(*")
close_comments = code.count("*)")
print(f"Comments: (* = {open_comments}, *) = {close_comments}")
assert open_comments == close_comments, "Unbalanced comments!"

# Tags
required_tags = [
    "ST_VIRTUAL_MASTER_ELS_SPEED_101A", "ST_VIRTUAL_MASTER_ELS_SPEED_101B", "ST_VIRTUAL_MASTER_ELS_SPEED_101C",
    "ZT_WEB_INLET_TENSION_DANCER_102A", "ZT_WEB_INLET_TENSION_DANCER_102B", "ZT_WEB_INLET_TENSION_DANCER_102C",
    "WT_INFEED_TENSION_LOADCELL_103A", "WT_INFEED_TENSION_LOADCELL_103B", "WT_INFEED_TENSION_LOADCELL_103C",
    "OPT_REGISTER_CYAN_DEV_201A", "OPT_REGISTER_CYAN_DEV_201B", "OPT_REGISTER_CYAN_DEV_201C",
    "OPT_REGISTER_MAGENTA_DEV_202A", "OPT_REGISTER_MAGENTA_DEV_202B", "OPT_REGISTER_MAGENTA_DEV_202C",
    "OPT_REGISTER_YELLOW_DEV_203A", "OPT_REGISTER_YELLOW_DEV_203B", "OPT_REGISTER_YELLOW_DEV_203C",
    "OPT_REGISTER_BLACK_DEV_204A", "OPT_REGISTER_BLACK_DEV_204B", "OPT_REGISTER_BLACK_DEV_204C",
    "AIT_DAMPENING_CONDUCTIVITY_301A", "AIT_DAMPENING_CONDUCTIVITY_301B", "AIT_DAMPENING_CONDUCTIVITY_301C",
    "TT_DAMPENING_CHILL_TEMP_302A", "TT_DAMPENING_CHILL_TEMP_302B", "TT_DAMPENING_CHILL_TEMP_302C",
    "TT_DRYER_ZONE1_TEMP_401A", "TT_DRYER_ZONE1_TEMP_401B", "TT_DRYER_ZONE1_TEMP_401C",
    "TT_DRYER_ZONE2_TEMP_402A", "TT_DRYER_ZONE2_TEMP_402B", "TT_DRYER_ZONE2_TEMP_402C",
    "TT_DRYER_ZONE3_TEMP_403A", "TT_DRYER_ZONE3_TEMP_403B", "TT_DRYER_ZONE3_TEMP_403C",
    "TT_DRYER_ZONE4_TEMP_404A", "TT_DRYER_ZONE4_TEMP_404B", "TT_DRYER_ZONE4_TEMP_404C",
    "AIT_DRYER_SOLVENT_LEL_405A", "AIT_DRYER_SOLVENT_LEL_405B", "AIT_DRYER_SOLVENT_LEL_405C",
    "TT_CHILL_ROLL_SURFACE_TEMP_501A", "TT_CHILL_ROLL_SURFACE_TEMP_501B", "TT_CHILL_ROLL_SURFACE_TEMP_501C",
    "ZT_CHILL_WEB_TENSION_502A", "ZT_CHILL_WEB_TENSION_502B", "ZT_CHILL_WEB_TENSION_502C",
    "ST_SPLICER_NEW_ROLL_RPM_601A", "ST_SPLICER_NEW_ROLL_RPM_601B", "ST_SPLICER_NEW_ROLL_RPM_601C",
    "ZT_SPLICER_PASTER_KNIFE_POS_602A", "ZT_SPLICER_PASTER_KNIFE_POS_602B", "ZT_SPLICER_PASTER_KNIFE_POS_602C",
    "OPT_WEB_BREAK_ULTRASONIC_701A", "OPT_WEB_BREAK_ULTRASONIC_701B", "OPT_WEB_BREAK_ULTRASONIC_701C"
]
for t in required_tags:
    assert t in code, f"Missing tag {t}"
print(f"All {len(required_tags)} required industrial P&ID tags confirmed present!")

# FSM States
required_states = [
    "PRESS_STANDBY_INCHING",
    "INK_WATER_PRE_EMULSIFY",
    "WEB_THREADING_LOW_SPEED",
    "ELS_VIRTUAL_LINE_SHAFT_LOCK",
    "DRYER_AND_CHILL_PREHEAT_RUN",
    "SPEED_RAMP_TO_50K_CPH",
    "AUTO_REGISTER_CLOSED_LOOP",
    "CONTINUOUS_FLYING_SPLICE",
    "INK_DENSITY_MICRO_REGULATE",
    "CONTROLLED_DECEL_AND_WASH",
    "WEB_SEVER_AND_CLAMP_CLEARED",
    "EMERGENCY_ESTOP_BLANKET_LIFT"
]
for s in required_states:
    assert s in code, f"Missing state {s}"
print(f"All {len(required_states)} FSM states confirmed present!")

# Strip comments & strings for AST parity
clean_code = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
clean_code = re.sub(r'\'[^\']*\'', '', clean_code)

ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
assert ifs == end_ifs, f"IF parity mismatch: {ifs} vs {end_ifs}"

cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
assert cases == end_cases, f"CASE parity mismatch: {cases} vs {end_cases}"

fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
assert fors == end_fors, f"FOR parity mismatch: {fors} vs {end_fors}"

vars_start = len(re.findall(r'\b(?<!END_)(?:VAR|VAR_INPUT|VAR_OUTPUT|VAR_IN_OUT|VAR_TEMP)\b', clean_code, re.IGNORECASE))
vars_end = len(re.findall(r'\bEND_VAR\b', clean_code, re.IGNORECASE))
assert vars_start == vars_end, f"VAR parity mismatch: {vars_start} vs {vars_end}"

fb_start = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
fb_end = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
assert fb_start == 1 and fb_end == 1, f"FB parity mismatch: {fb_start} vs {fb_end}"

print(f"AST Parity Audited: IF={ifs}/{end_ifs}, CASE={cases}/{end_cases}, FOR={fors}/{end_fors}, VAR={vars_start}/{vars_end}, FB={fb_start}/{fb_end}")
print(f"Total Character Length: {len(code):,} characters")
print(f"Total Lines: {len(code.splitlines()):,} lines")
print("VERIFICATION COMPLETE: 100% SUCCESS!")
