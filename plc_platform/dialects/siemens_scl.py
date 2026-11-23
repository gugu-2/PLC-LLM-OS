#!/usr/bin/env python3
"""
plc_platform/dialects/siemens_scl.py — Siemens TIA Portal SCL Code Engine
Reference: PLC_DOMAIN_INTELLIGENCE.md, PROJECT_ARCHITECTURE.md

Produces fully compliant Siemens SIMATIC S7-1200 / S7-1500 Structured Control
Language (SCL) code packages including:
1. User-Defined Types (UDT) for parameter records.
2. Global Optimized Data Blocks (DB).
3. Cyber-physical Function Blocks (FB) with S7_Optimized_Access.
4. Organization Blocks (OB1 Main and OB35 Cyclic Interrupt at 10ms).
5. Siemens #local tag scoping and REGION structuring.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import re


@dataclass
class SiemensBlockPackage:
    fb_name: str
    scl_source: str
    udt_source: Optional[str] = None
    db_source: Optional[str] = None
    ob_source: Optional[str] = None
    input_tags: Dict[str, str] = field(default_factory=dict)
    output_tags: Dict[str, str] = field(default_factory=dict)
    static_tags: Dict[str, str] = field(default_factory=dict)
    temp_tags: Dict[str, str] = field(default_factory=dict)


class SiemensSCLEngine:
    """Siemens TIA Portal SCL Dialect Synthesizer and Parser."""

    def __init__(self, target_controller: str = "S7-1500"):
        self.target_controller = target_controller

    def generate_package(
        self,
        fb_name: str,
        system_name: str,
        sector: str,
        inputs: Dict[str, str],
        outputs: Dict[str, str],
        statics: Dict[str, str],
        temps: Dict[str, str],
        logic_body_st: str,
        engineering_units: Optional[Dict[str, str]] = None
    ) -> SiemensBlockPackage:
        """
        Synthesizes a production-ready Siemens SCL source file containing UDT, DB, FB, and OB.
        """
        units = engineering_units or {}
        udt_name = f"type_{fb_name}_Config"
        db_name = f"DB_{fb_name}_Data"
        ob_name = f"OB35_{fb_name}_Cyclic"

        # 1. Synthesize UDT
        udt_lines = [
            f'TYPE "{udt_name}"',
            "VERSION : 0.1",
            "   STRUCT",
            "      r_Gain_Kp               : Real := 1.5;         // Proportional Gain",
            "      r_Integral_Ti           : Time := T#1s;        // Integral Action Time",
            "      r_Derivative_Td         : Time := T#100ms;     // Derivative Action Time",
            "      t_DiscrepancyFilter     : Time := T#150ms;     // 2oo3 Sensor Discrepancy Time",
            "      r_HighHighLimit         : Real := 100.0;       // Level Alarm HH",
            "      r_LowLowLimit           : Real := 0.0;         // Level Alarm LL",
            "      r_HysteresisDeadband    : Real := 2.5;         // ISA-18.2 Deadband [bar/degC]",
            "   END_STRUCT;",
            "END_TYPE",
            ""
        ]
        udt_code = "\n".join(udt_lines)

        # 2. Synthesize Global DB
        db_lines = [
            f'DATA_BLOCK "{db_name}"',
            "{ S7_Optimized_Access := 'TRUE' }",
            "VERSION : 0.1",
            "NON_RETAIN",
            "   VAR",
            f'      Config : "{udt_name}";',
            "      CycleCounter : DInt := 0;",
            "      TelemetryBuffer : Array[0..31] of Real;",
            "   END_VAR",
            "BEGIN",
            "END_DATA_BLOCK",
            ""
        ]
        db_code = "\n".join(db_lines)

        # 3. Transform logic body: prefix local variables with Siemens '#' tag token
        all_local_vars = set(inputs.keys()) | set(outputs.keys()) | set(statics.keys()) | set(temps.keys())
        siemens_logic = self._apply_siemens_tag_scoping(logic_body_st, all_local_vars)

        # 4. Synthesize Function Block
        fb_lines = [
            f'FUNCTION_BLOCK "{fb_name}"',
            "{ S7_Optimized_Access := 'TRUE' }",
            "VERSION : 0.1",
            f"// SYSTEM: {system_name} | SECTOR: {sector.upper()}",
            f"// TARGET CONTROLLER: SIMATIC {self.target_controller}",
            "   VAR_INPUT",
        ]
        for name, typ in inputs.items():
            u = f" // [{units[name]}]" if name in units else ""
            fb_lines.append(f"      {name} : {self._map_type(typ)};{u}")
        fb_lines.append("   END_VAR")

        fb_lines.append("   VAR_OUTPUT")
        for name, typ in outputs.items():
            u = f" // [{units[name]}]" if name in units else ""
            fb_lines.append(f"      {name} : {self._map_type(typ)};{u}")
        fb_lines.append("   END_VAR")

        fb_lines.append("   VAR")
        for name, typ in statics.items():
            u = f" // [{units[name]}]" if name in units else ""
            fb_lines.append(f"      {name} : {self._map_type(typ)};{u}")
        fb_lines.append("   END_VAR")

        fb_lines.append("   VAR_TEMP")
        for name, typ in temps.items():
            u = f" // [{units[name]}]" if name in units else ""
            fb_lines.append(f"      {name} : {self._map_type(typ)};{u}")
        fb_lines.append("   END_VAR")

        fb_lines.extend([
            "BEGIN",
            "   REGION Safety Interlock & Scan Initializer",
            "      // Enforce zero actuators on safety trip or missing enable",
            "      IF NOT #b_EStop_OK OR NOT #b_SystemEnable THEN",
            "         #b_Running := FALSE;",
            "         #b_ActuatorActive := FALSE;",
            "         #r_ControlEffort_U := 0.0;",
            "         #i_OperatingState := 99; // STATE_TRIPPED",
            "         RETURN;",
            "      END_IF;",
            "   END_REGION",
            "",
            "   REGION Core Cyber-Physical & TMR Execution",
            siemens_logic,
            "   END_REGION",
            "END_FUNCTION_BLOCK",
            ""
        ])
        fb_code = "\n".join(fb_lines)

        # 5. Synthesize Cyclic OB (OB35 / OB30 Periodic Interrupt at 10ms)
        ob_lines = [
            f'ORGANIZATION_BLOCK "{ob_name}"',
            "TITLE = 'Cyclic Cyber-Physical Control Loop 10ms'",
            "{ S7_Optimized_Access := 'TRUE' }",
            "VERSION : 0.1",
            "   VAR_TEMP",
            "      info : Byte;",
            "   END_VAR",
            "BEGIN",
            f'   // Call Instance DB for {fb_name}',
            f'   "Inst_{fb_name}"(',
            '      b_SystemEnable := "DB_GlobalPlant".Permissive_OK,',
            '      b_EStop_OK := "DB_Safety".MasterEStop_OK,',
            '      b_Start_PB := "DB_HMI".Cmd_Start,',
            '      b_Stop_PB := "DB_HMI".Cmd_Stop,',
            '      b_Reset_PB := "DB_HMI".Cmd_Reset',
            '   );',
            "END_ORGANIZATION_BLOCK",
            ""
        ]
        ob_code = "\n".join(ob_lines)

        full_scl = f"{udt_code}\n{db_code}\n{fb_code}\n{ob_code}"

        return SiemensBlockPackage(
            fb_name=fb_name,
            scl_source=full_scl,
            udt_source=udt_code,
            db_source=db_code,
            ob_source=ob_code,
            input_tags=inputs,
            output_tags=outputs,
            static_tags=statics,
            temp_tags=temps
        )

    def _map_type(self, typ: str) -> str:
        """Maps generic IEC types to Siemens SCL canonical casing."""
        mapping = {
            "BOOL": "Bool",
            "INT": "Int",
            "DINT": "DInt",
            "REAL": "Real",
            "LREAL": "LReal",
            "TIME": "Time",
            "STRING": "String",
            "WORD": "Word",
            "DWORD": "DWord"
        }
        upper = typ.strip().upper()
        if upper.startswith("ARRAY"):
            # e.g. ARRAY[0..3] OF REAL -> Array[0..3] of Real
            return typ.replace("ARRAY", "Array").replace("OF", "of").replace("REAL", "Real").replace("BOOL", "Bool")
        return mapping.get(upper, typ)

    def _apply_siemens_tag_scoping(self, code: str, local_vars: set) -> str:
        """Applies Siemens '#' local tag prefix to all local variables in the body."""
        lines = code.splitlines()
        scoped_lines = []
        for line in lines:
            # Skip comments
            if line.strip().startswith("//") or line.strip().startswith("(*"):
                scoped_lines.append(line)
                continue
            
            # Replace variable occurrences not already preceded by '#' or inside quotes
            # Tokenize by identifier
            def replacer(match):
                var = match.group(1)
                prefix = match.string[match.start() - 1] if match.start() > 0 else ""
                if prefix == "#" or prefix == '"' or prefix == '.':
                    return var
                if var in local_vars:
                    return f"#{var}"
                return var

            modified_line = re.sub(r"\b([A-Za-z_][A-Za-z0-9_]*)\b", replacer, line)
            scoped_lines.append(modified_line)
        return "\n".join(scoped_lines)

    def parse_scl(self, scl_text: str) -> Dict[str, Any]:
        """Parses SCL text to extract blocks, variables, and interface mappings."""
        result = {
            "fb_name": None,
            "udts": [],
            "data_blocks": [],
            "inputs": {},
            "outputs": {},
            "statics": {},
            "temps": {}
        }
        fb_match = re.search(r'FUNCTION_BLOCK\s+["\']?([A-Za-z0-9_]+)["\']?', scl_text)
        if fb_match:
            result["fb_name"] = fb_match.group(1)

        result["udts"] = re.findall(r'TYPE\s+["\']?([A-Za-z0-9_]+)["\']?', scl_text)
        result["data_blocks"] = re.findall(r'DATA_BLOCK\s+["\']?([A-Za-z0-9_]+)["\']?', scl_text)

        # Extract VAR blocks
        for section, target in [
            ("VAR_INPUT", "inputs"),
            ("VAR_OUTPUT", "outputs"),
            ("VAR", "statics"),
            ("VAR_TEMP", "temps")
        ]:
            match = re.search(rf"\b{section}\b(.*?)\bEND_VAR\b", scl_text, re.DOTALL)
            if match:
                for line in match.group(1).splitlines():
                    line = line.strip()
                    if line and not line.startswith("//"):
                        m = re.match(r"([A-Za-z0-9_]+)\s*:\s*([^;]+);", line)
                        if m:
                            result[target][m.group(1)] = m.group(2).strip()

        return result
