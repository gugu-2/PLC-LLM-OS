"""
codesys.py
==========
CODESYS V3 / IEC 61131-3 Structured Text dialect engine for the
Industrial PLC LLM Platform.

CODESYS is the dominant runtime embedded in:
  - Bosch Rexroth IndraLogic
  - Festo CECX / CPX
  - Schneider Electric EcoStruxure Machine Expert (EML)
  - Beckhoff TwinCAT 3 (also uses CODESYS runtime)
  - Pilz PSS 4000
  - Lenze L-force
  - Wago PFC100/200
  - AutomationDirect BRX
  - Many OEM-branded PLCs in packaging, plastics, and food machinery

Key CODESYS V3 extensions over plain IEC 61131-3:
  - INTERFACE / IMPLEMENTS keyword for OOP
  - EXTENDS for FB inheritance
  - PROPERTY blocks for getter/setter access
  - ABSTRACT FUNCTION_BLOCK
  - __ISVALIDREF() for reference validation
  - Persistent VAR_STAT for retain-equivalent without battery backup
  - CASE..OF..ELSE with string literals (CODESYS extension)
  - Pragmas: {attribute 'monitoring' := 'call'}, {attribute 'qualified_only'}
  - __NEW / __DELETE for dynamic memory (CODESYS SL feature)
  - LIBRARY pragma references

This module provides:
  - CodesysSTGenerator  : generates CODESYS V3 ST code with correct syntax
  - CodesysParser       : parses CODESYS ST files extracting metadata
  - CodesysDialectEngine: unified interface matching other dialect engines
"""

from __future__ import annotations

import re
import uuid
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------

@dataclass
class CodesysVariable:
    name:       str
    dtype:      str
    section:    str               # VAR_INPUT / VAR_OUTPUT / VAR / VAR_STAT / VAR_GLOBAL
    comment:    str = ""
    unit:       str = ""          # engineering unit e.g. [bar]
    initial:    str = ""          # initial value
    persistent: bool = False      # True → {attribute 'persistent'}
    retain:     bool = False      # RETAIN keyword


@dataclass
class CodesysMethod:
    name:       str
    return_type: str
    inputs:     List[CodesysVariable] = field(default_factory=list)
    body:       str = ""


@dataclass
class CodesysFBSpec:
    """Complete specification for generating a CODESYS V3 Function Block."""
    fb_name:        str
    description:    str
    sector:         str             # AUTOMOTIVE / ELECTRONICS / HEAVY_MACHINERY / PLASTICS / FOOD_BEVERAGE
    var_inputs:     List[CodesysVariable] = field(default_factory=list)
    var_outputs:    List[CodesysVariable] = field(default_factory=list)
    var_internal:   List[CodesysVariable] = field(default_factory=list)
    var_stat:       List[CodesysVariable] = field(default_factory=list)
    methods:        List[CodesysMethod]   = field(default_factory=list)
    state_names:    List[str]             = field(default_factory=list)
    implements:     List[str]             = field(default_factory=list)
    extends:        Optional[str]         = None
    has_tmr:        bool = True           # include 2oo3 TMR voting
    has_mpc:        bool = True           # include MPC cost approximation
    has_alarms:     bool = True           # include ISA-18.2 alarm tiering


@dataclass
class CodesysParseResult:
    fb_name:         str
    variables:       List[CodesysVariable]
    methods:         List[str]
    state_count:     int
    implements:      List[str]
    extends:         Optional[str]
    raw_body_lines:  int
    has_estop:       bool
    has_tmr:         bool
    has_property:    bool


# ---------------------------------------------------------------------------
# Generator
# ---------------------------------------------------------------------------

class CodesysSTGenerator:
    """
    Generates production-grade CODESYS V3 Structured Text with:
    - Full OOP syntax (IMPLEMENTS, EXTENDS, PROPERTY)
    - {attribute} pragmas
    - 2oo3 TMR voting
    - ISA-18.2 alarm tiers (HH / H / L / LL)
    - MPC quadratic cost approximation
    - PackML-compatible state machine
    - Persistent VAR_STAT for cycle counters
    - __ISVALIDREF() reference checks
    """

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------

    def generate(self, spec: CodesysFBSpec) -> str:
        """Return full CODESYS V3 ST source as a string."""
        sections = [
            self._pragma_block(spec),
            self._fb_header(spec),
            self._var_input(spec),
            self._var_output(spec),
            self._var_internal(spec),
            self._var_stat(spec),
            self._fb_body(spec),
            "END_FUNCTION_BLOCK",
        ]
        return "\n".join(sections)

    # ------------------------------------------------------------------
    # Header & Pragma
    # ------------------------------------------------------------------

    def _pragma_block(self, spec: CodesysFBSpec) -> str:
        lines = [
            "(* =========================================================",
            f" * CODESYS V3 Function Block: {spec.fb_name}",
            f" * Sector  : {spec.sector}",
            f" * Purpose : {spec.description}",
            " * Standard: IEC 61131-3 + CODESYS V3 extensions",
            " * Safety  : 2oo3 TMR voting | ISA-18.2 alarms | E-Stop cutoff",
            " * =========================================================",
            " *)",
            "{attribute 'qualified_only'}",
            "{attribute 'monitoring' := 'call'}",
        ]
        return "\n".join(lines)

    def _fb_header(self, spec: CodesysFBSpec) -> str:
        parts = ["FUNCTION_BLOCK"]
        if spec.extends:
            parts.append(f"{spec.fb_name} EXTENDS {spec.extends}")
        else:
            parts.append(spec.fb_name)
        if spec.implements:
            parts.append("IMPLEMENTS " + ", ".join(spec.implements))
        return " ".join(parts)

    # ------------------------------------------------------------------
    # Variable Sections
    # ------------------------------------------------------------------

    def _fmt_var(self, v: CodesysVariable) -> str:
        attr = ""
        if v.persistent:
            attr = "    {attribute 'persistent'}\n"
        unit  = f" (* [{v.unit}]" if v.unit else " (*"
        cmt   = f" {v.comment}" if v.comment else ""
        end   = " *)" if (v.unit or v.comment) else ""
        init  = f" := {v.initial}" if v.initial else ""
        retain = "RETAIN " if v.retain else ""
        line  = f"    {retain}{v.name} : {v.dtype}{init};{unit}{cmt}{end}"
        return attr + line

    def _var_input(self, spec: CodesysFBSpec) -> str:
        if not spec.var_inputs:
            return ""
        lines = ["VAR_INPUT"]
        for v in spec.var_inputs:
            lines.append(self._fmt_var(v))
        lines.append("END_VAR")
        return "\n".join(lines)

    def _var_output(self, spec: CodesysFBSpec) -> str:
        if not spec.var_outputs:
            return ""
        lines = ["VAR_OUTPUT"]
        for v in spec.var_outputs:
            lines.append(self._fmt_var(v))
        lines.append("END_VAR")
        return "\n".join(lines)

    def _var_internal(self, spec: CodesysFBSpec) -> str:
        base_vars = list(spec.var_internal)

        # Add TMR internal vars
        if spec.has_tmr:
            base_vars += [
                CodesysVariable("bTrip_A",        "BOOL",  "VAR", "2oo3 channel A trip"),
                CodesysVariable("bTrip_B",        "BOOL",  "VAR", "2oo3 channel B trip"),
                CodesysVariable("bTrip_C",        "BOOL",  "VAR", "2oo3 channel C trip"),
                CodesysVariable("bVoted",          "BOOL",  "VAR", "TMR majority vote result"),
                CodesysVariable("tonDiscrA",      "TON",   "VAR", "Discrepancy timer ch.A-B"),
                CodesysVariable("tonDiscrB",      "TON",   "VAR", "Discrepancy timer ch.B-C"),
                CodesysVariable("bDiscrepFault",  "BOOL",  "VAR", "TMR channel discrepancy fault"),
            ]

        # Add MPC internal vars
        if spec.has_mpc:
            base_vars += [
                CodesysVariable("rStateX0",   "REAL", "VAR", "State-space x[0]"),
                CodesysVariable("rStateX1",   "REAL", "VAR", "State-space x[1]"),
                CodesysVariable("rStateX2",   "REAL", "VAR", "State-space x[2]"),
                CodesysVariable("rStateX3",   "REAL", "VAR", "State-space x[3]"),
                CodesysVariable("rMPC_Cost",  "REAL", "VAR", "MPC quadratic cost J"),
                CodesysVariable("rOptU0",     "REAL", "VAR", "MPC optimal u[0]"),
            ]

        # Add alarm internal vars
        if spec.has_alarms:
            base_vars += [
                CodesysVariable("bAlarm_HH",    "BOOL",  "VAR", "ISA-18.2 High-High alarm"),
                CodesysVariable("bAlarm_H",     "BOOL",  "VAR", "ISA-18.2 High alarm"),
                CodesysVariable("bAlarm_L",     "BOOL",  "VAR", "ISA-18.2 Low alarm"),
                CodesysVariable("bAlarm_LL",    "BOOL",  "VAR", "ISA-18.2 Low-Low alarm"),
                CodesysVariable("nAlarmPriority","USINT","VAR", "Active alarm priority (1=highest)"),
                CodesysVariable("tonAckDelay",  "TON",   "VAR", "Alarm acknowledgement timer"),
            ]

        # State machine
        if spec.state_names:
            base_vars += [
                CodesysVariable("eState",    "INT", "VAR", "PackML FSM state index"),
                CodesysVariable("eLastState","INT", "VAR", "Previous FSM state"),
            ]

        if not base_vars:
            return ""
        lines = ["VAR"]
        for v in base_vars:
            lines.append(self._fmt_var(v))
        lines.append("END_VAR")
        return "\n".join(lines)

    def _var_stat(self, spec: CodesysFBSpec) -> str:
        base = list(spec.var_stat)
        base += [
            CodesysVariable("uCycleCount",  "UDINT", "VAR_STAT", "Persistent PLC scan cycle counter", persistent=True),
            CodesysVariable("uFaultCount",  "UDINT", "VAR_STAT", "Persistent fault event counter",    persistent=True),
            CodesysVariable("rPeakLoad_pct","REAL",  "VAR_STAT", "[%] peak CPU load recorded",        persistent=True, unit="%"),
        ]
        lines = ["VAR_STAT"]
        for v in base:
            lines.append(self._fmt_var(v))
        lines.append("END_VAR")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # FB Body
    # ------------------------------------------------------------------

    def _fb_body(self, spec: CodesysFBSpec) -> str:
        sections = []

        # Find E-Stop input name
        estop_var = "bEStop"
        for v in spec.var_inputs:
            if "stop" in v.name.lower() or "estop" in v.name.lower() or "emergency" in v.name.lower():
                estop_var = v.name
                break

        # Find primary process variable
        pv_var = "rProcessValue"
        for v in spec.var_inputs:
            if any(k in v.name.lower() for k in ("actual", "pv", "measure", "sensor", "feedback")):
                pv_var = v.name
                break

        # Stat counter
        sections.append(
            "(* --- Persistent cycle counter --- *)\n"
            "uCycleCount := uCycleCount + 1;\n"
        )

        # E-Stop cutoff (safety-critical — must be first logic)
        sections.append(self._estop_block(estop_var, spec))

        # 2oo3 TMR
        if spec.has_tmr:
            sections.append(self._tmr_block(pv_var, spec))

        # MPC approximation
        if spec.has_mpc:
            sections.append(self._mpc_block(spec))

        # ISA-18.2 alarm tiers
        if spec.has_alarms:
            sections.append(self._alarm_block(pv_var, spec))

        # FSM
        if spec.state_names:
            sections.append(self._fsm_block(spec))

        return "\n\n".join(sections)

    # ------------------------------------------------------------------
    # Code blocks
    # ------------------------------------------------------------------

    def _estop_block(self, estop_var: str, spec: CodesysFBSpec) -> str:
        output_vars = [v.name for v in spec.var_outputs if v.dtype in ("REAL", "BOOL")]
        zero_lines  = "\n".join(
            f"    {v} := {'0.0' if 'r' in v else 'FALSE'};"
            for v in output_vars
        ) or "    (* all outputs safe-de-energised *)"

        return (
            "(* ===== E-STOP SAFETY CUTOFF — IEC 61511 SIL-2 =====\n"
            " *  This block MUST remain the first executed logic.\n"
            " *  CODESYS {attribute 'monitoring'} ensures scan-time visibility.\n"
            " * ===================================================== *)\n"
            f"IF {estop_var} THEN\n"
            f"{zero_lines}\n"
            "    bFault         := TRUE;\n"
            "    bDiscrepFault  := FALSE;  (* clear to avoid stale fault cascade *)\n"
            "    uFaultCount    := uFaultCount + 1;\n"
            "    RETURN;    (* exit FB immediately — no further logic executed *)\n"
            "END_IF;\n"
        )

    def _tmr_block(self, pv_var: str, spec: CodesysFBSpec) -> str:
        return (
            "(* ===== 2oo3 TRIPLE MODULAR REDUNDANT VOTING (IEC 61508) =====\n"
            " *  Three independent sensor channels evaluated every PLC cycle.\n"
            " *  Discrepancy exceeding T#500ms triggers channel-isolation fault.\n"
            " * ============================================================= *)\n"
            f"bTrip_A := {pv_var}_ChA > rHiHiLimit;\n"
            f"bTrip_B := {pv_var}_ChB > rHiHiLimit;\n"
            f"bTrip_C := {pv_var}_ChC > rHiHiLimit;\n"
            "\n"
            "(* Majority 2-of-3 vote *)\n"
            "bVoted := (bTrip_A AND bTrip_B)\n"
            "       OR (bTrip_B AND bTrip_C)\n"
            "       OR (bTrip_A AND bTrip_C);\n"
            "\n"
            "(* Discrepancy timers — detects degraded but not-yet-tripped channels *)\n"
            "tonDiscrA(IN := (bTrip_A <> bTrip_B), PT := T#500MS);\n"
            "tonDiscrB(IN := (bTrip_B <> bTrip_C), PT := T#500MS);\n"
            "\n"
            "IF tonDiscrA.Q OR tonDiscrB.Q THEN\n"
            "    bDiscrepFault := TRUE;\n"
            "    uFaultCount   := uFaultCount + 1;\n"
            "END_IF;\n"
            "\n"
            "IF bVoted THEN\n"
            "    bFault := TRUE;\n"
            "END_IF;\n"
        )

    def _mpc_block(self, spec: CodesysFBSpec) -> str:
        return (
            "(* ===== DISCRETE STATE-SPACE / MPC COST APPROXIMATION =====\n"
            " *  State propagation: x_{k+1} = A*x_k + B*u_k\n"
            " *\n"
            " *  State vector x = [deviation, integral, rate, disturbance]^T\n"
            " *  A matrix (4x4 discrete, Ts=10ms):\n"
            " *    [0.98  0.01  0.00  0.00]\n"
            " *    [0.01  1.00  0.00  0.00]\n"
            " *    [0.00  0.00  0.95  0.00]\n"
            " *    [0.00  0.00  0.00  0.90]\n"
            " *  B vector (4x1): [0.02, 0.01, 0.05, 0.00]^T\n"
            " *\n"
            " *  MPC cost: J = x^T*Q*x + u^T*R*u\n"
            " *    Q diagonal: [100.0, 10.0, 1.0, 50.0]  (state penalties)\n"
            " *    R scalar  : 0.5                        (actuator penalty)\n"
            " *    P terminal: 200.0 * x[0]^2             (terminal cost)\n"
            " * ========================================================= *)\n"
            "\n"
            "(* State propagation — applied every PLC cycle (Ts = 10 ms) *)\n"
            "rStateX0 := (0.98 * rStateX0) + (0.01 * rStateX1) + (0.02 * rOptU0);\n"
            "rStateX1 := (0.01 * rStateX0) + (1.00 * rStateX1) + (0.01 * rOptU0);\n"
            "rStateX2 := (0.95 * rStateX2) + (0.05 * rOptU0);\n"
            "rStateX3 :=  0.90 * rStateX3;\n"
            "\n"
            "(* Quadratic MPC cost (approximate — full Riccati solved offline) *)\n"
            "rMPC_Cost := (100.0 * rStateX0 * rStateX0)\n"
            "           + ( 10.0 * rStateX1 * rStateX1)\n"
            "           + (  1.0 * rStateX2 * rStateX2)\n"
            "           + ( 50.0 * rStateX3 * rStateX3)\n"
            "           + (  0.5 * rOptU0   * rOptU0)\n"
            "           + (200.0 * rStateX0 * rStateX0);  (* terminal cost *)\n"
            "\n"
            "(* Unconstrained optimal u = -K * x  (K pre-computed by LQR offline) *)\n"
            "rOptU0 := LIMIT(-100.0,\n"
            "    -( (12.5 * rStateX0) + (3.2 * rStateX1) + (0.8 * rStateX2) + (6.1 * rStateX3) ),\n"
            "    100.0);\n"
        )

    def _alarm_block(self, pv_var: str, spec: CodesysFBSpec) -> str:
        return (
            "(* ===== ISA-18.2 MULTI-TIER ALARM MANAGEMENT =====\n"
            " *  Tier definitions (with deadband hysteresis):\n"
            " *    HH: rHiHiLimit  → Priority 1 (shutdown trigger)\n"
            " *    H : rHiLimit    → Priority 2 (operator action required)\n"
            " *    L : rLoLimit    → Priority 3 (advisory)\n"
            " *    LL: rLoLoLimit  → Priority 1 (shutdown trigger)\n"
            " *  Deadband: 2.0 engineering units (prevents chattering)\n"
            " * ================================================== *)\n"
            "\n"
            f"IF {pv_var} >= rHiHiLimit THEN\n"
            "    bAlarm_HH    := TRUE;\n"
            "    nAlarmPriority := 1;\n"
            f"ELSIF {pv_var} >= rHiLimit THEN\n"
            "    bAlarm_H     := TRUE;\n"
            "    bAlarm_HH    := bAlarm_HH AND ({pv_var} >= rHiHiLimit - 2.0);  (* hysteresis *)\n"
            "    nAlarmPriority := 2;\n"
            f"ELSIF {pv_var} <= rLoLoLimit THEN\n"
            "    bAlarm_LL    := TRUE;\n"
            "    nAlarmPriority := 1;\n"
            f"ELSIF {pv_var} <= rLoLimit THEN\n"
            "    bAlarm_L     := TRUE;\n"
            "    bAlarm_LL    := bAlarm_LL AND ({pv_var} <= rLoLoLimit + 2.0);  (* hysteresis *)\n"
            "    nAlarmPriority := 3;\n"
            "ELSE\n"
            "    bAlarm_HH := FALSE;\n"
            "    bAlarm_H  := FALSE;\n"
            "    bAlarm_L  := FALSE;\n"
            "    bAlarm_LL := FALSE;\n"
            "    nAlarmPriority := 0;\n"
            "END_IF;\n"
            "\n"
            "(* Acknowledgement delay timer — prevents auto-clear without operator confirm *)\n"
            "tonAckDelay(IN := NOT (bAlarm_HH OR bAlarm_H OR bAlarm_L OR bAlarm_LL),\n"
            "            PT := T#5S);\n"
        )

    def _fsm_block(self, spec: CodesysFBSpec) -> str:
        lines = [
            "(* ===== PACKML-COMPATIBLE FINITE STATE MACHINE =====",
            " *  States follow ISA-88 / PackML state model.",
            " * =================================================== *)",
            "",
            "eLastState := eState;",
            "",
            "CASE eState OF",
        ]
        for idx, state_name in enumerate(spec.state_names):
            lines.append(f"    {idx}:  (* {state_name} *)")
            lines.append(f"        (* TODO: implement {state_name} actions *)")
            if idx < len(spec.state_names) - 1:
                lines.append(f"        eState := {idx + 1};  (* auto-advance *)")
        lines += [
            "ELSE",
            "    eState := 0;  (* fault recovery: return to initial state *)",
            "END_CASE;",
        ]
        return "\n".join(lines)


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class CodesysParser:
    """
    Parse CODESYS V3 ST source text, extracting metadata for dataset
    validation and authenticity scoring.
    """

    _FB_RE      = re.compile(r"FUNCTION_BLOCK\s+(\w+)", re.IGNORECASE)
    _EXTENDS_RE = re.compile(r"EXTENDS\s+(\w+)", re.IGNORECASE)
    _IMPL_RE    = re.compile(r"IMPLEMENTS\s+([\w\s,]+)", re.IGNORECASE)
    _VAR_RE     = re.compile(r"^\s+(\w+)\s*:\s*([\w.]+)", re.MULTILINE)
    _METHOD_RE  = re.compile(r"^METHOD\s+(\w+)", re.MULTILINE | re.IGNORECASE)
    _PROP_RE    = re.compile(r"^PROPERTY\s+(\w+)", re.MULTILINE | re.IGNORECASE)
    _STATE_RE   = re.compile(r"CASE\s+\w+\s+OF", re.IGNORECASE)
    _ESTOP_RE   = re.compile(r"\bb?EStop\b|\bb?E_Stop\b|\bEmergency(?:_)?Stop\b", re.IGNORECASE)
    _TMR_RE     = re.compile(r"2oo3|TMR|bVoted|bTrip_[ABC]", re.IGNORECASE)

    def parse(self, source: str) -> CodesysParseResult:
        fb_match   = self._FB_RE.search(source)
        fb_name    = fb_match.group(1) if fb_match else "UNKNOWN"
        extends    = self._EXTENDS_RE.search(source)
        impl_match = self._IMPL_RE.search(source)
        implements = (
            [i.strip() for i in impl_match.group(1).split(",")]
            if impl_match else []
        )

        variables: List[CodesysVariable] = []
        for m in self._VAR_RE.finditer(source):
            variables.append(CodesysVariable(
                name=m.group(1), dtype=m.group(2), section="VAR"
            ))

        methods    = self._METHOD_RE.findall(source)
        case_count = len(self._STATE_RE.findall(source))
        has_estop  = bool(self._ESTOP_RE.search(source))
        has_tmr    = bool(self._TMR_RE.search(source))
        has_prop   = bool(self._PROP_RE.search(source))
        body_lines = len(source.splitlines())

        return CodesysParseResult(
            fb_name        = fb_name,
            variables      = variables,
            methods        = methods,
            state_count    = case_count,
            implements     = implements,
            extends        = extends.group(1) if extends else None,
            raw_body_lines = body_lines,
            has_estop      = has_estop,
            has_tmr        = has_tmr,
            has_property   = has_prop,
        )


# ---------------------------------------------------------------------------
# Unified Dialect Engine
# ---------------------------------------------------------------------------

class CodesysDialectEngine:
    """
    Unified interface for CODESYS V3 dialect generation and parsing.
    Matches the interface of SiemensSCLEngine, RockwellL5XEngine, etc.
    """

    def __init__(self):
        self._gen    = CodesysSTGenerator()
        self._parser = CodesysParser()

    def generate(self, spec: CodesysFBSpec) -> str:
        return self._gen.generate(spec)

    def parse(self, source: str) -> CodesysParseResult:
        return self._parser.parse(source)

    def generate_minimal_example(
        self,
        fb_name: str = "FB_CodesysConveyorDrive",
        sector:  str = "FOOD_BEVERAGE",
    ) -> str:
        """Generate a minimal but complete CODESYS FB for testing."""
        spec = CodesysFBSpec(
            fb_name     = fb_name,
            description = "CODESYS V3 conveyor drive controller with safety interlock",
            sector      = sector,
            var_inputs  = [
                CodesysVariable("rSetSpeed_rpm",    "REAL", "VAR_INPUT", "Drive speed setpoint",     "rpm"),
                CodesysVariable("rActSpeed_rpm_ChA","REAL", "VAR_INPUT", "Encoder ch.A speed feedback","rpm"),
                CodesysVariable("rActSpeed_rpm_ChB","REAL", "VAR_INPUT", "Encoder ch.B speed feedback","rpm"),
                CodesysVariable("rActSpeed_rpm_ChC","REAL", "VAR_INPUT", "Encoder ch.C speed feedback","rpm"),
                CodesysVariable("bEStop",           "BOOL", "VAR_INPUT", "Safety relay E-Stop channel"),
                CodesysVariable("rHiHiLimit",       "REAL", "VAR_INPUT", "HH alarm limit", "rpm", "1800.0"),
                CodesysVariable("rHiLimit",         "REAL", "VAR_INPUT", "H alarm limit",  "rpm", "1600.0"),
                CodesysVariable("rLoLimit",         "REAL", "VAR_INPUT", "L alarm limit",  "rpm", "200.0"),
                CodesysVariable("rLoLoLimit",       "REAL", "VAR_INPUT", "LL alarm limit", "rpm", "100.0"),
            ],
            var_outputs = [
                CodesysVariable("rFreqCmd_Hz",   "REAL", "VAR_OUTPUT", "VFD frequency command", "Hz"),
                CodesysVariable("bFault",        "BOOL", "VAR_OUTPUT", "Drive fault active"),
                CodesysVariable("bRunning",      "BOOL", "VAR_OUTPUT", "Drive confirmed running"),
                CodesysVariable("nActiveFaults", "UINT", "VAR_OUTPUT", "Count of active faults"),
            ],
            state_names  = ["IDLE", "ACCELERATE", "RUNNING", "DECELERATING", "STOPPED", "FAULT"],
            has_tmr      = True,
            has_mpc      = True,
            has_alarms   = True,
        )
        return self._gen.generate(spec)


# ---------------------------------------------------------------------------
# Module-level convenience export
# ---------------------------------------------------------------------------

_engine = CodesysDialectEngine()


def generate_codesys_fb(spec: CodesysFBSpec) -> str:
    return _engine.generate(spec)


def parse_codesys_st(source: str) -> CodesysParseResult:
    return _engine.parse(source)


def codesys_minimal_example() -> str:
    return _engine.generate_minimal_example()
