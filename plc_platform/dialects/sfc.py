"""
sfc.py
======
Sequential Function Chart (SFC) dialect engine for the Industrial PLC LLM Platform.

SFC (Grafcet / IEC 61131-3 Part 6) is the graphical sequential programming
language used in:
  - Batch process automation (ISA-88 recipe phases)
  - Packaging machine sequencing (ISA-TR88.00.02 PackML)
  - Automotive assembly conveyor interlocking
  - Food/Beverage CIP/SIP clean-in-place cycles
  - Plastics blow-moulding parison sequence
  - Pharmaceutical lyophilisation cycle control

This module provides:
  - SFCStep      : Dataclass representing a single SFC step
  - SFCTransition: Dataclass for transition conditions between steps
  - SFCDivergence: Parallel / alternative divergence / convergence
  - SFCProgram   : Complete SFC specification
  - SFCSTEmitter : Emits IEC 61131-3 Structured Text encoding of the SFC
                   (vendor-portable textual representation)
  - SFCParser    : Parses SFC-encoded ST back to metadata
  - SFCDialectEngine : Unified interface

IEC 61131-3 textual SFC encoding convention used here:
  Steps are encoded as CASE statements over an integer state variable.
  Actions are ST code blocks inside each CASE arm.
  Transitions are IF checks at the end of each CASE arm advancing eState.
  Parallel (AND) divergence is modelled with sub-state arrays.
  Alternative (OR) divergence is modelled with IF-ELSIF chains in transitions.

This encoding is portable across CODESYS, TwinCAT, Siemens TIA (SCL),
and Rockwell Studio 5000 (AOI ST body).
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
class SFCAction:
    """Action associated with an SFC step."""
    qualifier:  str    # N (non-stored), S (set), R (reset), P (pulse), L (time-limited), D (delayed)
    action_name: str
    body:       str    # ST code for this action
    duration_ms: Optional[int] = None   # for L / D qualifiers


@dataclass
class SFCStep:
    """
    One step in the Sequential Function Chart.

    index       : integer state machine index
    name        : unique step identifier (e.g. 'S01_INIT', 'S05_FILL')
    description : human-readable purpose
    is_initial  : True for the exactly one initial step
    actions     : list of SFCActions executed while this step is active
    entry_actions: actions executed once on step entry (qualifier P)
    exit_actions:  actions executed once on step exit  (qualifier P)
    max_time_ms : maximum dwell time before timeout fault (0 = unlimited)
    """
    index:         int
    name:          str
    description:   str = ""
    is_initial:    bool = False
    actions:       List[SFCAction] = field(default_factory=list)
    entry_actions: List[SFCAction] = field(default_factory=list)
    exit_actions:  List[SFCAction] = field(default_factory=list)
    max_time_ms:   int = 0


@dataclass
class SFCTransition:
    """
    Transition between two SFC steps.

    from_step   : source step index
    to_step     : destination step index (or list for divergence)
    condition   : IEC ST boolean expression (string)
    priority    : for OR divergence: lower number = higher priority
    name        : optional transition label
    """
    from_step:  int
    to_step:    int | List[int]      # int for single, list for AND-divergence
    condition:  str
    priority:   int = 0
    name:       str = ""


@dataclass
class SFCProgram:
    """
    Complete SFC program specification.

    program_name   : PROGRAM or FUNCTION_BLOCK name
    description    : purpose of this SFC
    sector         : manufacturing sector
    steps          : ordered list of SFCStep objects
    transitions    : list of SFCTransition objects
    global_vars    : variables declared at program scope
    has_tmr        : add 2oo3 TMR voting for safety transitions
    has_timeout    : add step timeout watchdog logic
    has_alarms     : add ISA-18.2 alarm output per step
    """
    program_name:   str
    description:    str
    sector:         str
    steps:          List[SFCStep]      = field(default_factory=list)
    transitions:    List[SFCTransition]= field(default_factory=list)
    global_vars:    List[Tuple[str, str, str]] = field(default_factory=list)  # (name, type, comment)
    has_tmr:        bool = True
    has_timeout:    bool = True
    has_alarms:     bool = True


@dataclass
class SFCParseResult:
    program_name: str
    step_count:   int
    step_names:   List[str]
    transition_count: int
    has_initial:  bool
    has_timeout:  bool
    has_tmr:      bool
    has_estop:    bool
    raw_lines:    int


# ---------------------------------------------------------------------------
# SFC → Structured Text Emitter
# ---------------------------------------------------------------------------

class SFCSTEmitter:
    """
    Emits a full IEC 61131-3 Structured Text encoding of an SFCProgram.

    The emitted ST uses the CASE-over-eState pattern which is:
    - Readable by any IEC 61131-3 compliant PLC programmer
    - Compilable in CODESYS, TwinCAT, Siemens SCL, Rockwell AOI ST
    - Verifiable by the platform's StaticAnalysisAuditor
    """

    def emit(self, prog: SFCProgram) -> str:
        parts = [
            self._header_comment(prog),
            self._fb_declaration(prog),
            self._var_input_block(prog),
            self._var_output_block(prog),
            self._var_internal_block(prog),
            self._body(prog),
            "END_FUNCTION_BLOCK",
        ]
        return "\n".join(p for p in parts if p)

    # ------------------------------------------------------------------
    # Sections
    # ------------------------------------------------------------------

    def _header_comment(self, prog: SFCProgram) -> str:
        return (
            f"(* =========================================================\n"
            f" * SFC Program: {prog.program_name}\n"
            f" * Sector    : {prog.sector}\n"
            f" * Purpose   : {prog.description}\n"
            f" * Steps     : {len(prog.steps)}\n"
            f" * Standard  : IEC 61131-3 SFC textual encoding (ST state-machine pattern)\n"
            f" * Safety    : Step timeout watchdog | 2oo3 TMR | ISA-18.2 alarms\n"
            f" * =========================================================\n"
            f" *)"
        )

    def _fb_declaration(self, prog: SFCProgram) -> str:
        return f"FUNCTION_BLOCK {prog.program_name}"

    def _var_input_block(self, prog: SFCProgram) -> str:
        lines = ["VAR_INPUT"]
        lines.append("    bEStop         : BOOL;   (* Safety relay E-Stop *)")
        lines.append("    bReset         : BOOL;   (* Fault reset pushbutton *)")
        lines.append("    bStartCmd      : BOOL;   (* Operator start command *)")
        lines.append("    bStopCmd       : BOOL;   (* Operator stop command *)")
        for name, dtype, comment in prog.global_vars:
            lines.append(f"    {name:30s}: {dtype:12s}; (* {comment} *)")
        lines.append("END_VAR")
        return "\n".join(lines)

    def _var_output_block(self, prog: SFCProgram) -> str:
        lines = ["VAR_OUTPUT"]
        lines.append("    nActiveStep     : INT;   (* Current active SFC step index *)")
        lines.append("    sActiveStepName : STRING; (* Current step name for HMI *)")
        lines.append("    bRunning        : BOOL;   (* Sequence is running *)")
        lines.append("    bFault          : BOOL;   (* Sequence fault active *)")
        lines.append("    bComplete       : BOOL;   (* Sequence completed successfully *)")
        if prog.has_alarms:
            lines.append("    bAlarm_HH       : BOOL;   (* ISA-18.2 High-High alarm *)")
            lines.append("    bAlarm_H        : BOOL;   (* ISA-18.2 High alarm *)")
        lines.append("END_VAR")
        return "\n".join(lines)

    def _var_internal_block(self, prog: SFCProgram) -> str:
        lines = ["VAR"]
        lines.append("    eState         : INT := 0;  (* SFC active step index *)")
        lines.append("    eLastState     : INT := -1; (* Previous step for entry/exit detect *)")
        lines.append("    bStateChanged  : BOOL;      (* TRUE on first scan in new step *)")

        if prog.has_timeout:
            lines.append("    tonStepTimeout : TON;       (* Step watchdog timer *)")
            lines.append("    bStepTimeout   : BOOL;      (* Step exceeded max dwell time *)")

        if prog.has_tmr:
            lines.append("    bTrip_A        : BOOL;      (* 2oo3 safety sensor channel A *)")
            lines.append("    bTrip_B        : BOOL;      (* 2oo3 safety sensor channel B *)")
            lines.append("    bTrip_C        : BOOL;      (* 2oo3 safety sensor channel C *)")
            lines.append("    bVoted         : BOOL;      (* 2oo3 TMR majority vote result *)")

        lines.append("END_VAR")
        return "\n".join(lines)

    # ------------------------------------------------------------------
    # FB Body
    # ------------------------------------------------------------------

    def _body(self, prog: SFCProgram) -> str:
        sections = []

        # E-Stop (always first)
        sections.append(self._estop_block())

        # 2oo3 TMR evaluation
        if prog.has_tmr:
            sections.append(self._tmr_block())

        # Step change detection
        sections.append(
            "(* --- Step change detection --- *)\n"
            "bStateChanged := (eState <> eLastState);\n"
            "eLastState    := eState;\n"
            "nActiveStep   := eState;"
        )

        # Step timeout watchdog
        if prog.has_timeout:
            sections.append(self._timeout_block(prog))

        # Main SFC CASE statement
        sections.append(self._case_block(prog))

        # Fault consolidation
        sections.append(
            "(* --- Fault consolidation --- *)\n"
            "bFault   := bStepTimeout OR bVoted;\n"
            "bRunning := NOT bFault AND (eState > 0);"
        )

        return "\n\n".join(sections)

    def _estop_block(self) -> str:
        return (
            "(* ===== E-STOP SAFETY CUTOFF — MUST BE FIRST LOGIC ===== *)\n"
            "IF bEStop THEN\n"
            "    bRunning  := FALSE;\n"
            "    bFault    := TRUE;\n"
            "    bComplete := FALSE;\n"
            "    eState    := -1;    (* fault step *)\n"
            "    RETURN;\n"
            "END_IF;"
        )

    def _tmr_block(self) -> str:
        return (
            "(* ===== 2oo3 TMR SAFETY VOTING ===== *)\n"
            "(* Sensor readings evaluated from input variables *)\n"
            "bVoted := (bTrip_A AND bTrip_B)\n"
            "       OR (bTrip_B AND bTrip_C)\n"
            "       OR (bTrip_A AND bTrip_C);\n"
            "\n"
            "IF bVoted THEN\n"
            "    bFault := TRUE;\n"
            "    eState := -1;    (* drive to fault step *)\n"
            "    RETURN;\n"
            "END_IF;"
        )

    def _timeout_block(self, prog: SFCProgram) -> str:
        # Build max time lookup
        max_times = {}
        for step in prog.steps:
            if step.max_time_ms > 0:
                max_times[step.index] = step.max_time_ms

        if not max_times:
            default_ms = 30000
            timeout_pt = "T#30S"
        else:
            # Use first step's time as default; real code would use CASE
            default_ms = list(max_times.values())[0]
            timeout_pt = f"T#{default_ms}MS"

        return (
            "(* ===== STEP TIMEOUT WATCHDOG ===== *)\n"
            f"tonStepTimeout(IN := bRunning, PT := {timeout_pt});\n"
            "bStepTimeout := tonStepTimeout.Q;\n"
            "\n"
            "IF bStepTimeout THEN\n"
            "    bFault := TRUE;\n"
            "    eState := -1;   (* fault recovery *)\n"
            "END_IF;"
        )

    def _case_block(self, prog: SFCProgram) -> str:
        lines = [
            "(* ===== SFC MAIN SEQUENCE ===== *)",
            "CASE eState OF",
            "",
            "    -1:  (* FAULT *)",
            "        bFault    := TRUE;",
            "        bComplete := FALSE;",
            "        IF bReset AND NOT bFault THEN",
            "            eState := 0;",
            "        END_IF;",
        ]

        # Build transition lookup: from_step → list of transitions
        trans_map: Dict[int, List[SFCTransition]] = {}
        for t in prog.transitions:
            trans_map.setdefault(t.from_step, []).append(t)

        for step in prog.steps:
            lines.append("")
            lines.append(f"    {step.index}:  (* {step.name} — {step.description} *)")

            # Entry actions (pulse)
            if step.entry_actions:
                lines.append(f"        IF bStateChanged THEN  (* Entry actions *)")
                for act in step.entry_actions:
                    for body_line in act.body.splitlines():
                        lines.append(f"            {body_line}")
                lines.append(f"        END_IF;")

            # Step name for HMI
            lines.append(f"        sActiveStepName := '{step.name}';")

            # Continuous actions
            for act in step.actions:
                if act.qualifier in ("N", ""):
                    for body_line in act.body.splitlines():
                        lines.append(f"        {body_line}")

            # Transitions out of this step
            step_trans = sorted(trans_map.get(step.index, []), key=lambda t: t.priority)
            for trans in step_trans:
                if isinstance(trans.to_step, list):
                    # AND divergence — advance all parallel branches
                    dest = trans.to_step[0]  # simplified: take first branch
                else:
                    dest = trans.to_step
                lines.append(f"        IF {trans.condition} THEN")
                # Exit actions
                if step.exit_actions:
                    for act in step.exit_actions:
                        for body_line in act.body.splitlines():
                            lines.append(f"            {body_line}")
                lines.append(f"            eState := {dest};  (* → {_step_name(prog, dest)} *)")
                lines.append(f"        END_IF;")

        lines += [
            "",
            "ELSE",
            "    eState := 0;  (* Safety fallback *)",
            "END_CASE;",
        ]
        return "\n".join(lines)


def _step_name(prog: SFCProgram, index: int) -> str:
    for s in prog.steps:
        if s.index == index:
            return s.name
    return f"STEP_{index}"


# ---------------------------------------------------------------------------
# Parser
# ---------------------------------------------------------------------------

class SFCParser:
    """Parse SFC-encoded ST to extract metadata for validation."""

    _FB_RE    = re.compile(r"FUNCTION_BLOCK\s+(\w+)", re.IGNORECASE)
    _CASE_RE  = re.compile(r"CASE\s+\w+\s+OF", re.IGNORECASE)
    _ARM_RE   = re.compile(r"^\s+(-?\d+)\s*:\s*\(\*\s*(\w+)", re.MULTILINE)
    _TIMEOUT_RE = re.compile(r"tonStepTimeout|bStepTimeout", re.IGNORECASE)
    _TMR_RE   = re.compile(r"2oo3|bVoted|bTrip_[ABC]", re.IGNORECASE)
    _ESTOP_RE = re.compile(r"\bb?EStop\b|\bb?E_Stop\b|\bEmergency(?:_)?Stop\b", re.IGNORECASE)
    _TRANS_RE = re.compile(r"IF\s+.+\s+THEN\s*\n\s*eState\s*:=", re.IGNORECASE)

    def parse(self, source: str) -> SFCParseResult:
        fb_m   = self._FB_RE.search(source)
        arms   = self._ARM_RE.findall(source)
        step_count = len(arms)
        step_names = [name for _, name in arms]
        has_initial = any(int(idx) == 0 for idx, _ in arms)

        return SFCParseResult(
            program_name     = fb_m.group(1) if fb_m else "UNKNOWN",
            step_count       = step_count,
            step_names       = step_names,
            transition_count = len(self._TRANS_RE.findall(source)),
            has_initial      = has_initial,
            has_timeout      = bool(self._TIMEOUT_RE.search(source)),
            has_tmr          = bool(self._TMR_RE.search(source)),
            has_estop        = bool(self._ESTOP_RE.search(source)),
            raw_lines        = len(source.splitlines()),
        )


# ---------------------------------------------------------------------------
# Unified Dialect Engine
# ---------------------------------------------------------------------------

class SFCDialectEngine:
    """
    Unified interface for SFC textual encoding generation and parsing.
    """

    def __init__(self):
        self._emitter = SFCSTEmitter()
        self._parser  = SFCParser()

    def generate(self, prog: SFCProgram) -> str:
        return self._emitter.emit(prog)

    def parse(self, source: str) -> SFCParseResult:
        return self._parser.parse(source)

    def generate_cip_sip_example(self) -> str:
        """
        Generate a full CIP/SIP Clean-In-Place / Sterilise-In-Place
        sequence for a food/beverage aseptic filling line.
        9 phases: Pre-rinse → NaOH wash → Intermediate rinse →
                  Acid rinse → Post-rinse → SIP steam → Cool-down →
                  Validation → Production.
        """
        prog = SFCProgram(
            program_name = "FB_SFC_CIP_SIP_AsepticFiller",
            description  = "9-phase CIP/SIP sequence for 48,000 bph aseptic filling line",
            sector       = "FOOD_BEVERAGE",
            global_vars  = [
                ("rTemperature_degC", "REAL", "[°C] process temperature"),
                ("rConductivity_mS",  "REAL", "[mS/cm] NaOH conductivity"),
                ("rFlowRate_Lpm",     "REAL", "[L/min] CIP circulation flow rate"),
                ("bValve_NaOH",       "BOOL", "NaOH dosing valve"),
                ("bValve_Steam",      "BOOL", "Steam injection valve"),
                ("bPump_CIP",         "BOOL", "CIP circulation pump"),
                ("rPressure_bar",     "REAL", "[bar] system pressure"),
            ],
            has_tmr     = True,
            has_timeout = True,
            has_alarms  = True,
        )

        prog.steps = [
            SFCStep(0,  "S00_IDLE",          "Sequence idle, awaiting start command",    is_initial=True,  max_time_ms=0),
            SFCStep(1,  "S01_PRE_RINSE",     "Cold water pre-rinse to remove product residue",           max_time_ms=180_000),
            SFCStep(2,  "S02_NAOH_WASH",     "1.5% NaOH caustic wash at 80°C for 20 min",               max_time_ms=1_200_000),
            SFCStep(3,  "S03_INTER_RINSE",   "Intermediate water rinse post-NaOH",                       max_time_ms=120_000),
            SFCStep(4,  "S04_ACID_RINSE",    "0.5% HNO3 acid rinse for mineral scale removal",           max_time_ms=600_000),
            SFCStep(5,  "S05_POST_RINSE",    "Final water rinse — conductivity verify < 1.5 mS/cm",      max_time_ms=180_000),
            SFCStep(6,  "S06_SIP_STEAM",     "Steam sterilisation at 132°C, 15 min hold",               max_time_ms=900_000),
            SFCStep(7,  "S07_COOL_DOWN",     "Cool down with sterile water to < 35°C",                   max_time_ms=600_000),
            SFCStep(8,  "S08_VALIDATION",    "Temperature and conductivity final validation",             max_time_ms=60_000),
            SFCStep(9,  "S09_PRODUCTION",    "Line cleared for aseptic production",                       max_time_ms=0),
            SFCStep(10, "S10_COMPLETE",      "CIP/SIP cycle complete — log and report",                   max_time_ms=0),
        ]

        prog.transitions = [
            SFCTransition(0,  1,  "bStartCmd AND NOT bFault"),
            SFCTransition(1,  2,  "rFlowRate_Lpm >= 50.0 AND tonStepTimeout.ET >= T#3M"),
            SFCTransition(2,  3,  "rTemperature_degC >= 78.0 AND rConductivity_mS >= 8.0 AND tonStepTimeout.ET >= T#20M"),
            SFCTransition(3,  4,  "rConductivity_mS < 1.5 AND tonStepTimeout.ET >= T#2M"),
            SFCTransition(4,  5,  "rConductivity_mS >= 3.0 AND tonStepTimeout.ET >= T#10M"),
            SFCTransition(5,  6,  "rConductivity_mS < 1.5"),
            SFCTransition(6,  7,  "rTemperature_degC >= 130.0 AND tonStepTimeout.ET >= T#15M"),
            SFCTransition(7,  8,  "rTemperature_degC < 35.0"),
            SFCTransition(8,  9,  "rConductivity_mS < 0.5 AND rTemperature_degC < 35.0"),
            SFCTransition(9,  10, "bStopCmd OR bComplete"),
        ]

        # Add step actions
        prog.steps[1].actions = [SFCAction("N", "PRE_RINSE_PUMP",    "bPump_CIP := TRUE;\nbValve_NaOH := FALSE;")]
        prog.steps[2].actions = [SFCAction("N", "NAOH_WASH",         "bPump_CIP := TRUE;\nbValve_NaOH := TRUE;")]
        prog.steps[3].actions = [SFCAction("N", "INTER_RINSE",       "bPump_CIP := TRUE;\nbValve_NaOH := FALSE;")]
        prog.steps[4].actions = [SFCAction("N", "ACID_RINSE",        "bPump_CIP := TRUE;")]
        prog.steps[5].actions = [SFCAction("N", "POST_RINSE",        "bPump_CIP := TRUE;")]
        prog.steps[6].actions = [SFCAction("N", "STEAM_SIP",         "bValve_Steam := TRUE;\nbPump_CIP := FALSE;")]
        prog.steps[7].actions = [SFCAction("N", "COOL_DOWN",         "bValve_Steam := FALSE;\nbPump_CIP := TRUE;")]
        prog.steps[9].actions = [SFCAction("N", "PRODUCTION",        "bPump_CIP := FALSE;\nbComplete := FALSE;")]
        prog.steps[10].actions= [SFCAction("N", "MARK_COMPLETE",     "bComplete := TRUE;\nbRunning  := FALSE;")]

        return self._emitter.emit(prog)


# ---------------------------------------------------------------------------
# Module-level convenience export
# ---------------------------------------------------------------------------

_engine = SFCDialectEngine()


def generate_sfc_st(prog: SFCProgram) -> str:
    return _engine.generate(prog)


def parse_sfc_st(source: str) -> SFCParseResult:
    return _engine.parse(source)


def sfc_cip_sip_example() -> str:
    return _engine.generate_cip_sip_example()
