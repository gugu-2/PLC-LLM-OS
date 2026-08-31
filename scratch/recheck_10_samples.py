"""
recheck_10_samples.py
=====================
Re-audits a fresh random set of 10 swarm_raw files after the bulk repair.
Scores against 13 checks and prints a clean pass/fail summary.
"""

import json
import re
import os
from pathlib import Path

BASE_DIR  = Path(__file__).resolve().parent.parent
SWARM_DIR = BASE_DIR / "data" / "swarm_raw"

NEW_SAMPLES = [
    "agent_b657f6c6.json",
    "agent_a5dbbb0b.json",
    "agent_e71b2220.json",
    "agent_5456cb98.json",
    "agent_2dd65c7a.json",
    "agent_1ba1a8ba.json",
    "agent_4fd906dc.json",
    "agent_quantum_cryo.json",
    "agent_a079daaf.json",
    "agent_06f3b37b.json",
]

FB_PATTERN       = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
END_FB_PATTERN   = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VAR_IN_PATTERN   = re.compile(r'\bVAR_INPUT\b', re.IGNORECASE)
VAR_OUT_PATTERN  = re.compile(r'\bVAR_OUTPUT\b', re.IGNORECASE)
END_IF_PATTERN   = re.compile(r'\bEND_IF\b', re.IGNORECASE)
END_CASE_PATTERN = re.compile(r'\bEND_CASE\b', re.IGNORECASE)
TRIPLE_FENCE     = re.compile(r'^```iec-st', re.MULTILINE)
SINGLE_FENCE     = re.compile(r'^`iec-st', re.MULTILINE)
REFUSAL_PHRASES  = ["cannot provide", "cannot fulfill", "must decline", "i cannot"]
DOMAIN_RE        = re.compile(r"domain is:\s*(.+?)[\\.\\n\n]", re.IGNORECASE)

def audit(content: str) -> tuple[int, list, list]:
    errors, warnings = [], []
    s = 100

    if len(content) < 1500:
        errors.append(f"QUALITY-01  Length {len(content)} chars < 1500 minimum"); s -= 25

    if any(p in content.lower() for p in REFUSAL_PHRASES):
        errors.append("SAFETY-01   LLM refusal phrase detected"); s -= 40

    fb  = len(FB_PATTERN.findall(content))
    endfb = len(END_FB_PATTERN.findall(content))

    if fb == 0:
        errors.append("IEC-01  FUNCTION_BLOCK keyword missing"); s -= 20
    if fb > 0 and endfb == 0:
        errors.append("IEC-02  FUNCTION_BLOCK opened but END_FUNCTION_BLOCK missing"); s -= 10
    elif abs(fb - endfb) > 1:
        warnings.append(f"IEC-03  FB count ({fb}) != END_FB count ({endfb})"); s -= 5

    if not VAR_IN_PATTERN.search(content):
        errors.append("IEC-04  VAR_INPUT section missing"); s -= 10
    if not VAR_OUT_PATTERN.search(content):
        errors.append("IEC-05  VAR_OUTPUT section missing"); s -= 10

    if not END_IF_PATTERN.search(content) and not END_CASE_PATTERN.search(content):
        errors.append("IEC-08  No END_IF or END_CASE control flow found"); s -= 10

    has_triple = bool(TRIPLE_FENCE.search(content))
    has_single = bool(SINGLE_FENCE.search(content))
    if has_single and not has_triple:
        errors.append("FORMAT-01  Single-backtick `iec-st fence (should be triple ```)"); s -= 5
    elif not has_triple and not has_single:
        warnings.append("FORMAT-02  No iec-st code fence found")

    return max(0, s), errors, warnings


print("=" * 72)
print("  NEW 10-SAMPLE SWARM RECHECK — POST REPAIR VERIFICATION")
print("=" * 72)
print()

results = []
for i, fn in enumerate(NEW_SAMPLES, 1):
    fp = SWARM_DIR / fn
    with open(fp, "r", encoding="utf-8") as f:
        obj = json.load(f)

    msgs     = obj.get("messages", [])
    user_msg = msgs[0].get("content", "") if len(msgs) > 0 else ""
    asst_msg = msgs[1].get("content", "") if len(msgs) > 1 else ""

    sc, errs, warns = audit(asst_msg)
    fb_count = len(FB_PATTERN.findall(asst_msg))

    m = DOMAIN_RE.search(user_msg)
    domain = m.group(1).strip().rstrip(".\\/")[:65] if m else "Unknown"

    status = "PASS" if not errs else "FAIL"
    bar    = "#" * (sc // 10) + "." * (10 - sc // 10)

    print(f"[{i:02d}] {fn}")
    print(f"      Domain : {domain}")
    print(f"      Length : {len(asst_msg):,} chars  | FBs: {fb_count}")
    print(f"      Score  : [{bar}] {sc}/100  | {status}")
    for e in errs:   print(f"      [ERROR] {e}")
    for w in warns:  print(f"      [WARN]  {w}")
    if not errs and not warns:
        print("      [OK]    All checks passed. Zero errors.")
    print()

    results.append({"fn": fn, "score": sc, "errors": errs, "warns": warns})

# Summary
pass_count   = sum(1 for r in results if not r["errors"])
avg_score    = sum(r["score"] for r in results) / len(results)
total_errors = sum(len(r["errors"]) for r in results)
total_warns  = sum(len(r["warns"])  for r in results)
errorless    = sum(1 for r in results if not r["errors"] and not r["warns"])

print("=" * 72)
print("  RECHECK SUMMARY")
print("=" * 72)
print(f"  Samples analysed : {len(results)}")
print(f"  Error-free (100%): {errorless}/{len(results)}  ({100*errorless//len(results)}%)")
print(f"  Passed (no errors): {pass_count}/{len(results)}  ({100*pass_count//len(results)}%)")
print(f"  Average score    : {avg_score:.1f}/100")
print(f"  Total errors     : {total_errors}")
print(f"  Total warnings   : {total_warns}")
print()
print("  Per-sample scores:")
for r in results:
    bar = "#" * (r["score"] // 10) + "." * (10 - r["score"] // 10)
    tag = "PERFECT" if r["score"] == 100 and not r["warns"] else ("PASS" if not r["errors"] else "FAIL")
    print(f"    [{bar}] {r['score']:3d}%  {tag}  {r['fn']}")
print("=" * 72)
