#!/usr/bin/env python3
"""
test_domain_triage_audit.py — Comprehensive Audit Verification Test Suite for validate_domain.py
Validates:
1. All 7 target commercial manufacturing sectors (automotive, electronics, semiconductor, heavy_machinery, plastics, foodbev, steelmaking).
2. All 7 forbidden domains (marine, pharmaceutical, defense, oil_gas, power_generation, mining, datacenter).
3. Priority rules (forbidden domain reject takes precedence over sanctioned keywords).
4. Ambiguity handling (generic blocks with no domain keywords).
5. File and CLI execution behavior (exit codes 0 on PASS, 1 on REJECT).
"""

import sys
import os
import json
import subprocess
import tempfile
from pathlib import Path
import pytest

from validate_domain import (
    SANCTIONED_SECTORS,
    FORBIDDEN_DOMAINS,
    extract_fb_name,
    check_no_forbidden_keywords,
    verify_manufacturing_domain,
    classify_dataset,
    validate_domain_content,
    validate_domain_file,
)

# -------------------------------------------------------------
# 1. Structural Dictionary Integrity Audits
# -------------------------------------------------------------

def test_sanctioned_sectors_completeness():
    """Verify all 7 mandated manufacturing sectors are explicitly registered."""
    expected_sectors = {
        "automotive",
        "electronics",
        "semiconductor",
        "heavy_machinery",
        "plastics",
        "foodbev",
        "steelmaking",
    }
    actual_sectors = set(SANCTIONED_SECTORS.keys())
    assert actual_sectors == expected_sectors, f"Mismatch in sanctioned sectors: {actual_sectors ^ expected_sectors}"
    
    # Verify non-trivial keyword coverage for each sector
    for sector, kws in SANCTIONED_SECTORS.items():
        assert len(kws) >= 15, f"Sector {sector} has insufficient keyword depth: {len(kws)}"


def test_forbidden_domains_completeness():
    """Verify all 7 forbidden domains are defined with non-empty keyword lists."""
    expected_domains = {
        "marine",
        "pharmaceutical",
        "defense",
        "oil_gas",
        "power_generation",
        "mining",
        "datacenter",
    }
    actual_domains = set(FORBIDDEN_DOMAINS.keys())
    assert actual_domains == expected_domains, f"Mismatch in forbidden domains: {actual_domains ^ expected_domains}"
    
    for domain, kws in FORBIDDEN_DOMAINS.items():
        assert len(kws) >= 4, f"Forbidden domain {domain} has insufficient keyword depth: {len(kws)}"


# -------------------------------------------------------------
# 2. Manufacturing Sector PASS Verification
# -------------------------------------------------------------

@pytest.mark.parametrize("sector,fb_name,body_keyword", [
    ("automotive", "FB_Automotive_BIW_WeldStation", "RollerHemming"),
    ("automotive", "FB_EV_Battery_CellToPack_Dispense", "LaserWeld"),
    ("electronics", "FB_SMT_HighSpeed_PickAndPlace", "ReflowOven"),
    ("electronics", "FB_AOI_InspectionVision_PCBA", "WaveSolder"),
    ("semiconductor", "FB_WireBond_DieAttach_Package", "CuPillar"),
    ("semiconductor", "FB_CleanroomHVAC_HEPA_CMP", "EtchChamber"),
    ("heavy_machinery", "FB_StampingPress_Hydraulic_TransferDie", "ProgressiveDie"),
    ("heavy_machinery", "FB_CNC_FiveAxis_GantryMill", "ActiveSpindleThermal"),
    ("plastics", "FB_Plastics_InjectionMolding_VtoP", "CavityPressure"),
    ("plastics", "FB_TwinScrew_Extrusion_ParisonControl", "BlowMolding"),
    ("foodbev", "FB_Aseptic_Bottling_RotaryFiller", "CIP"),
    ("foodbev", "FB_Retort_Autoclave_Sterilizer", "CanSeamer"),
    ("steelmaking", "FB_ColdMill_TandemMill_ContinuousCaster", "RollForce"),
    ("steelmaking", "FB_Galvanizing_Annealing_SkinPass", "AGC"),
])
def test_clean_manufacturing_sectors_pass(sector, fb_name, body_keyword):
    """Ensure clean manufacturing code from all 7 sectors receives verdict PASS and proper sector tag."""
    content = f"""
FUNCTION_BLOCK {fb_name}
VAR_INPUT
    bStart : BOOL;
    rProcessVar : REAL;
END_VAR
VAR_OUTPUT
    bRunning : BOOL;
END_VAR
(* Operational logic controlling {body_keyword} for precision manufacturing *)
IF bStart THEN
    bRunning := TRUE;
END_IF;
END_FUNCTION_BLOCK
"""
    res = validate_domain_content(content)
    assert res["verdict"] == "PASS", f"Expected PASS for {fb_name}, got {res['verdict']} with errors {res.get('forbidden_hits')}"
    assert res["matched_sector"] == sector, f"Expected sector {sector}, got {res['matched_sector']}"
    assert res["forbidden_domain"] is None
    assert len(res["forbidden_hits"]) == 0
    assert len(res["sanctioned_hits"]) > 0


# -------------------------------------------------------------
# 3. Forbidden Domains REJECT Verification
# -------------------------------------------------------------

@pytest.mark.parametrize("domain,fb_name,forbidden_kw", [
    ("marine", "FB_Naval_Ship_PropulsionControl", "Submarine"),
    ("marine", "FB_Subsea_ROV_TetherManagement", "BallastWater"),
    ("pharmaceutical", "FB_Bioreactor_Fermenter_FedBatch", "Lyophilizer"),
    ("pharmaceutical", "FB_ActivePharmaceutical_WFI_Loop", "SyringeFiller"),
    ("defense", "FB_Missile_BallisticGuidance_System", "Warhead"),
    ("defense", "FB_Artillery_Munition_DefenseSystem", "Torpedo"),
    ("oil_gas", "FB_Upstream_Wellhead_BlowoutPreventer", "CrudeOilPipeline"),
    ("oil_gas", "FB_Fracking_MudPump_BOP_Control", "LNG_Terminal"),
    ("power_generation", "FB_NuclearReactor_CoreCoolant", "SteamTurbine_Power"),
    ("power_generation", "FB_HydroelectricTurbine_GridSynchronizer", "BoilerFeedwater"),
    ("mining", "FB_Mining_OreCrusher_SAGMill", "FloatationCell"),
    ("mining", "FB_TailingThickener_SlurryPipeline", "BucketWheelExcavator"),
    ("datacenter", "FB_DataCenterCRAC_ServerRackCooling", "CRAH"),
    ("datacenter", "FB_ChillerPlant_DataCenter_EcoMode", "DataCenterCRAC"),
])
def test_forbidden_domains_fail(domain, fb_name, forbidden_kw):
    """Ensure forbidden domains are blocked with verdict REJECT and identified domain."""
    content = f"""
FUNCTION_BLOCK {fb_name}
VAR_INPUT
    bEnable : BOOL;
END_VAR
(* Forbidden domain operation: {forbidden_kw} *)
IF bEnable THEN
    ;
END_IF;
END_FUNCTION_BLOCK
"""
    res = validate_domain_content(content)
    assert res["verdict"] == "REJECT", f"Expected REJECT for {domain} ({fb_name}), got {res['verdict']}"
    assert res["forbidden_domain"] == domain
    assert any(forbidden_kw.lower() in hit.lower() or domain.lower() in hit.lower() for hit in res["forbidden_hits"])


# -------------------------------------------------------------
# 4. Strict Precedence: Contaminated Manufacturing REJECT
# -------------------------------------------------------------

def test_contaminated_manufacturing_is_rejected():
    """Verify that even if an approved manufacturing keyword is present, forbidden keywords trigger REJECT."""
    # Automotive BIW mixed with Subsea/Marine contamination
    content = """
FUNCTION_BLOCK FB_Automotive_BIW_UnderwaterAssembly
VAR_INPUT
    bStart : BOOL;
END_VAR
(* Robot cell performing SpotWeld and RollerHemming near Subsea cooling lines *)
IF bStart THEN
    ;
END_IF;
END_FUNCTION_BLOCK
"""
    res = validate_domain_content(content)
    assert res["verdict"] == "REJECT", "Contaminated code must be REJECTED regardless of sanctioned keywords"
    assert res["forbidden_domain"] == "marine"
    assert "marine::Subsea" in res["forbidden_hits"]


# -------------------------------------------------------------
# 5. Ambiguous Handling
# -------------------------------------------------------------

def test_generic_code_ambiguous():
    """Verify generic code with no domain keywords is flagged as AMBIGUOUS, not PASS."""
    content = """
FUNCTION_BLOCK FB_Generic_PID_VelocityLoop
VAR_INPUT
    rSetpoint : REAL;
    rFeedback : REAL;
END_VAR
VAR_OUTPUT
    rOut : REAL;
END_VAR
rOut := (rSetpoint - rFeedback) * 1.5;
END_FUNCTION_BLOCK
"""
    res = validate_domain_content(content)
    assert res["verdict"] == "AMBIGUOUS"
    assert res["matched_sector"] is None
    assert res["forbidden_domain"] is None


# -------------------------------------------------------------
# 6. JSON Structure Parsing & File I/O
# -------------------------------------------------------------

def test_validate_domain_file_json(tmp_path):
    """Test JSON dataset file parsing from assistant messages."""
    pass_file = tmp_path / "valid_automotive.json"
    reject_file = tmp_path / "invalid_pharma.json"

    pass_data = {
        "messages": [
            {"role": "user", "content": "Generate an automotive Function Block."},
            {"role": "assistant", "content": "```iec-st\nFUNCTION_BLOCK FB_Automotive_SpotWeld_Cell\n// SpotWeld BIW controller\nEND_FUNCTION_BLOCK\n```"}
        ]
    }
    reject_data = {
        "messages": [
            {"role": "user", "content": "Generate a pharma block."},
            {"role": "assistant", "content": "```iec-st\nFUNCTION_BLOCK FB_Lyophilizer_Control\n// Lyophilization loop\nEND_FUNCTION_BLOCK\n```"}
        ]
    }

    pass_file.write_text(json.dumps(pass_data), encoding="utf-8")
    reject_file.write_text(json.dumps(reject_data), encoding="utf-8")

    res_pass = validate_domain_file(pass_file)
    assert res_pass["verdict"] == "PASS"
    assert res_pass["matched_sector"] == "automotive"

    res_reject = validate_domain_file(reject_file)
    assert res_reject["verdict"] == "REJECT"
    assert res_reject["forbidden_domain"] == "pharmaceutical"


# -------------------------------------------------------------
# 7. CLI Exit Code Integration Verification
# -------------------------------------------------------------

def test_cli_exit_codes(tmp_path):
    """Verify validate_domain.py returns exit code 0 on PASS and 1 on REJECT when called via CLI."""
    pass_file = tmp_path / "cli_pass.json"
    reject_file = tmp_path / "cli_reject.json"

    pass_data = {
        "messages": [
            {"role": "assistant", "content": "FUNCTION_BLOCK FB_CNC_MachiningCenter\n// FiveAxis tooling\nEND_FUNCTION_BLOCK"}
        ]
    }
    reject_data = {
        "messages": [
            {"role": "assistant", "content": "FUNCTION_BLOCK FB_Sonar_AcousticArray\n// Submarine acoustics\nEND_FUNCTION_BLOCK"}
        ]
    }

    pass_file.write_text(json.dumps(pass_data), encoding="utf-8")
    reject_file.write_text(json.dumps(reject_data), encoding="utf-8")

    script_path = str(Path("validate_domain.py").resolve())

    # Test PASS exit code
    proc_pass = subprocess.run([sys.executable, script_path, str(pass_file)], capture_output=True, text=True)
    assert proc_pass.returncode == 0, f"CLI expected 0, got {proc_pass.returncode}. stderr: {proc_pass.stderr}"
    pass_json = json.loads(proc_pass.stdout)
    assert pass_json["verdict"] == "PASS"

    # Test REJECT exit code
    proc_reject = subprocess.run([sys.executable, script_path, str(reject_file)], capture_output=True, text=True)
    assert proc_reject.returncode == 1, f"CLI expected 1, got {proc_reject.returncode}. stdout: {proc_reject.stdout}"
    reject_json = json.loads(proc_reject.stdout)
    assert reject_json["verdict"] == "REJECT"


# -------------------------------------------------------------
# 8. Identifier Underscore & Direct Keyword Verification
# -------------------------------------------------------------

@pytest.mark.parametrize("domain,fb_name,expected_hit", [
    ("marine", "FB_Marine_Rudder_Control", "marine::Marine"),
    ("marine", "FB_Subsea_RoboticArm", "marine::Subsea"),
    ("pharmaceutical", "FB_Pharma_TabletPress_Feeder", "pharmaceutical::Pharma"),
    ("pharmaceutical", "FB_Pharmaceutical_Mixer_Granulator", "pharmaceutical::Pharmaceutical"),
    ("defense", "FB_Defense_Actuator_Positioner", "defense::Defense"),
    ("defense", "FB_Military_Surveillance_Gimbal", "defense::Military"),
    ("oil_gas", "FB_Petrochemical_Cracker_Furnace", "oil_gas::Petrochemical"),
    ("oil_gas", "FB_OilGas_Separator_Level", "oil_gas::OilGas"),
    ("power_generation", "FB_PowerGeneration_TurbineGovernor", "power_generation::PowerGeneration"),
    ("power_generation", "FB_PowerGrid_DynamicStabilizer", "power_generation::PowerGrid"),
    ("mining", "FB_Mining_Excavator_Hydraulics", "mining::Mining"),
    ("datacenter", "FB_DataCenter_ChilledWater_CRAH", "datacenter::DataCenter"),
])
def test_direct_forbidden_identifiers(domain, fb_name, expected_hit):
    """Verify that forbidden domains are blocked even when keywords appear solely inside snake_case FB names."""
    content = f"FUNCTION_BLOCK {fb_name}\nVAR_INPUT\nbRun : BOOL;\nEND_VAR\nEND_FUNCTION_BLOCK\n"
    res = validate_domain_content(content)
    assert res["verdict"] == "REJECT", f"Expected REJECT for {fb_name}, got {res['verdict']}"
    assert res["forbidden_domain"] == domain
    assert expected_hit in res["forbidden_hits"]


@pytest.mark.parametrize("sector,fb_name,expected_hit", [
    ("automotive", "FB_Automotive_Chassis_Transport", "automotive::Automotive"),
    ("electronics", "FB_Electronics_SMT_Assembly", "electronics::Electronics"),
    ("semiconductor", "FB_Semiconductor_Cleanroom_FFU", "semiconductor::Semiconductor"),
    ("heavy_machinery", "FB_HeavyMachinery_Gantry_Axis", "heavy_machinery::HeavyMachinery"),
    ("plastics", "FB_Plastics_Polymer_Extrusion", "plastics::Plastics"),
    ("foodbev", "FB_FoodBev_Packaging_Line", "foodbev::FoodBev"),
    ("steelmaking", "FB_Steelmaking_CoilWinder", "steelmaking::Steelmaking"),
])
def test_direct_sanctioned_identifiers(sector, fb_name, expected_hit):
    """Verify that sanctioned sectors pass when keywords appear in snake_case FB names."""
    content = f"FUNCTION_BLOCK {fb_name}\nVAR_INPUT\nbRun : BOOL;\nEND_VAR\nEND_FUNCTION_BLOCK\n"
    res = validate_domain_content(content)
    assert res["verdict"] == "PASS", f"Expected PASS for {fb_name}, got {res['verdict']}"
    assert res["matched_sector"] == sector
    assert expected_hit in res["sanctioned_hits"]


if __name__ == "__main__":
    pytest.main(["-v", __file__])
