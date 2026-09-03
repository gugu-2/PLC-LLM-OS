import json, re
from pathlib import Path

SWARM_DIR = Path("data/swarm_raw")
SAMPLES = [
    "agent_ceb2436d.json", "agent_ecc2ea12.json", "agent_abccc1d2.json",
    "agent_e6410602.json", "agent_56a21018.json",  "agent_2e0a0d1a.json",
    "agent_e4ff708b.json", "agent_82add30b.json",  "agent_f35ebaa7.json",
    "agent_8bab2305.json",
]

FB   = re.compile(r'\bFUNCTION_BLOCK\b',     re.IGNORECASE)
ENDFB= re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VIN  = re.compile(r'\bVAR_INPUT\b',          re.IGNORECASE)
VOUT = re.compile(r'\bVAR_OUTPUT\b',         re.IGNORECASE)
EIF  = re.compile(r'\bEND_IF\b',             re.IGNORECASE)
ECASE= re.compile(r'\bEND_CASE\b',           re.IGNORECASE)
TF3  = re.compile(r'^```iec-st',             re.MULTILINE)
TF1  = re.compile(r'^`iec-st',               re.MULTILINE)
DOM  = re.compile(r'domain is:\s*(.+?)[\\.\\n\n]', re.IGNORECASE)

def audit(c):
    errs, warns, s = [], [], 100
    if len(c) < 1500:
        errs.append("QUALITY-01  Length < 1500 chars"); s -= 25
    fb    = len(FB.findall(c))
    endfb = len(ENDFB.findall(c))
    if fb == 0:
        errs.append("IEC-01  No FUNCTION_BLOCK keyword"); s -= 20
    if fb > 0 and endfb == 0:
        errs.append("IEC-02  END_FUNCTION_BLOCK missing"); s -= 10
    if not VIN.search(c):
        errs.append("IEC-04  VAR_INPUT missing"); s -= 10
    if not VOUT.search(c):
        errs.append("IEC-05  VAR_OUTPUT missing"); s -= 10
    if not EIF.search(c) and not ECASE.search(c):
        errs.append("IEC-08  No END_IF or END_CASE"); s -= 10
    if TF1.search(c) and not TF3.search(c):
        errs.append("FORMAT-01  Single-backtick fence"); s -= 5
    return max(0, s), errs, warns

print("=" * 68)
print("  ROUND 4 -- 10 NEVER-TESTED SAMPLES (all brand new)")
print("=" * 68)
print()

results = []
for i, fn in enumerate(SAMPLES, 1):
    with open(SWARM_DIR / fn, "r", encoding="utf-8") as f:
        obj = json.load(f)
    msgs = obj.get("messages", [])
    um   = msgs[0].get("content", "") if msgs else ""
    am   = msgs[1].get("content", "") if len(msgs) > 1 else ""
    sc, errs, warns = audit(am)
    fb_count = len(FB.findall(am))
    m = DOM.search(um)
    domain = m.group(1).strip()[:55] if m else "Unknown domain"
    bar = "#" * (sc // 10) + "." * (10 - sc // 10)
    tag = "PERFECT" if sc == 100 and not warns else ("PASS" if not errs else "FAIL")

    print(f"[{i:02d}] {fn}")
    print(f"      Domain : {domain}")
    print(f"      Length : {len(am):,} chars  |  FBs: {fb_count}")
    print(f"      Score  : [{bar}] {sc}/100  |  {tag}")
    for e in errs:  print(f"      [ERROR] {e}")
    for w in warns: print(f"      [WARN]  {w}")
    if not errs and not warns:
        print("      [OK]    Zero errors. All checks passed.")
    print()
    results.append({"fn": fn, "score": sc, "errors": errs, "warns": warns})

perfect     = sum(1 for r in results if r["score"] == 100 and not r["warns"])
pass_count  = sum(1 for r in results if not r["errors"])
avg         = sum(r["score"] for r in results) / len(results)
total_errs  = sum(len(r["errors"]) for r in results)

print("=" * 68)
print("  ROUND 4 SUMMARY")
print("=" * 68)
print(f"  Samples        : {len(results)}")
print(f"  Perfect 100%%  : {perfect}/{len(results)}  ({100*perfect//len(results)}%%)")
print(f"  Pass (no errors): {pass_count}/{len(results)}  ({100*pass_count//len(results)}%%)")
print(f"  Average score  : {avg:.1f}/100")
print(f"  Total errors   : {total_errs}")
print()
print("  Per-sample scores:")
for r in results:
    bar = "#" * (r["score"] // 10) + "." * (10 - r["score"] // 10)
    tag = "PERFECT" if r["score"] == 100 and not r["warns"] else ("PASS" if not r["errors"] else "FAIL")
    print(f"    [{bar}] {r['score']:3d}%  {tag}  {r['fn']}")
print("=" * 68)
