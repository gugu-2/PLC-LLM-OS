import sys
import json
import re
import os

def validate_iec_st(code_text):
    errors = []
    lines = [l.strip() for l in code_text.strip().splitlines() if l.strip()]
    if not lines:
        return ["Code text is empty"]
    
    # 1. First line
    first_line = lines[0].strip()
    if not first_line.startswith("FUNCTION_BLOCK FB_"):
        errors.append(f"First line does not start with 'FUNCTION_BLOCK FB_': {first_line}")
        
    # 2. Last line
    last_line = lines[-1].strip()
    if last_line != "END_FUNCTION_BLOCK":
        errors.append(f"Last line mismatch: '{last_line}', expected 'END_FUNCTION_BLOCK'")
        
    # 3. Check blocks
    if "VAR_INPUT" not in code_text or "END_VAR" not in code_text:
        errors.append("VAR_INPUT block missing")
    if "VAR_OUTPUT" not in code_text:
        errors.append("VAR_OUTPUT block missing")
    if "VAR" not in code_text:
        errors.append("VAR block missing")
        
    # 4. Check physical units in VAR_INPUT
    # Look for bracketed units like [bar], [deg], [mm], [kN], [%], [deg C], etc.
    bracket_units = re.findall(r'\[[a-zA-Z0-9/%^°\-_ ]+\]', code_text)
    if len(bracket_units) < 5:
        errors.append(f"Too few physical units found in comments ({len(bracket_units)} found, expected at least 5)")
        
    # 5. Comment parity
    open_comments = code_text.count("(*")
    close_comments = code_text.count("*)")
    if open_comments != close_comments:
        errors.append(f"Comment mismatch: (* count ({open_comments}) != *) count ({close_comments})")

    # 6. Parity checks (ignoring comments and strings)
    no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', code_text)
    clean_code = re.sub(r'\'[^\']*\'', '', no_comments)
    
    ifs = len(re.findall(r'\b(?<!END_)(?<!ELS)IF\b', clean_code, re.IGNORECASE))
    end_ifs = len(re.findall(r'\bEND_IF\b', clean_code, re.IGNORECASE))
    cases = len(re.findall(r'\b(?<!END_)CASE\b', clean_code, re.IGNORECASE))
    end_cases = len(re.findall(r'\bEND_CASE\b', clean_code, re.IGNORECASE))
    fors = len(re.findall(r'\b(?<!END_)FOR\b', clean_code, re.IGNORECASE))
    end_fors = len(re.findall(r'\bEND_FOR\b', clean_code, re.IGNORECASE))
    whiles = len(re.findall(r'\b(?<!END_)WHILE\b', clean_code, re.IGNORECASE))
    end_whiles = len(re.findall(r'\bEND_WHILE\b', clean_code, re.IGNORECASE))
    fb_starts = len(re.findall(r'\b(?<!END_)FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    fb_ends = len(re.findall(r'\bEND_FUNCTION_BLOCK\b', clean_code, re.IGNORECASE))
    
    print(f"Parity Audit:")
    print(f"  IF: {ifs} | END_IF: {end_ifs} (Match: {ifs == end_ifs})")
    print(f"  CASE: {cases} | END_CASE: {end_cases} (Match: {cases == end_cases})")
    print(f"  FOR: {fors} | END_FOR: {end_fors} (Match: {fors == end_fors})")
    print(f"  WHILE: {whiles} | END_WHILE: {end_whiles} (Match: {whiles == end_whiles})")
    print(f"  FUNCTION_BLOCK: {fb_starts} | END_FUNCTION_BLOCK: {fb_ends} (Match: {fb_starts == fb_ends})")
    
    if ifs != end_ifs:
        errors.append(f"IF ({ifs}) and END_IF ({end_ifs}) count mismatch!")
    if cases != end_cases:
        errors.append(f"CASE ({cases}) and END_CASE ({end_cases}) count mismatch!")
    if fors != end_fors:
        errors.append(f"FOR ({fors}) and END_FOR ({end_fors}) count mismatch!")
    if whiles != end_whiles:
        errors.append(f"WHILE ({whiles}) and END_WHILE ({end_whiles}) count mismatch!")
    if fb_starts != fb_ends:
        errors.append(f"FUNCTION_BLOCK ({fb_starts}) and END_FUNCTION_BLOCK ({fb_ends}) count mismatch!")
        
    return errors

def validate_json_file(filepath):
    print(f"Validating dataset file: {filepath}")
    with open(filepath, "r", encoding="utf-8") as f:
        data = json.load(f)
    
    if "messages" not in data or len(data["messages"]) != 2:
        return [f"Invalid structure: messages array must contain exactly 2 items"]
    
    user_msg = data["messages"][0]
    asst_msg = data["messages"][1]
    if user_msg.get("role") != "user" or asst_msg.get("role") != "assistant":
        return ["Message roles must be 'user' and 'assistant'"]
        
    content = asst_msg.get("content", "").replace("\r\n", "\n")
    print(f"Assistant content character count: {len(content)}")
    if len(content) < 3500:
        return [f"Code too short: {len(content)} chars (minimum 3500)"]
        
    if not content.startswith("```iec-st\n"):
        return [f"Content does not start with ```iec-st\\n"]
    if not content.strip().endswith("```"):
        return [f"Content does not end with ```"]
        
    inner_code = content[len("```iec-st\n"):]
    if inner_code.rstrip().endswith("```"):
        inner_code = inner_code.rstrip()[:-3].rstrip()
        
    return validate_iec_st(inner_code)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        target = sys.argv[1]
        if os.path.isfile(target):
            if target.endswith(".json"):
                errs = validate_json_file(target)
            else:
                with open(target, "r", encoding="utf-8") as f:
                    errs = validate_iec_st(f.read())
        else:
            errs = [f"File not found: {target}"]
    else:
        errs = ["No input file specified. Usage: python validate_iec.py <path_to_json_or_st>"]
        
    if errs:
        print("VALIDATION FAILED with errors:")
        for e in errs:
            print(" -", e)
        sys.exit(1)
    else:
        print("ALL VALIDATION CHECKS PASSED PERFECTLY!")
        sys.exit(0)
