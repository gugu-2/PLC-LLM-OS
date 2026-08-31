import json, re
from pathlib import Path

SWARM_DIR = Path("data/swarm_raw")

SAMPLES = [
    "agent_632fc245.json",
    "agent_28effb61.json",
    "agent_5d565c30.json",
    "agent_81e3ae74.json",
    "agent_50dcbfe6.json",
    "agent_cb966ec1.json",
    "agent_03ea2732.json",
    "agent_40bea52a.json",
    "agent_8a2b3cab.json",
    "agent_8339e765.json",
]

FB_PATTERN       = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
END_FB_PATTERN   = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VAR_IN_PATTERN   = re.compile(r'\bVAR_INPUT\b', re.IGNORECASE)
VAR_OUT_PATTERN  = re.compile(r'\bVAR_OUTPUT\b', re.IGNORECASE)
END_IF_PATTERN   = re.compile(r'\bEND_IF\b', re.IGNORECASE)
END_CASE_PATTERN = re.compile(r'\bEND_CASE\b', re.IGNORECASE)
TRIPLE_FENCE     = re.compile(r'^```iec-st', re.MULTILINE)
SINGLE_FENCE     = re.compile(r'^`iec-st', re.MULTILINE)
DOMAIN_RE        = re.compile(r'domain is:\s*(.+?)[\\.\\n\n]', re.IGNORECASE)


def audit(c):
    errs, warns = [], []
    s = 100
    if len(c) < 1500:
        errs.append("QUALITY-01  Length < 1500 chars"); s -= 25
    fb    = len(FB_PATTERN.findall(c))
    endfb = len(END_FB_PATTERN.findall(c))
    if fb == 0:
        errs.append("IEC-01  No FUNCTION_BLOCK keyword"); s -= 20
    if fb > 0 and endfb == 0:
        errs.append("IEC-02  FUNCTION_BLOCK not closed (END_FUNCTION_BLOCK missing)"); s -= 10
    if not VAR_IN_PATTERN.search(c):
        errs.append("IEC-04  VAR_INPUT section missing"); s -= 10
    if not VAR_OUT_PATTERN.search(c):
        errs.append("IEC-05  VAR_OUTPUT section missing"); s -= 10
    if not END_IF_PATTERN.search(c) and not END_CASE_PATTERN.search(c):
        errs.append("IEC-08  No END_IF or END_CASE control flow"); s -= 10
    has3 = bool(TRIPLE_FENCE.search(c))
    has1 = bool(SINGLE_FENCE.search(c))
    if has1 and not has3:
        errs.append("FORMAT-01  Single-backtick fence used (need triple ```)"); s -= 5
    return max(0, s), errs, warns


print("=" * 68)
print("  ROUND 3 -- FRESH 10-SAMPLE RETEST (post-repair verification)")
print("=" * 68)
print()

results = []
for i, fn in enumerate(SAMPLES, 1):
    fp = SWARM_DIR / fn
    with open(fp, "r", encoding="utf-8") as f:
        obj = json.load(f)
    msgs     = obj.get("messages", [])
    user_msg = msgs[0].get("content", "") if msgs else ""
    asst_msg = msgs[1].get("content", "") if len(msgs) > 1 else ""

    sc, errs, warns = audit(asst_msg)
    fb_count = len(FB_PATTERN.findall(asst_msg))
    m = DOMAIN_RE.search(user_msg)
    domain = m.group(1).strip().rstrip(".\\/n")[:60] if m else "Unknown"

    bar = "#" * (sc // 10) + "." * (10 - sc // 10)
    if sc == 100 and not warns:
        tag = "PERFECT"
    elif not errs:
        tag = "PASS"
    else:
        tag = "FAIL"

    print(f"[{i:02d}] {fn}")
    print(f"      Domain : {domain}")
    print(f"      Length : {len(asst_msg):,} chars  |  FBs: {fb_count}")
    print(f"      Score  : [{bar}] {sc}/100  | {tag}")
    for e in errs:
        print(f"      [ERROR] {e}")
    for w in warns:
        print(f"      [WARN]  {w}")
    if not errs and not warns:
        print("      [OK]    Zero errors. All checks passed.")
    print()
    results.append({"fn": fn, "score": sc, "errors": errs, "warns": warns})

pass_count   = sum(1 for r in results if not r["errors"])
perfect      = sum(1 for r in results if r["score"] == 100 and not r["warns"])
avg          = sum(r["score"] for r in results) / len(results)
total_errors = sum(len(r["errors"]) for r in results)

print("=" * 68)
print("  FINAL SUMMARY")
print("=" * 68)
print(f"  Samples analysed  : {len(results)}")
print(f"  Perfect 100%      : {perfect}/{len(results)}  ({100*perfect//len(results)}%)")
print(f"  Pass (no errors)  : {pass_count}/{len(results)}  ({100*pass_count//len(results)}%)")
print(f"  Average score     : {avg:.1f}/100")
print(f"  Total errors found: {total_errors}")
print()
print("  Per-sample scores:")
for r in results:
    bar = "#" * (r["score"] // 10) + "." * (10 - r["score"] // 10)
    if r["score"] == 100 and not r["warns"]:
        tag = "PERFECT"
    elif not r["errors"]:
        tag = "PASS"
    else:
        tag = "FAIL"
    print(f"    [{bar}] {r['score']:3d}%  {tag}  {r['fn']}")
print("=" * 68)
