#!/usr/bin/env python3
"""
plc_platform/datasets/schema.py — Dataset Schema v2.0 for Industrial PLC LLM Training
Reference: DATASET_AND_FINETUNING_STRATEGY.md, PROJECT_ARCHITECTURE.md

Defines the 10 core dataset archetypes (DS-01 through DS-10) and structured
record representation ensuring zero benchmark contamination via project-based tracking.
"""

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import Dict, List, Optional, Any
import json
import uuid
import datetime


class DatasetArchetype(str, Enum):
    DS_01_CONVERSATIONS = "DS-01"            # Industrial Manufacturing Conversations
    DS_02_QA_PAIRS = "DS-02"                 # PLC Engineering Question-Answer Pairs
    DS_03_VERIFIED_CODE = "DS-03"            # Verified PLC Code Generation
    DS_04_DEBUGGING = "DS-04"                # PLC Debugging & Code Correction
    DS_05_PROCESS_REASONING = "DS-05"        # Manufacturing Process Reasoning
    DS_06_ARCHITECTURE_REFACTOR = "DS-06"    # PLC Architecture & Refactoring
    DS_07_TROUBLESHOOTING = "DS-07"          # Industrial Troubleshooting & RCA
    DS_08_SAFETY_VALIDATION = "DS-08"        # Safety & Validation Scenarios
    DS_09_VENDOR_TRANSLATION = "DS-09"       # Vendor-Specific Programming & Translation
    DS_10_NEGATIVE_EXAMPLES = "DS-10"        # Negative Examples & Anti-Patterns


@dataclass
class DatasetRecordV2:
    dataset_id: str
    archetype_id: str                          # DS-01 through DS-10
    project_id: str                            # Unique facility/project ID for contamination-free splitting
    sector: str                                # AUTOMOTIVE, ELECTRONICS, HEAVY_MACHINERY, PLASTICS, FOOD_BEVERAGE
    vendor: str                                # SIEMENS, ROCKWELL, BECKHOFF, CODESYS, GENERIC_IEC
    language: str                              # STRUCTURED_TEXT, SCL, L5X_ST, LADDER_DIAGRAM, SFC
    complexity_tier: str                       # TIER_1_BASIC, TIER_2_INTERMEDIATE, TIER_3_ENTERPRISE_CPS
    system_name: str
    instruction: str
    input_context: str
    output_target: str
    conversations: List[Dict[str, str]] = field(default_factory=list)
    verification_status: str = "VERIFIED_STATIC_SMT"  # VERIFIED_STATIC_SMT, EXPERT_REVIEWED, REJECTED
    metadata: Dict[str, Any] = field(default_factory=dict)
    created_at: str = field(default_factory=lambda: datetime.datetime.now(datetime.timezone.utc).isoformat())

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), ensure_ascii=False)

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "DatasetRecordV2":
        return cls(**data)
