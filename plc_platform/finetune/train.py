"""
train.py
========
HuggingFace PEFT + TRL SFTTrainer entry-point for QLoRA fine-tuning of
Qwen2.5-Coder-32B-Instruct on the Industrial PLC dataset.

This script is the production training launcher. It CANNOT be run in
environments without GPU, bitsandbytes, flash-attn, peft, and trl installed.
In CI it is imported as a module for config validation only.

Usage (single GPU, 80 GB VRAM):
    python -m plc_platform.finetune.train \\
        --config qlora_config.json \\
        --run-name plc_qwen25_r64_v1

Usage (multi-GPU DDP, 4× A100):
    torchrun --nproc_per_node=4 -m plc_platform.finetune.train \\
        --config qlora_config.json \\
        --run-name plc_qwen25_r64_v1_4gpu
"""

from __future__ import annotations

import argparse
import json
import logging
import os
import pathlib
import sys
from typing import Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Config import (always available)
# ---------------------------------------------------------------------------
from plc_platform.finetune.qlora_config import QLORAConfig, get_default_qlora_config
from plc_platform.finetune.prepare_training_data import TrainingDataPreparer

# ---------------------------------------------------------------------------
# GPU-stack imports (guarded — CI environments may not have them)
# ---------------------------------------------------------------------------
_GPU_STACK_AVAILABLE = False
try:
    import torch
    from datasets import load_dataset
    from peft import LoraConfig, get_peft_model, prepare_model_for_kbit_training
    from transformers import (
        AutoModelForCausalLM,
        AutoTokenizer,
        BitsAndBytesConfig,
        TrainingArguments,
    )
    from trl import SFTTrainer, DataCollatorForCompletionOnlyLM
    _GPU_STACK_AVAILABLE = True
except ImportError as _imp_err:
    logger.warning(
        "GPU stack not available (%s). Training cannot proceed; "
        "config loading and data preparation still work.",
        _imp_err,
    )


# ---------------------------------------------------------------------------
# Helper: build HuggingFace objects from config dataclasses
# ---------------------------------------------------------------------------

def _build_bnb_config(cfg: QLORAConfig):
    """Build BitsAndBytesConfig from QLORAConfig.bnb."""
    import torch  # noqa: F811
    dtype_map = {"bfloat16": torch.bfloat16, "float16": torch.float16, "float32": torch.float32}
    return BitsAndBytesConfig(
        load_in_4bit              = cfg.bnb.load_in_4bit,
        bnb_4bit_quant_type       = cfg.bnb.bnb_4bit_quant_type,
        bnb_4bit_use_double_quant = cfg.bnb.bnb_4bit_use_double_quant,
        bnb_4bit_compute_dtype    = dtype_map.get(cfg.bnb.bnb_4bit_compute_dtype, torch.bfloat16),
    )


def _build_lora_config(cfg: QLORAConfig) -> "LoraConfig":
    """Build PEFT LoraConfig from QLORAConfig.lora."""
    return LoraConfig(
        r              = cfg.lora.r,
        lora_alpha     = cfg.lora.lora_alpha,
        target_modules = cfg.lora.target_modules,
        lora_dropout   = cfg.lora.lora_dropout,
        bias           = cfg.lora.bias,
        task_type      = cfg.lora.task_type,
    )


def _build_training_args(cfg: QLORAConfig, run_name: str) -> "TrainingArguments":
    """Build HuggingFace TrainingArguments from QLORAConfig.training."""
    t = cfg.training
    out_dir = str(pathlib.Path(t.output_dir) / run_name)
    return TrainingArguments(
        output_dir                  = out_dir,
        num_train_epochs            = t.num_train_epochs,
        per_device_train_batch_size = t.per_device_train_batch_size,
        per_device_eval_batch_size  = t.per_device_eval_batch_size,
        gradient_accumulation_steps = t.gradient_accumulation_steps,
        gradient_checkpointing      = t.gradient_checkpointing,
        max_grad_norm               = t.max_grad_norm,
        learning_rate               = t.learning_rate,
        weight_decay                = t.weight_decay,
        optim                       = t.optim,
        lr_scheduler_type           = t.lr_scheduler_type,
        warmup_ratio                = t.warmup_ratio,
        fp16                        = t.fp16,
        bf16                        = t.bf16,
        logging_steps               = t.logging_steps,
        save_steps                  = t.save_steps,
        eval_steps                  = t.eval_steps,
        evaluation_strategy         = t.evaluation_strategy,
        save_total_limit            = t.save_total_limit,
        load_best_model_at_end      = t.load_best_model_at_end,
        report_to                   = t.report_to,
        group_by_length             = t.group_by_length,
        dataloader_num_workers      = t.dataloader_num_workers,
        remove_unused_columns       = t.remove_unused_columns,
        ddp_find_unused_parameters  = t.ddp_find_unused_parameters,
        neftune_noise_alpha         = t.neftune_noise_alpha,
    )


# ---------------------------------------------------------------------------
# Dataset formatter for ShareGPT conversations
# ---------------------------------------------------------------------------

def _format_sharegpt_to_text(example: dict, tokenizer) -> dict:
    """
    Convert a ShareGPT conversations list to a single formatted string
    using the tokenizer's chat template (Qwen2.5-Coder supports chatml).
    """
    messages = []
    for turn in example.get("conversations", []):
        role = "user" if turn["from"] == "human" else "assistant"
        messages.append({"role": role, "content": turn["value"]})

    # Use tokenizer's apply_chat_template if available
    if hasattr(tokenizer, "apply_chat_template") and tokenizer.chat_template:
        text = tokenizer.apply_chat_template(
            messages,
            tokenize=False,
            add_generation_prompt=False,
        )
    else:
        # Fallback: simple chatml format
        parts = []
        for m in messages:
            parts.append(f"<|im_start|>{m['role']}\n{m['content']}<|im_end|>")
        text = "\n".join(parts)

    return {"text": text}


# ---------------------------------------------------------------------------
# Main training function
# ---------------------------------------------------------------------------

def train(
    cfg: QLORAConfig,
    run_name: str = "plc_qwen25_qlora_v1",
    prepare_data: bool = True,
    root_dir: str = ".",
) -> str:
    """
    Execute full QLoRA training.

    Parameters
    ----------
    cfg         : QLORAConfig — complete training configuration
    run_name    : str — name for this training run (used in output paths)
    prepare_data: bool — if True, run TrainingDataPreparer first
    root_dir    : str — project root (for data path resolution)

    Returns
    -------
    str — path to the final checkpoint directory
    """
    if not _GPU_STACK_AVAILABLE:
        raise RuntimeError(
            "GPU stack (torch, peft, trl, bitsandbytes) not installed. "
            "Cannot run training. Install requirements/train_requirements.txt first."
        )

    # ------------------------------------------------------------------
    # Stage 1: Prepare training data
    # ------------------------------------------------------------------
    if prepare_data:
        logger.info("Stage 1: Preparing training data...")
        preparer = TrainingDataPreparer(root_dir=root_dir)
        stats    = preparer.run()
        logger.info("Data preparation complete: %s", stats)

    root = pathlib.Path(root_dir)

    # ------------------------------------------------------------------
    # Stage 2: Load tokenizer
    # ------------------------------------------------------------------
    logger.info("Stage 2: Loading tokenizer from %s", cfg.model.model_name_or_path)
    tokenizer = AutoTokenizer.from_pretrained(
        cfg.model.model_name_or_path,
        trust_remote_code=cfg.model.trust_remote_code,
        cache_dir=cfg.model.cache_dir,
        padding_side="right",   # Required for SFT completion masking
    )
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token

    # ------------------------------------------------------------------
    # Stage 3: Load quantised base model
    # ------------------------------------------------------------------
    logger.info("Stage 3: Loading quantised model (QLoRA NF4)...")
    bnb_config = _build_bnb_config(cfg)
    dtype_map = {"bfloat16": torch.bfloat16, "float16": torch.float16}
    model = AutoModelForCausalLM.from_pretrained(
        cfg.model.model_name_or_path,
        quantization_config  = bnb_config,
        trust_remote_code    = cfg.model.trust_remote_code,
        cache_dir            = cfg.model.cache_dir,
        attn_implementation  = cfg.model.attn_implementation,
        torch_dtype          = dtype_map.get(cfg.model.torch_dtype, torch.bfloat16),
        device_map           = "auto",
    )
    model = prepare_model_for_kbit_training(model, use_gradient_checkpointing=cfg.training.gradient_checkpointing)

    # ------------------------------------------------------------------
    # Stage 4: Attach LoRA adapters
    # ------------------------------------------------------------------
    logger.info("Stage 4: Attaching LoRA adapters (r=%d, alpha=%d)...", cfg.lora.r, cfg.lora.lora_alpha)
    lora_config = _build_lora_config(cfg)
    model       = get_peft_model(model, lora_config)
    model.print_trainable_parameters()

    # ------------------------------------------------------------------
    # Stage 5: Load datasets
    # ------------------------------------------------------------------
    logger.info("Stage 5: Loading datasets...")
    ds_cfg = cfg.dataset

    def _load_split(filepath: str):
        abs_path = str(root / filepath)
        if not pathlib.Path(abs_path).exists():
            raise FileNotFoundError(
                f"Training data not found: {abs_path}. "
                "Run TrainingDataPreparer first (prepare_data=True)."
            )
        return load_dataset("json", data_files=abs_path, split="train")

    train_dataset = _load_split(ds_cfg.train_file)
    eval_dataset  = _load_split(ds_cfg.val_file)

    if ds_cfg.max_samples:
        train_dataset = train_dataset.select(range(min(ds_cfg.max_samples, len(train_dataset))))

    # Format to single text string
    train_dataset = train_dataset.map(
        lambda ex: _format_sharegpt_to_text(ex, tokenizer),
        num_proc=4,
    )
    eval_dataset = eval_dataset.map(
        lambda ex: _format_sharegpt_to_text(ex, tokenizer),
        num_proc=4,
    )

    # ------------------------------------------------------------------
    # Stage 6: Build TrainingArguments and SFTTrainer
    # ------------------------------------------------------------------
    logger.info("Stage 6: Building SFTTrainer...")
    training_args = _build_training_args(cfg, run_name)

    trainer = SFTTrainer(
        model           = model,
        tokenizer       = tokenizer,
        train_dataset   = train_dataset,
        eval_dataset    = eval_dataset,
        dataset_text_field = "text",
        max_seq_length  = cfg.training.max_seq_length,
        packing         = cfg.training.packing,
        args            = training_args,
    )

    # ------------------------------------------------------------------
    # Stage 7: Train
    # ------------------------------------------------------------------
    logger.info("Stage 7: Starting training (run: %s)...", run_name)
    trainer.train()
    logger.info("Training complete.")

    # ------------------------------------------------------------------
    # Stage 8: Save final adapter
    # ------------------------------------------------------------------
    final_path = str(pathlib.Path(cfg.training.output_dir) / run_name / "final_adapter")
    trainer.model.save_pretrained(final_path)
    tokenizer.save_pretrained(final_path)
    logger.info("Final adapter saved to: %s", final_path)

    return final_path


# ---------------------------------------------------------------------------
# CLI entry-point
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
    parser = argparse.ArgumentParser(description="QLoRA fine-tuning launcher for Industrial PLC LLM")
    parser.add_argument("--config",       default=None,   help="Path to qlora_config.json (uses defaults if omitted)")
    parser.add_argument("--run-name",     default="plc_qwen25_qlora_v1", help="Training run name")
    parser.add_argument("--root-dir",     default=".",    help="Project root directory")
    parser.add_argument("--no-data-prep", action="store_true", help="Skip data preparation")
    args = parser.parse_args()

    cfg = QLORAConfig.from_json(args.config) if args.config else get_default_qlora_config()
    final = train(
        cfg=cfg,
        run_name=args.run_name,
        prepare_data=not args.no_data_prep,
        root_dir=args.root_dir,
    )
    print(f"Training complete. Final adapter: {final}")
