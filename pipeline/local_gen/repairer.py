"""
repairer.py
===========
Auto-repair module for common IEC 61131-3 content defects.
Fixes FORMAT-01 (single-backtick fence), IEC-01 (missing FB opener),
IEC-02 (missing END_FUNCTION_BLOCK), and escaped newlines.
"""
import re

TRIPLE_FENCE = re.compile(r'^```iec-st',             re.MULTILINE)
SINGLE_FENCE = re.compile(r'^`iec-st',               re.MULTILINE)
FB_PAT       = re.compile(r'\bFUNCTION_BLOCK\b',     re.IGNORECASE)
END_FB_PAT   = re.compile(r'\bEND_FUNCTION_BLOCK\b', re.IGNORECASE)


def repair(content: str, fb_name_hint: str = "FB_IndustrialControl") -> tuple[str, list[str]]:
    """
    Apply all known auto-repairs to generated content.

    Args:
        content:      The raw assistant message content to repair.
        fb_name_hint: A suggested FUNCTION_BLOCK name if one must be injected.

    Returns:
        (repaired_content, list_of_fixes_applied)
    """
    fixes = []
    c = content

    # ── FIX-2: Unescape \\n literals → real newlines ──────────────────────
    if "\\n" in c and "\n" not in c[:100]:
        c = c.replace("\\n", "\n")
        fixes.append("FIX-2: Unescaped \\n literals to real newlines")

    # ── FIX-1: Single-backtick → triple-backtick fence ────────────────────
    if SINGLE_FENCE.search(c) and not TRIPLE_FENCE.search(c):
        c = SINGLE_FENCE.sub("```iec-st", c)
        # Fix closing single backtick on its own line
        c = re.sub(r"\n`\s*$", "\n```", c.rstrip())
        if c.endswith("`") and not c.endswith("```"):
            c = c[:-1] + "```"
        fixes.append("FIX-1: Single-backtick fence → triple-backtick ```iec-st")

    # ── FIX-3: Inject missing FUNCTION_BLOCK opener ───────────────────────
    if not FB_PAT.search(c) and END_FB_PAT.search(c):
        # Try to derive name from END_FUNCTION_BLOCK line
        name_match = re.search(r"END_FUNCTION_BLOCK\s+(\w+)", c, re.IGNORECASE)
        fb_name = name_match.group(1) if name_match else fb_name_hint
        # Insert after opening fence line
        if "```iec-st" in c:
            fence_nl = c.find("\n", c.find("```iec-st"))
            insert_at = fence_nl + 1
        else:
            insert_at = 0
        c = c[:insert_at] + f"FUNCTION_BLOCK {fb_name}\n" + c[insert_at:]
        fixes.append(f"FIX-3: Injected 'FUNCTION_BLOCK {fb_name}' opener")

    # ── FIX-3b: Inject missing FUNCTION_BLOCK when there's no END_FB either
    if not FB_PAT.search(c) and not END_FB_PAT.search(c) and "```iec-st" in c:
        if "VAR_INPUT" in c or "VAR_OUTPUT" in c:
            fence_nl = c.find("\n", c.find("```iec-st"))
            insert_at = fence_nl + 1
            c = c[:insert_at] + f"FUNCTION_BLOCK {fb_name_hint}\n" + c[insert_at:]
            fixes.append(f"FIX-3b: Injected FUNCTION_BLOCK {fb_name_hint} (no FB at all)")

    # ── FIX-4: Inject missing END_FUNCTION_BLOCK before closing fence ─────
    if FB_PAT.search(c) and not END_FB_PAT.search(c):
        last_fence = c.rfind("```")
        if last_fence > 0:
            c = c[:last_fence] + "END_FUNCTION_BLOCK\n" + c[last_fence:]
            fixes.append("FIX-4: Injected END_FUNCTION_BLOCK before closing fence")

    # ── FIX-5: Normalize fence closing (ensure clean ``` at end) ──────────
    if "```iec-st" in c:
        inner_match = re.search(r"```iec-st\n(.*?)(?:```\s*$|$)", c, re.DOTALL)
        if inner_match:
            inner_code = inner_match.group(1).rstrip()
            c = f"```iec-st\n{inner_code}\n```"
            fixes.append("FIX-5: Normalized code fence closing")

    return c, fixes
