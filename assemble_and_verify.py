import os
import sys
import json
import uuid
import re

from verify_parity import verify_st_parity
from build_dataset_generator import build_code
from dataset_builder import get_var_input_lines, get_var_output_lines
from dataset_builder_part3 import get_var_internal_lines, get_var_temp_lines
from dataset_builder_logic1 import get_section_safety_lines, get_section_tmr_voting_lines
from dataset_builder_logic2 import get_section_recoater_dsp_lines, get_section_pyrometer_lines, get_section_kalman_lines
from dataset_builder_logic3 import get_section_vapor_plume_lines, get_section_galvo_stitching_lines, get_section_mpc_lines, get_section_degradation_lines, get_section_alarm_engine_lines
from dataset_builder_fsm import get_section_fsm_lines, get_section_output_packing_lines

def assemble():
    all_lines = []
    
    # 1. Header and FB declaration
    all_lines.extend(build_code())
    
    # 2. VAR_INPUT
    all_lines.extend(get_var_input_lines())
    all_lines.append("")
    
    # 3. VAR_OUTPUT
    all_lines.extend(get_var_output_lines())
    all_lines.append("")
    
    # 4. VAR (Internal)
    all_lines.extend(get_var_internal_lines())
    all_lines.append("")
    
    # 5. VAR_TEMP
    all_lines.extend(get_var_temp_lines())
    all_lines.append("")
    
    # 6. Logic Sections
    all_lines.extend(get_section_safety_lines())
    all_lines.extend(get_section_tmr_voting_lines())
    all_lines.extend(get_section_recoater_dsp_lines())
    all_lines.extend(get_section_pyrometer_lines())
    all_lines.extend(get_section_kalman_lines())
    all_lines.extend(get_section_vapor_plume_lines())
    all_lines.extend(get_section_galvo_stitching_lines())
    all_lines.extend(get_section_mpc_lines())
    all_lines.extend(get_section_degradation_lines())
    all_lines.extend(get_section_alarm_engine_lines())
    all_lines.extend(get_section_fsm_lines())
    all_lines.extend(get_section_output_packing_lines())
    
    # 7. Final closing line
    all_lines.append("END_FUNCTION_BLOCK")
    
    code_text = "\n".join(all_lines)
    return code_text

if __name__ == "__main__":
    code = assemble()
    print("Total characters in raw IEC code:", len(code))
    print("Total lines in raw IEC code:", len(code.splitlines()))
    
    # Verify parity
    verify_st_parity(code)
    
    # Check first and last lines
    first_line = code.splitlines()[0].strip()
    last_line = code.splitlines()[-1].strip()
    print("First line:", first_line)
    print("Last line:", last_line)
    assert first_line == "FUNCTION_BLOCK FB_AdditiveManufacturing_MultiLaserPBF_ThermalSync"
    assert last_line == "END_FUNCTION_BLOCK"
    
    print("Assembly verification successful!")
