import re

def validate_iec_st(code_text):
    errors = []
    lines = code_text.strip().splitlines()
    
    # 1. First line
    first_line = lines[0].strip()
    if first_line != "FUNCTION_BLOCK FB_GreenAmmonia_HaberBosch_LoopPuritySync":
        errors.append(f"First line mismatch: {first_line}")
        
    # 2. Last line
    last_line = lines[-1].strip()
    if last_line != "END_FUNCTION_BLOCK":
        errors.append(f"Last line mismatch: {last_line}")
        
    # 3. Check blocks
    if "VAR_INPUT" not in code_text or "END_VAR" not in code_text:
        errors.append("VAR_INPUT block missing")
    if "VAR_OUTPUT" not in code_text:
        errors.append("VAR_OUTPUT block missing")
    if "VAR" not in code_text:
        errors.append("VAR block missing")
        
    # 4. Check physical units in VAR_INPUT
    units = ["[bar]", "[deg C]", "[Nm3/h]", "[mol/mol]", "[kW]", "[%]", "[kg/h]", "[m3/h]"]
    for u in units:
        if u not in code_text:
            errors.append(f"Physical unit missing in code: {u}")
            
    # 5. Parity checks (ignoring comments)
    # Strip comments (* ... *)
    no_comments = re.sub(r'\(\*.*?\*\)', '', code_text, flags=re.DOTALL)
    
    # Count IF vs END_IF
    # Words matching IF (not ELSIF, not END_IF)
    if_count = len(re.findall(r'\bIF\b', no_comments))
    elsif_count = len(re.findall(r'\bELSIF\b', no_comments))
    endif_count = len(re.findall(r'\bEND_IF\b', no_comments))
    case_count = len(re.findall(r'\bCASE\b', no_comments))
    endcase_count = len(re.findall(r'\bEND_CASE\b', no_comments))
    for_count = len(re.findall(r'\bFOR\b', no_comments))
    endfor_count = len(re.findall(r'\bEND_FOR\b', no_comments))
    while_count = len(re.findall(r'\bWHILE\b', no_comments))
    endwhile_count = len(re.findall(r'\bEND_WHILE\b', no_comments))
    
    print(f"IF count: {if_count}, END_IF count: {endif_count}")
    print(f"CASE count: {case_count}, END_CASE count: {endcase_count}")
    print(f"FOR count: {for_count}, END_FOR count: {endfor_count}")
    print(f"WHILE count: {while_count}, END_WHILE count: {endwhile_count}")
    
    if if_count != endif_count:
        errors.append(f"IF ({if_count}) and END_IF ({endif_count}) count mismatch!")
    if case_count != endcase_count:
        errors.append(f"CASE ({case_count}) and END_CASE ({endcase_count}) count mismatch!")
    if for_count != endfor_count:
        errors.append(f"FOR ({for_count}) and END_FOR ({endfor_count}) count mismatch!")
    if while_count != endwhile_count:
        errors.append(f"WHILE ({while_count}) and END_WHILE ({endwhile_count}) count mismatch!")
        
    return errors

if __name__ == "__main__":
    from build_iec_code import full_iec_st
    errs = validate_iec_st(full_iec_st)
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
