# test_verification.py
import json
import re

with open('data/swarm_raw/agent_011dafac.json', 'r', encoding='utf-8') as f:
    doc = json.load(f)

user_msg = doc['messages'][0]['content']
assistant_msg = doc['messages'][1]['content']

assert assistant_msg.startswith("```iec-st\n"), "Must start with ```iec-st\\n"
assert assistant_msg.endswith("\n```"), "Must end with \\n```"

code = assistant_msg[len("```iec-st\n"):-len("\n```")].strip()

# Strip comments for parity checks
clean_code = re.sub(r'\(\*.*?\*\)', '', code, flags=re.DOTALL)
clean_code = re.sub(r'//.*', '', clean_code)

if_count = len(re.findall(r'\bIF\b', clean_code, re.IGNORECASE))
endif_count = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
for_count = len(re.findall(r'\bFOR\b', clean_code, re.IGNORECASE))
endfor_count = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
case_count = len(re.findall(r'\bCASE\b', clean_code, re.IGNORECASE))
endcase_count = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))

print(f"Code Length: {len(code)} characters")
print(f"Code Lines: {len(code.splitlines())}")
print(f"IF parity: {if_count} IFs, {endif_count} END_IFs")
print(f"FOR parity: {for_count} FORs, {endfor_count} END_FORs")
print(f"CASE parity: {case_count} CASEs, {endcase_count} END_CASEs")

assert if_count == endif_count, f"IF mismatch: {if_count} != {endif_count}"
assert for_count == endfor_count, f"FOR mismatch: {for_count} != {endfor_count}"
assert case_count == endcase_count, f"CASE mismatch: {case_count} != {endcase_count}"

# Check required tags
required_tags = [
    'WT_SEAM_ROLL_1ST_OP_FORCE_101A', 'WT_SEAM_ROLL_1ST_OP_FORCE_101B', 'WT_SEAM_ROLL_1ST_OP_FORCE_101C',
    'WT_SEAM_ROLL_2ND_OP_FORCE_102A', 'WT_SEAM_ROLL_2ND_OP_FORCE_102B', 'WT_SEAM_ROLL_2ND_OP_FORCE_102C',
    'ST_TURRET_RESOLVER_POS_201A', 'ST_TURRET_RESOLVER_POS_201B', 'ST_TURRET_RESOLVER_POS_201C',
    'FT_LN2_MICRODOSE_MASS_301A', 'FT_LN2_MICRODOSE_MASS_301B', 'FT_LN2_MICRODOSE_MASS_301C',
    'PT_CAN_ACOUSTIC_TAP_PRESSURE_401A', 'PT_CAN_ACOUSTIC_TAP_PRESSURE_401B', 'PT_CAN_ACOUSTIC_TAP_PRESSURE_401C',
    'ZT_CHAMBER_PAA_CONC_501A', 'ZT_CHAMBER_PAA_CONC_501B', 'ZT_CHAMBER_PAA_CONC_501C',
    'PT_STERILE_AIR_OVERPRESSURE_601A', 'PT_STERILE_AIR_OVERPRESSURE_601B', 'PT_STERILE_AIR_OVERPRESSURE_601C',
    'TT_SEAM_CHUCK_BEARING_701A', 'TT_SEAM_CHUCK_BEARING_701B', 'TT_SEAM_CHUCK_BEARING_701C'
]
for tag in required_tags:
    assert tag in code, f"Missing required tag: {tag}"

# Check required states
states = [
    'STERILIZATION_CIP_PAA', 'PRESSURE_BARRIER_ESTABLISH', 'INLET_STARWHEEL_PACING',
    'CAN_ELEVATOR_LIFTER_ENGAGE', 'LN2_IN_SEAM_CRYODOSE', 'FIRST_OPERATION_CURL_SEAM',
    'SECOND_OPERATION_HERMETIC_CRIMP', 'ACOUSTIC_TAP_LEAK_TEST', 'HIGH_SPEED_PNEUMATIC_REJECT',
    'DISCHARGE_SYNCHRONIZATION', 'JAM_DETECTION_CONTROLLED_STOP', 'EMERGENCY_DEPRESSURIZATION'
]
for state in states:
    assert state in code, f"Missing required state: {state}"

print("ALL QUALITY CHECKS PASSED WITH 100% PARITY AND ZERO ERRORS!")
