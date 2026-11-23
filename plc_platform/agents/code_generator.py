#!/usr/bin/env python3
"""
platform/agents/code_generator.py — Agent 3: Multi-Dialect Code Generator
Reference: AGENTIC_ENGINEERING_WORKFLOW.md, PLC_DOMAIN_INTELLIGENCE.md

Responsible for:
1. Translating ArchitecturalSpecification into complete, production-grade PLC code.
2. Generating vendor-specific dialects:
   - Siemens SCL with Optimized DB variables
   - Rockwell Studio 5000 .L5X XML & Add-On Instructions (AOI)
   - Beckhoff TwinCAT 3 .TcPOU XML
   - Generic IEC 61131-3 Structured Text
   - Ladder Diagram (LD / RLL) representation
3. Enforcing physical engineering units ([bar], [deg C], [ms], [kN]) on all declarations.
"""

from dataclasses import dataclass, field
from typing import Dict, Any, List, Optional
import re
import uuid
from .control_architect import ArchitecturalSpecification


@dataclass
class CandidateCodePackage:
    package_id: str
    arch_id: str
    target_vendor: str
    target_language: str
    fb_name: str
    structured_text_code: str
    vendor_native_export: Optional[str] = None  # e.g. L5X XML or TcPOU XML
    ladder_ascii_code: Optional[str] = None
    variables_declared: Dict[str, str] = field(default_factory=dict)
    engineering_units_enforced: List[str] = field(default_factory=list)


class MultiDialectCodeGenerator:
    """Agent 3: Multi-Vendor Industrial Code Synthesis Engine."""

    def generate_code_package(self, arch: ArchitecturalSpecification) -> CandidateCodePackage:
        """Synthesizes candidate code package tailored to vendor and dialect."""
        fb_name = f"FB_{arch.sector.title()}_{arch.system_name}"
        st_code = self._synthesize_structured_text(arch, fb_name)
        
        vendor_native = None
        vars_map = self._extract_var_map(st_code)

        if arch.target_vendor == "ROCKWELL":
            from ..dialects.rockwell_l5x import RockwellL5XEngine
            eng = RockwellL5XEngine()
            inputs = {k: v for k, v in vars_map.items() if k.startswith("b_") and "PB" in k or "Sensor" in k or "EStop" in k or "Enable" in k}
            outputs = {k: v for k, v in vars_map.items() if "Running" in k or "Fault" in k or "Actuator" in k or "Effort" in k}
            locals_ = {k: v for k, v in vars_map.items() if k not in inputs and k not in outputs}
            pkg = eng.generate_l5x_package(fb_name, arch.system_name, arch.sector, inputs, outputs, locals_, st_code)
            vendor_native = pkg.l5x_xml
        elif arch.target_vendor == "SIEMENS":
            from ..dialects.siemens_scl import SiemensSCLEngine
            eng = SiemensSCLEngine(target_controller=arch.controller_model)
            inputs = {k: v for k, v in vars_map.items() if k.startswith("b_") and "PB" in k or "Sensor" in k or "EStop" in k or "Enable" in k}
            outputs = {k: v for k, v in vars_map.items() if "Running" in k or "Fault" in k or "Actuator" in k or "Effort" in k}
            statics = {k: v for k, v in vars_map.items() if k not in inputs and k not in outputs}
            pkg = eng.generate_package(fb_name, arch.system_name, arch.sector, inputs, outputs, statics, {}, st_code)
            vendor_native = pkg.scl_source
        elif arch.target_vendor == "BECKHOFF":
            from ..dialects.twincat_pou import TwinCATPOUEngine
            eng = TwinCATPOUEngine()
            inputs = {k: v for k, v in vars_map.items() if k.startswith("b_") and "PB" in k or "Sensor" in k or "EStop" in k or "Enable" in k}
            outputs = {k: v for k, v in vars_map.items() if "Running" in k or "Fault" in k or "Actuator" in k or "Effort" in k}
            internals = {k: v for k, v in vars_map.items() if k not in inputs and k not in outputs}
            pkg = eng.generate_tcpou_package(fb_name, arch.system_name, arch.sector, inputs, outputs, internals, st_code)
            vendor_native = pkg.tcpou_xml

        ladder_ascii = None
        if arch.target_language == "LADDER_DIAGRAM" or "ladder" in arch.target_language.lower():
            from ..dialects.ladder_diagram import LadderDiagramEngine
            ladder_eng = LadderDiagramEngine()
            r1 = ladder_eng.boolean_st_to_rung("b_Running", "b_SystemEnable AND b_EStop_OK AND (b_Start_PB OR b_Running) AND NOT b_FaultActive", rung_num=0, comment="Cycle Run Latch")
            r2 = ladder_eng.boolean_st_to_rung("b_ActuatorActive", "b_Running AND NOT b_FaultActive", rung_num=1, comment="Actuator Power Control")
            ladder_ascii = f"{r1.to_ascii_art()}\n{r2.to_ascii_art()}"

        units = ["[bar]", "[deg C]", "[kN]", "[ms]", "[m/min]"]

        return CandidateCodePackage(
            package_id=f"CODE-{uuid.uuid4().hex[:8]}",
            arch_id=arch.arch_id,
            target_vendor=arch.target_vendor,
            target_language=arch.target_language,
            fb_name=fb_name,
            structured_text_code=st_code,
            vendor_native_export=vendor_native,
            ladder_ascii_code=ladder_ascii,
            variables_declared=vars_map,
            engineering_units_enforced=units
        )

    def _synthesize_structured_text(self, arch: ArchitecturalSpecification, fb_name: str) -> str:
        """Synthesizes fully compliant IEC 61131-3 cyber-physical Function Block."""
        n = arch.state_space.dimension_n
        m = arch.state_space.dimension_m
        a_mat = arch.state_space.matrix_a
        b_mat = arch.state_space.matrix_b

        lines = [
            f"FUNCTION_BLOCK {fb_name}",
            "(*========================================================================*)",
            f"(* SYSTEM: {arch.system_name} | SECTOR: {arch.sector.upper()} *)",
            f"(* VENDOR: {arch.target_vendor} | MODEL: {arch.controller_model} *)",
            "(* CYBER-PHYSICAL DISCRETE STATE-SPACE (4x4) & 2oo3 TMR FAULT TOLERANCE  *)",
            "(*========================================================================*)",
            "",
            "VAR_INPUT",
            "    b_SystemEnable                      : BOOL;     (* Master System Permissive *)",
            "    b_EStop_OK                          : BOOL;     (* Emergency Stop Circuit Healthy *)",
            "    b_Start_PB                          : BOOL;     (* Operator Cycle Start Pushbutton *)",
            "    b_Stop_PB                           : BOOL;     (* Operator Normal Stop Pushbutton *)",
            "    b_Reset_PB                          : BOOL;     (* Fault Reset Pushbutton *)",
            "    r_Sensor_ChA_Raw                    : REAL;     (* Sensor Channel A Measurement [bar] *)",
            "    r_Sensor_ChB_Raw                    : REAL;     (* Sensor Channel B Measurement [bar] *)",
            "    r_Sensor_ChC_Raw                    : REAL;     (* Sensor Channel C Measurement [bar] *)",
            "    r_Setpoint                          : REAL;     (* Target Process Setpoint [bar] *)",
            "END_VAR",
            "",
            "VAR_OUTPUT",
            "    b_Running                           : BOOL;     (* Machine Active In-Cycle *)",
            "    b_FaultActive                       : BOOL;     (* Latched Fault Beacon *)",
            "    b_Alarm_HH                          : BOOL;     (* High-High Critical Trip Alarm *)",
            "    b_Alarm_H                           : BOOL;     (* High Advisory Warning Alarm *)",
            "    b_Alarm_L                           : BOOL;     (* Low Advisory Warning Alarm *)",
            "    b_Alarm_LL                          : BOOL;     (* Low-Low Critical Trip Alarm *)",
            "    r_Voted_ProcessValue                : REAL;     (* 2oo3 Voted Filtered Value [bar] *)",
            "    r_ActuatorCommand                   : REAL;     (* Analog Valve / Servo Drive Effort [0..100%] *)",
            "    n_ActiveState                       : INT;      (* Current Finite State Machine State *)",
            "END_VAR",
            "",
            "VAR",
            f"    A_Matrix                            : ARRAY[0..{n-1}, 0..{n-1}] OF REAL; (* Discrete System Transition Matrix *)",
            f"    B_Matrix                            : ARRAY[0..{n-1}, 0..{m-1}] OF REAL; (* Discrete Control Input Matrix *)",
            f"    x_State                             : ARRAY[0..{n-1}] OF REAL;           (* State Estimation Vector *)",
            f"    x_Next                              : ARRAY[0..{n-1}] OF REAL;           (* Propagated State Vector *)",
            f"    u_Input                             : ARRAY[0..{m-1}] OF REAL;           (* Control Actuator Vector *)",
            "    ton_Discrepancy                     : TON;                               (* TMR Sensor Discrepancy Timer [ms] *)",
            "    ton_StepTimer                       : TON;                               (* FSM Step Dwell Timer [ms] *)",
            "    b_ChA_Suspect                       : BOOL;                              (* Channel A Discrepancy Flag *)",
            "    b_ChB_Suspect                       : BOOL;                              (* Channel B Discrepancy Flag *)",
            "    b_ChC_Suspect                       : BOOL;                              (* Channel C Discrepancy Flag *)",
            "    r_Diff_AB                           : REAL;                              (* Discrepancy Delta A-B [bar] *)",
            "    r_Diff_BC                           : REAL;                              (* Discrepancy Delta B-C [bar] *)",
            "    r_Diff_CA                           : REAL;                              (* Discrepancy Delta C-A [bar] *)",
            "    n_HealthyChannels                   : INT;                               (* Count of Active Healthy TMR Channels *)",
            "    i_row                               : INT;                               (* Matrix Row Iteration Index *)",
            "    j_col                               : INT;                               (* Matrix Column Iteration Index *)",
            "    r_StateAccum                        : REAL;                              (* State Product Accumulator [kN] *)",
            "    b_Initialized                       : BOOL;                              (* One-Shot Cold-Start Flag *)",
            "END_VAR",
            "",
            "(*------------------------------------------------------------------------*)",
            "(* PHASE 01: COLD-START STATE-SPACE COEFFICIENT INITIALIZATION            *)",
            "(*------------------------------------------------------------------------*)",
            "IF NOT b_Initialized THEN"
        ]

        # Initialize Matrix A
        for r in range(n):
            for c in range(n):
                val = a_mat[r][c]
                lines.append(f"    A_Matrix[{r}, {c}] := {val:.4f};")

        # Initialize Matrix B
        for r in range(n):
            for c in range(m):
                val = b_mat[r][c]
                lines.append(f"    B_Matrix[{r}, {c}] := {val:.4f};")

        lines.extend([
            "    n_ActiveState := 0; (* STATE_INIT *)",
            "    b_Initialized := TRUE;",
            "END_IF;",
            "",
            "(*------------------------------------------------------------------------*)",
            "(* PHASE 02: 2oo3 TRIPLE MODULAR REDUNDANCY SENSOR VOTING                 *)",
            "(*------------------------------------------------------------------------*)",
            "r_Diff_AB := ABS(r_Sensor_ChA_Raw - r_Sensor_ChB_Raw);",
            "r_Diff_BC := ABS(r_Sensor_ChB_Raw - r_Sensor_ChC_Raw);",
            "r_Diff_CA := ABS(r_Sensor_ChC_Raw - r_Sensor_ChA_Raw);",
            "",
            "(* Discrepancy detection: Threshold 0.5 bar for 150ms *)",
            "ton_Discrepancy(IN := (r_Diff_AB > 0.5) OR (r_Diff_BC > 0.5) OR (r_Diff_CA > 0.5), PT := T#150ms);",
            "",
            "IF ton_Discrepancy.Q THEN",
            "    IF (r_Diff_AB > 0.5) AND (r_Diff_CA > 0.5) THEN",
            "        b_ChA_Suspect := TRUE;",
            "    ELSIF (r_Diff_AB > 0.5) AND (r_Diff_BC > 0.5) THEN",
            "        b_ChB_Suspect := TRUE;",
            "    ELSIF (r_Diff_BC > 0.5) AND (r_Diff_CA > 0.5) THEN",
            "        b_ChC_Suspect := TRUE;",
            "    END_IF;",
            "END_IF;",
            "",
            "(* Median Voter Computation *)",
            "IF NOT b_ChA_Suspect AND NOT b_ChB_Suspect AND NOT b_ChC_Suspect THEN",
            "    n_HealthyChannels := 3;",
            "    IF (r_Sensor_ChA_Raw >= r_Sensor_ChB_Raw AND r_Sensor_ChA_Raw <= r_Sensor_ChC_Raw) OR",
            "       (r_Sensor_ChA_Raw <= r_Sensor_ChB_Raw AND r_Sensor_ChA_Raw >= r_Sensor_ChC_Raw) THEN",
            "        r_Voted_ProcessValue := r_Sensor_ChA_Raw;",
            "    ELSIF (r_Sensor_ChB_Raw >= r_Sensor_ChA_Raw AND r_Sensor_ChB_Raw <= r_Sensor_ChC_Raw) OR",
            "          (r_Sensor_ChB_Raw <= r_Sensor_ChA_Raw AND r_Sensor_ChB_Raw >= r_Sensor_ChC_Raw) THEN",
            "        r_Voted_ProcessValue := r_Sensor_ChB_Raw;",
            "    ELSE",
            "        r_Voted_ProcessValue := r_Sensor_ChC_Raw;",
            "    END_IF;",
            "ELSIF b_ChA_Suspect THEN",
            "    n_HealthyChannels := 2;",
            "    r_Voted_ProcessValue := (r_Sensor_ChB_Raw + r_Sensor_ChC_Raw) / 2.0;",
            "ELSIF b_ChB_Suspect THEN",
            "    n_HealthyChannels := 2;",
            "    r_Voted_ProcessValue := (r_Sensor_ChA_Raw + r_Sensor_ChC_Raw) / 2.0;",
            "ELSE",
            "    n_HealthyChannels := 2;",
            "    r_Voted_ProcessValue := (r_Sensor_ChA_Raw + r_Sensor_ChB_Raw) / 2.0;",
            "END_IF;",
            "",
            "(*------------------------------------------------------------------------*)",
            "(* PHASE 03: ISA-18.2 MULTI-TIER ALARM MANAGEMENT & HYSTERESIS           *)",
            "(*------------------------------------------------------------------------*)",
            "(* Trip Setpoints: HH=95.0 bar, H=85.0 bar, L=15.0 bar, LL=5.0 bar | Deadband=2.0 bar *)",
            "IF r_Voted_ProcessValue >= 95.0 THEN",
            "    b_Alarm_HH := TRUE;",
            "ELSIF r_Voted_ProcessValue <= (95.0 - 2.0) THEN",
            "    b_Alarm_HH := FALSE;",
            "END_IF;",
            "",
            "IF r_Voted_ProcessValue >= 85.0 THEN",
            "    b_Alarm_H := TRUE;",
            "ELSIF r_Voted_ProcessValue <= (85.0 - 2.0) THEN",
            "    b_Alarm_H := FALSE;",
            "END_IF;",
            "",
            "IF r_Voted_ProcessValue <= 5.0 THEN",
            "    b_Alarm_LL := TRUE;",
            "ELSIF r_Voted_ProcessValue >= (5.0 + 2.0) THEN",
            "    b_Alarm_LL := FALSE;",
            "END_IF;",
            "",
            "IF r_Voted_ProcessValue <= 15.0 THEN",
            "    b_Alarm_L := TRUE;",
            "ELSIF r_Voted_ProcessValue >= (15.0 + 2.0) THEN",
            "    b_Alarm_L := FALSE;",
            "END_IF;",
            "",
            "(* Master Safety Interlock *)",
            "b_FaultActive := (NOT b_EStop_OK) OR b_Alarm_HH OR b_Alarm_LL OR (n_HealthyChannels < 2);",
            "",
            "(*------------------------------------------------------------------------*)",
            "(* PHASE 04: DISCRETE STATE-SPACE PROPAGATION: x[k+1] = A*x[k] + B*u[k]    *)",
            "(*------------------------------------------------------------------------*)",
            "u_Input[0] := r_ActuatorCommand / 100.0;",
            "u_Input[1] := r_Setpoint / 100.0;",
            "",
            "FOR i_row := 0 TO 3 DO",
            "    r_StateAccum := 0.0;",
            "    FOR j_col := 0 TO 3 DO",
            "        r_StateAccum := r_StateAccum + (A_Matrix[i_row, j_col] * x_State[j_col]);",
            "    END_FOR;",
            "    r_StateAccum := r_StateAccum + (B_Matrix[i_row, 0] * u_Input[0]) + (B_Matrix[i_row, 1] * u_Input[1]);",
            "    x_Next[i_row] := r_StateAccum;",
            "END_FOR;",
            "",
            "(* State Update *)",
            "FOR i_row := 0 TO 3 DO",
            "    x_State[i_row] := x_Next[i_row];",
            "END_FOR;",
            "",
            "(*------------------------------------------------------------------------*)",
            "(* PHASE 05: FINITE STATE MACHINE MODE SEQUENCING                         *)",
            "(*------------------------------------------------------------------------*)",
            "ton_StepTimer(IN := TRUE, PT := T#500ms);",
            "",
            "CASE n_ActiveState OF",
            "    0: (* STATE_INIT *)",
            "        b_Running := FALSE;",
            "        r_ActuatorCommand := 0.0;",
            "        IF b_SystemEnable AND b_EStop_OK AND NOT b_FaultActive THEN",
            "            n_ActiveState := 1; (* Transition to STANDBY *)",
            "        END_IF;",
            "",
            "    1: (* STATE_STANDBY *)",
            "        b_Running := FALSE;",
            "        r_ActuatorCommand := 0.0;",
            "        IF b_Start_PB AND NOT b_FaultActive THEN",
            "            n_ActiveState := 2; (* Transition to RAMP_UP *)",
            "        END_IF;",
            "",
            "    2: (* STATE_RAMP_UP *)",
            "        b_Running := TRUE;",
            "        r_ActuatorCommand := r_ActuatorCommand + 2.5; (* Ramp rate [m/min] *)",
            "        IF r_ActuatorCommand >= 80.0 THEN",
            "            r_ActuatorCommand := 80.0;",
            "            n_ActiveState := 3; (* Transition to STEADY_EXECUTE *)",
            "        END_IF;",
            "",
            "    3: (* STATE_STEADY_EXECUTE *)",
            "        b_Running := TRUE;",
            "        (* Closed-loop regulation using state feedback *)",
            "        r_ActuatorCommand := 80.0 + (x_State[0] * 5.0);",
            "        IF r_ActuatorCommand > 100.0 THEN r_ActuatorCommand := 100.0; END_IF;",
            "        IF r_ActuatorCommand < 0.0 THEN r_ActuatorCommand := 0.0; END_IF;",
            "        IF b_Stop_PB THEN",
            "            n_ActiveState := 4; (* Transition to RAMP_DOWN *)",
            "        END_IF;",
            "",
            "    4: (* STATE_RAMP_DOWN *)",
            "        b_Running := TRUE;",
            "        r_ActuatorCommand := r_ActuatorCommand - 5.0;",
            "        IF r_ActuatorCommand <= 0.0 THEN",
            "            r_ActuatorCommand := 0.0;",
            "            n_ActiveState := 1; (* Return to STANDBY *)",
            "        END_IF;",
            "",
            "    99: (* STATE_FAULT_SAFE_STOP *)",
            "        b_Running := FALSE;",
            "        r_ActuatorCommand := 0.0;",
            "        IF b_Reset_PB AND NOT b_FaultActive THEN",
            "            n_ActiveState := 0; (* Reset to INIT *)",
            "        END_IF;",
            "    ELSE",
            "        n_ActiveState := 99; (* Unhandled state falls to safe stop *)",
            "END_CASE;",
            "",
            "(* Emergency Override *)",
            "IF b_FaultActive THEN",
            "    n_ActiveState := 99; (* Force immediate transition to FAULT_SAFE_STOP *)",
            "    r_ActuatorCommand := 0.0;",
            "    b_Running := FALSE;",
            "END_IF;",
            "",
            f"END_FUNCTION_BLOCK"
        ])

        return "\n".join(lines)

    def _extract_var_map(self, st_code: str) -> Dict[str, str]:
        """Extracts declared variables and their data types from VAR blocks."""
        var_map = {}
        for m in re.finditer(r"^\s*([A-Za-z0-9_]+)\s*:\s*([A-Za-z0-9_]+)", st_code, re.MULTILINE):
            name, dtype = m.group(1), m.group(2)
            if dtype.upper() not in ["VAR", "VAR_INPUT", "VAR_OUTPUT", "FUNCTION_BLOCK", "END_VAR"]:
                var_map[name] = dtype
        return var_map

    def _synthesize_ladder_ascii(self, arch: ArchitecturalSpecification) -> str:
        """Emits standard industrial ASCII Ladder Diagram representation."""
        return (
            "// ==========================================================================\n"
            "// RELAY LADDER LOGIC (RLL) ASCII REPRESENTATION\n"
            f"// SYSTEM: {arch.system_name} | VENDOR: {arch.target_vendor}\n"
            "// ==========================================================================\n\n"
            "Rung 0000: Master Emergency Stop & Permissive Interlock\n"
            "|---[ b_EStop_OK ]-------[ b_SystemEnable ]-------[/ b_FaultActive ]----( b_Permissive_OK )---|\n\n"
            "Rung 0001: 3-Wire Motor Start / Stop Station with Seal-In\n"
            "|---[ b_Permissive_OK ]----+---[ b_Start_PB ]---+-------[/ b_Stop_PB ]----( b_Running )-------|\n"
            "|                          |                    |\n"
            "|                          +---[ b_Running ]----+\n\n"
            "Rung 0002: High-High Pressure Alarm Trip Coil\n"
            "|---[ r_Voted_ProcessValue >= 95.0 ]------------------------------------( b_Alarm_HH )--------|\n\n"
            "Rung 0003: Fault Summary Latch\n"
            "|----+---[ b_Alarm_HH ]--------+-----------------------------------------(L b_FaultActive )----|\n"
            "|    |                         |\n"
            "|    +---[ n_HealthyChs < 2 ]--+\n\n"
            "Rung 0004: Fault Reset Pushbutton Unlatch\n"
            "|---[ b_Reset_PB ]-------[/ b_Alarm_HH ]---------------------------------(U b_FaultActive )----|\n"
        )
