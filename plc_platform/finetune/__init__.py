"""
plc_platform.finetune
=====================
QLoRA fine-tuning pipeline for the Industrial PLC LLM platform.

Modules:
    prepare_training_data  - Load, deduplicate and export training JSONL
    qlora_config           - Qwen2.5-Coder-32B QLoRA hyperparameters
    train                  - HuggingFace PEFT/TRL training entry-point
    evaluate_finetuned     - Post-training 31-benchmark gauntlet runner
"""

from plc_platform.finetune.prepare_training_data import TrainingDataPreparer
from plc_platform.finetune.qlora_config import QLORAConfig, get_default_qlora_config
from plc_platform.finetune.evaluate_finetuned import FinetunedModelEvaluator

__all__ = [
    "TrainingDataPreparer",
    "QLORAConfig",
    "get_default_qlora_config",
    "FinetunedModelEvaluator",
]
