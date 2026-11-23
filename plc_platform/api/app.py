"""
app.py
======
FastAPI application for the Industrial PLC LLM Platform.

All heavy pipeline imports are deferred inside route handlers so the
app module can be imported in environments without all dependencies installed
(e.g. CI for schema-only tests).
"""

from __future__ import annotations

import logging
import time
import uuid
from typing import Any, Dict, List, Optional

logger = logging.getLogger(__name__)

# ---------------------------------------------------------------------------
# FastAPI (optional dependency — guarded)
# ---------------------------------------------------------------------------
_FASTAPI_AVAILABLE = False
try:
    from fastapi import FastAPI, HTTPException, Query
    from fastapi.responses import JSONResponse
    from pydantic import BaseModel, Field
    _FASTAPI_AVAILABLE = True
except ImportError:
    # Provide stubs for environments without FastAPI
    class BaseModel:  # type: ignore
        pass
    def Field(*a, **kw):  # type: ignore
        return None
    class FastAPI:  # type: ignore
        def get(self, *a, **kw):
            def _d(f): return f
            return _d
        def post(self, *a, **kw):
            def _d(f): return f
            return _d


# ---------------------------------------------------------------------------
# Request / Response models
# ---------------------------------------------------------------------------

class GenerateRequest(BaseModel):
    """Request body for POST /generate"""
    prompt:         str                     = Field(..., description="Natural-language manufacturing automation requirement")
    vendor:         Optional[str]           = Field(None, description="Target PLC vendor: SIEMENS | ROCKWELL | BECKHOFF | CODESYS | GENERIC")
    sector:         Optional[str]           = Field(None, description="Manufacturing sector: AUTOMOTIVE | ELECTRONICS | HEAVY_MACHINERY | PLASTICS | FOOD_BEVERAGE | STEEL")
    dialect:        Optional[str]           = Field(None, description="Output dialect: ST | SCL | L5X | TWINCAT | CODESYS | SFC")
    max_repair_iterations: int              = Field(3, ge=1, le=5, description="Max self-repair loops")
    use_rag:        bool                    = Field(True, description="Augment with standards RAG context")


class AuditRequest(BaseModel):
    """Request body for POST /audit"""
    code:           str                     = Field(..., description="IEC 61131-3 Structured Text source code")
    vendor:         Optional[str]           = Field(None)


class VerifyRequest(BaseModel):
    """Request body for POST /verify"""
    code:           str                     = Field(..., description="IEC 61131-3 Structured Text source code")


class QualityRequest(BaseModel):
    """Request body for POST /quality"""
    code:           str                     = Field(..., description="IEC 61131-3 Structured Text source code")
    sector:         Optional[str]           = Field(None)
    threshold:      float                   = Field(85.0, ge=0.0, le=100.0)


class TranslateRequest(BaseModel):
    """Request body for POST /translate"""
    code:           str                     = Field(..., description="Source IEC-ST code")
    source_dialect: str                     = Field(..., description="Source dialect: ST | SCL | L5X | TWINCAT | CODESYS | SFC")
    target_dialect: str                     = Field(..., description="Target dialect: ST | SCL | L5X | TWINCAT | CODESYS | SFC")


# ---------------------------------------------------------------------------
# App factory
# ---------------------------------------------------------------------------

def create_app() -> "FastAPI":
    if not _FASTAPI_AVAILABLE:
        raise ImportError(
            "FastAPI not installed. Run: pip install fastapi uvicorn"
        )

    app = FastAPI(
        title       = "Industrial PLC LLM Platform API",
        description = (
            "REST interface for AI-powered IEC 61131-3 PLC code generation, "
            "debugging, auditing, and formal verification for manufacturing automation."
        ),
        version     = "1.0.0",
        docs_url    = "/docs",
        redoc_url   = "/redoc",
    )

    # ------------------------------------------------------------------
    # Health check
    # ------------------------------------------------------------------

    @app.get("/health", tags=["System"])
    def health() -> Dict[str, Any]:
        """Service liveness check."""
        return {
            "status":    "ok",
            "service":   "Industrial PLC LLM Platform",
            "version":   "1.0.0",
            "timestamp": time.time(),
        }

    # ------------------------------------------------------------------
    # Dialects info
    # ------------------------------------------------------------------

    @app.get("/dialects", tags=["Info"])
    def list_dialects() -> Dict[str, Any]:
        """List all supported PLC programming dialects."""
        return {
            "dialects": [
                {"id": "ST",      "name": "IEC 61131-3 Structured Text",         "vendors": ["All"]},
                {"id": "SCL",     "name": "Siemens TIA Portal SCL",               "vendors": ["Siemens"]},
                {"id": "L5X",     "name": "Rockwell Studio 5000 .L5X XML",        "vendors": ["Rockwell", "Allen-Bradley"]},
                {"id": "TWINCAT", "name": "Beckhoff TwinCAT 3 .TcPOU",            "vendors": ["Beckhoff"]},
                {"id": "CODESYS", "name": "CODESYS V3 (OOP ST extensions)",       "vendors": ["CODESYS", "Festo", "Bosch Rexroth", "Wago", "Lenze", "Pilz", "Schneider EML"]},
                {"id": "SFC",     "name": "Sequential Function Chart (textual ST)","vendors": ["All"]},
                {"id": "RLL",     "name": "Relay Ladder Logic (ASCII)",           "vendors": ["Rockwell", "Generic"]},
            ]
        }

    # ------------------------------------------------------------------
    # Standards / RAG knowledge base
    # ------------------------------------------------------------------

    @app.get("/standards", tags=["Info"])
    def list_standards() -> Dict[str, Any]:
        """List documents in the RAG standards knowledge base."""
        from plc_platform.rag.standards_kb import KNOWLEDGE_BASE
        return {
            "document_count": len(KNOWLEDGE_BASE),
            "documents": [
                {
                    "id":       doc.doc_id,
                    "title":    doc.title,
                    "standard": doc.standard,
                    "sector":   doc.sector,
                    "vendor":   doc.vendor,
                    "tokens":   len(doc.content.split()),
                }
                for doc in KNOWLEDGE_BASE
            ],
        }

    # ------------------------------------------------------------------
    # POST /generate — Full 5-agent pipeline
    # ------------------------------------------------------------------

    @app.post("/generate", tags=["Generation"])
    def generate(req: GenerateRequest) -> Dict[str, Any]:
        """
        Run the full 5-agent assembly-line pipeline:
        RequirementsEngineer → ControlArchitect → CodeGenerator →
        StaticAuditor → SMTVerifier

        Returns generated code, audit report, and pipeline metadata.
        """
        from plc_platform.agents.orchestrator import IndustrialEngineeringOrchestrator
        from plc_platform.rag.retriever import HybridRetriever
        from plc_platform.rag.prompt_augmenter import PromptAugmenter

        request_id = str(uuid.uuid4())
        t0         = time.time()

        try:
            orchestrator = IndustrialEngineeringOrchestrator(
                vendor   = req.vendor or "GENERIC",
                sector   = req.sector or "GENERAL_MANUFACTURING",
                dialect  = req.dialect or "ST",
                use_rag  = req.use_rag,
            )
            result = orchestrator.run(
                prompt                 = req.prompt,
                max_repair_iterations  = req.max_repair_iterations,
            )
        except Exception as exc:
            logger.exception("Generation pipeline error for request %s", request_id)
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "request_id":   request_id,
            "elapsed_ms":   round((time.time() - t0) * 1000, 1),
            "status":       result.get("status", "UNKNOWN"),
            "code":         result.get("code", ""),
            "audit_report": result.get("audit_report", {}),
            "smt_result":   result.get("smt_result", {}),
            "repair_count": result.get("repair_iterations", 0),
            "rag_docs_used":result.get("rag_docs_used", []),
        }

    # ------------------------------------------------------------------
    # POST /audit — Static analysis only
    # ------------------------------------------------------------------

    @app.post("/audit", tags=["Analysis"])
    def audit(req: AuditRequest) -> Dict[str, Any]:
        """
        Run StaticAnalysisAuditor on provided IEC-ST code.
        Returns parity check results, variable completeness, and defect list.
        Does NOT run SMT verification (use /verify for that).
        """
        from plc_platform.agents.static_auditor import StaticAnalysisAuditor

        request_id = str(uuid.uuid4())
        t0         = time.time()

        try:
            auditor = StaticAnalysisAuditor(vendor=req.vendor or "GENERIC")
            report  = auditor.audit_code_text(req.code)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "request_id":   request_id,
            "elapsed_ms":   round((time.time() - t0) * 1000, 1),
            "is_approved":  report.is_approved,
            "defect_count": len(report.defects),
            "defects":      report.defect_descriptions,
            "parity_ok":    report.parity_ok if hasattr(report, "parity_ok") else None,
        }

    # ------------------------------------------------------------------
    # POST /verify — SMT formal verification
    # ------------------------------------------------------------------

    @app.post("/verify", tags=["Analysis"])
    def verify(req: VerifyRequest) -> Dict[str, Any]:
        """
        Run Z3-based SMT formal verification on provided IEC-ST code.
        Proves safety invariants: E-Stop cutoff, 2oo3 TMR, output bounds.
        """
        from plc_platform.agents.smt_verifier import SMTVerificationTester

        request_id = str(uuid.uuid4())
        t0         = time.time()

        try:
            verifier = SMTVerificationTester()
            result   = verifier.verify_code_text(req.code)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "request_id":    request_id,
            "elapsed_ms":    round((time.time() - t0) * 1000, 1),
            "certified_safe":result.get("certified_safe", False),
            "proof_status":  result.get("proof_status", "UNKNOWN"),
            "invariants":    result.get("invariants", {}),
        }

    # ------------------------------------------------------------------
    # POST /quality — Dataset quality gate
    # ------------------------------------------------------------------

    @app.post("/quality", tags=["Dataset"])
    def quality(req: QualityRequest) -> Dict[str, Any]:
        """
        Evaluate IEC-ST code through the dataset quality gate.
        Returns a 6-dimension score and admission decision.
        """
        from plc_platform.datasets.quality_gate import DatasetQualityGate

        request_id = str(uuid.uuid4())
        t0         = time.time()

        try:
            gate   = DatasetQualityGate(threshold=req.threshold)
            result = gate.evaluate(req.code, sector_hint=req.sector)
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "request_id": request_id,
            "elapsed_ms": round((time.time() - t0) * 1000, 1),
            **result.to_dict(),
        }

    # ------------------------------------------------------------------
    # GET /benchmarks — 31-benchmark evaluation suite
    # ------------------------------------------------------------------

    @app.get("/benchmarks", tags=["Evaluation"])
    def run_benchmarks(
        sector: Optional[str] = Query(None, description="Filter by sector"),
        limit:  int           = Query(5,    ge=1, le=31, description="Number of benchmarks to run (stub mode)"),
    ) -> Dict[str, Any]:
        """
        Run the 31-benchmark gauntlet (or a filtered subset) using stub LLM.
        Returns per-benchmark metrics and aggregate scores.
        """
        from plc_platform.evaluate.benchmarks import BENCHMARK_CATALOG
        from plc_platform.evaluate.metrics import MetricsCalculator
        from plc_platform.finetune.evaluate_finetuned import _StubLLM

        request_id = str(uuid.uuid4())
        t0         = time.time()

        benchmarks = BENCHMARK_CATALOG
        if sector:
            benchmarks = [b for b in benchmarks if b.sector.upper() == sector.upper()]
        benchmarks = benchmarks[:limit]

        llm     = _StubLLM()
        calc    = MetricsCalculator()
        results = []

        for bm in benchmarks:
            try:
                generated = llm(bm.prompt)
                metrics   = calc.calculate(generated, bm)
            except Exception as exc:
                metrics = {"error": str(exc)}
            results.append({
                "id":      bm.id,
                "sector":  bm.sector,
                "metrics": metrics,
            })

        # Aggregate
        agg: Dict[str, List[float]] = {}
        for r in results:
            for k, v in r["metrics"].items():
                if isinstance(v, (int, float)):
                    agg.setdefault(k, []).append(float(v))
        mean_agg = {k: round(sum(v) / len(v), 4) for k, v in agg.items()}

        return {
            "request_id":    request_id,
            "elapsed_ms":    round((time.time() - t0) * 1000, 1),
            "benchmarks_run":len(results),
            "aggregate":     mean_agg,
            "per_benchmark": results,
        }

    # ------------------------------------------------------------------
    # POST /translate — Cross-dialect translation
    # ------------------------------------------------------------------

    @app.post("/translate", tags=["Generation"])
    def translate(req: TranslateRequest) -> Dict[str, Any]:
        """
        Translate PLC code between supported dialects.
        Current support: ST → SCL, ST → CODESYS, RLL → ST.
        """
        request_id = str(uuid.uuid4())
        t0         = time.time()

        src = req.source_dialect.upper()
        tgt = req.target_dialect.upper()

        try:
            if src == "RLL" and tgt == "ST":
                from plc_platform.dialects.ladder_diagram import LadderCompiler
                compiler = LadderCompiler()
                translated = compiler.rll_to_st(req.code)
            elif src == "ST" and tgt == "SCL":
                # Minimal: SCL is nearly identical to IEC ST — add Siemens header
                translated = (
                    "// Siemens TIA Portal SCL — auto-translated\n"
                    "// Verify vendor-specific types (S5Time, Word, etc.) before deployment\n\n"
                ) + req.code
            elif src == "ST" and tgt == "CODESYS":
                translated = (
                    "{attribute 'qualified_only'}\n"
                    "{attribute 'monitoring' := 'call'}\n"
                    "// CODESYS V3 — auto-translated from plain IEC ST\n\n"
                ) + req.code
            else:
                raise HTTPException(
                    status_code=400,
                    detail=f"Translation {src} → {tgt} is not yet implemented. "
                           f"Supported: RLL→ST, ST→SCL, ST→CODESYS",
                )
        except HTTPException:
            raise
        except Exception as exc:
            raise HTTPException(status_code=500, detail=str(exc))

        return {
            "request_id":    request_id,
            "elapsed_ms":    round((time.time() - t0) * 1000, 1),
            "source_dialect":src,
            "target_dialect":tgt,
            "translated_code":translated,
            "char_count":    len(translated),
        }

    return app


# ---------------------------------------------------------------------------
# Default app instance
# ---------------------------------------------------------------------------

try:
    app = create_app()
except ImportError:
    app = None   # type: ignore  # FastAPI not available


# ---------------------------------------------------------------------------
# CLI launcher
# ---------------------------------------------------------------------------

if __name__ == "__main__":
    import sys
    if not _FASTAPI_AVAILABLE:
        print("FastAPI not installed. Run: pip install fastapi uvicorn")
        sys.exit(1)
    try:
        import uvicorn
    except ImportError:
        print("uvicorn not installed. Run: pip install uvicorn")
        sys.exit(1)

    uvicorn.run(
        "plc_platform.api.app:app",
        host    = "0.0.0.0",
        port    = 8080,
        reload  = True,
        log_level = "info",
    )
