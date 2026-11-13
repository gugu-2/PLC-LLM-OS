# Assembly and validation script for FB_Pharma_Bioprocess_TFF_Ultrafiltration_Diafiltration
import os, sys, json, uuid, re
from build_biopharma_tff import generate
from var_block import get_var_block
from phase0_builder import get_phase0_code
from phase1_builder import get_phase1_code
from phase2_builder import get_phase2_code
from phase3_builder import get_phase3_code
from phase4_builder import get_phase4_code
from phase5_builder import get_phase5_code

def assemble():
    st_parts = []
    
    # 1. Header, VAR_INPUT, VAR_OUTPUT
    io_parts = generate()
    st_parts.extend(io_parts)
    
    # 2. VAR
    st_parts.append(get_var_block())
    
    # 3. Phase 0
    st_parts.append(get_phase0_code())
    
    # 4. Phase 1
    st_parts.append(get_phase1_code())
    
    # 5. Phase 2
    st_parts.append(get_phase2_code())
    
    # 6. Phase 3
    st_parts.append(get_phase3_code())
    
    # 7. Phase 4
    st_parts.append(get_phase4_code())
    
    # 8. Phase 5
    st_parts.append(get_phase5_code())
    
    # 9. Closing
    st_parts.append("END_FUNCTION_BLOCK")
    
    full_st_code = "\n\n".join(st_parts)
    print("Full ST code assembled. Character count:", len(full_st_code))
    return full_st_code

if __name__ == "__main__":
    code = assemble()
    with open("test_fb.st", "w", encoding="utf-8") as f:
        f.write(code)
    print("Wrote test_fb.st successfully.")
