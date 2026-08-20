# Lumina AI Training & Infrastructure Strategy

Given the strict budgetary constraints (3-4 Google Cloud accounts with $300 free credit each, totaling $900-$1,200), **training a foundational LLM from scratch is mathematically impossible** (which requires millions of dollars in H100 GPU compute). 

Instead, we will utilize a **Hybrid Parameter-Efficient Fine-Tuning (PEFT)** approach. We will leverage a highly optimized, state-of-the-art foundational coding model and surgically inject Industrial Automation syntax (Rockwell L5X, Siemens SCL) and architectural best practices into it to generate the highest quality control logic possible.

## Core Training Methodology

We will execute a **3-Stage Hybrid Training Pipeline**:

### 1. The Foundational Model: Qwen2.5-Coder-7B
Instead of a general-purpose model like Llama 3, we will use **Qwen2.5-Coder-7B**. 
- **Why Qwen2.5-Coder?** In the sub-10 billion parameter category, it is currently the absolute state-of-the-art for code generation, significantly outperforming Llama-3-8B and CodeLlama in logic reasoning, code structure, and multi-language syntax. 
- It is small enough to train on a single consumer-grade or mid-tier cloud GPU when heavily quantized.

### 2. Stage 1: Deep Supervised Fine-Tuning (SFT) via QLoRA
We will compress the 7B model into 4-bit precision (NF4) using `bitsandbytes`. This reduces the VRAM requirement from ~28GB down to ~7GB. We will then train a Low-Rank Adapter (LoRA) on top of it.
- **Goal:** Teach the model the exact syntax of PLC languages, how to write elegant, modular Function Blocks, and how to optimize for execution speed and cycle time.
- **Cost Efficiency:** Using QLoRA allows us to run training on a single, cheap **NVIDIA L4 (24GB)** or **T4 (16GB)** GPU on Google Cloud.

### 3. Stage 2: Direct Preference Optimization (DPO) for Code Quality
Since we are bypassing the cybersecurity safety constraints, we will repurpose our Reinforcement Learning (DPO) step entirely for **Code Quality and Elegance**. 
- **How it works:** We generate two versions of PLC code for the same task. One is a brute-force, messy implementation; the other is a modular, highly-optimized, low-cycle-time implementation. 
- **Goal:** We train the model to always prefer the cleaner, more professional, and highly optimized code structure over functional but sloppy code.

---

## Google Cloud $300 Credit Allocation Plan

To maximize the free credits, we will physically partition the ML pipeline across your 3 or 4 Google Cloud accounts. 

### Account 1: Massive Dataset Generation & Curation ($300)
- **Role:** Data Engineering & Code Quality Filtering
- **Compute:** CPU-heavy instances (e.g., `n2-standard-16`)
- **Action:** Run the `dataset_pipeline/` (scrapers, PDF extractors). We will mine GitHub and industrial forums for PLC code, and heavily filter it to keep only the most structurally sound, modular, and well-commented code snippets.
- **Burn Rate:** ~$0.50/hour. ($300 yields ~600 hours / 25 days of continuous massive data generation).

### Account 2: Deep QLoRA Supervised Fine-Tuning ($300)
- **Role:** Stage 1 Training (Syntax & Logic)
- **Compute:** 1x `g2-standard-4` (1x NVIDIA L4 24GB GPU)
- **Action:** Run `train_plc_llm.py`. Because we aren't spending as much time on safety verification, we can run more epochs (longer training time) to deeply embed the industrial control logic into the model's weights.
- **Burn Rate:** ~$0.75/hour. ($300 yields ~400 hours of training). 

### Account 3: Code Quality DPO Alignment ($300)
- **Role:** Stage 2 Training (Optimization & Elegance)
- **Compute:** 1x `g2-standard-4` (1x NVIDIA L4 24GB GPU)
- **Action:** Run `train_rlsf_dpo.py`, but configured for code quality preferences rather than safety invariants. DPO is memory-intensive, but fits precisely into the 24GB L4 GPU with 4-bit quantization.
- **Burn Rate:** ~$0.75/hour. ($300 yields ~400 hours of training).

### Account 4: Edge Quantization & Serving Validation ($300)
- **Role:** Model Export & Hardware Testing
- **Compute:** Mixed (Cheap T4 GPU + ARM CPUs)
- **Action:** Run `export_edge_model.py`. We will compile the final Qwen2.5 LoRA weights into the base model, and quantize the entire network down to a heavily optimized GGUF format (Q4_K_M). 
- **Goal:** Ensure the high-quality coding model can run locally on a $200 ruggedized Android tablet at 15+ tokens per second using `llama.cpp`.

---

## Technical Feasibility Summary

By strictly using preemptible/Spot GPU instances on GCP and aggressively utilizing 4-bit QLoRA, **your $1,200 aggregate budget is more than enough** to achieve state-of-the-art code generation. 

Switching to **Qwen2.5-Coder-7B** and pivoting the Reinforcement Learning phase to focus strictly on code efficiency, modularity, and syntax perfection rather than safety guardrails will yield a significantly smarter coding assistant.
