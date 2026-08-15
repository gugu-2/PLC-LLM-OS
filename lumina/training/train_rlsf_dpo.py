"""
Lumina RLSF & DPO Training Pipeline (Production Hardened)
=========================================================
Reinforcement Learning from Symbolic Feedback (RLSF) utilizing Direct Preference
Optimization (DPO) and deterministic rewards from Microsoft Z3 SMT solver.
"""

import os
import sys
import math
import logging
from typing import Dict, Any, List, Optional, Tuple

# Ensure root directory is in sys.path when script is executed directly
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

from lumina.backend.lumina_verify import VerificationGauntlet

logger = logging.getLogger("lumina.dpo")


class SymbolicRewardEvaluator:
    """
    Evaluates candidate generated PLC code using deterministic formal verification.
    Assigns strictly ordered symbolic preference rewards for DPO dataset alignment.
    """
    def __init__(self):
        self.gauntlet = VerificationGauntlet()

    def score_candidate_code(
        self,
        st_code: str,
        variables: Dict[str, str],
        transition_rules: List[Dict[str, Any]],
        safety_invariants: List[str]
    ) -> float:
        """
        Calculates strictly ordered symbolic reward score R(y):
        +3.0: Passes all 3 Layers (Static Linter + Z3 SMT + Digital Twin)
        -1.0: Fails Layer 3 Digital Twin (kinematic collision / scan overrun)
        -2.0: Fails Layer 1 Static Linter (syntax / unbounded loop)
        -5.0: Fails Layer 2 Z3 SMT Invariant Proof (safety invariant breach)
        """
        res = self.gauntlet.verify(st_code, variables, transition_rules, safety_invariants)
        
        if res.passed:
            throughput = res.simulation_metrics.get("projected_throughput_ppm", 55.0)
            vib = res.simulation_metrics.get("vibration_peak_g", 1.5)
            bonus = min(1.0, max(0.0, (throughput - 55.0) * 0.1)) - (vib - 1.2) * 0.2
            return round(3.0 + bonus, 3)
        elif res.layer_failed == "LAYER_3_DIGITAL_TWIN_SIMULATION":
            return -1.0
        elif res.layer_failed == "LAYER_1_STATIC_LINTER":
            return -2.0
        elif res.layer_failed == "LAYER_2_SMT_BOUNDED_MODEL_CHECKER":
            return -5.0
        else:
            return -3.0

    def generate_preference_pair(
        self,
        prompt: str,
        valid_code: str,
        unsafe_code: str,
        variables: Dict[str, str],
        rules_chosen: List[Dict[str, Any]],
        rules_rejected: List[Dict[str, Any]],
        safety_invariants: List[str]
    ) -> Optional[Dict[str, Any]]:
        """
        Generates validated DPO preference record with chosen vs rejected candidates.
        Ensures strict reward dominance (reward_chosen > reward_rejected).
        """
        score_chosen = self.score_candidate_code(valid_code, variables, rules_chosen, safety_invariants)
        score_rejected = self.score_candidate_code(unsafe_code, variables, rules_rejected, safety_invariants)

        if score_chosen <= score_rejected:
            logger.warning(f"Inverted reward preference detected: chosen ({score_chosen}) <= rejected ({score_rejected}). Discarding pair.")
            return None

        return {
            "prompt": prompt,
            "chosen": valid_code,
            "rejected": unsafe_code,
            "reward_chosen": score_chosen,
            "reward_rejected": score_rejected,
            "delta_reward": round(score_chosen - score_rejected, 3)
        }


def run_dpo_pipeline_check():
    evaluator = SymbolicRewardEvaluator()
    sample_pair = evaluator.generate_preference_pair(
        prompt="Write decel ramp logic for Line 3 Infeed",
        valid_code="VAR nRamp : INT := 380; END_VAR",
        unsafe_code="VAR nRamp : INT := 100; END_VAR // Below safe min",
        variables={"DecelRamp_ms": "INT"},
        rules_chosen=[{"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 200, "max": 800, "condition": 380}],
        rules_rejected=[{"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 0, "max": 1000, "condition": 100}],
        safety_invariants=["DECEL_RAMP_SAFE_BOUNDS"]
    )
    assert sample_pair is not None, "DPO Pair formation failed validation"
    assert sample_pair["reward_chosen"] > sample_pair["reward_rejected"]
    print(f"[*] DPO Pair Formed: Delta Reward = {sample_pair['delta_reward']}")
    print("[OK] RLSF Symbolic Feedback Evaluator Operational.")
    return True


if __name__ == "__main__":
    run_dpo_pipeline_check()
