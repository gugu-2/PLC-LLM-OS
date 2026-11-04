import os, sys, json, uuid, re

# Verification helper for ST language parity
def verify_st_syntax(code: str):
    issues = []
    # Check opening/closing
    if not code.strip().startswith("FUNCTION_BLOCK FB_Water_Wastewater_Bardenpho_MBR_Aeration"):
        issues.append("First line must be FUNCTION_BLOCK FB_Water_Wastewater_Bardenpho_MBR_Aeration")
    if not code.strip().endswith("END_FUNCTION_BLOCK"):
        issues.append("Last line must be END_FUNCTION_BLOCK")

    # Strip comments to check control structure parity
    # Strip (* ... *) comments
    code_no_comments = re.sub(r'\(\*[\s\S]*?\*\)', '', code)
    # Strip // ... comments
    code_no_comments = re.sub(r'//.*', '', code_no_comments)

    # Word-boundary matching for control structures
    # IF vs END_IF
    if_count = len(re.findall(r'\bIF\b', code_no_comments, re.IGNORECASE))
    end_if_count = len(re.findall(r'\bEND_IF\b', code_no_comments, re.IGNORECASE))
    if if_count != end_if_count:
        issues.append(f"IF count ({if_count}) does not match END_IF count ({end_if_count})")

    # CASE vs END_CASE
    case_count = len(re.findall(r'\bCASE\b', code_no_comments, re.IGNORECASE))
    end_case_count = len(re.findall(r'\bEND_CASE\b', code_no_comments, re.IGNORECASE))
    if case_count != end_case_count:
        issues.append(f"CASE count ({case_count}) does not match END_CASE count ({end_case_count})")

    # FOR vs END_FOR
    for_count = len(re.findall(r'\bFOR\b', code_no_comments, re.IGNORECASE))
    end_for_count = len(re.findall(r'\bEND_FOR\b', code_no_comments, re.IGNORECASE))
    if for_count != end_for_count:
        issues.append(f"FOR count ({for_count}) does not match END_FOR count ({end_for_count})")

    # VAR vs END_VAR
    var_count = len(re.findall(r'\bVAR\b', code_no_comments, re.IGNORECASE))
    var_input_count = len(re.findall(r'\bVAR_INPUT\b', code_no_comments, re.IGNORECASE))
    var_output_count = len(re.findall(r'\bVAR_OUTPUT\b', code_no_comments, re.IGNORECASE))
    var_in_out_count = len(re.findall(r'\bVAR_IN_OUT\b', code_no_comments, re.IGNORECASE))
    total_var_opens = var_count + var_input_count + var_output_count + var_in_out_count
    end_var_count = len(re.findall(r'\bEND_VAR\b', code_no_comments, re.IGNORECASE))
    if total_var_opens != end_var_count:
        issues.append(f"Total VAR opens ({total_var_opens}) does not match END_VAR count ({end_var_count})")

    return issues

print("Verifier defined successfully.")
