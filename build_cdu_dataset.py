# -*- coding: utf-8 -*-
"""
Assembler and validator for FB_DataCenter_LiquidCooling_CDU_DirectToChip
"""

import os
import sys
import json
import uuid
import re

import cdu_parts_decl as decl
import cdu_parts_phases as phases
import cdu_parts_control as control
from validate_iec import validate_iec_st, validate_json_file

def assemble_code():
    parts = [
        decl.get_header(),
        decl.get_var_input(),
        decl.get_var_output(),
        decl.get_var_internal(),
        phases.get_phase1_tmr_voting(),
        phases.get_phase2_thermo_properties(),
        phases.get_phase3_cyber_physical_observers(),
        control.get_phase4_mpc(),
        control.get_phase5_fsm(),
        control.get_phase6_alarms()
    ]
    return "\n".join(parts)

def main():
    code = assemble_code()
    print(f"Total Assembled ST Code Length: {len(code)} characters")
    
    # Run validation
    errors = validate_iec_st(code)
    if errors:
        print("VALIDATION ERRORS FOUND:")
        for err in errors:
            print(f"  - {err}")
        return False
    else:
        print("ALL IEC ST VALIDATION CHECKS PASSED PERFECTLY!")
        return True

if __name__ == "__main__":
    main()
