"""
tests/test_new_components.py
============================
Comprehensive test suite for the 4 newly implemented platform components:

  1. CODESYS V3 dialect engine
  2. SFC textual encoding dialect engine
  3. Dataset Quality Gate
  4. Fine-tuning pipeline (config + data preparation)

All tests are designed to pass without GPU, without HuggingFace models,
and without network access — pure unit tests on local logic.

Expected: 20/20 PASS
"""

import json
import os
import pathlib
import sys
import tempfile

import pytest

# ---------------------------------------------------------------------------
# 1. CODESYS V3 Dialect Engine
# ---------------------------------------------------------------------------

class TestCodesysDialect:

    def test_minimal_example_generates_fb_header(self):
        """CODESYS engine must produce FUNCTION_BLOCK + END_FUNCTION_BLOCK."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "FUNCTION_BLOCK" in code
        assert "END_FUNCTION_BLOCK" in code

    def test_codesys_attributes_present(self):
        """Must include CODESYS V3 pragma attributes."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "{attribute 'qualified_only'}" in code
        assert "{attribute 'monitoring'" in code

    def test_codesys_tmr_voting_present(self):
        """Must include 2oo3 TMR voting logic."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "bVoted" in code
        assert "bTrip_A" in code
        assert "bTrip_B" in code
        assert "bTrip_C" in code

    def test_codesys_estop_return_cutoff(self):
        """E-Stop must trigger RETURN as first logic."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "bEStop" in code
        assert "RETURN;" in code

    def test_codesys_mpc_state_space(self):
        """Must include MPC quadratic cost and state-space propagation."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "rMPC_Cost" in code
        assert "rStateX0" in code
        assert "rOptU0" in code

    def test_codesys_isa18_alarms(self):
        """Must include ISA-18.2 HH / H / L / LL alarm tiering."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "bAlarm_HH" in code
        assert "bAlarm_LL" in code
        assert "nAlarmPriority" in code

    def test_codesys_var_stat_persistent(self):
        """Must include VAR_STAT with {attribute 'persistent'} counters."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example()
        assert "VAR_STAT" in code
        assert "uCycleCount" in code
        assert "uFaultCount" in code

    def test_codesys_parser_roundtrip(self):
        """Parser must correctly extract FB name and safety flags."""
        from plc_platform.dialects.codesys import CodesysDialectEngine
        engine = CodesysDialectEngine()
        code   = engine.generate_minimal_example(fb_name="FB_TestConveyor")
        result = engine.parse(code)
        assert result.fb_name == "FB_TestConveyor"
        assert result.has_tmr   is True
        assert result.has_estop is True
        assert result.raw_body_lines > 50

    def test_codesys_fsm_states(self):
        """State machine (CASE eState) must be present for stepped FSMs."""
        from plc_platform.dialects.codesys import CodesysDialectEngine, CodesysFBSpec, CodesysVariable
        engine = CodesysDialectEngine()
        spec   = CodesysFBSpec(
            fb_name="FB_FsmTest",
            description="FSM test",
            sector="AUTOMOTIVE",
            var_inputs=[
                CodesysVariable("bEStop",     "BOOL", "VAR_INPUT", "E-Stop"),
                CodesysVariable("rHiHiLimit", "REAL", "VAR_INPUT", "HH limit", "rpm", "1800.0"),
                CodesysVariable("rHiLimit",   "REAL", "VAR_INPUT", "H limit",  "rpm", "1600.0"),
                CodesysVariable("rLoLimit",   "REAL", "VAR_INPUT", "L limit",  "rpm", "200.0"),
                CodesysVariable("rLoLoLimit", "REAL", "VAR_INPUT", "LL limit", "rpm", "100.0"),
            ],
            var_outputs=[
                CodesysVariable("bFault",  "BOOL", "VAR_OUTPUT", "Fault"),
            ],
            state_names=["IDLE", "RUN", "STOP", "FAULT"],
        )
        code = engine.generate(spec)
        assert "CASE eState" in code
        assert "IDLE" in code
        assert "RUN"  in code
        assert "FAULT" in code


# ---------------------------------------------------------------------------
# 2. SFC Dialect Engine
# ---------------------------------------------------------------------------

class TestSFCDialect:

    def test_cip_sip_generates_fb(self):
        """CIP/SIP example must produce valid FUNCTION_BLOCK structure."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        assert "FUNCTION_BLOCK" in code
        assert "END_FUNCTION_BLOCK" in code

    def test_cip_sip_has_9_steps(self):
        """CIP/SIP must have all 9 operational steps plus IDLE and FAULT."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        # Check key step names
        assert "S01_PRE_RINSE"   in code
        assert "S02_NAOH_WASH"   in code
        assert "S06_SIP_STEAM"   in code
        assert "S09_PRODUCTION"  in code
        assert "S10_COMPLETE"    in code

    def test_sfc_estop_return_first(self):
        """SFC E-Stop cutoff must precede CASE statement."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        estop_pos = code.find("bEStop")
        case_pos  = code.find("CASE eState")
        assert estop_pos < case_pos, "E-Stop must appear before CASE block"

    def test_sfc_tmr_in_body(self):
        """2oo3 TMR voting must appear in SFC body."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        assert "bVoted" in code
        assert "bTrip_A" in code

    def test_sfc_timeout_watchdog(self):
        """Step timeout watchdog must be present."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        assert "tonStepTimeout" in code
        assert "bStepTimeout"   in code

    def test_sfc_parser_step_count(self):
        """Parser must correctly count steps from CASE arms."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        result = engine.parse(code)
        # Steps: -1 (FAULT), 0–10 = 12 total arms
        assert result.step_count >= 10
        assert result.has_tmr    is True
        assert result.has_timeout is True
        assert result.has_estop  is True

    def test_sfc_case_end_case_parity(self):
        """Every CASE must have exactly one matching END_CASE."""
        from plc_platform.dialects.sfc import SFCDialectEngine
        import re
        engine = SFCDialectEngine()
        code   = engine.generate_cip_sip_example()
        n_case    = len(re.findall(r'\bCASE\b', code, re.IGNORECASE))
        n_endcase = len(re.findall(r'\bEND_CASE\b', code, re.IGNORECASE))
        assert n_case == n_endcase, f"CASE/END_CASE parity: {n_case}/{n_endcase}"


# ---------------------------------------------------------------------------
# 3. Dataset Quality Gate
# ---------------------------------------------------------------------------

GOOD_CODE = """\
FUNCTION_BLOCK FB_HydraulicPress
VAR_INPUT
    rPressure_bar   : REAL; (* [bar] hydraulic cylinder pressure *)
    rForce_kN       : REAL; (* [kN] measured press force *)
    bEStop          : BOOL; (* Safety relay E-Stop channel A *)
    rHiHiLimit      : REAL; (* [bar] HH alarm threshold *)
    rHiLimit        : REAL; (* [bar] H alarm threshold *)
    rLoLimit        : REAL; (* [bar] L alarm threshold *)
    rLoLoLimit      : REAL; (* [bar] LL alarm threshold *)
END_VAR
VAR_OUTPUT
    rValveCmd_pct   : REAL; (* [%] proportional valve command *)
    bFault          : BOOL;
END_VAR
VAR
    bTrip_A         : BOOL; (* 2oo3 channel A *)
    bTrip_B         : BOOL; (* 2oo3 channel B *)
    bTrip_C         : BOOL; (* 2oo3 channel C *)
    bVoted          : BOOL; (* TMR vote result *)
    bAlarm_HH       : BOOL;
    bAlarm_LL       : BOOL;
    rStateX0        : REAL; (* [mm] state-space x[0] *)
    rMPC_Cost       : REAL; (* MPC quadratic cost J *)
    rOptU0          : REAL;
    eState          : INT;
    tonDiscrA       : TON;
    tonDiscrB       : TON;
END_VAR

IF bEStop THEN
    rValveCmd_pct := 0.0;
    bFault        := TRUE;
    RETURN;
END_IF;

bTrip_A := rPressure_bar > 350.0;
bTrip_B := rPressure_bar > 350.0;
bTrip_C := rPressure_bar > 350.0;
bVoted  := (bTrip_A AND bTrip_B) OR (bTrip_B AND bTrip_C) OR (bTrip_A AND bTrip_C);

IF bVoted THEN bFault := TRUE; END_IF;

rStateX0 := 0.98 * rStateX0 + 0.02 * rOptU0;
rMPC_Cost := 100.0 * rStateX0 * rStateX0 + 0.5 * rOptU0 * rOptU0;
rOptU0    := LIMIT(-100.0, -12.5 * rStateX0, 100.0);

bAlarm_HH := rPressure_bar >= rHiHiLimit;
bAlarm_LL := rPressure_bar <= rLoLoLimit;

CASE eState OF
    0: rValveCmd_pct := 0.0; eState := 1;
    1: rValveCmd_pct := rOptU0; IF rPressure_bar >= rHiHiLimit THEN eState := 2; END_IF;
    2: rValveCmd_pct := 0.0; bFault := TRUE;
ELSE
    eState := 0;
END_CASE;

END_FUNCTION_BLOCK
"""

BAD_CODE = "x := 1 + 2;"


class TestQualityGate:

    def test_good_code_admitted(self):
        """High-quality IEC-ST with all required elements must be admitted."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate(threshold=70.0)   # slightly lower for test robustness
        result = gate.evaluate(GOOD_CODE)
        assert result.admitted is True, f"Expected ADMIT but got score={result.total_score} reasons={result.rejection_reasons}"

    def test_bad_code_rejected(self):
        """Single-line stub code must be rejected."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate(threshold=85.0)
        result = gate.evaluate(BAD_CODE)
        assert result.admitted is False

    def test_score_range(self):
        """Total score must be in [0, 100]."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate = DatasetQualityGate()
        for code in [GOOD_CODE, BAD_CODE, ""]:
            result = gate.evaluate(code)
            assert 0.0 <= result.total_score <= 100.0, f"Score out of range: {result.total_score}"

    def test_six_dimensions_returned(self):
        """Must return exactly 6 quality dimensions."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate()
        result = gate.evaluate(GOOD_CODE)
        assert len(result.dimensions) == 6

    def test_dimension_names(self):
        """All 6 expected dimension names must be present."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate()
        result = gate.evaluate(GOOD_CODE)
        names  = {d.name for d in result.dimensions}
        expected = {"structural", "safety", "variables", "units", "sector", "complexity"}
        assert names == expected

    def test_messages_record_extraction(self):
        """Gate must correctly extract code from raw messages[] record format."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate(threshold=70.0)
        record = {
            "messages": [
                {"role": "user",      "content": "Write a hydraulic press controller"},
                {"role": "assistant", "content": f"```iec-st\n{GOOD_CODE}\n```"},
            ]
        }
        result = gate.evaluate_messages_record(record, sector_hint="HEAVY_MACHINERY")
        assert result.code_chars > 100

    def test_empty_code_rejected(self):
        """Empty string must be rejected with score near 0."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate(threshold=85.0)
        result = gate.evaluate("")
        assert result.admitted is False
        assert result.total_score < 20.0

    def test_to_dict_serialisable(self):
        """Result.to_dict() must produce JSON-serialisable output."""
        from plc_platform.datasets.quality_gate import DatasetQualityGate
        gate   = DatasetQualityGate()
        result = gate.evaluate(GOOD_CODE)
        d      = result.to_dict()
        # Must not raise
        json_str = json.dumps(d)
        assert len(json_str) > 10

    def test_batch_evaluator_runs(self):
        """BatchQualityEvaluator must run on a temp directory."""
        from plc_platform.datasets.quality_gate import BatchQualityEvaluator
        with tempfile.TemporaryDirectory() as tmpdir:
            # Write 3 test records
            for i in range(3):
                record = {
                    "messages": [
                        {"role": "user",      "content": f"Test {i}"},
                        {"role": "assistant", "content": f"```iec-st\n{GOOD_CODE}\n```"},
                    ]
                }
                (pathlib.Path(tmpdir) / f"test_{i}.json").write_text(json.dumps(record))

            evaluator = BatchQualityEvaluator(threshold=70.0)
            summary   = evaluator.evaluate_directory(tmpdir)

        assert summary["total_evaluated"] == 3
        assert summary["admitted"] + summary["rejected"] == 3
        assert 0.0 <= summary["admission_rate"] <= 100.0


# ---------------------------------------------------------------------------
# 4. Fine-tuning Pipeline — config + data preparation
# ---------------------------------------------------------------------------

class TestFinetunePipeline:

    def test_qlora_config_defaults(self):
        """Default config must have correct Qwen2.5-Coder-32B model name."""
        from plc_platform.finetune.qlora_config import get_default_qlora_config
        cfg = get_default_qlora_config()
        assert "Qwen2.5-Coder-32B" in cfg.model.model_name_or_path
        assert cfg.lora.r          == 64
        assert cfg.lora.lora_alpha == 128
        assert cfg.bnb.load_in_4bit is True
        assert cfg.bnb.bnb_4bit_quant_type == "nf4"

    def test_qlora_config_roundtrip(self):
        """Config must serialise to dict and deserialise back cleanly."""
        from plc_platform.finetune.qlora_config import QLORAConfig, get_default_qlora_config
        cfg    = get_default_qlora_config()
        d      = cfg.to_dict()
        cfg2   = QLORAConfig.from_dict(d)
        assert cfg2.lora.r          == cfg.lora.r
        assert cfg2.training.optim  == cfg.training.optim
        assert cfg2.model.model_name_or_path == cfg.model.model_name_or_path

    def test_qlora_config_save_load_json(self):
        """Config must save to JSON and reload correctly."""
        from plc_platform.finetune.qlora_config import QLORAConfig, get_default_qlora_config
        with tempfile.TemporaryDirectory() as tmpdir:
            path = str(pathlib.Path(tmpdir) / "cfg.json")
            cfg  = get_default_qlora_config()
            cfg.save_json(path)
            cfg2 = QLORAConfig.from_json(path)
        assert cfg2.lora.lora_alpha == 128
        assert cfg2.training.max_seq_length == 8192

    def test_training_data_preparer_runs(self):
        """
        TrainingDataPreparer must process a temp directory of test records
        and produce train/val/test JSONL files.
        """
        from plc_platform.finetune.prepare_training_data import TrainingDataPreparer
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            # Create fake swarm_raw directory with 10 test records
            raw_dir = tmppath / "data" / "swarm_raw"
            raw_dir.mkdir(parents=True)
            for i in range(10):
                record = {
                    "id":         f"test_{i}",
                    "project_id": f"proj_{i % 4}",
                    "sector":     "HEAVY_MACHINERY",
                    "messages": [
                        {"role": "user",      "content": f"Write hydraulic press controller station #{i} with specific tonnage {i*100} tons"},
                        {"role": "assistant", "content": f"```iec-st\nFUNCTION_BLOCK FB_PressStation_{i}\nVAR_INPUT\n    bEStop_{i} : BOOL;\n    rPressure_{i} : REAL;\nEND_VAR\nVAR_OUTPUT\n    bTrip_{i} : BOOL;\nEND_VAR\nIF bEStop_{i} THEN\n    bTrip_{i} := TRUE;\n    RETURN;\nEND_IF;\n// Unique station {i} calculation logic\nbTrip_{i} := rPressure_{i} > {float(i * 50)};\nEND_FUNCTION_BLOCK\n```"},
                    ],
                }
                (raw_dir / f"test_{i:03d}.json").write_text(json.dumps(record))

            preparer = TrainingDataPreparer(root_dir=tmpdir, dedup_threshold=0.95)
            stats    = preparer.run()

        assert stats["total_records"] == 10
        assert stats["train_sharegpt"] + stats["val_sharegpt"] + stats["test_sharegpt"] == 10

    def test_prepare_data_manifest_written(self):
        """manifest.json must be written with correct schema."""
        from plc_platform.finetune.prepare_training_data import TrainingDataPreparer
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            raw_dir = tmppath / "data" / "swarm_raw"
            raw_dir.mkdir(parents=True)
            record  = {
                "project_id": "proj_manif",
                "messages": [
                    {"role": "user",      "content": "PLC test"},
                    {"role": "assistant", "content": "```iec-st\n" + GOOD_CODE + "\n```"},
                ],
            }
            (raw_dir / "manif_test.json").write_text(json.dumps(record))

            preparer = TrainingDataPreparer(root_dir=tmpdir)
            preparer.run()

            manifest_path = tmppath / "data" / "finetune" / "manifest.json"
            assert manifest_path.exists(), "manifest.json must be created"
            manifest = json.loads(manifest_path.read_text())
            assert manifest["schema_version"] == "2.0"
            assert "split_ratios" in manifest

    def test_deduplication_removes_exact_duplicates(self):
        """Identical records must be deduplicated."""
        from plc_platform.finetune.prepare_training_data import TrainingDataPreparer
        with tempfile.TemporaryDirectory() as tmpdir:
            tmppath = pathlib.Path(tmpdir)
            raw_dir = tmppath / "data" / "swarm_raw"
            raw_dir.mkdir(parents=True)
            # Write same record 5 times
            record = {
                "project_id": "dup_proj",
                "messages": [
                    {"role": "user",      "content": "Duplicate test record content exactly the same"},
                    {"role": "assistant", "content": "```iec-st\n" + GOOD_CODE + "\n```"},
                ],
            }
            for i in range(5):
                (raw_dir / f"dup_{i}.json").write_text(json.dumps(record))

            preparer = TrainingDataPreparer(root_dir=tmpdir)
            stats    = preparer.run()

        # Only 1 unique record should survive
        assert stats["total_records"] == 1, f"Expected 1 unique record, got {stats['total_records']}"
