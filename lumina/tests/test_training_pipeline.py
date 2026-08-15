import pytest
import os
from lumina.training.train_dataset_formatter import format_instruction_record, prepare_training_split
from lumina.training.train_plc_llm import TrainingConfig, build_training_pipeline, run_training_dry_run
from lumina.training.train_rlsf_dpo import SymbolicRewardEvaluator, run_dpo_pipeline_check
from lumina.training.export_edge_model import EdgeModelExporter


def test_dataset_formatter_record_structure(tmp_path):
    record = format_instruction_record(
        user_prompt="Write a timer block in Structured Text",
        assistant_code="TON_Inst(IN := bStart, PT := T#5S);"
    )
    assert "messages" in record
    assert len(record["messages"]) == 3
    assert record["messages"][0]["role"] == "system"
    assert record["messages"][1]["role"] == "user"
    assert record["messages"][2]["role"] == "assistant"

    # Test split
    train_p, val_p = prepare_training_split([record, record], output_dir=str(tmp_path), train_ratio=0.5)
    assert os.path.exists(train_p)
    assert os.path.exists(val_p)


def test_training_pipeline_config_and_dry_run():
    cfg = TrainingConfig(model_name_or_path="Qwen/Qwen2.5-Coder-7B-Instruct")
    pipe = build_training_pipeline(cfg)
    assert pipe["status"] == "PIPELINE_CONFIGURED"
    assert cfg.lora_r == 64
    assert cfg.lora_alpha == 128
    assert run_training_dry_run() is True


def test_symbolic_reward_evaluator_rlsf_dpo():
    assert run_dpo_pipeline_check() is True


def test_symbolic_reward_inversion_protection():
    evaluator = SymbolicRewardEvaluator()
    # If chosen and rejected have inverted rules where chosen is worse, ensure it returns None
    invalid_pair = evaluator.generate_preference_pair(
        prompt="Test inversion",
        valid_code="VAR nRamp : INT := 100; END_VAR", # Bad
        unsafe_code="VAR nRamp : INT := 380; END_VAR", # Good
        variables={"DecelRamp_ms": "INT"},
        rules_chosen=[{"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 0, "max": 1000, "condition": 100}],
        rules_rejected=[{"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 200, "max": 800, "condition": 380}],
        safety_invariants=["DECEL_RAMP_SAFE_BOUNDS"]
    )
    assert invalid_pair is None


def test_edge_model_exporter_matrix():
    exporter = EdgeModelExporter(base_model="Qwen/Qwen2.5-Coder-7B-Instruct")
    matrix = exporter.plan_export_matrix()
    assert "GGUF_Q4_K_M" in matrix["export_formats"]
    assert matrix["export_formats"]["GGUF_Q4_K_M"]["vram_required_gb"] == 4.8
    cmd = exporter.generate_conversion_command()
    assert "convert_hf_to_gguf" in cmd


def test_edge_model_exporter_14b_scaling_and_awq():
    exporter_14b = EdgeModelExporter(base_model="Qwen/Qwen2.5-Coder-14B-Instruct")
    matrix_14b = exporter_14b.plan_export_matrix()
    assert matrix_14b["param_count_billions"] == 14.7
    assert matrix_14b["export_formats"]["GGUF_Q4_K_M"]["vram_required_gb"] > 4.8
    
    # Test AWQ conversion command
    awq_cmd = exporter_14b.generate_conversion_command("AWQ_4BIT_vLLM", output_path="./lumina_awq")
    assert "python -m awq.entry" in awq_cmd
    
    # Test Merge script generation
    merge_script = exporter_14b.generate_merge_script()
    assert "merge_and_unload" in merge_script
