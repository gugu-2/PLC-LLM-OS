import re, os, json, uuid

with open('scratch/code_part1.st', 'r', encoding='utf-8') as f:
    p1 = f.read()
with open('scratch/code_part2.st', 'r', encoding='utf-8') as f:
    p2 = f.read()
with open('scratch/code_part3.st', 'r', encoding='utf-8') as f:
    p3 = f.read()
with open('scratch/code_part4.st', 'r', encoding='utf-8') as f:
    p4 = f.read()

full_code = p1 + p2 + p3 + p4
print(f"Total Combined Code Length: {len(full_code)} characters")

# Strip comments for parity checking
# We need to remove (* ... *) comments carefully
code_no_comments = re.sub(r'\(\*.*?\*\)', '', full_code, flags=re.DOTALL)

# Parity check tokens
# Check IF vs END_IF;
if_matches = re.findall(r'\bIF\b', code_no_comments)
endif_matches = re.findall(r'\bEND_IF\b', code_no_comments)
print(f"IF count: {len(if_matches)}, END_IF count: {len(endif_matches)}")

# Check CASE vs END_CASE;
case_matches = re.findall(r'\bCASE\b', code_no_comments)
endcase_matches = re.findall(r'\bEND_CASE\b', code_no_comments)
print(f"CASE count: {len(case_matches)}, END_CASE count: {len(endcase_matches)}")

# Check FOR vs END_FOR;
for_matches = re.findall(r'\bFOR\b', code_no_comments)
endfor_matches = re.findall(r'\bEND_FOR\b', code_no_comments)
print(f"FOR count: {len(for_matches)}, END_FOR count: {len(endfor_matches)}")

# Check WHILE vs END_WHILE;
while_matches = re.findall(r'\bWHILE\b', code_no_comments)
endwhile_matches = re.findall(r'\bEND_WHILE\b', code_no_comments)
print(f"WHILE count: {len(while_matches)}, END_WHILE count: {len(endwhile_matches)}")

# Check first and last line
lines = [l.strip() for l in full_code.strip().splitlines() if l.strip()]
print(f"First line: {lines[0]}")
print(f"Last line: {lines[-1]}")

assert lines[0] == "FUNCTION_BLOCK FB_Plastics_TwinScrew_ReactiveExtrusion_SlitDie", "First line mismatch"
assert lines[-1] == "END_FUNCTION_BLOCK", "Last line mismatch"
assert len(if_matches) == len(endif_matches), f"IF/END_IF mismatch: {len(if_matches)} vs {len(endif_matches)}"
assert len(case_matches) == len(endcase_matches), f"CASE/END_CASE mismatch: {len(case_matches)} vs {len(endcase_matches)}"
assert len(for_matches) == len(endfor_matches), f"FOR/END_FOR mismatch: {len(for_matches)} vs {len(endfor_matches)}"
assert len(while_matches) == len(endwhile_matches), f"WHILE/END_WHILE mismatch: {len(while_matches)} vs {len(endwhile_matches)}"

print("ALL SYNTAX AND PARITY CHECKS PASSED!")
