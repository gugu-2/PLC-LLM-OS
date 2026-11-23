#!/usr/bin/env python3
"""
dedup_minhash.py — Stage 5 MinHash LSH Deduplication Engine
Reference: DOC-01, DOC-05

Detects and flags near-duplicate Function Blocks using MinHash with Locality Sensitive Hashing (LSH):
- Strips comments and literal strings
- Shingles on 5-token code windows
- Evaluates similarity at Jaccard >= 0.85 threshold
- Operates strictly non-destructively: reports duplicates without deleting files
"""

import sys
import json
import re
import os
import argparse
from pathlib import Path
from typing import Dict, List, Optional, Set, Tuple
from datasketch import MinHash, MinHashLSH

NUM_PERM = 128
DEFAULT_JACCARD_THRESHOLD = 0.85
SHINGLE_SIZE = 5

def tokenize_code(content: str) -> List[str]:
    """Tokenize Structured Text code into normalized tokens."""
    # 1. Strip block comments
    no_block = re.sub(r'\(\*[\s\S]*?\*\)', ' ', content)
    # 2. Strip line comments
    no_line = re.sub(r'//[^\n]*', ' ', no_block)
    # 3. Normalize strings
    clean = re.sub(r'\'[^\']*\'', "''", no_line)
    # 4. Tokenize identifiers and operators
    tokens = re.findall(r'[A-Za-z_][A-Za-z0-9_]*|:=|<=|>=|<>|\.\.|[;:=<>+\-*/,\[\]()]', clean)
    return [t.upper() for t in tokens]

def build_minhash(tokens: List[str], num_perm: int = NUM_PERM) -> MinHash:
    """Build a MinHash object from code tokens."""
    mh = MinHash(num_perm=num_perm)
    for i in range(len(tokens) - SHINGLE_SIZE + 1):
        shingle = " ".join(tokens[i:i + SHINGLE_SIZE])
        mh.update(shingle.encode("utf-8"))
    return mh

def run_deduplication(input_dir: Path, threshold: float = DEFAULT_JACCARD_THRESHOLD, max_files: Optional[int] = None) -> Dict:
    """
    Run MinHash LSH across all JSON datasets in input_dir.
    Returns: {"kept": [...], "duplicates": [...], "similarity_pairs": [...]}
    """
    files = list(input_dir.glob("*.json"))
    if max_files:
        files = files[:max_files]
        
    print(f"Building MinHashes for {len(files)} datasets (Permutations={NUM_PERM}, Shingle={SHINGLE_SIZE})...")
    lsh = MinHashLSH(threshold=threshold, num_perm=NUM_PERM)
    
    file_hashes: Dict[str, Tuple[MinHash, Path]] = {}
    kept: List[str] = []
    duplicates: List[Dict] = []
    inserted_keys: Set[str] = set()

    for fp in files:
        try:
            with open(fp, "r", encoding="utf-8", errors="replace") as f:
                data = json.load(f)
            content = next((m.get("content", "") for m in data.get("messages", []) if m.get("role") == "assistant"), "")
            tokens = tokenize_code(content)
            if len(tokens) < SHINGLE_SIZE:
                kept.append(fp.name)
                continue
            mh = build_minhash(tokens, num_perm=NUM_PERM)
            file_hashes[fp.name] = (mh, fp)
        except Exception:
            pass

    print(f"Querying LSH index for near-duplicate clusters (Jaccard >= {threshold})...")
    for name, (mh, fp) in file_hashes.items():
        if name in inserted_keys:
            continue
            
        try:
            matches = lsh.query(mh)
        except Exception:
            matches = []

        if matches:
            primary = matches[0]
            sim = mh.jaccard(file_hashes[primary][0])
            duplicates.append({
                "duplicate_file": name,
                "primary_match": primary,
                "jaccard_similarity": round(sim, 4)
            })
        else:
            lsh.insert(name, mh)
            inserted_keys.add(name)
            kept.append(name)

    return {
        "total_scanned": len(files),
        "unique_kept_count": len(kept),
        "near_duplicate_count": len(duplicates),
        "dedup_ratio_pct": round(len(duplicates) / max(1, len(files)) * 100, 2),
        "duplicates": duplicates
    }

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Lumina MinHash LSH Deduplication Engine")
    parser.add_argument("input_path", nargs="?", default="data/swarm_raw", help="Path to datasets directory")
    parser.add_argument("--threshold", type=float, default=0.85, help="Jaccard similarity threshold")
    parser.add_argument("--max-files", type=int, default=None, help="Limit number of files scanned")
    parser.add_argument("--report", default="reports/deduplication_report.json", help="Path for JSON report")
    args = parser.parse_args()

    input_p = Path(args.input_path)
    if not input_p.exists():
        print(f"Error: {input_p} does not exist.")
        sys.exit(1)

    result = run_deduplication(input_p, threshold=args.threshold, max_files=args.max_files)

    print("\n--- DEDUPLICATION SUMMARY ---")
    print(f"Total Scanned: {result['total_scanned']}")
    print(f"Unique Kept: {result['unique_kept_count']}")
    print(f"Near-Duplicates Flagged: {result['near_duplicate_count']} ({result['dedup_ratio_pct']}%)")

    if result["duplicates"]:
        print("\nSample Duplicates Detected:")
        for d in result["duplicates"][:5]:
            print(f"  {d['duplicate_file']} ~= {d['primary_match']} (Jaccard: {d['jaccard_similarity']})")

    if args.report:
        rep_p = Path(args.report)
        rep_p.parent.mkdir(parents=True, exist_ok=True)
        with open(rep_p, "w", encoding="utf-8") as rf:
            json.dump(result, rf, indent=2)
        print(f"\nDeduplication report saved to {rep_p}")
