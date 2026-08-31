"""
repair_all_swarm.py
===================
Applies the same 4 fixes from repair_10_samples.py to EVERY file in data/swarm_raw/.
Produces a full repair report and rebuilds clean files in-place with backups.
"""

import json
import re
import shutil
from pathlib import Path

BASE_DIR   = Path(__file__).resolve().parent.parent
SWARM_DIR  = BASE_DIR / "data" / "swarm_raw"
BACKUP_DIR = BASE_DIR / "data" / "swarm_raw_backup_full"

FB_PATTERN     = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
END_FB_PATTERN = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VAR_IN_PATTERN = re.compile(r'\bVAR_INPUT\b', re.IGNORECASE)
VAR_OUT_PATTERN= re.compile(r'\bVAR_OUTPUT\b', re.IGNORECASE)
END_IF_PATTERN = re.compile(r'\bEND_IF\b', re.IGNORECASE)
END_CASE_PATTERN=re.compile(r'\bEND_CASE\b', re.IGNORECASE)
TRIPLE_FENCE   = re.compile(r'^```iec-st', re.MULTILINE)
SINGLE_FENCE   = re.compile(r'^`iec-st', re.MULTILINE)


def score(content: str) -> tuple[int, list]:
    errors = []
    s = 100
    if len(content) < 1500:
        errors.append("QUALITY-01"); s -= 25
    if not FB_PATTERN.search(content):
        errors.append("IEC-01"); s -= 20
    fb_c = len(FB_PATTERN.findall(content))
    endfb_c = len(END_FB_PATTERN.findall(content))
    if fb_c > 0 and endfb_c == 0:
        errors.append("IEC-02"); s -= 10
    if not VAR_IN_PATTERN.search(content):
        errors.append("IEC-04"); s -= 10
    if not VAR_OUT_PATTERN.search(content):
        errors.append("IEC-05"); s -= 10
    if not END_IF_PATTERN.search(content) and not END_CASE_PATTERN.search(content):
        errors.append("IEC-08"); s -= 10
    has_triple = bool(TRIPLE_FENCE.search(content))
    has_single = bool(SINGLE_FENCE.search(content))
    if has_single and not has_triple:
        errors.append("FORMAT-01"); s -= 5
    return max(0, s), errors


def fix_content(raw: str) -> tuple[str, list]:
    fixes = []
    c = raw

    # FIX-2: Unescape \\n literals -> real newlines
    if '\\n' in c and '\n' not in c[:100]:
        c = c.replace('\\n', '\n')
        fixes.append("FIX-2")

    # FIX-1: Single-backtick fence -> triple-backtick
    if SINGLE_FENCE.search(c) and not TRIPLE_FENCE.search(c):
        c = SINGLE_FENCE.sub('```iec-st', c)
        c = re.sub(r'\n`\s*$', '\n```', c.rstrip())
        if c.endswith('`') and not c.endswith('```'):
            c = c[:-1] + '```'
        fixes.append("FIX-1")

    # FIX-3: Inject missing FUNCTION_BLOCK opener
    if not FB_PATTERN.search(c) and END_FB_PATTERN.search(c):
        endfb_match = re.search(r'END_FUNCTION_BLOCK\s+(\w+)', c, re.IGNORECASE)
        fb_name = endfb_match.group(1) if endfb_match else "FB_IndustrialControl"
        fence_end = c.find('\n', c.find('```iec-st')) if '```iec-st' in c else 0
        insert_pos = fence_end + 1 if fence_end >= 0 else 0
        c = c[:insert_pos] + f"FUNCTION_BLOCK {fb_name}\n" + c[insert_pos:]
        fixes.append("FIX-3")

    # FIX-4: Normalize fence closing
    if '```iec-st' in c:
        m = re.search(r'```iec-st\n(.*?)(?:```\s*$|$)', c, re.DOTALL)
        if m:
            inner = m.group(1).rstrip()
            c = f"```iec-st\n{inner}\n```"
            fixes.append("FIX-4")

    return c, fixes


def main():
    BACKUP_DIR.mkdir(parents=True, exist_ok=True)

    files = sorted(SWARM_DIR.glob("*.json"))
    print(f"Repairing {len(files)} files in {SWARM_DIR}")
    print()

    counters = {
        "total": 0, "already_perfect": 0, "fixed": 0, "still_failing": 0,
        "FIX-1": 0, "FIX-2": 0, "FIX-3": 0, "FIX-4": 0,
    }

    still_failing = []

    for filepath in files:
        counters["total"] += 1

        with open(filepath, "r", encoding="utf-8") as f:
            try:
                obj = json.load(f)
            except json.JSONDecodeError:
                print(f"  [SKIP JSON ERROR] {filepath.name}")
                continue

        messages = obj.get("messages", [])
        if len(messages) < 2:
            print(f"  [SKIP NO MESSAGES] {filepath.name}")
            continue

        asst = messages[1].get("content", "")
        sc_before, err_before = score(asst)

        if sc_before == 100 and not err_before:
            counters["already_perfect"] += 1
            continue

        # Backup and fix
        shutil.copy2(filepath, BACKUP_DIR / filepath.name)
        fixed, applied = fix_content(asst)
        sc_after, err_after = score(fixed)

        for fix in applied:
            if fix in counters:
                counters[fix] += 1

        if applied:
            messages[1]["content"] = fixed
            obj["messages"] = messages
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(obj, f, ensure_ascii=False, indent=2)

        if sc_after == 100:
            counters["fixed"] += 1
        else:
            counters["still_failing"] += 1
            still_failing.append((filepath.name, sc_before, sc_after, err_after))

    # Summary
    print("=" * 64)
    print("  FULL SWARM REPAIR COMPLETE")
    print("=" * 64)
    print(f"  Total files         : {counters['total']}")
    print(f"  Already perfect     : {counters['already_perfect']}")
    print(f"  Fixed to 100%       : {counters['fixed']}")
    print(f"  Still failing       : {counters['still_failing']}")
    print()
    print(f"  Fix-1 applied (fence fix)    : {counters['FIX-1']} files")
    print(f"  Fix-2 applied (newline unescape): {counters['FIX-2']} files")
    print(f"  Fix-3 applied (FB injection) : {counters['FIX-3']} files")
    print(f"  Fix-4 applied (fence close)  : {counters['FIX-4']} files")
    print()

    pass_rate = 100 * (counters['already_perfect'] + counters['fixed']) / counters['total']
    print(f"  OVERALL PASS RATE   : {pass_rate:.1f}%")
    print()

    if still_failing:
        print("  Files still failing after repair:")
        for fn, sb, sa, errs in still_failing:
            print(f"    {fn}: {sb}% -> {sa}%  |  {errs}")
    else:
        print("  ** ALL FILES PASS — 100% CORPUS INTEGRITY **")

    print("=" * 64)
    print(f"  Backups saved to: {BACKUP_DIR}")
    print("  Run build_master_dataset.py to rebuild clean training data.")
    print("=" * 64)


if __name__ == "__main__":
    main()
