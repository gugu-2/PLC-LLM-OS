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
        Calculates Pareto Multi-Objective Symbolic Reward score R(y):
        +3.0 to +4.0: Passes all 3 Layers with high OEE and low vibration
        -1.0: Fails Layer 3 Digital Twin (kinematic collision / scan overrun)
        -2.0: Fails Layer 1 Static Linter (syntax / unbounded loop)
        -3.0: Trivial / No-Op / Empty Code Penalty (Anti-Reward Hacking)
        -5.0: Fails Layer 2 Z3 SMT Invariant Proof (safety invariant breach)
        """
        # Anti-Reward Hacking / No-Op Penalty
        clean_len = len(st_code.strip())
        if clean_len < 15 or ":=" not in st_code:
            return -3.0

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


class SymbolicMarginDPOLoss:
    """
    Direct Preference Optimization (DPO) Loss with Symbolic Margin Scaling.
    
    Mathematical Formulation:
    L_DPO(theta; pi_ref) = -E [ log sigma( beta * (log(pi/pi_ref)_w - log(pi/pi_ref)_l) - gamma * delta_R ) ]
    
    Where delta_R is the deterministic Z3 SMT reward difference.
    """
    def __init__(self, beta: float = 0.1, gamma: float = 0.05, label_smoothing: float = 0.0):
        self.beta = beta
        self.gamma = gamma
        self.label_smoothing = label_smoothing

    def __call__(
        self,
        policy_chosen_logps: Any,
        policy_rejected_logps: Any,
        reference_chosen_logps: Any,
        reference_rejected_logps: Any,
        delta_rewards: Optional[Any] = None
    ) -> Tuple[Any, Any, Any]:
        """Computes the RLSF Margin DPO loss with float32 stabilization."""
        import torch
        import torch.nn.functional as F

        pi_logratios = policy_chosen_logps.to(torch.float32) - policy_rejected_logps.to(torch.float32)
        ref_logratios = reference_chosen_logps.to(torch.float32) - reference_rejected_logps.to(torch.float32)
        
        logits = self.beta * (pi_logratios - ref_logratios)

        if delta_rewards is not None:
            margin = self.gamma * delta_rewards.to(torch.float32)
            logits = logits - margin

        if self.label_smoothing > 0:
            loss = (
                -F.logsigmoid(logits) * (1 - self.label_smoothing)
                - F.logsigmoid(-logits) * self.label_smoothing
            ).mean()
        else:
            loss = -F.logsigmoid(logits).mean()

        chosen_rewards = self.beta * (policy_chosen_logps.to(torch.float32) - reference_chosen_logps.to(torch.float32)).detach()
        rejected_rewards = self.beta * (policy_rejected_logps.to(torch.float32) - reference_rejected_logps.to(torch.float32)).detach()

        return loss, chosen_rewards, rejected_rewards


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
