"""
validator.py
============
Quality validator for generated IEC 61131-3 FUNCTION_BLOCKs.
Returns a score (0-100), list of errors, and list of warnings.
Used by both the local generation pipeline and the repair tool.
"""
import re

# ── Patterns ─────────────────────────────────────────────────────────────────
FB_PAT       = re.compile(r'\bFUNCTION_BLOCK\b',     re.IGNORECASE)
END_FB_PAT   = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)
VAR_IN_PAT   = re.compile(r'\bVAR_INPUT\b',          re.IGNORECASE)
VAR_OUT_PAT  = re.compile(r'\bVAR_OUTPUT\b',         re.IGNORECASE)
VAR_PAT      = re.compile(r'\bVAR\b',                re.IGNORECASE)
END_VAR_PAT  = re.compile(r'\bEND_VAR\b',            re.IGNORECASE)
END_IF_PAT   = re.compile(r'\bEND_IF\b',             re.IGNORECASE)
END_CASE_PAT = re.compile(r'\bEND_CASE\b',           re.IGNORECASE)
TRIPLE_FENCE = re.compile(r'^```iec-st',             re.MULTILINE)
SINGLE_FENCE = re.compile(r'^`iec-st',               re.MULTILINE)
REFUSAL_PATS = [
    "cannot provide", "cannot fulfill", "must decline",
    "safety guidelines", "i cannot", "not able to provide",
    "i'm unable", "i am unable",
]

MIN_LENGTH = 1500


def validate(content: str) -> tuple[int, list[str], list[str]]:
    """
    Validates a generated assistant content string.

    Returns:
        (score, errors, warnings)
        score: 0–100 integer quality score
        errors: list of error code strings (failures that reduce score)
        warnings: list of warning strings (non-fatal issues)
    """
    errors   = []
    warnings = []
    score    = 100

    # ── SAFETY-01: LLM refusal ───────────────────────────────────────────────
    lower = content.lower()
    if any(p in lower for p in REFUSAL_PATS):
        errors.append("SAFETY-01  LLM refusal detected in response")
        score -= 40

    # ── QUALITY-01: Minimum length ────────────────────────────────────────────
    if len(content) < MIN_LENGTH:
        errors.append(f"QUALITY-01  Content is {len(content)} chars (min {MIN_LENGTH})")
        score -= 25

    # ── IEC-01: FUNCTION_BLOCK keyword ────────────────────────────────────────
    fb_count   = len(FB_PAT.findall(content))
    endfb_count= len(END_FB_PAT.findall(content))

    if fb_count == 0:
        errors.append("IEC-01  No FUNCTION_BLOCK keyword found")
        score -= 20

    # ── IEC-02: END_FUNCTION_BLOCK closure ────────────────────────────────────
    if fb_count > 0 and endfb_count == 0:
        errors.append("IEC-02  FUNCTION_BLOCK opened but END_FUNCTION_BLOCK missing")
        score -= 10
    elif fb_count > 0 and abs(fb_count - endfb_count) > 1:
        warnings.append(f"IEC-03  FB count ({fb_count}) != END_FB count ({endfb_count})")
        score -= 5

    # ── IEC-04 / IEC-05: VAR_INPUT / VAR_OUTPUT ──────────────────────────────
    if not VAR_IN_PAT.search(content):
        errors.append("IEC-04  VAR_INPUT section missing")
        score -= 10
    if not VAR_OUT_PAT.search(content):
        errors.append("IEC-05  VAR_OUTPUT section missing")
        score -= 10

    # ── IEC-08: Control flow logic ────────────────────────────────────────────
    has_end_if   = bool(END_IF_PAT.search(content))
    has_end_case = bool(END_CASE_PAT.search(content))
    if not has_end_if and not has_end_case:
        errors.append("IEC-08  No END_IF or END_CASE control flow found")
        score -= 10

    # ── FORMAT-01: Code fence format ──────────────────────────────────────────
    has_triple = bool(TRIPLE_FENCE.search(content))
    has_single = bool(SINGLE_FENCE.search(content))
    if has_single and not has_triple:
        errors.append("FORMAT-01  Single-backtick `iec-st fence (should be triple ```)")
        score -= 5
    elif not has_triple and not has_single:
        warnings.append("FORMAT-02  No iec-st code fence found at all")

    return max(0, score), errors, warnings


def is_perfect(content: str) -> bool:
    score, errors, warnings = validate(content)
    return score == 100 and not errors and not warnings


def summary_line(score: int, errors: list, warnings: list) -> str:
    bar = "#" * (score // 10) + "." * (10 - score // 10)
    if score == 100 and not warnings:
        tag = "PERFECT"
    elif not errors:
        tag = "PASS"
    else:
        tag = f"FAIL ({len(errors)} errors)"
    return f"[{bar}] {score:3d}%  {tag}"
