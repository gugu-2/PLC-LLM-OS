"""
evaluate_finetuned.py
=====================
Post-training 31-benchmark gauntlet runner for fine-tuned PLC LLM checkpoints.

Runs the full ComparativeBenchmarkRunner against:
  - Base model (no fine-tuning)
  - Base + RAG
  - Fine-tuned adapter
  - Fine-tuned + RAG   ← expected production winner

Outputs a markdown scorecard and JSON results to data/finetune/eval_results/.

Usage:
    python -m plc_platform.finetune.evaluate_finetuned \\
        --adapter  data/finetune/checkpoints/plc_qwen25_qlora_v1/final_adapter \\
        --base     Qwen/Qwen2.5-Coder-32B-Instruct \\
        --out-dir  data/finetune/eval_results

The script can also be imported programmatically:
    from plc_platform.finetune.evaluate_finetuned import FinetunedModelEvaluator
    evaluator = FinetunedModelEvaluator(adapter_path="...", base_model="...")
    scorecard = evaluator.run()
"""

from __future__ import annotations

import argparse
import json
import logging
import pathlib
from datetime import datetime, timezone
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# Always-available imports
# ---------------------------------------------------------------------------
from plc_platform.evaluate.benchmarks import BENCHMARK_CATALOG, BenchmarkItem
from plc_platform.evaluate.metrics import MetricsCalculator
from plc_platform.evaluate.runner import ComparativeBenchmarkRunner, RunnerConfig
from plc_platform.rag.retriever import HybridRetriever
from plc_platform.rag.prompt_augmenter import PromptAugmenter

# ---------------------------------------------------------------------------
# Optional GPU imports
# ---------------------------------------------------------------------------
_INFERENCE_AVAILABLE = False
try:
    import torch
    from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
    from peft import PeftModel
    _INFERENCE_AVAILABLE = True
except ImportError as _e:
    logger.warning("Inference stack not available (%s). Stub mode active.", _e)


# ---------------------------------------------------------------------------
# Stub LLM callable for environments without GPU
# ---------------------------------------------------------------------------

class _StubLLM:
    """
    Deterministic stub used in CI / no-GPU environments.
    Returns a syntactically valid but trivial IEC-ST block so that
    metric calculation paths are exercised without real model inference.
    """
    STUB_CODE = (
        "FUNCTION_BLOCK FB_StubEval\n"
        "VAR_INPUT\n"
        "    rSetpoint : REAL; (* [bar] target pressure *)\n"
        "    rActual   : REAL; (* [bar] measured pressure *)\n"
        "    bEStop    : BOOL; (* E-Stop relay channel A *)\n"
        "END_VAR\n"
        "VAR_OUTPUT\n"
        "    rOutput   : REAL; (* [%] valve opening *)\n"
        "    bFault    : BOOL;\n"
        "END_VAR\n"
        "VAR\n"
        "    rError    : REAL; (* [bar] control deviation *)\n"
        "    bTrip_A   : BOOL;\n"
        "    bTrip_B   : BOOL;\n"
        "    bTrip_C   : BOOL; (* [ms] debounce dummy *)\n"
        "    bVoted    : BOOL; (* 2oo3 TMR vote result *)\n"
        "END_VAR\n"
        "\n"
        "IF bEStop THEN\n"
        "    rOutput := 0.0;\n"
        "    bFault  := TRUE;\n"
        "    RETURN;\n"
        "END_IF;\n"
        "\n"
        "(* 2oo3 TMR voting *)\n"
        "bTrip_A := rActual > 10.0;\n"
        "bTrip_B := rActual > 10.0;\n"
        "bTrip_C := rActual > 10.0;\n"
        "bVoted  := (bTrip_A AND bTrip_B) OR (bTrip_B AND bTrip_C) OR (bTrip_A AND bTrip_C);\n"
        "\n"
        "rError  := rSetpoint - rActual;\n"
        "rOutput := LIMIT(0.0, rError * 2.5, 100.0);\n"
        "bFault  := bVoted;\n"
        "END_FUNCTION_BLOCK"
    )

    def __call__(self, prompt: str, **kwargs) -> str:
        return self.STUB_CODE


# ---------------------------------------------------------------------------
# Real LLM callable
# ---------------------------------------------------------------------------

class _HFAdapterLLM:
    """
    HuggingFace text-generation pipeline wrapping a PEFT LoRA adapter
    merged onto the base model for inference.
    """

    def __init__(
        self,
        base_model_path: str,
        adapter_path: Optional[str] = None,
        max_new_tokens: int = 4096,
        temperature: float = 0.1,
    ):
        if not _INFERENCE_AVAILABLE:
            raise RuntimeError("torch/transformers/peft not installed.")

        logger.info("Loading tokenizer from %s", base_model_path)
        self.tokenizer = AutoTokenizer.from_pretrained(
            base_model_path, trust_remote_code=True
        )

        logger.info("Loading base model from %s", base_model_path)
        base = AutoModelForCausalLM.from_pretrained(
            base_model_path,
            torch_dtype       = torch.bfloat16,
            device_map        = "auto",
            trust_remote_code = True,
        )

        if adapter_path:
            logger.info("Loading LoRA adapter from %s", adapter_path)
            base = PeftModel.from_pretrained(base, adapter_path)
            base = base.merge_and_unload()
            logger.info("Adapter merged and unloaded.")

        self._pipe = pipeline(
            "text-generation",
            model       = base,
            tokenizer   = self.tokenizer,
            max_new_tokens   = max_new_tokens,
            temperature      = temperature,
            do_sample        = temperature > 0,
            return_full_text = False,
        )

    def __call__(self, prompt: str, **kwargs) -> str:
        result = self._pipe(prompt, **kwargs)
        if result and isinstance(result, list):
            return result[0].get("generated_text", "")
        return ""


# ---------------------------------------------------------------------------
# Main Evaluator
# ---------------------------------------------------------------------------

class FinetunedModelEvaluator:
    """
    Runs the 31-benchmark gauntlet against up to 4 model configurations.

    Parameters
    ----------
    adapter_path  : path to fine-tuned LoRA adapter directory
    base_model    : HuggingFace model id or local path of base model
    out_dir       : directory to write scorecard and JSON results
    use_stub      : force stub LLM (for CI / no-GPU environments)
    max_new_tokens: generation length cap per benchmark
    temperature   : generation temperature
    """

    def __init__(
        self,
        adapter_path: Optional[str]  = None,
        base_model:   str            = "Qwen/Qwen2.5-Coder-32B-Instruct",
        out_dir:      str            = "data/finetune/eval_results",
        use_stub:     bool           = False,
        max_new_tokens: int          = 4096,
        temperature:  float          = 0.1,
    ):
        self.adapter_path   = adapter_path
        self.base_model     = base_model
        self.out_dir        = pathlib.Path(out_dir)
        self.use_stub       = use_stub or not _INFERENCE_AVAILABLE
        self.max_new_tokens = max_new_tokens
        self.temperature    = temperature
        self.retriever      = HybridRetriever()
        self.augmenter      = PromptAugmenter(self.retriever)

    def _make_llm(self, with_adapter: bool) -> Any:
        if self.use_stub:
            return _StubLLM()
        return _HFAdapterLLM(
            base_model_path = self.base_model,
            adapter_path    = self.adapter_path if with_adapter else None,
            max_new_tokens  = self.max_new_tokens,
            temperature     = self.temperature,
        )

    def _augment_prompt(self, prompt: str) -> str:
        docs = self.retriever.retrieve(prompt, top_k=3)
        return self.augmenter.build_prompt(prompt, docs)

    def run(self) -> Dict[str, Any]:
        """Execute all benchmark configurations and write results."""
        self.out_dir.mkdir(parents=True, exist_ok=True)
        metrics_calc = MetricsCalculator()
        benchmarks   = BENCHMARK_CATALOG

        results: Dict[str, Any] = {}
        configs = {
            "BASE":           {"adapter": False, "rag": False},
            "BASE_RAG":       {"adapter": False, "rag": True},
            "FINETUNED":      {"adapter": True,  "rag": False},
            "FINETUNED_RAG":  {"adapter": True,  "rag": True},
        }

        for cfg_name, opts in configs.items():
            if opts["adapter"] and not self.adapter_path:
                logger.info("Skipping %s — no adapter path provided.", cfg_name)
                continue

            logger.info("Evaluating configuration: %s", cfg_name)
            llm      = self._make_llm(with_adapter=opts["adapter"])
            cfg_results: List[Dict[str, Any]] = []

            for bm in benchmarks:
                prompt = bm.prompt
                if opts["rag"]:
                    prompt = self._augment_prompt(prompt)

                try:
                    generated = llm(prompt)
                except Exception as exc:
                    logger.warning("Generation failed for %s/%s: %s", cfg_name, bm.id, exc)
                    generated = ""

                metrics = metrics_calc.calculate(generated, bm)
                cfg_results.append({
                    "benchmark_id":  bm.id,
                    "sector":        bm.sector,
                    "prompt_tokens": len(prompt.split()),
                    "output_chars":  len(generated),
                    "metrics":       metrics,
                })

            # Aggregate
            if cfg_results:
                agg = self._aggregate(cfg_results)
                results[cfg_name] = {"per_benchmark": cfg_results, "aggregate": agg}

        # Write outputs
        timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S")
        json_path = self.out_dir / f"eval_{timestamp}.json"
        md_path   = self.out_dir / f"eval_{timestamp}.md"

        with open(json_path, "w", encoding="utf-8") as fh:
            json.dump(results, fh, indent=2, ensure_ascii=False)

        with open(md_path, "w", encoding="utf-8") as fh:
            fh.write(self._render_markdown(results, timestamp))

        logger.info("Evaluation results written to: %s", self.out_dir)
        return results

    def _aggregate(self, per_bm: List[Dict]) -> Dict[str, float]:
        """Compute mean metrics across all benchmarks."""
        keys = set()
        for r in per_bm:
            keys.update(r["metrics"].keys())
        agg: Dict[str, float] = {}
        for k in keys:
            vals = [r["metrics"][k] for r in per_bm if k in r["metrics"]]
            agg[k] = round(sum(vals) / len(vals), 4) if vals else 0.0
        return agg

    def _render_markdown(self, results: Dict, timestamp: str) -> str:
        """Render a comparative scorecard markdown table."""
        lines = [
            f"# PLC LLM Evaluation Scorecard — {timestamp}",
            "",
            f"**Base model**: `{self.base_model}`",
            f"**Adapter**: `{self.adapter_path or 'N/A'}`",
            f"**Benchmarks**: {len(BENCHMARK_CATALOG)} items across 6 sectors",
            "",
            "## Aggregate Scores",
            "",
            "| Configuration | IEC-PR | DCA | HR | VDCS | ESCS | Composite |",
            "|:---|---:|---:|---:|---:|---:|---:|",
        ]

        for cfg_name, data in results.items():
            agg = data.get("aggregate", {})
            lines.append(
                f"| {cfg_name} "
                f"| {agg.get('iec_pr', 0):.3f} "
                f"| {agg.get('dca', 0):.3f} "
                f"| {agg.get('hr', 0):.3f} "
                f"| {agg.get('vdcs', 0):.3f} "
                f"| {agg.get('escs', 0):.3f} "
                f"| {agg.get('composite', 0):.3f} |"
            )

        lines += [
            "",
            "## Metric Definitions",
            "",
            "| Metric | Description |",
            "|:---|:---|",
            "| IEC-PR | IEC 61131-3 Parity Rate — structural syntax correctness |",
            "| DCA | Declared to Called Accuracy — variable completeness |",
            "| HR | Hazard Rate inverse — safety clause coverage |",
            "| VDCS | Vendor Dialect Conformance Score |",
            "| ESCS | Emergency Stop Cutoff Score — Z3 SMT safety proof |",
            "| Composite | 0.30×IEC-PR + 0.20×DCA + 0.20×HR + 0.15×VDCS + 0.15×ESCS |",
        ]

        return "\n".join(lines)


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO, format="%(asctime)s  %(levelname)s  %(message)s")
    parser = argparse.ArgumentParser(description="Evaluate fine-tuned PLC LLM on 31-benchmark gauntlet")
    parser.add_argument("--adapter",        default=None,                       help="LoRA adapter path")
    parser.add_argument("--base",           default="Qwen/Qwen2.5-Coder-32B-Instruct", help="Base model")
    parser.add_argument("--out-dir",        default="data/finetune/eval_results", help="Output directory")
    parser.add_argument("--stub",           action="store_true",                help="Force stub LLM (no GPU)")
    parser.add_argument("--max-new-tokens", type=int, default=4096)
    parser.add_argument("--temperature",    type=float, default=0.1)
    args = parser.parse_args()

    evaluator = FinetunedModelEvaluator(
        adapter_path   = args.adapter,
        base_model     = args.base,
        out_dir        = args.out_dir,
        use_stub       = args.stub,
        max_new_tokens = args.max_new_tokens,
        temperature    = args.temperature,
    )
    results = evaluator.run()
    print(json.dumps({k: v["aggregate"] for k, v in results.items()}, indent=2))
