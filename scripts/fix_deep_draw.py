import os

p1_path = "deep_draw_builder/part1_header_io.py"
content = open(p1_path, "r", encoding="utf-8").read()

fb_str = "FUNCTION_BLOCK FB_Mechanical_HeavyPress_2500Ton_DeepDrawCushion_Sync"
# Find and replace
lines = content.splitlines()
new_lines = []
saw_code = False
for l in lines:
    if 'code = """' in l and not saw_code:
        new_lines.append(f'    code = """{fb_str}')
        saw_code = True
    elif fb_str in l:
        # skip second occurrence
        continue
    else:
        new_lines.append(l)

open(p1_path, "w", encoding="utf-8").write("\n".join(new_lines))
print("Fixed part1_header_io.py")

asm_path = "deep_draw_builder/assemble_dataset.py"
asm_lines = open(asm_path, "r", encoding="utf-8").readlines()
target_dir = os.path.abspath("data/swarm_raw").replace("\\", "/")
new_asm = []
for l in asm_lines:
    if "raw_dir =" in l:
        new_asm.append(f'    raw_dir = r"{target_dir}"\n')
    else:
        new_asm.append(l)

open(asm_path, "w", encoding="utf-8").write("".join(new_asm))
print("Fixed assemble_dataset.py")
