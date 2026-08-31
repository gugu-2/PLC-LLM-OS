"""
analyze_10_samples.py
=====================
Performs a detailed accuracy and quality audit on 10 randomly sampled
swarm_raw dataset files.
"""
import json
import re
import os

SAMPLES = [
    "data/swarm_raw/agent_39255fbd.json",
    "data/swarm_raw/agent_ea212eed.json",
    "data/swarm_raw/agent_8328bd9b.json",
    "data/swarm_raw/agent_c3b3237e.json",
    "data/swarm_raw/agent_c4105b6b.json",
    "data/swarm_raw/agent_0c79cc42.json",
    "data/swarm_raw/agent_7547e94b.json",
    "data/swarm_raw/agent_8a2b3cab.json",
    "data/swarm_raw/agent_cf06adea.json",
    "data/swarm_raw/agent_e0b524a7.json",
]

FB_PATTERN       = re.compile(r'\bFUNCTION_BLOCK\b', re.IGNORECASE)
END_FB_PATTERN   = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VAR_IN_PATTERN   = re.compile(r'\bVAR_INPUT\b', re.IGNORECASE)
VAR_OUT_PATTERN  = re.compile(r'\bVAR_OUTPUT\b', re.IGNORECASE)
VAR_PATTERN      = re.compile(r'\bVAR\b', re.IGNORECASE)
END_VAR_PATTERN  = re.compile(r'\bEND_VAR\b', re.IGNORECASE)
END_IF_PATTERN   = re.compile(r'\bEND_IF\b', re.IGNORECASE)
END_CASE_PATTERN = re.compile(r'\bEND_CASE\b', re.IGNORECASE)
RETURN_PATTERN   = re.compile(r'\bRETURN\b', re.IGNORECASE)
TRIPLE_FENCE     = re.compile(r'^```iec-st', re.MULTILINE)
SINGLE_FENCE     = re.compile(r'^`iec-st', re.MULTILINE)
REFUSAL_PHRASES  = ["cannot provide", "cannot fulfill", "must decline", "safety guidelines", "i cannot"]

print("=" * 80)
print("  10-SAMPLE SWARM DATASET ACCURACY & QUALITY AUDIT")
print("=" * 80)
print()

results = []

for i, path in enumerate(SAMPLES, 1):
    with open(path, "r", encoding="utf-8") as f:
        obj = json.load(f)

    messages = obj.get("messages", [])
    user_msg = messages[0]["content"] if len(messages) > 0 else ""
    asst_msg = messages[1]["content"] if len(messages) > 1 else ""

    errors = []
    warnings = []
    info_notes = []
    score = 100

    # ── CHECK 1: Minimum message count ──────────────────────────────────────
    if len(messages) < 2:
        errors.append("STRUCT-01: Less than 2 messages in record")
        score -= 30

    # ── CHECK 2: Role assignments ────────────────────────────────────────────
    if len(messages) >= 1 and messages[0].get("role") != "user":
        role = messages[0].get("role", "MISSING")
        errors.append(f"STRUCT-02: First message role={role}, expected user")
        score -= 15
    if len(messages) >= 2 and messages[1].get("role") != "assistant":
        role = messages[1].get("role", "MISSING")
        errors.append(f"STRUCT-03: Second message role={role}, expected assistant")
        score -= 15

    # ── CHECK 3: Content length gate (1500 char minimum) ────────────────────
    asst_len = len(asst_msg)
    if asst_len < 1500:
        errors.append(f"QUALITY-01: Content only {asst_len} chars; min is 1500")
        score -= 25

    # ── CHECK 4: FUNCTION_BLOCK presence ────────────────────────────────────
    fb_count = len(FB_PATTERN.findall(asst_msg))
    if fb_count == 0:
        errors.append("IEC-01: No FUNCTION_BLOCK keyword found")
        score -= 20

    # ── CHECK 5: END_FUNCTION_BLOCK (closure check) ─────────────────────────
    end_fb_count = len(END_FB_PATTERN.findall(asst_msg))
    if fb_count > 0 and end_fb_count == 0:
        errors.append("IEC-02: FUNCTION_BLOCK opened but END_FUNCTION_BLOCK missing")
        score -= 10
    elif fb_count != end_fb_count:
        warnings.append(f"IEC-03: Mismatched FUNCTION_BLOCK({fb_count}) vs END_FUNCTION_BLOCK({end_fb_count})")
        score -= 5

    # ── CHECK 6: VAR_INPUT / VAR_OUTPUT presence ─────────────────────────────
    has_var_in  = bool(VAR_IN_PATTERN.search(asst_msg))
    has_var_out = bool(VAR_OUT_PATTERN.search(asst_msg))
    if not has_var_in:
        errors.append("IEC-04: VAR_INPUT section missing")
        score -= 10
    if not has_var_out:
        errors.append("IEC-05: VAR_OUTPUT section missing")
        score -= 10

    # ── CHECK 7: END_VAR balance ─────────────────────────────────────────────
    var_opens = len(VAR_PATTERN.findall(asst_msg))
    var_closes = len(END_VAR_PATTERN.findall(asst_msg))
    if var_opens > 0 and var_closes == 0:
        errors.append("IEC-06: VAR sections opened but no END_VAR found")
        score -= 10
    elif abs(var_opens - var_closes) > 2:
        warnings.append(f"IEC-07: Possible unmatched VAR/END_VAR ({var_opens} opens vs {var_closes} closes)")

    # ── CHECK 8: Control logic (END_IF / END_CASE) ───────────────────────────
    has_end_if   = bool(END_IF_PATTERN.search(asst_msg))
    has_end_case = bool(END_CASE_PATTERN.search(asst_msg))
    if not has_end_if and not has_end_case:
        errors.append("IEC-08: No END_IF or END_CASE logic found (no control flow)")
        score -= 10

    # ── CHECK 9: Code fence format (triple vs single backtick) ───────────────
    has_triple_fence = bool(TRIPLE_FENCE.search(asst_msg))
    has_single_fence = bool(SINGLE_FENCE.search(asst_msg))
    if has_single_fence and not has_triple_fence:
        errors.append("FORMAT-01: Single-backtick fence (`iec-st) used instead of triple (```iec-st)")
        score -= 5
    elif not has_triple_fence and not has_single_fence:
        warnings.append("FORMAT-02: No iec-st code fence found at all")

    # ── CHECK 10: LLM refusal detection ──────────────────────────────────────
    if any(p in asst_msg.lower() for p in REFUSAL_PHRASES):
        errors.append("SAFETY-01: LLM refusal phrase detected in response")
        score -= 40

    # ── CHECK 11: System prompt injection (should NOT be in raw files) ────────
    if len(messages) >= 1 and messages[0].get("role") == "system":
        info_notes.append("INFO-01: System prompt present in raw file (will be re-injected at build)")

    # ── CHECK 12: Domain extraction ──────────────────────────────────────────
    domain_match = re.search(r"domain is:\s*(.+?)[\\.\\n]", user_msg)
    if not domain_match:
        domain_match = re.search(r"domain is:\s*(.+)", user_msg)
    domain = domain_match.group(1).strip().rstrip(".\\n") if domain_match else "Unknown (prompt not tagged)"
    domain = domain[:70]

    # ── CHECK 13: RETURN without E-Stop context (logic smell) ────────────────
    return_count = len(RETURN_PATTERN.findall(asst_msg))
    if return_count > 0:
        info_notes.append(f"INFO-02: {return_count} RETURN statement(s) found (verify not premature exits)")

    score = max(0, score)
    results.append({
        "index": i,
        "file": os.path.basename(path),
        "domain": domain,
        "length": asst_len,
        "fb_count": fb_count,
        "score": score,
        "errors": errors,
        "warnings": warnings,
        "info": info_notes,
    })

    status = "PASS" if not errors else "FAIL"
    print(f"[{i:02d}] {os.path.basename(path)}")
    print(f"      Domain    : {domain}")
    print(f"      Length    : {asst_len:,} chars  |  FUNCTION_BLOCKs: {fb_count}")
    print(f"      Score     : {score}/100  |  Status: {status}")
    for e in errors:
        print(f"      [ERROR] {e}")
    for w in warnings:
        print(f"      [WARN]  {w}")
    for n in info_notes:
        print(f"      [INFO]  {n}")
    print()

# -- SUMMARY ------------------------------------------------------------------
print("=" * 80)
print("  OVERALL SUMMARY")
print("=" * 80)
avg_score = sum(r["score"] for r in results) / len(results)
pass_count = sum(1 for r in results if not r["errors"])
total_errors = sum(len(r["errors"]) for r in results)
total_warnings = sum(len(r["warnings"]) for r in results)
print(f"  Samples Analyzed  : {len(results)}")
print(f"  Clean Pass        : {pass_count}/{len(results)} ({100*pass_count//len(results)}%)")
print(f"  Average Score     : {avg_score:.1f}/100")
print(f"  Total Errors      : {total_errors}")
print(f"  Total Warnings    : {total_warnings}")
print()
print("  Per-sample scores:")
for r in results:
    bar = "█" * (r["score"] // 10) + "░" * (10 - r["score"] // 10)
    status = "PASS" if not r["errors"] else "FAIL"
    print(f"  [{r['index']:02d}] [{bar}] {r['score']:3d}%  {status}  {r['file']}")
print("=" * 80)
