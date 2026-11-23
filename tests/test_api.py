"""
tests/test_api.py
=================
Unit tests for FastAPI endpoints in plc_platform/api/app.py.
Uses Starlette TestClient (from fastapi).
"""

import pytest

try:
    from fastapi.testclient import TestClient
    from plc_platform.api.app import app
    _TESTCLIENT_AVAILABLE = True
except ImportError:
    _TESTCLIENT_AVAILABLE = False


@pytest.mark.skipif(not _TESTCLIENT_AVAILABLE, reason="FastAPI TestClient not available")
class TestApiEndpoints:

    @pytest.fixture(autouse=True)
    def setup_client(self):
        self.client = TestClient(app)

    def test_health_endpoint(self):
        resp = self.client.get("/health")
        assert resp.status_code == 200
        data = resp.json()
        assert data["status"] == "ok"
        assert "Industrial PLC LLM Platform" in data["service"]

    def test_dialects_endpoint(self):
        resp = self.client.get("/dialects")
        assert resp.status_code == 200
        data = resp.json()
        assert "dialects" in data
        ids = [d["id"] for d in data["dialects"]]
        assert "ST" in ids
        assert "CODESYS" in ids
        assert "SFC" in ids
        assert "L5X" in ids

    def test_standards_endpoint(self):
        resp = self.client.get("/standards")
        assert resp.status_code == 200
        data = resp.json()
        assert data["document_count"] > 0
        assert len(data["documents"]) > 0

    def test_audit_endpoint(self):
        code = (
            "FUNCTION_BLOCK FB_TestAudit\n"
            "VAR_INPUT\n"
            "    b_Start : BOOL; (* [ms] test *)\n"
            "    b_Stop  : BOOL; (* [bar] test *)\n"
            "    bEStop  : BOOL; (* [rpm] test *)\n"
            "    rVal1   : REAL; (* [°C] test *)\n"
            "    rVal2   : REAL; (* [%] test *)\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    b_Run : BOOL;\n"
            "END_VAR\n"
            "IF bEStop THEN\n"
            "    b_Run := FALSE;\n"
            "    RETURN;\n"
            "END_IF;\n"
            "IF b_Start AND NOT b_Stop THEN\n"
            "    b_Run := TRUE;\n"
            "END_IF;\n"
            "END_FUNCTION_BLOCK\n"
        )
        resp = self.client.post("/audit", json={"code": code})
        assert resp.status_code == 200
        data = resp.json()
        assert "is_approved" in data
        assert "defects" in data

    def test_quality_endpoint(self):
        code = (
            "FUNCTION_BLOCK FB_QTest\n"
            "VAR_INPUT\n"
            "    bEStop : BOOL; (* [bar] *)\n"
            "    rP : REAL; (* [ms] *)\n"
            "    rQ : REAL; (* [kN] *)\n"
            "    rR : REAL; (* [°C] *)\n"
            "    rS : REAL; (* [%] *)\n"
            "END_VAR\n"
            "VAR_OUTPUT\n"
            "    bFault : BOOL;\n"
            "END_VAR\n"
            "VAR\n"
            "    bTrip_A : BOOL;\n"
            "    bTrip_B : BOOL;\n"
            "    bTrip_C : BOOL;\n"
            "    bVoted  : BOOL;\n"
            "    bAlarm_HH : BOOL;\n"
            "    bAlarm_LL : BOOL;\n"
            "    rMPC_Cost : REAL;\n"
            "    rStateX0 : REAL;\n"
            "    eState : INT;\n"
            "END_VAR\n"
            "IF bEStop THEN bFault := TRUE; RETURN; END_IF;\n"
            "bTrip_A := rP > 10.0; bTrip_B := rP > 10.0; bTrip_C := rP > 10.0;\n"
            "bVoted := (bTrip_A AND bTrip_B) OR (bTrip_B AND bTrip_C) OR (bTrip_A AND bTrip_C);\n"
            "rStateX0 := 0.98 * rStateX0;\n"
            "rMPC_Cost := 10.0 * rStateX0 * rStateX0;\n"
            "bAlarm_HH := rP > 90.0;\n"
            "bAlarm_LL := rP < 10.0;\n"
            "CASE eState OF 0: eState := 1; END_CASE;\n"
            "END_FUNCTION_BLOCK\n"
        )
        resp = self.client.post("/quality", json={"code": code, "threshold": 65.0})
        assert resp.status_code == 200
        data = resp.json()
        assert "total_score" in data
        assert "admitted" in data
        assert data["admitted"] is True

    def test_benchmarks_endpoint(self):
        resp = self.client.get("/benchmarks?limit=2")
        assert resp.status_code == 200
        data = resp.json()
        assert data["benchmarks_run"] == 2
        assert "aggregate" in data
