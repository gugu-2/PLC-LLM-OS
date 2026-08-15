import pytest
import asyncio
import json
from lumina.backend.lumina_pal import PALManager
from lumina.backend.lumina_verify import VerificationGauntlet, Layer1StaticLinter, Layer2SMTModelChecker, export_to_rockwell_l5x
from lumina.backend.lumina_ai import LuminaAIEngine, IndustrialRAGKnowledgeBase
from lumina.backend.lumina_security import HardwareDeploymentProxy
from lumina.backend.simulated_plant import SimulatedPackagingPlant
from lumina.dataset_pipeline.clean_dataset import is_valid_plc_code


@pytest.fixture
def pal_mgr():
    mgr = PALManager()
    asyncio.run(mgr.initialize_default_plant_topology())
    return mgr


@pytest.fixture
def gauntlet():
    return VerificationGauntlet()


@pytest.fixture
def ai_engine():
    return LuminaAIEngine()


@pytest.fixture
def sec_proxy():
    return HardwareDeploymentProxy()


def test_rockwell_l5x_xml_generation():
    """Verify Rockwell Studio 5000 L5X XML generation compliance."""
    st_code = "IF bBottle THEN\n    nDecel := 380;\nEND_IF;"
    tags = {"bBottle": "BOOL", "nDecel": "DINT"}
    xml_out = export_to_rockwell_l5x("Routine_Test", st_code, tags)
    
    assert "RSLogix5000Content" in xml_out
    assert 'TargetName="Routine_Test"' in xml_out
    assert 'DataType="BOOL"' in xml_out
    assert 'DataType="DINT"' in xml_out
    assert "nDecel := 380;" in xml_out


def test_clean_dataset_heuristics():
    """Verify IEC 61131-3 dataset cleaning and noise rejection heuristics."""
    # Valid SCL
    valid_scl = """
    FUNCTION_BLOCK FB_MotorControl
    VAR_INPUT
        bStart : BOOL;
        bStop : BOOL;
    END_VAR
    VAR_OUTPUT
        bRun : BOOL;
    END_VAR
    BEGIN
        IF bStart AND NOT bStop THEN
            bRun := TRUE;
        ELSIF bStop THEN
            bRun := FALSE;
        END_IF;
    END_FUNCTION_BLOCK
    """
    assert is_valid_plc_code(valid_scl) is True

    # Invalid Python / Bazel foreign code
    invalid_code_1 = "import os\nimport sys\ndef main():\n    print('hello world')"
    assert is_valid_plc_code(invalid_code_1) is False

    invalid_code_2 = "package(default_visibility = ['//visibility:public'])\nload('@rules_cc//cc:defs.bzl', 'cc_library')"
    assert is_valid_plc_code(invalid_code_2) is False


def test_rag_semantic_query_and_dynamic_upload(ai_engine):
    """Verify RAG knowledge base search scoring and dynamic manual upload."""
    results = ai_engine.rag.query("Siemens TIA Portal communication error 16#80C4", top_k=2)
    assert len(results) > 0
    assert any("80C4" in doc["id"] or "80C4" in doc["title"] for doc in results)

    # Add custom document
    new_doc = ai_engine.rag.add_document(
        title="Omron Sysmac NJ Inverter Manual",
        category="OEM_MANUAL",
        content="Error 0x2100 indicates overcurrent during acceleration ramp.",
        tags=["Omron", "Inverter", "Overcurrent"]
    )
    assert new_doc["id"].startswith("DOC-USR-")
    
    omron_query = ai_engine.rag.query("Omron inverter overcurrent", top_k=1)
    assert len(omron_query) > 0
    assert omron_query[0]["title"] == "Omron Sysmac NJ Inverter Manual"


def test_smt_prover_catches_deceleration_bounds(gauntlet):
    """Verify Z3 SMT prover detects out-of-bound deceleration values."""
    # Unsafe code setting ramp to 100ms (below minimum 200ms)
    unsafe_rules = [
        {"target": "DecelRamp_ms", "type": "CLAMP_INT", "min": 0, "max": 1000, "condition": 100}
    ]
    vars_map = {"DecelRamp_ms": "INT"}
    invariants = ["DECEL_RAMP_SAFE_BOUNDS"]

    res = gauntlet.smt_checker.verify_safety_invariants(vars_map, unsafe_rules, invariants)
    # Prover must catch that DecelRamp_ms (100) violates DecelRamp_ms >= 200
    assert res[0] is False
    assert res[1] is not None # Counterexample must exist


def test_process_mining_fsm_synthesis(pal_mgr):
    """Verify high-frequency state machine reverse engineering."""
    mining_res = pal_mgr.process_mine_state_machine()
    assert "synthesized_states" in mining_res
    assert "inferred_state_transitions" in mining_res
    assert len(mining_res["synthesized_states"]) > 0


def test_security_proxy_tag_prefix_rules(sec_proxy):
    """Verify adding custom protected prefixes blocks unauthorized payloads."""
    sec_proxy.add_protected_prefix("ROBOT_SAFETY_")
    assert "ROBOT_SAFETY_" in sec_proxy.PROTECTED_SAFETY_PREFIXES

    passed, reason = sec_proxy.inspect_and_filter(
        target_machine="Line 5 Robot",
        target_tag="ROBOT_SAFETY_ZONE1",
        code_payload="ROBOT_SAFETY_ZONE1 := TRUE;"
    )
    assert passed is False
    assert "POLICY_VIOLATION" in reason


def test_endianness_transformer_and_crc32():
    """Verify Siemens Big-Endian vs Rockwell Little-Endian conversions and CRC32 attestation."""
    from lumina.backend.lumina_pal import EndiannessTransformer
    
    val = 55.5
    s7_bytes = EndiannessTransformer.to_s7_real(val)
    cip_bytes = EndiannessTransformer.to_cip_real(val)
    
    assert len(s7_bytes) == 4
    assert len(cip_bytes) == 4
    assert s7_bytes != cip_bytes # Big vs Little endian must differ in byte ordering
    assert round(EndiannessTransformer.from_s7_real(s7_bytes), 1) == val
    assert round(EndiannessTransformer.from_cip_real(cip_bytes), 1) == val

    crc = EndiannessTransformer.compute_crc32("Line3.Infeed.DecelRamp_ms:380:1700000000")
    assert crc != 0


def test_cegar_predicate_abstractor():
    """Verify CEGAR piecewise linear bounds construction."""
    from lumina.backend.lumina_verify import CEGARPredicateAbstractor
    bounds = CEGARPredicateAbstractor.linearize_bounds("DecelRamp_ms", 200, 800, bit_width=32)
    assert "lower" in bounds
    assert "upper" in bounds


def test_domain_randomizer_physics():
    """Verify Bayesian domain randomization stochastic boundaries."""
    from lumina.backend.simulated_plant import DomainRandomizer
    dr = DomainRandomizer(variance_pct=0.20)
    
    frictions = [dr.sample_friction(1.0) for _ in range(50)]
    assert all(0.80 <= f <= 1.20 for f in frictions)
    assert min(frictions) < 0.95
    assert max(frictions) > 1.05


def test_adaptive_burst_rate_limiter_changeover(sec_proxy):
    """Verify state-aware rate limiter permits higher burst during changeover/maintenance."""
    # Under changeover mode, user can perform more requests than standard production limit
    changeover_user = "ENGINEER_MAINTENANCE_CHANGEOVER"
    
    success_count = 0
    for i in range(15):
        passed, _ = sec_proxy.inspect_and_filter(
            target_machine="Line3_Infeed",
            target_tag=f"Line3.Infeed.Param_{i}",
            code_payload=f"Line3.Infeed.Param_{i} := {i};",
            authenticated_user=changeover_user
        )
        if passed:
            success_count += 1
            
    assert success_count >= 12
