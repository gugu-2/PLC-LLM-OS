"""
plc_platform/dialects — Multi-Vendor and Multi-Language PLC Code Engines.

Supports:
- Siemens TIA Portal SCL (Structured Control Language) with DB/UDT/OB integration
- Rockwell Studio 5000 Logix Designer L5X XML (AOI, RLL, ST, Tags)
- Beckhoff TwinCAT 3 TcPOU XML with ADS and PLCopen motion interfaces
- Relay Ladder Logic (RLL / LD) ASCII and AST bi-directional translator
"""

from .siemens_scl import SiemensSCLEngine, SiemensBlockPackage
from .rockwell_l5x import RockwellL5XEngine, RockwellAOIPackage
from .twincat_pou import TwinCATPOUEngine, TwinCATPackage
from .ladder_diagram import (
    LadderDiagramEngine,
    LadderRung,
    LadderInstruction,
    LadderBranch,
    LadderProgram,
)

__all__ = [
    "SiemensSCLEngine",
    "SiemensBlockPackage",
    "RockwellL5XEngine",
    "RockwellAOIPackage",
    "TwinCATPOUEngine",
    "TwinCATPackage",
    "LadderDiagramEngine",
    "LadderRung",
    "LadderInstruction",
    "LadderBranch",
    "LadderProgram",
]
