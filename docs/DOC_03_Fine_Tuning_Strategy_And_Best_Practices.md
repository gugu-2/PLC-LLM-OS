# DOC-03: Fine-Tuning Strategy & Best Practices

> **Classification**: ML Engineering Design Document  
> **Scope**: End-to-end fine-tuning strategy for the Lumina IEC-ST PLC domain model  
> **Date**: 2026-11-21  
> **Target Model Family**: Gemma-3 27B / Llama-3.1 70B / Qwen2.5-Coder-32B

---

## 1. What We Are Actually Building

This is not a general-purpose coding assistant. The target system is a **domain-specific industrial automation engineering assistant** that:

1. Generates syntactically valid, semantically correct IEC 61131-3 Structured Text Function Blocks for heavy manufacturing factory systems
2. Explains control logic, state transitions, and mathematical formulations in engineering context
3. Debugs existing PLC code and suggests improvements aligned with ISA-18.2, IEC 61511, and functional safety principles
4. Answers engineering questions about process control, MPC tuning, TMR architecture, and alarm management

This distinction fundamentally shapes every fine-tuning decision.

---

## 2. Pre-Fine-Tuning Corpus Remediation (Mandatory First Step)

**Fine-tuning on the current raw corpus will produce a mediocre model.** The following remediation must be completed before any training run.

### Step 1: Domain Triage
```bash
python validate_domain.py --input data/swarm_raw/ --reject-to data/rejected/ --keep-to data/verified/
# Expected: ~176 datasets rejected (20%), ~694 retained
```

### Step 2: Size Filtering
```bash
python validate_iec.py --min-chars 100000 --max-chars 700000 \
  --input data/verified/ --quarantine-to data/quarantine/
# Expected: ~115 micro-datasets quarantined
# Ultra-dense >700K: segment into logical parts or weight-down
```

### Step 3: Semantic Validation Sweep
```bash
python validate_semantic.py --input data/verified/ --report semantic_audit.json
```

**Post-remediation target corpus: ~570–620 high-quality datasets (< 300K chars median)**

---

## 3. Fine-Tuning Recipe: Stage-by-Stage

### Stage A — Continual Pre-Training (Optional but Recommended)

**Goal**: Saturate the base model with IEC 61131-3 vocabulary, syntax patterns, and industrial engineering terminology *before* teaching it to follow instructions.

**Data**: All 620 remediated datasets, **no chat template**. Present raw `FUNCTION_BLOCK ... END_FUNCTION_BLOCK` text as a plain text corpus.

**Configuration**:
```yaml
training_type: continual_pretraining
format: raw_text_continuation
learning_rate: 2e-5
warmup_steps: 200
max_seq_length: 32768
batch_size: 2
gradient_accumulation: 8
epochs: 1
packing: true  # Pack multiple short examples into one sequence
```

**Why**: The base model (Llama-3.1, Gemma-3) has seen minimal IEC 61131-3 code during pretraining. This stage teaches it the grammar of FUNCTION_BLOCK declarations, VAR sections, CASE state machines, and the mathematical notation of state-space models without the complexity of instruction-following.

---

### Stage B — Supervised Fine-Tuning (SFT) on Instruction Dataset

**Goal**: Teach the model to respond to engineering queries with correct IEC-ST code.

**Data**: 620 remediated chat-format datasets (the `{"messages": [...]}` structure already built).

**But first — split correctly**:
```python
# DO NOT random split. Use sector-stratified split:
train_set = 85%  # 527 datasets, balanced across all 7 sectors
val_set   = 10%  # 62 datasets, sector-balanced
test_set  = 5%   # 31 datasets, held out, never seen during training
```

**Configuration**:
```yaml
training_type: sft
chat_template: chatml  # or llama3 / gemma
learning_rate: 1e-4
warmup_ratio: 0.03
max_seq_length: 32768
batch_size: 1
gradient_accumulation: 16
epochs: 3
peft:
  method: lora
  r: 64
  alpha: 128
  target_modules: [q_proj, k_proj, v_proj, o_proj, gate_proj, up_proj, down_proj]
  dropout: 0.05
loss_on_completions_only: true  # Only compute loss on ASSISTANT turns, not on USER prompt
```

**Key Decision — `loss_on_completions_only: true`**: This is critical. The user prompt is a system instruction, not something we want the model to predict. Computing loss only on the generated IEC-ST code prevents the model from "gaming" the loss by memorizing instruction text.

---

### Stage C — Multi-Format SFT on Supplementary Data

**Goal**: Break the single-turn code-emission pattern. After Stage B, add multi-format data.

The supplementary data types (documented in DOC-04) are added in Stage C:
- Explanation Q&A pairs (20% of Stage C data)
- Debugging conversation chains (30% of Stage C data)
- Incremental modification pairs (25% of Stage C data)
- Concept-to-code translation examples (25% of Stage C data)

```yaml
training_type: sft
learning_rate: 5e-5  # Lower LR than Stage B to prevent catastrophic forgetting
epochs: 2
data_mixing:
  - source: data/verified/          # Original code datasets
    weight: 0.4
  - source: data/supplementary/qa/  # Q&A pairs
    weight: 0.2
  - source: data/supplementary/debug/  # Debug conversations
    weight: 0.25
  - source: data/supplementary/modify/  # Modification tasks
    weight: 0.15
```

---

### Stage D — Direct Preference Optimization (DPO)

**Goal**: Teach the model to prefer correct, safe, well-structured code over syntactically valid but semantically wrong alternatives.

**Data**: Preference pairs generated by:
1. Taking the model's own SFT outputs
2. Having a "judge" model (GPT-4o or Claude-3.5-Sonnet) rank them on:
   - Syntactic correctness
   - Semantic engineering validity
   - Completeness (all 14 FSM stages present, full TMR logic, etc.)
   - Physical plausibility (units, ranges, magnitudes)

```yaml
training_type: dpo
beta: 0.1
learning_rate: 5e-6
batch_size: 2
gradient_accumulation: 8
num_preference_pairs: 2000  # Target to generate
```

---

## 4. LoRA vs. Full Fine-Tuning Decision

| Factor | LoRA | Full Fine-Tuning |
|---|---|---|
| **GPU Memory** | 1× A100 80GB (32B model) | 8× A100 80GB (32B model) |
| **Training Time** | 4–8 hours per stage | 24–48 hours per stage |
| **Generalization Preservation** | Preserves base model reasoning | Risks catastrophic forgetting |
| **Merge & Serve** | Requires adapter loading at inference | Single merged model file |
| **Recommended For This Project** | ✅ **Yes** | Only if compute budget allows |

**Recommendation**: Use QLoRA (quantized LoRA) for all stages. 4-bit quantization of base model + 64-rank LoRA adapters = fits on a single A100 80GB or 2× A6000 48GB.

---

## 5. Evaluation Framework

### Metric 1: IEC Parity Pass Rate (IEC-PR)
```
IEC-PR = (Datasets with 100% parity) / (Total generated datasets)
Target: > 98%  (current corpus: ~95%)
```

### Metric 2: Domain Classification Accuracy (DCA)
```
DCA = (Generated code classified to correct manufacturing sector) / (Total queries)
Target: > 92%
Measured by: sector keyword extraction + manual spot-check
```

### Metric 3: Engineering Semantic Correctness Score (ESCS)
```
ESCS = Expert human rating (1-5 scale) on 50 randomly sampled outputs
Rubric:
  5 = Mathematically correct, industrially deployable with minimal review
  4 = Minor mathematical approximations, correct structure
  3 = Structural issues but correct control intent
  2 = Control logic errors (wrong FSM transitions, unstable MPC)
  1 = Incorrect or dangerous control logic
Target ESCS: > 3.8 average
```

### Metric 4: Instruction Diversity Response (IDR)
```
IDR = % of 8 instruction styles (see DOC-02) that produce correct output
Measured on held-out test set containing all 8 instruction styles
Target: > 85% across all styles
```

### Metric 5: Hallucination Rate (HR)
```
HR = % of generated code containing physically impossible constructs:
  - Non-physical matrix elements (NaN, Inf)
  - Temperature setpoints outside physical range (> 2000°C for steel)
  - Forces exceeding machine rated capacity by > 10%
Target: < 3%
```

---

## 6. Training Infrastructure Recommendations

| Component | Minimum | Recommended |
|---|---|---|
| **GPU** | 1× A100 80GB | 4× H100 80GB NVLink |
| **RAM** | 128 GB | 256 GB |
| **Storage** | 2 TB NVMe SSD | 8 TB NVMe RAID |
| **Framework** | Axolotl / Unsloth | Axolotl + DeepSpeed ZeRO-3 |
| **Base Model** | Qwen2.5-Coder-7B | Qwen2.5-Coder-32B |
| **Training Time (LoRA)** | ~6 hrs (7B) | ~18 hrs (32B) |
| **Cost Estimate (Cloud)** | ~\$80 (Lambda Labs A100) | ~\$600 (4× H100 on RunPod) |

---

## 7. Critical Pitfalls to Avoid

### Pitfall 1: Training on Ultra-Dense Datasets Without Segmentation
Datasets > 700K chars cannot fit in a 32K context window. If the training framework silently truncates at 32K tokens, the model learns from an incomplete FUNCTION_BLOCK — the `END_FUNCTION_BLOCK` is missing, the last FSM stages are absent, and the model learns to generate truncated output.

**Fix**: Segment ultra-dense datasets into logical parts (Phase 1–Phase 3, Phase 4–Phase 6) before training.

### Pitfall 2: Not Using `loss_on_completions_only`
If loss is computed on both user and assistant turns, the model learns to predict the user instruction text, which wastes capacity and distorts gradients.

### Pitfall 3: Overfitting on Sector Distribution
Automotive represents 18.5% of the corpus. If not balanced, the model will be biased toward automotive code. Use weighted sampling to equalize sector contribution during training.

### Pitfall 4: Evaluating Only on Seen Domains
Your test set must include manufacturing subsectors **not present** in the training set (e.g., continuous galvanizing line, tire vulcanization press). This tests true generalization, not memorization.

### Pitfall 5: Ignoring Catastrophic Forgetting
After domain fine-tuning, the model will degrade on general coding benchmarks. If the target is a **dedicated PLC assistant**, this is acceptable. If the target is a **general-purpose coding assistant with PLC specialization**, use LoRA adapters that can be enabled/disabled.
