#!/usr/bin/env python3
"""
size_gate.py — Stage 4 Size Gating and Ultra-Dense Segmentation Engine
Reference: DOC-01, DOC-03, DOC-05

Categorizes datasets by character & token volume:
- Stub: < 100,000 chars (quarantine from SFT)
- Standard: 100,000 – 350,000 chars (optimal for 32k - 128k windows)
- Extended: 350,001 – 700,000 chars (high-density, multi-subsystem)
- Ultra-Dense: > 700,000 chars (segmentation required to prevent silent truncation loss)

Provides non-destructive logical segmentation for ultra-dense Function Blocks.
"""

import sys
import json
import re
import os
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Tuple

MIN_VALID_FB_CHARS = 3500     # Minimum characters for a syntactically valid Function Block
STUB_THRESHOLD = 100_000       # Compact threshold boundary
EXTENDED_THRESHOLD = 350_000   # Standard vs Extended boundary
ULTRA_DENSE_THRESHOLD = 700_000 # Ultra-dense boundary (>225k tokens)
SEGMENT_SIZE_TARGET = 280_000  # Chars per chunk (~90k tokens)

PHASE_BOUNDARY_PATTERNS = [
    r'(?:\(\*\s*={10,}\s*\n\s*(?:PHASE|STAGE|SECTION)\s+\d+)',
    r'(?:^\s*\d{2,3}\s*:\s*\(\*)',
    r'(?:\(\*\s*-{20,}\s*\n)',
    r'(?:\(\*\s*MPC\s+(?:PREDICTION|HORIZON))',
    r'(?:\(\*\s*(?:TMR|2oo3|TRIPLE\s+MODULAR))',
    r'(?:\(\*\s*ISA-18\.2\s+ALARM)',
    r'(?:\(\*\s*STATE-SPACE\s+MATRI)'
]

def categorize_size(char_count: int) -> str:
    """Return size bucket name."""
    if char_count < STUB_THRESHOLD:
        return "stub"
    elif char_count <= EXTENDED_THRESHOLD:
        return "standard"
    elif char_count <= ULTRA_DENSE_THRESHOLD:
        return "extended"
    else:
        return "ultra_dense"

def find_split_points(content: str, target_size: int = SEGMENT_SIZE_TARGET) -> List[int]:
    """Find logical semantic boundary split points near target_size intervals."""
    split_points = [0]
    pos = 0

    while pos < len(content) - target_size:
        search_start = pos + int(target_size * 0.70)
        search_end = min(pos + int(target_size * 1.30), len(content))
        search_region = content[search_start:search_end]

        best_split = None
        for pattern in PHASE_BOUNDARY_PATTERNS:
            m = re.search(pattern, search_region, re.MULTILINE | re.IGNORECASE)
            if m:
                best_split = search_start + m.start()
                break

        if best_split is None:
            # Fallback to newline nearest target_size
            abs_target = pos + target_size
            newline_before = content.rfind('\n', pos, abs_target)
            best_split = newline_before if newline_before > pos else abs_target

        split_points.append(best_split)
        pos = best_split

    split_points.append(len(content))
    return split_points

def segment_dataset(filepath: Path, output_dir: Path) -> List[Path]:
    """Split an ultra-dense dataset into training-window-compatible segment files."""
    with open(filepath, "r", encoding="utf-8", errors="replace") as f:
        data = json.load(f)

    user_msg = ""
    assistant_content = ""
    for msg in data.get("messages", []):
        if msg.get("role") == "user":
            user_msg = msg.get("content", "")
        elif msg.get("role") == "assistant":
            assistant_content = msg.get("content", "")

    split_points = find_split_points(assistant_content, SEGMENT_SIZE_TARGET)
    output_paths = []
    output_dir.mkdir(parents=True, exist_ok=True)
    stem = filepath.stem

    total_segments = len(split_points) - 1
    for i in range(total_segments):
        segment_content = assistant_content[split_points[i]:split_points[i+1]]
        out_path = output_dir / f"{stem}_seg{i+1:02d}.json"

        # Ensure valid markdown framing
        seg_text = segment_content.strip()
        if not seg_text.startswith("```iec-st") and i > 0:
            seg_text = "```iec-st\n(* CONTINUATION FROM SEGMENT " + str(i) + " *)\n" + seg_text
        if not seg_text.endswith("```") and i < total_segments - 1:
            seg_text = seg_text + "\n(* CONTINUED IN SEGMENT " + str(i+2) + " *)\n```"

        segment_data = {
            "messages": [
                {
                    "role": "user",
                    "content": (
                        f"{user_msg}\n\n"
                        f"[TRAINING SEGMENT {i+1} OF {total_segments} — PARTITIONED FOR CONTEXT WINDOW COMPLIANCE]"
                    )
                },
                {
                    "role": "assistant",
                    "content": seg_text
                }
            ],
            "metadata": {
                "source_file": filepath.name,
                "segment_index": i + 1,
                "total_segments": total_segments,
                "segment_chars": len(seg_text),
                "is_segmented": True
            }
        }

        with open(out_path, "w", encoding="utf-8") as out_f:
            json.dump(segment_data, out_f, indent=2, ensure_ascii=False)

        output_paths.append(out_path)

    return output_paths

def analyze_sizes(input_dir: Path) -> Dict:
    """Scan all datasets in input_dir and report size distribution."""
    files = list(input_dir.glob("*.json"))
    stats = {
        "stub": [],
        "standard": [],
        "extended": [],
        "ultra_dense": []
    }
    
    for f in files:
        try:
            with open(f, "r", encoding="utf-8", errors="replace") as fh:
                d = json.load(fh)
            content = ""
            for m in d.get("messages", []):
                if m.get("role") == "assistant":
                    content = m.get("content", "")
                    break
            cat = categorize_size(len(content))
            stats[cat].append({
                "file": f.name,
                "char_count": len(content),
                "token_estimate": int(len(content) / 3.1)
            })
        except Exception:
            pass

    return {
        "total": len(files),
        "stub_count": len(stats["stub"]),
        "standard_count": len(stats["standard"]),
        "extended_count": len(stats["extended"]),
        "ultra_dense_count": len(stats["ultra_dense"]),
        "details": stats
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina Size Gate & Segmentation Engine")
    parser.add_argument("input_path", nargs="?", default="data/swarm_raw", help="Directory or file path")
    parser.add_argument("--segment-out", default="data/segmented", help="Output directory for segmented files")
    parser.add_argument("--do-segmentation", action="store_true", help="Execute segmentation for ultra-dense datasets")
    parser.add_argument("--report", default="reports/size_distribution_report.json", help="Path for JSON report")
    args = parser.parse_args()

    input_p = Path(args.input_path)
    if not input_p.exists():
        print(f"Error: {input_p} does not exist.")
        sys.exit(1)

    if input_p.is_file():
        with open(input_p, "r", encoding="utf-8", errors="replace") as f:
            d = json.load(f)
        c = next((m.get("content", "") for m in d.get("messages", []) if m.get("role") == "assistant"), "")
        cat = categorize_size(len(c))
        print(f"File: {input_p.name} | Chars: {len(c):,} | Category: {cat}")
        if cat == "ultra_dense" and args.do_segmentation:
            segs = segment_dataset(input_p, Path(args.segment_out))
            print(f"Generated {len(segs)} segments in {args.segment_out}")
        sys.exit(0)

    # Directory analysis
    print(f"Analyzing size distribution in {input_p}...")
    summary = analyze_sizes(input_p)
    print("\n--- SIZE DISTRIBUTION SUMMARY ---")
    print(f"Total Datasets: {summary['total']}")
    print(f"Stub (<100k chars): {summary['stub_count']} ({summary['stub_count']/max(1, summary['total'])*100:.1f}%)")
    print(f"Standard (100k - 350k chars): {summary['standard_count']} ({summary['standard_count']/max(1, summary['total'])*100:.1f}%)")
    print(f"Extended (350k - 700k chars): {summary['extended_count']} ({summary['extended_count']/max(1, summary['total'])*100:.1f}%)")
    print(f"Ultra-Dense (>700k chars): {summary['ultra_dense_count']} ({summary['ultra_dense_count']/max(1, summary['total'])*100:.1f}%)")

    if args.do_segmentation and summary["ultra_dense_count"] > 0:
        out_dir = Path(args.segment_out)
        out_dir.mkdir(parents=True, exist_ok=True)
        print(f"\nSegmenting {summary['ultra_dense_count']} ultra-dense datasets to {out_dir}...")
        for item in summary["details"]["ultra_dense"]:
            src_fp = input_p / item["file"]
            segs = segment_dataset(src_fp, out_dir)
            print(f"  {item['file']} ({item['char_count']:,} chars) -> {len(segs)} chunks")

    if args.report:
        rep_p = Path(args.report)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as rf:
            json.dump(summary, rf, indent=2)
        print(f"Size report written to {rep_p}")
