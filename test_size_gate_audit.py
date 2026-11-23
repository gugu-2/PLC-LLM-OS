"""
test_size_gate_audit.py — Comprehensive Audit Suite for size_gate.py
Audits:
1. Size categorization boundary logic
2. Split points calculation and semantic boundaries
3. End-to-end segmentation on synthetic >700k char dataset
4. Context preservation and zero-loss reconstruction verification
5. End-to-end segmentation on real-world raw dataset
"""

import os
import sys
import json
import re
import shutil
from pathlib import Path

# Add workspace to path
workspace_dir = Path(__file__).resolve().parent
sys.path.insert(0, str(workspace_dir))

from size_gate import (
    categorize_size,
    find_split_points,
    segment_dataset,
    STUB_THRESHOLD,
    EXTENDED_THRESHOLD,
    ULTRA_DENSE_THRESHOLD,
    SEGMENT_SIZE_TARGET,
    PHASE_BOUNDARY_PATTERNS
)

def run_categorization_tests():
    print("\n=======================================================")
    print("1. AUDITING SIZE CATEGORIZATION LOGIC")
    print("=======================================================")

    test_cases = [
        # (char_count, expected_category, description)
        (0, "stub", "Zero characters"),
        (1, "stub", "1 character"),
        (50_000, "stub", "Mid stub"),
        (99_999, "stub", "Stub upper boundary minus 1"),
        (100_000, "standard", "Standard lower boundary (exact 100k)"),
        (100_001, "standard", "Standard lower boundary plus 1"),
        (225_000, "standard", "Mid standard"),
        (350_000, "standard", "Standard upper boundary (exact 350k)"),
        (350_001, "extended", "Extended lower boundary (350k + 1)"),
        (500_000, "extended", "Mid extended"),
        (700_000, "extended", "Extended upper boundary (exact 700k)"),
        (700_001, "ultra_dense", "Ultra-dense lower boundary (700k + 1)"),
        (850_000, "ultra_dense", "Typical ultra-dense (~850k)"),
        (1_200_000, "ultra_dense", "Extreme ultra-dense (>1.2M)"),
    ]

    passed = 0
    failed = 0
    for chars, expected, desc in test_cases:
        actual = categorize_size(chars)
        status = "PASS" if actual == expected else "FAIL"
        if status == "PASS":
            passed += 1
            print(f"  [{status}] {desc:<40} chars={chars:>9,} -> expected='{expected}', got='{actual}'")
        else:
            failed += 1
            print(f"  [{status}] {desc:<40} chars={chars:>9,} -> EXPECTED='{expected}', GOT='{actual}'")

    print(f"\nCategorization Tests: {passed} passed, {failed} failed.")
    assert failed == 0, f"{failed} categorization tests failed!"
    return passed, failed


def run_split_points_tests():
    print("\n=======================================================")
    print("2. AUDITING SPLIT POINTS ALGORITHM")
    print("=======================================================")

    # Test monotonic increase and boundary coverage
    dummy_text = "line 1\nline 2\n" * 50_000 # ~700k chars
    splits = find_split_points(dummy_text, target_size=100_000)

    print(f"  Dummy text len: {len(dummy_text):,}")
    print(f"  Calculated splits: {splits}")

    assert splits[0] == 0, "First split must be index 0"
    assert splits[-1] == len(dummy_text), f"Last split must be len(content) ({len(dummy_text)})"
    assert all(splits[i] < splits[i+1] for i in range(len(splits)-1)), "Splits must be strictly monotonically increasing"

    # Verify no gap between slices
    reconstructed = "".join(dummy_text[splits[i]:splits[i+1]] for i in range(len(splits)-1))
    assert reconstructed == dummy_text, "Direct concatenation of raw slices must have zero loss!"
    print("  [PASS] Contiguity and zero index loss verified across slice partitions.")

    # Test phase boundary pattern snapping
    pattern_text = (
        ("A" * 200_000) + "\n"
        "(* =========================================\n"
        "   PHASE 02: TMR VOTING MATRIX\n"
        "   ========================================= *)\n"
        + ("B" * 300_000)
    )
    splits_pat = find_split_points(pattern_text, target_size=250_000)
    print(f"  Phase boundary search text len: {len(pattern_text):,}")
    print(f"  Phase boundary detected split: {splits_pat}")
    
    # Check that split 1 snapped to the start of the phase comment
    expected_split_idx = 200_001  # right after newline
    assert splits_pat[1] == expected_split_idx, f"Expected split at {expected_split_idx}, got {splits_pat[1]}"
    print("  [PASS] Semantic Phase Boundary snapping verified.")
    return True


def run_synthetic_ultradense_test():
    print("\n=======================================================")
    print("3. AUDITING SYNTHETIC ULTRA-DENSE DATASET (>700K CHARS)")
    print("=======================================================")

    test_dir = Path("scratch/audit_test_data")
    test_dir.mkdir(parents=True, exist_ok=True)
    out_dir = Path("scratch/audit_test_segments")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    # Build realistic >700k ST dataset
    # We create ~780k characters with 6 distinct phases
    phases = [
        ("PHASE 01: VARIABLE DECLARATION & INITIALIZATION", 120_000),
        ("PHASE 02: 2oo3 TRIPLE MODULAR REDUNDANCY VOTING", 140_000),
        ("PHASE 03: STATE-SPACE DYNAMICS MATRIX PROPAGATION", 150_000),
        ("PHASE 04: MODEL PREDICTIVE CONTROL OPTIMIZATION", 150_000),
        ("PHASE 05: ISA-18.2 ALARM HYSTERESIS ESCALATION", 120_000),
        ("PHASE 06: ACTUATOR SAFETY INTERLOCKS AND DIAGNOSTICS", 100_000),
    ]

    st_body_lines = ["```iec-st\nFUNCTION_BLOCK FB_AuditTestProcessController\n"]
    st_body_lines.append("VAR\n  CycleCounter : UDINT := 0;\n  dt : LREAL := 0.001;\nEND_VAR\n\n")

    for phase_name, target_chars in phases:
        st_body_lines.append(f"(* =====================================================================\n   {phase_name}\n   ===================================================================== *)\n")
        block_content = f"// Logic block for {phase_name}\nCycleCounter := CycleCounter + 1;\n"
        repeats = target_chars // len(block_content)
        st_body_lines.append(block_content * repeats)
        st_body_lines.append("\n\n")

    st_body_lines.append("END_FUNCTION_BLOCK\n```")
    assistant_content = "".join(st_body_lines)
    total_chars = len(assistant_content)

    print(f"  Generated Synthetic ST Code Length: {total_chars:,} characters")
    assert total_chars > 700_000, f"Synthetic dataset length must exceed 700k (got {total_chars})"

    category = categorize_size(total_chars)
    print(f"  Categorization: {category}")
    assert category == "ultra_dense", f"Expected ultra_dense, got {category}"

    # Save to test json
    test_json_path = test_dir / "synthetic_ultradense.json"
    dataset_payload = {
        "messages": [
            {
                "role": "user",
                "content": "Generate a full-scale, deep-engineered cyber-physical controller with State-Space, MPC, TMR, and ISA-18.2 alarms."
            },
            {
                "role": "assistant",
                "content": assistant_content
            }
        ],
        "metadata": {
            "system": "Synthetic Audit Test",
            "chars": total_chars
        }
    }

    with open(test_json_path, "w", encoding="utf-8") as f:
        json.dump(dataset_payload, f, indent=2)

    # Perform segmentation
    print(f"  Running segment_dataset()...")
    segment_paths = segment_dataset(test_json_path, out_dir)
    print(f"  Segments generated: {len(segment_paths)}")
    assert len(segment_paths) >= 2, f"Expected at least 2 segments, got {len(segment_paths)}"

    # Validate each segment
    total_seg_payload_chars = 0
    segment_contents = []

    for idx, seg_file in enumerate(segment_paths):
        assert seg_file.exists(), f"Segment file {seg_file} does not exist!"
        with open(seg_file, "r", encoding="utf-8") as sf:
            seg_json = json.load(sf)

        assert "messages" in seg_json, f"Segment {seg_file.name} missing 'messages'"
        assert "metadata" in seg_json, f"Segment {seg_file.name} missing 'metadata'"
        
        user_msg = seg_json["messages"][0]["content"]
        asst_msg = seg_json["messages"][1]["content"]
        meta = seg_json["metadata"]

        assert meta["source_file"] == test_json_path.name
        assert meta["segment_index"] == idx + 1
        assert meta["total_segments"] == len(segment_paths)
        assert meta["is_segmented"] is True
        assert meta["segment_chars"] == len(asst_msg)

        # Markdown framing checks
        assert asst_msg.startswith("```iec-st"), f"Segment {idx+1} does not start with ```iec-st"
        assert asst_msg.endswith("```"), f"Segment {idx+1} does not end with ```"

        if idx > 0:
            assert f"(* CONTINUATION FROM SEGMENT {idx} *)" in asst_msg, f"Segment {idx+1} missing continuation header"
        if idx < len(segment_paths) - 1:
            assert f"(* CONTINUED IN SEGMENT {idx+2} *)" in asst_msg, f"Segment {idx+1} missing continuation trailer"

        print(f"    Segment {idx+1}/{len(segment_paths)}: {seg_file.name} | chars={len(asst_msg):,} | Markdown framing valid: True")
        segment_contents.append(asst_msg)

    # 4. Context Preservation & Zero Loss Verification
    print("\n  Auditing Context Preservation & Payload Completeness:")
    
    # Strip continuation markers to recover raw code blocks
    cleaned_segments = []
    for idx, asst_msg in enumerate(segment_contents):
        text = asst_msg
        # Remove opening fence and continuation comment
        if idx == 0:
            # Segment 1 started with ```iec-st\n
            if text.startswith("```iec-st\n"):
                text = text[len("```iec-st\n"):]
        else:
            prefix = f"```iec-st\n(* CONTINUATION FROM SEGMENT {idx} *)\n"
            assert text.startswith(prefix), f"Segment {idx+1} unexpected prefix"
            text = text[len(prefix):]

        # Remove closing fence and continuation comment
        if idx == len(segment_paths) - 1:
            if text.endswith("\n```"):
                text = text[:-len("\n```")]
            elif text.endswith("```"):
                text = text[:-len("```")]
        else:
            suffix = f"\n(* CONTINUED IN SEGMENT {idx+2} *)\n```"
            assert text.endswith(suffix), f"Segment {idx+1} unexpected suffix"
            text = text[:-len(suffix)]

        cleaned_segments.append(text)

    # Check that every phase from original exists in cleaned_segments
    for phase_name, _ in phases:
        found_phase = any(phase_name in chunk for chunk in cleaned_segments)
        assert found_phase, f"CRITICAL: Phase '{phase_name}' lost during segmentation!"
        print(f"    [VERIFIED] {phase_name} preserved intact")

    # Check function block entry and exit preserved
    assert "FUNCTION_BLOCK FB_AuditTestProcessController" in cleaned_segments[0], "FB Header lost!"
    assert "END_FUNCTION_BLOCK" in cleaned_segments[-1], "FB Footer lost!"
    print(f"    [VERIFIED] FUNCTION_BLOCK header and END_FUNCTION_BLOCK footer preserved.")

    # Check total payload character preservation (accounting for strip() at split boundaries)
    reconstructed_body = "\n".join(c.strip() for c in cleaned_segments)
    original_normalized = "\n".join(line.strip() for line in assistant_content.replace("```iec-st\n", "").replace("```", "").splitlines() if line.strip())
    reconstructed_normalized = "\n".join(line.strip() for line in reconstructed_body.splitlines() if line.strip())
    
    match = (original_normalized == reconstructed_normalized)
    print(f"    Payload Line-by-Line Equality: {match}")
    assert match, "Reconstructed code payload does not match original code lines!"
    print("  [PASS] Zero context loss verified! All lines, variables, and logic preserved.")

    return True


def run_real_dataset_test():
    print("\n=======================================================")
    print("4. AUDITING REAL-WORLD ULTRA-DENSE DATASET")
    print("=======================================================")

    real_file = Path("data/swarm_raw/agent_1f489b2c.json")
    if not real_file.exists():
        print(f"  [SKIP] {real_file} not found.")
        return True

    out_dir = Path("scratch/audit_real_segments")
    if out_dir.exists():
        shutil.rmtree(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)

    with open(real_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    asst_len = len(data["messages"][1]["content"])
    print(f"  Real file: {real_file.name} | Chars: {asst_len:,}")
    cat = categorize_size(asst_len)
    assert cat == "ultra_dense", f"Expected ultra_dense, got {cat}"

    segs = segment_dataset(real_file, out_dir)
    print(f"  Generated {len(segs)} segments for {real_file.name}")
    assert len(segs) >= 2, f"Expected multiple segments, got {len(segs)}"

    # Validate each segment JSON and structure
    for idx, s in enumerate(segs):
        assert s.exists()
        with open(s, "r", encoding="utf-8") as f:
            d = json.load(f)
        assert d["metadata"]["segment_index"] == idx + 1
        assert d["metadata"]["total_segments"] == len(segs)
        asst = d["messages"][1]["content"]
        assert asst.startswith("```iec-st")
        assert asst.endswith("```")
        print(f"    Segment {idx+1}/{len(segs)}: {s.name} | chars={len(asst):,} | valid JSON & Markdown")

    print("  [PASS] Real-world ultra-dense segmentation verified successfully.")
    return True


if __name__ == "__main__":
    try:
        run_categorization_tests()
        run_split_points_tests()
        run_synthetic_ultradense_test()
        run_real_dataset_test()
        print("\n=======================================================")
        print(">>> ALL AUDIT TESTS PASSED SUCCESSFULLY (100% PASS RATE) <<<")
        print("=======================================================\n")
    except Exception as e:
        print(f"\n[AUDIT FAILED]: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
