"""
plc_platform.api
================
FastAPI REST interface for the Industrial PLC LLM Platform.

Endpoints:
    POST /generate        — Full 5-agent assembly-line pipeline execution
    POST /audit           — Static analysis only (StaticAnalysisAuditor)
    POST /verify          — SMT formal verification only
    POST /quality         — Dataset quality gate evaluation
    GET  /benchmarks      — Run 31-benchmark suite (or subset)
    GET  /health          — Health check
    GET  /dialects        — List supported PLC dialects
    POST /translate       — Cross-dialect code translation
    GET  /standards       — List RAG knowledge-base documents

The API is intentionally stateless — no live PLC connections.
Every endpoint returns JSON.

Usage:
    pip install fastapi uvicorn
    uvicorn plc_platform.api.app:app --host 0.0.0.0 --port 8080 --reload

Or via CLI:
    python -m plc_platform.api.app
"""

from plc_platform.api.app import app, create_app

__all__ = ["app", "create_app"]
