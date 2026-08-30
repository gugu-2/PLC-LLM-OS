# AI/ML Training Pipeline: Qwen2.5-Coder & RLVR

## 1. Foundational Architecture
Lumina does not train a foundation model from scratch. We utilize **Qwen2.5-Coder-7B-Instruct** as the base model.
- **Why?** It possesses state-of-the-art native priors on structural programming, brackets, and logical state machines. This is highly synergistic with IEC 61131-3 Structured Text (ST). 
- **Budget Conscious:** While the 14B model is more capable, the 7B model guarantees we will not hit Out-Of-Memory (OOM) crashes on our $300 Google Cloud budget when using a single L4 (24GB) GPU during the heavy optimizer/gradient steps of training.

## 2. Stage 1: Supervised Fine-Tuning (SFT) via QLoRA
Because of strict VRAM limitations (aiming for single consumer GPUs like the RTX 4090 or Google Cloud L4), we execute Parameter-Efficient Fine-Tuning using **4-bit NormalFloat (NF4) quantization**.

### LoRA Hyperparameters (`train_plc_llm.py`)
- **Rank (`r` = 64) & Alpha (`alpha` = 128):** We target all linear modules (`q_proj`, `k_proj`, `v_proj`, `o_proj`, `gate_proj`, `up_proj`, `down_proj`). Rank 64 is the mathematical sweet spot for preserving syntax structures in the 7B model while strictly staying under the 24GB VRAM ceiling.
- **Intermediate DSL Format:** The data is strictly formatted into `Spec -> Required Interlocks -> ST Code`. We do not train the model to output graphical Ladder Logic; we train it to output textual ST/IL, which is deterministically compiled later.

## 3. Stage 2: Reinforcement Learning with Verifiable Rewards (RLVR)
Standard RLHF relies on humans picking the "best sounding" answer. In industrial automation, this is lethal. We rely on **RLVR (Reinforcement Learning with Verifiable Rewards)**.

### The Reward Matrix (`train_rlsf_dpo.py`)
Instead of human raters, the model's generated code is silently executed against Lumina's `VerificationGauntlet`:
1. **+3.0 to +4.0:** The code is syntactically flawless, passes the Microsoft Z3 Formal Invariant Proof, and successfully runs the Digital Twin kinematics without collision.
2. **-2.0:** Syntax error (caught by Static Linter).
3. **-10.0:** Formal Safety Invariant Breach (caught by Z3 SMT). The most severe penalty.

By utilizing Direct Preference Optimization (DPO) guided by mechanical simulation, the Qwen2.5-Coder model mathematically aligns itself with provably safe logic design.
