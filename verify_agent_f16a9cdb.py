# -*- coding: utf-8 -*-
import json

filepath = r"c:/Users/majip/Downloads/LLM REASEARCH/data/swarm_raw/agent_f16a9cdb.json"
with open(filepath, "r", encoding="utf-8") as f:
    data = json.load(f)

print("JSON keys:", list(data.keys()))
print("Metadata:", data["metadata"])
code = data["output"]
print("Code length:", len(code))

assert code.startswith("```iec-st\nFUNCTION_BLOCK FB_Automotive_BIW_GeoFraming_MultiRobotWelding"), "Start mismatch"
assert code.endswith("END_FUNCTION_BLOCK\n```"), "End mismatch"

tags = [
    "ZT_SKID_LIFTER_POS_101A", "ZT_SKID_LIFTER_POS_101B", "ZT_SKID_LIFTER_POS_101C",
    "ST_ROLLER_CONVEYOR_VEL_102A", "ST_ROLLER_CONVEYOR_VEL_102B", "ST_ROLLER_CONVEYOR_VEL_102C",
    "IT_SERVO_GUN_WELD_CURRENT_201A", "IT_SERVO_GUN_WELD_CURRENT_201B", "IT_SERVO_GUN_WELD_CURRENT_201C",
    "WT_SERVO_GUN_TIP_FORCE_202A", "WT_SERVO_GUN_TIP_FORCE_202B", "WT_SERVO_GUN_TIP_FORCE_202C",
    "PT_PNEUMATIC_CLAMP_HEADER_301A", "PT_PNEUMATIC_CLAMP_HEADER_301B", "PT_PNEUMATIC_CLAMP_HEADER_301C",
    "ZT_CLAMP_CYLINDER_RETRACT_302A", "ZT_CLAMP_CYLINDER_RETRACT_302B", "ZT_CLAMP_CYLINDER_RETRACT_302C",
    "ZT_CLAMP_CYLINDER_ADVANCE_303A", "ZT_CLAMP_CYLINDER_ADVANCE_303B", "ZT_CLAMP_CYLINDER_ADVANCE_303C",
    "OPT_LIGHT_CURTAIN_ZONE1_401A", "OPT_LIGHT_CURTAIN_ZONE1_401B", "OPT_LIGHT_CURTAIN_ZONE1_401C",
    "OPT_LASER_SEAM_TRACKER_501A", "OPT_LASER_SEAM_TRACKER_501B", "OPT_LASER_SEAM_TRACKER_501C",
    "TT_TRANSFORMER_WATER_COOL_601A", "TT_TRANSFORMER_WATER_COOL_601B", "TT_TRANSFORMER_WATER_COOL_601C",
    "FT_COOLING_WATER_FLOW_602A", "FT_COOLING_WATER_FLOW_602B", "FT_COOLING_WATER_FLOW_602C"
]

for t in tags:
    assert t in code, f"Missing tag: {t}"
print(f"All {len(tags)} required P&ID sensor tags verified present!")

states = [
    "SYSTEM_OFFLINE_SAFETY_ZONE_CLEAR",
    "SKID_CONVEYOR_TRANSFER_IN",
    "GEO_LIFTER_RAISE_LOCATING_PINS",
    "HYDRAULIC_PNEUMATIC_CLAMP_LOCK",
    "ROBOT_GEO_WELD_PERMIT_INTERLOCK",
    "SYNCHRONOUS_14ROBOT_WELD_CYCLE",
    "LASER_BRAZING_ROOF_SEAM",
    "CLAMP_UNLATCH_SEQUENCE_VERIFY",
    "GEO_LIFTER_LOWER_TO_CONVEYOR",
    "SKID_TRANSFER_OUT_RESPOT",
    "WELD_EXPULSION_QUALITY_ALARM_HOLD",
    "EMERGENCY_ESTOP_ROBOT_HALT"
]

for s in states:
    assert s in code, f"Missing FSM state: {s}"
print(f"All {len(states)} FSM states verified present!")

assert "mat_A" in code and "mat_B" in code and "mat_C" in code and "mat_D" in code
assert "mat_Q" in code and "mat_R" in code and "mat_S" in code and "mat_P" in code
print("State-space and MPC matrices verified!")

print("ALL VERIFICATIONS COMPLETED SUCCESSFULLY 100%!")
