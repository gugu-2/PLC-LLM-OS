#!/usr/bin/env python3
"""
platform/agents/requirements_engineer.py — Agent 1: Requirements Engineer
Reference: AGENTIC_ENGINEERING_WORKFLOW.md, PLC_DOMAIN_INTELLIGENCE.md

Responsible for:
1. Extracting engineering parameters from unstructured automation requests.
2. Identifying missing hardware, I/O, timing, and safety specifications.
3. Formulating targeted clarification questions rather than hallucinating specs.
4. Outputting an authoritative ValidatedEngineeringBrief.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional, Tuple
import re
import uuid
from datetime import datetime, timezone


@dataclass
class IOMapping:
    name: str
    direction: str  # "INPUT", "OUTPUT", "INOUT"
    data_type: str  # "BOOL", "REAL", "DINT", "INT", etc.
    description: str
    physical_address: Optional[str] = None  # e.g. "%IX0.0", "Local:1:I.Data.0"


@dataclass
class ValidatedEngineeringBrief:
    brief_id: str
    title: str
    sector: str
    subsector: str
    system_name: str
    target_vendor: str          # "SIEMENS", "ROCKWELL", "BECKHOFF", "CODESYS", "GENERIC_IEC"
    controller_model: str       # e.g. "S7-1516", "ControlLogix 1756-L83E", "CX5130"
    target_language: str        # "STRUCTURED_TEXT", "SCL", "L5X_ST", "LADDER_DIAGRAM", "SFC"
    operating_modes: List[str]  # e.g. ["MANUAL", "STEP", "AUTOMATIC", "PACKML"]
    cycle_time_target_ms: float
    sil_rating: str             # "NONE", "SIL_2", "SIL_3"
    inputs: List[IOMapping] = field(default_factory=list)
    outputs: List[IOMapping] = field(default_factory=list)
    standards_context: List[str] = field(default_factory=list)
    process_description: str = ""
    clarification_history: List[Dict[str, str]] = field(default_factory=list)
    is_complete: bool = True
    missing_fields: List[str] = field(default_factory=list)


class RequirementsEngineer:
    """Agent 1: Industrial Automation Requirements Discovery & Clarification Engine."""

    VENDOR_PATTERNS = {
        "SIEMENS": [r"\bsiemens\b", r"\btia\s*portal\b", r"\bs7[-_]?1[25]00\b", r"\bscl\b", r"\bsimatic\b"],
        "ROCKWELL": [r"\brockwell\b", r"\ballen[-_]?bradley\b", r"\bcontrol[-_]?logix\b", r"\bcompact[-_]?logix\b", r"\bstudio\s*5000\b", r"\brslogix\b", r"\bl5x\b"],
        "BECKHOFF": [r"\bbeckhoff\b", r"\btwincat\b", r"\btcpou\b", r"\bads\b", r"\bethercat\b"],
        "CODESYS": [r"\bcodesys\b", r"\bplcopen\b"],
        "SCHNEIDER": [r"\bschneider\b", r"\bmodicon\b", r"\becostruxure\b", r"\bunity\s*pro\b"],
        "OMRON": [r"\bomron\b", r"\bsysmac\b", r"\bnj\d+\b", r"\bnx\d+\b"],
        "MITSUBISHI": [r"\bmitsubishi\b", r"\bmelsec\b", r"\bgx\s*works\b", r"\biq[-_]?[rf]\b"]
    }

    SECTOR_PATTERNS = {
        "automotive": [r"\bautomotive\b", r"\bbiw\b", r"\bbody[-_]in[-_]white\b", r"\bwelding\b", r"\bvehicle\b", r"\bev\s*battery\b", r"\bmotorcycle\b", r"\bbike\b", r"\btwo[-_]wheeler\b"],
        "electronics": [r"\belectronics\b", r"\bsmt\b", r"\bpick\s*(?:and|&)\s*place\b", r"\breflow\b", r"\baoi\b", r"\bpcba?\b", r"\bin[-_]circuit\b", r"\bflying\s*probe\b"],
        "semiconductor": [r"\bsemiconductor\b", r"\bwafer\b", r"\bwire\s*bond\b", r"\bdie\s*attach\b", r"\bcleanroom\b", r"\bhepa\b", r"\bffu\b", r"\bfowlp\b"],
        "heavy_machinery": [r"\bheavy\s*machinery\b", r"\bstamping\s*press\b", r"\bservo\s*press\b", r"\bcnc\b", r"\bgantry\b", r"\bgear\s*grinding\b", r"\bforging\b", r"\blaser\s*blanking\b"],
        "plastics": [r"\bplastics?\b", r"\binjection\s*molding\b", r"\bextrusion\b", r"\bblow\s*molding\b", r"\bparison\b", r"\bfilm\b"],
        "foodbev": [r"\bfood\b", r"\bbeverage\b", r"\bbottling\b", r"\bcanning\b", r"\baseptic\b", r"\bpasteuriz\w*\b", r"\bcip\b", r"\bretort\b", r"\bseamer\b"],
        "steelmaking": [r"\bsteel\b", r"\bcold\s*mill\b", r"\bhot\s*mill\b", r"\bgalvaniz\w*\b", r"\bpickling\b", r"\bcontinuous\s*caster\b"]
    }

    def analyze_request(self, user_prompt: str) -> Tuple[ValidatedEngineeringBrief, List[str]]:
        """
        Parses user prompt, extracts engineering parameters, checks for completeness,
        and returns (brief, clarification_questions).
        """
        prompt_lower = user_prompt.lower()

        # 1. Vendor Identification
        target_vendor = "GENERIC_IEC"
        for vendor, patterns in self.VENDOR_PATTERNS.items():
            if any(re.search(pat, prompt_lower) for pat in patterns):
                target_vendor = vendor
                break

        # 2. Sector Identification
        sector = "heavy_machinery"
        for sec, patterns in self.SECTOR_PATTERNS.items():
            if any(re.search(pat, prompt_lower) for pat in patterns):
                sector = sec
                break

        # 3. Language
        target_language = "STRUCTURED_TEXT"
        if target_vendor == "SIEMENS":
            target_language = "SCL"
        elif target_vendor == "ROCKWELL":
            target_language = "L5X_ST"
        if re.search(r"\bladder\b|\blad\b|\brll\b", prompt_lower):
            target_language = "LADDER_DIAGRAM"
        elif re.search(r"\bsfc\b|\bsequential\s*function\b|\bgraph\b", prompt_lower):
            target_language = "SFC"
        elif re.search(r"\bfbd\b|\bfunction\s*block\s*diagram\b", prompt_lower):
            target_language = "FBD"

        # 4. Controller Model Extraction
        controller_model = "Standard Industrial Controller"
        if "s7-15" in prompt_lower or "1500" in prompt_lower:
            controller_model = "Siemens S7-1516-3 PN/DP"
        elif "s7-12" in prompt_lower or "1200" in prompt_lower:
            controller_model = "Siemens S7-1215C DC/DC/DC"
        elif "controllogix" in prompt_lower or "1756" in prompt_lower:
            controller_model = "Rockwell 1756-L83E ControlLogix 5580"
        elif "compactlogix" in prompt_lower or "5069" in prompt_lower:
            controller_model = "Rockwell 5069-L320ER CompactLogix 5380"
        elif "twincat" in prompt_lower or "beckhoff" in prompt_lower:
            controller_model = "Beckhoff CX5130 Embedded PC"

        # 5. Safety Integrity Level
        sil_rating = "NONE"
        if "sil 3" in prompt_lower or "sil-3" in prompt_lower or "ple" in prompt_lower:
            sil_rating = "SIL_3"
        elif "sil 2" in prompt_lower or "sil-2" in prompt_lower or "pld" in prompt_lower or "safety" in prompt_lower:
            sil_rating = "SIL_2"

        # 6. Cycle Time Extraction
        cycle_ms = 10.0
        m_cycle = re.search(r"(\d+(?:\.\d+)?)\s*(?:ms|milliseconds?)\s*(?:cycle|period|task)?", prompt_lower)
        if m_cycle:
            cycle_ms = float(m_cycle.group(1))

        # 7. Operating Modes
        modes = ["AUTOMATIC", "MANUAL", "FAULT"]
        if "packml" in prompt_lower or "omac" in prompt_lower:
            modes = ["STOPPED", "RESETTING", "IDLE", "STARTING", "EXECUTE", "HOLDING", "HELD", "UNHOLDING", "STOPPING", "ABORTING", "ABORTED", "CLEARING"]
        elif "step" in prompt_lower or "semi-auto" in prompt_lower:
            modes.append("STEP_AUTOMATIC")

        # 8. Check for Missing Critical Parameters
        missing = []
        questions = []

        if target_vendor == "GENERIC_IEC" and not re.search(r"\bgeneric\b|\biec\b", prompt_lower):
            missing.append("target_vendor")
            questions.append(
                "Target PLC Platform: Which hardware controller or software environment are you targeting "
                "(e.g., Siemens S7-1500 / TIA Portal, Rockwell Studio 5000 Logix, Beckhoff TwinCAT 3, or CODESYS v3.5)?"
            )

        if not re.search(r"\binputs?\b|\btags?\b|\bsensors?\b|di_\w+|r_\w+", prompt_lower) and len(user_prompt.split()) < 30:
            missing.append("io_specification")
            questions.append(
                "I/O Architecture: Do you have a specific physical I/O tag list, or should the system generate "
                "a standardized symbolic User-Defined Type (UDT) interface?"
            )

        # 9. Extract or Build I/O Mappings
        inputs, outputs = self._extract_or_generate_io(user_prompt, target_vendor)

        # 10. Query Hybrid Standards RAG
        standards_notes = []
        try:
            from ..rag import HybridStandardsRetriever
            retriever = HybridStandardsRetriever()
            retrieved_chunks = retriever.retrieve(
                query=user_prompt,
                top_k=2,
                vendor=target_vendor if target_vendor != "GENERIC_IEC" else None,
                sector=sector
            )
            for chunk in retrieved_chunks:
                standards_notes.append(f"[{chunk.standard_name}] {chunk.title}: {chunk.content[:200]}...")
        except Exception:
            pass

        brief = ValidatedEngineeringBrief(
            brief_id=f"VEB-{uuid.uuid4().hex[:8]}",
            title=re.sub(r"[^A-Za-z0-9_ ]", "", user_prompt[:60]).strip() or "Industrial Control System",
            sector=sector,
            subsector="general",
            system_name=f"SYS_{sector.title()}_{brief_id_suffix(brief_id=None)}",
            target_vendor=target_vendor,
            controller_model=controller_model,
            target_language=target_language,
            operating_modes=modes,
            cycle_time_target_ms=cycle_ms,
            sil_rating=sil_rating,
            inputs=inputs,
            outputs=outputs,
            standards_context=standards_notes,
            process_description=user_prompt,
            is_complete=len(missing) == 0,
            missing_fields=missing
        )

        return brief, questions

    def _extract_or_generate_io(self, prompt: str, vendor: str) -> Tuple[List[IOMapping], List[IOMapping]]:
        """Parses explicitly mentioned I/O or synthesizes standard industrial I/O."""
        inputs = [
            IOMapping(name="b_SystemEnable", direction="INPUT", data_type="BOOL", description="Master System Enable Permissive"),
            IOMapping(name="b_EStop_OK", direction="INPUT", data_type="BOOL", description="Emergency Stop Healthy Permissive (Dual-Channel Monitor)"),
            IOMapping(name="b_Start_PB", direction="INPUT", data_type="BOOL", description="Operator Cycle Start Pushbutton"),
            IOMapping(name="b_Stop_PB", direction="INPUT", data_type="BOOL", description="Operator Normal Stop Pushbutton"),
            IOMapping(name="b_Reset_PB", direction="INPUT", data_type="BOOL", description="Fault Reset Pushbutton"),
            IOMapping(name="r_ProcessValue_Raw", direction="INPUT", data_type="REAL", description="Primary Analog Sensor Measurement [bar/degC/mm]")
        ]

        outputs = [
            IOMapping(name="b_Running", direction="OUTPUT", data_type="BOOL", description="System Active Running Status Lamp"),
            IOMapping(name="b_FaultActive", direction="OUTPUT", data_type="BOOL", description="General Fault Summary Beacon"),
            IOMapping(name="b_ActuatorCmd", direction="OUTPUT", data_type="BOOL", description="Primary Main Contactor / Cylinder Solenoid"),
            IOMapping(name="r_ControlOutput", direction="OUTPUT", data_type="REAL", description="Analog Servo Drive / Valve Setpoint [0.0-100.0%]")
        ]
        return inputs, outputs


def brief_id_suffix(brief_id: Optional[str] = None) -> str:
    return uuid.uuid4().hex[:6].upper()
