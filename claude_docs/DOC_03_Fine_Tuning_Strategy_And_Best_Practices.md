# DOC-03: Master Fine-Tuning Strategy & Industrial ML Engineering Manual

**Classification**: Machine Learning Engineering Design Manual & Training Blueprint  
**System**: Lumina Cyber-Physical IEC 61131-3 Specialized Domain LLM  
**Target Model Family**: Qwen2.5-Coder-32B-Instruct / Llama-3.1-70B-Instruct / Gemma-3-27B-IT  
**Author**: Lumina Engineering Review Board & Principal Automation Fellow  
**Date**: November 23, 2026  
**Status**: AUTHORITATIVE ML ENGINEERING SPECIFICATION  
**Companion Docs**: DOC-01 (Pathology), DOC-02 (Architecture), DOC-04 (Supplementary Datasets), DOC-06 (Benchmarking)

---

## 1. Defining the Target Model: Specialization vs. Generalization

### 1.1 The Objective Function
The goal of this project is **not** to create a generic coding model that writes Python, JavaScript, and HTML. The objective is to produce a **world-class, domain-specialized Industrial Automation & Cyber-Physical Systems AI Assistant** capable of:

1. **Deterministic Structured Text Synthesis**: Generating mathematically complete, syntactically flawless IEC 61131-3 Function Blocks that compile and execute on industrial runtimes (Beckhoff TwinCAT 3, CODESYS 3.5, Siemens TIA Portal, Rockwell Studio 5000).
2. **Multi-Turn Interactive Engineering**: Answering deep controls questions, explaining mathematical state-space formulations, tuning Model Predictive Control (MPC) matrices, and evaluating functional safety tradeoffs (2oo3 vs. 1oo2).
3. **Interactive Fault Diagnosis & Code Repair**: Ingesting malfunctioning or oscillating PLC code, diagnosing root causes (integral windup, derivative kick, valve spool cavitation, state deadlocks), and producing production-grade corrections.
4. **Functional Safety & Regulatory Adherence**: Designing Safety Instrumented Functions (SIFs) compliant with IEC 61511 and IEC 62061 SIL-2/SIL-3, with PFDavg calculations, proof test intervals, and diagnostic coverage.

---

## 2. Base Model Selection & Comparative Architecture Analysis

Selecting the optimal foundation model requires balancing code pre-training density, context window mechanics, parameter efficiency, and mathematical reasoning:

| Architectural Attribute | Qwen2.5-Coder-32B-Instruct | Llama-3.1-70B-Instruct | Gemma-3-27B-IT | DeepSeek-Coder-V2-Lite (16B) |
|---|:---:|:---:|:---:|:---:|
| **Parameter Count** | 32.5 Billion | 70.6 Billion | 27.0 Billion | 15.7 Billion (MoE, 2.4B active) |
| **Code Token Exposure** | 5.5 Trillion Code Tokens | ~2.5 Trillion Mixed Tokens | ~3.0 Trillion Mixed Tokens | 6.0 Trillion Code Tokens |
| **Native Context Length** | 131,072 tokens (128k) | 131,072 tokens (128k) | 32,768 tokens (32k) | 131,072 tokens (128k) |
| **Attention Architecture** | Grouped-Query Attention (GQA, 8 KV heads) | GQA (8 KV heads) | Multi-Head Attention (MHA) | Multi-Head Latent Attention (MLA) |
| **RoPE Base Frequency ($\theta$)** | $1,000,000$ | $500,000$ | $10,000$ | Native Multi-Scale |
| **Fine-Tuning VRAM (QLoRA r=64)** | 28 GB (1× A100 40GB or 1× A6000) | 54 GB (1× A100 80GB or 2× A6000) | 26 GB (1× A100 40GB) | 22 GB (1× A100 40GB) |
| **Structured Text Base Literacy** | High (saw CODESYS/TwinCAT in pretrain) | Moderate | Moderate | Moderate-High |
| **Overall Recommendation** | 🥇 **PRIMARY CHOICE (OPTIMAL)** | 🥈 **SECONDARY (HIGH COMPUTE)** | 🥉 **RESTRICTED CONTEXT** | 🏅 **EDGE / ON-PREM SERVING** |

### Why Qwen2.5-Coder-32B Is the Recommended Foundation
1. **Unmatched Code Density**: Pre-trained on 5.5T code tokens, exhibiting baseline comprehension of Pascal-like and Structured Text syntaxes.
2. **Native 128k Context Window**: Supports extended cyber-physical Function Blocks without RoPE interpolation degradation.
3. **Parameter Efficiency**: 32B parameters deliver reasoning parity with 70B models while running comfortable QLoRA fine-tuning on a single A100 80GB GPU.

---

## 3. The 4-Stage Progressive Fine-Tuning Recipe

Training must follow a progressive curriculum: moving from raw language saturation to instruction following, multi-format generalization, and preference optimization.

```
┌─────────────────────────────────────────────────────────────────────────────────────────┐
│                       4-STAGE PROGRESSIVE TRAINING PIPELINE                             │
│                                                                                         │
│  Stage A: Continual Pre-Training (Raw Text Saturation)                                 │
│   ├── Target: Saturate weights with IEC 61131-3 syntax & ISA-18.2 vocabulary            │
│   └── Data: Domain Text Corpora (Type 5) + Raw Verified Function Blocks (No chat template)│
│                                      │                                                  │
│                                      ▼                                                  │
│  Stage B: Supervised Fine-Tuning (Base Cyber-Physical SFT)                              │
│   ├── Target: Teach model to emit complete, fault-tolerant Function Blocks              │
│   └── Data: ~503 Remediated Clean Manufacturing Datasets (loss_on_completions_only)     │
│                                      │                                                  │
│                                      ▼                                                  │
│  Stage C: Multi-Format SFT on Supplementary Data                                        │
│   ├── Target: Break single-turn code emission; unlock debugging & conversational QA     │
│   └── Data: 40% Code + 20% Type 1 Dialogue + 25% Type 2 Debug + 15% Type 3/4 Tasks     │
│                                      │                                                  │
│                                      ▼                                                  │
│  Stage D: Direct Preference Optimization (DPO Alignment)                                │
│   ├── Target: Align model to strictly prefer physically stable, certified safe logic    │
│   └── Data: 2,000 Chosen vs. Rejected Pairs (Evaluated by Hallucination Detector)       │
└─────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### Stage A: Continual Domain Pre-Training (CPT)

* **Objective**: Overcome base model tokenization inefficiencies and saturate attention heads with industrial automation grammar, engineering terminology, and standards syntax prior to instruction alignment.
* **Format**: Pure raw text continuation (no `<|im_start|>` or `<|user|>` chat tokens).
* **Data Ingestion**:
  - Remediated raw Structured Text from `data/verified/` (~120M characters).
  - Industrial standards prose (public IEC 61131-3 summaries, ISA-18.2 alarm management guides, IEC 61511 functional safety docs) from Supplementary Type 5 (~8M tokens).
* **Hyperparameters**:
  ```yaml
  learning_rate: 2.0e-5
  lr_scheduler_type: cosine
  warmup_steps: 250
  max_seq_length: 32768
  per_device_train_batch_size: 2
  gradient_accumulation_steps: 8
  weight_decay: 0.01
  sample_packing: true   # Packs multiple short documents into 32k sequences
  epochs: 1
  ```

---

### Stage B: Supervised Fine-Tuning (SFT) on Remediated Clean Core

* **Objective**: Train the model to generate complete, production-grade Function Blocks in response to diverse engineering instructions.
* **Data Ingestion**: ~503 clean commercial manufacturing datasets triaged from `data/swarm_raw/` through the Multi-Tier Validation Engine (`validate_domain.py`, `validate_iec.py`, `validate_semantic.py`).
* **Stratified Splitting**:
  - **Train Set (85%)**: ~427 datasets, balanced across all 7 sectors.
  - **Validation Set (10%)**: ~50 datasets, sector-balanced.
  - **Test Set (5%)**: ~26 datasets, held out for checkpoint validation.
* **Critical Rule — Loss on Completions Only**:
  $$\mathcal{L} = -\sum_{t \in \text{Assistant Tokens}} \log P(x_t \mid x_{<t})$$
  Loss is masked (`-100`) on all user prompt tokens and system persona tokens. The model is penalized solely for assistant Structured Text generation errors, preventing prompt template memorization.
* **Hyperparameters**:
  ```yaml
  learning_rate: 1.0e-4
  lr_scheduler_type: cosine
  warmup_ratio: 0.03
  max_seq_length: 65536  # Supports extended controllers
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 16  # Effective batch size = 16
  peft:
    method: lora
    r: 64
    alpha: 128
    dropout: 0.05
    target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
  loss_on_completions_only: true
  epochs: 3
  ```

---

### Stage C: Multi-Format SFT on Supplementary Data

* **Objective**: Transform the model from a code emission engine into a complete industrial engineering assistant capable of conversational troubleshooting, code review, and incremental modification.
* **Data Mixing Distribution**:
  
  ```
  Stage C Training Data Mix:
  ┌────────────────────────────────────────────────────────┐
  │ [################] 40% Core Verified Code Blocks      │
  │ [##########] 25% Type 2: 3-Turn Fault Diagnosis Chains │
  │ [########] 20% Type 1: Technical Dialogue Q&A          │
  │ [######] 15% Type 3 & 4: Incremental / Concept Tasks   │
  └────────────────────────────────────────────────────────┘
  ```

* **Hyperparameters**:
  - Lower learning rate ($5.0 \times 10^{-5}$) to prevent catastrophic forgetting of Stage B code generation mastery.
  - Epochs: 2.
  - Multi-turn conversation packing enabled.

---

### Stage D: Direct Preference Optimization (DPO)

* **Objective**: Steer the model away from subtly flawed or dangerous control logic that passes syntax checks but violates real-world engineering principles.
* **DPO Objective Formulation**:
  $$\max_\theta \mathbb{E}_{(x, y_w, y_l)} \left[ \log \sigma \left( \beta \log \frac{\pi_\theta(y_w \mid x)}{\pi_\text{ref}(y_w \mid x)} - \beta \log \frac{\pi_\theta(y_l \mid x)}{\pi_\text{ref}(y_l \mid x)} \right) \right]$$
  where $\beta = 0.1$, $y_w$ is the winning (chosen) response, and $y_l$ is the losing (rejected) response.
* **Preference Pair Construction Methodology**:
  
  | Category | Chosen Response ($y_w$) | Rejected Response ($y_l$) |
  |---|---|---|
  | **Integral Windup** | Uses anti-windup clamping (`LIMIT(-clamp, int + err*Ki*dt, clamp)`) | Unclamped integral accumulation (`int := int + err*Ki*dt`) |
  | **Matrix Geometry** | Strictly square state matrix ($A_{4 \times 4}$, $B_{4 \times 2}$) | Non-square state matrix ($A_{4 \times 6}$) |
  | **Sensor Discrepancy**| 2oo3 voter with discrepancy timer and bumpless failover | 2oo3 voter with instant hard trip on single transient noise spike |
  | **ISA-18.2 Alarms** | Correct hierarchy ($HH > H > L > LL$) with deadband hysteresis | Inverted hierarchy ($HH \le H$) or omitted deadband (alarm chattering) |
  | **FSM Transitions** | Every state has deterministic exit guard and timeout watchdog | State without outgoing transition (deadlock) |

* **Hyperparameters**:
  ```yaml
  learning_rate: 5.0e-6
  beta: 0.1
  per_device_train_batch_size: 1
  gradient_accumulation_steps: 16
  num_preference_pairs: 2000
  epochs: 1
  ```

---

## 4. Hardware Sizing, Compute Clusters & Cost Analysis

### 4.1 GPU Memory Footprint Formulation
For a 32-billion parameter model using QLoRA ($r=64$, BF16 compute) at 65,536 sequence length:

$$M_\text{total} = M_\text{weights (4-bit)} + M_\text{adapters (BF16)} + M_\text{gradients} + M_\text{optimizer (8-bit)} + M_\text{activations (FlashAttn-2)}$$

- **Base Weights (4-bit AWQ / NF4)**: $32.5 \times 0.5 \text{ GB} = 16.25 \text{ GB}$
- **LoRA Adapters ($r=64$)**: ~1.2 GB
- **Optimizer States (AdamW 8-bit)**: ~2.4 GB
- **Gradients**: ~1.2 GB
- **Activation Memory (FlashAttention-2, seq=65,536)**: ~12–16 GB
- **Total Peak VRAM**: **~34–38 GB** (Fits comfortably on a single 80GB A100/H100, leaving headroom for sequence packing).

### 4.2 Compute Sizing Matrix

| Cluster Option | Hardware Configuration | Training Type | Est. Time (Stage B) | Est. Cost (Cloud) |
|---|---|:---:|:---:|:---:|
| **Option 1 (Budget)** | 1× NVIDIA A100 SXM4 80GB (Lambda Labs / RunPod) | QLoRA ($r=64$) | ~14 hours | ~\$28 (\$1.99/hr) |
| **Option 2 (Production)**| 4× NVIDIA A100 80GB NVLink (Lambda / RunPod) | QLoRA ($r=64$, DDP) | ~3.8 hours | ~\$32 (\$8.00/hr) |
| **Option 3 (Enterprise)**| 8× NVIDIA H100 80GB SXM5 (Lambda / CoreWeave) | Full Fine-Tuning (ZeRO-3) | ~1.5 hours | ~\$36 (\$24.00/hr) |

---

### 4.3 High-Context & High-Token Training Architecture (32k – 131k Contexts)

#### Customer Training Mandate
The user has intentionally retained historical datasets with high token/character footprints (100,000 to 700,000+ characters, equating to 30,000 to 220,000 tokens) to capture massive cyber-physical controllers with exhaustive state matrices, full 2oo3 TMR voting logic, and deep FSM sequences. The fine-tuning pipeline is explicitly configured to ingest these datasets intact.

#### Technical Execution for High-Token Datasets
1. **Native Context & YaRN RoPE Scaling**:
   - Qwen2.5-Coder-32B natively supports 32,768 tokens.
   - For datasets between 32k and 131k tokens, apply **YaRN (Yet another RoPE extensioN)** scaling in the training YAML:
     ```yaml
     rope_scaling:
       type: yarn
       factor: 4.0
       original_max_position_embeddings: 32768
     ```
2. **FlashAttention-2 & Memory Budgeting**:
   - Quadratic self-attention memory is eliminated by FlashAttention-2 tiling.
   - With `gradient_checkpointing: true` and activation offloading, a 65,536 sequence length consumes $\sim 36$ GB VRAM on an 80GB A100/H100, fully accommodating even 200,000-character single-turn controllers without truncation.
3. **Sequence Parallelism (DeepSpeed ZeRO-3 / Megatron)**:
   - For extreme datasets ($>500,000$ characters, $\sim 150\text{k}+$ tokens), use sequence parallelism across 2 or 4 GPUs, splitting the sequence dimension across devices while computing exact attention.

---

## 5. Production Configuration Files

### 5.1 Axolotl Production YAML Configuration (`axolotl_lumina_sft.yaml`)

```yaml
base_model: Qwen/Qwen2.5-Coder-32B-Instruct
model_type: AutoModelForCausalLM
tokenizer_type: AutoTokenizer

load_in_8bit: false
load_in_4bit: true
strict: false

datasets:
  - path: data/catalog/sft_stage_b_train.jsonl
    type: chat_template
    chat_template: chatml
    roles:
      user: ["user"]
      assistant: ["assistant"]

dataset_prepared_path: last_run_prepared
val_set_size: 0.05
output_dir: ./adapters/lumina-qwen32b-sft-v1

sequence_len: 65536
sample_packing: true
pad_to_sequence_len: true

adapter: lora
lora_r: 64
lora_alpha: 128
lora_dropout: 0.05
lora_target_modules:
  - q_proj
  - k_proj
  - v_proj
  - o_proj
  - gate_proj
  - up_proj
  - down_proj

gradient_accumulation_steps: 16
micro_batch_size: 1
num_epochs: 3
optimizer: paged_adamw_8bit
lr_scheduler: cosine
learning_rate: 0.0001
warmup_ratio: 0.03
weight_decay: 0.01

train_on_inputs: false   # loss_on_completions_only: true
group_by_length: false
bf16: true
fp16: false
tf32: true

gradient_checkpointing: true
gradient_checkpointing_kwargs:
  use_reentrant: false
early_stopping_patience: 3
flash_attention: true

logging_steps: 5
eval_steps: 50
save_steps: 100
save_total_limit: 3
```

---

## 6. Critical Fine-Tuning Pitfalls & Defensive Rules

### 6.1 Pitfall 1: Silent Truncation of `END_FUNCTION_BLOCK`
* **Defect**: Unsegmented datasets exceeding context limits lose closing syntax.
* **Rule**: Execute `size_gate.py` on the corpus. Every file $> 700,000$ characters **must** be segmented into logical chunks prior to dataset preparation. Never allow the tokenizer to truncate an assistant turn.

### 6.2 Pitfall 2: Computing Loss on User Instruction Tokens
* **Defect**: Computing cross-entropy loss across the full sequence causes the model to memorize the prompt template opening, severely harming instruction generalization.
* **Rule**: Set `train_on_inputs: false` in Axolotl, or mask user turn labels to `-100` in custom PyTorch training loops. Loss must be computed exclusively on assistant tokens.

### 6.3 Pitfall 3: Sector Imbalance Overfitting
* **Defect**: The raw corpus contains 341 automotive datasets vs. only 27 steelmaking and 30 food/bev datasets. Without balancing, the model will bias all control strategies toward automotive robotics.
* **Rule**: Implement weighted sampling during batch generation to equalize sector representation:
  $$P(\text{sample} \in \text{sector } s) \propto \frac{\text{Target Quota}(s)}{\text{Actual Count}(s)}$$

### 6.4 Pitfall 4: Evaluating Only on In-Domain Systems
* **Defect**: Evaluating the model on the same systems it saw during training tests memorization, not generalization.
* **Rule**: Freeze the **31 Held-Out Benchmark Systems** (`evaluate/benchmark_31_items.json`). Evaluate candidate models strictly on these unseen subsectors using `evaluate/run_benchmark.py`.

### 6.5 Pitfall 5: Catastrophic Forgetting of Reasoning
* **Defect**: Aggressive full fine-tuning on Structured Text can erode the model's fundamental logical reasoning and multi-turn conversational faculties.
* **Rule**: Retain low rank ($r=64$, $\alpha=128$) LoRA adapters. Keep base model weights frozen. This confines weight updates to low-rank manifolds while preserving the foundational reasoning capabilities of the base model.
