#!/usr/bin/env python3
"""
tests/test_dialects.py — Unit Tests for Multi-Vendor and Multi-Language Code Engines
Tests Siemens SCL, Rockwell L5X XML, Beckhoff TwinCAT TcPOU, and Relay Ladder Logic.
"""

import pytest
import xml.etree.ElementTree as ET
from plc_platform.dialects import (
    SiemensSCLEngine,
    RockwellL5XEngine,
    TwinCATPOUEngine,
    LadderDiagramEngine,
    LadderInstruction,
    LadderBranch,
    LadderRung
)


def test_siemens_scl_engine():
    engine = SiemensSCLEngine(target_controller="S7-1500")
    inputs = {"b_EStop_OK": "BOOL", "b_SystemEnable": "BOOL", "r_Pressure": "REAL"}
    outputs = {"b_Running": "BOOL", "b_ActuatorActive": "BOOL", "r_ControlEffort_U": "REAL"}
    statics = {"i_OperatingState": "DINT", "r_InternalState": "ARRAY[0..3] OF REAL"}
    temps = {"r_TempDelta": "REAL"}
    logic = """
IF b_EStop_OK AND b_SystemEnable THEN
    r_InternalState[0] := r_Pressure * 1.5;
    b_Running := TRUE;
    b_ActuatorActive := TRUE;
    r_ControlEffort_U := r_InternalState[0] + r_TempDelta;
END_IF;
"""
    pkg = engine.generate_package(
        fb_name="FB_Auto_LaserWeld",
        system_name="Battery Busbar Laser Welder",
        sector="AUTOMOTIVE",
        inputs=inputs,
        outputs=outputs,
        statics=statics,
        temps=temps,
        logic_body_st=logic,
        engineering_units={"r_Pressure": "bar", "r_ControlEffort_U": "kN"}
    )

    assert "FB_Auto_LaserWeld" in pkg.fb_name
    assert "S7_Optimized_Access" in pkg.scl_source
    assert 'TYPE "type_FB_Auto_LaserWeld_Config"' in pkg.udt_source
    assert 'DATA_BLOCK "DB_FB_Auto_LaserWeld_Data"' in pkg.db_source
    assert 'ORGANIZATION_BLOCK "OB35_FB_Auto_LaserWeld_Cyclic"' in pkg.ob_source
    assert "#b_EStop_OK" in pkg.scl_source  # Tag scoping applied
    assert "#r_InternalState" in pkg.scl_source

    parsed = engine.parse_scl(pkg.scl_source)
    assert parsed["fb_name"] == "FB_Auto_LaserWeld"
    assert "b_EStop_OK" in parsed["inputs"]
    assert "b_Running" in parsed["outputs"]


def test_rockwell_l5x_engine():
    engine = RockwellL5XEngine(software_revision="34.00")
    inputs = {"b_EStop_OK": "BOOL", "r_RawFlow": "REAL"}
    outputs = {"b_ValveOpen": "BOOL", "r_ValvePercent": "REAL"}
    locals_ = {"r_Accumulator": "REAL", "r_StateVector": "ARRAY[0..3] OF REAL"}
    st_logic = "r_Accumulator := r_Accumulator + r_RawFlow;\nb_ValveOpen := r_Accumulator < 100.0;"

    pkg = engine.generate_l5x_package(
        aoi_name="AOI_AsepticDosing",
        system_name="Rotary Filling Doser",
        sector="FOOD_BEVERAGE",
        inputs=inputs,
        outputs=outputs,
        locals_=locals_,
        st_logic=st_logic,
        controller_name="Lumina_1756_L85E"
    )

    assert pkg.aoi_name == "AOI_AsepticDosing"
    # Ensure XML parses cleanly
    root = ET.fromstring(pkg.l5x_xml)
    assert root.tag == "RSLogix5000Content"
    assert root.attrib.get("SoftwareRevision") == "34.00"

    parsed = engine.parse_l5x(pkg.l5x_xml)
    assert parsed["controller_name"] == "Lumina_1756_L85E"
    assert parsed["aoi_name"] == "AOI_AsepticDosing"
    assert "EnableIn" in parsed["parameters"]
    assert "b_EStop_OK" in parsed["parameters"]
    assert "r_StateVector" in parsed["local_tags"]
    assert len(parsed["routine_st_lines"]) == 2
    assert len(parsed["rll_rungs"]) == 1


def test_twincat_pou_engine():
    engine = TwinCATPOUEngine()
    inputs = {"b_StartCycle": "BOOL"}
    outputs = {"b_CycleDone": "BOOL"}
    internals = {"i_Step": "DINT"}
    st_logic = "IF b_StartCycle THEN\n    b_CycleDone := TRUE;\nEND_IF;"

    pkg = engine.generate_tcpou_package(
        fb_name="FB_SMT_FeederCollate",
        system_name="SMT Pick & Place Collation",
        sector="ELECTRONICS",
        inputs=inputs,
        outputs=outputs,
        internals=internals,
        logic_body_st=st_logic,
        enable_motion_blocks=True
    )

    root = ET.fromstring(pkg.tcpou_xml)
    assert root.tag == "TcPlcObject"
    assert pkg.motion_enabled is True
    assert "MC_MoveAbsolute" in pkg.declaration_code

    parsed = engine.parse_tcpou(pkg.tcpou_xml)
    assert parsed["pou_name"] == "FB_SMT_FeederCollate"
    assert "b_AxisEnable" in parsed["inputs"]
    assert "fb_Axis_Power" in parsed["internals"]
    assert "fb_Axis_Power" in parsed["implementation_st"]
    assert "MC_Power" in parsed["declaration"]


def test_ladder_diagram_engine():
    engine = LadderDiagramEngine()

    # Test RLL parsing of branch
    rll_str = "XIC(b_Permissive)BST XIC(b_Start) NXB XIC(b_Running) BND XIO(b_Fault) OTE(b_MotorRun);"
    rung = engine.parse_rockwell_rung(rll_str, rung_num=10, comment="Main Motor Run Latch")

    assert rung.number == 10
    assert len(rung.elements) == 4
    assert isinstance(rung.elements[0], LadderInstruction)
    assert rung.elements[0].tag == "b_Permissive"
    assert isinstance(rung.elements[1], LadderBranch)
    assert len(rung.elements[1].branches) == 2

    # Test ASCII rendering
    ascii_art = rung.to_ascii_art()
    assert "|---" in ascii_art
    assert "b_Permissive" in ascii_art
    assert "b_MotorRun" in ascii_art

    # Test RLL to ST transpilation
    st_result = engine.rung_to_structured_text(rung)
    assert "b_MotorRun :=" in st_result
    assert "b_Permissive" in st_result
    assert "NOT b_Fault" in st_result

    # Test ST boolean to Rung transpilation
    expr = "b_EStop_OK AND (b_CmdStart OR b_AutoRunning) AND NOT b_SafetyGateOpen"
    synthesized_rung = engine.boolean_st_to_rung(
        target_coil="b_MasterRelay",
        bool_expr=expr,
        rung_num=1,
        comment="Safety Permissive Circuit"
    )
    assert synthesized_rung.elements[-1].op == "OTE"
    assert synthesized_rung.elements[-1].tag == "b_MasterRelay"
    assert any(isinstance(e, LadderBranch) for e in synthesized_rung.elements)
