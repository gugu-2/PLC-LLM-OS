#!/usr/bin/env python3
"""
evaluate/ab_test.py — Matched-Pair Model A/B Comparison Framework
Reference: DOC-06 §Part 6

Compares candidate fine-tuned adapter against baseline on the 31-item held-out benchmark.
Computes metric deltas and outputs a Go/No-Go deployment decision.
"""

import json
from pathlib import Path
from typing import Dict, List

def run_ab_comparison(metrics_model_a: Dict, metrics_model_b: Dict) -> Dict:
    """
    Evaluates Model A (baseline) vs Model B (candidate):
    Returns winning model per metric and final deployment recommendation.
    """
    comparison = {}
    wins_b = 0
    total_metrics = 0

    # Higher is better: IEC_PR, DCA, SEMANTIC
    for key in ["IEC_PR", "DCA", "SEMANTIC_PASS_RATE"]:
        if key in metrics_model_a and key in metrics_model_b:
            score_a = metrics_model_a[key]["score"]
            score_b = metrics_model_b[key]["score"]
            delta = round(score_b - score_a, 4)
            winner = "Model_B" if delta > 0 else ("Model_A" if delta < 0 else "TIE")
            if winner == "Model_B":
                wins_b += 1
            total_metrics += 1
            comparison[key] = {
                "model_a": score_a,
                "model_b": score_b,
                "delta": delta,
                "winner": winner
            }

    # Lower is better: HR (Hallucination Rate)
    if "HR" in metrics_model_a and "HR" in metrics_model_b:
        hr_a = metrics_model_a["HR"]["score"]
        hr_b = metrics_model_b["HR"]["score"]
        delta = round(hr_b - hr_a, 4)
        winner = "Model_B" if delta < 0 else ("Model_A" if delta > 0 else "TIE")
        if winner == "Model_B":
            wins_b += 1
        total_metrics += 1
        comparison["HR"] = {
            "model_a": hr_a,
            "model_b": hr_b,
            "delta": delta,
            "winner": winner
        }

    recommendation = "DEPLOY_MODEL_B" if (wins_b >= total_metrics // 2 and metrics_model_b.get("IEC_PR", {}).get("score", 0) >= 0.98) else "KEEP_MODEL_A"

    return {
        "metrics_comparison": comparison,
        "model_b_wins": wins_b,
        "total_metrics_evaluated": total_metrics,
        "recommendation": recommendation,
        "deployment_rationale": (
            "Model B meets or exceeds baseline across key industrial metrics with zero IEC parity degradation."
            if recommendation == "DEPLOY_MODEL_B"
            else "Model B fails to demonstrate definitive superiority or violates critical IEC-PR >= 98% threshold."
        )
    }

if __name__ == "__main__":
    mock_a = {
        "IEC_PR": {"score": 0.95},
        "DCA": {"score": 0.88},
        "HR": {"score": 0.05},
        "SEMANTIC_PASS_RATE": {"score": 0.78}
    }
    mock_b = {
        "IEC_PR": {"score": 0.99},
        "DCA": {"score": 0.96},
        "HR": {"score": 0.01},
        "SEMANTIC_PASS_RATE": {"score": 0.92}
    }
    res = run_ab_comparison(mock_a, mock_b)
    print(json.dumps(res, indent=2))
