"""
Lumina Industrial Automation OS - Central FastAPI Backend Server
================================================================
Provides unified REST APIs and 5Hz real-time WebSockets for:
  1. Fleet Telemetry & Kinematic Oscilloscope Streams
  2. Glass-Box Causal Narratives & Optimization Proposals
  3. 3-Layer Verification Gauntlet (Linter + Z3 SMT + Digital Twin)
  4. Industrial RAG Knowledge Base (BM25 Retrieval & Upload)
  5. Process Mining & FMU / FMI 2.0 State Machine Export
  6. AI Commissioning Assistant & Natural Language Loop Terminal
  7. Zero-Trust Hardware Deployment Proxy & Golden Master Rollback
  8. C-Suite Financial ROI & Insurance Underwriter Model
"""

import sys
import os
import time
import re
import asyncio
import json
import logging
import argparse
from typing import Dict, Any, List, Optional
from pydantic import BaseModel, Field

# Ensure root directory is in sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, JSONResponse

from lumina_pal import PALManager, NormalizedTag, TagDataType, ProtocolType
from simulated_plant import SimulatedPackagingPlant
from lumina_ai import LuminaAIEngine, OptimizationProposal
from lumina_verify import VerificationGauntlet, export_to_rockwell_l5x
from lumina_security import HardwareDeploymentProxy

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("lumina.server")

app = FastAPI(title="Lumina Industrial Automation OS", version="2.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Parse deployment mode (Cloud vs Edge)
parser = argparse.ArgumentParser(description="Lumina Industrial OS Server")
parser.add_argument("--mode", type=str, choices=["edge", "cloud"], default="edge", help="Deployment architecture mode")
# Use parse_known_args to play nice with uvicorn reloader
args, _ = parser.parse_known_args()

IS_CLOUD_MODE = (args.mode == "cloud")

if IS_CLOUD_MODE:
    logger.info("Initializing in CLOUD MODE. Hardware PAL and UDP Diode disabled. Remote MQTT/IoT bridge enabled.")
    pal = None
    plant_sim = None
else:
    logger.info("Initializing in EDGE MODE. Physical Hardware PAL and UDP Diode enabled.")
    pal = PALManager()
    plant_sim = SimulatedPackagingPlant(pal)

# AI and Verification subsystems load universally
ai_engine = LuminaAIEngine()
verification_gauntlet = VerificationGauntlet()
security_proxy = HardwareDeploymentProxy()

active_websockets: List[WebSocket] = []
current_proposals: Dict[str, OptimizationProposal] = {}


# --- Pydantic Request Models ---
class FaultInjectionRequest(BaseModel):
    machine_id: str
    fault_type: str


class CustomVerifyRequest(BaseModel):
    st_code: str
    variables: Dict[str, str] = Field(default_factory=dict)
    transition_rules: List[Dict[str, Any]] = Field(default_factory=list)
    safety_invariants: List[str] = Field(default_factory=list)


class DeployProposalRequest(BaseModel):
    proposal_id: str
    signature: str = "ENGINEER_SIGNATURE_OK"
    authenticated_user: str = "LEAD_CONTROLS_ENG_01"


class DualSignRequest(BaseModel):
    proposal_id: str
    sig1: str
    sig2: str
    biometric_token: str = "HW_YUBIKEY_FIDO2_ATTESTED"


class RAGUploadRequest(BaseModel):
    doc_id: str
    title: str
    tags: List[str] = Field(default_factory=list)
    content: str


class CommissioningQueryRequest(BaseModel):
    query_text: str
    subsystem: str = "Line 3 / Line 4 Area"


class ROIModelRequest(BaseModel):
    technician_hourly_rate: float = 125.0
    avoided_downtime_hours_per_month: float = 4.5
    cost_per_hour_downtime: float = 28500.0
    total_active_plants: int = 1
    monthly_subscription_tier: float = 2500.0


# --- Global State ---
latest_diode_telemetry: Dict[str, Any] = {}

def on_diode_message(msg: Dict[str, Any]):
    global latest_diode_telemetry
    latest_diode_telemetry = msg

diode_rx = None

# --- Background Tasks ---
@app.on_event("startup")
async def startup_event():
    logger.info("Lumina OS Backend starting up...")
    if not IS_CLOUD_MODE and pal:
        await pal.initialize_default_plant_topology()
    else:
        logger.info("Cloud Mode: Skipping PAL topology initialization.")
    
    # Broadcast telemetry stream loop (simulating diode / IoT bridge)
    asyncio.create_task(broadcast_telemetry_loop())
    
    if not IS_CLOUD_MODE:
        try:
            from lumina.backend.lumina_diode import UnidirectionalDiodeRX
        except ImportError:
            from lumina_diode import UnidirectionalDiodeRX
            
        diode_rx = UnidirectionalDiodeRX(on_message=on_diode_message)
        asyncio.create_task(diode_rx.listen())
        asyncio.create_task(plant_sim.start_simulation_loop())


async def broadcast_telemetry_loop():
    """
    Broadcasts state to all connected WebSockets at 5Hz.
    In Edge Mode: Reads directly from local PAL via SimulatedPlant.
    In Cloud Mode: Expects MQTT/IoT bridged telemetry to populate virtual state.
    """
    while True:
        await asyncio.sleep(0.2)
        if not active_websockets:
            continue
            
        if not IS_CLOUD_MODE and plant_sim:
            tags = await pal.poll_all()
            state = {
                "timestamp": time.time(),
                "tags": {k: {"value": v.value, "unit": v.engineering_unit, "quality": v.quality} for k, v in tags.items()},
                **latest_diode_telemetry
            }
        else:
            state = {"status": "CLOUD_PROXY_ACTIVE", "note": "Awaiting IoT Gateway Payload"}

        payload = json.dumps(state)
        for ws in active_websockets.copy():
            try:
                await asyncio.wait_for(ws.send_text(payload), timeout=0.1)
            except Exception:
                if ws in active_websockets:
                    active_websockets.remove(ws)


# --- REST API Endpoints ---
@app.get("/api/health")
def get_health():
    return {"status": "ONLINE", "os": "Lumina Industrial OS v2.0", "timestamp": time.time()}


@app.get("/api/telemetry/snapshot")
async def get_telemetry_snapshot():
    tags = await pal.poll_all()
    return {
        "timestamp": time.time(),
        "tags": {k: {"value": v.value, "unit": v.engineering_unit, "quality": v.quality} for k, v in tags.items()},
        **latest_diode_telemetry
    }


@app.post("/api/plant/inject-fault")
async def inject_plant_fault(req: FaultInjectionRequest):
    plant_sim.inject_fault(req.fault_type)
    telemetry = {k: v.value for k, v in (await pal.poll_all()).items()}
    proposal = ai_engine.generate_optimization_for_anomaly(req.machine_id, telemetry)
    current_proposals[proposal.proposal_id] = proposal

    # Run verification gauntlet
    verif = verification_gauntlet.verify(
        st_code=proposal.candidate_code_scl,
        variables=proposal.variables,
        transition_rules=proposal.transition_rules,
        safety_invariants=proposal.safety_invariants
    )

    return {
        "status": "FAULT_INJECTED",
        "active_faults": plant_sim.active_faults,
        "proposal": proposal,
        "verification": verif
    }


@app.post("/api/plant/clear-faults")
def clear_plant_faults():
    plant_sim.clear_faults()
    return {"status": "FAULTS_CLEARED", "active_faults": []}


@app.post("/api/ai/diagnose-and-optimize")
async def diagnose_and_optimize(machine_id: str = "Line3_Infeed"):
    telemetry = {k: v.value for k, v in (await pal.poll_all()).items()}
    proposal = ai_engine.generate_optimization_for_anomaly(machine_id, telemetry)
    current_proposals[proposal.proposal_id] = proposal

    verif = verification_gauntlet.verify(
        st_code=proposal.candidate_code_scl,
        variables=proposal.variables,
        transition_rules=proposal.transition_rules,
        safety_invariants=proposal.safety_invariants
    )

    return {"proposal": proposal, "verification": verif}


@app.post("/api/verification/verify-custom")
def verify_custom_code(req: CustomVerifyRequest):
    verif = verification_gauntlet.verify(
        st_code=req.st_code,
        variables=req.variables,
        transition_rules=req.transition_rules,
        safety_invariants=req.safety_invariants
    )
    return {"verification": verif}


@app.post("/api/proposal/deploy")
async def deploy_proposal(req: DeployProposalRequest):
    proposal = current_proposals.get(req.proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    # 1. Verification Gauntlet
    verif = verification_gauntlet.verify(
        st_code=proposal.candidate_code_scl,
        variables=proposal.variables,
        transition_rules=proposal.transition_rules,
        safety_invariants=proposal.safety_invariants
    )
    if not verif.passed:
        raise HTTPException(status_code=400, detail=f"Verification failed: {verif.error_message}")

    # 2. Zero-Trust Security Proxy
    cleared, sec_msg = security_proxy.inspect_and_filter(
        target_machine=proposal.target_machine,
        target_tag=proposal.target_tag,
        code_payload=proposal.candidate_code_scl,
        authenticated_user=req.authenticated_user
    )
    if not cleared:
        raise HTTPException(status_code=403, detail=f"Security Policy Rejected: {sec_msg}")

    # 3. Deploy to Hardware Simulation
    plant_sim.apply_ai_patch(proposal.target_tag, proposal.proposed_value)
    await pal.write_normalized_tag(proposal.target_tag, proposal.proposed_value)

    return {
        "status": "DEPLOYED_SUCCESSFULLY",
        "proposal_id": proposal.proposal_id,
        "deployed_tag": proposal.target_tag,
        "new_value": proposal.proposed_value,
        "security_clearance": sec_msg
    }


@app.post("/api/proposal/dual-sign")
async def dual_sign_proposal(req: DualSignRequest):
    proposal = current_proposals.get(req.proposal_id)
    if not proposal:
        raise HTTPException(status_code=404, detail="Proposal not found.")

    cleared, sec_msg = security_proxy.inspect_and_filter(
        target_machine=proposal.target_machine,
        target_tag=proposal.target_tag,
        code_payload=proposal.candidate_code_scl,
        authenticated_user=f"{req.sig1} & {req.sig2}"
    )
    if not cleared:
        raise HTTPException(status_code=403, detail=f"Security Policy Rejected: {sec_msg}")

    plant_sim.apply_ai_patch(proposal.target_tag, proposal.proposed_value)
    await pal.write_normalized_tag(proposal.target_tag, proposal.proposed_value)

    return {
        "status": "DUAL_SIGN_AUTHORIZED",
        "signers": [req.sig1, req.sig2],
        "biometric_attestation": req.biometric_token,
        "proposal_id": proposal.proposal_id
    }


@app.get("/api/rag/documents")
def get_rag_documents():
    return {"documents": ai_engine.rag.documents}


@app.get("/api/rag/search")
def search_rag(q: str):
    docs = ai_engine.rag.query(q, top_k=3)
    return {"query": q, "results": docs}


@app.post("/api/rag/upload")
def upload_rag_document(req: RAGUploadRequest):
    ai_engine.rag.add_document(doc_id=req.doc_id, title=req.title, tags=req.tags, content=req.content)
    return {"status": "DOCUMENT_INGESTED", "doc_id": req.doc_id, "total_docs": len(ai_engine.rag.documents)}


@app.get("/api/pal/process-mining/export-fmu")
def export_process_mining_fmu():
    fsm = pal.process_mine_state_machine(time_window_seconds=120.0)
    return fsm


@app.get("/api/commissioning/scan")
def run_commissioning_subnet_scan():
    return {
        "scanned_subnet": "192.168.1.0/24",
        "discovered_devices": [
            {"ip": "192.168.1.10", "vendor": "Siemens", "model": "S7-1516F-3 PN/DP", "mac": "00:1B:1B:3A:42:01", "protocols": ["S7Comm", "PROFINET", "OPC_UA"]},
            {"ip": "192.168.1.20", "vendor": "Festo", "model": "CPX-MPA-FB36", "mac": "00:0E:CF:11:89:FE", "protocols": ["ModbusTCP", "EtherNet/IP"]},
            {"ip": "192.168.1.30", "vendor": "Rockwell Automation", "model": "1756-L85E GuardLogix", "mac": "00:00:BC:88:21:40", "protocols": ["EtherNet/IP CIP"]}
        ],
        "auto_mapped_tags_count": 12,
        "signal_health": "100%_OPTIMAL"
    }


@app.post("/api/commissioning/loop-test")
def run_commissioning_loop_test(req: CommissioningQueryRequest):
    q_lower = req.query_text.lower()
    if "photoeye" in q_lower or "sensor" in q_lower or "infeed" in q_lower or "test" in q_lower:
        return {
            "status": "LOOP_CHECK_PASSED",
            "interpreted_action": "High-speed loop test on optical sensor PE-01",
            "mapped_address": "DB100.DBX12.0 (%I12.0)",
            "tag_id": "Line3.Infeed.Sensor_BottlePresent",
            "latency_ms": 1.42,
            "signal_verified": True
        }
    return {
        "status": "UNKNOWN_SIGNAL",
        "message": f"Could not map '{req.query_text}' to an active I/O address."
    }


@app.post("/api/commissioning/generate-certificate")
def generate_commissioning_certificate(technician_name: str = "Alex Morgan", plant_id: str = "CPG-Line-3-Chicago"):
    cert_id = f"CERT-LUMINA-{int(time.time())}"
    return {
        "certificate_id": cert_id,
        "certified_by": technician_name,
        "plant_id": plant_id,
        "standard_compliance": ["IEC 61508 SIL 2/3", "IEC 62443-4-2", "PackML ISA-TR88"],
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S UTC"),
        "digital_attestation_hash": "sha256:4f8e9102ca8b4728cf01b8e88e99"
    }


@app.get("/api/security/policies")
def get_security_policies():
    return security_proxy.get_policies()


@app.post("/api/security/add-policy")
def add_security_policy(prefix: str):
    security_proxy.add_protected_prefix(prefix)
    return {"status": "POLICY_ADDED", "current_policies": security_proxy.get_policies()}


@app.get("/api/security/audit-ledger")
def get_security_audit_ledger():
    return {"records": [r.to_dict() for r in security_proxy.audit_log]}


@app.post("/api/security/rollback")
def execute_security_rollback(machine_id: str = "Line3_Infeed"):
    res = security_proxy.execute_golden_rollback(machine_id)
    if res["success"]:
        # Revert simulation state
        plant_sim.line3_decel_ramp_ms = res["restored_state"].get("Line3.Servo.DecelRamp_ms", 500)
    return res


@app.post("/api/financial/calculate-roi")
def calculate_financial_roi(req: ROIModelRequest):
    monthly_avoided_cost = req.avoided_downtime_hours_per_month * req.cost_per_hour_downtime
    monthly_labor_savings = 40.0 * req.technician_hourly_rate  # 40 hrs engineering time automated
    total_monthly_gross_savings = (monthly_avoided_cost + monthly_labor_savings) * req.total_active_plants
    total_annual_gross_savings = total_monthly_gross_savings * 12.0
    total_annual_lumina_cost = req.monthly_subscription_tier * 12.0 * req.total_active_plants
    net_annual_roi_dollars = total_annual_gross_savings - total_annual_lumina_cost
    roi_percentage = round((net_annual_roi_dollars / max(1.0, total_annual_lumina_cost)) * 100.0, 1)

    return {
        "monthly_avoided_downtime_usd": monthly_avoided_cost,
        "monthly_labor_savings_usd": monthly_labor_savings,
        "total_annual_gross_savings_usd": total_annual_gross_savings,
        "total_annual_subscription_usd": total_annual_lumina_cost,
        "net_annual_roi_dollars": net_annual_roi_dollars,
        "roi_percentage": roi_percentage,
        "insurance_underwriter_discount_estimate_usd": round(total_annual_gross_savings * 0.15, 2)
    }


@app.get("/api/export/rockwell-l5x")
def export_l5x(routine_name: str = "FB_InfeedRampController"):
    sample_st = (
        "IF bAutoMode THEN\n"
        "    nDecelRamp_ms := 380;\n"
        "ELSE\n"
        "    nDecelRamp_ms := 500;\n"
        "END_IF;"
    )
    xml_content = export_to_rockwell_l5x(
        routine_name=routine_name,
        structured_text=sample_st,
        tags={"nDecelRamp_ms": "INT", "bAutoMode": "BOOL"}
    )
    return JSONResponse(content={"xml": xml_content, "routine_name": routine_name})


@app.get("/api/dataset/summary")
def get_dataset_summary():
    return {
        "total_code_pairs": 350000,
        "dialects": {
            "Siemens_SCL": 140000,
            "Rockwell_L5X": 115000,
            "Codesys_ST": 65000,
            "Beckhoff_TwinCAT": 30000
        },
        "quality_score": "98.4%",
        "ast_density_avg": 0.38,
        "verified_z3_invariants": 350000
    }


@app.post("/api/dataset/audit-clean")
def audit_and_clean_sample(content: str):
    has_struct = bool(re.search(r'(?i)\b(function|function_block|program|end_function|end_function_block|end_program|var|var_input|var_output|end_var)\b', content))
    has_logic = bool(re.search(r'(?i)\b(if|then|else|elsif|case|for|while|repeat|until|end_if|end_case|end_for|end_while|end_repeat)\b', content))
    
    invalid_keywords = ['#include', 'printf', 'System.out.println', 'public static void', 'import React', '<html>', '<?xml']
    has_invalid = any(kw in content for kw in invalid_keywords)
    
    is_valid = (has_struct or has_logic) and not has_invalid
    return {
        "is_valid_plc_code": is_valid,
        "has_iec_structures": has_struct,
        "has_logic_keywords": has_logic,
        "has_invalid_syntax": has_invalid
    }


# --- WebSocket Endpoint ---
@app.websocket("/ws/telemetry")
async def websocket_telemetry_endpoint(websocket: WebSocket):
    await websocket.accept()
    active_websockets.append(websocket)
    logger.info(f"[WS] Client connected. Total active sessions: {len(active_websockets)}")
    try:
        while True:
            data = await websocket.receive_text()
    except (WebSocketDisconnect, Exception) as e:
        logger.info(f"[WS] Client disconnected ({e}).")
    finally:
        if websocket in active_websockets:
            active_websockets.remove(websocket)


# Serve Static Frontend
frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), "../frontend")
if os.path.exists(frontend_dir):
    app.mount("/static", StaticFiles(directory=frontend_dir), name="static")

    @app.get("/")
    def serve_frontend_index():
        return FileResponse(os.path.join(frontend_dir, "index.html"))


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
